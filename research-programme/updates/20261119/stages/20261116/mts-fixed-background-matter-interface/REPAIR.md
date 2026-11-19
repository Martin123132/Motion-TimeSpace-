# Preserved failed run and narrow floating-point repair

The original run completed all three panels, failing the deliberately
unstable-bath control each time. Its files and script remain in place.

Root cause: JSON represents integer-valued numbers without a decimal suffix.
The original np.diag constructor therefore created an integer matrix from
[2,3,5]; assigning -0.4 and -0.25 truncated both couplings to zero. Assigning
the small negative unstable diagonal likewise truncated it to zero.
The positive bath matrix was consequently wrong too, even though its separate
edge/matrix action check agreed because both used that same wrong matrix.

The repair explicitly makes the bath mass matrix floating point. It preserves
all parameters, seeds, tolerances, gauge operators, probes and saved fixtures.
Two independent guards now check fractional off-diagonal preservation and the
Schur-complement determinant identity. The expected negative eigenvalue of
the intentionally unstable fixture must pass the original separation floor.

Run the corrected copy in float-bath-repair. It reads the original cached NPZ
fixtures rather than generating new random data. Paths for inherited-source
verification and local receipts are adapted to that subdirectory. All
original panels, result.json, protocol and original source remain unchanged.
Authoritative acceptance is the corrected folder's result.json, not the
preserved failed result at the stage root. This is a representation repair,
not a theoretical change, threshold relaxation or fresh choice of data.
