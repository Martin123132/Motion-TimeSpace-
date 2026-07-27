from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2181"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2181-Y5-R2FR-PiM-commutator-worldtube-source-glue-zero-or-epsilonM-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2181_SOURCE_REGISTER.csv",
    "commutator_audit": OUT / "P8_Y5_PARENT_QLOC_2181_PIM_COMMUTATOR_ZERO_AUDIT.csv",
    "worldtube_audit": OUT / "P8_Y5_PARENT_QLOC_2181_WORLDTUBE_SOURCE_GLUE_AUDIT.csv",
    "epsilon_decomp": OUT / "P8_Y5_PARENT_QLOC_2181_EPSILON_M_DECOMPOSITION.csv",
    "finite_rows": OUT / "P8_Y5_PARENT_QLOC_2181_EPSILON_M_FINITE_ROWS.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2181_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2181_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2181_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2181_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2181_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2181_EPSILON_M_FINITE_ROWS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2181_PIM_COMMUTATOR_AUDIT_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "PIM_COMMUTATOR_WORLDTUBE_GLUE_2181_NONCLAIM.csv",
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
    body = []
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


def formalization_has_2181_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2181-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2181*",
        "*P8_Y5_BRR545_2181*",
        "*Y5_R2FR_PiM_commutator_worldtube_source_glue_zero_or_epsilonM_fill_2181*",
        "*JR2181*",
        "*PIM_COMMUTATOR_WORLDTUBE_GLUE_2181*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2180_handoff",
            ROOT / "2180-Y5-R2FR-PiM-JH-mass-current-to-v-source-coefficient-glue-or-delta-kappa-fill.md",
            ["NEXT2180_0_2181", "PIM_COMMUTATOR_AND_WORLDTUBE_GLUE_NEXT"],
            "2180 selects Pi_M commutator and worldtube glue as the next source-normalization gate.",
        ),
        (
            "2180_validation",
            OUT / "P8_Y5_BRR545_2180_VALIDATION.csv",
            ["VAL2180_OVERALL", "PASS"],
            "2180 validation passed before 2181 continues the chain.",
        ),
        (
            "1013_flux_obstruction",
            ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
            ["d(Pi_M J_H)=0 compact-exterior flux closure", "[d,Pi_M]J_H"],
            "1013 supplies the exact flux obstruction and retained commutator row.",
        ),
        (
            "1014_commutator",
            ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
            ["[d,Pi_M]J_H=0", "fail_current_claim"],
            "1014 shows the commutator/topological route is conditional, not derived.",
        ),
        (
            "topological_hilbert",
            OUT / "P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
            ["EH501_0_equality_statement", "R_eq is not parent-derived zero"],
            "topological-Hilbert equality is the clean route but R_eq remains open.",
        ),
        (
            "source_measure_flux",
            OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
            ["T509_0_charge_identity_needed", "closure_not_derived_for_current_MTS"],
            "source-measure/M_eff flux theorem records the source equality and closure debt.",
        ),
        (
            "charge_current_direct",
            OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
            ["CC7_closed_flux_and_Gauss_calibration", "CC8_second_order_limit"],
            "direct charge-current attempt separates first-order calibration from second-order PPN stability.",
        ),
        (
            "1886_source_slot",
            ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
            ["NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED", "REFUSED_G_ABSORPTION_WITHOUT_COMMON_MODE_GUARD"],
            "1886 forbids measured-G absorption and hidden source-only slots as derivations.",
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


def commutator_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "PCA2181_0_product_rule",
            "projected-current product rule",
            "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H.",
            "EXACT_PRODUCT_RULE",
            "commutator is a real obstruction term, not notation.",
        ),
        (
            "PCA2181_1_fixed_topological_route",
            "fixed topological Pi_M route",
            "If Pi_M is a fixed metric-independent charge map and Pi_M J_H equals a closed topological current up to zero-flux exact terms, then [d,Pi_M]J_H=0.",
            "EXACT_CONDITIONAL_COMMUTATOR_ZERO",
            "this is the clean route but needs Hilbert equality and zero boundary flux.",
        ),
        (
            "PCA2181_2_wrong_object_blocker",
            "closed wrong object",
            "A closed J_M_top does not prove measured source closure unless Pi_M J_H=J_M_top+dB_zero and the boundary flux vanishes.",
            "CONSERVATION_NOT_ENOUGH",
            "1014/501 blocker carried forward.",
        ),
        (
            "PCA2181_3_Hodge_route",
            "Hodge/domain projector route",
            "If Pi_M depends on metric, domain, normal, Green operator or readout, delta Pi_M and [d,Pi_M]J_H become stress/source residuals.",
            "PROJECTOR_STRESS_RETAINED_IF_USED",
            "Hodge route is allowed only with finite bounds or a parent zero theorem.",
        ),
        (
            "PCA2181_4_post_readout_mask",
            "post-readout projector mask",
            "Choosing Pi_M after orbital/readout calibration is forbidden as derivation.",
            "FORBIDDEN_AS_DERIVATION",
            "may be closure-only, not local-GR evidence.",
        ),
        (
            "PCA2181_5_current_status",
            "commutator zero status",
            "Current corpus does not parent-sign fixed Pi_M, Hilbert equality, zero boundary flux, zero extra projection and zero projector stress together.",
            "COMMUTATOR_ZERO_NOT_DERIVED",
            "I_commutator remains a finite-or-zero residual.",
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


def worldtube_audit_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "WTG2181_0_source_identity",
            "worldtube source identity",
            "M_source[W]=integral_S Pi_M J_H=M_eff must hold before orbital fitting and before measured-G calibration.",
            "EXACT_TARGET_IDENTITY",
            "this is the source side of epsilon_M=0.",
        ),
        (
            "WTG2181_1_domain_selector",
            "worldtube/domain selector",
            "The compact source worldtube and S2 class must be parent-selected without preferred-frame/readout leakage.",
            "MISSING_PARENT_DOMAIN_SELECTOR",
            "otherwise the source can be chosen to fit the orbit.",
        ),
        (
            "WTG2181_2_Hilbert_source",
            "same Hilbert source",
            "The Hilbert mass current J_H must be the same ordinary-matter source used by the v equation, clocks and orbital readout.",
            "MISSING_SAME_SOURCE_CERTIFICATE",
            "same-frame language alone is not a parent source theorem.",
        ),
        (
            "WTG2181_3_zero_extra_channels",
            "no extra mass channels",
            "Boundary, non-EH, memory, range, species, domain and projector channels must not add mu_extra to M_eff.",
            "MISSING_MU_EXTRA_ZERO_OR_BOUNDS",
            "1012 eight-channel source-normalization vector remains active.",
        ),
        (
            "WTG2181_4_calibration",
            "absolute calibration",
            "The surface charge normalization must match the v-source mass without a floating constant except a parent-fixed derivative-silent calibration.",
            "MISSING_ABSOLUTE_CALIBRATION_OWNER",
            "constant offset cannot hide beta/Gdot/radial hair unless parent-fixed.",
        ),
        (
            "WTG2181_5_current_status",
            "worldtube glue status",
            "Current corpus does not parent-sign domain selector, Hilbert equality, extra-channel silence and absolute calibration together.",
            "WORLDTUBE_GLUE_NOT_DERIVED",
            "epsilon_M remains nonclaim.",
        ),
    ]
    return [
        base_row(
            glue_id=glue_id,
            gate=gate,
            statement=statement,
            status=status,
            implication=implication,
        )
        for glue_id, gate, statement, status, implication in specs
    ]


def epsilon_decomp_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EMD2181_0_definition",
            "epsilon_M definition",
            "epsilon_M=M_source[v]/M_eff[Pi_M J_H]-1.",
            "EXACT_FROM_2180",
            "this is the mass-current/source-measure residual feeding Delta_Newton_v.",
        ),
        (
            "EMD2181_1_flux_identity",
            "flux obstruction identity",
            "Delta_flux/M_eff = M_eff^-1 integral_A(-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent).",
            "EXACT_FLUX_OBSTRUCTION_SHAPE",
            "maps 1013 obstruction rows into epsilon_M.",
        ),
        (
            "EMD2181_2_topological_equality",
            "topological-Hilbert equality residual",
            "R_eq_integral/M_eff measures Pi_M J_H - J_M_top - dB_zero over the linked source boundary.",
            "EXACT_EQUALITY_RESIDUAL",
            "closed topological current is useful only if R_eq and B_zero flux vanish.",
        ),
        (
            "EMD2181_3_worldtube_piece",
            "worldtube source mismatch",
            "epsilon_W := M_source[W]/M_top_or_Hilbert[W]-1.",
            "EXACT_DEFINITION",
            "domain/source selector mismatch becomes a direct source-normalization residual.",
        ),
        (
            "EMD2181_4_total_envelope",
            "no-cancellation epsilon_M envelope",
            "abs(epsilon_M) <= abs(epsilon_W)+abs(I_commutator)+abs(epsilon_extra)+abs(A_parent)+abs(R_eq)+abs(B_zero_flux)+abs(epsilon_calibration), after common normalization.",
            "EXACT_ABSOLUTE_LEDGER",
            "no cancellation credit is allowed until a parent identity is derived.",
        ),
        (
            "EMD2181_5_newton_link",
            "Newton residual link",
            "Delta_Newton_v=(1+delta_KC)(1+epsilon_M)-1.",
            "EXACT_FROM_2180",
            "epsilon_M remains a live Newton amplitude residual.",
        ),
        (
            "EMD2181_6_current_status",
            "epsilon_M zero status",
            "No component of the epsilon_M envelope is parent-zero or source-backed numeric in the current 2181 branch.",
            "EPSILON_M_ZERO_NOT_DERIVED",
            "finite rows stay mandatory.",
        ),
    ]
    return [
        base_row(
            decomp_id=decomp_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for decomp_id, object_name, statement, status, implication in specs
    ]


def finite_row_rows() -> list[dict[str, Any]]:
    specs = [
        ("EFR2181_0_epsilon_M", "epsilon_M", "M_source[v]/M_eff[Pi_M J_H]-1", "MISSING_EPSILON_M_ZERO_OR_NUMERIC_VALUE", "dimensionless", "Newton;PPN;R11"),
        ("EFR2181_1_I_commutator", "I_commutator", "normalized finite-annulus integral of [d,Pi_M]J_H", "MISSING_COMMUTATOR_ZERO_OR_VALUE", "dimensionless_or_GM_flux_units", "Newton;R4_beta;R9_Gdot;R10;R11"),
        ("EFR2181_2_R_eq", "R_eq_integral", "normalized integral of Pi_M J_H - J_M_top - dB_zero", "MISSING_R_EQ_ZERO_OR_VALUE", "dimensionless_after_Meff_normalization", "Newton;PPN;R11"),
        ("EFR2181_3_B_zero", "B_zero_flux", "boundary/improvement exact flux through compact linked boundary", "MISSING_B_ZERO_FLUX_ZERO_OR_VALUE", "GM_flux_or_dimensionless", "R4_beta;R7_alpha3;R8_xi;R9_Gdot"),
        ("EFR2181_4_extra", "epsilon_extra_current", "normalized -Pi_M dJ_extra + A_parent extra-current/anomaly source piece", "MISSING_EXTRA_CURRENT_ZERO_OR_VALUE", "dimensionless_or_GM_flux_units", "Newton;PPN;R11"),
        ("EFR2181_5_worldtube", "epsilon_worldtube", "worldtube source/domain selector mismatch in source mass", "MISSING_WORLDTUBE_GLUE_ZERO_OR_VALUE", "dimensionless", "Newton;WEP;clock;orbital"),
        ("EFR2181_6_calibration", "epsilon_calibration", "absolute calibration offset between surface charge and v-source mass", "MISSING_PARENT_FIXED_CALIBRATION_OR_VALUE", "dimensionless", "R4_beta;R9_Gdot;Newton"),
        ("EFR2181_7_projector_stress", "projector_stress_beta_equiv", "weak-field/PPN stress equivalent from delta Pi_M", "MISSING_PROJECTOR_STRESS_MAP_OR_VALUE", "PPN_or_operator_units", "PPN_beta;R11;local_GR"),
        ("EFR2181_8_total", "epsilon_M_abs", "absolute no-cancellation envelope for epsilon_M components", "MISSING_COMPONENT_VALUES", "declared_common_norm", "all_local_arenas"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            status=status,
            units=units,
            observable_link=observable_link,
            value="MISSING_NUMERIC_VALUE",
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
            no_cancellation_policy=True,
        )
        for row_id, symbol, definition, status, units, observable_link in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2181_0_commutator", "[d,Pi_M]J_H=0 theorem or bound", "UNSIGNED", "I_commutator remains live"),
        ("CG2181_1_worldtube", "worldtube source equality", "UNSIGNED", "source measure can still be the wrong object"),
        ("CG2181_2_topological_Hilbert", "Pi_M J_H=J_M_top+dB_zero with zero flux", "UNSIGNED", "closed topological current not enough"),
        ("CG2181_3_epsilon_M", "epsilon_M=0 or finite score-ready row", "UNSIGNED", "Newton source glue remains blocked"),
        ("CG2181_4_no_absorption", "post-readout masks and measured-G absorption rejected", "PASS_GUARDRAIL", "no-cheat guard retained"),
        ("CG2181_5_conditional_route", "fixed topological Hilbert route would close commutator", "CONDITIONAL_PASS", "useful target but not parent-signed"),
        ("CG2181_6_verdict", "Newton/local-GR claim", "BLOCKED_NONCLAIM", "2181 writes epsilon_M decomposition; no claim"),
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
            "DEC2181_0_gain_commutator",
            "COMMUTATOR_ZERO_ROUTE_SPLIT",
            "fixed topological Pi_M can kill [d,Pi_M]J_H only if Hilbert equality and zero-flux exact terms are also parent-signed.",
            "selected",
        ),
        (
            "DEC2181_1_gain_epsilon",
            "EPSILON_M_ABSOLUTE_LEDGER_WRITTEN",
            "epsilon_M is decomposed into worldtube, commutator, extra-current, anomaly, equality, boundary and calibration pieces.",
            "selected",
        ),
        (
            "DEC2181_2_no_claim",
            "CLOSED_WRONG_OBJECT_BLOCKER_RETAINED",
            "a conserved topological current is not Newton evidence unless it equals the Hilbert/source current used by v and orbits.",
            "selected",
        ),
        (
            "DEC2181_3_finite",
            "EPSILON_M_ROWS_ARE_LIVE",
            "I_commutator, R_eq, B_zero_flux, epsilon_worldtube and calibration rows remain missing theorem-zero or numeric values.",
            "selected",
        ),
        (
            "DEC2181_4_next",
            "TOPOLOGICAL_HILBERT_EQUALITY_OR_REQ_BOUND_NEXT",
            "the next derivation should attack Pi_M J_H=J_M_top+dB_zero and R_eq=0, or fill R_eq/I_commutator rows.",
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
            route_id="NEXT2181_0_2182",
            selection_status="selected",
            target_file="2182-Y5-R2FR-topological-Hilbert-equality-R_eq-zero-or-epsilonM-bound-fill.md",
            target_script="scripts/Y5_R2FR_topological_Hilbert_equality_R_eq_zero_or_epsilonM_bound_fill_2182.py",
            objective="derive Pi_M J_H=J_M_top+dB_zero with zero compact boundary flux for the constrained v source, or fill R_eq/I_commutator/epsilon_M finite rows",
            success_condition="R_eq=0, B_zero_flux=0, fixed source worldtube and parent Hilbert charge equality are signed; otherwise source-backed nonclaim rows are emitted",
            do_not_do="do not count a closed wrong topological charge as measured mass, do not impose equality with a late multiplier, do not use reference-only zero",
        ),
        base_row(
            route_id="NEXT2181_1_numeric_parallel",
            selection_status="held_parallel",
            target_file="2182b-Y5-R2FR-epsilonM-Icommutator-source-backed-bound-acquisition.md",
            target_script="scripts/Y5_R2FR_epsilonM_Icommutator_source_backed_bound_acquisition_2182b.py",
            objective="acquire source-backed finite rows for epsilon_M, I_commutator, R_eq or B_zero_flux if derivation fails",
            success_condition="at least one row has numeric value, units, source path, arena projection and remains nonclaim until full envelope closes",
            do_not_do="do not score placeholders, cancellation-only rows or source-free assertions",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["finite_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["commutator_audit"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["epsilon_decomp"], BRANCH_COPIES["source_weight"]),
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
    validations.append(base_row(validation_id="VAL2181_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2181_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    comm_statuses = {row["status"] for row in rows_by_name["commutator_audit"]}
    comm_pass = "EXACT_PRODUCT_RULE" in comm_statuses and "EXACT_CONDITIONAL_COMMUTATOR_ZERO" in comm_statuses and "COMMUTATOR_ZERO_NOT_DERIVED" in comm_statuses
    validations.append(base_row(validation_id="VAL2181_02_commutator_audit", status="PASS" if comm_pass else "FAIL", detail="commutator zero route is exact conditional and not claimed"))

    world_statuses = {row["status"] for row in rows_by_name["worldtube_audit"]}
    world_pass = "EXACT_TARGET_IDENTITY" in world_statuses and "WORLDTUBE_GLUE_NOT_DERIVED" in world_statuses
    validations.append(base_row(validation_id="VAL2181_03_worldtube_audit", status="PASS" if world_pass else "FAIL", detail="worldtube source identity written and remains unsigned"))

    eps_statuses = {row["status"] for row in rows_by_name["epsilon_decomp"]}
    eps_pass = "EXACT_ABSOLUTE_LEDGER" in eps_statuses and "EPSILON_M_ZERO_NOT_DERIVED" in eps_statuses
    validations.append(base_row(validation_id="VAL2181_04_epsilon_decomposition", status="PASS" if eps_pass else "FAIL", detail="epsilon_M no-cancellation ledger written and kept nonclaim"))

    finite_rows = rows_by_name["finite_rows"]
    finite_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in finite_rows)
    validations.append(base_row(validation_id="VAL2181_05_finite_rows", status="PASS" if finite_ok else "FAIL", detail=f"epsilon_M finite rows={len(finite_rows)} remain score_ready=false"))

    claim_statuses = {row["status"] for row in rows_by_name["claim_gate"]}
    validations.append(base_row(validation_id="VAL2181_06_claim_gate", status="PASS" if "BLOCKED_NONCLAIM" in claim_statuses and "PASS_GUARDRAIL" in claim_statuses else "FAIL", detail="Newton/local-GR claim blocked and no-cheat guard retained"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2181_07_decision", status="PASS" if "TOPOLOGICAL_HILBERT_EQUALITY_OR_REQ_BOUND_NEXT" in decision_text else "FAIL", detail="decision selects topological-Hilbert equality/R_eq next"))

    validations.append(base_row(validation_id="VAL2181_08_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2182" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2182 topological-Hilbert equality target selected"))

    validations.append(base_row(validation_id="VAL2181_09_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2181_10_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2181_11_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2181_artifacts()
    validations.append(base_row(validation_id="VAL2181_12_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2181 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2181_13_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2181_OVERALL", status="PASS" if overall else "FAIL", detail="2181 writes Pi_M commutator/worldtube epsilon_M decomposition and keeps Newton/local-GR blocked"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2181 - Y5/R2FR PiM Commutator Worldtube Source Glue Zero Or EpsilonM Fill

## Current Verdict

2181 does **not** close `epsilon_M`. It does the sharper thing: it proves exactly what would have to close.

The projected-current product rule is:

`d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H`.

So `[d,Pi_M]J_H=0` is not automatic. A fixed topological projector can kill the commutator only if the topological charge is also the observed Hilbert/source charge:

`Pi_M J_H = J_M_top + dB_zero`,

with zero compact boundary flux. Otherwise we have a conserved wrong object.

The source glue target is:

`M_source[W]=integral_S Pi_M J_H=M_eff`,

before orbital fitting and before measured-G calibration.

The useful output is the no-cancellation ledger:

`abs(epsilon_M) <= abs(epsilon_W)+abs(I_commutator)+abs(epsilon_extra)+abs(A_parent)+abs(R_eq)+abs(B_zero_flux)+abs(epsilon_calibration)`.

And it still feeds:

`Delta_Newton_v=(1+delta_KC)(1+epsilon_M)-1`.

So the next target is surgical: prove topological-Hilbert equality and zero boundary flux, or fill `R_eq/I_commutator/epsilon_M` as finite source-normalization rows.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Pi_M Commutator Zero Audit

{md_table(rows_by_name["commutator_audit"], ["audit_id", "gate", "statement", "status", "implication", "valid_for_claim"])}

## Worldtube Source Glue Audit

{md_table(rows_by_name["worldtube_audit"], ["glue_id", "gate", "statement", "status", "implication", "valid_for_claim"])}

## Epsilon_M Decomposition

{md_table(rows_by_name["epsilon_decomp"], ["decomp_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Epsilon_M Finite Rows

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

This keeps us moving forward rather than circling. The commutator route is not dead, but it cannot be claimed from projector algebra. It needs topological-Hilbert equality, zero boundary flux, a parent-owned worldtube, and no extra mass channels.

If those close, `epsilon_M` can plausibly go to zero. If they do not, `epsilon_M` is not shameful; it becomes the finite source-normalization residual the theory must test.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "commutator_audit": commutator_audit_rows(),
        "worldtube_audit": worldtube_audit_rows(),
        "epsilon_decomp": epsilon_decomp_rows(),
        "finite_rows": finite_row_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "commutator_audit", "worldtube_audit", "epsilon_decomp", "finite_rows", "claim_gate", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
