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

CHECKPOINT = "3044"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3044-Y5-R2FR-AW-source-amplitude-theorem-or-DWPHI-bound-row-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3044_00_3043_doc": ROOT / "3043-Y5-R2FR-W-symbol-retirement-audit-or-DWPhi-first-bound-row-under-AX1090.md",
    "SRC3044_01_3043_bound": RESIDUALS / "P8_Y5_R2FR_3043_DWPHI_FIRST_BOUND_ROW_ATTEMPT.csv",
    "SRC3044_02_3043_decision": RESIDUALS / "P8_Y5_R2FR_3043_W_SYMBOL_RETIREMENT_DECISION.csv",
    "SRC3044_03_3043_next": RESIDUALS / "P8_Y5_R2FR_3043_NEXT_TARGET.csv",
    "SRC3044_04_gamma_kernel": RESIDUALS / "P8_Y5_R2FR_3016_GAMMA_KERNEL_DERIVATION.csv",
    "SRC3044_05_gamma_fill_contract": RESIDUALS / "P8_Y5_R2FR_3017_GAMMA_COEFFICIENT_FILL_CONTRACT.csv",
    "SRC3044_06_gamma_fill_attempt": RESIDUALS / "P8_Y5_R2FR_3018_GAMMA_COEFFICIENT_FILL_ATTEMPT.csv",
    "SRC3044_07_beta_square_law": RESIDUALS / "P8_Y5_R2FR_3019_BETA_SQUARE_LAW_PROOF_ATTEMPT.csv",
    "SRC3044_08_beta_field_contract": RESIDUALS / "P8_Y5_R2FR_3019_SECOND_ORDER_FIELD_EQUATION_CONTRACT.csv",
    "SRC3044_09_beta_fill_template": RESIDUALS / "P8_Y5_BETA_COEFFICIENT_FILL_INPUT.csv",
    "SRC3044_10_eh_mass_theorem": RESIDUALS / "P8_Y5_EH_MASS_PARAMETER_THEOREM.csv",
    "SRC3044_11_source_calibrated_eh": RESIDUALS / "P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv",
    "SRC3044_12_newton_stack": RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv",
    "SRC3044_13_pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "SRC3044_14_charge_attempt": RESIDUALS / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
    "SRC3044_15_hilbert_contract": RESIDUALS / "P8_Hilbert_monopole_calibration_CONTRACT.csv",
    "SRC3044_16_symbol_map": RESIDUALS / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
    "SRC3044_17_min_parent_blocks": RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3044_SOURCE_REGISTER.csv",
    "theorem": RESIDUALS / "P8_Y5_R2FR_3044_AW_SOURCE_AMPLITUDE_THEOREM_ATTEMPT.csv",
    "poisson": RESIDUALS / "P8_Y5_R2FR_3044_POISSON_UNIQUENESS_PROOF_ROUTE.csv",
    "aliases": RESIDUALS / "P8_Y5_R2FR_3044_AW_ALIAS_MAP.csv",
    "bound": RESIDUALS / "P8_Y5_R2FR_3044_DWPHI_AW_BOUND_ROW_SCHEMA.csv",
    "countermodels": RESIDUALS / "P8_Y5_R2FR_3044_COUNTERMODEL_LEDGER.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3044_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3044_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3044_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3044_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3044_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_copy": PARENT_ACTION / "AW_source_amplitude_theorem_3044_NOT_SIGNED.csv",
    "poisson_copy": PARENT_ACTION / "AW_poisson_uniqueness_route_3044_CONDITIONAL_NONCLAIM.csv",
    "alias_copy": PARENT_ACTION / "AW_alias_map_3044_NONCLAIM.csv",
    "bound_copy": LOCAL_BOUNDS / "D_WPhi_AW_bound_schema_3044_BLOCKED_NONCLAIM.csv",
    "queue_copy": RAB_QUEUE / "JR3044_LINEAR_SOURCE_NORMALIZATION_COEFFICIENT_MAP_NEXT_NONCLAIM.csv",
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
    "SRC3044_00_3043_doc": "3043 handoff: W cannot be retired; A_W is next target",
    "SRC3044_01_3043_bound": "D_WPhi first bound row blocked by missing A_W",
    "SRC3044_02_3043_decision": "W retirement decision ledger",
    "SRC3044_03_3043_next": "explicit 3044 target selector",
    "SRC3044_04_gamma_kernel": "A_T/A_S PPN gamma algebra",
    "SRC3044_05_gamma_fill_contract": "A_T source-normalization contract",
    "SRC3044_06_gamma_fill_attempt": "A_T value unfilled attempt",
    "SRC3044_07_beta_square_law": "A_source/B_source beta extraction and square law",
    "SRC3044_08_beta_field_contract": "linear and quadratic coefficient contract",
    "SRC3044_09_beta_fill_template": "unfilled A/B coefficient template",
    "SRC3044_10_eh_mass_theorem": "conditional EH mass-family control theorem",
    "SRC3044_11_source_calibrated_eh": "source-calibrated EH proof stack",
    "SRC3044_12_newton_stack": "source-normalized Newton rungs",
    "SRC3044_13_pg_contract": "Poisson/Gauss/source calibration contract",
    "SRC3044_14_charge_attempt": "charge/current equality attempt",
    "SRC3044_15_hilbert_contract": "Hilbert monopole calibration contract",
    "SRC3044_16_symbol_map": "symbol to action map",
    "SRC3044_17_min_parent_blocks": "minimum parent local-GR action blocks",
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

theorem_rows = [
    base(
        {
            "theorem_id": "AW3044_0_metric_relation",
            "claim_piece": "weak-field metric coefficient relation",
            "statement": "From g00=-1+2 A_W W/c^2+O(W^2), the metric potential readout is Phi_metric=A_W W+O(W^2).",
            "result": "ALGEBRAIC_RELATION_DERIVED",
            "owned_by_mts_parent": True,
            "missing_for_claim": "not_missing_for_relation_only",
            "claim_effect": "turns W=Phi into the sharper A_W=1 problem",
        }
    ),
    base(
        {
            "theorem_id": "AW3044_1_poisson_uniqueness",
            "claim_piece": "conditional A_W=1 theorem",
            "statement": "If Phi_metric and W solve the same same-frame Poisson/source equation with the same boundary condition before measured-GM fitting, then H=Phi_metric-W is harmonic with zero boundary data, so H=0 and A_W=1 on the nonzero local branch.",
            "result": "CONDITIONAL_PROOF_ROUTE_FOUND",
            "owned_by_mts_parent": False,
            "missing_for_claim": "MISSING_PARENT_LINEAR_FIELD_EQUATION_FOR_PHI; MISSING_PARENT_SOURCE_DEFINITION_FOR_W; MISSING_SAME_BOUNDARY_AND_FRAME_PROOF",
            "claim_effect": "exact route to Newtonian normalization, but not current evidence",
        }
    ),
    base(
        {
            "theorem_id": "AW3044_2_current_AW_status",
            "claim_piece": "current parent status of A_W",
            "statement": "Existing A_T/A_source rows identify the needed coefficient but leave it unfilled or parent-unsigned.",
            "result": "A_W_NOT_PARENT_SIGNED",
            "owned_by_mts_parent": False,
            "missing_for_claim": "MISSING_A_T_PARENT_SOURCE_NORMALIZATION; MISSING_A_SOURCE_PARENT_LINEAR_COEFFICIENT_MAP",
            "claim_effect": "no W=Phi, Newton, PPN or local-GR promotion",
        }
    ),
    base(
        {
            "theorem_id": "AW3044_3_orbital_shortcut_rejected",
            "claim_piece": "measured-GM cannot set A_W=1",
            "statement": "U=A_W W or mu_obs=G M can absorb a common first-order amplitude; it does not prove that W was parent-normalized as Phi_metric before calibration.",
            "result": "NO_ORBITAL_GM_SHORTCUT",
            "owned_by_mts_parent": True,
            "missing_for_claim": "MISSING_FIXED_BEFORE_READOUT_SOURCE_CONVENTION",
            "claim_effect": "prevents a circular Newton proof",
        }
    ),
    base(
        {
            "theorem_id": "AW3044_4_residual_bound_law",
            "claim_piece": "D_WPhi bound algebra",
            "statement": "If A_W=1+epsilon_A and |epsilon_A|<1, then D_WPhi=W/Phi_metric-1=-epsilon_A/(1+epsilon_A), hence |D_WPhi|<=Delta_A/(1-Delta_A) for |epsilon_A|<=Delta_A<1.",
            "result": "BOUND_KERNEL_DERIVED_VALUES_MISSING",
            "owned_by_mts_parent": True,
            "missing_for_claim": "MISSING_NUMERIC_OR_THEOREM_ZERO_DELTA_A",
            "claim_effect": "creates an executable fallback once A_W components are sourced",
        }
    ),
    base(
        {
            "theorem_id": "AW3044_5_verdict",
            "claim_piece": "current A_W=1 claim",
            "statement": "The clean theorem exists, but its premises are not signed by the current parent-action/source-normalization stack.",
            "result": "A_W_EQUALS_ONE_NOT_CLAIMED",
            "owned_by_mts_parent": False,
            "missing_for_claim": "MISSING_LINEAR_SOURCE_NORMALIZATION_COEFFICIENT_MAP",
            "claim_effect": "move to linear coefficient map or finite A_W residual acquisition",
        }
    ),
]

poisson_route = [
    base(
        {
            "rung_id": "PUN3044_0_same_frame",
            "required_identity": "Phi_metric and W live in the same observed/source frame before readout fitting",
            "math_form": "e_obs=e_source=e_readout; delta_frame_source=0",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "source_anchor": "P8_source_normalized_Newton_branch_STACK.csv SN0",
            "failure_if_missing": "A_W can be a frame/readout conversion rather than a field-equation coefficient",
        }
    ),
    base(
        {
            "rung_id": "PUN3044_1_metric_phi_equation",
            "required_identity": "the 00 parent metric equation reduces to Poisson for Phi_metric",
            "math_form": "nabla^2 Phi_metric = 4*pi*G_ref*rho_H + residual_Phi",
            "current_status": "CONDITIONAL_FORMULA_ONLY",
            "source_anchor": "P8_source_normalized_Newton_branch_STACK.csv SN5",
            "failure_if_missing": "Phi_metric source coefficient remains A_T/A_source rather than one",
        }
    ),
    base(
        {
            "rung_id": "PUN3044_2_W_source_equation",
            "required_identity": "W is defined by the same parent Hilbert/source density, not by post-fit orbital GM",
            "math_form": "nabla^2 W = 4*pi*G_ref*rho_H + residual_W",
            "current_status": "DENOMINATOR_CONTRACT_PRESENT_UNSIGNED",
            "source_anchor": "P8_Y5_R2FR_3019_SECOND_ORDER_FIELD_EQUATION_CONTRACT.csv FEC3019_0",
            "failure_if_missing": "W is just a source-coordinate potential and A_W remains free",
        }
    ),
    base(
        {
            "rung_id": "PUN3044_3_residual_equality",
            "required_identity": "all non-EH/source/boundary/range/readout residuals in the two equations are zero or identical common-mode terms",
            "math_form": "residual_Phi-residual_W=0",
            "current_status": "MISSING_ZERO_OR_BOUND_FOR_RESIDUAL_DIFFERENCE",
            "source_anchor": "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv PG6/PG9",
            "failure_if_missing": "Phi_metric-W is sourced, so uniqueness cannot force A_W=1",
        }
    ),
    base(
        {
            "rung_id": "PUN3044_4_boundary_lock",
            "required_identity": "same additive constant/asymptotic condition and compact exterior domain",
            "math_form": "H=Phi_metric-W; nabla^2 H=0; H|boundary=0 or H->0 at infinity",
            "current_status": "MISSING_SAME_BOUNDARY_OR_ASYMPTOTIC_LOCK",
            "source_anchor": "P8_Hilbert_monopole_calibration_CONTRACT.csv HM5/HM7",
            "failure_if_missing": "constant or radial boundary hair can mimic an amplitude shift",
        }
    ),
    base(
        {
            "rung_id": "PUN3044_5_uniqueness_step",
            "required_identity": "maximum principle or standard elliptic uniqueness applies on the local exterior",
            "math_form": "nabla^2 H=0 with zero boundary data implies H=0",
            "current_status": "MATH_STEP_VALID_IF_PRIOR_RUNGS_PASS",
            "source_anchor": "3044 derivation",
            "failure_if_missing": "not a blocker; mathematical step is ordinary once premises exist",
        }
    ),
    base(
        {
            "rung_id": "PUN3044_6_AW_conclusion",
            "required_identity": "Phi_metric=A_W W and Phi_metric=W on the same nonzero branch",
            "math_form": "A_W=1; D_WPhi=0",
            "current_status": "CONCLUSION_BLOCKED_BY_PRIOR_RUNGS",
            "source_anchor": "3043 relation plus PUN3044_0-5",
            "failure_if_missing": "A_W remains a residual coefficient",
        }
    ),
]

alias_rows = [
    base(
        {
            "alias_id": "AWA3044_0_AW",
            "symbol": "A_W",
            "meaning": "linear amplitude relating source-coordinate W to metric potential Phi_metric",
            "relation": "Phi_metric=A_W W",
            "status": "TARGET_COEFFICIENT",
            "guard": "not set to one without same-source Poisson uniqueness or parent coefficient map",
        }
    ),
    base(
        {
            "alias_id": "AWA3044_1_A_source",
            "symbol": "A_source",
            "meaning": "linear coefficient in g00=-1+2 A_source W/c^2",
            "relation": "candidate same object as A_W in beta chain",
            "status": "ALIAS_IF_SAME_GAUGE_AND_DENOMINATOR",
            "guard": "3019 marks parent linear coefficient map missing",
        }
    ),
    base(
        {
            "alias_id": "AWA3044_2_A_T",
            "symbol": "A_T",
            "meaning": "time-time weak-field coefficient used by gamma extraction",
            "relation": "candidate same object as A_W after fixed-GM comparison",
            "status": "ALIAS_IF_SAME_SOURCE_NORMALIZATION",
            "guard": "3018 marks A_T value unfilled",
        }
    ),
    base(
        {
            "alias_id": "AWA3044_3_epsilon_A",
            "symbol": "epsilon_A",
            "meaning": "A_W-1 after a chosen parent-normalized reference branch",
            "relation": "A_W=1+epsilon_A",
            "status": "RESIDUAL_PARAMETER",
            "guard": "needs theorem-zero or numeric source-backed bound",
        }
    ),
    base(
        {
            "alias_id": "AWA3044_4_DWPhi",
            "symbol": "D_WPhi",
            "meaning": "relative mismatch between W and Phi_metric",
            "relation": "D_WPhi=1/A_W-1=-epsilon_A/(1+epsilon_A)",
            "status": "BOUND_KERNEL_READY_VALUES_MISSING",
            "guard": "no prediction row until Delta_A is sourced",
        }
    ),
]

bound_rows = [
    base(
        {
            "bound_id": "DWA3044_0_relation",
            "quantity": "D_WPhi_from_AW",
            "expression": "D_WPhi=W/Phi_metric-1=1/A_W-1",
            "units": "dimensionless",
            "status": "DERIVED_ALGEBRAIC_KERNEL",
            "blocking_issue": "MISSING_A_W_VALUE_OR_ZERO_THEOREM",
            "observable_link": "PPN gamma/beta; Newton source normalization; R10 local source channel",
            "next_action": "derive A_W=1 or fill epsilon_A component envelope",
        }
    ),
    base(
        {
            "bound_id": "DWA3044_1_component_envelope",
            "quantity": "Delta_A",
            "expression": "|epsilon_A| <= |epsilon_linear_source|+|epsilon_frame|+|epsilon_boundary|+|epsilon_range|+|epsilon_readout|",
            "units": "dimensionless",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "blocking_issue": "MISSING_COMPONENT_VALUES; MISSING_SOURCE_PATHED_NUMERIC_ROWS",
            "observable_link": "first executable A_W/D_WPhi bound row",
            "next_action": "source each component or prove theorem-zero",
        }
    ),
    base(
        {
            "bound_id": "DWA3044_2_total_bound",
            "quantity": "D_WPhi_total_abs",
            "expression": "|D_WPhi| <= Delta_A/(1-Delta_A) for Delta_A<1",
            "units": "dimensionless",
            "status": "BOUND_FORMULA_READY_NO_VALID_ROW",
            "blocking_issue": "MISSING_DELTA_A_NUMERIC_BOUND_OR_ZERO_THEOREM",
            "observable_link": "3042/3043 D_WPhi branch",
            "next_action": "do not run claim comparator until Delta_A is real",
        }
    ),
]

countermodels = [
    base(
        {
            "countermodel_id": "CM3044_0_common_amplitude",
            "case": "Phi_metric=A_W W with constant A_W not equal to one",
            "why_it_blocks": "orbital U=A_W W can still be fitted as measured GM, so data calibration alone does not prove parent normalization",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3044_1_different_source_coefficients",
            "case": "nabla^2 Phi_metric=4*pi*G_phi rho and nabla^2 W=4*pi*G_W rho",
            "why_it_blocks": "same density but different coefficients gives A_W=G_phi/G_W",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3044_2_boundary_offset_or_hair",
            "case": "Phi_metric-W solves Laplace equation with nonzero boundary/asymptotic data",
            "why_it_blocks": "homogeneous exterior mode is not forced to vanish",
            "status": "LIVE_BLOCKER",
        }
    ),
    base(
        {
            "countermodel_id": "CM3044_3_residual_source_difference",
            "case": "R11, range, boundary, source-current or readout residual enters one equation but not the other",
            "why_it_blocks": "Phi_metric-W is sourced, so uniqueness theorem does not apply",
            "status": "LIVE_BLOCKER",
        }
    ),
]

gates = [
    base({"gate_id": "GATE3044_0_sources_exist", "gate": "all cited source paths exist", "passed": all(boolish(r["exists"]) for r in source_register), "claim_effect": "audit is source-backed"}),
    base({"gate_id": "GATE3044_1_AW_relation", "gate": "Phi_metric=A_W W relation is derived from weak-field metric grammar", "passed": True, "claim_effect": "sharpens W=Phi into A_W=1"}),
    base({"gate_id": "GATE3044_2_poisson_route", "gate": "Poisson uniqueness route to A_W=1 is written", "passed": True, "claim_effect": "gives exact proof contract"}),
    base({"gate_id": "GATE3044_3_parent_source_equations", "gate": "same-source Phi and W equations are parent-signed", "passed": False, "claim_effect": "blocks A_W=1 claim"}),
    base({"gate_id": "GATE3044_4_boundary_lock", "gate": "same boundary/asymptotic condition is parent-signed", "passed": False, "claim_effect": "blocks uniqueness conclusion"}),
    base({"gate_id": "GATE3044_5_no_residual_difference", "gate": "R11/source/boundary/range/readout residual difference is zero or bounded", "passed": False, "claim_effect": "blocks D_WPhi=0"}),
    base({"gate_id": "GATE3044_6_no_orbital_shortcut", "gate": "measured-GM shortcut is explicitly rejected", "passed": True, "claim_effect": "prevents circular Newton proof"}),
    base({"gate_id": "GATE3044_7_no_claim_rows", "gate": "no generated 3044 row is valid for claim", "passed": True, "claim_effect": "private nonclaim checkpoint"}),
    base({"gate_id": "GATE3044_8_next_target", "gate": "next target selects linear source-normalization coefficient map", "passed": True, "claim_effect": "points to the real missing coefficient"}),
]

decision_rows = [
    base(
        {
            "decision_id": "DEC3044_0_relation",
            "question": "what is the exact local relation between W and Phi_metric?",
            "answer": "Phi_metric=A_W W",
            "reason": "weak-field metric grammar contains g00=-1+2 A_W W/c^2",
            "action": "stop arguing W; target A_W",
        }
    ),
    base(
        {
            "decision_id": "DEC3044_1_AW_equals_one",
            "question": "is A_W=1 proved now?",
            "answer": "NO",
            "reason": "same-source Poisson equations, residual silence and boundary lock are not parent-signed",
            "action": "keep A_W/D_WPhi as explicit residual",
        }
    ),
    base(
        {
            "decision_id": "DEC3044_2_conditional_theorem",
            "question": "is there a respectable derivation route?",
            "answer": "YES_CONDITIONAL",
            "reason": "Poisson uniqueness proves Phi_metric=W if both solve the same parent source problem with same boundary data",
            "action": "turn that route into a coefficient-map checklist",
        }
    ),
    base(
        {
            "decision_id": "DEC3044_3_bound",
            "question": "can a numeric D_WPhi bound row be created now?",
            "answer": "NO",
            "reason": "Delta_A components have no source-backed numeric values or theorem-zero certificates",
            "action": "stage schema only; do not run as evidence",
        }
    ),
    base(
        {
            "decision_id": "DEC3044_4_next",
            "question": "what is the least-smuggly next target?",
            "answer": "linear source-normalization coefficient map",
            "reason": "A_W=1 reduces to same-source linear field equation plus boundary/residual silence",
            "action": "3045 should extract or bound the linear coefficient map directly",
        }
    ),
]

next_rows = [
    base(
        {
            "next_id": "NEXT3044_0_3045",
            "next_checkpoint": "3045-Y5-R2FR-linear-source-normalization-coefficient-map-or-AW-bound-row-under-AX1090.md",
            "script_stub": "scripts/Y5_R2FR_linear_source_normalization_coefficient_map_or_AW_bound_row_under_AX1090_3045.py",
            "mission": "derive same-source linear field equations for Phi_metric and W, including boundary/residual silence, or create source-backed epsilon_A component rows",
            "starting_equation": "Phi_metric=A_W W; A_W=1+epsilon_A; D_WPhi=-epsilon_A/(1+epsilon_A)",
            "do_not_repeat": "do not infer A_W=1 from U=A_W W, beta extraction grammar, or fitted orbital GM",
            "claim_policy": "no Newton/PPN/local-GR claim until A_W or Delta_A is theorem-zero or source-backed numeric",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["theorem"], theorem_rows)
write_csv(OUTPUTS["poisson"], poisson_route)
write_csv(OUTPUTS["aliases"], alias_rows)
write_csv(OUTPUTS["bound"], bound_rows)
write_csv(OUTPUTS["countermodels"], countermodels)
write_csv(OUTPUTS["gates"], gates)
write_csv(OUTPUTS["decision"], decision_rows)
write_csv(OUTPUTS["next"], next_rows)

branch_map = [
    ("theorem_copy", OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_copy"], "A_W theorem attempt copy"),
    ("poisson_copy", OUTPUTS["poisson"], BRANCH_OUTPUTS["poisson_copy"], "conditional Poisson uniqueness route copy"),
    ("alias_copy", OUTPUTS["aliases"], BRANCH_OUTPUTS["alias_copy"], "A_W alias map copy"),
    ("bound_copy", OUTPUTS["bound"], BRANCH_OUTPUTS["bound_copy"], "blocked D_WPhi/A_W bound schema copy"),
    ("queue_copy", OUTPUTS["next"], BRANCH_OUTPUTS["queue_copy"], "3045 acquisition queue copy"),
]
branch_rows: list[dict[str, Any]] = []
for copy_id, source, destination, description in branch_map:
    shutil.copyfile(source, destination)
    branch_rows.append(
        base(
            {
                "copy_id": copy_id,
                "source": str(source),
                "destination": str(destination),
                "exists": destination.exists(),
                "description": description,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

if PYCACHE.exists():
    shutil.rmtree(PYCACHE)

generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
branch_csv_paths = list(BRANCH_OUTPUTS.values())
formalization_hits = list(FORMALIZATION.rglob("*3044*")) if FORMALIZATION.exists() else []

all_csv_rows: list[dict[str, str]] = []
for path in csv_paths:
    all_csv_rows.extend(rows(path))

validation_rows = [
    base({"validation_id": "VAL3044_00_sources_exist", "passed": all(boolish(r["exists"]) for r in source_register), "requirement": "all cited source paths exist", "evidence": OUTPUTS["sources"].name}),
    base({"validation_id": "VAL3044_01_csv_parse", "passed": all(csv_ok(path) for path in csv_paths), "requirement": "all generated CSV and branch-copy rows parse cleanly", "evidence": "csv.DictReader parse check"}),
    base({"validation_id": "VAL3044_02_relation_identified", "passed": any(r["theorem_id"] == "AW3044_0_metric_relation" and r["result"] == "ALGEBRAIC_RELATION_DERIVED" for r in theorem_rows), "requirement": "Phi_metric=A_W W relation is recorded", "evidence": OUTPUTS["theorem"].name}),
    base({"validation_id": "VAL3044_03_poisson_route", "passed": any(r["rung_id"] == "PUN3044_5_uniqueness_step" for r in poisson_route), "requirement": "Poisson uniqueness proof route is present", "evidence": OUTPUTS["poisson"].name}),
    base({"validation_id": "VAL3044_04_AW_not_promoted", "passed": any(r["theorem_id"] == "AW3044_5_verdict" and r["result"] == "A_W_EQUALS_ONE_NOT_CLAIMED" for r in theorem_rows), "requirement": "A_W=1 is not claimed", "evidence": OUTPUTS["theorem"].name}),
    base({"validation_id": "VAL3044_05_bound_fail_closed", "passed": any(r["bound_id"] == "DWA3044_2_total_bound" and r["status"] == "BOUND_FORMULA_READY_NO_VALID_ROW" for r in bound_rows), "requirement": "D_WPhi bound row remains blocked without Delta_A", "evidence": OUTPUTS["bound"].name}),
    base({"validation_id": "VAL3044_06_no_claim_rows", "passed": not any(boolish(r.get("valid_for_claim")) or boolish(r.get("claim_allowed")) or boolish(r.get("valid_prediction_row")) for r in all_csv_rows), "requirement": "no 3044 row is valid for claim", "evidence": "generated rows"}),
    base({"validation_id": "VAL3044_07_countermodels_live", "passed": len(countermodels) >= 4 and all(row["status"] == "LIVE_BLOCKER" for row in countermodels), "requirement": "countermodels block shortcut promotion", "evidence": OUTPUTS["countermodels"].name}),
    base({"validation_id": "VAL3044_08_branch_copies", "passed": all(path.exists() and csv_ok(path) for path in branch_csv_paths), "requirement": "branch copies exist and parse", "evidence": OUTPUTS["branches"].name}),
    base({"validation_id": "VAL3044_09_output_scope", "passed": all(under(path, ROOT) for path in generated_paths), "requirement": "all generated outputs are inside post-checkpoint-work", "evidence": str(ROOT)}),
    base({"validation_id": "VAL3044_10_formalization_untouched", "passed": len(formalization_hits) == 0, "requirement": "formalization-workbench modified-file target count remains 0", "evidence": f"formalization 3044 hits={len(formalization_hits)}"}),
    base({"validation_id": "VAL3044_11_next_target", "passed": next_rows[0]["next_checkpoint"].startswith("3045-"), "requirement": "next target selects linear source-normalization coefficient map", "evidence": OUTPUTS["next"].name}),
    base({"validation_id": "VAL3044_12_pycache_removed", "passed": not PYCACHE.exists(), "requirement": "scripts __pycache__ removed", "evidence": str(PYCACHE)}),
]
write_csv(OUTPUTS["validation"], validation_rows)

doc_text = f"""# 3044 - A_W Source-Amplitude Theorem or D_WPhi Bound Row

Status: `Y5_R2FR_3044_AW_not_signed_poisson_uniqueness_route_ready`

Generated: `{RUN_UTC}`

## Verdict

3044 sharpens the previous `W`/`Phi_metric` obstruction into the actual local source-amplitude coefficient:

`Phi_metric = A_W W`.

The useful derivation route is now exact: if `Phi_metric` and `W` are parent-owned solutions of the same same-frame Poisson/source equation with the same boundary/asymptotic condition, then their difference is harmonic with zero boundary data, so `Phi_metric=W` and `A_W=1`.

But the current corpus does not yet sign those premises. Existing `A_T`/`A_source` rows mark the coefficient as missing or parent-unsigned, and a fitted orbital `GM` can absorb a common first-order amplitude. Therefore 3044 does not claim `A_W=1`, `D_WPhi=0`, Newton, PPN, or local GR.

## Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "claim_piece", "result", "missing_for_claim", "claim_effect"])}

## Poisson Uniqueness Route

{md_table(poisson_route, ["rung_id", "required_identity", "math_form", "current_status", "failure_if_missing"])}

## Alias Map

{md_table(alias_rows, ["alias_id", "symbol", "relation", "status", "guard"])}

## D_WPhi / A_W Bound Schema

{md_table(bound_rows, ["bound_id", "quantity", "expression", "status", "blocking_issue", "next_action"])}

## Countermodels

{md_table(countermodels, ["countermodel_id", "case", "why_it_blocks", "status"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "question", "answer", "reason", "action"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "passed", "claim_effect"])}

## Next Target

{md_table(next_rows, ["next_id", "next_checkpoint", "mission", "starting_equation", "claim_policy"])}

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "destination", "exists", "description"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}
"""

DOC.write_text(doc_text, encoding="utf-8")

failures = [row for row in validation_rows if not boolish(row["passed"])]
if failures:
    raise SystemExit(f"3044 validation failed: {[row['validation_id'] for row in failures]}")

print(f"wrote {DOC}")
print(f"validation rows: {len(validation_rows)} passed")
print("claim status: A_W=1 not claimed; D_WPhi bound schema only")
