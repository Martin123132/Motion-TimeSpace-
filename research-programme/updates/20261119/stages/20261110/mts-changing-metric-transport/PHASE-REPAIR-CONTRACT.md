# Preserve a small physical beat beside a large carrier phase

Frozen after the native continuity diagnostic, before evaluating this repair.
That diagnostic passes for both retained histories; it did not reproduce the
microscopic density discrepancy. Do not blame the native solver from that
failed hypothesis. Keep its result unchanged.

The transport code accurately evaluates the small beat Wk-W0, but subsequently
forms the large floating-point sum theta0+theta_beat before taking sine/cosine.
At this interval's roughly32000radian carrier angle, argument rounding can be
comparable to the beat of the lowest-k modes. Density reads out a small real
part beside a much larger phase response, so normalized field convergence
alone is not an adequate density accuracy guarantee.

Use the exactly equivalent angle addition identities instead:

    cos(theta0+beat)=cos(theta0)cos(beat)-sin(theta0)sin(beat),
    sin(theta0+beat)=sin(theta0)cos(beat)+cos(theta0)sin(beat).

Do not add the angles first. This is a binary64 evaluation repair, not a new
frequency, pressure law, coupling, source, grid, tolerance or state selection.
The original source/model/transport files and failed outputs remain intact.

First change only the endpoint basis, reusing integral8192, to isolate this
mechanism. Record both original and conditional dressed initial states. Then
recompute the unchanged full forcing integral with separate rotations at4096
and8192panels,16nodes,eight panels/batch. Retain all399modes, the original
normalizers and the2e-5 gate. Cold remains the saved physical Euler control.
Native comparison failures remain reportable even if numerical checks pass.

Validate the separate rotation against80digit trigonometric evaluation of
the represented carrier and beat at a low-k mode, the worst failing original
mode, and the four original direct-control modes. This validates evaluation,
not physical initial data or the exact background's full uncertainty.
