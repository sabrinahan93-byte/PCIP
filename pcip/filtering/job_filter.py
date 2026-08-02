MATCH_KEYWORDS = [

    # Core payment
    "payment",
    "payments",
    "fintech",
    "merchant",
    "acquiring",
    "acquirer",
    "gateway",
    "checkout",
    "wallet",
    "card",
    "issuing",
    "issuer",
    "billing",
    "settlement",
    "remittance",
    "cross border",
    "cross-border",


    # Commercial / Growth
    "partnership",
    "partner",
    "business development",
    "business",
    "commercial",
    "sales",
    "account executive",
    "account manager",
    "customer success",
    "client success",
    "strategic",
    "enterprise",
    "key account",
    "channel",
    "growth",
    "market expansion",
    "go to market",
    "gtm",


    # Operations
    "operations",
    "program manager",
    "project manager",
    "implementation",
    "solutions",
    "merchant solution"

]



HIGH_VALUE_KEYWORDS = [

    "payment partnership",
    "payment partnerships",
    "merchant",
    "acquiring",
    "business development",
    "customer success",
    "strategic partnership",
    "channel",
    "solutions"

]



MEDIUM_VALUE_KEYWORDS = [

    "product manager",
    "program manager",
    "operations",
    "account executive",
    "enterprise",
    "commercial"

]



EXCLUDE_KEYWORDS = [

    "software engineer",
    "backend engineer",
    "frontend engineer",
    "full stack engineer",
    "developer",
    "machine learning",
    "data scientist",
    "data engineer",
    "devops",
    "cloud engineer",
    "security engineer",
    "designer",
    "research scientist",
    "intern",
    "legal",
    "tax",
    "accounting"

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



    # High value matches

    for keyword in HIGH_VALUE_KEYWORDS:


        if keyword in title:

            score += 30



    # Medium value matches

    for keyword in MEDIUM_VALUE_KEYWORDS:


        if keyword in title:

            score += 15



    # General payment / commercial relevance

    for keyword in MATCH_KEYWORDS:


        if keyword in title:

            score += 5



    # Penalty

    for keyword in EXCLUDE_KEYWORDS:


        if keyword in title:

            score -= 50



    # Limit

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


    #
    # Release 5.3 Filtering v2
    #
    # Keep potential opportunities
    #

    return score >= 25
