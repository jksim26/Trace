"""Test isolation: open_store() defaults to the repo's real kb/ vault, so the
whole test session points $TRACE_DB_DIR at a temp dir instead — no test can
leave a trace.db (or half-seeded store) inside the committed vault."""
import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def _isolated_trace_db_dir(tmp_path_factory):
    os.environ["TRACE_DB_DIR"] = str(tmp_path_factory.mktemp("trace-dbs"))
