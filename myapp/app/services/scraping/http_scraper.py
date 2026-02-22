from urllib.request import Request, urlopen

from app.core.logging import get_logger
from app.utils.http import normalize_url

logger = get_logger(__name__)


class HttpScraper:
    def scrape(self, source_url: str, raw_html: str = "") -> tuple[str, str]:
        if raw_html.strip():
            return "inline", raw_html

        url = normalize_url(source_url)
        if not url:
            return "mock", "<html><body><h1>No source provided</h1></body></html>"

        request = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko)"
                )
            },
        )

        try:
            with urlopen(request, timeout=10) as response:
                html = response.read().decode("utf-8", errors="ignore")
                return url, html
        except Exception as exc:
            logger.warning("HTTP scraping failed for %s: %s", url, exc)
            return "mock", "<html><body><h1>Fallback scrape mode</h1></body></html>"
