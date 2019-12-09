import logging
from .configure import configure
import copy
import pathlib
import re
import uuid
from collections import OrderedDict, defaultdict
from typing import DefaultDict, List

configure()
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
            r"<B>(?P<name>[^<]+?)</B>\s+f\s+(?P<bday>[0-9-\\.xX]+?)(\s+?i\s+?(?P<bplace>[^<]+?))?\s+?(?P<families><[^\r\n]*?)?<BR>",
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
                merge[prop] = tuple(" ".join(person[prop].split()) for person in match if prop in person and person[prop])

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
