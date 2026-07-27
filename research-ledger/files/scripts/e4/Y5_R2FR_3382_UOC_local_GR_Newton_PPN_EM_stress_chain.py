from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"
DOC = ROOT / "3382-Y5-R2FR-UOC-local-GR-Newton-PPN-EM-stress-chain-under-AX1090.md"
RUN_UTC = datetime.now(timezone.utc).isoformat()

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3382_SOURCE_REGISTER.csv",
    "uoc_activation": OUT / "P8_Y5_R2FR_3382_UOC_BRANCH_ACTIVATION_CONTRACT.csv",
    "local_action": OUT / "P8_Y5_R2FR_3382_LOCAL_ACTION_BLOCK_UNDER_UOC.csv",
    "newton_chain": OUT / "P8_Y5_R2FR_3382_NEWTON_SOURCE_NORMALIZATION_CHAIN.csv",
    "ppn_map": OUT / "P8_Y5_R2FR_3382_PPN_RESIDUAL_VECTOR_UNDER_UOC.csv",
    "em_stress": OUT / "P8_Y5_R2FR_3382_EM_POYNTING_HILBERT_STRESS_CHAIN.csv",
    "no_smuggling": OUT / "P8_Y5_R2FR_3382_NO_SMUGGLING_FIREWALL.csv",
    "claim_ladder": OUT / "P8_Y5_R2FR_3382_CLAIM_LADDER.csv",
    "runner": OUT / "P8_Y5_R2FR_3382_RUNNER_NONCLAIM.csv",
    "gates": OUT / "P8_Y5_R2FR_3382_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3382_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3382_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3382_VALIDATION.csv",
}

LOCAL_SOURCES = [
    ("SRC3382_0_3381_doc", ROOT / "3381-Y5-R2FR-MTS-triad-parent-object-language-adoption-or-minimal-coupling-axiom-under-AX1090.md", "3381 UOC/minimal coupling handoff"),
    ("SRC3382_1_3381_axiom", OUT / "P8_Y5_R2FR_3381_MINIMAL_UNIVERSAL_COUPLING_AXIOM.csv", "UOC axiom rows"),
    ("SRC3382_2_3381_chain", OUT / "P8_Y5_R2FR_3381_LOCAL_GR_CHAIN_CONSEQUENCE.csv", "3381 local-GR chain consequence"),
    ("SRC3382_3_3381_nogo", OUT / "P8_Y5_R2FR_3381_SCALAR_TRIAD_NO_GO_COUNTERMODEL.csv", "3381 no-go countermodels"),
    ("SRC3382_4_3380_arena", OUT / "P8_Y5_R2FR_3380_ARENA_PROJECTION_REQUIREMENTS.csv", "3380 WEP/PPN/R10/clock arena projection requirements"),
    ("SRC3382_5_3377_newton", OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv", "3377 weak-field source normalization theorem"),
    ("SRC3382_6_3377_ppn_update", OUT / "P8_Y5_R2FR_3377_NEWTON_PPN_UPDATE_NONCLAIM.csv", "3377 Newton/PPN update"),
    ("SRC3382_7_3375_worldtube", OUT / "P8_Y5_R2FR_3375_WORLDTUBE_SOURCE_MEASURE_SELECTOR_THEOREM.csv", "3375 worldtube source measure selector"),
    ("SRC3382_8_3375_poynting", OUT / "P8_Y5_R2FR_3375_POYNTING_SOURCE_WORLD_TUBE_PLACEMENT.csv", "3375 Poynting source-worldtube placement"),
    ("SRC3382_9_3343_maxwell", OUT / "P8_Y5_R2FR_3343_PUBLIC_MAXWELL_ACTION_DERIVATION.csv", "3343 public Maxwell action derivation"),
    ("SRC3382_10_3343_double_count", OUT / "P8_Y5_R2FR_3343_POYNTING_DOUBLE_COUNT_GUARD.csv", "3343 Poynting double-count guard"),
    ("SRC3382_11_3166_cassini", OUT / "P8_Y5_R2FR_3166_CASSINI_GAMMA_SOURCE_INTAKE.csv", "Cassini PPN gamma source intake"),
    ("SRC3382_12_motion_load_contract", ROOT / "01-motion-load-route-contract.md", "motion-load local route PPN contract"),
    ("SRC3382_13_motion_load_reduction", ROOT / "02-motion-load-local-GR-reduction.md", "conditional gamma/beta reduction"),
    ("SRC3382_14_vacuum_reciprocity", ROOT / "04-vacuum-reciprocity-action-contract.md", "vacuum reciprocity parent-origin attempt"),
]


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def parse_csv(path: Path) -> tuple[bool, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            list(csv.DictReader(handle))
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def parse_text(path: Path) -> tuple[bool, str]:
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True, ""
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._\n"
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines) + "\n"


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source_id, path, role in LOCAL_SOURCES:
        exists = path.exists()
        if not exists:
            parse_ok, parse_error = False, "missing"
        elif path.suffix.lower() == ".csv":
            parse_ok, parse_error = parse_csv(path)
        else:
            parse_ok, parse_error = parse_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "parse_ok": bool_text(parse_ok),
                "role": role,
                "parse_error": parse_error,
                "valid_for_claim": "false",
            }
        )
    return rows


def uoc_activation_rows() -> list[dict[str, str]]:
    return [
        {
            "activation_id": "UOC3382_0_branch_label",
            "branch_clause": "UOC is explicit branch input, not derived theorem",
            "branch_effect": "source-coupling universality is available as a declared local equivalence-principle/minimal-coupling principle",
            "not_allowed": "do not write 'MTS derives universal matter coupling' unless 3383 derives matter ontology",
            "status": "EXPLICIT_AXIOM_BRANCH",
            "valid_for_claim": "false",
        },
        {
            "activation_id": "UOC3382_1_single_geometry",
            "branch_clause": "all local-test matter uses Geom_obs=q(Phi)",
            "branch_effect": "hidden source metric/c_g_b_dis source-frame families are zero in this branch, unless a new parent field is explicitly introduced",
            "not_allowed": "second source coframe, disformal source metric, or arena-dependent source frame",
            "status": "SOURCE_FRAME_LOCKED_BY_AXIOM",
            "valid_for_claim": "false",
        },
        {
            "activation_id": "UOC3382_2_single_measure",
            "branch_clause": "all ordinary matter uses one dmu_obs and observed connection",
            "branch_effect": "species-dependent source measure and source-only weights are disallowed",
            "not_allowed": "w_A S_A, kappa_A T_A, source-only material marker prefactors",
            "status": "SOURCE_WEIGHT_LOCKED_BY_AXIOM",
            "valid_for_claim": "false",
        },
        {
            "activation_id": "UOC3382_3_universal_kappa",
            "branch_clause": "one kappa_MTS=8*pi*G_ref/c^4",
            "branch_effect": "Newtonian source normalization can inherit the same coefficient as the local field equation",
            "not_allowed": "orbital GM backfill, readout-specific G, species-specific G",
            "status": "COEFFICIENT_LOCKED_BY_AXIOM_AND_3377",
            "valid_for_claim": "false",
        },
        {
            "activation_id": "UOC3382_4_variation_before_readout",
            "branch_clause": "arena maps are applied after Hilbert variation",
            "branch_effect": "WEP, PPN, R10, clocks and orbital maps cannot reenter the source action as hidden knobs",
            "not_allowed": "postfit Pi_M, source-worldtube chosen after residual inspection, readout-dependent source current",
            "status": "READOUT_FIREWALL_LOCKED_BY_AXIOM",
            "valid_for_claim": "false",
        },
    ]


def local_action_rows() -> list[dict[str, str]]:
    return [
        {
            "block_id": "ACT3382_0_effective_action",
            "action_block": "S_eff[g_obs,Phi,psi_A,A_Q] = integral dmu_obs[(1/2 kappa_MTS)R[g_obs] + L_MTS_IR(Phi,g_obs) + L_matter(psi_A,e_obs,nabla_obs,A_obs,theta_A) + L_EM(g_obs,A_Q,J_Q)]",
            "uoc_role": "fixes the matter/EM metric, measure and connection",
            "derived_status": "VALID_EFFECTIVE_BRANCH_CONTRACT_NOT_PSI_ONLY_DERIVATION",
            "residual": "R_EH_induction;R_MTS_IR_local_silence;E_UOC_axiom",
            "valid_for_claim": "false",
        },
        {
            "block_id": "ACT3382_1_variation_g",
            "action_block": "delta S_eff/delta g_obs gives G_munu[g_obs] + K_MTS_IR_munu = kappa_MTS(T_matter_munu + T_EM_munu)",
            "uoc_role": "same Hilbert variation defines all ordinary source stress",
            "derived_status": "CONDITIONAL_FIELD_EQUATION",
            "residual": "K_MTS_IR_munu must be zero, higher-order, or PPN-bounded locally",
            "valid_for_claim": "false",
        },
        {
            "block_id": "ACT3382_2_variation_A",
            "action_block": "delta S_EM/delta A_Q gives nabla_mu(lambda_0 F^munu)=J_Q^nu",
            "uoc_role": "EM current lives in same observed geometry/Hodge structure",
            "derived_status": "EXACT_CONDITIONAL_MAXWELL_BRANCH",
            "residual": "epsilon_EM if lambda_0, Hodge star, or current uses hidden frame/background flow",
            "valid_for_claim": "false",
        },
        {
            "block_id": "ACT3382_3_boundary_source",
            "action_block": "M_source[W] = Hamiltonian/Noether charge from the same parent action and worldtube support closure(supp J_H[tau])",
            "uoc_role": "prevents readout-selected mass/worldtube backfill",
            "derived_status": "CONDITIONAL_ON_3375_AND_BOUNDARY_REFERENCE_LOCK",
            "residual": "R_source_measure;R_reference_selector;R_Poynting_worldtube if public EM branch fails",
            "valid_for_claim": "false",
        },
    ]


def newton_chain_rows() -> list[dict[str, str]]:
    return [
        {
            "chain_id": "NEW3382_0_same_kappa",
            "step": "coefficient owner",
            "formula": "kappa_MTS = 8*pi*G_ref/c^4",
            "result_under_UOC": "one fixed parent/effective coefficient, not a source/readout parameter",
            "remaining_gap": "G_ref numerical value remains calibrated, as in GR; EH coefficient derivation from psi remains open",
            "status": "CONDITIONAL_PASS",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "NEW3382_1_same_source",
            "step": "Hilbert source owner",
            "formula": "T_munu = -(2/sqrt(-g_obs)) delta S_matter/delta g_obs^munu",
            "result_under_UOC": "rho_H is the same source in field equation, Hamiltonian charge and Newtonian limit",
            "remaining_gap": "UOC is axiom branch; source measure theorem remains conditional on 3375",
            "status": "CONDITIONAL_PASS",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "NEW3382_2_poisson",
            "step": "weak-field 00 equation",
            "formula": "G_00^(1)=2 nabla^2 Phi_N/c^2, T_00=rho_H c^2 -> nabla^2 Phi_N=4*pi*G_ref*rho_H",
            "result_under_UOC": "Newton/Poisson coefficient follows without orbital GM backfill",
            "remaining_gap": "extra local K_MTS_IR_00 must be zero, higher-order, or bounded",
            "status": "EXACT_CONDITIONAL_ALGEBRA",
            "valid_for_claim": "false",
        },
        {
            "chain_id": "NEW3382_3_gauss_charge",
            "step": "Hamiltonian/Gauss consistency",
            "formula": "Phi_N=-G_ref M_H/r using the same boundary charge normalization",
            "result_under_UOC": "surface mass and volume source use one normalization if boundary reference is locked",
            "remaining_gap": "H_ref/B_ref/source-blind boundary lock remains conditional on 3376/3377",
            "status": "CONDITIONAL_PASS_BOUNDARY_GAP",
            "valid_for_claim": "false",
        },
    ]


def ppn_map_rows() -> list[dict[str, str]]:
    return [
        {
            "ppn_id": "PPN3382_0_gamma_source_side",
            "component": "gamma-1",
            "uoc_effect": "kills source-frame/readout source prefactor contributions to gamma",
            "remaining_mts_effect": "metric response still needs reciprocal/readout ownership or a direct PPN metric solution",
            "current_bound_source": "Cassini gamma intake available",
            "status": "SOURCE_SIDE_CLEAN_SHAPE_CONDITIONAL",
            "valid_for_claim": "false",
        },
        {
            "ppn_id": "PPN3382_1_beta_second_order",
            "component": "beta-1",
            "uoc_effect": "fixes same source normalization entering second-order potentials",
            "remaining_mts_effect": "kappa_v/K_MTS_IR second-order kernel must vanish or be bounded",
            "current_bound_source": "no full beta source row imported here",
            "status": "BETA_LEDGER_OPEN",
            "valid_for_claim": "false",
        },
        {
            "ppn_id": "PPN3382_2_preferred_frame",
            "component": "alpha_1, alpha_2, alpha_3",
            "uoc_effect": "forbids readout-channel source frame as a hidden preferred-frame source",
            "remaining_mts_effect": "motion/time background, memory flow or hidden Hodge/constitutive terms may still induce preferred-frame residuals",
            "current_bound_source": "not filled in 3382",
            "status": "COMPONENT_MAP_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "ppn_id": "PPN3382_3_nonconservative",
            "component": "zeta_i, xi",
            "uoc_effect": "single Hilbert source supports standard conservation if K_MTS_IR is divergence-compatible",
            "remaining_mts_effect": "Bianchi balance requires nabla_mu K_MTS_IR^munu = 0 locally or an explicit exchange current that is PPN-safe",
            "current_bound_source": "not filled in 3382",
            "status": "Bianchi_EXCHANGE_GATE_OPEN",
            "valid_for_claim": "false",
        },
        {
            "ppn_id": "PPN3382_4_local_extra_tensor",
            "component": "K_MTS_IR_munu local residual",
            "uoc_effect": "does not automatically remove extra MTS curvature-memory/local response tensor",
            "remaining_mts_effect": "must prove K_MTS_IR_munu=O(PPN-safe), exact zero in local vacuum, or direct bounded vector",
            "current_bound_source": "local PPN branch still open in prior ledgers",
            "status": "PRIMARY_LOCAL_PPN_BLOCKER_REMAINS",
            "valid_for_claim": "false",
        },
        {
            "ppn_id": "PPN3382_5_ruling",
            "component": "full PPN vector",
            "uoc_effect": "source coupling is no longer the main hidden variable in this branch",
            "remaining_mts_effect": "full PPN vector still needs metric solution or component residual bounds",
            "current_bound_source": "Cassini gamma only covers one projection",
            "status": "NOT_FULL_LOCAL_GR_PASS",
            "valid_for_claim": "false",
        },
    ]


def em_stress_rows() -> list[dict[str, str]]:
    return [
        {
            "em_id": "EM3382_0_public_maxwell_action",
            "claim_piece": "public Maxwell action",
            "formula": "S_EM=-lambda_0/4 int sqrt(-g_obs) F^2 + int sqrt(-g_obs) A_mu J_Q^mu",
            "uoc_effect": "uses same public g_obs/Hodge star as rods/clocks/source variation",
            "status": "EXACT_CONDITIONAL_ACTION_FORM",
            "residual_if_missing": "epsilon_EM_hidden_Hodge",
            "valid_for_claim": "false",
        },
        {
            "em_id": "EM3382_1_hilbert_stress",
            "claim_piece": "EM Hilbert stress",
            "formula": "T_EM^munu=lambda_0(F^mualpha F^nu_alpha - 1/4 g_obs^munu F^2)",
            "uoc_effect": "EM energy density, pressure, radiation stress and Poynting flux gravitate through the same Hilbert source",
            "status": "EXACT_CONDITIONAL_VARIATION",
            "residual_if_missing": "R_Poynting_worldtube",
            "valid_for_claim": "false",
        },
        {
            "em_id": "EM3382_2_poynting_worldtube",
            "claim_piece": "Poynting/source-worldtube placement",
            "formula": "M_source[W]=M_matter+M_EM+M_binding+M_boundary+residuals",
            "uoc_effect": "Poynting is not optional; it is included in T_EM/H_tau or carried as explicit residual",
            "status": "POLICY_LOCK_CONDITIONAL_ON_PUBLIC_EM_BRANCH",
            "residual_if_missing": "R_Poynting_worldtube >= ||S_EM dot n||_L1(B)/|M_H_ref|",
            "valid_for_claim": "false",
        },
        {
            "em_id": "EM3382_3_no_double_count",
            "claim_piece": "double-count guard",
            "formula": "do not add second background/Poynting force if same flux is already in Hilbert T_EM",
            "uoc_effect": "prevents a new hidden fifth-force channel",
            "status": "GUARD_REQUIRED",
            "residual_if_missing": "epsilon_EM_double_count",
            "valid_for_claim": "false",
        },
        {
            "em_id": "EM3382_4_mts_em_origin",
            "claim_piece": "EM-from-MTS origin",
            "formula": "derive A_Q,J_Q,lambda_0/Hodge from MTS or label Maxwell import",
            "uoc_effect": "UOC couples EM stress consistently, but does not by itself derive EM from MTS",
            "status": "ORIGIN_OPEN_NOT_COUPLING_BLOCKER",
            "residual_if_missing": "R_EM_origin",
            "valid_for_claim": "false",
        },
    ]


def no_smuggling_rows() -> list[dict[str, str]]:
    return [
        {
            "firewall_id": "FIRE3382_0_uoc_label",
            "rule": "Every local-GR statement under this branch must say 'under UOC' or 'with explicit universal observed-geometry coupling'.",
            "blocks": "pretending matter coupling was derived from psi",
            "status": "REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "FIRE3382_1_extra_tensor_split",
            "rule": "Separate source-side universality from extra MTS_IR local tensor silence.",
            "blocks": "using UOC to claim K_MTS_IR PPN safety",
            "status": "REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "FIRE3382_2_em_public_or_residual",
            "rule": "EM/Poynting must be in public Hilbert stress or retained as R_Poynting_worldtube.",
            "blocks": "ignoring wave energy or double-counting it as a new background force",
            "status": "REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "firewall_id": "FIRE3382_3_ppn_full_vector",
            "rule": "Cassini gamma or reciprocal gamma=1 shape cannot stand for the full PPN vector.",
            "blocks": "gamma-only local-GR promotion",
            "status": "REQUIRED",
            "valid_for_claim": "false",
        },
    ]


def claim_ladder_rows() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "CLAIM3382_0_allowed_now",
            "claim_level": "private WIP",
            "wording": "Under explicit UOC, the source side of the local GR/Newton branch has a clean Hilbert-source normalization.",
            "evidence": "3381 UOC + 3377 weak-field algebra + 3375 source measure selector",
            "allowed": "true_private_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "claim_id": "CLAIM3382_1_allowed_with_label",
            "claim_level": "draft/theory note",
            "wording": "MTS has an effective local-GR branch if UOC is accepted as an equivalence-principle/minimal-coupling axiom and local MTS_IR residuals are PPN-safe.",
            "evidence": "3382 chain plus explicit residual gates",
            "allowed": "true_with_axiom_and_residual_warning",
            "valid_for_claim": "false",
        },
        {
            "claim_id": "CLAIM3382_2_not_allowed",
            "claim_level": "public strong claim",
            "wording": "MTS fully derives local GR including universal matter coupling and PPN safety.",
            "evidence": "not available",
            "allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def runner_rows() -> list[dict[str, str]]:
    return [
        {
            "run_id": "RUN3382_0_uoc_source_side",
            "test": "does UOC close source-prefactor ambiguity",
            "result": "PASS_UNDER_EXPLICIT_AXIOM",
            "detail": "single geometry/measure/kappa/variation-before-readout removes hidden source weights in this branch",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3382_1_newton",
            "test": "does Newton/Poisson normalization follow",
            "result": "PASS_CONDITIONAL_ALGEBRA",
            "detail": "3377 weak-field algebra follows with same Hilbert source and kappa_MTS",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3382_2_ppn",
            "test": "does full local PPN pass follow",
            "result": "FAIL_FULL_VECTOR_STILL_OPEN",
            "detail": "UOC fixes source side but K_MTS_IR/local response and beta/preferred-frame/nonconservative components still need derivation or bounds",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3382_3_em_stress",
            "test": "does EM/Poynting enter source consistently",
            "result": "PASS_CONDITIONAL_PUBLIC_MAXWELL_BRANCH",
            "detail": "public Maxwell action gives Hilbert T_EM and Poynting flux in source charge; hidden Hodge/direct vertices remain residuals",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "run_id": "RUN3382_4_firewall",
            "test": "does checkpoint prevent overclaim",
            "result": "PASS_CLAIM_FIREWALL",
            "detail": "branch is labelled as UOC; local-GR full claim remains blocked",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def gate_rows(source_ok: bool) -> list[dict[str, str]]:
    return [
        {
            "gate_id": "GATE3382_0_sources",
            "claim": "all 3382 source paths exist and parse",
            "gate_pass": bool_text(source_ok),
            "reason": "source register validates UOC, Newton, PPN and EM stress inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3382_1_source_side",
            "claim": "source-prefactor ambiguity is closed in UOC branch",
            "gate_pass": "true",
            "reason": "closed by explicit UOC, not by pure derivation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3382_2_newton",
            "claim": "Newton/Poisson source normalization follows under UOC",
            "gate_pass": "true",
            "reason": "same kappa_MTS and same Hilbert source give 3377 algebra",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3382_3_em_stress",
            "claim": "EM/Poynting source stress is consistently placed under public Maxwell branch",
            "gate_pass": "true",
            "reason": "3343/3375 public-Hodge route includes T_EM and Poynting in Hilbert/Hamiltonian source",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3382_4_full_ppn",
            "claim": "full PPN vector passes",
            "gate_pass": "false",
            "reason": "extra MTS_IR tensor/local response and beta/preferred-frame/nonconservative components remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "gate_id": "GATE3382_5_derived_local_gr",
            "claim": "local GR is fully derived from MTS without extra axiom",
            "gate_pass": "false",
            "reason": "UOC is explicit axiom branch and full PPN remains open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC3382_0_progress",
            "decision": "UOC is a useful bridge, not a final derivation.",
            "because": "It makes source coupling, Newton normalization and EM stress placement clean without hiding the coupling assumption.",
            "next_action": "now attack the extra MTS_IR local PPN tensor rather than source-prefactor ambiguity",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3382_1_ppn_status",
            "decision": "Full local PPN remains the main blocker.",
            "because": "UOC does not prove K_MTS_IR_munu is locally zero/safe, nor does it fill beta, alpha_i, zeta_i and xi.",
            "next_action": "derive a residual vector under UOC and decide zero theorem vs bound runner",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3382_2_em_status",
            "decision": "Poynting vector concern is properly handled in the clean branch.",
            "because": "Public Maxwell/Hodge route includes EM energy flux in Hilbert stress; hidden/direct EM vertices remain explicit residuals.",
            "next_action": "do not add a separate Poynting force unless a parent vertex and subtraction rule are derived",
            "valid_for_claim": "false",
        },
    ]


def next_rows() -> list[dict[str, str]]:
    return [
        {
            "target_id": "3383-Y5-R2FR-UOC-extra-MTSIR-local-PPN-residual-vector-or-zero-theorem-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3383_UOC_extra_MTSIR_local_PPN_residual_vector_or_zero_theorem.py",
            "objective": "under explicit UOC, isolate the remaining K_MTS_IR local tensor/residual vector and try to prove it vanishes through PPN order or build finite PPN bound rows",
            "why_next": "3382 closes source-side ambiguity under an axiom, leaving extra MTS local-response safety as the real local-GR blocker",
            "valid_for_claim": "false",
        },
        {
            "target_id": "3384-Y5-R2FR-matter-ontology-from-MTS-excitations-or-UOC-demotion-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3384_matter_ontology_from_MTS_excitations_or_UOC_demotion.py",
            "objective": "try to derive UOC from matter-as-MTS-excitation ontology; if not, keep UOC as a declared equivalence-principle axiom",
            "why_next": "parallel deeper derivation route for eventually removing the UOC axiom label",
            "valid_for_claim": "false",
        },
    ]


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    offenders: list[str] = []
    for path in paths:
        if not path.exists() or path.suffix.lower() != ".csv":
            continue
        for index, row in enumerate(read_csv_rows(path), start=2):
            if "valid_for_claim" in row and row["valid_for_claim"].strip().lower() != "false":
                offenders.append(f"{path.name}:line{index}:{row['valid_for_claim']}")
    return not offenders, "; ".join(offenders)


def validate(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in rows_by_name["source_register"])
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation" and path.suffix.lower() == ".csv"]
    parse_results = [parse_csv(path)[0] for path in output_csvs if path.exists()]
    flags_ok, flag_detail = all_claim_flags_false(output_csvs)
    formalization_hits = [
        hit
        for hit in FW.rglob("*3382*")
        if hit.name.startswith(("3382-Y5", "P8_Y5_R2FR_3382", "P8_Y5_BRR545_3382", "Y5_R2FR_3382"))
    ] if FW.exists() else []
    uoc_ids = {row["activation_id"] for row in rows_by_name["uoc_activation"]}
    action_ids = {row["block_id"] for row in rows_by_name["local_action"]}
    newton_ids = {row["chain_id"] for row in rows_by_name["newton_chain"]}
    ppn_statuses = {row["status"] for row in rows_by_name["ppn_map"]}
    em_ids = {row["em_id"] for row in rows_by_name["em_stress"]}
    firewall_ids = {row["firewall_id"] for row in rows_by_name["no_smuggling"]}
    runner_results = {row["result"] for row in rows_by_name["runner"]}
    gate_map = {row["gate_id"]: row["gate_pass"] for row in rows_by_name["gates"]}
    checks = [
        ("VAL3382_0_sources_exist_parse", "all cited 3382 source paths exist and parse", source_ok, ""),
        ("VAL3382_1_outputs_parse", "all generated CSV outputs parse cleanly", len(parse_results) == len(output_csvs) and all(parse_results), f"parsed={sum(1 for ok in parse_results if ok)} expected={len(output_csvs)}"),
        ("VAL3382_2_uoc_activation", "UOC activation covers branch label, geometry, measure, kappa and variation-before-readout", {"UOC3382_0_branch_label", "UOC3382_1_single_geometry", "UOC3382_2_single_measure", "UOC3382_3_universal_kappa", "UOC3382_4_variation_before_readout"}.issubset(uoc_ids), ""),
        ("VAL3382_3_action_block", "action block covers effective action, metric variation, Maxwell variation and boundary source", {"ACT3382_0_effective_action", "ACT3382_1_variation_g", "ACT3382_2_variation_A", "ACT3382_3_boundary_source"}.issubset(action_ids), ""),
        ("VAL3382_4_newton_chain", "Newton chain covers kappa, Hilbert source, Poisson and Gauss charge", {"NEW3382_0_same_kappa", "NEW3382_1_same_source", "NEW3382_2_poisson", "NEW3382_3_gauss_charge"}.issubset(newton_ids), ""),
        ("VAL3382_5_ppn_map_blocks_full_claim", "PPN map distinguishes source-side cleanup from remaining full-vector blocker", "PRIMARY_LOCAL_PPN_BLOCKER_REMAINS" in ppn_statuses and "NOT_FULL_LOCAL_GR_PASS" in ppn_statuses, ""),
        ("VAL3382_6_em_stress", "EM stress covers public Maxwell action, Hilbert stress, Poynting worldtube, double-count guard and EM-origin gap", {"EM3382_0_public_maxwell_action", "EM3382_1_hilbert_stress", "EM3382_2_poynting_worldtube", "EM3382_3_no_double_count", "EM3382_4_mts_em_origin"}.issubset(em_ids), ""),
        ("VAL3382_7_no_smuggling", "firewall covers UOC label, extra tensor split, EM public/residual and full PPN vector", {"FIRE3382_0_uoc_label", "FIRE3382_1_extra_tensor_split", "FIRE3382_2_em_public_or_residual", "FIRE3382_3_ppn_full_vector"}.issubset(firewall_ids), ""),
        ("VAL3382_8_runner", "runner passes UOC/Newton/EM conditionally but fails full PPN vector", {"PASS_UNDER_EXPLICIT_AXIOM", "PASS_CONDITIONAL_ALGEBRA", "FAIL_FULL_VECTOR_STILL_OPEN", "PASS_CONDITIONAL_PUBLIC_MAXWELL_BRANCH", "PASS_CLAIM_FIREWALL"}.issubset(runner_results), ""),
        ("VAL3382_9_gates", "gates pass source/Newton/EM and block full PPN/derived local GR", gate_map.get("GATE3382_1_source_side") == "true" and gate_map.get("GATE3382_2_newton") == "true" and gate_map.get("GATE3382_3_em_stress") == "true" and gate_map.get("GATE3382_4_full_ppn") == "false" and gate_map.get("GATE3382_5_derived_local_gr") == "false", ""),
        ("VAL3382_10_no_overclaim_flags", "all generated rows with valid_for_claim remain false", flags_ok, flag_detail),
        ("VAL3382_11_next_target", "next target moves to UOC extra-MTSIR local PPN residual vector or zero theorem", rows_by_name["next"][0]["target_id"].startswith("3383-Y5-R2FR-UOC-extra-MTSIR"), ""),
        ("VAL3382_12_write_scope_outside_formalization", "no 3382 files were written under formalization-workbench", not formalization_hits, f"hits={len(formalization_hits)}"),
    ]
    checks.append(("VAL3382_13_overall", "3382 validation overall", all(passed for _, _, passed, _ in checks), "all required checks passed" if all(passed for _, _, passed, _ in checks) else "one or more checks failed"))
    return [{"check_id": check_id, "check": check, "passed": bool_text(passed), "detail": detail} for check_id, check, passed, detail in checks]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3382 - Y5/R2FR UOC local-GR Newton PPN EM stress chain under AX1090",
        "",
        "## Summary",
        "- 3382 pushes the explicit UOC branch through the local source-coupling stack instead of pretending UOC was derived.",
        "- Result: source side improves sharply. Under UOC there is one observed geometry, one measure, one Hilbert source, one `kappa_MTS`, and variation-before-readout.",
        "- Newton result: with 3377, the Poisson/Newton normalization follows conditionally from the same `kappa_MTS=8*pi*G_ref/c^4` and the same Hilbert source. `G_ref` remains a calibrated universal constant, as in GR, not a per-source backfill.",
        "- EM result: public Maxwell/Hodge branch places EM stress and Poynting flux inside Hilbert stress/Hamiltonian source. If EM uses hidden Hodge/background vertices, it becomes an explicit residual.",
        "- PPN result: not passed. UOC cleans source coupling, but it does not prove the extra local MTS tensor `K_MTS_IR` is zero or PPN-safe, and it does not fill the full beta/preferred-frame/nonconservative vector.",
        "- Best next strike: under UOC, isolate the remaining extra-MTS local PPN residual vector and try a zero theorem before falling back to finite bounds.",
        "",
        "## Source Register",
        md_table(rows_by_name["source_register"]),
        "## UOC Branch Activation Contract",
        md_table(rows_by_name["uoc_activation"]),
        "## Local Action Block Under UOC",
        md_table(rows_by_name["local_action"]),
        "## Newton Source Normalization Chain",
        md_table(rows_by_name["newton_chain"]),
        "## PPN Residual Vector Under UOC",
        md_table(rows_by_name["ppn_map"]),
        "## EM/Poynting Hilbert Stress Chain",
        md_table(rows_by_name["em_stress"]),
        "## No-smuggling Firewall",
        md_table(rows_by_name["no_smuggling"]),
        "## Claim Ladder",
        md_table(rows_by_name["claim_ladder"]),
        "## Nonclaim Runner",
        md_table(rows_by_name["runner"]),
        "## Promotion Gates",
        md_table(rows_by_name["gates"]),
        "## Decision Ledger",
        md_table(rows_by_name["decision"]),
        "## Validation",
        md_table(rows_by_name["validation"]),
        "## Next Target",
        md_table(rows_by_name["next"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_register = source_rows()
    source_ok = all(row["exists"] == "true" and row["parse_ok"] == "true" for row in source_register)
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register,
        "uoc_activation": uoc_activation_rows(),
        "local_action": local_action_rows(),
        "newton_chain": newton_chain_rows(),
        "ppn_map": ppn_map_rows(),
        "em_stress": em_stress_rows(),
        "no_smuggling": no_smuggling_rows(),
        "claim_ladder": claim_ladder_rows(),
        "runner": runner_rows(),
        "gates": gate_rows(source_ok),
        "decision": decision_rows(),
        "next": next_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    rows_by_name["validation"] = validate(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print(f"Generated UTC {RUN_UTC}")


if __name__ == "__main__":
    main()
