# Tarang Receipt Reader — prototype

A conservative receipt-processing prototype for Tarang Pharma Distribution. It provides:
- FastAPI endpoint (`POST /extract`) accepting a receipt photo and rep-entered claim.
- Streamlit demo screen for trying an image.
- Optional local OCR through Tesseract + `pytesseract`; no API key is required.
- Rule-based extraction of likely vendor/date/receipt number/GSTIN/amount, claim-vs-receipt comparisons, and duplicate-image checks.
- `predictions.csv` with one row per supplied test claim in the required schema.

## Important limitation
The supplied upload contained the CSV files and task text, but **no `images/` directory or receipt photos**. Therefore predictions.csv is a conservative CSV-derived baseline, not a photo-read result: dates and amounts are parsed from rep-entered fields, vendor names are normalized from historical clerk entries where an exact vendor key matches, GSTIN is borrowed only from an exact historical vendor key, and receipt numbers are left blank. Every test claim is marked `review`. Do not present this as achieving 95% image field accuracy or deploy automatic approvals. Add the original images and run OCR/validation before relying on extraction.

## Quick start (Python 3.10+)
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.api:app --reload
```
API docs: http://127.0.0.1:8000/docs

In another terminal:
```bash
streamlit run app/ui.py
```
The app works without API keys. OCR is optional; install the Tesseract executable separately and ensure `tesseract` is on PATH. If unavailable, the service returns a clear OCR-unavailable warning and asks for review.

## API
`POST /extract` multipart form:
- `file`: image file
- `claim_json`: JSON string containing `claim_id`, `emp_id`, `category`, `vendor`, `amount_claimed`, `expense_date`, `rep_comment`

Example:
```bash
curl -X POST http://127.0.0.1:8000/extract \
  -F "file=@receipt.jpg" \
  -F 'claim_json={"claim_id":"demo-1","category":"Food","vendor":"Cafe","amount_claimed":"Rs 250","expense_date":"2026-10-10"}'
```

## Decisions and safety
The endpoint defaults to `review`. It never auto-approves based only on a low claim amount. Reasons include OCR availability, unreadable/missing fields, mismatch between claim and detected amount, amount >= ₹2,000, possible duplicate image hash, and policy-specific checks. A production system should use confidence calibration, a held-out validation set, human review sampling, duplicate receipt matching (not only byte-identical files), and a rollback switch before considering auto-approval.

## Evaluation / evidence
See `EVIDENCE.md`. Training set has 283 processed rows: 275 approved, 6 queried, 2 rejected. No receipt images were supplied in the accessible upload, so image-level accuracy and OCR failure modes cannot be measured honestly. Do not claim 95% accuracy. The included `predictions.csv` has 190 rows to match `sample_submission.csv`; schema and row count are checked by `tests/test_outputs.py`.

## Costs and potential savings
Two clerks cost ₹76,000/month combined. At 2,400 claims/month × 3.5 minutes, typing/checking consumes about 140 hours/month. Dividing loaded monthly cost by this work volume gives an approximate direct labor allocation of ₹31.67 per claim, or ₹76,000/month if all of that work were eliminated (not a cash saving unless staffing/overtime is reduced or capacity is redeployed). A 90% under-₹2,000 share implies about 2,160 claims/month in the proposed auto-approval cohort. OCR/model/API costs are not included; this prototype makes no paid API calls. Since auto-approval is disabled, realized savings are currently ₹0/month.

## Files
- `predictions.csv`: submission-shaped baseline.
- `memo.md`: one-page recommendation to Finance Controller.
- `submission-form.md`: completed draft answers, including explicit limitations and no fabricated screen-recording/repository links.
- `EVIDENCE.md`: data checks and validation limitations.
