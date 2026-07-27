from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1774"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1774_0_1773_handoff",
        "source_key": "1773_handoff",
        "source_path": ROOT / "1773-Y5-R2FR-topological-Hilbert-equality-or-R-eq-bound.md",
        "needles": ["NEXT1773_0_primary", "PCL1773_4_verdict", "REQ1773_4_M_H_ref"],
    },
    {
        "source_id": "SRC1774_1_1773_validation",
        "source_key": "1773_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1773_VALIDATION.csv",
        "needles": ["VAL1773_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1774_2_1773_period",
        "source_key": "1773_period_lock",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_PERIOD_CHARGE_LOCK_AUDIT.csv",
        "needles": ["PCL1773_0_linked_period", "PCL1773_1_charge_normalization", "PCL1773_4_verdict"],
    },
    {
        "source_id": "SRC1774_3_1773_bound_pack",
        "source_key": "1773_bound_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1773_R_EQ_BOUND_PACK.csv",
        "needles": ["REQ1773_1_Delta_period", "REQ1773_4_M_H_ref", "REQ1773_7_epsilon_eq_abs"],
    },
    {
        "source_id": "SRC1774_4_1519_coframe_tau",
        "source_key": "1519_coframe_tau_mhref",
        "source_path": ROOT / "1519-Y5-parent-observed-coframe-tau-source-frame-lock-or-MHref-first-row.md",
        "needles": ["OCF1519_4_tau_lock", "MHR1519_7_MHref", "REJ1519_1_orbital_GM"],
    },
    {
        "source_id": "SRC1774_5_1645_Htau",
        "source_key": "1645_Htau_integrability",
        "source_path": ROOT / "1645-Y5-R2FR-Htau-MHref-integrability-reference-lock-or-Mstar-source-row.md",
        "needles": ["H_tau exists on the branch iff d_field alpha_tau = 0", "M_* = M_H_ref = H_tau[S_outer] - H_ref"],
    },
    {
        "source_id": "SRC1774_6_1652_denominator",
        "source_key": "1652_MHref_first_row",
        "source_path": ROOT / "1652-Y5-R2FR-MHref-denominator-first-row-and-source-measure-flux-contract.md",
        "needles": ["CG1652_0_MHref", "DEC1652_0_MHref", "NO_ORBITAL_GM_IMPORT"],
    },
    {
        "source_id": "SRC1774_7_1733_current_owner",
        "source_key": "1733_theta_Qtau_owner",
        "source_path": ROOT / "1733-Y5-R2FR-parent-theta-Qtau-current-owner-or-Htau-first-row.md",
        "needles": ["COA1733_7_owner_verdict", "HFR1733_2_total_deltaH", "CG1733_3_MHref"],
    },
    {
        "source_id": "SRC1774_8_hwt_attempt",
        "source_key": "hilbert_worldtube_attempt",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_5_exact_and_reference_terms_zero"],
    },
    {
        "source_id": "SRC1774_9_parent_contract",
        "source_key": "hilbert_parent_contract",
        "source_path": RESIDUALS / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
        "needles": ["PAC537_1_single_observed_source_frame", "PAC537_5_Hilbert_topological_charge_equality"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_SOURCE_REGISTER.csv",
    "lock_theorem": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_PERIOD_CHARGE_LOCK_THEOREM.csv",
    "mhref_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_MHREF_DENOMINATOR_GATE.csv",
    "first_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_PERIOD_MHREF_FIRST_ROWS.csv",
    "runner": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_LOCK_REFUSAL_RUNNER.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_COUNTERMODEL_LEDGER.csv",
    "impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_GR_NEWTON_IMPACT_LEDGER.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1774_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1774_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1774 period-charge lock / M_H_ref first-row evidence",
            }
        )
    return rows


def lock_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1774_0_statement",
            "claim": "period-charge lock theorem",
            "mathematical_form": "If the same parent action fixes e_obs, tau, W_source, Q_tau^MTS, H_ref, Pi_M, and omega_M_top, and the exterior current is closed with no retained leakage, then integral_L Pi_M J_H = H_tau[S_L]-H_ref = integral_L J_M_top for every linked L.",
            "status": "CONDITIONAL_THEOREM_CONTRACT",
            "would_close": "Delta_period=0 and M_H_ref becomes the noncircular denominator for R_eq",
            "current_blocker": "Theta_total/Q_tau owner, H_tau integrability, tau projectability, and boundary/reference lock are not signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1774_1_current_descent",
            "claim": "Q_tau^MTS descends to the same current as Pi_M J_H",
            "mathematical_form": "delta H_tau = integral_S(delta Q_tau^MTS - i_tau Theta_total) and (4*pi*G_ref)^-1 integral_S Pi_M J_H = H_tau[S]-H_ref",
            "status": "OWNER_NOT_SIGNED",
            "would_close": "Hilbert source period equals Hamiltonian charge",
            "current_blocker": "1733 owner verdict remains unsigned for retained sectors",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1774_2_tau_frame",
            "claim": "one observed tau/coframe controls source, charge, clock, orbit, and boundary",
            "mathematical_form": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary and e_obs is fixed before readout",
            "status": "MISSING_TAU_COFRAME_LOCK",
            "would_close": "prevents frame/time retuning in M_H_ref and Delta_period",
            "current_blocker": "1519 retains coframe/tau lock as missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1774_3_integrability_reference",
            "claim": "H_tau is integrable and reference-fixed",
            "mathematical_form": "d_field alpha_tau=0 with alpha_tau=integral_S(delta Q_tau^MTS - i_tau Theta_total)-delta H_ref",
            "status": "MISSING_HTAU_INTEGRABILITY",
            "would_close": "M_H_ref=H_tau[S_outer]-H_ref becomes a real source charge",
            "current_blocker": "1645 retained curl components and reference terms are not zero/bounded",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1774_4_period_zero",
            "claim": "Delta_period is zero",
            "mathematical_form": "Delta_period[L] := integral_L(Pi_M J_H - J_M_top)=0 for every linked L",
            "status": "NOT_DERIVED_FOR_CURRENT_MTS",
            "would_close": "same cohomology class needed by 1773 equality",
            "current_blocker": "PD normalization, M_H_ref, current descent, and no-readout selector are missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "PCT1774_5_verdict",
            "claim": "current MTS has period-charge lock and legal M_H_ref",
            "mathematical_form": "PCT1774_1 through PCT1774_4 all pass in the same parent action",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "would_close": "R_eq can be normalized and Newton/local-GR gates can be re-audited",
            "current_blocker": "no legal denominator or linked-period equality yet",
            "valid_for_claim": False,
        },
    ]


def mhref_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MHG1774_0_definition",
            "object": "M_H_ref",
            "required_condition": "M_H_ref := H_tau[S_outer]-H_ref in the same observed coframe/tau/source frame",
            "current_status": "DEFINITION_ONLY",
            "blocker": "H_tau and H_ref are not parent-signed current objects",
            "shortcut_rejected": "M_H_ref=1; bare mass; orbital GM import",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MHG1774_1_positive_finite",
            "object": "positivity",
            "required_condition": "M_H_ref>0 with units and source path for every scored arena/system",
            "current_status": "MISSING_POSITIVE_SOURCE_ROW",
            "blocker": "no H_tau/H_ref row has positive numeric or theorem-zero support",
            "shortcut_rejected": "normalizing by a convention or a fitted scale",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MHG1774_2_integrability",
            "object": "Hamiltonian integrability",
            "required_condition": "d_field alpha_tau=0 or explicit absolute curl residual divided by M_H_ref",
            "current_status": "MISSING_CURL_COMPONENTS",
            "blocker": "retained-sector, projector, boundary, reference, tau, and surface curls remain open",
            "shortcut_rejected": "EH-only charge import",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MHG1774_3_same_source",
            "object": "source/Hilbert equality",
            "required_condition": "(4*pi*G_ref)^-1 integral_S Pi_M J_H = M_H_ref on linked surfaces",
            "current_status": "MISSING_HILBERT_TO_HTAU_MAP",
            "blocker": "Q_tau^MTS/Pi_M J_H equality is not parent-owned",
            "shortcut_rejected": "defining Q_M from measured orbital acceleration",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MHG1774_4_verdict",
            "object": "legal denominator",
            "required_condition": "definition, positivity, integrability, and same-source equality all pass",
            "current_status": "DENOMINATOR_NOT_ACCEPTED",
            "blocker": "M_H_ref remains first-row acquisition target",
            "shortcut_rejected": "all circular denominators remain refused",
            "valid_for_claim": False,
        },
    ]


def first_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FR1774_0_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "H_tau[S_outer]-H_ref in the same observed coframe/tau/source frame",
            "required_fields": "system_id;arena;e_obs_id;tau_id;S_outer;H_tau;H_ref;Q_tau_source;Theta_source;units;source_path;equation_ref;no_orbital_GM_import",
            "status": "MISSING_M_H_REF",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FR1774_1_Delta_period",
            "quantity": "Delta_period",
            "definition": "max_L abs(integral_L(Pi_M J_H - J_M_top))",
            "required_fields": "system_id;linked_cycle_id;PiM_JH_period;JM_top_period;W_source;omega_M_top_normalization;M_H_ref;units;source_path",
            "status": "MISSING_PERIOD_MISMATCH_BOUND",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FR1774_2_deltaH_curl",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "absolute Hamiltonian one-form curl obstruction divided by M_H_ref",
            "required_fields": "I_EH;I_X;I_projector;I_boundary;I_ref;I_tau;I_surface;M_H_ref;component_units;source_paths",
            "status": "MISSING_HTAU_CURL_COMPONENTS",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FR1774_3_PD_normalization",
            "quantity": "omega_M_top_period",
            "definition": "integral_L omega_M_top = 1 for canonical linked cycles of W_source",
            "required_fields": "W_source_certificate;linked_cycle_basis;omega_M_top_definition;period_values;source_path",
            "status": "MISSING_PD_NORMALIZATION_CERTIFICATE",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FR1774_4_B_zero_Delta_symp",
            "quantity": "B_zero_flux;Delta_symp;H_ref_shift",
            "definition": "boundary/reference/symplectic offset in the linked source charge",
            "required_fields": "surface_pair;boundary_rule;B_zero_flux;Delta_symp;H_ref_shift;M_H_ref;units;source_path",
            "status": "MISSING_BOUNDARY_REFERENCE_INPUT",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FR1774_5_epsilon_period_abs",
            "quantity": "epsilon_period_abs",
            "definition": "absolute no-cancellation envelope of period mismatch, denominator, curl, boundary, and PD normalization residuals",
            "required_fields": "component_abs_sum;M_H_ref;component_source_paths;units;no_cancellation_guard",
            "status": "MISSING_COMPONENT_INPUTS",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_rows(first_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": f"RUN1774_{idx}_{row['quantity']}",
            "input_row": row["row_id"],
            "runner_decision": "REFUSE_SCORING",
            "refusal_reasons": f"{row['status']};VALID_FOR_CLAIM_FALSE;NO_CIRCULAR_DENOMINATOR;NO_CANCELLATION_CREDIT",
            "accepted_for_scoring": False,
            "claim_allowed": False,
        }
        for idx, row in enumerate(first_rows)
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1774_0_orbital_GM_import",
            "countermodel": "M_H_ref is set equal to measured orbital GM/G_ref",
            "survives_current_constraints": True,
            "why_survives": "no parent Hamiltonian denominator row exists",
            "what_kills_it": "source-backed H_tau-H_ref row plus no-orbital-import certificate",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1774_1_split_tau",
            "countermodel": "source, charge, clock, orbit, and boundary use different tau choices",
            "survives_current_constraints": True,
            "why_survives": "tau projectability/common observed time flow is not parent signed",
            "what_kills_it": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary theorem",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1774_2_nonintegrable_charge",
            "countermodel": "surface charge one-form is not integrable",
            "survives_current_constraints": True,
            "why_survives": "d_field alpha_tau components remain uncomputed",
            "what_kills_it": "curl zero theorem or finite curl residual bound",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1774_3_same_denominator_wrong_period",
            "countermodel": "M_H_ref exists but topological period mismatch remains nonzero",
            "survives_current_constraints": True,
            "why_survives": "Delta_period row is unfilled",
            "what_kills_it": "linked-period equality theorem or bound",
        },
    ]


def impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1774_0_R_eq",
            "bridge_piece": "R_eq normalization",
            "impact": "R_eq cannot be claim-scaled until M_H_ref is source-backed and Delta_period is bounded",
            "current_status": "BLOCKED",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1774_1_Newton",
            "bridge_piece": "Newtonian source mass",
            "impact": "Poisson-source coefficient cannot be derived by importing measured orbital GM",
            "current_status": "BLOCKED_NO_ORBITAL_GM_IMPORT",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1774_2_GR",
            "bridge_piece": "GR reduction",
            "impact": "Einstein/EH charge pattern remains reference-only until MTS Theta/Q_tau descends",
            "current_status": "BLOCKED_BY_CURRENT_OWNER",
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "IMP1774_3_PPN",
            "bridge_piece": "PPN/local tests",
            "impact": "period/denominator residuals remain possible fifth-force/source-normalization terms",
            "current_status": "NONCLAIM_RESIDUALS_ACTIVE",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1774_0_theorem_route",
            "decision": "PERIOD_CHARGE_LOCK_IS_CLEAN_CONDITIONAL_ROUTE",
            "reason": "if one parent current owns tau, H_tau, Pi_M J_H and J_M_top, linked periods become the same source charge",
            "next_action": "do not promote until current owner and M_H_ref clauses are signed",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1774_1_current_status",
            "decision": "CURRENT_MTS_LOCK_NOT_SIGNED",
            "reason": "observed coframe/tau, Theta/Q_tau owner, H_tau integrability, reference lock, and period mismatch rows are missing",
            "next_action": "keep all first rows nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1774_2_guardrail",
            "decision": "ORBITAL_GM_AND_EH_ONLY_IMPORT_REJECTED",
            "reason": "those would use the target Newton/GR result as an input denominator",
            "next_action": "demand source-backed H_tau-H_ref or explicit residual bound",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1774_3_best_next",
            "decision": "QTAU_PERIOD_MAP_OR_DELTA_PERIOD_SOURCE_PACK_IS_NEXT",
            "reason": "the shortest route is the map from parent Q_tau/H_tau to the Pi_M period; fallback is a source pack for Delta_period and H_tau curl",
            "next_action": "build 1775 Q_tau-period map current descent or Delta_period source pack",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1774_0_period_lock",
            "claim": "Delta_period=0 for current MTS",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_QTAU_PERIOD_MAP_AND_PD_CERTIFICATE",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1774_1_MHref",
            "claim": "M_H_ref is a legal same-frame source denominator",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_HTAU_HREF_THETA_QTAU_INTEGRABILITY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1774_2_R_eq_score",
            "claim": "R_eq/period residual rows can be scored",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "MISSING_MHREF_AND_PERIOD_INPUTS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1774_3_Newton_local_GR",
            "claim": "Newton/local-GR reduction can reopen",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "DENOMINATOR_AND_PERIOD_COUNTERMODELS_RETAINED",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1774_0_primary",
            "next_target": "1775-Y5-R2FR-Qtau-period-map-current-descent-or-Delta-period-source-pack.md",
            "script": "scripts/Y5_R2FR_Qtau_period_map_current_descent_or_Delta_period_source_pack.py",
            "objective": "prove the parent map from Q_tau/H_tau to the Pi_M linked period, or stage source-ready Delta_period, H_tau curl, and M_H_ref rows",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1774_1_parallel",
            "next_target": "1775b-Y5-R2FR-Htau-first-row-component-source-pack.md",
            "script": "scripts/Y5_R2FR_Htau_first_row_component_source_pack.py",
            "objective": "split alpha_tau curl components into strict source rows with units, surface IDs, and no-cancellation guard",
            "selection_status": "parallel_fallback",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    first = first_row_rows()
    return {
        "source_register": source_register_rows(),
        "lock_theorem": lock_theorem_rows(),
        "mhref_gate": mhref_gate_rows(),
        "first_rows": first,
        "runner": runner_rows(first),
        "countermodel": countermodel_rows(),
        "impact": impact_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1774_{key.upper()}.csv")


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return all(boolish(row["exists"]) for row in rows), all(boolish(row["needles_present"]) for row in rows)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for flag in ("valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring"):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                if any(boolish(row.get(flag, False)) for flag in ("valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring")):
                    return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1774_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    return not any(FORMALIZATION.rglob("*1774*")) if FORMALIZATION.exists() else True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1774_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1774_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1774_2_theorem_contract",
            any(row["theorem_id"] == "PCT1774_0_statement" and row["status"] == "CONDITIONAL_THEOREM_CONTRACT" for row in rows_map["lock_theorem"]),
            "period-charge theorem contract is recorded",
        ),
        (
            "VAL1774_3_current_lock_not_promoted",
            any(row["theorem_id"] == "PCT1774_5_verdict" and row["status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["lock_theorem"]),
            "current period-charge lock remains unpromoted",
        ),
        (
            "VAL1774_4_MHref_denominator_blocked",
            any(row["gate_id"] == "MHG1774_4_verdict" and row["current_status"] == "DENOMINATOR_NOT_ACCEPTED" for row in rows_map["mhref_gate"]),
            "M_H_ref denominator gate is blocked",
        ),
        (
            "VAL1774_5_first_rows_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["first_rows"]),
            "period/M_H_ref first rows remain nonclaim",
        ),
        (
            "VAL1774_6_runner_refuses",
            all(row["runner_decision"] == "REFUSE_SCORING" and not boolish(row["claim_allowed"]) for row in rows_map["runner"]),
            "runner refuses current scoring lanes",
        ),
        (
            "VAL1774_7_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "denominator/period countermodels remain live",
        ),
        (
            "VAL1774_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1774_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1774_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1774_11_decision_next",
            any(row["decision_id"] == "DEC1774_3_best_next" and "QTAU_PERIOD_MAP" in row["decision"] for row in rows_map["decision"]),
            "decision selects Q_tau-period map next",
        ),
        (
            "VAL1774_12_next_selected",
            any(row["route_id"] == "NEXT1774_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1774_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1774 CSVs parse"),
        ("VAL1774_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1774_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1774_16_formalization_untouched", formalization_untouched(), "no 1774 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1774_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1774 period-charge lock or M_H_ref first-row checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1774 - Y5/R2FR Period-Charge Lock or M_H_ref First Row",
            "",
            "## Verdict",
            "",
            "The period-charge lock has a clean conditional shape, but it is not proved for current MTS. The missing object is not philosophical now: it is a same-frame Hamiltonian source denominator plus a linked-period equality map. `M_H_ref` cannot be orbital GM, bare mass, or a reference convention; it must be `H_tau[S_outer]-H_ref` from the same parent current used by the projected Hilbert source.",
            "",
            "**Claim ceiling:** no `Delta_period=0`, legal `M_H_ref`, `R_eq` score, Newton/GR reduction, R10/R11 pass, PPN pass, clock/orbital pass, or local-GR claim is allowed from 1774.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Period-Charge Lock Theorem",
            markdown_table(rows_map["lock_theorem"], ["theorem_id", "claim", "mathematical_form", "status", "would_close", "current_blocker", "valid_for_claim"]),
            "",
            "## M_H_ref Denominator Gate",
            markdown_table(rows_map["mhref_gate"], ["gate_id", "object", "required_condition", "current_status", "blocker", "shortcut_rejected", "valid_for_claim"]),
            "",
            "## First Rows",
            markdown_table(rows_map["first_rows"], ["row_id", "quantity", "definition", "required_fields", "status", "score_ready", "claim_allowed", "valid_for_claim"]),
            "",
            "## Refusal Runner",
            markdown_table(rows_map["runner"], ["run_id", "input_row", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## GR/Newton Impact Ledger",
            markdown_table(rows_map["impact"], ["impact_id", "bridge_piece", "impact", "current_status"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the no-magic-mass checkpoint. The theory is allowed to use topological charge only if the parent action proves it is the same Hamiltonian/Hilbert source charge. That is good news structurally: the exact missing bridge is now named. It is also why we still cannot reopen Newton/local-GR claims yet.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1774-Y5-R2FR-period-charge-lock-or-MHref-first-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1774 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
