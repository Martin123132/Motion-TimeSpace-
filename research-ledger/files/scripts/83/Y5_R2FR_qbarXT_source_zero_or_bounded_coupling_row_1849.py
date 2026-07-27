from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1849"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1849-Y5-R2FR-qbarXT-source-zero-or-bounded-coupling-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1849_0_1848_next",
        "source_key": "1848_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_NEXT_TARGET.csv",
        "needles": ["NEXT1848_0_primary", "1849-Y5-R2FR-qbarXT"],
        "role": "1848 selects qbarXT source-zero or bounded coupling row.",
    },
    {
        "source_id": "SRC1849_1_1848_validation",
        "source_key": "1848_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1848_VALIDATION.csv",
        "needles": ["VAL1848_OVERALL", "PASS"],
        "role": "confirms 1848 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1849_2_1848_qbar_handoff",
        "source_key": "1848_qbar_handoff",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1848_QBARXT_HANDOFF_SCHEMA.csv",
        "needles": ["QBH1848_4_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1848 gives the qbarXT handoff schema.",
    },
    {
        "source_id": "SRC1849_3_1027_source_zero",
        "source_key": "1027_source_zero_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv",
        "needles": ["QZ1027_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1027 records qbarXT/J_X source-zero as conditional only.",
    },
    {
        "source_id": "SRC1849_4_1027_counterexamples",
        "source_key": "1027_counterexample_guard",
        "source_path": RESIDUALS / "P8_Y5_R10_1027_COUNTEREXAMPLE_GUARD.csv",
        "needles": ["CE1027_0_common_Weyl", "CE1027_4_frame_rename"],
        "role": "1027 lists counterexamples blocking weak source-zero claims.",
    },
    {
        "source_id": "SRC1849_5_1027_bounded_schema",
        "source_key": "1027_bounded_qbar_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1027_BOUNDED_QBARXT_ROW_SCHEMA.csv",
        "needles": ["BQT1027_3_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1027 supplies bounded qbarXT row schema.",
    },
    {
        "source_id": "SRC1849_6_1027_dependencies",
        "source_key": "1027_dependency_links",
        "source_path": RESIDUALS / "P8_Y5_R10_1027_DEPENDENCY_LINKS.csv",
        "needles": ["DEP1027_3_no_cancellation", "GUARDRAIL_ACTIVE"],
        "role": "1027 links qbarXT to alpha products and no-cancellation guard.",
    },
    {
        "source_id": "SRC1849_7_1044_pullback",
        "source_key": "1044_matter_pullback_derivation",
        "source_path": RESIDUALS / "P8_Y5_R10_1044_MATTER_PULLBACK_DERIVATION.csv",
        "needles": ["MPD1044_8_current_verdict", "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED"],
        "role": "1044 gives exact ordinary-matter pullback theorem and current failure.",
    },
    {
        "source_id": "SRC1849_8_1044_premise_gate",
        "source_key": "1044_matter_pullback_premises",
        "source_path": RESIDUALS / "P8_Y5_R10_1044_MATTER_PULLBACK_PREMISE_GATE.csv",
        "needles": ["MPG1044_6_verdict", "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED"],
        "role": "1044 lists premise gates blocking matter-pullback zero.",
    },
    {
        "source_id": "SRC1849_9_1044_component_envelope",
        "source_key": "1044_qbar_component_envelope",
        "source_path": RESIDUALS / "P8_Y5_R10_1044_QBARXT_COMPONENT_ENVELOPE.csv",
        "needles": ["QBC1044_5_total_abs_guard", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1044 gives a more granular qbarXT component envelope.",
    },
    {
        "source_id": "SRC1849_10_1044_refusal",
        "source_key": "1044_placeholder_refusal",
        "source_path": RESIDUALS / "P8_Y5_R10_1044_PLACEHOLDER_REFUSAL_RUNNER.csv",
        "needles": ["REF1044_0_qbar_zero", "blocked"],
        "role": "1044 runner refuses qbar zero and bound claims.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_SOURCE_REGISTER.csv",
    "source_zero_proof": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_SOURCE_ZERO_PROOF_AUDIT.csv",
    "matter_pullback": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_MATTER_PULLBACK_DERIVATION.csv",
    "premise_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_MATTER_PULLBACK_PREMISE_GATE.csv",
    "counterexamples": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_COUNTEREXAMPLE_GUARD.csv",
    "bounded_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_BOUNDED_QBARXT_ROW_SCHEMA.csv",
    "component_envelope": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_QBARXT_COMPONENT_ENVELOPE.csv",
    "dependency_links": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_DEPENDENCY_LINKS.csv",
    "refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "branch_verdicts": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_BRANCH_VERDICTS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1849_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1849_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def source_zero_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QZ1849_0_chain_rule",
            "target": "qbar_XT=0/J_matter_pullback=0",
            "required_statement": "If X is vertical to q, e_obs=Obs_e(q(Phi)), S_matter=Sbar[psi,e_obs,theta_A], and Lie_vX theta_A=0, then Lie_vX S_matter=0.",
            "current_evidence": "chain-rule theorem is valid conditionally in 1027 and matter-pullback identity is exact in 1044",
            "status": "CONDITIONAL_THEOREM_VALID",
            "missing_for_claim": "parent-signed q/v_X, observed coframe functor, matter functor, no-marker constants and hidden-tail silence",
            "if_missing": "retain qbar_XT as finite source/test coupling",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QZ1849_1_q_verticality",
            "target": "Dq[v_X]=0",
            "required_statement": "X is a representative/gauge direction before variation, not a physical quotient observable.",
            "current_evidence": "1845 quotient route failed current branch; no-pole certificate remains conditional",
            "status": "MISSING_PARENT_Q_KERNEL_CERTIFICATE",
            "missing_for_claim": "presymplectic-null kernel, boundary flux zero and degree-count/no-pole proof",
            "if_missing": "ordinary matter can see an X-dependent observed-frame or source channel",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QZ1849_2_observed_coframe",
            "target": "Lie_vX e_obs=0",
            "required_statement": "e_obs=Obs_e(q(Phi)) is parent-signed and no representative Weyl/disformal frame affects rods, clocks, masses, charges or free fall.",
            "current_evidence": "frame/coframe descent is conditional; 1849 retains frame-leak component rows",
            "status": "MISSING_OBS_E_DESCENT_OR_FRAME_LEAK_ZERO",
            "missing_for_claim": "q/Obs_e parent signature and no-shadow-frame theorem or sourced frame-leak bounds",
            "if_missing": "qbar_XT can re-enter through common Weyl/disformal coupling",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QZ1849_3_matter_functor",
            "target": "S_matter descends through observed variables only",
            "required_statement": "S_matter=sum_A S_A[psi_A,e_obs,omega[e_obs],theta_A] for all ordinary matter/readout species.",
            "current_evidence": "1044 exact contract written but parent selection unsigned",
            "status": "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "missing_for_claim": "parent principle selecting strict observed coframe and one matter/source/readout action",
            "if_missing": "matter action can contain direct X-sensitive frame/source slot",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QZ1849_4_no_marker_constants",
            "target": "Lie_vX theta_A=0",
            "required_statement": "material constants, masses, clocks, EM constants and readout markers are quotient-owned/superselected, not vertical fields.",
            "current_evidence": "no-marker and material-marker counterexamples survive",
            "status": "MISSING_NO_MARKER_THEOREM",
            "missing_for_claim": "constant/mass/EM/material-marker descent or numeric b_A/b_alpha bounds",
            "if_missing": "WEP can pass by species-blindness while common source-normalization survives",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QZ1849_5_hidden_source_tail",
            "target": "no hidden non-Hilbert/source/domain tail",
            "required_statement": "non-Hilbert current, support shift, boundary tail, domain projector and source-normalization residuals are theorem-zero or bounded.",
            "current_evidence": "1044 keeps non-Hilbert/source/support residuals in qbar component envelope",
            "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_BOUND",
            "missing_for_claim": "q_nonH, Delta_W_support, domain/boundary/source-normalization rows with units and source paths",
            "if_missing": "qbar_XT=0 for visible matter still may not silence total local coupling",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "proof_id": "QZ1849_6_verdict",
            "target": "qbar_XT/J_X source-zero theorem",
            "required_statement": "QZ1849_1 through QZ1849_5 all close from the same parent branch.",
            "current_evidence": "conditional pieces exist, but no single parent certificate closes",
            "status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "q-kernel, observed coframe, matter functor, no-marker and hidden-source/boundary silence",
            "if_missing": "bounded qbar_XT component envelope remains mandatory",
            "valid_for_claim": False,
        },
    ]


def matter_pullback_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "MPD1849_0_target",
            "claim_piece": "ordinary test-body X charge",
            "formula": "qbar_XT := M_T^-1 delta_{v_X} S_T",
            "derivation_result": "TARGET_RESTATED",
            "proof_status": "NOT_A_CLAIM",
            "gap": "requires parent-owned vertical action on matter and matter functor descent",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "MPD1849_1_chain_rule_identity",
            "claim_piece": "chain-rule variation",
            "formula": "delta_v S_T = 1/2 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu + sum_a int J_theta^a Lie_v theta_a + boundary/gauge/E_Psi terms",
            "derivation_result": "DERIVED_STANDARD_ON_SHELL_IDENTITY",
            "proof_status": "CONDITIONAL_MATH_OK",
            "gap": "zero only if geometry, constants, matter lift and boundary terms descend",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "MPD1849_2_geometry_pullback_zero",
            "claim_piece": "observed geometry X-blindness",
            "formula": "if ghat=ghat(q_loc(Phi)) and Dq_loc[v_X]=0, then Lie_v ghat_munu=0 up to owned gauge",
            "derivation_result": "SUFFICIENT_SUBLEMMA_WRITTEN",
            "proof_status": "PARENT_FUNCTOR_UNSIGNED",
            "gap": "unique observed coframe/metric functor not parent-derived in current corpus",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "MPD1849_3_constants_zero",
            "claim_piece": "matter constants X-blindness",
            "formula": "Lie_v theta_a=0 for masses, charges, alpha_EM, clocks, representation labels and material standards",
            "derivation_result": "SUFFICIENT_SUBLEMMA_WRITTEN",
            "proof_status": "CONSTANT_SUPERSELECTION_UNSIGNED",
            "gap": "no parent theorem excludes theta_a(X), theta_a(I_Q), or material-marker dependence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "MPD1849_4_source_current_universality",
            "claim_piece": "source-current equality",
            "formula": "one Hilbert/coframe matter source and one global/superselected kappa multiply sum_A T_A",
            "derivation_result": "RELATIVE_CERTIFICATE_READY",
            "proof_status": "PARENT_SCHEMA_UNSIGNED",
            "gap": "relative species prefactors, non-Hilbert currents and measured-GM calibration are not removed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "MPD1849_5_exact_theorem_if_signed",
            "claim_piece": "conditional matter-pullback theorem",
            "formula": "geometry pullback + constants zero + owned matter lift + boundary silence imply delta_v S_T=0, hence qbar_XT=0 and J_matter=0",
            "derivation_result": "EXACT_CONDITIONAL_THEOREM",
            "proof_status": "NOT_PARENT_SIGNED",
            "gap": "strong future parent-action contract, not a current MTS proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "MPD1849_6_current_verdict",
            "claim_piece": "current MTS matter-pullback zero",
            "formula": "qbar_XT=0 and J_matter=0 cannot be promoted until parent matter functor and no-marker/source-current clauses are signed",
            "derivation_result": "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED",
            "proof_status": "RESIDUAL_REQUIRED",
            "gap": "build nonclaim qbarXT component envelope and keep WEP/R10/clock links active",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def premise_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MPG1849_0_parent_matter_functor",
            "premise": "S_matter=sum_A S_A[Psi_A,e_obs(q_loc(Phi)),omega[e_obs],theta_A]",
            "needed_for": "geometry and matter-domain pullback",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "qbar_geom and frame/source residuals remain active",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MPG1849_1_vertical_kernel",
            "premise": "v_X in ker(Dq_loc) with owned fixed/gauge lift on Psi_A",
            "needed_for": "Lie_v e_obs=0 and no physical matter transformation",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "representative motion may be physical fifth-force/source charge",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MPG1849_2_constant_superselection",
            "premise": "Lie_v theta_A=0 for masses, charges, alpha_EM, clocks and representation labels",
            "needed_for": "no constant/clock/material qbar channel",
            "current_status": "NOT_PARENT_SIGNED",
            "if_missing": "qbar_marker and clock/fine-structure rows remain active",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MPG1849_3_no_marker_extension",
            "premise": "no direct material marker, hidden conformal/disformal frame, source-only coefficient or post-readout EFT counterterm",
            "needed_for": "no hidden fifth-force loophole",
            "current_status": "CONTRACT_WRITTEN_NOT_DERIVED",
            "if_missing": "relative species/source charges survive even when Ward identities hold",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MPG1849_4_boundary_support_silence",
            "premise": "matter edge/worldtube boundary terms vanish or are retained with source-backed bounds",
            "needed_for": "chain-rule boundary term cannot hide qbarXT",
            "current_status": "OPEN",
            "if_missing": "qbar_nonH and boundary/source support residuals remain active",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MPG1849_5_universal_source_current",
            "premise": "one Hilbert/coframe matter source and one global/superselected kappa",
            "needed_for": "source-charge WEP and measured-source consistency",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "if_missing": "WEP source-charge and measured-GM residual rows stay live",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "MPG1849_6_verdict",
            "premise": "all matter-pullback gates pass simultaneously",
            "needed_for": "J_matter=0 and qbar_XT=0 claim",
            "current_status": "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED",
            "if_missing": "qbarXT bound fallback is mandatory",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def counterexample_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1849_0_common_Weyl",
            "weak_premise": "universal covariant matter coupling",
            "construction": "e_m=A_g(X)e_obs or g_m=exp(2F(X))g_obs for all species",
            "failure": "WEP composition spread can vanish while qbar_XT is common nonzero source charge",
            "required_repair": "prove A_g'(0)=0/no-shadow-frame theorem or source c_g/b_g bound",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1849_1_disformal_frame",
            "weak_premise": "single observed coframe notation",
            "construction": "g_m=A_g(X)^2 g_obs+B_g(X)U_muU_nu",
            "failure": "preferred-frame/PPN/clock source can survive coframe projection",
            "required_repair": "disformal absence theorem or PPN/preferred-frame bound row",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1849_2_material_marker",
            "weak_premise": "matter geometry is X-blind",
            "construction": "theta_A(X), m_A(X), alpha_EM(X), or material class labels enter ordinary matter constants",
            "failure": "delta_X S_matter returns through constants even when partial_X e_obs=0",
            "required_repair": "no-marker theorem or material sensitivity b_A/b_alpha rows",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1849_3_nonHilbert_tail",
            "weak_premise": "Hilbert matter current is standard",
            "construction": "non-Hilbert current, boundary/source support shift, or domain/projector tail",
            "failure": "ordinary Hilbert qbar_XT may be zero while source-normalization residual remains",
            "required_repair": "q_nonH/Delta_W_support/source-tail theorem-zero or bound rows",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "counterexample_id": "CE1849_4_frame_rename",
            "weak_premise": "choose e_obs as matter frame",
            "construction": "rename the matter frame and move X-dependence into EH/operator/source calibration",
            "failure": "projection-by-declaration hides the same coupling in another sector",
            "required_repair": "parent q/Obs_e and full source-normalization ledger, not a field rename",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
    ]


def bounded_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQT1849_0_visible_geometry",
            "symbol": "qbar_geom",
            "definition": "ordinary test-body X charge from representative Weyl/disformal observed-frame leakage",
            "formula_or_bound": "|qbar_geom| <= |tau_R10 c_g| + |tau_dis b_dis|",
            "required_columns": "system_id;test_body;lambda;tau_R10;c_g;tau_dis;b_dis;units;source_path;valid_for_claim",
            "current_status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "observable_link": "R10;PPN;clock;WEP",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQT1849_1_marker_constants",
            "symbol": "qbar_marker",
            "definition": "ordinary test-body X charge from masses, material constants, EM constants or clock markers",
            "formula_or_bound": "|qbar_marker| <= sum_A |s_A b_A| + |s_alpha b_alpha|",
            "required_columns": "system_id;material_pair;species_sensitivities;b_A;b_alpha;units;source_path;valid_for_claim",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "observable_link": "WEP;clock;composition;R10",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQT1849_2_nonHilbert_tail",
            "symbol": "qbar_nonH",
            "definition": "test/source coupling from non-Hilbert current, boundary tail, support shift, or domain projector",
            "formula_or_bound": "|qbar_nonH| <= |q_nonH| + |Delta_W_support| + |q_domain| + |q_boundary|",
            "required_columns": "system_id;arena;q_nonH;Delta_W_support;q_domain;q_boundary;units;source_path;valid_for_claim",
            "current_status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "observable_link": "R10;orbital;source_normalization;local_GR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQT1849_3_total_abs_guard",
            "symbol": "qbar_XT_bound_abs",
            "definition": "no-cancellation envelope for ordinary test-body X charge",
            "formula_or_bound": "|qbar_XT| <= |qbar_geom| + |qbar_marker| + |qbar_nonH| + |qbar_hidden|",
            "required_columns": "system_id;lambda;abs_qbar_geom;abs_qbar_marker;abs_qbar_nonH;abs_qbar_hidden;qbar_XT_bound_abs;units;source_paths;valid_for_claim",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "observable_link": "R10;WEP;clock;PPN;local_GR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "BQT1849_4_claim_gate",
            "symbol": "qbar_XT_claim_gate",
            "definition": "qbar_XT zero or bound can be claimed only after every component has theorem-zero or numeric bound",
            "formula_or_bound": "valid_for_claim=true only if no MISSING markers and qbar_XT_bound_abs has units/source paths",
            "required_columns": "all_component_statuses;all_source_paths;units;normalization;valid_for_claim",
            "current_status": "CLAIM_BLOCKED",
            "observable_link": "all_local_arenas",
            "valid_for_claim": False,
        },
    ]


def component_envelope_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "QBC1849_0_qbar_geom",
            "symbol": "qbar_geom",
            "definition": "ordinary test-body X charge from observed metric/coframe leakage",
            "formula_or_bound": "qbar_geom=(2 M_T)^-1 int sqrt(-g_hat) T_T^{mu nu} Lie_v ghat_munu",
            "required_input": "Lie_v ghat_munu or theorem-zero geometry descent certificate",
            "current_value": "MISSING_LIE_V_GHAT",
            "units": "dimensionless_after_normalization",
            "observable_links": "R10;PPN;clock;WEP_direct_geometry",
            "status": "MISSING_FRAME_LEAK_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QBC1849_1_qbar_constants",
            "symbol": "qbar_constants",
            "definition": "ordinary test-body X charge from masses, charges, alpha_EM, clock, or representation constants",
            "formula_or_bound": "qbar_constants=M_T^-1 sum_a int J_theta^a Lie_v theta_a",
            "required_input": "constant-superselection theorem or dtheta_a/dX coefficients with source paths",
            "current_value": "MISSING_DTHETA_DX",
            "units": "dimensionless_after_sensitivity_normalization",
            "observable_links": "WEP;clock;fine_structure;R10",
            "status": "MISSING_NO_MARKER_CONSTANT_THEOREM_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QBC1849_2_qbar_marker",
            "symbol": "qbar_marker",
            "definition": "source/test charge from material markers, hidden frames, direct MTS vertices, or post-readout masks",
            "formula_or_bound": "|qbar_marker| <= sum |s_marker b_marker| over declared channels",
            "required_input": "no-marker theorem or marker sensitivities and coefficients",
            "current_value": "MISSING_MARKER_COEFFICIENTS",
            "units": "dimensionless",
            "observable_links": "WEP_source_charge;clock;R11;R10",
            "status": "MISSING_NO_MARKER_THEOREM_OR_NUMERIC_BOUNDS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QBC1849_3_qbar_source_weight",
            "symbol": "qbar_source_weight",
            "definition": "relative species or class source-only weight in the active gravitational source",
            "formula_or_bound": "|qbar_source_weight| <= max_A |kappa_A/kappa_univ - 1| plus measured-GM calibration tail",
            "required_input": "minimal matter action source-current theorem or source-weight split values",
            "current_value": "MISSING_DELTA_KAPPA_A",
            "units": "dimensionless_after_source_normalization",
            "observable_links": "WEP_source_charge;orbital;R10_source_mass",
            "status": "MISSING_UNIVERSAL_SOURCE_CURRENT_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QBC1849_4_qbar_nonH",
            "symbol": "qbar_nonH",
            "definition": "non-Hilbert, boundary, connection, domain or support-shift contribution",
            "formula_or_bound": "|qbar_nonH| <= |q_nonH| + |Delta_W_support| + |q_domain| + |q_boundary|",
            "required_input": "hidden-source zero theorem or component numeric bounds",
            "current_value": "MISSING_NONHILBERT_BOUND",
            "units": "dimensionless_or_declared_component_units",
            "observable_links": "R10;orbital;source_normalization;boundary",
            "status": "MISSING_HIDDEN_SOURCE_ZERO_OR_NUMERIC_BOUND",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "QBC1849_5_total_abs_guard",
            "symbol": "qbar_XT_bound_abs",
            "definition": "no-cancellation envelope for ordinary test-body X charge",
            "formula_or_bound": "|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|+|qbar_nonH|",
            "required_input": "all components theorem-zero or source-backed numeric bounds",
            "current_value": "MISSING_COMPONENT_VALUES",
            "units": "dimensionless_after_declared_normalization",
            "observable_links": "R10;WEP;clock;PPN;local_GR",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def dependency_link_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "dependency_id": "DEP1849_0_alpha_product",
            "quantity": "alpha_bulk(lambda_X)",
            "depends_on": "K_X;Qbar_XH(lambda_X);qbar_XT;lambda_X;alpha_bound(lambda_X)",
            "current_status": "BLOCKED_BY_QBAR_AND_OTHER_INPUTS",
            "why": "qbar_XT is only one factor; qbar_XT bound also needs K_X, Qbar_XH, lambda_X and real bound curve",
            "next_action": "keep alpha row nonclaim until every factor is sourced",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dependency_id": "DEP1849_1_source_zero_stronger",
            "quantity": "qbar_XT=0",
            "depends_on": "q-kernel;Obs_e descent;matter functor;no-marker;hidden-tail silence",
            "current_status": "FAIL_CURRENT_CLAIM",
            "why": "conditional chain rule is valid but parent certificate does not close",
            "next_action": "do not set alpha to zero by qbar_XT unless certificate closes",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dependency_id": "DEP1849_2_bound_fallback",
            "quantity": "qbar_XT_bound_abs",
            "depends_on": "c_g;b_dis;b_A;b_alpha;q_nonH;Delta_W_support;q_domain;q_boundary",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "why": "surviving counterexamples are componentized into bounded source rows",
            "next_action": "source first real c_g/b_A/q_nonH rows or prove theorem-zero",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "dependency_id": "DEP1849_3_no_cancellation",
            "quantity": "total local coupling envelope",
            "depends_on": "absolute component sum, not signed cancellation",
            "current_status": "GUARDRAIL_ACTIVE",
            "why": "unknown frame/marker/source components cannot cancel into fake GR limit",
            "next_action": "use component-sum absolute envelopes for all retained residuals",
            "valid_for_claim": False,
        },
    ]


def refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": "REF1849_0_qbar_zero",
            "object": "qbar_XT=0",
            "current_status": "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED",
            "refusal_status": "BLOCKED",
            "failure_reasons": "MPG1849_0_parent_matter_functor;MPG1849_1_vertical_kernel;MPG1849_2_constant_superselection;MPG1849_3_no_marker_extension;MPG1849_4_boundary_support_silence;MPG1849_5_universal_source_current;MPG1849_6_verdict",
            "score_eligible": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "refusal_id": "REF1849_1_Jmatter_zero",
            "object": "J_matter=0",
            "current_status": "FAIL_CURRENT_CLAIM_QBARXT_ZERO_NOT_SIGNED",
            "refusal_status": "BLOCKED",
            "failure_reasons": "parent matter functor and no-marker/source-current clauses unsigned",
            "score_eligible": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "refusal_id": "REF1849_2_qbar_bound_values",
            "object": "qbar_XT_bound_abs",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "refusal_status": "BLOCKED",
            "failure_reasons": "QBC1849_0_qbar_geom;QBC1849_1_qbar_constants;QBC1849_2_qbar_marker;QBC1849_3_qbar_source_weight;QBC1849_4_qbar_nonH;QBC1849_5_total_abs_guard",
            "score_eligible": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def branch_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1849_0_conditional_zero",
            "branch": "qbar_XT source-zero",
            "status": "CONDITIONAL_THEOREM_VALID_NOT_PARENT_SIGNED",
            "because": "chain-rule zero works if q, Obs_e, S_matter, theta_A and hidden tails are all parent-owned",
            "allowed_statement": "MTS has exact source-zero theorem target",
            "forbidden_statement": "current MTS has qbar_XT=0",
            "next_action": "retain qbar_XT as source-coupling row unless parent certificate closes",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1849_1_counterexamples",
            "branch": "weak-premise shortcut rejection",
            "status": "COUNTEREXAMPLES_BLOCK_ZERO_CLAIM",
            "because": "universal Weyl, disformal, marker constants, source weights and non-Hilbert tails remain legal",
            "allowed_statement": "WEP/species-blindness can help but is not source-zero",
            "forbidden_statement": "WEP/covariance alone kills qbar_XT",
            "next_action": "source or zero each counterexample component",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1849_2_bound_schema",
            "branch": "bounded qbarXT fallback",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "because": "component rows define how to bound qbar_XT without cancellation, but no numeric/theorem-zero inputs are filled",
            "allowed_statement": "bounded coupling interface is ready",
            "forbidden_statement": "bounded coupling has passed a local test",
            "next_action": "fill first real frame/marker/non-Hilbert source row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1849_3_next_target",
            "branch": "next target",
            "status": "FRAME_MARKER_BOUND_INPUT_OR_NO_MARKER_THEOREM",
            "because": "proof route failed current claim; next honest move is stronger no-marker theorem or first real bound rows",
            "allowed_statement": "1850 should attack c_g/b_A/q_nonH first rows or no-marker theorem",
            "forbidden_statement": "run local tests as claim before qbarXT row is real",
            "next_action": "1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1849_0_sources_registered",
            "claim": "1849 source chain exists",
            "gate_pass": False,
            "reason": "source chain supports audit continuity only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1849_1_chain_rule_shape",
            "claim": "chain-rule source-zero theorem shape is claim-active",
            "gate_pass": False,
            "reason": "conditional theorem written, but parent premises are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1849_2_matter_functor",
            "claim": "ordinary matter functor descends through observed variables only",
            "gate_pass": False,
            "reason": "MPG1849_0 remains NOT_PARENT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1849_3_no_marker",
            "claim": "constants/material markers are X-independent",
            "gate_pass": False,
            "reason": "no-marker theorem missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1849_4_qbarXT_zero_claim",
            "claim": "qbar_XT/J_X source-zero may be claimed",
            "gate_pass": False,
            "reason": "required clauses do not close together",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1849_5_qbarXT_bound_claim",
            "claim": "qbar_XT bound row may be scored",
            "gate_pass": False,
            "reason": "component values and source paths are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1849_6_local_GR_claim",
            "claim": "local GR/Newton reduction is derived",
            "gate_pass": False,
            "reason": "source-zero, no-pole, Hessian, boundary and PPN gates remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1849_0_zero_result",
            "decision": "qbar_XT=0/J_X=0 is an exact conditional theorem but not a current MTS result.",
            "because": "parent q-kernel, observed coframe descent, matter functor, no-marker constants and hidden-source silence are not signed together.",
            "next_action": "do not claim source-zero or local GR from chain rule alone",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1849_1_bound_schema",
            "decision": "The bounded qbar_XT row schema is staged.",
            "because": "surviving counterexamples map cleanly into c_g/b_dis/b_A/b_alpha/q_nonH/support components.",
            "next_action": "fill real theorem-zero or numeric bounds before scoring",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1849_2_coupling_status",
            "decision": "The coupling gap is now a source-row problem, not a vague criticism.",
            "because": "qbar_XT has named components, dependencies, observables and no-cancellation policy.",
            "next_action": "source first c_g/b_A/q_nonH rows or derive no-marker theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1849_3_next_target",
            "decision": "Next target is frame/marker coupling bound input pack or no-marker theorem.",
            "because": "clean zero proof did not close; next honest progress is stronger parent no-marker theorem or first real bound rows.",
            "next_action": "1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1849_0_primary",
            "next_target": "1850-Y5-R2FR-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
            "script": "scripts/Y5_R2FR_frame_marker_coupling_bound_input_pack_or_no_marker_theorem_1850.py",
            "objective": "try to derive the no-marker/constant-descent theorem for ordinary matter; if unsigned, build first claim-blocked c_g, b_dis, b_A, b_alpha, q_nonH and support-shift bound rows with units, source paths and observable links",
            "selection_status": "selected",
            "success_condition": "no-marker theorem closes, or frame/marker/source bound input pack is complete and nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1849_1_parallel",
            "next_target": "1850b-Y5-R2FR-parent-matter-functor-descent-signature.md",
            "script": "scripts/Y5_R2FR_parent_matter_functor_descent_signature_1850b.py",
            "objective": "try to sign the parent ordinary-matter functor and vertical matter lift directly",
            "selection_status": "held",
            "success_condition": "one parent matter functor row signs geometry pullback, matter lift, constants and boundary silence together",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "source_zero_proof": source_zero_proof_rows(),
        "matter_pullback": matter_pullback_rows(),
        "premise_gates": premise_gate_rows(),
        "counterexamples": counterexample_rows(),
        "bounded_schema": bounded_schema_rows(),
        "component_envelope": component_envelope_rows(),
        "dependency_links": dependency_link_rows(),
        "refusal": refusal_rows(),
        "branch_verdicts": branch_verdict_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for row in rows:
        for key in row:
            if key not in names:
                names.append(key)
    return names


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        for target in [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1849_{key.upper()}.csv",
        ]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1849_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1849-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1849",
        "P8_Y5_BRR545_1849",
        "Y5_R2FR_qbarXT_source_zero_or_bounded_coupling_row_1849",
    ]
    return not any(any(marker in path.name for marker in markers) for path in FORMALIZATION.rglob("*"))


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "score_eligible", "score_ready"]:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            has_missing = any("MISSING_" in str(value) for value in row.values())
            if not has_missing:
                continue
            for field in ["valid_for_claim", "claim_allowed", "score_eligible", "score_ready"]:
                if row.get(field) is True:
                    return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    checks = [
        ("VAL1849_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1849_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1849_2_source_zero_blocks",
            any(row["proof_id"] == "QZ1849_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["source_zero_proof"]),
            "qbarXT source-zero theorem remains nonclaim",
        ),
        (
            "VAL1849_3_matter_pullback_exact_conditional",
            any(row["derivation_id"] == "MPD1849_5_exact_theorem_if_signed" and row["derivation_result"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["matter_pullback"]),
            "matter-pullback theorem is written as exact conditional",
        ),
        (
            "VAL1849_4_premise_gates_block",
            any(row["gate_id"] == "MPG1849_6_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_MATTER_PULLBACK_NOT_SIGNED" for row in rows_map["premise_gates"]),
            "matter-pullback premise gates block claim",
        ),
        (
            "VAL1849_5_counterexamples_block",
            all(row["blocks_zero_claim"] is True and row["valid_for_claim"] is False for row in rows_map["counterexamples"]),
            "counterexamples all block weak zero claims",
        ),
        (
            "VAL1849_6_bound_schema_nonclaim",
            any(row["row_id"] == "BQT1849_4_claim_gate" and row["current_status"] == "CLAIM_BLOCKED" for row in rows_map["bounded_schema"]),
            "bounded qbarXT schema remains claim-blocked",
        ),
        (
            "VAL1849_7_component_envelope_nonclaim",
            any(row["component_id"] == "QBC1849_5_total_abs_guard" and row["status"] == "SCHEMA_READY_VALUES_MISSING" for row in rows_map["component_envelope"]),
            "component envelope remains values-missing",
        ),
        (
            "VAL1849_8_dependency_guard_active",
            any(row["dependency_id"] == "DEP1849_3_no_cancellation" and row["current_status"] == "GUARDRAIL_ACTIVE" for row in rows_map["dependency_links"]),
            "no-cancellation dependency guard is active",
        ),
        (
            "VAL1849_9_refusal_runner_blocks",
            all(row["claim_allowed"] is False and row["score_eligible"] is False for row in rows_map["refusal"]),
            "placeholder/refusal runner blocks all claims",
        ),
        (
            "VAL1849_10_branch_next_selected",
            any(row["verdict_id"] == "BV1849_3_next_target" and row["status"] == "FRAME_MARKER_BOUND_INPUT_OR_NO_MARKER_THEOREM" for row in rows_map["branch_verdicts"]),
            "branch verdict selects frame/marker/no-marker target",
        ),
        (
            "VAL1849_11_claim_gates_blocked",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in rows_map["claim_gate"]),
            "all claim gates remain blocked",
        ),
        (
            "VAL1849_12_decision_next",
            any(row["decision_id"] == "DEC1849_3_next_target" and "frame/marker" in row["decision"] for row in rows_map["decision"]),
            "decision ledger selects frame/marker coupling target",
        ),
        (
            "VAL1849_13_next_target_selected",
            any(row["route_id"] == "NEXT1849_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1849_14_no_claim_flags", no_claim_flags(rows_map), "no claim flags are true"),
        ("VAL1849_15_missing_rows_nonclaim", missing_rows_not_ready(rows_map), "MISSING_* rows stay nonclaim"),
        ("VAL1849_16_csv_parse", csv_parse_all(), "all generated 1849 CSVs parse"),
        ("VAL1849_17_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1849_18_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1849_19_formalization_untouched", no_formalization_outputs(), "no 1849 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1849_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1849 qbarXT source-zero or bounded coupling row",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1849 Y5 R2FR qbarXT source-zero or bounded coupling row",
            "",
            "**Progress:** 1849 ports the source-zero route into the active parent-q_loc branch. The chain-rule proof is exact as conditional mathematics: if matter only sees quotient-owned observed variables and constants are vertical-trivial, then `qbar_XT=0` and `J_matter=0` for ordinary matter.",
            "",
            "**Current verdict:** the zero theorem is not an active MTS claim. The parent q-kernel, observed coframe, matter functor, no-marker constants, hidden source tails, source-current universality, and boundary support do not close together. The bounded `qbar_XT` component envelope is staged but value-missing.",
            "",
            "**Claim ceiling:** no source-zero claim, no finite-alpha pass, no R10/WEP/clock/PPN/orbital pass, no local-GR/Newton reduction, no GitHub action, and no `formalization-workbench` edit is allowed from 1849.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Source-Zero Proof Audit",
            markdown_table(rows_map["source_zero_proof"], ["proof_id", "target", "required_statement", "current_evidence", "status", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "",
            "## Matter Pullback Derivation",
            markdown_table(rows_map["matter_pullback"], ["derivation_id", "claim_piece", "formula", "derivation_result", "proof_status", "gap", "claim_allowed", "valid_for_claim"]),
            "",
            "## Matter Pullback Premise Gates",
            markdown_table(rows_map["premise_gates"], ["gate_id", "premise", "needed_for", "current_status", "if_missing", "gate_pass", "valid_for_claim"]),
            "",
            "## Counterexample Guard",
            markdown_table(rows_map["counterexamples"], ["counterexample_id", "weak_premise", "construction", "failure", "required_repair", "blocks_zero_claim", "valid_for_claim"]),
            "",
            "## Bounded qbarXT Row Schema",
            markdown_table(rows_map["bounded_schema"], ["row_id", "symbol", "definition", "formula_or_bound", "required_columns", "current_status", "observable_link", "valid_for_claim"]),
            "",
            "## qbarXT Component Envelope",
            markdown_table(rows_map["component_envelope"], ["component_id", "symbol", "definition", "formula_or_bound", "required_input", "current_value", "units", "observable_links", "status", "valid_for_claim"]),
            "",
            "## Dependency Links",
            markdown_table(rows_map["dependency_links"], ["dependency_id", "quantity", "depends_on", "current_status", "why", "next_action", "valid_for_claim"]),
            "",
            "## Placeholder Refusal Runner",
            markdown_table(rows_map["refusal"], ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed", "valid_for_claim"]),
            "",
            "## Branch Verdicts",
            markdown_table(rows_map["branch_verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the coupling fight with the fog removed. The route to local GR is not 'qbar is small because vibes'; it is either a signed source-zero theorem or a bounded residual vector with frame, marker, source-weight and non-Hilbert components. That is the sort of thing local tests can actually attack.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1849 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
