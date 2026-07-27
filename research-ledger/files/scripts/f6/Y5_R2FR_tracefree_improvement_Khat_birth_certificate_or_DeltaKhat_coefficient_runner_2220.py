from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2220"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2220-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaKhat-coefficient-runner.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2220_SOURCE_REGISTER.csv",
    "birth_certificate": OUT / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE.csv",
    "variation_contract": OUT / "P8_Y5_PARENT_QLOC_2220_KL_VARIATION_AND_COEFFICIENT_CONTRACT.csv",
    "lambda_runner": OUT / "P8_Y5_PARENT_QLOC_2220_LAMBDA_PHI_OBSTRUCTION_RUNNER.csv",
    "delta_envelope": OUT / "P8_Y5_PARENT_QLOC_2220_DELTAKHAT_COEFFICIENT_ENVELOPE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2220_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2220_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2220_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2220_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2220_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2220_TRACEFREE_KHAT_BIRTH_OR_DELTA_ENVELOPE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2220_TRACEFREE_KHAT_DELTA_ENVELOPE_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_TRACEFREE_KHAT_BIRTH_CERTIFICATE_2220_NONCLAIM.csv",
}


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
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2220_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2220-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2220*",
        "*P8_Y5_BRR545_2220*",
        "*Y5_R2FR_tracefree_improvement_Khat_birth_certificate_or_DeltaKhat_coefficient_runner_2220*",
        "*JR2220*",
        "*PARENT_QLOC_TRACEFREE_KHAT_BIRTH_CERTIFICATE_2220*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2219_handoff",
            ROOT / "2219-Y5-R2FR-Khat-source-definition-owner-or-DeltaKhat-component-fill.md",
            ["NEXT2219_0_2220", "KSO2219_2_tracefree_improvement", "VAL2219_OVERALL"],
            "immediate handoff selecting trace-free improvement birth certificate.",
        ),
        (
            "1287_first_component",
            OUT / "P8_Y5_R10_1287_FIRST_KHAT_COMPONENT_ROW_NONCLAIM.csv",
            ["KTC1287_0_flat_Ricci_scalar_KL00", "FORMAL_COMPONENT_ROW_FILLED_NONCLAIM", "CANDIDATE_KHAT_COMPONENT_NOT_MATCHED_TO_CURRENT_MTS_KHAT"],
            "first source-anchored K_L component row.",
        ),
        (
            "1525_origin_doc",
            ROOT / "1525-Y5-parent-Khat-origin-or-Kmetric-derivative-domain-boundary-kernels.md",
            ["KOR1525_2_improvement_action_route", "KER1525_7_verdict", "VAL1525_15_overall"],
            "trace-free improvement route and Kmetric fallback kernels.",
        ),
        (
            "1526_variation_doc",
            ROOT / "1526-Y5-tracefree-Hessian-improvement-action-coefficient-and-symbol-match.md",
            ["VAR1526_3_tracefree_projection", "SIG1526_1_coefficient_law", "VAL1526_16_overall"],
            "exact trace-free projection and coefficient/sign law.",
        ),
        (
            "1527_phi_owner_doc",
            ROOT / "1527-Y5-phi-owner-and-current-Khat-symbol-match-source-hunt.md",
            ["AUX1527_0_local_action_candidate", "MLT1527_4_verdict", "VAL1527_16_overall"],
            "local auxiliary phi contract and multiplier-stress gate.",
        ),
        (
            "1528_lambda_theorem_doc",
            ROOT / "1528-Y5-lambda-phi-silence-no-flux-or-multiplier-stress-bound.md",
            ["LPE1528_6_theorem_shape", "MSB1528_4_verdict", "VAL1528_16_overall"],
            "lambda_phi energy theorem shape and symbolic stress bound.",
        ),
        (
            "1529_boundary_doc",
            ROOT / "1529-Y5-parent-boundary-no-flux-zero-mode-certificate-or-lambda-phi-bound-inputs.md",
            ["VAL1529_15_overall", "NEXT1529_0_1530", "boundary/no-flux certificate"],
            "no boundary/zero-mode certificate; bound inputs staged.",
        ),
        (
            "1530_bound_doc",
            ROOT / "1530-Y5-lambda-phi-bound-input-source-pass.md",
            ["BIA1530_6_delta_g_SGamma_norm", "DGS1530_5_verdict", "VAL1530_15_overall"],
            "lambda_phi bound algebra reduced to Kmetric kernel norms.",
        ),
        (
            "1193_ricci_branch",
            OUT / "P8_Y5_R10_1193_RICCI_EXACT_SCALAR_BRANCH.csv",
            ["RES1193_3_Ricci_flat_limit", "RES1193_5_matter_domain_failure", "RES1193_6_scalar_branch_verdict"],
            "Ricci-flat/Einstein scalar exactness scope and generic matter failure.",
        ),
        (
            "833_amplitude",
            OUT / "P8_Y5_R10_833_HESSIAN_KHAT_AMPLITUDE_LAW.csv",
            ["AL833_1_exact_L2_norm", "AL833_3_Newton_fraction_gate", "local safety must come from metric-nullity"],
            "K_L amplitude is order Gamma and needs response bounds.",
        ),
        (
            "1530_delta_reduction",
            OUT / "P8_Y5_PARENT_QLOC_1530_DELTA_G_SGAMMA_REDUCTION.csv",
            ["DGS1530_3_norm_envelope", "DGS1530_5_verdict", "NOT_NUMERIC_REDUCED_TO_KERNELS"],
            "delta_g S_Gamma reduced to missing Kmetric kernels.",
        ),
        (
            "1529_bound_inputs",
            OUT / "P8_Y5_PARENT_QLOC_1529_LAMBDA_PHI_BOUND_INPUT_LEDGER.csv",
            ["BIN1529_0_C_P", "BIN1529_6_delta_g_SGamma_norm", "BIN1529_8_no_cancellation_guard"],
            "missing bound constants and absolute no-cancellation guard.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def birth_certificate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            certificate_id="TIB2220_0_tensor_shape",
            clause="trace-free tensor shape",
            evidence="VAR1526_3 and KOR1525_1 derive K_L^{mu nu}=2 nabla^mu nabla^nu phi-(1/2)g^{mu nu}Box phi in 4D.",
            status="PASS_CONDITIONAL_MATH",
            blocker="shape equality alone is not parent ownership",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_1_parent_action_shape",
            clause="improvement action term",
            evidence="S_I[c_I]=c_I int sqrt(-g) phi R plus compatible boundary term is written as a candidate.",
            status="SHAPE_WRITTEN_NOT_PARENT_ADOPTED",
            blocker="current MTS parent action has not adopted S_I/S_phiK as live sector",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_2_coefficient_sign",
            clause="coefficient and sign convention",
            evidence="SIG1526_1 derives sigma_resp*c_I=1 for K_hat=K_L in the trace-free derivative channel.",
            status="LAW_DERIVED_VALUE_NOT_SOURCED",
            blocker="sigma_resp and c_I are not source-fixed current conventions",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_3_phi_local_owner",
            clause="local phi owner",
            evidence="1527 stages S_phiK to localize Box phi=S_Gamma and rejects naked inverse Box.",
            status="AUXILIARY_CONTRACT_STAGED_NONCLAIM",
            blocker="S_phiK is not parent-adopted and adds lambda_phi stress",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_4_lambda_phi_silence",
            clause="lambda_phi stress zero or bounded",
            evidence="1528 writes energy theorem shape; 1529 finds no boundary certificate; 1530 has formula-only bound.",
            status="BLOCKED",
            blocker="zero-mode/no-flux certificate and bound constants are missing",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_5_domain_curvature_scope",
            clause="Ricci-flat/Einstein local domain scope",
            evidence="1193 recovers Ricci-flat scalar limit but rejects generic matter-domain scalar closure.",
            status="DOMAIN_LIMITED_NOT_GENERIC",
            blocker="same-parent local-vacuum/Ricci-flat branch certificate is missing",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_6_boundary_projector",
            clause="boundary, zero-mode, projector and domain ownership",
            evidence="1528/1529 keep boundary/no-flux and zero-mode unsigned; 2219 keeps projector/domain residuals open.",
            status="BLOCKED",
            blocker="no parent boundary/zero-mode/projector commutator certificate",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_7_amplitude_response",
            clause="metric amplitude and local observable response",
            evidence="833 shows K_L amplitude is order Gamma; 1530 projection remains schema-only.",
            status="BLOCKED",
            blocker="K_L response coefficient, K00 projection, Pi_gamma/C_op/GM and arena response are missing",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_8_live_Khat_adoption",
            clause="current MTS K_hat adoption",
            evidence="1527 KAD row and 2219 owner audit stage adoption but keep it not live.",
            status="STAGED_NOT_PROMOTED",
            blocker="adoption cannot go live until phi/lambda/boundary/sign/response clauses close",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="TIB2220_9_verdict",
            clause="trace-free improvement Khat birth certificate",
            evidence="combined 2220 gate",
            status="BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
            blocker="promote nothing; retain coefficient-envelope route",
            certificate_pass=False,
        ),
    ]


def variation_contract_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            contract_id="KLC2220_0_variation_identity",
            object="metric variation of sqrt(-g) phi R",
            formula="delta[sqrt(-g)phi R]/delta g^{mu nu}=sqrt(-g)[phi G_mu_nu+(g_mu_nu Box-nabla_mu nabla_nu)phi] plus boundary",
            source_anchor="VAR1526_1_standard_variation_identity",
            usable_now="conditional_formal",
            missing="sign convention; boundary term; current parent adoption",
            score_ready=False,
        ),
        base_row(
            contract_id="KLC2220_1_tracefree_projection",
            object="K_L trace-free response",
            formula="TF[2(nabla^mu nabla^nu phi-g^{mu nu}Box phi)]=2nabla^mu nabla^nu phi-(1/2)g^{mu nu}Box phi",
            source_anchor="VAR1526_3_tracefree_projection",
            usable_now="exact_algebra_nonclaim",
            missing="does not prove live K_hat equals this response",
            score_ready=False,
        ),
        base_row(
            contract_id="KLC2220_2_coefficient_law",
            object="coefficient/sign match",
            formula="sigma_resp*c_I=1",
            source_anchor="SIG1526_1_coefficient_law",
            usable_now="law_written_not_sourced",
            missing="sigma_resp convention and c_I source value",
            score_ready=False,
        ),
        base_row(
            contract_id="KLC2220_3_phi_source",
            object="phi equation",
            formula="Box phi=S_Gamma=(2/3)(Gamma_eff+C)",
            source_anchor="AUX1527_1_lambda_variation;RES1193_3_Ricci_flat_limit",
            usable_now="local_auxiliary_contract_only",
            missing="S_phiK parent adoption; branch/domain/boundary",
            score_ready=False,
        ),
        base_row(
            contract_id="KLC2220_4_multiplier_equation",
            object="lambda_phi equation",
            formula="Box lambda_phi=-c_I R plus convention/boundary terms",
            source_anchor="AUX1527_2_phi_variation;LPE1528_0_multiplier_equation",
            usable_now="obstruction_active",
            missing="lambda_phi zero theorem or finite stress bound",
            score_ready=False,
        ),
        base_row(
            contract_id="KLC2220_5_amplitude_warning",
            object="K_L carrier amplitude",
            formula="||K_L||_L2=sqrt(n/(n-1))*||Gamma||_L2 in flat carrier model",
            source_anchor="AL833_1_exact_L2_norm",
            usable_now="safety_warning",
            missing="metric-nullity or response bound",
            score_ready=False,
        ),
        base_row(
            contract_id="KLC2220_6_verdict",
            object="variation/coefficient contract",
            formula="K_L shape and coefficient law are real conditional math; birth certificate still fails",
            source_anchor="combined 2220",
            usable_now="nonclaim_derivation_gain",
            missing="parent adoption and residual bounds",
            score_ready=False,
        ),
    ]


def lambda_runner_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            runner_id="LPR2220_0_zero_theorem",
            route="prove lambda_phi=0",
            required_inputs="static elliptic branch; R=0 same-parent local vacuum; parent domain; boundary/no-flux; zero-mode fixing",
            current_evidence="1528 theorem shape; 1529 no certificate",
            result="BLOCKED_NOT_ZERO_PROVEN",
            fallback="use multiplier-stress envelope",
            score_ready=False,
        ),
        base_row(
            runner_id="LPR2220_1_bound_formula",
            route="finite lambda_phi stress bound",
            required_inputs="C_P; C_E; C_T; R_norm; boundary_source_norm; initial_data/static exclusion; delta_g_SGamma_norm; observable projection",
            current_evidence="1530 organizes formula but values are missing",
            result="FORMULA_ONLY_NOT_SCORE_READY",
            fallback="source Kmetric kernel norms and projection constants",
            score_ready=False,
        ),
        base_row(
            runner_id="LPR2220_2_delta_g_SGamma",
            route="reduce delta_g S_Gamma",
            required_inputs="M_m; M_L; K_conn; K_domain; K_boundary; sign/volume; units",
            current_evidence="1530 DGS1530_5 reduces to Kmetric kernels",
            result="REDUCED_TO_SAME_KERNEL_BOTTLENECK",
            fallback="2221 Kmetric kernel norm source pass",
            score_ready=False,
        ),
        base_row(
            runner_id="LPR2220_3_Khat_promotion",
            route="promote Khat=K_L",
            required_inputs="TIB2220 birth certificate passes and lambda_phi zero/bound accepted",
            current_evidence="birth certificate fails; lambda_phi unresolved",
            result="BLOCKED_NO_PROMOTION",
            fallback="retain Delta_Khat coefficient envelope",
            score_ready=False,
        ),
        base_row(
            runner_id="LPR2220_4_verdict",
            route="lambda_phi obstruction",
            required_inputs="zero theorem or score-ready absolute bound",
            current_evidence="neither route closes",
            result="ACTIVE_OBSTRUCTION",
            fallback="do not publish/local-claim; run kernel norm pass",
            score_ready=False,
        ),
    ]


def delta_envelope_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            envelope_id="DKE2220_0_KL_adoption_defect",
            residual_symbol="Delta_Khat_KL_adoption",
            formula="K_hat_live - K_L",
            bound_or_condition="zero only if current MTS explicitly adopts K_hat:=TF[sigma_resp*c_I metric response int sqrt(-g)phi R]",
            missing_inputs="live adoption source; parent action term; sign convention",
            status="ZERO_NOT_PROVEN_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            envelope_id="DKE2220_1_coeff_sign_defect",
            residual_symbol="Delta_cI_sigma",
            formula="|sigma_resp*c_I-1| * ||K_L||",
            bound_or_condition="requires sigma_resp*c_I=1 or a finite coefficient error bound",
            missing_inputs="sigma_resp; c_I; coefficient uncertainty; K_L norm",
            status="COEFFICIENT_VALUE_MISSING",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            envelope_id="DKE2220_2_lambda_stress",
            residual_symbol="epsilon_lambda_phi",
            formula="<= |C_T|*(C_E*A)^2 + |C_T|*C_P*C_E*A*||delta_g S_Gamma||, A=|c_I|||R||+boundary_source_norm+initial_data_norm",
            bound_or_condition="absolute no-cancellation envelope if lambda_phi zero theorem fails",
            missing_inputs="C_P; C_E; C_T; R_norm; boundary_source_norm; initial_data_norm; delta_g_SGamma_norm",
            status="FORMULA_ONLY_NOT_NUMERIC",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            envelope_id="DKE2220_3_delta_g_SGamma",
            residual_symbol="epsilon_delta_g_SGamma",
            formula="<=(2/3)(L_cg^-2|F_prime|||M_m||+2L_cg^-3|F||||M_L||+||K_conn||+||K_domain||+||K_boundary||)",
            bound_or_condition="kernel norm source pass can make lambda_phi bound score-ready",
            missing_inputs="M_m; M_L; K_conn; K_domain; K_boundary; L_cg; F; F_prime; units",
            status="REDUCED_TO_KERNEL_NORMS",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            envelope_id="DKE2220_4_curvature_domain_remainder",
            residual_symbol="epsilon_Ricci_curl",
            formula="curved scalar exactness remainder from 2 nabla_[alpha](R_{beta]sigma}nabla^sigma phi)",
            bound_or_condition="zero on same-parent Ricci-flat/Einstein branch; otherwise finite curvature/domain bound",
            missing_inputs="domain classifier; Ricci norm; alignment theorem or remainder norm",
            status="DOMAIN_LIMITED_BOUND_REQUIRED",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            envelope_id="DKE2220_5_amplitude_response",
            residual_symbol="epsilon_KL_metric_response",
            formula="metric_response_coeff * |K_L00| / |4*pi*G*rho/c^2| with ||K_L||~||Gamma||",
            bound_or_condition="K_L cancellation of divergence is not a PPN/Newton safety proof",
            missing_inputs="response coefficient; K00 projection; matter curvature; source normalization",
            status="AMPLITUDE_RESPONSE_MISSING",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            envelope_id="DKE2220_6_observable_projection",
            residual_symbol="epsilon_projection",
            formula="Pi_gamma/P_loc/C_op/GM projection of K_L plus lambda_phi stress into q_loc_hat",
            bound_or_condition="needed before PPN/R10/clock/orbital scoring",
            missing_inputs="Pi_gamma; P_loc; C_op; Q_lambda; measured GM normalization",
            status="PROJECTION_SCHEMA_ONLY",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            envelope_id="DKE2220_7_total",
            residual_symbol="Delta_Khat_tracefree_total",
            formula="abs-sum of DKE2220_0..6",
            bound_or_condition="no cancellation between K_L, Gamma, lambda_phi, boundary or projection terms",
            missing_inputs="all component source values or theorem-zero certificates",
            status="TOTAL_ENVELOPE_NONCLAIM",
            score_ready=False,
            valid_prediction_row=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2220_0_tracefree_math",
            gate="trace-free improvement math derived",
            status="PASS_CONDITIONAL_NONCLAIM",
            reason="K_L shape and coefficient law are real conditional results.",
        ),
        base_row(
            gate_id="CG2220_1_birth_certificate",
            gate="trace-free Khat birth certificate passes",
            status="BLOCKED_NONCLAIM",
            reason="parent adoption, phi owner, lambda_phi, boundary, domain and response clauses fail.",
        ),
        base_row(
            gate_id="CG2220_2_lambda_phi",
            gate="lambda_phi zero or finite accepted bound",
            status="BLOCKED_NONCLAIM",
            reason="zero theorem lacks boundary/zero-mode certificate and bound lacks input values.",
        ),
        base_row(
            gate_id="CG2220_3_delta_envelope",
            gate="Delta_Khat coefficient envelope staged",
            status="PASS_NONCLAIM",
            reason="failed clauses are converted into explicit residual channels.",
        ),
        base_row(
            gate_id="CG2220_4_local_GR_Newton",
            gate="local GR/Newton reduction claim",
            status="BLOCKED_NONCLAIM",
            reason="Khat adoption and q_loc observable projection remain blocked.",
        ),
        base_row(
            gate_id="CG2220_5_GitHub",
            gate="GitHub/public update",
            status="BLOCKED_NONCLAIM",
            reason="private branch remains mid-proof and nonclaim.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2220_0_gain",
            decision="TRACEFREE_IMPROVEMENT_ROUTE_IS_REAL_MATH",
            rationale="the phi R trace-free variation gives the K_L tensor shape and coefficient law; this is not a vibe.",
            next_action="preserve it as best Khat candidate.",
        ),
        base_row(
            decision_id="DEC2220_1_failure",
            decision="BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS",
            rationale="the local auxiliary route creates lambda_phi stress, and no zero theorem or finite bound is source-ready.",
            next_action="do not promote Khat=K_L.",
        ),
        base_row(
            decision_id="DEC2220_2_shared_blocker",
            decision="DELTAG_SGAMMA_KERNELS_ARE_THE_SHARED BOTTLENECK".replace(" ", "_"),
            rationale="lambda_phi bound and Delta_Khat computability both reduce to M_m, M_L, K_conn, K_domain and K_boundary norms.",
            next_action="source or bound Kmetric kernel norms next.",
        ),
        base_row(
            decision_id="DEC2220_3_no_claim",
            decision="LOCAL_GR_REMAINS_BLOCKED_NOT_DEAD",
            rationale="one serious route is isolated; failure is at explicit source/norm clauses, not at the tensor identity.",
            next_action="run 2221 kernel norm source pass before empirical local tests or GitHub.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2220_0_2221",
            selection_status="selected",
            target_file="2221-Y5-R2FR-delta-g-SGamma-Kmetric-kernel-norm-source-pass.md",
            target_script="scripts/Y5_R2FR_delta_g_SGamma_Kmetric_kernel_norm_source_pass_2221.py",
            objective="source or bound the Kmetric kernel norms controlling delta_g S_Gamma and Delta_Khat: M_m, M_L, K_conn, K_domain, K_boundary, sign/units, L_cg, F and F_prime.",
            success_condition="kernel norms become source-backed theorem-zero or finite coefficient rows; otherwise local branch remains explicit residual-bound only.",
            do_not_do="do not set delta_g S_Gamma to zero from fixed-point language; do not promote Khat/local GR; do not use GitHub.",
        ),
        base_row(
            route_id="NEXT2220_1_boundary_parallel",
            selection_status="held_parallel",
            target_file="2221b-Y5-R2FR-parent-boundary-zero-mode-certificate-retry.md",
            target_script="scripts/Y5_R2FR_parent_boundary_zero_mode_certificate_retry_2221b.py",
            objective="retry the lambda_phi boundary/zero-mode proof only if a new parent boundary certificate source appears.",
            success_condition="Dirichlet or Neumann plus zero-mode reference is parent-signed.",
            do_not_do="do not import boundary precedent as proof.",
        ),
        base_row(
            route_id="NEXT2220_2_response_parallel",
            selection_status="held_parallel",
            target_file="2221c-Y5-R2FR-KL-amplitude-response-to-PPN-source-pack.md",
            target_script="scripts/Y5_R2FR_KL_amplitude_response_to_PPN_source_pack_2221c.py",
            objective="build source rows for K_L amplitude response if Khat adoption later closes.",
            success_condition="response coefficient/K00 projection/matter curvature rows are source-backed.",
            do_not_do="do not score PPN from formal K_L alone.",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["delta_envelope"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["delta_envelope"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["birth_certificate"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        count = 0
        if source.exists():
            shutil.copyfile(source, target)
            copied = True
            parse_ok, count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    birth_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    lambda_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2220_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2220_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    birth_ok = len(birth_rows) == 10 and any(row.get("certificate_id") == "TIB2220_9_verdict" and row.get("status") == "BIRTH_CERTIFICATE_FAILS_CURRENT_CORPUS" for row in birth_rows)
    birth_ok = birth_ok and all(not truthy(row.get("certificate_pass")) for row in birth_rows)
    add("VAL2220_02_birth_certificate", birth_ok, "birth certificate attempts promotion and correctly refuses it")

    variation_ok = any(row.get("contract_id") == "KLC2220_1_tracefree_projection" for row in variation_rows)
    variation_ok = variation_ok and any(row.get("contract_id") == "KLC2220_2_coefficient_law" for row in variation_rows)
    variation_ok = variation_ok and all(not truthy(row.get("score_ready")) for row in variation_rows)
    add("VAL2220_03_variation_contract", variation_ok, "K_L trace-free variation and coefficient law are recorded nonclaim")

    lambda_ok = any(row.get("runner_id") == "LPR2220_4_verdict" and row.get("result") == "ACTIVE_OBSTRUCTION" for row in lambda_rows)
    lambda_ok = lambda_ok and all(not truthy(row.get("score_ready")) for row in lambda_rows)
    add("VAL2220_04_lambda_runner", lambda_ok, "lambda_phi obstruction is active and not score-ready")

    envelope_ok = len(envelope_rows) == 8 and any(row.get("envelope_id") == "DKE2220_7_total" for row in envelope_rows)
    envelope_ok = envelope_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in envelope_rows)
    add("VAL2220_05_delta_envelope", envelope_ok, "Delta_Khat coefficient envelope rows are explicit and nonclaim")

    claim_ok = any(row.get("gate_id") == "CG2220_1_birth_certificate" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2220_4_local_GR_Newton" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2220_06_claim_gate", claim_ok, "birth certificate and local-GR/Newton claims remain blocked")

    decision_ok = any(row.get("decision") == "DELTAG_SGAMMA_KERNELS_ARE_THE_SHARED_BOTTLENECK" for row in decision_rows_)
    add("VAL2220_07_decision", decision_ok, "decision selects Kmetric kernel norms as shared blocker")

    next_ok = any(row.get("route_id") == "NEXT2220_0_2221" and "kernel-norm" in str(row.get("target_file")) for row in next_rows)
    add("VAL2220_08_next_target", next_ok, "2221 Kmetric kernel norm source pass selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2220_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2220_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, birth_rows, variation_rows, lambda_rows, envelope_rows, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2220_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    no_score_promoted = all(
        not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row"))
        for group in [envelope_rows]
        for row in group
    )
    no_score_promoted = no_score_promoted and all(not truthy(row.get("score_ready")) for row in variation_rows + lambda_rows)
    add("VAL2220_12_no_score_promotion", no_score_promoted, "no formula-only row is score/promoted")

    formalization_clean = not formalization_has_2220_artifacts()
    add("VAL2220_13_formalization_clean", formalization_clean, "formalization-workbench has no 2220 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2220_14_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2220_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2220 confirms the trace-free improvement Khat route is real conditional math but fails the current birth certificate, emits nonclaim Delta_Khat coefficient envelopes, and selects delta_g S_Gamma/Kmetric kernel norm sourcing next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    birth_rows: list[dict[str, Any]],
    variation_rows: list[dict[str, Any]],
    lambda_rows: list[dict[str, Any]],
    envelope_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2220 - Y5/R2FR Trace-Free Improvement Khat Birth Certificate Or DeltaKhat Coefficient Runner",
        "",
        "## Current Verdict",
        "",
        "2220 takes the cleanest Khat leap and refuses to fake the landing.",
        "",
        "The positive result is real: the trace-free part of the metric variation of `int sqrt(-g) phi R` gives the `K_L` tensor shape, and the coefficient law `sigma_resp*c_I=1` is the exact adoption condition for the local trace-free derivative channel.",
        "",
        "The promotion still fails because the local auxiliary route needs `lambda_phi` to be zero or bounded. The previous 1528-1530 trail already showed that zero-mode/no-flux is not parent-signed, and the multiplier-stress bound reduces to missing `delta_g S_Gamma` / Kmetric kernel norms.",
        "",
        "So `K_hat=K_L` is not live. The branch advances by turning that failure into an explicit `Delta_Khat_tracefree_total` coefficient envelope and selecting the shared blocker: `M_m`, `M_L`, `K_conn`, `K_domain`, `K_boundary`, sign/units, `L_cg`, `F`, and `F_prime`.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Trace-Free Improvement Birth Certificate",
        "",
        md_table(birth_rows, ["certificate_id", "clause", "evidence", "status", "blocker", "certificate_pass", "valid_for_claim"]),
        "",
        "## K_L Variation And Coefficient Contract",
        "",
        md_table(variation_rows, ["contract_id", "object", "formula", "source_anchor", "usable_now", "missing", "score_ready", "valid_for_claim"]),
        "",
        "## Lambda Phi Obstruction Runner",
        "",
        md_table(lambda_rows, ["runner_id", "route", "required_inputs", "current_evidence", "result", "fallback", "score_ready", "valid_for_claim"]),
        "",
        "## Delta Khat Coefficient Envelope",
        "",
        md_table(envelope_rows, ["envelope_id", "residual_symbol", "formula", "bound_or_condition", "missing_inputs", "status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is a good narrowing. The best Khat candidate survived as mathematics but not as a live parent object. The failure is now concentrated in sourceable quantities rather than philosophical mush: kernel norms and projection constants. That is exactly the kind of thing a serious testable framework can carry forward.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    birth_rows = birth_certificate_rows()
    variation_rows = variation_contract_rows()
    lambda_rows = lambda_runner_rows()
    envelope_rows = delta_envelope_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["birth_certificate"], birth_rows),
        (OUTPUTS["variation_contract"], variation_rows),
        (OUTPUTS["lambda_runner"], lambda_rows),
        (OUTPUTS["delta_envelope"], envelope_rows),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        birth_rows,
        variation_rows,
        lambda_rows,
        envelope_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        birth_rows,
        variation_rows,
        lambda_rows,
        envelope_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
