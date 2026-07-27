from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3565-Y5-R2FR-spin-torsion-hypermomentum-silence-or-P4-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_Y5_SPIN_TORSION_HYPERMOMENTUM_3565"
CHECKPOINT_ID = "3565"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty CSV requested: {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def file_contains(path: Path, token: str) -> bool:
    return token in path.read_text(encoding="utf-8", errors="ignore")


def sources() -> dict[str, Path]:
    return {
        "handoff_3564": RESIDUALS / "P8_Y5_R2FR_3564_NEXT_TARGET.csv",
        "theorem_3564": RESIDUALS / "P8_Y5_R2FR_3564_NONHILBERT_BYPASS_THEOREM.csv",
        "fallback_3564": RESIDUALS / "P8_Y5_R2FR_3564_OFFICIAL_NONHILBERT_FALLBACK_ROWS.csv",
        "spin_audit_2348": RESIDUALS / "P8_Y5_PARENT_QLOC_2348_SPIN_CONNECTION_COFRAME_OWNED_AUDIT.csv",
        "spin_p4_2348": RESIDUALS / "P8_Y5_PARENT_QLOC_2348_AXIAL_TORSION_P4_COMPONENT_ROW.csv",
        "projective_audit_2349": RESIDUALS / "P8_Y5_PARENT_QLOC_2349_PROJECTIVE_TRACE_SILENCE_AUDIT.csv",
        "projective_stack_2349": RESIDUALS / "P8_Y5_PARENT_QLOC_2349_PROJECTIVE_PROOF_STACK.csv",
        "projective_p4_2349": RESIDUALS / "P8_Y5_PARENT_QLOC_2349_P4_PROJECTIVE_COMPONENT_ROW.csv",
        "connection_audit_2374": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_NOHYPERMOMENTUM_LEVICIVITA_PROOF_AUDIT.csv",
        "connection_p4_2374": RESIDUALS / "P8_Y5_PARENT_QLOC_2374_P4_HYPERMOMENTUM_RESIDUAL_ROW.csv",
        "gamma_slot_2375": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_GAMMA_SLOT_SECTOR_AUDIT.csv",
        "nogamma_stack_2375": RESIDUALS / "P8_Y5_PARENT_QLOC_2375_NO_GAMMA_THEOREM_STACK.csv",
        "nogamma_3493": RESIDUALS / "P8_Y5_R2FR_3493_NO_GAMMA_THEOREM_LEDGER.csv",
        "source_hyper_3496": RESIDUALS / "P8_Y5_R2FR_3496_HYPERMOMENTUM_ZERO_DERIVATION.csv",
        "source_kernel_3496": RESIDUALS / "P8_Y5_R2FR_3496_SOURCE_HYPERMOMENTUM_KERNEL_VECTOR.csv",
        "projector_3498": RESIDUALS / "P8_Y5_R2FR_3498_PROJECTOR_NATURALITY_THEOREM.csv",
        "projective_guard_3082": RESIDUALS / "P8_Y5_R2FR_3082_PROJECTIVE_GUARD_REQUIREMENTS.csv",
    }


def source_register(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    roles = {
        "handoff_3564": "declares the 3565 spin/torsion/hypermomentum target",
        "theorem_3564": "imports the non-Hilbert bypass theorem and next-gate selection",
        "fallback_3564": "imports official E_spin non-Hilbert fallback status",
        "spin_audit_2348": "coframe-owned spin-connection theorem and counterbranch",
        "spin_p4_2348": "axial torsion/nonmetricity P4 component rows",
        "projective_audit_2349": "projective trace silence audit",
        "projective_stack_2349": "projective proof stack and parent-action contract",
        "projective_p4_2349": "projective P4 component rows",
        "connection_audit_2374": "no-hypermomentum/Levi-Civita proof audit",
        "connection_p4_2374": "hypermomentum P4 residual row",
        "gamma_slot_2375": "sector-by-sector no-Gamma slot audit",
        "nogamma_stack_2375": "no-Gamma theorem stack",
        "nogamma_3493": "recent exact no-Gamma theorem ledger",
        "source_hyper_3496": "source hypermomentum zero derivation and kernel route",
        "source_kernel_3496": "symbolic source hypermomentum kernel vector",
        "projector_3498": "projector naturality/source-hypermomentum product-rule closure",
        "projective_guard_3082": "all-sector projective guard requirements",
    }
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "source_id": source_id,
            "source_path": str(path),
            "source_path_exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in source_paths.items()
    ]


def theorem_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "STH3565_0_connection_fork",
            "name": "connection fork",
            "statement": "The local source branch has only two disciplined routes: either Gamma_ind/omega_ind is absent from the ordinary/source/readout action, or every independent-connection response is retained as an E_spin/P4 residual.",
            "derivation": "3564 makes spin/torsion the active non-Hilbert head. 2348, 2374, 2375 and 3493 all reduce the issue to variable-domain ownership: no independent connection coordinate gives zero derivative; a live independent connection gives hypermomentum.",
            "required_premises": "same local parent branch; no cancellation between residual heads",
            "current_status": "EXACT_STRUCTURAL_FORK_NONCLAIM",
            "effect": "removes the fog option: prove no-Gamma or carry P4",
            "source_path": str(source_paths["theorem_3564"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "STH3565_1_variable_absence_zero",
            "name": "variable-absence hypermomentum zero",
            "statement": "For any sector action S_i whose argument list excludes Gamma_ind, the independent-connection functional derivative delta S_i / delta Gamma_ind is zero or vacuous on the reduced configuration space.",
            "derivation": "This is the Frechet derivative on a reduced domain. If S_i = Sbar_i[q,e_obs,omega_LC[e_obs],Psi,A,theta,R_post] and Gamma_ind is not a coordinate, partial_Gamma S_i=0. Summing individually zero sector derivatives gives Delta_abs=0 without cancellation.",
            "required_premises": "each matter/source/clock/light/orbit/boundary/readout sector must sign its no-Gamma argument list",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "effect": "would kill E_spin if every sector signs the domain",
            "source_path": str(source_paths["nogamma_3493"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "STH3565_2_owned_spin_connection",
            "name": "owned spin connection zero",
            "statement": "If spinors and spin transport use omega_obs = omega_LC[e_obs] rather than omega_ind, their spin-connection variation is owned by the coframe/Hilbert stress equation and does not create an independent torsion source.",
            "derivation": "delta omega_LC is induced by delta e_obs. The spin backreaction enters the e/coframe equation, while delta S_spin / delta Gamma_ind=0 because Gamma_ind is absent.",
            "required_premises": "parent ordinary action explicitly writes omega_LC[e_obs] for spin/transport and excludes torsionful omega_ind",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "effect": "Delta_spin can be zeroed only inside a signed owned-coframe branch",
            "source_path": str(source_paths["spin_audit_2348"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "STH3565_3_palatini_LC_route",
            "name": "Palatini EH no-hypermomentum route",
            "statement": "If Gamma_ind appears only in an EH/Palatini gravitational block and all matter/source/readout hypermomentum vanishes, the connection equation reduces to Levi-Civita compatibility up to projective gauge.",
            "derivation": "With no hypermomentum source, the Palatini connection equation constrains the affine connection to the metric-compatible Levi-Civita class modulo projective freedom; the projective trace is harmless only after gauge/invariance clauses are signed.",
            "required_premises": "EH-only operator; Delta_lambda^{mu nu}=0; all-sector projective silence or gauge fixing",
            "current_status": "EXACT_CONDITIONAL_ROUTE_NOT_ACTIVE",
            "effect": "dynamic LC route exists but is not live until projective/readout guards close",
            "source_path": str(source_paths["connection_audit_2374"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "STH3565_4_projective_guard",
            "name": "projective trace guard",
            "statement": "A projective trace direction cannot be treated as harmless unless source charge, clocks, WEP material response, light, orbital readout and boundary/domain maps are invariant, gauge-fixed before coupling, or explicitly bounded.",
            "derivation": "Projective freedom in the gravity equation is not enough if observable sectors couple to the trace. 2349 and 3082 require all-sector invariance or a P4 trace residual.",
            "required_premises": "all-sector projective invariance certificate or projective P4 residual with units",
            "current_status": "REQUIRED_GUARD_UNSIGNED",
            "effect": "blocks public Palatini/no-hypermomentum promotion",
            "source_path": str(source_paths["projective_guard_3082"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "STH3565_5_source_hypermomentum_candidate",
            "name": "source hypermomentum product-rule partial closure",
            "statement": "Inside the candidate q/e_obs/tau functor branch, the independent-Gamma source-current commutator closes: delta_Gamma(Pi J_H)=0 when delta_Gamma J_H=0 and delta_Gamma Pi=0.",
            "derivation": "3496 separates the source tail into delta_Gamma J_H and projector/support terms. 3498 proves projector naturality conditionally: if Pi descends through q/e_obs/tau/topology, D_Gamma Pi=0. The product rule then kills this source-hypermomentum subpiece.",
            "required_premises": "minimal parent source-action signature; q/e_obs/tau projector naturality; regular support and fixed reference",
            "current_status": "CANDIDATE_PARTIAL_GATE_ADVANCED",
            "effect": "real progress on source hypermomentum, but not a total spin/torsion zero",
            "source_path": str(source_paths["projector_3498"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "STH3565_6_total_verdict",
            "name": "total E_spin verdict",
            "statement": "E_spin is not zeroed in the live corpus: ordinary matter/spin are promising conditional zeros, source hypermomentum has a candidate product-rule closure, but source/readout/boundary/projective and parent-signature clauses are still unsigned.",
            "derivation": "2375 marks source/worldtube, clock, orbit, boundary and projective slots unsigned. 2348 and 2374 refuse public promotion. 3564 requires componentwise zero or absolute fallback.",
            "required_premises": "none; this is the live checkpoint verdict",
            "current_status": "TOTAL_ZERO_NOT_DERIVED_OFFICIAL_P4_FALLBACK",
            "effect": "promote E_spin/P4 residual rows as the official local connection fallback",
            "source_path": str(source_paths["gamma_slot_2375"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "theorem_id": "STH3565_7_parent_action_contract",
            "name": "future parent action contract",
            "statement": "A claim-grade parent action must either declare Arg(S_local) with no Gamma_ind/omega_ind in ordinary/source/readout sectors, or declare the independent affine coefficients and provide sourced P4 bounds and weak-field maps.",
            "derivation": "This follows from the connection fork: absence is a theorem-zero; presence is a residual. A mixed or unstated branch is not a derivation.",
            "required_premises": "one written parent action branch with variable list, source/readout policy and projective policy",
            "current_status": "CONTRACT_READY_NOT_SIGNED",
            "effect": "sets 3566 target",
            "source_path": str(source_paths["nogamma_stack_2375"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def sector_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("SECT3565_0_total", "total ordinary/source/readout branch", "E_spin_abs", "NOT_PARENT_SIGNED_RETAIN_P4", "all component Gamma derivatives zeroed individually, or every live component bounded", "Delta_abs", "gamma_slot_2375"),
        ("SECT3565_1_matter", "ordinary matter", "Delta_matter", "CONDITIONAL_NO_GAMMA_SUPPORTED", "S_matter[Psi,e_obs,omega_LC[e_obs],A,theta] with no Gamma_ind", "zero_if_parent_signature_signed_else_bound", "nogamma_3493"),
        ("SECT3565_2_spin_transport", "spinors and spin transport", "Delta_spin", "CONDITIONAL_OWNED_COFRAME_SUPPORTED", "omega_obs=omega_LC[e_obs] and no torsionful omega_ind", "zero_if_owned_coframe_else_P4S2348", "spin_audit_2348"),
        ("SECT3565_3_source_worldtube", "source mass/worldtube/support", "Delta_source", "CANDIDATE_PARTIAL_ZERO_BUT_SUPPORT_GUARDS_LIVE", "q/e_obs/tau source and projector naturality plus regular support/reference lock", "epsilon_hypermomentum_source_kernel", "source_hyper_3496"),
        ("SECT3565_4_EM_light", "EM/light/lightcone", "Delta_light", "PARTIAL_PUBLIC_HODGE_CONDITIONAL", "public-Hodge EM/light branch and downstream optical readout, no affine Gamma probe", "bound_if_ray_detector_readout_uses_Gamma", "source_hyper_3496"),
        ("SECT3565_5_clock", "clock/frequency standards", "Delta_clock", "UNSIGNED_READOUT_SLOT", "clocks downstream of matter/gauge/e_obs and no Gamma-source current", "P4_clock_component_required", "gamma_slot_2375"),
        ("SECT3565_6_orbit", "orbit/Kepler/GM readout", "Delta_orbit", "UNSIGNED_READOUT_SLOT", "metric geodesic/GM transfer branch, no independent autoparallel Gamma_ind law", "P4_orbit_component_required", "gamma_slot_2375"),
        ("SECT3565_7_boundary", "boundary/domain/improvement", "Delta_boundary", "PARALLEL_GATE_OPEN", "exact/projected-silent boundary or sourced finite flux envelope", "P4_boundary_component_required", "fallback_3564"),
        ("SECT3565_8_projective", "projective trace", "Delta_projective", "PRIVATE_OR_PALATINI_CONDITIONAL_ONLY", "projective trace gauge/fixed/unobservable in every observed sector", "P4_projective_component_required", "projective_audit_2349"),
        ("SECT3565_9_projector", "projector/support map", "Delta_projector_comm", "CANDIDATE_Q_NATURAL_ZERO_NONPUBLIC", "Pi descends through q/e_obs/tau/topology and not Gamma_ind", "zero_candidate_else_KHS3496_6", "projector_3498"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "sector_id": sector_id,
            "sector": sector,
            "residual_symbol": symbol,
            "current_status": status,
            "zero_condition": zero_condition,
            "fallback": fallback,
            "source_path": str(source_paths[source_key]),
            "parent_signed": False,
            "theorem_zero_live": False,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for sector_id, sector, symbol, status, zero_condition, fallback, source_key in rows
    ]


def p4_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    rows = [
        ("P4H3565_0_total", "E_spin_abs", "official spin/torsion/hypermomentum envelope", "abs(Delta_matter)+abs(Delta_spin)+abs(epsilon_hypermomentum_source)+abs(Delta_clock)+abs(Delta_light)+abs(Delta_orbit)+abs(Delta_boundary)+abs(Delta_projective)+abs(Delta_projector_comm)", "dimensionless after local source normalization or declared P4 arena units", "OFFICIAL_NONCLAIM_FALLBACK", "component zero theorems or sourced bounds for every summand; K_spin weak-field map; no-cancellation policy", "fallback_3564"),
        ("P4H3565_1_matter_noGamma", "Delta_matter", "bulk ordinary matter independent-Gamma response", "delta S_matter/delta Gamma_ind", "hypermomentum or normalized response", "ZERO_IF_PARENT_NO_GAMMA_SIGNATURE_SIGNED", "explicit S_matter argument list and no representative Gamma dependence", "nogamma_3493"),
        ("P4H3565_2_spin_owned_or_axial", "Delta_spin", "spinor/spin-transport torsion response", "S_axial_abs + T_trace_abs + Q_weyl_abs + Q_shear_abs + Delta_spin_projective_abs", "normalized hypermomentum envelope", "P4_COMPONENTS_MISSING", "spin branch coefficient c_A,c_T,c_Q,c_Qs; source density; clock/spin bounds", "spin_p4_2348"),
        ("P4H3565_3_source_kernel", "epsilon_hypermomentum_source", "source/worldtube/projector independent-Gamma tail", "sum_i abs(K_i * epsilon_i)", "dimensionless source-tail envelope", "SYMBOLIC_KERNEL_NONCLAIM", "K_i values; support regularity; H_ref lock; Poynting norms; projector naturality or bound", "source_kernel_3496"),
        ("P4H3565_4_clock", "Delta_clock", "clock/frequency affine readout tail", "||delta_Gamma S_clock||/N_clock or arena response", "fractional clock/dimensionless", "MISSING_CLOCK_GAMMA_RESPONSE", "clock action/protocol argument list or clock response kernel", "gamma_slot_2375"),
        ("P4H3565_5_light", "Delta_light", "lightcone/EM optical affine readout tail", "||delta_Gamma S_light||/N_light or Shapiro/optical response", "lightcone/PPN units after projection", "MISSING_LIGHT_GAMMA_RESPONSE", "public-Hodge EM plus detector/ray downstream proof or optical response kernel", "gamma_slot_2375"),
        ("P4H3565_6_orbit", "Delta_orbit", "autoparallel/geodesic/GM-transfer affine tail", "||delta_Gamma S_orbit||/N_orbit", "GM/PPN/orbital residual units", "MISSING_ORBIT_GAMMA_RESPONSE", "geodesic-vs-autoparallel parent clause; GM transfer map; orbit kernel", "gamma_slot_2375"),
        ("P4H3565_7_boundary", "Delta_boundary", "boundary/domain/improvement connection tail", "boundary/projector/local-support Gamma response", "boundary current or dimensionless envelope", "MISSING_BOUNDARY_FLUX_BOUND", "worldtube flux zero theorem or source-backed boundary envelope", "fallback_3564"),
        ("P4H3565_8_projective", "Delta_projective", "projective trace residual", "P_source_trace_abs + P_clock_trace_abs + P_WEP_trace_abs + P_orbit_trace_abs + P_boundary_trace_abs", "projective trace normalization or arena units", "P4_PROJECTIVE_COMPONENTS_MISSING", "all-sector invariance or trace coupling bounds", "projective_p4_2349"),
        ("P4H3565_9_weak_field_map", "K_spin", "weak-field map from E_spin to local tests", "epsilon_local_connection <= K_spin * E_spin_abs", "R10/PPN/WEP/clock/orbital units after projection", "MISSING_K_SPIN_AND_ARENA_MAP", "component basis; units; lab frame; observable kernels; local-test bounds", "connection_p4_2374"),
        ("P4H3565_10_no_cancellation", "sum_abs_components", "policy guard", "claim_allowed = all components zero OR every absolute component bound passes arena limits", "boolean", "ACTIVE_GUARD", "forbid cancellation between unsigned spin/source/readout/projective components", "fallback_3564"),
    ]
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "p4_id": p4_id,
            "quantity": quantity,
            "component": component,
            "formula": formula,
            "units": units,
            "current_status": status,
            "required_inputs": required_inputs,
            "source_path": str(source_paths[source_key]),
            "official_spin_torsion_fallback": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for p4_id, quantity, component, formula, units, status, required_inputs, source_key in rows
    ]


def decision_rows(source_paths: dict[str, Path]) -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3565_0_exact_fork",
            "decision": "accept the no-Gamma-or-P4 fork",
            "reason": "variable absence gives an exact zero; independent connection gives hypermomentum/residuals",
            "consequence": "future work must sign the parent variable list or fill P4 coefficients",
            "status": "FORK_NOW_CANONICAL",
            "source_path": str(source_paths["nogamma_3493"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3565_1_partial_progress",
            "decision": "promote source-hypermomentum product-rule closure as a candidate subresult",
            "reason": "3496 plus 3498 kills delta_Gamma(Pi J_H) inside q/e_obs/tau projector naturality branch",
            "consequence": "source hypermomentum is no longer just missing; it has a conditional kernel theorem and explicit counterterms",
            "status": "CANDIDATE_PARTIAL_GATE_ADVANCED",
            "source_path": str(source_paths["projector_3498"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3565_2_no_public_zero",
            "decision": "do not claim E_spin=0",
            "reason": "source/readout/boundary/projective and parent-signature clauses remain unsigned",
            "consequence": "local GR/Newton connection recovery remains blocked by the official E_spin/P4 fallback",
            "status": "TOTAL_ZERO_NOT_DERIVED",
            "source_path": str(source_paths["gamma_slot_2375"]),
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3565_3_best_next",
            "decision": "write the parent local action variable signature next",
            "reason": "that is the shortest path from conditional theorem to live branch theorem; otherwise numeric P4 coefficients must be sourced",
            "consequence": "3566 targets Arg(S_local) or first spin/P4 coefficient map",
            "status": "NEXT_TARGET_SELECTED",
            "source_path": str(source_paths["handoff_3564"]),
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status": "SPIN_TORSION_TOTAL_ZERO_NOT_DERIVED_OFFICIAL_P4_FALLBACK_SELECTED",
            "strongest_result": "exact no-Gamma/owned-coframe fork plus candidate source-hypermomentum product-rule partial closure",
            "still_missing": "parent local action variable signature, all-sector source/readout no-Gamma clauses, projective all-sector guard, boundary/worldtube flux zero or bound, K_spin weak-field map",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3565_0",
            "target_doc": "3566-Y5-R2FR-parent-local-action-variable-signature-or-first-spin-P4-coefficient.md",
            "target_script": "scripts/Y5_R2FR_3566_parent_local_action_variable_signature_or_first_spin_P4_coefficient.py",
            "objective": "attempt to write the claim-grade parent local action variable signature that omits Gamma_ind/omega_ind from ordinary/source/readout sectors; if it cannot be signed, start the first sourced E_spin/P4 coefficient and weak-field map row",
            "success_gate": "Arg(S_local) signed with no independent connection across all local sectors, or E_spin/P4 gains one real source-backed coefficient/map row",
            "reason": "3565 shows the math fork is exact; only the parent action signature or numeric residual inputs can move the branch now",
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "canonical_item": "spin_torsion_hypermomentum_connection_gate",
            "canonical_status": "OFFICIAL_NONCLAIM_P4_FALLBACK",
            "zero_claim_status": "NOT_DERIVED",
            "conditional_theorem_status": "EXACT_NO_GAMMA_OR_P4_FORK",
            "partial_progress": "source_hypermomentum_product_rule_candidate_closure",
            "next_action": "parent local action variable signature or first E_spin/P4 coefficient",
            "valid_for_claim": False,
        }
    ]


def validate(
    source_paths: dict[str, Path],
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    sector: list[dict[str, object]],
    p4: list[dict[str, object]],
) -> list[dict[str, object]]:
    validations: list[tuple[str, bool, str]] = []
    pre_validation_outputs = {
        output_id: path
        for output_id, path in outputs.items()
        if output_id != "validation"
    }
    validations.append(
        (
            "VAL3565_0_sources_exist",
            all(path.exists() for path in source_paths.values()),
            "all required source paths exist",
        )
    )
    needles = {
        "handoff_3564": "NEXT3564_0",
        "theorem_3564": "NHB3564_5_next_gate",
        "fallback_3564": "FNH3564_1_spin",
        "spin_audit_2348": "SPIN2348_6_verdict",
        "spin_p4_2348": "P4S2348_0_spin_total",
        "projective_audit_2349": "PROJ2349_5_verdict",
        "projective_stack_2349": "PSTACK2349_4_parent_contract",
        "projective_p4_2349": "P4P2349_0_projective_total",
        "connection_audit_2374": "NHL2374_6_verdict",
        "connection_p4_2374": "P4R2374_0_hypermomentum_total",
        "gamma_slot_2375": "NGSA2375_9_verdict",
        "nogamma_stack_2375": "NGT2375_4_result",
        "nogamma_3493": "NGT3493_0_variable_absence",
        "source_hyper_3496": "DER3496_6_verdict",
        "source_kernel_3496": "KHS3496_0_master_envelope",
        "projector_3498": "PNT3498_6_product_rule_closure",
        "projective_guard_3082": "PGRD3082_0_all_sector_invariance",
    }
    validations.append(
        (
            "VAL3565_1_required_needles_found",
            all(path.exists() and file_contains(path, token) for path_id, token in needles.items() for path in [source_paths[path_id]]),
            "all selected source needles found",
        )
    )
    validations.append(
        (
            "VAL3565_2_outputs_exist",
            all(path.exists() for path in pre_validation_outputs.values()),
            "all pre-validation 3565 output files written",
        )
    )
    csvs_parse = True
    parse_details: list[str] = []
    for output_id, path in pre_validation_outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            row_count = len(read_csv(path))
            csvs_parse = csvs_parse and row_count > 0
            parse_details.append(f"{output_id}:{row_count}")
        except Exception as exc:
            csvs_parse = False
            parse_details.append(f"{output_id}:ERROR:{exc}")
    validations.append(("VAL3565_3_csv_parse", csvs_parse, "; ".join(parse_details)))
    theorem_ids = {str(row["theorem_id"]) for row in theorem}
    validations.append(
        (
            "VAL3565_4_exact_fork_present",
            {"STH3565_1_variable_absence_zero", "STH3565_2_owned_spin_connection", "STH3565_3_palatini_LC_route"}.issubset(theorem_ids),
            "exact conditional no-Gamma, owned-spin and Palatini route rows present",
        )
    )
    validations.append(
        (
            "VAL3565_5_partial_source_progress_recorded",
            any(row["theorem_id"] == "STH3565_5_source_hypermomentum_candidate" for row in theorem),
            "source-hypermomentum product-rule partial closure recorded",
        )
    )
    validations.append(
        (
            "VAL3565_6_sector_rows_cover_local_arenas",
            len(sector) >= 10 and {"Delta_clock", "Delta_light", "Delta_orbit", "Delta_projective"}.issubset({str(row["residual_symbol"]) for row in sector}),
            "sector rows include matter, spin, source, clock, light, orbit, boundary and projective arenas",
        )
    )
    validations.append(
        (
            "VAL3565_7_p4_fallback_nonclaim",
            all(str(row["valid_for_claim"]).lower() == "false" and str(row["claim_allowed"]).lower() == "false" for row in p4),
            "all P4 fallback rows remain nonclaim",
        )
    )
    validations.append(
        (
            "VAL3565_8_official_total_fallback_marked",
            any(row["p4_id"] == "P4H3565_0_total" and row["current_status"] == "OFFICIAL_NONCLAIM_FALLBACK" for row in p4),
            "official E_spin total fallback selected",
        )
    )
    formalization_touched = any(FORMALIZATION.rglob("*3565*")) if FORMALIZATION.exists() else False
    validations.append(
        (
            "VAL3565_9_formalization_workbench_untouched",
            not formalization_touched,
            "no 3565 checkpoint output appears in formalization-workbench",
        )
    )
    return [
        {
            "timestamp_utc": now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "passes": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
        }
        for validation_id, passed, detail in validations
    ]


def write_doc(
    outputs: dict[str, Path],
    theorem: list[dict[str, object]],
    sector: list[dict[str, object]],
    p4: list[dict[str, object]],
    decisions: list[dict[str, object]],
    status: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    lines: list[str] = [
        "# 3565 - Spin torsion hypermomentum silence or P4 bound",
        "",
        "## Verdict",
        "3565 makes the connection fork explicit.  The math route is clean: if the local parent action has no independent `Gamma_ind`/`omega_ind` slot, then the spin/torsion/hypermomentum source derivative is zero by variable absence.  If an independent connection is present, it is not a vibe-zero; it becomes the official `E_spin`/P4 residual branch.",
        "",
        "The strongest new movement is narrower but real: source hypermomentum now has a candidate product-rule closure.  In the `q/e_obs/tau` projector-natural branch, `delta_Gamma(Pi J_H)=0` follows from `delta_Gamma J_H=0` and `delta_Gamma Pi=0`.  This does not close total local GR, but it turns one old fog-bank into a precise theorem-or-kernel row.",
        "",
        "Total `E_spin=0` is not claimed.  Parent variable signature, source/readout no-Gamma clauses, all-sector projective silence, boundary/worldtube flux and the `K_spin` weak-field map remain unsigned.",
        "",
        "## What moved",
        "- The connection problem is now a strict fork: no independent connection, or P4 residual.",
        "- Owned-coframe spin and no-Gamma matter are exact conditional theorems, not assumptions.",
        "- Source hypermomentum gains a candidate product-rule closure through projector naturality.",
        "- `E_spin_abs` is promoted as the official nonclaim P4 fallback for this gate.",
        "- Next target is the parent local action variable signature or the first sourced spin/P4 coefficient.",
        "",
        "## Generated outputs",
    ]
    for output_id, path in outputs.items():
        lines.append(f"- `{output_id}`: `{path}`")
    lines.extend(["", "## Theorem stack"])
    for row in theorem:
        lines.append(f"- `{row['theorem_id']}`: {row['statement']}")
    lines.extend(["", "## Sector verdicts"])
    for row in sector:
        lines.append(f"- `{row['sector_id']}` `{row['residual_symbol']}`: {row['current_status']} ({row['zero_condition']})")
    lines.extend(["", "## P4 fallback rows"])
    for row in p4:
        lines.append(f"- `{row['p4_id']}` `{row['quantity']}`: {row['current_status']} ({row['required_inputs']})")
    lines.extend(["", "## Decision ledger"])
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} -> {row['consequence']}")
    lines.extend(["", "## Status"])
    for row in status:
        lines.append(f"- `{row['status']}`: strongest result = {row['strongest_result']}")
    lines.extend(["", "## Validation"])
    for row in validation:
        lines.append(f"- `{row['validation_id']}`: {row['status']} ({row['detail']})")
    lines.extend(
        [
            "",
            "## Next target",
            f"- `{next_target[0]['target_doc']}`",
            f"- Objective: {next_target[0]['objective']}",
        ]
    )
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    source_paths = sources()
    register = source_register(source_paths)
    theorem = theorem_rows(source_paths)
    sector = sector_rows(source_paths)
    p4 = p4_rows(source_paths)
    decisions = decision_rows(source_paths)
    status = status_rows()
    next_target = next_target_rows()
    canonical = canonical_status_rows()
    outputs = {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3565_SOURCE_REGISTER.csv",
        "theorem_stack": RESIDUALS / "P8_Y5_R2FR_3565_SPIN_TORSION_THEOREM_STACK.csv",
        "sector_verdicts": RESIDUALS / "P8_Y5_R2FR_3565_SECTOR_GAMMA_SLOT_VERDICT.csv",
        "p4_fallback_rows": RESIDUALS / "P8_Y5_R2FR_3565_P4_SPIN_HYPERMOMENTUM_BOUND_ROWS.csv",
        "decision_ledger": RESIDUALS / "P8_Y5_R2FR_3565_DECISION_LEDGER.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3565_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3565_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_spin_torsion_hypermomentum_official_fallback_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3565_VALIDATION.csv",
    }
    write_csv(outputs["source_register"], register)
    write_csv(outputs["theorem_stack"], theorem)
    write_csv(outputs["sector_verdicts"], sector)
    write_csv(outputs["p4_fallback_rows"], p4)
    write_csv(outputs["decision_ledger"], decisions)
    write_csv(outputs["status"], status)
    write_csv(outputs["next_target"], next_target)
    write_csv(outputs["canonical_status"], canonical)
    validation = validate(source_paths, outputs, theorem, sector, p4)
    write_csv(outputs["validation"], validation)
    write_doc(outputs, theorem, sector, p4, decisions, status, validation, next_target)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"3565 validation failed: {failed}")
    print(f"wrote {DOC}")
    for output_id, path in outputs.items():
        print(f"{output_id}: {path}")


if __name__ == "__main__":
    main()
