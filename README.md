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

## Results (Example Output)

### PD Backtesting
Example output obtained after running `backtesting_pure.py`:

Observations: 40000  
Brier score: 0.11  

Deciles (sorted by increasing PD):

Decile | Avg PD | Observed DR | DR - PD
1 | 0.025 | 0.029 | +0.003
2 | 0.035 | 0.034 | -0.002
3 | 0.050 | 0.052 | +0.002
...
10 | 0.377 | 0.384 | +0.007

**Interpretation**  
- Default rates increase monotonically across PD deciles  
- Observed default rates are close to average PD  
- Model calibration is globally satisfactory

---

### Credit Stress Testing
Example output obtained after running `stress_test_pure.py`:

Base | avg_PD = 3.87% | EL = 12.17 M€
Adverse | avg_PD = 5.03% | EL = 15.82 M€ (+30%)
Severe | avg_PD = 6.19% | EL = 19.47 M€ (+60%)
**Interpretation**  
- Expected losses increase consistently with scenario severity  
- Stress impacts are monotonic and economically coherent  
- This type of analysis can be used as input for ICAAP exercises
