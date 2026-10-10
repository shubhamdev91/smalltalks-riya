# Deliverables builder notes

- Rebuild everything (runs aggregate.py first): `C:\Users\SSTS\AppData\Local\Programs\Python\Python312\python.exe -I tools\build_master.py C:\Users\SSTS\Desktop\Hiring` (add `--final` to drop the DRAFT label).
- Outputs: master_candidates.xlsx (All applicants / Shortlist / Coverage / Blockers), shortlist.md, priority_interview_group.md, final_progress_report.md.
- If master_candidates.xlsx is open in Excel, the script writes master_candidates_new.xlsx instead.
- final_score = judge_total (else screener total) + audit_adjustment; recommendation = audit > judge > screener; ties go to email applicants.
- Gender-blind guard: output text is neutralised in memory; input files that still contain gendered pronouns are listed on the Blockers sheet (8 at the first draft: 3 assessments, 5 portfolio audits). Fix with tools/neutralise_pronouns.py (owners only).
- Email data: email_applicants.csv / email_cv_index.csv / verification/*.md are picked up automatically when they appear.
