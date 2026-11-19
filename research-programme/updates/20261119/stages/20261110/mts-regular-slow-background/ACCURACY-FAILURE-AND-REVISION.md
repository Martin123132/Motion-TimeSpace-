# Preserved accuracy-test failure and bounded revision

The first planned run, baseline IntTolBoost12, failed and exited normally
with a failed worker receipt. No numerical packet or successful result was
saved. The loop stopped; IntTolBoost24 and the MTS attempts were not run.
The native messages reported Romberg tolerance2.5436656473769231e-20 and
DVERK failure at x=.0005, xend=.046917448974454871. This is an execution
failure, not a physical exclusion. No automatic identical retry is allowed.

Inspection now establishes why doubling this setting was inappropriate:
native camb_python.f90 uses tol=base_tol/exp(AccuracyBoost*IntTolBoost-1),
with base_tol=1e-4 in config.f90. At AccuracyBoost2.5, increasing the setting
6->12 requests a factor exp(15) tighter tolerance, not a factor2. Some
background integrations use an additional factor1/1000.

Instead freeze tolerance halving and quartering using

    IntTolBoost = 6 + ln(factor)/2.5,  factor in {2,4}.

These are distinct, mathematically specified refinements, not an identical
failed-run retry. Acceptance gates, action, source grids, initial data and
all other settings remain unchanged. Both cold and heavy receive both
refinements. The inappropriate12 test and its failure remain in the ledger.
