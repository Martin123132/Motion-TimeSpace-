from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3482-Y5-R2FR-earth-source-amplitude-SEq-current-bound-or-zero-theorem.md"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]
DD_KEYS = ["Q_hatm_full", "Q_delta_m", "Q_m_e", "Q_e_full"]

SOURCES: dict[str, dict[str, Any]] = {
    "script_3482": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3481": {
        "path": ROOT / "3481-Y5-R2FR-source-current-Jq-theorem-or-first-transport-normalizer-row.md",
        "role": "3481 handoff",
    },
    "wep_norm_3481": {
        "path": OUT / "P8_Y5_R2FR_3481_WEP_SHARED_EARTH_NORMALIZER_ROWS_NONCLAIM.csv",
        "role": "shared WEP normalizer rows",
    },
    "wep_collapse_3481": {
        "path": OUT / "P8_Y5_R2FR_3481_WEP_COLLAPSED_BOUND_FACTORS.csv",
        "role": "WEP collapsed bounds containing abs_S_Eq_inv",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "full-rank row matrix",
    },
    "earth_composition_2789": {
        "path": OUT / "P8_Y5_R2FR_2789_BULK_EARTH_COMPOSITION_TARGET.csv",
        "role": "bulk Earth composition proxy",
    },
    "dd_formula_3472": {
        "path": OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_FORMULA_AUDIT.csv",
        "role": "full DD four-charge formula audit",
    },
    "dd_source_proxy_2789": {
        "path": OUT / "P8_Y5_R2FR_2789_DD_EARTH_SOURCE_VECTOR_FIRST_ROW_NONCLAIM.csv",
        "role": "older two-component DD Earth source proxy",
    },
    "source_caveat_2789": {
        "path": OUT / "P8_Y5_R2FR_2789_SOURCE_VECTOR_CAVEAT_GATE.csv",
        "role": "Earth source vector caveat gates",
    },
    "source_leg_2444": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2444_SOURCE_LEG_DERIVATION_CONTRACT.csv",
        "role": "S_Eq contract",
    },
    "jq_attempt_2445": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2445_JQ_SOURCE_CURRENT_EXTRACTION_ATTEMPT.csv",
        "role": "J_q extraction attempt",
    },
    "residual_pack_2446": {
        "path": OUT / "P8_Y5_PARENT_QLOC_2446_MTS_RESIDUAL_CURRENT_PACK_FOR_S_EQ.csv",
        "role": "S_Eq residual current pack",
    },
    "source_norm_stack": {
        "path": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
        "role": "source normalization theorem stack",
    },
    "source_zero_targets": {
        "path": OUT / "P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv",
        "role": "source normalization zero targets",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", "<br>").replace("|", "/") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def norm(values: list[float]) -> float:
    return math.sqrt(sum(value * value for value in values))


def normalize(values: list[float]) -> list[float]:
    value = norm(values)
    if value <= 0:
        raise ValueError("zero vector")
    return [entry / value for entry in values]


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def dd_charges(A: float, Z: float) -> dict[str, float]:
    q_p = Z / A
    q_delta = (A - 2.0 * Z) / A
    q_c = Z * (Z - 1.0) / (A ** (4.0 / 3.0))
    return {
        "Q_hatm_full": 0.093 - 0.036 / (A ** (1.0 / 3.0)) - 0.020 * (q_delta**2) - 1.4e-4 * q_c,
        "Q_delta_m": 0.0017 * q_delta,
        "Q_m_e": 5.5e-4 * q_p,
        "Q_e_full": (-1.4 + 8.2 * q_p + 7.7 * q_c) * 1.0e-4,
    }


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "source_id": source_id,
            "source_path": str(meta["path"]),
            "exists": meta["path"].exists(),
            "role": meta["role"],
            "valid_for_claim": False,
        }
        for source_id, meta in SOURCES.items()
    ]


def earth_element_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCES["earth_composition_2789"]["path"]):
        charges = dd_charges(float(row["A"]), float(row["Z"]))
        weight = float(row["normalized_mass_fraction"])
        output: dict[str, Any] = {
            "element_charge_id": f"EARTH3482_{row['element']}",
            "element": row["element"],
            "normalized_mass_fraction": f"{weight:.15e}",
            "A": row["A"],
            "Z": row["Z"],
            "source_table": row["source_table"],
            "status": "FULL_DD_FOUR_CHARGE_EARTH_ELEMENT_PROXY_NONCLAIM",
            "valid_for_claim": False,
        }
        for key, value in charges.items():
            output[key] = f"{value:.15e}"
            output[f"weighted_{key}"] = f"{weight * value:.15e}"
        rows.append(output)
    return rows


def earth_source_vector_rows(element_rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[float]]:
    vector = [sum(float(row[f"weighted_{key}"]) for row in element_rows) for key in DD_KEYS]
    vector_norm = norm(vector)
    mass_fraction_sum = sum(float(row["normalized_mass_fraction"]) for row in element_rows)
    rows = [
        {
            "source_vector_id": "EARTH3482_0_bulk_full_DD_four_charge",
            "source_body": "Earth",
            "basis": "full_Damour_Donoghue_four_charge_proxy",
            "Q_hatm_full_Earth": f"{vector[0]:.15e}",
            "Q_delta_m_Earth": f"{vector[1]:.15e}",
            "Q_m_e_Earth": f"{vector[2]:.15e}",
            "Q_e_full_Earth": f"{vector[3]:.15e}",
            "source_vector_norm": f"{vector_norm:.15e}",
            "unit_Q_hatm_full_Earth": f"{vector[0] / vector_norm:.15e}",
            "unit_Q_delta_m_Earth": f"{vector[1] / vector_norm:.15e}",
            "unit_Q_m_e_Earth": f"{vector[2] / vector_norm:.15e}",
            "unit_Q_e_full_Earth": f"{vector[3] / vector_norm:.15e}",
            "normalized_mass_fraction_sum": f"{mass_fraction_sum:.15e}",
            "source_rows": str(SOURCES["earth_composition_2789"]["path"]),
            "formula_source_path": str(SOURCES["dd_formula_3472"]["path"]),
            "claim_status": "NUMERIC_BULK_EARTH_DD_SOURCE_VECTOR_NONCLAIM_PARENT_MAP_MISSING",
            "valid_for_claim": False,
        }
    ]
    return rows, vector


def wep_unit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCES["matrix_3475"]["path"]):
        if row["bound_units"] != "dimensionless_eta":
            continue
        raw = [
            float(row["raw_D_hatm_eff"]),
            float(row["raw_D_delta_m_eff"]),
            float(row["raw_D_me_eff"]),
            float(row["raw_D_e_eff"]),
        ]
        rows.append(
            {
                "aug_row_id": row["aug_row_id"],
                "arena": row["arena"],
                "raw_norm": norm(raw),
                "unit": normalize(raw),
                "eta_bound": float(row["bound"]),
            }
        )
    return rows


def source_geometry_rows(earth_vector: list[float]) -> list[dict[str, Any]]:
    earth_norm = norm(earth_vector)
    earth_unit = normalize(earth_vector)
    rows: list[dict[str, Any]] = []
    for row in wep_unit_rows():
        cosine = dot(earth_unit, row["unit"])
        rows.append(
            {
                "geometry_id": f"SG3482_{row['aug_row_id']}",
                "row_id": row["aug_row_id"],
                "arena": row["arena"],
                "earth_vector_norm": f"{earth_norm:.12e}",
                "test_delta_norm": f"{row['raw_norm']:.12e}",
                "source_test_unit_cosine": f"{cosine:.12e}",
                "same_vector_quadratic_form": f"eta ~= ({earth_norm:.6e} e_hat·C) * ({row['raw_norm']:.6e} u_AB·C)",
                "meaning": "if S_Eq=Q_Earth·C, this WEP row is quadratic in C, not a linear row with an external source amplitude",
                "valid_for_claim": False,
            }
        )
    return rows


def branch_logic_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "BR3482_0_external_transport_amplitude",
            "assumption": "S_Eq is a parent-owned source transport amplitude independent of the visible coefficient vector C",
            "math_form": "eta_AB = S_Eq (DeltaQ_AB · C)",
            "what_3481_buys": "N_AB=|S_Eq|^-1/||DeltaQ_AB|| and 3480 linear inverse can be used if |S_Eq| has a lower bound",
            "needed_for_claim": "derive S_Eq != 0 lower bound or a sourced normalization value from J_q/H_tau",
            "status": "CONDITIONAL_BRANCH_ONLY",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BR3482_1_same_visible_vector_DD",
            "assumption": "S_Eq is the Earth body coupling built from the same visible vector C",
            "math_form": "S_Eq = Q_Earth · C, so eta_AB = (Q_Earth · C)(DeltaQ_AB · C)",
            "what_3481_buys": "the row-norm factors remain useful, but the WEP rows are quadratic constraints, not independent linear rank rows",
            "needed_for_claim": "solve/score the mixed quadratic WEP plus linear clock system or prove Q_Earth·C=0/source silence",
            "status": "MORE_PHYSICAL_DD_BRANCH_REQUIRES_NONLINEAR_RUNNER",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BR3482_2_zero_source_current",
            "assumption": "J_q^A=0 or projects to S_Eq=0 in the local compact Earth source",
            "math_form": "S_Eq=0 => eta_AB source product vanishes",
            "what_3481_buys": "WEP source channel would be locally silent, but WEP no longer bounds C_i through that source",
            "needed_for_claim": "parent-sign all residual-current zero families and prevent readout reentry",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "OBS3482_0_lower_bound_obstruction",
            "statement": "A WEP upper bound on |S_Eq Y_AB| cannot give an upper bound on |Y_AB| or |C_i| without a lower bound on |S_Eq|.",
            "proof": "For any measured bound B and any candidate Y_AB, choosing sufficiently small nonzero |S_Eq| keeps |S_Eq Y_AB| <= B.",
            "consequence": "3481 coefficient envelopes containing abs_S_Eq_inv are not empirical coefficient bounds until |S_Eq| >= L_E > 0 is derived.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OBS3482_1_upper_bound_different_use",
            "statement": "An upper bound on |S_Eq| helps prove a small WEP product for assumed C_i priors, but it cannot isolate C_i.",
            "proof": "The inequality |S_Eq Y| <= U_E |Y| is product-side, not inverse-side.",
            "consequence": "source-current no-hair can support local-silence/product closure, while coefficient extraction needs source lower bound or clock-only routes.",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OBS3482_2_same_vector_quadratic_guard",
            "statement": "If S_Eq=Q_Earth·C, WEP constraints are quadratic in C and must not be used as independent linear rows in the 3475 rank matrix.",
            "proof": "Substitution gives eta_AB=(Q_Earth·C)(DeltaQ_AB·C), a product of two linear forms.",
            "consequence": "future runner must branch: external-amplitude linear inverse, or DD same-vector nonlinear score.",
            "valid_for_claim": False,
        },
    ]


def residual_reduction_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(SOURCES["residual_pack_2446"]["path"]):
        if row["residual_id"].endswith("_verdict"):
            continue
        rows.append(
            {
                "reduction_id": f"SRR3482_{row['residual_id']}",
                "residual_id": row["residual_id"],
                "source_current_piece": row["residual_current_piece"],
                "feeds_S_Eq_through": row["feeds_S_Eq_through"],
                "current_status": row["current_status"],
                "required_zero_or_bound": row["required_zero_or_bound"],
                "bound_role": "contributes to U_E upper/product-silence bound; lower-bound use requires sign/nonzero source theorem",
                "priority": priority_for_residual(row["residual_id"]),
                "valid_for_claim": False,
            }
        )
    return rows


def priority_for_residual(residual_id: str) -> str:
    if residual_id.endswith("_3_matter_source_glue"):
        return "P0_direct_WEP_source_current"
    if residual_id.endswith("_4_coupling_constant"):
        return "P0_Newton_G_source_normalization"
    if residual_id.endswith("_6_EM_clock_mass_coupling_guard"):
        return "P1_visible_coefficient_reentry"
    if residual_id.endswith("_2_projector_domain"):
        return "P1_PiM_projector_source_lock"
    return "P2_supporting_source_residual"


def source_ready_rows(earth_vector: list[float]) -> list[dict[str, Any]]:
    earth_norm = norm(earth_vector)
    return [
        {
            "row_id": "SEQ3482_0_abs_S_Eq_lower_bound",
            "quantity": "L_E <= |S_Eq|",
            "needed_for": "turn 3481 WEP coefficient envelopes into empirical upper bounds on C_i",
            "candidate_value": "MISSING_LOWER_BOUND_OR_PARENT_NONZERO_THEOREM",
            "units": "dimensionless_source_amplitude",
            "available_proxy": f"bulk full-DD Earth charge norm = {earth_norm:.12e}",
            "why_proxy_not_claim": "DD proxy is not parent MTS transport; if same-vector, source amplitude is Q_Earth·C and can vanish by direction",
            "valid_for_claim": False,
        },
        {
            "row_id": "SEQ3482_1_abs_S_Eq_upper_bound",
            "quantity": "|S_Eq| <= U_E",
            "needed_for": "product-silence/local-GR source-current suppression branch",
            "candidate_value": "MISSING_UPPER_BOUND_OR_ZERO_THEOREM",
            "units": "dimensionless_source_amplitude",
            "available_proxy": "residual families named in 2446 and source-normalization channels in 657",
            "why_proxy_not_claim": "families are not numerically bounded or zero-derived",
            "valid_for_claim": False,
        },
        {
            "row_id": "SEQ3482_2_same_vector_runner_input",
            "quantity": "Q_Earth_full_DD_vector",
            "needed_for": "nonlinear WEP runner eta=(Q_Earth·C)(DeltaQ·C)",
            "candidate_value": "SEE_P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv",
            "units": "dimensionless_DD_charge_proxy",
            "available_proxy": "source-backed bulk Earth composition plus DD four-charge formulas",
            "why_proxy_not_claim": "bulk/profile/worldtube weighting and MTS-to-DD coefficient map remain missing",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(earth_vector: list[float], residual_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3482_0_full_dd_earth_vector",
            "requirement": "bulk Earth full DD four-charge proxy is finite and nonzero",
            "passed": norm(earth_vector) > 0 and all(math.isfinite(value) for value in earth_vector),
            "evidence": f"norm={norm(earth_vector):.12e}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3482_1_external_source_lower_bound",
            "requirement": "derive |S_Eq| >= L_E > 0 for linear inverse WEP coefficient bound",
            "passed": False,
            "evidence": "no parent lower-bound/nonzero theorem; only proxy source vector",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3482_2_same_vector_guard",
            "requirement": "if S_Eq=Q_Earth·C, WEP rows are marked quadratic not linear",
            "passed": True,
            "evidence": "BR3482_1 and OBS3482_2 written",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3482_3_residual_family_reduction",
            "requirement": "S_Eq reduced to named residual current families",
            "passed": len(residual_rows) >= 7,
            "evidence": f"families={len(residual_rows)}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3482_4_no_claim",
            "requirement": "no WEP/local-GR/Newton/source-coupling pass claimed",
            "passed": True,
            "evidence": "all generated rows valid_for_claim=false",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3482_0_branch_split",
            "decision": "The WEP source throat must split into external-amplitude linear branch and same-visible-vector quadratic branch.",
            "rationale": "if S_Eq is Q_Earth·C, WEP constraints are quadratic and cannot be used as independent linear rank rows.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3482_1_dd_proxy_value",
            "decision": "A full-DD bulk Earth source vector can be built, but it is a nonclaim comparator, not parent MTS S_Eq.",
            "rationale": "bulk composition/profile/worldtube weighting and MTS-to-DD coefficient map are missing.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3482_2_best_next_attack",
            "decision": "Build the nonlinear WEP same-vector runner while carrying clock rows separately, then compare with the external-amplitude branch.",
            "rationale": "this tests the physically natural DD structure without smuggling a source lower bound.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3483-Y5-R2FR-quadratic-DD-WEP-source-runner-or-external-SEq-lower-bound.md",
            "next_script": "scripts/Y5_R2FR_3483_quadratic_DD_WEP_source_runner_or_external_SEq_lower_bound.py",
            "objective": "Implement the same-vector nonlinear WEP branch eta=(Q_Earth·C)(DeltaQ·C), keep clock rows linear/product-only, and compare it against the external S_Eq branch without using S_Eq=1.",
            "success_gate": "WEP rows are no longer accidentally treated as independent linear rows when the Earth source is the same visible coefficient vector",
            "exclude": "local-GR claim; GitHub; formalization-workbench edits; setting source amplitude to unity; ignoring clock transport",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def csv_outputs() -> dict[str, Path]:
    return {
        "source_register": OUT / "P8_Y5_R2FR_3482_SOURCE_REGISTER.csv",
        "earth_elements": OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_ELEMENT_ROWS_NONCLAIM.csv",
        "earth_vector": OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv",
        "source_geometry": OUT / "P8_Y5_R2FR_3482_SOURCE_TEST_GEOMETRY.csv",
        "branch_logic": OUT / "P8_Y5_R2FR_3482_SEQ_BRANCH_LOGIC.csv",
        "obstructions": OUT / "P8_Y5_R2FR_3482_SEQ_BOUND_OBSTRUCTION_THEOREMS.csv",
        "residual_reduction": OUT / "P8_Y5_R2FR_3482_SEQ_RESIDUAL_FAMILY_REDUCTION.csv",
        "source_ready": OUT / "P8_Y5_R2FR_3482_ABS_SEQ_SOURCE_READY_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3482_CLAIM_GATES.csv",
        "decision": OUT / "P8_Y5_R2FR_3482_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R2FR_3482_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3482_VALIDATION.csv",
    }


def git_formalization_status() -> str:
    if not (FORMALIZATION / ".git").exists():
        return "NOT_A_GIT_REPOSITORY"
    try:
        result = subprocess.run(
            ["git", "-C", str(FORMALIZATION), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return "GIT_NOT_AVAILABLE"
    if result.returncode != 0:
        return f"GIT_STATUS_FAILED:{result.stderr.strip()}"
    return result.stdout.strip() or "CLEAN"


def validation_rows(
    outputs: dict[str, Path],
    rows_by_output: dict[str, list[dict[str, Any]]],
    earth_vector: list[float],
) -> list[dict[str, Any]]:
    validation: list[dict[str, Any]] = []
    source_rows = source_register()
    validation.append(
        {
            "check_id": "VAL3482_0_sources_exist",
            "passed": all(parse_bool(row["exists"]) for row in source_rows),
            "detail": "all local sources exist",
            "valid_for_claim": False,
        }
    )
    parsed_ok = True
    parse_detail: list[str] = []
    for name, path in outputs.items():
        if name == "validation" and not path.exists():
            parse_detail.append("validation:pending")
            continue
        try:
            parsed = read_csv(path)
            parse_detail.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parsed_ok = False
            parse_detail.append(f"{name}:{type(exc).__name__}")
    validation.append(
        {
            "check_id": "VAL3482_1_csv_parse",
            "passed": parsed_ok,
            "detail": "; ".join(parse_detail),
            "valid_for_claim": False,
        }
    )
    mass_sum = sum(float(row["normalized_mass_fraction"]) for row in rows_by_output["earth_elements"])
    validation.append(
        {
            "check_id": "VAL3482_2_earth_mass_fraction",
            "passed": abs(mass_sum - 1.0) < 1e-12,
            "detail": f"sum={mass_sum:.15e}",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3482_3_earth_vector_nonzero",
            "passed": norm(earth_vector) > 0 and all(math.isfinite(value) for value in earth_vector),
            "detail": f"norm={norm(earth_vector):.12e}",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3482_4_branch_split_present",
            "passed": len(rows_by_output["branch_logic"]) == 3,
            "detail": f"branches={len(rows_by_output['branch_logic'])}",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3482_5_quadratic_guard_present",
            "passed": any(row["theorem_id"] == "OBS3482_2_same_vector_quadratic_guard" for row in rows_by_output["obstructions"]),
            "detail": "same-vector WEP quadratic guard written",
            "valid_for_claim": False,
        }
    )
    validation.append(
        {
            "check_id": "VAL3482_6_residual_reduction",
            "passed": len(rows_by_output["residual_reduction"]) >= 7,
            "detail": f"families={len(rows_by_output['residual_reduction'])}",
            "valid_for_claim": False,
        }
    )
    all_rows: list[dict[str, Any]] = []
    for rows in rows_by_output.values():
        all_rows.extend(rows)
    no_claim = all(not parse_bool(row.get("valid_for_claim", False)) for row in all_rows)
    validation.append(
        {
            "check_id": "VAL3482_7_no_claim",
            "passed": no_claim,
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": False,
        }
    )
    no_formalization_output = all(not str(path).startswith(str(FORMALIZATION)) for path in outputs.values())
    validation.append(
        {
            "check_id": "VAL3482_8_no_formalization_outputs",
            "passed": no_formalization_output,
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": False,
        }
    )
    formalization_status = git_formalization_status()
    validation.append(
        {
            "check_id": "VAL3482_9_git_formalization_clean",
            "passed": formalization_status in {"CLEAN", "NOT_A_GIT_REPOSITORY"},
            "detail": formalization_status,
            "valid_for_claim": False,
        }
    )
    passed = all(parse_bool(row["passed"]) for row in validation)
    validation.append(
        {
            "check_id": "VAL3482_SUMMARY",
            "passed": passed,
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": False,
        }
    )
    return validation


def write_doc(rows_by_output: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 3482: Earth Source Amplitude `S_Eq` Current Bound Or Zero Theorem

## Current Verdict
- **Main correction:** `S_Eq` has two distinct meanings that must not be merged.
- **External-amplitude branch:** if a parent transport theorem gives an independent nonzero `S_Eq`, then the 3481 linear inverse envelope is usable after a lower bound.
- **Same-vector branch:** if `S_Eq = Q_Earth · C`, WEP becomes `eta_AB=(Q_Earth·C)(DeltaQ_AB·C)`, so the WEP rows are quadratic, not independent linear rows.
- **Concrete progress:** built a full four-channel bulk Earth DD proxy vector for the same visible basis, but kept it nonclaim because the parent MTS-to-DD/source-profile map is missing.

## Earth Full DD Element Rows
{md_table(rows_by_output["earth_elements"])}

## Earth Full DD Source Vector
{md_table(rows_by_output["earth_vector"])}

## Source/Test Geometry
{md_table(rows_by_output["source_geometry"])}

## `S_Eq` Branch Logic
{md_table(rows_by_output["branch_logic"])}

## Bound Obstruction Theorems
{md_table(rows_by_output["obstructions"])}

## Residual Family Reduction
{md_table(rows_by_output["residual_reduction"])}

## `abs_S_Eq` Source-Ready Rows
{md_table(rows_by_output["source_ready"])}

## Claim Gates
{md_table(rows_by_output["claim_gates"])}

## Decision
{md_table(rows_by_output["decision"])}

## Next Target
{md_table(rows_by_output["next"])}

## Source Register
{md_table(rows_by_output["source_register"])}

## Validation
{md_table(rows_by_output["validation"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs = csv_outputs()
    element_output = earth_element_rows()
    earth_vector_rows, earth_vector = earth_source_vector_rows(element_output)
    residual_rows = residual_reduction_rows()
    rows_by_output: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "earth_elements": element_output,
        "earth_vector": earth_vector_rows,
        "source_geometry": source_geometry_rows(earth_vector),
        "branch_logic": branch_logic_rows(),
        "obstructions": obstruction_rows(),
        "residual_reduction": residual_rows,
        "source_ready": source_ready_rows(earth_vector),
        "claim_gates": claim_gate_rows(earth_vector, residual_rows),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(outputs[key], rows)
    validation = validation_rows(outputs, rows_by_output, earth_vector)
    rows_by_output["validation"] = validation
    write_csv(outputs["validation"], validation)
    write_doc(rows_by_output)


if __name__ == "__main__":
    main()
