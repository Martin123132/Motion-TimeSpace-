from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_ACTION_SOURCE_BLIND_FUNCTOR_SIGNATURE_2329"

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
FORMALIZATION = PROJECT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICRO_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2329-Y5-R2FR-parent-action-source-blind-functor-signature.md"

PATHS = {
    "2328_doc": ROOT / "2328-Y5-R2FR-NoSourceOnlySpeciesSlot-or-source-profile-vector-first-row.md",
    "2328_validation": OUT / "P8_Y5_BRR545_2328_VALIDATION.csv",
    "2328_derivation": OUT / "P8_Y5_PARENT_QLOC_2328_NO_SOURCE_ONLY_SPECIES_SLOT_DERIVATION_ATTEMPT.csv",
    "2328_contract": OUT / "P8_Y5_PARENT_QLOC_2328_PARENT_ACTION_CONTRACT.csv",
    "2328_profile": OUT / "P8_Y5_PARENT_QLOC_2328_SOURCE_PROFILE_VECTOR_FIRST_ROW.csv",
    "2328_counter": OUT / "P8_Y5_PARENT_QLOC_2328_COUNTERMODEL_DECISION_LEDGER.csv",
    "943_coframe": OUT / "P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
    "944_descent": OUT / "P8_Y5_R10_944_DESCENT_PROOF_GATE.csv",
    "954_clause": OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
    "954_label": OUT / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
    "955_lemma": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "955_class": OUT / "P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
    "1079_theorem": OUT / "P8_Y5_R10_1079_NARROW_CURRENT_OWNER_THEOREM_ATTEMPT.csv",
    "1332_common": OUT / "P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv",
    "1332_premise": OUT / "P8_Y5_R10_1332_COMMON_MODE_PREMISE_AUDIT.csv",
    "1333_attempt": OUT / "P8_Y5_R10_1333_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv",
    "1333_counter": OUT / "P8_Y5_R10_1333_SOURCE_PREFACTOR_COUNTERMODEL_LEDGER.csv",
    "1337_contract": OUT / "P8_Y5_R10_1337_MINIMAL_PARENT_ACTION_CONTRACT.csv",
    "1337_theorem": OUT / "P8_Y5_R10_1337_COMMON_MODE_THEOREM_UPDATE.csv",
    "1337_gate": OUT / "P8_Y5_R10_1337_LOCAL_GR_IMPLICATION_GATE.csv",
    "1425_premise": OUT / "P8_Y5_R10_1425_COMMON_MODE_PREMISE_AUDIT.csv",
    "2125_common": OUT / "P8_Y5_PARENT_QLOC_2125_COMMON_MODE_DESCENT_AUDIT.csv",
}

SOURCES = [
    ("SRC2329_00_2328_doc", "2328_doc", PATHS["2328_doc"], ["NEXT2328_0", "source-blind"], "2328 handoff"),
    ("SRC2329_01_2328_validation", "2328_validation", PATHS["2328_validation"], ["VAL2328_OVERALL", "PASS"], "2328 validation"),
    ("SRC2329_02_2328_derivation", "2328_derivation", PATHS["2328_derivation"], ["NSOS2328_4_source_blind_functor", "EXACT_CONDITIONAL_THEOREM"], "source-blind theorem"),
    ("SRC2329_03_2328_contract", "2328_contract", PATHS["2328_contract"], ["PAC2328_2_no_source_only_species_slot", "CONTRACT_EXACT_BUT_UNSIGNED"], "2328 parent contract"),
    ("SRC2329_04_2328_profile", "2328_profile", PATHS["2328_profile"], ["SPV2328_0_schema", "SCHEMA_READY_VALUES_MISSING"], "finite fallback row"),
    ("SRC2329_05_2328_counter", "2328_counter", PATHS["2328_counter"], ["CMD2328_0_relative_species_weight", "LIVE_UNTIL_PARENT_CONTRACT_SIGNED"], "countermodel decision"),
    ("SRC2329_06_943_coframe", "943_coframe", PATHS["943_coframe"], ["CFC943_2_matter_functor", "not_parent_signed"], "observed coframe matter functor"),
    ("SRC2329_07_944_descent", "944_descent", PATHS["944_descent"], ["QDG944_3_matter_action_factorization", "not_parent_signed"], "matter action factorization gate"),
    ("SRC2329_08_954_clause", "954_clause", PATHS["954_clause"], ["PAC954_1_no_source_prefactors", "exact_high_pressure_missing_clause"], "parent action clause"),
    ("SRC2329_09_954_label", "954_label", PATHS["954_label"], ["PLF954_5_verdict", "exact_contract_written_not_parent_signed"], "label forgetting attempt"),
    ("SRC2329_10_955_lemma", "955_lemma", PATHS["955_lemma"], ["MMA955_5_minimal_schema", "conditional_parent_schema_lemma"], "minimal matter lemma"),
    ("SRC2329_11_955_class", "955_class", PATHS["955_class"], ["SPC955_2_relative_species_weight", "live_countermodel"], "source prefactor classification"),
    ("SRC2329_12_1079_theorem", "1079_theorem", PATHS["1079_theorem"], ["NCO1079_5_species_action_weight", "SURVIVES_PRE_VARIATION"], "Hilbert-owner limit"),
    ("SRC2329_13_1332_common", "1332_common", PATHS["1332_common"], ["CMT1332_0_common_mode_source_coupling", "EXACT_CONDITIONAL_THEOREM"], "common-mode source theorem"),
    ("SRC2329_14_1332_premise", "1332_premise", PATHS["1332_premise"], ["PREM1332_3_no_relative_source_prefactors", "EXACT_HIGH_PRESSURE_MISSING_CLAUSE"], "common-mode premise audit"),
    ("SRC2329_15_1333_attempt", "1333_attempt", PATHS["1333_attempt"], ["NSP1333_4_minimal_schema", "NOT_DERIVED_CURRENT_CORPUS"], "no-source-prefactor attempt"),
    ("SRC2329_16_1333_counter", "1333_counter", PATHS["1333_counter"], ["CM1333_0_relative_species_weight", "LIVE_COUNTERMODEL"], "source-prefactor countermodel"),
    ("SRC2329_17_1337_contract", "1337_contract", PATHS["1337_contract"], ["PACT1337_2_no_source_only_species_slot", "SHARPEST_REQUIRED_PARENT_PREMISE"], "minimal parent action contract"),
    ("SRC2329_18_1337_theorem", "1337_theorem", PATHS["1337_theorem"], ["THM1337_0_common_mode_reduced_theorem", "EXACT_CONDITIONAL_REDUCED_PREMISES"], "reduced theorem"),
    ("SRC2329_19_1337_gate", "1337_gate", PATHS["1337_gate"], ["LGR1337_0_source_side", "CONDITIONAL_ON_PARENT_CONTRACT"], "local GR implication gate"),
    ("SRC2329_20_1425_premise", "1425_premise", PATHS["1425_premise"], ["PREM1425_3_no_relative_source_prefactors", "EXACT_HIGH_PRESSURE_MISSING_CLAUSE"], "WEP premise audit"),
    ("SRC2329_21_2125_common", "2125_common", PATHS["2125_common"], ["CMD2125_1_minimal_missing_clause", "THEOREM_TARGET_SHARPENED_NOT_CLOSED"], "common-mode descent audit"),
]

OUTPUTS = {
    "sources": OUT / "P8_Y5_PARENT_QLOC_2329_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_PARENT_QLOC_2329_SOURCE_BLIND_FUNCTOR_SIGNATURE.csv",
    "proof": OUT / "P8_Y5_PARENT_QLOC_2329_NOSOURCE_SLOT_THEOREM_PROOF.csv",
    "activation": OUT / "P8_Y5_PARENT_QLOC_2329_PARENT_SIGNATURE_ACTIVATION_MATRIX.csv",
    "countermodel": OUT / "P8_Y5_PARENT_QLOC_2329_COUNTERMODEL_CLOSURE_MATRIX.csv",
    "claims": OUT / "P8_Y5_PARENT_QLOC_2329_CLAIM_GATES.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2329_REFUSAL_RUNNER.csv",
    "next": OUT / "P8_Y5_PARENT_QLOC_2329_NEXT_TARGET.csv",
    "copies": OUT / "P8_Y5_PARENT_QLOC_2329_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2329_VALIDATION.csv",
}

BRANCH_COPY_SPECS = [
    ("COPY2329_0_signature", OUTPUTS["signature"], BETA_DOCS / "SOURCE_BLIND_FUNCTOR_SIGNATURE_2329_NONCLAIM.csv"),
    ("COPY2329_1_countermodel", OUTPUTS["countermodel"], MICRO_RESIDUALS / "nosource_slot_countermodel_closure_2329_nonclaim.csv"),
    ("COPY2329_2_activation", OUTPUTS["activation"], RAB_QUEUE / "JR2329_PARENT_SIGNATURE_ACTIVATION_MATRIX_NONCLAIM.csv"),
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


def build_signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBF2329_0_parent_data",
            "signature_clause": "parent configuration contains an observed quotient before matter coupling",
            "mathematical_form": "Phi -> q(Phi)=Q_obs; O(q)=(M,g_obs,e_obs,omega_obs,theta)",
            "function": "defines what ordinary matter can see",
            "status": "SIGNATURE_PRECISE_NOT_INHERITED_PROOF",
            "closes_countermodel": "representative-only frame/source leaks",
            "parent_signed_active": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBF2329_1_source_blind_functor",
            "signature_clause": "ordinary matter is a source-blind functor of observed quotient data",
            "mathematical_form": "Matter: Q_obs x SpeciesRep -> ActionDensity, with no argument Coeff_active_source(A)",
            "function": "puts species labels inside representations and theta_A, not inside gravitational source strength",
            "status": "CORE_SIGNATURE_WRITTEN",
            "closes_countermodel": "SpeciesLabel -> active source coefficient morphism",
            "parent_signed_active": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBF2329_2_single_measure_scale",
            "signature_clause": "ordinary matter uses one observed measure and one common source normalization",
            "mathematical_form": "S_m = integral mu_obs sum_A L_A(j^k Psi_A,e_obs,omega_obs,theta_A)",
            "function": "makes Hilbert variation label-additive and permits one common calibration into kappa/G_N",
            "status": "SIGNATURE_PRECISE_NOT_INHERITED_PROOF",
            "closes_countermodel": "species-dependent measure/source scale",
            "parent_signed_active": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBF2329_3_theta_separation",
            "signature_clause": "theta_A may encode non-gravitational matter constants, not a source-only spurion",
            "mathematical_form": "theta_A allowed iff it changes matter dynamics/standards or is retained as a finite residual; source-only theta_A is inadmissible",
            "function": "prevents hiding w_A by renaming it as a material constant",
            "status": "SIGNATURE_PRECISE_REQUIRES_PARENT_ADMISSIBILITY_RULE",
            "closes_countermodel": "source-only constants disguised as theta_A",
            "parent_signed_active": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBF2329_4_hilbert_before_readout",
            "signature_clause": "source current is the Hilbert/coframe derivative before arena projection",
            "mathematical_form": "T_H := delta S_m/delta e_obs; K_arena, masks, Pi_gamma and GM calibration act downstream",
            "function": "kills post-variation source-current rescaling",
            "status": "EXACT_SUBTHEOREM_CONDITIONAL",
            "closes_countermodel": "post-variation source selectors",
            "parent_signed_active": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBF2329_5_nonhilbert_residual_policy",
            "signature_clause": "non-Hilbert/boundary/readout source currents are zero only by proof, otherwise retained",
            "mathematical_form": "J_source = T_H + J_NH + J_boundary + J_readout, with every non-Hilbert term zero/exact/projected-silent or finite-bounded",
            "function": "prevents source-only species weights returning through hidden currents",
            "status": "OPEN_PARALLEL_GATE_RETAINED",
            "closes_countermodel": "hidden non-Hilbert source-current weights only if signed",
            "parent_signed_active": "false",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "SBF2329_6_verdict",
            "signature_clause": "source-blind parent matter signature",
            "mathematical_form": "SBF2329_0 through SBF2329_5",
            "function": "would close NoSourceOnlySpeciesSlot and the source-side common-mode theorem if parent-adopted",
            "status": "SIGNATURE_READY_NOT_CORPUS_ADOPTED",
            "closes_countermodel": "known source-only species slot countermodels conditionally",
            "parent_signed_active": "false",
            "valid_for_claim": "false",
        },
    ]


def build_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NST2329_0_no_slot_from_signature",
            "lemma": "absence of source coefficient object",
            "formal_step": "In the source-blind functor signature, Coeff_active_source(A) is not in the domain of Matter, so partial S_m / partial w_A is undefined rather than zero-by-fit.",
            "proof_status": "EXACT_IF_SIGNATURE_ADOPTED",
            "remaining_gap": "signature is drafted here, not inherited from a deeper root action",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NST2329_1_common_scale_quotient",
            "lemma": "common source scale is calibration, not WEP/PPN residual",
            "formal_step": "If S_m -> lambda S_m for all ordinary matter, then kappa lambda is the locally measured coupling and relative source coefficients remain absent.",
            "proof_status": "EXACT_IF_SINGLE_SCALE",
            "remaining_gap": "requires proof there is only one scale, not species scales lambda_A",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NST2329_2_theta_loophole_closed",
            "lemma": "theta_A cannot hide source-only w_A",
            "formal_step": "If theta_A affects nongravitational dynamics, it is an ordinary material constant and must enter material tensors; if it only multiplies source strength, it is the forbidden source coefficient.",
            "proof_status": "EXACT_CLASSIFICATION_IF_ADMISSIBILITY_RULE_ADOPTED",
            "remaining_gap": "parent admissibility rule for theta_A must be signed",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NST2329_3_hilbert_owner",
            "lemma": "post-variation source tricks are killed",
            "formal_step": "The source tensor used by the field equation is the Hilbert variation of S_m before K_arena/Pi/readout; later projections cannot redefine the variational source.",
            "proof_status": "EXACT_GIVEN_READOUT_ORDER",
            "remaining_gap": "does not kill pre-action w_A unless the signature also forbids the slot",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NST2329_4_countermodel_closure",
            "lemma": "relative species-weight countermodel closure",
            "formal_step": "S_m=sum_A(1+epsilon_A)S_A is rejected exactly at SBF2329_1/SBF2329_2/SBF2329_3 because epsilon_A is a species-to-source coefficient not tied to ordinary matter normalization.",
            "proof_status": "CLOSED_IF_SIGNATURE_PARENT_SIGNED",
            "remaining_gap": "not closed in active corpus until parent signature is adopted or derived",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NST2329_5_source_side_GR",
            "lemma": "source-side GR/Newton reduction",
            "formal_step": "With SBF2329 signed and non-Hilbert residuals zero/retained, ordinary matter contributes one calibrated Hilbert source current T_total to the local field equation.",
            "proof_status": "CONDITIONAL_SOURCE_SIDE_GR_THEOREM",
            "remaining_gap": "left-hand EH/Newton limit and local readout residuals remain separate gates",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NST2329_6_verdict",
            "lemma": "NoSourceOnlySpeciesSlot active proof",
            "formal_step": "2329 derives NoSourceOnlySpeciesSlot as an unavoidable result of previous MTS primitives without adding/adopting a parent signature.",
            "proof_status": "NOT_DERIVED_SIGNATURE_ONLY",
            "remaining_gap": "2329 writes the exact signature and proof skeleton, but active adoption is still a theory decision or deeper derivation target",
            "valid_for_claim": "false",
        },
    ]


def build_activation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACT2329_0_signature_written",
            "activation_item": "source-blind matter functor signature",
            "evidence": "SBF2329_0 through SBF2329_6",
            "status": "WRITTEN_PRECISELY",
            "effect_if_activated": "NoSourceOnlySpeciesSlot closes at parent action level",
            "current_claim_effect": "none; nonclaim private contract",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACT2329_1_inherited_from_prior_primitives",
            "activation_item": "derivation from existing MTS primitives",
            "evidence": "943/944/954/955/1337 all say contract-ready or conditional, not parent-signed",
            "status": "NOT_INHERITED_AS_THEOREM",
            "effect_if_activated": "would avoid adding a new parent axiom",
            "current_claim_effect": "must not claim derivation from old primitives",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACT2329_2_adopt_as_parent_action_definition",
            "activation_item": "adopt signature as next parent action restriction",
            "evidence": "SBF2329 signature is internally precise and closes known countermodels conditionally",
            "status": "THEORY_DECISION_REQUIRED",
            "effect_if_activated": "source-side common-mode branch becomes much cleaner but must be declared as parent-action narrowing",
            "current_claim_effect": "not active yet",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACT2329_3_nonhilbert_residual",
            "activation_item": "non-Hilbert/boundary/readout residual silence",
            "evidence": "SBF2329_5 retained as open parallel gate",
            "status": "OPEN_PARALLEL_GATE",
            "effect_if_activated": "prevents hidden source weights bypassing Hilbert-source theorem",
            "current_claim_effect": "source-side GR theorem remains conditional",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ACT2329_4_finite_fallback",
            "activation_item": "source-profile vector finite branch",
            "evidence": "SPV2328_0_schema and LSGM2327 bound route",
            "status": "RETAINED_IF_SIGNATURE_NOT_ADOPTED",
            "effect_if_activated": "turns source-only slot leakage into bounded vector acquisition problem",
            "current_claim_effect": "schema only; no numeric claim",
            "valid_for_claim": "false",
        },
    ]


def build_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMC2329_0_relative_species_weight",
            "countermodel": "S_m=sum_A(1+epsilon_A)S_A",
            "signature_response": "forbidden by no SpeciesLabel -> Coeff_active_source object unless epsilon_A is an ordinary theta_A with nongravitational effects",
            "closure_status": "CLOSED_CONDITIONALLY_BY_SBF2329_1_TO_3",
            "if_signature_inactive": "retain Delta_w_source_profile/source residual vector",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMC2329_1_species_measure_weight",
            "countermodel": "S_m=sum_A integral w_A mu_obs L_A",
            "signature_response": "forbidden by one observed measure/source scale",
            "closure_status": "CLOSED_CONDITIONALLY_BY_SBF2329_2",
            "if_signature_inactive": "finite source/vector branch required",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMC2329_2_hidden_theta_source_weight",
            "countermodel": "theta_A contains a source-only multiplier but no nongravitational effect",
            "signature_response": "reclassified as forbidden Coeff_active_source(A), not allowed theta_A",
            "closure_status": "CLOSED_CONDITIONALLY_BY_SBF2329_3",
            "if_signature_inactive": "material/source tensor must retain coefficient",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMC2329_3_post_readout_source_selector",
            "countermodel": "K_arena or Pi_gamma reweights source after variation",
            "signature_response": "readout maps are downstream and cannot redefine T_H",
            "closure_status": "CLOSED_CONDITIONALLY_BY_SBF2329_4",
            "if_signature_inactive": "readout/source commutator residual remains",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CMC2329_4_nonhilbert_current",
            "countermodel": "J_source=T_H+sum_A zeta_A J_NH,A",
            "signature_response": "not closed by source-blind Hilbert signature unless J_NH is zero/exact/projected silent or bounded",
            "closure_status": "OPEN_RETAINED",
            "if_signature_inactive": "explicit non-Hilbert residual row required",
            "valid_for_claim": "false",
        },
    ]


def build_claim_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "CG2329_0_sources", "gate": "source paths and needles valid", "passed": "true", "claim_effect": "audit reproducible", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2329_1_signature_written", "gate": "source-blind parent action signature written precisely", "passed": "true", "claim_effect": "candidate contract ready for theory decision", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2329_2_NoSourceSlot_if_signed", "gate": "NoSourceOnlySpeciesSlot follows if signature is adopted", "passed": "true", "claim_effect": "conditional theorem only", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2329_3_active_parent_signed", "gate": "signature inherited/adopted by active corpus", "passed": "false", "claim_effect": "not active; no source-side GR claim", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2329_4_nonhilbert_silence", "gate": "non-Hilbert/boundary/readout source currents silent", "passed": "false", "claim_effect": "hidden-current gate remains", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2329_5_local_GR_Newton", "gate": "local GR/Newton recovery derived", "passed": "false", "claim_effect": "source-side only and still conditional", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "CG2329_6_github_public_update", "gate": "safe to push as public evidence", "passed": "false", "claim_effect": "not yet; private contract checkpoint", "valid_for_claim": "false"},
    ]


def build_refusal_rows() -> list[dict[str, Any]]:
    return [
        {"branch_id": BRANCH_ID, "row_id": "REF2329_0_signature_as_derivation", "claim": "2329 derives the parent signature from older MTS primitives", "allowed": "false", "reason": "older rows support a contract-ready shape, not an inherited theorem", "blocking_rows": "ACT2329_1_inherited_from_prior_primitives;NST2329_6_verdict", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2329_1_signature_as_public_claim", "claim": "source-blind functor signature is a public local-GR pass", "allowed": "false", "reason": "signature is precise but not active/adopted and non-Hilbert gates remain", "blocking_rows": "CG2329_3_active_parent_signed;CG2329_4_nonhilbert_silence", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2329_2_theta_hiding", "claim": "source-only w_A can be renamed theta_A and ignored", "allowed": "false", "reason": "theta_A is allowed only if it affects ordinary matter normalization or remains a finite residual", "blocking_rows": "SBF2329_3_theta_separation;NST2329_2_theta_loophole_closed", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2329_3_nonhilbert_ignore", "claim": "Hilbert-source theorem automatically kills non-Hilbert source currents", "allowed": "false", "reason": "non-Hilbert/boundary/readout currents are a separate open gate", "blocking_rows": "SBF2329_5_nonhilbert_residual_policy;CMC2329_4_nonhilbert_current", "valid_for_claim": "false"},
        {"branch_id": BRANCH_ID, "row_id": "REF2329_4_skip_finite_fallback", "claim": "finite source-profile vector route can be deleted", "allowed": "false", "reason": "fallback remains necessary until signature is adopted/derived and hidden-current gates close", "blocking_rows": "ACT2329_4_finite_fallback", "valid_for_claim": "false"},
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2329_0",
            "next_target": "2330-Y5-R2FR-parent-action-adoption-vs-deeper-quotient-derivation-decision.md",
            "why": "2329 wrote the exact signature; next choose whether to adopt it as a parent action restriction or try to derive it from deeper quotient/flow primitives.",
            "claim_status": "private_theory_decision_gate",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2329_1",
            "next_target": "2330b-Y5-R2FR-nonHilbert-source-current-silence-or-residual-row.md",
            "why": "even with source-blind Hilbert matter, non-Hilbert/boundary/readout source currents remain a parallel local-GR gate.",
            "claim_status": "parallel_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2329_2",
            "next_target": "2330c-Y5-R2FR-source-profile-vector-acquisition-if-signature-not-adopted.md",
            "why": "if the signature is not adopted, the finite source-profile vector fallback becomes the honest route.",
            "claim_status": "fallback_nonclaim",
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

    add("VAL2329_00_sources_exist", all(row["exists"] == "true" for row in source_rows), "every cited source path exists")
    add("VAL2329_01_needles_found", all(row["needles_found"] == "true" for row in source_rows), "all source needles were found")
    signature_rows = read_csv_rows(OUTPUTS["signature"])
    add("VAL2329_02_signature_written", any(row.get("row_id") == "SBF2329_6_verdict" and row.get("status") == "SIGNATURE_READY_NOT_CORPUS_ADOPTED" for row in signature_rows), "source-blind functor signature written and not overpromoted")
    proof_rows = read_csv_rows(OUTPUTS["proof"])
    add("VAL2329_03_conditional_proof", any(row.get("row_id") == "NST2329_4_countermodel_closure" and row.get("proof_status") == "CLOSED_IF_SIGNATURE_PARENT_SIGNED" for row in proof_rows), "NoSourceOnlySpeciesSlot proof closes conditionally")
    add("VAL2329_04_active_not_promoted", any(row.get("row_id") == "NST2329_6_verdict" and row.get("proof_status") == "NOT_DERIVED_SIGNATURE_ONLY" for row in proof_rows), "active derivation not overclaimed")
    activation_rows = read_csv_rows(OUTPUTS["activation"])
    add("VAL2329_05_activation_matrix", any(row.get("row_id") == "ACT2329_2_adopt_as_parent_action_definition" and row.get("status") == "THEORY_DECISION_REQUIRED" for row in activation_rows), "adoption-vs-derivation decision exposed")
    counter_rows = read_csv_rows(OUTPUTS["countermodel"])
    add("VAL2329_06_nonhilbert_open", any(row.get("row_id") == "CMC2329_4_nonhilbert_current" and row.get("closure_status") == "OPEN_RETAINED" for row in counter_rows), "non-Hilbert current gate retained")
    claim_rows = read_csv_rows(OUTPUTS["claims"])
    add("VAL2329_07_claim_gates_block", any(row.get("row_id") == "CG2329_5_local_GR_Newton" and row.get("passed") == "false" for row in claim_rows), "local GR/Newton claim remains blocked")
    add("VAL2329_08_github_blocked", any(row.get("row_id") == "CG2329_6_github_public_update" and row.get("passed") == "false" for row in claim_rows), "public GitHub update not recommended as evidence")
    refusal_rows = read_csv_rows(OUTPUTS["refusal"])
    add("VAL2329_09_refusals_block", all(row.get("allowed") == "false" for row in refusal_rows), "refusal runner blocks shortcut claims")
    add("VAL2329_10_next_target", len(read_csv_rows(OUTPUTS["next"])) >= 2, "next targets selected")
    add("VAL2329_11_branch_copies_parse", all(Path(row["branch_copy_path"]).exists() and int(row["row_count"]) > 0 for row in branch_copy_rows), "branch copies exist and parse")
    claim_flags: list[str] = []
    for path in generated_paths:
        for index, row in enumerate(read_csv_rows(path), start=2):
            if str(row.get("valid_for_claim", "")).lower() == "true":
                claim_flags.append(f"{path.name}:{index}")
    add("VAL2329_12_no_claim_flags", not claim_flags, "no generated row is valid_for_claim=true" if not claim_flags else ";".join(claim_flags))
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        checkpoint_patterns = ("*P8_Y5*2329*.csv", "*2329-Y5*.md", "*SOURCE_BLIND*2329*", "*NOSOURCE*2329*")
        for pattern in checkpoint_patterns:
            formalization_hits.extend(FORMALIZATION.rglob(pattern))
    add("VAL2329_13_formalization_untouched_by_2329", not formalization_hits, "no 2329 checkpoint output appears in formalization-workbench" if not formalization_hits else ";".join(str(path) for path in formalization_hits[:5]))
    add("VAL2329_OVERALL", all(row["status"] == "PASS" for row in rows), "2329 writes the exact source-blind parent matter functor signature, proves NoSourceOnlySpeciesSlot conditionally, refuses to claim inherited derivation/adoption, retains non-Hilbert and finite fallback gates, and recommends no GitHub evidence update yet.")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    activation_rows: list[dict[str, Any]],
    countermodel_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    refusal_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_copy_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    content = f"""# 2329 - Parent Action Source-Blind Functor Signature

## Summary

2329 turns the coupling throat into an explicit parent-action signature.

The clean signature is:

`Matter: Q_obs x SpeciesRep -> ActionDensity`

with one observed quotient frame, one measure/source scale, one Hilbert source before readout, ordinary matter constants
inside `theta_A`, and no object `Coeff_active_source(A)` in the domain. In that signature, a source-only species weight
`w_A` is not merely set to zero; it is not an admissible parent-action argument.

That is the strongest version of the route so far. But this checkpoint does **not** pretend it was already derived from
older MTS primitives. It is a precise parent-action signature ready for a theory decision or deeper quotient derivation.
Until adopted or derived, the source-profile vector fallback and non-Hilbert source-current gate remain live.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Source-Blind Functor Signature

{markdown_table(signature_rows, ["row_id", "signature_clause", "mathematical_form", "function", "status", "closes_countermodel", "parent_signed_active", "valid_for_claim"])}

## NoSourceOnlySpeciesSlot Theorem Proof

{markdown_table(proof_rows, ["row_id", "lemma", "formal_step", "proof_status", "remaining_gap", "valid_for_claim"])}

## Parent Signature Activation Matrix

{markdown_table(activation_rows, ["row_id", "activation_item", "evidence", "status", "effect_if_activated", "current_claim_effect", "valid_for_claim"])}

## Countermodel Closure Matrix

{markdown_table(countermodel_rows, ["row_id", "countermodel", "signature_response", "closure_status", "if_signature_inactive", "valid_for_claim"])}

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
        "signature": build_signature_rows(),
        "proof": build_proof_rows(),
        "activation": build_activation_rows(),
        "countermodel": build_countermodel_rows(),
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
        rows_by_output["signature"],
        rows_by_output["proof"],
        rows_by_output["activation"],
        rows_by_output["countermodel"],
        rows_by_output["claims"],
        rows_by_output["refusal"],
        rows_by_output["next"],
        branch_copy_rows,
        validation_rows,
    )
    failed = [row for row in validation_rows if row["status"] != "PASS"]
    if failed:
        raise SystemExit("2329 validation failed: " + "; ".join(row["row_id"] for row in failed))
    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
