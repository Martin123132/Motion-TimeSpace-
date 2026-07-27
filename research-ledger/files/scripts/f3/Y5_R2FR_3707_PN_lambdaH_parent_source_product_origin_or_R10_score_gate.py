from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3707"
BRANCH_ID = "MTS_R2FR_Y5_PN_LAMBDAH_PARENT_SOURCE_PRODUCT_ORIGIN_OR_R10_SCORE_GATE_3707"
DOC = ROOT / "3707-Y5-R2FR-PN-lambdaH-parent-source-product-origin-or-R10-score-gate.md"

DOC_3706 = ROOT / "3706-Y5-R2FR-parent-boundary-action-collar-signature-or-edge-budget-bound.md"
NEXT_3706 = RESIDUALS / "P8_Y5_R2FR_3706_NEXT_TARGET.csv"
PRODUCT_3703 = RESIDUALS / "P8_Y5_R2FR_3703_R10_PRODUCT_BOUND_ROWS.csv"
MISSING_3703 = RESIDUALS / "P8_Y5_R2FR_3703_MISSING_PARENT_INPUT_ROWS.csv"
REDUCED_3705 = RESIDUALS / "P8_Y5_R2FR_3705_REDUCED_BUDGET_ROWS.csv"
ETA_3706 = RESIDUALS / "P8_Y5_R2FR_3706_ETA_COMPONENT_BOUND_ROWS.csv"
DOC_3695 = ROOT / "3695-Y5-R2FR-parent-Hessian-kinetic-metric-source-extraction-for-muH.md"
MU_3695 = RESIDUALS / "P8_Y5_R2FR_3695_SYMBOLIC_MUH_ROWS.csv"
HESSIAN_3695 = RESIDUALS / "P8_Y5_R2FR_3695_HESSIAN_EXTRACTION_ROWS.csv"
CLOSURE_3695 = RESIDUALS / "P8_Y5_R2FR_3695_CLOSURE_BINDER_ROWS.csv"
SOURCE_STACK = RESIDUALS / "P8_source_normalized_Newton_branch_STACK.csv"
MEFF_THEOREM = RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"
KAPPA_STATUS = RESIDUALS / "P8_local_GR_kappa_G_Newtonian_gate_status.csv"
CURVE_STATUS_3702 = RESIDUALS / "P8_Y5_R2FR_3702_STATUS.csv"
CURVE_3702 = RESIDUALS / "P8_Y5_R2FR_3702_R10_BOUND_CURVE_CANDIDATE.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def sci(value: float) -> str:
    return f"{value:.12e}"


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3706", DOC_3706, "P_N and lambda_H", "3706 handoff to source-product score gate"),
        ("next_3706", NEXT_3706, "P_N and lambda_H", "declared 3707 target"),
        ("product_3703", PRODUCT_3703, "P_N_max(eta)", "R10 product-bound rows"),
        ("missing_3703", MISSING_3703, "K_N*rho_Newton", "missing parent input ledger"),
        ("reduced_3705", REDUCED_3705, "alpha_boundary_edge", "projection-clean reduced R10 gate"),
        ("eta_3706", ETA_3706, "eta_total_template", "boundary/edge eta component templates"),
        ("doc_3695", DOC_3695, "mu_H^2 = 2u_1", "parent Hessian/mass-gap derivation"),
        ("mu_3695", MU_3695, "lambda_H = 1/sqrt(mu_H^2)", "symbolic mu_H interface rows"),
        ("hessian_3695", HESSIAN_3695, "M_H,IJ = 2 u_1 G_H,IJ", "Hessian extraction rows"),
        ("closure_3695", CLOSURE_3695, "u_1(local)>0", "closure binder for mass-gap proof"),
        ("source_stack", SOURCE_STACK, "SN5_EH_to_Poisson_coefficient", "source-normalized Newton stack"),
        ("meff_theorem", MEFF_THEOREM, "M_eff[W]", "source measure / exterior flux theorem"),
        ("kappa_status", KAPPA_STATUS, "calibrated_baseline_not_derived", "local GR kappa/G status"),
        ("curve_status_3702", CURVE_STATUS_3702, "R10_CANDIDATE_CURVE", "candidate curve status"),
        ("curve_3702", CURVE_3702, "R10C3702_000", "candidate curve table"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append({
            **base(timestamp),
            "source_id": source_id,
            "role": role,
            "path": str(path),
            "needle": needle,
            "exists": exists,
            "needle_found": needle in text if exists else False,
            "claim_allowed": False,
        })
    return rows


def parent_input_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        {
            **base(timestamp),
            "input_id": "PIN3707_0_muH_lambdaH",
            "quantity": "lambda_H=1/mu_H",
            "parent_formula": "mu_H^2 = 2u_1 + lambda_min(G_H^{-1/2}S_corrG_H^{-1/2}) - R_domain - R_source_slope",
            "score_gate": "choose lambda_H from parent; evaluate alpha_bound_R10(lambda_H) without fitting lambda_H",
            "required_parent_coefficients": "u_1(local), positive G_H, S_corr eigenbound, R_domain, R_source_slope, local branch/environment labels",
            "current_evidence": "3695 derives symbolic Hessian/mass-gap route but u_1 value/origin and correction bounds are unsigned",
            "status": "SYMBOLIC_PARENT_ORIGIN_FOUND_NUMERIC_VALUE_MISSING",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "input_id": "PIN3707_1_P_N",
            "quantity": "P_N",
            "parent_formula": "P_N := K_N*rho_Newton*C_H^2||J_y+B_y||^2",
            "score_gate": "P_N <= 2*(1-eta_boundary-eta_edge)*alpha_bound_R10(lambda_H)/lambda_H^4",
            "required_parent_coefficients": "K_N, rho_Newton normalization, C_H horizontal Green constant, J_y source norm, B_y residual/boundary source norm",
            "current_evidence": "3703 compressed R10 to one source product but parent-owned factors are not numeric",
            "status": "SOURCE_PRODUCT_ISOLATED_NUMERIC_FACTORS_MISSING",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "input_id": "PIN3707_2_eta_total",
            "quantity": "eta_R10=eta_boundary+eta_edge",
            "parent_formula": "alpha_boundary_edge <= eta_R10*alpha_bound_R10(lambda_H)",
            "score_gate": "0 <= eta_R10 < 1; score table uses eta=0,0.1,0.5 templates only",
            "required_parent_coefficients": "boundary no-flux zero or finite B_boundary; edge support/readout zero or finite B_edge and alpha_edge",
            "current_evidence": "projection eta is zero on the branch; boundary and edge are only templates after 3706",
            "status": "PROJECTION_CLEAN_BOUNDARY_EDGE_OPEN",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "input_id": "PIN3707_3_curve",
            "quantity": "alpha_bound_R10(lambda)",
            "parent_formula": "external experimental bound curve, not a parent coefficient",
            "score_gate": "candidate curve allowed for private smoke only; claim needs official table or manually reviewed digitization",
            "required_parent_coefficients": "none; requires source-backed curve review and provenance",
            "current_evidence": "3702 candidate curve reproduces 38.6 um alpha=1 anchor but remains nonclaim",
            "status": "CANDIDATE_CURVE_SMOKE_ONLY",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "input_id": "PIN3707_4_source_normalization",
            "quantity": "Newton/source denominator",
            "parent_formula": "M_eff[W] = M_source[W] = integral_S Q_M[tau] = (4*pi*G_ref)^-1 integral_S Pi_M J_H",
            "score_gate": "P_N and rho_Newton are meaningful only after the same Hilbert/source mass-current object is identified",
            "required_parent_coefficients": "observed frame, source projector Pi_M, observed-time Hamiltonian charge, closed exterior mass flux, no extra source channels",
            "current_evidence": "source-normalized Newton stack and Meff theorem are conditional; kappa_GN remains calibrated baseline",
            "status": "SOURCE_DENOMINATOR_NOT_PARENT_LOCKED",
            "claim_allowed": False,
        },
    ]
    return rows


def score_gate_rows(timestamp: str, reduced_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index, row in enumerate(reduced_rows):
        lambda_m = float(row["lambda_m"])
        alpha_bound = float(row["alpha_bound_abs"])
        mu_h = 1.0 / lambda_m
        mu_h_sq = mu_h * mu_h
        u1_clean_required = 0.5 * mu_h_sq
        p_max_eta0 = 2.0 * alpha_bound / (lambda_m ** 4)
        p_max_eta01 = 0.9 * p_max_eta0
        p_max_eta05 = 0.5 * p_max_eta0
        rows.append({
            **base(timestamp),
            "score_id": f"R10SG3707_{index:03d}",
            "source_reduced_budget_id": row["reduced_budget_id"],
            "lambda_m": sci(lambda_m),
            "lambda_um": f"{lambda_m * 1e6:.6f}",
            "mu_H_m_inv": sci(mu_h),
            "mu_H_sq_m2": sci(mu_h_sq),
            "u1_clean_required_m2": sci(u1_clean_required),
            "alpha_bound_abs": sci(alpha_bound),
            "P_N_max_eta0_m4": sci(p_max_eta0),
            "P_N_max_eta10_m4": sci(p_max_eta01),
            "P_N_max_eta50_m4": sci(p_max_eta05),
            "sqrt_P_N_max_eta10_m2": sci(math.sqrt(p_max_eta01)),
            "clean_u1_formula": "u1_clean_required=1/(2*lambda_H^2) when S_corr=R_domain=R_source_slope=0",
            "general_u1_formula": "u1_required=0.5*(lambda_H^-2 - lambda_min_corr + R_domain + R_source_slope)",
            "score_formula": "P_N <= 2*(1-eta_boundary-eta_edge)*alpha_bound_R10(lambda_H)/lambda_H^4",
            "score_status": "EXECUTABLE_NONCLAIM_PARENT_PN_LAMBDAH_ETA_AND_CURVE_REVIEW_REQUIRED",
            "claim_allowed": False,
        })
    return rows


def anchor_rows(timestamp: str) -> list[dict[str, object]]:
    anchors = [
        ("ANCH3707_0_official_alpha1", 38.6e-6, 1.0, "official short-range alpha=1 threshold anchor quoted by 3702/3703; not a full curve"),
    ]
    rows = []
    for anchor_id, lambda_m, alpha_bound, provenance in anchors:
        mu_h = 1.0 / lambda_m
        p_eta0 = 2.0 * alpha_bound / (lambda_m ** 4)
        rows.append({
            **base(timestamp),
            "anchor_id": anchor_id,
            "lambda_m": sci(lambda_m),
            "lambda_um": f"{lambda_m * 1e6:.6f}",
            "mu_H_m_inv": sci(mu_h),
            "mu_H_sq_m2": sci(mu_h * mu_h),
            "u1_clean_required_m2": sci(0.5 * mu_h * mu_h),
            "alpha_bound_abs": sci(alpha_bound),
            "P_N_max_eta0_m4": sci(p_eta0),
            "P_N_max_eta10_m4": sci(0.9 * p_eta0),
            "P_N_max_eta50_m4": sci(0.5 * p_eta0),
            "provenance": provenance,
            "claim_allowed": False,
        })
    return rows


def obstruction_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("OBS3707_0_muH", "lambda_H/mu_H", "derive numeric positive mu_H^2 from u_1, G_H, S_corr, R_domain and R_source_slope", "R10 range must be inherited, not fit"),
        ("OBS3707_1_PN", "P_N", "derive or bound K_N*rho_Newton*C_H^2||J_y+B_y||^2", "R10 amplitude must be a source product, not an adjustable alpha"),
        ("OBS3707_2_eta", "eta_boundary+eta_edge", "prove boundary/edge zeros or source finite eta values", "nuisance can consume the bound"),
        ("OBS3707_3_curve", "alpha_bound_R10(lambda)", "promote candidate digitization to reviewed/official bound curve", "current curve is private smoke data"),
        ("OBS3707_4_source_mass", "rho_Newton/M_eff source denominator", "lock observed frame, Hilbert current, Hamiltonian charge and closed mass flux", "P_N normalization is physically meaningful only after source mass identity"),
    ]
    return [
        {
            **base(timestamp),
            "obstruction_id": obstruction_id,
            "quantity": quantity,
            "needed_action": needed_action,
            "why_it_matters": why_it_matters,
            "status": "REQUIRED_BEFORE_R10_OR_LOCAL_GR_CLAIM",
            "claim_allowed": False,
        }
        for obstruction_id, quantity, needed_action, why_it_matters in specs
    ]


def decision_rows(timestamp: str, score_rows_: list[dict[str, object]]) -> list[dict[str, object]]:
    tightest = min(score_rows_, key=lambda row: float(row["P_N_max_eta10_m4"]))
    return [
        {
            **base(timestamp),
            "decision_id": "DEC3707_0_score_gate_built",
            "decision": "R10 gate is now a scoreable parent-coefficient contract, not a free alpha(lambda) fit",
            "rationale": "Given parent lambda_H, parent P_N and eta_boundary+eta_edge, the inequality is one line and uses the candidate curve table.",
            "status": "EXECUTABLE_NONCLAIM_GATE",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3707_1_u1_range_exposed",
            "decision": "The clean local mass-gap coefficient required by any lambda_H is explicitly u_1=1/(2lambda_H^2)",
            "rationale": "This makes the mu_H route attackable from the parent relaxation/fixed-point functional instead of treating lambda_H as phenomenology.",
            "status": "DERIVED_CLEAN_BRANCH_REQUIREMENT",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3707_2_tightest_candidate_row",
            "decision": f"Tightest eta=0.1 candidate row is lambda={tightest['lambda_um']} um with P_N_max={tightest['P_N_max_eta10_m4']} m^-4",
            "rationale": "This is a private smoke lower-envelope value; it is useful for stress-testing parent coefficients only.",
            "status": "PRIVATE_SMOKE_BOUND_ONLY",
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "decision_id": "DEC3707_3_next_target",
            "decision": "Next attack should derive u_1/local mass-gap from the parent relaxation/fixed-point functional before trying another broad audit",
            "rationale": "lambda_H controls both R10 and the local-GR shield; P_N scoring is useless until the range is parent-owned.",
            "status": "ADVANCE_TO_U1_ORIGIN",
            "claim_allowed": False,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3707_0_muH", "mu_H^2 numeric/positive and parent-derived for the local branch"),
        ("CG3707_1_PN", "P_N numeric or upper-bounded from parent source coefficients"),
        ("CG3707_2_eta", "eta_boundary+eta_edge theorem-zero or finite source value"),
        ("CG3707_3_curve", "R10 bound curve official/reviewed, not private candidate"),
        ("CG3707_4_source_norm", "rho_Newton and source mass/current normalization parent-locked"),
        ("CG3707_5_score", "P_N <= 2*(1-eta)*alpha_bound/lambda_H^4 is evaluated at parent lambda_H"),
        ("CG3707_6_public", "public R10/local-GR claim allowed"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": "BLOCKED",
            "claim_allowed": False,
        }
        for gate_id, requirement in specs
    ]


def status_rows(timestamp: str, score_rows_: list[dict[str, object]], anchor_rows_: list[dict[str, object]]) -> list[dict[str, object]]:
    tightest = min(score_rows_, key=lambda row: float(row["P_N_max_eta10_m4"]))
    anchor = anchor_rows_[0]
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3707_0",
            "status": "R10_SCORE_GATE_EXECUTABLE_BUT_NONCLAIM_PARENT_COEFFICIENTS_MISSING",
            "summary": (
                "3707 converts the remaining R10/local-screening problem into an explicit score gate. "
                "The gate is P_N <= 2*(1-eta_boundary-eta_edge)*alpha_bound(lambda_H)/lambda_H^4 with "
                "lambda_H=1/mu_H and clean-branch u_1=1/(2lambda_H^2). "
                f"The official alpha=1 anchor implies P_N_max_eta0={anchor['P_N_max_eta0_m4']} m^-4 and "
                f"u1_clean={anchor['u1_clean_required_m2']} m^-2 at lambda=38.6 um. "
                f"The tightest private candidate eta=0.1 row is lambda={tightest['lambda_um']} um and P_N_max={tightest['P_N_max_eta10_m4']} m^-4."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3707_0",
            "target_doc": "3708-Y5-R2FR-u1-parent-relaxation-functional-origin-or-local-mass-gap-closure.md",
            "target_script": "scripts/Y5_R2FR_3708_u1_parent_relaxation_functional_origin_or_local_mass_gap_closure.py",
            "objective": "derive u_1(local) from the parent relaxation/fixed-point functional, or demote lambda_H to an explicit closure coefficient feeding the R10/PPN score gates",
            "success_gate": "u_1, correction lower bounds, and mu_H^2 are parent-derived/bounded enough to choose lambda_H without fitting it to R10",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    parent_inputs: list[dict[str, object]],
    score_rows_: list[dict[str, object]],
    anchors: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    tightest = min(score_rows_, key=lambda row: float(row["P_N_max_eta10_m4"]))
    anchor = anchors[0]
    lines = [
        "# 3707 Y5 R2FR P_N lambda_H Parent Source Product Origin Or R10 Score Gate",
        "",
        "Private checkpoint. No GitHub action. No public claim.",
        "",
        "## Status",
        "",
        f"- `{status[0]['status']}`",
        f"- {status[0]['summary']}",
        "",
        "## Main Result",
        "",
        "- The R10 branch is no longer a vague `alpha(lambda)` question; it is a parent-coefficient score gate.",
        "- Define `P_N := K_N*rho_Newton*C_H^2||J_y+B_y||^2`, `lambda_H:=1/mu_H`, and `eta:=eta_boundary+eta_edge`.",
        "- The reduced R10 score condition is `P_N <= 2*(1-eta)*alpha_bound_R10(lambda_H)/lambda_H^4`.",
        "- The clean even-scalar local gap gives `mu_H^2=2u_1`, hence `u_1(lambda_H)=1/(2lambda_H^2)` before correction terms.",
        "- The corrected branch is `u_1 >= 0.5*(lambda_H^-2 - lambda_min_corr + R_domain + R_source_slope)`.",
        "- This is still nonclaim because `u_1`, `P_N`, boundary/edge `eta`, and the reviewed R10 curve are not parent/source owned yet.",
        "",
        "## Anchor Consequence",
        "",
        f"- At the `alpha=1`, `lambda=38.6 um` anchor: `mu_H={anchor['mu_H_m_inv']} m^-1`, `u1_clean={anchor['u1_clean_required_m2']} m^-2`, `P_N_max_eta0={anchor['P_N_max_eta0_m4']} m^-4`, `P_N_max_eta10={anchor['P_N_max_eta10_m4']} m^-4`.",
        "",
        "## Candidate Curve Score Table",
        "",
        f"- Candidate score rows generated: `{len(score_rows_)}`.",
        f"- Tightest private candidate eta=0.1 row: `lambda={tightest['lambda_um']} um`, `P_N_max={tightest['P_N_max_eta10_m4']} m^-4`, `u1_clean={tightest['u1_clean_required_m2']} m^-2`.",
        "- Every row is `valid_for_claim=false`; the table is a smoke/stress gate for future parent coefficients.",
        "",
        "## Parent Inputs",
        "",
    ]
    for row in parent_inputs:
        lines.append(f"- `{row['input_id']}` `{row['quantity']}`: `{row['status']}` | {row['parent_formula']}")
    lines.extend(["", "## Remaining Obstructions", ""])
    for row in obstructions:
        lines.append(f"- `{row['obstruction_id']}` `{row['quantity']}`: {row['needed_action']}")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']}")
    lines.extend(["", "## Claim Gates", ""])
    for row in claim_gates:
        lines.append(f"- `{row['claim_gate_id']}`: `{row['status']}` | {row['requirement']}")
    lines.extend(["", "## Source Register", ""])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: exists={row['exists']} needle_found={row['needle_found']} path=`{row['path']}`")
    lines.extend(["", "## Next Target", ""])
    lines.append(f"- `{next_target[0]['target_doc']}`")
    lines.append(f"- Objective: {next_target[0]['objective']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    generated_paths: list[Path],
    sources: list[dict[str, object]],
    parent_inputs: list[dict[str, object]],
    score_rows_: list[dict[str, object]],
    anchors: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    timestamp = stamp()
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("sources_exist", "all cited local sources exist", all(bool(row["exists"]) for row in sources), ""))
    checks.append(("needles_found", "all source needles found", all(bool(row["needle_found"]) for row in sources), ""))
    checks.append(("outputs_exist", "all generated paths exist", all(path.exists() for path in generated_paths), ""))
    csv_parse_ok = True
    csv_error = ""
    try:
        for path in [path for path in generated_paths if path.suffix.lower() == ".csv"]:
            if not parse_csv(path):
                csv_parse_ok = False
                csv_error = f"empty csv: {path}"
                break
    except Exception as exc:  # pragma: no cover
        csv_parse_ok = False
        csv_error = str(exc)
    checks.append(("csv_parse", "all generated CSV files parse and are nonempty", csv_parse_ok, csv_error))
    checks.append(("parent_inputs", "all core parent inputs are represented", {row["quantity"] for row in parent_inputs} >= {"lambda_H=1/mu_H", "P_N", "eta_R10=eta_boundary+eta_edge", "alpha_bound_R10(lambda)"}, ""))
    checks.append(("score_rows", "score rows preserve 3705 curve count and positive bounds", len(score_rows_) == 67 and all(float(row["P_N_max_eta10_m4"]) > 0 and float(row["u1_clean_required_m2"]) > 0 for row in score_rows_), f"rows={len(score_rows_)}"))
    checks.append(("score_formula", "score formula is present in every score row", all("P_N <=" in row["score_formula"] and "lambda_H^4" in row["score_formula"] for row in score_rows_), ""))
    checks.append(("anchor", "official alpha=1 anchor consequence is positive and nonclaim", len(anchors) == 1 and float(anchors[0]["P_N_max_eta0_m4"]) > 0 and anchors[0]["claim_allowed"] is False, ""))
    checks.append(("obstructions", "single obstruction set contains muH, PN, eta, curve and source mass", {row["quantity"] for row in obstructions} >= {"lambda_H/mu_H", "P_N", "eta_boundary+eta_edge", "alpha_bound_R10(lambda)", "rho_Newton/M_eff source denominator"}, ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3708", "next target advances to u1 origin", str(next_target[0]["target_doc"]).startswith("3708-") and "u1" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains score gate and u1 derivation", all(term in doc_text for term in ["P_N <=", "u_1(lambda_H)=1/(2lambda_H^2)", "valid_for_claim=false", "38.6 um"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3707*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3707 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
    return [
        {
            **base(timestamp),
            "validation_id": check_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": details,
        }
        for check_id, description, passed, details in checks
    ]


def main() -> int:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    reduced = parse_csv(REDUCED_3705)
    sources = source_register(timestamp)
    parent_inputs = parent_input_rows(timestamp)
    scores = score_gate_rows(timestamp, reduced)
    anchors = anchor_rows(timestamp)
    obstructions = obstruction_rows(timestamp)
    decisions = decision_rows(timestamp, scores)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, scores, anchors)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3707_SOURCE_REGISTER.csv",
        "parent_inputs": RESIDUALS / "P8_Y5_R2FR_3707_PARENT_INPUT_AUDIT_ROWS.csv",
        "scores": RESIDUALS / "P8_Y5_R2FR_3707_R10_SCORE_GATE_ROWS.csv",
        "anchors": RESIDUALS / "P8_Y5_R2FR_3707_OFFICIAL_ANCHOR_SCORE_ROWS.csv",
        "obstructions": RESIDUALS / "P8_Y5_R2FR_3707_OBSTRUCTION_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3707_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3707_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3707_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3707_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3707_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["parent_inputs"], parent_inputs)
    write_csv(outputs["scores"], scores)
    write_csv(outputs["anchors"], anchors)
    write_csv(outputs["obstructions"], obstructions)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, parent_inputs, scores, anchors, obstructions, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, parent_inputs, scores, anchors, obstructions, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3707 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3707 checkpoint: R10 score gate executable; parent P_N/lambda_H/u1 inputs isolated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
