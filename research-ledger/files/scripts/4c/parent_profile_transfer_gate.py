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


def el_profile_rows() -> List[Dict[str, object]]:
    return [
        {
            "el_id": "EL4489_0_operator",
            "object": "projected Hessian profile operator",
            "formula": "D2[F]=(2/5)F''+2F'/x+6F/(5x^2)",
            "result": "profile source operator carried from 3179/3191",
            "status": "OPERATOR_CARRIED",
            "valid_for_claim": False,
        },
        {
            "el_id": "EL4489_1_quadratic_functional",
            "object": "toy parent profile functional",
            "formula": "J[F]=integral x^4(D2[F])^2 dx",
            "result": "candidate functional for parent selection; not parent-signed",
            "status": "CANDIDATE_FUNCTIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "el_id": "EL4489_2_normal_equation",
            "object": "Euler-Lagrange equation",
            "formula": "D2dagger[x^4D2[F]]=0; D2dagger[u]=(2/5)u''-(2u/x)'+6u/(5x^2)",
            "result": "interior profile equation solved at toy-functional level",
            "status": "EL_CONTRACT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "el_id": "EL4489_3_power_modes",
            "object": "normal-mode family",
            "formula": "D2dagger[x^4D2[x^p]]=(4/25)p(p-2)(p+1)(p+3)x^p",
            "result": "F_EL=A+B*x^2+C/x+D/x^3",
            "status": "INTERIOR_EL_SOLUTION_FAMILY_DERIVED",
            "valid_for_claim": False,
        },
    ]


def profile_selection_rows(sel3190: Dict[str, str], sel3192: List[Dict[str, str]], sel3193: List[Dict[str, str]], glue3194: List[Dict[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = [
        {
            "selection_id": "PSEL4489_0_smoothstep_minN4_candidate",
            "source_row": sel3190["selection_id"],
            "profile_type": "C2_smoothstep_ansatz",
            "transition_width": sel3190["selected_width"],
            "N4_D2": sel3190["selected_N4_D2"],
            "critical_abs_sK2_kappaSTF": sel3190["critical_abs_sK2_kappaSTF_for_tight_proxy"],
            "boundary_or_parent_status": "ANSATZ_CANDIDATE_NOT_PARENT_DERIVED",
            "claim_effect": "useful scan candidate only",
            "valid_for_claim": False,
        }
    ]
    for row in sel3192:
        rows.append(
            {
                "selection_id": "PSEL4489_" + row["selection_id"].replace("SEL3192_", ""),
                "source_row": row["selection_id"],
                "profile_type": "exact_interior_EL",
                "transition_width": row["transition_width"],
                "N4_D2": row["exact_EL_N4_D2"],
                "critical_abs_sK2_kappaSTF": row["critical_abs_sK2_kappaSTF_for_tight_proxy"],
                "boundary_or_parent_status": row["status"],
                "claim_effect": "interior profile improved; boundary/interface still gated",
                "valid_for_claim": False,
            }
        )
    glue_by_width = {row["transition_width"]: row for row in glue3194}
    for row in sel3193:
        glue = glue_by_width.get(row["transition_width"], {})
        rows.append(
            {
                "selection_id": "PSEL4489_" + row["selection_id"].replace("SEL3193_", ""),
                "source_row": row["selection_id"],
                "profile_type": "boundary_momentum_audit",
                "transition_width": row["transition_width"],
                "N4_D2": row["N4_D2"],
                "critical_abs_sK2_kappaSTF": "",
                "boundary_or_parent_status": row["status"],
                "lambda_norm_if_glued": glue.get("lambda_norm", ""),
                "claim_effect": "natural interface fails; gluing multipliers can close only if parent-owned",
                "valid_for_claim": False,
            }
        )
    return rows


def interface_gluing_rows() -> List[Dict[str, object]]:
    return [
        {
            "interface_id": "IF4489_0_natural_momenta",
            "object": "quadratic profile interface momenta",
            "formula": "Pi_1=(4/5)u; Pi_0=4u/x-(4/5)u'; u=x^4D2[F]",
            "result": "natural joins without interface action require [Pi_1]=0 and [Pi_0]=0",
            "status": "INTERFACE_CONDITIONS_DERIVED",
            "valid_for_claim": False,
        },
        {
            "interface_id": "IF4489_1_natural_no_go",
            "object": "pure natural interface route",
            "formula": "exterior join forces u_tr(b)=0 and u'_tr(b)=0 -> A=B=0 -> F_tr=C/x+D/x^3; exterior matching forces F_tr=x^-3",
            "result": "cannot also match core F=x^2 and F'=2x",
            "status": "PURE_NATURAL_INTERFACE_REJECTED",
            "valid_for_claim": False,
        },
        {
            "interface_id": "IF4489_2_gluing_multiplier_action",
            "object": "C1 constrained gluing",
            "formula": "S_glue=sum(lambda_0[F]+lambda_1[F']); variation gives [F]=[F']=0 and [Pi_i]+lambda_i=0",
            "result": "lambda_i=-[Pi_i] closes interface equations exactly if parent allows gluing multipliers",
            "status": "MECHANISM_CONSTRUCTED_PARENT_SIGNATURE_REQUIRED",
            "valid_for_claim": False,
        },
        {
            "interface_id": "IF4489_3_rejected_penalty",
            "object": "source-neutral quadratic C1 penalty",
            "formula": "S_bl=(1/2)k0[F]^2+(1/2)k1[F']^2+k01[F][F']",
            "result": "fails on C1 matched exact branch because penalty gradient vanishes where nonzero momentum is required",
            "status": "QUADRATIC_PENALTY_REJECTED",
            "valid_for_claim": False,
        },
    ]


def transfer_sensitivity_rows(crit3191: List[Dict[str, str]]) -> List[Dict[str, object]]:
    keep = {
        "1.000000000000000e+00",
        "1.000000000000000e+06",
        "1.000000000000000e+09",
        "1.000000000000000e+10",
        "1.000000000000000e+11",
    }
    rows: List[Dict[str, object]] = []
    for row in crit3191:
        if row["abs_sK2_kappaSTF"] not in keep:
            continue
        rows.append(
            {
                "transfer_id": "TS4489_" + row["critical_id"].replace("CRIT3191_", ""),
                "abs_sK2_kappaSTF": row["abs_sK2_kappaSTF"],
                "N4_D2": row["N4_D2"],
                "PH_envelope": row["PH_envelope"],
                "base_PH_bound": row["base_PH_bound"],
                "minimum_transfer_bound_factor_to_pass": row["minimum_transfer_bound_factor_to_pass"],
                "equivalent_max_tightening_factor": row["equivalent_max_tightening_factor"],
                "interpretation": row["interpretation"],
                "status": "TRANSFER_TIGHTENING_CRITICAL_NONCLAIM",
                "valid_for_claim": False,
            }
        )
    return rows


def parent_requirement_rows() -> List[Dict[str, object]]:
    return [
        {
            "requirement_id": "REQ4489_0_parent_profile_equation",
            "object": "profile equation",
            "needed": "derive J[F] or the actual parent profile functional from MTS, not just the toy quadratic stress",
            "current_status": "TOY_EL_SOLVED_PARENT_FUNCTIONAL_UNSIGNED",
            "claim_effect": "profile rows remain candidates",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ4489_1_boundary_layer_origin",
            "object": "C1 gluing multipliers",
            "needed": "derive constrained gluing domains, finite edge stress, or modified bulk functional from parent action",
            "current_status": "MECHANISM_CLOSES_EQUATIONS_PARENT_SIGNATURE_MISSING",
            "claim_effect": "interface closure remains nonclaim",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ4489_2_coupling_product",
            "object": "s_K2*kappa_STF",
            "needed": "source-owned sign and magnitude or exact coupling zero theorem",
            "current_status": "COUPLING_PRODUCT_MISSING",
            "claim_effect": "P_H cannot be claimed small or zero",
            "valid_for_claim": False,
        },
        {
            "requirement_id": "REQ4489_3_transfer_upgrade",
            "object": "slip-to-observable map",
            "needed": "PPN/orbital/light-time transfer for Psi-Phi=2Sigma_H r^-3P2 and DeltaK_TF leakage",
            "current_status": "PUBLIC_P2_PRESSURE_PROXY_ONLY",
            "claim_effect": "no PPN/orbital/local-GR claim",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4489_0_toy_EL_solved",
            "finding": "quadratic toy profile equation has an exact interior solution family",
            "reason": "normal equation modes are 1, x^2, x^-1 and x^-3",
            "effect": "profile selection moved beyond smoothstep ansatz",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4489_1_natural_interface_no_go",
            "finding": "pure natural interface matching fails",
            "reason": "exterior natural conditions collapse transition to x^-3 and prevent core matching",
            "effect": "boundary/interface mechanism is required",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4489_2_gluing_multiplier_route",
            "finding": "C1 gluing multipliers close interface equations exactly if parent-owned",
            "reason": "lambda_i=-[Pi_i] follows from stationarity of S_glue",
            "effect": "next theorem target is parent origin of gluing/edge stress",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4489_3_transfer_sensitivity",
            "finding": "selected profile survives substantial transfer tightening for moderate coupling products",
            "reason": "critical rows show order-one can tighten by 5.74e10 and 1e9 by about 57 before failing",
            "effect": "transfer upgrade likely not fatal unless coupling is huge or bound tightens enormously",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    el_rows: List[Dict[str, object]],
    selection_rows: List[Dict[str, object]],
    interface_rows: List[Dict[str, object]],
    transfer_rows: List[Dict[str, object]],
    req_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4489_0_sources",
            "gate": "all cited source paths and needles exist",
            "gate_pass": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "detail": "source hygiene only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4489_1_EL_solved",
            "gate": "toy interior EL profile solved",
            "gate_pass": any(row.get("el_id") == "EL4489_3_power_modes" for row in el_rows),
            "claim_allowed": False,
            "detail": "toy functional not parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4489_2_profile_selection_rows",
            "gate": "profile selection rows include smoothstep and exact EL branches",
            "gate_pass": len(selection_rows) >= 8,
            "claim_allowed": False,
            "detail": "selection candidates only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4489_3_interface_no_go_and_glue",
            "gate": "natural no-go and gluing multiplier mechanism are both written",
            "gate_pass": any(row.get("interface_id") == "IF4489_1_natural_no_go" for row in interface_rows)
            and any(row.get("interface_id") == "IF4489_2_gluing_multiplier_action" for row in interface_rows),
            "claim_allowed": False,
            "detail": "mechanism requires parent origin",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4489_4_transfer_rows",
            "gate": "transfer tightening critical rows exist",
            "gate_pass": len(transfer_rows) >= 5,
            "claim_allowed": False,
            "detail": "sensitivity only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4489_5_required_parent_inputs_explicit",
            "gate": "parent requirements remain explicit",
            "gate_pass": len(req_rows) >= 4,
            "claim_allowed": False,
            "detail": "no closure assumption smuggled in",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4489_6_no_generated_claim_rows",
            "gate": "all generated rows remain private nonclaim",
            "gate_pass": all(
                str(row.get("valid_for_claim")).lower() == "false"
                for group in [sources, el_rows, selection_rows, interface_rows, transfer_rows, req_rows]
                for row in group
            ),
            "claim_allowed": False,
            "detail": "no local-GR, J2, PPN, R10, clock, orbital or EM claim is promoted",
            "valid_for_claim": False,
        },
    ]
