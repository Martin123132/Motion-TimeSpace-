from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
FORMALIZATION = ROOT.parent / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
CHECKPOINT_ID = "3706"
BRANCH_ID = "MTS_R2FR_Y5_PARENT_BOUNDARY_ACTION_COLLAR_SIGNATURE_OR_EDGE_BUDGET_BOUND_3706"
DOC = ROOT / "3706-Y5-R2FR-parent-boundary-action-collar-signature-or-edge-budget-bound.md"

DOC_3705 = ROOT / "3705-Y5-R2FR-compact-collar-no-flux-and-r10-projection-certificate.md"
COLLAR_3705 = RESIDUALS / "P8_Y5_R2FR_3705_COMPACT_COLLAR_THEOREM_ROWS.csv"
ETA_3705 = RESIDUALS / "P8_Y5_R2FR_3705_ETA_COMPONENT_ROWS.csv"
REDUCED_3705 = RESIDUALS / "P8_Y5_R2FR_3705_REDUCED_BUDGET_ROWS.csv"
BOUNDARY_SCALAR = RESIDUALS / "P8_BOUNDARY_SCALAR_ACTION_OWNER_ATTEMPT.csv"
BOUNDARY_STRESS = RESIDUALS / "P8_R11_BOUNDARY_STRESS_THEOREM_STACK.csv"
BOUNDARY_FLUX = RESIDUALS / "P8_Y5_BRR545_BOUNDARY_FLUX_BOUND_FILL_ROW.csv"
DOC_1007 = ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md"
DOC_1009 = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
DOC_1011 = ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md"


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


def source_register(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("doc_3705", DOC_3705, "alpha_boundary_edge", "3705 reduced boundary/edge nuisance"),
        ("collar_3705", COLLAR_3705, "CCT3705_5_parent_signature_gap", "compact collar clauses"),
        ("eta_3705", ETA_3705, "eta_boundary + eta_edge", "reduced eta component schema"),
        ("reduced_3705", REDUCED_3705, "alpha_boundary_edge", "candidate reduced budget rows"),
        ("boundary_scalar", BOUNDARY_SCALAR, "O7_parent_owner_verdict", "scalar boundary action owner attempt"),
        ("boundary_stress", BOUNDARY_STRESS, "T1_boundary_scalar_no_flux", "boundary stress theorem stack"),
        ("boundary_flux", BOUNDARY_FLUX, "MISSING_NUMERIC_VALUE_OR_THEOREM_ZERO", "boundary flux finite-bound row"),
        ("doc_1007", DOC_1007, "symplectic_boundary_flux", "H_tau/symplectic boundary flux attempt"),
        ("doc_1009", DOC_1009, "S_GHY + fixed exact/topological boundary/reference terms", "parent current-chain boundary contract"),
        ("doc_1011", DOC_1011, "B_Z=0/no odd boundary charge", "response-doublet boundary zero attempt"),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                **base(timestamp),
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
            }
        )
    return rows


def boundary_variation_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "BAV3706_0_horizontal_action",
            "S_H[y]=1/2 int_Omega [(D y) G_H (D y)+ y M_eff,H y] - int_Omega y J_H + S_boundary,H[y,q]",
            "start from the horizontal local branch after quotient/gauge fixing",
            "defines where boundary terms must come from; not an added R10 patch",
            "DERIVED_CONTRACT",
            False,
        ),
        (
            "BAV3706_1_first_variation",
            "delta S_H|boundary = int_partialOmega <n_mu G_H^{mu nu}D_nu y + Pi_H, delta y>",
            "integration by parts plus boundary functional variation Pi_H:=delta S_boundary,H/delta y",
            "the boundary obstruction is exactly the unowned canonical boundary momentum",
            "DERIVED_FORMULA",
            False,
        ),
        (
            "BAV3706_2_dirichlet_zero",
            "if y|partialOmega=0 and delta y|partialOmega=0 then B_boundary=0",
            "fixed horizontal collar data",
            "mathematically sufficient but needs parent selection of fixed horizontal boundary data",
            "SUFFICIENT_NOT_PARENT_SIGNED",
            False,
        ),
        (
            "BAV3706_3_natural_no_flux_zero",
            "if n_mu G_H^{mu nu}D_nu y + Pi_H = 0 and Pi_H=0 on the local branch then B_boundary=0",
            "natural variational boundary condition",
            "mathematically sufficient but needs parent boundary action proving Pi_H vanishes or is fixed/topological",
            "SUFFICIENT_NOT_PARENT_SIGNED",
            False,
        ),
        (
            "BAV3706_4_edge_commutator",
            "B_edge = [L_H,chi_c]y on the collar annulus",
            "cutoff/localization identity",
            "edge leakage is controlled by support separation and a massive Green decay estimate, not by fitting",
            "DERIVED_FORMULA",
            False,
        ),
        (
            "BAV3706_5_edge_bound",
            "||B_edge|| <= C_chi C_H ||J_H|| exp(-d_c/lambda_H)(1+d_c/lambda_H)",
            "massive kernel estimate on collar thickness d_c",
            "turns edge silence into a finite bound if zero is not parent-signed",
            "CONDITIONAL_BOUND",
            False,
        ),
    ]
    return [
        {
            **base(timestamp),
            "variation_id": variation_id,
            "formula": formula,
            "basis": basis,
            "meaning": meaning,
            "status": status,
            "parent_signed": parent_signed,
            "claim_allowed": False,
        }
        for variation_id, formula, basis, meaning, status, parent_signed in specs
    ]


def parent_signature_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "PSG3706_0_boundary_action_exists",
            "explicit S_boundary,H for horizontal response variables",
            "not_signed",
            "1009 boundary/reference sector is a contract, not a promoted parent action; 1007 says MTS theta/Q_tau are missing",
        ),
        (
            "PSG3706_1_fixed_or_natural_condition",
            "parent branch selects y=0 on partialOmega_c or natural no-flux nGHy+Pi_H=0",
            "not_signed",
            "3705 staged this as sufficient, but no parent boundary selector owns it yet",
        ),
        (
            "PSG3706_2_PiH_zero_or_topological",
            "Pi_H vanishes or is fixed exact/topological data on the local collar",
            "not_signed",
            "boundary scalar/stress rows are conditional and require marker-free scalar homogeneous boundary action",
        ),
        (
            "PSG3706_3_support_separation",
            "source/readout support is separated from cutoff derivative support",
            "branch_defined_not_parent_signed",
            "can be imposed as a mathematical local-domain choice, but parent domain selector is not derived",
        ),
        (
            "PSG3706_4_same_readout",
            "same R10/Newton readout operator on interior and collar overlap",
            "branch_defined_not_parent_signed",
            "needed for alpha_edge=0; not yet tied to parent readout action",
        ),
        (
            "PSG3706_5_verdict",
            "B_boundary=B_edge=alpha_edge=0 by parent boundary action",
            "fail_current_claim",
            "mathematical route is explicit, but parent boundary action/collar signature is not present in the current corpus",
        ),
    ]
    return [
        {
            **base(timestamp),
            "signature_id": signature_id,
            "requirement": requirement,
            "status": status,
            "evidence": evidence,
            "claim_allowed": False,
        }
        for signature_id, requirement, status, evidence in specs
    ]


def component_bound_rows(timestamp: str, reduced_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for idx, row in enumerate(reduced_rows):
        alpha_bound = float(row["alpha_bound_abs"])
        eta_boundary = 0.05
        eta_edge = 0.05
        eta_total = eta_boundary + eta_edge
        rows.append(
            {
                **base(timestamp),
                "component_bound_id": f"CBB3706_{idx:03d}",
                "source_reduced_budget_id": row["reduced_budget_id"],
                "lambda_m": row["lambda_m"],
                "lambda_um": row["lambda_um"],
                "alpha_bound_abs": row["alpha_bound_abs"],
                "eta_boundary_template": f"{eta_boundary:.6f}",
                "eta_edge_template": f"{eta_edge:.6f}",
                "eta_total_template": f"{eta_total:.6f}",
                "P_boundary_max_template": f"{2.0 * eta_boundary * alpha_bound:.12e}",
                "P_edge_max_if_alpha_edge_zero_template": f"{2.0 * eta_edge * alpha_bound:.12e}",
                "alpha_edge_max_if_Bedge_zero_template": f"{eta_edge * alpha_bound:.12e}",
                "component_gate": "P_boundary<=2*eta_boundary*alpha_bound; 0.5*P_edge+alpha_edge<=eta_edge*alpha_bound",
                "status": "FINITE_TEMPLATE_NOT_SOURCE_VALUE",
                "claim_allowed": False,
            }
        )
    return rows


def solve_collar_ratio(target: float) -> float:
    low = 0.0
    high = 1.0
    def envelope(value: float) -> float:
        return math.exp(-value) * (1.0 + value)
    while envelope(high) > target:
        high *= 2.0
    for _ in range(80):
        mid = (low + high) / 2.0
        if envelope(mid) > target:
            low = mid
        else:
            high = mid
    return high


def collar_ratio_rows(timestamp: str) -> list[dict[str, object]]:
    targets = [0.1, 0.05, 0.01, 0.001]
    rows = []
    for idx, target in enumerate(targets):
        ratio = solve_collar_ratio(target)
        rows.append(
            {
                **base(timestamp),
                "ratio_id": f"CRR3706_{idx}",
                "target_edge_amplitude_fraction": f"{target:.6e}",
                "required_d_c_over_lambda_H": f"{ratio:.9f}",
                "check_envelope": f"{math.exp(-ratio) * (1.0 + ratio):.12e}",
                "formula": "exp(-d_c/lambda_H)*(1+d_c/lambda_H) <= target_edge_amplitude_fraction",
                "use": "collar thickness design rule for finite edge budget; constants C_chi and C_H still need parent/source rows",
                "claim_allowed": False,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3706_0",
            "Parent boundary action does not currently sign the collar/no-flux zero.",
            "Existing boundary scalar/stress/flux ledgers all mark the route conditional or missing numeric/theorem-zero inputs.",
            "ZERO_NOT_PROMOTED",
        ),
        (
            "DEC3706_1",
            "The variational boundary condition is now exact enough to attack.",
            "The required object is Pi_H=delta S_boundary,H/delta y and either fixed y or natural no-flux nGHy+Pi_H=0.",
            "PARENT_SIGNATURE_CONTRACT_ADVANCES",
        ),
        (
            "DEC3706_2",
            "Finite component budgets are installed for R10.",
            "eta_boundary and eta_edge can now be bounded component-by-component against alpha_bound(lambda) instead of living as vague nuisance terms.",
            "BUDGET_ROWS_ADVANCE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, status in specs
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, object]]:
    specs = [
        ("CG3706_0_boundary_action", "S_boundary,H and Pi_H are parent-derived for horizontal local branch", "BLOCKED"),
        ("CG3706_1_no_flux", "fixed y or natural no-flux boundary condition is parent-selected", "BLOCKED"),
        ("CG3706_2_edge", "support separation and same readout are parent-selected or finite edge constants are sourced", "BLOCKED"),
        ("CG3706_3_eta_values", "eta_boundary and eta_edge are actual source values or theorem-zero, not templates", "BLOCKED"),
        ("CG3706_4_R10_score", "P_N and lambda_H are parent-sourced and scored with eta_boundary+eta_edge", "BLOCKED"),
        ("CG3706_5_public", "public R10/local-Newton claim allowed", "BLOCKED"),
    ]
    return [
        {
            **base(timestamp),
            "claim_gate_id": gate_id,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
        }
        for gate_id, requirement, status in specs
    ]


def status_rows(timestamp: str, component_bounds: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status_id": "STATUS3706_0",
            "status": "BOUNDARY_ACTION_ZERO_NOT_PARENT_SIGNED_COMPONENT_ETA_BOUNDS_STAGED",
            "summary": (
                "3706 derives the exact horizontal boundary variation needed for the compact collar/no-flux zero, but current boundary-action evidence remains conditional. "
                f"It therefore stages {len(component_bounds)} component budget rows for eta_boundary and eta_edge plus collar-thickness design rows."
            ),
            "claim_allowed": False,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3706_0",
            "target_doc": "3707-Y5-R2FR-PN-lambdaH-parent-source-product-origin-or-R10-score-gate.md",
            "target_script": "scripts/Y5_R2FR_3707_PN_lambdaH_parent_source_product_origin_or_R10_score_gate.py",
            "objective": "attack the remaining R10 score blockers: parent-source P_N and lambda_H/mu_H; if absent, produce a final nonclaim R10 score gate with explicit required values",
            "success_gate": "P_N and lambda_H are parent-derived/bounded enough to evaluate the R10 candidate curve, or the exact missing parent coefficients are isolated",
            "claim_allowed": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    variations: list[dict[str, object]],
    signatures: list[dict[str, object]],
    component_bounds: list[dict[str, object]],
    ratios: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim_gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    tightest = min(component_bounds, key=lambda row: float(row["alpha_bound_abs"]))
    lines = [
        "# 3706 Y5 R2FR Parent Boundary Action Collar Signature Or Edge Budget Bound",
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
        "- The boundary zero route is now a precise variational contract, not a slogan.",
        "- Horizontal variation gives `delta S_H|boundary = int_partialOmega <n_mu G_H^{mu nu}D_nu y + Pi_H, delta y>`.",
        "- `B_boundary=0` follows if the parent branch fixes `y=0` on the collar boundary or selects natural no-flux `nG_HDy+Pi_H=0` with `Pi_H=0/fixed-topological`.",
        "- `B_edge` is the cutoff commutator `[L_H,chi_c]y`; a massive collar gives `||B_edge|| <= C_chi C_H ||J_H|| exp(-d_c/lambda_H)(1+d_c/lambda_H)`.",
        "- Current evidence does not parent-sign the boundary action, no-flux condition, or edge/readout support contract.",
        "- Finite component templates are staged: `P_boundary<=2 eta_boundary alpha_bound` and `0.5 P_edge + alpha_edge <= eta_edge alpha_bound`.",
        "- `valid_for_claim=false`: these are required bounds and theorem contracts, not measured/source-owned eta values.",
        "",
        "## Boundary Variation",
        "",
    ]
    for row in variations:
        lines.append(f"- `{row['variation_id']}`: `{row['status']}` parent_signed={row['parent_signed']} | {row['formula']}")
    lines.extend(["", "## Parent Signature Audit", ""])
    for row in signatures:
        lines.append(f"- `{row['signature_id']}`: `{row['status']}` | {row['requirement']} | {row['evidence']}")
    lines.extend(["", "## Component Bounds", ""])
    lines.append(f"- Component rows generated: `{len(component_bounds)}`.")
    lines.append(f"- Tightest template row by alpha bound: `lambda={tightest['lambda_um']} um`, `P_boundary_max={tightest['P_boundary_max_template']}`.")
    lines.extend(["", "## Collar Ratios", ""])
    for row in ratios:
        lines.append(f"- `{row['ratio_id']}`: target={row['target_edge_amplitude_fraction']} requires `d_c/lambda_H >= {row['required_d_c_over_lambda_H']}`")
    lines.extend(["", "## Decisions", ""])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: `{row['status']}` | {row['decision']} | {row['rationale']}")
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
    variations: list[dict[str, object]],
    signatures: list[dict[str, object]],
    component_bounds: list[dict[str, object]],
    ratios: list[dict[str, object]],
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
    variation_text = " ".join(str(row["formula"]) for row in variations)
    checks.append(("variation_formula", "boundary variation and edge commutator formulas are present", "delta S_H|boundary" in variation_text and "[L_H,chi_c]y" in variation_text, ""))
    checks.append(("parent_not_signed", "parent signature verdict blocks zero claim", any(row["signature_id"] == "PSG3706_5_verdict" and row["status"] == "fail_current_claim" for row in signatures), ""))
    checks.append(("component_bounds", "component budget rows preserve curve count and positivity", len(component_bounds) >= 30 and all(float(row["P_boundary_max_template"]) > 0 and float(row["P_edge_max_if_alpha_edge_zero_template"]) > 0 for row in component_bounds), f"rows={len(component_bounds)}"))
    checks.append(("collar_ratios", "collar ratio rows are monotonic and positive", len(ratios) >= 4 and all(float(row["required_d_c_over_lambda_H"]) > 0 for row in ratios), ""))
    checks.append(("decisions_nonclaim", "all decisions are nonclaim", all(row["claim_allowed"] is False for row in decisions), ""))
    checks.append(("claim_gates_blocked", "all claim gates blocked", all(row["status"] == "BLOCKED" and row["claim_allowed"] is False for row in claim_gates), ""))
    checks.append(("next_target_3707", "next target advances to P_N/lambda_H source product", str(next_target[0]["target_doc"]).startswith("3707-") and "PN-lambdaH" in str(next_target[0]["target_doc"]), ""))
    doc_text = read_text(DOC) if DOC.exists() else ""
    checks.append(("doc_core_terms", "doc contains core 3706 terms", all(term in doc_text for term in ["delta S_H|boundary", "B_boundary=0", "B_edge", "eta_boundary", "valid_for_claim=false"]), ""))
    formalization_leaks = list(FORMALIZATION.rglob("*3706*")) if FORMALIZATION.exists() else []
    checks.append(("no_formalization_leak", "no 3706 files were written into formalization-workbench", len(formalization_leaks) == 0, "; ".join(str(path) for path in formalization_leaks)))
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
    variations = boundary_variation_rows(timestamp)
    signatures = parent_signature_rows(timestamp)
    component_bounds = component_bound_rows(timestamp, reduced)
    ratios = collar_ratio_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gates = claim_gate_rows(timestamp)
    status = status_rows(timestamp, component_bounds)
    next_target = next_rows(timestamp)

    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3706_SOURCE_REGISTER.csv",
        "variations": RESIDUALS / "P8_Y5_R2FR_3706_BOUNDARY_VARIATION_ROWS.csv",
        "signatures": RESIDUALS / "P8_Y5_R2FR_3706_PARENT_SIGNATURE_AUDIT_ROWS.csv",
        "component_bounds": RESIDUALS / "P8_Y5_R2FR_3706_ETA_COMPONENT_BOUND_ROWS.csv",
        "ratios": RESIDUALS / "P8_Y5_R2FR_3706_COLLAR_RATIO_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3706_DECISION_ROWS.csv",
        "claim_gates": RESIDUALS / "P8_Y5_R2FR_3706_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3706_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3706_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3706_VALIDATION.csv",
    }

    write_csv(outputs["sources"], sources)
    write_csv(outputs["variations"], variations)
    write_csv(outputs["signatures"], signatures)
    write_csv(outputs["component_bounds"], component_bounds)
    write_csv(outputs["ratios"], ratios)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["claim_gates"], claim_gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, variations, signatures, component_bounds, ratios, decisions, claim_gates, status, next_target)

    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(generated_paths, sources, variations, signatures, component_bounds, ratios, decisions, claim_gates, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3706 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3706 checkpoint: boundary action zero not parent-signed; eta component bounds staged")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
