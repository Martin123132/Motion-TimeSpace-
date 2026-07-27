from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3671"
BRANCH_ID = "MTS_R2FR_Y5_HESSIAN_STF_PARENT_NORMALIZATION_OR_KH_SOURCE_COEFFICIENT_3671"
DOC = ROOT / "3671-Y5-R2FR-Hessian-STF-parent-normalization-or-kH-source-coefficient.md"

R_SUN_M = 6.957e8
AU_M = 1.495978707e11
B_GAMMA_CASSINI = 2.3e-5
LAMBDA_OVER_B_GRID = [0.01, 0.1, 1.0, 10.0, 100.0]
HALF_PATH_OVER_B_GRID = [AU_M / R_SUN_M, 1000.0, 2000.0]
SIMPSON_STEPS = 20000


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
        ("handoff_3670", RESIDUALS / "P8_Y5_R2FR_3670_NEXT_TARGET.csv", "parent/readout/Green normalization", "3670 selected parent normalization"),
        ("doc_3670", ROOT / "3670-Y5-R2FR-KgammaH-transfer-kernel-or-conservative-linear-bound.md", "C_parent_H", "KgammaH geometry leaves parent normalization unsigned"),
        ("kernel_3670", RESIDUALS / "P8_Y5_R2FR_3670_KGAMMAH_PATH_KERNEL_ROWS.csv", "KGH3670_eta_100_zeta_215.032", "explicit direct Hessian path kernel"),
        ("bounds_3670", RESIDUALS / "P8_Y5_R2FR_3670_CONSERVATIVE_BETAH_BOUND_ROWS.csv", "beta_H=|C_parent_H", "conservative betaH convention"),
        ("doc_3669", ROOT / "3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md", "S_TF^X|linear", "linear Hessian-STF branch definition"),
        ("weak_response_2477", ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md", "C_metric=(2/c^2)*C_obs*C_Green*C_res", "metric-response factorisation"),
        ("metric_inputs_3384", RESIDUALS / "P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv", "MRI3384_1_Cmetric", "missing metric response input"),
        ("common_mode_3060", RESIDUALS / "P8_Y5_R2FR_3060_COMMON_MODE_METRIC_RESPONSE_THEOREM_ATTEMPT.csv", "CONDITIONAL_NOT_SIGNED", "same-frame common-mode route remains conditional"),
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


def simpson_even_integral(func, eta: float, extent: float) -> float:
    n = SIMPSON_STEPS
    if n % 2:
        n += 1
    h = extent / n
    total = 0.0
    for index in range(n + 1):
        u = index * h
        weight = 1 if index in (0, n) else 4 if index % 2 else 2
        total += weight * func(u, eta)
    return 2.0 * h * total / 3.0


def yukawa_potential_shape(u: float, eta: float) -> float:
    rho = math.sqrt(1.0 + u * u)
    return math.exp(-rho / eta) / rho


def parent_normalization_derivation_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "PND3671_0_linear_metric_split",
            "weak-field scalar slip variable",
            "Use Y=Phi-Psi as the scalar slip channel controlled by the trace-free spatial equation.",
            "P_TF[partial_i partial_j Y] = source_TF",
            "DERIVED_STANDARD_LINEAR_FORM_CONDITIONAL",
        ),
        (
            "PND3671_1_STF_inversion_lemma",
            "Hessian-STF inversion lemma",
            "If the parent equation has P_TF[partial_i partial_j Y]=C_H P_TF[partial_i partial_j X], then P_TF[partial_i partial_j(Y-C_H X)]=0.",
            "Y=C_H X + kernel(P_TF partial partial)",
            "DERIVED_CONDITIONAL_LEMMA",
        ),
        (
            "PND3671_2_boundary_kernel",
            "kernel removal conditions",
            "Asymptotic flatness, no preferred affine gradient, no isotropic quadratic background, and no boundary/readout STF floor remove the integration kernel.",
            "kernel(P_TF partial partial)->0 under local-asymptotic boundary silence",
            "BOUNDARY_CONDITIONAL_NOT_PARENT_SIGNED",
        ),
        (
            "PND3671_3_parent_coefficient_fork",
            "normalization fork",
            "If the MTS source is already placed on the geometric left-hand side, C_parent_H may be dimensionless. If it is stress-energy anisotropic stress, C_parent_H carries the Einstein 8*pi*G/c^4 normalization and source units.",
            "Y_X = C_parent_H*k_H*X",
            "COEFFICIENT_SOURCE_UNITS_UNSIGNED",
        ),
        (
            "PND3671_4_readout_kernel_change",
            "readout kernel change",
            "The parent-field-equation route integrates the Hessian-STF source into a scalar Yukawa slip, so the Shapiro geometry kernel is the positive Yukawa-potential path kernel, not the direct Hessian readout kernel from 3670.",
            "G_X(eta,zeta)=int exp(-rho/eta)/rho du / (2 asinh zeta)",
            "DERIVED_SCALAR_SLIP_KERNEL_IF_PARENT_EQUATION_SIGNS",
        ),
        (
            "PND3671_5_verdict",
            "3671 verdict",
            "The mathematical inversion route is built, but the theory still must decide/source whether k_H is a geometric equation coefficient or a stress/anistropic-source coefficient.",
            "xi_H=|C_parent_H*k_H*f_EM/Z_X| remains nonclaim until C_parent_H and k_H are parent-owned",
            "PARTIAL_DERIVATION_PARENT_COEFFICIENT_UNSIGNED",
        ),
    ]
    return [
        {
            **base(ts),
            "derivation_id": derivation_id,
            "clause": clause,
            "statement": statement,
            "formula": formula,
            "status": status,
            "claim_allowed": False,
        }
        for derivation_id, clause, statement, formula, status in specs
    ]


def scalar_slip_kernel_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for eta in LAMBDA_OVER_B_GRID:
        local_yukawa_suppression = math.exp(-1.0 / eta)
        for extent in HALF_PATH_OVER_B_GRID:
            integral = simpson_even_integral(yukawa_potential_shape, eta, extent)
            denominator = 2.0 * math.asinh(extent)
            gx = integral / denominator
            xi_h_max = B_GAMMA_CASSINI / gx if gx > 0 else math.inf
            rows.append(
                {
                    **base(ts),
                    "kernel_id": f"YX3671_eta_{eta:g}_zeta_{extent:.6g}",
                    "lambda_over_b_eta": f"{eta:.12e}",
                    "half_path_over_b_zeta": f"{extent:.12e}",
                    "local_yukawa_suppression_exp_minus_b_over_lambda": f"{local_yukawa_suppression:.12e}",
                    "I_X_dimensionless": f"{integral:.12e}",
                    "D_shapiro_dimensionless": f"{denominator:.12e}",
                    "G_X_dimensionless": f"{gx:.12e}",
                    "xi_H_max_if_no_other_terms": f"{xi_h_max:.12e}",
                    "xi_H_definition": "xi_H=|C_parent_H*k_H*f_EM/Z_X| in scalar-slip normalization Y_X=xi_H*X_shape",
                    "status": "SCALAR_SLIP_YUKAWA_KERNEL_CONDITIONAL_NONCLAIM",
                    "why_nonclaim": "requires parent equation P_TF[dd(Phi-Psi)]=C_parent_H*k_H*P_TF[ddX], boundary kernel silence, and sourced C_parent_H/k_H/f_EM/Z_X",
                    "score_ready": False,
                    "claim_allowed": False,
                }
            )
    return rows


def normalization_fork_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "NF3671_0_geometric_LHS",
            "geometric equation coefficient",
            "k_H already has geometry units and sits in the same weak-field equation as P_TF[dd(Phi-Psi)]",
            "C_parent_H dimensionless, possibly C_parent_H=1 by convention",
            "PROMISING_BUT_NOT_SOURCE_SIGNED",
        ),
        (
            "NF3671_1_stress_RHS",
            "anisotropic stress coefficient",
            "k_H multiplies a physical stress-like source, so Einstein normalization and source dimensions must be explicit",
            "C_parent_H ~ 8*pi*G/c^4 times unit conversion",
            "UNSIGNED_UNITS_BLOCKER",
        ),
        (
            "NF3671_2_direct_metric_readout",
            "direct h_ij^TF readout",
            "Use 3670 absolute Hessian path kernel if parent action couples Hessian-STF directly into the observed spatial metric/readout.",
            "delta t_TF proportional to integral n^i n^j h_ij^TF dz",
            "CONSERVATIVE_FALLBACK_AVAILABLE",
        ),
        (
            "NF3671_3_scalar_slip_readout",
            "scalar slip readout",
            "Use 3671 Yukawa path kernel if parent field equation first inverts the Hessian-STF source into Phi-Psi.",
            "delta gamma_X proportional to xi_H*G_X(lambda/b,L/b)",
            "BEST_ROUTE_IF_PARENT_EQUATION_SIGNS",
        ),
    ]
    return [
        {
            **base(ts),
            "fork_id": fork_id,
            "route": route,
            "condition": condition,
            "normalization": normalization,
            "status": status,
            "claim_allowed": False,
        }
        for fork_id, route, condition, normalization, status in specs
    ]


def conservative_xi_bound_rows(ts: str, kernels: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "bound_id": str(row["kernel_id"]).replace("YX3671", "XIH3671"),
            "kernel_id": row["kernel_id"],
            "xi_H_definition": row["xi_H_definition"],
            "bound_formula": f"xi_H <= {row['xi_H_max_if_no_other_terms']} if C_other_gamma=0 and quadratic/direct-TF branches are zero",
            "readout_route": "scalar-slip Yukawa path kernel from Hessian-STF inversion",
            "required_for_claim": "source C_parent_H route; source k_H; source f_EM/Z_X; bound boundary kernel, C_other_gamma, direct h_TF, and quadratic beta_G",
            "status": "CONDITIONAL_SCALAR_SLIP_BOUND_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
        }
        for row in kernels
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3671_0_STF_inversion", "Hessian-STF inversion route", "PASSED_CONDITIONAL_DERIVATION", "P_TF ddY = C P_TF ddX integrates to Y=CX up to boundary/gauge kernel"),
        ("CG3671_1_scalar_kernel", "Yukawa scalar-slip kernel", "PASSED_CONDITIONAL_KERNEL", "positive path kernel G_X generated for eta/zeta grid"),
        ("CG3671_2_parent_coefficient", "C_parent_H coefficient", "FAILED_UNSIGNED", "geometric-vs-stress normalization and units are not parent-signed"),
        ("CG3671_3_boundary_kernel", "STF inversion kernel silence", "FAILED_UNSIGNED", "asymptotic/boundary/readout kernel silence remains a condition"),
        ("CG3671_4_claim_status", "Cassini/local-GR claim", "BLOCKED_NONCLAIM", "xi_H and all source coefficients remain nonclaim"),
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


def status_rows(ts: str, kernels: list[dict[str, object]]) -> list[dict[str, object]]:
    strongest = min(kernels, key=lambda row: float(row["xi_H_max_if_no_other_terms"]))
    return [
        {
            **base(ts),
            "status": "STF_INVERSION_ROUTE_DERIVED_PARENT_COEFFICIENT_UNSIGNED",
            "summary": "3671 derives the conditional parent-equation route: a Hessian-STF source can invert to a scalar slip Y=Phi-Psi proportional to X, replacing the direct Hessian readout by a Yukawa path kernel if the parent equation signs the route.",
            "claim_ceiling": "no Cassini/gamma, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": f"Strongest conditional scalar-slip proxy row is {strongest['kernel_id']} with xi_H <= {strongest['xi_H_max_if_no_other_terms']} before C_parent_H/k_H/f_EM/Z_X are owned.",
            "next_missing_piece": "choose/source the parent coefficient route: geometric LHS normalization versus stress-energy RHS normalization",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3671_0",
            "target_doc": "3672-Y5-R2FR-geometric-vs-stress-source-normalization-decision.md",
            "target_script": "scripts/Y5_R2FR_3672_geometric_vs_stress_source_normalization_decision.py",
            "objective": "decide whether the k_H Hessian-STF branch belongs to the geometric left-hand side or to a stress-energy right-hand side, and derive the corresponding units/normalization ledger",
            "success_gate": "C_parent_H is either reduced to a parent-owned convention with units, or the branch is explicitly split into geometric and stress-source variants with no claim leakage",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    kernels: list[dict[str, object]],
    forks: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    strongest = min(kernels, key=lambda row: float(row["xi_H_max_if_no_other_terms"]))
    lines = [
        "# 3671 - Hessian-STF parent normalization or kH source coefficient",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "This is the important fork: 3670 treated the Hessian-STF term as a direct readout kernel. 3671 tests whether the parent field equation instead integrates it into scalar slip.",
        "",
        "Let `Y=Phi-Psi`. If the parent weak-field trace-free equation has",
        "",
        "`P_TF[partial_i partial_j Y] = C_parent_H*k_H*P_TF[partial_i partial_j X]`,",
        "",
        "then",
        "",
        "`P_TF[partial_i partial_j(Y-C_parent_H*k_H*X)]=0`.",
        "",
        "With asymptotic/boundary/readout kernel silence, this gives the conditional local result:",
        "",
        "`Y_X = C_parent_H*k_H*X`.",
        "",
        "That is a real derivation route, but it is not claimed yet because `C_parent_H` is not parent-owned: the branch must decide whether `k_H` lives as a geometric equation coefficient or as a stress-energy/source coefficient requiring Einstein/unit normalization.",
        "",
        "If this route is signed, the Cassini/Shapiro kernel becomes the positive Yukawa scalar-slip path kernel:",
        "",
        "`G_X(eta,zeta)=int_{-zeta}^{zeta} exp(-sqrt(1+u^2)/eta)/sqrt(1+u^2) du / (2 asinh zeta)`.",
        "",
        f"Strongest sampled scalar-slip proxy row: `{strongest['kernel_id']}` with `xi_H <= {strongest['xi_H_max_if_no_other_terms']}` if other branches are zero.",
        "",
        "`xi_H=|C_parent_H*k_H*f_EM/Z_X|`; this remains nonclaim until the parent normalization, k_H source, f_EM, and Z_X are signed.",
        "",
        "## Derivation rows",
    ]
    for row in derivations:
        lines.append(f"- `{row['derivation_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Normalization forks"])
    for row in forks:
        lines.append(f"- `{row['fork_id']}`: {row['status']} - {row['route']} => `{row['normalization']}`")
    lines.extend(["", "## Scalar-slip kernel rows"])
    for row in kernels:
        lines.append(
            f"- `{row['kernel_id']}`: eta={row['lambda_over_b_eta']}, zeta={row['half_path_over_b_zeta']}, "
            f"G_X={row['G_X_dimensionless']}, xi_H_max={row['xi_H_max_if_no_other_terms']}"
        )
    lines.extend(["", "## Bound rows"])
    for row in bounds[:5]:
        lines.append(f"- `{row['bound_id']}`: `{row['bound_formula']}`")
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
    derivations: list[dict[str, object]],
    kernels: list[dict[str, object]],
    forks: list[dict[str, object]],
    bounds: list[dict[str, object]],
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
    generated = sources + derivations + kernels + forks + bounds + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3671*", "3671-Y5-R2FR-*", "P8_Y5*3671*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3671_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3671_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3671_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3671 outputs written")
    add("VAL3671_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3671_4_inversion_derivation", any(row["derivation_id"] == "PND3671_1_STF_inversion_lemma" and row["status"] == "DERIVED_CONDITIONAL_LEMMA" for row in derivations), "STF inversion lemma derived")
    add("VAL3671_5_kernel_grid", len(kernels) == len(LAMBDA_OVER_B_GRID) * len(HALF_PATH_OVER_B_GRID), "all eta/zeta scalar kernels generated")
    add("VAL3671_6_kernel_numerics", all(float(row["I_X_dimensionless"]) > 0 and float(row["D_shapiro_dimensionless"]) > 0 and float(row["G_X_dimensionless"]) > 0 for row in kernels), "scalar kernel numerics are positive")
    add("VAL3671_7_fork_split", {"NF3671_0_geometric_LHS", "NF3671_1_stress_RHS", "NF3671_2_direct_metric_readout", "NF3671_3_scalar_slip_readout"}.issubset({str(row["fork_id"]) for row in forks}), "normalization forks recorded")
    add("VAL3671_8_bound_rows", len(bounds) == len(kernels) and all("xi_H <=" in row["bound_formula"] for row in bounds), "conditional xiH bound rows generated")
    add("VAL3671_9_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3671_10_parent_unsigned_gate", any(row["gate_id"] == "CG3671_2_parent_coefficient" and row["status"] == "FAILED_UNSIGNED" for row in gates), "parent coefficient remains unsigned")
    add("VAL3671_11_doc_written", "Y=Phi-Psi" in doc_text and "Y_X = C_parent_H*k_H*X" in doc_text and "not claimed" in doc_text, "doc records scalar-slip derivation and nonclaim status")
    add("VAL3671_12_no_formalization_leak", not leaks, "no 3671 checkpoint files in formalization-workbench")
    add("VAL3671_13_next_target", next_target[0]["target_doc"].startswith("3672-") and "geometric-vs-stress" in next_target[0]["target_doc"], "3672 source-normalization target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    derivations = parent_normalization_derivation_rows(ts)
    kernels = scalar_slip_kernel_rows(ts)
    forks = normalization_fork_rows(ts)
    bounds = conservative_xi_bound_rows(ts, kernels)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, kernels)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3671_SOURCE_REGISTER.csv",
        "derivations": RESIDUALS / "P8_Y5_R2FR_3671_PARENT_NORMALIZATION_DERIVATION_ROWS.csv",
        "kernels": RESIDUALS / "P8_Y5_R2FR_3671_SCALAR_SLIP_KERNEL_ROWS.csv",
        "forks": RESIDUALS / "P8_Y5_R2FR_3671_NORMALIZATION_FORK_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3671_CONDITIONAL_XIH_BOUND_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3671_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3671_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3671_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3671_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["derivations"], derivations)
    write_csv(outputs["kernels"], kernels)
    write_csv(outputs["forks"], forks)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, derivations, kernels, forks, bounds, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, derivations, kernels, forks, bounds, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3671 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3671 checkpoint with {len(validation)} validation checks; scalar-slip inversion route derived, parent coefficient unsigned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
