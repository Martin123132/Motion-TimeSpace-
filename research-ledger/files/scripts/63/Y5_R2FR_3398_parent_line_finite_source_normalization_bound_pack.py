from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3398-Y5-R2FR-parent-line-finite-source-normalization-bound-pack-under-AX1090.md"


def rel(path: Path) -> str:
    return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, Any]]:
    paths = [
        ("SRC3398_00_3395_doc", ROOT / "3395-Y5-R2FR-weak-field-source-normalization-return-under-AX1090.md", "3395 source-normalization parent line"),
        ("SRC3398_01_3395_residuals", OUT / "P8_Y5_R2FR_3395_COUPLING_RESIDUAL_CONTRACT_NONCLAIM.csv", "3395 residual contract"),
        ("SRC3398_02_3395_parent_line", OUT / "P8_Y5_R2FR_3395_MINIMAL_PARENT_ACTION_LINE_CANDIDATE.csv", "3395 minimal parent action line"),
        ("SRC3398_03_3396_doc", ROOT / "3396-Y5-R2FR-minimal-parent-line-integration-or-source-normalization-demotion-under-AX1090.md", "3396 integration audit"),
        ("SRC3398_04_3396_adoption_packet", OUT / "P8_Y5_R2FR_3396_PARENT_ADOPTION_PACKET_NONCLAIM.csv", "3396 staged parent adoption packet"),
        ("SRC3398_05_3396_demote", OUT / "P8_Y5_R2FR_3396_SOURCE_NORMALIZATION_DEMOTION_LEDGER.csv", "3396 demotion ledger"),
        ("SRC3398_06_3397_doc", ROOT / "3397-Y5-R2FR-full-PPN-vector-readiness-after-parent-line-audit-under-AX1090.md", "3397 full PPN vector readiness"),
        ("SRC3398_07_3397_inputs", OUT / "P8_Y5_R2FR_3397_PPN_INPUT_SCHEMA_NONCLAIM.csv", "3397 PPN input schema"),
        ("SRC3398_08_2576_law", OUT / "P8_Y5_HCORE_QR_COUPLING_2576_NEWTON_PPN_COEFFICIENT_LAW.csv", "2576 Newton/PPN coefficient law"),
        ("SRC3398_09_3377_theorem", OUT / "P8_Y5_R2FR_3377_WEAK_FIELD_SOURCE_NORMALIZATION_THEOREM.csv", "3377 weak-field source-normalization theorem"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, description in paths:
        rows.append(
            {
                "source_id": source_id,
                "path": rel(path),
                "exists": path.exists(),
                "description": description,
                "role": "upstream_evidence",
                "valid_for_claim": False,
            }
        )
    return rows


def residual_bound_definitions() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "RB3398_0_delta_kappa",
            "symbol": "delta_kappa",
            "definition": "delta_kappa := kappa_MTS*c^4/(8*pi*G_ref)-1",
            "zero_condition": "MPL3395 signs one universal c-explicit parent coefficient kappa_MTS=8*pi*G_ref/c^4 before readout",
            "finite_bound_symbol": "B_delta_kappa",
            "finite_bound_law": "|delta_kappa| <= B_delta_kappa",
            "current_bound_status": "FINITE_SYMBOLIC_BOUND_DEFINED_NUMERIC_PARENT_COEFFICIENT_MISSING",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RB3398_1_delta_ellJ",
            "symbol": "delta_ellJ",
            "definition": "delta_ellJ := J_H/J_Hilbert-1, equivalently ell_J-1 if the only mismatch is a source-current scale",
            "zero_condition": "same matter variation defines Hilbert stress, Hamiltonian source current, compact mass, and PPN source density",
            "finite_bound_symbol": "B_delta_ellJ",
            "finite_bound_law": "|delta_ellJ| <= B_delta_ellJ",
            "current_bound_status": "FINITE_SYMBOLIC_BOUND_DEFINED_MATTER_DESCENT_COEFFICIENT_MISSING",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RB3398_2_epsilon_Gref_match",
            "symbol": "epsilon_Gref_match",
            "definition": "epsilon_Gref_match := |G_Htau/G_Poisson-1| + |G_PPN/G_Poisson-1|",
            "zero_condition": "EH, Hamiltonian/Gauss, and PPN source potential inherit the same G_ref and M_H branch",
            "finite_bound_symbol": "B_epsilon_Gref_match",
            "finite_bound_law": "epsilon_Gref_match <= B_GH + B_GPPN",
            "current_bound_status": "FINITE_SYMBOLIC_BOUND_DEFINED_HTAU_PPN_MATCH_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RB3398_3_delta_KC",
            "symbol": "delta_KC",
            "definition": "for L_v=-A_v|grad v|^2-B_v*rho_H*c^2*v, delta_KC := (B_v/A_v)/(16*pi*G_ref/c^4)-1",
            "zero_condition": "A_v=c^4/(32*pi*G_ref) and B_v=1/2, so variation gives nabla^2 v=8*pi*G_ref*rho_H/c^2",
            "finite_bound_symbol": "B_delta_KC",
            "finite_bound_law": "|delta_KC| <= B_delta_KC",
            "current_bound_status": "FINITE_SYMBOLIC_BOUND_DEFINED_V_ACTION_RATIO_INPUTS_MISSING",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RB3398_4_Delta_Newton_v_coupled",
            "symbol": "Delta_Newton_v_coupled",
            "definition": "Delta_Newton_v_coupled := (1+delta_KC)(1+epsilon_M)(1+delta_kappa)(1+delta_ellJ)-1",
            "zero_condition": "delta_KC=epsilon_M=delta_kappa=delta_ellJ=0 independently, with no cancellation credit",
            "finite_bound_symbol": "B_Delta_Newton",
            "finite_bound_law": "|Delta_Newton_v_coupled| <= (1+B_delta_KC)*(1+B_epsilon_M)*(1+B_delta_kappa)*(1+B_delta_ellJ)-1",
            "current_bound_status": "FINITE_COMPOSITE_BOUND_DERIVED_COMPONENT_NUMERICS_MISSING",
            "valid_for_claim": False,
        },
        {
            "residual_id": "RB3398_5_kappa_v",
            "symbol": "kappa_v",
            "definition": "kappa_v := -eta_v + kappa_source_quad + kappa_PiM + kappa_boundary + kappa_readout + kappa_operator + kappa_coupling",
            "zero_condition": "all second-order beta-source, PiM, boundary, readout, operator, and coupling terms vanish or cancel by a signed identity, not by fitting",
            "finite_bound_symbol": "B_kappa_v",
            "finite_bound_law": "|kappa_v| <= B_eta_v+B_source_quad+B_PiM+B_boundary+B_readout+B_operator+B_coupling",
            "current_bound_status": "FINITE_SUM_BOUND_DERIVED_COMPONENT_NUMERICS_MISSING",
            "valid_for_claim": False,
        },
    ]


def component_inputs() -> list[dict[str, Any]]:
    return [
        {
            "input_id": "CI3398_0_K_parent",
            "feeds": "B_delta_kappa",
            "needed_quantity": "kappa_MTS or branch coefficient K_parent",
            "required_relation": "K_parent = 8*pi*G_ref/c^4",
            "available_now": False,
            "status": "MISSING_PARENT_NUMERIC_OR_SIGNED_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "input_id": "CI3398_1_J_ratio",
            "feeds": "B_delta_ellJ",
            "needed_quantity": "J_H/J_Hilbert or ell_J",
            "required_relation": "J_H=J_Hilbert and ell_J=1 in same e_obs,tau branch",
            "available_now": False,
            "status": "MISSING_MATTER_DESCENT_NUMERIC_OR_SIGNED_IDENTITY",
            "valid_for_claim": False,
        },
        {
            "input_id": "CI3398_2_G_Htau",
            "feeds": "B_epsilon_Gref_match",
            "needed_quantity": "G_Htau/G_Poisson",
            "required_relation": "G_Htau=G_Poisson=G_ref",
            "available_now": False,
            "status": "MISSING_HTAU_GAUSS_NORMALIZATION",
            "valid_for_claim": False,
        },
        {
            "input_id": "CI3398_3_G_PPN",
            "feeds": "B_epsilon_Gref_match",
            "needed_quantity": "G_PPN/G_Poisson",
            "required_relation": "PPN U uses same G_ref and same M_H source",
            "available_now": False,
            "status": "MISSING_PPN_SOURCE_POTENTIAL_NORMALIZATION",
            "valid_for_claim": False,
        },
        {
            "input_id": "CI3398_4_Av_Bv",
            "feeds": "B_delta_KC",
            "needed_quantity": "A_v and B_v in L_v=-A_v|grad v|^2-B_v*rho_H*c^2*v",
            "required_relation": "B_v/A_v=16*pi*G_ref/c^4",
            "available_now": False,
            "status": "MISSING_PARENT_V_REDUCTION_COEFFICIENTS",
            "valid_for_claim": False,
        },
        {
            "input_id": "CI3398_5_epsilon_M",
            "feeds": "B_Delta_Newton",
            "needed_quantity": "epsilon_M mass-current glue residual",
            "required_relation": "M_source[v]=M_eff[Pi_M J_H]",
            "available_now": False,
            "status": "MISSING_WORLD_TUBE_HILBERT_SOURCE_SELECTOR",
            "valid_for_claim": False,
        },
        {
            "input_id": "CI3398_6_kappa_v_components",
            "feeds": "B_kappa_v",
            "needed_quantity": "eta_v, source_quad, PiM, boundary, readout, operator, coupling component bounds",
            "required_relation": "each component is zero by signed identity or has an independent finite source-bound",
            "available_now": False,
            "status": "MISSING_SECOND_ORDER_COMPONENT_BOUNDS",
            "valid_for_claim": False,
        },
    ]


def derived_bound_ledger() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "DER3398_0_v_action_ratio",
            "claim": "the v-action source coefficient ratio is fixed by variation, not guessed",
            "derivation": "delta int(-A_v|grad v|^2-B_v*rho_H*c^2*v)=0 gives 2*A_v*nabla^2 v=B_v*rho_H*c^2; matching nabla^2 v=8*pi*G_ref*rho_H/c^2 requires B_v/A_v=16*pi*G_ref/c^4",
            "result": "delta_KC=(B_v/A_v)/(16*pi*G_ref/c^4)-1",
            "status": "DERIVED_RATIO_CONTRACT",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DER3398_1_newton_no_cancellation",
            "claim": "Newton amplitude residual can be bounded without hiding one failure in another factor",
            "derivation": "with independent nonnegative component bounds, |prod_i(1+r_i)-1| is controlled by prod_i(1+B_i)-1; no cancellation is credited",
            "result": "|Delta_Newton_v_coupled| <= (1+B_delta_KC)(1+B_epsilon_M)(1+B_delta_kappa)(1+B_delta_ellJ)-1",
            "status": "DERIVED_COMPOSITE_BOUND",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DER3398_2_kappav_triangle",
            "claim": "beta source residual has a finite scoring target once components are individually bounded",
            "derivation": "from 2576 kappa_v ledger, triangle inequality gives a non-cancellation upper bound across eta_v, source_quad, PiM, boundary, readout, operator, and coupling terms",
            "result": "|kappa_v| <= B_eta_v+B_source_quad+B_PiM+B_boundary+B_readout+B_operator+B_coupling",
            "status": "DERIVED_SUM_BOUND",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "DER3398_3_parent_zero_branch",
            "claim": "if MPL3395 is later parent-signed, the same table collapses to the zero branch instead of being rewritten",
            "derivation": "delta_kappa, delta_ellJ, epsilon_Gref_match, and delta_KC are all defined as deviations from the parent-owned same-source same-G branch",
            "result": "parent signature sets the first four residuals to zero; kappa_v still needs second-order ledger or signed beta identity",
            "status": "ZERO_BRANCH_COMPATIBLE",
            "valid_for_claim": False,
        },
    ]


def newton_coupling_bound() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "NB3398_0_first_order_exact_if_signed",
            "arena": "Newton/Poisson amplitude",
            "statement": "signed kappa_MTS=8*pi*G_ref/c^4 plus same Hilbert source gives nabla^2 Phi_N=4*pi*G_ref*rho_H",
            "source": "3395/3377 weak-field algebra",
            "status": "EXACT_CONDITIONAL",
            "numeric_bound_ready": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "NB3398_1_finite_fallback",
            "arena": "Newton/v branch amplitude",
            "statement": "|Delta_Newton_v_coupled| <= (1+B_delta_KC)(1+B_epsilon_M)(1+B_delta_kappa)(1+B_delta_ellJ)-1",
            "source": "3398 composite bound",
            "status": "FINITE_SYMBOLIC_NONCLAIM",
            "numeric_bound_ready": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "NB3398_2_no_measured_G_absorption",
            "arena": "anti-circularity",
            "statement": "measured orbital GM can calibrate a body mass only after the map is fixed; it cannot define G_ref, ell_J, N_G, M_H_ref, or Pi_M for the theorem",
            "source": "3395/3396 no-backfill guardrail",
            "status": "GUARDRAIL_CARRIED_FORWARD",
            "numeric_bound_ready": False,
            "valid_for_claim": False,
        },
    ]


def ppn_handoff() -> list[dict[str, Any]]:
    return [
        {
            "handoff_id": "PH3398_0_gamma",
            "ppn_parameter": "gamma",
            "source_bound_dependency": "B_delta_kappa;B_delta_ellJ;B_epsilon_Gref_match;local_hygiene_bound",
            "handoff_status": "SCORABLE_AFTER_NUMERIC_BOUNDS_AND_EMPIRICAL_SOURCE",
            "valid_for_claim": False,
        },
        {
            "handoff_id": "PH3398_1_beta",
            "ppn_parameter": "beta",
            "source_bound_dependency": "B_kappa_v;B_Delta_Newton;local_hygiene_bound",
            "handoff_status": "SCORABLE_AFTER_SECOND_ORDER_COMPONENT_BOUNDS",
            "valid_for_claim": False,
        },
        {
            "handoff_id": "PH3398_2_alpha",
            "ppn_parameter": "alpha1;alpha2;alpha3",
            "source_bound_dependency": "preferred-frame residuals plus B_delta_ellJ/B_epsilon_Gref_match",
            "handoff_status": "NEEDS_VECTOR_SOURCE_BOUNDS",
            "valid_for_claim": False,
        },
        {
            "handoff_id": "PH3398_3_zeta",
            "ppn_parameter": "zeta1;zeta2;zeta3;zeta4",
            "source_bound_dependency": "stress-conservation/source-current descent plus boundary/reference residuals",
            "handoff_status": "NEEDS_CONSERVATION_AND_BOUNDARY_SOURCE_BOUNDS",
            "valid_for_claim": False,
        },
        {
            "handoff_id": "PH3398_4_xi",
            "ppn_parameter": "xi",
            "source_bound_dependency": "preferred-location/aniso-kernel/readout residuals plus local package",
            "handoff_status": "NEEDS_LOCATION_READOUT_BOUND",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3398_0_residual_formulas",
            "claim": "finite residual formulas exist for all six 3397 source-normalization rows",
            "gate_pass": True,
            "reason": "delta_kappa, delta_ellJ, epsilon_Gref_match, delta_KC, Delta_Newton_v_coupled, and kappa_v now have explicit zero and bound laws",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3398_1_numeric_inputs",
            "claim": "numeric source-normalization bounds exist",
            "gate_pass": False,
            "reason": "parent coefficients/source-current ratios/component bounds are not yet numeric or source-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3398_2_newton",
            "claim": "Newton amplitude is parent-derived or tightly bounded",
            "gate_pass": False,
            "reason": "composite bound law exists, but component bounds remain symbolic",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3398_3_ppn",
            "claim": "full local PPN vector is scorable",
            "gate_pass": False,
            "reason": "needs numeric 3398 bounds plus empirical PPN bound source pack",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "run_id": "RUN3398_0_residual_pack",
            "test": "six source-normalization residuals",
            "status": "PASS_FORMULAS_DEFINED_NONCLAIM",
            "detail": "six headline residual rows plus epsilon_M component input are present",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3398_1_v_ratio",
            "test": "delta_KC coefficient ratio derivation",
            "status": "PASS_DERIVED_RATIO_CONTRACT",
            "detail": "variation fixes B_v/A_v target as 16*pi*G_ref/c^4",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3398_2_newton_bound",
            "test": "Delta_Newton composite bound",
            "status": "PASS_SYMBOLIC_BOUND_READY",
            "detail": "non-cancellation product bound derived; numeric component bounds still missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3398_3_kappav_bound",
            "test": "kappa_v component sum bound",
            "status": "PASS_SYMBOLIC_BOUND_READY",
            "detail": "triangle bound exists; component ledgers still need numeric/source rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN3398_4_firewall",
            "test": "no local GR/Newton/PPN claim",
            "status": "PASS_CLAIM_FIREWALL",
            "detail": "all generated rows remain valid_for_claim=false",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3398_0_progress",
            "finding": "the coupling gap has been turned into a bound calculus",
            "reason": "six residuals now have explicit zero branches and finite fallback laws",
            "next_action": "fill numeric/source component bounds rather than re-litigating whether the gap exists",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3398_1_delta_KC",
            "finding": "delta_KC is not arbitrary",
            "reason": "the v-action variation fixes the needed coefficient ratio B_v/A_v=16*pi*G_ref/c^4",
            "next_action": "audit parent reduction for A_v and B_v or bound their mismatch",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3398_2_delta_Newton",
            "finding": "Newton amplitude can be bounded without cancellation games",
            "reason": "product bound separates delta_KC, epsilon_M, delta_kappa, and delta_ellJ",
            "next_action": "source or derive each component independently",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3398_3_kappav",
            "finding": "beta cannot be claimed from gamma or reciprocal readout alone",
            "reason": "kappa_v is now a component-sum bound target with named missing pieces",
            "next_action": "build the second-order beta component ledger",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3399-Y5-R2FR-source-normalization-component-extractor-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3399_source_normalization_component_extractor.py",
            "objective": "extract or construct numeric/source rows for B_delta_kappa, B_delta_ellJ, B_GH, B_GPPN, B_delta_KC, B_epsilon_M, and the kappa_v component bounds",
            "why_next": "3398 supplies the formulas; 3399 must populate the component bound inputs from parent algebra, data conventions, or explicit nonclaim source rows",
            "valid_for_claim": False,
        },
        {
            "target_id": "3400-Y5-R2FR-empirical-PPN-bound-source-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3400_empirical_PPN_bound_source_pack.py",
            "objective": "source empirical PPN bounds for gamma, beta, alpha_i, zeta_i, and xi so 3397/3398 can be scored later",
            "why_next": "even perfect MTS residual rows still need a sourced empirical PPN comparison table",
            "valid_for_claim": False,
        },
    ]


def validate(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": passed, "detail": detail})

    sources = outputs["source_register"]
    add(
        "VAL3398_0_sources_exist",
        "all cited upstream source paths exist",
        all(str(row["exists"]).lower() == "true" or row["exists"] is True for row in sources),
        f"sources={len(sources)}",
    )

    expected_symbols = {
        "delta_kappa",
        "delta_ellJ",
        "epsilon_Gref_match",
        "delta_KC",
        "Delta_Newton_v_coupled",
        "kappa_v",
    }
    found_symbols = {row["symbol"] for row in outputs["residual_bound_definitions"]}
    add(
        "VAL3398_1_six_residuals",
        "six 3397 source-normalization residuals have bound rows",
        expected_symbols == found_symbols,
        "found=" + ";".join(sorted(found_symbols)),
    )

    add(
        "VAL3398_2_bound_laws_present",
        "every residual row has zero condition and finite bound law",
        all(row["zero_condition"] and row["finite_bound_law"] for row in outputs["residual_bound_definitions"]),
        "",
    )
    add(
        "VAL3398_3_delta_KC_derivation",
        "delta_KC variation ratio is derived",
        any("16*pi*G_ref/c^4" in row["result"] for row in outputs["derived_bound_ledger"]),
        "",
    )
    add(
        "VAL3398_4_newton_product_bound",
        "Delta_Newton composite product bound is present",
        any("(1+B_delta_KC)" in row["finite_bound_law"] for row in outputs["residual_bound_definitions"]),
        "",
    )
    add(
        "VAL3398_5_kappav_component_bound",
        "kappa_v component-sum bound is present",
        any("B_eta_v" in row["finite_bound_law"] for row in outputs["residual_bound_definitions"]),
        "",
    )
    add(
        "VAL3398_6_claim_firewall",
        "all generated claim flags remain false",
        all(str(row.get("valid_for_claim", False)).lower() == "false" for group in outputs.values() for row in group),
        "",
    )
    add(
        "VAL3398_7_outputs_parse",
        "all generated CSV outputs parse cleanly",
        True,
        "checked after write by main",
    )
    add(
        "VAL3398_8_write_scope",
        "no 3398 output path targets formalization-workbench",
        "formalization-workbench" not in str(DOC).lower() and all("formalization-workbench" not in str(path).lower() for path in OUTPUT_PATHS.values()),
        "",
    )
    add(
        "VAL3398_9_next_target",
        "next target moves from formulas to numeric/source component extraction",
        any("component" in row["objective"] and "B_delta_kappa" in row["objective"] for row in outputs["next_target"]),
        "",
    )
    add(
        "VAL3398_10_overall",
        "3398 validation overall",
        all(str(row["passed"]).lower() == "true" or row["passed"] is True for row in rows),
        "all required checks passed",
    )
    return rows


OUTPUT_PATHS = {
    "source_register": OUT / "P8_Y5_R2FR_3398_SOURCE_REGISTER.csv",
    "residual_bound_definitions": OUT / "P8_Y5_R2FR_3398_RESIDUAL_BOUND_DEFINITIONS.csv",
    "component_inputs": OUT / "P8_Y5_R2FR_3398_COMPONENT_INPUTS_NONCLAIM.csv",
    "derived_bound_ledger": OUT / "P8_Y5_R2FR_3398_DERIVED_BOUND_LEDGER.csv",
    "newton_coupling_bound": OUT / "P8_Y5_R2FR_3398_NEWTON_COUPLING_BOUND.csv",
    "ppn_handoff": OUT / "P8_Y5_R2FR_3398_PPN_VECTOR_HANDOFF.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3398_PROMOTION_GATES.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3398_RUNNER_NONCLAIM.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3398_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3398_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3398_VALIDATION.csv",
}


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    timestamp = datetime.now(timezone.utc).isoformat()
    sections = [
        "# 3398 - Y5/R2FR parent-line finite source-normalization bound pack under AX1090",
        "",
        "## Summary",
        "- 3398 does not claim local GR, Newton, or PPN success.",
        "- It converts the coupling problem into explicit finite residual laws for `delta_kappa`, `delta_ellJ`, `epsilon_Gref_match`, `delta_KC`, `Delta_Newton_v_coupled`, and `kappa_v`.",
        "- The concrete advance is that `delta_KC` now has a derived coefficient-ratio contract, `Delta_Newton_v_coupled` has a non-cancellation product bound, and `kappa_v` has a component-sum bound.",
        "- Numeric/source rows are still required before scoring; this checkpoint makes the next extraction target finite instead of foggy.",
        f"- Generated UTC: `{timestamp}`.",
        "",
        "## Source Register",
        md_table(outputs["source_register"]),
        "",
        "## Residual Bound Definitions",
        md_table(outputs["residual_bound_definitions"]),
        "",
        "## Component Inputs",
        md_table(outputs["component_inputs"]),
        "",
        "## Derived Bound Ledger",
        md_table(outputs["derived_bound_ledger"]),
        "",
        "## Newton Coupling Bound",
        md_table(outputs["newton_coupling_bound"]),
        "",
        "## PPN Vector Handoff",
        md_table(outputs["ppn_handoff"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Nonclaim Runner",
        md_table(outputs["runner_nonclaim"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    outputs = {
        "source_register": source_register(),
        "residual_bound_definitions": residual_bound_definitions(),
        "component_inputs": component_inputs(),
        "derived_bound_ledger": derived_bound_ledger(),
        "newton_coupling_bound": newton_coupling_bound(),
        "ppn_handoff": ppn_handoff(),
        "promotion_gates": promotion_gates(),
        "runner_nonclaim": runner_nonclaim(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    outputs["validation"] = validate(outputs)

    for name, rows in outputs.items():
        write_csv(OUTPUT_PATHS[name], rows)

    reparsed = []
    for path in OUTPUT_PATHS.values():
        reparsed.append((path.name, len(read_csv(path))))
    validation_rows = read_csv(OUTPUT_PATHS["validation"])
    if not all(row["passed"].lower() == "true" for row in validation_rows):
        raise RuntimeError("3398 validation failed")

    write_doc(outputs)
    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUT_PATHS)} CSV outputs under {OUT}")
    print("Parsed outputs: " + "; ".join(f"{name}={count}" for name, count in reparsed))


if __name__ == "__main__":
    main()
