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
QUARANTINE = MICROSCOPE / "quarantine" / "1603"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1603-Y5-R2FR-source-label-forgetting-or-finite-C_EP-source-pack.md"

SOURCE_FILES = {
    "1602_doc": ROOT / "1602-Y5-R2FR-C_EP-source-coefficient-or-common-mode-zero-theorem.md",
    "1602_validation": OUT / "P8_Y5_BRR545_1602_VALIDATION.csv",
    "1602_zero": OUT / "P8_Y5_PARENT_QLOC_1602_COMMON_MODE_ZERO_THEOREM_ATTEMPT.csv",
    "1602_audit": OUT / "P8_Y5_PARENT_QLOC_1602_CEP_SOURCE_COEFFICIENT_AUDIT.csv",
    "1602_next": OUT / "P8_Y5_PARENT_QLOC_1602_NEXT_TARGET.csv",
    "1461_no_relative": OUT / "P8_Y5_R10_1461_NO_RELATIVE_SOURCE_LABEL_AUDIT.csv",
    "1461_counter": OUT / "P8_Y5_R10_1461_SOURCE_LABEL_COUNTERMODEL_AUDIT.csv",
    "1450_decision": OUT / "P8_Y5_R10_1450_C_PARENT_EVALUATION_DECISION.csv",
    "1443_search": OUT / "P8_Y5_R10_1443_C_PARENT_SOURCE_SEARCH_PLAN.csv",
    "1431_schema": OUT / "P8_Y5_R10_1431_C_PARENT_IMPORT_SCHEMA.csv",
    "1442_gates": OUT / "P8_Y5_R10_1442_C_PARENT_WEP_SLOT_IMPORT_GATES.csv",
    "1442_template": OUT / "P8_Y5_R10_1442_C_PARENT_WEP_SLOT_IMPORT_TEMPLATE.csv",
    "1485_refusal": OUT / "P8_Y5_R10_1485_C_PARENT_IMPORT_REFUSAL.csv",
    "coeff_decision": COEFF / "C_parent_WEP_source_label_decision_1450.csv",
}

NEEDLES = {
    "1602_doc": ["NEXT_1603_SOURCE_LABEL_FORGETTING_OR_FINITE_CEP_SOURCE_PACK", "source-label forgetting"],
    "1602_validation": ["VAL1602_OVERALL", "PASS"],
    "1602_zero": ["CMZ1602_3_verdict", "COMMON_MODE_ZERO_THEOREM_NOT_CLOSED"],
    "1602_audit": ["CEA1602_4_verdict", "C_EP_NOT_DERIVED_OR_ZERO_CERTIFIED"],
    "1602_next": ["1603-Y5-R2FR-source-label-forgetting-or-finite-C_EP-source-pack", "finite C_EP row"],
    "1461_no_relative": ["NRS1461_5_delta_q_zero_decision", "DELTA_Q_ZERO_NOT_PROMOTED"],
    "1461_counter": ["CM1461_4_readout_selector_reentry", "RETAIN_LIVE_NONCLAIM"],
    "1450_decision": ["DO_NOT_IMPORT_EPSILON_ZERO_OR_C_PARENT_WEP", "Hilbert-source route is mathematically sharp"],
    "1443_search": ["CPS1443_2_bound_inversion_forbidden", "FORBIDDEN"],
    "1431_schema": ["zero_certificate_status", "QT_ZERO_CLOSED"],
    "1442_gates": ["CPWG1442_6_no_absorption", "tau_eff=1 shortcuts cannot supply C_parent"],
    "1442_template": ["CP_WEP_TiPt_TEMPLATE", "TEMPLATE_ONLY_NOT_IMPORTABLE"],
    "1485_refusal": ["IMP1485_4_bound_inversion", "REFUSED_BOUND_INVERSION_FORBIDDEN"],
    "coeff_decision": ["EVAL1450_0_source_label", "DO_NOT_IMPORT_EPSILON_ZERO_OR_C_PARENT_WEP"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1603_SOURCE_REGISTER.csv"
LABEL_FORGETTING = OUT / "P8_Y5_PARENT_QLOC_1603_SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT.csv"
FINITE_SCHEMA = OUT / "P8_Y5_PARENT_QLOC_1603_FINITE_CEP_SOURCE_PACK_SCHEMA.csv"
FINITE_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_1603_FINITE_CEP_SOURCE_PACK_TEMPLATE.csv"
VALIDATOR_SPEC = OUT / "P8_Y5_PARENT_QLOC_1603_FINITE_CEP_VALIDATOR_SPEC.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1603_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1603_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1603_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1603_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1603_VALIDATION.csv"

COPY_TARGETS = {
    LABEL_FORGETTING: [
        QUARANTINE / "SOURCE_LABEL_FORGETTING_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_source_label_forgetting_theorem_attempt_nonclaim_1603.csv",
    ],
    FINITE_SCHEMA: [
        QUARANTINE / "FINITE_CEP_SOURCE_PACK_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_CEP_source_pack_schema_nonclaim_1603.csv",
    ],
    FINITE_TEMPLATE: [
        QUARANTINE / "FINITE_CEP_SOURCE_PACK_TEMPLATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_CEP_source_pack_template_nonclaim_1603.csv",
    ],
    VALIDATOR_SPEC: [
        QUARANTINE / "FINITE_CEP_VALIDATOR_SPEC_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_finite_CEP_validator_spec_nonclaim_1603.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1603.csv",
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
                "source_id": f"SRC1603_{index}_{source_id}",
                "source_path": path.relative_to(ROOT).as_posix() if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1603_source_label_forgetting_or_finite_CEP_source_pack_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def label_forgetting_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "SLF1603_0_source_functor_domain",
            "required_statement": "source functor domain is total stress/current, not labelled species stress pairs",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "countermodel": "relative w_A or labelled stress-pair source functor",
            "result": "CLAUSE_OPEN",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "SLF1603_1_common_measure_current",
            "required_statement": "one measure/action/current normalization for all ordinary matter sectors",
            "current_status": "MISSING_AXIOM_NOT_REDUCED",
            "countermodel": "species-dependent Jacobian/action weight",
            "result": "CLAUSE_OPEN",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "SLF1603_2_no_hidden_marker_hom",
            "required_statement": "hidden or MTS marker cannot feed source coefficients",
            "current_status": "MISSING_PARENT_SIGNATURE",
            "countermodel": "hidden marker source coefficient",
            "result": "CLAUSE_OPEN",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "SLF1603_3_nonHilbert_silence",
            "required_statement": "no non-Hilbert current bypasses total stress source",
            "current_status": "OPEN_PARALLEL_GATE",
            "countermodel": "J_src = kappa T_Hilbert + J_NH",
            "result": "CLAUSE_OPEN",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "SLF1603_4_readout_no_reentry",
            "required_statement": "downstream source-worldtube/readout kernels cannot recreate species labels",
            "current_status": "CONDITIONAL_SOURCE_FILES_MISSING",
            "countermodel": "readout selector reentry after variation",
            "result": "CLAUSE_OPEN",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "SLF1603_5_verdict",
            "required_statement": "all source-label forgetting clauses close together",
            "current_status": "SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "countermodel": "at least one live finite source-label route remains",
            "result": "C_EP_ZERO_NOT_CERTIFIED",
            "claim_allowed": False,
        },
    ]


def finite_schema_rows() -> list[dict[str, Any]]:
    fields = [
        ("schema_version", "FINITE_CEP_SOURCE_PACK_1603"),
        ("same_parent_branch_id", BRANCH_ID),
        ("coefficient_id", "unique row id"),
        ("quantity", "C_EP or declared factor C_parent_WEP|DeltaR_TiPt|S_Earth_EP|P_readout|correction_bound"),
        ("value", "finite numeric or DERIVED_ZERO with exact certificate"),
        ("uncertainty", "numeric uncertainty or exact theorem tag"),
        ("units", "declared dimensionless or SI/natural-unit conversion"),
        ("sign_convention", "TiPt body order, source sign and field convention"),
        ("basis", "MTS parent WEP basis, not DD-only comparator"),
        ("source_path", "local path, URL, DOI, or parent theorem path"),
        ("parent_status", "PARENT_DERIVED|SOURCE_BACKED_NUMERIC|DERIVED_ZERO"),
        ("zero_certificate_status", "QT_ZERO_CLOSED|NUMERIC_NONZERO|NOT_ZERO_CERTIFIED"),
        ("no_bound_inversion", "must be true"),
        ("no_tau_unity", "must be true"),
        ("valid_for_claim", "false until full branch scorepack passes"),
        ("claim_allowed", "false until WEP/local gates pass"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "schema_id": f"FCS1603_{index}_{field}",
            "field": field,
            "required_value_or_policy": policy,
            "claim_allowed": False,
        }
        for index, (field, policy) in enumerate(fields)
    ]


def finite_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "template_id": "FCT1603_0_C_EP_source_pack_template",
            "schema_version": "FINITE_CEP_SOURCE_PACK_1603",
            "coefficient_id": "C_EP_TEMPLATE",
            "quantity": "C_EP",
            "value": "MISSING_NUMERIC_OR_DERIVED_ZERO",
            "uncertainty": "MISSING_UNCERTAINTY_OR_EXACT",
            "units": "MISSING_UNITS",
            "sign_convention": "MISSING_TiPt_EP_TEMPLATE_SIGN",
            "basis": "MISSING_MTS_PARENT_WEP_BASIS",
            "source_path": "MISSING_PARENT_THEOREM_OR_SOURCE",
            "parent_status": "MISSING_PARENT_DERIVED_OR_SOURCE_BACKED_NUMERIC",
            "zero_certificate_status": "NOT_ZERO_CERTIFIED",
            "no_bound_inversion": False,
            "no_tau_unity": False,
            "parser_status": "TEMPLATE_ONLY_NOT_IMPORTABLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validator_spec_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "validator_id": "FCV1603_0_required_fields",
            "rule": "all finite C_EP source-pack fields must be present and nonempty",
            "failure_status": "REJECT_MISSING_FIELDS",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "validator_id": "FCV1603_1_branch_basis",
            "rule": "same_parent_branch_id and MTS parent WEP basis must match branch",
            "failure_status": "REJECT_BRANCH_OR_BASIS_MISMATCH",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "validator_id": "FCV1603_2_value_policy",
            "rule": "value must be finite numeric or DERIVED_ZERO; MISSING/PENDING/PLACEHOLDER/TEMPLATE forbidden",
            "failure_status": "REJECT_BAD_VALUE",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "validator_id": "FCV1603_3_provenance",
            "rule": "source_path must exist or be a real URL/DOI and cannot cite MICROSCOPE bound as coefficient source",
            "failure_status": "REJECT_BAD_PROVENANCE_OR_BOUND_INVERSION",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "validator_id": "FCV1603_4_zero_policy",
            "rule": "DERIVED_ZERO requires parent-signed zero certificate; closure-only zero rejected",
            "failure_status": "REJECT_CLOSURE_ONLY_ZERO",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "validator_id": "FCV1603_5_claim_policy",
            "rule": "validator may accept source-pack rows for quarantine, but claim_allowed remains false until WEP/local gates pass",
            "failure_status": "NONCLAIM_ACCEPT_ONLY",
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1603_0_label_forgetting",
            "acceptance_rule": "C_EP=0 requires all source-label forgetting clauses closed",
            "input_state": "five clauses remain open",
            "runner_result": "REJECT_SOURCE_LABEL_FORGETTING_CLAIM",
            "effect": "zero route remains unclaimed",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1603_1_finite_pack",
            "acceptance_rule": "finite C_EP rows must pass strict source-pack validator",
            "input_state": "template only; no finite row supplied",
            "runner_result": "NO_FINITE_CEP_ROW_ACCEPTED",
            "effect": "finite route remains input-ready but empty",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1603_2_bound_shortcut",
            "acceptance_rule": "MICROSCOPE bound and tau_eff=1 cannot supply C_EP",
            "input_state": "shortcuts explicitly forbidden",
            "runner_result": "REJECT_BOUND_INVERSION_AND_TAU_UNITY",
            "effect": "keeps coefficient route noncircular",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1603_0_label_forgetting", "source-label forgetting theorem", "five source-label clauses remain open"),
        ("CG1603_1_finite_CEP", "finite C_EP source pack accepted", "template only; no source-backed row"),
        ("CG1603_2_CEP", "C_EP finite or zero resolved", "both routes remain open"),
        ("CG1603_3_WEP", "MTS passes MICROSCOPE/WEP", "product anchor only"),
        ("CG1603_4_local_GR", "derived local GR branch", "source/coupling branch unresolved"),
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
            "decision_id": "DEC1603_0_zero_route",
            "decision": "SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "reason": "relative weights, species measure, hidden markers, non-Hilbert currents and readout reentry survive",
            "next_action": "attack no-w_A/source-action-weight clause first",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1603_1_finite_route",
            "decision": "FINITE_CEP_VALIDATOR_READY_NO_ROW",
            "reason": "strict schema/template/validator exists, but no finite source-backed C_EP row is present",
            "next_action": "only accept future finite row with source, units, sign, branch and no bound inversion",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1603_2_next",
            "decision": "NEXT_1604_NO_WA_SOURCE_ACTION_WEIGHT_OR_FINITE_ROW_SEARCH",
            "reason": "no-w_A is the sharpest zero-route clause and finite row search is the matching nonzero route",
            "next_action": "derive no pre-variation source/action weights or search for source-backed finite C_EP row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1604-Y5-R2FR-no-wA-source-action-weight-or-finite-C_EP-row-search.md",
            "script": "scripts/Y5_R2FR_no_wA_source_action_weight_or_finite_CEP_row_search.py",
            "objective": "derive no pre-variation source/action weights for ordinary matter, or search/import-test a source-backed finite C_EP row against the 1603 validator",
            "success_condition": "parent-signed no-w_A theorem closing the leading source-label route, or a validator-readable finite C_EP row that remains nonclaim until WEP gates pass",
            "do_not": "do not use closure-only zero, bound inversion, DD-only proxy, tau_eff=1, or public/local-GR claims",
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


def no_formalization_1603() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1603*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    label = read_csv(LABEL_FORGETTING)
    schema = read_csv(FINITE_SCHEMA)
    template = read_csv(FINITE_TEMPLATE)
    validator = read_csv(VALIDATOR_SPEC)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1603_0_sources_exist", all(row["exists"] == "True" or row["exists"] is True for row in sources), "all cited 1603 local source paths exist"),
        ("VAL1603_1_needles_found", all(row["needle_found"] == "True" or row["needle_found"] is True for row in sources), "all required 1603 source needles found"),
        ("VAL1603_2_label_verdict", any(row["clause_id"] == "SLF1603_5_verdict" and row["result"] == "C_EP_ZERO_NOT_CERTIFIED" for row in label), "source-label forgetting remains unproved"),
        ("VAL1603_3_schema_written", len(schema) >= 10 and any(row["field"] == "no_bound_inversion" for row in schema), "finite C_EP schema written"),
        ("VAL1603_4_template_nonimportable", any(row["template_id"] == "FCT1603_0_C_EP_source_pack_template" and row["parser_status"] == "TEMPLATE_ONLY_NOT_IMPORTABLE" for row in template), "finite C_EP template remains nonimportable"),
        ("VAL1603_5_validator_rules", len(validator) >= 6 and any(row["validator_id"] == "FCV1603_4_zero_policy" for row in validator), "finite C_EP validator rules written"),
        ("VAL1603_6_runner_refuses_routes", any(row["runner_id"] == "RUN1603_0_label_forgetting" and row["runner_result"] == "REJECT_SOURCE_LABEL_FORGETTING_CLAIM" for row in runner) and any(row["runner_id"] == "RUN1603_1_finite_pack" and row["runner_result"] == "NO_FINITE_CEP_ROW_ACCEPTED" for row in runner), "runner refuses zero claim and finite claim"),
        ("VAL1603_7_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1603 claim gates remain closed"),
        ("VAL1603_8_decision_next", any(row["decision"] == "NEXT_1604_NO_WA_SOURCE_ACTION_WEIGHT_OR_FINITE_ROW_SEARCH" for row in decisions), "decision selects 1604 no-w_A or finite row search"),
        ("VAL1603_9_csv_parse", csv_parses(generated_csvs), "all generated 1603 CSVs parse"),
        ("VAL1603_10_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1603 rows are score-ready, prediction rows, or claim-allowed"),
        ("VAL1603_11_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1603_12_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1603_13_formalization_untouched", no_formalization_1603(), "no 1603 outputs found under formalization-workbench"),
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
            "check_id": "VAL1603_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1603 source-label forgetting or finite C_EP source-pack validation",
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
    label: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    template: list[dict[str, Any]],
    validator: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1603 - R2/fR Source-Label Forgetting Or Finite C_EP Source Pack",
                "## Verdict\n"
                "- 1603 tests the zero route directly: source-label forgetting is still not parent-signed, so `C_EP=0` is not certified.\n"
                "- Five clauses remain open: source functor domain, common measure/current, no hidden marker hom, non-Hilbert silence, and readout no-reentry.\n"
                "- The finite route is now stricter: a `C_EP` source-pack schema/template/validator exists, but no finite row is accepted or claimable.\n"
                "- Bound inversion, DD-only proxy, closure-only zero, and `tau_eff=1` shortcuts are explicitly rejected.\n"
                "- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Source-Label Forgetting Theorem Attempt",
                md_table(label, ["clause_id", "required_statement", "current_status", "countermodel", "result"]),
                "## Finite C_EP Source-Pack Schema",
                md_table(schema, ["schema_id", "field", "required_value_or_policy"]),
                "## Finite C_EP Source-Pack Template",
                md_table(template, ["template_id", "quantity", "value", "source_path", "parser_status"]),
                "## Finite C_EP Validator Spec",
                md_table(validator, ["validator_id", "rule", "failure_status"]),
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
    label = label_forgetting_rows()
    schema = finite_schema_rows()
    template = finite_template_rows()
    validator = validator_spec_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        LABEL_FORGETTING,
        FINITE_SCHEMA,
        FINITE_TEMPLATE,
        VALIDATOR_SPEC,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(LABEL_FORGETTING, label)
    write_csv(FINITE_SCHEMA, schema)
    write_csv(FINITE_TEMPLATE, template)
    write_csv(VALIDATOR_SPEC, validator)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, label, schema, template, validator, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
