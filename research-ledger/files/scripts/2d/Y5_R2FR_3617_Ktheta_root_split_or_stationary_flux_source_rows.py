from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
EXTERNAL = ROOT / "source-intake" / "external" / "arxiv_1905_03413"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3617"
BRANCH_ID = "MTS_R2FR_Y5_KTHETA_ROOT_SPLIT_OR_STATIONARY_FLUX_SOURCE_ROWS_3617"
DOC = ROOT / "3617-Y5-R2FR-Ktheta-root-split-or-stationary-flux-source-rows.md"
ARXIV_URL = "https://arxiv.org/abs/1905.03413"
OMEGA_M = 0.315
OMEGA_LAMBDA = 0.685


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8-sig", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3617_SOURCE_REGISTER.csv",
        "root_split_derivation": RESIDUALS / "P8_Y5_R2FR_3617_KTHETA_SCREEN_ROOT_SPLIT_DERIVATION.csv",
        "energy_scaling_ledger": RESIDUALS / "P8_Y5_R2FR_3617_ENERGY_SCALING_LEDGER.csv",
        "bandpass_integrals": RESIDUALS / "P8_Y5_R2FR_3617_GRB_BANDPASS_INTEGRALS.csv",
        "projection_runner": RESIDUALS / "P8_Y5_R2FR_3617_KTHETA_PROJECTION_RUNNER.csv",
        "htau_stationary_source_rows": RESIDUALS / "P8_Y5_R2FR_3617_HTAU_STATIONARY_SOURCE_ROWS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3617_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3617_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3617_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Ktheta_root_split_or_stationary_flux_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3617_VALIDATION.csv",
    }


def source_map() -> dict[str, tuple[Path, str]]:
    return {
        "handoff_3616": (
            RESIDUALS / "P8_Y5_R2FR_3616_NEXT_TARGET.csv",
            "3617-Y5-R2FR-Ktheta-root-split-or-stationary-flux-source-rows.md",
        ),
        "projection_3616": (
            RESIDUALS / "P8_Y5_R2FR_3616_FRESNEL_TO_XI_PROJECTION_DERIVATION.csv",
            "K_Fresnel",
        ),
        "runner_3616": (
            RESIDUALS / "P8_Y5_R2FR_3616_PROJECTION_RUNNER_TEMPLATE.csv",
            "GRB 061122",
        ),
        "bound_3615": (
            RESIDUALS / "P8_Y5_R2FR_3615_BFRESNEL_PRIMARY_BOUND_ACQUISITION.csv",
            "BFB3615_0_GRB061122",
        ),
        "principal_3614": (
            RESIDUALS / "P8_Y5_R2FR_3614_PRINCIPAL_HODGE_BOUND.csv",
            "Delta_chi_principal",
        ),
        "chi_reconstruct_3287": (
            RESIDUALS / "P8_Y5_R2FR_3287_CHI_TO_HODGE_RECONSTRUCTION_THEOREM.csv",
            "nonbirefringence reconstructs conformal metric",
        ),
        "wei_2019_source": (
            EXTERNAL / "ms.tex",
            "H_{0}=67.3",
        ),
        "htau_backup_3616": (
            RESIDUALS / "P8_Y5_R2FR_3616_HTAU_FLUX_BACKUP_REDUCTION.csv",
            "S_Poynting.n=0",
        ),
    }


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for source_id, source_data in source_map().items():
        source_path, needle = source_data
        exists = source_path.exists()
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(source_path),
                "source_url": ARXIV_URL if source_id == "wei_2019_source" else "",
                "exists": exists,
                "needle": needle,
                "needle_found": exists and contains(source_path, needle),
                "valid_for_claim": False,
            }
        )
    return rows


def e_z(redshift: float) -> float:
    return math.sqrt(OMEGA_M * (1.0 + redshift) ** 3 + OMEGA_LAMBDA)


def integral_i(redshift: float, exponent: float, steps: int = 4000) -> float:
    if steps % 2:
        steps += 1
    h = redshift / steps
    total = 0.0
    for idx in range(steps + 1):
        z_value = idx * h
        weight = 4.0 if idx % 2 else 2.0
        if idx in (0, steps):
            weight = 1.0
        total += weight * (1.0 + z_value) ** exponent / e_z(z_value)
    return total * h / 3.0


def parse_energy_range_keV(value: str) -> tuple[float, float, float]:
    cleaned = value.replace("—", "-").replace("---", "-").replace("–", "-").replace(" ", "")
    lo_text, hi_text = cleaned.split("-", 1)
    lo = float(lo_text)
    hi = float(hi_text)
    return lo, hi, math.sqrt(lo * hi)


def root_split_derivation_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "KTD3617_0_scalar_warning",
            "target": "avoid scalar double-root instability",
            "statement": "A scalar quartic residual alone is a bad primary variable near a repeated GR light cone: generic polynomial perturbations give square-root root motion unless the polarization operator structure is used.",
            "formula": "F=u^2+a u+b gives Delta_u=sqrt(a^2-4b)",
            "derived_result": "do not claim a linear K_theta from scalar B_Fresnel unless a,b are supplied by a reciprocal screen operator",
            "status": "DERIVED_WARNING_ROUTE_REJECTED_FOR_CLAIMS",
            "source_path": str(sources["projection_3616"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "KTD3617_1_screen_operator",
            "target": "physical polarization screen",
            "statement": "Use the two-dimensional transverse polarization screen instead of the scalar quartic as the primary perturbation object.",
            "formula": "h_AB(k,U)=omega^-2 e_A^a delta P_ab(k) e_B^b; A,B=1,2",
            "derived_result": "h_AB is the normalized reciprocal principal-symbol perturbation on the physical screen",
            "status": "KTHETA_OBJECT_DERIVED_SYMBOLIC",
            "source_path": str(sources["principal_3614"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "KTD3617_2_mode_root_shift",
            "target": "root shift per polarization",
            "statement": "In a normalized Maxwell/GR branch, the two light-cone shifts are the screen eigenvalues divided by the unperturbed cone slope.",
            "formula": "delta u_pm = -omega^2 lambda_pm(h)/gamma0",
            "derived_result": "Delta_u = omega^2 diam_spec(h)/gamma0",
            "status": "ROOT_SPLIT_LAW_DERIVED_SYMBOLIC",
            "source_path": str(sources["chi_reconstruct_3287"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "KTD3617_3_frequency_split",
            "target": "phase/frequency splitting",
            "statement": "For u=-omega^2+|p|^2, the background slope is |partial_omega u|=2 omega, so frequency split is linear in the screen spectral diameter.",
            "formula": "Delta_omega = omega diam_spec(h)/(2 gamma0)",
            "derived_result": "Delta_theta_MTS = integral omega diam_spec(h)/(4 gamma0) dt",
            "status": "KTHETA_PHASE_LAW_DERIVED",
            "source_path": str(sources["projection_3616"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "KTD3617_4_energy_power_law",
            "target": "cosmological projection",
            "statement": "If the MTS screen diameter obeys an owned power law, diam_spec(h)<=C_screen B_Fresnel_MTS (k/M_*)^s, then K_theta is explicit.",
            "formula": "K_theta(s)=C_screen k0^(s+1) I_s(z)/(4 gamma0 M_*^s H0)",
            "derived_result": "I_s(z)=int_0^z (1+z')^s dz'/sqrt(Omega_m(1+z')^3+Omega_Lambda)",
            "status": "KTHETA_DERIVED_CONDITIONAL_ON_ENERGY_POWER",
            "source_path": str(sources["wei_2019_source"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "KTD3617_5_xi_projection",
            "target": "map into Wei xi bound",
            "statement": "Combining 3616's xi inversion with the screen split law gives the explicit nonclaim projection coefficient.",
            "formula": "K_Fresnel(s)=C_screen M_pl I_s(z)/(4 gamma0 M_*^s k0^(1-s) I_1(z))",
            "derived_result": "abs(xi_MTS_eff)<=K_Fresnel(s) B_Fresnel_MTS",
            "status": "K_FRESNEL_FORM_DERIVED_SYMBOLIC",
            "source_path": str(sources["projection_3616"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "KTD3617_6_s_equal_1_special_case",
            "target": "least-scrutiny GRB-compatible scaling",
            "statement": "For an owned linear-in-energy birefringent branch, the GRB projection has the same redshift kernel as the source model.",
            "formula": "s=1 => K_Fresnel=C_screen M_pl/(4 gamma0 M_*)",
            "derived_result": "if M_*=M_pl and C_screen=gamma0=1, xi_MTS_eff <= B_Fresnel_MTS/4",
            "status": "SPECIAL_CASE_DERIVED_NONCLAIM",
            "source_path": str(sources["wei_2019_source"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "KTD3617_7_claim_gate",
            "target": "claim discipline",
            "statement": "The route is now mathematically sharper, but it still needs parent ownership of h_AB, s, M_*, gamma0, C_screen and B_Fresnel_MTS before any GRB score is valid.",
            "formula": "claim_allowed iff all parent/source inputs exist and abs(K_Fresnel B_Fresnel_MTS)<=xi_bound",
            "derived_result": "current checkpoint supplies the symbolic Ktheta law, not a pass",
            "status": "NO_CLAIM_GATE_RETAINED",
            "source_path": str(sources["runner_3616"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def energy_scaling_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "scaling_id": "ESL3617_0_s0",
            "energy_power_s": 0,
            "interpretation": "energy-independent principal constitutive anisotropy",
            "projection_formula": "K_Fresnel=C_screen M_pl I_0/(4 gamma0 k0 I_1)",
            "physics_read": "usually brutally constrained by GRB polarimetry unless B_Fresnel_MTS is tiny",
            "parent_status": "NOT_SELECTED_PARENT_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "scaling_id": "ESL3617_1_s1",
            "energy_power_s": 1,
            "interpretation": "linear-in-energy birefringent screen perturbation",
            "projection_formula": "K_Fresnel=C_screen M_pl/(4 gamma0 M_*)",
            "physics_read": "best-matched route to the acquired Wei GRB xi bound; still needs parent derivation of M_* and h_AB",
            "parent_status": "PROMISING_ROUTE_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "scaling_id": "ESL3617_2_s2",
            "energy_power_s": 2,
            "interpretation": "quadratic-in-energy higher-order branch",
            "projection_formula": "K_Fresnel=C_screen M_pl k0 I_2/(4 gamma0 M_*^2 I_1)",
            "physics_read": "less constrained at keV energies if M_* is high, but must come from parent operator dimension",
            "parent_status": "ALTERNATE_ROUTE_NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bandpass_integral_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    for bound_row in read_csv(source_map()["bound_3615"][0]):
        z_value = float(bound_row["redshift"])
        e_min, e_max, e_eff = parse_energy_range_keV(bound_row["energy_range_keV"])
        i0 = integral_i(z_value, 0.0)
        i1 = integral_i(z_value, 1.0)
        i2 = integral_i(z_value, 2.0)
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "object": bound_row["object"],
                "redshift": z_value,
                "energy_min_keV": e_min,
                "energy_max_keV": e_max,
                "energy_eff_geom_keV": e_eff,
                "Omega_m": OMEGA_M,
                "Omega_Lambda": OMEGA_LAMBDA,
                "I0": f"{i0:.10g}",
                "I1_source_kernel": f"{i1:.10g}",
                "I2": f"{i2:.10g}",
                "I0_over_I1": f"{i0 / i1:.10g}",
                "I2_over_I1": f"{i2 / i1:.10g}",
                "source_path": str(source_map()["wei_2019_source"][0]),
                "score_status": "KERNELS_COMPUTED_NONCLAIM",
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def projection_runner_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows = []
    bound_rows = read_csv(source_map()["bound_3615"][0])
    integral_by_object = {row["object"]: row for row in bandpass_integral_rows()}
    for bound_row in bound_rows:
        kernel = integral_by_object[bound_row["object"]]
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "runner_id": f"KTR3617_{len(rows)}_{bound_row['object'].replace(' ', '')}",
                "object": bound_row["object"],
                "xi_bound": bound_row["bound_value"],
                "Ktheta_formula": "K_theta(s)=C_screen k0^(s+1) I_s/(4 gamma0 M_*^s H0)",
                "Kfresnel_formula": "K_Fresnel(s)=C_screen M_pl I_s/(4 gamma0 M_*^s k0^(1-s) I_1)",
                "s1_special_formula": "s=1 => K_Fresnel=C_screen M_pl/(4 gamma0 M_*)",
                "I0_over_I1": kernel["I0_over_I1"],
                "I2_over_I1": kernel["I2_over_I1"],
                "missing_parent_inputs": "h_AB ownership; energy_power_s; M_star; gamma0; C_screen; B_Fresnel_MTS",
                "result": "BLOCKED_SYMBOLIC_KTHETA_DERIVED",
                "can_score": False,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def htau_stationary_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    sources = source_map()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "HSR3617_0_EH_stationary_source_row",
            "quantity": "I_EH_stationary_boundary",
            "zero_clause": "Lie_tau g=0; N_AB=0; delta C_corner=0",
            "source_bound_row": "I_EH <= C_news||N_AB|| + C_stat||Lie_tau h_ab|| + C_corner|delta C_corner|",
            "status": "SOURCE_ROW_TEMPLATE_READY_NOT_ACTIVATED",
            "source_path": str(sources["htau_backup_3616"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "row_id": "HSR3617_1_matter_EM_no_flux_source_row",
            "quantity": "I_matter_EM_flux",
            "zero_clause": "Lie_tau Psi=0; Lie_tau A=0; T_matter(tau,n)=0; S_Poynting.n=0",
            "source_bound_row": "I_matter_EM_flux <= int_S(|T_matter(tau,n)|+|S_Poynting.n|)dA + C_L||Lie_tau(Psi,A)|| + C_surface|delta C_tau|",
            "status": "SOURCE_ROW_TEMPLATE_READY_NOT_ACTIVATED",
            "source_path": str(sources["htau_backup_3616"][0]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3617_0_Ktheta_derived",
            "decision": "K_theta is derived symbolically from the physical two-polarization screen operator, avoiding the scalar double-root trap.",
            "status": "PASS_DERIVATION_NONCLAIM",
            "next_action": "parent-own h_AB and the energy power law",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3617_1_energy_scaling_pressure",
            "decision": "The best route is s=1 because it maps cleanly to the GRB xi kernel; s=0 is likely too constrained unless amplitude is extremely small.",
            "status": "ROUTE_RANKED_NOT_SELECTED_BY_FIAT",
            "next_action": "derive s and M_* from parent operator dimension rather than choose by hand",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3617_2_runner_blocked_correctly",
            "decision": "The runner now has kernels and formulas but still refuses to score without parent amplitude and scale.",
            "status": "PASS_BLOCKED_CORRECTLY",
            "next_action": "fill B_Fresnel_MTS or prove h_AB=0 in the local branch",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3617_3_next_target",
            "decision": "3618 should attack parent ownership of the screen perturbation h_AB and its energy exponent.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3618-Y5-R2FR-screen-operator-parent-origin-or-energy-scaling-gate.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3617_0",
            "result": "KTHETA_SYMBOLIC_DERIVED_PARENT_SCREEN_INPUTS_MISSING",
            "summary": "3617 derives the root-split coefficient through the physical polarization-screen operator and computes GRB kernel rows; scoring remains blocked until h_AB, energy power s, M_*, gamma0, C_screen and B_Fresnel_MTS are parent-owned.",
            "Ktheta_derived": True,
            "GRB_kernels_computed": True,
            "preferred_route": "derive s=1 from parent operator if possible, not by fiat",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3617_0",
            "target_doc": "3618-Y5-R2FR-screen-operator-parent-origin-or-energy-scaling-gate.md",
            "target_script": "scripts/Y5_R2FR_3618_screen_operator_parent_origin_or_energy_scaling_gate.py",
            "objective": "derive whether the parent MTS action gives h_AB=0 in the local Maxwell/GR branch, or if not, derive the energy exponent s, scale M_*, gamma0 and C_screen for the surviving screen perturbation",
            "success_gate": "either h_AB is theorem-zero from local Hodge/same-metric descent, or a parent-owned nonzero h_AB row with s, M_*, gamma0, C_screen and B_Fresnel_MTS is produced",
            "reason": "3617 produced the Ktheta bridge; the next real gap is parent origin of the screen perturbation and energy scaling.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "Ktheta": "DERIVED_SYMBOLIC_SCREEN_OPERATOR",
            "scalar_double_root_route": "REJECTED_FOR_CLAIMS_WITHOUT_SCREEN_STRUCTURE",
            "GRB_kernels": "COMPUTED_NONCLAIM",
            "missing_core_input": "parent h_AB, s, M_*, gamma0, C_screen, B_Fresnel_MTS",
            "claim_status": "NO_CLAIM",
            "next_target": "3618 screen operator parent origin or energy-scaling gate",
            "valid_for_claim": False,
        }
    ]


def write_markdown() -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3617 Y5 R2FR: K_theta root split or stationary flux source rows",
                "",
                "## Verdict",
                "- The useful derivation route is the polarization-screen operator, not a raw scalar quartic residual.",
                "- `K_theta` is now derived symbolically: it maps the normalized screen spectral split into accumulated polarization rotation.",
                "- This is real progress, but still no claim: the parent action must own the screen perturbation `h_AB`, its energy power `s`, the scale `M_*`, and the amplitude `B_Fresnel_MTS`.",
                "",
                "## Why the scalar route is rejected",
                "- A scalar quartic written as `F=u^2+a u+b` has root split `Delta_u=sqrt(a^2-4b)`.",
                "- Near a repeated GR cone, that is not a safe linear bound unless the underlying reciprocal two-polarization operator is supplied.",
                "- So the framework should not pretend that a scalar `B_Fresnel` number alone gives a clean `K_theta`.",
                "",
                "## Screen-operator derivation",
                "- Define the physical transverse screen perturbation `h_AB(k,U)=omega^-2 e_A^a delta P_ab(k) e_B^b`.",
                "- Mode shifts: `delta u_pm = -omega^2 lambda_pm(h)/gamma0`.",
                "- Frequency split: `Delta_omega = omega diam_spec(h)/(2 gamma0)`.",
                "- Polarization rotation: `Delta_theta_MTS = integral omega diam_spec(h)/(4 gamma0) dt`.",
                "",
                "## Cosmological K_theta",
                "- If `diam_spec(h)<=C_screen B_Fresnel_MTS (k/M_*)^s`, then",
                "- `K_theta(s)=C_screen k0^(s+1) I_s(z)/(4 gamma0 M_*^s H0)`.",
                "- `I_s(z)=int_0^z (1+z')^s dz'/sqrt(Omega_m(1+z')^3+Omega_Lambda)`.",
                "- Into the Wei GRB `xi` convention:",
                "- `K_Fresnel(s)=C_screen M_pl I_s(z)/(4 gamma0 M_*^s k0^(1-s) I_1(z))`.",
                "- Special case `s=1`: `K_Fresnel=C_screen M_pl/(4 gamma0 M_*)`.",
                "",
                "## Practical read",
                "- `s=1` is the least awkward route because it shares the same redshift/energy kernel as the acquired GRB bound.",
                "- `s=0` is likely brutally constrained unless the local amplitude is tiny or theorem-zero.",
                "- The next derivation must not choose `s=1` by taste; it has to come from the parent operator dimension or a high-frequency relic/flow mechanism.",
                "",
                "## Outputs",
                "- `P8_Y5_R2FR_3617_KTHETA_SCREEN_ROOT_SPLIT_DERIVATION.csv` contains the derivation.",
                "- `P8_Y5_R2FR_3617_GRB_BANDPASS_INTEGRALS.csv` contains the GRB redshift kernels.",
                "- `P8_Y5_R2FR_3617_KTHETA_PROJECTION_RUNNER.csv` contains a blocked-but-ready comparator.",
                "- `P8_Y5_R2FR_3617_HTAU_STATIONARY_SOURCE_ROWS.csv` preserves the backup flux route.",
                "",
                "## Next target",
                "- `3618-Y5-R2FR-screen-operator-parent-origin-or-energy-scaling-gate.md`.",
                "- Best route: prove `h_AB=0` from local Hodge/same-metric descent, or derive the nonzero branch's `s`, `M_*`, `gamma0`, `C_screen`, and `B_Fresnel_MTS`.",
                "",
                "## Claim status",
                "- `NO_CLAIM`: this checkpoint derives the bridge, not the amplitude.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    results: list[tuple[str, bool, str]] = []

    sources = source_map()
    sources_exist = all(source_path.exists() for source_path, _needle in sources.values())
    needles_found = all(source_path.exists() and contains(source_path, needle) for source_path, needle in sources.values())
    results.append(("VAL3617_0_sources_exist", sources_exist, "all required 3617 source paths exist"))
    results.append(("VAL3617_1_needles_found", needles_found, "all selected 3617 source anchors found"))

    pre_validation_paths = [path for name, path in paths.items() if name != "validation"]
    outputs_exist = DOC.exists() and all(path.exists() for path in pre_validation_paths)
    results.append(("VAL3617_2_outputs_exist", outputs_exist, "all pre-validation 3617 outputs written"))

    parse_details: list[str] = []
    csv_parse_pass = True
    for name, path in paths.items():
        if name == "validation":
            continue
        try:
            parse_details.append(f"{name}:{len(read_csv(path))}")
        except Exception as exception:
            csv_parse_pass = False
            parse_details.append(f"{name}:ERROR:{exception}")
    results.append(("VAL3617_3_csv_parse", csv_parse_pass, "; ".join(parse_details)))

    derivation_rows = read_csv(paths["root_split_derivation"]) if paths["root_split_derivation"].exists() else []
    screen_operator_written = any("h_AB" in row["formula"] for row in derivation_rows)
    ktheta_written = any("K_theta(s)" in row["formula"] for row in derivation_rows)
    s1_written = any("s=1" in row["formula"] and "B_Fresnel_MTS/4" in row["derived_result"] for row in derivation_rows)
    scalar_warning_written = any(row["status"] == "DERIVED_WARNING_ROUTE_REJECTED_FOR_CLAIMS" for row in derivation_rows)
    results.append(("VAL3617_4_screen_operator_written", screen_operator_written, "screen h_AB operator written"))
    results.append(("VAL3617_5_Ktheta_formula_written", ktheta_written, "Ktheta formula written"))
    results.append(("VAL3617_6_s1_special_case_written", s1_written, "s=1 special case written"))
    results.append(("VAL3617_7_scalar_route_guarded", scalar_warning_written, "scalar double-root route guarded"))

    integral_rows = read_csv(paths["bandpass_integrals"]) if paths["bandpass_integrals"].exists() else []
    integrals_positive = bool(integral_rows) and all(
        float(row["I0"]) > 0.0 and float(row["I1_source_kernel"]) > 0.0 and float(row["I2"]) > 0.0
        for row in integral_rows
    )
    results.append(("VAL3617_8_grb_integrals_positive", integrals_positive, "GRB cosmological kernels are positive"))

    runner_rows = read_csv(paths["projection_runner"]) if paths["projection_runner"].exists() else []
    runner_blocks = bool(runner_rows) and all(
        row["result"] == "BLOCKED_SYMBOLIC_KTHETA_DERIVED" and row["can_score"] == "False"
        for row in runner_rows
    )
    results.append(("VAL3617_9_runner_blocks_without_parent_inputs", runner_blocks, "projection runner blocks without parent inputs"))

    all_outputs_nonclaim = True
    for name, path in paths.items():
        if name == "validation" or not path.exists():
            continue
        for row in read_csv(path):
            if row.get("valid_for_claim") == "True" or row.get("claim_allowed") == "True":
                all_outputs_nonclaim = False
    results.append(("VAL3617_10_all_outputs_nonclaim", all_outputs_nonclaim, "all generated rows remain nonclaim"))

    formalization_clean = True
    formalization_detail = "formalization-workbench not found"
    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3617*"))
        formalization_clean = len(leaked_paths) == 0
        formalization_detail = "no 3617 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    results.append(("VAL3617_11_no_formalization_leak", formalization_clean, formalization_detail))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["root_split_derivation"], root_split_derivation_rows())
    write_csv(paths["energy_scaling_ledger"], energy_scaling_rows())
    write_csv(paths["bandpass_integrals"], bandpass_integral_rows())
    write_csv(paths["projection_runner"], projection_runner_rows())
    write_csv(paths["htau_stationary_source_rows"], htau_stationary_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3617 validation failed: {failed}")
    print(f"wrote 3617 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
