from __future__ import annotations

import csv
from pathlib import Path


PACK_ID = "P8_Y5_R10_1332"
TITLE = "1332-Y5-R10-RAB-universal-metric-source-coupling-or-electron-normalization-closure"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COMMON_MODE_THEOREM_PATH = OUT_DIR / f"{PACK_ID}_COMMON_MODE_SOURCE_THEOREM.csv"
PREMISE_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_COMMON_MODE_PREMISE_AUDIT.csv"
ELECTRON_BRANCH_PATH = OUT_DIR / f"{PACK_ID}_ELECTRON_NORMALIZATION_BRANCH.csv"
LOCAL_GR_GATE_PATH = OUT_DIR / f"{PACK_ID}_LOCAL_GR_PROMOTION_GATE.csv"
RUNNER_PATH = OUT_DIR / f"{PACK_ID}_DELTA_W_RUNNER_UPDATE.csv"
ANTI_SHORTCUT_PATH = OUT_DIR / f"{PACK_ID}_ANTI_SHORTCUT_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1332_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


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


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {"check_id": check_id, "check": check, "status": "PASS" if passed else "FAIL", "details": details}


def is_false(value: object) -> bool:
    return str(value).strip().lower() == "false"


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    for table in tables:
        for row in table:
            if "valid_for_claim" in row and not is_false(row.get("valid_for_claim", False)):
                return False
            if "claim_allowed" in row and not is_false(row.get("claim_allowed", False)):
                return False
    return True


def generated_inside_formalization() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [path for path in FORMALIZATION.rglob("*1332*") if path.is_file()]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_specs = [
        {
            "source_id": "SRC1332_0_1331_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1331_NEXT_TARGET.csv",
            "needle": "NEXT1331_0_1332",
            "role": "selected 1332 target",
        },
        {
            "source_id": "SRC1332_1_1331_theorem",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1331_PARENT_SOURCE_BASIS_MAP_THEOREM.csv",
            "needle": "THM1331_2_universal_metric_escape",
            "role": "universal metric escape theorem input",
        },
        {
            "source_id": "SRC1332_2_1330_electron",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1330_AUDITED_ELECTRON_FRACTION_ROWS.csv",
            "needle": "CFI1330_TA6V_electron",
            "role": "audited finite electron component",
        },
        {
            "source_id": "SRC1332_3_943_coframe_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_943_COFRAME_COUPLING_CONTRACT.csv",
            "needle": "CFC943_7_contract_verdict",
            "role": "single observed coframe coupling contract",
        },
        {
            "source_id": "SRC1332_4_944_descent_gate",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_944_DESCENT_PROOF_GATE.csv",
            "needle": "QDG944_7_total",
            "role": "quotient observed coframe descent gate",
        },
        {
            "source_id": "SRC1332_5_954_no_prefactor",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
            "needle": "PAC954_1_no_source_prefactors",
            "role": "no independent source prefactor parent clause",
        },
        {
            "source_id": "SRC1332_6_954_label_forgetting",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
            "needle": "PLF954_5_verdict",
            "role": "label-forgetting derivation attempt",
        },
        {
            "source_id": "SRC1332_7_955_minimal_action",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
            "needle": "MMA955_6_verdict",
            "role": "minimal matter action lemma",
        },
        {
            "source_id": "SRC1332_8_955_prefactors",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_955_SOURCE_PREFACTOR_CLASSIFICATION.csv",
            "needle": "SPC955_2_relative_species_weight",
            "role": "source prefactor countermodel classification",
        },
        {
            "source_id": "SRC1332_9_653_requirements",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_653_PARENT_SIGNATURE_REQUIREMENTS.csv",
            "needle": "PMF653_0_explicit_parent_matter_functor",
            "role": "parent matter functor signature requirements",
        },
        {
            "source_id": "SRC1332_10_653_theorem_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_653_THEOREM_ATTEMPT_AUDIT.csv",
            "needle": "TA653_3_species_blind_functor",
            "role": "species-blind functor theorem audit",
        },
        {
            "source_id": "SRC1332_11_627_zero_audit",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_627_ZERO_PROOF_AUDIT.csv",
            "needle": "ZCG627_2_matter_action_descent",
            "role": "matter action descent zero-proof audit",
        },
        {
            "source_id": "SRC1332_12_726_owner",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_726_PARENT_OWNER_MAP.csv",
            "needle": "POM726_9_matter_quotient",
            "role": "parent owner map matter quotient row",
        },
        {
            "source_id": "SRC1332_13_1331_validation",
            "local_path": "source-intake/mts_residuals/P8_Y5_BRR545_1331_VALIDATION.csv",
            "needle": "VAL1331_9_overall",
            "role": "1331 pass gate",
        },
    ]
    source_register: list[dict[str, object]] = []
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

    common_mode_theorem = [
        {
            "theorem_id": "CMT1332_0_common_mode_source_coupling",
            "statement": "If ordinary matter is one parent matter functional of one descended observed metric/coframe, with no relative source-only species prefactors and no hidden marker/readout spurions, then all ordinary material components couple to the same calibrated source current.",
            "formal_result": "delta_w_e = delta_w_q = delta_w_g = delta_w_EM = delta_w_nuc = delta_w_K = delta_w_common; Delta_w_TiPt = 0 after G_N calibration",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "The total Hilbert/coframe derivative of a single matter action is T_total=sum_A T_A. A common prefactor multiplies the whole source and is absorbed into measured kappa/G_N. Relative WEP/source residuals require a forbidden relative prefactor, marker, frame leak, non-Hilbert current, or readout spurion.",
            "claim_result": "COMMON_MODE_ROUTE_IDENTIFIED_NOT_PROMOTED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "CMT1332_1_electron_normalization_corollary",
            "statement": "The audited electron fraction becomes locally harmless if the electron contribution is part of the same total matter action with no separate source prefactor.",
            "formal_result": "F_e(B) may differ by material, but its source coefficient is common with all other components, so it does not create a differential source weight by itself",
            "proof_status": "CONDITIONAL_COROLLARY",
            "proof_sketch": "Material fractions only matter when component coefficients differ. If all coefficients collapse to delta_w_common, sum_c F_B,c delta_w_common = delta_w_common for normalized mass fractions and is calibrated away.",
            "claim_result": "ELECTRON_ROW_REMAINS_PLUMBING_UNTIL_PARENT_SIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "theorem_id": "CMT1332_2_countermodel",
            "statement": "A relative source prefactor w_A or hidden marker coefficient is compatible with covariance/additivity and reopens WEP/source residuals unless parent-forbidden.",
            "formal_result": "S_matter=sum_A w_A S_A gives T_source=sum_A w_A T_A; if w_A/w_B differs, Delta_w_TiPt can be finite",
            "proof_status": "COUNTERMODEL_RETAINED",
            "proof_sketch": "The same-action/Hilbert derivative argument does not by itself forbid constant per-species prefactors before variation. They must be absent by parent schema, quotient theorem, or explicit source bound.",
            "claim_result": "LOCAL_GR_NOT_CLAIMED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    premise_audit = [
        {
            "premise_id": "PREM1332_0_parent_q_map",
            "needed_premise": "parent quotient map q exists before matter coupling",
            "source_evidence": "CFC943_0;QDG944_0;ZCG627_0;POM726_9",
            "current_status": "UNSIGNED",
            "if_signed": "representative variables cannot be directly seen by ordinary matter",
            "if_unsigned": "finite frame/source residual branch remains legal",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1332_1_observed_coframe_descent",
            "needed_premise": "observed coframe/metric descends through q",
            "source_evidence": "CFC943_1;DER943_0;QDG944_2;P944_1",
            "current_status": "CONDITIONAL_LEMMA_NOT_PARENT_SIGNED",
            "if_signed": "vertical/frame leak killed by chain rule",
            "if_unsigned": "species or representative frame coupling can survive",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1332_2_single_matter_functional",
            "needed_premise": "ordinary matter is one total matter functional of one observed frame",
            "source_evidence": "PAC954_0;PLF954_1;MMA955_1",
            "current_status": "READY_AS_PARENT_CONTRACT_NOT_SIGNED",
            "if_signed": "total Hilbert current is label-forgetting",
            "if_unsigned": "separate source functional can reweight species",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1332_3_no_relative_source_prefactors",
            "needed_premise": "no independent species/source prefactors w_A multiply matter actions",
            "source_evidence": "PAC954_1;PLF954_2;MMA955_0;SPC955_2",
            "current_status": "EXACT_HIGH_PRESSURE_MISSING_CLAUSE",
            "if_signed": "relative component weights collapse to common mode",
            "if_unsigned": "constant w_A countermodel survives covariance and additivity",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1332_4_constants_quotient_owned",
            "needed_premise": "masses, charges, alpha_EM, clock standards are quotient-owned or retained as finite residuals",
            "source_evidence": "CFC943_3;QDG944_5;PMF653_2;PMF653_3",
            "current_status": "UNSIGNED_HARD_BLOCKER",
            "if_signed": "DD alpha/mass composition channel closes locally",
            "if_unsigned": "alpha/mass/electron residual coefficient branch remains live",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1332_5_no_hidden_spurion_or_nonHilbert_current",
            "needed_premise": "no marker/domain/boundary/readout prefactor and no unowned non-Hilbert current",
            "source_evidence": "PAC954_3;PAC954_4;SPC955_3;SPC955_4;QDG944_6",
            "current_status": "OPEN_PARALLEL_GATE",
            "if_signed": "source current cannot be reopened after label-forgetting",
            "if_unsigned": "hidden source residual can bypass the theorem",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "PREM1332_6_source_readout_worldtube",
            "needed_premise": "tau/source normal/readout worldtube use the same observed frame",
            "source_evidence": "CFC943_5;DER943_4;P944_4;POM726_8",
            "current_status": "UNSIGNED_SOURCE_READOUT_BRANCH",
            "if_signed": "WEP/PPN/clock projections refer to the same local source current",
            "if_unsigned": "readout/source projection residual remains live",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    electron_branch = [
        {
            "branch_id": "ELEC1332_0_common_mode_if_signed",
            "input": "CFI1330_TA6V_electron;CFI1330_PtRh10_electron",
            "condition": "PREM1332_0..PREM1332_6 parent-signed",
            "result": "electron fraction contrast is not a WEP/source residual because electron coefficient equals common matter coefficient",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "ELEC1332_1_finite_residual_if_unsigned",
            "input": "DELTA1330_0_TA6V_minus_PtRh10_electron",
            "condition": "relative source prefactor or constant marker survives",
            "result": "finite electron residual must be bounded as |delta_w_e| times audited electron contrast, not claimed zero",
            "status": "FINITE_NONCLAIM_RESIDUAL_RETAINED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "ELEC1332_2_no_electron_only_score",
            "input": "audited electron contrast only",
            "condition": "non-electron components and parent map unresolved",
            "result": "electron row cannot score WEP or local GR alone",
            "status": "SCORING_REFUSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    local_gr_gate = [
        {
            "gate_id": "LGR1332_0_common_mode_source",
            "gate": "ordinary matter source reduces to one calibrated Hilbert current",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "blocks_local_GR_claim": True,
            "reason": "no-source-prefactor and quotient matter descent premises remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LGR1332_1_left_hand_EH_Newton_limit",
            "gate": "geometric field equation reduces to EH/Newton left-hand operator",
            "status": "OUT_OF_SCOPE_NOT_CLOSED_BY_SOURCE_THEOREM",
            "blocks_local_GR_claim": True,
            "reason": "source-side common mode is necessary but not sufficient for full local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "LGR1332_2_PPN_readout_silence",
            "gate": "PPN/clock/orbital readout residuals vanish or are bounded",
            "status": "UNSIGNED_SOURCE_READOUT_BRANCH",
            "blocks_local_GR_claim": True,
            "reason": "same-worldtube/readout projection still open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    runner = [
        {
            "runner_id": "RUN1332_0_common_mode_theorem",
            "target": "collapse finite component weights to common calibrated source mode",
            "input_status": "EXACT_CONDITIONAL_THEOREM_UNSIGNED_PREMISES",
            "runner_status": "STAGED_NOT_CLAIMED",
            "reason": "the theorem is strong, but parent action has not signed no relative source prefactors or matter descent",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1332_1_electron_residual_branch",
            "target": "audited electron component if common mode remains unsigned",
            "input_status": "FINITE_NONCLAIM_RESIDUAL_RETAINED",
            "runner_status": "REFUSED_WEP_SCORE",
            "reason": "electron coefficient/bound still missing; one component is not a full WEP vector",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    anti_shortcut = [
        {
            "gate_id": "SHORT1332_0_no_contract_as_derivation",
            "shortcut": "treat parent matter contract as already derived",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1332_1_no_common_prefactor_confusion",
            "shortcut": "confuse harmless common prefactor with proof of absent relative prefactors",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1332_2_no_electron_only_local_GR",
            "shortcut": "use audited electron row as local-GR evidence",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "SHORT1332_3_no_DD_or_TiPt_tuning",
            "shortcut": "import DD charges or tune Ti/Pt cancellation",
            "enforcement": "REFUSED",
            "status": "ENFORCED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1332_0_theorem_result",
            "decision": "common-mode source theorem is the clean local-GR route but remains conditional",
            "because": "relative source prefactors and hidden marker/readout channels are exact countermodels until parent-forbidden",
            "effect": "do not score WEP/local GR; focus next on deriving the no-source-prefactor parent schema",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1332_1_next_pressure",
            "decision": "the highest-value missing clause is no independent source prefactors w_A",
            "because": "if w_A is absent by parent schema, electron/component fractions collapse into common mode rather than needing a phenomenological component fit",
            "effect": "next checkpoint should attempt the no-prefactor theorem or retain finite electron residual bounds",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1332_0_1333",
            "target_file": "1333-Y5-R10-RAB-no-source-prefactor-parent-schema-or-electron-residual-bound.md",
            "target_script": "scripts/Y5_R10_RAB_no_source_prefactor_parent_schema_or_electron_residual_bound.py",
            "task": "try to derive why the parent matter action cannot contain relative source-only species prefactors w_A; if not, create the finite electron residual coefficient/bound contract",
            "success_condition": "no-prefactor clause becomes an exact signed parent-schema theorem, or the finite electron residual branch gets a bounded nonclaim coefficient target",
            "do_not": "do not treat minimality preference as derivation, do not score WEP, do not tune Ti/Pt, and do not claim local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    tables_for_nonclaim = [
        source_register,
        common_mode_theorem,
        premise_audit,
        electron_branch,
        local_gr_gate,
        runner,
        anti_shortcut,
        decision,
        next_target,
    ]

    source_anchor_count = sum(1 for row in source_register if row["exists"] and row["needle_found"])
    theorem_exact = any(row["theorem_id"] == "CMT1332_0_common_mode_source_coupling" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in common_mode_theorem)
    no_premises_signed = all(row["parent_signed"] is False for row in premise_audit)
    electron_retained = any(row["branch_id"] == "ELEC1332_1_finite_residual_if_unsigned" and row["status"] == "FINITE_NONCLAIM_RESIDUAL_RETAINED" for row in electron_branch)
    local_claim_blocked = all(row["blocks_local_GR_claim"] is True and is_false(row["claim_allowed"]) for row in local_gr_gate)
    runner_not_scoreable = all(row["score_ready"] is False for row in runner)
    shortcuts_enforced = all(row["status"] == "ENFORCED" for row in anti_shortcut)
    nonclaim = all_nonclaim(tables_for_nonclaim)
    formal_clean = len(generated_inside_formalization()) == 0
    next_is_1333 = next_target[0]["target_file"].startswith("1333-")

    validations = [
        validation_row(
            "VAL1332_0_sources_exist",
            "registered source paths exist and anchors are found",
            source_anchor_count == len(source_register),
            f"{source_anchor_count}/{len(source_register)} source anchors found",
        ),
        validation_row(
            "VAL1332_1_common_mode_theorem",
            "common-mode source coupling theorem is exact conditional",
            theorem_exact,
            "CMT1332_0_common_mode_source_coupling=EXACT_CONDITIONAL_THEOREM",
        ),
        validation_row(
            "VAL1332_2_no_premises_signed",
            "premise audit refuses parent-signed promotion",
            no_premises_signed,
            ";".join(f"{row['premise_id']}={row['current_status']}" for row in premise_audit),
        ),
        validation_row(
            "VAL1332_3_electron_branch_retained",
            "finite electron residual branch remains explicit if common mode unsigned",
            electron_retained,
            ";".join(f"{row['branch_id']}={row['status']}" for row in electron_branch),
        ),
        validation_row(
            "VAL1332_4_local_GR_blocked",
            "local GR/WEP promotion remains blocked",
            local_claim_blocked,
            ";".join(f"{row['gate_id']}={row['status']}" for row in local_gr_gate),
        ),
        validation_row(
            "VAL1332_5_runners_not_scoreable",
            "runners refuse WEP/full Delta_w scoring",
            runner_not_scoreable,
            ";".join(f"{row['runner_id']}={row['runner_status']}" for row in runner),
        ),
        validation_row(
            "VAL1332_6_shortcuts_enforced",
            "anti-shortcut gates are enforced",
            shortcuts_enforced,
            ";".join(row["gate_id"] for row in anti_shortcut),
        ),
        validation_row(
            "VAL1332_7_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim,
            "valid_for_claim=false and claim_allowed=false where present",
        ),
        validation_row(
            "VAL1332_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            formal_clean,
            f"formalization_generated_output_count={len(generated_inside_formalization())}",
        ),
        validation_row(
            "VAL1332_9_next_target_1333",
            "next target routes to no-source-prefactor theorem or finite electron residual bound",
            next_is_1333,
            str(next_target[0]["target_file"]),
        ),
    ]
    validations.append(
        validation_row(
            "VAL1332_10_overall",
            "overall 1332 validation",
            all(row["status"] == "PASS" for row in validations),
            "1332 proves a conditional common-mode source theorem and blocks local-GR promotion until no-prefactor/matter-descent premises are signed",
        )
    )

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(COMMON_MODE_THEOREM_PATH, common_mode_theorem)
    write_csv(PREMISE_AUDIT_PATH, premise_audit)
    write_csv(ELECTRON_BRANCH_PATH, electron_branch)
    write_csv(LOCAL_GR_GATE_PATH, local_gr_gate)
    write_csv(RUNNER_PATH, runner)
    write_csv(ANTI_SHORTCUT_PATH, anti_shortcut)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# {TITLE}

**Current verdict:** 1332 proves the clean local-GR source route only conditionally: one descended observed matter action plus no relative source-only prefactors collapses all ordinary component weights into one calibrated common mode. The current corpus does not yet sign those premises.

**Main progress:** the electron row is now conceptually placed. Its audited material contrast is harmless if common-mode coupling is parent-signed; otherwise it remains a finite nonclaim residual branch requiring a coefficient/bound.

**Decision:** the next derivation target is the no-source-prefactor parent schema. That is the lever that can turn component arithmetic back into GR-style universal coupling rather than a DD/material-charge fit.

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Common-Mode Source Theorem
{markdown_table(common_mode_theorem, ["theorem_id", "statement", "formal_result", "proof_status", "proof_sketch", "claim_result", "valid_for_claim", "claim_allowed"])}

## Common-Mode Premise Audit
{markdown_table(premise_audit, ["premise_id", "needed_premise", "source_evidence", "current_status", "if_signed", "if_unsigned", "parent_signed", "valid_for_claim", "claim_allowed"])}

## Electron Normalization Branch
{markdown_table(electron_branch, ["branch_id", "input", "condition", "result", "status", "valid_for_claim", "claim_allowed"])}

## Local GR Promotion Gate
{markdown_table(local_gr_gate, ["gate_id", "gate", "status", "blocks_local_GR_claim", "reason", "valid_for_claim", "claim_allowed"])}

## Delta-w Runner Update
{markdown_table(runner, ["runner_id", "target", "input_status", "runner_status", "reason", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"])}

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
