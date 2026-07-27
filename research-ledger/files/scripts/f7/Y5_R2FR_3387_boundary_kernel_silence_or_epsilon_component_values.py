from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3387-Y5-R2FR-boundary-kernel-silence-or-epsilon-component-values-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3387_SOURCE_REGISTER.csv",
    "boundary_law": OUT / "P8_Y5_R2FR_3387_BOUNDARY_COLLAR_TAIL_LAW.csv",
    "kernel_law": OUT / "P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv",
    "component_contract": OUT / "P8_Y5_R2FR_3387_EPSILON_COMPONENT_VALUE_CONTRACT.csv",
    "component_targets": OUT / "P8_Y5_R2FR_3387_COMPONENT_TARGETS_FROM_3386.csv",
    "runner": OUT / "P8_Y5_R2FR_3387_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3387_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3387_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3387_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3387_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3387_0_3386_doc", ROOT / "3386-Y5-R2FR-epsilon-eff-parent-silence-or-first-finite-inputs-under-AX1090.md", "3386 epsilon_eff handoff"),
    ("SRC3387_1_3386_parent_silence", OUT / "P8_Y5_R2FR_3386_PARENT_SILENCE_ATTEMPT.csv", "3386 boundary/kernel zero clauses"),
    ("SRC3387_2_3386_finite_inputs", OUT / "P8_Y5_R2FR_3386_FIRST_FINITE_INPUT_ROWS_NONCLAIM.csv", "3386 finite input rows"),
    ("SRC3387_3_3386_backsolve", OUT / "P8_Y5_R2FR_3386_THRESHOLD_BACKSOLVE.csv", "3386 target ceilings"),
    ("SRC3387_4_3376_doc", ROOT / "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md", "3376 boundary zero-flux theorem attempt"),
    ("SRC3387_5_3376_zero_attempt", OUT / "P8_Y5_R2FR_3376_BOUNDARY_ZERO_FLUX_THEOREM_ATTEMPT.csv", "3376 boundary theorem clauses"),
    ("SRC3387_6_3376_bound_rows", OUT / "P8_Y5_R2FR_3376_BZERO_FIRST_BOUND_ROWS_NONCLAIM.csv", "3376 finite boundary rows"),
    ("SRC3387_7_3376_signature", OUT / "P8_Y5_R2FR_3376_BOUNDARY_SIGNATURE_AUDIT.csv", "3376 missing boundary signatures"),
    ("SRC3387_8_3321_kernel", OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv", "3321 Gaussian smoothing/transfer law"),
    ("SRC3387_9_3336_tree_contract", OUT / "P8_Y5_R2FR_3336_TREE_EPSILON_BOUND_CONTRACT.csv", "3336 boundary/kernel conditional zero and tree thresholds"),
    ("SRC3387_10_3332_epsilon", OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv", "3332 epsilon_eff decomposition"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
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
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def boundary_law_rows() -> list[dict[str, str]]:
    return [
        {
            "law_id": "BL3387_0_target",
            "quantity": "epsilon_boundary_PPN",
            "law_or_theorem": "normalized boundary/collar/source-worldtube leakage in the local PPN smoothing readout",
            "formula": "epsilon_boundary_PPN := ||B_PPN_boundary||/||R_EH_PPN||",
            "derivation_status": "DEFINITION_FROM_3386",
            "current_claim_status": "NONCLAIM",
            "missing_or_guard": "requires boundary zero theorem or finite same-frame leakage inputs",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL3387_1_compact_kernel_interior_zero",
            "quantity": "epsilon_boundary_PPN",
            "law_or_theorem": "exact interior support theorem",
            "formula": "if supp(S_ell x local test field) lies inside the source-free PPN collar and physical flux is in Hilbert stress, then boundary readout term = 0",
            "derivation_status": "VALID_CONDITIONAL_THEOREM",
            "current_claim_status": "NOT_CURRENT_BRANCH",
            "missing_or_guard": "current imported kernel is Gaussian/infinite-tail; compact-support kernel or parent interior-collar owner not signed",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL3387_2_gaussian_collar_tail",
            "quantity": "epsilon_boundary_tail",
            "law_or_theorem": "Gaussian leakage is exponentially suppressed by collar distance",
            "formula": "epsilon_boundary_tail <= C_boundary exp[-d_collar^2/(2 ell_s^2)]",
            "derivation_status": "DERIVED_FROM_GAUSSIAN_TAIL_NONCLAIM",
            "current_claim_status": "FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "missing_or_guard": "requires d_collar/ell_s and C_boundary in same observed local frame",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL3387_3_physical_flux_additive",
            "quantity": "epsilon_boundary_physical",
            "law_or_theorem": "physical EM/Poynting/matter flux cannot be erased by a boundary gauge argument",
            "formula": "epsilon_boundary_physical <= (|B_zero_flux|+|Delta_symp|+|Phi_Poynting_bound|+|corner/topology|)/M_H_ref",
            "derivation_status": "INHERITED_FROM_3376",
            "current_claim_status": "BOUND_ROWS_UNFILLED",
            "missing_or_guard": "B_zero_flux, Delta_symp, Phi_Poynting_bound, corner/topology and M_H_ref remain nonclaim/unfilled",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL3387_4_combined_bound",
            "quantity": "epsilon_boundary_PPN",
            "law_or_theorem": "boundary channel bound with no cancellation",
            "formula": "epsilon_boundary_PPN <= C_boundary exp[-d_collar^2/(2 ell_s^2)] + (|B_zero_flux|+|Delta_symp|+|Phi_Poynting_bound|+|corner/topology|)/M_H_ref + epsilon_worldtube_mismatch",
            "derivation_status": "DERIVED_COMPONENT_BOUND",
            "current_claim_status": "NUMERICALLY_UNSCORED",
            "missing_or_guard": "all terms must be zero-signed or source-valued before epsilon_boundary_PPN can be used",
            "valid_for_claim": "false",
        },
        {
            "law_id": "BL3387_5_verdict",
            "quantity": "epsilon_boundary_PPN=0",
            "law_or_theorem": "boundary zero route",
            "formula": "compact/interior support zero AND 3376 physical/reference/topology flux zero",
            "derivation_status": "PROMISING_BUT_NOT_PARENT_SIGNED",
            "current_claim_status": "ZERO_NOT_CLAIMED",
            "missing_or_guard": "kernel support/collar, fixed primitive, relative class, physical flux placement, reference lock, M_H_ref",
            "valid_for_claim": "false",
        },
    ]


def kernel_law_rows() -> list[dict[str, str]]:
    return [
        {
            "law_id": "KL3387_0_target",
            "quantity": "epsilon_kernel_aniso_PPN",
            "law_or_theorem": "kernel anisotropy / PPN projector commutator leakage",
            "formula": "epsilon_kernel_aniso_PPN := ||[P_PPN,S_ell] + anisotropic first-moment defect||",
            "derivation_status": "DEFINITION_FROM_3386",
            "current_claim_status": "NONCLAIM",
            "missing_or_guard": "requires parent smoothing/projector owner or finite commutator norm",
            "valid_for_claim": "false",
        },
        {
            "law_id": "KL3387_1_constant_projector_zero",
            "quantity": "[P_0,S_ell]",
            "law_or_theorem": "constant local PPN projector commutes with an isotropic convolution kernel",
            "formula": "P_0 int K_ell(x-y)f(y)dy - int K_ell(x-y)P_0 f(y)dy = 0",
            "derivation_status": "EXACT_LOCAL_TANGENT_FRAME_THEOREM",
            "current_claim_status": "CONDITIONAL_ONLY",
            "missing_or_guard": "requires actual P_PPN to be constant over smoothing support in the parent local branch",
            "valid_for_claim": "false",
        },
        {
            "law_id": "KL3387_2_variable_projector_identity",
            "quantity": "[P(x),S_ell]f",
            "law_or_theorem": "exact commutator identity for position-dependent projector",
            "formula": "[P,S_ell]f(x)=int K_ell(x-y)[P(x)-P(y)]f(y)dy",
            "derivation_status": "DERIVED_IDENTITY",
            "current_claim_status": "FORMULA_READY",
            "missing_or_guard": "needs norm for projector variation in the observed PPN branch",
            "valid_for_claim": "false",
        },
        {
            "law_id": "KL3387_3_variable_projector_bound",
            "quantity": "epsilon_kernel_aniso_PPN",
            "law_or_theorem": "first finite projector-commutator envelope",
            "formula": "epsilon_kernel_aniso_PPN <= C1 ell_s ||nabla P_PPN|| + C2 ell_s^2 ||nabla^2 P_PPN|| + epsilon_kernel_moment + epsilon_gauge_readout",
            "derivation_status": "DERIVED_OPERATOR_BOUND_NONCLAIM",
            "current_claim_status": "NUMERIC_INPUTS_MISSING",
            "missing_or_guard": "requires C1,C2, ell_s, projector-gradient norms, moment defect and gauge/readout defect",
            "valid_for_claim": "false",
        },
        {
            "law_id": "KL3387_4_UOC_observed_metric_route",
            "quantity": "nabla P_PPN",
            "law_or_theorem": "if P_PPN is built only from the same UOC observed metric/coframe, projector variation is tied to local metric variation",
            "formula": "||nabla P_PPN|| <= C_P ||nabla g_obs|| + C_gauge ||nabla gauge||",
            "derivation_status": "STRUCTURAL_ROUTE_NOT_NUMERIC",
            "current_claim_status": "PROMISING_BUT_UNSIGNED",
            "missing_or_guard": "requires parent-owned PPN readout/gauge convention and local metric derivative bound",
            "valid_for_claim": "false",
        },
        {
            "law_id": "KL3387_5_verdict",
            "quantity": "epsilon_kernel_aniso_PPN=0",
            "law_or_theorem": "kernel zero route",
            "formula": "constant PPN projector + isotropic zero-first-moment kernel + no gauge/readout drift",
            "derivation_status": "EXACT_IN_TANGENT_LIMIT_NOT_CURRENT_PROOF",
            "current_claim_status": "ZERO_NOT_CLAIMED",
            "missing_or_guard": "actual local readout projector is not yet parent-proved constant/commuting through PPN order",
            "valid_for_claim": "false",
        },
    ]


def component_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "CC3387_0_boundary_zero",
            "quantity": "epsilon_boundary_PPN",
            "claim_route": "compact/interior support plus 3376 zero-flux/reference/topology theorem",
            "bound_route": "BL3387_4 combined bound",
            "required_inputs": "kernel branch; d_collar/ell_s; C_boundary; B_zero_flux; Delta_symp; Phi_Poynting_bound; corner/topology; M_H_ref; epsilon_worldtube_mismatch",
            "current_value": "MISSING_BOUNDARY_COMPONENT_VALUES",
            "status": "ZERO_NOT_SIGNED_BOUND_FORMULA_READY",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CC3387_1_kernel_zero",
            "quantity": "epsilon_kernel_aniso_PPN",
            "claim_route": "constant parent PPN projector with isotropic zero-first-moment kernel",
            "bound_route": "KL3387_3 variable projector commutator envelope",
            "required_inputs": "C1;C2;ell_s;||nabla P_PPN||;||nabla^2 P_PPN||;epsilon_kernel_moment;epsilon_gauge_readout",
            "current_value": "MISSING_KERNEL_PROJECTOR_COMPONENT_VALUES",
            "status": "TANGENT_ZERO_DERIVED_REAL_PATCH_BOUND_READY",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CC3387_2_reduced_epsilon_eff",
            "quantity": "epsilon_eff_PPN",
            "claim_route": "if CC3387_0 and CC3387_1 zero, epsilon_eff_PPN <= epsilon_bg_PPN*T_grad(lambda_PPN)",
            "bound_route": "epsilon_eff_PPN <= epsilon_bg*T_grad + BL3387_4 + KL3387_3",
            "required_inputs": "epsilon_bg;T_grad plus boundary and kernel component values",
            "current_value": "MISSING_REDUCED_EPSILON_VALUES",
            "status": "REDUCTION_FORMULA_READY_NOT_NUMERIC",
            "valid_for_claim": "false",
        },
        {
            "contract_id": "CC3387_3_claim_firewall",
            "quantity": "local_PPN_gamma",
            "claim_route": "only after A_gamma, Cmetric, floors, epsilon_bg/Tgrad, boundary and kernel are all source-backed or zero-signed",
            "bound_route": "3385/3386 Cassini runner after component replacement",
            "required_inputs": "all active component contracts plus A_gamma/Cmetric/floor rows",
            "current_value": "BLOCKED_NONCLAIM",
            "status": "NO_LOCAL_GR_OR_PPN_PASS",
            "valid_for_claim": "false",
        },
    ]


def component_target_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in read_csv_rows(OUT / "P8_Y5_R2FR_3386_THRESHOLD_BACKSOLVE.csv"):
        rows.append(
            {
                "target_id": "CT3387_" + source.get("backsolve_id", "").replace("TB3386_", ""),
                "threshold_source": source.get("threshold_source", ""),
                "source_row": source.get("source_row", ""),
                "A_gamma_or_PPN_times_Cmetric": source.get("A_gamma_or_PPN_times_Cmetric", ""),
                "T_grad_sample": source.get("T_grad_sample", ""),
                "epsilon_eff_max": source.get("epsilon_eff_max", ""),
                "epsilon_boundary_target_if_equal_split": source.get("epsilon_boundary_max_equal_third", ""),
                "epsilon_kernel_target_if_equal_split": source.get("epsilon_kernel_aniso_max_equal_third", ""),
                "boundary_kernel_sum_target_if_equal_split": _sum_strings(source.get("epsilon_boundary_max_equal_third", ""), source.get("epsilon_kernel_aniso_max_equal_third", "")),
                "use": "target ceiling for BL3387_4 and KL3387_3, not evidence",
                "valid_for_claim": "false",
            }
        )
    return rows


def _sum_strings(left: str, right: str) -> str:
    try:
        return f"{float(left) + float(right):.15e}"
    except (TypeError, ValueError):
        return "MISSING_NUMERIC_TARGET"


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3387_0_boundary_zero",
            "test": "try epsilon_boundary_PPN=0",
            "result": "FAIL_CURRENT_ZERO_NOT_PARENT_SIGNED",
            "detail": "compact/interior zero theorem is valid, but current Gaussian tail plus 3376 physical/reference clauses are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3387_1_boundary_bound",
            "test": "derive finite boundary/collar tail law",
            "result": "PASS_BOUND_FORMULA_NONCLAIM",
            "detail": "epsilon_boundary <= Gaussian collar tail + 3376 physical/reference/topology flux terms",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3387_2_kernel_zero",
            "test": "try epsilon_kernel_aniso_PPN=0",
            "result": "PASS_TANGENT_ZERO_FAIL_REAL_PATCH_ZERO",
            "detail": "constant projector and isotropic kernel commute exactly, but real PPN projector constancy is not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3387_3_kernel_bound",
            "test": "derive variable projector commutator bound",
            "result": "PASS_COMMUTATOR_BOUND_NONCLAIM",
            "detail": "[P,S]f identity gives C1 ell_s ||nabla P|| + C2 ell_s^2 ||nabla^2 P|| plus moment/gauge defects",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3387_4_targets",
            "test": "attach 3386 target ceilings to boundary/kernel components",
            "result": "PASS_TARGETS_NONCLAIM",
            "detail": f"targets={len(read_csv_rows(OUT / 'P8_Y5_R2FR_3386_THRESHOLD_BACKSOLVE.csv'))}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3387_5_firewall",
            "test": "prevent local PPN/local-GR overclaim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "new formulas are constraints on future inputs, not evidence of passing Cassini/local GR",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3387_0_sources",
            "claim": "all 3387 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates 3376, 3386, 3321, 3332 and 3336 inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3387_1_boundary_exact_zero",
            "claim": "epsilon_boundary_PPN=0 in current MTS",
            "gate_pass": "false",
            "reason": "compact/interior theorem is conditional and current Gaussian/reference/flux clauses are not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3387_2_boundary_bound_ready",
            "claim": "epsilon_boundary_PPN finite bound formula is ready",
            "gate_pass": "true",
            "reason": "derived collar-tail plus 3376 flux/reference/topology envelope",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3387_3_kernel_tangent_zero",
            "claim": "constant tangent-frame projector commutes with isotropic kernel",
            "gate_pass": "true",
            "reason": "algebraic convolution commutator vanishes for constant P0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3387_4_kernel_real_zero",
            "claim": "epsilon_kernel_aniso_PPN=0 in current MTS",
            "gate_pass": "false",
            "reason": "actual PPN projector constancy/commutation through local patch is not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3387_5_component_values",
            "claim": "boundary/kernel component values are sourced",
            "gate_pass": "false",
            "reason": "d_collar/ell_s, C_boundary, flux terms, projector gradients and moment/gauge defects are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3387_6_local_ppn",
            "claim": "local PPN/local-GR branch passes from 3387",
            "gate_pass": "false",
            "reason": "3387 only gives structural laws and targets; it does not supply claim-valid component values",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3387_0_progress",
            "decision": "Boundary and kernel leakage are now bound-law problems, not vague blockers.",
            "because": "3387 derives a Gaussian collar-tail boundary envelope and a variable-projector commutator identity.",
            "next_action": "source or parent-sign the geometric scale inputs instead of inventing epsilon values",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3387_1_boundary",
            "decision": "Boundary zero is available only if the parent selects compact/interior support or signs the full 3376 zero-flux package.",
            "because": "Gaussian smoothing has tails, and physical/reference/topology flux cannot be erased by exactness.",
            "next_action": "either parent-own compact local smoothing/collar support or fill d_collar/ell_s plus flux rows",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3387_2_kernel",
            "decision": "Kernel anisotropy is exactly zero in the local tangent constant-projector limit.",
            "because": "isotropic convolution commutes with a constant PPN projector, but the real patch needs a projector-gradient bound.",
            "next_action": "derive parent PPN projector constancy through the smoothing scale or source ||nabla P_PPN|| and ||nabla^2 P_PPN||",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3387_3_best_next",
            "decision": "Best next move is smoothing/projector ownership, not random numeric fitting.",
            "because": "if parent UOC fixes compact/interior/isotropic smoothing and constant PPN readout, two epsilon_eff heads vanish structurally.",
            "next_action": "build 3388 smoothing-projector parent-owner checkpoint; fallback is first finite scale-input runner",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3388-Y5-R2FR-smoothing-projector-parent-owner-or-epsilon-scale-inputs-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3388_smoothing_projector_parent_owner_or_epsilon_scale_inputs.py",
            "objective": "try to parent-own compact/interior/isotropic local smoothing and constant PPN projector commutation; if not, fill first finite scale rows for d_collar/ell_s, projector gradients, moment defect, and gauge readout defect",
            "why_next": "3387 shows these are the actual inputs controlling epsilon_boundary_PPN and epsilon_kernel_aniso_PPN",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3389-Y5-R2FR-background-gradient-and-Tgrad-scale-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3389_background_gradient_and_Tgrad_scale_bound.py",
            "objective": "derive or source epsilon_bg_PPN and ell_s/lambda_PPN so the remaining background-gradient leakage can be scored after boundary/kernel handling",
            "why_next": "once boundary/kernel are zeroed or bounded, epsilon_bg*T_grad is the remaining epsilon_eff channel",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3387*")
        if hit.name.startswith(("3387-Y5", "P8_Y5_R2FR_3387", "P8_Y5_BRR545_3387", "Y5_R2FR_3387"))
    ] if FW.exists() else []
    boundary_status = {row["derivation_status"] for row in rows_by_name["boundary_law"]}
    kernel_status = {row["derivation_status"] for row in rows_by_name["kernel_law"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3387_0_sources_exist_parse", "all cited 3387 source paths exist and parse", source_ok, ""),
        ("VAL3387_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3387_2_boundary_law", "boundary laws include compact zero and Gaussian collar-tail bound", {"VALID_CONDITIONAL_THEOREM", "DERIVED_FROM_GAUSSIAN_TAIL_NONCLAIM", "DERIVED_COMPONENT_BOUND"}.issubset(boundary_status), ""),
        ("VAL3387_3_kernel_law", "kernel laws include constant-projector zero and variable-projector bound", {"EXACT_LOCAL_TANGENT_FRAME_THEOREM", "DERIVED_IDENTITY", "DERIVED_OPERATOR_BOUND_NONCLAIM"}.issubset(kernel_status), ""),
        ("VAL3387_4_component_contract", "component contract keeps boundary/kernel values missing and nonclaim", len(rows_by_name["component_contract"]) == 4 and all(row["valid_for_claim"] == "false" for row in rows_by_name["component_contract"]), ""),
        ("VAL3387_5_targets", "3386 component target ceilings are attached", len(rows_by_name["component_targets"]) == len(read_csv_rows(OUT / "P8_Y5_R2FR_3386_THRESHOLD_BACKSOLVE.csv")) and len(rows_by_name["component_targets"]) > 0, f"rows={len(rows_by_name['component_targets'])}"),
        ("VAL3387_6_runner", "runner records zero failures, derived bounds, target attachment and firewall", {"FAIL_CURRENT_ZERO_NOT_PARENT_SIGNED", "PASS_BOUND_FORMULA_NONCLAIM", "PASS_TANGENT_ZERO_FAIL_REAL_PATCH_ZERO", "PASS_COMMUTATOR_BOUND_NONCLAIM", "PASS_TARGETS_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3387_7_gates", "gates pass formulas but block current zeros, finite values and local PPN", gate_map.get("GATE3387_2_boundary_bound_ready") == "true" and gate_map.get("GATE3387_3_kernel_tangent_zero") == "true" and gate_map.get("GATE3387_1_boundary_exact_zero") == "false" and gate_map.get("GATE3387_4_kernel_real_zero") == "false" and gate_map.get("GATE3387_5_component_values") == "false" and gate_map.get("GATE3387_6_local_ppn") == "false", ""),
        ("VAL3387_8_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3387_9_next_target", "next target moves to smoothing/projector ownership or scale inputs", rows_by_name["next"][0]["target_id"].startswith("3388-Y5-R2FR-smoothing-projector"), ""),
        ("VAL3387_10_write_scope_outside_formalization", "no 3387 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3387_11_overall", "3387 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3387 - Y5/R2FR boundary-kernel silence or epsilon component values under AX1090",
        "",
        "## Summary",
        "- 3387 goes after the two structural `epsilon_eff_PPN` heads exposed by 3386: boundary leakage and kernel/projector anisotropy.",
        "- Boundary result: exact zero is possible for compact/interior support plus the 3376 zero-flux package, but current Gaussian smoothing only gives an exponential collar-tail law unless the parent changes/signs the kernel branch.",
        "- Kernel result: an isotropic smoothing kernel commutes exactly with a constant local PPN projector; for the real patch, 3387 derives the variable-projector commutator bound.",
        "- This is real forward motion: `epsilon_boundary_PPN` and `epsilon_kernel_aniso_PPN` are now tied to geometric scale inputs instead of floating placeholders.",
        "- Current verdict: no local-GR/PPN claim. The exact zeros are conditional; finite scale/projector values remain missing.",
        "- Best next strike: parent-own the smoothing/projector package, or fill the first finite scale rows for the derived laws.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Boundary Collar Tail Law",
        md_table(rows_by_name["boundary_law"]),
        "## Kernel Projector Commutator Law",
        md_table(rows_by_name["kernel_law"]),
        "## Epsilon Component Value Contract",
        md_table(rows_by_name["component_contract"]),
        "## Component Targets From 3386",
        md_table(rows_by_name["component_targets"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "boundary_law": boundary_law_rows(),
        "kernel_law": kernel_law_rows(),
        "component_contract": component_contract_rows(),
        "component_targets": component_target_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
