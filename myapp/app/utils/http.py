from urllib.parse import urlparse



def normalize_url(url: str) -> str:
    cleaned = (url or "").strip()
    if not cleaned:
        return ""

    parsed = urlparse(cleaned)
    if parsed.scheme:
        return cleaned
    return f"https://{cleaned}"
