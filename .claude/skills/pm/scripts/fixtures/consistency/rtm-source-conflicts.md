Rows of docs/scope-package.en.md before commit bfd9df8, where the Inter-RTM gave four
requirements a narrower Source than the requirements documentation.

| ID | Requirement | Source | Priority | Category | Business Objective | Deliverable | Verification | Validation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FR06 | Tuition, invoicing, payments, and debt tracking (F06) | Front-desk staff, Accountant | Must have | Functional | BR03 | 1.5.1.1, 1.5.1.3 (D4) | Invoice totals match the policy worked examples; the aged debt list ties to the invoice ledger | Accountant reconciles one term of test invoices and payments in UAT |
| FR12 | Android and iOS application for parents and teachers (F12) | Student / Parent, Teacher | Must have | Functional | BR05; Stakeholder satisfaction: <mark>70% of guardians with a smartphone</mark> activated by closeout | 1.4.4.1, 1.5.4.1, 1.5.4.3, 1.9.1.2 (D3, D4, D11) | Every F12 function within 3 taps; push delivery recorded in the F09 log | Parents and teachers use the application during the pilot and the first warranty month |
| NFR01 | Functional completeness in UAT (A01) | Center Director, sponsor | Must have | Acceptance | Scope: no function deferred without an approved change request; BR07 | 1.6.2.2, 1.8.3.2 (D5) | UAT pass rate at or above 99%; defect log shows no open Critical or High | UAT sign-off by the sponsor at M6 against the test set agreed at M5 |
| NFR08 | Usability in Vietnamese after half a day of training (A08) | Front-desk staff, Teacher | Must have | Usability | Stakeholder satisfaction: <mark>80% of the 52 staff users</mark> trained and active; BR07 | 1.3.1.4, 1.8.2.2 (D2, D8) | Click count measured on each of the three paths; training record shows the half-day format | Staff perform their daily tasks unaided the day after training |

| ID | Business Requirement | Priority | Source | ID | Technical Requirement | Priority | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BR03 | Overdue tuition visible and falling to <mark>3%</mark> | Must have | Accountant | FR06 | Invoicing, payment recording, and the aged debt list | Must have | Accountant |
| BR05 | Notification cost held down | Must have | Center Director | FR12 | Application as the push channel over the same API | Must have | Student / Parent |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR01 | All twelve functions accepted in UAT | Must have | Center Director |
| BR07 | The center operates on the system, data in its own hands | Must have | Center Director | NFR08 | Daily tasks after half a day of training | Must have | Front-desk staff |
