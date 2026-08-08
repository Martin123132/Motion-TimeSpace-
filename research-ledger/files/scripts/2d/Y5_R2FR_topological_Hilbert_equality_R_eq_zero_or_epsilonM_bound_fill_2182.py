from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2182"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2182_SOURCE_REGISTER.csv",
    "equality_audit": OUT / "P8_Y5_PARENT_QLOC_2182_TOPOLOGICAL_HILBERT_EQUALITY_AUDIT.csv",
    "bzero_conditions": OUT / "P8_Y5_PARENT_QLOC_2182_REQ_BZERO_ZERO_CONDITIONS.csv",
    "epsilon_map": OUT / "P8_Y5_PARENT_QLOC_2182_EPSILON_M_BOUND_MAP.csv",
    "finite_rows": OUT / "P8_Y5_PARENT_QLOC_2182_FINITE_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2182_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2182_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2182_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2182_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2182_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2182_TOPOLOGICAL_HILBERT_EQUALITY_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2182_EQUALITY_AUDIT_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "TOPOLOGICAL_HILBERT_EQUALITY_R_EQ_2182_NONCLAIM.csv",
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
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2182_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2182-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2182*",
        "*P8_Y5_BRR545_2182*",
        "*Y5_R2FR_topological_Hilbert_equality_R_eq_zero_or_epsilonM_bound_fill_2182*",
        "*JR2182*",
        "*TOPOLOGICAL_HILBERT_EQUALITY_R_EQ_2182*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2181_handoff",
            ROOT / "2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md",
            ["NEXT2181_0_2182", "TOPOLOGICAL_HILBERT_EQUALITY_OR_REQ_BOUND_NEXT"],
            "2181 selects topological-Hilbert equality and R_eq/B_zero fill as the next source-normalization gate.",
        ),
        (
            "2181_validation",
            OUT / "P8_Y5_BRR545_2181_VALIDATION.csv",
            ["VAL2181_OVERALL", "PASS"],
            "2181 validation passed before 2182 continues the chain.",
        ),
        (
            "1015_same_object_lemma",
            ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md",
            ["same-object lemma", "Pi_M J_H = J_M_top + dB_zero", "R_eq_integral"],
            "1015 records the conditional de Rham/Poincare-dual equality theorem and residual rows.",
        ),
        (
            "1014_commutator",
            ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            ["[d,Pi_M]J_H=0", "Pi_M J_H = J_M_top + dB_zero", "MISSING_R_EQ_INTEGRAL"],
            "1014 shows commutator zero still needs topological-Hilbert equality or finite residual rows.",
        ),
        (
            "topological_hilbert_attempt",
            OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
            ["EH501_0_equality_statement", "Pi_M J_H = J_M_top + dB_zero + R_eq", "R_eq is not parent-derived zero"],
            "prior attempt names the equality residual and refuses reference-only zero.",
        ),
        (
            "topological_hilbert_obstructions",
            OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
            ["OB501_0_independent_topological_label", "OB501_1_worldtube_domain_selection", "OB501_2_boundary_improvement"],
            "obstruction map identifies conserved-wrong-object, worldtube, and boundary improvement risks.",
        ),
        (
            "topological_hilbert_routes",
            OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ROUTE_TESTS.csv",
            ["R501_0_define_top_charge_from_Hilbert_source", "R501_1_late_equality_multiplier", "R501_3_bound_runner"],
            "route split says source-defined topological charge is best, late multiplier is rejected, bound runner is fallback.",
        ),
        (
            "source_measure_flux",
            OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
            ["T509_0_charge_identity_needed", "T509_1_flux_closure", "T509_2_no_extra_mass_channel"],
            "source-measure theorem records the charge identity, flux closure, and no-extra-channel requirements.",
        ),
    ]
    rows = []
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


def equality_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "TEA2182_0_identity_target",
            "topological-Hilbert equality with residual",
            "Pi_M J_H = J_M_top + dB_zero + R_eq.",
            "EXACT_IDENTITY_DEFINITION",
            "R_eq is the named failure of the topological route, not a decorative term.",
        ),
        (
            "TEA2182_1_same_worldtube_class",
            "same compact Hilbert source class",
            "If Pi_M J_H and J_M_top represent the same compact-support Hilbert worldtube charge class, then their difference is exact up to R_eq.",
            "EXACT_CONDITIONAL_EQUALITY_THEOREM",
            "topology can work only after the parent action defines Q_M from the Hilbert source, not from an independent label.",
        ),
        (
            "TEA2182_2_closed_wrong_object_guard",
            "closed topological current is not enough",
            "dJ_M_top=0 does not imply d(Pi_M J_H)=0 unless R_eq=0 and the compact boundary improvement has zero flux.",
            "CONSERVATION_NOT_ENOUGH",
            "this blocks the common cheat: conserving the wrong object and calling it measured mass.",
        ),
        (
            "TEA2182_3_R_eq_zero",
            "residual equality zero",
            "R_eq := Pi_M J_H - J_M_top - dB_zero must be parent-derived zero or source-backed bounded.",
            "R_EQ_ZERO_NOT_DERIVED",
            "current MTS cannot claim measured source closure from the topological route.",
        ),
        (
            "TEA2182_4_commutator_link",
            "commutator inheritance",
            "d(Pi_M J_H)=dR_eq because dJ_M_top=0 and d^2B_zero=0 under the same-class assumptions.",
            "EXACT_CONDITIONAL_COMMUTATOR_LINK",
            "if R_eq is not zero, I_commutator is a finite live row.",
        ),
        (
            "TEA2182_5_worldtube_selector",
            "parent source worldtube selector",
            "The source worldtube W_source, Hilbert measure, linking surfaces, and observed time generator must be fixed before readout.",
            "WORLDTUBE_SELECTOR_NOT_DERIVED",
            "otherwise Q_M can be tuned after seeing the exterior orbit/source data.",
        ),
        (
            "TEA2182_6_no_late_multiplier",
            "late equality multiplier rejected",
            "S_glue = integral Lambda_eq wedge (Pi_M J_H - J_M_top - dB_zero) imposes equality only if Lambda_eq has an independent parent origin.",
            "CLOSURE_ONLY_IF_USED",
            "a multiplier that simply demands Newton closure is bookkeeping, not derivation.",
        ),
        (
            "TEA2182_7_current_verdict",
            "topological-Hilbert equality for current branch",
            "The conditional theorem is clean, but R_eq=0, B_zero_flux=0, worldtube ownership, and extra-channel silence are not parent-signed.",
            "CURRENT_CLAIM_FAILS_NONCLAIM",
            "2182 should feed finite residual rows or the next parent-selector theorem, not a Newton/local-GR claim.",
        ),
    ]
    return [
        base_row(
            audit_id=audit_id,
            gate=gate,
            statement=statement,
            status=status,
            implication=implication,
        )
        for audit_id, gate, statement, status, implication in specs
    ]


def bzero_condition_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "BZ2182_0_exact_term",
            "exact improvement term",
            "dB_zero may shift representatives without changing the de Rham class.",
            "REFERENCE_REPRESENTATIVE_ALLOWED",
            "allowed only as a representative change, not a hidden source charge.",
        ),
        (
            "BZ2182_1_compact_flux_zero",
            "compact linked-boundary zero flux",
            "Integral_boundary dB_zero = 0 for the compact linked boundary used in M_eff scoring.",
            "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE",
            "if nonzero, the Newton source coefficient shifts by boundary bookkeeping.",
        ),
        (
            "BZ2182_2_single_reference",
            "single fixed reference",
            "The reference for B_zero must be fixed once by the parent action/source worldtube, not fitted per arena.",
            "MISSING_FIXED_REFERENCE_CERTIFICATE",
            "arena-specific reference choices would mimic measured-G calibration.",
        ),
        (
            "BZ2182_3_no_asymptotic_leak",
            "no asymptotic or inner-boundary leak",
            "The improvement term must have no hidden flux through infinity, inner excision surfaces, or source-hole boundaries.",
            "MISSING_BOUNDARY_TOPOLOGY_CERTIFICATE",
            "otherwise local and orbital masses can differ by a surface hair row.",
        ),
        (
            "BZ2182_4_no_stress_shift",
            "no metric/projector stress shift",
            "The B_zero representative must not reintroduce delta_g Pi_M or projector-stress terms in the PPN/vector residuals.",
            "MISSING_PROJECTOR_STRESS_SILENCE",
            "a zero-flux identity at monopole order is not enough for local-GR reduction.",
        ),
        (
            "BZ2182_5_current_verdict",
            "B_zero zero proof for current branch",
            "No current source provides B_zero_flux=0 with fixed source worldtube, fixed reference, and projector-stress silence.",
            "B_ZERO_FLUX_ZERO_NOT_DERIVED",
            "retain B_zero_flux as a finite nonclaim row.",
        ),
    ]
    return [
        base_row(
            condition_id=condition_id,
            condition=condition,
            statement=statement,
            status=status,
            implication=implication,
        )
        for condition_id, condition, statement, status, implication in specs
    ]


def epsilon_map_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EMB2182_0_R_eq_integral",
            "R_eq_integral",
            "M_H_ref^-1 integral_link R_eq or equivalent shell-normalized equality residual.",
            "MISSING_R_EQ_ZERO_OR_VALUE",
            "feeds epsilon_M and I_commutator; blocks measured-GM source closure.",
        ),
        (
            "EMB2182_1_B_zero_flux",
            "B_zero_flux",
            "M_H_ref^-1 integral_boundary dB_zero for the compact linked boundary/reference.",
            "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE",
            "feeds epsilon_M as a boundary/reference source shift.",
        ),
        (
            "EMB2182_2_I_commutator",
            "I_commutator",
            "M_H_ref^-1 integral_A [d,Pi_M]J_H inherited when Pi_M is not a fixed chain map or R_eq varies across the annulus.",
            "MISSING_I_COMMUTATOR_ZERO_OR_VALUE",
            "feeds radial measured-mass drift and PPN/source residual rows.",
        ),
        (
            "EMB2182_3_epsilon_worldtube",
            "epsilon_worldtube",
            "charge shift from choosing W_source, linking surface, source support, or time generator.",
            "MISSING_WORLDTUBE_SELECTOR_ZERO_OR_VALUE",
            "feeds source normalization and frame/domain residual rows.",
        ),
        (
            "EMB2182_4_epsilon_extra",
            "epsilon_extra_current",
            "nonEH, memory, symplectic-boundary, domain, range, frame, and projector mass-channel residuals.",
            "MISSING_EXTRA_CHANNEL_ZERO_OR_VALUE",
            "prevents closed Pi_M J_H from being the full observed mass source.",
        ),
        (
            "EMB2182_5_epsilon_calibration",
            "epsilon_calibration",
            "single absolute calibration residual linking Hilbert source charge to Newton coefficient.",
            "MISSING_ABSOLUTE_CALIBRATION_ZERO_OR_VALUE",
            "keeps measured G and fitted GM from hiding a source mismatch.",
        ),
        (
            "EMB2182_6_total_envelope",
            "epsilon_M_abs",
            "abs(epsilon_M) <= abs(epsilon_worldtube)+abs(I_commutator)+abs(R_eq_integral)+abs(B_zero_flux)+abs(epsilon_extra)+abs(epsilon_calibration).",
            "EXACT_ABSOLUTE_LEDGER",
            "no cancellation credit is allowed until a parent identity proves signed cancellation.",
        ),
        (
            "EMB2182_7_Newton_link",
            "Delta_Newton_v",
            "Delta_Newton_v = (1+delta_KC)(1+epsilon_M)-1.",
            "EXACT_LINK_TO_2179_2181",
            "even a perfect v-field action still fails Newton if epsilon_M is not zero or bounded.",
        ),
    ]
    return [
        base_row(
            map_id=map_id,
            symbol=symbol,
            definition=definition,
            status=status,
            implication=implication,
        )
        for map_id, symbol, definition, status, implication in specs
    ]


def finite_row_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EFR2182_0_R_eq",
            "R_eq_integral",
            "normalized integral of Pi_M J_H - J_M_top - dB_zero over the linked source boundary or shell",
            "MISSING_R_EQ_ZERO_OR_VALUE",
            "dimensionless_after_M_H_ref_normalization",
            "Newton;PPN;R10;R11",
            "MISSING_NUMERIC_VALUE",
        ),
        (
            "EFR2182_1_B_zero",
            "B_zero_flux",
            "compact linked-boundary flux of dB_zero/reference improvement",
            "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE",
            "GM_flux_or_dimensionless_after_M_H_ref_normalization",
            "Newton;PPN;R7;R8;R9;R11",
            "MISSING_NUMERIC_VALUE",
        ),
        (
            "EFR2182_2_I_commutator",
            "I_commutator",
            "finite annulus integral of [d,Pi_M]J_H or dR_eq between linked surfaces",
            "MISSING_I_COMMUTATOR_ZERO_OR_VALUE",
            "GM_flux_or_dimensionless_after_M_H_ref_normalization",
            "Newton;R10;R11;radial-source",
            "MISSING_NUMERIC_VALUE",
        ),
        (
            "EFR2182_3_worldtube",
            "epsilon_worldtube",
            "source-domain, linking-surface, observed-time-generator, and Hilbert measure mismatch",
            "MISSING_WORLDTUBE_SELECTOR_ZERO_OR_VALUE",
            "dimensionless",
            "Newton;PPN;WEP;orbital-source",
            "MISSING_NUMERIC_VALUE",
        ),
        (
            "EFR2182_4_extra",
            "epsilon_extra_current",
            "nonEH/symplectic/memory/domain/range/frame/projector extra source-current channels",
            "MISSING_EXTRA_CHANNEL_ZERO_OR_VALUE",
            "dimensionless_or_GM_flux",
            "Newton;PPN;WEP;R10;R11",
            "MISSING_NUMERIC_VALUE",
        ),
        (
            "EFR2182_5_calibration",
            "epsilon_calibration",
            "absolute calibration residual between Hilbert source charge and exterior Newton coefficient",
            "MISSING_ABSOLUTE_CALIBRATION_ZERO_OR_VALUE",
            "dimensionless",
            "Newton;PPN;orbital",
            "MISSING_NUMERIC_VALUE",
        ),
        (
            "EFR2182_6_total",
            "epsilon_M_abs",
            "absolute no-cancellation envelope for measured source normalization",
            "MISSING_COMPONENT_INPUTS",
            "dimensionless",
            "Newton;local-GR;R10;R11",
            "MISSING_NUMERIC_VALUE",
        ),
        (
            "EFR2182_7_Delta_Newton",
            "Delta_Newton_v_link",
            "(1+delta_KC)(1+epsilon_M)-1 with delta_KC inherited from the v-action/source coefficient gate",
            "MISSING_DELTA_KC_AND_EPSILON_M_INPUTS",
            "dimensionless",
            "Newton;PPN;local-GR",
            "MISSING_NUMERIC_VALUE",
        ),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            status=status,
            units=units,
            observable_link=observable_link,
            value=value,
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
        )
        for row_id, symbol, definition, status, units, observable_link, value in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "CG2182_0_conditional_math",
            "conditional topological-Hilbert theorem is mathematically clean",
            "PASS_GUARDRAIL",
            "same compact-support class plus zero residual gives exactness up to zero-flux improvement.",
        ),
        (
            "CG2182_1_same_object",
            "Pi_M J_H and J_M_top are parent-signed as the same Hilbert source object",
            "BLOCKED_NONCLAIM",
            "source worldtube, Hilbert measure, topological representative, and observed time generator are not parent-signed.",
        ),
        (
            "CG2182_2_R_eq_zero",
            "R_eq=0 is derived for current MTS",
            "BLOCKED_NONCLAIM",
            "only a residual definition exists; no parent identity sets it to zero.",
        ),
        (
            "CG2182_3_B_zero_flux_zero",
            "B_zero_flux=0 is derived for current MTS",
            "BLOCKED_NONCLAIM",
            "compact boundary/reference zero is not sourced.",
        ),
        (
            "CG2182_4_epsilon_M_claim",
            "epsilon_M=0 or bounded tightly enough for Newton/local-GR",
            "BLOCKED_NONCLAIM",
            "finite rows remain placeholders with missing source paths and values.",
        ),
        (
            "CG2182_5_Newton_local_GR",
            "Newton/local-GR reduction can reopen from topological route",
            "BLOCKED_NONCLAIM",
            "measured source closure and PPN/calibration stability are not established.",
        ),
        (
            "CG2182_6_no_cheat_guard",
            "late multiplier, reference-only zero, and closed-wrong-object promotion are forbidden",
            "PASS_GUARDRAIL",
            "2182 keeps all equality/bound rows nonclaim.",
        ),
    ]
    return [
        base_row(
            gate_id=gate_id,
            gate=gate,
            status=status,
            implication=implication,
        )
        for gate_id, gate, status, implication in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "DEC2182_0_exact_conditional_theorem",
            "EXACT_CONDITIONAL_THEOREM_WRITTEN",
            "If the parent action defines the topological charge as the Poincare dual of the same compact Hilbert source worldtube, equality follows up to exact plus residual terms.",
            "selected",
        ),
        (
            "DEC2182_1_claim_status",
            "R_EQ_AND_B_ZERO_STILL_BLOCK",
            "Current sources do not prove R_eq=0 or B_zero_flux=0, so topology remains a promising route but not Newton evidence.",
            "selected",
        ),
        (
            "DEC2182_2_finite_rows",
            "EPSILON_M_BOUND_ROWS_RETAINED",
            "R_eq_integral, B_zero_flux, I_commutator, worldtube, extra-channel and calibration rows are explicit nonclaim finite inputs.",
            "selected",
        ),
        (
            "DEC2182_3_next",
            "WORLDTUBE_HILBERT_SOURCE_SELECTOR_OR_R_EQ_FILL_NEXT",
            "The shortest honest route is to prove the parent selector for W_source/rho_H/time-generator/class/reference, or acquire source-backed R_eq/B_zero rows.",
            "selected",
        ),
    ]
    return [
        base_row(
            decision_id=decision_id,
            decision=decision,
            rationale=rationale,
            selection_status=status,
        )
        for decision_id, decision, rationale, status in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2182_0_2183",
            selection_status="selected",
            target_file="2183-Y5-R2FR-worldtube-Hilbert-source-selector-and-zero-boundary-flux-or-R_eq-fill.md",
            target_script="scripts/Y5_R2FR_worldtube_Hilbert_source_selector_and_zero_boundary_flux_or_R_eq_fill_2183.py",
            objective="derive the parent-owned compact Hilbert source worldtube, same-frame source measure, topological representative, and zero boundary flux; otherwise fill R_eq/B_zero/I_commutator finite rows",
            success_condition="W_source, rho_H dV_H, observed time generator, J_M_top=PD(W_source), R_eq=0, B_zero_flux=0, and no extra current channels are parent-signed; otherwise source-backed nonclaim rows exist",
            do_not_do="do not use a closed wrong topological charge, late equality multiplier, reference-only zero, post-readout worldtube, fitted GM calibration, or GitHub action",
        ),
        base_row(
            route_id="NEXT2182_1_numeric_parallel",
            selection_status="held_parallel",
            target_file="2183b-Y5-R2FR-first-source-backed-R_eq-B_zero-Icommutator-input.md",
            target_script="scripts/Y5_R2FR_first_source_backed_R_eq_B_zero_Icommutator_input_2183b.py",
            objective="if derivation stalls, acquire the first source-backed residual input with units, normalization, arena projection, and claim=false",
            success_condition="at least one R_eq/B_zero/I_commutator/worldtube row has a real source path, positive/finite unit normalization, and remains nonclaim until the full envelope closes",
            do_not_do="do not fabricate numeric residuals, use placeholders as evidence, or score cancellation-only rows",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["finite_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["equality_audit"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["epsilon_map"], BRANCH_COPIES["source_weight"]),
    ]
    rows = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(base_row(copy_id=copy_id, source_path=str(source), target_path=str(target), copied=target.exists()))
    return rows


def all_claim_flags_false(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if str(row.get("claim_allowed", "")).lower() == "true":
                return False
            if str(row.get("valid_for_claim", "")).lower() == "true":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []
    source_rows = rows_by_name["source_register"]
    validations.append(base_row(validation_id="VAL2182_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2182_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    equality_statuses = {row["status"] for row in rows_by_name["equality_audit"]}
    equality_pass = {"EXACT_CONDITIONAL_EQUALITY_THEOREM", "R_EQ_ZERO_NOT_DERIVED", "CURRENT_CLAIM_FAILS_NONCLAIM"}.issubset(equality_statuses)
    validations.append(base_row(validation_id="VAL2182_02_equality_audit", status="PASS" if equality_pass else "FAIL", detail="conditional equality theorem written, R_eq zero not claimed"))

    bzero_statuses = {row["status"] for row in rows_by_name["bzero_conditions"]}
    bzero_pass = "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE" in bzero_statuses and "B_ZERO_FLUX_ZERO_NOT_DERIVED" in bzero_statuses
    validations.append(base_row(validation_id="VAL2182_03_bzero_conditions", status="PASS" if bzero_pass else "FAIL", detail="B_zero zero-flux conditions are explicit and unsigned"))

    epsilon_statuses = {row["status"] for row in rows_by_name["epsilon_map"]}
    epsilon_pass = "EXACT_ABSOLUTE_LEDGER" in epsilon_statuses and "EXACT_LINK_TO_2179_2181" in epsilon_statuses
    validations.append(base_row(validation_id="VAL2182_04_epsilon_bound_map", status="PASS" if epsilon_pass else "FAIL", detail="epsilon_M envelope and Delta_Newton_v link written"))

    finite_rows = rows_by_name["finite_rows"]
    finite_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) and row.get("source_path") == "MISSING_SOURCE_PATH" for row in finite_rows)
    validations.append(base_row(validation_id="VAL2182_05_finite_rows_nonclaim", status="PASS" if finite_ok else "FAIL", detail=f"finite rows={len(finite_rows)} remain missing/source-free/nonclaim"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    claim_pass = "BLOCKED_NONCLAIM" in claim_statuses and "PASS_GUARDRAIL" in claim_statuses
    validations.append(base_row(validation_id="VAL2182_06_claim_gate", status="PASS" if claim_pass else "FAIL", detail="claim gate blocks Newton/local-GR and keeps no-cheat guard"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2182_07_decision", status="PASS" if "WORLDTUBE_HILBERT_SOURCE_SELECTOR_OR_R_EQ_FILL_NEXT" in decision_text else "FAIL", detail="decision selects parent worldtube/source selector or R_eq fill next"))

    validations.append(base_row(validation_id="VAL2182_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2183" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2183 worldtube-Hilbert selector target selected"))

    validations.append(base_row(validation_id="VAL2182_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2182_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2182_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2182_artifacts()
    validations.append(base_row(validation_id="VAL2182_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2182 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2182_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2182_OVERALL", status="PASS" if overall else "FAIL", detail="2182 writes exact conditional topological-Hilbert equality gate and keeps source closure blocked/nonclaim"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2182 - Y5/R2FR Topological-Hilbert Equality R_eq Zero Or EpsilonM Bound Fill

## Current Verdict

2182 gets us closer, but it does **not** let us claim local GR/Newton yet.

The clean theorem is now explicit:

`Pi_M J_H = J_M_top + dB_zero + R_eq`.

If the parent action defines `J_M_top` as the Poincare dual of the same compact Hilbert source worldtube seen by `Pi_M J_H`, then the equality is mathematically natural. If additionally `R_eq=0` and the compact boundary flux of `dB_zero` vanishes, the topological route can carry the measured source charge rather than a closed wrong charge.

But the current corpus still does not parent-sign those clauses. The missing pieces are:

- `R_eq=0` or a source-backed finite value.
- `B_zero_flux=0` or a source-backed finite value.
- A parent-owned `W_source`, Hilbert measure, observed time generator, and linking-surface class.
- No hidden non-EH, memory, domain, frame, range, symplectic-boundary, or projector source channel.
- A single absolute calibration linking the Hilbert charge to the Newton coefficient.

The useful bound is:

`abs(epsilon_M) <= abs(epsilon_worldtube)+abs(I_commutator)+abs(R_eq_integral)+abs(B_zero_flux)+abs(epsilon_extra)+abs(epsilon_calibration)`.

And the Newton link remains:

`Delta_Newton_v = (1+delta_KC)(1+epsilon_M)-1`.

So the night-shift verdict is sharp: topology is a serious route, not a throwaway, but it has to become the **same Hilbert source object**. Otherwise it remains finite closure machinery.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Topological-Hilbert Equality Audit

{md_table(rows_by_name["equality_audit"], ["audit_id", "gate", "statement", "status", "implication", "valid_for_claim"])}

## B_zero Zero-Flux Conditions

{md_table(rows_by_name["bzero_conditions"], ["condition_id", "condition", "statement", "status", "implication", "valid_for_claim"])}

## Epsilon_M Bound Map

{md_table(rows_by_name["epsilon_map"], ["map_id", "symbol", "definition", "status", "implication", "valid_for_claim"])}

## Finite Rows

{md_table(rows_by_name["finite_rows"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"])}

## Claim Gate

{md_table(rows_by_name["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is not circular work. It is the exact place where the leap either becomes a theorem or stays a closure. The route is less grim than it looked because the mathematical condition is clean: same compact Hilbert source class plus zero equality/boundary residuals. The grim bit is also clean: current MTS has not yet signed the parent selector that makes the closed topological charge the measured mass.

Next we either prove that parent selector, or we stop treating the topological route as derived Newton evidence and fill the residual rows honestly.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "equality_audit": equality_audit_rows(),
        "bzero_conditions": bzero_condition_rows(),
        "epsilon_map": epsilon_map_rows(),
        "finite_rows": finite_row_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in [
        "source_register",
        "equality_audit",
        "bzero_conditions",
        "epsilon_map",
        "finite_rows",
        "claim_gate",
        "decision",
        "next_target",
    ]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
