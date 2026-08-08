from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2219"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2219-Y5-R2FR-Khat-source-definition-owner-or-DeltaKhat-component-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2219_SOURCE_REGISTER.csv",
    "birth_certificate": OUT / "P8_Y5_PARENT_QLOC_2219_KHAT_BIRTH_CERTIFICATE_GATE.csv",
    "owner_audit": OUT / "P8_Y5_PARENT_QLOC_2219_KHAT_SOURCE_OWNER_AUDIT.csv",
    "component_fill": OUT / "P8_Y5_PARENT_QLOC_2219_DELTA_KHAT_COMPONENT_FILL.csv",
    "nonclaim_rows": OUT / "P8_Y5_PARENT_QLOC_2219_KHAT_NONCLAIM_COMPONENT_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2219_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2219_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2219_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2219_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2219_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2219_KHAT_SOURCE_OWNER_OR_DELTA_FILL_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2219_DELTA_KHAT_COMPONENT_FILL_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_KHAT_SOURCE_OWNER_2219_NONCLAIM.csv",
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


def formalization_has_2219_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2219-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2219*",
        "*P8_Y5_BRR545_2219*",
        "*Y5_R2FR_Khat_source_definition_owner_or_DeltaKhat_component_fill_2219*",
        "*JR2219*",
        "*PARENT_QLOC_KHAT_SOURCE_OWNER_2219*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2218_handoff",
            ROOT / "2218-Y5-R2FR-Kmetric-vs-Khat-tensor-comparison-and-Helmholtz-gate.md",
            ["NEXT2218_0_2219", "KTC2218_6_verdict", "VAL2218_OVERALL"],
            "immediate handoff: source Khat or fill Delta_Khat components.",
        ),
        (
            "2218_delta_rows",
            OUT / "P8_Y5_PARENT_QLOC_2218_DELTA_KHAT_ACQUISITION_ROWS.csv",
            ["DKA2218_0_volume", "DKA2218_7_total", "NONCLAIM_ACQUISITION_ROW"],
            "generic Delta_Khat acquisition rows that 2219 concretizes.",
        ),
        (
            "515_metric_response_audit",
            ROOT / "515-match-Gamma-eff-Khat-to-metric-response-action.md",
            ["MA515_1_Khat_metric_response", "RO515_C_response_displacement_pair", "D515_0"],
            "older strict no-match audit and response/displacement repair route.",
        ),
        (
            "756_symbol_match",
            ROOT / "756-Y5-R10-Gamma-Khat-metric-response-symbol-match-or-q_loc-component-candidate-builder.md",
            ["MRM756_2_Khat_identification", "RDR756_1_metric_response_of_doublet", "QCB756_5_no_fake_data_guard"],
            "no-fake-data guard and response-doublet physical-lock warning.",
        ),
        (
            "830_owner_audit_doc",
            ROOT / "830-Y5-R10-Khat-boundary-owner-or-residual-vector-runner.md",
            ["KO830_0_parent_tensor_operator", "KO830_5_verdict", "OG830_1_PPN"],
            "Khat owner theorem requirements and arena gates.",
        ),
        (
            "831_range_contract_doc",
            ROOT / "831-Y5-R10-parent-Khat-tensor-operator-or-local-branch-closure.md",
            ["OC831_1_balance_action", "RT831_1_projection_law", "PA831_5_verdict"],
            "D_T range/cokernel reduction and parent-adoption failure.",
        ),
        (
            "1525_origin_audit",
            OUT / "P8_Y5_PARENT_QLOC_1525_KHAT_ORIGIN_AUDIT.csv",
            ["KOR1525_2_improvement_action_route", "KOR1525_3_current_symbol_match", "KOR1525_5_verdict"],
            "trace-free improvement route is precise but not live.",
        ),
        (
            "1527_adoption_row",
            OUT / "P8_Y5_PARENT_QLOC_1527_KHAT_ADOPTION_ROW.csv",
            ["KAD1527_0_adoption_contract", "KAD1527_3_symbol_status", "KAD1527_4_verdict"],
            "staged nonclaim adoption row for Khat as trace-free improvement response.",
        ),
        (
            "1664_source_formula_audit",
            OUT / "P8_Y5_PARENT_QLOC_1664_GAMMA_KHAT_SOURCE_FORMULA_AUDIT.csv",
            ["SFA1664_1_live_Khat_operator", "SFA1664_2_improvement_candidate", "SFA1664_5_verdict"],
            "live Khat operator still missing while formal rescue routes remain nonclaim.",
        ),
        (
            "2111_match_gate",
            OUT / "P8_Y5_PARENT_QLOC_2111_KHAT_MATCH_GATE.csv",
            ["KMG2111_3_live_Khat", "KMG2111_4_connection", "KMG2111_8_verdict"],
            "conditional algebraic closure but live Khat/connection/domain/boundary still open.",
        ),
        (
            "2207_match_audit",
            OUT / "P8_Y5_PARENT_QLOC_2207_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
            ["KMR2207_2_Khat_identity", "KMR2207_3_double_zero", "KMR2207_5_overall"],
            "formal variation exists; Khat identity and units/readout fail.",
        ),
        (
            "1366_match_ledger",
            OUT / "P8_Y5_R10_1366_KMETRIC_KHAT_MATCH_LEDGER.csv",
            ["MATCH1366_2_Kmetric_kernel", "MATCH1366_3_live_Khat_comparison", "MATCH1366_4_acceptance"],
            "component kernels and residual Delta_K remain not computable.",
        ),
        (
            "223_constitutive_owner",
            ROOT / "223-X-constraint-algebra-and-Khat-Gamma-constitutive-owner.md",
            ["P^{mu nu}=partial V_def/partial Z_{mu nu}", "trace/traceless split", "`P` constitutive owner derived"],
            "defect-potential throat: elegant owner contract, not derived.",
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
            certificate_id="KBC2219_0_parent_action_term",
            required_clause="specific parent action term exists before readout",
            pass_condition="S_Khat[g,fields] is written with field content, coefficients, sign and domain.",
            best_current_evidence="1527 stages TF[metric response of int sqrt(-g) phi R]; 831 stages S_bal as a contract.",
            current_status="STAGED_NOT_PARENT_SIGNED",
            blocker="no live parent adoption or coefficient/sign/boundary certificate",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="KBC2219_1_live_tensor_formula",
            required_clause="K_hat^{mu nu} tensor formula exists component-by-component",
            pass_condition="formula includes volume, trace-free projection, derivative, connection, domain, projector and boundary terms.",
            best_current_evidence="1525/1527 give K_L candidate; 2218 says live Khat component source is absent.",
            current_status="CANDIDATE_ONLY",
            blocker="live MTS K_hat is not equal to K_L by sourced definition",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="KBC2219_2_same_branch_Gamma_link",
            required_clause="Gamma_eff and K_hat are projections of the same parent object",
            pass_condition="one parent field/action produces scalar Gamma and tensor Khat without post-readout tuning.",
            best_current_evidence="223 defect potential and 515 response/displacement route are coherent contracts.",
            current_status="CONTRACT_ONLY",
            blocker="V_def/Z_mu_nu or response field not derived",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="KBC2219_3_metric_variation_or_operator_owner",
            required_clause="Khat is Hilbert response or parent Euler/balance operator",
            pass_condition="either Khat=K_metric[Gamma_eff] or S_bal/equivalent D_T operator is parent-signed.",
            best_current_evidence="831 derives D_T range/cokernel law; 515/756 refuse live metric-response match.",
            current_status="MATHEMATICAL_ROUTE_NOT_ADOPTED",
            blocker="operator/range route is not a parent action block",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="KBC2219_4_boundary_projector_domain",
            required_clause="boundary, projector and domain variations are owned",
            pass_condition="K_boundary, K_domain, K_conn and P_loc commutator are zero/proper or finite with source paths.",
            best_current_evidence="2111 and 1366 explicitly retain these terms.",
            current_status="OPEN_RETAINED_RESIDUALS",
            blocker="no no-flux/corner/commutator theorem",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="KBC2219_5_units_readout",
            required_clause="stress-density units and local observable readout are fixed",
            pass_condition="Gamma_eff, K_hat, q_loc, PPN/R10/clock/orbital response rows share one unit convention.",
            best_current_evidence="515 MA515_6 and 2207 KMR2207_4 keep units/readout missing.",
            current_status="MISSING_UNITS_READOUT",
            blocker="cannot score local tests from symbolic tensors",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="KBC2219_6_matter_descent",
            required_clause="ordinary matter reads only the descended local metric/coframe",
            pass_condition="quotient-invariant matter action and coframe/connection descent are signed.",
            best_current_evidence="830 keeps matter descent as an owner clause.",
            current_status="OPEN",
            blocker="WEP/clock cannot be protected by geometry-only closure",
            certificate_pass=False,
        ),
        base_row(
            certificate_id="KBC2219_7_verdict",
            required_clause="all Khat source-owner birth certificate clauses pass",
            pass_condition="KBC2219_0..6 are source-signed in one branch.",
            best_current_evidence="combined 2219 audit",
            current_status="BIRTH_CERTIFICATE_NOT_CLOSED",
            blocker="no live source-owned Khat definition can be promoted",
            certificate_pass=False,
        ),
    ]


def owner_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            owner_id="KSO2219_0_live_symbol_owner",
            route="current corpus K_hat as already-defined tensor",
            candidate_formula="live K_hat^{mu nu}",
            source_evidence="1664 SFA1664_1 and 2111 KMG2111_3",
            source_owner_status="FAIL_CURRENT_CORPUS",
            why_not_promoted="no explicit tensor/operator expression before projection with units, derivative, boundary, projector and domain terms",
            next_repair="source live tensor formula or stop treating Khat as independently known",
            source_owner_signed=False,
            preferred_route=False,
        ),
        base_row(
            owner_id="KSO2219_1_metric_response_scalar_density",
            route="K_hat := K_metric[Gamma_eff]",
            candidate_formula="2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} minus sign/volume convention",
            source_evidence="515 MA515_1; 2217 FMV; 2218 Kmetric table",
            source_owner_status="FORMAL_DEFINITION_ONLY",
            why_not_promoted="Gamma_eff is not parent-owned as a live scalar density and current Khat is not shown equal to Kmetric",
            next_repair="make Gamma_eff explicit and compare all Kmetric components",
            source_owner_signed=False,
            preferred_route=False,
        ),
        base_row(
            owner_id="KSO2219_2_tracefree_improvement",
            route="trace-free improvement Hilbert response",
            candidate_formula="K_L^{mu nu}=2 nabla^mu nabla^nu phi - (1/2) g^{mu nu} Box phi, or TF metric response of int sqrt(-g) phi R",
            source_evidence="1287 first component row; 1525 origin audit; 1527 adoption row",
            source_owner_status="BEST_CONCRETE_CANDIDATE_STAGED_NONCLAIM",
            why_not_promoted="phi owner, coefficient, sign, boundary, multiplier silence and live adoption are unsigned",
            next_repair="write a birth-certificate gate for the improvement action and phi equation",
            source_owner_signed=False,
            preferred_route=True,
        ),
        base_row(
            owner_id="KSO2219_3_DT_balance_operator",
            route="D_T range/cokernel balance operator",
            candidate_formula="S_bal=(2 kappa_K)^-1 ||D_T K_hat-G||^2 + S_reg + B",
            source_evidence="830 owner audit; 831 operator/range theorem",
            source_owner_status="MATHEMATICAL_REDUCTION_NOT_PARENT_ADOPTION",
            why_not_promoted="S_bal or equivalent block is not found in MTS parent action and arena response matrices are missing",
            next_repair="parent-sign S_bal or use its cokernel/boundary bound as a residual row",
            source_owner_signed=False,
            preferred_route=False,
        ),
        base_row(
            owner_id="KSO2219_4_response_doublet_normal_form",
            route="response doublet normal-form Hilbert stress",
            candidate_formula="Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4), Khat=metric response of same density",
            source_evidence="756 response-doublet repair; 1664 SFA1664_3; 2217 density candidate",
            source_owner_status="FORMAL_MECHANISM_NOT_LIVE",
            why_not_promoted="Z is not locked to the actual physical q_loc/PPN residual vector and source/boundary rows remain open",
            next_repair="map Z to actual vertical generator and prove source-current/boundary zero",
            source_owner_signed=False,
            preferred_route=False,
        ),
        base_row(
            owner_id="KSO2219_5_defect_potential",
            route="constitutive defect potential",
            candidate_formula="P^{mu nu}=partial V_def/partial Z_{mu nu}; Khat=P+Gamma_eff g",
            source_evidence="223 X constraint algebra and constitutive owner",
            source_owner_status="ELEGANT_CONTRACT_NOT_DERIVED",
            why_not_promoted="V_def, Z_mu_nu, full parent metric M_AB and cross-term policy are missing",
            next_repair="construct V_def from existing coherence-defect blocks or demote",
            source_owner_signed=False,
            preferred_route=False,
        ),
        base_row(
            owner_id="KSO2219_6_scalar_memory_hilbert_stress",
            route="scalar memory sector Hilbert stress",
            candidate_formula="Khat from L_m=-1/2 Z_m(X)(nabla m)^2 - V_R(m,X)",
            source_evidence="827/828 Khat response and owner audits",
            source_owner_status="INSUFFICIENT_BY_ITSELF",
            why_not_promoted="near local equilibrium the stress is gradient/quadratic and cannot cancel arbitrary baseline drift; X_B/L_cg ancestors are open",
            next_repair="derive X_B/L_cg from covariant fields and include bath/source stress in Ward identity",
            source_owner_signed=False,
            preferred_route=False,
        ),
        base_row(
            owner_id="KSO2219_7_residual_branch",
            route="retain Delta_Khat and q_loc as explicit residuals",
            candidate_formula="Delta_Khat_total and q_loc residual vector",
            source_evidence="1010 residual retention; 2218 Delta rows",
            source_owner_status="HONEST_FALLBACK",
            why_not_promoted="this keeps tests honest but does not derive local GR/Newton",
            next_repair="fill finite coefficients, units and arena response operators",
            source_owner_signed=False,
            preferred_route=False,
        ),
        base_row(
            owner_id="KSO2219_8_verdict",
            route="source-owned Khat definition for current MTS",
            candidate_formula="one live tensor owner before readout",
            source_evidence="combined 2219 owner audit",
            source_owner_status="NOT_CLOSED",
            why_not_promoted="best concrete route is trace-free improvement, but it remains staged/nonclaim",
            next_repair="attack KSO2219_2 birth certificate before any GitHub/local-GR promotion",
            source_owner_signed=False,
            preferred_route=False,
        ),
    ]


def component_fill_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            component_id="DKF2219_0_volume",
            residual_symbol="Delta_Khat_vol",
            component_question="does live Khat include the same volume/sign/background term as Kmetric?",
            best_current_source="1366 MATCH1366_0; 2111 KMG2111_0",
            concrete_blocker="overall sign, volume convention and Gamma0/background subtraction are not fixed in a live Khat definition",
            required_next_input="sign convention; volume subtraction rule; source path tying Khat trace convention to Gamma_eff",
            current_status="BLOCKED_WITH_SOURCE_PATH",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            component_id="DKF2219_1_deltaM",
            residual_symbol="Delta_Khat_deltaM",
            component_question="does live Khat contain metric variation of M_AB?",
            best_current_source="2216/2217 parent Hessian and formal variation rows",
            concrete_blocker="M_AB is a candidate Hessian/pseudoinverse object, not a parent-signed function of g with units and domain",
            required_next_input="M_AB(g,R_even,D,...) source formula; dM_AB/dg; pairing units",
            current_status="BLOCKED_WITH_SOURCE_PATH",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            component_id="DKF2219_2_deltaZ",
            residual_symbol="Delta_Khat_deltaZ",
            component_question="does live Khat contain the same metric/coframe response of Z?",
            best_current_source="756 response doublet; 1664 SFA1664_3; 2217 FMV2217_1",
            concrete_blocker="Z is not proven equal to the actual vertical generator/observed residual vector and its metric response is not owned",
            required_next_input="physical Z map; DZ/Dg or coframe response; no-linear-source theorem",
            current_status="BLOCKED_WITH_SOURCE_PATH",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            component_id="DKF2219_3_derivative",
            residual_symbol="Delta_Khat_deriv",
            component_question="are connection/CDB/derivative terms included or zero?",
            best_current_source="2111 KMG2111_4; 1366 MATCH1366_2",
            concrete_blocker="K_conn, CDB, derivative-order and integration-by-parts terms are retained residuals",
            required_next_input="K_conn_norm or zero theorem; derivative order; integration-by-parts convention",
            current_status="BLOCKED_WITH_SOURCE_PATH",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            component_id="DKF2219_4_boundary",
            residual_symbol="Delta_Khat_boundary",
            component_question="are boundary/projector/corner terms exact or finite?",
            best_current_source="513 GK513_5; 830 KO830_1; 831 PA831_3",
            concrete_blocker="boundary no-flux, projector commutator and source-measure descent are not signed",
            required_next_input="boundary primitive; no-flux/corner theorem; P_loc commutator norm",
            current_status="BLOCKED_WITH_SOURCE_PATH",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            component_id="DKF2219_5_units",
            residual_symbol="Delta_Khat_units",
            component_question="can Khat, Gamma_eff and q_loc be put in local test units?",
            best_current_source="515 MA515_6; 2207 KMR2207_4",
            concrete_blocker="stress-density units, q_loc units and arena response normalization are missing",
            required_next_input="unit map for Gamma_eff/Khat/Z/M/q_loc plus PPN/R10/clock/orbital response matrices",
            current_status="BLOCKED_WITH_SOURCE_PATH",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            component_id="DKF2219_6_helmholtz",
            residual_symbol="H_GK",
            component_question="does the proposed Khat stress satisfy Helmholtz integrability?",
            best_current_source="513 GK513_1; 1010 GKT1010_2; 2218 HMG2218_3",
            concrete_blocker="there is no sourced tensor input to run the second-variation symmetry test",
            required_next_input="explicit T_GK tensor and boundary convention; second-variation symmetry calculation",
            current_status="NOT_EVALUABLE_WITH_SOURCE_PATH",
            score_ready=False,
            valid_prediction_row=False,
        ),
        base_row(
            component_id="DKF2219_7_live_tensor_owner",
            residual_symbol="Delta_Khat_total",
            component_question="is there a live source-owned Khat tensor definition?",
            best_current_source="1527 KAD1527_4; 1664 SFA1664_5; 2218 KTC2218_6",
            concrete_blocker="trace-free improvement adoption is staged but not live; no current source-owned Khat tensor matches Kmetric",
            required_next_input="parent action birth certificate or finite residual coefficient envelope",
            current_status="SOURCE_OWNER_NOT_CLOSED",
            score_ready=False,
            valid_prediction_row=False,
        ),
    ]


def nonclaim_component_rows(component_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in component_rows:
        rows.append(
            base_row(
                nonclaim_id=str(row["component_id"]).replace("DKF", "NCR"),
                residual_symbol=row["residual_symbol"],
                source_path_or_anchor=row["best_current_source"],
                coefficient_status="MISSING_NUMERIC_COEFFICIENT_OR_THEOREM_ZERO",
                unit_status="MISSING_UNITS" if row["residual_symbol"] != "H_GK" else "STRUCTURAL_OBSTRUCTION",
                arena_projection_status="MISSING_ARENA_PROJECTION",
                allowable_use="ledger_only_nonclaim",
                forbidden_use="local_GR_Newton_PPN_R10_clock_orbital_WEP_claim",
                score_ready=False,
                valid_prediction_row=False,
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2219_0_source_hunt",
            gate="Khat source-owner hunt completed for current corpus",
            status="PASS_NONCLAIM",
            reason="candidate routes are ranked and tied to source paths.",
        ),
        base_row(
            gate_id="CG2219_1_live_Khat_owner",
            gate="live Khat tensor owner found",
            status="BLOCKED_NONCLAIM",
            reason="no route is parent-signed; best trace-free improvement route is staged only.",
        ),
        base_row(
            gate_id="CG2219_2_Delta_fill",
            gate="Delta_Khat component rows filled with concrete blockers",
            status="PASS_NONCLAIM",
            reason="generic missing rows are replaced by source-anchored component blockers.",
        ),
        base_row(
            gate_id="CG2219_3_Helmholtz",
            gate="Helmholtz integrability can be evaluated",
            status="BLOCKED_NONCLAIM",
            reason="explicit sourced stress tensor and boundary convention are still absent.",
        ),
        base_row(
            gate_id="CG2219_4_local_GR_Newton",
            gate="local GR/Newton reduction claim",
            status="BLOCKED_NONCLAIM",
            reason="Khat source owner, units, boundary/projector and matter descent are open.",
        ),
        base_row(
            gate_id="CG2219_5_GitHub",
            gate="public/GitHub update",
            status="BLOCKED_NONCLAIM",
            reason="private derivation branch remains mid-gate.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2219_0_no_live_owner",
            decision="NO_LIVE_KHAT_SOURCE_OWNER",
            rationale="all live-symbol searches fail; all successful-looking objects are contracts, candidates or staged adoption rows.",
            next_action="do not publish/local-claim this branch yet.",
        ),
        base_row(
            decision_id="DEC2219_1_best_route",
            decision="TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE_IS_BEST_NEXT_SHOT",
            rationale="it has an explicit tensor shape, source path history, and a concrete adoption row; it is less arbitrary than a new free Khat tensor.",
            next_action="attempt parent-signing of the improvement action, phi owner, coefficient and boundary clauses.",
        ),
        base_row(
            decision_id="DEC2219_2_residuals",
            decision="DELTA_KHAT_ROWS_ARE_NOW_COMPONENT_ANCHORED",
            rationale="Delta_Khat is no longer one foggy blocker; every component has a named source trail and missing input.",
            next_action="if birth certificate fails, turn the same rows into finite coefficient envelopes.",
        ),
        base_row(
            decision_id="DEC2219_3_claim_status",
            decision="LOCAL_GR_REMAINS_BLOCKED_NOT_DEAD",
            rationale="the route has a precise throat: sign Khat owner or bound its components; nothing was disproved, but nothing can be claimed.",
            next_action="run 2220 before returning to empirical local tests or GitHub.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2219_0_2220",
            selection_status="selected",
            target_file="2220-Y5-R2FR-tracefree-improvement-Khat-birth-certificate-or-DeltaKhat-coefficient-runner.md",
            target_script="scripts/Y5_R2FR_tracefree_improvement_Khat_birth_certificate_or_DeltaKhat_coefficient_runner_2220.py",
            objective="try to parent-sign the staged trace-free improvement Khat route: action term, phi owner/equation, coefficient/sign, boundary and multiplier-silence clauses; if it fails, emit first finite Delta_Khat coefficient-envelope rows.",
            success_condition="either KSO2219_2 receives a source-owned birth certificate, or every failed clause becomes a concrete coefficient/bound input row.",
            do_not_do="do not promote K_L as live Khat by notation; do not claim local GR/Newton; do not use GitHub.",
        ),
        base_row(
            route_id="NEXT2219_1_units_parallel",
            selection_status="held_parallel",
            target_file="2220b-Y5-R2FR-Gamma-Khat-q-loc-units-and-arena-response-map.md",
            target_script="scripts/Y5_R2FR_Gamma_Khat_qloc_units_and_arena_response_map_2220b.py",
            objective="normalize units for Gamma_eff, Khat, q_loc, Delta_Khat and arena response operators.",
            success_condition="symbolic residuals become dimensionally checkable nonclaim rows.",
            do_not_do="do not score local tests from placeholder units.",
        ),
        base_row(
            route_id="NEXT2219_2_boundary_parallel",
            selection_status="held_parallel",
            target_file="2220c-Y5-R2FR-Khat-boundary-projector-commutator-zero-or-bound.md",
            target_script="scripts/Y5_R2FR_Khat_boundary_projector_commutator_zero_or_bound_2220c.py",
            objective="attack the boundary/projector/domain part of Delta_Khat directly.",
            success_condition="no-flux/commutator theorem or finite edge/source-measure rows.",
            do_not_do="do not bury boundary terms in the bulk tensor definition.",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["component_fill"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["component_fill"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["owner_audit"], BRANCH_COPIES["beta_docs"]),
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
    owner_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    nonclaim_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add(
        "VAL2219_00_sources_exist",
        all(truthy(row.get("path_exists")) for row in source_rows),
        f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist",
    )
    add(
        "VAL2219_01_needles_found",
        all(truthy(row.get("needles_found")) for row in source_rows),
        f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found",
    )

    birth_ok = len(birth_rows) == 8 and any(row.get("certificate_id") == "KBC2219_7_verdict" for row in birth_rows)
    birth_ok = birth_ok and all(not truthy(row.get("certificate_pass")) for row in birth_rows)
    add("VAL2219_02_birth_certificate_gate", birth_ok, "Khat birth certificate is explicit and not falsely closed")

    owner_ok = len(owner_rows) == 9
    owner_ok = owner_ok and any(row.get("owner_id") == "KSO2219_2_tracefree_improvement" and truthy(row.get("preferred_route")) for row in owner_rows)
    owner_ok = owner_ok and any(row.get("owner_id") == "KSO2219_8_verdict" and row.get("source_owner_status") == "NOT_CLOSED" for row in owner_rows)
    owner_ok = owner_ok and all(not truthy(row.get("source_owner_signed")) for row in owner_rows)
    add("VAL2219_03_owner_audit", owner_ok, "owner audit ranks trace-free improvement but signs no live owner")

    component_ok = len(component_rows) == 8
    component_ok = component_ok and all("MISSING_SOURCE_BACKED_COMPONENT" not in str(row.get("concrete_blocker")) for row in component_rows)
    component_ok = component_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in component_rows)
    add("VAL2219_04_delta_component_fill", component_ok, "Delta_Khat rows have source-anchored blockers and remain non-score-ready")

    nonclaim_ok = len(nonclaim_rows_) == len(component_rows)
    nonclaim_ok = nonclaim_ok and all(row.get("allowable_use") == "ledger_only_nonclaim" for row in nonclaim_rows_)
    nonclaim_ok = nonclaim_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in nonclaim_rows_)
    add("VAL2219_05_nonclaim_rows", nonclaim_ok, "nonclaim component rows forbid arena/local promotion")

    claim_ok = any(row.get("gate_id") == "CG2219_1_live_Khat_owner" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2219_4_local_GR_Newton" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2219_06_claim_gate", claim_ok, "Khat owner and local-GR/Newton claims remain blocked")

    decision_ok = any(row.get("decision") == "TRACEFREE_IMPROVEMENT_BIRTH_CERTIFICATE_IS_BEST_NEXT_SHOT" for row in decision_rows_)
    add("VAL2219_07_decision", decision_ok, "decision ledger selects trace-free improvement birth certificate next")

    next_ok = any(row.get("route_id") == "NEXT2219_0_2220" and "tracefree-improvement" in str(row.get("target_file")) for row in next_rows)
    add("VAL2219_08_next_target", next_ok, "2220 trace-free improvement Khat birth certificate selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2219_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2219_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, birth_rows, owner_rows, component_rows, nonclaim_rows_, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2219_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    no_live_promotion = all(not truthy(row.get("source_owner_signed")) for row in owner_rows)
    no_live_promotion = no_live_promotion and all(not truthy(row.get("certificate_pass")) for row in birth_rows)
    add("VAL2219_12_no_live_promotion", no_live_promotion, "no owner/birth-certificate row is promoted")

    formalization_clean = not formalization_has_2219_artifacts()
    add("VAL2219_13_formalization_clean", formalization_clean, "formalization-workbench has no 2219 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2219_14_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2219_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2219 finds no live source-owned Khat tensor, ranks trace-free improvement as the best concrete next route, fills Delta_Khat components with source-anchored blockers, keeps all local claims blocked, and selects 2220 birth-certificate work",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    birth_rows: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    nonclaim_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2219 - Y5/R2FR Khat Source Definition Owner Or DeltaKhat Component Fill",
        "",
        "## Current Verdict",
        "",
        "2219 does not find a live source-owned `K_hat` tensor in the current corpus. That keeps the local-GR/Newton reduction blocked.",
        "",
        "But the result is sharper than 2218: the best concrete route is now identified as the trace-free improvement / Hilbert-response candidate already staged in the 1287/1525/1527 trail. It has a real tensor shape, but it is not live until the parent action term, `phi` owner, coefficient/sign, boundary, multiplier-silence, units, and matter-descent clauses are source-signed.",
        "",
        "So the next clean move is not another broad Khat hunt. It is a birth-certificate attempt for that trace-free improvement route. If the certificate fails, the same rows become finite `Delta_Khat` coefficient envelopes.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Khat Birth Certificate Gate",
        "",
        md_table(birth_rows, ["certificate_id", "required_clause", "pass_condition", "best_current_evidence", "current_status", "blocker", "certificate_pass", "valid_for_claim"]),
        "",
        "## Khat Source Owner Audit",
        "",
        md_table(owner_rows, ["owner_id", "route", "candidate_formula", "source_evidence", "source_owner_status", "why_not_promoted", "next_repair", "source_owner_signed", "preferred_route", "valid_for_claim"]),
        "",
        "## Delta Khat Component Fill",
        "",
        md_table(component_rows, ["component_id", "residual_symbol", "component_question", "best_current_source", "concrete_blocker", "required_next_input", "current_status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Nonclaim Component Rows",
        "",
        md_table(nonclaim_rows_, ["nonclaim_id", "residual_symbol", "source_path_or_anchor", "coefficient_status", "unit_status", "arena_projection_status", "allowable_use", "forbidden_use", "score_ready", "valid_prediction_row", "valid_for_claim"]),
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
        "This is not a loop. It is the bottleneck narrowing properly. The theory now has one least-handwavy `K_hat` route to attack: the trace-free improvement response. If that birth certificate can be signed, the local GR branch gets much more serious. If it cannot, `Delta_Khat` becomes a measured/bounded residual rather than a hidden cancellation.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    birth_rows = birth_certificate_rows()
    owner_rows = owner_audit_rows()
    component_rows = component_fill_rows()
    nonclaim_rows_ = nonclaim_component_rows(component_rows)
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["birth_certificate"], birth_rows),
        (OUTPUTS["owner_audit"], owner_rows),
        (OUTPUTS["component_fill"], component_rows),
        (OUTPUTS["nonclaim_rows"], nonclaim_rows_),
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
        owner_rows,
        component_rows,
        nonclaim_rows_,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        birth_rows,
        owner_rows,
        component_rows,
        nonclaim_rows_,
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
