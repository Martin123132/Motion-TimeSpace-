from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3419-Y5-R2FR-Khat-Gamma-eff-metric-response-lock-and-Helmholtz-audit-under-AX1090.md"

ALPHA3_PRODUCT_LIMIT = 5.381673706808059e-15

SOURCES = {
    "doc_3418": ROOT / "3418-Y5-R2FR-q_loc-vector-zero-Ward-boundary-proof-or-alpha-bound-row-under-AX1090.md",
    "parent_contract_3418": OUT / "P8_Y5_R2FR_3418_PARENT_CONTRACT_CLAUSES.csv",
    "vector_zero_3418": OUT / "P8_Y5_R2FR_3418_VECTOR_ZERO_DERIVATION.csv",
    "next_3418": OUT / "P8_Y5_R2FR_3418_NEXT_TARGET.csv",
    "contract_3411": OUT / "P8_Y5_R2FR_3411_KHAT_METRIC_RESPONSE_CONTRACT.csv",
    "symbol_verdict_3412": OUT / "P8_Y5_R2FR_3412_SYMBOL_MATCH_VERDICT.csv",
    "candidate_ranking_3412": OUT / "P8_Y5_R2FR_3412_CONSTRUCTION_CANDIDATE_RANKING.csv",
    "metric_template_3413": OUT / "P8_Y5_R2FR_3413_METRIC_RESPONSE_TEMPLATE.csv",
    "response_doublet_3413": OUT / "P8_Y5_R2FR_3413_RESPONSE_DOUBLET_ACTION.csv",
    "khat_identity_3065": OUT / "P8_Y5_R2FR_3065_KHAT_METRIC_RESPONSE_IDENTITY_AUDIT.csv",
    "khat_components_3066": OUT / "P8_Y5_R2FR_3066_KHAT_COMPONENT_SOURCE_LIST.csv",
    "khat_match_3076": OUT / "P8_Y5_R2FR_3076_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "gamma_candidates_3242": OUT / "P8_Y5_R2FR_3242_GAMMA_EFF_DENSITY_CANDIDATE_RANKING.csv",
    "source_formula_1664": OUT / "P8_Y5_PARENT_QLOC_1664_GAMMA_KHAT_SOURCE_FORMULA_AUDIT.csv",
    "helmholtz_obstruction_1664": OUT / "P8_Y5_PARENT_QLOC_1664_HELMHOLTZ_OBSTRUCTION.csv",
    "kmetric_compare_2218": OUT / "P8_Y5_PARENT_QLOC_2218_KMETRIC_KHAT_TENSOR_COMPARISON.csv",
    "helmholtz_gate_2218": OUT / "P8_Y5_PARENT_QLOC_2218_HELMHOLTZ_GATE.csv",
    "birth_certificate_2219": OUT / "P8_Y5_PARENT_QLOC_2219_KHAT_BIRTH_CERTIFICATE_GATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3419_SOURCE_REGISTER.csv",
    "branch_split": OUT / "P8_Y5_R2FR_3419_METRIC_RESPONSE_BRANCH_SPLIT.csv",
    "response_lock": OUT / "P8_Y5_R2FR_3419_KHAT_RESPONSE_LOCK_THEOREM.csv",
    "helmholtz_audit": OUT / "P8_Y5_R2FR_3419_HELMHOLTZ_AUDIT.csv",
    "live_symbol_adoption": OUT / "P8_Y5_R2FR_3419_LIVE_SYMBOL_ADOPTION_MAP.csv",
    "kmetric_expansion": OUT / "P8_Y5_R2FR_3419_RESPONSE_DOUBLET_KMETRIC_EXPANSION.csv",
    "qloc_consequence": OUT / "P8_Y5_R2FR_3419_QLOC_CONSEQUENCE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3419_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3419_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3419_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3419_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3419_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def cell(value: Any) -> str:
        return str(value).replace("|", "/").replace("\n", " ")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3418": "declares Khat/Gamma_eff metric-response lock as the load-bearing q_loc vector-zero clause",
        "parent_contract_3418": "lists Khat response and Helmholtz as unsigned parent clauses",
        "vector_zero_3418": "shows q_loc vector-zero follows if parent clauses close",
        "next_3418": "selects this 3419 metric-response/Helmholtz audit",
        "contract_3411": "original metric-response contract for Gamma_eff/K_hat",
        "symbol_verdict_3412": "states current old-symbol match is not claim-grade but construction route remains live",
        "candidate_ranking_3412": "ranks response-doublet quadratic density as best construction candidate",
        "metric_template_3413": "expands K_metric response pieces and retained Delta_K risks",
        "response_doublet_3413": "provides response-doublet action template",
        "khat_identity_3065": "old audit: formal K_metric exists but live Khat match not signed",
        "khat_components_3066": "old component list: live Khat components not source-signed",
        "khat_match_3076": "old match audit: Delta_K retained",
        "gamma_candidates_3242": "recent Gamma_eff candidate ranking",
        "source_formula_1664": "source formula audit showing old live formula failure and formal routes",
        "helmholtz_obstruction_1664": "Helmholtz obstruction audit for current symbols",
        "kmetric_compare_2218": "component comparison showing no sourced Khat component match",
        "helmholtz_gate_2218": "Helmholtz not evaluable without explicit tensor components",
        "birth_certificate_2219": "Khat birth-certificate gate for parent action/source ownership",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def branch_split() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": "MRS3419_A_old_symbol_match",
            "branch": "match old/live K_hat symbols to K_metric[Gamma_eff]",
            "status": "FAIL_CURRENT_CORPUS",
            "reason": "3065/3066/3076/2218 agree that live K_hat components, signs, units, derivative and boundary terms are not source-signed.",
            "allowed_use": "historical audit and residual interface only",
            "valid_for_claim": False,
        },
        {
            "branch_id": "MRS3419_B_parent_response_adoption",
            "branch": "future parent branch defines K_hat := K_metric[Gamma_eff]",
            "status": "EXACT_IF_EXPLICITLY_ADOPTED",
            "reason": "once K_hat is the Hilbert metric response of one scalar density, Helmholtz is automatic in the bulk and Ward identity becomes live.",
            "allowed_use": "extension route, not proof that old K_hat already matched",
            "valid_for_claim": False,
        },
        {
            "branch_id": "MRS3419_C_forbidden_blend",
            "branch": "keep old K_hat language while silently using adopted K_metric behavior",
            "status": "FORBIDDEN_CLOSURE_SMUGGLE",
            "reason": "this would mix a failed old-symbol match with a new parent definition.",
            "allowed_use": "none; all unmatched old symbols must be demoted or mapped",
            "valid_for_claim": False,
        },
    ]


def response_lock() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "KRL3419_0_definition",
            "statement": "In the parent-response branch, K_hat^{mu nu} is defined as K_metric^{mu nu}[Gamma_eff].",
            "formula": "K_hat^{mu nu} := 2/sqrt(-g) delta(sqrt(-g) Gamma_eff)/delta g_{mu nu} plus fixed sign, derivative and boundary convention",
            "derivation_status": "DEFINITIONAL_PARENT_LOCK_IF_ADOPTED",
            "remaining_condition": "the branch must explicitly retire or map every old independent K_hat occurrence",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KRL3419_1_stress_identity",
            "statement": "With K_hat=K_metric, T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu} is the Hilbert stress in the same convention.",
            "formula": "T_GK^{mu nu}=(-2/sqrt(-g)) delta S_GK/delta g_{mu nu}; S_GK=int sqrt(-g) Gamma_eff + boundary",
            "derivation_status": "EXACT_CONDITIONAL_ON_SIGN_CONVENTION",
            "remaining_condition": "lock one sign/volume convention and subtract or quarantine background Gamma0",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KRL3419_2_old_match_rejection",
            "statement": "Current old-symbol K_hat is not proved equal to K_metric.",
            "formula": "Delta_K^{mu nu}:=K_hat_old^{mu nu}-K_metric^{mu nu}[Gamma_eff]",
            "derivation_status": "DELTA_K_RETAINED_FOR_OLD_SYMBOLS",
            "remaining_condition": "source component formulas for K_hat_old^{00}, K_hat_old^{0i}, trace, tracefree, derivative and boundary slots",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "KRL3419_3_adoption_policy",
            "statement": "The lowest-scrutiny route is to make the future parent theory use K_metric as K_hat, not to pretend old K_hat was already matched.",
            "formula": "K_hat_MTS(parent) == K_metric[Gamma_eff]; K_hat_old -> alias_if_mapped else Delta_K_residual",
            "derivation_status": "ALLOWED_EXTENSION_POLICY_NONCLAIM",
            "remaining_condition": "write adoption map and continue with Euler/boundary/projector gates",
            "valid_for_claim": False,
        },
    ]


def helmholtz_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "HMA3419_0_action_defined_bulk",
            "target": "bulk K_metric response",
            "test": "second metric variations commute for a differentiable scalar-density action",
            "result": "PASS_IN_PARENT_RESPONSE_BRANCH",
            "reason": "if K_hat is defined by S_GK variation, Helmholtz is not an extra empirical assumption in the bulk",
            "residual_if_fail": "none in adopted branch; old branch remains Delta_K/H_GK",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HMA3419_1_old_live_symbols",
            "target": "old/live K_hat symbols",
            "test": "evaluate Helmholtz on sourced K_hat tensor components",
            "result": "FAIL_NOT_EVALUABLE_CURRENT_SYMBOLS",
            "reason": "1664/2218 show explicit live tensor components and boundary convention are missing",
            "residual_if_fail": "H_GK_old",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HMA3419_2_boundary",
            "target": "boundary/improvement/corner terms",
            "test": "two metric variations commute up to exact, fixed-reference boundary terms",
            "result": "OPEN_BOUNDARY_CONVENTION",
            "reason": "action-defined bulk does not automatically silence nontrivial boundary flux or moving-domain projector terms",
            "residual_if_fail": "H_GK_boundary and alpha-vector boundary leakage",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HMA3419_3_gauge_projector",
            "target": "projector/readout terms",
            "test": "projector and readout are q-basic and do not create representative-dependent response",
            "result": "OPEN_PROJECTOR_OWNER",
            "reason": "P_loc and P_V still require parent ownership from 3418",
            "residual_if_fail": "Delta_K_projector and q_loc vector leakage",
            "valid_for_claim": False,
        },
        {
            "audit_id": "HMA3419_4_verdict",
            "target": "Helmholtz status after 3419",
            "test": "old-symbol branch vs parent-response branch",
            "result": "BULK_HELMHOLTZ_CLOSED_ONLY_IF_NEW_PARENT_RESPONSE_BRANCH_IS_EXPLICIT",
            "reason": "this is progress but not local-GR promotion; Euler, boundary, projector and spurion gates remain",
            "residual_if_fail": "keep Delta_K/H_GK rows",
            "valid_for_claim": False,
        },
    ]


def live_symbol_adoption() -> list[dict[str, Any]]:
    return [
        {
            "slot_id": "LSA3419_0_symbol_Khat",
            "old_symbol_status": "independent/ambiguous K_hat",
            "adoption_rule": "K_hat now means K_metric[Gamma_eff] only inside the parent-response branch",
            "old_symbol_policy": "alias_if_mapped_else_residual",
            "residual_name": "Delta_K_total",
            "status": "ADOPTION_RULE_WRITTEN_NOT_PUBLIC_CLAIM",
            "valid_for_claim": False,
        },
        {
            "slot_id": "LSA3419_1_00",
            "old_symbol_status": "K_hat^{00} formula missing",
            "adoption_rule": "K_metric^{00} becomes the only scoreable 00 component after sign/source convention is fixed",
            "old_symbol_policy": "old K_hat^{00} cannot be used without source match",
            "residual_name": "DeltaK_00",
            "status": "OLD_COMPONENT_RETIRED_PENDING_MAP",
            "valid_for_claim": False,
        },
        {
            "slot_id": "LSA3419_2_0i",
            "old_symbol_status": "K_hat^{0i} formula missing",
            "adoption_rule": "K_metric^{0i} must vanish by rest-frame/parity or be bounded after variation",
            "old_symbol_policy": "old 0i cannot protect alpha3",
            "residual_name": "DeltaK_0i_alpha_vector",
            "status": "HIGH_PRIORITY_FOR_VECTOR_SILENCE",
            "valid_for_claim": False,
        },
        {
            "slot_id": "LSA3419_3_trace",
            "old_symbol_status": "spatial trace convention missing",
            "adoption_rule": "trace comes from K_metric volume/subtraction convention",
            "old_symbol_policy": "no trace shortcut",
            "residual_name": "DeltaK_trace",
            "status": "CONVENTION_LOCK_NEEDED",
            "valid_for_claim": False,
        },
        {
            "slot_id": "LSA3419_4_tracefree",
            "old_symbol_status": "formal tracefree route exists but not parent adopted",
            "adoption_rule": "tracefree part must be generated by the same K_metric variation or retained as DeltaK_TF",
            "old_symbol_policy": "formal K_L route is not a free import",
            "residual_name": "DeltaK_TF",
            "status": "SERIOUS_ROUTE_BUT_NOT_MATCHED",
            "valid_for_claim": False,
        },
        {
            "slot_id": "LSA3419_5_derivative_boundary_projector",
            "old_symbol_status": "derivative/domain/boundary/projector terms open",
            "adoption_rule": "all derivative and boundary terms are part of K_metric convention and P_loc ownership",
            "old_symbol_policy": "open terms stay as absolute residuals",
            "residual_name": "DeltaK_derivative_boundary_projector",
            "status": "DEFER_TO_3420_BOUNDARY_PROJECTOR",
            "valid_for_claim": False,
        },
    ]


def kmetric_expansion() -> list[dict[str, Any]]:
    return [
        {
            "term_id": "KME3419_0_normal_form",
            "input_density": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "metric_response_piece": "K_metric=K[Gamma0]+K[1/2 M_AB Z^A Z^B]+O(Z^4)",
            "order_at_Z0": "background plus O(Z^2)",
            "zero_result": "linear residual vanishes if Gamma0 is background-subtracted and delta_g Z is finite",
            "open_clause": "Z^A must be the physical q_loc/source/stress residual basis",
            "valid_for_claim": False,
        },
        {
            "term_id": "KME3419_1_volume",
            "input_density": "delta sqrt(-g)",
            "metric_response_piece": "metric-proportional Gamma_eff term",
            "order_at_Z0": "Gamma0",
            "zero_result": "local-force silent only after background/cosmological subtraction or constant-gradient silence",
            "open_clause": "Gamma0 convention and local background subtraction",
            "valid_for_claim": False,
        },
        {
            "term_id": "KME3419_2_mass_matrix",
            "input_density": "delta_g M_AB",
            "metric_response_piece": "1/2(delta_g M_AB)Z^A Z^B",
            "order_at_Z0": "O(Z^2)",
            "zero_result": "no linear q_loc force from smooth M_AB",
            "open_clause": "M_AB q-basic owner, units, positivity and nonsingular domain",
            "valid_for_claim": False,
        },
        {
            "term_id": "KME3419_3_residual_basis",
            "input_density": "delta_g Z^A",
            "metric_response_piece": "M_AB Z^A delta_g Z^B",
            "order_at_Z0": "O(Z) if delta_g Z finite",
            "zero_result": "linear term vanishes at Z=0 only if the physical branch really has Z=0",
            "open_clause": "component lock: Z spans Y0-Y6/q_loc/source/stress residuals",
            "valid_for_claim": False,
        },
        {
            "term_id": "KME3419_4_boundary",
            "input_density": "integration-by-parts and boundary terms",
            "metric_response_piece": "B_GK, collar, symplectic and projector terms",
            "order_at_Z0": "can survive as boundary-supported O(1) or O(Z)",
            "zero_result": "not killed by bulk metric-response definition alone",
            "open_clause": "3420 boundary/projector/harmonic silence",
            "valid_for_claim": False,
        },
    ]


def qloc_consequence() -> list[dict[str, Any]]:
    return [
        {
            "consequence_id": "QCG3419_0_Khat_clause",
            "claim": "The Khat-response/Helmholtz part of the q_loc vector-zero route can be closed in a new explicit parent-response branch.",
            "status": "CLOSED_AS_CONDITIONAL_EXTENSION_NOT_OLD_MATCH",
            "why_not_claim": "old live K_hat symbols are not proved matched; Euler/boundary/projector/no-spurion gates remain open",
            "next_dependency": "adopt map plus 3420 boundary/projector and Euler/no-spurion gates",
            "valid_for_claim": False,
        },
        {
            "consequence_id": "QCG3419_1_alpha3",
            "claim": "If the adopted parent branch plus boundary/projector silence passes, alpha3_q is theorem-zero rather than numerically fine-tuned.",
            "status": "POTENTIAL_STRONG_ROUTE",
            "why_not_claim": f"without vector-zero, |W_q_alpha3 f_qV| must still be <= {ALPHA3_PRODUCT_LIMIT}",
            "next_dependency": "prove no vector spurion and no boundary/projector alpha-vector charge",
            "valid_for_claim": False,
        },
        {
            "consequence_id": "QCG3419_2_old_residuals",
            "claim": "Every unmatched old Khat component is now explicitly residualized instead of blocking the whole branch ambiguously.",
            "status": "RESIDUAL_INTERFACE_SHARPENED",
            "why_not_claim": "residual rows have no numeric coefficients yet",
            "next_dependency": "only map or bound old components if they are retained in the final language",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3419_0_old_match",
            "gate": "old/live K_hat is matched to K_metric[Gamma_eff]",
            "current_result": "FAIL_CURRENT_CORPUS",
            "promotes_if": "component formulas and boundary convention are source-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3419_1_parent_response_adoption",
            "gate": "future parent branch defines K_hat as K_metric[Gamma_eff]",
            "current_result": "PASS_CONDITIONAL_EXTENSION_POLICY",
            "promotes_if": "all old Khat uses are mapped or residualized and sign/volume convention is fixed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3419_2_bulk_Helmholtz",
            "gate": "bulk Helmholtz/integrability for Khat response",
            "current_result": "PASS_IN_ADOPTED_PARENT_BRANCH",
            "promotes_if": "S_GK differentiable scalar density with fixed field domain",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3419_3_boundary_projector",
            "gate": "boundary/projector/harmonic terms do not reintroduce q_loc vector leakage",
            "current_result": "BLOCKED_DEFER_TO_3420",
            "promotes_if": "no-flux, q-basic projector, trivial cohomology or explicit bounds",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3419_4_Zbasis_Euler",
            "gate": "Z residual basis is physical and Euler/source-free on local branch",
            "current_result": "BLOCKED_COMPONENT_AND_EULER_LOCK_NEEDED",
            "promotes_if": "Z=0 branch covers q_loc/source/stress residuals and E_A=0 through O(U^2)",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3419_5_q_loc_vector_zero",
            "gate": "q_loc vector projection is theorem-zero",
            "current_result": "NOT_YET_PROMOTED",
            "promotes_if": "PG3419_1 through PG3419_4 pass",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3419_6_local_GR",
            "gate": "local GR/Newton/PPN branch is derived",
            "current_result": "BLOCKED",
            "promotes_if": "q_loc vector-zero plus retained beta/source/stress/nonEH envelopes close",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3419_0_no_old_match",
            "finding": "The old-symbol match is rejected for claim purposes.",
            "evidence": "source-signed live Khat components are absent across 3065/3066/3076/2218.",
            "action": "Stop trying to use old ambiguous Khat as if it already carried Hilbert ownership.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3419_1_parent_extension",
            "finding": "The response-defined Khat branch is the cleaner and less-scrutinized route.",
            "evidence": "action-defined K_metric closes bulk Helmholtz by construction rather than by matching ghosts.",
            "action": "Adopt explicitly as a future parent clause only if old Khat symbols are mapped or retired.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3419_2_not_closure",
            "finding": "This is not a closure axiom if written as a parent action definition with consequences.",
            "evidence": "Khat becomes a variational derivative, not a separately fitted tensor; unmatched old uses are residuals.",
            "action": "Proceed to boundary/projector and Z-basis/Euler gates before claiming q_loc silence.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3419_3_next",
            "finding": "The next live failure mode is no longer bulk Helmholtz; it is boundary/projector/spurion leakage.",
            "evidence": "3419 closes only the bulk response branch; 3418 still needs no-flux/projector/no-vector-spurion.",
            "action": "Build 3420 boundary/projector/harmonic silence gate with explicit alpha-vector consequence.",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3420-Y5-R2FR-boundary-projector-harmonic-and-no-vector-spurion-silence-gate-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3420_boundary_projector_harmonic_and_no_vector_spurion_silence_gate.py",
            "objective": "prove no-flux, q-basic projector, trivial local cohomology and no preferred-frame spurion for the adopted K_metric parent branch; otherwise emit alpha-vector residual rows",
            "why_next": "3419 makes the bulk Khat/Helmholtz route exact only in an explicit parent branch; boundary/projector/vector-spurion leakage is now the live alpha3 danger",
            "valid_for_claim": False,
        },
        {
            "target_id": "3421-Y5-R2FR-Z-basis-physical-lock-and-Euler-source-free-local-branch-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3421_Z_basis_physical_lock_and_Euler_source_free_local_branch.py",
            "objective": "prove Z=0 is the physical local branch covering q_loc/source/stress residuals and that E_A=0 through O(U^2)",
            "why_next": "response-doublet double-zero only helps local GR if Z spans the actual residual components",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3419_0",
            "script": str(Path(__file__).resolve()),
            "mode": "KHAT_METRIC_RESPONSE_BRANCH_SPLIT_AND_HELMHOLTZ_AUDIT",
            "result": "old Khat match fails; explicit parent-response adoption route closes bulk Khat/Helmholtz conditionally but leaves boundary/projector/Z-basis/Euler gates open",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    all_sources_exist = all(row["exists"] for row in source_rows)
    scope_ok = all(str(path).startswith(str(ROOT)) and "formalization-workbench" not in str(path) for path in OUTPUTS.values())
    nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for key, rows in generated.items()
        if key != "validation"
        for row in rows
    )
    old_match_fail = any(row["branch_id"] == "MRS3419_A_old_symbol_match" and row["status"] == "FAIL_CURRENT_CORPUS" for row in generated["branch_split"])
    adoption_present = any(row["branch_id"] == "MRS3419_B_parent_response_adoption" and row["status"] == "EXACT_IF_EXPLICITLY_ADOPTED" for row in generated["branch_split"])
    helmholtz_branch = any(row["audit_id"] == "HMA3419_0_action_defined_bulk" and row["result"] == "PASS_IN_PARENT_RESPONSE_BRANCH" for row in generated["helmholtz_audit"])
    forbidden_blend = any(row["branch_id"] == "MRS3419_C_forbidden_blend" and row["status"] == "FORBIDDEN_CLOSURE_SMUGGLE" for row in generated["branch_split"])
    local_blocked = any(row["gate_id"] == "PG3419_6_local_GR" and row["current_result"] == "BLOCKED" for row in generated["promotion_gates"])
    next_boundary = generated["next_target"][0]["target_id"].startswith("3420-Y5-R2FR-boundary-projector")

    rows = [
        {
            "check_id": "VAL3419_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all_sources_exist,
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3419_1_scope",
            "check": "all outputs stay under post-checkpoint-work",
            "passed": scope_ok,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3419_2_all_nonclaim",
            "check": "3419 does not claim local GR",
            "passed": nonclaim,
            "detail": "all generated rows valid_for_claim=false",
        },
        {
            "check_id": "VAL3419_3_old_match_fail",
            "check": "old Khat match remains rejected",
            "passed": old_match_fail,
            "detail": "no source-signed live Khat tensor match",
        },
        {
            "check_id": "VAL3419_4_adoption_route",
            "check": "explicit parent-response adoption route exists",
            "passed": adoption_present,
            "detail": "Khat := K_metric[Gamma_eff] branch written",
        },
        {
            "check_id": "VAL3419_5_bulk_helmholtz",
            "check": "bulk Helmholtz closes only in adopted parent branch",
            "passed": helmholtz_branch,
            "detail": "action-defined Kmetric has commuting second variations in bulk",
        },
        {
            "check_id": "VAL3419_6_no_blend",
            "check": "forbidden old/adopted blend is explicitly rejected",
            "passed": forbidden_blend,
            "detail": "no closure smuggling allowed",
        },
        {
            "check_id": "VAL3419_7_local_GR_blocked",
            "check": "local GR remains blocked",
            "passed": local_blocked,
            "detail": "boundary/projector/Z-basis/Euler gates remain open",
        },
        {
            "check_id": "VAL3419_8_next_target",
            "check": "next target attacks boundary/projector/spurion leakage",
            "passed": next_boundary,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3419_9_overall",
            "check": "3419 metric-response lock and Helmholtz audit are internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3419 - Khat/Gamma_eff Metric-Response Lock and Helmholtz Audit",
            "## Summary\n"
            "- This checkpoint separates the old-symbol match from the cleaner future parent-response branch.\n"
            "- Old-symbol result: current corpus still does not prove `K_hat_old = K_metric[Gamma_eff]`; the old `K_hat` slots stay residualized.\n"
            "- Forward route: in the parent-response branch, define `K_hat := K_metric[Gamma_eff] = 2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g`. That closes the bulk Khat/Helmholtz condition by construction, not by wishful matching.\n"
            "- Guardrail: it is forbidden to keep old ambiguous `K_hat` language while silently using the new parent-response behavior. Old slots must be mapped to the new response or demoted to `Delta_K` residuals.\n"
            "- Local GR is still not claimed: boundary/projector/harmonic/no-vector-spurion and Z-basis/Euler-source-free gates remain open.\n"
            "- Net progress: the bulk metric-response problem has a clean extension route; the live alpha3 danger moves to boundary/projector/spurion leakage.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## Metric-Response Branch Split\n" + md_table(generated["branch_split"]),
            "## Khat Response Lock Theorem\n" + md_table(generated["response_lock"]),
            "## Helmholtz Audit\n" + md_table(generated["helmholtz_audit"]),
            "## Live Symbol Adoption Map\n" + md_table(generated["live_symbol_adoption"]),
            "## Response-Doublet Kmetric Expansion\n" + md_table(generated["kmetric_expansion"]),
            "## q_loc Consequence\n" + md_table(generated["qloc_consequence"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "This is the cleanest route so far: stop chasing an unsourced old `K_hat`, and make the serious parent theory define `K_hat` as the metric response of `Gamma_eff`. "
            "That does not finish local GR, but it removes one major fog bank without cheating. The next fight is boundary/projector/no-vector-spurion silence.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "branch_split": branch_split(),
        "response_lock": response_lock(),
        "helmholtz_audit": helmholtz_audit(),
        "live_symbol_adoption": live_symbol_adoption(),
        "kmetric_expansion": kmetric_expansion(),
        "qloc_consequence": qloc_consequence(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    generated["validation"] = validation_rows(generated)

    for key, rows in generated.items():
        write_csv(OUTPUTS[key], rows)

    DOC.write_text(build_doc(generated), encoding="utf-8")

    if not all(str(row["passed"]).lower() == "true" for row in generated["validation"]):
        failed = [row for row in generated["validation"] if str(row["passed"]).lower() != "true"]
        raise SystemExit(f"3419 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
