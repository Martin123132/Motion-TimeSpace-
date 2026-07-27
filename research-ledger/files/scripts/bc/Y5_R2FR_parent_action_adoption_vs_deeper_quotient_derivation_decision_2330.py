from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_ACTION_ADOPTION_VS_DEEPER_QUOTIENT_DERIVATION_2330"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2330-Y5-R2FR-parent-action-adoption-vs-deeper-quotient-derivation-decision.md"

PATHS = {
    "2329_doc": ROOT / "2329-Y5-R2FR-parent-action-source-blind-functor-signature.md",
    "2329_validation": OUT / "P8_Y5_BRR545_2329_VALIDATION.csv",
    "2329_signature": OUT / "P8_Y5_PARENT_QLOC_2329_SOURCE_BLIND_FUNCTOR_SIGNATURE.csv",
    "2329_proof": OUT / "P8_Y5_PARENT_QLOC_2329_NOSOURCE_SLOT_THEOREM_PROOF.csv",
    "2329_activation": OUT / "P8_Y5_PARENT_QLOC_2329_PARENT_SIGNATURE_ACTIVATION_MATRIX.csv",
    "2329_counter": OUT / "P8_Y5_PARENT_QLOC_2329_COUNTERMODEL_CLOSURE_MATRIX.csv",
    "943_coframe": OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
    "944_descent": OUT / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv",
    "954_clause": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
    "955_lemma": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "1079_theorem": OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
    "1332_common": OUT / "P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv",
    "1333_attempt": OUT / "P8_Y5_R10_1333_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv",
    "1337_contract": OUT / "P8_Y5_R10_1337_MINIMAL_PARENT_ACTION_CONTRACT.csv",
    "1337_theorem": OUT / "P8_Y5_R10_1337_COMMON_MODE_THEOREM_UPDATE.csv",
    "1337_decision": OUT / "P8_Y5_R10_1337_DECISION_LEDGER.csv",
    "1337_gate": OUT / "P8_Y5_R10_1337_LOCAL_GR_IMPLICATION_GATE.csv",
    "2125_common": OUT / "P8_Y5_PARENT_QLOC_2125_COMMON_MODE_DESCENT_AUDIT.csv",
    "2327_bound": OUT / "P8_Y5_PARENT_QLOC_2327_LSOURCEGM_BOUND_ROW.csv",
    "2328_profile": OUT / "P8_Y5_PARENT_QLOC_2328_SOURCE_PROFILE_VECTOR_FIRST_ROW.csv",
}

SOURCES = [
    ("SRC2330_00_2329_doc", "2329_doc", PATHS["2329_doc"], ["NEXT2329_0", "adopt it as a parent action restriction"], "2329 handoff"),
    ("SRC2330_01_2329_validation", "2329_validation", PATHS["2329_validation"], ["VAL2329_OVERALL", "PASS"], "2329 validation"),
    ("SRC2330_02_2329_signature", "2329_signature", PATHS["2329_signature"], ["SBF2329_1_source_blind_functor", "SIGNATURE_READY_NOT_CORPUS_ADOPTED"], "source-blind signature"),
    ("SRC2330_03_2329_proof", "2329_proof", PATHS["2329_proof"], ["NST2329_4_countermodel_closure", "NOT_DERIVED_SIGNATURE_ONLY"], "conditional proof"),
    ("SRC2330_04_2329_activation", "2329_activation", PATHS["2329_activation"], ["ACT2329_2_adopt_as_parent_action_definition", "THEORY_DECISION_REQUIRED"], "activation matrix"),
    ("SRC2330_05_2329_counter", "2329_counter", PATHS["2329_counter"], ["CMC2329_4_nonhilbert_current", "OPEN_RETAINED"], "countermodel matrix"),
    ("SRC2330_06_943_coframe", "943_coframe", PATHS["943_coframe"], ["CFC943_2_matter_functor", "not_parent_signed"], "observed coframe contract"),
    ("SRC2330_07_944_descent", "944_descent", PATHS["944_descent"], ["QDG944_3_matter_action_factorization", "not_parent_signed"], "descent proof gate"),
    ("SRC2330_08_954_clause", "954_clause", PATHS["954_clause"], ["PAC954_1_no_source_prefactors", "exact_high_pressure_missing_clause"], "parent action clause"),
    ("SRC2330_09_955_lemma", "955_lemma", PATHS["955_lemma"], ["MMA955_5_minimal_schema", "conditional_parent_schema_lemma"], "minimal matter lemma"),
    ("SRC2330_10_1079_theorem", "1079_theorem", PATHS["1079_theorem"], ["NCO1079_5_species_action_weight", "SURVIVES_PRE_VARIATION"], "current-owner limit"),
    ("SRC2330_11_1332_common", "1332_common", PATHS["1332_common"], ["CMT1332_0_common_mode_source_coupling", "COUNTERMODEL_RETAINED"], "common-mode theorem"),
    ("SRC2330_12_1333_attempt", "1333_attempt", PATHS["1333_attempt"], ["NSP1333_4_minimal_schema", "NOT_DERIVED_CURRENT_CORPUS"], "no-source-prefactor derivation attempt"),
    ("SRC2330_13_1337_contract", "1337_contract", PATHS["1337_contract"], ["PACT1337_2_no_source_only_species_slot", "SHARPEST_REQUIRED_PARENT_PREMISE"], "minimal parent action contract"),
    ("SRC2330_14_1337_theorem", "1337_theorem", PATHS["1337_theorem"], ["THM1337_0_common_mode_reduced_theorem", "LOCAL_SOURCE_SIDE_GR_ROUTE_CONDITIONAL_NOT_PROMOTED"], "conditional source-side theorem"),
    ("SRC2330_15_1337_decision", "1337_decision", PATHS["1337_decision"], ["DEC1337_0_derivation_progress", "parent object language"], "prior decision ledger"),
    ("SRC2330_16_1337_gate", "1337_gate", PATHS["1337_gate"], ["LGR1337_0_source_side", "CONDITIONAL_ON_PARENT_CONTRACT"], "local GR implication gate"),
    ("SRC2330_17_2125_common", "2125_common", PATHS["2125_common"], ["CMD2125_1_minimal_missing_clause", "THEOREM_TARGET_SHARPENED_NOT_CLOSED"], "common-mode descent audit"),
    ("SRC2330_18_2327_bound", "2327_bound", PATHS["2327_bound"], ["LSGM2327_0_bound_contract", "epsilon_sigma_source_GM"], "finite source_GM fallback"),
    ("SRC2330_19_2328_profile", "2328_profile", PATHS["2328_profile"], ["SPV2328_0_schema", "SCHEMA_READY_VALUES_MISSING"], "source-profile fallback"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2330_SOURCE_REGISTER.csv",
    "derivation": OUT / "P8_Y5_PARENT_QLOC_2330_DEEPER_QUOTIENT_DERIVATION_AUDIT.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2330_ADOPTION_DECISION_MATRIX.csv",
    "restriction": OUT / "P8_Y5_PARENT_QLOC_2330_PARENT_ACTION_RESTRICTION_DRAFT.csv",
    "impact": OUT / "P8_Y5_PARENT_QLOC_2330_DOWNSTREAM_GATE_IMPACT.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2330_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2330_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2330_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2330_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2330_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2330_0_derivation", OUTPUTS["derivation"], BETA_DOCS / "DEEPER_QUOTIENT_DERIVATION_AUDIT_2330_NONCLAIM.csv"),
    ("COPY2330_1_restriction", OUTPUTS["restriction"], RAB_QUEUE / "JR2330_PARENT_ACTION_RESTRICTION_DRAFT_NONCLAIM.csv"),
    ("COPY2330_2_impact", OUTPUTS["impact"], MICRO_RESIDUALS / "downstream_gate_impact_2330_nonclaim.csv"),
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
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
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def needle_status(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing_file"
    text = read_text(path)
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "missing_needles=" + ";".join(missing)
    return True, "all_needles_found"


def relative_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, key, path, needles, role in SOURCES:
        found, note = needle_status(path, needles)
        rows.append(
            {
                "timestamp_utc": timestamp(),
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_key": key,
                "source_path": str(path),
                "exists": bool_text(path.exists()),
                "needles": ";".join(needles),
                "needles_found": bool_text(found),
                "source_role": role,
                "valid_for_claim": "false",
                "notes": note,
            }
        )
    return rows


def build_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQD2330_0_target",
            "derivation_target": "derive source-blind matter functor from deeper quotient/flow primitives",
            "test": "Can q/flow structure alone force Matter: Q_obs x SpeciesRep -> ActionDensity with no active-source coefficient slot?",
            "result": "TARGET_SHARPENED",
            "obstruction_or_win": "this would be stronger than adopting the signature as an axiom",
            "next_requirement": "show species labels cannot define independent gravitational charge",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQD2330_1_quotient_descent",
            "derivation_target": "quotient descent",
            "test": "S_matter factors through q(Phi) and observed coframe data",
            "result": "PARTIAL_WIN_NOT_ENOUGH",
            "obstruction_or_win": "descent blocks representative-only fields, but species-indexed constants can still live inside theta_A",
            "next_requirement": "theta_A admissibility rule or no independent gravitational charge theorem",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQD2330_2_naturality",
            "derivation_target": "natural matter functor",
            "test": "naturality over Q_obs and SpeciesRep forbids non-natural source coefficients",
            "result": "CONDITIONAL_WIN_RESTATES_SIGNATURE",
            "obstruction_or_win": "if Coeff_active_source is absent from the functor domain, w_A is impossible; but absence is exactly the signature to justify",
            "next_requirement": "derive the allowed functor domain from parent action principles",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQD2330_3_double_accounting",
            "derivation_target": "no duplicate inertial/source normalization",
            "test": "a source-only w_A changes gravitational source without changing nongravitational normalization, so it double-counts matter normalization",
            "result": "STRONG_PHYSICAL_PRINCIPLE_NOT_FORMAL_DERIVATION",
            "obstruction_or_win": "excellent engineering-style rationale, but covariance/additivity do not force it by themselves",
            "next_requirement": "promote to parent admissibility principle or connect to deeper charge/Noether identity",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQD2330_4_no_independent_gravitational_charge",
            "derivation_target": "no independent gravitational charge for ordinary matter",
            "test": "ordinary matter has one stress-energy/Noether source, not a second species charge for gravity",
            "result": "BEST_DEEPER_DERIVATION_TARGET",
            "obstruction_or_win": "if proved, this derives NoSourceOnlySpeciesSlot rather than adopting it",
            "next_requirement": "prove source charge equals Hilbert/Noether energy for all ordinary matter from parent symmetries",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DQD2330_5_verdict",
            "derivation_target": "deeper quotient derivation of source-blind signature now",
            "test": "assemble quotient descent, naturality, no-double-counting, and source charge identity",
            "result": "NOT_DERIVED_YET_ADOPTION_ROUTE_READY",
            "obstruction_or_win": "the signature is exact and well-motivated, but current evidence does not prove it from deeper primitives",
            "next_requirement": "choose provisional parent-action adoption or continue into a Noether/source-charge derivation target",
            "valid_for_claim": "false",
        },
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADM2330_0_option_adopt",
            "option": "adopt source-blind signature as parent-action restriction",
            "status": "RECOMMENDED_PROVISIONAL_PRIVATE_ROUTE",
            "benefit": "closes known source-only species-weight countermodels and cleans source-side GR route",
            "cost_or_risk": "must be labelled as an adopted parent-action restriction until deeper derivation exists",
            "decision": "ALLOW_AS_PRIVATE_WORKING_AXIOM_NOT_PUBLIC_CLAIM",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADM2330_1_option_deeper_derivation",
            "option": "continue trying to derive signature from quotient/flow/Noether source identity",
            "status": "BEST_PURIST_ROUTE",
            "benefit": "would make local GR reduction feel derived rather than stipulated",
            "cost_or_risk": "not closed now; may take several checkpoints",
            "decision": "KEEP_AS_NEXT_THEOREM_TARGET",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADM2330_2_option_finite_fallback",
            "option": "decline adoption and source finite profile/vector rows",
            "status": "HONEST_EMPIRICAL_FALLBACK",
            "benefit": "keeps theory testable without pretending source universality is proved",
            "cost_or_risk": "less GR-like; local-GR reduction becomes bounded-residual rather than theorem-zero",
            "decision": "RETAIN_IF_ADOPTION_OR_DERIVATION_FAILS",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ADM2330_3_decision",
            "option": "2330 selected route",
            "status": "DUAL_TRACK_SELECTED",
            "benefit": "use source-blind signature as a private working parent-action contract while immediately attacking deeper Noether/source-charge derivation",
            "cost_or_risk": "must not call it a public derivation or local-GR pass",
            "decision": "PROVISIONAL_ADOPTION_PLUS_DERIVATION_AUDIT",
            "valid_for_claim": "false",
        },
    ]


def build_restriction_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAR2330_0_name",
            "restriction": "Minimal Universal Matter Coupling (private working parent-action restriction)",
            "formal_clause": "ordinary matter action factors through Q_obs and contains no independent SpeciesLabel -> Coeff_active_source morphism",
            "activation_status": "PROVISIONAL_PRIVATE_CONTRACT_ONLY",
            "what_changes": "future local-GR branch may test consequences under this declared parent restriction",
            "what_not_changed": "no public claim; no formalization-workbench activation; no empirical pass",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAR2330_1_action_form",
            "restriction": "source-blind ordinary matter action",
            "formal_clause": "S_m = integral mu_obs sum_A L_A(j^k Psi_A,e_obs,omega_obs,theta_A); theta_A excludes source-only gravitational multipliers",
            "activation_status": "DRAFT_READY",
            "what_changes": "pre-action w_A is inadmissible inside the restricted branch",
            "what_not_changed": "non-Hilbert/boundary/readout currents still need zero proof or finite residual rows",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAR2330_2_common_calibration",
            "restriction": "one common source scale only",
            "formal_clause": "S_m -> lambda S_m allowed only as common calibration absorbed into measured kappa/G_N/GM",
            "activation_status": "DRAFT_READY",
            "what_changes": "common source scale is not a WEP/PPN residual",
            "what_not_changed": "relative scales lambda_A remain forbidden or finite residuals",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PAR2330_3_no_hidden_return",
            "restriction": "no hidden source-weight return",
            "formal_clause": "boundary, marker, readout, and non-Hilbert currents are zero only when proved exact/projected-silent; otherwise retained as J_residual",
            "activation_status": "OPEN_PARALLEL_GATE",
            "what_changes": "prevents using adoption to sweep source tails away",
            "what_not_changed": "must run non-Hilbert source-current silence or residual checkpoint next/parallel",
            "valid_for_claim": "false",
        },
    ]


def build_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGI2330_0_source_only_slot",
            "gate": "NoSourceOnlySpeciesSlot",
            "impact_if_private_restriction_used": "closed within restricted parent-action branch",
            "still_missing": "deeper derivation or public justification",
            "claim_status": "conditional_private_branch_only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGI2330_1_source_GM_zero",
            "gate": "epsilon_sigma_source_GM=0 from source universality",
            "impact_if_private_restriction_used": "major species-weight leak closed, but source profile/GM/same-frame and hidden-current gates remain",
            "still_missing": "GM calibration equation, same-frame source pullback, non-Hilbert silence",
            "claim_status": "not_zero_yet",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGI2330_2_source_side_GR",
            "gate": "ordinary matter source reduces to one calibrated Hilbert current",
            "impact_if_private_restriction_used": "source-side common-mode theorem becomes available conditionally",
            "still_missing": "non-Hilbert residual closure and left-hand EH/Newton operator",
            "claim_status": "conditional_source_side_only",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGI2330_3_local_GR_Newton",
            "gate": "full local GR/Newton recovery",
            "impact_if_private_restriction_used": "not enough by itself",
            "still_missing": "EH/Newton left-hand limit, PPN/readout residuals, local projector/domain terms",
            "claim_status": "blocked",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGI2330_4_empirical_branch",
            "gate": "finite source-profile vector fallback",
            "impact_if_private_restriction_used": "can be parked, not deleted",
            "still_missing": "needed if adoption/deeper derivation fails or hidden source tails remain",
            "claim_status": "retained_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2330_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2330_1_derivation_attempt", "gate": "deeper quotient derivation tested", "passed": "true", "claim_effect": "obstruction located", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2330_2_deeper_derivation_closed", "gate": "source-blind signature derived from deeper primitives now", "passed": "false", "claim_effect": "not claimed", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2330_3_private_restriction_ready", "gate": "private working parent-action restriction precisely drafted", "passed": "true", "claim_effect": "usable for internal branch bookkeeping only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2330_4_source_GM_zero", "gate": "source_GM leakage zero promoted", "passed": "false", "claim_effect": "still blocked by parallel gates", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2330_5_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "not enough yet", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2330_6_github_public_update", "gate": "safe to push as public evidence", "passed": "false", "claim_effect": "private decision checkpoint only", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2330_0_adoption_as_derivation", "claim": "private adoption equals derivation", "allowed": "false", "reason": "deeper quotient audit did not close; adoption must be labelled as a working parent-action restriction", "blocking_rows": "DQD2330_5_verdict;ADM2330_3_decision", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2330_1_adoption_as_public_claim", "claim": "source-blind signature proves local GR publicly", "allowed": "false", "reason": "local GR still needs non-Hilbert, same-frame/readout, and left-hand EH/Newton gates", "blocking_rows": "DGI2330_2_source_side_GR;DGI2330_3_local_GR_Newton", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2330_2_delete_fallback", "claim": "finite source-profile fallback can be deleted", "allowed": "false", "reason": "fallback remains needed if adoption/deeper derivation or hidden-current gates fail", "blocking_rows": "DGI2330_4_empirical_branch", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2330_3_skip_deeper_derivation", "claim": "no need to pursue deeper derivation after adoption", "allowed": "false", "reason": "the objective asks for derivability; adoption is useful but not the end state", "blocking_rows": "ADM2330_1_option_deeper_derivation", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2330_0",
            "next_target": "2331-Y5-R2FR-Noether-source-charge-identity-or-nonHilbert-residual-row.md",
            "why": "best purist route: try to derive no independent gravitational source charge from Hilbert/Noether source identity; if not, retain non-Hilbert residual row.",
            "claim_status": "private_derivation_next_step",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2330_1",
            "next_target": "2331b-Y5-R2FR-private-minimal-universal-matter-coupling-branch-ledger.md",
            "why": "track the provisional restricted parent-action branch separately so it cannot be mistaken for a public derivation.",
            "claim_status": "branch_bookkeeping_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2330_2",
            "next_target": "2331c-Y5-R2FR-same-frame-GM-calibration-after-source-slot-restriction.md",
            "why": "if the restriction is used privately, same-frame GM calibration becomes the next source_GM zero bottleneck.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row_id, src, dest in BRANCH_COPY_SPECS:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dest)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "source_csv": relative_path(src),
                "branch_copy_path": str(dest),
                "copy_exists": bool_text(dest.exists()),
                "row_count": str(len(read_csv_rows(dest))),
                "valid_for_claim": "false",
            }
        )
    return rows


def build_validation_rows(source_rows: list[dict[str, Any]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"]
    generated_paths += [Path(row["branch_copy_path"]) for row in branch_copy_rows]
    rows: list[dict[str, Any]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": "false",
            }
        )

    add("VAL2330_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2330_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    derivation_rows = read_csv_rows(OUTPUTS["derivation"])
    add("VAL2330_02_derivation_audit", any(row.get("row_id") == "DQD2330_5_verdict" and row.get("result") == "NOT_DERIVED_YET_ADOPTION_ROUTE_READY" for row in derivation_rows), "deeper derivation tested and not overclaimed")
    decision_rows = read_csv_rows(OUTPUTS["decision"])
    add("VAL2330_03_decision_matrix", any(row.get("row_id") == "ADM2330_3_decision" and row.get("decision") == "PROVISIONAL_ADOPTION_PLUS_DERIVATION_AUDIT" for row in decision_rows), "dual-track decision recorded")
    restriction_rows = read_csv_rows(OUTPUTS["restriction"])
    add("VAL2330_04_restriction_draft", any(row.get("row_id") == "PAR2330_0_name" and row.get("activation_status") == "PROVISIONAL_PRIVATE_CONTRACT_ONLY" for row in restriction_rows), "private parent-action restriction drafted")
    impact_rows = read_csv_rows(OUTPUTS["impact"])
    add("VAL2330_05_local_gr_still_blocked", any(row.get("row_id") == "DGI2330_3_local_GR_Newton" and row.get("claim_status") == "blocked" for row in impact_rows), "local GR/Newton still not claimed")
    add("VAL2330_06_fallback_retained", any(row.get("row_id") == "DGI2330_4_empirical_branch" and row.get("claim_status") == "retained_nonclaim" for row in impact_rows), "finite fallback retained")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2330_07_claim_gates_block", any(row.get("row_id") == "CG2330_5_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim gate remains false")
    add("VAL2330_08_github_blocked", any(row.get("row_id") == "CG2330_6_github_public_update" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended as evidence")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2330_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2330_10_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 2, "next targets selected")
    add("VAL2330_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2330_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2330*.csv", "*2330-Y5*.md", "*DEEPER_QUOTIENT*2330*", "*MINIMAL_UNIVERSAL*2330*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2330_13_formalization_untouched_by_2330", not formalization_hits, "no 2330 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2330_OVERALL", all(row["status"] == "PASS" for row in rows), "2330 tests the deeper quotient route, finds it not closed, records a provisional private Minimal Universal Matter Coupling restriction plus continued derivation audit, keeps finite/non-Hilbert fallbacks, and recommends no GitHub evidence update yet.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    derivation_rows: list[dict[str, Any]],
    decision_rows: list[dict[str, Any]],
    restriction_rows: list[dict[str, Any]],
    impact_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2330 - Parent Action Adoption Vs Deeper Quotient Derivation Decision

## Summary

2330 tests the purist route first: can the source-blind matter signature be derived from deeper quotient/flow structure
alone?

Result: not yet. Quotient descent and naturality get close, but they do not by themselves forbid species-indexed
constants. The missing deeper theorem is sharper now: ordinary matter must have no independent gravitational source
charge beyond its Hilbert/Noether stress source.

The disciplined decision is dual-track:

1. use `Minimal Universal Matter Coupling` as a **private provisional parent-action restriction** for bookkeeping, and
2. keep trying to derive that restriction from a deeper Noether/source-charge identity.

This is not a local-GR claim and not a GitHub/public evidence update. It is a clean fork-control step.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Deeper Quotient Derivation Audit

{markdown_table(derivation_rows, ["row_id", "derivation_target", "test", "result", "obstruction_or_win", "next_requirement", "valid_for_claim"])}

## Adoption Decision Matrix

{markdown_table(decision_rows, ["row_id", "option", "status", "benefit", "cost_or_risk", "decision", "valid_for_claim"])}

## Parent Action Restriction Draft

{markdown_table(restriction_rows, ["row_id", "restriction", "formal_clause", "activation_status", "what_changes", "what_not_changed", "valid_for_claim"])}

## Downstream Gate Impact

{markdown_table(impact_rows, ["row_id", "gate", "impact_if_private_restriction_used", "still_missing", "claim_status", "valid_for_claim"])}

## Claim Gates

{markdown_table(claim_rows, ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusal_rows, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_target", "why", "claim_status", "valid_for_claim"])}

## Branch Copies

{markdown_table(branch_copy_rows, ["row_id", "source_csv", "branch_copy_path", "copy_exists", "row_count", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows, ["row_id", "status", "detail", "valid_for_claim"])}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows_by_output = {
        "sources": build_sources(),
        "derivation": build_derivation_rows(),
        "decision": build_decision_rows(),
        "restriction": build_restriction_rows(),
        "impact": build_impact_rows(),
        "claims": build_claim_rows(),
        "refusal": build_refusal_rows(),
        "next": build_next_rows(),
    }
    for key, rows in rows_by_output.items():
        write_csv(OUTPUTS[key], rows)
    branch_copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["copies"], branch_copy_rows)
    validation_rows = build_validation_rows(rows_by_output["sources"], branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_doc(
        rows_by_output["sources"],
        rows_by_output["derivation"],
        rows_by_output["decision"],
        rows_by_output["restriction"],
        rows_by_output["impact"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2330 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
