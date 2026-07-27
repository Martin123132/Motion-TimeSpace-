from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_OBSERVED_COEFFICIENT_FUNCTOR_OR_FIRST_JQ_BOUND_ROW_2432"
CHECKPOINT_ID = "2432"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2432-Y5-R2FR-parent-observed-coefficient-functor-or-first-Jq-bound-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2432_SOURCE_REGISTER.csv",
    "functor_attempt": OUT / "P8_Y5_PARENT_QLOC_2432_OBSERVED_COEFFICIENT_FUNCTOR_ATTEMPT.csv",
    "target_category": OUT / "P8_Y5_PARENT_QLOC_2432_VISIBLE_COEFFICIENT_TARGET_CATEGORY.csv",
    "obstructions": OUT / "P8_Y5_PARENT_QLOC_2432_FUNCTOR_OBSTRUCTION_COUNTERMODELS.csv",
    "jq_closure_map": OUT / "P8_Y5_PARENT_QLOC_2432_JQ_CHANNEL_CLOSURE_MAP.csv",
    "first_bound_requirements": OUT / "P8_Y5_PARENT_QLOC_2432_FIRST_JQ_BOUND_ROW_REQUIREMENTS.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2432_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2432_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2432_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2432_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2432_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_functor": QUEUE / "JR2432_OBSERVED_COEFFICIENT_FUNCTOR_NONCLAIM.csv",
    "queue_bound_requirements": QUEUE / "JR2432_FIRST_JQ_BOUND_REQUIREMENTS_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "observed_coefficient_functor_Jq_map_nonclaim_2432.csv",
    "beta_docs": BETA_DOCS / "OBSERVED_COEFFICIENT_FUNCTOR_JQ_MAP_2432_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2432_00_2431_handoff",
        "source_path": ROOT / "2431-Y5-R2FR-Jq-source-leg-zero-theorem-or-component-bound-vector.md",
        "needles": ["NEXT2431_0_selected", "JZT2431_4_no_hidden_visible_Hom", "VAL2431_OVERALL"],
        "role": "fresh handoff to observed-coefficient functor construction",
    },
    {
        "source_id": "SRC2432_01_2431_validation",
        "source_path": OUT / "P8_Y5_BRR545_2431_VALIDATION.csv",
        "needles": ["VAL2431_OVERALL", "PASS"],
        "role": "confirms 2431 passed before 2432",
    },
    {
        "source_id": "SRC2432_02_2431_component_vector",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2431_JQ_COMPONENT_BOUND_VECTOR.csv",
        "needles": ["JQC2431_2_material_marker", "JQC2431_9_total_abs"],
        "role": "current J_q component vector",
    },
    {
        "source_id": "SRC2432_03_2318_functor_precedent",
        "source_path": ROOT / "2318-Y5-R2FR-parent-coefficient-functor-construction-or-finite-coupling-prior-runner.md",
        "needles": ["PCF2318_0_candidate_functor", "PCF2318_5_verdict"],
        "role": "older parent coefficient functor attempt",
    },
    {
        "source_id": "SRC2432_04_2317_hidden_visible",
        "source_path": ROOT / "2317-Y5-R2FR-no-hidden-visible-hom-jq-zero-or-finite-coefficient-prior.md",
        "needles": ["VAL2317_OVERALL", "finite coupling prior interface"],
        "role": "hidden-visible Hom obstruction and finite coupling interface",
    },
    {
        "source_id": "SRC2432_05_2391_obs_functor",
        "source_path": ROOT / "2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md",
        "needles": ["QOF2391_6_verdict", "QOC2391_6_matter_readout_descent"],
        "role": "q/Obs_e quotient-basic functor contract",
    },
    {
        "source_id": "SRC2432_06_2425_product_law",
        "source_path": ROOT / "2425-Y5-R2FR-parent-finite-quadratic-q-row-and-source-test-coupling-split.md",
        "needles": ["LAW2425_2_R10_alpha_match", "LAW2425_3_common_Weyl_cg"],
        "role": "source/test product law and c_g squared guard",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


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
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def functor_attempt_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="OCF2432_0_candidate",
            object="parent observed-coefficient functor",
            construction="Obs_coeff: Parent -> Coeff_vis with coefficients c_A = cbar_A(Obs_e, Q_obs, Rep, Top, Level_EM, universal constants) and no hidden/local q representative argument.",
            theorem_effect="if v_q in ker(D Obs_coeff), then Lie_vq c_A=0 for EM, mass, clock, source-weight, frame and readout coefficients",
            current_status="CANDIDATE_CONTRACT_WRITTEN_NOT_PARENT_SELECTED",
            blocker="parent syntax/target category not selected",
            theorem_zero=False,
        ),
        base_row(
            row_id="OCF2432_1_chain_rule",
            object="coefficient derivative silence",
            construction="For c_A=cbar_A(Obs_coeff(Phi)), Lie_vq c_A = D cbar_A[D Obs_coeff(v_q)] = 0 if D Obs_coeff(v_q)=0.",
            theorem_effect="kills b_alpha, b_mu, b_material, b_frame, source-weight and readout slopes in the J_q component vector",
            current_status="EXACT_CONDITIONAL_THEOREM",
            blocker="D Obs_coeff(v_q)=0 not parent-proved for all retained vertical vectors",
            theorem_zero=False,
        ),
        base_row(
            row_id="OCF2432_2_target_exclusion",
            object="no hidden-visible Hom target",
            construction="The visible coefficient target category must exclude Hom(hidden/profile/source labels -> visible coefficients) except fixed representation/topological labels.",
            theorem_effect="forbids c=c0+epsilon I_hid and source-only prefactor maps that regenerate J_q",
            current_status="REQUIRED_TYPE_RULE_NOT_PARENT_SIGNED",
            blocker="hidden invariant algebra and source-prefactor targets remain legal countermodels",
            theorem_zero=False,
        ),
        base_row(
            row_id="OCF2432_3_readout_closure",
            object="effective/readout closure",
            construction="Detector thresholds, clocks, rods, source-worldtube maps, effective actions and renormalized coefficients must also factor through Obs_coeff.",
            theorem_effect="prevents tree-level q-blindness from being undone downstream",
            current_status="REQUIRED_GUARD_UNSIGNED",
            blocker="readout/effective-action closure not proved",
            theorem_zero=False,
        ),
        base_row(
            row_id="OCF2432_4_common_measure",
            object="common measure/current normalization",
            construction="Action measure, Hilbert/source current, active mass and calibration maps must be owned by the same observed branch.",
            theorem_effect="prevents relative source-weight delta_w_A and measured-GM leakage",
            current_status="SOURCE_NORMALIZATION_OWNER_MISSING",
            blocker="common measure/current owner not signed",
            theorem_zero=False,
        ),
        base_row(
            row_id="OCF2432_5_verdict",
            object="functor closure verdict",
            construction="The candidate functor is exact enough to be the right parent contract, but current MTS does not yet prove its target category, vertical kernel basicness, no-Hom rule, common measure, or readout closure.",
            theorem_effect="J_q component vector remains live",
            current_status="PARENT_OBSERVED_COEFFICIENT_FUNCTOR_NOT_CONSTRUCTED",
            blocker="move to vertical-kernel/target-category owner or finite coefficient row",
            theorem_zero=False,
        ),
    ]


def target_category_rows() -> list[dict[str, Any]]:
    rows = [
        ("TGT2432_0_geometry", "observed geometry/coframe", "Obs_e, g_obs, connection data", "hidden/profile/source labels", "CONDITIONAL_ALLOWED", "J_q^frame if unsigned"),
        ("TGT2432_1_EM", "EM/fine-structure/gauge kinetic", "Level_EM, representation/topological fixed labels", "hidden scalar, q representative, source material label", "TARGET_NOT_PARENT_SIGNED", "J_q^marker, clocks, EM"),
        ("TGT2432_2_matter_masses", "mass ratios/material binding", "fixed representation/superselection data", "hidden profile scalar or local q amplitude", "TARGET_NOT_PARENT_SIGNED", "WEP/clock/material J_q"),
        ("TGT2432_3_source_weights", "active source weights and measured GM", "common calibration mode only", "species/source-only R_+ prefactors", "TARGET_EXCLUSION_UNSIGNED", "J_q^source_norm and R10/WEP source leg"),
        ("TGT2432_4_readouts", "clock/rod/detector/source-worldtube readout", "same Obs_coeff branch after variation", "post-variation q marker/readout tail", "READOUT_CLOSURE_UNSIGNED", "J_q^projector/readout/memory"),
        ("TGT2432_5_finite_range", "finite q exchange projection", "branch-locked K_q and beta_s beta_t product", "naked linear c_g or packed/unpacked source leg ambiguity", "PRODUCT_GUARD_RETAINED", "R10/PPN/WEP finite residual"),
        ("TGT2432_6_verdict", "visible coefficient target category", "all visible coefficients factor through q-blind observed objects", "any hidden-visible Hom or source-only prefactor", "TARGET_CATEGORY_NOT_PARENT_OWNED", "J_q=0 not claimable"),
    ]
    return [
        base_row(target_id=target_id, coefficient_target=target, allowed_domain=allowed, forbidden_domain=forbidden, current_status=status, impact_if_unsigned=impact)
        for target_id, target, allowed, forbidden, status, impact in rows
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        base_row(obstruction_id="OBS2432_0_hidden_scalar", countermodel="If hidden invariant I_hid survives, c_A=c_A0+epsilon I_hid is a valid visible coefficient map.", kills_functor_clause="no hidden-visible Hom", required_repair="prove hidden invariant algebra trivial/quotient-constant or forbid target by type", current_status="COUNTERMODEL_RETAINED"),
        base_row(obstruction_id="OBS2432_1_source_prefactor", countermodel="Species/source-only active weights w_A=w0(1+epsilon s_A q) alter source charge without changing test readout equally.", kills_functor_clause="source target exclusion", required_repair="common calibration only or source-label forgetting theorem", current_status="COUNTERMODEL_RETAINED"),
        base_row(obstruction_id="OBS2432_2_shadow_frame", countermodel="Observed frame e_obs=exp(b_g q) e_basic is one public frame but not quotient-basic unless b_g=0 or q is visible physical data.", kills_functor_clause="basic coframe/frame descent", required_repair="Lie_v e_parent=0 or bound b_g/b_dis", current_status="COUNTERMODEL_RETAINED"),
        base_row(obstruction_id="OBS2432_3_readout_reentry", countermodel="Detector thresholds, clocks or source-worldtube processing reintroduce q after the action variation.", kills_functor_clause="readout closure", required_repair="variation-before-readout theorem and readout functor naturality", current_status="COUNTERMODEL_RETAINED"),
        base_row(obstruction_id="OBS2432_4_boundary_body", countermodel="Body/worldtube boundary charge sets exterior q even when bulk coefficients descend.", kills_functor_clause="bulk-only descent", required_repair="Q_q[body]=0 theorem or source-backed charge bound", current_status="COUNTERMODEL_RETAINED"),
        base_row(obstruction_id="OBS2432_5_verdict", countermodel="At least one countermodel survives in the current corpus.", kills_functor_clause="claim-grade J_q=0", required_repair="prove target category plus vertical kernel basicness or use finite bounds", current_status="FUNCTOR_NOT_CLOSED"),
    ]


def jq_closure_map_rows() -> list[dict[str, Any]]:
    rows = [
        ("JQMAP2432_0_bulk_matter", "J_q^matter_bulk", "OCF2432_1_chain_rule plus ordinary matter target clauses", "PARTIAL_CONDITIONAL_ONLY", "B_matter_q"),
        ("JQMAP2432_1_frame", "J_q^frame", "TGT2432_0_geometry plus no shadow-frame countermodel", "OPEN_SHADOW_FRAME", "B_frame_q"),
        ("JQMAP2432_2_marker", "J_q^marker", "TGT2432_1_EM and TGT2432_2_matter_masses plus no hidden-visible Hom", "OPEN_HIDDEN_VISIBLE_HOM", "B_marker_q"),
        ("JQMAP2432_3_body", "J_q^body", "body/worldtube charge theorem independent of bulk functor", "OPEN_BODY_BOUNDARY_CHARGE", "B_body_q"),
        ("JQMAP2432_4_boundary", "J_q^boundary", "B_q/Q_q exact/proper-zero in physical source boundary class", "OPEN_SOURCE_BOUNDARY_CLASS", "B_boundary_q"),
        ("JQMAP2432_5_projector_readout", "J_q^projector", "readout functor naturality and variation-before-readout", "OPEN_READOUT_REENTRY", "B_projector_q"),
        ("JQMAP2432_6_memory", "J_q^memory", "memory kernel descends or is topological/first-class", "OPEN_MEMORY_KERNEL", "B_memory_q"),
        ("JQMAP2432_7_source_norm", "J_q^source_norm", "common measure/current/source calibration owner", "OPEN_SOURCE_NORMALIZATION", "B_source_norm_q"),
        ("JQMAP2432_8_total", "J_q^abs", "every channel closes in same branch or is bounded absolutely", "TOTAL_ZERO_NOT_PROVED", "B_total_q"),
    ]
    return [
        base_row(map_id=map_id, jq_component=component, closure_requirement=requirement, current_status=status, fallback_bound_symbol=fallback, theorem_zero=False, score_ready=False)
        for map_id, component, requirement, status, fallback in rows
    ]


def first_bound_requirement_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="FBR2432_0_first_recommended", component="J_q^marker or J_q^frame", reason="these hit clocks/WEP/R10/EM and test the no-hidden-visible Hom problem directly", required_fields="symbol;definition;units;normalization;q branch;projection arena;numeric bound or theorem-zero;uncertainty;source path;no-cancellation group", valid_for_claim=False, source_backed=False),
        base_row(row_id="FBR2432_1_no_numeric_today", component="all finite rows", reason="no source-backed coefficient value is present in this checkpoint", required_fields="do not fabricate b_alpha, b_g, delta_w, tau_readout, or source/worldtube charge values", valid_for_claim=False, source_backed=False),
        base_row(row_id="FBR2432_2_bound_rule", component="J_q^abs", reason="finite branch must use absolute sum not fitted cancellation", required_fields="B_total_q=sum_i B_i; q_bound=(B_total_q+Phi_boundary_abs)/c_q; alpha uses beta_s_abs beta_t_abs", valid_for_claim=False, source_backed=False),
        base_row(row_id="FBR2432_3_verdict", component="first J_q bound row", reason="schema is ready but not source-backed", required_fields="next step must either prove functor closure or source one real coefficient row", valid_for_claim=False, source_backed=False),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2432_0_functor_constructed", claim="parent observed-coefficient functor is constructed", gate_pass=False, reason="candidate contract written but target category, vertical kernel basicness, no-Hom, common measure and readout closure are unsigned"),
        base_row(claim_id="CGATE2432_1_no_hidden_visible", claim="no hidden-visible coefficient/readout Hom", gate_pass=False, reason="hidden scalar/source-prefactor/shadow-frame/readout countermodels remain"),
        base_row(claim_id="CGATE2432_2_Jq_zero", claim="J_q=0 follows", gate_pass=False, reason="J_q channel closure map has open frame, marker, body, boundary, projector, memory and source-normalization channels"),
        base_row(claim_id="CGATE2432_3_first_bound_score", claim="first J_q finite row can score", gate_pass=False, reason="first bound rows are requirements only, not source-backed numerical/theorem-zero values"),
        base_row(claim_id="CGATE2432_4_local_GR", claim="local GR/Newton reduction follows", gate_pass=False, reason="J_q zero and q no-hair activation are still blocked"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2432_0_candidate_functor", decision="ACCEPT_FUNCTOR_AS_EXACT_PARENT_CONTRACT", rationale="if parent-owned, chain rule kills visible coefficient slopes and many J_q channels", consequence="use as derivation target"),
        base_row(decision_id="DEC2432_1_no_promotion", decision="DO_NOT_PROMOTE_FUNCTOR_OR_JQ_ZERO", rationale="countermodels remain legal without target category and vertical-kernel proof", consequence="component vector stays live"),
        base_row(decision_id="DEC2432_2_best_next", decision="ATTACK_VERTICAL_KERNEL_AND_TARGET_CATEGORY_OWNER", rationale="without DObs(v_q)=0 and no hidden-visible targets, no coefficient functor can be claim-grade", consequence="select 2433"),
        base_row(decision_id="DEC2432_3_fallback", decision="FIRST_BOUND_ROW_AFTER_OWNER_ATTEMPT", rationale="if functor ownership fails, the honest path is source-backed finite coefficient rows", consequence="do not run empirical scoring yet"),
        base_row(decision_id="DEC2432_4_public", decision="NO_GITHUB_ACTION", rationale="private derivation gate only", consequence="continue private goal work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2432_0_selected",
            selection_status="selected",
            target_file="2433-Y5-R2FR-vertical-kernel-and-visible-target-category-owner-or-first-coefficient-bound-row.md",
            target_script="scripts/Y5_R2FR_vertical_kernel_and_visible_target_category_owner_or_first_coefficient_bound_row_2433.py",
            task="prove the retained q-vertical kernel is parent-null/matter-invisible and the visible coefficient target category excludes hidden scalar/source-prefactor/readout Hom maps; if not, fill first finite coefficient bound row as nonclaim",
            acceptance_target="DObs_coeff(v_q)=0 plus no-hidden-visible target theorem, or first coefficient-bound row with units/source/projection and valid_for_claim=false",
            guardrails="do not make q/Obs by projection declaration, invent coefficient values, cancel J_q components, claim local GR/R10/PPN/WEP/clock/orbital pass, edit formalization-workbench, or push GitHub",
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue_functor", OUTPUTS["functor_attempt"], COPY_TARGETS["queue_functor"], "observed coefficient functor nonclaim queue"),
        ("queue_bound_requirements", OUTPUTS["first_bound_requirements"], COPY_TARGETS["queue_bound_requirements"], "first J_q bound requirements nonclaim queue"),
        ("branch_wep", OUTPUTS["jq_closure_map"], COPY_TARGETS["branch_wep"], "WEP/local residual J_q closure map"),
        ("beta_docs", OUTPUTS["jq_closure_map"], COPY_TARGETS["beta_docs"], "beta-source observed coefficient J_q map"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target, note in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=source, target_path=target, source_exists=source.exists(), target_exists=target.exists(), notes=note))
    return rows


def validation_rows(all_outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_rows = all_outputs["source_register"]
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    formalization_hits: list[Path] = []
    for pattern in ["*2432-Y5-R2FR*", "*P8_Y5_PARENT_QLOC_2432*", "*P8_Y5_BRR545_2432*", "*JR2432*", "*OBSERVED_COEFFICIENT_FUNCTOR_JQ_MAP_2432*"]:
        formalization_hits.extend(FORMALIZATION.rglob(pattern) if FORMALIZATION.exists() else [])

    checks = [
        ("VAL2432_00_sources_exist", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2432_01_source_needles", all(row["needles_found"] for row in source_rows), "all cited source needles are present"),
        ("VAL2432_02_candidate_functor_written", any(row["row_id"] == "OCF2432_0_candidate" for row in all_outputs["functor_attempt"]), "candidate observed-coefficient functor written"),
        ("VAL2432_03_chain_rule_exact", any(row["row_id"] == "OCF2432_1_chain_rule" and row["current_status"] == "EXACT_CONDITIONAL_THEOREM" for row in all_outputs["functor_attempt"]), "exact coefficient chain-rule theorem present"),
        ("VAL2432_04_countermodels_retained", any(row["obstruction_id"] == "OBS2432_5_verdict" and row["current_status"] == "FUNCTOR_NOT_CLOSED" for row in all_outputs["obstructions"]), "countermodels are retained"),
        ("VAL2432_05_Jq_map_open", any(row["map_id"] == "JQMAP2432_8_total" and row["current_status"] == "TOTAL_ZERO_NOT_PROVED" for row in all_outputs["jq_closure_map"]), "J_q total remains open"),
        ("VAL2432_06_first_bound_nonclaim", all(not row["source_backed"] and not row["valid_for_claim"] for row in all_outputs["first_bound_requirements"]), "first bound requirements remain nonclaim"),
        ("VAL2432_07_claims_blocked", all(not row["gate_pass"] for row in all_outputs["claim_gates"]), "all claim gates remain false"),
        ("VAL2432_08_next_target_written", any(row["route_id"] == "NEXT2432_0_selected" for row in all_outputs["next_target"]), "next target selected"),
        ("VAL2432_09_branch_copies", all(row["target_exists"] for row in all_outputs["branch_copies"]), "branch copies were written"),
        ("VAL2432_10_no_formalization_artifacts", len(formalization_hits) == 0, "no 2432 artifacts were written to formalization-workbench"),
    ]
    for check_id, passed, notes in checks:
        rows.append(base_row(check_id=check_id, status="PASS" if passed else "FAIL", notes=notes, detail="" if passed else "required checkpoint condition failed"))
    for path in output_csvs:
        parses, row_count, message = csv_parses(path)
        rows.append(base_row(check_id=f"VAL2432_CSV_{path.stem}", status="PASS" if parses and row_count > 0 else "FAIL", notes=f"CSV parses with {row_count} rows", detail=message))
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            check_id="VAL2432_OVERALL",
            status="PASS" if overall else "FAIL",
            notes="2432 writes the parent observed-coefficient functor contract, proves its exact conditional chain-rule effect, retains countermodels, blocks J_q/local-GR promotion, and selects vertical-kernel/target-category owner or first coefficient-bound row next",
            detail="",
        )
    )
    return rows


def write_markdown(all_outputs: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2432 - Y5/R2FR Parent Observed-Coefficient Functor Or First Jq Bound Row",
        "",
        "## Result",
        "- 2432 constructs the exact parent contract we need: visible coefficients must be generated only from q-blind observed objects, fixed representation/topological labels, declared EM/source levels, and universal constants.",
        "- If parent-owned, the chain rule gives `Lie_vq c_A=0`, killing visible coefficient slopes and many `J_q` channels.",
        "- The construction still does not close: target category, vertical-kernel basicness, hidden scalar/source-prefactor exclusion, common measure/current ownership, and readout/effective-action closure are unsigned.",
        "- Therefore no `J_q=0`, local-GR/Newton, R10, PPN, WEP, clock, orbital, or public claim is created.",
        "",
        "## Practical Status",
        "This is the cleanest version of the coupling problem so far: either the parent theory has a q-blind observed-coefficient functor, or it has finite coefficients that must be bounded. No mushy middle.",
        "",
        "## Source Register",
        table(["source_id", "source_path", "path_exists", "needles_found", "role"], all_outputs["source_register"]),
        "",
        "## Observed-Coefficient Functor Attempt",
        table(["row_id", "object", "construction", "theorem_effect", "current_status", "blocker", "theorem_zero", "valid_for_claim"], all_outputs["functor_attempt"]),
        "",
        "## Visible Coefficient Target Category",
        table(["target_id", "coefficient_target", "allowed_domain", "forbidden_domain", "current_status", "impact_if_unsigned", "valid_for_claim"], all_outputs["target_category"]),
        "",
        "## Functor Obstruction Countermodels",
        table(["obstruction_id", "countermodel", "kills_functor_clause", "required_repair", "current_status", "valid_for_claim"], all_outputs["obstructions"]),
        "",
        "## J_q Channel Closure Map",
        table(["map_id", "jq_component", "closure_requirement", "current_status", "fallback_bound_symbol", "valid_for_claim"], all_outputs["jq_closure_map"]),
        "",
        "## First J_q Bound Row Requirements",
        table(["row_id", "component", "reason", "required_fields", "source_backed", "valid_for_claim"], all_outputs["first_bound_requirements"]),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], all_outputs["claim_gates"]),
        "",
        "## Decisions",
        table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], all_outputs["decisions"]),
        "",
        "## Next Target",
        table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], all_outputs["next_target"]),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], all_outputs["branch_copies"]),
        "",
        "## Validation",
        table(["check_id", "status", "notes", "detail"], all_outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for path in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        path.mkdir(parents=True, exist_ok=True)

    all_outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "functor_attempt": functor_attempt_rows(),
        "target_category": target_category_rows(),
        "obstructions": obstruction_rows(),
        "jq_closure_map": jq_closure_map_rows(),
        "first_bound_requirements": first_bound_requirement_rows(),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next_target": next_target_rows(),
    }

    for key, rows in all_outputs.items():
        write_csv(OUTPUTS[key], rows)

    all_outputs["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], all_outputs["branch_copies"])
    all_outputs["validation"] = validation_rows(all_outputs)
    write_csv(OUTPUTS["validation"], all_outputs["validation"])
    write_markdown(all_outputs)

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    print(DOC)
    print(OUTPUTS["validation"])
    print(f"VAL2432_OVERALL={all_outputs['validation'][-1]['status']}")


if __name__ == "__main__":
    main()
