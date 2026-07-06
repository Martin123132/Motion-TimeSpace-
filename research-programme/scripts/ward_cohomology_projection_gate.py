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


def theorem_attempt_rows() -> List[Dict[str, object]]:
    return [
        {
            "attempt_id": "WCP4495_0_Ward_identity",
            "route": "transition Ward/anomaly-inflow identity",
            "target_statement": "delta_g S_bulk[DeltaKTF] + delta_g S_boundary[DeltaKTF] = 0 while ordinary matter still has delta S_m/delta g != 0",
            "derivation_status": "NOT_DERIVED",
            "reason": "Current corpus repeatedly says no transition Ward/anomaly identity is present for this branch.",
            "effect_on_C_DeltaKTF": "no zero theorem",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "WCP4495_1_support_separated_cohomology",
            "route": "support-separated exact/no-flux local collar",
            "target_statement": "If supp(DeltaKTF/transition stress) is outside W_loc and side/interface pullbacks plus Hamiltonian boundary terms vanish or are routed, local transition response is zero through <=2PN.",
            "derivation_status": "CONDITIONAL_SPECIAL_CASE_DERIVED",
            "reason": "192/4176 establish J_tr^nu=0 in compact no-flux local collars; 4288 imports the finite-margin AJ zero in that restricted domain.",
            "effect_on_C_DeltaKTF": "C_DeltaKTF_effective=0 only for support-separated compact-collar branch",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "WCP4495_2_terminal_public_metric",
            "route": "terminal public metric/coframe alone",
            "target_statement": "terminal public metric exists, therefore all non-public representative couplings vanish",
            "derivation_status": "REJECTED",
            "reason": "4276 countermodels show terminality alone does not force action-domain descent or eliminate labels, source weights, field renames, or kernel motion.",
            "effect_on_C_DeltaKTF": "does not set C_DeltaKTF=0",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "WCP4495_3_matter_interface_action_domain",
            "route": "terminal public metric plus matter-interface descent",
            "target_statement": "S_matter=Sbar[Psi, Eval(e_pub(q(Phi))), theta(q)] and Dg_public[DeltaK_TF]=0 with no shadow labels or field-rename tails",
            "derivation_status": "BEST_THEOREM_TARGET_NOT_SIGNED",
            "reason": "4276 identifies this as the stronger surviving route, but it is not parent-signed in the current chain.",
            "effect_on_C_DeltaKTF": "could set zero if derived, but not current evidence",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "WCP4495_4_explicit_closure",
            "route": "finite C_DeltaKTF closure comparator",
            "target_statement": "Keep C_DeltaKTF visible and test it against 4493/4494 maxima instead of hiding it as a theorem.",
            "derivation_status": "IMPLEMENTED_AS_COMPARATOR",
            "reason": "4494 made this the only currently honest route for generic DeltaKTF.",
            "effect_on_C_DeltaKTF": "numeric pass/fail comparator, no derived zero",
            "valid_for_claim": False,
        },
    ]


def conditional_zero_rows() -> List[Dict[str, object]]:
    return [
        {
            "zero_id": "CZ4495_0_domain",
            "branch": "support_separated_compact_local_collar",
            "conditions": "supp(T_local) subset int(W_loc); supp(DeltaKTF/transition shell) outside W_loc or side/interface pullbacks vanish",
            "derived_result": "J_tr^nu=0 through <=2PN in W_loc",
            "sets_C_DeltaKTF_zero": True,
            "scope": "conditional private selector branch only",
            "not_scope": "generic transition shell or nonzero boundary/domain-wall response",
            "valid_for_claim": False,
        },
        {
            "zero_id": "CZ4495_1_boundary",
            "branch": "fixed_or_routed_boundary_Hamiltonian_charge",
            "conditions": "delta H_tau fixed, zero, or explicitly routed; no unrouted C_side/I_sector pullback",
            "derived_result": "boundary flux is not hidden bulk local metric response",
            "sets_C_DeltaKTF_zero": True,
            "scope": "local no-flux/collar calculation",
            "not_scope": "radiative or transition boundary treated as invisible without routing",
            "valid_for_claim": False,
        },
        {
            "zero_id": "CZ4495_2_AJ_import",
            "branch": "finite_margin_AJ_support_separated_window",
            "conditions": "4288 support-separated compact local collar; R_transport_to_local=R_Bgrad_to_local=0",
            "derived_result": "A_J,eff_private=0 in the finite-margin window",
            "sets_C_DeltaKTF_zero": True,
            "scope": "AJ/cGamma side-channel in compact collar",
            "not_scope": "DeltaKTF transition shell profile or public local-GR claim",
            "valid_for_claim": False,
        },
        {
            "zero_id": "CZ4495_3_generic_shell",
            "branch": "generic_transition_shell",
            "conditions": "transition support intersects local collar or finite boundary/domain-wall response survives",
            "derived_result": "no zero theorem; must use explicit C_DeltaKTF closure comparator or source real shell profiles",
            "sets_C_DeltaKTF_zero": False,
            "scope": "generic branch verdict",
            "not_scope": "not a theorem-zero branch",
            "valid_for_claim": False,
        },
    ]


def closure_trial_rows(closure_rows: List[Dict[str, str]]) -> List[Dict[str, object]]:
    trial_values = [
        ("exact_zero", 0.0),
        ("1e-26", 1.0e-26),
        ("1e-25", 1.0e-25),
        ("1e-24", 1.0e-24),
        ("1e-23", 1.0e-23),
        ("1e-22", 1.0e-22),
        ("1e-20", 1.0e-20),
        ("unit", 1.0),
    ]
    rows: List[Dict[str, object]] = []
    for closure in closure_rows:
        limit = float(closure["required_CDeltaKTF_max"])
        for label, trial in trial_values:
            passes = trial <= limit
            if limit == 0.0 and trial > 0.0:
                verdict = "FAIL_EXACT_ZERO_REQUIRED"
            elif passes:
                verdict = "PASS_CLOSURE_COMPARATOR"
            else:
                verdict = "FAIL_CDELTAKTF_TOO_LARGE"
            rows.append(
                {
                    "trial_id": f"CT4495_{closure['profile_id']}_{closure['abs_sK2_kappaSTF']}_{label}",
                    "profile_id": closure["profile_id"],
                    "abs_sK2_kappaSTF": closure["abs_sK2_kappaSTF"],
                    "required_CDeltaKTF_max": closure["required_CDeltaKTF_max"],
                    "trial_CDeltaKTF_label": label,
                    "trial_CDeltaKTF": f"{trial:.15e}",
                    "passes_closure_limit": passes,
                    "verdict": verdict,
                    "valid_for_claim": False,
                }
            )
    return rows


def comparator_summary_rows(trial_rows: List[Dict[str, object]]) -> List[Dict[str, object]]:
    groups: Dict[str, List[Dict[str, object]]] = {}
    for row in trial_rows:
        key = f"{row['profile_id']}|{row['abs_sK2_kappaSTF']}"
        groups.setdefault(key, []).append(row)
    rows: List[Dict[str, object]] = []
    for key, group in groups.items():
        profile_id, coupling = key.split("|", 1)
        passing = [row for row in group if str(row["passes_closure_limit"]).lower() == "true"]
        largest = max((float(row["trial_CDeltaKTF"]) for row in passing), default=float("nan"))
        rows.append(
            {
                "summary_id": f"CTS4495_{profile_id}_{coupling}",
                "profile_id": profile_id,
                "abs_sK2_kappaSTF": coupling,
                "required_CDeltaKTF_max": group[0]["required_CDeltaKTF_max"],
                "passing_trial_count": len(passing),
                "largest_passing_trial_CDeltaKTF": f"{largest:.15e}" if passing else "",
                "unit_CDeltaKTF_passes": any(row["trial_CDeltaKTF_label"] == "unit" and str(row["passes_closure_limit"]).lower() == "true" for row in group),
                "exact_zero_required": float(group[0]["required_CDeltaKTF_max"]) == 0.0,
                "status": "COMPARATOR_READY_NONCLAIM",
                "valid_for_claim": False,
            }
        )
    return rows


def decision_ledger_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4495_0_conditional_zero",
            "finding": "support-separated compact collars retain a real conditional zero theorem",
            "reason": "192/4176 no-flux clauses plus 4288 finite-margin import close local transition/AJ leakage in that restricted domain",
            "effect": "this branch can be used as a private selector, not as generic shell local-GR proof",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4495_1_generic_shell_not_zero",
            "finding": "generic DeltaKTF transition shell remains nonzero/closure-only",
            "reason": "Ward identity and terminal public projection are not parent-signed, and terminality alone has countermodels",
            "effect": "generic branch must use explicit C_DeltaKTF comparator or real shell profiles",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4495_2_comparator_ready",
            "finding": "C_DeltaKTF closure comparator is executable",
            "reason": "4494 maxima are converted to pass/fail rows for trial closure coefficients",
            "effect": "future empirical/local tests can include this lane transparently without smuggling a zero",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    sources: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
    trial_rows: List[Dict[str, object]],
    summary_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    smooth_1e9_summary = [
        row
        for row in summary_rows
        if row.get("profile_id") == "PSEL4489_0_smoothstep_minN4_candidate"
        and row.get("abs_sK2_kappaSTF") == "1.000000000000000e+09"
    ]
    return [
        {
            "gate_id": "CG4495_0_sources",
            "requirement": "all cited source paths exist and needles are found",
            "passed": all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in sources),
            "claim_allowed": False,
            "reason": "source-backed private theorem/comparator checkpoint",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4495_1_conditional_zero_scope",
            "requirement": "conditional no-flux zero exists but is scoped",
            "passed": any(row.get("sets_C_DeltaKTF_zero") is True for row in zero_rows)
            and any(row.get("sets_C_DeltaKTF_zero") is False for row in zero_rows),
            "claim_allowed": False,
            "reason": "closed only in support-separated compact collars",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4495_2_generic_theorem_not_derived",
            "requirement": "generic Ward/public-projection theorem is not claimed",
            "passed": any(row.get("derivation_status") == "NOT_DERIVED" for row in theorem_rows)
            and any(row.get("derivation_status") == "REJECTED" for row in theorem_rows),
            "claim_allowed": False,
            "reason": "terminality and Ward shortcuts are blocked",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4495_3_comparator_rows",
            "requirement": "closure comparator rows exist for every closure contract and trial value",
            "passed": len(trial_rows) >= 32 and len(summary_rows) >= 4,
            "claim_allowed": False,
            "reason": "closure coefficients are explicit",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4495_4_smoothstep_1e9_scale",
            "requirement": "smoothstep 1e9 allows tiny trials but rejects unit C_DeltaKTF",
            "passed": bool(smooth_1e9_summary)
            and str(smooth_1e9_summary[0].get("unit_CDeltaKTF_passes")).lower() == "false"
            and float(smooth_1e9_summary[0].get("largest_passing_trial_CDeltaKTF", "0")) >= 1.0e-23,
            "claim_allowed": False,
            "reason": "scale discipline preserved",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4495_5_local_GR",
            "requirement": "local-GR/J2/PPN claim",
            "passed": False,
            "claim_allowed": False,
            "reason": "generic DeltaKTF remains explicit closure or needs real shell/profile theorem",
            "valid_for_claim": False,
        },
    ]
