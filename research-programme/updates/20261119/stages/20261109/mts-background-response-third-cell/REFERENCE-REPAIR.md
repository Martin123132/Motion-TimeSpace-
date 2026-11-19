# Preserved failed reference check, corrected before acceptance

The first history attempt(history-balanced-01,Python29220,exit1 at11:18:29UTC) stopped at the unchanged carried-current gate. Inspection shows the evolved domain and phase/source/feedback slices used bank positions4:7, but the leading reference used2:5. That compared different physical epochs. This is an adapter error, not evidence of a physical instability. No new dense numerical packet or accepted history result was saved; the failed freeze, script and receipts remain untouched.

continue_current_v2.py uses ONE epoch_slice=slice(4,7) for every reference array, sample and stored-node check, and verifies incoming reference agreement BEFORE integrating. It records both the correct incoming error and the stale previous-leading error. It writes history-02; downstream v2 source/grid/batch adapters explicitly read that path. The physical RHS, parent raw states, normalization, original full-span step limits and tolerances are unchanged. The reviewed repair reruns only the rejected unsaved history calculation from the verified parent; no old accepted work is repeated.

Audit and cleanup must retain the failed history-balanced-01 exit1 and separately require history-balanced-02 exit0. No automatic retry or tolerance relaxation. The single-slice preflight prevents this indexing mismatch in later continuation adapters.
