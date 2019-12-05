from typing import Iterable

from ..common import Option, Pointer, Substructure, Tag

from .primitives import (
    ADDRESS_CITY,
    ADDRESS_COUNTRY,
    ADDRESS_EMAIL,
    ADDRESS_FAX,
    ADDRESS_LINE1,
    ADDRESS_LINE2,
    ADDRESS_LINE3,
    ADDRESS_POSTAL_CODE,
    ADDRESS_STATE,
    ADDRESS_WEB_PAGE,
    ADOPTED_BY_WHICH_PARENT,
    AGE_AT_EVENT,
    ATTRIBUTE_DESCRIPTOR,
    ATTRIBUTE_TYPE,
    AUTOMATED_RECORD_ID,
    BEFORE_COMMON_ERA,
    CASTE_NAME,
    CAUSE_OF_EVENT,
    CERTAINTY_ASSESSMENT,
    CHARACTER_ENCODING,
    COPYRIGHT_GEDCOM_FILE,
    COPYRIGHT_SOURCE_DATA,
    COUNT_OF_CHILDREN,
    DATE,
    DATE_APPROXIMATED,
    DATE_CALENDAR,
    DATE_CALENDAR_ESCAPE,
    DATE_EXACT,
    DATE_FREN,
    DATE_GREG,
    DATE_HEBR,
    DATE_JULN,
    DATE_PERIOD,
    DATE_PHRASE,
    DATE_RANGE,
    DATE_VALUE,
    DAY,
    DESCRIPTIVE_TITLE,
    DIGIT,
    DUAL_STYLE_YEAR,
    ENTRY_RECORDING_DATE,
    EVENT_ATTRIBUTE_TYPE,
    EVENT_DESCRIPTOR,
    EVENT_OR_FACT_CLASSIFICATION,
    EVENT_TYPE_CITED_FROM,
    EVENT_TYPE_FAMILY,
    EVENT_TYPE_INDIVIDUAL,
    EVENTS_RECORDED,
    FILE_CREATION_DATE,
    GEDCOM_CONTENT_DESCRIPTION,
    GEDCOM_FILE_NAME,
    GEDCOM_FORM,
    GEDCOM_VERSION_NUMBER,
    ID_NUMBER,
    LANGUAGE_ID,
    LANGUAGE_OF_TEXT,
    MONTH,
    MONTH_FREN,
    MONTH_HEBR,
    MULTIMEDIA_FILE_REFERENCE,
    MULTIMEDIA_FORMAT,
    NAME_OF_BUSINESS,
    NAME_OF_PRODUCT,
    NAME_OF_REPOSITORY,
    NAME_OF_SOURCE_DATA,
    NAME_PERSONAL,
    NAME_PHONETIC,
    NAME_PIECE,
    NAME_PIECE_GIVEN,
    NAME_PIECE_NICKNAME,
    NAME_PIECE_PREFIX,
    NAME_PIECE_SUFFIX,
    NAME_PIECE_SURNAME,
    NAME_PIECE_SURNAME_PREFIX,
    NAME_ROMANISED,
    NAME_TEXT,
    NAME_TYPE,
    NATIONAL_OR_TRIBAL_ORIGIN,
    NOBILITY_TYPE_TITLE,
    NULL,
    NUMBER,
    NUMBER_OF_RELATIONSHIPS,
    OCCUPATION,
    PEDIGREE_LINKAGE_TYPE,
    PHONE_NUMBER,
    PHONETISATION_METHOD,
    PHYSICAL_DESCRIPTION,
    PLACE_LATITUDE,
    PLACE_LONGITUDE,
    PLACE_NAME,
    PLACE_PHONETIC,
    PLACE_ROMANISED,
    PLACE_TEXT,
    POSSESSIONS,
    PRODUCT_VERSION_NUMBER,
    PUBLICATION_DATE,
    RECEIVING_SYSTEM_NAME,
    RELATION_IS_DESCRIPTOR,
    RELIGIOUS_AFFILIATION,
    RESPONSIBLE_AGENCY,
    ROLE_DESCRIPTOR,
    ROLE_IN_EVENT,
    ROMANISATION_METHOD,
    SCHOLASTIC_ACHIEVEMENT,
    SEX_VALUE,
    SOURCE_CALL_NUMBER,
    SOURCE_DESCRIPTIVE_TITLE,
    SOURCE_FILED_BY_ENTRY,
    SOURCE_JURISDICTION_PLACE,
    SOURCE_MEDIA_TYPE,
    SOURCE_ORIGINATOR,
    SOURCE_PUBLICATION_FACTS,
    SUBMITTER_NAME,
    SYSTEM_ID,
    TEXT,
    TEXT_FROM_SOURCE,
    TIME_VALUE,
    USER_REFERENCE_NUMBER,
    USER_REFERENCE_TYPE,
    USER_TEXT,
    WHERE_WITHIN_SOURCE,
    XREF_FAM,
    XREF_INDI,
    XREF_NOTE,
    XREF_OBJE,
    XREF_REPO,
    XREF_SOUR,
    XREF_SUBM,
    YEAR,
    Y,
)


class MULTIMEDIA_LINK(Substructure, delta_level=0):
    class OBJE(XREF_OBJE, Substructure, delta_level=0):
        pass


class NOTE_STRUCTUREs(Substructure, delta_level=0):
    class NOTE_STRUCTURE(Substructure, delta_level=0):
        pass

    class NOTE_STRUCTURE_USER_TEXT(NOTE_STRUCTURE, Option, Substructure, delta_level=-1):
        class NOTE(USER_TEXT, Substructure, delta_level=0):
            pass

    class NOTE_STRUCTURE_XREF_NOTE(NOTE_STRUCTURE, Option, Substructure, delta_level=-1):
        class NOTE(XREF_NOTE, Substructure, delta_level=0):
            pass


class CHANGE_DATE(Substructure, delta_level=0):
    class CHAN(Tag, Substructure, delta_level=0):
        class DATE(DATE_EXACT, Substructure, delta_level=1):
            class TIME(TIME_VALUE, Substructure, delta_level=1):
                pass

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]


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
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]

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

    class PHON(PHONE_NUMBER, Substructure, delta_level=-1):
        pass

    PHONs = Iterable[PHON]

    # TODO: move outside?
    class EMAIL(ADDRESS_EMAIL, Substructure, delta_level=-1):
        pass

    EMAILs = Iterable[EMAIL]

    # TODO: move outside?
    class FAX(ADDRESS_FAX, Substructure, delta_level=-1):
        pass

    FAXs = Iterable[FAX]

    # TODO: move outside?
    class WWW(ADDRESS_WEB_PAGE, Substructure, delta_level=-1):
        pass

    WWWs = Iterable[WWW]


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

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]


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

    NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]
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

    NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]
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

    class EVEN(INDIVIDUAL_EVENT_STRUCTURE, Option, EVENT_DESCRIPTOR, NULL, Substructure, delta_level=0):
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

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]


class SPOUSE_TO_FAMILY_LINK(Substructure, delta_level=0):
    class FAMS(XREF_FAM, Substructure, delta_level=0):
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]


class ASSOCIATION_STRUCTURE(Substructure, delta_level=0):
    class ASSO(XREF_INDI, Substructure, delta_level=0):
        class RELA(RELATION_IS_DESCRIPTOR, Substructure, delta_level=1):
            pass

        SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]


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
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]
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
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]
            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]

    class MULTIMEDIA_RECORD(LINEAGE_LINKED_RECORD, Option, Substructure, delta_level=0):
        class OBJE(XREF_OBJE, Pointer, Substructure, delta_level=0):
            class FILE(MULTIMEDIA_FILE_REFERENCE, Substructure, delta_level=1):
                class FORM(MULTIMEDIA_FORMAT, Substructure, delta_level=1):
                    class TYPE(SOURCE_MEDIA_TYPE, Substructure, delta_level=1):
                        pass

                class TITL(DESCRIPTIVE_TITLE, Substructure, delta_level=1):
                    pass

            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
                pass

            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]
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
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]
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

                NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]

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
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]
            MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]


class SUBMITTER_RECORD(Substructure, delta_level=0):
    class SUBM(XREF_SUBM, Pointer, Substructure, delta_level=0):
        class NAME(SUBMITTER_NAME, Substructure, delta_level=1):
            pass

        ADDRESS_STRUCTURE = ADDRESS_STRUCTURE
        MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]

        class RIN(AUTOMATED_RECORD_ID, Substructure, delta_level=1):
            pass

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTUREs.NOTE_STRUCTURE]
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
    "ADDRESS_STRUCTURE",
    "ASSOCIATION_STRUCTURE",
    "CHANGE_DATE",
    "CHIL",
    "CHILD_TO_FAMILY_LINK",
    "EVENs",
    "EVENT_DETAIL",
    "FAMILY_EVENT_DETAIL",
    "FAMILY_EVENT_STRUCTUREs",
    "FORM_RECORDS",
    "GEDCOM_FORM_HEADER_EXTENSIONs",
    "GEDCOM_HEADER",
    "GEDCOM_TRAILER",
    "INDIVIDUAL_ATTRIBUTE_STRUCTUREs",
    "INDIVIDUAL_EVENT_DETAIL",
    "INDIVIDUAL_EVENT_STRUCTUREs",
    "LINEAGE_LINKED_GEDCOM_FILE",
    "LINEAGE_LINKED_RECORDs",
    "MULTIMEDIA_LINK",
    "NOTE_STRUCTUREs",
    "PERSONAL_NAME_PIECES",
    "PERSONAL_NAME_STRUCTURE",
    "PLACE_STRUCTURE",
    "REFN",
    "SOURCE_CITATION",
    "SOURCE_REPOSITORY_CITATION",
    "SPOUSE_TO_FAMILY_LINK",
    "SUBMITTER_RECORD",
    "TEXTs",
]
