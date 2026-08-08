from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3388-Y5-R2FR-smoothing-projector-parent-owner-or-epsilon-scale-inputs-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3388_SOURCE_REGISTER.csv",
    "owner_attempt": OUT / "P8_Y5_R2FR_3388_SMOOTHING_PROJECTOR_OWNER_ATTEMPT.csv",
    "admissible_package": OUT / "P8_Y5_R2FR_3388_ADMISSIBLE_PACKAGE_CONTRACT.csv",
    "zero_implications": OUT / "P8_Y5_R2FR_3388_ZERO_IMPLICATIONS_AND_REDUCED_EPSILON.csv",
    "finite_inputs": OUT / "P8_Y5_R2FR_3388_FIRST_SCALE_INPUT_ROWS_NONCLAIM.csv",
    "target_requirements": OUT / "P8_Y5_R2FR_3388_SCALE_TARGET_REQUIREMENTS.csv",
    "runner": OUT / "P8_Y5_R2FR_3388_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3388_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3388_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3388_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3388_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3388_0_3387_doc", ROOT / "3387-Y5-R2FR-boundary-kernel-silence-or-epsilon-component-values-under-AX1090.md", "3387 boundary/kernel handoff"),
    ("SRC3388_1_3387_boundary", OUT / "P8_Y5_R2FR_3387_BOUNDARY_COLLAR_TAIL_LAW.csv", "boundary collar-tail law"),
    ("SRC3388_2_3387_kernel", OUT / "P8_Y5_R2FR_3387_KERNEL_PROJECTOR_COMMUTATOR_LAW.csv", "kernel projector commutator law"),
    ("SRC3388_3_3387_contract", OUT / "P8_Y5_R2FR_3387_EPSILON_COMPONENT_VALUE_CONTRACT.csv", "component value contract"),
    ("SRC3388_4_3387_targets", OUT / "P8_Y5_R2FR_3387_COMPONENT_TARGETS_FROM_3386.csv", "boundary/kernel target ceilings"),
    ("SRC3388_5_3386_finite_inputs", OUT / "P8_Y5_R2FR_3386_FIRST_FINITE_INPUT_ROWS_NONCLAIM.csv", "epsilon finite inputs"),
    ("SRC3388_6_3321_kernel", OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv", "Gaussian smoothing law"),
    ("SRC3388_7_3320_doc", ROOT / "3320-Y5-R2FR-local-first-gradient-silence-or-gradient-envelope-under-AX1090.md", "first-gradient silence and compact-kernel boundary form"),
    ("SRC3388_8_3376_doc", ROOT / "3376-Y5-R2FR-boundary-zero-flux-or-Bzero-first-row-under-AX1090.md", "boundary zero-flux package"),
    ("SRC3388_9_3376_zero", OUT / "P8_Y5_R2FR_3376_BOUNDARY_ZERO_FLUX_THEOREM_ATTEMPT.csv", "boundary zero-flux theorem attempt"),
    ("SRC3388_10_parent_local_zero_clause", OUT / "P8_PARENT_LOCAL_ZERO_ACTION_CLAUSE.csv", "partial parent local-zero/trace projector clause"),
    ("SRC3388_11_parent_local_zero_scorecard", OUT / "P8_PARENT_LOCAL_ZERO_IDENTITY_SCORECARD.csv", "trace projector partial ownership and remaining blockers"),
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


def to_float(value: str, default: float = math.nan) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


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


def owner_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "OWN3388_0_single_observed_geometry",
            "object": "UOC observed geometry/coframe",
            "required_parent_clause": "all local readout, smoothing, and PPN projection are built from the same observed metric/coframe before matter/source projection",
            "current_evidence": "post-UOC branch supports one public geometry, but smoothing/projector ownership is not signed as part of the parent action",
            "result": "STRUCTURAL_ROUTE_PRESENT_NOT_PARENT_SIGNED",
            "effect_if_signed": "removes hidden second-frame source for kernel/projector leakage",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OWN3388_1_smoothing_owner",
            "object": "S_ell",
            "required_parent_clause": "S_ell is a parent-owned local readout functor: normalized, scalar, isotropic in h_mu_nu, zero first moment, source/species blind, fixed before variation",
            "current_evidence": "3321 uses a Gaussian model; 3320 uses compact-kernel stationarity as a sufficient route, but neither is parent-signed",
            "result": "CANDIDATE_PACKAGE_NOT_SIGNED",
            "effect_if_signed": "kernel moment/aniso defects become zero except controlled collar tail for Gaussian branch",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OWN3388_2_compact_support_branch",
            "object": "compact/interior smoothing",
            "required_parent_clause": "support radius rho_K ell_s is strictly inside source-free collar: d_collar >= rho_K ell_s",
            "current_evidence": "3387 exact boundary zero theorem is valid for compact/interior support, but current imported kernel is Gaussian/infinite-tail",
            "result": "EXACT_BOUNDARY_ZERO_BRANCH_NOT_CURRENT_KERNEL",
            "effect_if_signed": "epsilon_boundary_tail=0 before physical/reference flux terms",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OWN3388_3_gaussian_branch",
            "object": "Gaussian heat-kernel style smoothing",
            "required_parent_clause": "Gaussian/heat-kernel smoothing is accepted as the parent readout; boundary is controlled by exp[-d_collar^2/(2 ell_s^2)] not exact zero",
            "current_evidence": "3321 and 3387 already derive Gaussian transfer/tail laws",
            "result": "FINITE_TAIL_BRANCH_FORMULA_READY",
            "effect_if_signed": "epsilon_boundary is a scale-separation input instead of an arbitrary closure",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OWN3388_4_constant_projector",
            "object": "P_PPN",
            "required_parent_clause": "P_PPN=P0 through the smoothing support in local normal/Fermi frame, with gauge/readout fixed before smoothing",
            "current_evidence": "3387 proves [P0,S_ell]=0 exactly, but actual P_PPN constancy through the real patch is not parent-signed",
            "result": "TANGENT_THEOREM_VALID_REAL_PATCH_UNSIGNED",
            "effect_if_signed": "epsilon_kernel_aniso_PPN=0 up to explicitly retained gauge/moment defects",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OWN3388_5_trace_projector_partial",
            "object": "trace/coherent projector",
            "required_parent_clause": "parent local-zero variables X and Qcoh=hX/3 own the trace projector rather than arbitrary smoothing",
            "current_evidence": "P8_PARENT_LOCAL_ZERO_IDENTITY_SCORECARD marks trace projector owner as partial_formal_pass, with STF/stress/boundary/R11 re-entry missing",
            "result": "PARTIAL_PROJECTOR_WIN_NOT_FULL_PPN_PROJECTOR",
            "effect_if_signed": "helps trace channel, but does not silence full PPN anisotropy/preferred-frame/projector stress",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "OWN3388_6_verdict",
            "object": "smoothing/projector package",
            "required_parent_clause": "OWN3388_0 through OWN3388_5 close in one local branch",
            "current_evidence": "conditional pieces exist, but compact support/current kernel choice, real-patch projector constancy, and stress/boundary clauses do not close together",
            "result": "PARENT_OWNER_NOT_CLOSED_SCALE_INPUTS_REQUIRED",
            "effect_if_signed": "would reduce epsilon_eff_PPN to epsilon_bg_PPN*T_grad(lambda_PPN)",
            "valid_for_claim": "false",
        },
    ]


def admissible_package_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PKG3388_0_branch_selector",
            "clause": "choose one smoothing branch before tests",
            "mathematical_content": "K_ell is either compact bump with support rho_K ell_s or Gaussian/heat-kernel with known tail",
            "forbidden_shortcut": "switch kernels after seeing local bound pressure",
            "current_status": "NOT_PARENT_DECLARED",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PKG3388_1_normalized_isotropic_kernel",
            "clause": "kernel normalization and isotropy",
            "mathematical_content": "int K_ell dV_h=1; int z^i K_ell(z)dV_h=0; K_ell(z)=k(|z|_h/ell_s)",
            "forbidden_shortcut": "anisotropic readout hidden inside an isotropic Poisson source",
            "current_status": "MODEL_READY_PARENT_SIGNATURE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PKG3388_2_variation_order",
            "clause": "smoothing/readout fixed before source projection",
            "mathematical_content": "delta S_ell and delta P_PPN are either included in stress/residuals or theorem-zero; no post-readout mask",
            "forbidden_shortcut": "choose smoothing/projector after varying matter/source",
            "current_status": "REQUIRED_GUARD_ACTIVE",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PKG3388_3_local_collar",
            "clause": "source-free collar scale",
            "mathematical_content": "d_collar/ell_s is declared in the same observed frame; compact branch requires d_collar >= rho_K ell_s",
            "forbidden_shortcut": "call boundary zero without proving kernel support stays inside the collar",
            "current_status": "FINITE_SCALE_INPUT_MISSING",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PKG3388_4_projector_constancy",
            "clause": "PPN projector is constant or bounded across the smoothing cell",
            "mathematical_content": "P_PPN(x)=P0+DeltaP; ||DeltaP|| <= ell_s||nabla P|| + ell_s^2||nabla^2 P||/2 + ...",
            "forbidden_shortcut": "spend tangent-frame commutation as a real-patch theorem",
            "current_status": "BOUND_READY_NUMERIC_INPUTS_MISSING",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PKG3388_5_gauge_readout_lock",
            "clause": "PPN gauge/readout does not drift under smoothing",
            "mathematical_content": "epsilon_gauge_readout=0 or is included additively in epsilon_kernel_aniso_PPN",
            "forbidden_shortcut": "hide gauge drift inside Cmetric",
            "current_status": "FINITE_INPUT_MISSING",
            "valid_for_claim": "false",
        },
    ]


def zero_implication_rows() -> list[dict[str, str]]:
    return [
        {
            "implication_id": "ZI3388_0_compact_exact",
            "premises": "PKG3388 compact branch; d_collar >= rho_K ell_s; 3376 physical/reference/topology flux zero; constant P_PPN; zero moment/gauge defects",
            "conclusion": "epsilon_boundary_PPN=0 and epsilon_kernel_aniso_PPN=0",
            "reduced_formula": "epsilon_eff_PPN <= epsilon_bg_PPN*T_grad(lambda_PPN)",
            "current_status": "CONDITIONAL_NOT_CURRENT_CLAIM",
            "why_not_claim": "compact kernel/support and full 3376/PPN-projector package are not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "ZI3388_1_gaussian_finite",
            "premises": "Gaussian branch; finite d_collar/ell_s; finite projector gradients; physical flux rows retained",
            "conclusion": "epsilon_boundary_PPN and epsilon_kernel_aniso_PPN are computable upper bounds",
            "reduced_formula": "epsilon_eff <= epsilon_bg*T_grad + C_B exp[-d^2/(2ell_s^2)] + flux/M_H_ref + C1 ell_s||nabla P|| + C2 ell_s^2||nabla^2P|| + epsilon_moment + epsilon_gauge",
            "current_status": "DERIVED_BOUND_FORMULA_READY",
            "why_not_claim": "scale/projector/flux values are missing",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "ZI3388_2_trace_partial",
            "premises": "parent local-zero trace projector clause only",
            "conclusion": "trace/coherent smoothing ambiguity is reduced, but full PPN anisotropic/preferred-frame projector leakage remains",
            "reduced_formula": "epsilon_kernel_aniso still retains STF/projector-stress/gauge terms",
            "current_status": "PARTIAL_PROGRESS_ONLY",
            "why_not_claim": "trace ownership does not prove full PPN projector constancy or zero stress variation",
            "valid_for_claim": "false",
        },
        {
            "implication_id": "ZI3388_3_local_gr_firewall",
            "premises": "all current 3388 rows only",
            "conclusion": "no local-GR/PPN claim follows",
            "reduced_formula": "claim requires source-backed values or parent-signed zeros for every additive term",
            "current_status": "FIREWALL_ACTIVE",
            "why_not_claim": "3388 produces contracts and scale targets, not evidence of passing bounds",
            "valid_for_claim": "false",
        },
    ]


def finite_input_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "SI3388_0_kernel_branch",
            "quantity": "kernel_branch",
            "definition": "compact_bump or gaussian_heat_kernel selected before tests",
            "needed_for": "decide exact collar zero versus exponential tail",
            "current_value": "MISSING_PARENT_KERNEL_BRANCH_DECLARATION",
            "units": "categorical",
            "source_or_theorem_required": "parent readout/smoothing clause",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SI3388_1_d_over_ell",
            "quantity": "d_collar/ell_s",
            "definition": "source-free collar distance divided by smoothing length",
            "needed_for": "epsilon_boundary_tail <= C_B exp[-(d/ell)^2/2]",
            "current_value": "MISSING_D_COLLAR_OVER_ELL_S",
            "units": "dimensionless",
            "source_or_theorem_required": "same-frame local geometry and smoothing scale",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SI3388_2_C_boundary",
            "quantity": "C_boundary",
            "definition": "operator/source amplitude multiplying Gaussian boundary tail",
            "needed_for": "boundary tail normalization",
            "current_value": "MISSING_C_BOUNDARY",
            "units": "dimensionless",
            "source_or_theorem_required": "norm of boundary readout relative to EH PPN response",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SI3388_3_flux_envelope",
            "quantity": "epsilon_boundary_physical",
            "definition": "(|B_zero_flux|+|Delta_symp|+|Phi_Poynting_bound|+|corner/topology|)/M_H_ref + epsilon_worldtube_mismatch",
            "needed_for": "physical/reference/topology part of epsilon_boundary_PPN",
            "current_value": "MISSING_3376_FLUX_REFERENCE_VALUES",
            "units": "dimensionless",
            "source_or_theorem_required": "3376 zero theorem or source-backed finite rows",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SI3388_4_projector_gradient",
            "quantity": "ell_s ||nabla P_PPN||",
            "definition": "first-order real-patch variation of local PPN projector across smoothing cell",
            "needed_for": "kernel commutator bound",
            "current_value": "MISSING_PROJECTOR_GRADIENT_NORM",
            "units": "dimensionless",
            "source_or_theorem_required": "parent PPN readout/gauge convention and local metric derivative bound",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SI3388_5_projector_hessian",
            "quantity": "ell_s^2 ||nabla^2 P_PPN||",
            "definition": "second-order projector variation across smoothing cell",
            "needed_for": "kernel commutator bound beyond tangent limit",
            "current_value": "MISSING_PROJECTOR_HESSIAN_NORM",
            "units": "dimensionless",
            "source_or_theorem_required": "local metric/gauge curvature bound",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SI3388_6_kernel_moment_defect",
            "quantity": "epsilon_kernel_moment",
            "definition": "nonzero first moment or anisotropic moment defect of actual smoothing kernel",
            "needed_for": "kernel anisotropy residual",
            "current_value": "MISSING_KERNEL_MOMENT_DEFECT",
            "units": "dimensionless",
            "source_or_theorem_required": "isotropic normalized kernel theorem or moment calculation",
            "valid_for_claim": "false",
        },
        {
            "input_id": "SI3388_7_gauge_readout_defect",
            "quantity": "epsilon_gauge_readout",
            "definition": "PPN gauge/readout drift introduced by smoothing and local frame choice",
            "needed_for": "kernel anisotropy residual and Cmetric separation",
            "current_value": "MISSING_GAUGE_READOUT_DEFECT",
            "units": "dimensionless",
            "source_or_theorem_required": "fixed PPN gauge/readout convention in UOC branch",
            "valid_for_claim": "false",
        },
    ]


def target_requirement_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in read_csv_rows(OUT / "P8_Y5_R2FR_3387_COMPONENT_TARGETS_FROM_3386.csv"):
        boundary_target = to_float(source.get("epsilon_boundary_target_if_equal_split", ""))
        kernel_target = to_float(source.get("epsilon_kernel_target_if_equal_split", ""))
        boundary_d_over_ell = math.sqrt(2.0 * math.log(1.0 / boundary_target)) if 0.0 < boundary_target < 1.0 else math.nan
        rows.append(
            {
                "target_id": "STR3388_" + source.get("target_id", "").replace("CT3387_", ""),
                "threshold_source": source.get("threshold_source", ""),
                "source_row": source.get("source_row", ""),
                "A_gamma_or_PPN_times_Cmetric": source.get("A_gamma_or_PPN_times_Cmetric", ""),
                "T_grad_sample": source.get("T_grad_sample", ""),
                "epsilon_boundary_target": source.get("epsilon_boundary_target_if_equal_split", ""),
                "required_d_collar_over_ell_if_Cboundary_1_and_flux_zero": f"{boundary_d_over_ell:.12e}" if math.isfinite(boundary_d_over_ell) else "MISSING_OR_NOT_APPLICABLE",
                "epsilon_kernel_target": source.get("epsilon_kernel_target_if_equal_split", ""),
                "required_ell_gradP_if_C1_1_and_other_kernel_terms_zero": f"{kernel_target:.15e}" if math.isfinite(kernel_target) else "MISSING_OR_NOT_APPLICABLE",
                "required_ell2_hessP_if_C2_1_and_other_kernel_terms_zero": f"{kernel_target:.15e}" if math.isfinite(kernel_target) else "MISSING_OR_NOT_APPLICABLE",
                "status": "TARGET_REQUIREMENT_ONLY_NONCLAIM",
                "valid_for_claim": "false",
            }
        )
    return rows


def runner_rows(targets: list[dict[str, str]]) -> list[dict[str, str]]:
    harsh_targets = [
        row for row in targets
        if row.get("A_gamma_or_PPN_times_Cmetric") in {"1.000000e+12", "1.000000e+16"}
    ]
    return [
        {
            "run_id": "RUN3388_0_parent_owner_attempt",
            "test": "try to parent-own smoothing/projector package",
            "result": "FAIL_CURRENT_PARENT_OWNER_NOT_CLOSED",
            "detail": "conditional components exist, but current corpus lacks one signed kernel/projector/collar/stress package",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3388_1_admissible_contract",
            "test": "write exact admissible package clauses",
            "result": "PASS_CONTRACT_WRITTEN_NONCLAIM",
            "detail": "kernel branch, isotropy, variation order, collar, projector constancy and gauge lock are explicit",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3388_2_zero_implications",
            "test": "derive exact-zero implications if package closes",
            "result": "PASS_CONDITIONAL_ZERO_MAP",
            "detail": "compact/interior support plus constant projector reduces epsilon_eff to epsilon_bg*T_grad",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3388_3_scale_inputs",
            "test": "stage finite scale input rows",
            "result": "PASS_SCALE_INPUT_ROWS_NONCLAIM",
            "detail": "kernel branch, d/ell, C_boundary, flux, projector gradients, moment and gauge defects are rowed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3388_4_target_requirements",
            "test": "translate 3387 component ceilings into scale requirements",
            "result": "PASS_TARGET_REQUIREMENTS_NONCLAIM",
            "detail": f"rows={len(targets)}; harsh_rows={len(harsh_targets)}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3388_5_firewall",
            "test": "prevent local PPN/local-GR overclaim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "no zero theorem or finite row is claim-valid yet",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3388_0_sources",
            "claim": "all 3388 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates 3387/3386/3376/3321/3320/local-zero inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3388_1_parent_owner",
            "claim": "smoothing/projector package is parent-signed",
            "gate_pass": "false",
            "reason": "kernel branch, collar support, real-patch projector constancy, gauge lock and stress clauses are not signed together",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3388_2_exact_boundary_kernel_zero",
            "claim": "epsilon_boundary=epsilon_kernel_aniso=0",
            "gate_pass": "false",
            "reason": "exact zero follows only under compact/interior support plus full zero-flux and constant-projector package",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3388_3_bound_laws",
            "claim": "finite boundary/kernel scale laws are ready",
            "gate_pass": "true",
            "reason": "3387 laws plus 3388 input contract and target requirements are explicit",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3388_4_scale_values",
            "claim": "finite scale values are sourced",
            "gate_pass": "false",
            "reason": "d/ell, C_boundary, flux envelope, projector gradients, moment and gauge defects remain MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3388_5_local_ppn",
            "claim": "local PPN/local-GR branch passes from 3388",
            "gate_pass": "false",
            "reason": "3388 supplies contracts/targets only; no claim-valid component values or parent zeros",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(targets: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3388_0_progress",
            "decision": "The smoothing/projector bottleneck is now an admissible-package theorem or finite-scale runner, not a vague closure.",
            "because": "3388 states the exact clauses needed to spend boundary/kernel zeros and converts 3387 targets into d/ell and projector-gradient requirements.",
            "next_action": "source or derive the scale inputs rather than fitting epsilon_boundary or epsilon_kernel directly",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3388_1_kernel_branch",
            "decision": "Current Gaussian branch cannot give exact boundary zero by itself.",
            "because": "Gaussian tails are noncompact; boundary zero requires compact/interior support or an exponentially small tail plus physical flux rows.",
            "next_action": "either parent-adopt compact local smoothing or fill d_collar/ell_s and C_boundary",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3388_2_projector",
            "decision": "The constant-projector theorem is a genuine local tangent result but not yet a real-patch PPN proof.",
            "because": "actual P_PPN variation across the smoothing cell must be zero-signed or bounded by ell_s||nabla P|| and ell_s^2||nabla^2P||.",
            "next_action": "derive local PPN projector constancy from UOC normal-frame readout or source projector-gradient norms",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3388_3_best_next",
            "decision": "Best next move is a scale-separation input runner before returning to background gradient.",
            "because": f"there are {len(targets)} target rows; without d/ell and projector-gradient values, 3386/3387 cannot be scored.",
            "next_action": "build 3389 finite scale-input runner for d_collar/ell_s, projector gradients, moment defect and gauge defect",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3389-Y5-R2FR-finite-epsilon-scale-input-runner-or-compact-kernel-adoption-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3389_finite_epsilon_scale_input_runner_or_compact_kernel_adoption.py",
            "objective": "source or derive d_collar/ell_s, C_boundary, projector-gradient norms, kernel moment defect and gauge readout defect; alternatively parent-adopt a compact/interior kernel package and route exact zero through the same gates",
            "why_next": "3388 shows these concrete scale inputs decide whether boundary/kernel epsilon channels pass the target ceilings",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3390-Y5-R2FR-background-gradient-and-Tgrad-scale-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3390_background_gradient_and_Tgrad_scale_bound.py",
            "objective": "derive or source epsilon_bg_PPN and ell_s/lambda_PPN after boundary/kernel scale inputs are handled",
            "why_next": "if boundary/kernel become zero or bounded, epsilon_bg*T_grad is the remaining epsilon_eff channel",
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
        for hit in FW.rglob("*3388*")
        if hit.name.startswith(("3388-Y5", "P8_Y5_R2FR_3388", "P8_Y5_BRR545_3388", "Y5_R2FR_3388"))
    ] if FW.exists() else []
    owner_results = {row["result"] for row in rows_by_name["owner_attempt"]}
    package_ids = {row["clause_id"] for row in rows_by_name["admissible_package"]}
    input_ids = {row["input_id"] for row in rows_by_name["finite_inputs"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3388_0_sources_exist_parse", "all cited 3388 source paths exist and parse", source_ok, ""),
        ("VAL3388_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3388_2_owner_attempt", "owner attempt fails current claim but identifies scale-input fallback", "PARENT_OWNER_NOT_CLOSED_SCALE_INPUTS_REQUIRED" in owner_results, ""),
        ("VAL3388_3_package_contract", "admissible package includes branch, isotropy, variation order, collar, projector and gauge clauses", {"PKG3388_0_branch_selector", "PKG3388_1_normalized_isotropic_kernel", "PKG3388_2_variation_order", "PKG3388_3_local_collar", "PKG3388_4_projector_constancy", "PKG3388_5_gauge_readout_lock"}.issubset(package_ids), ""),
        ("VAL3388_4_finite_inputs", "finite scale input rows cover kernel branch, collar, boundary, flux, projector, moment and gauge defects", {"SI3388_0_kernel_branch", "SI3388_1_d_over_ell", "SI3388_2_C_boundary", "SI3388_3_flux_envelope", "SI3388_4_projector_gradient", "SI3388_5_projector_hessian", "SI3388_6_kernel_moment_defect", "SI3388_7_gauge_readout_defect"}.issubset(input_ids), ""),
        ("VAL3388_5_target_requirements", "scale target requirements attach 3387 component targets", len(rows_by_name["target_requirements"]) == len(read_csv_rows(OUT / "P8_Y5_R2FR_3387_COMPONENT_TARGETS_FROM_3386.csv")) and len(rows_by_name["target_requirements"]) > 0, f"rows={len(rows_by_name['target_requirements'])}"),
        ("VAL3388_6_runner", "runner records owner failure, contract, zero map, scale rows, targets and firewall", {"FAIL_CURRENT_PARENT_OWNER_NOT_CLOSED", "PASS_CONTRACT_WRITTEN_NONCLAIM", "PASS_CONDITIONAL_ZERO_MAP", "PASS_SCALE_INPUT_ROWS_NONCLAIM", "PASS_TARGET_REQUIREMENTS_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3388_7_gates", "gates block parent owner, exact zeros, finite values and local PPN while passing bound laws", gate_map.get("GATE3388_1_parent_owner") == "false" and gate_map.get("GATE3388_2_exact_boundary_kernel_zero") == "false" and gate_map.get("GATE3388_3_bound_laws") == "true" and gate_map.get("GATE3388_4_scale_values") == "false" and gate_map.get("GATE3388_5_local_ppn") == "false", ""),
        ("VAL3388_8_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3388_9_next_target", "next target moves to finite scale-input runner or compact-kernel adoption", rows_by_name["next"][0]["target_id"].startswith("3389-Y5-R2FR-finite-epsilon-scale-input"), ""),
        ("VAL3388_10_write_scope_outside_formalization", "no 3388 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3388_11_overall", "3388 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3388 - Y5/R2FR smoothing-projector parent owner or epsilon scale inputs under AX1090",
        "",
        "## Summary",
        "- 3388 attacks the exact fork exposed by 3387: can the local smoothing/projector package be parent-owned strongly enough to spend `epsilon_boundary_PPN=epsilon_kernel_aniso_PPN=0`?",
        "- Verdict: not yet. The package is now explicit, but the current corpus does not sign kernel branch, collar support, real-patch PPN projector constancy, gauge lock, and stress/boundary clauses together.",
        "- Real progress: exact zero conditions and finite scale fallback now share one contract instead of two disconnected stories.",
        "- Compact/interior branch: if parent-adopted and paired with the 3376 zero-flux package, boundary/kernel leakage can vanish structurally.",
        "- Gaussian branch: current formulas stay finite and testable through `d_collar/ell_s`, `C_boundary`, projector gradients, moment defect, gauge defect, and physical flux rows.",
        f"- Scale discipline: `{len(rows_by_name['target_requirements'])}` target rows translate the 3387 component ceilings into required collar and projector-gradient sizes.",
        "- No local-GR/PPN claim is allowed from 3388; it creates the next executable scale-input runner.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Smoothing Projector Owner Attempt",
        md_table(rows_by_name["owner_attempt"]),
        "## Admissible Package Contract",
        md_table(rows_by_name["admissible_package"]),
        "## Zero Implications And Reduced Epsilon",
        md_table(rows_by_name["zero_implications"]),
        "## First Scale Input Rows",
        md_table(rows_by_name["finite_inputs"]),
        "## Scale Target Requirements",
        md_table(rows_by_name["target_requirements"]),
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
    targets = target_requirement_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "owner_attempt": owner_attempt_rows(),
        "admissible_package": admissible_package_rows(),
        "zero_implications": zero_implication_rows(),
        "finite_inputs": finite_input_rows(),
        "target_requirements": targets,
        "runner": runner_rows(targets),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(targets),
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
