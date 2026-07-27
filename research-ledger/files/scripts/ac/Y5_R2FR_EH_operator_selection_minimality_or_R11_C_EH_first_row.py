from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1820"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1820-Y5-R2FR-EH-operator-selection-minimality-or-R11-C-EH-first-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1820_0_1819_doc",
        "source_key": "1819_handoff_doc",
        "source_path": ROOT / "1819-Y5-R2FR-local-EH-symplectic-charge-inheritance-or-Cterm-residual-vector.md",
        "needles": ["NEXT1819_0_primary", "EH_OPERATOR_SELECTION_MINIMALITY_NEXT"],
        "role": "1819 selects EH operator selection/minimality and R2/fR as the next target.",
    },
    {
        "source_id": "SRC1820_1_1819_validation",
        "source_key": "1819_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1819_VALIDATION.csv",
        "needles": ["VAL1819_OVERALL", "PASS"],
        "role": "confirms 1819 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1820_2_1819_priority",
        "source_key": "1819_R11_priority",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_R11_PRIORITY_GATE.csv",
        "needles": ["R11P1819_0_R2_fR", "MISSING_MINIMALITY_OR_SCALAR_MODE_COEFFICIENT"],
        "role": "R2/fR scalar mode is the first unresolved C_EH/R11 target.",
    },
    {
        "source_id": "SRC1820_3_1819_CEH_row",
        "source_key": "1819_C_EH_residual",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1819_CTERM_RESIDUAL_VECTOR.csv",
        "needles": ["CTV1819_0_C_EH", "MISSING_EH_CONSTRAINT_ZERO_OR_SOURCE_BACKED_BOUND"],
        "role": "C_EH remains the operator mismatch charge residual.",
    },
    {
        "source_id": "SRC1820_4_1512_selection",
        "source_key": "1512_EH_selection",
        "source_path": RESIDUALS / "P8_Y5_PARENT_EH_1512_SELECTION_THEOREM_ATTEMPT.csv",
        "needles": ["THM1512_2_current_verdict", "NON_EH_VECTOR_REQUIRED"],
        "role": "EH selector exists only as conditional Lovelock-style logic.",
    },
    {
        "source_id": "SRC1820_5_1512_premises",
        "source_key": "1512_premise_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_EH_1512_PREMISE_SIGNING_AUDIT.csv",
        "needles": ["PRE1512_2_second_order", "CENTRAL_BLOCKER_NOT_DERIVED"],
        "role": "second-order metric equations are the central unsigned blocker.",
    },
    {
        "source_id": "SRC1820_6_1512_vector",
        "source_key": "1512_non_EH_vector",
        "source_path": RESIDUALS / "P8_Y5_PARENT_EH_1512_NON_EH_RESIDUAL_VECTOR.csv",
        "needles": ["R11_1512_01", "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT"],
        "role": "R2/fR coefficient row is retained and unfilled.",
    },
    {
        "source_id": "SRC1820_7_1513_minimality",
        "source_key": "1513_primitive_minimality",
        "source_path": RESIDUALS / "P8_Y5_PARENT_MINIMALITY_1513_PRIMITIVE_THEOREM_AUDIT.csv",
        "needles": ["PM1513_6_verdict", "THEOREM_NOT_PROVEN_CURRENT_CORPUS"],
        "role": "primitive minimality/no-higher-derivative theorem is not proven.",
    },
    {
        "source_id": "SRC1820_8_1513_R2FR",
        "source_key": "1513_R2FR_status",
        "source_path": RESIDUALS / "P8_Y5_PARENT_MINIMALITY_1513_R2FR_HIGHER_CURVATURE_STATUS.csv",
        "needles": ["R2FR1513_0_relative_zero", "RELATIVE_THEOREM_ONLY"],
        "role": "R2/fR zero theorem exists only relative to unsigned premises.",
    },
    {
        "source_id": "SRC1820_9_1513_decision",
        "source_key": "1513_operator_decision",
        "source_path": RESIDUALS / "P8_Y5_PARENT_MINIMALITY_1513_OPERATOR_BRANCH_DECISION.csv",
        "needles": ["DEC1513_1_R11_lock", "R11_VECTOR_ACTIVE"],
        "role": "non-EH operator vector remains active after minimality failed.",
    },
    {
        "source_id": "SRC1820_10_1586_signature",
        "source_key": "1586_minimality_signature",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1586_MINIMALITY_SIGNATURE_ATTEMPT.csv",
        "needles": ["MIN1586_4_second_order", "CENTRAL_BLOCKER_NOT_DERIVED"],
        "role": "no-higher-derivative/minimality signature remains unsigned.",
    },
    {
        "source_id": "SRC1820_11_1587_nohair",
        "source_key": "1587_R2FR_nohair",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1587_R2FR_RICCIWEYL_NOHAIR_ATTEMPT.csv",
        "needles": ["NH1587_1_integrated_out_scalar", "COUNTERMODEL_LIVE"],
        "role": "integrated-out scalar can regenerate an R2/fR branch unless forbidden.",
    },
    {
        "source_id": "SRC1820_12_1588_scalaron",
        "source_key": "1588_scalaron_map",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1588_R2FR_SCALARON_MAP.csv",
        "needles": ["SC1588_1_formula", "FORMULA_AVAILABLE_PARENT_COEFFICIENT_MISSING"],
        "role": "finite scalaron formula exists, but parent coefficient is absent.",
    },
    {
        "source_id": "SRC1820_13_1708_priority",
        "source_key": "1708_R11_priority",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1708_R11_PRIORITY_FILL_CONTRACT.csv",
        "needles": ["R11F1708_0_R2_fR", "HIGHEST_FIRST"],
        "role": "R2/fR fill is the highest-priority R11 component.",
    },
    {
        "source_id": "SRC1820_14_1770_dominance",
        "source_key": "1770_EH_dominance",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1770_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
        "needles": ["EHD1770_4_current_verdict", "FAIL_CURRENT_PARENT_PROOF"],
        "role": "EH dominance remains unproven because residual-sector certificates are missing.",
    },
    {
        "source_id": "SRC1820_15_1787_extra",
        "source_key": "1787_extra_sector_silence",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1787_EXTRA_SECTOR_SILENCE_MATRIX.csv",
        "needles": ["ESM1787_0_R2_fR_scalar", "RELATIVE_ZERO_THEOREM_AVAILABLE_PARENT_PREMISE_UNSIGNED"],
        "role": "R2/fR remains the first local risk in the extra-sector silence matrix.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_SOURCE_REGISTER.csv",
    "eh_operator_selection": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_EH_OPERATOR_SELECTION_MINIMALITY_THEOREM.csv",
    "premise_activation": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_PREMISE_ACTIVATION_AUDIT.csv",
    "r2fr_scalar_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_R2FR_SCALAR_MODE_AUDIT.csv",
    "ceh_first_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_C_EH_FIRST_ROW_SCHEMA.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1820_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1820_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for path in {RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "pass", "passed"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    headers = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        text = read_text(path)
        exists = path.exists()
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return rows


def eh_operator_selection_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EOS1820_0_target",
            "claim_piece": "local EH operator selection from MTS primitives",
            "mathematical_statement": "If the compact local exterior branch is 4D, local, diffeomorphism-invariant, metric-only, Levi-Civita, second-order, primitive/minimal, and boundary/topological harmless, then S_ext = int sqrt(-g)(a R - 2 Lambda) + exact/topological terms.",
            "derivation_status": "EXACT_CONDITIONAL_SELECTOR",
            "current_parent_status": "MINIMALITY_AND_SECOND_ORDER_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EOS1820_1_lovelock_gate",
            "claim_piece": "Lovelock-style EH gate",
            "mathematical_statement": "In four dimensions, a local metric-only diffeomorphism-invariant operator with second-order metric equations is EH plus Lambda and topological/boundary terms.",
            "derivation_status": "REFERENCE_THEOREM_SHAPE_AVAILABLE",
            "current_parent_status": "NOT_AN_MTS_PROOF_UNTIL_PARENT_PREMISES_FIRE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EOS1820_2_R2FR_exclusion",
            "claim_piece": "R2/fR scalar-mode exclusion",
            "mathematical_statement": "For f(R)=R+c_R2 R^2+..., f_RR != 0 creates a trace/scalaron mode and fourth-order metric equations; therefore c_R2=f_RR=0 follows only if the parent really supplies metric-only second-order no-extra-scalar minimality.",
            "derivation_status": "RELATIVE_ZERO_THEOREM",
            "current_parent_status": "ACTIVATOR_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EOS1820_3_integrated_out_guard",
            "claim_piece": "no regenerated curvature tower",
            "mathematical_statement": "A hidden scalar or local marker can generate beta^2 R^2/(2 M^2) or f_extra(R) after elimination unless the parent object language forbids the sector before variation.",
            "derivation_status": "COUNTERMODEL_GUARD",
            "current_parent_status": "NO_INTEGRATED_OUT_TOWER_THEOREM_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EOS1820_4_no_smuggling_guard",
            "claim_piece": "EH cannot be imported as the left-hand side",
            "mathematical_statement": "The local equation must remain E_MTS^{mu nu}=G^{mu nu}+Lambda g^{mu nu}+DeltaE_R11^{mu nu} until every retained operator is theorem-zero or bounded.",
            "derivation_status": "GUARDRAIL",
            "current_parent_status": "DELTAE_R11_RETAINED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EOS1820_5_first_row_fallback",
            "claim_piece": "first C_EH/R11 residual row if exclusion fails",
            "mathematical_statement": "If c_R2/f_RR cannot be derived zero, C_EH must carry a source-backed scalar-mode row with coefficient, units, normalization, scalar range, coupling, screening regime, weak-field map and local bound source.",
            "derivation_status": "FALLBACK_ROW_CONTRACT",
            "current_parent_status": "NONCLAIM_SCHEMA_ONLY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "EOS1820_6_verdict",
            "claim_piece": "1820 proves local EH operator selection",
            "mathematical_statement": "The conditional selector is sharp, but current MTS has not signed primitive minimality, no-natural-marker, no-integrated-out-tower, second-order metric-only, no-extra-scalar and boundary silence clauses together.",
            "derivation_status": "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF",
            "current_parent_status": "DEMOTE_TO_C_EH_R2FR_FIRST_ROW",
            "valid_for_claim": False,
        },
    ]


def premise_activation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PAC1820_0_local_4D",
            "premise": "compact local exterior branch is 4D",
            "why_needed": "Lovelock-style selection is a local 4D metric operator theorem",
            "source_anchor": "PRE1512_0_local_4D",
            "current_status": "STRUCTURAL_TARGET_NOT_PARENT_SIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PAC1820_1_metric_only",
            "premise": "observed local action is metric/coframe-only with no independent scalar/vector/domain carriers",
            "why_needed": "extra carriers evade EH selection and can generate source or fifth-force terms",
            "source_anchor": "PRE1512_1_metric_only; PRE1512_4_no_extra_fields",
            "current_status": "NOT_PARENT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PAC1820_2_second_order",
            "premise": "metric equations are strictly second order in the local exterior",
            "why_needed": "kills R2/fR/Ricci2/Weyl2/nonlocal higher-derivative leakage",
            "source_anchor": "PRE1512_2_second_order; MIN1586_4_second_order",
            "current_status": "CENTRAL_BLOCKER_NOT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PAC1820_3_no_natural_marker",
            "premise": "no nonconstant local marker or quotient extension can enter the operator coefficient",
            "why_needed": "forbids F(sigma)R and source/domain-dependent curvature coefficients",
            "source_anchor": "PM1513_2_no_natural_marker; MIN1586_1_no_marker_no_extension",
            "current_status": "NOT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PAC1820_4_no_integrated_tower",
            "premise": "hidden or auxiliary sectors cannot regenerate R2/fR after reduction",
            "why_needed": "otherwise a local scalar can be integrated out into beta^2 R^2/(2 M^2)",
            "source_anchor": "PM1513_4_no_integrated_tower; NH1587_1_integrated_out_scalar",
            "current_status": "NOT_DERIVED_COUNTERMODEL_LIVE",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PAC1820_5_boundary_topological",
            "premise": "boundary/topological terms are harmless for local charge and weak-field readout",
            "why_needed": "prevents exact/topological terms from becoming source, alpha3, xi or Gdot hair",
            "source_anchor": "PRE1512_5_boundary_harmless; CTV1819_3_C_boundary",
            "current_status": "CONDITIONAL_NOT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "PAC1820_6_verdict",
            "premise": "all EH operator selector premises active",
            "why_needed": "only then can R2/fR be set to theorem-zero and C_EH be closed",
            "source_anchor": "THM1512_2_current_verdict; PM1513_6_verdict",
            "current_status": "FAIL_CURRENT_ACTIVATION",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def r2fr_scalar_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_0_operator",
            "object": "R2/fR scalar-mode operator",
            "test_or_formula": "Delta L = sqrt(-g)(c_R2 R^2 + c_fR f_extra(R))",
            "effect_if_live": "extra scalar trace mode, Yukawa/fifth-force channel, PPN gamma/beta shift and C_EH leakage",
            "current_status": "RETAINED_NON_EH_RESIDUAL",
            "required_to_close": "derive c_R2=c_fR=0 or fill source-backed finite row",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_1_relative_zero",
            "object": "relative R2/fR zero theorem",
            "test_or_formula": "f_RR=0 if the local parent action is metric-only, second-order and no-extra-scalar",
            "effect_if_live": "would remove finite scalaron branch only after parent activator is signed",
            "current_status": "RELATIVE_THEOREM_AVAILABLE_PARENT_PREMISE_UNSIGNED",
            "required_to_close": "parent signs second-order/no-extra-scalar/minimality",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_2_scalaron_formula",
            "object": "finite scalaron map",
            "test_or_formula": "for f(R)=R+c_R2 R^2 around flat space, m_s^2=1/(6 c_R2), lambda_s=sqrt(6 c_R2) in c=hbar=1 units",
            "effect_if_live": "maps a sourced c_R2/f_RR into a range lambda_s",
            "current_status": "FORMULA_AVAILABLE_PARENT_COEFFICIENT_MISSING",
            "required_to_close": "c_R2/f_RR coefficient, sign, units and normalization",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_3_coupling",
            "object": "scalar coupling amplitude",
            "test_or_formula": "alpha_s=1/3 only for a simple unscreened metric f(R) scalar universally coupled to matter",
            "effect_if_live": "sets R10/PPN amplitude convention only under a stated matter-coupling regime",
            "current_status": "CONDITIONAL_COUPLING_NOT_MTS_PREDICTION",
            "required_to_close": "MTS matter coupling/readout/screening regime",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_4_integrated_scalar",
            "object": "integrated-out scalar countermodel",
            "test_or_formula": "L contains -1/2 M^2 phi^2 + beta phi R, solve phi=(beta/M^2)R to get beta^2 R^2/(2 M^2)",
            "effect_if_live": "regenerates R2 even if the visible ansatz initially looked EH-like",
            "current_status": "COUNTERMODEL_LIVE",
            "required_to_close": "no-integrated-out-tower theorem or finite coefficient row",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_5_no_marker",
            "object": "marker-prefactor curvature coupling",
            "test_or_formula": "L contains sqrt(-g) F(sigma) R or F(sigma) R^2 with sigma a domain/class/source marker",
            "effect_if_live": "turns local operator coefficients into environment/source functions",
            "current_status": "NO_NATURAL_MARKER_THEOREM_MISSING",
            "required_to_close": "primitive object language and naturality theorem",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_6_response_map",
            "object": "weak-field observable map",
            "test_or_formula": "needs gamma_minus_1, beta_minus_1, alpha(lambda), screening flag and source/readout normalization",
            "effect_if_live": "without this map a finite R2/fR row cannot be compared to R10/PPN/clocks/orbits",
            "current_status": "MISSING_WEAK_FIELD_MAP",
            "required_to_close": "arena-specific response coefficients and bounds",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_7_no_cancellation",
            "object": "no-cancellation guard",
            "test_or_formula": "|C_EH| includes absolute R2/fR contribution before any cancellation with C_extra/C_projector/boundary terms",
            "effect_if_live": "prevents hiding R2/fR inside another residual sector",
            "current_status": "GUARD_REQUIRED",
            "required_to_close": "componentwise theorem-zero or source-backed bound",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "R2A1820_8_verdict",
            "object": "R2/fR scalar-mode closure",
            "test_or_formula": "c_R2=c_fR=0 theorem or finite sourced scalaron row",
            "effect_if_live": "C_EH remains open and local GR/Newton cannot be claimed",
            "current_status": "FAIL_ZERO_PROOF_KEEP_FIRST_ROW_NONCLAIM",
            "required_to_close": "1821 must either sign no-higher-derivative parent minimality or source finite c_R2/f_RR input",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def ceh_first_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CEH1820_0_c_R2_eff",
            "quantity": "c_R2_eff_or_f_RR",
            "definition": "effective normalized R2/fR scalar-mode coefficient in the local exterior operator",
            "formal_expression": "Delta L_R2FR = sqrt(-g)(c_R2_eff R^2 + higher f_RR branch)",
            "required_inputs": "parent coefficient or zero theorem; EH normalization; sign convention; source_path",
            "units": "length_squared_after_EH_normalization",
            "value": "MISSING_PARENT_COEFFICIENT_OR_ZERO_THEOREM",
            "source_path": "",
            "arena_links": "R10_alpha_lambda;PPN_gamma_beta;clock_orbital_range",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CEH1820_1_lambda_s",
            "quantity": "lambda_s",
            "definition": "scalaron range induced by c_R2_eff under the simple metric f(R) branch",
            "formal_expression": "lambda_s=sqrt(6 c_R2_eff) in c=hbar=1 units, only if c_R2_eff>0 and branch assumptions hold",
            "required_inputs": "positive c_R2_eff; unit conversion; branch/screening flag",
            "units": "meters",
            "value": "MISSING_C_R2_EFF",
            "source_path": "",
            "arena_links": "R10_alpha_lambda;orbital_range",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CEH1820_2_alpha_s",
            "quantity": "alpha_s",
            "definition": "Yukawa amplitude for the scalar branch relative to Newtonian gravity",
            "formal_expression": "alpha_s=1/3 only for simple unscreened metric f(R) with universal matter coupling",
            "required_inputs": "matter coupling/readout theorem; screening/environment flag; source normalization",
            "units": "dimensionless",
            "value": "MISSING_MATTER_COUPLING_REGIME",
            "source_path": "",
            "arena_links": "R10_alpha_lambda;PPN_gamma_beta",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CEH1820_3_C_EH_R2FR",
            "quantity": "epsilon_C_EH_R2FR_abs",
            "definition": "absolute C_EH contribution from the R2/fR scalar-mode branch",
            "formal_expression": "abs(int_A C_EH[R2FR])/M_H_ref",
            "required_inputs": "operator coefficient; source curvature scale; annulus normalizer; source_path; no-cancellation guard",
            "units": "dimensionless_charge_fraction",
            "value": "MISSING_NORMALIZER_AND_SOURCE_SCALE",
            "source_path": "",
            "arena_links": "local_charge;PPN;R10",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CEH1820_4_total",
            "quantity": "C_EH_first_R11_scalar_mode_row",
            "definition": "first executable C_EH/R11 row needed if EH operator selection cannot zero R2/fR",
            "formal_expression": "row valid only if c_R2_eff/f_RR, lambda_s, alpha_s, screening, weak-field map, normalizer and source paths are all real",
            "required_inputs": "CEH1820_0 through CEH1820_3 plus arena bound source",
            "units": "row_contract",
            "value": "MISSING_PARENT_INPUTS_ROW_NONCLAIM",
            "source_path": "",
            "arena_links": "R10;PPN;clocks;orbital;local_GR_residual",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1820_0_R2FR_visible_term",
            "countermodel": "the local parent action contains a visible c_R2 R^2 or nonlinear f(R) term",
            "why_it_defeats_claim": "the field equations are higher order and carry a scalar trace mode",
            "blocked_by": "second-order metric-only parent theorem or source-backed scalar-mode coefficient bound",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1820_1_integrated_out_scalar",
            "countermodel": "an auxiliary/hidden scalar couples beta phi R and integrates out to beta^2 R^2/(2 M^2)",
            "why_it_defeats_claim": "R2/fR reappears after reduction even when the visible ansatz starts EH-like",
            "blocked_by": "no-integrated-out-tower theorem or finite scalaron row",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1820_2_marker_prefactor",
            "countermodel": "a covariant source/domain/class marker enters F(sigma)R or F(sigma)R^2",
            "why_it_defeats_claim": "operator coefficients become environment-dependent and evade pure EH selection",
            "blocked_by": "no-natural-marker theorem from the primitive quotient",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1820_3_boundary_not_harmless",
            "countermodel": "a topological/exact term has nonzero boundary readout or charge flux",
            "why_it_defeats_claim": "a formally harmless term becomes observable source/PPN hair",
            "blocked_by": "boundary zero-flux/reference-lock theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1820_4_response_map_missing",
            "countermodel": "finite R2/fR row exists but lacks source/readout/screening response map",
            "why_it_defeats_claim": "alpha(lambda), gamma, beta and local charge residuals cannot be scored safely",
            "blocked_by": "arena-specific weak-field map and bound-source ledger",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1820_0_if_EH_selector_closes",
            "if_closed": "PAC1820_0 through PAC1820_5 parent-sign together",
            "would_buy": "C_EH loses the R2/fR scalar-mode operator leak and the left-hand GR operator is no longer imported",
            "still_missing": "C_extra, C_projector, boundary/reference, R_Hsrc and source calibration",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1820_1_if_R2FR_finite",
            "if_closed": "finite c_R2/f_RR, lambda_s, alpha_s and source maps are sourced",
            "would_buy": "R2/fR becomes empirically bounded instead of hand-waved",
            "still_missing": "actual coefficient source and arena response rows",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1820_2_Newton",
            "if_closed": "R2/fR scalar-mode branch is zero or below local tolerance",
            "would_buy": "one major obstruction to Newton/GR reduction is removed",
            "still_missing": "source mass equality, Poisson/Gauss calibration and remaining R11 families",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1820_3_verdict",
            "if_closed": "1820 alone proves local GR",
            "would_buy": "nothing claimable alone; 1820 only resolves or residualizes the first operator-side scalar leak",
            "still_missing": "current run leaves R2/fR nonclaim and all broader local-GR claims blocked",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1820_0_operator_contract",
            "gate": "EH operator selection theorem contract written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "EOS1820 states the exact conditional selector and the R2/fR exclusion activator",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1820_1_parent_premises",
            "gate": "all parent minimality/second-order premises signed",
            "current_status": "BLOCKED",
            "reason": "PAC1820 has unsigned metric-only, second-order, no-marker, no-integrated-tower and boundary clauses",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1820_2_R2FR_zero",
            "gate": "R2/fR scalar-mode coefficient theorem-zero",
            "current_status": "BLOCKED",
            "reason": "relative zero theorem cannot activate without parent second-order/no-extra-scalar/minimality",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1820_3_finite_row",
            "gate": "C_EH/R11 finite scalar-mode row source-backed",
            "current_status": "BLOCKED",
            "reason": "CEH1820 rows are missing parent coefficient, units, normalizer, coupling and source paths",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1820_4_local_GR",
            "gate": "local GR/Newton promotion allowed",
            "current_status": "REFUSED",
            "reason": "C_EH remains nonclaim and other C-term/R_Hsrc/source-calibration gates are still open",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1820_0_EH_operator_selection",
            "claim": "MTS local operator is EH plus harmless terms",
            "status": "BLOCKED",
            "reason": "the selector is conditional and the parent premises are unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1820_1_R2FR_zero",
            "claim": "R2/fR scalar branch is theorem-zero",
            "status": "BLOCKED",
            "reason": "relative zero theorem has no parent activator in the current corpus",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1820_2_scalaron_score",
            "claim": "finite R2/fR scalaron branch is scored against R10/PPN",
            "status": "REFUSED",
            "reason": "coefficient, units, coupling, screening, normalizer and arena bounds are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1820_3_local_GR_PPN",
            "claim": "local GR/PPN follows from 1820",
            "status": "REFUSED",
            "reason": "1820 is one operator-side subgate; C_extra/C_projector/boundary/R_Hsrc/source calibration remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1820_0_theorem_result",
            "decision": "EH_OPERATOR_SELECTOR_CONTRACT_ONLY",
            "reason": "the Lovelock-style selection route is exact, but MTS has not derived the needed parent premises",
            "next_action": "do not promote local GR; keep DeltaE_R11 explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1820_1_R2FR_status",
            "decision": "R2FR_ZERO_PROOF_FAILS_CURRENT_PARENT",
            "reason": "R2/fR can be killed only relative to second-order/no-extra-scalar/minimality, and those clauses are unsigned",
            "next_action": "create nonclaim C_EH/R11 scalar-mode first row",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1820_2_first_row",
            "decision": "C_EH_R2FR_FIRST_ROW_READY_SCHEMA_ONLY",
            "reason": "CEH1820 rows name the needed coefficient, range, coupling and charge residual inputs without pretending they exist",
            "next_action": "source or derive c_R2_eff/f_RR and response maps before any R10/PPN score",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1820_3_best_next",
            "decision": "NO_HIGHER_DERIVATIVE_PARENT_MINIMALITY_NEXT",
            "reason": "the least scrutinizable route is still derivation-first: prove the parent cannot generate higher-derivative curvature terms; otherwise finite scalar-mode bound rows are unavoidable",
            "next_action": "1821-Y5-R2FR-no-higher-derivative-parent-minimality-or-R2FR-bound-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1820_0_primary",
            "next_target": "1821-Y5-R2FR-no-higher-derivative-parent-minimality-or-R2FR-bound-row.md",
            "script": "scripts/Y5_R2FR_no_higher_derivative_parent_minimality_or_R2FR_bound_row.py",
            "objective": "try to prove the parent object-language/no-integrated-out-tower theorem that forbids R2/fR; if not, fill a source-ready finite scalar-mode bound row without claiming a pass",
            "selection_status": "selected",
            "success_condition": "parent-signed no-higher-derivative theorem, or CEH/R2FR coefficient-bound rows remain valid_for_claim=false with all blockers explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1820_1_parallel",
            "next_target": "1821b-Y5-R2FR-weak-field-scalaron-response-map.md",
            "script": "scripts/Y5_R2FR_weak_field_scalaron_response_map.py",
            "objective": "derive the alpha(lambda), gamma, beta, screening and source-normalization map for any finite R2/fR branch",
            "selection_status": "held_parallel",
            "success_condition": "response map has source paths, units, normalizer and no-cancellation guard before scoring",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "eh_operator_selection": eh_operator_selection_rows(),
        "premise_activation": premise_activation_rows(),
        "r2fr_scalar_audit": r2fr_scalar_audit_rows(),
        "ceh_first_row": ceh_first_row_rows(),
        "countermodel_ledger": countermodel_rows(),
        "gr_newton_impact": gr_newton_impact_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(output, target_dir / output.name)


def branch_copies_exist() -> bool:
    for output in generated_csvs():
        for target_dir in (MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE):
            if not (target_dir / output.name).exists():
                return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    names = {DOC_PATH.name, OUTPUTS["validation"].name} | {path.name for path in generated_csvs()}
    return not any(path.name in names for path in FORMALIZATION.rglob("*") if path.is_file())


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    allowed_gate_pass = {"AC1820_0_operator_contract"}
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ("valid_for_claim", "claim_allowed_now", "claim_allowed", "score_ready", "gate_pass"):
                if field in row and boolish(row[field]):
                    if field == "gate_pass" and row.get("gate_id") in allowed_gate_pass:
                        continue
                    return False
    return True


def missing_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text and (
                boolish(row.get("score_ready", False))
                or boolish(row.get("valid_for_claim", False))
                or boolish(row.get("claim_allowed", False))
                or boolish(row.get("claim_allowed_now", False))
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1820_0_operator_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1820_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1820_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1820_2_selector_contract_written",
            any(row["theorem_id"] == "EOS1820_0_target" and row["derivation_status"] == "EXACT_CONDITIONAL_SELECTOR" for row in rows_map["eh_operator_selection"]),
            "EH operator selection/minimality contract is written",
        ),
        (
            "VAL1820_3_R2FR_relative_zero_only",
            any(row["theorem_id"] == "EOS1820_2_R2FR_exclusion" and row["current_parent_status"] == "ACTIVATOR_UNSIGNED" for row in rows_map["eh_operator_selection"]),
            "R2/fR exclusion remains a relative zero theorem only",
        ),
        (
            "VAL1820_4_theorem_not_promoted",
            any(row["theorem_id"] == "EOS1820_6_verdict" and row["derivation_status"] == "CONDITIONAL_THEOREM_NOT_CURRENT_PROOF" for row in rows_map["eh_operator_selection"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["eh_operator_selection"]),
            "1820 theorem is not promoted as current proof",
        ),
        (
            "VAL1820_5_premises_blocked",
            any(row["premise_id"] == "PAC1820_6_verdict" and row["current_status"] == "FAIL_CURRENT_ACTIVATION" for row in rows_map["premise_activation"])
            and all(not boolish(row["parent_signed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["premise_activation"]),
            "parent premise activation remains blocked",
        ),
        (
            "VAL1820_6_R2FR_audit_blocked",
            any(row["audit_id"] == "R2A1820_8_verdict" and row["current_status"] == "FAIL_ZERO_PROOF_KEEP_FIRST_ROW_NONCLAIM" for row in rows_map["r2fr_scalar_audit"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["r2fr_scalar_audit"]),
            "R2/fR scalar-mode audit remains nonclaim",
        ),
        (
            "VAL1820_7_CEH_first_row_nonclaim",
            any(row["row_id"] == "CEH1820_4_total" and row["value"] == "MISSING_PARENT_INPUTS_ROW_NONCLAIM" for row in rows_map["ceh_first_row"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["ceh_first_row"]),
            "C_EH/R11 first row is schema-only and nonclaim",
        ),
        (
            "VAL1820_8_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain retained",
        ),
        (
            "VAL1820_9_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1820_10_acceptance_blocks",
            any(row["gate_id"] == "AC1820_0_operator_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1820_11_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all EH/R2FR/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1820_12_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1820_13_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1820_14_decision_next",
            any(row["decision_id"] == "DEC1820_3_best_next" and row["decision"] == "NO_HIGHER_DERIVATIVE_PARENT_MINIMALITY_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects no-higher-derivative parent minimality next",
        ),
        (
            "VAL1820_15_next_selected",
            any(row["route_id"] == "NEXT1820_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1820_16_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1820 CSVs parse"),
        ("VAL1820_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1820_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1820_19_formalization_untouched", formalization_untouched(), "no 1820 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1820_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1820 EH operator selection minimality or R11 C_EH first row checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1820 Y5 R2FR EH operator selection minimality or R11 C_EH first row",
            "",
            "**Progress:** 1820 attacks the left-hand operator, not the data score. It writes the exact conditional route that would select EH and kill the R2/fR scalar-mode branch, then checks whether the current parent corpus actually signs the needed premises.",
            "",
            "**Current verdict:** useful but not victorious. The EH selector is mathematically sharp, and the R2/fR scalar branch is zero if metric-only second-order no-extra-scalar minimality is parent-signed. The current corpus does not sign those premises, so the route demotes to a nonclaim `C_EH/R11` first-row schema.",
            "",
            "**Claim ceiling:** no EH operator claim, no R2/fR zero claim, no scalaron/R10/PPN score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1820.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## EH Operator Selection Minimality Theorem",
            markdown_table(rows_map["eh_operator_selection"], ["theorem_id", "claim_piece", "mathematical_statement", "derivation_status", "current_parent_status", "valid_for_claim"]),
            "",
            "## Premise Activation Audit",
            markdown_table(rows_map["premise_activation"], ["premise_id", "premise", "why_needed", "source_anchor", "current_status", "parent_signed", "valid_for_claim"]),
            "",
            "## R2FR Scalar Mode Audit",
            markdown_table(rows_map["r2fr_scalar_audit"], ["audit_id", "object", "test_or_formula", "effect_if_live", "current_status", "required_to_close", "score_ready", "valid_for_claim"]),
            "",
            "## C_EH First Row Schema",
            markdown_table(rows_map["ceh_first_row"], ["row_id", "quantity", "definition", "formal_expression", "required_inputs", "units", "value", "arena_links", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "why_it_defeats_claim", "blocked_by", "retained", "valid_for_claim"]),
            "",
            "## GR Newton Impact Ledger",
            markdown_table(rows_map["gr_newton_impact"], ["impact_id", "if_closed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a clean narrowing, not a defeat. The R2/fR branch is now boxed into one of two honest paths: either MTS proves a real parent no-higher-derivative/minimality theorem, or it carries a finite scalar-mode coefficient into R10/PPN/clocks/orbits as an explicit residual. No more smuggling EH in through the side door.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1820 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
