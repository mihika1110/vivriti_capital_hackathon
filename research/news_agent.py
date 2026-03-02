import requests

RISK_KEYWORDS = [
    "fraud", "penalty", "nclt", "default", "sebi", "ed", "raid", "litigation"
]

def analyze_news(company_name):
    sample_news = [
        f"{company_name} promoter involved in tax dispute",
        f"Sector faces margin pressure due to RBI regulations"
    ]

    risks=[]
    for article in sample_news:
        for kw in RISK_KEYWORDS:
            if kw in article.lower():
                risks.append(article)
                break

    return {
        "articles":sample_news,
        "risk_mentions":risks,
        "risk_score":len(risks)*10
    }