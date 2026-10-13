# Memo to Nilesh Bhende? — Receipt-reading pilot recommendation

**To:** Nilesh Agrawal, Finance Controller  
**From:** Delivery team  
**Subject:** Tarang receipt-reading pilot: safe path to lower typing effort

## Recommendation
Pilot OCR-assisted data entry, but do **not** automatically approve claims yet. The provided workspace contains 283 processed claim rows and 190 test rows, but the receipt photos referenced in the brief were not included in the uploaded files. Therefore the current `predictions.csv` is a conservative CSV-derived baseline and not a validated photo-reading result. The demo service accepts an image and returns OCR suggestions, but always marks the claim `review`.

## Economics
Two clerks at ₹38,000/month cost ₹76,000/month. At 2,400 claims/month × 3.5 minutes each, manual typing/checking uses 8,400 minutes = 140 hours/month. The implied direct labour allocation is ₹76,000 ÷ 2,400 = **₹31.67 per claim**. If automation eventually removes all typing/checking effort, the theoretical upper bound is ₹76,000/month of capacity released—not necessarily cash saved unless staffing, overtime, or external costs fall. With the proposed 90% under-₹2,000 cohort, around 2,160 claims/month could be candidates for straight-through processing only after safety validation. This prototype uses no paid model API; current realized savings are **₹0/month**, because it does not auto-approve.

A query costs about ₹45 and delays payment by a week. Avoidable queries could therefore save ₹45 each, but the dataset does not establish how many queries the OCR tool would prevent. Wrong payouts are hard to recover, so the risk of an incorrect automatic approval must be measured before launch.

## What I need from Finance / IT
1. Provide the actual image directory with a stable mapping to `image_file`; include rotated, handwritten, faded, GST and non-GST examples.
2. Have clerks independently verify a stratified sample and label the five receipt fields, image readability, duplicate bill status, and policy exceptions.
3. Agree on a conservative launch threshold: initially assist typing only; then run shadow mode; enable low-value auto-approval only after held-out precision and amount-mismatch recall meet a jointly agreed threshold.
4. Define an audit sample, manual override, payment hold/rollback, retention policy and escalation route. Reps should not wait longer during the pilot: uncertain claims stay in the existing weekly review queue.

## Decision
Proceed with an OCR-assisted **human-in-the-loop pilot**, not a 95%-accuracy or auto-approval promise. The next gate is a measurable image-based evaluation, including amount accuracy and duplicate detection, before estimating realized savings.
