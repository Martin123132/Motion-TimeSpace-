from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2204"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2204-Y5-R2FR-topological-Hilbert-equality-or-R-eq-first-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2204_SOURCE_REGISTER.csv",
    "route_merge": OUT / "P8_Y5_PARENT_QLOC_2204_ROUTE_MERGE_AUDIT.csv",
    "same_object": OUT / "P8_Y5_PARENT_QLOC_2204_SAME_OBJECT_THEOREM_STATUS.csv",
    "r_eq_first_rows": OUT / "P8_Y5_PARENT_QLOC_2204_R_EQ_FIRST_ROW_REGISTER.csv",
    "frontier": OUT / "P8_Y5_PARENT_QLOC_2204_FRONTIER_SELECTION.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2204_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2204_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2204_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2204_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2204_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2204_ROUTE_MERGE_R_EQ_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2204_R_EQ_FIRST_ROW_REGISTER_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_ROUTE_MERGE_2204_NONCLAIM.csv",
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


def formalization_has_2204_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2204-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2204*",
        "*P8_Y5_BRR545_2204*",
        "*Y5_R2FR_topological_Hilbert_equality_or_R_eq_first_row_2204*",
        "*JR2204*",
        "*PARENT_QLOC_ROUTE_MERGE_2204*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2203_handoff",
            ROOT / "2203-Y5-R2FR-fixed-before-readout-PPN-map-or-measured-GM-obstruction-row.md",
            ["NEXT2203_0_2204", "FBR2203_7_verdict", "VAL2203_OVERALL"],
            "current 2203 branch selects topological-Hilbert/R_eq as the next readout/source-normalization gate.",
        ),
        (
            "2203_validation",
            OUT / "P8_Y5_BRR545_2203_VALIDATION.csv",
            ["VAL2203_OVERALL", "PASS"],
            "2203 validation passed before route merge.",
        ),
        (
            "1773_same_object",
            ROOT / "1773-Y5-R2FR-topological-Hilbert-equality-or-R-eq-bound.md",
            ["SOT1773_5_current_verdict", "PCL1773_4_verdict", "VAL1773_OVERALL"],
            "older R2FR checkpoint already isolated the conditional same-object theorem and period-charge blocker.",
        ),
        (
            "2182_equality_gate",
            ROOT / "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
            ["TEA2182_7_current_verdict", "EMB2182_6_total_envelope", "NEXT2182_0_2183"],
            "recent local-GR chain already wrote the exact R_eq/B_zero/epsilon_M gate.",
        ),
        (
            "2183_selector",
            ROOT / "2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md",
            ["WST2183_7_current_verdict", "DEC2183_2_best_next", "NEXT2183_0_2184"],
            "recent chain already sharpened the parent worldtube/source selector theorem.",
        ),
        (
            "2184_parent_action",
            ROOT / "2184-Y5-R2FR-minimal-parent-action-Hamiltonian-charge-contract-or-selector-residual-fill.md",
            ["VBR2184_2_EH_to_v_coefficients", "DEC2184_3_next", "NEXT2184_0_2185"],
            "recent chain already moved from selector theorem to minimal parent-action/EH fixed-point contract.",
        ),
        (
            "1015_same_object_lemma",
            ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
            ["SOL1015_6_verdict", "REB1015_0_R_eq_integral", "DEC1015_3_next_target"],
            "R10-era same-object lemma and R_eq first rows.",
        ),
        (
            "1153_no_tautology",
            ROOT / "1153-Y5-R10-topological-PiM-Hilbert-equality-parent-signature-or-R_eq-source-fill.md",
            ["THEO1153_7_verdict", "REQ1153_4_R_eq_finite_shell_profile", "GUARD1153_0_no_tautological_definition"],
            "parent-signature/no-tautology guard for Hilbert-topological equality.",
        ),
        (
            "1013_obstruction_vector",
            OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
            ["OBS1013_3_topological_equality_residual", "MISSING_R_EQ_INTEGRAL"],
            "machine R_eq row inside the measured-GM obstruction vector.",
        ),
        (
            "2182_validation",
            OUT / "P8_Y5_BRR545_2182_VALIDATION.csv",
            ["VAL2182_OVERALL", "PASS"],
            "2182 validation confirms the exact equality gate is already present.",
        ),
        (
            "2183_validation",
            OUT / "P8_Y5_BRR545_2183_VALIDATION.csv",
            ["VAL2183_OVERALL", "PASS"],
            "2183 validation confirms the worldtube/source selector branch is already present.",
        ),
        (
            "2184_validation",
            OUT / "P8_Y5_BRR545_2184_VALIDATION.csv",
            ["VAL2184_OVERALL", "PASS"],
            "2184 validation confirms the next non-duplicative frontier is coefficient/descent extraction.",
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


def route_merge_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="RMG2204_0_2203_demand",
            route_piece="2203 readout/source-normalization demand",
            evidence="fixed-before-readout PPN map failed; measured-GM obstruction vector selects R_eq/topological-Hilbert next",
            status="ACTIVE_HANDOFF",
            implication="2204 must handle R_eq without claiming local GR",
            duplicate_risk=False,
        ),
        base_row(
            route_id="RMG2204_1_1773_done",
            route_piece="same-object theorem already audited",
            evidence="1773 recorded conditional de Rham/Poincare-dual theorem, period-charge blocker, and R_eq bound pack",
            status="EVIDENCE_EXISTS",
            implication="do not spend another cycle proving the same conditional lemma",
            duplicate_risk=True,
        ),
        base_row(
            route_id="RMG2204_2_2182_done",
            route_piece="R_eq/B_zero/epsilon_M gate already built",
            evidence="2182 writes Pi_M J_H = J_M_top + dB_zero + R_eq and abs(epsilon_M) absolute envelope",
            status="EVIDENCE_EXISTS",
            implication="R_eq first rows exist as placeholders; no claim until source-backed or theorem-zero",
            duplicate_risk=True,
        ),
        base_row(
            route_id="RMG2204_3_2183_done",
            route_piece="worldtube/source selector already sharpened",
            evidence="2183 defines W_source=supp(J_H[e_obs,tau]) conditionally and blocks current branch on parent action/PiM/boundary signatures",
            status="EVIDENCE_EXISTS",
            implication="the topological route's real missing object is now a parent-owned charge contract",
            duplicate_risk=True,
        ),
        base_row(
            route_id="RMG2204_4_2184_frontier",
            route_piece="minimal parent-action charge contract frontier",
            evidence="2184 writes the parent action skeleton and selects EH-to-v coefficient extraction",
            status="FRONTIER_ALREADY_ADVANCED",
            implication="the best non-circular route is to carry 2203 into the existing EH fixed-point/descent frontier",
            duplicate_risk=False,
        ),
        base_row(
            route_id="RMG2204_5_verdict",
            route_piece="anti-circling route merge",
            evidence="2203 need is satisfied by existing 1773/2182/2183/2184 artifacts, but none permit a claim",
            status="ROUTE_MERGED_NO_DUPLICATE_REDERIVATION",
            implication="2204 records the merge and selects the next non-duplicative local-GR target",
            duplicate_risk=False,
        ),
    ]


def same_object_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            theorem_id="SOT2204_0_conditional_lemma",
            statement="If Pi_M J_H and J_M_top represent the same compact Hilbert source cohomology class, then Pi_M J_H-J_M_top=dB_zero plus residual R_eq.",
            status="CONDITIONAL_MATH_CLEAN_ALREADY_RECORDED",
            evidence_source="1015;1773;2182",
            missing_for_current_MTS="parent-signed worldtube, same Hilbert measure, period-charge lock, B_zero zero flux, no extra exchange",
            blocks_claim=False,
        ),
        base_row(
            theorem_id="SOT2204_1_current_branch",
            statement="Current MTS does not yet prove Pi_M J_H = J_M_top + dB_zero.",
            status="NOT_PARENT_SIGNED",
            evidence_source="1773;2182;2183;1153",
            missing_for_current_MTS="R_eq=0 or finite bound, M_H_ref, W_source selector, PiM/Hamiltonian lock, fixed reference",
            blocks_claim=True,
        ),
        base_row(
            theorem_id="SOT2204_2_no_closed_wrong_object",
            statement="A conserved topological current is not evidence unless it is the same observed Hilbert source object.",
            status="GUARDRAIL_ACTIVE",
            evidence_source="1773 countermodels;2182 closed-wrong-object guard;1153 no-tautology guard",
            missing_for_current_MTS="period-charge lock and parent-selected topological representative",
            blocks_claim=True,
        ),
        base_row(
            theorem_id="SOT2204_3_first_row_status",
            statement="R_eq_integral is the first equality residual row but remains missing/source-free.",
            status="SOURCE_READY_UNFILLED_NONCLAIM",
            evidence_source="1013;1015;1773;2182;1153",
            missing_for_current_MTS="numeric/theorem value, M_H_ref denominator, source path, units, arena projection",
            blocks_claim=True,
        ),
        base_row(
            theorem_id="SOT2204_4_route_verdict",
            statement="The topological-Hilbert branch is serious but currently conditional; the next real proof target is parent action/descent, not another equality restatement.",
            status="MERGED_TO_PARENT_ACTION_DESCENT_FRONTIER",
            evidence_source="2183;2184;2185;2186 chain",
            missing_for_current_MTS="MTS EH fixed-point descent, PiM lock, source measure glue, boundary zero, radial readout ownership",
            blocks_claim=True,
        ),
    ]


def r_eq_first_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            row_id="REQ2204_0_R_eq_integral",
            source_row="OBS1013_3;REB1015_0;REQ1773_0;EFR2182_0;REQ1153_4",
            quantity="R_eq_integral",
            definition="finite-shell/source-normalized integral of Pi_M J_H - J_M_top - dB_zero",
            units="dimensionless_after_M_H_ref_normalization",
            current_value="MISSING_R_EQ_INTEGRAL",
            required_inputs="system_id;r1;r2;PiM_JH_profile;JM_top_profile;B_zero_profile;M_H_ref;source_path;arena_projection",
            status="FIRST_ROW_EXISTS_BUT_UNFILLED",
            score_ready=False,
        ),
        base_row(
            row_id="REQ2204_1_M_H_ref",
            source_row="REQ1773_4;REB1015_5;REQ1153_6",
            quantity="M_H_ref",
            definition="same-frame Hilbert/Hamiltonian source charge denominator for equality residuals",
            units="mass_or_GM_source_charge",
            current_value="MISSING_M_H_REF",
            required_inputs="tau;e_obs;H_tau;H_ref;surface;reference;units;source_path",
            status="DENOMINATOR_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="REQ2204_2_B_zero_flux",
            source_row="OBS1013_4;REB1015_1;REQ1773_2;EFR2182_1",
            quantity="B_zero_flux",
            definition="compact linked-boundary flux of exact/reference improvement dB_zero",
            units="GM_flux_or_dimensionless_after_M_H_ref_normalization",
            current_value="MISSING_B_ZERO_FLUX",
            required_inputs="boundary_type;reference_choice;B_zero_definition;flux_value;M_H_ref;source_path",
            status="BOUNDARY_ZERO_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="REQ2204_3_period_lock",
            source_row="PCL1773_0;PCL1773_4",
            quantity="Delta_period",
            definition="max linked-surface period mismatch integral_L(Pi_M J_H-J_M_top)",
            units="dimensionless_or_GM_flux_after_M_H_ref",
            current_value="MISSING_PERIOD_LOCK",
            required_inputs="linked_cycles;surface_integrals;W_source;tau;M_H_ref;source_path",
            status="PERIOD_CHARGE_LOCK_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="REQ2204_4_selector_residual",
            source_row="WST2183;SRR2183_0",
            quantity="epsilon_W_selector",
            definition="charge/domain shift from parent source worldtube selection W_source=supp(J_H[e_obs,tau])",
            units="dimensionless_or_GM_flux",
            current_value="MISSING_PARENT_WORLDTUBE_SELECTOR",
            required_inputs="parent_action;J_H_definition;e_obs;tau;linking_surfaces;readout_independence",
            status="SELECTOR_MISSING",
            score_ready=False,
        ),
        base_row(
            row_id="REQ2204_5_parent_action_descent",
            source_row="MAS2184;DEG2186",
            quantity="epsilon_EH_fixed_point_descent",
            definition="failure of MTS parent action to descend to EH local fixed point with silent extra sectors",
            units="dimensionless_or_declared",
            current_value="MISSING_PARENT_DESCENT_PROOF",
            required_inputs="explicit_parent_action;double_zero_conditions;PiM_lock;boundary_zero;radial_readout_owner",
            status="FRONTIER_ROW_SELECTED",
            score_ready=False,
        ),
    ]


def frontier_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            frontier_id="FR2204_0_repeat_2204_literal",
            candidate="repeat topological-Hilbert equality derivation",
            selection_status="rejected_as_duplicate",
            reason="1015, 1773 and 2182 already record the clean conditional theorem and nonclaim R_eq rows.",
            next_use="only return if new parent-signature evidence appears",
        ),
        base_row(
            frontier_id="FR2204_1_source_backed_R_eq_now",
            candidate="acquire numeric/source-backed R_eq row immediately",
            selection_status="held_parallel",
            reason="possible fallback, but no current local source profile/M_H_ref denominator exists to fill honestly.",
            next_use="use if parent-action/descent route fails or produces a concrete finite residual formula",
        ),
        base_row(
            frontier_id="FR2204_2_parent_action_descent",
            candidate="merge to minimal parent-action/EH fixed-point descent frontier",
            selection_status="selected_next",
            reason="2184-2186 already moved beyond equality slogans into coefficient extraction, 2PN gauge debt, PiM/source/boundary descent gates.",
            next_use="build 2205 as the current-frontier descent synthesis: what is conditionally won, what remains unsigned, and which clause to attack first",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2204_0_conditional_theorem",
            gate="topological-Hilbert same-object theorem exists",
            status="PASS_NONCLAIM",
            implication="conditional math is clean but not a current MTS proof.",
        ),
        base_row(
            gate_id="CG2204_1_current_equality",
            gate="Pi_M J_H = J_M_top + dB_zero is parent-signed",
            status="BLOCKED_NONCLAIM",
            implication="same worldtube, period-charge lock, M_H_ref and boundary-zero clauses remain unsigned.",
        ),
        base_row(
            gate_id="CG2204_2_R_eq_first_row",
            gate="R_eq first row is source-backed",
            status="BLOCKED_NONCLAIM",
            implication="R_eq row exists as schema/placeholder only; no source path/value/denominator.",
        ),
        base_row(
            gate_id="CG2204_3_no_recircle",
            gate="avoid duplicate derivation loop",
            status="PASS_GUARDRAIL",
            implication="2204 records existing equality work and moves to parent-action/descent frontier.",
        ),
        base_row(
            gate_id="CG2204_4_local_gr_newton",
            gate="Newton/local-GR reduction can be claimed",
            status="BLOCKED_NONCLAIM",
            implication="no Newton, local-GR, PPN, WEP, R10, clock, orbital or public claim follows from 2204.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2204_0_topological_status",
            decision="CONDITIONAL_THEOREM_ALREADY_AVAILABLE",
            rationale="the topological-Hilbert same-object theorem is a valid conditional route, already recorded in 1015/1773/2182.",
            next_action="do not reprove unless new parent signatures are found",
        ),
        base_row(
            decision_id="DEC2204_1_claim_status",
            decision="CURRENT_MTS_EQUALITY_NOT_PARENT_SIGNED",
            rationale="R_eq=0, B_zero_flux=0, period-charge lock, M_H_ref and source selector remain missing or conditional.",
            next_action="keep all equality/source-normalization rows nonclaim",
        ),
        base_row(
            decision_id="DEC2204_2_anti_circling",
            decision="ROUTE_MERGE_INSTEAD_OF_DUPLICATE_LOOP",
            rationale="2183/2184 already advanced the route to a minimal parent-action and EH fixed-point descent contract.",
            next_action="carry 2203 readout obstruction into that existing frontier",
        ),
        base_row(
            decision_id="DEC2204_3_next",
            decision="MOVE_TO_CURRENT_FRONTIER_DESCENT_SYNTHESIS",
            rationale="the next useful work is to synthesize 2185/2186 conditional wins with 2199-2203 vector debts and choose the first parent-signature clause to derive.",
            next_action="2205 should attack MTS EH fixed-point descent/PiM/source/boundary/radial-readout ownership rather than restating R_eq",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2204_0_2205",
            selection_status="selected",
            target_file="2205-Y5-R2FR-current-frontier-EH-descent-PiM-source-readout-synthesis.md",
            target_script="scripts/Y5_R2FR_current_frontier_EH_descent_PiM_source_readout_synthesis_2205.py",
            objective="merge the 2185/2186 conditional EH-to-v wins with the 2199-2203 PPN/readout residual vector, then select the first parent-signature clause to derive or demote",
            success_condition="a non-duplicative frontier map identifies which of EH descent, PiM lock, source measure glue, boundary zero, extra-sector double-zero, or radial readout ownership is the next highest-leverage derivation target",
            do_not_do="do not restate R_eq as new work, do not claim local GR, do not use GitHub action, do not treat EH extraction as MTS proof without descent signatures",
        ),
        base_row(
            route_id="NEXT2204_1_R_eq_source_parallel",
            selection_status="held_parallel",
            target_file="2205b-Y5-R2FR-source-backed-R-eq-MHref-Bzero-input-acquisition.md",
            target_script="scripts/Y5_R2FR_source_backed_R_eq_MHref_Bzero_input_acquisition_2205b.py",
            objective="if derivation stalls, acquire first source-backed R_eq/M_H_ref/B_zero/period-lock row with units and claim=false",
            success_condition="at least one row has real source path, declared units, normalization, arena projection and valid_for_claim=false",
            do_not_do="do not fabricate numeric residuals, do not score placeholders, do not rely on cancellation",
        ),
    ]


def write_branch_copies() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["frontier"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["r_eq_first_rows"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["route_merge"], BRANCH_COPIES["beta_docs"]),
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
    route_rows: list[dict[str, Any]],
    same_rows: list[dict[str, Any]],
    r_eq_rows: list[dict[str, Any]],
    frontier_rows_data: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, passed: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if passed else "FAIL", detail=detail))

    add("VAL2204_00_sources_exist", all(truthy(r["path_exists"]) for r in source_rows), f"{sum(truthy(r['path_exists']) for r in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2204_01_needles_found", all(truthy(r["needles_found"]) for r in source_rows), f"{sum(truthy(r['needles_found']) for r in source_rows)}/{len(source_rows)} source needle sets found")
    add("VAL2204_02_route_merge", any(r["route_id"] == "RMG2204_5_verdict" and r["status"] == "ROUTE_MERGED_NO_DUPLICATE_REDERIVATION" for r in route_rows), "route merge prevents duplicate topological-Hilbert loop")
    add("VAL2204_03_same_object", any(r["theorem_id"] == "SOT2204_1_current_branch" and r["status"] == "NOT_PARENT_SIGNED" for r in same_rows), "current equality remains not parent-signed")
    add("VAL2204_04_r_eq_rows", len(r_eq_rows) == 6 and all(not truthy(r.get("score_ready", False)) for r in r_eq_rows), "R_eq/MHref/Bzero/frontier rows retained nonclaim")
    add("VAL2204_05_frontier_selected", any(r["frontier_id"] == "FR2204_2_parent_action_descent" and r["selection_status"] == "selected_next" for r in frontier_rows_data), "parent-action/descent frontier selected")
    add("VAL2204_06_claim_gate", any(r["gate_id"] == "CG2204_4_local_gr_newton" and r["status"] == "BLOCKED_NONCLAIM" for r in claim_rows), "local-GR remains blocked")
    add("VAL2204_07_decision", any(r["decision"] == "MOVE_TO_CURRENT_FRONTIER_DESCENT_SYNTHESIS" for r in decision_rows_data), "decision selects non-duplicative 2205 frontier synthesis")
    add("VAL2204_08_next_target", any(r["route_id"] == "NEXT2204_0_2205" and r["selection_status"] == "selected" for r in next_rows), "2205 frontier synthesis target selected")

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["route_merge"],
        OUTPUTS["same_object"],
        OUTPUTS["r_eq_first_rows"],
        OUTPUTS["frontier"],
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
    add("VAL2204_09_csv_parse", parse_ok_all, "; ".join(parse_parts))
    add("VAL2204_10_branch_copies", len(copy_rows) == 3 and all(truthy(r["copied"]) and truthy(r["parse_ok"]) for r in copy_rows), ";".join(str(r["target_path"]) for r in copy_rows))

    all_generated_rows = [
        *source_rows,
        *route_rows,
        *same_rows,
        *r_eq_rows,
        *frontier_rows_data,
        *claim_rows,
        *decision_rows_data,
        *next_rows,
        *copy_rows,
    ]
    add("VAL2204_11_claim_flags_false", all(not truthy(r.get("valid_for_claim", False)) and not truthy(r.get("claim_allowed", False)) for r in all_generated_rows), "all generated rows keep valid_for_claim=false and claim_allowed=false")
    add("VAL2204_12_score_flags_false", all(not truthy(r.get("score_ready", False)) for r in r_eq_rows), "no R_eq/frontier row is score-ready")
    add("VAL2204_13_formalization_clean", not formalization_has_2204_artifacts(), "formalization-workbench has no 2204 artifacts")
    add("VAL2204_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), str(ROOT / "scripts" / "__pycache__"))
    overall = all(row["status"] == "PASS" for row in rows)
    add("VAL2204_OVERALL", overall, "2204 merges existing topological-Hilbert work and selects current-frontier EH descent/PiM/source/readout synthesis next")
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    route_rows: list[dict[str, Any]],
    same_rows: list[dict[str, Any]],
    r_eq_rows: list[dict[str, Any]],
    frontier_rows_data: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_data: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_data: list[dict[str, Any]],
) -> None:
    sections = [
        "# 2204 - Y5/R2FR Topological-Hilbert Equality Or R_eq First Row",
        "",
        "## Current Verdict",
        "",
        "2204 does **not** pretend to discover the topological-Hilbert route from scratch. The corpus already did that work in 1015, 1773, 2182, and 2183. The conditional theorem is clean: if `Pi_M J_H` and `J_M_top` are the same compact Hilbert source class, then their difference is exact up to `R_eq` and boundary/reference terms.",
        "",
        "The current MTS branch still does **not** parent-sign that equality. `R_eq`, `M_H_ref`, `B_zero_flux`, period-charge lock, worldtube selector, PiM/Hamiltonian lock, source measure glue, and boundary/reference zero remain open or placeholder-only.",
        "",
        "So the useful 2204 move is anti-circling: merge the 2203 readout obstruction into the already-built 2182-2186 local-GR chain, keep all equality rows nonclaim, and move the next work to the current frontier: EH fixed-point descent, PiM/source/boundary/radial-readout ownership.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Route Merge Audit",
        "",
        md_table(route_rows, ["route_id", "route_piece", "status", "implication", "duplicate_risk", "valid_for_claim"]),
        "",
        "## Same-Object Theorem Status",
        "",
        md_table(same_rows, ["theorem_id", "statement", "status", "missing_for_current_MTS", "blocks_claim", "valid_for_claim"]),
        "",
        "## R_eq First Row Register",
        "",
        md_table(r_eq_rows, ["row_id", "quantity", "current_value", "status", "required_inputs", "score_ready", "valid_for_claim"]),
        "",
        "## Frontier Selection",
        "",
        md_table(frontier_rows_data, ["frontier_id", "candidate", "selection_status", "reason", "next_use", "valid_for_claim"]),
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
        "## Working Interpretation",
        "",
        "This is exactly the anti-merry-go-round checkpoint. The topological route is real but already conditionally mapped. Repeating it would be token-burn cosplay. The sharper move is to ask whether MTS owns the EH fixed point, PiM mass map, source measure, boundary zero, extra-sector double zeros, and radial readout map strongly enough to inherit the conditional EH/v wins from 2185/2186.",
        "",
        "Best next attack: `2205` should synthesize those current-frontier clauses and choose one to derive first, rather than restating `R_eq` one more time with a new hat on.",
    ]
    DOC.write_text("\n".join(sections) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    route_rows = route_merge_rows()
    same_rows = same_object_rows()
    r_eq_rows = r_eq_first_rows()
    frontier_rows_data = frontier_rows()
    claim_rows = claim_gate_rows()
    decision_rows_data = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["route_merge"], route_rows)
    write_csv(OUTPUTS["same_object"], same_rows)
    write_csv(OUTPUTS["r_eq_first_rows"], r_eq_rows)
    write_csv(OUTPUTS["frontier"], frontier_rows_data)
    write_csv(OUTPUTS["claim_gate"], claim_rows)
    write_csv(OUTPUTS["decision"], decision_rows_data)
    write_csv(OUTPUTS["next_target"], next_rows)
    copy_rows = write_branch_copies()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_data = validation_rows(
        source_rows,
        route_rows,
        same_rows,
        r_eq_rows,
        frontier_rows_data,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_data)
    write_doc(
        source_rows,
        route_rows,
        same_rows,
        r_eq_rows,
        frontier_rows_data,
        claim_rows,
        decision_rows_data,
        next_rows,
        copy_rows,
        validation_rows_data,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
