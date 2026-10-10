# LinkedIn review summary (job 4470290173, reviewed 10 Oct 2026)
Per-candidate files: crm_b2b_sales\linkedin_reviews\. This table is a quick index only; the files are the evidence. li_presence is a tie-break and is never added to a score.

| application_id | name | li_consistency | activity_12m | li_presence | red_flags |
|---|---|---|---|---|---|
| 39231408462 | Hasan Saeed | mismatch | low | 2 | none |
| 39235994198 | AKASH YADAV | minor_diff | low | 4 | soft |
| 39237404929 | Mayank Sharma | match | low | 2 | none |
| 39237762491 | Daksha Tiwari | mismatch | low | 4 | soft |
| 39239138315 | Neha Kumari | match | low | 2 | none |
| 39240107208 | Deepak kumar | match | low | 3 | none |
| 39245633509 | Dhruv Himani | mismatch | low | 2 | soft |
| 39245650030 | Noufal Pm | mismatch | high | 4 | soft |
| 39246162648 | Chetna G. | n/a | low | 4 | soft |
| 39251389502 | victor wemhe wezah | n/a | none | 1 | soft |
| 39251690999 | Neha Thakur | minor_diff | low | 2 | none |
| 39257932862 | Ankur G. | mismatch | low | 1 | none |
| 39260367509 | Mohini Bhadoriya | match | low | 3 | none |
| 39261705969 | Ayush Mangal | mismatch | none | 2 | soft |
| 39265525345 | Agneya_ S_Shetty | minor_diff | none | 2 | none |
| 39265582641 | Pooja Ahluwalia | minor_diff | medium | 3 | none |
| 39265820043 | Tamanna kunj | minor_diff | low | 2 | none |
| 39274548334 | Aarzoo pal | mismatch | none | 1 | none |
| 39275595739 | Zeeshan Malik | mismatch | high | 3 | yes (to verify) |
| 39283570163 | Priyanka Yadav | match | low | 2 | none |
| 39285815717 | Neha Gupta | match | low | 4 | none |
| 39285848350 | Kapil Chauhan | minor_diff | low | 3 | none |
| 39288692519 | Mohd zaid Ali | minor_diff | low | 3 | none |
| 39289522123 | Deveshwar . | minor_diff | low | 3 | none |
| 39290670512 | Hemanshu Tripathi | minor_diff | low | 2 | none |
| 39290728783 | Aanand Dubey | minor_diff | low | 3 | none |
| 39290908343 | Aishwarya Kochhar | match | none | 2 | none |
| 39291330960 | Abhinav Singh | minor_diff | low | 3 | none |
| 39291704385 | Ritu Binwal | minor_diff | low | 2 | none |
| 39297380044 | Arham Khan | match | none | 1 | none |
| 39300322696 | Aanchal choudhary | minor_diff | low | 1 | none |
| 39301261212 | Anushka T. | mismatch | none | 2 | none |
| 39301697872 | Riya Kumari | minor_diff | low | 3 | none |
| 39307303108 | kshama singh | mismatch | low | 2 | none |
| 39315453319 | Bhuvan Singh | minor_diff | low | 2 | none |
| 39317678546 | Surbhi Y | minor_diff | none | 2 | none |

## Conventions used (so the screener reads the fields the same way)
- li_consistency: match = titles, employers and dates agree. minor_diff = small date/title wording gaps, or a role present on one side only. mismatch = contradiction (CV title more senior, different current job or start date, no CV employer found on LinkedIn, CV name differs). n/a = no CV text (Chetna G. has no CV; victor wemhe wezah has an image-only scan).
- red_flags: only things visible on the public profile (title inflation on LinkedIn, contradictory tenures, promotional spam comments, pasted chatbot/template text). CV-side inflation is captured by li_consistency, not red_flags. "soft" = discrepancy worth asking about; "yes (to verify)" = Zeeshan Malik.
- activity_12m counts own posts, comments and reposts since 10 Oct 2025: none, low 1-5 items, medium 6-20, high = regular weekly posting. Job-application comments ("Interested") count as low activity. Non-work posts (puzzle-game scores, birthday wishes) and personal or political reposts were ignored.
- li_presence: 1 = bare; 2 = basic but complete; 3 = complete plus some professional activity; 4 = role-relevant posts or specifics; 5 = none given (nobody showed a clearly B2B/international-ready presence).

## Method notes
- Profiles were reached from each applicant card (opened by its applicationId URL; the panel header and job title were checked first), then the card's member-profile link. No search, no Google.
- Chrome reported visibilityState "hidden" for the whole run. Profile sections only loaded after real mouse-wheel scrolls (JS scrolling did not trigger the lazy load), so each profile was read after 3 wheel scrolls.
- Activity: the profile's Activity card (recent posts or comments) was used for most profiles. The separate activity pages were opened only for Abhinav Singh (posts) and Daksha Tiwari (comments), and the full experience list for Akash Yadav.
- Image-only CV (victor wemhe wezah): PDF could not be rendered here (poppler missing), so no CV comparison was made.
- Messages: read from the collapsed Messaging bar, Focused and Other tabs only; no thread opened; Page inboxes view not checked. Details in linkedin_reviews\_messages.md.

