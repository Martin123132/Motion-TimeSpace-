from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STARTED = datetime.now(timezone.utc)
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
BRANCH_ROOT = ROOT / "source-intake" / "microscope" / "branch_locked_wep"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1433-Y5-R10-RAB-parent-quotient-functor-construction-or-residual-activation.md"
BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
RESIDUAL_FILE = BRANCH_ROOT / "residuals" / "local_trace_residual_activation.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1433_SOURCE_REGISTER.csv"
QUOTIENT_FUNCTOR_ATTEMPT = OUT / "P8_Y5_R10_1433_PARENT_QUOTIENT_FUNCTOR_ATTEMPT.csv"
COMPATIBILITY_MAP_AUDIT = OUT / "P8_Y5_R10_1433_COMPATIBILITY_MAP_AUDIT.csv"
RESIDUAL_ACTIVATION_LEDGER = OUT / "P8_Y5_R10_1433_RESIDUAL_ACTIVATION_LEDGER.csv"
LOCAL_TRACE_RESIDUAL_SCHEMA = OUT / "P8_Y5_R10_1433_LOCAL_TRACE_RESIDUAL_SCHEMA.csv"
RUNNER_STATUS = OUT / "P8_Y5_R10_1433_RUNNER_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1433_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1433_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1433_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1433_VALIDATION.csv"


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
        ("SRC1433_0_1432_next", OUT / "P8_Y5_R10_1432_NEXT_TARGET.csv", "NEXT1432_0_1433", "1432 handoff selecting parent quotient functor construction."),
        ("SRC1433_1_1432_validation", OUT / "P8_Y5_BRR545_1432_VALIDATION.csv", "VAL1432_8_overall", "1432 validation summary."),
        ("SRC1433_2_branch_id", BRANCH_ID_FILE, branch, "branch lock row."),
        ("SRC1433_3_1432_status", BRANCH_ROOT / "coefficients" / "QT_zero_route_status.csv", "CLOSURE_ONLY_NOT_DERIVED", "Q_T zero route closure-only status."),
        ("SRC1433_4_407_parent_sketch", ROOT / "407-primitive-relational-quotient-action-sketch.md", "S_matter_quotient_functor", "primitive relational quotient action sketch."),
        ("SRC1433_5_410_functor_attempt", ROOT / "410-quotient-matter-functor-theorem-attempt.md", "parent quotient object", "quotient-matter functor theorem attempt."),
        ("SRC1433_6_626_signature", OUT / "P8_Y5_R10_626_SIGNATURE_LEDGER.csv", "QMS626_0_q_object", "q object and vertical kernel remain unsigned."),
        ("SRC1433_7_760_descent_gate", OUT / "P8_Y5_R10_760_DESCENT_SIGNATURE_GATE.csv", "DSG760_1_vertical_kernel", "local vertical kernel descent gate."),
        ("SRC1433_8_864_split", OUT / "P8_Y5_R10_864_PARENT_CLAUSE_CANDIDATE.csv", "PC864_5_total_verdict", "local/global split not promoted."),
        ("SRC1433_9_1431_import_schema", BRANCH_ROOT / "coefficients" / "C_parent_import_schema.csv", "zero_certificate_status", "fallback C_parent import schema."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchor, role in specs:
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "anchor": anchor,
                "anchor_found": text_has(path, anchor),
                "role": role,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def quotient_functor_attempt_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "QFC1433_0_parent_category",
            "same_parent_branch_id": branch,
            "construction_target": "parent configuration category C_parent with objects Phi and morphisms gauge/relational equivalences",
            "current_evidence": "407 sketches relational_MTS_state and S_relational_MTS",
            "result": "SKETCH_ONLY",
            "gap": "no formal category, equivalence relation, or action-level quotient universal property",
            "constructed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QFC1433_1_local_restriction",
            "same_parent_branch_id": branch,
            "construction_target": "restriction functor Res_U: C_parent -> C_local(U) for compact non-cosmological U",
            "current_evidence": "864 requires q_loc[U] but does not derive it",
            "result": "NOT_CONSTRUCTED",
            "gap": "no locality/sheaf rule proving global boundary trace data is excluded from every compact U",
            "constructed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QFC1433_2_FLRW_quotient",
            "same_parent_branch_id": branch,
            "construction_target": "q_FLRW that retains Q_trace and endpoint Ward charge",
            "current_evidence": "863/864 make Q_trace FLRW-visible as a sufficient clause",
            "result": "CONDITIONAL_READOUT_ONLY",
            "gap": "endpoint current, Qstar, stationarity, and charge unit are not parent derived",
            "constructed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QFC1433_3_local_quotient",
            "same_parent_branch_id": branch,
            "construction_target": "q_loc[U] that removes v_T and feeds ordinary matter geometry",
            "current_evidence": "626/760 state q object and vertical kernel gates",
            "result": "CONTRACT_ONLY",
            "gap": "q_loc is not supplied as a differentiable map with a kernel",
            "constructed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QFC1433_4_compatibility",
            "same_parent_branch_id": branch,
            "construction_target": "compatibility map showing q_FLRW and q_loc are readouts of one parent state, not separate patches",
            "current_evidence": "LGS864_3 guardrail",
            "result": "MISSING_COMPATIBILITY_MAP",
            "gap": "no inclusion/restriction/natural-transformation diagram is signed",
            "constructed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "QFC1433_5_verdict",
            "same_parent_branch_id": branch,
            "construction_target": "derive v_T in ker(Dq_loc) from constructed quotient functors",
            "current_evidence": "all QFC1433 rows",
            "result": "PARENT_QUOTIENT_FUNCTOR_NOT_CONSTRUCTED",
            "gap": "residual/source branch must activate until the functor pair exists",
            "constructed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def compatibility_audit_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CMA1433_0_one_parent_state",
            "same_parent_branch_id": branch,
            "compatibility_requirement": "q_FLRW and q_loc[U] are both functorial readouts of the same Phi",
            "current_status": "NOT_SIGNED",
            "if_missing": "model can become GR-local plus separate cosmology patch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA1433_1_restriction_naturality",
            "same_parent_branch_id": branch,
            "compatibility_requirement": "local restrictions commute with quotient/readout maps on overlaps",
            "current_status": "NOT_DEFINED",
            "if_missing": "different local labs may not share the same q_loc kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA1433_2_trace_boundary_cokernel",
            "same_parent_branch_id": branch,
            "compatibility_requirement": "Q_trace lies in the FLRW/boundary cokernel of compact local restriction",
            "current_status": "NOT_PROVED",
            "if_missing": "Dq_loc[v_T] can be nonzero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA1433_3_matter_functor",
            "same_parent_branch_id": branch,
            "compatibility_requirement": "ordinary matter functor factors through q_loc[U] after restriction",
            "current_status": "SUFFICIENT_AXIOM_NOT_PARENT_DERIVED",
            "if_missing": "matter can still see representative or trace marker data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def residual_activation_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "activation_id": "LTRA1433_0_trace_residual",
            "residual_branch": "local_trace_coupling",
            "activation_reason": "q_FLRW/q_loc functor pair and Dq_loc[v_T]=0 are not parent-derived",
            "active_inputs_needed": "C_parent; R_source; R_material; K_CMSM; eta_product_convention; measured_G_guard; C_parent_import_schema",
            "affected_arenas": "R10;WEP_MICROSCOPE;PPN;clocks;orbital;Newton_source_normalization",
            "runner_status": "RESIDUAL_ACTIVE_NONCLAIM",
            "source_path": str(DOC),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": branch,
            "activation_id": "LTRA1433_1_zero_route",
            "residual_branch": "Q_T_zero_theorem",
            "activation_reason": "zero route is closure-only until parent quotient functors exist",
            "active_inputs_needed": "parent q_loc; v_T kernel derivative; matter-stack descent; no-marker constants; no-hair",
            "affected_arenas": "theorem_zero_path",
            "runner_status": "BLOCKED_PENDING_PARENT_FUNCTOR",
            "source_path": str(DOC),
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def write_residual_file(rows: list[dict[str, Any]]) -> None:
    write_csv(RESIDUAL_FILE, rows)


def local_trace_residual_schema_rows(branch: str) -> list[dict[str, Any]]:
    fields = [
        ("same_parent_branch_id", branch, "branch matching"),
        ("residual_component", "trace_scalar|coframe_pullback|boundary_hair|marker_constant|source_normalization", "component identity"),
        ("coefficient_symbol", "C_T|Q_T_over_m|B_T|theta_T|mu_T", "coefficient slot"),
        ("value_or_bound", "numeric|DERIVED_ZERO|MISSING", "source-ready value field"),
        ("units", "SI_or_declared_natural_units", "dimensional check"),
        ("projection_matrix", "P_R10|P_WEP|P_PPN|P_clock|P_orbital", "arena projection"),
        ("source_path", "local path, URL, DOI, or theorem certificate", "provenance"),
        ("parent_status", "PARENT_DERIVED|SOURCE_BACKED|CLOSURE_ONLY|MISSING", "promotion status"),
        ("valid_for_claim", "false until complete", "claim safety"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "schema_field": field,
            "required_value_or_policy": policy,
            "purpose": purpose,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for field, policy, purpose in fields
    ]


def runner_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1433_0_quotient_functor",
            "target": "parent q_FLRW/q_loc functor pair",
            "input_status": "NOT_CONSTRUCTED",
            "runner_status": "REFUSE_VERTICALITY_PROMOTION",
            "score_ready": False,
            "reason": "no parent category/restriction/compatibility map with computable Dq_loc kernel",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1433_1_residual_branch",
            "target": "local trace residual source branch",
            "input_status": "ACTIVATED_SCHEMA_ONLY",
            "runner_status": "WAIT_FOR_SOURCE_ROWS",
            "score_ready": False,
            "reason": "residual branch is active but not numerically scoreable",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1433_0_parent_functors",
            "claim_component": "q_FLRW/q_loc parent functor construction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "construction remains sketch/contract only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1433_1_trace_verticality",
            "claim_component": "v_T in ker(Dq_loc)",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "no computable Dq_loc kernel",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1433_2_residual_branch",
            "claim_component": "local trace residual branch",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "branch activation is bookkeeping, not evidence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1433_3_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "local trace residuals remain active",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1433_0_functor_not_constructed",
            "decision": "do not promote the quotient functor construction",
            "because": "407/410 provide good theorem targets but no parent functor pair or compatibility map",
            "effect": "trace verticality and Q_T zero remain blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1433_1_residual_active",
            "decision": "activate local trace residual/source branch",
            "because": "once the zero theorem is closure-only, local trace coupling must be carried as a residual until bounded or derived zero",
            "effect": "future work has a residual schema instead of a hidden zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1433_2_next",
            "decision": "build branch-locked local trace residual source pack next",
            "because": "the derivation route is blocked at the functor level, so source-ready rows are the honest fallback",
            "effect": "1434 should define residual components and arena projections without scoring claims",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1433_0_1434",
            "next_target": "1434-Y5-R10-RAB-local-trace-residual-source-pack-schema-and-bound-map.md",
            "script": "scripts/Y5_R10_RAB_local_trace_residual_source_pack_schema_and_bound_map.py",
            "objective": "build a branch-locked local trace residual source pack schema mapping active residual components to R10, WEP, PPN, clocks, orbital, and Newton/source-normalization tests.",
            "include": "residual components; projection matrices; required bound/source paths; branch-id checks; refusal runner",
            "exclude": "numeric claim scoring; fitted coupling; local-GR claim; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        QUOTIENT_FUNCTOR_ATTEMPT,
        COMPATIBILITY_MAP_AUDIT,
        RESIDUAL_ACTIVATION_LEDGER,
        LOCAL_TRACE_RESIDUAL_SCHEMA,
        RUNNER_STATUS,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        RESIDUAL_FILE,
    ]
    parse_ok = True
    parse_errors: list[str] = []
    truthy_claim_flags: list[str] = []
    for path in csvs:
        try:
            rows = read_csv(path)
        except Exception as exc:
            parse_ok = False
            parse_errors.append(f"{path.name}:{type(exc).__name__}")
            continue
        for index, row in enumerate(rows, start=2):
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row", "constructed"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    functor_not_constructed = all(str(row.get("constructed")).lower() == "false" for row in attempts)
    residual_file_written = RESIDUAL_FILE.exists() and len(read_csv(RESIDUAL_FILE)) == len(residuals)
    residual_active = any(row["runner_status"] == "RESIDUAL_ACTIVE_NONCLAIM" for row in residuals)
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims) and not truthy_claim_flags
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1433_0_sources", sources_ok, "all 1433 cited source paths and anchors resolve"),
        ("VAL1433_1_functor_not_constructed", functor_not_constructed, "parent quotient functor pair is not promoted"),
        ("VAL1433_2_residual_file", residual_file_written and residual_active, "local trace residual activation file written"),
        ("VAL1433_3_claim_gates", claims_safe, "all claim/valid/constructed flags remain false except nonclaim gate_pass bookkeeping"),
        ("VAL1433_4_csv_parse", parse_ok, "all generated 1433 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1433_5_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1433_6_next_target", True, "1434 handoff written"),
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
            "check_id": "VAL1433_7_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1433 fails to construct parent quotient functors and activates the local trace residual branch as nonclaim",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1433 - Parent quotient functor construction or residual activation",
            "**Current verdict:** compatible `q_FLRW` and `q_loc[U]` functors are not constructed in 1433. The quotient language is a strong theorem target, but still not a parent-derived mechanism.",
            "**Main progress:** the local trace residual branch is now explicitly active as a nonclaim fallback. This prevents the theory from silently using `v_T in ker(Dq_loc)` as a hidden axiom.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Parent quotient functor attempt\n" + md_table(sections["attempt"]),
            "## Compatibility map audit\n" + md_table(sections["compatibility"]),
            "## Residual activation ledger\n" + md_table(sections["residuals"]),
            "## Local trace residual schema\n" + md_table(sections["schema"]),
            "## Runner status\n" + md_table(sections["runner"]),
            "## Claim gates\n" + md_table(sections["claims"]),
            "## Decision ledger\n" + md_table(sections["decisions"]),
            "## Validation\n" + md_table(sections["validation"]),
            "## Next target\n" + md_table(sections["next"]),
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    branch = branch_id()
    sources = source_register_rows(branch)
    attempts = quotient_functor_attempt_rows(branch)
    compatibility = compatibility_audit_rows(branch)
    residuals = residual_activation_rows(branch)
    write_residual_file(residuals)
    schema = local_trace_residual_schema_rows(branch)
    runner = runner_status_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(QUOTIENT_FUNCTOR_ATTEMPT, attempts)
    write_csv(COMPATIBILITY_MAP_AUDIT, compatibility)
    write_csv(RESIDUAL_ACTIVATION_LEDGER, residuals)
    write_csv(LOCAL_TRACE_RESIDUAL_SCHEMA, schema)
    write_csv(RUNNER_STATUS, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, attempts, residuals, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "attempt": attempts,
            "compatibility": compatibility,
            "residuals": residuals,
            "schema": schema,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1433_parent_quotient_not_constructed_local_trace_residual_active_nonclaim")


if __name__ == "__main__":
    main()
