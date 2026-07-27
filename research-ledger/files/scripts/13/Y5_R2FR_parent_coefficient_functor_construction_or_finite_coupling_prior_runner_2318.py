from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_COEFFICIENT_FUNCTOR_OR_FINITE_COUPLING_RUNNER_2318"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2318-Y5-R2FR-parent-coefficient-functor-construction-or-finite-coupling-prior-runner.md"

PATHS = {
    "2317_doc": ROOT / "2317-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior.md",
    "2317_validation": OUT / "P8_Y5_BRR545_2317_VALIDATION.csv",
    "2317_theorem": OUT / "P8_Y5_PARENT_QLOC_2317_NO_HIDDEN_VISIBLE_HOM_THEOREM_ATTEMPT.csv",
    "2317_priors": OUT / "P8_Y5_PARENT_QLOC_2317_FINITE_COUPLING_PRIOR_INTERFACE.csv",
    "1219_validation": OUT / "P8_Y5_BRR545_1219_VALIDATION.csv",
    "1219_functor": OUT / "P8_Y5_R10_1219_TYPED_VISIBLE_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
    "1219_counter": OUT / "P8_Y5_R10_1219_HIDDEN_SCALAR_COUNTEREXAMPLE_LOCK.csv",
    "1050_product": OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
    "1050_obstructions": OUT / "P8_Y5_R10_1050_PRODUCT_FUNCTOR_OBSTRUCTION_LEDGER.csv",
    "1050_visible": OUT / "P8_Y5_R10_1050_VISIBLE_ALGEBRA_AUDIT.csv",
    "1051_no_mixed": OUT / "P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
    "1051_scalar": OUT / "P8_Y5_R10_1051_INVARIANT_SCALAR_OBSTRUCTION_AUDIT.csv",
    "1066_operator_domain": OUT / "P8_Y5_R10_1066_OPERATOR_DOMAIN_RULE_AUDIT.csv",
    "1091_theorem": OUT / "P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
    "1479_prefactor": OUT / "P8_Y5_R10_1479_NO_SOURCE_ONLY_ACTION_PREFACTOR_TYPING_THEOREM_ATTEMPT.csv",
    "1479_hom": OUT / "P8_Y5_R10_1479_HOM_SPECIES_TO_SOURCE_PREFACTOR_AUDIT.csv",
    "1489_hom": OUT / "P8_Y5_R10_1489_NO_SOURCE_ONLY_HOM_EXCLUSION_THEOREM_ATTEMPT.csv",
    "1489_target": OUT / "P8_Y5_R10_1489_TYPED_COEFFICIENT_TARGET_AUDIT.csv",
    "1489_delta_w": OUT / "P8_Y5_R10_1489_DELTA_W_BOUND_INTERFACE_NONCLAIM.csv",
    "1490_source_target": OUT / "P8_Y5_R10_1490_SOURCE_COEFFICIENT_TARGET_EXCLUSION_ATTEMPT.csv",
    "1490_delta_w": OUT / "P8_Y5_R10_1490_DELTA_W_REAL_INPUT_REQUIREMENTS.csv",
    "1092_doc": ROOT / "1092-Y5-R10-hidden-invariant-algebra-triviality-or-balpha-tau-projection.md",
    "2200_doc": ROOT / "2200-Y5-R2FR-hidden-invariant-algebra-triviality-or-PPN-vector-source-row.md",
}

SOURCES = [
    ("SRC2318_00_2317_doc", "2317_doc", PATHS["2317_doc"], ["NEXT2317_0", "parent coefficient functor"], "2317 handoff to parent coefficient functor construction"),
    ("SRC2318_01_2317_validation", "2317_validation", PATHS["2317_validation"], ["VAL2317_OVERALL", "PASS"], "2317 validation"),
    ("SRC2318_02_2317_theorem", "2317_theorem", PATHS["2317_theorem"], ["NHVH2317_5_verdict", "NO_HIDDEN_VISIBLE_HOM_NOT_PARENT_DERIVED"], "no-hidden-visible-Hom theorem verdict"),
    ("SRC2318_03_2317_priors", "2317_priors", PATHS["2317_priors"], ["FCP2317_6_claim_gate", "NONCLAIM_REQUIREMENTS_ONLY"], "finite coupling prior interface"),
    ("SRC2318_04_1219_validation", "1219_validation", PATHS["1219_validation"], ["VAL1219_16_overall", "PASS"], "typed functor checkpoint validation"),
    ("SRC2318_05_1219_functor", "1219_functor", PATHS["1219_functor"], ["TVC1219_6_verdict", "TYPED_VISIBLE_COEFFICIENT_FUNCTOR_NOT_DERIVED"], "typed visible coefficient functor attempt"),
    ("SRC2318_06_1219_counter", "1219_counter", PATHS["1219_counter"], ["HSC1219_0_generic_scalar", "LOCKED_AS_ACTIVE_COUNTEREXAMPLE"], "hidden scalar counterexample lock"),
    ("SRC2318_07_1050_product", "1050_product", PATHS["1050_product"], ["PFT1050_5_verdict", "FAIL_CURRENT_CLAIM_PRIOR_WIDTH_PACK_REQUIRED"], "visible-hidden product functor attempt"),
    ("SRC2318_08_1050_obstructions", "1050_obstructions", PATHS["1050_obstructions"], ["OBS1050_0_scalar_invariant", "any surviving nonconstant local invariant scalar"], "product functor obstruction ledger"),
    ("SRC2318_09_1050_visible", "1050_visible", PATHS["1050_visible"], ["VA1050_4_source", "BLOCKED"], "visible algebra audit"),
    ("SRC2318_10_1051_no_mixed", "1051_no_mixed", PATHS["1051_no_mixed"], ["NMM1051_5_verdict", "FAIL_CURRENT_CLAIM_FIRST_PRIOR_CHAIN_REQUIRED"], "no mixed morphism lemma attempt"),
    ("SRC2318_11_1051_scalar", "1051_scalar", PATHS["1051_scalar"], ["ISO1051_0_hidden_scalar_I", "OBSTRUCTION_PROVED_IF_I_SURVIVES"], "hidden scalar obstruction audit"),
    ("SRC2318_12_1066_operator_domain", "1066_operator_domain", PATHS["1066_operator_domain"], ["ODR1066_4_verdict", "EXACT_RULE_NOT_DERIVED"], "operator-domain source scalar exclusion"),
    ("SRC2318_13_1091_theorem", "1091_theorem", PATHS["1091_theorem"], ["ODH1091_6_verdict", "THEOREM_NOT_DERIVED_CURRENT_CORPUS"], "operator-domain theorem attempt"),
    ("SRC2318_14_1479_prefactor", "1479_prefactor", PATHS["1479_prefactor"], ["NST1479_4_verdict", "PROOF_NOT_CLOSED_BOUND_PACK_REQUIRED"], "source-only prefactor typing theorem"),
    ("SRC2318_15_1479_hom", "1479_hom", PATHS["1479_hom"], ["HOM1479_2_hidden_invariant_to_prefactor", "OBSTRUCTION_SURVIVES"], "Hom species/hidden to source prefactor audit"),
    ("SRC2318_16_1489_hom", "1489_hom", PATHS["1489_hom"], ["HET1489_6_verdict", "NOT_DERIVED_DELTA_W_INTERFACE_BUILT"], "no source-only Hom exclusion theorem"),
    ("SRC2318_17_1489_target", "1489_target", PATHS["1489_target"], ["CTA1489_6_verdict", "EXACT_RULE_NOT_DERIVED"], "typed coefficient target audit"),
    ("SRC2318_18_1489_delta_w", "1489_delta_w", PATHS["1489_delta_w"], ["DWI1489_6_claim_gate", "NONCLAIM_INTERFACE_ONLY"], "delta_w bound interface"),
    ("SRC2318_19_1490_source_target", "1490_source_target", PATHS["1490_source_target"], ["SCT1490_5_verdict", "NOT_DERIVED_BOUND_INPUT_ROUTE_SELECTED"], "source coefficient target exclusion attempt"),
    ("SRC2318_20_1490_delta_w", "1490_delta_w", PATHS["1490_delta_w"], ["DWR1490_6_claim_gate", "MISSING_SOURCE_BACKED_VALUE"], "real delta_w input requirements"),
    ("SRC2318_21_1092_doc", "1092_doc", PATHS["1092_doc"], ["b_alpha*tau_clock_time", "source-backed nonclaim product bound"], "best existing clock product fallback"),
    ("SRC2318_22_2200_doc", "2200_doc", PATHS["2200_doc"], ["PPN vector source row", "NONCLAIM_VECTOR_TARGET"], "local-GR-facing vector-source fallback"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2318_SOURCE_REGISTER.csv",
    "construction": OUT / "P8_Y5_PARENT_QLOC_2318_PARENT_COEFFICIENT_FUNCTOR_CONSTRUCTION_ATTEMPT.csv",
    "targets": OUT / "P8_Y5_PARENT_QLOC_2318_COEFFICIENT_TARGET_CATEGORY_AUDIT.csv",
    "obligations": OUT / "P8_Y5_PARENT_QLOC_2318_FUNCTOR_PROOF_OBLIGATION_LEDGER.csv",
    "schema": OUT / "P8_Y5_PARENT_QLOC_2318_FINITE_COUPLING_PRIOR_RUNNER_SCHEMA.csv",
    "smoke": OUT / "P8_Y5_PARENT_QLOC_2318_FINITE_COUPLING_PRIOR_RUNNER_SMOKE_NONCLAIM.csv",
    "arena": OUT / "P8_Y5_PARENT_QLOC_2318_ARENA_ACCEPTANCE_GATES.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2318_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2318_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2318_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2318_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2318_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2318_0_construction", OUTPUTS["construction"], RAB_QUEUE / "JR2318_PARENT_COEFFICIENT_FUNCTOR_CONSTRUCTION_NONCLAIM.csv"),
    ("COPY2318_1_runner_schema", OUTPUTS["schema"], RAB_QUEUE / "JR2318_FINITE_COUPLING_PRIOR_RUNNER_SCHEMA_NONCLAIM.csv"),
    ("COPY2318_2_runner_smoke", OUTPUTS["smoke"], RAB_QUEUE / "JR2318_FINITE_COUPLING_PRIOR_RUNNER_SMOKE_NONCLAIM.csv"),
    ("COPY2318_3_arena_beta", OUTPUTS["arena"], BETA_DOCS / "PARENT_COEFFICIENT_FUNCTOR_ARENA_GATES_2318_NONCLAIM.csv"),
    ("COPY2318_4_arena_wep", OUTPUTS["arena"], MICRO_RESIDUALS / "parent_coefficient_functor_arena_gates_nonclaim_2318.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing_needles = [needle for needle in needles if needle not in text]
    if missing_needles:
        return False, "missing_needles=" + ";".join(missing_needles)
    return True, "all_needles_found"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        needles_found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(needles_found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_construction_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCF2318_0_candidate_functor",
            "claim_piece": "parent coefficient functor object",
            "formal_statement": "Define p_vis=(q_loc, pi_rep, pi_top, Level_EM) and F_coeff: O_vis -> p_vis^*Coeff(Q_obs,Rep,Top,Level) for EM, matter, clock, source, frame, readout, and finite-range operators.",
            "proof_status": "CANDIDATE_CONSTRUCTION_WRITTEN",
            "if_signed": "visible coefficients have no hidden/local scalar arguments",
            "current_gap": "the parent action has not selected this functor/target category as its syntax",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCF2318_1_vertical_silence",
            "claim_piece": "coefficient descent gives vertical derivative zero",
            "formal_statement": "If c_i=F_coeff(O_i)=p_vis^*cbar_i and v in ker(Dp_vis), then L_v c_i=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "if_signed": "b_alpha, b_mu, b_mA, b_nuc, shadow-frame slopes, and hidden coefficient pieces of j_q vanish",
            "current_gap": "does not prove c_i is in the image of F_coeff",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCF2318_2_source_target_exclusion",
            "claim_piece": "source-only R_+ target is excluded",
            "formal_statement": "F_coeff has no target object R_+^active-source-prefactor except a guarded common calibration mode.",
            "proof_status": "POWERFUL_IF_PARENT_SIGNED",
            "if_signed": "relative delta_w_A and kappa_A source multipliers become ill-typed",
            "current_gap": "1489/1490 record target exclusion as exact but not derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCF2318_3_hidden_scalar_counterexample",
            "claim_piece": "hidden scalar blocks construction",
            "formal_statement": "If I_hid survives and R or R_+ coefficient targets are legal, c=c0+epsilon I_hid is a valid hidden-visible Hom.",
            "proof_status": "COUNTEREXAMPLE_RETAINED",
            "if_signed": "not applicable; this is the obstruction",
            "current_gap": "hidden invariant algebra triviality/no-hair/profile-zero route remains unsigned",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCF2318_4_common_measure_readout",
            "claim_piece": "common measure and readout closure",
            "formal_statement": "The functor must own action-scale/current normalization and survive S_eff, threshold, detector, and source-worldtube readout maps.",
            "proof_status": "REQUIRED_GUARD_UNSIGNED",
            "if_signed": "tree-level coefficient silence would not be undone in the empirical arenas",
            "current_gap": "common measure/current owner and radiative/readout closure are not parent-signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PCF2318_5_verdict",
            "claim_piece": "construct parent coefficient functor now",
            "formal_statement": "PCF2318_0 through PCF2318_4 would give a parent coefficient functor that signs no-hidden-visible-Hom and feeds j_q source silence.",
            "proof_status": "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED",
            "if_signed": "local coupling branch could move from finite priors toward theorem-zero",
            "current_gap": "parent syntax/target category, hidden invariant triviality, common measure, and readout closure are still missing",
            "valid_for_claim": "false",
        },
    ]


def build_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "TCA2318_0_geometry",
            "coefficient_target": "geometry/coframe/connection coefficients",
            "allowed_domain": "q_loc, e_obs, g_obs, connection data",
            "forbidden_domain": "hidden representative/profile labels not seen by q_loc",
            "status": "ADMISSIBLE_CONDITIONAL",
            "effect_if_unsigned": "shadow geometry/frame terms remain possible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TCA2318_1_EM",
            "coefficient_target": "EM kinetic/fine-structure coefficient",
            "allowed_domain": "fixed charge lattice, Level_EM, quotient-owned gauge owner",
            "forbidden_domain": "f(I_hid)F_Q^2, alpha_eff(readout), threshold hidden maps",
            "status": "BLOCKED_BY_ALPHA_OWNER_AND_HIDDEN_SCALAR",
            "effect_if_unsigned": "b_alpha remains live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TCA2318_2_matter_constants",
            "coefficient_target": "masses, Yukawas, binding, nuclear/material constants",
            "allowed_domain": "fixed representation/superselection data or quotient-owned constant sector",
            "forbidden_domain": "m_A(I_hid), B_A(marker), Lambda_QCD(I_hid)",
            "status": "BLOCKED_BY_CONSTANT_SECTOR_OWNER",
            "effect_if_unsigned": "b_mu, b_mA, b_nuc remain live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TCA2318_3_source_prefactor",
            "coefficient_target": "active source/action prefactor",
            "allowed_domain": "one guarded common calibration mode only",
            "forbidden_domain": "w_A, kappa_A, w(I_hid), kappa(marker), current-label prefactors",
            "status": "TARGET_EXACT_NOT_DERIVED",
            "effect_if_unsigned": "delta_w_A source weights remain live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TCA2318_4_shadow_readout",
            "coefficient_target": "shadow frame/readout coefficient",
            "allowed_domain": "downstream readout maps proven to preserve parent coefficient syntax",
            "forbidden_domain": "A_A(I_hid)^2 g_obs, disformal B_A(I_hid), tau_readout(hidden/source-worldtube)",
            "status": "READOUT_CLOSURE_UNSIGNED",
            "effect_if_unsigned": "shadow-frame and Delta_tau residuals remain live",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "TCA2318_5_finite_range",
            "coefficient_target": "finite-range/R10 operator coefficient",
            "allowed_domain": "parent-owned range/operator data with source/test projections",
            "forbidden_domain": "alpha_X(lambda) or K_X sourced by hidden scalar without owner/projection",
            "status": "FINITE_OPERATOR_OWNER_MISSING",
            "effect_if_unsigned": "R10 alpha(lambda) needs curve/theorem-zero row",
            "valid_for_claim": "false",
        },
    ]


def build_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBL2318_0_parent_object",
            "proof_obligation": "single parent action/functor object is selected before readout and fitting",
            "source_basis": "1090;1447;2317",
            "status": "NOT_PARENT_SIGNED",
            "required_for": "own F_coeff rather than adopt it as hygiene",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBL2318_1_target_category",
            "proof_obligation": "coefficient target category excludes hidden-visible and source-only targets",
            "source_basis": "1066;1489;1490",
            "status": "EXACT_RULE_NOT_DERIVED",
            "required_for": "kill f(I_hid)F^2 and R_+ source prefactors",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBL2318_2_hidden_invariants",
            "proof_obligation": "hidden invariant algebra is trivial or every surviving scalar is no-haired/bounded",
            "source_basis": "1051;1092;1219;1924",
            "status": "COUNTEREXAMPLE_RETAINED",
            "required_for": "prevent hidden scalars from feeding allowed coefficient targets",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBL2318_3_common_measure",
            "proof_obligation": "common action/current/source normalization with no species-dependent Jacobian",
            "source_basis": "1066;1479;1489",
            "status": "COMMON_MEASURE_UNSIGNED",
            "required_for": "kill delta_w_A in the source/action-scale channel",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBL2318_4_readout_closure",
            "proof_obligation": "S_eff, thresholds, detector maps, clocks, and source-worldtubes preserve coefficient syntax",
            "source_basis": "1050;1051;1091;2317",
            "status": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
            "required_for": "stop hidden dependence re-entering after variation",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "OBL2318_5_verdict",
            "proof_obligation": "all parent coefficient functor obligations close together",
            "source_basis": "2318 synthesis",
            "status": "FUNCTOR_CONSTRUCTION_FAILS_CURRENTLY",
            "required_for": "promote no-hidden-visible-Hom and j_q coupling silence",
            "valid_for_claim": "false",
        },
    ]


def build_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCHEMA2318_0_required_columns",
            "runner_piece": "finite coupling prior input columns",
            "schema": "symbol, sector, coefficient_definition, units, theorem_zero_status, numeric_value, uncertainty, source_path, source_row_id, arena_projection, no_cancellation_group, score_ready, valid_for_claim",
            "acceptance_rule": "row can score only if theorem_zero_status=SIGNED_ZERO or numeric_value/uncertainty/source/projection are source-backed",
            "current_status": "SCHEMA_READY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCHEMA2318_1_no_cancellation",
            "runner_piece": "no-cancellation envelope",
            "schema": "sum_abs over live components by arena unless a parent covariance/orthogonality theorem signs cancellation",
            "acceptance_rule": "do not let b_alpha cancel delta_w_A or readout by fit choice",
            "current_status": "REQUIRED_GUARD",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCHEMA2318_2_branch_lock",
            "runner_piece": "same-branch lock",
            "schema": "coefficient, tau, range, source/test charge, denominator, and observable projection must belong to the same parent branch",
            "acceptance_rule": "reject mixed closure/source rows",
            "current_status": "REQUIRED_GUARD",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SCHEMA2318_3_nonclaim_first_rows",
            "runner_piece": "first eligible acquisition targets",
            "schema": "b_alpha*tau_clock_time product; delta_w_AB WEP interface; PPN vector component rows; R10 alpha(lambda) curve row",
            "acceptance_rule": "all start nonclaim until direct MTS projection/source path is present",
            "current_status": "ACQUISITION_QUEUE_READY",
            "valid_for_claim": "false",
        },
    ]


def build_smoke_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMOKE2318_0_b_alpha",
            "symbol": "b_alpha",
            "sector": "EM_alpha",
            "coefficient_definition": "vertical derivative of EM/gauge kinetic coefficient",
            "units": "dimensionless vertical derivative",
            "theorem_zero_status": "UNSIGNED",
            "numeric_value": "MISSING_SOURCE_BACKED_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "arena_projection": "clock;WEP;R10;PPN_alpha",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMOKE2318_1_b_alpha_tau_clock",
            "symbol": "b_alpha*tau_clock_time",
            "sector": "clock_product",
            "coefficient_definition": "source-backed clock product candidate from 1092, not standalone b_alpha",
            "units": "yr^-1 product/envelope",
            "theorem_zero_status": "SOURCE_BACKED_PRODUCT_NONCLAIM",
            "numeric_value": "2.1e-18",
            "source_path": str(PATHS["1092_doc"]),
            "arena_projection": "clock product only; standalone b_alpha blocked",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMOKE2318_2_delta_w",
            "symbol": "delta_w_A",
            "sector": "source_weight",
            "coefficient_definition": "relative active-source/action-scale weight after common mode removed",
            "units": "dimensionless",
            "theorem_zero_status": "UNSIGNED",
            "numeric_value": "MISSING_SOURCE_BACKED_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "arena_projection": "WEP;Newton;R10 source leg",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMOKE2318_3_ppn_vector",
            "symbol": "alpha_PPN_total_abs_vector",
            "sector": "PPN_vector",
            "coefficient_definition": "local-GR-facing vector envelope from 2200",
            "units": "dimensionless vector proxy",
            "theorem_zero_status": "SOURCE_BACKED_PROXY_NONCLAIM",
            "numeric_value": "0.005788015401465051",
            "source_path": str(PATHS["2200_doc"]),
            "arena_projection": "PPN vector target only; no raw component claim",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SMOKE2318_4_claim_gate",
            "symbol": "finite_coupling_runner_gate",
            "sector": "all",
            "coefficient_definition": "runner must refuse scoring while any row is missing theorem-zero or direct source-backed projection",
            "units": "guard",
            "theorem_zero_status": "NONCLAIM_RUNNER_SMOKE",
            "numeric_value": "NO_SCORE_ROWS",
            "source_path": "generated_from_2318_schema",
            "arena_projection": "all local arenas blocked",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_arena_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2318_0_local_GR",
            "arena": "local GR/Newton",
            "functor_effect_if_signed": "hidden-visible coupling legs in the local residual vector move toward theorem-zero",
            "current_decision": "FUNCTOR_NOT_CONSTRUCTED_USE_FINITE_RUNNER",
            "acceptance_gate": "every local residual vector component is theorem-zero or numeric/source-backed with no-cancellation placement",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2318_1_PPN",
            "arena": "PPN gamma/beta/preferred-frame vector",
            "functor_effect_if_signed": "b_alpha/shadow/readout/source-weight components would be removed from the vector",
            "current_decision": "USE_VECTOR_COMPONENT_RUNNER",
            "acceptance_gate": "component owner/projection rows required; Cassini proxy is not a raw component bound",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2318_2_WEP_clock",
            "arena": "WEP and clocks",
            "functor_effect_if_signed": "delta_w_A and constant-sector derivatives become ill-typed or vertically silent",
            "current_decision": "KEEP_B_ALPHA_TAU_AND_DELTA_W_NONCLAIM",
            "acceptance_gate": "standalone coefficients need source-backed tau/projection or theorem-zero",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ARENA2318_3_R10",
            "arena": "R10 finite range",
            "functor_effect_if_signed": "hidden EM/source/test coupling channels shrink",
            "current_decision": "R10_ALPHA_LAMBDA_STILL_CURVE_AND_PROJECTION_BLOCKED",
            "acceptance_gate": "real bound curve, range map, K_X, source/test charges, and no-cancellation envelope",
            "score_ready": "false",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2318_0_sources",
            "gate": "source paths and needles valid",
            "passed": "true",
            "claim_effect": "audit reproducible",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2318_1_conditional_functor",
            "gate": "conditional coefficient functor theorem stated",
            "passed": "true",
            "claim_effect": "exact route available under premises",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2318_2_parent_functor_constructed",
            "gate": "parent coefficient functor actually derived from MTS primitives",
            "passed": "false",
            "claim_effect": "no-hidden-visible-Hom cannot be promoted",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2318_3_runner_score_ready",
            "gate": "finite coupling runner has score-ready rows",
            "passed": "false",
            "claim_effect": "empirical local scoring blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2318_4_local_GR_Newton",
            "gate": "local GR/Newton recovery derived",
            "passed": "false",
            "claim_effect": "still a target, not a result",
            "valid_for_claim": "false",
        },
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2318_0_claim_functor",
            "claim": "2318 constructs the parent coefficient functor",
            "allowed": "false",
            "reason": "candidate functor and conditional silence theorem are written, but parent target category/hidden invariant/common measure/readout closure are unsigned",
            "blocking_rows": "PCF2318_5_verdict;OBL2318_5_verdict",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2318_1_score_runner",
            "claim": "finite coupling prior runner can score local tests now",
            "allowed": "false",
            "reason": "runner smoke rows are deliberately nonclaim; b_alpha*tau and PPN vector entries are proxy/product targets, not full MTS predictions",
            "blocking_rows": "SMOKE2318_4_claim_gate;CG2318_3_runner_score_ready",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2318_2_local_GR",
            "claim": "MTS derives local GR/Newton after 2318",
            "allowed": "false",
            "reason": "the functor failed and the residual runner is not source-complete",
            "blocking_rows": "ARENA2318_0_local_GR;CG2318_4_local_GR_Newton",
            "valid_for_claim": "false",
        },
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2318_0",
            "next_target": "2319-Y5-R2FR-first-source-backed-finite-coupling-row-balpha-clock-or-deltaw.md",
            "why": "2318 cannot honestly promote the functor; the next useful move is to convert the finite coupling runner from schema to first source-backed nonclaim rows, starting with the existing b_alpha*tau_clock product and delta_w/PPN vector requirements",
            "claim_status": "nonclaim_private_next_step",
            "valid_for_claim": "false",
        }
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, source_path, destination_path in BRANCH_COPY_SPECS:
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(source_path),
                "branch_copy_path": str(destination_path),
                "copy_exists": bool_text(destination_path.exists()),
                "row_count": len(read_csv_rows(destination_path)),
                "valid_for_claim": "false",
            }
        )
    return rows


def validate(
    source_rows: list[dict[str, Any]],
    construction_rows: list[dict[str, Any]],
    target_rows: list[dict[str, Any]],
    obligation_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tables = [source_rows, construction_rows, target_rows, obligation_rows, schema_rows, smoke_rows, arena_rows, claim_rows, refusal_rows, next_rows, copy_rows]
    formalization_output_markers = (
        "2318-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_2318",
        "P8_Y5_BRR545_2318",
        "JR2318_",
        "PARENT_COEFFICIENT_FUNCTOR_ARENA_GATES_2318",
        "parent_coefficient_functor_arena_gates_nonclaim_2318",
        "Y5_R2FR_parent_coefficient_functor_construction_or_finite_coupling_prior_runner_2318",
    )
    formalization_hits = [
        path
        for path in FORMALIZATION.rglob("*")
        if any(marker in path.name for marker in formalization_output_markers)
    ] if FORMALIZATION.exists() else []

    construction_ids = {row["row_id"] for row in construction_rows}
    target_ids = {row["row_id"] for row in target_rows}
    obligation_ids = {row["row_id"] for row in obligation_rows}
    smoke_ids = {row["row_id"] for row in smoke_rows}

    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2318_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists"))
    checks.append(("VAL2318_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found"))
    checks.append(("VAL2318_02_candidate_functor_written", {"PCF2318_0_candidate_functor", "PCF2318_1_vertical_silence"}.issubset(construction_ids), "candidate functor and conditional vertical silence are written"))
    checks.append(("VAL2318_03_functor_not_promoted", any(row["row_id"] == "PCF2318_5_verdict" and row["proof_status"] == "PARENT_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED" for row in construction_rows), "parent coefficient functor promotion refused"))
    checks.append(("VAL2318_04_target_category_complete", {"TCA2318_1_EM", "TCA2318_2_matter_constants", "TCA2318_3_source_prefactor", "TCA2318_4_shadow_readout", "TCA2318_5_finite_range"}.issubset(target_ids), "target category audit covers EM/matter/source/shadow/R10"))
    checks.append(("VAL2318_05_obligation_ledger", {"OBL2318_0_parent_object", "OBL2318_1_target_category", "OBL2318_2_hidden_invariants", "OBL2318_3_common_measure", "OBL2318_4_readout_closure", "OBL2318_5_verdict"}.issubset(obligation_ids), "proof obligation ledger includes all blockers"))
    checks.append(("VAL2318_06_schema_ready", any(row["row_id"] == "SCHEMA2318_0_required_columns" and "valid_for_claim" in row["schema"] for row in schema_rows), "finite coupling runner schema includes claim gate columns"))
    checks.append(("VAL2318_07_smoke_blocks_scoring", {"SMOKE2318_0_b_alpha", "SMOKE2318_1_b_alpha_tau_clock", "SMOKE2318_2_delta_w", "SMOKE2318_3_ppn_vector", "SMOKE2318_4_claim_gate"}.issubset(smoke_ids) and all(row["score_ready"] == "false" for row in smoke_rows), "runner smoke rows remain non-score-ready"))
    checks.append(("VAL2318_08_arena_blocks_preserved", all(row["score_ready"] == "false" for row in arena_rows), "all arena rows remain blocked/nonclaim"))
    checks.append(("VAL2318_09_claim_gates_block", any(row["row_id"] == "CG2318_4_local_GR_Newton" and row["passed"] == "false" for row in claim_rows), "local GR/Newton claim remains blocked"))
    checks.append(("VAL2318_10_refusals_block", all(row["allowed"] == "false" for row in refusal_rows), "refusal runner blocks premature claims"))
    checks.append(("VAL2318_11_next_target", any(row["row_id"] == "NEXT2318_0" and "first-source-backed-finite-coupling-row" in row["next_target"] for row in next_rows), "next target selected"))
    checks.append(("VAL2318_12_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in copy_rows), "branch copies exist and parse"))
    checks.append(("VAL2318_13_no_claim_flags", not any(row.get("valid_for_claim") == "true" for table in tables for row in table), "no generated row is valid_for_claim=true"))
    checks.append(("VAL2318_14_formalization_untouched_by_2318", len(formalization_hits) == 0, "no 2318 checkpoint output appears in formalization-workbench"))

    rows = [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": "false",
        }
        for row_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "row_id": "VAL2318_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2318 writes the candidate parent coefficient functor and exact conditional vertical-silence theorem, refuses promotion because parent syntax/target category, hidden invariant triviality, common measure, and radiative/readout closure remain unsigned, stages a finite coupling prior runner schema plus nonclaim smoke rows, keeps all local/PPN/R10/WEP/clock/orbital scoring blocked, and selects first source-backed finite coupling rows as the next target.",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(
    source_rows: list[dict[str, Any]],
    construction_rows: list[dict[str, Any]],
    target_rows: list[dict[str, Any]],
    obligation_rows: list[dict[str, Any]],
    schema_rows: list[dict[str, Any]],
    smoke_rows: list[dict[str, Any]],
    arena_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2318 - Parent Coefficient Functor Construction Or Finite Coupling Prior Runner",
        "",
        "## Summary",
        "",
        "2318 tries the leap rather than circling the same coupling wall. The candidate parent coefficient functor is now explicit: visible coefficients should be generated only from quotient data, fixed representation/topological data, and declared EM/source levels. If that functor is parent-signed, then hidden vertical motion cannot change visible coefficients and the dangerous first-order coupling legs in `j_q` vanish.",
        "",
        "The construction still does not close. The same hard blockers survive: the parent action has not selected the coefficient target category; hidden invariant scalars remain active counterexamples; source-only `R_+` prefactors are not parent-excluded; common measure/current ownership is unsigned; and readout/effective-action closure is not proved.",
        "",
        "So this checkpoint switches from theorem-claim mode to runner mode. It writes the finite-coupling prior runner schema and smoke rows. These rows do not score yet; they tell us exactly what a row must contain before it can pressure local GR/Newton, PPN, WEP, clocks, or R10.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "",
        "## Parent Coefficient Functor Construction Attempt",
        "",
        markdown_table(construction_rows, ["row_id", "claim_piece", "formal_statement", "proof_status", "if_signed", "current_gap", "valid_for_claim"]),
        "",
        "## Coefficient Target Category Audit",
        "",
        markdown_table(target_rows, ["row_id", "coefficient_target", "allowed_domain", "forbidden_domain", "status", "effect_if_unsigned", "valid_for_claim"]),
        "",
        "## Functor Proof Obligation Ledger",
        "",
        markdown_table(obligation_rows, ["row_id", "proof_obligation", "source_basis", "status", "required_for", "valid_for_claim"]),
        "",
        "## Finite Coupling Prior Runner Schema",
        "",
        markdown_table(schema_rows, ["row_id", "runner_piece", "schema", "acceptance_rule", "current_status", "valid_for_claim"]),
        "",
        "## Finite Coupling Prior Runner Smoke",
        "",
        markdown_table(smoke_rows, ["row_id", "symbol", "sector", "coefficient_definition", "units", "theorem_zero_status", "numeric_value", "source_path", "arena_projection", "score_ready", "valid_for_claim"]),
        "",
        "## Arena Acceptance Gates",
        "",
        markdown_table(arena_rows, ["row_id", "arena", "functor_effect_if_signed", "current_decision", "acceptance_gate", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Refusal Runner",
        "",
        markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = build_sources()
    construction_rows = build_construction_rows()
    target_rows = build_target_rows()
    obligation_rows = build_obligation_rows()
    schema_rows = build_schema_rows()
    smoke_rows = build_smoke_rows()
    arena_rows = build_arena_rows()
    claim_rows = build_claim_rows()
    refusal_rows = build_refusal_rows()
    next_rows = build_next_rows()

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["construction"], construction_rows)
    write_csv(OUTPUTS["targets"], target_rows)
    write_csv(OUTPUTS["obligations"], obligation_rows)
    write_csv(OUTPUTS["schema"], schema_rows)
    write_csv(OUTPUTS["smoke"], smoke_rows)
    write_csv(OUTPUTS["arena"], arena_rows)
    write_csv(OUTPUTS["claims"], claim_rows)
    write_csv(OUTPUTS["refusal"], refusal_rows)
    write_csv(OUTPUTS["next"], next_rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], copy_rows)

    validation_rows = validate(
        source_rows,
        construction_rows,
        target_rows,
        obligation_rows,
        schema_rows,
        smoke_rows,
        arena_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows)
    write_markdown(
        source_rows,
        construction_rows,
        target_rows,
        obligation_rows,
        schema_rows,
        smoke_rows,
        arena_rows,
        claim_rows,
        refusal_rows,
        next_rows,
        copy_rows,
        validation_rows,
    )

    overall = next(row for row in validation_rows if row["row_id"] == "VAL2318_OVERALL")
    print(f"{overall['row_id']}={overall['status']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
