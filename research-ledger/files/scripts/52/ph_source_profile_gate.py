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


def profile_gate_rows(ph_bound: float) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "PG4488_0_signed_estimator",
            "object": "P_H",
            "derived_law": "P_H=-(5/4)*s_K2*kappa_STF*I4_D2",
            "meaning": "signed source-profile estimator inherited from the Hessian branch",
            "current_status": "DERIVED_SYMBOLIC_SOURCE_PROFILE_GATE",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG4488_1_absolute_envelope",
            "object": "absolute profile norm",
            "derived_law": "|P_H| <= (5/4)*|s_K2*kappa_STF|*N4_D2",
            "meaning": "conservative bound using N4_D2=int |D2[F]| x^4 dx",
            "current_status": "EXECUTABLE_ENVELOPE_DERIVED",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG4488_2_tight_pressure_condition",
            "object": "tight half-range pressure gate",
            "derived_law": f"|s_K2*kappa_STF|*N4_D2 <= {(4.0 * ph_bound / 5.0):.15e}",
            "meaning": "sufficient condition for the smooth-profile branch under the current tight pressure proxy",
            "current_status": "PRESSURE_GATE_READY_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG4488_3_zero_routes",
            "object": "P_H zero branch",
            "derived_law": "P_H=0 if s_K2*kappa_STF=0 or I4_D2=0",
            "meaning": "zero routes remain parent-theorem tasks; profile cancellation cannot hide a fixed exterior c_ext",
            "current_status": "ZERO_ROUTES_IDENTIFIED_NOT_PROVEN",
            "valid_for_claim": False,
        },
    ]


def smooth_profile_rows(source_rows: List[Dict[str, str]], ph_bound: float) -> List[Dict[str, object]]:
    limit = 4.0 * ph_bound / 5.0
    rows: List[Dict[str, object]] = []
    for row in source_rows:
        n4 = float(row["N4_D2"])
        max_coupling = limit / n4 if n4 > 0 else float("inf")
        rows.append(
            {
                "profile_id": row["profile_id"].replace("SP3189", "SP4488"),
                "profile_family": row["profile_family"],
                "transition_width": row["transition_width"],
                "I4_D2": row["I4_D2"],
                "N4_D2": row["N4_D2"],
                "c_ext_est": row["c_ext_est"],
                "max_abs_sK2_kappaSTF_for_tight_pressure": f"{max_coupling:.15e}",
                "order_one_fraction_of_limit": f"{(n4 / limit):.15e}",
                "status": "LIVE_SMOOTH_PROFILE_ROW_NONCLAIM",
                "valid_for_claim": False,
            }
        )
    return rows


def margin_rows(source_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    selected_couplings = {"1.000000000000000e+00", "1.000000000000000e+09", "1.000000000000000e+12"}
    rows: List[Dict[str, object]] = []
    for row in source_rows:
        if row["abs_sK2_kappaSTF"] not in selected_couplings:
            continue
        rows.append(
            {
                "margin_id": row["margin_id"].replace("PM3189", "PM4488").replace("SP3189", "SP4488"),
                "profile_id": row["profile_id"].replace("SP3189", "SP4488"),
                "abs_sK2_kappaSTF": row["abs_sK2_kappaSTF"],
                "N4_D2": row["N4_D2"],
                "PH_envelope": row["PH_envelope"],
                "PH_bound": row["PH_bound"],
                "fraction_of_bound": row["fraction_of_bound"],
                "pressure_pass_if_sourced": row["pressure_pass_if_sourced"],
                "status": "SMOOTH_PROFILE_MARGIN_NONCLAIM",
                "valid_for_claim": False,
            }
        )
    return rows


def transfer_status_rows() -> List[Dict[str, object]]:
    return [
        {
            "transfer_id": "TR4488_0_current_proxy",
            "object": "public P2 pressure proxy",
            "status": "TRANSFER_PROXY_RETAINED_NONCLAIM",
            "needed_upgrade": "derive Shapiro/orbital/PPN covariance transfer for induced slip or source an accepted conservative public P2 comparator",
            "claim_effect": "pressure rows remain private robustness pressure, not a public local-GR/PPN pass",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "TR4488_1_profile_selection",
            "object": "smooth profile family",
            "status": "PROFILE_ROWS_READY_PARENT_SELECTION_MISSING",
            "needed_upgrade": "derive transition width/profile class from parent action or source model",
            "claim_effect": "smooth rows are live source-profile candidates but not parent-selected",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "TR4488_2_coupling_owner",
            "object": "s_K2*kappa_STF",
            "status": "COUPLING_PRODUCT_OWNER_MISSING",
            "needed_upgrade": "derive signed basis and parent variation coefficient or exact zero theorem",
            "claim_effect": "P_H cannot be claimed small or zero before coupling ownership",
            "valid_for_claim": False,
        },
        {
            "transfer_id": "TR4488_3_tensor_leakage",
            "object": "DeltaK_TF",
            "status": "LEAKAGE_TRANSFER_STILL_GATED",
            "needed_upgrade": "prove tensor leakage metric-null or include it in the same no-cancellation transfer vector",
            "claim_effect": "scalar smooth-profile safety does not alone close full local GR",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4488_0_profile_gate",
            "finding": "P_H source-profile gate is executable",
            "reason": "P_H=-(5/4)s_K2*kappa_STF I4_D2 and |P_H|<=(5/4)|s_K2*kappa_STF|N4_D2",
            "effect": "future local pressure checks can use profile/coupling products instead of vague source amplitude",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4488_1_smooth_profiles",
            "finding": "smooth finite-transition rows preserve c_ext=1 and have modest N4_D2",
            "reason": "C2 smoothstep rows give N4_D2 about 3.40 to 4.46 and I4_D2=-4/5",
            "effect": "order-one through 1e9 coupling products pass current tight pressure; 1e12 fails",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4488_2_transfer",
            "finding": "pressure proxy remains the public weak link",
            "reason": "the bound is still a solar public-P2 pressure proxy, not a full PPN/orbital/light-time transfer",
            "effect": "next work should either parent-select the profile/coupling or upgrade the transfer",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    gate_rows: List[Dict[str, object]],
    profile_rows: List[Dict[str, object]],
    margin_rows_list: List[Dict[str, object]],
    transfer_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4488_0_sources",
            "gate": "all cited source paths and needles exist",
            "gate_pass": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "detail": "source hygiene only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4488_1_profile_gate_written",
            "gate": "P_H profile gate exists",
            "gate_pass": any(row.get("gate_id") == "PG4488_2_tight_pressure_condition" for row in gate_rows),
            "claim_allowed": False,
            "detail": "executable gate, not source ownership",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4488_2_smooth_profiles_present",
            "gate": "smooth C2 profile rows exist",
            "gate_pass": len(profile_rows) >= 6,
            "claim_allowed": False,
            "detail": "candidate profile family only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4488_3_margin_rows_present",
            "gate": "order-one, 1e9, and 1e12 margin rows exist",
            "gate_pass": len(margin_rows_list) >= 18,
            "claim_allowed": False,
            "detail": "profile pressure smoke rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4488_4_transfer_not_overclaimed",
            "gate": "transfer proxy is explicitly retained as nonclaim",
            "gate_pass": any(row.get("transfer_id") == "TR4488_0_current_proxy" for row in transfer_rows),
            "claim_allowed": False,
            "detail": "no PPN/orbital covariance claim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4488_5_no_generated_claim_rows",
            "gate": "all generated rows remain private nonclaim",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [sources, gate_rows, profile_rows, margin_rows_list, transfer_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "no local-GR, J2, PPN, R10, clock, orbital or EM claim is promoted",
            "valid_for_claim": False,
        },
    ]
