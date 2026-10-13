# Evidence and evaluation notes

## Dataset integrity checks
- Training claims: 283
- Test claims: 190
- Required prediction rows generated: 190 (one per test claim)
- Training decisions: approved 275, queried 6, rejected 2.
- Training clerk field blanks: vendor 6, bill date 6, bill number 6, bill amount 6, GSTIN 171.
- Test claim amount parsed from rep entry: 190/190.
- Test amounts below ₹2,000 based on rep-entered claim amount: 176/190. This is not evidence that the receipt itself matches that amount.

## What was actually tested
A structural check verifies the prediction file has 190 rows, the same claim IDs/order as claims_test, the expected eight columns, and only allowed decisions. The data pack available in this workspace does not contain the receipt images mentioned in the task; it contains only CSV files and the task text. Consequently no OCR predictions could be compared to receipt ground truth, no held-out image evaluation was possible, and no claim of 95% field accuracy is supported.

The train CSV is clerk-entered historical data, not verified image-level ground truth. Clerk entries can contain blanks and manual errors. Training status is also not a clean label for fraud: the dataset has only 6 queried and 2 rejected examples, so a model trained to imitate those decisions would be poorly supported.

## Known failure modes / limitations
- Low-quality, rotated, blurred, shadowed, cropped or handwritten receipts can produce missing or wrong OCR text.
- A line-item amount can be mistaken for the final total; the current OCR heuristic is not a calibrated total detector.
- Date formats and invoice number formats vary.
- Vendor extraction from the first plausible OCR line can choose an address or slogan.
- GSTIN may legitimately be absent; blank is not proof of invalidity.
- Byte-identical hash detection catches only exact copies within one running process, not edited/compressed/resized copies or same bill photographed twice.
- Policy checks such as vehicle number on fuel bills, hotel grade/night limits, outstation lodging, food limits, and whether a bill was claimed by its payer need structured context and/or human confirmation. This prototype does not make definitive policy decisions.

## Expected score on hidden labels
No honest numerical field-level score can be predicted from this workspace because the receipt images are missing and there is no held-out OCR evaluation. Receipt number is deliberately blank in the CSV baseline instead of fabricated. The decision is `review` for every row to avoid unsupported auto-approval. This is a safe operational choice but may score poorly if the hidden labels expect `approve`; it is not presented as a predictive classifier.
