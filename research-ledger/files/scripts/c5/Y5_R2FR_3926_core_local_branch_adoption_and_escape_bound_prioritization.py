from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3926"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3926-Y5-R2FR-core-local-branch-adoption-and-escape-bound-prioritization.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3926_SOURCE_REGISTER.csv",
    "adoption": SRC / "P8_Y5_R2FR_3926_CORE_LOCAL_BRANCH_ADOPTION_RECORD.csv",
    "priority": SRC / "P8_Y5_R2FR_3926_ESCAPE_BOUND_PRIORITY_MATRIX.csv",
    "certificate": SRC / "P8_Y5_R2FR_3926_CERTIFICATE_OR_BOUND_ACTION_QUEUE.csv",
    "decision": SRC / "P8_Y5_R2FR_3926_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3926_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3926_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3926_VALIDATION.csv",
}

CORE_ADOPTION = (
    "PRIVATE_CORE_LOCAL_BRANCH_ADOPTED_FOR_WORKBENCH: EH/source/Y/R11/G0 variation core may be used as the local branch spine, "
    "but boundary/projector/domain/history remain theorem-or-bound gates and no public local-GR claim is allowed."
)
ESCAPE_FIRST = (
    "B_escape = |Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi + B_deriv + epsilon_domain_projector_abs"
)
PRIORITY_RULE = (
    "Prioritize components that feed multiple arenas and cannot be calibrated away: projector/domain stress, boundary/harmonic multipoles, "
    "history/nonlocal tails, time/radial/source derivative hair, then residual gamma/beta scalar coefficients."
)
NEXT_DOC = "3927-Y5-R2FR-Bescape-component-bound-pack-projector-domain-boundary-history.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3927_Bescape_component_bound_pack_projector_domain_boundary_history.py"


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
        ("SRC3926_00_next", SRC / "P8_Y5_R2FR_3925_NEXT_TARGET.csv", "NEXT3925_0", "3925 selected core adoption and escape prioritization"),
        ("SRC3926_01_variation_total", SRC / "P8_Y5_R2FR_3925_PARENT_CLAUSE_VARIATION_AUDIT.csv", "VAR3925_12_total", "3925 core-pass escape-partial verdict"),
        ("SRC3926_02_core", SRC / "P8_Y5_R2FR_3925_ADOPTION_VERDICT_MATRIX.csv", "ADOPT3925_0_core", "core branch adoption row"),
        ("SRC3926_03_verdict", SRC / "P8_Y5_R2FR_3925_ADOPTION_VERDICT_MATRIX.csv", "ADOPT3925_5_verdict", "3925 adoption verdict"),
        ("SRC3926_04_boundary", SRC / "P8_Y5_R2FR_3925_ADOPTION_VERDICT_MATRIX.csv", "ADOPT3925_1_boundary", "boundary partial row"),
        ("SRC3926_05_projector", SRC / "P8_Y5_R2FR_3925_ADOPTION_VERDICT_MATRIX.csv", "ADOPT3925_2_projector", "projector partial row"),
        ("SRC3926_06_domain", SRC / "P8_Y5_R2FR_3925_ADOPTION_VERDICT_MATRIX.csv", "ADOPT3925_3_domain", "domain partial row"),
        ("SRC3926_07_history", SRC / "P8_Y5_R2FR_3925_ADOPTION_VERDICT_MATRIX.csv", "ADOPT3925_4_history", "history not global zero row"),
        ("SRC3926_08_bound_queue", SRC / "P8_Y5_R2FR_3925_BLOCAL_BOUND_VALUE_QUEUE.csv", "BQ3925_0_escape", "escape first bound"),
        ("SRC3926_09_total_bound", SRC / "P8_Y5_R2FR_3925_BLOCAL_BOUND_VALUE_QUEUE.csv", "BQ3925_7_total", "B_local total queue"),
        ("SRC3926_10_clause", SRC / "P8_Y5_R2FR_3924_MINIMAL_PARENT_ACTION_SIGNATURE_CLAUSE.csv", "CLA3924_11_effect", "3924 adoption effect"),
        ("SRC3926_11_coverage_history", SRC / "P8_Y5_R2FR_3924_SIGNATURE_TO_THEOREM_COVERAGE.csv", "COV3924_11_history", "history partial coverage"),
        ("SRC3926_12_escape_total", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_9_total", "B_escape formula"),
        ("SRC3926_13_escape_map", SRC / "P8_Y5_R2FR_3922_ESCAPE_TO_PPN_ORBITAL_MAP.csv", "MAP3922_7_Gdot", "escape to Gdot map"),
        ("SRC3926_14_domain_bound", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv", "DPOB3431_4_total_domain_projector", "domain projector bound pack"),
        ("SRC3926_15_boundary_cert", SRC / "P8_Y5_R2FR_3892_BOUNDARY_TOPOLOGICAL_NOFLUX_CERTIFICATE.csv", "BC3892_4_verdict", "boundary certificate unsigned"),
        ("SRC3926_16_projector_cert", SRC / "P8_Y5_R2FR_3892_PROJECTOR_ABSOLUTE_TOPOLOGICAL_CERTIFICATE.csv", "PC3892_4_verdict", "projector certificate unsigned"),
        ("SRC3926_17_history_law", SRC / "P8_Y5_R2FR_3895_MEMORY_SUPPRESSION_LAW.csv", "LAW3895_3_history_decay", "history suppression law"),
        ("SRC3926_18_validation", SRC / "P8_Y5_BRR545_3925_VALIDATION.csv", "VAL3925_13_no_pycache", "3925 validation handoff"),
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


def adoption_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CORE3926_0_status", "core branch status", CORE_ADOPTION, "carry forward as private local branch spine", "PRIVATE_ADOPTION_NOT_PUBLIC_CLAIM"),
        ("CORE3926_1_signed_core", "signed core sectors", "EH public metric; same-frame Hilbert/Maxwell source; quadratic Y vacuum; double-zero R11; G0 coupling owner", "variation audit passed inside candidate branch", "PRIVATE_CORE_BRANCH"),
        ("CORE3926_2_not_signed", "not signed globally", "boundary certificate; projector certificate; fixed q-basic domain; no incoming history/nonlocal tail", "remain theorem-or-bound gates", "ESCAPE_GATES_ACTIVE"),
        ("CORE3926_3_allowed_use", "allowed internal use", "Use core branch when deriving local GR/Newton/Maxwell consequences, but attach B_escape/B_local to every local-GR promotion statement.", "prevents re-litigating signed core while preserving honesty", "INTERNAL_WORKBENCH_RULE"),
        ("CORE3926_4_forbidden_use", "forbidden promotion", "Do not claim local GR, PPN pass, or source-calibration pass until escape gates are signed or bounded.", "no public/local-GR promotion", "NO_PROMOTION_GUARD"),
    ]
    return [
        {
            "row_id": row_id,
            "item": item,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, item, statement, meaning, status in data
    ]


def priority_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PRI3926_0_projector_domain", 1, "epsilon_domain_projector_abs", "projector/domain stress", "feeds Xi_N, alpha_i, xi, zeta_i, source normalization", "zero via fixed topological/readout-only projector or bound DPOB3431 components"),
        ("PRI3926_1_boundary_harmonic", 2, "B_harmonic_boundary + P00_boundary", "boundary/harmonic multipoles", "feeds Xi_N, ephemeris, xi, alpha3/Gdot through boundary flux", "zero via boundary certificate or bound boundary amplitudes"),
        ("PRI3926_2_history_nonlocal", 3, "P00_history + P00_nonlocal", "history/nonlocal tail", "feeds Xi_N and time/radial drift; not globally zero", "local reset/no-tail certificate or 3895 suppression-law values"),
        ("PRI3926_3_derivative_hair", 4, "B_deriv", "time/radial/source/frame derivative hair", "feeds Gdot, WEP/source dependence, inverse-square residuals", "derive derivative silence or fill derivative bounds"),
        ("PRI3926_4_beta_common", 5, "Delta_sq", "common-mode square-law error", "feeds beta after Xi_N survives", "EH one-metric square law or numeric xi_1/xi_2"),
        ("PRI3926_5_gamma_STF", 6, "P_TF/R11 slip", "STF anisotropic leakage", "feeds gamma; lower priority if core/DZ retained", "derive zero or fill 3918 bound inputs"),
        ("PRI3926_6_total", 7, "B_local", "absolute local residual", "final no-cancellation local-GR gate", "sum all nonzero/unbounded components"),
    ]
    return [
        {
            "row_id": row_id,
            "priority_rank": rank,
            "target": target,
            "component": component,
            "why_priority": why,
            "zero_or_bound_route": route,
            "numeric_value": "",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, rank, target, component, why, route in data
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("ACT3926_0_projector", "attempt certificate first", "prove S_proj is readout-only/topological and source-equal, or fill epsilon_domain_projector_abs", "NEXT_THEOREM_OR_BOUND"),
        ("ACT3926_1_domain", "attempt certificate first", "prove q-basic fixed domain/no moving support, or fill DPOB3431 domain-motion/selector terms", "NEXT_THEOREM_OR_BOUND"),
        ("ACT3926_2_boundary", "attempt certificate first", "prove scalar/topological fixed boundary no-flux/no shear, or fill P00_boundary/B_harmonic_boundary", "NEXT_THEOREM_OR_BOUND"),
        ("ACT3926_3_history", "bound likely first", "no incoming history is local-branch-specific; fill suppression parameters gamma_mem, Delta t, lambda_gap, source norm unless reset theorem exists", "BOUND_FIRST_UNLESS_RESET_SIGNED"),
        ("ACT3926_4_derivatives", "bound likely first", "fill partial_t xi_1, partial_r xi_1, Delta_AB xi_1, delta_frame xi_1 or prove derivative silence", "BOUND_FIRST"),
        ("ACT3926_5_score", "do not score yet", "B_local cannot be scored until at least B_escape component values or theorem-zero certificates exist", "SCORE_BLOCKED_VALUES_MISSING"),
    ]
    return [
        {
            "row_id": row_id,
            "action_type": action_type,
            "action": action,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, action_type, action, status in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3926_0_adopt",
            "decision": "core local branch is adopted privately for continued derivations",
            "formula": CORE_ADOPTION,
            "claim_status": "PRIVATE_CORE_ONLY_NO_LOCAL_GR_PROMOTION",
            "next_action": "focus on escape/history certification or bounds",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3926_1_priority",
            "decision": "escape/history sector is first bound/certificate priority",
            "formula": PRIORITY_RULE,
            "claim_status": "NONCLAIM_PRIORITIZATION",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3926_2_blocker",
            "decision": "local-GR promotion remains blocked by B_escape/B_local values or certificates",
            "formula": ESCAPE_FIRST,
            "claim_status": "LOCAL_GR_STILL_UNPROMOTED",
            "next_action": "build B_escape component bound pack",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3926_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "build the B_escape component bound pack for projector/domain, boundary/harmonic, history/nonlocal and derivative-hair terms",
            "why_this_next": "3926 adopts the core privately and shows B_escape is the highest-leverage remaining obstruction to local-GR promotion",
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
            "summary": "core local branch adopted privately; B_escape prioritized as first theorem-or-bound obstruction",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3926 - Core Local Branch Adoption and Escape Bound Prioritization

Timestamp: `{timestamp}`

## Result

Core adoption record:

`{CORE_ADOPTION}`.

First obstruction:

`{ESCAPE_FIRST}`.

Priority rule:

`{PRIORITY_RULE}`.

## Meaning

The core branch is no longer the fog. Internally, we can use the EH/source/Y/R11/G0 core as the private local branch spine. The honest obstruction is now the escape sector: projector/domain stress, boundary/harmonic multipoles, history/nonlocal tails, and derivative hair. Those must be certified or bounded before any local-GR promotion.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3926_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3926_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3926_CORE_LOCAL_BRANCH_ADOPTION_RECORD.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3926_ESCAPE_BOUND_PRIORITY_MATRIX.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3926_CERTIFICATE_OR_BOUND_ACTION_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3926_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3926_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3926 - Core Local Branch Adoption and Escape Bound Priority

Timestamp: `{timestamp}`

- Core adoption record: `{CORE_ADOPTION}`.
- First obstruction: `{ESCAPE_FIRST}`.
- Priority rule: `{PRIORITY_RULE}`.
- Status: private core branch carried forward; escape/history sector blocks local-GR promotion.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3926 - Core Local Branch Adoption and Escape Bound Priority"
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
    adoption = adoption_rows(timestamp)
    priority = priority_rows(timestamp)
    certificate = certificate_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3926_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3926_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3926_02_adoption_record", any(row["row_id"] == "CORE3926_0_status" for row in adoption), "core adoption record emitted"),
        ("VAL3926_03_no_promotion", any(row["row_id"] == "CORE3926_4_forbidden_use" for row in adoption), "no-promotion guard emitted"),
        ("VAL3926_04_priority_matrix", len(priority) == 7, "escape priority matrix emitted"),
        ("VAL3926_05_projector_first", priority[0]["target"] == "epsilon_domain_projector_abs", "projector/domain prioritized first"),
        ("VAL3926_06_action_queue", len(certificate) == 6, "certificate-or-bound action queue emitted"),
        ("VAL3926_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (adoption, priority, certificate, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3926_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3926_09_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3926_10_spine_written", SPINE_PATH.exists() and "3926 - Core Local Branch Adoption and Escape Bound Priority" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3926_11_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3926_12_script_compiles", True, "script compiles"),
        ("VAL3926_13_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["adoption"], adoption_rows(timestamp))
    write_csv(OUTPUTS["priority"], priority_rows(timestamp))
    write_csv(OUTPUTS["certificate"], certificate_rows(timestamp))
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
        raise SystemExit(f"3926 validation failed: {failed}")
    print(f"3926 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
