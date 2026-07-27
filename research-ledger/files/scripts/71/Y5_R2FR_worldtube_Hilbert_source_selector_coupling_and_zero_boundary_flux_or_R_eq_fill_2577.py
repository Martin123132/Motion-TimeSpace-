from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_WORLDTUBE_HILBERT_SOURCE_SELECTOR_COUPLING_2577"
CHECKPOINT_ID = "2577"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC = ROOT / "2577-Y5-R2FR-worldtube-Hilbert-source-selector-coupling-and-zero-boundary-flux-or-R-eq-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_SOURCE_REGISTER.csv",
    "selector_theorem": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM.csv",
    "boundary_audit": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_BOUNDARY_ZERO_COUPLING_AUDIT.csv",
    "residual_ledger": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_RESIDUAL_INPUT_LEDGER.csv",
    "epsilonm_status": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_EPSILONM_CLOSURE_STATUS.csv",
    "implications": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_NEWTON_GR_IMPLICATIONS.csv",
    "claim_gates": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SOURCE_SELECTOR_COUPLING_2577_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2577_VALIDATION.csv",
}

COPY_TARGETS = {
    "selector_theorem": QUEUE / "JR2577_WORLDTUBE_HILBERT_COUPLING_SELECTOR_THEOREM_NONCLAIM.csv",
    "boundary_audit": QUEUE / "JR2577_BOUNDARY_ZERO_COUPLING_AUDIT_NONCLAIM.csv",
    "residual_ledger": QUEUE / "JR2577_R_EQ_BZERO_ICOMM_DELTAKAPPA_DELTAELLJ_RESIDUAL_LEDGER_NONCLAIM.csv",
    "epsilonm_status": LOCAL_BOUNDS / "EpsilonM_coupling_closure_status_2577_NONCLAIM.csv",
    "next_target": QUEUE / "JR2577_PIM_HAMILTONIAN_COUPLING_IDENTITY_OR_RESIDUAL_FILL_NEXT.csv",
}

SOURCES = [
    {
        "source_id": "SRC2577_00_2576_handoff",
        "source_path": ROOT / "2576-Y5-R2FR-parent-Hcore-QR-source-equation-coupling-owner-or-boundary-charge-owner.md",
        "needles": ["NEXT2576_0_selected", "LAW2576_4_Delta_Newton_v_coupled", "EM2576_5_verdict", "VAL2576_OVERALL"],
        "role": "active handoff adding coupling owner to the worldtube-Hilbert source selector target",
    },
    {
        "source_id": "SRC2577_01_2183_selector",
        "source_path": ROOT / "2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md",
        "needles": ["WST2183_5_R_eq_zero_condition", "BFA2183_4_zero_flux_verdict", "VAL2183_OVERALL"],
        "role": "conditional worldtube-Hilbert selector theorem and zero boundary flux blocker",
    },
    {
        "source_id": "SRC2577_02_2184_action_contract",
        "source_path": ROOT / "2184-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
        "needles": ["MAS2184_4_Hamiltonian_PiM", "NHC2184_4_PiM_identification", "VAL2184_OVERALL"],
        "role": "minimal parent-action/Hamiltonian charge contract and PiM identity blocker",
    },
    {
        "source_id": "SRC2577_03_2182_topological_identity",
        "source_path": ROOT / "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
        "needles": ["TEA2182_0_identity_target", "BZ2182_5_current_verdict", "VAL2182_OVERALL"],
        "role": "topological-Hilbert equality residual definition and B_zero blocker",
    },
    {
        "source_id": "SRC2577_04_2181_commutator",
        "source_path": ROOT / "2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md",
        "needles": ["PCA2181_0_product_rule", "EMD2181_4_total_envelope", "VAL2181_OVERALL"],
        "role": "Pi_M commutator obstruction and epsilon_M no-cancellation envelope",
    },
    {
        "source_id": "SRC2577_05_HWT536_attempt",
        "source_path": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv",
        "needles": ["HWT536_3_Hilbert_to_PiM_charge_map", "HWT536_5_exact_and_reference_terms_zero"],
        "role": "worldtube/Hilbert theorem attempt naming PiM charge map and exact/reference zero conditions",
    },
    {
        "source_id": "SRC2577_06_HWG535_certificate",
        "source_path": OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
        "needles": ["HWG535_3_exact_term_zero", "missing_certificate_or_bound"],
        "role": "certificate ledger for exact-term, commutator, and projector-stress blockers",
    },
    {
        "source_id": "SRC2577_07_PAC537_contract",
        "source_path": OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv",
        "needles": ["PAC537_5_Hilbert_topological_charge_equality", "PAC537_6_reference_and_boundary_zero"],
        "role": "parent-action clauses needed to own Hilbert/topological equality and boundary reference",
    },
    {
        "source_id": "SRC2577_08_HSM541_measure",
        "source_path": OUT / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "needles": ["HSM541_0_adopt_Hamiltonian_PiM", "HSM541_6_constant_universal_G"],
        "role": "Hamiltonian mass map and constant universal coupling contract",
    },
    {
        "source_id": "SRC2577_09_T510_worldtube_measure",
        "source_path": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "needles": ["T510_2_MTS_transfer_condition", "premises_open"],
        "role": "GR-style worldtube source measure and MTS transfer condition",
    },
    {
        "source_id": "SRC2577_10_2576_validation",
        "source_path": OUT / "P8_Y5_BRR545_2576_VALIDATION.csv",
        "needles": ["VAL2576_OVERALL", "PASS"],
        "role": "previous checkpoint validation",
    },
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {"timestamp_utc": now(), "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID, **row}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), ""
    except Exception as error:
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
                }
            )
        )
    return rows


def selector_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "WSC2577_0_parent_action_current",
            "premise": "covariant parent action owns the observed source current",
            "mathematical_form": "S_parent[e_obs,psi_m,X,kappa_MTS,ell_J,B_ref] with J_H[tau]=delta S_matter/delta e_obs contracted with tau",
            "derivation_status": "CONDITIONAL_CONTRACT_NOT_FULL_PARENT_ACTION",
            "closes_if_signed": "source current is selected before exterior readout",
            "current_blocker": "explicit MTS parent Lagrangian and variation are still not supplied",
            "coupling_clause": "kappa_MTS and ell_J must be action parameters, not fitted readout constants",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WSC2577_1_worldtube_selector",
            "premise": "source support is fixed before readout",
            "mathematical_form": "W_source := supp(J_H[e_obs,tau]); linked surfaces S1,S2 enclose the same W_source and bound a compact source-free annulus A",
            "derivation_status": "EXACT_SELECTOR_DEFINITION_CONDITIONAL",
            "closes_if_signed": "prevents choosing the mass domain after seeing orbital or PPN residuals",
            "current_blocker": "depends on parent-owned J_H and same observed source frame",
            "coupling_clause": "ell_J fixes the source-current normalization before W_source is selected",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WSC2577_2_Hamiltonian_PiM_identity",
            "premise": "Pi_M is the Hamiltonian mass-charge map",
            "mathematical_form": "(4*pi*G_ref)^-1 integral_S Pi_M J_H = H_tau[S] - H_tau[reference]",
            "derivation_status": "CORE_IDENTITY_NOT_DERIVED_CURRENT_CORPUS",
            "closes_if_signed": "Pi_M J_H becomes measured dressed source mass, not a conserved wrong object",
            "current_blocker": "Pi_M/Hamiltonian identity remains adopted as a contract rather than proved from MTS action",
            "coupling_clause": "G_ref/kappa_MTS must be the same fixed coefficient used by the v source equation",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WSC2577_3_same_topological_class",
            "premise": "topological representative is the same Hilbert worldtube class",
            "mathematical_form": "J_M_top := M_source[W] omega_W with d omega_W=0 and integral_link omega_W=1 for the same W_source",
            "derivation_status": "EXACT_CONDITIONAL_PD_MAP",
            "closes_if_signed": "topological charge is tied to the measured source class",
            "current_blocker": "same-class parent signature and no independent topological source label are unsigned",
            "coupling_clause": "M_source[W] must use the same ell_J-normalized Hilbert charge",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WSC2577_4_R_eq_zero_lemma",
            "premise": "same Hilbert/topological source class with fixed PiM",
            "mathematical_form": "Pi_M J_H - J_M_top = dB_zero, hence R_eq=0 in the compact support class",
            "derivation_status": "EXACT_CONDITIONAL_R_EQ_ZERO",
            "closes_if_signed": "removes the R_eq source mismatch from epsilon_M",
            "current_blocker": "requires WSC2577_2 and WSC2577_3; neither is parent-signed for MTS",
            "coupling_clause": "R_eq=0 must be true before coupling/readout normalization, not after calibration",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WSC2577_5_I_commutator_zero",
            "premise": "Pi_M is a fixed chain map on the exterior Hilbert current space",
            "mathematical_form": "[d,Pi_M]J_H=0 and projector-stress terms vanish or are bounded below local locks",
            "derivation_status": "EXACT_CONDITIONAL_COMMUTATOR_ZERO",
            "closes_if_signed": "removes radial measured-mass drift from epsilon_M",
            "current_blocker": "Pi_M covariance and projector-stress silence are not certified",
            "coupling_clause": "Pi_M cannot depend on kappa_MTS, ell_J, source class, or readout frame in a tunable way",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WSC2577_6_coupling_baseline_zero",
            "premise": "local coupling/source-current baseline is parent fixed",
            "mathematical_form": "Dln(kappa_MTS)=0 and Dln(ell_J)=0 on the local exterior comparison branch",
            "derivation_status": "COUPLING_BASELINE_NOT_DERIVED_CURRENT_CORPUS",
            "closes_if_signed": "removes delta_kappa and delta_ellJ from Delta_Newton_v_coupled",
            "current_blocker": "constant universal G/source-current scale contract is named but not parent-derived",
            "coupling_clause": "this is the coupling gate itself",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "WSC2577_7_current_verdict",
            "premise": "worldtube-Hilbert source selector with coupling closure for current MTS",
            "mathematical_form": "W_source + Pi_M^H + J_M_top + B_zero + fixed kappa_MTS/ell_J -> R_eq=I_commutator=B_zero_flux=delta_kappa=delta_ellJ=0",
            "derivation_status": "SELECTOR_COUPLING_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS",
            "closes_if_signed": "would close epsilon_M and reopen Newton/local-GR derivation route",
            "current_blocker": "PiM/Hamiltonian identity, fixed boundary reference, projector stress, extra sectors, and coupling baseline remain unsigned",
            "coupling_clause": "no hidden fitted-GM or source-scale absorption is allowed",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def boundary_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "BZA2577_0_reference_fixed_once",
            "boundary_clause": "fixed reference",
            "statement": "H_tau[reference] and B_zero reference are selected once by the parent action/local boundary condition",
            "status": "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "coupling_risk": "a moving reference is fitted GM/source-current normalization in disguise",
            "residual_if_missing": "B_zero_flux",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BZA2577_1_outer_flux_zero",
            "boundary_clause": "no outer compact leak",
            "statement": "no dB_zero, symplectic, nonEH, projector, or coupling flux exits the compact local exterior boundary",
            "status": "MISSING_OUTER_FLUX_ZERO",
            "coupling_risk": "outer leakage can look like a radius-dependent gravitational coupling",
            "residual_if_missing": "B_zero_flux;delta_kappa",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BZA2577_2_inner_flux_zero",
            "boundary_clause": "no inner/excision leak",
            "statement": "no hidden flux enters through source-hole, ring, regularization, or internal support boundaries",
            "status": "MISSING_INNER_FLUX_ZERO",
            "coupling_risk": "inner hair can masquerade as dressed source mass or ell_J shift",
            "residual_if_missing": "B_zero_flux;delta_ellJ",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BZA2577_3_projector_stress_zero",
            "boundary_clause": "no projector-stress term",
            "statement": "delta_g Pi_M and boundary variation of Pi_M vanish or have a source-backed bound",
            "status": "MISSING_PROJECTOR_STRESS_ZERO_OR_BOUND",
            "coupling_risk": "projector stress can fail PPN even with a closed monopole charge",
            "residual_if_missing": "I_commutator_or_projector_stress",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BZA2577_4_coupling_reference_silence",
            "boundary_clause": "no coupling boundary counterterm",
            "statement": "boundary/reference terms do not absorb Dln(kappa_MTS), Dln(ell_J), or source-frame shifts",
            "status": "MISSING_COUPLING_REFERENCE_SILENCE",
            "coupling_risk": "a boundary counterterm could produce an artificial local-GR pass",
            "residual_if_missing": "delta_kappa;delta_ellJ;epsilon_calibration",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BZA2577_5_zero_flux_verdict",
            "boundary_clause": "zero boundary flux with coupling",
            "statement": "current sources do not certify B_zero_flux=0 with fixed reference, no compact leaks, projector-stress silence, and coupling-reference silence",
            "status": "ZERO_BOUNDARY_FLUX_WITH_COUPLING_NOT_DERIVED",
            "coupling_risk": "boundary and coupling remain linked blockers",
            "residual_if_missing": "B_zero_flux;delta_kappa;delta_ellJ",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def residual_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "residual_id": "SRR2577_0_W_selector",
            "residual": "epsilon_W_selector",
            "definition": "dimensionless charge/domain shift from parent source worldtube selection W_source=supp(J_H[e_obs,tau])",
            "status": "MISSING_PARENT_WORLDTUBE_SELECTOR",
            "units": "dimensionless",
            "arenas": "Newton;PPN;WEP;orbital",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "SRR2577_1_PiM_Hamiltonian",
            "residual": "epsilon_PiM_Hamiltonian",
            "definition": "failure of Pi_M J_H to equal the Hamiltonian dressed mass-charge form",
            "status": "MISSING_PIM_HAMILTONIAN_IDENTITY",
            "units": "dimensionless_or_GM_flux",
            "arenas": "Newton;PPN;R10;R11",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "SRR2577_2_R_eq",
            "residual": "R_eq_integral",
            "definition": "compact support equality residual Pi_M J_H-J_M_top-dB_zero after W_source selection",
            "status": "MISSING_R_EQ_ZERO_OR_VALUE",
            "units": "dimensionless_after_M_H_ref_normalization",
            "arenas": "Newton;PPN;R10;R11",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "SRR2577_3_B_zero",
            "residual": "B_zero_flux",
            "definition": "compact boundary flux of dB_zero/reference/symplectic/coupling improvement",
            "status": "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE",
            "units": "GM_flux_or_dimensionless_after_M_H_ref_normalization",
            "arenas": "Newton;PPN;R7;R8;R9;R11",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "SRR2577_4_I_commutator",
            "residual": "I_commutator_or_projector_stress",
            "definition": "finite annulus integral of [d,Pi_M]J_H plus projector-stress boundary variation",
            "status": "MISSING_PIM_CHAIN_MAP_ZERO_OR_BOUND",
            "units": "GM_flux_or_PPN_equivalent",
            "arenas": "Newton;PPN;R10;R11",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "SRR2577_5_delta_kappa",
            "residual": "delta_kappa",
            "definition": "Dln(kappa_MTS) or equivalent gravitational coupling mismatch on the local exterior branch",
            "status": "MISSING_PARENT_CONSTANT_KAPPA_PROOF_OR_VALUE",
            "units": "dimensionless",
            "arenas": "Newton;PPN;clock;orbital;R10",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "SRR2577_6_delta_ellJ",
            "residual": "delta_ellJ",
            "definition": "Dln(ell_J) or equivalent source-current scale mismatch between Hilbert source and v source equation",
            "status": "MISSING_PARENT_CONSTANT_ELLJ_PROOF_OR_VALUE",
            "units": "dimensionless",
            "arenas": "Newton;PPN;WEP;orbital;R10",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "SRR2577_7_extra_channels",
            "residual": "epsilon_extra_source_charge",
            "definition": "nonEH, memory, motion, time, range, frame, symplectic-boundary, and projector source-charge channels",
            "status": "MISSING_EXTRA_SECTOR_ZERO_OR_BOUND",
            "units": "dimensionless_or_GM_flux",
            "arenas": "Newton;PPN;WEP;clock;orbital",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "SRR2577_8_total",
            "residual": "epsilon_M_abs_2577",
            "definition": "absolute no-cancellation sum of selector, PiM, R_eq, B_zero, commutator, coupling, extra, and calibration residuals",
            "status": "MISSING_COMPONENT_INPUTS",
            "units": "dimensionless",
            "arenas": "Newton;local-GR;R10;R11",
            "numeric_value": "MISSING_NUMERIC_VALUE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def epsilonm_status_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "status_id": "EPS2577_0_identity",
            "object": "source equality identity",
            "statement": "Pi_M J_H = J_M_top + dB_zero + R_eq",
            "status": "EXACT_IDENTITY_DEFINITION",
            "claim_effect": "defines the residuals; does not zero them",
            "valid_for_claim": False,
        },
        {
            "status_id": "EPS2577_1_zero_conditions",
            "object": "epsilon_M zero theorem",
            "statement": "epsilon_M=0 if W_selector, PiM_Hamiltonian, R_eq, B_zero_flux, I_commutator, delta_kappa, delta_ellJ, extra sectors, and calibration residuals all vanish in the same frame",
            "status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "claim_effect": "conditional route exists but current premises are unsigned",
            "valid_for_claim": False,
        },
        {
            "status_id": "EPS2577_2_absolute_envelope",
            "object": "no-cancellation envelope",
            "statement": "abs(epsilon_M) <= abs(epsilon_W_selector)+abs(epsilon_PiM_Hamiltonian)+abs(R_eq_integral)+abs(B_zero_flux)+abs(I_commutator)+abs(delta_kappa)+abs(delta_ellJ)+abs(epsilon_extra)+abs(epsilon_calibration)",
            "status": "EXACT_ABSOLUTE_LEDGER",
            "claim_effect": "prevents cancelling an unsigned source mismatch against a coupling mismatch",
            "valid_for_claim": False,
        },
        {
            "status_id": "EPS2577_3_current_verdict",
            "object": "epsilon_M with coupling",
            "statement": "current corpus has no parent-signed package proving the selector, PiM identity, boundary zero, commutator zero, and coupling baseline together",
            "status": "EPSILONM_COUPLING_CLOSURE_NOT_DERIVED",
            "claim_effect": "Newton/local-GR remains blocked; residual ledger is the honest fallback",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def implication_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "implication_id": "IMP2577_0_Newton_source",
            "premise_package": "epsilon_M=0 plus delta_KC=0, delta_kappa=0, delta_ellJ=0",
            "implication": "Delta_Newton_v_coupled=0 for the constrained v branch",
            "current_status": "BLOCKED_CONDITIONAL",
            "missing_piece": "PiM/Hamiltonian identity, boundary zero, and coupling baseline",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2577_1_beta",
            "premise_package": "pure linear exterior v branch and kappa_v=0 with no source/coupling/readout second-order tails",
            "implication": "beta=1 in the constrained v-readout branch",
            "current_status": "BLOCKED_CONDITIONAL",
            "missing_piece": "second-order source/coupling stability remains unsigned",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2577_2_local_GR",
            "premise_package": "u=0/Q_R=0, v=-2U/c^2, epsilon_M=0, delta_KC=0, delta_kappa=0, delta_ellJ=0, kappa_v=0, and full PPN vector silence",
            "implication": "local GR recovery would be derivable rather than postulated",
            "current_status": "NOT_CLAIMED",
            "missing_piece": "multiple parent signatures remain open",
            "valid_for_claim": False,
        },
        {
            "implication_id": "IMP2577_3_empirical_fallback",
            "premise_package": "source-backed finite rows for R_eq, B_zero_flux, I_commutator, delta_kappa, and delta_ellJ",
            "implication": "local branch can be tested as a bounded residual vector even if zero proof fails",
            "current_status": "FALLBACK_READY_NOT_POPULATED",
            "missing_piece": "real numeric source-backed rows",
            "valid_for_claim": False,
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GATE2577_0_internal_progress",
            "claim": "worldtube-Hilbert source selector with coupling has a precise conditional theorem and residual ledger",
            "gate_status": "PASS_INTERNAL_PROGRESS",
            "reason": "2577 combines same-source topology, Hamiltonian mass map, boundary zero, and coupling baseline in one gate",
            "gate_pass": True,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2577_1_selector",
            "claim": "parent worldtube selector is derived for current MTS",
            "gate_status": "BLOCKED",
            "reason": "J_H and W_source depend on an explicit parent action/source frame not yet derived",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2577_2_PiM_Hamiltonian",
            "claim": "Pi_M is proved to be the Hamiltonian mass map",
            "gate_status": "BLOCKED",
            "reason": "core PiM/Hamiltonian identity remains unsigned",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2577_3_R_eq_zero",
            "claim": "R_eq=0 is derived for current MTS",
            "gate_status": "BLOCKED",
            "reason": "same-object selector and PiM identity are conditional only",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2577_4_B_zero_flux_zero",
            "claim": "B_zero_flux=0 is derived with coupling silence",
            "gate_status": "BLOCKED",
            "reason": "fixed reference, leak zero, projector stress, and coupling-reference silence are missing",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2577_5_coupling_baseline",
            "claim": "delta_kappa=delta_ellJ=0 is derived",
            "gate_status": "BLOCKED",
            "reason": "constant universal coupling/source-current scale is a contract, not a proof",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2577_6_Newton_local_GR",
            "claim": "Newton or local GR is derived",
            "gate_status": "BLOCKED",
            "reason": "epsilon_M and coupling closure remain unproved; beta/full PPN vector remains separate",
            "gate_pass": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE2577_7_no_shortcuts",
            "claim": "closed wrong topological current, post-readout worldtube, fitted reference, fitted GM, or coupling cancellation can be used as evidence",
            "gate_status": "PASS_GUARDRAIL",
            "reason": "all shortcuts are explicitly demoted to nonclaim residuals",
            "gate_pass": True,
            "claim_allowed": False,
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2577_0_gain",
            "decision": "CONDITIONAL_SELECTOR_COUPLING_THEOREM_WRITTEN",
            "reason": "the worldtube selector, Hamiltonian PiM identity, topological representative, boundary zero, and coupling baseline are now one closure package",
            "effect": "we know exactly what must be parent-signed for epsilon_M=0",
        },
        {
            "decision_id": "DEC2577_1_claim_status",
            "decision": "CURRENT_MTS_CLAIM_FAILS_NONCLAIM",
            "reason": "PiM/Hamiltonian identity, fixed reference, zero boundary flux, projector stress silence, extra sectors, and coupling baseline are unsigned",
            "effect": "no Newton/local-GR claim",
        },
        {
            "decision_id": "DEC2577_2_fallback",
            "decision": "FINITE_RESIDUAL_ROWS_RETAINED",
            "reason": "if zero proof fails, R_eq, B_zero_flux, I_commutator, delta_kappa, and delta_ellJ must become source-backed inputs",
            "effect": "residual rows are staged with valid_for_claim=false",
        },
        {
            "decision_id": "DEC2577_3_next",
            "decision": "PIM_HAMILTONIAN_COUPLING_IDENTITY_SELECTED_NEXT",
            "reason": "the cleanest leap is to prove or reject Pi_M as the Hamiltonian mass map while carrying kappa_MTS/ell_J in the same identity",
            "effect": "2578 should attack the identity directly or start source-backed residual acquisition",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2577_0_selected",
            "selection_status": "selected",
            "target_file": "2578-Y5-R2FR-PiM-Hamiltonian-coupling-identity-or-source-backed-residual-fill.md",
            "target_script": "scripts/Y5_R2FR_PiM_Hamiltonian_coupling_identity_or_source_backed_residual_fill_2578.py",
            "task": "prove or reject that Pi_M J_H is the parent Hamiltonian mass-charge map with fixed kappa_MTS and ell_J on the local exterior branch; if not proved, populate source-ready residual rows for epsilon_PiM_Hamiltonian, R_eq, B_zero_flux, I_commutator, delta_kappa, and delta_ellJ",
            "acceptance_target": "PiM/Hamiltonian/coupling identity is parent-signed, or all failure modes are explicit nonclaim finite residual inputs",
            "guardrails": "no GitHub; no formalization-workbench edits; no fitted GM/H0; no closed-wrong-object promotion; no cancellation credit; no local-GR claim",
        }
    ]
    return [stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_map = {
        "selector_theorem": OUTPUTS["selector_theorem"],
        "boundary_audit": OUTPUTS["boundary_audit"],
        "residual_ledger": OUTPUTS["residual_ledger"],
        "epsilonm_status": OUTPUTS["epsilonm_status"],
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
                    "copy_id": f"COPY2577_{key}",
                    "source_path": str(source),
                    "target_path": str(target),
                    "source_exists": source.exists(),
                    "target_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, notes: str, detail: str = "") -> None:
        rows.append(stamp({"check_id": check_id, "status": "PASS" if passed else "FAIL", "notes": notes, "detail": detail}))

    add("VAL2577_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and required needles are present")
    add(
        "VAL2577_01_selector_verdict_nonclaim",
        any(row["theorem_id"] == "WSC2577_7_current_verdict" and row["derivation_status"] == "SELECTOR_COUPLING_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS" for row in data["selector_theorem"]),
        "selector coupling theorem remains conditional and nonclaim",
    )
    add(
        "VAL2577_02_PiM_identity_blocker",
        any(row["theorem_id"] == "WSC2577_2_Hamiltonian_PiM_identity" and row["derivation_status"] == "CORE_IDENTITY_NOT_DERIVED_CURRENT_CORPUS" for row in data["selector_theorem"]),
        "PiM/Hamiltonian identity is named as the core blocker",
    )
    add(
        "VAL2577_03_R_eq_conditional_only",
        any(row["theorem_id"] == "WSC2577_4_R_eq_zero_lemma" and row["derivation_status"] == "EXACT_CONDITIONAL_R_EQ_ZERO" for row in data["selector_theorem"]),
        "R_eq zero is conditional only",
    )
    add(
        "VAL2577_04_boundary_verdict_blocked",
        any(row["audit_id"] == "BZA2577_5_zero_flux_verdict" and row["status"] == "ZERO_BOUNDARY_FLUX_WITH_COUPLING_NOT_DERIVED" for row in data["boundary_audit"]),
        "B_zero flux with coupling remains blocked",
    )
    required_residuals = {"R_eq_integral", "B_zero_flux", "I_commutator_or_projector_stress", "delta_kappa", "delta_ellJ"}
    actual_residuals = {row["residual"] for row in data["residual_ledger"]}
    add(
        "VAL2577_05_required_residual_rows",
        required_residuals.issubset(actual_residuals) and all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in data["residual_ledger"]),
        "R_eq/B_zero/I_commutator/delta_kappa/delta_ellJ rows exist and remain nonclaim",
    )
    add(
        "VAL2577_06_epsilon_envelope_coupled",
        any(row["status_id"] == "EPS2577_2_absolute_envelope" and "delta_kappa" in row["statement"] and "delta_ellJ" in row["statement"] for row in data["epsilonm_status"]),
        "epsilon_M envelope includes coupling residuals",
    )
    add(
        "VAL2577_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"]),
        "no gate allows Newton/local-GR or source-closure claim",
    )
    add(
        "VAL2577_08_next_target_written",
        any(row["route_id"] == "NEXT2577_0_selected" for row in data["next"]),
        "2578 PiM/Hamiltonian/coupling identity target selected",
    )
    add(
        "VAL2577_09_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in ("*2577*", "*P8_Y5_SOURCE_SELECTOR_COUPLING_2577*", "*JR2577*"):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2577_10_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2577 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2577_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2577_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2577_OVERALL",
        overall,
        "2577 builds the conditional worldtube-Hilbert source selector with coupling, keeps current MTS nonclaim, and selects PiM/Hamiltonian/coupling identity next",
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
            values.append(value.replace("|", "\\|").replace("\n", " "))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2577 Y5 R2FR Worldtube-Hilbert Source Selector Coupling And Zero Boundary Flux Or R_eq Fill",
        "",
        "**Status:** private nonclaim derivation checkpoint. The worldtube-Hilbert source-selector theorem becomes sharper when coupling ownership is included, but current MTS still lacks the parent-signed PiM/Hamiltonian identity, fixed boundary reference, zero compact flux, projector-stress silence, extra-sector silence, and fixed `kappa_MTS`/`ell_J` baseline.",
        "",
        "**Main result:** if the parent action owns `J_H`, `W_source`, `Pi_M` as the Hamiltonian mass map, `J_M_top=PD(W_source)`, `B_zero` with zero compact flux, and constant same-frame `kappa_MTS`/`ell_J`, then `R_eq=0`, `I_commutator=0`, `B_zero_flux=0`, `delta_kappa=0`, `delta_ellJ=0`, hence the `epsilon_M` source-closure branch can close. Current corpus does not prove that package, so these are staged as explicit nonclaim residuals rather than hidden calibration knobs.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role"]),
        "",
        "## Worldtube-Hilbert Coupling Selector Theorem",
        markdown_table(data["selector_theorem"], ["theorem_id", "premise", "mathematical_form", "derivation_status", "closes_if_signed", "current_blocker", "coupling_clause", "valid_for_claim"]),
        "",
        "## Boundary Zero Coupling Audit",
        markdown_table(data["boundary_audit"], ["audit_id", "boundary_clause", "statement", "status", "coupling_risk", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Residual Input Ledger",
        markdown_table(data["residual_ledger"], ["residual_id", "residual", "definition", "status", "units", "arenas", "numeric_value", "source_path", "valid_for_claim", "claim_allowed"]),
        "",
        "## EpsilonM Closure Status",
        markdown_table(data["epsilonm_status"], ["status_id", "object", "statement", "status", "claim_effect", "valid_for_claim"]),
        "",
        "## Newton / GR Implications",
        markdown_table(data["implications"], ["implication_id", "premise_package", "implication", "current_status", "missing_piece", "valid_for_claim"]),
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

    data = {
        "sources": source_register_rows(),
        "selector_theorem": selector_theorem_rows(),
        "boundary_audit": boundary_audit_rows(),
        "residual_ledger": residual_ledger_rows(),
        "epsilonm_status": epsilonm_status_rows(),
        "implications": implication_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["selector_theorem"], data["selector_theorem"])
    write_csv(OUTPUTS["boundary_audit"], data["boundary_audit"])
    write_csv(OUTPUTS["residual_ledger"], data["residual_ledger"])
    write_csv(OUTPUTS["epsilonm_status"], data["epsilonm_status"])
    write_csv(OUTPUTS["implications"], data["implications"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2577_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
