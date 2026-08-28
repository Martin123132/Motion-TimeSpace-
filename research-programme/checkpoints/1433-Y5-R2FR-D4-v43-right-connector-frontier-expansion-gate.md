# 5417: v43 right-connector frontier-expansion gate

## Decision

**PASS FOR SAME-REVISION FRONTIER EXPANSION AND CONTINUED V43 PRODUCTION ONLY.**

A three-hour bounded continuation sequence advances the preserved `S_X006_MC04_SP_DP` right connector without adding an analytic repair. The split ledger retains exactly the four checkpoint-5416 classes, so this is genuine progress under the existing proof rather than another renamed target.

## Production evidence

- accepted boxes: `131 -> 233` (`+102`);
- pending boxes: `14` at maximum depth `17`;
- certified area coverage: `1.68609619140626% -> 6.378173828125%`;
- weakest new denominator margin: `0.00010237716235513576`;
- weakest new collision-Jacobian margin: `0.7281267861815186`;
- accepted plus pending area: `0.039327536205488567`.

All 102 newly accepted rows carry finite positive interval certificates. The depth-17 transition audited at checkpoint 5416 remains present unchanged, and no accepted row uses a point-only or fitted closure claim.

## Claim boundary

The right connector and 211 further contour jobs remain open. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.
