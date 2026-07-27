from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from Y5_R10_alpha_product_prediction_stub_runner_and_required_inputs import (
    BOUND_REQUIRED_COLUMNS,
    PRODUCT_REQUIRED_COLUMNS,
    run_product_runner,
)


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_DIR = ROOT / "runs" / "1090-MOMS-parent-action-synthesis" / "results"
PRODUCT_RUN_DIR = RUN_DIR / "product_runner"
PREDICTION_TEMPLATE = OUT / "P8_Y5_R10_1090_WEP_PRODUCT_CANDIDATE_NONCLAIM.csv"
BOUND_IMPORT = OUT / "P8_Y5_R10_1090_WEP_BOUND_IMPORT.csv"
ETA_BOUND = 2.8e-15


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
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
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def parse_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except ValueError:
        return None


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(columns) + " |",
            "| " + " | ".join("---" for _ in columns) + " |",
            *["| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |" for row in rows],
        ]
    ) + "\n"


def count_formalization_modified_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(
        1
        for path in FORMALIZATION.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) >= STARTED
    )


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, str]]:
    specs = [
        ("SRC1090_0_1089_next", "source-intake/mts_residuals/P8_Y5_R10_1089_NEXT_TARGET.csv", "NEXT1089_0_1090", "1089 handoff."),
        ("SRC1090_1_1089_hunt", "source-intake/mts_residuals/P8_Y5_R10_1089_SIGNATURE_SOURCE_HUNT.csv", "HUNT1089_8_verdict", "source hunt verdict."),
        ("SRC1090_2_1089_coverage", "source-intake/mts_residuals/P8_Y5_R10_1089_MOMS_CLAUSE_COVERAGE_MATRIX.csv", "MOMS1088_7_all_in_one", "MOMS coverage matrix."),
        ("SRC1090_3_1088_signature", "source-intake/mts_residuals/P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv", "MOMS1088_7_verdict", "minimal signature clause."),
        ("SRC1090_4_1088_theorem", "source-intake/mts_residuals/P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv", "THM1088_5_conclusion", "conditional zero theorem."),
        ("SRC1090_5_1055_contract", "1055-Y5-R10-alpha-owner-and-matter-functor-parent-action-contract.md", "PAC1055_6_single_parent_action", "single parent action contract candidate."),
        ("SRC1090_6_990_contract", "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md", "PAC990_2_matter_functor", "GR/EM/matter coupling contract."),
        ("SRC1090_7_943_coframe", "943-Y5-R10-single-observed-coframe-matter-coupling-contract-or-frame-residual-source-pack.md", "CFC943_7_contract_verdict", "coframe/matter descent contract."),
        ("SRC1090_8_1045_functor", "1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md", "MFS1045_6_verdict", "parent matter functor audit."),
        ("SRC1090_9_1067_action_scale", "1067-Y5-R10-parent-quantum-action-scale-normalization-or-WEP-tau-projection.md", "ASO1067_5_verdict", "action-scale/species-weight audit."),
        ("SRC1090_10_1066_syntax", "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md", "SSE1066_2_variation_before_readout", "source-scalar/variation-order audit."),
        ("SRC1090_11_1079_current", "source-intake/mts_residuals/P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv", "NCO1079_6_verdict", "narrow current-owner theorem attempt."),
        ("SRC1090_12_formal_parent_v0", "../formalization-workbench/36-minimal-parent-equations-v0.md", "not action-derived", "formal parent equation scaffold."),
        ("SRC1090_13_local_bounds", "source-intake/local_bounds/local_bound_claims.csv", "R1_WEP_source_charge", "MICROSCOPE WEP bound row."),
    ]
    rows: list[dict[str, str]] = []
    for source_id, relative_path, needle, note in specs:
        path = source_path(relative_path)
        exists = path.exists()
        text = read_text(path) if exists else ""
        needle_found = exists and needle.lower() in text.lower()
        rows.append(
            {
                "source_id": source_id,
                "relative_path": relative_path,
                "absolute_path": str(path),
                "exists": str(exists).lower(),
                "needle": needle,
                "needle_found": str(needle_found).lower(),
                "note": note,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def synthesis_attempt_rows() -> list[dict[str, str]]:
    return [
        {
            "synthesis_id": "SYN1090_0_target",
            "synthesis_statement": "derive MOMS1088 from existing parent-action contracts without adding a new axiom",
            "input_sources": "PAC1055;PAC990;CFC943;MFS1045;ASO1067;SSE1066;NCO1079",
            "derivation_attempt": "compose single parent action schema, quotient coframe descent, matter bundle functor, constant-sector ownership, no source weights, no shadow frame, and variation-before-readout",
            "result": "TARGET_SHARPENED",
            "why_not_claim": "target statement is precise, but each upstream clause must be parent-derived rather than merely present",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "synthesis_id": "SYN1090_1_action_object",
            "synthesis_statement": "PAC1055_6 supplies the candidate one-action object",
            "input_sources": "1055 PAC1055_6; 990 PAC990_0",
            "derivation_attempt": "use S_parent = S_geom + S_hidden + S_EM + sum_A S_A + S_boundary as the single owner",
            "result": "SCHEMA_AVAILABLE_NOT_DERIVED",
            "why_not_claim": "1055 explicitly says schema written not derived from deeper MTS primitives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "synthesis_id": "SYN1090_2_quotient_pullback",
            "synthesis_statement": "CFC943/MFS1045 supply quotient coframe and matter pullback algebra",
            "input_sources": "943 CFC943_0-2; 1045 MFS1045_0-2",
            "derivation_attempt": "if e_obs=Obs_e(q(Phi)) and Dq(v_X)=0, chain rule gives Lie_vX e_obs=0 and visible geometry silence",
            "result": "EXACT_CONDITIONAL_LEMMA",
            "why_not_claim": "q, Obs_e, and the matter bundle functor are not parent-selected in the current action",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "synthesis_id": "SYN1090_3_matter_lift",
            "synthesis_statement": "MFS1045 supplies fixed/gauge vertical lift options",
            "input_sources": "1045 VLG1045_0-4",
            "derivation_attempt": "choose delta_v Psi_A=0 or gauge/local-Lorentz/diffeomorphism lift and push remaining terms to boundary",
            "result": "LIFT_OPTIONS_AVAILABLE_NOT_OWNED",
            "why_not_claim": "freezing the lift is a convention unless the parent matter bundle assigns it for every ordinary species and boundary class",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "synthesis_id": "SYN1090_4_constants",
            "synthesis_statement": "PAC1055/MFS1045 supply the fixed representation constant route",
            "input_sources": "1055 PAC1055_1-3; 1045 MFS1045_5",
            "derivation_attempt": "treat alpha_EM, masses, charges, clocks, and representation labels as fixed quotient/topological/superselection data",
            "result": "CONSTANT_ROUTE_AVAILABLE_UNSIGNED",
            "why_not_claim": "fixed representation data are asserted as a contract; hidden-visible coefficient functions remain legal without an operator-domain theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "synthesis_id": "SYN1090_5_no_species_weights",
            "synthesis_statement": "ASO1067/PAC1055 supply no w_A source-weight route",
            "input_sources": "1067 ASO1067_5; 1055 PAC1055_4",
            "derivation_attempt": "single hbar/action-measure/current owner plus source-label forgetting forbids w_A S_A",
            "result": "ACTION_SCALE_OWNER_UNSIGNED",
            "why_not_claim": "1067 shows relative action weights change Hilbert source and require a parent quantum/statistical measure theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "synthesis_id": "SYN1090_6_no_shadow_readout",
            "synthesis_statement": "CFC943/MFS1045/PAC1055 name no-shadow frame and readout-after-variation gates",
            "input_sources": "943 CFC943_6; 1045 MFS1045_4; 1055 CE1055_2; 1066 SSE1066_2",
            "derivation_attempt": "ban conformal/disformal/mass/domain/readout markers or retain them as explicit residuals",
            "result": "NO_SHADOW_AND_READOUT_GUARDS_UNSIGNED",
            "why_not_claim": "the corpus classifies the countermodels but does not derive an operator-domain exclusion",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "synthesis_id": "SYN1090_7_zero_theorem_if_axioms",
            "synthesis_statement": "if SYN1090_1 through SYN1090_6 were parent-signed, MOMS implies qbar_XT=0",
            "input_sources": "1088 THM1088_5_conclusion",
            "derivation_attempt": "vertical variation of S_matter hits no quotient-visible, constant, source-weight, shadow, or post-readout slot",
            "result": "CONDITIONAL_THEOREM_RECONFIRMED",
            "why_not_claim": "the missing parent signatures are exactly the theorem assumptions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "synthesis_id": "SYN1090_8_verdict",
            "synthesis_statement": "MOMS is derivable from the current corpus",
            "input_sources": "all synthesis rows",
            "derivation_attempt": "attempted composition of all available contracts into one parent-action derivation",
            "result": "SYNTHESIS_FAILS_MISSING_AXIOMS",
            "why_not_claim": "contract repetition does not derive the parent action object, matter category, constant sector, measure/current owner, or no-shadow operator domain",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dependency_rows() -> list[dict[str, str]]:
    return [
        {
            "dependency_id": "DEP1090_0_parent_primitives",
            "needed_object": "MTS primitive configuration category C_parent and action functional S_parent",
            "best_current_source": "1055 PAC1055_6; formalization-workbench 36",
            "current_status": "SCHEMA_NOT_DERIVED",
            "blocks": "all-in-one MOMS adoption",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1090_1_quotient_functor",
            "needed_object": "q_loc and Obs_e selected by parent kinematics",
            "best_current_source": "943 CFC943; 1045 MFS1045",
            "current_status": "CONDITIONAL_CHAIN_RULE_ONLY",
            "blocks": "Lie_v e_obs=0 promotion",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1090_2_matter_category",
            "needed_object": "species-complete matter bundle over observed quotient geometry",
            "best_current_source": "1045 MFS1045_2; 1055 PAC1055_2",
            "current_status": "MATTER_CATEGORY_NOT_CONSTRUCTED",
            "blocks": "ordinary matter descent theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1090_3_vertical_lift",
            "needed_object": "parent-owned vertical lift on every ordinary matter species",
            "best_current_source": "1045 VLG1045",
            "current_status": "LIFT_NOT_PARENT_SIGNED",
            "blocks": "delta_v Psi_A silence",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1090_4_constant_sector",
            "needed_object": "fixed representation/topological data for masses, charges, clocks, alpha_EM",
            "best_current_source": "1055 PAC1055_1-3; 1045 MFS1045_5",
            "current_status": "SUPERSELECTION_NOT_DERIVED",
            "blocks": "no alpha/mass/clock WEP residual",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1090_5_action_measure",
            "needed_object": "single hbar/measure/current owner forbidding w_A S_A",
            "best_current_source": "1067 ASO1067; 1055 PAC1055_4",
            "current_status": "MEASURE_OWNER_REQUIRED",
            "blocks": "no species weight theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1090_6_operator_domain",
            "needed_object": "no hidden-visible coefficient homs and no shadow/domain/readout markers",
            "best_current_source": "1055 PAC1055_3; 943 CFC943_6; 1045 MFS1045_4",
            "current_status": "OPERATOR_DOMAIN_NOT_DERIVED",
            "blocks": "no-shadow/no-marker theorem",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "dependency_id": "DEP1090_7_variation_order",
            "needed_object": "variation-before-readout rule tied to the same parent action",
            "best_current_source": "1066 SSE1066_2; 1079 current-owner stack",
            "current_status": "CONDITIONAL_RULE_NOT_PARENT_SIGNED",
            "blocks": "post-readout source selector exclusion",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def missing_axiom_rows() -> list[dict[str, str]]:
    return [
        {
            "axiom_id": "AX1090_0_parent_object",
            "axiom_if_adopted": "there exists one parent action object whose ordinary-matter domain is defined before all readout/projection/fitting choices",
            "why_needed": "separate contracts cannot derive each other without a common owner",
            "current_basis": "PAC1055/PAC990 schemas",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "could become a clean but inserted minimality principle rather than MTS derivation",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "axiom_id": "AX1090_1_no_hidden_visible_hom",
            "axiom_if_adopted": "hidden/representative variables have no allowed homomorphism into visible matter coefficients except through q_obs or fixed representation data",
            "why_needed": "kills f_X F^2, m_A(X), conformal/disformal matter frames, and material marker functions",
            "current_basis": "PAC1055_3 and no-shadow ledgers",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "too strong unless tied to a real MTS quotient/category construction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "axiom_id": "AX1090_2_common_quantum_measure",
            "axiom_if_adopted": "one hbar/action measure/current normalization applies to all ordinary matter sectors and has no species-dependent Jacobian",
            "why_needed": "forbids w_A S_A source weights that survive classical EOM rescaling",
            "current_basis": "1067 action-scale owner audit",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "imports quantum/statistical structure not yet derived from MTS primitives",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "axiom_id": "AX1090_3_fixed_constant_sector",
            "axiom_if_adopted": "ordinary masses, charges, alpha_EM, clocks, and representation labels are fixed by parent topological/representation data or retained as explicit residuals",
            "why_needed": "removes constant-sector WEP/R10/clock source currents",
            "current_basis": "1055 alpha/matter contract; 1045 constants split",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "could hide real EM/mass coupling debt unless EM owner is separately derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "axiom_id": "AX1090_4_variation_domain_order",
            "axiom_if_adopted": "all source/current variations are taken before empirical readout, material projection, source-worldtube selection, or calibration",
            "why_needed": "prevents post-variation selectors from manufacturing or erasing a local current",
            "current_basis": "1066/1079/1087 variation-order gates",
            "status": "MISSING_AXIOM_NOT_ADOPTED",
            "danger_if_adopted": "readout physics can be over-constrained if not derived with the detector/source model",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def closure_demotion_rows() -> list[dict[str, str]]:
    return [
        {
            "closure_id": "CLOS1090_0_MOMS",
            "object": "MOMS1088 ordinary-matter signature",
            "new_status": "closure_candidate_not_adopted",
            "allowed_use": "private branch organization; conditional theorem; comparison scaffold if explicitly labelled closure_assumed later",
            "forbidden_use": "derived WEP/R10/local-GR pass; theorem-zero promotion; hiding finite coefficients",
            "reopen_condition": "derive AX1090_0 through AX1090_4 from parent primitives or supply a single source signing them",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "CLOS1090_1_qbar_XT_zero",
            "object": "qbar_XT=0 local WEP/source-current branch",
            "new_status": "conditional_only",
            "allowed_use": "if MOMS is assumed, zero theorem follows by 1088",
            "forbidden_use": "claiming local WEP safety without MOMS source or finite coefficient bounds",
            "reopen_condition": "MOMS parent derivation or source-backed finite DD coefficient/product bound",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "closure_id": "CLOS1090_2_finite_DD",
            "object": "finite DD coefficient branch",
            "new_status": "phenomenological_scaffold_retained",
            "allowed_use": "screening/debugging with source-backed rows and explicit derivation_status",
            "forbidden_use": "pair cancellation, invented coefficients, measured-G absorption, unit source proxy as claim",
            "reopen_condition": "filled same-branch coefficient/range/profile/readout rows with provenance",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def prediction_rows() -> list[dict[str, str]]:
    return [
        {
            "prediction_id": "PRED1090_0_synthesis_failed_missing_axioms",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "product_value": "MISSING_MOMS_PARENT_AXIOMS_OR_FILLED_FINITE_DD_PRODUCT",
            "product_units": "dimensionless",
            "product_source": "source-intake/mts_residuals/P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
            "inputs_present": "conditional zero theorem; synthesis attempt; missing axiom ledger; MICROSCOPE bound",
            "required_inputs": "derive AX1090_0..AX1090_4 or fill finite DD product rows with provenance",
            "derivation_status": "SYNTHESIS_FAILS_MISSING_AXIOMS",
            "valid_for_claim": "false",
            "notes": "generic product runner must refuse; 1090 is a theorem/closure status checkpoint",
        }
    ]


def bound_import_rows() -> list[dict[str, str]]:
    return [
        {
            "bound_id": "BOUND1090_0_MICROSCOPE_WEP",
            "arena": "MICROSCOPE_WEP",
            "product_symbol": "P_WEP_relative_source_weight",
            "bound_value": f"{ETA_BOUND:.16e}",
            "bound_units": "dimensionless",
            "bound_source": "source-intake/local_bounds/local_bound_claims.csv",
            "source_row": "R1_WEP_source_charge",
            "bound_type": "absolute_eta_upper_bound",
            "valid_for_claim": "true",
            "notes": "source-backed comparator bound; MTS prediction row remains invalid",
        }
    ]


def product_status_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "runner_id": "APR1090_0_synthesis_missing_axioms_stub",
            "prediction_rows": str(product_status.get("prediction_rows", "")),
            "bound_rows": str(product_status.get("bound_rows", "")),
            "valid_prediction_rows": str(product_status.get("valid_prediction_rows", "")),
            "valid_bound_rows": str(product_status.get("valid_bound_rows", "")),
            "comparison_rows": str(product_status.get("comparison_rows", "")),
            "claim_allowed": str(product_status.get("claim_allowed", "")).lower(),
            "expected_result": "reject missing MOMS parent axioms and empty finite DD product",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def claim_gate_rows(product_status: dict[str, Any]) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG1090_0_synthesis",
            "claim_component": "MOMS derived from current corpus",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "SYN1090_8_verdict=SYNTHESIS_FAILS_MISSING_AXIOMS",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1090_1_missing_axioms",
            "claim_component": "missing axioms adopted",
            "gate_pass": "false",
            "claim_allowed": "false",
            "reason": "AX1090_0..AX1090_4 are explicitly not adopted",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1090_2_qbar_zero",
            "claim_component": "qbar_XT=0 local theorem",
            "gate_pass": "true",
            "claim_allowed": "false",
            "reason": "conditional theorem remains true only under unsigned MOMS assumptions",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CG1090_3_product_runner",
            "claim_component": "WEP product runner",
            "gate_pass": str(product_status.get("valid_prediction_rows") == 0).lower(),
            "claim_allowed": "false",
            "reason": f"valid_prediction_rows={product_status.get('valid_prediction_rows')}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC1090_0_synthesis_result",
            "decision": "MOMS cannot be called derived from the current corpus",
            "because": "the synthesis requires five extra principles that current files name but do not derive",
            "next_action": "either derive the missing axioms from deeper MTS primitives or keep MOMS as an explicit closure candidate",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1090_1_project_value",
            "decision": "the failure is useful rather than fatal",
            "because": "1088 still gives a real theorem target: if the ordinary-matter signature is derived, WEP/source-current zero follows cleanly",
            "next_action": "attack the smallest missing axiom instead of repeating the whole contract",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC1090_2_best_next",
            "decision": "target the no-hidden-visible-hom/operator-domain axiom first",
            "because": "it simultaneously attacks constant superselection, no-shadow frame, no direct alpha/mass vertex, and material marker leakage",
            "next_action": "construct or reject the parent operator-domain theorem from primitive MTS object language",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_id": "NEXT1090_0_1091",
            "next_target": "1091-Y5-R10-parent-operator-domain-no-hidden-visible-hom-theorem-or-MOMS-closure.md",
            "objective": "try to derive the no hidden-visible hom/operator-domain theorem that would forbid alpha_EM(X), m_A(X), shadow frames, material markers, and source-only coefficient maps; if this fails, keep MOMS as explicit closure and route local tests through finite residual coefficients",
            "include": "primitive MTS object language; hidden-visible hom ban; constant superselection; no-shadow frame; direct alpha/mass vertex exclusion; closure fallback",
            "exclude": "contract repetition as proof; invented coefficients; pair cancellation; measured-G absorption; WEP/local-GR claim; GitHub; formalization edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def csv_outputs_parse(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def validate_outputs(
    outputs: dict[str, Path],
    source_rows: list[dict[str, str]],
    synthesis_rows: list[dict[str, str]],
    dependency_rows_: list[dict[str, str]],
    axiom_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    prediction_rows_: list[dict[str, str]],
    bound_rows_: list[dict[str, str]],
    product_status: dict[str, Any],
    claim_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V1090_0_local_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in source_rows), "all cited source paths and needles are present"))
    checks.append(("V1090_1_synthesis_fails_explicitly", any(row["synthesis_id"] == "SYN1090_8_verdict" and row["result"] == "SYNTHESIS_FAILS_MISSING_AXIOMS" for row in synthesis_rows), "synthesis attempt ends in explicit missing-axiom failure"))
    checks.append(("V1090_2_dependencies_written", len(dependency_rows_) == 8 and all(row["valid_for_claim"] == "false" for row in dependency_rows_), "derivation dependency matrix is complete and nonclaim"))
    checks.append(("V1090_3_missing_axioms_not_adopted", len(axiom_rows) == 5 and all(row["status"] == "MISSING_AXIOM_NOT_ADOPTED" for row in axiom_rows), "missing axiom ledger is explicit and none are adopted"))
    checks.append(("V1090_4_closure_demotions", len(closure_rows) == 3 and all(row["valid_for_claim"] == "false" for row in closure_rows), "closure demotion register is written"))
    checks.append(("V1090_5_prediction_missing_nonclaim", any("MISSING_MOMS_PARENT_AXIOMS" in row["product_value"] and row["valid_for_claim"] == "false" for row in prediction_rows_), "prediction row remains missing MOMS parent axioms or finite product"))
    checks.append(("V1090_6_bound_numeric", bool(bound_rows_) and parse_float(bound_rows_[0]["bound_value"]) is not None and float(bound_rows_[0]["bound_value"]) > 0 and bound_rows_[0]["valid_for_claim"] == "true", "MICROSCOPE bound import is positive numeric"))
    checks.append(("V1090_7_product_runner_refuses", product_status.get("valid_prediction_rows") == 0 and product_status.get("claim_allowed") is False, "generic product runner reports no valid prediction rows and claim false"))
    checks.append(("V1090_8_claim_gates_safe", claim_rows and all(row["claim_allowed"] == "false" for row in claim_rows), "all claim gates deny WEP/local-GR claim"))
    checks.append(("V1090_9_next_target", any(row["next_target"].startswith("1091-Y5-R10-parent-operator-domain") for row in next_rows), "1091 handoff written"))
    generated_paths = list(outputs.values()) + [DOC]
    checks.append(("V1090_10_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in generated_paths), "all generated outputs are under post-checkpoint-work"))
    checks.append(("V1090_11_csv_parse", csv_outputs_parse([path for key, path in outputs.items() if key != "validation"]), "all 1090 CSV outputs parse cleanly"))
    checks.append(("V1090_12_formalization_untouched", count_formalization_modified_since_start() == 0, "formalization-workbench modified-file count remains zero"))
    checks.append(("V1090_SUMMARY", True, "MOMS synthesis fails without five missing axioms; MOMS remains conditional/closure-candidate, not derived; finite branch remains nonclaim"))
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]


def write_doc(
    source_rows: list[dict[str, str]],
    synthesis_rows: list[dict[str, str]],
    dependency_rows_: list[dict[str, str]],
    axiom_rows: list[dict[str, str]],
    closure_rows: list[dict[str, str]],
    product_status_rows_: list[dict[str, str]],
    product_comparisons: list[dict[str, Any]],
    claim_rows: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
    next_rows: list[dict[str, str]],
) -> None:
    text = "\n".join(
        [
            "# 1090-Y5-R10 MOMS parent-action synthesis or explicit missing axiom ledger",
            "",
            "## Current verdict",
            "1090 attempts the honest synthesis: combine the best existing parent-action contracts into one derivation of the MOMS1088 ordinary-matter signature. The theorem shape is strong, and the conditional zero result from 1088 survives. But the synthesis does not close from current files. Five extra principles are needed and are not adopted here: one parent ordinary-matter action object, no hidden-visible coefficient homs, one common quantum/action measure, fixed ordinary constant sector, and variation-before-readout tied to the same parent action.",
            "",
            "This is a useful narrowing, not a dead end. We now know the smallest missing load-bearing beam. The next derivation should attack the operator-domain/no-hidden-visible-hom theorem first, because it also hits constant superselection, no-shadow frame, direct alpha/mass vertices, and material marker leakage.",
            "",
            "## Source register",
            md_table(source_rows, ["source_id", "relative_path", "exists", "needle_found", "note"]),
            "## Synthesis attempt",
            md_table(synthesis_rows, ["synthesis_id", "synthesis_statement", "input_sources", "result", "why_not_claim"]),
            "## Derivation dependency matrix",
            md_table(dependency_rows_, ["dependency_id", "needed_object", "best_current_source", "current_status", "blocks"]),
            "## Missing axiom ledger",
            md_table(axiom_rows, ["axiom_id", "axiom_if_adopted", "why_needed", "current_basis", "status", "danger_if_adopted"]),
            "## Closure demotion register",
            md_table(closure_rows, ["closure_id", "object", "new_status", "allowed_use", "forbidden_use", "reopen_condition"]),
            "## Product runner status",
            md_table(product_status_rows_, ["runner_id", "valid_prediction_rows", "valid_bound_rows", "comparison_rows", "claim_allowed", "expected_result"]),
            "## Product comparison rows",
            md_table(product_comparisons, ["comparison_id", "arena", "product_symbol", "product_value", "bound_value", "comparison_status", "pass_for_claim", "issues"]),
            "## Claim gates",
            md_table(claim_rows, ["gate_id", "claim_component", "gate_pass", "claim_allowed", "reason"]),
            "## Decision ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action"]),
            "## Validation",
            md_table(validation_rows, ["check_id", "result", "detail"]),
            "## Next target",
            md_table(next_rows, ["next_id", "next_target", "objective", "include", "exclude"]),
            "",
        ]
    )
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    synthesis_rows = synthesis_attempt_rows()
    dependency_rows_ = dependency_rows()
    axiom_rows = missing_axiom_rows()
    closure_rows = closure_demotion_rows()
    prediction_rows_ = prediction_rows()
    bound_rows_ = bound_import_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R10_1090_SOURCE_REGISTER.csv",
        "synthesis": OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv",
        "dependencies": OUT / "P8_Y5_R10_1090_DERIVATION_DEPENDENCY_MATRIX.csv",
        "missing_axioms": OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv",
        "closure_demotions": OUT / "P8_Y5_R10_1090_CLOSURE_DEMOTION_REGISTER.csv",
        "prediction": PREDICTION_TEMPLATE,
        "bound": BOUND_IMPORT,
        "product_status": OUT / "P8_Y5_R10_1090_PRODUCT_RUNNER_STATUS.csv",
        "product_comparison": OUT / "P8_Y5_R10_1090_PRODUCT_COMPARISON_ROWS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1090_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1090_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1090_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1090_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows)
    write_csv(outputs["synthesis"], synthesis_rows)
    write_csv(outputs["dependencies"], dependency_rows_)
    write_csv(outputs["missing_axioms"], axiom_rows)
    write_csv(outputs["closure_demotions"], closure_rows)
    write_csv(outputs["prediction"], prediction_rows_, PRODUCT_REQUIRED_COLUMNS)
    write_csv(outputs["bound"], bound_rows_, BOUND_REQUIRED_COLUMNS)

    product_result = run_product_runner(PREDICTION_TEMPLATE, BOUND_IMPORT, PRODUCT_RUN_DIR)
    product_status = product_result["status"]
    product_status_rows_ = product_status_rows(product_status)
    product_comparisons = product_result["comparisons"]
    claim_rows = claim_gate_rows(product_status)
    decisions = decision_rows()

    write_csv(outputs["product_status"], product_status_rows_)
    write_csv(outputs["product_comparison"], product_comparisons)
    write_csv(outputs["claim_gates"], claim_rows)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_rows)

    validation_rows = validate_outputs(
        outputs,
        source_rows,
        synthesis_rows,
        dependency_rows_,
        axiom_rows,
        closure_rows,
        prediction_rows_,
        bound_rows_,
        product_status,
        claim_rows,
        next_rows,
    )
    write_csv(outputs["validation"], validation_rows)
    write_doc(
        source_rows,
        synthesis_rows,
        dependency_rows_,
        axiom_rows,
        closure_rows,
        product_status_rows_,
        product_comparisons,
        claim_rows,
        decisions,
        validation_rows,
        next_rows,
    )
    remove_pycache()

    failed = [row for row in validation_rows if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
