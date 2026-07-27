from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_HAMILTONIAN_CHARGE_EXTRACTION_POSITIVITY_PACK_OR_DENOMINATOR_BLOCK_2461"
CHECKPOINT_ID = "2461"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
HAMILTONIAN = ROOT / "source-intake" / "hamiltonian-source"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2461-Y5-R2FR-parent-Hamiltonian-charge-extraction-positivity-pack-or-denominator-block.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2461_SOURCE_REGISTER.csv",
    "pack_requirements": OUT / "P8_Y5_PARENT_QLOC_2461_CHARGE_POSITIVITY_PACK_REQUIREMENTS.csv",
    "pack_fit_matrix": OUT / "P8_Y5_PARENT_QLOC_2461_EXISTING_SOURCE_PACK_FIT_MATRIX.csv",
    "denominator_block": OUT / "P8_Y5_PARENT_QLOC_2461_DENOMINATOR_BLOCK_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2461_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2461_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2461_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2461_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2461_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_requirements": QUEUE / "JR2461_CHARGE_POSITIVITY_PACK_REQUIREMENTS_NONCLAIM.csv",
    "queue_fit_matrix": QUEUE / "JR2461_EXISTING_SOURCE_PACK_FIT_MATRIX_NONCLAIM.csv",
    "hamiltonian_block": HAMILTONIAN / "Hamiltonian_denominator_block_ledger_2461_NONCLAIM.csv",
    "local_block": LOCAL_BOUNDS / "Local_scoring_denominator_block_2461_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2461_00_2460_doc",
        "source_path": ROOT / "2460-Y5-R2FR-same-frame-Hamiltonian-denominator-derivation-or-retain-local-bound-block.md",
        "needles": ["HDC2460_7_current_verdict", "POS2460_5_energy_condition", "NEXT2460_0_selected", "VAL2460_OVERALL"],
        "role": "handoff: denominator contract exact but unsigned",
    },
    {
        "source_id": "SRC2461_01_2460_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2460_HAMILTONIAN_DENOMINATOR_CONTRACT.csv",
        "needles": ["HDC2460_1_parent_charge_extraction", "HDC2460_6_positivity", "FAIL_CURRENT_CLAIM_BUT_EXACT_CONTRACT_WRITTEN"],
        "role": "machine-readable denominator clauses",
    },
    {
        "source_id": "SRC2461_02_1008_theta_Qtau",
        "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "needles": ["PVA1008_6_verdict", "QTA1008_8_Q_total", "CG1008_5_MHref", "V1008_SUMMARY"],
        "role": "Noether charge extraction partial pack",
    },
    {
        "source_id": "SRC2461_03_1009_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "needles": ["PCS1009_9_total_parent_contract", "CG1009_5_Htau_MHref_local_GR", "DEC1009_0_contract_not_parent_action", "V1009_SUMMARY"],
        "role": "parent current-chain sector pack",
    },
    {
        "source_id": "SRC2461_04_1015_same_object",
        "source_path": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "needles": ["SOL1015_6_verdict", "HEA1015_8_verdict", "REB1015_5_M_H_ref", "V1015_SUMMARY"],
        "role": "Hilbert/topological same-object pack",
    },
    {
        "source_id": "SRC2461_05_1016_worldtube",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "needles": ["PSC1016_5_dressed_source_charge", "PST1016_1_source_measure_lemma", "CG1016_2_M_H_ref_claim", "V1016_SUMMARY"],
        "role": "worldtube/source-measure bridge pack",
    },
    {
        "source_id": "SRC2461_06_1030_matter_frame",
        "source_path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "needles": ["SPM1030_3_total_Hilbert_source", "SPM1030_6_contract_verdict", "DEC1030_2_contract_status", "V1030_SUMMARY"],
        "role": "single public metric / Hilbert source pack",
    },
]

REQUIREMENTS = [
    ("REQ2461_0_parent_action", "single parent action/current-chain variation", "delta L_parent=E_A delta Phi^A+d theta_MTS with all retained sectors", "required before any Q_tau total"),
    ("REQ2461_1_Qtau_total", "parent-owned Q_tau^MTS total", "J_tau=dQ_tau^MTS+C_tau with EH, boundary, extra, projector and matter/source pieces owned", "required before H_tau exists"),
    ("REQ2461_2_integrability", "integrable fixed-reference H_tau", "field-space curl zero and H_ref fixed before readout", "required before M_H_ref is a number"),
    ("REQ2461_3_same_frame", "single tau/coframe/public metric", "same observed frame for matter source, Hamiltonian charge, clocks, rods and readout", "required before denominator normalizes residuals"),
    ("REQ2461_4_worldtube_bridge", "parent-selected compact Hilbert source worldtube", "W_source=closure(supp J_H[tau]) with linking surfaces fixed before readout", "required before charge is source mass"),
    ("REQ2461_5_positivity", "source positivity and extra-sector lower bound", "ordinary source charge nonnegative/nonzero and retained sectors cannot make total denominator nonpositive", "required before division by M_H_ref"),
    ("REQ2461_6_no_shortcuts", "no orbital GM, fitted mass, fitted reference or EH-only import", "denominator cannot be copied from target Newton/GR readout or reference convention", "required to keep derivation honest"),
]

CANDIDATES = [
    {
        "candidate_id": "CAND2461_1008_theta_Qtau",
        "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
        "covers": ["REQ2461_1_Qtau_total"],
        "partial": ["REQ2461_0_parent_action", "REQ2461_6_no_shortcuts"],
        "blocker": "theta/Q_tau extraction contract exists but Q_tau total is not promoted",
    },
    {
        "candidate_id": "CAND2461_1009_current_chain",
        "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
        "covers": ["REQ2461_0_parent_action"],
        "partial": ["REQ2461_1_Qtau_total", "REQ2461_6_no_shortcuts"],
        "blocker": "sector blocks are candidates; total parent action switch rejected without certificates",
    },
    {
        "candidate_id": "CAND2461_1015_same_object",
        "source_path": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "covers": [],
        "partial": ["REQ2461_4_worldtube_bridge", "REQ2461_6_no_shortcuts"],
        "blocker": "same-object lemma is conditional; parent worldtube/source-measure/class hypotheses unsigned",
    },
    {
        "candidate_id": "CAND2461_1016_worldtube",
        "source_path": ROOT / "1016-Y5-R10-parent-worldtube-source-measure-selector-or-R_eq-first-input.md",
        "covers": [],
        "partial": ["REQ2461_3_same_frame", "REQ2461_4_worldtube_bridge", "REQ2461_6_no_shortcuts"],
        "blocker": "source selector and M_H_ref are exact contracts but not current theorem",
    },
    {
        "candidate_id": "CAND2461_1030_matter_frame",
        "source_path": ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md",
        "covers": [],
        "partial": ["REQ2461_3_same_frame", "REQ2461_5_positivity", "REQ2461_6_no_shortcuts"],
        "blocker": "single-public-metric/matter functor domain is written but not parent-signed; no positivity theorem",
    },
    {
        "candidate_id": "CAND2461_2460_denominator_contract",
        "source_path": ROOT / "2460-Y5-R2FR-same-frame-Hamiltonian-denominator-derivation-or-retain-local-bound-block.md",
        "covers": ["REQ2461_6_no_shortcuts"],
        "partial": ["REQ2461_0_parent_action", "REQ2461_1_Qtau_total", "REQ2461_2_integrability", "REQ2461_3_same_frame", "REQ2461_4_worldtube_bridge", "REQ2461_5_positivity"],
        "blocker": "exact denominator contract but all theorem-producing clauses unsigned",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: bool) -> str:
    return "True" if value else "False"


def metadata(valid_for_claim: bool = False, claim_allowed: bool = False) -> dict[str, str]:
    return {
        "timestamp_utc": stamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": truth(valid_for_claim),
        "claim_allowed": truth(claim_allowed),
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def cell(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def table(columns: list[str], rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                **metadata(),
                "source_id": source["source_id"],
                "source_path": str(path),
                "exists": truth(path.exists()),
                "needles": ";".join(source["needles"]),
                "missing_needles": ";".join(missing),
                "source_pass": truth(path.exists() and not missing),
                "role": source["role"],
            }
        )
    return rows


def pack_requirement_rows() -> list[dict[str, Any]]:
    return [
        {
            **metadata(),
            "requirement_id": req_id,
            "required_clause": clause,
            "mathematical_form": form,
            "why_required": why,
            "current_pack_status": "REQUIRED_NOT_SATISFIED",
        }
        for req_id, clause, form, why in REQUIREMENTS
    ]


def pack_fit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for candidate in CANDIDATES:
        path = Path(candidate["source_path"])
        for req_id, clause, _form, _why in REQUIREMENTS:
            if req_id in candidate["covers"]:
                fit = "CONTRACT_COVERS_BUT_NOT_PROMOTED"
            elif req_id in candidate["partial"]:
                fit = "PARTIAL_ONLY"
            else:
                fit = "NO_COVERAGE"
            rows.append(
                {
                    **metadata(),
                    "candidate_id": candidate["candidate_id"],
                    "source_path": str(path),
                    "requirement_id": req_id,
                    "required_clause": clause,
                    "fit_status": fit,
                    "promote_pack_clause": "False",
                    "blocker": candidate["blocker"],
                }
            )
    return rows


def denominator_block_rows(matrix_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    requirement_ids = [req[0] for req in REQUIREMENTS]
    promoted = {
        req_id: [
            row["candidate_id"]
            for row in matrix_rows
            if row["requirement_id"] == req_id and row["promote_pack_clause"] == "True"
        ]
        for req_id in requirement_ids
    }
    missing = [req_id for req_id, sources in promoted.items() if not sources]
    rows = [
        {
            "block_id": "DBL2461_0_pack_assembly",
            "question": "Can existing source fragments assemble a claim-grade M_H_ref pack?",
            "result": "NO",
            "missing_requirements": ";".join(missing),
            "effect": "M_H_ref/N_E remains invalid for claim",
            "claim_allowed": "False",
        },
        {
            "block_id": "DBL2461_1_what_is_reusable",
            "question": "Are the fragments useless?",
            "result": "NO_PARTIAL_CONTRACTS_REUSABLE",
            "missing_requirements": "one-parent ownership and parent signatures",
            "effect": "reuse 1008/1009/1016/1030 as pack clauses, not as evidence",
            "claim_allowed": "False",
        },
        {
            "block_id": "DBL2461_2_local_scoring",
            "question": "May finite Delta_ref/local PPN scoring proceed?",
            "result": "NO",
            "missing_requirements": "valid positive same-frame denominator",
            "effect": "RUN2459_live and local-GR gates remain blocked",
            "claim_allowed": "False",
        },
    ]
    return [{**metadata(), **row, "valid_for_claim": "False"} for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2461_0_pack_requirements_written",
            "claim": "Charge-extraction/positivity pack requirements are explicit.",
            "gate_status": "PASS",
            "reason": "2461 lists parent action, Q_tau, integrability, frame, worldtube, positivity and no-shortcut clauses",
            "gate_pass": "True",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2461_1_pack_assembled",
            "claim": "Existing sources assemble into a claim-grade denominator pack.",
            "gate_status": "BLOCKED",
            "reason": "all existing sources are partial or contract-only; none promote clauses",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2461_2_positivity",
            "claim": "Parent energy/source positivity theorem exists for M_H_ref.",
            "gate_status": "BLOCKED",
            "reason": "matter/source positivity and extra-sector lower bounds are not parent-signed",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2461_3_denominator",
            "claim": "M_H_ref/N_E can normalize live residuals.",
            "gate_status": "BLOCKED",
            "reason": "pack assembly fails and denominator remains invalid for claim",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE2461_4_local_GR",
            "claim": "Local GR/Newton/PPN branch passes.",
            "gate_status": "BLOCKED",
            "reason": "no denominator, no finite local residual score, no local-GR claim",
            "gate_pass": "False",
            "claim_allowed": "False",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2461_0_no_pack_promotion",
            "decision": "Do not promote a denominator pack from existing fragments.",
            "reason": "the fragments are useful contracts but none are parent-signed in one chain",
            "effect": "M_H_ref remains blocked",
        },
        {
            "decision_id": "DEC2461_1_reusable_spine",
            "decision": "Keep 1008/1009/1016/1030 as the reusable denominator spine.",
            "reason": "they cover the right clauses: charge extraction, parent sectors, worldtube/source, and public matter frame",
            "effect": "future derivation can stitch these only through one parent action",
        },
        {
            "decision_id": "DEC2461_2_next_best_target",
            "decision": "Attack the parent current-chain action first, not positivity first.",
            "reason": "positivity of a nonexistent Q_tau is meaningless; the charge object must exist before an energy theorem can apply",
            "effect": "next target should try to promote or demote the minimal parent current-chain action",
        },
        {
            "decision_id": "DEC2461_3_local_scoring_block",
            "decision": "Keep local finite-bound scoring blocked.",
            "reason": "normalization remains invalid and orbital/fitted shortcuts are forbidden",
            "effect": "the local branch stays rigorous rather than post-hoc",
        },
    ]
    return [{**metadata(), **row} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2461_0_selected",
            "selection_status": "selected",
            "target_file": "2462-Y5-R2FR-minimal-parent-current-chain-promotion-or-denominator-final-block.md",
            "target_script": "scripts/Y5_R2FR_minimal_parent_current_chain_promotion_or_denominator_final_block_2462.py",
            "task": "try to promote the minimal parent current-chain action enough to own theta_MTS and Q_tau^MTS; if not, mark the Hamiltonian denominator unavailable until new parent-action material is supplied",
            "acceptance_target": "single parent action field list, sector variations, theta/Q_tau pieces and fixed-reference convention, or explicit final denominator-block ledger",
            "guardrails": "no EH-only charge import; no stitched contracts as theorem; no orbital-GM denominator; no fitted reference; no local-GR claim; no GitHub",
        }
    ]
    return [{**metadata(), **row} for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_requirements", OUTPUTS["pack_requirements"], COPY_TARGETS["queue_requirements"]),
        ("queue_fit_matrix", OUTPUTS["pack_fit_matrix"], COPY_TARGETS["queue_fit_matrix"]),
        ("hamiltonian_block", OUTPUTS["denominator_block"], COPY_TARGETS["hamiltonian_block"]),
        ("local_block", OUTPUTS["denominator_block"], COPY_TARGETS["local_block"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            {
                **metadata(),
                "copy_id": copy_id,
                "source_path": str(source),
                "target_path": str(target),
                "source_exists": truth(source.exists()),
                "target_exists": truth(target.exists()),
            }
        )
    return rows


def csv_parse_status(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as exc:  # pragma: no cover - diagnostic only
        return False, 0, repr(exc)


def formalization_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return list(FORMALIZATION.rglob("*2461*"))


def validation_rows(
    source_rows: list[dict[str, Any]],
    req_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    block_rows: list[dict[str, Any]],
    gate_rows: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail})

    add("VAL2461_00_sources_exist", all(row["source_pass"] == "True" for row in source_rows), "all cited source paths exist and needles are present", ";".join(row["source_id"] for row in source_rows if row["source_pass"] != "True"))
    add("VAL2461_01_requirements_complete", len(req_rows) == len(REQUIREMENTS), "charge-extraction/positivity requirements are complete", str(len(req_rows)))
    add("VAL2461_02_matrix_complete", len(matrix_rows) == len(REQUIREMENTS) * len(CANDIDATES), "candidate matrix covers each requirement/source pair", str(len(matrix_rows)))
    add("VAL2461_03_no_promotions", all(row["promote_pack_clause"] == "False" for row in matrix_rows), "no partial source is promoted as claim-grade")
    add("VAL2461_04_denominator_block_written", any(row["result"] == "NO" and row["block_id"] == "DBL2461_0_pack_assembly" for row in block_rows), "denominator block ledger records failed pack assembly")
    add("VAL2461_05_local_scoring_blocked", any(row["block_id"] == "DBL2461_2_local_scoring" and row["claim_allowed"] == "False" for row in block_rows), "local finite scoring remains blocked")
    add("VAL2461_06_claim_gates_safe", all(row["claim_allowed"] == "False" for row in gate_rows) and any(row["gate_id"] == "GATE2461_4_local_GR" and row["gate_status"] == "BLOCKED" for row in gate_rows), "local-GR/PPN/Newton claims remain blocked")
    add("VAL2461_07_next_target_written", len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2461_0_selected", "2462 minimal current-chain target selected")
    add("VAL2461_08_branch_copies", len(branch_rows) == 4 and all(row["target_exists"] == "True" for row in branch_rows), "nonclaim branch copies exist")
    hits = formalization_hits()
    add("VAL2461_09_no_formalization_artifacts", not hits, "no 2461 artifacts were written to formalization-workbench", ";".join(str(path) for path in hits))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2461_CSV_{path.stem}", ok, f"CSV parses with {count} rows" if ok else "CSV parse failed", detail or str(path))

    for key, path in COPY_TARGETS.items():
        ok, count, detail = csv_parse_status(path)
        add(f"VAL2461_COPY_CSV_{key}", ok, f"copy CSV parses with {count} rows" if ok else "copy CSV parse failed", detail or str(path))

    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2461_OVERALL", overall, "2461 assembles the denominator pack matrix, finds no promotable pack, and keeps denominator/local scoring blocked")
    return [{**metadata(), **row} for row in rows]


def write_doc(
    sources: list[dict[str, Any]],
    req_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    block_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    nonzero_matrix = [row for row in matrix_rows if row["fit_status"] != "NO_COVERAGE"]
    doc = "\n\n".join(
        [
            "# 2461 Y5 R2FR Parent Hamiltonian Charge Extraction Positivity Pack Or Denominator Block",
            "**Status:** denominator source-pack assembly attempted. Existing work contains useful partial clauses, but no coherent parent-signed pack for `theta_MTS`, `Q_tau^MTS`, fixed `H_ref`, same-frame source, worldtube bridge and positivity. `M_H_ref/N_E` remains blocked.",
            "**Private reading:** we found the spine, not the living animal. The reusable pieces are real, but stitching them together as a theorem would be cheating unless one parent action owns the chain.",
            "## Source Register\n" + table(["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"], sources),
            "## Charge Positivity Pack Requirements\n" + table(["requirement_id", "required_clause", "mathematical_form", "why_required", "current_pack_status"], req_rows),
            "## Existing Source Pack Fit Matrix\n" + table(["candidate_id", "requirement_id", "required_clause", "fit_status", "promote_pack_clause", "blocker"], nonzero_matrix),
            "## Denominator Block Ledger\n" + table(["block_id", "question", "result", "missing_requirements", "effect", "claim_allowed"], block_rows),
            "## Claim Gates\n" + table(["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"], gates),
            "## Decision Ledger\n" + table(["decision_id", "decision", "reason", "effect"], decisions),
            "## Next Target\n" + table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], next_rows),
            "## Branch Copies\n" + table(["copy_id", "source_path", "target_path", "source_exists", "target_exists"], branch_rows),
            "## Validation\n" + table(["check_id", "status", "notes", "detail"], validations),
        ]
    )
    DOC.write_text(doc + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    requirements = pack_requirement_rows()
    matrix = pack_fit_rows()
    blocks = denominator_block_rows(matrix)
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["pack_requirements"], requirements)
    write_csv(OUTPUTS["pack_fit_matrix"], matrix)
    write_csv(OUTPUTS["denominator_block"], blocks)
    write_csv(OUTPUTS["claim_gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next_target"], next_rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    validations = validation_rows(sources, requirements, matrix, blocks, gates, next_rows, branch_rows)
    write_csv(OUTPUTS["validation"], validations)
    write_doc(sources, requirements, matrix, blocks, gates, decisions, next_rows, branch_rows, validations)

    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
