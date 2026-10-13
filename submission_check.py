import pandas as pd
test=pd.read_csv("data/claims_test.csv")
pred=pd.read_csv("predictions.csv",keep_default_na=False)
expected=["claim_id","vendor","receipt_date","receipt_number","gstin","total_amount","decision","reason"]
assert pred.columns.tolist()==expected
assert pred.claim_id.tolist()==test.claim_id.tolist()
assert len(pred)==len(test)
assert set(pred.decision).issubset({"approve","review"})
print(f"PASS: {len(pred)} rows; columns/order and decisions valid.")
print("Decision counts:",pred.decision.value_counts().to_dict())
