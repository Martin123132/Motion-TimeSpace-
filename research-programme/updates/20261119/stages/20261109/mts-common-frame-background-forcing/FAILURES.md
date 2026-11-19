# Inspected setup failure

probe-half-01 exited1 before evaluating a frame: the existing native factory creates its case directory but expects the context parent to exist. The new wrapper had not made that parent. No scientific gate ran or failed. frame_source_v2.py creates the owned context parent before calling the unchanged factory; probe_frame_v2.py uses source-02 and new receipts. Original scripts, freeze and traceback remain untouched. This is a setup repair, not a retry of a rejected physical result.

