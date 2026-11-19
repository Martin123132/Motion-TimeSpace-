# Preserve the first precision-worker failure

The first precision worker stopped at its diagnostic normalization: mpmath 2x2 matrices require two indices, unlike NumPy flat indexing. The evaluated formulas were unchanged. check_precision.py and its frozen hash and failed receipts are retained. check_precision_v2.py changes only the matrix indexing plus its own receipt/input filenames; both precisions are then evaluated afresh. No physical tolerance, primitive input or source gate changes.
