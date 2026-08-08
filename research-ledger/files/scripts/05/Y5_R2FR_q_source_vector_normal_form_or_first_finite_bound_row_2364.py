from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_Q_SOURCE_VECTOR_NORMAL_FORM_OR_FIRST_FINITE_BOUND_ROW_2364"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2364-Y5-R2FR-q-source-vector-normal-form-or-first-finite-bound-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def rel(path: Path) -> str:
    try:
        return path.relative_to(POST_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return path.exists() and needle in path.read_text(encoding="utf-8", errors="replace")


def no_claim(extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {
        "parent_signed": "false",
        "theorem_zero": "false",
        "numeric_value_present": "false",
        "source_backed": "false",
        "operator_domain_ready": "false",
        "projection_ready": "false",
        "score_ready": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2364_2363_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2363_NEXT_TARGET.csv", "NEXT2363_0_selected", "2363 selects q source-vector normal form"),
        ("SRC2364_2363_validation", "source-intake/mts_residuals/P8_Y5_BRR545_2363_VALIDATION.csv", "VAL2363_OVERALL", "prior checkpoint validation"),
        ("SRC2364_2300_q_euler", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2300_Q_EULER_SOURCE_VECTOR_NORMAL_FORM.csv", "QEUL2300_0_q_equation", "full q Euler/source-vector normal form"),
        ("SRC2364_2300_residuals", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2300_Q_RESIDUAL_ACQUISITION_ROWS.csv", "QRES2300_0_BqWeyl", "q residual acquisition rows"),
        ("SRC2364_2301_firstclass", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2301_Q_FIRSTCLASS_REMOVAL_ATTEMPT.csv", "QFC2301_6_verdict", "first-class removal remains unsigned"),
        ("SRC2364_2301_ricci_weyl", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2301_Q_RICCI_WEYL_SPLIT_ATTEMPT.csv", "QRWS2301_2_Weyl_not_silent", "Weyl survives local exterior vacuum"),
        ("SRC2364_2301_curv_rows", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2301_Q_CURVATURE_RESIDUAL_ACQUISITION_ROWS.csv", "QCURV2301_0_BqWeyl", "BqWeyl curvature residual acquisition row"),
        ("SRC2364_2301_vacuum_gate", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2301_Q_LOCAL_VACUUM_SOURCE_SILENCE_GATE.csv", "QLVS2301_4_verdict", "local vacuum source silence fails current claim"),
        ("SRC2364_2302_bqweyl_zero", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2302_BQWEYL_INDEX_ZERO_THEOREM_GATE.csv", "BQWZ2302_6_verdict", "conditional BqWeyl index theorem not activated"),
        ("SRC2364_2302_qrep", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2302_Q_REPRESENTATION_CERTIFICATE_ATTEMPT.csv", "QRC2302_7_verdict", "q representation certificate fails current claim"),
        ("SRC2364_2303_qfield", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2303_Q_FIELD_CONTENT_CERTIFICATE_SOURCE_HUNT.csv", "QFCH2303_6_verdict", "q field-content source hunt negative"),
        ("SRC2364_2303_nospurion", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2303_Q_NO_SPURION_CERTIFICATE_SOURCE_HUNT.csv", "NSH2303_5_verdict", "no-spurion certificate not signed"),
        ("SRC2364_2303_bound_req", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2303_BQWEYL_LOCAL_BOUND_ACQUISITION_REQUIREMENTS.csv", "BQA2303_1_parent_coefficient", "BqWeyl local bound acquisition requirements"),
        ("SRC2364_2303_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2303_NEXT_TARGET.csv", "NEXT2303_0_primary", "prior BqWeyl next target"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, source_path, needle, role in sources:
        path = POST_ROOT / source_path
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "source_path": source_path,
                "needle": needle,
                "role": role,
                "path_exists": str(path.exists()).lower(),
                "needle_found": str(contains(path, needle)).lower(),
                "valid_for_claim": "false",
            }
        )
    return rows


def q_slot_normal_form() -> list[dict[str, object]]:
    rows = [
        (
            "SLOT2364_0_q_euler",
            "full q Euler/source-vector normal form",
            "E_q = L_q q + B_qRic R_Ricci + B_qW C_Weyl + C_qT T_H + epsilon_q_source sigma_source + Q_q_body delta_body + Pi_q delta_boundary + tail_q = 0",
            "NORMAL_FORM_ACCEPTED_NONCLAIM",
            "all source-looking q channels are explicit, not hidden inside q_R",
        ),
        (
            "SLOT2364_1_firstclass_escape",
            "first-class/constraint removal route",
            "q is absent after reduction only if Omega, generator, brackets, degree count, matter descent, and boundary neutrality close together",
            "EXACT_ROUTE_UNSIGNED",
            "would remove the q pole/source slots, but 2301/2302 do not sign it",
        ),
        (
            "SLOT2364_2_operator_block",
            "LHS/operator-owned route",
            "[E_GR,E_q]^T has L_GR, L_q, and B_qRic blocks; B_qRic can be operator-owned only after Schur/diagonalization/domain positivity",
            "OPERATOR_ROUTE_OPEN_UNSIGNED",
            "Ricci mixing is not automatically a residual, but it cannot be used as a local-GR proof yet",
        ),
        (
            "SLOT2364_3_absolute_residual",
            "absolute residual vector",
            "J_q_res = B_qW C_Weyl + C_qT T_H + epsilon_q_source sigma_source + Q_q_body delta_body + Pi_q delta_boundary + tail_q",
            "RESIDUAL_VECTOR_LOCKED",
            "no sign cancellation is allowed; every component must be theorem-zero or finite bounded",
        ),
        (
            "SLOT2364_4_local_vacuum_condition",
            "local exterior q silence condition",
            "exterior silence requires B_qW=0/bounded, C_qT T_H=0 outside matter, epsilon=0, Q_q_body=0, Pi_q=0, and tail_q=0",
            "CONDITION_WRITTEN_NOT_SATISFIED",
            "local vacuum does not kill Weyl, body/boundary, or readout/history terms",
        ),
        (
            "SLOT2364_5_nohair_activation",
            "positive no-hair activation",
            "positive L_q plus zero boundary/source data, or first-class absence, can activate the q=0/local plateau branch",
            "NOT_ACTIVATED",
            "operator positivity and source silence are still open gates",
        ),
        (
            "SLOT2364_6_verdict",
            "q source-vector status",
            "normal form is derived enough to choose the first dangerous row, but not enough to claim local GR/Newton",
            "SOURCE_VECTOR_READY_CLAIM_BLOCKED",
            "prioritize B_qWeyl next because Weyl survives exterior vacuum",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "slot": slot,
            "formula_or_statement": statement,
            "status": status,
            "effect": effect,
        }
        for row_id, slot, statement, status, effect in rows
    ]


def q_euler_residual_vector() -> list[dict[str, object]]:
    rows = [
        ("EUL2364_0_BqWeyl", "B_qWeyl C_Weyl", "Weyl/tidal curvature residual", "finite residual unless no-spurion or first-class theorem closes", "FIRST_BOUND_ROW_PRIORITY", 1, "PPN;orbital;local_GR;alpha3"),
        ("EUL2364_1_BqRic", "B_qRic R_Ricci", "Ricci/Einstein operator-mixing residual", "operator-owned only after Schur/domain positivity; otherwise finite residual", "SECONDARY_OPERATOR_OR_BOUND_ROW", 2, "local_GR;R10"),
        ("EUL2364_2_CqT", "C_qT T_H", "Hilbert trace/matter coupling", "zero outside matter only after direct q matter slot is forbidden; interiors still need WEP/R10 bounds", "FINITE_BOUND_ROW_REQUIRED", 3, "WEP;PPN;R10;orbital"),
        ("EUL2364_3_epsilon", "epsilon_q_source sigma_source", "source-only q scalar", "forbidden by object language or bounded by source-width row", "FINITE_BOUND_ROW_REQUIRED", 4, "WEP;R10;clock"),
        ("EUL2364_4_Qq_body", "Q_q_body delta_body", "body/source-worldtube q charge", "body matching must prove neutral or supply a finite row", "FINITE_BOUND_ROW_REQUIRED", 5, "R10;PPN;orbital;local_GR"),
        ("EUL2364_5_Piq", "Pi_q delta_boundary", "boundary q momentum", "boundary variational principle must kill or bound it", "FINITE_BOUND_ROW_REQUIRED", 6, "R10;PPN;orbital;alpha3"),
        ("EUL2364_6_tail_q", "tail_q", "readout/history/projector/counterterm tail", "post-variation re-entry must be killed or bounded absolutely", "FINITE_BOUND_ROW_REQUIRED", 7, "clock;orbital;PPN;alpha3"),
        ("EUL2364_7_firstclass", "C_q_firstclass", "constraint-removal certificate", "if signed, all q residual rows can be removed after reduction", "OPEN_ESCAPE_NOT_SIGNED", 1, "all_local_arenas"),
        ("EUL2364_8_total_abs", "|J_q_res|", "absolute residual envelope", "|B_qW C_Weyl| + |C_qT T_H| + |epsilon sigma| + |Q_body| + |Pi_boundary| + |tail|", "SCHEMA_READY_VALUES_MISSING", 1, "all_local_arenas"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "component_id": component_id,
            "symbol_or_term": symbol,
            "meaning": meaning,
            "required_closure_or_bound": requirement,
            "status": status,
            "priority": priority,
            "observable_link": observable,
        }
        for component_id, symbol, meaning, requirement, status, priority, observable in rows
    ]


def closure_and_finite_row_gates() -> list[dict[str, object]]:
    rows = [
        ("GATE2364_0_firstclass", "q first-class/constraint removed", "Omega/generator/brackets/degree/matter/boundary all signed", "OPEN_BLOCKER", "2301/2302 keep first-class certificate unsigned"),
        ("GATE2364_1_q_representation", "q scalar/quotient/no-Weyl-spurion object language", "q type, transform law, density convention, and no hidden projector signed", "OPEN_BLOCKER", "2302/2303 found conditional clauses but no parent-signed certificate"),
        ("GATE2364_2_operator_domain", "positive L_q and Schur-owned B_qRic block", "self-adjoint domain, boundary class, positivity/coercivity, and diagonalization", "OPEN_BLOCKER", "operator route cannot be used as proof before domains are declared"),
        ("GATE2364_3_residual_zero_or_bound", "each J_q_res component zero or source-backed finite", "BqWeyl, CqT, epsilon, body, boundary, and tail rows all closed", "OPEN_BLOCKER", "no residual component is currently score-ready"),
        ("GATE2364_4_projection", "finite q profile projected to arenas", "R10/PPN/clock/orbital response kernels in same q normalization", "OPEN_BLOCKER", "arena projections exist only as requirements"),
        ("GATE2364_5_newton_gr_order", "GR/Newton limit used only after q silence", "do not use exterior GR vacuum to erase the same q residuals needed to prove GR", "ORDER_GUARD_ACTIVE", "Weyl is not vacuum-silent and Ricci silence is order-dependent"),
        ("GATE2364_6_verdict", "local-GR/Newton claim gate", "all above gates close in one parent branch", "FAIL_CURRENT_CLAIM", "source-vector normal form advances the work, but the local branch remains nonclaim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "required_evidence": evidence,
            "status": status,
            "reason": reason,
            "gate_pass": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for gate_id, gate, evidence, status, reason in rows
    ]


def first_bound_row_queue() -> list[dict[str, object]]:
    rows = [
        (
            "FBQ2364_0_BqWeyl",
            "B_qWeyl",
            1,
            "q_Weyl <= ||G_q|| |B_qWeyl| sup_D |C_Weyl| plus body/boundary/tail envelope",
            "Weyl survives exterior vacuum, so this is the dangerous local-GR residual",
            "SELECT_FIRST_BOUND_ROW_NONCLAIM",
            "Z_BqWeyl theorem-zero or BqWeyl, G_q, C_Weyl profile, tau projections, and source paths",
        ),
        (
            "FBQ2364_1_BqRic",
            "B_qRic",
            2,
            "operator Schur residual <= ||L_q^-1/2 B_qRic L_GR^-1/2||",
            "Ricci may be LHS-owned, but only after diagonalization and domain positivity",
            "PARALLEL_OPERATOR_BOUND_ROW",
            "operator domains, gauges, boundary conditions, and source normalization",
        ),
        (
            "FBQ2364_2_CqT",
            "C_qT",
            3,
            "|q_T| <= ||G_q|| |C_qT| |T_H|",
            "matter trace coupling tests direct q matter sensitivity",
            "QUEUE_AFTER_BQWEYL",
            "matter descent theorem or WEP/R10 projection units",
        ),
        (
            "FBQ2364_3_body_boundary_tail",
            "Q_q_body/Pi_q/tail_q",
            4,
            "epsilon_tail = |Q_q_body| + |Pi_q| + |tail_q| in q profile units",
            "worldtube and readout re-entry can fake a source even if bulk terms are absent",
            "QUEUE_AFTER_BULK_ROWS",
            "body matching, boundary variational principle, and readout/projector silence",
        ),
        (
            "FBQ2364_4_total_abs",
            "J_q_res_abs",
            5,
            "absolute sum of all nonzero rows must be below every arena tolerance",
            "no cancellation policy keeps the local branch honest",
            "NOT_SCORE_READY",
            "all individual rows numeric, source-backed, unit-matched, and projected",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "symbol": symbol,
            "priority": priority,
            "bound_shape": bound_shape,
            "selection_reason": reason,
            "status": status,
            "required_inputs": required,
        }
        for row_id, symbol, priority, bound_shape, reason, status, required in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2364_0_source_vector", "accept q source-vector normal form", 1, "DONE_NONCLAIM", "we now have the explicit residual vector and no-cancellation policy"),
        ("DEC2364_1_BqWeyl", "attack q no-Weyl-spurion or BqWeyl first finite row", 1, "SELECT_NEXT_TARGET", "BqWeyl is first because exterior Weyl does not vanish"),
        ("DEC2364_2_firstclass", "return to first-class q removal", 2, "KEEP_OPEN_UNSIGNED", "still strongest if it closes, but 2301/2302 lack parent canonical data"),
        ("DEC2364_3_BqRic", "build BqRic Schur/operator bound", 2, "PARALLEL_HELD", "important, but cannot silence Weyl and has order-guard issues"),
        ("DEC2364_4_CqT_body_tail", "derive matter/body/boundary/tail zero rows", 3, "QUEUE_AFTER_BQWEYL", "needed after the dangerous curvature residual is controlled"),
        ("DEC2364_5_empirical", "run PPN/R10/clock/orbital comparator", 5, "DEFER_UNTIL_INTERNAL_ROW", "testing would only test placeholders until at least one q source row is sourced"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "route": route,
            "rank": rank,
            "decision": decision,
            "reason": reason,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, route, rank, decision, reason in rows
    ]


def claim_gates() -> list[dict[str, object]]:
    rows = [
        ("CG2364_0_BqWeyl_zero", "B_qWeyl theorem-zero is active", "BLOCKED", "no q representation/no-spurion or first-class certificate is parent-signed"),
        ("CG2364_1_BqWeyl_bound", "B_qWeyl finite bound row is score-ready", "BLOCKED", "BqWeyl, Gq, Weyl profile, units, and projection rows missing"),
        ("CG2364_2_q_source_silence", "J_q_res=0 in local exterior", "BLOCKED", "body, boundary, tail, and Weyl channels remain live"),
        ("CG2364_3_local_GR_Newton", "local GR/Newton reduction derived", "BLOCKED", "q residual vector and operator gates remain open"),
        ("CG2364_4_empirical", "R10/PPN/clock/orbital pass/fail meaningful", "BLOCKED", "no source-backed internal prediction vector"),
        ("CG2364_5_public", "public claim safe", "BLOCKED", "checkpoint is private derivation plumbing only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "passes_public_claim": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, claim, status, reason in rows
    ]


def refusal_runner() -> list[dict[str, object]]:
    rows = [
        ("REF2364_0_claim_BqWeyl_zero", "claim B_qWeyl=0", "requires parent q no-spurion/representation or first-class certificate", "REFUSED"),
        ("REF2364_1_claim_local_nohair", "claim q_loc=0/no-hair", "requires positive L_q plus zero residual vector and boundary data", "REFUSED"),
        ("REF2364_2_claim_local_GR", "claim local GR/Newton derived", "requires q source silence and operator reduction without circular exterior-vacuum assumptions", "REFUSED"),
        ("REF2364_3_claim_empirical_pass", "claim R10/PPN/clock/orbital pass", "requires source-backed finite q row and arena projection kernels", "REFUSED"),
        ("REF2364_4_claim_public_ready", "publish as solved field theory", "requires complete derivation and empirical robustness, not a private source-vector checkpoint", "REFUSED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "attempted_claim": attempted,
            "missing_evidence": missing,
            "refusal_result": result,
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
        for row_id, attempted, missing, result in rows
    ]


def next_target() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2364_0_selected",
            "next_file": "2365-Y5-R2FR-q-representation-no-Weyl-spurion-or-BqWeyl-bound-row.md",
            "next_script": "scripts/Y5_R2FR_q_representation_no_Weyl_spurion_or_BqWeyl_bound_row_2365.py",
            "selected_reason": "B_qWeyl is the first dangerous residual in the q source vector because Weyl/tidal curvature survives exterior vacuum",
            "success_condition": "either activate the conditional no-Weyl-spurion/index theorem from parent-signed q representation clauses, or fill the first source-backed nonclaim B_qWeyl bound row",
            "fallback_condition": "if q representation/no-spurion remains unsigned and no numeric row can be sourced, keep local-GR/Newton blocked and move to BqRic/CqT/body-tail rows only as nonclaim acquisitions",
            "valid_for_claim": "false",
            "claim_allowed": "false",
        }
    ]


def formalization_status() -> tuple[bool, str]:
    if not FORMALIZATION_WORKBENCH.exists():
        return True, "formalization-workbench path not found; generator has no write targets there"
    try:
        result = subprocess.run(
            ["git", "-C", str(PROJECT_ROOT), "status", "--short", "--", "formalization-workbench"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return True, f"git unavailable ({exc}); generator writes only under post-checkpoint-work"
    if result.returncode == 0:
        changed = [line for line in result.stdout.splitlines() if line.strip()]
        return len(changed) == 0, "git modified-file count for formalization-workbench is 0" if not changed else f"formalization-workbench has {len(changed)} status rows"
    return True, "project is not a git worktree here; generator writes only under post-checkpoint-work"


def parse_csv_ok(paths: Iterable[Path]) -> tuple[bool, str]:
    for path in paths:
        try:
            rows = read_csv(path)
        except Exception as exc:
            return False, f"{rel(path)} failed to parse: {exc}"
        if not rows:
            return False, f"{rel(path)} has no rows"
    return True, "all generated CSV files parse and contain rows"


def no_positive_claim_flags(paths: Iterable[Path]) -> tuple[bool, str]:
    flag_columns = [
        "parent_signed",
        "theorem_zero",
        "numeric_value_present",
        "source_backed",
        "operator_domain_ready",
        "projection_ready",
        "score_ready",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "passes_public_claim",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            row_name = row.get("row_id") or row.get("component_id") or row.get("gate_id") or row.get("source_id") or "?"
            for column in flag_columns:
                if row.get(column, "").strip().lower() == "true":
                    offenders.append(f"{rel(path)}:{row_name}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": "false"})

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2364_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2364_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))

    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2364_02_outputs_exist", all(path.exists() for path in generated), "all 2364 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2364_03_csv_parse", parse_ok, parse_detail)

    slots = {row["row_id"]: row["status"] for row in read_csv(outputs["slots"])}
    add("VAL2364_04_q_euler_recorded", slots.get("SLOT2364_0_q_euler") == "NORMAL_FORM_ACCEPTED_NONCLAIM", "q Euler/source-vector normal form recorded")
    add("VAL2364_05_claim_blocked", slots.get("SLOT2364_6_verdict") == "SOURCE_VECTOR_READY_CLAIM_BLOCKED", "source-vector ready but claim blocked")

    residuals = read_csv(outputs["residuals"])
    bqweyl_rows = [row for row in residuals if row.get("component_id") == "EUL2364_0_BqWeyl"]
    add("VAL2364_06_bqweyl_first_priority", bool(bqweyl_rows and bqweyl_rows[0].get("priority") == "1"), "BqWeyl marked first dangerous residual")

    gates = {row["gate_id"]: row["status"] for row in read_csv(outputs["gates"])}
    add("VAL2364_07_local_gate_fails", gates.get("GATE2364_6_verdict") == "FAIL_CURRENT_CLAIM", "local-GR/Newton claim gate remains failed")

    bound_queue = {row["row_id"]: row["status"] for row in read_csv(outputs["bound_queue"])}
    add("VAL2364_08_bound_queue_selected", bound_queue.get("FBQ2364_0_BqWeyl") == "SELECT_FIRST_BOUND_ROW_NONCLAIM", "BqWeyl selected as first nonclaim bound row")

    decisions = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2364_09_next_route_selected", decisions.get("DEC2364_1_BqWeyl") == "SELECT_NEXT_TARGET", "next route selected")

    refusal = read_csv(outputs["refusal"])
    add("VAL2364_10_refusal_runner_blocks_claims", all(row.get("refusal_result") == "REFUSED" for row in refusal), "all premature claims are refused")

    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2364_11_no_positive_claim_flags", flag_ok, flag_detail)

    formal_ok, formal_detail = formalization_status()
    add("VAL2364_12_formalization_untouched", formal_ok, formal_detail)
    add("VAL2364_13_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2364_0_selected", "2365 BqWeyl/no-spurion target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2364_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2364 valid: q source-vector normal form consolidated, BqWeyl selected as first dangerous finite row, no local-GR/Newton claim promoted" if overall else "one or more validation gates failed",
            "valid_for_claim": "false",
        }
    )
    return rows


def write_markdown(outputs: dict[str, Path]) -> None:
    def table(headers: list[str], rows: list[dict[str, str]]) -> str:
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join("---" for _ in headers) + " |",
        ]
        for row in rows:
            lines.append("| " + " | ".join(row.get(header, "").replace("|", "/") for header in headers) + " |")
        return "\n".join(lines)

    slots = read_csv(outputs["slots"])
    residuals = read_csv(outputs["residuals"])
    gates = read_csv(outputs["gates"])
    bound_queue = read_csv(outputs["bound_queue"])
    decisions = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2364 - q Source-Vector Normal Form Or First Finite Bound Row

## Result

The q-source problem is now written in the right grammar:

`E_q = L_q q + B_qRic R_Ricci + B_qW C_Weyl + C_qT T_H + epsilon_q_source sigma_source + Q_q_body delta_body + Pi_q delta_boundary + tail_q = 0`.

So the absolute residual vector is:

`J_q_res = B_qW C_Weyl + C_qT T_H + epsilon_q_source sigma_source + Q_q_body delta_body + Pi_q delta_boundary + tail_q`.

This is progress, not a claim.  The clean local-GR/Newton route now has three honest exits: first-class q removal, operator-owned positive q dynamics with every residual silenced, or finite source rows that are numerically bounded and projected.  None is closed today.  The first dangerous row is `B_qWeyl`, because Weyl/tidal curvature survives in exterior vacuum; pretending vacuum kills it would be circular.

## Parent Action q Slot Normal Form

{table(["row_id", "slot", "status", "effect"], slots)}

## q Euler Residual Vector

{table(["component_id", "symbol_or_term", "status", "priority", "observable_link"], residuals)}

## Closure And Finite-Row Gates

{table(["gate_id", "gate", "status", "reason"], gates)}

## First Bound Row Queue

{table(["row_id", "symbol", "priority", "status", "selection_reason"], bound_queue)}

## Decision Ledger

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["slots"])}`
- `{rel(outputs["residuals"])}`
- `{rel(outputs["gates"])}`
- `{rel(outputs["bound_queue"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["refusal"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is the coupling trap made explicit.  If `B_qWeyl` can be zeroed by a real parent no-spurion/representation theorem, the local branch gets much cleaner.  If not, `B_qWeyl` must become the first finite nonclaim row with units, a q Green operator, a Weyl profile, and arena projections.  Either way, the next move is not vibes; it is a signed object-language clause or a bounded coefficient row.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_SOURCE_REGISTER.csv",
        "slots": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_PARENT_ACTION_Q_SLOT_NORMAL_FORM.csv",
        "residuals": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_Q_EULER_RESIDUAL_VECTOR.csv",
        "gates": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_CLOSURE_AND_FINITE_ROW_GATES.csv",
        "bound_queue": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_FIRST_BOUND_ROW_QUEUE.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_DECISION_LEDGER.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_CLAIM_GATES.csv",
        "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_REFUSAL_RUNNER.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2364_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2364_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["slots"], q_slot_normal_form())
    write_csv(outputs["residuals"], q_euler_residual_vector())
    write_csv(outputs["gates"], closure_and_finite_row_gates())
    write_csv(outputs["bound_queue"], first_bound_row_queue())
    write_csv(outputs["decision"], decision_ledger())
    write_csv(outputs["claims"], claim_gates())
    write_csv(outputs["refusal"], refusal_runner())
    write_csv(outputs["next"], next_target())
    validation = validation_rows(outputs, sources)
    write_csv(outputs["validation"], validation)
    write_markdown(outputs)

    for row in validation:
        line = f"{row['row_id']},{row['status']},{row['detail']}"
        print(line.encode("ascii", errors="replace").decode("ascii"))
    return 0 if validation[-1]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
