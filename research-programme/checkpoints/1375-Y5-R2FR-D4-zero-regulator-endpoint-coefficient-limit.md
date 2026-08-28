# 5359 - D4 zero-regulator endpoint coefficient limit

## Decision

`D4_ZERO_REGULATOR_EIGHT_ENDPOINT_COEFFICIENT_LIMIT_DERIVED__FIT_INTEGRATED_D4`

## Exact local reduction

The positive-regulator target branch has

`q(0)=-5/4`, `q'(0)=-i/32`, `w(0)=-i sqrt(5)/2`.

Conjugation symmetry makes the real event map even in the regulator.  For each material polynomial `P_j(R,c,d,q)=0`,

`a_e = z0'_e(0) = i R_e (partial_q P_j)/(16 partial_R P_j)`.

The endpoint-coordinate derivative `z1_e(0)` is obtained from the exact hard-boundary and material-pole derivatives proved in checkpoint 5358.  No finite-regulator fit supplies either local factor.

## Parent residue

The remaining factor is evaluated as the parent Laurent coefficient

`C0_e(0)=M_phys Res_{E=E_e}[Delta_w o_e K_e/(y_e z_e J_e)]`,

with `K_e=lim_(zeta->z_e) (zeta-z_e)^2(F_direct+F_sub)`.  Reciprocal `SM/DM` events use `y=1/y_-` and the `v` labels; representative `SP/DP` events use `y=y_-` and the `u` labels.  This also handles the two desingularized `s14` collision events without reinstating a simple-root axiom.

## Eight limits

| event | C0(0) | a=z0'(0) | z1(0) | A_e(0) | radius |
|---|---:|---:|---:|---:|---:|
| E01 | -62.10552284485105586668664691532702239384 | 0.006760905058930296021294588153660014834982 i | -2.297058085471188729898917490410134616458 | 0.1827944823185147595919483741317001463061 i | 6.164563091027475931264166098370680343481e-24 |
| E02 | 6.387314063799641476563759021626777943647 | -0.00129329571235235894544518397388113566324 i | -1.646309444508955086703097570375158342767 | 0.005017699387993193319407780141979140719719 i | 1.776941440718198720550701625451600226008e-25 |
| E03 | 16.60241263745955795394238917640137126098 | -0.01045513814604213633086704322470788289924 i | -15.59128989355664955875522842956167634771 | 0.01113317235888035079635648122375485414082 i | 1.301521972377933969075264753188638056876e-24 |
| E04 | -0.0008854080584659677387786915570995580546696 | 0.000007140856414251695437704212245365744849876 i | 0.1771235692251388109408539017170046301757 | 0.00000003569582433995743643549614977330913160586 i | 4.105044830865201586459028487185221712215e-26 |
| E05 | 0.0008704766134911317235057369896423806311692 | -0.000003194615502326122619498543799863209482262 i | 0.1151416356446172643884320445820919767833 | 0.00000002415145545138966206937626272989316459458 i | 2.658855309691887015498694573133770669771e-26 |
| E06 | 0.001355980021842405766568976900217584529267 | -0.00002029105396415955574257092499919480489729 i | 0.7389413500256232867529611941858231032437 | 0.00000003723470583500630052379634424546092434401 i | 8.055282879053840173623174532485171337417e-26 |
| E07 | -0.0006365664587711333588280934606299782934474 | -0.0000245614444083080707135678170353957473227 i | 0.615166798629279997986834911561021500132 | -0.00000002541585749448563821585489661485450210584 i | 9.606170095523907706367409664264497959876e-26 |
| E08 | -173.6693227407891406300124286714545371493 | -0.05485479991261938186177818444016659878749 i | 35.05105653740899738023142488428374199324 | 0.2717919769333812242043525758619029493496 i | 4.362261061587697916214195420270869062656e-23 |

## Sum and independent ladder check

- Direct zero-regulator sum: `5.9332230508928156e-30 + 0.47073740266489766 i`.
- Direct disk radius: `5.1510643354505556e-23`.
- Checkpoint 5357 extrapolated intercept: `1.9794425833767675e-06 + 0.4707373916054135 i`.
- Direct-to-ladder distance: `1.9794734787501256e-06` against the frozen ladder envelope `1.9201925077212943e-05`.

The direct result is purely imaginary to its numerical certificate.  The small real intercept in the six-rung fit is therefore a finite-rung/extrapolation artifact, not a new parent coefficient.

## Claim boundary

- `valid_for_D4_zero_regulator_parent_residue_evaluation`: `True`.
- `valid_for_D4_zero_regulator_eight_endpoint_coefficients`: `True`.
- `valid_for_D4_endpoint_coefficient_regulator_zero_limit`: `True`.
- Integrated D4, outer-regulator, angular, phase-space, local-GR and full-MTS claims remain false.

## Next obstruction

Insert the derived endpoint coefficient into the preregistered integrated D4 asymptotic, perform the endpoint subtraction at each rung, and prove or bound the analytic remainder before fitting the fixed-decay outer-regulator limit.
