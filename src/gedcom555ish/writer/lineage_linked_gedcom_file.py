import re
import datetime
import uuid
from typing import Tuple, List, Union, Optional, Callable
from enum import Enum
import warnings
import inspect
import os


class Meta(type):
    @classmethod
    def __prepare__(metaclass, name, bases, **kwds):
        """
            __prepare__
            :param metaclass:   classdef keyword argument 'metaclass'
            :param name:        classdef name
            :param bases:       classdef positional arguments
            :param **kwds:      classdef keyword arguments (sans 'metaclass')
                                NOTE: same as in classdef, passed by value
            :return:            namespace
        """
        return super().__prepare__(metaclass, name, bases, **kwds)

    @staticmethod
    def __new__(metaclass, name, bases, namespace, **kwds):
        """
            __new__
            :param metaclass:   classdef keyword argument 'metaclass'
            :param name:        classdef name
            :param bases:       classdef positional arguments
            :param namespace:   namespace
                                NOTE:
                                if '__classcell__' is present, it must be included in the call to super().
            :param **kwds:      classdef keyword arguments (sans 'metaclass')
                                NOTE: same as in classdef, passed by value
            :return:            <class 'name'>
        """
        return super().__new__(metaclass, name, bases, namespace)

    def __init__(classname, name, bases, namespace, **kwds):
        """
            __init__
            :param classname:       <class 'name'>
            :param name:            classdef name
            :param bases:           classdef positional arguments
            :param namespace:       namespace
            :param **kwds:          classdef keyword arguments (sans 'metaclass')
                                    NOTE: same as in classdef, passed by value
            :return:                None
            NOTE:
            must call: super().__init__([args...]).
        """
        for key, value in kwds.items():
            if not hasattr(classname, key):
                setattr(classname, key, value)
            else:
                warnings.warn(f"Could not enter {key}:{value} into class dictionary", Warning)
        super().__init__(name, bases, namespace, **kwds)

    def __call__(classname, *args, **kwargs):
        """
            __call__
            :param classname:   <class 'name'>
            :param *args:       class call positional arguments (instantiation of <class 'name'>)
            :param **kwargs:    class call keyword arguments (instantiation of <class 'name'>)
            :return:            <name object at 0x...>
            NOTE:
            <class 'name'>(*ARGS, **KWARGS)
                __call__(<class 'name'>, *args, **kwargs)
                    <class 'name'>:         __init__(<name object at 0x...>, *args, **kwargs) -> None
                    <class 'name'> bases:   __init__(<name object at 0x...>, [args...]) -> None
            -> <name object at 0x...>
        """
        return super().__call__(*args, **kwargs)


class XREF_ID:
    def __init__(self, identifier=None):
        if isinstance(identifier, uuid.UUID):
            self.id = str(identifier).replace("-", "")[0:20]
        elif identifier is not None:
            self.id = str(identifier)[0:20]
        else:
            self.id = str(uuid.uuid1()).replace("-", "")[0:20]

    def __str__(self):
        return f"@{self.id}@"


class GEDCOM_SYNTAX:
    digit = f"[\u0030-\u0039]"
    alpha = f"[\u0041-\u005A|\u0061-\u007A]"
    alphanum = f"[{alpha}|{digit}]"
    non_zero_digit = f"[\u0031-\u0039]"
    level = f"[{digit}|{non_zero_digit}{digit}]"
    tag = f"[\u005F|{alphanum}]+"
    identifier_string = f"{alphanum}+"
    at = "\u0040"
    xref_ID = f"{at}{identifier_string}{at}"
    pointer = f"{xref_ID}"
    escape_text = f"[{alphanum}|\u0020]+"
    escape = f"\u0040\u0023{escape_text}\u0040"
    delim = f"\u0020"
    line_char = f"[^\u0000-\u0008\u000A-\u001F\u00FF]"
    line_text = f"{line_char}+"
    line_item = f"[{escape}|{line_text}|{escape}{delim}{line_text}]"
    line_value = f"[{pointer}|{line_item}]"
    carriage_return = "\u000D"
    line_feed = "\u000A"
    terminator = f"[{carriage_return}|{line_feed}|{carriage_return}{line_feed}]"
    null = f""


class GEDCOM_LINE:
    def __init__(
        self, *, level: int, tag: str, xref_id: XREF_ID = None, line_value: str = None,
    ):
        self.level = level
        self.xref_id = xref_id
        self.tag = tag
        self.line_value = line_value

    def __str__(self):
        return (
            " ".join([str(val) for val in [self.level, self.xref_id, self.tag, self.line_value] if val is not None])
            + "\n"
        )


class Primitive:
    def __init__(self, *args, **kwargs):
        self.value = str()
        for arg in args:
            self.value += str(arg)
        for kwarg in kwargs:
            self.value += str(kwarg)

    def __str__(self):
        print(f"<Primitive:{self.value}")
        return self.value


class ADDRESS_CITY(Primitive, metaclass=Meta, Size=(1, 60)):
    pass


class ADDRESS_COUNTRY(Primitive, metaclass=Meta, Size=(1, 60)):
    pass


class ADDRESS_EMAIL(Primitive, metaclass=Meta, Size=(5, 120)):
    pass


class ADDRESS_FAX(Primitive, metaclass=Meta, Size=(5, 60)):
    pass


class ADDRESS_LINE1(Primitive, metaclass=Meta, Size=(1, 60)):
    pass


class ADDRESS_LINE2(Primitive, metaclass=Meta, Size=(1, 60)):
    pass


class ADDRESS_LINE3(Primitive, metaclass=Meta, Size=(1, 60)):
    pass


class ADDRESS_POSTAL_CODE(Primitive, metaclass=Meta, Size=(1, 10)):
    pass


class ADDRESS_STATE(Primitive, metaclass=Meta, Size=(1, 60)):
    pass


class ADDRESS_WEB_PAGE(Primitive, metaclass=Meta, Size=(4, 2047)):
    pass


class ADOPTED_BY_WHICH_PARENT(Primitive, metaclass=Meta, Size=(4, 4)):
    pass


class AGE_AT_EVENT(Primitive, metaclass=Meta, Size=(2, 13)):
    pass


class ATTRIBUTE_DESCRIPTOR(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class ATTRIBUTE_TYPE(
    Primitive, metaclass=Meta, Size=(None, None),
):
    pass


class AUTOMATED_RECORD_ID(Primitive, metaclass=Meta, Size=(1, 12)):
    pass


class BEFORE_COMMON_ERA(Primitive, metaclass=Meta, Size=(2, 4)):
    pass


class CASTE_NAME(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class CAUSE_OF_EVENT(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class CERTAINTY_ASSESSMENT(Primitive, metaclass=Meta, Size=(1, 1)):
    pass


class CHARACTER_ENCODING(Primitive, metaclass=Meta, Size=(5, 7)):
    pass


class COPYRIGHT_GEDCOM_FILE(Primitive, metaclass=Meta, Size=(1, 248)):
    pass


class COPYRIGHT_SOURCE_DATA(Primitive, metaclass=Meta, Size=(1, 248)):
    pass


class COUNT_OF_CHILDREN(Primitive, metaclass=Meta, Size=(1, 3)):
    pass


class DATE_EXACT(
    Primitive, metaclass=Meta, Size=(10, 11),
):
    pass


class DATE_PERIOD(Primitive, metaclass=Meta, Size=(7, 35)):
    pass


def get_month(date: datetime.datetime):
    return [None, "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][date.month]


def try_strptime(date_phrase: str):
    date_phrase = date_phrase.strip().rstrip(".xX-")
    for fmt in [r"%Y-%m-%d", r"%Y-%m", r"%Y"]:
        try:
            return datetime.datetime.strptime(date_phrase, fmt)
        except Exception as _:
            pass
    return None


def get_gedcom_date(date_phrase: str):
    interpreted_date = try_strptime(date_phrase)
    if interpreted_date:
        return " ".join(
            [
                "INT",
                str(interpreted_date.day),
                get_month(interpreted_date),
                str(interpreted_date.year),
                "".join(["(", date_phrase, ")"]),
            ]
        )
    else:
        return "".join(["(", date_phrase, ")"])


class DATE_VALUE(Primitive, metaclass=Meta, Size=(1, 35)):
    def __init__(self, date: str):
        self.date = get_gedcom_date(date)

    def __str__(self):
        return self.date


class DESCRIPTIVE_TITLE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class ENTRY_RECORDING_DATE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class EVENT_DESCRIPTOR(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class EVENT_OR_FACT_CLASSIFICATION(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class EVENT_TYPE_CITED_FROM(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class EVENTS_RECORDED(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class FILE_CREATION_DATE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class GEDCOM_CONTENT_DESCRIPTION(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class GEDCOM_FILE_NAME(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class GEDCOM_FORM(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class GEDCOM_VERSION_NUMBER(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class ID_NUMBER(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class LANGUAGE_OF_TEXT(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class MULTIMEDIA_FILE_REFERENCE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class MULTIMEDIA_FORMAT(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_OF_BUSINESS(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_OF_PRODUCT(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_OF_REPOSITORY(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_OF_SOURCE_DATA(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_PERSONAL(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_PHONETIC(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_PIECE_GIVEN(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_PIECE_NICKNAME(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_PIECE_PREFIX(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_PIECE_SUFFIX(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_PIECE_SURNAME_PREFIX(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_PIECE_SURNAME(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_ROMANISED(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NAME_TYPE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NATIONAL_OR_TRIBAL_ORIGIN(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NOBILITY_TYPE_TITLE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NULL(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class NUMBER_OF_RELATONSHIPS(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class OCCUPATION(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PEDIGREE_LINKAGE_TYPE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PHONE_NUMBER(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PHONETISATION_METHOD(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PHYSICAL_DESCRIPTION(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PLACE_LATITUDE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PLACE_LONGITUDE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PLACE_NAME(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PLACE_PHONETIC(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PLACE_ROMANISED(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class POSSESSIONS(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PRODUCT_VERSION_NUMBER(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class PUBLICATION_DATE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class RECEIVING_SYSTEM_NAME(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class RELATION_IS_DESCRIPTOR(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class RELIGIOUS_AFFILIATION(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class RESPONSIBLE_AGENCY(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class ROLE_IN_EVENT(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class ROMANISATION_METHOD(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SEX_VALUE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SCHOLASTIC_ACHIEVEMENT(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SOURCE_CALL_NUMBER(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SOURCE_DESCRIPTIVE_TITLE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SOURCE_FILED_BY_ENTRY(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SOURCE_JURISDICTION_PLACE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SOURCE_MEDIA_TYPE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SOURCE_ORIGINATOR(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SOURCE_PUBLICATION_FACTS(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SUBMITTER_NAME(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class SYSTEM_ID(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class TEXT_FROM_SOURCE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class TIME_VALUE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class USER_REFERENCE_NUMBER(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class USER_REFERENCE_TYPE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class USER_TEXT(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class WHERE_WITHIN_SOURCE(Primitive, metaclass=Meta, Size=(None, None)):
    pass


class XREF_FAM(XREF_ID, metaclass=Meta, Size=(3, 22)):
    pass


class XREF_INDI(XREF_ID, metaclass=Meta, Size=(3, 22)):
    pass


class XREF_NOTE(XREF_ID, metaclass=Meta, Size=(3, 22)):
    pass


class XREF_OBJE(XREF_ID, metaclass=Meta, Size=(3, 22)):
    pass


class XREF_REPO(XREF_ID, metaclass=Meta, Size=(3, 22)):
    pass


class XREF_SOUR(XREF_ID, metaclass=Meta, Size=(3, 22)):
    pass


class XREF_SUBM(XREF_ID, metaclass=Meta, Size=(3, 22)):
    pass


class GEDCOM_LINES:
    def __init__(self):
        self.lines: List[Union[Callable[[int], GEDCOM_LINE], "GEDCOM_LINES"]] = list()

    def add_text(self, *, level_delta: int, tag: str, primitive: Primitive, xref_id: XREF_ID = None):
        try:

            def unicode_chunksplit(slicable, safe_chunksize: int):
                from_char = 0
                while from_char < len(slicable):
                    for to_char in range(from_char + safe_chunksize, from_char, -1):
                        if len(slicable[from_char:to_char].encode("utf-8")) <= safe_chunksize:
                            yield slicable[from_char:to_char]
                            from_char = to_char
                            break

            safe_chunksize = 255
            safe_chunksize -= len("99")
            if xref_id:
                safe_chunksize -= len(" ") + len(str(xref_id).encode("UTF-8"))
            if tag:
                safe_chunksize -= len(" ") + len(tag.encode("UTF-8"))
            safe_chunksize -= len(os.linesep)
            safe_chunksize -= len(" ")
            value = str(primitive)
            if isinstance(primitive, XREF_ID):
                pass
            else:
                value.replace("@", "@@")
            lines = value.split(os.linesep)
            if isinstance(primitive, Enum):
                primitive = primitive.value
            for line_no, line in enumerate(lines):
                for text_chunk_no, unicode_text_chunk in enumerate(unicode_chunksplit(line, safe_chunksize)):
                    if text_chunk_no == 0:
                        if line_no == 0:

                            def apply_text(
                                n, level_delta=level_delta, tag=tag, xref_id=xref_id, line_value=unicode_text_chunk
                            ):
                                return GEDCOM_LINE(
                                    level=n + level_delta, tag=tag, xref_id=xref_id, line_value=line_value
                                )

                            self.lines.append(apply_text)
                            continue
                        else:

                            def apply_cont(n, level_delta=level_delta, xref_id=xref_id, line_value=unicode_text_chunk):
                                return GEDCOM_LINE(
                                    level=n + level_delta + 1, tag="CONT", xref_id=xref_id, line_value=line_value
                                )

                            self.lines.append(apply_cont)
                    else:

                        def apply_conc(n, level_delta=level_delta, xref_id=xref_id, line_value=unicode_text_chunk):
                            return GEDCOM_LINE(
                                level=n + level_delta + 1, tag="CONC", xref_id=xref_id, line_value=line_value
                            )

                        if hasattr(primitive, "meta"):
                            if max(getattr(getattr(primitive, "meta"), "Size")) <= 248:
                                raise ValueError(
                                    f"'never uses CONC records for line values with a maximum length of 248 or less': {line}"
                                )
                            else:
                                self.lines.append(apply_conc)
        except Exception as ex:
            raise ex

    def add_primitives(self, level_delta: int, tag: str, *primitives: Optional[Primitive], xref_id: XREF_ID = None):
        if primitives:
            for primitive in primitives:
                if primitive:
                    self.add_text(level_delta=level_delta, tag=tag, primitive=primitive, xref_id=xref_id)
        else:

            def apply(n, level_delta=level_delta, tag=tag, xref_id=xref_id):
                return GEDCOM_LINE(level=n + level_delta, tag=tag, xref_id=xref_id, line_value=None)

            self.lines.append(apply)

    def add_substructures(self, level_delta: int, *substructs: Optional["Substructure"]):
        if substructs:
            for substruct in substructs:
                if substruct:

                    def apply(n, level_delta=level_delta, substruct=substruct):
                        return substruct(n + level_delta)

                    self.lines.append(apply)

    def __call__(self, level=int):
        return "".join([str(line(level)) for line in self.lines])


class Tag:
    pass


class Pointer:
    pass


class Substructure(object):
    @classmethod
    def nested_classes(cls, *queries):
        inners = []
        for attrname in dir(cls):
            attr = getattr(cls, attrname)
            if isinstance(attr, type) and any(issubclass(attr, innercls) for innercls in queries):
                inners.append(attr)
        return inners

    def instances_of_nested_classes(self, *queries):
        inners = []
        for attrname in dir(self):
            attr = getattr(self, attrname)
            if not isinstance(attr, type) and any(isinstance(attr, innercls) for innercls in queries):
                inners.append(attr)
        return inners

    @staticmethod
    def find_stuff(nested, base, level=0):
        if isinstance(nested, Primitive):
            if isinstance(nested, base):
                yield nested
            else:
                raise ValueError(f"do not understand what to do with this one! nested={nested} base={base}")
        else:
            yield from (
                attribute
                for attribute in (getattr(nested, attr) for attr in dir(nested))
                if isinstance(attribute, base)
            )

    def __call__(self, lines: GEDCOM_LINES):
        if isinstance(self, Tag):
            lines.add_primitives(self.__class__.__qualname__.count(".") - 1, self.__class__.__name__)
        elif isinstance(self, XREF_ID):
            lines.add_primitives(self.__class__.__qualname__.count(".") - 1, self.__class__.__name__, xref_id=self)
        clssource = inspect.getsource(self.__class__)
        nesteds = list(self.instances_of_nested_classes(XREF_ID, Primitive, Substructure))
        nesteds = sorted(
            nesteds,
            key=lambda p: result.start()
            if (
                result := re.search(
                    fr"class\s+{p.__class__.__name__}|{p.__class__.__name__}\s*=\s*{p.__class__.__name__}", clssource
                )
            )
            else float("inf"),
        )
        print(f"self={self}")
        for nested in nesteds:
            level = nested.__class__.__qualname__.count(".") - 1
            tag = nested.__class__.__name__
            bases = [base for base in nested.__class__.__bases__ if base not in (XREF_ID, Primitive, Substructure)]
            xrefs: List[XREF_ID] = list()
            primitives: List[Primitive] = list()
            substructures: List[Substructure] = list()
            for base in bases:
                if isinstance(nested, Pointer) and issubclass(base, XREF_ID):
                    xrefs.extend(Substructure.find_stuff(nested, base))
                if issubclass(base, Primitive):
                    primitives.extend(Substructure.find_stuff(nested, base))
                if issubclass(base, Substructure):
                    substructures.extend(Substructure.find_stuff(nested, base))
            if primitives:
                print(f"<primitives:{primitives}>")
                lines.add_primitives(level, tag, *primitives, xref_id=xrefs[0] if xrefs else None)
            if substructures:
                print(f"<substructures:{substructures}>")
                lines.add_substructures(level, *substructures)
            try:
                print(f"<try:{nested}>")
                nested(lines)
            except Exception as _:
                try:
                    print(f"<except:{nested}>")
                    lines.add_primitives(level, tag, xref_id=xrefs[0] if xrefs else None)
                except Exception as _:
                    print(f"<unused?:{nested}>")
                    pass
        return lines


class MULTIMEDIA_LINK(Substructure):
    class OBJE(XREF_OBJE, Substructure):
        pass


class NOTE_STRUCTURE(Substructure):
    class NOTE(XREF_NOTE, USER_TEXT, Substructure):
        pass


class CHANGE_DATE(Substructure):
    class CHAN(Tag, Substructure):
        class DATE(DATE_EXACT, Substructure):
            class TIME(TIME_VALUE, Substructure):
                pass

        NOTE_STRUCTURE = NOTE_STRUCTURE


class SOURCE_CITATION(Substructure):
    class SOUR(XREF_SOUR, Substructure):
        class PAGE(WHERE_WITHIN_SOURCE, Substructure):
            pass

        class EVEN(EVENT_TYPE_CITED_FROM, Substructure):
            class ROLE(ROLE_IN_EVENT, Substructure):
                pass

        class DATA(Tag, Substructure):
            class DATE(ENTRY_RECORDING_DATE, Substructure):
                pass

            class TEXT(TEXT_FROM_SOURCE, Substructure):
                pass

        MULTIMEDIA_LINK = MULTIMEDIA_LINK
        NOTE_STRUCTURE = NOTE_STRUCTURE

        class QUAY(CERTAINTY_ASSESSMENT, Substructure):
            pass


class ADDRESS_STRUCTURE(Substructure):
    class ADDR(Tag, Substructure):
        class ADR1(ADDRESS_LINE1, Substructure):
            pass

        class ADR2(ADDRESS_LINE2, Substructure):
            pass

        class ADR3(ADDRESS_LINE3, Substructure):
            pass

        class CITY(ADDRESS_CITY, Substructure):
            pass

        class STAE(ADDRESS_STATE, Substructure):
            pass

        class POST(ADDRESS_POSTAL_CODE, Substructure):
            pass

        class CTRY(ADDRESS_COUNTRY, Substructure):
            pass

    class PHON(PHONE_NUMBER, Substructure):
        pass

    class EMAIL(ADDRESS_EMAIL, Substructure):
        pass

    class FAX(ADDRESS_FAX, Substructure):
        pass

    class WWW(ADDRESS_WEB_PAGE, Substructure):
        pass


class PLACE_STRUCTURE(Substructure):
    class PLAC(PLACE_NAME, Substructure):
        class FONE(PLACE_PHONETIC, Substructure):
            class TYPE(PHONETISATION_METHOD, Substructure):
                pass

        class ROMN(PLACE_ROMANISED, Substructure):
            class TYPE(ROMANISATION_METHOD, Substructure):
                pass

        class MAP(Tag, Substructure):
            class LATI(PLACE_LATITUDE, Substructure):
                pass

            class LONG(PLACE_LONGITUDE, Substructure):
                pass

        NOTE_STRUCTURE = NOTE_STRUCTURE


class EVENT_DETAIL(Substructure):
    class TYPE(EVENT_OR_FACT_CLASSIFICATION, Substructure):
        pass

    class DATE(DATE_VALUE, Substructure):
        pass

    PLACE_STRUCTURE = PLACE_STRUCTURE
    ADDRESS_STRUCTURE = ADDRESS_STRUCTURE

    class AGNC(RESPONSIBLE_AGENCY, Substructure):
        pass

    class RELI(RELIGIOUS_AFFILIATION, Substructure):
        pass

    class CAUS(CAUSE_OF_EVENT, Substructure):
        pass

    NOTE_STRUCTURE = NOTE_STRUCTURE
    SOURCE_CITATION = SOURCE_CITATION
    MULTIMEDIA_LINK = MULTIMEDIA_LINK


class FAMILY_EVENT_DETAIL(Substructure):
    class HUSB(Tag, Substructure):
        class AGE(AGE_AT_EVENT, Substructure):
            pass

    class WIFE(Tag, Substructure):
        class AGE(AGE_AT_EVENT, Substructure):
            pass

    EVENT_DETAIL = EVENT_DETAIL


class FAMILY_EVENT_STRUCTUREs(Substructure):
    class FAMILY_EVENT_STRUCTURE(Substructure):
        pass

    class ANUL(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class CENS(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class DIV(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class DIVF(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class ENGA(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARB(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARC(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARR(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARL(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARS(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class RESI(FAMILY_EVENT_STRUCTURE, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class EVEN(FAMILY_EVENT_STRUCTURE, EVENT_DESCRIPTOR, NULL, Substructure):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL


class PERSONAL_NAME_PIECES(Substructure):
    class NPFX(NAME_PIECE_PREFIX, Substructure):
        pass

    class GIVN(NAME_PIECE_GIVEN, Substructure):
        pass

    class NICK(NAME_PIECE_NICKNAME, Substructure):
        pass

    class SPFX(NAME_PIECE_SURNAME_PREFIX, Substructure):
        pass

    class SURN(NAME_PIECE_SURNAME, Substructure):
        pass

    class NSFX(NAME_PIECE_SUFFIX, Substructure):
        pass

    NOTE_STRUCTURE = NOTE_STRUCTURE
    SOURCE_CITATION = SOURCE_CITATION


class PERSONAL_NAME_STRUCTURE(Substructure):
    class NAME(NAME_PERSONAL, Substructure):
        class TYPE(NAME_TYPE, Substructure):
            pass

        PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES

        class FONE(NAME_PHONETIC, Substructure):
            class TYPE(PHONETISATION_METHOD, Substructure):
                pass

            PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES

        class ROMN(NAME_ROMANISED, Substructure):
            class TYPE(ROMANISATION_METHOD, Substructure):
                pass

            PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES


class INDIVIDUAL_EVENT_DETAIL(Substructure):
    EVENT_DETAIL = EVENT_DETAIL

    class AGE(AGE_AT_EVENT, Substructure):
        pass


class INDIVIDUAL_EVENT_STRUCTUREs(Substructure):
    class INDIVIDUAL_EVENT_STRUCTURE(Substructure):
        pass

    class BIRT(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class FAMC(XREF_FAM, Substructure):
            pass

    class CHR(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class FAMC(XREF_FAM, Substructure):
            pass

    class DEAT(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class BURI(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class CREM(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class ADOP(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class FAMC(XREF_FAM, Substructure):
            class ADOP(ADOPTED_BY_WHICH_PARENT, Substructure):
                pass

    class BAPM(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class BARM(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class BASM(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class CHRA(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class CONF(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class FCOM(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class NATU(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class EMIG(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class IMMI(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class CENS(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class PROB(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class WILL(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class GRAD(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class RETI(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class EVEN(INDIVIDUAL_EVENT_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL


class INDIVIDUAL_ATTRIBUTE_STRUCTUREs(Substructure):
    class INDIVIDUAL_ATTRIBUTE_STRUCTURE(Substructure):
        pass

    class CAST(CASTE_NAME, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class DSCR(PHYSICAL_DESCRIPTION, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class EDUC(SCHOLASTIC_ACHIEVEMENT, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class IDNO(ID_NUMBER, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class NATI(NATIONAL_OR_TRIBAL_ORIGIN, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class NCHI(COUNT_OF_CHILDREN, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class NMR(NUMBER_OF_RELATONSHIPS, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class OCCU(OCCUPATION, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class PROP(POSSESSIONS, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class RELI(RELIGIOUS_AFFILIATION, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class RESI(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class TITL(NOBILITY_TYPE_TITLE, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass

    class FACT(ATTRIBUTE_DESCRIPTOR, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure):
            pass


class CHILD_TO_FAMILY_LINK(Substructure):
    class FAMC(XREF_FAM, Substructure):
        class PEDI(PEDIGREE_LINKAGE_TYPE, Substructure):
            pass

        NOTE_STRUCTURE = NOTE_STRUCTURE


class SPOUSE_TO_FAMILY_LINK(Substructure):
    class FAMS(XREF_FAM, Substructure):
        NOTE_STRUCTURE = NOTE_STRUCTURE


class ASSOCIATION_STRUCTURE(Substructure):
    class ASSO(XREF_INDI, Substructure):
        class RELA(RELATION_IS_DESCRIPTOR, Substructure):
            pass

        SOURCE_CITATION = SOURCE_CITATION
        NOTE_STRUCTURE = NOTE_STRUCTURE


class SOURCE_REPOSITORY_CITATION(Substructure):
    class REPO(XREF_REPO, Substructure):
        class CALN(SOURCE_CALL_NUMBER, Substructure):
            class MEDI(SOURCE_MEDIA_TYPE, Substructure):
                pass


class LINEAGE_LINKED_RECORDs(Substructure):
    class LINEAGE_LINKED_RECORD(Substructure):
        pass

    class FAM_GROUP_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class FAM(XREF_FAM, Pointer, Substructure):
            FAMILY_EVENT_STRUCTURE = FAMILY_EVENT_STRUCTUREs

            class HUSB(XREF_INDI, Substructure):
                pass

            class WIFE(XREF_INDI, Substructure):
                pass

            class CHIL(XREF_INDI, Substructure):
                pass

            class NCHI(COUNT_OF_CHILDREN, Substructure):
                pass

            class REFN(USER_REFERENCE_NUMBER, Substructure):
                pass

            class TYPE(USER_REFERENCE_TYPE, Substructure):
                pass

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTURE = NOTE_STRUCTURE
            SOURCE_CITATION = SOURCE_CITATION
            MULTIMEDIA_LINK = MULTIMEDIA_LINK

    class INDIVIDUAL_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class INDI(XREF_INDI, Pointer, Substructure):
            PERSONAL_NAME_STRUCTURE = PERSONAL_NAME_STRUCTURE

            class SEX(SEX_VALUE, Substructure):
                pass

            INDIVIDUAL_EVENT_STRUCTURE = INDIVIDUAL_EVENT_STRUCTUREs
            INDIVIDUAL_ATTRIBUTE_STRUCTURE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs
            CHILD_TO_FAMILY_LINK = CHILD_TO_FAMILY_LINK
            SPOUSE_TO_FAMILY_LINK = SPOUSE_TO_FAMILY_LINK
            ASSOCIATION_STRUCTURE = ASSOCIATION_STRUCTURE

            class REFN(USER_REFERENCE_NUMBER, Substructure):
                class TYPE(USER_REFERENCE_TYPE, Substructure):
                    pass

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTURE = NOTE_STRUCTURE
            SOURCE_CITATION = SOURCE_CITATION
            MULTIMEDIA_LINK = MULTIMEDIA_LINK

    class MULTIMEDIA_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class OBJE(XREF_OBJE, Pointer, Substructure):
            class FILE(MULTIMEDIA_FILE_REFERENCE, Substructure):
                class FORM(MULTIMEDIA_FORMAT, Substructure):
                    class TYPE(SOURCE_MEDIA_TYPE, Substructure):
                        pass

                class TITL(DESCRIPTIVE_TITLE, Substructure):
                    pass

            class REFN(USER_REFERENCE_NUMBER, Substructure):
                class TYPE(USER_REFERENCE_TYPE, Substructure):
                    pass

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            NOTE_STRUCTURE = NOTE_STRUCTURE
            SOURCE_CITATION = SOURCE_CITATION
            CHANGE_DATE = CHANGE_DATE

    class NOTE_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class NOTE(XREF_NOTE, USER_TEXT, Pointer, Substructure):
            class REFN(USER_REFERENCE_NUMBER, Substructure):
                class TYPE(USER_REFERENCE_TYPE, Substructure):
                    pass

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            SOURCE_CITATION = SOURCE_CITATION
            CHANGE_DATE = CHANGE_DATE

    class REPOSITORY_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class REPO(XREF_REPO, Pointer, Substructure):
            class NAME(NAME_OF_REPOSITORY, Substructure):
                pass

            ADDRESS_STRUCTURE = ADDRESS_STRUCTURE
            NOTE_STRUCTURE = NOTE_STRUCTURE

            class REFN(USER_REFERENCE_NUMBER, Substructure):
                class TYPE(USER_REFERENCE_TYPE, Substructure):
                    pass

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            CHANGE_DATE = CHANGE_DATE

    class SOURCE_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class SOUR(XREF_SOUR, Substructure):
            class DATA(Tag, Substructure):
                class EVEN(EVENTS_RECORDED, Substructure):
                    class DATE(DATE_PERIOD, Substructure):
                        pass

                    class PLAC(SOURCE_JURISDICTION_PLACE, Substructure):
                        pass

                class AGNC(RESPONSIBLE_AGENCY, Substructure):
                    pass

                NOTE_STRUCTURE = NOTE_STRUCTURE

            class AUTH(SOURCE_ORIGINATOR, Substructure):
                pass

            class TITL(SOURCE_DESCRIPTIVE_TITLE, Substructure):
                pass

            class ABBR(SOURCE_FILED_BY_ENTRY, Substructure):
                pass

            class PUBL(SOURCE_PUBLICATION_FACTS, Substructure):
                pass

            class TEXT(TEXT_FROM_SOURCE, Substructure):
                pass

            SOURCE_REPOSITORY_CITATION = SOURCE_REPOSITORY_CITATION

            class REFN(USER_REFERENCE_NUMBER, Substructure):
                class TYPE(USER_REFERENCE_TYPE, Substructure):
                    pass

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTURE = NOTE_STRUCTURE
            MULTIMEDIA_LINK = MULTIMEDIA_LINK


class GEDCOM_FORM_HEADER_EXTENSION(Substructure):
    class LINEAGE_LINKED_HEADER_EXTENSION(Substructure):
        class DEST(RECEIVING_SYSTEM_NAME, Substructure):
            pass

        class SOUR(SYSTEM_ID, Substructure):
            class VERS(PRODUCT_VERSION_NUMBER, Substructure):
                pass

            class NAME(NAME_OF_PRODUCT, Substructure):
                pass

            class CORP(NAME_OF_BUSINESS, Substructure):
                ADDRESS_STRUCTURE = ADDRESS_STRUCTURE

            class DATA(NAME_OF_SOURCE_DATA, Substructure):
                class DATE(PUBLICATION_DATE, Substructure):
                    pass

                class COPR(COPYRIGHT_SOURCE_DATA, Substructure):
                    pass

    class DATE(FILE_CREATION_DATE, Substructure):
        class TIME(TIME_VALUE, Substructure):
            pass

    class LANG(LANGUAGE_OF_TEXT, Substructure):
        pass

    class SUBM(XREF_SUBM, Substructure):
        pass

    class FILE(GEDCOM_FILE_NAME, Substructure):
        pass

    class COPR(COPYRIGHT_GEDCOM_FILE, Substructure):
        pass

    class NOTE(GEDCOM_CONTENT_DESCRIPTION, Substructure):
        pass


class GEDCOM_HEADER(Substructure):
    class HEAD(Tag, Substructure):
        class GEDC(Tag, Substructure):
            class VERS(GEDCOM_VERSION_NUMBER, Substructure):
                pass

            class FORM(GEDCOM_FORM, Substructure):
                class VERS(GEDCOM_VERSION_NUMBER, Substructure):
                    pass

        class CHAR(CHARACTER_ENCODING, Substructure):
            pass


class SUBMITTER_RECORD(Substructure):
    class SUBM(XREF_SUBM, Pointer, Substructure):
        class NAME(SUBMITTER_NAME, Substructure):
            pass

        ADDRESS_STRUCTURE = ADDRESS_STRUCTURE
        MULTIMEDIA_LINK = MULTIMEDIA_LINK

        class RIN(AUTOMATED_RECORD_ID, Substructure):
            pass

        NOTE_STRUCTURE = NOTE_STRUCTURE
        CHANGE_DATE = CHANGE_DATE


class GEDCOM_TRAILER(Substructure):
    class TRLR(Tag, Substructure):
        pass


class LINEAGE_LINKED_GEDCOM_FILE(Substructure):
    GEDCOM_HEADER = GEDCOM_HEADER
    GEDCOM_FORM_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSION
    SUBMITTER_RECORD = SUBMITTER_RECORD
    LINEAGE_LINKED_RECORD = LINEAGE_LINKED_RECORDs
    GEDCOM_TRAILER = GEDCOM_TRAILER
