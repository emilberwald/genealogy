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
from difflib import SequenceMatcher
from typing import DefaultDict, Dict, List, Optional, Set

import pkg_resources

from .configure import configure
from gedcomish.common import GEDCOM_LINES, NULL
from gedcomish.gedcom555ish.lineage_linked_gedcom_file import (
    ADDRESS_STRUCTURE,
    ASSOCIATION_STRUCTURE,
    CHANGE_DATE,
    CHIL,
    CHILD_TO_FAMILY_LINK,
    EVENT_DETAIL,
    FAMILY_EVENT_DETAIL,
    FORM_RECORDS,
    GEDCOM_HEADER,
    GEDCOM_TRAILER,
    INDIVIDUAL_EVENT_DETAIL,
    LINEAGE_LINKED_GEDCOM_FILE,
    MULTIMEDIA_LINK,
    PERSONAL_NAME_PIECES,
    PERSONAL_NAME_STRUCTURE,
    PLACE_STRUCTURE,
    REFN,
    SOURCE_CITATION,
    SOURCE_REPOSITORY_CITATION,
    SPOUSE_TO_FAMILY_LINK,
    SUBMITTER_RECORD,
    EVENs,
    FAMILY_EVENT_STRUCTUREs,
    GEDCOM_FORM_HEADER_EXTENSIONs,
    INDIVIDUAL_ATTRIBUTE_STRUCTUREs,
    INDIVIDUAL_EVENT_STRUCTUREs,
    LINEAGE_LINKED_RECORDs,
    NOTE_STRUCTUREs,
    TEXTs,
)
from gedcomish.gedcom555ish.primitives import XREF_FAM, XREF_INDI, XREF_SUBM

configure()
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
        ^
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
        ^
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
        ^
        (
            Barn:
            |Barn\s+i(?P<MARRIAGE_NUMERAL>.+?)giftet:
            |Barn\s+utan\s+känd\s+(?P<UNKNOWN_PARTNER_BIOLOGICAL_PARENTAL_ROLE>moder|fader):
            |Barn\s+med\s+(?P<PARTNER_NAME>[^:]+):
        )
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

IGNORE = re.compile(r"^<A\sNAME=[0-9]+>$")


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
                    assert match
                    assert match["HREF"] == match["REF"]
                    refs.append(match["REF"])
                yield line[0:end].strip(), refs
            elif line:
                raise ValueError(f"section without family references: {line}")
            else:
                logger.warning(f"empty line in {heading} at {line_no}: {line}")


RegistryDetail = namedtuple("RegistryDetail", ("detail",))
RegistryLocation = namedtuple("RegistryLocation", ("location",))
RegistryPerson = namedtuple("RegistryPerson", ("firstnames", "surnames", "birthday", "birthplace", "families"))


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
                            families=tuple(int(ref) for ref in refs),
                        )
                    )
                else:
                    result[int(ref)].append(
                        RegistryPerson(
                            firstnames=tuple(m["FIRSTNAMES"].split()) if m["FIRSTNAMES"] else None,
                            surnames=None,
                            birthday=m["BIRTHDAY"],
                            birthplace=tuple(m["BIRTHPLACE"].split()) if m["BIRTHPLACE"] else None,
                            families=tuple(int(ref) for ref in refs),
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
    logger.warning(f"UNKNOWN SECTIONS:{unknown_sections}")
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
    return indexed_sections


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

    if (part_no + 1 == len(parts)) and (match := regex.match(current)):
        merge = current
        merge_match = match
        merge_lookahead = part_no + 1
    else:
        for end in range(part_no + 1, len(parts)):
            trial_merge = trim(" ".join((current, " ".join(parts[part_no + 1 : end]))))
            remains = trim(" ".join(parts[end:]))
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
        remains = trim(merge[0 : merge_match.start()] + merge[merge_match.end() :])
        nof_lookahead = merge_lookahead - (part_no + 1)
        if nof_lookahead > 0:
            logger.debug(f"MERGE {nof_lookahead} lookaheads:\n{value}")
        return remains, value, nof_lookahead
    else:
        return None


def split_section(fam_id, source):
    parts = [
        trim(part)
        for part in itertools.chain.from_iterable(
            subpart.splitlines() for part in source.split("<P>") for subpart in part.split("<BR>")
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
    unknowns = list()
    remains = None
    part_it = enumerate(parts)
    part_no = None
    current = None
    while True:
        if remains:
            unknowns.append((part_no, remains))
            logger.warning(f"added unknown (remains):{fam_id}:\n{unknowns[-1]}\ncontext:\n{current}\n")
            remains = None
        current_part = next(part_it, None)
        if current_part:
            part_no, current = current_part
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
                if remains:
                    logger.warning(f"match has remains:{person}")
                for _ in range(0, nof_lookahead):
                    current_part = next(part_it, None)
                if any("CORRUPT" in fieldkey for fieldkey, fieldval in value.items() if fieldval):
                    logger.warning(f"CORRUPTION:{fam_id}:\n{value}\n")
                if value["IS_CHILD"]:
                    children.append((part_no, namedtuple("child", value.keys())(**value)))
                    logger.debug(f"added child:{fam_id}:\n{children[-1]}\n")
                else:
                    adults.append((part_no, namedtuple("adult", value.keys())(**value)))
                    logger.debug(f"added adult:{fam_id}:\n{adults[-1]}\n")
                continue
            if relation and not person and not union:
                # header for relation entry
                remains, value, nof_lookahead = relation
                if remains:
                    logger.warning(f"match has remains:{relation}")
                for _ in range(0, nof_lookahead):
                    current_part = next(part_it, None)
                relations.append((part_no, namedtuple("relation", value.keys())(**value)))
                logger.debug(f"added relation:{fam_id}:\n{relations[-1]}\n")
                continue
            if union and not person and not relation:
                # header for children entries
                remains, value, nof_lookahead = union
                if remains:
                    logger.warning(f"match has remains:{union}")
                for _ in range(0, nof_lookahead):
                    current_part = next(part_it, None)
                unions.append((part_no, namedtuple("union", value.keys())(**value)))
                logger.debug(f"added union:{fam_id}:\n{unions[-1]}\n")
                continue
            if current.strip():
                if IGNORE.match(current):
                    pass
                else:
                    for start in range(0, len(current)):
                        if unrecognized(current[start:]):
                            continue
                        else:
                            unknowns.append((part_no, current[0:start]))
                            logger.warning(f"added unknown:{fam_id}:\n{unknowns[-1]}\ncontext:\n{current}\n")
                            logger.debug(f"added unknown:{fam_id}:\n{unknowns[-1]}\n")
                            remains = current[start:]
                            break
                    if current == remains:
                        raise NotImplementedError()
    family_values = {
        "adults": adults,
        "children": children,
        "unions": unions,
        "relations": relations,
        "unknowns": unknowns,
    }
    return namedtuple("family", family_values.keys())(**family_values)


def split_sections(text, registry) -> DefaultDict[int, Sections]:
    indexed_sections = index_sections(find_sections(text))
    split_sections = defaultdict(Sections)
    for fam_id, data in indexed_sections.items():
        if fam_id in split_sections:
            raise ValueError(f"Parser failure: family already present! {data}")
        logger.debug(f"family:{data}")
        section = Sections(
            family=split_section(fam_id, data.family),
            person=indexed_sections[fam_id].person,
            location=indexed_sections[fam_id].location,
            detail=indexed_sections[fam_id].detail,
            unknown=None,
            source=data.family,
        )
        split_sections[fam_id] = section
    return split_sections


def partner_similarity(reg_person: RegistryPerson, union):
    reg_name = " ".join(reg_person.firstnames) if reg_person.firstnames else ""
    reg_name += " ".join(reg_person.surnames) if reg_person.surnames else ""
    return SequenceMatcher(None, v if (v := union.PARTNER_NAME) else "", reg_name).ratio()


def person_similarity(reg_person: RegistryPerson, fam_person, weight=2.0):
    score = (
        SequenceMatcher(
            None, v if (v := fam_person.BIRTHDAY) else "", "".join(v) if (v := reg_person.birthday) else ""
        ).ratio()
        * weight
    )
    score += (
        SequenceMatcher(
            None, v if (v := fam_person.BIRTHDAY_CORRUPT) else "", "".join(v) if (v := reg_person.birthday) else "",
        ).ratio()
        * weight
    )
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
    return SequenceMatcher(None, v if (v := fam_detail) else "", "".join(v) if (v := reg_detail.detail) else "").ratio()


def get_partner_by_partner_name(*, union, section, partner_similarity):
    return max(section.person, key=lambda reg_person, union=union: partner_similarity(reg_person, union))


def get_partners_by_marriage_numeral(*, fam_id, ids, union, section):
    marriage_no = None
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
    elif union.MARRIAGE_NUMERAL.strip():
        raise ValueError(f"Unrecognized numeral: {union.MARRIAGE_NUMERAL}")
    else:
        logger.warning("Marriage numeral is whitespace. Will use default value.")
        marriage_no = 1
    marriage_counter = 0
    for _, relation in section.family.relations:
        if "Gift" in relation.RELATIONTYPE:
            marriage_counter += 1
            if marriage_counter == marriage_no:
                return tuple(
                    adult
                    for adult, adult_id in ids.items()
                    if (adult_id in ids[(fam_id, relation)]) and (type(adult).__name__ == "adult")
                )
            else:
                continue
    raise ValueError(f"Could not find {union.MARRIAGE_NUMERAL} in {section.family.relations}.")


def get_closest_partner(*, union, section: Sections, part_after: int):
    adult_part_no, adult = max(
        (adult_part_no, adult) for adult_part_no, adult in section.family.adults if adult_part_no < part_after
    )
    return adult


def validate_partners_in_union(*, ids, partners):
    partner_ids = [ids[partner] for partner in partners]
    nof_partners = len(partner_ids)
    nof_unique_partners = len(set(partner_ids))
    if nof_partners != nof_unique_partners:
        if nof_unique_partners == 0:
            logger.warning(f"Unexpected genesis:\n{partners}")
        elif nof_partners == 2 and nof_unique_partners == 1:
            logger.warning(f"Unexpected parthenogenesis:\n{partners}")
        else:
            logger.warning(f"Unexpected multitude of parents:\n{partners}")


def get_parents(*, fam_id, ids, union, section: Sections, partner_similarity, union_part_no: int):
    _, parent = section.family.adults[0]
    parents = None
    if union.PARTNER_NAME:
        parents = (
            parent,
            get_partner_by_partner_name(union=union, section=section, partner_similarity=partner_similarity),
        )
    elif union.MARRIAGE_NUMERAL:
        parents = get_partners_by_marriage_numeral(fam_id=fam_id, ids=ids, union=union, section=section)
    elif union.UNKNOWN_PARTNER_BIOLOGICAL_PARENTAL_ROLE:
        parents = (parent, union.UNKNOWN_PARTNER_BIOLOGICAL_PARENTAL_ROLE)
    else:
        parents = (parent, get_closest_partner(union=union, section=section, part_after=union_part_no))
    return parents


def get_children(*, section: Sections, part_before: int, part_after: Optional[int]):
    return tuple(
        child
        for child_part_no, child in section.family.children
        if (part_before < child_part_no) and ((child_part_no < part_after) if part_after else True)
    )


def get_gedcom_individual(ids, fam_id, section, person):
    indi_record = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD()
    indi_record.INDI = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI(XREF_INDI(ids[person]))
    logger.debug(f"INDI using {ids[person]}")

    for reg_person in (
        reg_person
        for reg_person, reg_person_id in ids.items()
        if (reg_person_id == ids[person]) and isinstance(reg_person, RegistryPerson)
    ):
        if reg_person.firstnames or reg_person.surnames:
            if not isinstance(indi_record.INDI.PERSONAL_NAME_STRUCTUREs, list):
                indi_record.INDI.PERSONAL_NAME_STRUCTUREs = list()

            if reg_person.firstnames and reg_person.surnames:
                name = PERSONAL_NAME_STRUCTURE()
                name.NAME = PERSONAL_NAME_STRUCTURE.NAME(
                    " ".join(reg_person.firstnames) + "/" + " ".join(reg_person.surnames) + "/"
                )
                name.NAME.PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES()
                name.NAME.PERSONAL_NAME_PIECES.GIVN = PERSONAL_NAME_PIECES.GIVN(" ".join(reg_person.firstnames))
                name.NAME.PERSONAL_NAME_PIECES.SURN = PERSONAL_NAME_PIECES.SURN(" ".join(reg_person.surnames))
            elif reg_person.firstnames:
                name = PERSONAL_NAME_STRUCTURE()
                name.NAME = PERSONAL_NAME_STRUCTURE.NAME(" ".join(reg_person.firstnames))
                name.NAME.PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES()
                name.NAME.PERSONAL_NAME_PIECES.GIVN = PERSONAL_NAME_PIECES.GIVN(" ".join(reg_person.firstnames))
            elif reg_person.surnames:
                name = PERSONAL_NAME_STRUCTURE()
                name.NAME = PERSONAL_NAME_STRUCTURE.NAME("/" + " ".join(reg_person.surnames) + "/")
                name.NAME.PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES()
                name.NAME.PERSONAL_NAME_PIECES.SURN = PERSONAL_NAME_PIECES.SURN(" ".join(reg_person.surnames))
            else:
                RuntimeError(reg_person)

            indi_record.INDI.PERSONAL_NAME_STRUCTUREs.append(name)
        else:
            raise ValueError(reg_person)

        if reg_person.birthday:
            if not isinstance(indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs, list):
                indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()
            birth = INDIVIDUAL_EVENT_STRUCTUREs.BIRT()
            birth.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
            birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
            birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(reg_person.birthday)
            if person.BIRTHPLACE:
                if section.location:
                    location = max(
                        section.location,
                        key=lambda reg_location, fam_location=person.BIRTHPLACE: location_similarity(
                            reg_location, fam_location
                        ),
                    )
                    birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
                    birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
                        ", ".join(location.location)
                    )
                else:
                    birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
                    birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
                        person.BIRTHPLACE
                    )
            indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(birth)
        if person.DEATHDAY or person.DEATHDAY_CORRUPT:
            if not isinstance(indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs, list):
                indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()
            death = INDIVIDUAL_EVENT_STRUCTUREs.DEAT(NULL())
            death.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
            death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
            if person.DEATHDAY:
                death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(person.DEATHDAY)
            elif person.DEATHDAY_CORRUPT:
                death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(person.DEATHDAY_CORRUPT)
            else:
                raise RuntimeError()
            if person.DEATHPLACE:
                death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
                death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
                    person.DEATHPLACE
                )
            indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(death)
        if person.BIRTHEVENT:
            if not isinstance(indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs, list):
                indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()
            # TODO: classify event properly
            event = INDIVIDUAL_EVENT_STRUCTUREs.EVEN(NULL())
            event.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
            event.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
            if person.BIRTHEVENTDAY:
                event.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(person.BIRTHEVENTDAY)
            indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(event)
        if person.DEATHEVENT:
            if not isinstance(indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs, list):
                indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()
            # TODO: classify event properly
            event = INDIVIDUAL_EVENT_STRUCTUREs.EVEN(NULL())
            event.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
            event.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
            if person.DEATHEVENTDAY:
                event.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(person.DEATHEVENTDAY)
            indi_record.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(event)
        if person.DETAILS:
            if person.DETAILSPLACE:
                # TODO: use "sakregister"
                if not isinstance(indi_record.INDI.INDIVIDUAL_ATTRIBUTE_STRUCTUREs, list):
                    indi_record.INDI.INDIVIDUAL_ATTRIBUTE_STRUCTUREs = list()
                fact = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.FACT(person.DETAILS)
                fact.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.FACT.TYPE("DETAILS")
                fact.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
                fact.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
                fact.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
                fact.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
                    person.DETAILSPLACE
                )
                indi_record.INDI.INDIVIDUAL_ATTRIBUTE_STRUCTUREs.append(fact)
            else:
                if not isinstance(indi_record.INDI.NOTE_STRUCTUREs, list):
                    indi_record.INDI.NOTE_STRUCTUREs = list()
                note = NOTE_STRUCTUREs.NOTE_STRUCTURE_USER_TEXT()
                note.NOTE = NOTE_STRUCTUREs.NOTE_STRUCTURE_USER_TEXT.NOTE(person.DETAILS.strip())
                indi_record.INDI.NOTE_STRUCTUREs.append(note)
        if person.NOTES and person.NOTES.strip():
            if not isinstance(indi_record.INDI.NOTE_STRUCTUREs, list):
                indi_record.INDI.NOTE_STRUCTUREs = list()
            note = NOTE_STRUCTUREs.NOTE_STRUCTURE_USER_TEXT()
            note.NOTE = NOTE_STRUCTUREs.NOTE_STRUCTURE_USER_TEXT.NOTE(person.NOTES.strip())
            indi_record.INDI.NOTE_STRUCTUREs.append(note)
        child_to_family_links = list()
        spouse_to_family_links = list()
        if reg_person.families:
            for fam_id_alt in reg_person.families:
                alt_section = sections[fam_id_alt]
                if ids[person] in alt_section.family.children:
                    nof_unions = 0
                    for union_part_no, union in alt_section.family.unions:
                        if ids[person] in union.children:
                            # person participates as a child in a union
                            child_to_family_link = CHILD_TO_FAMILY_LINK()
                            child_to_family_link.FAMC = CHILD_TO_FAMILY_LINK.FAMC(ids[ids[(fam_id, union)]])
                            logger.debug(f"FAMC using {ids[ids[(fam_id, union)]]}")
                            child_to_family_links.append(child_to_family_link)
                            nof_unions += 1
                    if not nof_unions:
                        # person participates as a child, but not in any union
                        child_to_family_link = CHILD_TO_FAMILY_LINK()
                        child_to_family_link.FAMC = CHILD_TO_FAMILY_LINK.FAMC(ids[fam_id_alt])
                        logger.debug(f"FAMC using {ids[fam_id_alt]}")
                        child_to_family_links.append(child_to_family_link)
                if ids[person] in alt_section.family.adults:
                    nof_unions = 0
                    for union_part_no, union in alt_section.family.unions:
                        if ids[person] in union.children:
                            # person participates as an adult in a union
                            spouse_to_family_link = SPOUSE_TO_FAMILY_LINK()
                            spouse_to_family_link.FAMS = SPOUSE_TO_FAMILY_LINK.FAMS(ids[ids[(fam_id, union)]])
                            logger.debug(f"FAMS using {ids[ids[(fam_id, union)]]}")
                            spouse_to_family_links.append(spouse_to_family_link)
                            nof_unions += 1
                    if not nof_unions:
                        # person participates as an adult, but not in any union
                        spouse_to_family_link = SPOUSE_TO_FAMILY_LINK()
                        spouse_to_family_link.FAMS = SPOUSE_TO_FAMILY_LINK.FAMS(ids[fam_id_alt])
                        logger.debug(f"FAMS using {ids[fam_id_alt]}")
                        spouse_to_family_links.append(spouse_to_family_link)

        if child_to_family_links:
            if not isinstance(indi_record.INDI.CHILD_TO_FAMILY_LINKs, list):
                indi_record.INDI.CHILD_TO_FAMILY_LINKs = list()
            indi_record.INDI.CHILD_TO_FAMILY_LINKs.extend(child_to_family_links)
        if spouse_to_family_links:
            if not isinstance(indi_record.INDI.SPOUSE_TO_FAMILY_LINKs, list):
                indi_record.INDI.SPOUSE_TO_FAMILY_LINKs = list()
            indi_record.INDI.SPOUSE_TO_FAMILY_LINKs.extend(spouse_to_family_links)
    return indi_record


def add_reg_person_info(ids, sections):
    for fam_id, section in sections.items():
        logger.debug(f"{fam_id},{section}")
        for person in section.person:
            if len(set(section.person)) != len(section.person):
                logging.warning(f"could not disambiguate some persons:{section.person}")
            if person not in ids:
                ids[person]
                logger.debug(f"added registry person id:\n{person}\n{ids[person]}")


def add_family_info(ids, sections):
    for fam_id, section in sections.items():
        logger.debug(f"{fam_id},{section}")

        persons_in_fam_id = list()
        persons_in_fam = list()
        parent_part_no, parent = section.family.adults[0]
        for part_no, fam_person in section.family.adults:
            persons_descending = [
                person
                for person in sorted(
                    section.person, key=lambda person, fam_person=fam_person: person_similarity(person, fam_person),
                )
                if person not in persons_in_fam
            ]
            if persons_descending:
                person = persons_descending.pop()
                ids[fam_person] = ids[person]
                logger.debug(
                    f"added (shared) family person id:\n{fam_person}\n{ids[fam_person]}\nselected:\n{(person_similarity(person, fam_person),person)}\nothers:\n{[(person_similarity(person, fam_person),person) for person in persons_descending]}\nexcluded:\n{[(person_similarity(person, fam_person),person) for person in persons_in_fam]}\n"
                )
                persons_in_fam.append(person)
                persons_in_fam_id.append(ids[person])
            else:
                raise ValueError(f"Could not find matching person for {fam_person}")

        if section.family.children:
            for part_no, fam_person in section.family.children:
                persons_descending = [
                    person
                    for person in sorted(
                        section.person,
                        key=lambda reg_person, fam_person=fam_person: person_similarity(reg_person, fam_person),
                    )
                    if person not in persons_in_fam
                ]
                if persons_descending:
                    person = persons_descending.pop()
                    ids[fam_person] = ids[person]
                    logger.debug(
                        f"added (shared) family person id:\n{fam_person}\n{ids[fam_person]}\nselected:\n{(person_similarity(person, fam_person),person)}\nothers:\n{[(person_similarity(person, fam_person),person) for person in persons_descending]}\nexcluded:\n{[(person_similarity(person, fam_person),person) for person in persons_in_fam]}\n"
                    )
                    persons_in_fam.append(person)
                    persons_in_fam_id.append(ids[person])
                else:
                    logging.warning(f"Could not find matching person for {fam_person}")

        if len(persons_in_fam_id) != len(set(persons_in_fam_id)):
            raise ValueError("persons not unique")

        if section.family.relations:
            for relation_part_no, relation in section.family.relations:
                # closest lexically after
                try:
                    _, adult = min(
                        (adult_part_no, adult)
                        for adult_part_no, adult in section.family.adults
                        if adult_part_no > relation_part_no
                    )
                except Exception as e:
                    logger.error(e)
                    try:
                        _, adult = min(
                            (unknown_part_no, unknown)
                            for unknown_part_no, unknown in section.family.unknowns
                            if unknown_part_no > relation_part_no
                        )
                    except Exception as e:
                        logger.error(e)
                        adult = None
                if not adult:
                    logger.warning(f"Unexpected relationship between\n{parent}\nand missing\n{adult}\n")
                    ids[(fam_id, relation)] = (ids[parent], adult)
                    logger.debug(f"added relation id:\n{(fam_id,relation)}\n{ids[(fam_id,relation)]}")
                    ids[ids[(fam_id, relation)]]
                    logger.debug(
                        f"added relation id id:\n{(fam_id,relation)}\n{ids[(fam_id,relation)]}\n{ids[ids[(fam_id,relation)]]}\n"
                    )
                elif type(adult).__name__ == "adult":
                    if (ids[parent]) == (ids[adult]):
                        logger.warning(f"Unexpected self-relationship:\n{parent}\nand\n{adult}\n")
                    ids[(fam_id, relation)] = (ids[parent], ids[adult])
                    logger.debug(f"added relation id:\n{(fam_id,relation)}\n{ids[(fam_id,relation)]}")
                    ids[ids[(fam_id, relation)]]
                    logger.debug(
                        f"added relation id id:\n{(fam_id,relation)}\n{ids[(fam_id,relation)]}\n{ids[ids[(fam_id,relation)]]}\n"
                    )
                elif type(adult) == str:
                    logger.warning(f"Unexpected relationship between\n{parent}\nand freeform\n{adult}\n")
                    ids[(fam_id, relation)] = (ids[parent], ids[adult])
                    logger.debug(f"added relation id:\n{(fam_id,relation)}\n{ids[(fam_id,relation)]}")
                    ids[ids[(fam_id, relation)]]
                    logger.debug(
                        f"added relation id id:\n{(fam_id,relation)}\n{ids[(fam_id,relation)]}\n{ids[ids[(fam_id,relation)]]}\n"
                    )
                else:
                    raise RuntimeError(f"Do not recognize type:\n{adult}\n")

        if section.family.unions:
            for union_no, (union_part_no, union) in enumerate(section.family.unions):
                if (
                    parents := get_parents(
                        fam_id=fam_id,
                        ids=ids,
                        union=union,
                        section=section,
                        partner_similarity=partner_similarity,
                        union_part_no=union_part_no,
                    )
                ) :
                    validate_partners_in_union(ids=ids, partners=parents)
                    if (union_no + 1 < len(section.family.unions)) and (
                        next_union := section.family.unions[union_no + 1]
                    ):
                        children = get_children(section=section, part_before=union_part_no, part_after=next_union[0])
                    else:
                        children = get_children(section=section, part_before=union_part_no, part_after=None)
                    if not children:
                        raise RuntimeError("no children found")
                    ids[(fam_id, union)] = namedtuple("union_ids", ("parents", "children"))(
                        parents=tuple((ids[adult]) for adult in parents),
                        children=tuple((ids[child]) for child in children),
                    )
                    ids[ids[(fam_id, union)]]
                    logger.debug(
                        f"added union id id:\n{(fam_id, union)}\n{ids[(fam_id, union)]}\n{ids[ids[(fam_id, union)]]}\nparents:{parents}\nchildren:{children}"
                    )
                else:
                    raise RuntimeError("no parents found")


def get_gedcom_families(ids, fam_id, section):
    def add_partners(famrecord, input_partner_ids):
        partner_ids = list(set(input_partner_ids))
        if partner_ids and (husb := partner_ids.pop()):
            famrecord.FAM.HUSB = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.HUSB(husb)
            logger.debug(f"FAM.HUSB using {husb}")
            if partner_ids and (wife := partner_ids.pop()):
                famrecord.FAM.WIFE = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.WIFE(wife)
                logger.debug(f"FAM.WIFE using {wife}")
            if partner_ids:
                unselected_partners = [key for key, value in ids.items() if value in partner_ids]
                raise RuntimeError(f"Unselected partners:{unselected_partners}")
        else:
            RuntimeError()

    logger.debug(f"{fam_id},{section}")
    if not section.family.unions:
        if section.family.relations:
            for relation_part_no, relation in section.family.relations:
                famrecord = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
                famrecord.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM(XREF_FAM(ids[ids[(fam_id, relation)]]))
                logger.debug(f"FAM\n{(fam_id, relation)}\n{ids[(fam_id, relation)]}\n{ids[ids[(fam_id, relation)]]}")
                add_partners(famrecord, ids[(fam_id, relation)])
                yield famrecord
        else:
            famrecord = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
            famrecord.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM(XREF_FAM(fam_id))
            logger.debug(f"FAM using {fam_id}")
            yield famrecord
    else:
        for union_no, union in section.family.unions:
            union_id = ids[ids[(fam_id, union)]]
            famrecord = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
            famrecord.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM(XREF_FAM(union_id))
            logger.debug(f"FAM\n{(fam_id, union)}\n{ids[(fam_id, union)]}\n{ids[ids[(fam_id, union)]]}")
            add_partners(famrecord, ids[(fam_id, union)].parents)
            for child_id in ids[(fam_id, union)].children:
                if not isinstance(famrecord.FAM.CHILs, list):
                    famrecord.FAM.CHILs: LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.CHILs = list()
                famrecord.FAM.CHILs.append(CHIL(child_id))
                logger.debug(f"FAM.CHIL using {child_id}")
            yield famrecord
            # TODO: notes, details, locations, ...


def parsed_to_gedcom(path: pathlib.Path, sections):
    fam_records = set()
    indi_records = set()
    ids = defaultdict(uuid.uuid4)
    add_reg_person_info(ids, sections)
    add_family_info(ids, sections)

    for fam_id, section in sections.items():
        for family in get_gedcom_families(ids, fam_id, section):
            fam_records.add(family)

    already_added_id = set()
    for fam_id, section in sections.items():
        logger.debug(f"{fam_id},{section}")
        for adult_part_no, adult in section.family.adults:
            if ids[adult] in already_added_id:
                logger.debug(f"GEDCOM: skipping adult that was already added:\n{adult}\n")
            else:
                logger.debug(f"GEDCOM: adding adult:\n{adult}")
                indi_records.add(get_gedcom_individual(ids, fam_id, section, adult))
                already_added_id.add(ids[adult])
        for child_part_no, child in section.family.children:
            if ids[child] in already_added_id:
                logger.debug(f"GEDCOM: skipping child that was already added:\n{child}\n")
            else:
                logger.debug(f"GEDCOM: adding child:\n{child}\n")
                indi_records.add(get_gedcom_individual(ids, fam_id, section, child))
                already_added_id.add(ids[child])

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
    try:
        parser = argparse.ArgumentParser(description="Parse html file in holger-like format.")
        parser.add_argument("--holger", type=pathlib.Path, help="path to .htm file", required=True)
        parser.add_argument("--encoding", type=pathlib.Path, help="path to .htm file", required=False)
        pargs = parser.parse_args()
        sections = split_sections(
            pargs.holger.read_text(encoding=str(pargs.encoding) if pargs.encoding else None), dict()
        )
        parsed_to_gedcom(pargs.holger, sections)
    except Exception as e:
        logger.error(e)
        raise
