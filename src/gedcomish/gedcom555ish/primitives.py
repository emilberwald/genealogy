from ..common import XREF_ID, Primitive, get_gedcom_date


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

class Y(Primitive, Size=(1, 1)):
    pass

class YEAR(Primitive, Size=(3, 4)):
    pass

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
    "Y",
    "YEAR",
]

