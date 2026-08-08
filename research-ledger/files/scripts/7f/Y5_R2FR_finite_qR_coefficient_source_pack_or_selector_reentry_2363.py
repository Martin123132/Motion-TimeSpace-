from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_FINITE_QR_COEFFICIENT_SOURCE_PACK_OR_SELECTOR_REENTRY_2363"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2363-Y5-R2FR-finite-qR-coefficient-source-pack-or-selector-reentry.md"
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
        "numeric_value_present": "false",
        "source_backed": "false",
        "parent_prediction_ready": "false",
        "score_ready": "false",
        "valid_prediction_row": "false",
        "valid_for_claim": "false",
        "claim_allowed": "false",
    }
    if extra:
        row.update(extra)
    return row


def source_register() -> list[dict[str, object]]:
    sources = [
        ("SRC2363_2362_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2362_NEXT_TARGET.csv", "NEXT2362_0_selected", "2362 selects finite q_R coefficient source-pack route"),
        ("SRC2363_2284_audit", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2284_FINITE_Q_INPUT_SOURCE_AUDIT.csv", "FQA2284_0_Mq2", "finite q input source audit"),
        ("SRC2363_2284_formula", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2284_Q_RESIDUAL_FORMULA_LEDGER.csv", "QRF2284_0_algebraic_parent_block", "algebraic finite q normal form"),
        ("SRC2363_2285_source_pack", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2285_COEFFICIENT_SOURCE_PACK.csv", "PACK2285_0_qR", "coefficient source-pack requirements"),
        ("SRC2363_2285_projection", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2285_PROJECTION_MATRIX_NONCLAIM.csv", "POBS2285_0_gamma", "projection matrix exists but parent values missing"),
        ("SRC2363_2286_coeffs", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2286_MQ_JQ_COEFFICIENT_DEFINITIONS.csv", "COEF2286_0_Mq2", "coefficient definitions"),
        ("SRC2363_2286_normal", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2286_WEAK_FIELD_NORMAL_FORM.csv", "NF2286_1_algebraic_q_sector", "weak-field normal form"),
        ("SRC2363_2287_extract", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2287_COEFFICIENT_EXTRACTION_ATTEMPT.csv", "COEF2287_0_Mq2", "prior extraction attempt finds no internal coefficients"),
        ("SRC2363_2288_finite", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2288_FINITE_ZQ_INTAKE_GATE.csv", "FIN2288_0_Zq", "finite Zq/Mq2/jq/tau intake gate"),
        ("SRC2363_2289_internal", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2289_FIRST_INTERNAL_COEFFICIENT_ROW_STATUS.csv", "COEFF2289_5_verdict", "no first internal finite row ready"),
        ("SRC2363_2290_tau", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2290_TAU_R10_PROJECTION_ATTEMPT.csv", "TAU2290_4_verdict", "tau_R10 projection kernel not filled"),
        ("SRC2363_2290_join", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2290_INTERNAL_JOIN_READINESS.csv", "JOIN2290_8_alpha_predicted", "R10 join readiness blocked"),
        ("SRC2363_2297_jq", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2297_JQ_COMPONENT_DECOMPOSITION.csv", "JQD2297_0_matter_bulk", "Jq component decomposition"),
        ("SRC2363_2299_slots", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2299_Q_SOURCE_SLOT_EXCLUSION_ATTEMPT.csv", "QSE2299_0_parent_object_language", "q source slot exclusion remains unsigned"),
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


def finite_normal_form() -> list[dict[str, object]]:
    rows = [
        (
            "FNF2363_0_algebraic",
            "algebraic finite q branch",
            "L_q=-1/2 M_q^2 q^2 + J_q q; J_q=j_q L+O(L^2); q=q_R L+O(L^2); q_R=j_q/M_q^2",
            "FORMULA_READY_INPUTS_MISSING",
            "requires M_q^2, j_q, units, and source normalization",
        ),
        (
            "FNF2363_1_gradient",
            "gradient/range/hair branch",
            "L_q=-1/2 Z_q |grad q|^2 -1/2 M_q^2 q^2 + J_q q plus boundary terms",
            "OPERATOR_INVENTORY_MISSING",
            "requires Z_q, boundary class, lambda_q=sqrt(Z_q/M_q^2), and Green kernel",
        ),
        (
            "FNF2363_2_source_vector",
            "absolute source vector",
            "S_q_abs=|B_qR|+|C_qT|+|epsilon_q_source|+|Q_q_body|+|Pi_q|+|tail_q|",
            "SCHEMA_READY_VALUES_MISSING",
            "prevents hidden sign cancellations from masquerading as a zero theorem",
        ),
        (
            "FNF2363_3_projection",
            "observable projection",
            "R_local=P_obs[q_R,Q_R,lambda_q,delta_beta,source_norm,clock,WEP,R10,orbital]",
            "TRANSLATION_PARTIAL_PARENT_VALUES_MISSING",
            "some PPN translations exist, but parent q/source values do not",
        ),
        (
            "FNF2363_4_closure_control",
            "explicit q=0 closure benchmark",
            "q=0/R_AB=0 may be used only as labelled control branch",
            "BENCHMARK_ONLY",
            "not a derived local-GR/Newton claim",
        ),
        (
            "FNF2363_5_verdict",
            "finite q_R normal-form status",
            "normal forms are ready, but no internal row is ready for scoring",
            "NO_INTERNAL_ROW_READY",
            "build source-vector action inventory or first finite source-bound row next",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "object": obj,
            "formula_or_statement": formula,
            "status": status,
            "effect": effect,
        }
        for row_id, obj, formula, status, effect in rows
    ]


def coefficient_pack() -> list[dict[str, object]]:
    rows = [
        ("CSP2363_0_Mq2", "M_q^2", "parent Hessian/mass gap in same q normalization", "MISSING_PARENT_HESSIAN", "blocks q_R ratio and lambda_q"),
        ("CSP2363_1_Zq", "Z_q", "operator exclusion theorem-zero or finite gradient coefficient", "MISSING_ZQ_THEOREM_OR_COEFFICIENT", "blocks R10 range/hair projection"),
        ("CSP2363_2_jq", "j_q/J_q", "matter descent zero theorem or finite source leg", "MISSING_JQ_SOURCE_OR_ZERO", "blocks q_R amplitude and WEP/source sensitivity"),
        ("CSP2363_3_boundary", "Pi_q/Q_q/B_R", "boundary no-hair theorem or finite boundary momentum", "MISSING_BOUNDARY_SOURCE_OR_ZERO", "blocks exterior hair and alpha3/orbital edges"),
        ("CSP2363_4_delta_beta", "delta_beta", "O(L^2) parent weak-field completion in valid PPN gauge", "MISSING_PARENT_BETA_COMPLETION", "blocks beta/perihelion interpretation"),
        ("CSP2363_5_source_norm", "sourceGM/Pi_M/Hilbert glue", "same source charge supplies Newtonian Phi and q-source normalization", "MISSING_SOURCE_NORMALIZATION_THEOREM", "blocks Newton derivation and fitted-GM guard"),
        ("CSP2363_6_Pobs", "P_obs", "projection matrix from finite q state to local observables", "PARTIAL_TRANSLATION_PARENT_VALUES_MISSING", "blocks empirical runner"),
        ("CSP2363_7_tau_R10", "tau_R10 / alpha_R10(lambda)", "K_q^R10 beta_source beta_test + epsilon_tail with internal range/amplitude", "MISSING_PROJECTION_KERNEL", "external R10 bounds cannot define MTS coefficients"),
        ("CSP2363_8_verdict", "first accepted/raw internal row", "all row values sourced, unit-checked, and parent-normalized", "NOT_READY", "keep all local arenas nonclaim"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "target": target,
            "required_input": required,
            "status": status,
            "blocks": blocks,
        }
        for row_id, target, required, status, blocks in rows
    ]


def source_vector_contract() -> list[dict[str, object]]:
    rows = [
        ("SVC2363_0_object_language", "parent object language", "decide before variation whether q is auxiliary, physical LHS operator, source argument, or first-class removed", "MISSING_PARENT_OBJECT_LANGUAGE_SIGNATURE"),
        ("SVC2363_1_no_direct_matter", "no direct q matter slot", "S_matter depends on q only through quotient-owned observed geometry; otherwise C_qT/j_q survives", "MISSING_NO_DIRECT_Q_SLOT_THEOREM"),
        ("SVC2363_2_no_curvature_vertex", "no q-curvature/source vertex", "B_qR and C_qT vanish only if mixed q R_obs and q T_H operators are forbidden", "MISSING_BQR_ZERO_AND_CQT_ZERO"),
        ("SVC2363_3_body_worldtube", "source-worldtube charge", "Q_q[body]=0 or bounded by body/source matching and boundary rule", "MISSING_QQ_BODY_ZERO_OR_BOUND"),
        ("SVC2363_4_boundary_tail", "boundary/readout/history/projector tails", "Pi_q, edge, readout, history, projector and counterterm tails vanish or enter abs envelope", "MISSING_TAIL_ZERO_OR_BOUND"),
        ("SVC2363_5_no_cancellation", "absolute source policy", "component signs cannot be used to cancel; every channel must be zero-proved or bounded", "POLICY_ADOPTED_NONCLAIM"),
        ("SVC2363_6_verdict", "source-vector route", "the next derivation needs action-slot inventory before numeric bounds are meaningful", "SELECT_ACTION_SLOT_NORMAL_FORM_NEXT"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "clause": clause,
            "contract": contract,
            "status": status,
        }
        for row_id, clause, contract, status in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2363_0_zero_route", "auxiliary/no-pole selector re-entry", 1, "KEEP_OPEN_UNSIGNED", "would give q_R=0 if parent protection closes, but current proof remains unsigned"),
        ("DEC2363_1_finite_algebraic", "M_q^2 and j_q finite algebraic row", 2, "BLOCKED_INPUTS_MISSING", "cleanest score route if Hessian and source leg can be sourced"),
        ("DEC2363_2_gradient_range", "Z_q/M_q^2 finite range row", 3, "BLOCKED_INPUTS_MISSING", "needed if q has a physical gradient/hair channel"),
        ("DEC2363_3_tauR10", "tau_R10 projection kernel", 4, "BLOCKED_BY_INTERNAL_RANGE_AND_CHARGES", "cannot be filled from external R10 metadata alone"),
        ("DEC2363_4_source_vector", "q source-vector normal form", 1, "SELECT_NEXT_DERIVATION_ATTACK", "it is upstream of jq, BqR, CqT, Qq_body, Pi_q and readout tails"),
        ("DEC2363_5_empirical_runner", "PPN/R10/clock/orbital runner", 5, "DEFER_UNTIL_INTERNAL_ROW", "testing is meaningful only after at least one internal prediction row exists"),
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
        ("CG2363_0_internal_row", "at least one internal finite q coefficient/source row is score-ready", "BLOCKED", "all key rows remain missing or symbolic"),
        ("CG2363_1_zero_theorem", "q_R=0 theorem-zero is parent-signed", "BLOCKED", "auxiliary/no-pole protection contract remains unsigned"),
        ("CG2363_2_projection", "P_obs/tau_R10 projection is accepted", "BLOCKED", "source/test/product kernel and internal range/amplitude missing"),
        ("CG2363_3_newton", "Newton/source normalization is derived", "BLOCKED", "same-frame sourceGM/Hilbert/worldtube glue remains missing"),
        ("CG2363_4_empirical", "local empirical pass/fail is meaningful", "BLOCKED", "no sourced parent prediction vector yet"),
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


def next_target() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2363_0_selected",
            "next_file": "2364-Y5-R2FR-q-source-vector-normal-form-or-first-finite-bound-row.md",
            "next_script": "scripts/Y5_R2FR_q_source_vector_normal_form_or_first_finite_bound_row_2364.py",
            "selected_reason": "finite qR coefficients are blocked upstream by the q source-slot/action inventory; source-vector normal form is the least hand-wavy next derivation target",
            "success_condition": "classify q source-looking terms as forbidden, LHS/operator-owned, boundary-owned, first-class removed, or finite residual with source-bound rows",
            "fallback_condition": "if parent action slots cannot be signed, keep first finite bound rows as nonclaim placeholders and defer empirical scoring",
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
        "numeric_value_present",
        "source_backed",
        "parent_prediction_ready",
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "passes_public_claim",
    ]
    offenders: list[str] = []
    for path in paths:
        for row in read_csv(path):
            for column in flag_columns:
                if row.get(column, "").strip().lower() == "true":
                    offenders.append(f"{rel(path)}:{row.get('row_id', row.get('source_id', '?'))}:{column}")
    if offenders:
        return False, "; ".join(offenders[:10])
    return True, "all generated claim/readiness flags remain negative"


def validation_rows(outputs: dict[str, Path], sources: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(row_id: str, ok: bool, detail: str) -> None:
        rows.append({"row_id": row_id, "status": "PASS" if ok else "FAIL", "detail": detail, "valid_for_claim": "false"})

    missing_sources = [str(row["source_path"]) for row in sources if row["path_exists"] != "true"]
    missing_needles = [str(row["source_id"]) for row in sources if row["needle_found"] != "true"]
    add("VAL2363_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2363_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))
    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2363_02_outputs_exist", all(path.exists() for path in generated), "all 2363 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2363_03_csv_parse", parse_ok, parse_detail)

    normal = {row["row_id"]: row["status"] for row in read_csv(outputs["normal"])}
    add("VAL2363_04_normal_form_recorded", normal.get("FNF2363_0_algebraic") == "FORMULA_READY_INPUTS_MISSING", "finite q_R algebraic normal form recorded")
    add("VAL2363_05_no_internal_row", normal.get("FNF2363_5_verdict") == "NO_INTERNAL_ROW_READY", "no internal row promoted")
    pack = read_csv(outputs["pack"])
    add("VAL2363_06_pack_nonclaim", all(row.get("score_ready") == "false" for row in pack), "coefficient source pack remains nonclaim")
    source_vector = {row["row_id"]: row["status"] for row in read_csv(outputs["source_vector"])}
    add("VAL2363_07_source_vector_next", source_vector.get("SVC2363_6_verdict") == "SELECT_ACTION_SLOT_NORMAL_FORM_NEXT", "source-vector normal form selected")
    decisions = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2363_08_next_route_selected", decisions.get("DEC2363_4_source_vector") == "SELECT_NEXT_DERIVATION_ATTACK", "q source-vector normal form selected as next derivation attack")
    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2363_09_no_positive_claim_flags", flag_ok, flag_detail)
    formal_ok, formal_detail = formalization_status()
    add("VAL2363_10_formalization_untouched", formal_ok, formal_detail)
    add("VAL2363_11_claim_gates_blocked", all(row.get("passes_public_claim") == "false" for row in read_csv(outputs["claims"])), "all claim gates blocked")
    add("VAL2363_12_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2363_0_selected", "2364 source-vector target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2363_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2363 valid: finite q_R source pack consolidated, no internal row promoted, q source-vector normal form selected" if overall else "one or more validation gates failed",
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

    normal = read_csv(outputs["normal"])
    pack = read_csv(outputs["pack"])
    source_vector = read_csv(outputs["source_vector"])
    decisions = read_csv(outputs["decision"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2363 — Finite `q_R` Coefficient Source Pack Or Selector Re-entry

## Result

The finite-residual route is now in one place.  The clean algebraic branch is:

`L_q = -1/2 M_q^2 q^2 + J_q q`, with `J_q=j_q L+O(L^2)`, so `q=q_R L+O(L^2)` and `q_R=j_q/M_q^2`.

That is a testable shape, not yet a prediction.  `M_q^2`, `Z_q`, `j_q/J_q`, boundary charge, `P_obs`, `tau_R10`, and Newton/source normalization are all still missing as parent-owned internal rows.  The correct next move is upstream: write the q source-vector/action-slot normal form, so source-looking terms are either forbidden, operator-owned, boundary-owned, first-class removed, or retained as finite residual rows.

## Finite Normal Form

{table(["row_id", "object", "status", "effect"], normal)}

## Coefficient Source Pack

{table(["row_id", "target", "status", "blocks"], pack)}

## Source-Vector Contract

{table(["row_id", "clause", "status"], source_vector)}

## Decision Ledger

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["normal"])}`
- `{rel(outputs["pack"])}`
- `{rel(outputs["source_vector"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["claims"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This is where testing starts becoming concrete: not by running R10/PPN on placeholders, but by forcing the theory to supply one internal row.  First target is the q source-vector/action-slot normal form.  If it closes, some source terms become theorem-zero.  If it fails, the same rows become honest finite coefficients to source and bound.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2363_SOURCE_REGISTER.csv",
        "normal": RESIDUALS / "P8_Y5_PARENT_QLOC_2363_FINITE_QR_NORMAL_FORM.csv",
        "pack": RESIDUALS / "P8_Y5_PARENT_QLOC_2363_COEFFICIENT_SOURCE_PACK.csv",
        "source_vector": RESIDUALS / "P8_Y5_PARENT_QLOC_2363_Q_SOURCE_VECTOR_CONTRACT.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2363_DECISION_LEDGER.csv",
        "claims": RESIDUALS / "P8_Y5_PARENT_QLOC_2363_CLAIM_GATES.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2363_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2363_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["normal"], finite_normal_form())
    write_csv(outputs["pack"], coefficient_pack())
    write_csv(outputs["source_vector"], source_vector_contract())
    write_csv(outputs["decision"], decision_ledger())
    write_csv(outputs["claims"], claim_gates())
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
