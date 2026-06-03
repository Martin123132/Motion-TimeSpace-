from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "constant-universal-Geff-kappa-identity-attempt"
CHECKPOINT_DOC = "452-constant-universal-Geff-kappa-identity-attempt.md"
STATUS = "constant_universal_Geff_kappa_identity_attempt_written_conditional_global_coupling_route_not_parent_derived_Gdot_source_range_rows_retained_no_Newton_or_local_GR_pass"
CLAIM_CEILING = "constant_universal_Geff_kappa_identity_attempt_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "453-global-coupling-superselection-parent-action-contract.md"
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_constant_universal_Geff_kappa_CONTRACT.csv")


CONTRACT_COLUMNS = [
    "contract_id",
    "required_identity",
    "mathematical_form",
    "closes_component",
    "affected_rows",
    "current_status",
    "evidence_needed",
    "fallback_if_missing",
]


SOURCE_DOCS = [
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source pair and G_eff=kappa_eff c^4/(8 pi) algebra",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "constant universal kappa reduction requirement",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "GM absorption and constant universal source-normalization requirements",
    },
    {
        "path": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux closure attempt and constant G_eff next target",
    },
    {
        "path": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "MF7 constant universal coupling requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "HM4 constant universal G_eff requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_Ward_source_owner_identity_CONTRACT.csv",
        "role": "C4 constant universal coupling requirement",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv",
        "role": "A5 constant universal coupling parent-action block",
    },
    {
        "path": "source-intake/mts_residuals/P8_source_normalization_residual_vector_TEMPLATE.csv",
        "role": "P8 G_eff/source-normalization residual template",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/exchange_owner_conditions.csv",
        "role": "C5 constant kappa/G_eff exchange-owner condition",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/Ward_identity_chain.csv",
        "role": "Bianchi projection exposes T_obs grad kappa_eff term",
    },
    {
        "path": "runs/20260602-101500-Ward-Bianchi-exchange-owner-for-Poisson-source/results/source_residual_decomposition.csv",
        "role": "delta_kappa_source residual row",
    },
    {
        "path": "runs/20260602-085500-EH-operator-retained-ledger-and-source-normalization-test-plan/results/source_normalization_channel_plan.csv",
        "role": "constant_Geff source-normalization channel and locks",
    },
    {
        "path": "runs/20260602-094500-MTS-local-residual-vector-input-contract/results/residual_components.csv",
        "role": "R9 Gdot and R10 fifth-force residual definitions",
    },
    {
        "path": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local source locks including Gdot and source charge",
    },
]


THEOREM_STATEMENT = [
    {
        "part": "conditional_global_coupling_theorem",
        "statement": "If kappa_eff is a parent-selected global/superselection coupling, matter and gravity share the same observed frame, no local MTS invariant or material/source label enters kappa_eff, and the Hilbert mass monopole is closed, then G_eff is constant and universal in the local Newton branch.",
        "mathematical_form": "G_eff=kappa_eff c^4/(8 pi); d kappa_eff=partial_A kappa_eff=partial_lambda kappa_eff=0 => dG_eff=partial_A G_eff=partial_lambda G_eff=0",
        "status": "valid_conditional_route",
    },
    {
        "part": "Bianchi_limit",
        "statement": "Bianchi conservation does not by itself fix kappa_eff; if kappa_eff is local, the Ward/Bianchi identity exposes T_obs grad kappa_eff as an exchange/source residual.",
        "mathematical_form": "kappa_eff nabla_mu T_obs^{mu nu}=...+T_obs^{mu nu} nabla_mu kappa_eff+...",
        "status": "blocks_overclaim",
    },
    {
        "part": "current_corpus_status",
        "statement": "The corpus repeatedly requires constant universal kappa/G_eff, but it has not derived the parent global-coupling/superselection identity or ruled out scalar, memory, class, range, frame, or species dependence.",
        "mathematical_form": "C4/HM4/MF7/C5_constant_kappa_Geff remain not_parent_derived",
        "status": "not_parent_derived",
    },
]


IDENTITY_ROUTES = [
    {
        "route": "global_parent_coupling",
        "candidate_identity": "kappa_eff is a coupling constant in S_EH, not a field",
        "mathematical_form": "delta S_parent/delta kappa_eff is not a local Euler equation; d kappa_eff=0 by definition of the branch",
        "what_it_would_close": "Gdot, radial G, range G, species-weighted kappa",
        "current_status": "sufficient_if_parent_declares_superselection",
    },
    {
        "route": "superselection_sector",
        "candidate_identity": "kappa_eff labels a theory sector and is invariant under MTS selector/quotient/material directions",
        "mathematical_form": "L_xi kappa_eff=0 for xi in {selector, memory, class, marker, source-label}",
        "what_it_would_close": "partial_A kappa_eff and memory/class dependence",
        "current_status": "not_parent_derived",
    },
    {
        "route": "Bianchi_plus_separate_matter_conservation",
        "candidate_identity": "if matter stress is separately conserved for arbitrary local sources, Bianchi forbids local grad kappa_eff in the same frame",
        "mathematical_form": "nabla T_obs=0 and nabla E_EH=0 imply T_obs^{mu nu} nabla_mu kappa_eff=0; for arbitrary T_obs, nabla kappa_eff=0",
        "what_it_would_close": "local spacetime gradients of kappa_eff",
        "current_status": "conditional_but_requires_same_frame_and_no_exchange",
    },
    {
        "route": "unit_rescaling_gauge",
        "candidate_identity": "constant kappa rescaling is a unit choice, but only after all derivatives and source labels vanish",
        "mathematical_form": "kappa_eff -> constant kappa_ref is harmless iff partial_{t,r,A,lambda} kappa_eff=0",
        "what_it_would_close": "constant-only calibration ambiguity",
        "current_status": "calibration_only_not_derivation",
    },
    {
        "route": "scalar_tensor_rejection",
        "candidate_identity": "any local scalar or memory dependence of kappa_eff becomes a retained scalar-tensor/source-normalization branch",
        "mathematical_form": "kappa_eff=kappa0 F(Z,I_Q,C_D,lambda) => delta_kappa_source and R9/R10 rows",
        "what_it_would_close": "nothing unless F is theorem-constant or bounded",
        "current_status": "retained_fallback",
    },
]


PROOF_STEPS = [
    {
        "step": 1,
        "claim": "The weak-field EH algebra identifies the Newton coupling once the same-frame EH/source equation is assumed.",
        "mathematical_step": "G_eff=kappa_eff c^4/(8 pi)",
        "status": "algebra_pass",
        "gap": "algebra does not prove kappa_eff is constant or universal",
    },
    {
        "step": 2,
        "claim": "A true Newton constant requires kappa_eff to be a global coupling or superselection label.",
        "mathematical_step": "d kappa_eff=0 before local variation/readout",
        "status": "sufficient_if_parent_derived",
        "gap": "the current parent corpus has not supplied this identity",
    },
    {
        "step": 3,
        "claim": "If kappa_eff varies locally, Bianchi/Ward does not hide it; it becomes an exchange-owner term.",
        "mathematical_step": "q_loc^nu contains kappa_eff^-1 P_loc[T_obs^{mu nu} nabla_mu kappa_eff]",
        "status": "exact_residual_mapping",
        "gap": "the residual is not theorem-zero",
    },
    {
        "step": 4,
        "claim": "Species dependence is a source-charge residual, not a calibration.",
        "mathematical_step": "partial_A kappa_eff != 0 => partial_A mu_obs != 0",
        "status": "retained_R1_R9",
        "gap": "no species/source-blind kappa theorem",
    },
    {
        "step": 5,
        "claim": "Range or radial dependence is a fifth-force/radial-hair residual.",
        "mathematical_step": "partial_r kappa_eff or partial_lambda kappa_eff != 0 => alpha(lambda) or partial_r ln mu_obs",
        "status": "retained_R10_R11",
        "gap": "no no-range/no-radial-coupling theorem",
    },
    {
        "step": 6,
        "claim": "Time dependence is a Gdot/source-drift residual.",
        "mathematical_step": "d ln mu_obs/dt = d ln G_eff/dt + d ln M_eff/dt",
        "status": "retained_R9",
        "gap": "no local stationary coupling theorem",
    },
    {
        "step": 7,
        "claim": "Only a constant universal kappa_eff can be absorbed as measured G.",
        "mathematical_step": "delta kappa_eff/kappa_eff = constant_global can be a unit/calibration choice",
        "status": "valid_conditional_calibration",
        "gap": "constant-only status is not parent-derived",
    },
    {
        "step": 8,
        "claim": "Therefore constant G_eff is a required parent identity, not a result of Poisson algebra alone.",
        "mathematical_step": "R1/R4/R9/R10/R11 remain retained until CU0-CU8 close",
        "status": "no_promotion",
        "gap": "Newton/local-GR remain unpromoted",
    },
]


COUNTEREXAMPLES = [
    {
        "counterexample": "Brans_Dicke_like_scalar_kappa",
        "construction": "kappa_eff = kappa0 / phi(x)",
        "why_it_breaks_Newton": "Poisson coefficient and PPN gamma/beta become scalar-tensor residuals",
        "required_blocker": "phi frozen by theorem, infinite mass/zero coupling, or retained scalar branch",
        "affected_rows": "R3;R4;R9;R10;R11",
    },
    {
        "counterexample": "memory_dependent_Geff",
        "construction": "G_eff=G0[1+epsilon K_memory(t)]",
        "why_it_breaks_Newton": "cosmology memory success leaks into local Gdot unless compact-local silence is derived",
        "required_blocker": "local memory-kernel silence or Gdot residual below lock",
        "affected_rows": "R7;R9;R10;R11",
    },
    {
        "counterexample": "species_dependent_source_coupling",
        "construction": "kappa_A = kappa0(1+epsilon_A)",
        "why_it_breaks_Newton": "ordinary masses source gravity with composition-dependent strength",
        "required_blocker": "source-current universality plus kappa superselection",
        "affected_rows": "R1;R4;R9;R11",
    },
    {
        "counterexample": "range_dependent_running_G",
        "construction": "G_eff(lambda) or Yukawa-like G(r)=G0[1+alpha exp(-r/lambda)]",
        "why_it_breaks_Newton": "inverse-square law becomes finite-range force law",
        "required_blocker": "alpha(lambda)=0 theorem or executable curve below bounds",
        "affected_rows": "R10;R11",
    },
    {
        "counterexample": "frame_dependent_kappa",
        "construction": "kappa_eff differs between matter frame, clock frame, and EH operator frame",
        "why_it_breaks_Newton": "same-looking Poisson coefficient is a frame artefact",
        "required_blocker": "same observed coframe/source calibration theorem",
        "affected_rows": "R0;R2;R3;R4;R11",
    },
    {
        "counterexample": "domain_or_boundary_running_G",
        "construction": "kappa_eff=kappa0 F(D_boundary,L_cg,class)",
        "why_it_breaks_Newton": "domain/boundary data produce preferred-location, drift, or radial source normalization",
        "required_blocker": "boundary/domain no-hair and local trivial-class theorem",
        "affected_rows": "R4;R7;R8;R9;R10;R11",
    },
    {
        "counterexample": "constant_offset_overclaim",
        "construction": "kappa_eff=kappa0(1+epsilon_const) is treated as a prediction",
        "why_it_breaks_Newton": "constant offset is only calibration unless kappa0 is parent-normalized",
        "required_blocker": "absolute coupling normalization theorem or no prediction of G value",
        "affected_rows": "R4;R9;R11",
    },
]


CONTRACT = [
    {
        "contract_id": "CU0_same_frame_EH_source",
        "required_identity": "kappa_eff multiplies the source in the same observed frame used by matter and the EH operator",
        "mathematical_form": "E_munu[g_obs]=kappa_eff T_obs_munu[g_obs]",
        "closes_component": "frame/source calibration split",
        "affected_rows": "R0;R2;R3;R4;R11",
        "current_status": "conditional_not_parent_derived",
        "evidence_needed": "same-frame EH/source parent theorem",
        "fallback_if_missing": "frame residuals and operator ledger remain active",
    },
    {
        "contract_id": "CU1_global_coupling_status",
        "required_identity": "kappa_eff is a global coupling/superselection label, not a local field",
        "mathematical_form": "d kappa_eff=0 before local variation",
        "closes_component": "Gdot/radial/range coupling drift",
        "affected_rows": "R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "global-coupling parent-action or superselection theorem",
        "fallback_if_missing": "kappa_eff becomes retained scalar/source-normalization field",
    },
    {
        "contract_id": "CU2_no_MTS_invariant_dependence",
        "required_identity": "kappa_eff does not depend on memory, quotient, class, boundary, domain, or projector invariants",
        "mathematical_form": "partial_Z kappa_eff=partial_IQ kappa_eff=partial_C kappa_eff=partial_D kappa_eff=0",
        "closes_component": "memory/domain/boundary G drift",
        "affected_rows": "R7;R8;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant-sector/global-coupling independence theorem",
        "fallback_if_missing": "Gdot/fifth-force/domain residual rows remain",
    },
    {
        "contract_id": "CU3_species_source_blindness",
        "required_identity": "kappa_eff carries no species, source-composition, marker, or material label",
        "mathematical_form": "partial_A kappa_eff=partial_m kappa_eff=0",
        "closes_component": "source-charge WEP coupling split",
        "affected_rows": "R1;R4;R9;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "no-species/source-charge plus global-coupling theorem",
        "fallback_if_missing": "R1 source-normalization channel remains retained",
    },
    {
        "contract_id": "CU4_no_range_radial_running",
        "required_identity": "kappa_eff/G_eff has no radial or finite-range dependence",
        "mathematical_form": "partial_r kappa_eff=partial_lambda kappa_eff=0",
        "closes_component": "R10 fifth-force and radial source hair",
        "affected_rows": "R3;R4;R10;R11",
        "current_status": "not_derived_symbolic",
        "evidence_needed": "no finite-range source charge or alpha(lambda)=0 theorem",
        "fallback_if_missing": "R10 alpha(lambda) curve required",
    },
    {
        "contract_id": "CU5_Bianchi_exchange_zero",
        "required_identity": "Bianchi projection has no T_obs grad kappa_eff exchange term",
        "mathematical_form": "P_loc[T_obs^{mu nu} nabla_mu kappa_eff]=0",
        "closes_component": "q_loc and source residual kappa term",
        "affected_rows": "R4;R7;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "CU1-CU4 or explicit retained coefficient below locks",
        "fallback_if_missing": "delta_kappa_source row remains active",
    },
    {
        "contract_id": "CU6_constant_only_calibration_policy",
        "required_identity": "only a global constant offset in kappa_eff may be absorbed into measured G",
        "mathematical_form": "delta kappa_eff/kappa_eff = constant_global, with all derivatives zero",
        "closes_component": "unit/calibration ambiguity",
        "affected_rows": "R4;R9;R11",
        "current_status": "policy_written_not_parent_normalization",
        "evidence_needed": "absolute coupling normalization if predicting G itself",
        "fallback_if_missing": "do not claim prediction of G value; only claim no drift if derived",
    },
    {
        "contract_id": "CU7_measured_GM_product_silence",
        "required_identity": "G_eff and M_eff are separately or jointly stationary, universal, and range-independent",
        "mathematical_form": "d ln(G_eff M_eff)/dt=partial_A mu_obs=partial_lambda mu_obs=0",
        "closes_component": "measured-GM source normalization",
        "affected_rows": "R1;R4;R9;R10;R11",
        "current_status": "not_parent_derived",
        "evidence_needed": "constant G_eff plus mass-flux closure and zero mu_extra",
        "fallback_if_missing": "measured-GM residual vector remains retained",
    },
    {
        "contract_id": "CU8_retained_residual_fallback",
        "required_identity": "any coupling variation becomes executable residual data",
        "mathematical_form": "dln_Geff_dt, partial_A ln G_eff, partial_r ln G_eff, alpha(lambda), delta_kappa_source",
        "closes_component": "none; retained branch only",
        "affected_rows": "R1;R3;R4;R7;R8;R9;R10;R11",
        "current_status": "template_policy_only",
        "evidence_needed": "numeric coefficient/curve or theorem-zero proof",
        "fallback_if_missing": "no measured-GM/Newton/PPN/local-GR claim",
    },
]


GATE_TESTS = [
    {
        "gate": "conditional_global_coupling_theorem_written",
        "pass_condition": "global/superselection kappa implies constant universal G_eff",
        "current_result": "pass_conditional",
        "evidence": "proof chain and contract recorded",
    },
    {
        "gate": "Bianchi_not_overclaimed",
        "pass_condition": "Bianchi is not used to hide local grad kappa terms",
        "current_result": "pass",
        "evidence": "T_obs grad kappa residual retained",
    },
    {
        "gate": "constant_offset_not_prediction",
        "pass_condition": "global constant offset is treated as calibration unless absolute normalization is derived",
        "current_result": "pass",
        "evidence": "CU6 policy recorded",
    },
    {
        "gate": "global_coupling_parent_derived",
        "pass_condition": "kappa_eff is parent-derived global/superselection coupling",
        "current_result": "fail",
        "evidence": "CU1 remains not_parent_derived",
    },
    {
        "gate": "all_coupling_derivatives_zero",
        "pass_condition": "partial_t,r,A,lambda,Z kappa_eff all vanish by theorem",
        "current_result": "fail",
        "evidence": "CU2-CU5 remain open",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "pass_condition": "source-normalization plus PPN rows are theorem-zero or scored",
        "current_result": "fail",
        "evidence": "constant-coupling checkpoint only",
    },
]


THEOREM_STATUS = [
    {
        "claim": "constant universal G_eff conditional theorem written",
        "status": "pass_conditional",
        "evidence": "G_eff=kappa_eff c^4/(8 pi) plus global kappa gives derivative silence",
    },
    {
        "claim": "Bianchi/kappa overclaim blocked",
        "status": "pass",
        "evidence": "grad kappa mapped to source residual",
    },
    {
        "claim": "constant coupling contract written",
        "status": "pass",
        "evidence": str(CONTRACT_PATH),
    },
    {
        "claim": "global kappa parent-derived",
        "status": "fail",
        "evidence": "no parent global-coupling/superselection theorem",
    },
    {
        "claim": "Gdot/source/range derivative rows zero",
        "status": "fail",
        "evidence": "derivatives remain retained contract targets",
    },
    {
        "claim": "Newton/PPN/local-GR promoted",
        "status": "fail",
        "evidence": "measured-GM, source residual, and PPN rows remain open",
    },
]


DECISION = [
    {
        "decision": "The constant-universal G_eff/kappa identity has been attempted. The conditional route is clean: if kappa_eff is a parent-selected global or superselection coupling, independent of MTS invariants, source labels, material markers, range, radius, time, and frame, then G_eff=kappa_eff c^4/(8 pi) is constant and universal in the local Newton branch. But the current corpus does not derive that global-coupling identity. Bianchi/Ward instead exposes local grad kappa as a retained exchange/source residual. Therefore Gdot, source-charge, range/fifth-force, beta/source-normalization, and R11 operator rows remain active; no measured-GM, Newton, PPN, or local-GR promotion is allowed.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": NEXT_TARGET,
        "why_next": "derive or explicitly postulate why kappa_eff is a global superselection coupling rather than a local MTS field",
    },
    {
        "rank": 2,
        "target": "453-PiM-parent-symplectic-projector-algebra-attempt.md",
        "why_next": "mass-flux closure still needs actual Pi_M projector algebra and variation",
    },
    {
        "rank": 3,
        "target": "map CU0-CU8 into P8/R9/R10 residual evaluator",
        "why_next": "failed coupling identities should activate Gdot/source/range rows automatically",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as output_handle:
        writer = csv.DictWriter(output_handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for data_row in rows:
        values = []
        for fieldname in fieldnames:
            value = str(data_row.get(fieldname, ""))
            value = value.replace("\n", " ").replace("|", "/")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_source_register() -> list[dict[str, Any]]:
    source_register = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        source_register.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return source_register


def build_gate_results(source_register: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [source_row["source_file"] for source_row in source_register if not source_row["exists"]]
    gate_results = [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else "; ".join(missing_sources),
        },
        {
            "gate": "contract_schema_matches",
            "status": "pass" if list(CONTRACT[0].keys()) == CONTRACT_COLUMNS else "fail",
            "evidence": "constant universal G_eff/kappa contract columns match schema",
        },
        {
            "gate": "theorem_statement_written",
            "status": "pass" if len(THEOREM_STATEMENT) == 3 else "fail",
            "evidence": f"{len(THEOREM_STATEMENT)} theorem rows",
        },
        {
            "gate": "identity_routes_written",
            "status": "pass" if len(IDENTITY_ROUTES) == 5 else "fail",
            "evidence": f"{len(IDENTITY_ROUTES)} identity routes",
        },
        {
            "gate": "proof_steps_written",
            "status": "pass" if len(PROOF_STEPS) == 8 else "fail",
            "evidence": f"{len(PROOF_STEPS)} proof steps",
        },
        {
            "gate": "counterexamples_written",
            "status": "pass" if len(COUNTEREXAMPLES) == 7 else "fail",
            "evidence": f"{len(COUNTEREXAMPLES)} counterexamples",
        },
        {
            "gate": "contract_written",
            "status": "pass",
            "evidence": str(CONTRACT_PATH),
        },
        {
            "gate": "Bianchi_not_overclaimed",
            "status": "pass",
            "evidence": "grad kappa term mapped to retained residual",
        },
        {
            "gate": "constant_offset_not_prediction",
            "status": "pass",
            "evidence": "constant offset treated as calibration unless parent-normalized",
        },
        {
            "gate": "global_coupling_parent_derived",
            "status": "fail",
            "evidence": "no global-coupling/superselection parent theorem supplied",
        },
        {
            "gate": "MTS_invariant_dependence_forbidden",
            "status": "fail",
            "evidence": "memory/class/domain/projector dependence not parent-forbidden",
        },
        {
            "gate": "species_source_blind_kappa_derived",
            "status": "fail",
            "evidence": "partial_A kappa_eff remains a retained source-charge route",
        },
        {
            "gate": "range_radial_running_zero",
            "status": "fail",
            "evidence": "partial_r/partial_lambda kappa_eff not theorem-zero",
        },
        {
            "gate": "Gdot_zero_derived",
            "status": "fail",
            "evidence": "R9 Gdot row remains retained",
        },
        {
            "gate": "measured_GM_parent_derived",
            "status": "fail",
            "evidence": "constant coupling plus mass-flux closure and mu_extra zero are not all derived",
        },
        {
            "gate": "Newtonian_reduction_promoted",
            "status": "fail",
            "evidence": "constant-coupling checkpoint only",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "P8 and PPN rows remain retained",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]
    return gate_results


def render_doc(run_dir: Path, source_register: list[dict[str, Any]], gate_results: list[dict[str, str]]) -> str:
    return f"""# 452 - Constant Universal Geff/Kappa Identity Attempt

Private P8/R1/R4/R9/R10/R11 coupling checkpoint. This is not a public WEP, Einstein-Hilbert, measured-GM, Newtonian-limit, PPN, fifth-force, local-GR, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 451 showed that even a closed mass flux is not Newtonian unless `G_eff`/`kappa_eff` is constant and universal.

This checkpoint asks whether that constant-coupling identity is derived, or whether `kappa_eff` remains a possible local MTS/source-normalization residual.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/constant_universal_Geff_kappa_identity_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Contract | `{CONTRACT_PATH}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_register)}

## 4. Theorem Statement

{markdown_table(THEOREM_STATEMENT)}

## 5. Identity Routes

{markdown_table(IDENTITY_ROUTES)}

## 6. Conditional Proof Steps

{markdown_table(PROOF_STEPS)}

## 7. Counterexamples

{markdown_table(COUNTEREXAMPLES)}

## 8. Constant-Coupling Contract

The constant universal `G_eff`/`kappa_eff` contract has been written to `{CONTRACT_PATH}`.

{markdown_table(CONTRACT, CONTRACT_COLUMNS)}

## 9. Gate Tests

{markdown_table(GATE_TESTS)}

## 10. Theorem Status

{markdown_table(THEOREM_STATUS)}

## 11. Gate Results

{markdown_table(gate_results)}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: the algebra is good, but algebra is not ontology. If `kappa_eff` is a global parent coupling, Newton survives this gate. If it is a local MTS function, the theory has a scalar/source-normalization residual that must be derived zero or tested. No smuggling drifting `G` into measured `GM`.

## 13. Next Queue

{markdown_table(NEXT_QUEUE)}
"""


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_register = build_source_register()
    gate_results = build_gate_results(source_register)
    missing_sources = [source_row["source_file"] for source_row in source_register if not source_row["exists"]]

    write_csv(results_dir / "source_register.csv", source_register)
    write_csv(results_dir / "theorem_statement.csv", THEOREM_STATEMENT)
    write_csv(results_dir / "identity_routes.csv", IDENTITY_ROUTES)
    write_csv(results_dir / "proof_steps.csv", PROOF_STEPS)
    write_csv(results_dir / "counterexamples.csv", COUNTEREXAMPLES)
    write_csv(results_dir / "constant_coupling_contract.csv", CONTRACT, CONTRACT_COLUMNS)
    write_csv(results_dir / "gate_tests.csv", GATE_TESTS)
    write_csv(results_dir / "theorem_status.csv", THEOREM_STATUS)
    write_csv(results_dir / "gate_results.csv", gate_results)
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)
    write_csv(ROOT / CONTRACT_PATH, CONTRACT, CONTRACT_COLUMNS)

    doc_text = render_doc(run_dir, source_register, gate_results)
    (ROOT / CHECKPOINT_DOC).write_text(doc_text, encoding="utf-8")

    status_payload = {
        "timestamp": timestamp,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": CHECKPOINT_DOC,
        "run_dir": str(run_dir.relative_to(ROOT)),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "conditional_global_coupling_theorem_written": True,
        "Bianchi_not_overclaimed": True,
        "constant_offset_not_prediction": True,
        "global_coupling_parent_derived": False,
        "MTS_invariant_dependence_forbidden": False,
        "species_source_blind_kappa_derived": False,
        "range_radial_running_zero": False,
        "Gdot_zero_derived": False,
        "measured_GM_parent_derived": False,
        "Newtonian_reduction_promoted": False,
        "local_GR_claim_allowed": False,
        "counterexamples": len(COUNTEREXAMPLES),
        "contract_rows": len(CONTRACT),
        "failed_gates": [gate_row["gate"] for gate_row in gate_results if gate_row["status"] == "fail"],
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status_payload, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\n{datetime.now(timezone.utc).isoformat()}\n",
        encoding="utf-8",
    )
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Write the MTS constant universal G_eff/kappa identity attempt.")
    parser.add_argument(
        "--timestamp",
        default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix, e.g. 20260602-163000.",
    )
    parsed_args = parser.parse_args()
    run_dir = write_run(parsed_args.timestamp)
    status_payload = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status_payload, indent=2))


if __name__ == "__main__":
    main()
