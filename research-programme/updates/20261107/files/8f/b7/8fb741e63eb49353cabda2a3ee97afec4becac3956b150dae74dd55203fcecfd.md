# Stage126 — response-site source contract

The current inner reconstruction has40960 steps and the response2048.
The original65 source epochs define64 intervals, hence interval0 contains
640 inner steps and32 response updates.

The fixed response recurrence samples S at

    t_j=t0+(tf-t0)*j/2048, j=1,...,2048.

Within interval0 these are inner steps20,40,...,640. Stage125's
16-subinterval table supplied steps40,80,...,640. We add only the missing
odd sites20,60,...,620, retaining the actual saved initial condition,
piecewise-linear outer histories and65-knot inner coefficient bank.

For any two source representations agreeing at the recurrence's evaluation
sites, equal initial data implies equal subsequent states by induction:
at each BE/BDF2 step the matrix, stored history and source right-hand side
are identical. This is an exact statement about the chosen finite recurrence.
It does not imply the two continuous sources have the same physical effect.

We test three representations per background/window/source variant:
1. control:138 knots with the16 new values interpolated from the old122;
2. sites32:138 knots with the16 new physical-source evaluations;
3. collocated: values of sites32 at every actual response evaluation time,
   but with interval0 values supplied directly from the combined33 initial
   samples, eliminating an extra interpolation there up to coordinate roundoff.

Compare control with Stage125 and collocated with sites32. Only the sites32
versus Stage125 difference tests the new information. Inserted test bumps
between response sites, vanishing at every evaluation time, demonstrate
the sampler's blind spot and are never propagated as new physical inputs.

The retained conditional memory law is

    e(t)=U(t,t0)e0+integral_t0^t U(t,s)[f(s)-u'(s)]ds,
    S(t)=A(t)e(t).

No new initial-memory condition is fitted or derived here. Nor does evaluating
A at fresh temperatures refine the65-knot L bank inside U. Assembled and
direct source variants remain separate controls.

Success at32 sites closes interval0 source interpolation only for the current
inner trajectory and2048-step response. It cannot certify response-time
integration, the other63 intervals, the parent matching, or the collision
approximation. The next action should follow those distinctions, not continue
subdividing the same source between already supplied response evaluations.
