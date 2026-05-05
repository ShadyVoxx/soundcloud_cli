#HELPER FUNCTION
def truncate(text, length=20) -> str:
        return text if len(text) <=length else text[:length-1] + "…"

def get_artwork_url(url: str | None) -> str | None:
    if url is None:
        return None
    return url.replace("-large", "-t500x500")
