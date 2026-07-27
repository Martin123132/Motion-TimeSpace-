from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


BRANCH = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"

DOC_PATH = ROOT / "1992-Y5-R2FR-EP-template-alignment-lemma-or-source-pack-intake.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1992_VALIDATION.csv"

SOURCES = {
    "1991_doc": {
        "path": ROOT / "1991-Y5-R2FR-WEP-nondegeneracy-certificate-or-parent-Hilbert-owner.md",
        "needles": ["NEXT1991_0_primary", "EPT1991_0_target_statement"],
    },
    "1991_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1991_VALIDATION.csv",
        "needles": ["VAL1991_OVERALL", "PASS"],
    },
    "1601_doc": {
        "path": ROOT / "1601-Y5-R2FR-EP-template-alignment-lemma-or-CMSM-browser-capture.md",
        "needles": ["EPA1601_1_alignment_condition", "EPA1601_2_parent_source_coefficient", "DEC1601_2_next"],
    },
    "1601_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1601_VALIDATION.csv",
        "needles": ["VAL1601_OVERALL", "PASS"],
    },
    "1600_parent_k_vector": {
        "path": ROOT / "1600-Y5-R2FR-MICROSCOPE-HAR-intake-or-parent-K-vector-proof.md",
        "needles": ["KVP1600_1_EP_template_alignment", "PARENT_K_VECTOR_PROOF_NOT_DERIVED"],
    },
    "1599_symbolic_k_bridge": {
        "path": ROOT / "1599-Y5-R2FR-CMSM-capture-parser-or-symbolic-K-bridge.md",
        "needles": ["SKB1599_3_alignment_object", "MISSING_CRITICAL_ALIGNMENT"],
    },
    "1438_source_pack": {
        "path": ROOT / "1438-Y5-R10-RAB-WEP-slot-C-parent-zero-or-official-source-pack-intake.md",
        "needles": ["CPS1438_0_WEP_C_parent", "MISSING_DERIVED_ZERO_OR_NUMERIC_SOURCE"],
    },
    "1440_closure_demote": {
        "path": ROOT / "1440-Y5-R10-RAB-minimal-WEP-parent-clause-proof-obligations-or-closure-demotion.md",
        "needles": ["MPA1440_3_verdict", "DO_NOT_PROMOTE_DEMOTE_TO_CLOSURE_ONLY"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_SOURCE_REGISTER.csv",
    "alignment_review": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_EP_TEMPLATE_ALIGNMENT_REVIEW.csv",
    "cep_contract": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_CEP_CONTRACT.csv",
    "common_mode_zero": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_COMMON_MODE_ZERO_ROUTE.csv",
    "source_pack": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_SOURCE_PACK_FALLBACK.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1992_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "EP_TEMPLATE_ALIGNMENT_REVIEW_1992_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1992_CEP_CONTRACT_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1992_CEP_OR_COMMON_MODE_ZERO_QUEUE.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in OUTPUTS.values():
        path.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_PATH.parent.mkdir(parents=True, exist_ok=True)


def base_row(stamp: str) -> dict[str, str]:
    return {
        "branch_id": BRANCH,
        "valid_for_claim": "false",
        "claim_allowed": "false",
        "generated_utc": stamp,
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register(stamp: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, spec in SOURCES.items():
        path = spec["path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing = [needle for needle in spec["needles"] if needle not in text]
        row = base_row(stamp)
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "needed_for": "1992 EP-template alignment bridge and C_EP route selection",
                "needles": ";".join(spec["needles"]),
                "exists": str(exists),
                "anchor_found": str(exists and not missing),
                "missing_needles": ";".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if exists and not missing else "MISSING_SOURCE_OR_ANCHOR",
            }
        )
        rows.append(row)
    return rows


def build_tables() -> dict[str, list[dict[str, str]]]:
    stamp = now()

    def row(data: dict[str, str]) -> dict[str, str]:
        merged = base_row(stamp)
        merged.update(data)
        return merged

    alignment_review = [
        row(
            {
                "review_id": "EPTREV1992_0_inherited_decomposition",
                "statement": "V_MTS = C_EP*T_EP + V_perp + V_corr, with inner(K_EP,V_perp)=0 by definition",
                "source_basis": "1601 EPA1601_0_decomposition",
                "current_status": "CONDITIONAL_DECOMPOSITION_ACCEPTED",
                "verdict": "USE_AS_EXACT_NONCLAIM_LEMMA",
            }
        ),
        row(
            {
                "review_id": "EPTREV1992_1_sufficient_condition",
                "statement": "If abs(C_EP)*norm(K_EP)*norm(T_EP) > abs(inner(K_EP,V_corr)), then inner(K_EP,V_MTS) is nonzero",
                "source_basis": "1601 EPA1601_1_alignment_condition",
                "current_status": "EXACT_CONDITIONAL_ALIGNMENT_LEMMA",
                "verdict": "DERIVED_CONDITIONALLY_NOT_CLAIM_GRADE",
            }
        ),
        row(
            {
                "review_id": "EPTREV1992_2_blockers",
                "statement": "C_EP, template norm, correction projection bound, and official/readout-equivalent K_EP are not parent-signed or sourced",
                "source_basis": "1601 EPA1601_2_parent_source_coefficient; 1991 EPT1991_4_current_verdict",
                "current_status": "MISSING_PARENT_C_EP_AND_SOURCE_PACK",
                "verdict": "LEMMA_NOT_CLOSED",
            }
        ),
        row(
            {
                "review_id": "EPTREV1992_3_current_checkpoint",
                "statement": "1992 should not redo the 1601 lemma; it should select the smallest missing object",
                "source_basis": "1991 NEXT1991_0_primary; 1601 DEC1601_2_next",
                "current_status": "BRIDGE_CHECKPOINT",
                "verdict": "NEXT_OBJECT_IS_C_EP_OR_COMMON_MODE_ZERO",
            }
        ),
    ]

    cep_contract = [
        row(
            {
                "contract_id": "CEP1992_0_definition",
                "quantity": "C_EP",
                "definition": "coefficient of the finite MTS source-weight residual along the MICROSCOPE Earth-gravity EP template after choosing a common source/material/readout basis",
                "required_derivation": "derive from the parent MTS source coupling; do not fit it from the MICROSCOPE bound",
                "status": "MISSING_PARENT_C_EP",
            }
        ),
        row(
            {
                "contract_id": "CEP1992_1_nonzero_route",
                "quantity": "C_EP != 0",
                "definition": "finite branch contains a differential EP-template component rather than only source renormalization/common-mode response",
                "required_derivation": "parent source map plus Earth source worldtube plus Ti/Pt material contrast gives a signed nonzero template projection",
                "status": "NOT_PARENT_SIGNED",
            }
        ),
        row(
            {
                "contract_id": "CEP1992_2_zero_route",
                "quantity": "C_EP = 0",
                "definition": "finite source-weight branch is pure common-mode or forbidden by a universal Hilbert source owner",
                "required_derivation": "show no species/source-weight slot survives in the parent action or show the projected residual is exactly common-mode",
                "status": "COMMON_MODE_ZERO_THEOREM_NOT_PROVED",
            }
        ),
        row(
            {
                "contract_id": "CEP1992_3_normalization_requirements",
                "quantity": "C_EP units and sign",
                "definition": "basis, normalization, sign/body order, material tensor convention, source worldtube convention, and correction-term convention",
                "required_derivation": "source all conventions before any numeric C_EP row can be claim-grade",
                "status": "MISSING_BASIS_UNITS_AND_SOURCE_PATHS",
            }
        ),
        row(
            {
                "contract_id": "CEP1992_4_claim_status",
                "quantity": "C_EP claim gate",
                "definition": "no nonzero or zero C_EP claim is allowed from 1992",
                "required_derivation": "1993 must either derive the source coefficient or prove the common-mode zero theorem",
                "status": "NONCLAIM_CONTRACT_ONLY",
            }
        ),
    ]

    common_mode_zero = [
        row(
            {
                "route_id": "CMZ1992_0_universal_hilbert_owner",
                "candidate_theorem": "ordinary matter couples through one universal Hilbert source owner with no species/source-weight slot",
                "would_imply": "DeltaW_TiPt=0 and C_EP=0 for this finite WEP source-weight branch",
                "obstruction": "object-language owner theorem remains parent-unsigned",
                "status": "POSSIBLE_CLEAN_GR_ROUTE_NOT_PROVED",
            }
        ),
        row(
            {
                "route_id": "CMZ1992_1_common_source_normalization",
                "candidate_theorem": "the finite residual only renormalizes the common Earth/source response and has no differential Ti/Pt channel",
                "would_imply": "source response can shift common acceleration but not produce MICROSCOPE EP-template differential signal",
                "obstruction": "requires same-basis material response tensor and parent source map",
                "status": "POSSIBLE_COMMON_MODE_ROUTE_NOT_PROVED",
            }
        ),
        row(
            {
                "route_id": "CMZ1992_2_current_status",
                "candidate_theorem": "C_EP=0 by local/source universality",
                "would_imply": "finite WEP branch closes without needing tau_min or official projection data",
                "obstruction": "1440 already demoted the minimal WEP parent clause to closure-only",
                "status": "DO_NOT_PROMOTE_ZERO_THEOREM",
            }
        ),
    ]

    source_pack = [
        row(
            {
                "pack_id": "PACK1992_0_official_readout",
                "object": "official/readout-equivalent K_EP or K_CMSM design matrix",
                "required_for": "source-pack fallback projection inner(K_EP,V_MTS) and c_min",
                "status": "MISSING_OFFICIAL_FILE",
            }
        ),
        row(
            {
                "pack_id": "PACK1992_1_source_worldtube",
                "object": "Earth/source worldtube vector in the same parent basis",
                "required_for": "C_EP source side and finite branch amplitude",
                "status": "MISSING_SOURCE_VECTOR",
            }
        ),
        row(
            {
                "pack_id": "PACK1992_2_material_tensor",
                "object": "Ti/Pt material response tensor and body-order convention",
                "required_for": "differential EP-template component rather than common-mode response",
                "status": "MISSING_FULL_MATERIAL_TENSOR",
            }
        ),
        row(
            {
                "pack_id": "PACK1992_3_correction_bound",
                "object": "bound on inner(K_EP,V_corr)",
                "required_for": "conditional alignment inequality",
                "status": "MISSING_CORRECTION_PROJECTION_BOUND",
            }
        ),
        row(
            {
                "pack_id": "PACK1992_4_C_parent_import",
                "object": "C_parent_WEP zero theorem or numeric source-backed coefficient",
                "required_for": "connect older R10/WEP source-pack branch to C_EP",
                "status": "MISSING_DERIVED_ZERO_OR_NUMERIC_SOURCE",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1992_0_inherit_lemma",
                "check": "accept 1601 conditional EP-template lemma",
                "result": "PASS_CONDITIONAL_NONCLAIM",
                "reason": "the algebraic decomposition and sufficient inequality are already recorded and validated",
            }
        ),
        row(
            {
                "run_id": "RUN1992_1_close_alignment",
                "check": "promote EP-template alignment to claim",
                "result": "FAIL_CEP_AND_CORRECTION_MISSING",
                "reason": "C_EP, template/source basis, and correction bound remain missing",
            }
        ),
        row(
            {
                "run_id": "RUN1992_2_common_mode_zero",
                "check": "prove C_EP=0 by common-mode or Hilbert source owner",
                "result": "FAIL_PARENT_UNSIGNED",
                "reason": "universal source owner remains the clean route, but not yet derived",
            }
        ),
        row(
            {
                "run_id": "RUN1992_3_source_pack_fallback",
                "check": "stage official/source-pack route",
                "result": "FAIL_FILES_MISSING_BUT_QUEUE_READY",
                "reason": "required file classes are explicit but no fake rows are inserted",
            }
        ),
        row(
            {
                "run_id": "RUN1992_4_verdict",
                "check": "1992 route selection",
                "result": "NEXT_1993_CEP_SOURCE_COEFFICIENT_OR_COMMON_MODE_ZERO_THEOREM",
                "reason": "C_EP is the smallest remaining theoretical object; data fallback stays secondary",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1992_0_EP_alignment",
                "claim": "EP-template alignment is proved",
                "status": "FAIL_BLOCKED",
                "reason": "only a conditional sufficient lemma is available",
            }
        ),
        row(
            {
                "gate_id": "CG1992_1_CEP_nonzero",
                "claim": "C_EP is nonzero",
                "status": "FAIL_BLOCKED",
                "reason": "parent source coefficient is missing",
            }
        ),
        row(
            {
                "gate_id": "CG1992_2_CEP_zero",
                "claim": "C_EP is zero by common-mode/source universality",
                "status": "FAIL_BLOCKED",
                "reason": "common-mode zero theorem is not parent-signed",
            }
        ),
        row(
            {
                "gate_id": "CG1992_3_source_pack_score",
                "claim": "official WEP source-pack score can be run",
                "status": "FAIL_BLOCKED",
                "reason": "official readout, source, material, correction, and C_parent rows remain missing",
            }
        ),
        row(
            {
                "gate_id": "CG1992_4_local_GR_Newton",
                "claim": "local GR/Newton source coupling is derived",
                "status": "FAIL_BLOCKED",
                "reason": "neither C_EP zero theorem nor finite nonzero coefficient route closes",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1992_0_bridge_to_1601",
                "decision": "DO_NOT_REDERIVE_EP_TEMPLATE_LEMMA_FROM_SCRATCH",
                "because": "1601 already gives the exact conditional decomposition and alignment inequality",
                "next_action": "use it as a nonclaim lemma and attack C_EP",
            }
        ),
        row(
            {
                "decision_id": "DEC1992_1_next_smallest_unknown",
                "decision": "C_EP_IS_THE_COUPLING_NEEDLE",
                "because": "all later WEP nondegeneracy, tau, and source-pack routes depend on whether the parent residual has a differential EP-template component",
                "next_action": "derive C_EP from parent source coupling or prove C_EP=0 by common-mode/source universality",
            }
        ),
        row(
            {
                "decision_id": "DEC1992_2_fallback",
                "decision": "SOURCE_PACK_FALLBACK_IS_READY_BUT_SECONDARY",
                "because": "data can measure or bound a projection, but it cannot replace the parent coefficient theorem",
                "next_action": "only acquire source-pack rows after the C_EP/common-mode route is explicitly blocked",
            }
        ),
        row(
            {
                "decision_id": "DEC1992_3_claim_status",
                "decision": "NO_WEP_LOCAL_GR_OR_NEWTON_CLAIM",
                "because": "the bridge is useful but still has the coupling unsigned",
                "next_action": "keep all generated rows private and nonclaim",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1992_0_primary",
                "selection_status": "selected",
                "target_doc": "1993-Y5-R2FR-C-EP-source-coefficient-or-common-mode-zero-theorem.md",
                "target_script": "scripts/Y5_R2FR_C_EP_source_coefficient_or_common_mode_zero_theorem_1993.py",
                "task": "derive the parent C_EP source coefficient or prove the finite WEP source-weight residual is exactly common-mode/zero in the EP channel",
                "success_condition": "parent-signed C_EP nonzero with basis/correction obligations, or parent-signed C_EP=0 theorem; otherwise explicit source-pack fallback remains blocked",
                "do_not": "do not infer nonzero overlap from nonzero factors, fit C_EP from the MICROSCOPE bound, promote closure-only universality, modify formalization-workbench, or push GitHub",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1992_0_alignment_review",
                "artifact_type": "EP_template_alignment_bridge",
                "status": "CONDITIONAL_LEMMA_ACCEPTED_CEP_MISSING",
                "source_path": str(DOC_PATH),
                "next_target": "1993-Y5-R2FR-C-EP-source-coefficient-or-common-mode-zero-theorem.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1992_0_C_EP_contract",
                "quantity": "C_EP",
                "required_formula": "V_MTS = C_EP*T_EP + V_perp + V_corr",
                "required_evidence": "parent source coupling, same-basis source worldtube, Ti/Pt material tensor, sign/normalization, correction bound",
                "current_status": "MISSING_PARENT_C_EP",
                "status": "NONCLAIM_SLOT_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1992_0_CEP_or_common_mode_zero",
                "priority": "1",
                "needed_input": "C_EP source coefficient or common-mode zero theorem",
                "route": "derive C_EP from parent source coupling; if that fails, prove the finite residual is common-mode/zero in the EP channel; only then fall back to official source-pack acquisition",
                "required_fields": "parent_source_map;EP_template_basis;source_worldtube;material_tensor;normalization;correction_bound;source_path",
                "blocked_claims": "EP_alignment;C_EP_nonzero;C_EP_zero;tau_min;WEP_pass;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "alignment_review": alignment_review,
        "cep_contract": cep_contract,
        "common_mode_zero": common_mode_zero,
        "source_pack": source_pack,
        "runner_dryrun": runner_dryrun,
        "claim_gate": claim_gate,
        "decision": decision,
        "next": next_target,
        "source_weight": source_weight,
        "wep_coeffs": wep_coeffs,
        "queue": queue,
    }


def validate(tables: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def val(validation_id: str, status: str, detail: str) -> None:
        rows.append(
            {
                "validation_id": validation_id,
                "status": status,
                "detail": detail,
                "valid_for_claim": "false",
                "claim_allowed": "false",
            }
        )

    source_failures = [row for row in tables["source_register"] if row["status"] != "EXISTS_NEEDLES_CONFIRMED"]
    val("VAL1992_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    inherited = any(row["review_id"] == "EPTREV1992_1_sufficient_condition" and row["current_status"] == "EXACT_CONDITIONAL_ALIGNMENT_LEMMA" for row in tables["alignment_review"])
    not_closed = any(row["review_id"] == "EPTREV1992_2_blockers" and row["verdict"] == "LEMMA_NOT_CLOSED" for row in tables["alignment_review"])
    val("VAL1992_01_alignment_review", "PASS" if inherited and not_closed else "FAIL", "conditional EP-template lemma inherited without promotion")

    cep_missing = any(row["contract_id"] == "CEP1992_0_definition" and row["status"] == "MISSING_PARENT_C_EP" for row in tables["cep_contract"])
    cep_nonclaim = any(row["contract_id"] == "CEP1992_4_claim_status" and row["status"] == "NONCLAIM_CONTRACT_ONLY" for row in tables["cep_contract"])
    val("VAL1992_02_CEP_contract", "PASS" if cep_missing and cep_nonclaim else "FAIL", "C_EP is isolated as missing parent coefficient")

    zero_safe = any(row["route_id"] == "CMZ1992_2_current_status" and row["status"] == "DO_NOT_PROMOTE_ZERO_THEOREM" for row in tables["common_mode_zero"])
    val("VAL1992_03_common_mode_zero", "PASS" if zero_safe else "FAIL", "common-mode zero route retained but not promoted")

    source_pack_blocks = all("MISSING" in row["status"] for row in tables["source_pack"])
    val("VAL1992_04_source_pack", "PASS" if source_pack_blocks else "FAIL", "source-pack fallback remains explicitly blocked")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "NEXT_1993_CEP_SOURCE_COEFFICIENT_OR_COMMON_MODE_ZERO_THEOREM"
    val("VAL1992_05_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects C_EP/common-mode zero next")

    gates_safe = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    val("VAL1992_06_claim_gates", "PASS" if gates_safe else "FAIL", "all claim gates blocked")

    next_ok = tables["next"][0]["target_doc"] == "1993-Y5-R2FR-C-EP-source-coefficient-or-common-mode-zero-theorem.md"
    val("VAL1992_07_next_target", "PASS" if next_ok else "FAIL", "1993 C_EP/common-mode zero target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1992_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1992_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1992_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        formalization_artifacts = [path for path in FORMALIZATION.rglob("*1992*")]
    val("VAL1992_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1992_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1992_OVERALL", overall, "1992 EP-template alignment lemma bridge and C_EP route selection")
    return rows


def markdown_table(rows: list[dict[str, str]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("EP-Template Alignment Review", tables["alignment_review"]),
        ("C_EP Contract", tables["cep_contract"]),
        ("Common-Mode Zero Route", tables["common_mode_zero"]),
        ("Source-Pack Fallback", tables["source_pack"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1992 Y5 R2FR: EP-Template Alignment Lemma Or Source-Pack Intake",
        "",
        "Private checkpoint. This bridges the 1991 sharpened target to the older 1601 EP-template lemma without pretending the WEP/local-GR route is closed.",
        "",
        "Verdict: the EP-template alignment lemma is already conditionally derived in the useful form `V_MTS = C_EP*T_EP + V_perp + V_corr`. The exact sufficient condition is `abs(C_EP)*norm(K_EP)*norm(T_EP) > abs(inner(K_EP,V_corr))`. That is progress, but it is not claim-grade because `C_EP`, the readout/source basis, template normalization, and correction bound are still missing.",
        "",
        "Meaning: the coupling really is the needle. The next derivation target is the parent coefficient `C_EP`, or the cleaner theorem that `C_EP=0` because the finite branch is exactly common-mode/source-universal in the EP channel.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1992.",
        "",
    ]
    for title, rows in sections:
        lines.extend([f"## {title}", "", markdown_table(rows), ""])
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    ensure_dirs()
    pycache_path = ROOT / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    tables = build_tables()
    for output_name, path in OUTPUTS.items():
        write_csv(path, tables[output_name])
    validation_rows = validate(tables)
    write_csv(VALIDATION_PATH, validation_rows)
    write_markdown(tables, validation_rows)
    if pycache_path.exists():
        shutil.rmtree(pycache_path)
    overall = validation_rows[-1]["status"]
    print(f"wrote {DOC_PATH}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"VAL1992_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
