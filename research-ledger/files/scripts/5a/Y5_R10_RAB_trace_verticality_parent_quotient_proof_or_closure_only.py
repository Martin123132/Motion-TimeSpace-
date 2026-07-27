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

DOC = ROOT / "1432-Y5-R10-RAB-trace-verticality-parent-quotient-proof-or-closure-only.md"
BRANCH_ID_FILE = BRANCH_ROOT / "branch_id.csv"
QT_ZERO_STATUS_FILE = BRANCH_ROOT / "coefficients" / "QT_zero_route_status.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1432_SOURCE_REGISTER.csv"
TRACE_VERTICALITY_ATTEMPT = OUT / "P8_Y5_R10_1432_TRACE_VERTICALITY_PROOF_ATTEMPT.csv"
KERNEL_TEST_LEDGER = OUT / "P8_Y5_R10_1432_KERNEL_TEST_LEDGER.csv"
CLOSURE_ONLY_DEMOTION = OUT / "P8_Y5_R10_1432_CLOSURE_ONLY_DEMOTION.csv"
COUNTEREXAMPLE_LEDGER = OUT / "P8_Y5_R10_1432_COUNTEREXAMPLE_LEDGER.csv"
QT_ZERO_STATUS = OUT / "P8_Y5_R10_1432_QT_ZERO_ROUTE_STATUS.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_R10_1432_RUNNER_REFUSAL_STATUS.csv"
CLAIM_GATE = OUT / "P8_Y5_R10_1432_CLAIM_GATE.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1432_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1432_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1432_VALIDATION.csv"


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
        ("SRC1432_0_1431_next", OUT / "P8_Y5_R10_1431_NEXT_TARGET.csv", "NEXT1431_0_1432", "1431 handoff selecting trace verticality proof or closure-only demotion."),
        ("SRC1432_1_1431_validation", OUT / "P8_Y5_BRR545_1431_VALIDATION.csv", "VAL1431_8_overall", "1431 validation summary."),
        ("SRC1432_2_branch_id", BRANCH_ID_FILE, branch, "branch lock row."),
        ("SRC1432_3_1431_premise", OUT / "P8_Y5_R10_1431_QT_ZERO_PREMISE_GATE.csv", "QTP1431_1_trace_verticality", "trace verticality was central unsigned clause."),
        ("SRC1432_4_864_split_lemma", OUT / "P8_Y5_R10_864_LOCAL_GLOBAL_SPLIT_LEMMA.csv", "LGS864_0_conditional_split_lemma", "conditional local/global split lemma."),
        ("SRC1432_5_864_parent_clause", OUT / "P8_Y5_R10_864_PARENT_CLAUSE_CANDIDATE.csv", "PC864_1_trace_vertical_split", "sufficient trace vertical split clause."),
        ("SRC1432_6_873_proof_audit", OUT / "P8_Y5_R10_873_PROOF_CLAUSE_AUDIT.csv", "PC873_1_trace_verticality", "local trace verticality blocker."),
        ("SRC1432_7_626_signature", OUT / "P8_Y5_R10_626_SIGNATURE_LEDGER.csv", "QMS626_1_vertical_kernel", "vertical kernel clause unsigned."),
        ("SRC1432_8_762_stack", OUT / "P8_Y5_R10_762_GEOMETRY_STACK_DESCENT_CONTRACT.csv", "GSD762_5_stack_verdict", "geometry stack still unsigned."),
        ("SRC1432_9_763_marker", OUT / "P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv", "NMS763_6_verdict", "no-marker theorem still unsigned."),
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


def trace_verticality_attempt_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "TVP1432_0_define_parent_readouts",
            "same_parent_branch_id": branch,
            "claim_attempt": "one parent state Phi has q_FLRW(Phi) and q_loc[U](Phi) as compatible quotient readouts",
            "needed_equation": "q_FLRW: Phi -> Q_FLRW and q_loc[U]: Phi -> Q_loc(U)",
            "evidence": "PC864_0_parent_domains writes the sufficient clause",
            "result": "CONDITIONAL_ONLY_NOT_PARENT_DERIVED",
            "proof_gap": "no action-level functor construction or compatibility/inclusion map is supplied",
            "proves_verticality": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVP1432_1_define_trace_generator",
            "same_parent_branch_id": branch,
            "claim_attempt": "v_T is the tangent direction changing Q_trace while holding local quotient data fixed",
            "needed_equation": "Dq_FLRW[v_T] = delta Q_trace != 0 and Dq_loc[U][v_T] = 0",
            "evidence": "PC864_1_trace_vertical_split and LGS864_0 state this as sufficient",
            "result": "DEFINITION_AVAILABLE_AS_CLOSURE_NOT_DERIVED",
            "proof_gap": "the corpus does not derive why the trace endpoint is excluded from every compact local q_loc[U]",
            "proves_verticality": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVP1432_2_kernel_test",
            "same_parent_branch_id": branch,
            "claim_attempt": "v_T belongs to ker(Dq_loc[U]) on the ordinary matter branch",
            "needed_equation": "Dq_loc[U][v_T] = 0 for labs, rods, clocks, sources, and PPN domains",
            "evidence": "PC873_1 marks this as central unsigned clause",
            "result": "KERNEL_MEMBERSHIP_NOT_PROVED",
            "proof_gap": "no parent quotient map is available to differentiate, so the kernel test cannot be evaluated",
            "proves_verticality": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVP1432_3_matter_blindness",
            "same_parent_branch_id": branch,
            "claim_attempt": "ordinary matter only sees Obs_loc(q_loc[U](Phi)) and no Q_trace marker",
            "needed_equation": "S_matter[U]=Sbar[Obs_loc(q_loc[U](Phi)),Psi,theta(q_loc[U])]",
            "evidence": "GSD762_5 and NMS763_6 remain unsigned",
            "result": "MATTER_BLINDNESS_NOT_PARENT_SIGNED",
            "proof_gap": "geometry stack and no-marker constants can still carry Q_trace dependence",
            "proves_verticality": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "TVP1432_4_verdict",
            "same_parent_branch_id": branch,
            "claim_attempt": "prove trace verticality as a theorem",
            "needed_equation": "v_T in ker(Dq_loc[U]) from parent construction, not declaration",
            "evidence": "all TVP1432 rows",
            "result": "TRACE_VERTICALITY_NOT_PROVED_CLOSURE_ONLY_IF_USED",
            "proof_gap": "the split is a useful closure/axiom candidate, not a derivation",
            "proves_verticality": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def kernel_test_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "kernel_test_id": "KT1432_0_object",
            "same_parent_branch_id": branch,
            "test": "q_loc[U] exists as an action-level quotient object",
            "pass_condition": "parent action defines q_loc[U] before matter variation",
            "current_result": "FAIL_OBJECT_NOT_PARENT_CONSTRUCTED",
            "blocks": "cannot evaluate Dq_loc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_test_id": "KT1432_1_tangent",
            "same_parent_branch_id": branch,
            "test": "v_T is a tangent generator in parent configuration space",
            "pass_condition": "v_T has defined action on Phi and Q_trace",
            "current_result": "PARTIAL_FORMAL_GENERATOR_ONLY",
            "blocks": "can state but not compute kernel membership",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_test_id": "KT1432_2_derivative",
            "same_parent_branch_id": branch,
            "test": "Dq_loc[U][v_T] equals zero",
            "pass_condition": "explicit derivative or quotient construction proves zero",
            "current_result": "FAIL_NO_EXPLICIT_DERIVATIVE",
            "blocks": "Q_T zero theorem cannot be promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_test_id": "KT1432_3_uniform_U",
            "same_parent_branch_id": branch,
            "test": "kernel result holds for every compact non-cosmological local arena U",
            "pass_condition": "restriction/sheaf/locality rule excludes Q_trace uniformly",
            "current_result": "FAIL_NO_UNIFORM_LOCALITY_RULE",
            "blocks": "local labs, clocks, and PPN domains may see different residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "kernel_test_id": "KT1432_4_FLRW_visibility",
            "same_parent_branch_id": branch,
            "test": "q_FLRW still sees Q_trace while q_loc does not",
            "pass_condition": "compatible q_FLRW/q_loc readout map from one parent state",
            "current_result": "FAIL_COMPATIBILITY_MAP_MISSING",
            "blocks": "otherwise the split risks becoming patchwork local GR plus separate cosmology",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def closure_only_demotion_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "closure_id": "COD1432_0_if_adopted",
            "same_parent_branch_id": branch,
            "closure_statement": "Declare Dq_FLRW[v_T] != 0 and Dq_loc[U][v_T] = 0 as a parent closure axiom for compact local matter domains",
            "what_it_would_buy": "direct Q_T/m zero route can proceed conditionally through matter descent/no-marker/no-hair",
            "cost": "must be labelled closure/axiom until q_FLRW/q_loc are derived from a parent action",
            "current_status": "AVAILABLE_NOT_ADOPTED",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "COD1432_1_current_decision",
            "same_parent_branch_id": branch,
            "closure_statement": "Do not use trace verticality as theorem credit in 1432",
            "what_it_would_buy": "keeps derivation-first discipline intact",
            "cost": "C_parent and local residual branches remain blocked/open",
            "current_status": "TRACE_VERTICALITY_DEMOTED_TO_CLOSURE_ONLY",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "closure_id": "COD1432_2_public_language",
            "same_parent_branch_id": branch,
            "closure_statement": "If used later, say 'assuming the local/global quotient split' rather than 'deriving local GR'",
            "what_it_would_buy": "honest minimal spine for stress testing",
            "cost": "not a GR/Newton reduction proof",
            "current_status": "LANGUAGE_GUARD",
            "adopted_as_derivation": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def counterexample_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "counterexample_id": "CE1432_0_q_loc_includes_trace",
            "same_parent_branch_id": branch,
            "counterexample": "q_loc[U] explicitly includes a local scalar trace component inherited from Q_trace",
            "effect": "Dq_loc[v_T] != 0",
            "required_exclusion": "parent locality/restriction theorem excluding global trace endpoint from compact local quotient",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CE1432_1_trace_Weyl_frame",
            "same_parent_branch_id": branch,
            "counterexample": "local matter metric carries A_T(Q_trace)^2 g_obs or disformal trace factor",
            "effect": "rods/clocks see Q_trace even if q_loc omits it",
            "required_exclusion": "geometry-stack descent through q_loc plus no representative frame coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CE1432_2_marker_constants",
            "same_parent_branch_id": branch,
            "counterexample": "masses, alpha_EM, binding response, or material labels depend on Q_trace",
            "effect": "WEP/clock residual survives through theta_A derivative",
            "required_exclusion": "no-marker/no-spurion and constant-superselection theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "counterexample_id": "CE1432_3_boundary_hair",
            "same_parent_branch_id": branch,
            "counterexample": "boundary/exact trace current has nonzero local projection or shear/vector hair",
            "effect": "local q_loc force/source residual survives despite kernel declaration",
            "required_exclusion": "boundary no-hair and local projection silence theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def qt_zero_status_rows(branch: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": branch,
            "route": "Q_T_over_m_zero_theorem",
            "trace_verticality_status": "CLOSURE_ONLY_NOT_DERIVED",
            "kernel_test_status": "Dq_loc_vT_ZERO_NOT_COMPUTED",
            "matter_descent_status": "DEPENDENT_PREMISES_OPEN",
            "C_parent_effect": "do_not_set_CP1430_0_trace_charge_to_DERIVED_ZERO",
            "runner_status": "BLOCKED",
            "source_path": str(DOC),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def write_qt_zero_status_file(rows: list[dict[str, Any]]) -> None:
    write_csv(QT_ZERO_STATUS_FILE, rows)


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN1432_0_trace_verticality",
            "target": "v_T in ker(Dq_loc)",
            "input_status": "CLOSURE_ONLY_NOT_DERIVED",
            "runner_status": "REFUSE_KERNEL_ZERO_PROMOTION",
            "score_ready": False,
            "reason": "Dq_loc[v_T]=0 is a sufficient closure clause but no parent quotient construction computes it",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "runner_id": "RUN1432_1_QT_zero",
            "target": "Q_T/m zero theorem",
            "input_status": "TRACE_VERTICALITY_UNSIGNED",
            "runner_status": "REFUSE_QT_ZERO",
            "score_ready": False,
            "reason": "without trace verticality, Q_T/m cannot be set to derived zero",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG1432_0_trace_verticality",
            "claim_component": "v_T in ker(Dq_loc)",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "kernel membership is a closure candidate, not parent-derived",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1432_1_QT_zero",
            "claim_component": "Q_T/m = 0",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "trace verticality is unsigned and matter/no-marker/no-hair debts remain open",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1432_2_C_parent",
            "claim_component": "C_parent zero or numeric coupling",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "CP1430 rows remain placeholder/import-only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1432_3_local_GR",
            "claim_component": "local-GR/Newton reduction",
            "gate_pass": False,
            "claim_allowed": False,
            "reason": "local trace silence is not derived",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1432_0_no_kernel_proof",
            "decision": "do not promote v_T in ker(Dq_loc)",
            "because": "no explicit parent q_loc functor or derivative computation exists",
            "effect": "Q_T zero remains blocked and C_parent cannot be set to derived zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1432_1_closure_only",
            "decision": "record trace verticality as closure-only if used",
            "because": "the sufficient split is mathematically clean but not derived",
            "effect": "future writing must mark the route as assumed local/global quotient split",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1432_2_next",
            "decision": "try parent quotient functor construction next",
            "because": "the only way to promote verticality is to derive q_FLRW and q_loc from one parent state with a compatibility map",
            "effect": "1433 should build or reject the parent quotient functor construction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1432_0_1433",
            "next_target": "1433-Y5-R10-RAB-parent-quotient-functor-construction-or-residual-activation.md",
            "script": "scripts/Y5_R10_RAB_parent_quotient_functor_construction_or_residual_activation.py",
            "objective": "try to construct compatible q_FLRW and q_loc[U] functors from one parent state; if not, activate the residual/source branch for local trace coupling.",
            "include": "parent state category; restriction to compact U; FLRW quotient; compatibility map; kernel derivative; residual activation ledger",
            "exclude": "WEP score; fitted C_parent; local-GR claim; formalization edits; GitHub",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
    closure: list[dict[str, Any]],
    status_rows: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    csvs = [
        SOURCE_REGISTER,
        TRACE_VERTICALITY_ATTEMPT,
        KERNEL_TEST_LEDGER,
        CLOSURE_ONLY_DEMOTION,
        COUNTEREXAMPLE_LEDGER,
        QT_ZERO_STATUS,
        RUNNER_REFUSAL,
        CLAIM_GATE,
        DECISION_LEDGER,
        NEXT_TARGET,
        QT_ZERO_STATUS_FILE,
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
            for key in ("claim_allowed", "valid_for_claim", "valid_prediction_row", "adopted_as_derivation", "proves_verticality"):
                if (row.get(key) or "").strip().lower() == "true":
                    truthy_claim_flags.append(f"{path.name}:{index}:{key}=true")
    sources_ok = all(row["path_exists"] and row["anchor_found"] for row in sources)
    no_verticality_proof = all(str(row.get("proves_verticality")).lower() == "false" for row in attempts)
    closure_not_adopted = all(str(row.get("adopted_as_derivation")).lower() == "false" for row in closure)
    status_written = QT_ZERO_STATUS_FILE.exists() and len(read_csv(QT_ZERO_STATUS_FILE)) == len(status_rows)
    claims_safe = all(str(row.get("claim_allowed")).lower() == "false" for row in claims) and not truthy_claim_flags
    formalization_count = count_formalization_modified_since_start()
    checks = [
        ("VAL1432_0_sources", sources_ok, "all 1432 cited source paths and anchors resolve"),
        ("VAL1432_1_no_verticality_proof", no_verticality_proof, "trace verticality is not promoted"),
        ("VAL1432_2_closure_only", closure_not_adopted, "closure route recorded without adoption as derivation"),
        ("VAL1432_3_QT_status_file", status_written, "QT zero route status file written"),
        ("VAL1432_4_claim_gates", claims_safe, "all claim/valid/adopted/proof flags remain false"),
        ("VAL1432_5_csv_parse", parse_ok, "all generated 1432 CSVs parse cleanly" if parse_ok else ";".join(parse_errors)),
        ("VAL1432_6_formalization_untouched", formalization_count == 0, f"formalization modified-file count since start={formalization_count}"),
        ("VAL1432_7_next_target", True, "1433 handoff written"),
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
            "check_id": "VAL1432_8_overall",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1432 demotes trace verticality to closure-only and keeps Q_T/C_parent/local-GR claims blocked",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(sections: dict[str, list[dict[str, Any]]]) -> None:
    content = "\n\n".join(
        [
            "# 1432 - Trace verticality parent quotient proof or closure-only",
            "**Current verdict:** `v_T in ker(Dq_loc)` is not derived in 1432. The local/global split remains a clean closure candidate, but using it as theorem credit would smuggle the coupling answer.",
            "**Main progress:** the exact kernel test is now explicit: construct `q_loc[U]`, define `v_T`, compute `Dq_loc[U][v_T]`, prove it vanishes uniformly for compact local arenas, and keep `q_FLRW` visibility compatible with the same parent state.",
            "## Source register\n" + md_table(sections["sources"]),
            "## Trace verticality proof attempt\n" + md_table(sections["attempt"]),
            "## Kernel test ledger\n" + md_table(sections["kernel"]),
            "## Closure-only demotion\n" + md_table(sections["closure"]),
            "## Counterexample ledger\n" + md_table(sections["counterexamples"]),
            "## Q_T zero route status\n" + md_table(sections["status"]),
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
    attempts = trace_verticality_attempt_rows(branch)
    kernel = kernel_test_rows(branch)
    closure = closure_only_demotion_rows(branch)
    counterexamples = counterexample_rows(branch)
    status_rows = qt_zero_status_rows(branch)
    write_qt_zero_status_file(status_rows)
    runner = runner_refusal_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(TRACE_VERTICALITY_ATTEMPT, attempts)
    write_csv(KERNEL_TEST_LEDGER, kernel)
    write_csv(CLOSURE_ONLY_DEMOTION, closure)
    write_csv(COUNTEREXAMPLE_LEDGER, counterexamples)
    write_csv(QT_ZERO_STATUS, status_rows)
    write_csv(RUNNER_REFUSAL, runner)
    write_csv(CLAIM_GATE, claims)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)

    validation = validation_rows(sources, attempts, closure, status_rows, claims)
    write_csv(VALIDATION, validation)
    write_doc(
        {
            "sources": sources,
            "attempt": attempts,
            "kernel": kernel,
            "closure": closure,
            "counterexamples": counterexamples,
            "status": status_rows,
            "runner": runner,
            "claims": claims,
            "decisions": decisions,
            "validation": validation,
            "next": next_rows,
        }
    )
    remove_pycache()
    print("Y5_R10_1432_trace_verticality_closure_only_QT_zero_blocked_nonclaim")


if __name__ == "__main__":
    main()
