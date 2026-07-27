from __future__ import annotations

import csv
import math
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3670"
BRANCH_ID = "MTS_R2FR_Y5_KGAMMAH_TRANSFER_KERNEL_OR_CONSERVATIVE_LINEAR_BOUND_3670"
DOC = ROOT / "3670-Y5-R2FR-KgammaH-transfer-kernel-or-conservative-linear-bound.md"

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
        ("handoff_3669", RESIDUALS / "P8_Y5_R2FR_3669_NEXT_TARGET.csv", "KgammaH-transfer-kernel", "3669 selected the KgammaH target"),
        ("doc_3669", ROOT / "3669-Y5-R2FR-kH-Hessian-STF-parent-owner-or-linear-gamma-bound-row.md", "S_TF^X|linear", "linear Hessian-STF branch definition"),
        ("linear_3669", RESIDUALS / "P8_Y5_R2FR_3669_LINEAR_MUH_BOUND_ROWS.csv", "mu_H=|K_gamma_H", "muH transfer-kernel blocker"),
        ("profile_3658", RESIDUALS / "P8_Y5_R2FR_3658_GAMMA_PROFILE_COEFFICIENT_ROWS.csv", "GPC3658_2_Yukawa_like_profile", "Yukawa Hessian-STF profile kernel"),
        ("derivation_3668", RESIDUALS / "P8_Y5_R2FR_3668_KH_KG_PROJECTION_DERIVATION_ROWS.csv", "LINEAR_KH_AND_QUADRATIC_KG_SPLIT_DERIVED", "linear kH / quadratic kG hierarchy"),
        ("reduced_3668", RESIDUALS / "P8_Y5_R2FR_3668_REDUCED_BOUND_INTERFACE_ROWS.csv", "RB3668_lambda_over_r_1", "prior scale-proxy bound interface"),
        ("weak_response_2477", ROOT / "2477-Y5-R2FR-parent-weak-field-metric-response-theorem-or-no-go.md", "C_metric=(2/c^2)*C_obs*C_Green*C_res", "metric-response factorisation"),
        ("metric_inputs_3384", RESIDUALS / "P8_Y5_R2FR_3384_METRIC_RESPONSE_INPUT_REQUIREMENTS.csv", "MRI3384_1_Cmetric", "missing parent metric-response input"),
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


def simpson_even_integral(func, eta: float, extent: float, absolute: bool) -> float:
    n = SIMPSON_STEPS
    if n % 2:
        n += 1
    h = extent / n
    total = 0.0
    for index in range(n + 1):
        u = index * h
        value = func(u, eta)
        if absolute:
            value = abs(value)
        weight = 1 if index in (0, n) else 4 if index % 2 else 2
        total += weight * value
    return 2.0 * h * total / 3.0


def hessian_stf_projected_shape(u: float, eta: float) -> float:
    radius = math.sqrt(1.0 + u * u)
    hessian_shape = math.exp(-radius / eta) * (
        3.0 / radius**3 + 3.0 / (eta * radius**2) + 1.0 / (eta**2 * radius)
    )
    angular_projection = u * u / (1.0 + u * u) - 1.0 / 3.0
    return hessian_shape * angular_projection


def geometry_derivation_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "KGD3670_0_coordinates",
            "straight-line Shapiro geometry",
            "z is the unperturbed photon coordinate, b is impact parameter, r=b*sqrt(1+u^2), u=z/b",
            "r(z)=sqrt(b^2+z^2)",
            "DERIVED_GEOMETRY_LOCKED",
        ),
        (
            "KGD3670_1_radial_Hessian_STF",
            "radial Hessian-STF decomposition",
            "For radial X(r), P_TF[partial_i partial_j X]=(X''-X'/r)(rhat_i rhat_j-delta_ij/3)",
            "X=e^{-r/lambda}/r => X''-X'/r=e^{-r/lambda}(3/r^3+3/(lambda*r^2)+1/(lambda^2*r))",
            "DERIVED_ANALYTIC_KERNEL",
        ),
        (
            "KGD3670_2_null_projection",
            "projection onto photon direction",
            "The Shapiro readout sees n^i n^j P_TF[partial_i partial_j X], giving an angular factor that changes sign along the path.",
            "n^i n^j(rhat_i rhat_j-delta_ij/3)=u^2/(1+u^2)-1/3",
            "DERIVED_SIGN_STRUCTURE",
        ),
        (
            "KGD3670_3_dimensionless_kernel",
            "dimensionless line-of-sight kernel",
            "With eta=lambda/b and zeta=L/b, the signed geometry kernel is J_H(eta,zeta)=int_{-zeta}^{zeta} F_H(u,eta) du.",
            "F_H=e^{-sqrt(1+u^2)/eta}(3/rho^3+3/(eta*rho^2)+1/(eta^2*rho))*(u^2/(1+u^2)-1/3)",
            "DERIVED_TRANSFER_GEOMETRY",
        ),
        (
            "KGD3670_4_shapiro_normalization",
            "Shapiro normalization proxy",
            "The GR comparison denominator for the same straight path is D(zeta)=int dz/r = 2 asinh(zeta); actual parent/readout normalization is not yet owned.",
            "G_H=J_H/D, G_H_abs=J_abs/D, actual dimensionful kernel = G_H/b^2",
            "GEOMETRY_DERIVED_PARENT_NORMALIZATION_UNSIGNED",
        ),
        (
            "KGD3670_5_conservative_rule",
            "absolute-path conservative rule",
            "Do not use signed cancellation as evidence. Until the parent readout is signed, use J_abs or carry both signed and absolute rows.",
            "beta_H <= B_gamma/G_H_abs for beta_H defined in the chosen b^2-normalized parent convention",
            "CONSERVATIVE_NONCLAIM_CONVENTION",
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


def path_kernel_rows(ts: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    zero_crossing_u = 1.0 / math.sqrt(2.0)
    for eta in LAMBDA_OVER_B_GRID:
        local_shape = math.exp(-1.0 / eta) * (3.0 + 3.0 / eta + 1.0 / eta**2)
        closest_projection_shape = abs(hessian_stf_projected_shape(0.0, eta))
        for extent in HALF_PATH_OVER_B_GRID:
            signed_j = simpson_even_integral(hessian_stf_projected_shape, eta, extent, absolute=False)
            abs_j = simpson_even_integral(hessian_stf_projected_shape, eta, extent, absolute=True)
            denominator = 2.0 * math.asinh(extent)
            signed_g = signed_j / denominator
            abs_g = abs_j / denominator
            cancellation = abs(signed_j) / abs_j if abs_j > 0 else 0.0
            beta_h_max = B_GAMMA_CASSINI / abs_g if abs_g > 0 else math.inf
            rows.append(
                {
                    **base(ts),
                    "kernel_id": f"KGH3670_eta_{eta:g}_zeta_{extent:.6g}",
                    "lambda_over_b_eta": f"{eta:.12e}",
                    "half_path_over_b_zeta": f"{extent:.12e}",
                    "angular_zero_crossing_u": f"{zero_crossing_u:.12e}",
                    "local_hessian_shape_b3": f"{local_shape:.12e}",
                    "closest_projected_abs_shape_b3": f"{closest_projection_shape:.12e}",
                    "J_H_signed_dimensionless": f"{signed_j:.12e}",
                    "J_H_abs_dimensionless": f"{abs_j:.12e}",
                    "D_shapiro_dimensionless": f"{denominator:.12e}",
                    "G_H_signed_dimensionless": f"{signed_g:.12e}",
                    "G_H_abs_dimensionless": f"{abs_g:.12e}",
                    "G_H_abs_per_m2_for_b_Rsun": f"{abs_g / R_SUN_M**2:.12e}",
                    "signed_to_absolute_fraction": f"{cancellation:.12e}",
                    "beta_H_max_if_no_other_terms": f"{beta_h_max:.12e}",
                    "status": "EXPLICIT_GEOMETRY_KERNEL_NONCLAIM",
                    "why_nonclaim": "straight-line/path/impact proxy only; parent C_parent_H, Green normalization, k_H, f_EM/Z_X, and C_other_gamma are unsigned",
                    "score_ready": False,
                    "claim_allowed": False,
                }
            )
    return rows


def conservative_bound_rows(ts: str, kernels: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for kernel in kernels:
        rows.append(
            {
                **base(ts),
                "bound_id": str(kernel["kernel_id"]).replace("KGH3670", "CBH3670"),
                "kernel_id": kernel["kernel_id"],
                "beta_H_definition": "beta_H=|C_parent_H*k_H*f_EM/Z_X|/b^2 in the selected Shapiro normalization",
                "conservative_kernel_choice": "G_H_abs_dimensionless",
                "conservative_bound_formula": f"beta_H <= {kernel['beta_H_max_if_no_other_terms']} if C_other_gamma=0 and beta_G=0",
                "signed_cancellation_policy": "signed J_H may be diagnostic only; it is not used to weaken a bound or claim a pass",
                "required_for_claim": "derive C_parent_H and readout normalization; fix b/path for Cassini observable; source k_H, f_EM, Z_X; bound C_other_gamma and quadratic beta_G",
                "status": "CONSERVATIVE_LINEAR_BOUND_CONVENTION_NONCLAIM",
                "score_ready": False,
                "claim_allowed": False,
            }
        )
    return rows


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3670_0_geometry_kernel", "K_gamma_H geometry", "PASSED_DERIVED_GEOMETRY", "radial Hessian-STF Shapiro projection and dimensionless path integral derived"),
        ("CG3670_1_cancellation_guard", "line-of-sight cancellation", "PASSED_GUARDRAIL", "absolute-path kernel selected for conservative nonclaim bound rows"),
        ("CG3670_2_parent_normalization", "parent/readout normalization", "FAILED_UNSIGNED", "C_parent_H / C_metric / Green/readout map still not derived"),
        ("CG3670_3_local_gamma_claim", "Cassini gamma/local-GR claim", "BLOCKED_NONCLAIM", "k_H, f_EM/Z_X, C_other_gamma and parent metric map are not source-owned"),
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
    strongest = min(kernels, key=lambda row: float(row["beta_H_max_if_no_other_terms"]))
    return [
        {
            **base(ts),
            "status": "KGAMMAH_GEOMETRY_DERIVED_PARENT_NORMALIZATION_UNSIGNED",
            "summary": "3670 derives the explicit Hessian-STF Shapiro geometry kernel for the k_H branch and replaces the naked K_gamma_H placeholder with signed and absolute path-integral rows.",
            "claim_ceiling": "no Cassini/gamma, local-GR, PPN, WEP/R10, Newtonian, source-calibration, or EH-dominance pass is claimed",
            "useful_result": f"Strongest absolute-path proxy row is {strongest['kernel_id']} with beta_H <= {strongest['beta_H_max_if_no_other_terms']} before parent/readout normalization is owned.",
            "next_missing_piece": "C_parent_H: the parent metric/readout/Green normalization mapping beta_H back to k_H*f_EM/Z_X",
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3670_0",
            "target_doc": "3671-Y5-R2FR-Hessian-STF-parent-normalization-or-kH-source-coefficient.md",
            "target_script": "scripts/Y5_R2FR_3671_Hessian_STF_parent_normalization_or_kH_source_coefficient.py",
            "objective": "derive the parent/readout/Green normalization C_parent_H that maps the explicit KgammaH geometry kernel back to k_H*f_EM/Z_X, or keep the branch as a conservative bound convention",
            "success_gate": "beta_H is connected to parent-owned k_H/f_EM/Z_X coefficients, or the missing normalization is isolated as the next closure blocker without weakening the conservative kernel rows",
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    derivations: list[dict[str, object]],
    kernels: list[dict[str, object]],
    bounds: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    strongest = min(kernels, key=lambda row: float(row["beta_H_max_if_no_other_terms"]))
    lines = [
        "# 3670 - KgammaH transfer kernel or conservative linear bound",
        "",
        f"**Status:** {status[0]['summary']}",
        "",
        "This checkpoint does not merely say `K_gamma_H` is missing. It derives the part we can own from geometry:",
        "",
        "`P_TF[partial_i partial_j X]=(X''-X'/r)(rhat_i rhat_j-delta_ij/3)`",
        "",
        "`X=e^{-r/lambda}/r => X''-X'/r=e^{-r/lambda}(3/r^3+3/(lambda*r^2)+1/(lambda^2*r))`",
        "",
        "For a straight Shapiro path with `u=z/b`, the photon projection is:",
        "",
        "`n^i n^j(rhat_i rhat_j-delta_ij/3)=u^2/(1+u^2)-1/3`",
        "",
        "So the dimensionless signed kernel is:",
        "",
        "`J_H(eta,zeta)=int_{-zeta}^{zeta} e^{-sqrt(1+u^2)/eta}(3/rho^3+3/(eta*rho^2)+1/(eta^2*rho))*(u^2/(1+u^2)-1/3) du`",
        "",
        "with `eta=lambda/b`, `zeta=L/b`, `rho=sqrt(1+u^2)`, and Shapiro denominator `D=2 asinh(zeta)`. The dimensionful path kernel is `G_H/b^2`, where `G_H=J_H/D`.",
        "",
        "Because the projection changes sign at `u=1/sqrt(2)`, signed cancellation is diagnostic only. The conservative nonclaim branch uses the absolute-path kernel `J_abs/D`; it does **not** use cancellation to claim a pass.",
        "",
        f"Strongest sampled absolute-path proxy row: `{strongest['kernel_id']}` with `beta_H <= {strongest['beta_H_max_if_no_other_terms']}` if `C_other_gamma=0` and `beta_G=0`.",
        "",
        "`beta_H=|C_parent_H*k_H*f_EM/Z_X|/b^2` in the selected Shapiro normalization. `C_parent_H` is still not parent-owned, so this is not claimed as a Cassini/local-GR result.",
        "",
        "## Derivation rows",
    ]
    for row in derivations:
        lines.append(f"- `{row['derivation_id']}`: {row['status']} - `{row['formula']}`")
    lines.extend(["", "## Path kernel rows"])
    for row in kernels:
        lines.append(
            f"- `{row['kernel_id']}`: eta={row['lambda_over_b_eta']}, zeta={row['half_path_over_b_zeta']}, "
            f"G_abs={row['G_H_abs_dimensionless']}, signed/abs={row['signed_to_absolute_fraction']}, "
            f"beta_H_max={row['beta_H_max_if_no_other_terms']}"
        )
    lines.extend(["", "## Conservative bound rows"])
    for row in bounds[:5]:
        lines.append(f"- `{row['bound_id']}`: `{row['conservative_bound_formula']}`")
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
    generated = sources + derivations + kernels + bounds + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3670*", "3670-Y5-R2FR-*", "P8_Y5*3670*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))
    add("VAL3670_0_sources_exist", all(row["exists"] for row in sources), "every cited source exists")
    add("VAL3670_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3670_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3670 outputs written")
    add("VAL3670_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3670_4_derivation_clauses", {"KGD3670_1_radial_Hessian_STF", "KGD3670_2_null_projection", "KGD3670_3_dimensionless_kernel", "KGD3670_5_conservative_rule"}.issubset({str(row["derivation_id"]) for row in derivations}), "geometry derivation clauses present")
    add("VAL3670_5_kernel_grid", len(kernels) == len(LAMBDA_OVER_B_GRID) * len(HALF_PATH_OVER_B_GRID), "all eta/zeta kernel rows generated")
    add("VAL3670_6_kernel_numerics", all(float(row["J_H_abs_dimensionless"]) >= abs(float(row["J_H_signed_dimensionless"])) and float(row["D_shapiro_dimensionless"]) > 0 for row in kernels), "absolute kernels dominate signed kernels and denominators are positive")
    add("VAL3670_7_cancellation_guard", all(0 <= float(row["signed_to_absolute_fraction"]) <= 1.0000001 for row in kernels), "signed cancellation fractions bounded")
    add("VAL3670_8_bound_rows", len(bounds) == len(kernels) and all("beta_H <=" in row["conservative_bound_formula"] for row in bounds), "conservative betaH bound rows generated")
    add("VAL3670_9_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim")
    add("VAL3670_10_parent_unsigned_gate", any(row["gate_id"] == "CG3670_2_parent_normalization" and row["status"] == "FAILED_UNSIGNED" for row in gates), "parent normalization remains unsigned")
    add("VAL3670_11_doc_written", "J_H" in doc_text and "absolute-path" in doc_text and "not claimed" in doc_text, "doc records derived kernel and nonclaim status")
    add("VAL3670_12_no_formalization_leak", not leaks, "no 3670 checkpoint files in formalization-workbench")
    add("VAL3670_13_next_target", next_target[0]["target_doc"].startswith("3671-") and "parent-normalization" in next_target[0]["target_doc"], "3671 parent-normalization target selected")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    derivations = geometry_derivation_rows(ts)
    kernels = path_kernel_rows(ts)
    bounds = conservative_bound_rows(ts, kernels)
    gates = claim_gate_rows(ts)
    status = status_rows(ts, kernels)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3670_SOURCE_REGISTER.csv",
        "derivations": RESIDUALS / "P8_Y5_R2FR_3670_KGAMMAH_GEOMETRY_DERIVATION_ROWS.csv",
        "kernels": RESIDUALS / "P8_Y5_R2FR_3670_KGAMMAH_PATH_KERNEL_ROWS.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3670_CONSERVATIVE_BETAH_BOUND_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3670_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3670_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3670_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3670_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["derivations"], derivations)
    write_csv(outputs["kernels"], kernels)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, derivations, kernels, bounds, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, derivations, kernels, bounds, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3670 validation failed: {failures}", file=sys.stderr)
        return 1
    print(f"wrote 3670 checkpoint with {len(validation)} validation checks; KgammaH geometry kernel derived, parent normalization unsigned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
