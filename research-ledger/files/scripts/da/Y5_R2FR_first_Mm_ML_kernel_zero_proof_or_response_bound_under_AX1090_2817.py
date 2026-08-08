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
DOC = WORK / "2817-Y5-R2FR-first-Mm-ML-kernel-zero-proof-or-response-bound-under-AX1090.md"

SRC_2816_NEXT = MTS / "P8_Y5_R2FR_2816_NEXT_TARGET.csv"
SRC_2816_NORM = MTS / "P8_Y5_R2FR_2816_KERNEL_NORMALIZATION_MAP.csv"
SRC_2816_CSIGN = MTS / "P8_Y5_R2FR_2816_CSIGN_EXPORT_CONVENTION.csv"
SRC_2816_ZERO = MTS / "P8_Y5_R2FR_2816_MM_ML_ZERO_PROOF_AUDIT.csv"
SRC_2816_TEMPLATE = MTS / "P8_Y5_R2FR_2816_UPDATED_KMETRIC00_TEMPLATE.csv"
SRC_1290_AUDIT = MTS / "P8_Y5_R10_1290_METRIC_KERNEL_AUDIT.csv"
SRC_1291_STRICT = MTS / "P8_Y5_R10_1291_STRICT_DOUBLE_ZERO_PARENT_CLAUSE.csv"
SRC_1368_KERNEL = MTS / "P8_Y5_R10_1368_M_LCG_KERNEL_HUNT.csv"
SRC_1369_LCG = MTS / "P8_Y5_R10_1369_LCG_METRIC_RESPONSE_DERIVATION_LEDGER.csv"
SRC_1371_ZERO = MTS / "P8_Y5_R10_1371_LOCAL_RESIDUAL_ZERO_OR_BOUND_LEDGER.csv"
SRC_1520_LCG = MTS / "P8_Y5_PARENT_LCG_1520_METRIC_SILENCE_THEOREM.csv"
SRC_1534_NOHAIR = MTS / "P8_Y5_PARENT_QLOC_1534_LOCAL_LOCKING_NOHAIR_THEOREM.csv"
SRC_1534_LEAK = MTS / "P8_Y5_PARENT_QLOC_1534_QUADRATIC_LEAKAGE_BOUND_CONTRACT.csv"
SRC_1536_NLOCK = MTS / "P8_Y5_PARENT_QLOC_1536_NLOCK_ENVELOPE_CONTRACT.csv"
SRC_1536_SILENCE = MTS / "P8_Y5_PARENT_QLOC_1536_EXACT_SILENCE_AUDIT.csv"
SRC_1537_PRIORITY = MTS / "P8_Y5_PARENT_QLOC_1537_FIRST_PRIORITY_NORM_ROWS.csv"
SRC_1537_RUNNER = MTS / "P8_Y5_PARENT_QLOC_1537_NLOCK_RUNNER_INPUT_NONCLAIM.csv"
SRC_2221_KERNEL = MTS / "P8_Y5_PARENT_QLOC_2221_KMETRIC_KERNEL_NORM_SOURCE_AUDIT.csv"
SRC_2734_LCG = MTS / "P8_Y5_R2FR_2734_LCG_METRIC_SILENCE_AUDIT.csv"
SRC_2734_BOUND = MTS / "P8_Y5_R2FR_2734_FIRST_ML_KERNEL_NORM_ROW.csv"
SRC_2714_ZERO = MTS / "P8_Y5_R2FR_2714_LAMBDA_PHI_ZERO_ATTEMPT.csv"
SRC_FP511 = MTS / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2817_SOURCE_REGISTER.csv",
    "premises": MTS / "P8_Y5_R2FR_2817_PARENT_PREMISE_MATCH_AUDIT.csv",
    "kernel_zero": MTS / "P8_Y5_R2FR_2817_MM_ML_KERNEL_ZERO_ATTEMPT.csv",
    "coefficient_kill": MTS / "P8_Y5_R2FR_2817_STRICT_DOUBLE_ZERO_COEFFICIENT_KILL.csv",
    "bound_schema": MTS / "P8_Y5_R2FR_2817_HILBERT_NORMALIZED_CHAIN_BOUND_SCHEMA.csv",
    "gates": MTS / "P8_Y5_R2FR_2817_CLAIM_GATES.csv",
    "decision": MTS / "P8_Y5_R2FR_2817_DECISION_LEDGER.csv",
    "next": MTS / "P8_Y5_R2FR_2817_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2817_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2817_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "premise_queue": RAB_QUEUE / "JR2817_PARENT_PREMISE_MATCH_AUDIT_NONCLAIM.csv",
    "zero_queue": RAB_QUEUE / "JR2817_MM_ML_KERNEL_ZERO_ATTEMPT_NONCLAIM.csv",
    "kill_queue": RAB_QUEUE / "JR2817_STRICT_DOUBLE_ZERO_COEFFICIENT_KILL_NONCLAIM.csv",
    "bound_queue": RAB_QUEUE / "JR2817_HILBERT_NORMALIZED_CHAIN_BOUND_SCHEMA_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2817_NEXT_LOCAL_LOCK_AMPLITUDE_LAW.csv",
    "beta_doc": BETA_DOCS / "STRICT_DOUBLE_ZERO_COEFFICIENT_KILL_2817_NONCLAIM.csv",
    "local_bound_copy": LOCAL_BOUNDS / "Hilbert_normalized_chain_bound_schema_2817_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "microscope_strict_double_zero_coefficient_kill_2817_nonclaim.csv",
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
        ("SRC2817_0_2816_next", SRC_2816_NEXT, "NEXT2816_0_2817", "2817 handoff"),
        ("SRC2817_1_2816_norm", SRC_2816_NORM, "KNM2816_2_hilbert_kernel_definition", "Hilbert-normalized kernel convention"),
        ("SRC2817_2_2816_csign", SRC_2816_CSIGN, "CSE2816_1_canonical_export", "C_sign=+1 convention"),
        ("SRC2817_3_2816_zero", SRC_2816_ZERO, "ZPA2816_4_zero_verdict", "direct zero blocker"),
        ("SRC2817_4_2816_template", SRC_2816_TEMPLATE, "KTT2816_0_canonical_template", "canonical chain formula"),
        ("SRC2817_5_1290_audit", SRC_1290_AUDIT, "MKA1290_3_strict_double_zero_branch", "strict double-zero route"),
        ("SRC2817_6_1291_strict", SRC_1291_STRICT, "SDZ1291_5_parent_clause_verdict", "strict double-zero parent clause"),
        ("SRC2817_7_1368_kernel", SRC_1368_KERNEL, "KERN1368_5_chain_kernel_verdict", "kernel hunt verdict"),
        ("SRC2817_8_1369_lcg", SRC_1369_LCG, "ML1369_3_chain_zero_gate_update", "Lcg chain zero gate"),
        ("SRC2817_9_1371_zero", SRC_1371_ZERO, "LRZ1371_3_gradient_source", "local residual zero/bound route"),
        ("SRC2817_10_1520_lcg", SRC_1520_LCG, "ML1520_4_live_claim", "Lcg silence not claimed"),
        ("SRC2817_11_1534_nohair", SRC_1534_NOHAIR, "NH1534_5_double_zero_impact", "local lock impact"),
        ("SRC2817_12_1534_leak", SRC_1534_LEAK, "LEAK1534_5_Kchain_bound", "leakage bound contract"),
        ("SRC2817_13_1536_nlock", SRC_1536_NLOCK, "NLOCK1536_5_lock_norm", "N_lock envelope"),
        ("SRC2817_14_1536_silence", SRC_1536_SILENCE, "SIL1536_6_exact_lock", "exact lock not proved"),
        ("SRC2817_15_1537_priority", SRC_1537_PRIORITY, "FP1537_4_pair_verdict", "source/inner priority blockers"),
        ("SRC2817_16_1537_runner", SRC_1537_RUNNER, "NLR1537_3_local_lock", "lock runner missing inputs"),
        ("SRC2817_17_2221_kernel", SRC_2221_KERNEL, "KNA2221_4_local_lock", "kernel norm source audit"),
        ("SRC2817_18_2734_lcg", SRC_2734_LCG, "LCGMS2734_5_verdict", "preferred Lcg route narrowed"),
        ("SRC2817_19_2734_bound", SRC_2734_BOUND, "MLB2734_2_double_zero_displacement", "M_L bound schema"),
        ("SRC2817_20_2714_zero", SRC_2714_ZERO, "LZA2714_1_fixed_point_shortcut", "shortcut rejection guard"),
        ("SRC2817_21_fp511", SRC_FP511, "FP511_2_positive_mass_gap", "local GR fixed-point condition"),
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


def build_premise_rows() -> list[dict[str, Any]]:
    rows = [
        ("PMA2817_0_convention", "Hilbert-normalized covariant kernels and C_sign=+1", "CLOSED_FOR_NOTATION", "2816 fixes the sign/factor convention.", SRC_2816_CSIGN, "CSE2816_1_canonical_export"),
        ("PMA2817_1_strict_double_zero_form", "F(m_*)=0 and F'(m_*)=0", "CLAUSE_WRITTEN_NOT_PARENT_MATCHED", "1291 writes the sufficient form F=(m-m_*)^2H but does not source-match live MTS.", SRC_1291_STRICT, "SDZ1291_1_strict_F_form"),
        ("PMA2817_2_parent_lock", "m=m_* in the local exterior", "CONDITIONAL_NOT_LIVE", "1534 writes the exact no-hair theorem but source/boundary/operator premises remain unsigned.", SRC_1534_NOHAIR, "NH1534_6_verdict"),
        ("PMA2817_3_Lcg_finite", "L_cg finite, nonzero, and not singular at the source root", "CLAUSE_WRITTEN_NOT_PARENT_MATCHED", "1291/2734 allow coefficient kill if F(m_*)=0 even with finite M_L.", SRC_1291_STRICT, "SDZ1291_2_Lcg_status"),
        ("PMA2817_4_hidden_kernels", "K_conn, K_domain, K_boundary vanish or are bounded", "OPEN_RETAINED", "2714 warns fixed-point shortcuts do not remove hidden Kmetric kernels.", SRC_2714_ZERO, "LZA2714_1_fixed_point_shortcut"),
        ("PMA2817_5_leakage_inputs", "Delta_m or N_lock sourced if exact lock fails", "MISSING", "1536/1537 leave N_lock and first source/inner norms missing.", SRC_1537_RUNNER, "NLR1537_3_local_lock"),
    ]
    return [
        {
            "premise_id": premise_id,
            "premise": premise,
            "status": status,
            "evidence": evidence,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for premise_id, premise, status, evidence, source_path, anchor in rows
    ]


def build_kernel_zero_rows() -> list[dict[str, Any]]:
    rows = [
        ("KZA2817_0_Mm_fixed_field", "M_m^{00}=0", "If m is a parent-owned independent scalar held fixed during Hilbert variation, then M_m^{00}=0.", "CONDITIONAL_RELATIVE_ZERO", "parent action must exclude metric-composite/readout/domain/projector definitions of m", SRC_1368_KERNEL, "KERN1368_0_m_fixed_field_branch"),
        ("KZA2817_1_Mm_counterbranch", "M_m^{00} retained", "If m is a metric-composite readout, norm, curvature scalar, or domain-selected scalar, the metric kernel generally survives.", "COUNTERBRANCH_RETAINED", "explicit parent m definition or finite kernel bound", SRC_1368_KERNEL, "KERN1368_1_m_metric_composite_branch"),
        ("KZA2817_2_ML_fixed_L0", "M_L^{00}=0", "If L_cg=L0 is a fixed parent scalar parameter under Hilbert variation, then M_L^{00}=0.", "EXACT_UNDER_CLOSURE_NOT_LIVE", "signed parent fixed-L0 clause and readout/domain separation", SRC_1520_LCG, "ML1520_1_fixed_parameter_derivative"),
        ("KZA2817_3_ML_counterbranch", "M_L^{00} retained", "If L_cg is a proper length, curvature scale, density scale, domain support, or projector collar, M_L generally survives.", "COUNTERBRANCH_RETAINED", "L_cg parent definition or response coefficient", SRC_2734_LCG, "LCGMS2734_4_metric_composite_counterbranch"),
        ("KZA2817_4_zero_verdict", "direct kernel-zero proof", "The direct M_m=M_L=0 route remains conditional/closure-looking; do not claim it.", "DIRECT_KERNEL_ZERO_NOT_CLAIMED", "use coefficient kill or finite bound instead", SRC_2816_ZERO, "ZPA2816_4_zero_verdict"),
    ]
    return [
        {
            "attempt_id": attempt_id,
            "target": target,
            "statement": statement,
            "status": status,
            "missing_or_guard": missing,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "zero_proved": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for attempt_id, target, statement, status, missing, source_path, anchor in rows
    ]


def build_coefficient_kill_rows() -> list[dict[str, Any]]:
    rows = [
        ("CK2817_0_canonical_formula", "algebraic chain", "K_alg^{00}=L_cg^-2 F'(m) M_m^{00}-2 L_cg^-3 F(m) M_L^{00}", "2816 canonical Hilbert-normalized convention with C_sign=+1.", "FORMULA_IMPORTED", SRC_2816_TEMPLATE, "KTT2816_0_canonical_template"),
        ("CK2817_1_exact_double_zero", "coefficient kill", "At exact local lock m=m_* with F(m_*)=F'(m_*)=0, K_alg^{00}=0 for any finite M_m^{00}, M_L^{00}.", "This is algebraically stronger and less scrutiny-heavy than proving L_cg metric silence.", "EXACT_CONDITIONAL_LEMMA", SRC_1291_STRICT, "SDZ1291_1_strict_F_form"),
        ("CK2817_2_local_lock_dependency", "same-branch lock", "The lemma is live only if the parent action locks the compact local exterior to m_* rather than fitting a per-system root.", "1534 writes but does not prove the no-hair/local-lock theorem.", "LOCK_DEPENDENT_NOT_LIVE", SRC_1534_NOHAIR, "NH1534_5_double_zero_impact"),
        ("CK2817_3_hidden_terms_guard", "full Kmetric_chain", "Coefficient kill removes only the algebraic M_m/M_L channels; K_conn, K_domain, K_boundary and active stress remain.", "Fixed-point language alone cannot close DeltaK/q_loc.", "HIDDEN_KERNELS_RETAINED", SRC_2221_KERNEL, "KNA2221_6_hidden"),
        ("CK2817_4_verdict", "best current route", "Adopt strict double-zero/source-root coefficient kill as the preferred local-chain derivation target, while retaining leakage bounds.", "No local-GR/WEP/PPN/orbital claim follows until lock and hidden kernels close.", "BEST_ROUTE_NONCLAIM", SRC_2734_LCG, "LCGMS2734_5_verdict"),
    ]
    return [
        {
            "kill_id": kill_id,
            "object": obj,
            "lemma_or_formula": lemma,
            "interpretation": interpretation,
            "status": status,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "exact_if_premises_hold": kill_id == "CK2817_1_exact_double_zero",
            "live_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for kill_id, obj, lemma, interpretation, status, source_path, anchor in rows
    ]


def build_bound_schema_rows() -> list[dict[str, Any]]:
    rows = [
        ("HKB2817_0_exact_lock", "exact local lock", "Delta_m=0 and F(m_*)=F'(m_*)=0", "||K_alg||_D=0", "parent no-hair/local-lock theorem; hidden kernels separately zero/bounded", "EXACT_CONDITIONAL_ZERO_NOT_CLAIMED", SRC_1534_NOHAIR, "NH1534_3_exact_nohair"),
        ("HKB2817_1_double_zero_leakage", "near-lock bound", "|m-m_*|<=Delta_m, |F''|<=F2_bar, L_cg>=L_min, finite kernels", "||K_alg||_D <= L_min^-2 F2_bar Delta_m M_m_bar + L_min^-3 F2_bar Delta_m^2 M_L_bar + O(Delta_m^2 M_m_bar + Delta_m^3 M_L_bar)", "Delta_m amplitude law; F2_bar; M_m_bar; M_L_bar; L_min; same-norm domain", "BEST_NONCLAIM_BOUND_SCHEMA", SRC_2734_BOUND, "MLB2734_2_double_zero_displacement"),
        ("HKB2817_2_Nlock_bridge", "amplitude from energy norm", "E_m(u)<=N_lock and ||u||<=C_emb N_lock", "Delta_m <= C_emb N_lock", "N_src, N_inner, remaining N_lock components, C_emb", "AMPLITUDE_BRIDGE_NOT_NUMERIC", SRC_1536_NLOCK, "NLOCK1536_5_lock_norm"),
        ("HKB2817_3_first_physical_inputs", "first missing norms", "N_lock starts with N_src and N_inner", "N_src zero/bound and N_inner zero/bound decide whether lock can be claimed or bounded", "U_B*S_cg and compact inner charge Q_m^H", "NEXT_INPUT_PRIORITY", SRC_1537_PRIORITY, "FP1537_4_pair_verdict"),
    ]
    return [
        {
            "bound_id": bound_id,
            "branch": branch,
            "assumptions": assumptions,
            "bound_or_result": bound,
            "missing_inputs": missing,
            "status": status,
            "source_path": sp(source_path),
            "source_anchor": anchor,
            "anchor_found": anchor_found(source_path, anchor),
            "uses_2816_Csign": True,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
        for bound_id, branch, assumptions, bound, missing, status, source_path, anchor in rows
    ]


def build_gate_rows(sections: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    coefficient_lemma = any(row["kill_id"] == "CK2817_1_exact_double_zero" and row["exact_if_premises_hold"] for row in sections["coefficient_kill"])
    direct_kernel_zero = all(row["zero_proved"] for row in sections["kernel_zero"])
    bound_schema = any(row["bound_id"] == "HKB2817_1_double_zero_leakage" and row["uses_2816_Csign"] for row in sections["bound_schema"])
    rows = [
        ("CG2817_0_sources_anchored", "2817 source anchors are present", all(row["anchor_found"] for row in sections["sources"]), "all required anchors were found"),
        ("CG2817_1_direct_kernel_zero", "M_m and M_L kernel-zero theorem is proved", direct_kernel_zero, "direct kernel-zero remains conditional/closure-looking"),
        ("CG2817_2_coefficient_kill", "strict double-zero coefficient kill is algebraically exact", coefficient_lemma, "exact if parent lock and F=F'=0 premises hold"),
        ("CG2817_3_bound_schema", "finite leakage bound schema exists under 2816 convention", bound_schema, "bound remains symbolic until Delta_m, kernels and domain constants are sourced"),
        ("CG2817_4_local_claim", "local-GR/WEP/PPN/orbital claim can be made", False, "hidden Kmetric kernels, lock amplitude and observable projection remain open"),
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
        ("DEC2817_0_do_not_force_ML_zero", "Do not make direct L_cg metric silence the main route.", "It is exact under fixed-L0 closure but still unsigned and easier to challenge.", "use it only as a fallback or notation split"),
        ("DEC2817_1_prefer_source_root", "Prefer strict double-zero/source-root coefficient kill.", "It deletes both algebraic M_m and M_L channels without assuming the kernels vanish.", "derive local lock and F-root from the parent action"),
        ("DEC2817_2_next_quantity", "The next physical quantity is Delta_m or N_lock.", "If exact lock fails, the algebraic chain is bounded by Delta_m and finite kernels under the 2816 convention.", "2818 should derive local lock amplitude law or fill the first N_src/N_inner bound row"),
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
            "next_id": "NEXT2817_0_2818",
            "next_target": "2818-Y5-R2FR-local-lock-amplitude-law-or-first-Nlock-input-under-AX1090.md",
            "script": "scripts/Y5_R2FR_local_lock_amplitude_law_or_first_Nlock_input_under_AX1090_2818.py",
            "objective": "derive exact local lock Delta_m=0 from the parent no-hair/source-boundary silence premises, or produce the first finite N_lock input row starting with N_src or N_inner so the 2817 chain bound can become numeric",
            "include": "energy norm E_m; D_m/M_scr assumptions; N_src; N_inner; C_emb; Delta_m bridge; same local domain; hidden kernel blockers retained",
            "exclude": "claiming local GR from coefficient kill alone; plateau axiom; fitted per-system root; measured-G absorption; GitHub; formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": utc_now(),
        }
    ]


def copy_branches() -> list[dict[str, Any]]:
    copy_plan = [
        (OUTPUTS["premises"], BRANCH_OUTPUTS["premise_queue"], "premise_queue"),
        (OUTPUTS["kernel_zero"], BRANCH_OUTPUTS["zero_queue"], "zero_queue"),
        (OUTPUTS["coefficient_kill"], BRANCH_OUTPUTS["kill_queue"], "kill_queue"),
        (OUTPUTS["bound_schema"], BRANCH_OUTPUTS["bound_queue"], "bound_queue"),
        (OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next_queue"),
        (OUTPUTS["coefficient_kill"], BRANCH_OUTPUTS["beta_doc"], "beta_doc"),
        (OUTPUTS["bound_schema"], BRANCH_OUTPUTS["local_bound_copy"], "local_bound_copy"),
        (OUTPUTS["gates"], BRANCH_OUTPUTS["microscope_copy"], "microscope_copy"),
    ]
    rows = []
    for source, destination, label in copy_plan:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            {
                "copy_id": f"BC2817_{label}",
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
        ("VAL2817_0_sources_exist", all(row["path_exists"] for row in sections["sources"]), "all source-register local paths exist"),
        ("VAL2817_1_source_anchors", all(row["anchor_found"] for row in sections["sources"]), "all source-register anchors were found"),
        ("VAL2817_2_premises_anchored", all(row["anchor_found"] for row in sections["premises"]), "all premise audit anchors were found"),
        ("VAL2817_3_direct_zero_not_claimed", all(not row["zero_proved"] for row in sections["kernel_zero"]), "direct M_m/M_L kernel-zero is not claimed"),
        ("VAL2817_4_coefficient_kill_exact_conditional", any(row["kill_id"] == "CK2817_1_exact_double_zero" and row["exact_if_premises_hold"] for row in sections["coefficient_kill"]), "strict double-zero coefficient kill lemma recorded"),
        ("VAL2817_5_hidden_terms_retained", any(row["kill_id"] == "CK2817_3_hidden_terms_guard" and row["status"] == "HIDDEN_KERNELS_RETAINED" for row in sections["coefficient_kill"]), "hidden Kmetric terms remain retained"),
        ("VAL2817_6_bound_schema_uses_2816", all(row["uses_2816_Csign"] for row in sections["bound_schema"]), "bound schema uses 2816 Csign convention"),
        ("VAL2817_7_bound_schema_nonclaim", all(not row["score_ready"] and not row["claim_allowed"] for row in sections["bound_schema"]), "bound rows remain nonclaim"),
        ("VAL2817_8_claim_gates_safe", all(str(row["claim_allowed"]).lower() == "false" for row in sections["gates"]), "all claim gates keep claims blocked"),
        ("VAL2817_9_next_target_2818", any(row["next_id"] == "NEXT2817_0_2818" for row in sections["next"]), "next target is 2818"),
        ("VAL2817_10_branch_outputs_exist", all(path.exists() for path in BRANCH_OUTPUTS.values()), "branch copies were written"),
        ("VAL2817_11_outputs_exist", all(path.exists() for path in generated_paths), "all generated output paths exist"),
        ("VAL2817_12_csv_parse", all(csv_parses(path) for path in generated_paths), "all generated CSV outputs parse"),
        ("VAL2817_13_cited_paths_exist", cited_paths_exist(sections), "all cited local file/copy paths in generated rows exist"),
        ("VAL2817_14_no_claim_flags", not claim_flags_true(sections), "no valid_for_claim or claim_allowed flag is true"),
        ("VAL2817_15_generated_under_post_checkpoint", all(str(path).startswith(str(WORK)) for path in generated_paths + [DOC]), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2817_16_formalization_untouched", formalization_untouched_since_run(), "formalization-workbench was not modified during this run"),
        ("VAL2817_17_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [{"validation_id": check_id, "passed": bool(passed), "detail": detail, "generated_utc": utc_now()} for check_id, passed, detail in checks]
    rows.append(
        {
            "validation_id": "VAL2817_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2817 rejects direct M_m/M_L kernel-zero as a live claim, records the exact strict-double-zero coefficient-kill lemma under the 2816 convention, and stages the Delta_m/N_lock leakage bound route.",
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
        "# 2817 - Y5 R2FR First Mm ML Kernel Zero Proof Or Response Bound Under AX1090",
        "",
        "## Private Verdict",
        "",
        "2817 does not prove the direct `M_m^{00}=M_L^{00}=0` theorem as a live MTS claim. The fixed-field and fixed-`L0` routes are exact under their own hypotheses, but those hypotheses still look like closure unless the parent action signs them.",
        "",
        "The useful progress is better: under the 2816 Hilbert-normalized convention, the algebraic chain `K_alg^{00}=L_cg^-2 F'(m)M_m^{00}-2L_cg^-3F(m)M_L^{00}` is exactly killed at an exact local lock if `F(m_*)=F'(m_*)=0`, even when `M_m` and `M_L` are finite.",
        "",
        "So the preferred route is now source-root/double-zero plus local lock amplitude, not direct Lcg metric silence. If exact lock fails, 2817 stages the finite leakage bound in terms of `Delta_m`, `M_m_bar`, `M_L_bar`, `F2_bar`, and `L_min`.",
        "",
        "## Parent Premise Match Audit",
        markdown_table(sections["premises"], ["premise_id", "premise", "status", "evidence"]),
        "",
        "## Mm ML Kernel Zero Attempt",
        markdown_table(sections["kernel_zero"], ["attempt_id", "target", "status", "missing_or_guard", "zero_proved"]),
        "",
        "## Strict Double-Zero Coefficient Kill",
        markdown_table(sections["coefficient_kill"], ["kill_id", "object", "status", "exact_if_premises_hold", "live_claim"]),
        "",
        "## Hilbert-Normalized Chain Bound Schema",
        markdown_table(sections["bound_schema"], ["bound_id", "branch", "bound_or_result", "status", "missing_inputs"]),
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
        "premises": build_premise_rows(),
        "kernel_zero": build_kernel_zero_rows(),
        "coefficient_kill": build_coefficient_kill_rows(),
        "bound_schema": build_bound_schema_rows(),
    }
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
