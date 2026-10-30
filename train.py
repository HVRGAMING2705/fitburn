import json, numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

rng = np.random.default_rng(42)
n = 600
age = rng.uniform(16, 65, n)            # years
weight = rng.uniform(45, 110, n)        # kg
duration = rng.uniform(10, 120, n)      # minutes
avg_hr = rng.uniform(90, 175, n)        # beats per minute
intensity = rng.uniform(3, 10, n)       # MET level of the workout
# Generative calorie burn: classic MET formula (0.0175 * MET * kg * min)
# plus a heart-rate term, then realistic noise.
y = (0.0175 * intensity * weight * duration
     + 0.35 * (avg_hr - 90) * duration / 60
     + 0.02 * weight * (age - 30) * -0.15
     + rng.normal(0, 35, n))
y = np.clip(y, 30, 1500)
X = np.column_stack([age, weight, duration, avg_hr, intensity])
names = ["age_years", "weight_kg", "duration_min", "avg_heart_rate", "intensity_met"]
mu, sd = X.mean(0), X.std(0)
Xs = (X - mu) / sd
model = Ridge(alpha=1.0).fit(Xs, y)
kf = KFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(Ridge(alpha=1.0), Xs, y, cv=kf)
r2 = float(r2_score(y, pred_cv)); mae = float(mean_absolute_error(y, pred_cv))
rmse = float(np.sqrt(mean_squared_error(y, pred_cv)))
base_mae = float(mean_absolute_error(y, np.full(n, y.mean())))
print(f"CV R2={r2:.3f} MAE={mae:.2f} RMSE={rmse:.2f} baseline_MAE={base_mae:.2f} mean_cal={y.mean():.1f}")
print("coef", model.coef_, "intercept", model.intercept_)
mj = {"features": names, "means": mu.tolist(), "stds": sd.tolist(),
      "coef": model.coef_.tolist(), "intercept": float(model.intercept_),
      "metrics": {"cv_r2": r2, "cv_mae": mae, "cv_rmse": rmse, "baseline_mae": base_mae, "mean_calories": float(y.mean()), "n": n}}
with open("model.json", "w") as f: json.dump(mj, f, indent=1)

def predict(v):
    z = (np.array(v) - mu) / sd
    return float(model.intercept_ + z @ model.coef_)
samples = [[22, 68, 45, 140, 7.0], [45, 90, 30, 110, 4.0], [30, 75, 90, 155, 8.5],
           [19, 55, 60, 130, 6.0], [55, 100, 20, 100, 3.5]]
for s in samples: print(s, round(predict(s), 2))
