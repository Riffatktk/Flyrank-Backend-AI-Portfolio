"""Central config for the A9 scraper. One place to tune politeness knobs."""

BASE_URL = "https://books.toscrape.com/"
FIRST_CATALOGUE_URL = "https://books.toscrape.com/catalogue/page-1.html"
ROBOTS_URL = "https://books.toscrape.com/robots.txt"

USER_AGENT = "FlyRankInternshipA9/1.0 (+https://github.com/Riffatktk/flyrank-internship)"

REQUEST_TIMEOUT_SECONDS = 8
DELAY_BETWEEN_REAL_REQUESTS_SECONDS = 0.6
MAX_CATALOGUE_PAGES = 3

# One retry, short pause, only for timeouts / 5xx. Never for 404 or 403.
RETRYABLE_STATUS_CODES = {500, 502, 503, 504}
RETRY_WAIT_SECONDS = 1.5

CACHE_DIR = "cache"
OUTPUT_DIR = "output"
BOOKS_JSON_PATH = f"{OUTPUT_DIR}/books.json"
ERRORS_JSON_PATH = f"{OUTPUT_DIR}/errors.json"
RUN_REPORT_PATH = f"{OUTPUT_DIR}/run-report.json"
