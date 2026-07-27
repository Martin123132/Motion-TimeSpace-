from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1337"
TITLE = "1337-Y5-R10-RAB-common-mode-parent-action-premise-reduction-or-readout-data-intake"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_DIR = ROOT / "source-intake" / "microscope"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
INTAKE_STATUS_PATH = OUT_DIR / f"{PACK_ID}_OFFICIAL_INTAKE_STATUS.csv"
PREMISE_REDUCTION_PATH = OUT_DIR / f"{PACK_ID}_COMMON_MODE_PREMISE_REDUCTION.csv"
PARENT_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_MINIMAL_PARENT_ACTION_CONTRACT.csv"
COUNTERMODEL_PATH = OUT_DIR / f"{PACK_ID}_ADMISSIBLE_COUNTERMODEL_LEDGER.csv"
THEOREM_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_COMMON_MODE_THEOREM_UPDATE.csv"
LOCAL_GR_GATE_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_IMPLICATION_GATE.csv"
RUNNER_UPDATE_PATH = OUT_DIR / f"{PACK_ID}_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1337_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def bool_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not bool_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not bool_false(row.get("claim_allowed", False)):
                return False
    return True


def file_count(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for item in path.rglob("*") if item.is_file())


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1337*") if path.is_file()]


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1337_0_1336_next",
            "local_path": "source-intake/microscope/metadata/P8_Y5_R10_1336_NEXT_TARGET.csv",
            "needle": "NEXT1336_0_1337",
            "role": "selected 1337 target",
        },
        {
            "source_id": "SRC1337_1_1336_pivot",
            "local_path": "source-intake/microscope/metadata/P8_Y5_R10_1336_COMMON_MODE_PIVOT_DECISION.csv",
            "needle": "PIVOT1336_1_common_mode_theory_route",
            "role": "1336 common-mode pivot",
        },
        {
            "source_id": "SRC1337_2_1336_validation",
            "local_path": "source-intake/microscope/metadata/P8_Y5_BRR545_1336_VALIDATION.csv",
            "needle": "VAL1336_11_overall",
            "role": "1336 pass gate",
        },
        {
            "source_id": "SRC1337_3_1332_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1332_COMMON_MODE_SOURCE_THEOREM.csv",
            "needle": "CMT1332_0_common_mode_source_coupling",
            "role": "conditional common-mode theorem",
        },
        {
            "source_id": "SRC1337_4_1332_premises",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1332_COMMON_MODE_PREMISE_AUDIT.csv",
            "needle": "PREM1332_3_no_relative_source_prefactors",
            "role": "common-mode missing premise audit",
        },
        {
            "source_id": "SRC1337_5_1333_derivation",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1333_NO_SOURCE_PREFACTOR_DERIVATION_ATTEMPT.csv",
            "needle": "NSP1333_5_verdict",
            "role": "failed no-prefactor derivation",
        },
        {
            "source_id": "SRC1337_6_1333_countermodel",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1333_SOURCE_PREFACTOR_COUNTERMODEL_LEDGER.csv",
            "needle": "CM1333_0_relative_species_weight",
            "role": "relative species prefactor countermodel",
        },
        {
            "source_id": "SRC1337_7_1334_admissibility",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1334_PARENT_ADMISSIBILITY_PRINCIPLE_AUDIT.csv",
            "needle": "ADM1334_5_verdict",
            "role": "parent admissibility attempt",
        },
        {
            "source_id": "SRC1337_8_1334_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1334_SAME_BRANCH_WEP_PRODUCT_REQUIREMENTS.csv",
            "needle": "SBR1334_3_parent_branch",
            "role": "same-branch requirement reminder",
        },
        {
            "source_id": "SRC1337_9_1214_no_slot",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1214_NO_SOURCE_ONLY_SLOT_SIGNATURE_AUDIT.csv",
            "needle": "NSS1214_5_verdict",
            "role": "no-source-only-slot signature audit",
        },
        {
            "source_id": "SRC1337_10_1319_signature",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1319_MINIMAL_SIGNATURE_CANDIDATE.csv",
            "needle": "SIG1319_4_source_weight_exclusion",
            "role": "minimal signature source-weight exclusion",
        },
        {
            "source_id": "SRC1337_11_1335_waitstate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1335_READOUT_SOURCE_WAITSTATE.csv",
            "needle": "WAIT1335_0_official_arrays",
            "role": "finite electron data route waitstate",
        },
    ]
    source_register = []
    for spec in source_specs:
        exists, needle_found = exists_and_contains(spec["local_path"], spec["needle"])
        source_register.append(
            {
                **spec,
                "exists": exists,
                "needle_found": needle_found,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )

    intake_paths = [
        ("INTAKE1337_0_official_readout", MICROSCOPE_DIR / "official_readout", "official MICROSCOPE readout arrays"),
        ("INTAKE1337_1_source_worldtube", MICROSCOPE_DIR / "source_worldtube", "source-worldtube/profile inputs"),
        ("INTAKE1337_2_product_convention", MICROSCOPE_DIR / "product_convention", "eta/product/readout convention"),
        ("INTAKE1337_3_branch_classifier", MICROSCOPE_DIR / "branch_classifier", "same-branch classifier"),
    ]
    intake_status = [
        {
            "intake_id": intake_id,
            "absolute_path": str(path),
            "needed_for": needed_for,
            "exists": path.exists(),
            "file_count": file_count(path),
            "status": "READY_FOR_USER_IMPORT_FILES_PENDING" if file_count(path) == 0 else "FILES_PRESENT_REVIEW_REQUIRED",
            "selected_now": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for intake_id, path, needed_for in intake_paths
    ]

    premise_reduction = [
        {
            "premise_id": "RED1337_0_original_bundle",
            "premise": "ordinary matter is one descended observed matter action with no relative source-only prefactors",
            "role": "1332 common-mode theorem input",
            "reduction": "split into descent, single observed measure/action scale, no source-only species coefficient, and calibration quotient",
            "status": "BUNDLE_REDUCED_NOT_PARENT_SIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "RED1337_1_descent",
            "premise": "S_matter factors through q to observed metric/coframe data",
            "role": "kills representative-only frame/source leakage",
            "reduction": "requires q-owned observed frame and silence of vertical representative variables",
            "status": "REQUIRED_BUT_NOT_SUFFICIENT",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "RED1337_2_single_measure_scale",
            "premise": "all ordinary matter terms share the same action measure and active-source normalization",
            "role": "turns a common prefactor into measured G_N rather than WEP charge",
            "reduction": "one public measure/coframe/action scale; no species-dependent gravitational measure",
            "status": "MINIMAL_PARENT_CONTRACT_CLAUSE",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "RED1337_3_no_source_only_species_slot",
            "premise": "there is no morphism from a species label to an active gravitational source coefficient",
            "role": "kills w_A S_A while still allowing masses, charges, spins, and internal constants inside theta_A",
            "reduction": "smallest missing axiom is NoSourceOnlySpeciesSlot in the parent object language",
            "status": "SHARPEST_MISSING_PREMISE",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "RED1337_4_calibration_quotient",
            "premise": "a common factor multiplying total T_matter is absorbed into measured kappa/G_N",
            "role": "prevents confusing common coupling with WEP violation",
            "reduction": "only relative source coefficients survive material-difference tests",
            "status": "EXACT_IF_RED1337_2_AND_RED1337_3_HOLD",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    parent_contract = [
        {
            "clause_id": "PACT1337_0_observed_frame",
            "contract_clause": "There is a unique public observed metric/coframe e_obs,g_obs obtained from the parent quotient q.",
            "mathematical_form": "q(Phi) -> (M,g_obs,e_obs,theta_obs)",
            "what_it_forbids": "ordinary matter directly seeing representative-only vertical fields",
            "current_status": "CONTRACT_READY_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PACT1337_1_single_matter_functional",
            "contract_clause": "Ordinary matter is varied from one observed matter functional, not separate active-source functionals.",
            "mathematical_form": "S_m = integral mu(g_obs) L_m(j^k Psi_A,g_obs,theta_A)",
            "what_it_forbids": "a second gravitational source action independent of nongravitational dynamics",
            "current_status": "CONTRACT_READY_NOT_DERIVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PACT1337_2_no_source_only_species_slot",
            "contract_clause": "Species labels may select internal matter representation and theta_A, but may not select an active-source multiplier w_A.",
            "mathematical_form": "Hom(SpeciesLabel,Coeff_active_source)=empty",
            "what_it_forbids": "S_m=sum_A w_A S_A with w_A not fixed by ordinary matter normalization",
            "current_status": "SHARPEST_REQUIRED_PARENT_PREMISE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PACT1337_3_common_calibration",
            "contract_clause": "One common source normalization is quotient-calibrated into kappa or measured G_N.",
            "mathematical_form": "kappa_eff T_total = kappa_measured T_total after local calibration",
            "what_it_forbids": "using a common factor as a composition-dependent residual",
            "current_status": "DERIVED_CONDITIONAL_ON_SINGLE_SOURCE_SCALE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "clause_id": "PACT1337_4_nonHilbert_silence",
            "contract_clause": "Boundary/readout/non-Hilbert source currents either vanish, are exact/projected silent, or are retained as finite residuals.",
            "mathematical_form": "J_source = T_Hilbert_total + J_residual, with J_residual=0 only if parent-signed",
            "what_it_forbids": "hiding a species source coefficient in a non-Hilbert or readout current",
            "current_status": "OPEN_PARALLEL_GATE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    countermodels = [
        {
            "countermodel_id": "CM1337_0_relative_source_weight",
            "form": "S_m=sum_A (1+epsilon_A) S_A[Psi_A,g_obs,theta_A]",
            "survives_premises": "diffeomorphism covariance; additivity; same Hilbert variation; quotient descent if w_A is declared observed constant",
            "violates_contract": "PACT1337_2_no_source_only_species_slot",
            "physical_effect": "Delta_w_AB=sum_A DeltaF_AB,A epsilon_A can generate WEP/material residuals",
            "status": "LIVE_UNLESS_NO_SOURCE_SLOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1337_1_species_measure_weight",
            "form": "S_m=sum_A integral w_A mu(g_obs) L_A",
            "survives_premises": "scalar density and covariance if w_A is constant",
            "violates_contract": "PACT1337_2_no_source_only_species_slot;PACT1337_1_single_matter_functional",
            "physical_effect": "species-dependent active gravitational mass normalization",
            "status": "LIVE_UNLESS_SINGLE_MEASURE_SOURCE_SCALE_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "countermodel_id": "CM1337_2_hidden_readout_source_weight",
            "form": "J_source=T_total+sum_A zeta_A J_A_readout",
            "survives_premises": "can be covariant if J_A_readout is built as a conserved current",
            "violates_contract": "PACT1337_4_nonHilbert_silence",
            "physical_effect": "local WEP/PPN/readout channel reopens even if Hilbert T is common",
            "status": "LIVE_UNLESS_NONHILBERT_SILENCE_PARENT_SIGNED_OR_BOUNDED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    theorem_update = [
        {
            "theorem_id": "THM1337_0_common_mode_reduced_theorem",
            "statement": "If clauses PACT1337_0 through PACT1337_4 are parent-signed, ordinary matter contributes only one calibrated Hilbert source current in the local branch.",
            "proof_status": "EXACT_CONDITIONAL_REDUCED_PREMISES",
            "proof_sketch": "Descent restricts matter to observed fields; one measure/action scale makes total Hilbert variation label-additive; no source-only species slot removes w_A; common normalization is absorbed into G_N; non-Hilbert/readout currents are silent or retained.",
            "claim_result": "LOCAL_SOURCE_SIDE_GR_ROUTE_CONDITIONAL_NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1337_1_no_source_slot_is_minimal",
            "statement": "The smallest still-missing coupling axiom is the absence of a source-only species slot in the parent object language.",
            "proof_status": "MINIMALITY_AUDIT_NOT_PARENT_PROOF",
            "proof_sketch": "Remove only PACT1337_2 and the w_A countermodel survives all other common-mode clauses; add it back and relative source prefactors collapse into common mode.",
            "claim_result": "NEXT_TARGET_OBJECT_LANGUAGE_DERIVATION",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "THM1337_2_readout_route_status",
            "statement": "Official MICROSCOPE data intake remains parked and cannot score the finite electron branch.",
            "proof_status": "DATA_WAITSTATE",
            "proof_sketch": "1336 found schemas/directories/source strings but zero official readout, source-worldtube, product-convention, or branch-classifier files.",
            "claim_result": "NO_WEP_SCORE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_gr_gate = [
        {
            "gate_id": "LGR1337_0_source_side",
            "gate": "matter source reduces to one calibrated Hilbert current",
            "current_status": "CONDITIONAL_ON_PARENT_CONTRACT",
            "blocks_claim": True,
            "reason": "PACT1337 clauses are not derived from MTS primitives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LGR1337_1_geometric_left_hand",
            "gate": "field equation left-hand side reduces to EH/Newton operator",
            "current_status": "STILL_REQUIRED_SEPARATE_GATE",
            "blocks_claim": True,
            "reason": "common-mode source is necessary but not the full GR reduction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LGR1337_2_readout_residuals",
            "gate": "PPN/clock/orbital/readout residuals vanish or are bounded",
            "current_status": "STILL_REQUIRED_SEPARATE_GATE",
            "blocks_claim": True,
            "reason": "non-Hilbert/readout/source-worldtube channels remain open unless parent-signed or bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner_update = [
        {
            "runner_id": "RUN1337_0_common_mode_premise_reduction",
            "target": "reduce common-mode source theorem to smallest parent premise",
            "input_status": "PREMISE_REDUCED",
            "runner_status": "CONDITIONAL_THEOREM_STRENGTHENED_NOT_CLAIMED",
            "score_ready": False,
            "reason": "NoSourceOnlySpeciesSlot is isolated but not parent-derived",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1337_1_official_readout_data_intake",
            "target": "finite electron WEP data route",
            "input_status": "OFFICIAL_FILES_ABSENT",
            "runner_status": "PARKED_WAITSTATE",
            "score_ready": False,
            "reason": "official MICROSCOPE files are not present in intake directories",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1337_0_no_contract_as_parent_derivation",
            "shortcut": "treat PACT1337 as already derived from motion/time/space primitives",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1337_1_no_countermodel_ignoring",
            "shortcut": "ignore w_A because it looks aesthetically ugly",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1337_2_no_WEP_score_without_files",
            "shortcut": "score WEP without official MICROSCOPE files",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1337_3_no_local_GR_claim",
            "shortcut": "promote source-side conditional theorem to full GR/Newton reduction",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1337_0_derivation_progress",
            "decision": "common-mode coupling problem is now reduced to one sharp parent-language gap",
            "because": "the relative w_A countermodel survives exactly when a source-only species slot is allowed",
            "effect": "next derivation should target the parent object language, not more WEP arithmetic",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1337_1_data_route",
            "decision": "official MICROSCOPE intake remains parked",
            "because": "schemas/directories exist but no official files are present",
            "effect": "do not spend theory tokens pretending unit-kernel WEP scoring is physical",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1337_0_1338",
            "target_file": "1338-Y5-R10-RAB-parent-object-language-no-source-slot-theorem-or-explicit-closure.md",
            "target_script": "scripts/Y5_R10_RAB_parent_object_language_no_source_slot_theorem_or_explicit_closure.py",
            "task": "try to derive NoSourceOnlySpeciesSlot from the MTS parent object language; if impossible, demote common-mode source coupling to an explicit local-GR closure condition",
            "success_condition": "source-only species coefficients are forbidden by a parent-language theorem, or the exact closure condition and live countermodels are written without a GR claim",
            "do_not": "do not use minimality taste as proof, do not score WEP without official files, do not claim local GR from source-side work alone",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        intake_status,
        premise_reduction,
        parent_contract,
        countermodels,
        theorem_update,
        local_gr_gate,
        runner_update,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    intake_absent = all(row["file_count"] == 0 for row in intake_status)
    sharpest_premise = any(row["premise_id"] == "RED1337_3_no_source_only_species_slot" and row["status"] == "SHARPEST_MISSING_PREMISE" for row in premise_reduction)
    live_countermodel = any(row["countermodel_id"] == "CM1337_0_relative_source_weight" and row["status"].startswith("LIVE") for row in countermodels)
    conditional_theorem = any(row["theorem_id"] == "THM1337_0_common_mode_reduced_theorem" and row["proof_status"] == "EXACT_CONDITIONAL_REDUCED_PREMISES" for row in theorem_update)
    local_gr_blocked = all(row["blocks_claim"] is True for row in local_gr_gate)
    runners_not_scoreable = all(row["score_ready"] is False and row["valid_prediction_row"] is False for row in runner_update)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1338 = next_target[0]["target_file"].startswith("1338-")

    validations = [
        validation_row(
            "VAL1337_0_sources_exist",
            "registered local source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1337_1_intake_absent",
            "official MICROSCOPE intake files remain absent",
            intake_absent,
            ";".join(f"{row['intake_id']}={row['file_count']}" for row in intake_status),
        ),
        validation_row(
            "VAL1337_2_sharpest_premise",
            "NoSourceOnlySpeciesSlot is isolated as the sharpest missing premise",
            sharpest_premise,
            "RED1337_3_no_source_only_species_slot=SHARPEST_MISSING_PREMISE",
        ),
        validation_row(
            "VAL1337_3_countermodel_live",
            "relative source-weight countermodel remains live unless the sharp premise is signed",
            live_countermodel,
            "CM1337_0_relative_source_weight live",
        ),
        validation_row(
            "VAL1337_4_conditional_theorem",
            "common-mode theorem is strengthened only as an exact conditional",
            conditional_theorem,
            "THM1337_0_common_mode_reduced_theorem=EXACT_CONDITIONAL_REDUCED_PREMISES",
        ),
        validation_row(
            "VAL1337_5_local_GR_blocked",
            "local GR/Newton claim remains blocked",
            local_gr_blocked,
            ";".join(f"{row['gate_id']}={row['current_status']}" for row in local_gr_gate),
        ),
        validation_row(
            "VAL1337_6_runners_not_scoreable",
            "runners refuse WEP/local-GR scoring",
            runners_not_scoreable,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner_update),
        ),
        validation_row(
            "VAL1337_7_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1337_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1337_9_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1337_10_next_target_1338",
            "next target routes to parent object-language no-source-slot theorem or explicit closure",
            next_is_1338,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1337_11_overall",
            "overall 1337 validation",
            all(row["status"] == "PASS" for row in validations),
            "1337 reduces the common-mode coupling gap to NoSourceOnlySpeciesSlot and keeps all WEP/local-GR claims blocked",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(INTAKE_STATUS_PATH, intake_status)
    write_csv(PREMISE_REDUCTION_PATH, premise_reduction)
    write_csv(PARENT_CONTRACT_PATH, parent_contract)
    write_csv(COUNTERMODEL_PATH, countermodels)
    write_csv(THEOREM_UPDATE_PATH, theorem_update)
    write_csv(LOCAL_GR_GATE_PATH, local_gr_gate)
    write_csv(RUNNER_UPDATE_PATH, runner_update)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1337 makes real derivation progress but does not claim local GR. The common-mode/source-coupling problem is reduced to one sharp missing parent-language premise: `NoSourceOnlySpeciesSlot`.

**Main progress:** the old broad coupling gap is now cleaner. If the parent action has one observed matter functional, one measure/source scale, no source-only species coefficient, calibrated common normalization, and silent non-Hilbert/readout currents, then ordinary matter contributes one calibrated Hilbert source. But the relative `w_A` countermodel remains live unless that no-source-slot premise is derived.

**Decision:** keep official MICROSCOPE WEP intake parked; next target is to derive `NoSourceOnlySpeciesSlot` from the parent object language or demote common-mode coupling to an explicit local-GR closure condition.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Official Intake Status
{markdown_table(intake_status, ["intake_id", "absolute_path", "needed_for", "exists", "file_count", "status", "selected_now", "valid_for_claim", "claim_allowed"])}

## Common-Mode Premise Reduction
{markdown_table(premise_reduction, ["premise_id", "premise", "role", "reduction", "status", "parent_signed", "valid_for_claim", "claim_allowed"])}

## Minimal Parent Action Contract
{markdown_table(parent_contract, ["clause_id", "contract_clause", "mathematical_form", "what_it_forbids", "current_status", "valid_for_claim", "claim_allowed"])}

## Admissible Countermodel Ledger
{markdown_table(countermodels, ["countermodel_id", "form", "survives_premises", "violates_contract", "physical_effect", "status", "valid_for_claim", "claim_allowed"])}

## Common-Mode Theorem Update
{markdown_table(theorem_update, ["theorem_id", "statement", "proof_status", "proof_sketch", "claim_result", "valid_for_claim", "claim_allowed"])}

## Local GR Implication Gate
{markdown_table(local_gr_gate, ["gate_id", "gate", "current_status", "blocks_claim", "reason", "valid_for_claim", "claim_allowed"])}

## Runner Update
{markdown_table(runner_update, ["runner_id", "target", "input_status", "runner_status", "score_ready", "reason", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

## Anti-Shortcut Gates
{markdown_table(anti_shortcut, ["gate_id", "shortcut", "enforcement", "status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decision, ["decision_id", "decision", "because", "effect", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    print(f"Wrote {DOC_PATH}")
    print(f"Wrote validation {VALIDATION_PATH}")


if __name__ == "__main__":
    main()
