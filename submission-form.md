# Submission form — draft answers

> Replace the GitHub URL and screen-recording URL after you publish/record them. Do not claim either exists until it does.

**Github Repo URL**  
`[PASTE YOUR PUBLIC REPOSITORY URL AFTER PUSHING THIS PROJECT]`

### 1. What did you build, and what decision does it support for Nilesh? State the number and the rupees.
I built a prototype receipt-reading service with a FastAPI endpoint and Streamlit screen. It accepts an uploaded image and claim details, attempts optional local Tesseract OCR, returns the five requested fields, highlights missing/mismatched values, and defaults to `review`. I generated a schema-matched `predictions.csv` for all 190 test claims. Finance's cost basis is ₹76,000/month for two clerks; 2,400 claims × 3.5 minutes is 140 hours/month, or about ₹31.67 direct labour allocation per claim. That is a theoretical capacity opportunity, not realized cash savings. Current realized savings are ₹0 because auto-approval is disabled and the receipt images were not present in the files I could access.

### 2. What do you expect predictions.csv to score on the hidden answers, field by field and on approve/review, and why?
I cannot give a credible numerical accuracy estimate. The accessible data contains 283 training rows and 190 test rows but no receipt photos, so I could not evaluate image OCR against the hidden receipt fields. The CSV baseline parses rep-entered date and amount, normalizes vendor from historical clerk entries only for exact normalized vendor keys, uses GSTIN only for exact historical vendor matches, leaves receipt numbers blank rather than inventing them, and marks every row `review`. Expect receipt-number accuracy to be poor due to blanks; vendor/date/amount are not independently verified from photos; GSTIN may be blank. Decision score is unknown and may be poor if labels expect approvals. I would report exact-match accuracy by field plus amount accuracy within the policy's ₹10 rounding tolerance, and precision/recall for approvals on a stratified held-out image set.

### 3. How do you know it works? What did you measure it against, how many receipts, and what kinds does it get wrong?
I verified the CSV output has 190 rows, the same claim IDs/order as `claims_test.csv`, the expected eight columns, and only `approve`/`review` decisions. The training CSV has 283 processed rows (275 approved, 6 queried, 2 rejected). I did not measure image-level accuracy because no image directory was included in the accessible upload. Known risks include rotated, blurred, shadowed, handwritten or cropped receipts; totals confused with line items; vendor extraction selecting a non-vendor line; variable date/invoice formats; and missing GSTIN. This is not evidence of 95% accuracy.

### 4. Did you change, narrow, or push back on Nilesh's ask? What, when, and why?
Yes. I kept the interface and endpoint, but did not enable automatic approvals. I chose this safety boundary because the photos were unavailable for validation, the historical decisions contain only 6 queries and 2 rejections, and a wrong payout can be difficult to recover. The prototype keeps all claims in review until Finance validates held-out image accuracy and sets an approval threshold.

### 5. What is wrong with what you are handing us, or with the data you were handed?
The accessible upload contained CSVs and the task text but not `images/`; therefore the generated predictions are not extracted from bill photos. Rep-entered expense dates and amounts are not receipt ground truth. Historical clerk fields contain blanks (6 each for vendor/date/number/amount; GSTIN blank on 171/283 rows). The service's local OCR heuristics are not calibrated and may misread totals, dates, vendor names or invoice numbers. Duplicate detection is only an in-memory exact-file hash and will miss re-photographed or recompressed copies. Policy checks are not comprehensive. The endpoint always returns `review`.

### 6. What does checking one claim cost, and what would a month cost at 2,400 claims? Show arithmetic.
Loaded clerk cost is ₹38,000 × 2 = ₹76,000/month. At 2,400 claims/month × 3.5 minutes = 8,400 minutes = 140 hours/month. Average direct cost allocation is ₹76,000 / 2,400 = ₹31.67 per claim. The entire ₹76,000 is an upper-bound capacity value if all work disappeared, not guaranteed cash savings. The prototype has no paid API calls; actual software/hosting costs are not included. Querying costs about ₹45 per claim queried, but no validated query-reduction estimate is available.

### 7. What did you deliberately leave out, and why that rather than something else?
I left out automatic approval, an ML classifier trained on historical status, and any claim of 95% accuracy. The image set was missing, while queried/rejected labels are sparse and cannot reliably teach fraud or policy decisions. I also did not fabricate receipt numbers or infer them from filenames. These are higher-risk than delivering a review-first interface.

### 8. Anything you built or found that nobody asked for?
The API returns OCR text and a SHA-256 image hash to support debugging and exact duplicate checks during a running process. The README includes a conservative cost model and staged rollout recommendation. The hash check is not a substitute for semantic duplicate detection.

### 9. What did you use AI for? Which tools and models, where they helped, where they misled you, what you threw away. Link your three-minute screen recording here.
I used an AI assistant to help structure the code, review edge cases, draft documentation and calculate the cost model. The shipped prototype uses local Tesseract OCR when installed; it makes no paid model API calls and requires no API key. I did not use AI-generated values as verified receipt data. I discarded the idea of auto-approving all claims below ₹2,000 without validating receipt amount, readability, duplicates and policy exceptions.  
Screen recording: `[PASTE YOUR SCREEN RECORDING LINK AFTER RECORDING A DEMO OF 3 MINUTES OR LESS]`

### 10. Someone picks this up on Monday and you are unreachable. The three things they need to know.
1. Follow README.md to install requirements and start `uvicorn app.api:app --reload`, then `streamlit run app/ui.py`; install Tesseract separately for OCR.
2. `predictions.csv` is a conservative baseline built without the missing images; do not claim image accuracy or use it to pay claims. The service always returns `review`.
3. Obtain and map the receipt photos, create independently verified ground truth, measure per-field accuracy and approval precision/recall, and keep a rollback/manual-review path before any auto-approval pilot.
