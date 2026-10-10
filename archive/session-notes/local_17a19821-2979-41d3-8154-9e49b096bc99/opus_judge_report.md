# LIVE STATUS: reports for the orchestrator (local_005b980d…) go here because outbound messages are capped. Newest at the top.

## Email-applicant pass (31 E files, index 669): DONE, queue empty, waiting
Every E applicant with a CV has an Opus pass (Vineet Chaturvedi E9682752167 has no CV and stays hold_no_cv). The link-gap sweep was run first. Master: **shortlist 39** · review 147 · reject 480 · hold_no_cv 3 · format problems 0.

**New shortlist:** **Ayush Kumar Rai E7505206373 — 56** (CLAUDE.md/AGENTS.md opened: stock, so no credit from them; a project-specific agent prompt is credited; the "published SDK" claim is not on npm).
**Waiver list addition:** **Tejas Lamba E7473944243 — 59, held at review.** Evidence for the CallKaro role starts Sep 2026, so total experience is ~10 months and the gate follows the CV. The cover letter's ~14 months is not supported, and the portfolio tejas.is-a.dev is DNS-dead.
**Review:** Arham Shameem 52 (ai-tester worker pipeline verified) · Pradyumn 46 (Play Store app verified) · Vineet Joshi 42 (Postgres+pgvector in their own Phone_RAG repo, so the gate passes; metrics inflated).
**Reject:** Aman Tiwari 41 · Aditya Kumar (adityaraj12) 37 (live demos, but 0 months of experience) · Muskan Rastogi 35 · Pintu Kumar 33 (the "RAG" never calls an LLM) · Khushbu Pandya 32 · Farhan Khan 29 · Pranay Kumar 29 · Rudra Pandit 27 · Seema Bharti 22 · Gourav Singh 18 · Uday Raj Gupta 15 · Abhijit Kundu 4 (email looks auto-applied).

**Duplicates merged (judged once on the LinkedIn file; source: both; +2–3 email credit; E file has `duplicate_of:` + stub):**
Mayank Kapoor 39236192619 → 47 review · Rohit Rawat 39234713012 → 50 review · Abhishek Tiwari 39239150310 → 39 reject (two CVs conflict; real tenure ~2 yrs, not 3.8) · Gaurav Kumar 39286836891 → 37 reject (4 mo) · Kanak Sharma 39233742796 → 36 reject (email inflates tenure to "2+ yrs") · Mohammed Sohail 39261022662 → 32 reject · Shubham Singh 39234562872 → 33 reject · Prince Kumar Mishra 39236159925 → 29 reject (email adds skills/projects not on the CV) · Nikhil V. 39235037388 → 38 reject (expects 4–6 LPA) · Diwansh Gupta 39246350526 → 40 reject · Priya Gautam 39239853045 → 39 reject (live AI SaaS but fails the gate).
**Two duplicates you hadn't listed (found by the judge):** Shubham Gangwar E7530758492 = 39236894557 → 27 reject · **Saif Ali Nagori E4092610514 = 39234567961, IDENTITY FLAG: the LinkedIn applicant name is "Mohammed Faizan" but the file carries Saif's CV (same email/phone/GitHub). Confirm who applied before any contact.** → 28 reject.
**CV-vs-email conflicts flagged:** Uday Raj Gupta (claims 2+ yrs Go/Postgres; the CV shows ~7 mo QA with MySQL) · Pranay Kumar (CV GitHub handle 404s; email handle pranaykumar092 is real) · Tejas Lamba (tenure) · Kanak Sharma (tenure) · Prince Kumar Mishra (skills) · Rudra Pandit (two GitHub handles).

## Pass at index 638–641 (Top fit + Maybe complete): JUDGE QUEUE EMPTY, waiting
Link-gap sweep run first: nothing new at ≥35 with code links. 10 judged:
- **Bhushan Bharat: 56 on merit, held at REVIEW (judge_override)**. Screener had strong_shortlist 67. The experience gate rests on self-founded ventures plus a 4-month remote internship. Prepozone is live (sitemap updated 6–8 Oct), but tenure, users and revenue are unverified, the product code is private, and the public repos are short bursts. The brief's gate counts jobs/internships, so this is gate-unclear → review (same as Rajwinder Singh). **If Shubham accepts venture tenure, Bhushan becomes a 56 shortlist.** Added to the waiver list.
- **Pawan Bisht 55 SHORTLIST** (screener 59): strong Postgres backend (Revenant), but no AI/agent evidence (AnyaAI is React Native boilerplate); salary doubtful.
- Jhalak Kumar 44 review (one 3-day undeployed repo; MySQL only; the second login jhalak-id is probably the same person, unconfirmed) · Aayush Kumar 41 review (live self-built AI product resumeprompt.in, code private; live-product exception).
- Reject: Anjani Kushwaha 41 · Anurag Singh 37 (audit agrees) · Kanak Sharma 34 · Lata Sharma 31 · Kamal Gupta 27 (audit agrees) · Vani Krishna 25.
**Shortlist now 38** (adds Pawan Bisht 55; Shivam Omer and Satwik Kanhere were already removed in the re-check pass). Master: shortlist 38 · review 139 · reject 460 · hold_no_cv 2. Format problems 0. Audit cumulative: 2 misses in ~142.
Waiver list additions: Bhushan Bharat 56 (venture tenure).

## Re-check pass (commit Atom fallback + stock agent-file rule), shortlist now 37
Removed from shortlist (now review): Shivam Omer 52 and Satwik Kanhere 50 (their d4 credit rested on stock create-next-app CLAUDE.md/AGENTS.md). Score changes: Mohammad Sameer 58, Aman Sharma 57, Ankit Kumar 62 (still review on the gate), Rajwinder Singh 55 (Gemini triage confirmed, but stock Nx CLAUDE.md; still review on the gate). Commit shapes confirmed sole-author and sustained for Aqib, Kripa, Aditya Raj, Manish (confidence raised to medium), Firoz, Anurag, Nikhil Bhatt. Sam Vasishat 36 and Tushar Jaiswal 34: reject. In the shortlist lists below, ignore Shivam Omer and Satwik Kanhere.

## JUDGE QUEUE EMPTY at index 625: ~423 unique candidates judged (434 ledger rows incl. re-checks), waiting
Master: shortlist 39 · review 134 · reject 447 · hold_no_cv 5. Format problems 0. Link-gap sweep (≥35 with code links) is clear.
Final tail since reports 14–17: Deepanshu Singh 47 review; everything else reject (≈20, all screener ≤38). Audit: 0 more misses.

**FINAL SHORTLIST (39), judge total (salary, location):**
67 Gurnoor Singh Saini (doubtful, Chandigarh) · 67 Ravinder Pandey (doubtful, NCR) · 67 Chirag Singh (doubtful, Pune) · 66 Mohd Ashhar (doubtful, NCR) · 65 Shivam Kumar Singh (doubtful, Bengaluru) · 63 B. Adhi Shakthi (plausible, other) · 63 jaswanth pakalapati (plausible, other) · 61 Kripa Shankar Mishra (doubtful, unknown) · 61 Aqib Siddiqui (doubtful, NCR) · 61 Nikhil Bhatt (plausible, NCR) · 60 Nikhil Rai (plausible, NCR) · 60 Adarsh Sinha (doubtful, other)
— wave 2 (55–59): 59 Mann Vishnoi · 59 Nipun Goel · 59 Ankur Pandey · 59 Mohammad Sameer · 59 Naga Balaji Nagendra · 59 Sundram Mishra · 59 Aditya Raj · 59 Mansi Sonani · 58 Tanishk Khare · 58 Dhruv Gupta · 58 Firoz Ahmad · 58 Anubhav Hooda · 58 Aman Sharma · 58 Siddhesh Kumar · 57 Anurag Yadav · 57 Sandeep Kumar Jha · 57 Shivam Omer · 57 Ayush Joshi · 56 Abhay J. · 56 Satwik Kanhere · 56 Saksham Kanojia · 55 Manish Bhaktisagar · 55 Mahesh C · 55 Agastya Srivastava · 55 Bhavya Kohli · 55 Himanshu Choudhary · 55 Sushil Bajpai.
No strong_shortlist: nobody combines multiple verified, deployed, owned products with Go/ERP fit and an affordable salary. Recommend inviting the 12 at 60+ first; confirm salary and relocation on the first call (9 of the 12 are doubtful or outside NCR).

**GATE-WAIVER / CONFIRMATION LIST (Shubham's call; files say review):** Ankit Kumar 66 (~11 mo) · Soumil Suri 62 (~9 mo) · Vaibhav Kandpal 61 (student, undated work) · Joney 59 (~6 mo) · Aditya Kumar Singh 59 (~3 mo, student) · Rajwinder Singh 56 (gate unclear) · Amar Kumar Thakur 56 (B.Tech until 2027) · Luvish Gulati 55 (no Postgres anywhere) · Garv Goel 55 (SQL Server/SQLite) · Akash Tripathi 55 (~7 mo) · Ajay Barman 54 (no work) · Vipul Sharma 54 (~6 mo) · Kinshuk Narang 53 · Anushka Tewari 53 (student) · Raghav Gupta 52 (~11 mo) · Shahzeb Khan 52 · Priya Sharma 51 (fresher) · Pranav K. 51 · Pranav Kumar 50.

**Rejection audit, cumulative:** 2 misses (Aditya Raj, Manish Bhaktisagar, both from the old on-site rule plus hidden links) in ~140 samples. No widening needed.

## Reports 14–17 (index 625)
NEW SHORTLIST: **Sandeep Kumar Jha 57** (Postgres re-check: own repo has Prisma provider "postgresql" plus a pgvector DATABASE_URL, so the gate passes). Luvish Gulati and Garv Goel were re-checked and have no Postgres in their own repos (SQL Server/SQLite/none), so both stay on the waiver list.
WAIVER LIST ADDITIONS: Joney 59 (~6 mo; strong merit) · Anushka Tewari 53 (student until 2027, current internship) · Pranav K. 51 (~8–9 mo; live payroll product).
REVIEW: Rajiv Thakkar 50 (CloudStore live; ~20 ambitious repos in 4 months) · Rohit Rawat (39234713012) 48 · D Shakthi Saravanan 47 · Manish Kumar 46 · HARSH MOHAN 44 (audit reject → review) · Raunak Kumar 44 · Arupananda Parida 44 (verified Postgres JobScheduler).
REJECT: ~55 more, all screener ≤45, including every audit sample. Audit cumulative: 2 misses in ~130 (both from the old on-site rule).
PROCESS NOTES: (1) The audit sampler now uses a stable 1-in-6 by application_id (positional sampling drifted and over-sampled). (2) Link-gap sweep: only rejects scored ≥35 with code/demo links are pulled in. All four historical big jumps came from 36–39, and below 35 there were 0 misses in ~60. (3) link_gap_sweep.py has false positives: in several files the screener had already inspected the "unexamined" links, but the URLs were written differently.
Shortlist now 39 (adds Sandeep Kumar Jha 57).

## Reports 12–13 (index 528)
NEW SHORTLIST: **Nikhil Rai 60** (judge ruling: Neon Postgres verified in their own CV-linked repo passes the Postgres gate, the same ruling as Mohit Kumar; ~23 mo experience; live CRM verified) · **Mansi Sonani 59** (screener 62; leadmind-mcp is a single-day repo; Render demos cold-start).
WAIVER LIST ADDITIONS: Aditya Kumar Singh 59 (~3 mo, student until 2027) · Kinshuk Narang 53 (no job; Postgres similar) · Shahzeb Khan 52 (~3 mo software) · Priya Sharma 51 (fresher; demo on Neon) · Pranav Kumar 50 (~9 mo, student until 2028).
REVIEW: Mayank Kapoor 45 · Nitesh Kumar 43 · Alok Rai 42 · Ananya Singh Rajvanshi 42 (Postgres similar).
REJECT (19): Kunal Singh 41 · Gagandeep Singh 41 · Wasim Raja Middya 41 · Amit Panja 40 · Dharshan L 42 · Ashish Kumar (39276749615) 44 · Nitish Kumar 39 · Prachi Sharma 39 · Praveen Kumar 38 · Aman Kumar 38 · PRATEEK SINGH 38 · Diwansh Gupta 38 · Shantanu R. 37 · Vishal Tomar 35 · Priyanka Thakur 33 · Nitin Rohilla 33 · Pankaj Kumar Verma 32 · Aryan Singh 32 · Manish Lodha 29 · Rahul Agarwal 29 · Ritik Kumar 28.
AUDIT: 13 more, 0 misses. Cumulative: 2 misses in ~90; both were from the old on-site rule plus hidden links.
Suggestion: Sandeep Kumar Jha, Luvish Gulati and Garv Goel (waiver list, Postgres similar) can each get a quick check of their own repos for Postgres/Neon. If found, the same ruling would move them to shortlist.

## Report 11 (index 486)
Rajwinder Singh, 56 on merit, held at **review**: the ≥12-month gate is unclear (internship months unconfirmed, ~1.0 yr). Added to the waiver list.
REVIEW: Ritu Choudhary 46 (screener had shortlisted at 57; tutorial microservices) · Sumit Kumar 47 (MCP server live) · Girraj Singhal 45 · Vikas Verma 44 · ABHISHEK KUMAR 43 (audit reject → review; LangGraph pipeline, possibly employer code) · Rahul Sharma 43 · Aniket Savita 43.
REJECT: Ayush Kumar Dwivedi 41, Rohit Baghel 41, Syed Junaid Ali 42 (2 mo), Manish Sahni 40, Chirag Tyagi 40 (copied YouTube demos), Chitransh Johari 40, Anabil Baruah 39, Gourav Batra 39, Ranjesh Kumar Verma 39, Aman pal 38, Ayush Aggarwal (39257618733) 37, Ashish Singh 33. Audit: 7 more, 0 misses.

## CURRENT SHORTLIST (36), judge totals
67 Gurnoor Singh Saini · 67 Ravinder Pandey · 67 Chirag Singh · 66 Mohd Ashhar · 65 Shivam Kumar Singh · 63 B. Adhi Shakthi · 63 jaswanth pakalapati · 61 Aqib Siddiqui · 61 Kripa Shankar Mishra · 61 Nikhil Bhatt · 60 Adarsh Sinha · 59 Mann Vishnoi · 59 Aditya Raj · 59 Mohammad Sameer · 59 Nipun Goel · 59 Sundram Mishra · 59 Ankur Pandey · 59 Naga Balaji Nagendra · 58 Tanishk Khare · 58 Anubhav Hooda · 58 Dhruv Gupta · 58 Aman Sharma · 58 Firoz Ahmad · 58 Siddhesh Kumar · 57 Anurag Yadav · 57 Shivam Omer · 57 Ayush Joshi · 56 Saksham Kanojia · 56 Satwik Kanhere · 56 Abhay J. · 55 Manish Bhaktisagar · 55 Agastya Srivastava · 55 Himanshu Choudhary · 55 Bhavya Kohli · 55 Sushil Bajpai · 55 Mahesh C · **60 Nikhil Rai · 59 Mansi Sonani** (added in reports 12–13; 38 total).
No strong_shortlist. Suggestion: invite the 60+ group first (11), hold 55–59 as wave 2.

## GATE-WAIVER / CONFIRMATION LIST (Shubham's call; files say review)
Ankit Kumar 66 (~11 mo) · Soumil Suri 62 (~9 mo) · Vaibhav Kandpal 61 (student, undated) · Sandeep Kumar Jha 57 (Postgres similar) · Rajwinder Singh 56 (gate unclear) · Amar Kumar Thakur 56 (B.Tech until 2027) · Luvish Gulati 55 (Postgres similar) · Garv Goel 55 (Postgres similar) · Akash Tripathi 55 (~7 mo) · Ajay Barman 54 (no work) · Vipul Sharma 54 (~6 mo) · Raghav Gupta 52 (~11 mo).

# Opus judge: pass 3 (Top fit page 5, 125 assessments)
19 judged (Opus, high effort). New shortlist: **Dhruv Gupta 58** (salary doubtful). **Soumil Suri 62 → review via judge_override**: shortlist-grade work (live PandaPrep LangGraph app with tests/evals; Drift package), but ~9 months total experience fails the locked ≥12-month gate. Shubham to decide; Soumil is the first to invite if the gate is waived. Om Trivedi (screener shortlist 58) → review 52 (dead demo domain, mirrored employer code). Review: Madhav Singhal 48, Jiya Arora 46, Naina Varshney 45, mohd azad 45, Deepak Kathuria 45, Vijay Sharma 44, Abhishek Kumar 43. Reject: 10 (Vishesh Kumar, arsalan chaudhary, Avinish Kumar, Rohan Gaur, Gaurang Varshney, Mehul Gautam, DUSHYANT GOYAL, Atul Dahiya, Mudit Parashar…). Audit: Avinish Kumar and Mudit Parashar both agree, 0 misses. Link sweep 0.
Shortlist now 12 (adds Dhruv Gupta).

# Opus judge: pass 2 update (2026-10-08, link sweep)

**REJECTION AUDIT: 2 MISSES.** Among the screener rejects that had their CV links hidden, 2 of 7 are shortlist-grade:
- **Aditya Raj 59 shortlist** (screener 38 reject). Delhi, ~15 mo remote. Taxova.ai is live on Railway: WhatsApp Cloud API webhooks, GST invoice extraction, GSTR-2B reconciliation, ITC rules, HITL, RAG. The repo tree matches the CV (FastAPI, db.py, Dockerfile, tests). This is the closest fit to Sutra/BUSY accounting in the pool. Commits unverified (429).
- **Manish Bhaktisagar 55 shortlist, low confidence** (screener 37 reject). Email applicant (source: both), ~16 mo remote, demo.adtext.org live, very active voice/phone-agent and retrieval-eval repos. Backend/Postgres depth unverified; location unknown.
Agree (still reject): Abhishek Mor 38 (no relational DB), Vivek Sagar 21, Varun Kumar Prajapati 28, Yash Joshi 43 (no job experience), Shashank Singh Negi 24.
Overall audit: 2 misses in 12 samples. Both came from the old on-site gate plus hidden links, so the 3 rejects not yet audited in the 30–44 band (all have an Opus pass now or no links) look low risk; the link-gap sweep now reports 0.

Re-checks (links examined, earlier Opus block kept): Vedant Roy 47 review (+2; email credit; Streamlit demos redirect, unverified) · Jatin Kashyap 52 review (+1; all 7 demos live, several v0/AI-Studio generated) · Dhruv Khandelwal 49 review (+1; Go repo with migrations/Docker) · Shivansh Chandra 49 (no change) · Moguloju Sai 44 (no change; HF Spaces are tutorials).
URL re-check with fixed helper: 8 files got a `url_recheck` line (Agastya, Tanishk, Rahul S., Prateek, Om Mishra, Prafull: live; Anmol: Render 503 cold start; Khushal: parked-domain redirect). No score changes.
Shortlist is now 11: Aqib Siddiqui 61 · Kripa Shankar Mishra 61 · Mann Vishnoi 59 · **Aditya Raj 59** · Tanishk Khare 58 · Anubhav Hooda 58 · Saksham Kanojia 56 · **Manish Bhaktisagar 55** · Agastya Srivastava 55 · Himanshu Choudhary 55 · Bhavya Kohli 55.
Also: Abhishek Mor's mcp-social-media repo has a committed .env. gate_onsite_experience corrected to pass for Aditya, Manish and Vedant.

# Opus judge: final report (pass 1)

Written 2026-10-08 by the Opus judge session. 92 assessments judged (every queue row from tools/aggregate.py as of 101 assessment files). Ledger: `progress/judge.csv`. Aggregator format problems: 0.

## Shortlist (case_study_invite: yes). No strong_shortlist yet.
| Judge | Screener | Name | Salary | Location | Note |
|---:|---:|---|---|---|---|
| 61 | 39 | Aqib Siddiqui | doubtful | delhi_ncr (Gurugram) | Screener missed GitHub (aqibsidd). Real 2026 repos: skilljit (Claude skill/MCP router, CI, bench), multi-agent-rag-chat. 4 yrs on-site, payout/bank-reconciliation work. MySQL recent; Postgres named. |
| 61 | 36 | Kripa Shankar Mishra | doubtful | unknown | Screener missed GitHub (KripaMishra). ~24 own repos 2023–26: sales agent with tests/Docker, voice agent, Go API, coding-agent skills. Location must be confirmed. |
| 59 | 61 | Mann Vishnoi | doubtful | delhi_ncr | Applied-AI lead; deployed voice demo; flagship code private, ERP-agents repo has no tests. |
| 58 | 62 | Tanishk Khare | plausible | india_other | Node/Prisma/Postgres plus a real Claude tool-calling voice agent. Re-marked eligible (remote rule). |
| 58 | 58 | Anubhav Hooda | plausible | unknown | Live multi-tenant Supabase SaaS plus RAG. Judge agreed with the screener. |
| 56 | 64 | Saksham Kanojia | plausible | delhi_ncr | 21 mo on-site; collabdocs live but a single-day repo; Nexus not public. |
| 55 | 63 | Agastya Srivastava | plausible | delhi_ncr | Postgres+pgvector, NestJS, RAG; no coding-agent evidence. Re-marked eligible. |
| 55 | 52 | Himanshu Choudhary | doubtful | india_other | Verified live Go LLM SaaS; 34 on-site months. |
| 55 | 56 | Bhavya Kohli | doubtful | unknown | Real agent repo; remote-only, now eligible. |

## Best review band (case_study_invite: maybe; use if the shortlist is thin)
Azhar Sayyad 52 (pharmacy-ERP domain; relocation) · Saurabh Kumar Bajpai 52 · Rasheed Maliyekkal 52 (3 live products, authorship unproven) · Raghav Gupta 52 (≈11 mo of work, student until 2028) · Jatin Kashyap 51 (DeployLane PaaS live; internship undated) · Tanish Chugh 50 (strong CV, AI work uninspected, salary) · Sarthak Jindal 50.

## Screener misses / systemic issues
1. **Link annotations missed.** In ≥12 files the screener wrote `github: none` or missed demos even though URLs were in the CV text. 2 of 9 shortlists came from this (Aqib +22, Kripa +25). Large raises: Rasheed +14, Dhruv Khandelwal +10, Gyanesh Shukla +11, Jatin Kashyap +16, Moguloju Sai +10, Shivam Pandey +8, Sarthak Sharma +7. **Recommend:** screeners grep `http` in each CV text, and sweep the existing screener rejects (not covered by my queue unless sampled).
2. **Overscoring of CV-only AI claims.** Of the original top 12, the average fell ~8 points, mostly in agents/agentic_coding credited above the 40% "uninspected" cap. 4 of 10 screener shortlists fell to review/reject (Yash Sharma 49→38 reject, Divyanshu 50→45, Tania T 51→49, Raghav Agarwal 61→48).
3. **"review" overused.** Many files scored 32–40 were marked review. Judge rule: ≤41 → reject unless an inspected Sutra-relevant project exists.
4. **Dim 6 underscored** for long on-site Delhi history (should be 4–5).
5. **Gender-blind breach:** the screener section of `39246142938_Khushboo_Gour.md` uses gendered pronouns. Needs neutralising by the owner.
6. **Possible secrets committed:** Gyanesh Shukla's multi-agent-system repo has an env-local file.
7. Hidden ATS keyword block in Tarun J.'s CV (rejected 43). Rohit Sharma's CV contains an unedited AI-drafting note.

## Rejection audit
Samples: Shafi Ur Rahman (54→47 review), Vedant Roy (38→45 review, old on-site rule), Shivansh Chandra (41→49 review), Prateek Gaur (agree), Mansha Singhal (agree; Postgres fail), Rajesh kumar Pal (agree), Amit Gupta (agree). **0 misses in 7** (none would be shortlisted). Three screener rejects moved up to review, all because of the old on-site rule or missed links.

## Tooling notes
- GitHub API 429 for all sessions. `gh_fetch repos` falls back to HTML and works (usernames are case-sensitive). commits/readme are mostly unavailable, so commit histories of shortlisted repos are unverified. Re-check Aqib, Kripa and Dev Grover (devgr72) once the limit resets or a token is added.
- `gh_fetch url` returns status 0 for many custom domains (network limit here). Treated as unverified, not dead.
- Judged files: front-matter score_* / total / recommendation / eligibility / salary_fit now hold judge values (the aggregator requires total = sum). Screener originals are in the Opus block (`screener_total`, `screener_scores`). Some files also got a corrected `github:` line.
