import pathlib
import tempfile
import contextlib
import inspect

from gedcomish.common import GEDCOM_LINES

from gedcomish.gedcom555ish.lineage_linked_gedcom_file import (
    ADDRESS_CITY,
    ADDRESS_COUNTRY,
    ADDRESS_EMAIL,
    ADDRESS_FAX,
    ADDRESS_LINE1,
    ADDRESS_LINE2,
    ADDRESS_LINE3,
    ADDRESS_POSTAL_CODE,
    ADDRESS_STATE,
    ADDRESS_STRUCTURE,
    ADDRESS_WEB_PAGE,
    ADOPTED_BY_WHICH_PARENT,
    AGE_AT_EVENT,
    ASSOCIATION_STRUCTURE,
    ATTRIBUTE_DESCRIPTOR,
    ATTRIBUTE_TYPE,
    AUTOMATED_RECORD_ID,
    BEFORE_COMMON_ERA,
    CASTE_NAME,
    CAUSE_OF_EVENT,
    CERTAINTY_ASSESSMENT,
    CHANGE_DATE,
    CHARACTER_ENCODING,
    CHILD_TO_FAMILY_LINK,
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
    EVENT_DETAIL,
    EVENT_OR_FACT_CLASSIFICATION,
    EVENT_TYPE_CITED_FROM,
    EVENT_TYPE_FAMILY,
    EVENT_TYPE_INDIVIDUAL,
    EVENTS_RECORDED,
    FAMILY_EVENT_DETAIL,
    FAMILY_EVENT_STRUCTUREs,
    FILE_CREATION_DATE,
    FORM_RECORDS,
    GEDCOM_CONTENT_DESCRIPTION,
    GEDCOM_FILE_NAME,
    GEDCOM_FORM,
    GEDCOM_FORM_HEADER_EXTENSION,
    GEDCOM_HEADER,
    GEDCOM_TRAILER,
    GEDCOM_VERSION_NUMBER,
    ID_NUMBER,
    INDIVIDUAL_ATTRIBUTE_STRUCTUREs,
    INDIVIDUAL_EVENT_DETAIL,
    INDIVIDUAL_EVENT_STRUCTUREs,
    LANGUAGE_ID,
    LANGUAGE_OF_TEXT,
    LINEAGE_LINKED_GEDCOM_FILE,
    LINEAGE_LINKED_RECORDs,
    MONTH,
    MONTH_FREN,
    MONTH_HEBR,
    MULTIMEDIA_FILE_REFERENCE,
    MULTIMEDIA_FORMAT,
    MULTIMEDIA_LINK,
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
    NOTE_STRUCTURE,
    NULL,
    NUMBER,
    NUMBER_OF_RELATIONSHIPS,
    OCCUPATION,
    PEDIGREE_LINKAGE_TYPE,
    PERSONAL_NAME_PIECES,
    PERSONAL_NAME_STRUCTURE,
    PHONE_NUMBER,
    PHONETISATION_METHOD,
    PHYSICAL_DESCRIPTION,
    PLACE_LATITUDE,
    PLACE_LONGITUDE,
    PLACE_NAME,
    PLACE_PHONETIC,
    PLACE_ROMANISED,
    PLACE_STRUCTURE,
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
    SOURCE_CITATION,
    SOURCE_DESCRIPTIVE_TITLE,
    SOURCE_FILED_BY_ENTRY,
    SOURCE_JURISDICTION_PLACE,
    SOURCE_MEDIA_TYPE,
    SOURCE_ORIGINATOR,
    SOURCE_PUBLICATION_FACTS,
    SOURCE_REPOSITORY_CITATION,
    SPOUSE_TO_FAMILY_LINK,
    SUBMITTER_NAME,
    SUBMITTER_RECORD,
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
)


@contextlib.contextmanager
def NamedTemporaryFile(*args, **kwargs):
    f = tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)
    try:
        yield f
    finally:
        pathlib.Path(f.name).unlink()


class TestExampleFiles:
    def test_minimal555(self):
        minimal555 = LINEAGE_LINKED_GEDCOM_FILE()
        minimal555.GEDCOM_HEADER = GEDCOM_HEADER()
        minimal555.GEDCOM_HEADER.HEAD = GEDCOM_HEADER.HEAD()
        minimal555.GEDCOM_HEADER.HEAD.GEDC = GEDCOM_HEADER.HEAD.GEDC()
        minimal555.GEDCOM_HEADER.HEAD.GEDC.VERS = GEDCOM_HEADER.HEAD.GEDC.VERS("5.5.5")
        minimal555.GEDCOM_HEADER.HEAD.GEDC.FORM = GEDCOM_HEADER.HEAD.GEDC.FORM("LINEAGE-LINKED")
        minimal555.GEDCOM_HEADER.HEAD.GEDC.FORM.VERS = GEDCOM_HEADER.HEAD.GEDC.FORM.VERS("5.5.5")
        minimal555.GEDCOM_HEADER.HEAD.CHAR = GEDCOM_HEADER.HEAD.CHAR("UTF-8")
        minimal555.GEDCOM_FORM_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSION()
        minimal555.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION = (
            GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION()
        )
        minimal555.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR(
            "gedcom.org"
        )
        minimal555.FORM_RECORDS = FORM_RECORDS()
        minimal555.FORM_RECORDS.SUBMITTER_RECORD = SUBMITTER_RECORD()
        minimal555.FORM_RECORDS.SUBMITTER_RECORD.SUBM = SUBMITTER_RECORD.SUBM("U")
        minimal555.FORM_RECORDS.SUBMITTER_RECORD.SUBM.NAME = SUBMITTER_RECORD.SUBM.NAME("gedcom.org")
        minimal555.GEDCOM_TRAILER = GEDCOM_TRAILER()
        minimal555.GEDCOM_TRAILER.TRLR = GEDCOM_TRAILER.TRLR()
        lines = GEDCOM_LINES()
        lines = minimal555(lines)
        result = lines(0)
        print(result)
        with NamedTemporaryFile(suffix=".ged") as fp:
            fp.close()
            file = pathlib.Path(fp.name)
            file.write_text(result, encoding="utf-8-sig")
            actual = file.read_text()
            expected = (
                pathlib.Path(inspect.getframeinfo(inspect.currentframe()).filename).resolve().parent
                / pathlib.Path("MINIMAL555.GED")
            ).read_text()
            assert actual == expected

    def test_555sample(self):
        ex = LINEAGE_LINKED_GEDCOM_FILE()
        ex.GEDCOM_HEADER = GEDCOM_HEADER()
        ex.GEDCOM_HEADER.HEAD = GEDCOM_HEADER.HEAD()
        ex.GEDCOM_HEADER.HEAD.GEDC = GEDCOM_HEADER.HEAD.GEDC()
        ex.GEDCOM_HEADER.HEAD.GEDC.VERS = GEDCOM_HEADER.HEAD.GEDC.VERS("5.5.5")
        ex.GEDCOM_HEADER.HEAD.GEDC.FORM = GEDCOM_HEADER.HEAD.GEDC.FORM("LINEAGE-LINKED")
        ex.GEDCOM_HEADER.HEAD.GEDC.FORM.VERS = GEDCOM_HEADER.HEAD.GEDC.FORM.VERS("5.5.5")
        ex.GEDCOM_HEADER.HEAD.CHAR = GEDCOM_HEADER.HEAD.CHAR("UTF-8")
        ex.GEDCOM_FORM_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSION()
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR(
            "GS"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR = (
            GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR()
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.NAME = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.NAME(
            "GEDCOM Specification"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.VERS = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.VERS(
            "5.5.5"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.CORP = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.CORP(
            "gedcom.org"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE = (
            ADDRESS_STRUCTURE()
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE.ADDR = (
            ADDRESS_STRUCTURE.ADDR()
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE.ADDR.CITY = ADDRESS_STRUCTURE.ADDR.CITY(
            "LEIDEN"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE.WWW = ADDRESS_STRUCTURE.WWW(
            "www.gedcom.org"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.DATE = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.DATE("2 Oct 2019")
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.DATE.TIME = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.DATE.TIME("0:00:00")
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.FILE = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.FILE("555Sample.ged")
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.LANG = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.LANG("English")
        ex.GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SUBM = GEDCOM_FORM_HEADER_EXTENSION.LINEAGE_LINKED_HEADER_EXTENSION.SUBM("U1")

        ex.FORM_RECORDS = FORM_RECORDS()
        ex.FORM_RECORDS.SUBMITTER_RECORD = SUBMITTER_RECORD()
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM = SUBMITTER_RECORD.SUBM("U1")
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.NAME = SUBMITTER_RECORD.SUBM.NAME("Reldon Poulson")
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE = ADDRESS_STRUCTURE()
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE.ADDR = ADDRESS_STRUCTURE.ADDR()
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE.ADDR.ADR1 = ADDRESS_STRUCTURE.ADDR.ADR1(
            "1900 43rd Street West"
        )
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE.ADDR.CITY = ADDRESS_STRUCTURE.ADDR.CITY("Billings")
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE.ADDR.STAE = ADDRESS_STRUCTURE.ADDR.STAE("Montana")
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE.ADDR.POST = ADDRESS_STRUCTURE.ADDR.POST("68051")
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE.ADDR.CTRY = ADDRESS_STRUCTURE.ADDR.CTRY(
            "United States of America"
        )
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE.PHON = ADDRESS_STRUCTURE.PHON("+1 (406) 555-1232")

        ########################################################################
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs: List[LINEAGE_LINKED_RECORDs.LINEAGE_LINKED_RECORD] = list()
        ########################################################################
        indi = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD()
        indi.INDI = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI("I1")
        indi.INDI.PERSONAL_NAME_STRUCTUREs = list()
        name = PERSONAL_NAME_STRUCTURE()
        name.NAME = PERSONAL_NAME_STRUCTURE.NAME("Robert Eugene /Williams/")
        name.NAME.PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES()
        name.NAME.PERSONAL_NAME_PIECES.SURN = PERSONAL_NAME_PIECES.SURN("Williams")
        name.NAME.PERSONAL_NAME_PIECES.GIVN = PERSONAL_NAME_PIECES.GIVN("Robert Eugene")
        indi.INDI.PERSONAL_NAME_STRUCTUREs.append(name)

        indi.INDI.SEX = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI.SEX("M")

        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()

        birth = INDIVIDUAL_EVENT_STRUCTUREs.BIRT()
        birth.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("2 oct 1822")
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Weston, Madison, Connecticut, United States of America"
        )
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.SOURCE_CITATION = SOURCE_CITATION()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.SOURCE_CITATION.SOUR = SOURCE_CITATION.SOUR("S1")
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.SOURCE_CITATION.SOUR.PAGE = SOURCE_CITATION.SOUR.PAGE(
            "Sec. 2, p. 45"
        )
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(birth)

        death = INDIVIDUAL_EVENT_STRUCTUREs.DEAT()
        death.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("from 1900 to 1905")
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(death)

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(indi)
        ########################################################################
        indi = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD()
        indi.INDI = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI("I2")

        indi.INDI.PERSONAL_NAME_STRUCTUREs = list()
        name = PERSONAL_NAME_STRUCTURE()
        name.NAME = PERSONAL_NAME_STRUCTURE.NAME("Mary Ann /Wilson/")
        name.NAME.PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES()
        name.NAME.PERSONAL_NAME_PIECES.SURN = PERSONAL_NAME_PIECES.SURN("Wilson")
        name.NAME.PERSONAL_NAME_PIECES.GIVN = PERSONAL_NAME_PIECES.GIVN("Mary Ann")
        indi.INDI.PERSONAL_NAME_STRUCTUREs.append(name)

        indi.INDI.SEX = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI.SEX("F")

        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()

        birth = INDIVIDUAL_EVENT_STRUCTUREs.BIRT()
        birth.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("BEF 1828")
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Connecticut, United States of America"
        )
        birth.FAMC = INDIVIDUAL_EVENT_STRUCTUREs.BIRT.FAMC("F1")
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(birth)

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(indi)
        ########################################################################
        indi = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD()
        indi.INDI = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI("I3")

        indi.INDI.PERSONAL_NAME_STRUCTUREs = list()

        name = PERSONAL_NAME_STRUCTURE()
        name.NAME = PERSONAL_NAME_STRUCTURE.NAME("Joe /Williams/")
        name.NAME.PERSONAL_NAME_PIECES = PERSONAL_NAME_PIECES()
        name.NAME.PERSONAL_NAME_PIECES.SURN = PERSONAL_NAME_PIECES.SURN("Williams")
        name.NAME.PERSONAL_NAME_PIECES.GIVN = PERSONAL_NAME_PIECES.GIVN("Joe")
        indi.INDI.PERSONAL_NAME_STRUCTUREs.append(name)

        indi.INDI.SEX = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI.SEX("M")

        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list()

        birth = INDIVIDUAL_EVENT_STRUCTUREs.BIRT()
        birth.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("11 jun 1861")
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Idaho Falls, Bonneville, Idaho, United States of America"
        )
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(birth)

        adoption = INDIVIDUAL_EVENT_STRUCTUREs.ADOP()
        adoption.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        adoption.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        adoption.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("16 Mar 1864")
        adoption.FAMC = INDIVIDUAL_EVENT_STRUCTUREs.ADOP.FAMC()
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(adoption)

        indi.INDI.CHILD_TO_FAMILY_LINKs = list()

        child_to_family_link = CHILD_TO_FAMILY_LINK()
        child_to_family_link.FAMC = CHILD_TO_FAMILY_LINK.FAMC("F1")
        indi.INDI.CHILD_TO_FAMILY_LINKs.append(child_to_family_link)

        child_to_family_link = CHILD_TO_FAMILY_LINK()
        child_to_family_link.FAMC = CHILD_TO_FAMILY_LINK.FAMC("F2")
        child_to_family_link.FAMC.PEDI = CHILD_TO_FAMILY_LINK.FAMC.PEDI("adopted")
        indi.INDI.CHILD_TO_FAMILY_LINKs.append(child_to_family_link)

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(indi)
        ########################################################################
        fam = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
        fam.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM("F1")
        fam.FAM.HUSB = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.HUSB("I1")
        fam.FAM.WIFE = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.HUSB("I2")
        fam.FAM.CHIL = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.CHIL("I3")
        fam.FAM.FAMILY_EVENT_STRUCTURE = FAMILY_EVENT_STRUCTUREs()
        fam.FAM.FAMILY_EVENT_STRUCTURE.MARR = FAMILY_EVENT_STRUCTUREs.MARR()
        fam.FAM.FAMILY_EVENT_STRUCTURE.MARR.FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL()
        fam.FAM.FAMILY_EVENT_STRUCTURE.MARR.FAMILY_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        fam.FAM.FAMILY_EVENT_STRUCTURE.MARR.FAMILY_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("Dec 1859")
        fam.FAM.FAMILY_EVENT_STRUCTURE.MARR.FAMILY_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        fam.FAM.FAMILY_EVENT_STRUCTURE.MARR.FAMILY_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Rapid City, Pennington, South Dakota, United States of America"
        )

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(fam)
        ########################################################################
        fam = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
        fam.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM("F2")
        fam.FAM.HUSB = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.HUSB("I1")
        fam.FAM.CHIL = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.CHIL("I3")

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(fam)
        ########################################################################
        sour = LINEAGE_LINKED_RECORDs.SOURCE_RECORD()
        sour.SOUR = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR("S1")
        sour.SOUR.DATA = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA()
        sour.SOUR.DATA.EVEN = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA.EVEN("BIRT, DEAT, MARR")
        sour.SOUR.DATA.EVEN.DATE = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA.EVEN.DATE("FROM Jan 1820 TO Dec 1825")
        sour.SOUR.DATA.EVEN.PLAC = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA.EVEN.PLAC(
            "Madison, Connecticut, United States of America"
        )
        sour.SOUR.DATA.AGNC = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA.AGNC("Madison County Court")
        sour.SOUR.TITL = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.TITL(
            "Madison County Birth, Death and Marriage Records"
        )
        sour.SOUR.ABBR = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.ABBR("Madison BMD Records")

        sour.SOUR.SOURCE_REPOSITORY_CITATIONs = list()

        citation = SOURCE_REPOSITORY_CITATION()
        citation.REPO = SOURCE_REPOSITORY_CITATION.REPO("R1")
        citation.REPO.CALN = SOURCE_REPOSITORY_CITATION.REPO.CALN("138-1234.01")
        sour.SOUR.SOURCE_REPOSITORY_CITATIONs.append(citation)

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(sour)
        ########################################################################
        repo = LINEAGE_LINKED_RECORDs.REPOSITORY_RECORD()
        repo.REPO = LINEAGE_LINKED_RECORDs.REPOSITORY_RECORD.REPO("R1")
        repo.REPO.NAME = LINEAGE_LINKED_RECORDs.REPOSITORY_RECORD.REPO.NAME("Family History Library")
        repo.REPO.ADDRESS_STRUCTURE = ADDRESS_STRUCTURE()
        repo.REPO.ADDRESS_STRUCTURE.ADDR = ADDRESS_STRUCTURE.ADDR()
        repo.REPO.ADDRESS_STRUCTURE.ADDR.ADR1 = ADDRESS_STRUCTURE.ADDR.ADR1("35 N West Temple Street")
        repo.REPO.ADDRESS_STRUCTURE.ADDR.CITY = ADDRESS_STRUCTURE.ADDR.CITY("Salt Lake City")
        repo.REPO.ADDRESS_STRUCTURE.ADDR.STAE = ADDRESS_STRUCTURE.ADDR.STAE("Utah")
        repo.REPO.ADDRESS_STRUCTURE.ADDR.POST = ADDRESS_STRUCTURE.ADDR.POST("84150")
        repo.REPO.ADDRESS_STRUCTURE.ADDR.CTRY = ADDRESS_STRUCTURE.ADDR.CTRY("United States of America")

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(repo)
        ########################################################################

        ex.GEDCOM_TRAILER = GEDCOM_TRAILER()
        ex.GEDCOM_TRAILER.TRLR = GEDCOM_TRAILER.TRLR()

        lines = GEDCOM_LINES()
        lines = ex(lines)
        result = lines(0)
        print(result)
        with NamedTemporaryFile(suffix=".ged") as fp:
            fp.close()
            file = pathlib.Path(fp.name)
            file.write_text(result, encoding="utf-8-sig")
            actual = file.read_text()
            expected = (
                pathlib.Path(inspect.getframeinfo(inspect.currentframe()).filename).resolve().parent
                / pathlib.Path("555SAMPLE.GED")
            ).read_text()
            assert actual == expected

