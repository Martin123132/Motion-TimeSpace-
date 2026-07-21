from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4543"
CLAIM_ID = "L-385"
BRANCH_ID = "MTS_R2FR_Y5_CGAMMA_GDOT_PRODUCT_TO_PROFILE_COEFFICIENT_4543"
MARKER = "PPC4161_CGAMMA_GDOT_PRODUCT_BOUND_TO_PROFILE_COEFFICIENT_OR_PARENT_MEMORY_OPERATOR_4543"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_GDOT_PRODUCT_BOUND_TO_PROFILE_COEFFICIENT_OR_PARENT_MEMORY_OPERATOR_4543"
DECISION = "EXACT_GDOT_PRODUCT_TO_PROFILE_THEOREM_DERIVED_NO_COEFFICIENT_CLAIM_PROFILE_ZERO_OR_LOWER_BOUND_REQUIRED"
NEXT_TARGET = "4544-Y5-R2FR-DtXi0-local-stationarity-zero-and-tensor-perp-silence-or-profile-source-row.md"

FORMAL_PATH = FORMAL / "559-PPC4161-cGamma-Gdot-product-bound-to-profile-coefficient-or-parent-memory-operator.md"
DOC_PATH = POST / "4543-Y5-R2FR-cGamma-Gdot-product-bound-to-profile-coefficient-or-parent-memory-operator.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4543_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_PRODUCT_TO_COEFFICIENT_THEOREM.csv"
INPUT_LEDGER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_GDOT_CONVERSION_INPUT_LEDGER.csv"
PARENT_OPERATOR_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_PARENT_MEMORY_OPERATOR_AUDIT.csv"
COEFFICIENT_STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_COEFFICIENT_BOUND_STATUS.csv"
PROFILE_ACTIONS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_PROFILE_ACTION_DECISION.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_DECISION.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_NEXT_TARGET.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4543_STATUS.csv"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4543_VALIDATION.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "True" if value else "False"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, Any]]:
    specs = [
        {
            "source_id": "SRC4543_00_4542_status",
            "label": "4542 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4542_STATUS.csv",
            "needle": "PARENT_MEMORY_EQUATION_NOT_FOUND_FIRST_CGAMMA_GDOT_PRODUCT_BOUND_PROMOTED_NONCLAIM",
            "role": "imports the first source-backed C_Gamma_Gdot product bound",
        },
        {
            "source_id": "SRC4543_01_4542_bound",
            "label": "4542 first selected bound",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4542_FIRST_SELECTED_BOUND_ROW.csv",
            "needle": "2.42e-14",
            "role": "sets B_Gdot = 2.42e-14 yr^-1",
        },
        {
            "source_id": "SRC4543_02_4542_requirements",
            "label": "4542 conversion requirements",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4542_PRODUCT_TO_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "J_Gdot^Gamma",
            "role": "states the missing conversion inputs",
        },
        {
            "source_id": "SRC4543_03_4189_coefficient_fill",
            "label": "4189 first coefficient fill",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4189_FIRST_COEFFICIENT_FILL.csv",
            "needle": "c_Gamma D_t Xi_0",
            "role": "gives the symbolic Gdot channel profile formula",
        },
        {
            "source_id": "SRC4543_04_4189_status",
            "label": "4189 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4189_STATUS.csv",
            "needle": "CGamma_Gdot_formula_filled",
            "role": "confirms formula filled but no numeric parent value",
        },
        {
            "source_id": "SRC4543_05_4190_profile_bounds",
            "label": "4190 D_t Xi profile bounds",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4190_DTXI_GRADXI_PROFILE_BOUNDS.csv",
            "needle": "SYMBOLIC4190_DTXI",
            "role": "stores the conditional profile allowance |D_t Xi_0| <= B/|c_Gamma|",
        },
        {
            "source_id": "SRC4543_06_4190_status",
            "label": "4190 status",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4190_STATUS.csv",
            "needle": "numeric_profile_value_available",
            "role": "records finite profile bounds but no numeric profile value",
        },
        {
            "source_id": "SRC4543_07_4193_budget",
            "label": "4193 finite profile budget",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4193_FINITE_PROFILE_BUDGET.csv",
            "needle": "BUD4193_SYMBOLIC_DTXI",
            "role": "links D_t Xi residual budget to source/support/boundary terms",
        },
        {
            "source_id": "SRC4543_08_4193_Jres",
            "label": "4193 residual-source decomposition",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4193_JRES_DECOMPOSITION.csv",
            "needle": "boundary_in",
            "role": "identifies tensor/boundary residual terms feeding the profile",
        },
        {
            "source_id": "SRC4543_09_4193_zero_contract",
            "label": "4193 projector zero contract",
            "path": SOURCE_DIR / "P8_Y5_R2FR_4193_PROJECTOR_ZERO_CONTRACT.csv",
            "needle": "P_loc J_res = 0",
            "role": "records the zero route needed for local profile silence",
        },
    ]
    rows: list[dict[str, Any]] = []
    for spec in specs:
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle = str(spec["needle"])
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": spec["source_id"],
                "label": spec["label"],
                "path": str(path),
                "exists": b(exists),
                "needle": needle,
                "needle_found": b(exists and needle in text),
                "role": spec["role"],
                "valid_for_claim": "False",
            }
        )
    return rows


def load_gdot_bound() -> dict[str, str]:
    rows = read_csv(SOURCE_DIR / "P8_Y5_R2FR_4542_FIRST_SELECTED_BOUND_ROW.csv")
    gdot = next(row for row in rows if row["effective_product"] == "C_Gamma_Gdot")
    return gdot


def theorem_rows() -> list[dict[str, Any]]:
    gdot = load_gdot_bound()
    bound = gdot["max_abs_effective_product"]
    units = gdot["units"]
    return [
        {
            "theorem_id": "THM4543_0_channel_identity",
            "statement": "C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot",
            "derivation": "4189 filled the Gdot channel as c_Gamma D_t Xi_0; 4543 restores the possible tensor/perpendicular leakage term left open by 4541-4542.",
            "condition": "linearized local branch and no cross-channel cancellation",
            "consequence": "the measured Gdot drift bounds the whole channel product, not c_Gamma alone",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM4543_1_product_bound",
            "statement": f"|C_Gamma_Gdot| <= B_Gdot = {bound} {units}",
            "derivation": "direct import of the 4542 first selected source-backed product row",
            "condition": "use as a first-order local Newton/source-coupling guard",
            "consequence": "any future parent profile must satisfy |c_Gamma D_t Xi_0 + T_perp,Gdot| <= B_Gdot",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM4543_2_exact_silence_route",
            "statement": "If D_t Xi_0 = 0 and T_perp,Gdot = 0, then C_Gamma_Gdot = 0.",
            "derivation": "substitution into the channel identity",
            "condition": "parent-signed local stationarity plus tensor/perpendicular silence",
            "consequence": "Gdot passes without needing a numerical c_Gamma value, but this does not bound c_Gamma itself",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM4543_3_coefficient_bound_route",
            "statement": "If |D_t Xi_0| >= X_min > 0 and |T_perp,Gdot| <= T_max, then |c_Gamma| <= (B_Gdot + T_max)/X_min.",
            "derivation": "|c_Gamma D_t Xi_0| = |C_Gamma_Gdot - T_perp,Gdot| <= |C_Gamma_Gdot| + |T_perp,Gdot|",
            "condition": "requires a nonzero lower bound on the physical Gdot profile and an independent tensor-perp bound",
            "consequence": "this is the first honest c_Gamma coefficient-bound formula, but X_min and T_max are not yet supplied",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM4543_4_upper_bound_warning",
            "statement": "An upper bound |D_t Xi_0| <= X_max does not by itself upper-bound |c_Gamma| from |c_Gamma D_t Xi_0| <= B_Gdot.",
            "derivation": "the profile can approach zero, making arbitrarily large c_Gamma compatible with a small product unless a lower profile floor or zero theorem is supplied",
            "condition": "pure product-bound algebra",
            "consequence": "the next derivation should seek D_t Xi_0 = 0 for local silence, or source a nonzero profile lower bound before claiming a coefficient constraint",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM4543_5_assumed_cGamma_profile_allowance",
            "statement": f"For any assumed |c_Gamma| > 0 with T_perp,Gdot = 0, |D_t Xi_0| <= {bound}/|c_Gamma| {units}.",
            "derivation": "divide the product bound by an assumed nonzero coefficient; this is a profile allowance, not a coefficient measurement",
            "condition": "assumed c_Gamma magnitude and no tensor-perp contribution",
            "consequence": "4190 and 4193 budget rows remain useful as profile-suppression tests",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def input_ledger_rows() -> list[dict[str, Any]]:
    gdot = load_gdot_bound()
    return [
        {
            "input_id": "IN4543_0_B_Gdot",
            "quantity": "B_Gdot",
            "value": gdot["max_abs_effective_product"],
            "units": gdot["units"],
            "status": "source_backed_product_bound_available",
            "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4542_FIRST_SELECTED_BOUND_ROW.csv"),
            "needed_for_cGamma_bound": "yes",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4543_1_J_Gdot_Gamma",
            "quantity": "J_Gdot^Gamma",
            "value": "absorbed_into_D_t_Xi_0_in_4189_smoke_formula",
            "units": "unit-normalized bookkeeping; physical parent Jacobian not separately sourced",
            "status": "symbolic_only",
            "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4189_FIRST_COEFFICIENT_FILL.csv"),
            "needed_for_cGamma_bound": "yes_if_not_absorbed",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4543_2_DtXi0_value",
            "quantity": "D_t Xi_0",
            "value": "no numeric value or lower bound",
            "units": "yr^-1",
            "status": "profile_allowances_exist_but_no_value",
            "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4190_DTXI_GRADXI_PROFILE_BOUNDS.csv"),
            "needed_for_cGamma_bound": "yes",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4543_3_DtXi0_lower_floor",
            "quantity": "X_min <= |D_t Xi_0|",
            "value": "missing",
            "units": "yr^-1",
            "status": "required_only_for_coefficient_bound_route",
            "source_path": "",
            "needed_for_cGamma_bound": "yes",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4543_4_tensor_perp_bound",
            "quantity": "T_perp,Gdot",
            "value": "missing or zero if tensor/perpendicular silence theorem closes",
            "units": "yr^-1",
            "status": "open",
            "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4193_JRES_DECOMPOSITION.csv"),
            "needed_for_cGamma_bound": "yes",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4543_5_zero_route",
            "quantity": "D_t Xi_0 = 0 and T_perp,Gdot = 0",
            "value": "not parent-signed",
            "units": "n/a",
            "status": "best_derivation_route_for_local_GR_silence",
            "source_path": str(SOURCE_DIR / "P8_Y5_R2FR_4193_PROJECTOR_ZERO_CONTRACT.csv"),
            "needed_for_cGamma_bound": "no_but_needed_for_local_silence",
            "valid_for_claim": "False",
        },
    ]


def parent_operator_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "POA4543_0_operator",
            "clause": "find parent equation L_Gamma Gamma_mem = J_Gamma",
            "status": "not_found_in_4542_or_4189",
            "effect_if_closed": "compute D_t Xi_0, prove D_t Xi_0=0, or source a profile floor",
            "current_action": "do not invent operator; use channel theorem and profile-zero target",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "POA4543_1_stationarity",
            "clause": "derive local stationarity D_t Xi_0=0",
            "status": "contract_exists_but_parent_signature_open",
            "effect_if_closed": "Gdot cGamma channel becomes silent if tensor-perp also vanishes",
            "current_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "POA4543_2_tensor_perp",
            "clause": "prove or bound T_perp,Gdot",
            "status": "open",
            "effect_if_closed": "prevents hidden leakage/cancellation in local Newton drift",
            "current_action": "bind tensor-perp to 4193 residual-source decomposition",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "CBS4543_0_product",
            "object": "C_Gamma_Gdot",
            "status": "bounded",
            "result": "|C_Gamma_Gdot| <= 2.42e-14 yr^-1",
            "why": "source-backed 4542 product row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "status_id": "CBS4543_1_coefficient",
            "object": "c_Gamma",
            "status": "not_bounded",
            "result": "no coefficient value or upper bound follows yet",
            "why": "need nonzero |D_t Xi_0| floor or parent profile calculation plus T_perp bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "status_id": "CBS4543_2_local_silence",
            "object": "Gdot residual",
            "status": "conditional_zero_route_identified",
            "result": "D_t Xi_0=0 and T_perp,Gdot=0 imply C_Gamma_Gdot=0",
            "why": "direct substitution into the derived channel identity",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "status_id": "CBS4543_3_profile_budget",
            "object": "D_t Xi_0",
            "status": "profile_allowance_available",
            "result": "|D_t Xi_0| <= 2.42e-14/|c_Gamma| yr^-1 for assumed c_Gamma and T_perp=0",
            "why": "useful for source-support-budget tests but not a coefficient bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def profile_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "action_id": "PAD4543_0_best_route",
            "route": "derive local stationarity and tensor-perp silence",
            "reason": "this can make the Gdot channel locally silent without needing to numerically derive c_Gamma",
            "target": NEXT_TARGET,
            "risk": "requires parent-signed zero clauses, not just smoothness language",
            "selected": "True",
            "valid_for_claim": "False",
        },
        {
            "action_id": "PAD4543_1_fallback",
            "route": "source a nonzero D_t Xi_0 profile lower bound and tensor-perp bound",
            "reason": "only then can the product bound be divided into a coefficient bound",
            "target": "future coefficient-bound row",
            "risk": "a lower profile floor may be physically unnatural if the intended local branch is stationary",
            "selected": "False",
            "valid_for_claim": "False",
        },
        {
            "action_id": "PAD4543_2_rejected_shortcut",
            "route": "divide by an upper profile bound",
            "reason": "mathematically invalid for upper-bounding c_Gamma because the profile can go to zero",
            "target": "do_not_use",
            "risk": "would create a false local-GR pass",
            "selected": "False",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim_gate_id": "CG4543_0_product_bound",
            "gate": "Gdot product bound",
            "status": "PASS_NONCLAIM",
            "meaning": "C_Gamma_Gdot has a source-backed product bound",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4543_1_cGamma_coefficient",
            "gate": "c_Gamma coefficient bound",
            "status": "BLOCKED_NO_PROFILE_FLOOR_OR_ZERO_PROOF",
            "meaning": "cannot divide the product bound into c_Gamma without a nonzero profile lower bound or a parent profile calculation",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4543_2_Gdot_silence",
            "gate": "Gdot channel silence",
            "status": "CONDITIONAL_DTXI_AND_TPERP_ZERO",
            "meaning": "if D_t Xi_0 and T_perp,Gdot are parent-zero, the channel vanishes",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "claim_gate_id": "CG4543_3_public_local_GR",
            "gate": "public local GR",
            "status": "BLOCKED_LOCAL_SILENCE_NOT_PARENT_SIGNED",
            "meaning": "local GR still waits for parent-signed profile/tensor silence or coefficient-level residual bounds",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4543_0",
            "decision": DECISION,
            "meaning": "4543 derives the exact Gdot product-to-profile law. The useful leap is that an upper profile allowance is not enough to bound c_Gamma; the honest local-GR route is to prove D_t Xi_0=0 and tensor/perp silence, or else source a nonzero physical profile floor.",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NT4543_0",
            "target": NEXT_TARGET,
            "objective": "try to prove D_t Xi_0=0 and T_perp,Gdot=0 from the local stationarity/projector-zero contract; if that fails, write the first real profile-source row",
            "derive_first": "turn P_loc J_res=0 plus boundary/no-flux routing into D_t Xi_0=0",
            "fallback": "source or bound X_min and T_max so |c_Gamma| <= (B_Gdot + T_max)/X_min becomes numerical",
            "avoid": "using upper profile allowances as c_Gamma bounds",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT,
            "result": DECISION,
            "C_Gamma_Gdot_product_bound_available": "True",
            "C_Gamma_Gdot_max_abs": "2.42e-14",
            "C_Gamma_Gdot_units": "yr^-1",
            "c_Gamma_coefficient_bound_available": "False",
            "profile_zero_route_identified": "True",
            "profile_floor_available": "False",
            "tensor_perp_bound_available": "False",
            "public_local_GR_claim_allowed": "False",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    ledger: list[dict[str, Any]],
    parent_audit: list[dict[str, Any]],
    coefficient_status: list[dict[str, Any]],
    profile_actions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks.append({"validation_id": "VAL4543_00_sources", "status": "PASS" if source_ok else "FAIL", "detail": "all source paths exist and needles found" if source_ok else "source path or needle missing"})

    product_ok = any(row["theorem_id"] == "THM4543_1_product_bound" and "2.42e-14" in row["statement"] for row in theorem)
    checks.append({"validation_id": "VAL4543_01_product_bound", "status": "PASS" if product_ok else "FAIL", "detail": "Gdot product bound imported into theorem"})

    identity_ok = any(row["theorem_id"] == "THM4543_0_channel_identity" and "D_t Xi_0" in row["statement"] and "T_perp" in row["statement"] for row in theorem)
    checks.append({"validation_id": "VAL4543_02_channel_identity", "status": "PASS" if identity_ok else "FAIL", "detail": "channel identity includes profile and tensor-perp terms"})

    lower_bound_ok = any(row["theorem_id"] == "THM4543_3_coefficient_bound_route" and "X_min" in row["statement"] for row in theorem)
    checks.append({"validation_id": "VAL4543_03_coefficient_condition", "status": "PASS" if lower_bound_ok else "FAIL", "detail": "coefficient bound requires a nonzero profile lower floor"})

    warning_ok = any(row["theorem_id"] == "THM4543_4_upper_bound_warning" for row in theorem)
    checks.append({"validation_id": "VAL4543_04_upper_bound_warning", "status": "PASS" if warning_ok else "FAIL", "detail": "upper profile bounds are not misused as c_Gamma bounds"})

    missing_inputs_ok = any(row["input_id"] == "IN4543_3_DtXi0_lower_floor" and row["value"] == "missing" for row in ledger) and any(row["input_id"] == "IN4543_4_tensor_perp_bound" and "missing" in row["value"] for row in ledger)
    checks.append({"validation_id": "VAL4543_05_missing_inputs_honest", "status": "PASS" if missing_inputs_ok else "FAIL", "detail": "missing profile floor and tensor-perp bound remain explicit"})

    operator_ok = any(row["audit_id"] == "POA4543_0_operator" and row["status"] == "not_found_in_4542_or_4189" for row in parent_audit)
    checks.append({"validation_id": "VAL4543_06_parent_operator", "status": "PASS" if operator_ok else "FAIL", "detail": "parent memory operator remains absent without fabrication"})

    coefficient_blocked = any(row["status_id"] == "CBS4543_1_coefficient" and row["status"] == "not_bounded" for row in coefficient_status)
    selected_route = any(row["action_id"] == "PAD4543_0_best_route" and row["selected"] == "True" for row in profile_actions)
    checks.append({"validation_id": "VAL4543_07_decision_route", "status": "PASS" if coefficient_blocked and selected_route else "FAIL", "detail": "selected next route is local profile/tensor silence, not false coefficient division"})

    gates_ok = all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in gates)
    checks.append({"validation_id": "VAL4543_08_claim_firewall", "status": "PASS" if gates_ok else "FAIL", "detail": "all claim gates remain private/nonclaim"})

    csv_paths = [
        SOURCE_REGISTER,
        THEOREM_CSV,
        INPUT_LEDGER_CSV,
        PARENT_OPERATOR_AUDIT_CSV,
        COEFFICIENT_STATUS_CSV,
        PROFILE_ACTIONS_CSV,
        CLAIM_GATES_CSV,
        DECISION_CSV,
        NEXT_CSV,
        STATUS_CSV,
    ]
    csv_ok = True
    details: list[str] = []
    for path in csv_paths:
        try:
            if not read_csv(path):
                csv_ok = False
                details.append(f"{path.name}:empty")
        except Exception as exc:
            csv_ok = False
            details.append(f"{path.name}:{exc}")
    checks.append({"validation_id": "VAL4543_09_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSV files parse and have rows" if csv_ok else ";".join(details)})

    pycache_absent = not (SCRIPT_DIR / "__pycache__").exists()
    checks.append({"validation_id": "VAL4543_10_pycache_absent", "status": "PASS" if pycache_absent else "FAIL", "detail": "scripts __pycache__ absent after cleanup" if pycache_absent else "scripts __pycache__ still present"})

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append({"validation_id": "VAL4543_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "4543 exact Gdot product-to-profile/coefficient theorem"})
    return checks


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    ledger: list[dict[str, Any]],
    parent_audit: list[dict[str, Any]],
    coefficient_status: list[dict[str, Any]],
    profile_actions: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4543 - cGamma Gdot product bound to profile/coefficient law or parent memory operator

Generated: `{utc_now()}`  
Marker: `{MARKER}`  
Decision: `{DECISION}`  
Claim: `{CLAIM_ID}` remains private, conditional and nonclaim.

## What Moved

4542 gave the first useful local guard:

```text
|C_Gamma_Gdot| <= 2.42e-14 yr^-1.
```

4543 derives the exact conversion logic instead of pretending this is already a `c_Gamma` bound. The Gdot channel is:

```text
C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot.
```

So there are two honest routes:

```text
D_t Xi_0 = 0 and T_perp,Gdot = 0  ->  C_Gamma_Gdot = 0
```

or

```text
|D_t Xi_0| >= X_min > 0 and |T_perp,Gdot| <= T_max
  -> |c_Gamma| <= (B_Gdot + T_max)/X_min.
```

The key correction is that an **upper** profile allowance, such as `|D_t Xi_0| <= B/|c_Gamma|`, is useful for profile suppression but cannot upper-bound `c_Gamma`. To bound `c_Gamma`, the branch needs a nonzero profile floor or a parent-calculated profile. To pass local GR cleanly, the better derivation route is local stationarity plus tensor/perp silence.

## Product-To-Coefficient Theorem

{markdown_table(theorem)}

## Gdot Conversion Input Ledger

{markdown_table(ledger)}

## Parent Memory Operator Audit

{markdown_table(parent_audit)}

## Coefficient Bound Status

{markdown_table(coefficient_status)}

## Profile Action Decision

{markdown_table(profile_actions)}

## Claim Gates

{markdown_table(gates)}

## Decision

{markdown_table(decisions)}

## Next Target

{markdown_table(next_target)}

## Status

{markdown_table(status)}

## Source Register

{markdown_table(sources)}

## Validation

{markdown_table(validation)}
"""


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write(text.strip() + "\n")


def append_claim_once() -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if f"{CLAIM_ID}," in existing:
        return
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_memory_bound",
        "claim": "4543 derives the exact Gdot product-to-profile/coefficient law: C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot, with a source-backed product bound but no coefficient claim until a profile floor/parent profile or zero theorem is supplied.",
        "current_evidence": "Generated source register, product-to-coefficient theorem, Gdot conversion input ledger, parent operator audit, coefficient status, profile action decision, claim gates, status and validation CSVs.",
        "status": "exact_product_to_profile_theorem_nonclaim_profile_zero_route_selected",
        "next_test": NEXT_TARGET,
        "key_risk": "Mistaking an upper profile allowance for an upper bound on c_Gamma.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Local GR remains unclaimed until D_t Xi_0/tensor-perp silence or a real coefficient-bound input closes.",
    }
    file_exists = CLAIMS_PATH.exists() and CLAIMS_PATH.stat().st_size > 0
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main() -> None:
    sources = source_rows()
    theorem = theorem_rows()
    ledger = input_ledger_rows()
    parent_audit = parent_operator_audit_rows()
    coefficient_status = coefficient_status_rows()
    profile_actions = profile_action_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()
    status = status_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(THEOREM_CSV, theorem)
    write_csv(INPUT_LEDGER_CSV, ledger)
    write_csv(PARENT_OPERATOR_AUDIT_CSV, parent_audit)
    write_csv(COEFFICIENT_STATUS_CSV, coefficient_status)
    write_csv(PROFILE_ACTIONS_CSV, profile_actions)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(NEXT_CSV, next_target)
    write_csv(STATUS_CSV, status)

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    validation = validate(sources, theorem, ledger, parent_audit, coefficient_status, profile_actions, gates)
    write_csv(VALIDATION_PATH, validation)

    body = build_doc(sources, theorem, ledger, parent_audit, coefficient_status, profile_actions, gates, decisions, next_target, status, validation)
    FORMAL_PATH.write_text(body, encoding="utf-8")
    DOC_PATH.write_text(body, encoding="utf-8")

    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## 4543 cGamma Gdot Product Bound To Profile/Coefficient Law

Marker: `{MARKER}`  
4543 derives the exact conversion law `C_Gamma_Gdot = c_Gamma D_t Xi_0 + T_perp,Gdot`. The source-backed product guard remains `|C_Gamma_Gdot| <= 2.42e-14 yr^-1`, but this is not a coefficient bound. A real `c_Gamma` bound requires a nonzero profile floor `|D_t Xi_0| >= X_min` plus tensor/perp control; the cleaner local-GR route is `D_t Xi_0=0` and `T_perp,Gdot=0`. Next target: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## 4543 Packet Integration - Gdot Product Bound Conversion Law

Marker: `{PACKET_MARKER}`  
The packet now distinguishes three cases: product bound, coefficient bound, and local silence. `C_Gamma_Gdot` is bounded; `c_Gamma` is not. If the branch proves `D_t Xi_0=0` and `T_perp,Gdot=0`, the Gdot channel becomes locally silent without needing to assign a numeric `c_Gamma`.
""",
    )

    shutil.rmtree(SCRIPT_DIR / "__pycache__", ignore_errors=True)
    print(f"wrote {FORMAL_PATH}")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"decision {DECISION}")


if __name__ == "__main__":
    main()
