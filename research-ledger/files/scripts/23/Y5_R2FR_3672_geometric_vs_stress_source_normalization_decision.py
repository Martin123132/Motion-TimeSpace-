from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3672"
BRANCH_ID = "MTS_R2FR_Y5_GEOMETRIC_VS_STRESS_SOURCE_NORMALIZATION_DECISION_3672"
DOC = ROOT / "3672-Y5-R2FR-geometric-vs-stress-source-normalization-decision.md"

C_LIGHT_M_PER_S = 299_792_458.0
G_REF_SI = 6.67430e-11
KAPPA_E_SI = 8.0 * math.pi * G_REF_SI / C_LIGHT_M_PER_S**4


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
        ("handoff_3671", RESIDUALS / "P8_Y5_R2FR_3671_NEXT_TARGET.csv", "geometric-vs-stress", "3671 selected this normalization fork"),
        ("doc_3671", ROOT / "3671-Y5-R2FR-Hessian-STF-parent-normalization-or-kH-source-coefficient.md", "Y_X = C_parent_H*k_H*X", "scalar-slip inversion route"),
        ("forks_3671", RESIDUALS / "P8_Y5_R2FR_3671_NORMALIZATION_FORK_ROWS.csv", "NF3671_1_stress_RHS", "geometric versus stress fork rows"),
        ("kernels_3671", RESIDUALS / "P8_Y5_R2FR_3671_SCALAR_SLIP_KERNEL_ROWS.csv", "YX3671_eta_100_zeta_215.032", "xiH bound grid"),
        ("bounds_3671", RESIDUALS / "P8_Y5_R2FR_3671_CONDITIONAL_XIH_BOUND_ROWS.csv", "xi_H <=", "conditional scalar-slip bound rows"),
        ("weak_response_2477", ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md", "C_metric=(2/c^2)*C_obs*C_Green*C_res", "residual metric-response factorisation"),
        ("metric_inputs_3384", RESIDUALS / "P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv", "MRI3384_1_Cmetric", "PPN metric-response blocker"),
        ("common_mode_3060", RESIDUALS / "P8_Y5_R2FR_3060_COMMON_MODE_METRIC_RESPONSE_THEOREM_ATTEMPT.csv", "CONDITIONAL_NOT_SIGNED", "common-mode theorem remains conditional"),
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


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DEC3672_0_do_not_merge_routes",
            "split the coupling branch",
            "The same scalar-slip observable can be produced by a geometric left-side residual or by a stress-energy right-side anisotropic source, but they have different units and different proof burdens.",
            "Do not use one symbol k_H for both branches.",
            "DECISION_LOCKED_NONCLAIM",
        ),
        (
            "DEC3672_1_geometric_branch",
            "geometric LHS coefficient",
            "Define X_b=e^{-rho/eta}/rho dimensionless and dimensionless derivatives D_b=b partial. If P_TF[D_bD_b Y]=k_H_geo P_TF[D_bD_b X_b], then C_parent_H=1 by normalized-equation convention.",
            "xi_H_geo=|k_H_geo*f_EM/Z_X|",
            "PREFERRED_INTERNAL_ROUTE_IF_PARENT_ACTION_PLACES_TERM_IN_DELTA_E",
        ),
        (
            "DEC3672_2_stress_branch",
            "stress RHS coefficient",
            "If the term is anisotropic stress, write pi_TF=Sigma_H P_TF[partial_i partial_j X_b]*(f_EM/Z_X), where Sigma_H has units J/m so kappa_E*Sigma_H is dimensionless after STF inversion.",
            "xi_H_stress=|kappa_E*Sigma_H*f_EM/Z_X|",
            "SOURCE_NORMALIZATION_ROUTE_REQUIRES_STRESS_LEDGER",
        ),
        (
            "DEC3672_3_do_not_claim_equivalence",
            "equivalence guardrail",
            "The two branches can be compared by xi_H only after their parent coefficients are sourced. A small xi_H bound is not evidence that either route is physically selected.",
            "xi_H = xi_H_geo or xi_H_stress depending on signed parent placement",
            "CLAIM_GUARDRAIL_LOCKED",
        ),
        (
            "DEC3672_4_next_route",
            "next target selection",
            "The least-scrutiny route is to try to prove the parent residual is geometric by locating the Hessian-STF operator in DeltaE_MTS rather than in a fitted effective stress tensor.",
            "hunt parent action first; retain stress branch as bounded fallback",
            "SELECT_GEOMETRIC_PARENT_OWNER_HUNT",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "formula": formula,
            "status": status,
            "claim_allowed": False,
        }
        for decision_id, decision, rationale, formula, status in specs
    ]


def unit_ledger_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "UL3672_0_Y",
            "Y=Phi-Psi",
            "dimensionless",
            "scalar slip read by PPN gamma/Shapiro",
            "observable field; no SI source units",
            "LOCKED",
        ),
        (
            "UL3672_1_Xb",
            "X_b=e^{-rho/eta}/rho",
            "dimensionless",
            "normalized local source profile with rho=r/b",
            "dimensionless profile; physical Hessian contributes b^-2",
            "LOCKED_BY_3671_NORMALIZATION",
        ),
        (
            "UL3672_2_geo",
            "k_H_geo",
            "dimensionless",
            "geometric left-side coefficient in P_TF[D_bD_bY]=k_H_geo P_TF[D_bD_bX_b]",
            "C_parent_H=1 by normalized weak-field equation convention",
            "DEFINED_NONCLAIM",
        ),
        (
            "UL3672_3_stress",
            "Sigma_H",
            "J/m",
            "anisotropic stress line-energy coefficient in pi_TF=Sigma_H P_TF[partial_i partial_jX_b]",
            "kappa_E*Sigma_H is dimensionless after inversion",
            "DEFINED_NONCLAIM",
        ),
        (
            "UL3672_4_kappa",
            "kappa_E=8*pi*G_ref/c^4",
            "m/J",
            "Einstein SI coupling for stress-energy route",
            f"kappa_E={KAPPA_E_SI:.12e} m/J using G_ref={G_REF_SI:.8e}, c={C_LIGHT_M_PER_S:.0f}",
            "CONVENTIONAL_CONSTANT_ROW_NONCLAIM",
        ),
        (
            "UL3672_5_xi",
            "xi_H",
            "dimensionless",
            "scalar-slip amplitude bounded by Shapiro/Cassini proxy rows",
            "xi_H_geo=|k_H_geo*f_EM/Z_X|; xi_H_stress=|kappa_E*Sigma_H*f_EM/Z_X|",
            "BRIDGE_VARIABLE_NONCLAIM",
        ),
    ]
    return [
        {
            **base(ts),
            "unit_id": unit_id,
            "symbol": symbol,
            "units": units,
            "definition": definition,
            "normalization_role": role,
            "status": status,
            "claim_allowed": False,
        }
        for unit_id, symbol, units, definition, role, status in specs
    ]


def branch_bound_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    kernel_rows = load_csv(RESIDUALS / "P8_Y5_R2FR_3671_SCALAR_SLIP_KERNEL_ROWS.csv")
    for row in kernel_rows:
        xi_max = float(row["xi_H_max_if_no_other_terms"])
        sigma_max = xi_max / KAPPA_E_SI
        rows.append(
            {
                **base(ts),
                "bound_id": str(row["kernel_id"]).replace("YX3671", "GB3672"),
                "kernel_id": row["kernel_id"],
                "lambda_over_b_eta": row["lambda_over_b_eta"],
                "half_path_over_b_zeta": row["half_path_over_b_zeta"],
                "xi_H_max": f"{xi_max:.12e}",
                "geometric_bound": f"|k_H_geo*f_EM/Z_X| <= {xi_max:.12e}",
                "stress_bound": f"|Sigma_H*f_EM/Z_X| <= {sigma_max:.12e} J/m",
                "kappa_E_m_per_J": f"{KAPPA_E_SI:.12e}",
                "route_status": "DUAL_BRANCH_BOUND_NONCLAIM",
                "why_nonclaim": "branch placement, k_H_geo or Sigma_H, f_EM/Z_X, boundary kernel, C_other_gamma, and quadratic/direct-TF floors are not parent-owned",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def parent_owner_requirements(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "POR3672_0_parent_operator_location",
            "locate Hessian-STF in parent first variation",
            "Show whether the operator appears in DeltaE_MTS/geometric equations or only as an effective source.",
            "MISSING_PARENT_ACTION_MAPPING",
            "selects k_H_geo versus Sigma_H",
        ),
        (
            "POR3672_1_dimensionless_normalization",
            "fix X_b and derivative convention",
            "Keep X_b dimensionless and physical b^-2 factors explicit so no hidden length scale is smuggled into the coupling.",
            "CONVENTION_DEFINED_NEEDS_PARENT_SIGNOFF",
            "prevents unit drift",
        ),
        (
            "POR3672_2_source_descent",
            "stress-energy descent if RHS route used",
            "Derive pi_TF from matter/EM/action variables and prove Sigma_H has J/m units with no fitted-GM or fitted-Cassini calibration.",
            "MISSING_IF_STRESS_ROUTE",
            "prevents patchwork source coupling",
        ),
        (
            "POR3672_3_boundary_kernel",
            "STF inversion boundary silence",
            "Remove or bound the kernel of P_TF[partial_i partial_j] for the local solar collar/readout.",
            "MISSING_BOUNDARY_CERTIFICATE",
            "needed for scalar-slip inversion claim",
        ),
        (
            "POR3672_4_other_floors",
            "C_other_gamma and quadratic floors",
            "Bound direct h_TF readout, k_G branch, boundary/readout floors, and non-EM source components before scoring gamma.",
            "MISSING_FLOOR_BOUNDS",
            "keeps local-GR/PPN claim blocked",
        ),
    ]
    return [
        {
            **base(ts),
            "requirement_id": requirement_id,
            "requirement": requirement,
            "description": description,
            "status": status,
            "why_it_matters": why,
            "claim_allowed": False,
        }
        for requirement_id, requirement, description, status, why in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3672_0_split", "geometric/stress split", "PASS_DECISION", "ambiguous k_H replaced by k_H_geo and Sigma_H routes"),
        ("CG3672_1_units", "unit ledger", "PASS_NONCLAIM_LEDGER", "dimensionless geometric route and J/m stress route are unit-separated"),
        ("CG3672_2_geo_claim", "geometric route claim", "BLOCKED_PARENT_MAPPING", "must locate operator in DeltaE_MTS or parent LHS"),
        ("CG3672_3_stress_claim", "stress route claim", "BLOCKED_SOURCE_DESCENT", "must derive Sigma_H from stress/EM/action variables"),
        ("CG3672_4_gamma_claim", "Cassini/local-GR claim", "BLOCKED_NONCLAIM", "xi_H branch, floors, and boundary kernel remain unsigned"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
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
            "status": "COUPLING_SPLIT_INTO_GEOMETRIC_AND_STRESS_BRANCHES_NONCLAIM",
            "summary": "3672 stops using one overloaded k_H coupling. The scalar-slip amplitude is split into a dimensionless geometric branch xi_H_geo=|k_H_geo*f_EM/Z_X| and a stress-energy branch xi_H_stress=|kappa_E*Sigma_H*f_EM/Z_X| with Sigma_H in J/m.",
            "claim_ceiling": "no Cassini/gamma, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": f"Strongest inherited scalar-slip row gives {strongest['geometric_bound']} or {strongest['stress_bound']} before parent coefficients are sourced.",
            "next_missing_piece": "locate the Hessian-STF operator in the parent first variation to select geometric LHS or stress RHS",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3672_0",
            "target_doc": "3673-Y5-R2FR-parent-action-Hessian-STF-operator-location.md",
            "target_script": "scripts/Y5_R2FR_3673_parent_action_Hessian_STF_operator_location.py",
            "objective": "hunt the parent action/first-variation trail for the Hessian-STF operator and decide whether it belongs to DeltaE_MTS/geometric LHS or to an effective stress-energy RHS",
            "success_gate": "operator placement is source-backed, or both k_H_geo and Sigma_H remain explicit nonclaim branches with no coefficient merging",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    decisions: list[dict[str, object]],
    units: list[dict[str, object]],
    bounds: list[dict[str, object]],
    requirements: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    strongest = min(bounds, key=lambda row: float(row["xi_H_max"]))
    lines = [
        "# 3672 - Geometric vs stress source normalization decision",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "This checkpoint resolves the coupling ambiguity by refusing to let one symbol do two incompatible jobs.",
        "",
        "## Decision",
        "- If the Hessian-STF term is part of the parent geometric field equation, use the normalized branch:",
        "  `P_TF[D_bD_b Y]=k_H_geo P_TF[D_bD_b X_b]`, so `C_parent_H=1` by convention and `xi_H_geo=|k_H_geo*f_EM/Z_X|`.",
        "- If the term is a stress-energy source, use:",
        "  `pi_TF=Sigma_H P_TF[partial_i partial_j X_b]*(f_EM/Z_X)`, so `xi_H_stress=|kappa_E*Sigma_H*f_EM/Z_X|`.",
        "- These are not interchangeable until the parent action/first variation says where the operator lives.",
        "",
        f"`kappa_E=8*pi*G_ref/c^4={KAPPA_E_SI:.12e} m/J` for the stress-route conversion row.",
        "",
        f"Strongest inherited scalar-slip row: `{strongest['kernel_id']}` gives `{strongest['geometric_bound']}` or `{strongest['stress_bound']}`.",
        "",
        "No Cassini/local-GR claim follows from this: the row is a units-clean bridge, not a sourced coefficient.",
        "",
        "## Decision rows",
    ]
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Unit ledger"])
    for row in units:
        lines.append(f"- `{row['unit_id']}`: `{row['symbol']}` [{row['units']}] - {row['status']}")
    lines.extend(["", "## Dual branch bounds"])
    for row in bounds[:6]:
        lines.append(f"- `{row['bound_id']}`: `{row['geometric_bound']}`; `{row['stress_bound']}`")
    lines.extend(["", "## Parent-owner requirements"])
    for row in requirements:
        lines.append(f"- `{row['requirement_id']}`: {row['status']} - {row['requirement']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['gate_id']}`: {row['status']} - {row['gate']}")
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
    decisions: list[dict[str, object]],
    units: list[dict[str, object]],
    bounds: list[dict[str, object]],
    requirements: list[dict[str, object]],
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
    generated = sources + decisions + units + bounds + requirements + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3672*", "3672-Y5-R2FR-*", "P8_Y5*3672*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3672_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3672_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3672_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3672 outputs written")
    add("VAL3672_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3672_4_split_decision", {"DEC3672_1_geometric_branch", "DEC3672_2_stress_branch", "DEC3672_3_do_not_claim_equivalence"}.issubset({str(row["decision_id"]) for row in decisions}), "geometric/stress split decisions present")
    add("VAL3672_5_unit_ledger", {"k_H_geo", "Sigma_H", "kappa_E=8*pi*G_ref/c^4", "xi_H"}.issubset({str(row["symbol"]) for row in units}), "unit ledger has branch variables")
    add("VAL3672_6_bounds", len(bounds) == len(load_csv(RESIDUALS / "P8_Y5_R2FR_3671_SCALAR_SLIP_KERNEL_ROWS.csv")) and all("J/m" in row["stress_bound"] for row in bounds), "dual branch bounds generated")
    add("VAL3672_7_kappa_positive", KAPPA_E_SI > 0 and all(abs(float(row["kappa_E_m_per_J"]) - KAPPA_E_SI) / KAPPA_E_SI < 1.0e-12 for row in bounds), "Einstein stress conversion is positive and copied")
    add("VAL3672_8_requirements", {"POR3672_0_parent_operator_location", "POR3672_2_source_descent", "POR3672_3_boundary_kernel"}.issubset({str(row["requirement_id"]) for row in requirements}), "parent-owner requirements present")
    add("VAL3672_9_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3672_10_claim_gates", any(row["gate_id"] == "CG3672_4_gamma_claim" and row["status"] == "BLOCKED_NONCLAIM" for row in gates), "gamma claim remains blocked")
    add("VAL3672_11_doc_written", "k_H_geo" in doc_text and "Sigma_H" in doc_text and "not interchangeable" in doc_text, "doc records split and no-merge rule")
    add("VAL3672_12_no_formalization_leak", not leaks, "no 3672 checkpoint files in formalization-workbench")
    add("VAL3672_13_next_target", next_target[0]["target_doc"].startswith("3673-") and "parent-action" in next_target[0]["target_doc"], "3673 parent-action operator-location target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    decisions = decision_rows(ts)
    units = unit_ledger_rows(ts)
    bounds = branch_bound_rows(ts)
    requirements = parent_owner_requirements(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, bounds)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3672_SOURCE_REGISTER.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3672_NORMALIZATION_DECISION_ROWS.csv",
        "units": RESIDUALS / "P8_Y5_R2FR_3672_UNIT_LEDGER_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3672_DUAL_BRANCH_BOUND_ROWS.csv",
        "requirements": RESIDUALS / "P8_Y5_R2FR_3672_PARENT_OWNER_REQUIREMENTS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3672_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3672_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3672_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3672_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["units"], units)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["requirements"], requirements)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, decisions, units, bounds, requirements, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, decisions, units, bounds, requirements, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3672 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3672 checkpoint with {len(validation)} validation checks; coupling split into geometric and stress branches")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
