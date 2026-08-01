from bs4 import BeautifulSoup
from urllib.parse import urljoin


def extract_jobs(
    html,
    base_url,
    company
):

    jobs = []

    soup = BeautifulSoup(
        html,
        "html.parser"
    )


    links = soup.find_all("a")


    for link in links:

        title = link.get_text(
            strip=True
        )

        href = link.get(
            "href"
        )


        if not title or not href:
            continue


        keywords = [
            "manager",
            "director",
            "lead",
            "partnership",
            "payment",
            "business",
            "customer",
            "account",
            "commercial"
        ]


        if any(
            k.lower() in title.lower()
            for k in keywords
        ):

            jobs.append(
                {
                    "Company": company,
                    "Job Title": title,
                    "Job URL":
                        urljoin(
                            base_url,
                            href
                        ),
                    "Official Source":
                        base_url
                }
            )


    return jobs
