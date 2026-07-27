from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2207"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2207_SOURCE_REGISTER.csv",
    "metric_variation": OUT / "P8_Y5_PARENT_QLOC_2207_GAMMA_EFF_METRIC_VARIATION_ATTEMPT.csv",
    "metric_match": OUT / "P8_Y5_PARENT_QLOC_2207_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "first_operator": OUT / "P8_Y5_PARENT_QLOC_2207_FIRST_RESPONSE_OPERATOR_ROW.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2207_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2207_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2207_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2207_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2207_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2207_GAMMA_EFF_METRIC_VARIATION_ATTEMPT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2207_FIRST_RESPONSE_OPERATOR_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_KHAT_METRIC_RESPONSE_AUDIT_2207_NONCLAIM.csv",
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


def formalization_has_2207_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2207-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2207*",
        "*P8_Y5_BRR545_2207*",
        "*Y5_R2FR_Gamma_eff_metric_variation_or_first_q_loc_response_operator_row_2207*",
        "*JR2207*",
        "*PARENT_QLOC_KHAT_METRIC_RESPONSE_AUDIT_2207*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2206_handoff",
            ROOT / "2206-Y5-R2FR-GammaKhat-q-loc-parent-action-signature-or-official-residual-demotion.md",
            ["NEXT2206_0_2207", "DEC2206_3_best_next", "VAL2206_OVERALL"],
            "2206 selects one Gamma_eff metric variation attempt or first response-operator row.",
        ),
        (
            "2206_next_target",
            OUT / "P8_Y5_PARENT_QLOC_2206_NEXT_TARGET.csv",
            ["NEXT2206_0_2207", "metric response"],
            "machine-readable 2206 next target.",
        ),
        (
            "2206_residual_demotion",
            OUT / "P8_Y5_PARENT_QLOC_2206_OFFICIAL_RESIDUAL_DEMOTION.csv",
            ["q_metric_response_defect", "q_loc_residual_vector_abs"],
            "official q_loc residual vector to be fed by 2207.",
        ),
        (
            "Gamma_owner_candidates",
            OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner"],
            "best available Gamma_eff candidate and fallback residual runner.",
        ),
        (
            "GK_metric_response_audit",
            OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            ["MA515_1_Khat_metric_response", "MA515_6_units_and_readout"],
            "audit that current Khat is not yet metric response of a source-owned Gamma_eff.",
        ),
        (
            "GK_action_candidates",
            OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
            ["GK514_A_metric_response_scalar_density", "GK514_D_residual_branch"],
            "candidate action routes and residual branch.",
        ),
        (
            "1010_action_helmholtz",
            ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            ["GKT1010_1_metric_response_identity", "GKT1010_6_verdict", "QRES1010_0_q_loc_vector"],
            "action, metric-response, Helmholtz and q_loc retention schema.",
        ),
        (
            "2191_component_runner",
            ROOT / "2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md",
            ["QCS2191_1_PPN", "RUN2191_0_PPN", "VAL2191_OVERALL"],
            "q_loc PPN component and response-operator requirements.",
        ),
        (
            "2198_component_pressure",
            ROOT / "2198-Y5-R2FR-beta-source-zero-or-bounded-component-pack.md",
            ["FPP2198_1_alpha_PPN_proxy", "TBG2198_3_vector_tail", "VAL2198_OVERALL"],
            "Cassini proxy pressure exists but is not a direct MTS component bound.",
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


def metric_variation_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            attempt_id="GMV2207_0_response_doublet_setup",
            candidate_id="GO516_A_response_doublet_quadratic_density",
            gamma_eff_candidate="Gamma_eff=Gamma0+1/2 M_AB(g,R_even,D,...) Z^A Z^B+O(Z^4)",
            metric_variation_result="K_metric^{mu nu}=2/sqrt(-g) delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} = volume_term + 1/2 (delta M_AB/delta g_{mu nu}) Z^A Z^B + M_AB Z^A delta_g Z^B + derivative/boundary terms",
            double_zero_result="after Gamma0 subtraction and regular Z=0 fixed point, K_metric(Phi0)=0 and first Z-variation vanishes conditionally",
            what_this_proves="formal response-doublet density can carry the desired double-zero shape",
            what_it_does_not_prove="current MTS K_hat is not yet shown to equal this K_metric",
            proof_status="CONDITIONAL_FORMAL_VARIATION_NOT_PARENT_SIGNED",
        ),
        base_row(
            attempt_id="GMV2207_1_positive_auxiliary_setup",
            candidate_id="GO516_B_positive_auxiliary_energy_density",
            gamma_eff_candidate="Gamma_eff=V(Phi)+1/2 G_AB(Phi) nabla Phi^A nabla Phi^B",
            metric_variation_result="K_metric is the usual potential-plus-gradient stress response, with derivative/boundary terms from the kinetic operator",
            double_zero_result="can vanish if Phi=Phi0, nabla Phi=0, V(Phi0) is subtracted, source current is zero, and boundary no-flux holds",
            what_this_proves="positive energy/gap route is mathematically plausible",
            what_it_does_not_prove="source-free collar, positive gap, K_hat identity and boundary silence are not signed",
            proof_status="CONDITIONAL_GAP_ROUTE_NOT_PARENT_SIGNED",
        ),
        base_row(
            attempt_id="GMV2207_2_topological_boundary_setup",
            candidate_id="GO516_C_topological_boundary_density",
            gamma_eff_candidate="Gamma_eff=dB_GK or normalized boundary/topological density",
            metric_variation_result="bulk K_metric can be improvement/exact and locally silent only if the boundary class is fixed before readout",
            double_zero_result="bulk zero possible, boundary flux still live",
            what_this_proves="topological route can remove bulk q_loc only under fixed boundary class",
            what_it_does_not_prove="theta_GK/Q_GK no-flux and charge units remain open",
            proof_status="CONDITIONAL_TOPOLOGICAL_ROUTE_BOUNDARY_OPEN",
        ),
        base_row(
            attempt_id="GMV2207_3_verdict",
            candidate_id="selected_current_branch",
            gamma_eff_candidate="response-doublet metric variation is the best formal candidate; residual branch remains official",
            metric_variation_result="metric-response clause can be written but not matched to current K_hat",
            double_zero_result="conditional double-zero exists for a future parent branch, not for current claim",
            what_this_proves="the coupling has a credible derivation target rather than pure hand switching",
            what_it_does_not_prove="q_loc=0, local GR, PPN pass, or Newton limit",
            proof_status="METRIC_RESPONSE_NOT_PARENT_SIGNED_FIRST_OPERATOR_ROW_REQUIRED",
        ),
    ]


def metric_match_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            audit_id="KMR2207_0_candidate_density_exists",
            match_clause="Gamma_eff source-owned scalar density",
            required_evidence="explicit local scalar density with field content, metric dependence, units, and boundary convention",
            current_evidence="GO516_A gives a candidate formula but MA515_0 says current Gamma_eff owner is missing",
            pass_now=False,
            residual_if_missing="q_action_owner_defect",
            next_action="write actual parent density or keep residual branch",
        ),
        base_row(
            audit_id="KMR2207_1_metric_variation_computed_formally",
            match_clause="formal K_metric formula",
            required_evidence="delta[sqrt(-g)Gamma_eff]/delta g_{mu nu} is written with volume, derivative and boundary terms",
            current_evidence="2207 writes the response-doublet formal variation",
            pass_now=True,
            residual_if_missing="none_for_formal_step",
            next_action="compare this K_metric to the existing K_hat symbol map",
        ),
        base_row(
            audit_id="KMR2207_2_Khat_identity",
            match_clause="K_hat equals K_metric",
            required_evidence="source path showing K_hat was defined as the same metric response under the same convention",
            current_evidence="MA515_1 says no derivation as delta[sqrt(-g)Gamma_eff]/delta g was found",
            pass_now=False,
            residual_if_missing="q_metric_response_defect",
            next_action="find or derive K_hat identity; otherwise score q_metric_response_defect",
        ),
        base_row(
            audit_id="KMR2207_3_double_zero",
            match_clause="T_GK(Phi0)=0 and first variation zero",
            required_evidence="Gamma0 subtraction, Z=0 fixed point, regular M_AB and no linear metric/readout term",
            current_evidence="formal response doublet gives this conditionally, but physical q_loc component map is missing",
            pass_now=False,
            residual_if_missing="epsilon_C0_GammaKhat;epsilon_dC_GammaKhat",
            next_action="map response doublet variables to observed q_loc components",
        ),
        base_row(
            audit_id="KMR2207_4_units_readout",
            match_clause="units and PPN/R10 response",
            required_evidence="q_loc units, source normalization, and response operators into local observables",
            current_evidence="2191 and MA515_6 keep units/readout source-missing",
            pass_now=False,
            residual_if_missing="q_units_response_defect",
            next_action="create first nonclaim response-operator row",
        ),
        base_row(
            audit_id="KMR2207_5_overall",
            match_clause="Khat metric-response parent signature",
            required_evidence="all KMR2207_0..4 pass in one branch",
            current_evidence="only the formal variation step passes; ownership and Khat identity fail",
            pass_now=False,
            residual_if_missing="q_loc_residual_vector_abs",
            next_action="do not claim q_loc zero; use first response operator row",
        ),
    ]


def first_operator_rows() -> list[dict[str, Any]]:
    source_basis = ROOT / "2191-Y5-R2FR-q_loc-component-projection-runner-and-theorem-zero-certificate.md"
    return [
        base_row(
            operator_id="ROP2207_0_PPN_q_loc_linear_response_schema",
            arena="PPN",
            row_kind="first_nonclaim_response_operator_schema",
            input_contract="observed-frame q_loc components q_T,q_L,q_TF,q_alpha_i plus source normalization and weak-field gauge",
            output_quantity="Delta_PPN_q=(Delta_beta,Delta_gamma,Delta_alpha_i,Delta_zeta_i,Delta_xi)",
            operator_form="Delta_PPN_A = integral_D G_A^nu(x,xprime) q_loc_nu(xprime) dVprime + boundary/support terms",
            input_units="force_density_or_dimensionless_after_declared_normalization",
            output_units="dimensionless_PPN_coefficients",
            source_path=str(source_basis),
            equation_ref="QCS2191_1_PPN;RUN2191_0_PPN;2207_Ward_identity_contract",
            schema_ready=True,
            score_ready=False,
            valid_for_claim=False,
            blocking_missing_inputs="MISSING_GREEN_OPERATOR;MISSING_QLOC_PROFILE;MISSING_SOURCE_NORMALIZATION;MISSING_BOUNDARY_SUPPORT_TERMS",
            notes="This is not a PPN score. It is the first source-backed schema row telling future tests exactly what must be filled.",
        ),
        base_row(
            operator_id="ROP2207_1_R10_q_loc_range_response_held",
            arena="R10_short_range",
            row_kind="held_next_response_operator_schema",
            input_contract="q_loc(lambda) profile, range kernel, alpha(lambda) conversion, real bound curve",
            output_quantity="alpha_R10_q(lambda)",
            operator_form="alpha_R10_q(lambda)=integral W_R10(lambda,x) q_loc(x) dV after units/source normalization",
            input_units="force_density_or_declared_range_normalized_vector",
            output_units="dimensionless_alpha_lambda",
            source_path=str(source_basis),
            equation_ref="QCS2191_2_R10;RUN2191_1_R10",
            schema_ready=False,
            score_ready=False,
            valid_for_claim=False,
            blocking_missing_inputs="MISSING_RANGE_KERNEL;MISSING_CQ_ALPHA_LAMBDA;MISSING_REAL_BOUND_CURVE;MISSING_COMPONENT_PROFILE",
            notes="R10 is held until PPN schema and/or real range kernel are better specified.",
        ),
    ]


def claim_gate_rows(metric_rows: list[dict[str, Any]], match_rows: list[dict[str, Any]], operator_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    formal_step = any(row.get("audit_id") == "KMR2207_1_metric_variation_computed_formally" and truthy(row.get("pass_now")) for row in match_rows)
    khat_match = any(row.get("audit_id") == "KMR2207_5_overall" and truthy(row.get("pass_now")) for row in match_rows)
    first_schema = any(row.get("operator_id") == "ROP2207_0_PPN_q_loc_linear_response_schema" and truthy(row.get("schema_ready")) for row in operator_rows)
    return [
        base_row(
            gate_id="CG2207_0_formal_metric_variation",
            gate="one Gamma_eff metric variation has been written",
            status="PASS_NONCLAIM" if formal_step else "BLOCKED_NONCLAIM",
            implication="response-doublet route has a real algebraic target, but not yet MTS ownership",
        ),
        base_row(
            gate_id="CG2207_1_Khat_match",
            gate="K_hat equals the computed K_metric",
            status="PASS" if khat_match else "BLOCKED_NONCLAIM",
            implication="q_metric_response_defect remains live",
        ),
        base_row(
            gate_id="CG2207_2_q_loc_zero",
            gate="q_loc=0/local GR can be claimed",
            status="BLOCKED_NONCLAIM",
            implication="formal variation alone is not enough; action owner, Khat identity, Euler, P_loc and boundary remain unsigned",
        ),
        base_row(
            gate_id="CG2207_3_first_operator",
            gate="first q_loc response-operator schema row exists",
            status="PASS_NONCLAIM" if first_schema else "BLOCKED_NONCLAIM",
            implication="PPN testing path now has a concrete nonclaim input contract",
        ),
        base_row(
            gate_id="CG2207_4_empirical_score",
            gate="PPN/R10 score can be computed",
            status="BLOCKED_NONCLAIM",
            implication="Green operator, q_loc profile, source normalization and boundary/support rows are still missing",
        ),
        base_row(
            gate_id="CG2207_5_GitHub",
            gate="public/github update",
            status="BLOCKED_NONCLAIM",
            implication="private goal work only; no GitHub action",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2207_0_gain",
            decision="RESPONSE_DOUBLET_METRIC_VARIATION_WRITTEN",
            rationale="The best Gamma_eff candidate has a formal metric response and can conditionally produce a double-zero at Z=0 after Gamma0 subtraction.",
            next_action="preserve this as the leading future parent-action construction",
        ),
        base_row(
            decision_id="DEC2207_1_limit",
            decision="KHAT_IDENTITY_NOT_MATCHED",
            rationale="Current corpus still does not prove K_hat equals that metric response under the same convention, so q_loc theorem-zero cannot be promoted.",
            next_action="keep q_metric_response_defect in the official residual vector",
        ),
        base_row(
            decision_id="DEC2207_2_testing_path",
            decision="FIRST_PPN_RESPONSE_OPERATOR_SCHEMA_OPENED",
            rationale="Since the parent signature did not close, future empirical work now has a concrete PPN operator row rather than a vague q_loc complaint.",
            next_action="2208 should lower the PPN Green/source-normalization placeholders or pivot to R10 range kernel if PPN is too broad",
        ),
        base_row(
            decision_id="DEC2207_3_no_claim",
            decision="NO_LOCAL_GR_OR_PPN_CLAIM",
            rationale="2207 is a derivation attempt plus testing schema, not a theorem-zero or empirical pass.",
            next_action="continue deriving missing operator/source/profile rows before scoring",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2207_0_2208",
            selection_status="selected",
            target_file="2208-Y5-R2FR-PPN-Green-operator-source-normalization-or-R10-range-kernel.md",
            target_script="scripts/Y5_R2FR_PPN_Green_operator_source_normalization_or_R10_range_kernel_2208.py",
            objective="lower the first PPN q_loc response operator by deriving or sourcing the Green operator, source normalization, q_loc profile units, and boundary/support terms; if PPN is too broad, pivot to the R10 range kernel row",
            success_condition="one response-operator component is source-backed beyond schema level, still valid_for_claim=false, or a blocker ledger proves the required data are missing",
            do_not_do="do not compute PPN/R10 scores from placeholders, do not use Cassini proxy as direct MTS bound, do not claim q_loc zero, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2207_1_parent_parallel",
            selection_status="held_parallel",
            target_file="2208b-Y5-R2FR-Khat-identity-source-hunt.md",
            target_script="scripts/Y5_R2FR_Khat_identity_source_hunt_2208b.py",
            objective="hunt the corpus for an explicit K_hat metric-response definition; if found, reconnect to parent-action route",
            success_condition="K_hat identity source path exists and matches the 2207 convention, or q_metric_response_defect remains active",
            do_not_do="do not infer Khat identity by notation similarity",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["metric_variation"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["first_operator"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["metric_match"], BRANCH_COPIES["beta_docs"]),
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
    metric_rows: list[dict[str, Any]],
    match_rows: list[dict[str, Any]],
    operator_rows: list[dict[str, Any]],
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
    add("VAL2207_00_sources_exist", sources_exist, f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2207_01_needles_found", needles_found, f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    response_variation = any(row.get("attempt_id") == "GMV2207_0_response_doublet_setup" and "delta[sqrt(-g)Gamma_eff]" in str(row.get("metric_variation_result")) for row in metric_rows)
    verdict_not_signed = any(row.get("attempt_id") == "GMV2207_3_verdict" and "NOT_PARENT_SIGNED" in str(row.get("proof_status")) for row in metric_rows)
    add("VAL2207_02_metric_variation_attempt", response_variation and verdict_not_signed, "response-doublet metric variation written and kept nonclaim")

    formal_pass = any(row.get("audit_id") == "KMR2207_1_metric_variation_computed_formally" and truthy(row.get("pass_now")) for row in match_rows)
    overall_fail = any(row.get("audit_id") == "KMR2207_5_overall" and not truthy(row.get("pass_now")) for row in match_rows)
    add("VAL2207_03_match_audit", formal_pass and overall_fail, "formal variation passes; Khat identity/overall parent signature remains blocked")

    ppn_schema = [
        row for row in operator_rows
        if row.get("operator_id") == "ROP2207_0_PPN_q_loc_linear_response_schema"
    ]
    ppn_ok = bool(ppn_schema) and truthy(ppn_schema[0].get("schema_ready")) and not truthy(ppn_schema[0].get("score_ready")) and Path(str(ppn_schema[0].get("source_path"))).exists()
    add("VAL2207_04_first_operator_row", ppn_ok, "first PPN response-operator schema row exists with source path and claim=false")

    claim_ok = any(row.get("gate_id") == "CG2207_2_q_loc_zero" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    operator_gate_ok = any(row.get("gate_id") == "CG2207_3_first_operator" and row.get("status") == "PASS_NONCLAIM" for row in claim_rows)
    add("VAL2207_05_claim_gate", claim_ok and operator_gate_ok, "q_loc zero blocked; first operator row passes as nonclaim schema")

    decision_ok = any(row.get("decision") == "KHAT_IDENTITY_NOT_MATCHED" for row in decision_rows_) and any(row.get("decision") == "FIRST_PPN_RESPONSE_OPERATOR_SCHEMA_OPENED" for row in decision_rows_)
    add("VAL2207_06_decision", decision_ok, "decision ledger records Khat mismatch and PPN operator opening")

    next_ok = any(row.get("route_id") == "NEXT2207_0_2208" and "PPN" in str(row.get("objective")) for row in next_rows)
    add("VAL2207_07_next_target", next_ok, "2208 PPN Green/source-normalization or R10 range kernel target selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2207_08_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in branch_rows)
    add("VAL2207_09_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in branch_rows))

    generated_groups = [source_rows, metric_rows, match_rows, operator_rows, claim_rows, decision_rows_, next_rows, branch_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2207_10_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    formalization_clean = not formalization_has_2207_artifacts()
    add("VAL2207_11_formalization_clean", formalization_clean, "formalization-workbench has no 2207 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2207_12_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2207_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2207 writes one formal Gamma_eff metric variation, refuses Khat metric-response promotion, and opens the first nonclaim PPN q_loc response-operator schema row",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    metric_rows: list[dict[str, Any]],
    match_rows: list[dict[str, Any]],
    operator_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branch_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2207 - Y5/R2FR Gamma_eff Metric Variation Or First q_loc Response Operator Row",
        "",
        "## Current Verdict",
        "",
        "2207 takes the requested leap but refuses to fake the landing.",
        "",
        "The best current `Gamma_eff` candidate is the response-doublet quadratic density:",
        "",
        "`Gamma_eff = Gamma0 + 1/2 M_AB(g,R_even,D,...) Z^A Z^B + O(Z^4)`.",
        "",
        "Its formal metric variation can give the right double-zero shape: after `Gamma0` subtraction and at the `Z=0` local fixed point, the metric response and its first `Z` variation vanish conditionally. That is a genuine mathematical opening.",
        "",
        "But the current corpus still does **not** prove that the existing `K_hat` is this metric response. So `q_loc=0` is still not claimed. Instead, 2207 opens the first nonclaim PPN response-operator schema row so the demoted residual can be tested honestly.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Gamma_eff Metric Variation Attempt",
        "",
        md_table(metric_rows, ["attempt_id", "candidate_id", "gamma_eff_candidate", "metric_variation_result", "double_zero_result", "what_this_proves", "what_it_does_not_prove", "proof_status", "valid_for_claim"]),
        "",
        "## Khat Metric Response Match Audit",
        "",
        md_table(match_rows, ["audit_id", "match_clause", "required_evidence", "current_evidence", "pass_now", "residual_if_missing", "next_action", "valid_for_claim"]),
        "",
        "## First Response Operator Row",
        "",
        md_table(operator_rows, ["operator_id", "arena", "row_kind", "input_contract", "output_quantity", "operator_form", "input_units", "output_units", "source_path", "equation_ref", "schema_ready", "score_ready", "blocking_missing_inputs", "valid_for_claim"]),
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
        "This is a good sign, but not yet a win. The response-doublet form is exactly the sort of mechanism that could make the local branch derivable rather than axiomatic. The missing bridge is the one that matters: `K_hat` must be shown to be the same metric response, not merely named like one.",
        "",
        "Next best move: lower the PPN response row. That means deriving or sourcing the weak-field Green operator, source normalization, q_loc profile units, and boundary/support terms. If that is too broad, pivot to the R10 range kernel because it is narrower and more directly scoreable.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    metric_rows = metric_variation_rows()
    match_rows = metric_match_rows()
    operator_rows = first_operator_rows()
    claim_rows = claim_gate_rows(metric_rows, match_rows, operator_rows)
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["metric_variation"], metric_rows),
        (OUTPUTS["metric_match"], match_rows),
        (OUTPUTS["first_operator"], operator_rows),
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
        metric_rows,
        match_rows,
        operator_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        branch_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        metric_rows,
        match_rows,
        operator_rows,
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
