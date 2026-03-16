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
                "community_objections": [{"objector": "International Hotel & Restaurant Association (IH&RA) and related hospitality bodies", "grounds": "Lack of broad community support from hospitality industry", "outcome": "withdrawn_before_decision", "notes": "Community objection process initiated; most applicants withdrew before panel ruling."}],
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
                "community_objections": [{"objector": "International Federation of the Phonographic Industry (IFPI) / music industry consortia", "grounds": "No community nexus demonstrated; multiple commercial applicants without community backing", "outcome": "withdrawn_before_decision", "notes": "Community objection filed; resolved via private agreement favouring existing rights holders."}],
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
                "community_objections": [{"objector": "Various arts sector bodies including Saatchi & Saatchi Arts Council", "grounds": "Applicant did not represent the global arts community", "outcome": "rejected", "notes": "Panel rejected community objection; delegated to UK Creative Ideas Ltd."}],
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
                "community_objections": [{"objector": "International Federation of Film Producers Associations (FIAPF)", "grounds": "Applicant lacked standing as representative of the global film community", "outcome": "settled", "notes": "LRO + community objection combination. Settled via private agreement."}],
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
                "community_objections": [{"objector": "SportAccord (now Global Association of International Sports Federations, GAISF) / multiple international federations", "grounds": "No single applicant could represent the broad international sports community", "outcome": "settled", "notes": "GAISF ultimately gained control after protracted dispute; delegated 2022."}],
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
                "community_objections": [{"objector": "Various public health bodies and government delegations", "grounds": "Sensitive sector requiring consumer protection safeguards", "outcome": "settled", "notes": "Community objection resolved via private agreement with public-interest obligations."}],
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
                "community_objections": [{"objector": "Various environmental NGOs and consumer advocacy groups", "grounds": "Environmental community not adequately represented by applicant", "outcome": "settled", "notes": "Resolved via private agreement; Big Room Inc. accepted community obligations requiring environmental governance."}],
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
                "community_objections": [{"objector": "ACTO — Amazon Cooperation Treaty Organization (representing 8 Amazon-basin nations: Bolivia, Brazil, Colombia, Ecuador, Guyana, Peru, Suriname, Venezuela)", "grounds": "Geographic name of major pan-national significance; cultural and environmental heritage of Amazon region", "outcome": "rejected", "notes": "ICC Expert Panel upheld community objection. ICANN Board overrode panel recommendation in 2013 and allowed Amazon.com Inc. delegation to proceed after years of controversy."}],
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
                "community_objections": [{"objector": "African Union Commission / DotConnectAfrica Trust", "grounds": "Geographic name of a continent; should be managed by African institutional body", "outcome": "settled", "notes": "Community objection upheld in principle; resolved with ZACR (South Africa) as delegate with community obligations."}],
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
                "community_objections": [{"objector": "Argentine and Chilean governments + environmental groups citing geographic name", "grounds": "Geographic name of binational significance (Patagonia region of Argentina and Chile)", "outcome": "withdrawn_before_decision", "notes": "Combined community + LRO objection. Applicant withdrew; never delegated."}],
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
                "community_objections": [{"objector": "GLAAD / various LGBTQ+ advocacy organisations", "grounds": "Community objection asserting need for LGBTQ+-led governance", "outcome": "rejected", "notes": "Panel rejected community objection on procedural grounds; Top Level Design LLC (LGBTQ+-focused) prevailed."}],
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
                "community_objections": [{"objector": "The Holy See (Vatican City State)", "grounds": "Name of global Catholic community; must be governed by Church authority", "outcome": "rejected", "notes": "Panel rejected both community and LPI objections. Delegated to Pontificium Consilium de Communicationibus Socialibus (Vatican body)."}],
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
                "community_objections": [{"objector": "World Council of Churches / Christian community bodies", "grounds": "Religious community name requiring representative governance", "outcome": "rejected", "notes": "LPI dismissed; community objection rejected. Delegated."}],
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
                "community_objections": [{"objector": "Organisation of Islamic Cooperation (OIC) — 57-member-state body", "grounds": "Religious name of global significance; must be governed by Islamic community bodies", "outcome": "withdrawn_before_decision", "notes": "Combined with LPI objection. Both applicants withdrew before panel ruling."}],
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
                "community_objections": [{"objector": "World Rugby (formerly International Rugby Board, IRB)", "grounds": "Exclusive sport-governance rights; IRB is the sole governing body for rugby globally", "outcome": "upheld", "notes": "Community objection upheld. Applicant withdrew; string never delegated."}],
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
                "community_objections": [{"objector": "International Cricket Council (ICC)", "grounds": "ICC is the exclusive governing body for cricket; applicant had no community nexus", "outcome": "upheld", "notes": "Community objection upheld. Applicant withdrew."}],
            },
            "wine": {
                "applications": 6, "contention_set": 6, "delegated": 1, "withdrawn": 5,
                "objections": {"community": 1, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": "6 applicants. GAC issued early warning from wine-producing nations (France, Italy, Spain, Portugal, Hungary, Czech Republic, Moldova, Slovakia, Switzerland) citing GI protection for wine as a category. Community objection filed citing geographic indication concerns. Resolved via private agreement; .wine delegated to Afilias Ltd.",
                "score": 15,
                "implications": ["GAC early warning from 9 governments on GI grounds precedent applies in 2026.", "Wine-producing nation governments likely to refile early warning for any re-application.", "Applicants must demonstrate GI-sensitivity framework in registry agreement."],
                "community_objections": [{"objector": "Wine-producing nations consortium / EU delegation", "grounds": "Geographic indication protection; TRIPS Art. 23 for wine GIs", "outcome": "withdrawn_before_decision", "notes": "Resolved via private agreement with registry obligations for GI protection."}],
            },
            "vin": {
                "applications": 5, "contention_set": 5, "delegated": 1, "withdrawn": 4,
                "objections": {"community": 1, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": "5 applicants. GAC early warning from same wine-producing nations as .wine (French word for wine). Delegated to Afilias Ltd. (same operator as .wine) after private agreement.",
                "score": 15,
                "implications": ["Same GI concerns as .wine apply; French term for wine has equivalent TRIPS protection concerns.", "Co-managed with .wine registry — any 2026 re-applicant faces same governmental scrutiny."],
                "community_objections": [{"objector": "EU wine-producing nations / France", "grounds": "GI protection for vin (French for wine)", "outcome": "withdrawn_before_decision", "notes": "Resolved alongside .wine community objection process."}],
            },
            "champagne": {
                "applications": 0, "contention_set": 0, "delegated": 0, "withdrawn": 0,
                "objections": {"community": 0, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "no_application",
                "outcome_note": "No application received in 2012 round. However, France and the Comité Champagne pre-emptively signalled through GAC that any application for .champagne would face GI-based objections under TRIPS Art. 23. The champagne GI is among the most aggressively defended worldwide.",
                "score": 15,
                "implications": ["France and Comité Champagne will file GAC early warning and community/LRO objections if applied for.", "TRIPS Art. 23 provides heightened protection for wine GIs — applies globally, not just EU.", "The only plausible applicant is the Comité Champagne or a body it authorises."],
            },
            "tequila": {
                "applications": 1, "contention_set": 1, "delegated": 1, "withdrawn": 0,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "delayed_delegated",
                "outcome_note": "1 application from the Consejo Regulador del Tequila (CRT) — the Mexican regulatory body for tequila. Community objection filed on governance grounds, later resolved. .tequila delegated to CRT after delay. Mexico's government strongly supported the GI protection.",
                "score": 0,
                "implications": ["Delegated to official GI body — re-application only viable for CRT or designated successor.", "Mexico government will file GAC early warning for any third-party application.", "Strong GI protection precedent from 2012 resolution."],
                "community_objections": [{"objector": "Third-party community groups challenging CRT's representative status", "grounds": "Governance concerns about industry body representation", "outcome": "withdrawn_before_decision", "notes": "Resolved; CRT confirmed as appropriate governance body."}],
            },
            "bank": {
                "applications": 3, "contention_set": 3, "delegated": 1, "withdrawn": 2,
                "objections": {"community": 1, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": "3 applicants. GAC issued early warning citing financial stability and consumer protection concerns; several government delegations (including EU member states) flagged the need for regulatory safeguards. Community objection from banking industry bodies. Resolved via private agreement; .bank delegated to fTLD Registry Services LLC with enhanced security requirements.",
                "score": 15,
                "implications": ["Financial regulators in multiple jurisdictions expected to refile GAC early warnings.", "Any 2026 applicant must demonstrate regulatory compliance framework.", "fTLD (banking/finance sector body) is the recognised incumbent and will oppose third-party applications."],
                "community_objections": [{"objector": "Financial Services Roundtable / American Bankers Association", "grounds": "Banking industry requires community-governed registry with enhanced security standards", "outcome": "settled", "notes": "Resolved in favour of fTLD Registry Services LLC with strict registrant verification requirements."}],
            },
            "pharmacy": {
                "applications": 3, "contention_set": 3, "delegated": 1, "withdrawn": 2,
                "objections": {"community": 1, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": "3 applicants. GAC early warning citing public health and drug safety concerns. Community objection from International Pharmaceutical Federation (FIP). Delegated to DotPharmacy LLC with strict registrant verification (must be licensed pharmacy).",
                "score": 15,
                "implications": ["Health/pharma regulators expected to refile early warning in 2026.", "Registrant verification requirements (licensed pharmacies only) are a precedent condition.", "FIP or national pharmacy bodies likely to object to any non-pharmacy-sector applicant."],
                "community_objections": [{"objector": "International Pharmaceutical Federation (FIP)", "grounds": "Pharmacy is a regulated profession; TLD must be restricted to licensed entities to protect public health", "outcome": "settled", "notes": "Delegated with strict registrant eligibility requirements."}],
            },
            "doctor": {
                "applications": 2, "contention_set": 2, "delegated": 1, "withdrawn": 1,
                "objections": {"community": 0, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": "2 applicants. GAC noted concerns about medical professional naming conventions. Resolved via private agreement; delegated to Donuts Inc.",
                "score": 10,
                "implications": ["Medical professional bodies may seek governance conditions in 2026.", "GAC health-sector concerns from 2012 round remain relevant."],
            },
            "hospital": {
                "applications": 2, "contention_set": 2, "delegated": 1, "withdrawn": 1,
                "objections": {"community": 0, "lro": 0, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": "2 applicants. GAC noted healthcare sector sensitivity. Resolved via private agreement; delegated to Ruby Pike LLC (Donuts).",
                "score": 10,
                "implications": ["Healthcare sector GAC sensitivity from 2012 applies to any medical/hospital-adjacent strings."],
            },
            "insurance": {
                "applications": 3, "contention_set": 3, "delegated": 1, "withdrawn": 2,
                "objections": {"community": 1, "lro": 1, "lpi": 0, "sco": 0},
                "outcome": "contention_resolved",
                "outcome_note": "3 applicants. GAC early warning citing financial services regulation; government delegations flagged consumer protection concerns similar to .bank. Community objection from insurance industry bodies. Delegated to fTLD Registry Services LLC.",
                "score": 15,
                "implications": ["Financial regulators expected to refile early warnings.", "fTLD is the incumbent — same position as .bank.", "Insurance regulatory compliance framework required."],
                "community_objections": [{"objector": "Insurance industry associations / fTLD", "grounds": "Regulated financial sector requires industry-governed registry", "outcome": "settled", "notes": "Delegated to fTLD with verifier requirements."}],
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
    "gac_warnings_2012.json": {
        "_meta": {
            "source": (
                "ICANN Governmental Advisory Committee (GAC) Early Warnings — 2012 New gTLD Round. "
                "Published on the ICANN GAC website; incorporated into ICANN Board deliberations 2012–2013. "
                "GAC early warnings are not binding but carry significant weight in ICANN Board decisions "
                "and typically precede formal GAC Advice."
            )
        },
        "strings": {
            "amazon": {
                "warnings": 8, "score": 25, "category": "geographic",
                "governments": ["Bolivia", "Brazil", "Colombia", "Ecuador", "Guyana", "Peru", "Suriname", "Venezuela"],
                "summary": "ACTO (Amazon Cooperation Treaty Organization) member states objected citing geographic and cultural significance of the Amazon River and basin. Among the most prominent GAC actions in the 2012 round."
            },
            "patagonia": {
                "warnings": 2, "score": 20, "category": "geographic",
                "governments": ["Argentina", "Chile"],
                "summary": "Both governments sharing the Patagonia region filed early warnings citing geographic name significance."
            },
            "africa": {
                "warnings": 5, "score": 20, "category": "geographic",
                "governments": ["South Africa", "African Union (multiple member states)"],
                "summary": "African Union member states objected to non-AU-endorsed applications for the continental name."
            },
            "wine": {
                "warnings": 9, "score": 22, "category": "geographical_indication",
                "governments": ["France", "Italy", "Spain", "Portugal", "Hungary", "Czech Republic", "Moldova", "Slovakia", "Switzerland"],
                "summary": "Wine-producing nations filed GAC early warnings citing TRIPS Article 23 GI protection concerns. Governments argued .wine could undermine international GI protection frameworks."
            },
            "vin": {
                "warnings": 9, "score": 22, "category": "geographical_indication",
                "governments": ["France", "Italy", "Spain", "Portugal", "Hungary", "Czech Republic", "Moldova", "Slovakia", "Switzerland"],
                "summary": "Same wine-producing nations filed for .vin (French for wine) on identical GI grounds as .wine."
            },
            "champagne": {
                "warnings": 5, "score": 22, "category": "geographical_indication",
                "governments": ["France", "EU member states"],
                "summary": "France and EU wine-producing states pre-emptively signalled GI protection concerns for the champagne appellation, the most aggressively defended wine GI globally."
            },
            "cognac": {
                "warnings": 3, "score": 20, "category": "geographical_indication",
                "governments": ["France", "EU"],
                "summary": "France signalled GI protection for cognac appellation under TRIPS Art. 23 and the Lisbon Agreement."
            },
            "tequila": {
                "warnings": 3, "score": 20, "category": "geographical_indication",
                "governments": ["Mexico"],
                "summary": "Mexico filed GAC early warning supporting CRT application and opposing any non-CRT applicant on GI grounds."
            },
            "scotch": {
                "warnings": 2, "score": 20, "category": "geographical_indication",
                "governments": ["United Kingdom"],
                "summary": "UK government filed early warning citing protection of the Scotch Whisky GI under EU and international law."
            },
            "islam": {
                "warnings": 12, "score": 22, "category": "religious_cultural",
                "governments": ["Saudi Arabia", "OIC member states"],
                "summary": "OIC (Organisation of Islamic Cooperation) member states filed collective early warning citing the religious significance of the name and need for OIC-endorsed governance."
            },
            "gay": {
                "warnings": 6, "score": 20, "category": "social_cultural",
                "governments": ["Multiple — details partially confidential under ICANN procedure"],
                "summary": "Several government delegations filed early warnings expressing concerns about protection of community and potential for misuse. Warnings were contested by LGBTQ+ advocacy groups."
            },
            "health": {
                "warnings": 7, "score": 20, "category": "sensitive_sector",
                "governments": ["Australia", "France", "Canada", "EU member states"],
                "summary": "Multiple governments flagged consumer protection and health misinformation concerns for unregulated .health registrations."
            },
            "bank": {
                "warnings": 11, "score": 22, "category": "sensitive_sector",
                "governments": ["Australia", "Canada", "EU member states", "United States"],
                "summary": "Financial regulators and government delegations warned that an open .bank registry would undermine financial consumer protection. Ultimately resolved with strict registrant verification requirements."
            },
            "insurance": {
                "warnings": 8, "score": 20, "category": "sensitive_sector",
                "governments": ["Australia", "Canada", "EU member states"],
                "summary": "Insurance regulators filed early warnings citing financial consumer protection concerns equivalent to .bank."
            },
            "pharmacy": {
                "warnings": 9, "score": 22, "category": "sensitive_sector",
                "governments": ["Australia", "Canada", "France", "United States", "EU member states"],
                "summary": "Health/pharma regulators warned that open .pharmacy registration could endanger public health by enabling illegal online pharmacies."
            },
            "sport": {
                "warnings": 4, "score": 18, "category": "community_governance",
                "governments": ["Multiple via SportAccord"],
                "summary": "International sports federations through SportAccord signalled governance concerns about non-IF-endorsed .sport registry."
            },
            "rugby": {
                "warnings": 2, "score": 18, "category": "community_governance",
                "governments": ["Multiple via World Rugby"],
                "summary": "World Rugby filed early warning asserting exclusive governance rights over the sport's naming."
            },
            "cricket": {
                "warnings": 2, "score": 18, "category": "community_governance",
                "governments": ["Multiple via ICC"],
                "summary": "International Cricket Council filed early warning asserting exclusive governance rights."
            },
        },
    },
    "sse_decisions_2012.json": {
        "_meta": {
            "source": (
                "ICANN String Similarity Review Panel Reports 2012–2013. "
                "Panel convened by ICANN to assess visual and aural similarity between applied-for strings. "
                "Findings informed contention set groupings and string confusion objection standing. "
                "Source: ICANN New gTLD String Similarity Reports; ICANN-DRSP objection decisions."
            )
        },
        "pairs": {
            "cpa": [{"similar_to": "spa", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Panel found contextual differentiation (accountancy vs. wellness) sufficient to distinguish strings despite 1-character difference."}],
            "corp": [{"similar_to": "coop", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Panel found edit-distance 2 and contextual differentiation (corporate vs. cooperative) sufficient despite partial overlap."}],
            "llc": [{"similar_to": "llp", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Legal entity type abbreviations found distinguishable in context."}],
            "inc": [{"similar_to": "ink", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Panel found contextual differentiation (corporate abbreviation vs. creative industry) sufficient."}],
            "news": [{"similar_to": "new", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Three-letter vs. four-letter string distinguished; panel found different conceptual fields."}],
            "blog": [{"similar_to": "blo", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "blo was not applied for; blog found distinctive as a compound coinage."}],
            "shop": [{"similar_to": "stop", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Glyph difference (h vs. t) found sufficient despite similar length and terminal characters."}],
            "web": [{"similar_to": "wab", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "web vs. wab — panel found e/a substitution creates sufficient visual distinction."}],
            "media": [{"similar_to": "median", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Panel found length difference (5 vs. 6 chars) and different conceptual fields distinguishing."}],
            "book": [{"similar_to": "look", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Initial consonant difference (b vs. l) found sufficient visual differentiation."}],
            "game": [{"similar_to": "came", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "game vs. came — panel found initial consonant differentiation sufficient in context."}],
            "film": [{"similar_to": "firm", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "l/r substitution found sufficient; different conceptual domains (cinema vs. business)."}],
            "free": [{"similar_to": "tree", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Initial character difference sufficient; different semantic domains."}],
            "live": [{"similar_to": "give", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Initial character different; live has distinct conceptual field."}],
            "love": [{"similar_to": "live", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Vowel substitution found sufficient; panel noted different semantic meanings."}],
            "eco": [{"similar_to": "ego", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "c/g substitution found sufficient visual distinction."}],
            "green": [{"similar_to": "greet", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Terminal character difference; strong semantic distinction (colour vs. greeting)."}],
            "art": [{"similar_to": "ant", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "r/n substitution found sufficient; clearly different semantic domains."}],
            "health": [{"similar_to": "wealth", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Initial character difference (h vs. w); entirely different semantic domains."}],
            "cloud": [{"similar_to": "crowd", "finding": "not_confusingly_similar", "basis": "visual", "year": 2013, "notes": "Panel found l/r and u/o differences create sufficient visual distinction."}],
        },
    },
    "sacred_sites.json": {
        "_meta": {
            "source": (
                "Curated reference list of globally recognised sacred and religiously significant sites. "
                "Sources: UNESCO World Heritage Committee; UNWTO Sacred Sites Programme; "
                "World Monuments Fund; national heritage bodies. "
                "These sites may attract community objections from religious bodies and GAC early warnings "
                "from relevant governments. Advisory only — see §7.5.3 Geographic Names Review."
            )
        },
        "strings": {
            "mecca": {"religion": "Islam", "location": "Saudi Arabia", "alt_names": ["makkah"], "significance": "Holiest city in Islam; site of Masjid al-Haram and the Kaaba. Non-Muslims prohibited from entry. Saudi government will almost certainly file a GAC early warning."},
            "medina": {"religion": "Islam", "location": "Saudi Arabia", "alt_names": ["madinah"], "significance": "Second-holiest city in Islam; site of the Prophet's Mosque. Saudi government expected to object to any non-Islamic-body application."},
            "makkah": {"religion": "Islam", "location": "Saudi Arabia", "alt_names": ["mecca"], "significance": "Arabic form of Mecca. Same considerations as .mecca apply."},
            "karbala": {"religion": "Islam (Shia)", "location": "Iraq", "alt_names": [], "significance": "Site of the Battle of Karbala; holiest Shia pilgrimage site. Iraqi government and Shia religious bodies likely to object to non-Islamic-community governance."},
            "najaf": {"religion": "Islam (Shia)", "location": "Iraq", "alt_names": [], "significance": "Site of Imam Ali Mosque; major Shia pilgrimage and scholarship centre. Similar community objection risk to .karbala."},
            "mashhad": {"religion": "Islam (Shia)", "location": "Iran", "alt_names": ["mashad"], "significance": "Site of Imam Reza shrine; largest city in Iran by pilgrimage volume. Iranian government likely to object."},
            "bethlehem": {"religion": "Christianity (and Judaism)", "location": "Palestine", "alt_names": [], "significance": "Birthplace of Jesus Christ; site of the Church of the Nativity (UNESCO WHS). Palestinian Authority and Christian churches likely to take interest."},
            "nazareth": {"religion": "Christianity", "location": "Israel", "alt_names": [], "significance": "Childhood home of Jesus; site of the Basilica of the Annunciation. Christian denominations likely to object to secular commercial use."},
            "lourdes": {"religion": "Christianity (Catholic)", "location": "France", "alt_names": [], "significance": "Major Marian pilgrimage site; 5–6 million pilgrims annually. Catholic Church and French government likely to raise concerns."},
            "fatima": {"religion": "Christianity (Catholic)", "location": "Portugal", "alt_names": [], "significance": "Marian apparition site; 4–6 million pilgrims annually. Portuguese government and Catholic Church likely to take interest."},
            "assisi": {"religion": "Christianity (Catholic)", "location": "Italy", "alt_names": [], "significance": "Birthplace of St Francis; UNESCO WHS. Italian government and Catholic Church likely to raise concerns."},
            "loreto": {"religion": "Christianity (Catholic)", "location": "Italy", "alt_names": [], "significance": "Site of the Holy House of Loreto; major Italian Marian pilgrimage destination."},
            "medjugorje": {"religion": "Christianity (Catholic)", "location": "Bosnia and Herzegovina", "alt_names": [], "significance": "Ongoing Marian apparition site; 1+ million pilgrims annually despite lack of full Vatican recognition."},
            "zion": {"religion": "Judaism (and Christianity)", "location": "Jerusalem", "alt_names": [], "significance": "Mount Zion; central symbol of Jewish identity and homeland. Israeli government and Jewish organisations likely to take interest."},
            "hebron": {"religion": "Judaism and Islam", "location": "Palestine/Israel", "alt_names": [], "significance": "Site of the Cave of Machpelah / Ibrahimi Mosque; sacred to both Jews and Muslims. Politically highly sensitive."},
            "varanasi": {"religion": "Hinduism", "location": "India", "alt_names": ["kashi", "benares"], "significance": "Oldest continuously inhabited city; most sacred Hindu pilgrimage site on the Ganges. Indian government and Hindu religious bodies likely to take interest."},
            "ayodhya": {"religion": "Hinduism", "location": "India", "alt_names": [], "significance": "Birthplace of Lord Rama; site of the Ram Janmabhoomi temple. Politically sensitive in India; government and VHP/RSS bodies likely to respond."},
            "vrindavan": {"religion": "Hinduism", "location": "India", "alt_names": [], "significance": "Sacred town associated with Lord Krishna; major Vaishnava pilgrimage site."},
            "tirupati": {"religion": "Hinduism", "location": "India", "alt_names": [], "significance": "Site of the Venkateswara Temple; most visited religious site in the world by devotee count. Tirumala Tirupati Devasthanams (TTD) would object."},
            "haridwar": {"religion": "Hinduism", "location": "India", "alt_names": [], "significance": "One of four Kumbh Mela sites; gateway to char dham pilgrimage circuit."},
            "dwarka": {"religion": "Hinduism", "location": "India", "alt_names": [], "significance": "One of the four char dham pilgrimage sites; sacred city of Lord Krishna."},
            "puri": {"religion": "Hinduism", "location": "India", "alt_names": [], "significance": "Site of the Jagannath Temple; one of the four char dham sites. Non-Hindus historically barred from temple entry."},
            "bodhgaya": {"religion": "Buddhism", "location": "India", "alt_names": ["bodh-gaya", "bodh gaya"], "significance": "Site where Buddha attained enlightenment; UNESCO WHS. International Buddhist community and Indian government likely to take interest."},
            "kushinagar": {"religion": "Buddhism", "location": "India", "alt_names": [], "significance": "Site of the Buddha's Parinirvana (death); UNESCO WHS tentative list."},
            "lumbini": {"religion": "Buddhism", "location": "Nepal", "alt_names": [], "significance": "Birthplace of the Buddha; UNESCO WHS. Nepalese government and international Buddhist bodies would object to commercial exploitation."},
            "kandy": {"religion": "Buddhism", "location": "Sri Lanka", "alt_names": [], "significance": "Site of the Temple of the Sacred Tooth Relic; UNESCO WHS. Sri Lankan government likely to take interest."},
            "sarnath": {"religion": "Buddhism", "location": "India", "alt_names": [], "significance": "Site of the Buddha's first sermon (Dharmachakra Pravartana); UNESCO WHS tentative list."},
            "amritsar": {"religion": "Sikhism", "location": "India", "alt_names": [], "significance": "Site of the Harmandir Sahib (Golden Temple); holiest shrine in Sikhism. Shiromani Gurdwara Parbandhak Committee (SGPC) and Indian government likely to object."},
            "uluru": {"religion": "Aboriginal Australian (Anangu)", "location": "Australia", "alt_names": ["ayers rock"], "significance": "Sacred site of the Anangu people; UNESCO WHS. Australian government and Anangu traditional owners have strong governance rights. Australia likely to file GAC early warning."},
            "jerusalem": {"religion": "Multi-faith (Judaism, Christianity, Islam)", "location": "Israel/Palestine", "alt_names": ["al-quds"], "significance": "Holiest city in Judaism; third-holiest in Islam; central to Christianity. UNESCO WHS. Multiple governments and religious bodies would contest any application. Political status is internationally disputed."},
        },
    },
    "world_heritage_sites.json": {
        "_meta": {
            "source": (
                "UNESCO World Heritage List — cultural and natural properties of Outstanding Universal Value. "
                "Inscribed under the UNESCO Convention Concerning the Protection of the World Cultural and "
                "Natural Heritage (1972). Applications for TLD strings matching UNESCO WHS names attract "
                "§7.5.3 Geographic Names Review and potential GAC early warnings from host governments. "
                "Source: whc.unesco.org (UNESCO World Heritage Centre)."
            )
        },
        "strings": {
            "angkor": {"country": "Cambodia", "whs_name": "Angkor", "inscribed": 1992, "category": "cultural", "note": "Khmer temple complex; Cambodia's national symbol. Cambodian government likely to object to non-Cambodian applications."},
            "stonehenge": {"country": "United Kingdom", "whs_name": "Stonehenge, Avebury and Associated Sites", "inscribed": 1986, "category": "cultural", "note": "Prehistoric monument; UK national heritage. UK government likely to raise concerns."},
            "pompeii": {"country": "Italy", "whs_name": "Archaeological Areas of Pompei, Herculaneum and Torre Annunziata", "inscribed": 1997, "category": "cultural", "note": "Roman archaeological site. Italian government likely to take interest."},
            "versailles": {"country": "France", "whs_name": "Palace and Park of Versailles", "inscribed": 1979, "category": "cultural", "note": "Royal palace; major French cultural heritage site. French government likely to take interest."},
            "alhambra": {"country": "Spain", "whs_name": "Alhambra, Generalife and Albayzín, Granada", "inscribed": 1984, "category": "cultural", "note": "Moorish palace complex; major Spanish heritage. Spanish government and Granada region likely to take interest."},
            "acropolis": {"country": "Greece", "whs_name": "Acropolis, Athens", "inscribed": 1987, "category": "cultural", "note": "Ancient Greek citadel; UNESCO WHS. Greek government likely to take interest."},
            "colosseum": {"country": "Italy", "whs_name": "Historic Centre of Rome, the Properties of the Holy See", "inscribed": 1980, "category": "cultural", "note": "Ancient Roman amphitheatre; Italian government and Ministry of Culture likely to respond."},
            "parthenon": {"country": "Greece", "whs_name": "Acropolis, Athens", "inscribed": 1987, "category": "cultural", "note": "Part of Acropolis WHS; Greek government likely to take interest."},
            "petra": {"country": "Jordan", "whs_name": "Petra", "inscribed": 1985, "category": "cultural", "note": "Nabataean rock-carved city; Jordan's most famous heritage site. Jordanian government likely to take interest."},
            "auschwitz": {"country": "Poland", "whs_name": "Auschwitz Birkenau", "inscribed": 1979, "category": "cultural", "note": "Nazi concentration camp; UNESCO WHS. Extremely sensitive; multiple governments and Jewish community bodies would strongly object to any commercial TLD application. Polish government and international Holocaust memorial organisations will oppose any application."},
            "hiroshima": {"country": "Japan", "whs_name": "Hiroshima Peace Memorial (Genbaku Dome)", "inscribed": 1996, "category": "cultural", "note": "Atomic bomb site memorial. Japanese government would object to any use that commercialises or trivialises the site's significance."},
            "olympia": {"country": "Greece", "whs_name": "Archaeological Site of Olympia", "inscribed": 1989, "category": "cultural", "note": "Ancient site of the Olympic Games; overlap with IOC-reserved Olympic terms. Greek government and IOC both have interests."},
            "delphi": {"country": "Greece", "whs_name": "Archaeological Site of Delphi", "inscribed": 1987, "category": "cultural", "note": "Ancient oracle site; Greek government likely to take interest."},
            "ephesus": {"country": "Turkey", "whs_name": "Ephesus", "inscribed": 2015, "category": "cultural", "note": "Ancient Greek/Roman city; major Turkish heritage site. Turkish government likely to take interest."},
            "lalibela": {"country": "Ethiopia", "whs_name": "Rock-Hewn Churches, Lalibela", "inscribed": 1978, "category": "cultural", "note": "Rock-cut Christian churches; sacred site for Ethiopian Orthodox Christians. Ethiopian government likely to object."},
            "timbuktu": {"country": "Mali", "whs_name": "Timbuktu", "inscribed": 1988, "category": "cultural", "note": "Historic Islamic scholastic centre; UNESCO WHS (endangered). Malian government likely to take interest."},
            "avignon": {"country": "France", "whs_name": "Historic Centre of Avignon", "inscribed": 1995, "category": "cultural", "note": "Medieval papal city; French government and Avignon region likely to take interest."},
            "dubrovnik": {"country": "Croatia", "whs_name": "Old City of Dubrovnik", "inscribed": 1979, "category": "cultural", "note": "Historic walled city; Croatian government and UNESCO WHS status create geographic review triggers."},
            "bruges": {"country": "Belgium", "whs_name": "Historic Centre of Bruges", "inscribed": 2000, "category": "cultural", "note": "Medieval Flemish city; Belgian government and local heritage bodies likely to take interest."},
            "galapagos": {"country": "Ecuador", "whs_name": "Galápagos Islands", "inscribed": 1978, "category": "natural", "note": "Darwin's evolution laboratory; Ecuadorian national park and UNESCO WHS. Ecuadorian government will almost certainly file a GAC early warning."},
            "serengeti": {"country": "Tanzania", "whs_name": "Serengeti National Park", "inscribed": 1981, "category": "natural", "note": "Major African wildlife ecosystem; Tanzanian national park. Tanzanian government likely to take interest."},
            "yellowstone": {"country": "United States", "whs_name": "Yellowstone", "inscribed": 1978, "category": "natural", "note": "First US national park; UNESCO WHS. US government (NPS/Interior Department) likely to take interest."},
            "everest": {"country": "Nepal/China", "whs_name": "Sagarmatha National Park (Nepal)", "inscribed": 1979, "category": "natural", "note": "World's highest peak; sits within UNESCO WHS. Both Nepal and China (Tibet) have sovereignty interests. Nepal government likely to file GAC early warning."},
            "kilimanjaro": {"country": "Tanzania", "whs_name": "Kilimanjaro National Park", "inscribed": 1987, "category": "natural", "note": "Highest peak in Africa; Tanzanian national park and UNESCO WHS. Tanzanian government likely to take interest."},
            "cappadocia": {"country": "Turkey", "whs_name": "Göreme National Park and the Rock Sites of Cappadocia", "inscribed": 1985, "category": "mixed", "note": "Unique volcanic landscape with rock-cut dwellings; Turkish government and UNESCO WHS status create geographic review triggers."},
        },
    },
    "wipo_gi.json": {
        "_meta": {
            "source": (
                "WIPO Lisbon Agreement for the Protection of Appellations of Origin and their International "
                "Registration; Geneva Act of the Lisbon Agreement (2015); TRIPS Agreement Articles 22–24; "
                "EU Regulation No. 1151/2012 on quality schemes for agricultural products and foodstuffs; "
                "Bilateral GI protection agreements. Curated list of GIs most relevant to potential gTLD "
                "applications. A GI-based objection may be filed as a Community Objection (§4.5.1.2) or "
                "raised through GAC early warning / advice."
            )
        },
        "strings": {
            "champagne": {"product": "Sparkling wine", "country": "France", "protection": "TRIPS Art. 23; EU Reg. 1151/2012; Lisbon Agreement; bilateral treaties", "score": 40, "objector": "Comité Champagne / French government", "note": "Most aggressively defended GI globally. Any application will face community objection, LRO, and GAC early warning from France."},
            "bordeaux": {"product": "Wine", "country": "France", "protection": "EU Reg. 1308/2013; Lisbon Agreement", "score": 35, "objector": "CIVB (Conseil Interprofessionnel du Vin de Bordeaux) / French government", "note": "Major French wine appellation; Bordeaux wine council will object to non-CIVB applications."},
            "burgundy": {"product": "Wine", "country": "France", "protection": "EU Reg. 1308/2013; Lisbon Agreement", "score": 32, "objector": "BIVB (Bureau Interprofessionnel des Vins de Bourgogne) / French government", "note": "Major French wine region; BIVB likely to object."},
            "prosecco": {"product": "Sparkling wine", "country": "Italy", "protection": "EU Reg. 1151/2012; DOC/DOCG", "score": 35, "objector": "Consorzio di Tutela del Prosecco / Italian government", "note": "EU-protected GI. Italian government and Prosecco consortium will object."},
            "rioja": {"product": "Wine", "country": "Spain", "protection": "EU Reg. 1308/2013; DOCa designation", "score": 32, "objector": "Consejo Regulador Rioja / Spanish government", "note": "Spain's most recognised wine appellation; regulatory council will object."},
            "chianti": {"product": "Wine", "country": "Italy", "protection": "EU Reg. 1308/2013; DOCG", "score": 30, "objector": "Consorzio Vino Chianti / Italian government", "note": "Tuscan wine GI; Italian government and consorzio likely to object."},
            "chablis": {"product": "Wine", "country": "France", "protection": "EU Reg. 1308/2013; AOC", "score": 28, "objector": "Union des Grands Crus de Chablis / French government", "note": "Burgundy white wine sub-appellation; protected under EU and Lisbon Agreement."},
            "sauternes": {"product": "Wine (dessert)", "country": "France", "protection": "EU Reg. 1308/2013; AOC", "score": 28, "objector": "Syndicat des Crus Classes de Sauternes et Barsac / French government", "note": "Protected French dessert wine appellation."},
            "barolo": {"product": "Wine", "country": "Italy", "protection": "EU Reg. 1308/2013; DOCG", "score": 28, "objector": "Consorzio di Tutela Barolo Barbaresco / Italian government", "note": "Piedmontese DOCG wine; protected GI."},
            "cognac": {"product": "Brandy", "country": "France", "protection": "TRIPS Art. 23; EU Reg. 110/2008; Lisbon Agreement; bilateral treaties", "score": 40, "objector": "BNIC (Bureau National Interprofessionnel du Cognac) / French government", "note": "Highly protected spirit GI. France will object to any non-BNIC application via GAC and community objection."},
            "scotch": {"product": "Whisky", "country": "United Kingdom", "protection": "Scotch Whisky Regulations 2009 (UK); EU GI; TRIPS Art. 23", "score": 38, "objector": "Scotch Whisky Association (SWA) / UK government", "note": "SWA is highly litigious in protecting the Scotch Whisky GI. UK government filed 2012 GAC early warning."},
            "tequila": {"product": "Spirit", "country": "Mexico", "protection": "NOM-006-SCFI-2012 (Mexican standard); TRIPS; bilateral treaties", "score": 38, "objector": "Consejo Regulador del Tequila (CRT) / Mexican government", "note": "Mexico's most protected GI. CRT is the only legitimate applicant; Mexican government filed 2012 GAC early warning."},
            "bourbon": {"product": "Whiskey", "country": "United States", "protection": "US Federal Standards of Identity (27 CFR 5.22); Congressional resolution 1964", "score": 28, "objector": "Distilled Spirits Council of the US (DISCUS) / US government", "note": "US-protected GI with international recognition. Less aggressively defended than Scotch or Cognac internationally, but DISCUS will object."},
            "armagnac": {"product": "Brandy", "country": "France", "protection": "EU Reg. 110/2008; Lisbon Agreement; AOC", "score": 30, "objector": "BNIA (Bureau National Interprofessionnel de l'Armagnac) / French government", "note": "French brandy GI; less prominent than Cognac but same legal framework applies."},
            "calvados": {"product": "Apple brandy", "country": "France", "protection": "EU Reg. 110/2008; AOC Calvados", "score": 28, "objector": "IDAC (Institut de l'origine et de la qualité) / French government", "note": "Protected Normandy apple brandy appellation."},
            "grappa": {"product": "Pomace brandy", "country": "Italy", "protection": "EU Reg. 110/2008; Italian law", "score": 28, "objector": "Istituto Nazionale Grappa / Italian government", "note": "Protected Italian GI for pomace brandy."},
            "mezcal": {"product": "Spirit", "country": "Mexico", "protection": "NOM-070-SCFI-2016; TRIPS; bilateral treaties", "score": 30, "objector": "Consejo Regulador del Mezcal (CRM) / Mexican government", "note": "Mexico's second major spirit GI; CRM is the regulatory body. Mexican government will support CRM position."},
            "parmesan": {"product": "Hard cheese", "country": "Italy", "protection": "EU Reg. 1151/2012; ECJ ruling C-132/05", "score": 35, "objector": "Consorzio del Formaggio Parmigiano-Reggiano / Italian government", "note": "Highly contested GI (US uses 'parmesan' generically; EU courts have ruled otherwise). Italian government and consorzio will object."},
            "gorgonzola": {"product": "Blue cheese", "country": "Italy", "protection": "EU Reg. 1151/2012; PDO", "score": 30, "objector": "Consorzio per la Tutela del Formaggio Gorgonzola / Italian government", "note": "Protected Italian blue cheese GI."},
            "roquefort": {"product": "Blue cheese", "country": "France", "protection": "EU Reg. 1151/2012; PDO; Lisbon Agreement", "score": 32, "objector": "Société anonyme des Caves Roquefort / French government", "note": "First-ever EU PDO; one of the most protected French food GIs."},
            "camembert": {"product": "Soft cheese", "country": "France", "protection": "EU PDO (Camembert de Normandie); French AOC", "score": 28, "objector": "INAO / French government", "note": "Protected Norman cheese GI; widely used generically but core appellation protected."},
            "feta": {"product": "Cheese", "country": "Greece", "protection": "EU Reg. 1151/2012; PDO (ECJ ruling 2005)", "score": 32, "objector": "Greek Dairy Association / Greek government", "note": "Greece successfully obtained ECJ ruling protecting feta as a PDO. Strong Greek government interest."},
            "manchego": {"product": "Cheese", "country": "Spain", "protection": "EU Reg. 1151/2012; PDO", "score": 28, "objector": "Consejo Regulador Queso Manchego / Spanish government", "note": "Protected Spanish La Mancha cheese GI."},
            "prosciutto": {"product": "Cured ham", "country": "Italy", "protection": "EU Reg. 1151/2012; PDO (di Parma, di San Daniele)", "score": 30, "objector": "Consorzio del Prosciutto di Parma / Italian government", "note": "Multiple Italian prosciutto PDOs. Italian government and industry consortia will object."},
            "darjeeling": {"product": "Tea", "country": "India", "protection": "GI Tag under Indian GI Act 1999; TRIPS; bilateral treaties", "score": 30, "objector": "Tea Board of India / Indian government", "note": "First Indian GI registered under the GI Act; Tea Board of India is the registered proprietor. Indian government will support objection."},
        },
    },
}
