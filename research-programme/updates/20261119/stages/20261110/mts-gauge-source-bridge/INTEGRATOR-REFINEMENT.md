# Internal step refinement, fixed physical test

The initial native-equivalent heavy run gave errors versus the saved fine
DOP853 state:8steps4.43835e-4,16steps2.64079e-5,32steps1.63071e-6.
The32-versus16difference still exceeded2e-5, so that attempt was not
accepted. The failure receipt and terminal values are retained; that first
checker did not save its arrays before raising. The updated checker saves
per-model progress before an acceptance failure.

The next paired check uses32/64 INTERNAL exponential steps and the same
2e-5 gate, initial states, RHS, frequency, background, data grid and
DOP853 reference. It does not alter the native saved output cadence or
claim8/16passed. This is ordinary integration-error refinement, not a
change of physical coefficients or evidence selection.
