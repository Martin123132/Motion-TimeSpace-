from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2029-Y5-R2FR-source-SZ-normal-form-and-local-profile-pack.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"


def formalization_has_2029_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    try:
        return any(FORMALIZATION.rglob("*2029*SZ*")) or any(FORMALIZATION.rglob("*2029*profile*"))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        (
            "SRC2029_00_2028_handoff",
            ROOT / "2028-Y5-R2FR-vZ-local-vacuum-double-zero-or-finite-jZB-bound.md",
            ["NEXT2028_0_2029", "VDZ2028_7_verdict", "VAL2028_OVERALL"],
            "2028 handoff selects S_Z normal form and local profile pack.",
        ),
        (
            "SRC2029_01_2028_obligations",
            OUT / "P8_Y5_PARENT_QLOC_2028_PROOF_OBLIGATIONS.csv",
            ["OBL2028_0_SZ_source", "OBL2028_5_mZ2", "OBL2028_8_profile"],
            "machine-readable missing S_Z/gap/profile obligations.",
        ),
        (
            "SRC2029_02_1747_gap",
            ROOT / "1747-Y5-R2FR-canonical-gap-coupling-source-silence-or-wall-bound-row.md",
            ["CPG1747_1_gap", "GAS1747_0_mu_m2", "VAL1747_OVERALL"],
            "canonical gap/amplitude source package remains missing.",
        ),
        (
            "SRC2029_03_1861_evenness",
            ROOT / "1861-Y5-R2FR-source-functional-evenness-JZ-BZ-coupling-lock-or-profile-acquisition.md",
            ["SFE1861_1_exchange_evenness_condition", "JBC1861_0_bulk_JZ", "QI1861_0_formal_double_zero"],
            "exchange-even source theorem and J_Z/B_Z finite fallback.",
        ),
        (
            "SRC2029_04_1858_constraint",
            ROOT / "1858-Y5-R2FR-parent-constraint-package-no-GR-import-gate.md",
            ["PCP1858_2_generator_or_auxiliary_solve", "ORG1858_4_second_class_auxiliary", "VAL1858_OVERALL"],
            "constraint/auxiliary route is live but parent package is unsigned.",
        ),
        (
            "SRC2029_05_1868_grammar",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_CANDIDATE_PARENT_GRAMMAR.csv",
            ["CPG1868_3_derivative_permission", "CPG1868_4_constraint_admission"],
            "typed parent grammar can forbid standalone reciprocal scalar dynamics if signed.",
        ),
        (
            "SRC2029_06_1868_legality",
            ROOT / "source-intake" / "microscope" / "quarantine" / "1868" / "P8_Y5_PARENT_QLOC_1868_TERM_LEGALITY_MATRIX.csv",
            ["TLM1868_0_ZR_kinetic", "TLM1868_1_MR2_potential"],
            "dangerous kinetic/potential terms are legal countermodels unless grammar is signed.",
        ),
        (
            "SRC2029_07_Cperp_quotient_skeleton",
            ROOT / "runs" / "20260601-000089-parent-no-Cperp-action-or-closure" / "results" / "quotient_action_skeleton.csv",
            ["configuration_space", "memory_class", "matter_metric"],
            "quotient action skeleton omits raw representative Cperp from physical action.",
        ),
        (
            "SRC2029_08_Cperp_constraint_algebra",
            ROOT / "runs" / "20260601-000088-Cperp-residual-shift-constraint-attempt" / "results" / "constraint_algebra.csv",
            ["candidate_generator", "Hamiltonian_bracket", "preservation_condition"],
            "residual-shift constraint algebra condition for no physical representative.",
        ),
        (
            "SRC2029_09_1937_hilbert_source",
            ROOT / "1937-Y5-R2FR-parent-Hilbert-source-coupling-signature-or-nonmetric-source-coefficient-ledger.md",
            ["HST1937_0_variational_source_owner", "CG1937_2_parent_derivation", "VAL1937_OVERALL"],
            "minimal Hilbert source signature candidate and nonmetric-source blocker.",
        ),
    ]
    rows = []
    for source_id, path, needles, note in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        ok = exists and all(needle in text for needle in needles)
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "status": "EXISTS_NEEDLES_CONFIRMED" if ok else "MISSING_OR_NEEDLE_FAIL",
                "needles": ";".join(needles),
                "note": note,
            }
        )
        rows.append(row)
    return rows


def route_sort_rows() -> list[dict[str, object]]:
    data = [
        (
            "SZR2029_0_canonical_finite_field",
            "canonical finite Z field",
            "S_Z=int sqrt(-g_obs)[-1/2 K(Z)(nabla Z)^2 - V(Z)] + S_boundary",
            "USES_2028_DOUBLE_ZERO_THEOREM",
            "scientifically honest if Z is physical; must source K0,V0,Vprime0,mZ2,A_Z,Q_Z",
            "not source-backed; generic bulk Z gravitates if double-zero fails",
            "candidate only",
        ),
        (
            "SZR2029_1_quotient_representative",
            "quotient representative/no raw Z action",
            "S_parent=S_red[q(Phi)] + topological/exact pieces; raw representative Z appears only as gauge/choice data",
            "EXACT_IF_QUOTIENT_AXIOM_DERIVED",
            "cleanest local-GR silence if MTS object-language really makes Z nonphysical",
            "quotient axiom and matter/readout descent are unsigned",
            "best exact route if parent grammar can be derived",
        ),
        (
            "SZR2029_2_constraint_auxiliary",
            "constraint or algebraic auxiliary elimination",
            "S_Z=int Lambda_Z C_Z[B,U] or algebraic auxiliary block; E_Lambda=0 and E_Z solve/remove Z before readout",
            "EXACT_IF_CONSTRAINT_PACKAGE_SIGNED",
            "less vulnerable to fifth-force criticism than a propagating scalar when no physical local Z mode is intended",
            "generator/auxiliary solve, boundary, matter descent and degree count remain unsigned",
            "best fallback exact route",
        ),
        (
            "SZR2029_3_topological_exact",
            "topological/exact boundary sector",
            "S_Z=dB_Z or metric-independent topological class with Q_Z=0/proper/exact on local branch",
            "EXACT_IF_BOUNDARY_CERTIFIED",
            "kills J_B^Z without tuning a potential",
            "no parent topological/exact certificate",
            "held as special case of quotient/constraint",
        ),
        (
            "SZR2029_4_finite_residual",
            "finite residual profile",
            "retain J_B^Z,C_ZB,A_Z,ell_Z,Q_Z,source-slot and tau/readout coefficients as source-backed nonclaim rows",
            "TESTABLE_IF_SOURCED",
            "keeps the theory empirical if exact local-GR derivation fails",
            "no numeric/source-backed rows yet",
            "fallback testing route",
        ),
        (
            "SZR2029_5_verdict",
            "2029 route verdict",
            "No existing current-state source signs a full physical S_Z normal form. The least-scrutiny route is to prove Z is quotient/constraint/auxiliary, not a propagating local scalar; canonical double-zero remains the finite-field fallback.",
            "ROUTE_SORTED_NONCLAIM",
            "the next work is a parent object-language/constraint origin proof or finite coefficient acquisition, not another Dq-only pass",
            "parent origin and numeric rows missing",
            "select 2030 object-language/constraint-origin target",
        ),
    ]
    rows = []
    for row_id, route, normal_form, status, strength, blocker, selection in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "route": route,
                "normal_form": normal_form,
                "status": status,
                "strength": strength,
                "blocker": blocker,
                "selection": selection,
            }
        )
        rows.append(row)
    return rows


def coefficient_pack_rows() -> list[dict[str, object]]:
    data = [
        ("SZC2029_0_K0", "K0", "local kinetic coefficient in canonical normalization", "K0>0", "MISSING_VALUE_OR_THEOREM", "canonical finite field"),
        ("SZC2029_1_Z0", "Z0", "local branch point/background representative", "partial_mu Z0=0", "MISSING_LOCAL_BRANCH", "canonical/constraint"),
        ("SZC2029_2_V0", "V(Z0)", "local vacuum source level", "0 after non-circular reference", "MISSING_VACUUM_REFERENCE", "canonical finite field"),
        ("SZC2029_3_Vprime0", "V'(Z0)", "stationarity/linear-force coefficient", "0", "MISSING_STATIONARITY_PROOF", "canonical finite field"),
        ("SZC2029_4_Vsecond0", "V''(Z0)", "positive Hessian before kinetic normalization", ">0 if K0>0", "MISSING_HESSIAN", "canonical finite field"),
        ("SZC2029_5_mZ2", "m_Z^2", "V''(Z0)/K0", ">0", "MISSING_MASS_GAP", "canonical finite field"),
        ("SZC2029_6_ellZ", "ell_Z", "1/m_Z in c=hbar=1 units", "finite positive range", "MISSING_MASS_GAP", "canonical finite field"),
        ("SZC2029_7_AZ", "A_Z", "local profile amplitude |zeta(d0)| or source boundary amplitude", "finite source-backed value", "MISSING_PROFILE_AMPLITUDE", "finite residual"),
        ("SZC2029_8_QZ", "Q_Z/B_Z", "boundary charge or linked flux", "zero/proper/exact or bounded", "MISSING_BOUNDARY_ZERO_OR_VALUE", "all routes"),
        ("SZC2029_9_direct_slot", "partial_Z S_matter/readout/source", "direct source/readout/theta coefficient", "zero theorem or bounded value", "MISSING_NO_SOURCE_SLOT_PROOF", "all routes"),
        ("SZC2029_10_JBZ", "J_B^Z", "delta S_Z/delta B_obs on local branch", "zero theorem or bounded source ratio", "MISSING_PARENT_ACTION_VALUE", "finite residual"),
        ("SZC2029_11_CZB", "C_ZB", "delta J_B^Z/delta Z on local branch", "zero theorem or bounded first-order slope", "MISSING_MIXED_HESSIAN", "finite residual"),
        ("SZC2029_12_arena_projection", "Pi_arena", "projection to PPN/R10/WEP/clocks/orbital observables", "declared map and units", "MISSING_ARENA_PROJECTION", "testing"),
    ]
    rows = []
    for row_id, symbol, definition, required_value, status, route in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "required_value": required_value,
                "status": status,
                "route": route,
                "source_path": "MISSING_PARENT_OR_DATA_SOURCE",
                "claim_status": "NONCLAIM_COEFFICIENT_ROW",
            }
        )
        rows.append(row)
    return rows


def normal_form_equation_rows() -> list[dict[str, object]]:
    data = [
        (
            "EQ2029_0_canonical_action",
            "S_Z^can",
            "int sqrt(-g_obs)[-1/2 K0 (nabla zeta)^2 - 1/2 K0 m_Z^2 zeta^2 + O(zeta^3)] + S_boundary",
            "valid only after V0=Vprime0=0 and K0,mZ2 are source-backed",
            "NONCLAIM_FORMULA",
        ),
        (
            "EQ2029_1_double_zero_source",
            "J_B^Z,C_ZB",
            "J_B^Z|0=0 and C_ZB|0=0 if V0=Vprime0=grad Z0=Q_Z=direct_slot=0",
            "uses 2028 theorem; side channels must be signed",
            "CONDITIONAL_THEOREM_FORMULA",
        ),
        (
            "EQ2029_2_profile_tail",
            "zeta(d)",
            "|zeta(d)| <= A_Z exp(-d/ell_Z), ell_Z=1/m_Z",
            "requires positive gap and boundary/source amplitude",
            "NONCLAIM_BOUND_FORMULA",
        ),
        (
            "EQ2029_3_total_residual",
            "epsilon_Z_total",
            "C2 A_Z^2 (m_Z^2 + L_local^-2) exp(-2d/ell_Z) + |B_Z| + |direct_slot| + |tau_Z|",
            "scoreable only after units, norms and arena projection are sourced",
            "NONCLAIM_RESIDUAL_FORMULA",
        ),
        (
            "EQ2029_4_constraint_action",
            "S_Z^constraint",
            "int Lambda_Z C_Z[B,U] + exact/proper boundary; E_Lambda=0 and E_Z algebraically remove Z before readout",
            "preferred if Z is not meant to be a physical propagating local field",
            "CONDITIONAL_EXACT_ROUTE_FORMULA",
        ),
        (
            "EQ2029_5_quotient_action",
            "S_Z^quotient",
            "S_parent=S_red[q(Phi)] with raw Z absent except gauge-fixing/exact boundary terms",
            "kills local Z stress only if q/action/matter/boundary descent is parent-derived",
            "CONDITIONAL_EXACT_ROUTE_FORMULA",
        ),
    ]
    rows = []
    for row_id, symbol, formula, assumptions, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "symbol": symbol,
                "formula": formula,
                "assumptions": assumptions,
                "status": status,
            }
        )
        rows.append(row)
    return rows


def local_profile_schema_rows() -> list[dict[str, object]]:
    data = [
        ("PROF2029_0_profile_id", "profile_id", "unique local profile/source environment identifier", "dimensionless label", "MISSING_ROW"),
        ("PROF2029_1_arena", "arena", "R10, PPN, WEP, clock, orbital, or cosmology/local overlap", "label", "MISSING_ROW"),
        ("PROF2029_2_distance", "d", "distance from source/boundary/local transition wall", "length", "MISSING_ROW"),
        ("PROF2029_3_amplitude", "A_Z", "profile amplitude at reference distance", "field units", "MISSING_ROW"),
        ("PROF2029_4_range", "ell_Z", "1/m_Z or sourced transition range", "length", "MISSING_ROW"),
        ("PROF2029_5_boundary", "B_Z/Q_Z", "boundary/source flux contribution", "source units", "MISSING_ROW"),
        ("PROF2029_6_direct", "direct_slot", "matter/readout/source direct coefficient", "source/readout units", "MISSING_ROW"),
        ("PROF2029_7_total", "epsilon_Z_total", "arena-normalized residual", "arena-specific", "MISSING_ROW"),
        ("PROF2029_8_source_path", "source_path", "path to derivation/table producing numbers", "path", "MISSING_ROW"),
        ("PROF2029_9_validity", "valid_for_claim", "true only if all source/value/unit/projection fields are real", "boolean", "FALSE_REQUIRED"),
    ]
    rows = []
    for row_id, field, definition, units, status in data:
        row = base_row()
        row.update(
            {
                "row_id": row_id,
                "field": field,
                "definition": definition,
                "units": units,
                "status": status,
                "claim_status": "SCHEMA_ONLY",
            }
        )
        rows.append(row)
    return rows


def claim_gate_rows() -> list[dict[str, object]]:
    data = [
        ("GATE2029_0_source_search", "current-state source search found a complete S_Z", "source register and coefficient pack", "FAIL_NOT_FOUND", False),
        ("GATE2029_1_canonical_double_zero", "canonical finite-field double-zero is active", "SZC2029_0..9 plus EQ2029_0..3", "FAIL_MISSING_COEFFICIENTS", False),
        ("GATE2029_2_constraint_auxiliary", "Z is removed by parent constraint/auxiliary before readout", "SZR2029_2;EQ2029_4;1858", "FAIL_UNSIGNED", False),
        ("GATE2029_3_quotient_representative", "raw Z is absent from physical action by quotient grammar", "SZR2029_1;EQ2029_5;Cperp skeleton", "FAIL_UNSIGNED", False),
        ("GATE2029_4_finite_profile", "finite residual profile is score-ready", "PROF2029_*;SZC2029_7..12", "FAIL_MISSING_NUMBERS", False),
        ("GATE2029_5_local_GR_claim", "local GR/Newton/PPN/R10 pass can be claimed", "GATE2029_1 or GATE2029_2 or GATE2029_3 or GATE2029_4", "FAIL_BLOCKED", False),
    ]
    rows = []
    for gate_id, claim, required_rows, status, allowed in data:
        row = base_row()
        row.update(
            {
                "gate_id": gate_id,
                "claim": claim,
                "required_rows": required_rows,
                "status": status,
                "claim_allowed": allowed,
                "reason": "S_Z origin/profile is not parent-signed or source-backed",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> list[dict[str, object]]:
    data = [
        ("DEC2029_0_source_result", "No current artifact supplies a complete claim-grade S_Z normal form with K0,V0,Vprime0,mZ2,A_Z,Q_Z and no-source-slot.", "keep all exact/local-GR claims blocked"),
        ("DEC2029_1_best_route", "If Z is not intended as a real local field, the best route is parent object-language/constraint/auxiliary removal, not canonical scalar tuning.", "this is less vulnerable to fifth-force scrutiny"),
        ("DEC2029_2_finite_field_route", "If Z is physical, canonical double-zero remains viable but needs a birth certificate and profile numbers.", "derive/source coefficients before testing local arenas"),
        ("DEC2029_3_testing_route", "If neither exact route closes, finite J_B^Z/C_ZB/profile rows become the honest empirical route.", "prepare scoreable rows without claiming local GR"),
    ]
    rows = []
    for decision_id, decision, consequence in data:
        row = base_row()
        row.update({"decision_id": decision_id, "decision": decision, "consequence": consequence})
        rows.append(row)
    return rows


def next_target_rows() -> list[dict[str, object]]:
    row = base_row()
    row.update(
        {
            "next_id": "NEXT2029_0_2030",
            "target_doc": "2030-Y5-R2FR-parent-object-language-Z-removal-or-SZ-coefficient-acquisition.md",
            "objective": "try to prove from MTS parent object-language that Z is quotient/constraint/auxiliary rather than a propagating local scalar; if not, acquire first real S_Z coefficient/profile rows",
            "required_inputs": "typed parent primitives; legality of Z kinetic/potential terms; constraint/auxiliary solve; boundary charge; matter/readout descent; or sourced K0,V0,Vprime0,mZ2,A_Z,Q_Z rows",
            "exclusions": "local-GR claim; Dq-only proof; stationarity-only proof; scalar tuning without source; hiding fifth-force terms; GitHub; formalization-workbench edits",
        }
    )
    return [row]


def write_branch_copies(
    route_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
) -> list[dict[str, object]]:
    copies = [
        ("COPY2029_0_source_weight", SOURCE_WEIGHT_DOCS / "AFRAME_SZ_ROUTE_SORT_2029_NONCLAIM.csv", route_rows),
        ("COPY2029_1_wep_lock", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2029_SZ_COEFFICIENT_STATUS_NONCLAIM.csv", coefficient_rows),
        ("COPY2029_2_acquisition_queue", QUEUE / "JR2029_SZ_PROFILE_AND_COEFFICIENT_QUEUE.csv", profile_rows + coefficient_rows),
    ]
    rows = []
    for copy_id, path, payload in copies:
        write_csv(path, payload)
        row = base_row()
        row.update(
            {
                "copy_id": copy_id,
                "path": str(path),
                "status": "WRITTEN_NONCLAIM_COPY" if path.exists() and csv_rows_parse(path) else "COPY_WRITE_FAIL",
            }
        )
        rows.append(row)
    return rows


def validation_rows(
    source_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    equation_rows: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL2029_00_sources_exist", all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in source_rows), "all cited source paths and needles exist"))
    checks.append(("VAL2029_01_csv_parse", all(path.exists() and csv_rows_parse(path) for path in csv_paths), "all generated CSV files parse cleanly"))
    checks.append(("VAL2029_02_routes_sorted", len(route_rows) == 6 and any(row["row_id"] == "SZR2029_5_verdict" for row in route_rows), "route sort includes verdict row"))
    checks.append(("VAL2029_03_canonical_formula", any(row["row_id"] == "EQ2029_0_canonical_action" and "m_Z^2" in str(row["formula"]) for row in equation_rows), "canonical S_Z normal-form formula is present"))
    checks.append(("VAL2029_04_constraint_formula", any(row["row_id"] == "EQ2029_4_constraint_action" and "Lambda_Z C_Z" in str(row["formula"]) for row in equation_rows), "constraint/auxiliary formula is present"))
    checks.append(("VAL2029_05_profile_schema", len(profile_rows) == 10 and any(row["field"] == "epsilon_Z_total" for row in profile_rows), "finite profile schema is complete enough for future rows"))
    checks.append(("VAL2029_06_coefficients_nonclaim", all(row["valid_for_claim"] is False and str(row["status"]).startswith("MISSING_") for row in coefficient_rows), "all coefficient rows remain missing/nonclaim"))
    checks.append(("VAL2029_07_claims_blocked", all(row["claim_allowed"] is False for row in gate_rows), "all local claims remain blocked"))
    checks.append(("VAL2029_08_next_selected", len(next_rows) == 1 and next_rows[0]["next_id"] == "NEXT2029_0_2030", "next target is selected"))
    checks.append(("VAL2029_09_formalization_unchanged", count_formalization_modified() == 0, "formalization-workbench modified-file count remains 0"))
    checks.append(("VAL2029_10_no_formalization_2029_artifacts", not formalization_has_2029_artifacts(), "no 2029 S_Z/profile artifacts were written under formalization-workbench"))
    rows = []
    for check_id, passed, detail in checks:
        row = base_row()
        row.update({"check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail})
        rows.append(row)
    overall = base_row()
    overall.update(
        {
            "check_id": "VAL2029_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL",
            "detail": "2029 S_Z normal-form/profile pack is internally valid and nonclaim.",
        }
    )
    rows.append(overall)
    return rows


def write_doc(
    source_rows: list[dict[str, object]],
    route_rows: list[dict[str, object]],
    coefficient_rows: list[dict[str, object]],
    equation_rows: list[dict[str, object]],
    profile_rows: list[dict[str, object]],
    gate_rows: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    branch_rows: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    lines = [
        "# 2029 Y5 R2FR Source S_Z Normal Form And Local Profile Pack",
        "",
        "## Current Verdict",
        "No claim-grade current-state source supplies the full `S_Z` birth certificate. The route split is now explicit: either `Z` is not a physical local scalar and must be removed by parent object-language, quotient, constraint, or auxiliary elimination; or `Z` is a physical finite field and must provide sourced `K0`, `V(Z0)`, `V'(Z0)`, `m_Z^2`, profile amplitude, boundary charge, and no-source-slot rows before any local-GR/Newton/PPN/R10 claim. The least-scrutiny route is the parent object-language/constraint route; the canonical double-zero remains the finite-field fallback.",
        "",
        "## Source Register",
        md_table(source_rows, ["source_id", "source_path", "status", "needles", "note", "valid_for_claim"]),
        "## S_Z Route Sort",
        md_table(route_rows, ["row_id", "route", "normal_form", "status", "strength", "blocker", "selection", "valid_for_claim"]),
        "## S_Z Coefficient Pack",
        md_table(coefficient_rows, ["row_id", "symbol", "definition", "required_value", "status", "route", "source_path", "claim_status", "valid_for_claim"]),
        "## Normal-Form Equations",
        md_table(equation_rows, ["row_id", "symbol", "formula", "assumptions", "status", "valid_for_claim"]),
        "## Local Profile Schema",
        md_table(profile_rows, ["row_id", "field", "definition", "units", "status", "claim_status", "valid_for_claim"]),
        "## Claim Gate",
        md_table(gate_rows, ["gate_id", "claim", "required_rows", "status", "claim_allowed", "reason", "valid_for_claim"]),
        "## Decision Ledger",
        md_table(decision_rows_, ["decision_id", "decision", "consequence", "valid_for_claim"]),
        "## Next Target",
        md_table(next_rows, ["next_id", "target_doc", "objective", "required_inputs", "exclusions", "valid_for_claim"]),
        "## Branch Copies",
        md_table(branch_rows, ["copy_id", "path", "status", "valid_for_claim"]),
        "## Validation",
        md_table(validation_rows_, ["check_id", "status", "detail", "valid_for_claim"]),
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    route_rows = route_sort_rows()
    coefficient_rows = coefficient_pack_rows()
    equation_rows = normal_form_equation_rows()
    profile_rows = local_profile_schema_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "source": OUT / "P8_Y5_PARENT_QLOC_2029_SOURCE_REGISTER.csv",
        "routes": OUT / "P8_Y5_PARENT_QLOC_2029_SZ_ROUTE_SORT.csv",
        "coefficients": OUT / "P8_Y5_PARENT_QLOC_2029_SZ_COEFFICIENT_PACK.csv",
        "equations": OUT / "P8_Y5_PARENT_QLOC_2029_NORMAL_FORM_EQUATIONS.csv",
        "profile": OUT / "P8_Y5_PARENT_QLOC_2029_LOCAL_PROFILE_SCHEMA.csv",
        "gate": OUT / "P8_Y5_PARENT_QLOC_2029_CLAIM_GATE.csv",
        "decision": OUT / "P8_Y5_PARENT_QLOC_2029_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2029_NEXT_TARGET.csv",
        "branch": OUT / "P8_Y5_PARENT_QLOC_2029_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2029_VALIDATION.csv",
    }
    write_csv(paths["source"], source_rows)
    write_csv(paths["routes"], route_rows)
    write_csv(paths["coefficients"], coefficient_rows)
    write_csv(paths["equations"], equation_rows)
    write_csv(paths["profile"], profile_rows)
    write_csv(paths["gate"], gate_rows)
    write_csv(paths["decision"], decision_rows_)
    write_csv(paths["next"], next_rows)
    branch_rows = write_branch_copies(route_rows, coefficient_rows, profile_rows)
    write_csv(paths["branch"], branch_rows)

    csv_paths_without_validation = [path for key, path in paths.items() if key != "validation"] + [
        Path(row["path"]) for row in branch_rows
    ]
    validation_rows_ = validation_rows(
        source_rows,
        route_rows,
        coefficient_rows,
        equation_rows,
        profile_rows,
        gate_rows,
        next_rows,
        csv_paths_without_validation,
    )
    write_csv(paths["validation"], validation_rows_)
    csv_paths = list(paths.values()) + [Path(row["path"]) for row in branch_rows]
    validation_rows_ = validation_rows(
        source_rows,
        route_rows,
        coefficient_rows,
        equation_rows,
        profile_rows,
        gate_rows,
        next_rows,
        csv_paths,
    )
    write_csv(paths["validation"], validation_rows_)
    write_doc(
        source_rows,
        route_rows,
        coefficient_rows,
        equation_rows,
        profile_rows,
        gate_rows,
        decision_rows_,
        next_rows,
        branch_rows,
        validation_rows_,
    )
    remove_pycache()


if __name__ == "__main__":
    main()
