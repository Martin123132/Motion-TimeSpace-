from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List, Mapping


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


def zero_theorem_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "zero_id": "Z4492_0_definition",
            "quantity": "DeltaK_TF",
            "attempted_zero_route": "DeltaK_TF^{ij}:=K_L^{<ij>}-P_Y[K_L]^{ij}; prove the public metric only sees P_Y[K_L]",
            "derivation_result": "P_Y[K_L] is owned, but the full Hessian carrier has non-Y_a tensor footprint unless parent projection/soldering is signed",
            "status": "OPEN_PARENT_PROJECTION_ROUTE_UNSIGNED",
            "effect": "would set A_DeltaKTF_surface=0 if the parent public metric readout equals P_Y[K_L]",
            "valid_for_claim": False,
        },
        {
            "zero_id": "Z4492_1_Bprime_condition",
            "quantity": "B_prime",
            "attempted_zero_route": "Use B(r):=(3/2)F(r)/r^2 and require B'(r)=0 across the tested collar",
            "derivation_result": "core F=A*r^2 gives B'=0, but exterior F=C*r^-3 gives B'=-(15/2)C*r^-6; a nonzero matched exterior cannot keep B'=0 globally",
            "status": "REJECTED_FOR_NONZERO_MATCHED_EXTERIOR",
            "effect": "DeltaKTF exact zero cannot be obtained from the current matched profile alone",
            "valid_for_claim": False,
        },
        {
            "zero_id": "Z4492_2_metric_null",
            "quantity": "delta_g_public[K_L]",
            "attempted_zero_route": "Treat the full Hessian carrier as metric-null or an improvement term",
            "derivation_result": "4487 identity-readout branch gives nonzero gravitational slip unless Sigma_H=0; improvement/solder map still not parent-signed",
            "status": "REJECTED_ON_IDENTITY_READOUT_OPEN_WITH_PARENT_SOLDER",
            "effect": "cannot claim public metric silence without a parent readout map",
            "valid_for_claim": False,
        },
        {
            "zero_id": "Z4492_3_boundary_silence",
            "quantity": "boundary_and_readout_terms",
            "attempted_zero_route": "Let boundary/readout terms cancel or absorb DeltaKTF",
            "derivation_result": "4491 no-cancellation rule forbids destructive cancellation as evidence; any surviving lane needs its own signed bound",
            "status": "CANCELLATION_ROUTE_REJECTED",
            "effect": "requires a direct bound or exact zero, not a balancing trick",
            "valid_for_claim": False,
        },
        {
            "zero_id": "Z4492_4_current_verdict",
            "quantity": "A_DeltaKTF_surface",
            "attempted_zero_route": "Combine B'=0, metric-null, parent projection, and boundary silence",
            "derivation_result": "exact zero is not proven for the current finite matched branch; only the parent projection/solder route remains open",
            "status": "EXACT_ZERO_NOT_PROVEN_FINITE_BOUND_REQUIRED",
            "effect": "move to explicit no-cancellation allowance requirement",
            "valid_for_claim": False,
        },
    ]


def selected_allowance_rows(allowance_rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    target_ids = {
        "DA4491_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+09",
        "DA4491_PSEL4489_0_smoothstep_minN4_candidate_1.000000000000000e+11",
        "DA4491_PSEL4489_1_min_N4_exact_EL_scan_1.000000000000000e+11",
        "DA4491_PSEL4489_1_balanced_Fpp_jump_1.000000000000000e+11",
    }
    selected = [row for row in allowance_rows if row.get("allowance_id") in target_ids]
    return sorted(selected, key=lambda row: row["allowance_id"])


def bprime_leakage_bound_rows(allowance_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in selected_allowance_rows(allowance_rows):
        coupling = float(row["abs_sK2_kappaSTF"])
        allowance = float(row["min_remaining_A_DeltaKTF_allowance"])
        required_product = allowance / coupling if coupling else 0.0
        status = "FINITE_BOUND_REQUIRED" if required_product > 0.0 else "NO_ALLOWANCE_EXACT_ZERO_OR_SMALLER_BETA_REQUIRED"
        rows.append(
            {
                "bprime_bound_id": f"BP4492_{row['allowance_id'].removeprefix('DA4491_')}",
                "profile_id": row["profile_id"],
                "abs_sK2_kappaSTF": row["abs_sK2_kappaSTF"],
                "hardest_arena": row["hardest_arena"],
                "remaining_A_DeltaKTF_allowance": row["min_remaining_A_DeltaKTF_allowance"],
                "bound_model": "A_DeltaKTF_surface <= C_DeltaKTF * |s_K2*kappa_STF| * N_Bprime",
                "required_CDeltaKTF_times_NBprime_max": f"{required_product:.15e}",
                "interpretation": "the entire public-metric leakage transfer C_DeltaKTF*N_Bprime must fit below this number under no-cancellation",
                "status": status,
                "valid_for_claim": False,
            }
        )
    return rows


def allowance_requirement_rows(bprime_rows: List[Mapping[str, object]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for row in bprime_rows:
        rows.append(
            {
                "requirement_id": str(row["bprime_bound_id"]).replace("BP4492_", "REQ4492_"),
                "profile_id": row["profile_id"],
                "coupling_cell": row["abs_sK2_kappaSTF"],
                "mathematical_requirement": "Either prove A_DeltaKTF_surface=0, or prove/source C_DeltaKTF*N_Bprime <= required_CDeltaKTF_times_NBprime_max",
                "required_CDeltaKTF_times_NBprime_max": row["required_CDeltaKTF_times_NBprime_max"],
                "source_needed": "parent public-metric projection coefficient C_DeltaKTF and actual profile leakage norm N_Bprime",
                "claim_effect_if_met": "this DeltaKTF lane would fit inside the 4491 no-cancellation allowance for the listed profile/coupling cell",
                "current_status": "UNMET_NUMERIC_PARENT_INPUTS",
                "valid_for_claim": False,
            }
        )
    return rows


def coupling_product_signature_rows() -> List[Dict[str, object]]:
    return [
        {
            "signature_id": "SIG4492_0_sK2_zero",
            "quantity": "s_K2",
            "signature_attempt": "parent variation sets Hessian source-to-metric response coefficient to zero",
            "current_result": "not found in current source chain",
            "status": "UNSIGNED",
            "next_derivation": "derive metric response coefficient from parent action/readout map",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4492_1_kappa_STF_zero",
            "quantity": "kappa_STF",
            "signature_attempt": "matter/source kernel has no tracefree Hessian projection in the public metric channel",
            "current_result": "not found; current projected Hessian branch explicitly keeps kappa_STF symbolic",
            "status": "UNSIGNED",
            "next_derivation": "derive kappa_STF from the matter coupling/source domain rather than fit it",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4492_2_c_ext_zero",
            "quantity": "c_ext",
            "signature_attempt": "set the exterior r^-3 amplitude to zero",
            "current_result": "trivializes the exterior local test branch and is not a useful local-GR recovery route",
            "status": "REJECTED_AS_TRIVIAL_BRANCH",
            "next_derivation": "keep nonzero exterior branch and bound its leakage",
            "valid_for_claim": False,
        },
        {
            "signature_id": "SIG4492_3_product_bound",
            "quantity": "|s_K2*kappa_STF|",
            "signature_attempt": "use the 4492 leakage inequality to limit the live product",
            "current_result": "|s_K2*kappa_STF| <= allowance/(C_DeltaKTF*N_Bprime) whenever C_DeltaKTF*N_Bprime is sourced",
            "status": "FORMULA_DERIVED_NUMERIC_COEFFICIENTS_MISSING",
            "next_derivation": "compute N_Bprime from actual profile families or prove C_DeltaKTF=0 by parent projection",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4492_0_zero_attempt",
            "finding": "DeltaKTF exact zero fails for the matched profile-only route",
            "reason": "B'=0 holds in the quadratic core but not in the nonzero r^-3 exterior; transition leakage is unavoidable unless the parent public metric projection kills it",
            "effect": "the old plateau/silence shortcut is not allowed",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4492_1_numeric_squeeze",
            "finding": "finite DeltaKTF leakage is now turned into a hard inequality",
            "reason": "A_DeltaKTF_surface <= C_DeltaKTF*|s_K2*kappa_STF|*N_Bprime and 4491 gives the remaining no-cancellation allowance",
            "effect": "the next stage has concrete target numbers rather than vibes",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4492_2_branch_selection",
            "finding": "best next fork is parent projection zero or actual Bprime norm computation",
            "reason": "without C_DeltaKTF or N_Bprime, the local branch cannot be promoted even though moderate coupling remains numerically viable",
            "effect": "4493 should compute/source the leakage norm or prove the public metric only sees P_Y[K_L]",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
    bprime_rows: List[Dict[str, object]],
    requirement_rows: List[Dict[str, object]],
    signature_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    one_e9 = [
        row
        for row in bprime_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    one_e11_fail = [
        row
        for row in bprime_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+11"
    ]
    return [
        {
            "gate_id": "CG4492_0_sources",
            "requirement": "all cited source paths exist and needles are found",
            "passed": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "reason": "private derivation/bound checkpoint only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4492_1_exact_zero_audited",
            "requirement": "DeltaKTF exact-zero theorem is attempted and verdict recorded",
            "passed": any(row.get("status") == "EXACT_ZERO_NOT_PROVEN_FINITE_BOUND_REQUIRED" for row in zero_rows),
            "claim_allowed": False,
            "reason": "matched branch does not prove zero",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4492_2_bprime_bound_rows",
            "requirement": "finite Bprime leakage bound rows exist",
            "passed": len(bprime_rows) >= 4,
            "claim_allowed": False,
            "reason": "bound rows are requirements until C_DeltaKTF and N_Bprime are sourced",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4492_3_moderate_cell_squeezed",
            "requirement": "smoothstep 1e9 DeltaKTF requirement is computed",
            "passed": bool(one_e9) and one_e9[0].get("required_CDeltaKTF_times_NBprime_max") == "1.376467175318575e-22",
            "claim_allowed": False,
            "reason": "gives a concrete target number, not a claim",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4492_4_huge_smoothstep_blocked",
            "requirement": "smoothstep 1e11 zero allowance remains blocked",
            "passed": bool(one_e11_fail) and one_e11_fail[0].get("required_CDeltaKTF_times_NBprime_max") == "0.000000000000000e+00",
            "claim_allowed": False,
            "reason": "no finite DeltaKTF bound rescues that cell under beta=1 no-cancellation",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4492_5_signature_rows",
            "requirement": "coupling-product signature routes are classified",
            "passed": len(signature_rows) >= 4 and any(row.get("status") == "FORMULA_DERIVED_NUMERIC_COEFFICIENTS_MISSING" for row in signature_rows),
            "claim_allowed": False,
            "reason": "product law is derived but parent coefficients remain unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4492_6_local_GR",
            "requirement": "local-GR/J2/PPN claim",
            "passed": False,
            "claim_allowed": False,
            "reason": "A_DeltaKTF zero/bound, parent projection, C_DeltaKTF, N_Bprime and arena transfers remain unclosed",
            "valid_for_claim": False,
        },
    ]
