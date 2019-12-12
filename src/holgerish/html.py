import copy
import datetime
import logging
import pathlib
import re
import socket
import uuid
from collections import OrderedDict, defaultdict
from typing import DefaultDict, List

import pkg_resources

from gedcomish.common import GEDCOM_LINES, NULL
from gedcomish.gedcom555ish.lineage_linked_gedcom_file import (
    CHIL,
    CHILD_TO_FAMILY_LINK,
    EVENT_DETAIL,
    FORM_RECORDS,
    GEDCOM_FORM_HEADER_EXTENSIONs,
    GEDCOM_HEADER,
    GEDCOM_TRAILER,
    INDIVIDUAL_EVENT_DETAIL,
    INDIVIDUAL_EVENT_STRUCTUREs,
    LINEAGE_LINKED_GEDCOM_FILE,
    LINEAGE_LINKED_RECORDs,
    PERSONAL_NAME_PIECES,
    PERSONAL_NAME_STRUCTURE,
    PLACE_STRUCTURE,
    SPOUSE_TO_FAMILY_LINK,
    SUBMITTER_RECORD,
    XREF_SUBM,
)
from gedcomish.gedcom555ish.primitives import XREF_FAM, XREF_INDI

logger = logging.getLogger(__name__)


def parse_individual(text):
    pattern = re.compile(
        r"<B>(?P<name>[^<]+?)</B>"
        + r".*?född.*?"
        + r"(?P<bday>[0-9-\.xX]+)"
        + r"((<BR>|\s)+?i\s+?"
        + r"(?P<bplace>[^)]+\))"
        + r")?"
        + r".*?(död.*?"
        + r"(?P<dday>[0-9-\.xX]+)"
        + r".*?"
        + r"((<BR>|\s)+?i\s+?"
        + r"(?P<dplace>[^)]+\))"
        + r")?|<P>)"
    )
    yield from (m.groupdict() for m in pattern.finditer(text))


def normalize_date(s):
    s = list(s.ljust(10, "0")[0:10])
    s = [c if c.isdigit() else "0" for c in s]
    s[4] = "-"
    s[7] = "-"
    return "".join(s)


def normalize_name(s):
    return set(s.replace(",", " ").split())


_PERSON_IN_FAMILY = "person_in_family"
_PARENT_IN_FAMILY = "parent_in_family"
_CHILD_IN_FAMILY = "child_in_family"
_NAME = "name"
_FIRST_NAMES = "first_names"
_LAST_NAMES = "last_names"
_BIRTHDAY = "bday"
_DEATHDAY = "dday"
_BIRTHPLACE = "bplace"
_LIVINGPLACE = "lplace"
_DEATHPLACE = "dplace"
_SEX = "sex"
_SEX_MALE = "M"
_SEX_FEMALE = "F"
_SEX_UNDETERMINED = "U"
_SOURCE_TEXT_FAMILY = "source_text_family"

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
    (?P<RELATIONTYPE>Gift|Sambo|Relation|Förlovad|Trolovad|Partner|Särbo)
    (
        \s*?
        (?P<DATEMODIFIER>.+?)?
        \s+?
        (?P<RELATIONDAY>[0-9-.xX]+)
        (
            \s+?i\s+?
            (?P<RELATIONPLACE>.+?)
        )?
        \s+
        |(?P<RELATIONDETAIL>.+?)
        \s+
    )?
    med
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
                    från\s+?familj
                    \s*
                    <A\sHREF=\#(?P<FROM_HREF>[0-9]+)>
                    (?P<FROM_REF>[0-9]+)
                    <\/A>
                \)
            )?
            (
                ,
                \s*?
                född
                \s+?
                (?P<BIRTHDAY>[0-9-.xX]+)
                (
                    \s+?i\s+?
                    (?P<BIRTHPLACE>.+?)
                )?
            )?
            (
                ,
                \s*?
                död
                \s+?
                (?P<DEATHDAY>[0-9-.xX]+)
                (
                    \s+?i\s+?
                    (?P<DEATHPLACE>.+?)
                )?
            )?
            (
                ,
                \s*?
                se\s+?familj
                \s+?
                <A\sHREF=\#(?P<SEE_HREF>[0-9]+)>
                (?P<SEE_REF>[0-9]+)
                <\/A>
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

FAMILY_CHILDREN_SECTION_HEADER = re.compile(
    r"""
        Barn:
        |Barn\s+i(?P<MARRIAGE_NO>.+?)giftet:
        |Barn\s+utan\s+känd\s+(?P<PARTNER_SEX>moder|fader):
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


def refine_detail_sections(sections: list):
    """
        returns a defaultdict(list),
        which maps family id to a list of details
    """
    result = defaultdict(list)
    for text, refs in section_parts(sections, SAKREGISTER):
        for ref in refs:
            result[ref].append(text)
    return result


def refine_location_sections(sections: list):
    """
        returns a defaultdict(list),
        which maps family id to a list of tuples, each tuple element signifying a part of an address,
        NOTE:
        location parts may have whitespace or comma signs between them in the family sections.
    """
    result = defaultdict(list)
    for text, refs in section_parts(sections, ORTREGISTER):
        for ref in refs:
            result[ref].append(tuple(text.split()))
    return result


def refine_person_sections(sections: list):
    """
        returns a defaultdict(list),
        which maps family id to a dict, with keys "name", "firstnames" and "surnames"
    """
    result = defaultdict(list)
    for text, refs in section_parts(sections, PERSONREGISTER):
        for ref in refs:
            if (m := PERSONREGISTRY_PERSON_REGEX.search(text)) :
                if m["SECONDNAMES"]:
                    result[ref].append(
                        dict(
                            firstnames=m["SECONDNAMES"].split() if m["SECONDNAMES"] else None,
                            surnames=m["FIRSTNAMES"].split() if m["FIRSTNAMES"] else None,
                            birthday=m["BIRTHDAY"],
                            birthplace=m["BIRTHPLACE"].split() if m["BIRTHPLACE"] else None,
                        )
                    )
                else:
                    result[ref].append(
                        dict(
                            firstnames=m["FIRSTNAMES"].split() if m["FIRSTNAMES"] else None,
                            surnames=None,
                            birthday=m["BIRTHDAY"],
                            birthplace=m["BIRTHPLACE"].split() if m["BIRTHPLACE"] else None,
                        )
                    )
    return result


def split_sections(text, registry):
    sections = re.split("<HR WIDTH=500>", text)
    family_sections = dict()
    person_sections = list()
    detail_sections = list()
    person_sections = list()
    location_sections = list()
    unknown_sections = list()
    for section in sections:
        if SAKREGISTER in section:
            detail_sections.append(section)
        elif ORTREGISTER in section:
            location_sections.append(section)
        elif PERSONREGISTER in section:
            person_sections.append(section)
        elif (m := FAMILY_REGEX.search(section)) :
            if m["ID"] in family_sections:
                raise ValueError("Family already present!")
            family_sections[m["ID"]] = section
        else:
            unknown_sections.append(section)
    del sections, section, m
    details = refine_detail_sections(detail_sections)
    del detail_sections
    locations = refine_location_sections(location_sections)
    del location_sections
    persons = refine_person_sections(person_sections)

    for family_id, family in family_sections.items():
        parts = family.split("<P>")
        assert FAMILY_REGEX.search(parts[0])
        for part in parts[1:]:
            subparts = part.split("<BR>")
            nonmatches = list()
            for subpart in (subpart for subpart in (" ".join(subpart.split()) for subpart in subparts) if subpart):
                if (m := FAMILY_RELATION_REGEX.search(subpart)) :
                    value = m.groupdict()
                    pass
                elif (m := FAMILY_PERSON_REGEX.search(subpart)) :
                    value = m.groupdict()
                    pass
                elif (m := FAMILY_CHILDREN_SECTION_HEADER.search(subpart)) :
                    value = m.groupdict()
                    pass
                else:
                    value = subpart
                    nonmatches.append(value)
                    pass
            unmatched = " ".join(nonmatches)
            nonmatches = list()
            if (m := FAMILY_RELATION_REGEX.search(unmatched)) :
                value = m.groupdict()
                pass
            elif (m := FAMILY_PERSON_REGEX.search(unmatched)) :
                value = m.groupdict()
                pass
            elif (m := FAMILY_CHILDREN_SECTION_HEADER.search(unmatched)) :
                value = m.groupdict()
                pass
            else:
                value = unmatched
                nonmatches.append(unmatched)
                pass

            pass


class PersonRegistry:
    """
    Searches for persons in the person registry.

    fields:
        _NAME
        _BIRTHDAY
        _BIRTHPLACE
        _PERSON_IN_FAMILY
    """

    def __init__(self, file: pathlib.Path):
        self.file = file
        self.persons = PersonRegistry._parse_personregister(file)

    def get_persons(self):
        return OrderedDict(sorted(copy.deepcopy(self.persons).items(), key=lambda p: p[1][0][_BIRTHDAY]))

    @staticmethod
    def _gen_family_ids_from_registered_person(person):
        pattern = re.compile(
            r"(?P<family><A HREF=#(?P<fam_href>[0-9]+?)>(?P<fam_ref>[0-9]+?)</A>,?\s*?)", flags=re.DOTALL,
        )

        yield from (m.groupdict() for m in pattern.finditer(person["families"]))

    @staticmethod
    def _gen_registered_person(personregister):
        pattern = re.compile(
            r"<B>(?P<name>[^<]+?)</B>\s+f\s+(?P<bday>[0-9-\\.xX]+?)(\s+?i\s+?(?P<bplace>.*?))?\s+?(?P<families><[^\r\n]*?)?<BR>",
            flags=re.DOTALL,
        )
        yield from (m.groupdict() for m in pattern.finditer(personregister["Personregister"]))

    @staticmethod
    def _gen_personregistry(text):
        pattern = re.compile(
            r"<CENTER><FONT SIZE=5>Personregister</FONT></CENTER>(?P<Personregister>.*)<CENTER><FONT SIZE=5>Ortregister</FONT></CENTER>",
            flags=re.DOTALL,
        )
        yield from (m.groupdict() for m in pattern.finditer(text))

    @staticmethod
    def _parse_personregister(file: pathlib.Path):
        text = file.read_text(encoding="utf-8")

        persons: DefaultDict[uuid.UUID, List] = defaultdict(list)
        for personregister in PersonRegistry._gen_personregistry(text):
            for person in PersonRegistry._gen_registered_person(personregister):
                person_id = uuid.uuid1()
                person[_PERSON_IN_FAMILY] = list()
                for family in PersonRegistry._gen_family_ids_from_registered_person(person):
                    assert family["fam_href"] == family["fam_ref"]
                    person[_PERSON_IN_FAMILY].append(family["fam_ref"])
                person[_PERSON_IN_FAMILY] = tuple(person[_PERSON_IN_FAMILY])
                persons[person_id].append(person)
        return persons


class FamilyRegistry:
    """
    Searches for persons in the family sections.

    fields:
        _NAME
        _BIRTHDAY
        _BIRTHPLACE
        _DEATHDAY
        _DEATHPLACE
        _LIVINGPLACE
        _PARENT_IN_FAMILY
        _CHILD_IN_FAMILY
    """

    def __init__(self, file: pathlib.Path):
        self.file = file
        self.persons, self.family_to_source = FamilyRegistry._parse_family_registry(file)

    def get_persons(self):
        return sorted(
            copy.deepcopy(self.persons),
            key=lambda p: (p[_BIRTHDAY] is None, normalize_date(p[_BIRTHDAY]) if p[_BIRTHDAY] else p[_BIRTHDAY],),
        )

    def get_family_to_source(self):
        return copy.deepcopy(self.family_to_source)

    @staticmethod
    def _gen_family_person_info(family_person):
        # split on
        # Familj [0-9]+
        # children:
        # *  se familj
        #
        text = family_person["person"]
        text = text.replace("<BR>", "")
        text = text.replace("<P>", "")
        text = text.replace("\r", "")
        text = text.replace("\n", "")
        pattern = re.compile(
            r"<B>(?P<name>.*?)</B>"
            r"(.*?född\s*(?P<bday>[0-9-\.xX]+)(\s*i\s*(?P<bplace>[^)]+?\)))?)?"
            r"(.*?död\s*(?P<dday>[0-9-\.xX]+)(\s*i\s*(?P<dplace>[^)]+?\)))?)?"
            r"(.*?Bosatt\s*i\s*(?P<lplace>[^)]+?\)))?"
            # r"(.*?Gift\s*(?P<mday>[0-9-\.xX]+)(\s*i\s*(?P<mplace>[^)]+?\)))?)?"
        )
        yield from (m.groupdict() for m in pattern.finditer(text))

    @staticmethod
    def _gen_family_person(family):
        pattern = re.compile(r"(?P<person>.*?)(<B>|$)", flags=re.DOTALL,)
        text = family["family"]

        for child_idx, child in enumerate(text.split("*")):
            for _, person in enumerate(child.split("<B>")):
                yield from (
                    dict(
                        {key: "<B>" + val for key, val in match.groupdict().items()},
                        **{_PARENT_IN_FAMILY: (family["fam_ref"],)},
                    )
                    if child_idx == 0
                    else dict(
                        {key: "<B>" + val for key, val in match.groupdict().items()},
                        **{_CHILD_IN_FAMILY: (family["fam_ref"],)},
                    )
                    for match in pattern.finditer(person)
                )

    @staticmethod
    def _gen_family(family_section):
        pattern = re.compile(r"(?P<fam_ref>[0-9]+)>(?P<family>.*?)(<A NAME=|$)", flags=re.DOTALL,)
        yield from (m.groupdict() for m in pattern.finditer(family_section["family_section"]))

    @staticmethod
    def _gen_family_section(text):
        pattern = re.compile(
            r"(?P<family_section><A NAME=[0-9]>.*?)<CENTER><FONT SIZE=5>Personregister</FONT></CENTER>",
            flags=re.DOTALL,
        )
        yield from (m.groupdict() for m in pattern.finditer(text))

    @staticmethod
    def _parse_family_registry(file: pathlib.Path):
        text = file.read_text(encoding="utf-8")
        family_persons = list()
        family_to_source = dict()
        for family_section in FamilyRegistry._gen_family_section(text):
            for family in FamilyRegistry._gen_family(family_section):
                family_to_source[family["fam_ref"]] = family["family"]
                for person in FamilyRegistry._gen_family_person(family):
                    for info in FamilyRegistry._gen_family_person_info(person):
                        family_persons.append(
                            dict(
                                info,
                                **{
                                    _PARENT_IN_FAMILY: person[_PARENT_IN_FAMILY]
                                    if _PARENT_IN_FAMILY in person
                                    else tuple(),
                                    _CHILD_IN_FAMILY: person[_CHILD_IN_FAMILY]
                                    if _CHILD_IN_FAMILY in person
                                    else tuple(),
                                },
                            )
                        )

        return family_persons, family_to_source


def match(personRegistry: PersonRegistry, familyRegistry: FamilyRegistry):
    registered_persons = personRegistry.get_persons()
    persons = familyRegistry.get_persons()
    family_to_source = familyRegistry.get_family_to_source()
    logger.info(f"matching {len(persons)} persons  to the {len(registered_persons)} persons in registry.")
    for person_id, person_query in registered_persons.items():
        normalized_bday_query = normalize_date(person_query[0][_BIRTHDAY])
        normalized_name_query = normalize_name(person_query[0][_NAME])
        family_ids_query = set(person_query[0][_PERSON_IN_FAMILY])

        keep_looping = True
        while keep_looping:
            keep_looping = False
            for full_person in persons:
                normalized_date_person = (
                    normalize_date(full_person[_BIRTHDAY]) if full_person[_BIRTHDAY] else full_person[_BIRTHDAY]
                )
                normalized_name_person = normalize_name(full_person[_NAME])

                # Check age
                if (full_person[_BIRTHDAY] is None, normalized_date_person) > (False, normalized_bday_query,):
                    break

                # Check family connections
                if not any(
                    [
                        set(full_person[_PARENT_IN_FAMILY]) & family_ids_query,
                        set(full_person[_CHILD_IN_FAMILY]) & family_ids_query,
                    ]
                ):
                    continue

                # Check name and age
                if all(
                    [normalized_date_person == normalized_bday_query, normalized_name_person == normalized_name_query]
                ):
                    registered_persons[person_id].append(full_person)
                    persons.remove(full_person)
                    keep_looping = True
                    break
    logger.warning(f"#unmatched persons: {len(persons)}")
    logger.info(f"adding person info to families.")
    families: DefaultDict[str, DefaultDict[str, List]] = defaultdict(lambda: defaultdict(list))
    for person_id, infos in registered_persons.items():
        for info in infos:
            for family_kind in (_PERSON_IN_FAMILY, _PARENT_IN_FAMILY, _CHILD_IN_FAMILY):
                if family_kind in info:
                    for family_id in info[family_kind]:
                        families[family_id][family_kind].append(person_id)
    for family_id, source_text in family_to_source.items():
        families[family_id][_SOURCE_TEXT_FAMILY] = source_text
    return registered_persons, persons, families


def merge(matches):
    merges = dict()
    for match_id, match in matches.items():
        merge = dict()
        try:
            merge[_NAME] = (match[0][_NAME],)
        except Exception as e:
            logger.error(f"{e}")
        try:
            last_names, first_names = match[0][_NAME].split(",")
            first_names = first_names.split()
            last_names = last_names.split()
            merge[_FIRST_NAMES] = tuple(first_names)
            merge[_LAST_NAMES] = tuple(last_names)
        except Exception as e:
            logger.error(f"{e}")

        try:
            merge[_BIRTHDAY] = (match[0][_BIRTHDAY],)
        except Exception as e:
            logger.error(f"{e}")
        try:
            merge[_PERSON_IN_FAMILY] = match[0][_PERSON_IN_FAMILY]
        except Exception as e:
            logger.error(f"{e}")
        try:
            merge[_PARENT_IN_FAMILY] = tuple(
                family_id
                for person in match
                if _PARENT_IN_FAMILY in person
                for family_id in person[_PARENT_IN_FAMILY]
                if person[_PARENT_IN_FAMILY]
            )
        except Exception as e:
            logger.error(f"{e}")
        try:
            merge[_CHILD_IN_FAMILY] = tuple(
                family_id
                for person in match
                if _CHILD_IN_FAMILY in person
                for family_id in person[_CHILD_IN_FAMILY]
                if person[_CHILD_IN_FAMILY]
            )
        except Exception as e:
            logger.error(f"{e}")
        try:
            merge[_DEATHDAY] = tuple(person[_DEATHDAY] for person in match if _DEATHDAY in person and person[_DEATHDAY])
            for prop in (
                _BIRTHPLACE,
                _DEATHPLACE,
                _LIVINGPLACE,
            ):
                merge[prop] = tuple(
                    " ".join(person[prop].split()) for person in match if prop in person and person[prop]
                )

            for prop in (_BIRTHPLACE, _DEATHPLACE, _LIVINGPLACE):
                if merge[prop] and len(merge[prop]) > 1:
                    for prop_place in merge[prop]:
                        if all(pplace in prop_place for pplace in merge[prop]):
                            merge[prop] = (prop_place,)
                            break
        except Exception as e:
            logger.error(f"{e}")
        merges[match_id] = {k: v for k, v in merge.items() if v}
    return merges


def parse_html(file: pathlib.Path):
    personRegistry = PersonRegistry(file)
    familyRegistry = FamilyRegistry(file)
    matched, unmatched, families = match(personRegistry, familyRegistry)
    logger.warning(f"unmatched persons: {unmatched}")
    return merge(matched), unmatched, families


def parsed_to_gedcom(path: pathlib.Path, parsed):
    merges, unmatched, families = parsed
    fam_records = set()
    indi_records = set()
    for fam_id in families.keys():

        famrecord = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
        famrecord.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM(XREF_FAM(fam_id))

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

