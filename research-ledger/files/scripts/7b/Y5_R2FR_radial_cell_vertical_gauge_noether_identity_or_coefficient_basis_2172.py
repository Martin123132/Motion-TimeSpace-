from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2172"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2172-Y5-R2FR-radial-cell-vertical-gauge-noether-identity-or-coefficient-basis.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2172_SOURCE_REGISTER.csv",
    "generator_algebra": OUT / "P8_Y5_PARENT_QLOC_2172_GENERATOR_ALGEBRA.csv",
    "noether_attempt": OUT / "P8_Y5_PARENT_QLOC_2172_NOETHER_IDENTITY_ATTEMPT.csv",
    "leak_bound": OUT / "P8_Y5_PARENT_QLOC_2172_COFRAME_LEAK_BOUND.csv",
    "coefficient_basis": OUT / "P8_Y5_PARENT_QLOC_2172_COEFFICIENT_BASIS_NONCLAIM.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2172_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2172_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2172_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2172_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2172_COEFFICIENT_BASIS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2172_COFRAME_LEAK_BOUND_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "VERTICAL_GENERATOR_OBSTRUCTION_2172_NONCLAIM.csv",
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


def formalization_has_2172_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2172-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2172*",
        "*P8_Y5_BRR545_2172*",
        "*Y5_R2FR_radial_cell_vertical_gauge_noether_identity_or_coefficient_basis_2172*",
        "*JR2172*",
        "*VERTICAL_GENERATOR_OBSTRUCTION_2172*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2171_handoff",
            ROOT / "2171-Y5-R2FR-compatibility-object-category-principle-or-finite-local-source-row.md",
            ["NEXT2171_0_2172", "VG2171_0_generator"],
            "2171 selects actual vertical generator/Noether identity construction.",
        ),
        (
            "2171_validation",
            OUT / "P8_Y5_BRR545_2171_VALIDATION.csv",
            ["VAL2171_OVERALL,PASS"],
            "2171 validation passed.",
        ),
        (
            "1878_dobs_kernel",
            ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
            ["C_R = R_AB = 2(ln T + ln sqrt(S))", "DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS"],
            "1878 supplies the observed-coframe visibility obstruction.",
        ),
        (
            "1879_common_frame",
            ROOT / "1879-Y5-R2FR-parent-coframe-ownership-or-common-frame-leak-bound.md",
            ["e_obs = E(Q_vis)", "PARENT_COFRAME_OWNERSHIP_NOT_DERIVED_CURRENT_CORPUS"],
            "1879 supplies the coframe-ownership route and leak rows.",
        ),
        (
            "2168_category_route",
            ROOT / "2168-Y5-R2FR-object-language-radial-cell-constraint-or-finite-ZRJR-intake.md",
            ["C_R=R_AB=2u", "MISSING_PARENT_CATEGORY_PRINCIPLE"],
            "2168 states the category route and missing parent principle.",
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


def generator_algebra_rows() -> list[dict[str, Any]]:
    equal_weight_min = 1.0 / (2.0 * math.sqrt(2.0))
    specs = [
        (
            "GA2172_0_variables",
            "define logarithmic coframe variations",
            "x=delta ln T, y=delta ln sqrt(S), so delta C_R=2(x+y)",
            "EXACT_ALGEBRA",
            "sets the generator problem in the current observed coframe",
        ),
        (
            "GA2172_1_readout_kernel",
            "current observed coframe kernel",
            "delta e_obs=0 requires x=0 and y=0 for theta_0=T cdt and theta_1=sqrt(S) dr",
            "EXACT_KERNEL_CONDITION",
            "then delta C_R=0, so no nontrivial generator can both change C_R and leave current coframe fixed",
        ),
        (
            "GA2172_2_no_nontrivial_vertical",
            "vertical generator existence test",
            "delta C_R=epsilon != 0 and delta e_obs=0 are inconsistent under current observed coframe",
            "NO_NONTRIVIAL_VERTICAL_GENERATOR_CURRENT_READOUT",
            "vertical-gauge proof cannot close without a new readout functor or constraint-first route",
        ),
        (
            "GA2172_3_min_equal_weight_leak",
            "minimum equal-weight coframe leak",
            f"min sqrt(x^2+y^2) subject to 2(x+y)=epsilon is |epsilon|/(2 sqrt(2)) = {equal_weight_min:.12g} |epsilon|",
            "EXACT_LOWER_BOUND_EQUAL_WEIGHT_NORM",
            "any nonzero C_R generator has nonzero clock/ruler response in the current two-leg log norm",
        ),
        (
            "GA2172_4_weighted_leak",
            "minimum weighted coframe leak",
            "for norm sqrt(w_T x^2+w_S y^2), min leak is |epsilon|/(2 sqrt(1/w_T+1/w_S)) for positive weights",
            "EXACT_LOWER_BOUND_WEIGHTED_NORM",
            "the obstruction survives any positive local weighting of the two visible legs",
        ),
        (
            "GA2172_5_escape_conditions",
            "allowed escape routes",
            "only a parent-owned Q_vis/E readout rebuild, or a parent auxiliary constraint imposing C_R=0 before readout, can avoid the obstruction",
            "ESCAPE_ROUTES_IDENTIFIED_NONCLAIM",
            "next target should not pretend current readout has a hidden vertical kernel",
        ),
    ]
    return [
        base_row(
            algebra_id=algebra_id,
            object=object_name,
            statement=statement,
            status=status,
            implication=implication,
        )
        for algebra_id, object_name, statement, status, implication in specs
    ]


def noether_attempt_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NI2172_0_generator",
            "construct v_R with delta C_R=epsilon",
            "possible algebraically by choosing x+y=epsilon/2",
            "ALGEBRAIC_FAMILY_EXISTS",
            "not enough for gauge because observed coframe moves",
        ),
        (
            "NI2172_1_verticality",
            "require v_R in kernel of current observed readout",
            "x=0 and y=0",
            "FAILS_FOR_EPSILON_NONZERO",
            "the current readout has no nontrivial C_R vertical generator",
        ),
        (
            "NI2172_2_noether_identity",
            "derive a Noether identity from v_R",
            "would require action invariance under a generator that is also readout-vertical",
            "BLOCKED_BY_READOUT_VERTICALITY",
            "there is no current generator to feed the identity",
        ),
        (
            "NI2172_3_action_invariance",
            "test delta_v S_parent=0",
            "not reached as a claim; derivative/potential/source countermodels remain legal",
            "MISSING_PARENT_ACTION_SYMMETRY",
            "even a new generator would still need action invariance and boundary silence",
        ),
        (
            "NI2172_4_result",
            "vertical-gauge proof status",
            "current MTS readout cannot support a nontrivial C_R-shift gauge generator",
            "VERTICAL_GAUGE_ROUTE_REJECTED_FOR_CURRENT_READOUT",
            "move to auxiliary constraint origin or readout-functor rebuild",
        ),
    ]
    return [
        base_row(
            attempt_id=attempt_id,
            target=target,
            test=test,
            status=status,
            implication=implication,
        )
        for attempt_id, target, test, status, implication in specs
    ]


def leak_bound_rows() -> list[dict[str, Any]]:
    equal_weight_min = 1.0 / (2.0 * math.sqrt(2.0))
    return [
        base_row(
            bound_id="CLB2172_0_equal_weight",
            leak_symbol="epsilon_R_cell_min",
            definition="minimum equal-weight log-coframe response for a C_R generator",
            formula="epsilon_R_cell_min >= |delta C_R|/(2 sqrt(2))",
            coefficient=f"{equal_weight_min:.12g}",
            units="dimensionless_log_coframe_per_dimensionless_delta_C_R",
            status="EXACT_ALGEBRAIC_LOWER_BOUND_NONCLAIM",
            observable_link="PPN;clock;orbital;local_GR",
            source_path=str(DOC),
            score_ready=False,
        ),
        base_row(
            bound_id="CLB2172_1_weighted",
            leak_symbol="epsilon_R_cell_weighted_min",
            definition="minimum weighted log-coframe response for positive leg weights",
            formula="epsilon_R_cell_weighted_min >= |delta C_R|/(2 sqrt(1/w_T+1/w_S))",
            coefficient="symbolic_positive_weights",
            units="dimensionless_log_coframe_per_dimensionless_delta_C_R",
            status="EXACT_ALGEBRAIC_LOWER_BOUND_NONCLAIM",
            observable_link="PPN;clock;orbital;local_GR",
            source_path=str(DOC),
            score_ready=False,
        ),
        base_row(
            bound_id="CLB2172_2_zero_kernel",
            leak_symbol="epsilon_R_cell_zero",
            definition="zero coframe response under current observed coframe",
            formula="epsilon_R_cell=0 => delta C_R=0",
            coefficient="zero_generator_only",
            units="dimensionless",
            status="NO_NONTRIVIAL_ZERO_LEAK_GENERATOR_CURRENT_READOUT",
            observable_link="local_GR",
            source_path=str(DOC),
            score_ready=False,
        ),
    ]


def coefficient_basis_rows() -> list[dict[str, Any]]:
    specs = [
        ("CB2172_0_readout_leak", "epsilon_R_cell", "observed coframe leak tied to C_R generator", "bounded below by generator algebra unless readout is rebuilt", "PPN;clock;orbital;local_GR"),
        ("CB2172_1_ZR", "Z_R", "kinetic reciprocal operator coefficient", "still finite/missing because type-only and vertical-gauge routes fail under current readout", "R10;PPN;clock;orbital"),
        ("CB2172_2_MR2", "M_R^2", "potential/mass-gap reciprocal operator coefficient", "still finite/missing unless auxiliary constraint removes the mode", "R10;clock;orbital"),
        ("CB2172_3_JR", "J_R", "direct matter source coefficient", "still finite/missing without matter descent/no-source-only theorem", "WEP;R10;PPN"),
        ("CB2172_4_QR", "Q_R/q_R_hat", "boundary/exterior reciprocal charge", "still finite/missing without boundary no-charge theorem", "PPN;orbital;light_time"),
        ("CB2172_5_bdw", "b_R,d_R,w_R", "common Weyl/disformal/source-weight readout and source coupling", "still finite/missing without terminal public coframe and source-current owner", "PPN;clock;WEP;orbital"),
        ("CB2172_6_beta", "delta_beta_source", "second-order active-source beta residual", "still finite/missing; gamma channel cannot substitute", "PPN;local_GR"),
        ("CB2172_7_total", "epsilon_local_abs", "no-cancellation local residual envelope", "requires all component rows theorem-zero or source-backed before any arena score", "all_local_arenas"),
    ]
    return [
        base_row(
            basis_id=basis_id,
            symbol=symbol,
            definition=definition,
            status="MISSING_THEOREM_ZERO_OR_SOURCE_BACKED_VALUE",
            reason=reason,
            observable_link=observable_link,
            value="MISSING_NUMERIC_VALUE",
            units="MISSING_UNITS_OR_DECLARED_DIMENSIONLESS",
            source_path="MISSING_SOURCE_PATH",
            score_ready=False,
            no_cancellation_policy=True,
        )
        for basis_id, symbol, definition, reason, observable_link in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2172_0_result", "NO_NONTRIVIAL_VERTICAL_GENERATOR_CURRENT_READOUT", "a C_R-changing generator necessarily moves at least one current observed coframe leg", "selected"),
        ("DEC2172_1_gain", "EXACT_LEAK_BOUND_DERIVED", "the minimum equal-weight coframe leak is |delta C_R|/(2 sqrt(2)); the obstruction is algebraic, not vibes", "selected"),
        ("DEC2172_2_noether", "NOETHER_ROUTE_BLOCKED_BY_VERTICALITY", "without a readout-vertical generator there is no current Noether identity that can make C_R pure gauge", "selected"),
        ("DEC2172_3_next", "AUXILIARY_CONSTRAINT_OR_READOUT_REBUILD_NEXT", "the clean remaining derivation routes are parent-owned Lambda_R C_R with Dirac preservation, or a real Q_vis/E readout rebuild", "selected"),
        ("DEC2172_4_claim_ceiling", "FINITE_BASIS_NONCLAIM", "all finite rows remain nonclaim until zero theorem or source-backed values exist", "selected"),
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
            route_id="NEXT2172_0_2173",
            selection_status="selected",
            target_file="2173-Y5-R2FR-radial-cell-auxiliary-constraint-origin-dirac-or-readout-rebuild.md",
            target_script="scripts/Y5_R2FR_radial_cell_auxiliary_constraint_origin_dirac_or_readout_rebuild_2173.py",
            objective="try the remaining clean derivation route: parent-owned Lambda_R C_R auxiliary constraint with Dirac preservation and matter/boundary/readout silence; if not, specify the readout-functor rebuild or demote to finite coefficients",
            success_condition="C_R=0 is imposed before readout by a parent-origin auxiliary constraint with preserved constraint algebra, or the route is explicitly closure-only and finite rows stay primary",
            do_not_do="do not claim vertical gauge under current coframe, do not insert Lambda_R by hand, do not import GR or use finite rows as predictions",
        ),
        base_row(
            route_id="NEXT2172_1_empirical_parallel",
            selection_status="held_parallel",
            target_file="2173b-Y5-R2FR-local-residual-coefficient-first-real-source-row.md",
            target_script="scripts/Y5_R2FR_local_residual_coefficient_first_real_source_row_2173b.py",
            objective="begin one real source-backed residual coefficient acquisition if the auxiliary route fails",
            success_condition="one finite component has source path, units, convention, projection and remains nonclaim until full envelope exists",
            do_not_do="do not score symbolic placeholders or use external bounds as MTS predictions",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["coefficient_basis"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["leak_bound"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["decision"], BRANCH_COPIES["source_weight"]),
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
    validations.append(base_row(validation_id="VAL2172_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2172_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    algebra_statuses = {row["status"] for row in rows_by_name["generator_algebra"]}
    validations.append(base_row(validation_id="VAL2172_02_generator_obstruction", status="PASS" if "NO_NONTRIVIAL_VERTICAL_GENERATOR_CURRENT_READOUT" in algebra_statuses else "FAIL", detail="current observed coframe has no nontrivial C_R vertical generator"))

    leak_formula = " ".join(str(row.get("formula", "")) for row in rows_by_name["leak_bound"])
    validations.append(base_row(validation_id="VAL2172_03_leak_bound", status="PASS" if "|delta C_R|/(2 sqrt(2))" in leak_formula else "FAIL", detail="equal-weight lower-bound formula recorded"))

    noether_statuses = {row["status"] for row in rows_by_name["noether_attempt"]}
    validations.append(base_row(validation_id="VAL2172_04_noether_rejected_current_readout", status="PASS" if "VERTICAL_GAUGE_ROUTE_REJECTED_FOR_CURRENT_READOUT" in noether_statuses else "FAIL", detail="Noether route is blocked by readout verticality, not claimed"))

    coeff_rows = rows_by_name["coefficient_basis"]
    coeff_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in coeff_rows)
    validations.append(base_row(validation_id="VAL2172_05_coefficients_nonclaim", status="PASS" if coeff_ok else "FAIL", detail=f"coefficient_basis_rows={len(coeff_rows)} remain score_ready=false"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2172_06_decision", status="PASS" if "AUXILIARY_CONSTRAINT_OR_READOUT_REBUILD_NEXT" in decision_text else "FAIL", detail="decision selects auxiliary constraint/readout rebuild next"))

    validations.append(base_row(validation_id="VAL2172_07_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2173" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2173 auxiliary constraint/readout rebuild target selected"))

    validations.append(base_row(validation_id="VAL2172_08_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2172_09_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2172_10_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2172_artifacts()
    validations.append(base_row(validation_id="VAL2172_11_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2172 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2172_12_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2172_OVERALL", status="PASS" if overall else "FAIL", detail="2172 derives the current-readout vertical-generator obstruction and selects auxiliary constraint/readout rebuild next"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2172 - Y5/R2FR Radial-Cell Vertical-Gauge Noether Identity Or Coefficient Basis

## Current Verdict

2172 rejects the clean vertical-gauge route **for the current observed coframe**.

This is a real derivation result, but it is a no-go rather than a pass. Let

`x = delta ln T`, `y = delta ln sqrt(S)`, so `delta C_R = 2(x+y)`.

For the current observed coframe legs `theta_0=T cdt` and `theta_1=sqrt(S) dr`, readout verticality requires `x=0` and `y=0`. Therefore `delta C_R=0`. A nonzero `C_R` generator cannot sit in the kernel of the current observed coframe.

The minimum equal-weight coframe leak for a nonzero generator is

`min sqrt(x^2+y^2) = |delta C_R|/(2 sqrt(2))`.

So the category principle cannot be closed by hidden vertical gauge under the current readout. The remaining clean derivation route is a parent-owned auxiliary constraint `Lambda_R C_R` imposed before readout, or a genuine readout-functor rebuild.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Generator Algebra

{md_table(rows_by_name["generator_algebra"], ["algebra_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## Noether Identity Attempt

{md_table(rows_by_name["noether_attempt"], ["attempt_id", "target", "test", "status", "implication", "valid_for_claim"])}

## Coframe Leak Bound

{md_table(rows_by_name["leak_bound"], ["bound_id", "leak_symbol", "definition", "formula", "coefficient", "units", "status", "score_ready", "valid_for_claim"])}

## Coefficient Basis Nonclaim

{md_table(rows_by_name["coefficient_basis"], ["basis_id", "symbol", "definition", "status", "reason", "observable_link", "score_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is the most useful kind of bad news: it removes a tempting but slippery route. If clocks and rulers use the current `T, sqrt(S)` coframe, then a nonzero `C_R` shift is physically visible. So `C_R` cannot simply be declared gauge.

That narrows the honest local-GR derivation. We now need either a parent-origin auxiliary constraint that kills `C_R` before readout, or a parent-owned readout rebuild proving the observed coframe never depended on that cell in the first place. If neither closes, the finite coefficient basis is the live empirical branch.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "generator_algebra": generator_algebra_rows(),
        "noether_attempt": noether_attempt_rows(),
        "leak_bound": leak_bound_rows(),
        "coefficient_basis": coefficient_basis_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "generator_algebra", "noether_attempt", "leak_bound", "coefficient_basis", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
