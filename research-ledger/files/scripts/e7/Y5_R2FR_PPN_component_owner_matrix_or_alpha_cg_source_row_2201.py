from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2201"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2201-Y5-R2FR-PPN-component-owner-matrix-or-alpha-cg-source-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2201_SOURCE_REGISTER.csv",
    "component_owner_matrix": OUT / "P8_Y5_PARENT_QLOC_2201_PPN_COMPONENT_OWNER_MATRIX.csv",
    "alpha_cg_source_row": OUT / "P8_Y5_PARENT_QLOC_2201_ALPHA_CG_SOURCE_ROW.csv",
    "alpha_cg_projection_gate": OUT / "P8_Y5_PARENT_QLOC_2201_ALPHA_CG_PROJECTION_GATE.csv",
    "readout_competitor_gate": OUT / "P8_Y5_PARENT_QLOC_2201_READOUT_COMPETITOR_GATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2201_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2201_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2201_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2201_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2201_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2201_ALPHA_CG_SOURCE_ROW_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2201_PPN_COMPONENT_OWNER_MATRIX_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_ALPHA_CG_PROJECTION_GATE_2201_NONCLAIM.csv",
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
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2201_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2201-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2201*",
        "*P8_Y5_BRR545_2201*",
        "*Y5_R2FR_PPN_component_owner_matrix_or_alpha_cg_source_row_2201*",
        "*JR2201*",
        "*PARENT_QLOC_ALPHA_CG_PROJECTION_GATE_2201*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2200_doc",
            ROOT / "2200-Y5-R2FR-hidden-invariant-algebra-triviality-or-PPN-vector-source-row.md",
            ["NEXT2200_0_2201", "PCC2200_0_cg", "VAL2200_OVERALL"],
            "2200 selected a PPN component owner matrix, with alpha_cg or readout as first target.",
        ),
        (
            "2200_next",
            OUT / "P8_Y5_PARENT_QLOC_2200_NEXT_TARGET.csv",
            ["NEXT2200_0_2201", "do not bind raw c_g", "do not use pair cancellations"],
            "Machine-readable 2201 handoff.",
        ),
        (
            "2200_component_contract",
            OUT / "P8_Y5_PARENT_QLOC_2200_PPN_COMPONENT_CONTRACT.csv",
            ["PCC2200_0_cg", "PCC2200_5_readout", "PCC2200_6_total"],
            "Component envelope to be converted into owner/projection rows.",
        ),
        (
            "2200_vector_source",
            OUT / "P8_Y5_PARENT_QLOC_2200_PPN_VECTOR_SOURCE_ROW.csv",
            ["PVS2200_0_cassini_gamma_source", "PVS2200_2_vector_contract", "0.005788015401465051"],
            "Cassini source ceiling and alpha proxy target.",
        ),
        (
            "2161_doc",
            ROOT / "2161-Y5-R2FR-parent-NX-lambda-extraction-or-PPN-vector-envelope.md",
            ["N_X/Lambda Extraction Attempt", "MISSING_ZX_TAU_RANGE", "VAL2161_OVERALL"],
            "Shows alpha_cg cannot be reduced to raw c_g because normalization/range are missing.",
        ),
        (
            "2162_doc",
            ROOT / "2162-Y5-R2FR-minimal-parent-X-sector-action-clause-or-PPN-vector-fill.md",
            ["PPN/Local Residual Vector Fill", "PVF2162_0_cg", "VAL2162_OVERALL"],
            "Confirms propagating X-sector is closure/backstop and finite vector rows are acquisition required.",
        ),
        (
            "1852_doc",
            ROOT / "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
            ["PPN Observable Bound", "CGB1852_1_cg_conditional", "VAL1852_OVERALL"],
            "Original Cassini-to-alpha proxy and conditional c_g translation gate.",
        ),
        (
            "1312_doc",
            ROOT / "1312-Y5-R10-RAB-b-alpha-no-vertex-or-source-backed-coefficient.md",
            ["b_alpha No-F2 Proof Audit", "B_ALPHA_THEOREM_ZERO_NOT_DERIVED", "VAL1312_11_overall"],
            "Alpha/EM branch audit proving no hidden-visible coefficient shortcut is available.",
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


def component_owner_matrix_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            component_id="PCM2201_0_alpha_cg",
            rank=1,
            selected_first=True,
            component="common conformal coupling",
            object="alpha_cg",
            formula="tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)",
            owner_candidate="same-branch Xhat plus universal common matter frame",
            owner_status="MISSING_PARENT_OWNER_AND_ZX",
            projection_status="MISSING_TAU_PPN_RANGE_SCREENING",
            source_ceiling_status="CASSINI_PROXY_CEILING_AVAILABLE_NONCLAIM",
            reason_for_rank="cleanest source ceiling and exposes the normalization/range bottleneck directly",
            score_ready=False,
        ),
        base_row(
            component_id="PCM2201_1_readout",
            rank=2,
            selected_first=False,
            component="measured-G/readout calibration tail",
            object="alpha_readout",
            formula="tau_readout*C_readout",
            owner_candidate="variation-before-readout map from parent metric/source variables to measured GM/gamma",
            owner_status="MISSING_READOUT_FUNCTOR",
            projection_status="MISSING_MEASURED_G_GAMMA_MAP",
            source_ceiling_status="CASSINI_OBSERVABLE_AVAILABLE_BUT_NO_MTS_MAP",
            reason_for_rank="potential theorem-zero route, but less numeric until the readout functor is signed",
            score_ready=False,
        ),
        base_row(
            component_id="PCM2201_2_nonH",
            rank=3,
            selected_first=False,
            component="non-Hilbert/source-current tail",
            object="alpha_nonH",
            formula="tau_nonH*q_nonH",
            owner_candidate="parent source-current conservation law",
            owner_status="MISSING_SOURCE_CURRENT_OWNER",
            projection_status="MISSING_NONHILBERT_PPN_MAP",
            source_ceiling_status="NO_COMPONENT_NUMERIC_SOURCE",
            reason_for_rank="important for Newton/source normalization, but not first because no direct component ceiling exists",
            score_ready=False,
        ),
        base_row(
            component_id="PCM2201_3_disformal",
            rank=4,
            selected_first=False,
            component="disformal/preferred-frame tail",
            object="alpha_dis",
            formula="tau_dis*b_dis",
            owner_candidate="matter metric expansion beyond common conformal frame",
            owner_status="MISSING_MATTER_METRIC_EXPANSION",
            projection_status="MISSING_PREFERRED_FRAME_PPN_MAP",
            source_ceiling_status="PPN_ALPHA1_ALPHA2_SOURCES_EXIST_BUT_NOT_MAPPED_HERE",
            reason_for_rank="dangerous but second-order until common/readout/source maps are organized",
            score_ready=False,
        ),
        base_row(
            component_id="PCM2201_4_support_domain",
            rank=5,
            selected_first=False,
            component="support/domain local-projection tail",
            object="alpha_support_domain",
            formula="tau_support*Delta_W_support + tau_domain*q_domain",
            owner_candidate="finite-source support and representative-domain rule",
            owner_status="MISSING_SUPPORT_DOMAIN_OWNER",
            projection_status="MISSING_FINITE_SOURCE_PPN_MAP",
            source_ceiling_status="NO_COMPONENT_NUMERIC_SOURCE",
            reason_for_rank="must be bounded for local labs, but less directly Cassini-owned",
            score_ready=False,
        ),
        base_row(
            component_id="PCM2201_5_boundary",
            rank=6,
            selected_first=False,
            component="boundary/local flux tail",
            object="alpha_boundary",
            formula="tau_boundary*q_boundary",
            owner_candidate="fixed or zero local boundary flux theorem",
            owner_status="MISSING_BOUNDARY_FLUX_THEOREM",
            projection_status="MISSING_BOUNDARY_PPN_MAP",
            source_ceiling_status="NO_COMPONENT_NUMERIC_SOURCE",
            reason_for_rank="no plateau axiom allowed; needs parent boundary theorem before scoring",
            score_ready=False,
        ),
        base_row(
            component_id="PCM2201_6_total_abs",
            rank=7,
            selected_first=False,
            component="absolute PPN residual vector",
            object="alpha_PPN_total_abs",
            formula="sum_abs(alpha_cg,alpha_readout,alpha_nonH,alpha_dis,alpha_support_domain,alpha_boundary)",
            owner_candidate="component-complete no-cancellation vector",
            owner_status="COMPONENT_OWNERS_MISSING",
            projection_status="SOURCE_CEILING_READY_COMPONENTS_MISSING",
            source_ceiling_status="CASSINI_PROXY_CEILING_AVAILABLE_NONCLAIM",
            reason_for_rank="acceptance object after components are filled, not a first component",
            score_ready=False,
        ),
    ]


def alpha_cg_source_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="ACS2201_0_alpha_cg_target",
            selected_component="alpha_cg",
            observable_arena="PPN/Cassini/Shapiro",
            source_observable="gamma_minus_1",
            source_bound_value=6.7e-5,
            source_bound_units="dimensionless",
            translated_ceiling_object="abs(alpha_cg_contribution)",
            translated_ceiling_value=0.005788015401465051,
            translated_ceiling_units="dimensionless",
            formula="abs(tau_PPN*S_PPN(lambda_X,env)*c_g/sqrt(Z_X)) <= 0.005788015401465051 only if all other PPN vector components are theorem-zero or separately bounded",
            owner_required="same-branch Xhat, Z_X, lambda_X, tau_PPN, S_PPN, c_g",
            owner_status="MISSING_PARENT_OWNER_AND_PROJECTION",
            source_backed=True,
            direct_mts_prediction=False,
            score_ready=False,
            no_cancellation_placement="single absolute contribution inside alpha_PPN_total_abs; cannot borrow cancellation from other components",
        ),
        base_row(
            row_id="ACS2201_1_raw_cg_refusal",
            selected_component="raw_c_g",
            observable_arena="PPN/Cassini/Shapiro",
            source_observable="gamma_minus_1",
            source_bound_value=6.7e-5,
            source_bound_units="dimensionless",
            translated_ceiling_object="raw_c_g",
            translated_ceiling_value="MISSING_ZX_TAU_RANGE",
            translated_ceiling_units="per_Xhat_normalization",
            formula="abs(c_g) <= alpha_proxy*sqrt(Z_X)/(abs(tau_PPN*S_PPN)) only after normalization/range/projection gates",
            owner_required="Z_X, tau_PPN, S_PPN(lambda_X,env), vector tail control",
            owner_status="REFUSED_NOT_INVARIANT",
            source_backed=True,
            direct_mts_prediction=False,
            score_ready=False,
            no_cancellation_placement="raw c_g is excluded from comparison objects",
        ),
    ]


def alpha_cg_projection_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="ACG2201_0_common_frame",
            requirement="universal common matter frame",
            needed_statement="ordinary matter sees A_g(Xhat)^2 g_E with no disformal/species/readout split at same PPN order",
            current_status="NOT_PARENT_SIGNED",
            blocks_score=True,
        ),
        base_row(
            gate_id="ACG2201_1_same_branch_owner",
            requirement="same-branch Xhat owner",
            needed_statement="the same Xhat owns c_g, Z_X, M_X^2, lambda_X, tau_PPN and source/readout terms",
            current_status="MISSING_PARENT_OWNER",
            blocks_score=True,
        ),
        base_row(
            gate_id="ACG2201_2_normalization",
            requirement="positive Z_X/canonical normalization",
            needed_statement="Z_X is parent-owned, positive, unit-fixed and cannot be rescaled away",
            current_status="MISSING_ZX",
            blocks_score=True,
        ),
        base_row(
            gate_id="ACG2201_3_range_screening",
            requirement="solar-system range/screening transfer",
            needed_statement="S_PPN(lambda_X,env) is derived for Cassini geometry from M_X^2/lambda_X and local environment",
            current_status="MISSING_LAMBDA_X_AND_S_PPN",
            blocks_score=True,
        ),
        base_row(
            gate_id="ACG2201_4_tau_PPN",
            requirement="PPN projection coefficient",
            needed_statement="tau_PPN maps the parent residual to the observed Cassini gamma channel",
            current_status="MISSING_TAU_PPN",
            blocks_score=True,
        ),
        base_row(
            gate_id="ACG2201_5_vector_tails",
            requirement="all other vector components theorem-zero or bounded",
            needed_statement="alpha_dis, alpha_nonH, alpha_support_domain, alpha_boundary and alpha_readout are zero or independently bounded",
            current_status="VECTOR_TAILS_UNCONTROLLED",
            blocks_score=True,
        ),
        base_row(
            gate_id="ACG2201_6_verdict",
            requirement="alpha_cg score-ready component",
            needed_statement="ACG2201_0 through ACG2201_5 all pass",
            current_status="BLOCKED_NONCLAIM_SOURCE_ROW_ONLY",
            blocks_score=True,
        ),
    ]


def readout_competitor_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            readout_id="RCG2201_0_candidate",
            route="readout theorem-zero competitor",
            possible_zero_theorem="variation-before-readout plus fixed measured-G/gamma functor could remove alpha_readout as an independent fitted tail",
            current_status="PROMISING_BUT_UNSIGNED",
            why_not_first="no numeric component row until the parent-to-observed metric/readout functor is written",
            next_use="if alpha_cg remains blocked, 2202 may attack readout theorem-zero directly",
        ),
        base_row(
            readout_id="RCG2201_1_guard",
            route="post-fit absorption guard",
            possible_zero_theorem="readout cannot be tuned after seeing Cassini/GM/orbital data to cancel PPN residuals",
            current_status="GUARD_NEEDED_NOT_DERIVED",
            why_not_first="requires a fixed-before-readout certificate",
            next_use="include in PPN owner matrix before any local-GR claim",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2201_0_component_matrix",
            gate="PPN component owner matrix exists",
            status="PASS_NONCLAIM",
            implication="all PPN vector legs now have owner/projection/source-ceiling slots.",
        ),
        base_row(
            gate_id="CG2201_1_alpha_cg_source",
            gate="alpha_cg has a source-backed ceiling target",
            status="PASS_NONCLAIM",
            implication="Cassini pressure is attached to alpha_cg as a target contribution, not as an MTS prediction.",
        ),
        base_row(
            gate_id="CG2201_2_alpha_cg_prediction",
            gate="alpha_cg is score-ready",
            status="BLOCKED_NONCLAIM",
            implication="Z_X, lambda_X, tau_PPN, S_PPN, same-branch c_g and vector-tail controls are missing.",
        ),
        base_row(
            gate_id="CG2201_3_raw_cg",
            gate="raw c_g is bounded",
            status="BLOCKED_NONCLAIM",
            implication="raw c_g remains non-invariant under field normalization and cannot be bound directly.",
        ),
        base_row(
            gate_id="CG2201_4_local_gr_newton",
            gate="local GR/Newton recovery claim",
            status="BLOCKED_NONCLAIM",
            implication="no local-GR, PPN, WEP, R10, clock, orbital or public claim follows from 2201.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2201_0_first_component",
            decision="SELECT_ALPHA_CG_FIRST_AS_SOURCE_CEILING_TARGET",
            rationale="it has the cleanest Cassini source pressure and names the exact normalization/range/projection blockers.",
            next_action="do not score it until the alpha_cg projection gate closes",
        ),
        base_row(
            decision_id="DEC2201_1_readout",
            decision="KEEP_READOUT_AS_SECOND_ROUTE",
            rationale="readout theorem-zero may be cleaner for GR/Newton recovery, but it needs a fixed observed-metric functor first.",
            next_action="if alpha_cg remains blocked, derive the fixed-before-readout PPN map",
        ),
        base_row(
            decision_id="DEC2201_2_next",
            decision="MOVE_TO_ALPHA_CG_PROJECTION_CLAUSE_OR_READOUT_ZERO_THEOREM",
            rationale="the source target exists; the missing work is either the actual projection map or a theorem-zero route for readout tails.",
            next_action="2202 should attack tau_PPN/S_PPN/Z_X ownership or the readout functor zero theorem",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2201_0_2202",
            selection_status="selected",
            target_file="2202-Y5-R2FR-alpha-cg-projection-clause-or-readout-zero-theorem.md",
            target_script="scripts/Y5_R2FR_alpha_cg_projection_clause_or_readout_zero_theorem_2202.py",
            objective="try to close the alpha_cg projection clause: Z_X, lambda_X/S_PPN, tau_PPN, common frame and vector-tail placement; if it fails, attack the readout theorem-zero route",
            success_condition="alpha_cg becomes a numeric/source-backed nonclaim prediction row or readout tail becomes theorem-zero conditional with fixed-before-readout clauses",
            do_not_do="do not bind raw c_g, do not set tau_PPN or S_PPN to one by convention, do not claim local GR, do not cancel vector components",
        )
    ]


def write_branch_copies() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["alpha_cg_source_row"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["component_owner_matrix"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["alpha_cg_projection_gate"], BRANCH_COPIES["beta_docs"]),
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
    matrix_rows: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    projection_rows: list[dict[str, Any]],
    readout_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if passed else "FAIL", detail=detail))

    add(
        "VAL2201_00_sources_exist",
        all(truthy(row["path_exists"]) for row in source_rows),
        f"{sum(truthy(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist",
    )
    add(
        "VAL2201_01_needles_found",
        all(truthy(row["needles_found"]) for row in source_rows),
        f"{sum(truthy(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found",
    )
    add(
        "VAL2201_02_matrix_complete",
        len(matrix_rows) == 7 and any(truthy(row["selected_first"]) and row["object"] == "alpha_cg" for row in matrix_rows),
        "seven component owner rows exist and alpha_cg is selected first",
    )
    add(
        "VAL2201_03_alpha_source_row",
        len(alpha_rows) == 2
        and any(row["row_id"] == "ACS2201_0_alpha_cg_target" and truthy(row["source_backed"]) for row in alpha_rows)
        and all(not truthy(row["direct_mts_prediction"]) for row in alpha_rows),
        "alpha_cg source target is source-backed but not a direct MTS prediction",
    )
    add(
        "VAL2201_04_projection_blocks",
        len(projection_rows) == 7 and all(truthy(row["blocks_score"]) for row in projection_rows),
        "all alpha_cg projection clauses block scoring",
    )
    add(
        "VAL2201_05_readout_competitor",
        len(readout_rows) == 2 and all("UNSIGNED" in row["current_status"] or "NEEDED" in row["current_status"] for row in readout_rows),
        "readout route is retained as unsigned competitor",
    )
    add(
        "VAL2201_06_claim_gate",
        any(row["gate_id"] == "CG2201_1_alpha_cg_source" and row["status"] == "PASS_NONCLAIM" for row in claim_rows)
        and any(row["gate_id"] == "CG2201_4_local_gr_newton" and row["status"] == "BLOCKED_NONCLAIM" for row in claim_rows),
        "source target passes nonclaim and local-GR remains blocked",
    )
    add(
        "VAL2201_07_decision",
        any(row["decision"] == "MOVE_TO_ALPHA_CG_PROJECTION_CLAUSE_OR_READOUT_ZERO_THEOREM" for row in decision_rows_data),
        "decision selects alpha_cg projection clause or readout zero theorem next",
    )
    add(
        "VAL2201_08_next_target",
        len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2201_0_2202",
        "2202 target selected",
    )
    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["component_owner_matrix"],
        OUTPUTS["alpha_cg_source_row"],
        OUTPUTS["alpha_cg_projection_gate"],
        OUTPUTS["readout_competitor_gate"],
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
    add("VAL2201_09_csv_parse", parse_ok_all, "; ".join(parse_parts))
    add(
        "VAL2201_10_branch_copies",
        len(copy_rows) == 3 and all(truthy(row["copied"]) and truthy(row["parse_ok"]) for row in copy_rows),
        ";".join(str(row["target_path"]) for row in copy_rows),
    )
    all_generated_rows = [
        *source_rows,
        *matrix_rows,
        *alpha_rows,
        *projection_rows,
        *readout_rows,
        *claim_rows,
        *decision_rows_data,
        *next_rows,
        *copy_rows,
    ]
    add(
        "VAL2201_11_claim_flags_false",
        all(not truthy(row.get("valid_for_claim", False)) and not truthy(row.get("claim_allowed", False)) for row in all_generated_rows),
        "all generated rows keep valid_for_claim=false and claim_allowed=false",
    )
    add(
        "VAL2201_12_score_flags_false",
        all(not truthy(row.get("score_ready", False)) for row in [*matrix_rows, *alpha_rows]),
        "no alpha_cg or matrix row is score-ready",
    )
    add(
        "VAL2201_13_formalization_clean",
        not formalization_has_2201_artifacts(),
        "formalization-workbench has no 2201 artifacts",
    )
    add(
        "VAL2201_14_pycache_absent",
        not (ROOT / "scripts" / "__pycache__").exists(),
        str(ROOT / "scripts" / "__pycache__"),
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2201_OVERALL",
        overall,
        "2201 builds the PPN component owner matrix and stages alpha_cg as a source-backed nonclaim target, not a prediction",
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    matrix_rows: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    projection_rows: list[dict[str, Any]],
    readout_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_data: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2201 - Y5/R2FR PPN Component Owner Matrix Or Alpha-Cg Source Row",
        "",
        "## Current Verdict",
        "",
        "2201 turns the 2200 PPN vector contract into an owner/projection matrix. The first component selected is `alpha_cg`, not because it is claimable, but because Cassini gives the cleanest source ceiling and this leg exposes the exact missing normalization, range, and projection clauses.",
        "",
        "`alpha_cg` now has a source-backed nonclaim target row: `abs(alpha_cg) <= 0.005788015401465051` only as an absolute contribution inside the full PPN vector, and only after the other vector tails are theorem-zero or separately bounded. Raw `c_g` remains refused.",
        "",
        "The readout tail is kept as the second route, because a fixed-before-readout theorem could be cleaner for GR/Newton recovery, but it is not signed yet.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## PPN Component Owner Matrix",
        "",
        md_table(
            matrix_rows,
            [
                "component_id",
                "rank",
                "selected_first",
                "component",
                "object",
                "owner_status",
                "projection_status",
                "source_ceiling_status",
                "reason_for_rank",
                "score_ready",
                "valid_for_claim",
            ],
        ),
        "",
        "## Alpha-Cg Source Row",
        "",
        md_table(
            alpha_rows,
            [
                "row_id",
                "selected_component",
                "source_observable",
                "source_bound_value",
                "translated_ceiling_object",
                "translated_ceiling_value",
                "owner_status",
                "source_backed",
                "direct_mts_prediction",
                "score_ready",
                "valid_for_claim",
            ],
        ),
        "",
        "## Alpha-Cg Projection Gate",
        "",
        md_table(projection_rows, ["gate_id", "requirement", "needed_statement", "current_status", "blocks_score", "valid_for_claim"]),
        "",
        "## Readout Competitor Gate",
        "",
        md_table(readout_rows, ["readout_id", "route", "possible_zero_theorem", "current_status", "why_not_first", "next_use", "valid_for_claim"]),
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
        "This is a forward step toward GR/Newton reduction because the local PPN comparison is no longer a single vague coupling. It is a component matrix with a sourced ceiling and explicit owner/projection gates. The project still cannot claim local GR, but it now has a concrete first PPN component to either derive, source, or kill.",
        "",
        "Best next attack: `2202` should try to close the `alpha_cg` projection clause. If `Z_X`, `lambda_X/S_PPN`, `tau_PPN`, common-frame and vector-tail placement cannot be derived, switch to the readout theorem-zero route rather than looping raw `c_g`.",
    ]
    DOC.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    matrix_rows = component_owner_matrix_rows()
    alpha_rows = alpha_cg_source_rows()
    projection_rows = alpha_cg_projection_gate_rows()
    readout_rows = readout_competitor_rows()
    claim_rows = claim_gate_rows()
    decision_rows_data = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["component_owner_matrix"], matrix_rows)
    write_csv(OUTPUTS["alpha_cg_source_row"], alpha_rows)
    write_csv(OUTPUTS["alpha_cg_projection_gate"], projection_rows)
    write_csv(OUTPUTS["readout_competitor_gate"], readout_rows)
    write_csv(OUTPUTS["claim_gate"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows_data)
    write_csv(OUTPUTS["next_target"], next_rows)

    copy_rows = write_branch_copies()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_data = validation_rows(
        source_rows,
        matrix_rows,
        alpha_rows,
        projection_rows,
        readout_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_data)
    write_doc(
        source_rows,
        matrix_rows,
        alpha_rows,
        projection_rows,
        readout_rows,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
        validation_rows_data,
    )


if __name__ == "__main__":
    main()
