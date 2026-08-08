from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2218"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2218-Y5-R2FR-Kmetric-vs-Khat-tensor-comparison-and-Helmholtz-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2218_SOURCE_REGISTER.csv",
    "kmetric_components": OUT / "P8_Y5_PARENT_QLOC_2218_KMETRIC_COMPONENT_TABLE.csv",
    "khat_appearances": OUT / "P8_Y5_PARENT_QLOC_2218_KHAT_SOURCE_APPEARANCE_TABLE.csv",
    "tensor_comparison": OUT / "P8_Y5_PARENT_QLOC_2218_KMETRIC_KHAT_TENSOR_COMPARISON.csv",
    "helmholtz_gate": OUT / "P8_Y5_PARENT_QLOC_2218_HELMHOLTZ_GATE.csv",
    "delta_acquisition": OUT / "P8_Y5_PARENT_QLOC_2218_DELTA_KHAT_ACQUISITION_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2218_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2218_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2218_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2218_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2218_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2218_DELTA_KHAT_COMPONENT_ACQUISITION_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2218_KMETRIC_KHAT_COMPARISON_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_KMETRIC_COMPONENTS_2218_NONCLAIM.csv",
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


def formalization_has_2218_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2218-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2218*",
        "*P8_Y5_BRR545_2218*",
        "*Y5_R2FR_Kmetric_vs_Khat_tensor_comparison_and_Helmholtz_gate_2218*",
        "*JR2218*",
        "*PARENT_QLOC_KMETRIC_COMPONENTS_2218*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2217_handoff",
            ROOT / "2217-Y5-R2FR-response-doublet-parent-density-and-Khat-identity-construction.md",
            ["NEXT2217_0_2218", "DK2217_1_Khat_tensor_gap", "VAL2217_OVERALL"],
            "2217 selects term-by-term Kmetric/Khat comparison and Helmholtz gate.",
        ),
        (
            "2217_delta_rows",
            OUT / "P8_Y5_PARENT_QLOC_2217_KHAT_MISMATCH_RESIDUAL_ROWS.csv",
            ["DK2217_1_Khat_tensor_gap", "DK2217_4_Helmholtz_gap", "DK2217_6_verdict"],
            "machine-readable Delta_Khat residual rows.",
        ),
        (
            "1010_action_guard",
            ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            ["GKT1010_1_metric_response_identity", "GKT1010_2_Helmholtz_integrability", "V1010_SUMMARY"],
            "Gamma/Khat metric-response and Helmholtz guardrail.",
        ),
        (
            "2207_variation",
            ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["GMV2207_0_response_doublet_setup", "KMR2207_2_Khat_identity", "VAL2207_OVERALL"],
            "formal response-doublet metric variation and blocked Khat match.",
        ),
        (
            "metric_audit",
            OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            ["MA515_1_Khat_metric_response", "MA515_5_boundary_terms", "MA515_6_units_and_readout"],
            "Khat response, boundary and unit gaps.",
        ),
        (
            "metric_contract",
            OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            ["MR514_1_Khat_metric_response", "MR514_2_Ward_identity", "MR514_5_double_zero"],
            "metric-response pass conditions.",
        ),
        (
            "metric_pass_fail",
            OUT / "P8_GK_METRIC_RESPONSE_PASS_FAIL.csv",
            ["PF515_2_Khat_response_found", "PF515_3_response_template_found", "PF515_5_residual_branch"],
            "pass/fail ledger for Khat response source search.",
        ),
        (
            "first_variation_contract",
            OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
            ["GK513_1_integrability", "GK513_3_double_zero", "GK513_5_boundary_no_flux"],
            "Helmholtz/integrability, double-zero and boundary clauses.",
        ),
        (
            "gamma_owner_candidates",
            OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner", "best_candidate_not_current_MTS_derived"],
            "candidate response-doublet density and fallback residual branch.",
        ),
        (
            "response_variation",
            OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            ["AV517_1_scalar_density", "AV517_2_first_variation_Z", "AV517_4_Euler_equation"],
            "formal response-doublet variation and source-current blocker.",
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


def kmetric_component_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            component_id="KMC2218_0_volume",
            kmetric_component="volume/sign convention term",
            formal_expression="K_vol^{mu nu} = convention-dependent Gamma_eff g^{mu nu} term after varying sqrt(-g)",
            required_for_match="declared sign and volume subtraction convention",
            source_status="FORMAL_COMPONENT_ONLY",
            unresolved="Gamma0/background subtraction and stress-density sign not source-normalized",
            match_ready=False,
        ),
        base_row(
            component_id="KMC2218_1_deltaM",
            kmetric_component="metric variation of M_AB",
            formal_expression="K_deltaM^{mu nu} = 1/2 (delta M_AB / delta g_{mu nu}) Z^A Z^B",
            required_for_match="source-backed formula for M_AB(g,R_even,D,...) and its metric dependence",
            source_status="MISSING_MAB_METRIC_DEPENDENCE",
            unresolved="no parent M_AB function or units",
            match_ready=False,
        ),
        base_row(
            component_id="KMC2218_2_deltaZ",
            kmetric_component="metric variation of Z basis",
            formal_expression="K_deltaZ^{mu nu} = M_AB Z^A delta_g Z^B plus symmetric partner under field-space pairing",
            required_for_match="whether Z^A depends on metric/coframe/readout variables",
            source_status="MISSING_Z_BASIS_METRIC_RESPONSE",
            unresolved="Z basis and physical component map not parent-signed",
            match_ready=False,
        ),
        base_row(
            component_id="KMC2218_3_derivative",
            kmetric_component="derivative/principal-symbol terms",
            formal_expression="K_deriv^{mu nu} from any nabla Z, nabla R_even, connection, domain or CDB dependence in Gamma_eff",
            required_for_match="derivative order and integration-by-parts convention",
            source_status="LIVE_CDB_DOMAIN_BLOCKER",
            unresolved="CDB/domain/connection pieces not extracted",
            match_ready=False,
        ),
        base_row(
            component_id="KMC2218_4_boundary",
            kmetric_component="boundary/symplectic/projector terms",
            formal_expression="K_boundary^{mu nu} from boundary primitive, corners, P_loc, source worldtubes and support variation",
            required_for_match="proper/no-flux theorem or finite boundary coefficient rows",
            source_status="BOUNDARY_PROJECTOR_OPEN",
            unresolved="boundary terms can feed q_loc even if bulk terms match",
            match_ready=False,
        ),
        base_row(
            component_id="KMC2218_5_units",
            kmetric_component="units and pairing",
            formal_expression="K_metric^{mu nu} must have same stress-density units as K_hat and q_loc divergence",
            required_for_match="Gamma_eff units, Z/M units, source pairing and readout normalization",
            source_status="MISSING_UNITS",
            unresolved="no local test can be scored",
            match_ready=False,
        ),
        base_row(
            component_id="KMC2218_6_verdict",
            kmetric_component="full formal K_metric tensor",
            formal_expression="K_metric = K_vol + K_deltaM + K_deltaZ + K_deriv + K_boundary",
            required_for_match="each component must be matched or retained in Delta_Khat",
            source_status="COMPONENTS_STAGED_NOT_MATCHED",
            unresolved="no component currently source-signed equal to K_hat",
            match_ready=False,
        ),
    ]


def khat_appearance_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            appearance_id="KSA2218_0_symbol_route",
            source="01/02 early route symbols",
            khat_role="framework symbol",
            evidence_summary="Gamma_eff, K_hat and q_loc appear as local-GR route targets.",
            tensor_definition_status="NO_TENSOR_DEFINITION",
            usable_for_match=False,
        ),
        base_row(
            appearance_id="KSA2218_1_q_loc_identity",
            source="compact-shell/q_loc identity and 1010 residual row",
            khat_role="q_loc divergence term",
            evidence_summary="q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}).",
            tensor_definition_status="IDENTITY_SLOT_ONLY",
            usable_for_match=False,
        ),
        base_row(
            appearance_id="KSA2218_2_metric_response_contract",
            source="P8_GK_METRIC_RESPONSE_CONTRACT.csv",
            khat_role="required target",
            evidence_summary="contract requires K_hat to equal K_metric including derivative/boundary terms.",
            tensor_definition_status="PASS_CONDITION_NOT_SOURCE",
            usable_for_match=False,
        ),
        base_row(
            appearance_id="KSA2218_3_metric_response_audit",
            source="P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            khat_role="failed source search",
            evidence_summary="no derivation as delta[sqrt(-g)Gamma_eff]/delta g was found.",
            tensor_definition_status="FAIL_CURRENT_CLAIM",
            usable_for_match=False,
        ),
        base_row(
            appearance_id="KSA2218_4_response_template",
            source="P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv + source-current audit",
            khat_role="conditional conjugate response template",
            evidence_summary="possible parent response identity exists, but not a tensor equality.",
            tensor_definition_status="PROMISING_TEMPLATE_ONLY",
            usable_for_match=False,
        ),
        base_row(
            appearance_id="KSA2218_5_2207_formal_variation",
            source="2207 formal metric variation",
            khat_role="formal comparison target",
            evidence_summary="response-doublet K_metric is written, current K_hat identity remains blocked.",
            tensor_definition_status="FORMAL_KMETRIC_NOT_EXISTING_KHAT",
            usable_for_match=False,
        ),
        base_row(
            appearance_id="KSA2218_6_verdict",
            source="combined 2218 appearance scan",
            khat_role="no sourced tensor definition found",
            evidence_summary="all useful Khat appearances are targets, identities, residual slots or conditional templates.",
            tensor_definition_status="NO_COMPONENT_MATCH_AVAILABLE",
            usable_for_match=False,
        ),
    ]


def tensor_comparison_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            comparison_id="KTC2218_0_volume",
            kmetric_component="K_vol",
            khat_component_source="none source-signed",
            comparison_result="NO_MATCH_SOURCE",
            reason="Khat volume/sign convention is not defined.",
            delta_component="Delta_Khat_vol",
            source_signed_match=False,
        ),
        base_row(
            comparison_id="KTC2218_1_deltaM",
            kmetric_component="K_deltaM",
            khat_component_source="none source-signed",
            comparison_result="NO_MATCH_SOURCE",
            reason="M_AB(g,...) and existing Khat delta-M structure are not sourced.",
            delta_component="Delta_Khat_deltaM",
            source_signed_match=False,
        ),
        base_row(
            comparison_id="KTC2218_2_deltaZ",
            kmetric_component="K_deltaZ",
            khat_component_source="none source-signed",
            comparison_result="NO_MATCH_SOURCE",
            reason="Z basis metric response and physical component map are missing.",
            delta_component="Delta_Khat_deltaZ",
            source_signed_match=False,
        ),
        base_row(
            comparison_id="KTC2218_3_derivative",
            kmetric_component="K_deriv",
            khat_component_source="CDB/K_conn/K_domain open ledgers only",
            comparison_result="LIVE_UNEXTRACTED_NOT_MATCH",
            reason="connection/domain/CDB derivative order not extracted.",
            delta_component="Delta_Khat_deriv",
            source_signed_match=False,
        ),
        base_row(
            comparison_id="KTC2218_4_boundary",
            kmetric_component="K_boundary",
            khat_component_source="boundary/projector open ledgers only",
            comparison_result="LIVE_UNEXTRACTED_NOT_MATCH",
            reason="boundary no-flux and projector commutator terms are not signed.",
            delta_component="Delta_Khat_boundary",
            source_signed_match=False,
        ),
        base_row(
            comparison_id="KTC2218_5_units",
            kmetric_component="units/readout",
            khat_component_source="none source-signed",
            comparison_result="NO_MATCH_SOURCE",
            reason="stress-density and q_loc/readout units are missing.",
            delta_component="Delta_Khat_units",
            source_signed_match=False,
        ),
        base_row(
            comparison_id="KTC2218_6_verdict",
            kmetric_component="full tensor",
            khat_component_source="combined corpus scan",
            comparison_result="NO_COMPONENT_SOURCE_SIGNED",
            reason="no Kmetric component can be identified with a sourced Khat tensor component.",
            delta_component="Delta_Khat_total",
            source_signed_match=False,
        ),
    ]


def helmholtz_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_row_id="HMG2218_0_required_condition",
            helmholtz_clause="variational stress integrability",
            mathematical_test="delta(sqrt(-g)T_GK^{mu nu})/delta g_{alpha beta} symmetric under exchange of metric variations up to boundary terms",
            current_status="NOT_CHECKED_CURRENT_CORPUS",
            implication_if_fail="no action exists for proposed Khat stress even if term shapes look similar",
            next_action="requires explicit T_GK tensor components first",
            helmholtz_pass=False,
        ),
        base_row(
            gate_row_id="HMG2218_1_input_gap",
            helmholtz_clause="input tensor missing",
            mathematical_test="T_GK^{mu nu}=Gamma_eff g^{mu nu}-K_hat^{mu nu} with sourced Khat components",
            current_status="KHAT_COMPONENTS_MISSING",
            implication_if_fail="Helmholtz cannot be evaluated, only retained as obstruction",
            next_action="source Khat components or keep Delta_Khat/H_GK rows",
            helmholtz_pass=False,
        ),
        base_row(
            gate_row_id="HMG2218_2_boundary_symmetry",
            helmholtz_clause="boundary symmetry",
            mathematical_test="boundary terms from two metric variations commute or are exact/proper",
            current_status="BOUNDARY_OPEN",
            implication_if_fail="boundary can obstruct action existence and local no-force claim",
            next_action="derive boundary primitive or finite edge coefficients",
            helmholtz_pass=False,
        ),
        base_row(
            gate_row_id="HMG2218_3_verdict",
            helmholtz_clause="2218 Helmholtz verdict",
            mathematical_test="full Helmholtz test requires sourced tensor components and boundary convention",
            current_status="HELMHOLTZ_NOT_EVALUABLE_YET",
            implication_if_fail="H_GK remains official obstruction",
            next_action="2219 source Khat definition or Delta_Khat/H_GK component rows",
            helmholtz_pass=False,
        ),
    ]


def delta_acquisition_rows() -> list[dict[str, Any]]:
    specs = [
        ("DKA2218_0_volume", "Delta_Khat_vol", "volume/sign convention mismatch", "Gamma_eff sign, volume subtraction, Khat trace convention"),
        ("DKA2218_1_deltaM", "Delta_Khat_deltaM", "metric variation of M_AB mismatch", "source-backed M_AB(g,...) and Khat M-response term"),
        ("DKA2218_2_deltaZ", "Delta_Khat_deltaZ", "metric variation of Z mismatch", "Z basis/coframe/readout dependence and Khat Z-response term"),
        ("DKA2218_3_derivative", "Delta_Khat_deriv", "derivative/CDB mismatch", "K_conn/K_domain/CDB derivative order and Khat derivative term"),
        ("DKA2218_4_boundary", "Delta_Khat_boundary", "boundary/projector mismatch", "boundary primitive, P_loc commutator and Khat edge term"),
        ("DKA2218_5_units", "Delta_Khat_units", "units/readout mismatch", "stress-density units and q_loc/readout normalization"),
        ("DKA2218_6_Helmholtz", "H_GK", "Helmholtz integrability obstruction", "second metric variation symmetry and boundary symmetry"),
        ("DKA2218_7_total", "Delta_Khat_total", "all unmatched Khat identity pieces", "source-backed component table or finite residual coefficients"),
    ]
    rows: list[dict[str, Any]] = []
    for acquisition_id, residual_symbol, residual_channel, required_source in specs:
        rows.append(
            base_row(
                acquisition_id=acquisition_id,
                residual_symbol=residual_symbol,
                residual_channel=residual_channel,
                required_source=required_source,
                current_value="MISSING_SOURCE_BACKED_COMPONENT",
                current_units="MISSING_UNITS",
                status="NONCLAIM_ACQUISITION_ROW",
                score_ready=False,
                valid_prediction_row=False,
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2218_0_Kmetric_components",
            gate="K_metric component table written",
            status="PASS_NONCLAIM",
            reason="formal components are now separated into volume, deltaM, deltaZ, derivative, boundary and units.",
        ),
        base_row(
            gate_id="CG2218_1_Khat_component_match",
            gate="at least one Khat component source-signed",
            status="BLOCKED_NONCLAIM",
            reason="all Khat appearances are identity slots, contracts, templates or failed source searches.",
        ),
        base_row(
            gate_id="CG2218_2_Helmholtz",
            gate="Helmholtz integrability evaluable/pass",
            status="BLOCKED_NONCLAIM",
            reason="sourced Khat tensor components and boundary convention are missing.",
        ),
        base_row(
            gate_id="CG2218_3_Delta_Khat",
            gate="Delta_Khat residual rows staged",
            status="PASS_NONCLAIM",
            reason="each unmatched component has a nonclaim acquisition row.",
        ),
        base_row(
            gate_id="CG2218_4_local_GR_Newton",
            gate="local GR/Newton reduction claim",
            status="BLOCKED_NONCLAIM",
            reason="Khat identity, Helmholtz, source/boundary and units remain open.",
        ),
        base_row(
            gate_id="CG2218_5_GitHub",
            gate="GitHub/public update",
            status="BLOCKED_NONCLAIM",
            reason="private derivation checkpoint only.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2218_0_gain",
            decision="KMETRIC_COMPONENTS_SEPARATED",
            rationale="the comparison is no longer one opaque Khat identity; it is a component checklist.",
            next_action="use component rows as the only legal path to Khat promotion.",
        ),
        base_row(
            decision_id="DEC2218_1_failure",
            decision="NO_KHAT_COMPONENT_SOURCE_SIGNED",
            rationale="the corpus contains Khat targets and identities, but no tensor definition matched to Kmetric components.",
            next_action="retain Delta_Khat component residuals.",
        ),
        base_row(
            decision_id="DEC2218_2_helmholtz",
            decision="HELMHOLTZ_NOT_EVALUABLE_YET",
            rationale="integrability needs a sourced stress tensor and boundary convention first.",
            next_action="keep H_GK as obstruction until tensor components exist.",
        ),
        base_row(
            decision_id="DEC2218_3_next",
            decision="KHAT_SOURCE_DEFINITION_OR_DELTA_COMPONENT_FILL_NEXT",
            rationale="the next non-circular move is to find/define Khat component sources or fill Delta_Khat rows.",
            next_action="2219 should attempt Khat source-definition owner before any local test.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2218_0_2219",
            selection_status="selected",
            target_file="2219-Y5-R2FR-Khat-source-definition-owner-or-DeltaKhat-component-fill.md",
            target_script="scripts/Y5_R2FR_Khat_source_definition_owner_or_DeltaKhat_component_fill_2219.py",
            objective="hunt for a source-owned Khat tensor definition component-by-component; if not found, fill Delta_Khat_vol/deltaM/deltaZ/deriv/boundary/units/H_GK acquisition rows with explicit source paths and units.",
            success_condition="one Khat component becomes source-signed against Kmetric, or every Delta_Khat component row has a concrete source/owner blocker.",
            do_not_do="do not assume Khat identity by notation, do not claim local GR/Newton, do not use GitHub.",
        ),
        base_row(
            route_id="NEXT2218_1_units_parallel",
            selection_status="held_parallel",
            target_file="2218b-Y5-R2FR-Gamma-Khat-Z-M-units-and-pairing-normalization.md",
            target_script="scripts/Y5_R2FR_Gamma_Khat_Z_M_units_and_pairing_normalization_2218b.py",
            objective="derive units and pairing for Gamma_eff, K_hat, Z, M_AB, source S_A and q_loc.",
            success_condition="unit-normalized rows can be checked dimensionally or remain explicit blockers.",
            do_not_do="do not compute scores from dimensionless placeholders.",
        ),
        base_row(
            route_id="NEXT2218_2_boundary_parallel",
            selection_status="held_parallel",
            target_file="2219b-Y5-R2FR-Kmetric-boundary-primitive-or-edge-residual-row.md",
            target_script="scripts/Y5_R2FR_Kmetric_boundary_primitive_or_edge_residual_row_2219b.py",
            objective="derive the boundary/symplectic/projector primitive for Kmetric-Khat or emit edge residual coefficients.",
            success_condition="boundary term is exact/proper/no-flux or finite coefficient rows exist.",
            do_not_do="do not hide boundary terms inside bulk Khat identity.",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["delta_acquisition"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["tensor_comparison"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["kmetric_components"], BRANCH_COPIES["beta_docs"]),
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
    kmetric_rows: list[dict[str, Any]],
    khat_rows: list[dict[str, Any]],
    comparison_rows: list[dict[str, Any]],
    helmholtz_rows: list[dict[str, Any]],
    acquisition_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2218_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2218_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    kmetric_ok = len(kmetric_rows) == 7 and any(row.get("component_id") == "KMC2218_6_verdict" for row in kmetric_rows)
    kmetric_ok = kmetric_ok and all(not truthy(row.get("match_ready")) for row in kmetric_rows)
    add("VAL2218_02_kmetric_components", kmetric_ok, "Kmetric components are separated and not falsely marked match-ready")

    khat_ok = len(khat_rows) == 7 and any(row.get("appearance_id") == "KSA2218_6_verdict" and row.get("tensor_definition_status") == "NO_COMPONENT_MATCH_AVAILABLE" for row in khat_rows)
    khat_ok = khat_ok and all(not truthy(row.get("usable_for_match")) for row in khat_rows)
    add("VAL2218_03_khat_appearances", khat_ok, "Khat appearances scanned; no sourced tensor component found")

    comparison_ok = any(row.get("comparison_id") == "KTC2218_6_verdict" and row.get("comparison_result") == "NO_COMPONENT_SOURCE_SIGNED" for row in comparison_rows)
    comparison_ok = comparison_ok and all(not truthy(row.get("source_signed_match")) for row in comparison_rows)
    add("VAL2218_04_tensor_comparison", comparison_ok, "no Kmetric/Khat component match promoted")

    helmholtz_ok = any(row.get("gate_row_id") == "HMG2218_3_verdict" and row.get("current_status") == "HELMHOLTZ_NOT_EVALUABLE_YET" for row in helmholtz_rows)
    helmholtz_ok = helmholtz_ok and all(not truthy(row.get("helmholtz_pass")) for row in helmholtz_rows)
    add("VAL2218_05_helmholtz_gate", helmholtz_ok, "Helmholtz gate remains not evaluable without sourced tensor")

    acquisition_ok = len(acquisition_rows) == 8
    acquisition_ok = acquisition_ok and all(row.get("current_value") == "MISSING_SOURCE_BACKED_COMPONENT" for row in acquisition_rows)
    acquisition_ok = acquisition_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in acquisition_rows)
    add("VAL2218_06_delta_acquisition", acquisition_ok, "Delta_Khat component acquisition rows are explicit and nonclaim")

    claim_ok = any(row.get("gate_id") == "CG2218_1_Khat_component_match" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2218_4_local_GR_Newton" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2218_07_claim_gate", claim_ok, "Khat component and local-GR/Newton claims remain blocked")

    decision_ok = any(row.get("decision") == "KHAT_SOURCE_DEFINITION_OR_DELTA_COMPONENT_FILL_NEXT" for row in decision_rows_)
    add("VAL2218_08_decision", decision_ok, "decision ledger selects Khat source-definition or Delta fill next")

    next_ok = any(row.get("route_id") == "NEXT2218_0_2219" and "Khat" in str(row.get("target_file")) for row in next_rows)
    add("VAL2218_09_next_target", next_ok, "2219 Khat source-definition/DeltaKhat fill selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2218_10_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2218_11_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, kmetric_rows, khat_rows, comparison_rows, helmholtz_rows, acquisition_rows, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2218_12_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    no_missing_promoted = all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in acquisition_rows)
    add("VAL2218_13_missing_not_promoted", no_missing_promoted, "Delta_Khat missing components are not promoted to score-ready")

    formalization_clean = not formalization_has_2218_artifacts()
    add("VAL2218_14_formalization_clean", formalization_clean, "formalization-workbench has no 2218 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2218_15_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2218_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2218 separates Kmetric components, scans Khat appearances, finds no source-signed tensor match, keeps Helmholtz not evaluable, and selects Khat source-definition or DeltaKhat component fill next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    kmetric_rows: list[dict[str, Any]],
    khat_rows: list[dict[str, Any]],
    comparison_rows: list[dict[str, Any]],
    helmholtz_rows: list[dict[str, Any]],
    acquisition_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2218 - Y5/R2FR Kmetric Vs Khat Tensor Comparison And Helmholtz Gate",
        "",
        "## Current Verdict",
        "",
        "2218 turns the `K_hat = K_metric` question into a component table. The formal candidate tensor splits as:",
        "",
        "`K_metric = K_vol + K_deltaM + K_deltaZ + K_deriv + K_boundary`.",
        "",
        "The corpus contains many `Khat/K_hat` appearances, but they are route symbols, q_loc identity slots, pass-condition contracts, conditional templates, or failed source searches. No sourced tensor component currently matches any `K_metric` component.",
        "",
        "So `Delta_Khat_total` remains active, and Helmholtz integrability is not evaluable yet because the sourced stress tensor is missing.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Kmetric Component Table",
        "",
        md_table(kmetric_rows, ["component_id", "kmetric_component", "formal_expression", "required_for_match", "source_status", "unresolved", "match_ready", "valid_for_claim"]),
        "",
        "## Khat Source Appearance Table",
        "",
        md_table(khat_rows, ["appearance_id", "source", "khat_role", "evidence_summary", "tensor_definition_status", "usable_for_match", "valid_for_claim"]),
        "",
        "## Kmetric / Khat Tensor Comparison",
        "",
        md_table(comparison_rows, ["comparison_id", "kmetric_component", "khat_component_source", "comparison_result", "reason", "delta_component", "source_signed_match", "valid_for_claim"]),
        "",
        "## Helmholtz Gate",
        "",
        md_table(helmholtz_rows, ["gate_row_id", "helmholtz_clause", "mathematical_test", "current_status", "implication_if_fail", "next_action", "helmholtz_pass", "valid_for_claim"]),
        "",
        "## Delta Khat Acquisition Rows",
        "",
        md_table(acquisition_rows, ["acquisition_id", "residual_symbol", "residual_channel", "required_source", "current_value", "current_units", "status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
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
        "This is a proper hard stop, not a defeat. The route now says exactly what must be found: an actual `K_hat` tensor definition, component by component. Until then the theory does not get to borrow the parent action. The honest next punch is 2219: source `K_hat`, or fill `Delta_Khat` components as residuals.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    kmetric_rows = kmetric_component_rows()
    khat_rows = khat_appearance_rows()
    comparison_rows = tensor_comparison_rows()
    helmholtz_rows = helmholtz_gate_rows()
    acquisition_rows = delta_acquisition_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["kmetric_components"], kmetric_rows),
        (OUTPUTS["khat_appearances"], khat_rows),
        (OUTPUTS["tensor_comparison"], comparison_rows),
        (OUTPUTS["helmholtz_gate"], helmholtz_rows),
        (OUTPUTS["delta_acquisition"], acquisition_rows),
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
        kmetric_rows,
        khat_rows,
        comparison_rows,
        helmholtz_rows,
        acquisition_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        kmetric_rows,
        khat_rows,
        comparison_rows,
        helmholtz_rows,
        acquisition_rows,
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
