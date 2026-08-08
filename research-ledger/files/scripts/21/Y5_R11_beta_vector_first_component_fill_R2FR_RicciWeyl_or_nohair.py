from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1587"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1587-Y5-R11-beta-vector-first-component-fill-R2FR-RicciWeyl-or-nohair.md"

SOURCE_FILES = {
    "1586_doc": ROOT / "1586-Y5-parent-minimality-no-extra-sector-signature-or-R11-beta-vector-fill.md",
    "1586_validation": OUT / "P8_Y5_BRR545_1586_VALIDATION.csv",
    "1586_fill": OUT / "P8_Y5_PARENT_QLOC_1586_R11_BETA_VECTOR_FILL_REQUIREMENTS.csv",
    "962_r2fr_zero": OUT / "P8_Y5_R10_962_R2FR_ZERO_PROOF_ATTEMPT.csv",
    "963_derivative_audit": OUT / "P8_Y5_R10_963_DERIVATIVE_ORDER_AUDIT.csv",
    "963_coefficient_owner": OUT / "P8_Y5_R10_963_R2FR_COEFFICIENT_OWNER_AUDIT.csv",
    "964_minimality": OUT / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
    "965_curve_manifest": OUT / "P8_Y5_R10_965_R2FR_FULL_CURVE_INTAKE_MANIFEST.csv",
    "440_doc": ROOT / "440-metric-only-second-order-sector-reduction-attempt.md",
    "1193_ricci_doc": ROOT / "1193-Y5-R10-Ricci-exact-scalar-branch-or-vector-tensor-compensator.md",
    "1193_ricci_csv": OUT / "P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
    "local_eh_audit": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
    "r11_beta_vector": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "r11_executable": OUT / "R11_nonEH_operator_vector_executable.csv",
    "local_bounds": LOCAL_BOUNDS / "local_bound_claims.csv",
}

NEEDLES = {
    "1586_doc": ["NEXT_1587_R11_BETA_VECTOR_FIRST_COMPONENT_FILL_R2FR_RICCIWEYL_OR_NOHAIR", "FILL1586_1_delta_beta_R2_fR"],
    "1586_validation": ["VAL1586_OVERALL", "PASS"],
    "1586_fill": ["FILL1586_1_delta_beta_R2_fR", "FILL1586_2_delta_beta_Ricci_Weyl"],
    "962_r2fr_zero": ["R2Z962_5_relative_zero_theorem", "conditional proof of c_R2=c_fR=0"],
    "963_derivative_audit": ["DO963_6_verdict", "NOT_PARENT_SIGNED_CURRENT_CORPUS"],
    "963_coefficient_owner": ["CO963_4_verdict", "NO_EXECUTABLE_OWNER_FOUND"],
    "964_minimality": ["MIN964_5_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
    "965_curve_manifest": ["R2FC965_0_Lee2020_full_curve_required", "R2FC965_3_MTS_R2FR_prediction_required"],
    "440_doc": ["higher_curvature_metric_operators", "central_open"],
    "1193_ricci_doc": ["Ricci-exact scalar branch", "generic local matter/lab domain scalar closure"],
    "1193_ricci_csv": ["RES1193_5_matter_domain_failure", "SCALAR_ROUTE_FAILS_GENERIC_MATTER_DOMAIN"],
    "local_eh_audit": ["R2_fR_scalar_mode", "Ricci_Weyl_squared"],
    "r11_beta_vector": ["B530_1_R2_fR_scalar", "B530_2_Ricci_Weyl"],
    "r11_executable": ["R2_fR_scalar_mode", "Ricci_Weyl_squared"],
    "local_bounds": ["Will_2014_PPN_beta_table", "beta_minus_1", "7.8e-05"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1587_SOURCE_REGISTER.csv"
NOHAIR_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1587_R2FR_RICCIWEYL_NOHAIR_ATTEMPT.csv"
FIRST_COMPONENT_FILL = OUT / "P8_Y5_PARENT_QLOC_1587_FIRST_COMPONENT_FILL_ROWS.csv"
BOUND_INTERFACE = OUT / "P8_Y5_PARENT_QLOC_1587_BOUND_INTERFACE_REQUIREMENTS.csv"
BETA_RUNNER = OUT / "P8_Y5_PARENT_QLOC_1587_BETA_COMPONENT_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1587_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1587_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1587_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1587_VALIDATION.csv"

COPY_TARGETS = {
    NOHAIR_ATTEMPT: [
        QUARANTINE / "R2FR_RICCIWEYL_NOHAIR_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_RicciWeyl_nohair_attempt_nonclaim_1587.csv",
    ],
    FIRST_COMPONENT_FILL: [
        QUARANTINE / "FIRST_COMPONENT_FILL_ROWS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R11_beta_first_component_fill_rows_nonclaim_1587.csv",
    ],
    BOUND_INTERFACE: [
        QUARANTINE / "BOUND_INTERFACE_REQUIREMENTS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_RicciWeyl_bound_interface_nonclaim_1587.csv",
    ],
    BETA_RUNNER: [
        QUARANTINE / "BETA_COMPONENT_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "beta_component_runner_nonclaim_1587.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_RicciWeyl_decision_nonclaim_1587.csv",
    ],
}


def flags() -> dict[str, bool]:
    return {
        "parent_signed": False,
        "numeric_value_present": False,
        "source_backed": False,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1587_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "R11 beta first-component R2/fR and Ricci/Weyl no-hair or fill",
                **flags(),
            }
        )
    return rows


def nohair_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NH1587_0_R2FR_relative_zero",
            "R2/f(R) relative zero theorem",
            "nonlinear f(R) carries a scalar trace pole and violates second-order metric equations unless f_RR=0 under the metric-only/no-extra-scalar parent premises",
            "would set c_R2=c_fR=0 if parent P6/no-extra-scalar/minimality were signed",
            "RELATIVE_THEOREM_AVAILABLE_NOT_ACTIVATED",
            "963/964 keep the parent second-order/minimality activator unsigned",
        ),
        (
            "NH1587_1_integrated_out_scalar",
            "auxiliary scalar tower escape",
            "a hidden scalar with beta phi R and mass M can integrate out to beta^2 R^2/(2M^2)",
            "must be forbidden by parent object-language/no-integrated-out theorem or filled as finite scalar map",
            "COUNTERMODEL_LIVE",
            "no theorem forbids regenerated R2/fR after sector elimination",
        ),
        (
            "NH1587_2_RicciWeyl_topology",
            "Ricci/Weyl curvature-squared safe case",
            "only an exact 4D Gauss-Bonnet/topological combination with harmless boundary flux is locally safe",
            "would remove local bulk variation for the exact topological combination only",
            "MISSING_TOPOLOGICAL_COMBINATION_OR_COEFFICIENTS",
            "generic Ricci^2 and Weyl^2 are not killed by the GB safe case",
        ),
        (
            "NH1587_3_RicciWeyl_spin2",
            "Ricci/Weyl tensor-mode leakage",
            "generic Ricci^2/Weyl^2 terms can introduce quadratic metric slip, preferred-location/tensor response or massive spin-2-like weak-field corrections",
            "requires zero coefficients, decoupling, or a weak-field response map",
            "MISSING_WEAK_FIELD_MAP",
            "no c_Ricci/c_Weyl coefficient, normalization or beta/xi map is sourced",
        ),
        (
            "NH1587_4_Ricci_exact_scalar_branch_limit",
            "Ricci-exact scalar branch is special, not generic",
            "1193 keeps an Einstein/Ricci-flat scalar branch but rejects generic matter Ricci scalar closure",
            "can inform special-domain bounds but not a full local-GR theorem",
            "SPECIAL_BRANCH_ONLY",
            "generic local matter domains still need vector/tensor compensator or source-backed residuals",
        ),
        (
            "NH1587_5_field_redefinition_guard",
            "field redefinition escape",
            "curvature-squared terms cannot be declared harmless unless matter/source/readout/boundary equivalence is preserved",
            "would permit coefficient demotion only with observable-equivalence certificate",
            "NOT_CERTIFIED",
            "readout and source-normalization leakage could move instead of vanish",
        ),
        (
            "NH1587_6_verdict",
            "R2/fR and Ricci/Weyl theorem-zero",
            "NH1587_0 through NH1587_5 all parent-signed or explicitly bounded",
            "would close the first R11 beta-vector components",
            "FAIL_CURRENT_CLAIM_FIRST_COMPONENTS_NOT_DERIVED",
            "first components remain fill rows, not theorem-zero",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "nohair_id": nohair_id,
            "target": target,
            "statement": statement,
            "effect_if_signed": effect_if_signed,
            "status": status,
            "blocking_gap": blocking_gap,
            **flags(),
        }
        for nohair_id, target, statement, effect_if_signed, status, blocking_gap in rows
    ]


def first_component_fill_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "FC1587_0_R2FR",
            "B530_1_R2_fR_scalar",
            "R2_fR_scalar_mode",
            "delta_beta_R2_fR",
            "c_R2_or_c_fR",
            "length^2_or_inverse_mass_squared_after_EH_normalization",
            "c_R2/c_fR, f_RR, scalaron mass m_s or lambda_s, scalar coupling alpha_s, screening flag, branch context, source path",
            "gamma,beta,alpha(lambda) scalar-mode residual map",
            "MISSING_PARENT_COEFFICIENT_AND_FULL_CURVE",
            "Lee2020_full_curve_target;Will_beta;Cassini_gamma",
        ),
        (
            "FC1587_1_RicciWeyl",
            "B530_2_Ricci_Weyl",
            "Ricci_Weyl_squared",
            "delta_beta_Ricci_Weyl",
            "c_Ricci_or_c_Weyl",
            "length^2_or_cutoff_power_after_EH_normalization",
            "c_Ricci, c_Weyl, topological decomposition, massive tensor/slip response, boundary flux policy, source path",
            "quadratic metric slip/location/tensor response map into beta,gamma,xi and R11",
            "MISSING_COEFFICIENT_AND_WEAK_FIELD_MAP",
            "Will_beta;Cassini_gamma;preferred_location_xi_bound_if_mapped",
        ),
        (
            "FC1587_2_GaussBonnet_safe_case",
            "B530_2_Ricci_Weyl",
            "boundary_topological_combination",
            "delta_beta_Ricci_Weyl_topological_part",
            "c_GB",
            "topological_or_boundary_normalized",
            "exact 4D GB combination, boundary/corner no-flux certificate, no local stress/readout hair",
            "topological safe subtraction only, not generic Ricci/Weyl silence",
            "CONDITIONAL_SAFE_CASE_NOT_CURRENT_ROW",
            "boundary_alpha3_xi_Gdot_locks_if_boundary_not_silent",
        ),
        (
            "FC1587_3_field_redefinition_equivalence",
            "B530_1_R2_fR_scalar;B530_2_Ricci_Weyl",
            "field_redefinition_escape",
            "delta_beta_curvature_squared_equivalence",
            "Delta_redef",
            "dimensionless_equivalence_error",
            "matter/source/readout/boundary equivalence proof or finite residual after redefinition",
            "prevents moving curvature leakage into matter constants or observed readout",
            "MISSING_REDEFINITION_EQUIVALENCE_CERTIFICATE",
            "WEP;clock;gamma;beta;source_normalization",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "fill_id": fill_id,
            "source_component_id": source_component_id,
            "operator_family": operator_family,
            "component": component,
            "coefficient_symbol": coefficient_symbol,
            "required_units": required_units,
            "required_real_input": required_real_input,
            "weak_field_map": weak_field_map,
            "current_status": current_status,
            "bound_interfaces": bound_interfaces,
            "no_cancellation_target": "abs(component) contributes to Delta_beta_total_abs <= 7.8e-05",
            **flags(),
        }
        for fill_id, source_component_id, operator_family, component, coefficient_symbol, required_units, required_real_input, weak_field_map, current_status, bound_interfaces in rows
    ]


def bound_interface_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BI1587_0_R2FR_R10_curve",
            "R2_fR_scalar_mode",
            "R10 alpha(lambda) bound curve",
            "full digitized positive lambda/alpha bound curve plus MTS scalar mass/coupling prediction",
            "Lee2020 full curve target exists in 965, but no full curve and no MTS prediction are present",
            "MISSING_FULL_CURVE_AND_PREDICTION",
        ),
        (
            "BI1587_1_R2FR_PPN",
            "R2_fR_scalar_mode",
            "PPN gamma/beta branch",
            "scalar range/regime map and gamma/beta prediction after measured-GM normalization",
            "Cassini/Will bounds exist, but scalar regime and prediction are missing",
            "MISSING_PPN_PROJECTION",
        ),
        (
            "BI1587_2_RicciWeyl_PPN",
            "Ricci_Weyl_squared",
            "PPN beta/gamma/xi map",
            "weak-field map from c_Ricci/c_Weyl to beta, gamma, preferred-location or tensor response",
            "no coefficient, units, normalization or observable response matrix exists",
            "MISSING_WEAK_FIELD_RESPONSE",
        ),
        (
            "BI1587_3_GB_boundary",
            "boundary_topological_combination",
            "boundary/local flux locks",
            "proof exact GB/topological term has zero local boundary/corner/readout flux or finite alpha3/xi/Gdot map",
            "topological safe case is conditional; boundary harmlessness is not parent-signed",
            "MISSING_BOUNDARY_NOFLUX",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": interface_id,
            "operator_family": operator_family,
            "interface": interface,
            "required_inputs": required_inputs,
            "current_evidence": current_evidence,
            "status": status,
            **flags(),
        }
        for interface_id, operator_family, interface, required_inputs, current_evidence, status in rows
    ]


def beta_runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1587_0_R2FR_zero", "set delta_beta_R2_fR=0", "REFUSE_UNSIGNED_ZERO_THEOREM", "relative theorem exists but parent second-order/no-extra-scalar signature is not signed"),
        ("RUN1587_1_R2FR_R10_score", "score finite R2/fR scalar branch against R10 curve", "NOT_RUN_COMPONENTS_MISSING", "no MTS scalar prediction and no full digitized curve are present"),
        ("RUN1587_2_RicciWeyl_zero", "set delta_beta_Ricci_Weyl=0", "REFUSE_UNSIGNED_ZERO_THEOREM", "no coefficient-zero, topological-combination or weak-field map is sourced"),
        ("RUN1587_3_partial_beta_sum", "compute partial Delta_beta_abs for first components", "NOT_RUN_COMPONENTS_MISSING", "both first components are missing-valued nonclaims"),
        ("RUN1587_4_GB_shortcut", "use Gauss-Bonnet safe case to clear Ricci/Weyl row", "REFUSE_OVERBROAD_TOPOLOGY", "exact topological combination and boundary no-flux are not current rows"),
        ("RUN1587_5_local_gr", "claim local GR reduction from first components", "BLOCKED_NO_CLAIM", "even these first components are not closed, and other beta/source/matter/conservation gates remain open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": False,
            **flags(),
        }
        for runner_id, case, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1587_0_R2FR_zero", "R2/fR beta component theorem-zero", "BLOCKED_NO_CLAIM", "parent second-order/no-extra-scalar/minimality activator is unsigned"),
        ("GATE1587_1_R2FR_score", "finite R2/fR scalar branch score", "BLOCKED_NO_CLAIM", "coefficient, scalar mass/coupling and full bound curve are missing"),
        ("GATE1587_2_RicciWeyl_zero", "Ricci/Weyl beta component theorem-zero", "BLOCKED_NO_CLAIM", "coefficient-zero/topological/weak-field response proof is missing"),
        ("GATE1587_3_first_component_beta", "first R11 beta components below lock", "BLOCKED_NO_CLAIM", "partial beta sum cannot run with missing components"),
        ("GATE1587_4_local_gr", "derived local GR branch", "BLOCKED_NO_CLAIM", "R11, source, common matter, conservation and full beta envelope remain open"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1587_0_R2FR_result",
            "R2FR_RELATIVE_THEOREM_NOT_ACTIVATED",
            "R2/fR zero is mathematically clean under metric-only second-order no-extra-scalar premises, but those premises remain unsigned",
            "do not claim delta_beta_R2_fR=0",
        ),
        (
            "DEC1587_1_RicciWeyl_result",
            "RICCIWEYL_ZERO_NOT_DERIVED",
            "generic Ricci/Weyl curvature-squared leakage is not topological unless coefficients/combinations/boundaries are sourced",
            "keep delta_beta_Ricci_Weyl as a fill row",
        ),
        (
            "DEC1587_2_practical_route",
            "R2FR_SCALARON_COEFFICIENT_OR_FULL_CURVE_IS_FIRST_FILL",
            "R2/fR already has a relative theorem, scalaron map and R10 curve target, making it the most fillable first component",
            "try parent coefficient/mass-coupling extraction first, then full-curve acquisition",
        ),
        (
            "DEC1587_3_next",
            "NEXT_1588_R2FR_SCALARON_COEFFICIENT_MAP_OR_FULL_CURVE_BOUND_INTAKE",
            "the next checkpoint should either source c_R2/fRR -> m_s,lambda_s,alpha_s or acquire the full bound curve needed for nonclaim scoring",
            "derive coefficient/mass/coupling first; if missing, build strict acquisition ledger",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1588-Y5-R2FR-scalaron-coefficient-map-or-full-curve-bound-intake.md",
            "script": "scripts/Y5_R2FR_scalaron_coefficient_map_or_full_curve_bound_intake.py",
            "objective": "try to extract c_R2/fRR, scalaron mass/range, coupling and screening from the parent branch; if not, acquire/source the full R10 alpha(lambda) bound curve for a strict nonclaim scalar branch runner",
            "do_not": "do not use Lee/Kapner anchor-only rows, relative zero theorem, or EH reference family as a beta/R10 pass",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1587_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1587" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    nohair = read_csv(NOHAIR_ATTEMPT)
    fills = read_csv(FIRST_COMPONENT_FILL)
    interfaces = read_csv(BOUND_INTERFACE)
    runner = read_csv(BETA_RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_components = {"delta_beta_R2_fR", "delta_beta_Ricci_Weyl", "delta_beta_Ricci_Weyl_topological_part", "delta_beta_curvature_squared_equivalence"}
    required_claims = {
        "R2/fR beta component theorem-zero",
        "finite R2/fR scalar branch score",
        "Ricci/Weyl beta component theorem-zero",
        "first R11 beta components below lock",
        "derived local GR branch",
    }
    checks = [
        ("VAL1587_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1587 source paths exist"),
        ("VAL1587_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1587 source needles found"),
        (
            "VAL1587_2_nohair_fails_open",
            any(row["nohair_id"] == "NH1587_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_FIRST_COMPONENTS_NOT_DERIVED" for row in nohair),
            "R2/fR and Ricci/Weyl no-hair attempt is explicit but not promoted",
        ),
        (
            "VAL1587_3_fill_rows_schema",
            {row["component"] for row in fills} == required_components
            and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in fills),
            "first component fill rows are present and nonclaim",
        ),
        (
            "VAL1587_4_bound_interfaces_blocked",
            all(row["status"].startswith("MISSING") for row in interfaces),
            "bound/observable interfaces remain missing rather than scored",
        ),
        (
            "VAL1587_5_runner_blocks",
            all(row["can_score"] == "False" for row in runner)
            and any(row["runner_id"] == "RUN1587_5_local_gr" and row["status"] == "BLOCKED_NO_CLAIM" for row in runner),
            "runner blocks zero shortcuts, finite scoring and local GR",
        ),
        (
            "VAL1587_6_claim_gates_closed",
            {row["claim"] for row in gates} == required_claims
            and all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates),
            "all 1587 claim gates remain closed",
        ),
        (
            "VAL1587_7_decision_next",
            any(row["decision"] == "NEXT_1588_R2FR_SCALARON_COEFFICIENT_MAP_OR_FULL_CURVE_BOUND_INTAKE" for row in decisions),
            "decision selects R2/fR scalaron coefficient map or full curve intake",
        ),
        ("VAL1587_8_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1587 CSVs parse cleanly"),
        ("VAL1587_9_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1587_10_no_raw_accepted", not has_1587_rows(RAB_RAW) and not has_1587_rows(RAB_ACCEPTED), "no 1587 rows written to raw/accepted finite directories"),
        ("VAL1587_11_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1587_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1587_13_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1587 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1587_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1587 R11 beta first-component R2/fR and Ricci/Weyl validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    nohair: list[dict[str, Any]],
    fills: list[dict[str, Any]],
    interfaces: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1587 - R11 Beta Vector First Component Fill: R2/fR, Ricci/Weyl Or No-Hair",
                "## Verdict\n"
                "- The R2/f(R) zero route is mathematically clean only as a relative theorem: if the parent branch is metric-only, second-order and no-extra-scalar, then `c_R2=c_fR=0`; current MTS has not signed those activators.\n"
                "- Ricci/Weyl leakage is not killed by saying Gauss-Bonnet: only the exact topological combination with boundary harmlessness is safe, while generic Ricci^2/Weyl^2 needs coefficients and weak-field maps.\n"
                "- The first R11 beta components are now fill rows, not theorem-zero rows: `delta_beta_R2_fR`, `delta_beta_Ricci_Weyl`, the topological safe-case boundary part, and field-redefinition equivalence.\n"
                "- No beta score runs yet because coefficient values, units, normalization, scalar/tensor response maps, and bound interfaces are missing.\n"
                "- No beta, EH, Newton, PPN, local-GR, R10, WEP, clock, orbital, conservation or common-matter claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## R2/fR and Ricci/Weyl No-Hair Attempt",
                md_table(nohair, ["nohair_id", "target", "statement", "effect_if_signed", "status", "blocking_gap"]),
                "## First Component Fill Rows",
                md_table(fills, ["fill_id", "operator_family", "component", "coefficient_symbol", "required_units", "current_status", "bound_interfaces"]),
                "## Bound Interface Requirements",
                md_table(interfaces, ["interface_id", "operator_family", "interface", "required_inputs", "current_evidence", "status"]),
                "## Beta Component Runner",
                md_table(runner, ["runner_id", "case", "status", "reason", "can_score"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    nohair = nohair_attempt_rows()
    fills = first_component_fill_rows()
    interfaces = bound_interface_rows()
    runner = beta_runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        NOHAIR_ATTEMPT,
        FIRST_COMPONENT_FILL,
        BOUND_INTERFACE,
        BETA_RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(NOHAIR_ATTEMPT, nohair)
    write_csv(FIRST_COMPONENT_FILL, fills)
    write_csv(BOUND_INTERFACE, interfaces)
    write_csv(BETA_RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, nohair, fills, interfaces, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
