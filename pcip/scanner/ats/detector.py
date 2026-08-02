import requests
from urllib.parse import urljoin


ATS_PATTERNS = {


    "Greenhouse": [

        "greenhouse.io",

        "boards.greenhouse.io"

    ],


    "Lever": [

        "jobs.lever.co",

        "lever.co"

    ],


    "Workday": [

        "myworkdayjobs.com",

        "workday.com"

    ],


    "SmartRecruiters": [

        "smartrecruiters.com"

    ]

}



def detect_ats(
    career_url
):


    result = {


        "ATS": "Unknown",

        "ATS_URL": "",

        "Confidence": 0

    }



    if not career_url:


        return result



    try:


        response = requests.get(

            career_url,

            timeout=10,

            headers={

                "User-Agent":

                "Mozilla/5.0"

            }

        )



        html = response.text.lower()



        for ats, patterns in ATS_PATTERNS.items():


            for pattern in patterns:


                if pattern in html:


                    result["ATS"] = ats


                    result["Confidence"] = 95


                    result["ATS_URL"] = extract_ats_url(

                        html,

                        pattern

                    )


                    return result



        # fallback:
        # check redirect url


        final_url = response.url.lower()



        for ats, patterns in ATS_PATTERNS.items():


            for pattern in patterns:


                if pattern in final_url:


                    result["ATS"] = ats


                    result["ATS_URL"] = response.url

                    result["Confidence"] = 90


                    return result



    except Exception as e:


        result["Error"] = str(e)



    return result




def extract_ats_url(
    html,
    pattern
):


    try:


        index = html.find(
            pattern
        )


        if index == -1:

            return ""



        start = html.rfind(

            "https://",

            0,

            index

        )



        if start == -1:

            return ""



        end = html.find(

            "\"",

            index

        )



        if end == -1:

            end = index + len(pattern)



        return html[start:end]



    except:


        return ""
