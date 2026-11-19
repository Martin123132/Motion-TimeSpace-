# Explicit proof-script repair

The first proof worker exited with an error before writing proof.json. Its
mass contribution accidentally used the unexpanded square-root prefactor
instead of the already-computed second-order expansion, so polynomial
coefficient extraction left the expansion parameter inside square roots.
This was a script variable-selection mistake, not a failed action identity.

The corrected worker is separately named proof-fixed. Original proof-start
and proof-end receipts remain, including the exact failing expression.
No output or scientific failure was silently overwritten; all identities
must be recomputed successfully before the corrected proof is accepted.
