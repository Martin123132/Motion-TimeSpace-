from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1256"
TITLE = "1256-Y5-R10-parent-Hcore-reciprocal-source-equation-minimal-reentry"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
HCORE_CONTRACT_PATH = OUT_DIR / f"{PACK_ID}_MINIMAL_HCORE_SOURCE_EQUATION_CONTRACT.csv"
BRANCH_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_VARIATIONAL_BRANCH_AUDIT.csv"
BOUNDARY_AUDIT_PATH = OUT_DIR / f"{PACK_ID}_BOUNDARY_TERM_AUDIT.csv"
COEFFICIENT_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_COEFFICIENT_REQUIREMENTS.csv"
CASSINI_CEILING_PATH = OUT_DIR / f"{PACK_ID}_CASSINI_CEILING_COMPATIBILITY.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1256_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def recent_formalization_writes() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    recent: list[Path] = []
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if mtime >= RUN_STARTED_UTC:
                recent.append(path)
    return recent


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1256_0_1255_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1255_NEXT_TARGET.csv",
            "needle": "NEXT1255_0_1256",
            "purpose": "handoff back to parent H_core reciprocal source equation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1256_1_1255_ceiling",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1255_1249_RUNNER_SNAPSHOT.csv",
            "needle": "READY_NONCLAIM_NUMERIC_PASS",
            "purpose": "nonclaim q_Rhat ceiling now available as empirical guardrail",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1256_2_1253_Hcore",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1253_RECIPROCAL_HCORE_SOURCE_EQUATION_ATTEMPT.csv",
            "needle": "SOURCE_EQUATION_NOT_DERIVED",
            "purpose": "previous H_core source equation failure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1256_3_11_current",
            "local_path": "11-cell-current-origin-attempt.md",
            "needle": "W partial_r R_AB = Q_R",
            "purpose": "current conservation gives charge, not zero",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1256_4_07_constraint",
            "local_path": "07-nonpropagating-reciprocity-constraint.md",
            "needle": "S_constraint = integral lambda_R R_AB",
            "purpose": "nonpropagating constraint branch",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1256_5_10_contract",
            "local_path": "10-observer-map-symplectic-contract.md",
            "needle": "a genuine constraint whose multiplier has a parent origin",
            "purpose": "acceptable parent routes for local reciprocity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1256_6_1240_projection",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
            "needle": "gamma_minus_1_QR approximately -q_R_hat/2",
            "purpose": "finite Q_R to local gamma residual map",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1256_7_1255_raw",
            "local_path": "source-intake/qr-hat/raw/QRHAT1255_CASSINI_GAMMA_PHENOMENOLOGICAL_BOUND_NONCLAIM.csv",
            "needle": "QRHAT1255_CASSINI_GAMMA_1SIGMA_BOUND_NONCLAIM",
            "purpose": "active nonclaim q_Rhat ceiling row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    hcore_contract = [
        {
            "contract_id": "HC1256_0_minimal_density",
            "object": "reciprocal H_core sector",
            "minimal_form": "H_R = int_Sigma sqrt(h)[1/2 Z_R h^{ij} D_i R_AB D_j R_AB + 1/2 M_R^2 R_AB^2 + lambda_R R_AB + J_R R_AB] + int_boundary B_R",
            "variation": "E_R := delta H_R/delta R_AB = -D_i(Z_R D^i R_AB)+M_R^2 R_AB+lambda_R+J_R plus coefficient-variation terms",
            "boundary_term": "Pi_R^n delta R_AB with Pi_R^n = Z_R n^i D_i R_AB + partial B_R/partial R_AB",
            "status": "FORMAL_VARIATIONAL_CONTRACT_NOT_PARENT_SIGNED",
            "missing": "parent origin of Z_R, M_R^2, lambda_R, J_R, B_R, matter descent, and coefficient variations",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "HC1256_1_spherical_exterior",
            "object": "weak-field exterior current",
            "minimal_form": "for Z_R constant, M_R=0, lambda_R=J_R=0: partial_r(r^2 Z_R partial_r R_AB)=0",
            "variation": "r^2 Z_R partial_r R_AB = Q_R",
            "boundary_term": "Q_R = int_{S_r} Pi_R^n dS in the declared normalization",
            "status": "RECOVERS_11_CURRENT_SHAPE_ONLY",
            "missing": "does not prove Q_R=0 and does not derive a finite Q_R value",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    branch_audit = [
        {
            "branch_id": "BR1256_0_nonprop_constraint",
            "branch": "Z_R=0 and parent-owned lambda_R R_AB",
            "equation_result": "R_AB=0 from delta/delta lambda_R",
            "local_GR_effect": "would kill Q_R hair and close the gamma residual if parent-signed",
            "current_status": "BEST_ZERO_ROUTE_BUT_UNSIGNED",
            "blocker": "lambda_R origin, Dirac chain, matter compatibility, and boundary silence remain missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1256_1_kinetic_finite_hair",
            "branch": "Z_R>0, M_R=0, no source neutrality",
            "equation_result": "exterior R_AB = -Q_R/(Z_R r) after asymptotic offset is killed",
            "local_GR_effect": "finite gamma residual q_Rhat must be below the 1255 Cassini ceiling",
            "current_status": "TESTABLE_BUT_NOT_DERIVED",
            "blocker": "Q_R/Z_R source value and boundary class are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1256_2_massive_suppressed_hair",
            "branch": "Z_R>0 and M_R^2>0",
            "equation_result": "R_AB exterior has Yukawa-like suppression with range ell_R=sqrt(Z_R/M_R^2) in the simplest constant-coefficient limit",
            "local_GR_effect": "could suppress local PPN while allowing nonlocal/cosmological branch if scale separation is derived",
            "current_status": "PROMISING_CONCEPTUAL_ROUTE_NOT_SOURCED",
            "blocker": "M_R^2, Z_R, source coupling J_R, and scale separation are not parent-derived",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": "BR1256_3_boundary_nohair",
            "branch": "Pi_R^n=0 or exact boundary flux for physical local sources",
            "equation_result": "Q_R=0 only if natural boundary condition/source neutrality is parent-owned",
            "local_GR_effect": "would close reciprocal hair without necessarily inserting R_AB=0 everywhere",
            "current_status": "POSSIBLE_BUT_NOT_PROVED",
            "blocker": "physical source/test boundaries have not been shown compact-proper, exact, or neutral",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    boundary_audit = [
        {
            "boundary_id": "BA1256_0_variation_surface",
            "object": "Pi_R^n",
            "required_condition": "boundary variation must be cancelled, fixed, exact, or shown zero for physical source boundaries",
            "current_status": "OPEN",
            "claim_risk": "hidden boundary charge can reappear as q_Rhat/gamma hair",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "boundary_id": "BA1256_1_reference_subtraction",
            "object": "B_R reference/counterterm",
            "required_condition": "reference subtraction must not hide observed GM or import GR AB=1",
            "current_status": "MISSING",
            "claim_risk": "could zero the charge by convention rather than theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "boundary_id": "BA1256_2_source_worldtube",
            "object": "allowed local source boundary class",
            "required_condition": "source worldtubes must be shown neutral/proper/exact or assigned a finite residual row",
            "current_status": "MISSING",
            "claim_risk": "proper compact silence may be wrongly promoted to real matter boundaries",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    coefficient_requirements = [
        {
            "coefficient_id": "COEF1256_0_ZR",
            "symbol": "Z_R",
            "needed_for": "kinetic reciprocal hair and massive suppression",
            "must_be_sourced_by": "parent H_core/L_MTS_core coefficient or theorem-zero",
            "current_status": "MISSING",
            "if_missing": "cannot compute Q_R/Z_R or ell_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "COEF1256_1_MR2",
            "symbol": "M_R^2",
            "needed_for": "local Yukawa suppression range ell_R=sqrt(Z_R/M_R^2)",
            "must_be_sourced_by": "parent potential/second variation around local vacuum",
            "current_status": "MISSING",
            "if_missing": "massive suppression branch stays conceptual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "COEF1256_2_lambdaR",
            "symbol": "lambda_R",
            "needed_for": "nonpropagating R_AB=0 constraint",
            "must_be_sourced_by": "parent multiplier origin and Dirac closure",
            "current_status": "UNSIGNED",
            "if_missing": "constraint branch remains closure/ansatz",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "COEF1256_3_JR",
            "symbol": "J_R",
            "needed_for": "source coupling and finite Q_R",
            "must_be_sourced_by": "matter descent/source current map",
            "current_status": "MISSING",
            "if_missing": "cannot tell whether matter sources reciprocal charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "coefficient_id": "COEF1256_4_BR",
            "symbol": "B_R",
            "needed_for": "boundary flux/no-hair theorem",
            "must_be_sourced_by": "boundary variation and allowed source-boundary class",
            "current_status": "MISSING",
            "if_missing": "cannot prove Q_R=0 or normalize finite Q_R",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    cassini_ceiling = [
        {
            "ceiling_id": "CEIL1256_0_available_guardrail",
            "input": "1255 nonclaim Cassini gamma ceiling",
            "bound": "abs(q_R_hat)<=4.6e-05",
            "applies_to": "finite kinetic/boundary residual branch only",
            "does_not_apply_to": "parent derivation claim or local-GR proof",
            "status": "AVAILABLE_AS_SMOKE_CEILING",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "ceiling_id": "CEIL1256_1_finite_branch_test",
            "input": "future Q_R/Z_R or q_Rhat prediction",
            "bound": "must satisfy abs(gamma_minus_1_QR)=abs(q_R_hat)/2 <= 2.3e-5 under strict one-sigma smoke",
            "applies_to": "future parent-derived finite coefficient",
            "does_not_apply_to": "phenomenological ceiling row itself",
            "status": "WAITING_FOR_PARENT_QRHAT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "GATE1256_0_variational_contract",
            "claim": "minimal reciprocal H_core variational contract written",
            "status": "PASS_NONCLAIM",
            "reason": "E_R and Pi_R^n contract are explicit but not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1256_1_zero_theorem",
            "claim": "Q_R=0 theorem derived",
            "status": "BLOCKED",
            "reason": "nonpropagating/boundary routes still lack parent multiplier or no-hair proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1256_2_finite_prediction",
            "claim": "finite MTS q_Rhat prediction exists",
            "status": "BLOCKED",
            "reason": "Z_R, Q_R/J_R, B_R, and source boundary class are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1256_3_local_GR",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED",
            "reason": "contract narrows the route but does not close zero, finite, matter, beta, or boundary gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1256_0_contract",
            "decision": "the reciprocal local branch now has a minimal parent-action contract",
            "because": "every viable route must choose values/status for Z_R, M_R^2, lambda_R, J_R, and B_R",
            "next_action": "attack the coefficient-origin problem, starting with whether Z_R is zero, positive, or absent by symmetry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1256_1_best_route",
            "decision": "best next derivation target is the Z_R/lambda_R selector",
            "because": "Z_R=0 with parent lambda_R gives the clean GR route; Z_R>0 requires finite q_Rhat or massive suppression",
            "next_action": "1257-Y5-R10-ZR-lambdaR-selector-from-parent-primitives.md",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1256_0_1257",
            "target_file": "1257-Y5-R10-ZR-lambdaR-selector-from-parent-primitives.md",
            "target_script": "scripts/Y5_R10_ZR_lambdaR_selector_from_parent_primitives.py",
            "task": "try to derive whether the reciprocal sector is nonpropagating (Z_R=0 with parent lambda_R) or kinetic/suppressed (Z_R>0, possibly M_R^2>0)",
            "success_condition": "produce a parent-selector theorem candidate or an explicit fork ledger that routes to zero constraint, finite q_Rhat, or massive suppression without mixing them",
            "do_not": "do not infer Z_R=0 from desire for GR and do not use the Cassini ceiling as a derived coefficient",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (HCORE_CONTRACT_PATH, hcore_contract),
        (BRANCH_AUDIT_PATH, branch_audit),
        (BOUNDARY_AUDIT_PATH, boundary_audit),
        (COEFFICIENT_REQUIREMENTS_PATH, coefficient_requirements),
        (CASSINI_CEILING_PATH, cassini_ceiling),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]

    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(str(row["local_path"]), str(row["needle"])) for row in source_register]
    sources_exist = all(exists for exists, _ in source_checks)
    needles_found = all(found for _, found in source_checks)
    contract_has_ER = any("E_R :=" in row["variation"] for row in hcore_contract)
    contract_has_boundary = any("Pi_R^n" in row["boundary_term"] for row in hcore_contract)
    branches_complete = {row["branch_id"] for row in branch_audit} == {
        "BR1256_0_nonprop_constraint",
        "BR1256_1_kinetic_finite_hair",
        "BR1256_2_massive_suppressed_hair",
        "BR1256_3_boundary_nohair",
    }
    coefficient_missing_visible = all(row["current_status"] in {"MISSING", "UNSIGNED"} for row in coefficient_requirements)
    ceiling_nonclaim = all(is_false(row["valid_for_claim"]) and is_false(row["claim_allowed"]) for row in cassini_ceiling)
    claims_ok = all(row["status"] in {"PASS_NONCLAIM", "BLOCKED"} and is_false(row["claim_allowed"]) for row in claim_gates)
    all_nonclaim = all(
        is_false(row.get("valid_for_claim", "")) and is_false(row.get("claim_allowed", ""))
        for _, rows in generated_tables
        for row in rows
    )
    next_is_1257 = next_target[0]["target_file"].startswith("1257-")

    csv_parse_details: list[str] = []
    csv_parse_ok = True
    for path, _ in generated_tables:
        try:
            rows = read_csv(path)
            csv_parse_details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            csv_parse_details.append(f"{path.name}:ERROR:{exc}")

    formalization_writes = recent_formalization_writes()

    validation_rows = [
        validation_row("VAL1256_0_sources_exist", "all cited local sources exist", sources_exist, f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist"),
        validation_row("VAL1256_1_needles_found", "all cited local needles found", needles_found, f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found"),
        validation_row("VAL1256_2_contract_ER", "minimal H_core contract defines E_R", contract_has_ER, "E_R := delta H_R/delta R_AB present"),
        validation_row("VAL1256_3_contract_boundary", "minimal H_core contract defines boundary momentum", contract_has_boundary, "Pi_R^n boundary term present"),
        validation_row("VAL1256_4_branches_complete", "all reciprocal variational branches are separated", branches_complete, f"branch_rows={len(branch_audit)}"),
        validation_row("VAL1256_5_coefficients_missing_visible", "missing coefficient owners remain explicit", coefficient_missing_visible, f"coefficient_rows={len(coefficient_requirements)}"),
        validation_row("VAL1256_6_ceiling_nonclaim", "Cassini q_Rhat ceiling is nonclaim only", ceiling_nonclaim, "ceiling applies only to future finite residual branch"),
        validation_row("VAL1256_7_claim_gates", "claim gates keep local GR and finite prediction blocked", claims_ok, f"claim_gate_rows={len(claim_gates)}"),
        validation_row("VAL1256_8_nonclaim_policy", "all generated rows remain nonclaim", all_nonclaim, "valid_for_claim=false and claim_allowed=false throughout generated tables"),
        validation_row("VAL1256_9_next_target_1257", "next target is Z_R/lambda_R selector", next_is_1257, str(next_target[0]["target_file"])),
        validation_row("VAL1256_10_csv_parse", "all generated CSVs parse cleanly", csv_parse_ok, "; ".join(csv_parse_details)),
        validation_row("VAL1256_11_formalization_untouched", "formalization-workbench untouched during run", not formalization_writes, f"formalization_recent_write_count_since_run_start={len(formalization_writes)}"),
    ]
    overall = all(row["status"] == "PASS" for row in validation_rows)
    validation_rows.append(
        validation_row(
            "VAL1256_12_overall",
            "overall 1256 validation",
            overall,
            "1256 writes the minimal reciprocal H_core source-equation contract, separates zero/finite/suppressed/boundary branches, and keeps claims blocked",
        )
    )
    write_csv(VALIDATION_PATH, validation_rows)

    doc = f"""# {TITLE}

**Current verdict:** 1256 gets us closer to the derivation target but does not close it. The reciprocal local branch now has a minimal parent-action contract: `E_R := delta H_R/delta R_AB` plus boundary momentum `Pi_R^n`.

**Main progress:** the route is split cleanly into four boxes: nonpropagating constraint, kinetic finite hair, massive/suppressed hair, and boundary no-hair. Each box now has explicit coefficient requirements rather than a vague “coupling problem.”

**No-claim guard:** no `Q_R=0` theorem, finite MTS `q_R_hat` prediction, local PPN pass, or local-GR/Newton derivation is promoted. The 1255 Cassini ceiling remains a smoke guardrail only.

Generated UTC: {datetime.now(timezone.utc).isoformat()}

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## Minimal H_core Source Equation Contract
{markdown_table(hcore_contract, ["contract_id", "object", "minimal_form", "variation", "boundary_term", "status", "missing", "valid_for_claim", "claim_allowed"])}

## Variational Branch Audit
{markdown_table(branch_audit, ["branch_id", "branch", "equation_result", "local_GR_effect", "current_status", "blocker", "valid_for_claim", "claim_allowed"])}

## Boundary Term Audit
{markdown_table(boundary_audit, ["boundary_id", "object", "required_condition", "current_status", "claim_risk", "valid_for_claim", "claim_allowed"])}

## Coefficient Requirements
{markdown_table(coefficient_requirements, ["coefficient_id", "symbol", "needed_for", "must_be_sourced_by", "current_status", "if_missing", "valid_for_claim", "claim_allowed"])}

## Cassini Ceiling Compatibility
{markdown_table(cassini_ceiling, ["ceiling_id", "input", "bound", "applies_to", "does_not_apply_to", "status", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
