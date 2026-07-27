from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2203"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2203-Y5-R2FR-fixed-before-readout-PPN-map-or-measured-GM-obstruction-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2203_SOURCE_REGISTER.csv",
    "fixed_before_readout": OUT / "P8_Y5_PARENT_QLOC_2203_FIXED_BEFORE_READOUT_MAP_ATTEMPT.csv",
    "measured_gm_obstruction": OUT / "P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "alpha_readout": OUT / "P8_Y5_PARENT_QLOC_2203_ALPHA_READOUT_ROW.csv",
    "route_selection": OUT / "P8_Y5_PARENT_QLOC_2203_ROUTE_SELECTION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2203_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2203_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2203_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2203_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2203_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2203_FIXED_READOUT_BLOCKED_MEASURED_GM_OBSTRUCTION_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2203_MEASURED_GM_OBSTRUCTION_VECTOR_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_FIXED_BEFORE_READOUT_MAP_ATTEMPT_2203_NONCLAIM.csv",
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


def formalization_has_2203_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2203-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2203*",
        "*P8_Y5_BRR545_2203*",
        "*Y5_R2FR_fixed_before_readout_PPN_map_or_measured_GM_obstruction_row_2203*",
        "*JR2203*",
        "*PARENT_QLOC_FIXED_BEFORE_READOUT_MAP_ATTEMPT_2203*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2202_doc",
            ROOT / "2202-Y5-R2FR-alpha-cg-projection-clause-or-readout-zero-theorem.md",
            ["NEXT2202_0_2203", "SEL2202_1_readout", "VAL2202_OVERALL"],
            "2202 handoff into fixed-before-readout PPN map.",
        ),
        (
            "2202_next",
            OUT / "P8_Y5_PARENT_QLOC_2202_NEXT_TARGET.csv",
            ["NEXT2202_0_2203", "do not absorb residuals", "measured-GM"],
            "Machine-readable 2203 target and guardrails.",
        ),
        (
            "1012_doc",
            ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
            ["Y5O1012_8_verdict", "Y5O1012_0_same_frame", "Y5O1012_6_no_absorption_cheat"],
            "Measured-GM/source-normalization owner theorem attempt.",
        ),
        (
            "1013_doc",
            ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            ["OBS1013_1_PiM_commutator", "CG1013_4_Newton_local_GR", "DEC1013_0_exact_obstruction_is_best_object"],
            "Exact measured-GM obstruction vector and Newton/local-GR block.",
        ),
        (
            "1013_vector_csv",
            OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
            ["OBS1013_7_calibration_PPN_tail", "retained_unfilled", "Delta_cal + Delta_PPN"],
            "Machine-readable measured-GM obstruction vector reused by 2203.",
        ),
        (
            "1014_doc",
            ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            ["PCT1014_7_verdict", "PRS1014_1_topological_Hilbert_equality", "DEC1014_2_next_R_eq"],
            "Topological-Hilbert equality selected as the next root after commutator obstruction.",
        ),
        (
            "462_doc",
            ROOT / "462-charge-current-equality-direct-derivation-attempt.md",
            ["direct_residual_identity", "Delta_cal", "Delta_PPN"],
            "Charge-current equality reduces to an explicit residual identity, not equality.",
        ),
        (
            "465_doc",
            ROOT / "465-constant-GM-derivative-hair-fill-gate.md",
            ["CGM0_master_identity", "CGM7_second_order_beta_residue", "constant_GM_derivative_hair_gate"],
            "Derivative hair law for measured GM and local PPN promotion.",
        ),
        (
            "2200_vector_source",
            OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
            ["PVS2200_2_vector_contract", "NONCLAIM_VECTOR_TARGET", "0.005788015401465051"],
            "Absolute PPN vector ceiling that readout cannot hide by calibration.",
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


def fixed_before_readout_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            clause_id="FBR2203_0_target",
            clause="fixed parent-to-observed PPN functor",
            mathematical_form="(g_parent,J_H,Pi_M,G_eff,theta_parent) -> (g_obs,gamma_obs,beta_obs,GM_obs) before local-test fitting",
            required_statement="observed metric and measured source normalization are fixed functors of parent variables before PPN residual comparison",
            current_evidence="2202 sharpens this as the next route, but no parent readout functor certificate is present",
            status="TARGET_SHARP_NOT_DERIVED",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="FBR2203_1_same_frame",
            clause="same frame for source, clocks and orbit",
            mathematical_form="S_matter[psi,e_obs] defines J_H[e_obs], while e_obs also defines clocks, rods and orbital readout",
            required_statement="one observed coframe is parent-selected for matter variation, source current, clocks and orbits",
            current_evidence="Y5O1012_0_same_frame is only conditional_not_parent_derived",
            status="CONDITIONAL_NOT_PARENT_DERIVED",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="FBR2203_2_PiM_origin",
            clause="Pi_M parent origin before readout",
            mathematical_form="Pi_M: J_H -> H^2_abs(Sigma_ext) mass-flux class, fixed before measured-GM/orbit fitting",
            required_statement="Pi_M is not a post-readout mass mask",
            current_evidence="Y5O1012_2_PiM_parent_origin remains not_parent_derived; PCT1014 retains projector variation",
            status="NOT_PARENT_DERIVED",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="FBR2203_3_flux_closure",
            clause="projected source flux closure",
            mathematical_form="d(Pi_M J_H)=0 or exact obstruction vector is theorem-zero/bounded",
            required_statement="measured mass is radially/time stable and cannot leak into alpha(lambda), Gdot or beta/gamma rows",
            current_evidence="1013 constructs obstruction vector; all rows retained_unfilled",
            status="EXACT_OBSTRUCTION_ACTIVE_NOT_ZERO",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="FBR2203_4_worldtube_glue",
            clause="same compact source worldtube",
            mathematical_form="M_source[W]=integral_S Q_M[tau]=M_eff, with same exterior charge used by Poisson/Gauss/orbit",
            required_statement="closed charge equals the observed Hilbert compact-source mass, not merely some conserved topological charge",
            current_evidence="Y5O1012_4_worldtube_glue and DEC1013_1_topological_route_not_enough keep this unsigned",
            status="NOT_DERIVED_CORE_MISSING_PIECE",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="FBR2203_5_no_absorption",
            clause="no measured-GM/gamma absorption cheat",
            mathematical_form="calibration/readout constants are fixed before Cassini, GM, beta/gamma and orbit residuals are evaluated",
            required_statement="readout cannot cancel alpha_cg or vector tails after seeing the data",
            current_evidence="Y5O1012_6_no_absorption_cheat is a written rule but not satisfied by parent rows",
            status="RULE_WRITTEN_NOT_SATISFIED",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="FBR2203_6_Poisson_Gauss_orbit",
            clause="same charge sources Newton and PPN",
            mathematical_form="nabla^2 Phi=4 pi G_ref rho_H, a_r=-G_ref M_ref/r^2, and gamma/beta are read from the same fixed g_obs",
            required_statement="one source charge feeds Poisson/Gauss/orbit and second-order PPN without residual source hair",
            current_evidence="Y5O1012_7 is conditional_not_parent_derived; CGM7 blocks local-GR promotion after first order",
            status="CONDITIONAL_NOT_PARENT_DERIVED",
            blocks_prediction=True,
        ),
        base_row(
            clause_id="FBR2203_7_verdict",
            clause="fixed-before-readout PPN map",
            mathematical_form="FBR2203_0 through FBR2203_6 all parent-signed and no obstruction vector rows retained",
            required_statement="measured-GM and PPN readout are fixed from the parent before any fit/comparison",
            current_evidence="source identity exists only as residual/obstruction vector, not as a theorem-zero functor",
            status="FIXED_BEFORE_READOUT_MAP_NOT_DERIVED",
            blocks_prediction=True,
        ),
    ]


def measured_gm_obstruction_rows() -> list[dict[str, Any]]:
    source_csv = OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv"
    if not source_csv.exists():
        return [
            base_row(
                obstruction_id="MGV2203_MISSING_SOURCE",
                symbol="MISSING_1013_VECTOR",
                definition="1013 measured-GM obstruction vector not found",
                value_or_theorem="MISSING_SOURCE_PATH",
                units="MISSING",
                affected_rows="R4;R10;R11",
                current_status="source_missing",
                score_ready=False,
                source_path=str(source_csv),
            )
        ]
    rows: list[dict[str, Any]] = []
    with source_csv.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for source_row in reader:
            source_id = source_row.get("obstruction_id", "")
            suffix = source_id.split("_", 1)[1] if "_" in source_id else source_id
            rows.append(
                base_row(
                    obstruction_id=f"MGV2203_{suffix}",
                    source_obstruction_id=source_id,
                    symbol=source_row.get("symbol", ""),
                    definition=source_row.get("definition", ""),
                    value_or_theorem=source_row.get("value_or_theorem", ""),
                    units=source_row.get("units", ""),
                    affected_rows=source_row.get("affected_rows", ""),
                    source_path=source_row.get("source_path", ""),
                    current_status=source_row.get("current_status", ""),
                    readout_role="blocks fixed-before-readout GM/PPN map until theorem-zero or source-backed bound exists",
                    score_ready=False,
                )
            )
    return rows


def alpha_readout_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="ARW2203_0_alpha_readout",
            object="alpha_readout",
            formula="tau_readout*C_readout",
            source_ceiling="must fit inside absolute PPN vector target before any cancellation with alpha_cg",
            prediction_value="MISSING_FIXED_READOUT_FUNCTOR",
            units="dimensionless_PPN_vector_component",
            observable_links="Cassini_gamma;measured_GM;orbital_source_normalization;PPN_beta_gamma;Gdot;R10_alpha_lambda",
            status="READOUT_COMPONENT_RETAINED_NONCLAIM",
            score_ready=False,
            issue="without fixed readout/source normalization, local tests can hide or mimic source hair",
        ),
        base_row(
            row_id="ARW2203_1_no_cancellation_guard",
            object="alpha_readout_plus_alpha_cg",
            formula="abs(alpha_PPN_total) <= abs(alpha_cg)+abs(alpha_dis)+abs(alpha_nonH)+abs(alpha_support)+abs(alpha_boundary)+abs(alpha_readout)",
            source_ceiling="0.005788015401465051 vector proxy from 2200/2201",
            prediction_value="MISSING_VECTOR_COMPONENTS",
            units="dimensionless",
            observable_links="Cassini_gamma;Shapiro_delay;PPN_vector",
            status="NO_CANCELLATION_SCORING_ONLY",
            score_ready=False,
            issue="readout cannot be tuned to subtract alpha_cg; components must be zeroed or bounded separately",
        ),
    ]


def route_selection_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="SEL2203_0_fixed_readout",
            route="fixed-before-readout PPN theorem",
            selection_status="attempted_not_derived",
            reason="same-frame, Pi_M ownership, flux closure, worldtube glue, no-absorption, and Poisson/Gauss/PPN clauses remain unsigned",
            next_use="keep as the readout contract; do not promote alpha_readout to zero",
        ),
        base_row(
            route_id="SEL2203_1_measured_GM_vector",
            route="measured-GM obstruction vector",
            selection_status="staged_nonclaim",
            reason="the exact obstruction vector is the safest object: it says exactly what must be theorem-zero or bounded",
            next_use="score or derive each source-normalization obstruction rather than treating GM as fitted away",
        ),
        base_row(
            route_id="SEL2203_2_topological_Hilbert",
            route="topological-Hilbert equality or R_eq first row",
            selection_status="selected_next",
            reason="1014 identifies R_eq as the root wrong-conserved-object blocker after Pi_M commutator attempts",
            next_use="derive Pi_M J_H = J_M_top + dB_zero for the same compact source worldtube, or stage R_eq source row",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2203_0_fixed_readout_map",
            gate="fixed-before-readout map is parent-derived",
            status="BLOCKED_NONCLAIM",
            implication="alpha_readout cannot be set to zero or used as a derived PPN cancellation.",
        ),
        base_row(
            gate_id="CG2203_1_measured_GM_closure",
            gate="measured-GM/source-normalization closure",
            status="BLOCKED_NONCLAIM",
            implication="Newton/source-normalization and local-GR gates stay closed while obstruction rows remain unfilled.",
        ),
        base_row(
            gate_id="CG2203_2_readout_absorption",
            gate="post-fit readout absorption is forbidden",
            status="PASS_GUARDRAIL_NONCLAIM",
            implication="the no-cheat rule is installed, but not a proof of GR reduction.",
        ),
        base_row(
            gate_id="CG2203_3_obstruction_rows_score_ready",
            gate="measured-GM obstruction vector has numeric/theorem rows",
            status="BLOCKED_NONCLAIM",
            implication="all rows are retained_unfilled and valid_for_claim=false.",
        ),
        base_row(
            gate_id="CG2203_4_local_gr_newton",
            gate="local GR/Newton recovery claim",
            status="BLOCKED_NONCLAIM",
            implication="no local-GR, Newton, PPN, WEP, R10, clock, orbital or public claim follows from 2203.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2203_0_fixed_readout_result",
            decision="FIXED_BEFORE_READOUT_MAP_NOT_DERIVED",
            rationale="the contract is now explicit, but the current corpus still has no parent-signed map from source/current/readout variables to observed gamma and measured GM.",
            next_action="retain alpha_readout as a nonclaim vector component",
        ),
        base_row(
            decision_id="DEC2203_1_obstruction_result",
            decision="MEASURED_GM_OBSTRUCTION_VECTOR_IS_ACTIVE_OBJECT",
            rationale="1013/462/465 convert vague measured-GM language into exact obstruction terms and derivative-hair rows.",
            next_action="derive or source the obstruction terms, beginning with topological-Hilbert equality R_eq",
        ),
        base_row(
            decision_id="DEC2203_2_next",
            decision="MOVE_TO_TOPOLOGICAL_HILBERT_EQUALITY_OR_R_EQ_FIRST_ROW",
            rationale="fixed topology can only help if the closed topological current is proved to equal Pi_M J_H for the same compact source worldtube.",
            next_action="2204 should derive Pi_M J_H = J_M_top + dB_zero or write an R_eq source-ready nonclaim row",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2203_0_2204",
            selection_status="selected",
            target_file="2204-Y5-R2FR-topological-Hilbert-equality-or-R-eq-first-row.md",
            target_script="scripts/Y5_R2FR_topological_Hilbert_equality_or_R_eq_first_row_2204.py",
            objective="derive Pi_M J_H = J_M_top + dB_zero from the same compact-source worldtube, or stage a source-backed R_eq/readout obstruction row as nonclaim",
            success_condition="either topological-Hilbert equality is parent-signed, or R_eq becomes an explicit source-ready obstruction row with units, normalization, and no claim credit",
            do_not_do="do not use a closed wrong topological charge, reference-only zero, fitted GM calibration, post-readout equality multiplier, cancellation, or local-GR claim",
        )
    ]


def write_branch_copies() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["route_selection"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["measured_gm_obstruction"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["fixed_before_readout"], BRANCH_COPIES["beta_docs"]),
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
    fixed_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if passed else "FAIL", detail=detail))

    add("VAL2203_00_sources_exist", all(truthy(r["path_exists"]) for r in source_rows), f"{sum(truthy(r['path_exists']) for r in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2203_01_needles_found", all(truthy(r["needles_found"]) for r in source_rows), f"{sum(truthy(r['needles_found']) for r in source_rows)}/{len(source_rows)} source needle sets found")
    add("VAL2203_02_fixed_map_blocks", len(fixed_rows) == 8 and any(r["clause_id"] == "FBR2203_7_verdict" and r["status"] == "FIXED_BEFORE_READOUT_MAP_NOT_DERIVED" for r in fixed_rows), "fixed-before-readout map is attempted and not promoted")
    add("VAL2203_03_obstruction_vector", len(obstruction_rows) == 8 and all(not truthy(r.get("score_ready", False)) for r in obstruction_rows), "eight measured-GM obstruction rows retained nonclaim")
    add("VAL2203_04_alpha_readout", any(r["row_id"] == "ARW2203_0_alpha_readout" and r["status"] == "READOUT_COMPONENT_RETAINED_NONCLAIM" for r in alpha_rows), "alpha_readout retained as vector component")
    add("VAL2203_05_no_cancellation_guard", any(r["row_id"] == "ARW2203_1_no_cancellation_guard" and r["status"] == "NO_CANCELLATION_SCORING_ONLY" for r in alpha_rows), "readout cannot cancel alpha_cg")
    add("VAL2203_06_route_selection", any(r["route_id"] == "SEL2203_2_topological_Hilbert" and r["selection_status"] == "selected_next" for r in route_rows), "topological-Hilbert/R_eq selected next")
    add("VAL2203_07_claim_gate", any(r["gate_id"] == "CG2203_4_local_gr_newton" and r["status"] == "BLOCKED_NONCLAIM" for r in claim_rows), "local-GR remains blocked")
    add("VAL2203_08_decision", any(r["decision"] == "MOVE_TO_TOPOLOGICAL_HILBERT_EQUALITY_OR_R_EQ_FIRST_ROW" for r in decision_rows_data), "decision selects 2204")
    add("VAL2203_09_next_target", len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2203_0_2204", "2204 target selected")

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["fixed_before_readout"],
        OUTPUTS["measured_gm_obstruction"],
        OUTPUTS["alpha_readout"],
        OUTPUTS["route_selection"],
        OUTPUTS["claim_gate"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    parse_ok_all = True
    parse_parts: list[str] = []
    for path in generated_csvs:
        parse_ok, count, detail = csv_rows_parse(path)
        parse_ok_all = parse_ok_all and parse_ok and count > 0
        parse_parts.append(f"{path.name}:{count if parse_ok else detail}")
    add("VAL2203_10_csv_parse", parse_ok_all, "; ".join(parse_parts))
    add("VAL2203_11_branch_copies", len(copy_rows) == 3 and all(truthy(r["copied"]) and truthy(r["parse_ok"]) for r in copy_rows), ";".join(str(r["target_path"]) for r in copy_rows))

    all_generated_rows = [
        *source_rows,
        *fixed_rows,
        *obstruction_rows,
        *alpha_rows,
        *route_rows,
        *claim_rows,
        *decision_rows_data,
        *next_rows,
        *copy_rows,
    ]
    add("VAL2203_12_claim_flags_false", all(not truthy(r.get("valid_for_claim", False)) and not truthy(r.get("claim_allowed", False)) for r in all_generated_rows), "all generated rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2203_13_score_flags_false", all(not truthy(r.get("score_ready", False)) for r in [*obstruction_rows, *alpha_rows]), "no obstruction/readout row is score-ready")
    add("VAL2203_14_formalization_clean", not formalization_has_2203_artifacts(), "formalization-workbench has no 2203 artifacts")
    add("VAL2203_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), str(ROOT / "scripts" / "__pycache__"))
    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2203_OVERALL", overall, "2203 turns readout into an explicit nonclaim obstruction vector and selects topological-Hilbert/R_eq next")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    fixed_rows: list[dict[str, Any]],
    obstruction_rows: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_data: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2203 - Y5/R2FR Fixed-Before-Readout PPN Map Or Measured-GM Obstruction Row",
        "",
        "## Current Verdict",
        "",
        "2203 tries the readout route directly. The fixed-before-readout map is now explicit, but it is not derived: the current corpus still lacks the parent-signed functor from source/current/readout variables to observed `gamma`, `beta`, clocks, or measured `GM` before local-test fitting.",
        "",
        "The useful result is therefore not a local-GR pass. It is a cleaner obstruction: `alpha_readout` is retained as its own nonclaim PPN-vector component, and the measured-GM obstruction vector from 1013 is promoted into the R2FR local-GR branch as the object to derive or bound. No readout component may be used to cancel `alpha_cg`.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Fixed-Before-Readout Map Attempt",
        "",
        md_table(fixed_rows, ["clause_id", "clause", "mathematical_form", "status", "blocks_prediction", "valid_for_claim"]),
        "",
        "## Measured-GM Obstruction Vector",
        "",
        md_table(obstruction_rows, ["obstruction_id", "source_obstruction_id", "symbol", "value_or_theorem", "units", "current_status", "score_ready", "valid_for_claim"]),
        "",
        "## Alpha-Readout Row",
        "",
        md_table(alpha_rows, ["row_id", "object", "formula", "prediction_value", "status", "score_ready", "issue", "valid_for_claim"]),
        "",
        "## Route Selection",
        "",
        md_table(route_rows, ["route_id", "route", "selection_status", "reason", "next_use", "valid_for_claim"]),
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
        "This is progress, but it is the knife-work kind, not the fireworks kind. The route is no longer allowed to say `measured GM absorbs it` or `readout fixes it later`. If MTS is going to reduce to Newton/GR, the measured source and observed metric map must be parent-fixed before the comparison.",
        "",
        "Best next attack: `2204` should derive `Pi_M J_H = J_M_top + dB_zero` from the same compact-source worldtube, or write the first source-ready `R_eq` obstruction row. That is the shortest honest path toward turning fixed topology into actual measured-GM/Newton/PPN evidence.",
    ]
    DOC.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    fixed_rows = fixed_before_readout_rows()
    obstruction_rows = measured_gm_obstruction_rows()
    alpha_rows = alpha_readout_rows()
    route_rows = route_selection_rows()
    claim_rows = claim_gate_rows()
    decision_rows_data = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["fixed_before_readout"], fixed_rows)
    write_csv(OUTPUTS["measured_gm_obstruction"], obstruction_rows)
    write_csv(OUTPUTS["alpha_readout"], alpha_rows)
    write_csv(OUTPUTS["route_selection"], route_rows)
    write_csv(OUTPUTS["claim_gate"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows_data)
    write_csv(OUTPUTS["next_target"], next_rows)
    copy_rows = write_branch_copies()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_data = validation_rows(
        source_rows,
        fixed_rows,
        obstruction_rows,
        alpha_rows,
        route_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_data)
    write_doc(
        source_rows,
        fixed_rows,
        obstruction_rows,
        alpha_rows,
        route_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
        validation_rows_data,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
