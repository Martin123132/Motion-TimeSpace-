from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3037"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3037-Y5-R2FR-minimum-source-readout-lock-parent-clause-or-XiH-bound-inputs-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3037_00_3036_doc": ROOT / "3036-Y5-R2FR-source-readout-lock-or-XiH-finite-residual-under-AX1090.md",
    "SRC3037_01_3036_theorem": RESIDUALS / "P8_Y5_R2FR_3036_SOURCE_READOUT_LOCK_THEOREM_ATTEMPT.csv",
    "SRC3037_02_3036_lock": RESIDUALS / "P8_Y5_R2FR_3036_LOCK_CLAUSE_MATRIX.csv",
    "SRC3037_03_3036_residual": RESIDUALS / "P8_Y5_R2FR_3036_XIH_FINITE_RESIDUAL_ROWS.csv",
    "SRC3037_04_min_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
    "SRC3037_05_min_matter": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv",
    "SRC3037_06_min_matter_gate": RESIDUALS / "P8_Y5_MIN_PARENT_MATTER_2587_ADOPTION_GATE.csv",
    "SRC3037_07_parent_terms": RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "SRC3037_08_parent_decision": RESIDUALS / "P8_Y5_PARENT_ACTION_CONTRACT_DECISION.csv",
    "SRC3037_09_parent_derivation": RESIDUALS / "P8_Y5_PARENT_ACTION_DERIVATION_ATTEMPT.csv",
    "SRC3037_10_source_bridge": RESIDUALS / "P8_Y5_PARENT_ACTION_2464_SOURCE_BRIDGE_CONTRACT.csv",
    "SRC3037_11_no_prefactor": RESIDUALS / "P8_Y5_NO_SOURCE_PREFACTOR_2645_PARENT_ACTION_CLAUSE_ATTEMPT.csv",
    "SRC3037_12_matter_owner": RESIDUALS / "P8_Y5_R10_1487_ORDINARY_MATTER_SUBACTION_OWNER.csv",
    "SRC3037_13_current_chain": RESIDUALS / "P8_Y5_R10_1488_ORDINARY_MATTER_SUBACTION_CURRENT_CHAIN_ATTEMPT.csv",
    "SRC3037_14_JH_current": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv",
    "SRC3037_15_PG_bridge": RESIDUALS / "P8_Y5_R2FR_2921_POISSON_GAUSS_ORBITAL_BRIDGE_AUDIT.csv",
    "SRC3037_16_source_mass": RESIDUALS / "P8_Y5_R2FR_2921_PARENT_SOURCE_MASS_IDENTITY_AUDIT.csv",
    "SRC3037_17_flux": RESIDUALS / "P8_Y5_PIM_JH_FLUX_2584_EXACT_OBSTRUCTION_VECTOR.csv",
    "SRC3037_18_frame": RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
    "SRC3037_19_tau": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
    "SRC3037_20_readout_order": RESIDUALS / "P8_Y5_FIELD_QUOTIENT_2570_READOUT_ORDER_GATE.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3037_SOURCE_REGISTER.csv",
    "minimum_clause": RESIDUALS / "P8_Y5_R2FR_3037_MINIMUM_SOURCE_READOUT_LOCK_PARENT_CLAUSE.csv",
    "derivation_audit": RESIDUALS / "P8_Y5_R2FR_3037_MINIMUM_LOCK_DERIVATION_AUDIT.csv",
    "adoption_gate": RESIDUALS / "P8_Y5_R2FR_3037_MINIMUM_LOCK_ADOPTION_GATE.csv",
    "bound_schema": RESIDUALS / "P8_Y5_R2FR_3037_XIH_BOUND_INPUT_SCHEMA.csv",
    "delta_contract": RESIDUALS / "P8_Y5_R2FR_3037_DELTA_A_SOURCE_RESIDUAL_CONTRACT.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3037_MINIMUM_LOCK_COUNTERMODEL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3037_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3037_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3037_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3037_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3037_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "minimum_clause_copy": PARENT_ACTION / "minimum_source_readout_lock_parent_clause_3037_NOT_SIGNED.csv",
    "adoption_gate_copy": PARENT_ACTION / "minimum_source_readout_lock_adoption_gate_3037_NONCLAIM.csv",
    "bound_schema_copy": LOCAL_BOUNDS / "XiH_bound_input_schema_3037_NONCLAIM.csv",
    "delta_contract_copy": LOCAL_BOUNDS / "delta_A_source_residual_contract_3037_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3037_COMMON_SOURCE_FUNCTIONAL_OR_XIH_BOUND_RUNNER_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    table_lines = [header, divider]
    for output_row in output_rows:
        cells = [
            as_str(output_row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            for column in columns
        ]
        table_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(table_lines)


source_roles = {
    "SRC3037_00_3036_doc": "3036 handoff to minimum lock or XiH bound route",
    "SRC3037_01_3036_theorem": "conditional source-readout lock theorem",
    "SRC3037_02_3036_lock": "lock clause matrix",
    "SRC3037_03_3036_residual": "XiH finite residual vector",
    "SRC3037_04_min_blocks": "minimum local-GR action blocks",
    "SRC3037_05_min_matter": "minimal parent matter coupling action contract",
    "SRC3037_06_min_matter_gate": "minimal matter adoption gates",
    "SRC3037_07_parent_terms": "source owner parent action term contract",
    "SRC3037_08_parent_decision": "parent action contract decision",
    "SRC3037_09_parent_derivation": "formal parent action derivation attempt",
    "SRC3037_10_source_bridge": "source bridge contract",
    "SRC3037_11_no_prefactor": "no-source-prefactor parent clause attempt",
    "SRC3037_12_matter_owner": "ordinary matter subaction owner",
    "SRC3037_13_current_chain": "ordinary matter current-chain attempt",
    "SRC3037_14_JH_current": "J_H current definition theorem attempt",
    "SRC3037_15_PG_bridge": "Poisson/Gauss bridge",
    "SRC3037_16_source_mass": "parent source-mass identity audit",
    "SRC3037_17_flux": "Omega_GM measured-mass obstruction vector",
    "SRC3037_18_frame": "observed frame lock contract",
    "SRC3037_19_tau": "tau generator lock contract",
    "SRC3037_20_readout_order": "variation-before-readout gate",
}

source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": source_roles[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

minimum_clause_rows = [
    base(
        {
            "clause_id": "MSRL3037_0_total_clause",
            "clause_piece": "minimum source-readout lock parent clause",
            "formal_statement": "S_parent contains one variation-before-readout observed stack q->(e_obs,tau,N,W), one universal S_ord[Psi,e_obs,theta], one Hcore source vertex, one parent charge normalization, and one boundary/reference class",
            "would_buy": "Xi_H and C_WH become coefficients of the same source object before calibration",
            "current_status": "CANDIDATE_CLAUSE_WRITTEN_NOT_DERIVED",
            "missing_for_claim": "MISSING_PARENT_ACTION_ADOPTION; MISSING_UNIQUENESS; MISSING_FIELD_LIST; MISSING_FIRST_VARIATION",
            "source_path": str(SOURCE_PATHS["SRC3037_04_min_blocks"]),
        }
    ),
    base(
        {
            "clause_id": "MSRL3037_1_observed_stack",
            "clause_piece": "single observed stack",
            "formal_statement": "q(Phi) owns e_obs, tau_obs, psi_N=-log(N), W/c^2, rho_H support, and readout order",
            "would_buy": "blocks frame/lapse/tau rescaling routes",
            "current_status": "CONTRACT_ONLY",
            "missing_for_claim": "MISSING_Q_OBJECT; MISSING_OBS_E; MISSING_TAU_SELECTOR; MISSING_LAPSE_READOUT_SOURCE",
            "source_path": str(SOURCE_PATHS["SRC3037_05_min_matter"]),
        }
    ),
    base(
        {
            "clause_id": "MSRL3037_2_universal_matter",
            "clause_piece": "universal ordinary matter functor",
            "formal_statement": "S_ord=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A] and no source-only w_A/c_A/J_A prefactor exists",
            "would_buy": "J_H is the total observed Hilbert source current with no species/source reweighting",
            "current_status": "CONDITIONAL_CONTRACT_COUNTERMODEL_SURVIVES",
            "missing_for_claim": "MISSING_NO_SOURCE_PREF_ACTOR_GRAMMAR; MISSING_SINGLE_ACTION_MEASURE_OWNER",
            "source_path": str(SOURCE_PATHS["SRC3037_11_no_prefactor"]),
        }
    ),
    base(
        {
            "clause_id": "MSRL3037_3_common_source_functional",
            "clause_piece": "common source functional",
            "formal_statement": "the same parent source functional M_src[J_H,tau,e_obs] appears in the psi_N source equation and the W/c^2 Poisson/Gauss source equation",
            "would_buy": "reduces Xi_H=C_WH to a single normalization theorem rather than two fitted constants",
            "current_status": "NOT_FOUND_AS_PARENT_DERIVED_OBJECT",
            "missing_for_claim": "MISSING_COMMON_SOURCE_FUNCTIONAL; MISSING_HCORE_SOURCE_VERTEX_OWNER; MISSING_POISSON_COEFFICIENT_OWNER",
            "source_path": str(SOURCE_PATHS["SRC3037_10_source_bridge"]),
        }
    ),
    base(
        {
            "clause_id": "MSRL3037_4_charge_denominator",
            "clause_piece": "M_H_ref/G_ref denominator lock",
            "formal_statement": "M_H_ref=H_tau[S_outer]-H_ref and G_ref are parent charge/readout data fixed before orbital GM or comparator GR is used",
            "would_buy": "prevents measured-GM absorption and makes C_WH source-normalized",
            "current_status": "MISSING_DENOMINATOR_OWNER",
            "missing_for_claim": "MISSING_H_TAU; MISSING_H_REF; MISSING_G_REF_OWNER; MISSING_INTEGRABILITY; MISSING_POSITIVITY",
            "source_path": str(SOURCE_PATHS["SRC3037_16_source_mass"]),
        }
    ),
    base(
        {
            "clause_id": "MSRL3037_5_flux_silence",
            "clause_piece": "Omega_GM and boundary/projector silence",
            "formal_statement": "Omega_GM=-Pi_M dJ_extra+[d,Pi_M]J_H+A_parent+tails is zero by parent theorem or finite below arena bounds",
            "would_buy": "prevents same-current theorem from conserving the wrong mass",
            "current_status": "RETAINED_OBSTRUCTION",
            "missing_for_claim": "MISSING_OMEGA_GM_ZERO_OR_BOUND; MISSING_PROJECTOR_CHAINMAP; MISSING_WORLDTUBE_GLUE",
            "source_path": str(SOURCE_PATHS["SRC3037_17_flux"]),
        }
    ),
    base(
        {
            "clause_id": "MSRL3037_6_verdict",
            "clause_piece": "minimum clause current corpus verdict",
            "formal_statement": "MSRL3037_0 through MSRL3037_5 are all derived from MTS core variables in one parent branch",
            "would_buy": "promote the first-order source normalization route to a real theorem candidate",
            "current_status": "MINIMUM_LOCK_CLAUSE_NOT_DERIVED",
            "missing_for_claim": "CLAUSE_IS_CONTRACT_NOT_PARENT_THEOREM",
            "source_path": str(SOURCE_PATHS["SRC3037_09_parent_derivation"]),
        }
    ),
]

derivation_rows = [
    base(
        {
            "audit_id": "DER3037_0_min_blocks",
            "candidate_source": "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS",
            "what_it_gives": "EH core, universal matter, extra-field silence, boundary/reference, metric readout blocks",
            "why_insufficient": "block list is a minimum contract; it does not derive the common Hcore/W source functional or M_H_ref/G_ref values",
            "current_status": "USEFUL_CONTRACT_NOT_PROOF",
            "source_path": str(SOURCE_PATHS["SRC3037_04_min_blocks"]),
        }
    ),
    base(
        {
            "audit_id": "DER3037_1_min_matter",
            "candidate_source": "2587 minimal parent matter action",
            "what_it_gives": "single observed matter stack and variation-before-readout workflow",
            "why_insufficient": "adoption gate says q/e_obs/tau/ell_J and no-source-slot proof are missing",
            "current_status": "CONTRACT_NOT_ADOPTED",
            "source_path": str(SOURCE_PATHS["SRC3037_06_min_matter_gate"]),
        }
    ),
    base(
        {
            "audit_id": "DER3037_2_no_prefactor",
            "candidate_source": "2645 no-source-prefactor clause",
            "what_it_gives": "exact target for forbidding w_A/c_A/source-only prefactors",
            "why_insufficient": "countermodel survives until parent grammar makes w_A untypeable",
            "current_status": "THEOREM_NOT_DERIVED",
            "source_path": str(SOURCE_PATHS["SRC3037_11_no_prefactor"]),
        }
    ),
    base(
        {
            "audit_id": "DER3037_3_parent_action",
            "candidate_source": "537 parent action derivation attempt",
            "what_it_gives": "formal Noether/current/charge derivation if an explicit action is supplied",
            "why_insufficient": "full parent Lagrangian, Q_tau/C_tau split and PiM/Hilbert identification are not supplied",
            "current_status": "FORMAL_IF_ACTION_SUPPLIED",
            "source_path": str(SOURCE_PATHS["SRC3037_09_parent_derivation"]),
        }
    ),
    base(
        {
            "audit_id": "DER3037_4_source_bridge",
            "candidate_source": "2464 source bridge contract",
            "what_it_gives": "lists current origin, worldtube integral, conservation, exterior vacuum and universality clauses",
            "why_insufficient": "each bridge clause is marked missing",
            "current_status": "SOURCE_BRIDGE_MISSING",
            "source_path": str(SOURCE_PATHS["SRC3037_10_source_bridge"]),
        }
    ),
    base(
        {
            "audit_id": "DER3037_5_current_chain",
            "candidate_source": "1488 ordinary matter current-chain attempt",
            "what_it_gives": "exact current-chain target and source-prefactor countermodel",
            "why_insufficient": "ordinary matter action owner still allows pre-action relative weights without grammar proof",
            "current_status": "COUNTERMODEL_SURVIVES",
            "source_path": str(SOURCE_PATHS["SRC3037_13_current_chain"]),
        }
    ),
    base(
        {
            "audit_id": "DER3037_6_derivation_verdict",
            "candidate_source": "3037 synthesis",
            "what_it_gives": "the minimum parent lock clause is now explicit",
            "why_insufficient": "current corpus does not derive it from core MTS variables; adopting it would be a closure axiom",
            "current_status": "FAIL_CURRENT_CLAIM_MOVE_TO_COMMON_SOURCE_FUNCTIONAL_OR_BOUNDS",
            "source_path": str(SOURCE_PATHS["SRC3037_00_3036_doc"]),
        }
    ),
]

adoption_gate_rows = [
    base(
        {
            "gate_id": "ADOPT3037_0_single_parent_action",
            "required_evidence": "one explicit S_parent with field list, source/readout stack, first variation and boundary class",
            "current_status": "MISSING",
            "blocks": "turning MSRL3037 from contract to theorem",
        }
    ),
    base(
        {
            "gate_id": "ADOPT3037_1_common_source_functional",
            "required_evidence": "same source functional M_src feeds Hcore psi_N and W/c^2 equations with fixed coefficient map",
            "current_status": "MISSING",
            "blocks": "Xi_H=C_WH derivation",
        }
    ),
    base(
        {
            "gate_id": "ADOPT3037_2_readout_normal_form",
            "required_evidence": "psi_N=-log(N), W/c^2, e_obs and tau_obs are fixed before source calibration",
            "current_status": "CONTRACT_ONLY",
            "blocks": "field-rescaling and time-normalization shortcuts",
        }
    ),
    base(
        {
            "gate_id": "ADOPT3037_3_no_source_slot",
            "required_evidence": "parent grammar forbids source-only weights, species labels, source masks and shadow frames",
            "current_status": "COUNTERMODEL_SURVIVES",
            "blocks": "universal JHrho",
        }
    ),
    base(
        {
            "gate_id": "ADOPT3037_4_charge_denominator",
            "required_evidence": "H_tau, H_ref, Q_tau, M_H_ref, G_ref, integrability and positivity sourced before orbital readout",
            "current_status": "MISSING",
            "blocks": "C_WH and measured-GM normalization",
        }
    ),
    base(
        {
            "gate_id": "ADOPT3037_5_flux_silence",
            "required_evidence": "Omega_GM zero theorem or finite source-backed obstruction vector",
            "current_status": "MISSING_ZERO_OR_BOUND",
            "blocks": "wrong-mass conservation countermodel",
        }
    ),
]

bound_schema_rows = [
    base(
        {
            "bound_id": "BND3037_0_XiH",
            "quantity": "Xi_H",
            "definition": "-JHrho/(C_N K0)",
            "required_fields": "system_id;source_body;C_H0;JHrho;rho_H_units;sign;source_path;source_anchor;derivation_or_measurement_method",
            "current_value": "MISSING_RATIO_VALUE",
            "acceptance_rule": "finite, sourced, same branch, same norm/units as C_WH; no field-rescaling convention",
            "status": "SOURCE_BACKED_INPUT_REQUIRED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_id": "BND3037_1_C_WH",
            "quantity": "C_WH",
            "definition": "4*pi*G_ref/c^2 on the local W/c^2 branch",
            "required_fields": "G_ref;M_H_ref;Poisson/Gauss source path;no_EH_import_certificate;units;source_anchor",
            "current_value": "CONDITIONAL_COMPARATOR_VALUE_ONLY",
            "acceptance_rule": "parent-owned G_ref or explicitly nonclaim comparator value",
            "status": "PARENT_OWNER_REQUIRED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_id": "BND3037_2_delta_XiH",
            "quantity": "delta_XiH",
            "definition": "Xi_H/C_WH - 1",
            "required_fields": "Xi_H;C_WH;uncertainty_or_bound;no_cancellation_policy;arena_projection",
            "current_value": "MISSING_DELTA_VALUE",
            "acceptance_rule": "can score only after Xi_H and C_WH rows pass",
            "status": "DERIVED_INPUT_REQUIRED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_id": "BND3037_3_Omega_GM",
            "quantity": "Omega_GM",
            "definition": "-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent + tails",
            "required_fields": "R_eq;I_commutator;B_zero_flux;A_parent;M_H_ref;surface_pair;units;source_path",
            "current_value": "MISSING_ZERO_OR_BOUND",
            "acceptance_rule": "zero theorem or finite obstruction below arena-specific bound",
            "status": "OBSTRUCTION_INPUT_REQUIRED_NONCLAIM",
        }
    ),
    base(
        {
            "bound_id": "BND3037_4_R_lock_components",
            "quantity": "R_lock_vector",
            "definition": "R_frame,R_tau,R_prefactor,R_worldtube,Omega_GM/M_H_ref",
            "required_fields": "component values or theorem-zero rows in one norm convention",
            "current_value": "MISSING_COMPONENT_VALUES",
            "acceptance_rule": "total envelope uses absolute values; no tuned cancellation",
            "status": "VECTOR_INPUT_REQUIRED_NONCLAIM",
        }
    ),
]

delta_contract_rows = [
    base(
        {
            "contract_id": "DAS3037_0_formula",
            "quantity": "delta_A_source",
            "formula": "delta_A_source = Xi_H/C_WH - 1 + R_lock",
            "claim_status": "FORMULA_ONLY_NONCLAIM",
            "needed_to_promote": "minimum parent lock theorem or finite bound rows for all terms",
        }
    ),
    base(
        {
            "contract_id": "DAS3037_1_total_abs",
            "quantity": "delta_A_source_total_abs",
            "formula": "abs(delta_XiH)+abs(R_frame)+abs(R_tau)+abs(R_prefactor)+abs(R_worldtube)+abs(Omega_GM/M_H_ref)",
            "claim_status": "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED",
            "needed_to_promote": "component values with units and common normalization",
        }
    ),
    base(
        {
            "contract_id": "DAS3037_2_acceptance",
            "quantity": "local_GR_first_order_gate",
            "formula": "pass iff delta_A_source_total_abs is theorem-zero or below declared arena threshold",
            "claim_status": "BLOCKED",
            "needed_to_promote": "thresholds, source-backed component rows and PPN followthrough",
        }
    ),
]

countermodel_rows = [
    base(
        {
            "countermodel_id": "CM3037_0_contract_axiom",
            "countermodel": "adopt MSRL as a closure axiom rather than deriving it from MTS variables",
            "effect": "can force-looking local GR without explaining why the source/readout lock exists",
            "status": "REJECTED_AS_DERIVATION",
        }
    ),
    base(
        {
            "countermodel_id": "CM3037_1_common_matter_not_Hcore",
            "countermodel": "universal S_ord fixes J_H but Hcore source vertex keeps an independent C_H0/JHrho ratio",
            "effect": "WEP-like matter success does not imply Xi_H=C_WH",
            "status": "LIVE",
        }
    ),
    base(
        {
            "countermodel_id": "CM3037_2_closed_wrong_charge",
            "countermodel": "Pi_M J_H is conserved but not the same worldtube mass or boundary charge used by W/c^2",
            "effect": "Omega_GM or R_worldtube shifts measured GM",
            "status": "LIVE",
        }
    ),
    base(
        {
            "countermodel_id": "CM3037_3_readout_reentry",
            "countermodel": "post-variation readout map, source support, or G_ref calibration re-enters after the parent variation",
            "effect": "local match becomes fitted calibration rather than derivation",
            "status": "LIVE",
        }
    ),
]

gates = [
    base(
        {
            "gate_id": "GATE3037_0_sources",
            "gate": "all cited local source paths exist",
            "result": all(path.exists() for path in SOURCE_PATHS.values()),
            "notes": "minimum clause audit is source-backed to existing corpus",
        }
    ),
    base(
        {
            "gate_id": "GATE3037_1_minimum_clause_written",
            "gate": "minimum source-readout parent clause is explicit",
            "result": any(row["clause_id"] == "MSRL3037_0_total_clause" for row in minimum_clause_rows),
            "notes": "contract only",
        }
    ),
    base(
        {
            "gate_id": "GATE3037_2_clause_derived",
            "gate": "minimum clause is derived from MTS core variables",
            "result": False,
            "notes": "current evidence is contract/adoption-gate level, not theorem",
        }
    ),
    base(
        {
            "gate_id": "GATE3037_3_bound_inputs_staged",
            "gate": "XiH, C_WH, delta_XiH, Omega_GM and R_lock bound schemas exist",
            "result": all(
                any(row["quantity"] == quantity for row in bound_schema_rows)
                for quantity in ["Xi_H", "C_WH", "delta_XiH", "Omega_GM", "R_lock_vector"]
            ),
            "notes": "all remain nonclaim with missing values",
        }
    ),
    base(
        {
            "gate_id": "GATE3037_4_countermodels_retained",
            "gate": "live countermodels are retained",
            "result": any(row["status"] == "LIVE" for row in countermodel_rows),
            "notes": "prevents axiom-smuggling",
        }
    ),
    base(
        {
            "gate_id": "GATE3037_5_no_claim_rows",
            "gate": "all generated rows remain nonclaim",
            "result": True,
            "notes": "no local-GR/Newton/PPN claim",
        }
    ),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3037_0_derivation",
            "question": "does the current corpus derive the minimum source-readout lock clause?",
            "answer": "NO",
            "reason": "the clause can be written cleanly from existing contracts, but no source derives it as the unique parent action/functor from MTS core variables",
            "next_action": "attack the common source functional directly or switch to strict XiH/delta_XiH/Omega_GM bound inputs",
        }
    ),
    base(
        {
            "decision_id": "DEC3037_1_best_route",
            "question": "what is the next non-circular route?",
            "answer": "derive common source functional normal form",
            "reason": "this is the only subclause that directly identifies the Hcore source coefficient with the W/c^2 Poisson coefficient",
            "next_action": "3038 should try the common source functional; if it fails, build the bound runner",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3037_0_3038",
            "next_checkpoint": "3038-Y5-R2FR-common-source-functional-normal-form-or-XiH-bound-runner-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_common_source_functional_normal_form_or_XiH_bound_runner_under_AX1090_3038.py",
            "mission": "derive a parent common source functional whose variation fixes both Xi_H and C_WH, or implement a strict nonclaim XiH/delta_XiH/Omega_GM bound-input runner",
            "starting_equation": "delta_A_source = Xi_H/C_WH - 1 + R_lock",
            "do_not_repeat": "do not re-audit K0, Ward-only conservation, or coframe-only descent as sufficient",
            "claim_policy": "no Newton/local-GR/PPN claim until common source functional or finite residual vector passes",
        }
    )
]

for output_key, output_rows in {
    "sources": source_register,
    "minimum_clause": minimum_clause_rows,
    "derivation_audit": derivation_rows,
    "adoption_gate": adoption_gate_rows,
    "bound_schema": bound_schema_rows,
    "delta_contract": delta_contract_rows,
    "countermodels": countermodel_rows,
    "gates": gates,
    "decision": decision_rows,
    "next": next_rows,
}.items():
    write_csv(OUTPUTS[output_key], output_rows)

shutil.copyfile(OUTPUTS["minimum_clause"], BRANCH_OUTPUTS["minimum_clause_copy"])
shutil.copyfile(OUTPUTS["adoption_gate"], BRANCH_OUTPUTS["adoption_gate_copy"])
shutil.copyfile(OUTPUTS["bound_schema"], BRANCH_OUTPUTS["bound_schema_copy"])
shutil.copyfile(OUTPUTS["delta_contract"], BRANCH_OUTPUTS["delta_contract_copy"])
shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"])

branch_rows = [
    base(
        {
            "branch_copy_id": output_key,
            "path": str(path),
            "exists": path.exists(),
            "role": "branch-scoped nonclaim copy for minimum-lock/XiH route",
            "status": "PRESENT_NONCLAIM_COPY" if path.exists() else "MISSING_BRANCH_COPY",
        }
    )
    for output_key, path in BRANCH_OUTPUTS.items()
]
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

csv_outputs = [path for output_key, path in OUTPUTS.items() if output_key != "validation"]
branch_outputs = list(BRANCH_OUTPUTS.values())
all_generated_paths = csv_outputs + branch_outputs + [DOC]
all_rows = (
    source_register
    + minimum_clause_rows
    + derivation_rows
    + adoption_gate_rows
    + bound_schema_rows
    + delta_contract_rows
    + countermodel_rows
    + gates
    + decision_rows
    + next_rows
    + branch_rows
)

validation_rows = [
    base(
        {
            "validation_id": "VAL3037_00_sources_exist",
            "passed": all(path.exists() for path in SOURCE_PATHS.values()),
            "requirement": "all cited source paths exist",
            "evidence": OUTPUTS["sources"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_01_csv_parse",
            "passed": all(csv_ok(path) for path in csv_outputs + branch_outputs),
            "requirement": "all generated CSV and branch-copy rows parse cleanly",
            "evidence": "csv.DictReader over generated outputs",
        }
    ),
    base(
        {
            "validation_id": "VAL3037_02_min_clause",
            "passed": any(row["clause_id"] == "MSRL3037_0_total_clause" for row in minimum_clause_rows),
            "requirement": "minimum source-readout lock parent clause is written",
            "evidence": OUTPUTS["minimum_clause"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_03_not_derived",
            "passed": any(row["current_status"] == "MINIMUM_LOCK_CLAUSE_NOT_DERIVED" for row in minimum_clause_rows),
            "requirement": "minimum clause is not claim-promoted",
            "evidence": OUTPUTS["minimum_clause"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_04_adoption_gates",
            "passed": all(row["current_status"] in {"MISSING", "CONTRACT_ONLY", "COUNTERMODEL_SURVIVES", "MISSING_ZERO_OR_BOUND"} for row in adoption_gate_rows),
            "requirement": "adoption gates remain blocked",
            "evidence": OUTPUTS["adoption_gate"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_05_bound_schema",
            "passed": bool(gates[3]["result"]),
            "requirement": "bound schemas cover XiH, C_WH, delta_XiH, Omega_GM and R_lock",
            "evidence": OUTPUTS["bound_schema"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_06_delta_contract",
            "passed": any(row["quantity"] == "delta_A_source" for row in delta_contract_rows),
            "requirement": "delta_A_source residual contract exists",
            "evidence": OUTPUTS["delta_contract"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_07_countermodels",
            "passed": any(row["status"] == "LIVE" for row in countermodel_rows),
            "requirement": "live countermodels are retained",
            "evidence": OUTPUTS["countermodels"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_08_no_claim_rows",
            "passed": all(not boolish(row.get("valid_for_claim")) and not boolish(row.get("claim_allowed")) for row in all_rows),
            "requirement": "no 3037 row is valid for claim",
            "evidence": "generated row flags",
        }
    ),
    base(
        {
            "validation_id": "VAL3037_09_branch_copies",
            "passed": all(path.exists() and csv_ok(path) for path in branch_outputs),
            "requirement": "branch copies exist and parse",
            "evidence": OUTPUTS["branches"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_10_output_scope",
            "passed": all(under(path, ROOT) for path in all_generated_paths),
            "requirement": "all generated outputs are inside post-checkpoint-work",
            "evidence": str(ROOT),
        }
    ),
    base(
        {
            "validation_id": "VAL3037_11_formalization_untouched",
            "passed": sum(1 for path in all_generated_paths if under(path, FORMALIZATION)) == 0,
            "requirement": "formalization-workbench modified-file target count remains 0",
            "evidence": "formalization_output_hits=0",
        }
    ),
    base(
        {
            "validation_id": "VAL3037_12_next_target",
            "passed": bool(next_rows) and next_rows[0]["next_checkpoint"].startswith("3038-"),
            "requirement": "next target selects common source functional or XiH bound runner",
            "evidence": OUTPUTS["next"].name,
        }
    ),
    base(
        {
            "validation_id": "VAL3037_13_pycache_removed",
            "passed": not PYCACHE.exists(),
            "requirement": "scripts __pycache__ removed",
            "evidence": str(PYCACHE),
        }
    ),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3037 - Minimum Source-Readout Lock Parent Clause Or XiH Bound Inputs under AX1090

Status: `Y5_R2FR_3037_minimum_lock_clause_written_not_derived_XiH_bound_schema_staged_3038_next`

## Verdict

3037 writes the smallest parent clause that would make the first-order local-GR source normalization non-circular:

`S_parent` must provide one variation-before-readout observed stack, one universal ordinary-matter current, one Hcore source vertex, one `W/c^2` source equation, one `tau/M_H_ref/G_ref` denominator, and one flux/boundary silence rule in the same branch.

If that clause were derived, `Xi_H=C_WH` would become a theorem candidate instead of a calibration choice. But the current corpus does **not** derive it. The inspected sources give contracts, blocks, adoption gates, and conditional lemmas; none supplies the one parent action/functor proof.

So 3037 does not claim local GR. It stages the strict fallback: source-backed `Xi_H`, `C_WH`, `delta_XiH`, `Omega_GM`, and `R_lock` input schemas, with the governing residual equation

`delta_A_source = Xi_H/C_WH - 1 + R_lock`.

## Minimum Parent Clause

{md_table(minimum_clause_rows, ["clause_id", "clause_piece", "formal_statement", "current_status", "missing_for_claim"])}

## Derivation Audit

{md_table(derivation_rows, ["audit_id", "candidate_source", "what_it_gives", "why_insufficient", "current_status"])}

## Adoption Gate

{md_table(adoption_gate_rows, ["gate_id", "required_evidence", "current_status", "blocks"])}

## XiH Bound Input Schema

{md_table(bound_schema_rows, ["bound_id", "quantity", "definition", "required_fields", "current_value", "status"])}

## Delta A Source Contract

{md_table(delta_contract_rows, ["contract_id", "quantity", "formula", "claim_status", "needed_to_promote"])}

## Countermodel Ledger

{md_table(countermodel_rows, ["countermodel_id", "countermodel", "effect", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "next_action"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "do_not_repeat", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc, encoding="utf-8")

print(f"Wrote {DOC}")
print(f"Wrote validation {OUTPUTS['validation']}")
print("3037 verdict: minimum source-readout lock clause written but not derived; XiH bound schemas staged.")
