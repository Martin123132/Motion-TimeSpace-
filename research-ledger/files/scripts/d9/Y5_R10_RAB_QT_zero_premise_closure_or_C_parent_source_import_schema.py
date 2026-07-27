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

DOC = ROOT / "1431-Y5-R10-RAB-QT-zero-premise-closure-or-C-parent-source-import-schema.md"
BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
C_PARENT_FILE = BRANCH_ROOT / "coefficients" / "C_parent.csv"
C_PARENT_IMPORT_SCHEMA_FILE = BRANCH_ROOT / "coefficients" / "C_parent_import_schema.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1431_SOURCE_REGISTER.csv"
QT_ZERO_PREMISE_GATE = OUT / "P8_Y5_R10_1431_QT_ZERO_PREMISE_GATE.csv"
QT_RESIDUAL_DECOMPOSITION = OUT / "P8_Y5_R10_1431_QT_RESIDUAL_DECOMPOSITION.csv"
C_PARENT_IMPORT_SCHEMA = OUT / "P8_Y5_R10_1431_C_PARENT_IMPORT_SCHEMA.csv"
PROMOTION_TESTS = OUT / "P8_Y5_R10_1431_PROMOTION_TESTS.csv"
BRANCH_MATCH_AUDIT = OUT / "P8_Y5_R10_1431_BRANCH_MATCH_AUDIT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1431_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1431_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1431_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1431_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1431_VALIDATION.csv"


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
        ("SRC1431_0_1430_next", OUT / "P8_Y5_R10_1430_NEXT_TARGET.csv", "NEXT1430_0_1431", "1430 handoff selecting Q_T zero premise closure or C_parent import schema."),
        ("SRC1431_1_1430_validation", OUT / "P8_Y5_BRR545_1430_VALIDATION.csv", "VAL1430_8_overall", "1430 validation summary."),
        ("SRC1431_2_branch_id", BRANCH_ID_FILE, branch, "branch lock row."),
        ("SRC1431_3_C_parent", C_PARENT_FILE, "CP1430_6_verdict", "C_parent placeholder/refusal rows."),
        ("SRC1431_4_873_premises", OUT / "P8_Y5_R10_873_PROOF_CLAUSE_AUDIT.csv", "PC873_1_trace_verticality", "trace verticality premise audit."),
        ("SRC1431_5_873_zero", OUT / "P8_Y5_R10_873_LOCAL_TRACE_CHARGE_ZERO_THEOREM.csv", "QTZ873_3_verdict", "chain-rule zero theorem verdict."),
        ("SRC1431_6_864_nohair", OUT / "P8_Y5_R10_864_LOCAL_NOHAIR_CONTRACT.csv", "NH864_3_clock_WEP_markers", "local nohair/marker silence contract."),
        ("SRC1431_7_762_stack", OUT / "P8_Y5_R10_762_GEOMETRY_STACK_DESCENT_CONTRACT.csv", "GSD762_5_stack_verdict", "geometry-stack descent status."),
        ("SRC1431_8_763_spurion", OUT / "P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv", "NMS763_6_verdict", "no-marker/no-spurion theorem status."),
        ("SRC1431_9_626_signature", OUT / "P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv", "QIM626_5_signature_verdict", "quotient-invariant matter action signature status."),
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


def qt_zero_premise_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "premise_id": "QTP1431_0_parent_q_loc",
            "same_parent_branch_id": branch,
            "required_premise": "q_loc[U]: Phi -> Q_loc(U) is parent-owned before ordinary matter variation",
            "source_anchor": "PC873_0_parent_q_loc;QIM626_0_descent_equivalence",
            "current_status": "NOT_PARENT_SIGNED",
            "if_closed": "vertical derivative test becomes well-defined",
            "if_open": "v_T may still be a physical local variable",
            "premise_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "QTP1431_1_trace_verticality",
            "same_parent_branch_id": branch,
            "required_premise": "v_T in ker(Dq_loc[U]) for ordinary labs, sources, rods, clocks, and PPN domains",
            "source_anchor": "PC873_1_trace_verticality",
            "current_status": "CENTRAL_UNSIGNED_CLAUSE",
            "if_closed": "FLRW-visible trace endpoint can be locally matter-blind",
            "if_open": "trace endpoint can become a real local coupling",
            "premise_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "QTP1431_2_geometry_stack_descent",
            "same_parent_branch_id": branch,
            "required_premise": "measure, coframe/metric, connection, and derivative operator all factor through q_loc",
            "source_anchor": "GSD762_5_stack_verdict",
            "current_status": "GEOMETRY_STACK_DESCENT_NOT_PARENT_SIGNED",
            "if_closed": "ordinary matter has no direct v_T geometry derivative",
            "if_open": "coframe, spin, EM, torsion, or derivative couplings can reintroduce Q_T",
            "premise_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "QTP1431_3_no_marker_constants",
            "same_parent_branch_id": branch,
            "required_premise": "theta_A, alpha_EM, masses, binding responses, and material labels carry no v_T/Q_trace marker charge",
            "source_anchor": "NMS763_6_verdict;NH864_3_clock_WEP_markers",
            "current_status": "NO_MARKER_SPURION_THEOREM_NOT_PARENT_SIGNED",
            "if_closed": "species/clock/material charge cannot create WEP leakage",
            "if_open": "Q_T^A/m_A can be species dependent and must be bounded",
            "premise_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "QTP1431_4_boundary_readout_silence",
            "same_parent_branch_id": branch,
            "required_premise": "boundary/exact terms and reduced readout EFT have zero local force/source/clock projection",
            "source_anchor": "NH864_1_boundary_exact_terms;PC873_4_boundary_and_reduced_EFT_silence",
            "current_status": "BOUNDARY_READOUT_SILENCE_OPEN",
            "if_closed": "zero theorem is stable under local integration/readout",
            "if_open": "zero can be an artifact of chosen variables while residual survives",
            "premise_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "premise_id": "QTP1431_5_verdict",
            "same_parent_branch_id": branch,
            "required_premise": "all QTP1431_0..QTP1431_4 close",
            "source_anchor": "QTP1431_0..QTP1431_4",
            "current_status": "QT_ZERO_THEOREM_NOT_CLOSED",
            "if_closed": "C_parent trace-charge branch can be set to zero without fitting",
            "if_open": "C_parent source import schema remains required",
            "premise_closed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def qt_residual_decomposition_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "QTR1431_0_chain_rule",
            "same_parent_branch_id": branch,
            "term": "partial_{v_T} S_A",
            "decomposition": "(delta S_A/dG_matter) Lie_{v_T}G_matter + (partial S_A/partial theta_A) Lie_{v_T}theta_A + boundary/readout terms",
            "zero_condition": "all geometry, marker, and boundary/readout terms vanish",
            "current_status": "IDENTITY_VALID_ZERO_NOT_PROVED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "QTR1431_1_geometry",
            "same_parent_branch_id": branch,
            "term": "(delta S_A/dG_matter) Lie_{v_T}G_matter",
            "decomposition": "measure + coframe/metric + connection + derivative stack",
            "zero_condition": "G_matter(Phi)=Gbar(q_loc(Phi)) up to owned gauge/exact terms",
            "current_status": "OPEN_BY_GSD762",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "QTR1431_2_marker",
            "same_parent_branch_id": branch,
            "term": "(partial S_A/partial theta_A) Lie_{v_T}theta_A",
            "decomposition": "masses, charges, alpha_EM, binding response, species/material labels",
            "zero_condition": "ordinary constants are representation/superselection data with no v_T derivative",
            "current_status": "OPEN_BY_NMS763_NH864",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "QTR1431_3_boundary_readout",
            "same_parent_branch_id": branch,
            "term": "P_loc dB_trace and post-readout EFT terms",
            "decomposition": "edge currents, exact terms, reduced EFT corrections",
            "zero_condition": "local projection silence and no post-readout theorem credit",
            "current_status": "OPEN_BY_NH864_PC873",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "QTR1431_4_Cparent_import_need",
            "same_parent_branch_id": branch,
            "term": "C_parent fallback",
            "decomposition": "if any QTR1431_1..QTR1431_3 survives, source/import C_parent components",
            "zero_condition": "not applicable unless zero theorem closes",
            "current_status": "IMPORT_SCHEMA_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def c_parent_import_schema_rows(branch: str) -> list[dict[str, Any]]:
    required = [
        ("schema_version", "string", "C_PARENT_IMPORT_SCHEMA_1431", "locks parser and interpretation"),
        ("same_parent_branch_id", "string", branch, "must exactly match branch_id.csv"),
        ("coefficient_id", "string", "unique row id", "stable component identity"),
        ("component", "string", "Q_T_over_m|C_T_metric|C_T_source|Z_T|lambda_T|DD_pullback_or_other", "declares the physical slot"),
        ("value", "float_or_DERIVED_ZERO", "numeric value or DERIVED_ZERO", "no MISSING/PENDING/PLACEHOLDER for claim rows"),
        ("uncertainty", "float_or_exact", "uncertainty or exact theorem tag", "required for numeric rows"),
        ("units", "string", "SI or declared natural-unit conversion", "dimension checking"),
        ("sign_convention", "string", "explicit body/order/field sign", "prevents sign flips"),
        ("basis", "string", "MTS parent basis, not DD-only proxy", "prevents ontology swap"),
        ("source_path", "path_or_url_or_doi", "local file, URL, or DOI", "provenance"),
        ("parent_status", "enum", "PARENT_DERIVED|SOURCE_BACKED_NUMERIC|DERIVED_ZERO|EXTERNAL_COMPARATOR_ONLY", "promotion gate"),
        ("zero_certificate_status", "enum", "QT_ZERO_CLOSED|NUMERIC_NONZERO|NOT_ZERO_CERTIFIED", "distinguishes theorem zero from missing"),
        ("valid_for_claim", "boolean", "false until all promotion tests pass", "claim safety"),
        ("claim_allowed", "boolean", "false until full branch scorepack passes", "claim safety"),
    ]
    return [
        {
            "same_parent_branch_id": branch,
            "field": field,
            "type": field_type,
            "required_value_or_policy": policy,
            "purpose": purpose,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for field, field_type, policy, purpose in required
    ]


def write_import_schema_file(rows: list[dict[str, Any]]) -> None:
    write_csv(C_PARENT_IMPORT_SCHEMA_FILE, rows)


def promotion_test_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "test_id": "PROM1431_0_branch_match",
            "same_parent_branch_id": branch,
            "test": "all imported C_parent rows carry the exact branch id",
            "pass_condition": branch,
            "current_result": "SCHEMA_ONLY_NO_IMPORTED_ROWS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "PROM1431_1_no_missing_markers",
            "same_parent_branch_id": branch,
            "test": "claim rows contain no MISSING/PENDING/PLACEHOLDER/NOT_SCOREABLE values",
            "pass_condition": "all required fields concrete",
            "current_result": "FAILED_FOR_EXISTING_C_PARENT_PLACEHOLDERS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "PROM1431_2_zero_or_numeric",
            "same_parent_branch_id": branch,
            "test": "each component is either DERIVED_ZERO with certificate or numeric/source-backed",
            "pass_condition": "QT_ZERO_CLOSED or SOURCE_BACKED_NUMERIC",
            "current_result": "FAILED_ZERO_PREMISES_UNSIGNED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "PROM1431_3_not_DD_only",
            "same_parent_branch_id": branch,
            "test": "DD comparator rows cannot be promoted as MTS coefficients without parent pullback",
            "pass_condition": "basis != DD-only or parent pullback source present",
            "current_result": "GUARD_WRITTEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "test_id": "PROM1431_4_full_scorepack",
            "same_parent_branch_id": branch,
            "test": "C_parent, R_source, R_material, K_CMSM, product convention, and measured-G guard all pass together",
            "pass_condition": "full branch scorepack complete",
            "current_result": "FAILED_SOURCE_MATERIAL_READOUT_STILL_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def branch_match_audit_rows(branch: str) -> list[dict[str, Any]]:
    targets = [
        ("BMA1431_0_branch_id", BRANCH_ID_FILE),
        ("BMA1431_1_C_parent", C_PARENT_FILE),
        ("BMA1431_2_C_parent_import_schema", C_PARENT_IMPORT_SCHEMA_FILE),
    ]
    rows: list[dict[str, Any]] = []
    for audit_id, path in targets:
        parsed = read_csv(path) if path.exists() else []
        values = sorted({row.get("same_parent_branch_id", "") for row in parsed if row.get("same_parent_branch_id")})
        rows.append(
            {
                "audit_id": audit_id,
                "target_path": str(path),
                "file_exists": path.exists(),
                "row_count": len(parsed),
                "branch_values": ";".join(values),
                "result": "PASS" if path.exists() and values == [branch] else "FAIL",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1431_0_QT_zero",
            "target": "Q_T/m zero theorem",
            "input_status": "PREMISES_OPEN",
            "runner_status": "REFUSE_ZERO_PROMOTION",
            "score_ready": False,
            "reason": "q_loc verticality, geometry-stack descent, no-marker constants, and boundary/readout silence remain unsigned",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1431_1_C_parent_import",
            "target": "source-backed C_parent import",
            "input_status": "SCHEMA_READY_NO_SOURCE_ROWS",
            "runner_status": "WAIT_FOR_REAL_IMPORT",
            "score_ready": False,
            "reason": "import schema exists but no numeric/derived-zero source rows have been imported",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1431_0_QT_zero",
            "claim_component": "Q_T/m = 0 theorem",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "conditional chain rule is valid but premises are unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1431_1_C_parent_import_schema",
            "claim_component": "C_parent import schema",
            "gate_pass": True,
            "claim_allowed": False,
            "reason": "schema exists, but schema is not data or theorem",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1431_2_C_parent",
            "claim_component": "branch-locked C_parent",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "existing C_parent rows remain placeholders/refusals",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1431_3_finite_WEP",
            "claim_component": "finite Ti/Pt WEP prediction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "coupling/source/material/readout scorepack incomplete",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1431_4_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "Q_T zero and full local-coupling silence remain unproved",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1431_0_zero_not_closed",
            "decision": "do not promote Q_T/m=0",
            "because": "the chain-rule identity is good, but each parent-signature premise still has open counterchannels",
            "effect": "C_parent remains blocked rather than quietly zeroed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1431_1_import_schema_written",
            "decision": "write strict C_parent import schema",
            "because": "if derivation stalls, the fallback must demand real units/signs/sources rather than loose coefficients",
            "effect": "future imported coupling rows have an exact acceptance contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1431_2_next",
            "decision": "attack the central unsigned premise: v_T in ker(Dq_loc)",
            "because": "without local trace verticality, matter descent cannot kill Q_T",
            "effect": "1432 should either derive trace verticality from the parent quotient or mark the zero route closure-only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1431_0_1432",
            "next_target": "1432-Y5-R10-RAB-trace-verticality-parent-quotient-proof-or-closure-only.md",
            "script": "scripts/Y5_R10_RAB_trace_verticality_parent_quotient_proof_or_closure_only.py",
            "objective": "try to prove v_T belongs to ker(Dq_loc) on the local ordinary-matter branch, or demote the Q_T zero route to closure-only.",
            "include": "parent quotient map; local/FLRW trace split; vertical generator definition; kernel test; ordinary matter branch; counterexample ledger",
            "exclude": "WEP score; C_parent numeric import; fitted coupling; local-GR claim; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    premise: list[dict[str, Any]],
    schema: list[dict[str, Any]],
    branch_audit: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        QT_ZERO_PREMISE_GATE,
        QT_RESIDUAL_DECOMPOSITION,
        C_PARENT_IMPORT_SCHEMA,
        PROMOTION_TESTS,
        BRANCH_MATCH_AUDIT,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        C_PARENT_IMPORT_SCHEMA_FILE,
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
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row", "adopted_as_derivation", "premise_closed"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    premise_not_closed = all(str(row.get("premise_closed")).lower() == "false" for row in premise)
    schema_written = C_PARENT_IMPORT_SCHEMA_FILE.exists() and len(read_csv(C_PARENT_IMPORT_SCHEMA_FILE)) == len(schema)
    branch_match_ok = all(row["result"] == "PASS" for row in branch_audit)
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims) and not truthy_claim_flags
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1431_0_sources", sources_ok, "all 1431 cited source paths and anchors resolve"),
        ("VAL1431_1_QT_zero_not_closed", premise_not_closed, "Q_T zero theorem premises remain explicitly open"),
        ("VAL1431_2_import_schema", schema_written, "C_parent import schema written"),
        ("VAL1431_3_branch_match", branch_match_ok, "branch_id, C_parent, and import schema share one branch id"),
        ("VAL1431_4_claim_gates", claims_safe, "all claim/valid/adopted/premise flags remain false"),
        ("VAL1431_5_csv_parse", parse_ok, "all generated 1431 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1431_6_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1431_7_next_target", True, "1432 handoff written"),
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
            "check_id": "VAL1431_8_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1431 refuses Q_T zero promotion and writes a strict C_parent import schema",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1431 - Q_T zero premise closure or C_parent source import schema",
            "**Current verdict:** the chain-rule shape for `Q_T/m = 0` is still mathematically good, but 1431 cannot close its parent premises. The route remains nonclaim.",
            "**Main progress:** the surviving leakage terms are now explicit, and a strict branch-locked `C_parent_import_schema.csv` exists for any future sourced coupling vector.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Q_T zero premise gate\n" + md_table(sections["premise"]),
            "## Q_T residual decomposition\n" + md_table(sections["residual"]),
            "## C_parent import schema\n" + md_table(sections["schema"]),
            "## Promotion tests\n" + md_table(sections["promotion"]),
            "## Branch match audit\n" + md_table(sections["branch_audit"]),
            "## Runner refusal status\n" + md_table(sections["runner"]),
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
    premise = qt_zero_premise_rows(branch)
    residual = qt_residual_decomposition_rows(branch)
    schema = c_parent_import_schema_rows(branch)
    write_import_schema_file(schema)
    promotion = promotion_test_rows(branch)
    branch_audit = branch_match_audit_rows(branch)
    runner = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(QT_ZERO_PREMISE_GATE, premise)
    write_csv(QT_RESIDUAL_DECOMPOSITION, residual)
    write_csv(C_PARENT_IMPORT_SCHEMA, schema)
    write_csv(PROMOTION_TESTS, promotion)
    write_csv(BRANCH_MATCH_AUDIT, branch_audit)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, premise, schema, branch_audit, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "premise": premise,
            "residual": residual,
            "schema": schema,
            "promotion": promotion,
            "branch_audit": branch_audit,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1431_QT_zero_not_closed_C_parent_import_schema_written_nonclaim")


if __name__ == "__main__":
    main()
