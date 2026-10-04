"""CLI behaviour for the text report."""
from orderly.cli import main


def test_report_prints_a_total(capsys):
    assert main(["report"]) == 0
    assert "Total" in capsys.readouterr().out


def test_report_filters_by_status(capsys):
    assert main(["report", "--status", "paid"]) == 0
    assert "paid" in capsys.readouterr().out


def test_list_prints_order_ids(capsys):
    assert main(["list"]) == 0
    assert "ORD-1000" in capsys.readouterr().out


def test_show_missing_order_exits_nonzero(capsys):
    assert main(["show", "ORD-nope"]) == 1
