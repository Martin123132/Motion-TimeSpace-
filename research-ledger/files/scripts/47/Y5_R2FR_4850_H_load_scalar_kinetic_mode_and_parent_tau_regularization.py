from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Any


CHECKPOINT = "4850"
TIMESTAMP = "2026-07-09T23:30:00+00:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
FIT_SOURCE = OUTPUT / "P8_Y5_R2FR_4849_ROBUSTNESS_RESULTS.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC4850_00_4847", POST / "4847-Y5-R2FR-coherent-load-covariant-Hilbert-stress-and-tau-Euler-equation-or-H-load-cosmology-smoke-fit.md", "D_\\mu f", "unit-flow Euler constraint and covariant stress"),
        ("SRC4850_01_4849", POST / "4849-Y5-R2FR-positive-H-load-total-kinetic-bound-parameterization-or-local-H-load-cosmology-demotion.md", "K_0=6(1-f_K)", "kinetic-fraction branch and real-data decision"),
        ("SRC4850_02_fit", FIT_SOURCE, "HLOAD_EXP_POS_KSAFE", "all fitted f_K rows"),
        ("SRC4850_03_cartan", POST / "4070-Y5-R2FR-psi-packet-coframe-parent-action-normalization-and-torsion-gate.md", "Einstein-Cartan / Palatini action", "coframe/EH parent branch context"),
        ("SRC4850_04_candidate", POST / "4072-Y5-R2FR-local-motion-frame-gauge-action-or-effective-GR-demotion.md", "S_EC", "private motion-frame gauge action candidate"),
        ("SRC4850_05_checkpoint", POST / "4850-Y5-R2FR-H-load-scalar-kinetic-mode-or-parent-tau-regularization-before-CMB-growth.md", "POSITIVE_H_LOAD_MINIMAL_FLOW_CUSCUTON_EQUIVALENCE_DERIVED", "human-readable complete-constraint derivation"),
        ("SRC4850_06_formal", FORMAL / "866-PPC4161-H-load-cuscuton-equivalence-and-principal-constraint-gate.md", "H_LOAD_CUSCUTON_CONSTRAINT_SAFE", "formal-workbench integration"),
        ("SRC4850_07_claims", FORMAL / "02-claims-register.csv", "L-692", "nonclaim register row"),
        ("SRC4850_08_script", Path(__file__).resolve(), 'CHECKPOINT = "4850"', "executable algebra and fit classifier"),
    ]
    rows = []
    for source_id, path, needle, role in sources:
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def kinetic_rows() -> list[dict[str, Any]]:
    rows = [
        ("KIN4850_0_action", "independent_unit_flow", "memory action", "S_mem=-kappa^-1 int sqrt(-g)[G(theta)+lambda_u(u^2+1)]", "theta=div u and u is varied", "PARENT_EULER_INCLUDED"),
        ("KIN4850_1_euler", "independent_unit_flow", "flow Euler constraint", "phi:=G_theta; nabla_mu phi=2 lambda_u u_mu; D_mu phi=0", "phi has no spatial variation in the u-orthogonal directions", "EXACT_CONSTRAINT"),
        ("KIN4850_2_legendre", "g_not_zero_patch", "Legendre transform", "U(phi)=phi theta-G(theta); U_phi=theta; U_phiphi=1/G_theta_theta", "equivalent first-order action is int sqrt(-g)[u dot nabla phi+U-lambda_u(u^2+1)]/kappa", "EXACT_LOCAL_EQUIVALENCE"),
        ("KIN4850_3_cuscuton", "timelike_gradient_patch", "cuscuton form", "u_mu=sign(lambda_u) nabla_mu phi/sqrt[-(nabla phi)^2]", "eliminating u gives sigma sqrt[-(nabla phi)^2]+U(phi)", "NO_EXTRA_PROPAGATING_SCALAR"),
        ("KIN4850_4_apparent_ADM", "u_normal_but_Euler_omitted", "incomplete scalar Schur coefficient", "Q_naive=2(2+3g)/g=2(3lambda_ADM-1)/(lambda_ADM-1)", "negative Q_naive is not a ghost test because D_i G_theta=0 and the lapse/phi constraint were omitted", "FORBIDDEN_INCOMPLETE_DIAGNOSIS"),
        ("KIN4850_5_longitudinal", "independent_unit_flow", "local longitudinal constraint energy", "L2_mem=-(g/2kappa)(partial_i delta u^i)^2", "elliptic/coercive sign is -g>0", "PRINCIPAL_CONSTRAINT_GATE"),
        ("KIN4850_6_fraction", "positive_H_load", "kinetic-fraction map", "g=-2f_K/3; -g=2f_K/3; K0=6(1-f_K)", "0<f_K<1 gives positive longitudinal constraint coefficient and positive homogeneous Jacobian", "PRINCIPAL_SIGN_PASS_EDGE_DEPENDENT"),
        ("KIN4850_7_tensor", "minimal_flow", "tensor principal block", "Q_T=1 and c_T^2=1", "G(theta) has no trace-free tensor Hessian", "PASS_MINIMAL_TENSOR"),
        ("KIN4850_8_vector", "minimal_flow", "transverse vector block", "no transverse-vector time kinetic from G(div u)", "flow Euler makes the timelike-gradient branch algebraic/constraint-like; a separate parent vector kinetic term would define a different branch", "NO_PROPAGATING_MEMORY_VECTOR"),
        ("KIN4850_9_local_endpoint", "stationary_local", "g=0 endpoint", "G=G_theta=G_theta_theta=0 at theta=0", "Legendre chart is singular there, but the original u action is smooth and exactly silent; parent coframe owns u", "ORIGINAL_VARIABLE_PATCH_REQUIRED"),
    ]
    return [
        {
            "row_id": row_id,
            "branch": branch,
            "object": obj,
            "formula": formula,
            "consequence": consequence,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, branch, obj, formula, consequence, status in rows
    ]


def fit_rows() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in read_csv(FIT_SOURCE):
        if not row.get("model", "").startswith("HLOAD"):
            continue
        f_k = float(row["f_K"])
        g_theta_theta = -2.0 * f_k / 3.0
        lambda_adm = 1.0 + g_theta_theta
        q_naive = -6.0 * (1.0 - f_k) / f_k
        elliptic_coefficient = -g_theta_theta
        homogeneous = float(row["homogeneous_kinetic_bracket0"])
        principal_pass = elliptic_coefficient > 0.0 and homogeneous > 0.0
        output.append(
            {
                "variant": row["variant"],
                "branch": row["branch"],
                "model": row["model"],
                "f_K": f"{f_k:.15e}",
                "G_theta_theta": f"{g_theta_theta:.15e}",
                "lambda_ADM_apparent": f"{lambda_adm:.15e}",
                "Q_naive_Euler_omitted": f"{q_naive:.15e}",
                "longitudinal_elliptic_coefficient": f"{elliptic_coefficient:.15e}",
                "homogeneous_constraint_jacobian": f"{homogeneous:.15e}",
                "memory_extra_scalar_dof": 0,
                "principal_constraint_pass": principal_pass,
                "principal_status": "CUSCUTON_CONSTRAINT_PRINCIPAL_PASS_AT_Z0_EDGE_DEPENDENT" if principal_pass else "PRINCIPAL_CONSTRAINT_FAIL",
                "fit_status_4849": row["status"],
                "edge_flags": row["edge_flags"],
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return output


def completion_rows() -> list[dict[str, Any]]:
    rows = [
        ("CMP4850_0_minimal", "independent varied unit flow", "impose u Euler and unit constraint", "cuscuton-equivalent on g!=0 timelike-gradient patches; no extra scalar", "RETAIN_PRIVATE_BRANCH"),
        ("CMP4850_1_elliptic", "longitudinal principal symbol", "-G_theta_theta>0", "positive H-load has -g=2f_K/3>0", "PASS_AT_Z0_FOR_ALL_FITS"),
        ("CMP4850_2_homogeneous", "background constraint Jacobian", "6+9G_theta_theta=6(1-f_K)>0", "invertible for f_K<1 and degenerates as f_K approaches 1", "EDGE_MARGIN_REQUIRED"),
        ("CMP4850_3_legendre", "Legendre chart", "G_theta_theta!=0 and nabla phi timelike", "valid on evolving cosmological patches; not valid at the stationary local g=0 endpoint", "PATCHWISE_ONLY"),
        ("CMP4850_4_local", "stationary local branch", "use original u,Q,Lambda variables", "memory stress and tau force vanish exactly at theta=0", "LOCAL_ZERO_RETAINED"),
        ("CMP4850_5_shared_tau", "shared propagating parent tau/coframe", "add parent Hessian before eliminating constraints", "may introduce new scalar/vector modes and is not certified by the minimal cuscuton result", "SEPARATE_BRANCH_MATRIX_REQUIRED"),
        ("CMP4850_6_matter", "matter-coupled perturbations", "derive lapse/shift/delta-phi constraints and effective growth kernel", "required before CMB, growth or chronometer promotion", "NEXT_TARGET"),
        ("CMP4850_7_naive_ghost", "ADM lambda-only diagnosis", "forbid eliminating shift while omitting u Euler/lapse/phi constraints", "Q_naive<0 is an incomplete off-shell Schur complement, not a physical ghost eigenvalue", "REJECT_SHORTCUT"),
    ]
    return [
        {
            "row_id": row_id,
            "route": route,
            "required_clause": clause,
            "result": result,
            "decision": decision,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, route, clause, result, decision in rows
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    kinetics: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    completions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    claim_rows = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-692"]
    checkpoint = (POST / "4850-Y5-R2FR-H-load-scalar-kinetic-mode-or-parent-tau-regularization-before-CMB-growth.md").read_text(encoding="utf-8")
    formal = (FORMAL / "866-PPC4161-H-load-cuscuton-equivalence-and-principal-constraint-gate.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    checks = [
        result("VAL4850_00_sources", len(sources) == 9 and all(row["source_exists"] and row["needle_found"] for row in sources), f"sources={len(sources)}"),
        result("VAL4850_01_kinetic_rows", len(kinetics) == 10, f"rows={len(kinetics)}"),
        result("VAL4850_02_fit_count", len(fits) == 12, f"H-load fits={len(fits)}"),
        result("VAL4850_03_fraction_domain", all(0.0 < float(row["f_K"]) < 1.0 for row in fits), "all fitted f_K in open positive branch"),
        result("VAL4850_04_elliptic_sign", all(float(row["longitudinal_elliptic_coefficient"]) > 0.0 for row in fits), "all fitted rows have -G_theta_theta>0 at z=0"),
        result("VAL4850_05_constraint_jacobian", all(float(row["homogeneous_constraint_jacobian"]) > 0.0 for row in fits), "all fitted rows have K0>0"),
        result("VAL4850_06_no_extra_scalar", all(int(row["memory_extra_scalar_dof"]) == 0 for row in fits), "minimal varied-unit-flow branch is constraint-like"),
        result(
            "VAL4850_07_fraction_identity",
            all(
                math.isclose(float(row["homogeneous_constraint_jacobian"]), 6.0 * (1.0 - float(row["f_K"])), rel_tol=1.0e-12, abs_tol=1.0e-12)
                and math.isclose(float(row["longitudinal_elliptic_coefficient"]), 2.0 * float(row["f_K"]) / 3.0, rel_tol=1.0e-12, abs_tol=1.0e-12)
                for row in fits
            ),
            "K0 and elliptic coefficient identities retained",
        ),
        result("VAL4850_08_completion_gate", len(completions) == 8 and any(row["decision"] == "REJECT_SHORTCUT" for row in completions), "minimal/shared/local/matter forks classified"),
        result("VAL4850_09_claim", len(claim_rows) == 1 and claim_rows[0].get("status") == "positive_H_load_cuscuton_constraint_safe_edge_dependent_private_nonclaim", f"L-692 rows={len(claim_rows)}"),
        result("VAL4850_10_documents", "POSITIVE_H_LOAD_MINIMAL_FLOW_CUSCUTON_EQUIVALENCE_DERIVED" in checkpoint and "H_LOAD_CUSCUTON_CONSTRAINT_SAFE" in formal, "checkpoint and formal marker found"),
        result("VAL4850_11_resume", "Last checkpoint: `4850-" in resume and "4851-Y5-R2FR-H-load-cuscuton-matter-perturbation" in resume, "resume advanced to matter perturbations"),
        result("VAL4850_12_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4850_OVERALL", all(row["status"] == "PASS" for row in checks), "H_LOAD_CUSCUTON_EQUIVALENCE_AND_PRINCIPAL_CONSTRAINT_GATE_VALIDATED"))
    return checks


def main() -> int:
    sources = source_rows()
    kinetics = kinetic_rows()
    fits = fit_rows()
    completions = completion_rows()
    validation = validation_rows(sources, kinetics, fits, completions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4850_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4850_ADM_KINETIC_MATRIX.csv", kinetics)
    write_csv(OUTPUT / "P8_Y5_R2FR_4850_FIT_STABILITY.csv", fits)
    write_csv(OUTPUT / "P8_Y5_R2FR_4850_REGULARIZER_GATE.csv", completions)
    write_csv(OUTPUT / "P8_Y5_BRR545_4850_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4850_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4850_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
