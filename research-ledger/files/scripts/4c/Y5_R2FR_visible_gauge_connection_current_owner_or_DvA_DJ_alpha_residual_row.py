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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1814"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1814-Y5-R2FR-visible-gauge-connection-current-owner-or-DvA-DJ-alpha-residual-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1814_0_1813_doc",
        "source_key": "1813_handoff_doc",
        "source_path": ROOT / "1813-Y5-R2FR-A-owned-placement-and-EM-level-owner-or-alpha-marker-residual-row.md",
        "needles": ["DEC1813_3_best_next", "NEXT1813_0_primary"],
        "role": "1813 selects visible gauge connection/current owner as the next target.",
    },
    {
        "source_id": "SRC1814_1_1813_validation",
        "source_key": "1813_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1813_VALIDATION.csv",
        "needles": ["VAL1813_OVERALL", "PASS"],
        "role": "confirms 1813 split-contract checkpoint passed as nonclaim.",
    },
    {
        "source_id": "SRC1814_2_1813_split_theorem",
        "source_key": "1813_A_owned_split",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_A_OWNED_SPLIT_THEOREM.csv",
        "needles": ["AST1813_1_split_contract", "A_Q^vis"],
        "role": "split contract distinguishing visible connection from EM level owner.",
    },
    {
        "source_id": "SRC1814_3_1813_em_contract",
        "source_key": "1813_EM_level_owner_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_EM_LEVEL_OWNER_CONTRACT.csv",
        "needles": ["ELO1813_0_visible_connection", "ELO1813_4_current_owner"],
        "role": "latest visible connection and same-current owner contract clauses.",
    },
    {
        "source_id": "SRC1814_4_1813_residual",
        "source_key": "1813_alpha_marker_residual_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_ALPHA_MARKER_RESIDUAL_ROW_SCHEMA.csv",
        "needles": ["AMR1813_0_Dv_AQ", "AMR1813_3_current_rescale"],
        "role": "A_Q/current residual fallback rows staged by 1813.",
    },
    {
        "source_id": "SRC1814_5_1414_current_owner",
        "source_key": "1414_beta_source_alpha_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv",
        "needles": ["BSA1414_2_Noether_current_owner", "MISSING"],
        "role": "older same-current owner blocker.",
    },
    {
        "source_id": "SRC1814_6_1414_verdict",
        "source_key": "1414_beta_source_alpha_verdict",
        "source_path": RESIDUALS / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv",
        "needles": ["BSA1414_5_verdict", "OWNER_NOT_DERIVED"],
        "role": "current owner route requires finite target rows if not derived.",
    },
    {
        "source_id": "SRC1814_7_765_maxwell_gate",
        "source_key": "765_maxwell_kinetic_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "needles": ["MKI765_0_projection", "MKI765_3_same_current"],
        "role": "Maxwell inheritance clauses for projection and same current.",
    },
    {
        "source_id": "SRC1814_8_765_total",
        "source_key": "765_maxwell_total_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "needles": ["MKI765_5_total", "blocked"],
        "role": "Maxwell inheritance cannot be promoted yet.",
    },
    {
        "source_id": "SRC1814_9_765_rescale",
        "source_key": "765_current_rescale_counterexample",
        "source_path": RESIDUALS / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["RCE765_2_current_rescale", "different source/test charge response"],
        "role": "current/source-test rescaling counterexample.",
    },
    {
        "source_id": "SRC1814_10_642_maxwell",
        "source_key": "642_maxwell_descent",
        "source_path": RESIDUALS / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "needles": ["MD642_0_Bianchi", "MD642_2_current_conservation"],
        "role": "conditional Maxwell connection/current support.",
    },
    {
        "source_id": "SRC1814_11_642_alpha",
        "source_key": "642_alpha_blocker",
        "source_path": RESIDUALS / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "needles": ["MD642_4_alpha_constant", "blocked"],
        "role": "Maxwell form does not derive measured alpha owner.",
    },
    {
        "source_id": "SRC1814_12_781_action",
        "source_key": "781_parent_action",
        "source_path": RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
        "needles": ["MPC781_2_geometry_stack", "D_m=D[e_obs,A_owned]"],
        "role": "candidate parent matter derivative stack containing owned gauge connection.",
    },
    {
        "source_id": "SRC1814_13_781_readout",
        "source_key": "781_readout_action",
        "source_path": RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
        "needles": ["MPC781_5_readout_action", "Lie_v O_i=0"],
        "role": "candidate readout action requiring invisible observables.",
    },
    {
        "source_id": "SRC1814_14_1056_norm",
        "source_key": "1056_vertical_generator_norm",
        "source_path": RESIDUALS / "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv",
        "needles": ["VNA1056_3_same_current_owner", "NOT_PARENT_SIGNED"],
        "role": "same generator/current owner remains unsigned.",
    },
    {
        "source_id": "SRC1814_15_1056_verdict",
        "source_key": "1056_alpha_owner_verdict",
        "source_path": RESIDUALS / "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv",
        "needles": ["VNA1056_6_verdict", "ALPHA_OWNER_NOT_DERIVED_RETAIN_B_ALPHA"],
        "role": "alpha owner cannot be promoted while current rescaling remains legal.",
    },
    {
        "source_id": "SRC1814_16_1480_current_label",
        "source_key": "1480_current_label_obstruction",
        "source_path": RESIDUALS / "P8_Y5_R10_1480_HOM_OBSTRUCTION_LEDGER.csv",
        "needles": ["HOB1480_3_current_label", "CURRENT_OWNER_UNSIGNED"],
        "role": "current/source-normalization label obstruction.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_SOURCE_REGISTER.csv",
    "connection_current_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv",
    "visible_connection_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_OWNER_AUDIT.csv",
    "current_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_CURRENT_OWNER_AUDIT.csv",
    "dva_dj_residual": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_DVA_DJ_ALPHA_RESIDUAL_ROW_SCHEMA.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1814_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1814_VALIDATION.csv",
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


def connection_current_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VCC1814_0_target",
            "claim": "visible gauge connection and source/test current share one parent owner",
            "mathematical_statement": "If A_parent=A_Q^vis T_Q+A_perp is parent-defined, T_Q has fixed nonrescalable normalization, ordinary matter uses D_m[A_Q^vis], J_Q=delta S_matter/delta A_Q^vis is the T_Q Noether/Ward current, and source/test readouts use that same J_Q with no c_A or kappa_A map, then the EM source/test normalization cannot vary independently of the visible connection.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "current_corpus_status": "ANTECEDENTS_NOT_JOINTLY_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VCC1814_1_connection_projection",
            "claim": "A_Q^vis is an induced parent connection",
            "mathematical_statement": "A_Q^vis is legitimate only if it is the T_Q projection of a parent connection before readout, not an appended Maxwell closure field.",
            "proof_status": "NECESSARY_CONNECTION_CONDITION",
            "current_corpus_status": "PROJECTION_TEMPLATE_ONLY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VCC1814_2_current_variation",
            "claim": "J_Q is fixed by parent matter action variation",
            "mathematical_statement": "J_Q := delta S_matter/delta A_Q^vis with charge labels as fixed T_Q representation weights; this removes independent source/test current normalization only if no further current morphism is available.",
            "proof_status": "EXACT_CONDITIONAL_VARIATION",
            "current_corpus_status": "NOETHER_CURRENT_OWNER_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VCC1814_3_rescaling_exclusion",
            "claim": "current rescaling is forbidden",
            "mathematical_statement": "Maps J_A -> c_A J_A, source labels A -> kappa_A, or readout-worldtube selectors must be ill-typed parent morphisms, otherwise WEP/R10/source-test alpha branches remain live finite residuals.",
            "proof_status": "REQUIRED_NO_MORPHISM_CONDITION",
            "current_corpus_status": "CURRENT_RESCALING_COUNTERMODEL_SURVIVES",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "VCC1814_4_verdict",
            "claim": "1814 proves visible connection/current owner in the current corpus",
            "mathematical_statement": "VCC1814_1 through VCC1814_3 close in one parent action branch with source/test readout transfer",
            "proof_status": "CONNECTION_CURRENT_OWNER_CONTRACT_NOT_CURRENT_PROOF",
            "current_corpus_status": "DEMOTE_TO_DVA_DJ_RESIDUAL_ROWS",
            "valid_for_claim": False,
        },
    ]


def visible_connection_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VGA1814_0_parent_connection_projection",
            "object": "A_parent -> A_Q^vis T_Q",
            "current_status": "TEMPLATE_ONLY_NOT_PARENT_SIGNED",
            "source_anchor": "MKI765_0_projection; ELO1813_0_visible_connection",
            "would_close": "makes A_Q^vis a parent connection rather than a later Maxwell field",
            "missing_for_claim": "parent bundle, generator T_Q, projection map, connection normalization and gauge redundancy",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VGA1814_1_Dm_matter_connection",
            "object": "D_m[e_obs,A_Q^vis]",
            "current_status": "CANDIDATE_CONTRACT_NOT_ACTION_SIGNED",
            "source_anchor": "MPC781_2_geometry_stack; MD642_3_Lorentz_readout",
            "would_close": "puts charged matter coupling inside the same ordinary matter derivative stack",
            "missing_for_claim": "parent matter category and proof ordinary charged fields are sections of this connection",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VGA1814_2_Dv_AQ_zero",
            "object": "D_v A_Q^vis",
            "current_status": "MISSING_DV_AQ_VALUE_OR_THEOREM_ZERO",
            "source_anchor": "AMR1813_0_Dv_AQ",
            "would_close": "connection column is invisible to retained local vertical directions",
            "missing_for_claim": "Dq/connection-column theorem-zero or finite source-backed D_v A_Q row with norm",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "VGA1814_3_verdict",
            "object": "visible gauge connection owner",
            "current_status": "VISIBLE_CONNECTION_OWNER_NOT_DERIVED",
            "source_anchor": "VGA1814_0 through VGA1814_2",
            "would_close": "first half of same-current owner theorem",
            "missing_for_claim": "projection, matter derivative ownership and D_v A_Q silence all closed",
            "valid_for_claim": False,
        },
    ]


def current_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1814_0_noether_current",
            "object": "J_Q=delta S_matter/delta A_Q^vis",
            "current_status": "NOETHER_CURRENT_OWNER_MISSING",
            "source_anchor": "BSA1414_2_Noether_current_owner; MKI765_3_same_current",
            "would_close": "ties charge labels, interaction current and source/test normalization to one action variation",
            "missing_for_claim": "parent matter action variation, current_id, charge_unit_owner and material/readout transfer",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1814_1_current_conservation",
            "object": "d*J_Q=0 or nabla_mu J_Q^mu=0",
            "current_status": "CONDITIONAL_SUPPORT_ONLY",
            "source_anchor": "MD642_2_current_conservation",
            "would_close": "gives Ward/Noether support once the current owner is identified",
            "missing_for_claim": "identification of relative/boundary current with observed EM source current",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1814_2_no_current_rescale",
            "object": "J_A -> c_A J_A",
            "current_status": "COUNTEREXAMPLE_SURVIVES",
            "source_anchor": "BSA1414_4_no_current_rescaling; RCE765_2_current_rescale; HOB1480_3_current_label",
            "would_close": "prevents source/test charge response from being fitted independently of Maxwell current",
            "missing_for_claim": "object-language theorem banning current/source normalization labels or finite c_A row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1814_3_source_test_transfer",
            "object": "WEP/R10/source-test current readout",
            "current_status": "READOUT_TRANSFER_UNSIGNED",
            "source_anchor": "BSA1414_3_WEP_source_leg; MPC781_5_readout_action",
            "would_close": "lets WEP/R10 use the same current without an arena-specific source factor",
            "missing_for_claim": "official source worldtube/readout kernel or theorem that readout is pure postprocessing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "COA1814_4_verdict",
            "object": "same Noether/current owner",
            "current_status": "CURRENT_OWNER_NOT_DERIVED",
            "source_anchor": "COA1814_0 through COA1814_3",
            "would_close": "source/test current rescaling branch would become theorem-zero",
            "missing_for_claim": "Noether current owner, no-rescaling theorem and readout transfer all closed",
            "valid_for_claim": False,
        },
    ]


def residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DJ1814_0_Dv_AQ",
            "quantity": "epsilon_Dv_AQ_abs",
            "definition": "visible connection derivative along retained local vertical directions",
            "formal_expression": "||D_v A_Q^vis||",
            "zero_condition": "A_Q^vis is a parent-owned Q_vis connection column and v lies in ker(Dq) for that column",
            "required_inputs": "direction_id; connection_component; derivative_or_zero_theorem; norm; units; source_path",
            "current_status": "MISSING_DV_AQ_VALUE_OR_THEOREM_ZERO",
            "units": "connection_norm_or_dimensionless_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_AQ_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DJ1814_1_Dv_JQ",
            "quantity": "epsilon_Dv_JQ_abs",
            "definition": "Noether/source current derivative along retained local vertical directions",
            "formal_expression": "||D_v J_Q||/||J_Q||",
            "zero_condition": "J_Q is a parent Noether current from the same A_Q^vis action variation and has no hidden/source-label argument",
            "required_inputs": "current_id; D_v_JQ_or_zero_theorem; current_norm; units; source_path",
            "current_status": "MISSING_DV_JQ_VALUE_OR_THEOREM_ZERO",
            "units": "fractional_current_norm",
            "source_path": "",
            "common_normalizer": "MISSING_JQ_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DJ1814_2_current_rescale",
            "quantity": "epsilon_cA_abs",
            "definition": "species/source/test current normalization mismatch",
            "formal_expression": "sup_A |Delta c_A| or sup_A |D_v ln c_A|",
            "zero_condition": "current/source normalization labels are not valid parent morphisms",
            "required_inputs": "species_or_source_id; c_A_or_zero_theorem; WEP/R10 projection; units; source_path",
            "current_status": "MISSING_NO_CURRENT_RESCALE_THEOREM_OR_C_A_BOUND",
            "units": "dimensionless_current_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_CURRENT_RESCALE_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DJ1814_3_source_test_transfer",
            "quantity": "epsilon_source_test_transfer_abs",
            "definition": "arena readout/source-worldtube transfer mismatch from J_Q to source/test charge",
            "formal_expression": "||K_arena[J_Q]-J_Q||/||J_Q||",
            "zero_condition": "source/test readout is pure postprocessing of the same parent current",
            "required_inputs": "arena; transfer_kernel; mismatch_or_zero_theorem; units; source_path",
            "current_status": "MISSING_SOURCE_TEST_TRANSFER_OR_VALUE",
            "units": "dimensionless_transfer_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_TRANSFER_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "DJ1814_4_total",
            "quantity": "epsilon_connection_current_total_abs",
            "definition": "total no-cancellation envelope for visible connection/current owner failure",
            "formal_expression": "abs(DJ1814_0)+abs(DJ1814_1)+abs(DJ1814_2)+abs(DJ1814_3)",
            "zero_condition": "all connection/current owner clauses theorem-zero or all finite components source-backed",
            "required_inputs": "all DJ1814 component values; common normalizer; source paths; arena projection",
            "current_status": "MISSING_COMPONENT_VALUES_AND_COMMON_NORMALIZER",
            "units": "absolute_no_cancellation_envelope",
            "source_path": "",
            "common_normalizer": "MISSING_TOTAL_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1814_0_appended_Maxwell",
            "countermodel": "A_Q is appended as a Maxwell closure field after parent action",
            "why_it_defeats_claim": "connection then has the right equations but not a parent MTS owner",
            "blocked_by": "parent connection projection A_parent=A_Q T_Q+A_perp",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1814_1_current_rescale",
            "countermodel": "S_int=sum_A q_A(X) int A_Q J_A or J_A -> c_A J_A",
            "why_it_defeats_claim": "source/test response varies independently of Maxwell kinetic/connection owner",
            "blocked_by": "same Noether current owner and no current-label morphism theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1814_2_source_readout_selector",
            "countermodel": "readout/source-worldtube selector maps J_Q to arena-specific effective current",
            "why_it_defeats_claim": "WEP/R10 can see a current different from the parent variation current",
            "blocked_by": "source/test transfer theorem or finite transfer residual row",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1814_3_generator_rescale",
            "countermodel": "T_Q and A_Q rescaled with compensating charge labels",
            "why_it_defeats_claim": "charge/current normalization remains conventional without a fixed generator norm",
            "blocked_by": "nonrescalable T_Q norm/lattice plus same-current owner",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1814_0_connection_owner",
            "if_closed": "A_Q^vis is a parent-owned visible connection",
            "would_buy": "EM coupling enters ordinary matter through a derived connection rather than an appended field",
            "still_missing": "current owner, unique F2, alpha level, readout closure and full q/Dq geometry",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1814_1_current_owner",
            "if_closed": "same Noether current owner is parent-signed",
            "would_buy": "source/test current rescaling branch is structurally removed for WEP/R10 alpha channels",
            "still_missing": "source/test transfer and no current-label morphism theorem remain unsigned",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1814_2_GR_Newton_source",
            "if_closed": "connection/current owner closes with matter-functor signature",
            "would_buy": "source universality moves closer to derivable GR/Newton rather than fitted equivalence",
            "still_missing": "Hilbert source owner, Poisson/EH limit, measured-G guard, PPN and boundary support",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1814_3_verdict",
            "if_closed": "1814 package closes",
            "would_buy": "major source/test coupling route would be theorem-zero",
            "still_missing": "current corpus does not close it; residual rows remain schema-only",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1814_0_theorem_contract",
            "gate": "visible connection/current theorem written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "VCC1814 gives an exact conditional route to same-current ownership",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1814_1_visible_connection",
            "gate": "A_Q^vis parent connection owner closes",
            "current_status": "BLOCKED",
            "reason": "VGA1814_3 remains VISIBLE_CONNECTION_OWNER_NOT_DERIVED",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1814_2_current_owner",
            "gate": "same Noether current owner closes",
            "current_status": "BLOCKED",
            "reason": "COA1814_4 remains CURRENT_OWNER_NOT_DERIVED",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1814_3_residual_values",
            "gate": "D_v A_Q/D_v J_Q residual rows source-backed",
            "current_status": "BLOCKED",
            "reason": "DJ1814 rows contain missing values, source paths and normalizers",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1814_4_local_promotion",
            "gate": "WEP/R10/PPN/local-GR promotion allowed",
            "current_status": "REFUSED",
            "reason": "connection/current contract alone is not a local-GR derivation or finite arena pass",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1814_0_connection_current_owner",
            "claim": "visible connection and current owner are proved",
            "status": "BLOCKED",
            "reason": "VCC1814 is exact conditional but projection/current/readout antecedents are unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1814_1_current_rescaling_zero",
            "claim": "current/source-test rescaling is theorem-zero",
            "status": "BLOCKED",
            "reason": "current-label and source/readout selector countermodels survive",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1814_2_alpha_WEP_R10",
            "claim": "alpha WEP/R10 source-test branch passes",
            "status": "BLOCKED",
            "reason": "D_v A_Q/D_v J_Q rows are not sourced and alpha level/unique F2 remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1814_3_local_GR_Newton",
            "claim": "local GR/Newton/PPN follows",
            "status": "REFUSED",
            "reason": "1814 is a source/test coupling subgate, not the full GR reduction",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1814_0_theorem_result",
            "decision": "CONNECTION_CURRENT_OWNER_EXACT_CONDITIONAL",
            "reason": "if parent projection, matter variation, no current rescaling and source/test transfer all close, then A_Q and J_Q share one owner",
            "next_action": "keep as theorem contract, not claim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1814_1_current_status",
            "decision": "CURRENT_OWNER_NOT_DERIVED",
            "reason": "A_Q projection is template-only, Noether current owner is missing, and c_A/source-readout countermodels survive",
            "next_action": "retain D_v A_Q/D_v J_Q/current-rescale residual schema",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1814_2_residual_status",
            "decision": "DVA_DJ_RESIDUAL_SCHEMA_READY_NONCLAIM",
            "reason": "D_v A_Q, D_v J_Q, c_A and source/test transfer rows are explicit but have no sourced values",
            "next_action": "fill no row without units, source path, common normalizer and no-cancellation guard",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1814_3_best_next",
            "decision": "NOETHER_CURRENT_OWNER_NO_RESCALE_NEXT",
            "reason": "the tightest next proof is whether parent matter-action naturality forbids J_A -> c_A J_A before arena readout",
            "next_action": "1815-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1814_0_primary",
            "next_target": "1815-Y5-R2FR-Noether-current-owner-and-no-current-rescale-proof-or-cA-bound-row.md",
            "script": "scripts/Y5_R2FR_Noether_current_owner_and_no_current_rescale_proof_or_cA_bound_row.py",
            "objective": "try to prove the same Noether current owner and ban J_A -> c_A J_A/current-label morphisms; if not, source a finite c_A bound row",
            "selection_status": "selected",
            "success_condition": "Noether current owner/no-rescale theorem-zero, or c_A residual bound row is source-backed and remains nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1814_1_parallel",
            "next_target": "1815b-Y5-R2FR-source-test-transfer-kernel-or-arena-current-residual-row.md",
            "script": "scripts/Y5_R2FR_source_test_transfer_kernel_or_arena_current_residual_row.py",
            "objective": "stage WEP/R10/source-test transfer kernels after current owner/no-rescale status is decided",
            "selection_status": "held_parallel",
            "success_condition": "transfer kernel theorem-zero, or arena current mismatch row is source-backed",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "connection_current_theorem": connection_current_theorem_rows(),
        "visible_connection_audit": visible_connection_rows(),
        "current_owner_audit": current_owner_rows(),
        "dva_dj_residual": residual_rows(),
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
    allowed_gate_pass = {"AC1814_0_theorem_contract"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1814_0_theorem_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1814_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1814_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1814_2_theorem_contract_written",
            any(row["theorem_id"] == "VCC1814_0_target" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["connection_current_theorem"]),
            "visible connection/current owner theorem is written as exact conditional",
        ),
        (
            "VAL1814_3_theorem_not_promoted",
            any(row["theorem_id"] == "VCC1814_4_verdict" and row["proof_status"] == "CONNECTION_CURRENT_OWNER_CONTRACT_NOT_CURRENT_PROOF" for row in rows_map["connection_current_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["connection_current_theorem"]),
            "connection/current theorem is not promoted as current proof",
        ),
        (
            "VAL1814_4_visible_connection_blocked",
            any(row["audit_id"] == "VGA1814_3_verdict" and row["current_status"] == "VISIBLE_CONNECTION_OWNER_NOT_DERIVED" for row in rows_map["visible_connection_audit"]),
            "visible connection owner remains blocked",
        ),
        (
            "VAL1814_5_current_owner_blocked",
            any(row["audit_id"] == "COA1814_4_verdict" and row["current_status"] == "CURRENT_OWNER_NOT_DERIVED" for row in rows_map["current_owner_audit"]),
            "same current owner remains blocked",
        ),
        (
            "VAL1814_6_residual_schema_nonclaim",
            any(row["residual_id"] == "DJ1814_4_total" for row in rows_map["dva_dj_residual"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["dva_dj_residual"]),
            "D_v A_Q/D_v J_Q residual rows are schema-only and nonclaim",
        ),
        (
            "VAL1814_7_countermodels_retained",
            all(boolish(row["retained"]) and not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "connection/current countermodels remain retained",
        ),
        (
            "VAL1814_8_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1814_9_acceptance_blocks",
            any(row["gate_id"] == "AC1814_0_theorem_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1814_10_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all connection/current/local claim gates remain blocked or refused",
        ),
        ("VAL1814_11_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1814_12_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1814_13_decision_next",
            any(row["decision_id"] == "DEC1814_3_best_next" and row["decision"] == "NOETHER_CURRENT_OWNER_NO_RESCALE_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects Noether current owner/no-rescale next",
        ),
        (
            "VAL1814_14_next_selected",
            any(row["route_id"] == "NEXT1814_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1814_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1814 CSVs parse"),
        ("VAL1814_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1814_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1814_18_formalization_untouched", formalization_untouched(), "no 1814 outputs found under formalization-workbench"),
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
            "check_id": "VAL1814_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1814 visible gauge connection current owner or DvA DJ alpha residual row checkpoint",
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
            "# 1814 Y5 R2FR visible gauge connection current owner or DvA DJ alpha residual row",
            "",
            "**Progress:** 1814 writes the exact same-current theorem. If `A_Q^vis` is a parent connection and `J_Q` is the Noether current from the same parent matter variation, source/test charge normalization cannot be inserted as a free coupling without becoming an explicit residual.",
            "",
            "**Current verdict:** exact conditional theorem, not current proof. Maxwell-form support exists, but `A_Q^vis` projection is still template-only, the Noether/current owner is missing, and `J_A -> c_A J_A` plus source/readout transfer countermodels survive.",
            "",
            "**Claim ceiling:** no visible gauge connection owner claim, no same-current owner claim, no current-rescaling zero claim, no alpha WEP/R10/clock pass, no PPN/local-GR/Newton pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1814.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Visible Connection Current Owner Theorem",
            markdown_table(rows_map["connection_current_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Visible Connection Owner Audit",
            markdown_table(rows_map["visible_connection_audit"], ["audit_id", "object", "current_status", "source_anchor", "would_close", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Current Owner Audit",
            markdown_table(rows_map["current_owner_audit"], ["audit_id", "object", "current_status", "source_anchor", "would_close", "missing_for_claim", "valid_for_claim"]),
            "",
            "## DvA DJ Alpha Residual Row Schema",
            markdown_table(rows_map["dva_dj_residual"], ["residual_id", "quantity", "definition", "formal_expression", "zero_condition", "current_status", "units", "common_normalizer", "score_ready", "valid_for_claim"]),
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
            "This is exactly where the coupling either becomes physics or stays bookkeeping. We now have the theorem form: one parent connection, one parent current, no current-label morphism. The corpus does not yet prove it, so the next clean attack is the no-rescale lemma for `J_A -> c_A J_A` from parent matter-action naturality.",
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
    print(f"1814 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
