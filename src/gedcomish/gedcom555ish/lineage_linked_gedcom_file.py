from typing import Iterable

from ..common import XREF_ID, Option, Pointer, Primitive, Substructure, Tag, get_gedcom_date


class ADDRESS_CITY(Primitive, Size=(1, 60)):
    pass


class ADDRESS_COUNTRY(Primitive, Size=(1, 60)):
    pass


class ADDRESS_EMAIL(Primitive, Size=(5, 120)):
    pass


class ADDRESS_FAX(Primitive, Size=(5, 60)):
    pass


class ADDRESS_LINE1(Primitive, Size=(1, 60)):
    pass


class ADDRESS_LINE2(Primitive, Size=(1, 60)):
    pass


class ADDRESS_LINE3(Primitive, Size=(1, 60)):
    pass


class ADDRESS_POSTAL_CODE(Primitive, Size=(1, 10)):
    pass


class ADDRESS_STATE(Primitive, Size=(1, 60)):
    pass


class ADDRESS_WEB_PAGE(Primitive, Size=(4, 2047)):
    pass


class ADOPTED_BY_WHICH_PARENT(Primitive, Size=(4, 4)):
    pass


class AGE_AT_EVENT(Primitive, Size=(2, 13)):
    pass


class ATTRIBUTE_DESCRIPTOR(Primitive, Size=(1, 90)):
    pass


class ATTRIBUTE_TYPE(Primitive, Size=(4, 4)):
    pass


class AUTOMATED_RECORD_ID(Primitive, Size=(1, 12)):
    pass


class BEFORE_COMMON_ERA(Primitive, Size=(2, 4)):
    pass


class CASTE_NAME(Primitive, Size=(1, 90)):
    pass


class CAUSE_OF_EVENT(Primitive, Size=(1, 90)):
    pass


class CERTAINTY_ASSESSMENT(Primitive, Size=(1, 1)):
    pass


class CHARACTER_ENCODING(Primitive, Size=(5, 7)):
    pass


class COPYRIGHT_GEDCOM_FILE(Primitive, Size=(1, 248)):
    pass


class COPYRIGHT_SOURCE_DATA(Primitive, Size=(1, 248)):
    pass


class COUNT_OF_CHILDREN(Primitive, Size=(1, 3)):
    pass


class DATE_APPROXIMATED(Primitive, Size=(8, 39)):
    pass


class DATE_CALENDAR_ESCAPE(Primitive, Size=(4, 15)):
    pass


class DATE_CALENDAR(Primitive, Size=(4, 35)):
    pass


class DATE_EXACT(Primitive, Size=(10, 11)):
    pass


class DATE_FREN(Primitive, Size=(4, 35)):
    pass


class DATE_GREG(Primitive, Size=(4, 35)):
    pass


class DATE_HEBR(Primitive, Size=(4, 35)):
    pass


class DATE_JULN(Primitive, Size=(4, 35)):
    pass


class DATE_PERIOD(Primitive, Size=(7, 35)):
    pass


class DATE_PHRASE(Primitive, Size=(1, 35)):
    pass


class DATE_RANGE(Primitive, Size=(8, 35)):
    pass


class DATE_VALUE(Primitive, Size=(1, 35)):
    @staticmethod
    def date(date_phrase: str):
        return get_gedcom_date(date_phrase)


class DATE(Primitive, Size=(4, 35)):
    pass


class DAY(Primitive, Size=(1, 2)):
    pass


class DESCRIPTIVE_TITLE(Primitive, Size=(1, 248)):
    pass


class DIGIT(Primitive, Size=(1, 1)):
    pass


class DUAL_STYLE_YEAR(Primitive, Size=(3, 7)):
    pass


class ENTRY_RECORDING_DATE(Primitive, Size=(1, 90)):
    pass


class EVENT_ATTRIBUTE_TYPE(Primitive, Size=(1, 15)):
    pass


class EVENT_DESCRIPTOR(Primitive, Size=(1, 90)):
    pass


class EVENT_OR_FACT_CLASSIFICATION(Primitive, Size=(1, 90)):
    pass


class EVENT_TYPE_CITED_FROM(Primitive, Size=(1, 15)):
    pass


class EVENT_TYPE_FAMILY(Primitive, Size=(3, 4)):
    pass


class EVENT_TYPE_INDIVIDUAL(Primitive, Size=(3, 4)):
    pass


class EVENTS_RECORDED(Primitive, Size=(1, 90)):
    pass


class FILE_CREATION_DATE(Primitive, Size=(10, 11)):
    pass


class GEDCOM_CONTENT_DESCRIPTION(Primitive, Size=(1, 248)):
    pass


class GEDCOM_FILE_NAME(Primitive, Size=(5, 248)):
    pass


class GEDCOM_FORM(Primitive, Size=(14, 20)):  # Size=(1,20)
    pass


class GEDCOM_VERSION_NUMBER(Primitive, Size=(3, 11)):
    pass


class ID_NUMBER(Primitive, Size=(1, 30)):
    pass


class LANGUAGE_ID(Primitive, Size=(1, 15)):
    pass


class LANGUAGE_OF_TEXT(Primitive, Size=(1, 15)):
    pass


class MONTH_FREN(Primitive, Size=4):
    pass


class MONTH_HEBR(Primitive, Size=3):
    pass


class MONTH(Primitive, Size=3):
    pass


class MULTIMEDIA_FILE_REFERENCE(Primitive, Size=(1, 259)):
    pass


class MULTIMEDIA_FORMAT(Primitive, Size=(3, 4)):
    pass


class NAME_OF_BUSINESS(Primitive, Size=(1, 90)):
    pass


class NAME_OF_PRODUCT(Primitive, Size=(1, 90)):
    pass


class NAME_OF_REPOSITORY(Primitive, Size=(1, 90)):
    pass


class NAME_OF_SOURCE_DATA(Primitive, Size=(1, 90)):
    pass


class NAME_PERSONAL(Primitive, Size=(1, 120)):
    pass


class NAME_PHONETIC(Primitive, Size=(1, 120)):
    pass


class NAME_PIECE_GIVEN(Primitive, Size=(1, 120)):
    pass


class NAME_PIECE_NICKNAME(Primitive, Size=(1, 30)):
    pass


class NAME_PIECE_PREFIX(Primitive, Size=(1, 30)):
    pass


class NAME_PIECE_SUFFIX(Primitive, Size=(1, 30)):
    pass


class NAME_PIECE_SURNAME_PREFIX(Primitive, Size=(1, 30)):
    pass


class NAME_PIECE_SURNAME(Primitive, Size=(1, 120)):
    pass


class NAME_PIECE(Primitive, Size=(1, 90)):
    pass


class NAME_ROMANISED(Primitive, Size=(1, 120)):
    pass


class NAME_TEXT(Primitive, Size=(1, 120)):
    pass


class NAME_TYPE(Primitive, Size=(5, 30)):
    pass


class NATIONAL_OR_TRIBAL_ORIGIN(Primitive, Size=(1, 120)):
    pass


class NOBILITY_TYPE_TITLE(Primitive, Size=(1, 120)):
    pass


class NULL(Primitive, Size=(0, 0)):
    pass


class NUMBER_OF_RELATIONSHIPS(Primitive, Size=(1, 3)):
    pass


class NUMBER(Primitive, Size=(3, 4)):
    pass


class OCCUPATION(Primitive, Size=(1, 90)):
    pass


class PEDIGREE_LINKAGE_TYPE(Primitive, Size=(5, 7)):
    pass


class PHONE_NUMBER(Primitive, Size=(1, 25)):
    pass


class PHONETISATION_METHOD(Primitive, Size=(5, 30)):
    pass


class PHYSICAL_DESCRIPTION(Primitive, Size=(1, 4095)):
    pass


class PLACE_LATITUDE(Primitive, Size=(2, 10)):
    pass


class PLACE_LONGITUDE(Primitive, Size=(2, 11)):
    pass


class PLACE_NAME(Primitive, Size=(1, 120)):
    pass


class PLACE_PHONETIC(Primitive, Size=(1, 120)):
    pass


class PLACE_ROMANISED(Primitive, Size=(1, 120)):
    pass


class PLACE_TEXT(Primitive, Size=(1, 120)):
    pass


class POSSESSIONS(Primitive, Size=(1, 248)):
    pass


class PRODUCT_VERSION_NUMBER(Primitive, Size=(3, 15)):
    pass


class PUBLICATION_DATE(Primitive, Size=(10, 11)):
    pass


class RECEIVING_SYSTEM_NAME(Primitive, Size=(1, 20)):
    pass


class RELATION_IS_DESCRIPTOR(Primitive, Size=(1, 25)):
    pass


class RELIGIOUS_AFFILIATION(Primitive, Size=(1, 90)):
    pass


class RESPONSIBLE_AGENCY(Primitive, Size=(1, 120)):
    pass


class ROLE_DESCRIPTOR(Primitive, Size=(1, 25)):
    pass


class ROLE_IN_EVENT(Primitive, Size=(3, 27)):
    pass


class ROMANISATION_METHOD(Primitive, Size=(5, 30)):
    pass


class SCHOLASTIC_ACHIEVEMENT(Primitive, Size=(1, 248)):
    pass


class SEX_VALUE(Primitive, Size=(1, 1)):
    pass


class SOURCE_CALL_NUMBER(Primitive, Size=(1, 120)):
    pass


class SOURCE_DESCRIPTIVE_TITLE(Primitive, Size=(1, 4095)):
    pass


class SOURCE_FILED_BY_ENTRY(Primitive, Size=(1, 60)):
    pass


class SOURCE_JURISDICTION_PLACE(Primitive, Size=(1, 120)):
    pass


class SOURCE_MEDIA_TYPE(Primitive, Size=(1, 15)):
    pass


class SOURCE_ORIGINATOR(Primitive, Size=(1, 255)):
    pass


class SOURCE_PUBLICATION_FACTS(Primitive, Size=(1, 4095)):
    pass


class SUBMITTER_NAME(Primitive, Size=(1, 60)):
    pass


class SYSTEM_ID(Primitive, Size=(1, 20)):
    pass


class TEXT_FROM_SOURCE(Primitive, Size=(1, 32767)):
    pass


class TEXT(Primitive, Size=(1, 32767)):
    pass


class TIME_VALUE(Primitive, Size=(7, 12)):
    pass


class USER_REFERENCE_NUMBER(Primitive, Size=(1, 20)):
    pass


class USER_REFERENCE_TYPE(Primitive, Size=(1, 40)):
    pass


class USER_TEXT(Primitive, Size=(1, 32767)):
    pass


class WHERE_WITHIN_SOURCE(Primitive, Size=(1, 248)):
    pass


class XREF_FAM(XREF_ID, Size=(3, 22)):
    pass


class XREF_INDI(XREF_ID, Size=(3, 22)):
    pass


class XREF_NOTE(XREF_ID, Size=(3, 22)):
    pass


class XREF_OBJE(XREF_ID, Size=(3, 22)):
    pass


class XREF_REPO(XREF_ID, Size=(3, 22)):
    pass


class XREF_SOUR(XREF_ID, Size=(3, 22)):
    pass


class XREF_SUBM(XREF_ID, Size=(3, 22)):
    pass


class YEAR(Primitive, Size=(3, 4)):
    pass


class Y(Primitive, Size=(1, 1)):
    pass


class MULTIMEDIA_LINK(Substructure, delta_level=0):
    class OBJE(XREF_OBJE, Substructure, delta_level=0):
        pass


class NOTE_STRUCTURE(Substructure, delta_level=0):
    class NOTE(XREF_NOTE, USER_TEXT, Substructure, delta_level=0):
        pass


class CHANGE_DATE(Substructure, delta_level=0):
    class CHAN(Tag, Substructure, delta_level=0):
        class DATE(DATE_EXACT, Substructure, delta_level=1):
            class TIME(TIME_VALUE, Substructure, delta_level=1):
                pass

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


class TEXTs(Substructure):
    class TEXT(TEXT_FROM_SOURCE, Option, Substructure, delta_level=1):
        pass


class SOURCE_CITATION(Substructure, delta_level=-1):
    class SOUR(XREF_SOUR, Substructure, delta_level=0):
        class PAGE(WHERE_WITHIN_SOURCE, Substructure, delta_level=1):
            pass

        class EVEN(EVENT_TYPE_CITED_FROM, Substructure, delta_level=1):
            class ROLE(ROLE_IN_EVENT, Substructure, delta_level=1):
                pass

        class DATA(Tag, Substructure, delta_level=1):
            class DATE(ENTRY_RECORDING_DATE, Substructure, delta_level=1):
                pass

            TEXTs = Iterable[TEXTs.TEXT]

        MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]

        class QUAY(CERTAINTY_ASSESSMENT, Substructure, delta_level=1):
            pass


class ADDRESS_STRUCTURE(Substructure, delta_level=0):
    class ADDR(Tag, Substructure, delta_level=0):
        class ADR1(ADDRESS_LINE1, Substructure, delta_level=1):
            pass

        class ADR2(ADDRESS_LINE2, Substructure, delta_level=1):
            pass

        class ADR3(ADDRESS_LINE3, Substructure, delta_level=1):
            pass

        class CITY(ADDRESS_CITY, Substructure, delta_level=1):
            pass

        class STAE(ADDRESS_STATE, Substructure, delta_level=1):
            pass

        class POST(ADDRESS_POSTAL_CODE, Substructure, delta_level=1):
            pass

        class CTRY(ADDRESS_COUNTRY, Substructure, delta_level=1):
            pass

    class PHON(PHONE_NUMBER, Substructure, delta_level=0):
        pass

    class EMAIL(ADDRESS_EMAIL, Substructure, delta_level=0):
        pass

    class FAX(ADDRESS_FAX, Substructure, delta_level=0):
        pass

    class WWW(ADDRESS_WEB_PAGE, Substructure, delta_level=0):
        pass


class PLACE_STRUCTURE(Substructure, delta_level=-1):
    class PLAC(PLACE_NAME, Substructure, delta_level=0):
        # TODO: should this be outside?
        class FONE(PLACE_PHONETIC, Substructure, delta_level=1):
            class TYPE(PHONETISATION_METHOD, Substructure, delta_level=1):
                pass

        FONEs = Iterable[FONE]

        # TODO: should this be outside?
        class ROMN(PLACE_ROMANISED, Substructure, delta_level=1):
            class TYPE(ROMANISATION_METHOD, Substructure, delta_level=1):
                pass

        ROMNs = Iterable[ROMN]

        class MAP(Tag, Substructure, delta_level=1):
            class LATI(PLACE_LATITUDE, Substructure, delta_level=1):
                pass

            class LONG(PLACE_LONGITUDE, Substructure, delta_level=1):
                pass

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


class EVENT_DETAIL(Substructure, delta_level=-1):
    class TYPE(EVENT_OR_FACT_CLASSIFICATION, Substructure, delta_level=0):
        pass

    class DATE(DATE_VALUE, Substructure, delta_level=0):
        pass

    PLACE_STRUCTURE = PLACE_STRUCTURE
    ADDRESS_STRUCTURE = ADDRESS_STRUCTURE

    class AGNC(RESPONSIBLE_AGENCY, Substructure, delta_level=0):
        pass

    class RELI(RELIGIOUS_AFFILIATION, Substructure, delta_level=0):
        pass

    class CAUS(CAUSE_OF_EVENT, Substructure, delta_level=0):
        pass

    NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
    SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
    MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]


class FAMILY_EVENT_DETAIL(Substructure, delta_level=0):
    class HUSB(Tag, Substructure, delta_level=0):
        class AGE(AGE_AT_EVENT, Substructure, delta_level=1):
            pass

    class WIFE(Tag, Substructure, delta_level=0):
        class AGE(AGE_AT_EVENT, Substructure, delta_level=1):
            pass

    EVENT_DETAIL = EVENT_DETAIL


class FAMILY_EVENT_STRUCTUREs(Substructure, delta_level=None):
    class FAMILY_EVENT_STRUCTURE(Substructure, delta_level=0):
        pass

    class ANUL(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class CENS(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class DIV(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class DIVF(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class ENGA(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARB(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARC(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARR(FAMILY_EVENT_STRUCTURE, Option, Y, NULL, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARL(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class MARS(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class RESI(FAMILY_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL

    class EVEN(FAMILY_EVENT_STRUCTURE, Option, EVENT_DESCRIPTOR, NULL, Substructure, delta_level=0):
        FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL


class PERSONAL_NAME_PIECES(Substructure, delta_level=0):
    class NPFX(NAME_PIECE_PREFIX, Substructure, delta_level=0):
        pass

    class GIVN(NAME_PIECE_GIVEN, Substructure, delta_level=0):
        pass

    class NICK(NAME_PIECE_NICKNAME, Substructure, delta_level=0):
        pass

    class SPFX(NAME_PIECE_SURNAME_PREFIX, Substructure, delta_level=0):
        pass

    class SURN(NAME_PIECE_SURNAME, Substructure, delta_level=0):
        pass

    class NSFX(NAME_PIECE_SUFFIX, Substructure, delta_level=0):
        pass

    NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
    SOURCE_CITATIONs = Iterable[SOURCE_CITATION]


class PERSONAL_NAME_STRUCTURE(Substructure, delta_level=0):
    class NAME(NAME_PERSONAL, Substructure, delta_level=0):
        class TYPE(NAME_TYPE, Substructure, delta_level=0):
            pass

        PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES

        # TODO: should this be outside?
        class FONE(NAME_PHONETIC, Substructure, delta_level=0):
            class TYPE(PHONETISATION_METHOD, Substructure, delta_level=1):
                pass

            PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES

        FONEs = Iterable[FONE]

        # TODO: should this be outside?
        class ROMN(NAME_ROMANISED, Substructure, delta_level=0):
            class TYPE(ROMANISATION_METHOD, Substructure, delta_level=1):
                pass

            PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES

        ROMNs = Iterable[ROMN]


class INDIVIDUAL_EVENT_DETAIL(Substructure, delta_level=0):
    EVENT_DETAIL = EVENT_DETAIL

    class AGE(AGE_AT_EVENT, Substructure, delta_level=1):
        pass


class INDIVIDUAL_EVENT_STRUCTUREs(Substructure, delta_level=None):
    class INDIVIDUAL_EVENT_STRUCTURE(Substructure, delta_level=0):
        pass

    class BIRT(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class FAMC(XREF_FAM, Substructure, delta_level=1):
            pass

    class CHR(INDIVIDUAL_EVENT_STRUCTURE, Option, Y, NULL, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class FAMC(XREF_FAM, Substructure, delta_level=1):
            pass

    class DEAT(INDIVIDUAL_EVENT_STRUCTURE, Option, Y, NULL, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class BURI(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class CREM(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class ADOP(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class FAMC(XREF_FAM, Substructure, delta_level=1):
            class ADOP(ADOPTED_BY_WHICH_PARENT, Substructure, delta_level=1):
                pass

    class BAPM(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class BARM(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class BASM(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class CHRA(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class CONF(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class FCOM(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class NATU(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class EMIG(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class IMMI(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class CENS(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class PROB(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class WILL(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class GRAD(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class RETI(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

    class EVEN(INDIVIDUAL_EVENT_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL


class INDIVIDUAL_ATTRIBUTE_STRUCTUREs(Substructure, delta_level=None):
    class INDIVIDUAL_ATTRIBUTE_STRUCTURE(Substructure, delta_level=0):
        pass

    class CAST(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, CASTE_NAME, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class DSCR(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, PHYSICAL_DESCRIPTION, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class EDUC(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, SCHOLASTIC_ACHIEVEMENT, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class IDNO(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, ID_NUMBER, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class NATI(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, NATIONAL_OR_TRIBAL_ORIGIN, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class NCHI(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, COUNT_OF_CHILDREN, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class NMR(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, NUMBER_OF_RELATIONSHIPS, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class OCCU(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, OCCUPATION, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class PROP(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, POSSESSIONS, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class RELI(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, RELIGIOUS_AFFILIATION, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class RESI(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, Tag, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class TITL(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, NOBILITY_TYPE_TITLE, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass

    class FACT(INDIVIDUAL_ATTRIBUTE_STRUCTURE, Option, ATTRIBUTE_DESCRIPTOR, Substructure, delta_level=0):
        INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL

        class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
            pass


class CHILD_TO_FAMILY_LINK(Substructure, delta_level=0):
    class FAMC(XREF_FAM, Substructure, delta_level=0):
        class PEDI(PEDIGREE_LINKAGE_TYPE, Substructure, delta_level=1):
            pass

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


class SPOUSE_TO_FAMILY_LINK(Substructure, delta_level=0):
    class FAMS(XREF_FAM, Substructure, delta_level=0):
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


class ASSOCIATION_STRUCTURE(Substructure, delta_level=0):
    class ASSO(XREF_INDI, Substructure, delta_level=0):
        class RELA(RELATION_IS_DESCRIPTOR, Substructure, delta_level=1):
            pass

        SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


class SOURCE_REPOSITORY_CITATION(Substructure, delta_level=0):
    class REPO(XREF_REPO, Substructure, delta_level=0):
        class CALN(SOURCE_CALL_NUMBER, Substructure, delta_level=1):
            class MEDI(SOURCE_MEDIA_TYPE, Substructure, delta_level=1):
                pass


class REFN(USER_REFERENCE_NUMBER, Substructure, delta_level=0):
    class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
        pass


class EVENs(Substructure, delta_level=None):
    class EVEN(EVENTS_RECORDED, Substructure, delta_level=0):
        class DATE(DATE_PERIOD, Substructure, delta_level=1):
            pass

        class PLAC(SOURCE_JURISDICTION_PLACE, Substructure, delta_level=1):
            pass


class CHIL(XREF_INDI, Substructure, delta_level=0):
    pass


class LINEAGE_LINKED_RECORDs(Substructure, delta_level=None):
    EVENs = EVENs

    class LINEAGE_LINKED_RECORD(Substructure, delta_level=0):
        pass

    class FAM_GROUP_RECORD(LINEAGE_LINKED_RECORD, Option, Substructure, delta_level=0):
        class FAM(XREF_FAM, Pointer, Substructure, delta_level=0):
            FAMILY_EVENT_STRUCTUREs = Iterable[FAMILY_EVENT_STRUCTUREs.FAMILY_EVENT_STRUCTURE]

            class HUSB(XREF_INDI, Substructure, delta_level=1):
                pass

            class WIFE(XREF_INDI, Substructure, delta_level=1):
                pass

            CHILs = Iterable[CHIL]

            class NCHI(COUNT_OF_CHILDREN, Substructure, delta_level=1):
                pass

            REFNs = Iterable[REFN]

            class TYPE(USER_REFERENCE_TYPE, Substructure, delta_level=1):
                pass

            class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]

    class INDIVIDUAL_RECORD(LINEAGE_LINKED_RECORD, Option, Substructure, delta_level=0):
        class INDI(XREF_INDI, Pointer, Substructure, delta_level=0):
            PERSONAL_NAME_STRUCTUREs = Iterable[PERSONAL_NAME_STRUCTURE]

            class SEX(SEX_VALUE, Substructure, delta_level=1):
                pass

            INDIVIDUAL_EVENT_STRUCTUREs = Iterable[INDIVIDUAL_EVENT_STRUCTUREs.INDIVIDUAL_EVENT_STRUCTURE]
            INDIVIDUAL_ATTRIBUTE_STRUCTUREs = Iterable[INDIVIDUAL_ATTRIBUTE_STRUCTUREs.INDIVIDUAL_ATTRIBUTE_STRUCTURE]
            CHILD_TO_FAMILY_LINKs = Iterable[CHILD_TO_FAMILY_LINK]
            SPOUSE_TO_FAMILY_LINKs = Iterable[SPOUSE_TO_FAMILY_LINK]
            ASSOCIATION_STRUCTUREs = Iterable[ASSOCIATION_STRUCTURE]

            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]

    class MULTIMEDIA_RECORD(LINEAGE_LINKED_RECORD, Option, Substructure, delta_level=0):
        class OBJE(XREF_OBJE, Pointer, Substructure, delta_level=0):
            # TODO: should this be outside?
            class FILE(MULTIMEDIA_FILE_REFERENCE, Substructure, delta_level=1):
                class FORM(MULTIMEDIA_FORMAT, Substructure, delta_level=1):
                    class TYPE(SOURCE_MEDIA_TYPE, Substructure, delta_level=1):
                        pass

                class TITL(DESCRIPTIVE_TITLE, Substructure, delta_level=1):
                    pass

            FILEs = Iterable[FILE]

            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
                pass

            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            CHANGE_DATE = CHANGE_DATE

    class NOTE_RECORD(LINEAGE_LINKED_RECORD, Option, Substructure, delta_level=0):
        class NOTE(XREF_NOTE, Pointer, USER_TEXT, Substructure, delta_level=0):
            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
                pass

            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            CHANGE_DATE = CHANGE_DATE

    class REPOSITORY_RECORD(LINEAGE_LINKED_RECORD, Option, Substructure, delta_level=0):
        class REPO(XREF_REPO, Pointer, Substructure, delta_level=0):
            class NAME(NAME_OF_REPOSITORY, Substructure, delta_level=1):
                pass

            ADDRESS_STRUCTURE = ADDRESS_STRUCTURE
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
                pass

            CHANGE_DATE = CHANGE_DATE

    class SOURCE_RECORD(LINEAGE_LINKED_RECORD, Option, Substructure, delta_level=0):
        class SOUR(XREF_SOUR, Pointer, Substructure, delta_level=0):
            class DATA(Tag, Substructure, delta_level=1):
                EVENs = Iterable[EVENs.EVEN]

                class AGNC(RESPONSIBLE_AGENCY, Substructure, delta_level=1):
                    pass

                NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]

            class AUTH(SOURCE_ORIGINATOR, Substructure, delta_level=1):
                pass

            class TITL(SOURCE_DESCRIPTIVE_TITLE, Substructure, delta_level=1):
                pass

            class ABBR(SOURCE_FILED_BY_ENTRY, Substructure, delta_level=1):
                pass

            class PUBL(SOURCE_PUBLICATION_FACTS, Substructure, delta_level=1):
                pass

            class TEXT(TEXT_FROM_SOURCE, Substructure, delta_level=1):
                pass

            SOURCE_REPOSITORY_CITATIONs = Iterable[SOURCE_REPOSITORY_CITATION]

            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]


class SUBMITTER_RECORD(Substructure, delta_level=0):
    class SUBM(XREF_SUBM, Pointer, Substructure, delta_level=0):
        class NAME(SUBMITTER_NAME, Substructure, delta_level=1):
            pass

        ADDRESS_STRUCTURE = ADDRESS_STRUCTURE
        MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]

        class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
            pass

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
        CHANGE_DATE = CHANGE_DATE


class GEDCOM_HEADER(Substructure, delta_level=0):
    class HEAD(Tag, Substructure, delta_level=0):
        class GEDC(Tag, Substructure, delta_level=1):
            class VERS(GEDCOM_VERSION_NUMBER, Substructure, delta_level=1):
                pass

            class FORM(GEDCOM_FORM, Substructure, delta_level=1):
                class VERS(GEDCOM_VERSION_NUMBER, Substructure, delta_level=1):
                    pass

        class CHAR(CHARACTER_ENCODING, Substructure, delta_level=1):
            pass


class GEDCOM_FORM_HEADER_EXTENSIONs(Substructure, delta_level=None):
    class GEDCOM_FORM_HEADER_EXTENSION(Substructure, delta_level=1):
        pass

    class LINEAGE_LINKED_HEADER_EXTENSION(GEDCOM_FORM_HEADER_EXTENSION, Option, Substructure, delta_level=1):
        class DEST(RECEIVING_SYSTEM_NAME, Substructure, delta_level=0):
            pass

        class SOUR(SYSTEM_ID, Substructure, delta_level=0):
            class VERS(PRODUCT_VERSION_NUMBER, Substructure, delta_level=1):
                pass

            class NAME(NAME_OF_PRODUCT, Substructure, delta_level=1):
                pass

            class CORP(NAME_OF_BUSINESS, Substructure, delta_level=1):
                ADDRESS_STRUCTURE = ADDRESS_STRUCTURE

            class DATA(NAME_OF_SOURCE_DATA, Substructure, delta_level=1):
                class DATE(PUBLICATION_DATE, Substructure, delta_level=1):
                    pass

                class COPR(COPYRIGHT_SOURCE_DATA, Substructure, delta_level=1):
                    pass

        class DATE(FILE_CREATION_DATE, Substructure, delta_level=0):
            class TIME(TIME_VALUE, Substructure, delta_level=1):
                pass

        class LANG(LANGUAGE_OF_TEXT, Substructure, delta_level=0):
            pass

        class SUBM(XREF_SUBM, Substructure, delta_level=0):
            pass

        class FILE(GEDCOM_FILE_NAME, Substructure, delta_level=0):
            pass

        class COPR(COPYRIGHT_GEDCOM_FILE, Substructure, delta_level=0):
            pass

        class NOTE(GEDCOM_CONTENT_DESCRIPTION, Substructure, delta_level=0):
            pass


class FORM_RECORDS(Substructure, delta_level=-1):
    SUBMITTER_RECORD = SUBMITTER_RECORD
    LINEAGE_LINKED_RECORDs = Iterable[LINEAGE_LINKED_RECORDs.LINEAGE_LINKED_RECORD]


class GEDCOM_TRAILER(Substructure, delta_level=0):
    class TRLR(Tag, Substructure, delta_level=0):
        pass


class LINEAGE_LINKED_GEDCOM_FILE(Substructure, delta_level=-1):
    GEDCOM_HEADER = GEDCOM_HEADER
    GEDCOM_FORM_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION
    FORM_RECORDS = FORM_RECORDS
    GEDCOM_TRAILER = GEDCOM_TRAILER


__all__ = [
    "ADDRESS_CITY",
    "ADDRESS_COUNTRY",
    "ADDRESS_EMAIL",
    "ADDRESS_FAX",
    "ADDRESS_LINE1",
    "ADDRESS_LINE2",
    "ADDRESS_LINE3",
    "ADDRESS_POSTAL_CODE",
    "ADDRESS_STATE",
    "ADDRESS_WEB_PAGE",
    "ADOPTED_BY_WHICH_PARENT",
    "AGE_AT_EVENT",
    "ATTRIBUTE_DESCRIPTOR",
    "ATTRIBUTE_TYPE",
    "AUTOMATED_RECORD_ID",
    "BEFORE_COMMON_ERA",
    "CASTE_NAME",
    "CAUSE_OF_EVENT",
    "CERTAINTY_ASSESSMENT",
    "CHARACTER_ENCODING",
    "COPYRIGHT_GEDCOM_FILE",
    "COPYRIGHT_SOURCE_DATA",
    "COUNT_OF_CHILDREN",
    "DATE_APPROXIMATED",
    "DATE_CALENDAR_ESCAPE",
    "DATE_CALENDAR",
    "DATE_EXACT",
    "DATE_FREN",
    "DATE_GREG",
    "DATE_HEBR",
    "DATE_JULN",
    "DATE_PERIOD",
    "DATE_PHRASE",
    "DATE_RANGE",
    "DATE_VALUE",
    "DATE",
    "DAY",
    "DESCRIPTIVE_TITLE",
    "DIGIT",
    "DUAL_STYLE_YEAR",
    "ENTRY_RECORDING_DATE",
    "EVENT_ATTRIBUTE_TYPE",
    "EVENT_DESCRIPTOR",
    "EVENT_OR_FACT_CLASSIFICATION",
    "EVENT_TYPE_CITED_FROM",
    "EVENT_TYPE_FAMILY",
    "EVENT_TYPE_INDIVIDUAL",
    "EVENTS_RECORDED",
    "FILE_CREATION_DATE",
    "GEDCOM_CONTENT_DESCRIPTION",
    "GEDCOM_FILE_NAME",
    "GEDCOM_FORM",
    "GEDCOM_VERSION_NUMBER",
    "ID_NUMBER",
    "LANGUAGE_ID",
    "LANGUAGE_OF_TEXT",
    "MONTH_FREN",
    "MONTH_HEBR",
    "MONTH",
    "MULTIMEDIA_FILE_REFERENCE",
    "MULTIMEDIA_FORMAT",
    "NAME_OF_BUSINESS",
    "NAME_OF_PRODUCT",
    "NAME_OF_REPOSITORY",
    "NAME_OF_SOURCE_DATA",
    "NAME_PERSONAL",
    "NAME_PHONETIC",
    "NAME_PIECE_GIVEN",
    "NAME_PIECE_NICKNAME",
    "NAME_PIECE_PREFIX",
    "NAME_PIECE_SUFFIX",
    "NAME_PIECE_SURNAME_PREFIX",
    "NAME_PIECE_SURNAME",
    "NAME_PIECE",
    "NAME_ROMANISED",
    "NAME_TEXT",
    "NAME_TYPE",
    "NATIONAL_OR_TRIBAL_ORIGIN",
    "NOBILITY_TYPE_TITLE",
    "NULL",
    "NUMBER_OF_RELATIONSHIPS",
    "NUMBER",
    "OCCUPATION",
    "PEDIGREE_LINKAGE_TYPE",
    "PHONE_NUMBER",
    "PHONETISATION_METHOD",
    "PHYSICAL_DESCRIPTION",
    "PLACE_LATITUDE",
    "PLACE_LONGITUDE",
    "PLACE_NAME",
    "PLACE_PHONETIC",
    "PLACE_ROMANISED",
    "PLACE_TEXT",
    "POSSESSIONS",
    "PRODUCT_VERSION_NUMBER",
    "PUBLICATION_DATE",
    "RECEIVING_SYSTEM_NAME",
    "RELATION_IS_DESCRIPTOR",
    "RELIGIOUS_AFFILIATION",
    "RESPONSIBLE_AGENCY",
    "ROLE_DESCRIPTOR",
    "ROLE_IN_EVENT",
    "ROMANISATION_METHOD",
    "SCHOLASTIC_ACHIEVEMENT",
    "SEX_VALUE",
    "SOURCE_CALL_NUMBER",
    "SOURCE_DESCRIPTIVE_TITLE",
    "SOURCE_FILED_BY_ENTRY",
    "SOURCE_JURISDICTION_PLACE",
    "SOURCE_MEDIA_TYPE",
    "SOURCE_ORIGINATOR",
    "SOURCE_PUBLICATION_FACTS",
    "SUBMITTER_NAME",
    "SYSTEM_ID",
    "TEXT_FROM_SOURCE",
    "TEXT",
    "TIME_VALUE",
    "USER_REFERENCE_NUMBER",
    "USER_REFERENCE_TYPE",
    "USER_TEXT",
    "WHERE_WITHIN_SOURCE",
    "XREF_FAM",
    "XREF_INDI",
    "XREF_NOTE",
    "XREF_OBJE",
    "XREF_REPO",
    "XREF_SOUR",
    "XREF_SUBM",
    "YEAR",
    "Y",
    "MULTIMEDIA_LINK",
    "NOTE_STRUCTURE",
    "CHANGE_DATE",
    "TEXTs",
    "SOURCE_CITATION",
    "ADDRESS_STRUCTURE",
    "PLACE_STRUCTURE",
    "EVENT_DETAIL",
    "FAMILY_EVENT_DETAIL",
    "FAMILY_EVENT_STRUCTUREs",
    "PERSONAL_NAME_PIECES",
    "PERSONAL_NAME_STRUCTURE",
    "INDIVIDUAL_EVENT_DETAIL",
    "INDIVIDUAL_EVENT_STRUCTUREs",
    "INDIVIDUAL_ATTRIBUTE_STRUCTUREs",
    "CHILD_TO_FAMILY_LINK",
    "SPOUSE_TO_FAMILY_LINK",
    "ASSOCIATION_STRUCTURE",
    "SOURCE_REPOSITORY_CITATION",
    "REFN",
    "EVENs",
    "CHIL",
    "LINEAGE_LINKED_RECORDs",
    "SUBMITTER_RECORD",
    "GEDCOM_HEADER",
    "GEDCOM_FORM_HEADER_EXTENSIONs",
    "FORM_RECORDS",
    "GEDCOM_TRAILER",
    "LINEAGE_LINKED_GEDCOM_FILE",
]
