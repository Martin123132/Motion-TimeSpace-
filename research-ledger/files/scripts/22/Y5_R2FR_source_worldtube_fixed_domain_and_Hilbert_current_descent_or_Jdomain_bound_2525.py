from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_SOURCE_WORLDTUBE_DOMAIN_DESCENT_2525"
CHECKPOINT_ID = "2525"
DOC = ROOT / "2525-Y5-R2FR-source-worldtube-fixed-domain-and-Hilbert-current-descent-or-Jdomain-bound.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_SOURCE_REGISTER.csv",
    "worldtube_descent_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_WORLDTUBE_DESCENT_AUDIT.csv",
    "fixed_domain_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_FIXED_DOMAIN_GATE.csv",
    "jdomain_bound_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_JDOMAIN_BOUND_ROWS.csv",
    "observable_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_OBSERVABLE_GATE.csv",
    "dryrun_results": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_DRYRUN_RESULTS.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2525_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2525_VALIDATION.csv",
}

BRANCH_COPIES = {
    "worldtube_descent_audit": ROOT
    / "source-intake"
    / "local_bounds"
    / "Worldtube_domain_descent_audit_2525_NONCLAIM.csv",
    "jdomain_bound_rows": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Jdomain_bound_rows_2525_NONCLAIM.csv",
    "fixed_domain_gate": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2525_FIXED_DOMAIN_GATE_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "JR2525_NEXT_TARGET_NONCLAIM.csv",
}

SOURCE_SPECS = [
    {
        "source_id": "SRC2525_0_2524_next",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2524_NEXT_TARGET.csv",
        "needles": ["NEXT2524_0_selected", "W_source"],
        "role": "authoritative 2524 handoff to fixed source-worldtube/domain descent",
    },
    {
        "source_id": "SRC2525_1_2524_validation",
        "path": "source-intake/mts_residuals/P8_Y5_BRR545_2524_VALIDATION.csv",
        "needles": ["VAL2524_OVERALL", "PASS"],
        "role": "previous checkpoint validation gate",
    },
    {
        "source_id": "SRC2525_2_2524_jpim_rows",
        "path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2524_JPIM_BOUND_ROWS.csv",
        "needles": ["JPIM2524_7_worldtube", "MISSING_WORLDTUBE_FIXEDNESS_OR_BOUND"],
        "role": "Pi_M checkpoint identifies worldtube fixedness as a required component",
    },
    {
        "source_id": "SRC2525_3_2355_fixed_domain",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2355_FIXED_DOMAIN_THEOREM_AUDIT.csv",
        "needles": ["FDT2355_1_vertical_support_descent", "EXACT_CONDITIONAL_LEMMA"],
        "role": "prior fixed-domain theorem: support descent is clean but conditional",
    },
    {
        "source_id": "SRC2525_4_2356_descent",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2356_SOURCE_CURRENT_DESCENT_THEOREM_AUDIT.csv",
        "needles": ["SCD2356_1_descent_theorem", "EXACT_CONDITIONAL_THEOREM"],
        "role": "prior source-current descent theorem in exact conditional form",
    },
    {
        "source_id": "SRC2525_5_2356_parent_clauses",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2356_PARENT_DESCENT_CLAUSES.csv",
        "needles": ["PDC2356_9_verdict", "DESCENT_CHAIN_NOT_CLOSED"],
        "role": "parent descent clauses remain unsigned in the current corpus",
    },
    {
        "source_id": "SRC2525_6_2356_domain_rows",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2356_DOMAIN_MOTION_BOUND_ROWS.csv",
        "needles": ["DMB2356_0_total", "MISSING_COMPONENT_VALUES"],
        "role": "fallback domain-motion/source-current bound row set",
    },
    {
        "source_id": "SRC2525_7_2419_chainmap",
        "path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2419_CHAINMAP_ZERO_GATE.csv",
        "needles": ["CMG2419_4_source_descent", "CONDITIONAL_APPLICATION_BLOCKED"],
        "role": "source-worldtube/projector chain-map gate points to source-current descent",
    },
    {
        "source_id": "SRC2525_8_2466_hilbert",
        "path": "source-intake/mts_residuals/P8_Y5_SOURCE_BRIDGE_2466_HILBERT_CURRENT_DESCENT.csv",
        "needles": ["HIL2466_1_define_current", "MISSING_PARENT_SCALE"],
        "role": "Hilbert current contract and parent scale blocker",
    },
    {
        "source_id": "SRC2525_9_2466_worldtube",
        "path": "source-intake/mts_residuals/P8_Y5_SOURCE_BRIDGE_2466_WORLDTUBE_BRIDGE.csv",
        "needles": ["WT2466_2_surface_independence", "MISSING_CONSERVATION_PROOF"],
        "role": "worldtube bridge: surface independence requires conservation/jump conditions",
    },
    {
        "source_id": "SRC2525_10_2481_gauss",
        "path": "source-intake/mts_residuals/P8_Y5_SOURCE_NORM_2481_WORLDTUBE_GAUSS_GATE.csv",
        "needles": ["WT2481_1_stationary_collar", "BLOCKED_DYNAMIC"],
        "role": "stationary source-normalization control branch and dynamic blocker",
    },
    {
        "source_id": "SRC2525_11_2468_hypotheses",
        "path": "source-intake/mts_residuals/P8_Y5_STATIONARY_SOURCE_2468_THEOREM_HYPOTHESES.csv",
        "needles": ["HYP2468_5_compact_support", "ASSUMED_OR_BOUND_REQUIRED"],
        "role": "stationary local-source theorem relies on compact support and fixed projector hypotheses",
    },
    {
        "source_id": "SRC2525_12_2503_selector",
        "path": "2503-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R-eq-fill.md",
        "needles": ["WHS2503_6_current_verdict", "SELECTOR_THEOREM_CONDITIONAL_CURRENT_CLAIM_FAILS"],
        "role": "worldtube-Hilbert selector theorem remains conditional and not claimable",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        cells: list[str] = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", "<br>").replace("|", "\\|")
            cells.append(value)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["path"]
        text = read_text(path)
        found_needles = [needle for needle in spec["needles"] if needle in text]
        rows.append(
            base_row(
                source_id=spec["source_id"],
                source_path=spec["path"],
                path_exists=path.exists(),
                required_needles=";".join(spec["needles"]),
                found_needles=";".join(found_needles),
                role=spec["role"],
                source_pass=path.exists() and len(found_needles) == len(spec["needles"]),
            )
        )
    return rows


def worldtube_descent_audit_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "audit_id": "WTD2525_0_definition",
            "claim_piece": "source-worldtube/current complex",
            "formal_statement": "W_source:=closure(supp J_H[e_obs,tau]), A_ext and S_link are chosen from q(W_source), and Pi_M acts on the same parent Hilbert-current complex before readout.",
            "result": "DEFINITION_LOCKED_CONDITIONAL",
            "blocking_gap": "definition is clean only after J_H, tau, q(W_source), A_ext and S_link are parent-owned",
            "effect": "prevents fitted source masks from posing as derivations",
        },
        {
            "audit_id": "WTD2525_1_Hilbert_current_contract",
            "claim_piece": "Hilbert current source",
            "formal_statement": "T_H^{mu nu}=-(2/sqrt(-g))delta S_matter/delta g_mu_nu and J_M^nu=ell_J T_H^{nu rho} tau_rho.",
            "result": "PASS_AS_CONDITIONAL_CONTRACT",
            "blocking_gap": "ell_J, tau, matter coupling descent and current exchange are not parent-signed",
            "effect": "gives the least-circular source object, but not yet a Newton proof",
        },
        {
            "audit_id": "WTD2525_2_source_current_descent",
            "claim_piece": "J_H=q^*Jbar_H descent",
            "formal_statement": "If S_matter factors through q, v in ker(Dq), and vertical matter lifts are gauge/Euler/boundary-only, then the bulk vertical source current vanishes.",
            "result": "EXACT_CONDITIONAL_THEOREM",
            "blocking_gap": "q object, verticality, matter factorization, constants, no-source-slot, boundary/support and readout-order clauses are unsigned together",
            "effect": "this is the real route to fixed source support",
        },
        {
            "audit_id": "WTD2525_3_support_corollary",
            "claim_piece": "vertical support fixedness",
            "formal_statement": "If J_H=q^*Jbar_H with compact regular support, then D_v q(W_source)=0 on regular support strata.",
            "result": "EXACT_CONDITIONAL_COROLLARY",
            "blocking_gap": "regular support, source-free annulus, no boundary tail and pullback source current are not current-MTS signatures",
            "effect": "worldtube motion can vanish by descent, not by wishful support choice",
        },
        {
            "audit_id": "WTD2525_4_fixed_domain_stokes",
            "claim_piece": "fixed annulus/linking surface",
            "formal_statement": "Stokes/linking arguments apply to the same fixed A_ext and S_link only after the parent owns q(W_source), source-free exterior and boundary class.",
            "result": "EXACT_CONDITIONAL_STOKES_ROUTE",
            "blocking_gap": "fixed-domain owner, exterior silence, zero boundary flux and fixed reference are not signed",
            "effect": "domain-mask and boundary-crossing rows remain live",
        },
        {
            "audit_id": "WTD2525_5_stationary_control",
            "claim_piece": "stationary compact source branch",
            "formal_statement": "Under fixed ell_J, stationary tau, matter-shell conservation, compact support and no side flux, Q_M and M_H are surface-independent.",
            "result": "PASS_STATIONARY_CONDITIONAL_CONTROL",
            "blocking_gap": "dynamic exchange, jump/support theorem and parent kappa/G calibration remain unsigned",
            "effect": "useful control lane, not a full local-GR/Newton source theorem",
        },
        {
            "audit_id": "WTD2525_6_noether_guard",
            "claim_piece": "Noether/conservation shortcut",
            "formal_statement": "dJ=0 or diffeomorphism covariance does not imply J_H=q^*Jbar_H or measured-source equality.",
            "result": "SHORTCUT_REFUSED",
            "blocking_gap": "conserved wrong-object currents and post-readout masks remain possible",
            "effect": "keeps source descent distinct from ordinary conservation",
        },
        {
            "audit_id": "WTD2525_7_dynamic_and_boundary",
            "claim_piece": "dynamic worldtube and boundary closure",
            "formal_statement": "nabla_mu J_M^mu plus tau/GK/matter exchange, jump/support terms and boundary flux must vanish or be bounded.",
            "result": "DYNAMIC_WORLDLINE_CLOSURE_NOT_DERIVED",
            "blocking_gap": "exchange current, distributional jump support and zero boundary flux remain open",
            "effect": "dynamic/source-boundary rows remain retained",
        },
        {
            "audit_id": "WTD2525_8_verdict",
            "claim_piece": "fixed source-worldtube/domain current descent",
            "formal_statement": "W_source, A_ext, S_link, J_H and tau are all parent-owned/fixed before readout and live on one Hilbert-current complex.",
            "result": "WORLD_TUBE_DOMAIN_DESCENT_NOT_DERIVED_STAGE_BOUND_ROWS",
            "blocking_gap": "the theorem route is exact but the parent matter-coupling/current-domain antecedents are not signed",
            "effect": "retain finite E_worldtube/E_domain_motion/E_current_escape rows and move to parent matter-coupling action",
        },
    ]
    return [base_row(**entry) for entry in entries]


def fixed_domain_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "FDG2525_0_parent_q",
            "required_clause": "parent q object before matter/readout",
            "formal_condition": "q: Phi_parent -> Q_obs is parent kinematics/action data and not a retrospective label",
            "current_status": "BLOCKED_Q_OBJECT_NOT_PARENT_SIGNED",
            "if_fail": "Dq(v)=0 is notation rather than a source theorem",
        },
        {
            "gate_id": "FDG2525_1_vertical_generator",
            "required_clause": "local residual direction is quotient-vertical",
            "formal_condition": "v in ker(Dq) on an open local branch, not merely at a point or by symbol choice",
            "current_status": "BLOCKED_VERTICALITY_NOT_SIGNED",
            "if_fail": "the source current can couple to a physical local mode",
        },
        {
            "gate_id": "FDG2525_2_JH_descent",
            "required_clause": "Hilbert current descends",
            "formal_condition": "J_H=q^*Jbar_H and J_v^matter=0 modulo owned gauge/Euler/boundary terms",
            "current_status": "BLOCKED_SOURCE_CURRENT_DESCENT_UNSIGNED",
            "if_fail": "worldtube support can move under vertical variation",
        },
        {
            "gate_id": "FDG2525_3_tau_ellJ",
            "required_clause": "tau and ell_J parent-owned",
            "formal_condition": "tau_source=tau_clock=tau_readout and ell_J is fixed before local tests",
            "current_status": "BLOCKED_TAU_ELLJ_LOCK_UNSIGNED",
            "if_fail": "clock/scale drift moves source normalization and support",
        },
        {
            "gate_id": "FDG2525_4_compact_regular_support",
            "required_clause": "compact regular source support with buffer annulus",
            "formal_condition": "supp(Jbar_H) is compact/regular and exterior collar is source-free except bounded tails",
            "current_status": "BLOCKED_SUPPORT_THEOREM_ASSUMED_OR_BOUND_REQUIRED",
            "if_fail": "source tails leak into the exterior annulus",
        },
        {
            "gate_id": "FDG2525_5_fixed_domain_owner",
            "required_clause": "fixed A_ext and S_link",
            "formal_condition": "A_ext and S_link are selected from q(W_source) before readout and do not drift under v",
            "current_status": "BLOCKED_FIXED_DOMAIN_OWNER_UNSIGNED",
            "if_fail": "dchi_W and boundary-crossing rows survive",
        },
        {
            "gate_id": "FDG2525_6_exterior_silence",
            "required_clause": "no hidden exterior/current escape",
            "formal_condition": "non-EH, memory, domain, range, species, anomaly, boundary and projector source channels are zero or bounded in A_ext",
            "current_status": "BLOCKED_EXTERIOR_SILENCE_UNSIGNED",
            "if_fail": "J_escape/E_extra_current survives",
        },
        {
            "gate_id": "FDG2525_7_boundary_jump",
            "required_clause": "zero boundary/jump/support leakage",
            "formal_condition": "distributional jump conditions and boundary flux make no unowned source contribution",
            "current_status": "BLOCKED_BOUNDARY_SUPPORT_SILENCE_OPEN",
            "if_fail": "boundary-crossing and side-flux residuals survive",
        },
        {
            "gate_id": "FDG2525_8_MHref",
            "required_clause": "positive same-frame M_H_ref denominator",
            "formal_condition": "M_H_ref=H_tau[S_outer]-H_ref>0 is parent-owned and not orbital-GM backfilled",
            "current_status": "BLOCKED_MHREF_NORMALIZATION_MISSING",
            "if_fail": "finite domain rows are not dimensionless or noncircular",
        },
        {
            "gate_id": "FDG2525_9_no_readout_mask",
            "required_clause": "no post-readout source mask",
            "formal_condition": "W_source, A_ext, S_link and Pi_M are not selected after orbit/PPN/WEP/clock fitting",
            "current_status": "GUARDRAIL_ACTIVE_NOT_ZERO_THEOREM",
            "if_fail": "measured-GM/source-mask laundering enters the proof",
        },
        {
            "gate_id": "FDG2525_10_theorem",
            "required_clause": "fixed domain/source-current theorem",
            "formal_condition": "FDG2525_0 through FDG2525_9 all pass with source paths",
            "current_status": "CLAIM_BLOCKED_STAGE_JDOMAIN_ROWS",
            "if_fail": "retain nonclaim finite domain/current rows",
        },
    ]
    return [base_row(**entry, gate_pass=False) for entry in entries]


def jdomain_bound_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "row_id": "JDOM2525_0_total",
            "quantity": "E_source_worldtube_domain_abs",
            "row_role": "absolute envelope for failed source-worldtube/domain/current descent",
            "formula_or_bound": "E_source_worldtube_domain_abs <= E_current_descent + E_tau_ellJ + E_support_motion + E_domain_mask + E_boundary_crossing + E_exterior_tail + E_current_escape + E_dynamic_exchange + E_MHref_guard + E_readout_mask",
            "units": "dimensionless_after_MHref_or_memory_source_units",
            "required_inputs": "component zero certificates or values; M_H_ref; units; source paths; no-cancellation ledger",
            "current_status": "MISSING_WORLD_TUBE_DESCENT_ZERO_OR_COMPONENT_VALUES",
            "observable_links": "J_PiM_comm;J_readout;J_mem;Q_mem;Newton;PPN;R10;WEP;clock;orbit",
        },
        {
            "row_id": "JDOM2525_1_current_descent",
            "quantity": "E_current_descent",
            "row_role": "failure of Hilbert current to descend through q",
            "formula_or_bound": "E_current_descent := ||J_H - q^*Jbar_H|| or ||delta_v S_matter-DSbar[Dq(v)]||_bulk / M_H_ref",
            "units": "source_current_units_over_MHref",
            "required_inputs": "parent matter action; q map; vertical generator; matter factorization proof or finite coefficient",
            "current_status": "MISSING_SOURCE_CURRENT_DESCENT_PROOF_OR_BOUND",
            "observable_links": "worldtube;Newton;WEP;PPN",
        },
        {
            "row_id": "JDOM2525_2_tau_ellJ",
            "quantity": "E_tau_ellJ",
            "row_role": "source clock/scale drift",
            "formula_or_bound": "E_tau_ellJ <= |delta ell_J|/|ell_J| + ||delta tau_source|| K_tau + exchange-current terms",
            "units": "dimensionless_or_source_current_units",
            "required_inputs": "ell_J parent source; tau lock; exchange-current theorem or bound",
            "current_status": "MISSING_TAU_ELLJ_PARENT_LOCK_OR_EXCHANGE_BOUND",
            "observable_links": "clock;Gdot;orbit;source_normalization",
        },
        {
            "row_id": "JDOM2525_3_support_motion",
            "quantity": "E_support_motion",
            "row_role": "vertical motion of source support",
            "formula_or_bound": "E_support_motion <= ||D_v q(W_source)|| times source-boundary kernel",
            "units": "domain_motion_kernel_units",
            "required_inputs": "regular support theorem; support stratification; source-boundary kernel",
            "current_status": "MISSING_SUPPORT_FIXEDNESS_OR_BOUND",
            "observable_links": "J_PiM_comm;Newton;orbit",
        },
        {
            "row_id": "JDOM2525_4_domain_mask",
            "quantity": "E_domain_mask",
            "row_role": "moving domain mask contribution",
            "formula_or_bound": "E_domain_mask := abs(int_A dchi_W wedge Pi_M J_H)/M_H_ref",
            "units": "source_flux_over_MHref",
            "required_inputs": "chi_W profile; A_ext; Pi_M J_H profile; M_H_ref; source path",
            "current_status": "MISSING_DCHI_OR_FIXED_DOMAIN_THEOREM",
            "observable_links": "I_commutator;R10;orbital",
        },
        {
            "row_id": "JDOM2525_5_boundary_crossing",
            "quantity": "E_boundary_crossing",
            "row_role": "moving boundary/linking-surface crossing term",
            "formula_or_bound": "E_boundary_crossing := abs(int_boundary(A_ext) i_v(Pi_M J_H))/M_H_ref",
            "units": "source_flux_over_MHref",
            "required_inputs": "boundary surface; variation vector; Pi_M J_H profile; M_H_ref",
            "current_status": "MISSING_BOUNDARY_CROSSING_ZERO_OR_BOUND",
            "observable_links": "PPN;orbit;R10",
        },
        {
            "row_id": "JDOM2525_6_exterior_tail",
            "quantity": "E_exterior_tail",
            "row_role": "unowned source/exterior tail",
            "formula_or_bound": "E_exterior_tail <= abs(int_A chi_ext J_tail)/M_H_ref",
            "units": "source_flux_over_MHref",
            "required_inputs": "compact support/falloff theorem or numeric tail profile",
            "current_status": "MISSING_COMPACT_SUPPORT_OR_TAIL_BOUND",
            "observable_links": "Newton;R10;WEP",
        },
        {
            "row_id": "JDOM2525_7_current_escape",
            "quantity": "E_current_escape",
            "row_role": "current outside fixed Hilbert/source complex",
            "formula_or_bound": "E_current_escape <= ||P_source[J_escape]||/M_H_ref",
            "units": "dimensionless_after_MHref",
            "required_inputs": "extra-current inventory; anomaly/source-channel zero theorem or finite rows",
            "current_status": "MISSING_EXTRA_CURRENT_SILENCE_OR_BOUND",
            "observable_links": "Newton;PPN;species;R11",
        },
        {
            "row_id": "JDOM2525_8_dynamic_exchange",
            "quantity": "E_dynamic_exchange",
            "row_role": "dynamic tau/GK/matter exchange and jump/support leakage",
            "formula_or_bound": "E_dynamic_exchange <= abs(int_V (nabla_mu J_M^mu + I_tau + I_GK)) + jump/support side-flux terms",
            "units": "source_current_units_over_MHref",
            "required_inputs": "dynamic exchange identity; distributional jump conditions; side-flux theorem or bound",
            "current_status": "MISSING_DYNAMIC_EXCHANGE_AND_JUMP_SUPPORT",
            "observable_links": "clock;Gdot;orbit;local_GR",
        },
        {
            "row_id": "JDOM2525_9_MHref_guard",
            "quantity": "E_MHref_guard",
            "row_role": "same-frame denominator guard",
            "formula_or_bound": "E_MHref_guard := I_not_sourced(M_H_ref,H_tau,H_ref,Q_tau,tau_source=tau_readout)",
            "units": "guard_or_dimensionless_denominator_residual",
            "required_inputs": "positive M_H_ref; parent H_tau/H_ref/Q_tau; tau lock; no orbital-GM backfill",
            "current_status": "MISSING_MHREF_TAU_LOCK",
            "observable_links": "all_local_arenas",
        },
        {
            "row_id": "JDOM2525_10_readout_mask",
            "quantity": "E_readout_mask",
            "row_role": "post-readout domain/source mask leakage",
            "formula_or_bound": "E_readout_mask <= ||partial_fit W_source|| + ||partial_fit A_ext|| + ||partial_fit S_link|| under fitted arena maps",
            "units": "dimensionless_or_domain_motion_units",
            "required_inputs": "fixed-before-readout theorem or finite calibration sensitivity",
            "current_status": "MISSING_NO_READOUT_MASK_THEOREM_OR_BOUND",
            "observable_links": "orbit;PPN;WEP;clock",
        },
        {
            "row_id": "JDOM2525_11_JPiM_insertion",
            "quantity": "domain/current contribution to J_PiM_comm",
            "row_role": "worldtube/domain component inside Pi_M commutator",
            "formula_or_bound": "J_PiM_comm includes E_source_worldtube_domain_abs plus Pi_M representative, R_eq, B_zero and projector-stress rows under common normalization",
            "units": "memory_source_units_or_dimensionless_after_MHref",
            "required_inputs": "E_source_worldtube_domain_abs value/theorem-zero plus remaining J_PiM components",
            "current_status": "FILL_CONTRACT_READY_VALUES_MISSING",
            "observable_links": "J_PiM_comm;J_readout;Q_mem",
        },
        {
            "row_id": "JDOM2525_12_Qmem_insertion",
            "quantity": "N_src J_domain",
            "row_role": "domain/current leakage insertion into Q_mem through readout source drive",
            "formula_or_bound": "Q_mem_domain <= A_ref^-1 N_src J_domain",
            "units": "dimensionless_after_Aref",
            "required_inputs": "A_ref;N_src;J_domain value/theorem-zero; source path",
            "current_status": "FILL_CONTRACT_READY_VALUES_MISSING",
            "observable_links": "Q_norm;PPN_gamma;local_GR",
        },
    ]
    return [
        base_row(
            **entry,
            score_ready=False,
            valid_prediction_row=False,
            accepted_for_scoring=False,
            claim_pass=False,
        )
        for entry in entries
    ]


def observable_gate_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "gate_id": "WOG2525_0_JPiM",
            "arena": "J_PiM_comm/J_readout",
            "map_formula": "E_source_worldtube_domain_abs enters J_PiM_comm and therefore J_readout",
            "required_bundle": "fixed domain theorem or finite domain/current values plus M_H_ref",
            "status": "BLOCKED_MISSING_DOMAIN_CURRENT_VALUE_OR_THEOREM",
        },
        {
            "gate_id": "WOG2525_1_Qmem",
            "arena": "Q_mem residual",
            "map_formula": "Q_mem_domain <= A_ref^-1 N_src J_domain",
            "required_bundle": "A_ref;N_src;J_domain units/value/source path",
            "status": "BLOCKED_MISSING_QMEM_DOMAIN_INSERTION_VALUES",
        },
        {
            "gate_id": "WOG2525_2_Newton",
            "arena": "Newton/source normalization",
            "map_formula": "worldtube/domain/current descent decides whether source mass is parent-owned instead of fitted GM",
            "required_bundle": "J_H descent; fixed W_source; M_H_ref; kappa/G origin; no readout mask",
            "status": "BLOCKED_MISSING_SOURCE_NORMALIZATION_CERTIFICATE",
        },
        {
            "gate_id": "WOG2525_3_PPN_R10",
            "arena": "PPN/R10",
            "map_formula": "domain/exterior/projector leakage projects into PPN source residuals and short-range source/test normalization",
            "required_bundle": "PPN/R10 projection kernels; source/test charge map; finite component values",
            "status": "BLOCKED_MISSING_ARENA_PROJECTIONS",
        },
        {
            "gate_id": "WOG2525_4_WEP_clock_orbit",
            "arena": "WEP/clock/orbit",
            "map_formula": "tau/ell_J/support/calibration drift maps into material, clock and orbit residuals",
            "required_bundle": "tau lock; material tensor; orbit kernels; fixed calibration protocol",
            "status": "BLOCKED_MISSING_TAU_MATERIAL_ORBIT_BUNDLE",
        },
        {
            "gate_id": "WOG2525_5_local_GR",
            "arena": "local GR/Newton claim",
            "map_formula": "local GR requires source-worldtube descent plus Pi_M lock, EH descent, extra-sector silence and readout gates",
            "required_bundle": "all upstream zero certificates or finite residuals under empirical bounds",
            "status": "BLOCKED_NO_LOCAL_GR_CLAIM",
        },
    ]
    return [base_row(**entry, claim_pass=False) for entry in entries]


def dryrun_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "case_id": "DRY2525_0_support_by_definition",
            "case_description": "claim W_source is fixed because it is defined as supp(J_H)",
            "missing_requirements": "parent J_H descent; tau lock; regular support; no source tail",
            "result_status": "REJECT",
            "blocking_markers": "DEFINITION_NOT_OWNERSHIP",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2525_1_noether_only",
            "case_description": "use Noether conservation or dJ=0 as proof of source-current descent",
            "missing_requirements": "J_H=q^*Jbar_H; matter coupling factorization; same measured source object",
            "result_status": "REJECT",
            "blocking_markers": "CONSERVATION_NOT_DESCENT",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2525_2_stokes_on_moving_domain",
            "case_description": "apply Stokes theorem while A_ext/S_link/source mask move with the residual direction",
            "missing_requirements": "fixed-domain owner or dchi/boundary-crossing rows",
            "result_status": "REJECT",
            "blocking_markers": "MOVING_DOMAIN_TERMS_DROPPED",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2525_3_stationary_as_full_dynamic",
            "case_description": "promote stationary compact-source control branch to full dynamic source-normalization theorem",
            "missing_requirements": "dynamic exchange identity; jump/support theorem; kappa/G origin",
            "result_status": "REJECT",
            "blocking_markers": "STATIONARY_CONTROL_ONLY",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2525_4_observed_GM_backfill",
            "case_description": "normalize M_H_ref or W_source using observed orbital GM",
            "missing_requirements": "parent denominator; no fitted-source feedback",
            "result_status": "REJECT",
            "blocking_markers": "ORBITAL_GM_LAUNDERING",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2525_5_numeric_domain_without_sources",
            "case_description": "score domain/current leakage without component values, units, M_H_ref and source paths",
            "missing_requirements": "component rows; units; source paths; denominator; arena projection",
            "result_status": "REJECT",
            "blocking_markers": "MISSING_DOMAIN_RUNNER_BUNDLE",
            "pass_fail": "BLOCKED_NONCLAIM",
        },
        {
            "case_id": "DRY2525_6_future_complete_domain",
            "case_description": "future source-worldtube/domain row with real zero theorem or source-backed component values",
            "missing_requirements": "none in schema; evidence remains future",
            "result_status": "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST",
            "blocking_markers": "FUTURE_EVIDENCE_ONLY",
            "pass_fail": "TEMPLATE_NONCLAIM",
        },
    ]
    return [base_row(**entry, claim_pass=False) for entry in entries]


def decision_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "decision_id": "DEC2525_0_conditional_gain",
            "decision": "preserve source-current descent as exact conditional route",
            "rationale": "if J_H descends through q and support is regular, source-worldtube motion really can vanish",
            "next_action": "do not repeat the support theorem without new parent action evidence",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2525_1_no_promotion",
            "decision": "do not claim fixed source-worldtube/domain",
            "rationale": "parent q, matter factorization, tau/ell_J, support, boundary, exterior silence and M_H_ref are not jointly signed",
            "next_action": "retain finite domain/current rows",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2525_2_next",
            "decision": "select minimal parent matter-coupling action next",
            "rationale": "one parent action signature is the least handwavy way to sign J_H=q^*Jbar_H, no source-only slots, constants and boundary support together",
            "next_action": "write/test the action-coupling contract or source the first domain-motion inputs",
            "status": "ACTIVE",
        },
        {
            "decision_id": "DEC2525_3_queue",
            "decision": "delay fibre B_h queue by one checkpoint",
            "rationale": "source-worldtube descent remains upstream of the Pi_M/Newton local-GR artery",
            "next_action": "keep fibre route queued after parent matter-coupling action gate",
            "status": "ACTIVE",
        },
    ]
    return [base_row(**entry) for entry in entries]


def next_target_rows() -> list[dict[str, Any]]:
    entries = [
        {
            "route_id": "NEXT2525_0_selected",
            "selection_status": "selected",
            "target_file": "2526-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
            "target_script": "scripts/Y5_R2FR_minimal_parent_matter_coupling_action_or_domain_motion_input_2526.py",
            "objective": "write/test the minimal parent matter-coupling action that would sign source-current descent, no-source-slot, constants, variation-before-readout and boundary/support silence; otherwise keep domain-motion input rows",
            "success_condition": "parent action clauses jointly sign J_H=q^*Jbar_H and fixed W_source, or E_current_descent/E_domain_motion rows remain explicit nonclaim inputs",
            "do_not_do": "do not claim fixed support by definition; do not use Noether conservation alone; do not normalize with observed orbital GM; do not claim Newton/local GR",
        },
        {
            "route_id": "NEXT2525_1_fibre_queue",
            "selection_status": "queued_after_parent_matter_action",
            "target_file": "2527-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "target_script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2527.py",
            "objective": "classify fibre B_h with hidden-visible grammar reentry or finite fibre coefficient rows after the parent matter/source-current lane is narrowed",
            "success_condition": "B_h has theorem-zero evidence or finite nonclaim Z_h/M2_h/B_h/C_h/source-charge rows",
            "do_not_do": "do not let source-worldtube closure erase independent fibre residuals",
        },
    ]
    return [base_row(**entry) for entry in entries]


def branch_copy_rows() -> list[dict[str, Any]]:
    source_map = {
        "worldtube_descent_audit": OUTPUTS["worldtube_descent_audit"],
        "jdomain_bound_rows": OUTPUTS["jdomain_bound_rows"],
        "fixed_domain_gate": OUTPUTS["fixed_domain_gate"],
        "next_target": OUTPUTS["next_target"],
    }
    rows: list[dict[str, Any]] = []
    for key, destination in BRANCH_COPIES.items():
        source = source_map[key]
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        parse_ok, row_count, parse_message = csv_rows_parse(destination)
        rows.append(
            base_row(
                copy_id=f"COPY2525_{key}",
                source_path=str(source.relative_to(ROOT)),
                destination_path=str(destination.relative_to(ROOT)),
                copied=destination.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_message=parse_message,
                status="NONCLAIM_BRANCH_COPY",
            )
        )
    return rows


def falsey(value: Any) -> bool:
    return str(value).strip().lower() in {"false", "0", "no", "not_computed", ""}


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name in {"source_register", "validation"}:
            continue
        for row in rows:
            for key in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "valid_prediction_row",
                "accepted_for_scoring",
                "claim_pass",
                "gate_pass",
            ):
                if key in row and not falsey(row[key]):
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: bool, detail: str = "") -> None:
        checks.append(
            base_row(
                check_id=check_id,
                status="PASS" if status else "FAIL",
                detail=detail,
                valid_for_claim=False,
                claim_allowed=False,
            )
        )

    source_rows = rows_by_name["source_register"]
    audit_rows = rows_by_name["worldtube_descent_audit"]
    gate_rows = rows_by_name["fixed_domain_gate"]
    bound_rows = rows_by_name["jdomain_bound_rows"]

    add("VAL2525_00_sources_exist", all(str(row["path_exists"]) == "True" for row in source_rows))
    add("VAL2525_01_source_needles", all(str(row["source_pass"]) == "True" for row in source_rows))
    add(
        "VAL2525_02_descent_theorem_written",
        any(
            row["audit_id"] == "WTD2525_2_source_current_descent"
            and row["result"] == "EXACT_CONDITIONAL_THEOREM"
            for row in audit_rows
        ),
        "source-current descent theorem is recorded as conditional",
    )
    add(
        "VAL2525_03_support_corollary_written",
        any(
            row["audit_id"] == "WTD2525_3_support_corollary"
            and row["result"] == "EXACT_CONDITIONAL_COROLLARY"
            for row in audit_rows
        ),
        "regular quotient support fixedness is preserved as conditional corollary",
    )
    add(
        "VAL2525_04_zero_not_promoted",
        any(
            row["audit_id"] == "WTD2525_8_verdict"
            and row["result"] == "WORLD_TUBE_DOMAIN_DESCENT_NOT_DERIVED_STAGE_BOUND_ROWS"
            for row in audit_rows
        ),
        "worldtube/domain current descent remains unclaimed",
    )
    add(
        "VAL2525_05_gates_blocked",
        len(gate_rows) == 11 and all(str(row["gate_pass"]) == "False" for row in gate_rows),
        "q/current/tau/support/domain/exterior/boundary/MHref gates all block promotion",
    )
    add(
        "VAL2525_06_bound_rows_complete",
        all(
            any(row["row_id"] == required for row in bound_rows)
            for required in [
                "JDOM2525_0_total",
                "JDOM2525_1_current_descent",
                "JDOM2525_4_domain_mask",
                "JDOM2525_5_boundary_crossing",
                "JDOM2525_8_dynamic_exchange",
                "JDOM2525_11_JPiM_insertion",
                "JDOM2525_12_Qmem_insertion",
            ]
        ),
        "domain/current rows include total, descent, domain mask, boundary, dynamic exchange, JPiM and Qmem insertion",
    )
    add(
        "VAL2525_07_bound_rows_nonclaim",
        all(
            str(row["accepted_for_scoring"]) == "False"
            and str(row["claim_pass"]) == "False"
            and str(row["score_ready"]) == "False"
            for row in bound_rows
        ),
        "all domain/current rows are blocked for scoring",
    )
    add(
        "VAL2525_08_observable_gates_blocked",
        all(
            str(row["claim_pass"]) == "False" and str(row["status"]).startswith("BLOCKED")
            for row in rows_by_name["observable_gate"]
        ),
        "JPiM/Qmem/Newton/PPN/R10/WEP/clock/orbit/local-GR gates remain blocked",
    )
    add(
        "VAL2525_09_dryruns_block_bad_rows",
        all(str(row["claim_pass"]) == "False" for row in rows_by_name["dryrun_results"])
        and all(
            str(row["result_status"]) in {"REJECT", "WOULD_ACCEPT_SCHEMA_IF_REAL_FILES_AND_VALUES_EXIST"}
            for row in rows_by_name["dryrun_results"]
        ),
        "definition-only, Noether-only, moving-Stokes, stationary-as-dynamic, fitted GM and incomplete numeric rows do not score",
    )
    add(
        "VAL2525_10_next_target_parent_matter",
        any(
            row["route_id"] == "NEXT2525_0_selected"
            and "minimal-parent-matter-coupling-action" in row["target_file"]
            for row in rows_by_name["next_target"]
        ),
        "minimal parent matter-coupling action selected next",
    )
    add("VAL2525_11_no_claim_flags", no_claim_flags(rows_by_name))
    add(
        "VAL2525_12_branch_copies",
        all(
            str(row["copied"]) == "True" and str(row["parse_ok"]) == "True"
            for row in rows_by_name["branch_copies"]
        ),
    )
    formalization = ROOT.parent / "formalization-workbench"
    formalization_hits = [
        path
        for path in formalization.rglob("*2525*")
        if ".venv" not in path.parts and "site-packages" not in path.parts
    ] if formalization.exists() else []
    add(
        "VAL2525_13_no_formalization_artifacts",
        len(formalization_hits) == 0,
        ";".join(str(path) for path in formalization_hits),
    )
    add("VAL2525_14_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists())

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2525_CSV_{path.stem}", parse_ok, f"{parse_message}; rows={row_count}")
    for key, path in BRANCH_COPIES.items():
        parse_ok, row_count, parse_message = csv_rows_parse(path)
        add(f"VAL2525_COPY_CSV_{key}", parse_ok, f"{parse_message}; rows={row_count}")

    overall = all(row["status"] == "PASS" for row in checks)
    checks.append(
        base_row(
            check_id="VAL2525_OVERALL",
            status="PASS" if overall else "FAIL",
            detail="2525 preserves source-current descent/support fixedness as conditional, refuses fixed worldtube/domain promotion, stages domain/current rows, and selects minimal parent matter-coupling action next.",
            valid_for_claim=False,
            claim_allowed=False,
        )
    )
    return checks


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 2525 - Source-Worldtube Fixed Domain and Hilbert-Current Descent or Jdomain Bound",
                "",
                "**Current verdict:** the clean route exists: if `J_H=q^*Jbar_H`, `v in ker(Dq)`, support is regular/compact, and `tau`, `ell_J`, `A_ext`, `S_link`, and `M_H_ref` are parent-owned before readout, the source worldtube/domain can be fixed for the `Pi_M` chain-map route. Current MTS does not sign those antecedents together.",
                "",
                "**Main gain:** the remaining source-worldtube debt is now split into explicit nonclaim rows: source-current descent, `tau/ell_J`, support motion, domain mask, boundary crossing, exterior tail, current escape, dynamic exchange, denominator guard, and readout-mask leakage.",
                "",
                "**Claim discipline:** no Newton, local-GR, PPN, WEP, R10, clock, orbit, `J_PiM`, `J_readout`, `J_mem`, `Q_mem`, or GitHub/public claim is made.",
                "",
                "## Source Register",
                md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "found_needles", "source_pass", "role"]),
                "",
                "## Worldtube Descent Audit",
                md_table(rows_by_name["worldtube_descent_audit"], ["audit_id", "claim_piece", "formal_statement", "result", "blocking_gap", "effect"]),
                "",
                "## Fixed Domain Gate",
                md_table(rows_by_name["fixed_domain_gate"], ["gate_id", "required_clause", "formal_condition", "current_status", "if_fail", "gate_pass"]),
                "",
                "## Jdomain Bound Rows",
                md_table(rows_by_name["jdomain_bound_rows"], ["row_id", "quantity", "row_role", "formula_or_bound", "required_inputs", "current_status", "observable_links"]),
                "",
                "## Observable Gate",
                md_table(rows_by_name["observable_gate"], ["gate_id", "arena", "map_formula", "required_bundle", "status", "claim_pass"]),
                "",
                "## Dry Run",
                md_table(rows_by_name["dryrun_results"], ["case_id", "case_description", "missing_requirements", "result_status", "blocking_markers", "pass_fail"]),
                "",
                "## Decision Ledger",
                md_table(rows_by_name["decision_ledger"], ["decision_id", "decision", "rationale", "next_action", "status"]),
                "",
                "## Next Target",
                md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"]),
                "",
                "## Validation",
                md_table(rows_by_name["validation"], ["check_id", "status", "detail"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "worldtube_descent_audit": worldtube_descent_audit_rows(),
        "fixed_domain_gate": fixed_domain_gate_rows(),
        "jdomain_bound_rows": jdomain_bound_rows(),
        "observable_gate": observable_gate_rows(),
        "dryrun_results": dryrun_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
