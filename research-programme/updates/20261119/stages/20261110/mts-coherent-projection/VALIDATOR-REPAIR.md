# Preserve and correct the derivative-verifier mismatch

The first validation run failed its1e-10 algebra gate. All numerical transport
packets and their original step/history tests remain unchanged. The failing
verifier is retained verbatim as verify_projection.py, with its failed
validate-start/end receipts.

diagnose_derivative.py shows the cause: at an unretained coarse-history knot,
the old test sent M built from the NATIVE background into the matrix RHS but
built the independent product-rule derivative with the COARSE interpolated
background. The vectors were not the same physical M=B U^T. Only heavy-coarse
is affected: normalized input mismatch2.60739e-9, derivative mismatch9.57141e-10.

The corrected algebra test constructs the same physical M with the same B
used by both derivatives, while retaining the native us/ws. Its maximum
heavy error is2.62117e-16. The baseline maximum is1.02225e-13, also below the
UNCHANGED1e-10 gate. The separate history-sensitivity comparison still tests
the actual coarse/native difference at its original2e-5 numerical gate.

This changes only the verifier's algebra input consistency, not the theory,
source curve, state transport, output packets, tolerances or physical tests.
verify_projection_consistent.py loads the preserved original verifier and
substitutes the tested same-state derivative comparison, a distinct receipt
label, and cleanup handling that explicitly preserves the failed validation.
