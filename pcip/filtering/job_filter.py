MATCH_KEYWORDS = [

    # =========================================================
    # English
    # =========================================================

    # Payment ecosystem

    "payment",
    "payments",

    "fintech",

    "gateway",
    "checkout",
    "wallet",

    "billing",
    "settlement",
    "remittance",

    "payout",
    "payin",
    "pay-in",
    "pay-out",

    "card",


    # Business

    "channel",
    "strategic",

    "enterprise",

    "platform",
    "marketplace",

    "merchant",


    # Product / Technology Adjacent

    "api",
    "integration",
    "implementation",

    "solution",

    "web3",

    "stablecoin",
    "stablecoins",


    # =========================================================
    # Chinese
    # =========================================================

    "支付",
    "金融科技",

    "支付网关",

    "支付渠道",
    "支付通道",

    "钱包",

    "收单",

    "发卡",
    "卡发行",

    "结算",
    "汇款",

    "收款",
    "付款",

    "账单",

    "商户",
]



HIGH_VALUE_KEYWORDS = [

    # =========================================================
    # English
    # =========================================================

    # Core Payments / Infrastructure

    "cross-border payment",
    "cross-border payments",
    "cross border payment",
    "cross border payments",

    "payment partnership",
    "payment partnerships",

    "merchant solution",
    "merchant solutions",
    "merchant acquiring",

    "acquiring",
    "acquirer",

    "card issuing",
    "issuer",

    "payment channel",
    "payment channels",


    # Commercial Payment Roles

    "strategic partnership",
    "strategic partnerships",

    "payment strategy",

    "payment solution",
    "payment solutions",

    "account manager",

    "global payment partnership",
    "global payments partnership",

    "customer success manager",


    # =========================================================
    # Chinese
    # =========================================================

    "跨境支付",
    "支付渠道",

    "售前解决方案",
    "行业解决方案",
    "支付解决方案",

    "收单",
    "收单业务",

    "卡发行",
    "发卡",

    "客户经理",
]



MEDIUM_VALUE_KEYWORDS = [

    # =========================================================
    # English
    # =========================================================

    # Commercial

    "business development",
    "business development manager",

    "customer success",
    "client success",

    "key account",

    "enterprise",
    "commercial",

    "partnership",

    "crypto",


    # Growth

    "market expansion",

    "go to market",
    "go-to-market",
    "gtm",

    "growth",


    # Payment Operations / Delivery

    "payment operations",
    "merchant operations",

    "solutions manager",
    "solution manager",


    # =========================================================
    # Chinese
    # =========================================================

    "商务拓展",
    "业务拓展",
    "商业拓展",

    "客户成功",

    "大客户",
    "关键客户",

    "商业合作",
    "渠道合作",

    "市场拓展",
    "市场扩张",

    "业务发展",
    "战略合作",
]


COMBINATION_KEYWORDS = {

    # AI + Payment related roles
    "ai_payment": {
        "keywords": [
            "ai",
            "payment"
        ],
        "score": 20
    },


    # Cross-border acquiring related roles
    "cross_border_acquiring": {
        "keywords": [
            "cross border",
            "acquiring"
        ],
        "score": 20
    },


    # Merchant payment solution roles
    "merchant_payment_solution": {
        "keywords": [
            "merchant",
            "payment"
        ],
        "score": 15
    },


    # Payment partnership roles
    "payment_partnership": {
        "keywords": [
            "payment",
            "partnership"
        ],
        "score": 20
    }

}



EXCLUDE_KEYWORDS = [

    # =========================================================
    # English
    # =========================================================

    # Engineering

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


    # Non-target functions

    "designer",
    "research scientist",

    "intern",
    "internship",

    "legal",
    "tax",
    "accounting",


    # Junior / Support

    "assistant",
    "coordinator",
    "junior",

    "technical support",
    "customer support",
    "support specialist",

    "VP",
    "Director",


    # Location / Language

    "San Francisco",
    "Japanese",


    # =========================================================
    # Chinese
    # =========================================================

    "软件工程师",
    "后端工程师",
    "前端工程师",
    "全栈工程师",

    "开发工程师",

    "机器学习",
    "数据科学家",
    "数据工程师",
    "运维工程师",

    "设计师",

    "实习生",

    "法务",
    "法律",
    "税务",
    "会计",
    "财务",
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



    # -----------------------------
    # High value matches
    # -----------------------------

    for keyword in HIGH_VALUE_KEYWORDS:

        if keyword in title:

            score += 30



    # -----------------------------
    # Medium value matches
    # -----------------------------

    for keyword in MEDIUM_VALUE_KEYWORDS:

        if keyword in title:

            score += 15




    # -----------------------------
    # General matches
    # -----------------------------

    for keyword in MATCH_KEYWORDS:

        if keyword in title:

            score += 5



    # -----------------------------
    # Combination matches
    # -----------------------------

    for rule in COMBINATION_KEYWORDS.values():

        matched = True


        for keyword in rule["keywords"]:

            if keyword not in title:

                matched = False
                break

                
        if matched:

            score += rule["score"]




   # -----------------------------
    # Exclude penalty
    # -----------------------------

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
