from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
INPUT_DIR = MICROSCOPE / "quarantine" / "1599" / "input"
QUARANTINE = MICROSCOPE / "quarantine" / "1601"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1601-Y5-R2FR-EP-template-alignment-lemma-or-CMSM-browser-capture.md"

SOURCE_FILES = {
    "1600_doc": ROOT / "1600-Y5-R2FR-MICROSCOPE-HAR-intake-or-parent-K-vector-proof.md",
    "1600_validation": OUT / "P8_Y5_BRR545_1600_VALIDATION.csv",
    "1600_K_proof": OUT / "P8_Y5_PARENT_QLOC_1600_PARENT_K_VECTOR_PROOF_ATTEMPT.csv",
    "1600_K_components": OUT / "P8_Y5_PARENT_QLOC_1600_K_COMPONENT_CONTRACT.csv",
    "1600_alignment": OUT / "P8_Y5_PARENT_QLOC_1600_ALIGNMENT_GATE.csv",
    "1600_next": OUT / "P8_Y5_PARENT_QLOC_1600_NEXT_TARGET.csv",
    "1599_symbolic_k": OUT / "P8_Y5_PARENT_QLOC_1599_SYMBOLIC_K_BRIDGE.csv",
    "1599_filelist": OUT / "P8_Y5_PARENT_QLOC_1599_CMSM_PARSED_FILELIST_CANDIDATE.csv",
    "1598_kernel": OUT / "P8_Y5_PARENT_QLOC_1598_MEASUREMENT_KERNEL_STATUS.csv",
}

NEEDLES = {
    "1600_doc": ["NEXT_1601_EP_TEMPLATE_ALIGNMENT_LEMMA_OR_CMSM_BROWSER_CAPTURE", "EP-template alignment"],
    "1600_validation": ["VAL1600_OVERALL", "PASS"],
    "1600_K_proof": ["KVP1600_1_EP_template_alignment", "NO_EP_TEMPLATE_ALIGNMENT_PROOF"],
    "1600_K_components": ["KCC1600_0_K_EP", "SYMBOLIC_ONLY_NO_ARRAYS"],
    "1600_alignment": ["ALG1600_2_combined_verdict", "ALIGNMENT_REMAINS_MISSING"],
    "1600_next": ["1601-Y5-R2FR-EP-template-alignment-lemma-or-CMSM-browser-capture", "EP-template alignment"],
    "1599_symbolic_k": ["SKB1599_0_EP_signal_template", "K_EP_gravity_dot_V_MTS_source_material"],
    "1599_filelist": ["PFL1599_0_no_filelist_rows", "NO_PARSEABLE_OFFICIAL_FILELIST"],
    "1598_kernel": ["MKS1598_0_published_measurement_equation", "SYMBOLIC_KERNEL_STRUCTURE_AVAILABLE"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1601_SOURCE_REGISTER.csv"
EP_LEMMA = OUT / "P8_Y5_PARENT_QLOC_1601_EP_TEMPLATE_ALIGNMENT_LEMMA.csv"
EP_COUNTERMODEL = OUT / "P8_Y5_PARENT_QLOC_1601_EP_TEMPLATE_COUNTERMODEL.csv"
AMPLITUDE_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1601_EP_ALIGNMENT_AMPLITUDE_CONTRACT.csv"
CAPTURE_STATUS = OUT / "P8_Y5_PARENT_QLOC_1601_CMSM_BROWSER_CAPTURE_STATUS.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1601_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1601_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1601_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1601_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1601_VALIDATION.csv"

COPY_TARGETS = {
    EP_LEMMA: [
        QUARANTINE / "EP_TEMPLATE_ALIGNMENT_LEMMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_EP_template_alignment_lemma_nonclaim_1601.csv",
    ],
    EP_COUNTERMODEL: [
        QUARANTINE / "EP_TEMPLATE_COUNTERMODEL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_EP_template_countermodel_nonclaim_1601.csv",
    ],
    AMPLITUDE_CONTRACT: [
        QUARANTINE / "EP_ALIGNMENT_AMPLITUDE_CONTRACT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_EP_alignment_amplitude_contract_nonclaim_1601.csv",
    ],
    CAPTURE_STATUS: [
        QUARANTINE / "CMSM_BROWSER_CAPTURE_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_CMSM_browser_capture_status_nonclaim_1601.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE_CLOSED.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_closed_1601.csv",
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
                "source_id": f"SRC1601_{index}_{source_id}",
                "source_path": path.relative_to(ROOT).as_posix() if path.exists() else str(path),
                "exists": path.exists(),
                "needle_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "source_role": "1601_EP_template_alignment_or_CMSM_capture_input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def ep_lemma_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "lemma_id": "EPA1601_0_decomposition",
            "statement": "decompose the branch source-material readout vector as V_MTS = C_EP T_EP + V_perp + V_corr",
            "condition": "T_EP is the MICROSCOPE Earth-gravity EP template; <K_EP,V_perp>=0 by definition; V_corr contains corrections/windowing errors",
            "status": "CONDITIONAL_DECOMPOSITION_DEFINED",
            "result": "PROOF_REDUCED_TO_C_EP_AND_CORRECTION_BOUND",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "lemma_id": "EPA1601_1_alignment_condition",
            "statement": "if |C_EP| ||K_EP|| ||T_EP|| > |<K_EP,V_corr>| then <K_EP,V_MTS> != 0",
            "condition": "requires nonzero C_EP, nonzero template norm, and signed/absolute bound on correction projection",
            "status": "CONDITIONAL_ALIGNMENT_LEMMA_DERIVED",
            "result": "EP_ALIGNMENT_SUFFICIENT_CONDITION",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "lemma_id": "EPA1601_2_parent_source_coefficient",
            "statement": "C_EP must be supplied by parent MTS source coupling, not fitted from the MICROSCOPE bound",
            "condition": "parent action/source map gives nonzero differential source coefficient in the observed Earth-gravity EP channel",
            "status": "MISSING_PARENT_C_EP",
            "result": "NO_PARENT_SIGNED_EP_COMPONENT",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "lemma_id": "EPA1601_3_verdict",
            "statement": "the EP-template alignment lemma is derived conditionally but not closed by current corpus evidence",
            "condition": "C_EP and correction bound remain unsourced; CMSM browser/HAR evidence absent",
            "status": "EP_TEMPLATE_ALIGNMENT_NOT_PROVEN",
            "result": "LEMMA_ROUTE_BLOCKED_NONCLAIM",
            "claim_allowed": False,
        },
    ]


def ep_countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "EPC1601_0_common_mode_only",
            "construction": "parent source response shifts only the common-mode/gravitational normalization and leaves no differential EP-template component",
            "math_result": "C_EP=0 while a source response exists",
            "blocked_claim": "source response implies EP-template alignment",
            "escape_condition": "derive nonzero differential source coefficient before measured-G/common-mode absorption",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "EPC1601_1_quadrature_phase",
            "construction": "MTS residual is in a quadrature/orthogonal orbital phase relative to the EP template",
            "math_result": "<K_EP,V_MTS>=0 despite nonzero residual norm",
            "blocked_claim": "nonzero residual norm implies MICROSCOPE EP-channel projection",
            "escape_condition": "source parent phase/observed coframe theorem or official template projection",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "EPC1601_2_correction_cancellation",
            "construction": "correction/window terms cancel the EP-template projection within the observed channel",
            "math_result": "C_EP template projection can be canceled without a signed correction bound",
            "blocked_claim": "symbolic EP template alone proves nonzero readout",
            "escape_condition": "official CMSM correction arrays or parent no-cancellation theorem",
            "claim_allowed": False,
        },
    ]


def amplitude_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "EAC1601_0_C_EP",
            "quantity": "C_EP",
            "needed_form": "nonzero parent source coefficient for the MICROSCOPE EP-template channel",
            "current_status": "MISSING_PARENT_C_EP",
            "why_needed": "sets the leading alignment amplitude",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "EAC1601_1_template_norm",
            "quantity": "||K_EP|| ||T_EP||",
            "needed_form": "positive sourced norm from official template/readout arrays or exact symbolic normalization",
            "current_status": "MISSING_NUMERIC_TEMPLATE_NORM",
            "why_needed": "turns nonzero C_EP into lower bound",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "EAC1601_2_correction_bound",
            "quantity": "|<K_EP,V_corr>|",
            "needed_form": "upper bound from official corrections/windowing or parent theorem",
            "current_status": "MISSING_CORRECTION_BOUND",
            "why_needed": "prevents correction cancellation",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": "EAC1601_3_alignment_margin",
            "quantity": "M_EP = |C_EP| ||K_EP|| ||T_EP|| - |<K_EP,V_corr>|",
            "needed_form": "strictly positive margin",
            "current_status": "NOT_EVALUATED",
            "why_needed": "M_EP>0 proves EP-template alignment",
            "claim_allowed": False,
        },
    ]


def capture_status_rows() -> list[dict[str, Any]]:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    has_input = any(path.is_file() for path in INPUT_DIR.iterdir())
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "capture_id": "CAP1601_0_CMSM_input_folder",
            "route": INPUT_DIR.relative_to(ROOT).as_posix(),
            "current_status": "INPUT_FILES_PRESENT" if has_input else "NO_INPUT_FILES_PRESENT",
            "filelist_acquired": has_input,
            "claim_impact": "rerun 1599 parser if input appears; current 1601 uses theory route only",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "capture_id": "CAP1601_1_browser_capture_route",
            "route": "CMSM browser/HAR capture",
            "current_status": "AVAILABLE_AS_FALLBACK_NOT_EXECUTED",
            "filelist_acquired": False,
            "claim_impact": "data route remains parked until authenticated evidence is available",
            "claim_allowed": False,
        },
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1601_0_conditional_lemma",
            "acceptance_rule": "record conditional EP-template alignment lemma",
            "input_state": "mathematical inequality derived; C_EP/corrections unsourced",
            "runner_result": "ACCEPT_CONDITIONAL_LEMMA_ONLY",
            "effect": "proof target sharpened",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1601_1_proof_claim",
            "acceptance_rule": "parent-signed C_EP and correction bound required",
            "input_state": "C_EP missing; correction bound missing",
            "runner_result": "REJECT_EP_ALIGNMENT_CLAIM",
            "effect": "no tau_min or WEP score",
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1601_2_CMSM_capture",
            "acceptance_rule": "reviewed HAR/filelist evidence required",
            "input_state": "no input files present",
            "runner_result": "NO_CMSM_CAPTURE_INGESTED",
            "effect": "data route remains fallback",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    claims = [
        ("CG1601_0_EP_alignment", "EP-template alignment proven", "C_EP and correction bound are missing"),
        ("CG1601_1_tau", "tau_WEP lower bound exists", "EP alignment margin not positive/sourced"),
        ("CG1601_2_CMSM", "CMSM browser/HAR evidence ingested", "no input files present"),
        ("CG1601_3_WEP", "MTS passes MICROSCOPE/WEP", "product anchor only"),
        ("CG1601_4_local_GR", "derived local GR branch", "readout/coupling residual remains open"),
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
            "decision_id": "DEC1601_0_progress",
            "decision": "CONDITIONAL_EP_ALIGNMENT_LEMMA_DERIVED",
            "reason": "the proof now reduces to a nonzero parent EP coefficient and a correction-cancellation bound",
            "next_action": "hunt C_EP in parent source/matter action",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1601_1_blocker",
            "decision": "EP_TEMPLATE_ALIGNMENT_NOT_PROVEN",
            "reason": "common-mode-only, quadrature, and correction-cancellation countermodels remain live",
            "next_action": "try C_EP source-coefficient theorem or use CMSM data route",
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1601_2_next",
            "decision": "NEXT_1602_CEP_SOURCE_COEFFICIENT_OR_COMMON_MODE_ZERO_THEOREM",
            "reason": "C_EP is now the smallest unsourced theoretical object",
            "next_action": "derive nonzero C_EP from parent source coupling or prove source response is common-mode zero for WEP",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1602-Y5-R2FR-C_EP-source-coefficient-or-common-mode-zero-theorem.md",
            "script": "scripts/Y5_R2FR_C_EP_source_coefficient_or_common_mode_zero_theorem.py",
            "objective": "derive a parent-signed nonzero EP-template source coefficient C_EP, or prove the finite branch is purely common-mode/zero in WEP",
            "success_condition": "C_EP source coefficient with sign/units and correction contract, or theorem that WEP finite branch is common-mode only and cannot violate WEP",
            "do_not": "do not fit C_EP from the MICROSCOPE bound, do not claim WEP/local GR, do not use tau_WEP=1",
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


def no_formalization_1601() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(FORMALIZATION.rglob("*1601*"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = source_register_rows()
    lemma = read_csv(EP_LEMMA)
    counter = read_csv(EP_COUNTERMODEL)
    contract = read_csv(AMPLITUDE_CONTRACT)
    capture = read_csv(CAPTURE_STATUS)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    copies = [target for targets in COPY_TARGETS.values() for target in targets]
    checks = [
        ("VAL1601_0_sources_exist", all(row["exists"] == "True" or row["exists"] is True for row in sources), "all cited 1601 local source paths exist"),
        ("VAL1601_1_needles_found", all(row["needle_found"] == "True" or row["needle_found"] is True for row in sources), "all required 1601 source needles found"),
        ("VAL1601_2_conditional_lemma", any(row["lemma_id"] == "EPA1601_1_alignment_condition" and row["result"] == "EP_ALIGNMENT_SUFFICIENT_CONDITION" for row in lemma), "conditional EP-template alignment lemma recorded"),
        ("VAL1601_3_lemma_not_claimed", any(row["lemma_id"] == "EPA1601_3_verdict" and row["status"] == "EP_TEMPLATE_ALIGNMENT_NOT_PROVEN" for row in lemma), "EP-template alignment remains unproven"),
        ("VAL1601_4_countermodels", len(counter) >= 3 and any(row["countermodel_id"] == "EPC1601_0_common_mode_only" for row in counter), "countermodels recorded"),
        ("VAL1601_5_CEP_contract", any(row["contract_id"] == "EAC1601_0_C_EP" and row["current_status"] == "MISSING_PARENT_C_EP" for row in contract), "C_EP source coefficient contract recorded"),
        ("VAL1601_6_capture_status", any(row["capture_id"] == "CAP1601_0_CMSM_input_folder" for row in capture), "CMSM capture fallback status recorded"),
        ("VAL1601_7_runner_rejects_claim", any(row["runner_id"] == "RUN1601_1_proof_claim" and row["runner_result"] == "REJECT_EP_ALIGNMENT_CLAIM" for row in runner), "runner rejects EP alignment claim"),
        ("VAL1601_8_claim_gates_closed", gates and all(row["claim_allowed"].lower() == "false" for row in gates), "all 1601 claim gates remain closed"),
        ("VAL1601_9_decision_next", any(row["decision"] == "NEXT_1602_CEP_SOURCE_COEFFICIENT_OR_COMMON_MODE_ZERO_THEOREM" for row in decisions), "decision selects 1602 C_EP source coefficient or common-mode zero theorem"),
        ("VAL1601_10_csv_parse", csv_parses(generated_csvs), "all generated 1601 CSVs parse"),
        ("VAL1601_11_claim_safety_flags", no_claim_flags(generated_csvs), "no generated 1601 rows are score-ready, prediction rows, or claim-allowed"),
        ("VAL1601_12_branch_copies", all(path.exists() for path in copies), "branch/quarantine nonclaim copies exist"),
        ("VAL1601_13_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1601_14_formalization_untouched", no_formalization_1601(), "no 1601 outputs found under formalization-workbench"),
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
            "check_id": "VAL1601_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1601 EP-template alignment lemma or CMSM capture validation",
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
    lemma: list[dict[str, Any]],
    counter: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    capture: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1601 - R2/fR EP-Template Alignment Lemma Or CMSM Browser Capture",
                "## Verdict\n"
                "- 1601 derives the conditional EP-template alignment lemma: if `|C_EP| ||K_EP|| ||T_EP|| > |<K_EP,V_corr>|`, then the MICROSCOPE EP-template projection is nonzero.\n"
                "- The lemma is not claimable: `C_EP`, official template norm, and correction bound are not parent-signed or sourced.\n"
                "- Three countermodels remain live: common-mode-only response, quadrature/orthogonal phase, and correction/window cancellation.\n"
                "- The smallest next theoretical object is now `C_EP`, the parent EP-template source coefficient.\n"
                "- No WEP, local-GR, Newton, PPN, R10, clock, orbital, beta/coupling, or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## EP-Template Alignment Lemma",
                md_table(lemma, ["lemma_id", "statement", "condition", "status", "result"]),
                "## EP-Template Countermodels",
                md_table(counter, ["countermodel_id", "construction", "math_result", "blocked_claim", "escape_condition"]),
                "## Alignment Amplitude Contract",
                md_table(contract, ["contract_id", "quantity", "needed_form", "current_status", "why_needed"]),
                "## CMSM Browser Capture Status",
                md_table(capture, ["capture_id", "route", "current_status", "filelist_acquired", "claim_impact"]),
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
    lemma = ep_lemma_rows()
    counter = ep_countermodel_rows()
    contract = amplitude_contract_rows()
    capture = capture_status_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        EP_LEMMA,
        EP_COUNTERMODEL,
        AMPLITUDE_CONTRACT,
        CAPTURE_STATUS,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(EP_LEMMA, lemma)
    write_csv(EP_COUNTERMODEL, counter)
    write_csv(AMPLITUDE_CONTRACT, contract)
    write_csv(CAPTURE_STATUS, capture)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, lemma, counter, contract, capture, runner, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
