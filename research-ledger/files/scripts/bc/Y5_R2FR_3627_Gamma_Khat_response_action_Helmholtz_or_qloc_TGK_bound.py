from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHECKPOINT_ID = "3627"
BRANCH_ID = "MTS_R2FR_Y5_GAMMA_KHAT_RESPONSE_ACTION_HELMHOLTZ_OR_QLOC_TGK_BOUND_3627"
DOC = ROOT / "3627-Y5-R2FR-Gamma-Khat-response-action-Helmholtz-or-qloc-TGK-bound.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8", errors="replace")


def output_paths() -> dict[str, Path]:
    return {
        "source_register": RESIDUALS / "P8_Y5_R2FR_3627_SOURCE_REGISTER.csv",
        "helmholtz_gate": RESIDUALS / "P8_Y5_R2FR_3627_SGK_HELMHOLTZ_ACTION_GATE.csv",
        "metric_response": RESIDUALS / "P8_Y5_R2FR_3627_GAMMA_KHAT_METRIC_RESPONSE_DERIVATION.csv",
        "double_zero": RESIDUALS / "P8_Y5_R2FR_3627_EULER_DOUBLE_ZERO_BOUNDARY_GATE.csv",
        "bound_rows": RESIDUALS / "P8_Y5_R2FR_3627_QLOC_TGK_BOUND_ROWS.csv",
        "decision_gates": RESIDUALS / "P8_Y5_R2FR_3627_DECISION_GATES.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3627_STATUS.csv",
        "next_target": RESIDUALS / "P8_Y5_R2FR_3627_NEXT_TARGET.csv",
        "canonical_status": RESIDUALS / "P8_Y5_Gamma_Khat_SGK_Helmholtz_status.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3627_VALIDATION.csv",
    }


def source_map() -> list[dict[str, str]]:
    return [
        {
            "source_id": "handoff_3626",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3626_NEXT_TARGET.csv"),
            "needle": "Gamma-Khat-response-action-Helmholtz",
            "role": "3626 handoff to S_GK Helmholtz/action-existence gate.",
        },
        {
            "source_id": "inventory_3626",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3626_LOCAL_RESIDUAL_LAGRANGIAN_INVENTORY.csv"),
            "needle": "ACTION_EXISTENCE_AND_HELMHOLTZ_NOT_PROVED",
            "role": "3626 mapped q_loc/T_GK to S_GK candidate owner.",
        },
        {
            "source_id": "euler_map_3626",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3626_EULER_VARIATION_CLOSURE_MAP.csv"),
            "needle": "EVM3626_2_GK_Helmholtz",
            "role": "3626 identifies Helmholtz/Euler test.",
        },
        {
            "source_id": "component_rows_3626",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv"),
            "needle": "MISSING_QLOC_OR_COFRAME_PROJECTION",
            "role": "nonclaim PPN component rows to update if action fails.",
        },
        {
            "source_id": "gk_first_variation",
            "path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"),
            "needle": "GK513_0_action_existence",
            "role": "Gamma/Khat/q_loc action-existence contract.",
        },
        {
            "source_id": "gk_candidates",
            "path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "needle": "GK514_A_metric_response_scalar_density",
            "role": "candidate S_GK action families.",
        },
        {
            "source_id": "stress_rewrite",
            "path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv"),
            "needle": "SR513_0_define_extra_stress",
            "role": "algebraic q_loc/T_GK rewrite.",
        },
        {
            "source_id": "demotion",
            "path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv"),
            "needle": "QR513_0_nonvariational_stress",
            "role": "explicit demotion/fallback cases.",
        },
        {
            "source_id": "metric_contract",
            "path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv"),
            "needle": "MR514_1_Khat_metric_response",
            "role": "metric-response contract clauses.",
        },
        {
            "source_id": "metric_audit",
            "path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv"),
            "needle": "MA515_1_Khat_metric_response",
            "role": "prior audit: metric response not matched in current corpus.",
        },
        {
            "source_id": "response_doublet",
            "path": str(RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"),
            "needle": "RD516_5_PPN_lock",
            "role": "response-doublet alternate repair route.",
        },
        {
            "source_id": "q_loc_1011",
            "path": str(ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md"),
            "needle": "7.432631961576971e-06",
            "role": "existing compact-shell q_loc proxy and bound-fill rows.",
        },
        {
            "source_id": "ppn_schema_3625",
            "path": str(RESIDUALS / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv"),
            "needle": "ENV3625_2_preferred_frame",
            "role": "PPN/Newton envelope components for q_loc/T_GK fallback.",
        },
    ]


def source_register_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    rows: list[dict[str, object]] = []
    for item in source_map():
        path = Path(item["path"])
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                **item,
                "exists": path.exists(),
                "needle_found": path.exists() and contains(path, item["needle"]),
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def helmholtz_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "HAG3627_0_stress_rewrite",
            "test": "algebraic stress rewrite",
            "requirement": "define T_GK^{mn}=Gamma_eff g^{mn}-K_hat^{mn} and q_loc^n=P_loc nabla_m T_GK^{mn}",
            "derived_or_tested": "This rewrite is an algebraic identity and is already usable as a residual definition.",
            "current_status": "PASS_IDENTITY_NOT_ACTION_PROOF",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "HAG3627_1_action_existence",
            "test": "local scalar action exists",
            "requirement": "there exists S_GK[g,Phi] with T_GK^{mn}=-(2/sqrt(-g)) delta S_GK/delta g_mn",
            "derived_or_tested": "Necessary for deriving q_loc zero from a Ward identity rather than imposing it.",
            "current_status": "NOT_SUPPLIED_CURRENT_CORPUS",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "HAG3627_2_Helmholtz_symmetry",
            "test": "variational Helmholtz/integrability",
            "requirement": "delta(sqrt(-g)T_GK^{mn})/delta g_ab is symmetric as a second variation up to boundary terms",
            "derived_or_tested": "Without this symmetry no metric action can generate the claimed stress.",
            "current_status": "NOT_CHECKED_CURRENT_MTS",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "HAG3627_3_metric_response_candidate_A",
            "test": "Gamma scalar-density response",
            "requirement": "Gamma_eff is a covariant scalar density and K_hat equals its metric response under one fixed sign convention",
            "derived_or_tested": "If S_GK=-int sqrt(-g)Gamma_eff and K_hat=K_metric, then T_GK becomes parent-owned.",
            "current_status": "BEST_CANDIDATE_NOT_MATCHED_TO_EXISTING_MTS",
            "source_path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "HAG3627_4_positive_auxiliary_candidate_B",
            "test": "positive auxiliary/no-hair action",
            "requirement": "L_GK=-1/2 G_AB grad Phi^A grad Phi^B - V(Phi) matches Gamma/Khat pieces and has a positive source-free local operator",
            "derived_or_tested": "Would derive local silence by mass gap/no-hair if symbol matching and source zero hold.",
            "current_status": "CONDITIONAL_CANDIDATE_NEEDS_SYMBOL_MATCH",
            "source_path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "HAG3627_5_topological_candidate_C",
            "test": "exact/topological sector",
            "requirement": "S_GK=int dB_GK or topological density gives zero bulk stress and fixed/no-flux boundary charge",
            "derived_or_tested": "Could kill bulk q_loc but does not by itself solve boundary/source mass leakage.",
            "current_status": "BOUNDARY_FLUX_RISK_OPEN",
            "source_path": str(RESIDUALS / "P8_GK_STRESS_ACTION_CANDIDATES.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "gate_id": "HAG3627_6_verdict",
            "test": "current S_GK proof status",
            "requirement": "all action-existence, Helmholtz, metric-response, Euler, double-zero, projector, and boundary gates pass",
            "derived_or_tested": "Current corpus has a serious route but not a proof; fallback q_loc/T_GK component rows remain required.",
            "current_status": "SGK_NOT_CLAIMED_BOUND_BRANCH_REQUIRED",
            "source_path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv"),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def metric_response_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "MRD3627_0_candidate_action",
            "statement": "Candidate A treats Gamma_eff as the scalar density that generates K_hat by metric response.",
            "formula": "S_GK=-int d^4x sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)",
            "condition": "Gamma_eff covariant, local, unit-declared, and fixed before readout",
            "result_if_true": "Gamma_eff/K_hat become one variational object rather than independent knobs",
            "current_status": "FORMULA_WRITTEN_NOT_PARENT_MATCHED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "MRD3627_1_metric_response",
            "statement": "The metric response defines the tensor piece that must match K_hat.",
            "formula": "K_metric^{mn}:= -2 delta Gamma_eff/delta g_mn - convention_terms; equivalently T_GK^{mn}=Gamma_eff g^{mn}-K_metric^{mn}",
            "condition": "one fixed sign/volume convention is declared and derivative/boundary terms are included",
            "result_if_true": "K_hat^{mn}=K_metric^{mn} closes the Gamma/Khat response pair",
            "current_status": "MATCH_MISSING_CURRENT_CORPUS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "MRD3627_2_Ward_residual",
            "statement": "Diffeomorphism invariance then makes q_loc a Ward/Euler residual.",
            "formula": "nabla_m T_GK^{mn}=sum_A E_A nabla^n Phi^A + boundary/nonlocal terms",
            "condition": "S_GK is diffeomorphism-invariant and Phi^A are the actual fields in Gamma_eff/K_hat",
            "result_if_true": "q_loc^n=P_loc nabla_m T_GK^{mn} vanishes on shell in source-free compact local branch if boundary terms vanish",
            "current_status": "EXACT_CONDITIONAL_NOT_SIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "derivation_id": "MRD3627_3_Helmholtz_obstruction",
            "statement": "If K_hat is not the metric response of Gamma_eff, the response action route fails.",
            "formula": "delta(sqrt(-g)(Gamma g-Khat)^{mn})/delta g_ab != symmetric second variation => no S_GK",
            "condition": "computed response operator fails Helmholtz symmetry or source/boundary terms cannot repair it",
            "result_if_true": "Gamma_eff/K_hat are closure bookkeeping and must be scored as q_loc/T_GK residuals",
            "current_status": "OBSTRUCTION_NOT_RESOLVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def double_zero_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "zero_id": "DZ3627_0_background_subtraction",
            "clause": "constant background",
            "required_condition": "Gamma_eff(Phi0) is constant and absorbed into Lambda_eff/background subtraction",
            "effect": "no local force from the value of Gamma_eff at the fixed point",
            "current_status": "CONDITIONAL_STANDARD_NOT_PARENT_MATCHED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "zero_id": "DZ3627_1_stress_value",
            "clause": "stress zero/value gate",
            "required_condition": "T_GK^{mn}(Phi0)=Gamma_eff(Phi0)g^{mn}-K_hat^{mn}(Phi0)=0 or pure background",
            "effect": "no zeroth-order local metric/source residual",
            "current_status": "NOT_MATCHED_CURRENT_CORPUS",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "zero_id": "DZ3627_2_first_variation",
            "clause": "F_1/double-zero gate",
            "required_condition": "partial_A T_GK^{mn}(Phi0)=0, equivalently partial_A[Gamma_eff g^{mn}-K_hat^{mn}]_{Phi0}=0",
            "effect": "linear PPN/fifth-force/source-normalization leakage is absent",
            "current_status": "F1_NOT_PROVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "zero_id": "DZ3627_3_positive_operator",
            "clause": "Euler/no-hair gate",
            "required_condition": "extra-field operator has positive Hessian/gap after gauge/constraint removal and no source term",
            "effect": "compact local exterior gives delta Phi=0 or exponentially bounded hair",
            "current_status": "POSITIVE_OPERATOR_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "zero_id": "DZ3627_4_boundary",
            "clause": "boundary/no-flux gate",
            "required_condition": "S_GK boundary/symplectic terms have zero or fixed topological flux through linked local surfaces",
            "effect": "bulk q_loc zero does not leak into source mass or radial force",
            "current_status": "BOUNDARY_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bound_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "QTB3627_0_compact_proxy",
            "quantity": "max |P_loc d_rel J_rel| or q_loc leakage proxy",
            "candidate_value": "7.432631961576971e-06",
            "units": "dimensionless_proxy",
            "bound_or_gate": "not a claim curve; requires mapping to PPN/source-normalization units",
            "source_path": str(ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md"),
            "status": "RETAINED_ANCHOR_PROXY_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "QTB3627_1_alpha3",
            "quantity": "q_loc preferred-frame alpha3 channel",
            "candidate_value": "MISSING_QLOC_TO_ALPHA3_COEFFICIENT",
            "units": "dimensionless",
            "bound_or_gate": "alpha3 comparator requires official/source-backed bound row and projection coefficient",
            "source_path": str(ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md"),
            "status": "MAPPING_MISSING_BLOCKED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "QTB3627_2_PPN_metric_tail",
            "quantity": "T_GK/q_loc contribution to gamma,beta,xi",
            "candidate_value": "MISSING_WEAK_FIELD_METRIC_SOLUTION",
            "units": "dimensionless_vector",
            "bound_or_gate": "component projections must feed ENV3625_0..ENV3625_3 with no-cancellation guard",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3625_PPN_NEWTON_ENVELOPE_SCHEMA.csv"),
            "status": "PPN_MAPPING_MISSING_BLOCKED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "QTB3627_3_Newton_source",
            "quantity": "T_GK/q_loc contribution to delta_Newton_MTS",
            "candidate_value": "MISSING_PI00_DELTAE_OR_SOURCE_PROFILE",
            "units": "dimensionless_or_acceleration_profile",
            "bound_or_gate": "Newton/GM row requires source mass not defined by measured GM",
            "source_path": str(RESIDUALS / "P8_Y5_R2FR_3626_PPN_COMPONENT_FILL_ROWS.csv"),
            "status": "SOURCE_MASS_CLOSURE_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "QTB3627_4_TGK_stress_norm",
            "quantity": "||T_GK|| local exterior stress norm",
            "candidate_value": "MISSING_TGK_STRESS_NORM_OR_ZERO_THEOREM",
            "units": "stress_or_metric_response_units",
            "bound_or_gate": "metric Green-function response bound required before PPN scoring",
            "source_path": str(RESIDUALS / "P8_GK_METRIC_RESPONSE_CONTRACT.csv"),
            "status": "STRESS_NORM_MISSING_BLOCKED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "bound_id": "QTB3627_5_boundary_flux",
            "quantity": "S_GK boundary/symplectic flux",
            "candidate_value": "MISSING_BOUNDARY_FLUX_OR_NO_FLUX_THEOREM",
            "units": "flux_over_MH_or_declared_boundary_units",
            "bound_or_gate": "bulk q_loc zero cannot claim local GR until boundary flux is zero/fixed/bounded",
            "source_path": str(RESIDUALS / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv"),
            "status": "BOUNDARY_NO_FLUX_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_gate_rows() -> list[dict[str, object]]:
    timestamp = utc_now()
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3627_0_identity",
            "decision": "q_loc is exactly the projected divergence of T_GK once T_GK=Gamma_eff g-K_hat is defined.",
            "status": "ALGEBRAIC_PROGRESS",
            "next_action": "use this identity as the residual definition whether or not S_GK exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3627_1_action_route",
            "decision": "The least-scrutiny derivation route is candidate A: Gamma_eff as a covariant scalar density and K_hat as its metric response.",
            "status": "BEST_ROUTE_SELECTED_NOT_CLOSED",
            "next_action": "construct explicit Gamma_eff scalar density and compute K_metric in 3628",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3627_2_current_claim",
            "decision": "Current corpus does not prove S_GK action-existence, Helmholtz symmetry, metric-response match, double-zero, or boundary no-flux.",
            "status": "SGK_NOT_CLAIMED",
            "next_action": "do not claim local q_loc/T_GK silence from 3627",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3627_3_bound_branch",
            "decision": "q_loc/T_GK component-bound rows are staged and remain nonclaim; only the old compact-shell proxy has a numeric anchor and it is not a claim curve.",
            "status": "BOUND_BRANCH_STAGED_NOT_SCORED",
            "next_action": "fill weak-field projection, stress norm, and official/source-backed bounds if action route fails",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "decision_id": "DEC3627_4_next_target",
            "decision": "Next checkpoint should attempt the explicit Gamma_eff scalar-density construction and K_metric comparison.",
            "status": "NEXT_TARGET_SELECTED",
            "next_action": "3628-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS3627_0",
            "result": "SGK_HELMHOLTZ_ROUTE_CONDITIONAL_BOUND_BRANCH_STAGED_NO_CLAIM",
            "summary": "3627 derives the exact conditional route from Gamma_eff/K_hat to a variational S_GK and q_loc Ward residual, but current corpus does not pass action-existence, Helmholtz, metric-response, double-zero, or boundary gates; q_loc/T_GK bound rows are staged nonclaim.",
            "stress_identity_available": True,
            "SGK_action_claimed": False,
            "bound_rows_staged": True,
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "next_id": "NEXT3627_0",
            "target_doc": "3628-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md",
            "target_script": "scripts/Y5_R2FR_3628_SGK_explicit_scalar_density_construction_or_bound_runner.py",
            "objective": "attempt an explicit Gamma_eff scalar-density construction, compute the corresponding K_metric response, compare it to K_hat, and either sign the metric-response owner or demote q_loc/T_GK to the nonclaim bound runner",
            "success_gate": "Gamma_eff has declared fields/units/covariance, K_metric is computed with boundary terms, K_hat-K_metric is zero or a retained coefficient row, and F1/double-zero plus boundary gates are evaluated",
            "reason": "3627 shows the route is mathematically clean but unsigned; the next real leap is an explicit scalar-density object, not another generic gate.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def canonical_status_rows() -> list[dict[str, object]]:
    return [
        {
            "timestamp_utc": utc_now(),
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "SGK_route": "EXACT_CONDITIONAL_NOT_SIGNED",
            "q_loc_identity": "q_loc=P_loc_div_TGK",
            "Helmholtz_status": "ACTION_EXISTENCE_AND_METRIC_RESPONSE_MATCH_MISSING",
            "bound_branch": "QLOC_TGK_NONCLAIM_ROWS_STAGED",
            "local_GR_claim": "NO_CLAIM",
            "next_pressure_point": "explicit_Gamma_eff_scalar_density_and_Kmetric_comparison",
            "valid_for_claim": False,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def write_markdown() -> None:
    sources = source_register_rows()
    helmholtz = helmholtz_gate_rows()
    metric = metric_response_rows()
    double_zero = double_zero_rows()
    bounds = bound_rows()
    decisions = decision_gate_rows()
    status = status_rows()
    next_target = next_target_rows()
    content = f"""# 3627 Y5 R2FR Gamma-Khat response action Helmholtz or q_loc/T_GK bound

**Status:** {status[0]["summary"]}

**Claim ceiling:** no `S_GK`, `q_loc=0`, `T_GK=0`, PPN, Newton, R10/R11, source-normalization, or local-GR claim is allowed from 3627.

## Core result

The clean route is now exact but conditional:

```text
T_GK^{{mn}} := Gamma_eff g^{{mn}} - K_hat^{{mn}}
q_loc^n := P_loc nabla_m T_GK^{{mn}}
```

If there exists a diffeomorphism-invariant `S_GK[g,Phi]` with `T_GK=-(2/sqrt(-g)) delta S_GK/delta g`, then

```text
nabla_m T_GK^{{mn}} = sum_A E_A nabla^n Phi^A + boundary terms.
```

So `q_loc -> 0` can be derived in a compact source-free local branch only if the Euler terms, double-zero/fixed-point terms, projector ownership, and boundary flux terms also close. Current corpus has the algebraic identity and candidate route, not the signed action.

## Source register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Helmholtz/action gate

{markdown_table(helmholtz, ["gate_id", "test", "requirement", "current_status"])}

## Metric-response derivation

{markdown_table(metric, ["derivation_id", "statement", "formula", "condition", "current_status"])}

## Euler / double-zero / boundary gate

{markdown_table(double_zero, ["zero_id", "clause", "required_condition", "effect", "current_status"])}

## q_loc / T_GK bound rows

{markdown_table(bounds, ["bound_id", "quantity", "candidate_value", "units", "bound_or_gate", "status"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "status", "next_action"])}

## Next target

{markdown_table(next_target, ["target_doc", "target_script", "objective", "success_gate"])}
"""
    DOC.write_text(content, encoding="utf-8")


def validate() -> list[dict[str, object]]:
    timestamp = utc_now()
    paths = output_paths()
    pre_validation = {key: path for key, path in paths.items() if key != "validation"}
    sources = source_register_rows()
    helmholtz = helmholtz_gate_rows()
    metric = metric_response_rows()
    double_zero = double_zero_rows()
    bounds = bound_rows()
    decisions = decision_gate_rows()
    status = status_rows()
    next_target = next_target_rows()

    results: list[tuple[str, bool, str]] = []
    missing_sources = [row["path"] for row in sources if not row["exists"]]
    results.append(("VAL3627_0_sources_exist", not missing_sources, "all sources exist" if not missing_sources else "; ".join(missing_sources)))
    missing_needles = [row["source_id"] for row in sources if not row["needle_found"]]
    results.append(("VAL3627_1_needles_found", not missing_needles, "all source anchors found" if not missing_needles else "; ".join(missing_needles)))
    missing_outputs = [key for key, path in pre_validation.items() if not path.exists()]
    results.append(("VAL3627_2_outputs_exist", not missing_outputs, "all pre-validation outputs written" if not missing_outputs else "; ".join(missing_outputs)))

    parse_ok = True
    parse_details: list[str] = []
    for key, path in pre_validation.items():
        if path.suffix.lower() != ".csv":
            continue
        try:
            rows = read_csv(path)
            parse_details.append(f"{key}:{len(rows)}")
            if not rows:
                parse_ok = False
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{key}:{exc}")
    results.append(("VAL3627_3_csv_parse", parse_ok, "; ".join(parse_details)))

    identity_ok = any(row["gate_id"] == "HAG3627_0_stress_rewrite" and row["current_status"] == "PASS_IDENTITY_NOT_ACTION_PROOF" for row in helmholtz)
    results.append(("VAL3627_4_stress_identity_written", identity_ok, "q_loc/T_GK algebraic identity written"))
    helmholtz_ok = any(row["gate_id"] == "HAG3627_2_Helmholtz_symmetry" for row in helmholtz)
    results.append(("VAL3627_5_Helmholtz_gate_written", helmholtz_ok, "Helmholtz symmetry gate written"))
    metric_ok = any(row["derivation_id"] == "MRD3627_1_metric_response" and "K_metric" in row["formula"] for row in metric)
    results.append(("VAL3627_6_metric_response_formula_written", metric_ok, "K_metric response formula written"))
    double_zero_ok = any(row["zero_id"] == "DZ3627_2_first_variation" and "partial_A" in row["required_condition"] for row in double_zero)
    results.append(("VAL3627_7_double_zero_gate_written", double_zero_ok, "F1/double-zero gate written"))
    bound_rows_ok = len(bounds) == 6 and all(row["score_ready"] is False for row in bounds)
    results.append(("VAL3627_8_bound_rows_blocked", bound_rows_ok, "q_loc/T_GK bound rows staged and blocked"))
    sgk_not_claimed = status[0]["SGK_action_claimed"] is False and any(row["current_status"] == "SGK_NOT_CLAIMED_BOUND_BRANCH_REQUIRED" for row in helmholtz)
    results.append(("VAL3627_9_SGK_not_claimed", sgk_not_claimed, "S_GK action remains nonclaim"))
    all_nonclaim = all(row.get("claim_allowed") is False and row.get("valid_for_claim") is False for collection in [helmholtz, metric, double_zero, bounds, decisions, status, next_target] for row in collection)
    results.append(("VAL3627_10_all_outputs_nonclaim", all_nonclaim, "all outputs remain nonclaim"))

    if FORMALIZATION.exists():
        leaked_paths = list(FORMALIZATION.rglob("*3627*"))
        formalization_clean = len(leaked_paths) == 0
        detail = "no 3627 files in formalization-workbench" if formalization_clean else "; ".join(str(path) for path in leaked_paths[:5])
    else:
        formalization_clean = True
        detail = "formalization-workbench not present"
    results.append(("VAL3627_11_no_formalization_leak", formalization_clean, detail))

    next_ok = next_target[0]["target_doc"] == "3628-Y5-R2FR-SGK-explicit-scalar-density-construction-or-bound-runner.md"
    results.append(("VAL3627_12_next_target_written", next_ok, "3628 explicit scalar-density target written"))

    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "validation_id": validation_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in results
    ]


def main() -> None:
    paths = output_paths()
    write_csv(paths["source_register"], source_register_rows())
    write_csv(paths["helmholtz_gate"], helmholtz_gate_rows())
    write_csv(paths["metric_response"], metric_response_rows())
    write_csv(paths["double_zero"], double_zero_rows())
    write_csv(paths["bound_rows"], bound_rows())
    write_csv(paths["decision_gates"], decision_gate_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_csv(paths["canonical_status"], canonical_status_rows())
    write_markdown()
    write_csv(paths["validation"], validate())

    failed = [row for row in read_csv(paths["validation"]) if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3627 validation failed: {failed}")
    print(f"wrote 3627 checkpoint with {len(read_csv(paths['validation']))} validation checks")


if __name__ == "__main__":
    main()
