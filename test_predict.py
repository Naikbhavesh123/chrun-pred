import pickle
import pandas as pd
with open('churn_model.pkl', 'rb') as f:
    model = pickle.load(f)

print(type(model))

try:
    print(getattr(model, "get_booster", None))
except Exception as e:
    print("get_booster error:", e)

# Create dummy dataframe
d = {"monthly_fee":[79.0],"avg_weekly_usage_hours":[14.0],
     "support_tickets":[1],"payment_failures":[0],
     "tenure_months":[11],"last_login_days_ago":[9],
     "plan_type_Premium":[1],"plan_type_Standard":[0]}
X = pd.DataFrame(d)

try:
    fn = model.get_booster().feature_names
    if fn: X = X.reindex(columns=fn, fill_value=0)
except Exception as e:
    print("feature_names error:", e)

print("Dataframe X columns:", X.columns)
try:
    prob = float(model.predict_proba(X)[0][1])
    print("Probability:", prob)
except Exception as e:
    print("Prediction error:", e)
