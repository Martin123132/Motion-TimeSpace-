from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1920"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1920-Y5-R2FR-source-weight-parent-current-owner-or-delta-w-first-rows.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1919_next": OUT / "P8_Y5_PARENT_QLOC_1919_NEXT_TARGET.csv",
    "1919_doc": ROOT / "1919-Y5-R2FR-readout-tau-parent-descent-or-source-kernel-first-row.md",
    "1915_priority": OUT / "P8_Y5_PARENT_QLOC_1915_RESIDUAL_PRIORITY_MATRIX_NONCLAIM.csv",
    "1914_vector": OUT / "P8_Y5_PARENT_QLOC_1914_FINITE_RESIDUAL_VECTOR_V0_NONCLAIM.csv",
    "1913_typing": OUT / "P8_Y5_PARENT_QLOC_1913_Q_FUNCTOR_TYPING_MATRIX_NONCLAIM.csv",
    "1913_parent": OUT / "P8_Y5_PARENT_QLOC_1913_PARENT_ACTION_Q_FUNCTOR_CONSTRUCTION_ATTEMPT.csv",
    "1912_axioms": OUT / "P8_Y5_PARENT_QLOC_1912_MINIMAL_AXIOM_DEBT_LEDGER_NONCLAIM.csv",
    "1915_no_cancellation": OUT / "P8_Y5_PARENT_QLOC_1915_NO_CANCELLATION_FIRST_FILL_DRYRUN.csv",
}

NEEDLES = {
    "1919_next": ["NEXT1919_0_primary", "source_weight_residual"],
    "1919_doc": ["NEXT1919_0_primary", "VAL1919_OVERALL"],
    "1915_priority": ["source_weight_residual", "COUPLING_PRESSURE_HIGH_BUT_PARENT_CURRENT_OWNER_UNSIGNED"],
    "1914_vector": ["FRV1914_source_weight_residual", "MISSING_ARENA_KERNELS"],
    "1913_typing": ["QTM1913_6_measure_current", "MISSING_AXIOM_NOT_ADOPTED"],
    "1913_parent": ["PAQ1913_4_minimality_guard", "PAQ1913_5_verdict"],
    "1912_axioms": ["AX1912_4_no_species_source_weights", "AX1912_5_common_measure_current"],
    "1915_no_cancellation": ["DFF1915_2_cancellation_fit", "REFUSE_CANCELLATION_WITHOUT_PARENT_IDENTITY"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1920_SOURCE_REGISTER.csv",
    "proof_attempt": OUT / "P8_Y5_PARENT_QLOC_1920_SOURCE_WEIGHT_PARENT_CURRENT_PROOF_ATTEMPT.csv",
    "delta_rows": OUT / "P8_Y5_PARENT_QLOC_1920_DELTA_W_FIRST_ROWS_NONCLAIM.csv",
    "guard": OUT / "P8_Y5_PARENT_QLOC_1920_SOURCE_WEIGHT_NO_ABSORPTION_GUARD.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1920_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1920_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1920_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1920_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1920_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["proof_attempt"], SOURCE_WEIGHT_DOCS / "SOURCE_WEIGHT_PARENT_CURRENT_OWNER_PROOF_1920_NONCLAIM.csv"),
    (OUTPUTS["delta_rows"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1920_DELTA_W_FIRST_ROWS_NONCLAIM.csv"),
    (OUTPUTS["delta_rows"], QUEUE / "JR1920_SOURCE_WEIGHT_DELTA_W_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1920_CLAIM_GATE.csv"),
]


def ensure_dirs() -> None:
    for path in [OUT, SOURCE_WEIGHT_DOCS, MICROSCOPE_COEFFS, QUEUE, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in NEEDLES[key] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1920 source-weight parent current owner or Delta w first rows",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def proof_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": "SWP1920_0_target",
            "claim_piece": "parent common-current/no-source-weight theorem",
            "formal_statement": "All ordinary source weights w_A and source-label multipliers are either forbidden by the parent operator domain or descend to one species-blind current/measure before variation.",
            "current_status": "TARGET_SHARP",
            "source_anchor": "NEXT1919_0_primary; FRV1914_source_weight_residual",
            "what_fails": "not a failure row; establishes the theorem target",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "SWP1920_1_no_species_source_weights",
            "claim_piece": "no w_A/source-label slot before variation",
            "formal_statement": "No material marker, source-only multiplier, species Jacobian, or pre-action w_A(X)S_A slot exists in the parent action.",
            "current_status": "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
            "source_anchor": "AX1912_4_no_species_source_weights",
            "what_fails": "this is identified as the strongest WEP countermodel and is not parent-forbidden yet",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "SWP1920_2_common_measure_current",
            "claim_piece": "single species-blind measure/current owner",
            "formal_statement": "One action measure/current normalization applies to all ordinary sectors before field equations and classical normalization.",
            "current_status": "MISSING_AXIOM_NOT_ADOPTED",
            "source_anchor": "AX1912_5_common_measure_current; QTM1913_6_measure_current",
            "what_fails": "relative action/source weights can survive classical EOM normalization",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "SWP1920_3_no_hidden_hom",
            "claim_piece": "hidden-to-visible coefficient exclusion",
            "formal_statement": "Hidden or representative variables cannot map into visible matter coefficients except through q_obs or fixed data.",
            "current_status": "MISSING_AXIOM_NOT_ADOPTED",
            "source_anchor": "QTM1913_5_no_hidden_hom",
            "what_fails": "source weights remain live alongside f_X F^2, m_A(X), and frame coefficients",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "SWP1920_4_minimality_guard",
            "claim_piece": "minimal syntax is not derivation",
            "formal_statement": "Writing w_A=1 into a candidate action does not prove w_A is illegal unless the parent operator domain forbids the slot.",
            "current_status": "ADOPTION_GUARD_ACTIVE",
            "source_anchor": "PAQ1913_4_minimality_guard",
            "what_fails": "minimality can hide exactly the coupling degree of freedom being tested",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "SWP1920_5_verdict",
            "claim_piece": "1920 source-weight verdict",
            "formal_statement": "The source_weight_residual is not zero-derived in the current corpus; finite Delta w_A rows must be retained until a parent common-current/no-weight theorem is signed.",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS_DELTA_W_ROWS_STAGED",
            "source_anchor": "SWP1920_1_no_species_source_weights through SWP1920_4_minimality_guard",
            "what_fails": "source-weight exclusion, common-current ownership, and hidden-hom exclusion are unsigned",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def delta_rows() -> list[dict[str, Any]]:
    specs = [
        ("DWA1920_0_WEP_TiPt", "WEP_MICROSCOPE_TiPt", "Delta w_TiPt", "MISSING_DIFFERENTIAL_SOURCE_WEIGHT", "test_material_pair;w_Ti;w_Pt;composition_model;uncertainty;source_path"),
        ("DWA1920_1_R10", "R10_short_range", "Delta w_R10_source_test", "MISSING_SOURCE_TEST_WEIGHT_VECTOR", "source_body;test_body;w_source;w_test;lambda_range;profile;uncertainty;source_path"),
        ("DWA1920_2_PPN", "PPN_beta_gamma_source", "Delta w_PPN_source", "MISSING_PPN_SOURCE_WEIGHT", "source_body;stress_trace_convention;w_source;metric_readout;uncertainty;source_path"),
        ("DWA1920_3_orbital", "orbital_GM_inverse_square", "Delta w_orbital_source", "MISSING_ORBITAL_SOURCE_WEIGHT", "source_body;GM_calibration_rule;w_source;support_profile;uncertainty;source_path"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, arena, symbol, value, columns in specs:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "residual_component": "source_weight_residual",
                "arena": arena,
                "symbol": symbol,
                "candidate_value": value,
                "units": "dimensionless_or_declared",
                "source_path": "MISSING_PARENT_OR_EXPERIMENTAL_SOURCE_WEIGHT_SOURCE",
                "source_row_id": "MISSING_SOURCE_ROW_ID",
                "required_columns": columns,
                "parent_requirements": "no_species_source_weights; common_measure_current; material_source_map; no_calibration_hiding",
                "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def guard_rows() -> list[dict[str, Any]]:
    guards = [
        ("SWG1920_0_mass_absorption", "absorb Delta w_A into inertial/gravitational mass labels", "FORBIDDEN_WITHOUT_PARENT_COMMON_MODE_IDENTITY"),
        ("SWG1920_1_GM_absorption", "absorb source weight into measured GM or orbital ephemeris calibration", "FORBIDDEN_FOR_LOCAL_CLAIM"),
        ("SWG1920_2_Qbar_absorption", "fold source weights into Qbar_XH without a separate row", "FORBIDDEN_FOR_R10_SCORING"),
        ("SWG1920_3_tau_absorption", "move source weights into tau/readout kernels after 1919 boxed them", "FORBIDDEN_CROSS_RESIDUAL_HIDE"),
        ("SWG1920_4_covariance_shortcut", "claim covariance or minimality excludes source weights", "FORBIDDEN_AS_DERIVATION"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "forbidden_move": move,
            "policy": policy,
            "reason": "source weights are a live coupling degree of freedom until the parent current/measure owner forbids them",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for guard_id, move, policy in guards
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1920_0_parent_current_owner",
            "requirement": "source/species weights parent-forbidden by common-current theorem",
            "status": "FAIL_NOT_PARENT_SIGNED",
            "evidence": "SWP1920_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1920_1_delta_w_rows",
            "requirement": "Delta w_A rows sourced with units, priors, and arena kernels",
            "status": "FAIL_ROWS_SCHEMA_ONLY",
            "evidence": "DWA1920_0_WEP_TiPt through DWA1920_3_orbital",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1920_2_absorption_guard",
            "requirement": "no mass/GM/Qbar/tau/covariance hiding",
            "status": "PASS_GUARD_ONLY",
            "evidence": "SWG1920_0_mass_absorption through SWG1920_4_covariance_shortcut",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1920_3_local_claim",
            "requirement": "source_weight_residual supports local claim",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1920_0_parent_current_owner; CG1920_1_delta_w_rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1920_0_derivation_result",
            "decision": "SOURCE_WEIGHT_ZERO_NOT_DERIVED",
            "why": "no species/source-weight slot and common-current ownership remain unsigned",
            "next_action": "retain Delta w_A as finite residual rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1920_1_delta_rows",
            "decision": "DELTA_W_ROWS_STAGED_NONCLAIM",
            "why": "four local arenas now have explicit source-weight row schemas",
            "next_action": "do not score until source paths and numeric/derived values replace all MISSING markers",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1920_2_next_residual",
            "decision": "MOVE_TO_CONSTANT_SECTOR_RESIDUAL",
            "why": "constant_sector is rank 4 and controls mass, charge, alpha, and clocks after the coupling-weight route is boxed",
            "next_action": "1921 should try constant-sector superselection or stage alpha/mass/clock coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1920_0_primary",
            "selection_status": "selected",
            "target_doc": "1921-Y5-R2FR-constant-sector-superselection-or-alpha-mass-clock-first-rows.md",
            "target_script": "scripts/Y5_R2FR_constant_sector_superselection_or_alpha_mass_clock_first_rows_1921.py",
            "objective": "attack constant_sector_residual: prove mass/charge/alpha/clock constants are fixed superselection data, or stage first alpha/mass/clock finite rows as nonclaim",
            "success_condition": "constant_sector_residual gets a parent theorem-zero source path, finite source-ready coefficient rows, or closure-only demotion with blockers preserved",
            "do_not": "do not call masses, charges, alpha_EM, or clock constants fixed unless the parent sector signs them or the rows are explicitly retained as residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1920_0_gain",
            "area": "source_weight residual",
            "summary": "1920 isolates the coupling bottleneck: no-source-weight and common-current clauses are unsigned.",
            "status": "BOXED_WITH_DELTA_W_QUEUE",
            "what_it_means": "we now know exactly what would be needed to stop source labels acting like hidden couplings",
            "next": "move to constant-sector residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1920_1_safety",
            "area": "coupling discipline",
            "summary": "mass, GM, Qbar, tau, covariance, and cross-residual hiding moves are explicitly blocked.",
            "status": "NO_ABSORPTION_GUARD_ACTIVE",
            "what_it_means": "future fits cannot accidentally bury the coupling residual",
            "next": "source Delta w_A or derive the common current owner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1920_2_next",
            "area": "residual priority",
            "summary": "constant_sector_residual is next because fixed masses/charges/alpha/clocks are needed for local GR and EM discipline.",
            "status": "NEXT_ATTACK_SELECTED",
            "what_it_means": "we continue moving through the residual vector instead of overfitting one obstruction",
            "next": "1921 constant-sector superselection",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "proof_attempt": proof_attempt_rows(),
        "delta_rows": delta_rows(),
        "guard": guard_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
    }


def copy_branch_artifacts() -> None:
    for source, destination in BRANCH_COPIES:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = parse_csv(OUTPUTS["source_register"])
    rows.append(
        {
            "validation_id": "VAL1920_00_sources",
            "status": "PASS" if all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    proof = parse_csv(OUTPUTS["proof_attempt"])
    verdict = next(r for r in proof if r["proof_id"] == "SWP1920_5_verdict")
    rows.append(
        {
            "validation_id": "VAL1920_01_proof_attempt",
            "status": "PASS" if verdict["current_status"] == "NOT_DERIVED_CURRENT_CORPUS_DELTA_W_ROWS_STAGED" and all(r["proof_pass"] == "False" for r in proof) else "FAIL",
            "detail": "source-weight zero proof remains unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    deltas = parse_csv(OUTPUTS["delta_rows"])
    rows.append(
        {
            "validation_id": "VAL1920_02_delta_rows",
            "status": "PASS" if len(deltas) == 4 and all(r["status"] == "SOURCE_READY_SCHEMA_ONLY_NONCLAIM" and r["valid_for_claim"] == "False" for r in deltas) else "FAIL",
            "detail": "four Delta w_A arena schemas staged as nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    guards = parse_csv(OUTPUTS["guard"])
    rows.append(
        {
            "validation_id": "VAL1920_03_absorption_guard",
            "status": "PASS" if len(guards) == 5 and all(r["status"] == "ACTIVE" for r in guards) else "FAIL",
            "detail": "mass/GM/Qbar/tau/covariance hiding shortcuts forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(r for r in gates if r["gate_id"] == "CG1920_3_local_claim")
    rows.append(
        {
            "validation_id": "VAL1920_04_claim_gate",
            "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL",
            "detail": "source_weight residual supports no claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append(
        {
            "validation_id": "VAL1920_05_decision",
            "status": "PASS" if any(r["decision"] == "MOVE_TO_CONSTANT_SECTOR_RESIDUAL" for r in decisions) else "FAIL",
            "detail": "constant-sector residual selected after boxing source_weight",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append(
        {
            "validation_id": "VAL1920_06_next_target",
            "status": "PASS" if next_rows[0]["target_doc"].startswith("1921-Y5-R2FR-constant-sector") else "FAIL",
            "detail": "1921 constant-sector route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    all_generated = [p for k, p in OUTPUTS.items() if k != "validation"]
    all_claim_safe = True
    csv_ok = True
    for path in all_generated:
        try:
            parsed = parse_csv(path)
            csv_ok = csv_ok and bool(parsed)
            for row in parsed:
                if row.get("valid_for_claim", "False") != "False" or row.get("claim_allowed", "False") != "False":
                    all_claim_safe = False
        except Exception:
            csv_ok = False
    rows.append(
        {
            "validation_id": "VAL1920_07_claim_flags_safe",
            "status": "PASS" if all_claim_safe else "FAIL",
            "detail": "claim flags all false",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    rows.append(
        {
            "validation_id": "VAL1920_08_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSVs parse with rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    rows.append(
        {
            "validation_id": "VAL1920_09_branch_copies",
            "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL",
            "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append(
        {
            "validation_id": "VAL1920_10_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.name.startswith("1920-")
            or "_1920" in path.name
            or "1920_" in path.name
            or "Y5_R2FR_source_weight" in path.name
        )
    rows.append(
        {
            "validation_id": "VAL1920_11_formalization_untouched",
            "status": "PASS" if formalization_count == 0 else "FAIL",
            "detail": f"formalization_1920_artifact_count={formalization_count}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        {
            "validation_id": "VAL1920_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1920 source-weight parent current owner or Delta w first rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("\n", " ").replace("|", "\\|") for h in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1920 - Source-Weight Parent Current Owner Or Delta-w First Rows

## Purpose

This checkpoint attacks the rank-3 `source_weight_residual`: either prove the parent forbids species/source weights through a common current/measure owner, or stage explicit `Delta w_A` rows without claiming a pass.

## Result

- The parent common-current/no-source-weight theorem is not derived from the current corpus.
- The obstruction is the coupling pressure we expected: no-species-weight exclusion, common-current ownership, and hidden-to-visible coefficient exclusion are unsigned.
- Four source-ready but nonclaim `Delta w_A` row schemas are staged for MICROSCOPE/WEP, R10, PPN, and orbital systems.
- Absorption into mass, measured `GM`, `Qbar`, `tau`, covariance, or cross-residual cancellation is explicitly forbidden.
- The next target is `constant_sector_residual`: fixed mass/charge/alpha/clock superselection or finite coefficient rows.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Parent Current Proof Attempt

{markdown_table(rows_by_name["proof_attempt"])}

## Delta-w First Rows

{markdown_table(rows_by_name["delta_rows"])}

## No-Absorption Guard

{markdown_table(rows_by_name["guard"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["snapshot"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
