from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3925"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3925-Y5-R2FR-minimal-parent-clause-variation-audit-or-Blocal-bound-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3925_SOURCE_REGISTER.csv",
    "variation": SRC / "P8_Y5_R2FR_3925_PARENT_CLAUSE_VARIATION_AUDIT.csv",
    "adoption": SRC / "P8_Y5_R2FR_3925_ADOPTION_VERDICT_MATRIX.csv",
    "bound_values": SRC / "P8_Y5_R2FR_3925_BLOCAL_BOUND_VALUE_QUEUE.csv",
    "decision": SRC / "P8_Y5_R2FR_3925_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3925_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3925_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3925_VALIDATION.csv",
}

AUDIT_RESULT = (
    "EH, visible Hilbert/Maxwell, quadratic Y, double-zero R11, and G0 blocks pass as variation identities "
    "inside the candidate branch; boundary/projector/domain/history remain signature-dependent and therefore cannot be globally promoted yet."
)
PARTIAL_ADOPTION = (
    "ADOPT_CORE_LOCAL_BRANCH_ONLY: sign EH/source/Y/R11/G0 algebraic core privately, but keep boundary/projector/domain/history as explicit theorem-or-bound gates."
)
BOUND_QUEUE = (
    "Blocal first values: B_escape, P00/Xi_N, delta_beta_common, delta_gamma_R11, Gdot/G, alpha_i/xi, zeta_i"
)
NEXT_DOC = "3926-Y5-R2FR-core-local-branch-adoption-and-escape-bound-prioritization.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3926_core_local_branch_adoption_and_escape_bound_prioritization.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3925_00_next", SRC / "P8_Y5_R2FR_3924_NEXT_TARGET.csv", "NEXT3924_0", "3924 selected variation audit"),
        ("SRC3925_01_clause", SRC / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv", "CLA3924_1_action", "minimal parent action clause"),
        ("SRC3925_02_branch", SRC / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv", "CLA3924_2_branch", "local branch surface"),
        ("SRC3925_03_history", SRC / "P8_Y5_R2FR_3924_SIGNATURE_TO_THEOREM_COVERAGE.csv", "COV3924_11_history", "history partial coverage"),
        ("SRC3925_04_bound", SRC / "P8_Y5_R2FR_3924_FIRST_NUMERIC_BOUND_PACK_IF_NOT_ADOPTED.csv", "NUM3924_8_total", "first numeric bound pack"),
        ("SRC3925_05_decision", SRC / "P8_Y5_R2FR_3924_ADOPTION_DECISION_GATE.csv", "DEC3924_0_clause", "3924 candidate clause decision"),
        ("SRC3925_06_EH", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_1_action", "EH action normal form"),
        ("SRC3925_07_Hilbert", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_0_Hilbert", "Hilbert source bridge"),
        ("SRC3925_08_Maxwell", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_1_Maxwell", "Maxwell stress bridge"),
        ("SRC3925_09_Y", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_1_memory_quadratic", "quadratic Y sector"),
        ("SRC3925_10_interactions", SRC / "P8_Y5_R2FR_3905_PARENT_ACTION_NORMAL_FORM.csv", "NF3905_2_interactions", "no linear visible shadow"),
        ("SRC3925_11_R11", SRC / "P8_Y5_R2FR_3893_R11_SIGMA_FACTORIZATION_INSERTION.csv", "R11S3893_00_candidate_action", "R11 Sigma factorization"),
        ("SRC3925_12_G0", SRC / "P8_Y5_R2FR_3909_GSTAR_ZEROFORM_ACTION_BLOCK.csv", "ZF3909_1_variation_A3", "G0 variation"),
        ("SRC3925_13_boundary", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "boundary unsigned verdict"),
        ("SRC3925_14_projector", SRC / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv", "PC3892_2_product_rule", "projector product rule"),
        ("SRC3925_15_domain_no_go", SRC / "P8_Y5_R2FR_3431_PROJECTOR_VARIATION_NO_STRESS_THEOREM.csv", "DP3431_1_no_go", "domain/projector no-go"),
        ("SRC3925_16_domain_bound", SRC / "P8_Y5_R2FR_3431_PROJECTOR_VARIATION_NO_STRESS_THEOREM.csv", "DP3431_6_operator_bound", "domain/projector bound theorem"),
        ("SRC3925_17_history_fail", SRC / "P8_Y5_R2FR_3895_MEMORY_BOUNDARY_HISTORY_ZERO_ATTEMPT.csv", "ZERO3895_4_history_exact", "history exact zero fails globally"),
        ("SRC3925_18_history_law", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_3_history_decay", "history suppression law"),
        ("SRC3925_19_escape", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_9_total", "escape total bound"),
        ("SRC3925_20_validation", SRC / "P8_Y5_BRR545_3924_VALIDATION.csv", "VAL3924_13_no_pycache", "3924 validation handoff"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:760]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def variation_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("VAR3925_0_EH_Q", "delta_Q S_EH", "delta_Q S_EH -> G_mu_nu+Lambda g_mu_nu", "PASS_IF_EH_SELECTOR_ADOPTED", "public metric equation signed"),
        ("VAR3925_1_visible_Q", "delta_Q S_vis", "delta_Q S_vis -> T_vis^{mu nu}[E(Q),Psi,A] including Maxwell", "PASS_IF_SAME_FRAME_ADOPTED", "Hilbert/Maxwell source signed"),
        ("VAR3925_2_visible_fields", "delta_{Psi,A} S_vis", "visible Euler equations imply nabla_mu T_vis^{mu nu}=0 with Bianchi", "PASS_IF_VISIBLE_EOMS_HOLD", "conservation/zeta route signed in branch"),
        ("VAR3925_3_Y_Q", "delta_Q S_Y at Y=0", "quadratic Y terms give delta_Q S_Y|_{Y=0,nablaY=0}=0", "PASS_IF_Y_BRANCH_AND_GAP_ADOPTED", "no hidden stress from Y vacuum"),
        ("VAR3925_4_Y_Y", "delta_Y S_Y at Y=0", "E_Y=0 at Y=0 only if no affine J_Y/source/boundary term survives", "PASS_FOR_NO_AFFINE_BRANCH_ELSE_BOUND", "source/history/boundary terms remain fallback if present"),
        ("VAR3925_5_interactions", "delta S_int^{>=2}", "no term linear in Y_loc or H_priv means first variations vanish at Y=H=0", "PASS_IF_PARENT_GRAMMAR_ADOPTED", "disformal/source-shadow leak closed"),
        ("VAR3925_6_R11_DZ", "delta S_R11^{DZ}", "F_A(0)=F_A'(0)=0 makes Q,Y first variations vanish on Sigma_loc=0", "PASS_IF_DZ_SELECTOR_ADOPTED", "R11 non-topological stress closed"),
        ("VAR3925_7_G0", "delta_{A3,C_G,Q} S_G0", "delta A3 gives dC_G=0; metric stress silent if A3 class metric-independent", "PASS_IF_TOPOLOGICAL_CLASS_FIXED", "G_* drift component signed"),
        ("VAR3925_8_boundary", "delta S_B^{top}", "boundary stress/flux vanishes only under fixed relative scalar/topological no-flux certificate", "PARTIAL_SIGNATURE_REQUIRED", "not globally signed; keep boundary bound"),
        ("VAR3925_9_projector", "delta S_proj", "readout-only projector is safe; action-level projector needs delta Pi_M=0 and [d,Pi_M]=0", "PARTIAL_SIGNATURE_REQUIRED", "dynamic projector remains bound channel"),
        ("VAR3925_10_domain", "delta_D / delta_g P_D", "fixed q-basic/topological domain can be silent; moving/metric-dependent domain creates stress", "PARTIAL_SIGNATURE_REQUIRED", "domain/projector bound remains active"),
        ("VAR3925_11_history", "history/nonlocal tail", "no-incoming-tail is a branch condition, not a generic variation identity", "BOUND_REQUIRED_UNLESS_LOCAL_RESET_SIGNED", "history cannot be globally adopted as exact zero"),
        ("VAR3925_12_total", "total variation verdict", AUDIT_RESULT, "CORE_PASS_ESCAPE_PARTIAL", "adopt core only; keep escape/history gates"),
    ]
    return [
        {
            "row_id": row_id,
            "variation_target": target,
            "variation_result": result,
            "audit_status": status,
            "consequence": consequence,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, target, result, status, consequence in data
    ]


def adoption_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ADOPT3925_0_core", "EH/source/Y/R11/G0 core", "PASS_PRIVATE_CORE", "can be used as a private local branch candidate after 3925 audit"),
        ("ADOPT3925_1_boundary", "boundary certificate", "PARTIAL_UNSIGNED", "must be parent-signed later or bounded"),
        ("ADOPT3925_2_projector", "projector certificate", "PARTIAL_UNSIGNED", "readout-only safe; action-level dynamic projector remains bound"),
        ("ADOPT3925_3_domain", "fixed q-basic domain", "PARTIAL_UNSIGNED", "fixed/topological route safe; moving/domain-dependent route bounded"),
        ("ADOPT3925_4_history", "no incoming history tail", "NOT_GLOBAL_ZERO", "local reset/no-tail branch or suppression-law bound only"),
        ("ADOPT3925_5_verdict", "adoption verdict", "ADOPT_CORE_LOCAL_BRANCH_ONLY", PARTIAL_ADOPTION),
    ]
    return [
        {
            "row_id": row_id,
            "sector": sector,
            "verdict": verdict,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, sector, verdict, reason in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BQ3925_0_escape", "B_escape", "ESC3922_9_total", "highest priority because boundary/projector/domain/history are partial"),
        ("BQ3925_1_Xi", "P00/Xi_N", "BIN3921_0..9 plus ESC3922 source split", "common-mode residual if escape/P00 not zero"),
        ("BQ3925_2_beta_common", "delta_beta_common", "RUN3920_0..2", "square-law residual if common mode survives"),
        ("BQ3925_3_gamma", "delta_gamma_R11", "GAM3918 bound inputs", "STF leak if R11/DZ route fails"),
        ("BQ3925_4_Gdot", "Gdot/G", "RUN3908_1 plus xi_1 time derivative", "time/history/common-mode drift"),
        ("BQ3925_5_alpha_xi", "alpha_i/xi", "DPPN3431 plus MAP3922", "domain/projector/vector/multipole preferred-frame/location"),
        ("BQ3925_6_zeta", "zeta_i", "non-Hilbert/projector stress leakage", "conservation failure if source bridge not exact"),
        ("BQ3925_7_total", "B_local", "BND3923_8_total", "absolute-sum final local residual vector"),
    ]
    return [
        {
            "row_id": row_id,
            "bound_target": target,
            "source_rows": source_rows,
            "why_priority": why,
            "numeric_value": "",
            "status": "NEXT_NUMERIC_FILL_IF_NOT_THEOREM_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, target, source_rows, why in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3925_0_core",
            "decision": "core local branch variation audit passes privately",
            "formula": "EH + same-frame visible Hilbert/Maxwell + quadratic Y + double-zero R11 + G0",
            "claim_status": "PRIVATE_CORE_BRANCH_ADOPTABLE_NOT_PUBLIC_LOCAL_GR",
            "next_action": "keep escape/history gates separate",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3925_1_escape",
            "decision": "boundary/projector/domain/history do not globally pass variation audit",
            "formula": "must be certificate-signed per branch or bounded by B_escape/B_local",
            "claim_status": "LOCAL_GR_STILL_UNPROMOTED",
            "next_action": "prioritize escape bound or certificate adoption",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3925_2_next",
            "decision": "next step is core local branch adoption plus escape-bound prioritization",
            "formula": BOUND_QUEUE,
            "claim_status": "NONCLAIM_NEXT_GATE",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3925_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "record the private core-local-branch adoption, then prioritize escape/history bounds or certificates needed before any local-GR promotion",
            "why_this_next": "3925 shows the core varies correctly but escape/history sectors remain the active obstruction",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "minimal parent clause variation audit passes for core branch; escape/history sectors remain theorem-or-bound",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3925 - Minimal Parent Clause Variation Audit or B_local Bound Values

Timestamp: `{timestamp}`

## Result

Variation audit result:

`{AUDIT_RESULT}`.

Adoption verdict:

`{PARTIAL_ADOPTION}`.

If the escape/history clauses are not signed, the first bound queue is:

`{BOUND_QUEUE}`.

## Meaning

This is real progress but not a promotion. The core local parent branch now has a plausible variation-level spine. The remaining obstruction is more specific: boundary, projector, domain, and history/no-tail sectors either need parent certificates or source-backed bounds. That is a much tighter problem than the earlier generic “coupling missing” issue.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3925_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3925_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3925_PARENT_CLAUSE_VARIATION_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3925_ADOPTION_VERDICT_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3925_BLOCAL_BOUND_VALUE_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3925_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3925_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3925 - Minimal Parent Clause Variation Audit

Timestamp: `{timestamp}`

- Variation audit result: `{AUDIT_RESULT}`.
- Adoption verdict: `{PARTIAL_ADOPTION}`.
- First bound queue if not certified: `{BOUND_QUEUE}`.
- Status: private core branch can be carried forward; escape/history sectors still block local-GR promotion.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3925 - Minimal Parent Clause Variation Audit"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    variation = variation_rows(timestamp)
    adoption = adoption_rows(timestamp)
    bounds = bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3925_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3925_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3925_02_variation_rows", len(variation) == 13, "variation audit rows emitted"),
        ("VAL3925_03_core_pass", any(row["row_id"] == "VAR3925_12_total" and row["audit_status"] == "CORE_PASS_ESCAPE_PARTIAL" for row in variation), "core-pass escape-partial verdict emitted"),
        ("VAL3925_04_adoption_matrix", len(adoption) == 6, "adoption verdict matrix emitted"),
        ("VAL3925_05_history_not_global", any(row["row_id"] == "ADOPT3925_4_history" and row["verdict"] == "NOT_GLOBAL_ZERO" for row in adoption), "history not globally zero"),
        ("VAL3925_06_bound_queue", len(bounds) == 8, "Blocal bound queue emitted"),
        ("VAL3925_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (variation, adoption, bounds, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3925_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3925_09_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3925_10_spine_written", SPINE_PATH.exists() and "3925 - Minimal Parent Clause Variation Audit" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3925_11_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3925_12_script_compiles", True, "script compiles"),
        ("VAL3925_13_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["variation"], variation_rows(timestamp))
    write_csv(OUTPUTS["adoption"], adoption_rows(timestamp))
    write_csv(OUTPUTS["bound_values"], bound_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3925 validation failed: {failed}")
    print(f"3925 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
