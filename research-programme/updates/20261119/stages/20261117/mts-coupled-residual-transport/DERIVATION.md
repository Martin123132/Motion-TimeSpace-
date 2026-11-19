# Coupled residual transport, not a fitted error curve

The retained perturbation system is linear on its fixed active regime at a
specified homogeneous background. Its heavy branch selector is metadata held
at its saved value, not a freely varied perturbation. Inactive seeds are equal
between physical evolutions; their affine contribution cancels. The homogeneous
background equations are independent of these linear perturbations.

Write the parent and approximate active states as y'=A y+c and
yt'=A yt+c-r. The known second-order field residual r is nonzero only in the
heavy f/g slots. Subtraction derives e=yt-y and e'=A e-r. This includes the
metric constraint and every retained species, not a prescribed metric force.
The exact variation-of-constants solution is
e(t)=U(t,t0)e(t0)-integral[U(t,s)r(s) ds].
Consequently ||e(t)|| <= ||U(t,t0)|| ||e(t0)|| +
integral[||U(t,s)|| ||r(s)|| ds]. We do not claim a certified numerical bound
on U from this identity; this stage validates the driven error evolution.

For original/coherent background operators A0 and A1, store errors e0 and de:
e0'=A0 e0-r0;
de'=A1 de+(A1-A0)e0-dr.
The second formula avoids subtracting the two large physical trajectories.
The residual and its change are obtained from the already derived
R=E^-1 C K2 (I+K1+K2)^-1 E x, never from the measured discrepancy.
An unequal background would add (At-A)y plus ct-c. This implementation uses
ONE live background for both independent perturbation evolutions, exactly as
the retained equations permit; it does not silently discard this extra term.

K1/K2 obey their retained recurrences and start at zero only at3040. Parent
and approximate perturbations and work integrals are integrated independently.
The transported error is a third independent ODE, not yt-y stored under another
name. The extended state retains K, defect work, parent state and error when
crossing3041. Error normalization is state_units*1e-7, with the original/change
factor1e-5 unchanged; it does not change the physical normalization or gates.

At fixed background each physical readout is a linear functional B(t)y;
its predicted discrepancy is B(t)e. Heavy sources are
beta*(mu^2 Phi ef+V eg, k V ef, V eg-mu^2 Phi ef).
Actual derivative observables would ALSO need the instantaneous -r term.
This stage predicts source and five value readouts, not their derivatives.
Raw approximate metric/exchange gates still use the previously derived
actual-RHS correction; none is excused by subtracting the transported error.

Before evolution: test zero/affine offsets, additivity and homogeneity for both
backgrounds and baseline/MTS, including inactive seed cancellation, at three
saved times. Sampled numerical checks support the declared native regime, not
a theorem for all backgrounds or selector changes. Freeze clocks, code and
unchanged1e-10 algebra/2e-5 numerical gates before scoring.

First replay3040..3041 jointly to test the NEW transport, comparing also with
the independent saved direct/approximate histories. Full-norm accuracy and
error-relative resolution are separate. Only after the primary replay gates
pass may the COMPLETE state continue3041..3042, with baseline direct32/64 on
that new interval. No future metric/source history drives the ODE. Original
background/thermodynamic tables remain inputs. No new fit, field or parameter.
