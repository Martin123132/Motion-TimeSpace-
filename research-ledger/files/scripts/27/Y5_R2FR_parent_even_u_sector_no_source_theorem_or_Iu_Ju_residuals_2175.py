from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2175"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2175-Y5-R2FR-parent-even-u-sector-no-source-theorem-or-Iu-Ju-residuals.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2175_SOURCE_REGISTER.csv",
    "even_theorem": OUT / "P8_Y5_PARENT_QLOC_2175_EVEN_U_SECTOR_THEOREM_AUDIT.csv",
    "symmetry_conditions": OUT / "P8_Y5_PARENT_QLOC_2175_SYMMETRY_DESCENT_CONDITIONS.csv",
    "residual_rows": OUT / "P8_Y5_PARENT_QLOC_2175_IU_JU_RESIDUAL_ROW_CONTRACT.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2175_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2175_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2175_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2175_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2175_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2175_IU_JU_RESIDUAL_ROW_CONTRACT_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2175_EVEN_U_SECTOR_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT_DOCS / "U_SECTOR_NO_SOURCE_THEOREM_2175_NONCLAIM.csv",
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


def formalization_has_2175_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2175-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2175*",
        "*P8_Y5_BRR545_2175*",
        "*Y5_R2FR_parent_even_u_sector_no_source_theorem_or_Iu_Ju_residuals_2175*",
        "*JR2175*",
        "*U_SECTOR_NO_SOURCE_THEOREM_2175*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2174_handoff",
            ROOT / "2174-Y5-R2FR-Hcore-canonical-bracket-closure-or-auxiliary-route-demotion.md",
            ["NEXT2174_0_2175", "PARENT_EVENNESS_NO_SOURCE_U_SECTOR_NEXT"],
            "2174 selects source-free/even u-sector theorem or I_u/J_u residuals.",
        ),
        (
            "2174_validation",
            OUT / "P8_Y5_BRR545_2174_VALIDATION.csv",
            ["VAL2174_OVERALL,PASS"],
            "2174 validation passed.",
        ),
        (
            "2164_evenness",
            ROOT / "2164-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-finite-vector-coefficients.md",
            ["EVENNESS_THEOREM_NOT_ACTIVATED", "J_Z/B_Z"],
            "2164 gives the exact conditional evenness theorem and coupling-lock failure.",
        ),
        (
            "1886_no_source_slot",
            ROOT / "1886-Y5-R2FR-common-matter-no-source-only-slot-proof-or-finite-wR-row.md",
            ["NO_SOURCE_ONLY_SLOT_NOT_PARENT_DERIVED", "SOURCE_WEIGHT_SEAM_IS_REAL"],
            "1886 keeps the source-only/action-weight seam live.",
        ),
        (
            "1885_beta_source",
            ROOT / "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
            ["NO_SOURCE_ONLY_SLOT_IS_NEXT_BEST_ATTACK", "BETA_NOT_DERIVED_FROM_GAMMA"],
            "1885 keeps beta/source coupling independent from gamma.",
        ),
        (
            "1892_matter_signature",
            ROOT / "1892-Y5-R2FR-ordinary-matter-action-signature-or-deltaw-species-projection-kernels.md",
            ["ORDINARY_MATTER_ACTION_SIGNATURE_NOT_PARENT_SIGNED", "OMAS1892_0_target_signature"],
            "1892 gives the ordinary-matter action signature needed to silence source coupling.",
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


def even_theorem_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "EUT2175_0_target",
            "u-sector target",
            "u=C_R/2 is the radial-cell coordinate and p_u is its conjugate momentum.",
            "SETUP",
            "I_u and J_u are the linear p_u and u coefficients in H_core.",
        ),
        (
            "EUT2175_1_canonical_involution",
            "reciprocal-cell involution",
            "A parent-owned involution R_u sends (u,p_u) to (-u,-p_u) while preserving the visible quotient data.",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "If signed, all terms odd under R_u are forbidden, including I_u p_u and J_u u.",
        ),
        (
            "EUT2175_2_time_reversal",
            "momentum parity",
            "A parent time-orientation/rest-frame rule forbids a bare linear p_u drift at u=0.",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "If signed, I_u=0 independently of the u-reflection argument.",
        ),
        (
            "EUT2175_3_source_evenness",
            "source/readout evenness",
            "Matter, boundary, source-normalization, clocks and readout functionals are even in u or quotient-descended before readout.",
            "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "If signed, J_u and boundary/readout linear source terms vanish at u=0.",
        ),
        (
            "EUT2175_4_no_source_slot",
            "no source-only action weight",
            "Ordinary matter has no independent source-only multiplier w_A(u), kappa_A(u), beta_w(u), or material source scalar.",
            "MISSING_PARENT_OBJECT_LANGUAGE",
            "Without this, J_u/beta_source can survive even if visible equations look common-frame.",
        ),
        (
            "EUT2175_5_theorem",
            "I_u/J_u theorem-zero",
            "If EUT2175_1 through EUT2175_4 are parent-signed in one action package, then I_u=J_u=0 and the second-class u-constraint branch is clean.",
            "EXACT_CONDITIONAL_THEOREM",
            "This is the clean local-GR auxiliary route, but it is conditional only.",
        ),
        (
            "EUT2175_6_verdict",
            "current parent status",
            "Current MTS corpus proves the even/source-free u-sector theorem.",
            "NOT_DERIVED_CURRENT_CORPUS",
            "The exact theorem is written; parent involution/current-owner/source-slot premises remain unsigned.",
        ),
    ]
    return [
        base_row(
            theorem_id=theorem_id,
            clause=clause,
            statement=statement,
            status=status,
            implication=implication,
        )
        for theorem_id, clause, statement, status, implication in specs
    ]


def symmetry_condition_rows() -> list[dict[str, Any]]:
    specs = [
        ("SYM2175_0_Ru", "R_u involution", "construct R_u from MTS primitives, not from a post-hoc u sign flip", "MISSING_PARENT_CONSTRUCTOR", "needed to forbid odd u-sector terms"),
        ("SYM2175_1_Qvis", "visible quotient preservation", "R_u leaves Q_vis, source mass convention, clocks, photons and orbital readout invariant after constraint", "MISSING_VISIBLE_QUOTIENT_PROOF", "needed so symmetry is not empirically destructive"),
        ("SYM2175_2_Hcore", "H_core invariance", "H_core composed with R_u equals H_core near u=0, with no GR exterior import", "MISSING_HCORE_SYMMETRY", "kills I_u and J_u in the core"),
        ("SYM2175_3_matter", "ordinary matter descent", "S_matter is R_u-even or quotient-descended and has no source-only u multipliers", "MISSING_MATTER_SIGNATURE", "kills source-side J_u and beta_source legs"),
        ("SYM2175_4_boundary", "boundary/readout descent", "boundary, tau, endpoint and readout maps are R_u-even or exact/no-flux after u=0", "MISSING_BOUNDARY_READOUT_SILENCE", "kills Q_R/readout re-entry"),
        ("SYM2175_5_radiative", "radiative/stability closure", "radiative/effective reductions do not regenerate odd u terms", "MISSING_STABILITY_THEOREM", "protects I_u/J_u beyond the formal parent level"),
        ("SYM2175_6_success", "full no-source u-sector", "all symmetry/descent clauses close simultaneously", "NOT_SATISFIED_CURRENT_CORPUS", "otherwise residual rows are mandatory"),
    ]
    return [
        base_row(
            condition_id=condition_id,
            condition=condition,
            required_statement=required_statement,
            status=status,
            implication=implication,
        )
        for condition_id, condition, required_statement, status, implication in specs
    ]


def residual_row_contract() -> list[dict[str, Any]]:
    specs = [
        ("IUR2175_0_Iu", "I_u", "linear p_u/motion-load drift coefficient in H_core", "p_u_coefficient_or_declared_normalized", "PPN;clock;orbital;local_GR", "MISSING_ZERO_THEOREM_OR_SOURCE_VALUE", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("IUR2175_1_Ju", "J_u", "linear u source/readout/matter coefficient in H_core", "u_source_coefficient_or_declared_normalized", "WEP;R10_source_leg;PPN_beta;clock;local_GR", "MISSING_NO_SOURCE_THEOREM_OR_SOURCE_VALUE", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("IUR2175_2_Lambda_reaction", "Lambda_R_reaction", "projection of Lambda_R response into visible coframe/source equations after u=0", "reaction_projection_norm", "PPN;clock;orbital;local_GR", "MISSING_INVISIBILITY_THEOREM_OR_BOUND", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("IUR2175_3_wu", "w_u_or_beta_u", "source-only u-dependent matter/action weight", "dimensionless_source_weight_derivative", "WEP;R10;PPN_source_normalization", "MISSING_NO_SOURCE_ONLY_SLOT_OR_VALUE", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("IUR2175_4_boundary", "B_u_or_Q_u", "boundary/corner reciprocal u charge after constraint", "boundary_flux_or_charge_units", "orbital;PPN;R10_guard", "MISSING_BOUNDARY_NO_CHARGE_OR_VALUE", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
        ("IUR2175_5_total", "epsilon_u_linear_abs", "absolute no-cancellation envelope for I_u, J_u, Lambda reaction, source weight and boundary u leaks", "declared_common_norm", "all_local_arenas", "MISSING_ALL_COMPONENTS", "MISSING_NUMERIC_VALUE", "MISSING_SOURCE_PATH"),
    ]
    return [
        base_row(
            row_id=row_id,
            symbol=symbol,
            definition=definition,
            units=units,
            observable_link=observable_link,
            status=status,
            value=value,
            source_path=source_path,
            no_cancellation_policy=True,
            score_ready=False,
        )
        for row_id, symbol, definition, units, observable_link, status, value, source_path in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2175_0_conditional_theorem", "even/source-free u theorem is logically valid under premises", "PASS_CONDITIONAL_NONCLAIM", "does not prove premises", False),
        ("CG2175_1_parent_involution", "R_u involution is parent-derived", "BLOCKED", "constructor and visible quotient ownership missing", False),
        ("CG2175_2_Iu_Ju_zero", "I_u=J_u=0 theorem-zero rows are live claim inputs", "BLOCKED", "symmetry/descent/source-slot clauses unsigned", False),
        ("CG2175_3_residual_score", "finite I_u/J_u residual rows are score-ready", "BLOCKED", "values, units, source paths and projections missing", False),
        ("CG2175_4_local_GR", "local GR/Newton follows from auxiliary u branch", "BLOCKED", "I_u/J_u plus boundary/matter/readout/beta gates remain open", False),
    ]
    return [
        base_row(
            gate_id=gate_id,
            claim=claim,
            status=status,
            blocked_by=blocked_by,
            score_ready=score_ready,
        )
        for gate_id, claim, status, blocked_by, score_ready in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2175_0_gain", "EXACT_EVEN_U_THEOREM_WRITTEN", "R_u/time-reversal/even-source premises would kill I_u and J_u without tuning", "selected"),
        ("DEC2175_1_no_claim", "THEOREM_NOT_PARENT_SIGNED", "R_u constructor, H_core symmetry, matter/source slot, boundary and stability clauses remain unsigned", "selected"),
        ("DEC2175_2_coupling", "SOURCE_WEIGHT_SEAM_REMAINS_LIVE", "1886-style source-only weights can become J_u/beta_source even when visible EOM look harmless", "selected"),
        ("DEC2175_3_residuals", "IU_JU_ROWS_ARE_THE_FALLBACK", "if parent symmetry fails, I_u/J_u become finite residual coefficients with no-cancellation policy", "selected"),
        ("DEC2175_4_next", "PARENT_RU_INVOLUTION_OR_FINITE_IU_JU_ROW_NEXT", "next step is to construct R_u/current-owner or start first real finite row acquisition", "selected"),
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
            route_id="NEXT2175_0_2176",
            selection_status="selected",
            target_file="2176-Y5-R2FR-parent-Ru-involution-current-owner-or-finite-Iu-Ju-row.md",
            target_script="scripts/Y5_R2FR_parent_Ru_involution_current_owner_or_finite_Iu_Ju_row_2176.py",
            objective="construct the parent reciprocal-cell involution R_u and current/action owner that make H_core and matter/source/readout even in u; if not, emit first finite I_u/J_u row contract",
            success_condition="R_u is parent-owned and kills I_u/J_u with no source/boundary/readout re-entry, or I_u/J_u are demoted to sourced finite residual rows",
            do_not_do="do not claim local GR from conditional parity alone, do not absorb source weights into G_N, do not import GR H_core",
        ),
        base_row(
            route_id="NEXT2175_1_boundary_parallel",
            selection_status="held_parallel",
            target_file="2176b-Y5-R2FR-u-boundary-no-charge-or-Qu-bound-row.md",
            target_script="scripts/Y5_R2FR_u_boundary_no_charge_or_Qu_bound_row_2176b.py",
            objective="prove boundary/corner u-charge silence or produce Q_u finite source row",
            success_condition="bulk u elimination cannot be reopened by boundary hair, or boundary residual is explicit",
            do_not_do="do not assume bulk second-class constraints kill boundary charge automatically",
        ),
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["residual_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["even_theorem"], BRANCH_COPIES["branch_wep"]),
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
    validations.append(base_row(validation_id="VAL2175_00_sources_exist", status="PASS" if all(row["path_exists"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['path_exists']) for row in source_rows)}/{len(source_rows)} sources exist"))
    validations.append(base_row(validation_id="VAL2175_01_needles_found", status="PASS" if all(row["needles_found"] for row in source_rows) else "FAIL", detail=f"{sum(bool(row['needles_found']) for row in source_rows)}/{len(source_rows)} source needle sets found"))

    theorem_statuses = {row["status"] for row in rows_by_name["even_theorem"]}
    validations.append(base_row(validation_id="VAL2175_02_even_theorem", status="PASS" if "EXACT_CONDITIONAL_THEOREM" in theorem_statuses and "NOT_DERIVED_CURRENT_CORPUS" in theorem_statuses else "FAIL", detail="even/source-free u theorem is exact conditional but not claimed"))

    condition_statuses = {row["status"] for row in rows_by_name["symmetry_conditions"]}
    validations.append(base_row(validation_id="VAL2175_03_symmetry_conditions", status="PASS" if "MISSING_PARENT_CONSTRUCTOR" in condition_statuses and "NOT_SATISFIED_CURRENT_CORPUS" in condition_statuses else "FAIL", detail="R_u and descent conditions remain unsigned"))

    residual_rows = rows_by_name["residual_rows"]
    residual_ok = all(str(row.get("status", "")).startswith("MISSING_") and not bool(row.get("score_ready")) for row in residual_rows)
    validations.append(base_row(validation_id="VAL2175_04_residual_rows", status="PASS" if residual_ok else "FAIL", detail=f"Iu/Ju residual rows={len(residual_rows)} remain score_ready=false"))

    gate_text = " ".join(str(row.get("status", "")) + str(row.get("blocked_by", "")) for row in rows_by_name["claim_gate"])
    validations.append(base_row(validation_id="VAL2175_05_claim_gates", status="PASS" if "BLOCKED" in gate_text and "symmetry/descent/source-slot clauses unsigned" in gate_text else "FAIL", detail="claim gates block local GR and residual scoring"))

    decision_text = " ".join(str(row.get("decision", "")) + " " + str(row.get("rationale", "")) for row in rows_by_name["decision"])
    validations.append(base_row(validation_id="VAL2175_06_decision", status="PASS" if "PARENT_RU_INVOLUTION_OR_FINITE_IU_JU_ROW_NEXT" in decision_text else "FAIL", detail="decision selects R_u/current-owner or finite row next"))

    validations.append(base_row(validation_id="VAL2175_07_next_target", status="PASS" if any(row["selection_status"] == "selected" and "2176" in row["target_file"] for row in rows_by_name["next_target"]) else "FAIL", detail="2176 R_u involution/finite row target selected"))

    validations.append(base_row(validation_id="VAL2175_08_claim_flags_false", status="PASS" if all_claim_flags_false(rows_by_name) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))

    parse_details: list[str] = []
    parse_pass = True
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        parse_pass = parse_pass and ok
        parse_details.append(f"{path.name}:{count if ok else detail}")
    validations.append(base_row(validation_id="VAL2175_09_csv_parse", status="PASS" if parse_pass else "FAIL", detail="; ".join(parse_details)))

    copy_rows = rows_by_name["branch_copies"]
    validations.append(base_row(validation_id="VAL2175_10_branch_copies", status="PASS" if all(row["copied"] for row in copy_rows) else "FAIL", detail=";".join(str(row["target_path"]) for row in copy_rows)))

    formalization_clean = not formalization_has_2175_artifacts()
    validations.append(base_row(validation_id="VAL2175_11_formalization_clean", status="PASS" if formalization_clean else "FAIL", detail="formalization-workbench has no 2175 artifacts"))

    remove_pycache()
    cache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    validations.append(base_row(validation_id="VAL2175_12_pycache_absent", status="PASS" if cache_absent else "FAIL", detail=str(ROOT / "scripts" / "__pycache__")))

    overall = all(row["status"] == "PASS" for row in validations)
    validations.append(base_row(validation_id="VAL2175_OVERALL", status="PASS" if overall else "FAIL", detail="2175 writes the exact even/source-free u-sector theorem and keeps I_u/J_u as finite residuals unless parent-signed"))
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2175 - Y5/R2FR Parent Even U-Sector No-Source Theorem Or I_u/J_u Residuals

## Current Verdict

2175 does **not** prove local GR/Newton and does **not** set `I_u=0` or `J_u=0` as current theorem-zero rows.

It does write the exact clean theorem we need:

If the parent theory owns a reciprocal-cell involution `R_u : (u,p_u) -> (-u,-p_u)`, if `H_core` is invariant under it, and if matter/source/boundary/readout functionals are even or quotient-descended with no source-only `u` slots, then the linear terms `I_u p_u` and `J_u u` are illegal. In that branch, `I_u=J_u=0` and the second-class auxiliary mechanism from 2174 becomes much cleaner.

Current MTS does not yet parent-sign the involution, source-current owner, ordinary-matter no-source slot, boundary silence or radiative/readout stability. So this is a strong conditional theorem, not a claim.

## Source Register

{md_table(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"])}

## Even U-Sector Theorem Audit

{md_table(rows_by_name["even_theorem"], ["theorem_id", "clause", "statement", "status", "implication", "valid_for_claim"])}

## Symmetry And Descent Conditions

{md_table(rows_by_name["symmetry_conditions"], ["condition_id", "condition", "required_statement", "status", "implication", "valid_for_claim"])}

## I_u/J_u Residual Row Contract

{md_table(rows_by_name["residual_rows"], ["row_id", "symbol", "definition", "units", "observable_link", "status", "value", "source_path", "score_ready", "valid_for_claim"])}

## Claim Gate

{md_table(rows_by_name["claim_gate"], ["gate_id", "claim", "status", "blocked_by", "score_ready", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "rationale", "selection_status", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"])}

## Branch Copies

{md_table(rows_by_name["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "valid_for_claim"])}

## Validation

{md_table(rows_by_name["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"])}

## Working Interpretation

This is promising in a precise way. The auxiliary mechanism is no longer just "add Lambda and hope": it now has a conditional symmetry theorem that would kill the two linear leaks that matter.

But the theory still has to earn that theorem. The next real step is to construct the parent `R_u` involution/current owner, or admit that `I_u/J_u` are finite residual couplings to be sourced and tested.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)

    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "even_theorem": even_theorem_rows(),
        "symmetry_conditions": symmetry_condition_rows(),
        "residual_rows": residual_row_contract(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    for name in ["source_register", "even_theorem", "symmetry_conditions", "residual_rows", "claim_gate", "decision", "next_target"]:
        write_csv(OUTPUTS[name], rows_by_name[name])

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()


if __name__ == "__main__":
    main()
