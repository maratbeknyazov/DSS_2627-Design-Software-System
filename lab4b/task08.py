# Lab 4B - Task 8 - the Java habit that broke the search
#
# 8.1  A class keeps ONE function under each attribute name; the second
#      `def search` silently REPLACED the first (Python's final assignment
#      wins, slide 38: names are looked up in one slot). The class now has
#      only the two-argument version, so ps.search("iphone") dies with
#          TypeError: search() missing 1 required positional argument
#      for every request without filters - the shape the author had in
#      mind was lost in the "overloading".
#
# 8.2  One search() supports both calls; the default is `filters=None`,
#      NOT `filters={}`: a mutable default is created ONCE and shared by
#      every call - the exact bug of Lab 4A Task 1 (the cart that belonged
#      to everybody).
#
# 8.3  I choose the keyword-only dictionary: search("iphone",
#      filters={"brand": "Apple"}). Defenders: (a) filter keys come from
#      DATA (an HTTP JSON body) and may be any strings - keyword arguments
#      must be valid identifiers written in code and cannot be built
#      dynamically; (b) keyword-only (`*`) keeps the query clearly the
#      first argument and forbids accidental positional mixing; (c) dict +
#      None default solves 8.2 cleanly.
#
# 8.4  pyflakes finds it before review. Verified run on the ORIGINAL code:
#          tmp/lab4b_check/task08_original.py:9:5: redefinition of unused
#          'search' from line 5
#      (python -m pyflakes). pyflakes on THIS fixed file is clean.
#
# Run once for verification, as the task requires:
#     pip install mypy pyflakes
#     python -m pyflakes task08.py        -> no output, exit 0
#
# Done when: both kinds of call work, there is no mutable default, and a
#            test covers the call without filters.

import inspect


class ProductSearch:
    def __init__(self, products: list[dict]) -> None:
        self.products = products

    def search(
        self,
        query: str,
        *,
        filters: dict[str, object] | None = None,   # 8.2: None, never {}
    ) -> list[dict]:
        q = query.lower()
        result = [p for p in self.products if q in p["title"].lower()]
        if filters:
            for key, value in filters.items():
                result = [p for p in result if p.get(key) == value]
        return result


# --------------------------- tests ---------------------------

PRODUCTS = [
    {"title": "iPhone 15", "brand": "Apple"},
    {"title": "iPad Pro", "brand": "Apple"},
    {"title": "Samsung Galaxy S24", "brand": "Samsung"},
]


def test_search_without_filters_works():
    # The exact call shape that killed production.
    result = ProductSearch(PRODUCTS).search("iphone")
    assert result == [{"title": "iPhone 15", "brand": "Apple"}]


def test_search_with_filters_works():
    result = ProductSearch(PRODUCTS).search(
        "apple", filters={"brand": "Samsung"}
    )
    assert result == []                              # filter wins over text


def test_filtering_selects_the_matching_subset():
    result = ProductSearch(PRODUCTS).search("ip", filters={"brand": "Apple"})
    assert [p["title"] for p in result] == ["iPhone 15", "iPad Pro"]


def test_no_mutable_default_is_used():
    parameters = inspect.signature(ProductSearch.search).parameters
    assert parameters["filters"].default is None


def test_calling_with_an_explicit_empty_dict_leaves_no_traces():
    shared = {}
    ps = ProductSearch(PRODUCTS)
    first = ps.search("iphone", filters=shared)
    assert first == [{"title": "iPhone 15", "brand": "Apple"}]
    assert shared == {}                              # the caller's dict is safe
