# FitBurn — Calorie Burn Predictor

A 2nd-year B.Tech AI/ML project by Vikranth Reddy (Woxsen University).

## What it does
Predicts the calories burned by a workout from age, weight, duration, average heart rate and workout intensity (MET level).

## Model
- Ridge regression (alpha = 1.0) on standardised features
- Trained on 600 synthetic workouts (seed 42)
- 5-fold cross-validation: R² = 0.907, MAE = 89.8 kcal, RMSE = 116.3 kcal
- Baseline (predict the mean): MAE = 310.6 kcal — the model is ~3.5x better

## Files
- `train.py` — generates data, trains the model, writes `model.json`
- `model.json` — learned means, standard deviations, coefficients, intercept
- `index.html` — interactive demo; the browser runs the exact same weights as Python

## Live demo
https://fitburn.vercel.app
