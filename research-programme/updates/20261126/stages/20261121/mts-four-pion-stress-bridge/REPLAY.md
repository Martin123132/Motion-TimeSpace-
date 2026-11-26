# Local offline replay

From this folder with the retained Python 3.13, NumPy and SciPy, set one numerical thread and run `python -B bridge.py`. The calculation verifies the previous 15-file seal before importing the original signed pion response. It verifies the eight local source tables and regenerates the numerical results without a network request. The intake module also uses Requests. Optional: `python -B intake.py --acquire` compares each versioned HEPData table to its saved copy, never replacing a differing file.

The evidence files are `stress-norm.csv` (nine energies), `input-targets.csv`, `window-moments.csv`, `angular-comparison.csv`, `aperture-rates.csv` and `checks.json`. All angles are CM angles, all energies GeV, cross sections nb. TSV previews and third-party figures are unnecessary. The files stay local; there is no active numerical worker or web service.

See [stress](STRESS.md) for the contact/pole cancellation and independent neutral field-coordinate check, [unitarity](UNITARITY.md) for the sign bound and counterexample, and [angular inputs](ANGULAR.md) for the actual calibration and exclusions. A successful replay tests the implementation, not the truncation error of leading chiral order.
