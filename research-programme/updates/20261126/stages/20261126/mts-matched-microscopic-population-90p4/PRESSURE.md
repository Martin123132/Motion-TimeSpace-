# Independent pressure balance after restoring the branch clock

This is an exposed diagnostic, not a new choice of phase, window or acceptable error. Let M=am, X=kz, y=a(vf+bw)/ρ₀, d=a(vw+M²bf)/ρ₀, p=a(vw−M²bf)/ρ₀, r=k²/(4M²). Differentiating y with the two synchronous wave equations and a′=Ha gives exactly

    p = [y′ + H y + a b v X/ρ₀] / [2(1+r)] + r d/(1+r).

Test it without taking p as input: differentiate the saved y across each smooth branch, never across the switch, using degree 7 and 9 interpolants on the original half knots. The projected prediction is the sum of the differentiated envelope, H y, metric driving and gradient terms, with the coefficients INSIDE the projection. Compare against the direct kinetic-minus-potential prediction on the same 31 centers. The difference from the native fluid pressure splits into these terms, minus the native sound-speed expression. Score on pressure's own scale; also compare the pressure law evaluated on the predicted density and current versus evaluated on the native density and current to distinguish closure from trajectory error. Use field values and metric driving already saved; no fit, no change to the photon source and no special rule for pressure nodes.
