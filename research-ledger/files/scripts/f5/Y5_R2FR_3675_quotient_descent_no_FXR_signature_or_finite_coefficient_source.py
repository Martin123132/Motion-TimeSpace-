from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3675"
BRANCH_ID = "MTS_R2FR_Y5_QUOTIENT_DESCENT_NO_FXR_SIGNATURE_OR_FINITE_COEFFICIENT_SOURCE_3675"
DOC = ROOT / "3675-Y5-R2FR-quotient-descent-no-FXR-signature-or-finite-coefficient-source.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        rows = load_csv(path)
        return True, len(rows)
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3674", RESIDUALS / "P8_Y5_R2FR_3674_NEXT_TARGET.csv", "quotient-descent-no-FXR", "3674 selected no-FXR signature or finite coefficient source"),
        ("doc_3674", ROOT / "3674-Y5-R2FR-nonminimal-FXR-owner-or-ban-gate.md", "F0_prime=0", "conditional F(X)R ban theorem"),
        ("ban_3674", RESIDUALS / "P8_Y5_R2FR_3674_QUOTIENT_DESCENT_BAN_THEOREM_ROWS.csv", "QDB3674_5_ban_theorem", "ban theorem rows"),
        ("bounds_3674", RESIDUALS / "P8_Y5_R2FR_3674_INHERITED_FXR_BOUND_ROWS.csv", "A_H*F0_prime", "finite F(X)R inherited bounds"),
        ("coeff_templates_3674", RESIDUALS / "P8_Y5_R2FR_3674_FXR_COEFFICIENT_TEMPLATE_ROWS.csv", "FXRC3674_0_allowed_branch", "coefficient template rows"),
        ("doc_1022", ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md", "S_parent=S_red[q(Phi)]", "quotient/action descent clause"),
        ("audit_1037", RESIDUALS / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv", "NP1037_1_action_descent", "no physical X pole audit"),
        ("minimality_964", RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv", "MIN964_4_descent_signature", "minimality/no-reentry theorem attempt"),
        ("doc_964", ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md", "marker-prefactor `F(sigma)R`", "F(sigma)R countermodel remains live"),
        ("contract_990", RESIDUALS / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_1_gravity_operator", "parent action contract"),
        ("vertex_1048", RESIDUALS / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv", "PVS1048_0_field_domain", "operator list signature audit"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def signature_audit_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "SIG3675_0_q_kernel",
            "Dq[v_X]=0 for the actual local X branch",
            "1022/1037 give the correct quotient test and route preference.",
            "CONTRACT_PRESENT_NOT_PARENT_SIGNED",
            "need field-by-field q map and vertical generator for X",
            False,
        ),
        (
            "SIG3675_1_grav_action_descent",
            "S_grav[Phi]=S_EH[q(Phi)] before variation",
            "1022 gives the descent condition; 990 says EH-only or retained R11 executable, not a signed no-FXR theorem.",
            "CONDITIONAL_NOT_SIGNED",
            "need parent Lagrangian or operator grammar proving no independent X argument in gravity sector",
            False,
        ),
        (
            "SIG3675_2_no_FXR_slot",
            "no F(X)R or F(Xhat)R local operator",
            "964 explicitly retains marker-prefactor F(sigma)R as a legal countermodel unless minimality/no-extension is proven.",
            "FAILED_CURRENT_SIGNATURE_COUNTERMODEL_LIVE",
            "need primitive quotient/no-natural-marker theorem or declared allowed-operator list",
            False,
        ),
        (
            "SIG3675_3_no_reentry",
            "no integrated-out scalar, projector, memory, or nonlocal re-entry",
            "964 says integrated-out towers and nonlocal memory kernels remain legal until no-reentry is proven.",
            "FAILED_CURRENT_SIGNATURE_REENTRY_LIVE",
            "need sector elimination theorem showing Delta S_eff has no R*X or F(X)R term",
            False,
        ),
        (
            "SIG3675_4_readout_descent",
            "observed metric/readout descends through q with no X frame",
            "1048 covers clock/readout vertices for constants but does not sign a full no-Hessian readout frame for this branch.",
            "CONTRACT_PRESENT_NOT_PARENT_SIGNED",
            "need no A(X)g_obs, no disformal derivative frame, no boundary Hessian readout term",
            False,
        ),
        (
            "SIG3675_5_verdict",
            "no-FXR signature status",
            "The ban theorem is mathematically useful, but current evidence does not sign all clauses, so k_H_geo=0 cannot be promoted.",
            "NO_FXR_ZERO_NOT_CLAIMED_FINITE_BRANCH_REQUIRED",
            "stage finite A_H,F0,F0_prime coefficient source rows",
            False,
        ),
    ]
    return [
        {
            **base(ts),
            "signature_id": signature_id,
            "clause": clause,
            "evidence_summary": evidence_summary,
            "status": status,
            "missing_for_signature": missing,
            "source_signed": source_signed,
            "claim_allowed": False,
        }
        for signature_id, clause, evidence_summary, status, missing, source_signed in specs
    ]


def finite_coefficient_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "FCS3675_0_AH",
            "A_H",
            "dimensionless",
            "nonminimal curvature slot amplitude in S_H=(M_*^2/2) int sqrt(-g) A_H F(X) R",
            "parent gravity operator list and normalization of the F(X)R term",
            "MISSING_PARENT_SLOT",
        ),
        (
            "FCS3675_1_F0",
            "F0",
            "dimensionless",
            "background value F(X0) entering the effective EH normalization denominator",
            "local background branch and F function definition",
            "MISSING_PARENT_FUNCTION",
        ),
        (
            "FCS3675_2_F0_prime",
            "F0_prime",
            "per normalized X_b",
            "first derivative of F with respect to the normalized local X variable at X0",
            "parent field normalization and derivative convention",
            "MISSING_PARENT_FUNCTION_DERIVATIVE",
        ),
        (
            "FCS3675_3_DH",
            "D_H=1+A_H*F0",
            "dimensionless",
            "effective EH normalization denominator for the geometric branch",
            "A_H and F0",
            "MISSING_COMPONENTS",
        ),
        (
            "FCS3675_4_cFXR",
            "c_FXR=A_H*F0_prime/(1+A_H*F0)",
            "dimensionless",
            "finite geometric Hessian-STF coefficient magnitude before f_EM/Z_X projection",
            "A_H, F0, F0_prime, equation-side sign convention",
            "FORMULA_READY_INPUTS_MISSING",
        ),
        (
            "FCS3675_5_xiFXR",
            "xi_FXR=|c_FXR*f_EM/Z_X|",
            "dimensionless",
            "Cassini/Shapiro scalar-slip branch amplitude bounded by 3671/3672/3674 rows",
            "c_FXR, f_EM, Z_X, boundary/readout and quadratic floor bounds",
            "BOUND_INTERFACE_READY_INPUTS_MISSING",
        ),
    ]
    return [
        {
            **base(ts),
            "coefficient_id": coefficient_id,
            "symbol": symbol,
            "units": units,
            "definition": definition,
            "required_source": required_source,
            "current_status": status,
            "numeric_value": "MISSING_PARENT_INPUT",
            "score_ready": False,
            "claim_allowed": False,
        }
        for coefficient_id, symbol, units, definition, required_source, status in specs
    ]


def finite_bound_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in load_csv(RESIDUALS / "P8_Y5_R2FR_3674_INHERITED_FXR_BOUND_ROWS.csv"):
        rows.append(
            {
                **base(ts),
                "bound_id": str(row["bound_id"]).replace("FXRB3674", "FXRS3675"),
                "source_bound_id": row["bound_id"],
                "kernel_id": row["kernel_id"],
                "xi_H_max": row["xi_H_max"],
                "finite_coefficient_bound": f"|c_FXR*f_EM/Z_X| <= {row['xi_H_max']}",
                "c_FXR_definition": "c_FXR=A_H*F0_prime/(1+A_H*F0)",
                "zero_branch_value": "0 only if SIG3675_0..4 become source_signed=true",
                "inherited_allowed_bound": row["fxr_allowed_bound"],
                "stress_fallback_bound": row["stress_fallback_bound"],
                "status": "FINITE_FXR_BOUND_ROW_NONCLAIM",
                "why_nonclaim": "no-FXR ban is unsigned and finite A_H,F0,F0_prime,f_EM,Z_X/floors are missing",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def blocker_or_source_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "BOS3675_0_best_zero_route",
            "primitive quotient/no-natural-marker theorem",
            "prove every local exterior gravitational operator factors through q and forbids marker scalar arguments",
            "would sign SIG3675_0..2",
            "DERIVATION_TARGET",
        ),
        (
            "BOS3675_1_no_reentry_route",
            "integrated-out sector no-reentry theorem",
            "prove auxiliary/projector/memory sectors cannot generate R*X, F(X)R, R Box^-1 R, or scalar-tensor poles",
            "would sign SIG3675_3",
            "DERIVATION_TARGET",
        ),
        (
            "BOS3675_2_readout_route",
            "single public metric/readout descent",
            "prove clocks/light/rods use q(Phi) only, with no conformal/disformal/derivative X readout or boundary Hessian term",
            "would sign SIG3675_4",
            "DERIVATION_TARGET",
        ),
        (
            "BOS3675_3_finite_source_route",
            "finite coefficient source acquisition",
            "if zero route fails, source A_H,F0,F0_prime and f_EM/Z_X from parent action rather than fitting Cassini",
            "would make finite branch testable but not automatically local-GR",
            "ACQUISITION_ROUTE",
        ),
    ]
    return [
        {
            **base(ts),
            "route_id": route_id,
            "route": route,
            "task": task,
            "effect": effect,
            "status": status,
            "claim_allowed": False,
        }
        for route_id, route, task, effect, status in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3675_0_no_zero_promotion",
            "Do not promote k_H_geo=0.",
            "The ban theorem has the right shape, but source evidence leaves no-FXR/no-reentry/readout clauses unsigned.",
            "NO_FXR_ZERO_REFUSED",
        ),
        (
            "DEC3675_1_finite_branch_named",
            "Use c_FXR as the finite branch coefficient.",
            "The allowed branch is no longer vague coupling: c_FXR=A_H*F0_prime/(1+A_H*F0).",
            "FINITE_COEFFICIENT_LEDGER_CREATED",
        ),
        (
            "DEC3675_2_best_next",
            "Prioritize no-natural-marker/no-reentry proof before numeric fitting.",
            "If the ban theorem signs, the branch dies cleanly and local GR improves; if not, coefficient sourcing remains disciplined.",
            "SELECT_3676_NO_NATURAL_MARKER_NO_REENTRY",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3675_0_signature_audit", "no-FXR signature audit", "PASS_AUDIT", "all ban clauses checked against current source trail"),
        ("CG3675_1_zero_claim", "k_H_geo=0 claim", "BLOCKED_UNSIGNED_SIGNATURE", "SIG3675_0..4 are not all source-signed"),
        ("CG3675_2_finite_coefficients", "finite c_FXR coefficient", "BLOCKED_PARENT_INPUTS", "A_H,F0,F0_prime,f_EM,Z_X missing"),
        ("CG3675_3_bound_rows", "finite branch bound rows", "PASS_NONCLAIM_INTERFACE", "rows generated from inherited 3674 bounds"),
        ("CG3675_4_local_GR", "Cassini/local-GR claim", "BLOCKED_NONCLAIM", "zero and finite branches are both nonclaim"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "detail": detail,
            "claim_allowed": False,
        }
        for gate_id, gate, status, detail in specs
    ]


def status_rows(ts: str, bounds: list[dict[str, object]]) -> list[dict[str, object]]:
    strongest = min(bounds, key=lambda row: float(row["xi_H_max"]))
    return [
        {
            **base(ts),
            "status": "NO_FXR_SIGNATURE_UNSIGNED_FINITE_CFXR_SOURCE_ROWS_STAGED",
            "summary": "3675 attempts to sign the quotient/action/readout descent ban for F(X)R and refuses promotion: no-FXR, no-reentry, and no-readout-Hessian clauses remain unsigned. The finite branch is now explicit as c_FXR=A_H*F0_prime/(1+A_H*F0), with inherited nonclaim bound rows.",
            "claim_ceiling": "no k_H zero, finite F(X)R prediction, Cassini/gamma, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": f"Strongest finite branch row is {strongest['finite_coefficient_bound']}; zero branch requires SIG3675_0..4 source_signed=true.",
            "next_missing_piece": "prove no-natural-marker/no-reentry/readout descent, or source A_H,F0,F0_prime and f_EM/Z_X",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3675_0",
            "target_doc": "3676-Y5-R2FR-no-natural-marker-no-reentry-theorem-or-FXR-prior-row.md",
            "target_script": "scripts/Y5_R2FR_3676_no_natural_marker_no_reentry_theorem_or_FXR_prior_row.py",
            "objective": "try to prove the primitive quotient/no-natural-marker plus no-reentry theorem needed to sign no-FXR; if it fails, create an explicit nonclaim prior/source row for c_FXR",
            "success_gate": "either no marker/no reentry closes enough to set c_FXR=0, or c_FXR has a finite nonclaim prior/source row with every missing parent input named",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    signatures: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    bounds: list[dict[str, object]],
    routes: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    strongest = min(bounds, key=lambda row: float(row["xi_H_max"]))
    lines = [
        "# 3675 - Quotient descent no-FXR signature or finite coefficient source",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "Result: the clean zero path is **not signed yet**. The right theorem is known, but the current corpus still leaves marker-prefactor, integrated-out scalar, improvement-stress, and readout-frame re-entry live.",
        "",
        "So the finite branch is named explicitly:",
        "",
        "`c_FXR = A_H*F0_prime/(1+A_H*F0)`",
        "",
        "and the tested scalar-slip amplitude is:",
        "",
        "`xi_FXR = |c_FXR*f_EM/Z_X|`.",
        "",
        f"Strongest inherited finite-row template: `{strongest['finite_coefficient_bound']}`.",
        "",
        "The zero branch remains legal only if every `SIG3675_0..4` row becomes `source_signed=true`.",
        "",
        "## Signature audit",
    ]
    for row in signatures:
        lines.append(f"- `{row['signature_id']}`: {row['status']} - {row['clause']}")
    lines.extend(["", "## Finite coefficient ledger"])
    for row in coefficients:
        lines.append(f"- `{row['coefficient_id']}`: `{row['symbol']}` [{row['units']}] - {row['current_status']}")
    lines.extend(["", "## Finite bound rows"])
    for row in bounds[:5]:
        lines.append(f"- `{row['bound_id']}`: `{row['finite_coefficient_bound']}`")
    lines.extend(["", "## Blocker/source routes"])
    for row in routes:
        lines.append(f"- `{row['route_id']}`: {row['status']} - {row['route']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']}")
    lines.extend(
        [
            "",
            "## Next target",
            f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.",
            "",
            "## Sources",
        ]
    )
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    signatures: list[dict[str, object]],
    coefficients: list[dict[str, object]],
    bounds: list[dict[str, object]],
    routes: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + signatures + coefficients + bounds + routes + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3675*", "3675-Y5-R2FR-*", "P8_Y5*3675*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3675_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3675_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3675_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3675 outputs written")
    add("VAL3675_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3675_4_signature_audit", {"SIG3675_0_q_kernel", "SIG3675_1_grav_action_descent", "SIG3675_2_no_FXR_slot", "SIG3675_3_no_reentry", "SIG3675_4_readout_descent", "SIG3675_5_verdict"}.issubset({str(row["signature_id"]) for row in signatures}), "signature audit covers all no-FXR clauses")
    add("VAL3675_5_zero_not_signed", not all(str(row["source_signed"]).lower() == "true" for row in signatures if row["signature_id"] != "SIG3675_5_verdict"), "no-FXR zero is not source-signed")
    add("VAL3675_6_coefficients", {"A_H", "F0", "F0_prime", "c_FXR=A_H*F0_prime/(1+A_H*F0)", "xi_FXR=|c_FXR*f_EM/Z_X|"}.issubset({str(row["symbol"]) for row in coefficients}), "finite coefficient ledger has required symbols")
    add("VAL3675_7_bounds", len(bounds) == len(load_csv(RESIDUALS / "P8_Y5_R2FR_3674_INHERITED_FXR_BOUND_ROWS.csv")) and all("c_FXR" in row["finite_coefficient_bound"] for row in bounds), "finite c_FXR bound rows generated")
    add("VAL3675_8_routes", {"BOS3675_0_best_zero_route", "BOS3675_1_no_reentry_route", "BOS3675_2_readout_route", "BOS3675_3_finite_source_route"}.issubset({str(row["route_id"]) for row in routes}), "blocker/source routes present")
    add("VAL3675_9_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3675_10_claim_gates", any(row["claim_gate_id"] == "CG3675_4_local_GR" and row["status"] == "BLOCKED_NONCLAIM" for row in gates), "local-GR claim remains blocked")
    add("VAL3675_11_doc_written", "not signed yet" in doc_text and "c_FXR" in doc_text and "SIG3675_0..4" in doc_text, "doc records unsigned zero and finite coefficient")
    add("VAL3675_12_no_formalization_leak", not leaks, "no 3675 checkpoint files in formalization-workbench")
    add("VAL3675_13_next_target", next_target[0]["target_doc"].startswith("3676-") and "no-natural-marker" in next_target[0]["target_doc"], "3676 no-natural-marker target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    signatures = signature_audit_rows(ts)
    coefficients = finite_coefficient_rows(ts)
    bounds = finite_bound_rows(ts)
    routes = blocker_or_source_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, bounds)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3675_SOURCE_REGISTER.csv",
        "signatures": RESIDUALS / "P8_Y5_R2FR_3675_NO_FXR_SIGNATURE_AUDIT.csv",
        "coefficients": RESIDUALS / "P8_Y5_R2FR_3675_FINITE_FXR_COEFFICIENT_SOURCE_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3675_FINITE_CFXR_BOUND_ROWS.csv",
        "routes": RESIDUALS / "P8_Y5_R2FR_3675_BLOCKER_OR_SOURCE_ROUTES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3675_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3675_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3675_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3675_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3675_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["signatures"], signatures)
    write_csv(outputs["coefficients"], coefficients)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["routes"], routes)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, signatures, coefficients, bounds, routes, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, signatures, coefficients, bounds, routes, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3675 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3675 checkpoint with {len(validation)} validation checks; no-FXR signature unsigned, finite c_FXR rows staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
