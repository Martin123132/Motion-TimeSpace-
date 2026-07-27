from __future__ import annotations

import csv
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_ROOT = MICROSCOPE / "branch_locked_wep"
COEFFICIENT_ROOT = BRANCH_ROOT / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1446-Y5-R10-RAB-parent-action-coupling-source-search-against-C-parent-contract.md"

PREV_NEXT = OUT / "P8_Y5_R10_1445_NEXT_TARGET.csv"
PREV_CONTRACT = COEFFICIENT_ROOT / "C_parent_WEP_coupling_theorem_contract.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1445_VALIDATION.csv"
LIVE_C_PARENT_IMPORT = COEFFICIENT_ROOT / "C_parent_WEP_slot_import.csv"
LIVE_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1446_SOURCE_REGISTER.csv"
CORPUS_HITS = OUT / "P8_Y5_R10_1446_CORPUS_SEARCH_HITS.csv"
CANDIDATE_LEDGER = OUT / "P8_Y5_R10_1446_PARENT_ACTION_COUPLING_CANDIDATE_LEDGER.csv"
CLAUSE_AUDIT = OUT / "P8_Y5_R10_1446_CONTRACT_CLAUSE_REDUCTION_AUDIT.csv"
IMPORT_GATE = OUT / "P8_Y5_R10_1446_IMPORT_DECISION_GATE.csv"
PARSER_DRYRUN = OUT / "P8_Y5_R10_1446_PARSER_DRYRUN.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1446_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1446_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1446_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1446_VALIDATION.csv"

BRANCH_CANDIDATES = COEFFICIENT_ROOT / "C_parent_WEP_parent_action_coupling_candidate_ledger.csv"
BRANCH_CLAUSE_AUDIT = COEFFICIENT_ROOT / "C_parent_WEP_contract_clause_reduction_audit.csv"
BRANCH_IMPORT_GATE = COEFFICIENT_ROOT / "C_parent_WEP_import_decision_gate.csv"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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
            writer.writerow(row)


def write_table(handle: Any, title: str, rows: list[dict[str, Any]]) -> None:
    handle.write(f"\n## {title}\n")
    if not rows:
        handle.write("\nNo rows.\n")
        return
    fields = list(rows[0].keys())
    handle.write("| " + " | ".join(fields) + " |\n")
    handle.write("| " + " | ".join(["---"] * len(fields)) + " |\n")
    for row in rows:
        handle.write("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |\n")


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def source_path(relative: str) -> Path:
    return ROOT / relative


def source_register_rows() -> list[dict[str, Any]]:
    entries = [
        ("SRC1446_0_prev_next", PREV_NEXT, "1445 handoff into parent-action/coupling source search"),
        ("SRC1446_1_prev_contract", PREV_CONTRACT, "C_parent_WEP coupling theorem contract"),
        ("SRC1446_2_prev_validation", PREV_VALIDATION, "1445 validation"),
        ("SRC1446_3_1008_doc", source_path("1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md"), "parent theta/Qtau extraction attempt"),
        ("SRC1446_4_1008_variation", OUT / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv", "parent variation audit"),
        ("SRC1446_5_1009_doc", source_path("1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"), "parent current-chain sector contract"),
        ("SRC1446_6_1009_sector", OUT / "P8_Y5_R10_1009_PARENT_SECTOR_CONTRACT.csv", "parent sector contract rows"),
        ("SRC1446_7_1009_runner", OUT / "P8_Y5_R10_1009_SECTOR_VARIATION_RUNNER.csv", "sector variation runner refusals"),
        ("SRC1446_8_1016_doc", source_path("1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md"), "parent worldtube/source selector contract"),
        ("SRC1446_9_1016_contract", OUT / "P8_Y5_R10_1016_PARENT_SELECTOR_CONTRACT.csv", "parent selector contract"),
        ("SRC1446_10_1077_doc", source_path("1077-Y5-R10-parent-WEP-coupling-owner-theorem-or-material-vector-source-row.md"), "parent WEP coupling-owner theorem attempt"),
        ("SRC1446_11_1077_theorem", OUT / "P8_Y5_R10_1077_PARENT_WEP_COUPLING_OWNER_THEOREM_ATTEMPT.csv", "WEP coupling-owner theorem attempt"),
        ("SRC1446_12_1077_signature", OUT / "P8_Y5_R10_1077_CLAUSE_SIGNATURE_MATRIX.csv", "WEP clause signature matrix"),
        ("SRC1446_13_1078_doc", source_path("1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md"), "proof-stack attempt for object/action/current owner"),
        ("SRC1446_14_1078_action_measure", OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv", "action-measure proof attempt"),
        ("SRC1446_15_1078_current_owner", OUT / "P8_Y5_R10_1078_CURRENT_OWNER_PROOF_ATTEMPT.csv", "current-owner proof attempt"),
        ("SRC1446_16_1088_doc", source_path("1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md"), "MOMS minimal ordinary-matter signature"),
        ("SRC1446_17_1088_clause", OUT / "P8_Y5_R10_1088_MINIMAL_SIGNATURE_CLAUSE.csv", "MOMS clauses"),
        ("SRC1446_18_1088_theorem", OUT / "P8_Y5_R10_1088_CONDITIONAL_ZERO_THEOREM.csv", "conditional zero theorem"),
        ("SRC1446_19_1090_doc", source_path("1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md"), "MOMS synthesis and missing axiom ledger"),
        ("SRC1446_20_1090_synthesis", OUT / "P8_Y5_R10_1090_SYNTHESIS_ATTEMPT.csv", "MOMS synthesis attempt"),
        ("SRC1446_21_1090_axioms", OUT / "P8_Y5_R10_1090_MISSING_AXIOM_LEDGER.csv", "missing axiom ledger"),
        ("SRC1446_22_1217_doc", source_path("1217-Y5-R10-WEP-Cparent-coefficient-map-or-finite-prior-row.md"), "Cparent coefficient map attempt"),
        ("SRC1446_23_1217_map", OUT / "P8_Y5_R10_1217_CPARENT_MAP_ATTEMPT.csv", "Cparent map attempt"),
        ("SRC1446_24_1217_zero", OUT / "P8_Y5_R10_1217_COEFFICIENT_ZERO_AUDIT.csv", "coefficient zero audit"),
    ]
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": path.exists(),
            "role": role,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_id, path, role in entries
    ]


def corpus_search_hits() -> list[dict[str, Any]]:
    terms = [
        "parent action",
        "S_parent",
        "C_parent_WEP",
        "functional derivative",
        "coupling owner",
        "ordinary matter",
        "WEP",
        "DERIVED_ZERO",
        "missing axiom",
        "fail_current_claim",
    ]
    pattern = re.compile("|".join(re.escape(term) for term in terms), re.IGNORECASE)
    rows: list[dict[str, Any]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".csv", ".txt"}:
            continue
        if "1446-" in path.name or "P8_Y5_R10_1446" in path.name:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        local_count = 0
        for line_number, line in enumerate(lines, start=1):
            match = pattern.search(line)
            if not match:
                continue
            snippet = line.strip()
            rows.append(
                {
                    "hit_id": f"HIT1446_{len(rows)}",
                    "source_path": str(path),
                    "line_number": line_number,
                    "matched_term": match.group(0),
                    "snippet": snippet[:300],
                    "valid_prediction_row": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
            local_count += 1
            if local_count >= 3:
                break
        if len(rows) >= 80:
            break
    return rows


def candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "PAC1446_0_1008_parent_theta_Qtau",
            "source_path": str(source_path("1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md")),
            "candidate_route": "parent theta/Q_tau current-chain extraction",
            "best_support": "disciplined extraction contract exists for L_parent, theta_MTS, J_tau, and charge pieces",
            "blocking_evidence": "PVA1008_0 and QTA1008_0 say explicit current-chain L_parent is missing across EH, matter/source, extra, projector, boundary/reference, and coupling sectors",
            "contract_coverage": "CTC1445_0 partial; CTC1445_2 not satisfied",
            "import_decision": "REJECT_IMPORT_CONTRACT_ONLY",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "PAC1446_1_1009_parent_sector_contract",
            "source_path": str(source_path("1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md")),
            "candidate_route": "sum of owned parent sectors S_parent",
            "best_support": "PCS1009_9 names S_parent=sum owned sectors; sectors include EH, matter, Gamma/Khat, PiM, worldtube glue, and response doublets",
            "blocking_evidence": "SVR1009 rows refuse every sector as incomplete parent current-chain contract; total parent switch is unsigned",
            "contract_coverage": "CTC1445_0 strongest current scaffold; no WEP coefficient functional derivative",
            "import_decision": "REJECT_IMPORT_NO_TOTAL_PARENT_ACTION",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "PAC1446_2_1016_worldtube_selector",
            "source_path": str(source_path("1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md")),
            "candidate_route": "parent-owned worldtube/source-measure selector",
            "best_support": "PSC1016 defines pre-readout source support, one observed coframe, tau, Hamiltonian source charge, PiM, coupling descent, and boundary reference lock",
            "blocking_evidence": "PST1016 lemmas are conditional; selector verdict says current MTS has not parent-signed the clauses",
            "contract_coverage": "CTC1445_1 partial for source/readout projection; CTC1445_3 not closed",
            "import_decision": "REJECT_IMPORT_SELECTOR_CONDITIONAL",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "PAC1446_3_1077_WEP_coupling_owner",
            "source_path": str(source_path("1077-Y5-R10-parent-WEP-coupling-owner-theorem-or-material-vector-source-row.md")),
            "candidate_route": "parent WEP coupling-owner theorem-zero",
            "best_support": "WCO1077 states WEP zero if object language, action measure, current owner, and readout/source closure are parent-signed",
            "blocking_evidence": "CLAUSE1077 matrix marks object/action measure conditional unsigned, current/source worldtube/readout missing, material tensor toy-only",
            "contract_coverage": "CTC1445_1 and CTC1445_3 WEP-specific but unsigned",
            "import_decision": "REJECT_IMPORT_WEP_THEOREM_UNSIGNED",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "PAC1446_4_1078_measure_current_owner",
            "source_path": str(source_path("1078-Y5-R10-parent-action-object-language-measure-current-owner-proof-stack.md")),
            "candidate_route": "action-measure and current-owner proof stack",
            "best_support": "AM1078 and CO1078 isolate the needed hbar/action measure and current/source owner proofs",
            "blocking_evidence": "proof stack does not find a signed parent measure/current owner; counterexamples remain live",
            "contract_coverage": "CTC1445_0/1 supporting premise only",
            "import_decision": "REJECT_IMPORT_PREMISES_NOT_PROVEN",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "PAC1446_5_1088_MOMS_conditional_zero",
            "source_path": str(source_path("1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md")),
            "candidate_route": "MOMS ordinary-matter signature conditional zero theorem",
            "best_support": "MOMS1088 clauses imply delta_v S_matter=0 and qbar_XT=0 if all signature clauses are parent-derived",
            "blocking_evidence": "THM1088_6 says required clauses are known but not parent-derived in one action",
            "contract_coverage": "CTC1445_2/3 best theorem-zero route, but conditional only",
            "import_decision": "REJECT_IMPORT_CONDITIONAL_ZERO_ONLY",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "PAC1446_6_1090_MOMS_synthesis",
            "source_path": str(source_path("1090-Y5-R10-MOMS-parent-action-synthesis-or-explicit-missing-axiom-ledger.md")),
            "candidate_route": "derive MOMS from existing contracts",
            "best_support": "SYN1090 synthesizes parent object, quotient pullback, matter lift, constants, no species weights, and no-shadow readout routes",
            "blocking_evidence": "SYN1090_8 fails with missing axioms AX1090_0 through AX1090_4; AX1090 rows are not adopted",
            "contract_coverage": "CTC1445_0/2/3 conditional derivation route",
            "import_decision": "REJECT_IMPORT_MISSING_AXIOMS",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "PAC1446_7_1217_Cparent_map",
            "source_path": str(source_path("1217-Y5-R10-WEP-Cparent-coefficient-map-or-finite-prior-row.md")),
            "candidate_route": "C_parent to material/DD coefficient map",
            "best_support": "CMAP1217 sharpens mass-response formula, alpha/surface operators, same-branch normalization, and no-absorption guard",
            "blocking_evidence": "CMAP1217_5 says C_PARENT map not derived; ZERO1217 vector zero remains conditional not signed",
            "contract_coverage": "CTC1445_2 coefficient definition strongest but no functional derivative or finite source value",
            "import_decision": "REJECT_IMPORT_NO_COEFFICIENT_MAP",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def clause_audit_rows(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_0_parent_action",
            "clause_result": "BLOCKED_CONTRACT_ONLY",
            "best_candidate_ids": "PAC1446_0_1008_parent_theta_Qtau;PAC1446_1_1009_parent_sector_contract;PAC1446_6_1090_MOMS_synthesis",
            "evidence_summary": "parent action blocks and sector contracts exist, but no total parent action is promoted or source-signed",
            "missing_for_import": "single parent action object; field list; first variation; theta/Q ownership; coupling sector signature",
            "clause_satisfied_for_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_1_projection_generator",
            "clause_result": "BLOCKED_PARTIAL_BRANCH_GUARD_ONLY",
            "best_candidate_ids": "PAC1446_2_1016_worldtube_selector;PAC1446_3_1077_WEP_coupling_owner;PAC1446_7_1217_Cparent_map",
            "evidence_summary": "same-branch/source/readout projection contracts exist, but material tensor, source worldtube, K_CMSM, and V_WEP generator are not all signed",
            "missing_for_import": "V_WEP definition; source/readout projector; Ti/Pt material tensor; official readout arrays",
            "clause_satisfied_for_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_2_coefficient_definition",
            "clause_result": "BLOCKED_NO_FUNCTIONAL_DERIVATIVE_OR_ZERO",
            "best_candidate_ids": "PAC1446_5_1088_MOMS_conditional_zero;PAC1446_7_1217_Cparent_map",
            "evidence_summary": "conditional zero and coefficient-map formulas exist, but no normalized delta S_parent / delta V_WEP or DERIVED_ZERO proof is sourced",
            "missing_for_import": "functional derivative definition; units/sign/basis; theorem-zero certificate or finite source-backed coefficient",
            "clause_satisfied_for_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_3_GR_limit",
            "clause_result": "BLOCKED_CONDITIONAL_LOCAL_LIMIT_ONLY",
            "best_candidate_ids": "PAC1446_5_1088_MOMS_conditional_zero;PAC1446_6_1090_MOMS_synthesis",
            "evidence_summary": "MOMS would suppress local WEP/DD current if its parent-action axioms were signed, but AX1090 reduction remains missing",
            "missing_for_import": "AX1090_0 parent object; no hidden-visible hom; common measure; fixed constants; variation-before-readout proof",
            "clause_satisfied_for_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_4_no_bound_inversion",
            "clause_result": "GUARD_CLOSED_NOT_A_DERIVATION",
            "best_candidate_ids": "PAC1446_7_1217_Cparent_map",
            "evidence_summary": "1217 and 1445 reject WEP threshold/bound inversion as a theory coefficient source",
            "missing_for_import": "not applicable; this is a guardrail, not a coefficient source",
            "clause_satisfied_for_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "clause_id": "CTC1445_5_import_condition",
            "clause_result": "BLOCKED_LIVE_IMPORT_ABSENT",
            "best_candidate_ids": "none",
            "evidence_summary": "no live C_parent_WEP_slot_import.csv exists and no candidate satisfies proof-or-source finite coefficient conditions",
            "missing_for_import": "live import row with no placeholders; source path/URL/DOI; units; sign; basis; parent_status",
            "clause_satisfied_for_import": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def import_gate_rows(clause_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": "IMPORT1446_0_C_parent_WEP_slot",
            "target_import_path": str(LIVE_C_PARENT_IMPORT),
            "target_exists": LIVE_C_PARENT_IMPORT.exists(),
            "required_clauses_closed": "CTC1445_0;CTC1445_1;CTC1445_2;CTC1445_3;CTC1445_5",
            "closed_clause_count": sum(str(row["clause_satisfied_for_import"]) == "True" for row in clause_rows),
            "decision": "DO_NOT_CREATE_IMPORT",
            "reason": "corpus contains contracts and conditional zero routes, not a source-signed parent coefficient",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def parser_dryrun_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1446_0_candidate_ledger",
            "target_path": str(BRANCH_CANDIDATES),
            "target_exists": BRANCH_CANDIDATES.exists(),
            "parser_status": "PASS_LEDGER_ONLY_NONCLAIM",
            "refusal_reason": "candidate ledger is evidence triage, not coefficient import",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1446_1_clause_audit",
            "target_path": str(BRANCH_CLAUSE_AUDIT),
            "target_exists": BRANCH_CLAUSE_AUDIT.exists(),
            "parser_status": "PASS_AUDIT_ONLY_NONCLAIM",
            "refusal_reason": "no clause_satisfied_for_import true rows",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1446_2_live_import",
            "target_path": str(LIVE_C_PARENT_IMPORT),
            "target_exists": LIVE_C_PARENT_IMPORT.exists(),
            "parser_status": "REFUSED_LIVE_C_PARENT_IMPORT_ABSENT",
            "refusal_reason": "no source-signed finite coefficient or DERIVED_ZERO certificate",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "dryrun_id": "PDR1446_3_live_readout",
            "target_path": str(LIVE_READOUT),
            "target_exists": LIVE_READOUT.exists(),
            "parser_status": "REFUSED_LIVE_K_CMSM_READOUT_ABSENT",
            "refusal_reason": "readout matrix still absent, so even a future coefficient could not score today",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG1446_0_no_parent_action", "no source-signed total parent action exists"),
        ("CG1446_1_no_V_WEP", "WEP vertical/source projection generator is not parent-defined"),
        ("CG1446_2_no_Cparent_definition", "C_parent_WEP is not a functional derivative or theorem-zero"),
        ("CG1446_3_no_GR_limit", "local GR/Newton suppression mechanism remains conditional"),
        ("CG1446_4_no_import", "live C_parent_WEP_slot_import.csv remains absent"),
        ("CG1446_5_no_readout", "live K_CMSM/readout file remains absent"),
        ("CG1446_6_no_score", "no WEP/local-GR/Newton score or claim is allowed from 1446"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "gate_status": "LOCKED_CLAIM_FALSE",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate in gates
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1446_0_best_current_route",
            "decision": "MOMS/AX1090 remains the best derivation route, not 1009 sector summation alone",
            "why": "1088 gives the cleanest zero theorem if its ordinary-matter signature is parent-derived; 1090 shows exactly which axioms are missing",
            "consequence": "attack AX1090_0 and CTC1445_2 directly next",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1446_1_no_import",
            "decision": "do not create C_parent_WEP_slot_import.csv",
            "why": "all candidates are contracts, conditionals, or finite-prior scaffolds",
            "consequence": "branch remains private/nonclaim",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1446_2_next_functional_derivative",
            "decision": "try to define C_parent_WEP as a parent functional derivative against V_WEP",
            "why": "without this, the local branch cannot honestly reduce to GR/Newton; with it, finite or zero routes become testable",
            "consequence": "1447 targets the functional derivative/source theorem rather than more broad searching",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1446_0_1447",
            "next_target": "1447-Y5-R10-RAB-C-parent-functional-derivative-source-or-AX1090-parent-object-proof.md",
            "script": "scripts/Y5_R10_RAB_C_parent_functional_derivative_source_or_AX1090_parent_object_proof.py",
            "objective": "attempt to construct C_parent_WEP := normalized delta S_parent / delta V_WEP from the strongest MOMS/AX1090 parent-object route; if this cannot be source-signed, record the exact obstruction and keep import blocked.",
            "include": "functional derivative definition; V_WEP domain; parent object proof attempt; clause-by-clause obstruction; no-claim parser dry-run",
            "exclude": "numeric WEP score; local-GR claim; invented coefficient; closure-only zero; bound-inverted coefficient; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_live_scaffolds(candidates: list[dict[str, Any]], audit: list[dict[str, Any]], import_gate: list[dict[str, Any]]) -> None:
    write_csv(BRANCH_CANDIDATES, candidates)
    write_csv(BRANCH_CLAUSE_AUDIT, audit)
    write_csv(BRANCH_IMPORT_GATE, import_gate)


def validation_rows(
    sources: list[dict[str, Any]],
    hits: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    import_gate: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    generated = [
        SOURCE_REGISTER,
        CORPUS_HITS,
        CANDIDATE_LEDGER,
        CLAUSE_AUDIT,
        IMPORT_GATE,
        PARSER_DRYRUN,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        BRANCH_CANDIDATES,
        BRANCH_CLAUSE_AUDIT,
        BRANCH_IMPORT_GATE,
    ]
    all_sources_exist = all(str(row["exists"]) == "True" for row in sources)
    enough_hits = len(hits) >= 20
    enough_candidates = len(candidates) >= 8
    has_wep_candidate = any("WEP" in row["candidate_route"] or "WEP" in row["candidate_id"] for row in candidates)
    all_candidates_false = all(str(row["valid_for_claim"]) == "False" and str(row["claim_allowed"]) == "False" for row in candidates)
    no_clause_import = all(str(row["clause_satisfied_for_import"]) == "False" for row in audit)
    import_blocked = str(import_gate[0]["decision"]) == "DO_NOT_CREATE_IMPORT" and not LIVE_C_PARENT_IMPORT.exists()
    dryrun_false = all(str(row["claim_allowed"]) == "False" for row in dryrun)
    gates_false = all(str(row["claim_allowed"]) == "False" for row in gates)
    readout_absent = not LIVE_READOUT.exists()
    csvs_parse = all(csv_parses(path) for path in generated)
    formalization_recent = 0
    if FORMALIZATION.exists():
        formalization_recent = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)
    checks = [
        ("VAL1446_0_sources", all_sources_exist, "all cited source paths exist"),
        ("VAL1446_1_corpus_hits", enough_hits, f"corpus search produced {len(hits)} parent/coupling hits"),
        ("VAL1446_2_candidate_count", enough_candidates and has_wep_candidate, "candidate ledger includes broad parent and WEP-specific routes"),
        ("VAL1446_3_candidates_nonclaim", all_candidates_false, "all candidate rows remain nonclaim"),
        ("VAL1446_4_clause_audit_blocks", no_clause_import, "no C_parent contract clause is satisfied for import"),
        ("VAL1446_5_import_blocked", import_blocked, "C_parent import remains absent and blocked"),
        ("VAL1446_6_dryrun_false", dryrun_false, "parser dry-run refuses score/import paths"),
        ("VAL1446_7_claim_gates", gates_false, "all claim gates remain false"),
        ("VAL1446_8_readout_absent", readout_absent, "live K_CMSM readout remains absent"),
        ("VAL1446_9_csv_parse", csvs_parse, "all generated 1446 CSVs parse cleanly"),
        ("VAL1446_10_formalization_untouched", formalization_recent == 0, f"formalization modified-file count since start={formalization_recent}"),
        ("VAL1446_11_next_target", True, "1447 handoff written"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail, "generated_utc": now()}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1446_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1446 finds candidate routes but no source-signed C_parent_WEP import route",
            "generated_utc": now(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    hits: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    import_gate: list[dict[str, Any]],
    dryrun: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.parent.mkdir(parents=True, exist_ok=True)
    with DOC.open("w", encoding="utf-8") as handle:
        handle.write("# 1446 - Parent action/coupling source search against C_parent contract\n\n")
        handle.write(
            "**Current verdict:** the corpus contains several serious parent-action/coupling routes, especially "
            "`1009` current-chain sectors, `1016` source selector, `1077` WEP coupling-owner theorem, `1088` MOMS, "
            "`1090` AX/MOMS synthesis, and `1217` Cparent map. None source-signs `C_parent_WEP := normalized "
            "delta S_parent / delta V_WEP`, and none proves a DERIVED_ZERO. The import stays blocked.\n"
        )
        write_table(handle, "Source register", sources)
        write_table(handle, "Corpus search hits", hits[:30])
        write_table(handle, "Parent-action/coupling candidate ledger", candidates)
        write_table(handle, "Contract clause reduction audit", audit)
        write_table(handle, "Import decision gate", import_gate)
        write_table(handle, "Parser dry-run", dryrun)
        write_table(handle, "Claim gates", gates)
        write_table(handle, "Decision ledger", decisions)
        write_table(handle, "Validation", validation)
        write_table(handle, "Next target", next_rows)


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def main() -> None:
    sources = source_register_rows()
    hits = corpus_search_hits()
    candidates = candidate_rows()
    audit = clause_audit_rows(candidates)
    import_gate = import_gate_rows(audit)
    dryrun = parser_dryrun_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_live_scaffolds(candidates, audit, import_gate)
    write_csv(SOURCE_REGISTER, sources)
    write_csv(CORPUS_HITS, hits)
    write_csv(CANDIDATE_LEDGER, candidates)
    write_csv(CLAUSE_AUDIT, audit)
    write_csv(IMPORT_GATE, import_gate)
    write_csv(PARSER_DRYRUN, dryrun)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, hits, candidates, audit, import_gate, dryrun, gates)
    write_csv(VALIDATION, validation)
    write_doc(sources, hits, candidates, audit, import_gate, dryrun, gates, decisions, validation, next_rows)
    remove_pycache()
    print("Y5_R10_1446_parent_action_coupling_search_Cparent_import_blocked")


if __name__ == "__main__":
    main()
