from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_Q_REPRESENTATION_NO_WEYL_SPURION_2530"
CHECKPOINT_ID = "2530"
DOC = ROOT / "2530-Y5-R2FR-q-representation-no-Weyl-spurion-or-BqWeyl-bound-row.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_SOURCE_REGISTER.csv",
    "linear_zero_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_LINEAR_BQWEYL_ZERO_AUDIT.csv",
    "no_spurion_contract": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_NO_SPURION_CONTRACT.csv",
    "linear_bound_row": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_BQWEYL_BOUND_ROW_STATUS.csv",
    "quadratic_reentry": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_QUADRATIC_WEYL_REENTRY.csv",
    "claim_gates": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_CLAIM_GATES.csv",
    "refusal_runner": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_REFUSAL_RUNNER.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2530_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2530_VALIDATION.csv",
}

BRANCH_COPIES = {
    "linear_zero_audit": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Linear_BqWeyl_zero_audit_2530_NONCLAIM.csv",
    "no_spurion_contract": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "No_Weyl_spurion_contract_2530_NONCLAIM.csv",
    "linear_bound_row": ROOT
    / "source-intake"
    / "local_bounds"
    / "BqWeyl_linear_bound_row_2530_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "DqWeyl2_2530_NEXT_TARGET_NONCLAIM.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": "False",
        "claim_allowed": "False",
        **row,
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


SOURCE_SPECS = [
    {
        "source_id": "SRC2530_0_2529_doc",
        "source_path": "2529-Y5-R2FR-psi-determinant-quotient-map-or-finite-qR-coefficients.md",
        "needle": "NEXT2529_0_selected",
        "role": "current handoff selecting B_qWeyl row",
    },
    {
        "source_id": "SRC2530_1_2529_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2529_VALIDATION.csv",
        "needle": "VAL2529_OVERALL,PASS",
        "role": "2529 validation anchor",
    },
    {
        "source_id": "SRC2530_2_2365_doc",
        "source_path": "2365-Y5-R2FR-q-representation-no-Weyl-spurion-or-BqWeyl-bound-row.md",
        "needle": "LBZ2365_4_linear_verdict",
        "role": "linear Weyl index lemma and no-spurion precedent",
    },
    {
        "source_id": "SRC2530_3_2365_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2365_VALIDATION.csv",
        "needle": "VAL2365_OVERALL,PASS",
        "role": "2365 validation anchor",
    },
    {
        "source_id": "SRC2530_4_2365_zero",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2365_LINEAR_BQWEYL_ZERO_AUDIT.csv",
        "needle": "LBZ2365_4_linear_verdict",
        "role": "linear BqWeyl zero audit rows",
    },
    {
        "source_id": "SRC2530_5_2365_nospurion",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2365_NO_SPURION_CONTRACT.csv",
        "needle": "NSC2365_6_verdict",
        "role": "no-spurion object-language contract",
    },
    {
        "source_id": "SRC2530_6_2365_quad",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2365_QUADRATIC_WEYL_REENTRY.csv",
        "needle": "QWR2365_5_verdict",
        "role": "quadratic Weyl re-entry branch",
    },
    {
        "source_id": "SRC2530_7_2366_doc",
        "source_path": "2366-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
        "needle": "DQC2366_4_verdict",
        "role": "quadratic Weyl coefficient and operator-normalization precedent",
    },
    {
        "source_id": "SRC2530_8_2366_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2366_VALIDATION.csv",
        "needle": "VAL2366_OVERALL,PASS",
        "role": "2366 validation anchor",
    },
]


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = ROOT / spec["source_path"]
        rows.append(
            stamp(
                {
                    **spec,
                    "path_exists": str(path.exists()),
                    "needle_found": str(contains(path, spec["needle"])),
                    "status": "SOURCE_OK" if path.exists() and contains(path, spec["needle"]) else "SOURCE_BLOCKED",
                }
            )
        )
    return rows


def linear_zero_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "LBZ2530_0_metric_trace",
            "test": "metric-only one-Weyl contraction",
            "lemma": "a scalar linear in one Weyl tensor cannot be formed using only metric contractions because the Weyl tensor is trace-free",
            "status": "EXACT_INDEX_LEMMA",
            "claim_scope": "safe only inside a metric-only q scalar/quotient grammar",
        },
        {
            "row_id": "LBZ2530_1_epsilon_trace",
            "test": "epsilon-only one-Weyl contraction",
            "lemma": "a single Weyl tensor also has no parity-odd scalar source from epsilon alone; parity-odd scalars start at C*Cdual",
            "status": "EXACT_INDEX_LEMMA",
            "claim_scope": "does not kill quadratic Weyl or pseudoscalar towers",
        },
        {
            "row_id": "LBZ2530_2_spurion_countermodel",
            "test": "q P^{abcd} C_abcd",
            "lemma": "a four-index parent/readout/projector spurion immediately permits a linear Weyl source",
            "status": "COUNTERMODEL_SURVIVES",
            "claim_scope": "this is the precise object-language clause that must be forbidden",
        },
        {
            "row_id": "LBZ2530_3_parent_signature",
            "test": "typed no-Weyl-spurion grammar",
            "lemma": "linear B_qWeyl vanishes only if q is scalar/quotient/pure-density and the parent action has no Weyl-type spurion, projector, hidden tensor or readout kernel",
            "status": "NOT_PARENT_SIGNED",
            "claim_scope": "contract exists; current MTS source does not adopt it as theorem",
        },
        {
            "row_id": "LBZ2530_4_linear_verdict",
            "test": "linear B_qWeyl status",
            "lemma": "linear Weyl kill is mathematically strong but evidence-weak as a parent action claim",
            "status": "DEMOTE_TO_CLOSURE_ONLY",
            "claim_scope": "no local-GR/Newton claim",
        },
    ]
    return [stamp(row) for row in rows]


def no_spurion_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NSC2530_0_q_representation",
            "clause": "q representation",
            "needed": "q is a scalar/quotient/pure-density field, not a Weyl-index carrier",
            "status": "MISSING_Q_REPRESENTATION_CERTIFICATE",
        },
        {
            "row_id": "NSC2530_1_allowed_tensor_slots",
            "clause": "allowed tensor slots",
            "needed": "parent action grammar lists allowed contractions and excludes one-Weyl scalar source slots",
            "status": "MISSING_OBJECT_LANGUAGE_SIGNATURE",
        },
        {
            "row_id": "NSC2530_2_no_projector",
            "clause": "no Weyl projector/spurion",
            "needed": "no P^{abcd}, hidden anisotropic tensor, material frame, or readout kernel can contract one Weyl tensor",
            "status": "MISSING_NO_PROJECTOR_THEOREM",
        },
        {
            "row_id": "NSC2530_3_boundary_readout",
            "clause": "boundary/readout stability",
            "needed": "integration by parts, boundary kernels and readout maps do not regenerate a Weyl spurion",
            "status": "MISSING_BOUNDARY_READOUT_STABILITY",
        },
        {
            "row_id": "NSC2530_4_radiative_regeneration",
            "clause": "radiative/no-regeneration rule",
            "needed": "loops/integrating-out cannot regenerate q P^{abcd} C_abcd",
            "status": "MISSING_NO_REGENERATION_THEOREM",
        },
        {
            "row_id": "NSC2530_5_verdict",
            "clause": "no-spurion contract",
            "needed": "NSC2530_0..4 all parent-signed together",
            "status": "CONTRACT_READY_THEOREM_NOT_SIGNED",
        },
    ]
    return [stamp(row) for row in rows]


def bound_row_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "BQB2530_0_zero_switch",
            "quantity": "Z_BqWeyl_linear",
            "status": "ZERO_SWITCH_FALSE",
            "units": "dimensionless_bool",
            "needed_for_claim": "parent-signed no-spurion contract",
        },
        {
            "row_id": "BQB2530_1_parent_coefficient",
            "quantity": "B_qWeyl",
            "status": "MISSING_PARENT_COEFFICIENT",
            "units": "parent_normalized",
            "needed_for_claim": "action coefficient or theorem-zero source",
        },
        {
            "row_id": "BQB2530_2_q_operator",
            "quantity": "L_q/G_q",
            "status": "MISSING_Q_OPERATOR_NORMALIZATION",
            "units": "operator_declared",
            "needed_for_claim": "same-domain q Green operator",
        },
        {
            "row_id": "BQB2530_3_weyl_profile",
            "quantity": "C_Weyl_local",
            "status": "MISSING_DOMAIN_PROFILE",
            "units": "length^-2",
            "needed_for_claim": "local source/domain Weyl profile",
        },
        {
            "row_id": "BQB2530_4_projection",
            "quantity": "tau_BqWeyl_arena",
            "status": "MISSING_ARENA_PROJECTION",
            "units": "arena_specific",
            "needed_for_claim": "R10/PPN/clock/orbital projection kernels",
        },
        {
            "row_id": "BQB2530_5_acceptance",
            "quantity": "linear_BqWeyl_claim",
            "status": "CLAIM_BLOCKED",
            "units": "boolean",
            "needed_for_claim": "zero route or all finite rows sourced",
        },
    ]
    return [stamp(row) for row in rows]


def quadratic_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "QWR2530_0_DqWeyl2",
            "object": "D_qWeyl2",
            "status": "LIVE_NONCLAIM_RESIDUAL",
            "why_survives": "q C_abcd C^abcd is a legal scalar unless higher-curvature/no-regeneration grammar forbids it",
        },
        {
            "row_id": "QWR2530_1_DqWeylDual",
            "object": "D_qWeylDual",
            "status": "LIVE_NONCLAIM_RESIDUAL",
            "why_survives": "q C_abcd *C^abcd is the parity/orientation branch not killed by one-Weyl index lemma",
        },
        {
            "row_id": "QWR2530_2_no_tower",
            "object": "Z_DqWeyl2",
            "status": "ZERO_THEOREM_NOT_DERIVED",
            "why_survives": "requires no bare Weyl2, no integrated-out regeneration and no hidden coefficient morphism",
        },
        {
            "row_id": "QWR2530_3_kernel",
            "object": "K_C2_ext",
            "status": "ANALYTIC_KERNEL_READY_NONCLAIM",
            "why_survives": "exterior Schwarzschild/Weyl2 kernel is useful plumbing only without coefficient and q operator",
        },
        {
            "row_id": "QWR2530_4_inputs",
            "object": "D_qWeyl2;L_q/G_q;P_obs",
            "status": "BLOCKED_INPUTS_MISSING",
            "why_survives": "2366 confirms coefficient/operator/projection rows remain unsourced",
        },
        {
            "row_id": "QWR2530_5_verdict",
            "object": "quadratic Weyl branch",
            "status": "SELECT_NEXT_COEFFICIENT_OR_Q_OPERATOR_TARGET",
            "why_survives": "even a linear Weyl kill does not finish the local branch",
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CG2530_0_linear_index_zero",
            "claim": "linear B_qWeyl is theorem-zero for current MTS",
            "allowed": "False",
            "blocked_by": "NSC2530_0_q_representation;NSC2530_2_no_projector;NSC2530_3_boundary_readout",
        },
        {
            "row_id": "CG2530_1_linear_finite_bound",
            "claim": "linear B_qWeyl finite row is score-ready",
            "allowed": "False",
            "blocked_by": "BQB2530_1_parent_coefficient;BQB2530_2_q_operator;BQB2530_3_weyl_profile;BQB2530_4_projection",
        },
        {
            "row_id": "CG2530_2_quadratic_Weyl_zero",
            "claim": "quadratic Weyl branch is zero",
            "allowed": "False",
            "blocked_by": "QWR2530_0_DqWeyl2;QWR2530_1_DqWeylDual;QWR2530_2_no_tower",
        },
        {
            "row_id": "CG2530_3_local_GR_Newton",
            "claim": "local GR/Newton branch derived",
            "allowed": "False",
            "blocked_by": "CG2530_0_linear_index_zero;CG2530_2_quadratic_Weyl_zero",
        },
        {
            "row_id": "CG2530_4_public_or_github",
            "claim": "public/GitHub update recommended from 2530",
            "allowed": "False",
            "blocked_by": "linear no-spurion and quadratic Weyl remain nonclaim",
        },
    ]
    return [stamp(row) for row in rows]


def refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "REF2530_0_index_lemma_as_parent",
            "shortcut": "treat the one-Weyl index lemma as a parent action theorem",
            "verdict": "REJECT",
            "reason": "the lemma only works after the q representation/no-spurion grammar is parent-signed",
        },
        {
            "row_id": "REF2530_1_vacuum_kills_weyl",
            "shortcut": "claim exterior vacuum kills Weyl residuals",
            "verdict": "REJECT",
            "reason": "Weyl survives in exterior vacuum",
        },
        {
            "row_id": "REF2530_2_ignore_spurion",
            "shortcut": "ignore possible P^{abcd} / hidden tensor / readout kernel",
            "verdict": "REJECT",
            "reason": "one such object revives linear B_qWeyl immediately",
        },
        {
            "row_id": "REF2530_3_linear_kill_finishes_local_GR",
            "shortcut": "declare local GR after linear B_qWeyl is conditionally killed",
            "verdict": "REJECT",
            "reason": "quadratic Weyl and source/operator rows remain live",
        },
        {
            "row_id": "REF2530_4_placeholder_bound",
            "shortcut": "fill B_qWeyl with placeholder coefficient/profile/projection",
            "verdict": "REJECT",
            "reason": "finite row needs sourced coefficient, q operator, Weyl profile, units and arena projection",
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DEC2530_0_linear_index",
            "decision": "retain one-Weyl index theorem as a conditional lever",
            "reason": "it is mathematically exact under metric/epsilon-only no-spurion grammar",
            "effect": "linear B_qWeyl has a precise kill condition",
            "status": "KEEP_CONDITIONAL",
        },
        {
            "row_id": "DEC2530_1_linear_claim",
            "decision": "do not claim B_qWeyl(linear)=0 now",
            "reason": "parent q representation, no-spurion grammar, boundary/readout and regeneration clauses are unsigned",
            "effect": "linear zero remains closure-only",
            "status": "BLOCK_CLAIM",
        },
        {
            "row_id": "DEC2530_2_linear_bound",
            "decision": "do not score finite linear B_qWeyl row",
            "reason": "parent coefficient, q operator, Weyl profile and projections are missing",
            "effect": "finite row remains nonclaim",
            "status": "BLOCK_SCORE",
        },
        {
            "row_id": "DEC2530_3_quadratic",
            "decision": "select quadratic Weyl branch next",
            "reason": "q C^2 and q C*Cdual survive the one-Weyl index theorem",
            "effect": "2531 targets D_qWeyl2 coefficient/operator normalization",
            "status": "SELECTED",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NEXT2530_0_selected",
            "priority": "selected",
            "next_target": "2531-Y5-R2FR-DqWeyl2-parent-coefficient-or-q-operator-normalization-source.md",
            "script": "scripts/Y5_R2FR_DqWeyl2_parent_coefficient_or_q_operator_normalization_source_2531.py",
            "objective": "derive D_qWeyl2=0 from a parent no-higher-curvature/no-regeneration theorem, or source D_qWeyl2, L_q/G_q and P_obs as nonclaim rows",
            "acceptance_gate": "D_qWeyl2 zero theorem or finite coefficient/operator/projection rows are source-backed; otherwise quadratic Weyl remains live and local-GR blocked",
            "do_not": "do not let the linear Weyl index lemma erase quadratic Weyl; do not score placeholders; do not claim local GR/Newton",
        },
        {
            "row_id": "NEXT2530_1_parallel",
            "priority": "parallel_nonclaim",
            "next_target": "2531b-Y5-R2FR-q-representation-no-spurion-adoption-certificate.md",
            "script": "scripts/Y5_R2FR_q_representation_no_spurion_adoption_certificate_2531b.py",
            "objective": "try to parent-sign q representation/no-spurion grammar directly from MTS core",
            "acceptance_gate": "adoption source signs q representation, allowed tensor slots, no projector/spurion, boundary/readout and no-regeneration clauses",
            "do_not": "do not adopt no-spurion by taste",
        },
    ]
    return [stamp(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    copies = [
        ("linear_zero_audit", OUTPUTS["linear_zero_audit"], BRANCH_COPIES["linear_zero_audit"]),
        ("no_spurion_contract", OUTPUTS["no_spurion_contract"], BRANCH_COPIES["no_spurion_contract"]),
        ("linear_bound_row", OUTPUTS["linear_bound_row"], BRANCH_COPIES["linear_bound_row"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    for copy_id, source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            stamp(
                {
                    "copy_id": copy_id,
                    "source_path": str(source.relative_to(ROOT)),
                    "destination_path": str(destination.relative_to(ROOT)),
                    "destination_exists": str(destination.exists()),
                    "status": "COPIED_NONCLAIM",
                }
            )
        )
    return rows


def any_claim_enabled(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    truthy = {"true", "yes", "1", "claim_ready", "score_ready"}
    for rows in rows_by_name.values():
        for row in rows:
            for key, value in row.items():
                if key in {"path_exists", "needle_found", "destination_exists"}:
                    continue
                if key in {"valid_for_claim", "claim_allowed", "allowed", "claim_ready"} and str(value).strip().lower() in truthy:
                    return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    sources = rows_by_name["source_register"]
    checks.append(("VAL2530_00_sources_exist", all(row["path_exists"] == "True" for row in sources), "every required source path exists"))
    checks.append(("VAL2530_01_source_needles", all(row["needle_found"] == "True" for row in sources), "all required source needles found"))
    checks.append(("VAL2530_02_index_lemma_retained", any(row["row_id"] == "LBZ2530_0_metric_trace" and row["status"] == "EXACT_INDEX_LEMMA" for row in rows_by_name["linear_zero_audit"]), "linear index lemma retained"))
    checks.append(("VAL2530_03_linear_not_promoted", any(row["row_id"] == "LBZ2530_4_linear_verdict" and row["status"] == "DEMOTE_TO_CLOSURE_ONLY" for row in rows_by_name["linear_zero_audit"]), "linear BqWeyl zero not promoted"))
    checks.append(("VAL2530_04_no_spurion_unsigned", any(row["row_id"] == "NSC2530_5_verdict" and row["status"] == "CONTRACT_READY_THEOREM_NOT_SIGNED" for row in rows_by_name["no_spurion_contract"]), "no-spurion contract remains unsigned"))
    checks.append(("VAL2530_05_bound_rows_blocked", any(row["row_id"] == "BQB2530_5_acceptance" and row["status"] == "CLAIM_BLOCKED" for row in rows_by_name["linear_bound_row"]), "finite linear BqWeyl row blocked"))
    checks.append(("VAL2530_06_quadratic_selected", any(row["row_id"] == "QWR2530_5_verdict" and row["status"] == "SELECT_NEXT_COEFFICIENT_OR_Q_OPERATOR_TARGET" for row in rows_by_name["quadratic_reentry"]), "quadratic Weyl branch selected"))
    checks.append(("VAL2530_07_claim_gates_blocked", all(row["allowed"] == "False" for row in rows_by_name["claim_gates"]), "all claim gates blocked"))
    checks.append(("VAL2530_08_refusals_cover_shortcuts", len(rows_by_name["refusal_runner"]) >= 5 and all("REJECT" in row["verdict"] for row in rows_by_name["refusal_runner"]), "shortcuts refused"))
    checks.append(("VAL2530_09_next_selected", any(row["row_id"] == "NEXT2530_0_selected" and "DqWeyl2" in row["next_target"] for row in rows_by_name["next_target"]), "DqWeyl2 next target selected"))
    checks.append(("VAL2530_10_no_claim_flags", not any_claim_enabled(rows_by_name), "no generated row enables claim flags"))
    checks.append(("VAL2530_11_branch_copies", all(row["destination_exists"] == "True" for row in rows_by_name["branch_copies"]), "branch copies exist"))
    checks.append(("VAL2530_12_no_formalization_artifacts", not any("formalization-workbench" in str(path).lower() for path in [DOC, *OUTPUTS.values(), *BRANCH_COPIES.values()]), "no outputs target formalization-workbench"))
    checks.append(("VAL2530_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2530_CSV_{path.stem}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2530_CSV_{path.stem}", False, f"{path.name} parse failed: {exc}"))
    for copy_id, path in BRANCH_COPIES.items():
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2530_COPY_CSV_{copy_id}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2530_COPY_CSV_{copy_id}", False, f"{path.name} parse failed: {exc}"))

    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2530_OVERALL",
            overall,
            "2530 keeps the exact one-Weyl index lemma as a conditional lever, refuses to promote linear B_qWeyl without a parent no-spurion grammar, blocks finite linear scoring, and selects quadratic Weyl/D_qWeyl2 next.",
        )
    )
    return [stamp({"check_id": check_id, "status": "PASS" if ok else "FAIL", "details": detail}) for check_id, ok, detail in checks]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def slim(rows: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [{column: row.get(column, "") for column in columns} for row in rows]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2530 - q Representation No-Weyl-Spurion or `B_qWeyl` Bound Row",
                "**Current verdict:** linear `B_qWeyl` has a sharp mathematical kill condition: one Weyl tensor cannot form a scalar source for scalar/quotient `q` with only metric/epsilon contractions. But current MTS does not parent-sign the required q-representation/no-spurion/no-readout-kernel grammar, so the linear zero is closure-only, not a local-GR theorem.",
                "**Main gain:** the dangerous linear Weyl route is no longer vague. Either parent MTS forbids Weyl spurions/projectors/hidden tensors/readout kernels, or it owes a finite `B_qWeyl` row. Even if the linear route closes, quadratic Weyl terms survive and must be attacked next.",
                "**Claim discipline:** no local-GR/Newton/R10/PPN/clock/orbital/GitHub claim is allowed from 2530. This checkpoint only sharpens the Weyl residual hierarchy.",
                "## Source Register",
                markdown_table(
                    slim(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needle_found", "status", "role"]),
                    ["source_id", "source_path", "path_exists", "needle_found", "status", "role"],
                ),
                "## Linear `B_qWeyl` Zero Audit",
                markdown_table(
                    slim(rows_by_name["linear_zero_audit"], ["row_id", "test", "lemma", "status", "claim_scope"]),
                    ["row_id", "test", "lemma", "status", "claim_scope"],
                ),
                "## No-Spurion Contract",
                markdown_table(
                    slim(rows_by_name["no_spurion_contract"], ["row_id", "clause", "needed", "status"]),
                    ["row_id", "clause", "needed", "status"],
                ),
                "## Linear `B_qWeyl` Bound Row Status",
                markdown_table(
                    slim(rows_by_name["linear_bound_row"], ["row_id", "quantity", "status", "units", "needed_for_claim"]),
                    ["row_id", "quantity", "status", "units", "needed_for_claim"],
                ),
                "## Quadratic Weyl Re-Entry",
                markdown_table(
                    slim(rows_by_name["quadratic_reentry"], ["row_id", "object", "status", "why_survives"]),
                    ["row_id", "object", "status", "why_survives"],
                ),
                "## Claim Gates",
                markdown_table(
                    slim(rows_by_name["claim_gates"], ["row_id", "claim", "allowed", "blocked_by"]),
                    ["row_id", "claim", "allowed", "blocked_by"],
                ),
                "## Refusal Runner",
                markdown_table(
                    slim(rows_by_name["refusal_runner"], ["row_id", "shortcut", "verdict", "reason"]),
                    ["row_id", "shortcut", "verdict", "reason"],
                ),
                "## Decision Ledger",
                markdown_table(
                    slim(rows_by_name["decision_ledger"], ["row_id", "decision", "reason", "effect", "status"]),
                    ["row_id", "decision", "reason", "effect", "status"],
                ),
                "## Next Target",
                markdown_table(
                    slim(rows_by_name["next_target"], ["row_id", "priority", "next_target", "script", "objective", "acceptance_gate", "do_not"]),
                    ["row_id", "priority", "next_target", "script", "objective", "acceptance_gate", "do_not"],
                ),
                "## Branch Copies",
                markdown_table(
                    slim(rows_by_name["branch_copies"], ["copy_id", "source_path", "destination_path", "destination_exists", "status"]),
                    ["copy_id", "source_path", "destination_path", "destination_exists", "status"],
                ),
                "## Validation",
                markdown_table(
                    slim(rows_by_name["validation"], ["check_id", "status", "details"]),
                    ["check_id", "status", "details"],
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    remove_pycache()
    rows_by_name: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "linear_zero_audit": linear_zero_rows(),
        "no_spurion_contract": no_spurion_rows(),
        "linear_bound_row": bound_row_rows(),
        "quadratic_reentry": quadratic_rows(),
        "claim_gates": claim_gate_rows(),
        "refusal_runner": refusal_rows(),
        "decision_ledger": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    rows_by_name["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], rows_by_name["branch_copies"])

    rows_by_name["validation"] = validation_rows(rows_by_name)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    remove_pycache()

    print(f"wrote {DOC}")
    for name, path in OUTPUTS.items():
        print(f"wrote {name}: {path}")
    for key, path in BRANCH_COPIES.items():
        print(f"copied {key}: {path}")


if __name__ == "__main__":
    main()
