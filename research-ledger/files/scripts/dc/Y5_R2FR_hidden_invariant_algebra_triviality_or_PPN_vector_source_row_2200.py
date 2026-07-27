from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2200"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2200-Y5-R2FR-hidden-invariant-algebra-triviality-or-PPN-vector-source-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2200_SOURCE_REGISTER.csv",
    "hidden_route_synthesis": OUT / "P8_Y5_PARENT_QLOC_2200_HIDDEN_ROUTE_SYNTHESIS.csv",
    "ppn_vector_source_row": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
    "ppn_component_contract": OUT / "P8_Y5_PARENT_QLOC_2200_PPN_COMPONENT_CONTRACT.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2200_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2200_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2200_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2200_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2200_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2200_PPN_VECTOR_SOURCE_ROW_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_PPN_COMPONENT_CONTRACT_2200_NONCLAIM.csv",
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
        values: list[str] = []
        for column in columns:
            values.append(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|"))
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2200_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2200-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2200*",
        "*P8_Y5_BRR545_2200*",
        "*Y5_R2FR_hidden_invariant_algebra_triviality_or_PPN_vector_source_row_2200*",
        "*JR2200*",
        "*PARENT_QLOC_PPN_COMPONENT_CONTRACT_2200*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2199_doc",
            ROOT / "2199-Y5-R2FR-no-hidden-visible-hom-or-PPN-vector-envelope.md",
            ["NEXT2199_0_2200", "VAL2199_OVERALL", "hidden invariant algebra"],
            "2199 selected hidden invariant triviality first, with PPN vector source row as fallback.",
        ),
        (
            "2199_next",
            OUT / "P8_Y5_PARENT_QLOC_2199_NEXT_TARGET.csv",
            ["2200-Y5-R2FR-hidden-invariant-algebra-triviality-or-PPN-vector-source-row.md", "do not claim local GR"],
            "Machine-readable 2200 target.",
        ),
        (
            "1924_doc",
            ROOT / "1924-Y5-R2FR-hidden-invariant-algebra-triviality-or-scalar-prior-rows.md",
            ["HIDDEN_INVARIANT_TRIVIALITY_NOT_DERIVED", "VAL1924_OVERALL", "seven generator debts"],
            "Earlier R2FR hidden-invariant attempt; prevents duplicating the same theorem failure.",
        ),
        (
            "1925_doc",
            ROOT / "1925-Y5-R2FR-parent-scalar-nohair-input-pack-or-finite-profile-rows.md",
            ["SCALAR_NOHAIR_INPUT_PACK_NOT_DERIVED", "VAL1925_OVERALL", "direct WEP product"],
            "Earlier R2FR scalar no-hair input-pack attempt; records exact conditional identity and missing clauses.",
        ),
        (
            "2161_doc",
            ROOT / "2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md",
            ["PPN Vector Envelope", "VAL2161_OVERALL", "Cassini scalar proxy"],
            "Current parent-normalization/PPN vector envelope checkpoint.",
        ),
        (
            "2161_ppn_vector",
            OUT / "P8_Y5_PARENT_QLOC_2161_PPN_VECTOR_ENVELOPE.csv",
            ["PVE2161_7_source_proxy_ceiling", "SOURCE_PROXY_ONLY", "PVE2161_6_total_abs_guard"],
            "Machine-readable PPN vector component envelope.",
        ),
        (
            "2198_proxy_pressure",
            OUT / "P8_Y5_PARENT_QLOC_2198_FIRST_PROXY_PRESSURE_ROW.csv",
            ["FPP2198_1_alpha_PPN_proxy", "0.005788015401465051", "raw c_g remains unbounded"],
            "Cassini-derived alpha proxy pressure row; not a direct MTS component bound.",
        ),
        (
            "local_bounds",
            ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
            ["Cassini_Shapiro_gamma_2003", "gamma_minus_1", "nature01997"],
            "Local empirical bound ledger containing Cassini gamma source metadata.",
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


def hidden_route_synthesis_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="HRS2200_0_2199_target",
            route="hidden invariant algebra triviality",
            current_result="TARGET_SHARP_BUT_ALREADY_TESTED",
            evidence="2199 reduces no-hidden-visible-hom to hidden invariant triviality; 1924 already attempts O(C_hid)^inv=R.",
            obstruction="surviving generator debt and scalar counterexample remain live",
            next_effect="do not rerun the same theorem without a new parent owner/no-hair input",
        ),
        base_row(
            route_id="HRS2200_1_1924_verdict",
            route="O(C_hid)^inv=R",
            current_result="NOT_DERIVED_CURRENT_CORPUS",
            evidence="1924 records seven generator debts: finite cell spectrum, domain class, selector, memory scalar, time arrow, species constants, readout projector.",
            obstruction="any nonconstant scalar I_hid still builds coefficient maps into alpha, masses, clocks, or source weights",
            next_effect="hidden-visible coefficient silence cannot be claimed",
        ),
        base_row(
            route_id="HRS2200_2_nohair_contract",
            route="exact scalar no-hair/profile-zero",
            current_result="EXACT_CONDITIONAL_THEOREM_NOT_PROMOTED",
            evidence="1925 retains the positive energy identity but rejects promotion because owner/sign/source/boundary/zero-mode/readout clauses do not close together.",
            obstruction="the identity may silence the wrong variable or miss finite source/boundary hair",
            next_effect="retain the no-hair contract as future parent-action requirement",
        ),
        base_row(
            route_id="HRS2200_3_route_selection",
            route="first PPN vector source row",
            current_result="SELECTED_NONCLAIM_NEXT",
            evidence="2161 and 2199 agree that the invariant local comparison object is the full PPN residual vector, not raw c_g.",
            obstruction="Cassini is source-backed pressure only until PPN vector components are parent-owned or bounded",
            next_effect="convert Cassini pressure into a machine-readable vector-source contract without claiming a pass",
        ),
    ]


def ppn_vector_source_rows() -> list[dict[str, Any]]:
    delta_gamma_guard = 6.7e-5
    alpha_proxy = math.sqrt(delta_gamma_guard / (2.0 - delta_gamma_guard))
    return [
        base_row(
            source_row_id="PVS2200_0_cassini_gamma_source",
            arena="PPN/Cassini/Shapiro",
            observable="gamma_minus_1",
            empirical_bound_value=delta_gamma_guard,
            empirical_bound_units="dimensionless",
            confidence_or_guard="two_sigma_guard_from_2198_abs_central_plus_2sigma",
            source_path_or_url="https://pubmed.ncbi.nlm.nih.gov/14508481/; D:\\Users\\ollet\\Desktop\\Turn an intuitive research programme into a formal field-theoretic framework\\Motion-TimeSpace--main\\post-checkpoint-work\\source-intake\\local_bounds\\local_bound_claims.csv",
            extraction_method="carried source-backed Cassini gamma pressure row; not refit here",
            translated_object="gamma_bound_only",
            translation_formula="none",
            translated_bound_value="not_applicable",
            translation_status="SOURCE_BOUND_ONLY",
            direct_mts_component_bound=False,
            required_inputs_for_claim="derive MTS PPN metric/readout map and vector observable",
            score_ready=False,
        ),
        base_row(
            source_row_id="PVS2200_1_alpha_eff_proxy",
            arena="PPN/Cassini/scalar-tensor proxy",
            observable="alpha_PPN_proxy",
            empirical_bound_value=alpha_proxy,
            empirical_bound_units="dimensionless",
            confidence_or_guard="derived_proxy_from_delta_gamma_guard",
            source_path_or_url=str(OUT / "P8_Y5_PARENT_QLOC_2198_FIRST_PROXY_PRESSURE_ROW.csv"),
            extraction_method="sqrt(delta_gamma/(2-delta_gamma)) unscreened massless single-scalar proxy",
            translated_object="alpha_eff_PPN",
            translation_formula="|alpha_eff_PPN| <= sqrt(delta_gamma/(2-delta_gamma))",
            translated_bound_value=f"{alpha_proxy:.18g}",
            translation_status="SOURCE_PROXY_ONLY",
            direct_mts_component_bound=False,
            required_inputs_for_claim="prove alpha_eff_PPN is the actual MTS PPN residual observable and bound all vector tails",
            score_ready=False,
        ),
        base_row(
            source_row_id="PVS2200_2_vector_contract",
            arena="PPN/local-GR comparison",
            observable="alpha_PPN_total_abs_vector",
            empirical_bound_value=alpha_proxy,
            empirical_bound_units="dimensionless",
            confidence_or_guard="proxy_ceiling_applies_only_after_translation_gate",
            source_path_or_url=str(OUT / "P8_Y5_PARENT_QLOC_2161_PPN_VECTOR_ENVELOPE.csv"),
            extraction_method="carry Cassini pressure onto full no-cancellation vector target",
            translated_object="|alpha_PPN_total|",
            translation_formula="|alpha_total| <= |alpha_cg|+|alpha_dis|+|alpha_nonH|+|alpha_support|+|alpha_boundary|+|alpha_readout|",
            translated_bound_value=f"{alpha_proxy:.18g}",
            translation_status="NONCLAIM_VECTOR_TARGET",
            direct_mts_component_bound=False,
            required_inputs_for_claim="numeric/theorem-zero rows for every vector component and no pair-cancellation assumption",
            score_ready=False,
        ),
    ]


def ppn_component_contract_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            component_id="PCC2200_0_cg",
            component="common conformal coupling",
            object="alpha_cg",
            formula="tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)",
            source_ceiling_link="PVS2200_2_vector_contract",
            current_status="MISSING_ZX_TAU_RANGE",
            required_parent_or_source_input="Z_X, lambda_X, tau_PPN, S_PPN, c_g same-branch owner",
            no_cancellation_policy="absolute contribution must fit under vector ceiling unless theorem-zero",
            score_ready=False,
        ),
        base_row(
            component_id="PCC2200_1_disformal",
            component="disformal/preferred-frame tail",
            object="alpha_dis",
            formula="tau_dis*b_dis",
            source_ceiling_link="PVS2200_2_vector_contract",
            current_status="MISSING_DISFORMAL_PPN_PROJECTION",
            required_parent_or_source_input="matter metric expansion and preferred-frame PPN map",
            no_cancellation_policy="cannot cancel alpha_cg by assumption",
            score_ready=False,
        ),
        base_row(
            component_id="PCC2200_2_nonH",
            component="non-Hilbert/source-current tail",
            object="alpha_nonH",
            formula="tau_nonH*q_nonH",
            source_ceiling_link="PVS2200_2_vector_contract",
            current_status="MISSING_NONHILBERT_PPN_PROJECTION",
            required_parent_or_source_input="source-current conservation accounting and non-Hilbert projection",
            no_cancellation_policy="retained until theorem-zero or bounded",
            score_ready=False,
        ),
        base_row(
            component_id="PCC2200_3_support_domain",
            component="support/domain local-projection tail",
            object="alpha_support_domain",
            formula="tau_support*Delta_W_support + tau_domain*q_domain",
            source_ceiling_link="PVS2200_2_vector_contract",
            current_status="MISSING_SUPPORT_DOMAIN_PPN_PROJECTION",
            required_parent_or_source_input="finite-source support theorem and representative-domain rule",
            no_cancellation_policy="absolute envelope required",
            score_ready=False,
        ),
        base_row(
            component_id="PCC2200_4_boundary",
            component="boundary/local flux tail",
            object="alpha_boundary",
            formula="tau_boundary*q_boundary",
            source_ceiling_link="PVS2200_2_vector_contract",
            current_status="MISSING_BOUNDARY_PPN_PROJECTION",
            required_parent_or_source_input="local boundary flux zero theorem or numeric bound",
            no_cancellation_policy="no local plateau axiom",
            score_ready=False,
        ),
        base_row(
            component_id="PCC2200_5_readout",
            component="measured-G/readout calibration tail",
            object="alpha_readout",
            formula="tau_readout*C_readout",
            source_ceiling_link="PVS2200_2_vector_contract",
            current_status="MISSING_READOUT_PPN_PROJECTION",
            required_parent_or_source_input="map from varied metric to measured GM/gamma readout",
            no_cancellation_policy="readout cannot absorb residual without proof",
            score_ready=False,
        ),
        base_row(
            component_id="PCC2200_6_total",
            component="absolute PPN residual vector",
            object="alpha_PPN_total_abs",
            formula="sum_abs(all_components)",
            source_ceiling_link="PVS2200_2_vector_contract",
            current_status="SOURCE_CEILING_READY_COMPONENTS_MISSING",
            required_parent_or_source_input="all components theorem-zero or numeric and sourced",
            no_cancellation_policy="pair cancellations forbidden for local-GR pass",
            score_ready=False,
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2200_0_hidden_route",
            gate="hidden invariant/no-hair route closes local scalar silence",
            status="BLOCKED_NONCLAIM",
            implication="1924/1925 prevent reusing O(C_hid)^inv=R or scalar no-hair as an active MTS theorem.",
        ),
        base_row(
            gate_id="CG2200_1_ppn_source_row",
            gate="Cassini PPN source row exists",
            status="PASS_NONCLAIM",
            implication="a real source-backed pressure row is staged, but only as gamma/proxy/vector target.",
        ),
        base_row(
            gate_id="CG2200_2_ppn_prediction",
            gate="MTS PPN vector prediction is score-ready",
            status="BLOCKED_NONCLAIM",
            implication="component rows lack Z_X, tau, range, source/current, support, boundary and readout projections.",
        ),
        base_row(
            gate_id="CG2200_3_local_gr_newton",
            gate="local GR/Newton recovery claim",
            status="BLOCKED_NONCLAIM",
            implication="no PPN/local-GR/Newton, WEP, R10, clock, or public claim follows from 2200.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2200_0_hidden_route",
            decision="DO_NOT_REPEAT_HIDDEN_TRIVIALITY_WITHOUT_NEW_PARENT_INPUT",
            rationale="2199 selected it, but 1924 and 1925 already show the exact missing clauses.",
            next_action="use hidden route only if a new parent owner/sign/source/boundary theorem appears",
        ),
        base_row(
            decision_id="DEC2200_1_ppn_route",
            decision="PROMOTE_PPN_VECTOR_SOURCE_CONTRACT_AS_NEXT_LOCAL_GR_OBJECT",
            rationale="Cassini gives real pressure and the vector is the invariant comparison object; raw c_g is not.",
            next_action="fill the PPN component owner/projection matrix one component at a time",
        ),
        base_row(
            decision_id="DEC2200_2_next",
            decision="MOVE_TO_PPN_COMPONENT_OWNER_MATRIX",
            rationale="the source ceiling is now explicit; the missing thing is the map from MTS parent variables to each PPN component.",
            next_action="2201 should derive or source the first PPN component owner row, starting with alpha_cg or readout.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2200_0_2201",
            selection_status="selected",
            target_file="2201-Y5-R2FR-PPN-component-owner-matrix-or-alpha-cg-source-row.md",
            target_script="scripts/Y5_R2FR_PPN_component_owner_matrix_or_alpha_cg_source_row_2201.py",
            objective="derive or source the first PPN vector component owner/projection row, without reducing the vector to raw c_g",
            success_condition="one component becomes theorem-zero or numeric/source-backed nonclaim with units, owner, projection, and no-cancellation placement",
            do_not_do="do not claim local GR, do not bind raw c_g, do not assume vector tails vanish, do not use pair cancellations",
        )
    ]


def write_branch_copies() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["ppn_vector_source_row"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["ppn_vector_source_row"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["ppn_component_contract"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        parse_ok, row_count, parse_detail = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=target.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_detail=parse_detail,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    hidden_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, detail: str) -> None:
        rows.append(
            base_row(
                validation_id=validation_id,
                status="PASS" if passed else "FAIL",
                detail=detail,
            )
        )

    add(
        "VAL2200_00_sources_exist",
        all(truthy(row["path_exists"]) for row in source_rows),
        f"{sum(truthy(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist",
    )
    add(
        "VAL2200_01_needles_found",
        all(truthy(row["needles_found"]) for row in source_rows),
        f"{sum(truthy(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found",
    )
    add(
        "VAL2200_02_hidden_not_repeated",
        any(row["current_result"] == "TARGET_SHARP_BUT_ALREADY_TESTED" for row in hidden_rows)
        and any(row["current_result"] == "EXACT_CONDITIONAL_THEOREM_NOT_PROMOTED" for row in hidden_rows),
        "hidden route synthesis cites 1924/1925 and refuses a duplicate theorem loop",
    )
    add(
        "VAL2200_03_ppn_source_positive",
        all(float(row["empirical_bound_value"]) > 0.0 for row in ppn_rows),
        "all PPN source/proxy bounds are positive numeric",
    )
    add(
        "VAL2200_04_proxy_not_direct",
        all(not truthy(row["direct_mts_component_bound"]) for row in ppn_rows),
        "Cassini rows are proxy/vector targets, not direct MTS component claims",
    )
    add(
        "VAL2200_05_component_contract",
        len(component_rows) == 7 and all(not truthy(row["score_ready"]) for row in component_rows),
        "seven PPN component rows staged; none score-ready",
    )
    add(
        "VAL2200_06_claim_gate",
        any(row["gate_id"] == "CG2200_1_ppn_source_row" and row["status"] == "PASS_NONCLAIM" for row in claim_rows)
        and all("CLAIM" not in row["status"] or row["status"].endswith("NONCLAIM") for row in claim_rows),
        "source row passes only as nonclaim and local-GR remains blocked",
    )
    add(
        "VAL2200_07_decision",
        any(row["decision"] == "MOVE_TO_PPN_COMPONENT_OWNER_MATRIX" for row in decision_rows_data),
        "decision selects PPN component owner matrix next",
    )
    add(
        "VAL2200_08_next_target",
        len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2200_0_2201",
        "2201 target selected",
    )
    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["hidden_route_synthesis"],
        OUTPUTS["ppn_vector_source_row"],
        OUTPUTS["ppn_component_contract"],
        OUTPUTS["claim_gate"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    parse_parts: list[str] = []
    parse_ok_all = True
    for path in generated_csvs:
        parse_ok, count, detail = csv_rows_parse(path)
        parse_ok_all = parse_ok_all and parse_ok and count > 0
        parse_parts.append(f"{path.name}:{count if parse_ok else detail}")
    add("VAL2200_09_csv_parse", parse_ok_all, "; ".join(parse_parts))
    add(
        "VAL2200_10_branch_copies",
        len(copy_rows) == 3 and all(truthy(row["copied"]) and truthy(row["parse_ok"]) for row in copy_rows),
        ";".join(str(row["target_path"]) for row in copy_rows),
    )
    all_generated_rows = [
        *source_rows,
        *hidden_rows,
        *ppn_rows,
        *component_rows,
        *claim_rows,
        *decision_rows_data,
        *next_rows,
        *copy_rows,
    ]
    add(
        "VAL2200_11_claim_flags_false",
        all(not truthy(row.get("valid_for_claim", False)) and not truthy(row.get("claim_allowed", False)) for row in all_generated_rows),
        "all generated rows keep valid_for_claim=false and claim_allowed=false",
    )
    add(
        "VAL2200_12_formalization_clean",
        not formalization_has_2200_artifacts(),
        "formalization-workbench has no 2200 artifacts",
    )
    add(
        "VAL2200_13_pycache_absent",
        not (ROOT / "scripts" / "__pycache__").exists(),
        str(ROOT / "scripts" / "__pycache__"),
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2200_OVERALL",
        overall,
        "2200 avoids a duplicate hidden-triviality loop and stages the Cassini/PPN vector source contract as nonclaim",
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    hidden_rows: list[dict[str, Any]],
    ppn_rows: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_data: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2200 - Y5/R2FR Hidden Invariant Algebra Triviality Or PPN Vector Source Row",
        "",
        "## Current Verdict",
        "",
        "2200 takes the 2199 target seriously without circling the same wall. The hidden-invariant route is real and high leverage, but 1924 and 1925 already show why it is not currently promotable: hidden generator debts survive, and the scalar no-hair identity only becomes an MTS theorem after parent owner, sign, source, boundary, zero-mode, and readout clauses close together.",
        "",
        "So this checkpoint selects the local-GR-facing fallback: a first source-backed PPN vector source row. Cassini supplies real pressure, but only as a gamma/proxy/vector ceiling. It is not a direct bound on raw `c_g`, not a PPN pass, and not a local GR/Newton recovery claim.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Hidden Route Synthesis",
        "",
        md_table(hidden_rows, ["route_id", "route", "current_result", "evidence", "obstruction", "next_effect", "valid_for_claim"]),
        "",
        "## PPN Vector Source Row",
        "",
        md_table(
            ppn_rows,
            [
                "source_row_id",
                "arena",
                "observable",
                "empirical_bound_value",
                "empirical_bound_units",
                "translation_status",
                "direct_mts_component_bound",
                "required_inputs_for_claim",
                "score_ready",
                "valid_for_claim",
            ],
        ),
        "",
        "## PPN Component Contract",
        "",
        md_table(
            component_rows,
            [
                "component_id",
                "component",
                "object",
                "formula",
                "current_status",
                "required_parent_or_source_input",
                "no_cancellation_policy",
                "score_ready",
                "valid_for_claim",
            ],
        ),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_data, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
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
        md_table(validation_rows_data, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Interpretation",
        "",
        "This is a useful shift in attack. The derivation route has not been abandoned; it has been made exact and parked until the parent action can sign its premises. The active local-GR comparison route is now the full PPN vector under a Cassini source ceiling, with no raw-`c_g` shortcut and no cancellation games.",
        "",
        "Best next attack: build the `2201` PPN component owner matrix and try to make one component theorem-zero or numeric/source-backed. That is the most direct way to move from beautiful conditional local-GR math toward an actual GR/Newton recovery test.",
    ]
    DOC.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    hidden_rows = hidden_route_synthesis_rows()
    ppn_rows = ppn_vector_source_rows()
    component_rows = ppn_component_contract_rows()
    claim_rows = claim_gate_rows()
    decision_rows_data = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["hidden_route_synthesis"], hidden_rows)
    write_csv(OUTPUTS["ppn_vector_source_row"], ppn_rows)
    write_csv(OUTPUTS["ppn_component_contract"], component_rows)
    write_csv(OUTPUTS["claim_gate"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows_data)
    write_csv(OUTPUTS["next_target"], next_rows)

    copy_rows = write_branch_copies()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_data = validation_rows(
        source_rows,
        hidden_rows,
        ppn_rows,
        component_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_data)
    write_doc(
        source_rows,
        hidden_rows,
        ppn_rows,
        component_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
        validation_rows_data,
    )


if __name__ == "__main__":
    main()
