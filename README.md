# Credit Risk – Backtesting & Stress Testing (Pure Python)

## Overview
This project illustrates a simplified implementation of:
- PD backtesting by deciles
- Model calibration analysis (Brier score)
- Credit stress testing under adverse scenarios

The implementation is intentionally done in **pure Python**, without external libraries, to ensure compatibility with constrained banking environments.

## Backtesting
- Segmentation of exposures into PD deciles
- Comparison between average PD and observed default rate
- Calibration diagnostics

## Stress Testing
- Base / Adverse / Severe scenarios
- PD shocks applied at portfolio level
- Expected Loss projection: EL = PD × LGD × EAD

## Context
This type of analysis is typically used as input for:
- Model performance monitoring
- ICAAP stress testing exercises
- Risk management decision-making

## How to run
```bash
py backtesting_pure.py
py stress_test_pure.py
