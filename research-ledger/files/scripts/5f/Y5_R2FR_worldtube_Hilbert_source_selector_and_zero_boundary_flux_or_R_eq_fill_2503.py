from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_WORLDTUBE_HILBERT_SELECTOR_ZERO_FLUX_OR_REQ_FILL_2503"
CHECKPOINT_ID = "2503"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2503-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R-eq-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_NO_SHADOW_2503_SOURCE_REGISTER.csv",
    "selector_theorem": OUT / "P8_Y5_NO_SHADOW_2503_WORLDTUBE_HILBERT_SELECTOR_THEOREM.csv",
    "source_contract": OUT / "P8_Y5_NO_SHADOW_2503_SOURCE_MEASURE_CONTRACT_AUDIT.csv",
    "boundary_flux": OUT / "P8_Y5_NO_SHADOW_2503_ZERO_BOUNDARY_FLUX_AUDIT.csv",
    "residual_rows": OUT / "P8_Y5_NO_SHADOW_2503_SELECTOR_RESIDUAL_ROWS.csv",
    "live_binding": OUT / "P8_Y5_NO_SHADOW_2503_LIVE_LOCAL_GR_BINDING_STATUS.csv",
    "claim_gates": OUT / "P8_Y5_NO_SHADOW_2503_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_NO_SHADOW_2503_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_NO_SHADOW_2503_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_NO_SHADOW_2503_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2503_VALIDATION.csv",
}

COPY_TARGETS = {
    "selector_theorem": LOCAL_BOUNDS / "Worldtube_Hilbert_selector_theorem_2503_NONCLAIM.csv",
    "source_contract": LOCAL_BOUNDS / "Source_measure_contract_audit_2503_NONCLAIM.csv",
    "residual_rows": QUEUE / "JR2503_SELECTOR_RESIDUAL_ROWS_NONCLAIM.csv",
    "live_binding": BETA_DOCS / "Live_local_GR_binding_status_2503_NONCLAIM.csv",
    "next_target": QUEUE / "JR2503_MINIMAL_PARENT_ACTION_CHARGE_CONTRACT_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2503_00_2502_handoff",
        "source_path": ROOT / "2502-Y5-R2FR-parent-Hcore-QR-source-equation-or-boundary-charge-owner.md",
        "needles": ["NEXT2502_0_selected", "EM2502_5_verdict", "VAL2502_OVERALL"],
        "role": "current live handoff into worldtube-Hilbert source selector",
    },
    {
        "source_id": "SRC2503_01_2183_selector",
        "source_path": ROOT / "2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md",
        "needles": ["WST2183_5_R_eq_zero_condition", "BFA2183_4_zero_flux_verdict", "VAL2183_OVERALL"],
        "role": "prior conditional worldtube-Hilbert selector theorem",
    },
    {
        "source_id": "SRC2503_02_2184_charge_contract",
        "source_path": ROOT / "2184-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
        "needles": ["MAS2184_1_action_skeleton", "NHC2184_4_PiM_identification", "VAL2184_OVERALL"],
        "role": "next-stage minimal parent-action Hamiltonian charge contract",
    },
    {
        "source_id": "SRC2503_03_1015_same_object",
        "source_path": ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
        "needles": ["SOL1015_3_de_rham_equality", "CG1015_3_topological_Hilbert_equality", "V1015_SUMMARY"],
        "role": "same-object de Rham/Poincare-dual equality lemma and residual rows",
    },
    {
        "source_id": "SRC2503_04_hilbert_worldtube_attempt",
        "source_path": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_0_parent_worldtube_fixed", "HWT536_5_exact_and_reference_terms_zero", "HWT536_8_weak_field_readout_after_charge_glue"],
        "role": "Hilbert worldtube theorem attempt and missing certificate map",
    },
    {
        "source_id": "SRC2503_05_hilbert_worldtube_certificate",
        "source_path": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
        "needles": ["HWG535_0_worldtube_fixed_before_readout", "HWG535_3_exact_term_zero", "HWG535_5_no_projector_stress"],
        "role": "certificate rows for missing worldtube and boundary zero clauses",
    },
    {
        "source_id": "SRC2503_06_worldtube_measure",
        "source_path": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "needles": ["T510_1_worldtube_source_measure", "T510_2_MTS_transfer_condition", "T510_3_Newton_PPN_readout"],
        "role": "GR-style worldtube source measure and MTS transfer condition",
    },
    {
        "source_id": "SRC2503_07_hamiltonian_source_measure",
        "source_path": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "needles": ["HSM541_0_adopt_Hamiltonian_PiM", "HSM541_2_observed_worldtube_source", "HSM541_7_PPN_followthrough"],
        "role": "Hamiltonian mass-map, observed worldtube and PPN followthrough contract",
    },
    {
        "source_id": "SRC2503_08_obstructions",
        "source_path": OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
        "needles": ["OB501_0_independent_topological_label", "OB501_2_boundary_improvement", "OB501_3_hidden_exchange"],
        "role": "closed-wrong-object, boundary and hidden-channel obstruction map",
    },
    {
        "source_id": "SRC2503_09_noether_closure",
        "source_path": OUT / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv",
        "needles": ["T505_conditional_Noether_mass_charge_closure", "T505_source_measure_matching", "T505_Newton_limit_corollary"],
        "role": "conditional Noether mass charge closure theorem and limits",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8", newline="")
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:  # pragma: no cover
        return False, 0, str(error)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": str(path),
                    "exists": path.exists(),
                    "missing_needles": ";".join(missing),
                    "source_pass": path.exists() and not missing,
                    "role": source["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def selector_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "WHS2503_0_observed_current",
            "clause": "observed Hilbert current",
            "statement": "J_H[tau] is obtained from delta S_matter/delta e_obs, contracted with a fixed observed time generator tau.",
            "status": "CONDITIONAL_SOURCE_OWNER",
            "implication": "source mass starts from the same observed coframe used by clocks, rods and v readout",
            "missing": "explicit parent action and tau selector",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WHS2503_1_worldtube_selector",
            "clause": "compact source worldtube",
            "statement": "W_source := supp(J_H[e_obs,tau]) and linked surfaces must enclose that same W_source before readout/fitting.",
            "status": "EXACT_SELECTOR_DEFINITION_CONDITIONAL",
            "implication": "forbids choosing the source domain after seeing orbital residuals",
            "missing": "parent-owned support/topology selector",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WHS2503_2_hamiltonian_mass_map",
            "clause": "Pi_M as Hamiltonian charge map",
            "statement": "(4*pi*G_ref)^-1 int_S Pi_M J_H must equal H_tau[S]-H_ref.",
            "status": "CORE_IDENTITY_UNSIGNED",
            "implication": "Pi_M becomes measured source mass rather than a conserved wrong object",
            "missing": "Hamiltonian PiM adoption/derivation",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WHS2503_3_topological_representative",
            "clause": "J_M_top is PD(W_source)",
            "statement": "J_M_top := M_source[W] omega_W with d omega_W=0 and int_link omega_W=1 for the same W_source.",
            "status": "EXACT_CONDITIONAL_SAME_OBJECT_MAP",
            "implication": "topology can carry the measured Hilbert source charge",
            "missing": "same-worldtube representative certificate",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WHS2503_4_R_eq_zero",
            "clause": "topological-Hilbert equality residual",
            "statement": "If Pi_M J_H and J_M_top represent the same compact Hilbert source class, Pi_M J_H-J_M_top=dB_zero and R_eq=0.",
            "status": "EXACT_CONDITIONAL_R_EQ_ZERO",
            "implication": "the commutator/source-normalization route can close without a late multiplier",
            "missing": "same-object hypotheses are not parent-signed",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WHS2503_5_B_zero_flux",
            "clause": "zero compact boundary flux",
            "statement": "int_boundary dB_zero=0 must hold with a fixed reference, no compact leaks and no projector/symplectic stress shift.",
            "status": "B_ZERO_FLUX_ZERO_NOT_DERIVED",
            "implication": "prevents exact/reference bookkeeping from shifting measured GM",
            "missing": "fixed-reference and boundary-variation certificate",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WHS2503_6_current_verdict",
            "clause": "current MTS selector theorem",
            "statement": "The selector theorem is mathematically clean, but current MTS lacks a signed parent action, Hamiltonian PiM identity, worldtube selector and zero boundary flux.",
            "status": "SELECTOR_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS",
            "implication": "route remains live and serious, not claimable",
            "missing": "minimal parent-action charge contract or source-backed residual rows",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def source_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "SCA2503_0_parent_action",
            "contract": "covariant local parent action",
            "statement": "S_parent must own e_obs, matter, extra sectors, kappa, boundary reference and readout before source scoring.",
            "status": "MISSING_SIGNED_PARENT_ACTION",
            "effect_if_missing": "J_H/W_source/Pi_M may be post-hoc selectors",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA2503_1_tau",
            "contract": "fixed observed time generator",
            "statement": "tau must be fixed by local asymptotic/clock structure before H_tau and M_source are evaluated.",
            "status": "MISSING_TAU_SELECTOR",
            "effect_if_missing": "Hamiltonian mass drifts with clock/readout convention",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA2503_2_PiM",
            "contract": "Hamiltonian Pi_M identity",
            "statement": "Pi_M J_H must be the Hamiltonian/covariant-phase-space mass-charge map on the local branch.",
            "status": "PIM_HAMILTONIAN_IDENTITY_UNSIGNED",
            "effect_if_missing": "topological Pi_M can conserve a non-observed object",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA2503_3_same_source",
            "contract": "same Hilbert source measure",
            "statement": "M_source[W], M_eff[Pi_M J_H], v source rho_H and orbital GM must be the same source object.",
            "status": "SAME_SOURCE_CERTIFICATE_MISSING",
            "effect_if_missing": "epsilon_M remains a live Newton/source residual",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA2503_4_extra_channels",
            "contract": "extra mass-channel silence",
            "statement": "non-EH, memory, domain, range, frame, symplectic-boundary and projector channels add no independent mass charge.",
            "status": "EXTRA_CHANNEL_SILENCE_NOT_DERIVED",
            "effect_if_missing": "closed Hilbert flux does not equal full observed mass",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SCA2503_5_Gauss_readout",
            "contract": "same charge controls Newton coefficient",
            "statement": "nabla^2 Phi=4*pi*G_ref rho_H and a_r=-G_ref M_source/r^2 must use the same M_source.",
            "status": "NEWTON_GAUSS_READOUT_NOT_DERIVED",
            "effect_if_missing": "source equality cannot yet claim Newton/local GR",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def boundary_flux_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "flux_id": "BZF2503_0_fixed_reference",
            "clause": "fixed boundary/reference subtraction",
            "statement": "H_tau[reference] and B_zero reference must be selected once by the parent action/local boundary condition.",
            "status": "MISSING_FIXED_REFERENCE",
            "risk": "per-arena reference choices mimic fitted GM",
            "valid_for_claim": False,
        },
        {
            "flux_id": "BZF2503_1_outer_inner_flux",
            "clause": "no compact leak",
            "statement": "No residual dB_zero, symplectic, nonEH or boundary flux crosses the compact linked surfaces.",
            "status": "MISSING_COMPACT_FLUX_ZERO",
            "risk": "measured source shifts between linked surfaces",
            "valid_for_claim": False,
        },
        {
            "flux_id": "BZF2503_2_exact_not_enough",
            "clause": "exact term guard",
            "statement": "Pi_M J_H-J_M_top=dB_zero is not enough unless int_boundary dB_zero=0 in the scoring class.",
            "status": "REFERENCE_ONLY_ZERO_REJECTED",
            "risk": "exact bookkeeping hides a monopole/source shift",
            "valid_for_claim": False,
        },
        {
            "flux_id": "BZF2503_3_projector_stress",
            "clause": "no projector/symplectic stress",
            "statement": "B_zero and Pi_M must not reintroduce delta_g Pi_M, endpoint, tau, or symplectic stress at PPN order.",
            "status": "PROJECTOR_STRESS_SILENCE_UNSIGNED",
            "risk": "R_eq may close at monopole order while beta/PPN still fails",
            "valid_for_claim": False,
        },
        {
            "flux_id": "BZF2503_4_current_verdict",
            "clause": "zero boundary flux theorem",
            "statement": "Current sources do not certify B_zero_flux=0 with fixed reference, no compact leaks and projector-stress silence.",
            "status": "ZERO_BOUNDARY_FLUX_NOT_DERIVED_CURRENT_CORPUS",
            "risk": "B_zero_flux remains a finite/nonclaim residual row",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "RES2503_0_W_selector",
            "symbol": "epsilon_W_selector",
            "definition": "charge/domain shift from parent source worldtube selection W_source=supp(J_H[e_obs,tau])",
            "status": "MISSING_PARENT_WORLDTUBE_SELECTOR",
            "units": "dimensionless",
            "observable_link": "Newton;PPN;WEP;orbital",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "RES2503_1_tau",
            "symbol": "epsilon_tau_selector",
            "definition": "Hamiltonian source-charge drift from unresolved observed time generator tau",
            "status": "MISSING_TAU_SELECTOR_PROOF",
            "units": "dimensionless_or_charge_fraction",
            "observable_link": "Newton;clock;orbital",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "RES2503_2_PiM",
            "symbol": "epsilon_PiM_Hamiltonian",
            "definition": "failure of Pi_M J_H to equal the Hamiltonian mass-charge form",
            "status": "MISSING_PIM_HAMILTONIAN_IDENTITY",
            "units": "dimensionless_or_GM_flux",
            "observable_link": "Newton;PPN;R10;R11",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "RES2503_3_R_eq",
            "symbol": "R_eq_integral",
            "definition": "normalized compact support equality residual Pi_M J_H-J_M_top-dB_zero",
            "status": "MISSING_R_EQ_ZERO_OR_VALUE",
            "units": "dimensionless_after_M_H_ref_normalization",
            "observable_link": "Newton;PPN;R10;R11",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "RES2503_4_B_zero",
            "symbol": "B_zero_flux",
            "definition": "compact boundary flux of dB_zero/reference/symplectic improvement",
            "status": "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE",
            "units": "GM_flux_or_dimensionless_after_M_H_ref_normalization",
            "observable_link": "Newton;PPN;R7;R8;R9;R11",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "RES2503_5_I_commutator",
            "symbol": "I_commutator",
            "definition": "finite annulus integral of [d,Pi_M]J_H or dR_eq between linked surfaces",
            "status": "MISSING_I_COMMUTATOR_ZERO_OR_VALUE",
            "units": "GM_flux_or_dimensionless_after_M_H_ref_normalization",
            "observable_link": "Newton;R10;R11;radial_source",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "RES2503_6_extra",
            "symbol": "epsilon_extra_current",
            "definition": "nonEH, memory, symplectic-boundary, domain, range, frame, projector and calibration source channels",
            "status": "MISSING_EXTRA_CHANNEL_ZERO_OR_VALUE",
            "units": "dimensionless_or_GM_flux",
            "observable_link": "Newton;PPN;WEP;clock;R10;R11",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "RES2503_7_total",
            "symbol": "epsilon_M_abs_2503",
            "definition": "absolute no-cancellation envelope for selector, tau, PiM, R_eq, B_zero, commutator and extra-current residuals",
            "status": "MISSING_COMPONENT_INPUTS",
            "units": "dimensionless",
            "observable_link": "Newton;local_GR;PPN;R10;R11",
            "value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def live_binding_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "binding_id": "LGB2503_0_from_2502",
            "object": "Delta_Newton_v",
            "current_law": "Delta_Newton_v=(1+delta_KC)(1+epsilon_M)-1",
            "selector_effect": "2503 targets epsilon_M by source selector/topological-Hilbert equality",
            "status": "EPSILON_M_STILL_UNSIGNED",
            "next_dependency": "delta_KC remains separate action-coefficient target",
            "valid_for_claim": False,
        },
        {
            "binding_id": "LGB2503_1_R_eq",
            "object": "R_eq_integral",
            "current_law": "Pi_M J_H-J_M_top=dB_zero+R_eq",
            "selector_effect": "R_eq=0 if same compact Hilbert source class is parent-signed",
            "status": "CONDITIONAL_ZERO_NOT_CLAIMED",
            "next_dependency": "parent action must own W_source, PiM, tau and J_M_top",
            "valid_for_claim": False,
        },
        {
            "binding_id": "LGB2503_2_B_zero",
            "object": "B_zero_flux",
            "current_law": "exact improvement contributes no measured mass only if compact boundary flux vanishes",
            "selector_effect": "requires fixed reference and no symplectic/projector stress",
            "status": "BOUNDARY_ZERO_NOT_DERIVED",
            "next_dependency": "boundary/reference calculation in parent charge contract",
            "valid_for_claim": False,
        },
        {
            "binding_id": "LGB2503_3_local_GR",
            "object": "local GR/Newton branch",
            "current_law": "requires u=0 order, v source normalization, delta_KC=0, epsilon_M=0, kappa_v=0 and PPN residual silence",
            "selector_effect": "2503 advances only epsilon_M/source object leg",
            "status": "LOCAL_GR_CLAIM_BLOCKED",
            "next_dependency": "2504 minimal parent-action charge contract, then coefficient extraction",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2503_0_conditional_theorem",
            "claim": "worldtube-Hilbert selector theorem is a valid internal conditional route",
            "status": "PASS_GUARDRAIL",
            "reason": "same compact Hilbert source class gives R_eq=0 only under explicit premises",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2503_1_parent_action",
            "claim": "explicit MTS parent action owns J_H, tau, Pi_M, W_source and boundary reference",
            "status": "BLOCKED",
            "reason": "current sources contain contracts/skeletons, not a completed varied parent Lagrangian",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2503_2_R_eq_zero",
            "claim": "R_eq=0 is derived for current MTS",
            "status": "BLOCKED",
            "reason": "same-object selector premises remain unsigned",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2503_3_B_zero_flux",
            "claim": "B_zero_flux=0 is derived",
            "status": "BLOCKED",
            "reason": "fixed reference, no compact leak and projector-stress silence are not certified",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2503_4_Newton_local_GR",
            "claim": "Newton/local-GR source reduction can be claimed",
            "status": "BLOCKED",
            "reason": "epsilon_M residual rows remain missing/source-free and delta_KC/kappa_v remain open",
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2503_5_no_cheats",
            "claim": "closed-wrong-charge, late multiplier, fitted GM/reference or post-readout worldtube may pass",
            "status": "PASS_GUARDRAIL",
            "reason": "2503 explicitly rejects those routes",
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2503_0_gain",
            "decision": "SELECTOR_THEOREM_LIVE_IN_CURRENT_BRANCH",
            "reason": "R_eq=0 follows conditionally if topology is the same compact Hilbert source object",
            "effect": "epsilon_M is no longer vague; it has a selector/boundary residual structure",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2503_1_no_claim",
            "decision": "CURRENT_SELECTOR_PREMISES_UNSIGNED",
            "reason": "parent action, tau, Pi_M identity, W_source, B_zero flux and extra-channel silence remain unproved",
            "effect": "no Newton/local-GR claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2503_2_fallback",
            "decision": "RESIDUAL_ROWS_REMAIN_PRIMARY_IF_PARENT_CONTRACT_FAILS",
            "reason": "R_eq, B_zero_flux, I_commutator, epsilon_tau and epsilon_PiM have no theorem-zero or numeric values",
            "effect": "finite empirical source-normalization branch remains prepared",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2503_3_next",
            "decision": "MINIMAL_PARENT_ACTION_CHARGE_CONTRACT_NEXT",
            "reason": "the least circular next leap is to construct the action/Noether/Hamiltonian charge chain that owns the selector",
            "effect": "2504 should live-port the 2184 contract and push toward EH-to-v coefficient extraction",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2503_0_selected",
            "selection_status": "selected",
            "target_file": "2504-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
            "target_script": "scripts/Y5_R2FR_minimal_parent_action_Hamiltonian_charge_contract_or_selector_residual_fill_2504.py",
            "task": "construct the minimal covariant local parent-action charge contract that owns e_obs, J_H, Pi_M, tau, W_source, fixed reference and B_zero for the constrained v branch; otherwise demote selector route to explicit residual rows",
            "acceptance_target": "parent action skeleton derives Hilbert source current, Hamiltonian mass projector, source worldtube, topological representative, R_eq=0 and B_zero_flux=0 without post-readout choices; otherwise source-backed nonclaim residual rows are retained",
            "guardrails": "do not impose equality with a late multiplier, choose W_source after fitting, absorb source mismatch into G, claim Newton/local-GR from the conditional theorem, or use GitHub action",
            "valid_for_claim": False,
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "selector_theorem": OUTPUTS["selector_theorem"],
        "source_contract": OUTPUTS["source_contract"],
        "residual_rows": OUTPUTS["residual_rows"],
        "live_binding": OUTPUTS["live_binding"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, source in copy_map.items():
        target = COPY_TARGETS[key]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            stamp(
                {
                    "copy_id": f"COPY2503_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(
            stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if passed else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2503_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2503_01_selector_verdict",
        any(row["theorem_id"] == "WHS2503_6_current_verdict" and row["status"] == "SELECTOR_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS" for row in data["selector"]),
        "selector theorem is conditional and not promoted",
    )
    add(
        "VAL2503_02_source_contract",
        any(row["audit_id"] == "SCA2503_2_PiM" and row["status"] == "PIM_HAMILTONIAN_IDENTITY_UNSIGNED" for row in data["source_contract"]),
        "PiM/Hamiltonian identity remains explicit blocker",
    )
    add(
        "VAL2503_03_boundary_flux",
        any(row["flux_id"] == "BZF2503_4_current_verdict" and row["status"] == "ZERO_BOUNDARY_FLUX_NOT_DERIVED_CURRENT_CORPUS" for row in data["boundary"]),
        "zero boundary flux remains unsigned",
    )
    add(
        "VAL2503_04_residual_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["residuals"]),
        "all selector residual rows remain nonclaim and not score-ready",
    )
    add(
        "VAL2503_05_live_binding",
        any(row["binding_id"] == "LGB2503_3_local_GR" and row["status"] == "LOCAL_GR_CLAIM_BLOCKED" for row in data["live_binding"]),
        "live local-GR binding remains blocked",
    )
    add(
        "VAL2503_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["gates"]),
        "claim gates deny Newton/local-GR and shortcut promotion",
    )
    add(
        "VAL2503_07_next_target",
        any(row["route_id"] == "NEXT2503_0_selected" for row in data["next"]),
        "2504 minimal parent-action charge contract selected",
    )
    add(
        "VAL2503_08_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2503*", "*P8_Y5_NO_SHADOW_2503*", "*JR2503*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add("VAL2503_09_no_formalization_artifacts", not formalization_artifacts, "no 2503 artifacts were written to formalization-workbench", ";".join(str(path) for path in formalization_artifacts))

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2503_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2503_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2503_OVERALL",
        overall,
        "2503 installs the worldtube-Hilbert selector theorem in the live branch, keeps current MTS nonclaim, and selects parent-action charge contract next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("|", "\\|").replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2503 Y5 R2FR Worldtube-Hilbert Source Selector And Zero Boundary Flux Or R_eq Fill",
        "",
        "**Status:** private nonclaim checkpoint. `2503` installs the worldtube-Hilbert selector theorem in the live `2502` local-GR/Newton branch, but it does not claim Newton, PPN, or local GR.",
        "",
        "**Main result:** topology is a serious route only if it is the same measured Hilbert source object. The target chain is `parent action -> J_H[e_obs,tau] -> W_source -> Hamiltonian Pi_M mass map -> J_M_top=PD(W_source) -> R_eq=0 -> B_zero_flux=0`. Current MTS has the conditional theorem and contracts, but not the signed parent action/charge package.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Worldtube-Hilbert Selector Theorem",
        markdown_table(data["selector"], ["theorem_id", "clause", "statement", "status", "implication", "missing", "valid_for_claim"]),
        "",
        "## Source Measure Contract Audit",
        markdown_table(data["source_contract"], ["audit_id", "contract", "statement", "status", "effect_if_missing", "valid_for_claim"]),
        "",
        "## Zero Boundary Flux Audit",
        markdown_table(data["boundary"], ["flux_id", "clause", "statement", "status", "risk", "valid_for_claim"]),
        "",
        "## Selector Residual Rows",
        markdown_table(data["residuals"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"]),
        "",
        "## Live Local-GR Binding Status",
        markdown_table(data["live_binding"], ["binding_id", "object", "current_law", "selector_effect", "status", "next_dependency", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["gates"], ["gate_id", "claim", "status", "reason", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)
    data = {
        "sources": source_register_rows(),
        "selector": selector_theorem_rows(),
        "source_contract": source_contract_rows(),
        "boundary": boundary_flux_rows(),
        "residuals": residual_rows(),
        "live_binding": live_binding_rows(),
        "gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }
    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["selector_theorem"], data["selector"])
    write_csv(OUTPUTS["source_contract"], data["source_contract"])
    write_csv(OUTPUTS["boundary_flux"], data["boundary"])
    write_csv(OUTPUTS["residual_rows"], data["residuals"])
    write_csv(OUTPUTS["live_binding"], data["live_binding"])
    write_csv(OUTPUTS["claim_gates"], data["gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])
    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])
    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)
    print(f"wrote {DOC}")
    for key, path in OUTPUTS.items():
        print(f"wrote {key}: {path}")
    for key, path in COPY_TARGETS.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
