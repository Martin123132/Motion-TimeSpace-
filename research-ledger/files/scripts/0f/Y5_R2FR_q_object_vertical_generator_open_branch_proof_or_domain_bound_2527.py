from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BRANCH_ID = "MTS_R2FR_Q_OBJECT_VERTICAL_GENERATOR_REENTRY_2527"
CHECKPOINT_ID = "2527"
DOC = ROOT / "2527-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md"
MTS_RESIDUALS = ROOT / "source-intake" / "mts_residuals"

OUTPUTS = {
    "source_register": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_SOURCE_REGISTER.csv",
    "open_branch_audit": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_Q_VERTICAL_OPEN_BRANCH_REENTRY_AUDIT.csv",
    "kernel_gate": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_DQ_KERNEL_GATE_MATRIX.csv",
    "domain_bound_rows": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_DQ_DOMAIN_BOUND_ROWS.csv",
    "claim_gates": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_CLAIM_GATES.csv",
    "refusal_runner": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_REFUSAL_RUNNER.csv",
    "decision_ledger": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_DECISION_LEDGER.csv",
    "next_target": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_NEXT_TARGET.csv",
    "branch_copies": MTS_RESIDUALS / "P8_Y5_NO_SHADOW_2527_BRANCH_COPIES.csv",
    "validation": MTS_RESIDUALS / "P8_Y5_BRR545_2527_VALIDATION.csv",
}

BRANCH_COPIES = {
    "open_branch_audit": ROOT
    / "source-intake"
    / "beta-source"
    / "docs"
    / "Q_vertical_open_branch_reentry_2527_NONCLAIM.csv",
    "kernel_gate": ROOT
    / "source-intake"
    / "local_bounds"
    / "Dq_vertical_kernel_gate_2527_NONCLAIM.csv",
    "domain_bound_rows": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "DQ2527_DOMAIN_BOUND_ROWS_NONCLAIM.csv",
    "next_target": ROOT
    / "source-intake"
    / "rab-sector"
    / "acquisition-queue"
    / "DQ2527_NEXT_TARGET_NONCLAIM.csv",
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
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


SOURCE_SPECS = [
    {
        "source_id": "SRC2527_0_2526_doc",
        "source_path": "2526-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md",
        "needle": "NEXT2526_0_selected",
        "role": "immediate handoff selecting q-object / vertical-generator proof",
    },
    {
        "source_id": "SRC2527_1_2526_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2526_VALIDATION.csv",
        "needle": "VAL2526_OVERALL,PASS",
        "role": "2526 validation anchor",
    },
    {
        "source_id": "SRC2527_2_2526_signing",
        "source_path": "source-intake/mts_residuals/P8_Y5_NO_SHADOW_2526_ACTION_SIGNING_TESTS.csv",
        "needle": "AST2526_0_q_object",
        "role": "q and verticality remain unsigned after matter coupling",
    },
    {
        "source_id": "SRC2527_3_2358_doc",
        "source_path": "2358-Y5-R2FR-q-object-vertical-generator-open-branch-proof-or-domain-bound.md",
        "needle": "Q_OBJECT_NOT_PARENT_SIGNED",
        "role": "prior q/v proof attempt and failure mode",
    },
    {
        "source_id": "SRC2527_4_2358_validation",
        "source_path": "source-intake/mts_residuals/P8_Y5_BRR545_2358_VALIDATION.csv",
        "needle": "VAL2358_OVERALL,PASS",
        "role": "2358 validation anchor",
    },
    {
        "source_id": "SRC2527_5_2358_audit",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2358_Q_VERTICAL_OPEN_BRANCH_AUDIT.csv",
        "needle": "QVA2358_2_q_map",
        "role": "q object and vertical basis audit rows",
    },
    {
        "source_id": "SRC2527_6_2358_kernel",
        "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_2358_DQ_KERNEL_GATE_MATRIX.csv",
        "needle": "DQM2358_5_kernel_total",
        "role": "Dq kernel gate precedent",
    },
    {
        "source_id": "SRC2527_7_2356_doc",
        "source_path": "2356-Y5-R2FR-parent-source-current-descent-or-domain-motion-bound.md",
        "needle": "PDC2356_0_parent_q_object",
        "role": "source-current descent clauses requiring q and verticality",
    },
    {
        "source_id": "SRC2527_8_2223_doc",
        "source_path": "2223-Y5-R2FR-quotient-map-vertical-generator-frontier-import-or-finite-coupling-row.md",
        "needle": "Exact source silence does not close",
        "role": "older q/Dq frontier import and finite fallback",
    },
    {
        "source_id": "SRC2527_9_1541_doc",
        "source_path": "1541-Y5-quotient-map-vertical-generator-kernel-certificate.md",
        "needle": "Dq",
        "role": "earlier q-map vertical-generator certificate attempt",
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


def open_branch_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "QVA2527_0_parent_field_chart",
            "clause": "parent field chart",
            "required_statement": "there is an open parent branch U with field coordinates Phi^I and smooth transition rules",
            "proof_attempt": "needed before q can be a differentiable map rather than a label on variables",
            "current_evidence": "2358 and 2223 name the need but do not parent-sign the chart",
            "status": "PARENT_CHART_NOT_SIGNED",
            "blocks_claim": "True",
        },
        {
            "row_id": "QVA2527_1_equivalence_relation",
            "clause": "visible-state equivalence relation",
            "required_statement": "Phi ~ Phi' iff every visible/ordinary-matter stack component agrees",
            "proof_attempt": "must be parent-defined before any quotient map q exists",
            "current_evidence": "MCA2526 uses q(Phi), but does not derive the equivalence relation",
            "status": "EQUIVALENCE_RELATION_NOT_SIGNED",
            "blocks_claim": "True",
        },
        {
            "row_id": "QVA2527_2_q_map",
            "clause": "parent quotient map",
            "required_statement": "q: U -> Q_vis is smooth and maps parent fields to quotient-owned observed data",
            "proof_attempt": "candidate q is exactly the map needed by MCA2526 and source-current descent",
            "current_evidence": "uses q but no source gives q's component formula and target space",
            "status": "Q_OBJECT_NOT_PARENT_SIGNED",
            "blocks_claim": "True",
        },
        {
            "row_id": "QVA2527_3_constant_rank_open_branch",
            "clause": "submersion / constant-rank condition",
            "required_statement": "rank Dq is constant on an open local branch, so ker(Dq) is a smooth vertical bundle",
            "proof_attempt": "without constant rank, a one-point kernel identity is not a local theorem",
            "current_evidence": "no Dq matrix/rank certificate exists for the current MTS parent variables",
            "status": "OPEN_BRANCH_RANK_NOT_SIGNED",
            "blocks_claim": "True",
        },
        {
            "row_id": "QVA2527_4_vertical_basis",
            "clause": "vertical generator basis",
            "required_statement": "there are smooth basis fields v_a spanning ker(Dq) on U",
            "proof_attempt": "verticality must be a tangent-to-fibres statement, not a name given to a residual",
            "current_evidence": "2358 retains Dq kernel rows because the basis is not parent-signed",
            "status": "VERTICAL_BASIS_NOT_SIGNED",
            "blocks_claim": "True",
        },
        {
            "row_id": "QVA2527_5_local_generator_decomposition",
            "clause": "local residual generator decomposition",
            "required_statement": "X_loc = c^a v_a + EOM + boundary/support terms on U",
            "proof_attempt": "only then does Dq[X_loc]=0 modulo owned EOM/boundary pieces",
            "current_evidence": "no source decomposes the physical local generator into the q-vertical basis",
            "status": "LOCAL_GENERATOR_DECOMPOSITION_NOT_SIGNED",
            "blocks_claim": "True",
        },
        {
            "row_id": "QVA2527_6_kernel_conclusion",
            "clause": "open-branch kernel theorem",
            "required_statement": "Dq[X_loc]=0 throughout U, not only at a point or in a chosen representative",
            "proof_attempt": "would close AST2526_0 and AST2526_1 and activate the coupling theorem",
            "current_evidence": "antecedents QVA2527_0..5 are unsigned",
            "status": "KERNEL_THEOREM_NOT_PROMOTED",
            "blocks_claim": "True",
        },
    ]
    return [stamp(row) for row in rows]


def kernel_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DQM2527_0_q_component_formula",
            "object": "q^A(Phi)",
            "zero_condition": "component formulas are parent-derived and differentiable",
            "current_status": "MISSING_Q_COMPONENT_FORMULA",
            "finite_fallback": "record q_component_source and q_component_uncertainty before scoring",
            "claim_ready": "False",
        },
        {
            "row_id": "DQM2527_1_Dq_matrix",
            "object": "partial q^A / partial Phi^I",
            "zero_condition": "Dq matrix exists on U and has constant rank",
            "current_status": "MISSING_DQ_MATRIX_AND_RANK_CERTIFICATE",
            "finite_fallback": "epsilon_Dq_rank_or_projection_leak",
            "claim_ready": "False",
        },
        {
            "row_id": "DQM2527_2_vertical_basis_matrix",
            "object": "v_a^I",
            "zero_condition": "basis spans ker(Dq) on U",
            "current_status": "MISSING_VERTICAL_BASIS_SOURCE",
            "finite_fallback": "basis_completeness_defect",
            "claim_ready": "False",
        },
        {
            "row_id": "DQM2527_3_kernel_product",
            "object": "Dq_A_I v_a^I",
            "zero_condition": "all Dq[v_a] vanish as symbolic identities on U",
            "current_status": "KERNEL_PRODUCT_UNSIGNED",
            "finite_fallback": "max_a ||Dq[v_a]||_Q / ||v_a||_F",
            "claim_ready": "False",
        },
        {
            "row_id": "DQM2527_4_local_generator_projection",
            "object": "Dq[X_loc]",
            "zero_condition": "X_loc lies in span{v_a}+EOM+boundary with bounded support terms",
            "current_status": "LOCAL_GENERATOR_PROJECTION_UNSIGNED",
            "finite_fallback": "epsilon_Dq_Xloc_abs",
            "claim_ready": "False",
        },
        {
            "row_id": "DQM2527_5_kernel_total",
            "object": "open-branch Dq kernel gate",
            "zero_condition": "DQM2527_0..4 close on the same branch and norm",
            "current_status": "Dq_KERNEL_UNSIGNED_RETAIN_BOUND_ROWS",
            "finite_fallback": "Dq_vertical_leak_total",
            "claim_ready": "False",
        },
    ]
    return [stamp(row) for row in rows]


def domain_bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DQB2527_0_Dq_vertical_leak_total",
            "quantity": "epsilon_Dq_vertical_total",
            "definition": "max_a ||Dq[v_a]||_Q / ||v_a||_F on the selected open branch",
            "required_inputs": "q_component_formula;Dq_matrix;vertical_basis;Q_norm;F_norm;open_branch_domain",
            "units": "dimensionless after norm declaration",
            "status": "MISSING_COMPONENT_VALUES",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DQB2527_1_Xloc_projection_leak",
            "quantity": "epsilon_Dq_Xloc_abs",
            "definition": "||Dq[X_loc]||_Q / ||X_loc||_F including owned EOM and boundary remainder contract",
            "required_inputs": "Xloc_formula;generator_decomposition;Dq_matrix;boundary_remainder_bound",
            "units": "dimensionless after norm declaration",
            "status": "MISSING_XLOC_FORMULA_AND_PROJECTION",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DQB2527_2_rank_defect",
            "quantity": "epsilon_rank_branch",
            "definition": "measure of constant-rank failure or singular-set proximity on U",
            "required_inputs": "rank_Dq;domain_U;singular_set_distance;regularity_class",
            "units": "dimensionless or declared chart units",
            "status": "MISSING_RANK_CERTIFICATE",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DQB2527_3_domain_current_bound",
            "quantity": "J_domain_Dq_abs",
            "definition": "K_Dq * epsilon_Dq_Xloc_abs * A_source * S_link / M_H_ref",
            "required_inputs": "K_Dq;epsilon_Dq_Xloc_abs;A_source;S_link;M_H_ref",
            "units": "dimensionless only after M_H_ref and source norm are parent-signed",
            "status": "MISSING_DQ_AND_SOURCE_NORMALIZATION_INPUTS",
            "valid_for_claim": "False",
        },
        {
            "row_id": "DQB2527_4_arena_projection",
            "quantity": "arena Dq leak rows",
            "definition": "R10/PPN/clock/orbital projections of the same Dq leak quantity",
            "required_inputs": "arena_projectors;units;source_path;row_id;validity_flags",
            "units": "arena-specific",
            "status": "MISSING_ARENA_PROJECTIONS",
            "valid_for_claim": "False",
        },
    ]
    return [stamp(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CG2527_0_q_object",
            "claim": "parent q object exists before matter/readout",
            "allowed": "False",
            "blocked_by": "QVA2527_0_parent_field_chart;QVA2527_1_equivalence_relation;QVA2527_2_q_map",
        },
        {
            "row_id": "CG2527_1_vertical_generator",
            "claim": "local generator is in ker(Dq) on an open branch",
            "allowed": "False",
            "blocked_by": "QVA2527_3_constant_rank_open_branch;QVA2527_4_vertical_basis;QVA2527_5_local_generator_decomposition",
        },
        {
            "row_id": "CG2527_2_source_current_descent",
            "claim": "MCA2526 coupling theorem fires for current MTS",
            "allowed": "False",
            "blocked_by": "CG2527_0_q_object;CG2527_1_vertical_generator;MCA2526_adoption_missing",
        },
        {
            "row_id": "CG2527_3_local_GR_Newton",
            "claim": "local GR/Newton branch derived",
            "allowed": "False",
            "blocked_by": "CG2527_2_source_current_descent;M_H_ref;boundary_support;domain_motion_rows",
        },
        {
            "row_id": "CG2527_4_public_or_github",
            "claim": "public claim or GitHub update recommended from 2527",
            "allowed": "False",
            "blocked_by": "all q/Dq rows nonclaim",
        },
    ]
    return [stamp(row) for row in rows]


def refusal_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "REF2527_0_q_by_name",
            "shortcut": "declare q because the matter action uses q(Phi)",
            "verdict": "REJECT",
            "reason": "using q in MCA2526 is not a parent construction of q",
            "required_repair": "field chart, equivalence relation, target space and component formulas",
        },
        {
            "row_id": "REF2527_1_vertical_by_label",
            "shortcut": "call X_loc vertical because it is hidden/local",
            "verdict": "REJECT",
            "reason": "vertical means tangent to fibres of q: Dq[X_loc]=0 on an open branch",
            "required_repair": "Dq matrix and generator decomposition",
        },
        {
            "row_id": "REF2527_2_point_kernel",
            "shortcut": "prove Dq[v]=0 at one point or one representative",
            "verdict": "REJECT",
            "reason": "source-current descent requires an open-branch theorem, not a point identity",
            "required_repair": "constant-rank certificate and open-domain statement",
        },
        {
            "row_id": "REF2527_3_no_pole_selector_as_q",
            "shortcut": "use no-pole/no-shadow selector as the quotient map without a smooth quotient construction",
            "verdict": "REJECT_AS_CURRENT_PROOF",
            "reason": "it may become a route, but it must define the same q target and Dq kernel",
            "required_repair": "convert selector into a field chart/equivalence relation or keep it as a finite selector leak",
        },
        {
            "row_id": "REF2527_4_observed_stack_backfill",
            "shortcut": "define q by observed GR/Newton variables already known to work",
            "verdict": "REJECT",
            "reason": "that imports the desired local limit instead of deriving it",
            "required_repair": "parent-owned construction before fitting/readout",
        },
    ]
    return [stamp(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "DEC2527_0_theorem_shape",
            "decision": "retain exact q-vertical theorem contract",
            "reason": "if q is a constant-rank parent quotient and X_loc is tangent to q-fibres, source-current descent becomes a real theorem instead of an axiom",
            "next_action": "prove the parent field chart/equivalence relation or demote to finite Dq leak rows",
            "status": "ACTIVE",
        },
        {
            "row_id": "DEC2527_1_no_promotion",
            "decision": "do not claim q/v closure",
            "reason": "current evidence still lacks q component formulas, Dq matrix, rank certificate, and local generator decomposition",
            "next_action": "keep CG2527 gates false",
            "status": "BLOCK_CLAIM",
        },
        {
            "row_id": "DEC2527_2_selected_route",
            "decision": "select parent field-chart/equivalence construction next",
            "reason": "that is the upstream missing object; another coupling ansatz cannot create q after the fact",
            "next_action": "2528 field-chart/equivalence relation or no-pole selector conversion",
            "status": "SELECTED",
        },
        {
            "row_id": "DEC2527_3_fallback",
            "decision": "preserve finite Dq/domain rows",
            "reason": "if the quotient cannot be derived, the theory must pay a measurable residual rather than hide the leak",
            "next_action": "source DQB2527 rows with units and arena projections",
            "status": "HELD_PARALLEL",
        },
    ]
    return [stamp(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NEXT2527_0_selected",
            "priority": "selected",
            "next_target": "2528-Y5-R2FR-parent-q-field-chart-equivalence-relation-or-no-pole-selector.md",
            "script": "scripts/Y5_R2FR_parent_q_field_chart_equivalence_relation_or_no_pole_selector_2528.py",
            "objective": "construct a parent field chart and equivalence relation that makes q a smooth constant-rank quotient, or convert the no-pole/no-shadow selector into an explicit finite selector leak",
            "acceptance_gate": "q target, component formulas, Dq matrix, rank certificate, and equivalence relation are all parent-signed on one open branch, otherwise no q/v claim",
            "do_not": "do not define q by observed GR variables; do not use one-point verticality; do not claim local GR/Newton",
        },
        {
            "row_id": "NEXT2527_1_fallback",
            "priority": "fallback_nonclaim",
            "next_target": "2528b-Y5-R2FR-Dq-domain-bound-input-pack.md",
            "script": "scripts/Y5_R2FR_Dq_domain_bound_input_pack_2528b.py",
            "objective": "source every finite Dq/domain leak input with units, norms, and arena projections",
            "acceptance_gate": "all DQB2527 rows have numeric values or remain explicitly blocked nonclaim",
            "do_not": "do not score missing Dq rows or use placeholders as local-GR evidence",
        },
        {
            "row_id": "NEXT2527_2_later",
            "priority": "queued_after_q_route",
            "next_target": "2529-Y5-R2FR-fibre-Bh-finite-row-or-hidden-visible-grammar-reentry.md",
            "script": "scripts/Y5_R2FR_fibre_Bh_finite_row_or_hidden_visible_grammar_reentry_2529.py",
            "objective": "return to the fibre B_h residual after the q/source-current lane is narrowed",
            "acceptance_gate": "B_h is theorem-zero or finite nonclaim rows are sourced",
            "do_not": "do not erase independent fibre residuals with the matter-coupling contract",
        },
    ]
    return [stamp(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("open_branch_audit", OUTPUTS["open_branch_audit"], BRANCH_COPIES["open_branch_audit"]),
        ("kernel_gate", OUTPUTS["kernel_gate"], BRANCH_COPIES["kernel_gate"]),
        ("domain_bound_rows", OUTPUTS["domain_bound_rows"], BRANCH_COPIES["domain_bound_rows"]),
        ("next_target", OUTPUTS["next_target"], BRANCH_COPIES["next_target"]),
    ]
    rows: list[dict[str, Any]] = []
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
                if key in {"valid_for_claim", "claim_allowed", "claim_ready", "allowed"} and str(value).strip().lower() in truthy:
                    return True
    return False


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    source_rows = rows_by_name["source_register"]
    checks.append(("VAL2527_00_sources_exist", all(row["path_exists"] == "True" for row in source_rows), "every required source path exists"))
    checks.append(("VAL2527_01_source_needles", all(row["needle_found"] == "True" for row in source_rows), "required source needles found"))
    checks.append(("VAL2527_02_open_branch_blockers", all(row["blocks_claim"] == "True" for row in rows_by_name["open_branch_audit"]), "q/v open branch clauses remain honest blockers"))
    checks.append(("VAL2527_03_q_and_verticality_unsigned", any(row["status"] == "Q_OBJECT_NOT_PARENT_SIGNED" for row in rows_by_name["open_branch_audit"]) and any(row["status"] == "VERTICAL_BASIS_NOT_SIGNED" for row in rows_by_name["open_branch_audit"]), "q object and vertical basis are explicitly unsigned"))
    checks.append(("VAL2527_04_kernel_gate_nonclaim", all(row["claim_ready"] == "False" for row in rows_by_name["kernel_gate"]), "Dq kernel matrix rows remain nonclaim"))
    checks.append(("VAL2527_05_bound_rows_nonclaim", all(row["valid_for_claim"] == "False" for row in rows_by_name["domain_bound_rows"]), "finite Dq/domain rows remain nonclaim"))
    checks.append(("VAL2527_06_claim_gates_blocked", all(row["allowed"] == "False" for row in rows_by_name["claim_gates"]), "all claim gates blocked"))
    checks.append(("VAL2527_07_refusals_cover_shortcuts", len(rows_by_name["refusal_runner"]) >= 5 and all("REJECT" in row["verdict"] for row in rows_by_name["refusal_runner"]), "shortcuts refused"))
    checks.append(("VAL2527_08_next_selected", any(row["row_id"] == "NEXT2527_0_selected" and "field-chart" in row["next_target"] for row in rows_by_name["next_target"]), "field-chart/equivalence target selected"))
    checks.append(("VAL2527_09_no_claim_flags", not any_claim_enabled(rows_by_name), "no generated row enables claim flags"))
    checks.append(("VAL2527_10_branch_copies", all(row["destination_exists"] == "True" for row in rows_by_name["branch_copies"]), "branch copies exist"))
    checks.append(("VAL2527_11_no_formalization_artifacts", not any("formalization-workbench" in str(path).lower() for path in [*OUTPUTS.values(), *BRANCH_COPIES.values(), DOC]), "no outputs target formalization-workbench"))
    checks.append(("VAL2527_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))

    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2527_CSV_{path.stem}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2527_CSV_{path.stem}", False, f"{path.name} parse failed: {exc}"))
    for copy_id, path in BRANCH_COPIES.items():
        try:
            parsed = csv_rows(path)
            checks.append((f"VAL2527_COPY_CSV_{copy_id}", len(parsed) > 0, f"{path.name} parses"))
        except Exception as exc:
            checks.append((f"VAL2527_COPY_CSV_{copy_id}", False, f"{path.name} parse failed: {exc}"))

    overall = all(ok for _, ok, _ in checks)
    checks.append(
        (
            "VAL2527_OVERALL",
            overall,
            "2527 imports the prior q/v failure, writes the exact open-branch quotient theorem contract, keeps Dq/domain rows nonclaim, and selects parent field-chart/equivalence construction next.",
        )
    )
    return [
        stamp(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "details": detail,
            }
        )
        for check_id, ok, detail in checks
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")) for column in columns) + " |")
    return "\n".join(output)


def slim(rows: list[dict[str, Any]], columns: list[str]) -> list[dict[str, Any]]:
    return [{column: row.get(column, "") for column in columns} for row in rows]


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 2527 - `q` Object / Vertical Generator Open-Branch Proof or Domain Bound",
                "**Current verdict:** the matter-coupling contract from 2526 does not create `q`; it only says what happens if `q` already exists. The open-branch proof still fails under current evidence because the parent field chart, equivalence relation, smooth quotient map, constant-rank `Dq`, vertical basis, and local-generator decomposition are not jointly parent-signed.",
                "**Main gain:** this narrows the missing geometry to one exact theorem contract: on an open branch `U`, construct `q: U -> Q_vis` as a constant-rank quotient and prove `X_loc in ker(Dq)` modulo owned EOM/boundary terms. If that cannot be done, the theory owes finite `Dq_vertical_leak` / domain-motion rows.",
                "**Claim discipline:** no local-GR, Newton, PPN, R10, clock, orbital, GitHub, or public claim is allowed from 2527. This is a private proof gate and residual ledger.",
                "## Source Register",
                markdown_table(
                    slim(rows_by_name["source_register"], ["source_id", "source_path", "path_exists", "needle_found", "status", "role"]),
                    ["source_id", "source_path", "path_exists", "needle_found", "status", "role"],
                ),
                "## Open-Branch `q` / Verticality Audit",
                markdown_table(
                    slim(rows_by_name["open_branch_audit"], ["row_id", "clause", "required_statement", "proof_attempt", "current_evidence", "status", "blocks_claim"]),
                    ["row_id", "clause", "required_statement", "proof_attempt", "current_evidence", "status", "blocks_claim"],
                ),
                "## `Dq` Kernel Gate Matrix",
                markdown_table(
                    slim(rows_by_name["kernel_gate"], ["row_id", "object", "zero_condition", "current_status", "finite_fallback", "claim_ready"]),
                    ["row_id", "object", "zero_condition", "current_status", "finite_fallback", "claim_ready"],
                ),
                "## Finite Domain Bound Rows",
                markdown_table(
                    slim(rows_by_name["domain_bound_rows"], ["row_id", "quantity", "definition", "required_inputs", "units", "status", "valid_for_claim"]),
                    ["row_id", "quantity", "definition", "required_inputs", "units", "status", "valid_for_claim"],
                ),
                "## Claim Gates",
                markdown_table(
                    slim(rows_by_name["claim_gates"], ["row_id", "claim", "allowed", "blocked_by"]),
                    ["row_id", "claim", "allowed", "blocked_by"],
                ),
                "## Refusal Runner",
                markdown_table(
                    slim(rows_by_name["refusal_runner"], ["row_id", "shortcut", "verdict", "reason", "required_repair"]),
                    ["row_id", "shortcut", "verdict", "reason", "required_repair"],
                ),
                "## Decision Ledger",
                markdown_table(
                    slim(rows_by_name["decision_ledger"], ["row_id", "decision", "reason", "next_action", "status"]),
                    ["row_id", "decision", "reason", "next_action", "status"],
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
        "open_branch_audit": open_branch_audit_rows(),
        "kernel_gate": kernel_gate_rows(),
        "domain_bound_rows": domain_bound_rows(),
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
