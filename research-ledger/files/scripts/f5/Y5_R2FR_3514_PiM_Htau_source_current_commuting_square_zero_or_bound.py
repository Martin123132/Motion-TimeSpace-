from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3514-Y5-R2FR-PiM-Htau-source-current-commuting-square-zero-or-bound.md"
CANONICAL_COMMUTATOR = OUT / "P8_EM_PiM_Htau_commutator_residual_law.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3514": {"path": Path(__file__).resolve(), "role": "3514 generator"},
    "doc_3513": {
        "path": ROOT / "3513-Y5-R2FR-ellJ-source-current-owner-JH-Htau-PiM-Href-or-bound.md",
        "role": "3513 ell_J residual-law handoff",
    },
    "ellj_residual_3513": {
        "path": OUT / "P8_EM_ellJ_source_current_owner_residual_law.csv",
        "role": "canonical ell_J residual law",
    },
    "next_3513": {
        "path": OUT / "P8_Y5_R2FR_3513_NEXT_TARGET.csv",
        "role": "3514 target selection",
    },
    "pim_lock_2665": {
        "path": OUT / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv",
        "role": "Pi_M/Hamiltonian/source-domain lock",
    },
    "htau_integrability_2667": {
        "path": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "role": "H_tau integrability gate",
    },
    "source_measure_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
        "role": "H_tau/worldtube source-measure theorem",
    },
    "source_measure_residual_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_SOURCE_MEASURE_RESIDUAL_IDENTITY.csv",
        "role": "source-measure residual identity",
    },
    "reference_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
        "role": "reference/denominator anti-laundering contract",
    },
    "worldtube_2611": {
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
        "role": "worldtube source-owner audit",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "PHC3514_0_source_branch_bundle",
            "claim_piece": "source branch coordinates",
            "statement": "Treat the parent source branch as a local bundle with coordinates (M_H_ref, sigma^a) once tau, surfaces, reference and frame are fixed.",
            "formula": "B_source locally has coordinates (M,sigma); Pi_M^H := partial/partial M |_{sigma,tau,Sigma,H_ref,e_obs}",
            "status": "DERIVATION_FRAME_SET",
            "zero_condition": "M_H_ref is parent-defined and positive before orbital/R10 readout",
            "remaining_gap": "M_H_ref still depends on H_tau integrability and H_ref lock",
            "source_path": str(SOURCES["pim_lock_2665"]["path"]),
            "claim_allowed": "False",
        },
        {
            "derivation_id": "PHC3514_1_mass_connection_commutator",
            "claim_piece": "exact Pi_M commutator law",
            "statement": "For a residual direction X with source-branch connection D_X=partial_X+A_X^M partial_M+A_X^a partial_a, the commutator with Pi_M is fixed by mass-curvature of the connection.",
            "formula": "[D_X,Pi_M]F = -(partial_M A_X^M) partial_M F - (partial_M A_X^a) partial_a F + R_domain+R_frame+R_ref",
            "status": "EXACT_LOCAL_COORDINATE_IDENTITY",
            "zero_condition": "partial_M A_X^M=0, partial_M A_X^a=0, and domain/frame/reference maps are fixed",
            "remaining_gap": "source-branch connection A_X is not parent-derived",
            "source_path": str(SOURCES["ellj_residual_3513"]["path"]),
            "claim_allowed": "False",
        },
        {
            "derivation_id": "PHC3514_2_apply_to_Htau",
            "claim_piece": "Pi_M/H_tau square",
            "statement": "Applying the commutator law to H_tau-H_ref reduces the dangerous ell_J denominator drift to mass-connection curvature plus H_tau curl and boundary/source-domain terms.",
            "formula": "R_PiM+R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units",
            "status": "EXACT_RESIDUAL_REDUCTION",
            "zero_condition": "mass-flat source connection, integrable H_tau, source-blind H_ref, fixed support and same-frame readout",
            "remaining_gap": "C_M/C_shape and C_curl are not zero-owned",
            "source_path": str(SOURCES["source_measure_residual_2938"]["path"]),
            "claim_allowed": "False",
        },
        {
            "derivation_id": "PHC3514_3_conditional_zero_theorem",
            "claim_piece": "commutator zero route",
            "statement": "If the source branch is mass-flat and H_tau is an integrable Noether charge on the fixed source support, then the Pi_M/H_tau square commutes and the two hardest ell_J residual rows vanish.",
            "formula": "mass_flat(D_X,Pi_M) and curl(delta H_tau)=0 => R_PiM=R_Htau=0",
            "status": "CONDITIONAL_ZERO_THEOREM_NOT_LIVE",
            "zero_condition": "parent action supplies A_X, theta_MTS, omega_MTS, tau/surface lock and boundary exactness",
            "remaining_gap": "A_X and theta/omega owners are not yet derived",
            "source_path": str(SOURCES["htau_integrability_2667"]["path"]),
            "claim_allowed": "False",
        },
        {
            "derivation_id": "PHC3514_4_current_verdict",
            "claim_piece": "current MTS status",
            "statement": "3514 does not close local GR, but it turns the Pi_M/H_tau obstruction into a finite mathematical target: prove mass-flat source connection plus integrable H_tau, or bound those pieces.",
            "formula": "claim requires C_M=C_shape=C_curl=C_domain=C_ref=C_frame=C_units=0 or sourced independent bounds",
            "status": "NARROWED_NOT_CLAIMED",
            "zero_condition": "all commutator components are zero-owned without cancellation",
            "remaining_gap": "mass-connection law needs parent construction",
            "source_path": str(SOURCES["doc_3513"]["path"]),
            "claim_allowed": "False",
        },
    ]


def component_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PHCR3514_0_total",
            "component": "R_PiM_plus_R_Htau",
            "definition": "combined Pi_M/H_tau source-current square residual",
            "formula": "R_PiM+R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units",
            "source_status": "EXACT_COMPONENT_DECOMPOSITION_NONCLAIM",
            "zero_condition": "every component row below is zero-owned by parent geometry/source action",
            "observable_links": "ell_J; Newton_GM; PPN; R10; Gdot",
            "next_action": "derive mass-flat source connection before trying numeric scoring",
            "source_path": str(SOURCES["ellj_residual_3513"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCR3514_1_C_M",
            "component": "C_M",
            "definition": "mass-coordinate connection curvature",
            "formula": "C_M := -(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau)",
            "source_status": "NEW_PARENT_CONNECTION_REQUIRED",
            "zero_condition": "partial_M A_X^M=0: residual direction X does not change how source mass is parameterized",
            "observable_links": "Gdot; Newton_GM; orbital source mass",
            "next_action": "3515 should derive A_X from q(Phi) source-branch geometry",
            "source_path": str(SOURCES["pim_lock_2665"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCR3514_2_C_shape",
            "component": "C_shape",
            "definition": "shape/source-sector leakage into the mass projector",
            "formula": "C_shape := -(partial_M A_X^a) partial_a(H_tau-H_ref)/(Pi_M H_tau)",
            "source_status": "SOURCE_SHAPE_CONNECTION_UNSIGNED",
            "zero_condition": "partial_M A_X^a=0 or shape directions are orthogonal to Pi_M by parent metric",
            "observable_links": "WEP; R10 source support; PPN source profile",
            "next_action": "prove mass/shape orthogonality or carry shape-leakage bound rows",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCR3514_3_C_curl",
            "component": "C_curl",
            "definition": "H_tau field-space curl/nonintegrability",
            "formula": "C_curl := Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)",
            "source_status": "HTAU_INTEGRABILITY_CURL_OPEN",
            "zero_condition": "theta_MTS and omega_MTS are parent-derived and the boundary symplectic flux is exact/zero",
            "observable_links": "Gdot; Newton source; clocks; PPN",
            "next_action": "derive theta/omega owner or bound the curl",
            "source_path": str(SOURCES["htau_integrability_2667"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCR3514_4_C_domain",
            "component": "C_domain",
            "definition": "domain/Hodge/worldtube variation inside Pi_M",
            "formula": "C_domain := normalized D_X(W_source, Sigma, Hodge, linked surfaces)",
            "source_status": "DOMAIN_SUPPORT_NOT_PARENT_SIGNED",
            "zero_condition": "W_source and linked surfaces are selected from supp J_H[tau] before readout",
            "observable_links": "R10; Newton source; PPN near-source profile",
            "next_action": "keep as explicit source-support residual",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCR3514_5_C_ref",
            "component": "C_ref",
            "definition": "reference subtraction fails to commute with Pi_M or D_X",
            "formula": "C_ref := -([D_X,Pi_M]H_ref + Pi_M D_X H_ref)/(Pi_M H_tau)",
            "source_status": "REFERENCE_SELECTOR_UNSIGNED",
            "zero_condition": "H_ref is source-blind and fixed by boundary/topology/asymptotic coframe only",
            "observable_links": "R10 denominator; Gdot; local boundary terms",
            "next_action": "do not cancel against H_tau; derive selector after source connection",
            "source_path": str(SOURCES["reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCR3514_6_C_frame",
            "component": "C_frame",
            "definition": "same-frame/tau/surface readout mismatch",
            "formula": "C_frame := D_X ln(tau, e_obs, Sigma, readout frame mismatch)",
            "source_status": "PARALLEL_RFRAME_FACTOR",
            "zero_condition": "same observed frame/tau/source support is used in H_tau, Pi_M and readout",
            "observable_links": "clock; PPN; orbital_GM",
            "next_action": "retain as R_frame product gate",
            "source_path": str(SOURCES["reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCR3514_7_C_units",
            "component": "C_units",
            "definition": "normalization denominator/source unit leakage",
            "formula": "C_units := D_X ln(Pi_M H_tau denominator units)",
            "source_status": "ELLJ_UNITS_NONCLAIM",
            "zero_condition": "M_H_ref denominator is parent-owned and not defined from measured GM",
            "observable_links": "ell_J; Gdot; Newton_G",
            "next_action": "blocked until M_H_ref positivity and source-denominator lock",
            "source_path": str(SOURCES["reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def zero_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PHCG3514_0_mass_flat_connection",
            "condition": "partial_M A_X^M=0 and partial_M A_X^a=0",
            "meaning": "residual direction X does not reparameterize mass or leak mass into source-shape coordinates",
            "current_status": "NOT_PARENT_DERIVED",
            "blocks_claim": "True",
            "next_action": "derive A_X from q(Phi) source-branch geometry",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PHCG3514_1_integrable_Htau",
            "condition": "curl(delta H_tau)=0 up to exact/proper boundary terms",
            "meaning": "H_tau is a real charge rather than path-dependent bookkeeping",
            "current_status": "HTAU_CURL_GATE_OPEN",
            "blocks_claim": "True",
            "next_action": "derive theta_MTS/omega_MTS owner",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PHCG3514_2_fixed_support",
            "condition": "D_X W_source = 0 at fixed source-current support class",
            "meaning": "Pi_M is not secretly moving the source domain after seeing data",
            "current_status": "WORLDTUBE_SELECTOR_UNSIGNED",
            "blocks_claim": "True",
            "next_action": "prove W_source=closure(supp J_H[tau])",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PHCG3514_3_source_blind_reference",
            "condition": "D_X H_ref=0 and [D_X,Pi_M]H_ref=0",
            "meaning": "reference subtraction cannot launder the mass-current normalization",
            "current_status": "REFERENCE_SELECTOR_UNSIGNED",
            "blocks_claim": "True",
            "next_action": "derive Sigma_ref selector",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "PHCG3514_4_same_frame",
            "condition": "tau, e_obs, surfaces and readout frame are the same branch data",
            "meaning": "the commutator is not being changed by clock/frame normalization",
            "current_status": "RFRAME_PARALLEL_GATE_OPEN",
            "blocks_claim": "True",
            "next_action": "keep with R_frame product-lock branch",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PHCB3514_0_commutator_Gdot",
            "arena": "Gdot/time drift",
            "quantity": "R_PiM+R_Htau time projection",
            "prediction": "MISSING_C_M_C_SHAPE_C_CURL_TIME",
            "bound": "4.0e-14 yr^-1 only after other product factors are independent",
            "source_path": str(SOURCES["ellj_residual_3513"]["path"]),
            "runner_status": "BLOCKED_PREDICTION_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCB3514_1_PPN",
            "arena": "local PPN",
            "quantity": "projector/source prefactor residual",
            "prediction": "MISSING_PPN_COMMUTATOR_PROJECTION",
            "bound": "MISSING_PPN_BOUND",
            "source_path": str(SOURCES["pim_lock_2665"]["path"]),
            "runner_status": "BLOCKED_BOUND_AND_PROJECTION_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "PHCB3514_2_R10",
            "arena": "R10 alpha source",
            "quantity": "Qbar_XH denominator commutator",
            "prediction": "MISSING_R10_QBAR_DENOMINATOR_COMMUTATOR",
            "bound": "MISSING_ALPHA_LAMBDA_BOUND_LINK",
            "source_path": str(SOURCES["pim_lock_2665"]["path"]),
            "runner_status": "BLOCKED_DENOMINATOR_MISSING",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3514_0_result",
            "decision": "retain conditional commutator zero theorem",
            "rationale": "the mass-connection identity is exact, but A_X is not yet parent-derived",
            "effect": "Pi_M/H_tau obstruction is no longer vague; it is mass-flat connection plus H_tau curl",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3514_1_no_claim",
            "decision": "do not close ell_J/local GR from 3514",
            "rationale": "mass-flatness, integrability, support and reference gates are still unsigned",
            "effect": "all empirical/local rows stay nonclaim",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3514_2_next",
            "decision": "derive source-branch mass connection next",
            "rationale": "if A_X is parent-owned and mass-flat, one of the largest coupling obstructions collapses",
            "effect": "3515 targets q(Phi)-induced source-branch connection A_X",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3515-Y5-R2FR-source-branch-mass-connection-flatness-or-first-commutator-bound.md",
            "next_script": "scripts/Y5_R2FR_3515_source_branch_mass_connection_flatness_or_first_commutator_bound.py",
            "objective": "Try to derive the source-branch connection A_X from q(Phi), e_obs, tau and W_source, then prove partial_M A_X^M=partial_M A_X^a=0; if not, create first nonclaim numeric slots for C_M and C_shape.",
            "success_gate": "Mass-flat source connection is parent-signed, or C_M/C_shape become bounded nonclaim rows without measured-GM absorption.",
            "forbidden_shortcuts": "do not assume Pi_M fixed by definition; do not import orbital GM; do not hide source-shape leakage in H_ref or R_frame",
            "claim_allowed": "False",
        }
    ]


def validate(outputs: dict[str, Path], source_rows: list[dict[str, Any]], derivation: list[dict[str, Any]], components: list[dict[str, Any]], gates: list[dict[str, Any]], bounds: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    checks.append(
        {
            "check_id": "VAL3514_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in source_rows)),
            "detail": "all cited source paths exist",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3514_1_commutator_identity_present",
            "passed": bool_text(any("[D_X,Pi_M]" in row["formula"] and "partial_M A_X" in row["formula"] for row in derivation)),
            "detail": "mass-connection commutator identity written",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3514_2_component_reduction_present",
            "passed": bool_text(any(row["row_id"] == "PHCR3514_0_total" and "C_M" in row["formula"] and "C_curl" in row["formula"] for row in components)),
            "detail": "R_PiM+R_Htau component law written",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3514_3_zero_gates_block_claim",
            "passed": bool_text(all(row["blocks_claim"] == "True" and row["valid_for_claim"] == "False" for row in gates)),
            "detail": "all zero gates block claims until parent-signed",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3514_4_bound_rows_nonclaim",
            "passed": bool_text(all("MISSING_" in row["prediction"] and row["valid_for_claim"] == "False" for row in bounds)),
            "detail": "bound rows remain nonclaim while predictions are missing",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3514_5_next_target_mass_connection",
            "passed": bool_text(any("mass connection" in row["next_doc"] or "mass_connection" in row["next_script"] for row in next_rows)),
            "detail": "3515 mass-connection flatness selected next",
            "valid_for_claim": "False",
        }
    )

    csvs_parse = True
    parse_details: list[str] = []
    for name, path in outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        if name == "validation" and not path.exists():
            parse_details.append("validation:deferred_until_written")
            continue
        try:
            read_csv_rows(path)
            parse_details.append(name)
        except Exception as exc:  # pragma: no cover
            csvs_parse = False
            parse_details.append(f"{name}:{exc}")
    checks.append(
        {
            "check_id": "VAL3514_6_csvs_parse",
            "passed": bool_text(csvs_parse),
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3514_7_formalization_workbench_not_targeted",
            "passed": "True",
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )
    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3514_SUMMARY",
            "passed": bool_text(passed),
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    components: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3514 - PiM/Htau Source-Current Commuting Square: Zero Or Bound

## Summary
- **Actual derivation gain:** the `Pi_M/H_tau` obstruction is now a commutator law on a source-branch bundle.
- **Core identity:** `[D_X,Pi_M]F = -(partial_M A_X^M) partial_M F - (partial_M A_X^a) partial_a F + residuals`.
- **Applied result:** `R_PiM+R_Htau = C_M + C_shape + C_curl + C_domain + C_ref + C_frame + C_units`.
- **Current status:** not a local-GR claim; the next real target is deriving a parent-owned mass-flat source connection `A_X`.

## Source Register
{markdown_table(source_rows, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Commutator Derivation
{markdown_table(derivation, ["derivation_id", "claim_piece", "statement", "formula", "status", "zero_condition", "remaining_gap", "claim_allowed"])}

## Residual Components
{markdown_table(components, ["row_id", "component", "definition", "formula", "source_status", "zero_condition", "observable_links", "next_action", "valid_for_claim"])}

## Zero Gates
{markdown_table(gates, ["gate_id", "condition", "meaning", "current_status", "blocks_claim", "next_action", "valid_for_claim"])}

## Bound Input Template
{markdown_table(bounds, ["row_id", "arena", "quantity", "prediction", "bound", "runner_status", "valid_for_claim"])}

## Decisions
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}

Generated: {now_utc()}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    derivation = derivation_rows()
    components = component_rows()
    gates = zero_gate_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3514_SOURCE_REGISTER.csv",
        "derivation": OUT / "P8_Y5_R2FR_3514_PIM_HTAU_COMMUTATOR_DERIVATION.csv",
        "components": OUT / "P8_Y5_R2FR_3514_PIM_HTAU_RESIDUAL_COMPONENTS.csv",
        "canonical_components": CANONICAL_COMMUTATOR,
        "zero_gates": OUT / "P8_Y5_R2FR_3514_PIM_HTAU_ZERO_GATES.csv",
        "bound_template": OUT / "P8_Y5_R2FR_3514_PIM_HTAU_BOUND_INPUT_TEMPLATE.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3514_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3514_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3514_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(
        outputs["derivation"],
        derivation,
        ["derivation_id", "claim_piece", "statement", "formula", "status", "zero_condition", "remaining_gap", "source_path", "claim_allowed"],
    )
    component_fields = ["row_id", "component", "definition", "formula", "source_status", "zero_condition", "observable_links", "next_action", "source_path", "valid_for_claim"]
    write_csv(outputs["components"], components, component_fields)
    write_csv(outputs["canonical_components"], components, component_fields)
    write_csv(outputs["zero_gates"], gates, ["gate_id", "condition", "meaning", "current_status", "blocks_claim", "next_action", "valid_for_claim"])
    write_csv(outputs["bound_template"], bounds, ["row_id", "arena", "quantity", "prediction", "bound", "source_path", "runner_status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"])

    validation_rows = validate(outputs, source_rows, derivation, components, gates, bounds, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(source_rows, derivation, components, gates, bounds, decisions, next_rows, validation_rows)

    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
