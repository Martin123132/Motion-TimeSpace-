from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4149-Y5-R2FR-Gamma-eff-extremum-source-zero-lock-or-phi-charge-bound.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_GAMMA_EXTREMUM_SOURCE_ZERO_OR_PHI_CHARGE_4149"
CHECKPOINT_ID = "4149"
DECISION = "GAMMA_EXTREMUM_DOUBLE_ZERO_LAW_DERIVED_RESPONSE_DOUBLET_ROUTE_BEST_CURRENT_SOURCE_ZERO_UNSIGNED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4149_00_4148_doc": (
        ROOT / "4148-Y5-R2FR-local-phi-freeze-no-scalar-charge-or-coupling-drift-bound.md",
        "Gamma_eff+C",
        "4148 selected Gamma_eff source-zero as the next root obstruction.",
    ),
    "SRC4149_01_4148_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4148_NEXT_TARGET.csv",
        "J_phi=0",
        "Machine-readable 4148 handoff.",
    ),
    "SRC4149_02_4148_source_ledger": (
        SOURCE_DIR / "P8_Y5_R2FR_4148_PHI_SOURCE_LEDGER.csv",
        "MISSING_GAMMA_EXTREMUM_LOCK",
        "4148 source ledger identifying the Gamma extremum blocker.",
    ),
    "SRC4149_03_GK_contract": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
        "GK513_3_double_zero",
        "Gamma/Khat first-variation double-zero contract.",
    ),
    "SRC4149_04_GK_integrability": (
        SOURCE_DIR / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
        "IG513_4_fixed_point_double_zero",
        "Gamma/Khat integrability gates.",
    ),
    "SRC4149_05_Gamma_owner": (
        SOURCE_DIR / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
        "Gamma_eff = Gamma0 + 1/2 M_AB",
        "Response-doublet quadratic density candidate.",
    ),
    "SRC4149_06_response_doublet": (
        ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
        "response-doublet double-zero remains a viable conditional route",
        "Prior response-doublet source-current zero attempt.",
    ),
    "SRC4149_07_response_source_ledger": (
        SOURCE_DIR / "P8_RESPONSE_DOUBLET_EULER_SOURCE_LEDGER.csv",
        "Y5_source_normalization",
        "Response-doublet source-current blocker ledger.",
    ),
    "SRC4149_08_Ward_contract": (
        SOURCE_DIR / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "C7_second_order_source_closure",
        "Source-owner Ward contract and source residual caveat.",
    ),
    "SRC4149_09_script": (
        SCRIPT_PATH,
        "GAMMA_EXTREMUM_DOUBLE_ZERO_LAW_DERIVED_RESPONSE_DOUBLET_ROUTE_BEST",
        "This generator records the 4149 Gamma extremum/source-zero lock attempt.",
    ),
}


def common() -> dict:
    return {
        "timestamp_utc": TIMESTAMP,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
    }


def write_csv(path: Path, rows: List[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4149_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4149_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4149_GAMMA_EXTREMUM_LAW": SOURCE_DIR / "P8_Y5_R2FR_4149_GAMMA_EXTREMUM_LAW.csv",
        "P8_Y5_R2FR_4149_RESPONSE_DOUBLET_ROUTE": SOURCE_DIR / "P8_Y5_R2FR_4149_RESPONSE_DOUBLET_ROUTE.csv",
        "P8_Y5_R2FR_4149_SOURCE_ZERO_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4149_SOURCE_ZERO_AUDIT.csv",
        "P8_Y5_R2FR_4149_PHI_CHARGE_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4149_PHI_CHARGE_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4149_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4149_DECISION_GATES.csv",
        "P8_Y5_R2FR_4149_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4149_STATUS.csv",
        "P8_Y5_R2FR_4149_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4149_NEXT_TARGET.csv",
    }


def source_rows() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        exists = path.exists()
        text = read_text(path) if exists and path.is_file() else ""
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "needle": needle,
                "role": role,
                "exists": str(exists),
                "needle_found": str(bool(exists and needle in text)),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def extremum_rows() -> List[dict]:
    return [
        {
            **common(),
            "law_id": "GE4149_0_background_subtraction",
            "statement": "amplitude zero is not first-variation zero",
            "formula": "choose C=-Gamma_eff(Phi0) so Gamma_eff(Phi0)+C=0",
            "derivation": "This removes the constant local source but says nothing about delta(Gamma_eff+C).",
            "result": "AMPLITUDE_ZERO_ONLY",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "law_id": "GE4149_1_extremum_condition",
            "statement": "Gamma source-zero condition",
            "formula": "delta(Gamma_eff+C)=D_A Gamma_eff|_0 delta Phi^A + delta_source Gamma_eff|_0 + delta_domain Gamma_eff|_0 + ...",
            "derivation": "Since C is a fixed subtraction, the phi source vanishes only if every first-variation channel vanishes.",
            "result": "FIRST_VARIATION_ZERO_REQUIRED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "law_id": "GE4149_2_Jphi_lock",
            "statement": "J_phi zero from Gamma extremum",
            "formula": "J_phi=(2 zeta_phi/3)delta(Gamma_eff+C)+J_matter+J_domain+J_boundary+J_memory+J_mixed",
            "derivation": "J_phi=0 requires the Gamma first variation plus all ordinary/source/domain/boundary/mixed channels to vanish together.",
            "result": "SOURCE_ZERO_LOCK_CONDITIONS_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "law_id": "GE4149_3_double_zero",
            "statement": "local double-zero law",
            "formula": "Gamma_eff+C=O(Z^2) near the local branch implies Gamma_eff(Phi0)+C=0 and D_A Gamma_eff|_0=0",
            "derivation": "A quadratic/even owner is the clean route to zero amplitude and zero linear source without tuning per arena.",
            "result": "DOUBLE_ZERO_LAW_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def response_doublet_rows() -> List[dict]:
    return [
        {
            **common(),
            "route_id": "RD4149_0_even_density",
            "route": "response-doublet even Gamma density",
            "formula": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4), Z^A=(R_+^A-R_-^A)/2",
            "derivation": "After C=-Gamma0, Gamma_eff+C=O(Z^2), so D_A Gamma_eff|_{Z=0}=0.",
            "route_result": "BEST_DERIVED_DOUBLE_ZERO_ROUTE",
            "current_status": "CONDITIONAL_NOT_LIVE_SIGNED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "route_id": "RD4149_1_phi_source_result",
            "route": "J_Gamma vanishes if physical local residual is Z=0",
            "formula": "J_Gamma=(2 zeta_phi/3)delta(Gamma_eff+C)=O(Z deltaZ), hence J_Gamma|_{Z=0}=0",
            "derivation": "The response-doublet route kills the Gamma contribution to the phi source at the branch.",
            "route_result": "J_GAMMA_ZERO_CONDITIONAL",
            "current_status": "requires Z physical lock and source-current zero",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "route_id": "RD4149_2_why_not_claimed",
            "route": "response-doublet promotion blockers",
            "formula": "need parent doublets, M_AB positivity, J_Z=0, B_Z=0, Y5 source-normalization silence, Y6 stress invisibility, and PPN lock",
            "derivation": "Prior response-doublet work shows the formal double-zero survives but source-current and local-test locks do not close.",
            "route_result": "CURRENT_SOURCE_ZERO_UNSIGNED",
            "current_status": "no local-GR/Newton/PPN claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "route_id": "RD4149_3_nonresponse_routes",
            "route": "positive auxiliary/topological routes",
            "formula": "positive auxiliary requires source-free no-hair; topological route requires exact bulk plus zero boundary flux",
            "derivation": "Both are valid theorem targets but require the same source-zero/boundary-zero type premises.",
            "route_result": "RETAINED_AS_BACKUPS",
            "current_status": "less direct than response-doublet for F_1=0",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def source_zero_audit_rows() -> List[dict]:
    return [
        {
            **common(),
            "audit_id": "SZ4149_0_parent_doublets",
            "requirement": "every physical local residual channel has parent-owned R_+^A,R_-^A doublets",
            "formula": "Z^A=(R_+^A-R_-^A)/2 is the actual local residual variable",
            "current_status": "NOT_DERIVED_FOR_ALL_CHANNELS",
            "residual_if_failed": "Gamma double-zero may be formal but not physical",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SZ4149_1_source_current",
            "requirement": "response-doublet Euler source vanishes",
            "formula": "L_AB Z^B=J_A+B_A; require J_A=0 and B_A=0",
            "current_status": "J_Z_AND_B_Z_UNSIGNED",
            "residual_if_failed": "J_Gamma and Q_phi remain active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SZ4149_2_Y5",
            "requirement": "source-normalization/measured-GM channel is doublet-odd or EH-only",
            "formula": "Y5_source_normalization has no exchange-even source current",
            "current_status": "HARD_FAIL_CURRENT",
            "residual_if_failed": "D_Geff_mismatch, measured-GM drift, R11 source-normalization",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SZ4149_3_Y6",
            "requirement": "extra stress/Bianchi channel is topological, invisible, or bounded",
            "formula": "Y6_extra_stress does not generate PPN-visible T_extra",
            "current_status": "RETAINED_DEBT",
            "residual_if_failed": "T_extra and beta/gamma/alpha_i residuals",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SZ4149_4_matter_source",
            "requirement": "ordinary matter does not couple linearly to Z or phi at fixed observed metric",
            "formula": "delta_Z S_matter|_{Z=0}=0 and delta_phi S_matter|_{g_obs}=0",
            "current_status": "MISSING_MATTER_DESCENT_SOURCE_ZERO",
            "residual_if_failed": "WEP/source-charge/scalar-charge rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "SZ4149_5_verdict",
            "requirement": "all double-zero/source-zero clauses close from one parent branch",
            "formula": "parent_signed(R_doublet,M_AB,J_A=0,B_A=0,Y5=0,Y6=0,PPN_lock)",
            "current_status": "FAIL_CURRENT_CLAIM",
            "residual_if_failed": "phi charge and q_loc/source-normalization bound rows remain active",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "bound_id": "GB4149_0_JGamma",
            "symbol": "J_Gamma",
            "formula": "|J_Gamma| <= (2|zeta_phi|/3)(|D_A Gamma_eff| |deltaPhi^A| + |delta_source Gamma_eff| + |delta_domain Gamma_eff| + |delta_boundary Gamma_eff|)",
            "units": "phi-source units",
            "required_inputs": "Gamma first derivatives, local residual amplitudes, source/domain/boundary variations",
            "status": "NONCLAIM_SOURCE_BOUND_FORM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "GB4149_1_response_doublet_tail",
            "symbol": "J_Gamma_doublet_tail",
            "formula": "if Gamma_eff+C=1/2 M_AB Z^A Z^B+O(Z^4), then |J_Gamma| <= (2|zeta_phi|/3)(||MZ|| |deltaZ| + O(|Z|^3|deltaZ|))",
            "units": "phi-source units",
            "required_inputs": "M_AB, Z amplitude, deltaZ/source response, PPN lock",
            "status": "CONDITIONAL_SMALL_TAIL_BOUND",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "GB4149_2_phi_charge",
            "symbol": "Q_phi",
            "formula": "|Q_phi| <= C_Ophi (||J_Gamma||_1+||J_matter||_1+||J_domain||_1+||J_boundary||_1+||J_mixed||_1)",
            "units": "field charge units",
            "required_inputs": "O_phi inverse norm/range, source-channel L1 bounds, boundary flux",
            "status": "PHI_CHARGE_BOUND_FORM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "GB4149_3_local_gr_residual",
            "symbol": "delta_beta_source_plus_q_loc",
            "formula": "local residual <= C_beta_phi Q_phi + C_q ||q_loc|| + C_G D_Geff_mismatch + C_T ||T_extra||",
            "units": "dimensionless PPN/source-normalization envelope",
            "required_inputs": "phi charge, q_loc residual, coupling drift, extra stress and projector constants",
            "status": "LOCAL_GR_BOUND_INTERFACE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DG4149_0_double_zero",
            "decision": "GAMMA_EXTREMUM_DOUBLE_ZERO_LAW_DERIVED",
            "evidence": "Gamma_eff+C=O(Z^2) gives both amplitude zero and first-variation zero",
            "claim_state": "conditional theorem only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4149_1_route",
            "decision": "RESPONSE_DOUBLET_ROUTE_SELECTED_AS_BEST",
            "evidence": "quadratic even Gamma density directly supplies F_1=0 without per-source tuning",
            "claim_state": "best route but unsigned",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4149_2_current",
            "decision": "CURRENT_SOURCE_ZERO_UNSIGNED",
            "evidence": "J_Z/B_Z/Y5/Y6/matter descent/PPN lock remain missing or retained debts",
            "claim_state": "no J_phi=0, no no-scalar-charge, no local-GR claim",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4149_3_next",
            "decision": "NEXT_TARGET_RESPONSE_DOUBLET_Y5Y6_SOURCE_LOCK",
            "evidence": "Y5 source-normalization and Y6 extra-stress are the hard blockers after formal double-zero",
            "claim_state": "derive or bound those source currents",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "status_id": "STATUS4149_0",
            "result": DECISION,
            "summary": "4149 derives the Gamma extremum/double-zero source law. A fixed subtraction C=-Gamma_eff(Phi0) kills only amplitude; J_phi needs first-variation zero. The clean route is a response-doublet even density Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4), which gives Gamma_eff+C=O(Z^2) and J_Gamma=0 at Z=0. Current MTS does not yet sign the needed parent doublets, J_Z=0, B_Z=0, Y5 source-normalization silence, Y6 extra-stress invisibility, matter descent, or PPN lock. Phi-charge/source bounds are retained.",
            "double_zero_law_derived": "True",
            "response_doublet_route_selected": "True",
            "source_zero_live_signed": "False",
            "J_phi_zero_claimed": "False",
            "phi_charge_bounds_filled": "True",
            "local_gr_claimed": "False",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> List[dict]:
    return [
        {
            **common(),
            "next_id": "NEXT4149_0",
            "target_doc": "4150-Y5-R2FR-response-doublet-Y5Y6-source-current-lock-or-Gamma-bound.md",
            "target_script": "scripts/Y5_R2FR_4150_response_doublet_Y5Y6_source_current_lock_or_Gamma_bound.py",
            "objective": "try to close the response-doublet source-current theorem for Y5 source-normalization and Y6 extra-stress: prove J_Z=0/B_Z=0 and PPN lock for those channels, or retain explicit J_Gamma/Q_phi/q_loc/source-normalization bounds",
            "success_gate": "Y5 and Y6 source currents are parent-zero/topological/bounded with no source tuning, or all Gamma/phi/q_loc residual channels remain explicit nonclaim bounds",
            "reason": "4149 makes F_1=0 a clean doublet theorem target; Y5/Y6 are the blockers that decide whether this can promote toward local GR.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4149 - Gamma-eff extremum/source-zero lock or phi-charge bound

## Decision
- Decision: `{DECISION}`.
- Real progress: the exact `Gamma_eff+C` source-zero law is derived.
- Claim ceiling: no `J_phi=0`, no no-scalar-charge theorem, no q_loc zero, no local-GR/Newton/PPN claim.

## Extremum law
Setting

`C=-Gamma_eff(Phi0)`

only gives

`Gamma_eff(Phi0)+C=0`.

It does **not** by itself give source-zero. The phi source contains

`J_phi=(2 zeta_phi/3)delta(Gamma_eff+C)+J_matter+J_domain+J_boundary+J_memory+J_mixed`.

Since `C` is fixed, the Gamma piece vanishes only if

`delta(Gamma_eff+C)=D_A Gamma_eff|_0 delta Phi^A + delta_source Gamma_eff|_0 + delta_domain Gamma_eff|_0 + ... = 0`.

So the required law is a genuine local extremum/double-zero:

`Gamma_eff+C=O(Z^2)`.

## Best route
The cleanest current route is the response-doublet even density:

`Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)`,

with

`Z^A=(R_+^A-R_-^A)/2`.

After `C=-Gamma0`,

`Gamma_eff+C=O(Z^2)`,

so

`D_A Gamma_eff|_{{Z=0}}=0`

and

`J_Gamma=(2 zeta_phi/3)delta(Gamma_eff+C)=O(Z deltaZ)`.

At the exact local branch `Z=0`, this kills the Gamma contribution to `J_phi`.

## Why it is not claimed
The response-doublet route still needs:
- parent-owned doublets for every physical local residual channel;
- positive/owned `M_AB`;
- `J_Z=0` and `B_Z=0`;
- Y5 source-normalization silence;
- Y6 extra-stress invisibility;
- matter descent/no-marker source-zero;
- PPN lock tying `Z` to the actual local residual vector.

Current sources keep Y5 as hard-fail current and Y6 as retained debt, so this is not a live source-zero theorem yet.

## Bound fallback
If the source-zero lock fails:

`|J_Gamma| <= (2|zeta_phi|/3)(|D_A Gamma_eff| |deltaPhi^A| + |delta_source Gamma_eff| + |delta_domain Gamma_eff| + |delta_boundary Gamma_eff|)`.

Then

`|Q_phi| <= C_Ophi (||J_Gamma||_1+||J_matter||_1+||J_domain||_1+||J_boundary||_1+||J_mixed||_1)`.

These feed the coupling drift and beta/source residual rows from 4147-4148.

## Current verdict
| Gate | Result | Meaning |
|---|---|---|
| amplitude zero | DERIVED_BY_SUBTRACTION | not enough for source-zero |
| first variation zero | DERIVED_IF_DOUBLE_ZERO | needs `Gamma_eff+C=O(Z^2)` |
| response-doublet route | BEST_CONDITIONAL_ROUTE | cleanest `F_1=0` mechanism |
| Y5/Y6 source locks | UNSIGNED | source-normalization and extra stress block promotion |
| local GR/Newton | NOT_CLAIMED | phi/q_loc/source residuals retained |

## Outputs
- `{outputs["P8_Y5_R2FR_4149_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4149_GAMMA_EXTREMUM_LAW"]}`
- `{outputs["P8_Y5_R2FR_4149_RESPONSE_DOUBLET_ROUTE"]}`
- `{outputs["P8_Y5_R2FR_4149_SOURCE_ZERO_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4149_PHI_CHARGE_BOUND_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4149_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4149_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4149_NEXT_TARGET"]}`

## Next Target
- `4150-Y5-R2FR-response-doublet-Y5Y6-source-current-lock-or-Gamma-bound.md`
- Try to close the response-doublet source-current theorem for Y5 source-normalization and Y6 extra-stress, or retain explicit `J_Gamma/Q_phi/q_loc/source-normalization` bounds.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4149_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4149_GAMMA_EXTREMUM_LAW"], extremum_rows())
    write_csv(outputs["P8_Y5_R2FR_4149_RESPONSE_DOUBLET_ROUTE"], response_doublet_rows())
    write_csv(outputs["P8_Y5_R2FR_4149_SOURCE_ZERO_AUDIT"], source_zero_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4149_PHI_CHARGE_BOUND_ROWS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4149_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4149_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4149_NEXT_TARGET"], next_rows())
    write_doc(outputs)
    return outputs


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, requirement: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                **common(),
                "check_id": check_id,
                "requirement": requirement,
                "passed": str(bool(passed)),
                "detail": detail,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )

    sources = source_rows()
    add(
        "VAL4149_0_sources",
        "all cited source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']} exists={row['exists']} needle={row['needle_found']}" for row in sources),
    )

    csv_ok = True
    csv_detail: List[str] = []
    for name, path in outputs.items():
        try:
            rows = parse_csv(path)
            csv_detail.append(f"{name}:{len(rows)}")
            csv_ok = csv_ok and bool(rows)
        except Exception as exc:
            csv_ok = False
            csv_detail.append(f"{name}:ERR {exc!r}")
    add("VAL4149_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "Gamma_eff+C=O(Z^2)",
        "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
        "J_Gamma=(2 zeta_phi/3)delta(Gamma_eff+C)=O(Z deltaZ)",
        "Y5 source-normalization silence",
        "4150-Y5-R2FR-response-doublet-Y5Y6-source-current-lock-or-Gamma-bound.md",
    ]
    add("VAL4149_2_doc_tokens", "document records extremum law, response-doublet route, blockers and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    law_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4149_GAMMA_EXTREMUM_LAW"]))
    law_tokens = ["AMPLITUDE_ZERO_ONLY", "FIRST_VARIATION_ZERO_REQUIRED", "SOURCE_ZERO_LOCK_CONDITIONS_DERIVED", "DOUBLE_ZERO_LAW_DERIVED"]
    add("VAL4149_3_extremum_law", "extremum law distinguishes amplitude subtraction from first-variation source-zero", all(token in law_text for token in law_tokens), "law tokens checked")

    route_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4149_RESPONSE_DOUBLET_ROUTE"]))
    route_tokens = ["Gamma_eff=Gamma0+1/2 M_AB", "J_GAMMA_ZERO_CONDITIONAL", "CURRENT_SOURCE_ZERO_UNSIGNED", "RETAINED_AS_BACKUPS"]
    add("VAL4149_4_response_route", "response-doublet route is selected but retained as nonclaim", all(token in route_text for token in route_tokens), "route tokens checked")

    audit_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4149_SOURCE_ZERO_AUDIT"]))
    audit_tokens = ["NOT_DERIVED_FOR_ALL_CHANNELS", "J_Z_AND_B_Z_UNSIGNED", "HARD_FAIL_CURRENT", "RETAINED_DEBT", "FAIL_CURRENT_CLAIM"]
    add("VAL4149_5_source_audit", "source-zero audit records doublet, source-current, Y5, Y6 and verdict blockers", all(token in audit_text for token in audit_tokens), "audit tokens checked")

    bound_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4149_PHI_CHARGE_BOUND_ROWS"]))
    bound_tokens = ["J_Gamma", "J_Gamma_doublet_tail", "Q_phi", "delta_beta_source_plus_q_loc"]
    add("VAL4149_6_bounds", "bound rows cover Gamma source, doublet tail, phi charge and local-GR residual interface", all(token in bound_text for token in bound_tokens), "bound tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4149_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("double_zero_law_derived") == "True"
        and status[0].get("response_doublet_route_selected") == "True"
        and status[0].get("source_zero_live_signed") == "False"
        and status[0].get("J_phi_zero_claimed") == "False"
        and status[0].get("phi_charge_bounds_filled") == "True"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4149_7_status", "status records double-zero law, best route, unsigned source zero and no claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4149_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4150-Y5-R2FR-response-doublet-Y5Y6-source-current-lock-or-Gamma-bound.md"
    add("VAL4149_8_next", "next target attacks response-doublet Y5/Y6 source-current locks", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4149_9_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4149-Y5-R2FR" in item.name or "R2FR_4149" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4149_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4149_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4149_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
