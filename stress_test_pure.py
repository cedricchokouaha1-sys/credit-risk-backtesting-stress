# stress_test_pure.py
# Stress test crédit (pur Python, sans dépendances)
# - Génère PD / EAD / LGD synthétiques
# - Applique scénarios macro (facteurs simples sur PD)
# - Calcule Expected Loss (EL)

import math
import random

random.seed(1)

def mean(x):
    return sum(x) / len(x) if x else 0.0

def clip(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

def lognormal(mean_log=10.0, sigma=0.6):
    # approximation via random.lognormvariate(mu, sigma)
    return random.lognormvariate(mean_log, sigma)

def main():
    n = 30000

    # Portfolio synthétique
    pd_base = []
    ead = []
    lgd = []

    for _ in range(n):
        # PD base (petite en moyenne)
        # on génère une PD entre ~0 et ~0.2
        p = random.betavariate(2, 50)
        pd_base.append(p)

        # EAD : lognormal, borné
        e = clip(lognormal(10.0, 0.6), 1e3, 5e7)
        ead.append(e)

        # LGD : autour de 40%
        l = clip(random.gauss(0.40, 0.10), 0.10, 0.90)
        lgd.append(l)

    def expected_loss(pds):
        return sum(p * e * l for p, e, l in zip(pds, ead, lgd))

    def stress_pd(pds, shock_factor):
        # shock_factor > 1 augmente le risque
        return [clip(p * shock_factor, 0.0, 1.0) for p in pds]

    scenarios = [
        ("Base", 1.00),
        ("Adverse", 1.30),   # +30% sur PD
        ("Severe", 1.60),    # +60% sur PD
    ]

    base_el = None

    print("\n=== MINI STRESS TEST (PURE PYTHON) ===")
    for name, factor in scenarios:
        pds = stress_pd(pd_base, factor)
        el = expected_loss(pds)
        if name == "Base":
            base_el = el
        uplift = (el / base_el - 1.0) if base_el else 0.0
        print(f"{name:<7} | avg_PD={mean(pds):.4f} | EL={el/1e6:,.2f} M€ | vs base={uplift*100:,.1f}%")

    print("\nInterprétation (entretien):")
    print("- On applique des scénarios adverses (ici facteur sur PD) puis on recalcule EL = PD×LGD×EAD.")
    print("- On compare Base vs Adverse vs Severe : l’augmentation doit être monotone et cohérente.")

if __name__ == "__main__":
    main()
