# Retained development receipt

collect-half-01 exited after its first native case because Python abs() was applied to a list of matrix differences. The source/physics checks had not reported a failure; the aggregation raised TypeError before a result was written.
The attempt, generated packets and exact collect_metric.py source remain intact and are not accepted as a completed result.
collect_metric_v2.py converts that list to an array, uses a fresh metric-02 destination and adds the derived full-row momentum identity check for both baseline and MTS. It does not change thresholds or numerical inputs.
This is an inspected implementation repair, not an automatic retry of a failed physics gate.
