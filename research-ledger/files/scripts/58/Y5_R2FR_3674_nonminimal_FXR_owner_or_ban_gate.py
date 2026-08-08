from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3674"
BRANCH_ID = "MTS_R2FR_Y5_NONMINIMAL_FXR_OWNER_OR_BAN_GATE_3674"
DOC = ROOT / "3674-Y5-R2FR-nonminimal-FXR-owner-or-ban-gate.md"


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
        ("handoff_3673", RESIDUALS / "P8_Y5_R2FR_3673_NEXT_TARGET.csv", "nonminimal-FXR", "3673 selected F(X)R gate"),
        ("doc_3673", ROOT / "3673-Y5-R2FR-parent-action-Hessian-STF-operator-location.md", "k_H_geo = - A_H F0_prime", "F(X)R owner derivation"),
        ("fxr_3673", RESIDUALS / "P8_Y5_R2FR_3673_FXR_OWNER_DERIVATION_ROWS.csv", "FXR3673_3_ban_gives_zero", "allow/ban derivation rows"),
        ("bounds_3672", RESIDUALS / "P8_Y5_R2FR_3672_DUAL_BRANCH_BOUND_ROWS.csv", "GB3672_eta_100_zeta_215.032", "inherited xiH bound rows"),
        ("doc_1022", ROOT / "1022-Y5-R10-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md", "S_parent=S_red[q(Phi)]", "vertical quotient action descent contract"),
        ("audit_1037", RESIDUALS / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv", "NP1037_1_action_descent", "no physical X pole audit"),
        ("doc_964", ROOT / "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md", "marker-prefactor `F(sigma)R`", "minimality theorem failure and F(sigma)R countermodel"),
        ("minimality_964", RESIDUALS / "P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv", "MIN964_4_descent_signature", "minimality theorem requirements"),
        ("contract_990", RESIDUALS / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", "PAC990_1_gravity_operator", "parent gravity operator contract"),
        ("vertex_1048", RESIDUALS / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv", "PVS1048_0_field_domain", "allowed local operator list requirement"),
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


def quotient_descent_ban_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "QDB3674_0_vertical_X",
            "X is vertical to observed quotient",
            "q:Phi->g_obs/e_obs is parent-defined before variation and Dq[v_X]=0.",
            "Lie_vX g_obs = 0",
            "CONDITIONAL_FROM_1022_1037_NOT_SIGNED",
        ),
        (
            "QDB3674_1_grav_action_descent",
            "gravity action descends through q",
            "S_grav[Phi]=S_EH[q(Phi)] + fixed boundary/topological terms; no independent X argument in the curvature operator.",
            "Lie_vX S_grav = 0 before variation",
            "CONDITIONAL_ACTION_DESCENT_NOT_SIGNED",
        ),
        (
            "QDB3674_2_no_FXR_slot",
            "no nonminimal curvature prefactor",
            "The parent operator grammar forbids F(X)R, F(Xhat)R, R f(marker), improvement-stress equivalents, and post-readout Hessian slots.",
            "F0_prime=0 for every vertical X direction",
            "MISSING_PARENT_OPERATOR_BAN",
        ),
        (
            "QDB3674_3_no_integrated_out_return",
            "no hidden integrated-out equivalent",
            "Auxiliary/projector/memory sectors do not regenerate an effective F_eff(X)R, R Box^-1 R, or scalar-tensor pole after solving their equations.",
            "Delta S_eff[g,X] has no linear R*X or R*F(X) term",
            "MISSING_NO_REENTRY_THEOREM",
        ),
        (
            "QDB3674_4_boundary_readout_silence",
            "no readout or boundary Hessian re-entry",
            "The observed rods/clocks/light metric is q(Phi) only through the same quotient, with no A(X)g_obs or boundary improvement that reintroduces P_TF nabla_i nabla_j X.",
            "Dg_readout[v_X]=0 and B_Hessian=0",
            "MISSING_READOUT_BOUNDARY_BAN",
        ),
        (
            "QDB3674_5_ban_theorem",
            "conditional k_H_geo zero theorem",
            "QDB3674_0 through QDB3674_4 imply the F(X)R owner is absent and the geometric Hessian-STF coefficient vanishes.",
            "k_H_geo = -A_H F0_prime/(1+A_H F0) = 0",
            "THEOREM_DERIVED_CONDITIONAL_NOT_CURRENT_CLAIM",
        ),
    ]
    return [
        {
            **base(ts),
            "ban_id": ban_id,
            "clause": clause,
            "statement": statement,
            "formula": formula,
            "status": status,
            "claim_allowed": False,
        }
        for ban_id, clause, statement, formula, status in specs
    ]


def fxr_coefficient_template_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "FXRC3674_0_allowed_branch",
            "allowed F(X)R branch",
            "S_H=(M_*^2/2) int sqrt(-g) A_H F(X)R",
            "k_H_geo=-A_H*F0_prime/(1+A_H*F0)",
            "A_H;F0;F0_prime;parent field normalization;equation-side sign",
            "MISSING_PARENT_COEFFICIENTS",
        ),
        (
            "FXRC3674_1_banned_branch",
            "banned F(X)R branch",
            "S_grav=S_EH[q(Phi)] and no independent X curvature prefactor",
            "k_H_geo=0",
            "q map; vertical generator; action descent; no marker; no re-entry",
            "CONDITIONAL_ZERO_IF_BAN_SIGNED",
        ),
        (
            "FXRC3674_2_improvement_branch",
            "improved stress equivalent",
            "T_ij -> T_ij + (nabla_i nabla_j - g_ij Box)U(X)",
            "k_H_geo-equivalent=-U0_prime in normalized units unless moved to geometry",
            "U0_prime;matter improvement owner;Bianchi/current chain",
            "MISSING_IMPROVEMENT_OWNER",
        ),
        (
            "FXRC3674_3_readout_branch",
            "post-variation readout Hessian",
            "g_readout=g_obs + H(X)_{ij}^{TF} or derivative frame term",
            "effective k_H_readout from Dg_readout[v_X]",
            "readout parent functor;clock/light rods;boundary silence",
            "MISSING_READOUT_OWNER",
        ),
    ]
    return [
        {
            **base(ts),
            "template_id": template_id,
            "branch": branch,
            "parent_form": parent_form,
            "coefficient_formula": coefficient_formula,
            "required_inputs": required_inputs,
            "status": status,
            "claim_allowed": False,
        }
        for template_id, branch, parent_form, coefficient_formula, required_inputs, status in specs
    ]


def inherited_fxr_bound_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in load_csv(RESIDUALS / "P8_Y5_R2FR_3672_DUAL_BRANCH_BOUND_ROWS.csv"):
        rows.append(
            {
                **base(ts),
                "bound_id": str(row["bound_id"]).replace("GB3672", "FXRB3674"),
                "source_bound_id": row["bound_id"],
                "kernel_id": row["kernel_id"],
                "xi_H_max": row["xi_H_max"],
                "fxr_allowed_bound": f"|A_H*F0_prime/(1+A_H*F0) * f_EM/Z_X| <= {row['xi_H_max']}",
                "fxr_banned_value": "0 if QDB3674_0..4 are parent-signed",
                "stress_fallback_bound": row["stress_bound"],
                "status": "INHERITED_BOUND_TEMPLATE_NONCLAIM",
                "why_nonclaim": "F(X)R coefficient, ban theorem, f_EM/Z_X, boundary/readout floors, and quadratic/direct-TF floors remain unsigned",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def countermodel_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "CM3674_0_marker_prefactor",
            "marker/scalar curvature prefactor",
            "S=int sqrt(-g) F(sigma_marker)R + S_sigma",
            "generates the same Hessian-STF owner unless sigma_marker/X is banned or quotient-descended",
            "LIVE_FROM_964",
        ),
        (
            "CM3674_1_auxiliary_scalar",
            "auxiliary scalar integrated out",
            "S=S_EH+int sqrt(-g)[-M^2 phi^2/2 + beta phi R]",
            "can regenerate f(R)/scalar-tensor response after solving phi unless no-reentry is proven",
            "LIVE_FROM_964",
        ),
        (
            "CM3674_2_improved_stress",
            "improved stress tensor",
            "T_ij -> T_ij + (nabla_i nabla_j-g_ij Box)U(X)",
            "can place Hessian-STF on the apparent RHS while being equivalent to nonminimal geometry",
            "LIVE_UNLESS_STRESS_GRAMMAR_BANNED",
        ),
        (
            "CM3674_3_readout_frame",
            "post-variation readout frame",
            "g_readout=A(X)^2 g_obs + derivative/disformal terms",
            "can reintroduce observed gamma slip even if the field equation bans F(X)R",
            "LIVE_UNLESS_READOUT_DESCENT_SIGNED",
        ),
    ]
    return [
        {
            **base(ts),
            "countermodel_id": countermodel_id,
            "countermodel": countermodel,
            "form": form,
            "effect": effect,
            "status": status,
            "claim_allowed": False,
        }
        for countermodel_id, countermodel, form, effect, status in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3674_0_ban_theorem_shape", "quotient-descent ban theorem shape", "PASS_CONDITIONAL_DERIVATION", "if q/action/readout descent and no-reentry clauses close, k_H_geo=0"),
        ("CG3674_1_ban_theorem_current", "current ban theorem", "BLOCKED_PARENT_SIGNATURE", "descent/no-marker/no-reentry/readout clauses are not all signed"),
        ("CG3674_2_allowed_coefficient", "allowed F(X)R coefficient", "BLOCKED_PARENT_COEFFICIENTS", "A_H,F0,F0_prime not source-owned"),
        ("CG3674_3_countermodels", "countermodel retention", "PASS_GUARDRAIL", "marker prefactor, auxiliary scalar, improved stress, readout frame retained"),
        ("CG3674_4_gamma_claim", "Cassini/local-GR claim", "BLOCKED_NONCLAIM", "no k_H zero or finite F(X)R coefficient is claimable"),
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
            "status": "FXR_BAN_THEOREM_DERIVED_CONDITIONAL_COUNTERMODELS_RETAINED",
            "summary": "3674 derives the exact quotient-descent ban theorem for the F(X)R Hessian-STF owner: if gravity and readout descend only through q and no marker/improvement/reentry slot exists, then F0_prime=0 and k_H_geo=0. Current files do not sign all clauses, so the finite F(X)R branch remains as a nonclaim bound template.",
            "claim_ceiling": "no k_H zero, finite F(X)R coefficient, Cassini/gamma, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": f"Strongest inherited F(X)R bound template is {strongest['fxr_allowed_bound']}; banned route gives zero only if QDB3674_0..4 are signed.",
            "next_missing_piece": "source the parent q/action/readout descent signature, or source A_H,F0,F0_prime for the finite F(X)R branch",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3674_0",
            "target_doc": "3675-Y5-R2FR-quotient-descent-no-FXR-signature-or-finite-coefficient-source.md",
            "target_script": "scripts/Y5_R2FR_3675_quotient_descent_no_FXR_signature_or_finite_coefficient_source.py",
            "objective": "try to sign the quotient/action/readout descent clauses that ban F(X)R and give k_H_geo=0; if not, build explicit finite A_H,F0,F0_prime source/coefficient rows without claiming local GR",
            "success_gate": "either QDB3674_0..4 are source-signed, or the finite F(X)R branch has explicit parent coefficient placeholders and bound rows with no claim leakage",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    ban_rows: list[dict[str, object]],
    templates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    countermodels: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    strongest = min(bounds, key=lambda row: float(row["xi_H_max"]))
    lines = [
        "# 3674 - Nonminimal F(X)R owner or ban gate",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "The conditional ban theorem is now explicit:",
        "",
        "`Dq[v_X]=0`, `S_grav[Phi]=S_EH[q(Phi)] + boundary/topological`, no `F(X)R`/improvement/readout re-entry",
        "",
        "implies",
        "",
        "`Lie_vX S_grav=0`, `F0_prime=0`, and therefore `k_H_geo=-A_H F0_prime/(1+A_H F0)=0`.",
        "",
        "This is the cleanest local-GR route, but it is not currently signed because the corpus still allows marker-prefactor, auxiliary scalar, improved-stress, and readout-frame countermodels unless the parent signature closes them.",
        "",
        f"Strongest inherited finite-branch template: `{strongest['fxr_allowed_bound']}`.",
        "",
        "## Quotient-descent ban rows",
    ]
    for row in ban_rows:
        lines.append(f"- `{row['ban_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## F(X)R coefficient templates"])
    for row in templates:
        lines.append(f"- `{row['template_id']}`: {row['status']} - `{row['coefficient_formula']}`")
    lines.extend(["", "## Inherited F(X)R bound rows"])
    for row in bounds[:5]:
        lines.append(f"- `{row['bound_id']}`: `{row['fxr_allowed_bound']}`; banned value `{row['fxr_banned_value']}`")
    lines.extend(["", "## Countermodels"])
    for row in countermodels:
        lines.append(f"- `{row['countermodel_id']}`: {row['status']} - {row['countermodel']}")
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
    ban_rows: list[dict[str, object]],
    templates: list[dict[str, object]],
    bounds: list[dict[str, object]],
    countermodels: list[dict[str, object]],
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
    generated = sources + ban_rows + templates + bounds + countermodels + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3674*", "3674-Y5-R2FR-*", "P8_Y5*3674*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3674_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3674_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3674_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3674 outputs written")
    add("VAL3674_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3674_4_ban_theorem", {"QDB3674_0_vertical_X", "QDB3674_1_grav_action_descent", "QDB3674_2_no_FXR_slot", "QDB3674_5_ban_theorem"}.issubset({str(row["ban_id"]) for row in ban_rows}), "ban theorem clauses present")
    add("VAL3674_5_templates", {"FXRC3674_0_allowed_branch", "FXRC3674_1_banned_branch", "FXRC3674_2_improvement_branch", "FXRC3674_3_readout_branch"}.issubset({str(row["template_id"]) for row in templates}), "allowed/banned/improvement/readout templates present")
    add("VAL3674_6_bounds", len(bounds) == len(load_csv(RESIDUALS / "P8_Y5_R2FR_3672_DUAL_BRANCH_BOUND_ROWS.csv")) and all("A_H*F0_prime" in row["fxr_allowed_bound"] for row in bounds), "inherited F(X)R bound templates generated")
    add("VAL3674_7_countermodels", {"CM3674_0_marker_prefactor", "CM3674_1_auxiliary_scalar", "CM3674_2_improved_stress", "CM3674_3_readout_frame"}.issubset({str(row["countermodel_id"]) for row in countermodels}), "countermodels retained")
    add("VAL3674_8_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3674_9_claim_gates", any(row["claim_gate_id"] == "CG3674_4_gamma_claim" and row["status"] == "BLOCKED_NONCLAIM" for row in gates), "gamma/local-GR claim remains blocked")
    add("VAL3674_10_doc_written", "F0_prime=0" in doc_text and "k_H_geo" in doc_text and "countermodels" in doc_text, "doc records ban theorem and countermodels")
    add("VAL3674_11_no_formalization_leak", not leaks, "no 3674 checkpoint files in formalization-workbench")
    add("VAL3674_12_next_target", next_target[0]["target_doc"].startswith("3675-") and "no-FXR" in next_target[0]["target_doc"], "3675 no-FXR/coefficient target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    ban_rows = quotient_descent_ban_rows(ts)
    templates = fxr_coefficient_template_rows(ts)
    bounds = inherited_fxr_bound_rows(ts)
    countermodels = countermodel_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, bounds)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3674_SOURCE_REGISTER.csv",
        "ban": RESIDUALS / "P8_Y5_R2FR_3674_QUOTIENT_DESCENT_BAN_THEOREM_ROWS.csv",
        "templates": RESIDUALS / "P8_Y5_R2FR_3674_FXR_COEFFICIENT_TEMPLATE_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3674_INHERITED_FXR_BOUND_ROWS.csv",
        "countermodels": RESIDUALS / "P8_Y5_R2FR_3674_COUNTERMODEL_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3674_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3674_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3674_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3674_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["ban"], ban_rows)
    write_csv(outputs["templates"], templates)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["countermodels"], countermodels)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, ban_rows, templates, bounds, countermodels, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, ban_rows, templates, bounds, countermodels, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3674 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3674 checkpoint with {len(validation)} validation checks; F(X)R ban theorem conditional, finite branch retained")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
