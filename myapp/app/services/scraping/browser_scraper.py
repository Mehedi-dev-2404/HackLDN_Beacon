from app.core.logging import get_logger
from app.services.scraping.http_scraper import HttpScraper

logger = get_logger(__name__)


class BrowserScraper:
    def __init__(self) -> None:
        self.http = HttpScraper()

    def scrape(self, source_url: str, raw_html: str = "") -> tuple[str, str]:
        if raw_html.strip():
            return "inline", raw_html

        # Placeholder browser mode for hackathon speed.
        logger.info("Browser mode requested; delegating to HTTP scraper")
        return self.http.scrape(source_url=source_url, raw_html=raw_html)
