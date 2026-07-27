from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_SOURCE_WORLDTUBE_CURRENT_COMPLEX_2586"
CHECKPOINT_ID = "2586"

DOC = ROOT / "2586-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SOURCE_COMPLEX_2586_SOURCE_REGISTER.csv",
    "owner_audit": OUT / "P8_Y5_SOURCE_COMPLEX_2586_OWNER_AUDIT.csv",
    "hilbert_current": OUT / "P8_Y5_SOURCE_COMPLEX_2586_HILBERT_CURRENT_CONTRACT.csv",
    "jdomain_rows": OUT / "P8_Y5_SOURCE_COMPLEX_2586_JDOMAIN_BOUND_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_SOURCE_COMPLEX_2586_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_SOURCE_COMPLEX_2586_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SOURCE_COMPLEX_2586_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SOURCE_COMPLEX_2586_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SOURCE_COMPLEX_2586_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2586_VALIDATION.csv",
}

COPY_TARGETS = {
    "owner_audit": QUEUE / "JR2586_SOURCE_WORLDTUBE_CURRENT_COMPLEX_OWNER_AUDIT_NONCLAIM.csv",
    "hilbert_current": QUEUE / "JR2586_HILBERT_CURRENT_CONTRACT_NONCLAIM.csv",
    "jdomain_rows": LOCAL_BOUNDS / "Source_worldtube_Jdomain_bound_rows_2586_NONCLAIM.csv",
    "next_target": QUEUE / "JR2586_MIN_PARENT_MATTER_COUPLING_ACTION_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2586_00_2585_handoff",
            "source_path": ROOT / "2585-Y5-R2FR-PiM-chainmap-commutator-zero-or-Icommutator-bound-fill.md",
            "needles": ["NEXT2585_0_selected", "ANT2585_3_physical_current", "VAL2585_OVERALL"],
            "role": "active handoff selecting source-worldtube/current-complex owner",
        },
        {
            "source_id": "SRC2586_01_2525_prior",
            "source_path": ROOT / "2525-Y5-R2FR-source-worldtube-fixed-domain-and-Hilbert-current-descent-or-Jdomain-bound.md",
            "needles": ["VAL2525_OVERALL", "NEXT2525_0_selected", "Jdomain"],
            "role": "prior fixed-domain/current descent checkpoint",
        },
        {
            "source_id": "SRC2586_02_2556_hilbert",
            "source_path": ROOT / "2556-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
            "needles": ["HIL2556_1_define_current", "GATE2556_3_worldtube", "VAL2556_OVERALL"],
            "role": "Hilbert/energy current selected as least-circular source bridge",
        },
        {
            "source_id": "SRC2586_03_2466_hilbert",
            "source_path": ROOT / "2466-Y5-R2FR-matter-current-descent-and-worldtube-source-bridge.md",
            "needles": ["HIL2466_1_define_current", "PV2466_4_overall", "VAL2466_OVERALL"],
            "role": "earlier Hilbert-current source bridge with clock/worldtube blockers",
        },
        {
            "source_id": "SRC2586_04_2503_selector",
            "source_path": LOCAL_BOUNDS / "Worldtube_Hilbert_selector_theorem_2503_NONCLAIM.csv",
            "needles": ["WHS2503_1_worldtube_selector", "WHS2503_4_R_eq_zero"],
            "role": "worldtube/Hilbert selector conditional theorem and same-object guard",
        },
        {
            "source_id": "SRC2586_05_2568_source_norm",
            "source_path": LOCAL_BOUNDS / "Hilbert_worldtube_source_normalization_2568_THEOREM_NONCLAIM.csv",
            "needles": ["THM2568_0_hilbert_current_contract", "THM2568_2_exact_divergence_identity"],
            "role": "Hilbert source-normalization divergence identity and stationary conditional branch",
        },
        {
            "source_id": "SRC2586_06_2524_jpim_rows",
            "source_path": ROOT / "source-intake" / "beta-source" / "docs" / "JPiM_bound_rows_2524_NONCLAIM.csv",
            "needles": ["JPIM2524_3_Ddomain", "MISSING_FIXED_DOMAIN_OR_OPERATOR_BOUND"],
            "role": "J_PiM bound rows showing domain-motion term remains unfilled",
        },
        {
            "source_id": "SRC2586_07_2585_validation",
            "source_path": OUT / "P8_Y5_BRR545_2585_VALIDATION.csv",
            "needles": ["VAL2585_OVERALL", "PASS"],
            "role": "previous checkpoint validation",
        },
    ]
    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                }
            )
        )
    return rows


def owner_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "SCO2586_0_parent_matter_action",
            "owner_clause": "parent action owns matter current before readout",
            "formal_statement": "S_matter[psi,e_obs,tau,ell_J] varies to T_H and defines J_H^mu=ell_J T_H^{mu nu} tau_nu before orbital/PPN fitting",
            "current_status": "CONDITIONAL_CONTRACT_NOT_PARENT_ACTION",
            "blocking_gap": "minimal parent matter-coupling action is not written/signed in the current corpus",
            "effect_if_missing": "the source current can be chosen after seeing Newton residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SCO2586_1_tau_lock",
            "owner_clause": "same time generator across source, charge, clocks and readout",
            "formal_statement": "tau_source=tau_charge=tau_clock=tau_readout and tau is normalized by parent/local boundary data",
            "current_status": "MISSING_TAU_LOCK",
            "blocking_gap": "clock-compatible conservation identity remains unsigned",
            "effect_if_missing": "current conservation leaks through T^{mu nu} nabla_mu tau_nu",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SCO2586_2_ellJ_lock",
            "owner_clause": "source-current scale ell_J fixed before readout",
            "formal_statement": "D ell_J=0 on the compact local branch or parent exchange terms exactly cancel scale gradients",
            "current_status": "MISSING_ELLJ_PARENT_SCALE",
            "blocking_gap": "ell_J is a contract, not yet a parent parameter with fixed value/units",
            "effect_if_missing": "source mass and q_loc/current amplitude can hide a fitted scale",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SCO2586_3_worldtube_support",
            "owner_clause": "source support/worldtube fixed before fitting",
            "formal_statement": "W_source := supp(J_H[e_obs,tau]) is parent-owned and regular; linked surfaces S_link enclose the same W_source",
            "current_status": "EXACT_SELECTOR_DEFINITION_CONDITIONAL",
            "blocking_gap": "support regularity, jump conditions and source-free annulus silence are not parent-signed",
            "effect_if_missing": "moving support creates domain terms and source-normalization leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SCO2586_4_exterior_complex",
            "owner_clause": "compact exterior current complex fixed",
            "formal_statement": "C_H(A_ext) is fixed with orientation, boundary conditions and no moving mask before Pi_M acts",
            "current_status": "MISSING_FIXED_DOMAIN_COMPLEX",
            "blocking_gap": "A_ext/S_link/domain-owner theorem is not signed",
            "effect_if_missing": "Stokes/chainmap arguments drop D_D Pi_M and boundary-crossing terms",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SCO2586_5_source_free_annulus",
            "owner_clause": "exterior annulus has no unaccounted source current",
            "formal_statement": "J_H=0 and dJ_H=0 in A_ext except accounted boundary/jump/exchange terms",
            "current_status": "CONDITIONAL_LOCAL_LIMIT_NOT_GLOBAL_THEOREM",
            "blocking_gap": "dynamic exchange, surface layers and extra-source channels are not zeroed or bounded",
            "effect_if_missing": "I_commutator can be evaluated on the wrong current complex",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SCO2586_6_same_object_guard",
            "owner_clause": "Hilbert source equals topological/charge object used by Pi_M",
            "formal_statement": "Pi_M J_H and J_M_top represent the same compact source class with zero B_zero flux",
            "current_status": "REQUIRED_NOT_PROVED",
            "blocking_gap": "R_eq and B_zero_flux remain retained residuals",
            "effect_if_missing": "fixed domain could still carry a closed wrong charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "SCO2586_7_verdict",
            "owner_clause": "source-worldtube/current complex owner theorem",
            "formal_statement": "W_source, A_ext, S_link, J_H[e_obs,tau], tau and ell_J are all parent-owned before readout and live in the Pi_M chain complex",
            "current_status": "SOURCE_WORLDTUBE_CURRENT_COMPLEX_NOT_DERIVED_CURRENT_CORPUS",
            "blocking_gap": "SCO2586_0 through SCO2586_6 remain unsigned",
            "effect_if_missing": "2585 chainmap theorem cannot be promoted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def hilbert_current_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "HCC2586_0_primary_current",
            "object": "Hilbert/energy source current",
            "formula": "J_M^mu = ell_J T_H^{mu nu} tau_nu",
            "status": "SELECTED_PRIMARY_CONTRACT",
            "reason": "least circular and most GR-compatible because the same stress-energy object sources the metric field equation",
            "missing_for_claim": "ell_J, tau, matter action descent and conservation identity",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HCC2586_1_divergence_identity",
            "object": "source-current conservation condition",
            "formula": "nabla_mu J_M^mu=(nabla_mu ell_J)T^{mu nu}tau_nu + ell_J(nabla_mu T^{mu nu})tau_nu + ell_J T^{mu nu}nabla_mu tau_nu",
            "status": "EXACT_IDENTITY_RETAINED",
            "reason": "localizes leakage into scale gradients, matter-shell failure and clock strain",
            "missing_for_claim": "parent exchange current or stationary/Killing collar proof",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HCC2586_2_worldtube_charge",
            "object": "source mass readout",
            "formula": "Q_M[Sigma]=int_{Sigma cap W_source}J_M^mu dSigma_mu; M_H=Q_M/ell_J",
            "status": "CONDITIONAL_CONTRACT",
            "reason": "source mass is defined before orbital fitting if W_source and ell_J are parent-owned",
            "missing_for_claim": "surface independence, jump/support conditions, no fitted GM",
            "valid_for_claim": False,
        },
        {
            "contract_id": "HCC2586_3_rejected_orbital_GM",
            "object": "fitted orbital GM current",
            "formula": "J_M chosen so integral equals observed GM",
            "status": "REJECTED_AS_DERIVATION",
            "reason": "would prove Newton by putting Newton into the source definition",
            "missing_for_claim": "not applicable; forbidden shortcut",
            "valid_for_claim": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def jdomain_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "JD2586_0_current_descent",
            "symbol": "E_current_descent",
            "definition": "norm of failure of J_H[e_obs,tau] to descend from parent matter action into the same source complex",
            "needed_for_claim": "J_H=q^*Jbar_H theorem or finite current-escape source row",
            "current_status": "MISSING_CURRENT_DESCENT_ZERO_OR_VALUE",
            "units": "dimensionless_or_current_norm",
            "observable_link": "I_commutator;source_normalization;PPN;R11",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "JD2586_1_domain_motion",
            "symbol": "E_domain_motion",
            "definition": "domain/worldtube/linking-surface motion contribution to source-current complex",
            "needed_for_claim": "fixed W_source/A_ext/S_link theorem or domain-motion coefficient",
            "current_status": "MISSING_FIXED_DOMAIN_OR_OPERATOR_BOUND",
            "units": "dimensionless_or_operator_norm_times_domain_variation",
            "observable_link": "I_commutator;radial_Meff_hair;R10;orbital",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "JD2586_2_tau_clock_leak",
            "symbol": "E_tau_clock",
            "definition": "ell_J T^{mu nu} nabla_mu tau_nu clock/source-current leakage",
            "needed_for_claim": "tau Killing/stationary collar or parent exchange-current cancellation",
            "current_status": "MISSING_CLOCK_COMPATIBILITY_ZERO_OR_BOUND",
            "units": "current_divergence_or_dimensionless_after_MHref",
            "observable_link": "clock;Gdot;PPN;local_GR",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "JD2586_3_ellJ_scale",
            "symbol": "E_ellJ_scale",
            "definition": "(nabla_mu ell_J)T^{mu nu}tau_nu source-scale leakage",
            "needed_for_claim": "D ell_J=0 parent scale theorem or source-backed drift bound",
            "current_status": "MISSING_ELLJ_SCALE_ZERO_OR_BOUND",
            "units": "current_divergence_or_dimensionless_scale_drift",
            "observable_link": "source_normalization;Gdot;orbital;PPN",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "JD2586_4_support_jump",
            "symbol": "E_support_jump",
            "definition": "surface-layer or boundary-crossing current at the edge of W_source",
            "needed_for_claim": "regular support/jump ledger with zero compact-boundary leak or finite source row",
            "current_status": "MISSING_JUMP_LEDGER_ZERO_OR_BOUND",
            "units": "GM_flux_or_dimensionless_after_MHref",
            "observable_link": "Newton;R10;R11;orbital",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "JD2586_5_extra_current_escape",
            "symbol": "E_extra_current_escape",
            "definition": "non-Hilbert/memory/domain/species/boundary current not included in J_H but seen by Pi_M or q_loc",
            "needed_for_claim": "extra-source annihilator theorem or component vector",
            "current_status": "MISSING_EXTRA_CURRENT_ZERO_OR_BOUND",
            "units": "dimensionless_or_GM_flux",
            "observable_link": "WEP;PPN;clock;R11;local_GR",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "JD2586_TOTAL",
            "symbol": "J_domain",
            "definition": "absolute no-cancellation source-worldtube/current-complex obstruction",
            "needed_for_claim": "all current/domain/tau/scale/support/extra terms theorem-zero or source-backed finite",
            "current_status": "TOTAL_SOURCE_COMPLEX_RETAINED_NONCLAIM",
            "units": "dimensionless_after_common_source_normalization",
            "observable_link": "PiM_chainmap;J_readout;Newton;PPN;R10;R11;local_GR",
            "numeric_value": "MISSING_COMPONENT_VALUES",
            "source_path": "THIS_CHECKPOINT_SYMBOLIC_LEDGER_ONLY",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def runner_refusal_rows(rows_in: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for row in rows_in:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"JDR2586_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_CLAIM_RETAINED_UNFILLED",
                    "failure_reasons": "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE;MISSING_SOURCE_PATH;VALID_FOR_CLAIM_FALSE",
                    "score_ready": False,
                    "claim_allowed": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2586_0_source_complex_owner",
            "claim": "source-worldtube/current complex is parent-owned",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "matter action, tau, ell_J, support, exterior domain and same-object guards remain unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2586_1_chainmap_antecedent",
            "claim": "2585 chainmap theorem antecedent J_H in C_H(A_ext) closes",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "physical current and fixed domain are not yet parent-signed",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2586_2_Jdomain_score",
            "claim": "J_domain rows are score-ready",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "no numeric/source-backed component values, units, denominators or source paths exist",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2586_3_Newton_local_GR",
            "claim": "Newton/local-GR source bridge is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "source current is a strong contract, not a parent action theorem",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2586_4_internal_progress",
            "claim": "least-circular source-current route is identified",
            "gate_status": "PASS_NONCLAIM",
            "reason": "Hilbert current remains the best GR-compatible route and orbital-GM current is rejected",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2586_0_hilbert_current_retained",
            "decision": "HILBERT_ENERGY_CURRENT_REMAINS_PRIMARY",
            "reason": "it is the least circular route to GR/Newton source structure and avoids species-charge tuning",
            "effect": "use J_M=ell_J T_H tau as the working source-current contract",
        },
        {
            "decision_id": "DEC2586_1_owner_not_proved",
            "decision": "SOURCE_WORLDTUBE_CURRENT_COMPLEX_NOT_PROVED",
            "reason": "parent matter action, tau/ell_J, support, fixed exterior domain, jump ledger and same-object equality are unsigned",
            "effect": "2585 PiM chainmap theorem remains conditional only",
        },
        {
            "decision_id": "DEC2586_2_bound_rows_staged",
            "decision": "JDOMAIN_ROWS_STAGED_NOT_SCORED",
            "reason": "domain/current escape rows are structurally named but lack source-backed values and denominators",
            "effect": "empirical use stays blocked until real rows exist",
        },
        {
            "decision_id": "DEC2586_3_next",
            "decision": "MINIMAL_PARENT_MATTER_COUPLING_ACTION_SELECTED_NEXT",
            "reason": "one parent action signature is the least handwavy way to sign current descent, tau/ell_J, no source-only slots and boundary/support silence together",
            "effect": "2587 should write/test the minimal parent matter-coupling action contract or demote to domain-motion inputs",
        },
    ]
    return [with_stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2586_0_selected",
            "selection_status": "selected",
            "target_file": "2587-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
            "target_script": "scripts/Y5_R2FR_minimal_parent_matter_coupling_action_or_domain_motion_input_2587.py",
            "task": "write/test the minimal parent matter-coupling action that would sign J_H=q^*Jbar_H, tau/ell_J ownership, no source-only slots, variation-before-readout, and boundary/support silence; otherwise keep domain-motion rows nonclaim",
            "acceptance_target": "parent action clauses jointly sign the Hilbert current/source-worldtube complex, or E_current_descent/E_domain_motion/E_tau/E_ellJ/E_support rows remain explicit nonclaim inputs",
            "guardrails": "no fitted GM source; no post-readout worldtube; no Noether-conservation-only proof; no source-only slot that bypasses matter action; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
        }
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2586_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                }
            )
        )

    add("VAL2586_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2586_01_owner_blocked",
        any(row["audit_id"] == "SCO2586_7_verdict" and row["valid_for_claim"] is False for row in data["owner_audit"]),
        "source-worldtube/current-complex owner theorem remains blocked",
    )
    add(
        "VAL2586_02_hilbert_selected",
        any(row["contract_id"] == "HCC2586_0_primary_current" and row["status"] == "SELECTED_PRIMARY_CONTRACT" for row in data["hilbert_current"]),
        "Hilbert current is retained as primary least-circular contract",
    )
    add(
        "VAL2586_03_orbital_gm_rejected",
        any(row["contract_id"] == "HCC2586_3_rejected_orbital_GM" for row in data["hilbert_current"]),
        "fitted orbital-GM current is rejected as derivation",
    )
    add(
        "VAL2586_04_jdomain_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["jdomain_rows"]),
        "J_domain/current leakage rows remain nonclaim",
    )
    add(
        "VAL2586_05_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses unfilled source-complex rows",
    )
    add(
        "VAL2586_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no source-complex, chainmap, Newton or local-GR claim is allowed",
    )
    add(
        "VAL2586_07_next_target_written",
        any(row["route_id"] == "NEXT2586_0_selected" for row in data["next"]),
        "2587 minimal parent matter-coupling action target selected",
    )
    add(
        "VAL2586_08_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2586-Y5-R2FR-source-worldtube-current*",
            "*Y5_R2FR_source_worldtube_current_complex*",
            "*P8_Y5_SOURCE_COMPLEX_2586*",
            "*JR2586*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2586_09_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2586 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2586_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2586_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2586_OVERALL",
        overall,
        "2586 retains Hilbert source current as primary contract, blocks source-worldtube/current-complex ownership, stages J_domain rows, and selects minimal parent matter-coupling action next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2586 Y5 R2FR source worldtube current complex owner or Jdomain bound fill",
        "",
        "**Status:** private nonclaim derivation checkpoint. The Hilbert/energy source current remains the best route, but the source-worldtube/current complex is not parent-owned yet.",
        "",
        "**Main result:** the right-looking local-GR source object is still `J_M^mu = ell_J T_H^{mu nu} tau_nu`, not a fitted orbital-GM current. But current MTS has not signed the parent matter action, tau/ell_J ownership, fixed `W_source/A_ext/S_link`, jump/support silence, extra-current silence, or same-object guard needed to put `J_H` inside the `Pi_M` chain complex. Therefore `J_domain` remains a retained nonclaim obstruction and 2585 cannot promote `[d,Pi_M]J_H=0`.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Owner Audit",
        markdown_table(data["owner_audit"], ["audit_id", "owner_clause", "formal_statement", "current_status", "blocking_gap", "effect_if_missing", "valid_for_claim", "claim_allowed"]),
        "",
        "## Hilbert Current Contract",
        markdown_table(data["hilbert_current"], ["contract_id", "object", "formula", "status", "reason", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Jdomain Bound Rows",
        markdown_table(data["jdomain_rows"], ["row_id", "symbol", "definition", "needed_for_claim", "current_status", "units", "observable_link", "numeric_value", "source_path", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "symbol", "verdict", "failure_reasons", "score_ready", "claim_allowed"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    jdomain_rows_data = jdomain_rows()
    data = {
        "sources": source_register_rows(),
        "owner_audit": owner_audit_rows(),
        "hilbert_current": hilbert_current_rows(),
        "jdomain_rows": jdomain_rows_data,
        "runner_refusal": runner_refusal_rows(jdomain_rows_data),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["owner_audit"], data["owner_audit"])
    write_csv(OUTPUTS["hilbert_current"], data["hilbert_current"])
    write_csv(OUTPUTS["jdomain_rows"], data["jdomain_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2586_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
