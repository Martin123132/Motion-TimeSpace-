from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3418-Y5-R2FR-q_loc-vector-zero-Ward-boundary-proof-or-alpha-bound-row-under-AX1090.md"

Q_PROXY = 7.432631961576971e-06
ALPHA3_BOUND = 3.999999999999999e-20
ALPHA3_PRODUCT_LIMIT = ALPHA3_BOUND / Q_PROXY
ALPHA3_ORDER_ONE_MISS_FACTOR = Q_PROXY / ALPHA3_BOUND

SOURCES = {
    "doc_3417": ROOT / "3417-Y5-R2FR-q_loc-U2-alpha-vector-and-retained-beta-stress-bound-pack-under-AX1090.md",
    "projection_split_3417": OUT / "P8_Y5_R2FR_3417_QLOC_PROJECTION_SPLIT.csv",
    "numeric_pressure_3417": OUT / "P8_Y5_R2FR_3417_QLOC_NUMERIC_PRESSURE.csv",
    "ward_rescue_3417": OUT / "P8_Y5_R2FR_3417_WARD_ZERO_RESCUE_GATES.csv",
    "promotion_3417": OUT / "P8_Y5_R2FR_3417_PROMOTION_GATES.csv",
    "next_3417": OUT / "P8_Y5_R2FR_3417_NEXT_TARGET.csv",
    "ward_3411": OUT / "P8_Y5_R2FR_3411_WARD_ZERO_THEOREM.csv",
    "stress_identity_3411": OUT / "P8_Y5_R2FR_3411_STRESS_IDENTITY_PROOF.csv",
    "symbol_audit_3411": OUT / "P8_Y5_R2FR_3411_CURRENT_SYMBOL_MATCH_AUDIT.csv",
    "double_zero_3413": OUT / "P8_Y5_R2FR_3413_DOUBLE_ZERO_PROOF.csv",
    "gates_3413": OUT / "P8_Y5_R2FR_3413_PROMOTION_GATES.csv",
    "hidden_stress_3416": OUT / "P8_Y5_R2FR_3416_HIDDEN_STRESS_EXCLUSION_GATE.csv",
    "local_status_3416": OUT / "P8_Y5_R2FR_3416_LOCAL_GR_STATUS.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3418_SOURCE_REGISTER.csv",
    "vector_zero_derivation": OUT / "P8_Y5_R2FR_3418_VECTOR_ZERO_DERIVATION.csv",
    "parent_contract": OUT / "P8_Y5_R2FR_3418_PARENT_CONTRACT_CLAUSES.csv",
    "boundary_projector_audit": OUT / "P8_Y5_R2FR_3418_BOUNDARY_PROJECTOR_AUDIT.csv",
    "alpha_bound_rows": OUT / "P8_Y5_R2FR_3418_ALPHA_VECTOR_BOUND_ROWS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3418_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3418_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3418_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3418_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3418_VALIDATION.csv",
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

    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = ["| " + " | ".join(cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3417": "declares alpha-vector pressure as next q_loc gate",
        "projection_split_3417": "splits q_loc into scalar, transverse, harmonic and range lanes",
        "numeric_pressure_3417": "provides q_proxy, alpha3 product limit and order-one miss factor",
        "ward_rescue_3417": "lists Ward-zero rescue clauses needing proof",
        "promotion_3417": "keeps local GR blocked until alpha-vector and Ward gates pass",
        "next_3417": "selects this q_loc vector-zero proof or alpha-bound fallback",
        "ward_3411": "conditional Ward-zero theorem for q_loc",
        "stress_identity_3411": "q_loc as projected divergence of effective extra stress",
        "symbol_audit_3411": "records K_hat/Gamma_eff/Helmholtz/Euler/boundary gaps",
        "double_zero_3413": "formal double-zero route and physical-lock caveat",
        "gates_3413": "q_loc local-GR promotion remains blocked",
        "hidden_stress_3416": "q_loc T_GK is safe only if Hilbert/Euler/boundary/vector clauses close",
        "local_status_3416": "local GR status before q_loc vector-zero refinement",
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


def vector_zero_derivation() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "VZD3418_0_projector_definition",
            "claim": "The dangerous q_loc piece is the vector projector P_V q_loc = q_T + q_harmonic.",
            "derivation": "3410/3417 Hodge split: q_loc^nu=q_parallel u^nu + D^nu chi_q + q_T^nu + q_harmonic^nu.",
            "requires": "local rest frame, spatial projector h^mu_nu and a stated local domain",
            "current_status": "PASS_KINEMATIC_ROUTING",
            "valid_for_claim": False,
        },
        {
            "step_id": "VZD3418_1_parent_Noether_identity",
            "claim": "If K_hat is the Hilbert metric response of Gamma_eff, q_loc is a Ward/Euler/boundary residual.",
            "derivation": "Diffeomorphism invariance of sqrt(-g)Gamma_eff gives nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A+nabla_mu B_GK^{mu nu}; q_loc is P_loc of this identity.",
            "requires": "K_hat^{mu nu}=2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_{mu nu} plus Helmholtz symmetry",
            "current_status": "CONDITIONAL_NOT_SYMBOL_SIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "VZD3418_2_bulk_vector_zero",
            "claim": "On source-free local solutions the bulk vector projection vanishes.",
            "derivation": "If E_A=0 through O(U^2), P_V(sum_A E_A nabla^nu Phi^A)=0, so alpha1/alpha2/alpha3 receive no q_loc bulk source.",
            "requires": "source-free Euler closure for every Gamma_eff/K_hat field through O(U^2)",
            "current_status": "CONDITIONAL_EULER_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "VZD3418_3_boundary_harmonic_zero",
            "claim": "The harmonic/transverse boundary projection vanishes on a simply connected no-flux local vacuum patch.",
            "derivation": "For a compact local ball with H^1=0 and P_V n_mu B_GK^{mu nu}=0 on the boundary, Hodge uniqueness leaves q_T=q_harmonic=0.",
            "requires": "trivial local cohomology, no surviving boundary charge, projector commutes with local readout",
            "current_status": "CONDITIONAL_BOUNDARY_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "VZD3418_4_preferred_frame_spurion_zero",
            "claim": "No exchange-odd local spurion means no alpha-vector response coefficient f_qV.",
            "derivation": "In the local matter rest frame, parity-even scalar U^2 data cannot source a transverse preferred-frame vector without a momentum, domain-normal, boundary or hidden-sector vector.",
            "requires": "no momentum spurion, no anisotropic domain normal, no hidden constitutive vector and no boundary flux",
            "current_status": "CONDITIONAL_SPURION_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "VZD3418_5_vector_zero_theorem",
            "claim": "Under VZD3418_1 through VZD3418_4, P_V q_loc=0 and therefore alpha1_q=alpha2_q=alpha3_q=xi_q=0.",
            "derivation": "Ward identity kills bulk, Hodge/no-flux kills harmonic and transverse boundary pieces, and parity/rest-frame silence kills preferred-frame spurions.",
            "requires": "all parent contract clauses PC3418_0 through PC3418_7 pass in the live MTS symbols",
            "current_status": "THEOREM_CONTRACT_BUILT_BUT_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
    ]


def parent_contract() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PC3418_0_scalar_density",
            "required_clause": "Gamma_eff is a scalar density built from q-basic fields and g_obs.",
            "proof_use": "allows diffeomorphism Noether identity",
            "current_evidence": "formal candidate exists in 3411/3413 but not full live-symbol source file",
            "status": "PARTIAL",
            "missing_to_promote": "source path for live Gamma_eff normal form",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3418_1_Khat_Hilbert_response",
            "required_clause": "K_hat^{mu nu}=2/sqrt(-g) delta(sqrt(-g)Gamma_eff)/delta g_{mu nu}.",
            "proof_use": "turns nabla^nu Gamma_eff-nabla_mu K_hat^{mu nu} into a Noether stress identity",
            "current_evidence": "3411 symbol audit says not matched to current symbols",
            "status": "FAIL_CURRENT_UNSIGNED",
            "missing_to_promote": "explicit variational derivative showing Delta_K=0",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3418_2_Helmholtz_integrability",
            "required_clause": "second metric variations are symmetric so K_hat really descends from one parent density.",
            "proof_use": "prevents an arbitrary K_hat from masquerading as Hilbert stress",
            "current_evidence": "3411 symbol audit marks Helmholtz not checked",
            "status": "FAIL_NOT_CHECKED",
            "missing_to_promote": "Helmholtz symmetry table for live K_hat/Gamma_eff symbols",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3418_3_Euler_source_free",
            "required_clause": "all local Gamma_eff fields obey source-free Euler equations through O(U^2).",
            "proof_use": "kills bulk vector q_loc projection",
            "current_evidence": "3411/3416 keep Euler closure open",
            "status": "FAIL_EULER_UNSIGNED",
            "missing_to_promote": "E_A=0 proof or source-backed residual bounds for every live field",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3418_4_boundary_no_flux",
            "required_clause": "P_V n_mu B_GK^{mu nu}=0 and no boundary improvement carries alpha-vector charge.",
            "proof_use": "kills transverse boundary leakage",
            "current_evidence": "3416 hidden/topological boundary row is conditional, not parent-signed",
            "status": "FAIL_BOUNDARY_UNSIGNED",
            "missing_to_promote": "no-flux/Stokes row with zero compact linking charge and fixed reference",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3418_5_projector_commutation",
            "required_clause": "P_loc/P_V commute with the local readout and do not create representative-dependent vector charge.",
            "proof_use": "prevents projection artefacts from reintroducing alpha3",
            "current_evidence": "3416 q_loc T_GK gate keeps projector ownership open",
            "status": "FAIL_PROJECTOR_UNSIGNED",
            "missing_to_promote": "q-basic projector ownership proof",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3418_6_trivial_local_cohomology",
            "required_clause": "the local vacuum patch has H^1=0 or every harmonic one-form has zero physical charge.",
            "proof_use": "kills q_harmonic",
            "current_evidence": "reasonable local-ball route exists but not declared as parent rule",
            "status": "CONDITIONAL_DOMAIN_RULE_NEEDED",
            "missing_to_promote": "local domain axiom/rule with exception handling for topology",
            "valid_for_claim": False,
        },
        {
            "clause_id": "PC3418_7_no_vector_spurion",
            "required_clause": "no momentum, domain-normal, hidden constitutive or boundary vector spurion survives in the local rest frame.",
            "proof_use": "kills f_qV and preferred-frame response",
            "current_evidence": "3417 identifies vector lane but does not zero it",
            "status": "FAIL_SPURION_AUDIT_MISSING",
            "missing_to_promote": "component audit of all vector spurions through O(U^2)",
            "valid_for_claim": False,
        },
    ]


def boundary_projector_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "BPA3418_0_bulk",
            "object": "sum_A E_A nabla^nu Phi^A",
            "vector_leak": "bulk transverse vector if any E_A source or momentum spurion remains",
            "zero_route": "E_A=0 on local vacuum branch",
            "bound_route": "source-backed coefficient for each nonzero E_A projection",
            "current_result": "OPEN",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BPA3418_1_boundary_flux",
            "object": "n_mu B_GK^{mu nu}",
            "vector_leak": "surface transverse vector or alpha3 boundary charge",
            "zero_route": "P_V n_mu B_GK^{mu nu}=0 by no-flux/topological exactness",
            "bound_route": "absolute boundary flux bound in alpha-vector rows",
            "current_result": "OPEN",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BPA3418_2_harmonic",
            "object": "q_harmonic^nu",
            "vector_leak": "nontrivial local cohomology or linking charge",
            "zero_route": "local ball H^1=0 or zero harmonic physical charge",
            "bound_route": "topological/harmonic charge bound",
            "current_result": "OPEN_DOMAIN_RULE_NEEDED",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BPA3418_3_projector",
            "object": "P_loc/P_V readout",
            "vector_leak": "representative Weyl/disformal/projector artefact",
            "zero_route": "q-basic readout and projector commutation",
            "bound_route": "projection artefact coefficient row",
            "current_result": "OPEN",
            "valid_for_claim": False,
        },
        {
            "audit_id": "BPA3418_4_hidden_constitutive",
            "object": "hidden/projector/constitutive stress",
            "vector_leak": "hidden vector stress not included in public Hilbert source",
            "zero_route": "safe-class theorem or source-silent/gapped no-hair",
            "bound_route": "absolute hidden stress projection bound",
            "current_result": "OPEN_RETAINED_RESIDUAL",
            "valid_for_claim": False,
        },
    ]


def alpha_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "AVB3418_0_alpha3_product",
            "quantity": "|W_q_alpha3 f_qV|",
            "required_bound": "alpha3_bound/q_proxy",
            "numeric_bound": ALPHA3_PRODUCT_LIMIT,
            "units": "dimensionless product",
            "source_path": str(SOURCES["numeric_pressure_3417"]),
            "status": "BOUND_FORMULA_READY_PARENT_COEFFICIENTS_MISSING",
            "valid_for_claim": False,
            "notes": "If vector-zero theorem fails, this product must be sourced below 5.38e-15.",
        },
        {
            "row_id": "AVB3418_1_alpha3_order_one_failure",
            "quantity": "alpha3_q if W_q_alpha3 f_qV=1",
            "required_bound": "alpha3_bound",
            "numeric_bound": ALPHA3_BOUND,
            "units": "dimensionless alpha3",
            "source_path": str(SOURCES["numeric_pressure_3417"]),
            "status": "ORDER_ONE_VECTOR_RESPONSE_EXCLUDED",
            "valid_for_claim": False,
            "notes": f"Order-one vector leakage misses alpha3 by {ALPHA3_ORDER_ONE_MISS_FACTOR:.6e}.",
        },
        {
            "row_id": "AVB3418_2_alpha1_alpha2",
            "quantity": "|W_q_alpha{1,2} f_qV|",
            "required_bound": "arena alpha1/alpha2 PPN bounds divided by q_proxy",
            "numeric_bound": "MISSING_ARENA_BOUND_SOURCE",
            "units": "dimensionless product",
            "source_path": "MISSING_EXTERNAL_OR_INTERNAL_BOUND_ROW",
            "status": "BOUND_ROW_NOT_READY",
            "valid_for_claim": False,
            "notes": "Do not infer alpha1/alpha2 safety from scalar beta or alpha3 rows.",
        },
        {
            "row_id": "AVB3418_3_xi_preferred_location",
            "quantity": "|W_q_xi f_xi|",
            "required_bound": "arena xi/preferred-location bound divided by q_proxy",
            "numeric_bound": "MISSING_ARENA_BOUND_SOURCE",
            "units": "dimensionless product",
            "source_path": "MISSING_EXTERNAL_OR_INTERNAL_BOUND_ROW",
            "status": "BOUND_ROW_NOT_READY",
            "valid_for_claim": False,
            "notes": "Domain anisotropy cannot be ignored unless boundary/domain spurions are zero.",
        },
        {
            "row_id": "AVB3418_4_vector_fallback_verdict",
            "quantity": "q_loc alpha-vector fallback",
            "required_bound": "all alpha-vector products sourced or theorem-zero",
            "numeric_bound": "NOT_SCORE_READY",
            "units": "n/a",
            "source_path": str(DOC),
            "status": "PROOF_CONTRACT_FIRST_BOUND_ROWS_SECOND",
            "valid_for_claim": False,
            "notes": "Current best route remains proof of f_qV=0, not numerical fine-tuning to 5e-15.",
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3418_0_vector_theorem_shape",
            "gate": "q_loc vector-zero theorem has a concrete derivation chain",
            "current_result": "PASS_CONDITIONAL_CONTRACT",
            "promotes_if": "not sufficient alone; requires parent contract clauses",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3418_1_Khat_response",
            "gate": "K_hat is the Hilbert metric response of Gamma_eff",
            "current_result": "FAIL_CURRENT_SYMBOL_MATCH_UNSIGNED",
            "promotes_if": "Delta_K=0 and Helmholtz symmetry hold for live MTS symbols",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3418_2_Euler_boundary",
            "gate": "Euler, boundary, harmonic and projector leaks are zero through O(U^2)",
            "current_result": "FAIL_BOUNDARY_PROJECTOR_UNSIGNED",
            "promotes_if": "PC3418_3 through PC3418_6 pass or are explicitly bounded",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3418_3_no_vector_spurion",
            "gate": "No hidden/rest-frame/domain vector spurion survives",
            "current_result": "FAIL_SPURION_AUDIT_MISSING",
            "promotes_if": "PC3418_7 passes or alpha-vector coefficients are sourced below bounds",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3418_4_alpha3_safety",
            "gate": "alpha3 q_loc lane is safe",
            "current_result": "BLOCKED_UNTIL_VECTOR_ZERO_OR_PRODUCT_BOUND",
            "promotes_if": "f_qV=0 theorem or |W_q_alpha3 f_qV|<=5.381673706808059e-15 with sourced coefficients",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3418_5_local_GR",
            "gate": "q_loc no longer blocks local GR/Newton/PPN",
            "current_result": "BLOCKED",
            "promotes_if": "PG3418_1 through PG3418_4 pass plus retained beta/stress lanes are bounded",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3418_0_derivation_status",
            "finding": "The vector-zero route is mathematically coherent, not mystical.",
            "evidence": "Noether/Ward identity plus Hodge/no-flux/parity can force P_V q_loc=0.",
            "action": "Keep derivation route alive, but only as conditional until live symbols sign it.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3418_1_no_smuggling",
            "finding": "The theorem cannot be promoted from covariance alone.",
            "evidence": "K_hat response, Helmholtz integrability, Euler closure, boundary flux and projector ownership are separate clauses.",
            "action": "Do not call local GR recovered from 3418 alone.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3418_2_best_next",
            "finding": "The highest-leverage next proof is K_hat/Gamma_eff metric-response lock.",
            "evidence": "If Delta_K=0 and Helmholtz pass, the Ward identity becomes live rather than decorative.",
            "action": "Build 3419 metric-response symbol-lock before more broad source ledgers.",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3418_3_fallback",
            "finding": "If K_hat lock fails, alpha-vector rows become mandatory.",
            "evidence": "alpha3 product must be <=5.381673706808059e-15; order-one leakage is excluded by ~1.86e14.",
            "action": "Prepare alpha-vector bound path but avoid claiming it without coefficients.",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3419-Y5-R2FR-Khat-Gamma-eff-metric-response-lock-and-Helmholtz-audit-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3419_Khat_Gamma_eff_metric_response_lock_and_Helmholtz_audit.py",
            "objective": "prove or reject Delta_K=K_hat-2/sqrt(-g)delta(sqrt(-g)Gamma_eff)/delta g for live MTS symbols, with Helmholtz symmetry audit",
            "why_next": "3418 shows q_loc vector-zero is available only if K_hat is a real parent metric response; this is the load-bearing clause",
            "valid_for_claim": False,
        },
        {
            "target_id": "3420-Y5-R2FR-boundary-projector-and-harmonic-silence-gate-under-AX1090.md",
            "script": "scripts/Y5_R2FR_3420_boundary_projector_and_harmonic_silence_gate.py",
            "objective": "prove no-flux, trivial local cohomology or bounded harmonic/projector leakage after the Khat response lock is settled",
            "why_next": "boundary/harmonic silence is the second load-bearing clause for P_V q_loc=0",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3418_0",
            "script": str(Path(__file__).resolve()),
            "mode": "VECTOR_ZERO_CONDITIONAL_PROOF_CONTRACT",
            "result": "q_loc vector-zero can be derived under a precise parent contract, but current live-symbol clauses are unsigned; alpha-vector fallback rows are staged nonclaim.",
            "valid_for_claim": False,
        }
    ]


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = generated["source_register"]
    all_sources_exist = all(row["exists"] for row in source_rows)
    all_outputs_in_post = all(str(path).startswith(str(ROOT)) and "formalization-workbench" not in str(path) for path in OUTPUTS.values())
    nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for key, rows in generated.items()
        if key != "validation"
        for row in rows
    )
    theorem_built = any(row["step_id"] == "VZD3418_5_vector_zero_theorem" for row in generated["vector_zero_derivation"])
    parent_unsigned = any(row["status"].startswith("FAIL") for row in generated["parent_contract"])
    alpha_limit_ok = abs(ALPHA3_PRODUCT_LIMIT - 5.381673706808059e-15) < 1e-28
    local_gr_blocked = any(
        row["gate_id"] == "PG3418_5_local_GR" and row["current_result"] == "BLOCKED"
        for row in generated["promotion_gates"]
    )
    next_khat = generated["next_target"][0]["target_id"].startswith("3419-Y5-R2FR-Khat")

    rows = [
        {
            "check_id": "VAL3418_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": all_sources_exist,
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3418_1_scope",
            "check": "all outputs stay under post-checkpoint-work",
            "passed": all_outputs_in_post,
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3418_2_all_nonclaim",
            "check": "3418 does not claim local GR or alpha-vector pass",
            "passed": nonclaim,
            "detail": "all generated rows are valid_for_claim=false",
        },
        {
            "check_id": "VAL3418_3_theorem_contract",
            "check": "vector-zero theorem contract exists",
            "passed": theorem_built,
            "detail": "VZD3418_5 present",
        },
        {
            "check_id": "VAL3418_4_parent_unsigned",
            "check": "unsigned parent clauses prevent promotion",
            "passed": parent_unsigned,
            "detail": "Khat/Helmholtz/Euler/boundary/projector clauses remain unsigned",
        },
        {
            "check_id": "VAL3418_5_alpha3_limit",
            "check": "alpha3 product limit preserved",
            "passed": alpha_limit_ok,
            "detail": f"alpha3_product_limit={ALPHA3_PRODUCT_LIMIT}",
        },
        {
            "check_id": "VAL3418_6_local_GR_blocked",
            "check": "local GR remains blocked",
            "passed": local_gr_blocked,
            "detail": "q_loc vector-zero is conditional only",
        },
        {
            "check_id": "VAL3418_7_next_target",
            "check": "next target attacks load-bearing Khat response",
            "passed": next_khat,
            "detail": generated["next_target"][0]["target_id"],
        },
    ]
    overall = all(row["passed"] for row in rows)
    rows.append(
        {
            "check_id": "VAL3418_8_overall",
            "check": "3418 vector-zero proof contract and fallback rows are internally valid",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
        }
    )
    return rows


def build_doc(generated: dict[str, list[dict[str, Any]]]) -> str:
    return "\n\n".join(
        [
            "# 3418 - q_loc Vector-Zero Ward/Boundary Proof or Alpha-Bound Row",
            "## Summary\n"
            "- This checkpoint does take the leap: it constructs the exact conditional route for `P_V q_loc=0`.\n"
            "- The route is Ward/Noether plus Hodge/no-flux plus rest-frame/parity silence: if those clauses are parent-signed, `alpha1_q`, `alpha2_q`, `alpha3_q`, and `xi_q` vanish as q_loc lanes.\n"
            "- It is not promoted yet. The live MTS symbols still need `K_hat` to be the Hilbert metric response of `Gamma_eff`, plus Helmholtz, Euler, boundary, projector and no-spurion clauses.\n"
            "- If the proof route fails, the alpha3 product must satisfy `|W_q_alpha3 f_qV| <= 5.381673706808059e-15`; order-one vector leakage is excluded by about `1.86e14`.\n"
            "- Best next strike: prove or reject the `K_hat/Gamma_eff` metric-response lock. That is the load-bearing hinge for local GR.",
            "## Source Register\n" + md_table(generated["source_register"]),
            "## Vector-Zero Derivation\n" + md_table(generated["vector_zero_derivation"]),
            "## Parent Contract Clauses\n" + md_table(generated["parent_contract"]),
            "## Boundary/Projector Audit\n" + md_table(generated["boundary_projector_audit"]),
            "## Alpha-Vector Bound Rows\n" + md_table(generated["alpha_bound_rows"]),
            "## Promotion Gates\n" + md_table(generated["promotion_gates"]),
            "## Decision Ledger\n" + md_table(generated["decision_ledger"]),
            "## Next Target\n" + md_table(generated["next_target"]),
            "## Runner Nonclaim\n" + md_table(generated["runner_nonclaim"]),
            "## Validation\n" + md_table(generated["validation"]),
            "## Bottom Line\n"
            "This is progress, not a retreat: `q_loc` vector silence is now a precise theorem contract rather than a vague hope. "
            "The local-GR branch lives or dies next on whether the current MTS `K_hat` is truly the metric response of one parent `Gamma_eff` density.",
        ]
    ) + "\n"


def main() -> None:
    if "formalization-workbench" in str(ROOT):
        raise RuntimeError(f"Refusing to run from formalization-workbench: {ROOT}")

    generated: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "vector_zero_derivation": vector_zero_derivation(),
        "parent_contract": parent_contract(),
        "boundary_projector_audit": boundary_projector_audit(),
        "alpha_bound_rows": alpha_bound_rows(),
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
        raise SystemExit(f"3418 validation failed: {failed}")

    print(f"wrote {len(generated)} CSV artefacts and {DOC}")


if __name__ == "__main__":
    main()
