MATCH_KEYWORDS = [

    # Payment / Fintech
    "payment",
    "payments",
    "fintech",
    "merchant",
    "acquiring",
    "gateway",
    "wallet",
    "card",
    "issuing",
    "issuer",
    "checkout",
    "billing",
    "settlement",
    "remittance",


    # Commercial
    "partnership",
    "partner",
    "business development",
    "business",
    "commercial",
    "sales",
    "account manager",
    "account management",
    "customer success",
    "client success",
    "strategic account",
    "key account",
    "enterprise",


    # Your target functions
    "channel",
    "growth",
    "go-to-market",
    "market expansion",
    "operations"

]



HIGH_MATCH_KEYWORDS = [

    "payment partnership",

    "payment partnerships",

    "merchant",

    "acquiring",

    "business development",

    "customer success",

    "strategic partnership",

    "channel"

]



EXCLUDE_KEYWORDS = [

    "software engineer",
    "backend engineer",
    "frontend engineer",
    "full stack",
    "developer",
    "machine learning",
    "data scientist",
    "data engineer",
    "devops",
    "security engineer",
    "designer",
    "legal",
    "tax",
    "accounting",
    "intern",
    "research"

]



def calculate_match_score(job):


    title = (

        job.get(
            "Job Title",
            ""

        )

        or ""

    ).lower()



    score = 0



    for keyword in HIGH_MATCH_KEYWORDS:


        if keyword in title:

            score += 25



    for keyword in MATCH_KEYWORDS:


        if keyword in title:

            score += 10



    for keyword in EXCLUDE_KEYWORDS:


        if keyword in title:

            score -= 40



    if score > 100:

        score = 100



    if score < 0:

        score = 0



    return score




def apply_match_score(job):


    score = calculate_match_score(

        job

    )


    job["Match Score"] = score


    return job




def is_relevant_job(job):


    score = calculate_match_score(

        job

    )


    return score >= 30
