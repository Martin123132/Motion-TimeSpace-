# A shared gravity source, a predicted radiation reversal, and its origin in the stored scalar history

**The main result:** we can evolve the CDM, baryon and photon density perturbations from the original matched matter state without supplying interior densities. On the smoothly evaluated original background tables we derived and tested a sign change in the MTS radiation correction. Its initial curvature is almost entirely attributable to an inconsistency between the archived heavy-field slope and velocity, not independent evidence for a new radiation mechanism. The same early-time control on the baseline found no reversal in the MTS event window.

## What was calculated

The complete native hierarchies (182 cold / 185 heavy active variables) were initialized from the unchanged prepared mode. Both finite Euler velocities, the quadrupole and all other multipoles evolve; density differences use one gravitational source. The CDM drive follows from the finite flat Einstein constraint; baryon/CDM and photon/CDM differences cancel the common metric explicitly. The massive-neutrino contribution at fixed hierarchy uses dDν/d ln a = −Dν−3δPν integrated over the scale change. Twelve independent same-state finite-shift fixtures tested five reconstructed rates plus total density against the native calculation; the maximum rate discrepancy on the specified fixture scales was 2.20e-8. The rest of the hierarchy uses a numerical midpoint-centred amplified operator difference, not a new analytic theory for every multipole. See METHOD.md, coupled.py, the two fixtures files and verification.json.

The original early interval spans about 0.00986 conformal Mpc from preparation near 88.5884 Mpc. Initial physical fields and old perturbations are not initialized on any later probe. Capsule files retain both arbitrary-step and predetermined-node clock samples, terminal states and withheld endpoints. Fixed-step DOP853 trials recorded their original embedded errors; they are not passed off as accepted adaptive solutions. In the adaptive calculation the signed radiation evolves with the physical system. Absolute transferred energy was checked separately by locating sign changes and by independent quadrature, rather than letting a cusp in an auxiliary variable dictate the required physical time steps.

| Original interval, smooth polynomial reference | Baseline | MTS parent |
|---|---:|---:|
| Signed integral, original binary geometry preparation | 6.34671921e-27 | 1.79440483e-20 |
| Signed integral, geometry explicitly rematched to same smooth reference | 6.78812942e-28 | 1.79438217e-20 |
| Relative change from that initialization choice | 89.30% | 1.263e-5 |
| Rematched correction / original elastic radiation integral | 1.843e-17 | 5.413e-9 |
| Rematched combined step / quadrature budget relative to signed result | 2.70e-10 | 2.55e-9 |

Integrals are in the retained mode normalization. The table is an internal perturbation result, not a sky-calibrated spectrum. The smooth reference uses the original coefficients and an explicitly declared arithmetic interpretation. It is not the same as requiring the original individually rounded native operations to pass. Those adaptive trials reached 80.5% and 91.8% of the interval (baseline) and 20.3% and 3.2% (MTS) before their evaluation budgets. Their actual last accepted states are saved; none is a completed binary-reference result. Original numerical gate 2e-5, algebra gate 1e-10. No fits, new observations or galaxy inputs.

## Prediction and falsification

For a genuinely matched smooth start, the initial matter and background differences vanish. The changed energy starts at order T²; the initial slope of the relative transfer rate is −2(H1−a0′/a0). A scale mismatch instead contributes a term of order T in the accumulated energy. The first-order approximation to the *ratio of integrals* failed its original slope-normalized tolerance on the first five probes, including a wrong sign on the shortest initial MTS probe. We kept that result and derived the curvature from the two Euler equations, Friedmann derivatives, original clock polynomial and opacity; no fitted slope or cutoff. The frozen curvature prediction passed on 4/5 new elapsed times for the smoothly rematched baseline and 1/5 for MTS; the latter passes on its shortest time. All ten exposed comparisons are distinguished from the new cases. See ONSET.md, CURVATURE.md and the frozen and test packets.

The coefficients then predicted the excess **rate** would reverse before the **accumulated excess energy**, inside the preparation cell for MTS. On two new integrations and two resolutions for locating crossings:

| Crossing | Frozen prediction (elapsed conformal Mpc) | Direct evolution | Relative timing error |
|---|---:|---:|---:|
| Rate | 1.07213786e-7 | 1.07216714e-7 | 2.73e-5 |
| Integral | 1.60820676e-7 | 1.60825671e-7 | 3.11e-5 |

Signs and order were correct; both timings narrowly **miss** 2e-5, even before the root-resolution allowances (5.31e-7 and 1.77e-7). No resolved crossing for baseline over the same elapsed span. These are reversals of a difference, not of total radiation. See REVERSAL.md, reversal-frozen.json and both direct results.

## Why it happens, and a tested alternative

At matched preparation, the changed relative acceleration contains −(H1′−H0′)v_b. The baryon velocity divided by the photon–baryon slip is about −6305 in the MTS cell, so a tiny derivative inconsistency matters. Splitting the Friedmann derivative into the original species gives **99.9394% of the signed initial energy-ratio curvature** from the heavy-field term proportional to v−φ′_table; its acceleration discrepancy adds 0.0684%, with other signed terms partly cancelling. This is attribution of the *initial Taylor coefficient*, not 99.94% of the entire signal, an observation, or a measured galaxy force. See mechanism.json.

We tested a joint representation rather than merely flagging the defect. A cubic uses the neighbouring tabulated field values and velocities. A quintic also uses the parent equation for endpoint accelerations. Neither uses the omitted field knot to construct its forecast. The heavy quintic recovered all nine omitted knots on field/velocity amplitude scales and passed the independent force equation at 6/6 sampled interior positions; the heavy cubic passed 0/6 force checks. At the true start the quintic nevertheless shifts H by 1.95e-8 relative to its original reference. It has not been inserted into the bank or used to claim a radiation pass. For the baseline slow field both alternatives matched the nine knot-amplitude checks but failed 6/6 interior force checks; a quintic velocity error reaches 6.31% on its **own** scale. Applying the heavy repair to both models silently would be wrong.

Lastly we integrated the archived velocity across nine original intervals and asked whether one initial position could account for all ten rounded field values. Even expanding the allowed rounding intervals by the numerical quadrature allowances leaves no common position. The gap is 0.674 initial-position word widths for the baseline and 4.33e7 for the heavy field. This is conditional on those tabulated velocity curves; it does not establish that any individual observation or the underlying field equation is wrong. See FIELD-CONTROL.md, KNOT-COMPATIBILITY.md and field-verification.json.

## Next physical calculation

Shoot the two-component physical field (φ,v) from an independently retained neighbouring knot using its equation of motion and common expansion. Predict interior knots that were not used for preparation; score positions, velocities and the acceleration defect on their own scales. For the nearly stationary baseline, test a velocity-first reconstruction with an explicit allowed position offset rather than differentiating rounded positions. If supported, compare matched radiation again on the original cells to separate a representation correction from a physical source. No change to the epoch-4252 restart, no full-history extension and no public update.

The first curvature control failed because it mixed an unrounded scale with the high/low-word reference while asserting an exactly vanishing initial displacement. It is retained alongside its original frozen file and the v2 identical-state check. The first field-knot checker compared Decimals rounded at different working precisions; v2 compares at the same precision before using the exact original knot words. Neither changed the physics tolerance. The separate manufactured polynomial verifier also treats the constant term at zero as one rather than asking Decimal for 0^0.
