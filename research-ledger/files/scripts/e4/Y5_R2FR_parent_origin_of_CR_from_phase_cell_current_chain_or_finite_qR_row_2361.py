from __future__ import annotations

import csv
import subprocess
from pathlib import Path
from typing import Iterable


BRANCH_ID = "MTS_R2FR_PARENT_ORIGIN_OF_CR_PHASE_CELL_CURRENT_CHAIN_OR_FINITE_QR_2361"
POST_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = POST_ROOT.parent
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2361-Y5-R2FR-parent-origin-of-CR-from-phase-cell-current-chain-or-finite-qR-row.md"
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
        ("SRC2361_2360_doc", "2360-Y5-R2FR-second-class-auxiliary-origin-no-derivative-grammar-or-finite-leak.md", "parent origin remains the first lock", "2360 selected parent origin as first lock"),
        ("SRC2361_2360_next", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2360_NEXT_TARGET.csv", "NEXT2360_0_selected", "machine-selected 2361 target"),
        ("SRC2361_11_cell_current", "11-cell-current-origin-attempt.md", "cell_current_origin_no_charge_obstruction", "ordinary current conservation leaves Q_R hair"),
        ("SRC2361_1577_radial_current", "1577-Y5-RAB-radial-observer-cell-current-or-finite-component-bound-fill.md", "RCC1577_0_current_equation", "radial observer-cell current rejected as exact derivation"),
        ("SRC2361_2227_phase_volume", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2227_PHASE_VOLUME_ORIGIN_AUDIT.csv", "ORG2227_5_current_verdict", "phase-volume motivates but does not derive q-sector origin"),
        ("SRC2361_2267_contract", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2267_LAMBDAR_ORIGIN_CONTRACT.csv", "LOC2267_1_psi_quotient_origin", "lists ψ quotient origin as a required input"),
        ("SRC2361_2268_tests", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2268_PHASE_VOLUME_PSI_ORIGIN_TESTS.csv", "OT2268_2_psi_covariance", "ψ covariance map is open rather than closed"),
        ("SRC2361_2283_finalizer", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2283_Q_CLOSURE_FINALIZER.csv", "QCF2283_3_reentry", "closure finalizer leaves re-entry for first-class or ψ quotient theorem"),
        ("SRC2361_2051_lambda", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2051_LAMBDAR_ORIGIN_AUDIT.csv", "LAM2051_6_verdict", "lambda_R parent origin not present in current corpus"),
        ("SRC2361_1866_gate", "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1866_LAMBDAR_ORIGIN_GATE.csv", "LOG1866_4_verdict", "object-language or canonical parent grammar required"),
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


def cr_origin_attempt() -> list[dict[str, object]]:
    rows = [
        (
            "CR2361_0_identity",
            "configuration-cell identity",
            "J_q = T sqrt(S), so C_R = ln(T^2 S) = 2 ln J_q and C_R=0 iff J_q=1.",
            "EXACT_IDENTITY_NOT_PARENT_LAW",
            "names the target but does not select it dynamically",
        ),
        (
            "CR2361_1_generic_liouville",
            "generic phase-volume preservation",
            "J_q J_p=1 holds generically after defining reciprocal momentum cell.",
            "REJECTED_TOO_WEAK",
            "true for every p-like route and cannot select the GR lane",
        ),
        (
            "CR2361_2_ordinary_current",
            "radial cell-current conservation",
            "partial_r(W_R partial_r C_R)=0 gives W_R C_R'=Q_R.",
            "REJECTED_NO_CHARGE_OBSTRUCTION",
            "conservation gives constant charge; it does not set Q_R=0",
        ),
        (
            "CR2361_3_boundary_normalization",
            "asymptotic normalization",
            "C_R(infinity)=0 fixes only the additive constant.",
            "REJECTED_IF_QR_NONZERO",
            "exterior C_R=-Q_R integral/W_R survives unless Q_R is killed",
        ),
        (
            "CR2361_4_nonpropagating_constraint",
            "lambda_R C_R closure",
            "delta_lambda S gives C_R=0 exactly if lambda_R block is admitted.",
            "CLOSURE_ONLY",
            "works as a benchmark but parent origin/backreaction remains unproved",
        ),
        (
            "CR2361_5_reduced_configuration",
            "pre-variation reduced q=0 configuration",
            "exclude q/C_R from the local vacuum configuration space before variation.",
            "BEST_CONDITIONAL_SEED_NOT_DERIVED",
            "avoids multiplier backreaction but needs parent reason q is absent/frozen",
        ),
        (
            "CR2361_6_psi_quotient",
            "ψ covariance quotient/determinant route",
            "derive the metric/readout map so q is absent, vertical, or minimized by the parent ψ covariance structure.",
            "BEST_NEXT_NONCIRCULAR_ROUTE",
            "could supply parent origin without ordinary current hair or post-hoc multiplier",
        ),
        (
            "CR2361_7_verdict",
            "parent origin of C_R",
            "phase-cell/current-chain routes do not currently prove C_R=0; they identify the needed constraint and the obstruction.",
            "PARENT_ORIGIN_NOT_DERIVED",
            "attack ψ quotient/determinant theorem next, keep finite q_R rows live",
        ),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "candidate_origin": candidate,
            "mathematical_content": content,
            "status": status,
            "effect": effect,
        }
        for row_id, candidate, content, status, effect in rows
    ]


def current_chain_audit() -> list[dict[str, object]]:
    rows = [
        ("CCA2361_0_target", "target current", "j_q should select J_q=1 or C_R=0 before local readout", "TARGET_DEFINED", "must be stronger than ordinary conservation"),
        ("CCA2361_1_continuity", "continuity equation", "nabla_a j_q^a=0", "TOO_WEAK", "integrated charge is conserved, not forced to vanish"),
        ("CCA2361_2_gradient_current", "gradient current", "j_q^r=W_R partial_r C_R", "NO_CHARGE_OBSTRUCTION", "Q_R hair survives"),
        ("CCA2361_3_no_charge", "no-charge theorem", "Q_R=0 from source neutrality and boundary/proper charge", "MISSING_THEOREM", "needed for current route to become derivation"),
        ("CCA2361_4_topological_flat", "flat/topological cell connection", "F_cell=0 with trivial holonomy could remove local hair", "PROMISING_BUT_UNSIGNED", "stress owner, holonomy class, and matter map missing"),
        ("CCA2361_5_parent_euler", "parent Euler difference", "E_T - E_S or equivalent forces d ln(T sqrt(S))=0 with zero charge", "MISSING_PARENT_EQUATIONS", "would be strongest direct derivation if built"),
        ("CCA2361_6_verdict", "current-chain verdict", "current language is bookkeeping until no-charge or ψ quotient closes", "DO_NOT_LOOP_CURRENT_ROUTE", "move to ψ determinant map or finite q_R"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "gate": gate,
            "required_statement": statement,
            "status": status,
            "failure_or_next": effect,
        }
        for row_id, gate, statement, status, effect in rows
    ]


def decision_ledger() -> list[dict[str, object]]:
    rows = [
        ("DEC2361_0_cell_identity", "C_R=2 ln J_q identity", 1, "KEEP_AS_DEFINITION", "exact and useful but not a parent law"),
        ("DEC2361_1_current_route", "ordinary phase-cell/current chain", 4, "REJECT_AS_STANDALONE_DERIVATION", "gives Q_R hair without no-charge theorem"),
        ("DEC2361_2_lambda_route", "post-hoc multiplier", 5, "KEEP_AS_CLOSURE_BENCHMARK_ONLY", "variation works but origin/backreaction not derived"),
        ("DEC2361_3_reduced_config", "pre-variation reduced configuration", 2, "KEEP_AS_SEED", "avoids multiplier backreaction if parent-owned"),
        ("DEC2361_4_psi_quotient", "ψ determinant/quotient map", 1, "SELECT_NEXT_ATTACK", "least circular remaining route to make q absent or vertical before variation"),
        ("DEC2361_5_finite_qR", "finite q_R residual row", 3, "KEEP_FALLBACK", "needed if ψ/reduced-configuration route fails"),
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


def finite_qr_contract() -> list[dict[str, object]]:
    rows = [
        ("FQ2361_0_qR_amplitude", "q_R / Q_R exterior charge", "derive Q_R=0 or source finite value and units", "MISSING_NO_CHARGE_THEOREM", "sets local reciprocal hair"),
        ("FQ2361_1_Zq", "Z_q kinetic coefficient", "prove forbidden or source numeric coefficient", "MISSING_OPERATOR_SIGNATURE", "sets pole strength"),
        ("FQ2361_2_Mq2", "M_q^2 stiffness", "source positive mass/stiffness or theorem-zero", "MISSING_STIFFNESS_INPUT", "sets finite range"),
        ("FQ2361_3_Jq_source", "source current J_q", "prove matter descent or source coupling", "MISSING_SOURCE_MAP", "sets WEP/R10/PPN amplitude"),
        ("FQ2361_4_Bq_boundary", "boundary/proper charge", "prove zero/exact/proper or source bound", "MISSING_BOUNDARY_CLASS", "sets exterior tail"),
        ("FQ2361_5_Pobs", "observable projection P_obs", "derive projection norm into clocks/orbits/EM/PPN", "MISSING_PROJECTION", "sets arena transfer"),
        ("FQ2361_6_tau", "tau_R10/tau_PPN/tau_clock/tau_orbital", "source arena transfer coefficients", "MISSING_ARENA_TRANSFER", "needed for empirical comparator"),
        ("FQ2361_7_verdict", "finite q_R branch", "cannot score until rows are numeric, sourced, and bounded", "NOT_SCORE_READY", "no local claim"),
    ]
    return [
        {
            **no_claim(),
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "quantity": quantity,
            "required_resolution": required,
            "status": status,
            "effect": effect,
        }
        for row_id, quantity, required, status, effect in rows
    ]


def next_target() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2361_0_selected",
            "next_file": "2362-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md",
            "next_script": "scripts/Y5_R2FR_psi_determinant_quotient_map_or_finite_qR_coefficients_2362.py",
            "selected_reason": "phase-cell/current routes identify C_R but do not parent-select C_R=0; ψ quotient is the least circular remaining route",
            "success_condition": "construct q:psi-data -> reduced local geometry and prove C_R/q is absent, vertical, or stationary before matter/readout",
            "fallback_condition": "if the ψ map remains open, start sourcing finite q_R coefficients instead of trying another current shortcut",
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
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
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
    add("VAL2361_00_required_sources_exist", not missing_sources, "all required source paths exist" if not missing_sources else "; ".join(missing_sources))
    add("VAL2361_01_required_needles_found", not missing_needles, "all source needles found" if not missing_needles else "; ".join(missing_needles))
    generated = [path for key, path in outputs.items() if key != "validation"]
    add("VAL2361_02_outputs_exist", all(path.exists() for path in generated), "all 2361 output files written")
    parse_ok, parse_detail = parse_csv_ok([path for path in generated if path.suffix == ".csv"])
    add("VAL2361_03_csv_parse", parse_ok, parse_detail)

    attempt = {row["row_id"]: row["status"] for row in read_csv(outputs["attempt"])}
    add("VAL2361_04_identity_recorded", attempt.get("CR2361_0_identity") == "EXACT_IDENTITY_NOT_PARENT_LAW", "C_R/J_q identity recorded without promoting it")
    add("VAL2361_05_current_rejected", attempt.get("CR2361_2_ordinary_current") == "REJECTED_NO_CHARGE_OBSTRUCTION", "ordinary current route rejected as standalone derivation")
    add("VAL2361_06_parent_origin_not_promoted", attempt.get("CR2361_7_verdict") == "PARENT_ORIGIN_NOT_DERIVED", "parent origin remains unclaimed")
    decisions = {row["row_id"]: row["decision"] for row in read_csv(outputs["decision"])}
    add("VAL2361_07_psi_next_selected", decisions.get("DEC2361_4_psi_quotient") == "SELECT_NEXT_ATTACK", "ψ determinant/quotient route selected next")
    finite = read_csv(outputs["finite"])
    add("VAL2361_08_finite_rows_nonclaim", all(row.get("score_ready") == "false" for row in finite), "finite q_R rows remain not score-ready")
    flag_ok, flag_detail = no_positive_claim_flags([path for path in generated if path.suffix == ".csv"])
    add("VAL2361_09_no_positive_claim_flags", flag_ok, flag_detail)
    formal_ok, formal_detail = formalization_status()
    add("VAL2361_10_formalization_untouched", formal_ok, formal_detail)
    add("VAL2361_11_next_selected", read_csv(outputs["next"])[0].get("row_id") == "NEXT2361_0_selected", "2362 ψ quotient target selected")

    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "row_id": "VAL2361_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2361 valid: C_R origin attempt rejects current shortcut, preserves finite q_R fallback, selects ψ quotient map" if overall else "one or more validation gates failed",
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

    attempt = read_csv(outputs["attempt"])
    chain = read_csv(outputs["chain"])
    decisions = read_csv(outputs["decision"])
    finite = read_csv(outputs["finite"])
    next_rows = read_csv(outputs["next"])

    md = f"""# 2361 — Parent Origin Of `C_R` From Phase-Cell Current Chain Or Finite `q_R` Row

## Result

The exact identity is now separated from the parent-law problem:

`J_q = T sqrt(S)`, therefore `C_R = ln(T^2 S) = 2 ln J_q`, and `C_R=0` iff `J_q=1`.

That is useful but not enough.  Ordinary phase-cell/current conservation gives `W_R C_R' = Q_R`, so it preserves reciprocal hair unless a separate no-charge theorem sets `Q_R=0`.  The least circular remaining route is therefore not another current loop: it is a `psi` determinant/quotient map proving `q/C_R` is absent, vertical, or stationary before matter/readout.

## `C_R` Origin Attempt

{table(["row_id", "candidate_origin", "status", "effect"], attempt)}

## Current-Chain Audit

{table(["row_id", "gate", "status", "failure_or_next"], chain)}

## Decision Ledger

{table(["row_id", "route", "rank", "decision", "reason"], decisions)}

## Finite `q_R` Fallback

{table(["row_id", "quantity", "status", "effect"], finite)}

## Next Target

{table(["row_id", "next_file", "success_condition", "fallback_condition"], next_rows)}

## Generated Files

- `{rel(outputs["source"])}`
- `{rel(outputs["attempt"])}`
- `{rel(outputs["chain"])}`
- `{rel(outputs["decision"])}`
- `{rel(outputs["finite"])}`
- `{rel(outputs["next"])}`
- `{rel(outputs["validation"])}`

## Practical Status

This trims the loop.  The cell-current path is not useless: it tells us exactly what must be killed, `Q_R`.  But it is not the killer.  Either the parent `psi` structure removes/freezes `q` before variation, or we stop trying to hide the residual and source the finite `q_R` coefficients honestly.
"""
    DOC_PATH.write_text(md, encoding="utf-8")


def main() -> int:
    sources = source_register()
    outputs = {
        "source": RESIDUALS / "P8_Y5_PARENT_QLOC_2361_SOURCE_REGISTER.csv",
        "attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_2361_CR_ORIGIN_PROOF_ATTEMPT.csv",
        "chain": RESIDUALS / "P8_Y5_PARENT_QLOC_2361_PHASE_CELL_CURRENT_CHAIN_AUDIT.csv",
        "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_2361_PARENT_ORIGIN_DECISION_LEDGER.csv",
        "finite": RESIDUALS / "P8_Y5_PARENT_QLOC_2361_FINITE_QR_ROW_CONTRACT.csv",
        "next": RESIDUALS / "P8_Y5_PARENT_QLOC_2361_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_2361_VALIDATION.csv",
    }

    write_csv(outputs["source"], sources)
    write_csv(outputs["attempt"], cr_origin_attempt())
    write_csv(outputs["chain"], current_chain_audit())
    write_csv(outputs["decision"], decision_ledger())
    write_csv(outputs["finite"], finite_qr_contract())
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
