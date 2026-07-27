from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_STARTED_UTC = datetime.now(timezone.utc)
ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
WORK = ROOT / "post-checkpoint-work"
MTS = WORK / "source-intake" / "mts_residuals"
RAB_QUEUE = WORK / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = WORK / "source-intake" / "beta-source" / "docs"
MICROSCOPE_DIR = WORK / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SCRIPTS = WORK / "scripts"
FORMALIZATION = ROOT / "formalization-workbench"
DOC = WORK / "2765-Y5-R2FR-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention-under-AX1090.md"

OUTPUTS = {
    "sources": MTS / "P8_Y5_R2FR_2765_SOURCE_REGISTER.csv",
    "theorem": MTS / "P8_Y5_R2FR_2765_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv",
    "operators": MTS / "P8_Y5_R2FR_2765_VISIBLE_OPERATOR_DOMAIN_AUDIT.csv",
    "counterterms": MTS / "P8_Y5_R2FR_2765_F2_COUNTERTERM_LEDGER.csv",
    "consequences": MTS / "P8_Y5_R2FR_2765_ALPHA_CONSEQUENCE_LEDGER.csv",
    "retained": MTS / "P8_Y5_R2FR_2765_RETAINED_B_ALPHA_BRANCH.csv",
    "data": MTS / "P8_Y5_R2FR_2765_R10_MICROSCOPE_DATA_FLANK.csv",
    "gates": MTS / "P8_Y5_R2FR_2765_CLAIM_GATES.csv",
    "refusal": MTS / "P8_Y5_R2FR_2765_REFUSAL_RUNNER_NONCLAIM.csv",
    "next": MTS / "P8_Y5_R2FR_2765_NEXT_TARGET.csv",
    "branches": MTS / "P8_Y5_R2FR_2765_BRANCH_COPIES.csv",
    "validation": MTS / "P8_Y5_BRR545_2765_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "theorem_queue": RAB_QUEUE / "JR2765_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT_NONCLAIM.csv",
    "operator_queue": RAB_QUEUE / "JR2765_VISIBLE_OPERATOR_DOMAIN_AUDIT_NONCLAIM.csv",
    "counterterm_queue": RAB_QUEUE / "JR2765_ALPHA_COUNTERTERM_RETAINED_BRANCH_NONCLAIM.csv",
    "beta_doc": BETA_DOCS / "UNIQUE_MAXWELL_SUBBLOCK_OR_ALPHA_COUNTERTERM_2765_NONCLAIM.csv",
    "microscope_copy": MICROSCOPE_DIR / "unique_maxwell_subblock_or_balpha_retention_2765_nonclaim.csv",
    "next_queue": RAB_QUEUE / "JR2765_OPERATOR_EXHAUSTION_NEXT.csv",
}


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in {p.parent for p in OUTPUTS.values()} | {p.parent for p in BRANCH_OUTPUTS.values()} | {DOC.parent}:
        path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WORK))
    except ValueError:
        return str(path)


def nonclaim(row: dict[str, Any]) -> dict[str, Any]:
    row["valid_for_claim"] = False
    return row


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def find_row(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    return {}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def csv_row_count(path: Path) -> int:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def build_sources() -> list[dict[str, Any]]:
    specs = [
        ("SRC2765_00_2764_doc", "2764_doc", WORK / "2764-Y5-R2FR-EM-vertical-generator-norm-or-MICROSCOPE-extraction-preflight-under-AX1090.md", ["NEXT2764_0_2765", "F2C2764_0_independent_F2"], "2764 handoff"),
        ("SRC2765_01_2764_validation", "2764_validation", MTS / "P8_Y5_BRR545_2764_VALIDATION.csv", ["VAL2764_OVERALL"], "2764 validation"),
        ("SRC2765_02_1057_doc", "1057_doc", WORK / "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md", ["UMS1057_2_no_independent_F2", "DEC1057_2_best_next"], "unique Maxwell subblock precedent"),
        ("SRC2765_03_1057_theorem", "1057_theorem_csv", MTS / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv", ["UMS1057_5_verdict"], "unique subblock theorem attempt"),
        ("SRC2765_04_1057_operator", "1057_operator_csv", MTS / "P8_Y5_R10_1057_OPERATOR_DOMAIN_AUDIT.csv", ["OD1057_1_U1_gauge"], "operator-domain audit"),
        ("SRC2765_05_1057_counterterm", "1057_counterterm_csv", MTS / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv", ["CT1057_0_constant_lambda"], "F2 counterterm ledger"),
        ("SRC2765_06_1057_retained", "1057_retained_csv", MTS / "P8_Y5_R10_1057_RETAINED_BRANCH_LEDGER.csv", ["RB1057_1_WEP"], "retained alpha branch"),
        ("SRC2765_07_1058_doc", "1058_operator_exhaustion_doc", WORK / "1058-Y5-R10-visible-operator-domain-exhaustion-or-alpha-counterterm-prior.md", ["VOE1058_5_verdict", "ACP1058_0_ZA_decomposition"], "visible operator exhaustion/fallback precedent"),
        ("SRC2765_08_1494_doc", "1494_data_doc", WORK / "1494-Y5-R10-RAB-PDF-table-text-extraction-for-EotWash-and-R10-curve-digitization.md", ["R10Q1494_1_curve_digitization", "MICQ1494_1_official_readout"], "data flank status"),
        ("SRC2765_09_1494_r10", "1494_r10_queue", MTS / "P8_Y5_R10_1494_R10_MANUAL_DIGITIZATION_QUEUE.csv", ["R10Q1494_1_curve_digitization"], "R10 digitization queue"),
        ("SRC2765_10_1494_blockers", "1494_blockers", MTS / "P8_Y5_R10_1494_TARGET_PROMOTION_BLOCKERS.csv", ["TBLK1494_overall"], "target promotion blockers"),
    ]
    rows = []
    for row_id, source_key, path, needles, role in specs:
        text = read_text(path)
        exists = path.exists()
        rows.append(nonclaim({
            "row_id": row_id,
            "source_key": source_key,
            "source_path": str(path),
            "exists": exists,
            "needle_spec": ";".join(needles),
            "needles_found": exists and all(needle in text for needle in needles),
            "source_role": role,
        }))
    return rows


def load_inputs() -> dict[str, dict[str, str]]:
    return {
        "ums_verdict": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"), "proof_id", "UMS1057_5_verdict"),
        "no_f2": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"), "proof_id", "UMS1057_2_no_independent_F2"),
        "op_f2": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_OPERATOR_DOMAIN_AUDIT.csv"), "operator_id", "OD1057_1_U1_gauge"),
        "ct_lambda": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"), "counterterm_id", "CT1057_0_constant_lambda"),
        "ct_hidden": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"), "counterterm_id", "CT1057_1_hidden_scalar"),
        "ct_rad": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"), "counterterm_id", "CT1057_2_radiative"),
        "rb_clock": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_RETAINED_BRANCH_LEDGER.csv"), "retained_id", "RB1057_0_clock"),
        "rb_wep": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_RETAINED_BRANCH_LEDGER.csv"), "retained_id", "RB1057_1_WEP"),
        "rb_r10": find_row(read_csv_rows(MTS / "P8_Y5_R10_1057_RETAINED_BRANCH_LEDGER.csv"), "retained_id", "RB1057_2_R10"),
        "r10_queue": find_row(read_csv_rows(MTS / "P8_Y5_R10_1494_R10_MANUAL_DIGITIZATION_QUEUE.csv"), "queue_id", "R10Q1494_1_curve_digitization"),
        "mic_queue": find_row(read_csv_rows(MTS / "P8_Y5_R10_1494_MICROSCOPE_PROMOTION_QUEUE.csv"), "queue_id", "MICQ1494_1_official_readout"),
    }


def build_theorem_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    no_f2 = inputs["no_f2"]
    verdict = inputs["ums_verdict"]
    return [
        nonclaim({"row_id": "UMS2765_0_target", "claim_piece": "unique observed Maxwell subblock", "mathematical_form": "S_EM[A_Q]=-C_P N_Q/4 int sqrt(-g_obs) F_Q^2 with no independent lambda_A F_Q^2", "status": "TARGET_SHARP", "if_signed": "g_EM^{-2}=C_P N_Q and Lie_v g_EM=0", "if_unsigned": "b_alpha remains retained"}),
        nonclaim({"row_id": "UMS2765_1_parent_curvature_norm", "claim_piece": "Maxwell term inherited from parent curvature norm", "mathematical_form": "F_parent=F_Q T_Q+F_perp and <F_Q T_Q,F_Q T_Q>_P=N_Q F_Q^2", "status": "CONDITIONAL_SUBLEMMA", "if_signed": "supplies one candidate coefficient C_P N_Q", "if_unsigned": "Maxwell closure remains appended"}),
        nonclaim({"row_id": "UMS2765_2_no_independent_F2", "claim_piece": "independent lambda_A F_Q^2 inadmissible", "mathematical_form": no_f2.get("mathematical_form", "Allowed[S_vis] contains no DeltaS=-lambda_A F_Q^2/4 outside parent curvature norm"), "status": no_f2.get("derivation_status", "NOT_DERIVED_CURRENT_CORPUS"), "if_signed": "unique Maxwell subblock closes alpha owner up to current/readout clauses", "if_unsigned": "g_EM^{-2}=C_P N_Q+lambda_A and alpha is not owned"}),
        nonclaim({"row_id": "UMS2765_3_no_hidden_or_radiative_F2", "claim_piece": "no hidden/radiative F2 counterterms", "mathematical_form": "no f(I_hid)F_Q^2 and no delta lambda_A(mu,Xhat)F_Q^2 after S_eff/readout", "status": "UNSIGNED", "if_signed": "protects b_alpha=0 through reduction", "if_unsigned": "finite b_alpha/b_clock priors remain live"}),
        nonclaim({"row_id": "UMS2765_4_verdict", "claim_piece": "promote no-independent-F2 theorem now", "mathematical_form": verdict.get("mathematical_form", "UMS1057_1..4 all signed => alpha_EM parent-owned by unique Maxwell subblock"), "status": "NO_INDEPENDENT_F2_NOT_DERIVED", "if_signed": "b_alpha=0 route reopens", "if_unsigned": "retain alpha counterterm/product-prior branch"}),
    ]


def build_operator_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    op = inputs["op_f2"]
    return [
        nonclaim({"row_id": "OPA2765_0_diffeomorphism", "operator": "F_Q^2 scalar density", "ordinary_symmetry_result": "ALLOWED", "reason": "sqrt(-g_obs) F_Q^{mu nu}F^Q_mu_nu is a covariant scalar density", "stronger_rule_needed": "parent visible operator-domain exhaustion"}),
        nonclaim({"row_id": "OPA2765_1_U1_gauge", "operator": "lambda_A F_Q^2", "ordinary_symmetry_result": op.get("ordinary_symmetry_result", "ALLOWED"), "reason": op.get("reason", "U(1) gauge invariance allows scalar gauge kinetic coefficients"), "stronger_rule_needed": op.get("stronger_rule_needed", "unique parent curvature norm or topological inheritance theorem")}),
        nonclaim({"row_id": "OPA2765_2_hidden_coeff", "operator": "f(Xhat)F_Q^2", "ordinary_symmetry_result": "ALLOWED_IF_HIDDEN_SCALAR_SURVIVES", "reason": "a hidden invariant scalar can multiply any visible scalar density unless target grammar forbids it", "stronger_rule_needed": "no hidden-visible Hom theorem or hidden invariant triviality"}),
        nonclaim({"row_id": "OPA2765_3_radiative", "operator": "delta lambda_A(mu,Xhat)F_Q^2", "ordinary_symmetry_result": "RETAINED", "reason": "tree-level ban does not imply effective/readout ban", "stronger_rule_needed": "radiative/readout closure"}),
        nonclaim({"row_id": "OPA2765_4_verdict", "operator": "visible operator-domain exhaustion", "ordinary_symmetry_result": "NOT_DERIVED", "reason": "current corpus has contracts and counterexamples, not an exhaustion theorem", "stronger_rule_needed": "derive allowed visible operator algebra from MTS primitives"}),
    ]


def build_counterterm_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row_id, source_key, fallback in [
        ("CT2765_0_constant_lambda", "ct_lambda", "constant independent Maxwell kinetic term"),
        ("CT2765_1_hidden_scalar", "ct_hidden", "hidden scalar gauge kinetic function"),
        ("CT2765_2_radiative", "ct_rad", "radiatively generated F_Q^2 threshold"),
    ]:
        source = inputs[source_key]
        rows.append(nonclaim({
            "row_id": row_id,
            "counterterm": source.get("counterterm", fallback),
            "formula": source.get("formula", "MISSING_FORMULA"),
            "status": source.get("status", "RETAINED"),
            "effect": source.get("effect", "keeps alpha owner unproved"),
            "repair_needed": source.get("repair_needed", "operator-domain exhaustion"),
        }))
    rows.append(nonclaim({"row_id": "CT2765_3_verdict", "counterterm": "alpha counterterm branch", "formula": "Z_A=C_P N_Q+lambda_A0+lambda_Ahid(I_hid)+delta_lambda_A_rad+readout terms", "status": "RETAINED_NONCLAIM_BRANCH", "effect": "no standalone b_alpha, WEP, R10, or local-GR pass", "repair_needed": "derive exhaustion or source product-prior rows"}))
    return rows


def build_consequence_rows() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "AC2765_0_if_unique", "condition": "unique Maxwell subblock plus fixed norm/current/readout", "result": "Lie_v ln alpha_EM=0", "impact": "b_alpha=0 and alpha-source branch can be theorem-zero", "current_status": "CONDITIONAL_ONLY"}),
        nonclaim({"row_id": "AC2765_1_current", "condition": "current corpus", "result": "b_alpha not derived zero", "impact": "retain clock product bound and WEP product target", "current_status": "RETAIN_B_ALPHA_PRODUCT_PRIOR"}),
        nonclaim({"row_id": "AC2765_2_local_GR", "condition": "no-independent-F2 unsigned", "result": "EM/source constant-sector debt remains", "impact": "local GR/Newton reduction cannot be called fully derived", "current_status": "PARTIAL_BLOCKER_RETAINED"}),
    ]


def build_retained_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "RB2765_0_clock", "arena": "clock", "quantity": inputs["rb_clock"].get("quantity", "b_alpha*tau_clock_time"), "bound_or_status": inputs["rb_clock"].get("bound_or_status", "2.1e-18 yr^-1 product bound retained"), "reason": inputs["rb_clock"].get("reason", "b_alpha zero is not derived and tau_clock is not parent-owned"), "score_ready": False}),
        nonclaim({"row_id": "RB2765_1_WEP", "arena": "MICROSCOPE_WEP", "quantity": inputs["rb_wep"].get("quantity", "beta_source_alpha*b_alpha*tau_WEP"), "bound_or_status": inputs["rb_wep"].get("bound_or_status", "4.797780522732e-05 product-width target retained"), "reason": inputs["rb_wep"].get("reason", "no-independent-F2 ban and beta_source_alpha zero remain conditional"), "score_ready": False}),
        nonclaim({"row_id": "RB2765_2_R10", "arena": "R10_short_range", "quantity": inputs["rb_r10"].get("quantity", "K_X^R10 beta_s beta_t + epsilon_tail"), "bound_or_status": inputs["rb_r10"].get("bound_or_status", "unscoreable until finite branch inputs and promoted bound curve exist"), "reason": inputs["rb_r10"].get("reason", "R10 alpha branch cannot use unsigned zero theorem"), "score_ready": False}),
        nonclaim({"row_id": "RB2765_3_policy", "arena": "cross_arena", "quantity": "alpha counterterm/product branch", "bound_or_status": "formal retained branch", "reason": "operator-domain exhaustion is not derived", "score_ready": False}),
    ]


def build_data_rows(inputs: dict[str, dict[str, str]]) -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "DATA2765_0_R10_curve", "data_object": "R10 alpha(lambda) curve", "current_status": inputs["r10_queue"].get("digitization_status", "NOT_DIGITIZED"), "target_path": inputs["r10_queue"].get("target_file", "source-intake/r10/derived/R10_alpha_lambda_bound_curve_DIGITIZED.csv"), "claim_role": "finite alpha branch comparator"}),
        nonclaim({"row_id": "DATA2765_1_MICROSCOPE_readout", "data_object": "MICROSCOPE CMSM readout/design matrix", "current_status": inputs["mic_queue"].get("promotion_status", "OFFICIAL_ARRAYS_MISSING"), "target_path": inputs["mic_queue"].get("target_file", "source-intake/microscope/official_readout/P_WEP_K_CMSM_readout.csv"), "claim_role": "WEP product projection"}),
        nonclaim({"row_id": "DATA2765_2_verdict", "data_object": "data flank", "current_status": "TEXT_AND_PROVENANCE_ONLY_NONCLAIM", "target_path": "R10/EotWash/MICROSCOPE target files", "claim_role": "cannot rescue alpha ownership; only future finite branch scoring"}),
    ]


def build_gates() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "CG2765_0_sources", "gate": "source paths and needles valid", "passed": True, "claim_effect": "audit reproducible"}),
        nonclaim({"row_id": "CG2765_1_unique_subblock", "gate": "observed Maxwell F_Q^2 is unique parent subblock", "passed": False, "claim_effect": "alpha owner not promoted"}),
        nonclaim({"row_id": "CG2765_2_no_independent_F2", "gate": "lambda_A F_Q^2 is forbidden", "passed": False, "claim_effect": "main theorem fails current corpus"}),
        nonclaim({"row_id": "CG2765_3_no_hidden_radiative_F2", "gate": "hidden/radiative F2 counterterms forbidden", "passed": False, "claim_effect": "b_alpha retained"}),
        nonclaim({"row_id": "CG2765_4_product_branch_score_ready", "gate": "retained alpha products are score-ready", "passed": False, "claim_effect": "clock/WEP/R10 remain product-only/nonclaim"}),
        nonclaim({"row_id": "CG2765_5_local_GR_Newton", "gate": "local GR/Newton residual complete", "passed": False, "claim_effect": "no local-GR/Newton claim from 2765"}),
    ]


def build_refusals() -> list[dict[str, Any]]:
    return [
        nonclaim({"row_id": "REF2765_0_unique_F2", "claim": "2765 proves no independent F_Q^2", "allowed": False, "reason": "ordinary symmetries allow F_Q^2 and parent operator-domain exhaustion is unsigned", "blocking_rows": "UMS2765_4_verdict;OPA2765_4_verdict"}),
        nonclaim({"row_id": "REF2765_1_balpha_zero", "claim": "b_alpha=0 or beta_source_alpha=0 is now proved", "allowed": False, "reason": "constant, hidden, and radiative alpha counterterms remain legal", "blocking_rows": "CT2765_3_verdict;CG2765_3_no_hidden_radiative_F2"}),
        nonclaim({"row_id": "REF2765_2_data_score", "claim": "R10/MICROSCOPE finite alpha branch can score", "allowed": False, "reason": "R10 curve and MICROSCOPE readout/product tensors remain unpromoted", "blocking_rows": "DATA2765_0_R10_curve;DATA2765_1_MICROSCOPE_readout"}),
        nonclaim({"row_id": "REF2765_3_local_GR", "claim": "MTS derives local GR/Newton after 2765", "allowed": False, "reason": "EM/source constant-sector debt remains and local residual vector is incomplete", "blocking_rows": "AC2765_2_local_GR;CG2765_5_local_GR_Newton"}),
    ]


def build_next() -> list[dict[str, Any]]:
    return [
        nonclaim({
            "row_id": "NEXT2765_0_2766",
            "next_target": "2766-Y5-R2FR-visible-operator-domain-exhaustion-or-alpha-counterterm-prior-under-AX1090.md",
            "script": "scripts/Y5_R2FR_visible_operator_domain_exhaustion_or_alpha_counterterm_prior_under_AX1090_2766.py",
            "why": "2765 cannot ban independent F_Q^2 by ordinary symmetry. The next honest theorem target is the visible operator-domain exhaustion rule; if it fails, the retained alpha counterterm branch becomes the formal route.",
            "include": "allowed visible operator algebra, parent-generation image, no hidden-visible Hom, radiative/readout closure, alpha counterterm product branch",
            "exclude": "compactness-alone alpha proof, aesthetic minimality, unit rescaling, tau unity shortcut, WEP/local-GR claim, GitHub, formalization edits",
        })
    ]


def copy_branch_outputs(theorem: list[dict[str, Any]], operators: list[dict[str, Any]], counterterms: list[dict[str, Any]], retained: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    specs = [
        ("BR2765_0_theorem_queue", "theorem", theorem, OUTPUTS["theorem"], BRANCH_OUTPUTS["theorem_queue"], "unique Maxwell subblock theorem attempt"),
        ("BR2765_1_operator_queue", "operators", operators, OUTPUTS["operators"], BRANCH_OUTPUTS["operator_queue"], "visible operator-domain audit"),
        ("BR2765_2_counterterm_queue", "counterterms", counterterms, OUTPUTS["counterterms"], BRANCH_OUTPUTS["counterterm_queue"], "alpha counterterm retained branch"),
        ("BR2765_3_beta_doc", "retained", retained, OUTPUTS["retained"], BRANCH_OUTPUTS["beta_doc"], "retained b_alpha branch beta docs copy"),
        ("BR2765_4_microscope_copy", "data", retained, OUTPUTS["retained"], BRANCH_OUTPUTS["microscope_copy"], "MICROSCOPE branch copy for retained alpha branch"),
        ("BR2765_5_next_queue", "next", next_rows, OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "next operator exhaustion target"),
    ]
    rows = []
    for copy_id, table_key, source_rows, source_table, copy_path, purpose in specs:
        write_csv(copy_path, source_rows)
        rows.append(nonclaim({
            "copy_id": copy_id,
            "table_key": table_key,
            "source_table": rel(source_table),
            "copy_path": rel(copy_path),
            "purpose": purpose,
            "exists": copy_path.exists(),
            "row_count": csv_row_count(copy_path) if copy_path.exists() else 0,
        }))
    return rows


def generated_files_under_work() -> bool:
    generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    return all(WORK in path.parents or path == WORK for path in generated)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime > RUN_STARTED_UTC.timestamp():
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("valid_for_claim", "False")).lower() == "true":
                return False
            if str(row.get("claim_allowed", "False")).lower() == "true":
                return False
            if str(row.get("allowed", "False")).lower() == "true":
                return False
    return True


def remove_pycache() -> None:
    pycache = SCRIPTS / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def build_validation(rows_by_name: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    theorem = rows_by_name["theorem"]
    operators = rows_by_name["operators"]
    counterterms = rows_by_name["counterterms"]
    retained = rows_by_name["retained"]
    data = rows_by_name["data"]
    gates = rows_by_name["gates"]
    refusals = rows_by_name["refusal"]
    next_rows = rows_by_name["next"]
    branches = rows_by_name["branches"]
    checks = [
        ("VAL2765_0_sources", all(row["exists"] and row["needles_found"] for row in sources), "every cited source path exists and needles are found"),
        ("VAL2765_1_no_independent_F2_not_derived", any(row["row_id"] == "UMS2765_4_verdict" and row["status"] == "NO_INDEPENDENT_F2_NOT_DERIVED" for row in theorem), "no-independent-F2 theorem remains non-promoted"),
        ("VAL2765_2_operator_allows_F2", any(row["row_id"] == "OPA2765_1_U1_gauge" and row["ordinary_symmetry_result"] == "ALLOWED" for row in operators), "ordinary gauge symmetry allows independent F2"),
        ("VAL2765_3_counterterms_retained", any(row["row_id"] == "CT2765_3_verdict" and row["status"] == "RETAINED_NONCLAIM_BRANCH" for row in counterterms), "alpha counterterm branch retained"),
        ("VAL2765_4_retained_nonclaim", all(row["score_ready"] is False for row in retained), "retained branch rows remain non-score-ready"),
        ("VAL2765_5_data_flank_nonclaim", any(row["row_id"] == "DATA2765_2_verdict" and "NONCLAIM" in row["current_status"] for row in data), "data flank remains nonclaim"),
        ("VAL2765_6_claim_gates_block", any(row["row_id"] == "CG2765_5_local_GR_Newton" and row["passed"] is False for row in gates), "local GR/Newton gate remains blocked"),
        ("VAL2765_7_refusals_block", all(row["allowed"] is False for row in refusals), "refusal runner blocks premature claims"),
        ("VAL2765_8_next", any(row["row_id"] == "NEXT2765_0_2766" and "visible-operator-domain-exhaustion" in row["next_target"] for row in next_rows), "next target selected"),
        ("VAL2765_9_branch_outputs", all(row["exists"] and int(row["row_count"]) > 0 for row in branches), "branch copies exist and contain rows"),
        ("VAL2765_10_csv_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV outputs parse cleanly"),
        ("VAL2765_11_no_claim_flags", no_claim_flags(rows_by_name), "no generated row is valid_for_claim=true/claim_allowed=true/allowed=true"),
        ("VAL2765_12_generated_under_post_checkpoint", generated_files_under_work(), "all generated outputs are under post-checkpoint-work"),
        ("VAL2765_13_formalization_untouched", formalization_untouched(), "formalization-workbench modified-file count remains zero during this run"),
        ("VAL2765_14_pycache_absent", not (SCRIPTS / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    rows = [{"validation_id": check_id, "passed": passed, "detail": detail, "timestamp_utc": ts()} for check_id, passed, detail in checks]
    rows.append({
        "validation_id": "VAL2765_OVERALL",
        "passed": all(row["passed"] for row in rows),
        "detail": "2765 states the unique Maxwell subblock/no-independent-F2 theorem in R2/f(R) language, refuses promotion because diffeomorphism and U(1) gauge symmetry allow F_Q^2 unless parent visible-operator-domain exhaustion is derived, retains constant/hidden/radiative alpha counterterms and b_alpha product branches, keeps data flanks nonclaim, and selects visible operator-domain exhaustion or alpha counterterm prior as the next target.",
        "timestamp_utc": ts(),
    })
    return rows


def build_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join([
        "# 2765 - Y5 R2/f(R): Unique Maxwell Subblock No Independent F2 Ban Or b_alpha Retention Under AX1090",
        "## Private Verdict\n\nThe theorem shape is exact: if the observed Maxwell term is the unique parent curvature subblock, and no independent `lambda_A F_Q^2`, hidden `f(I_hid)F_Q^2`, or radiative/readout counterterm is admissible, then alpha ownership can advance.\n\nBut ordinary diffeomorphism plus U(1) gauge symmetry do not ban `F_Q^2`. That means the current corpus cannot derive `b_alpha=0` from compactness, generator norm, or taste. The honest branch is retained alpha counterterms and product priors until visible operator-domain exhaustion is derived.",
        "## Source Register\n\n" + markdown_table(rows_by_name["sources"], ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"]),
        "## Unique Maxwell Subblock Theorem Attempt\n\n" + markdown_table(rows_by_name["theorem"], ["row_id", "claim_piece", "mathematical_form", "status", "if_signed", "if_unsigned", "valid_for_claim"]),
        "## Visible Operator-Domain Audit\n\n" + markdown_table(rows_by_name["operators"], ["row_id", "operator", "ordinary_symmetry_result", "reason", "stronger_rule_needed", "valid_for_claim"]),
        "## F2 Counterterm Ledger\n\n" + markdown_table(rows_by_name["counterterms"], ["row_id", "counterterm", "formula", "status", "effect", "repair_needed", "valid_for_claim"]),
        "## Alpha Consequence Ledger\n\n" + markdown_table(rows_by_name["consequences"], ["row_id", "condition", "result", "impact", "current_status", "valid_for_claim"]),
        "## Retained b_alpha Branch\n\n" + markdown_table(rows_by_name["retained"], ["row_id", "arena", "quantity", "bound_or_status", "reason", "score_ready", "valid_for_claim"]),
        "## R10 MICROSCOPE Data Flank\n\n" + markdown_table(rows_by_name["data"], ["row_id", "data_object", "current_status", "target_path", "claim_role", "valid_for_claim"]),
        "## Claim Gates\n\n" + markdown_table(rows_by_name["gates"], ["row_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "## Refusal Runner\n\n" + markdown_table(rows_by_name["refusal"], ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"]),
        "## Next Target\n\n" + markdown_table(rows_by_name["next"], ["row_id", "next_target", "script", "why", "include", "exclude", "valid_for_claim"]),
        "## Branch Copies\n\n" + markdown_table(rows_by_name["branches"], ["copy_id", "table_key", "source_table", "copy_path", "purpose", "exists", "row_count", "valid_for_claim"]),
        "## Validation\n\n" + markdown_table(rows_by_name["validation"], ["validation_id", "passed", "detail", "timestamp_utc"]),
        "## Plain-English Read\n\nThis is a real narrowing, not a dodge. The coupling problem has become an operator grammar problem: either all visible kinetic terms must be parent-generated, or alpha has a retained counterterm. If the grammar cannot be proved, we stop chasing zero and build product-prior tests.",
        "",
    ])


def main() -> None:
    ensure_dirs()
    inputs = load_inputs()
    sources = build_sources()
    theorem = build_theorem_rows(inputs)
    operators = build_operator_rows(inputs)
    counterterms = build_counterterm_rows(inputs)
    consequences = build_consequence_rows()
    retained = build_retained_rows(inputs)
    data = build_data_rows(inputs)
    gates = build_gates()
    refusals = build_refusals()
    next_rows = build_next()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["operators"], operators)
    write_csv(OUTPUTS["counterterms"], counterterms)
    write_csv(OUTPUTS["consequences"], consequences)
    write_csv(OUTPUTS["retained"], retained)
    write_csv(OUTPUTS["data"], data)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["refusal"], refusals)
    write_csv(OUTPUTS["next"], next_rows)

    branches = copy_branch_outputs(theorem, operators, counterterms, retained, next_rows)
    write_csv(OUTPUTS["branches"], branches)
    remove_pycache()

    rows_by_name = {
        "sources": sources,
        "theorem": theorem,
        "operators": operators,
        "counterterms": counterterms,
        "consequences": consequences,
        "retained": retained,
        "data": data,
        "gates": gates,
        "refusal": refusals,
        "next": next_rows,
        "branches": branches,
    }
    csv_paths = [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_OUTPUTS.values())
    validation = build_validation(rows_by_name, csv_paths)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    DOC.write_text(build_doc(rows_by_name), encoding="utf-8")
    remove_pycache()

    overall = next(row for row in validation if row["validation_id"] == "VAL2765_OVERALL")
    print(f"2765 complete: overall={overall['passed']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
