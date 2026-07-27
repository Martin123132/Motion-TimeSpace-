from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3463-Y5-R2FR-single-source-current-owner-from-Noether-Poynting-flow-or-WEP-tau-map-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3463": Path(__file__).resolve(),
    "doc_3462": ROOT / "3462-Y5-R2FR-no-source-only-slot-parent-grammar-or-first-WEP-sY5-row-under-AX1090.md",
    "grammar_3462": OUT / "P8_Y5_R2FR_3462_OBSERVABLE_GRAMMAR_DERIVATION_AUDIT.csv",
    "counter_3462": OUT / "P8_Y5_R2FR_3462_NO_GO_COUNTERMODEL.csv",
    "wep_3462": OUT / "P8_Y5_R2FR_3462_WEP_SY5_PRODUCT_ROW.csv",
    "chain_3462": OUT / "P8_Y5_R2FR_3462_BOUND_CHAIN_UPDATE.csv",
    "doc_3460": ROOT / "3460-Y5-R2FR-source-current-owner-for-doublet-or-Y5-source-normalization-bound-under-AX1090.md",
    "owner_3460": OUT / "P8_Y5_R2FR_3460_Y5_OWNER_THEOREM_ATTEMPT.csv",
    "decomp_3460": OUT / "P8_Y5_R2FR_3460_SOURCE_CURRENT_DECOMPOSITION.csv",
    "bounds_3460": OUT / "P8_Y5_R2FR_3460_Y5_BOUND_PLUG_ROWS.csv",
    "doc_3459": ROOT / "3459-Y5-R2FR-response-doublet-energy-identity-source-zero-or-q_loc-bound-under-AX1090.md",
    "bounds_3459": OUT / "P8_Y5_R2FR_3459_RESIDUAL_BOUNDS.csv",
    "ward_universality": OUT / "P8_source_current_Ward_universality_CONTRACT.csv",
    "ward_owner": OUT / "P8_Ward_source_owner_identity_CONTRACT.csv",
    "parent_terms": OUT / "P8_source_owner_parent_action_terms_CONTRACT.csv",
    "normalization_stack": OUT / "P8_SOURCE_NORMALIZATION_THEOREM_STACK.csv",
    "doc_1937": ROOT / "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md",
    "action_1937": OUT / "P8_Y5_PARENT_QLOC_1937_MINIMAL_PARENT_MATTER_ACTION_SIGNATURE.csv",
    "hilbert_1937": OUT / "P8_Y5_PARENT_QLOC_1937_HILBERT_SOURCE_THEOREM.csv",
    "doc_1938": ROOT / "1938-Y5-R2FR-Bianchi-Ward-conservation-and-Newtonian-limit-of-candidate-Hilbert-action.md",
    "ward_1938": OUT / "P8_Y5_PARENT_QLOC_1938_WARD_BIANCHI_CONSERVATION_THEOREM.csv",
    "newton_1938": OUT / "P8_Y5_PARENT_QLOC_1938_NEWTONIAN_LIMIT_DERIVATION.csv",
    "blockers_1938": OUT / "P8_Y5_PARENT_QLOC_1938_GRAVITY_OPERATOR_BLOCKERS.csv",
    "doc_1939": ROOT / "1939-Y5-R2FR-parent-gravity-operator-EH-or-R11-residual-Newtonian-law.md",
    "eh_1939": OUT / "P8_Y5_PARENT_QLOC_1939_EH_NEWTONIAN_THEOREM.csv",
    "doc_1940": ROOT / "1940-Y5-R2FR-EH-uniqueness-Lovelock-gate-or-R11-residual-operator.md",
    "lovelock_1940": OUT / "P8_Y5_PARENT_QLOC_1940_LOVELOCK_ASSUMPTION_GATE.csv",
    "heuristics": ROOT / "00-martin-fork-heuristics-private.md",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        values = [
            str(row.get(field, ""))
            .replace("\n", "<br>")
            .replace("|", "/")
            for field in fields
        ]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3463": "generator for this checkpoint",
        "doc_3462": "live no-source-only-slot obstruction predecessor",
        "grammar_3462": "3462 grammar no-go rows",
        "counter_3462": "weighted descended action countermodel",
        "wep_3462": "first WEP s_Y5 product row",
        "chain_3462": "live chain update into 3461/3460/3459",
        "doc_3460": "source-current owner/Y5 source normalization predecessor",
        "owner_3460": "Y5 source-current theorem attempt",
        "decomp_3460": "source-current component decomposition",
        "bounds_3460": "J_norm and q_loc bound plug rows",
        "doc_3459": "response-doublet energy identity predecessor",
        "bounds_3459": "response-doublet amplitude/q_loc residual bounds",
        "ward_universality": "source-current Ward universality contract",
        "ward_owner": "Ward/source owner identity contract",
        "parent_terms": "parent action term contract for source ownership",
        "normalization_stack": "source-normalization theorem stack",
        "doc_1937": "older minimal Hilbert source action candidate",
        "action_1937": "minimal parent matter action signature rows",
        "hilbert_1937": "conditional Hilbert source theorem rows",
        "doc_1938": "Ward/Bianchi/Newtonian test of candidate action",
        "ward_1938": "Ward/Bianchi conservation theorem rows",
        "newton_1938": "Newtonian limit derivation rows",
        "blockers_1938": "gravity-operator and PPN blockers",
        "doc_1939": "EH/Newtonian operator candidate predecessor",
        "eh_1939": "conditional EH-to-Poisson theorem rows",
        "doc_1940": "Lovelock/EH uniqueness conditional branch",
        "lovelock_1940": "Lovelock assumption gate rows",
        "heuristics": "private Martin-style fork heuristic mentioning Poynting/EM flow",
        "local_bounds": "source-backed local empirical bound ledger",
    }
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
        }
        for key, path in SOURCES.items()
    ]


def single_source_current_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "SSC3463_0_target",
            "question": "Can one conserved Noether/Hilbert/Poynting stress-current kill source-only weights?",
            "derivation": "Require source = Hilbert variation of the complete ordinary matter+EM action in one observed coframe, with no independent source selector.",
            "result": "TARGET_SHARPENED",
            "meaning": "This is the right coupling theorem, but it must include action-normalization ownership, not just conservation.",
            "source_path": str(SOURCES["doc_3462"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSC3463_1_Hilbert_Noether_current",
            "question": "Does the same-action Hilbert current give a unique source object?",
            "derivation": "T_tot^{mu nu}=(-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs_munu; diffeomorphism invariance gives nabla_mu T_tot^{mu nu}=0 on shell.",
            "result": "EXACT_CONDITIONAL_CURRENT_OWNER",
            "meaning": "It removes fitted/non-Hilbert source currents if the action is already fixed.",
            "source_path": str(SOURCES["hilbert_1937"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSC3463_2_Poynting_included",
            "question": "Does EM/Poynting flow belong to the same source-current?",
            "derivation": "For Maxwell action on g_obs, T_EM^{0i}=S_Poynting^i/c^2 in a local inertial frame, and nabla_mu(T_matter+T_EM)^{mu nu}=0 after Lorentz-force exchange cancels.",
            "result": "EXACT_CONDITIONAL_EM_SOURCE_ACCOUNTING",
            "meaning": "Poynting flow is not a side channel; it is part of the stress-current gravity sees when Maxwell is action-owned.",
            "source_path": str(SOURCES["script_3463"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSC3463_3_action_normalization",
            "question": "Does current ownership forbid S_A -> w_A S_A?",
            "derivation": "No. A constant sector multiplier scales Hilbert and Noether stress currents while leaving isolated classical EOM unchanged.",
            "result": "ROOT_BLOCKER",
            "meaning": "The real missing theorem is canonical action/source normalization: no independent sector scale w_A, including w_EM, may exist after measured matter constants are fixed.",
            "source_path": str(SOURCES["counter_3462"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSC3463_4_normalization_owner_route",
            "question": "What would close the blocker?",
            "derivation": "Parent observable algebra must fix action scales through one quantum/action unit, measured charges/masses/fine-structure constants, and one observed coframe/Hodge star; all remaining common normalization is calibration only.",
            "result": "CLOSURE_CONTRACT_IDENTIFIED",
            "meaning": "If this is parent-signed, Delta_w_AB=0 and the WEP source branch becomes theorem-zero.",
            "source_path": str(SOURCES["normalization_stack"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSC3463_5_verdict",
            "question": "Did 3463 prove source coupling?",
            "derivation": "Combine 1937 conditional Hilbert action, 1938 Ward identity, EM/Poynting stress accounting, and 3462 countermodel.",
            "result": "CONDITIONAL_OWNER_STRONGER_BUT_NOT_PARENT_CLOSED",
            "meaning": "We have a serious GR-compatible route, but the parent action-normalization theorem is still the exact missing coupling piece.",
            "source_path": str(SOURCES["action_1937"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def maxwell_poynting_stress_ledger() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EM3463_0_action",
            "object": "Maxwell action on observed geometry",
            "formula": "S_EM = -1/(4 mu0) int sqrt(-g_obs) F_mn F^mn + int A_mu J^mu",
            "derivation_status": "STANDARD_CONDITIONAL_ACTION_FORM",
            "implication": "The metric/coframe/Hodge star used by EM is the same object that defines EM stress-energy.",
            "missing_parent_piece": "derive this observed Hodge/coframe selection from MTS rather than importing it",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EM3463_1_hilbert_stress",
            "object": "EM Hilbert stress tensor",
            "formula": "T_EM^{mu nu}=(1/mu0)(F^{mu alpha}F^nu_alpha - 1/4 g_obs^{mu nu} F_ab F^ab)",
            "derivation_status": "EXACT_FROM_ACTION_CONDITIONAL",
            "implication": "EM energy, pressure, momentum density, and stresses gravitate through the same Hilbert source slot.",
            "missing_parent_piece": "action normalization 1/mu0 and charge/current normalization must be parent-owned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EM3463_2_poynting",
            "object": "Poynting vector as source-current component",
            "formula": "local inertial frame: T_EM^{0i}=S_Poynting^i/c^2, S_Poynting=E x H",
            "derivation_status": "EXACT_CONDITIONAL_LOCAL_FRAME_IDENTITY",
            "implication": "The user's Poynting intuition is a valid coupling diagnostic: EM energy flow is stress-current flow, not an extra fitted force.",
            "missing_parent_piece": "need MTS derivation of the observed EM Hodge/flow rule",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EM3463_3_exchange",
            "object": "matter-EM stress exchange",
            "formula": "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_matter^{mu nu}=+F^{nu lambda}J_lambda",
            "derivation_status": "EXACT_CONDITIONAL_ON_MAXWELL_MATTER_COUPLING",
            "implication": "Only the total matter+EM stress-current is conserved when charges exchange energy-momentum.",
            "missing_parent_piece": "the charged matter current owner and representation/charge normalization must be fixed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "EM3463_4_multiplier_obstruction",
            "object": "EM sector scale w_EM",
            "formula": "S_EM -> w_EM S_EM scales T_EM and Poynting source strength unless w_EM is absorbed into measured charge/unit conventions by a parent theorem",
            "derivation_status": "OBSTRUCTION_RETAINED",
            "implication": "Poynting accounting sharpens the coupling problem; it does not by itself prove the normalization.",
            "missing_parent_piece": "canonical EM action normalization / fine-structure / charge-current owner theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def action_normalization_obstruction() -> list[dict[str, Any]]:
    return [
        {
            "obstruction_id": "ANO3463_0_weighted_action",
            "construction": "S_m = sum_A w_A S_A[g_obs,Psi_A,theta_A]",
            "what_survives": "locality, covariance, same observed coframe, Hilbert variation, separate on-shell conservation for constant w_A",
            "why_source_owner_not_enough": "T_A^{mu nu} and the Noether current scale by w_A, so the owner exists but is not universally normalized",
            "closure_needed": "forbid independent sector action scales after matter constants are calibrated",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "ANO3463_1_classical_EOM",
            "construction": "delta(w_A S_A)=0 gives the same classical isolated EOM as delta S_A=0",
            "what_survives": "nongravitational classical equations may miss w_A",
            "why_source_owner_not_enough": "gravity and action/statistical weights still see the multiplier",
            "closure_needed": "quantum/statistical/action-unit normalization or an observable completeness theorem",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "ANO3463_2_EM_normalization",
            "construction": "S_EM -> w_EM S_EM",
            "what_survives": "vacuum Maxwell equations can be insensitive to an overall sector factor",
            "why_source_owner_not_enough": "EM stress, Poynting flux, and coupling to matter currents carry normalization information",
            "closure_needed": "charge/current/fine-structure owner tying EM action scale to measured constants",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "ANO3463_3_common_calibration",
            "construction": "w_A=w_common for every sector",
            "what_survives": "common source rescaling can be absorbed into measured G in Newtonian acceleration ratios",
            "why_source_owner_not_enough": "species/time/range/frame dependence cannot be absorbed",
            "closure_needed": "prove only common universal calibration remains, or bound every noncommon component",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "obstruction_id": "ANO3463_4_exact_contract",
            "construction": "canonical source-action normalization theorem",
            "what_survives": "all physical matter/EM constants enter theta_A, charges, representations, and stress-energy, not a separate gravitational source selector",
            "why_source_owner_not_enough": "this is precisely the additional theorem that converts conditional 1937 into a derived MTS source-coupling branch",
            "closure_needed": "derive from parent motion/time/space object language or keep WEP/PPN/R10 finite residual rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def wep_tau_projection_derivation() -> list[dict[str, Any]]:
    return [
        {
            "tau_id": "TAU3463_0_definition",
            "quantity": "Eotvos transfer from effective source-weight contrast",
            "derivation": "Let a_A=g_N(1+epsilon_A), a_B=g_N(1+epsilon_B). Then eta_AB=2(a_A-a_B)/(a_A+a_B).",
            "result": "eta_AB=2(epsilon_A-epsilon_B)/(2+epsilon_A+epsilon_B)",
            "value_or_status": "EXACT_SMALL_MODEL_FORMULA",
            "units": "dimensionless",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "tau_id": "TAU3463_1_direct_linear_limit",
            "quantity": "tau_WEP_direct",
            "derivation": "Define Delta_w_eff_AB := epsilon_A-epsilon_B in the direct point-particle source-charge model.",
            "result": "eta_AB = Delta_w_eff_AB + O(epsilon^2)",
            "value_or_status": "1.0",
            "units": "dimensionless transfer under explicit normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "tau_id": "TAU3463_2_not_unity_cheat",
            "quantity": "tau_MTS_raw",
            "derivation": "If the parent coefficient is raw Delta_w_TiPt, the map Delta_w_eff_TiPt = tau_MTS_raw * Delta_w_TiPt still contains material/source/readout physics.",
            "result": "tau_MTS_raw remains missing unless the parent-to-Eotvos projection is derived.",
            "value_or_status": "MISSING_PARENT_TO_EOTVOS_PROJECTION",
            "units": "dimensionless",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "tau_id": "TAU3463_3_effective_bound",
            "quantity": "effective contrast bound",
            "derivation": "Using the source-backed MICROSCOPE anchor and the direct eta normalization, a scoreable effective contrast must obey |Delta_w_eff_TiPt| <= 2.8e-15.",
            "result": "|Delta_w_eff_TiPt| <= eta_TiPt_bound",
            "value_or_status": "2.8e-15",
            "units": "dimensionless",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "tau_id": "TAU3463_4_live_row_update",
            "quantity": "P_WEP_sY5",
            "derivation": "P_WEP_sY5 can now be read as |Delta_w_eff_TiPt| in the direct normalized WEP model, but raw MTS Delta_w and tau_MTS are not derived.",
            "result": "product schema sharpened; prediction still missing",
            "value_or_status": "NONCLAIM_EFFECTIVE_BOUND_READY_RAW_MAP_MISSING",
            "units": "dimensionless",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bound_chain_update() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "CHAIN3463_0_to_3462",
            "feeds": "WEP3462_4_product",
            "update": "tau_WEP is no longer purely opaque: in the direct Eotvos-normalized model tau_direct=1, while tau_MTS_raw remains the parent projection.",
            "formula": "eta_AB = Delta_w_eff_AB + O(epsilon^2), Delta_w_eff_AB=tau_MTS_raw Delta_w_raw",
            "status": "EFFECTIVE_BOUND_READY_RAW_MAP_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3463_1_to_3460",
            "feeds": "Y5B3460_0_source_work_norm",
            "update": "source-current owner must be strengthened to canonical action/source normalization; otherwise C_w ||Delta_w|| remains live.",
            "formula": "J_norm <= C_Y5 ||s_Y5|| + C_w ||Delta_w_raw|| + Q_nonH + Q_boundary + Q_domain + Q_range + Q_time",
            "status": "ROOT_BLOCKER_SHARPENED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3463_2_to_3459",
            "feeds": "RDB3459_0_Z_amplitude;RDB3459_1_q_loc_Hilbert_branch",
            "update": "if canonical source normalization plus boundary silence are proved, the 3459 zero theorem becomes reachable; otherwise the amplitude bound remains finite.",
            "formula": "||Z|| <= (J_norm + sqrt(J_norm^2 + 4 lambda_min |B_flux|))/(2 lambda_min)",
            "status": "ZERO_ROUTE_CONDITIONAL_BOUND_ROUTE_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3463_3_to_1937_1940",
            "feeds": "1937 minimal Hilbert action;1938 Ward/Newton;1939 EH;1940 Lovelock",
            "update": "the older conditional GR/Newton route is now explicitly merged into the live 3462/3463 coupling branch.",
            "formula": "minimal Hilbert source + EH/Lovelock assumptions => conditional GR/Newton; missing parent signatures remain",
            "status": "OLDER_BRANCH_INTEGRATED_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def claim_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG3463_0_Hilbert_Noether_owner",
            "claim": "same-action Hilbert/Noether source owner exists for matter+EM",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "standard variational identity if the parent action and observed coframe are adopted",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3463_1_Poynting_source_accounting",
            "claim": "Poynting flow is part of the EM stress-current source",
            "gate_status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "T_EM^{0i}=S_Poynting^i/c^2 under Maxwell action on observed geometry",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3463_2_action_normalization",
            "claim": "source-only sector multipliers w_A are parent-forbidden",
            "gate_status": "FAIL_BLOCKED",
            "reason": "Hilbert/Noether ownership scales with w_A; canonical action normalization is not parent-derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3463_3_WEP_tau",
            "claim": "tau_WEP is fully derived for raw MTS coefficients",
            "gate_status": "FAIL_BLOCKED",
            "reason": "direct Eotvos-normalized tau is 1, but raw parent-to-effective Delta_w projection remains missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3463_4_local_GR_source_coupling",
            "claim": "local GR/Newton source coupling is derived",
            "gate_status": "FAIL_BLOCKED",
            "reason": "requires canonical source normalization, residual silence, observed-frame map, and PPN map",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3463_0_source_current_result",
            "decision": "Do not repeat generic source-current ownership as the missing theorem.",
            "because": "Hilbert/Noether ownership is conditional and useful, but a weighted action has an owned weighted current.",
            "next_action": "Attack canonical action/source normalization directly.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3463_1_poynting_result",
            "decision": "Keep EM/Poynting in the coupling spine.",
            "because": "Poynting flux is a stress-current component, so it is a concrete diagnostic for whether MTS has the right observed Hodge/coframe/source owner.",
            "next_action": "Derive or bound the EM action-normalization/fine-structure/current-owner map.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3463_2_tau_result",
            "decision": "Use the Eotvos-normalized effective contrast for WEP bookkeeping.",
            "because": "eta_AB linearizes directly to Delta_w_eff_AB, preventing tau_WEP from staying mystical while still refusing the raw-parent unity shortcut.",
            "next_action": "Map raw MTS source coefficients to Delta_w_eff_TiPt or prove they vanish.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3464-Y5-R2FR-canonical-action-normalization-from-MTS-primitives-or-WEP-effective-source-bound.md",
            "next_script": "scripts/Y5_R2FR_3464_canonical_action_normalization_from_MTS_primitives_or_WEP_effective_source_bound.py",
            "objective": "Try to derive the no-sector-action-scale theorem from MTS parent primitives, including EM action/charge/fine-structure normalization; if it fails, promote the WEP effective-source contrast bound as a nonclaim finite branch while raw coefficients remain unmapped.",
            "success_gate": "Either w_A and w_EM are parent-forbidden by canonical action normalization, or Delta_w_eff_TiPt and its raw-parent map are explicitly bounded with units and source paths.",
            "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; setting raw tau_MTS to one; hiding species weights in measured G",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validate(paths: dict[str, Path], datasets: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    stamp = now()

    sources = datasets["source_register"]
    missing_sources = [row["source_id"] for row in sources if not row["exists"]]
    checks.append(
        {
            "check_id": "VAL3463_0_sources_exist",
            "passed": not missing_sources,
            "detail": f"{len(sources) - len(missing_sources)}/{len(sources)} source paths exist; missing={';'.join(missing_sources) or 'none'}",
            "timestamp_utc": stamp,
        }
    )

    audit = datasets["single_source_current_audit"]
    results = {row["audit_id"]: row["result"] for row in audit}
    checks.append(
        {
            "check_id": "VAL3463_1_owner_limit_found",
            "passed": results.get("SSC3463_3_action_normalization") == "ROOT_BLOCKER"
            and results.get("SSC3463_5_verdict") == "CONDITIONAL_OWNER_STRONGER_BUT_NOT_PARENT_CLOSED",
            "detail": ";".join(f"{key}={value}" for key, value in results.items()),
            "timestamp_utc": stamp,
        }
    )

    em = datasets["maxwell_poynting_stress_ledger"]
    checks.append(
        {
            "check_id": "VAL3463_2_poynting_accounted",
            "passed": any("T_EM^{0i}=S_Poynting^i/c^2" in row["formula"] for row in em)
            and any("Lorentz-force exchange" in row["derivation_status"] or "nabla_mu T_EM" in row["formula"] for row in em),
            "detail": ";".join(row["row_id"] for row in em),
            "timestamp_utc": stamp,
        }
    )

    obstruction = datasets["action_normalization_obstruction"]
    checks.append(
        {
            "check_id": "VAL3463_3_weighted_action_obstruction",
            "passed": any("w_A S_A" in row["construction"] for row in obstruction)
            and any("w_EM" in row["construction"] for row in obstruction),
            "detail": ";".join(row["obstruction_id"] for row in obstruction),
            "timestamp_utc": stamp,
        }
    )

    tau = datasets["wep_tau_projection_derivation"]
    checks.append(
        {
            "check_id": "VAL3463_4_tau_direct_not_raw_cheat",
            "passed": any(row["tau_id"] == "TAU3463_1_direct_linear_limit" and row["value_or_status"] == "1.0" for row in tau)
            and any(row["tau_id"] == "TAU3463_2_not_unity_cheat" and "MISSING" in row["value_or_status"] for row in tau),
            "detail": ";".join(f"{row['tau_id']}={row['value_or_status']}" for row in tau),
            "timestamp_utc": stamp,
        }
    )

    chain = datasets["bound_chain_update"]
    checks.append(
        {
            "check_id": "VAL3463_5_chain_integrated",
            "passed": any("3462" in row["chain_id"] for row in chain)
            and any("3460" in row["chain_id"] for row in chain)
            and any("3459" in row["chain_id"] for row in chain)
            and any("1937_1940" in row["chain_id"] for row in chain),
            "detail": ";".join(f"{row['chain_id']}->{row['feeds']}" for row in chain),
            "timestamp_utc": stamp,
        }
    )

    claim_rows = [
        row
        for rows in datasets.values()
        for row in rows
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    checks.append(
        {
            "check_id": "VAL3463_6_no_claim_rows",
            "passed": not claim_rows,
            "detail": f"claim_like_rows={len(claim_rows)}",
            "timestamp_utc": stamp,
        }
    )

    parse_ok = True
    parse_details: list[str] = []
    for name, path in paths.items():
        if path.suffix.lower() == ".csv":
            if name == "validation" and not path.exists():
                parse_details.append(f"{path.name}:pending_write")
                continue
            try:
                parse_details.append(f"{path.name}:{len(read_csv(path))}")
            except Exception as exc:  # pragma: no cover - validation output
                parse_ok = False
                parse_details.append(f"{path.name}:PARSE_FAIL:{exc}")
    checks.append(
        {
            "check_id": "VAL3463_7_csv_parse",
            "passed": parse_ok,
            "detail": ";".join(parse_details),
            "timestamp_utc": stamp,
        }
    )

    formalization_has_outputs = any(FORMALIZATION.rglob("*3463*")) if FORMALIZATION.exists() else False
    checks.append(
        {
            "check_id": "VAL3463_8_formalization_untouched_by_3463",
            "passed": not formalization_has_outputs,
            "detail": f"formalization_exists={FORMALIZATION.exists()}; 3463_outputs_in_formalization={formalization_has_outputs}",
            "timestamp_utc": stamp,
        }
    )

    next_rows = datasets["next_target"]
    checks.append(
        {
            "check_id": "VAL3463_9_next_target_3464",
            "passed": len(next_rows) == 1 and "canonical-action-normalization" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
            "timestamp_utc": stamp,
        }
    )

    overall = all(row["passed"] for row in checks)
    checks.append(
        {
            "check_id": "VAL3463_SUMMARY",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
            "timestamp_utc": stamp,
        }
    )
    return checks


def write_doc(datasets: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3463 - Single Source-Current Owner From Noether/Poynting Flow Or WEP Tau Map Under AX1090",
        "",
        "**Current verdict:** the source-current route is real but sharper than we thought. A single Hilbert/Noether stress-current, including EM/Poynting flow, is the correct GR-compatible source object, but it does not by itself kill `w_A`: a weighted action has a weighted Hilbert current. The missing theorem is canonical action/source normalization.",
        "",
        "**Concrete progress:** Poynting is now in the spine as a source-current diagnostic, and the WEP transfer is partially demystified: in an Eotvos-normalized direct model `eta_AB = Delta_w_eff_AB + O(epsilon^2)`, so `tau_direct=1`; the raw MTS parent-to-effective map is still missing.",
        "",
        "## Source Register",
        md_table(datasets["source_register"]),
        "",
        "## Single Source-Current Audit",
        md_table(datasets["single_source_current_audit"]),
        "",
        "## Maxwell/Poynting Stress Ledger",
        md_table(datasets["maxwell_poynting_stress_ledger"]),
        "",
        "## Action-Normalization Obstruction",
        md_table(datasets["action_normalization_obstruction"]),
        "",
        "## WEP Tau Projection Derivation",
        md_table(datasets["wep_tau_projection_derivation"]),
        "",
        "## Bound Chain Update",
        md_table(datasets["bound_chain_update"]),
        "",
        "## Claim Gates",
        md_table(datasets["claim_gates"]),
        "",
        "## Decision Ledger",
        md_table(datasets["decision_ledger"]),
        "",
        "## Validation",
        md_table(datasets["validation"]),
        "",
        "## Next Target",
        md_table(datasets["next_target"]),
        "",
        "## Bottom Line",
        "",
        "- Good news: the conditional GR/Newton/Hilbert route is not fluff; older 1937-1940 work already makes it coherent, and 3463 merges it into the live chain.",
        "- Hard news: source-current ownership alone is insufficient because `w_A S_A` has its own owned source current.",
        "- Best next theorem: derive canonical action normalization/no-sector-scale from MTS primitives, with EM action/charge/fine-structure normalization as the cleanest probe.",
        "- Fallback: use the effective WEP contrast bound `|Delta_w_eff_TiPt| <= 2.8e-15` while raw parent coefficients remain unmapped.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_register": OUT / "P8_Y5_R2FR_3463_SOURCE_REGISTER.csv",
        "single_source_current_audit": OUT / "P8_Y5_R2FR_3463_SINGLE_SOURCE_CURRENT_AUDIT.csv",
        "maxwell_poynting_stress_ledger": OUT / "P8_Y5_R2FR_3463_MAXWELL_POYNTING_STRESS_LEDGER.csv",
        "action_normalization_obstruction": OUT / "P8_Y5_R2FR_3463_ACTION_NORMALIZATION_OBSTRUCTION.csv",
        "wep_tau_projection_derivation": OUT / "P8_Y5_R2FR_3463_WEP_TAU_PROJECTION_DERIVATION.csv",
        "bound_chain_update": OUT / "P8_Y5_R2FR_3463_BOUND_CHAIN_UPDATE.csv",
        "claim_gates": OUT / "P8_Y5_R2FR_3463_CLAIM_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3463_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3463_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3463_VALIDATION.csv",
    }
    datasets = {
        "source_register": source_register(),
        "single_source_current_audit": single_source_current_audit(),
        "maxwell_poynting_stress_ledger": maxwell_poynting_stress_ledger(),
        "action_normalization_obstruction": action_normalization_obstruction(),
        "wep_tau_projection_derivation": wep_tau_projection_derivation(),
        "bound_chain_update": bound_chain_update(),
        "claim_gates": claim_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    for key, rows in datasets.items():
        write_csv(paths[key], rows)
    datasets["validation"] = validate(paths, datasets)
    write_csv(paths["validation"], datasets["validation"])
    write_doc(datasets)


if __name__ == "__main__":
    main()
