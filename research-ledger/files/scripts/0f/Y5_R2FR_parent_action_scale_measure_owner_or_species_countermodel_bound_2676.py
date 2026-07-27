from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2676"
BRANCH_ID = "Y5_R2FR_PARENT_ACTION_SCALE_MEASURE_OWNER_OR_SPECIES_COUNTERMODEL_BOUND_2676"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
WEP_COEFF = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "2676-Y5-R2FR-parent-action-scale-measure-owner-or-species-countermodel-bound.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2676_SOURCE_REGISTER.csv",
    "proof_audit": RESIDUALS / "P8_Y5_R2FR_2676_ACTION_SCALE_MEASURE_OWNER_PROOF_AUDIT.csv",
    "lemma_ledger": RESIDUALS / "P8_Y5_R2FR_2676_EXACT_CONDITIONAL_LEMMA_LEDGER.csv",
    "countermodel_rows": RESIDUALS / "P8_Y5_R2FR_2676_SPECIES_COUNTERMODEL_BOUND_ROWS_NONCLAIM.csv",
    "runner_results": RESIDUALS / "P8_Y5_R2FR_2676_OWNER_RUNNER_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2676_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2676_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2676_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2676_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2676_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "microscope_countermodels": WEP_COEFF / "action_scale_measure_owner_countermodels_nonclaim_2676.csv",
    "source_weight": SOURCE_INTAKE / "source-weight" / "ACTION_SCALE_MEASURE_OWNER_COUNTERMODELS_2676_NONCLAIM.csv",
    "local_bounds": SOURCE_INTAKE / "local_bounds" / "Action_scale_measure_owner_countermodels_2676_NONCLAIM.csv",
    "wep_sources": SOURCE_INTAKE / "wep-sources" / "action_scale_measure_owner_wip_nonclaim_2676.csv",
    "microscope_lemmas": WEP_COEFF / "action_scale_measure_owner_exact_lemmas_conditional_2676.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2676_2675_AUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2675_SPECIES_CLOCK_ZERO_PROOF_AUDIT.csv",
        "required_needles": ["Z2675_0_species_conditional_theorem", "Z2675_4_verdict", "SPECIES_CLOCK_ZERO_NOT_PARENT_DERIVED"],
        "purpose": "inherits 2675 species/clock zero theorem status",
    },
    {
        "source_id": "SRC2676_2675_SPECIES_ROW",
        "relative_path": "source-intake/mts_residuals/P8_species_source_charge_residual_or_zero.csv",
        "required_needles": ["SSC2675_0_definition", "SSC2675_3_no_bound_inversion_guard", "BOUND_INVERSION_FORBIDDEN"],
        "purpose": "uses repaired nonclaim species residual row and no-bound-inversion guard",
    },
    {
        "source_id": "SRC2676_2675_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2675_NEXT_TARGET.csv",
        "required_needles": ["NEXT2675_0_selected", "parent action scale/measure", "species countermodels"],
        "purpose": "confirms 2676 target selection",
    },
    {
        "source_id": "SRC2676_COMMON_MEASURE_ATTEMPT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv",
        "required_needles": ["CMT1452_0_target", "CMT1452_1_classical_EOM_limit", "CMT1452_3_species_jacobian_countermodel", "CMT1452_6_verdict"],
        "purpose": "main source for action-scale/measure theorem and countermodels",
    },
    {
        "source_id": "SRC2676_COMMON_MEASURE_SIGNING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_common_measure_signing_decision_1452.csv",
        "required_needles": ["SIGN1452_0_common_measure", "REFUSE_COMMON_MEASURE_ZERO_IMPORT_KEEP_JA_LEDGER", "conditional route is clean"],
        "purpose": "records refusal to import common-measure zero",
    },
    {
        "source_id": "SRC2676_CURRENT_OWNER_ATTEMPT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv",
        "required_needles": ["CSO1453_1_hilbert_variation", "CSO1453_4_post_variation_rescaling", "CSO1453_5_pre_variation_weight", "CSO1453_6_nonhilbert_bypass", "CSO1453_7_verdict"],
        "purpose": "separates exact Hilbert/current sublemmas from surviving loopholes",
    },
    {
        "source_id": "SRC2676_CURRENT_OWNER_SIGNING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_current_owner_signing_decision_1453.csv",
        "required_needles": ["SIGN1453_0_current_owner", "REFUSE_CURRENT_OWNER_ZERO_IMPORT_KEEP_CA_ZETA_LEDGER", "pre-action weights"],
        "purpose": "records refusal to import current-owner zero",
    },
    {
        "source_id": "SRC2676_MINIMAL_PARENT_CLAUSE",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_minimal_parent_clause.csv",
        "required_needles": ["MPC1439_0_clause", "MPC1439_1_formal_zero", "MPC1439_3_strength_warning", "MPC1439_4_verdict"],
        "purpose": "states the exact sufficient local WEP parent clause",
    },
    {
        "source_id": "SRC2676_COUPLING_DERIVATION",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_coupling_derivation_attempt_nonclaim_1484.csv",
        "required_needles": ["CPD1484_1_functional_derivative", "CPD1484_2_double_zero_route", "CPD1484_3_finite_route", "CPD1484_5_verdict"],
        "purpose": "keeps finite C_parent route source-backed and nonclaim",
    },
    {
        "source_id": "SRC2676_FINITE_CX_CONTRACT",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_finite_CX_contract_1911_nonclaim.csv",
        "required_needles": ["CX1911_electron", "CX1911_EM", "CX1911_nonHilbert", "MISSING_PARENT_COEFFICIENT"],
        "purpose": "provides component-wise finite coefficient contract and forbidden bound inversion forms",
    },
    {
        "source_id": "SRC2676_NO_SOURCE_SLOT_SIGNING",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_no_source_slot_signing_decision_1451.csv",
        "required_needles": ["SIGN1451_0_no_slot", "REFUSE_ZERO_IMPORT_KEEP_BOUND_INPUTS", "operator grammar theorem"],
        "purpose": "records unsigned no-source-only-slot grammar theorem",
    },
    {
        "source_id": "SRC2676_SOURCE_FACTORIZATION",
        "relative_path": "source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv",
        "required_needles": ["SIGN1461_0_source_factorization", "REFUSE_DELTA_Q_ZERO_IMPORT_WRITE_CMSM_SCAFFOLD", "surviving countermodels"],
        "purpose": "records unsigned source-label forgetting/factorization theorem",
    },
    {
        "source_id": "SRC2676_NO_SPECIES_CONTRACT",
        "relative_path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
        "required_needles": ["S1_matter_factorization", "S4_source_normalization_species_blind", "S5_no_bulk_boundary_composition_charge", "S7_R1_empirical_fallback"],
        "purpose": "connects action-scale owner to bulk/boundary/domain composition charge clauses",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = []
        for header in headers:
            value = str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def proof_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "OWN2676_0_parent_owner_target",
            "claim_piece": "one parent action-scale/measure/current owner",
            "candidate_statement": "There exists one ordinary-matter parent sector S_matter = A_parent integral dmu_parent sum_A L_A(Psi_A,e_obs,omega[e_obs],theta_univ), with no hbar_A, w_A, J_A, c_A, zeta_A or source-only species slot.",
            "derived_if_signed": "species/source marker variations in ker(Dq_obs) cannot alter source normalization; epsilon_species_A=0 and C_parent_WEP=0",
            "current_status": "TARGET_SHARPENED_NOT_PARENT_SIGNED",
            "blocking_clauses": "parent action scale hbar_parent not signed; measure owner not signed; current owner conditional; non-Hilbert bypass open",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_minimal_parent_clause.csv")),
                ]
            ),
            "proof_status": "conditional_only",
            "theorem_zero": "false",
            "countermodel_bound_required": "true",
            "valid_for_claim": "false",
            "next_action": "write parent object-language no-species-weight theorem or retain explicit countermodel rows",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OWN2676_1_common_measure_route",
            "claim_piece": "single parent measure/action scale removes relative species weights",
            "candidate_statement": "A unique parent action scale/path measure forbids independent exp(i w_A S_A/hbar_parent), hbar_A, and species Jacobian factors.",
            "derived_if_signed": "relative action weights and measure Jacobians are illegal, not just bounded",
            "current_status": "CONDITIONAL_ROUTE_CLEAN_COUNTERMODELS_SURVIVE",
            "blocking_clauses": "species Jacobian and relative action-weight countermodels remain legal in current corpus",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
            "proof_status": "countermodel_survives",
            "theorem_zero": "false",
            "countermodel_bound_required": "true",
            "valid_for_claim": "false",
            "next_action": "target w_A/J_A object-language exclusion next",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OWN2676_2_hilbert_current_sublemma",
            "claim_piece": "Hilbert source tensor uniqueness",
            "candidate_statement": "For a fixed common S_matter varied with respect to e_obs/g_obs before readout, T_H is unique and obeys the diffeomorphism Ward identity on matter shell.",
            "derived_if_signed": "post-variation source rescaling cannot redefine the parent source; it becomes readout/calibration bookkeeping",
            "current_status": "EXACT_SUBTHEOREM_CONDITIONAL",
            "blocking_clauses": "common S_matter and variation-before-readout order are not parent-signed; pre-action weights still enter T_H",
            "source_paths": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
            "proof_status": "exact_conditional_sublemma",
            "theorem_zero": "false",
            "countermodel_bound_required": "true",
            "valid_for_claim": "false",
            "next_action": "use this as a lemma, not as a full WEP proof",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OWN2676_3_no_source_slot_route",
            "claim_piece": "no source-only species slot",
            "candidate_statement": "The parent object language has no independent source-only species label or spurion that can re-enter after quotienting.",
            "derived_if_signed": "epsilon_A=0 can be imported from grammar rather than fit to WEP",
            "current_status": "GRAMMAR_THEOREM_RIGHT_SHAPE_UNSIGNED",
            "blocking_clauses": "no-hidden-visible-hom, label forgetting, common measure/current and no-spurion-return are unsigned",
            "source_paths": ";".join(
                [
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_no_source_slot_signing_decision_1451.csv")),
                    str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_source_factorization_signing_decision_1461.csv")),
                ]
            ),
            "proof_status": "unsigned_grammar_route",
            "theorem_zero": "false",
            "countermodel_bound_required": "true",
            "valid_for_claim": "false",
            "next_action": "make the no-species-slot theorem syntactic and check countermodels against it",
            "timestamp_utc": stamp(),
        },
        {
            "audit_id": "OWN2676_4_verdict",
            "claim_piece": "parent owner closes species countermodels",
            "candidate_statement": "parent action-scale/measure/current owner proves epsilon_species_A=0 and C_parent_WEP=0",
            "derived_if_signed": "species channel exits the qbar_XT debt ledger and helps local-GR/PPN re-entry",
            "current_status": "PARENT_OWNER_NOT_DERIVED_COUNTERMODELS_RETAINED",
            "blocking_clauses": "w_A action weights; J_A measure Jacobians; c_A pre-variation source rescaling; zeta_A non-Hilbert current; boundary/domain composition labels",
            "source_paths": str(path_for("source-intake/mts_residuals/P8_species_source_charge_residual_or_zero.csv")),
            "proof_status": "not_closed",
            "theorem_zero": "false",
            "countermodel_bound_required": "true",
            "valid_for_claim": "false",
            "next_action": "convert each surviving countermodel into a finite nonclaim bound row",
            "timestamp_utc": stamp(),
        },
    ]


def lemma_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "LEM2676_0_variation_before_readout",
            "lemma": "If the same S_matter is fixed before readout, then the Hilbert source T_H := 2/sqrt(-g) delta S_matter/delta g is the parent source owner.",
            "status": "EXACT_CONDITIONAL",
            "what_it_kills": "post-variation c_A rescalings as source redefinitions",
            "what_survives": "pre-action weights w_A and measure Jacobians J_A",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "lemma_id": "LEM2676_1_classical_eom_not_enough",
            "lemma": "Matching matter equations of motion does not prove source equivalence because delta(w_A S_A)/delta g = w_A T_A.",
            "status": "REJECTION_LEMMA",
            "what_it_kills": "fake proof that source normalization follows from classical equations alone",
            "what_survives": "species action weights and measure/current countermodels",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "lemma_id": "LEM2676_2_minimal_parent_clause",
            "lemma": "If ordinary matter descends through one observed coframe with no independent species/source/boundary/readout functional, then the WEP functional derivative vanishes.",
            "status": "FORMAL_ZERO_CONDITIONAL",
            "what_it_kills": "C_parent_WEP once every clause is parent-signed",
            "what_survives": "all unsigned clause countermodels",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_minimal_parent_clause.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "lemma_id": "LEM2676_3_bound_inversion_forbidden",
            "lemma": "MICROSCOPE/WEP bounds can test a coefficient but cannot define the parent coefficient.",
            "status": "GUARDRAIL",
            "what_it_kills": "using empirical bound as a theory value",
            "what_survives": "finite parent coefficients only if sourced independently or theorem-zero",
            "source_path": str(path_for("source-intake/mts_residuals/P8_species_source_charge_residual_or_zero.csv")),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    common = "2.8e-15"
    return [
        {
            "countermodel_id": "CM2676_0_species_action_weight",
            "symbol": "w_A",
            "countermodel": "S_matter contains sum_A w_A S_A before variation",
            "leak_formula": "Delta_epsilon_AB includes Delta w_AB in the Hilbert source normalization",
            "required_zero_theorem": "parent action scale forbids independent species action weights/hbar_A",
            "bound_or_scale": common,
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
            "status": "COUNTERMODEL_RETAINED_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove w_A cannot appear in parent object language or fill Delta w_AB with source-independent units",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2676_1_species_measure_jacobian",
            "symbol": "J_A",
            "countermodel": "Dmu_parent or effective source measure contains species Jacobian factors J_A",
            "leak_formula": "Delta_epsilon_AB includes Delta ln J_AB or induced source-measure weight",
            "required_zero_theorem": "single parent measure/path-integral owner forbids species Jacobians",
            "bound_or_scale": common,
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/common_measure_current_theorem_attempt_1452.csv")),
            "status": "COUNTERMODEL_RETAINED_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive species-blind measure owner or fill J_A residual row",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2676_2_pre_variation_source_rescaling",
            "symbol": "c_A",
            "countermodel": "source current normalization c_A is inserted before Hilbert/source variation",
            "leak_formula": "J_src = sum_A c_A T_A, so Delta_epsilon_AB includes Delta c_AB",
            "required_zero_theorem": "source current is fixed by parent variation before material/readout selectors",
            "bound_or_scale": common,
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
            "status": "COUNTERMODEL_RETAINED_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "prove variation-before-readout plus no pre-action weights or fill c_A bound row",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2676_3_nonHilbert_current_bypass",
            "symbol": "zeta_A",
            "countermodel": "non-Hilbert or shadow current contributes J_src = kappa T_H + sum_A zeta_A J_NH,A",
            "leak_formula": "Delta_epsilon_AB includes projected Delta(zeta_A J_NH,A)/T_H",
            "required_zero_theorem": "non-Hilbert currents are absent, exact, or projected silent in the local branch",
            "bound_or_scale": common,
            "units": "current-normalized dimensionless projection",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/current_source_normalization_owner_theorem_attempt_1453.csv")),
            "status": "COUNTERMODEL_RETAINED_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive no non-Hilbert bypass or fill zeta_A projection with units",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2676_4_boundary_domain_composition_charge",
            "symbol": "q_BA;q_DA;q_XA",
            "countermodel": "bulk, boundary, class, or domain sectors carry composition charge",
            "leak_formula": "Delta_epsilon_AB includes q_XA-q_XB plus boundary/domain source-measure terms",
            "required_zero_theorem": "bulk/boundary/domain sectors carry no composition charge and no source-only label",
            "bound_or_scale": common,
            "units": "dimensionless after source normalization",
            "source_path": str(path_for("source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv")),
            "status": "COUNTERMODEL_RETAINED_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive boundary/domain no-composition theorem or add separate rows",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2676_5_parent_coefficient_components",
            "symbol": "C_e;C_q;C_alpha;C_bind;C_QCD;C_lat;C_shadow",
            "countermodel": "finite parent WEP component coefficients exist but are not derived, zero-certified, or source-backed",
            "leak_formula": "Delta_epsilon_TiPt = sum_i DeltaQ_i(TiPt) C_i + direct shadow/source terms",
            "required_zero_theorem": "each C_i is DERIVED_ZERO from parent proof or has an independent finite source",
            "bound_or_scale": common,
            "units": "declared parent WEP basis",
            "source_path": str(path_for("source-intake/microscope/branch_locked_wep/coefficients/C_parent_WEP_finite_CX_contract_1911_nonclaim.csv")),
            "status": "COMPONENT_CONTRACT_UNFILLED_NONCLAIM",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "derive component zeros or source finite C_i values independent of WEP bound",
            "timestamp_utc": stamp(),
        },
        {
            "countermodel_id": "CM2676_6_absolute_no_cancellation_envelope",
            "symbol": "epsilon_species_abs",
            "countermodel": "multiple species/source countermodels cancel accidentally",
            "leak_formula": "abs(epsilon_species_total) >= abs(w)+abs(J)+abs(c)+abs(zeta)+abs(boundary/domain)+abs(C_i)",
            "required_zero_theorem": "each component individually zero, or each absolute component numerically bounded",
            "bound_or_scale": common,
            "units": "dimensionless",
            "source_path": str(path_for("source-intake/mts_residuals/P8_species_source_charge_residual_or_zero.csv")),
            "status": "NO_CANCELLATION_ENVELOPE_NOT_COMPUTED",
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "next_action": "do not score species channel until component absolute envelope exists",
            "timestamp_utc": stamp(),
        },
    ]


def runner_results_rows(proof_rows: list[dict[str, Any]], counter_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in proof_rows:
        rows.append(
            {
                "runner_id": f"RUN2676_{row['audit_id']}",
                "target_id": row["audit_id"],
                "stage": "owner_proof_audit",
                "has_parent_zero": row["theorem_zero"],
                "has_numeric_counter_bound": "false",
                "has_existing_source_path": as_bool(all(Path(p).exists() for p in row["source_paths"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_PARENT_OWNER_UNSIGNED",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    for row in counter_rows:
        rows.append(
            {
                "runner_id": f"RUN2676_{row['countermodel_id']}",
                "target_id": row["countermodel_id"],
                "stage": "countermodel_bound_row",
                "has_parent_zero": "false",
                "has_numeric_counter_bound": "false",
                "has_existing_source_path": as_bool(all(Path(p).exists() for p in row["source_path"].split(";"))),
                "scored": "false",
                "claim_pass": "false",
                "valid_for_claim": "false",
                "refusal_code": "REFUSED_COUNTERMODEL_ROW_NONCLAIM",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2676_0_parent_owner_zero",
            "claim": "parent action-scale/measure/current owner is derived",
            "status": "FAIL_PARENT_OWNER_NOT_SIGNED",
            "blocking_rows": "OWN2676_0_parent_owner_target;OWN2676_1_common_measure_route;OWN2676_4_verdict",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2676_1_countermodel_bounds",
            "claim": "species countermodels are source-bounded",
            "status": "FAIL_COUNTERMODEL_ROWS_NONCLAIM",
            "blocking_rows": "CM2676_0_species_action_weight;CM2676_1_species_measure_jacobian;CM2676_2_pre_variation_source_rescaling;CM2676_3_nonHilbert_current_bypass;CM2676_6_absolute_no_cancellation_envelope",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2676_2_species_zero",
            "claim": "epsilon_species_A=0 is now derived",
            "status": "FAIL_OWNER_AND_COUNTERMODEL_GATES",
            "blocking_rows": "CG2676_0_parent_owner_zero;CG2676_1_countermodel_bounds",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2676_3_no_bound_inversion",
            "claim": "finite C_parent rows are not imported from MICROSCOPE bounds",
            "status": "PASS_GUARDRAIL",
            "blocking_rows": "none",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "gate_id": "CG2676_4_local_GR",
            "claim": "local GR/PPN recovery can use species channel silence",
            "status": "CLAIM_BLOCKED",
            "blocking_rows": "OWN2676_4_verdict;CG2676_0_parent_owner_zero;CG2676_1_countermodel_bounds",
            "is_evidence": "false",
            "keep_private": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2676_0_theorem_attempt",
            "question": "Can 2676 prove the parent action-scale/measure owner?",
            "result": "not_from_current_corpus",
            "reason": "Hilbert/Ward and post-variation rescaling lemmas are clean conditional pieces, but pre-action weights, species Jacobians and non-Hilbert currents survive",
            "action": "do not import epsilon_A=0",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2676_1_countermodel_route",
            "question": "Did 2676 still improve the framework?",
            "result": "yes_countermodels_named",
            "reason": "the old vague parent-owner gap is now an explicit list of w_A, J_A, c_A, zeta_A, q_boundary/domain and C_i rows",
            "action": "countermodel bound rows written as nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2676_2_next_route",
            "question": "What should be attacked next?",
            "result": "no_species_action_weight_object_language",
            "reason": "w_A/J_A are the most fundamental surviving countermodels; killing them makes current-owner lemmas much more useful",
            "action": "select 2677 no-species-action-weight object-language or w_A/J_A bound",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2676_0_selected",
            "kind": "selected",
            "target_doc": "2677-Y5-R2FR-no-species-action-weight-object-language-or-wA-JA-bound.md",
            "target_script": "scripts/Y5_R2FR_no_species_action_weight_object_language_or_wA_JA_bound_2677.py",
            "purpose": "try to prove the parent object language forbids w_A, hbar_A and J_A species action/measure weights, or keep them as explicit nonclaim bound rows",
            "acceptance_gate": "syntactic parent-action rule excluding species action weights/Jacobians plus source-label forgetting, or finite w_A/J_A rows with units, source path and no-cancellation envelope",
            "forbidden_shortcuts": "assuming EEP/WEP as axiom; using classical EOM alone; importing epsilon_A=0; using empirical bound as coefficient; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PS2676_0_scope",
            "field": "workspace_scope",
            "value": str(ROOT),
            "status": "private_post_checkpoint_only",
            "note": "no GitHub action and no formalization-workbench writes",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2676_1_progress",
            "field": "species_source_gap",
            "value": "parent owner theorem not closed but countermodels are now explicit",
            "status": "improved_not_claimed",
            "note": "we gained exact bottleneck names: w_A/J_A/c_A/zeta_A/q_boundary/C_i",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "status_id": "PS2676_2_next",
            "field": "next_derivation",
            "value": "no_species_action_weight_object_language",
            "status": "selected",
            "note": "this is the most root-cause route to derive WEP/source silence rather than fit it",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2676_0_microscope_countermodels",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["countermodel_rows"]),
            "destination": str(BRANCH_OUTPUTS["microscope_countermodels"]),
            "contents": "species countermodel bound rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2676_1_source_weight",
            "branch": "source-weight",
            "source_table": rel_path(OUTPUTS["countermodel_rows"]),
            "destination": str(BRANCH_OUTPUTS["source_weight"]),
            "contents": "source-weight countermodel rows retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2676_2_local_bounds",
            "branch": "local_bounds",
            "source_table": rel_path(OUTPUTS["countermodel_rows"]),
            "destination": str(BRANCH_OUTPUTS["local_bounds"]),
            "contents": "local bound rows for owner countermodels retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2676_3_wep_sources",
            "branch": "wep-sources",
            "source_table": rel_path(OUTPUTS["proof_audit"]),
            "destination": str(BRANCH_OUTPUTS["wep_sources"]),
            "contents": "parent owner WEP proof status retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2676_4_microscope_lemmas",
            "branch": "microscope/branch_locked_wep/coefficients",
            "source_table": rel_path(OUTPUTS["lemma_ledger"]),
            "destination": str(BRANCH_OUTPUTS["microscope_lemmas"]),
            "contents": "exact conditional lemmas retained nonclaim",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    source_ok = all(row["exists"] == "true" and row["missing_needles"] == "" for row in rows["source_register"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_sources_exist_and_needles_found",
            "passed": as_bool(source_ok),
            "details": "all cited source paths exist and required needles are present",
        }
    )

    all_nonclaim = all(row.get("valid_for_claim") == "false" for table in rows.values() for row in table)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_nonclaim_guard",
            "passed": as_bool(all_nonclaim),
            "details": "all generated rows carry valid_for_claim=false",
        }
    )

    owner_blocked = any(
        row["audit_id"] == "OWN2676_4_verdict"
        and row["current_status"] == "PARENT_OWNER_NOT_DERIVED_COUNTERMODELS_RETAINED"
        for row in rows["proof_audit"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_owner_verdict_blocks_claim",
            "passed": as_bool(owner_blocked),
            "details": "parent owner theorem is not promoted",
        }
    )

    lemmas_ok = (
        any(row["lemma_id"] == "LEM2676_0_variation_before_readout" and row["status"] == "EXACT_CONDITIONAL" for row in rows["lemma_ledger"])
        and any(row["lemma_id"] == "LEM2676_1_classical_eom_not_enough" and row["status"] == "REJECTION_LEMMA" for row in rows["lemma_ledger"])
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_exact_lemmas_and_rejections_recorded",
            "passed": as_bool(lemmas_ok),
            "details": "exact conditional Hilbert lemma and classical-EOM rejection lemma are both recorded",
        }
    )

    required_countermodels = {
        "CM2676_0_species_action_weight",
        "CM2676_1_species_measure_jacobian",
        "CM2676_2_pre_variation_source_rescaling",
        "CM2676_3_nonHilbert_current_bypass",
        "CM2676_4_boundary_domain_composition_charge",
        "CM2676_5_parent_coefficient_components",
        "CM2676_6_absolute_no_cancellation_envelope",
    }
    counter_ok = required_countermodels.issubset({row["countermodel_id"] for row in rows["countermodel_rows"]}) and all(
        row["score_ready"] == "false" and row["valid_for_claim"] == "false" for row in rows["countermodel_rows"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_countermodel_rows_complete_nonclaim",
            "passed": as_bool(counter_ok),
            "details": "w_A, J_A, c_A, zeta_A, boundary/domain, C_i and no-cancellation rows are present and nonclaim",
        }
    )

    runner_refuses = all(row["scored"] == "false" and row["claim_pass"] == "false" for row in rows["runner_results"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_runner_refuses_unsigned_rows",
            "passed": as_bool(runner_refuses),
            "details": "runner refuses scoring without parent owner zero or numeric countermodel bounds",
        }
    )

    gates_blocked = any(row["gate_id"] == "CG2676_4_local_GR" and row["status"] == "CLAIM_BLOCKED" for row in rows["claim_gates"])
    guard_pass = any(row["gate_id"] == "CG2676_3_no_bound_inversion" and row["status"] == "PASS_GUARDRAIL" for row in rows["claim_gates"])
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_claim_gates_correct",
            "passed": as_bool(gates_blocked and guard_pass),
            "details": "local-GR stays blocked while no-bound-inversion guard passes",
        }
    )

    next_selected = any(
        row["target_id"] == "NEXT2676_0_selected"
        and "2677-Y5-R2FR-no-species-action-weight-object-language-or-wA-JA-bound.md" in row["target_doc"]
        for row in rows["next_target"]
    )
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_next_target_selected",
            "passed": as_bool(next_selected),
            "details": "next target selects no-species-action-weight object language",
        }
    )

    parse_results = [parse_csv(path) for path in csv_paths]
    csv_ok = all(result[0] and result[1] > 0 for result in parse_results)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_csv_parse",
            "passed": as_bool(csv_ok),
            "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(csv_paths, parse_results)),
        }
    )

    branch_paths = [Path(row["destination"]) for row in rows["branch_copies"]]
    branch_parse = [parse_csv(path) for path in branch_paths]
    branch_ok = all(result[0] and result[1] > 0 for result in branch_parse)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_branch_copies_parse",
            "passed": as_bool(branch_ok),
            "details": "; ".join(f"{path.name}:{result[2]}:{result[1]}" for path, result in zip(branch_paths, branch_parse)),
        }
    )

    generated_paths = [*csv_paths, *branch_paths, DOC_PATH]
    formalization_guard = all("formalization-workbench" not in str(path) for path in generated_paths)
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_formalization_write_guard",
            "passed": as_bool(formalization_guard),
            "details": "generated path allowlist excludes formalization-workbench",
        }
    )

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_pycache_absent_at_validation_time",
            "passed": as_bool(pycache_absent),
            "details": "scripts/__pycache__ absent when validation rows were produced",
        }
    )

    overall = all(row["passed"] == "true" for row in out if row["validation_id"] != "VAL2676_pycache_absent_at_validation_time")
    out.append(
        {
            "timestamp_utc": stamp(),
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "validation_id": "VAL2676_OVERALL",
            "passed": as_bool(overall),
            "details": "2676 keeps parent-owner theorem conditional, records exact lemmas, retains species countermodel rows, and selects w_A/J_A object-language target",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        f"# {CHECKPOINT} — Parent Action-Scale/Measure Owner Or Species Countermodel Bound",
        "",
        "## Private Verdict",
        "",
        "This checkpoint took the hard route: try to make the species/source WEP silence derivable from one parent action scale, one measure, and one current owner. The exact conditional lemmas are real and useful: fixed Hilbert variation owns the source, and classical equations of motion alone do **not** prove source equivalence. But the current corpus still permits pre-action species weights, measure Jacobians, pre-variation source rescalings, non-Hilbert currents, and boundary/domain composition labels.",
        "",
        "So 2676 does **not** claim local GR, WEP, or species-source silence. It tightens the bottleneck: the next leap is an object-language theorem forbidding `w_A`, `hbar_A`, and `J_A`, or those countermodels must become explicit finite nonclaim rows.",
        "",
        "## Source Register",
        "",
        markdown_table(rows["source_register"]),
        "",
        "## Owner Proof Audit",
        "",
        markdown_table(rows["proof_audit"]),
        "",
        "## Exact Conditional Lemmas",
        "",
        markdown_table(rows["lemma_ledger"]),
        "",
        "## Species Countermodel Bound Rows",
        "",
        markdown_table(rows["countermodel_rows"]),
        "",
        "## Runner Results",
        "",
        markdown_table(rows["runner_results"]),
        "",
        "## Claim Gates",
        "",
        markdown_table(rows["claim_gates"]),
        "",
        "## Decision Ledger",
        "",
        markdown_table(rows["decision_ledger"]),
        "",
        "## Next Target",
        "",
        markdown_table(rows["next_target"]),
        "",
        "## Project Status",
        "",
        markdown_table(rows["project_status"]),
        "",
        "## Branch Copies",
        "",
        markdown_table(rows["branch_copies"]),
        "",
        "## Validation",
        "",
        markdown_table(rows["validation"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in [*OUTPUTS.values(), *BRANCH_OUTPUTS.values(), DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)

    rows: dict[str, list[dict[str, Any]]] = {}
    rows["source_register"] = source_register_rows()
    rows["proof_audit"] = proof_audit_rows()
    rows["lemma_ledger"] = lemma_ledger_rows()
    rows["countermodel_rows"] = countermodel_rows()
    rows["runner_results"] = runner_results_rows(rows["proof_audit"], rows["countermodel_rows"])
    rows["claim_gates"] = claim_gate_rows()
    rows["decision_ledger"] = decision_rows()
    rows["next_target"] = next_target_rows()
    rows["project_status"] = project_status_rows()
    rows["branch_copies"] = branch_copy_rows()

    for name in [
        "source_register",
        "proof_audit",
        "lemma_ledger",
        "countermodel_rows",
        "runner_results",
        "claim_gates",
        "decision_ledger",
        "next_target",
        "project_status",
        "branch_copies",
    ]:
        write_csv(OUTPUTS[name], rows[name])

    write_csv(BRANCH_OUTPUTS["microscope_countermodels"], rows["countermodel_rows"])
    write_csv(BRANCH_OUTPUTS["source_weight"], rows["countermodel_rows"])
    write_csv(BRANCH_OUTPUTS["local_bounds"], rows["countermodel_rows"])
    write_csv(BRANCH_OUTPUTS["wep_sources"], rows["proof_audit"])
    write_csv(BRANCH_OUTPUTS["microscope_lemmas"], rows["lemma_ledger"])

    csv_paths = [OUTPUTS[name] for name in OUTPUTS if name != "validation"]
    rows["validation"] = validation_rows(rows, csv_paths)
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
