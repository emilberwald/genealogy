import argparse
import copy
import datetime
import itertools
import logging
import pathlib
import re
import socket
import uuid
from collections import OrderedDict, defaultdict, namedtuple
from typing import DefaultDict, Dict, List, Set
from difflib import SequenceMatcher

import pkg_resources

from gedcomish.common import GEDCOM_LINES, NULL
from gedcomish.gedcom555ish.lineage_linked_gedcom_file import (
    CHIL,
    CHILD_TO_FAMILY_LINK,
    EVENT_DETAIL,
    FORM_RECORDS,
    GEDCOM_HEADER,
    GEDCOM_TRAILER,
    INDIVIDUAL_EVENT_DETAIL,
    LINEAGE_LINKED_GEDCOM_FILE,
    PERSONAL_NAME_PIECES,
    PERSONAL_NAME_STRUCTURE,
    PLACE_STRUCTURE,
    SPOUSE_TO_FAMILY_LINK,
    SUBMITTER_RECORD,
    XREF_SUBM,
    GEDCOM_FORM_HEADER_EXTENSIONs,
    INDIVIDUAL_EVENT_STRUCTUREs,
    LINEAGE_LINKED_RECORDs,
)
from gedcomish.gedcom555ish.primitives import XREF_FAM, XREF_INDI

logger = logging.getLogger(__name__)


def normalize_date(s):
    s = list(s.ljust(10, "0")[0:10])
    s = [c if c.isdigit() else "0" for c in s]
    s[4] = "-"
    s[7] = "-"
    return "".join(s)


def normalize_name(s):
    return set(s.replace(",", " ").split())


SAKREGISTER = "<CENTER><FONT SIZE=5>Sakregister</FONT></CENTER>"
ORTREGISTER = "<CENTER><FONT SIZE=5>Ortregister</FONT></CENTER>"
PERSONREGISTER = "<CENTER><FONT SIZE=5>Personregister</FONT></CENTER>"
FAMILY_REGEX = re.compile(
    r"""
        <CENTER>
        <FONT\sSIZE=5>
        \s*?
        Familj
        \s*?
        (?P<ID>[0-9]+)
        <\/FONT>
        <\/CENTER>
    """,
    re.VERBOSE,
)

FAMILY_RELATION_REGEX = re.compile(
    r"""
        \s*
        (?P<RELATIONTYPE>Gift|Sambo|Relation|Förlovad|Trolovad|Partner|Särbo)
        (
            (
                \s*?
                (?P<DATEMODIFIER>.+?)
            )?
            (
                \s+?
                (?P<RELATIONDAY>[0-9-.xX]+)
            )?
            (
                \s+?i\s+?
                (?P<RELATIONPLACE>.+?)
            )?
            \s+
            |(?P<RELATIONDETAIL>.+?)\s+
            |\s+
        )
        med
        \s*
    """,
    re.VERBOSE,
)

FAMILY_PERSON_REGEX = re.compile(
    r"""
        (
            \s*
            (?P<IS_CHILD>[*])
            \s*
        )?
        <B>
        (?P<FIRSTNAMES>.*?)
        (,
            (?P<SECONDNAMES>.*?)
        )?
        <\/B>
        \s*
        (
            \(
                \s*
                (?P<FAMILIES_PREFIX_DIRECTION>se|från)\s+?familj
                (?P<FAMILIES_PREFIX>\s*<A\sHREF=\#[0-9]+>[0-9]+<\/A>\s*,?\s*)+
            \)
            |
            \(
                (?P<FAMILIES_PREFIX_EVENT>.+?)
            \)
            \s*
        )?
        (
            ,
            \s*?
            född
            (
                \s+?(?P<BIRTHDAY>[0-9-.xX]+)
                |\s+?(?P<BIRTHDAY_CORRUPT>[^\s]+)
            )?
            (
                \s+?
                \(
                    (?P<BIRTHEVENT>.+?)?
                    \s*?
                    (?P<BIRTHEVENTDAY>[0-9-.xX]+)?
                \)
                \s*
            )?
            (
                \s+?i\s+?
                (?P<BIRTHPLACE>.+?)
            )?
        )?
        (
            ,
            \s*?
            död
            (
                \s+?(?P<DEATHDAY>[0-9-.xX]+)
                |\s+?(?P<DEATHDAY_CORRUPT>[^\s]+)
            )?
            (
                \s+?
                \(
                    (?P<DEATHEVENT>.+?)?
                    \s*?
                    (?P<DEATHEVENTDAY>[0-9-.xX]+)?
                \)
                \s*
            )?
            (
                \s+?i\s+?
                (?P<DEATHPLACE>.+?)
            )?
        )?
        (
            ,
            \s*?
            (?P<FAMILIES_SUFFIX_DIRECTION>se|från)\s+?familj
            (?P<FAMILIES_SUFFIX>\s*<A\sHREF=\#[0-9]+>[0-9]+<\/A>\s*,?\s*)+
        )?
        [.]
        (
            \s*?
            Bosatt
            (
                \s+?i\s+?
                (?P<HOMEPLACE>[^.]+?)
            )
            [.]
        )?
        (
            \s*?
            (?P<DETAILS>[^.]+?)
            (
                \s+?i\s+?
                (?P<DETAILSPLACE>[^.]+?)
            )?
            [.]
        )?
        (?P<NOTES>.*)
    """,
    re.VERBOSE,
)

FAMILY_UNION_REGEX = re.compile(
    r"""
        Barn:
        |Barn\s+i(?P<MARRIAGE_NUMERAL>.+?)giftet:
        |Barn\s+utan\s+känd\s+(?P<UNKNOWN_PARTNER_BIOLOGICAL_PARENTAL_ROLE>moder|fader):
        |Barn\s+med\s+(?P<PARTNER_NAME>[^:]+):
    """,
    re.VERBOSE,
)

ANCHOR_REGEX = re.compile(
    r"""
    <A\sHREF=\#(?P<HREF>[0-9]+)>
    (?P<REF>[0-9]+)
    <\/A>
    """,
    re.VERBOSE,
)

PERSONREGISTRY_PERSON_REGEX = re.compile(
    r"""
            <B>
            (?P<FIRSTNAMES>.*?)
            (,
                (?P<SECONDNAMES>.*?)
            )?
            <\/B>
            (
                \s+?f\s+?
                (?P<BIRTHDAY>[0-9-.xX]+)
            )?
            (
                \s+?i\s+?
                (?P<BIRTHPLACE>.+)
            )?
            """,
    re.VERBOSE,
)


def section_parts(sections: list, heading):
    for section in sections:
        section = section.replace("<P>", "")  # TODO: does <P> signify anything?
        lines = section.split("<BR>")
        assert heading in lines[0]
        for line_no, line in enumerate(line.strip() for line in lines[1:]):
            if (end := line.find("<A HREF=")) != -1:
                refs = list()
                for refpart in line[end:].split(","):
                    match = ANCHOR_REGEX.search(refpart)
                    assert match["HREF"] == match["REF"]
                    refs.append(match["REF"])
                yield line[0:end].strip(), refs
            elif line:
                raise ValueError(f"section without family references: {line}")
            else:
                logger.warning(f"empty line in {heading} at {line_no}: {line}")


RegistryDetail = namedtuple("RegistryDetail", ("detail",))
RegistryLocation = namedtuple("RegistryLocation", ("location",))
RegistryPerson = namedtuple("RegistryPerson", ("firstnames", "surnames", "birthday", "birthplace"))


def refine_detail_sections(sections: list) -> DefaultDict[int, List[RegistryDetail]]:
    """
        returns a defaultdict(list),
        which maps family id to a list of details
    """
    result = defaultdict(list)
    for text, refs in section_parts(sections, SAKREGISTER):
        for ref in refs:
            result[int(ref)].append(RegistryDetail(detail=text))
    return result


def refine_location_sections(sections: list) -> DefaultDict[int, List[RegistryLocation]]:
    """
        returns a defaultdict(list),
        which maps family id to a list of tuples, each tuple element signifying a part of an address,
        NOTE:
        location parts may have whitespace or comma signs between them in the family sections.
    """
    result = defaultdict(list)
    for text, refs in section_parts(sections, ORTREGISTER):
        for ref in refs:
            result[int(ref)].append(RegistryLocation(location=tuple(text.split())))
    return result


def refine_person_sections(sections: list) -> DefaultDict[int, List[RegistryPerson]]:
    result = defaultdict(list)
    for text, refs in section_parts(sections, PERSONREGISTER):
        for ref in refs:
            if (m := PERSONREGISTRY_PERSON_REGEX.search(text)) :
                if m["SECONDNAMES"]:
                    result[int(ref)].append(
                        RegistryPerson(
                            firstnames=tuple(m["SECONDNAMES"].split()) if m["SECONDNAMES"] else None,
                            surnames=tuple(m["FIRSTNAMES"].split()) if m["FIRSTNAMES"] else None,
                            birthday=m["BIRTHDAY"],
                            birthplace=tuple(m["BIRTHPLACE"].split()) if m["BIRTHPLACE"] else None,
                        )
                    )
                else:
                    result[int(ref)].append(
                        RegistryPerson(
                            firstnames=tuple(m["FIRSTNAMES"].split()) if m["FIRSTNAMES"] else None,
                            surnames=None,
                            birthday=m["BIRTHDAY"],
                            birthplace=tuple(m["BIRTHPLACE"].split()) if m["BIRTHPLACE"] else None,
                        )
                    )
    return result


Sections = namedtuple("Sections", ("family", "person", "location", "detail", "unknown", "source"))


def find_sections(text) -> Sections:
    sections = re.split("<HR WIDTH=500>", text)
    family_sections: Dict[int, str] = dict()
    person_sections: List[str] = list()
    detail_sections: List[str] = list()
    location_sections: List[str] = list()
    unknown_sections: List[str] = list()
    for section in sections:
        if SAKREGISTER in section:
            detail_sections.append(section)
        elif ORTREGISTER in section:
            location_sections.append(section)
        elif PERSONREGISTER in section:
            person_sections.append(section)
        elif (m := FAMILY_REGEX.search(section)) :
            if m["ID"] in family_sections:
                raise ValueError(f"FAMILY: duplicate id: {section}")
            elif m["ID"]:
                family_sections[int(m["ID"])] = section
            else:
                raise ValueError(f"FAMILY: missing id: {section}")
        else:
            unknown_sections.append(section)
    del sections, section, m
    logging.warning(f"UNKNOWN SECTIONS:{unknown_sections}")
    return Sections(
        family=family_sections,
        person=person_sections,
        location=location_sections,
        detail=detail_sections,
        unknown=unknown_sections,
        source=None,
    )


def index_sections(sections: Sections) -> DefaultDict[int, Sections]:
    details = refine_detail_sections(sections.detail)
    locations = refine_location_sections(sections.location)
    persons = refine_person_sections(sections.person)

    indexed_sections = defaultdict(Sections)
    found_fams: Set[int] = set()
    found_fams.update(details.keys())
    found_fams.update(locations.keys())
    found_fams.update(persons.keys())
    found_fams.update(sections.family.keys())
    for fam_id in found_fams:
        indexed_sections[fam_id] = Sections(
            family=sections.family[fam_id],
            person=persons[fam_id],
            location=locations[fam_id],
            detail=details[fam_id],
            unknown=None,
            source=None,
        )
    del details, locations, persons, found_fams
    return indexed_sections


def split_sections(text, registry) -> DefaultDict[int, Sections]:
    def trim(part):
        return " ".join(subpart.strip() for subpart in part.split())

    def unrecognized(text):
        return not any(
            [
                FAMILY_PERSON_REGEX.match(text),
                FAMILY_UNION_REGEX.match(text),
                FAMILY_RELATION_REGEX.match(text),
                IGNORE.match(text),
            ]
        )

    def lookahead_match(*, part_no, parts, current, regex):
        # check if there are more information in the following paragraph that belongs to the person
        merge = None
        merge_match = None
        merge_lookahead = None
        if (match := regex.match(current)) :
            merge = current
            merge_match = match
            merge_lookahead = part_no + 1
        for end in range(part_no + 2, len(parts)):
            trial_merge = trim(current + " ".join(parts[part_no + 1 : end]))
            remains = trim("".join(parts[end:]))
            if (match := regex.match(trial_merge)) :
                merge = trial_merge
                merge_match = match
                merge_lookahead = end
                if unrecognized(remains):
                    continue
                else:
                    break
        if merge and merge_match:
            value = merge_match.groupdict()
            merge_trimmed = trim(merge[0 : merge_match.start()] + merge[merge_match.end() :])
            nof_lookahead = merge_lookahead - (part_no + 1)
            if nof_lookahead > 0:
                logging.debug(f"MERGE {nof_lookahead} lookaheads:\n{value}")
            return merge_trimmed, value, nof_lookahead
        else:
            return None

    indexed_sections = index_sections(find_sections(text))
    split_sections = defaultdict(Sections)
    IGNORE = re.compile(r"^<A\sNAME=[0-9]+>$")
    for fam_id, data in indexed_sections.items():
        logging.debug(f"family:{data}")
        parts = [
            trim(part.replace("*", " * "))
            for part in itertools.chain.from_iterable(
                subpart.splitlines() for part in data.family.split("<P>") for subpart in part.split("<BR>")
            )
            if trim(part)
        ]
        if IGNORE.match(parts[0]):
            assert FAMILY_REGEX.search(parts[1])
            start = 2
        else:
            assert FAMILY_REGEX.search(parts[0])
            start = 1

        adults = list()
        children = list()
        unions = list()
        relations = list()
        unknown = list()
        remains = None
        part_it = enumerate(parts)
        while True:
            current_part = next(part_it, None)
            if current_part:
                part_no, current = current_part
                if remains:
                    current = trim(remains + " " + current)
                    remains = None
                if part_no < start:
                    continue
            else:
                break
            if current:
                person = lookahead_match(part_no=part_no, parts=parts, current=current, regex=FAMILY_PERSON_REGEX)
                relation = lookahead_match(part_no=part_no, parts=parts, current=current, regex=FAMILY_RELATION_REGEX)
                union = lookahead_match(part_no=part_no, parts=parts, current=current, regex=FAMILY_UNION_REGEX,)
                if person and not relation and not union:
                    # person entry
                    remains, value, nof_lookahead = person
                    for _ in range(0, nof_lookahead):
                        current_part = next(part_it, None)
                    if any("CORRUPT" in fieldkey for fieldkey, fieldval in value.items() if fieldval):
                        logging.warning(f"CORRUPTION:{fam_id}:\n{value}\n")
                    if value["IS_CHILD"]:
                        children.append((part_no, namedtuple("child", value.keys())(**value)))
                        logging.debug(f"added child:{fam_id}:\n{children[-1]}\n")
                    else:
                        adults.append((part_no, namedtuple("adult", value.keys())(**value)))
                        logging.debug(f"added adult:{fam_id}:\n{adults[-1]}\n")
                    continue
                if relation and not person and not union:
                    # header for relation entry
                    remains, value, nof_lookahead = relation
                    for _ in range(0, nof_lookahead):
                        current_part = next(part_it, None)
                    relations.append((part_no, namedtuple("relation", value.keys())(**value)))
                    logging.debug(f"added relation:{fam_id}:\n{relations[-1]}\n")
                    continue
                if union and not person and not relation:
                    # header for children entries
                    remains, value, nof_lookahead = union
                    for _ in range(0, nof_lookahead):
                        current_part = next(part_it, None)
                    unions.append((part_no, namedtuple("union", value.keys())(**value)))
                    logging.debug(f"added union:{fam_id}:\n{unions[-1]}\n")
                    continue
                if current.strip():
                    if IGNORE.match(current):
                        pass
                    else:
                        for start in range(0, len(current)):
                            if unrecognized(current[start:]):
                                continue
                            else:
                                unknown.append((part_no, current[0:start]))
                                logging.warning(
                                    f"added unknown:{fam_id}:\n{unknown[-1]}\ncontext:\n{current}\nfamily:\n{data.family}\n"
                                )
                                logging.debug(f"added unknown:{fam_id}:\n{unknown[-1]}\n")
                                remains = current[start:]
                                break
                        if current == remains:
                            raise NotImplementedError()

        if fam_id in split_sections:
            raise ValueError(f"Parser failure: family already present! {data}")
        else:
            family_values = {"adults": adults, "children": children, "unions": unions, "relations": relations}
            split_sections[fam_id] = Sections(
                family=namedtuple("family", family_values.keys())(**family_values),
                person=indexed_sections[fam_id].person,
                location=indexed_sections[fam_id].location,
                detail=indexed_sections[fam_id].detail,
                unknown=unknown,
                source=data.family,
            )
    return split_sections


def parsed_to_gedcom(path: pathlib.Path, sections):
    def partner_similarity(reg_person: RegistryPerson, union):
        return SequenceMatcher(
            None, v if (v := union.PARTNER_NAME) else "", "".join(v) if (v := reg_person.birthday) else ""
        ).ratio()

    def person_similarity(reg_person: RegistryPerson, fam_person):
        score = SequenceMatcher(
            None, v if (v := fam_person.BIRTHDAY) else "", "".join(v) if (v := reg_person.birthday) else ""
        ).ratio()
        score += SequenceMatcher(
            None, v if (v := fam_person.BIRTHDAY_CORRUPT) else "", "".join(v) if (v := reg_person.birthday) else "",
        ).ratio()
        score += SequenceMatcher(
            None, v if (v := fam_person.BIRTHPLACE) else "", "".join(v) if (v := reg_person.birthplace) else "",
        ).ratio()
        score += SequenceMatcher(
            None, v if (v := fam_person.FIRSTNAMES) else "", "".join(v) if (v := reg_person.firstnames) else "",
        ).ratio()
        score += SequenceMatcher(
            None, v if (v := fam_person.SECONDNAMES) else "", "".join(v) if (v := reg_person.firstnames) else "",
        ).ratio()
        score += SequenceMatcher(
            None, v if (v := fam_person.FIRSTNAMES) else "", "".join(v) if (v := reg_person.surnames) else ""
        ).ratio()
        score += SequenceMatcher(
            None, v if (v := fam_person.SECONDNAMES) else "", "".join(v) if (v := reg_person.surnames) else ""
        ).ratio()
        return score

    def location_similarity(reg_location: RegistryLocation, fam_location):
        return SequenceMatcher(
            None, v if (v := fam_location) else "", "".join(v) if (v := reg_location.location) else ""
        ).ratio()

    def detail_similarity(reg_detail: RegistryDetail, fam_detail):
        return SequenceMatcher(
            None, v if (v := fam_detail) else "", "".join(v) if (v := reg_detail.detail) else ""
        ).ratio()

    fam_records = set()
    indi_records = set()
    ids = defaultdict(uuid.uuid4)
    for fam_id, section in sections.items():

        famrecord = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
        famrecord.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM(XREF_FAM(fam_id))

        for person in section.person:
            ids[person]
        del person

        old_ids = {k:v for k,v in ids.items()}

        fam_persons = list()
        parent_part_no, parent = section.family.adults[0]
        for part_no, fam_person in section.family.adults:
            person = max(
                section.person, key=lambda reg_person, fam_person=fam_person: person_similarity(reg_person, fam_person),
            )
            ids[fam_person] = ids[person]
            fam_persons.append(ids[fam_person])
        del part_no, fam_person

        if section.family.children:
            for part_no, fam_person in section.family.children:
                person = max(
                    section.person,
                    key=lambda reg_person, fam_person=fam_person: person_similarity(reg_person, fam_person),
                )
                ids[fam_person] = ids[person]
                fam_persons.append(ids[fam_person])
            del part_no, fam_person
        if len(fam_persons) != len(set(fam_persons)):
            raise ValueError("persons not unique")
        del fam_persons


        if section.family.relations:
            for relation_part_no, relation in section.family.relations:
                # closest lexically after
                adult_part_no, adult = min(
                    (adult_part_no, adult)
                    for adult_part_no, adult in section.family.adults
                    if adult_part_no > relation_part_no
                )
                if ids[parent] == ids[adult]:
                    logging.warning(f"unexpected relationship between {parent} and {adult}")
                ids[relation] = (ids[parent], ids[adult])
            del adult_part_no, adult, relation_part_no, relation

        if section.family.unions:
            for union_part_no, union in section.family.unions:
                if union.PARTNER_NAME:
                    person = max(
                        section.person, key=lambda reg_person, union=union: partner_similarity(reg_person, union)
                    )
                    if not person:
                        raise ValueError(f"Could not find persons in {union} in {section.person}.")
                    if ids[parent] == ids[person]:
                        logging.warning(f"Unexpected parthenogenesis for {parent} and {person}.")
                    ids[union] = (ids[parent], ids[person])
                    del person
                elif union.MARRIAGE_NUMERAL:
                    marriage_no = 1
                    if "första" in union.MARRIAGE_NUMERAL:
                        marriage_no = 1
                    elif "andra" in union.MARRIAGE_NUMERAL:
                        marriage_no = 2
                    elif "tredje" in union.MARRIAGE_NUMERAL:
                        marriage_no = 3
                    elif "fjärde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 4
                    elif "femte" in union.MARRIAGE_NUMERAL:
                        marriage_no = 5
                    elif "sjätte" in union.MARRIAGE_NUMERAL:
                        marriage_no = 6
                    elif "sjunde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 7
                    elif "åttonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 8
                    elif "nionde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 9
                    elif "tionde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 10
                    elif "elfte" in union.MARRIAGE_NUMERAL:
                        marriage_no = 11
                    elif "tolfte" in union.MARRIAGE_NUMERAL:
                        marriage_no = 12
                    elif "trettonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 13
                    elif "fjortonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 14
                    elif "femtonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 15
                    elif "sextonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 16
                    elif "sjuttonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 17
                    elif "artonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 18
                    elif "nittonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 19
                    elif "tjugonde" in union.MARRIAGE_NUMERAL:
                        marriage_no = 20
                    else:
                        raise ValueError(f"Unrecognized numeral: {union.MARRIAGE_NUMERAL}")
                    marriage_counter = 0
                    for relation_part_no, relation in section.family.relations:
                        if "Gift" in relation.RELATIONTYPE:
                            marriage_counter += 1
                            if marriage_counter == marriage_no:
                                ids[union] = ids[relation]
                                del relation_part_no, relation, marriage_no, marriage_counter
                                break
                            else:
                                continue
                        raise ValueError(f"Could not find {union.MARRIAGE_NUMERAL} in {section.family.relations}.")
                elif union.UNKNOWN_PARTNER_BIOLOGICAL_PARENTAL_ROLE:
                    raise NotImplementedError("TODO: Add unknown partner info")
                else:
                    # closest lexically before
                    adult_part_no, adult = max(
                        (adult_part_no, adult)
                        for adult_part_no, adult in section.family.adults
                        if adult_part_no < union_part_no
                    )
                    ids[union] = (parent, adult)
                    del adult_part_no, adult
            del union_part_no, union

        new_ids = {k: v for k, v in ids.items() if k not in old_ids}
        #TODO: FIX BELOW

        parent_ids = families[fam_id][_PARENT_IN_FAMILY]
        if parent_ids:
            famrecord.FAM.HUSB = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.HUSB(parent_ids.pop())
        if parent_ids:
            famrecord.FAM.WIFE = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.WIFE(parent_ids.pop())
        if parent_ids:
            logger.warning(f"unselected parents:{[merges[parent_id] for parent_id in parent_ids]}")

        for child_id in families[fam_id][_CHILD_IN_FAMILY]:
            if not isinstance(famrecord.FAM.CHILs, list):
                famrecord.FAM.CHILs: LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.CHILs = list()
            famrecord.FAM.CHILs.append(CHIL(child_id))
        fam_records.add(famrecord)
    for person_id, person in merges.items():
        indirecord = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD()
        indirecord.INDI = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI(XREF_INDI(person_id))
        if (_FIRST_NAMES in person) and (_LAST_NAMES in person):
            if not isinstance(indirecord.INDI.PERSONAL_NAME_STRUCTUREs, list):
                indirecord.INDI.PERSONAL_NAME_STRUCTUREs = list()
            name = PERSONAL_NAME_STRUCTURE()
            name.NAME = PERSONAL_NAME_STRUCTURE.NAME(
                " ".join(person[_FIRST_NAMES]) + "/" + " ".join(person[_LAST_NAMES]) + "/"
            )
            name.NAME.PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES()
            name.NAME.PERSONAL_NAME_PIECES.GIVN = PERSONAL_NAME_PIECES.GIVN(" ".join(person[_FIRST_NAMES]))
            name.NAME.PERSONAL_NAME_PIECES.SURN = PERSONAL_NAME_PIECES.SURN(" ".join(person[_LAST_NAMES]))
            indirecord.INDI.PERSONAL_NAME_STRUCTUREs.append(name)
        if _NAME in person:
            if not isinstance(indirecord.INDI.PERSONAL_NAME_STRUCTUREs, list):
                indirecord.INDI.PERSONAL_NAME_STRUCTUREs = list()
            name = PERSONAL_NAME_STRUCTURE()
            name.NAME = str(person[_NAME][0])
            indirecord.INDI.PERSONAL_NAME_STRUCTUREs.append(name)
        if _BIRTHDAY in person:
            if not isinstance(indirecord.INDI.INDIVIDUAL_EVENT_STRUCTUREs, list):
                indirecord.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()
            birth = INDIVIDUAL_EVENT_STRUCTUREs.BIRT()
            birth.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
            birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
            birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(str(person[_BIRTHDAY][0]))
            if _BIRTHPLACE in person:
                birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
                birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
                    str(person[_BIRTHPLACE][0])
                )
            indirecord.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(birth)
        if _DEATHDAY in person:
            if not isinstance(indirecord.INDI.INDIVIDUAL_EVENT_STRUCTUREs, list):
                indirecord.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()
            death = INDIVIDUAL_EVENT_STRUCTUREs.DEAT(NULL())
            death.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
            death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
            death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(str(person[_DEATHDAY][0]))
            if _DEATHPLACE in person:
                death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
                death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
                    str(person[_DEATHPLACE][0])
                )
            indirecord.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(death)
        if _CHILD_IN_FAMILY in person and person[_CHILD_IN_FAMILY]:
            if not isinstance(indirecord.INDI.CHILD_TO_FAMILY_LINKs, list):
                indirecord.INDI.CHILD_TO_FAMILY_LINKs = list()
            for fam_id in person[_CHILD_IN_FAMILY]:
                child_to_family_link = CHILD_TO_FAMILY_LINK()
                child_to_family_link.FAMC = CHILD_TO_FAMILY_LINK.FAMC(fam_id)
                indirecord.INDI.CHILD_TO_FAMILY_LINKs.append(child_to_family_link)
        if _PARENT_IN_FAMILY in person and person[_PARENT_IN_FAMILY]:
            if not isinstance(indirecord.INDI.SPOUSE_TO_FAMILY_LINKs, list):
                indirecord.INDI.SPOUSE_TO_FAMILY_LINKs = list()
            for fam_id in person[_PARENT_IN_FAMILY]:
                spouse_to_family_link = SPOUSE_TO_FAMILY_LINK()
                spouse_to_family_link.FAMS = SPOUSE_TO_FAMILY_LINK.FAMS(fam_id)
                indirecord.INDI.SPOUSE_TO_FAMILY_LINKs.append(spouse_to_family_link)
        indi_records.add(indirecord)

    ex = LINEAGE_LINKED_GEDCOM_FILE()
    ex.GEDCOM_HEADER = GEDCOM_HEADER()
    ex.GEDCOM_HEADER.HEAD = GEDCOM_HEADER.HEAD()
    ex.GEDCOM_HEADER.HEAD.GEDC = GEDCOM_HEADER.HEAD.GEDC()
    ex.GEDCOM_HEADER.HEAD.GEDC.VERS = GEDCOM_HEADER.HEAD.GEDC.VERS("5.5.5")
    ex.GEDCOM_HEADER.HEAD.GEDC.FORM = GEDCOM_HEADER.HEAD.GEDC.FORM("LINEAGE-LINKED")
    ex.GEDCOM_HEADER.HEAD.GEDC.FORM.VERS = GEDCOM_HEADER.HEAD.GEDC.FORM.VERS("5.5.5")
    ex.GEDCOM_HEADER.HEAD.CHAR = GEDCOM_HEADER.HEAD.CHAR("UTF-8")
    ex.GEDCOM_FORM_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION()
    ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR(
        "genealogy.gedcomish"
    )
    ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.VERS = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.VERS(
        pkg_resources.get_distribution("genealogy").version
    )
    ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.DATA = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.DATA(
        path.parent.name + ": " + str(path.name)
    )
    ex.GEDCOM_FORM_HEADER_EXTENSION.DATE = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.DATE(
        datetime.datetime.now()
    )
    ex.GEDCOM_FORM_HEADER_EXTENSION.DATE.TIME = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.DATE.TIME(
        datetime.datetime.now()
    )
    subm_id = XREF_SUBM(create=True)
    ex.GEDCOM_FORM_HEADER_EXTENSION.SUBM = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SUBM(subm_id)
    ex.FORM_RECORDS = FORM_RECORDS()
    ex.FORM_RECORDS.SUBMITTER_RECORD = SUBMITTER_RECORD()
    ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM = SUBMITTER_RECORD.SUBM(subm_id)
    ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.NAME = SUBMITTER_RECORD.SUBM.NAME(socket.gethostname())
    ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs = list()
    ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.extend(fam_records)
    ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.extend(indi_records)
    ex.GEDCOM_TRAILER = GEDCOM_TRAILER()
    ex.GEDCOM_TRAILER.TRLR = GEDCOM_TRAILER.TRLR()
    lines = GEDCOM_LINES()
    lines = ex(lines=lines, delta_level=0)
    result = lines(0)
    outfile = path.with_suffix(".ged")
    outfile.write_text(result, encoding="utf-8-sig")
    logger.info(f"GEDCOM output: {outfile}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse html file in holger-like format.")
    parser.add_argument("--holger", type=pathlib.Path, help="path to .htm file")
    pargs = parser.parse_args()
    sections = split_sections(pargs.holger.read_text(), dict())
    parsed_to_gedcom(pargs.holger, sections)
