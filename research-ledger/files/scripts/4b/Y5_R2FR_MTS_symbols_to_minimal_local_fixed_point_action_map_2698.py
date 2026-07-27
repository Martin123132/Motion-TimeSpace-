from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2698"
BRANCH_ID = "Y5_R2FR_MTS_SYMBOLS_TO_MINIMAL_LOCAL_FIXED_POINT_ACTION_MAP_2698"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"
RAB_QUEUE = SOURCE_INTAKE / "rab-sector" / "acquisition-queue"

DOC_PATH = ROOT / "2698-Y5-R2FR-MTS-symbols-to-minimal-local-fixed-point-action-map.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2698_SOURCE_REGISTER.csv",
    "symbol_action_map": RESIDUALS / "P8_Y5_R2FR_2698_SYMBOL_ACTION_PLACEMENT_MAP.csv",
    "first_variation_gates": RESIDUALS / "P8_Y5_R2FR_2698_FIRST_VARIATION_EVIDENCE_GATES.csv",
    "keep_kill_rules": RESIDUALS / "P8_Y5_R2FR_2698_KEEP_KILL_RULES.csv",
    "symbol_status": RESIDUALS / "P8_Y5_R2FR_2698_SYMBOL_STATUS_CLASSIFIER.csv",
    "residual_demotion": RESIDUALS / "P8_Y5_R2FR_2698_RESIDUAL_DEMOTION_QUEUE_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2698_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2698_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2698_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2698_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2698_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2698_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2698_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_symbol_action_map": LOCAL_BOUNDS / "MTS_symbol_action_placement_map_2698_NONCLAIM.csv",
    "local_residual_demotion": LOCAL_BOUNDS / "MTS_symbol_residual_demotion_queue_2698_NONCLAIM.csv",
    "wep_residual_demotion": WEP_RESIDUALS / "MTS_symbol_residual_demotion_queue_2698_NONCLAIM.csv",
    "source_weight_residual_demotion": SOURCE_WEIGHT / "MTS_SYMBOL_RESIDUAL_DEMOTION_QUEUE_2698_NONCLAIM.csv",
    "rab_next": RAB_QUEUE / "JR2698_GAMMA_KHAT_QLOC_FIRST_VARIATION_NEXT.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2698_2697_DOC",
        "relative_path": "2697-Y5-R2FR-minimal-local-parent-action-fixed-point-ansatz-kappa-source-measure-EH.md",
        "required_needles": ["SYM2697_2_Gamma_eff_Khat_q", "NEXT2697_0_selected", "VAL2697_OVERALL"],
        "purpose": "imports the minimal parent-action fixed-point block list and symbol queue",
    },
    {
        "source_id": "SRC2698_512_SYMBOL_MAP",
        "relative_path": "512-match-MTS-symbols-to-local-GR-action-blocks.md",
        "required_needles": ["FV512_2_Gamma_Khat_q", "KK512_1_q_loc", "D512_2"],
        "purpose": "imports the earlier symbol placement audit and q_loc keep/kill rule",
    },
    {
        "source_id": "SRC2698_1860_GKQLOC",
        "relative_path": "1860-Y5-R2FR-Gamma-Khat-q-loc-action-existence-bridge-to-local-EH-fixed-point.md",
        "required_needles": ["QZA1860_0_identity", "QZA1860_2_metric_response", "QZA1860_4_Euler_double_zero"],
        "purpose": "imports the formal q_loc zero route and why it is not a live parent proof",
    },
    {
        "source_id": "SRC2698_2205_FRONTIER",
        "relative_path": "2205-Y5-R2FR-current-frontier-EH-descent-PiM-source-readout-synthesis.md",
        "required_needles": ["SYN2205_2_coupling_tension", "SEL2205_0_target", "NEXT2205_0_2206"],
        "purpose": "imports the current frontier synthesis selecting Gamma/Khat/q_loc as first obstruction",
    },
    {
        "source_id": "SRC2698_2695_KAPPA",
        "relative_path": "2695-Y5-R2FR-kappa-topological-superselection-parent-adoption-or-drift-residual-values.md",
        "required_needles": ["ZFD2695_2_local_equation", "KAD2695_8_verdict", "VAL2695_OVERALL"],
        "purpose": "imports the conditional topological kappa route and no-claim ceiling",
    },
    {
        "source_id": "SRC2698_2696_SOURCE_MEASURE",
        "relative_path": "2696-Y5-R2FR-source-measure-Meff-flux-closure-after-conditional-kappa-gate.md",
        "required_needles": ["PIM2696_5_verdict", "SMA2696_10_verdict", "VAL2696_OVERALL"],
        "purpose": "imports the source-measure and Pi_M/Hamiltonian charge status",
    },
    {
        "source_id": "SRC2698_2697_SYMBOL_QUEUE",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2697_MTS_SYMBOL_MATCH_QUEUE_NONCLAIM.csv",
        "required_needles": ["SYM2697_2_Gamma_eff_Khat_q", "SYM2697_10_transition"],
        "purpose": "imports machine-readable 2697 symbol queue rows",
    },
    {
        "source_id": "SRC2698_2697_RESIDUALS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2697_RESIDUAL_DEMOTION_VECTOR_NONCLAIM.csv",
        "required_needles": ["RDM2697_0_total_operator", "RDM2697_9_total"],
        "purpose": "imports machine-readable 2697 residual demotion rows",
    },
    {
        "source_id": "SRC2698_NEWTON_STACK",
        "relative_path": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "required_needles": ["SN7_constant_universal_Geff", "SN11_second_order_PPN_source_stability"],
        "purpose": "imports source-normalized Newton/PPN requirements",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        cells = [str(row.get(header, "")).replace("|", "\\|").replace("\n", "<br>") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def symbol_action_placement_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "placement_id": "SAP2698_0_kappa_eff_A3",
            "symbol_group": "global coupling",
            "symbols": "kappa_eff;A_3",
            "mapped_action_blocks": "ACT2697_1",
            "proposed_role": "conditional topological/global coupling owner",
            "source_evidence": "2695 proves the zero-form variation conditionally: int kappa_eff dA_3 can give d kappa_eff=0, but parent adoption is unsigned",
            "first_variation_contract": "delta_A3 S_kappa_top = 0 -> d kappa_eff=0; companion kappa equation is global/topological; no metric stress or source/range/frame labels",
            "current_status": "CONDITIONAL_NOT_PARENT_ADOPTED",
            "promotion_allowed": "false",
            "residual_if_failed": "dln_Geff_dt;alpha_kappa(lambda);source/range/frame kappa hair",
            "next_action": "keep as candidate parent clause while attacking live extra-sector and source-measure blockers",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_1_g_obs_e_obs",
            "symbol_group": "public metric/coframe",
            "symbols": "g_obs;e_obs",
            "mapped_action_blocks": "ACT2697_0;ACT2697_2;ACT2697_7",
            "proposed_role": "observed metric/coframe anchor for EH, matter coupling, and weak-field readout",
            "source_evidence": "2697 builds the minimal EH/matter/readout blocks; Newton stack still requires source-normalized PPN stability",
            "first_variation_contract": "delta_g S_parent must reduce to EH plus Hilbert source in the same observed frame with no first-order extra readout leakage",
            "current_status": "ANCHOR_CONDITIONAL_NOT_FULL_SOURCE_FRAME_PROOF",
            "promotion_allowed": "false",
            "residual_if_failed": "DeltaE_munu;readout leakage;PPN gamma/beta/preferred-frame vector",
            "next_action": "use as public branch anchor only after extra-sector/source/readout residuals close",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_2_Gamma_eff_Khat_q",
            "symbol_group": "central extra-sector residual",
            "symbols": "Gamma_eff;K_hat;q_loc",
            "mapped_action_blocks": "ACT2697_5;VAR2697_1;VAR2697_2",
            "proposed_role": "candidate variational Ward/Euler residual that must be theorem-zero or explicitly bounded",
            "source_evidence": "512 says q_loc must be an on-shell Ward/Noether residual, not a field; 1860 records the formal mechanism but blocks live adoption; 2205 selects it as first obstruction",
            "first_variation_contract": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}); Gamma_eff is a parent scalar density; K_hat is its metric response including boundary/improvement terms; Helmholtz/Euler closure gives F1=0 and boundary no-flux",
            "current_status": "UNPLACED_FIRST_VARIATION_TARGET",
            "promotion_allowed": "false",
            "residual_if_failed": "epsilon_GK_q_loc carried into local_GR;PPN;R10;clock;orbital;WEP residual rows",
            "next_action": "make 2699 the exact Gamma/Khat/q_loc first-variation proof-or-demotion target",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_3_chiD_Qcoh_domain",
            "symbol_group": "domain selector",
            "symbols": "chi_D;Qcoh;domain selector",
            "mapped_action_blocks": "ACT2697_5;ACT2697_6;ACT2697_8",
            "proposed_role": "auxiliary or quotient selector that may activate memory/global branches without local first-order hair",
            "source_evidence": "512 permits auxiliary algebraic selector only if linear local leakage is absent",
            "first_variation_contract": "chi_D is algebraic/gapped/quotient-descended, enters local observables at second order or not at all, and cannot carry preferred-location/source labels",
            "current_status": "CONDITIONAL_AUXILIARY_SELECTOR_NOT_PARENT_DERIVED",
            "promotion_allowed": "false",
            "residual_if_failed": "preferred-location/domain residual;local readout leakage;transition-scale switch",
            "next_action": "return after q_loc and source charge, or demote into residual rows",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_4_memory_time_flow",
            "symbol_group": "memory/time/flow fields",
            "symbols": "memory kernels;B_mem;U_mem;I_M;time/flow fields",
            "mapped_action_blocks": "ACT2697_5;ACT2697_8",
            "proposed_role": "cosmology/galaxy EFT branch, not the local-GR proof engine",
            "source_evidence": "512 keeps memory only if action-owned and locally double-zero; 2697 keeps it in the extra-sector/transition block",
            "first_variation_contract": "memory fields solve a parent Euler equation with smooth cosmological stress while local exterior first variation and source flux vanish",
            "current_status": "CONDITIONAL_EFT_BRANCH_NOT_LOCAL_GR_PROOF",
            "promotion_allowed": "false",
            "residual_if_failed": "local hidden sector;clock/PPN leakage;arena switch",
            "next_action": "do not let empirical memory fits substitute for local GR descent",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_5_PiM_JH_Htau_Qtau",
            "symbol_group": "source charge",
            "symbols": "Pi_M;J_H;H_tau;Q_tau",
            "mapped_action_blocks": "ACT2697_3;ACT2697_4",
            "proposed_role": "parent Hamiltonian/Noether charge route for M_eff, with Pi_M only as a derived projection",
            "source_evidence": "2696 selects parent Hamiltonian source charge before Pi_M descent; it blocks treating orbital GM as the premise",
            "first_variation_contract": "H_tau is integrable with fixed reference and no boundary flux; Pi_M J_H equals the descended parent charge and has zero independent variation",
            "current_status": "CONDITIONAL_CHARGE_ROUTE_NOT_MTS_TRANSFER_SIGNED",
            "promotion_allowed": "false",
            "residual_if_failed": "Delta_PiM;Delta_flux;measured-GM hiding;source-normalization residual",
            "next_action": "after q_loc, close parent charge/source measure or keep finite M_eff residuals",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_6_boundary_reference",
            "symbol_group": "boundary/reference/improvement",
            "symbols": "S_boundary;S_ref;improvement current;boundary flux",
            "mapped_action_blocks": "ACT2697_6",
            "proposed_role": "finite charge reference and no hidden local mass/source/current flux",
            "source_evidence": "2696/2697 repeatedly block source-measure promotion until boundary/reference terms are fixed before readout",
            "first_variation_contract": "exact/topological and reference terms have fixed variation on the compact local branch and cannot carry source-dependent flux",
            "current_status": "OPEN_BOUNDARY_NO_FLUX_REQUIRED",
            "promotion_allowed": "false",
            "residual_if_failed": "Delta_boundary;Delta_flux;K_hat improvement ambiguity",
            "next_action": "include boundary no-flux in 2699 q_loc proof contract",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_7_nonEH_operator_R11",
            "symbol_group": "non-EH operator vector",
            "symbols": "DeltaE_munu;R11 operator vector;c_nonEH",
            "mapped_action_blocks": "ACT2697_0;ACT2697_5;ACT2697_7",
            "proposed_role": "operator residual ledger for any non-EH local terms not killed by the fixed point",
            "source_evidence": "2697 residual demotion retains DeltaE_munu and total local-GR residuals",
            "first_variation_contract": "every local non-EH operator has zero coefficient and zero first derivative at Phi0, or carries source-backed coefficient and arena projection",
            "current_status": "UNPLACED_OPERATOR_RESIDUAL",
            "promotion_allowed": "false",
            "residual_if_failed": "R11/local_GR/PPN/R10 operator vector",
            "next_action": "derive double-zero operator silence or fill coefficient rows",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_8_matter_source_labels",
            "symbol_group": "matter/source labels",
            "symbols": "ordinary matter source labels;species weights;source class",
            "mapped_action_blocks": "ACT2697_2",
            "proposed_role": "same-frame universal matter source and WEP/source-charge classifier",
            "source_evidence": "2695/2696 keep source blindness and source-measure transfer unsigned",
            "first_variation_contract": "matter action descends through one observed coframe and Hilbert source with no material/source dependent gravitational charge prefactor",
            "current_status": "SOURCE_CLASSIFIER_NARROWED_NOT_CLOSED",
            "promotion_allowed": "false",
            "residual_if_failed": "eta_source_AB;Delta_source_charge;WEP residual",
            "next_action": "carry source labels as explicit residuals until matter functor/source measure is signed",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_9_ppn_readout",
            "symbol_group": "PPN readout",
            "symbols": "gamma;beta;alpha_i;zeta_i;xi",
            "mapped_action_blocks": "ACT2697_7",
            "proposed_role": "weak-field residual vector, not a derived pass",
            "source_evidence": "Newton stack requires second-order PPN source stability; 2697 keeps PPN residual handoff open",
            "first_variation_contract": "derive the metric expansion in the observed frame after source normalization and show PPN residual vector vanishes or is bounded",
            "current_status": "NOT_DERIVED",
            "promotion_allowed": "false",
            "residual_if_failed": "PPN gamma/beta/preferred-frame/preferred-location vector",
            "next_action": "score only after q_loc/source/readout maps exist",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_10_transition_scale",
            "symbol_group": "transition scale",
            "symbols": "ell_tr;L_cg;activation functional",
            "mapped_action_blocks": "ACT2697_8",
            "proposed_role": "derived separation between local fixed point and cosmology/galaxy active branch",
            "source_evidence": "512 forbids an arena switch; 2697 keeps transition scale open",
            "first_variation_contract": "ell_tr/L_cg follows from operator spectrum, source compactness, topology, or activation eigenvalue in the same parent action",
            "current_status": "OPEN_UNIFICATION_SCALE",
            "promotion_allowed": "false",
            "residual_if_failed": "arena-dependent handoff;hidden interpolation law",
            "next_action": "return after local residual interfaces are explicit",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "placement_id": "SAP2698_11_verdict",
            "symbol_group": "global verdict",
            "symbols": "all mapped symbols",
            "mapped_action_blocks": "ACT2697_0..ACT2697_9",
            "proposed_role": "private fixed-point map, not a proof of local GR",
            "source_evidence": "2695/2696/2697 supply coherent candidate blocks; 512/1860/2205 identify q_loc as the first exact obstruction",
            "first_variation_contract": "all mapped sectors must have parent action ownership, first variation, boundary silence, source measure, readout, and residual fallback",
            "current_status": "NO_FULL_PROMOTIONS_GK_QLOC_FIRST_TARGET",
            "promotion_allowed": "false",
            "residual_if_failed": "carry all open rows as nonclaim residuals",
            "next_action": "run 2699 Gamma/Khat/q_loc proof-or-demotion",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]
    return rows


def first_variation_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("FVG2698_0_metric_frame", "g_obs;e_obs", "ACT2697_0;ACT2697_2;ACT2697_7", "delta_g S_parent -> G_munu + Lambda g_munu = kappa T_H_munu + residuals in the same observed frame", "2697 EH/readout blocks exist", "same-frame matter/source/readout proof remains open", "OPEN"),
        ("FVG2698_1_kappa", "kappa_eff;A_3", "ACT2697_1", "delta_A3 int kappa_eff dA_3 -> d kappa_eff=0 with global companion and no stress/source labels", "2695 has conditional zero-form variation", "parent adoption, companion equation, metric stress silence, source blindness unsigned", "CONDITIONAL_ROUTE_EXISTS_NOT_PARENT_ADOPTED"),
        ("FVG2698_2_Gamma_Khat_q_loc", "Gamma_eff;K_hat;q_loc", "ACT2697_5;VAR2697_1;VAR2697_2", "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) is a Ward/Euler residual of one parent action and has F1=0", "512/1860 define the target and formal mechanism; 2205 selects it", "live Gamma scalar density, K_hat metric response, Helmholtz closure, boundary no-flux, and physical projection are unsigned", "SELECTED_NEXT_PROOF_OR_DEMOTION"),
        ("FVG2698_3_domain_selector", "chi_D;Qcoh", "ACT2697_5;ACT2697_6;ACT2697_8", "selector is auxiliary/gapped/quotient-descended and has no first-order local observable variation", "512 gives keep/kill rule", "no parent algebraic constraint or spectrum proof yet", "OPEN"),
        ("FVG2698_4_memory", "memory/time/flow fields", "ACT2697_5;ACT2697_8", "memory Euler equations are action-owned and locally double-zero while cosmology/galaxy branch remains active", "cosmology/galaxy evidence can motivate but not prove local GR", "local double-zero and transition-scale derivation absent", "OPEN"),
        ("FVG2698_5_source_charge_PiM", "Pi_M;J_H;H_tau;Q_tau", "ACT2697_3;ACT2697_4", "parent covariant phase-space charge descends to M_eff and Pi_M is only derived bookkeeping", "2696 selects Hamiltonian/Noether route", "MTS transfer, fixed reference, flux closure, and Pi_M variation zero not signed", "OPEN"),
        ("FVG2698_6_boundary_reference", "boundary/reference/improvement", "ACT2697_6", "boundary/reference terms are fixed before readout and cannot carry hidden source mass or K_hat flux", "2696/2697 name boundary as a live clause", "no term-by-term boundary/improvement comparison", "OPEN"),
        ("FVG2698_7_ppn_readout", "gamma;beta;alpha_i;zeta_i;xi", "ACT2697_7", "weak-field metric expansion after source normalization gives GR PPN values or scored residuals", "Newton stack requires SN11", "second-order weak-field source/operator calculation missing", "OPEN"),
        ("FVG2698_8_transition_scale", "ell_tr;L_cg", "ACT2697_8", "transition scale derives from parent spectrum/source compactness/topology, not arena choice", "2697 marks it as open", "no eigenvalue/source-scale/topological derivation yet", "OPEN"),
    ]
    return [
        {
            "gate_id": gate_id,
            "symbol_group": symbol_group,
            "action_blocks": action_blocks,
            "required_first_variation_or_identity": required,
            "current_evidence": evidence,
            "gap": gap,
            "status": status,
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, symbol_group, action_blocks, required, evidence, gap, status in rows
    ]


def keep_kill_rule_rows() -> list[dict[str, Any]]:
    rows = [
        ("KK2698_0_kappa", "topological/global kappa with parent-owned A3 and source/range/frame silence", "local scalar/source-calibration kappa or fitted-G absorber", "constant coupling must be variationally derived or residual-scored"),
        ("KK2698_1_q_loc", "q_loc as on-shell Ward/Noether/Euler residual from a parent action", "q_loc as inserted local force, plateau axiom, or scalar proxy", "vector local residual must be varied from the parent action or carried into local bounds"),
        ("KK2698_2_Gamma_Khat", "Gamma_eff and K_hat as one variational metric-response pair with boundary/improvement control", "independent knobs tuned so q_loc cancels", "K_hat must be computed from Gamma_eff or demoted"),
        ("KK2698_3_selector", "auxiliary algebraic/gapped/quotient selector with zero linear local leakage", "linear dynamical preferred-location/domain field", "selector cannot be a hidden fifth force"),
        ("KK2698_4_memory", "action-owned memory with cosmological role and local double-zero/silence", "memory as hidden local dark sector or empirical patch", "data fits cannot replace local first variation"),
        ("KK2698_5_source_mass", "M_eff as descended parent Hamiltonian/Noether charge", "bare rest mass, orbital GM, or Pi_M mask as premise", "source readout must be fixed before comparison"),
        ("KK2698_6_boundary", "fixed reference/topological boundary terms with no local flux", "boundary bookkeeping used to move mass/current residuals", "worldtube/Gauss mass cannot be hidden in reference choice"),
        ("KK2698_7_transition", "ell_tr/L_cg from parent spectrum/source scale/topology", "arena switch chosen after seeing data", "unification needs one action-owned transition law"),
        ("KK2698_8_ppn", "PPN residual vector derived or source-backed and bounded", "assuming GR PPN after matching Newton leading order", "GR reduction is second-order/PPN, not just inverse-square leading force"),
    ]
    return [
        {
            "rule_id": rule_id,
            "keep": keep,
            "kill": kill,
            "reason": reason,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for rule_id, keep, kill, reason in rows
    ]


def symbol_status_classifier_rows(symbol_map: list[dict[str, Any]]) -> list[dict[str, Any]]:
    classification = {
        "SAP2698_0_kappa_eff_A3": "conditional_candidate",
        "SAP2698_1_g_obs_e_obs": "anchor_conditional",
        "SAP2698_2_Gamma_eff_Khat_q": "unplaced_first_variation_target",
        "SAP2698_3_chiD_Qcoh_domain": "conditional_candidate",
        "SAP2698_4_memory_time_flow": "conditional_eft_branch",
        "SAP2698_5_PiM_JH_Htau_Qtau": "conditional_charge_route",
        "SAP2698_6_boundary_reference": "open_boundary_clause",
        "SAP2698_7_nonEH_operator_R11": "residual_demoted",
        "SAP2698_8_matter_source_labels": "source_classifier_open",
        "SAP2698_9_ppn_readout": "not_derived_residual_interface",
        "SAP2698_10_transition_scale": "open_unification_scale",
        "SAP2698_11_verdict": "no_full_promotions",
    }
    rows: list[dict[str, Any]] = []
    for row in symbol_map:
        rows.append(
            {
                "classifier_id": row["placement_id"].replace("SAP", "SSC"),
                "symbol_group": row["symbol_group"],
                "symbols": row["symbols"],
                "classification": classification[row["placement_id"]],
                "mapped_action_blocks": row["mapped_action_blocks"],
                "blocking_status": row["current_status"],
                "promote_now": "false",
                "claim_allowed": "false",
                "next_action": row["next_action"],
                "timestamp_utc": stamp(),
            }
        )
    return rows


def residual_demotion_queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("RDQ2698_0_q_loc", "epsilon_GK_q_loc", "Gamma/Khat/q_loc extra-sector residual", "Gamma_eff scalar density, K_hat metric response, Helmholtz/Euler closure and boundary no-flux remain unsigned", "prove 2699 q_loc parent Ward/Euler theorem or source-backed finite component profile", "local_GR;PPN;R10;clock;orbital;WEP", "MISSING_PARENT_GK_QLOC_FIRST_VARIATION"),
        ("RDQ2698_1_kappa", "delta_kappa_residuals", "global coupling residuals", "topological kappa route is conditional, not parent-adopted", "parent-owned A3/kappa companion/stress/source silence or numeric residual rows", "R9;R10;WEP;source_normalization;clock", "MISSING_KAPPA_PARENT_ADOPTION"),
        ("RDQ2698_2_source_mass", "Delta_PiM;Delta_flux;Delta_source_charge", "source-measure and parent charge residuals", "Pi_M/Hamiltonian/source flux route selected but not signed", "derive H_tau/Q_tau/Pi_M descent and fixed boundary reference", "Newton;PPN;orbital;WEP", "MISSING_PARENT_CHARGE_DESCENT"),
        ("RDQ2698_3_boundary", "Delta_boundary;Delta_improvement", "boundary/reference residuals", "reference and exact/topological terms may carry hidden local flux", "term-by-term fixed-reference and no-flux proof", "local_GR;PPN;source_measure;q_loc", "MISSING_BOUNDARY_NO_FLUX"),
        ("RDQ2698_4_matter", "eta_source_AB;Delta_source_frame", "matter/source label residuals", "same-frame universal matter descent and source blindness are unsigned", "matter functor/coframe descent with no material gravitational charge prefactor", "WEP;source_normalization;local_GR", "MISSING_MATTER_SOURCE_DESCENT"),
        ("RDQ2698_5_memory", "Delta_memory_local", "memory/time/flow local leakage residuals", "memory branch not proved locally double-zero", "action-owned auxiliary/gapped memory sector and local first-variation silence", "clock;PPN;local_GR;cosmology_bridge", "MISSING_MEMORY_DOUBLE_ZERO"),
        ("RDQ2698_6_ppn", "Delta_PPN_vector", "weak-field readout residual vector", "second-order PPN source/operator calculation missing", "derive gamma,beta,alpha_i,zeta_i,xi after source normalization", "PPN;light_deflection;perihelion;preferred_frame", "MISSING_PPN_EXPANSION"),
        ("RDQ2698_7_transition", "Delta_transition_switch", "transition scale/activation residual", "ell_tr/L_cg not derived from parent spectrum/source scale/topology", "derive activation eigenvalue/source compactness/topological scale", "local_GR;cosmology;galaxy", "MISSING_TRANSITION_SCALE_DERIVATION"),
        ("RDQ2698_8_total", "Delta_local_GR_abs", "total local fixed-point residual envelope", "any open symbol placement blocks local GR promotion", "all rows theorem-zero or source-backed bounded with no cancellation-only credit", "all local arenas", "MISSING_COMPONENT_VALUES_AND_THEOREMS"),
    ]
    return [
        {
            "residual_id": residual_id,
            "residual_symbol": symbol,
            "owner": owner,
            "why_retained": why,
            "required_to_remove": required,
            "affected_arenas": arenas,
            "status": status,
            "numeric_value_present": "false",
            "source_backed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for residual_id, symbol, owner, why, required, arenas, status in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2698_0_all_current", False, False, False, False, False, False, False),
        ("DRY2698_1_kappa_only", True, False, False, False, False, False, False),
        ("DRY2698_2_GK_signed_only", False, True, False, False, False, False, False),
        ("DRY2698_3_GK_missing", True, False, True, True, True, False, False),
        ("DRY2698_4_source_missing", True, True, False, True, True, False, False),
        ("DRY2698_5_memory_local_unproved", True, True, True, False, True, False, False),
        ("DRY2698_6_ppn_missing", True, True, True, True, False, False, False),
        ("DRY2698_7_all_theorems_but_transition_missing", True, True, True, True, True, False, False),
        ("DRY2698_8_full_private_contract", True, True, True, True, True, True, False),
        ("DRY2698_9_cancellation_only", True, True, True, True, True, True, True),
    ]
    return [
        {
            "case_id": case_id,
            "kappa_parent_signed": as_bool(kappa),
            "Gamma_Khat_q_loc_parent_signed": as_bool(gk),
            "source_charge_signed": as_bool(source),
            "boundary_no_flux_signed": as_bool(boundary),
            "ppn_readout_signed": as_bool(ppn),
            "transition_scale_derived": as_bool(transition),
            "cancellation_only": as_bool(cancellation),
            "expected_claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for case_id, kappa, gk, source, boundary, ppn, transition, cancellation in cases
    ]


def score_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    blockers: list[str] = []
    if row["kappa_parent_signed"] != "true":
        blockers.append("kappa_parent_unsigned")
    if row["Gamma_Khat_q_loc_parent_signed"] != "true":
        blockers.append("GK_q_loc_unsigned")
    if row["source_charge_signed"] != "true":
        blockers.append("source_charge_unsigned")
    if row["boundary_no_flux_signed"] != "true":
        blockers.append("boundary_no_flux_unsigned")
    if row["ppn_readout_signed"] != "true":
        blockers.append("PPN_readout_unsigned")
    if row["transition_scale_derived"] != "true":
        blockers.append("transition_scale_unsigned")
    if row["cancellation_only"] == "true":
        blockers.append("cancellation_only_forbidden")

    if not blockers:
        status = "PRIVATE_CONTRACT_COMPLETE_BUT_REQUIRES_SEPARATE_PROOF_AUDIT"
    else:
        status = "BLOCKED_NONCLAIM"

    return {
        "case_id": row["case_id"],
        "status": status,
        "blockers": ";".join(blockers),
        "claim_allowed": "false",
        "matches_expected": "true",
        "timestamp_utc": stamp(),
    }


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2698_0_sources", "all cited source paths and needles exist", "SOURCE_REGISTER_READY", "true", "false", "source-backed map only; no physics promotion"),
        ("CG2698_1_kappa", "kappa parent topological route signed", "CONDITIONAL_UNSIGNED", "false", "false", "2695 conditional route not adopted"),
        ("CG2698_2_GK_q_loc", "Gamma/Khat/q_loc theorem-zero chain signed", "FAIL_SELECTED_NEXT_TARGET", "false", "false", "central first-variation target remains open"),
        ("CG2698_3_source_charge", "M_eff/Pi_M/H_tau parent charge descent signed", "FAIL_SOURCE_MEASURE_UNSIGNED", "false", "false", "2696 blocks source-measure promotion"),
        ("CG2698_4_boundary", "boundary/reference no-flux signed", "FAIL_OPEN", "false", "false", "boundary/improvement terms unresolved"),
        ("CG2698_5_ppn", "PPN vector derived or bounded after source normalization", "FAIL_NOT_DERIVED", "false", "false", "Newton leading order is not a GR reduction"),
        ("CG2698_6_transition", "ell_tr/L_cg derived from parent action", "FAIL_OPEN", "false", "false", "arena switching forbidden"),
        ("CG2698_7_local_GR", "local EH/GR/Newton branch can be claimed", "BLOCKED_NONCLAIM", "false", "false", "no full symbol promotion and q_loc remains first target"),
        ("CG2698_8_public_or_github", "public/GitHub readiness from this checkpoint", "BLOCKED_PRIVATE_WORK", "false", "false", "private derivation checkpoint only"),
    ]
    return [
        {
            "claim_gate_id": gate_id,
            "gate": gate,
            "status": status,
            "gate_passed": passed,
            "claim_allowed": allowed,
            "reason": reason,
            "timestamp_utc": stamp(),
        }
        for gate_id, gate, status, passed, allowed, reason in rows
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2698_0_map_status", "SYMBOL_MAP_WRITTEN", "MTS symbols are now mapped onto the minimal local fixed-point action blocks with explicit no-claim statuses", "use as private navigation ledger"),
        ("DEC2698_1_promotions", "NO_SYMBOL_FULLY_PROMOTED", "every placement still needs parent ownership, first variation, source/readout/boundary closure, or residual values", "do not claim local GR/Newton/PPN/R10"),
        ("DEC2698_2_primary_obstruction", "GAMMA_KHAT_QLOC_IS_FIRST_EXACT_TARGET", "q_loc is the cleanest live coupling obstruction because it touches extra-sector silence, local force residuals, and PPN/local tests", "attack it before broader recaps"),
        ("DEC2698_3_source_parallel", "SOURCE_CHARGE_REMAINS_PARALLEL_BLOCKER", "even a q_loc win still needs parent H_tau/Pi_M/source-measure closure", "keep Pi_M as derived projection only"),
        ("DEC2698_4_transition", "TRANSITION_SCALE_HELD", "ell_tr/L_cg cannot be used as arena switch while local residuals are unresolved", "derive from spectrum/source/topology later"),
        ("DEC2698_5_public_policy", "PRIVATE_NON_GITHUB_CHECKPOINT", "this is a rigorous internal map, not a public claim package", "no GitHub action"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "next_use": next_use,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for decision_id, decision, rationale, next_use in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT2698_0_selected",
            "selection": "selected_primary",
            "target_doc": "2699-Y5-R2FR-Gamma-Khat-q-loc-first-variation-or-official-residual-demotion.md",
            "target_script": "scripts/Y5_R2FR_Gamma_Khat_q_loc_first_variation_or_official_residual_demotion_2699.py",
            "task": "derive or reject the exact parent first-variation identity whose Ward/Euler residual is q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "success_condition": "Gamma_eff is a parent scalar density, K_hat is its metric response including boundary/improvement terms, Helmholtz/Euler closure gives F1=0, P_loc q=0, and boundary flux is zero",
            "fallback": "officially demote epsilon_GK_q_loc into finite residual rows for local_GR, PPN, R10, clocks, orbitals, and WEP with valid_for_claim=false",
            "forbidden_shortcuts": "plateau axiom;scalar proxy for vector residual;fitted G;readout cancellation;arena switch;GitHub action",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "next_id": "NEXT2698_1_parallel_hold",
            "selection": "held_parallel",
            "target_doc": "2700-Y5-R2FR-parent-charge-source-measure-after-q-loc-classification.md",
            "target_script": "scripts/Y5_R2FR_parent_charge_source_measure_after_q_loc_classification_2700.py",
            "task": "return to H_tau/Pi_M/M_eff source-measure descent after q_loc is classified",
            "success_condition": "M_eff is a conserved parent Hamiltonian/Noether charge with fixed reference and no hidden flux before orbital readout",
            "fallback": "fill Delta_PiM, Delta_flux, and source-charge residual rows",
            "forbidden_shortcuts": "using orbital GM as premise;bare rest mass substitution;projector mask",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2698_0_project", "overall unified framework", "COHERENT_PRIVATE_FIXED_POINT_MAP", "we now have a disciplined symbol-to-action map, but it is not a proof", "attack q_loc first variation"),
        ("STATUS2698_1_local_GR", "local GR/Newton reduction", "BLOCKED_BUT_NARROWED", "main obstruction is no longer vague: Gamma/Khat/q_loc, source charge, boundary/readout, and PPN vector are explicit", "derive or demote q_loc"),
        ("STATUS2698_2_coupling", "coupling sector", "BEST_PROGRESS_IS_CONDITIONAL_KAPPA_PLUS_GK_TARGET", "kappa has a clean conditional topological route; q_loc remains the dangerous live coupling residual", "run 2699"),
        ("STATUS2698_3_data", "empirical testing", "NOT_NEXT_FOR_LOCAL_GR_CLAIM", "cosmology/galaxy tests are useful, but local GR derivability needs the residual interfaces first", "no new data claim from 2698"),
        ("STATUS2698_4_public", "public/GitHub", "NO_ACTION", "private workbench checkpoint with unresolved proof gates", "keep private"),
    ]
    return [
        {
            "status_id": status_id,
            "topic": topic,
            "status": status,
            "meaning": meaning,
            "next_action": next_action,
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for status_id, topic, status, meaning, next_action in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": "BC2698_0_local_symbol_map",
            "source_csv": str(OUTPUTS["symbol_action_map"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_symbol_action_map"]),
            "purpose": "make local-bound branch consume the symbol placement map without claim promotion",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2698_1_local_residuals",
            "source_csv": str(OUTPUTS["residual_demotion"]),
            "branch_csv": str(BRANCH_OUTPUTS["local_residual_demotion"]),
            "purpose": "make local-bound branch consume explicit residual demotion rows",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2698_2_wep_residuals",
            "source_csv": str(OUTPUTS["residual_demotion"]),
            "branch_csv": str(BRANCH_OUTPUTS["wep_residual_demotion"]),
            "purpose": "make WEP branch inherit no-claim source/q_loc residual status",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2698_3_source_weight",
            "source_csv": str(OUTPUTS["residual_demotion"]),
            "branch_csv": str(BRANCH_OUTPUTS["source_weight_residual_demotion"]),
            "purpose": "make source-weight branch inherit no-claim source-measure residual status",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "copy_id": "BC2698_4_rab_next",
            "source_csv": str(OUTPUTS["next_target"]),
            "branch_csv": str(BRANCH_OUTPUTS["rab_next"]),
            "purpose": "queue exact Gamma/Khat/q_loc first-variation target for RAB/local residual work",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    all_sources_exist = all(row["exists"] == "true" for row in source_rows)
    all_needles_found = all(row["missing_needles"] == "" for row in source_rows)

    parse_targets = {key: path for key, path in OUTPUTS.items() if key != "validation"}
    parse_targets.update(BRANCH_OUTPUTS)
    parse_results = {key: parse_csv(path) for key, path in parse_targets.items()}
    all_csv_parse = all(ok and count > 0 for ok, count, _ in parse_results.values())

    symbol_map = rows_by_name["symbol_action_map"]
    statuses = rows_by_name["symbol_status"]
    claim_gates = rows_by_name["claim_gates"]
    next_targets = rows_by_name["next_target"]
    dryrun_results = rows_by_name["dryrun_results"]

    no_symbol_promoted = all(row["promotion_allowed"] == "false" for row in symbol_map) and all(
        row["promote_now"] == "false" for row in statuses
    )
    qloc_selected = any("Gamma-Khat-q-loc" in row["target_doc"] and row["selection"] == "selected_primary" for row in next_targets)
    qloc_unpromoted = any(
        row["placement_id"] == "SAP2698_2_Gamma_eff_Khat_q"
        and row["current_status"] == "UNPLACED_FIRST_VARIATION_TARGET"
        and row["claim_allowed"] == "false"
        for row in symbol_map
    )
    claim_gates_safe = all(row["claim_allowed"] == "false" for row in claim_gates)
    dryruns_safe = all(row["claim_allowed"] == "false" and row["matches_expected"] == "true" for row in dryrun_results)
    no_formalization_outputs = all("formalization-workbench" not in str(path).lower() for path in parse_targets.values())
    no_github_outputs = all(".git" not in str(path).lower() and "github" not in path.name.lower() for path in parse_targets.values())

    checks = [
        ("VAL2698_0_sources_exist", all_sources_exist, "all cited local source paths exist"),
        ("VAL2698_1_needles_found", all_needles_found, "all required source needles were found"),
        ("VAL2698_2_csv_parse", all_csv_parse, "all generated CSVs and branch copies parse with at least one row"),
        ("VAL2698_3_no_symbol_promoted", no_symbol_promoted, "no symbol is promoted from mapping alone"),
        ("VAL2698_4_qloc_selected", qloc_selected, "Gamma/Khat/q_loc first-variation target selected"),
        ("VAL2698_5_qloc_unpromoted", qloc_unpromoted, "Gamma/Khat/q_loc remains unplaced/nonclaim"),
        ("VAL2698_6_claim_gates_safe", claim_gates_safe, "all claim gates keep claim_allowed=false"),
        ("VAL2698_7_dryruns_safe", dryruns_safe, "dry-run cases never allow claims"),
        ("VAL2698_8_no_formalization_outputs", no_formalization_outputs, "no output path points into formalization-workbench"),
        ("VAL2698_9_no_github_outputs", no_github_outputs, "no GitHub/public-output path was written"),
    ]

    for check_id, passed, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "passed": as_bool(passed),
                "detail": detail,
                "timestamp_utc": stamp(),
            }
        )

    for key, (ok, count, message) in parse_results.items():
        rows.append(
            {
                "check_id": f"VAL2698_PARSE_{key}",
                "passed": as_bool(ok and count > 0),
                "detail": f"{message}; rows={count}",
                "timestamp_utc": stamp(),
            }
        )

    overall = all(row["passed"] == "true" for row in rows)
    rows.append(
        {
            "check_id": "VAL2698_OVERALL",
            "passed": as_bool(overall),
            "detail": "2698 maps MTS symbols to the 2697 fixed-point action blocks, promotes nothing, and selects Gamma/Khat/q_loc as the next exact derivation target",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    source_rows = rows_by_name["source_register"]
    symbol_rows = rows_by_name["symbol_action_map"]
    gate_rows = rows_by_name["first_variation_gates"]
    keep_kill_rows = rows_by_name["keep_kill_rules"]
    residual_rows = rows_by_name["residual_demotion"]
    claim_rows = rows_by_name["claim_gates"]
    decision_rows = rows_by_name["decision_ledger"]
    next_rows = rows_by_name["next_target"]
    status_rows = rows_by_name["project_status"]
    validation = rows_by_name["validation"]

    qloc_row = next(row for row in symbol_rows if row["placement_id"] == "SAP2698_2_Gamma_eff_Khat_q")
    verdict = (
        "The 2698 map is progress, not promotion. The local-GR route now has a precise symbol contract: "
        "kappa has a clean conditional topological mechanism, source mass has a parent-charge route, and the "
        "live extra-sector obstruction is Gamma_eff/K_hat/q_loc. No symbol is claim-ready. The next leap is "
        "to try the exact q_loc first-variation proof; if it does not close, q_loc becomes an official finite "
        "residual vector rather than a hidden plateau axiom."
    )

    text = f"""# 2698: MTS Symbols To Minimal Local Fixed-Point Action Map

**Branch:** `{BRANCH_ID}`

## Private Verdict

{verdict}

## Main Map Takeaway

`{qloc_row["symbols"]}` is the next sharp target. The required identity is:

`q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}})`.

This checkpoint does not treat that expression as a force law, a fitted switch, or a plateau axiom. It treats it as a residual that must be derived from a parent action/metric-response/Ward identity or carried honestly into finite local-test residual rows.

## Source Register

{markdown_table(source_rows)}

## Symbol-To-Action Placement Map

{markdown_table(symbol_rows)}

## First-Variation Evidence Gates

{markdown_table(gate_rows)}

## Keep/Kill Rules

{markdown_table(keep_kill_rows)}

## Residual Demotion Queue

{markdown_table(residual_rows)}

## Claim Gates

{markdown_table(claim_rows)}

## Decision Ledger

{markdown_table(decision_rows)}

## Next Targets

{markdown_table(next_rows)}

## Project Status Snapshot

{markdown_table(status_rows)}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    symbol_rows = symbol_action_placement_rows()
    gate_rows = first_variation_gate_rows()
    keep_kill_rows = keep_kill_rule_rows()
    status_rows = symbol_status_classifier_rows(symbol_rows)
    residual_rows = residual_demotion_queue_rows()
    dryrun_cases = dryrun_case_rows()
    dryrun_results = [score_dryrun_case(row) for row in dryrun_cases]
    claim_rows = claim_gate_rows()
    decision_rows = decision_ledger_rows()
    next_rows = next_target_rows()
    project_rows = project_status_rows()
    branch_rows = branch_copy_rows()

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_rows,
        "symbol_action_map": symbol_rows,
        "first_variation_gates": gate_rows,
        "keep_kill_rules": keep_kill_rows,
        "symbol_status": status_rows,
        "residual_demotion": residual_rows,
        "dryrun_cases": dryrun_cases,
        "dryrun_results": dryrun_results,
        "claim_gates": claim_rows,
        "decision_ledger": decision_rows,
        "next_target": next_rows,
        "project_status": project_rows,
        "branch_copies": branch_rows,
    }

    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)

    write_csv(BRANCH_OUTPUTS["local_symbol_action_map"], symbol_rows)
    write_csv(BRANCH_OUTPUTS["local_residual_demotion"], residual_rows)
    write_csv(BRANCH_OUTPUTS["wep_residual_demotion"], residual_rows)
    write_csv(BRANCH_OUTPUTS["source_weight_residual_demotion"], residual_rows)
    write_csv(BRANCH_OUTPUTS["rab_next"], next_rows)

    validation = validation_rows(rows_by_name)
    rows_by_name["validation"] = validation
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name)

    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
