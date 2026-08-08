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

BRANCH_ID = "MTS_R2FR_PIM_CHAINMAP_COMMUTATOR_2585"
CHECKPOINT_ID = "2585"

DOC = ROOT / "2585-Y5-R2FR-PiM-chainmap-commutator-zero-or-Icommutator-bound-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PIM_CHAINMAP_2585_SOURCE_REGISTER.csv",
    "chainmap_audit": OUT / "P8_Y5_PIM_CHAINMAP_2585_THEOREM_AUDIT.csv",
    "antecedent_gate": OUT / "P8_Y5_PIM_CHAINMAP_2585_ANTECEDENT_GATE.csv",
    "icommutator_rows": OUT / "P8_Y5_PIM_CHAINMAP_2585_ICOMMUTATOR_BOUND_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_PIM_CHAINMAP_2585_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_PIM_CHAINMAP_2585_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_PIM_CHAINMAP_2585_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PIM_CHAINMAP_2585_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PIM_CHAINMAP_2585_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2585_VALIDATION.csv",
}

COPY_TARGETS = {
    "chainmap_audit": QUEUE / "JR2585_PIM_CHAINMAP_THEOREM_AUDIT_NONCLAIM.csv",
    "icommutator_rows": LOCAL_BOUNDS / "PiM_Icommutator_bound_rows_2585_NONCLAIM.csv",
    "antecedent_gate": QUEUE / "JR2585_PIM_CHAINMAP_ANTECEDENT_GATE_NONCLAIM.csv",
    "next_target": QUEUE / "JR2585_SOURCE_WORLDTUBE_CURRENT_COMPLEX_NEXT.csv",
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
            "source_id": "SRC2585_00_2584_handoff",
            "source_path": ROOT / "2584-Y5-R2FR-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            "needles": ["NEXT2584_0_selected", "OBS2584_1_PiM_chainmap_commutator", "VAL2584_OVERALL"],
            "role": "active handoff selecting PiM chainmap commutator zero or I_commutator bound fill",
        },
        {
            "source_id": "SRC2585_01_2524_projector",
            "source_path": ROOT / "2524-Y5-R2FR-PiM-projector-commutator-zero-or-JPiM-bound.md",
            "needles": ["PIM2524_2_fixed_chainmap_lemma", "JPIM2524_1_Icommutator", "VAL2524_OVERALL"],
            "role": "latest R2FR J_PiM commutator split and fixed-chainmap conditional theorem",
        },
        {
            "source_id": "SRC2585_02_2407_chainmap",
            "source_path": ROOT / "2407-Y5-R2FR-projector-PiM-commutator-variation-zero-or-operator-coefficient-bound.md",
            "needles": ["PZ2407_1_fixed_chainmap_lemma", "PCB2407_0_I_commutator", "VAL2407_OVERALL"],
            "role": "prior proof that fixed parent chain-map makes the commutator algebra conditionally clean",
        },
        {
            "source_id": "SRC2585_03_2181_worldtube",
            "source_path": ROOT / "2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md",
            "needles": ["PCA2181_1_fixed_topological_route", "EFR2181_1_I_commutator", "VAL2181_OVERALL"],
            "role": "worldtube/source-glue warning: closed topological current must equal observed Hilbert source",
        },
        {
            "source_id": "SRC2585_04_2524_copy",
            "source_path": LOCAL_BOUNDS / "PiM_projector_commutator_zero_audit_2524_NONCLAIM.csv",
            "needles": ["PIM2524_2_fixed_chainmap_lemma", "EXACT_CONDITIONAL_THEOREM"],
            "role": "branch-locked 2524 nonclaim chainmap audit",
        },
        {
            "source_id": "SRC2585_05_1518_chainmap_contract",
            "source_path": OUT / "P8_Y5_PARENT_PIM_1518_FIXED_CHAINMAP_CONTRACT.csv",
            "needles": ["FCM1518_3_chainmap", "CONDITIONAL_LEMMA_ONLY"],
            "role": "parent fixed-chainmap contract requirements",
        },
        {
            "source_id": "SRC2585_06_1518_commutator",
            "source_path": OUT / "P8_Y5_PARENT_PIM_1518_COMMUTATOR_ZERO_AUDIT.csv",
            "needles": ["COM1518_1_conditional_chainmap", "VALID_CONDITIONAL_MATH_ONLY"],
            "role": "prior commutator-zero audit: algebra is conditional only",
        },
        {
            "source_id": "SRC2585_07_2584_validation",
            "source_path": OUT / "P8_Y5_BRR545_2584_VALIDATION.csv",
            "needles": ["VAL2584_OVERALL", "PASS"],
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


def chainmap_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "CMA2585_0_product_rule",
            "claim_piece": "projected-current product rule",
            "formal_statement": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
            "result": "EXACT_OBSTRUCTION_IDENTITY",
            "blocking_gap": "none algebraically; the gap is the zero theorem for the second term",
            "effect": "prevents deleting the commutator by notation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA2585_1_fixed_chainmap_theorem",
            "claim_piece": "fixed parent chain-map zero",
            "formal_statement": "If Pi_M:C_H(A_ext)->C_M(A_ext) is parent-selected before readout, d Pi_M=Pi_M d on C_H(A_ext), delta_m Pi_M=0, and J_H in C_H(A_ext), then [d,Pi_M]J_H=0.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "blocking_gap": "current corpus does not parent-sign Pi_M, J_H and A_ext as one fixed source complex",
            "effect": "the algebraic route is clean but has no current claim credit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA2585_2_parent_selector",
            "claim_piece": "mass/source selector before readout",
            "formal_statement": "the parent action supplies chi_M or equivalent mass-channel selector independent of orbital GM, PPN score, or fitted source normalization",
            "result": "NOT_PARENT_SIGNED",
            "blocking_gap": "no explicit parent selector term/current map found in current MTS source trail",
            "effect": "Pi_M could otherwise be a post-readout mask",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA2585_3_fixed_domain_worldtube",
            "claim_piece": "fixed compact exterior domain",
            "formal_statement": "W_source, A_ext, S_link and orientation are fixed before readout and do not vary with metric/source fitting",
            "result": "NOT_PARENT_SIGNED",
            "blocking_gap": "worldtube/domain/current descent remains open",
            "effect": "domain motion produces D_D Pi_M and I_commutator leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA2585_4_physical_current_complex",
            "claim_piece": "observed Hilbert current is in the chain complex",
            "formal_statement": "J_H[e_obs,tau] is the same physical matter/source current used by clocks, rods, orbital readout and v-source equations, with all extra channels zeroed or included",
            "result": "NOT_PARENT_SIGNED",
            "blocking_gap": "same-frame Hilbert-current descent and extra-source silence are incomplete",
            "effect": "the chain-map may act on a surrogate current rather than measured mass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA2585_5_metric_domain_independence",
            "claim_piece": "no projector variation stress",
            "formal_statement": "delta_g Pi_M=delta_domain Pi_M=0, or every derivative of Pi_M has a source-backed operator bound",
            "result": "NOT_PARENT_SIGNED",
            "blocking_gap": "topological no-stress route is conditional; Hodge/Green/domain routes retain stress",
            "effect": "projector stress remains a PPN/local-GR residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA2585_6_same_object_warning",
            "claim_piece": "closed current is the observed source current",
            "formal_statement": "Pi_M J_H = J_M_top + dB_zero with zero compact boundary flux and the same M_H_ref denominator",
            "result": "REQUIRED_FOR_NEWTON_USE_NOT_PROVED",
            "blocking_gap": "R_eq, B_zero_flux and M_H_ref remain retained nonclaim rows",
            "effect": "a closed wrong charge cannot prove measured-GM or Newton reduction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "CMA2585_7_verdict",
            "claim_piece": "current MTS proves [d,Pi_M]J_H=0",
            "formal_statement": "all chainmap antecedents are parent-signed on the physical compact exterior source complex",
            "result": "PIM_CHAINMAP_COMMUTATOR_ZERO_NOT_DERIVED_CURRENT_CORPUS",
            "blocking_gap": "parent selector, fixed domain/worldtube, physical current complex, no projector stress, R_eq/B_zero/MHref locks",
            "effect": "OBS2584_1 remains an explicit measured-GM obstruction component",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def antecedent_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "ANT2585_0_parent_selector",
            "antecedent": "Pi_M selected by parent action before readout",
            "required_evidence": "explicit chi_M/ell_M/current-map clause or parent Noether charge map in the MTS action",
            "current_status": "MISSING_PARENT_SELECTOR",
            "blocks": "post-readout mask rejection",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ANT2585_1_fixed_chainmap",
            "antecedent": "d Pi_M = Pi_M d on physical Hilbert-current complex",
            "required_evidence": "chain complex C_H(A_ext), target mass complex, and proof Pi_M is a chain map",
            "current_status": "CONDITIONAL_MATH_NOT_PARENT_SIGNED",
            "blocks": "I_commutator zero",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ANT2585_2_domain_worldtube",
            "antecedent": "W_source/A_ext/S_link fixed before fitting",
            "required_evidence": "source-worldtube support theorem and fixed exterior linking class",
            "current_status": "MISSING_DOMAIN_LOCK",
            "blocks": "D_D Pi_M and domain-motion leakage",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ANT2585_3_physical_current",
            "antecedent": "J_H is the observed Hilbert/source current in the same frame",
            "required_evidence": "matter-current descent and tau/e_obs lock across source, clocks and orbital readout",
            "current_status": "MISSING_CURRENT_DESCENT",
            "blocks": "surrogate-current loophole",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ANT2585_4_extra_channels",
            "antecedent": "extra source channels are included or annihilated",
            "required_evidence": "Pi_M dJ_extra=0 theorem or source-backed extra-current vector",
            "current_status": "MISSING_EXTRA_PROJECTION_ZERO",
            "blocks": "Omega_GM extra-current term",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ANT2585_5_no_projector_stress",
            "antecedent": "delta Pi_M carries no local stress or bounded stress",
            "required_evidence": "topological metric-independent projector proof or operator coefficient bounds",
            "current_status": "MISSING_PROJECTOR_STRESS_ZERO_OR_BOUND",
            "blocks": "PPN/local-GR source-normalization residual",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "ANT2585_6_same_denominator",
            "antecedent": "M_H_ref/tau/source denominator is parent-owned",
            "required_evidence": "same positive denominator for I_commutator, R_eq, clocks and orbital readout",
            "current_status": "MISSING_MHREF_TAU_LOCK",
            "blocks": "score-ready dimensionless rows",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def icommutator_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "IC2585_0_I_commutator_abs",
            "symbol": "I_commutator_abs",
            "definition": "M_H_ref^-1 abs(int_A [d,Pi_M]J_H)",
            "needed_for_claim": "zero theorem or finite source-backed value with A_ext, orientation and M_H_ref",
            "current_status": "MISSING_CHAINMAP_ZERO_OR_SOURCE_ROW",
            "units": "dimensionless_after_MHref_normalization_or_GM_flux_before_normalization",
            "observable_link": "Newton;PPN;R10;R11;orbital",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "IC2585_1_DmPiM_JH",
            "symbol": "(delta_m Pi_M)J_H",
            "definition": "memory/metric/source variation of Pi_M acting on the Hilbert current",
            "needed_for_claim": "delta_m Pi_M=0 or operator norm bound times source variation amplitude",
            "current_status": "MISSING_PROJECTOR_VARIATION_ZERO_OR_BOUND",
            "units": "dimensionless_or_operator_norm",
            "observable_link": "PPN;R11;local_GR",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "IC2585_2_Ddomain_PiM",
            "symbol": "D_D Pi_M",
            "definition": "domain/worldtube/linking-surface derivative contribution to Pi_M",
            "needed_for_claim": "fixed domain theorem or finite domain-motion coefficient",
            "current_status": "MISSING_DOMAIN_LOCK_OR_OPERATOR_BOUND",
            "units": "operator_norm_or_dimensionless_flux",
            "observable_link": "radial_Meff_hair;R10;orbital",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "IC2585_3_projector_stress_beta_equiv",
            "symbol": "projector_stress_beta_equiv",
            "definition": "weak-field/PPN equivalent of stress generated by projector variation",
            "needed_for_claim": "topological no-stress proof or PPN operator coefficient",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP_OR_VALUE",
            "units": "PPN_or_operator_units",
            "observable_link": "PPN_beta;PPN_gamma;preferred_frame;local_GR",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "IC2585_4_R_eq_guard",
            "symbol": "R_eq_integral",
            "definition": "guard row preventing a closed wrong current from being counted as measured source mass",
            "needed_for_claim": "Pi_M J_H=J_M_top+dB_zero with zero compact boundary flux",
            "current_status": "MISSING_TOPOLOGICAL_HILBERT_EQUALITY_OR_VALUE",
            "units": "dimensionless_after_MHref_normalization",
            "observable_link": "Newton;source_normalization;R11",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "row_id": "IC2585_TOTAL",
            "symbol": "J_PiM_comm",
            "definition": "absolute no-cancellation Pi_M commutator/projector contribution",
            "needed_for_claim": "all components theorem-zero or source-backed finite with common denominator",
            "current_status": "TOTAL_PIM_COMMUTATOR_RETAINED_NONCLAIM",
            "units": "dimensionless_after_common_normalization",
            "observable_link": "J_readout;J_mem;Q_mem;Newton;PPN;R10;R11;local_GR",
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
                    "runner_id": f"ICR2585_{row['row_id']}",
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
            "gate_id": "CG2585_0_chainmap_zero",
            "claim": "[d,Pi_M]J_H=0 for current MTS",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "fixed chainmap theorem is conditional; parent selector/current/domain antecedents are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2585_1_Icommutator_score",
            "claim": "I_commutator row is score-ready",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "no numeric/source-backed value, denominator, source path or arena kernel exists",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2585_2_projector_stress",
            "claim": "projector variation/stress is zero or bounded",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "topological no-stress route is not parent-signed and Hodge/domain route keeps stress",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2585_3_source_normalization",
            "claim": "measured-GM/source-normalization bridge reopens",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "J_PiM_comm and R_eq guard remain retained residuals",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2585_4_Newton_local_GR",
            "claim": "Newton/local-GR source bridge is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "physical current/domain/source denominator is not parent-owned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG2585_5_conditional_progress",
            "claim": "fixed-chainmap lemma accepted as useful conditional theorem",
            "gate_status": "PASS_NONCLAIM",
            "reason": "the algebraic obstruction is isolated; the remaining work is parent ownership and source-complex descent",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [with_stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2585_0_conditional_theorem_kept",
            "decision": "FIXED_CHAINMAP_ZERO_IS_MATHEMATICALLY_CLEAN",
            "reason": "if Pi_M is a parent fixed chain map on the physical Hilbert-current complex, the commutator term vanishes exactly",
            "effect": "do not waste future passes re-deriving the product-rule algebra unless new parent evidence appears",
        },
        {
            "decision_id": "DEC2585_1_current_claim_rejected",
            "decision": "CURRENT_MTS_DOES_NOT_PROVE_CHAINMAP_ANTECEDENTS",
            "reason": "parent selector, fixed worldtube/domain, physical current complex, topological-Hilbert same-object guard, boundary flux and M_H_ref locks are unsigned",
            "effect": "OBS2584_1 remains retained nonclaim",
        },
        {
            "decision_id": "DEC2585_2_bound_fill_not_ready",
            "decision": "ICOMMUTATOR_BOUND_ROWS_STAGED_NOT_SCORED",
            "reason": "all coefficient rows still lack numeric values, units normalization, source paths and common denominator",
            "effect": "empirical runner must refuse them until source-backed rows exist",
        },
        {
            "decision_id": "DEC2585_3_next",
            "decision": "SOURCE_WORLDTUBE_CURRENT_COMPLEX_SELECTED_NEXT",
            "reason": "the narrowest missing antecedent is proving J_H, W_source, A_ext, S_link and tau live in the same parent-owned complex before readout",
            "effect": "2586 should attack source/current/domain descent rather than circling the Pi_M algebra",
        },
    ]
    return [with_stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2585_0_selected",
            "selection_status": "selected",
            "target_file": "2586-Y5-R2FR-source-worldtube-current-complex-owner-or-Jdomain-bound-fill.md",
            "target_script": "scripts/Y5_R2FR_source_worldtube_current_complex_owner_or_Jdomain_bound_fill_2586.py",
            "task": "prove W_source, A_ext, S_link, J_H[e_obs,tau] and tau are parent-owned before readout and live in the same Hilbert-current complex used by Pi_M, or fill domain/current-escape bound rows with units and source paths",
            "acceptance_target": "the chainmap antecedent for J_H in C_H(A_ext) is parent-signed, or J_domain/E_current_escape becomes a source-backed nonclaim residual vector",
            "guardrails": "no source worldtube chosen after fitting; no observed GM normalization; no Noether conservation alone as source equality; no closed wrong charge; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
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
                    "copy_id": f"COPY2585_{copy_id}",
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

    add("VAL2585_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2585_01_conditional_theorem",
        any(row["audit_id"] == "CMA2585_1_fixed_chainmap_theorem" and row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in data["chainmap_audit"]),
        "fixed chainmap theorem is recorded as conditional-clean",
    )
    add(
        "VAL2585_02_zero_not_promoted",
        any(row["audit_id"] == "CMA2585_7_verdict" and row["valid_for_claim"] is False for row in data["chainmap_audit"]),
        "current MTS PiM chainmap zero is not promoted",
    )
    add(
        "VAL2585_03_antecedents_blocked",
        all(row["gate_pass"] is False and row["valid_for_claim"] is False for row in data["antecedents"]),
        "all parent antecedent gates remain blocked",
    )
    add(
        "VAL2585_04_bound_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["icommutator_rows"]),
        "I_commutator/J_PiM bound rows remain nonclaim",
    )
    add(
        "VAL2585_05_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses unfilled chainmap rows",
    )
    add(
        "VAL2585_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no source-normalization, Newton, PPN or local-GR claim is allowed",
    )
    add(
        "VAL2585_07_next_target_written",
        any(row["route_id"] == "NEXT2585_0_selected" for row in data["next"]),
        "2586 source-worldtube/current-complex target selected",
    )
    add(
        "VAL2585_08_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2585-Y5-R2FR-PiM-chainmap*",
            "*Y5_R2FR_PiM_chainmap_commutator*",
            "*P8_Y5_PIM_CHAINMAP_2585*",
            "*JR2585*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2585_09_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2585 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2585_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2585_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2585_OVERALL",
        overall,
        "2585 preserves fixed-chainmap zero as conditional, keeps current MTS nonclaim, stages I_commutator rows, and selects source-worldtube/current-complex owner next",
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
        "# 2585 Y5 R2FR PiM chainmap commutator zero or Icommutator bound fill",
        "",
        "**Status:** private nonclaim derivation checkpoint. The fixed-chainmap lemma is accepted as exact conditional mathematics, but current MTS does not prove its parent antecedents.",
        "",
        "**Main result:** `[d,Pi_M]J_H=0` is not a mysterious new physics problem. It follows immediately if `Pi_M` is a parent-selected fixed chain map on the same compact-exterior Hilbert-current complex that contains the observed source current. The current corpus has not signed that source/current/domain complex, so `I_commutator_abs` and the wider `J_PiM_comm` ledger remain explicit nonclaim measured-GM obstruction rows.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Chainmap Theorem Audit",
        markdown_table(data["chainmap_audit"], ["audit_id", "claim_piece", "formal_statement", "result", "blocking_gap", "effect", "valid_for_claim", "claim_allowed"]),
        "",
        "## Antecedent Gate",
        markdown_table(data["antecedents"], ["gate_id", "antecedent", "required_evidence", "current_status", "blocks", "gate_pass", "valid_for_claim"]),
        "",
        "## Icommutator Bound Rows",
        markdown_table(data["icommutator_rows"], ["row_id", "symbol", "definition", "needed_for_claim", "current_status", "units", "observable_link", "numeric_value", "source_path", "score_ready", "valid_for_claim", "claim_allowed"]),
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

    icommutator_rows_data = icommutator_bound_rows()
    data = {
        "sources": source_register_rows(),
        "chainmap_audit": chainmap_audit_rows(),
        "antecedents": antecedent_gate_rows(),
        "icommutator_rows": icommutator_rows_data,
        "runner_refusal": runner_refusal_rows(icommutator_rows_data),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["chainmap_audit"], data["chainmap_audit"])
    write_csv(OUTPUTS["antecedent_gate"], data["antecedents"])
    write_csv(OUTPUTS["icommutator_rows"], data["icommutator_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2585_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
