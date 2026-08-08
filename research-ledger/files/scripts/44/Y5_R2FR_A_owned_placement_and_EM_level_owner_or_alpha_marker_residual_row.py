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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1813"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1813-Y5-R2FR-A-owned-placement-and-EM-level-owner-or-alpha-marker-residual-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1813_0_1812_doc",
        "source_key": "1812_handoff_doc",
        "source_path": ROOT / "1812-Y5-R2FR-parent-field-chart-Qvis-and-alpha-level-owner-or-first-residual-row.md",
        "needles": ["DEC1812_3_best_next", "NEXT1812_0_primary"],
        "role": "1812 selects A_owned placement and EM level owner as the next target.",
    },
    {
        "source_id": "SRC1813_1_1812_validation",
        "source_key": "1812_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1812_VALIDATION.csv",
        "needles": ["VAL1812_OVERALL", "PASS"],
        "role": "confirms 1812 owner package checkpoint passed as nonclaim.",
    },
    {
        "source_id": "SRC1813_2_1812_field_chart",
        "source_key": "1812_field_chart_qvis_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_FIELD_CHART_QVIS_OWNER_AUDIT.csv",
        "needles": ["FCQ1812_1_A_owned_placement", "BLOCKING_MISMATCH"],
        "role": "latest A_owned placement mismatch.",
    },
    {
        "source_id": "SRC1813_3_1812_alpha_level",
        "source_key": "1812_alpha_level_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_ALPHA_LEVEL_OWNER_AUDIT.csv",
        "needles": ["ALO1812_5_verdict", "ALPHA_LEVEL_OWNER_NOT_DERIVED"],
        "role": "latest alpha-level owner blocker.",
    },
    {
        "source_id": "SRC1813_4_1812_residual",
        "source_key": "1812_first_residual_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_DQ_DOBS_ALPHA_FIRST_RESIDUAL_ROW_SCHEMA.csv",
        "needles": ["DQA1812_3_A_owned_alpha_level", "MISSING_A_OWNED_PLACEMENT_AND_ALPHA_LEVEL_OWNER"],
        "role": "first A_owned/alpha-level residual schema row.",
    },
    {
        "source_id": "SRC1813_5_1812_hom_gate",
        "source_key": "1812_coefficient_domain_hom_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1812_COEFFICIENT_DOMAIN_HOM_GATE.csv",
        "needles": ["CDG1812_4_verdict", "COEFFICIENT_DOMAIN_HOM_GATE_BLOCKED"],
        "role": "coefficient-domain gate that blocks alpha-level promotion.",
    },
    {
        "source_id": "SRC1813_6_1782_field_chart",
        "source_key": "1782_field_chart_owner_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_FIELD_CHART_OWNER_GATE.csv",
        "needles": ["FCO1782_1_chart_version_consistency", "CHART_VERSION_MISMATCH_A_OWNED_UNSIGNED"],
        "role": "original chart version mismatch for A_owned.",
    },
    {
        "source_id": "SRC1813_7_1782_qvis",
        "source_key": "1782_qvis_column_owner_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1782_QVIS_COLUMN_OWNER_MATRIX.csv",
        "needles": ["QCO1782_4_A_owned", "not_decided_in_1667"],
        "role": "Q_vis column matrix where A_owned is undecided.",
    },
    {
        "source_id": "SRC1813_8_1674_ansatz",
        "source_key": "1674_parent_q_z_ansatz",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1674_PARENT_Q_Z_MINIMAL_ANSATZ.csv",
        "needles": ["QANS1674_1_visible_quotient", "A_owned"],
        "role": "minimal ansatz putting A_owned in Q_vis as owned gauge constants.",
    },
    {
        "source_id": "SRC1813_9_781_parent_action",
        "source_key": "781_minimal_parent_coupling_action",
        "source_path": RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
        "needles": ["MPC781_0_parent_variables", "A_owned"],
        "role": "minimal parent coupling action contract with owned gauge fields.",
    },
    {
        "source_id": "SRC1813_10_781_geometry_stack",
        "source_key": "781_geometry_stack",
        "source_path": RESIDUALS / "P8_Y5_R10_781_MINIMAL_PARENT_COUPLING_OWNER_ACTION.csv",
        "needles": ["MPC781_2_geometry_stack", "D_m=D[e_obs,A_owned]"],
        "role": "matter derivative/connection stack where A_owned enters ordinary matter.",
    },
    {
        "source_id": "SRC1813_11_783_field_map",
        "source_key": "783_field_map",
        "source_path": RESIDUALS / "P8_Y5_R10_783_COUPLING_OWNER_FIELD_MAP.csv",
        "needles": ["FM783_1_Q", "needed_but_not_owned"],
        "role": "Q/q field map remains needed but not owned.",
    },
    {
        "source_id": "SRC1813_12_765_maxwell_gate",
        "source_key": "765_maxwell_kinetic_inheritance_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv",
        "needles": ["MKI765_0_projection", "MKI765_5_total"],
        "role": "Maxwell inheritance gate for parent connection, norm, current and readout.",
    },
    {
        "source_id": "SRC1813_13_765_rescaling",
        "source_key": "765_rescaling_counterexamples",
        "source_path": RESIDUALS / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["RCE765_0_lambda_F2", "RCE765_1_generator_rescale"],
        "role": "rescaling and independent F2 counterexamples.",
    },
    {
        "source_id": "SRC1813_14_764_alpha_owner",
        "source_key": "764_alpha_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_764_ALPHA_EM_OWNER_AUDIT.csv",
        "needles": ["AEO764_2_parent_vertical_generator_norm", "best_route_not_proved"],
        "role": "best alpha-owner route remains unproved.",
    },
    {
        "source_id": "SRC1813_15_642_maxwell",
        "source_key": "642_maxwell_descent_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv",
        "needles": ["MD642_0_Bianchi", "MD642_4_alpha_constant"],
        "role": "Maxwell descent supports conditional form but not parent alpha ownership.",
    },
    {
        "source_id": "SRC1813_16_1056_vertical_norm",
        "source_key": "1056_vertical_generator_norm",
        "source_path": RESIDUALS / "P8_Y5_R10_1056_VERTICAL_GENERATOR_NORM_DERIVATION_AUDIT.csv",
        "needles": ["VNA1056_6_verdict", "ALPHA_OWNER_NOT_DERIVED_RETAIN_B_ALPHA"],
        "role": "vertical generator norm theorem remains conditional.",
    },
    {
        "source_id": "SRC1813_17_1235_unique_f2",
        "source_key": "1235_unique_F2",
        "source_path": RESIDUALS / "P8_Y5_R10_1235_UNIQUE_F2_TYPED_COEFFICIENT_DOMAIN_PROOF_ATTEMPT.csv",
        "needles": ["UF21235_7_verdict", "UNIQUE_F2_NOT_CLOSED"],
        "role": "unique F_Q^2 theorem is not closed.",
    },
    {
        "source_id": "SRC1813_18_1480_hom",
        "source_key": "1480_hom_exclusion",
        "source_path": RESIDUALS / "P8_Y5_R10_1480_COEFFICIENT_DOMAIN_HOM_EXCLUSION_ATTEMPT.csv",
        "needles": ["CDH1480_5_verdict", "PROOF_NOT_CLOSED"],
        "role": "coefficient-domain Hom exclusion remains conditional.",
    },
    {
        "source_id": "SRC1813_19_1414_current_owner",
        "source_key": "1414_beta_source_alpha_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_OWNER_ATTEMPT.csv",
        "needles": ["BSA1414_5_verdict", "OWNER_NOT_DERIVED"],
        "role": "source/current normalization owner remains missing.",
    },
]


OUTPUTS: dict[str, Path] = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_SOURCE_REGISTER.csv",
    "a_owned_split_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_A_OWNED_SPLIT_THEOREM.csv",
    "placement_candidate_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_A_OWNED_PLACEMENT_CANDIDATE_AUDIT.csv",
    "em_level_owner_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_EM_LEVEL_OWNER_CONTRACT.csv",
    "alpha_marker_residual": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_ALPHA_MARKER_RESIDUAL_ROW_SCHEMA.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_COUNTERMODEL_LEDGER.csv",
    "gr_newton_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_GR_NEWTON_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1813_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1813_VALIDATION.csv",
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


def a_owned_split_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "AST1813_0_problem",
            "claim": "A_owned cannot do connection and alpha-level jobs as one untyped symbol",
            "mathematical_statement": "If A_owned is simultaneously a Q_vis connection column, a fixed representation/level datum, and a kinetic coefficient owner, then D_v A_owned and D_v alpha_EM are underdetermined and the chart/Qvis theorem cannot decide which derivative is supposed to vanish.",
            "proof_status": "DIAGNOSTIC_EXACT",
            "current_corpus_status": "OVERLOADED_SYMBOL_CAUSES_BLOCKING_MISMATCH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "AST1813_1_split_contract",
            "claim": "split A_owned into visible connection and EM level/norm owners",
            "mathematical_statement": "Replace the overloaded slot by A_owned_split=(A_Q^vis,ell_EM). A_Q^vis is the parent-owned visible U(1) connection entering D_m and readout; ell_EM or g_* is fixed representation/fibre-metric/level data that owns g_EM^{-2} only if unique-F2 and current/readout clauses also close.",
            "proof_status": "CANONICAL_PLACEMENT_CONTRACT",
            "current_corpus_status": "CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "AST1813_2_qvis_rule",
            "claim": "Q_vis may contain the induced connection, not the alpha coefficient",
            "mathematical_statement": "Q_vis can include A_Q^vis as connection/readout data for ordinary matter, while ell_EM/g_* must not be treated as a fitted Q_vis column unless it is quotient-fixed or residualized.",
            "proof_status": "NECESSARY_TYPING_RULE",
            "current_corpus_status": "QVIS_RULE_NOT_ACTION_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "AST1813_3_zero_condition",
            "claim": "alpha-marker leakage vanishes only under a two-zero condition",
            "mathematical_statement": "The local alpha marker is zero only if D_v A_Q^vis=0 for ordinary vertical representatives and D_v ell_EM=0 with no lambda_A F_Q^2, f(I_hid)F_Q^2, current-rescaling, or readout leakage.",
            "proof_status": "EXACT_CONDITIONAL_ZERO_CONDITION",
            "current_corpus_status": "ANTECEDENTS_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "AST1813_4_verdict",
            "claim": "1813 closes A_owned placement and alpha level in the current corpus",
            "mathematical_statement": "AST1813_1 through AST1813_3 are parent-signed and all counterterms/readout leaks are forbidden",
            "proof_status": "PLACEMENT_CONTRACT_ONLY_NOT_CURRENT_PROOF",
            "current_corpus_status": "DEMOTE_TO_ALPHA_MARKER_RESIDUAL_ROWS",
            "valid_for_claim": False,
        },
    ]


def placement_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "placement_id": "APO1813_0_parent_connection",
            "candidate": "A_Q^vis as parent-owned visible connection",
            "role": "enters D_m=D[e_obs,A_Q^vis] and Lorentz/readout coupling",
            "status": "BEST_CANONICAL_CONNECTION_SLOT_CONTRACT_NOT_SIGNED",
            "why": "it matches 781 geometry stack and keeps ordinary matter coupling inside one parent action",
            "risk": "does not by itself fix g_EM^{-2}, alpha_EM, or current normalization",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "placement_id": "APO1813_1_qvis_column",
            "candidate": "induced A_Q^vis data as Q_vis column",
            "role": "observable connection/readout data, not an independent alpha coefficient",
            "status": "ALLOWED_ONLY_AS_INDUCED_CONNECTION_DATA",
            "why": "Q_vis needs the connection seen by charged matter, but not a free coefficient slot",
            "risk": "if Q_vis also carries ell_EM as a free column, alpha drift is smuggled back in",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "placement_id": "APO1813_2_fixed_level",
            "candidate": "ell_EM or g_* as fixed representation/fibre-metric level",
            "role": "owns Maxwell kinetic normalization only if inherited by unique parent subblock",
            "status": "PROMISING_LEVEL_SLOT_NOT_DERIVED",
            "why": "this is the least arbitrary way to make alpha structural rather than fitted",
            "risk": "lambda_A F_Q^2, generator rescaling, current rescaling and readout leakage remain legal",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "placement_id": "APO1813_3_pure_qvis_alpha",
            "candidate": "alpha_EM or g_EM as ordinary Q_vis scalar column",
            "role": "would make measured alpha an observed quotient variable",
            "status": "REJECT_AS_ZERO_THEOREM_ROUTE",
            "why": "putting alpha into Q_vis as data does not derive its silence; it only records the measured value",
            "risk": "turns structural owner into post-fit constant and weakens GR/Newton reduction",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "placement_id": "APO1813_4_mixed_A_owned",
            "candidate": "one A_owned symbol for connection, representation level and kinetic coefficient",
            "role": "old ambiguous chart slot",
            "status": "REJECT_OVERLOADED_SYMBOL",
            "why": "the same symbol cannot be both a derivative column and the coefficient-domain owner without a split map",
            "risk": "reopens D_v A, D_v ell_EM and alpha-counterterm residuals",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "placement_id": "APO1813_5_residual_fallback",
            "candidate": "D_v A_Q^vis and D_v ell_EM finite rows",
            "role": "honest nonclaim branch if parent owner fails",
            "status": "FALLBACK_SCHEMA_REQUIRED",
            "why": "failed placement can still become a measured residual vector with units and no-cancellation guard",
            "risk": "no local-GR or alpha-zero claim until source-backed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "placement_id": "APO1813_6_verdict",
            "candidate": "canonical A_owned split",
            "role": "A_owned_split=(A_Q^vis,ell_EM/g_*)",
            "status": "SPLIT_CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            "why": "this resolves the chart mismatch at object-language level but is not yet an action derivation",
            "risk": "must next sign connection/current/unique-F2/readout clauses or fill residual rows",
            "valid_for_claim": False,
        },
    ]


def em_level_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ELO1813_0_visible_connection",
            "owner_piece": "A_Q^vis",
            "required_statement": "A_parent contains a visible U(1) subconnection A_Q^vis along a fixed generator T_Q before readout, and D_m uses this induced connection.",
            "current_status": "TEMPLATE_ONLY_NOT_PARENT_SIGNED",
            "source_anchor": "MKI765_0_projection; MPC781_2_geometry_stack",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ELO1813_1_generator_norm",
            "owner_piece": "T_Q norm N_Q",
            "required_statement": "The parent fibre metric/lattice/symplectic form fixes <T_Q,T_Q>_P=N_Q and forbids T_Q -> sT_Q rescaling.",
            "current_status": "NORM_NOT_SIGNED",
            "source_anchor": "MKI765_1_norm; RCE765_1_generator_rescale",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ELO1813_2_level_to_alpha",
            "owner_piece": "ell_EM/g_*",
            "required_statement": "alpha_EM=alpha_*(ell_EM,g_*,hbar,c,*_obs) and Lie_v ell_EM=Lie_v g_*=0 while observed readout factors through Q_vis.",
            "current_status": "ALPHA_LEVEL_MAP_NOT_DERIVED",
            "source_anchor": "AEO764_2_parent_vertical_generator_norm; MD642_4_alpha_constant",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ELO1813_3_unique_F2",
            "owner_piece": "Maxwell kinetic coefficient domain",
            "required_statement": "No independent lambda_A F_Q^2 or f(I_hid)F_Q^2 term exists beyond the inherited parent curvature norm.",
            "current_status": "UNIQUE_F2_HOM_NOT_CLOSED",
            "source_anchor": "MKI765_2_unique_F2; UF21235_7_verdict; CDH1480_5_verdict",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ELO1813_4_current_owner",
            "owner_piece": "same Noether current owner",
            "required_statement": "Matter current, charge labels, source/test normalization, and A_Q coupling descend from the same T_Q owner.",
            "current_status": "CURRENT_OWNER_NOT_DERIVED",
            "source_anchor": "MKI765_3_same_current; BSA1414_5_verdict",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ELO1813_5_readout_closure",
            "owner_piece": "observed alpha readout",
            "required_statement": "Hodge/coframe, clock/spectroscopy and radiative maps do not reintroduce vertical representative data into measured alpha.",
            "current_status": "READOUT_CLOSURE_UNSIGNED",
            "source_anchor": "MKI765_4_readout; RCE765_3_coframe_Hodge_leak",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "ELO1813_6_verdict",
            "owner_piece": "EM level owner",
            "required_statement": "ELO1813_0 through ELO1813_5 close in one parent branch.",
            "current_status": "EM_LEVEL_OWNER_NOT_CLOSED",
            "source_anchor": "MKI765_5_total; VNA1056_6_verdict",
            "valid_for_claim": False,
        },
    ]


def alpha_marker_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": "AMR1813_0_Dv_AQ",
            "quantity": "epsilon_Dv_AQ_abs",
            "definition": "absolute derivative of the visible parent connection along retained local vertical directions",
            "formal_expression": "||D_v A_Q^vis||",
            "zero_condition": "A_Q^vis descends through Q_vis and v in ker(Dq) for the connection column",
            "required_inputs": "direction_id; connection_component; D_v_AQ_or_zero_theorem; norm; units; source_path",
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
            "residual_id": "AMR1813_1_Dv_ell_EM",
            "quantity": "epsilon_Dv_ell_EM_abs",
            "definition": "absolute derivative of the EM level/fibre metric owner",
            "formal_expression": "|D_v ell_EM|+|D_v g_*|",
            "zero_condition": "ell_EM/g_* is fixed parent level or quotient-silent fibre metric data",
            "required_inputs": "level_owner; D_v_level_or_zero_theorem; level_norm; units; source_path",
            "current_status": "MISSING_DV_LEVEL_VALUE_OR_THEOREM_ZERO",
            "units": "fractional_level_norm",
            "source_path": "",
            "common_normalizer": "MISSING_LEVEL_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "AMR1813_2_alpha_counterterm",
            "quantity": "epsilon_lambda_F2_abs",
            "definition": "independent Maxwell kinetic or hidden scalar coefficient response",
            "formal_expression": "|lambda_A|+sup_local |D_hid f(I_hid)|",
            "zero_condition": "unique parent F_Q^2 typed-domain theorem and Hom exclusion",
            "required_inputs": "coefficient_domain_certificate_or_bound; hidden_scalar_status; units; source_path",
            "current_status": "MISSING_UNIQUE_F2_OR_COEFFICIENT_BOUND",
            "units": "fractional_alpha_response",
            "source_path": "",
            "common_normalizer": "MISSING_ALPHA_RESPONSE_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "AMR1813_3_current_rescale",
            "quantity": "epsilon_current_owner_abs",
            "definition": "source/test current normalization mismatch after A_Q and F_Q^2 are fixed",
            "formal_expression": "sup_A |D_v ln c_A| or |Delta c_A|",
            "zero_condition": "same Noether owner fixes kinetic coefficient, charges, current and source/test normalization",
            "required_inputs": "species_or_current_id; c_A_or_zero_theorem; units; source_path; WEP/R10 projection",
            "current_status": "MISSING_CURRENT_OWNER_OR_FINITE_C_A",
            "units": "dimensionless_current_fraction",
            "source_path": "",
            "common_normalizer": "MISSING_CURRENT_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "AMR1813_4_readout_alpha",
            "quantity": "epsilon_readout_alpha_abs",
            "definition": "clock/spectroscopy/Hodge/radiative reentry into measured alpha",
            "formal_expression": "|D_v ln(*_obs)|+|D_v ln(hbar c)|+|D_v ln Z_alpha^ren|",
            "zero_condition": "readout and radiative maps descend through Q_vis or are postprocessing with no vertical data",
            "required_inputs": "readout_channel; derivative_or_zero_theorem; units; source_path; arena",
            "current_status": "MISSING_READOUT_RADIATIVE_CLOSURE_OR_VALUE",
            "units": "fractional_readout_alpha_response",
            "source_path": "",
            "common_normalizer": "MISSING_READOUT_NORMALIZER",
            "no_cancellation_guard": "required",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "residual_id": "AMR1813_5_total",
            "quantity": "epsilon_A_owned_alpha_total_abs",
            "definition": "total no-cancellation envelope for A_owned split and EM level owner failure",
            "formal_expression": "abs(AMR1813_0)+abs(AMR1813_1)+abs(AMR1813_2)+abs(AMR1813_3)+abs(AMR1813_4)",
            "zero_condition": "all owner clauses theorem-zero or all finite components source-backed with common normalizer",
            "required_inputs": "all AMR1813 components; common normalizer; units; source paths; arena projection",
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
            "countermodel_id": "CM1813_0_overloaded_A_owned",
            "countermodel": "one symbol acts as connection, fixed level and kinetic coefficient",
            "why_it_defeats_claim": "the derivative that must vanish is undefined until the object language is split",
            "blocked_by": "A_owned_split=(A_Q^vis,ell_EM/g_*) with separate owner clauses",
            "retained": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1813_1_lambda_F2",
            "countermodel": "Delta S=-lambda_A/4 int F_Q^2",
            "why_it_defeats_claim": "alpha_EM can vary independently of a fixed connection/generator",
            "blocked_by": "unique parent curvature norm and typed coefficient-domain theorem",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1813_2_generator_rescale",
            "countermodel": "T_Q -> sT_Q, A_Q -> A_Q/s, n_A -> s n_A",
            "why_it_defeats_claim": "connection and charge normalization stay conventional unless the parent norm/lattice is fixed",
            "blocked_by": "nonrescalable parent generator norm",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1813_3_current_rescale",
            "countermodel": "J_A -> c_A J_A or source/test charge normalization split",
            "why_it_defeats_claim": "same Maxwell term can still produce species/source-dependent WEP/R10 response",
            "blocked_by": "same Noether current owner",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1813_4_readout_alpha",
            "countermodel": "measured alpha changes through Hodge/clock/spectroscopy/radiative readout",
            "why_it_defeats_claim": "fixed abstract EM level is not enough if observed alpha readout carries vertical data",
            "blocked_by": "readout/radiative closure or finite residual row",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def gr_newton_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1813_0_chart_repair",
            "if_closed": "A_owned split contract is parent-signed",
            "would_buy": "removes the internal chart mismatch between Q_vis connection data and alpha-level data",
            "still_missing": "q/Dq cells, Obs_e factorisation, boundary/tau support and matter functor signature",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1813_1_alpha_branch",
            "if_closed": "A_Q^vis, ell_EM, unique F2, current owner and readout closure close together",
            "would_buy": "alpha-marker WEP/R10/clock branches become theorem-zero instead of product-prior residuals",
            "still_missing": "unique F2/Hom, current owner and readout/radiative closure are not derived",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1813_2_local_GR",
            "if_closed": "alpha coupling route is structurally removed",
            "would_buy": "one dangerous non-GR source/test coupling channel disappears from the local residual vector",
            "still_missing": "not the full GR reduction: EH/Poisson/measured-G/PPN/source-boundary gates remain",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "GNI1813_3_verdict",
            "if_closed": "1813 package closes",
            "would_buy": "real progress toward derivable source universality, but no standalone local-GR pass",
            "still_missing": "1813 closes only a contract split, not the parent action proof",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1813_0_split_contract",
            "gate": "A_owned split contract written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "AST1813 separates A_Q^vis from ell_EM/g_* and rejects overloaded A_owned",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1813_1_parent_signature",
            "gate": "split is parent-action signed",
            "current_status": "BLOCKED",
            "reason": "APO1813_6 is a contract, not an action derivation",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1813_2_em_level",
            "gate": "EM level owner closes",
            "current_status": "BLOCKED",
            "reason": "ELO1813_6 remains EM_LEVEL_OWNER_NOT_CLOSED",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1813_3_residual_values",
            "gate": "alpha-marker residual rows source-backed",
            "current_status": "BLOCKED",
            "reason": "AMR1813 rows have missing component values, source paths and common normalizers",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1813_4_local_promotion",
            "gate": "WEP/R10/clock/PPN/local-GR promotion allowed",
            "current_status": "REFUSED",
            "reason": "split contract alone does not prove alpha zero or finite arena residuals",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1813_0_A_owned_resolved",
            "claim": "A_owned placement is fully derived",
            "status": "BLOCKED",
            "reason": "split contract is written but not parent-action signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1813_1_alpha_owner",
            "claim": "alpha_EM is fixed by parent EM level",
            "status": "BLOCKED",
            "reason": "EM level map, unique F2, current owner and readout closure remain unsigned",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1813_2_alpha_marker_zero",
            "claim": "alpha-marker WEP/R10/clock leakage is theorem-zero",
            "status": "BLOCKED",
            "reason": "AMR1813 rows are MISSING and not score-ready",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1813_3_local_GR",
            "claim": "local GR/Newton/PPN follows",
            "status": "REFUSED",
            "reason": "A_owned split is only one source-side subgate and not a full local-GR derivation",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1813_0_split_result",
            "decision": "A_OWNED_OVERLOAD_REPAIRED_AS_CONTRACT",
            "reason": "the safest object language is A_owned_split=(A_Q^vis,ell_EM/g_*), with Q_vis carrying the induced connection and alpha owned only by a separate fixed level/norm clause",
            "next_action": "use split contract going forward, but do not treat it as a proof",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1813_1_current_status",
            "decision": "EM_LEVEL_OWNER_NOT_CLOSED",
            "reason": "unique F2/Hom, generator norm, same-current owner and readout/radiative closure remain unsigned",
            "next_action": "retain alpha-marker residual rows and no local claim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1813_2_residual_status",
            "decision": "ALPHA_MARKER_RESIDUAL_SCHEMA_READY_NONCLAIM",
            "reason": "D_v A_Q, D_v ell_EM, lambda_F2, current rescale and readout alpha rows are explicit but unsourced",
            "next_action": "fill no row without source path, units, common normalizer and no-cancellation guard",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1813_3_best_next",
            "decision": "VISIBLE_GAUGE_CONNECTION_CURRENT_OWNER_NEXT",
            "reason": "after the split, the least diffuse proof route is to parent-sign A_Q^vis as a connection and the same Noether current owner before tackling every arena projection",
            "next_action": "1814-Y5-R2FR-visible-gauge-connection-current-owner-or-DvA-DJ-alpha-residual-row.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1813_0_primary",
            "next_target": "1814-Y5-R2FR-visible-gauge-connection-current-owner-or-DvA-DJ-alpha-residual-row.md",
            "script": "scripts/Y5_R2FR_visible_gauge_connection_current_owner_or_DvA_DJ_alpha_residual_row.py",
            "objective": "try to parent-sign A_Q^vis as the visible gauge connection and the same Noether current owner; if not, emit D_v A_Q and D_v J_Q residual rows",
            "selection_status": "selected",
            "success_condition": "A_Q^vis/current owner theorem-zero, or D_v A_Q/D_v J_Q rows are source-backed and remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1813_1_parallel",
            "next_target": "1814b-Y5-R2FR-unique-F2-Hom-exclusion-or-lambdaF2-bound-row.md",
            "script": "scripts/Y5_R2FR_unique_F2_Hom_exclusion_or_lambdaF2_bound_row.py",
            "objective": "attack the independent F_Q^2/Hom coefficient counterterm after the connection/current owner route is fixed or rejected",
            "selection_status": "held_parallel",
            "success_condition": "unique F2 theorem-zero, or lambda_F2/f(I_hid) residual bound row is source-backed",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "a_owned_split_theorem": a_owned_split_theorem_rows(),
        "placement_candidate_audit": placement_candidate_rows(),
        "em_level_owner_contract": em_level_owner_rows(),
        "alpha_marker_residual": alpha_marker_residual_rows(),
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
    allowed_gate_pass = {"AC1813_0_split_contract"}
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
                or (boolish(row.get("gate_pass", False)) and row.get("gate_id") != "AC1813_0_split_contract")
            ):
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    exists_ok = all(boolish(row["exists"]) for row in source_rows)
    needles_ok = all(boolish(row["needles_present"]) for row in source_rows)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1813_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1813_1_needles_present", needles_ok, "all cited source needles are present"),
        (
            "VAL1813_2_split_contract_written",
            any(row["theorem_id"] == "AST1813_1_split_contract" and row["proof_status"] == "CANONICAL_PLACEMENT_CONTRACT" for row in rows_map["a_owned_split_theorem"]),
            "A_owned split contract is written",
        ),
        (
            "VAL1813_3_overload_rejected",
            any(row["placement_id"] == "APO1813_4_mixed_A_owned" and row["status"] == "REJECT_OVERLOADED_SYMBOL" for row in rows_map["placement_candidate_audit"]),
            "overloaded A_owned route is rejected",
        ),
        (
            "VAL1813_4_not_promoted",
            any(row["theorem_id"] == "AST1813_4_verdict" and row["proof_status"] == "PLACEMENT_CONTRACT_ONLY_NOT_CURRENT_PROOF" for row in rows_map["a_owned_split_theorem"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["a_owned_split_theorem"]),
            "split contract is not promoted as current proof",
        ),
        (
            "VAL1813_5_em_level_blocked",
            any(row["contract_id"] == "ELO1813_6_verdict" and row["current_status"] == "EM_LEVEL_OWNER_NOT_CLOSED" for row in rows_map["em_level_owner_contract"]),
            "EM level owner remains blocked",
        ),
        (
            "VAL1813_6_residual_schema_nonclaim",
            any(row["residual_id"] == "AMR1813_5_total" for row in rows_map["alpha_marker_residual"])
            and all(not boolish(row["score_ready"]) and not boolish(row["valid_for_claim"]) for row in rows_map["alpha_marker_residual"]),
            "alpha marker residual rows are schema-only and nonclaim",
        ),
        (
            "VAL1813_7_countermodels_retained",
            any(row["countermodel_id"] == "CM1813_0_overloaded_A_owned" and not boolish(row["retained"]) for row in rows_map["countermodel_ledger"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["countermodel_ledger"]),
            "overload countermodel is repaired as contract while physical countermodels remain nonclaim",
        ),
        (
            "VAL1813_8_gr_newton_nonclaim",
            all(not boolish(row["claim_allowed_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["gr_newton_impact"]),
            "GR/Newton impact rows remain nonclaim",
        ),
        (
            "VAL1813_9_acceptance_blocks",
            any(row["gate_id"] == "AC1813_0_split_contract" and boolish(row["gate_pass"]) and not boolish(row["claim_allowed"]) for row in rows_map["acceptance_gate"])
            and all(not boolish(row["claim_allowed"]) and not boolish(row["valid_for_claim"]) for row in rows_map["acceptance_gate"]),
            "acceptance gate permits contract-only progress and blocks claims",
        ),
        (
            "VAL1813_10_claim_gates_blocked",
            all(row["status"] in {"BLOCKED", "REFUSED"} and not boolish(row["gate_pass"]) and not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "all placement/alpha/local claim gates remain blocked or refused",
        ),
        ("VAL1813_11_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1813_12_missing_not_ready", missing_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1813_13_decision_next",
            any(row["decision_id"] == "DEC1813_3_best_next" and row["decision"] == "VISIBLE_GAUGE_CONNECTION_CURRENT_OWNER_NEXT" for row in rows_map["decision_ledger"]),
            "decision selects visible gauge connection/current owner next",
        ),
        (
            "VAL1813_14_next_selected",
            any(row["route_id"] == "NEXT1813_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1813_15_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1813 CSVs parse"),
        ("VAL1813_16_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1813_17_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1813_18_formalization_untouched", formalization_untouched(), "no 1813 outputs found under formalization-workbench"),
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
            "check_id": "VAL1813_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1813 A_owned placement and EM level owner or alpha marker residual row checkpoint",
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
            "# 1813 Y5 R2FR A-owned placement and EM-level owner or alpha-marker residual row",
            "",
            "**Progress:** 1813 repairs the object-language mistake: `A_owned` should not be one overloaded symbol doing connection, level, kinetic-coefficient and current-normalization jobs. The clean contract is `A_owned_split=(A_Q^vis, ell_EM/g_*)`.",
            "",
            "**Current verdict:** contract-level progress, not a physics claim. `A_Q^vis` is the visible parent connection that may enter `Q_vis` and ordinary matter derivatives. `ell_EM/g_*` is the fixed level/fibre-metric owner that would fix `alpha_EM` only if unique `F_Q^2`, current-owner, and readout/radiative clauses also close. Those clauses are still unsigned.",
            "",
            "**Claim ceiling:** no derived `A_owned` placement claim, no `alpha_EM` owner claim, no `b_alpha=0`, no WEP/R10/clock/PPN/local-GR/Newton pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1813.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## A Owned Split Theorem",
            markdown_table(rows_map["a_owned_split_theorem"], ["theorem_id", "claim", "mathematical_statement", "proof_status", "current_corpus_status", "valid_for_claim"]),
            "",
            "## Placement Candidate Audit",
            markdown_table(rows_map["placement_candidate_audit"], ["placement_id", "candidate", "role", "status", "why", "risk", "valid_for_claim"]),
            "",
            "## EM Level Owner Contract",
            markdown_table(rows_map["em_level_owner_contract"], ["contract_id", "owner_piece", "required_statement", "current_status", "source_anchor", "valid_for_claim"]),
            "",
            "## Alpha Marker Residual Row Schema",
            markdown_table(rows_map["alpha_marker_residual"], ["residual_id", "quantity", "definition", "formal_expression", "zero_condition", "current_status", "units", "common_normalizer", "score_ready", "valid_for_claim"]),
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
            "This is a good turn of the screw. We did not prove alpha constancy, but we removed a foggy notation trap. The next clean derivation target is whether the visible gauge connection and the source/test current really share one parent Noether owner. If yes, the alpha branch gets much less arbitrary; if no, the residual vector gets a concrete `D_v A_Q` and `D_v J_Q` row.",
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
    print(f"1813 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
