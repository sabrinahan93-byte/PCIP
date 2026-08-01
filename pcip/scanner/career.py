import requests
from bs4 import BeautifulSoup


def scan_career_page(url):

    jobs = []

    if not url:
        return jobs

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64)"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = soup.title.text if soup.title else ""

        jobs.append(
            {
                "source": url,
                "page_title": title,
                "status": "success"
            }
        )

    except Exception as e:

        jobs.append(
            {
                "source": url,
                "status": "failed",
                "error": str(e)
            }
        )

    return jobs
