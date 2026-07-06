from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    row_list = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in row_list:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def hessian_readout_rows() -> List[Dict[str, object]]:
    return [
        {
            "readout_id": "HMR4487_0_exterior_footprint",
            "object": "K_L exterior Hessian carrier",
            "derived_statement": "The exterior l=2 Hessian carrier has zero projected D2 source but a nonzero full tensor footprint.",
            "formula": "phi_ext=C*r^-3*P2(a.n); D2[C*r^-3]=0; <K_L:K_L>_Omega=336*C^2*r^-10",
            "consequence": "D2 source silence is not metric silence.",
            "status": "NONZERO_TENSOR_FOOTPRINT_CARRIED",
            "valid_for_claim": False,
        },
        {
            "readout_id": "HMR4487_1_identity_metric_readout",
            "object": "same-frame public weak-field metric",
            "derived_statement": "For ds^2=-(1+2Phi)dt^2+(1-2Psi)delta_ij dx^i dx^j, the exterior spatial Einstein tensor reads gravitational slip.",
            "formula": "G_ij^(1)=partial_i partial_j(Psi-Phi); K_L,ij=2 partial_i partial_j phi_ext",
            "consequence": "If G_ij^(1)=Sigma_H*K_L,ij, then Psi-Phi=2*Sigma_H*r^-3*P2.",
            "status": "SLIP_RESPONSE_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "readout_id": "HMR4487_2_metric_null_verdict",
            "object": "K_L -> public metric",
            "derived_statement": "Under same-frame identity metric readout, the Hessian carrier is not metric-null unless Sigma_H=0.",
            "formula": "delta g_public[K_L]=0 fails on identity readout; Sigma_H=0 or parent improvement/solder map required",
            "consequence": "The live route is zero-or-bound, not automatic local-GR closure.",
            "status": "METRIC_NULL_FAILS_ON_IDENTITY_READOUT",
            "valid_for_claim": False,
        },
        {
            "readout_id": "HMR4487_3_observable_amplitude",
            "object": "surface slip amplitude",
            "derived_statement": "The surface P2 slip coefficient is twice the canonical exterior slip amplitude.",
            "formula": "A_slip_surface=2*|Sigma_H|; slip_rms_surface=(2/sqrt(5))*|Sigma_H|",
            "consequence": "Local pressure rows can bound Sigma_H only after the slip-to-public-P2 transfer is accepted.",
            "status": "SLIP_BOUND_NORMAL_FORM_DERIVED",
            "valid_for_claim": False,
        },
    ]


def normalization_rows(c_k2_unit: float, chi_h: float) -> List[Dict[str, object]]:
    return [
        {
            "norm_id": "NORM4487_0_public_metric_unit",
            "object": "C_K2_unit",
            "formula": "A_metric=C_K2_unit*s_K2*M2_K2",
            "value": f"{c_k2_unit:.15e}",
            "derivation": "carried from 3165/3177/3185 public metric normalization",
            "status": "SOURCE_CARRIED_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM4487_1_projected_moment_map",
            "object": "P_H to projected metric amplitude",
            "formula": "P_H:=s_K2*kappa_STF*c_ext; M2_K2^proj=(4/25)*kappa_STF*c_ext; A_metric(P_H)=C_K2_unit*(4/25)*P_H",
            "value": f"{(4.0 * c_k2_unit / 25.0):.15e}",
            "derivation": "4486/3180 projected Hessian moment plus K2 metric unit",
            "status": "CONDITIONAL_PUBLIC_AMPLITUDE_MAP",
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM4487_2_chiH_natural",
            "object": "chi_H",
            "formula": "2*Sigma_H=A_metric(P_H), so Sigma_H=(2/25)*C_K2_unit*P_H and chi_H=2*C_K2_unit/25",
            "value": f"{chi_h:.15e}",
            "derivation": "3185 explains the apparent 1e-25 suppression as the public metric unit/projection factor",
            "status": "NATURAL_CHIH_ORDER_DERIVED_CONDITIONALLY",
            "valid_for_claim": False,
        },
        {
            "norm_id": "NORM4487_3_profile_estimator",
            "object": "P_H source profile estimator",
            "formula": "I4_D2=-4*c_ext/5; P_H=s_K2*kappa_STF*c_ext=-(5/4)*s_K2*kappa_STF*I4_D2",
            "value": "symbolic",
            "derivation": "3187 turns c_ext into a signed source-profile readout",
            "status": "SOURCE_PROFILE_ESTIMATOR_DERIVED_INPUTS_MISSING",
            "valid_for_claim": False,
        },
    ]


def adoption_fork_rows() -> List[Dict[str, object]]:
    return [
        {
            "fork_id": "HAF4487_0_same_frame_identity",
            "route": "adopt K_L as live same-frame metric source",
            "test": "Does K_L have public metric response?",
            "result": "yes, gravitational slip with Psi-Phi=2*Sigma_H*r^-3*P2",
            "status": "FINITE_BOUND_ROUTE_ACTIVE",
            "next_requirement": "source-own Sigma_H or P_H and verify slip transfer",
            "valid_for_claim": False,
        },
        {
            "fork_id": "HAF4487_1_parent_improvement_silence",
            "route": "make K_L improvement/boundary silent",
            "test": "Can parent action route K_L away from observed metric stress?",
            "result": "not signed in current evidence",
            "status": "ZERO_ROUTE_OPEN_NOT_PROVEN",
            "next_requirement": "closed improvement/boundary theorem",
            "valid_for_claim": False,
        },
        {
            "fork_id": "HAF4487_2_hidden_frame_solder",
            "route": "reject same-frame readout",
            "test": "Can K_L live in a hidden coframe not read by matter clocks/rods/light?",
            "result": "possible only with a real solder/coframe map",
            "status": "COFRAME_MAP_MISSING",
            "next_requirement": "solder map plus clock/light/orbital readout rules",
            "valid_for_claim": False,
        },
        {
            "fork_id": "HAF4487_3_parent_source_zero",
            "route": "Sigma_H=0 by source or coupling theorem",
            "test": "Can s_K2, kappa_STF, c_ext or I4_D2 be zeroed by parent symmetry?",
            "result": "open; c_ext=0 kills the projected branch, while coupling/source symmetry zero is not signed",
            "status": "SOURCE_ZERO_OPEN_NOT_PROVEN",
            "next_requirement": "parent source symmetry or coupling zero theorem",
            "valid_for_claim": False,
        },
    ]


def ph_bound_rows(legacy_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for legacy in legacy_rows:
        rows.append(
            {
                "bound_id": "PHB4487_" + legacy["bound_name"],
                "bound_name": legacy["bound_name"],
                "A_metric_bound_surface": legacy["A_metric_bound_surface"],
                "chi_H_natural": legacy["chi_H_natural"],
                "P_H_bound_from_slip": legacy["P_H_bound_from_slip"],
                "A_slip_if_P_H_equals_1": legacy["A_slip_if_P_H_equals_1"],
                "safety_margin_for_P_H_equals_1": legacy["safety_margin_for_P_H_equals_1"],
                "interpretation": legacy["interpretation"],
                "status": "BOUND_IMPORTED_AS_PRESSURE_NONCLAIM",
                "valid_for_claim": False,
            }
        )
    return rows


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4487_0_metric_null",
            "finding": "K_L is not metric-null under same-frame identity readout",
            "reason": "linearized G_ij reads the Hessian carrier as gravitational slip",
            "effect": "the Hessian branch must be zeroed by parent theorem or bounded as a slip/source product",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4487_1_chiH",
            "finding": "the apparent chi_H fine tuning is a normalization factor",
            "reason": "chi_H=2*C_K2_unit/25 follows from matching A_slip=2Sigma_H to the 3177/3180 public metric amplitude",
            "effect": "order-one P_H is far below current pressure, but P_H is not source-owned",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4487_2_profile_estimator",
            "finding": "P_H can be tied to a source profile moment",
            "reason": "I4_D2=-4c_ext/5 gives P_H=-(5/4)s_K2*kappa_STF*I4_D2",
            "effect": "next work should source-own I4_D2/N4_D2 and s_K2*kappa_STF, not hunt a mysterious metric coefficient",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4487_3_claim_status",
            "finding": "local-GR/J2/PPN claim remains blocked",
            "reason": "K_L adoption, Sigma_H/P_H source ownership, DeltaK_TF leakage and slip transfer are not all parent-signed",
            "effect": "private zero-or-bound branch only",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    readout_rows: List[Dict[str, object]],
    norm_rows: List[Dict[str, object]],
    fork_rows: List[Dict[str, object]],
    bound_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4487_0_sources",
            "gate": "all cited source paths and needles exist",
            "gate_pass": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "detail": "source hygiene only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4487_1_readout_derivation",
            "gate": "same-frame Hessian slip response is derived",
            "gate_pass": any(row.get("readout_id") == "HMR4487_1_identity_metric_readout" for row in readout_rows),
            "claim_allowed": False,
            "detail": "non-null response, not a local-GR pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4487_2_chiH_normalization",
            "gate": "natural chi_H normalization is carried",
            "gate_pass": any(row.get("norm_id") == "NORM4487_2_chiH_natural" for row in norm_rows),
            "claim_allowed": False,
            "detail": "conditional same-normalization map",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4487_3_metric_null_not_claimed",
            "gate": "metric-null route is not overclaimed",
            "gate_pass": any(row.get("fork_id") == "HAF4487_0_same_frame_identity" and "FINITE_BOUND" in str(row.get("status")) for row in fork_rows),
            "claim_allowed": False,
            "detail": "K_L is live under identity readout",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4487_4_pressure_rows_nonclaim",
            "gate": "P_H pressure rows exist but remain nonclaim",
            "gate_pass": len(bound_rows) >= 3 and all(str(row.get("valid_for_claim")).lower() == "false" for row in bound_rows),
            "claim_allowed": False,
            "detail": "source ownership and transfer still missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4487_5_no_generated_claim_rows",
            "gate": "all generated rows remain private nonclaim",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [sources, readout_rows, norm_rows, fork_rows, bound_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "no local-GR, J2, PPN, R10, clock, orbital or EM claim is promoted",
            "valid_for_claim": False,
        },
    ]
