import requests


def scan_career_page(url):

    if not url:
        return [
            {
                "source": url,
                "status": "failed",
                "error": "Empty URL"
            }
        ]


    try:

        headers = {

            "User-Agent":
                (
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


        return [

            {

                "source": url,

                "html": response.text,

                "page_title": "",

                "status": "success"

            }

        ]


    except Exception as e:


        return [

            {

                "source": url,

                "status": "failed",

                "error": str(e)

            }

        ]
