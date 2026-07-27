from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1870"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1870-Y5-R2FR-QR-ZR-MR2-source-chain-first-fill-or-no-charge-return.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_SOURCE_REGISTER.csv",
    "source_chain_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_QR_ZR_MR2_SOURCE_CHAIN_AUDIT.csv",
    "denominator_convention_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_DENOMINATOR_CONVENTION_GATE.csv",
    "no_charge_return_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_NO_CHARGE_RETURN_AUDIT.csv",
    "r10_ppn_fork_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_R10_PPN_FORK_MATRIX.csv",
    "first_fill_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_FIRST_FILL_ROWS_NONCLAIM.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1870_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1870_VALIDATION.csv",
}


def as_bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def path_has_needle(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def md_escape(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register() -> list[dict[str, Any]]:
    sources = [
        {
            "source_id": "SRC1870_0_1869_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1869-Y5-R2FR-finite-local-coefficient-bound-branch-setup.md",
            "required_needle": "NEXT1869_0_primary",
            "use_in_1870": "selects Q_R/Z_R/M_R^2 source-chain first fill.",
        },
        {
            "source_id": "SRC1870_1_1869_validation",
            "source_kind": "validation_anchor",
            "source_path": RESIDUALS / "P8_Y5_BRR545_1869_VALIDATION.csv",
            "required_needle": "VAL1869_OVERALL",
            "use_in_1870": "confirms finite coefficient-bound branch setup passed.",
        },
        {
            "source_id": "SRC1870_2_1869_schema",
            "source_kind": "component_schema",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1869_COMPONENT_INPUT_SCHEMA.csv",
            "required_needle": "FLC1869_1_ZR",
            "use_in_1870": "imports exact component rows to be first-filled.",
        },
        {
            "source_id": "SRC1870_3_1256_Hcore",
            "source_kind": "minimal_Hcore_source_equation",
            "source_path": RESIDUALS / "P8_Y5_R10_1256_MINIMAL_HCORE_SOURCE_EQUATION_CONTRACT.csv",
            "required_needle": "HC1256_0_minimal_density",
            "use_in_1870": "provides the finite operator/source equation for Z_R, M_R^2, lambda_R, J_R and B_R.",
        },
        {
            "source_id": "SRC1870_4_1256_coefficients",
            "source_kind": "coefficient_requirements",
            "source_path": RESIDUALS / "P8_Y5_R10_1256_COEFFICIENT_REQUIREMENTS.csv",
            "required_needle": "COEF1256_0_ZR",
            "use_in_1870": "shows Z_R/M_R^2/lambda_R/J_R/B_R are missing or unsigned.",
        },
        {
            "source_id": "SRC1870_5_1569_ZR",
            "source_kind": "ZR_first_row_attempt",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1569_ZR_THEOREM_OR_COEFFICIENT_ATTEMPT.csv",
            "required_needle": "ZR1569_3_verdict",
            "use_in_1870": "documents that no internal Z_R theorem-zero or coefficient row was ready.",
        },
        {
            "source_id": "SRC1870_6_1577_no_charge",
            "source_kind": "QR_no_charge_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1577_QR_NO_CHARGE_THEOREM_AUDIT.csv",
            "required_needle": "NCA1577_4_verdict",
            "use_in_1870": "documents current failure of Q_R=0 proof.",
        },
        {
            "source_id": "SRC1870_7_1581_profile",
            "source_kind": "qRhat_profile",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1581_QRHAT_PROFILE_DERIVATION.csv",
            "required_needle": "PROF1581_3_ppn_ratio",
            "use_in_1870": "provides q_R_hat profile and Cassini-facing Q_R relation.",
        },
        {
            "source_id": "SRC1870_8_1581_Cassini",
            "source_kind": "Cassini_bound_nonclaim",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1581_CASSINI_QR_BOUND_ROW_NONCLAIM.csv",
            "required_needle": "CB1581_0_qRhat",
            "use_in_1870": "provides nonclaim Cassini ceiling row for q_R_hat if tails are zero.",
        },
        {
            "source_id": "SRC1870_9_1582_denominator",
            "source_kind": "source_denominator_contract",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1582_SOURCE_DENOMINATOR_CONTRACT.csv",
            "required_needle": "SD1582_0_QR",
            "use_in_1870": "shows Q_R, kappa_W and same-frame GM denominator remain missing.",
        },
        {
            "source_id": "SRC1870_10_1638_chain",
            "source_kind": "PiR_to_QR_chain",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1638_PIR_TO_QR_QRLOCAL_CHAIN.csv",
            "required_needle": "PIRQR1638_5_normalization_bridge",
            "use_in_1870": "provides symbolic Pi_R to Q_R to q_R bridge and normalization blocker.",
        },
        {
            "source_id": "SRC1870_11_1638_blockers",
            "source_kind": "QR_normalization_blockers",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1638_QR_NORMALIZATION_BLOCKER_LEDGER.csv",
            "required_needle": "QRN1638_2_qR_denominator",
            "use_in_1870": "names denominator, W normalization and no-cancellation blockers.",
        },
        {
            "source_id": "SRC1870_12_1639_denominator",
            "source_kind": "conditional_denominator_formula",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1639_NR_DENOMINATOR_DERIVATION.csv",
            "required_needle": "NRD1639_2_compare_coefficients",
            "use_in_1870": "provides conditional q_R=Q_R c^2/(2GM*) formula.",
        },
        {
            "source_id": "SRC1870_13_1639_template",
            "source_kind": "PiR_QR_bound_template",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1639_PIR_QR_QRLOCAL_BOUND_TEMPLATE.csv",
            "required_needle": "PQT1639_0_qR_from_QR",
            "use_in_1870": "provides nonclaim bound template once Q_R and same-frame mass exist.",
        },
        {
            "source_id": "SRC1870_14_1632_R10",
            "source_kind": "R10_kernel_contract",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1632_TAU_R10_KERNEL_CONTRACT.csv",
            "required_needle": "KERN1632_2_finite_operator",
            "use_in_1870": "provides finite R10 Yukawa operator and Green-kernel conditions.",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source_entry in sources:
        source_path = source_entry["source_path"]
        needle = source_entry["required_needle"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_entry["source_id"],
                "source_kind": source_entry["source_kind"],
                "source_path": str(source_path),
                "path_exists": as_bool_text(source_path.exists()),
                "required_needle": needle,
                "needle_found": as_bool_text(path_has_needle(source_path, needle)),
                "use_in_1870": source_entry["use_in_1870"],
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def source_chain_audit() -> list[dict[str, Any]]:
    rows = [
        (
            "SCA1870_0_QR",
            "Q_R",
            "reciprocal exterior charge/hair amplitude",
            "Q_R=W R_AB' or Q_R=-Pi_R depending boundary convention",
            "SYMBOLIC_RELATION_ONLY",
            "MISSING_QR_VALUE_OR_PARENT_NO_CHARGE_THEOREM",
            "without Q_R or Q_R=0, PPN/orbital local hair cannot be scored",
        ),
        (
            "SCA1870_1_ZR",
            "Z_R",
            "kinetic/gradient stiffness for finite R_AB operator",
            "Z_R(nabla^2-lambda_R^-2)R_AB=-J_R",
            "FORMAL_OPERATOR_SLOT_ONLY",
            "MISSING_PARENT_OPERATOR_ZR",
            "without Z_R, neither R10 amplitude nor Q_R normalization has an action scale",
        ),
        (
            "SCA1870_2_MR2",
            "M_R^2",
            "mass-gap/range owner",
            "lambda_R=sqrt(Z_R/M_R^2) only after same-normalization Z_R and M_R^2 exist",
            "FORMAL_RANGE_SLOT_ONLY",
            "MISSING_PARENT_OPERATOR_MR2",
            "without M_R^2, finite Yukawa R10 lane cannot be assigned a range",
        ),
        (
            "SCA1870_3_lambdaR",
            "lambda_R",
            "finite R10/clock/orbital range",
            "lambda_R=sqrt(Z_R/M_R^2), not the Lagrange multiplier lambda_R in the nonpropagating branch",
            "NAME_COLLISION_REQUIRES_CONVENTION_LOCK",
            "MISSING_RANGE_RELATION_AND_SYMBOL_DISAMBIGUATION",
            "must separate range lambda_R from multiplier lambda_R before scoring",
        ),
        (
            "SCA1870_4_JR",
            "J_R",
            "source current driving finite reciprocal residual",
            "bulk/source current enters E_R and two-body R10 exchange legs",
            "FORMAL_SOURCE_SLOT_ONLY",
            "MISSING_SOURCE_CURRENT_OR_MATTER_DESCENT_ZERO",
            "without J_R or source/test beta legs, R10 alpha amplitude is not a prediction",
        ),
        (
            "SCA1870_5_PiR_BR",
            "Pi_R or B_R",
            "boundary momentum/tail and no-charge owner",
            "natural boundary gives Q_R=-Pi_R only after boundary class is fixed",
            "SYMBOLIC_BOUNDARY_RELATION_ONLY",
            "MISSING_BOUNDARY_VARIATION_CLASS_OR_ABSOLUTE_TAIL_BOUND",
            "without boundary silence/tail bound, no local-GR or PPN pass",
        ),
        (
            "SCA1870_6_denominator",
            "N_R or G M_*",
            "source denominator converting Q_R to q_R/q_R_hat",
            "q_R=Q_R c^2/(2GM_*) is present as a conditional formula",
            "CONDITIONAL_FORMULA_FOUND_NONCLAIM",
            "MISSING_QR_VALUE_SAME_FRAME_MASS_W_NORMALIZATION_AND_CONVENTION_LOCK",
            "this is the closest thing to progress: denominator form exists, inputs do not",
        ),
        (
            "SCA1870_7_verdict",
            "first fill",
            "theorem-zero or source-backed numeric row for the shared R10/PPN chain",
            "requires Q_R or no-charge plus Z_R/M_R^2/range/source denominator",
            "NO_FIRST_FILL_READY",
            "MISSING_PARENT_OR_NUMERIC_INPUTS",
            "keep all local arenas blocked; next lock denominator convention or source a real row",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "symbol": symbol,
            "role": role,
            "relation": relation,
            "current_status": status,
            "blocking_gap": blocker,
            "consequence": consequence,
            "numeric_value_present": as_bool_text(False),
            "source_backed": as_bool_text(False),
            "score_ready": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        }
        for audit_id, symbol, role, relation, status, blocker, consequence in rows
    ]


def denominator_convention_gate() -> list[dict[str, Any]]:
    rows = [
        (
            "DCG1870_0_1581_form",
            "q_R_hat=-Q_R/(2*kappa_W*G*M)+O(GM/r)",
            "Cassini-facing profile from W=kappa_W r^2 convention",
            "Q_R, kappa_W, G*M, sign, gauge and tails",
            "CONDITIONAL_PROFILE_NOT_SCORE_READY",
        ),
        (
            "DCG1870_1_1639_form",
            "q_R=Q_R*c^2/(2*G*M_*)",
            "local load denominator from R_AB=q_R L_N and L_N=2GM_*/(r c^2)",
            "Q_R tail coefficient, same-frame M_*, c/G convention and tail normalization",
            "CONDITIONAL_DENOMINATOR_FORMULA_FOUND",
        ),
        (
            "DCG1870_2_convention_collision",
            "q_R_hat versus q_R and kappa_W versus c^2 normalization",
            "two nonclaim denominator conventions must be reconciled before a source row can be scored",
            "normalization map kappa_W <-> c^-2 or explicit decision that rows use different Q_R definitions",
            "MISSING_CONVENTION_LOCK",
        ),
        (
            "DCG1870_3_required_lock",
            "Q_R units, W normalization, source mass frame, and q_R/q_R_hat naming",
            "single source-denominator convention for all PPN/orbital/R10 handoffs",
            "one row with source path, units, sign convention, and no-cancellation policy",
            "NEXT_REQUIRED_OBJECT",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "formula_or_object": formula,
            "meaning": meaning,
            "missing_inputs": missing,
            "status": status,
            "convention_locked": as_bool_text(False),
            "score_ready": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        }
        for gate_id, formula, meaning, missing, status in rows
    ]


def no_charge_return_audit() -> list[dict[str, Any]]:
    rows = [
        (
            "NCR1870_0_boundary_silence",
            "Pi_R=0 -> Q_R=0",
            "would kill massless reciprocal hair and PPN gamma residual",
            "MISSING_PARENT_BOUNDARY_VARIATION_CLASS",
        ),
        (
            "NCR1870_1_matter_descent",
            "delta_RAB S_matter_boundary=0",
            "would prevent local source worldtubes from regenerating Pi_R/Q_R",
            "MISSING_MATTER_DESCENT_PROOF",
        ),
        (
            "NCR1870_2_auxiliary_constraint",
            "parent-owned lambda_multiplier*C_R with no R_AB derivatives",
            "would remove R_AB before current formation",
            "MISSING_MULTIPLIER_ORIGIN_AND_DIRAC_CHAIN",
        ),
        (
            "NCR1870_3_no_derivative_grammar",
            "R_AB cannot carry Z_R or M_R^2 as an independent field",
            "would return to theorem-zero branch rather than finite-bound branch",
            "MISSING_PARENT_CATEGORY_PRINCIPLE",
        ),
        (
            "NCR1870_4_verdict",
            "Q_R=0 no-charge return",
            "sufficient for q_R/q_R_hat=0 only if tails/source/readout vanish too",
            "NO_CHARGE_RETURN_NOT_DERIVED_CURRENT_CORPUS",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "route": route,
            "effect_if_signed": effect,
            "current_status": status,
            "parent_signed": as_bool_text(False),
            "numeric_value_present": as_bool_text(False),
            "source_backed": as_bool_text(False),
            "score_ready": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        }
        for audit_id, route, effect, status in rows
    ]


def r10_ppn_fork_matrix() -> list[dict[str, Any]]:
    rows = [
        (
            "FORK1870_0_theorem_zero",
            "Q_R=0, Z_R absent/constraint-owned, J_R=0, boundary/readout tails=0",
            "local GR candidate; R10/PPN residuals vanish in reciprocal branch",
            "best physics route but not parent-signed",
            "BLOCKED_BY_NO_CHARGE_AND_TYPED_GRAMMAR",
        ),
        (
            "FORK1870_1_massless_hair",
            "Q_R nonzero, M_R^2=0 or no finite range",
            "PPN/orbital local-tail problem, not an R10 Yukawa alpha(lambda) prediction",
            "route to Cassini/q_R bound once denominator convention is locked",
            "BLOCKED_BY_QR_VALUE_AND_DENOMINATOR",
        ),
        (
            "FORK1870_2_massive_yukawa",
            "Z_R>0, M_R^2>0, lambda_range=sqrt(Z_R/M_R^2)",
            "R10/clock/orbital finite-range branch",
            "route to R10 alpha(lambda) only after source/test charges and accepted bound curve",
            "BLOCKED_BY_ZR_MR2_JR_BETA_TAU",
        ),
        (
            "FORK1870_3_source_current",
            "J_R/beta_source/beta_test nonzero",
            "finite two-body exchange amplitude and WEP/clock composition sensitivity",
            "must split source and test legs; no single coupling shortcut",
            "BLOCKED_BY_MATTER_DESCENT_OR_NUMERIC_CHARGES",
        ),
        (
            "FORK1870_4_decision",
            "first-fill route",
            "denominator convention lock is the smallest next executable object",
            "without it neither Q_R bound nor no-charge return can be represented cleanly",
            "SELECT_DENOMINATOR_LOCK_NEXT",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "fork_id": fork_id,
            "branch_condition": condition,
            "arena_consequence": consequence,
            "interpretation": interpretation,
            "current_status": status,
            "score_ready": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        }
        for fork_id, condition, consequence, interpretation, status in rows
    ]


def first_fill_rows() -> list[dict[str, Any]]:
    rows = [
        ("FF1870_0_QR", "Q_R", "reciprocal tail/charge amplitude", "theorem-zero no-charge proof or numeric Q_R with units/sign/source body", "MISSING_QR_VALUE_OR_ZERO_THEOREM"),
        ("FF1870_1_PiR", "Pi_R_boundary_abs", "boundary momentum feeding Q_R", "parent boundary silence proof or absolute finite Pi_R bound", "MISSING_BOUNDARY_MOMENTUM_BOUND"),
        ("FF1870_2_kappaW", "kappa_W", "W(r)=kappa_W r^2 normalization", "parent radial-cell kinetic normalization", "MISSING_W_NORMALIZATION"),
        ("FF1870_3_GM", "G*M_source or M_*", "same-frame source denominator", "declared Newtonian source mass convention in observer frame", "MISSING_SAME_FRAME_SOURCE_DENOMINATOR"),
        ("FF1870_4_ZR", "Z_R", "gradient stiffness/action scale", "parent Hessian/operator coefficient or no-pole theorem", "MISSING_PARENT_OPERATOR_ZR"),
        ("FF1870_5_MR2", "M_R^2", "mass gap/range owner", "same-normalization parent Hessian/mass coefficient", "MISSING_PARENT_OPERATOR_MR2"),
        ("FF1870_6_lambda_range", "lambda_range", "finite range sqrt(Z_R/M_R^2)", "derive from Z_R/M_R^2 after convention lock", "MISSING_RANGE_RELATION"),
        ("FF1870_7_JR", "J_R", "bulk reciprocal source current", "matter/source current map or theorem-zero", "MISSING_SOURCE_CURRENT"),
        ("FF1870_8_beta_source", "beta_source_R", "R10 source leg", "source material charge in R_AB normalization", "MISSING_SOURCE_CHARGE"),
        ("FF1870_9_beta_test", "beta_test_R", "R10 test leg", "test material/readout charge in R_AB normalization", "MISSING_TEST_CHARGE"),
        ("FF1870_10_tail", "epsilon_tail_R", "boundary/readout/source residual envelope", "absolute no-cancellation tail or theorem-zero for all local residuals", "MISSING_ABSOLUTE_TAIL_ENVELOPE"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "fill_id": fill_id,
            "symbol": symbol,
            "role": role,
            "accepted_input": accepted_input,
            "current_status": status,
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "units": "MISSING_UNITS_OR_NORMALIZATION",
            "source_path": "MISSING_SOURCE_PATH",
            "source_anchor": "MISSING_SOURCE_ANCHOR",
            "score_ready": as_bool_text(False),
            "valid_prediction_row": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
            "claim_allowed": as_bool_text(False),
        }
        for fill_id, symbol, role, accepted_input, status in rows
    ]


def claim_gate() -> list[dict[str, Any]]:
    rows = [
        ("CG1870_0_first_fill", "first theorem-zero or source-backed numeric row exists", "BLOCKED", "NO_FIRST_FILL_READY", "provide Q_R/no-charge, Z_R/M_R^2/range, or denominator convention row with source path and units"),
        ("CG1870_1_QR_zero", "Q_R=0 no-charge theorem", "BLOCKED", "NO_CHARGE_RETURN_NOT_DERIVED_CURRENT_CORPUS", "parent boundary/matter/descent/auxiliary proof"),
        ("CG1870_2_R10", "finite R10 Yukawa branch score", "BLOCKED", "MISSING_ZR_MR2_LAMBDA_JR_BETA_TAU_AND_ACCEPTED_BOUND", "same-normalized finite operator, source/test charges, projection kernel, accepted curve"),
        ("CG1870_3_PPN", "PPN q_R/q_R_hat residual score", "BLOCKED", "MISSING_QR_VALUE_DENOMINATOR_AND_TAIL_ENVELOPE", "Q_R or Pi_R value, denominator convention, external bound and no-cancellation vector"),
        ("CG1870_4_local_GR", "local GR/Newton reduction", "BLOCKED", "FINITE_SOURCE_CHAIN_NOT_FILLED_AND_NO_ZERO_THEOREM", "theorem-zero route or complete cross-arena finite residual demonstration"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "blocking_reason": reason,
            "required_before_claim": required,
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        }
        for claim_id, claim, status, reason, required in rows
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1870_0_result",
            "decision": "NO_FIRST_FILL_READY",
            "basis": "all inspected Q_R, Z_R, M_R^2, lambda_range, J_R and boundary/source rows remain theorem-unsigned or numeric-missing.",
            "consequence": "no R10/PPN/clock/orbital/local-GR score from 1870.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1870_1_denominator_progress",
            "decision": "CONDITIONAL_QR_TO_qR_DENOMINATOR_FORMULA_FOUND",
            "basis": "1639 gives q_R=Q_R c^2/(2GM_*) while 1581 gives q_R_hat=-Q_R/(2 kappa_W G M); both are nonclaim and need convention lock.",
            "consequence": "smallest next executable object is a single normalization convention row.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1870_2_fork",
            "decision": "MASSLESS_PPN_HAIR_VS_MASSIVE_R10_BRANCH_FORK_EXPLICIT",
            "basis": "Q_R without M_R^2 is a PPN/orbital tail; Z_R>0 and M_R^2>0 is a finite R10/clock/orbital branch.",
            "consequence": "do not route massless Q_R/r hair into R10 alpha(lambda).",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1870_3_next",
            "decision": "QR_NORMALIZATION_CONVENTION_LOCK_SELECTED_NEXT",
            "basis": "a locked Q_R -> q_R/q_R_hat denominator is required before either no-charge return or finite PPN bound can be scored.",
            "consequence": "1871 should reconcile q_R/q_R_hat, kappa_W, c^2, GM_*, sign and units into one nonclaim convention row.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1870_0_primary",
            "target_doc": "1871-Y5-R2FR-QR-normalization-convention-lock-or-source-denominator-row.md",
            "target_script": "scripts/Y5_R2FR_QR_normalization_convention_lock_or_source_denominator_row_1871.py",
            "objective": "reconcile q_R, q_R_hat, Q_R, Pi_R, kappa_W, c^2 and same-frame G*M into one source-denominator convention row; if impossible, leave a blocker ledger.",
            "selection_status": "selected",
            "success_condition": "one nonclaim denominator convention row that all PPN/orbital/R10 handoffs can reference, or explicit proof the conventions conflict.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1870_1_parallel_zero",
            "target_doc": "1871b-Y5-R2FR-boundary-no-charge-return-PiR-zero-proof-or-tail-bound.md",
            "target_script": "scripts/Y5_R2FR_boundary_no_charge_return_PiR_zero_proof_or_tail_bound_1871b.py",
            "objective": "try to sign Pi_R=0/source-boundary neutrality; if not, create absolute tail-bound input rows.",
            "selection_status": "held_parallel",
            "success_condition": "parent-signed no-charge theorem or source-ready Pi_R/Q_R tail row.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1870_2_parallel_range",
            "target_doc": "1871c-Y5-R2FR-ZR-MR2-range-owner-or-Yukawa-row.md",
            "target_script": "scripts/Y5_R2FR_ZR_MR2_range_owner_or_Yukawa_row_1871c.py",
            "objective": "try to source same-normalization Z_R/M_R^2/lambda_range for the finite R10 branch.",
            "selection_status": "held_parallel",
            "success_condition": "same-normalized range owner or explicit blocker.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "score_ready",
        "valid_prediction_row",
        "source_backed",
        "numeric_value_present",
        "parent_signed",
        "convention_locked",
    }
    for rows in rows_by_name.values():
        for table_row in rows:
            for field_name in claim_fields:
                if str(table_row.get(field_name, "")).strip().lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for table_row in rows:
            contains_missing = any("MISSING_" in str(value) for value in table_row.values())
            if contains_missing:
                for field_name in ("valid_for_claim", "claim_allowed", "score_ready", "valid_prediction_row"):
                    if str(table_row.get(field_name, "")).strip().lower() == "true":
                        return False
    return True


def csvs_parse(paths: list[Path]) -> bool:
    for csv_path in paths:
        with csv_path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
    return True


def copy_branch_outputs(paths: list[Path]) -> None:
    for branch_folder in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
        branch_folder.mkdir(parents=True, exist_ok=True)
    for output_path in paths:
        shutil.copy2(output_path, MICROSCOPE_RESIDUALS / output_path.name)
        shutil.copy2(output_path, QUARANTINE / output_path.name)
        shutil.copy2(output_path, RAB_QUEUE / f"JR1870_{output_path.name}")


def branch_copies_exist(paths: list[Path]) -> bool:
    for output_path in paths:
        expected_paths = [
            MICROSCOPE_RESIDUALS / output_path.name,
            QUARANTINE / output_path.name,
            RAB_QUEUE / f"JR1870_{output_path.name}",
        ]
        if not all(expected_path.exists() for expected_path in expected_paths):
            return False
    return True


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1870*"))


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], non_validation_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    chain_rows = rows_by_name["source_chain_audit"]
    denom_rows = rows_by_name["denominator_convention_gate"]
    nocharge_rows = rows_by_name["no_charge_return_audit"]
    fork_rows = rows_by_name["r10_ppn_fork_matrix"]
    fill_rows = rows_by_name["first_fill_rows"]
    claim_rows = rows_by_name["claim_gate"]
    decision_rows = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]

    checks = [
        {
            "validation_id": "VAL1870_0_sources_exist",
            "status": "PASS" if all(row["path_exists"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source paths exist",
        },
        {
            "validation_id": "VAL1870_1_needles_present",
            "status": "PASS" if all(row["needle_found"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source needles are present",
        },
        {
            "validation_id": "VAL1870_2_chain_no_first_fill",
            "status": "PASS" if any(row["current_status"] == "NO_FIRST_FILL_READY" for row in chain_rows) else "FAIL",
            "detail": "source-chain audit refuses first fill",
        },
        {
            "validation_id": "VAL1870_3_denominator_formula_nonclaim",
            "status": "PASS" if any(row["status"] == "CONDITIONAL_DENOMINATOR_FORMULA_FOUND" for row in denom_rows) else "FAIL",
            "detail": "conditional denominator formula is captured without claim promotion",
        },
        {
            "validation_id": "VAL1870_4_nocharge_not_derived",
            "status": "PASS" if any(row["current_status"] == "NO_CHARGE_RETURN_NOT_DERIVED_CURRENT_CORPUS" for row in nocharge_rows) else "FAIL",
            "detail": "no-charge return remains blocked",
        },
        {
            "validation_id": "VAL1870_5_fork_matrix_explicit",
            "status": "PASS" if any(row["current_status"] == "SELECT_DENOMINATOR_LOCK_NEXT" for row in fork_rows) else "FAIL",
            "detail": "R10/PPN fork selects denominator lock next",
        },
        {
            "validation_id": "VAL1870_6_first_fill_rows_missing",
            "status": "PASS" if len(fill_rows) >= 10 and all(row["valid_for_claim"] == "False" for row in fill_rows) else "FAIL",
            "detail": "first-fill rows are explicit nonclaim missing rows",
        },
        {
            "validation_id": "VAL1870_7_claim_gates_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_rows) else "FAIL",
            "detail": "all source-chain/local-claim gates remain blocked",
        },
        {
            "validation_id": "VAL1870_8_no_claim_flags",
            "status": "PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            "detail": "no generated claim or gate-pass flag is true",
        },
        {
            "validation_id": "VAL1870_9_missing_not_ready",
            "status": "PASS" if missing_rows_not_ready(rows_by_name) else "FAIL",
            "detail": "no MISSING_* row is marked score-ready or claim-ready",
        },
        {
            "validation_id": "VAL1870_10_decision_next",
            "status": "PASS" if any(row["decision"] == "QR_NORMALIZATION_CONVENTION_LOCK_SELECTED_NEXT" for row in decision_rows) else "FAIL",
            "detail": "decision ledger selects QR normalization convention lock next",
        },
        {
            "validation_id": "VAL1870_11_next_selected",
            "status": "PASS" if any(row["route_id"] == "NEXT1870_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "next target selected",
        },
        {
            "validation_id": "VAL1870_12_csv_parse",
            "status": "PASS" if csvs_parse(non_validation_paths) else "FAIL",
            "detail": "all generated non-validation CSVs parse",
        },
        {
            "validation_id": "VAL1870_13_branch_copies",
            "status": "PASS" if branch_copies_exist(non_validation_paths) else "FAIL",
            "detail": "branch/quarantine/queue copies exist",
        },
        {
            "validation_id": "VAL1870_14_pycache_absent",
            "status": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent",
        },
        {
            "validation_id": "VAL1870_15_formalization_untouched",
            "status": "PASS" if formalization_untouched() else "FAIL",
            "detail": "no 1870 outputs found under formalization-workbench",
        },
    ]
    overall_status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL1870_OVERALL",
            "status": overall_status,
            "detail": "1870 QR/ZR/MR2 source-chain first-fill or no-charge return checkpoint",
        }
    )
    return [{**row, "branch_id": BRANCH_ID, "valid_for_claim": as_bool_text(False)} for row in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1870 - Y5/R2FR Q_R/Z_R/M_R^2 Source Chain First Fill Or No-Charge Return",
        "",
        "## Verdict",
        "",
        "1870 tried the first-fill route for the shared R10/PPN chain and did not find a source-backed numeric row or parent-signed theorem-zero. `Q_R`, `Z_R`, `M_R^2`, range, source current, boundary tail, and source/test charges remain missing or conditional.",
        "",
        "The useful progress is that the denominator problem is now sharper. The corpus contains conditional forms `q_R_hat=-Q_R/(2 kappa_W G M)` and `q_R=Q_R c^2/(2 G M_*)`, but those are not yet one convention. Before we can score either a PPN hair branch or a no-charge return, we need a single `Q_R -> q_R/q_R_hat` normalization row with units, sign, source mass frame, and no-cancellation policy.",
        "",
        "**Claim ceiling:** no first coefficient fill, no `Q_R=0`, no `Z_R/M_R^2` range, no R10/PPN/clock/orbital pass, no local-GR/Newton reduction claim, no GitHub action, and no `formalization-workbench` edit is allowed from 1870.",
        "",
        "## Source Register",
        "",
        markdown_table(rows_by_name["source_register"], ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_1870", "valid_for_claim"]),
        "",
        "## Source Chain Audit",
        "",
        markdown_table(rows_by_name["source_chain_audit"], ["audit_id", "symbol", "role", "relation", "current_status", "blocking_gap", "consequence", "valid_for_claim"]),
        "",
        "## Denominator Convention Gate",
        "",
        markdown_table(rows_by_name["denominator_convention_gate"], ["gate_id", "formula_or_object", "meaning", "missing_inputs", "status", "convention_locked", "valid_for_claim"]),
        "",
        "## No-Charge Return Audit",
        "",
        markdown_table(rows_by_name["no_charge_return_audit"], ["audit_id", "route", "effect_if_signed", "current_status", "parent_signed", "valid_for_claim"]),
        "",
        "## R10/PPN Fork Matrix",
        "",
        markdown_table(rows_by_name["r10_ppn_fork_matrix"], ["fork_id", "branch_condition", "arena_consequence", "interpretation", "current_status", "valid_for_claim"]),
        "",
        "## First-Fill Rows",
        "",
        markdown_table(rows_by_name["first_fill_rows"], ["fill_id", "symbol", "role", "accepted_input", "current_status", "numeric_value", "units", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        markdown_table(rows_by_name["claim_gate"], ["claim_id", "claim", "status", "blocking_reason", "required_before_claim", "claim_allowed", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "basis", "consequence", "claim_allowed", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows_by_name["next_target"], ["route_id", "target_doc", "target_script", "objective", "selection_status", "success_condition", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        markdown_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim"]),
        "",
        "## Plain-English Status",
        "",
        "This is a good narrowing, not a win. We now know the next small gear is not a cosmology fit or a new galaxy curve; it is a normalization law. If `Q_R` exists, how exactly does it become the dimensionless local hair `q_R` seen by PPN? Lock that, then either prove `Q_R=0` or bound it. Without that lock, R10 and PPN can talk past each other.",
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "source_chain_audit": source_chain_audit(),
        "denominator_convention_gate": denominator_convention_gate(),
        "no_charge_return_audit": no_charge_return_audit(),
        "r10_ppn_fork_matrix": r10_ppn_fork_matrix(),
        "first_fill_rows": first_fill_rows(),
        "claim_gate": claim_gate(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    non_validation_paths = [path for name, path in OUTPUTS.items() if name != "validation"]
    for output_name, output_path in OUTPUTS.items():
        if output_name != "validation":
            write_csv(output_path, rows_by_name[output_name])
    copy_branch_outputs(non_validation_paths)
    remove_pycache()
    rows_by_name["validation"] = validation_rows(rows_by_name, non_validation_paths)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    copy_branch_outputs([OUTPUTS["validation"]])
    remove_pycache()


if __name__ == "__main__":
    main()
