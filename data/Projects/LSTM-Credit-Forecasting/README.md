# LSTM Credit Spend Forecasting — UIUC × Synchrony Datathon

> Forecasting Q4 2025 credit-card spend across thousands of accounts to drive credit-line recommendations. Submission for the UIUC × Synchrony "Cache Me If You Can" Datathon.

## Problem

Given historical account-level transaction and spend data, forecast forward-looking quarterly spend so that high-value accounts can be identified for proactive credit-line increase offers.

## Approach

- Built a sequence model (**LSTM**) over per-account spend time series to capture temporal spending patterns.
- Engineered account-level features (recency, frequency, monetary signals, trailing-period aggregates).
- Forecast **Q4 2025 spend across 14,099 accounts** with a mean absolute error of **~$2,444**.
- Translated forecasts into **credit-line recommendations for 288 high-value accounts** (~2% of the segment), prioritizing accounts with the strongest projected spend lift.

## Files

| File | What it does |
|------|--------------|
| `lstm datathon (4).ipynb` | LSTM model: data prep, sequence construction, training, and Q4 forecasting |
| `cache-me-if-you-can-datathon-submission.ipynb` | Final datathon submission notebook — analysis, results, and recommendations |

## Stack

`Python` · `pandas` · `NumPy` · `TensorFlow / Keras (LSTM)` · `scikit-learn`
