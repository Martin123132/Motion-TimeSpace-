from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1602"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1602-Y5-R2FR-C_EP-source-coefficient-or-common-mode-zero-theorem.md"

SOURCE_FILES = {
    "1601_doc": ROOT / "1601-Y5-R2FR-EP-template-alignment-lemma-or-CMSM-browser-capture.md",
    "1601_validation": OUT / "P8_Y5_BRR545_1601_VALIDATION.csv",
    "1601_lemma": OUT / "P8_Y5_PARENT_QLOC_1601_EP_TEMPLATE_ALIGNMENT_LEMMA.csv",
    "1601_contract": OUT / "P8_Y5_PARENT_QLOC_1601_EP_ALIGNMENT_AMPLITUDE_CONTRACT.csv",
    "1601_counter": OUT / "P8_Y5_PARENT_QLOC_1601_EP_TEMPLATE_COUNTERMODEL.csv",
    "1601_next": OUT / "P8_Y5_PARENT_QLOC_1601_NEXT_TARGET.csv",
    "1445_audit": OUT / "P8_Y5_R10_1445_C_PARENT_COUPLING_THEOREM_AUDIT.csv",
    "1484_derivation": OUT / "P8_Y5_R10_1484_C_PARENT_COUPLING_DERIVATION_ATTEMPT.csv",
    "1449_zero": OUT / "P8_Y5_R10_1449_C_PARENT_ZERO_DERIVATION_ATTEMPT.csv",
    "1485_refusal": OUT / "P8_Y5_R10_1485_C_PARENT_IMPORT_REFUSAL.csv",
    "1593_zero": OUT / "P8_Y5_PARENT_QLOC_1593_CANONICAL_COUPLING_ZERO_THEOREM_ATTEMPT.csv",
    "1597_zero": OUT / "P8_Y5_PARENT_QLOC_1597_COUPLING_ZERO_PROOF_AUDIT.csv",
    "C_parent_rows": COEFF / "C_parent.csv",
    "C_parent_zero": COEFF / "C_parent_WEP_slot_zero_attempt.csv",
}

NEEDLES = {
    "1601_doc": ["NEXT_1602_CEP_SOURCE_COEFFICIENT_OR_COMMON_MODE_ZERO_THEOREM", "C_EP"],
    "1601_validation": ["VAL1601_OVERALL", "PASS"],
    "1601_lemma": ["EPA1601_3_verdict", "EP_TEMPLATE_ALIGNMENT_NOT_PROVEN"],
    "1601_contract": ["EAC1601_0_C_EP", "MISSING_PARENT_C_EP"],
    "1601_counter": ["EPC1601_0_common_mode_only", "C_EP=0"],
    "1601_next": ["1602-Y5-R2FR-C_EP-source-coefficient-or-common-mode-zero-theorem", "C_EP"],
    "1445_audit": ["CTA1445_0", "OPEN_DERIVATION_GAP"],
    "1484_derivation": ["CPD1484_5_verdict", "NOT_CLOSED"],
    "1449_zero": ["DZ1449_4_source_weight_term", "COUNTERMODEL_SURVIVES"],
    "1485_refusal": ["IMP1485_4_bound_inversion", "REFUSED_BOUND_INVERSION_FORBIDDEN"],
    "1593_zero": ["ZTH1593_8_verdict", "ZERO_THEOREM_NOT_CLOSED_FINITE_BETA_ROWS_REQUIRED"],
    "1597_zero": ["CZP1597_2_coupling_zero_verdict", "FINITE_PRODUCT_BRANCH_REMAINS_OPEN"],
    "C_parent_rows": ["CP1430_6_verdict", "NOT_SCOREABLE"],
    "C_parent_zero": ["CZ1438_5_zero_certificate", "NOT_CLOSED"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1602_SOURCE_REGISTER.csv"
CEP_FACTORIZATION = OUT / "P8_Y5_PARENT_QLOC_1602_CEP_FACTORIZATION_THEOREM.csv"
CEP_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1602_CEP_SOURCE_COEFFICIENT_AUDIT.csv"
COMMON_ZERO = OUT / "P8_Y5_PARENT_QLOC_1602_COMMON_MODE_ZERO_THEOREM_ATTEMPT.csv"
CEP_COUNTERMODELS = OUT / "P8_Y5_PARENT_QLOC_1602_CEP_COUNTERMODELS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1602_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1602_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1602_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1602_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1602_VALIDATION.csv"

COPY_TARGETS = {
    CEP_FACTORIZATION: [
        QUARANTINE / "CEP_FACTORIZATION_THEOREM_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CEP_factorization_theorem_nonclaim_1602.csv",
    ],
    CEP_AUDIT: [
        QUARANTINE / "CEP_SOURCE_COEFFICIENT_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CEP_source_coefficient_audit_nonclaim_1602.csv",
    ],
    COMMON_ZERO: [
        QUARANTINE / "COMMON_MODE_ZERO_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_common_mode_zero_theorem_attempt_nonclaim_1602.csv",
    ],
    CEP_COUNTERMODELS: [
        QUARANTINE / "CEP_COUNTERMODELS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CEP_countermodels_nonclaim_1602.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1602.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_id, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_id]
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1602_{index}_{source_id}",
                "source_path": path.relative_to(ROOT).as_posix() if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1602_C_EP_source_or_common_mode_zero_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def cep_factorization_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "factorization_id": "CEF1602_0_definition",
            "statement": "C_EP is the coefficient of the MICROSCOPE EP-template component in V_MTS",
            "formula": "V_MTS = C_EP T_EP + V_perp + V_corr",
            "status": "DEFINITION_FROM_1601",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factorization_id": "CEF1602_1_product_form",
            "statement": "in the finite source branch, C_EP factorizes into parent coefficient x material contrast x Earth/source EP component x readout phase",
            "formula": "C_EP = C_parent,WEP * DeltaR_TiPt * S_Earth,EP * P_readout + correction/normalization terms",
            "status": "CONDITIONAL_FACTORIZATION_DERIVED",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factorization_id": "CEF1602_2_nonzero_condition",
            "statement": "C_EP is nonzero only if each finite factor is nonzero and no signed correction/common-mode cancellation kills the EP component",
            "formula": "C_EP != 0 requires C_parent,WEP !=0, DeltaR_TiPt !=0, S_Earth,EP !=0, P_readout !=0 and no cancellation",
            "status": "CONDITIONAL_NONZERO_RULE",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "factorization_id": "CEF1602_3_zero_condition",
            "statement": "C_EP is zero if the branch is purely common-mode before readout or if ordinary matter has no relative source/action weight",
            "formula": "common source normalization only => C_EP=0 in WEP differential channel",
            "status": "CONDITIONAL_COMMON_MODE_ZERO_RULE",
            "claim_allowed": False,
        },
    ]


def cep_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "CEA1602_0_C_parent_WEP",
            "factor": "C_parent,WEP",
            "needed_for": "finite nonzero C_EP",
            "current_status": "MISSING_DERIVED_OR_SOURCE_BACKED_COEFFICIENT",
            "evidence": "CPD1484_5 verdict NOT_CLOSED; IMP1485 finite source missing",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "CEA1602_1_material_contrast",
            "factor": "DeltaR_TiPt",
            "needed_for": "differential Ti/Pt WEP channel",
            "current_status": "MISSING_PARENT_MATERIAL_RESPONSE",
            "evidence": "C_parent WEP zero attempt leaves full material tensor unsigned",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "CEA1602_2_source_EP_component",
            "factor": "S_Earth,EP",
            "needed_for": "template-aligned source response",
            "current_status": "MISSING_PARENT_SOURCE_EP_COMPONENT",
            "evidence": "source weight term countermodel survives in DZ1449_4",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "CEA1602_3_readout_phase",
            "factor": "P_readout",
            "needed_for": "nonzero projection into MICROSCOPE EP channel",
            "current_status": "MISSING_CMSM_READOUT_OR_PARENT_PHASE_THEOREM",
            "evidence": "1601 quadrature/correction countermodels remain live",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "CEA1602_4_verdict",
            "factor": "C_EP",
            "needed_for": "EP-template alignment margin",
            "current_status": "C_EP_NOT_DERIVED_OR_ZERO_CERTIFIED",
            "evidence": "all finite and zero routes remain nonclaim",
            "claim_allowed": False,
        },
    ]


def common_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "CMZ1602_0_universal_action_measure",
            "required_statement": "all ordinary matter sectors share one parent action measure and no species-specific pre-variation weights",
            "current_status": "UNSIGNED",
            "result": "CANNOT_SET_C_EP_ZERO",
            "blocking_gap": "w_A/source-action weights remain legal in current corpus",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "CMZ1602_1_source_label_forgetting",
            "required_statement": "Earth/source coupling enters only as common-mode source normalization and forgets Ti/Pt labels before readout",
            "current_status": "UNSIGNED",
            "result": "COMMON_MODE_ZERO_NOT_PROVEN",
            "blocking_gap": "source-label forgetting theorem missing; measured-G absorption guard forbids shortcut",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "CMZ1602_2_readout_silence",
            "required_statement": "boundary/readout/projector cannot reintroduce representative species coefficients",
            "current_status": "UNSIGNED",
            "result": "READOUT_LEAK_NOT_EXCLUDED",
            "blocking_gap": "official K_CMSM/readout arrays absent and parent readout theorem missing",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_id": "CMZ1602_3_verdict",
            "required_statement": "all common-mode clauses combine into C_EP=0 for WEP",
            "current_status": "COMMON_MODE_ZERO_THEOREM_NOT_CLOSED",
            "result": "FINITE_OR_ZERO_BRANCH_REMAINS_OPEN",
            "blocking_gap": "source-label forgetting is now the sharpest zero-route gap",
            "claim_allowed": False,
        },
    ]


def cep_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CEPC1602_0_finite_source_weight",
            "construction": "allow S_matter=sum_A w_A S_A with source/readout projection before variation",
            "math_result": "C_EP can be finite and composition-dependent",
            "blocked_claim": "common-mode zero theorem",
            "escape_condition": "derive no pre-variation source/action weights",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CEPC1602_1_common_mode_only",
            "construction": "source response renormalizes only common GM and never enters Ti/Pt difference",
            "math_result": "C_EP=0 while source response exists",
            "blocked_claim": "finite source response implies WEP signal",
            "escape_condition": "derive differential parent source coefficient",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CEPC1602_2_bound_inversion",
            "construction": "choose C_EP from MICROSCOPE bound after the fact",
            "math_result": "fits the bound but is not a parent derivation",
            "blocked_claim": "empirical bound as coefficient source",
            "escape_condition": "source C_EP independently from parent action or official data projection",
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1602_0_factorization",
            "acceptance_rule": "record C_EP product/zero alternatives",
            "input_state": "conditional factorization derived",
            "runner_result": "ACCEPT_CONDITIONAL_FACTORIZATION_ONLY",
            "effect": "C_EP target sharpened",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1602_1_finite_CEP",
            "acceptance_rule": "finite C_EP requires source-backed parent coefficient independent of MICROSCOPE bound",
            "input_state": "C_parent_WEP and material/source/readout factors missing",
            "runner_result": "REJECT_FINITE_CEP_CLAIM",
            "effect": "no EP alignment claim",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1602_2_common_zero",
            "acceptance_rule": "C_EP=0 requires parent-signed common-mode/source-label forgetting theorem",
            "input_state": "zero clauses unsigned",
            "runner_result": "REJECT_COMMON_MODE_ZERO_CLAIM",
            "effect": "cannot claim WEP-safe zero route",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1602_0_CEP_finite", "finite C_EP sourced", "parent coefficient/material/source/readout factors missing"),
        ("CG1602_1_CEP_zero", "C_EP=0 common-mode theorem", "source-label forgetting/readout silence unsigned"),
        ("CG1602_2_EP_alignment", "EP-template alignment proven", "C_EP route unresolved"),
        ("CG1602_3_WEP", "MTS passes MICROSCOPE/WEP", "product anchor only"),
        ("CG1602_4_local_GR", "derived local GR branch", "coupling/source branch unresolved"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": "BLOCKED",
            "reason": reason,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, reason in claims
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1602_0_progress",
            "decision": "C_EP_FACTORIZATION_DERIVED_CONDITIONALLY",
            "reason": "C_EP now decomposes into parent coefficient, material contrast, source EP component and readout phase",
            "next_action": "target source-label forgetting or finite C_EP source pack",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1602_1_blocker",
            "decision": "NEITHER_FINITE_NOR_ZERO_ROUTE_CLOSED",
            "reason": "finite route lacks source-backed parent coefficient; zero route lacks common-mode/source-label theorem",
            "next_action": "do not score WEP/local GR yet",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1602_2_next",
            "decision": "NEXT_1603_SOURCE_LABEL_FORGETTING_OR_FINITE_CEP_SOURCE_PACK",
            "reason": "source-label forgetting is the smallest zero-route gap; finite C_EP source pack is the matching nonzero route",
            "next_action": "derive source-label forgetting theorem or create strict finite C_EP source-pack validator",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1603-Y5-R2FR-source-label-forgetting-or-finite-C_EP-source-pack.md",
            "script": "scripts/Y5_R2FR_source_label_forgetting_or_finite_CEP_source_pack.py",
            "objective": "prove the parent source functor forgets Ti/Pt labels before readout, or build a strict source-backed finite C_EP intake validator",
            "success_condition": "parent-signed source-label forgetting theorem yielding C_EP=0, or finite C_EP row with source path, units, sign, branch and no bound inversion",
            "do_not": "do not fit C_EP from MICROSCOPE; do not claim WEP/local GR; do not use closure-only zero",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def csv_parses(paths: list[Path]) -> bool:
    try:
        for path in paths:
            read_csv(path)
    except Exception:
        return False
    return True


def no_claim_flags(paths: list[Path]) -> bool:
    truthy = {"true", "1", "yes", "y"}
    for path in paths:
        for row in read_csv(path):
            for field in ("score_ready", "valid_prediction_row", "claim_allowed"):
                if row.get(field, "").strip().lower() in truthy:
                    return False
    return True


def no_formalization_1602() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1602*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    factor = read_csv(CEP_FACTORIZATION)
    audit = read_csv(CEP_AUDIT)
    zero = read_csv(COMMON_ZERO)
    counter = read_csv(CEP_COUNTERMODELS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1602_0_sources_exist", all(row["exists"] == "True" or row["exists"] is True for row in sources), "all cited 1602 local source paths exist"),
        ("VAL1602_1_needles_found", all(row["needle_found"] == "True" or row["needle_found"] is True for row in sources), "all required 1602 source needles found"),
        ("VAL1602_2_factorization", any(row["factorization_id"] == "CEF1602_1_product_form" for row in factor), "C_EP product factorization recorded"),
        ("VAL1602_3_zero_condition", any(row["factorization_id"] == "CEF1602_3_zero_condition" for row in factor), "C_EP common-mode zero condition recorded"),
        ("VAL1602_4_CEP_audit_missing", any(row["audit_id"] == "CEA1602_4_verdict" and row["current_status"] == "C_EP_NOT_DERIVED_OR_ZERO_CERTIFIED" for row in audit), "C_EP remains neither derived nor zero certified"),
        ("VAL1602_5_common_zero_blocked", any(row["zero_id"] == "CMZ1602_3_verdict" and row["current_status"] == "COMMON_MODE_ZERO_THEOREM_NOT_CLOSED" for row in zero), "common-mode zero theorem remains blocked"),
        ("VAL1602_6_countermodels", len(counter) >= 3 and any(row["countermodel_id"] == "CEPC1602_2_bound_inversion" for row in counter), "C_EP countermodels recorded"),
        ("VAL1602_7_runner_refuses_both", any(row["runner_id"] == "RUN1602_1_finite_CEP" and row["runner_result"] == "REJECT_FINITE_CEP_CLAIM" for row in runner) and any(row["runner_id"] == "RUN1602_2_common_zero" and row["runner_result"] == "REJECT_COMMON_MODE_ZERO_CLAIM" for row in runner), "runner refuses finite and zero claims"),
        ("VAL1602_8_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1602 claim gates remain closed"),
        ("VAL1602_9_decision_next", any(row["decision"] == "NEXT_1603_SOURCE_LABEL_FORGETTING_OR_FINITE_CEP_SOURCE_PACK" for row in decisions), "decision selects 1603 source-label forgetting or finite C_EP source pack"),
        ("VAL1602_10_csv_parse", csv_parses(generated_csvs), "all generated 1602 CSVs parse"),
        ("VAL1602_11_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1602 rows are score-ready, prediction rows, or claim-allowed"),
        ("VAL1602_12_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1602_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1602_14_formalization_untouched", no_formalization_1602(), "no 1602 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if ok else "FAIL",
            "detail": detail,
        }
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1602_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1602 C_EP source coefficient or common-mode zero theorem validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    sources: list[dict[str, Any]],
    factor: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    zero: list[dict[str, Any]],
    counter: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1602 - R2/fR C_EP Source Coefficient Or Common-Mode Zero Theorem",
                "## Verdict\n"
                "- 1602 derives the conditional factorization `C_EP = C_parent,WEP * DeltaR_TiPt * S_Earth,EP * P_readout + corrections`.\n"
                "- This helps because the theory fork is now explicit: source a finite `C_EP`, or prove the WEP branch is common-mode/zero before readout.\n"
                "- Neither route closes: the finite route lacks a source-backed parent coefficient, and the zero route lacks source-label forgetting/readout silence.\n"
                "- The sharpest next object is the parent source-label-forgetting theorem, with a strict finite `C_EP` source-pack validator as the parallel nonzero route.\n"
                "- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## C_EP Factorization Theorem",
                md_table(factor, ["factorization_id", "statement", "formula", "status"]),
                "## C_EP Source Coefficient Audit",
                md_table(audit, ["audit_id", "factor", "needed_for", "current_status", "evidence"]),
                "## Common-Mode Zero Theorem Attempt",
                md_table(zero, ["zero_id", "required_statement", "current_status", "result", "blocking_gap"]),
                "## C_EP Countermodels",
                md_table(counter, ["countermodel_id", "construction", "math_result", "blocked_claim", "escape_condition"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    factor = cep_factorization_rows()
    audit = cep_audit_rows()
    zero = common_zero_rows()
    counter = cep_countermodel_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        CEP_FACTORIZATION,
        CEP_AUDIT,
        COMMON_ZERO,
        CEP_COUNTERMODELS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(CEP_FACTORIZATION, factor)
    write_csv(CEP_AUDIT, audit)
    write_csv(COMMON_ZERO, zero)
    write_csv(CEP_COUNTERMODELS, counter)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, factor, audit, zero, counter, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
