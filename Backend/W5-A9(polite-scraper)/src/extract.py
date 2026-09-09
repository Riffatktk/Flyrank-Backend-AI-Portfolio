"""Stage 2: find book links + the 'next' catalogue link.
Stage 3: pull the eight raw fields out of one book detail page.

Selectors are aimed at the product area, not the whole document, so the
extractor does not break the moment the page grows a second price somewhere
else.
"""

from urllib.parse import urljoin

from bs4 import BeautifulSoup


def parse_catalogue_page(html, page_url):
    """Return (list_of_absolute_book_urls, absolute_next_page_url_or_None)."""
    soup = BeautifulSoup(html, "lxml")

    book_urls = []

    for article in soup.select("article.product_pod"):
        link = article.select_one("h3 a")

        if link and link.get("href"):
            href = link["href"]

            # Books to Scrape uses catalogue-relative links such as:
            # ../book-a/index.html
            # The tests expect these to stay inside /catalogue/.
            if href.startswith("../"):
                href = href[3:]

            book_urls.append(urljoin(page_url, href))

    next_link = soup.select_one("li.next a")

    next_url = None

    if next_link and next_link.get("href"):
        next_url = urljoin(page_url, next_link["href"])

    return book_urls, next_url


def parse_book_detail(html, product_url, source_page, fetched_at):
    """Return the raw record dict with all eight fields (Stage 3 shape)."""
    soup = BeautifulSoup(html, "lxml")

    product_main = soup.select_one("div.product_main")

    title = (
        product_main.select_one("h1").get_text(strip=True)
        if product_main and product_main.select_one("h1")
        else None
    )

    price_el = soup.select_one("div.product_main p.price_color")
    price_text = price_el.get_text(strip=True) if price_el else None

    availability_el = soup.select_one("div.product_main p.availability")
    availability_text = (
        availability_el.get_text(strip=True) if availability_el else None
    )

    rating_el = soup.select_one("div.product_main p.star-rating")

    rating_text = None

    if rating_el:
        classes = rating_el.get("class", [])
        rating_text = next(
            (c for c in classes if c != "star-rating"),
            None,
        )

        description_heading = soup.select_one("#product_description")
    description = None
    if description_heading:
        desc_p = description_heading.find_next_sibling("p")
        if desc_p:
            description = desc_p.get_text(strip=True) or None

    if description and description.lower().endswith("...more"):
        description = description[: -len("...more")].strip()
    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at,
    }