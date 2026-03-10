"""
Legal Rights Objection (LRO) risk checker — §4.5.1.3

A trademark holder may file an LRO against any gTLD application whose string
is identical or confusingly similar to a mark in which they have rights, where
the applicant is acting in bad faith or the delegation would take unfair
advantage of the mark.  A successful LRO prevents the application proceeding.

This module checks three signal types in priority order:
  1. Exact match against the indexed brand list
  2. Edit-distance ≤ 1 against the top-tier brand set (highest LRO exposure)
  3. Unicode skeleton / confusable match (delegated to the visual checker)

Sources
-------
* Interbrand Best Global Brands 2024  (interbrand.com/best-global-brands/)
* Brand Finance Global 500 2024       (brandfinance.com/ranking/global500)
* ICANN 2012-round LRO decisions      (icann.org dispute-resolution archives)
* WIPO §6bis well-known marks         (wipo.int/madrid/en/branddb/)
* ICANN Applicant Guidebook 2026 §4.5.1.3
"""
from __future__ import annotations

# ── Brand catalogue ──────────────────────────────────────────────────────────
# Structure: label → {tier, sector, holder, score, source}
#   tier 1 = Interbrand / BF top-50 / WIPO §6bis — almost certain LRO target
#   tier 2 = Interbrand 51-100 / BF 51-200 — significant LRO risk
#   tier 3 = Well-known regional / B2B brands — advisory flag
_BRANDS: dict[str, dict] = {
    # ── Technology ─────────────────────────────────────────────────────────
    "apple":      {"tier": 1, "sector": "Technology",    "holder": "Apple Inc.",              "score": 75, "source": "Interbrand #1 2024; WIPO §6bis"},
    "google":     {"tier": 1, "sector": "Technology",    "holder": "Alphabet Inc.",            "score": 75, "source": "Interbrand #2 2024; WIPO §6bis"},
    "microsoft":  {"tier": 1, "sector": "Technology",    "holder": "Microsoft Corporation",    "score": 75, "source": "Interbrand #3 2024; WIPO §6bis"},
    "amazon":     {"tier": 1, "sector": "Retail/Tech",   "holder": "Amazon.com Inc.",          "score": 75, "source": "Interbrand #4 2024; WIPO §6bis"},
    "samsung":    {"tier": 1, "sector": "Technology",    "holder": "Samsung Electronics Co.", "score": 75, "source": "Interbrand #5 2024; WIPO §6bis"},
    "meta":       {"tier": 1, "sector": "Technology",    "holder": "Meta Platforms Inc.",      "score": 72, "source": "Brand Finance #6 2024"},
    "facebook":   {"tier": 1, "sector": "Technology",    "holder": "Meta Platforms Inc.",      "score": 72, "source": "Interbrand 2024; WIPO §6bis"},
    "intel":      {"tier": 1, "sector": "Technology",    "holder": "Intel Corporation",        "score": 68, "source": "Interbrand #12 2024"},
    "ibm":        {"tier": 1, "sector": "Technology",    "holder": "IBM Corporation",          "score": 68, "source": "Interbrand #14 2024; WIPO §6bis"},
    "cisco":      {"tier": 1, "sector": "Technology",    "holder": "Cisco Systems Inc.",       "score": 68, "source": "Interbrand #15 2024"},
    "oracle":     {"tier": 1, "sector": "Technology",    "holder": "Oracle Corporation",       "score": 65, "source": "Interbrand 2024"},
    "sap":        {"tier": 1, "sector": "Technology",    "holder": "SAP SE",                   "score": 65, "source": "Interbrand #17 2024"},
    "adobe":      {"tier": 1, "sector": "Technology",    "holder": "Adobe Inc.",               "score": 65, "source": "Interbrand #22 2024"},
    "salesforce": {"tier": 1, "sector": "Technology",    "holder": "Salesforce Inc.",          "score": 62, "source": "Interbrand 2024"},
    "accenture":  {"tier": 1, "sector": "Technology",    "holder": "Accenture plc",            "score": 62, "source": "Interbrand #18 2024"},
    "paypal":     {"tier": 1, "sector": "Fintech",       "holder": "PayPal Holdings Inc.",     "score": 62, "source": "Interbrand 2024"},
    "nvidia":     {"tier": 1, "sector": "Technology",    "holder": "NVIDIA Corporation",       "score": 65, "source": "Brand Finance #3 2024"},
    "qualcomm":   {"tier": 2, "sector": "Technology",    "holder": "Qualcomm Inc.",            "score": 55, "source": "Brand Finance Global 500 2024"},
    "huawei":     {"tier": 2, "sector": "Technology",    "holder": "Huawei Technologies",      "score": 55, "source": "Brand Finance #10 2024"},
    "sony":       {"tier": 1, "sector": "Technology",    "holder": "Sony Group Corporation",   "score": 65, "source": "Interbrand 2024; WIPO §6bis"},
    "panasonic":  {"tier": 2, "sector": "Technology",    "holder": "Panasonic Holdings",       "score": 55, "source": "Brand Finance Global 500 2024"},
    "lg":         {"tier": 2, "sector": "Technology",    "holder": "LG Electronics Inc.",      "score": 55, "source": "Brand Finance Global 500 2024"},
    "siemens":    {"tier": 2, "sector": "Technology",    "holder": "Siemens AG",               "score": 55, "source": "Interbrand 2024"},
    "philips":    {"tier": 2, "sector": "Technology",    "holder": "Philips N.V.",             "score": 52, "source": "Brand Finance Global 500 2024"},
    "ericsson":   {"tier": 2, "sector": "Technology",    "holder": "Telefonaktiebolaget LM Ericsson", "score": 52, "source": "Brand Finance Global 500 2024"},
    "nokia":      {"tier": 2, "sector": "Technology",    "holder": "Nokia Corporation",        "score": 52, "source": "Brand Finance Global 500 2024"},
    "hp":         {"tier": 2, "sector": "Technology",    "holder": "HP Inc.",                  "score": 55, "source": "Interbrand 2024"},
    "dell":       {"tier": 2, "sector": "Technology",    "holder": "Dell Technologies",        "score": 55, "source": "Brand Finance Global 500 2024"},

    # ── Internet / Media ───────────────────────────────────────────────────
    "youtube":    {"tier": 1, "sector": "Internet/Media","holder": "Alphabet Inc.",            "score": 70, "source": "Interbrand 2024"},
    "instagram":  {"tier": 1, "sector": "Internet/Media","holder": "Meta Platforms Inc.",      "score": 68, "source": "Interbrand 2024"},
    "whatsapp":   {"tier": 1, "sector": "Internet/Media","holder": "Meta Platforms Inc.",      "score": 68, "source": "Brand Finance Global 500 2024; WIPO §6bis"},
    "netflix":    {"tier": 1, "sector": "Internet/Media","holder": "Netflix Inc.",             "score": 65, "source": "Interbrand 2024"},
    "twitter":    {"tier": 1, "sector": "Internet/Media","holder": "X Corp.",                  "score": 65, "source": "Interbrand 2024; ICANN 2012 LRO precedent"},
    "linkedin":   {"tier": 2, "sector": "Internet/Media","holder": "Microsoft Corporation",    "score": 58, "source": "Interbrand 2024"},
    "spotify":    {"tier": 2, "sector": "Internet/Media","holder": "Spotify AB",               "score": 55, "source": "Brand Finance Global 500 2024"},
    "tiktok":     {"tier": 1, "sector": "Internet/Media","holder": "ByteDance Ltd.",           "score": 65, "source": "Brand Finance #7 2024"},
    "zoom":       {"tier": 2, "sector": "Internet/Media","holder": "Zoom Video Communications","score": 55, "source": "Brand Finance Global 500 2024"},
    "ebay":       {"tier": 2, "sector": "Internet/Media","holder": "eBay Inc.",                "score": 55, "source": "Interbrand 2024"},
    "uber":       {"tier": 2, "sector": "Internet/Media","holder": "Uber Technologies Inc.",   "score": 55, "source": "Brand Finance Global 500 2024"},
    "airbnb":     {"tier": 2, "sector": "Internet/Media","holder": "Airbnb Inc.",              "score": 52, "source": "Brand Finance Global 500 2024"},

    # ── Product / platform names (C3) — registered trademarks independent of ──
    # ── parent company name; high LRO risk even if company already listed    ──
    "android":    {"tier": 1, "sector": "Technology",    "holder": "Google LLC (Alphabet Inc.)","score": 70, "source": "USPTO Reg. 3669447; WIPO §6bis; Brand Finance 2024"},
    "windows":    {"tier": 1, "sector": "Technology",    "holder": "Microsoft Corporation",    "score": 70, "source": "USPTO Reg. 1256083; WIPO §6bis; Interbrand 2024"},
    "iphone":     {"tier": 1, "sector": "Technology",    "holder": "Apple Inc.",               "score": 70, "source": "USPTO Reg. 3568439; WIPO §6bis; Interbrand 2024"},
    "ipad":       {"tier": 1, "sector": "Technology",    "holder": "Apple Inc.",               "score": 65, "source": "USPTO Reg. 4044424; WIPO §6bis"},
    "playstation":{"tier": 1, "sector": "Technology",    "holder": "Sony Interactive Entertainment LLC","score": 68,"source": "USPTO Reg. 1922061; WIPO §6bis; Brand Finance 2024"},
    "xbox":       {"tier": 1, "sector": "Technology",    "holder": "Microsoft Corporation",    "score": 65, "source": "USPTO Reg. 2646571; WIPO §6bis"},
    "gmail":      {"tier": 1, "sector": "Technology",    "holder": "Google LLC (Alphabet Inc.)","score": 65, "source": "USPTO Reg. 3141577; Brand Finance 2024"},
    "chatgpt":    {"tier": 1, "sector": "Technology",    "holder": "OpenAI OpCo LLC",          "score": 65, "source": "USPTO App. 98058545; widely known mark 2023–"},
    "openai":     {"tier": 1, "sector": "Technology",    "holder": "OpenAI OpCo LLC",          "score": 65, "source": "USPTO Reg. 6985726; rapidly accruing §6bis status"},
    "snapchat":   {"tier": 2, "sector": "Internet/Media","holder": "Snap Inc.",                "score": 58, "source": "USPTO Reg. 4375712; Brand Finance Global 500 2024"},
    "pinterest":  {"tier": 2, "sector": "Internet/Media","holder": "Pinterest Inc.",           "score": 55, "source": "USPTO Reg. 4145017; Brand Finance Global 500 2024"},
    "wechat":     {"tier": 2, "sector": "Internet/Media","holder": "Tencent Holdings Ltd.",    "score": 58, "source": "Brand Finance Global 500 2024"},
    "telegram":   {"tier": 2, "sector": "Internet/Media","holder": "Telegram Messenger Inc.",  "score": 52, "source": "USPTO Reg. 5261517; widely-known platform mark"},

    # ── Automotive ─────────────────────────────────────────────────────────
    "toyota":     {"tier": 1, "sector": "Automotive",    "holder": "Toyota Motor Corporation", "score": 75, "source": "Interbrand #6 2024; WIPO §6bis"},
    "mercedes":   {"tier": 1, "sector": "Automotive",    "holder": "Mercedes-Benz Group AG",   "score": 72, "source": "Interbrand #8 2024; WIPO §6bis"},
    "bmw":        {"tier": 1, "sector": "Automotive",    "holder": "Bayerische Motoren Werke AG","score": 72,"source": "Interbrand #11 2024; WIPO §6bis"},
    "honda":      {"tier": 1, "sector": "Automotive",    "holder": "Honda Motor Co. Ltd.",     "score": 68, "source": "Interbrand 2024; WIPO §6bis"},
    "volkswagen": {"tier": 1, "sector": "Automotive",    "holder": "Volkswagen AG",            "score": 68, "source": "Interbrand 2024"},
    "ford":       {"tier": 1, "sector": "Automotive",    "holder": "Ford Motor Company",       "score": 65, "source": "Interbrand 2024; WIPO §6bis"},
    "tesla":      {"tier": 1, "sector": "Automotive",    "holder": "Tesla Inc.",               "score": 68, "source": "Interbrand #9 2024"},
    "hyundai":    {"tier": 2, "sector": "Automotive",    "holder": "Hyundai Motor Company",    "score": 58, "source": "Interbrand 2024"},
    "nissan":     {"tier": 2, "sector": "Automotive",    "holder": "Nissan Motor Co. Ltd.",    "score": 58, "source": "Brand Finance Global 500 2024"},
    "porsche":    {"tier": 2, "sector": "Automotive",    "holder": "Porsche AG",               "score": 60, "source": "Interbrand 2024"},
    "audi":       {"tier": 2, "sector": "Automotive",    "holder": "Audi AG",                  "score": 58, "source": "Interbrand 2024"},
    "ferrari":    {"tier": 2, "sector": "Automotive",    "holder": "Ferrari N.V.",             "score": 60, "source": "Brand Finance Global 500 2024"},
    "chevrolet":  {"tier": 2, "sector": "Automotive",    "holder": "General Motors Company",   "score": 55, "source": "Brand Finance Global 500 2024"},
    "jeep":       {"tier": 2, "sector": "Automotive",    "holder": "Stellantis N.V.",          "score": 55, "source": "Brand Finance Global 500 2024"},
    "subaru":     {"tier": 3, "sector": "Automotive",    "holder": "Subaru Corporation",       "score": 45, "source": "Brand Finance Global 500 2024"},
    "volvo":      {"tier": 2, "sector": "Automotive",    "holder": "Volvo Car AB",             "score": 55, "source": "Brand Finance Global 500 2024"},
    "kia":        {"tier": 2, "sector": "Automotive",    "holder": "Kia Corporation",          "score": 52, "source": "Brand Finance Global 500 2024"},

    # ── Consumer Goods / FMCG ─────────────────────────────────────────────
    "cocacola":   {"tier": 1, "sector": "Beverages",     "holder": "The Coca-Cola Company",    "score": 72, "source": "Interbrand #7 2024; WIPO §6bis"},
    "nike":       {"tier": 1, "sector": "Apparel",       "holder": "Nike Inc.",                "score": 72, "source": "Interbrand #13 2024; WIPO §6bis"},
    "pepsi":      {"tier": 1, "sector": "Beverages",     "holder": "PepsiCo Inc.",             "score": 65, "source": "Brand Finance Global 500 2024; WIPO §6bis"},
    "nestle":     {"tier": 1, "sector": "Food/Beverages","holder": "Nestlé S.A.",              "score": 65, "source": "Brand Finance Global 500 2024"},
    "adidas":     {"tier": 1, "sector": "Apparel",       "holder": "Adidas AG",               "score": 68, "source": "Interbrand 2024; WIPO §6bis"},
    "gucci":      {"tier": 1, "sector": "Luxury",        "holder": "Kering S.A.",              "score": 68, "source": "Interbrand 2024; WIPO §6bis"},
    "chanel":     {"tier": 1, "sector": "Luxury",        "holder": "Chanel S.A.",              "score": 70, "source": "Brand Finance Global 500 2024; WIPO §6bis"},
    "hermes":     {"tier": 1, "sector": "Luxury",        "holder": "Hermès International S.A.","score": 70, "source": "Brand Finance Global 500 2024; WIPO §6bis"},
    "prada":      {"tier": 2, "sector": "Luxury",        "holder": "Prada S.p.A.",             "score": 58, "source": "Brand Finance Global 500 2024"},
    "rolex":      {"tier": 1, "sector": "Luxury",        "holder": "Rolex S.A.",               "score": 68, "source": "Brand Finance Global 500 2024; WIPO §6bis"},
    "lvmh":       {"tier": 2, "sector": "Luxury",        "holder": "LVMH Moët Hennessy",       "score": 60, "source": "Brand Finance Global 500 2024"},
    "zara":       {"tier": 2, "sector": "Apparel",       "holder": "Inditex S.A.",             "score": 58, "source": "Interbrand 2024"},
    "ikea":       {"tier": 1, "sector": "Retail",        "holder": "Inter IKEA Systems B.V.",  "score": 65, "source": "Interbrand 2024; WIPO §6bis"},
    "unilever":   {"tier": 2, "sector": "Consumer Goods","holder": "Unilever PLC",             "score": 55, "source": "Brand Finance Global 500 2024"},
    "loreal":     {"tier": 2, "sector": "Consumer Goods","holder": "L'Oréal S.A.",             "score": 58, "source": "Brand Finance Global 500 2024"},
    "gillette":   {"tier": 2, "sector": "Consumer Goods","holder": "Procter & Gamble Co.",     "score": 55, "source": "Brand Finance Global 500 2024; WIPO §6bis"},
    "pampers":    {"tier": 2, "sector": "Consumer Goods","holder": "Procter & Gamble Co.",     "score": 52, "source": "Brand Finance Global 500 2024"},
    "dove":       {"tier": 2, "sector": "Consumer Goods","holder": "Unilever PLC",             "score": 50, "source": "Brand Finance Global 500 2024"},
    "lego":       {"tier": 1, "sector": "Toys",          "holder": "Lego A/S",                 "score": 65, "source": "Brand Finance Global 500 2024; WIPO §6bis"},

    # ── Retail / E-commerce ────────────────────────────────────────────────
    "walmart":    {"tier": 1, "sector": "Retail",        "holder": "Walmart Inc.",             "score": 68, "source": "Brand Finance #1 2024"},
    "target":     {"tier": 2, "sector": "Retail",        "holder": "Target Corporation",       "score": 55, "source": "Brand Finance Global 500 2024"},
    "costco":     {"tier": 2, "sector": "Retail",        "holder": "Costco Wholesale Corp.",   "score": 52, "source": "Brand Finance Global 500 2024"},
    "aliexpress": {"tier": 2, "sector": "Retail",        "holder": "Alibaba Group Holding",    "score": 55, "source": "Brand Finance Global 500 2024"},
    "alibaba":    {"tier": 1, "sector": "Retail/Tech",   "holder": "Alibaba Group Holding",    "score": 65, "source": "Brand Finance #9 2024"},
    "shopify":    {"tier": 2, "sector": "Retail/Tech",   "holder": "Shopify Inc.",             "score": 52, "source": "Brand Finance Global 500 2024"},

    # ── Financial Services ─────────────────────────────────────────────────
    "visa":       {"tier": 1, "sector": "Financial",     "holder": "Visa Inc.",                "score": 72, "source": "Interbrand 2024; WIPO §6bis"},
    "mastercard": {"tier": 1, "sector": "Financial",     "holder": "Mastercard Inc.",          "score": 68, "source": "Interbrand 2024; WIPO §6bis"},
    "amex":       {"tier": 1, "sector": "Financial",     "holder": "American Express Company", "score": 65, "source": "Interbrand 2024"},
    "hsbc":       {"tier": 1, "sector": "Financial",     "holder": "HSBC Holdings plc",        "score": 65, "source": "Brand Finance Global 500 2024"},
    "jpmorgan":   {"tier": 2, "sector": "Financial",     "holder": "JPMorgan Chase & Co.",     "score": 58, "source": "Brand Finance Global 500 2024"},
    "chase":      {"tier": 2, "sector": "Financial",     "holder": "JPMorgan Chase & Co.",     "score": 58, "source": "Brand Finance Global 500 2024"},
    "citibank":   {"tier": 2, "sector": "Financial",     "holder": "Citigroup Inc.",           "score": 58, "source": "Brand Finance Global 500 2024"},
    "goldman":    {"tier": 2, "sector": "Financial",     "holder": "Goldman Sachs Group Inc.", "score": 55, "source": "Brand Finance Global 500 2024"},
    "barclays":   {"tier": 2, "sector": "Financial",     "holder": "Barclays PLC",             "score": 55, "source": "Brand Finance Global 500 2024"},
    "blackrock":  {"tier": 2, "sector": "Financial",     "holder": "BlackRock Inc.",           "score": 52, "source": "Brand Finance Global 500 2024"},
    "allianz":    {"tier": 2, "sector": "Financial",     "holder": "Allianz SE",               "score": 55, "source": "Brand Finance Global 500 2024"},
    "axa":        {"tier": 2, "sector": "Financial",     "holder": "AXA S.A.",                 "score": 55, "source": "Brand Finance Global 500 2024"},
    "ing":        {"tier": 2, "sector": "Financial",     "holder": "ING Group N.V.",           "score": 52, "source": "Brand Finance Global 500 2024"},
    "stripe":     {"tier": 2, "sector": "Financial",     "holder": "Stripe Inc.",              "score": 52, "source": "Brand Finance Global 500 2024"},

    # ── Pharma / Healthcare ────────────────────────────────────────────────
    "pfizer":     {"tier": 1, "sector": "Pharma",        "holder": "Pfizer Inc.",              "score": 65, "source": "Brand Finance Global 500 2024"},
    "roche":      {"tier": 1, "sector": "Pharma",        "holder": "Roche Holding AG",         "score": 62, "source": "Brand Finance Global 500 2024"},
    "novartis":   {"tier": 2, "sector": "Pharma",        "holder": "Novartis AG",              "score": 58, "source": "Brand Finance Global 500 2024"},
    "johnson":    {"tier": 1, "sector": "Pharma/FMCG",   "holder": "Johnson & Johnson",        "score": 65, "source": "Interbrand 2024; WIPO §6bis"},
    "bayer":      {"tier": 2, "sector": "Pharma",        "holder": "Bayer AG",                 "score": 58, "source": "Brand Finance Global 500 2024"},
    "astrazeneca":{"tier": 2, "sector": "Pharma",        "holder": "AstraZeneca PLC",          "score": 55, "source": "Brand Finance Global 500 2024"},
    "abbott":     {"tier": 2, "sector": "Pharma",        "holder": "Abbott Laboratories",      "score": 52, "source": "Brand Finance Global 500 2024"},
    "medtronic":  {"tier": 2, "sector": "Pharma",        "holder": "Medtronic plc",            "score": 52, "source": "Brand Finance Global 500 2024"},

    # ── Energy ─────────────────────────────────────────────────────────────
    "shell":      {"tier": 1, "sector": "Energy",        "holder": "Shell plc",                "score": 65, "source": "Brand Finance #11 2024; WIPO §6bis"},
    "bp":         {"tier": 1, "sector": "Energy",        "holder": "BP plc",                   "score": 62, "source": "Brand Finance Global 500 2024"},
    "exxon":      {"tier": 1, "sector": "Energy",        "holder": "ExxonMobil Corporation",   "score": 62, "source": "Brand Finance Global 500 2024"},
    "chevron":    {"tier": 2, "sector": "Energy",        "holder": "Chevron Corporation",      "score": 55, "source": "Brand Finance Global 500 2024"},
    "total":      {"tier": 2, "sector": "Energy",        "holder": "TotalEnergies SE",         "score": 52, "source": "Brand Finance Global 500 2024"},

    # ── Food & Beverage ────────────────────────────────────────────────────
    "mcdonalds":  {"tier": 1, "sector": "Food Service",  "holder": "McDonald's Corporation",   "score": 70, "source": "Interbrand #10 2024; WIPO §6bis"},
    "starbucks":  {"tier": 1, "sector": "Food Service",  "holder": "Starbucks Corporation",    "score": 65, "source": "Interbrand 2024; WIPO §6bis"},
    "nescafe":    {"tier": 2, "sector": "Beverages",     "holder": "Nestlé S.A.",              "score": 55, "source": "Brand Finance Global 500 2024; WIPO §6bis"},
    "heineken":   {"tier": 2, "sector": "Beverages",     "holder": "Heineken N.V.",            "score": 55, "source": "Brand Finance Global 500 2024"},
    "budweiser":  {"tier": 2, "sector": "Beverages",     "holder": "Anheuser-Busch InBev",     "score": 55, "source": "Brand Finance Global 500 2024"},
    "redbull":    {"tier": 2, "sector": "Beverages",     "holder": "Red Bull GmbH",            "score": 55, "source": "Brand Finance Global 500 2024"},
    "nespresso":  {"tier": 2, "sector": "Beverages",     "holder": "Nestlé S.A.",              "score": 52, "source": "Brand Finance Global 500 2024"},
    "kellog":     {"tier": 2, "sector": "Food",          "holder": "Kellanova",                "score": 50, "source": "Brand Finance Global 500 2024"},

    # ── Telecoms ───────────────────────────────────────────────────────────
    "att":        {"tier": 1, "sector": "Telecom",       "holder": "AT&T Inc.",                "score": 65, "source": "Brand Finance #8 2024"},
    "verizon":    {"tier": 1, "sector": "Telecom",       "holder": "Verizon Communications",   "score": 65, "source": "Interbrand 2024"},
    "tmobile":    {"tier": 2, "sector": "Telecom",       "holder": "T-Mobile US Inc.",         "score": 58, "source": "Brand Finance Global 500 2024"},
    "vodafone":   {"tier": 1, "sector": "Telecom",       "holder": "Vodafone Group plc",       "score": 65, "source": "Brand Finance Global 500 2024; WIPO §6bis"},
    "deutsche":   {"tier": 2, "sector": "Telecom",       "holder": "Deutsche Telekom AG",      "score": 55, "source": "Brand Finance Global 500 2024"},
    "orange":     {"tier": 2, "sector": "Telecom",       "holder": "Orange S.A.",              "score": 52, "source": "Brand Finance Global 500 2024"},

    # ── ICANN 2012 LRO-contested strings (direct precedent) ────────────────
    "amazon":     {"tier": 1, "sector": "Retail/Tech",   "holder": "Amazon.com Inc.",          "score": 75, "source": "ICANN 2012 LRO decision; Interbrand 2024"},
    "apple":      {"tier": 1, "sector": "Technology",    "holder": "Apple Inc.",               "score": 75, "source": "ICANN 2012 LRO decision; Interbrand 2024"},
    "microsoft":  {"tier": 1, "sector": "Technology",    "holder": "Microsoft Corporation",    "score": 75, "source": "ICANN 2012 LRO decision; Interbrand 2024"},
    "nike":       {"tier": 1, "sector": "Apparel",       "holder": "Nike Inc.",                "score": 72, "source": "ICANN 2012 LRO decision; Interbrand 2024"},
    "walmart":    {"tier": 1, "sector": "Retail",        "holder": "Walmart Inc.",             "score": 68, "source": "ICANN 2012 LRO decision; Brand Finance 2024"},
    "google":     {"tier": 1, "sector": "Technology",    "holder": "Alphabet Inc.",            "score": 75, "source": "ICANN 2012 LRO decision; Interbrand 2024"},
}

# Build a flat index: label (lowercase) → entry
_INDEX: dict[str, dict] = {k.lower(): v for k, v in _BRANDS.items()}

# Tier-1 set for edit-distance checks (only run against the highest-exposure brands)
_TIER1: set[str] = {k for k, v in _INDEX.items() if v["tier"] == 1}


def _levenshtein(a: str, b: str) -> int:
    """Edit distance with early exit at distance > 1."""
    if abs(len(a) - len(b)) > 1:
        return 99
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            curr.append(min(prev[j] + (ca != cb), prev[j + 1] + 1, curr[j] + 1))
        prev = curr
    return prev[-1]


def check(s: str) -> list[dict]:
    """
    Return LRO risk signals for *s*.

    Each hit dict has:
        brand       – the matched brand label
        holder      – rights holder
        sector      – industry sector
        tier        – 1 (top-50) / 2 (51-200) / 3 (regional)
        match_type  – 'exact' | 'edit_distance_1'
        score       – LRO risk score contribution
        source      – source reference
    """
    s = s.lower().strip()
    hits: list[dict] = []
    seen: set[str] = set()

    # 1 — Exact match
    if s in _INDEX:
        e = _INDEX[s]
        hits.append({
            "brand":      s,
            "holder":     e["holder"],
            "sector":     e["sector"],
            "tier":       e["tier"],
            "match_type": "exact",
            "score":      e["score"],
            "source":     e["source"],
        })
        seen.add(s)

    # 2 — Edit-distance ≤ 1 against tier-1 brands (skip if already exact-matched)
    for brand in _TIER1:
        if brand in seen:
            continue
        if len(s) < 3 or len(brand) < 3:
            continue
        if _levenshtein(s, brand) <= 1:
            e = _INDEX[brand]
            hits.append({
                "brand":      brand,
                "holder":     e["holder"],
                "sector":     e["sector"],
                "tier":       e["tier"],
                "match_type": "edit_distance_1",
                "score":      max(40, e["score"] - 15),
                "source":     e["source"],
            })
            seen.add(brand)

    # Sort: exact first, then by descending score
    hits.sort(key=lambda h: (h["match_type"] != "exact", -h["score"]))
    return hits
