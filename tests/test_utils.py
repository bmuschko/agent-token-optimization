"""Shared helpers."""
from orderly.utils.ids import is_prefixed, stable_id
from orderly.utils.text import mask, slugify, truncate


def test_slugify():
    assert slugify("Hello There!") == "hello-there"


def test_truncate_adds_suffix():
    assert truncate("abcdefgh", 5) == "ab..."


def test_mask_keeps_the_tail():
    assert mask("4111111111114417") == "************4417"


def test_stable_id_is_deterministic():
    assert stable_id("x", "a", "b") == stable_id("x", "a", "b")
    assert is_prefixed(stable_id("x", "a"), "x")
