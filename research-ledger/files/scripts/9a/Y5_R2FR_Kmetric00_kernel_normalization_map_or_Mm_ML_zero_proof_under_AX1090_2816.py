from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
FORMALIZATION = ROOT / "formalization-workbench"
MTS = WORK / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = WORK / "source-intake" / "local_bounds"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
DOC = WORK / "2816-Y5-R2FR-Kmetric00-kernel-normalization-map-or-Mm-ML-zero-proof-under-AX1090.md"

SRC_2815_NEXT = MTS / "P8_Y5_R2FR_2815_NEXT_TARGET.csv"
SRC_2815_SIGN = MTS / "P8_Y5_R2FR_2815_KMETRIC_HILBERT_SIGN_DERIVATION.csv"
SRC_2815_UPDATE = MTS / "P8_Y5_R2FR_2815_KMETRIC00_KERNEL_UPDATE.csv"
SRC_1289_DERIV = MTS / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv"
SRC_1289_EXPANSION = MTS / "P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv"
SRC_1286_RESPONSE = MTS / "P8_Y5_R10_1286_FIRST_RESPONSE_FIELD_COMPONENT_ROW_NONCLAIM.csv"
SRC_1286_BLOCKERS = MTS / "P8_Y5_R10_1286_FIRST_DELTAK_COMPONENT_BLOCKER_LEDGER.csv"
SRC_776_KGAMMA = MTS / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv"
SRC_776_VARIATION = MTS / "P8_Y5_R10_776_RESPONSE_DISPLACEMENT_VARIATION_LEDGER.csv"
SRC_798_GAMMA = MTS / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv"
SRC_2808_METRIC = MTS / "P8_Y5_R2FR_2808_METRIC_RESPONSE_DERIVATION_ATTEMPT.csv"
SRC_2808_UNITS = MTS / "P8_Y5_R2FR_2808_WARD_RESIDUAL_UNIT_CONTRACT.csv"
SRC_GK_CONTRACT = MTS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv"
SRC_GK_ACTION = MTS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2816_SOURCE_REGISTER.csv",
    "normalization": MTS / "P8_Y5_R2FR_2816_KERNEL_NORMALIZATION_MAP.csv",
    "csign": MTS / "P8_Y5_R2FR_2816_CSIGN_EXPORT_CONVENTION.csv",
    "zero_audit": MTS / "P8_Y5_R2FR_2816_MM_ML_ZERO_PROOF_AUDIT.csv",
    "template": MTS / "P8_Y5_R2FR_2816_UPDATED_KMETRIC00_TEMPLATE.csv",
    "gates": MTS / "P8_Y5_R2FR_2816_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2816_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2816_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2816_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2816_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "normalization_queue": RAB_QUEUE / "JR2816_KERNEL_NORMALIZATION_MAP_NONCLAIM.csv",
    "csign_queue": RAB_QUEUE / "JR2816_CSIGN_EXPORT_CONVENTION_NONCLAIM.csv",
    "zero_queue": RAB_QUEUE / "JR2816_MM_ML_ZERO_PROOF_AUDIT_NONCLAIM.csv",
    "template_queue": RAB_QUEUE / "JR2816_UPDATED_KMETRIC00_TEMPLATE_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2816_NEXT_MM_ML_ZERO_OR_BOUND.csv",
    "beta_doc": BETA_DOCS / "KMETRIC00_KERNEL_NORMALIZATION_2816_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Kmetric00_kernel_normalization_2816_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_Kmetric00_kernel_normalization_2816_nonclaim.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sp(path: Path) -> str:
    return str(path)


def ensure_dirs() -> None:
    directories = {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def anchor_found(path: Path, anchor: str) -> bool:
    return anchor in read_text(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def local_path_tokens(value: Any) -> list[Path]:
    if value is None:
        return []
    paths: list[Path] = []
    for token in str(value).split(";"):
        item = token.strip()
        if not item or item == "MISSING" or item.startswith("http"):
            continue
        candidate = Path(item)
        if not candidate.is_absolute():
            candidate = WORK / item
        if candidate.suffix or candidate.drive:
            paths.append(candidate)
    return paths


def build_sources() -> list[dict[str, Any]]:
    entries = [
        ("SRC2816_0_2815_next", SRC_2815_NEXT, "NEXT2815_0_2816", "handoff target for kernel normalization"),
        ("SRC2816_1_2815_sign", SRC_2815_SIGN, "KHS2815_1_pre_kernel_multiplier", "raw pre-kernel Hilbert sign"),
        ("SRC2816_2_2815_export_block", SRC_2815_SIGN, "KHS2815_3_export_blocker", "normalization blocker"),
        ("SRC2816_3_2815_update", SRC_2815_UPDATE, "KUU2815_2_final_export", "kernel-update export blocker"),
        ("SRC2816_4_1289_derivative", SRC_1289_DERIV, "KDR1289_0_Gamma_m_L_chain_kernel_00", "target Kmetric00 template"),
        ("SRC2816_5_1289_zero", SRC_1289_DERIV, "KDR1289_1_local_zero_condition_for_chain_kernel", "local zero-gate requirements"),
        ("SRC2816_6_1289_expansion", SRC_1289_EXPANSION, "KVE1289_2_metric_response_kernels", "symbolic metric-response kernels"),
        ("SRC2816_7_1286_response", SRC_1286_RESPONSE, "RFR1286_0_Gamma_memory_scalar_projection", "Gamma scalar projection source"),
        ("SRC2816_8_1286_blockers", SRC_1286_BLOCKERS, "DKC1286_1_missing_Kmetric_computation", "component blocker source"),
        ("SRC2816_9_776_kgamma", SRC_776_KGAMMA, "KGL776_2_derivative_terms", "derivative/projector stress blockers"),
        ("SRC2816_10_776_variation", SRC_776_VARIATION, "RAV776_2_formal_double_zero", "auxiliary double-zero clue"),
        ("SRC2816_11_798_gamma", SRC_798_GAMMA, "GSE798_2_local_locked_expansion", "local locked expansion clue"),
        ("SRC2816_12_2808_metric", SRC_2808_METRIC, "MRD2808_1_stress_split", "covariant Hilbert-stress split"),
        ("SRC2816_13_2808_units", SRC_2808_UNITS, "UNIT2808_1_Kmetric", "Kmetric unit contract"),
        ("SRC2816_14_gk_contract", SRC_GK_CONTRACT, "MR514_5_double_zero", "double-zero contract"),
        ("SRC2816_15_gk_action", SRC_GK_ACTION, "GK514_A_metric_response_scalar_density", "candidate parent action convention"),
    ]
    return [
        {
            "source_id": source_id,
            "path_or_url": sp(path),
            "anchor": anchor,
            "role": role,
            "path_exists": path.exists(),
            "anchor_found": anchor_found(path, anchor),
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for source_id, path, anchor, role in entries
    ]


def build_normalization_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KNM2816_0_metric_slot",
            "metric variation slot",
            "covariant g_{mu nu}",
            "2816 fixes all Kmetric-chain kernels in the same slot used by 2808: T_GK^{mu nu}:=-2/sqrt(-g) delta S_GK/delta g_{mu nu}.",
            "Using g^{mu nu} instead would require a separate sign/raising map and is not the canonical 2816 convention.",
            SRC_2808_METRIC,
            "MRD2808_1_stress_split",
            "CANONICAL_SLOT_FIXED_NONCLAIM",
        ),
        (
            "KNM2816_1_raw_kernel_definition",
            "raw kernels",
            "M_m,raw^{00}:=delta m/delta g_{00}; M_L,raw^{00}:=delta L_cg/delta g_{00}",
            "For raw kernels, Kmetric_chain^{00}=(-2)[L_cg^-2 F'(m) M_m,raw^{00}-2 L_cg^-3 F(m) M_L,raw^{00}] plus retained terms.",
            "This is equivalent to the 2815 pre-kernel sign row but is not selected as the future public notation.",
            SRC_2815_SIGN,
            "KHS2815_1_pre_kernel_multiplier",
            "RAW_BRANCH_MAPPED",
        ),
        (
            "KNM2816_2_hilbert_kernel_definition",
            "Hilbert-normalized kernels",
            "M_m^{00}:=-2 delta m/delta g_{00}; M_L^{00}:=-2 delta L_cg/delta g_{00}",
            "This absorbs the Hilbert factor into the response kernels, so the 1289-style bracket has C_sign=+1.",
            "This is a notation/normalization decision only; it does not supply numeric M_m or M_L.",
            SRC_1289_DERIV,
            "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "CANONICAL_KERNEL_NORMALIZATION_SELECTED",
        ),
        (
            "KNM2816_3_units",
            "kernel units",
            "M_m carries units of m per metric component; M_L carries units of length per metric component before any dimensionless field convention",
            "Kmetric_chain has the same units as Gamma_eff only after m, F(m), L_cg, and the metric-response kernels share the declared 2808/1286 unit ledger.",
            "No unit claim can be made until m/F/L_cg dimensions are declared numerically.",
            SRC_2808_UNITS,
            "UNIT2808_1_Kmetric",
            "UNITS_CONTRACT_RETAINED",
        ),
    ]
    return [
        {
            "map_id": row_id,
            "object": obj,
            "definition": definition,
            "consequence": consequence,
            "caveat": caveat,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "status": status,
            "generated_utc": utc_now(),
        }
        for row_id, obj, definition, consequence, caveat, source_path, anchor, status in rows
    ]


def build_csign_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CSE2816_0_raw_branch",
            "raw-kernel branch",
            "C_sign=-2",
            "Only if M_m/M_L mean raw covariant metric derivatives.",
            "not selected as canonical post-2816 notation; retained to prevent sign confusion",
            SRC_2815_SIGN,
            "KHS2815_1_pre_kernel_multiplier",
            "CONSISTENCY_BRANCH_RECORDED",
            False,
        ),
        (
            "CSE2816_1_canonical_export",
            "Hilbert-normalized covariant branch",
            "C_sign=+1",
            "Because M_m^{00}:=-2 delta m/delta g_{00} and M_L^{00}:=-2 delta L_cg/delta g_{00}.",
            "convention-export only; M_m, M_L, K_conn, K_domain, K_boundary remain missing",
            OUTPUTS["normalization"],
            "KNM2816_2_hilbert_kernel_definition",
            "CSIGN_EXPORTED_AS_CONVENTION_NOT_SCORE",
            True,
        ),
        (
            "CSE2816_2_contravariant_guard",
            "contravariant metric slot",
            "DO_NOT_USE_WITHOUT_MAP",
            "The exported C_sign=+1 is not automatically valid for kernels defined by variation with respect to g^{mu nu}.",
            "future rows must state the metric slot before any comparison to Khat or PPN/clock/orbital arenas",
            OUTPUTS["normalization"],
            "KNM2816_0_metric_slot",
            "METRIC_SLOT_GUARD_ACTIVE",
            False,
        ),
    ]
    return [
        {
            "export_id": export_id,
            "branch": branch,
            "C_sign_value_or_status": value,
            "condition": condition,
            "caveat": caveat,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": True if source_path == OUTPUTS["normalization"] else anchor_found(source_path, anchor),
            "exported_as_convention": exported,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "status": status,
            "generated_utc": utc_now(),
        }
        for export_id, branch, value, condition, caveat, source_path, anchor, status, exported in rows
    ]


def build_zero_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ZPA2816_0_Mm_zero",
            "M_m^{00}=0",
            "m is parent-locked to a local fixed point and its variation with respect to g_{00} vanishes in the local vacuum branch",
            "GSE798_2 supplies only a conditional locked expansion; no parent lock/variation-zero theorem is signed",
            SRC_798_GAMMA,
            "GSE798_2_local_locked_expansion",
            "NOT_PROVED",
            "MISSING_PARENT_LOCK_TO_m_STAR;MISSING_DELTA_m_DELTA_g00_ZERO",
        ),
        (
            "ZPA2816_1_ML_zero",
            "M_L^{00}=0",
            "L_cg is locally metric-silent or fixed by a quotient/background datum that does not vary with g_{00}",
            "1289 explicitly leaves L_cg metric silence open",
            SRC_1289_DERIV,
            "KDR1289_1_local_zero_condition_for_chain_kernel",
            "NOT_PROVED",
            "MISSING_LCG_METRIC_SILENCE",
        ),
        (
            "ZPA2816_2_Fprime_zero",
            "F'(m_*)=0",
            "the m-channel linear leakage is removed at the local stationary point",
            "contract rows require double-zero, but current sources do not prove the parent selects m_*",
            SRC_GK_CONTRACT,
            "MR514_5_double_zero",
            "CONDITIONAL_ONLY",
            "MISSING_PROOF_F_PRIME_ZERO;MISSING_PARENT_SELECTION_OF_m_STAR",
        ),
        (
            "ZPA2816_3_derivative_domain_boundary",
            "K_conn=K_domain=K_boundary=0",
            "connection/domain/boundary terms vanish or are bounded in the same local branch",
            "776 and 1289 retain derivative/projector/boundary terms as open blockers",
            SRC_776_KGAMMA,
            "KGL776_2_derivative_terms",
            "NOT_PROVED",
            "MISSING_K_CONN_00;MISSING_K_DOMAIN_00;MISSING_K_BOUNDARY_00",
        ),
        (
            "ZPA2816_4_zero_verdict",
            "Kmetric_chain^{00}=0",
            "all chain, connection, domain, and boundary channels vanish together",
            "the zero route is attractive but not closed; retain it as the next derivation target, not as a claim",
            SRC_1289_DERIV,
            "KDR1289_1_local_zero_condition_for_chain_kernel",
            "ZERO_PROOF_REJECTED_FOR_NOW",
            "MISSING_PARENT_LOCK_AND_SILENCE_CERTIFICATES",
        ),
    ]
    return [
        {
            "audit_id": audit_id,
            "zero_target": target,
            "needed_statement": needed,
            "current_evidence": evidence,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "status": status,
            "missing_before_zero_claim": missing,
            "zero_proved": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for audit_id, target, needed, evidence, source_path, anchor, status, missing in rows
    ]


def build_template_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "KTT2816_0_canonical_template",
            "Kmetric_chain^{00}",
            "Kmetric_chain^{00}=L_cg^-2 F'(m) M_m^{00}-2 L_cg^-3 F(m) M_L^{00}+K_conn^{00}+K_domain^{00}+K_boundary^{00}",
            "canonical post-2816 template with Hilbert-normalized covariant kernels and C_sign=+1",
            SRC_1289_DERIV,
            "KDR1289_0_Gamma_m_L_chain_kernel_00",
            "TEMPLATE_NORMALIZED_NONCLAIM",
            "MISSING_NUMERIC_M_m_00;MISSING_NUMERIC_M_L_00;MISSING_K_CONN_00;MISSING_K_DOMAIN_00;MISSING_K_BOUNDARY_00",
        ),
        (
            "KTT2816_1_zero_template",
            "Kmetric_chain^{00}=0 route",
            "requires F'(m_*)M_m^{00}=0, F(m_*)M_L^{00}=0, and K_conn=K_domain=K_boundary=0 or bounded below local target",
            "zero route remains a derivation target, not an asserted plateau axiom",
            OUTPUTS["zero_audit"],
            "ZPA2816_4_zero_verdict",
            "ZERO_ROUTE_OPEN_NONCLAIM",
            "MISSING_PARENT_LOCK_AND_SILENCE_CERTIFICATES",
        ),
    ]
    return [
        {
            "template_id": template_id,
            "object": obj,
            "canonical_formula": formula,
            "interpretation": interpretation,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": True if source_path == OUTPUTS["zero_audit"] else anchor_found(source_path, anchor),
            "status": status,
            "missing_before_score": missing,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for template_id, obj, formula, interpretation, source_path, anchor, status, missing in rows
    ]


def build_gate_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    csign_exported = any(row["export_id"] == "CSE2816_1_canonical_export" and row["C_sign_value_or_status"] == "C_sign=+1" for row in sections["csign"])
    zero_proved = all(row["zero_proved"] for row in sections["zero_audit"])
    rows = [
        ("CG2816_0_sources_anchored", "2816 source anchors are present", all(row["anchor_found"] for row in sections["sources"]), "all required local anchors were found"),
        ("CG2816_1_kernel_normalization", "kernel convention is normalized", True, "covariant metric slot plus Hilbert-normalized kernels selected"),
        ("CG2816_2_Csign_export", "C_sign can be exported as convention", csign_exported, "C_sign=+1 under Hilbert-normalized covariant kernels"),
        ("CG2816_3_Mm_ML_zero", "M_m and M_L vanish in local vacuum", zero_proved, "parent lock and L_cg metric silence remain unsigned"),
        ("CG2816_4_Kmetric00_score", "Kmetric00 branch is score-ready", False, "numeric/bounded M_m, M_L, K_conn, K_domain and K_boundary are still missing"),
        ("CG2816_5_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "normalization is not a local residual bound or zero theorem"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": passed,
            "reason": reason,
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": utc_now(),
        }
        for gate_id, claim, passed, reason in rows
    ]


def build_decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC2816_0_choose_convention",
            "Use Hilbert-normalized covariant kernels as the post-2816 canonical notation.",
            "It absorbs the 2815 raw -2 factor into M_m/M_L and lets 1289 keep the simple C_sign=+1 bracket.",
            "future kernel rows must state they use M_X^{00}:=-2 delta X/delta g_{00}",
        ),
        (
            "DEC2816_1_no_zero_claim",
            "Do not claim M_m=M_L=0.",
            "The fixed-point and L_cg-silence clauses remain conditional rather than parent-derived.",
            "derive the local fixed-point/source-support theorem or produce bounded response kernels",
        ),
        (
            "DEC2816_2_real_progress",
            "This closes the sign/factor ambiguity but not the local branch.",
            "The branch now has a stable tensor bookkeeping convention, which is needed before GR-reduction comparison.",
            "move next to first M_m/M_L zero proof or first response bound",
        ),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for decision_id, decision, because, next_action in rows
    ]


def build_next_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2816_0_2817",
            "next_target": "2817-Y5-R2FR-first-Mm-ML-kernel-zero-proof-or-response-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_first_Mm_ML_kernel_zero_proof_or_response_bound_under_AX1090_2817.py",
            "objective": "derive M_m^{00}=0 and M_L^{00}=0 from the parent local fixed-point/quotient-silence mechanism, or produce one bounded Hilbert-normalized response-kernel row under the 2816 convention",
            "include": "Hilbert-normalized covariant kernel definition; parent lock to m_*; L_cg metric-silence test; boundary/domain/connection retained; source paths; units",
            "exclude": "plateau axiom; local-GR/WEP/PPN/orbital claim; measured-G absorption; smoke Fermi evidence; GitHub; formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["normalization"], BRANCH_OUTPUTS["normalization_queue"], "normalization_queue"),
        (OUTPUTS["csign"], BRANCH_OUTPUTS["csign_queue"], "csign_queue"),
        (OUTPUTS["zero_audit"], BRANCH_OUTPUTS["zero_queue"], "zero_queue"),
        (OUTPUTS["template"], BRANCH_OUTPUTS["template_queue"], "template_queue"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
        (OUTPUTS["normalization"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["template"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2816_{label}",
                "source": sp(source),
                "destination": sp(destination),
                "exists": destination.exists(),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": utc_now(),
            }
        )
    return rows


def claim_flags_true(sections: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in sections.items():
        if key == "validation":
            continue
        for row in rows:
            if str(row.get("valid_for_claim", "false")).lower() == "true":
                return True
            if str(row.get("claim_allowed", "false")).lower() == "true":
                return True
    return False


def cited_paths_exist(sections: dict[str, list[dict[str, Any]]]) -> bool:
    paths: list[Path] = []
    for rows in sections.values():
        for row in rows:
            for key in ("source_path", "source_paths", "source", "destination", "path_or_url"):
                paths.extend(local_path_tokens(row.get(key)))
    return all(path.exists() for path in paths)


def formalization_untouched_since_run() -> bool:
    if not FORMALIZATION.exists():
        return True
    threshold = RUN_STARTED_UTC.timestamp()
    return not any(path.is_file() and path.stat().st_mtime >= threshold for path in FORMALIZATION.rglob("*"))


def build_validation(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    checks = [
        ("VAL2816_0_sources_exist", all(row["path_exists"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2816_1_source_anchors", all(row["anchor_found"] for row in sections["sources"]), "all source-register anchors were found"),
        ("VAL2816_2_normalization_anchored", all(row["anchor_found"] for row in sections["normalization"]), "all normalization-map anchors were found"),
        ("VAL2816_3_covariant_slot_fixed", any(row["map_id"] == "KNM2816_0_metric_slot" and row["definition"] == "covariant g_{mu nu}" for row in sections["normalization"]), "covariant metric slot was fixed"),
        ("VAL2816_4_hilbert_kernel_selected", any(row["map_id"] == "KNM2816_2_hilbert_kernel_definition" and row["status"] == "CANONICAL_KERNEL_NORMALIZATION_SELECTED" for row in sections["normalization"]), "Hilbert-normalized kernels were selected"),
        ("VAL2816_5_Csign_exported_convention", any(row["export_id"] == "CSE2816_1_canonical_export" and row["C_sign_value_or_status"] == "C_sign=+1" and row["exported_as_convention"] for row in sections["csign"]), "C_sign=+1 exported as convention"),
        ("VAL2816_6_zero_not_claimed", all(not row["zero_proved"] for row in sections["zero_audit"]), "M_m/M_L zero proof remains unclaimed"),
        ("VAL2816_7_template_safe", all(not row["score_ready"] and not row["claim_allowed"] for row in sections["template"]), "updated Kmetric00 templates remain nonclaim"),
        ("VAL2816_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2816_9_next_target_2817", any(row["next_id"] == "NEXT2816_0_2817" for row in sections["next"]), "next target is 2817"),
        ("VAL2816_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2816_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2816_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2816_13_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2816_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2816_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2816_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2816_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2816_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2816 fixes the Kmetric00 kernel convention: covariant metric slot, Hilbert-normalized M_m/M_L kernels, and C_sign=+1 as convention only; M_m/M_L zero proof and local claims remain blocked.",
            "generated_utc": utc_now(),
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
        + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def build_doc(sections: dict[str, list[dict[str, Any]]]) -> str:
    lines = [
        "# 2816 - Y5 R2FR Kmetric00 Kernel Normalization Map Or Mm ML Zero Proof Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2816 closes the sign/factor ambiguity that was left open in 2815. The canonical post-2816 convention is: vary in the covariant metric slot `g_{mu nu}` and define the response kernels as Hilbert-normalized objects, `M_m^{00}:=-2 delta m/delta g_{00}` and `M_L^{00}:=-2 delta L_cg/delta g_{00}`.",
        "",
        "Under that convention the 1289-style chain template can export `C_sign=+1` safely as a notation/convention result. This is real tensor bookkeeping progress, not a local-gravity score.",
        "",
        "The zero route does not close yet. `M_m^{00}=0`, `M_L^{00}=0`, `F'(m_*)=0`, and the connection/domain/boundary silences still need parent-signed proofs or bounded rows before any local-GR/WEP/PPN/orbital claim.",
        "",
        "## Kernel Normalization Map",
        markdown_table(sections["normalization"], ["map_id", "object", "definition", "status", "anchor_found"]),
        "",
        "## Csign Export Convention",
        markdown_table(sections["csign"], ["export_id", "branch", "C_sign_value_or_status", "exported_as_convention", "status"]),
        "",
        "## Mm ML Zero Proof Audit",
        markdown_table(sections["zero_audit"], ["audit_id", "zero_target", "status", "missing_before_zero_claim", "zero_proved"]),
        "",
        "## Updated Kmetric00 Template",
        markdown_table(sections["template"], ["template_id", "object", "canonical_formula", "status", "missing_before_score"]),
        "",
        "## Claim Gates",
        markdown_table(sections["gates"], ["gate_id", "claim", "gate_pass", "claim_allowed", "reason"]),
        "",
        "## Decision Ledger",
        markdown_table(sections["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Validation",
        markdown_table(sections["validation"], ["validation_id", "passed", "detail"]),
        "",
        "## Next Target",
        markdown_table(sections["next"], ["next_id", "next_target", "objective", "include", "exclude"]),
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    ensure_dirs()
    if (SCRIPTS / "__pycache__").exists():
        shutil.rmtree(SCRIPTS / "__pycache__")

    sections: dict[str, list[dict[str, Any]]] = {
        "sources": build_sources(),
        "normalization": build_normalization_rows(),
    }
    write_csv(OUTPUTS["normalization"], sections["normalization"])
    sections["csign"] = build_csign_rows()
    write_csv(OUTPUTS["csign"], sections["csign"])
    sections["zero_audit"] = build_zero_audit_rows()
    write_csv(OUTPUTS["zero_audit"], sections["zero_audit"])
    sections["template"] = build_template_rows()
    write_csv(OUTPUTS["template"], sections["template"])
    sections["gates"] = build_gate_rows(sections)
    sections["decision"] = build_decision_rows()
    sections["next"] = build_next_rows()

    for key, rows in sections.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    sections["branches"] = copy_branches()
    write_csv(OUTPUTS["branches"], sections["branches"])
    sections["validation"] = build_validation(sections)
    write_csv(OUTPUTS["validation"], sections["validation"])
    DOC.write_text(build_doc(sections), encoding="utf-8")
    print(f"wrote {DOC}")
    print(f"validation overall: {sections['validation'][-1]['passed']}")


if __name__ == "__main__":
    main()
