# 5456: D4 outer-parent leaf transplant smoke

## Decision

**OUTER_PARENT_TRANSPLANT_PARTIAL__TOP_PROJECTIVE_PIVOT_COVER_REQUIRED**

## Executable seam

The full inner-Q cover is complete. The outer geometry leaves therefore move to the checkpoint-5396 `evaluate_path_box` regular enclosure, augmented only by the derived stable deformed-recoil sheet chart below. The event principal pole is not reassigned to this evaluator: its exact `rho/delta` subtraction and logarithmic primitive remain owned by checkpoints 5450-5451.

For the deformed TOP contour, write `z=1-E=a+ib`, with `b` uniformly nonzero. The principal square root is `sqrt(z)=u+iv`, where `u^2=(sqrt(a^2+b^2)+a)/2` and `|v|^2=(sqrt(a^2+b^2)-a)/2`. Here `u` increases with `a` and `|b|`, while `|v|` decreases with `a` and increases with `|b|`. Directed endpoint evaluation therefore gives a rigorous positive-real-sheet rectangle and removes the inherited interval-wrapping false negative without adding a physical assumption.

The smoke selects both the maximum physical-path-area leaf and the minimum certified-gap leaf in every owner-cell/path group. It covers `77` representatives across `13` owner cells and all three contour segments. Passed: `4/4`.

## Claim boundary

This is a resumable partial smoke, not a transplant validation. It has completed 4/77 representatives. The next broad TOP leaf requires a finite projective-pivot cover; blind rectangular refinement is not accepted as the solution. Full event-cell coverage, event-local W3, the regulator limit, local GR and full MTS remain unclaimed.
