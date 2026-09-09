import os
from src.extract import parse_book_detail, parse_catalogue_page

FIXTURES = os.path.join(os.path.dirname(__file__), "fixtures")


def _read(name):
    with open(os.path.join(FIXTURES, name), encoding="utf-8") as f:
        return f.read()


def test_parse_book_detail_with_description():
    html = _read("book_with_description.html")
    record = parse_book_detail(
        html,
        product_url="https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        source_page="https://books.toscrape.com/catalogue/page-1.html",
        fetched_at="2026-08-06T10:00:00Z",
    )
    assert record["title"] == "A Light in the Attic"
    assert record["price_text"] == "£51.77"
    assert record["rating_text"] == "Five"
    assert record["description"] is not None


def test_parse_book_detail_missing_description_is_null():
    html = _read("book_no_description.html")
    record = parse_book_detail(
        html,
        product_url="https://books.toscrape.com/catalogue/no-blurb_1/index.html",
        source_page="https://books.toscrape.com/catalogue/page-1.html",
        fetched_at="2026-08-06T10:00:00Z",
    )
    assert record["title"] == "A Book With No Blurb"
    assert record["description"] is None  # never invent text that wasn't on the page


def test_parse_catalogue_page_relative_to_absolute_and_dedupe():
    html = """
    <html><body>
      <article class="product_pod"><h3><a href="../book-a/index.html">A</a></h3></article>
      <article class="product_pod"><h3><a href="../book-a/index.html">A again</a></h3></article>
      <article class="product_pod"><h3><a href="../book-b/index.html">B</a></h3></article>
      <li class="next"><a href="page-2.html">next</a></li>
    </body></html>
    """
    page_url = "https://books.toscrape.com/catalogue/page-1.html"
    links, next_url = parse_catalogue_page(html, page_url)
    assert links == [
        "https://books.toscrape.com/catalogue/book-a/index.html",
        "https://books.toscrape.com/catalogue/book-a/index.html",
        "https://books.toscrape.com/catalogue/book-b/index.html",
    ]
    assert next_url == "https://books.toscrape.com/catalogue/page-2.html"
