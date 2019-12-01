from ..common import XREF_ID, Meta, Primitive, Tag, Pointer, Substructure, get_gedcom_date
from typing import Iterable


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


class ATTRIBUTE_TYPE(Primitive, metaclass=Meta, Size=(4, 4)):
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


class DATE_APPROXIMATED(Primitive, metaclass=Meta, Size=(8, 39)):
    pass


class DATE_CALENDAR_ESCAPE(Primitive, metaclass=Meta, Size=(4, 15)):
    pass


class DATE_CALENDAR(Primitive, metaclass=Meta, Size=(4, 35)):
    pass


class DATE_EXACT(Primitive, metaclass=Meta, Size=(10, 11)):
    pass


class DATE_FREN(Primitive, metaclass=Meta, Size=(4, 35)):
    pass


class DATE_GREG(Primitive, metaclass=Meta, Size=(4, 35)):
    pass


class DATE_HEBR(Primitive, metaclass=Meta, Size=(4, 35)):
    pass


class DATE_JULN(Primitive, metaclass=Meta, Size=(4, 35)):
    pass


class DATE_PERIOD(Primitive, metaclass=Meta, Size=(7, 35)):
    pass


class DATE_PHRASE(Primitive, metaclass=Meta, Size=(1, 35)):
    pass


class DATE_RANGE(Primitive, metaclass=Meta, Size=(8, 35)):
    pass


class DATE_VALUE(Primitive, metaclass=Meta, Size=(1, 35)):
    @staticmethod
    def date(date_phrase: str):
        return get_gedcom_date(date_phrase)


class DATE(Primitive, metaclass=Meta, Size=(4, 35)):
    pass


class DAY(Primitive, metaclass=Meta, Size=(1, 2)):
    pass


class DESCRIPTIVE_TITLE(Primitive, metaclass=Meta, Size=(1, 248)):
    pass


class DIGIT(Primitive, metaclass=Meta, Size=(1, 1)):
    pass


class DUAL_STYLE_YEAR(Primitive, metaclass=Meta, Size=(3, 7)):
    pass


class ENTRY_RECORDING_DATE(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class EVENT_ATTRIBUTE_TYPE(Primitive, metaclass=Meta, Size=(1, 15)):
    pass


class EVENT_DESCRIPTOR(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class EVENT_OR_FACT_CLASSIFICATION(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class EVENT_TYPE_CITED_FROM(Primitive, metaclass=Meta, Size=(1, 15)):
    pass


class EVENT_TYPE_FAMILY(Primitive, metaclass=Meta, Size=(3, 4)):
    pass


class EVENT_TYPE_INDIVIDUAL(Primitive, metaclass=Meta, Size=(3, 4)):
    pass


class EVENTS_RECORDED(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class FILE_CREATION_DATE(Primitive, metaclass=Meta, Size=(10, 11)):
    pass


class GEDCOM_CONTENT_DESCRIPTION(Primitive, metaclass=Meta, Size=(1, 248)):
    pass


class GEDCOM_FILE_NAME(Primitive, metaclass=Meta, Size=(5, 248)):
    pass


class GEDCOM_FORM(Primitive, metaclass=Meta, Size=(14, 20)):  # Size=(1,20)
    pass


class GEDCOM_VERSION_NUMBER(Primitive, metaclass=Meta, Size=(3, 11)):
    pass


class ID_NUMBER(Primitive, metaclass=Meta, Size=(1, 30)):
    pass


class LANGUAGE_ID(Primitive, metaclass=Meta, Size=(1, 15)):
    pass


class LANGUAGE_OF_TEXT(Primitive, metaclass=Meta, Size=(1, 15)):
    pass


class MONTH_FREN(Primitive, metaclass=Meta, Size=4):
    pass


class MONTH_HEBR(Primitive, metaclass=Meta, Size=3):
    pass


class MONTH(Primitive, metaclass=Meta, Size=3):
    pass


class MULTIMEDIA_FILE_REFERENCE(Primitive, metaclass=Meta, Size=(1, 259)):
    pass


class MULTIMEDIA_FORMAT(Primitive, metaclass=Meta, Size=(3, 4)):
    pass


class NAME_OF_BUSINESS(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class NAME_OF_PRODUCT(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class NAME_OF_REPOSITORY(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class NAME_OF_SOURCE_DATA(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class NAME_PERSONAL(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class NAME_PHONETIC(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class NAME_PIECE_GIVEN(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class NAME_PIECE_NICKNAME(Primitive, metaclass=Meta, Size=(1, 30)):
    pass


class NAME_PIECE_PREFIX(Primitive, metaclass=Meta, Size=(1, 30)):
    pass


class NAME_PIECE_SUFFIX(Primitive, metaclass=Meta, Size=(1, 30)):
    pass


class NAME_PIECE_SURNAME_PREFIX(Primitive, metaclass=Meta, Size=(1, 30)):
    pass


class NAME_PIECE_SURNAME(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class NAME_PIECE(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class NAME_ROMANISED(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class NAME_TEXT(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class NAME_TYPE(Primitive, metaclass=Meta, Size=(5, 30)):
    pass


class NATIONAL_OR_TRIBAL_ORIGIN(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class NOBILITY_TYPE_TITLE(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class NULL(Primitive, metaclass=Meta, Size=(0, 0)):
    pass


class NUMBER_OF_RELATIONSHIPS(Primitive, metaclass=Meta, Size=(1, 3)):
    pass


class NUMBER(Primitive, metaclass=Meta, Size=(3, 4)):
    pass


class OCCUPATION(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class PEDIGREE_LINKAGE_TYPE(Primitive, metaclass=Meta, Size=(5, 7)):
    pass


class PHONE_NUMBER(Primitive, metaclass=Meta, Size=(1, 25)):
    pass


class PHONETISATION_METHOD(Primitive, metaclass=Meta, Size=(5, 30)):
    pass


class PHYSICAL_DESCRIPTION(Primitive, metaclass=Meta, Size=(1, 4095)):
    pass


class PLACE_LATITUDE(Primitive, metaclass=Meta, Size=(2, 10)):
    pass


class PLACE_LONGITUDE(Primitive, metaclass=Meta, Size=(2, 11)):
    pass


class PLACE_NAME(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class PLACE_PHONETIC(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class PLACE_ROMANISED(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class PLACE_TEXT(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class POSSESSIONS(Primitive, metaclass=Meta, Size=(1, 248)):
    pass


class PRODUCT_VERSION_NUMBER(Primitive, metaclass=Meta, Size=(3, 15)):
    pass


class PUBLICATION_DATE(Primitive, metaclass=Meta, Size=(10, 11)):
    pass


class RECEIVING_SYSTEM_NAME(Primitive, metaclass=Meta, Size=(1, 20)):
    pass


class RELATION_IS_DESCRIPTOR(Primitive, metaclass=Meta, Size=(1, 25)):
    pass


class RELIGIOUS_AFFILIATION(Primitive, metaclass=Meta, Size=(1, 90)):
    pass


class RESPONSIBLE_AGENCY(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class ROLE_DESCRIPTOR(Primitive, metaclass=Meta, Size=(1, 25)):
    pass


class ROLE_IN_EVENT(Primitive, metaclass=Meta, Size=(3, 27)):
    pass


class ROMANISATION_METHOD(Primitive, metaclass=Meta, Size=(5, 30)):
    pass


class SCHOLASTIC_ACHIEVEMENT(Primitive, metaclass=Meta, Size=(1, 248)):
    pass


class SEX_VALUE(Primitive, metaclass=Meta, Size=(1, 1)):
    pass


class SOURCE_CALL_NUMBER(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class SOURCE_DESCRIPTIVE_TITLE(Primitive, metaclass=Meta, Size=(1, 4095)):
    pass


class SOURCE_FILED_BY_ENTRY(Primitive, metaclass=Meta, Size=(1, 60)):
    pass


class SOURCE_JURISDICTION_PLACE(Primitive, metaclass=Meta, Size=(1, 120)):
    pass


class SOURCE_MEDIA_TYPE(Primitive, metaclass=Meta, Size=(1, 15)):
    pass


class SOURCE_ORIGINATOR(Primitive, metaclass=Meta, Size=(1, 255)):
    pass


class SOURCE_PUBLICATION_FACTS(Primitive, metaclass=Meta, Size=(1, 4095)):
    pass


class SUBMITTER_NAME(Primitive, metaclass=Meta, Size=(1, 60)):
    pass


class SYSTEM_ID(Primitive, metaclass=Meta, Size=(1, 20)):
    pass


class TEXT_FROM_SOURCE(Primitive, metaclass=Meta, Size=(1, 32767)):
    pass


class TEXT(Primitive, metaclass=Meta, Size=(1, 32767)):
    pass


class TIME_VALUE(Primitive, metaclass=Meta, Size=(7, 12)):
    pass


class USER_REFERENCE_NUMBER(Primitive, metaclass=Meta, Size=(1, 20)):
    pass


class USER_REFERENCE_TYPE(Primitive, metaclass=Meta, Size=(1, 40)):
    pass


class USER_TEXT(Primitive, metaclass=Meta, Size=(1, 32767)):
    pass


class WHERE_WITHIN_SOURCE(Primitive, metaclass=Meta, Size=(1, 248)):
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


class YEAR(Primitive, metaclass=Meta, Size=(3, 4)):
    pass


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

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


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

            TEXTs = Iterable[TEXT]

        MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]

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

        FONEs = Iterable[FONE]

        class ROMN(PLACE_ROMANISED, Substructure):
            class TYPE(ROMANISATION_METHOD, Substructure):
                pass

        ROMNs = Iterable[ROMN]

        class MAP(Tag, Substructure):
            class LATI(PLACE_LATITUDE, Substructure):
                pass

            class LONG(PLACE_LONGITUDE, Substructure):
                pass

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


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

    NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
    SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
    MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]


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

    NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
    SOURCE_CITATIONs = Iterable[SOURCE_CITATION]


class PERSONAL_NAME_STRUCTURE(Substructure):
    class NAME(NAME_PERSONAL, Substructure):
        class TYPE(NAME_TYPE, Substructure):
            pass

        PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES

        class FONE(NAME_PHONETIC, Substructure):
            class TYPE(PHONETISATION_METHOD, Substructure):
                pass

            PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES

        FONEs = Iterable[FONE]

        class ROMN(NAME_ROMANISED, Substructure):
            class TYPE(ROMANISATION_METHOD, Substructure):
                pass

            PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES

        ROMNs = Iterable[ROMN]


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

    class NMR(NUMBER_OF_RELATIONSHIPS, INDIVIDUAL_ATTRIBUTE_STRUCTURE, Substructure):
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

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


class SPOUSE_TO_FAMILY_LINK(Substructure):
    class FAMS(XREF_FAM, Substructure):
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


class ASSOCIATION_STRUCTURE(Substructure):
    class ASSO(XREF_INDI, Substructure):
        class RELA(RELATION_IS_DESCRIPTOR, Substructure):
            pass

        SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]


class SOURCE_REPOSITORY_CITATION(Substructure):
    class REPO(XREF_REPO, Substructure):
        class CALN(SOURCE_CALL_NUMBER, Substructure):
            class MEDI(SOURCE_MEDIA_TYPE, Substructure):
                pass


class REFN(USER_REFERENCE_NUMBER, Substructure):
    class TYPE(USER_REFERENCE_TYPE, Substructure):
        pass


class LINEAGE_LINKED_RECORDs(Substructure):
    class LINEAGE_LINKED_RECORD(Substructure):
        pass

    class FAM_GROUP_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class FAM(XREF_FAM, Pointer, Substructure):
            FAMILY_EVENT_STRUCTUREs = Iterable[FAMILY_EVENT_STRUCTUREs.FAMILY_EVENT_STRUCTURE]

            class HUSB(XREF_INDI, Substructure):
                pass

            class WIFE(XREF_INDI, Substructure):
                pass

            class CHIL(XREF_INDI, Substructure):
                pass

            CHILs = Iterable[CHIL]

            class NCHI(COUNT_OF_CHILDREN, Substructure):
                pass

            REFNs = Iterable[REFN]

            class TYPE(USER_REFERENCE_TYPE, Substructure):
                pass

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]

    class INDIVIDUAL_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class INDI(XREF_INDI, Pointer, Substructure):
            PERSONAL_NAME_STRUCTUREs = Iterable[PERSONAL_NAME_STRUCTURE]

            class SEX(SEX_VALUE, Substructure):
                pass

            INDIVIDUAL_EVENT_STRUCTUREs = Iterable[INDIVIDUAL_EVENT_STRUCTUREs.INDIVIDUAL_EVENT_STRUCTURE]
            INDIVIDUAL_ATTRIBUTE_STRUCTUREs = Iterable[INDIVIDUAL_ATTRIBUTE_STRUCTUREs.INDIVIDUAL_ATTRIBUTE_STRUCTURE]
            CHILD_TO_FAMILY_LINKs = Iterable[CHILD_TO_FAMILY_LINK]
            SPOUSE_TO_FAMILY_LINKs = Iterable[SPOUSE_TO_FAMILY_LINK]
            ASSOCIATION_STRUCTUREs = Iterable[ASSOCIATION_STRUCTURE]

            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]

    class MULTIMEDIA_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class OBJE(XREF_OBJE, Pointer, Substructure):
            class FILE(MULTIMEDIA_FILE_REFERENCE, Substructure):
                class FORM(MULTIMEDIA_FORMAT, Substructure):
                    class TYPE(SOURCE_MEDIA_TYPE, Substructure):
                        pass

                class TITL(DESCRIPTIVE_TITLE, Substructure):
                    pass

            FILEs = Iterable[FILE]

            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            CHANGE_DATE = CHANGE_DATE

    class NOTE_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class NOTE(XREF_NOTE, USER_TEXT, Pointer, Substructure):
            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            SOURCE_CITATIONs = Iterable[SOURCE_CITATION]
            CHANGE_DATE = CHANGE_DATE

    class REPOSITORY_RECORD(LINEAGE_LINKED_RECORD, Substructure):
        class REPO(XREF_REPO, Pointer, Substructure):
            class NAME(NAME_OF_REPOSITORY, Substructure):
                pass

            ADDRESS_STRUCTURE = ADDRESS_STRUCTURE
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            REFNs = Iterable[REFN]

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

                EVENs = Iterable[EVEN]

                class AGNC(RESPONSIBLE_AGENCY, Substructure):
                    pass

                NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]

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

            SOURCE_REPOSITORY_CITATIONs = Iterable[SOURCE_REPOSITORY_CITATION]

            REFNs = Iterable[REFN]

            class RIN(AUTOMATED_RECORD_ID, Substructure):
                pass

            CHANGE_DATE = CHANGE_DATE
            NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
            MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]


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
        MULTIMEDIA_LINKs = Iterable[MULTIMEDIA_LINK]

        class RIN(AUTOMATED_RECORD_ID, Substructure):
            pass

        NOTE_STRUCTUREs = Iterable[NOTE_STRUCTURE]
        CHANGE_DATE = CHANGE_DATE


class GEDCOM_TRAILER(Substructure):
    class TRLR(Tag, Substructure):
        pass


class FORM_RECORDS(Substructure):
    SUBMITTER_RECORD = SUBMITTER_RECORD
    LINEAGE_LINKED_RECORDs = Iterable[LINEAGE_LINKED_RECORDs.LINEAGE_LINKED_RECORD]


class LINEAGE_LINKED_GEDCOM_FILE(Substructure):
    GEDCOM_HEADER = GEDCOM_HEADER
    GEDCOM_FORM_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSION
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
    "ADDRESS_STRUCTURE",
    "ADDRESS_WEB_PAGE",
    "ADOPTED_BY_WHICH_PARENT",
    "AGE_AT_EVENT",
    "ASSOCIATION_STRUCTURE",
    "ATTRIBUTE_DESCRIPTOR",
    "ATTRIBUTE_TYPE",
    "AUTOMATED_RECORD_ID",
    "BEFORE_COMMON_ERA",
    "CASTE_NAME",
    "CAUSE_OF_EVENT",
    "CERTAINTY_ASSESSMENT",
    "CHANGE_DATE",
    "CHARACTER_ENCODING",
    "CHILD_TO_FAMILY_LINK",
    "COPYRIGHT_GEDCOM_FILE",
    "COPYRIGHT_SOURCE_DATA",
    "COUNT_OF_CHILDREN",
    "DATE",
    "DATE_APPROXIMATED",
    "DATE_CALENDAR",
    "DATE_CALENDAR_ESCAPE",
    "DATE_EXACT",
    "DATE_FREN",
    "DATE_GREG",
    "DATE_HEBR",
    "DATE_JULN",
    "DATE_PERIOD",
    "DATE_PHRASE",
    "DATE_RANGE",
    "DATE_VALUE",
    "DAY",
    "DESCRIPTIVE_TITLE",
    "DIGIT",
    "DUAL_STYLE_YEAR",
    "ENTRY_RECORDING_DATE",
    "EVENT_ATTRIBUTE_TYPE",
    "EVENT_DESCRIPTOR",
    "EVENT_DETAIL",
    "EVENT_OR_FACT_CLASSIFICATION",
    "EVENT_TYPE_CITED_FROM",
    "EVENT_TYPE_FAMILY",
    "EVENT_TYPE_INDIVIDUAL",
    "EVENTS_RECORDED",
    "FAMILY_EVENT_DETAIL",
    "FAMILY_EVENT_STRUCTUREs",
    "FILE_CREATION_DATE",
    "FORM_RECORDS",
    "GEDCOM_CONTENT_DESCRIPTION",
    "GEDCOM_FILE_NAME",
    "GEDCOM_FORM",
    "GEDCOM_FORM_HEADER_EXTENSION",
    "GEDCOM_HEADER",
    "GEDCOM_TRAILER",
    "GEDCOM_VERSION_NUMBER",
    "ID_NUMBER",
    "INDIVIDUAL_ATTRIBUTE_STRUCTUREs",
    "INDIVIDUAL_EVENT_DETAIL",
    "INDIVIDUAL_EVENT_STRUCTUREs",
    "LANGUAGE_ID",
    "LANGUAGE_OF_TEXT",
    "LINEAGE_LINKED_GEDCOM_FILE",
    "LINEAGE_LINKED_RECORDs",
    "MONTH",
    "MONTH_FREN",
    "MONTH_HEBR",
    "MULTIMEDIA_FILE_REFERENCE",
    "MULTIMEDIA_FORMAT",
    "MULTIMEDIA_LINK",
    "NAME_OF_BUSINESS",
    "NAME_OF_PRODUCT",
    "NAME_OF_REPOSITORY",
    "NAME_OF_SOURCE_DATA",
    "NAME_PERSONAL",
    "NAME_PHONETIC",
    "NAME_PIECE",
    "NAME_PIECE_GIVEN",
    "NAME_PIECE_NICKNAME",
    "NAME_PIECE_PREFIX",
    "NAME_PIECE_SUFFIX",
    "NAME_PIECE_SURNAME",
    "NAME_PIECE_SURNAME_PREFIX",
    "NAME_ROMANISED",
    "NAME_TEXT",
    "NAME_TYPE",
    "NATIONAL_OR_TRIBAL_ORIGIN",
    "NOBILITY_TYPE_TITLE",
    "NOTE_STRUCTURE",
    "NULL",
    "NUMBER",
    "NUMBER_OF_RELATIONSHIPS",
    "OCCUPATION",
    "PEDIGREE_LINKAGE_TYPE",
    "PERSONAL_NAME_PIECES",
    "PERSONAL_NAME_STRUCTURE",
    "PHONE_NUMBER",
    "PHONETISATION_METHOD",
    "PHYSICAL_DESCRIPTION",
    "PLACE_LATITUDE",
    "PLACE_LONGITUDE",
    "PLACE_NAME",
    "PLACE_PHONETIC",
    "PLACE_ROMANISED",
    "PLACE_STRUCTURE",
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
    "SOURCE_CITATION",
    "SOURCE_DESCRIPTIVE_TITLE",
    "SOURCE_FILED_BY_ENTRY",
    "SOURCE_JURISDICTION_PLACE",
    "SOURCE_MEDIA_TYPE",
    "SOURCE_ORIGINATOR",
    "SOURCE_PUBLICATION_FACTS",
    "SOURCE_REPOSITORY_CITATION",
    "SPOUSE_TO_FAMILY_LINK",
    "SUBMITTER_NAME",
    "SUBMITTER_RECORD",
    "SYSTEM_ID",
    "TEXT",
    "TEXT_FROM_SOURCE",
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
]
