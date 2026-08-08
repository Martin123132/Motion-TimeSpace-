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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1827"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1827-Y5-R2FR-Palatini-Regge-field-match-or-c2-scalaron-map.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1827_0_1826_next",
        "source_key": "1826_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_NEXT_TARGET.csv",
        "needles": ["NEXT1826_0_primary", "selected"],
        "role": "1826 selects Palatini/Regge field match or finite c2 scalaron map.",
    },
    {
        "source_id": "SRC1827_1_1826_validation",
        "source_key": "1826_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1826_VALIDATION.csv",
        "needles": ["VAL1826_OVERALL", "PASS"],
        "role": "confirms 1826 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1827_2_1826_contract",
        "source_key": "1826_palatini_regge_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_PALATINI_REGGE_OWNER_CONTRACT.csv",
        "needles": ["PRC1826_6_total", "CONTRACT_WRITTEN_NOT_SIGNED"],
        "role": "field/action/variation owner contract is written but unsigned.",
    },
    {
        "source_id": "SRC1827_3_1826_c2_fallback",
        "source_key": "1826_trace_norm_c2_prior",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1826_TRACE_NORM_C2_PRIOR_ROWS.csv",
        "needles": ["TNF1826_5_total", "C2_PRIOR_CONTRACT_READY_NONCLAIM"],
        "role": "trace/norm c2 branch remains the explicit fallback.",
    },
    {
        "source_id": "SRC1827_4_511_fixed_point",
        "source_key": "511_local_GR_fixed_point_ansatz",
        "source_path": ROOT / "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "needles": ["A511_0_EH_core", "MTS_symbol_mapping_now_required"],
        "role": "EH fixed-point action blocks exist as an ansatz; MTS symbol matching is required.",
    },
    {
        "source_id": "SRC1827_5_512_symbol_map",
        "source_key": "512_symbol_to_action_blocks",
        "source_path": ROOT / "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "needles": ["g_obs / g_readout", "no_symbol_fully_promotes_local_GR"],
        "role": "MTS symbols are placed against action blocks but none promote local GR.",
    },
    {
        "source_id": "SRC1827_6_538_euler_ward",
        "source_key": "538_euler_ward",
        "source_path": ROOT / "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
        "needles": ["EW538_4_PiM_Hilbert_identification", "not local GR"],
        "role": "Euler/Ward chain is conditional; Pi_M/Hilbert identification blocks local GR.",
    },
    {
        "source_id": "SRC1827_7_1561_ansatz",
        "source_key": "1561_minimal_action_ansatz",
        "source_path": ROOT / "1561-Y5-minimal-parent-weak-field-action-ansatz-and-Euler-Ward-PPN-gate.md",
        "needles": ["ADOPT1561_2_MTS_matching", "MISSING_SYMBOL_MATCH"],
        "role": "minimal EH ansatz is not adopted because symbol matching and source/boundary locks are missing.",
    },
    {
        "source_id": "SRC1827_8_1541_qmap",
        "source_key": "1541_observed_coframe_candidate",
        "source_path": ROOT / "1541-Y5-quotient-map-vertical-generator-kernel-certificate.md",
        "needles": ["QMAP1541_1_observed_coframe", "CONDITIONAL_PRIOR_CONTRACT"],
        "role": "observed coframe/g_obs candidate exists but is only conditional.",
    },
    {
        "source_id": "SRC1827_9_1542_q_definition",
        "source_key": "1542_visible_quotient_candidate",
        "source_path": ROOT / "1542-Y5-q-definition-or-Dqvm-coupling-coefficient-source-pack.md",
        "needles": ["q_loc(Phi)=(e_obs,g_obs,omega_obs,theta_vis,Pi_M J_H", "CANDIDATE_ONLY"],
        "role": "visible quotient candidate includes e_obs, g_obs, omega_obs, theta, and Pi_M J_H but is not proved.",
    },
    {
        "source_id": "SRC1827_10_463_R2FR",
        "source_key": "463_R2FR_operator_gate",
        "source_path": ROOT / "463-EH-only-or-R11-executable-vector-gate.md",
        "needles": ["R2_fR_scalar_mode", "c_R2/c_fR"],
        "role": "finite R2/fR scalar-mode row requires coefficient, scalar mass/coupling, and local maps.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_SOURCE_REGISTER.csv",
    "field_match_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_PALATINI_FIELD_MATCH_ATTEMPT.csv",
    "block_map": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_PALATINI_BLOCK_MAP.csv",
    "obstruction_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_FIELD_MATCH_OBSTRUCTION_LEDGER.csv",
    "c2_scalaron_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_C2_SCALARON_MAP_CONTRACT.csv",
    "local_gr_impact": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_LOCAL_GR_IMPACT_LEDGER.csv",
    "acceptance_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_ACCEPTANCE_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1827_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1827_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        missing_needles = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and not missing_needles,
                "missing_needles": ";".join(missing_needles),
                "role": source["role"],
            }
        )
    return rows


def field_match_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_0_target",
            "target": "field-match MTS to Palatini/Regge action",
            "test": "identify e_obs, omega_obs, F[omega], oriented hinge bivector B_h/A_h, signed Log(U_h), kappa, matter descent, and boundary variation in one parent action",
            "current_status": "TARGET_ATTEMPTED",
            "blocker": "multiple clauses remain candidate-only or missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_1_coframe",
            "target": "observed coframe e_obs / metric g_obs",
            "test": "q_loc candidate includes e_obs and g_obs, and prior local-GR maps place g_obs in the EH core",
            "current_status": "PARTIAL_CANDIDATE_UNSIGNED",
            "blocker": "coframe descent/no-shadow-frame theorem remains conditional",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_2_connection",
            "target": "connection omega_obs / Gamma_eff",
            "test": "Palatini action requires a connection whose curvature gives the local holonomy; MTS has Gamma_eff/omega_obs candidates but not a signed compatibility theorem",
            "current_status": "MISSING_CONNECTION_COMPATIBILITY",
            "blocker": "no proof that Gamma_eff is the Levi-Civita/spin connection of e_obs or an allowed independent connection with torsion/nonmetricity controlled",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_3_curvature_holonomy",
            "target": "F[omega], U_h, signed Log(U_h)",
            "test": "derive curvature and small-loop holonomy from the MTS connection/load grammar",
            "current_status": "MISSING_CURVATURE_HOLONOMY_OWNER",
            "blocker": "the log-holonomy variable is named by 1826 but not generated from the parent MTS connection",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_4_hinge_bivector",
            "target": "oriented hinge bivector / area A_h",
            "test": "construct B_h ~ integral_h e wedge e and a signed orientation from MTS cells/domains",
            "current_status": "MISSING_HINGE_BIVECTOR_OWNER",
            "blocker": "local MTS cell/domain machinery has not supplied a Regge hinge area/bivector with parent orientation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_5_kappa",
            "target": "constant kappa / G_eff normalization",
            "test": "match kappa to topological/global integration constant and measured source normalization",
            "current_status": "CONDITIONAL_KAPPA_CANDIDATE_ONLY",
            "blocker": "source-normalized GM/Pi_M/Hilbert charge equality remains unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_6_matter",
            "target": "universal matter descent",
            "test": "S_matter[psi,e_obs] must use one observed coframe with no hidden species/source/frame coupling",
            "current_status": "MISSING_MATTER_DESCENT",
            "blocker": "ordinary matter coframe descent is a repeated conditional contract, not a parent theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_7_variation_boundary",
            "target": "theta_MTS, Q_tau, Pi_M and boundary reference",
            "test": "vary the action and recover the correct symplectic potential, Hamiltonian charge, and boundary terms before readout",
            "current_status": "MISSING_VARIATION_AND_CHARGE_GLUE",
            "blocker": "Euler/Ward chain remains conditional and Pi_M/Hilbert identification is not signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "FMA1827_8_verdict",
            "target": "1827 field match closes Palatini/Regge owner",
            "test": "all FMA1827_1 through FMA1827_7 pass in one parent action",
            "current_status": "FIELD_MATCH_FAILS_CURRENT_CORPUS",
            "blocker": "coframe candidate exists, but connection/holonomy/hinge/action variation/source descent are not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def block_map_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "block_id": "PBM1827_0_e",
            "palatini_block": "coframe e_obs",
            "best_MTS_candidate": "q_loc visible candidate: e_obs, g_obs",
            "status": "PARTIAL_CANDIDATE_UNSIGNED",
            "missing_to_promote": "parent coframe descent and no-shadow-frame theorem",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "block_id": "PBM1827_1_omega",
            "palatini_block": "connection omega",
            "best_MTS_candidate": "omega_obs / Gamma_eff",
            "status": "MISSING_COMPATIBILITY_THEOREM",
            "missing_to_promote": "Levi-Civita/spin-connection match or independent-connection residual vector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "block_id": "PBM1827_2_F_LogU",
            "palatini_block": "curvature F and small-loop Log(U)",
            "best_MTS_candidate": "log-holonomy variable named by 1826",
            "status": "MISSING_PARENT_GENERATION",
            "missing_to_promote": "derive F[omega] and U_h from MTS transport/load connection",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "block_id": "PBM1827_3_Bh_Ah",
            "palatini_block": "oriented hinge bivector / area",
            "best_MTS_candidate": "local cell/domain/coframe area element",
            "status": "MISSING_HINGE_OWNER",
            "missing_to_promote": "derive oriented cell hinge and area scaling from MTS parent domain grammar",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "block_id": "PBM1827_4_action",
            "palatini_block": "linear action int e e F or sum A_h delta_h",
            "best_MTS_candidate": "EH fixed-point/minimal action ansatz",
            "status": "REPAIR_ANSATZ_NOT_DERIVATION",
            "missing_to_promote": "derive the action from MTS variables rather than importing EH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "block_id": "PBM1827_5_matter",
            "palatini_block": "universal matter source",
            "best_MTS_candidate": "S_matter[psi,e_obs] contract",
            "status": "MISSING_MATTER_FUNCTOR_THEOREM",
            "missing_to_promote": "prove all ordinary matter/readouts descend through the same observed coframe",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "block_id": "PBM1827_6_total",
            "palatini_block": "Palatini/Regge field match",
            "best_MTS_candidate": "combined q_loc/e_obs/omega_obs/Pi_M/theta candidates",
            "status": "BLOCK_MAP_INCOMPLETE_NONCLAIM",
            "missing_to_promote": "single parent action plus variation and source descent",
            "valid_for_claim": False,
        },
    ]


def obstruction_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1827_0_EH_import",
            "obstruction": "EH/Palatini action import",
            "why_it_matters": "importing the action gives the desired GR limit by assumption, not derivation",
            "resolution": "derive each action block from MTS variables or label it repair ansatz",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1827_1_connection",
            "obstruction": "connection compatibility",
            "why_it_matters": "wrong connection leaves torsion/nonmetricity/preferred-frame/operator residuals",
            "resolution": "prove Gamma_eff=omega[e_obs] or fill independent connection residual rows",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1827_2_hinge",
            "obstruction": "hinge bivector and orientation",
            "why_it_matters": "without B_h/A_h the signed Log(U) cannot become the Regge area-deficit action",
            "resolution": "derive oriented local cell/hinge measure from MTS domain grammar",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1827_3_source",
            "obstruction": "matter/source/Pi_M descent",
            "why_it_matters": "GR reduction needs the same Hilbert source that orbits, clocks, and PPN read",
            "resolution": "prove Pi_M/Hilbert/Noether equality and universal matter coframe descent",
            "retained": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "obstruction_id": "OBS1827_4_trace_norm",
            "obstruction": "trace/norm action remains legal",
            "why_it_matters": "even holonomy energy generates finite c2/R2-fR residuals",
            "resolution": "exclude trace/norm by theorem or fill c2 scalaron map",
            "retained": True,
            "valid_for_claim": False,
        },
    ]


def c2_scalaron_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "map_id": "CSM1827_0_c2_input",
            "quantity": "c2_visible",
            "contract": "finite value or prior for c2_visible = 1/2 Phi''(0)",
            "required_inputs": "parent Phi; normalization; uncertainty; source path",
            "current_status": "MISSING_PARENT_PHI_VALUE",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "CSM1827_1_R2_coefficient",
            "quantity": "c_R2_eff",
            "contract": "c_R2_eff ~ shape_factor * c2_visible * ell_cell^2 / EH_normalization",
            "required_inputs": "ell_cell; shape factor; EH normalization; continuum convention; units",
            "current_status": "MISSING_CELL_SCALE_AND_NORMALIZATION",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "CSM1827_2_scalaron",
            "quantity": "lambda_R2 and alpha_R2",
            "contract": "template scalar-mode map from c_R2_eff to finite range/coupling, modified by MTS matter coupling",
            "required_inputs": "linearized field equations; source coupling; sign/stability; mass; no-tachyon/no-ghost guard",
            "current_status": "MISSING_LINEARIZED_SCALAR_MODE_MAP",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "CSM1827_3_local_observables",
            "quantity": "R10/PPN/clock/orbital residuals",
            "contract": "map scalar mode into alpha(lambda), gamma-1, beta-1, source-normalization and clock rows",
            "required_inputs": "R10 bound curve; PPN response; matter coupling; source normalization; units",
            "current_status": "MISSING_OBSERVABLE_PROJECTION",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "map_id": "CSM1827_4_total",
            "quantity": "finite c2 scalaron branch",
            "contract": "score-ready only if CSM1827_0 through CSM1827_3 are all sourced",
            "required_inputs": "all coefficient, stability, source, and observable maps with source paths",
            "current_status": "C2_SCALARON_MAP_CONTRACT_READY_NONCLAIM",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def local_gr_impact_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1827_0_if_match_closes",
            "if_closed": "e, omega, F/LogU, B_h/A_h, kappa, matter, and variation all match in one MTS parent action",
            "would_buy": "serious Palatini/Regge-to-EH bridge and a strong route to c2_visible=0",
            "still_missing": "higher operators, source-normalized Newton chain, q_loc silence, PPN completion",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1827_1_if_match_fails",
            "if_closed": "field match remains unsigned",
            "would_buy": "honest finite residual/scalaron branch instead of a smuggled GR limit",
            "still_missing": "source-backed c2 and local observable projections",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "impact_id": "LGI1827_2_verdict",
            "if_closed": "1827 alone proves local GR/Newton",
            "would_buy": "nothing claimable alone",
            "still_missing": "the field match fails current corpus",
            "claim_allowed_now": False,
            "valid_for_claim": False,
        },
    ]


def acceptance_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1827_0_field_match_attempt",
            "gate": "Palatini/Regge field-match attempt written",
            "current_status": "PASS_CONTRACT_ONLY",
            "reason": "1827 maps each required block and identifies the blockers",
            "gate_pass": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1827_1_full_match",
            "gate": "full field/action/variation match",
            "current_status": "BLOCKED",
            "reason": "connection, holonomy, hinge, source, and variation owners are unsigned",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "AC1827_2_c2_map",
            "gate": "finite c2 scalaron map score-ready",
            "current_status": "BLOCKED",
            "reason": "coefficient and local observable maps are missing",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1827_0_field_match",
            "claim": "MTS owns Palatini/Regge parent action",
            "status": "BLOCKED",
            "reason": "field map fails current corpus",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1827_1_c2_zero",
            "claim": "c2_visible=0 by linear curvature action",
            "status": "BLOCKED",
            "reason": "linear action owner is not parent-signed",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1827_2_c2_score",
            "claim": "finite c2/R2-fR scalaron branch score-ready",
            "status": "BLOCKED",
            "reason": "c2 value, c_R2 map, scalar mass/coupling and observable projections are missing",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1827_3_local_GR",
            "claim": "local GR/Newton reduction follows",
            "status": "REFUSED",
            "reason": "field match, source, q_loc, PPN, and operator gates remain open",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1827_0_field_match_result",
            "decision": "PALATINI_REGGE_FIELD_MATCH_NOT_CLOSED",
            "reason": "coframe is a candidate, but connection, curvature/holonomy, hinge bivector, source descent and variation are not parent-signed",
            "next_action": "do not promote EH/Regge import or c2 zero",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1827_1_best_derivation_next",
            "decision": "CONNECTION_HINGE_OWNER_NEXT",
            "reason": "the largest new gap is not the coframe; it is the connection-to-holonomy plus oriented hinge/bivector owner",
            "next_action": "try to derive Gamma_eff/omega_obs compatibility and B_h/A_h from MTS cell geometry",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1827_2_fallback",
            "decision": "C2_SCALARON_MAP_NONCLAIM_READY",
            "reason": "if connection/hinge ownership fails, the finite c2 scalaron branch is the honest residual route",
            "next_action": "fill coefficient and local observable maps only with real inputs",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1827_3_best_next",
            "decision": "CONNECTION_HINGE_OWNER_OR_C2_MAP_FILL_NEXT",
            "reason": "1827 reduces the Palatini route to a narrower geometry-owner problem",
            "next_action": "1828-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1827_0_primary",
            "next_target": "1828-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md",
            "script": "scripts/Y5_R2FR_connection_hinge_bivector_owner_or_c2_map_fill.py",
            "objective": "derive Gamma_eff/omega_obs compatibility and the oriented hinge bivector/area from MTS cell geometry; if not, begin filling the finite c2 scalaron map as nonclaim rows",
            "selection_status": "selected",
            "success_condition": "connection and hinge owner signed, or c2 scalaron rows remain valid_for_claim=false with missing inputs explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1827_1_parallel",
            "next_target": "1828b-Y5-R2FR-matter-PiM-Hilbert-source-descent-for-Palatini-branch.md",
            "script": "scripts/Y5_R2FR_matter_PiM_Hilbert_source_descent_for_Palatini_branch.py",
            "objective": "parallel source route after geometry: prove universal matter coframe and Pi_M/Hilbert/Noether charge equality",
            "selection_status": "held_parallel",
            "success_condition": "same-frame source descent and Hamiltonian mass charge are parent-signed or retained as explicit residual rows",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "field_match_attempt": field_match_attempt_rows(),
        "block_map": block_map_rows(),
        "obstruction_ledger": obstruction_ledger_rows(),
        "c2_scalaron_contract": c2_scalaron_contract_rows(),
        "local_gr_impact": local_gr_impact_rows(),
        "acceptance_gate": acceptance_gate_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_csvs(paths: list[Path]) -> None:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            directory.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, directory / path.name)


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            with path.open("r", encoding="utf-8", newline="") as handle:
                list(csv.DictReader(handle))
    except Exception:
        return False
    return True


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    guarded_keys = {"valid_for_claim", "claim_allowed", "score_ready"}
    for rows in rows_map.values():
        for row in rows:
            for key in guarded_keys.intersection(row):
                if str(row[key]).lower() == "true":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    readiness_keys = ["valid_for_claim", "claim_allowed", "score_ready"]
    for rows in rows_map.values():
        for row in rows:
            has_missing = any("MISSING" in str(value) for value in row.values())
            if not has_missing:
                continue
            if any(str(row.get(key, "")).lower() == "true" for key in readiness_keys):
                return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        name = path.name
        if "1827-Y5-R2FR" in name or name.startswith("P8_Y5_PARENT_QLOC_1827") or name.startswith("P8_Y5_BRR545_1827"):
            return False
    return True


def branch_copies_exist(paths: list[Path]) -> bool:
    for path in paths:
        for directory in [MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
            if not (directory / path.name).exists():
                return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]], copied_paths: list[Path]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    output_paths = [OUTPUTS[key] for key in rows_map.keys()]
    checks: list[tuple[str, bool, str]] = [
        ("VAL1827_0_sources_exist", all(str(row["exists"]).lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL1827_1_needles_present", all(str(row["needles_present"]).lower() == "true" for row in source_rows), "all cited source needles are present"),
        ("VAL1827_2_field_match_written", any(row["attempt_id"] == "FMA1827_0_target" for row in rows_map["field_match_attempt"]), "field-match attempt is written"),
        (
            "VAL1827_3_field_match_not_promoted",
            any(
                row["attempt_id"] == "FMA1827_8_verdict"
                and row["current_status"] == "FIELD_MATCH_FAILS_CURRENT_CORPUS"
                and row["valid_for_claim"] is False
                for row in rows_map["field_match_attempt"]
            ),
            "field match fails current corpus and is not promoted",
        ),
        (
            "VAL1827_4_block_map_incomplete",
            any(
                row["block_id"] == "PBM1827_6_total"
                and row["status"] == "BLOCK_MAP_INCOMPLETE_NONCLAIM"
                for row in rows_map["block_map"]
            ),
            "Palatini block map remains incomplete",
        ),
        (
            "VAL1827_5_obstructions_retained",
            all(row["retained"] is True and row["valid_for_claim"] is False for row in rows_map["obstruction_ledger"]),
            "field-match obstructions are retained",
        ),
        (
            "VAL1827_6_c2_scalaron_nonclaim",
            any(
                row["map_id"] == "CSM1827_4_total"
                and row["current_status"] == "C2_SCALARON_MAP_CONTRACT_READY_NONCLAIM"
                and row["score_ready"] is False
                for row in rows_map["c2_scalaron_contract"]
            ),
            "c2 scalaron map contract is nonclaim",
        ),
        (
            "VAL1827_7_local_gr_nonclaim",
            all(row["claim_allowed_now"] is False and row["valid_for_claim"] is False for row in rows_map["local_gr_impact"]),
            "local GR impact rows remain nonclaim",
        ),
        (
            "VAL1827_8_acceptance_blocks",
            any(row["gate_id"] == "AC1827_0_field_match_attempt" and row["gate_pass"] is True and row["claim_allowed"] is False for row in rows_map["acceptance_gate"])
            and all(row["claim_allowed"] is False for row in rows_map["acceptance_gate"]),
            "acceptance gate allows contract-only progress and blocks claims",
        ),
        (
            "VAL1827_9_claim_gates_blocked",
            all(row["gate_pass"] is False and row["valid_for_claim"] is False for row in rows_map["claim_gate"]),
            "all field-match/c2/local-GR claim gates remain blocked or refused",
        ),
        ("VAL1827_10_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1827_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1827_12_decision_next",
            any(
                row["decision_id"] == "DEC1827_3_best_next"
                and row["decision"] == "CONNECTION_HINGE_OWNER_OR_C2_MAP_FILL_NEXT"
                for row in rows_map["decision_ledger"]
            ),
            "decision selects connection/hinge owner or c2 map fill next",
        ),
        (
            "VAL1827_13_next_selected",
            any(row["route_id"] == "NEXT1827_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1827_14_csv_parse", csv_parse_ok(output_paths), "all generated 1827 CSVs parse"),
        ("VAL1827_15_branch_copies", branch_copies_exist(copied_paths), "branch/quarantine/queue copies exist"),
        ("VAL1827_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1827_17_formalization_untouched", no_formalization_outputs(), "no 1827 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1827_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1827 Palatini-Regge field match or c2 scalaron map checkpoint",
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
            "# 1827 Y5 R2FR Palatini Regge field match or c2 scalaron map",
            "",
            "**Progress:** 1827 tests whether the clean Palatini/Regge route can be attached to actual MTS variables. The coframe/metric side has a candidate, but the connection, curvature/holonomy, oriented hinge bivector, source descent, and variation are not yet parent-signed.",
            "",
            "**Current verdict:** the field match fails current corpus, but usefully. The next derivation target is narrower: derive `Gamma_eff/omega_obs` compatibility and the oriented `B_h/A_h` hinge owner from MTS cell geometry. If that fails, the finite `c2_visible -> R2/fR` scalaron map must be filled as a nonclaim residual branch.",
            "",
            "**Claim ceiling:** no Palatini/Regge parent-action claim, no `c2_visible=0` claim, no finite scalaron score, no local GR/Newton promotion, no GitHub action, and no `formalization-workbench` edit is allowed from 1827.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Field Match Attempt",
            markdown_table(rows_map["field_match_attempt"], ["attempt_id", "target", "test", "current_status", "blocker", "claim_allowed", "valid_for_claim"]),
            "",
            "## Palatini Block Map",
            markdown_table(rows_map["block_map"], ["block_id", "palatini_block", "best_MTS_candidate", "status", "missing_to_promote", "valid_for_claim"]),
            "",
            "## Obstruction Ledger",
            markdown_table(rows_map["obstruction_ledger"], ["obstruction_id", "obstruction", "why_it_matters", "resolution", "retained", "valid_for_claim"]),
            "",
            "## C2 Scalaron Map Contract",
            markdown_table(rows_map["c2_scalaron_contract"], ["map_id", "quantity", "contract", "required_inputs", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Local GR Impact",
            markdown_table(rows_map["local_gr_impact"], ["impact_id", "if_closed", "would_buy", "still_missing", "claim_allowed_now", "valid_for_claim"]),
            "",
            "## Acceptance Gate",
            markdown_table(rows_map["acceptance_gate"], ["gate_id", "gate", "current_status", "reason", "gate_pass", "claim_allowed", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason", "gate_pass", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a useful failure. We are not stuck at 'does MTS reduce to GR?' anymore; the immediate geometry question is specific. Can the MTS effective connection and cell/domain geometry supply the same objects that Palatini/Regge uses: a compatible connection, a curvature holonomy, and an oriented area bivector? If yes, the linear-curvature route gets much stronger. If no, the theory still has a disciplined fallback: carry finite `c2_visible` into scalar-mode tests.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = rows_by_key()
    nonvalidation_paths: list[Path] = []
    for key, rows in rows_map.items():
        path = OUTPUTS[key]
        write_csv(path, rows)
        nonvalidation_paths.append(path)
    copy_csvs(nonvalidation_paths)
    validation_rows = build_validation(rows_map, nonvalidation_paths)
    write_csv(OUTPUTS["validation"], validation_rows)
    copy_csvs([OUTPUTS["validation"]])
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1827 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
