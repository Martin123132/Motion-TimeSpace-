# Preserved preflight source-copy failure

preflight-01 correctly rejected a nonidentical local evaluator before source calculations. Its only difference from the accepted parent was one extra trailing LF: parent1528bytes/SHA256fa43b4f2051981b118d660593fde1c25263ef9eb44d1a9c1d6be29fb75fbfe1c; unqualifiedcopy1529bytes/SHA2562b39a0ca6e3ae874ec604b1fbcf5c22ef9c373e53fa497f1c91ede2d47ffc9ac. Text with trailing whitespace removed was identical. The unqualified file is retained unchanged as real_series_unqualified_copy.py.

The local real_series.py is restored byte-for-byte to the accepted parent, retaining the SAME exact hash requirement (not replacing it with a looser test). preflight_v2.py uses a new output folder and attempt. Original preflight code, failed receipt and empty output directory remain. No numerical source, propagation or physical comparison was run by the failed preflight; no physics, arithmetic, bank, grid, source coefficient or tolerance changed. audit_continuation_v2.py recognizes this single diagnosed preflight failure while requiring every actual calculation to succeed.

A combined move/add patch was rejected atomically because it targeted the same path twice; separate move and add patches preserved the original copy and created the corrected copy. No partial mutation occurred from the rejected patch.

