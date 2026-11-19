# Direct quadrature readout precision

The first source replay preserved all old inputs and passed the saved
carrier-source map, but failed the stricter1e-10 algebra gate in the
independent arbitrarily rotated real-quadrature readout. Maximum normalized
difference was1.9144e-9. This attempt is saved, not accepted or erased.

The old normalizers resolve small density against a much larger phase
quadrature. Rotating both before forming dot products creates cancellation.
The next attempt changes only this independent readout to60digit arithmetic
on the same stored double inputs. It retains the original map, all input
states, synthetic rest sources, precision checks and tolerances. Outputs
and receipts are separate. Passing this does not imply physical accuracy
of60digits or an evolved late hierarchy.
