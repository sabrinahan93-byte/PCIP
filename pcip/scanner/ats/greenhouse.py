import requests
from bs4 import BeautifulSoup



def scan_greenhouse(
    ats_url,
    company
):


    jobs = []



    if not ats_url:

        return jobs



    try:


        response = requests.get(

            ats_url,

            timeout=15,

            headers={

                "User-Agent":

                "Mozilla/5.0"

            }

        )



        response.raise_for_status()



        soup = BeautifulSoup(

            response.text,

            "html.parser"

        )



        job_links = soup.find_all(

            "a",

            href=True

        )



        for link in job_links:


            href = link["href"]


            title = link.get_text(

                strip=True

            )



            if not title:

                continue



            if (

                "/jobs/" not in href

                and

                "job" not in href.lower()

            ):

                continue



            if href.startswith("/"):


                job_url = (

                    ats_url.rstrip("/")

                    +

                    href

                )


            else:


                job_url = href



            jobs.append(

                {

                    "Company":

                        company,


                    "Job Title":

                        title,


                    "Location":

                        "",


                    "Work Mode":

                        "",


                    "Job URL":

                        job_url,


                    "Source":

                        "Greenhouse"

                }

            )



    except Exception as e:


        print(

            "Greenhouse Scanner Error:",

            company,

            str(e)

        )



    return jobs
