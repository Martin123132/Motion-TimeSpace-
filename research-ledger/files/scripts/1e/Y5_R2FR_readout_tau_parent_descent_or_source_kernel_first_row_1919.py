from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1919"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1919-Y5-R2FR-readout-tau-parent-descent-or-source-kernel-first-row.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1918_doc": ROOT / "1918-Y5-R2FR-parent-cg-source-or-qkernel-matter-interface-proof.md",
    "1918_next": OUT / "P8_Y5_PARENT_QLOC_1918_NEXT_TARGET.csv",
    "1915_priority": OUT / "P8_Y5_PARENT_QLOC_1915_RESIDUAL_PRIORITY_MATRIX_NONCLAIM.csv",
    "1914_vector": OUT / "P8_Y5_PARENT_QLOC_1914_FINITE_RESIDUAL_VECTOR_V0_NONCLAIM.csv",
    "1913_typing": OUT / "P8_Y5_PARENT_QLOC_1913_Q_FUNCTOR_TYPING_MATRIX_NONCLAIM.csv",
    "1913_parent": OUT / "P8_Y5_PARENT_QLOC_1913_PARENT_ACTION_Q_FUNCTOR_CONSTRUCTION_ATTEMPT.csv",
    "1912_axioms": OUT / "P8_Y5_PARENT_QLOC_1912_MINIMAL_AXIOM_DEBT_LEDGER_NONCLAIM.csv",
    "1033_tau_audit": OUT / "P8_Y5_R10_1033_TAU_R10_DERIVATION_AUDIT.csv",
    "1033_acquisition": OUT / "P8_Y5_R10_1033_R10_ACQUISITION_TEMPLATE.csv",
}

NEEDLES = {
    "1918_doc": ["NEXT1918_0_primary", "VAL1918_OVERALL"],
    "1918_next": ["NEXT1918_0_primary", "readout_tau_residual"],
    "1915_priority": ["readout_tau_residual", "HIGH_LEVERAGE_BUT_KERNELS_MISSING"],
    "1914_vector": ["FRV1914_readout_tau_residual", "MISSING_ARENA_KERNELS"],
    "1913_typing": ["QTM1913_7_readout_boundary", "OPEN_RETAIN_IN_S_RES"],
    "1913_parent": ["PAQ1913_5_verdict", "CONSTRUCTION_CONTRACT_READY_PARENT_CERTIFICATION_FAILED"],
    "1912_axioms": ["AX1912_7_variation_before_readout", "MISSING_AXIOM_NOT_ADOPTED"],
    "1033_tau_audit": ["TAUR1033_6_verdict", "NOT_DERIVED_CURRENT_CORPUS"],
    "1033_acquisition": ["R10ACQ1033_3_tau_R10", "MISSING_ARENA_PROJECTION"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1919_SOURCE_REGISTER.csv",
    "proof_attempt": OUT / "P8_Y5_PARENT_QLOC_1919_READOUT_DESCENT_PROOF_ATTEMPT.csv",
    "tau_lock_audit": OUT / "P8_Y5_PARENT_QLOC_1919_TAU_SOURCE_NORMAL_LOCK_AUDIT.csv",
    "kernel_rows": OUT / "P8_Y5_PARENT_QLOC_1919_FIRST_READOUT_KERNEL_ROW_NONCLAIM.csv",
    "calibration_guard": OUT / "P8_Y5_PARENT_QLOC_1919_CALIBRATION_NO_ABSORPTION_GUARD.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1919_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1919_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1919_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1919_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1919_VALIDATION.csv",
}

BRANCH_COPIES = {
    OUTPUTS["proof_attempt"]: SOURCE_WEIGHT_DOCS / "READOUT_TAU_PARENT_DESCENT_PROOF_ATTEMPT_1919_NONCLAIM.csv",
    OUTPUTS["kernel_rows"]: MICROSCOPE_RESIDUALS / "P8_Y5_PARENT_QLOC_1919_FIRST_READOUT_KERNEL_ROW_NONCLAIM.csv",
    OUTPUTS["tau_lock_audit"]: QUEUE / "JR1919_READOUT_TAU_KERNEL_ACQUISITION_QUEUE.csv",
    OUTPUTS["claim_gate"]: QUARANTINE / "P8_Y5_PARENT_QLOC_1919_CLAIM_GATE.csv",
}


def ensure_dirs() -> None:
    for path in [OUT, MICROSCOPE_RESIDUALS, QUEUE, SOURCE_WEIGHT_DOCS, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_key, path in SOURCES.items():
        missing: list[str] = []
        exists = path.exists()
        text = read_text(path) if exists else ""
        for needle in NEEDLES[source_key]:
            if needle not in text:
                missing.append(needle)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": source_key,
                "source_path": str(path),
                "needed_for": "1919 readout/tau parent descent or source-kernel first row",
                "needles": ";".join(NEEDLES[source_key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_OR_NEEDLE_FAILED",
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
            "proof_id": "RTP1919_0_target",
            "claim_piece": "readout-after-variation parent descent theorem",
            "formal_statement": "For each local arena a, variation is performed on S_parent before readout/calibration, and readout R_a depends only on q(Phi), ordinary matter data, fixed theta_A, and declared boundary class.",
            "current_status": "TARGET_SHARP",
            "source_anchor": "NEXT1918_0_primary; FRV1914_readout_tau_residual",
            "what_fails": "not a failure row; establishes the theorem target",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "RTP1919_1_variation_order",
            "claim_piece": "variation before readout",
            "formal_statement": "delta S_parent is evaluated before material projection, detector readout, source normalization, calibration, or fitting.",
            "current_status": "MISSING_AXIOM_NOT_ADOPTED",
            "source_anchor": "AX1912_7_variation_before_readout",
            "what_fails": "the corpus names this as required, but it is not parent-derived or explicitly adopted as a closure axiom",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "RTP1919_2_readout_boundary_owner",
            "claim_piece": "readout and boundary owner",
            "formal_statement": "R_a and boundary/source-worldtube terms descend through the quotient or are exact/proper/common-mode before arena projection.",
            "current_status": "OPEN_RETAIN_IN_S_RES",
            "source_anchor": "QTM1913_7_readout_boundary; NQD1912_2_open_neighbourhood_upgrade",
            "what_fails": "post-selector and boundary source tails remain live countermodels",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "RTP1919_3_tau_source_normal_lock",
            "claim_piece": "tau/source-normal lock",
            "formal_statement": "tau_a, K_X(lambda), Qbar_XH, and arena source normalization are derived from the same parent readout/source functional, not fitted independently.",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS",
            "source_anchor": "TAUR1033_6_verdict; R10ACQ1033_3_tau_R10",
            "what_fails": "tau_R10 is only definition-level and companion factors remain missing",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "RTP1919_4_calibration_guard",
            "claim_piece": "no calibration hiding",
            "formal_statement": "unproved readout/tau/source-normal pieces cannot be absorbed into measured GM, fitted tau, detector calibration, or nuisance offsets unless a parent identity proves the absorption common-mode.",
            "current_status": "GUARD_ENFORCED_AS_POLICY_NOT_PROOF",
            "source_anchor": "P8_Y5_PARENT_QLOC_1915_NO_CANCELLATION_FIRST_FILL_DRYRUN.csv:DFF1915_2_cancellation_fit",
            "what_fails": "guard prevents false closure but does not derive a zero",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "RTP1919_5_verdict",
            "claim_piece": "1919 readout/tau descent verdict",
            "formal_statement": "The rank-2 readout_tau_residual is not zero-derived in the current corpus; it requires either parent-signed readout/variation order or explicit finite arena kernels.",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS_KERNEL_ROWS_STAGED",
            "source_anchor": "RTP1919_1_variation_order through RTP1919_4_calibration_guard",
            "what_fails": "variation order, readout boundary owner, tau/source-normal lock, and arena kernels remain unsigned",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def tau_lock_rows() -> list[dict[str, Any]]:
    arenas = [
        ("TLS1919_0_R10_tau", "R10_short_range", "tau_R10", "R10ACQ1033_3_tau_R10", "MISSING_ARENA_PROJECTION"),
        ("TLS1919_1_WEP_tau", "WEP_MICROSCOPE_TiPt", "tau_TiPt", "FRV1914_readout_tau_residual", "MISSING_DIFFERENTIAL_MATERIAL_READOUT_KERNEL"),
        ("TLS1919_2_PPN_tau", "PPN_beta_gamma_source", "tau_PPN", "FRV1914_readout_tau_residual", "MISSING_PPN_SOURCE_READOUT_KERNEL"),
        ("TLS1919_3_clock_tau", "clock_and_constant_drift", "tau_clock", "FRV1914_readout_tau_residual", "MISSING_CLOCK_READOUT_KERNEL"),
        ("TLS1919_4_orbital_tau", "orbital_GM_inverse_square", "tau_orbital", "FRV1914_readout_tau_residual", "MISSING_ORBITAL_GM_READOUT_KERNEL"),
    ]
    rows: list[dict[str, Any]] = []
    for lock_id, arena, symbol, anchor, status in arenas:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "lock_id": lock_id,
                "arena": arena,
                "symbol": symbol,
                "required_lock": "same parent variation/readout/source-normal functional controls the arena kernel",
                "source_anchor": anchor,
                "current_status": status,
                "missing_for_claim": "parent readout functional; material profile; source worldtube; normalization convention; uncertainty/prior",
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "lock_id": "TLS1919_5_verdict",
            "arena": "all_local_arenas",
            "symbol": "tau_a_vector",
            "required_lock": "all arena tau/source-normal kernels derived or sourced with shared convention",
            "source_anchor": "TLS1919_0_R10_tau through TLS1919_4_orbital_tau",
            "current_status": "NOT_LOCKED_CURRENT_CORPUS",
            "missing_for_claim": "every arena still lacks at least one parent/source/readout input",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    )
    return rows


def kernel_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    specs = [
        ("RTK1919_0_R10_first_row", "R10_short_range", "tau_R10(lambda)", "MISSING_ARENA_PROJECTION", "dimensionless", "test_body;material;profile;tau_R10;trace_convention;K_X;Qbar_XH;c_g;tail_envelope;source_path"),
        ("RTK1919_1_WEP_first_row", "WEP_MICROSCOPE_TiPt", "tau_TiPt(material_pair)", "MISSING_DIFFERENTIAL_READOUT_KERNEL", "dimensionless_or_declared", "source_body;test_materials;tau_Ti;tau_Pt;composition_model;readout_functional;uncertainty;source_path"),
        ("RTK1919_2_PPN_first_row", "PPN_beta_gamma_source", "tau_PPN(source)", "MISSING_PPN_READOUT_KERNEL", "dimensionless_or_declared", "source_body;metric_readout;stress_trace_convention;tau_PPN;uncertainty;source_path"),
        ("RTK1919_3_clock_first_row", "clock_and_constant_drift", "tau_clock(transition)", "MISSING_CLOCK_READOUT_KERNEL", "dimensionless_or_declared", "clock_transition;sensitivity_vector;readout_functional;tau_clock;uncertainty;source_path"),
        ("RTK1919_4_orbital_first_row", "orbital_GM_inverse_square", "tau_orbital(GM)", "MISSING_ORBITAL_GM_KERNEL", "dimensionless_or_declared", "source_body;orbit_model;GM_calibration_rule;tau_orbital;support_profile;uncertainty;source_path"),
    ]
    for kernel_id, arena, symbol, value, units, required in specs:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "kernel_id": kernel_id,
                "residual_component": "readout_tau_residual",
                "arena": arena,
                "kernel_symbol": symbol,
                "candidate_value": value,
                "units": units,
                "source_path": "MISSING_PARENT_OR_EXPERIMENTAL_KERNEL_SOURCE",
                "source_row_id": "MISSING_SOURCE_ROW_ID",
                "required_columns": required,
                "parent_requirements": "variation_before_readout; readout_map_owner; source_worldtube; no_calibration_hiding",
                "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def calibration_guard_rows() -> list[dict[str, Any]]:
    guards = [
        ("CNG1919_0_measured_GM", "absorb tau_orbital into measured GM", "FORBIDDEN_WITHOUT_PARENT_COMMON_MODE_IDENTITY"),
        ("CNG1919_1_detector_tau", "fit tau_a as free detector nuisance and call it derived", "FORBIDDEN_AS_DERIVATION"),
        ("CNG1919_2_R10_normalization", "absorb K_X/Qbar/tau_R10 into alpha_predicted without separate provenance", "FORBIDDEN_FOR_SCORE"),
        ("CNG1919_3_cross_residual_cancel", "cancel readout_tau against frame/source_weight residuals", "FORBIDDEN_WITHOUT_PARENT_IDENTITY"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "forbidden_move": move,
            "policy": policy,
            "reason": "readout/tau residuals are exactly the coupling leak we are trying to expose, not a bin for calibration magic",
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
            "gate_id": "CG1919_0_readout_parent_descent",
            "requirement": "readout-after-variation theorem parent-signed",
            "status": "FAIL_NOT_PARENT_SIGNED",
            "evidence": "RTP1919_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1919_1_tau_source_lock",
            "requirement": "tau/source-normal kernels locked or sourced per arena",
            "status": "FAIL_KERNELS_MISSING",
            "evidence": "TLS1919_5_verdict; RTK1919_0_R10_first_row through RTK1919_4_orbital_first_row",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1919_2_calibration_guard",
            "requirement": "no absorption into GM/tau/calibration/nuisance offsets",
            "status": "PASS_GUARD_ONLY",
            "evidence": "CNG1919_0_measured_GM through CNG1919_3_cross_residual_cancel",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1919_3_local_claim",
            "requirement": "readout_tau_residual supports local-GR/WEP/R10/PPN/clock/orbital claim",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1919_0_readout_parent_descent; CG1919_1_tau_source_lock",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1919_0_derivation_result",
            "decision": "READOUT_TAU_ZERO_NOT_DERIVED",
            "why": "variation-before-readout and readout/boundary owner remain unsigned",
            "next_action": "keep readout_tau as finite residual with explicit arena kernels",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1919_1_kernel_result",
            "decision": "FIRST_KERNEL_ROWS_STAGED_NONCLAIM",
            "why": "five arena schemas now say exactly what source/readout inputs are missing",
            "next_action": "do not score any arena until rows are sourced and no MISSING markers remain",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1919_2_next_residual",
            "decision": "MOVE_TO_SOURCE_WEIGHT_RESIDUAL",
            "why": "readout_tau is boxed as source-kernel acquisition; 1915 ranks source_weight next and it directly attacks the coupling bottleneck",
            "next_action": "1920 should try parent current/measure owner proof or stage Delta w_A rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1919_0_primary",
            "selection_status": "selected",
            "target_doc": "1920-Y5-R2FR-source-weight-parent-current-owner-or-delta-w-first-rows.md",
            "target_script": "scripts/Y5_R2FR_source_weight_parent_current_owner_or_delta_w_first_rows_1920.py",
            "objective": "attack the rank-3 source_weight_residual: prove species/source weights are forbidden by a parent current/measure owner, or stage Delta w_A arena rows as nonclaim",
            "success_condition": "source_weight_residual gets a parent theorem-zero source path, a finite source-ready Delta w row family, or a closure-only demotion with blockers preserved",
            "do_not": "do not absorb source weights into measured masses, GM, detector response, or covariance/minimality arguments",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1919_0_gain",
            "area": "readout_tau residual",
            "summary": "1919 identifies the exact non-derivation: variation order, readout owner, tau/source-normal lock, and arena kernels are missing.",
            "status": "BOXED_WITH_SOURCE_KERNEL_QUEUE",
            "what_it_means": "the route is not dead, but it cannot be claim-grade until kernels are derived or sourced",
            "next": "move to source_weight coupling residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1919_1_safety",
            "area": "calibration discipline",
            "summary": "measured GM, fitted tau, detector calibration, and cross-residual cancellations are explicitly forbidden as hiding places.",
            "status": "NO_ABSORPTION_GUARD_ACTIVE",
            "what_it_means": "we preserved the integrity of future local tests",
            "next": "source or derive kernels before scoring",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1919_2_next",
            "area": "residual priority",
            "summary": "source_weight_residual is now the best route because it targets the coupling problem directly.",
            "status": "NEXT_ATTACK_SELECTED",
            "what_it_means": "we stop circling c_g/readout and move to the current/measure owner problem",
            "next": "1920 source-weight parent current owner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "proof_attempt": proof_attempt_rows(),
        "tau_lock_audit": tau_lock_rows(),
        "kernel_rows": kernel_rows(),
        "calibration_guard": calibration_guard_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
    }


def copy_branch_artifacts() -> None:
    for source, destination in BRANCH_COPIES.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    sources = parse_csv(OUTPUTS["source_register"])
    rows.append(
        {
            "validation_id": "VAL1919_00_sources",
            "status": "PASS" if all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    proof = parse_csv(OUTPUTS["proof_attempt"])
    verdict = next(r for r in proof if r["proof_id"] == "RTP1919_5_verdict")
    rows.append(
        {
            "validation_id": "VAL1919_01_proof_attempt",
            "status": "PASS" if verdict["current_status"] == "NOT_DERIVED_CURRENT_CORPUS_KERNEL_ROWS_STAGED" and all(r["proof_pass"] == "False" for r in proof) else "FAIL",
            "detail": "readout/tau descent proof fails without parent-signed clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    lock = parse_csv(OUTPUTS["tau_lock_audit"])
    lock_verdict = next(r for r in lock if r["lock_id"] == "TLS1919_5_verdict")
    rows.append(
        {
            "validation_id": "VAL1919_02_tau_lock",
            "status": "PASS" if lock_verdict["current_status"] == "NOT_LOCKED_CURRENT_CORPUS" else "FAIL",
            "detail": "tau/source-normal lock remains unclosed",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    kernels = parse_csv(OUTPUTS["kernel_rows"])
    rows.append(
        {
            "validation_id": "VAL1919_03_kernel_rows",
            "status": "PASS" if len(kernels) == 5 and all(r["status"] == "SOURCE_READY_SCHEMA_ONLY_NONCLAIM" and r["valid_for_claim"] == "False" for r in kernels) else "FAIL",
            "detail": "five arena kernel schemas staged as nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    guards = parse_csv(OUTPUTS["calibration_guard"])
    rows.append(
        {
            "validation_id": "VAL1919_04_calibration_guard",
            "status": "PASS" if len(guards) == 4 and all(r["status"] == "ACTIVE" for r in guards) else "FAIL",
            "detail": "calibration/GM/tau absorption shortcuts forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    gates = parse_csv(OUTPUTS["claim_gate"])
    claim_gate = next(r for r in gates if r["gate_id"] == "CG1919_3_local_claim")
    rows.append(
        {
            "validation_id": "VAL1919_05_claim_gate",
            "status": "PASS" if claim_gate["status"] == "CLAIM_BLOCKED" else "FAIL",
            "detail": "readout_tau residual supports no claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    decisions = parse_csv(OUTPUTS["decision"])
    rows.append(
        {
            "validation_id": "VAL1919_06_decision",
            "status": "PASS" if any(r["decision"] == "MOVE_TO_SOURCE_WEIGHT_RESIDUAL" for r in decisions) else "FAIL",
            "detail": "source_weight residual selected after boxing readout_tau",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append(
        {
            "validation_id": "VAL1919_07_next_target",
            "status": "PASS" if next_rows[0]["target_doc"].startswith("1920-Y5-R2FR-source-weight") else "FAIL",
            "detail": "1920 source-weight route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    all_generated = [p for k, p in OUTPUTS.items() if k != "validation"]
    all_claim_safe = True
    for path in all_generated:
        for row in parse_csv(path):
            if row.get("valid_for_claim", "False") != "False" or row.get("claim_allowed", "False") != "False":
                all_claim_safe = False
    rows.append(
        {
            "validation_id": "VAL1919_08_claim_flags_safe",
            "status": "PASS" if all_claim_safe else "FAIL",
            "detail": "claim flags all false",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    csv_ok = True
    for path in all_generated:
        try:
            parsed = parse_csv(path)
            csv_ok = csv_ok and bool(parsed)
        except Exception:
            csv_ok = False
    rows.append(
        {
            "validation_id": "VAL1919_09_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSVs parse with rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    branch_copy_ok = all(path.exists() for path in BRANCH_COPIES.values())
    rows.append(
        {
            "validation_id": "VAL1919_10_branch_copies",
            "status": "PASS" if branch_copy_ok else "FAIL",
            "detail": "; ".join(str(path) for path in BRANCH_COPIES.values()),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    pycache = ROOT / "scripts" / "__pycache__"
    rows.append(
        {
            "validation_id": "VAL1919_11_pycache_absent",
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
            if path.name.startswith("1919-")
            or "_1919" in path.name
            or "1919_" in path.name
            or "Y5_R2FR_readout_tau" in path.name
        )
    rows.append(
        {
            "validation_id": "VAL1919_12_formalization_untouched",
            "status": "PASS" if formalization_count == 0 else "FAIL",
            "detail": f"formalization_1919_artifact_count={formalization_count}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )

    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        {
            "validation_id": "VAL1919_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1919 readout/tau parent descent or source-kernel first row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = row.get(header, "")
            values.append(str(value).replace("\n", " ").replace("|", "\\|"))
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1919 - Readout/Tau Parent Descent Or Source-Kernel First Row

## Purpose

This checkpoint attacks the rank-2 `readout_tau_residual`: either prove readout-after-variation plus tau/source-normal lock from the parent, or stage the first explicit arena kernel rows without claiming a pass.

## Result

- The readout/tau zero theorem is not derived from the current corpus.
- The obstruction is precise: variation-before-readout, readout/boundary ownership, tau/source-normal lock, and arena kernels are unsigned.
- Five source-ready but nonclaim kernel rows are staged for R10, MICROSCOPE/WEP, PPN, clocks, and orbital systems.
- Calibration hiding is explicitly forbidden: no absorbing this residual into measured `GM`, fitted `tau`, detector response, or cross-residual cancellation.
- The next target is `source_weight_residual`, because it hits the coupling/current-owner bottleneck directly.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Readout Descent Proof Attempt

{markdown_table(rows_by_name["proof_attempt"])}

## Tau/Source-Normal Lock Audit

{markdown_table(rows_by_name["tau_lock_audit"])}

## First Readout Kernel Rows

{markdown_table(rows_by_name["kernel_rows"])}

## Calibration No-Absorption Guard

{markdown_table(rows_by_name["calibration_guard"])}

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
