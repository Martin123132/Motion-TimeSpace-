from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
RESIDUAL_ROOT = BRANCH_ROOT / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1440-Y5-R10-RAB-minimal-WEP-parent-clause-proof-obligations-or-closure-demotion.md"

BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
NEXT_1439 = OUT / "P8_Y5_R10_1439_NEXT_TARGET.csv"
VALIDATION_1439 = OUT / "P8_Y5_BRR545_1439_VALIDATION.csv"
MINIMAL_CLAUSE_1439 = OUT / "P8_Y5_R10_1439_MINIMAL_PARENT_CLAUSE.csv"
COUNTERMODEL_1439 = OUT / "P8_Y5_R10_1439_COUNTERMODEL_LEDGER.csv"
PARSER_1439 = OUT / "P8_Y5_R10_1439_SOURCE_PACK_PARSER_DRYRUN.csv"
BRANCH_MINIMAL_CLAUSE_1439 = COEFFICIENT_ROOT / "C_parent_WEP_minimal_parent_clause.csv"
BRANCH_PARSER_1439 = RESIDUAL_ROOT / "source_pack_parser_dryrun.csv"

MOMS_1088 = OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv"
THM_1088 = OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv"
AXIOM_1090 = OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv"
CLOSURE_1090 = OUT / "P8_Y5_R10_1090_CLOSURE_DEMOTION_REGISTER.csv"
FRAME_1003 = OUT / "P8_Y5_R10_1003_COVARIANT_FRAME_THEOREM_AUDIT.csv"
PARENT_1009 = OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv"
SELECTOR_1016 = OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv"
SOURCE_ZERO_1027 = OUT / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv"
BRANCH_1028 = OUT / "P8_Y5_R10_1028_BRANCH_VERDICTS.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1440_SOURCE_REGISTER.csv"
PROOF_OBLIGATION_AUDIT = OUT / "P8_Y5_R10_1440_PROOF_OBLIGATION_AUDIT.csv"
MINIMAL_CLAUSE_PROOF_ATTEMPT = OUT / "P8_Y5_R10_1440_MINIMAL_CLAUSE_PROOF_ATTEMPT.csv"
CLOSURE_DEMOTION_REGISTER = OUT / "P8_Y5_R10_1440_CLOSURE_DEMOTION_REGISTER.csv"
SOURCE_PACK_ONLY_ROUTE_STATUS = OUT / "P8_Y5_R10_1440_SOURCE_PACK_ONLY_ROUTE_STATUS.csv"
REOPEN_CONDITIONS = OUT / "P8_Y5_R10_1440_REOPEN_CONDITIONS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1440_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1440_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1440_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1440_VALIDATION.csv"

BRANCH_CLOSURE_DEMOTION = COEFFICIENT_ROOT / "C_parent_WEP_clause_closure_demotion.csv"
BRANCH_SOURCE_PACK_ROUTE = RESIDUAL_ROOT / "source_pack_only_route_status.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean(value: Any) -> str:
    return str(value).replace("\n", " ").replace("\r", " ").strip()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: clean(row.get(key, "")) for key in fieldnames})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_has(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="ignore")


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


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


def branch_id() -> str:
    rows = read_csv(BRANCH_ID_FILE)
    if len(rows) != 1:
        raise ValueError(f"expected one branch row, got {len(rows)}")
    value = rows[0].get("same_parent_branch_id", "").strip()
    if not value:
        raise ValueError("same_parent_branch_id missing")
    return value


def source_register_rows(branch: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC1440_0_1439_next", NEXT_1439, "NEXT1439_0_1440", "1439 handoff selecting proof obligations or closure demotion."),
        ("SRC1440_1_1439_validation", VALIDATION_1439, "VAL1439_10_overall", "1439 validation summary."),
        ("SRC1440_2_1439_clause", MINIMAL_CLAUSE_1439, "MPC1439_4_verdict", "1439 minimal parent clause."),
        ("SRC1440_3_1439_countermodel", COUNTERMODEL_1439, "CM1439_3_basis_mismatch", "1439 countermodel ledger."),
        ("SRC1440_4_1439_parser", PARSER_1439, "PARSE1439_5", "1439 source-pack parser dry-run."),
        ("SRC1440_5_branch_clause", BRANCH_MINIMAL_CLAUSE_1439, "MPC1439_4_verdict", "branch minimal clause copy."),
        ("SRC1440_6_branch_parser", BRANCH_PARSER_1439, "PARSE1439_5", "branch parser dry-run copy."),
        ("SRC1440_7_branch_id", BRANCH_ID_FILE, branch, "active same-parent branch id."),
        ("SRC1440_8_MOMS1088", MOMS_1088, "MOMS1088_7_verdict", "minimal ordinary-matter signature clause."),
        ("SRC1440_9_THM1088", THM_1088, "THM1088_6_current_corpus_verdict", "conditional zero theorem."),
        ("SRC1440_10_AXIOM1090", AXIOM_1090, "AX1090_4_variation_domain_order", "missing axiom ledger."),
        ("SRC1440_11_CLOS1090", CLOSURE_1090, "CLOS1090_0_MOMS", "closure demotion precedent."),
        ("SRC1440_12_FRAME1003", FRAME_1003, "CFA1003_6_theorem_verdict", "covariant frame theorem audit."),
        ("SRC1440_13_PARENT1009", PARENT_1009, "PCS1009_2_universal_matter", "parent sector contract."),
        ("SRC1440_14_SELECTOR1016", SELECTOR_1016, "PSC1016_1_single_observed_coframe", "parent selector/coframe contract."),
        ("SRC1440_15_SOURCEZERO1027", SOURCE_ZERO_1027, "QZ1027_4_no_marker_constants", "source-zero proof audit."),
        ("SRC1440_16_BRANCH1028", BRANCH_1028, "BV1028_0_no_marker_theorem", "no-marker theorem verdict."),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "path_exists": path.exists(),
            "anchor": anchor,
            "anchor_found": text_has(path, anchor),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, anchor, role in specs
    ]


def proof_obligation_rows(branch: str) -> list[dict[str, Any]]:
    rows = [
        (
            "PO1440_0_parent_object",
            "one parent action object owns q, observed fields, matter sectors, source/readout order, and variation before projection",
            "AX1090_0_parent_object;PCS1009_9_total_parent_contract",
            "MISSING_PARENT_ACTION_OWNER",
            "multiple contracts exist, but no single parent action signs the whole ordinary-matter branch",
        ),
        (
            "PO1440_1_observed_quotient",
            "observed coframe/metric/gauge data descend through q and have no hidden representative frame",
            "MOMS1088_1_quotient_observables;CFA1003_1_quotient_coframe_descent",
            "CONDITIONAL_ONLY",
            "chain-rule zero is conditional on parent-derived q/coframe functor and no-shadow frame",
        ),
        (
            "PO1440_2_matter_functor",
            "all ordinary matter, clocks, rods, photons, and readouts use the same descended observed coframe",
            "MOMS1088_2_matter_bundle;CFA1003_2_matter_functor;PSC1016_1_single_observed_coframe",
            "UNSIGNED_PARENT_SELECTION",
            "the exact contract is written, but matter functor selection is not parent-signed",
        ),
        (
            "PO1440_3_no_marker_constants",
            "ordinary masses, charges, alpha_EM, clocks, and material labels are quotient-owned constants or explicit residuals",
            "MOMS1088_3_constant_superselection;QZ1027_4_no_marker_constants;AX1090_3_fixed_constant_sector",
            "MISSING_NO_MARKER_THEOREM",
            "material/EM/clock marker counterexamples survive without a parent theorem",
        ),
        (
            "PO1440_4_no_species_weights",
            "no independent w_A(X) S_A or source-only material multiplier exists before variation",
            "MOMS1088_4_no_species_weights;AX1090_2_common_quantum_measure",
            "PRE_ACTION_WEIGHT_EXCLUSION_UNSIGNED",
            "species/source weight countermodel remains legal unless excluded",
        ),
        (
            "PO1440_5_no_shadow_domain",
            "no shadow conformal/disformal matter frame, support/domain marker, boundary charge, or source-only metric survives",
            "MOMS1088_6_no_shadow_domain;AX1090_1_no_hidden_visible_hom",
            "NO_SHADOW_DOMAIN_UNSIGNED",
            "hidden visible homomorphism is explicitly a missing axiom, not a theorem",
        ),
        (
            "PO1440_6_readout_silence",
            "readout/orbit/source-worldtube projection cannot create or erase a WEP residual after parent variation",
            "MOMS1088_5_variation_order;AX1090_4_variation_domain_order;PARSE1439_source_pack",
            "CONDITIONAL_AND_FILES_MISSING",
            "variation-order rule is not parent-derived, and official readout/source files remain absent",
        ),
        (
            "PO1440_7_countermodel_exclusion",
            "species-marker, source-weight, readout-projection, and basis-mismatch countermodels are all excluded",
            "CM1439_0 through CM1439_3",
            "COUNTERMODELS_LIVE",
            "no current proof excludes all four countermodels",
        ),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "obligation_id": obligation_id,
            "proof_obligation": proof_obligation,
            "source_evidence": source_evidence,
            "current_status": current_status,
            "why_not_closed": why_not_closed,
            "proof_result": "NOT_PROVED",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for obligation_id, proof_obligation, source_evidence, current_status, why_not_closed in rows
    ]


def proof_attempt_rows(branch: str, obligations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed = [row["obligation_id"] for row in obligations if row["proof_result"] != "PROVED"]
    return [
        {
            "same_parent_branch_id": branch,
            "attempt_id": "MPA1440_0_assume_clause",
            "step": "Assume the minimal WEP parent clause from 1439 as a theorem target.",
            "result": "THEOREM_TARGET_ONLY",
            "detail": "The clause is precise enough to prove C_parent_WEP=0 if its premises are parent-derived.",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "attempt_id": "MPA1440_1_vertical_variation",
            "step": "Take the Ti/Pt differential vertical variation of the parent matter/source/readout action.",
            "result": "CONDITIONAL_ZERO_SHAPE",
            "detail": "If all ordinary labels descend through the observed quotient and no hidden labels survive, delta_v S=0.",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "attempt_id": "MPA1440_2_current_corpus_check",
            "step": "Check current corpus obligations against 1088/1090/1003/1009/1016/1027/1028 evidence.",
            "result": "FAILS_PROOF_OBLIGATIONS",
            "detail": ";".join(failed),
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "attempt_id": "MPA1440_3_verdict",
            "step": "Decide whether to promote C_parent_WEP=0.",
            "result": "DO_NOT_PROMOTE_DEMOTE_TO_CLOSURE_ONLY",
            "detail": "The conditional theorem is useful, but adopting it now would assume metric universality/EEP rather than derive it from MTS.",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def closure_demotion_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "closure_id": "CLOS1440_0_minimal_WEP_parent_clause",
            "object": "minimal WEP parent clause / MOMS-like ordinary-matter signature for C_parent_WEP",
            "new_status": "CLOSURE_ONLY_NOT_ADOPTED_AS_DERIVATION",
            "allowed_use": "private branch organization; conditional theorem target; explicit closure-assumed comparison if labelled",
            "forbidden_use": "derived WEP pass; local-GR claim; C_parent_WEP theorem-zero promotion; hiding finite coefficients",
            "reopen_condition": "derive every proof obligation from a single parent action, or import source-backed same-branch finite WEP coefficient/source-pack rows",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "closure_id": "CLOS1440_1_C_parent_WEP_zero",
            "object": "C_parent_WEP_TiPt = 0",
            "new_status": "NOT_ZERO_CERTIFIED",
            "allowed_use": "conditional algebra under explicitly assumed closure only",
            "forbidden_use": "score-ready P_WEP input; local-GR reduction evidence; MICROSCOPE pass",
            "reopen_condition": "parent-signed zero certificate or valid C_parent_WEP_slot_import.csv",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_pack_route_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "route_id": "SPR1440_0_source_pack_only_score_route",
            "route": "official/same-basis MICROSCOPE source-pack route",
            "route_status": "ONLY_SCORE_ROUTE_WHILE_CLAUSE_CLOSURE_ONLY",
            "current_parser_status": "REFUSED_TARGET_FILES_MISSING",
            "required_target_files": "official_readout; source_worldtube; product_convention; branch_classifier; full_material_tensor; C_parent_import",
            "claim_consequence": "no WEP or local-GR score until parser passes and C_parent is derived/filled",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def reopen_condition_rows(branch: str) -> list[dict[str, Any]]:
    rows = [
        ("REOPEN1440_0_parent_action", "derive AX1090_0 parent action object from MTS primitives"),
        ("REOPEN1440_1_hidden_hom", "derive AX1090_1 no-hidden-visible-hom theorem"),
        ("REOPEN1440_2_quantum_measure", "derive AX1090_2 common action/measure/no species Jacobian rule"),
        ("REOPEN1440_3_constants", "derive AX1090_3 fixed constant/material/EM sector or retain explicit residual fields"),
        ("REOPEN1440_4_variation_order", "derive AX1090_4 variation-before-readout/source-worldtube rule"),
        ("REOPEN1440_5_source_pack", "provide valid same-branch source-pack target files with no placeholders"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "reopen_id": reopen_id,
            "condition": condition,
            "current_status": "OPEN_NOT_SATISFIED",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for reopen_id, condition in rows
    ]


def claim_gate_rows(branch: str) -> list[dict[str, Any]]:
    gates = [
        ("CG1440_0_closure_not_claim", "closure-only WEP parent clause cannot be used as derived proof"),
        ("CG1440_1_zero_not_certified", "C_parent_WEP=0 is not zero-certified"),
        ("CG1440_2_countermodels_live", "countermodels remain live until parent action excludes them"),
        ("CG1440_3_source_pack_only", "only source-pack route can score while clause is closure-only"),
        ("CG1440_4_no_shortcuts", "no tau_eff=1, measured-G absorption, bound-as-prediction, or surrogate basis mixing"),
        ("CG1440_5_local_gr_blocked", "local-GR/Newton derivation claim remains blocked by WEP/source/matter descent gap"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1440_0_demote_clause",
            "decision": "demote the minimal WEP parent clause to closure-only",
            "why": "current corpus supplies a strong conditional theorem stack but not a single parent-signed derivation of the ordinary-matter signature",
            "consequence": "C_parent_WEP remains missing and WEP/local-GR claims remain forbidden",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "decision_id": "DEC1440_1_keep_source_pack",
            "decision": "keep official/same-basis source-pack route as the only score route",
            "why": "if WEP zero is not derived, a finite coefficient/source/readout/material pack is required for testing",
            "consequence": "next work should reduce AX1090 obligations or harden source-pack acquisition, not claim a pass",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1440_0_1441",
            "next_target": "1441-Y5-R10-RAB-AX1090-parent-axiom-reduction-or-source-pack-acquisition-priority.md",
            "script": "scripts/Y5_R10_RAB_AX1090_parent_axiom_reduction_or_source_pack_acquisition_priority.py",
            "objective": "try to reduce AX1090 missing axioms to MTS primitives; if they remain unproved, rank the official source-pack acquisition tasks needed for the finite WEP score route.",
            "include": "AX1090 axiom reduction; source-pack acquisition priority; closure-only labels; no-claim gates",
            "exclude": "numeric WEP score; local-GR claim; invented source-pack target files; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_branch_files(closure_rows: list[dict[str, Any]], source_pack_rows: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_CLOSURE_DEMOTION, closure_rows)
    write_csv(BRANCH_SOURCE_PACK_ROUTE, source_pack_rows)


def validation_rows(
    sources: list[dict[str, Any]],
    obligations: list[dict[str, Any]],
    proof_attempt: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    source_route: list[dict[str, Any]],
    reopen: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        PROOF_OBLIGATION_AUDIT,
        MINIMAL_CLAUSE_PROOF_ATTEMPT,
        CLOSURE_DEMOTION_REGISTER,
        SOURCE_PACK_ONLY_ROUTE_STATUS,
        REOPEN_CONDITIONS,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_CLOSURE_DEMOTION,
        BRANCH_SOURCE_PACK_ROUTE,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            parsed_rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(parsed_rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    obligations_not_proved = all(row["proof_result"] == "NOT_PROVED" for row in obligations)
    proof_demotes = any(row["result"] == "DO_NOT_PROMOTE_DEMOTE_TO_CLOSURE_ONLY" for row in proof_attempt)
    closure_written = any(row["new_status"] == "CLOSURE_ONLY_NOT_ADOPTED_AS_DERIVATION" for row in closure)
    source_pack_only = len(source_route) == 1 and source_route[0]["route_status"] == "ONLY_SCORE_ROUTE_WHILE_CLAUSE_CLOSURE_ONLY"
    reopen_visible = len(reopen) >= 6 and all(row["current_status"] == "OPEN_NOT_SATISFIED" for row in reopen)
    gates_safe = all(row["gate_status"] == "LOCKED_CLAIM_FALSE" for row in gates) and not truthy_claim_flags
    branch_files_ok = BRANCH_CLOSURE_DEMOTION.exists() and BRANCH_SOURCE_PACK_ROUTE.exists()
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1440_0_source_register", sources_ok, "all 1440 cited source paths and anchors resolve"),
        ("VAL1440_1_obligations_not_proved", obligations_not_proved, "all proof obligations remain not-proved in current corpus"),
        ("VAL1440_2_proof_demotes", proof_demotes, "minimal clause proof attempt demotes instead of promoting"),
        ("VAL1440_3_closure_written", closure_written, "closure demotion register written"),
        ("VAL1440_4_source_pack_only", source_pack_only, "source-pack route is the only score route while closure-only"),
        ("VAL1440_5_reopen_conditions", reopen_visible, "reopen conditions are explicit and unsatisfied"),
        ("VAL1440_6_claim_gates", gates_safe, "all claim/valid/prediction flags remain false"),
        ("VAL1440_7_csv_parse", parse_ok, "all generated 1440 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1440_8_branch_files", branch_files_ok, "branch closure and source-pack route files written"),
        ("VAL1440_9_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1440_10_next_target", True, "1441 handoff written"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "generated_utc": stamp(),
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1440_11_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1440 demotes the minimal WEP parent clause to closure-only and keeps source-pack scoring as the active route",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1440 - Minimal WEP parent clause proof obligations or closure demotion",
            "**Current verdict:** the minimal WEP parent clause is a strong sufficient theorem target, but the current corpus does not derive it from one parent action. It is demoted to closure-only, and `C_parent_WEP=0` remains not zero-certified.",
            "**Main progress:** the proof failure is now localized to named AX1090/MOMS obligations. While those are open, the official same-basis source-pack route is the only legitimate WEP scoring path.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Proof obligation audit\n" + md_table(sections["obligations"]),
            "## Minimal clause proof attempt\n" + md_table(sections["proof_attempt"]),
            "## Closure demotion register\n" + md_table(sections["closure"]),
            "## Source-pack-only route status\n" + md_table(sections["source_route"]),
            "## Reopen conditions\n" + md_table(sections["reopen"]),
            "## Claim gates\n" + md_table(sections["gates"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    COEFFICIENT_ROOT.mkdir(parents=True, exist_ok=True)
    RESIDUAL_ROOT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    obligations = proof_obligation_rows(branch)
    proof_attempt = proof_attempt_rows(branch, obligations)
    closure = closure_demotion_rows(branch)
    source_route = source_pack_route_rows(branch)
    reopen = reopen_condition_rows(branch)
    gates = claim_gate_rows(branch)
    decisions = decision_rows(branch)
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(PROOF_OBLIGATION_AUDIT, obligations)
    write_csv(MINIMAL_CLAUSE_PROOF_ATTEMPT, proof_attempt)
    write_csv(CLOSURE_DEMOTION_REGISTER, closure)
    write_csv(SOURCE_PACK_ONLY_ROUTE_STATUS, source_route)
    write_csv(REOPEN_CONDITIONS, reopen)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    write_branch_files(closure, source_route)

    validation = validation_rows(sources, obligations, proof_attempt, closure, source_route, reopen, gates)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "obligations": obligations,
            "proof_attempt": proof_attempt,
            "closure": closure,
            "source_route": source_route,
            "reopen": reopen,
            "gates": gates,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1440_minimal_WEP_clause_demoted_to_closure_source_pack_only_nonclaim")


if __name__ == "__main__":
    main()
