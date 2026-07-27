from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1855"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1855-Y5-R2FR-minimal-parent-X-sector-action-clause-or-demotion.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_SOURCE_REGISTER.csv",
    "action_clause": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_MINIMAL_PARENT_X_ACTION_CLAUSE.csv",
    "derived_laws": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_DERIVED_LAWS_FROM_CLAUSE.csv",
    "assumption_cost": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_ASSUMPTION_COST_AUDIT.csv",
    "branch_options": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_BRANCH_OPTIONS.csv",
    "demotion_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_CLOSURE_OR_DERIVED_DEMOTION_GATE.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1855_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1855_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1855_0_1854_handoff",
            "source_path": source_path("1854-Y5-R2FR-parent-Hessian-input-extraction-for-ZX-MX2.md"),
            "needle": "NEXT1854_0_primary",
            "use": "selected minimal parent X-sector action clause target",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1855_1_1854_required_clause",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1854_PARENT_ACTION_CLAUSE_REQUIRED.csv"),
            "needle": "PAC1854_1_quadratic_action",
            "use": "required parent action clause rows",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1855_2_1853_normalization",
            "source_path": source_path("1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md"),
            "needle": "rescaling-invariant effective coupling",
            "use": "normalization/range guard",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1855_3_1847_second_variation",
            "source_path": source_path("1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md"),
            "needle": "SV1847_3_range_relation",
            "use": "second-variation/range law precedent",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1855_4_1042_nohair",
            "source_path": source_path("1042-Y5-R10-sourcefree-positive-X-nohair-identity-or-alpha3-prior-first-fill.md"),
            "needle": "positive/source-free no-hair theorem",
            "use": "local GR/no-hair conditional theorem precedent",
            "status": "FOUND",
            "valid_for_claim": False,
        },
    ]

    action_rows = [
        {
            "clause_id": "MXA1855_0_action_header",
            "object": "minimal parent X-sector",
            "clause": "S_parent = S_GR[g] + S_matter[Psi,A_g(Xhat)^2 g,theta] + S_X[g,Xhat,q] + S_boundary",
            "role": "places Xhat inside a covariant parent action rather than as a fitted afterthought",
            "derived_from_current_MTS": False,
            "status": "CANDIDATE_CLOSURE_CLAUSE",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MXA1855_1_field_owner",
            "object": "Xhat",
            "clause": "Xhat is one dimensionless parent normal coordinate or quotient mode with fixed branch_id and forbidden rescalings after declaration.",
            "role": "locks c_g, Z_X, M_X^2, source current and range to one coordinate",
            "derived_from_current_MTS": False,
            "status": "REQUIRED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MXA1855_2_quadratic_block",
            "object": "S_X^(2)",
            "clause": "S_X^(2)=-1/2 int sqrt(-g) M_Pl^2 [Z_X(q) g^{mu nu} partial_mu Xhat partial_nu Xhat + M_X^2(q) Xhat^2] + int sqrt(-g) Xhat J_X",
            "role": "owns Z_X, M_X^2, canonical normalization, range and source current",
            "derived_from_current_MTS": False,
            "status": "REQUIRED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MXA1855_3_GR_branch",
            "object": "GR/Newton limit",
            "clause": "Xhat=0 is a stationary branch with E_X|0=0, J_X=0 or bounded, and S_matter reducing to ordinary metric matter.",
            "role": "makes GR/Newton a limit rather than a loose analogy",
            "derived_from_current_MTS": False,
            "status": "REQUIRED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MXA1855_4_cross_block",
            "object": "mixed Hessian",
            "clause": "delta^2 S_parent has no hidden first-order mixing with metric, coframe, memory, projector or material-marker sectors, or the mixing matrix is retained in the residual vector.",
            "role": "prevents a fake one-field c_g bound",
            "derived_from_current_MTS": False,
            "status": "REQUIRED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MXA1855_5_boundary_domain",
            "object": "boundary/support terms",
            "clause": "S_boundary fixes a self-adjoint local domain and declares Phi_boundary_X=0 or source-bounded in the same normalization.",
            "role": "makes positive no-hair/local GR theorem legal",
            "derived_from_current_MTS": False,
            "status": "REQUIRED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MXA1855_6_coupling_projection",
            "object": "test projections",
            "clause": "A_g, beta_source/test, tau_PPN, tau_R10, tau_WEP and clock/orbital projections are derived from the same Xhat normalization.",
            "role": "connects the field theory to Cassini, R10, WEP, clocks and orbital tests without branch mixing",
            "derived_from_current_MTS": False,
            "status": "REQUIRED_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "clause_id": "MXA1855_7_verdict",
            "object": "minimal clause status",
            "clause": "The clause is internally coherent as a closure contract, but not yet derived from MTS primitives.",
            "role": "separates useful field-theory spine from a claimed derivation",
            "derived_from_current_MTS": False,
            "status": "CLOSURE_CANDIDATE_NOT_MTS_DERIVATION",
            "valid_for_claim": False,
        },
    ]

    derived_law_rows = [
        {
            "law_id": "LAW1855_0_eom",
            "law": "Euler equation",
            "formula": "Z_X Box Xhat - M_X^2 Xhat = -J_X/M_Pl^2 plus declared boundary/domain terms",
            "requires_clause": "MXA1855_2_quadratic_block;MXA1855_5_boundary_domain",
            "status": "DERIVED_FROM_CANDIDATE_CLAUSE",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW1855_1_canonical_field",
            "law": "canonical normalization",
            "formula": "varphi = M_Pl sqrt(Z_X) Xhat and alpha_eff=tau c_g/sqrt(Z_X)",
            "requires_clause": "MXA1855_1_field_owner;MXA1855_2_quadratic_block",
            "status": "DERIVED_FROM_CANDIDATE_CLAUSE",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW1855_2_range",
            "law": "finite range",
            "formula": "lambda_X=sqrt(Z_X/M_X^2)",
            "requires_clause": "MXA1855_2_quadratic_block",
            "status": "DERIVED_FROM_CANDIDATE_CLAUSE",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW1855_3_positive_nohair",
            "law": "source-free positive no-hair",
            "formula": "int_A[Z_X|grad Xhat|^2+M_X^2 Xhat^2]=int_A Xhat J_X+Phi_boundary_X",
            "requires_clause": "Z_X>0;M_X^2>0;J_X=0;Phi_boundary_X=0;no zero mode",
            "status": "CONDITIONAL_THEOREM_AVAILABLE",
            "valid_for_claim": False,
        },
        {
            "law_id": "LAW1855_4_ppn_bound",
            "law": "Cassini/PPN effective bound",
            "formula": "|tau_PPN c_g S_PPN(lambda_X)/sqrt(Z_X)| <= alpha_PPN_proxy",
            "requires_clause": "MXA1855_6_coupling_projection plus range/screening map",
            "status": "CONDITIONAL_TEST_MAP_AVAILABLE",
            "valid_for_claim": False,
        },
    ]

    assumption_rows = [
        {
            "assumption_id": "ASC1855_0_new_degree",
            "assumption": "retain a physical scalar-like Xhat degree of freedom",
            "cost": "adds a potential fifth-force carrier unless source-zero/no-hair closes",
            "can_be_derived_now": False,
            "if_not_derived": "closure assumption",
            "valid_for_claim": False,
        },
        {
            "assumption_id": "ASC1855_1_positive_kinetic",
            "assumption": "Z_X>0",
            "cost": "chooses a healthy scalar branch and excludes ghost/constraint alternatives",
            "can_be_derived_now": False,
            "if_not_derived": "closure assumption or source input",
            "valid_for_claim": False,
        },
        {
            "assumption_id": "ASC1855_2_mass_gap_or_zero_protection",
            "assumption": "M_X^2>0 with range or M_X^2=0 protected by symmetry",
            "cost": "selects whether local tests are R10, PPN/orbital, or screened",
            "can_be_derived_now": False,
            "if_not_derived": "closure assumption or explicit empirical prior",
            "valid_for_claim": False,
        },
        {
            "assumption_id": "ASC1855_3_source_silence",
            "assumption": "ordinary matter source current J_X is zero or bounded",
            "cost": "decides whether local GR is theorem-zero or fifth-force residual",
            "can_be_derived_now": False,
            "if_not_derived": "bounded coupling branch",
            "valid_for_claim": False,
        },
        {
            "assumption_id": "ASC1855_4_projection_universality",
            "assumption": "same Xhat normalization controls PPN, R10, WEP, clock and orbital projections",
            "cost": "forbids branch mixing but requires a real matter/readout functor",
            "can_be_derived_now": False,
            "if_not_derived": "source-by-source empirical closure",
            "valid_for_claim": False,
        },
    ]

    branch_rows = [
        {
            "branch_id": "BRO1855_0_absent_or_constraint_X",
            "branch": "Xhat absent, auxiliary, or pure quotient gauge",
            "local_GR_status": "best for local GR",
            "test_status": "kills fifth-force route but must explain cosmology/galaxy effects elsewhere",
            "current_viability": "OPEN_NOT_DERIVED",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BRO1855_1_positive_sourcefree_X",
            "branch": "physical positive Xhat with J_X=0 and boundary flux zero",
            "local_GR_status": "conditional theorem-zero route",
            "test_status": "R10/PPN pass by no-hair if premises close",
            "current_viability": "PREMISES_UNSIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BRO1855_2_bounded_physical_X",
            "branch": "physical finite/screened Xhat with bounded source coupling",
            "local_GR_status": "not exact GR, but empirically testable residual branch",
            "test_status": "requires Z_X/M_X^2/J_X/tau rows and no-cancellation bounds",
            "current_viability": "SCHEMA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "branch_id": "BRO1855_3_current",
            "branch": "current MTS parent corpus",
            "local_GR_status": "not yet derived",
            "test_status": "source-backed proxies only",
            "current_viability": "CLOSURE_CLAUSE_NOT_DERIVED",
            "valid_for_claim": False,
        },
    ]

    demotion_rows = [
        {
            "gate_id": "DMG1855_0_internal_consistency",
            "test": "candidate clause is internally coherent",
            "result": "PASS_CONDITIONAL",
            "because": "it derives EOM, N_X, lambda_X and the no-hair/test contracts consistently",
            "claim_effect": "may be used as a private closure contract",
            "valid_for_claim": False,
        },
        {
            "gate_id": "DMG1855_1_mts_derivation",
            "test": "candidate clause is derived from MTS primitives",
            "result": "FAIL_CURRENT_CLAIM",
            "because": "no current source derives the physical X-sector action from motion/time/space primitives",
            "claim_effect": "not a public derivation of local GR",
            "valid_for_claim": False,
        },
        {
            "gate_id": "DMG1855_2_demote_if_unsigned",
            "test": "if no primitive derivation arrives",
            "result": "DEMOTE_TO_CLOSURE_ONLY",
            "because": "adding MXA1855 by hand is an EFT closure, not a fundamental derivation",
            "claim_effect": "finite c_g branch can still guide tests but cannot be sold as derived MTS",
            "valid_for_claim": False,
        },
    ]

    claim_rows = [
        {
            "gate_id": "CG1855_0_clause_written",
            "claim": "minimal X-sector closure clause is written",
            "gate_pass": True,
            "reason": "MXA1855 rows define field owner, quadratic block, GR branch, cross-block and projections",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1855_1_clause_derived",
            "claim": "minimal X-sector clause is derived from MTS primitives",
            "gate_pass": False,
            "reason": "no primitive derivation currently exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1855_2_local_GR",
            "claim": "local GR/Newton reduction is derived",
            "gate_pass": False,
            "reason": "candidate closure still needs source-zero/boundary/coupling premises",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1855_3_empirical_scoring",
            "claim": "R10/PPN/WEP/clock/orbital scoring is claim-ready",
            "gate_pass": False,
            "reason": "projection rows remain source-backed proxies until the action clause is derived and parameterized",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1855_0_clause_result",
            "decision": "A minimal parent X-sector clause can be written cleanly.",
            "because": "it derives the needed normalization, range, local no-hair and test-map contracts from one action.",
            "next_action": "try to derive the clause from MTS primitives rather than adopting it by hand",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1855_1_claim_status",
            "decision": "The clause is closure, not a derived MTS result yet.",
            "because": "the existing corpus does not derive Xhat, Z_X, M_X^2, source silence or projections from motion/time/space primitives.",
            "next_action": "keep local-GR and c_g claims blocked",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1855_2_best_next",
            "decision": "Next target should try the primitive derivation.",
            "because": "this is the only route that upgrades the branch from EFT closure to fundamental field theory.",
            "next_action": "1856-Y5-R2FR-derive-X-sector-from-MTS-primitives-or-reject-physical-scalar.md",
            "valid_for_claim": False,
        },
    ]

    next_rows = [
        {
            "route_id": "NEXT1855_0_primary",
            "next_target": "1856-Y5-R2FR-derive-X-sector-from-MTS-primitives-or-reject-physical-scalar.md",
            "script": "scripts/Y5_R2FR_derive_X_sector_from_MTS_primitives_or_reject_physical_scalar_1856.py",
            "objective": "attempt to derive Xhat, Z_X, M_X^2, source silence and projections from motion/time/space primitives; if not possible, reject the physical scalar branch as fundamental and keep it closure-only",
            "selection_status": "selected",
            "success_condition": "either a primitive derivation chain exists, or the finite physical scalar branch is explicitly demoted and a different local-GR route is selected",
        },
        {
            "route_id": "NEXT1855_1_parallel",
            "next_target": "1856b-Y5-R2FR-auxiliary-constraint-X-local-GR-route.md",
            "script": "scripts/Y5_R2FR_auxiliary_constraint_X_local_GR_route_1856b.py",
            "objective": "test the alternative that Xhat is auxiliary/constraint/gauge rather than a physical scalar",
            "selection_status": "held",
            "success_condition": "local GR follows from constraint elimination without introducing a fifth-force scalar",
        },
    ]

    return {
        "source_register": source_rows,
        "action_clause": action_rows,
        "derived_laws": derived_law_rows,
        "assumption_cost": assumption_rows,
        "branch_options": branch_rows,
        "demotion_gate": demotion_rows,
        "claim_gate": claim_rows,
        "decision": decision_rows,
        "next_target": next_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1855_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        if not path.exists():
            missing.append(str(row["source_path"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source paths exist"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all cited source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1855 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1855_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1855_0_sources_exist", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1855_1_needles_present", ok, detail))
    checks.append(
        (
            "VAL1855_2_clause_written",
            any(row["clause_id"] == "MXA1855_2_quadratic_block" for row in rows_map["action_clause"])
            and any(row["clause_id"] == "MXA1855_7_verdict" and row["status"] == "CLOSURE_CANDIDATE_NOT_MTS_DERIVATION" for row in rows_map["action_clause"]),
            "minimal X-sector action clause is written as closure candidate",
        )
    )
    checks.append(
        (
            "VAL1855_3_laws_derive_from_clause",
            all(row["status"] in {"DERIVED_FROM_CANDIDATE_CLAUSE", "CONDITIONAL_THEOREM_AVAILABLE", "CONDITIONAL_TEST_MAP_AVAILABLE"} for row in rows_map["derived_laws"]),
            "EOM, normalization, range and test laws derive conditionally from the clause",
        )
    )
    checks.append(
        (
            "VAL1855_4_assumptions_nonclaim",
            all(not boolish(row["can_be_derived_now"]) and not boolish(row["valid_for_claim"]) for row in rows_map["assumption_cost"]),
            "assumption-cost rows remain nonclaim",
        )
    )
    checks.append(
        (
            "VAL1855_5_demotion_gate",
            any(row["gate_id"] == "DMG1855_1_mts_derivation" and row["result"] == "FAIL_CURRENT_CLAIM" for row in rows_map["demotion_gate"])
            and any(row["gate_id"] == "DMG1855_2_demote_if_unsigned" and row["result"] == "DEMOTE_TO_CLOSURE_ONLY" for row in rows_map["demotion_gate"]),
            "demotion gate blocks derived-MTS claim",
        )
    )
    checks.append(
        (
            "VAL1855_6_claim_gates_safe",
            any(row["gate_id"] == "CG1855_0_clause_written" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1855_1_clause_derived" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "clause-written gate passes but derived/local claims do not",
        )
    )
    checks.append(
        (
            "VAL1855_7_next_target_selected",
            any(row["route_id"] == "NEXT1855_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        )
    )
    checks.append(
        (
            "VAL1855_8_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1855_9_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1855_10_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1855_11_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs = list(FORMALIZATION.rglob("*1855*")) if FORMALIZATION.exists() else []
    checks.append(("VAL1855_12_formalization_untouched", not formalization_outputs, "no 1855 outputs found under formalization-workbench"))
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1855_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1855 minimal parent X-sector action clause or demotion",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1855: Minimal Parent X-Sector Action Clause Or Demotion",
            "",
            "**Current verdict:** the minimal parent `Xhat` action clause can be written cleanly and it derives the needed equations, normalization, range, no-hair contract and test projections. But it is not yet derived from MTS primitives. So it is a private closure candidate, not a local-GR or `c_g` claim.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_path", "needle", "use", "status", "valid_for_claim"]),
            "",
            "## Minimal Parent X Action Clause",
            markdown_table(rows_map["action_clause"], ["clause_id", "object", "clause", "role", "derived_from_current_MTS", "status", "valid_for_claim"]),
            "",
            "## Derived Laws From Clause",
            markdown_table(rows_map["derived_laws"], ["law_id", "law", "formula", "requires_clause", "status", "valid_for_claim"]),
            "",
            "## Assumption Cost Audit",
            markdown_table(rows_map["assumption_cost"], ["assumption_id", "assumption", "cost", "can_be_derived_now", "if_not_derived", "valid_for_claim"]),
            "",
            "## Branch Options",
            markdown_table(rows_map["branch_options"], ["branch_id", "branch", "local_GR_status", "test_status", "current_viability", "valid_for_claim"]),
            "",
            "## Closure Or Derived Demotion Gate",
            markdown_table(rows_map["demotion_gate"], ["gate_id", "test", "result", "because", "claim_effect", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the fork in the road. The scalar branch is now well-formed as field theory, but well-formed is not the same as derived. To make MTS serious as a fundamental theory, the next step must derive this X-sector from motion/time/space primitives or reject it as only an EFT closure.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1855 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
