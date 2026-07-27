from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3096"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3096-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3096_00_3095_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3095_NEXT_TARGET.csv",
        "needles": ["NEXT3095_0_primary", "frame-marker-coupling-bound-input-pack"],
        "role": "3095 selects the frame/marker coupling pack or no-marker theorem target.",
    },
    "SRC3096_01_3095_doc": {
        "path": ROOT / "3095-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row-under-AX1090.md",
        "needles": ["FRAME_MARKER_BOUND_INPUT_OR_NO_MARKER_THEOREM", "qbar_XT_bound_abs"],
        "role": "3095 turns qbarXT into theorem-zero or component-bound work.",
    },
    "SRC3096_02_1850_doc": {
        "path": ROOT / "1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
        "needles": ["Frame/Marker Coupling Bound Input Pack", "fixed external spurions"],
        "role": "1850 active-branch precedent for partial no-marker progress and bound pack.",
    },
    "SRC3096_03_1850_no_marker": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_NO_MARKER_THEOREM_ATTEMPT.csv",
        "needles": ["NMT1850_6_verdict", "NO_MARKER_THEOREM_NOT_CLOSED"],
        "role": "1850 no-marker theorem attempt fails full claim but gives partial theorem rows.",
    },
    "SRC3096_04_1850_partial": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_PARTIAL_NO_MARKER_THEOREM.csv",
        "needles": ["PT1850_0_fixed_spurion_no_go", "GUARDRAIL_ACTIVE"],
        "role": "1850 partial no-marker theorem and guardrail rows.",
    },
    "SRC3096_05_1850_survivors": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_SURVIVING_MARKER_FAMILY_AUDIT.csv",
        "needles": ["SMF1850_1_common_frame", "LIVE_UNLESS_CG_ZERO_OR_BOUNDED"],
        "role": "1850 surviving marker family audit.",
    },
    "SRC3096_06_1850_bound_pack": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_FRAME_MARKER_BOUND_INPUT_PACK.csv",
        "needles": ["FMB1850_10_total_qbarXT_envelope", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1850 frame/marker/source bound input pack.",
    },
    "SRC3096_07_1850_projection": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_ARENA_PROJECTION_ROWS.csv",
        "needles": ["APR1850_0_tau_R10", "MISSING_ARENA_PROJECTION"],
        "role": "1850 arena projection rows for local tests.",
    },
    "SRC3096_08_1850_next": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1850_NEXT_TARGET.csv",
        "needles": ["NEXT1850_0_primary", "first-real-local-coupling-bound-source-table"],
        "role": "1850 selects first real local coupling bound source table.",
    },
    "SRC3096_09_1028_bound_pack": {
        "path": RESIDUALS / "P8_Y5_R10_1028_FRAME_MARKER_BOUND_INPUT_PACK.csv",
        "needles": ["FMB1028_10_total_qbarXT_envelope", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1028 older frame/marker/source input pack.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3096_SOURCE_REGISTER.csv",
    "no_marker": RESIDUALS / "P8_Y5_R2FR_3096_NO_MARKER_THEOREM_ATTEMPT.csv",
    "partial": RESIDUALS / "P8_Y5_R2FR_3096_PARTIAL_NO_MARKER_THEOREM.csv",
    "survivors": RESIDUALS / "P8_Y5_R2FR_3096_SURVIVING_MARKER_FAMILY_AUDIT.csv",
    "bound_pack": RESIDUALS / "P8_Y5_R2FR_3096_FRAME_MARKER_BOUND_INPUT_PACK.csv",
    "arena": RESIDUALS / "P8_Y5_R2FR_3096_ARENA_PROJECTION_ROWS.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_3096_QBARXT_TOTAL_ENVELOPE.csv",
    "dependencies": RESIDUALS / "P8_Y5_R2FR_3096_DEPENDENCY_LINKS.csv",
    "refusal": RESIDUALS / "P8_Y5_R2FR_3096_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3096_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3096_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3096_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3096_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3096_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "no_marker_copy": LOCAL_BOUNDS / "no_marker_theorem_attempt_3096_NONCLAIM.csv",
    "bound_pack_copy": LOCAL_BOUNDS / "frame_marker_bound_input_pack_3096_NONCLAIM.csv",
    "arena_copy": LOCAL_BOUNDS / "arena_projection_rows_3096_NONCLAIM.csv",
    "decisions_copy": LOCAL_BOUNDS / "decision_ledger_3096_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3096_first_real_local_coupling_bounds_NEXT_NONCLAIM.csv",
}


def meta() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def source_parse_ok(path: Path) -> bool:
    return csv_ok(path) if path.suffix.lower() == ".csv" else path.exists()


def with_meta(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = meta()
    return [{**base, **row} for row in output_rows]


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in output_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, Any]]:
    output_rows = []
    for source_id, source in SOURCES.items():
        path = Path(source["path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        output_rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "parse_ok": source_parse_ok(path),
                "sha256": file_hash(path),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return with_meta(output_rows)


def no_marker_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "attempt_id": "NMT3096_0_target",
                "claim_piece": "ordinary matter carries no independent X-marker",
                "formal_statement": "For every admissible ordinary matter sector A, S_A depends on X only through descended observed structures O(q(Phi)) and quotient-owned constants theta_A(q).",
                "derived_status": "TARGET_STATEMENT",
                "proof_status": "CONDITIONAL_ONLY",
                "missing_or_blocker": "parent matter functor, constant ownership, hidden frame silence and boundary support silence are not signed in one clause",
                "observable_impact": "would set qbar_constants=qbar_marker=qbar_source_weight=0",
            },
            {
                "attempt_id": "NMT3096_1_fixed_spurion_exclusion",
                "claim_piece": "fixed external covectors and active labels are illegal",
                "formal_statement": "A fixed active marker ell_X in E_X* is not a natural quotient functor and is excluded by parent object-language hygiene.",
                "derived_status": "PARTIAL_THEOREM",
                "proof_status": "SIGNED_AS_DESIGN_CONTRACT_NOT_FULL_PARENT_DERIVATION",
                "missing_or_blocker": "does not exclude co-moving material/domain/source markers",
                "observable_impact": "kills the weakest linear marker counterexample only",
            },
            {
                "attempt_id": "NMT3096_2_no_invariant_linear_covector",
                "claim_piece": "no invariant first-order X covector from empty vertical structure",
                "formal_statement": "If the vertical fibre has no parent-owned covector, F_1(v_X)=0 for fixed empty-background marker attempts.",
                "derived_status": "PARTIAL_THEOREM",
                "proof_status": "CONDITIONAL",
                "missing_or_blocker": "material constants and domain/readout data can supply covectors after matter is included",
                "observable_impact": "supports local extremum/amplitude route but not qbar_XT=0",
            },
            {
                "attempt_id": "NMT3096_3_co_moving_material_marker",
                "claim_piece": "material markers cannot source X",
                "formal_statement": "A material label m_A, isotope fraction, preparation marker, or readout class is either quotient-owned or absent from S_A.",
                "derived_status": "NOT_DERIVED",
                "proof_status": "COUNTERMODEL_SURVIVES",
                "missing_or_blocker": "co-moving material markers can descend with matter and still change source/test normalization",
                "observable_impact": "requires b_A and b_marker bound rows",
            },
            {
                "attempt_id": "NMT3096_4_constant_superselection",
                "claim_piece": "masses, charges, alpha_EM and clock constants are X-independent",
                "formal_statement": "Lie_v theta_A=0 for all constants used by ordinary matter, clocks and EM readout.",
                "derived_status": "NOT_PARENT_SIGNED",
                "proof_status": "OPEN",
                "missing_or_blocker": "constant-sector target spaces are continuous unless topological/superselection ownership is supplied",
                "observable_impact": "requires b_A and b_alpha rows for WEP/clocks/fine-structure",
            },
            {
                "attempt_id": "NMT3096_5_source_weight_and_boundary",
                "claim_piece": "source weights and boundary/support terms are absent",
                "formal_statement": "No kappa_A, domain class chi_D, support shift, boundary flux, non-Hilbert tail, or post-readout EFT term survives local projection.",
                "derived_status": "NOT_DERIVED",
                "proof_status": "COUNTERMODEL_SURVIVES",
                "missing_or_blocker": "source-only weights, support shifts and post-readout reductions are not eliminated by no-linear-marker hygiene",
                "observable_impact": "requires delta_kappa_A, q_nonH, Delta_W_support, q_domain and q_boundary rows",
            },
            {
                "attempt_id": "NMT3096_6_verdict",
                "claim_piece": "full no-marker theorem",
                "formal_statement": "NMT3096_1 and NMT3096_2 are useful partial results, but NMT3096_3 through NMT3096_5 remain live.",
                "derived_status": "FAIL_CURRENT_CLAIM",
                "proof_status": "NO_MARKER_THEOREM_NOT_CLOSED",
                "missing_or_blocker": "ordinary matter constants, material markers, source weights and boundary/source tails need theorem-zero or numeric bounds",
                "observable_impact": "stage frame/marker coupling bound input pack; do not claim local GR or R10 pass from zero",
            },
        ]
    )


def partial_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "theorem_id": "PT3096_0_fixed_spurion_no_go",
                "theorem": "Fixed active marker no-go",
                "statement": "A non-dynamical labelled marker used only to generate a local X-force is not an admissible parent quotient functor.",
                "proof_sketch": "It is not pulled back from q(Phi), not varied as matter, and not a gauge redundancy; retaining it would add a new external background structure.",
                "scope": "fixed external labels and empty-background linear covectors",
                "what_it_does_not_prove": "does not remove co-moving material markers, common frame factors, constant sectors, or boundary/support tails",
                "status": "PARTIAL_PROGRESS",
                "claim_allowed": False,
            },
            {
                "theorem_id": "PT3096_1_first_order_empty_fibre",
                "theorem": "Empty-fibre first-order silence",
                "statement": "If the X-fibre has no parent-owned covector and the ordinary matter functor sees only quotient-owned observed structures, the empty-background F_1 term vanishes.",
                "proof_sketch": "There is no natural E_X* object to contract with v_X; the chain-rule variation factors through Dq(v_X)=0.",
                "scope": "geometric/source-zero theorem under strict functorial and constant-superselection assumptions",
                "what_it_does_not_prove": "does not sign those assumptions for the current MTS parent action",
                "status": "CONDITIONAL_PROGRESS",
                "claim_allowed": False,
            },
            {
                "theorem_id": "PT3096_2_no_claim_boundary",
                "theorem": "No hidden replacement theorem",
                "statement": "Any theorem-zero use must also forbid replacement markers: A_g(X), B_dis(X), theta_A(X), kappa_A(X), chi_D(X), q_nonH and boundary/support shifts.",
                "proof_sketch": "Otherwise qbar_XT can return under a different name while the visible matter action appears quotient-invariant.",
                "scope": "guardrail for future parent action clauses",
                "what_it_does_not_prove": "does not provide numeric values or external bounds",
                "status": "GUARDRAIL_ACTIVE",
                "claim_allowed": False,
            },
        ]
    )


def survivor_rows() -> list[dict[str, Any]]:
    survivors = [
        ("SMF3096_0_fixed_spurion", "fixed active external spurion/covector", "CONDITIONALLY_EXCLUDED", "not a natural quotient-owned parent object and violates the object-language hygiene gate", "object-language exclusion row plus no hidden replacement marker", False),
        ("SMF3096_1_common_frame", "hidden common Weyl/conformal matter frame", "LIVE_UNLESS_CG_ZERO_OR_BOUNDED", "a common A_g(X) can be WEP-blind while still moving R10/PPN/clock normalization", "c_g theorem-zero or numeric bound", True),
        ("SMF3096_2_disformal_frame", "hidden disformal/profile matter frame", "LIVE_UNLESS_BDIS_ZERO_OR_BOUNDED", "disformal terms can vanish in one limit but survive in clocks/orbits/PPN projections", "b_dis theorem-zero or projection-specific bound", True),
        ("SMF3096_3_material_constants", "m_A, mass ratios, isotope/material labels, preparation markers", "LIVE_UNLESS_BA_ZERO_OR_BOUNDED", "co-moving material labels can descend with matter and are not killed by fixed-spurion exclusion", "b_A/b_marker theorem-zero or source-backed sensitivity bounds", True),
        ("SMF3096_4_alpha_clock_constants", "alpha_EM, gauge/binding constants, clock transition markers", "LIVE_UNLESS_BALPHA_ZERO_OR_BOUNDED", "clock/fine-structure observables directly constrain constant drift but do not prove zero without ownership", "b_alpha theorem-zero or clock/fine-structure bound", True),
        ("SMF3096_5_source_boundary_tail", "source-only weights, domain classes, support shifts, boundary/non-Hilbert current", "LIVE_UNLESS_SOURCE_TAIL_ZERO_OR_BOUNDED", "these enter local source normalization even if geometry and matter functors look clean", "delta_kappa_A, q_nonH, Delta_W_support, q_domain, q_boundary bound rows", True),
    ]
    return with_meta(
        [
            {
                "marker_id": marker_id,
                "family": family,
                "status_after_3096": status,
                "why": why,
                "required_bound_or_theorem": required,
                "blocks_full_zero_claim": blocks,
            }
            for marker_id, family, status, why, required, blocks in survivors
        ]
    )


def bound_pack_rows() -> list[dict[str, Any]]:
    rows_data = [
        ("FMB3096_0_cg", "c_g", "common Weyl/conformal derivative d ln A_g/dXhat for ordinary matter or source frame", "|c_g| <= MISSING_COMMON_FRAME_BOUND", "MISSING_CG_BOUND_OR_ZERO_THEOREM", "dimensionless_per_normalized_Xhat", "R10;PPN;clock;WEP_common_mode", "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND"),
        ("FMB3096_1_bdis", "b_dis", "representative disformal/profile-normalized matter frame derivative", "|b_dis| <= MISSING_DISFORMAL_BOUND", "MISSING_BDIS_BOUND_OR_ZERO_THEOREM", "dimensionless_or_declared_profile_units", "PPN;clock;orbital;R10", "MISSING_DISFORMAL_ZERO_OR_NUMERIC_BOUND"),
        ("FMB3096_2_bA", "b_A", "vertical derivative of material mass/species constants d ln m_A/dXhat or equivalent sensitivity", "|b_A| <= MISSING_MATERIAL_CONSTANT_BOUND", "MISSING_BA_BOUND_OR_ZERO_THEOREM", "dimensionless_per_normalized_Xhat", "WEP;clock;R10;particle_mass", "MISSING_MATERIAL_CONSTANT_ZERO_OR_NUMERIC_BOUND"),
        ("FMB3096_3_balpha", "b_alpha", "vertical derivative of alpha_EM/gauge/binding/clock readout constants", "|b_alpha| <= MISSING_ALPHA_CLOCK_BOUND", "MISSING_BALPHA_BOUND_OR_ZERO_THEOREM", "dimensionless_per_normalized_Xhat", "clock;fine_structure;EM;R10", "MISSING_ALPHA_CONSTANT_ZERO_OR_NUMERIC_BOUND"),
        ("FMB3096_4_bmarker", "b_marker", "vertical derivative of material/source/preparation/readout marker channel", "|b_marker| <= MISSING_MARKER_CHANNEL_BOUND", "MISSING_BMARKER_BOUND_OR_ZERO_THEOREM", "dimensionless", "WEP_source_charge;R10;clock;readout", "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS"),
        ("FMB3096_5_delta_kappa_A", "delta_kappa_A", "relative source-only matter prefactor or species/source current weight kappa_A/kappa_univ - 1", "|delta_kappa_A| <= MISSING_SOURCE_WEIGHT_BOUND", "MISSING_DELTA_KAPPA_A_BOUND_OR_ZERO_THEOREM", "dimensionless", "WEP_source_charge;orbital;R10_source_mass", "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND"),
        ("FMB3096_6_qnonH", "q_nonH", "ordinary source projection from non-Hilbert current, torsion/connection tail, projector, or memory exchange", "|q_nonH| <= MISSING_NONHILBERT_SOURCE_BOUND", "MISSING_QNONH_BOUND_OR_ZERO_THEOREM", "dimensionless_after_source_normalization", "R10;orbital;source_normalization;boundary", "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND"),
        ("FMB3096_7_Delta_W_support", "Delta_W_support", "worldtube/support/domain shift under local projection or observed-frame choice", "|Delta_W_support| <= MISSING_SUPPORT_SHIFT_BOUND", "MISSING_SUPPORT_SHIFT_BOUND_OR_ZERO_THEOREM", "dimensionless_or_projection_declared", "orbital;R10;boundary;local_GR", "MISSING_SUPPORT_SHIFT_ZERO_OR_NUMERIC_BOUND"),
        ("FMB3096_8_qdomain", "q_domain", "domain class or chi_D selector contribution to source/test normalization", "|q_domain| <= MISSING_DOMAIN_CLASS_BOUND", "MISSING_QDOMAIN_BOUND_OR_ZERO_THEOREM", "dimensionless", "WEP;R10;orbital;readout", "MISSING_DOMAIN_MARKER_ZERO_OR_NUMERIC_BOUND"),
        ("FMB3096_9_qboundary", "q_boundary", "boundary/local projection flux contribution to qbar_XT", "|q_boundary| <= MISSING_BOUNDARY_FLUX_BOUND", "MISSING_QBOUNDARY_BOUND_OR_ZERO_THEOREM", "dimensionless_after_boundary_normalization", "boundary;orbital;local_GR;R10", "MISSING_BOUNDARY_FLUX_ZERO_OR_NUMERIC_BOUND"),
        ("FMB3096_10_total_qbarXT_envelope", "qbar_XT_bound_abs", "absolute no-cancellation envelope over frame, marker, constants, source weight and non-Hilbert/support components", "|qbar_XT| <= |tau_g c_g|+|tau_dis b_dis|+sum_A|s_A b_A|+|s_alpha b_alpha|+|b_marker|+|delta_kappa_A|+|q_nonH|+|Delta_W_support|+|q_domain|+|q_boundary|", "MISSING_COMPONENT_VALUES", "dimensionless_after_declared_normalization", "R10;WEP;clock;PPN;orbital;local_GR", "SCHEMA_READY_VALUES_MISSING"),
        ("FMB3096_11_claim_gate", "claim_gate", "no R10/local-GR/PPN/clock/orbital claim until every component is theorem-zero or source-backed numeric", "claim_allowed iff all component rows are valid_for_claim=true and no MISSING_* markers remain", "CLAIM_BLOCKED", "gate", "all local arenas", "CLAIM_BLOCKED"),
    ]
    return with_meta(
        [
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "formula_or_bound": formula,
                "current_value": current_value,
                "units": units,
                "source_path": "source-intake/mts_residuals/P8_Y5_R2FR_3096_FRAME_MARKER_BOUND_INPUT_PACK.csv",
                "observable_link": observable_link,
                "status": status,
            }
            for row_id, symbol, definition, formula, current_value, units, observable_link, status in rows_data
        ]
    )


def arena_rows() -> list[dict[str, Any]]:
    rows_data = [
        ("APR3096_0_tau_R10", "tau_R10", "R10 short-range alpha(lambda)", "c_g;b_dis;b_A;b_alpha;b_marker;delta_kappa_A;q_nonH;Delta_W_support;q_domain;q_boundary", "alpha_R10(lambda_X)=K_X Qbar_XH(lambda_X) qbar_XT_bound_abs tau_R10(lambda_X)", "MISSING_TAU_R10_AND_COMPONENT_VALUES", "dimensionless_projection_or_declared", "MISSING_ARENA_PROJECTION"),
        ("APR3096_1_tau_PPN", "tau_PPN", "local weak-field/PPN", "c_g;b_dis;q_nonH;Delta_W_support;q_boundary", "PPN_residual_vector <= tau_PPN dot absolute_component_vector", "MISSING_TAU_PPN_AND_COMPONENT_VALUES", "dimensionless_projection_or_declared", "MISSING_ARENA_PROJECTION"),
        ("APR3096_2_tau_clock", "tau_clock", "clocks/fine-structure/EM readout", "c_g;b_A;b_alpha;b_marker;q_nonH", "clock_residual <= tau_clock dot absolute_component_vector", "MISSING_TAU_CLOCK_AND_COMPONENT_VALUES", "dimensionless_projection_or_declared", "MISSING_ARENA_PROJECTION"),
        ("APR3096_3_tau_orbital", "tau_orbital", "orbital/source-support systems", "delta_kappa_A;q_nonH;Delta_W_support;q_domain;q_boundary;c_g", "orbital_residual <= tau_orbital dot absolute_component_vector", "MISSING_TAU_ORBITAL_AND_COMPONENT_VALUES", "dimensionless_projection_or_declared", "MISSING_ARENA_PROJECTION"),
        ("APR3096_4_tau_WEP", "tau_WEP", "WEP/source charge", "b_A;b_marker;delta_kappa_A;q_domain", "eta_AB <= tau_WEP dot absolute_differential_component_vector", "MISSING_TAU_WEP_AND_COMPONENT_VALUES", "dimensionless_projection_or_declared", "MISSING_ARENA_PROJECTION"),
        ("APR3096_5_tau_alphaEM", "tau_alphaEM", "EM/fine-structure", "b_alpha;b_A;b_marker;c_g", "alpha_EM_residual <= tau_alphaEM dot absolute_component_vector", "MISSING_TAU_ALPHAEM_AND_COMPONENT_VALUES", "dimensionless_projection_or_declared", "MISSING_ARENA_PROJECTION"),
    ]
    return with_meta(
        [
            {
                "projection_id": projection_id,
                "symbol": symbol,
                "arena": arena,
                "uses_components": uses_components,
                "formula_or_contract": formula,
                "current_value": current_value,
                "units": units,
                "status": status,
            }
            for projection_id, symbol, arena, uses_components, formula, current_value, units, status in rows_data
        ]
    )


def envelope_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "envelope_id": "ENV3096_0_component_vector",
                "quantity": "absolute_component_vector",
                "formula": "(|c_g|,|b_dis|,|b_A|,|b_alpha|,|b_marker|,|delta_kappa_A|,|q_nonH|,|Delta_W_support|,|q_domain|,|q_boundary|)",
                "rule": "all unknown signs are discarded",
                "status": "GUARDRAIL_ACTIVE",
            },
            {
                "envelope_id": "ENV3096_1_no_cancellation",
                "quantity": "qbar_XT_bound_abs",
                "formula": "sum of absolute projected component magnitudes",
                "rule": "no cancellation between frame, marker, source and boundary tails may be used to pass local tests",
                "status": "GUARDRAIL_ACTIVE",
            },
            {
                "envelope_id": "ENV3096_2_claim_block",
                "quantity": "local_claim",
                "formula": "claim_allowed=false while any component/projection has MISSING_* or valid_for_claim=false",
                "rule": "schema can guide work but cannot be scored as evidence",
                "status": "CLAIM_BLOCKED",
            },
        ]
    )


def dependency_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "dependency_id": "DEP3096_0_no_marker_to_qbar_zero",
                "quantity": "qbar_XT=0",
                "requires": "full no-marker theorem plus parent matter functor plus boundary/source silence",
                "status": "FAIL_CURRENT_CLAIM",
                "reason": "partial no-spurion theorem does not eliminate live marker families",
                "next_action": "do not set qbar_XT=0; retain bound envelope",
            },
            {
                "dependency_id": "DEP3096_1_bound_pack_to_R10",
                "quantity": "alpha_R10(lambda_X)",
                "requires": "K_X;Qbar_XH(lambda_X);lambda_X;real alpha_bound(lambda);qbar_XT_bound_abs;tau_R10",
                "status": "BLOCKED_BY_COMPONENT_VALUES_AND_PROJECTION",
                "reason": "3096 supplies rows, not numeric bounds",
                "next_action": "source first real c_g/b_A/b_alpha/q_nonH/projection inputs",
            },
            {
                "dependency_id": "DEP3096_2_local_GR_to_zero_or_bounds",
                "quantity": "local GR limit",
                "requires": "all frame/marker/source/boundary components theorem-zero or below local arena bounds",
                "status": "BLOCKED",
                "reason": "local GR cannot be declared from covariance alone if matter/source couplings are unsigned",
                "next_action": "use no-cancellation component envelope",
            },
        ]
    )


def refusal_rows() -> list[dict[str, Any]]:
    refusals = [
        ("REF3096_0_full_no_marker", "full no-marker theorem closes", "FAIL_CURRENT_CLAIM", "NMT3096_3_co_moving_material_marker;NMT3096_4_constant_superselection;NMT3096_5_source_weight_and_boundary"),
        ("REF3096_1_qbarXT_zero", "qbar_XT=0", "NO_MARKER_THEOREM_NOT_CLOSED", "NMT3096_6_verdict;DEP3096_0_no_marker_to_qbar_zero"),
        ("REF3096_2_bound_values", "qbar_XT_bound_abs numeric", "SCHEMA_READY_VALUES_MISSING", "FMB3096_0_cg through FMB3096_10_total_qbarXT_envelope;APR3096_0_tau_R10 through APR3096_5_tau_alphaEM"),
        ("REF3096_3_local_GR", "local GR recovered", "COUPLING_ROWS_UNSIGNED", "matter/source coupling envelope not theorem-zero or source-bounded"),
    ]
    return with_meta(
        [
            {
                "refusal_id": refusal_id,
                "claim": claim,
                "computed_status": status,
                "runner_result": "BLOCKED",
                "blocking_rows": blocking_rows,
                "claim_allowed_for_physics": False,
            }
            for refusal_id, claim, status, blocking_rows in refusals
        ]
    )


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG3096_0_fixed_spurion", "fixed active markers excluded", True, "partial object-language hygiene supports this limited exclusion", False),
        ("CG3096_1_no_marker_full", "all material/source/readout markers excluded", False, "co-moving material, constants, source weights and boundary/source tails survive", False),
        ("CG3096_2_bound_rows_complete", "frame/marker bound rows numeric and sourced", False, "all component values are still MISSING_*", False),
        ("CG3096_3_projection_rows_complete", "arena projection rows numeric and sourced", False, "tau_R10/tau_PPN/tau_clock/tau_orbital/tau_WEP/tau_alphaEM are missing", False),
        ("CG3096_4_local_GR", "local GR branch passes", False, "coupling rows are neither zero-proven nor source-bounded", False),
    ]
    return with_meta(
        [
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": gate_pass,
                "reason": reason,
                "claim_allowed_for_physics": claim_allowed,
            }
            for gate_id, claim, gate_pass, reason, claim_allowed in gates
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3096_0_partial_win",
                "decision": "3096 proves a useful partial theorem only.",
                "because": "fixed external spurions and empty-background covectors can be excluded, but live matter/source markers remain",
                "next_action": "keep the partial theorem as a guardrail, not as a local-GR claim",
            },
            {
                "decision_id": "DEC3096_1_bound_pack",
                "decision": "The bound input pack is now the clean working object.",
                "because": "c_g, b_dis, b_A, b_alpha, b_marker, delta_kappa_A, q_nonH and support/domain/boundary tails are explicit rows with arenas",
                "next_action": "source or theorem-zero the rows one by one",
            },
            {
                "decision_id": "DEC3096_2_best_route",
                "decision": "Next route should source the first real local coupling bound inputs.",
                "because": "attempting another global no-marker theorem without new parent action clauses will likely loop",
                "next_action": "3097-Y5-R2FR-first-real-local-coupling-bound-source-table-under-AX1090.md",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "NEXT3096_0_primary",
                "next_checkpoint": "3097-Y5-R2FR-first-real-local-coupling-bound-source-table-under-AX1090.md",
                "script": "scripts/Y5_R2FR_first_real_local_coupling_bound_source_table_under_AX1090_3097.py",
                "objective": "source or bound the first real c_g, b_A, b_alpha, q_nonH, support/domain/boundary and arena-projection rows without making a local-GR claim",
                "selection_status": "selected",
                "success_condition": "at least one component row becomes source-backed numeric or theorem-zero while all incomplete rows remain nonclaim",
            },
            {
                "route_id": "NEXT3096_1_parallel",
                "next_checkpoint": "3097b-Y5-R2FR-parent-action-no-marker-clause-signature-under-AX1090.md",
                "script": "scripts/Y5_R2FR_parent_action_no_marker_clause_signature_under_AX1090_3097b.py",
                "objective": "write the exact parent action clauses that would sign full no-marker/constant/source-tail silence",
                "selection_status": "held",
                "success_condition": "parent action explicitly forbids every surviving marker family without post-hoc deletion",
            },
        ]
    )


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = {
        "no_marker_copy": OUTPUTS["no_marker"],
        "bound_pack_copy": OUTPUTS["bound_pack"],
        "arena_copy": OUTPUTS["arena"],
        "decisions_copy": OUTPUTS["decisions"],
        "next_copy": OUTPUTS["next"],
    }
    output_rows = []
    for key, source_path in copies.items():
        target_path = BRANCH_OUTPUTS[key]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        output_rows.append(
            {
                **meta(),
                "copy_id": f"COPY3096_{key}",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
            }
        )
    write_csv(OUTPUTS["branches"], output_rows)
    return output_rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in output_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 3096 Y5 R2FR frame-marker coupling bound input pack or no-marker theorem under AX1090",
        "",
        "**Progress:** 3096 ports the no-marker/frame-marker coupling fork into the current AX1090 branch. It records a partial theorem: fixed external spurions and empty-background linear covectors are bad parent object-language, but co-moving matter markers and common frames remain live.",
        "",
        "**Current verdict:** the full no-marker theorem does not close. The working object is now the claim-blocked frame/marker/source bound pack: `c_g`, `b_dis`, `b_A`, `b_alpha`, `b_marker`, `delta_kappa_A`, `q_nonH`, support/domain/boundary tails, and arena projections.",
        "",
        "**Claim ceiling:** no source-zero claim, finite-alpha pass, R10/WEP/clock/PPN/orbital pass, local-GR/Newton reduction, GitHub action, or `formalization-workbench` edit is allowed from 3096.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"]),
        "",
        "## No-Marker Theorem Attempt",
        markdown_table(data["no_marker"], ["attempt_id", "claim_piece", "formal_statement", "derived_status", "proof_status", "missing_or_blocker", "observable_impact", "valid_for_claim"]),
        "",
        "## Partial No-Marker Theorem",
        markdown_table(data["partial"], ["theorem_id", "theorem", "statement", "proof_sketch", "scope", "what_it_does_not_prove", "status", "claim_allowed", "valid_for_claim"]),
        "",
        "## Surviving Marker Families",
        markdown_table(data["survivors"], ["marker_id", "family", "status_after_3096", "why", "required_bound_or_theorem", "blocks_full_zero_claim", "valid_for_claim"]),
        "",
        "## Frame/Marker Bound Input Pack",
        markdown_table(data["bound_pack"], ["row_id", "symbol", "definition", "formula_or_bound", "current_value", "units", "observable_link", "status", "valid_for_claim"]),
        "",
        "## Arena Projection Rows",
        markdown_table(data["arena"], ["projection_id", "symbol", "arena", "uses_components", "formula_or_contract", "current_value", "units", "status", "valid_for_claim"]),
        "",
        "## qbarXT Total Envelope",
        markdown_table(data["envelope"], ["envelope_id", "quantity", "formula", "rule", "status", "valid_for_claim"]),
        "",
        "## Dependency Links",
        markdown_table(data["dependencies"], ["dependency_id", "quantity", "requires", "status", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Placeholder Refusal Runner",
        markdown_table(data["refusal"], ["refusal_id", "claim", "computed_status", "runner_result", "blocking_rows", "claim_allowed_for_physics", "valid_for_claim"]),
        "",
        "## Claim Gate",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed_for_physics", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "next_checkpoint", "script", "objective", "selection_status", "success_condition"]),
        "",
        "## Validation",
        markdown_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
        "## Working Interpretation",
        "This checkpoint prevents a fake local-GR win. We got a useful object-language guardrail, but the actual local coupling problem now lives in source-backed rows. The next serious move is not another broad theorem loop; it is the first real coupling-bound source table.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def contains_status(path: Path, field: str, expected: str) -> bool:
    return any(str(row.get(field, "")) == expected for row in rows(path))


def all_false(path: Path, field: str) -> bool:
    table = rows(path)
    return bool(table) and all(not boolish(row.get(field, "")) for row in table)


def validation_rows() -> list[dict[str, Any]]:
    formalization_3096 = list(FORMALIZATION.rglob("*3096*")) if FORMALIZATION.exists() else []
    checks = [
        ("VAL3096_00_sources_csv", csv_ok(OUTPUTS["sources"]), "source register parses", OUTPUTS["sources"]),
        ("VAL3096_01_sources_exist", all(boolish(row["exists"]) for row in rows(OUTPUTS["sources"])), "every cited local source path exists", OUTPUTS["sources"]),
        ("VAL3096_02_sources_parse", all(boolish(row["parse_ok"]) for row in rows(OUTPUTS["sources"])), "every cited csv source parses", OUTPUTS["sources"]),
        ("VAL3096_03_needles_present", all(boolish(row["needles_present"]) for row in rows(OUTPUTS["sources"])), "all source needles found", OUTPUTS["sources"]),
        ("VAL3096_04_doc_created", DOC.exists(), "checkpoint markdown created", DOC),
        ("VAL3096_05_no_marker_parse", csv_ok(OUTPUTS["no_marker"]), "no-marker attempt parses", OUTPUTS["no_marker"]),
        ("VAL3096_06_no_marker_blocks", contains_status(OUTPUTS["no_marker"], "proof_status", "NO_MARKER_THEOREM_NOT_CLOSED"), "full no-marker theorem remains nonclaim", OUTPUTS["no_marker"]),
        ("VAL3096_07_partial_parse", csv_ok(OUTPUTS["partial"]), "partial theorem rows parse", OUTPUTS["partial"]),
        ("VAL3096_08_partial_guardrail", contains_status(OUTPUTS["partial"], "status", "GUARDRAIL_ACTIVE"), "partial theorem guardrail active", OUTPUTS["partial"]),
        ("VAL3096_09_survivors_parse", csv_ok(OUTPUTS["survivors"]), "surviving marker family audit parses", OUTPUTS["survivors"]),
        ("VAL3096_10_survivors_block", any(boolish(row["blocks_full_zero_claim"]) for row in rows(OUTPUTS["survivors"])), "surviving families block full zero claim", OUTPUTS["survivors"]),
        ("VAL3096_11_bound_pack_parse", csv_ok(OUTPUTS["bound_pack"]), "bound input pack parses", OUTPUTS["bound_pack"]),
        ("VAL3096_12_bound_pack_nonclaim", contains_status(OUTPUTS["bound_pack"], "status", "CLAIM_BLOCKED") and all_false(OUTPUTS["bound_pack"], "valid_for_claim"), "bound rows remain claim-blocked", OUTPUTS["bound_pack"]),
        ("VAL3096_13_arena_parse", csv_ok(OUTPUTS["arena"]), "arena projection rows parse", OUTPUTS["arena"]),
        ("VAL3096_14_arena_missing", contains_status(OUTPUTS["arena"], "status", "MISSING_ARENA_PROJECTION"), "arena projections remain missing", OUTPUTS["arena"]),
        ("VAL3096_15_envelope_parse", csv_ok(OUTPUTS["envelope"]), "total envelope parses", OUTPUTS["envelope"]),
        ("VAL3096_16_no_cancellation_guard", contains_status(OUTPUTS["envelope"], "status", "GUARDRAIL_ACTIVE"), "no-cancellation guard active", OUTPUTS["envelope"]),
        ("VAL3096_17_dependencies_parse", csv_ok(OUTPUTS["dependencies"]), "dependency links parse", OUTPUTS["dependencies"]),
        ("VAL3096_18_refusal_parse", csv_ok(OUTPUTS["refusal"]), "placeholder refusal runner parses", OUTPUTS["refusal"]),
        ("VAL3096_19_refusal_blocks_local_GR", contains_status(OUTPUTS["refusal"], "claim", "local GR recovered"), "refusal runner blocks local GR claim", OUTPUTS["refusal"]),
        ("VAL3096_20_gates_parse", csv_ok(OUTPUTS["gates"]), "claim gates parse", OUTPUTS["gates"]),
        ("VAL3096_21_local_GR_blocked", contains_status(OUTPUTS["gates"], "claim", "local GR branch passes") and all_false(OUTPUTS["gates"], "claim_allowed_for_physics"), "local GR gate remains blocked", OUTPUTS["gates"]),
        ("VAL3096_22_decisions_parse", csv_ok(OUTPUTS["decisions"]), "decision ledger parses", OUTPUTS["decisions"]),
        ("VAL3096_23_next_parse", csv_ok(OUTPUTS["next"]), "next target parses", OUTPUTS["next"]),
        ("VAL3096_24_next_selected", contains_status(OUTPUTS["next"], "selection_status", "selected"), "primary next target selected", OUTPUTS["next"]),
        ("VAL3096_25_branch_copies_parse", csv_ok(OUTPUTS["branches"]), "branch copy ledger parses", OUTPUTS["branches"]),
        ("VAL3096_26_branch_copies_exist", all(boolish(row["target_exists"]) for row in rows(OUTPUTS["branches"])), "all branch copies exist", OUTPUTS["branches"]),
        ("VAL3096_27_no_formalization_edit", len(formalization_3096) == 0, "no 3096 files created under formalization-workbench", FORMALIZATION),
        ("VAL3096_28_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE),
    ]
    return [
        {
            **meta(),
            "validation_id": validation_id,
            "check_pass": bool(check_pass),
            "detail": detail,
            "artifact": str(artifact),
        }
        for validation_id, check_pass, detail, artifact in checks
    ]


def main() -> None:
    remove_pycache()
    for directory in [RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_rows(),
        "no_marker": no_marker_rows(),
        "partial": partial_rows(),
        "survivors": survivor_rows(),
        "bound_pack": bound_pack_rows(),
        "arena": arena_rows(),
        "envelope": envelope_rows(),
        "dependencies": dependency_rows(),
        "refusal": refusal_rows(),
        "gates": gate_rows(),
        "decisions": decision_rows(),
        "next": next_rows(),
    }

    for key, output_rows in data.items():
        write_csv(OUTPUTS[key], output_rows)

    data["branches"] = copy_branch_outputs()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if boolish(row["check_pass"]))
    print(f"3096 frame/marker bound checkpoint written: {passed}/{len(data['validation'])} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
