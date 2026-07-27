from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2176"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2176-Y5-R2FR-parent-Ru-involution-current-owner-or-finite-Iu-Ju-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2176_SOURCE_REGISTER.csv",
    "ru_algebra": OUT / "P8_Y5_PARENT_QLOC_2176_RU_INVOLUTION_ALGEBRA.csv",
    "owner_gates": OUT / "P8_Y5_PARENT_QLOC_2176_RU_OWNER_GATE_LEDGER.csv",
    "finite_rows": OUT / "P8_Y5_PARENT_QLOC_2176_IU_JU_FINITE_ROW_BACKSTOP.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2176_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2176_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2176_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2176_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2176_IU_JU_FINITE_ROW_BACKSTOP_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2176_RU_INVOLUTION_ALGEBRA_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "RU_INVOLUTION_OWNER_GATE_2176_NONCLAIM.csv",
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


def formalization_has_2176_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2176-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2176*",
        "*P8_Y5_BRR545_2176*",
        "*Y5_R2FR_parent_Ru_involution_current_owner_or_finite_Iu_Ju_row_2176*",
        "*JR2176*",
        "*RU_INVOLUTION_OWNER_GATE_2176*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2175_handoff",
            ROOT / "2175-Y5-R2FR-parent-even-u-sector-no-source-theorem-or-Iu-Ju-residuals.md",
            ["NEXT2175_0_2176", "PARENT_RU_INVOLUTION_OR_FINITE_IU_JU_ROW_NEXT"],
            "2175 selects parent R_u involution/current owner or finite I_u/J_u row.",
        ),
        (
            "2175_validation",
            OUT / "P8_Y5_BRR545_2175_VALIDATION.csv",
            ["VAL2175_OVERALL,PASS"],
            "2175 validation passed.",
        ),
        (
            "observer_contract",
            ROOT / "10-observer-map-symplectic-contract.md",
            ["J_q = T sqrt(S)", "R_AB = ln(T^2 S)"],
            "observer contract defines radial-cell Jacobian and reciprocal strain.",
        ),
        (
            "1877_qshape",
            ROOT / "1877-Y5-R2FR-qshape-or-lambdaR-parent-origin-source-hunt.md",
            ["QSHAPE_IS_NOT_INDEPENDENT_ESCAPE", "J_q=T sqrt(S)"],
            "1877 blocks cheap q_shape deletion and records the J_q identity.",
        ),
        (
            "1878_readout",
            ROOT / "1878-Y5-R2FR-qshape-readout-functor-kernel-or-parent-category-principle.md",
            ["DOBS_E_KERNEL_NOT_DERIVED_CURRENT_CORPUS", "theta_0=T cdt"],
            "1878 says current coframe readout sees radial-cell variation.",
        ),
        (
            "2172_vertical_obstruction",
            ROOT / "2172-Y5-R2FR-radial-cell-vertical-gauge-noether-identity-or-coefficient-basis.md",
            ["NO_NONTRIVIAL_VERTICAL_GENERATOR_CURRENT_READOUT", "AUXILIARY_CONSTRAINT_OR_READOUT_REBUILD_NEXT"],
            "2172 derives the current-readout vertical-generator obstruction.",
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


def ru_algebra_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RUA2176_0_log_variables",
            "log variables",
            "a=ln T, b=ln sqrt(S), u=a+b, v=a-b.",
            "EXACT_DEFINITION",
            "u is reciprocal-cell volume; v is the ratio/potential-like variable.",
        ),
        (
            "RUA2176_1_candidate",
            "candidate involution",
            "R_u sends u to -u and leaves v fixed.",
            "ALGEBRAIC_CANDIDATE",
            "this is the unique simple flip of the reciprocal cell while preserving the ratio variable.",
        ),
        (
            "RUA2176_2_original_variables",
            "T and sqrt(S) map",
            "R_u sends ln T to -ln sqrt(S) and ln sqrt(S) to -ln T, so T maps to 1/sqrt(S) and sqrt(S) maps to 1/T.",
            "EXACT_ALGEBRA",
            "the candidate is concrete, not just a symbol.",
        ),
        (
            "RUA2176_3_involution",
            "involution check",
            "Applying R_u twice returns T and sqrt(S).",
            "PASS_ALGEBRAIC_INVOLUTION",
            "R_u is mathematically consistent as a Z2 operation.",
        ),
        (
            "RUA2176_4_constraint_surface",
            "u=0 surface",
            "On u=0, T sqrt(S)=1 and R_u acts trivially on T and sqrt(S).",
            "PASS_FIXED_CONSTRAINT_SURFACE",
            "the symmetry is compatible with the auxiliary branch after the constraint is imposed.",
        ),
        (
            "RUA2176_5_symplectic_lift",
            "canonical lift",
            "With p_u mapped to -p_u and p_v fixed, p_u du + p_v dv is preserved.",
            "PASS_CANONICAL_LIFT_CONDITIONAL",
            "the involution can act on the canonical skeleton from 2174.",
        ),
        (
            "RUA2176_6_current_readout",
            "current coframe readout",
            "Off u=0, theta_0=T cdt and theta_1=sqrt(S) dr are changed by R_u.",
            "READOUT_NOT_INVARIANT_OFF_CONSTRAINT",
            "R_u needs a v-only visible quotient or a constraint-before-readout owner.",
        ),
        (
            "RUA2176_7_parent_status",
            "parent-owned R_u",
            "Current MTS corpus derives R_u as a parent symmetry of H_core, matter, boundary and readout.",
            "NOT_DERIVED_CURRENT_CORPUS",
            "algebraic candidate exists; parent action/current ownership remains missing.",
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


def owner_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("ROG2176_0_Qvis", "visible quotient owner", "Q_vis depends on v and parent fields, not on u, after the constraint is imposed", "MISSING_V_ONLY_QUOTIENT_OWNER", "needed for empirical readout continuity"),
        ("ROG2176_1_Hcore", "H_core R_u invariance", "H_core(T,S,...) equals H_core(R_u(T,S),...) without importing GR exterior", "MISSING_PARENT_HCORE_INVARIANCE", "needed to kill I_u/J_u in the core"),
        ("ROG2176_2_current", "current/action owner", "source charge, tau and Hamiltonian current are R_u-even or quotient-descended", "MISSING_CURRENT_OWNER", "needed to stop source normalization from breaking R_u"),
        ("ROG2176_3_matter", "ordinary matter owner", "matter action has no u-dependent source-only weights and descends through the same visible quotient", "MISSING_MATTER_NO_SOURCE_SLOT", "needed to kill beta_source/w_u/J_u legs"),
        ("ROG2176_4_boundary", "boundary owner", "boundary/corner symplectic terms are R_u-even or zero-projection after u=0", "MISSING_BOUNDARY_OWNER", "needed to stop Q_u/Q_R hair"),
        ("ROG2176_5_stability", "radiative/readout stability", "effective reductions do not regenerate odd u terms", "MISSING_STABILITY_OWNER", "needed for a durable local-GR theorem"),
        ("ROG2176_6_success", "R_u owner package", "all owner gates close in one parent package", "NOT_SATISFIED_CURRENT_CORPUS", "otherwise finite I_u/J_u rows remain mandatory"),
    ]
    return [
        base_row(
            gate_id=gate_id,
            gate=gate,
            required_statement=required_statement,
            status=status,
            implication=implication,
        )
        for gate_id, gate, required_statement, status, implication in specs
    ]


def finite_row_rows() -> list[dict[str, Any]]:
    specs = [
        ("FIJ2176_0_Iu", "I_u", "linear p_u drift under the R_u candidate", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE", "p_u_coefficient_or_declared_normalized", "PPN;clock;orbital;local_GR"),
        ("FIJ2176_1_Ju", "J_u", "linear u source/readout coupling under the R_u candidate", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE", "u_source_coefficient_or_declared_normalized", "WEP;R10_source_leg;PPN_beta;clock;local_GR"),
        ("FIJ2176_2_Qvis_leak", "epsilon_Qvis_u", "residual u-dependence in visible quotient/readout", "MISSING_V_ONLY_QUOTIENT_BOUND", "dimensionless_readout_derivative", "PPN;clock;orbital"),
        ("FIJ2176_3_source_weight", "w_u_or_beta_u", "u-dependent source/action weight seam", "MISSING_NO_SOURCE_SLOT_OR_VALUE", "dimensionless_source_weight_derivative", "WEP;R10;PPN_source_normalization"),
        ("FIJ2176_4_boundary", "Q_u", "u-sector boundary/corner charge", "MISSING_BOUNDARY_ZERO_OR_VALUE", "boundary_charge_units", "orbital;PPN;R10_guard"),
        ("FIJ2176_5_total", "epsilon_Ru_abs", "absolute no-cancellation envelope for R_u-breaking terms", "MISSING_COMPONENT_VALUES", "declared_common_norm", "all_local_arenas"),
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


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2176_0_gain", "ALGEBRAIC_RU_CANDIDATE_CONSTRUCTED", "R_u keeps v=ln(T/sqrt(S)) fixed and flips u=ln(T sqrt(S)); in original variables T maps to 1/sqrt(S) and sqrt(S) maps to 1/T", "selected"),
        ("DEC2176_1_constraint", "RU_FIXED_ON_U_ZERO_SURFACE", "on T sqrt(S)=1 the candidate acts trivially, so it is compatible with constraint-before-readout", "selected"),
        ("DEC2176_2_readout", "CURRENT_READOUT_NOT_OFFSHELL_INVARIANT", "current theta_0/theta_1 readout sees T and sqrt(S) separately, so R_u needs a v-only quotient or constraint-before-readout owner", "selected"),
        ("DEC2176_3_no_claim", "PARENT_RU_NOT_DERIVED", "H_core, current, matter, boundary and stability owner gates remain unsigned", "selected"),
        ("DEC2176_4_next", "V_ONLY_QUOTIENT_OR_CURRENT_READOUT_LOCK_NEXT", "next target is visible quotient/readout ownership; if it fails, R_u stays closure-only and finite rows become primary", "selected"),
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
            route_id="NEXT2176_0_2177",
            selection_status="selected",
            target_file="2177-Y5-R2FR-v-only-visible-quotient-readout-owner-or-current-readout-lock.md",
            target_script="scripts/Y5_R2FR_v_only_visible_quotient_readout_owner_or_current_readout_lock_2177.py",
            objective="prove that visible local observables descend through the v=ln(T/sqrt(S)) quotient after u=0, making R_u a parent symmetry; if not, lock the current T/sqrt(S) readout and demote R_u to closure-only/finite residuals",
            success_condition="v-only quotient/readout owner preserves Newton, PPN, clocks, photons, source mass and orbits, or finite R_u-breaking rows become the live branch",
            do_not_do="do not erase T and sqrt(S) from the observed coframe after using them; do not claim R_u from algebra alone; do not import GR",
        ),
        base_row(
            route_id="NEXT2176_1_finite_parallel",
            selection_status="held_parallel",
            target_file="2177b-Y5-R2FR-first-Iu-Ju-finite-source-row-acquisition.md",
            target_script="scripts/Y5_R2FR_first_Iu_Ju_finite_source_row_acquisition_2177b.py",
            objective="if v-only readout fails, acquire the first real finite I_u or J_u source-backed row",
            success_condition="one finite row has units, source path, convention and arena projection while remaining nonclaim",
            do_not_do="do not score missing or symbolic I_u/J_u rows",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["finite_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["ru_algebra"], BRANCH_COPIES["branch_wep"]),
        ("source_weight", OUTPUTS["owner_gates"], BRANCH_COPIES["source_weight"]),
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
    validations.append(base_row(validation_id="VAL2176_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2176_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    algebra_statuses = {row["status"] for row in rows_by_name["ru_algebra"]}
    validations.append(base_row(validation_id="VAL2176_02_ru_algebra", status="PASS" if "PASS_ALGEBRAIC_INVOLUTION" in algebra_statuses and "READOUT_NOT_INVARIANT_OFF_CONSTRAINT" in algebra_statuses else "FAIL", detail="R_u candidate is algebraic involution but not current-readout invariant off constraint"))

    owner_statuses = {row["status"] for row in rows_by_name["owner_gates"]}
    validations.append(base_row(validation_id="VAL2176_03_owner_gates", status="PASS" if "MISSING_V_ONLY_QUOTIENT_OWNER" in owner_statuses and "NOT_SATISFIED_CURRENT_CORPUS" in owner_statuses else "FAIL", detail="parent owner gates remain unsigned"))

    finite_rows = rows_by_name["finite_rows"]
    finite_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in finite_rows)
    validations.append(base_row(validation_id="VAL2176_04_finite_rows", status="PASS" if finite_ok else "FAIL", detail=f"finite R_u-breaking rows={len(finite_rows)} remain score_ready=false"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2176_05_decision", status="PASS" if "V_ONLY_QUOTIENT_OR_CURRENT_READOUT_LOCK_NEXT" in decision_text else "FAIL", detail="decision selects v-only quotient/readout owner next"))

    validations.append(base_row(validation_id="VAL2176_06_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2177" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2177 v-only quotient/readout owner target selected"))

    validations.append(base_row(validation_id="VAL2176_07_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2176_08_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2176_09_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2176_artifacts()
    validations.append(base_row(validation_id="VAL2176_10_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2176 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2176_11_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2176_OVERALL", status="PASS" if overall else "FAIL", detail="2176 constructs the algebraic R_u candidate and selects v-only visible quotient/readout ownership as the next gate"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2176 - Y5/R2FR Parent R_u Involution Current Owner Or Finite I_u/J_u Row

## Current Verdict

2176 constructs the explicit reciprocal-cell involution candidate, but does **not** claim it as a parent symmetry.

Let `a=ln T`, `b=ln sqrt(S)`, `u=a+b`, and `v=a-b`. The clean candidate is:

`R_u: u -> -u`, `v -> v`.

In the original variables this means:

`T -> 1/sqrt(S)`, and `sqrt(S) -> 1/T`.

This is an honest algebraic involution. It flips `C_R=2u`, preserves the ratio variable `v`, fixes the `u=0` constraint surface pointwise, and has a canonical lift if `p_u -> -p_u`.

But the current observed coframe uses `T` and `sqrt(S)` separately. So off the constrained surface, `R_u` is not automatically a symmetry of clocks/rulers/readout. To make it physical, the parent theory must prove a visible quotient/readout owner: observables descend through `v` after `u=0`, without source, boundary or matter re-entry.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## R_u Involution Algebra

{md_table(rows_by_name["ru_algebra"], ["algebra_id", "object", "statement", "status", "implication", "valid_for_claim"])}

## R_u Owner Gate Ledger

{md_table(rows_by_name["owner_gates"], ["gate_id", "gate", "required_statement", "status", "implication", "valid_for_claim"])}

## I_u/J_u Finite Row Backstop

{md_table(rows_by_name["finite_rows"], ["row_id", "symbol", "definition", "status", "units", "observable_link", "value", "source_path", "score_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is a useful forward move. `R_u` is no longer an abstract wish: it has a concrete transformation law and a clear invariant variable `v`.

The price is also clear. If the observed theory really needs `T` and `sqrt(S)` separately before constraint, then `R_u` is not an off-shell readout symmetry. The next proof must either derive a `v`-only visible quotient after `u=0`, or lock the current readout and demote the `R_u` route to closure/finite residuals.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "ru_algebra": ru_algebra_rows(),
        "owner_gates": owner_gate_rows(),
        "finite_rows": finite_row_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "ru_algebra", "owner_gates", "finite_rows", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
