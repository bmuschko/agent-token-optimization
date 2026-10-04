"""T2 acceptance: the report command can emit JSON."""
import json

from orderly.cli import main


def test_json_format_emits_valid_json(capsys):
    assert main(["report", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["order_count"] > 0
    assert "total_cents" in payload


def test_text_remains_the_default(capsys):
    assert main(["report"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("Orders")


def test_json_respects_the_status_filter(capsys):
    assert main(["report", "--format", "json", "--status", "paid"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "paid"
