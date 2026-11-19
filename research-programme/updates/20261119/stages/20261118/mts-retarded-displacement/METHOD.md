# Retarded displacement: experiment fixed before scoring

Question: when is the slow-field displacement offset inherited by epoch 1999 generated, and can the retained stress equations predict it without reading later native scalar perturbations? Compare the same baseline and MTS, at k=5, with both the physical slow field and the passive archived-background-velocity diagnostic. No change to the action, preparation, scattering bank, original output grid or 2e-5 tolerance. No native run. Numerical archive comparisons are not observational tests.

Let x=kτ, h=H/k (conformal H), B=φ′/k, w=(am/k)², y=(δφ,∂xδφ), C=δc. The retained equation is y′=A y+(0,B C′), A=[[0,1],[-1-w,-2h]]. With S=switched and N=native, e=yS−yN satisfies

    e′=A_N e + (0, B_N (C′_S−C′_N) + (B_S−B_N) C′_S
                     −2(h_S−h_N)yS[1] − (w_S−w_N)yS[0]).

The two final-coordinate responses are the two rows of the fundamental matrix Φ_N(T,x); the retarded source kernels are their second entries. For each interval the endpoint-inferred innovation e[j+1]−Φ[j]e[j] measures the net two projected source moments, not a pointwise force. Transport these to T and sum by intervals defined by the native clock spacing (dense: Δx≤1/40), horizon x=1, the bracket containing the switch x=52, and the direct-capture start 1991. A sum that reconstructs the final offset from measured states is an accounting identity, not a successful forecast. Do not claim sub-interval timing for such sums.

Independent force route: the actual retained camb_python.f90 records the double-precision baryon+CDM growth g=(∂τD)/(HD), D=(1−f_b)δc+f_bδb, *not* the derivative of total matter including massive neutrinos. equations.f90 has δb′=C′−v_b in x and stores synchronous v_b, hence C′=(H/k)gD+f_b v_b. Use the saved δ_nonu transfer for D; independently use the two component density transfers. Bound the round-to-nearest single-precision inputs against both adjacent representable values. Validate at all 2262 archived RHS captures in each preparation. This route does not differentiate rounded δc, does not estimate a new coupling, and uses no scalar perturbation targets to reconstruct the force.

Freeze original-knot linear, cubic and shape-preserving interpolation of the four source products; compare integration-step halving. Independently integrate the scalar source forward from the first saved native state only and test the two coordinates at 1999. Give component and interval results, including mismatch against the measured innovations. Where interpolation or precision is insufficient, the endpoints constrain only the projected net contribution. A compactly supported force with zero endpoint moments can leave the entire pair of samples unchanged. Do not infer a uniquely measured force inside a sparse gap.

Propagator checks: Liouville determinant exp(−2∫h dx), independent refinement, and the check against the measured change in log(a). Compare epoch definitions and both controls. Keep the perturbation-position and perturbation-velocity tests separate from the pressure readout. Report accuracy on the actual discrepancy scale and on the native field scale; they are different questions.
