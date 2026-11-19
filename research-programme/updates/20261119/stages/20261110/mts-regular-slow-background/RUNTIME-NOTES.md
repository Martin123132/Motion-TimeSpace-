# Numerical execution receipts

All workers use Python-B, one numerical thread, CPU4 and below-normal
priority. No subprocess service, compiler, browser, server or preview was
started. Exact PID/create-time/command receipts are retained per worker.

The original four native runs complete with error_code0. The tolerance
experiment initially requested IntTolBoost12 for the cold control and
failed. Native stdout reported two Integrate_Romberg warnings with tolerance
2.5436656473769231e-20, and DVERK failure x=.0005 to xend=.046917448974454871.
The numerical worker returned exit1 and its receipt states failed. The
controlling loop stopped. No boost24 or heavy boost12/24 run was started.

After reading the actual tolerance formula, four separately named factor2/4
tolerance refinements completed with error_code0. Heavy factor4 emitted:

    Integrate_Romberg failed to converge
    integral192.57607864970541
    error-2.7533531010703882e-14
    tolerance2.0788217977589195e-14

Do not treat code0 as erasing that warning. The factor4 output is retained
for diagnostics only; it is not a convergence certificate. The independent
canonical comparison fails for both heavy refinements anyway. No physical
acceptance threshold was relaxed. No identical failed-run retry occurred.

Final cleanup verification must allow the single documented failed receipt
while proving its process exited, not falsify it to obtain all-green workers.
