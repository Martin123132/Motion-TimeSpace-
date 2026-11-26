> Public reading copy: local links are mapped to released material or marked unavailable. Machine-specific passages, where present, have been omitted. See the inventory for the original digest.

# The switch-time wave predicts the next squared-flux correction

**Local retrospective simulation test, 24 November 2026.** The heavy geometric source no longer needs the later resolved wave as an input over this tested interval. The original companion stress and other downstream histories were held fixed to isolate this change. No observed photons or new cosmological parameters entered the comparison.

The last resolved input was at 89.14375 conformal Mpc, before the 89.148503803 switch. The calculation evolved 782 input modes; its outgoing squared-flux correction was frozen before scoring. A separate replay masked the entire later native wave and later phase-table values, removed the native matched initial-state table, and regenerated all nine forecast arrays identically using the same mode-pair geometry. [Frozen receipt](evidence-001.zip) (archive member: `frozen.json`) · [masked replay](evidence-001.zip) (archive member: `blind-replay.json`) · [equations](DERIVATION.md).

| Frozen six-period preparation, complex peak-relative error | First stress cycle (15 knots) | Through 89.6 Mpc (73 knots) |
|---|---:|---:|
| Squared-flux correction vs native wave minus matched | 0.018722% | 0.019133% |
| Time derivative of that correction vs native | 0.003281% | 0.003887% |
| Correction vs heavy-pair reconstruction using the later wave | 0.000138% | 0.000590% |
| Shorter, four-period input: correction vs native | 0.018727% | 0.019630% |

Setting the correction to zero produces 100% source error. No phases, amplitudes, steps or tolerances were adjusted after the freeze. The shorter-input control is not the reported primary solution. [Full scores](evidence-001.zip) (archive member: `source-scores.csv`).

| Through 89.6 Mpc | Coarse gravity step | Fine gravity step |
|---|---:|---:|
| Peak metric-rate error, photon launch | 0.45799% | 0.45821% |
| Peak metric-rate error, second launch | 0.31327% | 0.31338% |
| Photon correction, momentum-constraint drive, % of original joint launch | 0.00362484% | 0.00362483% |
| Photon correction, differentiated-curvature drive, same units | 0.00365848% | 0.00365045% |
| Difference between drive routes, % of the small correction vector | 0.93481% | 0.71034% |

Both launches pass the 0.5% metric check at both steps (unchanged matched photon launch previously 1.3424–1.3425%). Both photon estimates lie below 0.163% of launch, with the cold history unchanged. Photon time, angle and gravity refinements pass. The two drive routes **do not** agree to 0.5% of the much smaller correction itself. The end-of-window cancellation survives this source test; the retained discrepancy is essentially unchanged by replacing the oracle with the forecast. No new evolution interval or authoritative matched restart is claimed. [Photon readouts](evidence-001.zip) (archive member: `photon-scores.csv`) · [precision controls](evidence-001.zip) (archive member: `photon-controls.csv`) · [p16 metric](evidence-001.zip) (archive member: `metric-p16.csv`) · [p32 metric](evidence-001.zip) (archive member: `metric-p32.csv`).

**Next, using these saved histories first:** propagate the signed difference of metric-rate routes as its own photon source. Separate the matched constraint residual from the explicit-wave reference residual and check the switch-end derivative stencil separately from the interior. Their vector sum must reproduce the measured 0.935% / 0.710% differences before we attribute either to a physical source or change a step. This does not require extending the evolution.
