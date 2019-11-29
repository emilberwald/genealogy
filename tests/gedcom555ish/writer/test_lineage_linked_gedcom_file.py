import pathlib
import pytest
import tempfile
import contextlib

from gedcom555ish.writer.lineage_linked_gedcom_file import *


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
        minimal555.SUBMITTER_RECORD = SUBMITTER_RECORD()
        minimal555.SUBMITTER_RECORD.SUBM = SUBMITTER_RECORD.SUBM("U")
        minimal555.SUBMITTER_RECORD.SUBM.NAME = SUBMITTER_RECORD.SUBM.NAME("gedcom.org")
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
                pathlib.Path("tests")
                / pathlib.Path("gedcom555ish")
                / pathlib.Path("writer")
                / pathlib.Path("MINIMAL555.GED")
            ).read_text()
            assert actual == expected

