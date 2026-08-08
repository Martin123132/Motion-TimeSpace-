from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2683"
BRANCH_ID = "Y5_R2FR_FINITE_SOURCE_PREFACTOR_COEFFICIENT_SOURCE_PACK_OR_THEOREM_ZERO_RETURN_2683"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"

DOC_PATH = ROOT / "2683-Y5-R2FR-finite-source-prefactor-coefficient-source-pack-or-theorem-zero-return.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2683_SOURCE_REGISTER.csv",
    "requirements_audit": RESIDUALS / "P8_Y5_R2FR_2683_SOURCE_PACK_REQUIREMENTS_AUDIT.csv",
    "source_pack": RESIDUALS / "P8_Y5_R2FR_2683_FINITE_COEFFICIENT_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
    "zero_gates": RESIDUALS / "P8_Y5_R2FR_2683_THEOREM_ZERO_RETURN_GATES_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2683_SOURCE_PACK_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2683_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2683_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2683_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2683_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2683_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "microscope_requirements": WEP_COEFF / "source_prefactor_source_pack_requirements_audit_nonclaim_2683.csv",
    "microscope_source_pack": WEP_COEFF / "finite_coefficient_source_pack_template_nonclaim_2683.csv",
    "microscope_zero_gates": WEP_COEFF / "theorem_zero_return_gates_nonclaim_2683.csv",
    "source_weight_source_pack": SOURCE_WEIGHT / "FINITE_SOURCE_PREFACTOR_SOURCE_PACK_TEMPLATE_2683_NONCLAIM.csv",
    "local_bounds_source_pack": LOCAL_BOUNDS / "finite_source_prefactor_source_pack_template_2683_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2683_2682_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2682_NEXT_TARGET.csv",
        "required_needles": ["NEXT2682_0_selected", "source-pack requirements", "no row can be score-ready"],
        "purpose": "confirms selected 2683 target and forbidden shortcuts",
    },
    {
        "source_id": "SRC2683_2682_FINITE_ROWS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2682_FINITE_SOURCE_PREFACTOR_COEFFICIENT_ROWS_NONCLAIM.csv",
        "required_needles": ["FSP2682_0_cIhid", "FSP2682_4_total_envelope", "ACQUISITION_TEMPLATE_NONCLAIM"],
        "purpose": "imports finite coefficient rows and the total envelope",
    },
    {
        "source_id": "SRC2683_DELTA_W1476",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/Ci_source_weight_delta_w_input_nonclaim_1476.csv",
        "required_needles": ["DW1476_0_delta_w_A", "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W", "TAQ1067_2_delta_w_width_if_tau"],
        "purpose": "keeps Delta_w source row blocked unless theorem-zero or source-backed numeric input appears",
    },
    {
        "source_id": "SRC2683_COUNTERMODELS2676",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/action_scale_measure_owner_countermodels_nonclaim_2676.csv",
        "required_needles": ["CM2676_0_species_action_weight", "CM2676_2_pre_variation_source_rescaling", "COUNTERMODEL_RETAINED_NONCLAIM"],
        "purpose": "imports active source-prefactor countermodels",
    },
    {
        "source_id": "SRC2683_CURRENT1453",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv",
        "required_needles": ["CSO1453_4_post_variation_rescaling", "CSO1453_5_pre_variation_weight", "CSO1453_7_verdict"],
        "purpose": "imports the post/pre-current split",
    },
    {
        "source_id": "SRC2683_QLOC1816_SCHEMA",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1816_POST_CURRENT_CA_ROW_SCHEMA.csv",
        "required_needles": ["PCR1816_0_cA_post", "MISSING_READOUT_ORDER_THEOREM_OR_C_A_VALUE", "PCR1816_4_total"],
        "purpose": "imports the post-current/readout-order residual schema",
    },
    {
        "source_id": "SRC2683_QLOC1816_ACCEPTANCE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1816_ACCEPTANCE_GATE.csv",
        "required_needles": ["AC1816_1_order_parent_signed", "AC1816_3_residual_values", "BLOCKED"],
        "purpose": "imports the readout-order acceptance blockage",
    },
    {
        "source_id": "SRC2683_TYPED1470",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv",
        "required_needles": ["TNG1470_3_no_extension", "TNG1470_4_radiative_limit", "NOT_PARENT_DERIVED_START_SOURCE_FILL"],
        "purpose": "imports no-extension and radiative/readout closure blockers",
    },
    {
        "source_id": "SRC2683_MOMS1486",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv",
        "required_needles": ["MOMS1088_4_no_species_weights", "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED", "MOMS1088_7_verdict"],
        "purpose": "imports parent ordinary-matter signature blockers",
    },
    {
        "source_id": "SRC2683_RAD1471",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_radiative_readout_signing_decision_1471.csv",
        "required_needles": ["SIGN1471_0_radiative_readout", "REFUSE_RADIATIVE_READOUT_PROMOTION_FILL_PREDICTION_DEFINITIONS_NONCLAIM", "numeric MTS prediction components are missing"],
        "purpose": "keeps radiative/readout promotion refused",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def requirements_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "SPRA2683_0_contract",
            "requirement": "finite source-prefactor rows need a source pack before scoring",
            "mathematical_contract": "epsilon_prefactor_total is evaluable only after each occupant is theorem-zero or source-backed with units and arena projection",
            "current_status": "REQUIREMENTS_WRITTEN_NONCLAIM",
            "blocks_claim_because": "2682 finite rows are real loophole placeholders, not numeric theory values",
            "required_inputs": "coefficient value or zero theorem; units; sign convention; source path; K_pref; tau_arena; common normalizer; no-cancellation guard",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2682_NEXT_TARGET.csv")),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "emit source-pack template and refuse scoring until filled",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "SPRA2683_1_no_bound_inversion",
            "requirement": "experimental bounds cannot be used as MTS coefficient predictions",
            "mathematical_contract": "a WEP/R10/clock/PPN bound may constrain a predicted row but cannot define Delta_w_AB, c_A or C_eff",
            "current_status": "BOUND_INVERSION_FORBIDDEN",
            "blocks_claim_because": "using eta_R10 or eta_WEP as a theory value would be circular",
            "required_inputs": "independent parent coefficient, independent source integral, or parent theorem-zero",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/Ci_source_weight_delta_w_input_nonclaim_1476.csv")),
            "gate_pass": "true",
            "valid_for_claim": "false",
            "next_action": "treat bound-derived widths as diagnostic only",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "SPRA2683_2_common_normalizer",
            "requirement": "all finite coefficients need one common source normalizer",
            "mathematical_contract": "abs(epsilon_total) >= sum_i abs(epsilon_i) is meaningful only after every epsilon_i is expressed in the same dimensionless source fraction",
            "current_status": "COMMON_NORMALIZER_MISSING",
            "blocks_claim_because": "adding c(I_hid), Delta_w_AB, c_A/kappa_A and C_eff_tail without a shared normalization is not dimensional evidence",
            "required_inputs": "source_norm definition; units conversion; arena-specific denominator; coefficient-to-observable map",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1816_POST_CURRENT_CA_ROW_SCHEMA.csv")),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "derive or define a common source-normalized residual basis",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "SPRA2683_3_arena_projection",
            "requirement": "each coefficient needs K_pref and tau_arena before comparison to data",
            "mathematical_contract": "observable residual = K_pref(arena, coefficient) * tau_arena * epsilon_i plus declared boundary/readout terms",
            "current_status": "ARENA_PROJECTION_MATRIX_MISSING",
            "blocks_claim_because": "a coefficient row is not yet a WEP/R10/PPN/clock/orbital prediction",
            "required_inputs": "arena; test body/source; projection kernel; sign convention; units; source path",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1816_ACCEPTANCE_GATE.csv")),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "build a projection matrix before any local-test score",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "SPRA2683_4_no_cancellation_guard",
            "requirement": "finite branch must be absolute-envelope, not cancellation tuned",
            "mathematical_contract": "score with abs(epsilon_total) >= abs(cIhid)+abs(Delta_w)+abs(cA_pre/kappa_A)+abs(Ceff_tail)",
            "current_status": "NO_CANCELLATION_ENVELOPE_REQUIRED_NOT_COMPUTED",
            "blocks_claim_because": "opposite signs cannot rescue local tests unless each absolute component is bounded or zero",
            "required_inputs": "all component magnitudes in common normalizer; proof of nonnegative envelope convention",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2682_FINITE_SOURCE_PREFACTOR_COEFFICIENT_ROWS_NONCLAIM.csv")),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "keep every source-pack row nonclaim until the envelope closes",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "SPRA2683_5_theorem_zero_return",
            "requirement": "source pack can be bypassed only by parent theorem-zero",
            "mathematical_contract": "all finite source-prefactor occupants vanish if the parent action language has no source-prefactor target, no hidden scalar coefficient target, and no readout/radiative extension",
            "current_status": "THEOREM_ZERO_RETURN_OPEN_NOT_SIGNED",
            "blocks_claim_because": "the cleanest route is still conditional and lacks parent signatures",
            "required_inputs": "target absence; hidden invariant algebra triviality; line owner; variation order; no non-Hilbert bypass; no readout extension",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/MOMS_parent_signature_source_map_nonclaim_1486.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/typed_visible_action_grammar_attempt_1470.csv")),
                ]
            ),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "keep theorem-zero as parallel derivation route",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "SPRA2683_6_verdict",
            "requirement": "finite source-prefactor source pack sufficient for local claim",
            "mathematical_contract": "local GR/WEP/R10/PPN/clock/orbital claim requires either all zero gates true or all finite rows source-backed and projected",
            "current_status": "SOURCE_PACK_INCOMPLETE_BRANCH_BLOCKED",
            "blocks_claim_because": "zero gates and finite source inputs are both unsigned",
            "required_inputs": "complete template rows or theorem-zero closure",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_Y5_R2FR_2682_FINITE_SOURCE_PREFACTOR_COEFFICIENT_ROWS_NONCLAIM.csv")),
            "gate_pass": "false",
            "valid_for_claim": "false",
            "next_action": "move to arena projection matrix or theorem-zero return",
            "timestamp_utc": stamp(),
        },
    ]


def source_pack_rows() -> list[dict[str, Any]]:
    base = [
        (
            "SP2683_0_cIhid",
            "c(I_hid)",
            "hidden scalar source-prefactor",
            "hidden invariant algebra triviality or parent target-absence theorem",
            "finite independent source coefficient c(I_hid), not WEP/R10 inverted",
            "dimensionless_source_fraction",
            "positive envelope magnitude abs(c(I_hid))",
            "WEP;R10;clock;PPN;local-GR",
            "MISSING_PARENT_ZERO_OR_NUMERIC_SOURCE_COEFFICIENT",
            "prove hidden algebra triviality or source finite c(I_hid) row",
        ),
        (
            "SP2683_1_Delta_w_AB",
            "Delta_w_AB",
            "pre-action species/source weight",
            "action-line owner plus no source-prefactor target theorem",
            "finite Delta_w_AB vector from parent/source model independent of WEP bound",
            "dimensionless_source_fraction",
            "positive envelope magnitude abs(Delta_w_AB)",
            "WEP;Newton-source;R10;local-GR",
            "MISSING_THEOREM_ZERO_OR_NUMERIC_DELTA_W",
            "derive no species weights or fill source-backed Delta_w row",
        ),
        (
            "SP2683_2_cA_pre_kappa_A",
            "c_A_pre or kappa_A",
            "pre-current/source normalization scalar",
            "variation-before-readout plus no pre-current source slot theorem",
            "finite pre-current c_A/kappa_A row after source-normalizer split",
            "dimensionless_current_fraction",
            "positive envelope magnitude abs(c_A_pre/kappa_A)",
            "WEP;PPN;clock;source-normalization",
            "MISSING_READOUT_ORDER_THEOREM_OR_C_A_VALUE",
            "derive readout-order/source-slot theorem or fill c_A_pre row",
        ),
        (
            "SP2683_3_Ceff_tail",
            "C_eff_source_tail",
            "readout/radiative source-prefactor tail",
            "no-extension and radiative/readout closure theorem",
            "finite tail coefficient with cutoff/readout/source path and units",
            "declared_effective_source_fraction",
            "positive envelope magnitude abs(C_eff_source_tail)",
            "EM;clock;R10;WEP",
            "MISSING_NO_EXTENSION_OR_NUMERIC_TAIL",
            "derive no-extension/radiative closure or fill finite tail row",
        ),
        (
            "SP2683_4_total_envelope",
            "epsilon_prefactor_total",
            "absolute no-cancellation envelope",
            "all components theorem-zero",
            "sum of absolute source-normalized component magnitudes",
            "dimensionless_common_source_fraction",
            "abs(total) >= sum abs(component)",
            "all local source arenas",
            "MISSING_COMPONENT_VALUES_AND_COMMON_NORMALIZER",
            "compute only after all component rows are zero or source-backed",
        ),
        (
            "SP2683_5_arena_product",
            "K_pref * tau_arena * epsilon_prefactor_total",
            "future observable projection",
            "projection silence theorem for the arena",
            "source-backed K_pref and tau_arena with units/sign/source path",
            "arena_declared",
            "absolute observable residual bound",
            "WEP;R10;PPN;clock;orbital",
            "MISSING_ARENA_PROJECTION_MATRIX",
            "build arena projection matrix before testing",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for row in base:
        rows.append(
            {
                "pack_id": row[0],
                "symbol": row[1],
                "coefficient_role": row[2],
                "required_theory_zero_input": row[3],
                "required_finite_numeric_input": row[4],
                "units": row[5],
                "sign_convention": row[6],
                "arena_links": row[7],
                "source_path_required": "true",
                "arena_projection_required": "true",
                "common_normalizer_required": "true",
                "no_cancellation_guard_required": "true",
                "independent_of_bound_inversion": "true",
                "current_status": row[8],
                "score_ready": "false",
                "valid_for_claim": "false",
                "claim_allowed": "false",
                "next_action": row[9],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def zero_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TZ2683_0_source_prefactor_target_absent",
            "Coeff_source-prefactor absent from parent object language",
            "forbids w_A, c_A, kappa_A and c(I_hid) as source multipliers before variation",
            "SOURCE_PREFACTOR_TARGET_ABSENCE_NOT_PARENT_SIGNED",
            "P8_Y5_R2FR_2682_SOURCE_PREFACTOR_TARGET_NORMAL_FORM_AUDIT.csv",
        ),
        (
            "TZ2683_1_hidden_invariant_algebra_trivial",
            "hidden invariant algebra gives no nonconstant scalar coefficient c(I_hid)",
            "kills hidden scalar source-prefactor target without fitting",
            "HIDDEN_SCALAR_TRIVIALITY_NOT_SIGNED",
            "P8_Y5_R2FR_2681_SOURCE_PREFACTOR_RESIDUAL_ROWS_NONCLAIM.csv",
        ),
        (
            "TZ2683_2_action_line_owner",
            "one parent action-density line owns ordinary matter source normalization",
            "kills relative species/source weights Delta_w_AB",
            "ACTION_LINE_OWNER_NOT_PARENT_SIGNED",
            "P8_Y5_R2FR_2679_LINE_OWNER_THEOREM_CONTRACT_NONCLAIM.csv",
        ),
        (
            "TZ2683_3_variation_before_readout",
            "Hilbert/source current is extracted before readout or material selectors",
            "kills post-current c_A as a parent-source redefinition",
            "VARIATION_BEFORE_READOUT_NOT_JOINTLY_SIGNED",
            "P8_Y5_PARENT_QLOC_1816_ACCEPTANCE_GATE.csv",
        ),
        (
            "TZ2683_4_no_nonHilbert_bypass",
            "non-Hilbert, torsion, boundary or shadow currents are absent/exact/projected silent",
            "prevents zeta_A and source-current bypass rows",
            "NONHILBERT_BYPASS_NOT_CLOSED",
            "current_source_normalization_owner_theorem_attempt_1453.csv",
        ),
        (
            "TZ2683_5_no_readout_radiative_extension",
            "effective/readout/radiative maps cannot enlarge the source coefficient domain",
            "kills C_eff_source_tail",
            "NO_EXTENSION_AND_RADIATIVE_CLOSURE_NOT_SIGNED",
            "typed_visible_action_grammar_attempt_1470.csv",
        ),
        (
            "TZ2683_6_common_projection_silence",
            "common normalizer and arena projections carry no independent source charge",
            "lets zero proof survive WEP/R10/PPN/clock/orbital readout",
            "ARENA_PROJECTION_SILENCE_NOT_SIGNED",
            "P8_Y5_PARENT_QLOC_1816_POST_CURRENT_CA_ROW_SCHEMA.csv",
        ),
        (
            "TZ2683_7_verdict",
            "all theorem-zero clauses close",
            "would demote the finite source-pack branch to unnecessary bookkeeping",
            "THEOREM_ZERO_NOT_PROVED_RETURN_TO_SOURCE_PACK_OR_PROJECTION",
            "P8_Y5_R2FR_2683_THEOREM_ZERO_RETURN_GATES_NONCLAIM.csv",
        ),
    ]
    return [
        {
            "gate_id": gate_id,
            "zero_clause": clause,
            "if_signed_effect": effect,
            "current_status": status,
            "source_anchor": anchor,
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive this clause or keep finite source-pack row live",
            "timestamp_utc": stamp(),
        }
        for gate_id, clause, effect, status, anchor in rows
    ]


def runner_rows(source_pack: list[dict[str, Any]], zero_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in source_pack:
        missing_numeric = row["current_status"].startswith("MISSING")
        rows.append(
            {
                "runner_id": f"RUN2683_{row['pack_id']}",
                "target_id": row["pack_id"],
                "runner_stage": "finite_source_pack",
                "zero_available": "false",
                "numeric_source_backed": "false",
                "projection_available": "false" if row["arena_projection_required"] == "true" else "n/a",
                "common_normalizer_available": "false",
                "bound_inversion_used": "false",
                "missing_blocker": row["current_status"] if missing_numeric else "MISSING_SOURCE_PACK_CLOSURE",
                "score_ready": "false",
                "valid_for_claim": "false",
                "runner_verdict": "REFUSE_SCORE_UNSIGNED_SOURCE_PACK_ROW",
                "timestamp_utc": stamp(),
            }
        )
    unsigned_zero_gates = [row["gate_id"] for row in zero_gates if row["parent_signed"] != "true"]
    rows.append(
        {
            "runner_id": "RUN2683_THEOREM_ZERO_VERDICT",
            "target_id": "theorem_zero_return",
            "runner_stage": "theorem_zero_gates",
            "zero_available": "false",
            "numeric_source_backed": "n/a",
            "projection_available": "false",
            "common_normalizer_available": "false",
            "bound_inversion_used": "false",
            "missing_blocker": ";".join(unsigned_zero_gates),
            "score_ready": "false",
            "valid_for_claim": "false",
            "runner_verdict": "THEOREM_ZERO_NOT_PROVED",
            "timestamp_utc": stamp(),
        }
    )
    rows.append(
        {
            "runner_id": "RUN2683_BOUND_INVERSION_GUARD",
            "target_id": "all_finite_rows",
            "runner_stage": "circularity_guard",
            "zero_available": "n/a",
            "numeric_source_backed": "false",
            "projection_available": "n/a",
            "common_normalizer_available": "n/a",
            "bound_inversion_used": "false",
            "missing_blocker": "WEP_R10_BOUND_INVERSION_FORBIDDEN_AS_THEORY_INPUT",
            "score_ready": "false",
            "valid_for_claim": "false",
            "runner_verdict": "PASS_GUARD_BUT_REFUSE_CLAIM",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2683_0_source_pack_complete",
            "gate": "all finite source-prefactor coefficients source-backed or zero-certified",
            "current_status": "FAIL",
            "reason": "every component remains missing a parent zero or finite source-backed value",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2683_1_projection_matrix_complete",
            "gate": "K_pref and tau_arena available for WEP/R10/PPN/clock/orbital",
            "current_status": "FAIL",
            "reason": "arena projection matrix is not derived or sourced",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2683_2_no_bound_inversion",
            "gate": "no experimental bound is reused as an MTS prediction value",
            "current_status": "PASS_GUARD_ONLY",
            "reason": "the runner refuses WEP/R10 bound inversion and keeps rows nonclaim",
            "gate_pass": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2683_3_theorem_zero_closed",
            "gate": "the parent theorem-zero route closes every source-prefactor occupant",
            "current_status": "FAIL",
            "reason": "target absence, line owner, hidden-scalar triviality and readout closure remain unsigned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2683_4_local_GR_or_WEP_claim",
            "gate": "local GR/WEP/R10/PPN/clock/orbital promotion",
            "current_status": "REFUSED",
            "reason": "2683 is a source-pack gate only; no local claim is available",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2683_0_private_verdict",
            "decision": "SOURCE_PACK_TEMPLATE_WRITTEN_NONCLAIM",
            "rationale": "the coupling gap is now a finite checklist rather than a vague problem",
            "claim_allowed": "false",
            "next_action": "build arena projection matrix or return to theorem-zero clauses",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2683_1_no_shortcut",
            "decision": "DO_NOT_SCORE_FROM_WEP_OR_R10_BOUND_INVERSION",
            "rationale": "bounds can constrain predictions but cannot manufacture MTS coupling coefficients",
            "claim_allowed": "false",
            "next_action": "keep source values independent or theorem-derived",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2683_2_best_route",
            "decision": "NEXT_ATTACK_ARENA_PROJECTION_MATRIX_WITH_THEOREM_ZERO_ESCAPE_HATCH",
            "rationale": "even if a finite coefficient is later found, it cannot be compared to data without K_pref, tau_arena and common normalization",
            "claim_allowed": "false",
            "next_action": "2684 source-prefactor arena projection matrix or theorem-zero return",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2683_0_selected",
            "kind": "selected",
            "target_doc": "2684-Y5-R2FR-source-prefactor-arena-projection-matrix-or-theorem-zero-return.md",
            "target_script": "scripts/Y5_R2FR_source_prefactor_arena_projection_matrix_or_theorem_zero_return_2684.py",
            "purpose": "derive or stage K_pref and tau_arena for WEP, R10, PPN, clocks and orbital tests for each finite source-prefactor coefficient, while keeping parent theorem-zero as the cleaner escape hatch",
            "acceptance_gate": "every arena row declares observable, units, sign convention, source path, common normalizer and no-cancellation role; no row is claim-ready from experimental-bound inversion",
            "forbidden_shortcuts": "using WEP/R10 bounds as coefficient values; setting Delta_w=0 by preference; promoting c_A_post to c_A_pre; assuming readout/radiative tails vanish; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STATUS2683_0_coupling_gap",
            "sector": "local coupling / GR-reduction spine",
            "status": "COUPLING_GAP_FINITE_BUT_OPEN",
            "meaning": "the live obstacle is no longer mysterious: it is a finite source-prefactor coefficient pack plus arena projections, unless theorem-zero closes",
            "claim_allowed": "false",
            "next_action": "run 2684 projection matrix gate",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2683_1_derivation_route",
            "sector": "parent action theorem",
            "status": "THEOREM_ZERO_ROUTE_CLEAN_BUT_UNSIGNED",
            "meaning": "a parent no-source-prefactor/no-extension theorem would be stronger than finite fitting, but the clauses are not yet signed",
            "claim_allowed": "false",
            "next_action": "keep theorem-zero gates as parallel derivation targets",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "STATUS2683_2_testing_route",
            "sector": "WEP/R10/PPN/clock/orbital",
            "status": "TESTING_NOT_READY_FROM_THIS_BRANCH",
            "meaning": "testing needs projection kernels and independent coefficient values before comparison to data",
            "claim_allowed": "false",
            "next_action": "do not run public-style local-test claims from 2683",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, path in BRANCH_OUTPUTS.items():
        rows.append(
            {
                "copy_id": f"BC2683_{name}",
                "absolute_path": str(path),
                "relative_path": rel_path(path),
                "exists": as_bool(path.exists()),
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def validation_rows(all_outputs: dict[str, Path], branch_outputs: dict[str, Path], source_rows: list[dict[str, Any]], source_pack: list[dict[str, Any]], zero_gates: list[dict[str, Any]], runner: list[dict[str, Any]], claim_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output_paths = list(all_outputs.values()) + list(branch_outputs.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    source_pack_nonclaim = all(row["valid_for_claim"] == "false" and row["score_ready"] == "false" and row["independent_of_bound_inversion"] == "true" for row in source_pack)
    blockers_present = all(row["current_status"].startswith("MISSING") for row in source_pack)
    zero_nonclaim = all(row["parent_signed"] == "false" and row["claim_allowed"] == "false" for row in zero_gates)
    runner_refuses = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in runner)
    claim_blocked = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_gates)
    guard_pass_only = any(row["gate_id"] == "CG2683_2_no_bound_inversion" and row["gate_pass"] == "true" and row["claim_allowed"] == "false" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(all_outputs.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in branch_outputs.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2684" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2683_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2683_source_pack_nonclaim", source_pack_nonclaim, "source-pack rows remain nonclaim and independent of bound inversion"),
        ("VAL2683_missing_blockers_retained", blockers_present, "every finite source-pack row has an explicit MISSING blocker"),
        ("VAL2683_zero_gates_nonclaim", zero_nonclaim, "theorem-zero gates remain unsigned/nonclaim"),
        ("VAL2683_runner_refuses_unsigned_rows", runner_refuses, "runner refuses every unsigned source-pack row"),
        ("VAL2683_claim_gates_block_claims", claim_blocked, "all claim gates block promotion"),
        ("VAL2683_bound_inversion_guard", guard_pass_only, "bound-inversion guard passes only as a refusal rule"),
        ("VAL2683_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2683_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2683_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2683_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2683_next_target_selected", next_target_ok, "2684 projection/theorem-zero target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {
            "check_id": check_id,
            "passed": as_bool(ok),
            "detail": detail,
            "timestamp_utc": stamp(),
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2683_OVERALL",
            "passed": as_bool(overall),
            "detail": "2683 turns the coupling problem into a strict nonclaim source pack and selects the arena-projection/theorem-zero gate next",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(source_rows: list[dict[str, Any]], requirements: list[dict[str, Any]], source_pack: list[dict[str, Any]], zero_gates: list[dict[str, Any]], runner: list[dict[str, Any]], claim_gates: list[dict[str, Any]], decisions: list[dict[str, Any]], next_target: list[dict[str, Any]], status: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2683 — Y5/R2FR Finite Source-Prefactor Coefficient Source Pack or Theorem-Zero Return",
                "",
                "## Private Verdict",
                "",
                "The coupling gap is now finite and explicit, not foggy. The live objects are `c(I_hid)`, `Delta_w_AB`, `c_A_pre/kappa_A`, `C_eff_source_tail`, their absolute no-cancellation envelope, and the arena product `K_pref * tau_arena * epsilon_prefactor_total`.",
                "",
                "No local-GR, WEP, R10, PPN, clock, orbital, or Newton-source claim is allowed here. The result is a strict source-pack contract plus a theorem-zero return ledger.",
                "",
                "The clean derivation route is still preferred: prove the parent action has no source-prefactor target/no extension. If that fails, finite rows must be independently sourced and projected; experimental bounds cannot be inverted into theory coefficients.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Source-Pack Requirements Audit",
                "",
                markdown_table(requirements),
                "",
                "## Finite Coefficient Source-Pack Template",
                "",
                markdown_table(source_pack),
                "",
                "## Theorem-Zero Return Gates",
                "",
                markdown_table(zero_gates),
                "",
                "## Source-Pack Runner Results",
                "",
                markdown_table(runner),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    requirements = requirements_audit_rows()
    source_pack = source_pack_rows()
    zero_gates = zero_gate_rows()
    runner = runner_rows(source_pack, zero_gates)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["requirements_audit"], requirements)
    write_csv(OUTPUTS["source_pack"], source_pack)
    write_csv(OUTPUTS["zero_gates"], zero_gates)
    write_csv(OUTPUTS["runner_results"], runner)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["microscope_requirements"], requirements)
    write_csv(BRANCH_OUTPUTS["microscope_source_pack"], source_pack)
    write_csv(BRANCH_OUTPUTS["microscope_zero_gates"], zero_gates)
    write_csv(BRANCH_OUTPUTS["source_weight_source_pack"], source_pack)
    write_csv(BRANCH_OUTPUTS["local_bounds_source_pack"], source_pack)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(OUTPUTS, BRANCH_OUTPUTS, source_rows, source_pack, zero_gates, runner, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, requirements, source_pack, zero_gates, runner, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
