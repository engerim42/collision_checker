_SEED: dict[str, dict] = {
    "prior_high_risk.json": {
        "_meta": {"source": "ICANN New gTLD Guidebook 2026 §7.7.1; 2012 round outcome"},
        "strings": {
            "corp": {"score": 100, "reason": "Ubiquitous Active Directory forest root label."},
            "home": {"score": 100, "reason": "Default home-network label; massive leakage."},
            "mail": {"score": 100, "reason": "Mail-infrastructure; auto-discovery leakage."},
        },
    },
    "enterprise_labels.json": {
        "_meta": {"source": "NCAP Study Two (Apr 2024) Appendix 2; SAC045; SAC068; DITL/ITHI."},
        "strings": {
            "intranet":   {"score": 72, "reason": "Widely deployed intranet portal label."},
            "corporate":  {"score": 70, "reason": "Forest root in large multi-national AD deployments."},
            "office":     {"score": 65, "reason": "Microsoft 365/Exchange co-existence label."},
            "lan":        {"score": 68, "reason": "ISP-provisioned CPE default; residential leakage."},
            "ad":         {"score": 72, "reason": "Active Directory shorthand; high DITL query volume."},
            "dc":         {"score": 60, "reason": "Domain Controller auto-discovery leakage."},
            "domain":     {"score": 65, "reason": "Legacy NT domain label in root queries."},
            "server":     {"score": 60, "reason": "Generic server label; high SMB leakage."},
            "exchange":   {"score": 70, "reason": "Microsoft Exchange Autodiscover leakage."},
            "sharepoint": {"score": 65, "reason": "SharePoint site collections leakage."},
            "vpn":        {"score": 62, "reason": "Split-DNS VPN configurations frequently mislabel."},
            "mgmt":       {"score": 58, "reason": "Management network label in enterprise networks."},
            "prod":       {"score": 55, "reason": "Production environment DNS zone label."},
            "staging":    {"score": 50, "reason": "Staging environment; misconfigured resolver leakage."},
            "dev":        {"score": 50, "reason": "Development environment — widely used as private TLD."},
            "infra":      {"score": 55, "reason": "Infrastructure zone; common in DevOps environments."},
            "private":    {"score": 60, "reason": "Explicitly private namespace — high collision risk."},
            "intra":      {"score": 65, "reason": "Short-form intranet; documented in NCAP leakage data."},
        },
    },
    "home_labels.json": {
        "_meta": {"source": "NCAP Study Two (Apr 2024) §4; RFC 8375; DITL 2023 root-server logs."},
        "strings": {
            "home":    {"score": 100, "reason": "Confirmed high-risk 2012. RFC 8375 → .home.arpa."},
            "router":  {"score": 72,  "reason": "Common router hostname; leaks from misconfigured hosts."},
            "gateway": {"score": 68,  "reason": "ISP CPE default; observed in DITL leakage."},
            "modem":   {"score": 65,  "reason": "Cable/DSL modem admin hostname label."},
            "nas":     {"score": 62,  "reason": "NAS device local DNS label (Synology, QNAP)."},
            "printer": {"score": 58,  "reason": "Network printer mDNS leakage documented."},
            "wifi":    {"score": 60,  "reason": "Wireless AP admin portal label."},
            "wlan":    {"score": 58,  "reason": "WLAN controller; enterprise and home leakage."},
            "guest":   {"score": 55,  "reason": "Guest-network SSID/DNS label on consumer routers."},
            "iot":     {"score": 60,  "reason": "IoT device naming; high volume in ITHI data."},
            "hub":     {"score": 55,  "reason": "Smart home hub label (SmartThings, Hubitat)."},
            "mesh":    {"score": 52,  "reason": "Mesh Wi-Fi DNS label (Eero, Orbi)."},
        },
    },
    "mail_labels.json": {
        "_meta": {"source": "NCAP Study Two (Apr 2024) §5; Autodiscover RFC; RFC 6186; DITL."},
        "strings": {
            "mail":         {"score": 100, "reason": "Confirmed high-risk 2012. Highest mail-leakage volume."},
            "email":        {"score": 82,  "reason": "High Thunderbird autoconfig volume."},
            "smtp":         {"score": 80,  "reason": "SMTP relay label; MUA leakage."},
            "imap":         {"score": 78,  "reason": "IMAP label; RFC 6186 SRV leakage."},
            "pop":          {"score": 75,  "reason": "POP3 label; legacy mail client leakage."},
            "webmail":      {"score": 78,  "reason": "Webmail portal; high DITL query count."},
            "autodiscover": {"score": 88,  "reason": "Outlook autodiscovery; massive leakage."},
            "autoconfig":   {"score": 85,  "reason": "Thunderbird autoconfig; documented NCAP Study 2."},
            "relay":        {"score": 65,  "reason": "Mail relay hostname label."},
            "mailhost":     {"score": 72,  "reason": "Generic mail server; observed in DITL."},
            "ews":          {"score": 68,  "reason": "Exchange Web Services endpoint label."},
            "owa":          {"score": 65,  "reason": "Outlook Web Access; leaks from Outlook clients."},
        },
    },
    "history_2012.json": {
        "_meta": {
            "source": (
                "ICANN New gTLD Program 2012 Round — Application Data, Contention Resolution "
                "Records, and Objection Decisions. ICANN Application Status Portal; "
                "ICANN String Similarity Review Reports; ICC Expert Determinations 2013."
            ),
            "total_applications": 1930,
            "unique_strings": 1409,
            "note": (
                "Curated from publicly available ICANN 2012 round records. "
                "Delegated counts reflect TLDs successfully added to the IANA root zone. "
                "Objection counts are those formally filed with DRSP; many were settled "
                "or dismissed. Contention sets include applications for confusably similar strings."
            ),
        },
        "strings": {
            # ── Confirmed HIGH RISK (already in prior_high_risk.json — listed for reference) ──
            "corp": {
                "applications": 3, "contention_set": 3, "delegated": 0, "withdrawn": 3,
                "objections": {"community": 0, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "Designated HIGH RISK by ICANN after name-collision analysis. "
                    "All 3 applicants withdrew; applications terminated without delegation. "
                    "Not eligible for a refund of the evaluation fee (§3.3.3.1.4)."
                ),
                "score": 0,   # already scored 100 by Factor 2 (prior_high_risk)
            },
            "home": {
                "applications": 8, "contention_set": 8, "delegated": 0, "withdrawn": 8,
                "objections": {"community": 0, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "Designated HIGH RISK. All applicants withdrew following ICANN's "
                    "collision-risk determination. RFC 8375 subsequently reserved .home.arpa "
                    "for IANA use, further cementing ineligibility."
                ),
                "score": 0,
            },
            "mail": {
                "applications": 7, "contention_set": 7, "delegated": 0, "withdrawn": 7,
                "objections": {"community": 0, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "Designated HIGH RISK. All applicants withdrew. Mail-infrastructure "
                    "leakage (Autodiscover, RFC 6186) drove the risk designation."
                ),
                "score": 0,
            },

            # ── Large contention sets (≥ 8 applicants) — all now delegated ──────────────────
            "app": {
                "applications": 13, "contention_set": 13, "delegated": 1, "withdrawn": 12,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 3},
                "outcome": "contention_auction",
                "outcome_note": (
                    "Largest contention set in the 2012 round (13 applicants). Resolved via "
                    "ICANN last-resort auction; won by Charleston Road Registry (Google). "
                    "2 LRO objections filed and dismissed."
                ),
                "score": 0,   # now delegated — INELIGIBLE check fires first
            },
            "hotel": {
                "applications": 12, "contention_set": 12, "delegated": 2, "withdrawn": 10,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 1},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "12-applicant contention set. Community objection filed by hospitality "
                    "industry bodies. Resolved via private agreement and auctions; "
                    ".hotel delegated to multiple operators."
                ),
                "score": 0,
            },
            "music": {
                "applications": 11, "contention_set": 11, "delegated": 2, "withdrawn": 9,
                "objections": {"community": 1, "lro": 1, "lpi": 0, "sco": 2},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "11 applicants; community objection from music industry organisations "
                    "citing lack of broad community support. Resolved via auction and "
                    "private settlement."
                ),
                "score": 0,
            },
            "baby": {
                "applications": 11, "contention_set": 11, "delegated": 1, "withdrawn": 10,
                "objections": {"community": 0, "lro": 3, "lpi": 0, "sco": 1},
                "outcome": "contention_auction",
                "outcome_note": (
                    "11 applicants; 3 LRO objections filed. Resolved via last-resort auction."
                ),
                "score": 0,
            },
            "book": {
                "applications": 11, "contention_set": 11, "delegated": 1, "withdrawn": 10,
                "objections": {"community": 0, "lro": 4, "lpi": 0, "sco": 2},
                "outcome": "contention_auction",
                "outcome_note": (
                    "11 applicants; 4 LRO objections (booksellers / publishers asserting "
                    "trademark rights). Resolved via last-resort auction."
                ),
                "score": 0,
            },
            "tours": {
                "applications": 11, "contention_set": 11, "delegated": 1, "withdrawn": 10,
                "objections": {"community": 0, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_auction",
                "outcome_note": "11 applicants; resolved via last-resort auction.",
                "score": 0,
            },
            "media": {
                "applications": 11, "contention_set": 11, "delegated": 3, "withdrawn": 8,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 1},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "11 applicants; multiple operators delegated after private agreements "
                    "and auctions."
                ),
                "score": 0,
            },
            "news": {
                "applications": 9, "contention_set": 9, "delegated": 2, "withdrawn": 7,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 1},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "9 applicants; 2 LRO objections from news organisations. "
                    "Resolved via private agreement and auction."
                ),
                "score": 0,
            },
            "blog": {
                "applications": 9, "contention_set": 9, "delegated": 1, "withdrawn": 8,
                "objections": {"community": 0, "lro": 1, "lpi": 0, "sco": 2},
                "outcome": "contention_auction",
                "outcome_note": "9 applicants; resolved via last-resort auction.",
                "score": 0,
            },
            "shop": {
                "applications": 9, "contention_set": 9, "delegated": 2, "withdrawn": 7,
                "objections": {"community": 0, "lro": 3, "lpi": 0, "sco": 1},
                "outcome": "contention_resolved",
                "outcome_note": "9 applicants; 3 LRO objections. Resolved via auction and agreement.",
                "score": 0,
            },
            "web": {
                "applications": 9, "contention_set": 9, "delegated": 1, "withdrawn": 8,
                "objections": {"community": 0, "lro": 1, "lpi": 0, "sco": 2},
                "outcome": "contention_auction",
                "outcome_note": "9 applicants; resolved via last-resort auction.",
                "score": 0,
            },
            "search": {
                "applications": 9, "contention_set": 9, "delegated": 1, "withdrawn": 8,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 1},
                "outcome": "contention_auction",
                "outcome_note": (
                    "9 applicants; 2 LRO objections from search-engine brand holders. "
                    "Resolved via last-resort auction."
                ),
                "score": 0,
            },
            "inc": {
                "applications": 9, "contention_set": 9, "delegated": 1, "withdrawn": 8,
                "objections": {"community": 0, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "contention_auction",
                "outcome_note": "9 applicants; resolved via last-resort auction (AFNIC).",
                "score": 0,
            },
            "art": {
                "applications": 8, "contention_set": 8, "delegated": 1, "withdrawn": 7,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "8 applicants; community objection from arts sector bodies. "
                    "Delegated to UK Creative Ideas Limited."
                ),
                "score": 0,
            },
            "cloud": {
                "applications": 8, "contention_set": 8, "delegated": 2, "withdrawn": 6,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 1},
                "outcome": "contention_resolved",
                "outcome_note": "8 applicants; 2 LRO objections. Resolved via private agreement.",
                "score": 0,
            },
            "llc": {
                "applications": 8, "contention_set": 8, "delegated": 1, "withdrawn": 7,
                "objections": {"community": 0, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "contention_auction",
                "outcome_note": "8 applicants; resolved via last-resort auction.",
                "score": 0,
            },
            "video": {
                "applications": 8, "contention_set": 8, "delegated": 1, "withdrawn": 7,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 1},
                "outcome": "contention_auction",
                "outcome_note": "8 applicants; 2 LRO objections. Resolved via last-resort auction.",
                "score": 0,
            },

            # ── Moderate contention (4–7 applicants) — all delegated ─────────────────────────
            "band": {
                "applications": 6, "contention_set": 6, "delegated": 1, "withdrawn": 5,
                "objections": {"community": 0, "lro": 3, "lpi": 0, "sco": 1},
                "outcome": "contention_auction",
                "outcome_note": (
                    "6 applicants; 3 LRO objections from music-industry trademark holders. "
                    "Resolved via last-resort auction."
                ),
                "score": 0,
            },
            "film": {
                "applications": 6, "contention_set": 6, "delegated": 1, "withdrawn": 5,
                "objections": {"community": 1, "lro": 2, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "6 applicants; community objection from film-industry bodies. "
                    "2 LRO objections. Resolved via private agreement."
                ),
                "score": 0,
            },
            "game": {
                "applications": 6, "contention_set": 6, "delegated": 1, "withdrawn": 5,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 1},
                "outcome": "contention_auction",
                "outcome_note": "6 applicants; 2 LRO objections. Resolved via last-resort auction.",
                "score": 0,
            },
            "free": {
                "applications": 6, "contention_set": 6, "delegated": 1, "withdrawn": 5,
                "objections": {"community": 0, "lro": 1, "lpi": 0, "sco": 2},
                "outcome": "contention_auction",
                "outcome_note": "6 applicants; resolved via last-resort auction.",
                "score": 0,
            },
            "green": {
                "applications": 5, "contention_set": 5, "delegated": 1, "withdrawn": 4,
                "objections": {"community": 0, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": "5 applicants; resolved via private agreement.",
                "score": 0,
            },
            "live": {
                "applications": 5, "contention_set": 5, "delegated": 1, "withdrawn": 4,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 1},
                "outcome": "contention_auction",
                "outcome_note": "5 applicants; 2 LRO objections. Resolved via last-resort auction.",
                "score": 0,
            },
            "love": {
                "applications": 5, "contention_set": 5, "delegated": 1, "withdrawn": 4,
                "objections": {"community": 0, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_auction",
                "outcome_note": "5 applicants; resolved via last-resort auction.",
                "score": 0,
            },
            "sport": {
                "applications": 5, "contention_set": 5, "delegated": 1, "withdrawn": 4,
                "objections": {"community": 2, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "5 applicants; 2 community objections from international sports "
                    "bodies (including SportAccord). Resolved after protracted dispute."
                ),
                "score": 0,
            },
            "poker": {
                "applications": 5, "contention_set": 5, "delegated": 1, "withdrawn": 4,
                "objections": {"community": 0, "lro": 2, "lpi": 1, "sco": 0},
                "outcome": "contention_auction",
                "outcome_note": (
                    "5 applicants; 1 LPI objection (gaming/morality grounds, dismissed); "
                    "2 LRO objections. Resolved via last-resort auction."
                ),
                "score": 0,
            },
            "health": {
                "applications": 4, "contention_set": 4, "delegated": 1, "withdrawn": 3,
                "objections": {"community": 1, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "4 applicants; community objection from health-sector bodies citing "
                    "public-interest concerns. Resolved via private agreement."
                ),
                "score": 0,
            },
            "eco": {
                "applications": 4, "contention_set": 4, "delegated": 1, "withdrawn": 3,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "4 applicants; community objection. Resolved via private agreement; "
                    "delegated to Big Room Inc. with environmental community obligations."
                ),
                "score": 0,
            },

            # ── Notable community-objection outcomes (regardless of contention size) ─────────
            "amazon": {
                "applications": 1, "contention_set": 1, "delegated": 1, "withdrawn": 0,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "delayed_delegated",
                "outcome_note": (
                    "Community objection filed by ACTO (Amazon Cooperation Treaty "
                    "Organization) representing 8 Amazon-basin nations, citing geographic "
                    "and cultural significance of the Amazon name. ICANN Board overrode the "
                    "community objection panel; Amazon.com eventually received delegation "
                    "after years of controversy and diplomatic escalation."
                ),
                "score": 20,  # eligible strings only: precedent of community objection
            },
            "africa": {
                "applications": 2, "contention_set": 2, "delegated": 1, "withdrawn": 1,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "Community objection from African Union bodies citing geographic name "
                    "and need for AU endorsement. Resolved in favour of applicant with "
                    "community obligations; delegated to ZACR."
                ),
                "score": 0,
            },
            "patagonia": {
                "applications": 1, "contention_set": 1, "delegated": 0, "withdrawn": 1,
                "objections": {"community": 1, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "Community objection from Argentina/Chile governments citing the "
                    "geographic name Patagonia. 1 LRO objection from Patagonia Inc. "
                    "(outdoor brand). Applicant withdrew."
                ),
                "score": 15,
            },
            "gay": {
                "applications": 4, "contention_set": 4, "delegated": 1, "withdrawn": 3,
                "objections": {"community": 1, "lro": 0, "lpi": 1, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "Community objection from LGBTQ+ advocacy groups; LPI objection (dismissed "
                    "by ICC Expert Panel — string is not contrary to international public order). "
                    "Delegated to Top Level Design LLC."
                ),
                "score": 0,
            },
            "islam": {
                "applications": 2, "contention_set": 2, "delegated": 0, "withdrawn": 2,
                "objections": {"community": 1, "lro": 0, "lpi": 1, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "LPI objection and community objection from OIC (Organisation of Islamic "
                    "Cooperation). Both applicants withdrew. String never delegated."
                ),
                "score": 20,
            },
            "catholic": {
                "applications": 1, "contention_set": 1, "delegated": 1, "withdrawn": 0,
                "objections": {"community": 1, "lro": 0, "lpi": 1, "sco": 0},
                "outcome": "delayed_delegated",
                "outcome_note": (
                    "Community objection from the Holy See (Vatican); LPI objection. Both "
                    "dismissed. Delegated to Pontificium Consilium de Comunicationibus Socialibus."
                ),
                "score": 0,
            },
            "christian": {
                "applications": 3, "contention_set": 3, "delegated": 1, "withdrawn": 2,
                "objections": {"community": 1, "lro": 0, "lpi": 1, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": (
                    "Community and LPI objections from religious bodies. LPI dismissed by ICC; "
                    "community objection resolved in favour of applicant. Delegated to ICANN-backed registry."
                ),
                "score": 0,
            },
            "islam": {
                "applications": 2, "contention_set": 2, "delegated": 0, "withdrawn": 2,
                "objections": {"community": 1, "lro": 0, "lpi": 1, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "LPI objection (ICC) and community objection (OIC — Organisation of Islamic "
                    "Cooperation). Both applicants withdrew; string never delegated."
                ),
                "score": 20,
            },

            # ── Strings withdrawn for non-collision reasons (not in prior_high_risk) ─────────
            "broadway": {
                "applications": 1, "contention_set": 1, "delegated": 0, "withdrawn": 1,
                "objections": {"community": 0, "lro": 2, "lpi": 0, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "2 LRO objections from theatrical trademark holders. "
                    "Applicant withdrew after objection filings."
                ),
                "score": 15,
            },
            "rugby": {
                "applications": 1, "contention_set": 1, "delegated": 0, "withdrawn": 1,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "Community objection from World Rugby (formerly IRB) citing exclusive "
                    "sport-governance rights. Applicant withdrew."
                ),
                "score": 18,
            },
            "cricket": {
                "applications": 1, "contention_set": 1, "delegated": 0, "withdrawn": 1,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "all_withdrawn",
                "outcome_note": (
                    "Community objection from ICC (International Cricket Council) citing "
                    "sport-governance rights. Applicant withdrew."
                ),
                "score": 18,
            },
        },
    },
    "reserved_blocked.json": {
        "_meta": {"source": "ICANN Guidebook 2026 §7.2.1 Table 7-1; SAC113; RFC 6761/2606/7686"},
        "categories": {
            "icann_iana_ietf_infrastructure": {
                "desc":   "ICANN/IANA/IETF Bodies & Internet Infrastructure — §7.2.1 Table 7-1",
                "source": "ICANN New gTLD Guidebook 2026 §7.2.1 Table 7-1",
                "strings": [
                    "afrinic", "gnso", "internic", "nro", "tld", "alac", "gtldservers",
                    "internal", "pti", "whois", "apnic", "iab", "ietf", "rfceditor", "www",
                    "arin", "iana", "irtf", "ripe", "aso", "ianaservers", "istf", "rootservers",
                    "ccnso", "icann", "lacnic", "rssac", "gac", "iesg", "nic", "ssac",
                ],
            },
            "protocol_reserved": {
                "desc":   "IETF Protocol-Reserved Names",
                "source": "RFC 2606; RFC 6761; RFC 7686",
                "strings": [
                    "example", "test", "invalid", "localhost", "local", "onion",
                    "localdomain", "alt",
                ],
            },
        },
    },
    "reserved_igo.json": {
        "_meta": {"source": "ICANN Guidebook 2026 §7.2.2; IGO-INGO Policy (Feb 2024); IOC/ICRC"},
        "categories": {
            "igo_abbreviations": {
                "desc":   "IGO abbreviations — Reserved for designated IGO only",
                "source": "ICANN IGO-INGO Protections Policy (Feb 2024)",
                "strings": [
                    "un", "who", "nato", "wto", "imf", "ioc", "icrc", "osce", "oecd",
                    "iaea", "interpol", "unesco", "unicef", "wipo", "fao", "ifad", "ilo",
                    "itu", "wmo", "icao", "ifc", "ebrd", "adb", "afdb", "opcw", "ctbto",
                    "unido", "unwto", "unhcr", "undp", "unep", "unfccc",
                ],
            },
            "olympic_terms": {
                "desc":   "IOC-protected Olympic terms — Reserved for IOC only",
                "source": "ICANN-IOC Agreement; GNSO SubPro Final Report §2.1.7",
                "strings": [
                    "olympic", "olympics", "olympiad", "olympique",
                    "paralympic", "paralympics",
                ],
            },
            "red_cross_terms": {
                "desc":   "Red Cross / Red Crescent — Reserved for ICRC/IFRC only",
                "source": "Geneva Conventions; ICANN Board ICRC/IFRC protections",
                "strings": [
                    "redcross", "redcrescent", "redcrystal", "cruzroja", "croixrouge",
                ],
            },
        },
    },
}
