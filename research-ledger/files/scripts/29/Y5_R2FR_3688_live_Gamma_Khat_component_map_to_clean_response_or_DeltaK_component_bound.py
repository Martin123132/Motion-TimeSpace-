from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work")
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3688"
BRANCH_ID = "MTS_R2FR_Y5_LIVE_GAMMA_KHAT_COMPONENT_MAP_TO_CLEAN_RESPONSE_OR_DELTAK_COMPONENT_BOUND_3688"
DOC = ROOT / "3688-Y5-R2FR-live-Gamma-Khat-component-map-to-clean-response-or-DeltaK-component-bound.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
    }


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> tuple[bool, int]:
    try:
        return True, len(load_csv(path))
    except Exception:
        return False, 0


def source_register(ts: str) -> list[dict[str, object]]:
    specs = [
        ("handoff_3687", RESIDUALS / "P8_Y5_R2FR_3687_NEXT_TARGET.csv", "component map", "3687 selected live Gamma/Khat component mapping"),
        ("deltak_3687", RESIDUALS / "P8_Y5_R2FR_3687_DELTAK_DECOMPOSITION_ROWS.csv", "DK3687_6_live_verdict", "DeltaK component split to refine"),
        ("bounds_3687", RESIDUALS / "P8_Y5_R2FR_3687_REDUCED_RESIDUAL_BOUND_ROWS.csv", "RHB3687_1_DeltaK_total", "reduced Helmholtz/DeltaK residual rows"),
        ("symbol_3074", RESIDUALS / "P8_Y5_R2FR_3074_GAMMA_KHAT_SYMBOL_MATCH_LEDGER.csv", "SYM3074_1_Khat", "live Gamma/Khat/q_loc symbol inventory"),
        ("symbol_1281", RESIDUALS / "P8_Y5_R10_1281_GAMMA_KHAT_SYMBOL_MATCH_AUDIT.csv", "GKM1281_3_difference_test", "missing formula/tensor/variation/difference ledger"),
        ("requirements_1284", RESIDUALS / "P8_Y5_R10_1284_LIVE_GAMMA_KHAT_REQUIREMENTS.csv", "LGK1284_2_existing_Khat", "live Gamma/Khat required inputs"),
        ("contract_514", RESIDUALS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv", "MR514_1_Khat_metric_response", "metric-response contract for Khat"),
        ("response_2808", RESIDUALS / "P8_Y5_R2FR_2808_METRIC_RESPONSE_DERIVATION_ATTEMPT.csv", "MRD2808_3_projected_q_loc", "derived obstruction identity with DeltaK"),
        ("connection_3074", RESIDUALS / "P8_Y5_R2FR_3074_CONNECTION_STACK_GRAMMAR_AUDIT.csv", "CSG3074_4_Gamma_eff_reconciliation", "connection-stack grammar and Gamma/Khat reconciliation"),
        ("kconn_zero_3074", RESIDUALS / "P8_Y5_R2FR_3074_KCONN_ZERO_ATTEMPT.csv", "KCZ3074_1_metric_only_zero", "conditional K_conn zero lemma"),
        ("kconn_bound_3074", RESIDUALS / "P8_Y5_R2FR_3074_KCONN_BOUND_VECTOR_NONCLAIM.csv", "KCB3074_1_operator_stack", "K_conn bound vector template"),
        ("helmholtz_1664", RESIDUALS / "P8_Y5_PARENT_QLOC_1664_HELMHOLTZ_OBSTRUCTION.csv", "HOB1664_2_operator_gap", "live Khat operator gap"),
        ("component_1282", RESIDUALS / "P8_Y5_R10_1282_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv", "RCM1282_1_q_loc_vector_lock", "response-doublet physical component map remains open"),
        ("coupling_3629", RESIDUALS / "P8_Y5_R2FR_3629_RESPONSE_DOUBLET_COUPLING_LAW.csv", "CL3629_2_residual_profile", "source coupling produces a finite profile if not zero"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle, relevance in specs:
        text = read_text(path) if path.exists() else ""
        rows.append(
            {
                **base(ts),
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "relevance": relevance,
            }
        )
    return rows


def live_symbol_inventory_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "LSI3688_0_Gamma_eff",
            "Gamma_eff",
            "scalar density / source-local memory readout",
            "clean scalar density Gamma_eff(g,Y,DY,D,...) with units and background subtraction",
            "current corpus names Gamma_eff but lacks source-backed formula, units and parent field list",
            "R_Gamma_owner",
            "NOT_LIVE_ACTION_OWNED",
        ),
        (
            "LSI3688_1_Khat",
            "K_hat^{mu nu}",
            "tensor appearing in q_loc identity",
            "K_metric^{mu nu}[Gamma_eff] from delta[sqrt(-g)Gamma_eff]/delta g_mu_nu",
            "current corpus names K_hat but lacks explicit tensor components and boundary convention",
            "R_DeltaK_live_tensor",
            "LIVE_TENSOR_COMPONENTS_MISSING",
        ),
        (
            "LSI3688_2_q_loc",
            "q_loc^nu",
            "projected local residual",
            "P_loc(nabla_mu T_GK^{mu nu}) plus explicit DeltaK/Euler/boundary terms",
            "identity shape exists, but P_loc ownership, units and observable projection are unsigned",
            "R_q_profile_inputs",
            "PROFILE_IDENTITY_READY_INPUTS_MISSING",
        ),
        (
            "LSI3688_3_K_conn",
            "K_conn / connection-stack response",
            "operator/Hodge/domain/connection residue",
            "metric/coframe-derived LC response already absorbed into K_metric or GR-side variation",
            "conditional metric-only zero exists, but parent field inventory/no independent connection/no hypermomentum are unsigned",
            "R_DeltaK_conn",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
        ),
        (
            "LSI3688_4_P4_fallback",
            "P4 torsion/nonmetricity/projective/hypermomentum fallback",
            "non-LC geometry residue",
            "absent or constrained by parent Palatini/metric-only branch",
            "fallback remains legal because matter/source/readout connection independence is unsigned",
            "R_DeltaK_P4",
            "NONLC_FALLBACK_RETAINED",
        ),
        (
            "LSI3688_5_boundary_domain",
            "boundary/domain/corner response",
            "exact/improvement/fixed-reference response",
            "K_boundary[Theta_GK,B_GK,corners,reference] with no-flux projection",
            "boundary and moving-domain terms remain open",
            "R_DeltaK_boundary",
            "BOUNDARY_NO_FLUX_OPEN",
        ),
        (
            "LSI3688_6_flux",
            "EM/Poynting/wave flux stress",
            "physical flux sector if present",
            "K_flux^{mu nu}=W_AB F^{A mu rho}F^B{}^{nu}{}_{rho} as ordinary physical stress/current",
            "no live F,W,J owner in the local-GR q_loc branch; may be an EM branch, not a closure trick",
            "R_DeltaK_flux",
            "SEPARATE_PHYSICAL_BRANCH",
        ),
    ]
    return [
        {
            **base(ts),
            "inventory_id": inventory_id,
            "symbol": symbol,
            "live_role": live_role,
            "clean_response_slot": clean_response_slot,
            "current_evidence": current_evidence,
            "residual_if_unmatched": residual_if_unmatched,
            "status": status,
            "claim_allowed": False,
            "score_ready": False,
        }
        for inventory_id, symbol, live_role, clean_response_slot, current_evidence, residual_if_unmatched, status in specs
    ]


def component_match_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "CMM3688_0_convention",
            "sign/volume convention",
            "T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}",
            "MRD2808_1 derives the convention for any action-defined scalar density",
            "MATCHED_FOR_CLEAN_KMETRIC_NOT_LIVE_KHAT",
            "none for formal clean convention; live Khat still separate",
            "This is a real matched rung: no sign smuggling is needed once K_metric is defined variationally.",
        ),
        (
            "CMM3688_1_scalar_density",
            "Gamma_eff action owner",
            "Gamma_eff=Gamma_eff(g,Y,DY,D,...) with units, background subtraction and no data selector",
            "symbol appears but current ledgers mark formula/action owner missing",
            "UNMATCHED",
            "R_Gamma_owner",
            "Cannot compute live K_metric without this formula.",
        ),
        (
            "CMM3688_2_gradient_elastic",
            "K_grad",
            "K_grad^{mu nu}=G_AB D^mu Y^A D^nu Y^B",
            "clean response branch supplies the target; no live Khat gradient component table found",
            "UNMATCHED_COMPONENT",
            "R_DeltaK_grad",
            "A future component table can close this by identifying the anisotropic gradient stress.",
        ),
        (
            "CMM3688_3_coefficient_response",
            "K_coeff",
            "K_coeff^{mu nu}=metric response of G_AB, M_AB and D_mu coefficients",
            "current files require derivative/boundary accounting but do not list coefficient responses",
            "UNMATCHED_COMPONENT",
            "R_DeltaK_coeff",
            "Coefficient metric dependence is where hidden fitted geometry can leak in.",
        ),
        (
            "CMM3688_4_connection_stack",
            "K_conn",
            "K_conn_bar <= C_conn(||delta Gamma_LC|| O1 + ||delta G_AB|| O2 + ||delta star|| O3 + ||delta D|| O4)",
            "3074 supplies a nonclaim operator-stack bound template and a conditional metric-only zero lemma",
            "BOUND_TEMPLATE_FOUND_NOT_ZERO",
            "R_DeltaK_conn",
            "This is useful: K_conn is not vague anymore; it has a concrete bound interface.",
        ),
        (
            "CMM3688_5_projector_readout",
            "K_projector",
            "K_projector[delta_g P_loc, delta_g q, delta_g Y]",
            "P_loc/q ownership remains unsigned in 3686/3687 and response-doublet component map is not full-rank",
            "UNMATCHED_COMPONENT",
            "R_DeltaK_projector",
            "Projection cannot be allowed to hide a force component.",
        ),
        (
            "CMM3688_6_boundary_domain",
            "K_boundary",
            "K_boundary[Theta_GK,B_GK,corners,reference]",
            "boundary/no-flux ledgers remain conditional",
            "UNMATCHED_COMPONENT",
            "R_DeltaK_boundary",
            "Bulk action progress does not by itself control linked-surface mass or force leakage.",
        ),
        (
            "CMM3688_7_P4_nonLC",
            "K_P4",
            "torsion + nonmetricity + projective + hypermomentum residues",
            "3074 keeps P4 fallback required unless no independent connection/matter hypermomentum closes",
            "FALLBACK_COMPONENT_RETAINED",
            "R_DeltaK_P4",
            "This is the non-GR geometry escape hatch that must be either derived silent or bounded.",
        ),
        (
            "CMM3688_8_flux",
            "K_flux",
            "W_AB F^{A mu rho}F^B{}^{nu}{}_{rho}",
            "clean stress slot exists as physical EM/wave sector; no live local-GR branch owner",
            "PHYSICAL_BRANCH_SEPARATE",
            "R_DeltaK_flux",
            "Poynting-vector intuition is preserved only as explicit physical stress/current, not hidden q_loc closure.",
        ),
        (
            "CMM3688_9_verdict",
            "live Delta_K=0",
            "all live Khat components match K_grad+K_coeff+K_projector+K_boundary+K_flux under one convention",
            "only the formal convention and K_conn bound interface are currently strong; tensor components are missing",
            "DELTAK_ZERO_NOT_CLAIMED_COMPONENT_BOUNDS_REQUIRED",
            "R_DeltaK_total",
            "3688 converts the old Khat gap into a concrete component worklist.",
        ),
    ]
    return [
        {
            **base(ts),
            "match_id": match_id,
            "component": component,
            "clean_target": clean_target,
            "current_evidence": current_evidence,
            "match_status": match_status,
            "residual_if_unmatched": residual_if_unmatched,
            "interpretation": interpretation,
            "claim_allowed": False,
            "score_ready": False,
        }
        for match_id, component, clean_target, current_evidence, match_status, residual_if_unmatched, interpretation in specs
    ]


def deltak_bound_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "DKB3688_0_total",
            "abs(R_DeltaK_total)/N_H",
            "(|R_Gamma_owner|+|R_DeltaK_live_tensor|+|R_DeltaK_grad|+|R_DeltaK_coeff|+|R_DeltaK_conn|+|R_DeltaK_projector|+|R_DeltaK_boundary|+|R_DeltaK_P4|+|R_DeltaK_flux|)/N_H",
            "dimensionless no-cancellation envelope",
            "FORMULA_READY_COMPONENT_INPUTS_MISSING",
            "full live-Khat mismatch envelope",
            "CMM3688_9_verdict",
        ),
        (
            "DKB3688_1_Gamma_owner",
            "abs(R_Gamma_owner)/N_H",
            "MISSING_GAMMA_EFF_FORMULA_UNITS_PARENT_FIELD_LIST_BACKGROUND_SUBTRACTION",
            "dimensionless",
            "MISSING_SCALAR_DENSITY_OWNER",
            "needed before live K_metric computation",
            "LSI3688_0_Gamma_eff",
        ),
        (
            "DKB3688_2_live_tensor",
            "abs(R_DeltaK_live_tensor)/N_H",
            "MISSING_KHAT_LIVE_COMPONENT_TABLE_AND_INDEX_CONVENTION",
            "dimensionless",
            "MISSING_LIVE_TENSOR_COMPONENTS",
            "the direct tensor comparison cannot run without this",
            "LSI3688_1_Khat",
        ),
        (
            "DKB3688_3_grad",
            "abs(R_DeltaK_grad)/N_H",
            "MISSING_KHAT_GRADIENT_ELASTIC_COMPONENT_MATCH",
            "dimensionless",
            "MISSING_GRADIENT_COMPONENT",
            "match K_hat anisotropic part to G_AB D^mu Y^A D^nu Y^B",
            "CMM3688_2_gradient_elastic",
        ),
        (
            "DKB3688_4_coeff",
            "abs(R_DeltaK_coeff)/N_H",
            "MISSING_DELTA_G_GAB_MAB_DMU_RESPONSE",
            "dimensionless",
            "MISSING_COEFFICIENT_RESPONSE",
            "metric dependence of response coefficients must be explicit",
            "CMM3688_3_coefficient_response",
        ),
        (
            "DKB3688_5_conn",
            "abs(R_DeltaK_conn)/N_H",
            "C_conn(||delta Gamma_LC|| O1_bar + ||delta G_AB|| O2_bar + ||delta star|| O3_bar + ||delta D|| O4_bar)/N_H",
            "dimensionless after operator/domain normalization",
            "BOUND_TEMPLATE_NONNUMERIC",
            "3074 gives the first concrete K_conn bound interface",
            "CMM3688_4_connection_stack",
        ),
        (
            "DKB3688_6_projector",
            "abs(R_DeltaK_projector)/N_H",
            "MISSING_DELTA_G_PLOC_Q_READOUT_COMMUTATOR_BOUND",
            "dimensionless",
            "MISSING_PROJECTOR_RESPONSE",
            "P_loc/q variation must not be a data-chosen projector trick",
            "CMM3688_5_projector_readout",
        ),
        (
            "DKB3688_7_boundary",
            "abs(R_DeltaK_boundary)/N_H",
            "MISSING_THETA_BGK_CORNER_REFERENCE_NOFLUX_BOUND",
            "dimensionless",
            "MISSING_BOUNDARY_RESPONSE",
            "linked-surface leakage remains a physical local-source risk",
            "CMM3688_6_boundary_domain",
        ),
        (
            "DKB3688_8_P4",
            "abs(R_DeltaK_P4)/N_H",
            "MISSING_TORSION_NONMETRICITY_PROJECTIVE_HYPERMOMENTUM_BOUND",
            "dimensionless",
            "P4_FALLBACK_REQUIRED_NONCLAIM",
            "non-LC residues must be excluded or bounded",
            "CMM3688_7_P4_nonLC",
        ),
        (
            "DKB3688_9_flux",
            "abs(R_DeltaK_flux)/N_H",
            "MISSING_EXPLICIT_F_W_J_FLUX_STRESS_OR_ABSENCE_THEOREM",
            "dimensionless",
            "SEPARATE_EM_FLUX_INPUT_MISSING",
            "EM/Poynting sector can be physical but not a hidden local-GR zero",
            "CMM3688_8_flux",
        ),
    ]
    return [
        {
            **base(ts),
            "bound_id": bound_id,
            "quantity": quantity,
            "bound_or_formula": bound_or_formula,
            "units": units,
            "status": status,
            "interpretation": interpretation,
            "source_anchor": source_anchor,
            "claim_allowed": False,
            "score_ready": False,
        }
        for bound_id, quantity, bound_or_formula, units, status, interpretation, source_anchor in specs
    ]


def qloc_profile_input_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        (
            "QPI3688_0_identity",
            "q_loc profile identity",
            "q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho - nabla_mu Delta_K^{mu rho})",
            "derived obstruction identity from 2808/3686/3687",
            "READY_SYMBOLIC_IDENTITY",
            "use this for PPN/R10/clock/orbital projections once components are sourced",
        ),
        (
            "QPI3688_1_Euler_source",
            "E_A / J_A source term",
            "E_A=L_AB Y^B - J_A - B_A",
            "3629 gives Z=-(L^-1)J + boundary Green terms if J_A is not zero",
            "MISSING_JA_ZERO_OR_COEFFICIENT",
            "this is the coupling key: derive J_A=0 or bound the induced profile",
        ),
        (
            "QPI3688_2_DeltaK_divergence",
            "nabla_mu Delta_K^{mu rho}",
            "divergence of the DeltaK component vector",
            "3688 names every component but numeric/operator coefficients remain missing",
            "MISSING_COMPONENT_DIVERGENCE_BOUNDS",
            "turns Khat mismatch into observable local force residual",
        ),
        (
            "QPI3688_3_Ploc",
            "P_loc projector/readout",
            "parent-owned P_loc with units and no data-chosen projection",
            "P_loc ownership remains open",
            "MISSING_PLOC_OWNER_AND_COMMUTATOR",
            "needed before local tests can be trusted",
        ),
        (
            "QPI3688_4_arena_projection",
            "test arena projection",
            "map q_loc profile to PPN, R10, clocks, orbital, WEP and EM stress arenas",
            "existing arena rows are template/nonclaim",
            "MISSING_ARENA_COEFFICIENTS",
            "testing branch should start only after q_loc components have units",
        ),
    ]
    return [
        {
            **base(ts),
            "input_id": input_id,
            "input": input_name,
            "formula_or_requirement": formula_or_requirement,
            "current_evidence": current_evidence,
            "status": status,
            "next_use": next_use,
            "claim_allowed": False,
            "score_ready": False,
        }
        for input_id, input_name, formula_or_requirement, current_evidence, status, next_use in specs
    ]


def decision_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("DEC3688_0_result", "LIVE_COMPONENT_MAP_BUILT_DELTAK_ZERO_NOT_CLAIMED", "the live symbols are inventoried and mapped to clean response slots", "use the component matrix instead of repeating broad Khat-missing prose"),
        ("DEC3688_1_progress", "KCONN_BOUND_INTERFACE_FOUND", "connection-stack residue has a concrete nonclaim bound template from 3074", "source constants C_conn/O_i/domain norms before claiming smallness"),
        ("DEC3688_2_core_gap", "LIVE_KHAT_TENSOR_TABLE_MISSING", "the direct Khat=Kmetric test cannot run without component rows", "either derive canonical live Khat from clean response or quarantine old Khat as legacy residual"),
        ("DEC3688_3_coupling", "JA_COUPLING_IS_NEXT_PHYSICAL_KEY", "even if DeltaK is cleaned, q_loc still has E_A/J_A source profile", "go after J_A=0 theorem or finite coefficient bound soon"),
        ("DEC3688_4_next", "NEXT_BEST_TARGET", "least ambiguous leap is to canonicalize live Gamma/Khat definitions from the clean response action", "run 3689 canonical Gamma/Khat adoption law or legacy-symbol quarantine"),
        ("DEC3688_5_private", "PRIVATE_NONCLAIM", "no local-GR/Newton/public claim follows", "continue private derivation"),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "status": status,
            "decision": decision,
            "next_action": next_action,
            "claim_allowed": False,
            "score_ready": False,
        }
        for decision_id, status, decision, next_action in specs
    ]


def claim_gate_rows(ts: str) -> list[dict[str, object]]:
    specs = [
        ("CG3688_0_Khat_match", "claim live K_hat=K_metric", "BLOCKED_LIVE_TENSOR_TABLE", "the component table and index/boundary convention are missing"),
        ("CG3688_1_DeltaK_zero", "claim Delta_K=0", "BLOCKED_COMPONENT_RESIDUALS", "gradient, coefficient, connection, projector, boundary, P4 and flux pieces remain unmatched or nonnumeric"),
        ("CG3688_2_q_loc_zero", "claim q_loc^nu=0", "BLOCKED_JA_DELTAK_BOUNDARY_PLOC", "q_loc profile still contains source, DeltaK, boundary and projector terms"),
        ("CG3688_3_Newton_GR", "claim derived Newton/local-GR limit", "BLOCKED_LOCAL_SOURCE_BRANCH", "Gamma/Khat and J_A coupling are not signed"),
        ("CG3688_4_public_or_github", "public/GitHub promotion", "BLOCKED_PRIVATE", "private checkpoint only"),
    ]
    return [
        {
            **base(ts),
            "claim_gate_id": claim_gate_id,
            "gate": gate,
            "status": status,
            "reason": reason,
            "claim_allowed": False,
            "score_ready": False,
        }
        for claim_gate_id, gate, status, reason in specs
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "STATUS3688_0",
            "status": "LIVE_COMPONENT_MAP_BUILT_KCONN_BOUND_INTERFACE_FOUND_DELTAK_ZERO_NOT_CLAIMED",
            "summary": "3688 inventories live Gamma_eff/K_hat/q_loc/K_conn/P4/boundary/flux symbols, maps them to the clean response slots, records the exact formal convention match and the K_conn bound interface, and retains a named DeltaK component vector because the live Khat tensor table is absent.",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def next_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3688_0",
            "target_doc": "3689-Y5-R2FR-canonical-Gamma-Khat-adoption-law-or-legacy-symbol-quarantine.md",
            "target_script": "scripts/Y5_R2FR_3689_canonical_Gamma_Khat_adoption_law_or_legacy_symbol_quarantine.py",
            "objective": "try the leap forward: define canonical live Gamma_eff and K_hat by the clean response action and check backward-compatibility with legacy Gamma/Khat/q_loc usage; if incompatible, quarantine old symbols as explicit DeltaK residuals",
            "success_gate": "either a canonical action-defined Gamma/Khat branch is adopted for future derivations with legacy symbols quarantined, or the adoption fails with exact incompatibility rows and no local-GR/Newton claim",
            "claim_allowed": False,
            "score_ready": False,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    inventory: list[dict[str, object]],
    matches: list[dict[str, object]],
    bounds: list[dict[str, object]],
    qloc: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines = [
        "# 3688 - Live Gamma/Khat component map to clean response or DeltaK component bound",
        "",
        f"**Status:** {status[0]['status']}",
        "",
        "This checkpoint turns the live `Gamma_eff/K_hat` gap into a component map. It does not invent missing tensors. It records the clean formal convention that is already derived, finds the concrete `K_conn` bound interface, and carries every unmatched live piece as a named `Delta_K` component.",
        "",
        "## Main result",
        "",
        "Formal clean convention matched:",
        "",
        "`T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_metric^{mu nu}`.",
        "",
        "Live mismatch definition:",
        "",
        "`Delta_K^{mu nu}=K_hat_live^{mu nu}-K_metric^{mu nu}[Gamma_eff]`.",
        "",
        "Component envelope:",
        "",
        "`abs(R_DeltaK_total)/N_H <= (|R_Gamma_owner|+|R_DeltaK_live_tensor|+|R_DeltaK_grad|+|R_DeltaK_coeff|+|R_DeltaK_conn|+|R_DeltaK_projector|+|R_DeltaK_boundary|+|R_DeltaK_P4|+|R_DeltaK_flux|)/N_H`.",
        "",
        "Connection-stack bound interface:",
        "",
        "`K_conn_bar <= C_conn(||delta Gamma_LC|| O1_bar + ||delta G_AB|| O2_bar + ||delta star|| O3_bar + ||delta D|| O4_bar)`.",
        "",
        "q_loc profile retained:",
        "",
        "`q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho - nabla_mu Delta_K^{mu rho})`.",
        "",
        "## Live symbol inventory",
    ]
    for row in inventory:
        lines.append(f"- `{row['inventory_id']}`: {row['status']} - `{row['symbol']}` -> {row['residual_if_unmatched']}")
    lines.extend(["", "## Component match matrix"])
    for row in matches:
        lines.append(f"- `{row['match_id']}`: {row['match_status']} - {row['component']} -> {row['residual_if_unmatched']}; {row['interpretation']}")
    lines.extend(["", "## DeltaK component bounds"])
    for row in bounds:
        lines.append(f"- `{row['bound_id']}`: {row['status']} - `{row['quantity']}` -> `{row['bound_or_formula']}`; {row['interpretation']}")
    lines.extend(["", "## q_loc profile inputs"])
    for row in qloc:
        lines.append(f"- `{row['input_id']}`: {row['status']} - {row['input']} -> {row['next_use']}")
    lines.extend(["", "## Decisions"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['status']} - {row['decision']} -> {row['next_action']}")
    lines.extend(["", "## Claim gates"])
    for row in gates:
        lines.append(f"- `{row['claim_gate_id']}`: {row['status']} - {row['gate']} because {row['reason']}")
    lines.extend(["", "## Next target", f"`{next_target[0]['target_doc']}` via `{next_target[0]['target_script']}`.", "", "## Sources"])
    for row in sources:
        lines.append(f"- `{row['source_id']}`: `{row['source_path']}` exists={row['exists']} needle_found={row['needle_found']}")
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate(
    ts: str,
    output_paths: list[Path],
    sources: list[dict[str, object]],
    inventory: list[dict[str, object]],
    matches: list[dict[str, object]],
    bounds: list[dict[str, object]],
    qloc: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    status: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(validation_id: str, ok: bool, detail: str) -> None:
        rows.append(
            {
                "timestamp_utc": ts,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "validation_id": validation_id,
                "result": "PASS" if ok else "FAIL",
                "detail": detail,
            }
        )

    csv_status = [parse_csv(path) for path in output_paths if path.suffix.lower() == ".csv"]
    generated = sources + inventory + matches + bounds + qloc + decisions + gates + status + next_target
    doc_text = read_text(DOC)
    leaks: list[Path] = []
    if FORMALIZATION.exists():
        for pattern in ["*Y5_R2FR_3688*", "3688-Y5-R2FR-*", "P8_Y5*3688*"]:
            leaks.extend(FORMALIZATION.rglob(pattern))

    inventory_by_id = {str(row["inventory_id"]): row for row in inventory}
    match_by_id = {str(row["match_id"]): row for row in matches}
    bound_by_id = {str(row["bound_id"]): row for row in bounds}
    qloc_by_id = {str(row["input_id"]): row for row in qloc}
    required_components = [
        "R_Gamma_owner",
        "R_DeltaK_live_tensor",
        "R_DeltaK_grad",
        "R_DeltaK_coeff",
        "R_DeltaK_conn",
        "R_DeltaK_projector",
        "R_DeltaK_boundary",
        "R_DeltaK_P4",
        "R_DeltaK_flux",
    ]
    total_formula = str(bound_by_id["DKB3688_0_total"]["bound_or_formula"])

    add("VAL3688_0_sources_exist", all(row["exists"] for row in sources), "every cited source path exists")
    add("VAL3688_1_needles_found", all(row["needle_found"] for row in sources), "every source needle found")
    add("VAL3688_2_outputs_exist", all(path.exists() for path in output_paths), "all expected 3688 outputs written")
    add("VAL3688_3_csv_parse", all(ok and count > 0 for ok, count in csv_status), "all generated CSVs parse with rows")
    add("VAL3688_4_inventory", inventory_by_id["LSI3688_0_Gamma_eff"]["status"] == "NOT_LIVE_ACTION_OWNED" and inventory_by_id["LSI3688_1_Khat"]["status"] == "LIVE_TENSOR_COMPONENTS_MISSING", "live Gamma/Khat inventory records missing owner/tensor")
    add("VAL3688_5_formal_match", match_by_id["CMM3688_0_convention"]["match_status"] == "MATCHED_FOR_CLEAN_KMETRIC_NOT_LIVE_KHAT", "formal clean convention is matched but not live Khat")
    add("VAL3688_6_kconn_interface", "C_conn" in bound_by_id["DKB3688_5_conn"]["bound_or_formula"] and match_by_id["CMM3688_4_connection_stack"]["match_status"] == "BOUND_TEMPLATE_FOUND_NOT_ZERO", "K_conn bound interface is captured")
    add("VAL3688_7_total_components", all(component in total_formula for component in required_components), "DeltaK total envelope contains all named components")
    add("VAL3688_8_q_loc_profile", "q_loc^nu" in qloc_by_id["QPI3688_0_identity"]["formula_or_requirement"] and "Delta_K" in qloc_by_id["QPI3688_0_identity"]["formula_or_requirement"], "q_loc profile identity retained")
    add("VAL3688_9_next_target", next_target[0]["target_doc"].startswith("3689-") and "canonical" in next_target[0]["objective"], "3689 targets canonical adoption/quarantine")
    add("VAL3688_10_claim_gates_blocked", all(row["claim_allowed"] is False and row["score_ready"] is False for row in gates), "claim gates remain blocked")
    add("VAL3688_11_all_nonclaim", not any(str(row.get("valid_for_claim", "")).lower() == "true" or str(row.get("claim_allowed", "")).lower() == "true" or str(row.get("score_ready", "")).lower() == "true" for row in generated), "all generated rows remain nonclaim and unscoreable")
    add("VAL3688_12_doc_written", "R_DeltaK_total" in doc_text and "K_conn_bar" in doc_text and "q_loc^nu" in doc_text, "doc records DeltaK envelope, Kconn interface and qloc profile")
    add("VAL3688_13_no_formalization_leak", not leaks, "no 3688 checkpoint files in formalization-workbench")
    return rows


def main() -> int:
    ts = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    sources = source_register(ts)
    inventory = live_symbol_inventory_rows(ts)
    matches = component_match_rows(ts)
    bounds = deltak_bound_rows(ts)
    qloc = qloc_profile_input_rows(ts)
    decisions = decision_rows(ts)
    gates = claim_gate_rows(ts)
    status = status_rows(ts)
    next_target = next_rows(ts)
    outputs = {
        "sources": RESIDUALS / "P8_Y5_R2FR_3688_SOURCE_REGISTER.csv",
        "inventory": RESIDUALS / "P8_Y5_R2FR_3688_LIVE_SYMBOL_INVENTORY.csv",
        "matches": RESIDUALS / "P8_Y5_R2FR_3688_COMPONENT_MATCH_MATRIX.csv",
        "bounds": RESIDUALS / "P8_Y5_R2FR_3688_DELTAK_COMPONENT_BOUND_ROWS.csv",
        "qloc": RESIDUALS / "P8_Y5_R2FR_3688_QLOC_PROFILE_INPUT_ROWS.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3688_DECISION_ROWS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3688_CLAIM_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3688_STATUS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3688_NEXT_TARGET.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3688_VALIDATION.csv",
    }
    write_csv(outputs["sources"], sources)
    write_csv(outputs["inventory"], inventory)
    write_csv(outputs["matches"], matches)
    write_csv(outputs["bounds"], bounds)
    write_csv(outputs["qloc"], qloc)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["status"], status)
    write_csv(outputs["next"], next_target)
    write_doc(sources, inventory, matches, bounds, qloc, decisions, gates, status, next_target)
    generated_paths = [path for key, path in outputs.items() if key != "validation"] + [DOC]
    validation = validate(ts, generated_paths, sources, inventory, matches, bounds, qloc, decisions, gates, status, next_target)
    write_csv(outputs["validation"], validation)
    failures = [row for row in validation if row["result"] != "PASS"]
    if failures:
        print(f"3688 validation failed: {failures}", file=sys.stderr)
        return 1
    print("wrote 3688 checkpoint: live component map built; Kconn bound interface found; DeltaK zero not claimed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
