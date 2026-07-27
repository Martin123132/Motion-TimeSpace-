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
DOC_PATH = ROOT / "4147-Y5-R2FR-Jordan-frame-Geff-calibration-or-second-order-source-closure.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_JORDAN_GEFF_CALIBRATION_OR_SECOND_ORDER_SOURCE_4147"
CHECKPOINT_ID = "4147"
DECISION = "GEFF_CALIBRATION_CONDITIONS_DERIVED_LOCAL_CONSTANT_F_REQUIRED_SECOND_ORDER_SOURCE_BOUNDS_EMITTED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4147_00_4146_doc": (
        ROOT / "4146-Y5-R2FR-finite-source-support-theorem-or-matter-routing-coupling-gate.md",
        "M_eff(phi)^2=M0^2+2 c_I phi",
        "4146 constructed the Jordan-frame matter-routing route.",
    ),
    "SRC4147_01_4146_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4146_NEXT_TARGET.csv",
        "constant-universal G_eff calibration",
        "Machine-readable 4146 handoff to 4147.",
    ),
    "SRC4147_02_4146_matter_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4146_MATTER_ROUTING_CONTRACT.csv",
        "G_ref=1/(8 pi M_eff(phi_*)^2)",
        "4146 source-normalization clause.",
    ),
    "SRC4147_03_source_norm_stack": (
        SOURCE_DIR / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "S1_constant_kappa",
        "Existing constant-coupling source-normalization stack.",
    ),
    "SRC4147_04_newton_stack": (
        SOURCE_DIR / "P8_source_normalized_Newton_branch_STACK.csv",
        "SN11_second_order_PPN_source_stability",
        "Existing Newton/local-GR stack with beta-order source stability.",
    ),
    "SRC4147_05_source_owner_contract": (
        SOURCE_DIR / "P8_source_owner_parent_action_terms_CONTRACT.csv",
        "A10_second_order_source_closure",
        "Parent source-owner action term needed for beta closure.",
    ),
    "SRC4147_06_gk_metric_response": (
        SOURCE_DIR / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "K_hat is exactly",
        "Live Khat adoption must match the variational metric response.",
    ),
    "SRC4147_07_4144_minimal_clause": (
        SOURCE_DIR / "P8_Y5_R2FR_4144_MINIMAL_PARENT_CLAUSE.csv",
        "sigma_resp^{-1} phi R",
        "Minimal trace-free parent clause feeding the Jordan route.",
    ),
    "SRC4147_08_4142_doc": (
        ROOT / "4142-Y5-R2FR-scalar-hair-U2-orthogonality-or-beta-overlap-bound.md",
        "Generic scalar-hair orthogonality is rejected",
        "Scalar hair is not automatically safe for beta.",
    ),
    "SRC4147_09_script": (
        SCRIPT_PATH,
        "GEFF_CALIBRATION_CONDITIONS_DERIVED_LOCAL_CONSTANT_F_REQUIRED",
        "This generator records the 4147 calibration theorem split.",
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
        "P8_Y5_R2FR_4147_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4147_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4147_GEFF_CALIBRATION_THEOREM": SOURCE_DIR / "P8_Y5_R2FR_4147_GEFF_CALIBRATION_THEOREM.csv",
        "P8_Y5_R2FR_4147_CONSTANT_F_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4147_CONSTANT_F_AUDIT.csv",
        "P8_Y5_R2FR_4147_SECOND_ORDER_SOURCE_CLOSURE": SOURCE_DIR / "P8_Y5_R2FR_4147_SECOND_ORDER_SOURCE_CLOSURE.csv",
        "P8_Y5_R2FR_4147_COUPLING_BOUND_ROWS": SOURCE_DIR / "P8_Y5_R2FR_4147_COUPLING_BOUND_ROWS.csv",
        "P8_Y5_R2FR_4147_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4147_DECISION_GATES.csv",
        "P8_Y5_R2FR_4147_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4147_STATUS.csv",
        "P8_Y5_R2FR_4147_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4147_NEXT_TARGET.csv",
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


def geff_theorem_rows() -> List[dict]:
    return [
        {
            **common(),
            "theorem_id": "GT4147_0_jordan_action",
            "statement": "Jordan-frame parent coupling",
            "formula": "S_grav=(1/2)int sqrt|g| F(phi) R, F(phi)=M_eff(phi)^2=M0^2+2 c_I phi",
            "derivation": "Metric variation gives F G_mn = T_mn + nabla_m nabla_n F - g_mn Box F + T_phi_mn after moving non-EH terms to the RHS.",
            "status": "FIELD_EQUATION_DERIVED",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "GT4147_1_constant_F_calibration",
            "statement": "one measured Newton coupling if F is locally constant",
            "formula": "if F=F_*+O(v^6), nabla F=O(v^6), T_phi=O(v^6), then G_mn=F_*^{-1}T_mn+O(v^6) and G_ref=1/(8 pi F_*)",
            "derivation": "The nonminimal coupling becomes the EH coefficient through PPN beta order; the Newtonian Poisson coefficient is fixed once.",
            "status": "CONDITIONAL_THEOREM",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "GT4147_2_drift_law",
            "statement": "if F varies, coupling drift is unavoidable",
            "formula": "delta G_ref/G_ref = - delta F/F_* + O((delta F/F_*)^2); partial_a ln G_ref = - partial_a ln F",
            "derivation": "The measured coupling is the inverse Planck-mass coefficient; variation cannot be hidden without entering Gdot/radial/source/range rows.",
            "status": "RESIDUAL_LAW_DERIVED",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "theorem_id": "GT4147_3_tracefree_routing",
            "statement": "finite-source phi G_TF is routed only if F is adopted live",
            "formula": "2 phi G_TF is part of F(phi)G_TF only after the live field equation is split with F on the LHS",
            "derivation": "The same term is a residual source if Khat_current/F adoption is absent or if F is calibrated after readout.",
            "status": "LIVE_ADOPTION_REQUIRED",
            "current_corpus_claim": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def constant_f_audit_rows() -> List[dict]:
    return [
        {
            **common(),
            "audit_id": "CF4147_0_same_frame",
            "condition": "matter, clocks, rods and EH/source variation use one observed metric/coframe",
            "formula": "g_obs=g_matter=g_source",
            "why_needed": "otherwise G_ref can be hidden in a frame transformation",
            "current_status": "CONDITIONAL_NOT_LIVE_SIGNED",
            "residual_if_failed": "delta_frame_source; eta_WEP; alpha_clock; preferred-frame PPN rows",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "CF4147_1_local_constant_F",
            "condition": "F(phi) is constant through Newton and beta order",
            "formula": "deltaF/F_*=O(v^6), partial_t,r,A,lambda F=0, nabla_m nabla_n F=O(v^6)",
            "why_needed": "kills Gdot, radial/range/source/species dependence and derivative scalar stress through PPN order",
            "current_status": "MISSING_LOCAL_PHI_FREEZE_OR_NO_SCALAR_CHARGE_CERTIFICATE",
            "residual_if_failed": "D_Geff_mismatch; D_deltaF_gradient; delta_beta_source",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "CF4147_2_phi_owner_stress",
            "condition": "phi owner stress is zero or higher order in the local branch",
            "formula": "T_phi_mn=O(v^6) and scalar charge Q_phi=0, or bounded below beta/R10 gates",
            "why_needed": "constant F is not enough if the owner action adds independent stress",
            "current_status": "OWNER_TEMPLATE_STAGED_NOT_ADOPTED",
            "residual_if_failed": "D_owner; scalar_charge; gamma_minus_1; beta_minus_1",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "CF4147_3_live_khat_adoption",
            "condition": "Khat_current^TF is the metric response of the same F(phi)R parent term",
            "formula": "Khat_current^TF=Pi_TF[-2/sqrt|g| delta S_grav/delta g]^TF under one sign convention",
            "why_needed": "prevents using Jordan routing for source coupling while using a different Khat for q_loc",
            "current_status": "UNSIGNED",
            "residual_if_failed": "D_adoption",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "audit_id": "CF4147_4_no_retuning",
            "condition": "F_* and G_ref are parent-selected once, not fitted per source, range, or arena",
            "formula": "partial_source F_*=partial_lambda F_*=partial_dataset F_*=0",
            "why_needed": "keeps Newton's constant as a true constant rather than a calibration patch",
            "current_status": "RULE_DERIVED_NOT_PARENT_SIGNED",
            "residual_if_failed": "source-charge; alpha(lambda); Gdot; calibration offset",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def second_order_rows() -> List[dict]:
    return [
        {
            **common(),
            "closure_id": "SO4147_0_gr_limit",
            "statement": "second-order source closure if F is constant",
            "formula": "F=F_*, T_phi=0, same-frame matter -> g_00=-1+2U-2U^2+O(v^6), gamma=1, beta=1",
            "derivation": "The weak-field equations are exactly the EH/GR equations with coefficient F_* through beta order.",
            "status": "CONDITIONAL_GR_PPN_THEOREM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "closure_id": "SO4147_1_variable_F_source",
            "statement": "variable F creates beta/source residual",
            "formula": "S_beta^F=Pi_00^PPN[(nabla_0 nabla_0 F-g_00 Box F)+T_phi_00+T_phi_ii-deltaF F_*^{-1}T_m]_{U^2}",
            "derivation": "Derivative coupling and coupling mismatch enter the same U^2 projection as q_loc beta.",
            "status": "SOURCE_RESIDUAL_DERIVED",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "closure_id": "SO4147_2_beta_projector",
            "statement": "same-normalized beta projection",
            "formula": "delta_beta_source^F=-1/(2N_U2)<L_00^{-1}S_beta^F,U^2>",
            "derivation": "This connects the Jordan coupling drift directly to the 4139 beta projector normalization.",
            "status": "BOUND_OPERATOR_READY_NONNUMERIC",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "closure_id": "SO4147_3_verdict",
            "statement": "second-order closure cannot be claimed by calibration alone",
            "formula": "beta=1 requires S_beta^F=0 or a valid bound after Newtonian G_ref is fixed",
            "derivation": "A first-order Newton calibration does not automatically remove U^2 source nonlinearities.",
            "status": "NO_LIVE_SECOND_ORDER_CLAIM",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> List[dict]:
    return [
        {
            **common(),
            "bound_id": "CB4147_0_Geff_mismatch",
            "symbol": "D_Geff_mismatch",
            "formula": "|deltaG/G|=|deltaF/F_*|=|2 c_I delta_phi/F_*| + O(delta_phi^2)",
            "units": "dimensionless",
            "required_inputs": "c_I, F_*, delta_phi profile, source/range/frame labels",
            "status": "NONCLAIM_COUPLING_DRIFT_BOUND_ROW",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "CB4147_1_Gdot",
            "symbol": "dlnG_eff_dt",
            "formula": "d ln G_eff/dt = - d ln F/dt",
            "units": "inverse time",
            "required_inputs": "time derivative of local phi_* or theorem zero",
            "status": "RETAIN_GDOT_BOUND_ROW",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "CB4147_2_deltaF_gradient",
            "symbol": "D_deltaF_gradient",
            "formula": "||Pi_TF(nabla nabla F)||/||T_TF|| or beta projector <L_00^{-1}Pi_00[nabla nabla F],U^2>/N_U2",
            "units": "dimensionless after source normalization",
            "required_inputs": "F profile, Hessian profile, T_TF normalization, beta projector",
            "status": "MISSING_GRADIENT_PROFILE_OR_FREEZE_THEOREM",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "CB4147_3_scalar_charge",
            "symbol": "Q_phi",
            "formula": "Q_phi=int_B J_phi d^3x or exterior falloff coefficient of delta_phi",
            "units": "field charge in declared phi units",
            "required_inputs": "phi owner Euler equation, matter source coupling, boundary/falloff condition",
            "status": "MISSING_NO_SCALAR_CHARGE_CERTIFICATE",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "bound_id": "CB4147_4_beta_source",
            "symbol": "delta_beta_source",
            "formula": "|delta_beta_source| <= |C_Geff|D_Geff_mismatch + |C_Fgrad|D_deltaF_gradient + |C_phi| ||T_phi||/N_U2 + |C_adopt|D_adoption",
            "units": "dimensionless beta",
            "required_inputs": "operator constants, F profile, phi stress, adoption residual, N_U2",
            "status": "NONCLAIM_SECOND_ORDER_BOUND_ROW",
            "score_ready": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[dict]:
    return [
        {
            **common(),
            "decision_id": "DG4147_0_theorem",
            "decision": "GEFF_CALIBRATION_CONDITIONS_DERIVED",
            "evidence": "F constant through PPN order reduces Jordan-frame action to EH with G_ref=1/(8 pi F_*)",
            "claim_state": "conditional theorem only",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4147_1_current_corpus",
            "decision": "LOCAL_CONSTANT_F_NOT_LIVE_SIGNED",
            "evidence": "current files do not provide phi freeze/no scalar charge, owner stress silence, or live Khat adoption",
            "claim_state": "no Newton/local-GR promotion",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4147_2_second_order",
            "decision": "SECOND_ORDER_SOURCE_BOUND_ROWS_EMITTED",
            "evidence": "variable F produces S_beta^F and delta_beta_source through the same 4139 projector",
            "claim_state": "not score-ready",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DG4147_3_next",
            "decision": "NEXT_TARGET_LOCAL_PHI_FREEZE_OR_SCALAR_CHARGE_BOUND",
            "evidence": "constant G_eff reduces to proving delta_phi=0/O(v^6) or bounding scalar charge and F-gradient terms",
            "claim_state": "derive freeze/no-charge theorem or keep coupling bounds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def status_rows() -> List[dict]:
    return [
        {
            **common(),
            "status_id": "STATUS4147_0",
            "result": DECISION,
            "summary": "4147 derives the exact coupling condition for the Jordan-frame route. If F(phi)=M_eff(phi)^2 is locally constant through PPN order, with phi-owner stress silent and one observed matter/source frame, the local equations reduce to EH/GR with G_ref=1/(8 pi F_*). The current corpus does not yet own that freeze/no-scalar-charge certificate or live Khat adoption, so no Newton/local-GR claim is made. Variable F produces explicit G_eff drift, F-gradient and delta_beta_source bound rows.",
            "geff_calibration_conditions_derived": "True",
            "local_constant_F_required": "True",
            "local_constant_F_live_signed": "False",
            "second_order_source_closure_claimed": "False",
            "coupling_bound_rows_filled": "True",
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
            "next_id": "NEXT4147_0",
            "target_doc": "4148-Y5-R2FR-local-phi-freeze-no-scalar-charge-or-coupling-drift-bound.md",
            "target_script": "scripts/Y5_R2FR_4148_local_phi_freeze_no_scalar_charge_or_coupling_drift_bound.py",
            "objective": "try to derive delta_phi=0 through Newton/PPN order from the phi owner, mass gap, boundary data, or quotient/superselection rule; if not, emit Q_phi, dlnG_eff, D_deltaF_gradient and delta_beta_source bound rows",
            "success_gate": "local phi freeze/no scalar charge theorem is parent-signed with boundary and source terms, or all coupling-drift/source-residual bounds are explicit and nonclaim",
            "reason": "4147 proves constant F is the exact condition for a one-time G_ref calibration; the next root problem is deriving or bounding delta_phi.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def write_doc(outputs: Dict[str, Path]) -> None:
    text = f"""# 4147 - Jordan-frame `G_eff` calibration or second-order source closure

## Decision
- Decision: `{DECISION}`.
- The useful theorem is now exact: constant local `F(phi)=M_eff(phi)^2` is the condition for a one-time Newton coupling.
- Current corpus status: conditional theorem only; no Newton/local-GR/PPN claim.

## Coupling theorem
Take the Jordan-frame route from 4146:

`S_grav=(1/2)int sqrt|g| F(phi) R`, with `F(phi)=M_eff(phi)^2=M0^2+2 c_I phi`.

Metric variation gives

`F G_mn = T_mn + nabla_m nabla_n F - g_mn Box F + T_phi_mn`.

If

`F=F_*+O(v^6)`, `nabla F=O(v^6)`, and `T_phi_mn=O(v^6)`,

then through Newton and beta order

`G_mn=F_*^-1 T_mn+O(v^6)`,

so the measured local coupling is fixed once:

`G_ref=1/(8 pi F_*)`.

This is the clean answer to the Newton-constant question inside the MTS route: GR also takes `G` as a measured coupling, but here the Jordan parent route says exactly what object must be constant for MTS to inherit the same local coupling without smuggling.

## Drift law
If `F` varies, the variation is observable:

`delta G_ref/G_ref = - delta F/F_* + O((delta F/F_*)^2)`.

Equivalently:

`partial_a ln G_ref = - partial_a ln F`.

So time, radial, source, species, range, or frame dependence cannot be hidden inside measured `GM`; it becomes `Gdot`, source-charge, fifth-force/R10, WEP, or PPN residual debt.

## Second-order source closure
First-order Newton calibration is not enough. Variable `F` feeds beta order through

`S_beta^F=Pi_00^PPN[(nabla_0 nabla_0 F-g_00 Box F)+T_phi_00+T_phi_ii-deltaF F_*^-1 T_m]_[U^2]`.

Using the 4139 projector:

`delta_beta_source^F=-1/(2N_U2)<L_00^-1 S_beta^F,U^2>`.

Therefore `beta=1` follows only if `S_beta^F=0` by theorem, or if the bound row is numerically below the beta gate after Newtonian `G_ref` is fixed.

## Current verdict
| Gate | Result | Meaning |
|---|---|---|
| constant `F` theorem | CONDITIONAL_DERIVED | exact condition identified |
| local phi freeze/no scalar charge | MISSING | no live parent certificate yet |
| phi owner stress silence | UNSIGNED | staged, not adopted |
| live `Khat` adoption | UNSIGNED | still must use same parent response |
| beta source closure | BOUND_ROW_ONLY | no `beta=1` claim |

## Outputs
- `{outputs["P8_Y5_R2FR_4147_SOURCE_REGISTER"]}`
- `{outputs["P8_Y5_R2FR_4147_GEFF_CALIBRATION_THEOREM"]}`
- `{outputs["P8_Y5_R2FR_4147_CONSTANT_F_AUDIT"]}`
- `{outputs["P8_Y5_R2FR_4147_SECOND_ORDER_SOURCE_CLOSURE"]}`
- `{outputs["P8_Y5_R2FR_4147_COUPLING_BOUND_ROWS"]}`
- `{outputs["P8_Y5_R2FR_4147_DECISION_GATES"]}`
- `{outputs["P8_Y5_R2FR_4147_STATUS"]}`
- `{outputs["P8_Y5_R2FR_4147_NEXT_TARGET"]}`

## Next Target
- `4148-Y5-R2FR-local-phi-freeze-no-scalar-charge-or-coupling-drift-bound.md`
- Try to derive `delta_phi=0` through Newton/PPN order from the phi owner, mass gap, boundary data, or quotient/superselection rule; otherwise keep `Q_phi`, `dlnG_eff`, `D_deltaF_gradient`, and `delta_beta_source` as explicit nonclaim bounds.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    write_csv(outputs["P8_Y5_R2FR_4147_SOURCE_REGISTER"], source_rows())
    write_csv(outputs["P8_Y5_R2FR_4147_GEFF_CALIBRATION_THEOREM"], geff_theorem_rows())
    write_csv(outputs["P8_Y5_R2FR_4147_CONSTANT_F_AUDIT"], constant_f_audit_rows())
    write_csv(outputs["P8_Y5_R2FR_4147_SECOND_ORDER_SOURCE_CLOSURE"], second_order_rows())
    write_csv(outputs["P8_Y5_R2FR_4147_COUPLING_BOUND_ROWS"], bound_rows())
    write_csv(outputs["P8_Y5_R2FR_4147_DECISION_GATES"], decision_rows())
    write_csv(outputs["P8_Y5_R2FR_4147_STATUS"], status_rows())
    write_csv(outputs["P8_Y5_R2FR_4147_NEXT_TARGET"], next_rows())
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
        "VAL4147_0_sources",
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
    add("VAL4147_1_csv_parse", "all generated CSV outputs parse and are nonempty", csv_ok, ", ".join(csv_detail))

    doc_text = read_text(DOC_PATH) if DOC_PATH.exists() else ""
    doc_tokens = [
        DECISION,
        "F(phi)=M_eff(phi)^2=M0^2+2 c_I phi",
        "G_ref=1/(8 pi F_*)",
        "delta G_ref/G_ref = - delta F/F_*",
        "delta_beta_source^F=-1/(2N_U2)<L_00^-1 S_beta^F,U^2>",
        "4148-Y5-R2FR-local-phi-freeze-no-scalar-charge-or-coupling-drift-bound.md",
    ]
    add("VAL4147_2_doc_tokens", "document records calibration theorem, drift law, beta projector and next target", all(token in doc_text for token in doc_tokens), "tokens checked")

    theorem_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4147_GEFF_CALIBRATION_THEOREM"]))
    theorem_tokens = ["FIELD_EQUATION_DERIVED", "G_ref=1/(8 pi F_*)", "partial_a ln G_ref = - partial_a ln F", "LIVE_ADOPTION_REQUIRED"]
    add("VAL4147_3_theorem", "Geff theorem rows derive field equation, constant-F calibration and drift law", all(token in theorem_text for token in theorem_tokens), "theorem tokens checked")

    audit_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4147_CONSTANT_F_AUDIT"]))
    audit_tokens = ["MISSING_LOCAL_PHI_FREEZE_OR_NO_SCALAR_CHARGE_CERTIFICATE", "T_phi_mn=O(v^6)", "Khat_current^TF", "partial_source F_*"]
    add("VAL4147_4_audit", "constant-F audit exposes phi freeze, owner stress, adoption and no-retuning gates", all(token in audit_text for token in audit_tokens), "audit tokens checked")

    second_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4147_SECOND_ORDER_SOURCE_CLOSURE"]))
    second_tokens = ["g_00=-1+2U-2U^2+O(v^6)", "S_beta^F", "delta_beta_source^F", "NO_LIVE_SECOND_ORDER_CLAIM"]
    add("VAL4147_5_second_order", "second-order source closure is conditional and boundable through beta projector", all(token in second_text for token in second_tokens), "second-order tokens checked")

    bound_text = "\n".join(",".join(row.values()) for row in parse_csv(outputs["P8_Y5_R2FR_4147_COUPLING_BOUND_ROWS"]))
    bound_tokens = ["D_Geff_mismatch", "dlnG_eff_dt", "D_deltaF_gradient", "Q_phi", "delta_beta_source"]
    add("VAL4147_6_bounds", "coupling bound rows include drift, gradients, scalar charge and beta source", all(token in bound_text for token in bound_tokens), "bound tokens checked")

    status = parse_csv(outputs["P8_Y5_R2FR_4147_STATUS"])
    status_ok = (
        len(status) == 1
        and status[0].get("result") == DECISION
        and status[0].get("geff_calibration_conditions_derived") == "True"
        and status[0].get("local_constant_F_required") == "True"
        and status[0].get("local_constant_F_live_signed") == "False"
        and status[0].get("second_order_source_closure_claimed") == "False"
        and status[0].get("coupling_bound_rows_filled") == "True"
        and status[0].get("local_gr_claimed") == "False"
    )
    add("VAL4147_7_status", "status records exact coupling condition, no live F certificate and no local-GR claim", status_ok, str(status))

    next_target = parse_csv(outputs["P8_Y5_R2FR_4147_NEXT_TARGET"])
    next_ok = len(next_target) == 1 and next_target[0].get("target_doc") == "4148-Y5-R2FR-local-phi-freeze-no-scalar-charge-or-coupling-drift-bound.md"
    add("VAL4147_8_next", "next target attacks local phi freeze/no scalar charge", next_ok, str(next_target))

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    no_score = all(row.get("score_ready", "False") in ("False", "") for row in all_rows)
    add("VAL4147_9_no_claim", "all outputs remain nonclaim and not score-ready", no_claim and no_score, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(
            ("4147-Y5-R2FR" in item.name or "R2FR_4147" in item.name)
            for item in FORMALIZATION.rglob("*")
        )
    add("VAL4147_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4147_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4147_VALIDATION.csv"
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
