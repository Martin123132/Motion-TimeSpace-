from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2208"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2208_SOURCE_REGISTER.csv",
    "ppn_lowering": OUT / "P8_Y5_PARENT_QLOC_2208_PPN_GREEN_OPERATOR_LOWERING.csv",
    "ppn_blocker": OUT / "P8_Y5_PARENT_QLOC_2208_PPN_BLOCKER_LEDGER.csv",
    "r10_kernel": OUT / "P8_Y5_PARENT_QLOC_2208_R10_RANGE_KERNEL_SCAFFOLD.csv",
    "route_selection": OUT / "P8_Y5_PARENT_QLOC_2208_ROUTE_SELECTION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2208_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2208_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2208_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2208_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2208_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2208_PPN_INVERSE_DIVERGENCE_BLOCKER_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2208_R10_RANGE_KERNEL_SCAFFOLD_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_PPN_GREEN_LOWERING_2208_NONCLAIM.csv",
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
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2208_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2208-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2208*",
        "*P8_Y5_BRR545_2208*",
        "*Y5_R2FR_PPN_Green_operator_source_normalization_or_R10_range_kernel_2208*",
        "*JR2208*",
        "*PARENT_QLOC_PPN_GREEN_LOWERING_2208*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2207_handoff",
            ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["NEXT2207_0_2208", "ROP2207_0_PPN_q_loc_linear_response_schema", "VAL2207_OVERALL"],
            "2207 opens the first PPN q_loc response-operator schema and selects 2208.",
        ),
        (
            "2207_first_operator",
            OUT / "P8_Y5_PARENT_QLOC_2207_FIRST_RESPONSE_OPERATOR_ROW.csv",
            ["ROP2207_0_PPN_q_loc_linear_response_schema", "MISSING_GREEN_OPERATOR"],
            "machine-readable PPN and held R10 response-operator schema rows.",
        ),
        (
            "2206_residual_demotion",
            OUT / "P8_Y5_PARENT_QLOC_2206_OFFICIAL_RESIDUAL_DEMOTION.csv",
            ["q_loc_residual_vector_abs", "q_metric_response_defect"],
            "official q_loc residual vector that 2208 tries to project.",
        ),
        (
            "2191_component_runner",
            ROOT / "2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md",
            ["QCS2191_1_PPN", "QCS2191_2_R10", "RUN2191_0_PPN"],
            "component schema and PPN/R10 projection requirements.",
        ),
        (
            "1011_q_loc_bound",
            ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
            ["QBF1011_3_PPN_metric_tail", "QBF1011_0_compact_shell_budget", "V1011_SUMMARY"],
            "older q_loc bound-fill rows already record PPN metric-tail missingness.",
        ),
        (
            "1012_source_normalization",
            ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            ["Y5O1012_8_verdict", "Y5C1012_3_bulk_X_Yukawa_tail", "V1012_SUMMARY"],
            "source-normalization/R11 and range-dependence channels remain unfilled.",
        ),
        (
            "1852_cassini_proxy",
            ROOT / "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
            ["PPN1852_0_cassini_gamma", "PFM1852_3_multi_component_ppn", "VAL1852_OVERALL"],
            "Cassini proxy pressure is real but not a direct MTS residual-vector bound.",
        ),
        (
            "947_R10_projection",
            ROOT / "947-Y5-R10-cg-ba-bound-interface-projection-fill-or-no-marker-kernel-repair.md",
            ["PFA947_4_cg_parent_value", "CGATE947_0_R10_score"],
            "older R10 projection fill confirms parent coupling and kernel rows remain missing.",
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


def ppn_lowering_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            lowering_id="PPNL2208_0_operator_factorization",
            object="R_PPN[q_loc]",
            lowered_form="R_PPN = Pi_PPN o G_Einstein^lin o I_div^{-1}",
            meaning="The PPN Green operator cannot act on q_loc alone; it needs a residual stress/potential T_GK whose divergence gives q_loc.",
            derived_status="FORMAL_FACTORISATION_DERIVED",
            missing_for_score="I_div^{-1} boundary/gauge/domain rule; T_GK profile; source normalization",
            score_ready=False,
        ),
        base_row(
            lowering_id="PPNL2208_1_linearized_metric_kernel",
            object="G_Einstein^lin",
            lowered_form="in harmonic weak-field gauge, Box bar_h_{mu nu}=-(16*pi*G_ref/c^4) T_res_{mu nu}; static limit bar_h_{mu nu}(x)=4G_ref/c^4 int T_res_{mu nu}(x')/|x-x'| d^3x'",
            meaning="The ordinary weak-field Green kernel is available after a stress source is supplied.",
            derived_status="STANDARD_KERNEL_FORM_WRITTEN_NONCLAIM",
            missing_for_score="which residual stress components map to beta,gamma,alpha_i,xi; gauge transform to PPN coordinates",
            score_ready=False,
        ),
        base_row(
            lowering_id="PPNL2208_2_inverse_divergence_obstruction",
            object="I_div^{-1}[q_loc]",
            lowered_form="find T_res^{mu nu} such that -P_loc nabla_mu T_res^{mu nu}=q_loc^nu, with chosen gauge, support and boundary conditions",
            meaning="Many stresses have the same divergence; q_loc alone does not define a unique metric response.",
            derived_status="ROOT_BLOCKER_DERIVED",
            missing_for_score="stress reconstruction convention, no-hidden-boundary mode, support/domain map",
            score_ready=False,
        ),
        base_row(
            lowering_id="PPNL2208_3_source_normalization",
            object="PPN source normalization",
            lowered_form="Delta_PPN_A = Pi_A[h_res] after fixing G_ref, M_H/ref or source charge, tau frame and measured-GM no-absorption rule",
            meaning="PPN coefficients are dimensionless only after the same source measure that defines Newtonian GM is fixed.",
            derived_status="SOURCE_NORMALIZATION_BLOCKER_CONNECTED",
            missing_for_score="Y5 source-normalization owner or scored R11/source coefficients",
            score_ready=False,
        ),
        base_row(
            lowering_id="PPNL2208_4_boundary_support_terms",
            object="boundary/support contribution",
            lowered_form="Delta_PPN_A includes int_boundary B_A[T_res,P_loc,domain] plus compact-support/domain-motion terms",
            meaning="Boundary pieces can mimic or hide PPN residuals if omitted.",
            derived_status="BOUNDARY_TERM_RETAINED",
            missing_for_score="boundary no-flux theorem or finite boundary-response row",
            score_ready=False,
        ),
        base_row(
            lowering_id="PPNL2208_5_verdict",
            object="PPN q_loc response operator",
            lowered_form="PPN is lowered from a black-box Green row to stress reconstruction + weak-field Green + source normalization + boundary/support",
            meaning="This is progress, but still not score-ready.",
            derived_status="LOWERED_BUT_BLOCKED_PIVOT_TO_R10",
            missing_for_score="I_div^{-1}, q_loc/T_res profile, source normalization and boundary/support terms",
            score_ready=False,
        ),
    ]


def ppn_blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        (
            "PPNB2208_0_inverse_divergence",
            "q_loc does not uniquely determine T_res",
            "MISSING_I_DIV_INVERSE_CONVENTION",
            "derive parent T_GK or declare inverse-divergence gauge/domain/boundary rule",
            "PPN;local_GR",
        ),
        (
            "PPNB2208_1_q_profile",
            "q_loc component profile is missing",
            "MISSING_QLOC_PROFILE",
            "source q_T,q_L,q_TF,q_alpha_i over an observed domain",
            "PPN;R10;clock;orbital",
        ),
        (
            "PPNB2208_2_source_normalization",
            "Newtonian source measure and G_ref normalization are unsigned",
            "MISSING_SOURCE_NORMALIZATION",
            "close Y5/PiM/worldtube source measure or fill R11 coefficients",
            "Newton;PPN;R11;R10",
        ),
        (
            "PPNB2208_3_PPN_gauge",
            "weak-field harmonic solution must be transformed to PPN gauge",
            "MISSING_PPN_GAUGE_TRANSFORM",
            "derive parent-owned PPN gauge/readout transform",
            "beta;gamma;alpha_i;xi",
        ),
        (
            "PPNB2208_4_boundary_support",
            "boundary/support/domain terms can carry metric residuals",
            "MISSING_BOUNDARY_SUPPORT_RESPONSE",
            "prove no-flux/support silence or retain explicit boundary response",
            "PPN;source_normalization",
        ),
        (
            "PPNB2208_5_multi_component",
            "Cassini or beta/gamma cannot isolate q_loc alone",
            "MISSING_NO_CANCELLATION_VECTOR_COMPONENTS",
            "score q_loc with c_g, disformal, non-Hilbert, support, boundary and readout components in an absolute envelope",
            "PPN",
        ),
    ]
    return [
        base_row(
            blocker_id=blocker_id,
            blocker=blocker,
            current_status=status,
            required_fix=required_fix,
            observable_link=observable_link,
            blocks_score=True,
            valid_for_claim=False,
        )
        for blocker_id, blocker, status, required_fix, observable_link in blockers
    ]


def r10_kernel_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            kernel_id="R10K2208_0_yukawa_kernel_form",
            object="static finite-range kernel",
            kernel_form="K_lambda(r)=exp(-r/lambda)/(4*pi*r), solving (nabla^2-lambda^-2)K_lambda=-delta^3(r)",
            response_form="Phi_X(x)=Q_source int K_lambda(|x-x'|) rho_X(x') d^3x'",
            what_is_lowered="R10 range response now has a standard kernel scaffold rather than a placeholder W_R10",
            missing_for_score="MTS source charge Q_source, test charge Q_test, q_loc-to-scalar source map, lambda_X",
            schema_ready=True,
            score_ready=False,
        ),
        base_row(
            kernel_id="R10K2208_1_alpha_lambda_point_mass_map",
            object="alpha(lambda) conversion",
            kernel_form="for pointlike normalized source/test charges, Delta a/a_N ~ alpha(lambda)*(1+r/lambda)*exp(-r/lambda)",
            response_form="alpha_R10_q(lambda)=C_qalpha(lambda)*Q_source*Q_test after geometry/material/source normalization",
            what_is_lowered="the observable alpha(lambda) map is separated from parent coupling and material charges",
            missing_for_score="C_qalpha(lambda), source/test charge normalization, apparatus geometry kernel",
            schema_ready=True,
            score_ready=False,
        ),
        base_row(
            kernel_id="R10K2208_2_bound_curve_link",
            object="R10 bound curve",
            kernel_form="compare abs(alpha_R10_q(lambda)) <= alpha_bound(lambda)",
            response_form="requires digitized/source-backed alpha_bound(lambda), not anchor-only smoke rows",
            what_is_lowered="the test comparison rule is explicit",
            missing_for_score="real full bound curve or claim-valid source-backed interpolation rows",
            schema_ready=True,
            score_ready=False,
        ),
        base_row(
            kernel_id="R10K2208_3_route_verdict",
            object="R10 route",
            kernel_form="R10 is narrower than PPN because it needs one radial kernel and alpha(lambda) map rather than a full PPN gauge/vector solution",
            response_form="selected as next empirical-lowering lane, still nonclaim",
            what_is_lowered="R10 becomes the better next target after PPN inverse-divergence blocker",
            missing_for_score="parent q_loc-to-Yukawa source map, lambda_X, charges, bound curve",
            schema_ready=True,
            score_ready=False,
        ),
    ]


def route_selection_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="ROUTE2208_0_PPN",
            route="PPN Green/source-normalization lowering",
            status="LOWERED_BUT_NOT_SCORE_READY",
            reason="PPN response requires inverse-divergence stress reconstruction, source normalization, PPN gauge transform and boundary/support terms.",
            selected_next=False,
        ),
        base_row(
            route_id="ROUTE2208_1_R10",
            route="R10 range-kernel lowering",
            status="SELECTED_NEXT",
            reason="R10 needs a narrower Yukawa/range kernel plus alpha(lambda) conversion; still missing parent q_loc-to-source map and bound curve.",
            selected_next=True,
        ),
        base_row(
            route_id="ROUTE2208_2_parent",
            route="Khat/T_GK parent-stress reconstruction",
            status="HELD_PARALLEL",
            reason="If Khat identity appears, it supplies I_div^{-1} directly and reopens PPN/local-GR route.",
            selected_next=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2208_0_PPN_lowered",
            gate="PPN operator lowered from black-box row",
            status="PASS_NONCLAIM",
            implication="operator factorization is clearer, but not score-ready",
        ),
        base_row(
            gate_id="CG2208_1_PPN_score",
            gate="PPN score can be computed",
            status="BLOCKED_NONCLAIM",
            implication="inverse-divergence stress reconstruction, q profile, source normalization and boundary terms are missing",
        ),
        base_row(
            gate_id="CG2208_2_R10_kernel",
            gate="R10 kernel scaffold exists",
            status="PASS_NONCLAIM",
            implication="Yukawa/range route is now a better next empirical lane",
        ),
        base_row(
            gate_id="CG2208_3_R10_score",
            gate="R10 alpha(lambda) score can be computed",
            status="BLOCKED_NONCLAIM",
            implication="parent q_loc-to-source map, lambda_X, charge normalization and real bound curve are missing",
        ),
        base_row(
            gate_id="CG2208_4_local_GR",
            gate="local-GR/Newton reduction can be claimed",
            status="BLOCKED_NONCLAIM",
            implication="q_loc theorem-zero and residual bounds remain unproved",
        ),
        base_row(
            gate_id="CG2208_5_GitHub",
            gate="public/github update",
            status="BLOCKED_NONCLAIM",
            implication="private goal work only; no GitHub action",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2208_0_gain",
            decision="PPN_OPERATOR_LOWERED_TO_STRESS_RECONSTRUCTION",
            rationale="The PPN row is no longer a vague Green operator: it factors through residual stress reconstruction, weak-field Green kernel, source normalization and boundary terms.",
            next_action="do not score PPN until I_div^{-1} or parent T_GK profile exists",
        ),
        base_row(
            decision_id="DEC2208_1_blocker",
            decision="QLOC_ALONE_IS_NOT_A_METRIC_SOURCE",
            rationale="q_loc is a divergence/projection of residual stress; without T_res or an inverse-divergence convention, the metric perturbation is not unique.",
            next_action="derive Khat/T_GK identity or retain inverse-divergence blocker",
        ),
        base_row(
            decision_id="DEC2208_2_r10",
            decision="R10_RANGE_KERNEL_SELECTED_NEXT",
            rationale="R10 is narrower than full PPN and can be lowered with a Yukawa kernel plus alpha(lambda) conversion before full PPN gauge machinery.",
            next_action="2209 should fill parent q_loc-to-Yukawa source map, lambda_X, charge normalization, or blocker ledger",
        ),
        base_row(
            decision_id="DEC2208_3_no_claim",
            decision="NO_PPN_R10_LOCAL_GR_CLAIM",
            rationale="Both routes are schemas/blocker ledgers, not evidence of a pass.",
            next_action="keep all rows nonclaim until source-backed values or parent theorems exist",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2208_0_2209",
            selection_status="selected",
            target_file="2209-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md",
            target_script="scripts/Y5_R2FR_R10_q_loc_Yukawa_source_map_or_bound_curve_blocker_2209.py",
            objective="lower the R10 route by deriving or sourcing the q_loc-to-Yukawa source map, lambda_X, source/test charge normalization, and bound-curve link; if missing, produce a blocker ledger without scoring",
            success_condition="one R10 input row is source-backed beyond kernel scaffold, or all missing parent inputs are explicitly blocked with valid_for_claim=false",
            do_not_do="do not score alpha(lambda) from placeholders, do not use anchor-only bound rows as claims, do not claim local GR, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2208_1_parent_parallel",
            selection_status="held_parallel",
            target_file="2209b-Y5-R2FR-parent-TGK-stress-reconstruction-for-PPN.md",
            target_script="scripts/Y5_R2FR_parent_TGK_stress_reconstruction_for_PPN_2209b.py",
            objective="derive T_GK or an inverse-divergence convention that maps q_loc to a unique weak-field stress source",
            success_condition="I_div^{-1} is parent-signed or remains an explicit PPN blocker",
            do_not_do="do not choose an arbitrary inverse divergence to make PPN pass",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["ppn_blocker"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["r10_kernel"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["ppn_lowering"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copy_specs:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        row_count = 0
        if source.exists():
            shutil.copy2(source, target)
            copied = target.exists()
            parse_ok, row_count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=row_count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    r10_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(
            base_row(
                validation_id=validation_id,
                status="PASS" if status else "FAIL",
                detail=detail,
            )
        )

    sources_exist = all(truthy(row.get("path_exists")) for row in source_rows)
    needles_found = all(truthy(row.get("needles_found")) for row in source_rows)
    add("VAL2208_00_sources_exist", sources_exist, f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2208_01_needles_found", needles_found, f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    ppn_factor = any(row.get("lowering_id") == "PPNL2208_0_operator_factorization" and "I_div" in str(row.get("lowered_form")) for row in ppn_rows)
    ppn_blocked = any(row.get("lowering_id") == "PPNL2208_5_verdict" and str(row.get("derived_status")) == "LOWERED_BUT_BLOCKED_PIVOT_TO_R10" for row in ppn_rows)
    add("VAL2208_02_ppn_lowering", ppn_factor and ppn_blocked, "PPN row lowered to stress reconstruction and blocked honestly")

    blocker_ok = len(blocker_rows) >= 6 and all(truthy(row.get("blocks_score")) for row in blocker_rows)
    add("VAL2208_03_ppn_blockers", blocker_ok, f"PPN blockers={len(blocker_rows)}")

    r10_kernel_ok = any(row.get("kernel_id") == "R10K2208_0_yukawa_kernel_form" and "K_lambda" in str(row.get("kernel_form")) for row in r10_rows)
    r10_nonclaim = all(truthy(row.get("schema_ready")) and not truthy(row.get("score_ready")) for row in r10_rows)
    add("VAL2208_04_r10_kernel", r10_kernel_ok and r10_nonclaim, "R10 Yukawa kernel scaffold is present and nonclaim")

    route_ok = any(row.get("route_id") == "ROUTE2208_1_R10" and truthy(row.get("selected_next")) for row in route_rows)
    add("VAL2208_05_route_selection", route_ok, "R10 range kernel selected next after PPN lowering")

    claim_ok = any(row.get("gate_id") == "CG2208_1_PPN_score" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows) and any(row.get("gate_id") == "CG2208_3_R10_score" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2208_06_claim_gate", claim_ok, "PPN/R10/local claims remain blocked")

    decision_ok = any(row.get("decision") == "QLOC_ALONE_IS_NOT_A_METRIC_SOURCE" for row in decision_rows_) and any(row.get("decision") == "R10_RANGE_KERNEL_SELECTED_NEXT" for row in decision_rows_)
    add("VAL2208_07_decision", decision_ok, "decision ledger records q_loc metric-source blocker and R10 selection")

    next_ok = any(row.get("route_id") == "NEXT2208_0_2209" and "Yukawa" in str(row.get("objective")) for row in next_rows)
    add("VAL2208_08_next_target", next_ok, "2209 R10 q_loc-Yukawa source map target selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2208_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in branch_rows)
    add("VAL2208_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in branch_rows))

    generated_groups = [source_rows, ppn_rows, blocker_rows, r10_rows, route_rows, claim_rows, decision_rows_, next_rows, branch_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2208_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    formalization_clean = not formalization_has_2208_artifacts()
    add("VAL2208_12_formalization_clean", formalization_clean, "formalization-workbench has no 2208 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2208_13_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2208_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2208 lowers the PPN q_loc response operator to an inverse-divergence stress blocker and selects the narrower R10 Yukawa/kernel source-map route next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
    blocker_rows: list[dict[str, Any]],
    r10_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2208 - Y5/R2FR PPN Green Operator Source Normalization Or R10 Range Kernel",
        "",
        "## Current Verdict",
        "",
        "2208 lowers the PPN response row and finds the real obstruction: `q_loc` is a projected divergence, not by itself a unique metric source.",
        "",
        "The correct factorization is:",
        "",
        "`R_PPN[q_loc] = Pi_PPN o G_Einstein^lin o I_div^{-1}[q_loc]`.",
        "",
        "`G_Einstein^lin` is standard once a residual stress is supplied. The missing object is `I_div^{-1}`: a parent-signed reconstruction of `T_res` from `q_loc`, including gauge, support, source normalization, and boundary conditions. Without that, many residual stresses share the same `q_loc`, so a PPN score would be arbitrary.",
        "",
        "Because full PPN is too broad at this stage, 2208 selects the narrower R10 route next: use a finite-range/Yukawa kernel scaffold, then demand a parent q_loc-to-source map, `lambda_X`, source/test charges, and real alpha-bound curve before any score.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## PPN Green Operator Lowering",
        "",
        md_table(ppn_rows, ["lowering_id", "object", "lowered_form", "meaning", "derived_status", "missing_for_score", "score_ready", "valid_for_claim"]),
        "",
        "## PPN Blocker Ledger",
        "",
        md_table(blocker_rows, ["blocker_id", "blocker", "current_status", "required_fix", "observable_link", "blocks_score", "valid_for_claim"]),
        "",
        "## R10 Range Kernel Scaffold",
        "",
        md_table(r10_rows, ["kernel_id", "object", "kernel_form", "response_form", "what_is_lowered", "missing_for_score", "schema_ready", "score_ready", "valid_for_claim"]),
        "",
        "## Route Selection",
        "",
        md_table(route_rows, ["route_id", "route", "status", "reason", "selected_next", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
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
        md_table(branch_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is the correct kind of grim-but-useful result. PPN is not abandoned, but it needs `T_GK` or a parent inverse-divergence map before it can be scored. That is exactly the same ownership issue seen in 2206/2207, now expressed as an empirical operator problem.",
        "",
        "The best next attack is R10 because it is narrower: one finite-range kernel, one alpha(lambda) conversion, one source/test normalization problem. If that fills, we finally get a test lane that is less huge than full PPN.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    ppn_rows = ppn_lowering_rows()
    blocker_rows = ppn_blocker_rows()
    r10_rows = r10_kernel_rows()
    route_rows = route_selection_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["ppn_lowering"], ppn_rows),
        (OUTPUTS["ppn_blocker"], blocker_rows),
        (OUTPUTS["r10_kernel"], r10_rows),
        (OUTPUTS["route_selection"], route_rows),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], branch_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        ppn_rows,
        blocker_rows,
        r10_rows,
        route_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        ppn_rows,
        blocker_rows,
        r10_rows,
        route_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
