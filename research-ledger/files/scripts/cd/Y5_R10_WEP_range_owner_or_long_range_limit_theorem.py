from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1085-Y5-R10-WEP-range-owner-or-long-range-limit-theorem.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1085-WEP-range-owner-or-long-range-limit" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1085_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1085_WEP_BOUND_IMPORT.csv"

EARTH_RADIUS_M = 6_371_000.0
ORBIT_ALTITUDE_M = 710_000.0
ETA_BOUND = 2.8e-15
HBAR_C_EV_M = 1.973269804e-7


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1085_0_1084_next", "source-intake/mts_residuals/P8_Y5_R10_1084_NEXT_TARGET.csv", "1085-Y5-R10-WEP-range-owner-or-long-range-limit-theorem.md", "1084 handoff."),
        ("SRC1085_1_1084_validation", "source-intake/mts_residuals/P8_Y5_BRR545_1084_VALIDATION.csv", "V1084_SUMMARY", "1084 validation summary."),
        ("SRC1085_2_1084_kernel", "source-intake/mts_residuals/P8_Y5_R10_1084_SOURCE_PROFILE_KERNEL_DERIVATION_LEDGER.csv", "K1084_2_long_range_limit", "source-profile kernel and long-range condition."),
        ("SRC1085_3_1084_profile_grid", "source-intake/mts_residuals/P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv", "PROFILE1084_lambda_over_RE_1", "lambda-dependent profile grid."),
        ("SRC1085_4_1084_profile_gates", "source-intake/mts_residuals/P8_Y5_R10_1084_PROFILE_CLOSURE_GATES.csv", "PCG1084_0_long_range_bulk_limit", "bulk long-range gate."),
        ("SRC1085_5_1084_readout", "source-intake/mts_residuals/P8_Y5_R10_1084_MICROSCOPE_READOUT_IMPORT_GATE.csv", "RIG1084_0_CMSM_arrays", "official readout import gate."),
        ("SRC1085_6_1025_second_variation", "source-intake/mts_residuals/P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv", "SV1025_3_range_relation", "lambda_X=sqrt(Z_X/M_X^2) relation."),
        ("SRC1085_7_1025_hessian_audit", "source-intake/mts_residuals/P8_Y5_R10_1025_PARENT_HESSIAN_AUDIT.csv", "PHA1025_8_verdict", "parent Hessian ownership failed."),
        ("SRC1085_8_1026_metric_attempt", "source-intake/mts_residuals/P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv", "PM1026_0_metric_target", "parent field-space metric missing."),
        ("SRC1085_9_1037_no_pole", "source-intake/mts_residuals/P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv", "no-pole", "no-pole route audit."),
        ("SRC1085_10_1038_omega", "source-intake/mts_residuals/P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv", "ODC1038_8_verdict", "Omega/DCX no-pole certificate failed."),
        ("SRC1085_11_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle_found = exists and needle.lower() in text.lower()
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def web_source_rows() -> list[dict[str, str]]:
    return [
        {
            "web_source_id": "WEB1085_0_YUKAWA_PROFILE_KERNEL",
            "role": "finite-range profile-kernel reference inherited from 1084",
            "source_url": "https://arxiv.org/pdf/2507.02723",
            "source_title": "The Yukawa potential of a non-homogeneous sphere, with new limits on an ultralight boson",
            "evidence_used": "spherical finite-range profile kernel and long-range internal-structure limit",
            "status": "REFERENCE_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1085_1_MICROSCOPE_FINAL_BOUND",
            "role": "WEP bound source",
            "source_url": "https://arxiv.org/abs/2209.15487",
            "source_title": "MICROSCOPE mission: final results of the test of the Equivalence Principle",
            "evidence_used": "eta(Ti,Pt) source-backed bound inherited from local_bound_claims.csv",
            "status": "BOUND_SOURCE_ONLY_PREDICTION_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "web_source_id": "WEB1085_2_MICROSCOPE_ORBIT",
            "role": "Earth-source readout distance context",
            "source_url": "https://comptes-rendus.academie-sciences.fr/physique/item/10.5802/crphys.24.pdf",
            "source_title": "The MICROSCOPE space mission to test the Equivalence Principle",
            "evidence_used": "710 km orbit altitude context inherited from 1084",
            "status": "ORBIT_CONTEXT_ONLY_NONCLAIM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def range_owner_theorem_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "ROW1085_0_exact_range_relation",
            "branch": "massive scalar-like residual",
            "statement": "lambda_WEP = lambda_X = sqrt(Z_X/M_X^2) after canonicalizing O_X=-nabla_i(Z_X nabla^i)+M_X^2",
            "current_evidence": "SV1025_3_range_relation derives the relation but not parent-owned Z_X/M_X^2 values or units",
            "result": "RELATION_DERIVED_VALUES_MISSING",
            "missing_for_claim": "same-branch Z_X, M_X^2, units, source current, and boundary/readout convention",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "ROW1085_1_no_pole_escape",
            "branch": "no physical X pole / quotient branch",
            "statement": "if X is pure quotient/gauge before variation, lambda_WEP is absent and finite source profile disappears",
            "current_evidence": "1037/1038 sharpen but fail the no-pole certificate because Omega/DCX/vertical/boundary/matter descent objects are missing",
            "result": "NO_POLE_NOT_CLOSED",
            "missing_for_claim": "parent Omega, DC_X, all-field v_X, Q_X/K_boundary, degree count, matter descent",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "ROW1085_2_massless_long_range",
            "branch": "massless/common long-range carrier",
            "statement": "M_X^2=0 or protected massless source carrier gives lambda_WEP=infinity and bulk source vector is profile-safe",
            "current_evidence": "no parent Ward/symmetry theorem sets M_X^2=0 while keeping a controlled WEP coupling",
            "result": "LONG_RANGE_THEOREM_NOT_SIGNED",
            "missing_for_claim": "symmetry protecting zero mass plus source/readout normalization and no fifth-force contradiction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "ROW1085_3_short_range_residual",
            "branch": "finite short-range residual",
            "statement": "finite lambda_WEP requires the 1084 profile kernel, orbit attenuation, PREM/shell profile, and official readout",
            "current_evidence": "1084 profile grid shows source vector changes with lambda; readout arrays remain missing",
            "result": "FINITE_PROFILE_BRANCH_RETAINED",
            "missing_for_claim": "lambda_WEP owner, PREM/composition shell profile, official MICROSCOPE readout, parent-to-DD map",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "ROW1085_4_verdict",
            "branch": "1085 range owner",
            "statement": "MTS currently proves lambda_WEP >> R_E or lambda_WEP=infinity",
            "current_evidence": "range relation exists only as a contract; no-pole and massless routes are unsigned",
            "result": "RANGE_OWNER_NOT_DERIVED",
            "missing_for_claim": "parent-owned range theorem or sourced finite-range profile/readout branch",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def range_threshold_rows() -> list[dict[str, str]]:
    ratios = [1, 3, 10, 30, 100, 1000]
    rows: list[dict[str, str]] = []
    for ratio in ratios:
        lambda_m = ratio * EARTH_RADIUS_M
        mass_eV = HBAR_C_EV_M / lambda_m
        rows.append(
            {
                "threshold_id": f"LRT1085_lambda_over_RE_{ratio}",
                "lambda_over_R_E": f"{ratio:.6g}",
                "lambda_m": f"{lambda_m:.15e}",
                "equivalent_m_X_eV_if_relativistic": f"{mass_eV:.15e}",
                "static_operator_condition": f"M_X^2/Z_X <= 1/({ratio} R_E)^2",
                "bulk_vector_status": "profile_sensitive" if ratio < 10 else "bulk_limit_candidate_nonclaim",
                "claim_condition": "parent must derive this lower bound on lambda_WEP; empirical fit cannot choose it after the fact",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def profile_influence_rows() -> list[dict[str, str]]:
    grid = read_csv(OUT / "P8_Y5_R10_1084_SOURCE_PROFILE_WEIGHTING_GRID_NONCLAIM.csv")
    long_range = grid[0]
    long_alpha = float(long_range["Q_alpha_Coulomb_eff"])
    long_surface = float(long_range["Q_surface_binding_eff"])
    rows: list[dict[str, str]] = []
    for row in grid:
        if row["lambda_over_R_E"] == "inf":
            lambda_ratio = "inf"
            attenuation = 1.0
        else:
            ratio = float(row["lambda_over_R_E"])
            lambda_m = ratio * EARTH_RADIUS_M
            lambda_ratio = f"{ratio:.15e}"
            attenuation = pow(2.718281828459045, -ORBIT_ALTITUDE_M / lambda_m)
        alpha = float(row["Q_alpha_Coulomb_eff"])
        surface = float(row["Q_surface_binding_eff"])
        delta_alpha = alpha - long_alpha
        delta_surface = surface - long_surface
        rows.append(
            {
                "influence_id": "INF1085_" + row["lambda_label"],
                "lambda_label": row["lambda_label"],
                "lambda_over_R_E": lambda_ratio,
                "delta_alpha_vs_two_layer_long_range": f"{delta_alpha:.15e}",
                "delta_surface_vs_two_layer_long_range": f"{delta_surface:.15e}",
                "max_abs_profile_shift": f"{max(abs(delta_alpha), abs(delta_surface)):.15e}",
                "surface_orbit_attenuation_exp_minus_h_over_lambda": f"{attenuation:.15e}",
                "interpretation": "bulk_limit" if row["lambda_over_R_E"] in {"inf"} or (row["lambda_over_R_E"] != "inf" and float(row["lambda_over_R_E"]) >= 10) else "finite_profile_live",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def r10_wep_consistency_rows() -> list[dict[str, str]]:
    return [
        {
            "consistency_id": "RWC1085_0_same_lambda_object",
            "claim": "R10 lambda_X and WEP lambda_WEP are the same parent range",
            "current_status": "NOT_PARENT_SIGNED",
            "implication_if_true": "short-range R10 candidates cannot simultaneously justify bulk Earth WEP source vector; long-range WEP candidates must face long-range fifth-force/WEP constraints",
            "required_evidence": "single parent kinetic/mass operator and arena projection showing the same lambda in both observables",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consistency_id": "RWC1085_1_independent_lambdas",
            "claim": "R10 lambda and WEP lambda are independent",
            "current_status": "FORBIDDEN_UNLESS_PARENT_SPLITS_FIELDS",
            "implication_if_true": "requires two distinct fields/operators, otherwise range choice is post hoc",
            "required_evidence": "field decomposition with separate Z/M blocks and separate source/readout maps",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consistency_id": "RWC1085_2_bulk_shortcut",
            "claim": "use 1083 bulk Earth vector without lambda theorem",
            "current_status": "REJECTED",
            "implication_if_true": "would hide the finite-range source-profile dependence found in 1084",
            "required_evidence": "lambda_WEP >> R_E or source common-mode/no-pole theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "consistency_id": "RWC1085_3_r10_pressure",
            "claim": "R10 bound curve can score this branch now",
            "current_status": "REJECTED",
            "implication_if_true": "would require alpha(lambda), K_X(lambda), Qbar_XH(lambda), qbar_XT, and real bound curve in one convention",
            "required_evidence": "the 1033/1034/R10 projection stack plus parent range owner",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def range_acquisition_schema_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_id": "RAS1085_0_parent_operator",
            "needed_object": "O_X=-nabla_i(Z_X nabla^i)+M_X^2",
            "required_columns": "branch_id;field_id;Z_X;M_X2;Z_units;M_units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_HESSIAN_VALUES",
            "claim_blocker": "lambda cannot be owned without same-branch Z_X and M_X^2",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "schema_id": "RAS1085_1_long_range_certificate",
            "needed_object": "lambda_WEP lower bound or zero-mass theorem",
            "required_columns": "branch_id;lambda_lower_bound_m;mass_upper_bound_eV;theorem_or_source;source_path;valid_for_claim",
            "current_status": "MISSING_LONG_RANGE_THEOREM",
            "claim_blocker": "bulk Earth source vector remains conditional",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "schema_id": "RAS1085_2_finite_profile",
            "needed_object": "finite lambda source-profile branch",
            "required_columns": "branch_id;lambda_m;rho_profile;composition_profile;Q_eff_alpha;Q_eff_surface;source_path;valid_for_claim",
            "current_status": "MISSING_PREM_AND_LAMBDA_OWNER",
            "claim_blocker": "1084 two-layer grid is smoke only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "schema_id": "RAS1085_3_readout_product",
            "needed_object": "MICROSCOPE readout normalization",
            "required_columns": "segment;time;gx;gz;Sxx;Sxz;masks;K_MICROSCOPE;eta_normalization;source_path;valid_for_claim",
            "current_status": "OFFICIAL_ARRAYS_NOT_IMPORTED",
            "claim_blocker": "source profile alone is not a reported Eotvos prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "schema_id": "RAS1085_4_parent_to_DD_map",
            "needed_object": "C_parent -> (c_alpha,c_surface)",
            "required_columns": "branch_id;C_parent;c_alpha;c_surface;units;sign;source_path;valid_for_claim",
            "current_status": "PARENT_TO_DD_MAP_NOT_DERIVED",
            "claim_blocker": "DD source vector remains external comparator",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1085_0_range_owner_missing",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_LAMBDA_WEP_RANGE_OWNER_PARENT_TO_DD_MAP_AND_OFFICIAL_READOUT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1085_RANGE_OWNER_THEOREM_ATTEMPT.csv",
            "inputs_present": "1084 source-profile kernel; 1025 range relation; MICROSCOPE bound",
            "required_inputs": "parent-owned lambda_WEP or no-pole theorem; parent-to-DD coefficient map; official MICROSCOPE readout",
            "derivation_status": "RANGE_RELATION_KNOWN_BUT_RANGE_OWNER_MISSING",
            "valid_for_claim": "false",
            "notes": "runner must refuse; this checkpoint only decides the logical range gate",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1085_0_MICROSCOPE_WEP_source_charge",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": f"{ETA_BOUND:.15e}",
            "bound_units": "dimensionless",
            "bound_source": "https://arxiv.org/abs/2209.15487",
            "source_row": "MICROSCOPE_final_TiPt_source_charge_proxy:R1_WEP_source_charge;doi:10.1103/PhysRevLett.129.121102",
            "bound_type": "upper_abs_WEP_proxy_bound",
            "valid_for_claim": "true",
            "notes": "source-backed numeric bound only; MTS prediction remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1085_0_range_owner_product_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "passed_rows": str(product_status.get("passed_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing lambda_WEP range owner, parent-to-DD map, and official readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1085_0_range_owner",
            "claim_component": "lambda_WEP owned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "ROW1085_4_verdict=RANGE_OWNER_NOT_DERIVED",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1085_1_bulk_vector",
            "claim_component": "bulk Earth vector is physical source vector",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "requires lambda_WEP >> R_E, no-pole, or common-mode theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1085_2_R10_WEP_same_range",
            "claim_component": "R10/WEP range consistency",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "same-lambda or split-field branch not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1085_3_parent_to_DD_map",
            "claim_component": "DD source vector is MTS source vector",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "parent-to-DD coefficient map remains missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1085_4_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": "false",
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DECISION1085_0",
            "decision": "long-range bulk shortcut is not available yet",
            "because": "lambda_WEP >> R_E is a theorem condition, not a data-fitting convenience, and current parent files only provide the lambda relation",
            "next_action": "attack parent source-current/coupling zero or fill the finite-profile/readout inputs",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DECISION1085_1",
            "decision": "range and amplitude cannot be chosen independently",
            "because": "the same parent operator must own lambda_X, K_X, Qbar_XH, qbar_XT, and the DD coefficient map",
            "next_action": "return to the coupling/source-current owner before scoring WEP",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1085_0_1086",
            "next_target": "1086-Y5-R10-WEP-source-current-zero-or-parent-DD-map-first-row.md",
            "objective": "try the derivation-first route for WEP: prove the parent source/test composition current vanishes or map the first parent coefficient into the DD alpha/surface basis; if neither closes, retain finite-profile/readout acquisition",
            "include": "J_X/qbar_XT source-current zero attempt; C_parent to DD coefficient map; same-branch normalization; no-pole/common-mode alternatives; nonclaim fallback rows",
            "exclude": "measured-G absorption; fitted lambda choice; unit source proxy; DD smoke as MTS claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    web_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    threshold_rows: list[dict[str, str]],
    influence_rows: list[dict[str, str]],
    consistency_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1085_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited local source paths and needles are present"))
    checks.append(("V1085_1_web_sources_recorded", len(web_rows) == 3 and all(row["source_url"].startswith("https://") and row["valid_for_claim"] == "false" for row in web_rows), "web source urls/provenance are recorded as nonclaim"))
    checks.append(("V1085_2_range_theorem_attempt_complete", any(row["attempt_id"] == "ROW1085_4_verdict" and row["result"] == "RANGE_OWNER_NOT_DERIVED" for row in theorem_rows), "range-owner attempt ends in explicit nonclaim verdict"))
    checks.append(("V1085_3_thresholds_numeric", len(threshold_rows) == 6 and all(parse_float(row["lambda_m"]) is not None and parse_float(row["equivalent_m_X_eV_if_relativistic"]) is not None for row in threshold_rows), "lambda and mass-equivalent thresholds are numeric"))
    checks.append(("V1085_4_profile_influence_numeric", len(influence_rows) >= 7 and all(parse_float(row["max_abs_profile_shift"]) is not None for row in influence_rows), "profile influence rows are numeric"))
    checks.append(("V1085_5_R10_WEP_consistency_blocks_shortcuts", len(consistency_rows) == 4 and all(row["valid_for_claim"] == "false" for row in consistency_rows), "R10/WEP lambda consistency shortcuts are blocked"))
    checks.append(("V1085_6_acquisition_schema_nonclaim", len(schema_rows) == 5 and all(row["valid_for_claim"] == "false" for row in schema_rows), "range/profile/readout acquisition schema remains nonclaim"))
    checks.append(("V1085_7_prediction_missing_nonclaim", any("MISSING_LAMBDA_WEP" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "generic prediction row remains missing range owner inputs"))
    checks.append(("V1085_8_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1085_9_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1085_10_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1085_11_next_target", any(row["next_target"].startswith("1086-Y5-R10-WEP-source-current") for row in next_rows), "1086 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1085_12_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1085_13_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1085 CSV outputs parse cleanly"))
    checks.append(("V1085_14_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1085_SUMMARY", True, "range-owner theorem not derived; bulk Earth shortcut remains conditional; finite profile/readout/coupling gates remain live"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    web_rows: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    threshold_rows: list[dict[str, str]],
    influence_rows: list[dict[str, str]],
    consistency_rows: list[dict[str, str]],
    schema_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1085-Y5-R10 WEP range owner or long-range limit theorem",
            "",
            "## Current verdict",
            "1085 does not prove the long-range shortcut. The exact range relation already exists, lambda_X=sqrt(Z_X/M_X^2), and 1084 proves that the bulk Earth source vector is safe only in the long-range limit. But the current parent stack still does not own Z_X, M_X^2, a zero-mass/no-pole theorem, a parent-to-DD map, or the official MICROSCOPE readout. So the honest result is: lambda_WEP is still a missing parent input, and finite-profile/readout/coupling gates remain live.",
            "",
            "## Local source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Web source register",
            md_table(web_rows, ["web_source_id", "role", "source_url", "status"]),
            "## Range-owner theorem attempt",
            md_table(theorem_rows, ["attempt_id", "branch", "statement", "result", "missing_for_claim"]),
            "## Long-range thresholds",
            md_table(threshold_rows, ["threshold_id", "lambda_over_R_E", "lambda_m", "equivalent_m_X_eV_if_relativistic", "static_operator_condition", "bulk_vector_status"]),
            "## Profile influence readout",
            md_table(influence_rows, ["influence_id", "lambda_over_R_E", "delta_alpha_vs_two_layer_long_range", "delta_surface_vs_two_layer_long_range", "max_abs_profile_shift", "surface_orbit_attenuation_exp_minus_h_over_lambda", "interpretation"]),
            "## R10-WEP consistency ledger",
            md_table(consistency_rows, ["consistency_id", "claim", "current_status", "implication_if_true", "required_evidence"]),
            "## Range acquisition schema",
            md_table(schema_rows, ["schema_id", "needed_object", "current_status", "claim_blocker"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    web_rows = web_source_rows()
    theorem_rows = range_owner_theorem_attempt_rows()
    threshold_rows = range_threshold_rows()
    influence_rows = profile_influence_rows()
    consistency_rows = r10_wep_consistency_rows()
    schema_rows = range_acquisition_schema_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1085_SOURCE_REGISTER.csv",
        "web_source_register": OUT / "P8_Y5_R10_1085_WEB_SOURCE_REGISTER.csv",
        "theorem_attempt": OUT / "P8_Y5_R10_1085_RANGE_OWNER_THEOREM_ATTEMPT.csv",
        "long_range_thresholds": OUT / "P8_Y5_R10_1085_LONG_RANGE_THRESHOLD_TABLE.csv",
        "profile_influence": OUT / "P8_Y5_R10_1085_PROFILE_INFLUENCE_READOUT.csv",
        "r10_wep_consistency": OUT / "P8_Y5_R10_1085_R10_WEP_RANGE_CONSISTENCY_LEDGER.csv",
        "acquisition_schema": OUT / "P8_Y5_R10_1085_RANGE_ACQUISITION_SCHEMA.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1085_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1085_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1085_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1085_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1085_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1085_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["web_source_register"], web_rows)
    write_csv(outputs["theorem_attempt"], theorem_rows)
    write_csv(outputs["long_range_thresholds"], threshold_rows)
    write_csv(outputs["profile_influence"], influence_rows)
    write_csv(outputs["r10_wep_consistency"], consistency_rows)
    write_csv(outputs["acquisition_schema"], schema_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        web_rows,
        theorem_rows,
        threshold_rows,
        influence_rows,
        consistency_rows,
        schema_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        web_rows,
        theorem_rows,
        threshold_rows,
        influence_rows,
        consistency_rows,
        schema_rows,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
