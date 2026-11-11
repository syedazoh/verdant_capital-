"""Windows replacement contention must preserve complete reports and bounded failures."""

import errno
import json

import pytest

from data import files


@pytest.mark.parametrize("winerror", [5, 32, 33])
def test_transient_windows_replace_errors_are_retried(tmp_path, monkeypatch, winerror):
    target = tmp_path / "report.json"
    target.write_text('{"old": true}', encoding="utf-8")
    replace = files.os.replace
    attempts = []

    def contended_replace(source, destination):
        attempts.append(1)
        if len(attempts) <= 2:
            assert json.loads(target.read_text()) == {"old": True}
            error = PermissionError(errno.EACCES, "Windows file contention")
            error.winerror = winerror
            raise error
        replace(source, destination)

    monkeypatch.setattr(files.os, "replace", contended_replace)
    monkeypatch.setattr(files, "sleep", lambda _: None, raising=False)
    files.write_json(target, {"new": True})
    assert len(attempts) == 3
    assert json.loads(target.read_text()) == {"new": True}
    assert list(tmp_path.iterdir()) == [target]


@pytest.mark.parametrize("winerror,expected_attempts", [(32, 8), (None, 1)])
def test_permanent_errors_propagate_and_keep_previous_report(
    tmp_path, monkeypatch, winerror, expected_attempts
):
    target = tmp_path / "report.json"
    target.write_text('{"old": true}', encoding="utf-8")
    attempts = []

    def denied_replace(source, destination):
        attempts.append(1)
        error = PermissionError(errno.EACCES, "Replacement denied")
        if winerror is not None:
            error.winerror = winerror
        raise error

    monkeypatch.setattr(files.os, "replace", denied_replace)
    monkeypatch.setattr(files, "sleep", lambda _: None, raising=False)
    with pytest.raises(PermissionError):
        files.write_json(target, {"new": True})
    assert len(attempts) == expected_attempts
    assert json.loads(target.read_text()) == {"old": True}
    assert list(tmp_path.iterdir()) == [target]
