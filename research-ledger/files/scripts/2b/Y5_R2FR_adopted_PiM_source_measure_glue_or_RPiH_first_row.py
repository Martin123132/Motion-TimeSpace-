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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1778"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1778_0_1777_handoff",
        "source_key": "1777_handoff",
        "source_path": ROOT / "1777-Y5-R2FR-Hamiltonian-PiM-adoption-contract-or-RPiH-bound.md",
        "needles": ["NEXT1777_0_primary", "HPA1777_1_charge_functional", "RPH1777_0_R_PiH"],
    },
    {
        "source_id": "SRC1778_1_1777_validation",
        "source_key": "1777_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1777_VALIDATION.csv",
        "needles": ["VAL1777_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1778_2_1777_adoption_contract",
        "source_key": "1777_adoption_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_HAMILTONIAN_PIM_ADOPTION_CONTRACT.csv",
        "needles": ["HPA1777_1_charge_functional", "HPA1777_5_verdict"],
    },
    {
        "source_id": "SRC1778_3_1777_rpih_bound_pack",
        "source_key": "1777_rpih_bound_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1777_RPIH_BOUND_PACK.csv",
        "needles": ["RPH1777_0_R_PiH", "RPH1777_1_B_H_flux", "RPH1777_4_total_abs"],
    },
    {
        "source_id": "SRC1778_4_541_source_measure_contract",
        "source_key": "541_source_measure_contract",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "needles": ["HSM541_2_observed_worldtube_source", "HSM541_5_Gauss_orbital_readout"],
    },
    {
        "source_id": "SRC1778_5_542_conditional_theorem",
        "source_key": "542_conditional_theorem",
        "source_path": ROOT / "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md",
        "needles": ["SMT542_2_observed_worldtube_source", "SMT542_3_radial_closure"],
    },
    {
        "source_id": "SRC1778_6_554_source_equality",
        "source_key": "554_source_equality",
        "source_path": ROOT / "554-Y5-Hamiltonian-charge-integrability-reference-lock-or-source-equality-fill.md",
        "needles": ["HSE554_4_Hilbert_current_equality", "FB554_1_HPiM_source_equality_bound"],
    },
    {
        "source_id": "SRC1778_7_510_worldtube_theorem",
        "source_key": "510_worldtube_theorem",
        "source_path": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
        "needles": ["T510_1_worldtube_source_measure", "T510_2_MTS_transfer_condition"],
    },
    {
        "source_id": "SRC1778_8_510_worldtube_clauses",
        "source_key": "510_worldtube_clauses",
        "source_path": RESIDUALS / "P8_WORLDTUBE_SOURCE_MEASURE_CLAUSES.csv",
        "needles": ["WG510_1_minimal_observed_matter_coupling", "WG510_5_projector_ownership"],
    },
    {
        "source_id": "SRC1778_9_992_descent_gate",
        "source_key": "992_descent_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_992_SOURCE_CURRENT_DESCENT_THEOREM_GATE.csv",
        "needles": ["SCD992_2_Hilbert_current_definition", "SCD992_4_charge_current_equality"],
    },
    {
        "source_id": "SRC1778_10_992_bound_pack",
        "source_key": "992_bound_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_992_COMPONENT_BOUND_PACK.csv",
        "needles": ["BPK992_1_PiM_chain_map", "BPK992_2_charge_current_residuals"],
    },
    {
        "source_id": "SRC1778_11_458_gauss_contract",
        "source_key": "458_gauss_contract",
        "source_path": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "needles": ["PG1_charge_equals_projected_Hilbert_source", "PG4_Gauss_surface_integral"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_SOURCE_REGISTER.csv",
    "source_measure_lemma": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_ADOPTED_PIM_SOURCE_MEASURE_LEMMA.csv",
    "proof_clause_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_PROOF_CLAUSE_AUDIT.csv",
    "worldtube_current_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_WORLDTUBE_CURRENT_MAP.csv",
    "strict_residual_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_STRICT_RESIDUAL_ROWS.csv",
    "rpih_bh_first_row_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_RPIH_BH_FIRST_ROW_SCHEMA.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1778_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1778_VALIDATION.csv",
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
                "role": "1778 adopted-PiM source-measure glue and R_PiH/B_H first-row evidence",
            }
        )
    return rows


def source_measure_lemma_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "ASM1778_0_conditional_theorem",
            "claim": "adopted Hamiltonian Pi_M^H reads the observed dressed worldtube source",
            "mathematical_form": "M_H[W;S]=G_ref^-1 int_S Q_tau^MTS-H_ref = M_eff[Pi_M^H J_H^dress]",
            "status": "CONDITIONAL_LEMMA_SHAPE_DERIVED",
            "proof_content": "follows by covariant phase-space Stokes theorem if parent current, integrability, same observed source functor, chain map, boundary flux, and exterior C-term silence all hold",
            "missing_for_claim": "clauses PCA1778_0 through PCA1778_6 must be signed in one parent action",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "ASM1778_1_not_bare_matter",
            "claim": "the source measure is not bare rest mass",
            "mathematical_form": "J_H^dress = J_H^matter plus parent-owned binding/boundary/constraint dressing; M_bare != M_H by default",
            "status": "GUARDRAIL_RETAINED",
            "proof_content": "matches the GR-style worldtube theorem: exterior mass is a dressed Hamiltonian/Noether charge",
            "missing_for_claim": "explicit dressing map from parent action, not a post-readout definition",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "ASM1778_2_exact_residual_identity",
            "claim": "failed equality becomes a named residual rather than a hidden calibration",
            "mathematical_form": "Delta_Hsrc := G_ref^-1 int_S Q_tau^MTS-H_ref-M_eff[Pi_M^H J_H^dress]",
            "status": "RESIDUAL_IDENTITY_STAGED",
            "proof_content": "all unproved terms are retained as absolute no-cancellation residual rows",
            "missing_for_claim": "theorem-zero or sourced finite bounds for each component of Delta_Hsrc",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "ASM1778_3_old_pim_guardrail",
            "claim": "old/topological Pi_M cannot supply the source measure unless equivalent to Pi_M^H",
            "mathematical_form": "Pi_M^top J_H = Pi_M^H J_H + dB_H + R_PiH",
            "status": "RPIH_GUARDRAIL_RETAINED",
            "proof_content": "prevents topological conservation of a wrong object from becoming measured mass",
            "missing_for_claim": "R_PiH zero theorem or source-backed bound plus B_H flux convention",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "ASM1778_4_gauss_downstream",
            "claim": "source-measure equality is upstream of Poisson/Gauss/orbital readout",
            "mathematical_form": "M_orbit=G_ref M_H only after PG1-PG8 pass; orbital GM cannot prove Delta_Hsrc=0",
            "status": "NO_CIRCULAR_DENOMINATOR_POLICY",
            "proof_content": "Gauss and orbital calibration remain downstream checks, not evidence for the source equality itself",
            "missing_for_claim": "Poisson coefficient, Gauss surface integral, inverse-square readout, constant G, and PPN followthrough",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lemma_id": "ASM1778_5_verdict",
            "claim": "current MTS proves the adopted-PiM source-measure lemma",
            "mathematical_form": "ASM1778_0 clauses all signed, Delta_Hsrc=0, R_PiH=0, int dB_H=0",
            "status": "FAIL_CURRENT_PARENT_PROOF",
            "proof_content": "conditional theorem shape exists, but the parent current/source functor/chain-map/boundary rows are not signed",
            "missing_for_claim": "parent extraction or first strict component row with source path and units",
            "valid_for_claim": False,
        },
    ]


def proof_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1778_0_parent_current",
            "required_clause": "one parent action supplies theta_total, Q_tau, constraints, and boundary policy",
            "mathematical_form": "delta L_parent=E_i delta Phi^i+d theta_total; J_tau=theta_total(L_tau Phi)-i_tau L_parent=dQ_tau+C_tau",
            "current_status": "MISSING_PARENT_CURRENT_EXTRACTION",
            "why_blocks": "without Q_tau/theta ownership, H_tau is not a derived source charge",
            "exit_condition": "sector-by-sector theta_total/Q_tau/constraint table or strict residual row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1778_1_integrable_reference",
            "required_clause": "H_tau is finite, differentiable, integrable, and reference locked",
            "mathematical_form": "delta H_tau=int_S(delta Q_tau-i_tau theta_total), delta^2 H_tau=0, partial_source,r,t,frame B_ref=0",
            "current_status": "MISSING_INTEGRABILITY_REFERENCE_LOCK",
            "why_blocks": "reference subtraction or symplectic flux can masquerade as mass",
            "exit_condition": "curl-zero, B_ref superselection, tau-lock, and zero flux certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1778_2_one_observed_source_functor",
            "required_clause": "matter/source/clocks/readout use the same observed metric or coframe",
            "mathematical_form": "S_matter[psi,g_obs]; J_H[tau]=T_H^{mu nu} tau_nu dSigma_mu; g_readout=g_obs",
            "current_status": "MISSING_ONE_OBSERVED_COFRAME_THEOREM",
            "why_blocks": "source mass and orbital/clock readout can live in different frames",
            "exit_condition": "parent matter functor and no hidden source/readout map",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1778_3_PiM_H_chain_map",
            "required_clause": "Pi_M^H is a parent-owned chain map on the mass channel",
            "mathematical_form": "d(Pi_M^H J_H)=Pi_M^H dJ_H+[d,Pi_M^H]J_H with [d,Pi_M^H]J_H=0 or bounded",
            "current_status": "MISSING_PIMH_CHAIN_MAP",
            "why_blocks": "projected Hilbert mass can drift even if the total current is conserved",
            "exit_condition": "commutator theorem-zero or source-backed Pi_M^H chain-map bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1778_4_boundary_improvement_flux",
            "required_clause": "old/new PiM and Hamiltonian/Hilbert equality have no unowned boundary improvement flux",
            "mathematical_form": "int_boundary dB_H=0 and Pi_M^top J_H-Pi_M^H J_H-dB_H=R_PiH",
            "current_status": "MISSING_BH_FLUX_RULE_AND_RPIH_BOUND",
            "why_blocks": "a boundary bookkeeping term can shift source normalization",
            "exit_condition": "B_H flux theorem-zero or finite row plus R_PiH bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1778_5_dressed_source_map",
            "required_clause": "Hilbert worldtube source is dressed by parent constraints rather than equated to bare matter by assertion",
            "mathematical_form": "J_H^dress=J_H^matter+J_H^binding+J_H^boundary+J_H^constraint with parent-owned components",
            "current_status": "MISSING_DRESSED_SOURCE_MAP",
            "why_blocks": "bare matter equality would be too strong and GR itself would not use it naively",
            "exit_condition": "dressed-source definition from parent variation or explicit residual vector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1778_6_exterior_Cterm_silence",
            "required_clause": "compact exterior annulus carries no extra mass-source C terms",
            "mathematical_form": "int_A(C_EH+C_extra+C_projector+C_boundary+C_ref)=0",
            "current_status": "MISSING_EXTERIOR_CTERM_SILENCE",
            "why_blocks": "radial mass closure fails if extra/projector/boundary channels survive",
            "exit_condition": "field-specific C-term zero theorem or source-backed no-cancellation bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PCA1778_7_Poisson_Gauss_downstream",
            "required_clause": "Poisson/Gauss/orbital readout is derived only after source equality",
            "mathematical_form": "nabla^2 Phi=4*pi*G_ref rho_H and a_r=-G_ref M_H/r^2 after Delta_Hsrc=0",
            "current_status": "DOWNSTREAM_NOT_REACHED",
            "why_blocks": "using fitted orbital GM upstream would be circular",
            "exit_condition": "PG1-PG9 after source-measure glue passes",
            "valid_for_claim": False,
        },
    ]


def worldtube_current_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "WCM1778_0_object_inventory",
            "object": "Q_tau^MTS; H_tau; Pi_M^H; J_H^dress",
            "desired_relation": "one parent source-measure chain from Noether charge to projected observed Hilbert source",
            "current_status": "OBJECTS_NAMED_NOT_CHAINED",
            "failure_if_missing": "source-measure language remains definitional rather than derived",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "WCM1778_1_chain_identity",
            "object": "Hamiltonian charge to projected source current",
            "desired_relation": "G_ref^-1 Q_tau^MTS = Pi_M^H J_H^dress + dB_H + R_Hsrc",
            "current_status": "MISSING_CHAIN_IDENTITY",
            "failure_if_missing": "Delta_Hsrc survives as a source-normalization residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "WCM1778_2_worldtube_surface_equality",
            "object": "inner worldtube W and outer linking surface S",
            "desired_relation": "M_source[W]=G_ref^-1 int_S Q_tau^MTS-H_ref=M_eff[Pi_M^H J_H^dress]",
            "current_status": "CONDITIONAL_ONLY",
            "failure_if_missing": "closed exterior charge need not be the observed source monopole",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "WCM1778_3_old_topological_channel",
            "object": "Pi_M^top versus Pi_M^H",
            "desired_relation": "Pi_M^top is either equivalent to Pi_M^H up to zero-flux exact terms or is not used for measured mass",
            "current_status": "DEMOTED_UNLESS_EQUIVALENT",
            "failure_if_missing": "topological conservation can conserve the wrong mass object",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "WCM1778_4_gauss_readout_dependency",
            "object": "Poisson/Gauss/orbital GM",
            "desired_relation": "M_Gauss=M_source only after source equality, constant G, same-frame weak-field operator, and no residual source terms",
            "current_status": "DOWNSTREAM_BLOCKED",
            "failure_if_missing": "orbital data would be smuggled in as the source definition",
            "valid_for_claim": False,
        },
    ]


def strict_residual_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DHS1778_0_Delta_Hsrc",
            "quantity": "Delta_Hsrc_adopted_source_measure",
            "definition": "G_ref^-1 int_S Q_tau^MTS-H_ref-M_eff[Pi_M^H J_H^dress]",
            "required_fields": "system_id;surface_id;worldtube_id;Q_tau;H_ref;PiM_H_JH_dress;G_ref;units;source_path;equation_ref",
            "status": "MISSING_PARENT_CHAIN_IDENTITY",
            "bound_rule": "absolute value only; no cancellation between current, frame, boundary, and calibration terms",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DHS1778_1_Delta_frame_source",
            "quantity": "Delta_frame_source_readout",
            "definition": "difference between source coframe/metric and clock/orbital readout coframe before fitting",
            "required_fields": "system_id;source_frame;readout_frame;coframe_map;Delta_frame;units;source_path;lock_row",
            "status": "MISSING_ONE_OBSERVED_COFRAME_THEOREM",
            "bound_rule": "same-frame theorem-zero or finite source/readout frame residual",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DHS1778_2_Delta_dress",
            "quantity": "Delta_dressed_source_map",
            "definition": "J_H^dress-J_H^matter contribution from binding/boundary/constraint/source dressing",
            "required_fields": "system_id;matter_current;binding_term;boundary_term;constraint_term;units;source_path;derivation_status",
            "status": "MISSING_DRESSED_SOURCE_COMPONENTS",
            "bound_rule": "derive dressing from parent variation or carry every component as a residual",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DHS1778_3_Delta_Cext",
            "quantity": "Delta_Cext_annulus",
            "definition": "int_A(C_extra+C_projector+C_boundary+C_ref) in the compact source-free exterior",
            "required_fields": "system_id;annulus_id;C_extra;C_projector;C_boundary;C_ref;surface_pair;units;source_path",
            "status": "MISSING_EXTERIOR_CTERM_BOUND",
            "bound_rule": "componentwise theorem-zero or finite no-cancellation envelope",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DHS1778_4_total_abs",
            "quantity": "epsilon_Hsrc_total_abs",
            "definition": "abs(Delta_Hsrc)+abs(Delta_frame_source)+abs(Delta_dress)+abs(Delta_Cext)+abs(R_PiH)+abs(B_H_flux)",
            "required_fields": "component_rows;normalizer_MH;component_source_paths;no_cancellation_flag;units",
            "status": "MISSING_COMPONENT_INPUTS",
            "bound_rule": "cannot be scored until every component is theorem-zero or source-backed",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def rpih_bh_first_row_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RBH1778_0_R_PiH_first_row",
            "target_quantity": "R_PiH_equivalence_first_row",
            "formula": "Pi_M^top J_H - Pi_M^H J_H - dB_H",
            "required_columns": "system_id;PiM_top_definition;PiM_H_definition;J_H_dress_definition;B_H_definition;R_PiH_value;units;source_path;equation_ref;valid_for_claim",
            "current_status": "SCHEMA_ONLY_MISSING_SOURCE_VALUE",
            "acceptance_rule": "numeric/source-backed finite value or theorem-zero certificate; no inferred equality from notation",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RBH1778_1_B_H_flux_first_row",
            "target_quantity": "B_H_boundary_improvement_flux_first_row",
            "formula": "int_boundary dB_H over the chosen inner/outer surface pair",
            "required_columns": "system_id;surface_pair;boundary_rule;B_H_definition;B_H_flux_value;units;source_path;equation_ref;valid_for_claim",
            "current_status": "SCHEMA_ONLY_MISSING_BOUNDARY_RULE",
            "acceptance_rule": "zero-flux theorem for the selected boundary class or source-backed finite flux row",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RBH1778_2_Delta_Hsrc_first_row",
            "target_quantity": "Delta_Hsrc_first_row",
            "formula": "G_ref^-1 int_S Q_tau^MTS-H_ref-M_eff[Pi_M^H J_H^dress]",
            "required_columns": "system_id;worldtube_id;surface_id;Q_tau_source;H_ref_source;PiM_H_JH_source;Delta_Hsrc_value;units;source_path;equation_ref;valid_for_claim",
            "current_status": "SCHEMA_ONLY_MISSING_PARENT_CHAIN_VALUE",
            "acceptance_rule": "first row is allowed for bookkeeping only until all component sources exist",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1778_0_source_measure_lemma",
            "claim": "adopted Pi_M^H source-measure lemma is proved for current MTS",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "parent current, same observed source functor, chain map, boundary flux, and exterior C terms are not signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1778_1_RPiH_BH_bound",
            "claim": "old/topological Pi_M is equivalent to Pi_M^H or bounded",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "R_PiH and B_H flux are schema-only with no source-backed values",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1778_2_Newton_Gauss_orbit",
            "claim": "source-normalized Newton/Gauss/orbital reduction follows",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "Gauss/orbital readout is downstream and cannot be used to prove source equality",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1778_3_local_GR_PPN_R10",
            "claim": "local GR, PPN, R10, clock, orbital, or WEP pass follows",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "source-measure, constant G, weak-field operator, and second-order PPN gates remain open",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1778_0_conditional_lemma",
            "decision": "CONDITIONAL_ADOPTED_PIM_SOURCE_MEASURE_LEMMA_WRITTEN",
            "reason": "the GR-shaped source-measure chain is now explicit in Hamiltonian-PiM language",
            "next_action": "do not promote; use it as a theorem contract",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1778_1_current_status",
            "decision": "FAIL_CURRENT_PARENT_PROOF",
            "reason": "the exact chain from Q_tau to Pi_M^H J_H^dress is missing and old PiM equivalence is not proved",
            "next_action": "retain Delta_Hsrc, R_PiH, and B_H_flux rows",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1778_2_first_rows",
            "decision": "STRICT_FIRST_ROW_SCHEMAS_STAGED_NONCLAIM",
            "reason": "the fallback is now concrete enough to fill with source-backed values later",
            "next_action": "fill no rows until parent source paths and units exist",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1778_3_best_next",
            "decision": "PARENT_CURRENT_ONE_OBSERVED_SOURCE_FUNCTOR_OR_DELTA_HSRC_FIRST_ROW_IS_NEXT",
            "reason": "Delta_Hsrc cannot close before theta/Q_tau, J_H^dress, and one observed coframe are owned",
            "next_action": "build 1779 parent-current one-observed-source-functor gate or first Delta_Hsrc row",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1778_0_primary",
            "next_target": "1779-Y5-R2FR-parent-current-one-observed-source-functor-or-Delta-Hsrc-first-row.md",
            "script": "scripts/Y5_R2FR_parent_current_one_observed_source_functor_or_Delta_Hsrc_first_row.py",
            "objective": "extract theta_total, Q_tau, J_H^dress, and one observed coframe from the parent branch; if not, stage the first strict Delta_Hsrc component row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1778_1_parallel",
            "next_target": "1779b-Y5-R2FR-RPiH-BH-flux-first-source-row-pack.md",
            "script": "scripts/Y5_R2FR_RPiH_BH_flux_first_source_row_pack.py",
            "objective": "prepare the old/new PiM equivalence fallback with R_PiH and B_H flux source requirements",
            "selection_status": "held_parallel",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "source_measure_lemma": source_measure_lemma_rows(),
        "proof_clause_audit": proof_clause_audit_rows(),
        "worldtube_current_map": worldtube_current_map_rows(),
        "strict_residual_rows": strict_residual_rows(),
        "rpih_bh_first_row_schema": rpih_bh_first_row_schema_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
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
        shutil.copy2(path, RAB_QUEUE / f"JR1778_{key.upper()}.csv")


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
        if not (RAB_QUEUE / f"JR1778_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    return not any(FORMALIZATION.rglob("*1778*")) if FORMALIZATION.exists() else True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1778_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1778_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1778_2_conditional_lemma_written",
            any(row["lemma_id"] == "ASM1778_0_conditional_theorem" and row["status"] == "CONDITIONAL_LEMMA_SHAPE_DERIVED" for row in rows_map["source_measure_lemma"]),
            "adopted-PiM source-measure conditional lemma is written",
        ),
        (
            "VAL1778_3_current_proof_not_promoted",
            any(row["lemma_id"] == "ASM1778_5_verdict" and row["status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["source_measure_lemma"]),
            "current source-measure proof remains unpromoted",
        ),
        (
            "VAL1778_4_proof_clause_blockers_retained",
            all(str(row["current_status"]).startswith(("MISSING", "DOWNSTREAM")) and not boolish(row["valid_for_claim"]) for row in rows_map["proof_clause_audit"]),
            "proof clause blockers remain explicit and nonclaim",
        ),
        (
            "VAL1778_5_current_map_nonclaim",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["worldtube_current_map"]),
            "worldtube current map remains nonclaim",
        ),
        (
            "VAL1778_6_strict_residual_rows_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["strict_residual_rows"]),
            "strict residual rows are staged but not score-ready",
        ),
        (
            "VAL1778_7_RPiH_BH_schema_nonclaim",
            all(not boolish(row["valid_for_claim"]) and not boolish(row["score_ready"]) for row in rows_map["rpih_bh_first_row_schema"]),
            "R_PiH/B_H first-row schemas remain nonclaim",
        ),
        (
            "VAL1778_8_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1778_9_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1778_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1778_11_decision_next",
            any(row["decision_id"] == "DEC1778_3_best_next" and "PARENT_CURRENT_ONE_OBSERVED_SOURCE_FUNCTOR" in row["decision"] for row in rows_map["decision"]),
            "decision selects parent-current one-observed-source-functor next",
        ),
        (
            "VAL1778_12_next_selected",
            any(row["route_id"] == "NEXT1778_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1778_13_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1778 CSVs parse"),
        ("VAL1778_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1778_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1778_16_formalization_untouched", formalization_untouched(), "no 1778 outputs found under formalization-workbench"),
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
            "check_id": "VAL1778_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1778 adopted-PiM source-measure glue or R_PiH first-row checkpoint",
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
            "# 1778 - Y5/R2FR Adopted-PiM Source-Measure Glue or RPiH First Row",
            "",
            "## Verdict",
            "",
            "The adopted Hamiltonian `Pi_M^H` route now has the exact source-measure contract it needs: the exterior Hamiltonian charge must equal the dressed observed Hilbert worldtube source before any Poisson/Gauss/orbital readout is allowed. The conditional lemma is clean, but current MTS does not yet sign it because the parent current, one-observed-coframe source functor, `Pi_M^H` chain map, boundary improvement flux, dressed-source map, and exterior C-term silence are still open.",
            "",
            "The practical win is that the failure is no longer foggy. It is now `Delta_Hsrc`, plus `R_PiH` and `B_H_flux`, with strict nonclaim first-row schemas. No fitted orbital `GM` is allowed to sneak upstream as a source definition.",
            "",
            "**Claim ceiling:** no adopted-`Pi_M` source-measure proof, old/topological `Pi_M` equivalence, measured-GM/Newton/Gauss/orbit reduction, PPN pass, R10/R11/WEP/clock/orbital pass, local-GR pass, GitHub action, or `formalization-workbench` edit is allowed from 1778.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Adopted-PiM Source-Measure Lemma",
            markdown_table(rows_map["source_measure_lemma"], ["lemma_id", "claim", "mathematical_form", "status", "proof_content", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Proof Clause Audit",
            markdown_table(rows_map["proof_clause_audit"], ["clause_id", "required_clause", "mathematical_form", "current_status", "why_blocks", "exit_condition", "valid_for_claim"]),
            "",
            "## Worldtube Current Map",
            markdown_table(rows_map["worldtube_current_map"], ["map_id", "object", "desired_relation", "current_status", "failure_if_missing", "valid_for_claim"]),
            "",
            "## Strict Residual Rows",
            markdown_table(rows_map["strict_residual_rows"], ["row_id", "quantity", "definition", "required_fields", "status", "bound_rule", "score_ready", "claim_allowed", "valid_for_claim"]),
            "",
            "## RPiH/BH First-Row Schema",
            markdown_table(rows_map["rpih_bh_first_row_schema"], ["schema_id", "target_quantity", "formula", "required_columns", "current_status", "acceptance_rule", "score_ready", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is good news in the unglamorous way: the route toward GR/Newton is getting more derivable, not more hand-wavy. The current branch still fails as a proof, but it fails at a precise bridge: `Q_tau` must be extracted from the parent action and shown to equal the same observed dressed Hilbert source that matter, clocks, and orbits read. That is exactly the next bridge to attack.",
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
    doc_path = ROOT / "1778-Y5-R2FR-adopted-PiM-source-measure-glue-or-RPiH-first-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1778 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
