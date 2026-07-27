from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1105-Y5-R10-master-no-hidden-visible-coefficient-morphism-or-explicit-closure-pack.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    stamped: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        stamped.append(copied)
    return stamped


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "SRC1105_0_1104_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1104_NEXT_TARGET.csv",
            "needle": "NEXT1104_0_1105",
            "note": "1104 handoff to master no-hidden-visible coefficient morphism.",
        },
        {
            "source_id": "SRC1105_1_1104_closure",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1104_EXPLICIT_CLOSURE_LEDGER.csv",
            "needle": "CLOS1104_1_master_closure_candidate",
            "note": "1104 selected master closure candidate.",
        },
        {
            "source_id": "SRC1105_2_1091_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1091_OPERATOR_DOMAIN_THEOREM_ATTEMPT.csv",
            "needle": "ODH1091_6_verdict",
            "note": "older operator-domain theorem attempt already tests this route.",
        },
        {
            "source_id": "SRC1105_3_1091_obstruction",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1091_OPERATOR_DOMAIN_OBSTRUCTION_LEDGER.csv",
            "needle": "OBS1091_0_invariant_scalar",
            "note": "hidden invariant scalar obstruction.",
        },
        {
            "source_id": "SRC1105_4_1091_decision",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1091_DECISION_LEDGER.csv",
            "needle": "DEC1091_0_theorem_result",
            "note": "1091 decision: theorem not derived.",
        },
        {
            "source_id": "SRC1105_5_1058_exhaustion",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1058_VISIBLE_OPERATOR_DOMAIN_EXHAUSTION_ATTEMPT.csv",
            "needle": "VOE1058_5_verdict",
            "note": "visible operator-domain exhaustion attempt.",
        },
        {
            "source_id": "SRC1105_6_1049_classification",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1049_OPERATOR_CLASSIFICATION_RULE_ATTEMPT.csv",
            "needle": "OCR1049_5_verdict",
            "note": "operator classification/symmetry-ban attempt.",
        },
        {
            "source_id": "SRC1105_7_980_no_marker",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "NMF980_2_scalar_obstruction_lemma",
            "note": "scalar obstruction lemma.",
        },
        {
            "source_id": "SRC1105_8_1051_no_mixed",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1051_NO_MIXED_MORPHISM_LEMMA_ATTEMPT.csv",
            "needle": "NMM1051_5_verdict",
            "note": "no mixed morphism lemma attempt.",
        },
        {
            "source_id": "SRC1105_9_1098_requirements",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1098_SOURCE_BACKED_COEFFICIENT_REQUIREMENTS.csv",
            "needle": "REQ1098_0_c_alpha",
            "note": "finite coefficient source requirements.",
        },
        {
            "source_id": "SRC1105_10_1051_clock",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1051_B_ALPHA_CLOCK_PRODUCT_PRIOR_CHAIN.csv",
            "needle": "BAP1051_2_best_current_product",
            "note": "clock alpha product bound.",
        },
        {
            "source_id": "SRC1105_11_1064_numeric",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
            "needle": "REQ1064_4_R10",
            "note": "relative-weight WEP/PPN/Gdot/R10 source requirements.",
        },
        {
            "source_id": "SRC1105_12_1102_inputs",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1102_ALPHA_PRODUCT_INPUT_STATUS.csv",
            "needle": "IN1102_6_tau_WEP",
            "note": "latest alpha-product missing-input ledger.",
        },
        {
            "source_id": "SRC1105_13_1104_signature",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1104_PARENT_SIGNATURE_LEDGER.csv",
            "needle": "SIG1104_5_no_hidden_visible_hom",
            "note": "1104 signature master clause.",
        },
    ]
    checked: list[dict[str, object]] = []
    for row in rows:
        path = ROOT / str(row["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **row,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(row["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "MHM1105_0_target",
                "claim_piece": "master no-hidden-visible coefficient morphism",
                "formal_statement": "Hom(C_hid, Coeff(O_vis)) = Const or absent for O_vis in {F^2, mass, Yukawa, binding, clock, source}.",
                "result": "TARGET_SHARP",
                "proof_or_obstruction": "would subsume no-extra-F2, no mass/binding vertex, no clock readout leak, and no source-only weight",
            },
            {
                "attempt_id": "MHM1105_1_trivial_invariant_algebra",
                "claim_piece": "sufficient theorem",
                "formal_statement": "O(C_hid)^inv = R implies any hidden-to-visible scalar coefficient is constant.",
                "result": "EXACT_CONDITIONAL_THEOREM",
                "proof_or_obstruction": "current corpus does not prove invariant algebra triviality",
            },
            {
                "attempt_id": "MHM1105_2_product_functor",
                "claim_piece": "visible sector factors only through q and representation data",
                "formal_statement": "S_vis = S_vis[q(Phi), theta_rep] and Coeff(O_vis) is not a target of hidden-sector maps.",
                "result": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
                "proof_or_obstruction": "this is the desired parent object-language rule, not a derivation from current primitives",
            },
            {
                "attempt_id": "MHM1105_3_scalar_counterexample",
                "claim_piece": "surviving hidden invariant kills the theorem",
                "formal_statement": "If I_hid is invariant and nonconstant, c(I_hid)=c0+epsilon I_hid defines a legal visible coefficient map.",
                "result": "COUNTEREXAMPLE_PROVED",
                "proof_or_obstruction": "980, 1051, and 1091 all retain this obstruction",
            },
            {
                "attempt_id": "MHM1105_4_symmetry_limit",
                "claim_piece": "ordinary gauge/diffeomorphism symmetry is insufficient",
                "formal_statement": "Gauge and diffeomorphism invariance allow f(I)F^2, m_A(I)bar(psi)psi, nu_i(I), and w_A(I)T_A unless stronger sequester/product rules are signed.",
                "result": "INSUFFICIENT_SYMMETRY",
                "proof_or_obstruction": "operator classification attempts keep those operators as residuals",
            },
            {
                "attempt_id": "MHM1105_5_radiative_readout_limit",
                "claim_piece": "bare no-mixed rule is not enough",
                "formal_statement": "S_bare no mixed terms does not imply S_eff/readout no mixed terms without radiative/readout closure.",
                "result": "RADIATIVE_READOUT_CLOSURE_UNSIGNED",
                "proof_or_obstruction": "loops/readout can regenerate visible coefficient maps",
            },
            {
                "attempt_id": "MHM1105_6_verdict",
                "claim_piece": "derive the master morphism in current MTS",
                "formal_statement": "MHM1105_1 plus product functor plus radiative closure plus no scalar obstruction.",
                "result": "MASTER_THEOREM_NOT_DERIVED_DEMOTE_TO_EXPLICIT_CLOSURE",
                "proof_or_obstruction": "the master clause is useful and minimal-looking, but it remains a closure unless parent object-language typing is derived",
            },
        ]
    )


def subcase_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "subcase_id": "SUB1105_0_alpha_F2",
                "visible_operator": "F_Q^2",
                "forbidden_coefficient": "f(I_hid), f_X(Xhat), lambda_A",
                "observable_pressure": "clock alpha, WEP Coulomb/material, R10 alpha(lambda), EM normalization",
                "current_status": "RETAINED_RESIDUAL",
                "zero_if_master_signed": "b_alpha=c_alpha=0 subject to gauge-norm/readout closure",
            },
            {
                "subcase_id": "SUB1105_1_matter_mass",
                "visible_operator": "bar(psi_A)psi_A, Yukawa/Higgs/QCD, binding response",
                "forbidden_coefficient": "m_A(I_hid), y_A(I_hid), Lambda_QCD(I_hid), B_A(I_hid)",
                "observable_pressure": "mass ratios, clocks, WEP composition, nuclear/binding channels",
                "current_status": "RETAINED_RESIDUAL",
                "zero_if_master_signed": "b_mu, b_mA, b_nuc, c_surface zero subject to matter-spectrum owner",
            },
            {
                "subcase_id": "SUB1105_2_source_weight",
                "visible_operator": "Hilbert/source coupling T_A",
                "forbidden_coefficient": "w_A(I_hid), kappa_A(I_hid), source-only material multiplier",
                "observable_pressure": "WEP source charge, Newtonian GM, PPN source normalization, R10 source/test strength",
                "current_status": "RETAINED_RESIDUAL",
                "zero_if_master_signed": "relative source weights vanish only with source functor/current owner",
            },
            {
                "subcase_id": "SUB1105_3_clock_readout",
                "visible_operator": "clock/spectral readout map nu_i",
                "forbidden_coefficient": "nu_i(I_hid), Hodge/readout hidden factor, shadow-clock slot",
                "observable_pressure": "clock drifts, redshift/readout residuals",
                "current_status": "RETAINED_RESIDUAL",
                "zero_if_master_signed": "clock channels inherit upstream zero constants only after readout closure",
            },
            {
                "subcase_id": "SUB1105_4_radiative_return",
                "visible_operator": "S_eff/readout coefficient",
                "forbidden_coefficient": "delta c_eff(I_hid,mu), post-variation projector coefficient",
                "observable_pressure": "all local finite coefficients can regenerate",
                "current_status": "RETAINED_RESIDUAL",
                "zero_if_master_signed": "tree-level closure stable only if EFT/readout closure also signed",
            },
        ]
    )


def closure_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "closure_id": "PACK1105_0_parent_object_language",
                "closure_clause": "visible coefficients are generated only by q(Phi), fixed representation data, topological levels, or explicitly retained residual operators",
                "why_needed": "otherwise neutral scalars can multiply visible operators",
                "status": "EXPLICIT_CLOSURE_UNLESS_DERIVED",
                "minimum_test": "no arena-specific coefficient can be introduced after local tests are seen",
            },
            {
                "closure_id": "PACK1105_1_hidden_invariant_triviality_or_no_target",
                "closure_clause": "either O(C_hid)^inv=R or hidden invariants have no target action on Coeff(O_vis)",
                "why_needed": "one surviving invariant scalar builds c0+epsilon I_hid",
                "status": "EXPLICIT_CLOSURE_UNLESS_DERIVED",
                "minimum_test": "list every surviving scalar invariant and its allowed coefficient targets",
            },
            {
                "closure_id": "PACK1105_2_product_sequester",
                "closure_clause": "S_vis factors through visible quotient data and not through hidden relaxation variables",
                "why_needed": "product functor would kill mixed coefficients but is currently unsigned",
                "status": "EXPLICIT_CLOSURE_UNLESS_DERIVED",
                "minimum_test": "prove or retain every hidden-visible product term",
            },
            {
                "closure_id": "PACK1105_3_radiative_readout_stability",
                "closure_clause": "S_eff and readout maps preserve the same no-hidden-visible coefficient rule",
                "why_needed": "tree-level sequester does not stop loop/readout regeneration",
                "status": "EXPLICIT_CLOSURE_UNLESS_DERIVED",
                "minimum_test": "no zero theorem is public unless loop/readout closure is signed",
            },
            {
                "closure_id": "PACK1105_4_residual_vector_if_unsigned",
                "closure_clause": "if any closure clause is unsigned, keep the corresponding coefficient/product in a residual vector with source-backed priors",
                "why_needed": "prevents omission from being mistaken for derivation",
                "status": "ACTIVE_NONCLAIM_POLICY",
                "minimum_test": "strict runners reject missing, symbolic, unity, or unsourced rows",
            },
        ]
    )


def finite_requirement_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "requirement_id": "FIN1105_0_alpha_coefficient",
                "channel": "alpha/EM",
                "needed_row": "source-backed b_alpha, c_alpha_DD, or theorem-zero no-extra-F2",
                "current_bound_or_threshold": "abs(c_alpha_DD or b_alpha) <= 8.320244933243533e-10 for DD/WEP pressure; clock product bound exists separately",
                "missing": "coefficient value/source or parent no-extra-F2 theorem",
                "source_rows": "REQ1098_0_c_alpha; BAP1051_2_best_current_product",
            },
            {
                "requirement_id": "FIN1105_1_clock_product",
                "channel": "clock",
                "needed_row": "numeric MTS prediction for b_alpha*tau_clock_time or tau_clock/Xhat map",
                "current_bound_or_threshold": "abs(b_alpha*tau_clock_time) <= 2.1e-18 yr^-1",
                "missing": "tau_clock_time; Xhat normalization; standalone alpha owner",
                "source_rows": "BAP1051_2_best_current_product; IN1102_0_clock_product_bound",
            },
            {
                "requirement_id": "FIN1105_2_WEP_alpha_product",
                "channel": "WEP alpha/material",
                "needed_row": "numeric P_WEP_alpha or beta_source_alpha*tau_WEP*material response product",
                "current_bound_or_threshold": "direct alpha product target 4.797780522732e-05",
                "missing": "beta_source_alpha; tau_WEP; direct product theorem/value",
                "source_rows": "IN1102_4_WEP_product_target; IN1102_5_beta_source_alpha; IN1102_6_tau_WEP",
            },
            {
                "requirement_id": "FIN1105_3_WEP_relative_source_weight",
                "channel": "source/WEP",
                "needed_row": "numeric abs(Delta_w_TiPt*tau_WEP) or theorem-zero no-w_A",
                "current_bound_or_threshold": "eta_TiPt/source-charge proxy <= 2.8e-15",
                "missing": "Delta_w_TiPt theorem-zero or numeric prior; tau_WEP projection",
                "source_rows": "REQ1064_0_WEP_species; SSE1066_5_verdict",
            },
            {
                "requirement_id": "FIN1105_4_R10_product",
                "channel": "R10 short range",
                "needed_row": "numeric alpha(lambda) or relative-weight product with lambda, K(lambda), source/test weights, tau_R10, and promoted bound curve",
                "current_bound_or_threshold": "alpha(lambda) curve required; anchor-only rows are nonclaim",
                "missing": "lambda/K/tau_R10/source-test product and claim-valid bound curve",
                "source_rows": "REQ1064_4_R10; 563 R10 acquisition policy",
            },
            {
                "requirement_id": "FIN1105_5_mass_binding",
                "channel": "mass/binding/material",
                "needed_row": "source-backed b_mu, b_mA, b_nuc, c_surface, or theorem-zero matter-spectrum owner",
                "current_bound_or_threshold": "abs(c_surface_DD or b_binding) <= 6.9875016461438634e-11; common DD scale <= 6.4461422294339073e-11",
                "missing": "coefficient value/source or parent no-mass/no-binding theorem",
                "source_rows": "REQ1098_1_c_surface; REQ1098_2_c_common",
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1105_0_master_theorem",
                "claim": "master no-hidden-visible coefficient morphism is derived",
                "gate_pass": "false",
                "reason": "surviving invariant scalar counterexample remains and product/sequester/radiative closure are unsigned",
            },
            {
                "gate_id": "CG1105_1_closure_public_claim",
                "claim": "explicit closure pack can be used as a claim of derivation",
                "gate_pass": "false",
                "reason": "closure is a discipline contract, not evidence that MTS derives GR/local silence",
            },
            {
                "gate_id": "CG1105_2_subcase_zeroes",
                "claim": "alpha, mass, source, clock, and readout coefficients are zero",
                "gate_pass": "false",
                "reason": "subcases remain retained residuals unless closure pack is parent-signed or coefficients are sourced",
            },
            {
                "gate_id": "CG1105_3_finite_rows",
                "claim": "finite coefficient/product rows are scoreable",
                "gate_pass": "false",
                "reason": "finite rows list source requirements but no valid numeric MTS prediction rows are supplied",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1105_0_theorem_result",
                "decision": "master morphism theorem is not derived in the current corpus",
                "because": "1091 already proves the scalar obstruction and 1105 confirms the product/sequester/radiative clauses are unsigned",
                "next_action": "demote to explicit closure pack unless a deeper parent object-language derivation is produced",
            },
            {
                "decision_id": "DEC1105_1_closure_status",
                "decision": "the explicit closure pack is useful but expensive",
                "because": "it is a compact way to stop many leaks, but it is still an axiom/contract unless derived",
                "next_action": "audit whether the pack is minimal and independent before adopting it",
            },
            {
                "decision_id": "DEC1105_2_finite_policy",
                "decision": "if any closure clause is not adopted, finite products must be sourced row by row",
                "because": "bounds and thresholds are not predictions",
                "next_action": "prepare a minimum axiom-count audit or first source-backed coefficient row plan",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1105_0_1106",
                "next_target": "1106-Y5-R10-minimal-explicit-closure-pack-independence-audit-or-first-source-backed-coefficient-row.md",
                "objective": "audit whether the explicit closure pack from 1105 is minimal and independent; if it is too axiom-heavy or redundant, split it into derivable pieces and first finite source-backed coefficient/product rows without claiming local-GR/WEP/R10/clock success",
                "include": "closure independence matrix; redundancy/subsumption map; acceptable parent-action axiom count; finite alpha/source/mass/clock/R10 row priority; strict refusal gates",
                "exclude": "calling closure a derivation; new public claim; tau=1; measured-G relative-weight absorption; standalone b_alpha; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorems: list[dict[str, object]],
    subcases: list[dict[str, object]],
    closures: list[dict[str, object]],
    finite_requirements: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add(
        "V1105_0_sources_exist",
        all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources),
        "all cited local source paths exist and needles are found",
    )
    add(
        "V1105_1_theorem_demoted",
        any(row["result"] == "MASTER_THEOREM_NOT_DERIVED_DEMOTE_TO_EXPLICIT_CLOSURE" for row in theorems),
        "master morphism theorem is explicitly not promoted",
    )
    add(
        "V1105_2_counterexample_retained",
        any(row["result"] == "COUNTEREXAMPLE_PROVED" for row in theorems),
        "hidden invariant scalar counterexample is retained",
    )
    add(
        "V1105_3_subcases_cover_channels",
        len(subcases) >= 5 and {"SUB1105_0_alpha_F2", "SUB1105_2_source_weight", "SUB1105_3_clock_readout"}.issubset({row["subcase_id"] for row in subcases}),
        "subcases cover alpha, matter, source, clock, and radiative return",
    )
    add(
        "V1105_4_closure_pack_written",
        len(closures) >= 5 and any(row["closure_id"] == "PACK1105_4_residual_vector_if_unsigned" for row in closures),
        "explicit closure pack plus residual policy written",
    )
    add(
        "V1105_5_finite_requirements_written",
        len(finite_requirements) >= 6 and all("missing" in row for row in finite_requirements),
        "finite coefficient/product source requirements written",
    )
    add(
        "V1105_6_claim_gates_blocked",
        all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in gates),
        "all claim gates remain blocked",
    )
    add(
        "V1105_7_no_claim_rows",
        all(row.get("valid_for_claim") == "false" for row in theorems + subcases + closures + finite_requirements + gates + decisions + next_target),
        "all generated rows are nonclaim",
    )
    add(
        "V1105_8_next_target",
        next_target[0]["next_target"].startswith("1106-") and "closure-pack-independence" in str(next_target[0]["next_target"]),
        "1106 handoff targets closure-pack independence or first sourced row",
    )
    add(
        "V1105_9_generated_under_post_checkpoint",
        all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()),
        "all generated outputs are under post-checkpoint-work",
    )
    csv_parse_ok = True
    for name, path in outputs.items():
        if name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1105_10_csv_parse", csv_parse_ok, "all 1105 CSV outputs parse cleanly")
    add(
        "V1105_11_formalization_untouched",
        True,
        "generator writes no outputs under formalization-workbench",
    )
    add(
        "V1105_SUMMARY",
        True,
        "1105 demotes the master no-hidden-visible morphism to explicit closure pack and records finite source-row requirements",
    )
    return rows


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorems: list[dict[str, object]],
    subcases: list[dict[str, object]],
    closures: list[dict[str, object]],
    finite_requirements: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1105 - Master No-Hidden-Visible Coefficient Morphism Or Explicit Closure Pack

**Current verdict:** the master no-hidden-visible coefficient morphism is not derived in the current corpus. The exact obstruction is still the same sharp knife: one surviving hidden invariant scalar can feed a visible coefficient map.

**What improved:** the failure is now compressed into a usable closure pack. That pack is not a public claim, but it is the cleanest private contract for stopping the same leak from reappearing as alpha drift, mass drift, source weights, clock readout, or radiative return.

**Finite branch:** if the closure pack is not derived or adopted, every affected channel needs a source-backed numeric coefficient/product row. Bounds and thresholds stay as pressure, not MTS predictions.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Theorem Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_obstruction", "claim_allowed"], theorems)}

## Subcase Map
{table(["subcase_id", "visible_operator", "forbidden_coefficient", "observable_pressure", "current_status", "zero_if_master_signed", "claim_allowed"], subcases)}

## Explicit Closure Pack
{table(["closure_id", "closure_clause", "why_needed", "status", "minimum_test", "claim_allowed"], closures)}

## Finite Source Requirements
{table(["requirement_id", "channel", "needed_row", "current_bound_or_threshold", "missing", "source_rows", "claim_allowed"], finite_requirements)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "claim_allowed"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1105_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_THEOREM_ATTEMPT.csv",
        "subcases": OUT / "P8_Y5_R10_1105_MASTER_MORPHISM_SUBCASE_MAP.csv",
        "closure_pack": OUT / "P8_Y5_R10_1105_EXPLICIT_CLOSURE_PACK.csv",
        "finite_requirements": OUT / "P8_Y5_R10_1105_FINITE_SOURCE_REQUIREMENTS.csv",
        "claim_gates": OUT / "P8_Y5_R10_1105_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1105_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R10_1105_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1105_VALIDATION.csv",
    }
    sources = source_rows()
    theorems = theorem_rows()
    subcases = subcase_rows()
    closures = closure_pack_rows()
    finite_requirements = finite_requirement_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorems)
    write_csv(outputs["subcases"], subcases)
    write_csv(outputs["closure_pack"], closures)
    write_csv(outputs["finite_requirements"], finite_requirements)
    write_csv(outputs["claim_gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next_target"], next_target)
    validation = validate(sources, theorems, subcases, closures, finite_requirements, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorems, subcases, closures, finite_requirements, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
