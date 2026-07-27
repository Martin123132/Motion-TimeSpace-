from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1866"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1866-Y5-R2FR-reciprocity-selector-operator-or-Hcore-source-equation.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_SOURCE_REGISTER.csv",
    "selector_route_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_SELECTOR_ROUTE_AUDIT.csv",
    "hcore_source_equation_test": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_HCORE_SOURCE_EQUATION_TEST.csv",
    "lambdar_origin_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_LAMBDAR_ORIGIN_GATE.csv",
    "finite_zrjr_requirements": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_FINITE_ZRJR_REQUIREMENTS.csv",
    "no_gr_import_guard": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_NO_GR_IMPORT_GUARD.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1866_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1866_VALIDATION.csv",
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
            "source_id": "SRC1866_0_1865_doc",
            "source_kind": "current_handoff",
            "source_path": ROOT / "1865-Y5-R2FR-parent-Euler-difference-normal-form-or-SR-residual-decomposition.md",
            "required_needle": "NEXT1865_0_primary",
            "use_in_1866": "selects the reciprocity-selector/Hcore source-equation target.",
        },
        {
            "source_id": "SRC1866_1_1865_validation",
            "source_kind": "validation_anchor",
            "source_path": RESIDUALS / "P8_Y5_BRR545_1865_VALIDATION.csv",
            "required_needle": "VAL1865_OVERALL",
            "use_in_1866": "confirms the parent Euler difference checkpoint passed before this gate.",
        },
        {
            "source_id": "SRC1866_2_1865_missing",
            "source_kind": "selector_missing_ledger",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1865_MISSING_INPUT_LEDGER.csv",
            "required_needle": "MIL1865_1_orientation",
            "use_in_1866": "imports the missing Euler orientation/sign certificate.",
        },
        {
            "source_id": "SRC1866_3_1256_Hcore",
            "source_kind": "minimal_Hcore_contract",
            "source_path": RESIDUALS / "P8_Y5_R10_1256_MINIMAL_HCORE_SOURCE_EQUATION_CONTRACT.csv",
            "required_needle": "HC1256_0_minimal_density",
            "use_in_1866": "supplies the formal reciprocal Hcore density and Euler equation.",
        },
        {
            "source_id": "SRC1866_4_1257_selector",
            "source_kind": "ZR_lambda_selector_clause",
            "source_path": RESIDUALS / "P8_Y5_R10_1257_ZR_LAMBDAR_SELECTOR_CLAUSES.csv",
            "required_needle": "SEL1257_0_field_exclusion",
            "use_in_1866": "states the object-language route for forbidding derivative R_AB terms.",
        },
        {
            "source_id": "SRC1866_5_1273_Hcore_owner",
            "source_kind": "Hcore_owner_classification",
            "source_path": RESIDUALS / "P8_Y5_R10_1273_HCORE_OWNER_CLASSIFICATION.csv",
            "required_needle": "HCO1273_4_linear_multiplier",
            "use_in_1866": "identifies the strongest conditional exact-zero mechanism.",
        },
        {
            "source_id": "SRC1866_6_1273_Dirac",
            "source_kind": "Dirac_preservation_audit",
            "source_path": RESIDUALS / "P8_Y5_R10_1273_DIRAC_PRESERVATION_AUDIT.csv",
            "required_needle": "DPA1273_5_conditional_theorem",
            "use_in_1866": "keeps the multiplier theorem conditional until constraint preservation closes.",
        },
        {
            "source_id": "SRC1866_7_1622_lambda_origin",
            "source_kind": "lambdaR_parent_origin_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1622_LAMBDAR_PARENT_ORIGIN_AUDIT.csv",
            "required_needle": "LAMBDAR_PARENT_ORIGIN_NOT_DERIVED",
            "use_in_1866": "prevents promoting lambda_R C_R to a parent theorem.",
        },
        {
            "source_id": "SRC1866_8_1248_Dirac",
            "source_kind": "minimal_multiplier_Dirac_check",
            "source_path": RESIDUALS / "P8_Y5_R10_1248_DIRAC_CHECK.csv",
            "required_needle": "DIR1248_2_preservation",
            "use_in_1866": "records the missing H_core/bracket preservation check.",
        },
        {
            "source_id": "SRC1866_9_observer_contract",
            "source_kind": "observer_map_contract",
            "source_path": ROOT / "10-observer-map-symplectic-contract.md",
            "required_needle": "observer_map_contract_written_not_satisfied",
            "use_in_1866": "states the future parent-action contract for local vacuum reciprocity.",
        },
        {
            "source_id": "SRC1866_10_cell_current",
            "source_kind": "cell_current_no_charge_attempt",
            "source_path": ROOT / "11-cell-current-origin-attempt.md",
            "required_needle": "ordinary cell-current conservation does not close",
            "use_in_1866": "shows conserved current alone leaves Q_R hair.",
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
                "use_in_1866": source_entry["use_in_1866"],
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def selector_route_audit() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "RSA1866_0_target_orientation",
            "candidate_selector": "parent Euler orientation for C_R",
            "calculation_or_contract": "Need a parent-owned combination E_sel such that E_sel = partial_r C_R - S_R or algebraically E_Lambda = C_R before readout.",
            "best_possible_result": "D_R_NORMAL_FORM_DERIVED_IF_PARENT_SIGNED",
            "actual_status": "TARGET_DEFINED_NOT_DERIVED",
            "missing_input": "MISSING_RECIPROCITY_SELECTOR_ORIENTATION",
            "decision": "test concrete selector routes rather than assume E_time-E_radial selects C_R.",
            "selector_signed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RSA1866_1_object_language_exclusion",
            "candidate_selector": "typed parent grammar excludes independent R_AB field",
            "calculation_or_contract": "If R_AB is only a compatibility/cell-balance object, then D_i R_AB D^i R_AB and ordinary scalar potentials are not legal parent terms.",
            "best_possible_result": "Z_R_EQUALS_ZERO_BY_OBJECT_LANGUAGE",
            "actual_status": "BEST_LOW_SCRUTINY_ROUTE_NOT_SIGNED",
            "missing_input": "MISSING_TYPED_PARENT_CONSTRUCTOR_LIST",
            "decision": "pursue next because it avoids adding a new propagating scalar and is less vulnerable to fifth-force scrutiny.",
            "selector_signed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RSA1866_2_linear_multiplier",
            "candidate_selector": "lambda_R C_R or lambda_R(partial_r C_R-S_R)",
            "calculation_or_contract": "delta_lambda gives C_R=0 or partial_r C_R=S_R exactly; delta_C fixes lambda_R only after source/boundary compatibility.",
            "best_possible_result": "EXACT_LOCAL_RECIPROCITY_IF_PARENT_OWNED",
            "actual_status": "FORMAL_PASS_NOT_PARENT_SIGNED",
            "missing_input": "MISSING_LAMBDAR_PARENT_ORIGIN_DIRAC_MATTER_BOUNDARY",
            "decision": "retain as exact closure template, not a derivation.",
            "selector_signed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RSA1866_3_second_order_Hcore",
            "candidate_selector": "ordinary reciprocal Hcore with Z_R, M_R^2, J_R",
            "calculation_or_contract": "-D_i(Z_R D^i R_AB)+M_R^2 R_AB+lambda_R+J_R plus coefficient variations = 0.",
            "best_possible_result": "FINITE_ELLIPTIC_SUPPRESSION_OR_MASS_GAP",
            "actual_status": "FINITE_BRANCH_NOT_ZERO_PROOF",
            "missing_input": "MISSING_ZR_MR2_JR_BOUNDARY_SOURCE_AND_NO_CHARGE",
            "decision": "use only as source-ready residual branch unless object-language/multiplier proof closes.",
            "selector_signed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RSA1866_4_cell_current",
            "candidate_selector": "conserved reciprocal cell current",
            "calculation_or_contract": "partial_r(W partial_r R_AB)=0 gives W partial_r R_AB=Q_R.",
            "best_possible_result": "Q_R_ZERO_IF_PARENT_NO_CHARGE_THEOREM",
            "actual_status": "CONSERVATION_ONLY_LEAVES_HAIR",
            "missing_input": "MISSING_QR_ZERO_THEOREM_AND_BOUNDARY_CHARGE_CLASS",
            "decision": "hold as parallel no-charge theorem target, not the main selector proof.",
            "selector_signed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RSA1866_5_verdict",
            "candidate_selector": "1866 selector proof",
            "calculation_or_contract": "All available exact-zero routes require an unsigned parent grammar, multiplier origin, Dirac chain, or no-charge theorem.",
            "best_possible_result": "LOCAL_GR_SELECTOR_DERIVED",
            "actual_status": "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS",
            "missing_input": "MISSING_PARENT_OBJECT_LANGUAGE_OR_SIGNED_HCORE",
            "decision": "demote D_R to closure-only benchmark and move to object-language radial-cell constraint or finite Z_R/J_R intake.",
            "selector_signed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def hcore_source_equation_test() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "test_id": "HSE1866_0_minimal_density",
            "object": "reciprocal Hcore density",
            "equation_or_condition": "H_R=int sqrt(h)[1/2 Z_R h^ij D_i R_AB D_j R_AB + 1/2 M_R^2 R_AB^2 + lambda_R R_AB + J_R R_AB] + boundary B_R",
            "inference": "This is a valid formal variational template, not a parent-derived action.",
            "status": "FORMAL_TEMPLATE_ONLY",
            "obstruction": "MISSING_PARENT_ORIGIN_OF_ZR_MR2_LAMBDAR_JR_BR",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "HSE1866_1_Euler_equation",
            "object": "R_AB Euler/source equation",
            "equation_or_condition": "E_R=-D_i(Z_R D^i R_AB)+M_R^2 R_AB+lambda_R+J_R+coefficient_variation_terms=0.",
            "inference": "An ordinary Hcore makes R_AB a finite residual field unless the parent grammar forbids those terms or a multiplier constraint closes.",
            "status": "FINITE_RESIDUAL_BY_DEFAULT",
            "obstruction": "MISSING_SELECTOR_ZERO_THEOREM",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "HSE1866_2_exact_zero_conditions",
            "object": "conditions for exact C_R=0",
            "equation_or_condition": "Need either object-language exclusion of independent R_AB plus parent constraint, or parent-owned lambda_R with closed Dirac chain, matter descent, boundary silence, and readout invariance.",
            "inference": "These conditions would prove the local plateau; current corpus has them as a contract only.",
            "status": "ZERO_CONDITIONS_KNOWN_NOT_SATISFIED",
            "obstruction": "MISSING_PARENT_SIGNATURE",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "HSE1866_3_mass_gap_branch",
            "object": "finite suppression branch",
            "equation_or_condition": "If Z_R>0 and M_R^2>0, ell_R=sqrt(Z_R/M_R^2) suppresses reciprocal hair only after J_R, boundary flux, and arena projections are sourced.",
            "inference": "This can become a data-bounded local branch, but not a derived-GR branch.",
            "status": "FINITE_BRANCH_SOURCE_READY_ONLY",
            "obstruction": "MISSING_NUMERIC_PARENT_COEFFICIENTS_AND_PROJECTIONS",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "test_id": "HSE1866_4_no_charge_branch",
            "object": "current/no-charge alternative",
            "equation_or_condition": "partial_r(W partial_r R_AB)=0 allows W partial_r R_AB=Q_R; asymptotic flatness alone does not force Q_R=0.",
            "inference": "No-charge theorem remains a separate proof obligation.",
            "status": "Q_R_HAIR_NOT_KILLED",
            "obstruction": "MISSING_BOUNDARY_NO_CHARGE_THEOREM",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def lambdar_origin_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LOG1866_0_variation",
            "object": "bare multiplier variation",
            "test": "delta_lambda int lambda_R C_R gives C_R=0.",
            "status": "FORMAL_PASS_NOT_DERIVATION",
            "why_not_enough": "variation proves the inserted term works; it does not prove the term belongs to the parent action.",
            "required_to_close": "parent primitive or auxiliary sector that forces lambda_R before local closure is chosen.",
            "gate_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LOG1866_1_Dirac",
            "object": "constraint preservation",
            "test": "Check primary/secondary chain, Poisson brackets, boundary class, and matter/readout invariance.",
            "status": "BLOCKED",
            "why_not_enough": "H_core, canonical brackets, constraint algebra, and boundary/corner variational class remain unsigned.",
            "required_to_close": "full parent canonical grammar for T/S or motion-time-space primitives.",
            "gate_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LOG1866_2_object_language",
            "object": "typed parent constructor list",
            "test": "Prove R_AB appears only as compatibility data and cannot carry Z_R, M_R^2, or direct matter source terms.",
            "status": "NOT_PARENT_DERIVED",
            "why_not_enough": "without the constructor list, a generic scalar countermodel survives.",
            "required_to_close": "explicit allowed-objects grammar: primitives, derived compatibility objects, allowed contractions, allowed measures, and forbidden derivative terms.",
            "gate_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LOG1866_3_second_class_auxiliary",
            "object": "algebraic auxiliary route",
            "test": "Use a second-class auxiliary pair so C_R=0 is eliminated before matter/readout coupling.",
            "status": "BEST_CONDITIONAL_ROUTE_NOT_SIGNED",
            "why_not_enough": "strongest exact route, but still needs parent sort, no-derivative grammar, stable reduced readout, and boundary silence.",
            "required_to_close": "signed auxiliary sector with no surviving reciprocal charge.",
            "gate_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "LOG1866_4_verdict",
            "object": "lambda_R origin",
            "test": "Can lambda_R C_R be treated as a parent theorem in this corpus?",
            "status": "LAMBDAR_PARENT_ORIGIN_NOT_DERIVED",
            "why_not_enough": "all live support is formal/conditional, not parent-signed.",
            "required_to_close": "object-language radial-cell proof or explicit H_core/L_core with closed Dirac and boundary checks.",
            "gate_closed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def finite_zrjr_requirements() -> list[dict[str, Any]]:
    requirements = [
        (
            "FZR1866_0_ZR",
            "Z_R",
            "reciprocal gradient stiffness",
            "needed if R_AB is allowed as finite elliptic/local field",
            "parent H_core/L_core coefficient or theorem Z_R=0",
            "dimension depends on declared R_AB normalization and radial measure",
        ),
        (
            "FZR1866_1_MR2",
            "M_R^2",
            "reciprocal mass/stiffness scale",
            "needed to define ell_R=sqrt(Z_R/M_R^2) and local suppression",
            "parent potential/auxiliary elimination coefficient or theorem M_R^2 absent",
            "inverse length squared in canonical normalization",
        ),
        (
            "FZR1866_2_JR",
            "J_R",
            "direct reciprocal source",
            "needed to know whether matter sources C_R/R_AB locally",
            "matter descent/source map coefficient",
            "same units as E_R source term after normalization",
        ),
        (
            "FZR1866_3_BR",
            "B_R",
            "boundary/corner reciprocal term",
            "needed to decide whether Q_R hair is permitted",
            "parent boundary variational class",
            "surface charge normalization units",
        ),
        (
            "FZR1866_4_lambdaR",
            "lambda_R",
            "nonpropagating reciprocity multiplier",
            "needed for exact local zero route",
            "parent primitive, auxiliary field, or constraint-chain origin",
            "same units as E_R source term",
        ),
        (
            "FZR1866_5_QR",
            "Q_R",
            "reciprocal exterior hair/current charge",
            "needed if current or gradient branch survives",
            "boundary/no-charge theorem or sourced finite charge estimate",
            "flux of Z_R n^i D_i R_AB over a two-surface",
        ),
        (
            "FZR1866_6_SR",
            "S_R",
            "total local reciprocal source residual",
            "needed for D_R=partial_r C_R-S_R benchmark",
            "coefficient map from q_loc, matter descent, boundary, readout, and current slots",
            "radial derivative of C_R in declared coordinate/observer gauge",
        ),
        (
            "FZR1866_7_R10_projection",
            "tau_R10",
            "short-range fifth-force projection",
            "needed if finite reciprocal branch affects Yukawa-like local tests",
            "arena projection from Z_R/M_R^2/J_R/Q_R to alpha(lambda)",
            "dimensionless alpha or force-ratio convention",
        ),
        (
            "FZR1866_8_PPN_projection",
            "tau_PPN",
            "post-Newtonian residual projection",
            "needed to compare gamma/beta/light deflection bounds",
            "arena projection from C_R/R_AB residual to PPN residual vector",
            "dimensionless PPN deviations",
        ),
        (
            "FZR1866_9_clock_projection",
            "tau_clock",
            "clock/redshift residual projection",
            "needed if time-space reciprocal residual shifts local clock observables",
            "arena projection from C_R/S_R to frequency/redshift residual",
            "fractional frequency or redshift deviation",
        ),
        (
            "FZR1866_10_orbital_projection",
            "tau_orbital",
            "orbital/precession residual projection",
            "needed for Solar-system and binary-system local checks",
            "arena projection from C_R/R_AB residual to acceleration/precession residual",
            "acceleration or angular precession convention",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for requirement_id, coefficient, role, why_needed, required_source, units in requirements:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "requirement_id": requirement_id,
                "coefficient_or_projection": coefficient,
                "role": role,
                "why_needed": why_needed,
                "required_source": required_source,
                "units_or_dimension": units,
                "status": "MISSING_PARENT_INPUT",
                "next_action": "derive from parent object-language/Hcore; otherwise source as finite nonclaim residual row",
                "claim_ready": as_bool_text(False),
                "valid_for_claim": as_bool_text(False),
            }
        )
    return rows


def no_gr_import_guard() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NGI1866_0_no_EH_identity",
            "forbidden_shortcut": "use the GR Einstein-equation radial/time difference as the MTS selector proof",
            "why_forbidden": "that imports the local-GR fixed point before deriving it.",
            "allowed_replacement": "derive the C_R selector from MTS parent object-language, H_core, or constraint algebra.",
            "guard_status": "ACTIVE_BLOCK",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NGI1866_1_no_schwarzschild_gauge",
            "forbidden_shortcut": "set T*S=1 because Schwarzschild coordinates do that in GR vacuum",
            "why_forbidden": "coordinate form is not a parent MTS theorem.",
            "allowed_replacement": "prove C_R=0 before readout or retain finite C_R residual rows.",
            "guard_status": "ACTIVE_BLOCK",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NGI1866_2_no_asymptotic_QR_zero",
            "forbidden_shortcut": "kill Q_R by asymptotic flatness alone",
            "why_forbidden": "the cell-current audit shows asymptotic flatness permits exterior Q_R/r hair.",
            "allowed_replacement": "derive a boundary no-charge theorem or bound Q_R as a finite source.",
            "guard_status": "ACTIVE_BLOCK",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NGI1866_3_no_data_derivation",
            "forbidden_shortcut": "treat local-test compatibility as a derivation of GR",
            "why_forbidden": "data can constrain a finite branch, but does not explain why the parent action reduces to GR.",
            "allowed_replacement": "separate theorem claims from empirical robustness branches.",
            "guard_status": "ACTIVE_BLOCK",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def claim_gate() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1866_0_selector",
            "claim": "parent reciprocity selector has been derived",
            "status": "BLOCKED",
            "blocking_reason": "MISSING_TYPED_PARENT_CONSTRUCTOR_LIST_OR_SIGNED_HCORE",
            "required_before_claim": "prove object-language exclusion, multiplier origin, or explicit H_core orientation.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1866_1_DR",
            "claim": "D_R=partial_r C_R-S_R is a derived parent Euler equation",
            "status": "BLOCKED",
            "blocking_reason": "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS",
            "required_before_claim": "signed selector plus coefficient/source map.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1866_2_local_GR",
            "claim": "local GR/Newton reduction is derived",
            "status": "BLOCKED",
            "blocking_reason": "C_R_ZERO_AND_Q_R_ZERO_NOT_PARENT_PROVED",
            "required_before_claim": "parent local vacuum theorem, no-charge theorem, and PPN residual map.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1866_3_R10_PPN_clock_orbital",
            "claim": "R10/PPN/clock/orbital local tests are passed",
            "status": "BLOCKED",
            "blocking_reason": "FINITE_ZR_JR_QR_SR_ARENA_PROJECTIONS_MISSING",
            "required_before_claim": "numeric sourced coefficients and arena projection functions.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1866_4_public",
            "claim": "1866 supports public local-GR claim",
            "status": "BLOCKED",
            "blocking_reason": "PRIVATE_DERIVATION_GATE_NOT_CLOSED",
            "required_before_claim": "do not publicize as proof; keep as internal derivation discipline.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1866_0_result",
            "decision": "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS",
            "basis": "object-language exclusion, linear multiplier, second-order Hcore, and cell-current routes all remain parent-unsigned.",
            "consequence": "no local-GR/Newton reduction claim from 1866.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1866_1_demote_DR",
            "decision": "D_R_DEMOTED_TO_CLOSURE_BENCHMARK",
            "basis": "the D_R normal form is exact as a target but not derived from a live parent action.",
            "consequence": "use D_R to organize residuals and tests, not as a theorem.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1866_2_best_route",
            "decision": "OBJECT_LANGUAGE_RADIAL_CELL_CONSTRAINT_SELECTED_FIRST",
            "basis": "least-scrutiny route is to prove C_R/R_AB is compatibility data rather than a new propagating scalar.",
            "consequence": "try typed parent grammar before acquiring finite Z_R/J_R rows.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1866_3_fallback",
            "decision": "FINITE_ZR_JR_REQUIREMENT_LEDGER_READY",
            "basis": "if object-language proof fails, ordinary Hcore branch must be tested as finite residual physics.",
            "consequence": "source Z_R, M_R^2, J_R, B_R, Q_R, S_R, and arena projections before local claims.",
            "claim_allowed": as_bool_text(False),
            "valid_for_claim": as_bool_text(False),
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1866_0_primary",
            "target_doc": "1867-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
            "target_script": "scripts/Y5_R2FR_object_language_radial_cell_constraint_or_finite_ZRJR_intake_1867.py",
            "objective": "prove C_R/R_AB is a parent compatibility/constraint object with no independent derivative grammar; if this fails, generate finite Z_R/J_R/Q_R/S_R source-ready rows.",
            "selection_status": "selected",
            "success_condition": "typed parent object-language closes the selector without GR import, or all finite reciprocal residual coefficients/projections are explicit nonclaim rows.",
            "valid_for_claim": as_bool_text(False),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1866_1_parallel",
            "target_doc": "1867b-Y5-R2FR-reciprocal-no-charge-boundary-theorem-or-QR-source-row.md",
            "target_script": "scripts/Y5_R2FR_reciprocal_no_charge_boundary_theorem_or_QR_source_row_1867b.py",
            "objective": "try to prove Q_R=0 from boundary/source neutrality; if not, produce finite Q_R source rows.",
            "selection_status": "held_parallel",
            "success_condition": "no-charge theorem or sourced finite reciprocal-hair residual.",
            "valid_for_claim": as_bool_text(False),
        },
    ]


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_fields = {
        "valid_for_claim",
        "claim_allowed",
        "claim_ready",
        "gate_closed",
        "selector_signed",
        "proof_closed",
        "zero_claim",
        "passes_claim_gate",
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
                if str(table_row.get("valid_for_claim", "")).strip().lower() == "true":
                    return False
                if str(table_row.get("claim_allowed", "")).strip().lower() == "true":
                    return False
                if str(table_row.get("claim_ready", "")).strip().lower() == "true":
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
        shutil.copy2(output_path, RAB_QUEUE / f"JR1866_{output_path.name}")


def branch_copies_exist(paths: list[Path]) -> bool:
    for output_path in paths:
        expected_paths = [
            MICROSCOPE_RESIDUALS / output_path.name,
            QUARANTINE / output_path.name,
            RAB_QUEUE / f"JR1866_{output_path.name}",
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
    return not any(FORMALIZATION.rglob("*1866*"))


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], non_validation_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    selector_rows = rows_by_name["selector_route_audit"]
    hcore_rows = rows_by_name["hcore_source_equation_test"]
    lambdar_rows = rows_by_name["lambdar_origin_gate"]
    finite_rows = rows_by_name["finite_zrjr_requirements"]
    guard_rows = rows_by_name["no_gr_import_guard"]
    claim_rows = rows_by_name["claim_gate"]
    decision_rows = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]

    checks = [
        {
            "validation_id": "VAL1866_0_sources_exist",
            "status": "PASS" if all(row["path_exists"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source paths exist",
        },
        {
            "validation_id": "VAL1866_1_needles_present",
            "status": "PASS" if all(row["needle_found"] == "True" for row in source_rows) else "FAIL",
            "detail": "all cited source needles are present",
        },
        {
            "validation_id": "VAL1866_2_selector_not_derived",
            "status": "PASS" if any(row["actual_status"] == "RECIPROCITY_SELECTOR_NOT_DERIVED_CURRENT_CORPUS" for row in selector_rows) else "FAIL",
            "detail": "selector verdict remains nonclaim",
        },
        {
            "validation_id": "VAL1866_3_no_selector_signed",
            "status": "PASS" if all(row["selector_signed"] == "False" for row in selector_rows) else "FAIL",
            "detail": "no selector route is marked signed",
        },
        {
            "validation_id": "VAL1866_4_Hcore_finite_default",
            "status": "PASS" if any(row["status"] == "FINITE_RESIDUAL_BY_DEFAULT" for row in hcore_rows) else "FAIL",
            "detail": "ordinary Hcore branch is finite residual by default",
        },
        {
            "validation_id": "VAL1866_5_lambda_origin_blocked",
            "status": "PASS" if any(row["status"] == "LAMBDAR_PARENT_ORIGIN_NOT_DERIVED" for row in lambdar_rows) else "FAIL",
            "detail": "lambda_R origin is not promoted",
        },
        {
            "validation_id": "VAL1866_6_finite_requirements_present",
            "status": "PASS" if len(finite_rows) >= 10 and all(row["status"] == "MISSING_PARENT_INPUT" for row in finite_rows) else "FAIL",
            "detail": "finite Z_R/J_R/Q_R/S_R and arena requirements are explicit nonclaim rows",
        },
        {
            "validation_id": "VAL1866_7_no_GR_import_guard_active",
            "status": "PASS" if all(row["guard_status"] == "ACTIVE_BLOCK" for row in guard_rows) else "FAIL",
            "detail": "no-GR-import guards are active",
        },
        {
            "validation_id": "VAL1866_8_claim_gates_blocked",
            "status": "PASS" if all(row["status"] == "BLOCKED" for row in claim_rows) else "FAIL",
            "detail": "all selector/local-GR/test claim gates remain blocked",
        },
        {
            "validation_id": "VAL1866_9_no_claim_flags",
            "status": "PASS" if all_claim_flags_false(rows_by_name) else "FAIL",
            "detail": "no generated claim or gate-pass flag is true",
        },
        {
            "validation_id": "VAL1866_10_missing_not_ready",
            "status": "PASS" if missing_rows_not_ready(rows_by_name) else "FAIL",
            "detail": "no MISSING_* row is marked claim-ready",
        },
        {
            "validation_id": "VAL1866_11_decision_next",
            "status": "PASS" if any(row["decision"] == "OBJECT_LANGUAGE_RADIAL_CELL_CONSTRAINT_SELECTED_FIRST" for row in decision_rows) else "FAIL",
            "detail": "decision ledger selects object-language radial-cell constraint first",
        },
        {
            "validation_id": "VAL1866_12_next_selected",
            "status": "PASS" if any(row["route_id"] == "NEXT1866_0_primary" and row["selection_status"] == "selected" for row in next_rows) else "FAIL",
            "detail": "next target selected",
        },
        {
            "validation_id": "VAL1866_13_csv_parse",
            "status": "PASS" if csvs_parse(non_validation_paths) else "FAIL",
            "detail": "all generated non-validation CSVs parse",
        },
        {
            "validation_id": "VAL1866_14_branch_copies",
            "status": "PASS" if branch_copies_exist(non_validation_paths) else "FAIL",
            "detail": "branch/quarantine/queue copies exist",
        },
        {
            "validation_id": "VAL1866_15_pycache_absent",
            "status": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent",
        },
        {
            "validation_id": "VAL1866_16_formalization_untouched",
            "status": "PASS" if formalization_untouched() else "FAIL",
            "detail": "no 1866 outputs found under formalization-workbench",
        },
    ]
    overall_status = "PASS" if all(row["status"] == "PASS" for row in checks) else "FAIL"
    checks.append(
        {
            "validation_id": "VAL1866_OVERALL",
            "status": overall_status,
            "detail": "1866 reciprocity selector/Hcore source-equation checkpoint",
        }
    )
    return [{**row, "branch_id": BRANCH_ID, "valid_for_claim": as_bool_text(False)} for row in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 1866 - Y5/R2FR Reciprocity Selector Operator Or Hcore Source Equation",
        "",
        "## Verdict",
        "",
        "1866 goes after the missing gear from 1865: the parent reciprocity selector that would make the local Euler combination select `C_R=ln(T^2 S)` rather than an arbitrary variable mixture. The clean result is that the exact-zero branch is now very sharply fenced, but still not derived from the current corpus.",
        "",
        "The best route is the object-language route: prove that `C_R/R_AB` is not an independent scalar field at all, but a radial-cell compatibility/constraint object of the parent motion-time-space grammar. If that grammar is signed, `Z_R`, `M_R^2`, and direct `J_R` terms can be forbidden before local readout. If not, the ordinary `H_core` route gives a finite reciprocal residual branch, not exact local GR.",
        "",
        "**Claim ceiling:** no reciprocity-selector proof, no `D_R` derivation claim, no `C_R=0` theorem, no `Q_R=0` theorem, no local-GR/Newton reduction claim, no R10/PPN/clock/orbital pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1866.",
        "",
        "## Source Register",
        "",
        markdown_table(
            rows_by_name["source_register"],
            ["source_id", "source_kind", "source_path", "path_exists", "needle_found", "use_in_1866", "valid_for_claim"],
        ),
        "",
        "## Selector Route Audit",
        "",
        markdown_table(
            rows_by_name["selector_route_audit"],
            ["route_id", "candidate_selector", "best_possible_result", "actual_status", "missing_input", "decision", "selector_signed", "valid_for_claim"],
        ),
        "",
        "## Hcore Source-Equation Test",
        "",
        markdown_table(
            rows_by_name["hcore_source_equation_test"],
            ["test_id", "object", "equation_or_condition", "inference", "status", "obstruction", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Lambda_R Origin Gate",
        "",
        markdown_table(
            rows_by_name["lambdar_origin_gate"],
            ["gate_id", "object", "status", "why_not_enough", "required_to_close", "gate_closed", "valid_for_claim"],
        ),
        "",
        "## Finite Z_R/J_R Requirement Ledger",
        "",
        markdown_table(
            rows_by_name["finite_zrjr_requirements"],
            ["requirement_id", "coefficient_or_projection", "role", "why_needed", "required_source", "status", "claim_ready", "valid_for_claim"],
        ),
        "",
        "## No-GR-Import Guard",
        "",
        markdown_table(
            rows_by_name["no_gr_import_guard"],
            ["guard_id", "forbidden_shortcut", "why_forbidden", "allowed_replacement", "guard_status", "valid_for_claim"],
        ),
        "",
        "## Claim Gate",
        "",
        markdown_table(
            rows_by_name["claim_gate"],
            ["claim_id", "claim", "status", "blocking_reason", "required_before_claim", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Decision Ledger",
        "",
        markdown_table(
            rows_by_name["decision_ledger"],
            ["decision_id", "decision", "basis", "consequence", "claim_allowed", "valid_for_claim"],
        ),
        "",
        "## Next Target",
        "",
        markdown_table(
            rows_by_name["next_target"],
            ["route_id", "target_doc", "target_script", "objective", "selection_status", "success_condition", "valid_for_claim"],
        ),
        "",
        "## Validation",
        "",
        markdown_table(
            rows_by_name["validation"],
            ["validation_id", "status", "detail", "valid_for_claim"],
        ),
        "",
        "## Plain-English Status",
        "",
        "This is not a dead end; it is the theory telling us exactly where the bridge has to be built. We now know the local-GR route cannot honestly be won by waving at a plateau, at Schwarzschild coordinates, or at asymptotic flatness. The next clean swing is to prove the parent object-language: `C_R/R_AB` must be compatibility data, not a new scalar with its own kinetic/source terms. If that proof lands, local GR becomes much more derivable. If it fails, the theory still has a finite residual branch, but it must face R10/PPN/clock/orbital bounds with sourced coefficients.",
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "selector_route_audit": selector_route_audit(),
        "hcore_source_equation_test": hcore_source_equation_test(),
        "lambdar_origin_gate": lambdar_origin_gate(),
        "finite_zrjr_requirements": finite_zrjr_requirements(),
        "no_gr_import_guard": no_gr_import_guard(),
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
