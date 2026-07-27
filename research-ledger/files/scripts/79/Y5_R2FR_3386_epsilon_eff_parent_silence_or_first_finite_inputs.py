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
DOC = ROOT / "3386-Y5-R2FR-epsilon-eff-parent-silence-or-first-finite-inputs-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3386_SOURCE_REGISTER.csv",
    "component_decomposition": OUT / "P8_Y5_R2FR_3386_EPSILON_COMPONENT_DECOMPOSITION.csv",
    "parent_silence": OUT / "P8_Y5_R2FR_3386_PARENT_SILENCE_ATTEMPT.csv",
    "finite_inputs": OUT / "P8_Y5_R2FR_3386_FIRST_FINITE_INPUT_ROWS_NONCLAIM.csv",
    "threshold_backsolve": OUT / "P8_Y5_R2FR_3386_THRESHOLD_BACKSOLVE.csv",
    "runner": OUT / "P8_Y5_R2FR_3386_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3386_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3386_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3386_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3386_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3386_0_3385_doc", DOC.parent / "3385-Y5-R2FR-A_gamma-Cmetric-epsilon-eff-first-numeric-PPN-runner-under-AX1090.md", "3385 Cassini gamma runner handoff"),
    ("SRC3386_1_3385_thresholds", OUT / "P8_Y5_R2FR_3385_EPSILON_EFF_THRESHOLDS_NONCLAIM.csv", "full-gamma epsilon_eff thresholds from Cassini comparator"),
    ("SRC3386_2_3385_missing", OUT / "P8_Y5_R2FR_3385_MISSING_INPUTS_FOR_CLAIM.csv", "3385 missing input ledger"),
    ("SRC3386_3_3384_cmetric", OUT / "P8_Y5_R2FR_3384_CMETRIC_EPSILON_ZERO_OR_BOUND_ATTEMPT.csv", "3384 Cmetric/epsilon zero attempt"),
    ("SRC3386_4_3332_doc", DOC.parent / "3332-Y5-R2FR-PPN-epsilon-eff-and-floor-specialization-under-AX1090.md", "3332 epsilon_eff specialization"),
    ("SRC3386_5_3332_epsilon", OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv", "epsilon_eff decomposition and exact silence branch"),
    ("SRC3386_6_3321_kernel", OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv", "Gaussian T_grad transfer law"),
    ("SRC3386_7_3320_doc", DOC.parent / "3320-Y5-R2FR-local-first-gradient-silence-or-gradient-envelope-under-AX1090.md", "local first-gradient theorem attempt"),
    ("SRC3386_8_3320_gradient_attempt", OUT / "P8_Y5_R2FR_3320_FIRST_GRADIENT_THEOREM_ATTEMPT.csv", "first-gradient zero attempt"),
    ("SRC3386_9_3320_envelope", OUT / "P8_Y5_R2FR_3320_EPSILON_GRAD_ENVELOPE.csv", "epsilon_grad envelope fallback"),
    ("SRC3386_10_3335_tree_scenarios", OUT / "P8_Y5_R2FR_3335_TREE_EPSILON_SCENARIOS.csv", "tree epsilon scenario smoke rows"),
    ("SRC3386_11_3336_tree_contract", OUT / "P8_Y5_R2FR_3336_TREE_EPSILON_BOUND_CONTRACT.csv", "tree-partition epsilon_eff contract"),
    ("SRC3386_12_3336_required_inputs", OUT / "P8_Y5_R2FR_3336_REQUIRED_SOURCE_INPUTS.csv", "epsilon source-input requirements"),
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


def component_decomposition_rows() -> list[dict[str, str]]:
    return [
        {
            "component_id": "EC3386_0_background_gradient",
            "quantity": "epsilon_bg_PPN*T_grad(lambda_PPN)",
            "formula": "epsilon_bg_PPN * (ell_s/lambda_PPN) exp[-ell_s^2/(2 lambda_PPN^2)]",
            "meaning": "background first-gradient leakage after smoothing transfer",
            "zero_condition": "epsilon_bg_PPN=0 or T_grad(lambda_PPN)=0",
            "current_status": "FORMULA_READY_ZERO_NOT_PARENT_SIGNED",
            "needed_input": "parent-signed local first-gradient silence or numeric epsilon_bg_PPN and ell_s/lambda_PPN",
            "source_path": str(OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv"),
            "valid_for_claim": "false",
        },
        {
            "component_id": "EC3386_1_boundary",
            "quantity": "epsilon_boundary_PPN",
            "formula": "||local boundary/collar/source-worldtube leakage||_PPN",
            "meaning": "nonzero support, edge, or integration-by-parts flux leaking into the PPN readout",
            "zero_condition": "interior PPN patch plus parent-owned compact support/no-flux boundary silence",
            "current_status": "ZERO_CONDITIONAL_NOT_SIGNED",
            "needed_input": "boundary silence certificate or finite boundary leakage bound",
            "source_path": str(OUT / "P8_Y5_R2FR_3336_TREE_EPSILON_BOUND_CONTRACT.csv"),
            "valid_for_claim": "false",
        },
        {
            "component_id": "EC3386_2_kernel_anisotropy",
            "quantity": "epsilon_kernel_aniso_PPN",
            "formula": "||[P_PPN,S_ell] + anisotropic first-moment defect||",
            "meaning": "smoothing/projector anisotropy or kernel-PPN projection noncommutation",
            "zero_condition": "isotropic kernel and PPN projector commute on the local branch",
            "current_status": "ZERO_CONDITIONAL_NOT_SIGNED",
            "needed_input": "kernel isotropy/projector commutator zero theorem or finite commutator bound",
            "source_path": str(OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv"),
            "valid_for_claim": "false",
        },
        {
            "component_id": "EC3386_3_total",
            "quantity": "epsilon_eff_PPN",
            "formula": "epsilon_eff_PPN <= epsilon_bg_PPN*T_grad(lambda_PPN)+epsilon_boundary_PPN+epsilon_kernel_aniso_PPN",
            "meaning": "positive no-cancellation leakage budget for the tree-level PPN response",
            "zero_condition": "all three component channels vanish in the same parent branch",
            "current_status": "DECOMPOSED_NOT_CLAIMABLE",
            "needed_input": "simultaneous parent certificate or finite component values",
            "source_path": str(OUT / "P8_Y5_R2FR_3332_EPSILON_EFF_SPECIALIZATION.csv"),
            "valid_for_claim": "false",
        },
    ]


def parent_silence_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "PS3386_0_exact_chain",
            "claim": "epsilon_eff_PPN=0 under UOC/local branch",
            "sufficient_conditions": "epsilon_bg_PPN=0; epsilon_boundary_PPN=0; epsilon_kernel_aniso_PPN=0 in the same local PPN branch",
            "derivation_attempt": "Use 3332 exact silence plus 3320 first-gradient silence plus 3336 boundary/kernel conditional zero attempt.",
            "result": "CONDITIONAL_THEOREM_ONLY",
            "failure_or_gap": "the three zero clauses are individually conditional and not parent-signed together",
            "next_action": "try boundary/kernel zero first, then background gradient or scale-transfer bound",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PS3386_1_background_gradient_zero",
            "claim": "epsilon_bg_PPN=0",
            "sufficient_conditions": "pointwise constant local vacuum background or parent stationary/isotropic first-moment ensemble on smoothing support",
            "derivation_attempt": "3320 proves silence if partial_mu psi_bar=0 or if the smoothing first moment/cross covariance vanishes.",
            "result": "NOT_PARENT_SIGNED",
            "failure_or_gap": "current corpus supports smallness/slow variation but not exact real-branch first-gradient silence",
            "next_action": "derive local stationarity from parent field equation or keep epsilon_bg_PPN finite",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PS3386_2_boundary_zero",
            "claim": "epsilon_boundary_PPN=0",
            "sufficient_conditions": "PPN detector patch is interior, boundary flux vanishes, and source-worldtube readout is variation-before-readout",
            "derivation_attempt": "Integrate-by-parts form can silence boundary leakage if collar/source support is parent-owned.",
            "result": "PROMISING_BUT_UNSIGNED",
            "failure_or_gap": "boundary/source-worldtube silence has appeared repeatedly as conditional; no single parent local-collar certificate is signed",
            "next_action": "construct the local-collar boundary theorem or write the first finite epsilon_boundary row",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PS3386_3_kernel_anisotropy_zero",
            "claim": "epsilon_kernel_aniso_PPN=0",
            "sufficient_conditions": "isotropic smoothing kernel, zero first moment, and commutation with the PPN projection/gauge readout",
            "derivation_attempt": "The Gaussian transfer law is isotropic as a model, but the projection commutator has not been parent-owned.",
            "result": "PROMISING_BUT_UNSIGNED",
            "failure_or_gap": "model isotropy is not yet the same as a parent theorem for the actual local readout projector",
            "next_action": "prove [P_PPN,S_ell]=0 in the UOC branch or retain epsilon_kernel_aniso as finite input",
            "valid_for_claim": "false",
        },
        {
            "attempt_id": "PS3386_4_verdict",
            "claim": "local PPN tree leakage is zero",
            "sufficient_conditions": "all PS3386_1..3 close without changing branches",
            "derivation_attempt": "No-cancellation sum: zero total requires each nonnegative component channel to close.",
            "result": "ZERO_PROOF_NOT_CLOSED_CURRENTLY",
            "failure_or_gap": "the exact branch is mathematically clean but currently not parent-signed",
            "next_action": "promote the easiest clauses or run finite bound acquisition; no PPN claim",
            "valid_for_claim": "false",
        },
    ]


def finite_input_rows() -> list[dict[str, str]]:
    return [
        {
            "input_id": "FI3386_0_Tgrad",
            "quantity": "T_grad(lambda_PPN)",
            "units": "dimensionless",
            "definition": "T_grad=(ell_s/lambda_PPN) exp[-ell_s^2/(2 lambda_PPN^2)]",
            "current_value": "MISSING_ELL_S_OVER_LAMBDA_PPN",
            "required_source_or_theorem": "sourced smoothing scale ell_s and relevant PPN leakage wavelength lambda_PPN",
            "status": "FORMULA_READY_NUMERIC_RATIO_MISSING",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI3386_1_epsilon_bg",
            "quantity": "epsilon_bg_PPN",
            "units": "dimensionless",
            "definition": "normalized local first-gradient readout amplitude before transfer",
            "current_value": "MISSING_LOCAL_FIRST_GRADIENT_BOUND",
            "required_source_or_theorem": "parent local stationarity theorem or finite gradient norm bound in Solar-system/lab patch",
            "status": "ZERO_NOT_SIGNED_FINITE_INPUT_REQUIRED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI3386_2_epsilon_boundary",
            "quantity": "epsilon_boundary_PPN",
            "units": "dimensionless",
            "definition": "normalized boundary/collar/source-worldtube leakage contribution",
            "current_value": "MISSING_BOUNDARY_LEAKAGE_BOUND",
            "required_source_or_theorem": "compact-collar no-flux theorem or finite source-worldtube boundary coefficient",
            "status": "ZERO_NOT_SIGNED_FINITE_INPUT_REQUIRED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI3386_3_epsilon_kernel_aniso",
            "quantity": "epsilon_kernel_aniso_PPN",
            "units": "dimensionless",
            "definition": "normalized kernel anisotropy / PPN projector commutator leakage",
            "current_value": "MISSING_KERNEL_PROJECTOR_COMMUTATOR_BOUND",
            "required_source_or_theorem": "isotropic parent smoothing projector theorem or finite commutator norm",
            "status": "ZERO_NOT_SIGNED_FINITE_INPUT_REQUIRED",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "input_id": "FI3386_4_epsilon_eff",
            "quantity": "epsilon_eff_PPN",
            "units": "dimensionless",
            "definition": "epsilon_bg_PPN*T_grad + epsilon_boundary_PPN + epsilon_kernel_aniso_PPN",
            "current_value": "MISSING_COMPONENT_VALUES",
            "required_source_or_theorem": "all component values or all three zero theorems",
            "status": "ASSEMBLY_READY_NONCLAIM",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def transfer_samples() -> list[tuple[str, float]]:
    rows = read_csv_rows(OUT / "P8_Y5_R2FR_3321_KERNEL_TRANSFER_LAW.csv")
    samples: list[tuple[str, float]] = []
    for row in rows:
        law_id = row.get("law_id", "")
        if "SAMPLE" not in law_id:
            continue
        formula = row.get("formula", "")
        value = math.nan
        if "=" in formula:
            value = to_float(formula.split("=")[-1].strip())
        if math.isfinite(value):
            samples.append((law_id.replace("KER3321_SAMPLE_", ""), value))
    return samples or [
        ("shorter_than_smoothing", 1.928749847964e-21),
        ("equal_to_smoothing", 6.065306597126e-01),
        ("ten_times_smoothing", 9.950124791927e-02),
        ("million_times_smoothing", 9.999999999995e-07),
    ]


def threshold_backsolve_rows() -> list[dict[str, str]]:
    threshold_sources: list[tuple[str, str, float, float]] = []
    for row in read_csv_rows(OUT / "P8_Y5_R2FR_3385_EPSILON_EFF_THRESHOLDS_NONCLAIM.csv"):
        response = to_float(row.get("A_gamma_times_Cmetric", ""))
        epsilon_max = to_float(row.get("epsilon_eff_max_if_other_floors_zero", ""))
        if math.isfinite(response) and math.isfinite(epsilon_max):
            threshold_sources.append(("FULL_GAMMA_ZERO_FLOORS_3385", row.get("threshold_id", ""), response, epsilon_max))
    for row in read_csv_rows(OUT / "P8_Y5_R2FR_3336_TREE_EPSILON_BOUND_CONTRACT.csv"):
        response = to_float(row.get("A_PPN_times_Cmetric", ""))
        epsilon_max = to_float(row.get("tree_partition_allowance", ""))
        if math.isfinite(response) and math.isfinite(epsilon_max):
            threshold_sources.append(("TREE_PARTITION_3336", row.get("contract_id", ""), response, epsilon_max))

    rows: list[dict[str, str]] = []
    for source_label, source_id, response, epsilon_eff_max in threshold_sources:
        component_equal_budget = epsilon_eff_max / 3.0
        for sample_id, transfer in transfer_samples():
            epsilon_bg_max = component_equal_budget / transfer if transfer > 0 else math.inf
            rows.append(
                {
                    "backsolve_id": f"TB3386_{source_label}_{source_id}_{sample_id}",
                    "threshold_source": source_label,
                    "source_row": source_id,
                    "A_gamma_or_PPN_times_Cmetric": f"{response:.6e}",
                    "epsilon_eff_max": f"{epsilon_eff_max:.15e}",
                    "split_rule": "equal no-cancellation thirds",
                    "T_grad_sample": sample_id,
                    "T_grad_value": f"{transfer:.15e}",
                    "epsilon_bg_max_if_boundary_kernel_get_equal_thirds": f"{epsilon_bg_max:.15e}" if math.isfinite(epsilon_bg_max) else "inf",
                    "epsilon_boundary_max_equal_third": f"{component_equal_budget:.15e}",
                    "epsilon_kernel_aniso_max_equal_third": f"{component_equal_budget:.15e}",
                    "interpretation": "schema/backsolve only; use as target size, not evidence",
                    "valid_for_claim": "false",
                }
            )
    return rows


def runner_rows(parent_silence: list[dict[str, str]], finite_inputs: list[dict[str, str]], backsolve: list[dict[str, str]]) -> list[dict[str, str]]:
    zero_closed = any(row["attempt_id"] == "PS3386_4_verdict" and row["result"] == "ZERO_PROOF_CLOSED" for row in parent_silence)
    missing_inputs = [row for row in finite_inputs if row["current_value"].startswith("MISSING_")]
    return [
        {
            "run_id": "RUN3386_0_zero_attempt",
            "test": "try exact epsilon_eff_PPN=0 theorem",
            "result": "FAIL_CURRENT_ZERO_NOT_PARENT_SIGNED" if not zero_closed else "PASS_ZERO_PARENT_SIGNED",
            "detail": "background, boundary and kernel-anisotropy zero clauses do not close together in the current corpus",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3386_1_component_schema",
            "test": "decompose epsilon_eff into positive no-cancellation components",
            "result": "PASS_SCHEMA",
            "detail": "epsilon_eff = epsilon_bg*T_grad + epsilon_boundary + epsilon_kernel_aniso",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3386_2_finite_inputs",
            "test": "stage finite input rows for all live components",
            "result": "PASS_NONCLAIM_INPUT_ROWS",
            "detail": f"missing_component_values={len(missing_inputs)}",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3386_3_threshold_backsolve",
            "test": "convert Cassini/tree thresholds into component target ceilings",
            "result": "PASS_BACKSOLVE_NONCLAIM",
            "detail": f"rows={len(backsolve)}; equal thirds; transfer samples imported from 3321",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3386_4_firewall",
            "test": "prevent local PPN/local-GR overclaim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "all component and threshold rows are nonclaim until zero theorems or source-backed values exist",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool, parent_silence: list[dict[str, str]], finite_inputs: list[dict[str, str]]) -> list[dict[str, str]]:
    result_map = {row["attempt_id"]: row["result"] for row in parent_silence}
    missing_values = [row["quantity"] for row in finite_inputs if row["current_value"].startswith("MISSING_")]
    return [
        {
            "gate_id": "GATE3386_0_sources",
            "claim": "all 3386 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates 3320/3321/3332/3335/3336/3384/3385 inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3386_1_background_zero",
            "claim": "epsilon_bg_PPN=0 is parent-signed",
            "gate_pass": bool_text(result_map.get("PS3386_1_background_gradient_zero") == "PARENT_SIGNED"),
            "reason": "3320 exact first-gradient silence remains conditional/not signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3386_2_boundary_zero",
            "claim": "epsilon_boundary_PPN=0 is parent-signed",
            "gate_pass": bool_text(result_map.get("PS3386_2_boundary_zero") == "PARENT_SIGNED"),
            "reason": "local collar/source-worldtube boundary silence not yet owned by parent action",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3386_3_kernel_zero",
            "claim": "epsilon_kernel_aniso_PPN=0 is parent-signed",
            "gate_pass": bool_text(result_map.get("PS3386_3_kernel_anisotropy_zero") == "PARENT_SIGNED"),
            "reason": "Gaussian model isotropy exists, but projector commutator zero is not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3386_4_finite_values",
            "claim": "finite component values are sourced",
            "gate_pass": bool_text(not missing_values),
            "reason": "missing=" + ";".join(missing_values),
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3386_5_epsilon_eff",
            "claim": "epsilon_eff_PPN is zero or bounded for local PPN use",
            "gate_pass": "false",
            "reason": "zero proof fails and finite values remain missing; threshold targets only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3386_6_local_ppn",
            "claim": "local PPN gamma/local-GR branch passes",
            "gate_pass": "false",
            "reason": "epsilon_eff is still nonclaim and A_gamma/Cmetric/floors remain live",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(backsolve: list[dict[str, str]]) -> list[dict[str, str]]:
    harsh_rows = [row for row in backsolve if row["A_gamma_or_PPN_times_Cmetric"] in {"1.000000e+12", "1.000000e+16"}]
    return [
        {
            "decision_id": "DEC3386_0_progress",
            "decision": "The epsilon_eff blocker is no longer vague; it is exactly three component channels.",
            "because": "3332/3321 give epsilon_bg*T_grad plus boundary plus kernel-anisotropy, with no cancellation allowed.",
            "next_action": "try to zero boundary and kernel first, then bound background gradient/scale transfer",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3386_1_zero_status",
            "decision": "The exact local-vacuum tree zero is still a conditional theorem, not a current result.",
            "because": "first-gradient, boundary, and kernel commutator silence are each plausible but not signed in one parent branch.",
            "next_action": "do not spend epsilon_eff=0 credit yet",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3386_2_numeric_lesson",
            "decision": "Finite survival is possible only if component amplitudes are tiny under harsh response products.",
            "because": f"3386 produced {len(harsh_rows)} harsh response backsolve target rows from existing Cassini/tree thresholds.",
            "next_action": "use the backsolve rows as target sizes for finite input acquisition",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3386_3_best_route",
            "decision": "Least-scrutiny route is boundary/kernel silence before fitting any epsilon number.",
            "because": "boundary and kernel are structural/gauge/projection questions; if they zero, only epsilon_bg*T_grad remains to bound.",
            "next_action": "attack local-collar boundary silence and PPN-kernel commutator zero together",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3387-Y5-R2FR-boundary-kernel-silence-or-epsilon-component-values-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3387_boundary_kernel_silence_or_epsilon_component_values.py",
            "objective": "try to prove epsilon_boundary_PPN=epsilon_kernel_aniso_PPN=0 from local-collar silence, isotropic smoothing, and PPN projector commutation; if not, fill first finite component bounds",
            "why_next": "3386 shows these are the cleanest structural zeros; closing them reduces epsilon_eff to epsilon_bg*T_grad",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3388-Y5-R2FR-background-gradient-and-Tgrad-scale-bound-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3388_background_gradient_and_Tgrad_scale_bound.py",
            "objective": "derive or source epsilon_bg_PPN and ell_s/lambda_PPN so the remaining background-gradient leakage can be numerically scored",
            "why_next": "needed if boundary/kernel zeros close or remain small enough",
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
        for hit in FW.rglob("*3386*")
        if hit.name.startswith(("3386-Y5", "P8_Y5_R2FR_3386", "P8_Y5_BRR545_3386", "Y5_R2FR_3386"))
    ] if FW.exists() else []
    component_quantities = {row["quantity"] for row in rows_by_name["component_decomposition"]}
    parent_results = {row["result"] for row in rows_by_name["parent_silence"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3386_0_sources_exist_parse", "all cited 3386 source paths exist and parse", source_ok, ""),
        ("VAL3386_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3386_2_decomposition", "epsilon_eff decomposition has bg, boundary, kernel and total rows", {"epsilon_bg_PPN*T_grad(lambda_PPN)", "epsilon_boundary_PPN", "epsilon_kernel_aniso_PPN", "epsilon_eff_PPN"}.issubset(component_quantities), ""),
        ("VAL3386_3_zero_attempt", "zero proof is attempted and not overclaimed", {"CONDITIONAL_THEOREM_ONLY", "ZERO_PROOF_NOT_CLOSED_CURRENTLY"}.issubset(parent_results), ""),
        ("VAL3386_4_finite_inputs", "finite input rows include all live component values and remain missing/nonclaim", len(rows_by_name["finite_inputs"]) == 5 and all(row["valid_for_claim"] == "false" for row in rows_by_name["finite_inputs"]), ""),
        ("VAL3386_5_threshold_backsolve", "threshold backsolve rows exist for transfer samples and response products", len(rows_by_name["threshold_backsolve"]) >= 16, f"rows={len(rows_by_name['threshold_backsolve'])}"),
        ("VAL3386_6_runner", "runner records zero failure, schema pass, finite rows, backsolve, and firewall", {"FAIL_CURRENT_ZERO_NOT_PARENT_SIGNED", "PASS_SCHEMA", "PASS_NONCLAIM_INPUT_ROWS", "PASS_BACKSOLVE_NONCLAIM", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3386_7_gates", "gates block component zeros, finite values, epsilon_eff and local PPN", gate_map.get("GATE3386_1_background_zero") == "false" and gate_map.get("GATE3386_2_boundary_zero") == "false" and gate_map.get("GATE3386_3_kernel_zero") == "false" and gate_map.get("GATE3386_4_finite_values") == "false" and gate_map.get("GATE3386_5_epsilon_eff") == "false" and gate_map.get("GATE3386_6_local_ppn") == "false", ""),
        ("VAL3386_8_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3386_9_next_target", "next target attacks boundary/kernel silence before finite fitting", rows_by_name["next"][0]["target_id"].startswith("3387-Y5-R2FR-boundary-kernel"), ""),
        ("VAL3386_10_write_scope_outside_formalization", "no 3386 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    overall = all(passed for _, _, passed, _ in checks)
    checks.append(("VAL3386_11_overall", "3386 validation overall", overall, "all required checks passed" if overall else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    backsolve_count = len(rows_by_name["threshold_backsolve"])
    lines = [
        "# 3386 - Y5/R2FR epsilon_eff parent silence or first finite inputs under AX1090",
        "",
        "## Summary",
        "- 3386 attacks the actual post-3385 bottleneck: `epsilon_eff_PPN`, the leakage amplitude inside the Cassini-style PPN gamma residual.",
        "- Exact zero route: clean but not closed. `epsilon_eff_PPN=0` follows if background-gradient, boundary, and kernel-anisotropy channels all vanish in the same parent branch.",
        "- Current verdict: those zero clauses are conditional, not parent-signed. No local-GR/PPN claim is allowed from this checkpoint.",
        "- Concrete progress: the vague leakage term is now split into three named component obligations, and finite nonclaim rows are staged for each missing input.",
        f"- Numeric discipline: `{backsolve_count}` threshold backsolve rows translate existing Cassini/tree allowances into target component ceilings under transfer-law samples.",
        "- Best next strike: prove boundary/kernel silence first; if those close, the remaining fight becomes `epsilon_bg_PPN*T_grad(lambda_PPN)`.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## Epsilon Component Decomposition",
        md_table(rows_by_name["component_decomposition"]),
        "## Parent Silence Attempt",
        md_table(rows_by_name["parent_silence"]),
        "## First Finite Input Rows",
        md_table(rows_by_name["finite_inputs"]),
        "## Threshold Backsolve",
        md_table(rows_by_name["threshold_backsolve"]),
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
    parent_silence = parent_silence_rows()
    finite_inputs = finite_input_rows()
    threshold_backsolve = threshold_backsolve_rows()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "component_decomposition": component_decomposition_rows(),
        "parent_silence": parent_silence,
        "finite_inputs": finite_inputs,
        "threshold_backsolve": threshold_backsolve,
        "runner": runner_rows(parent_silence, finite_inputs, threshold_backsolve),
        "gates": gate_rows(source_ok, parent_silence, finite_inputs),
        "decision": decision_rows(threshold_backsolve),
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
