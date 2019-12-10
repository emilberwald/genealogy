import contextlib
import datetime
import inspect
import logging
import pathlib
import tempfile
from typing import List

import pytest

import gedcomish.configure
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
from gedcomish.gedcom555ish.primitives import *

gedcomish.configure.configure()
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def NamedTemporaryFile(*args, **kwargs):
    f = tempfile.NamedTemporaryFile(*args, delete=False, **kwargs)
    try:
        yield f
    finally:
        pathlib.Path(f.name).unlink()


class TestExampleFiles:
    def get_minimal555(self):
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
            "gedcom.org"
        )
        ex.FORM_RECORDS = FORM_RECORDS()
        ex.FORM_RECORDS.SUBMITTER_RECORD = SUBMITTER_RECORD()
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM = SUBMITTER_RECORD.SUBM(XREF_SUBM("U"))
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.NAME = SUBMITTER_RECORD.SUBM.NAME("gedcom.org")
        ex.GEDCOM_TRAILER = GEDCOM_TRAILER()
        ex.GEDCOM_TRAILER.TRLR = GEDCOM_TRAILER.TRLR()
        return ex

    def get_555sample(self):
        ex = LINEAGE_LINKED_GEDCOM_FILE()
        ex.GEDCOM_HEADER = GEDCOM_HEADER()
        ex.GEDCOM_HEADER.HEAD = GEDCOM_HEADER.HEAD()
        ex.GEDCOM_HEADER.HEAD.GEDC = GEDCOM_HEADER.HEAD.GEDC()
        ex.GEDCOM_HEADER.HEAD.GEDC.VERS = GEDCOM_HEADER.HEAD.GEDC.VERS("5.5.5")
        ex.GEDCOM_HEADER.HEAD.GEDC.FORM = GEDCOM_HEADER.HEAD.GEDC.FORM("LINEAGE-LINKED")
        ex.GEDCOM_HEADER.HEAD.GEDC.FORM.VERS = GEDCOM_HEADER.HEAD.GEDC.FORM.VERS("5.5.5")
        ex.GEDCOM_HEADER.HEAD.CHAR = GEDCOM_HEADER.HEAD.CHAR("UTF-8")
        ex.GEDCOM_FORM_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION()
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR("GS")
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.NAME = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.NAME(
            "GEDCOM Specification"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.VERS = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.VERS(
            "5.5.5"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.CORP = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.CORP(
            "gedcom.org"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE = ADDRESS_STRUCTURE()
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE.ADDR = ADDRESS_STRUCTURE.ADDR()
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE.ADDR.CITY = ADDRESS_STRUCTURE.ADDR.CITY("LEIDEN")
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE.WWWs = [ADDRESS_STRUCTURE.WWW("www.gedcom.org")]

        ex.GEDCOM_FORM_HEADER_EXTENSION.DATE = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.DATE(
            "2019-10-02"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.DATE.TIME = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.DATE.TIME(
            "0:00:00"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.FILE = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.FILE(
            "555Sample.ged"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LANG = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.LANG(
            "English"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SUBM = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SUBM("U1")

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
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("1822-10-02")
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

        death = INDIVIDUAL_EVENT_STRUCTUREs.DEAT(NULL())
        death.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("1905-04-14")
        death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        death.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Stamford, Fairfield, Connecticut, United States of America"
        )
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(death)

        burial = INDIVIDUAL_EVENT_STRUCTUREs.BURI()
        burial.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        burial.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        burial.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        burial.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Spring Hill Cemetery, Stamford, Fairfield, Connecticut, United States of America"
        )
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(burial)

        indi.INDI.SPOUSE_TO_FAMILY_LINKs = list()

        spouselink = SPOUSE_TO_FAMILY_LINK()
        spouselink.FAMS = SPOUSE_TO_FAMILY_LINK.FAMS("F1")
        indi.INDI.SPOUSE_TO_FAMILY_LINKs.append(spouselink)

        spouselink = SPOUSE_TO_FAMILY_LINK()
        spouselink.FAMS = SPOUSE_TO_FAMILY_LINK.FAMS("F2")
        indi.INDI.SPOUSE_TO_FAMILY_LINKs.append(spouselink)

        indi.INDI.INDIVIDUAL_ATTRIBUTE_STRUCTUREs = list()
        indiattr = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.RESI()
        indiattr.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        indiattr.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        indiattr.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(FROM="1900", TO="1905")
        indi.INDI.INDIVIDUAL_ATTRIBUTE_STRUCTUREs.append(indiattr)

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
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE(BEF="1828")
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Connecticut, United States of America"
        )
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(birth)

        indi.INDI.SPOUSE_TO_FAMILY_LINKs = list()
        spouselink = SPOUSE_TO_FAMILY_LINK()
        spouselink.FAMS = SPOUSE_TO_FAMILY_LINK.FAMS("F1")
        indi.INDI.SPOUSE_TO_FAMILY_LINKs.append(spouselink)

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
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("1861-06-11")
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        birth.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Idaho Falls, Bonneville, Idaho, United States of America"
        )
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(birth)

        indi.INDI.CHILD_TO_FAMILY_LINKs = list()

        child_to_family_link = CHILD_TO_FAMILY_LINK()
        child_to_family_link.FAMC = CHILD_TO_FAMILY_LINK.FAMC("F1")
        indi.INDI.CHILD_TO_FAMILY_LINKs.append(child_to_family_link)

        child_to_family_link = CHILD_TO_FAMILY_LINK()
        child_to_family_link.FAMC = CHILD_TO_FAMILY_LINK.FAMC("F2")
        child_to_family_link.FAMC.PEDI = CHILD_TO_FAMILY_LINK.FAMC.PEDI("adopted")
        indi.INDI.CHILD_TO_FAMILY_LINKs.append(child_to_family_link)

        adoption = INDIVIDUAL_EVENT_STRUCTUREs.ADOP()
        adoption.INDIVIDUAL_EVENT_DETAIL = INDIVIDUAL_EVENT_DETAIL()
        adoption.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        adoption.INDIVIDUAL_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("1864-03-16")
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs.append(adoption)

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(indi)
        ########################################################################
        fam = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
        fam.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM("F1")
        fam.FAM.HUSB = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.HUSB("I1")
        fam.FAM.WIFE = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.WIFE("I2")

        fam.FAM.CHILs = list()
        fam.FAM.CHILs.append(CHIL("I3"))

        fam.FAM.FAMILY_EVENT_STRUCTUREs = list()
        marriage = FAMILY_EVENT_STRUCTUREs.MARR(NULL())
        marriage.FAMILY_EVENT_DETAIL = FAMILY_EVENT_DETAIL()
        marriage.FAMILY_EVENT_DETAIL.EVENT_DETAIL = EVENT_DETAIL()
        marriage.FAMILY_EVENT_DETAIL.EVENT_DETAIL.DATE = EVENT_DETAIL.DATE("1859-12")
        marriage.FAMILY_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE = PLACE_STRUCTURE()
        marriage.FAMILY_EVENT_DETAIL.EVENT_DETAIL.PLACE_STRUCTURE.PLAC = PLACE_STRUCTURE.PLAC(
            "Rapid City, Pennington, South Dakota, United States of America"
        )
        fam.FAM.FAMILY_EVENT_STRUCTUREs.append(marriage)

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(fam)
        ########################################################################
        fam = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
        fam.FAM = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM("F2")
        fam.FAM.HUSB = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.HUSB("I1")

        fam.FAM.CHILs = list()
        fam.FAM.CHILs.append(CHIL("I3"))

        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(fam)
        ########################################################################
        sour = LINEAGE_LINKED_RECORDs.SOURCE_RECORD()
        sour.SOUR = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR("S1")
        sour.SOUR.DATA = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA()

        sour.SOUR.DATA.EVENs = list()
        even = LINEAGE_LINKED_RECORDs.EVENs.EVEN("BIRT, DEAT, MARR")
        even.DATE = LINEAGE_LINKED_RECORDs.EVENs.EVEN.DATE(FROM="1820-01", TO="1825-12")
        even.PLAC = LINEAGE_LINKED_RECORDs.EVENs.EVEN.PLAC("Madison, Connecticut, United States of America")
        sour.SOUR.DATA.EVENs.append(even)

        sour.SOUR.DATA.AGNC = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA.AGNC(
            RESPONSIBLE_AGENCY("Madison County Court")
        )
        sour.SOUR.TITL = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.TITL(
            "Madison County Birth, Death, and Marriage Records"
        )
        sour.SOUR.ABBR = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.ABBR("Madison BMD Records")

        sour.SOUR.SOURCE_REPOSITORY_CITATIONs = list()

        citation = SOURCE_REPOSITORY_CITATION()
        citation.REPO = SOURCE_REPOSITORY_CITATION.REPO("R1")
        citation.REPO.CALN = SOURCE_REPOSITORY_CITATION.REPO.CALN("13B-1234.01")
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
        return ex

    def check_similarity(self, ex, case_insensitive, granularity, name):
        lines = GEDCOM_LINES()
        lines = ex(lines=lines, delta_level=0)
        result = lines(0)
        logger.info(result)
        with NamedTemporaryFile(suffix=".ged") as fp:
            fp.close()
            file = pathlib.Path(fp.name)
            file.write_text(result, encoding="utf-8-sig")
            actual = file.read_text()
            expected = (
                pathlib.Path(inspect.getframeinfo(inspect.currentframe()).filename).resolve().parent
                / pathlib.Path(name)
            ).read_text()

            if case_insensitive:
                expected = expected.casefold()
                actual = actual.casefold()

            if granularity == "set-of-lines":
                actual_lines = set(actual.splitlines())
                expected_lines = set(expected.splitlines())
                assert actual_lines == expected_lines
            elif granularity == "list-of-lines":
                actual_lines = actual.splitlines()
                expected_lines = expected.splitlines()
                assert actual_lines == expected_lines
            elif granularity == "text":
                assert actual == expected

    @pytest.mark.parametrize("case_insensitive", [True, False])
    @pytest.mark.parametrize("granularity", ["set-of-lines", "list-of-lines", "text"])
    def test_555sample(self, case_insensitive, granularity):
        self.check_similarity(self.get_555sample(), case_insensitive, granularity, "555SAMPLE.GED")

    @pytest.mark.parametrize("case_insensitive", [True, False])
    @pytest.mark.parametrize("granularity", ["set-of-lines", "list-of-lines", "text"])
    def test_minimal555(self, case_insensitive, granularity):
        self.check_similarity(self.get_minimal555(), case_insensitive, granularity, "MINIMAL555.GED")


def _address_structure():
    sure = ADDRESS_STRUCTURE()
    sure.ADDR = ADDRESS_STRUCTURE.ADDR()
    sure.ADDR.ADR1 = ADDRESS_STRUCTURE.ADDR.ADR1("ADDRESS_LINE_1")
    sure.ADDR.ADR2 = ADDRESS_STRUCTURE.ADDR.ADR2("ADDRESS_LINE_2")
    sure.ADDR.ADR3 = ADDRESS_STRUCTURE.ADDR.ADR3("ADDRESS_LINE_3")
    sure.ADDR.CITY = ADDRESS_STRUCTURE.ADDR.CITY("ADDRESS_CITY")
    sure.ADDR.STAE = ADDRESS_STRUCTURE.ADDR.STAE("ADDRESS_STATE")
    sure.ADDR.POST = ADDRESS_STRUCTURE.ADDR.POST("POST_CODE")
    sure.ADDR.CTRY = ADDRESS_STRUCTURE.ADDR.CTRY("ADDRESS_COUNTRY")
    sure.PHONs = 3 * [ADDRESS_STRUCTURE.PHON("PHONE_NUMBER")]
    sure.EMAILs = 3 * [ADDRESS_STRUCTURE.EMAIL("local-part@domain")]
    sure.FAXs = 3 * [ADDRESS_STRUCTURE.FAX("ADDRESS_FAX")]
    sure.WWWs = 3 * [ADDRESS_STRUCTURE.WWW("scheme://userinfo@host:portpath?query#fragment")]
    return sure


def _place_structure(M: int):
    sure = PLACE_STRUCTURE()
    sure.PLAC = PLACE_STRUCTURE.PLAC("PLACE_NAME")
    fone = PLACE_STRUCTURE.PLAC.FONE("PLACE_PHONETIC")
    fone.TYPE = PLACE_STRUCTURE.PLAC.FONE.TYPE("PHONETISATION_METHOD")
    sure.PLAC.FONEs = M * [fone]
    romn = PLACE_STRUCTURE.PLAC.FONE("PLACE_ROMANISED")
    romn.TYPE = PLACE_STRUCTURE.PLAC.FONE.TYPE("ROMANISATION_METHOD")
    sure.PLAC.ROMNs = M * [romn]
    sure.PLAC.MAP = PLACE_STRUCTURE.PLAC.MAP()
    sure.PLAC.MAP.LATI = PLACE_STRUCTURE.PLAC.MAP.LATI("PLACE_LATITUDE")
    sure.PLAC.MAP.LONG = PLACE_STRUCTURE.PLAC.MAP.LONG("PLACE_LONGITUDE")
    sure.PLAC.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
    return sure


def _multimedia_link():
    sure = MULTIMEDIA_LINK()
    sure.OBJE = MULTIMEDIA_LINK.OBJE("XREF:OBJE")
    return sure


def _note_structure_user_text():
    sure = NOTE_STRUCTUREs.NOTE_STRUCTURE_USER_TEXT()
    sure.NOTE = NOTE_STRUCTUREs.NOTE_STRUCTURE_USER_TEXT.NOTE(USER_TEXT("USER_TEXT"))
    return sure


def _note_structure_xref_note():
    sure = NOTE_STRUCTUREs.NOTE_STRUCTURE_XREF_NOTE()
    sure.NOTE = NOTE_STRUCTUREs.NOTE_STRUCTURE_XREF_NOTE.NOTE("XREF:NOTE")
    return sure


def _change_date(M: int):
    sure = CHANGE_DATE()
    sure.CHAN = CHANGE_DATE.CHAN()
    sure.CHAN.DATE = CHANGE_DATE.CHAN.DATE(datetime.datetime.now())
    sure.CHAN.DATE.TIME = CHANGE_DATE.CHAN.DATE.TIME(datetime.datetime.now())
    sure.CHAN.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
    return sure


def _event_detail(M: int):
    sure = EVENT_DETAIL()
    sure.TYPE = EVENT_DETAIL.TYPE("EVENT_OR_FACT_CLASSIFICATION")
    sure.DATE = EVENT_DETAIL.DATE(datetime.datetime.now())
    sure.PLACE_STRUCTURE = _place_structure(M)
    sure.ADDRESS_STRUCTURE = _address_structure()
    sure.AGNC = EVENT_DETAIL.AGNC("RESPONSIBLE_AGENCY")
    sure.RELI = EVENT_DETAIL.RELI("RELIGIOUS_AFFILIATION")
    sure.CAUS = EVENT_DETAIL.CAUS("CAUSE_OF_EVENT")
    sure.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
    return sure


def _family_event_detail(M: int):
    sure = FAMILY_EVENT_DETAIL()
    sure.HUSB = FAMILY_EVENT_DETAIL.HUSB()
    sure.HUSB.AGE = FAMILY_EVENT_DETAIL.HUSB.AGE("AGE_AT_EVENT")
    sure.WIFE = FAMILY_EVENT_DETAIL.WIFE()
    sure.WIFE.AGE = FAMILY_EVENT_DETAIL.WIFE.AGE("AGE_AT_EVENT")
    sure.EVENT_DETAIL = _event_detail(M)
    return sure


def _family_event_structures(M: int):
    sure = FAMILY_EVENT_STRUCTUREs.ANUL()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.CENS()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.DIV()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.DIVF()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.ENGA()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.MARB()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.MARC()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.MARR(Y())
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.MARR(NULL())
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.MARL()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.MARS()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.RESI()
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.EVEN(Y())
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure
    sure = FAMILY_EVENT_STRUCTUREs.EVEN(NULL())
    sure.FAMILY_EVENT_DETAIL = _family_event_detail(M)
    yield sure


def _refn():
    sure = REFN("USER_REFNO")
    sure.TYPE = REFN.TYPE("USER_REFERENCE_TYPE")
    return sure


def _source_citation(M: int):
    sure = SOURCE_CITATION()
    sure.SOUR = SOURCE_CITATION.SOUR("XREF:SOUR")
    sure.SOUR.PAGE = SOURCE_CITATION.SOUR.PAGE("WHERE_WITHIN_SOURCE")
    sure.SOUR.EVEN = SOURCE_CITATION.SOUR.EVEN("EVENT_TYPE_CITED_FROM")
    sure.SOUR.EVEN.ROLE = SOURCE_CITATION.SOUR.EVEN.ROLE("ROLE_IN_EVENT")
    sure.SOUR.DATA = SOURCE_CITATION.SOUR.DATA()
    sure.SOUR.DATA.DATE = SOURCE_CITATION.SOUR.DATA.DATE(datetime.datetime.now())
    sure.SOUR.DATA.TEXTs = M * [TEXTs.TEXT("TEXT_FROM_SOURCE")]
    sure.SOUR.MULTIMEDIA_LINKs = M * [_multimedia_link()]
    sure.SOUR.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
    sure.SOUR.QUAY = SOURCE_CITATION.SOUR.QUAY(CERTAINTY_ASSESSMENT.QUESTIONABLE_RELIABILITY_OF_EVIDENCE)
    return sure


def _personal_name_pieces(M: int):
    sure = PERSONAL_NAME_PIECES()
    sure.NPFX = PERSONAL_NAME_PIECES.NPFX("NAME_PIECE_PREFIX")
    sure.GIVN = PERSONAL_NAME_PIECES.GIVN("NAME_PIECE_GIVEN")
    sure.NICK = PERSONAL_NAME_PIECES.NICK("NAME_PIECE_NICKNAME")
    sure.SPFX = PERSONAL_NAME_PIECES.SPFX("NAME_PIECE_SURNAME_PREFIX")
    sure.SURN = PERSONAL_NAME_PIECES.SURN("NAME_PEICE_SURNAME")
    sure.NSFX = PERSONAL_NAME_PIECES.NSFX("NAME_PIECE_SUFFIX")
    sure.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
    sure.SOURCE_CITATIONs = M * [_source_citation(M)]
    return sure


def _personal_name_structure(M: int):
    sure = PERSONAL_NAME_STRUCTURE()
    sure.NAME = PERSONAL_NAME_STRUCTURE.NAME("NAME_PERSONAL")
    sure.NAME.TYPE = PERSONAL_NAME_STRUCTURE.NAME.TYPE("NAME_TYPE")
    sure.NAME.PERSONAL_NAME_PIECES = _personal_name_pieces(M)
    fone = PERSONAL_NAME_STRUCTURE.NAME.FONE("NAME_PHONETIC")
    fone.TYPE = PERSONAL_NAME_STRUCTURE.NAME.FONE.TYPE("PHONETISATION_METHOD")
    fone.PERSONAL_NAME_PIECES = _personal_name_pieces(M)
    sure.NAME.FONEs = M * [fone]
    romn = PERSONAL_NAME_STRUCTURE.NAME.ROMN("NAME_ROMANISED")
    romn.TYPE = PERSONAL_NAME_STRUCTURE.NAME.FONE.TYPE("ROMANISATION_METHOD")
    romn.PERSONAL_NAME_PIECES = _personal_name_pieces(M)
    sure.NAME.ROMNs = M * [romn]
    return sure


def _individual_event_detail(M: int):
    sure = INDIVIDUAL_EVENT_DETAIL()
    sure.EVENT_DETAIL = _event_detail(M)
    sure.AGE = INDIVIDUAL_EVENT_DETAIL.AGE("AGE_AT_EVENT")
    return sure


def _individual_event_structures(M: int):
    sure = INDIVIDUAL_EVENT_STRUCTUREs.BIRT()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.FAMC = INDIVIDUAL_EVENT_STRUCTUREs.BIRT.FAMC("XREF:FAM")
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.CHR(Y())
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.FAMC = INDIVIDUAL_EVENT_STRUCTUREs.CHR.FAMC("XREF:FAM")
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.CHR(NULL())
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.FAMC = INDIVIDUAL_EVENT_STRUCTUREs.CHR.FAMC("XREF:FAM")
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.DEAT(Y())
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.DEAT(NULL())
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.BURI()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.CREM()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.ADOP()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.FAMC = INDIVIDUAL_EVENT_STRUCTUREs.ADOP.FAMC("XREF:FAM")
    sure.FAMC.ADOP = INDIVIDUAL_EVENT_STRUCTUREs.ADOP.FAMC.ADOP("ADOPTED_BY_WHICH_PARENT")
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.BAPM()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.BARM()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.BASM()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.CHRA()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.CONF()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.FCOM()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.NATU()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.EMIG()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.IMMI()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.CENS()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.PROB()
    yield sure
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.WILL()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.GRAD()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.RETI()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.EVEN(EVENT_DESCRIPTOR())
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure
    sure = INDIVIDUAL_EVENT_STRUCTUREs.EVEN(NULL())
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    yield sure


def _individual_attribute_structures(M: int):
    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.CAST(CASTE_NAME("CASTE_NAME"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.CAST.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.DSCR(PHYSICAL_DESCRIPTION("PHYSICAL_DESCRIPTION"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.DSCR.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.EDUC(SCHOLASTIC_ACHIEVEMENT("SCHOLASTIC_ACHIEVEMENT"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.EDUC.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.IDNO(ID_NUMBER("ID_NUMBER"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.IDNO.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.NATI(NATIONAL_OR_TRIBAL_ORIGIN("NATIONAL_OR_TRIBAL_ORIGIN"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.NATI.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.NCHI(COUNT_OF_CHILDREN("COUNT_OF_CHILDREN"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.NCHI.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.NMR(NUMBER_OF_RELATIONSHIPS("NUMBER_OF_RELATIONSHIPS"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.NMR.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.OCCU(OCCUPATION("OCCUPATION"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.OCCU.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.PROP(POSSESSIONS("POSSESSIONS"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.PROP.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.RELI(RELIGIOUS_AFFILIATION("RELIGIOUS_AFFILIATION"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.RELI.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.RESI()
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.RESI.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.TITL(NOBILITY_TYPE_TITLE("NOBILITY_TYPE_TITLE"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.TITL.TYPE("USER_REFERENCE_TYPE")
    yield sure

    sure = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.FACT(ATTRIBUTE_DESCRIPTOR("ATTRIBUTE_DESCRIPTOR"))
    sure.INDIVIDUAL_EVENT_DETAIL = _individual_event_detail(M)
    sure.TYPE = INDIVIDUAL_ATTRIBUTE_STRUCTUREs.FACT.TYPE("USER_REFERENCE_TYPE")
    yield sure


def _child_to_family_link(M: int):
    sure = CHILD_TO_FAMILY_LINK()
    sure.FAMC = CHILD_TO_FAMILY_LINK.FAMC("XREF:FAM")
    sure.FAMC.PEDI = CHILD_TO_FAMILY_LINK.FAMC.PEDI("PEDIGREE_LINKAGE_TYPE")
    sure.FAMC.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
    return sure


def _spouse_to_family_link(M: int):
    sure = SPOUSE_TO_FAMILY_LINK()
    sure.FAMS = SPOUSE_TO_FAMILY_LINK.FAMS("XREF:FAM")
    sure.FAMS.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
    return sure


def _association_structure(M: int):
    sure = ASSOCIATION_STRUCTURE()
    sure.ASSO = ASSOCIATION_STRUCTURE.ASSO("XREF:INDI")
    sure.ASSO.RELA = ASSOCIATION_STRUCTURE.ASSO.RELA("RELATION_IS_DESCRIPTOR")
    sure.ASSO.SOURCE_CITATIONs = M * [_source_citation(M)]
    sure.ASSO.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
    return sure


def _even():
    sure = EVENs.EVEN("EVENTS_RECORDED")
    sure.DATE = EVENs.EVEN.DATE(FROM=datetime.datetime.now(), TO=datetime.datetime.now())
    sure.PLAC = EVENs.EVEN.PLAC("SOURCE_JURISDICTION_PLACE")
    return sure


def _source_repository_citation(M: int):
    sure = SOURCE_REPOSITORY_CITATION()
    sure.REPO = SOURCE_REPOSITORY_CITATION.REPO("XREF:REPO")
    sure.REPO.CALN = SOURCE_REPOSITORY_CITATION.REPO.CALN("SOURCE_CALL_NUMBER")
    # sure.REPO.CALN.MEDI = SOURCE_REPOSITORY_CITATION.REPO.CALN.MEDI("SOURCE_MEDIA_TYPE")
    return sure


class TestGenerateFull:
    def test_prepare_check_in_gedcom_validator(self):
        M = 1

        ex = LINEAGE_LINKED_GEDCOM_FILE()

        ex.GEDCOM_HEADER = GEDCOM_HEADER()
        ex.GEDCOM_HEADER.HEAD = GEDCOM_HEADER.HEAD()
        ex.GEDCOM_HEADER.HEAD.GEDC = GEDCOM_HEADER.HEAD.GEDC()
        ex.GEDCOM_HEADER.HEAD.GEDC.VERS = GEDCOM_HEADER.HEAD.GEDC.VERS("5.5.5")
        ex.GEDCOM_HEADER.HEAD.GEDC.FORM = GEDCOM_HEADER.HEAD.GEDC.FORM("LINEAGE-LINKED")
        ex.GEDCOM_HEADER.HEAD.GEDC.FORM.VERS = GEDCOM_HEADER.HEAD.GEDC.FORM.VERS("5.5.5")
        ex.GEDCOM_HEADER.HEAD.CHAR = GEDCOM_HEADER.HEAD.CHAR("UTF-8")

        ex.GEDCOM_FORM_HEADER_EXTENSION = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION()
        ex.GEDCOM_FORM_HEADER_EXTENSION.DEST = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.DEST(
            "DEST_SYSTEM_ID"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR(
            "SOURCE_SYSTEM_ID"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.VERS = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.VERS(
            "0.0.0.0"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.NAME = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.NAME(
            "NAME_OF_PRODUCT"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.CORP = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.CORP(
            "NAME_OF_BUSINESS"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.CORP.ADDRESS_STRUCTURE = _address_structure()

        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.DATA = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.DATA(
            "NAME_OF_SOURCE_DATA"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.DATA.DATE = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.DATA.DATE(
            datetime.datetime.now()
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SOUR.DATA.COPR = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SOUR.DATA.COPR(
            "COPYRIGHT_SOURCE_DATA"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.DATE = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.DATE(
            datetime.datetime.now()
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.DATE.TIME = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.DATE.TIME(
            datetime.datetime.now()
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.LANG = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.LANG(
            "LANGUAGE_OF_TEXT"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.SUBM = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.SUBM(
            "XREF:SUBM"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.FILE = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.FILE(
            "GEDCOM_FILE_NAME"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.COPR = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.COPR(
            "COPYRIGHT_GEDCOM_FILE"
        )
        ex.GEDCOM_FORM_HEADER_EXTENSION.NOTE = GEDCOM_FORM_HEADER_EXTENSIONs.LINEAGE_LINKED_HEADER_EXTENSION.NOTE(
            "GEDCOM_CONTENT_DESCRIPTION"
        )

        ex.FORM_RECORDS = FORM_RECORDS()
        ex.FORM_RECORDS.SUBMITTER_RECORD = SUBMITTER_RECORD()
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM = SUBMITTER_RECORD.SUBM("XREF:SUBM")
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.NAME = SUBMITTER_RECORD.SUBM.NAME("SUBMITTER_NAME")
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.ADDRESS_STRUCTURE = _address_structure()
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.MULTIMEDIA_LINKs = M * [_multimedia_link()]
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.RIN = SUBMITTER_RECORD.SUBM.RIN("AUTOMATED_ID")
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.NOTE_STRUCTUREs = M * [
            _note_structure_user_text(),
            _note_structure_xref_note(),
        ]
        ex.FORM_RECORDS.SUBMITTER_RECORD.SUBM.CHANGE_DATE = _change_date(M)

        ########################################################################
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs: List[LINEAGE_LINKED_RECORDs.LINEAGE_LINKED_RECORD] = list()
        ########################################################################
        # <<FAM_GROUP_RECORD>>
        ########################################################################
        fam = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD()
        fam.FAM("XREF:FAM")
        fam.FAM.FAMILY_EVENT_STRUCTUREs = list(_family_event_structures(M))
        fam.FAM.HUSB = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.HUSB("XREF:INDI")
        fam.FAM.WIFE = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.WIFE("XREF:INDI")
        fam.FAM.CHILs = M * [CHIL("XREF:INDI")]
        fam.FAM.NCHI = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.NCHI("COUNT_OF_CHILDREN")
        fam.FAM.REFNs = M * [_refn()]
        fam.FAM.RIN = LINEAGE_LINKED_RECORDs.FAM_GROUP_RECORD.FAM.RIN("AUTOMATED_RECORD_ID")
        fam.FAM.CHANGE_DATE = _change_date(M)
        fam.FAM.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
        fam.FAM.SOURCE_CITATIONs = M * [_source_citation(M)]
        fam.FAM.MULTIMEDIA_LINKs = M * [_multimedia_link()]
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.extend(M * [fam])
        ########################################################################
        # <<INDIVIDUAL_RECORD>>
        ########################################################################
        indi = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD()
        indi.INDI("XREF:INDI")
        indi.INDI.PERSONAL_NAME_STRUCTUREs = M * [_personal_name_structure(M)]
        indi.INDI.SEX = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI.SEX("SEX_VALUE")
        indi.INDI.INDIVIDUAL_EVENT_STRUCTUREs = list(_individual_event_structures(M))
        indi.INDI.INDIVIDUAL_ATTRIBUTE_STRUCTUREs = list(_individual_attribute_structures(M))
        indi.INDI.CHILD_TO_FAMILY_LINKs = M * [_child_to_family_link(M)]
        indi.INDI.SPOUSE_TO_FAMILY_LINKs = M * [_spouse_to_family_link(M)]
        indi.INDI.ASSOCIATION_STRUCTUREs = M * [_association_structure(M)]
        indi.INDI.REFNs = M * [_refn()]
        indi.INDI.RIN = LINEAGE_LINKED_RECORDs.INDIVIDUAL_RECORD.INDI.RIN("AUTOMATED_ID")
        indi.INDI.CHANGE_DATE = _change_date(M)
        indi.INDI.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
        indi.INDI.SOURCE_CITATIONs = M * [_source_citation(M)]
        indi.INDI.MULTIMEDIA_LINKs = M * [_multimedia_link()]
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.extend(M * [indi])
        ########################################################################
        # <<MULTIMEDIA_RECORD>>
        ########################################################################
        obje = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD()
        obje.OBJE = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE("XREF:OBJE")
        obje.OBJE.FILE = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.FILE("MULTIMEDIA_FILE_REFERENCE")
        obje.OBJE.FILE.FORM = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.FILE.FORM("JPEG")
        obje.OBJE.FILE.FORM.TYPE = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.FILE.FORM.TYPE("SOURCE_MEDIA_TYPE")
        obje.OBJE.FILE.TITL = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.FILE.TITL("DESCRIPTIVE_TITLE")
        obje.OBJE.REFNs = M * [_refn()]
        obje.OBJE.RIN = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.RIN("AUTOMATED_ID")
        obje.OBJE.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
        obje.OBJE.SOURCE_CITATIONs = M * [_source_citation(M)]
        obje.OBJE.CHANGE_DATE = _change_date(M)
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(obje)
        obje = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD()
        obje.OBJE = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE("XREF:OBJE:TIFF")
        obje.OBJE.FILE = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.FILE("MULTIMEDIA_FILE_REFERENCE")
        obje.OBJE.FILE.FORM = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.FILE.FORM("TIFF")
        obje.OBJE.FILE.FORM.TYPE = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.FILE.FORM.TYPE("SOURCE_MEDIA_TYPE")
        obje.OBJE.FILE.TITL = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.FILE.TITL("DESCRIPTIVE_TITLE")
        obje.OBJE.REFNs = M * [_refn()]
        obje.OBJE.RIN = LINEAGE_LINKED_RECORDs.MULTIMEDIA_RECORD.OBJE.RIN("AUTOMATED_ID")
        obje.OBJE.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
        obje.OBJE.SOURCE_CITATIONs = M * [_source_citation(M)]
        obje.OBJE.CHANGE_DATE = _change_date(M)
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.append(obje)
        ########################################################################
        # <<NOTE_RECORD>>
        ########################################################################
        note = LINEAGE_LINKED_RECORDs.NOTE_RECORD()
        note.NOTE = LINEAGE_LINKED_RECORDs.NOTE_RECORD.NOTE(XREF_NOTE("XREF:NOTE"), USER_TEXT("USER_TEXT"))
        note.NOTE.REFNs = M * [_refn()]
        note.NOTE.RIN = LINEAGE_LINKED_RECORDs.NOTE_RECORD.NOTE.RIN("AUTOMATED_ID")
        note.NOTE.SOURCE_CITATIONs = M * [_source_citation(M)]
        note.NOTE.CHANGE_DATE = _change_date(M)
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.extend(M * [note])

        note = LINEAGE_LINKED_RECORDs.NOTE_RECORD()
        note.NOTE = LINEAGE_LINKED_RECORDs.NOTE_RECORD.NOTE(USER_TEXT("USER_TEXT"))
        note.NOTE.REFNs = M * [_refn()]
        note.NOTE.RIN = LINEAGE_LINKED_RECORDs.NOTE_RECORD.NOTE.RIN("AUTOMATED_ID")
        note.NOTE.SOURCE_CITATIONs = M * [_source_citation(M)]
        note.NOTE.CHANGE_DATE = _change_date(M)
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.extend(M * [note])
        ########################################################################
        # <<REPOSITORY_RECORD>>
        ########################################################################
        repo = LINEAGE_LINKED_RECORDs.REPOSITORY_RECORD()
        repo.REPO = LINEAGE_LINKED_RECORDs.REPOSITORY_RECORD.REPO("XREF:REPO")
        repo.REPO.NAME = LINEAGE_LINKED_RECORDs.REPOSITORY_RECORD.REPO.NAME("NAME_OF_REPOSITORY")
        repo.REPO.ADDRESS_STRUCTURE = _address_structure()
        repo.REPO.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
        repo.REPO.REFNs = M * [_refn()]
        repo.REPO.RIN = LINEAGE_LINKED_RECORDs.REPOSITORY_RECORD.REPO.RIN("AUTOMATED_ID")
        repo.REPO.CHANGE_DATE = _change_date(M)
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.extend(M * [repo])
        ########################################################################
        # <<SOURCE_RECORD>>
        ########################################################################
        sour = LINEAGE_LINKED_RECORDs.SOURCE_RECORD()
        sour.SOUR = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR("XREF:SOUR")
        sour.SOUR.DATA = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA()
        sour.SOUR.DATA.EVENs = M * [_even()]
        sour.SOUR.DATA.AGNC = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.DATA.AGNC("RESPONSIBLE_AGENCY")
        sour.SOUR.DATA.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
        sour.SOUR.AUTH = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.AUTH("SOURCE_ORIGINATOR")
        sour.SOUR.TITL = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.TITL("SOURCE_DESCRIPTIVE_TITLE")
        sour.SOUR.ABBR = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.ABBR("SOURCE_FILED_BY_ENTRY")
        sour.SOUR.PUBL = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.PUBL("SOURCE_PUBLICATION_FACTS")
        sour.SOUR.TEXT = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.TEXT("TEXT_FROM_SOURCE")
        sour.SOUR.SOURCE_REPOSITORY_CITATIONs = M * [_source_repository_citation(M)]
        sour.SOUR.REFNs = M * [_refn()]
        sour.SOUR.RIN = LINEAGE_LINKED_RECORDs.SOURCE_RECORD.SOUR.RIN("AUTOMATED_ID")
        sour.SOUR.CHANGE_DATE = _change_date(M)
        sour.SOUR.NOTE_STRUCTUREs = M * [_note_structure_user_text(), _note_structure_xref_note()]
        sour.SOUR.MULTIMEDIA_LINKs = M * [_multimedia_link()]
        ex.FORM_RECORDS.LINEAGE_LINKED_RECORDs.extend(M * [sour])
        ########################################################################

        ex.GEDCOM_TRAILER = GEDCOM_TRAILER()
        ex.GEDCOM_TRAILER.TRLR = GEDCOM_TRAILER.TRLR()

        lines = GEDCOM_LINES()
        lines = ex(lines=lines, delta_level=0)
        result = lines(0)
        logger.info(result)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ged") as fp:
            fp.close()
            file = pathlib.Path(fp.name)
            file.write_text(result, encoding="utf-8-sig")
            logger.info(file.absolute())

            assert False
