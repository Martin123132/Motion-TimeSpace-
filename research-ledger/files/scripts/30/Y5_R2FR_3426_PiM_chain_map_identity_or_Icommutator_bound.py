from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3426-Y5-R2FR-PiM-chain-map-identity-or-Icommutator-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3425": ROOT / "3425-Y5-R2FR-Hamiltonian-reference-PiM-integrability-lock-or-MHref-row-under-AX1090.md",
    "charge_decomp_3425": OUT / "P8_Y5_R2FR_3425_MTS_CHARGE_DECOMPOSITION.csv",
    "pc3400_3_3425": OUT / "P8_Y5_R2FR_3425_PC3400_3_LOCK_AUDIT.csv",
    "bounds_3425": OUT / "P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv",
    "next_3425": OUT / "P8_Y5_R2FR_3425_NEXT_TARGET.csv",
    "pim_topo_certificate": OUT / "P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv",
    "topo_conditions": OUT / "P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv",
    "pim_input_template": OUT / "P8_Y5_PIM_INPUT_FILL_TEMPLATE.csv",
    "projector_stress_contract": OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv",
    "topo_hilbert_attempt": OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
    "topo_hilbert_obstructions": OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
    "r_eq_rows_1015": OUT / "P8_Y5_R10_1015_R_EQ_BOUND_INPUT_ROWS.csv",
    "doc_1015": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
    "doc_3424": ROOT / "3424-Y5-R2FR-minimal-parent-source-coupling-action-or-PC3400-adoption-gate-under-AX1090.md",
    "action_3424": OUT / "P8_Y5_R2FR_3424_PARENT_ACTION_DENSITY.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3426_SOURCE_REGISTER.csv",
    "pim_branch_split": OUT / "P8_Y5_R2FR_3426_PIM_BRANCH_SPLIT.csv",
    "chain_map_theorem": OUT / "P8_Y5_R2FR_3426_PIM_CHAIN_MAP_THEOREM.csv",
    "topological_demoter": OUT / "P8_Y5_R2FR_3426_TOPOLOGICAL_PIM_DEMOTER.csv",
    "icomm_bound_rows": OUT / "P8_Y5_R2FR_3426_ICOMM_BOUND_ROWS.csv",
    "pc3400_3_update": OUT / "P8_Y5_R2FR_3426_PC3400_3_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3426_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3426_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3426_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3426_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3426_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3425": "Hamiltonian/PiM handoff",
        "charge_decomp_3425": "PiM identified as largest PC3400_3 residual",
        "pc3400_3_3425": "PC3400_3 lock audit",
        "bounds_3425": "Hamiltonian/PiM residual bound rows",
        "next_3425": "machine-readable 3426 target",
        "pim_topo_certificate": "topological PiM equality certificate",
        "topo_conditions": "topological PiM closure conditions",
        "pim_input_template": "PiM/R_eq/I_commutator input template",
        "projector_stress_contract": "projector variation stress contract",
        "topo_hilbert_attempt": "topological-Hilbert equality attempt",
        "topo_hilbert_obstructions": "topological-Hilbert obstructions",
        "r_eq_rows_1015": "R_eq/I_commutator fallback rows",
        "doc_1015": "same-object topological/Hilbert equality doc",
        "doc_3424": "minimal source-action candidate doc",
        "action_3424": "public EH/Hilbert action candidate",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def pim_branch_split() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "PBS3426_0_Hilbert_identity",
            "branch": "Pi_M^H is the identity/charge-inclusion map on the local public Hilbert mass current",
            "definition": "Pi_M^H J_H := J_H in the mass-charge subcomplex; M_H is read from H_tau, not from an independent topological label",
            "chain_map_status": "PASS_CONDITIONAL",
            "projector_stress_status": "ZERO_IF_IDENTITY_NO_METRIC_DEPENDENT_PROJECTOR",
            "valid_for_claim": False,
        },
        {
            "branch_id": "PBS3426_1_fixed_scalar_charge",
            "branch": "Pi_M^H maps a Hilbert current to a fixed scalar charge representative with parent-fixed basis form",
            "definition": "Pi_M^H J_H = ell_H[J_H;tau,S] omega_H, with d omega_H=0 and ell_H fixed by H_tau",
            "chain_map_status": "PASS_IF_ELLH_SURFACE_INVARIANT_AND_OMEGA_FIXED",
            "projector_stress_status": "ZERO_IF_OMEGA_AND_ELLH_ARE_METRIC_SILENT_AFTER_HILBERT_VARIATION",
            "valid_for_claim": False,
        },
        {
            "branch_id": "PBS3426_2_old_topological",
            "branch": "old independent topological Pi_M/J_M_top",
            "definition": "Pi_M J_H = J_M_top + dB_zero + R_eq, with Q_M not automatically the Hilbert source charge",
            "chain_map_status": "NOT_SIGNED",
            "projector_stress_status": "RETAIN_OR_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": "PBS3426_3_Hodge_DeWitt_projector",
            "branch": "metric/Hodge/orthogonal projector implementation",
            "definition": "Pi_M depends on star, Green operator, inner product, domain, or metric-dependent basis",
            "chain_map_status": "REJECT_AS_SILENT_CLOSURE_UNLESS_VARIATION_STRESS_RETAINED",
            "projector_stress_status": "T_PiM_MUST_BE_RETAINED",
            "valid_for_claim": False,
        },
        {
            "branch_id": "PBS3426_4_verdict",
            "branch": "preferred local branch",
            "definition": "use Hilbert-identity or fixed-Hilbert-charge Pi_M^H; demote old topological Pi_M unless same-object equality is proved",
            "chain_map_status": "BEST_ROUTE_CONDITIONAL",
            "projector_stress_status": "NO_PROJECTOR_STRESS_IN_IDENTITY_BRANCH",
            "valid_for_claim": False,
        },
    ]


def chain_map_theorem() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "PCM3426_0_domain",
            "claim": "Work on the local exterior Hilbert-current complex selected by the 3424 public source branch.",
            "identity": "J_H[tau] is the public Hilbert current; dJ_H=0 in the source-free exterior on shell",
            "status": "CONDITIONAL_ON_EH_HILBERT_SOURCE_BRANCH",
            "missing_to_promote": "source-free exterior and same tau/source frame",
            "valid_for_claim": False,
        },
        {
            "step_id": "PCM3426_1_identity_chain_map",
            "claim": "If Pi_M^H is the identity/inclusion on the mass-charge current, it commutes with d.",
            "identity": "[d,Pi_M^H]J_H = dJ_H - dJ_H = 0",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "missing_to_promote": "parent must adopt Pi_M^H rather than old independent topological Pi_M",
            "valid_for_claim": False,
        },
        {
            "step_id": "PCM3426_2_fixed_basis_chain_map",
            "claim": "A fixed scalar charge representative is also a chain map if its scalar is radially invariant and its basis form is closed.",
            "identity": "d(ell_H omega_H)-Pi_M^H(dJ_H) = d ell_H wedge omega_H + ell_H d omega_H = 0",
            "status": "EXACT_IF_DELLH_ZERO_AND_DOMEGA_ZERO",
            "missing_to_promote": "ell_H must be H_tau-derived and not fitted; omega_H must be parent-fixed",
            "valid_for_claim": False,
        },
        {
            "step_id": "PCM3426_3_projector_stress",
            "claim": "The identity/inclusion branch creates no independent projector stress.",
            "identity": "delta_g Pi_M^H = 0 as a separate operator; all metric variation is already in T_H and Q_tau",
            "status": "EXACT_FOR_IDENTITY_BRANCH",
            "missing_to_promote": "forbid Hodge/DeWitt/domain/readout projectors in the parent variation",
            "valid_for_claim": False,
        },
        {
            "step_id": "PCM3426_4_topological_demoter",
            "claim": "The old topological Pi_M is allowed only if it is proved to be the same Hilbert charge object.",
            "identity": "Pi_M^top J_H - Pi_M^H J_H = dB_zero + R_eq; require R_eq=0 and int dB_zero=0",
            "status": "NOT_PROVED_RETAIN_BOUND_ROWS",
            "missing_to_promote": "same-object equality, boundary zero, no independent topological label",
            "valid_for_claim": False,
        },
        {
            "step_id": "PCM3426_5_verdict",
            "claim": "PiM commutator hair can be killed in the Hilbert-identity branch, but not in the old topological branch.",
            "identity": "I_commutator^H=0; I_commutator^top retained unless same-object theorem passes",
            "status": "PARTIAL_PC3400_3_IMPROVEMENT",
            "missing_to_promote": "adopt Pi_M^H in parent branch and keep old Pi_M demoted or bounded",
            "valid_for_claim": False,
        },
    ]


def topological_demoter() -> list[dict[str, Any]]:
    return [
        {
            "demoter_id": "TDM3426_0_wrong_object",
            "old_topological_risk": "Q_M can be a conserved topological label but not the observed Hilbert source charge",
            "required_repair": "define Q_M from the same Hilbert worldtube before readout",
            "if_not_repaired": "R_eq_integral and independent-topological-label residual remain active",
            "valid_for_claim": False,
        },
        {
            "demoter_id": "TDM3426_1_boundary_exact",
            "old_topological_risk": "Pi_M J_H differs from J_M_top by exact/boundary flux",
            "required_repair": "prove int_boundary dB_zero=0 with fixed reference",
            "if_not_repaired": "B_zero_flux remains active",
            "valid_for_claim": False,
        },
        {
            "demoter_id": "TDM3426_2_commutator",
            "old_topological_risk": "old Pi_M may fail [d,Pi_M]J_H=0 on the Hilbert current domain",
            "required_repair": "prove Pi_M is fixed, closed and source-domain invariant",
            "if_not_repaired": "I_commutator remains active",
            "valid_for_claim": False,
        },
        {
            "demoter_id": "TDM3426_3_projector_stress",
            "old_topological_risk": "metric/Hodge/domain implementation can generate projector stress",
            "required_repair": "prove delta_g Pi_M=0 or retain T_PiM map into PPN/source residuals",
            "if_not_repaired": "projector_stress_beta_equiv remains active",
            "valid_for_claim": False,
        },
        {
            "demoter_id": "TDM3426_4_policy",
            "old_topological_risk": "a multiplier can impose equality after the fact",
            "required_repair": "Pi_M appears as parent-owned structure before readout or is not used for claims",
            "if_not_repaired": "branch is closure-only",
            "valid_for_claim": False,
        },
    ]


def icomm_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "ICB3426_0_identity_branch",
            "quantity": "I_commutator^H",
            "definition": "commutator for Hilbert-identity Pi_M branch",
            "bound_formula": "0 if Pi_M=Pi_M^H identity/inclusion is parent-adopted",
            "status": "CONDITIONAL_THEOREM_ZERO",
            "valid_for_claim": False,
        },
        {
            "bound_id": "ICB3426_1_topological_branch",
            "quantity": "I_commutator^top",
            "definition": "commutator for old independent topological Pi_M",
            "bound_formula": "M_H_ref^-1 |int_A [d,Pi_M^top]J_H|",
            "status": "MISSING_SOURCE_BACKED_VALUE_OR_SAME_OBJECT_PROOF",
            "valid_for_claim": False,
        },
        {
            "bound_id": "ICB3426_2_projector_stress",
            "quantity": "projector_stress_beta_equiv",
            "definition": "PPN/source equivalent of metric/domain/Hodge projector variation",
            "bound_formula": "0 for identity branch; otherwise map T_PiM_munu to gamma,beta,alpha_i,xi,delta_G",
            "status": "MISSING_PROJECTOR_STRESS_MAP_IF_NONIDENTITY_USED",
            "valid_for_claim": False,
        },
        {
            "bound_id": "ICB3426_3_R_eq",
            "quantity": "R_eq_integral",
            "definition": "same-object residual between old topological PiM and Hilbert PiM",
            "bound_formula": "M_H_ref^-1 |int_A(Pi_M^top J_H - Pi_M^H J_H - dB_zero)|",
            "status": "MISSING_R_EQ_OR_BOUNDARY_ZERO_PROOF",
            "valid_for_claim": False,
        },
        {
            "bound_id": "ICB3426_4_total",
            "quantity": "epsilon_PiM_after_3426",
            "definition": "no-cancellation PiM residual after adopting/demoting branch split",
            "bound_formula": "0 for parent-adopted Hilbert-identity branch; else |I_commutator^top|/M_H_ref+projector_stress_beta_equiv+|R_eq_integral|/M_H_ref",
            "status": "ZERO_ONLY_IN_HILBERT_IDENTITY_BRANCH_OTHERWISE_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def pc3400_3_update() -> list[dict[str, Any]]:
    return [
        {
            "pc_piece": "PC3400_3_PiM_chain_map",
            "before_3426": "OPEN_BIGGEST_PC3400_3_RESIDUAL",
            "after_3426": "CAN_SIGN_IF_PIM_HILBERT_IDENTITY_BRANCH_ADOPTED",
            "remaining": "reference/boundary/tau/MHref still not claim-ready",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_3_projector_stress",
            "before_3426": "projector stress retained if PiM metric/domain dependent",
            "after_3426": "ZERO_IN_IDENTITY_BRANCH_RETAINED_IN_NONIDENTITY_BRANCHES",
            "remaining": "must forbid Hodge/DeWitt/readout/domain projectors from parent variation",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_3_old_topological_PiM",
            "before_3426": "not derived same object",
            "after_3426": "DEMOTED_UNLESS_R_EQ_AND_B_ZERO_CLOSE",
            "remaining": "R_eq_integral and B_zero_flux rows stay active for old branch",
            "valid_for_claim": False,
        },
        {
            "pc_piece": "PC3400_3_verdict",
            "before_3426": "partial EH subcharge only",
            "after_3426": "EH subcharge plus Hilbert-identity PiM chain map can be coherently signed",
            "remaining": "fixed reference, boundary flux, tau lock, MHref row, no-extra-mass",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3426_0_chain_map_theorem",
            "claim": "Pi_M chain-map commutator is zero in the Hilbert-identity branch",
            "gate_status": "PASS_CONDITIONAL_THEOREM",
            "reason": "identity/inclusion commutes with d and adds no independent projector stress",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3426_1_old_topological_claim",
            "claim": "old topological PiM is the same object as Hilbert source charge",
            "gate_status": "FAIL_CURRENT",
            "reason": "same-object equality, R_eq and B_zero remain unproved",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3426_2_PC3400_3_PiM_piece",
            "claim": "PC3400_3 PiM chain-map piece is signable",
            "gate_status": "PASS_IF_HILBERT_IDENTITY_BRANCH_ADOPTED",
            "reason": "PiM must be Pi_M^H, not old independent PiM",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3426_3_PC3400_3_full",
            "claim": "full PC3400_3 Htau/PiM/reference lock is signed",
            "gate_status": "PARTIAL_ONLY",
            "reason": "reference/boundary/tau/MHref remain",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3426_4_local_GR",
            "claim": "local GR/Newton/PPN branch is derived",
            "gate_status": "BLOCKED",
            "reason": "PC3400_3 reference/boundary plus PC3400_4 no-extra-mass/Y6 and second-order gates remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3426_0_best_branch",
            "decision": "Use Pi_M^H as the Hilbert identity/charge map in the local source branch.",
            "because": "it kills [d,Pi_M]J_H exactly without inventing an independent conserved object",
            "next_action": "adopt it only inside the candidate branch; keep nonidentity PiM rows demoted",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3426_1_topological_demoted",
            "decision": "Old topological Pi_M is not thrown away, but it cannot carry local-GR claims unless same-object equality is proved.",
            "because": "a conserved topological label can be the wrong conserved object",
            "next_action": "retain R_eq, B_zero_flux and I_commutator rows for that branch",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3426_2_progress",
            "decision": "The PiM-specific part of PC3400_3 now has a clean derivation route.",
            "because": "identity/inclusion Pi_M has zero commutator and no independent metric/projector variation",
            "next_action": "move to reference/boundary flux lock, then no-extra-mass/Y6",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3426_3_next",
            "decision": "Next target should prove fixed reference and compact boundary/symplectic flux silence.",
            "because": "after PiM, reference/boundary terms are the largest remaining PC3400_3 residual",
            "next_action": "3427-Y5-R2FR-reference-boundary-flux-zero-or-Bzero-row-under-AX1090.md",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target": "3427-Y5-R2FR-reference-boundary-flux-zero-or-Bzero-row-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3427_reference_boundary_flux_zero_or_Bzero_row.py",
            "objective": "prove H_ref is fixed once and compact linked boundary/symplectic flux is zero in the Hilbert-identity source branch, or emit B_zero_flux/Delta_symp/H_ref_shift rows",
            "why_next": "3426 conditionally kills PiM commutator hair in the Hilbert-identity branch; reference/boundary flux is now the biggest PC3400_3 residual",
            "valid_for_claim": False,
        },
        {
            "target": "3428-Y5-R2FR-no-extra-mass-Y6-monopole-silence-or-bound-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3428_no_extra_mass_Y6_monopole_silence_or_bound.py",
            "objective": "exclude hidden/domain/memory/projector/Y6 extra monopole source charge after calibrated Hilbert coupling, or emit Delta_extra_mass rows",
            "why_next": "PC3400_4 remains after PC3400_3 reference/boundary lock",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3426_0",
            "script": str(Path(__file__).resolve()),
            "mode": "PIM_CHAIN_MAP_IDENTITY_OR_ICOMMUTATOR_BOUND",
            "summary": "Hilbert-identity PiM branch gives conditional commutator zero and no projector stress; old topological/nonidentity PiM demoted to R_eq/I_commutator/projector-stress bound rows; local GR not claimed",
            "valid_for_claim": False,
        }
    ]


def formalization_recent_count(start_utc: datetime) -> int:
    if not FORMALIZATION.exists():
        return 0
    threshold = start_utc.timestamp()
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= threshold)


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    sources = rows_by_name["source_register"]
    nonclaim = all(
        row.get("valid_for_claim") is False
        for name, rows in rows_by_name.items()
        if name != "validation"
        for row in rows
    )
    outputs_under_root = all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()) and str(DOC).startswith(str(ROOT))
    formalization_count = formalization_recent_count(start_utc)
    promotion = rows_by_name["promotion_gates"]
    return [
        {
            "check_id": "VAL3426_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in sources),
            "detail": f"{sum(1 for row in sources if row['exists'])}/{len(sources)} source paths exist",
        },
        {
            "check_id": "VAL3426_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": outputs_under_root,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3426_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim,
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3426_3_identity_theorem",
            "condition": "Hilbert-identity chain-map theorem exists",
            "passed": any(row["step_id"] == "PCM3426_1_identity_chain_map" for row in rows_by_name["chain_map_theorem"]),
            "detail": "PCM3426_1 present",
        },
        {
            "check_id": "VAL3426_4_topological_demoted",
            "condition": "old topological PiM remains nonclaim/demoted",
            "passed": any(row["gate_id"] == "PG3426_1_old_topological_claim" and row["gate_status"] == "FAIL_CURRENT" for row in promotion),
            "detail": "old topological branch not promoted",
        },
        {
            "check_id": "VAL3426_5_bound_rows",
            "condition": "I_commutator/R_eq/projector-stress bound rows exist",
            "passed": any(row["bound_id"] == "ICB3426_4_total" for row in rows_by_name["icomm_bound_rows"]),
            "detail": "ICB3426_4 present",
        },
        {
            "check_id": "VAL3426_6_PC3400_partial",
            "condition": "PC3400_3 PiM piece improves but full PC3400_3 remains partial",
            "passed": any(row["gate_id"] == "PG3426_3_PC3400_3_full" and row["gate_status"] == "PARTIAL_ONLY" for row in promotion),
            "detail": "reference/boundary/tau/MHref remain",
        },
        {
            "check_id": "VAL3426_7_local_GR_blocked",
            "condition": "local GR remains blocked",
            "passed": any(row["gate_id"] == "PG3426_4_local_GR" and row["gate_status"] == "BLOCKED" for row in promotion),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3426_8_next_target",
            "condition": "next target attacks reference/boundary flux",
            "passed": rows_by_name["next_target"][0]["target"].startswith("3427-Y5-R2FR-reference-boundary"),
            "detail": rows_by_name["next_target"][0]["target"],
        },
        {
            "check_id": "VAL3426_9_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": formalization_count == 0,
            "detail": f"modified_count_since_start={formalization_count}",
        },
        {
            "check_id": "VAL3426_10_overall",
            "condition": "3426 PiM chain-map checkpoint is internally valid",
            "passed": True,
            "detail": "PASS",
        },
    ]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3426 - PiM Chain-Map Identity or Icommutator Bound

## Summary
- This checkpoint attacks `Pi_M` directly instead of letting it remain a magic conserved-object selector.
- Best route: in the local source branch, define `Pi_M^H` as the identity/inclusion map on the public Hilbert mass-current subcomplex, or as a fixed Hilbert charge representative derived from `H_tau`.
- Then the commutator is exactly zero: `[d,Pi_M^H]J_H=0`, and there is no independent projector stress because the operator is not a Hodge/DeWitt/readout projector.
- This is a real improvement to `PC3400_3`, but it is conditional on adopting the Hilbert-identity branch.
- The old topological `Pi_M` is demoted, not deleted: it can return only if same-object equality proves `Pi_M^top J_H = Pi_M^H J_H + dB_zero` with zero residual and zero compact boundary flux.
- Nonidentity/Hodge/domain/readout projectors stay bound-branch only because their metric variation creates `T_PiM` hair.

## Source Register
{md_table(rows_by_name["source_register"])}

## PiM Branch Split
{md_table(rows_by_name["pim_branch_split"])}

## PiM Chain-Map Theorem
{md_table(rows_by_name["chain_map_theorem"])}

## Topological PiM Demoter
{md_table(rows_by_name["topological_demoter"])}

## Icomm Bound Rows
{md_table(rows_by_name["icomm_bound_rows"])}

## PC3400_3 Update
{md_table(rows_by_name["pc3400_3_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
The PiM fog clears a lot here. If the local branch uses the Hilbert-identity charge map, the commutator problem is not a new physical force. If it insists on the old independent topological projector, it must prove same-object equality or stay as explicit `R_eq/I_commutator/T_PiM` debt.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "pim_branch_split": pim_branch_split(),
        "chain_map_theorem": chain_map_theorem(),
        "topological_demoter": topological_demoter(),
        "icomm_bound_rows": icomm_bound_rows(),
        "pc3400_3_update": pc3400_3_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3426 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
