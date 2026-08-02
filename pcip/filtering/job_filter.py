"""
PCIP Release 5.2
Job Filtering Engine

Purpose:
Calculate Match Score for each discovered job.

This module ONLY evaluates jobs.
It does NOT:
- write Excel
- update Pipeline Status
- update Applied Date
- update Notes
"""


import re



# ==============================
# Keyword Configuration
# ==============================


PAYMENT_KEYWORDS = [

    "payment",
    "payments",
    "paytech",
    "fintech",
    "financial technology",
    "cross-border",
    "cross border",
    "merchant",
    "merchant solution",
    "acquiring",
    "issuer",
    "issuing",
    "wallet",
    "remittance",
    "money movement"

]



PARTNERSHIP_KEYWORDS = [

    "partnership",
    "partner",
    "ecosystem",
    "alliances",
    "strategic partnership"

]



COMMERCIAL_KEYWORDS = [

    "business development",
    "business development manager",
    "commercial",
    "sales",
    "account executive",
    "enterprise",
    "growth",
    "strategy"

]



SENIORITY_KEYWORDS = [

    "manager",
    "senior",
    "lead",
    "director",
    "head",
    "principal",
    "vp",
    "vice president"

]



SOLUTION_KEYWORDS = [

    "solution",
    "platform",
    "product strategy",
    "market expansion"

]



NEGATIVE_KEYWORDS = [

    "software engineer",
    "backend engineer",
    "frontend engineer",
    "developer",
    "engineering",
    "data scientist",
    "machine learning",
    "designer",
    "recruiter",
    "accountant",
    "legal counsel"

]



# ==============================
# Helpers
# ==============================


def normalize(text):

    """
    Normalize text for matching
    """

    if not text:

        return ""

    return str(text).lower().strip()



def contains_keyword(
    text,
    keywords
):

    for keyword in keywords:

        if keyword in text:

            return True

    return False



# ==============================
# Match Score Engine
# ==============================


def calculate_match_score(job):

    """
    Calculate job relevance score.

    Return:
        integer 0-100
    """


    title = normalize(
        job.get(
            "Job Title",
            ""
        )
    )


    company = normalize(
        job.get(
            "Company",
            ""
        )
    )


    text = (

        title
        +
        " "
        +
        company

    )



    score = 0



    # Payment relevance

    if contains_keyword(
        text,
        PAYMENT_KEYWORDS
    ):

        score += 30



    # Partnership relevance

    if contains_keyword(
        text,
        PARTNERSHIP_KEYWORDS
    ):

        score += 25



    # Commercial / BD relevance

    if contains_keyword(
        text,
        COMMERCIAL_KEYWORDS
    ):

        score += 20



    # Seniority

    if contains_keyword(
        text,
        SENIORITY_KEYWORDS
    ):

        score += 15



    # Strategic solution roles

    if contains_keyword(
        text,
        SOLUTION_KEYWORDS
    ):

        score += 10



    # Technical penalty

    if contains_keyword(
        text,
        NEGATIVE_KEYWORDS
    ):

        score -= 35



    # Limit range

    score = max(
        0,
        min(
            score,
            100
        )
    )



    return score



# ==============================
# Public Function
# ==============================


def apply_match_score(job):

    """
    Attach Match Score to job object.

    Example:

    Input:
    {
        "Company":"Adyen",
        "Job Title":"Payment Partnerships Lead"
    }


    Output:
    {
        "Company":"Adyen",
        "Job Title":"Payment Partnerships Lead",
        "Match Score":90
    }

    """


    job["Match Score"] = calculate_match_score(
        job
    )


    return job
