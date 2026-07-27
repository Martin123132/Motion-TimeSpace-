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

DOC_PATH = ROOT / "1991-Y5-R2FR-WEP-nondegeneracy-certificate-or-parent-Hilbert-owner.md"
VALIDATION_PATH = MTS_RESIDUALS / "P8_Y5_BRR545_1991_VALIDATION.csv"

SOURCES = {
    "1990_doc": {
        "path": ROOT / "1990-Y5-R2FR-tau-WEP-lower-bound-or-Hilbert-source-signature.md",
        "needles": ["NEXT1990_0_primary", "CERT1990_3_alignment_floor"],
    },
    "1990_validation": {
        "path": MTS_RESIDUALS / "P8_Y5_BRR545_1990_VALIDATION.csv",
        "needles": ["VAL1990_OVERALL", "PASS"],
    },
    "1598_nondeg": {
        "path": ROOT / "1598-Y5-R2FR-official-MICROSCOPE-readout-or-parent-nondegeneracy.md",
        "needles": ["MKS1598_3_alignment", "MISSING_CRITICAL_ALIGNMENT"],
    },
    "1600_k_vector": {
        "path": ROOT / "1600-Y5-R2FR-MICROSCOPE-HAR-intake-or-parent-K-vector-proof.md",
        "needles": ["KVP1600_1_EP_template_alignment", "NO_EP_TEMPLATE_ALIGNMENT_PROOF"],
    },
    "1438_source_pack": {
        "path": ROOT / "1438-Y5-R10-RAB-WEP-slot-C-parent-zero-or-official-source-pack-intake.md",
        "needles": ["PACK1438_0_official_readout", "MISSING_OFFICIAL_FILE"],
    },
    "1440_parent_clause": {
        "path": ROOT / "1440-Y5-R10-RAB-minimal-WEP-parent-clause-proof-obligations-or-closure-demotion.md",
        "needles": ["MPA1440_3_verdict", "DO_NOT_PROMOTE_DEMOTE_TO_CLOSURE_ONLY"],
    },
    "1936_hilbert": {
        "path": ROOT / "1936-Y5-R2FR-source-weight-universality-theorem-or-TiPt-material-charge-ledger.md",
        "needles": ["UNIV1936_1_hilbert_source_theorem", "UNIVERSALITY_NOT_DERIVED"],
    },
    "1988_hilbert": {
        "path": ROOT / "1988-Y5-R2FR-action-weight-source-beta-theorem-or-finite-row-fill.md",
        "needles": ["THM1988_0_parent_form", "THEOREM_NOT_CLOSED_CURRENT_CORPUS"],
    },
}

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_SOURCE_REGISTER.csv",
    "certificate_audit": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_NONDEGENERACY_CERTIFICATE_AUDIT.csv",
    "ep_template": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_EP_TEMPLATE_ALIGNMENT_LEMMA_CONTRACT.csv",
    "parent_owner": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_PARENT_HILBERT_OWNER_GATE.csv",
    "source_pack": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_SOURCE_PACK_SCORE_ROUTE.csv",
    "runner_dryrun": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_RUNNER_DRYRUN.csv",
    "claim_gate": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_CLAIM_GATE.csv",
    "decision": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_DECISION_LEDGER.csv",
    "next": MTS_RESIDUALS / "P8_Y5_PARENT_QLOC_1991_NEXT_TARGET.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "WEP_NONDEGENERACY_OR_PARENT_HILBERT_OWNER_1991_NONCLAIM.csv",
    "wep_coeffs": MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1991_EP_TEMPLATE_ALIGNMENT_CONTRACT_NONCLAIM.csv",
    "queue": RAB_QUEUE / "JR1991_EP_TEMPLATE_ALIGNMENT_OR_SOURCE_PACK_QUEUE.csv",
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
                "needed_for": "1991 WEP nondegeneracy certificate or parent Hilbert owner",
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

    certificate_audit = [
        row(
            {
                "cert_id": "NDC1991_0_target",
                "target": "prove |<K_CMSM,V_MTS>| >= c_min ||K_CMSM|| ||V_MTS|| with c_min>0",
                "evidence_needed": "official/readout-equivalent K_CMSM, same-basis V_MTS, norms, sign convention, uncertainty, or parent theorem fixing nonzero overlap",
                "current_status": "TARGET_SHARPENED_NOT_PROVED",
                "verdict": "NONDEGENERACY_NOT_CERTIFIED",
            }
        ),
        row(
            {
                "cert_id": "NDC1991_1_data_route",
                "target": "official CMSM/readout source pack gives projection value and c_min",
                "evidence_needed": "filelist/checksum/readout arrays/source worldtube/material tensor/product convention/sign/body order",
                "current_status": "OFFICIAL_SOURCE_PACK_MISSING",
                "verdict": "DATA_CERTIFICATE_NOT_AVAILABLE",
            }
        ),
        row(
            {
                "cert_id": "NDC1991_2_parent_route",
                "target": "parent geometry forces V_MTS outside ker(K_CMSM)",
                "evidence_needed": "EP-template alignment, window nonannihilation, correction noncancellation, source/material vector nonzero",
                "current_status": "PARENT_K_VECTOR_PROOF_NOT_DERIVED",
                "verdict": "THEOREM_CERTIFICATE_NOT_AVAILABLE",
            }
        ),
        row(
            {
                "cert_id": "NDC1991_3_fake_certificate_rejection",
                "target": "reject nonzero-factor shortcut",
                "evidence_needed": "alignment/coercivity, not just nonzero K and nonzero V",
                "current_status": "ORTHOGONALITY_NO_GO_ACTIVE",
                "verdict": "SHORTCUT_REJECTED",
            }
        ),
    ]

    ep_template = [
        row(
            {
                "lemma_id": "EPT1991_0_target_statement",
                "lemma": "MTS finite source-weight residual has a nonzero component in the MICROSCOPE EP-template channel",
                "formal_target": "Proj_EP[V_MTS] != 0, or stronger |Proj_EP[V_MTS]| >= e_min ||V_MTS|| with e_min>0",
                "why_first": "it is the first sublemma of the full K-vector nondegeneracy proof; without it, session/readout details cannot rescue tau_min",
                "current_status": "TARGET_SHARPENED",
            }
        ),
        row(
            {
                "lemma_id": "EPT1991_1_required_source_side",
                "lemma": "source residual contains Earth-gravity EP-frequency component rather than only common-mode or source-renormalization terms",
                "formal_target": "V_MTS = V_EP + V_perp with V_EP nonzero in the reported differential channel",
                "why_first": "MICROSCOPE reports an EP-template differential channel; an MTS source residual orthogonal to that template is invisible",
                "current_status": "NOT_PARENT_SIGNED",
            }
        ),
        row(
            {
                "lemma_id": "EPT1991_2_required_material_side",
                "lemma": "Ti/Pt material/source response has nonzero contrast in the same parent basis",
                "formal_target": "DeltaR_TiPt · C_parent not zero or theorem-zero branch declared",
                "why_first": "no material contrast means no WEP differential response even if source/readout is nonzero",
                "current_status": "FULL_MATERIAL_TENSOR_MISSING",
            }
        ),
        row(
            {
                "lemma_id": "EPT1991_3_window_and_correction_later",
                "lemma": "session windows, masks, and correction terms do not annihilate the EP component",
                "formal_target": "W_session K_EP V_EP remains nonzero after official masks/corrections",
                "why_first": "this is downstream of EP-template existence; do not attack full readout before source-template lemma",
                "current_status": "DEFER_UNTIL_EP_TEMPLATE_COMPONENT_EXISTS",
            }
        ),
        row(
            {
                "lemma_id": "EPT1991_4_current_verdict",
                "lemma": "Can current corpus prove EP-template alignment now?",
                "formal_target": "parent-signed EPT1991_0 through EPT1991_2",
                "why_first": "would yield the first genuine nondegeneracy bridge toward tau_min",
                "current_status": "LEMMA_NOT_DERIVED_CURRENT_CORPUS",
            }
        ),
    ]

    parent_owner = [
        row(
            {
                "owner_id": "OWN1991_0_hilbert_owner_target",
                "claim_if_signed": "one universal Hilbert source owner for ordinary matter, no species/source-weight slot, readout preserves the owner",
                "consequence": "DeltaW_TiPt=0 and WEP source-weight residual vanishes without tau_min",
                "current_status": "CONDITIONAL_THEOREM_EXACT_PARENT_UNSIGNED",
                "remaining_gap": "no-source-weight object language, common measure/current owner, readout preservation",
            }
        ),
        row(
            {
                "owner_id": "OWN1991_1_closure_warning",
                "claim_if_signed": "minimal WEP parent clause is adopted",
                "consequence": "would be closure-only unless derived from the parent action",
                "current_status": "DEMOTED_TO_CLOSURE_ONLY_IN_1440",
                "remaining_gap": "AX1090/MOMS obligations not reduced to MTS primitives",
            }
        ),
        row(
            {
                "owner_id": "OWN1991_2_current_status",
                "claim_if_signed": "parent Hilbert owner closes local WEP source coupling",
                "consequence": "supports GR/Newton-compatible source universality",
                "current_status": "DO_NOT_PROMOTE",
                "remaining_gap": "source owner theorem still missing; finite route remains active",
            }
        ),
    ]

    source_pack = [
        row(
            {
                "pack_id": "PACK1991_0_official_readout",
                "object": "K_CMSM/readout design matrix",
                "status": "MISSING_OFFICIAL_FILE",
                "required_for": "data-side c_min and tau/P lower-bound certificate",
            }
        ),
        row(
            {
                "pack_id": "PACK1991_1_source_worldtube",
                "object": "Earth/source worldtube vector",
                "status": "MISSING_SOURCE_VECTOR",
                "required_for": "same-basis V_MTS source side",
            }
        ),
        row(
            {
                "pack_id": "PACK1991_2_material_tensor",
                "object": "TA6V-minus-PtRh10 material response tensor",
                "status": "MISSING_FULL_MATERIAL_TENSOR",
                "required_for": "same-basis V_MTS material contrast",
            }
        ),
        row(
            {
                "pack_id": "PACK1991_3_product_convention",
                "object": "eta product normalization and sign/body order",
                "status": "MISSING_PRODUCT_CONVENTION_FILE",
                "required_for": "claim-grade projection value and tau convention",
            }
        ),
        row(
            {
                "pack_id": "PACK1991_4_c_parent",
                "object": "C_parent_WEP derived zero or numeric coefficient",
                "status": "NOT_ZERO_CERTIFIED_NO_NUMERIC_ROW",
                "required_for": "finite source-weight comparison or zero theorem",
            }
        ),
    ]

    runner_dryrun = [
        row(
            {
                "run_id": "RUN1991_0_full_nondegeneracy",
                "check": "full tau/P nondegeneracy certificate",
                "result": "FAIL_CERTIFICATE_MISSING",
                "reason": "official data and parent K-vector theorem are both missing",
            }
        ),
        row(
            {
                "run_id": "RUN1991_1_ep_template",
                "check": "EP-template alignment lemma",
                "result": "FAIL_NOT_DERIVED_BUT_SHARPENED",
                "reason": "source/material EP component clauses are now isolated as the next theorem target",
            }
        ),
        row(
            {
                "run_id": "RUN1991_2_hilbert_owner",
                "check": "parent Hilbert source/no-species owner",
                "result": "FAIL_PARENT_UNSIGNED",
                "reason": "conditional theorem remains exact but closure-only if adopted without parent proof",
            }
        ),
        row(
            {
                "run_id": "RUN1991_3_source_pack",
                "check": "official source-pack route",
                "result": "FAIL_FILES_MISSING",
                "reason": "readout/source/material/product/C_parent files remain absent or nonclaim placeholders",
            }
        ),
        row(
            {
                "run_id": "RUN1991_4_verdict",
                "check": "1991 next-step decision",
                "result": "EP_TEMPLATE_ALIGNMENT_SELECTED",
                "reason": "it is the smallest nondegeneracy sublemma and keeps the GR-source theorem route visible",
            }
        ),
    ]

    claim_gate = [
        row(
            {
                "gate_id": "CG1991_0_nondegeneracy",
                "claim": "tau/P lower-bound certificate exists",
                "status": "FAIL_BLOCKED",
                "reason": "alignment floor and official/source data missing",
            }
        ),
        row(
            {
                "gate_id": "CG1991_1_ep_template",
                "claim": "EP-template alignment lemma proved",
                "status": "FAIL_BLOCKED",
                "reason": "lemma is sharpened but not parent-signed",
            }
        ),
        row(
            {
                "gate_id": "CG1991_2_hilbert_owner",
                "claim": "parent Hilbert owner/no-species-weight theorem proved",
                "status": "FAIL_BLOCKED",
                "reason": "still conditional and closure-only if adopted",
            }
        ),
        row(
            {
                "gate_id": "CG1991_3_source_pack_score",
                "claim": "finite WEP source-pack score is possible",
                "status": "FAIL_BLOCKED",
                "reason": "official readout/source/material/product/C_parent rows missing",
            }
        ),
        row(
            {
                "gate_id": "CG1991_4_local_GR_Newton",
                "claim": "local GR/Newton source coupling derived",
                "status": "FAIL_BLOCKED",
                "reason": "neither Hilbert owner nor finite nondegeneracy route closes",
            }
        ),
    ]

    decision = [
        row(
            {
                "decision_id": "DEC1991_0_certificate_status",
                "decision": "FULL_NONDEGENERACY_CERTIFICATE_NOT_AVAILABLE",
                "because": "both official K/readout data and parent K-vector theorem remain missing",
                "next_action": "attack first sublemma rather than full certificate",
            }
        ),
        row(
            {
                "decision_id": "DEC1991_1_theorem_target",
                "decision": "EP_TEMPLATE_ALIGNMENT_IS_FIRST_SUBLEMMA",
                "because": "a nonzero EP-template component is required before window/readout nonannihilation or c_min can matter",
                "next_action": "1992-Y5-R2FR-EP-template-alignment-lemma-or-source-pack-intake.md",
            }
        ),
        row(
            {
                "decision_id": "DEC1991_2_hilbert_parallel",
                "decision": "KEEP_PARENT_HILBERT_OWNER_AS_CLEAN_GR_ROUTE",
                "because": "if DeltaW_TiPt=0 is parent-signed, WEP residual vanishes without tau lower-bound",
                "next_action": "do not demote or forget Hilbert owner; require parent proof before claiming",
            }
        ),
    ]

    next_target = [
        row(
            {
                "next_id": "NEXT1991_0_primary",
                "selection_status": "selected",
                "target_doc": "1992-Y5-R2FR-EP-template-alignment-lemma-or-source-pack-intake.md",
                "target_script": "scripts/Y5_R2FR_EP_template_alignment_lemma_or_source_pack_intake_1992.py",
                "task": "derive or reject the narrower EP-template alignment lemma; if not derivable, stage official source-pack intake as the finite route",
                "success_condition": "parent-signed nonzero EP-template component, or exact blocker/source-pack rows for readout/source/material intake; no WEP/local-GR claim",
                "do_not": "do not claim tau_min, use nonzero-factor shortcut, set tau_WEP=1, adopt closure-only Hilbert owner as derivation, invent source-pack rows, modify formalization-workbench, or push GitHub",
            }
        )
    ]

    source_weight = [
        row(
            {
                "artifact_id": "SW1991_0_nondegeneracy_record",
                "artifact_type": "WEP_nondegeneracy_or_parent_Hilbert_owner_gate",
                "status": "NONCLAIM_EP_TEMPLATE_ALIGNMENT_SELECTED",
                "source_path": str(DOC_PATH),
                "next_target": "1992-Y5-R2FR-EP-template-alignment-lemma-or-source-pack-intake.md",
            }
        )
    ]

    wep_coeffs = [
        row(
            {
                "coefficient_id": "WEP1991_0_EP_template_alignment_slot",
                "quantity": "e_min or Proj_EP[V_MTS]",
                "required_formula": "|Proj_EP[V_MTS]| >= e_min ||V_MTS|| with e_min>0",
                "required_evidence": "parent EP-template theorem or official source/readout/material projection",
                "current_status": "MISSING_EP_TEMPLATE_ALIGNMENT",
                "status": "NONCLAIM_SLOT_ONLY",
            }
        )
    ]

    queue = [
        row(
            {
                "queue_id": "JR1991_0_EP_template_alignment",
                "priority": "1",
                "needed_input": "EP-template alignment lemma or source-pack intake",
                "route": "derive Proj_EP[V_MTS] nonzero from parent source geometry, or acquire official MICROSCOPE source/readout/material files",
                "required_fields": "EP_template_definition;V_MTS_basis;source_worldtube;material_tensor;readout_kernel;projection_value_or_theorem;source_path",
                "blocked_claims": "tau_min;P_min;DeltaW bound;WEP pass;local_GR;Newton",
            }
        )
    ]

    return {
        "source_register": source_register(stamp),
        "certificate_audit": certificate_audit,
        "ep_template": ep_template,
        "parent_owner": parent_owner,
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
    val("VAL1991_00_sources", "PASS" if not source_failures else "FAIL", "all source paths exist and needles found" if not source_failures else ";".join(row["source_id"] for row in source_failures))

    cert_rejects = any(row["cert_id"] == "NDC1991_3_fake_certificate_rejection" and row["verdict"] == "SHORTCUT_REJECTED" for row in tables["certificate_audit"])
    val("VAL1991_01_certificate_audit", "PASS" if cert_rejects else "FAIL", "fake nonzero-factor certificate rejected")

    ep_selected = any(row["lemma_id"] == "EPT1991_0_target_statement" and row["current_status"] == "TARGET_SHARPENED" for row in tables["ep_template"])
    ep_not_claimed = any(row["lemma_id"] == "EPT1991_4_current_verdict" and row["current_status"] == "LEMMA_NOT_DERIVED_CURRENT_CORPUS" for row in tables["ep_template"])
    val("VAL1991_02_ep_template", "PASS" if ep_selected and ep_not_claimed else "FAIL", "EP-template target sharpened without promotion")

    owner_safe = any(row["owner_id"] == "OWN1991_2_current_status" and row["current_status"] == "DO_NOT_PROMOTE" for row in tables["parent_owner"])
    val("VAL1991_03_parent_owner", "PASS" if owner_safe else "FAIL", "Hilbert owner route retained but not promoted")

    source_pack_blocks = all("MISSING" in row["status"] or "NOT_ZERO_CERTIFIED" in row["status"] for row in tables["source_pack"])
    val("VAL1991_04_source_pack", "PASS" if source_pack_blocks else "FAIL", "source-pack score route remains blocked by explicit missing objects")

    runner_selects = tables["runner_dryrun"][-1]["result"] == "EP_TEMPLATE_ALIGNMENT_SELECTED"
    val("VAL1991_05_runner_decision", "PASS" if runner_selects else "FAIL", "runner selects EP-template alignment next")

    gates_safe = all(row["status"] == "FAIL_BLOCKED" for row in tables["claim_gate"])
    val("VAL1991_06_claim_gates", "PASS" if gates_safe else "FAIL", "all claim gates blocked")

    next_ok = tables["next"][0]["target_doc"] == "1992-Y5-R2FR-EP-template-alignment-lemma-or-source-pack-intake.md"
    val("VAL1991_07_next_target", "PASS" if next_ok else "FAIL", "1992 EP-template/source-pack target selected")

    all_rows = [row for rows_for_table in tables.values() for row in rows_for_table]
    flags_safe = all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in all_rows)
    val("VAL1991_08_claim_flags_safe", "PASS" if flags_safe else "FAIL", "claim flags all false")

    parse_failures = []
    for output_name, path in OUTPUTS.items():
        if not path.exists():
            parse_failures.append(f"{output_name}:missing")
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            parsed = list(csv.DictReader(handle))
        if not parsed:
            parse_failures.append(f"{output_name}:empty")
    val("VAL1991_09_csv_parse", "PASS" if not parse_failures else "FAIL", "all generated CSVs parse with rows" if not parse_failures else ";".join(parse_failures))

    pycache_exists = (ROOT / "scripts" / "__pycache__").exists()
    val("VAL1991_10_pycache_absent", "PASS" if not pycache_exists else "FAIL", "scripts __pycache__ absent")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        formalization_artifacts = [path for path in FORMALIZATION.rglob("*1991*")]
    val("VAL1991_11_formalization_untouched", "PASS" if not formalization_artifacts else "FAIL", f"formalization_1991_artifact_count={len(formalization_artifacts)}")

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    val("VAL1991_OVERALL", overall, "1991 WEP nondegeneracy certificate or parent Hilbert owner")
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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def write_markdown(tables: dict[str, list[dict[str, str]]], validation_rows: list[dict[str, str]]) -> None:
    sections = [
        ("Source Register", tables["source_register"]),
        ("Nondegeneracy Certificate Audit", tables["certificate_audit"]),
        ("EP-Template Alignment Lemma Contract", tables["ep_template"]),
        ("Parent Hilbert Owner Gate", tables["parent_owner"]),
        ("Source-Pack Score Route", tables["source_pack"]),
        ("Runner Dryrun", tables["runner_dryrun"]),
        ("Claim Gate", tables["claim_gate"]),
        ("Decision Ledger", tables["decision"]),
        ("Next Target", tables["next"]),
        ("Validation", validation_rows),
    ]
    lines = [
        "# 1991 Y5 R2FR: WEP Nondegeneracy Certificate Or Parent Hilbert Owner",
        "",
        "Private checkpoint. This resolves the 1990 fork without pretending to have data or a theorem we do not have.",
        "",
        "Verdict: full WEP nondegeneracy is not certified. Current files still lack official/readout-equivalent `K_CMSM`, same-basis source worldtube, full Ti/Pt material tensor, product convention, and a nonzero alignment floor. The parent Hilbert owner route remains the clean GR/Newton route, but it is still conditional and cannot be adopted as a derivation.",
        "",
        "Concrete progress: the next theorem-sized target is now the EP-template alignment lemma: prove the MTS source-weight residual has a nonzero component in the MICROSCOPE EP-template channel, before attempting full `c_min` or tau lower-bound claims.",
        "",
        "No WEP, local-GR, Newton, R10, PPN, clock, orbital, or public claim follows from 1991.",
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
    print(f"VAL1991_OVERALL={overall}")
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
