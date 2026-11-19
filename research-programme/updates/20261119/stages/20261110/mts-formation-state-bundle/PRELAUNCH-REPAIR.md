# Pre-launch repair

2026-11-10: the first extraction command stopped at Python parsing, before
any numerical worker receipt or output existed. A missing opening bracket
in the symbolic transformation matrix was restored. The derivation's wording
now explicitly includes the standard density and velocity transfer columns
among the float32-buffered outputs. No numerical result, input, tolerance or
existing checkpoint was changed. Source hashes are frozen by the first
successfully started worker.
