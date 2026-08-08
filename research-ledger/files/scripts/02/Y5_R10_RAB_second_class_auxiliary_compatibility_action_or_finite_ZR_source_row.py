from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1268"
TITLE = "1268-Y5-R10-RAB-second-class-auxiliary-compatibility-action-or-finite-ZR-source-row"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
RAB_DOCS_DIR = RAB_INTAKE_DIR / "docs"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COMPATIBILITY_ACTION_PATH = OUT_DIR / f"{PACK_ID}_COMPATIBILITY_ACTION_CANDIDATE.csv"
VARIATION_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_VARIATIONAL_ELIMINATION_AUDIT.csv"
AP_MATRIX_PATH = OUT_DIR / f"{PACK_ID}_AP1265_COMPATIBILITY_CLOSURE_MATRIX.csv"
FAILURE_MODE_PATH = OUT_DIR / f"{PACK_ID}_FAILURE_MODE_AUDIT.csv"
FINITE_STATUS_PATH = OUT_DIR / f"{PACK_ID}_FINITE_ZR_SOURCE_ROW_TEMPLATE_STATUS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1268_VALIDATION.csv"
FINITE_TEMPLATE_PATH = RAB_DOCS_DIR / "ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def live_intake_counts() -> tuple[int, int, int]:
    raw_dir = RAB_INTAKE_DIR / "raw"
    accepted_dir = RAB_INTAKE_DIR / "accepted"
    docs_dir = RAB_INTAKE_DIR / "docs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    accepted_dir.mkdir(parents=True, exist_ok=True)
    docs_dir.mkdir(parents=True, exist_ok=True)
    raw_rows = sum(len(read_csv(path)) for path in raw_dir.glob("*.csv"))
    accepted_rows = sum(len(read_csv(path)) for path in accepted_dir.glob("*.csv"))
    docs_rows = sum(len(read_csv(path)) for path in docs_dir.glob("*.csv"))
    return raw_rows, accepted_rows, docs_rows


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        COMPATIBILITY_ACTION_PATH,
        VARIATION_AUDIT_PATH,
        AP_MATRIX_PATH,
        FAILURE_MODE_PATH,
        FINITE_STATUS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        FINITE_TEMPLATE_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAB_DOCS_DIR.mkdir(parents=True, exist_ok=True)

    finite_template = [
        {
            "row_id": "ZR1268_TEMPLATE_ZR",
            "coefficient_symbol": "Z_R",
            "branch": "finite_RAB_kinetic_or_theorem_zero",
            "coefficient_value": "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO",
            "coefficient_units": "MISSING_PARENT_NORMALIZED_UNITS",
            "normalization_convention": "MISSING_RAB_DIMENSIONLESS_AND_DERIVATIVE_CONVENTION",
            "parent_action_block": "MISSING_COMPATIBILITY_ACTION_OR_COEFFICIENT_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "MISSING_R10_PPN_CLOCK_OR_ORBITAL_PROJECTION",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only finite-ZR row. Use only after source-backed value or theorem-zero certificate replaces every MISSING marker.",
        },
        {
            "row_id": "ZR1268_TEMPLATE_MR2",
            "coefficient_symbol": "M_R^2",
            "branch": "massive_or_suppressed_RAB_residual",
            "coefficient_value": "MISSING_NUMERIC_VALUE_OR_BOUND",
            "coefficient_units": "MISSING_INVERSE_LENGTH_SQUARED_OR_DECLARED_EQUIVALENT",
            "normalization_convention": "MISSING_MATCH_TO_Z_R_CONVENTION",
            "parent_action_block": "MISSING_PARENT_HESSIAN_OR_SECOND_VARIATION",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "MISSING_RANGE_TO_R10_PPN_CLOCK_OR_ORBITAL_MAP",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only mass-gap row. It cannot be scored without a sourced Hessian or explicit bound.",
        },
        {
            "row_id": "ZR1268_TEMPLATE_JR",
            "coefficient_symbol": "J_R",
            "branch": "matter_source_or_descent_zero",
            "coefficient_value": "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO",
            "coefficient_units": "MISSING_E_R_EQUATION_NORMALIZATION",
            "normalization_convention": "MISSING_SOURCE_CURRENT_CONVENTION",
            "parent_action_block": "MISSING_MATTER_DESCENT_OR_SOURCE_COUPLING",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "MISSING_QRHAT_OR_FORCE_RESIDUAL_MAP",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only bulk-source row. It must distinguish theorem-zero matter descent from finite source forcing.",
        },
        {
            "row_id": "ZR1268_TEMPLATE_BR",
            "coefficient_symbol": "B_R_or_Pi_Rn",
            "branch": "boundary_charge_or_nohair_zero",
            "coefficient_value": "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO",
            "coefficient_units": "MISSING_BOUNDARY_MOMENTUM_OR_CHARGE_UNITS",
            "normalization_convention": "MISSING_SURFACE_ORIENTATION_AND_MEASURE",
            "parent_action_block": "MISSING_BOUNDARY_FUNCTIONAL_OR_NO_FLUX_THEOREM",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "MISSING_QR_HAIR_TO_PPN_OR_ORBITAL_MAP",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only boundary row. A bulk auxiliary proof is insufficient if this row is nonzero.",
        },
        {
            "row_id": "ZR1268_TEMPLATE_TAU_R10",
            "coefficient_symbol": "tau_R10",
            "branch": "short_range_force_projection",
            "coefficient_value": "MISSING_TRANSFER_VALUE",
            "coefficient_units": "MISSING_DIMENSIONLESS_OR_KERNEL_UNITS",
            "normalization_convention": "MISSING_ALPHA_LAMBDA_MAPPING_CONVENTION",
            "parent_action_block": "MISSING_R10_PROJECTION_DERIVATION_OR_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "R10",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only arena projection row. It cannot convert coefficients into an alpha(lambda) claim yet.",
        },
        {
            "row_id": "ZR1268_TEMPLATE_TAU_PPN",
            "coefficient_symbol": "tau_PPN",
            "branch": "local_metric_projection",
            "coefficient_value": "MISSING_TRANSFER_VALUE",
            "coefficient_units": "MISSING_DIMENSIONLESS_TRANSFER_TO_GAMMA_BETA",
            "normalization_convention": "MISSING_GM_AND_PPN_CONVENTION",
            "parent_action_block": "MISSING_PPN_PROJECTION_DERIVATION_OR_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "PPN",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only PPN projection row. It cannot be used as a local-GR pass.",
        },
        {
            "row_id": "ZR1268_TEMPLATE_TAU_CLOCK",
            "coefficient_symbol": "tau_clock",
            "branch": "clock_or_spectroscopy_projection",
            "coefficient_value": "MISSING_TRANSFER_VALUE",
            "coefficient_units": "MISSING_FRACTIONAL_FREQUENCY_OR_DIMENSIONLESS_UNITS",
            "normalization_convention": "MISSING_CLOCK_READOUT_CONVENTION",
            "parent_action_block": "MISSING_CLOCK_READOUT_DERIVATION_OR_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "clock",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only clock projection row. It keeps readout effects separate from the local metric branch.",
        },
        {
            "row_id": "ZR1268_TEMPLATE_TAU_ORBITAL",
            "coefficient_symbol": "tau_orbital",
            "branch": "orbital_timing_projection",
            "coefficient_value": "MISSING_TRANSFER_VALUE",
            "coefficient_units": "MISSING_ACCELERATION_OR_DIMENSIONLESS_TRANSFER",
            "normalization_convention": "MISSING_ORBITAL_READOUT_CONVENTION",
            "parent_action_block": "MISSING_ORBITAL_PROJECTION_DERIVATION_OR_SOURCE",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "arena_projection": "orbital",
            "placeholder_status": "MISSING_DO_NOT_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "notes": "Docs-only orbital projection row. It requires a real force/timing map before use.",
        },
    ]
    write_csv(FINITE_TEMPLATE_PATH, finite_template)
    raw_rows, accepted_rows, docs_rows = live_intake_counts()

    source_register = [
        {
            "source_id": "SRC1268_0_1267_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1267_NEXT_TARGET.csv",
            "needle": "NEXT1267_0_1268",
            "purpose": "handoff to second-class auxiliary compatibility action",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_1_1267_ap_update",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1267_AP1265_CLOSURE_UPDATE.csv",
            "needle": "REFOCUSED_TO_SECOND_CLASS_PARENT_SIGNATURE",
            "purpose": "AP1265 route refocused from first-class to auxiliary compatibility",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_2_1267_finite",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1267_FINITE_ZR_ACQUISITION_START.csv",
            "needle": "FZA1267_0_ZR",
            "purpose": "finite fallback requirements from 1267",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_3_1265_ap",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1265_AUXILIARY_PROTECTION_AUDIT.csv",
            "needle": "AP1265_0_auxiliary_signature",
            "purpose": "core AP1265 protection clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_4_1265_risk",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1265_REGENERATION_RISK_LEDGER.csv",
            "needle": "RR1265_3_readout_EFT",
            "purpose": "regeneration risks to close or retain as finite fallback",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_5_1262_vertical_null",
            "local_path": "1262-Y5-R10-RAB-operator-exhaustion-minimal-assumption-audit-or-ZR-prior-envelope.md",
            "needle": "THEO1262_0_vertical_null_ban",
            "purpose": "conditional vertical-null ban and countermodel audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_6_1248_dirac",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1248_DIRAC_CHECK.csv",
            "needle": "DIR1248_2_preservation",
            "purpose": "prior Dirac preservation blocker",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_7_1264_aux",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1264_AUXILIARY_COMPATIBILITY_ROUTE.csv",
            "needle": "AUX1264_0_parent_block",
            "purpose": "candidate parent auxiliary compatibility block",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_8_1259_template",
            "local_path": "source-intake/rab-sector/docs/ZR1259_RAB_GRADIENT_COEFFICIENT_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1259_TEMPLATE_DO_NOT_SCORE",
            "purpose": "older gradient coefficient template",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1268_9_1268_template",
            "local_path": "source-intake/rab-sector/docs/ZR1268_FINITE_ZR_SOURCE_ROW_TEMPLATE_NONCLAIM.csv",
            "needle": "ZR1268_TEMPLATE_ZR",
            "purpose": "new finite-ZR source-row template generated by this checkpoint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    compatibility_action = [
        {
            "block_id": "CAC1268_0_parent_sort",
            "candidate_block": "R_AB is a compatibility coordinate/function, not a quotient observable or hidden scalar.",
            "action_piece": "R_AB := ln(T^2 S) or R_AB-C_AB[q(Phi),theta,top] as parent compatibility data.",
            "what_it_buys": "allows auxiliary elimination instead of physical R_AB hair",
            "status": "CANDIDATE_NOT_PARENT_SIGNED",
            "blocking_gap": "typed parent field/sort list is still not sourced from primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "block_id": "CAC1268_1_constraint_action",
            "candidate_block": "second-class/algebraic compatibility action",
            "action_piece": "S_R = integral mu_parent Lambda_R [R_AB - C_AB(q(Phi),theta,top)]",
            "what_it_buys": "E_Lambda enforces compatibility before local readout",
            "status": "EXACT_WITHIN_CANDIDATE",
            "blocking_gap": "parent necessity of Lambda_R block is not derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "block_id": "CAC1268_2_no_derivative_grammar",
            "candidate_block": "no D R_AB, D Lambda_R, vertical metric, or vertical connection in the parent density",
            "action_piece": "ParentGenerate excludes G_vert(DR,D R) and boundary derivative terms for R_AB.",
            "what_it_buys": "Z_R is not a legal tree-level operator inside the compatibility branch",
            "status": "REQUIRED_BUT_UNSIGNED",
            "blocking_gap": "operator-exhaustion/vertical-null theorem remains conditional",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "block_id": "CAC1268_3_matter_descent",
            "candidate_block": "matter action factors through public/quotient variables only",
            "action_piece": "S_matter = S_matter[Psi, q(Phi), theta] and delta S_matter/delta R_AB = 0.",
            "what_it_buys": "E_R gives Lambda_R=0 rather than finite matter force J_R",
            "status": "REQUIRED_BUT_UNSIGNED",
            "blocking_gap": "matter descent proof is absent in the R_AB branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "block_id": "CAC1268_4_boundary_readout",
            "candidate_block": "boundary and readout preserve auxiliary compatibility",
            "action_piece": "delta B_R/delta R_AB=0 and S_eff remains in Image(ParentGenerate[q,theta,top]).",
            "what_it_buys": "no boundary Q_R hair and no regenerated finite Z_R after elimination",
            "status": "REQUIRED_BUT_UNSIGNED",
            "blocking_gap": "boundary/no-flux and readout/EFT closure are still not proved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "block_id": "CAC1268_5_conditional_theorem",
            "candidate_block": "second-class auxiliary compatibility elimination theorem",
            "action_piece": "If CAC1268_0 through CAC1268_4 are parent-signed, eliminate R_AB,Lambda_R before readout; Z_R=J_R=B_R=0 on this branch.",
            "what_it_buys": "derived local reciprocity without pretending the constraint is first-class",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "blocking_gap": "three key protections remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    variation_audit = [
        {
            "step_id": "VAR1268_0_E_Lambda",
            "variation": "delta_{Lambda_R} S_R",
            "result": "R_AB - C_AB[q(Phi),theta,top] = 0",
            "status": "FORMAL_PASS_WITHIN_CANDIDATE",
            "claim_gap": "constraint action must be parent-owned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "VAR1268_1_E_R",
            "variation": "delta_{R_AB} S_total",
            "result": "Lambda_R + J_R + delta B_R/delta R_AB + readout_regen_terms = 0",
            "status": "PASS_ONLY_IF_SOURCES_ZERO",
            "claim_gap": "need J_R=0, boundary zero, and readout-regeneration zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "VAR1268_2_aux_elimination",
            "variation": "solve E_Lambda and E_R together",
            "result": "R_AB=C_AB and Lambda_R=0 only if no direct R_AB source exists",
            "status": "EXACT_CONDITIONAL",
            "claim_gap": "otherwise Lambda_R or finite residual remains",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "VAR1268_3_no_symplectic_sector",
            "variation": "canonical/Dirac classification after algebraic elimination",
            "result": "no physical Pi_R or Q_R hair remains if the auxiliary block is complete and boundary-silent",
            "status": "EXACT_CONDITIONAL",
            "claim_gap": "boundary silence still not signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "step_id": "VAR1268_4_operator_ban",
            "variation": "test legality of adding 1/2 Z_R h^{ij}D_iR_ABD_jR_AB",
            "result": "operator is forbidden only if R_AB is purely auxiliary/vertical and no vertical metric/connection exists",
            "status": "BLOCKED_BY_UNSIGNED_OPERATOR_EXCLUSION",
            "claim_gap": "finite-ZR template remains required",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    ap_matrix = [
        {
            "clause_id": "AP1265_0_auxiliary_signature",
            "compatibility_action_status": "PARTIAL_PASS_CANDIDATE_WRITTEN",
            "evidence": "CAC1268_0_parent_sort; CAC1268_1_constraint_action",
            "remaining_gap": "parent sort/field list not signed",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_1_no_derivatives",
            "compatibility_action_status": "UNSIGNED",
            "evidence": "CAC1268_2_no_derivative_grammar; VAR1268_4_operator_ban",
            "remaining_gap": "no object-language proof bans D R_AB",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_2_eliminability",
            "compatibility_action_status": "EXACT_CONDITIONAL",
            "evidence": "VAR1268_0_E_Lambda; VAR1268_1_E_R; VAR1268_2_aux_elimination",
            "remaining_gap": "J_R, B_R, and readout terms must be zero",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_3_boundary_silence",
            "compatibility_action_status": "UNSIGNED",
            "evidence": "CAC1268_4_boundary_readout; VAR1268_3_no_symplectic_sector",
            "remaining_gap": "no boundary/corner no-hair theorem",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "AP1265_4_readout_stability",
            "compatibility_action_status": "UNSIGNED",
            "evidence": "CAC1268_4_boundary_readout",
            "remaining_gap": "no readout/EFT closure theorem",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    failure_modes = [
        {
            "failure_id": "FM1268_0_physical_RAB",
            "if_clause_fails": "AP1265_0",
            "then_effect": "R_AB can be a physical local strain/scalar",
            "required_fallback": "source Z_R and M_R^2 or prove field exclusion",
            "status": "FINITE_BRANCH_REQUIRED_IF_FAILS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FM1268_1_kinetic_counterterm",
            "if_clause_fails": "AP1265_1",
            "then_effect": "D R_AB kinetic/gradient operator is legal",
            "required_fallback": "source Z_R or theorem-zero operator ban",
            "status": "FINITE_BRANCH_REQUIRED_IF_FAILS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FM1268_2_matter_source",
            "if_clause_fails": "AP1265_2 or matter descent part",
            "then_effect": "E_R contains J_R and can source reciprocal hair",
            "required_fallback": "source J_R or matter descent zero theorem",
            "status": "FINITE_BRANCH_REQUIRED_IF_FAILS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FM1268_3_boundary_charge",
            "if_clause_fails": "AP1265_3",
            "then_effect": "Q_R/B_R boundary hair survives even if bulk is auxiliary",
            "required_fallback": "source B_R/Pi_Rn or no-flux theorem",
            "status": "FINITE_BRANCH_REQUIRED_IF_FAILS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "failure_id": "FM1268_4_readout_regeneration",
            "if_clause_fails": "AP1265_4",
            "then_effect": "effective/readout action can regenerate Z_R or observable transfer",
            "required_fallback": "source tau_R10/tau_PPN/tau_clock/tau_orbital",
            "status": "FINITE_BRANCH_REQUIRED_IF_FAILS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    finite_status = [
        {
            "template_id": "T1268_0_finite_template",
            "template_path": str(FINITE_TEMPLATE_PATH),
            "rows": len(finite_template),
            "status": "DOCS_ONLY_NONCLAIM_PLACEHOLDERS_PRESENT",
            "raw_rows": raw_rows,
            "accepted_rows": accepted_rows,
            "docs_rows": docs_rows,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    claim_gates = [
        {
            "gate_id": "GATE1268_0_compatibility_action",
            "claim": "parent-signed second-class compatibility action is complete",
            "status": "BLOCKED",
            "reason": "candidate action is written, but parent sort, operator exclusion, matter descent, boundary silence, and readout stability are not all signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1268_1_ZR_zero",
            "claim": "Z_R=0 theorem follows from auxiliary compatibility",
            "status": "BLOCKED",
            "reason": "the theorem is exact conditional only; AP1265_1/AP1265_3/AP1265_4 remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1268_2_finite_template",
            "claim": "finite-ZR source row template exists",
            "status": "PASS_NONCLAIM",
            "reason": "docs-only template with explicit MISSING markers was generated; no placeholder is accepted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1268_3_local_tests",
            "claim": "local GR/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "neither theorem-zero nor finite source rows are claim-valid",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1268_0_candidate_action",
            "decision": "keep the second-class auxiliary compatibility action as the best derivation route",
            "because": "it gives the right variational elimination without pretending the hard constraint is first-class",
            "status": "EXACT_CONDITIONAL_PROGRESS",
            "next_action": "source/sign the parent sort and operator/matter/boundary/readout clauses",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1268_1_not_closed",
            "decision": "do not claim Z_R=0 or local GR yet",
            "because": "the compatibility action is a candidate block, not a parent-derived necessity",
            "status": "CLAIM_BLOCKED",
            "next_action": "attack AP1265_1 operator exclusion first, then boundary/readout",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1268_2_fallback_ready",
            "decision": "create a stricter finite-ZR source-row template",
            "because": "if any compatibility clause fails, the local branch needs quantified residual coefficients and projections",
            "status": "DOCS_TEMPLATE_READY_NONCLAIM",
            "next_action": "do not move template rows to raw/accepted until all MISSING markers are replaced by sourced values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1268_0_1269",
            "target_file": "1269-Y5-R10-RAB-operator-exclusion-parent-sort-proof-or-ZR-template-intake-validator.md",
            "target_script": "scripts/Y5_R10_RAB_operator_exclusion_parent_sort_proof_or_ZR_template_intake_validator.py",
            "task": "try to prove the parent sort/operator-exclusion clause for R_AB so the compatibility action cannot grow a Z_R kinetic term; if it fails, add an intake validator that refuses finite-ZR rows with MISSING markers or absent source paths",
            "success_condition": "AP1265_1 is parent-signed by a typed operator exclusion proof, or the finite-ZR template has a validator that blocks every placeholder/source-missing row",
            "do_not": "do not score docs-only finite-ZR rows and do not claim local GR from the conditional compatibility action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (COMPATIBILITY_ACTION_PATH, compatibility_action),
        (VARIATION_AUDIT_PATH, variation_audit),
        (AP_MATRIX_PATH, ap_matrix),
        (FAILURE_MODE_PATH, failure_modes),
        (FINITE_STATUS_PATH, finite_status),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    conditional_theorem_present = any(row["status"] == "EXACT_CONDITIONAL_NOT_PARENT_SIGNED" for row in compatibility_action)
    ap_ids = {row["clause_id"] for row in ap_matrix}
    expected_ap_ids = {
        "AP1265_0_auxiliary_signature",
        "AP1265_1_no_derivatives",
        "AP1265_2_eliminability",
        "AP1265_3_boundary_silence",
        "AP1265_4_readout_stability",
    }
    ap_blocks_claim = all(row["claim_status"] == "BLOCKED" for row in ap_matrix)
    template_rows = read_csv(FINITE_TEMPLATE_PATH)
    template_has_missing = all(any("MISSING_" in str(value) for value in row.values()) for row in template_rows)
    template_nonclaim = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in template_rows)
    finite_status_ok = finite_status[0]["status"] == "DOCS_ONLY_NONCLAIM_PLACEHOLDERS_PRESENT"
    claim_gates_safe = all(
        row["status"] in {"BLOCKED", "PASS_NONCLAIM"} and is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"])
        for row in claim_gates
    ) and any(row["gate_id"] == "GATE1268_0_compatibility_action" and row["status"] == "BLOCKED" for row in claim_gates)
    all_generated_rows = [
        *source_register,
        *compatibility_action,
        *variation_audit,
        *ap_matrix,
        *failure_modes,
        *finite_status,
        *claim_gates,
        *decisions,
        *next_target,
        *template_rows,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in [*generated_tables, (FINITE_TEMPLATE_PATH, finite_template)]:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1268_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1268_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1268_2_conditional_action",
            "compatibility action theorem is present but conditional",
            conditional_theorem_present,
            "CAC1268_5_conditional_theorem=EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
        ),
        validation_row(
            "VAL1268_3_ap_matrix_complete",
            "all AP1265 clauses are audited against compatibility action",
            ap_ids == expected_ap_ids and ap_blocks_claim,
            f"covered={len(ap_ids)}; missing={sorted(expected_ap_ids - ap_ids)}; all_blocked={ap_blocks_claim}",
        ),
        validation_row(
            "VAL1268_4_template_created",
            "finite-ZR docs template is created with required rows",
            len(template_rows) == 8 and finite_status_ok,
            f"template_rows={len(template_rows)}; raw_rows={raw_rows}; accepted_rows={accepted_rows}; docs_rows={docs_rows}",
        ),
        validation_row(
            "VAL1268_5_template_placeholders",
            "finite-ZR template keeps MISSING markers and remains nonclaim",
            template_has_missing and template_nonclaim,
            "all template rows contain MISSING markers and claim flags are false",
        ),
        validation_row(
            "VAL1268_6_claim_gates",
            "claim gates block compatibility/local-test claims",
            claim_gates_safe,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1268_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables and template",
        ),
        validation_row(
            "VAL1268_8_next_target_1269",
            "next target routes to operator exclusion or template intake validator",
            next_target[0]["next_id"] == "NEXT1268_0_1269",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1268_9_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1268_10_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1268_11_overall",
            "overall 1268 validation",
            overall_pass,
            "1268 writes the second-class auxiliary compatibility action as an exact conditional theorem, keeps all AP1265 claim gates blocked, and creates a stricter finite-ZR docs-only source-row template",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1268 constructs the right kind of local mechanism: a second-class/algebraic auxiliary compatibility action. It is mathematically cleaner than the failed first-class route: `E_{{Lambda_R}}` enforces `R_AB-C_AB=0`, and `E_{{R_AB}}` kills `Lambda_R` only if matter, boundary, and readout sources are absent.

**Main progress:** this gives an exact conditional route to `Z_R=0` without fake gauge language. But it still is not a public theorem because the parent sort, no-derivative grammar, matter descent, boundary silence, and readout stability are not all signed.

**No-claim guard:** no `Z_R=0`, local-GR/Newton, R10, PPN, clock, or orbital claim is made. Since the compatibility action is not fully signed, a stricter docs-only finite-`Z_R` source-row template was created and kept nonclaim.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Compatibility Action Candidate
{markdown_table(compatibility_action, ["block_id", "candidate_block", "action_piece", "what_it_buys", "status", "blocking_gap", "valid_for_claim", "claim_allowed"])}

## Variational Elimination Audit
{markdown_table(variation_audit, ["step_id", "variation", "result", "status", "claim_gap", "valid_for_claim", "claim_allowed"])}

## AP1265 Compatibility Closure Matrix
{markdown_table(ap_matrix, ["clause_id", "compatibility_action_status", "evidence", "remaining_gap", "claim_status", "valid_for_claim", "claim_allowed"])}

## Failure Mode Audit
{markdown_table(failure_modes, ["failure_id", "if_clause_fails", "then_effect", "required_fallback", "status", "valid_for_claim", "claim_allowed"])}

## Finite Z_R Source Row Template Status
{markdown_table(finite_status, ["template_id", "template_path", "rows", "status", "raw_rows", "accepted_rows", "docs_rows", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
