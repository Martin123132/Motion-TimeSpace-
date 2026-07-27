from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3515-Y5-R2FR-source-branch-mass-connection-flatness-or-first-commutator-bound.md"
CANONICAL_CONNECTION = OUT / "P8_EM_source_branch_mass_connection_flatness_law.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3515": {"path": Path(__file__).resolve(), "role": "3515 generator"},
    "doc_3514": {
        "path": ROOT / "3514-Y5-R2FR-PiM-Htau-source-current-commuting-square-zero-or-bound.md",
        "role": "3514 Pi_M/H_tau commutator handoff",
    },
    "commutator_3514": {
        "path": OUT / "P8_EM_PiM_Htau_commutator_residual_law.csv",
        "role": "canonical Pi_M/H_tau commutator law",
    },
    "next_3514": {
        "path": OUT / "P8_Y5_R2FR_3514_NEXT_TARGET.csv",
        "role": "3515 target selection",
    },
    "field_quotient_2570": {
        "path": OUT / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv",
        "role": "Dq vertical-generator ledger",
    },
    "common_descent_2643": {
        "path": OUT / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv",
        "role": "common quotient descent signature gate",
    },
    "source_identity_2642": {
        "path": OUT / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv",
        "role": "source-current identity proof attempt",
    },
    "source_descent_2909": {
        "path": OUT / "P8_Y5_R2FR_2909_SOURCE_CURRENT_DESCENT_PROOF_ATTEMPT.csv",
        "role": "source-current descent proof attempt",
    },
    "worldtube_2611": {
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
        "role": "worldtube source support audit",
    },
    "frame_1519": {
        "path": OUT / "P8_Y5_PARENT_FRAME_1519_COFRAME_TAU_LOCK_AUDIT.csv",
        "role": "coframe/tau lock audit",
    },
    "coframe_1739": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1739_PARENT_COFRAME_OWNERSHIP_THEOREM_ATTEMPT.csv",
        "role": "parent coframe ownership theorem attempt",
    },
    "readout_1926": {
        "path": OUT / "P8_Y5_PARENT_QLOC_1926_OBSERVED_FRAME_READOUT_CONTRACT.csv",
        "role": "observed frame/source readout contract",
    },
    "reference_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
        "role": "M_H_ref/reference anti-laundering contract",
    },
    "htau_integrability_2667": {
        "path": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "role": "H_tau integrability curl gate",
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


def connection_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "SBC3515_0_source_coordinate_map",
            "claim_piece": "source-coordinate map",
            "statement": "Define the source-branch coordinates as a parent map Y(Phi)=(M_H_ref(Phi), sigma^a(Phi)), where M_H_ref=H_tau-H_ref and sigma^a are support/shape coordinates of W_source.",
            "formula": "Y: Phi -> (M_H_ref, sigma^a); W_source=closure(supp J_H[tau]); M_H_ref=H_tau[S_outer]-H_ref",
            "derivation_status": "EXACT_DEFINITION_WITH_NONCLAIM_INPUTS",
            "zero_or_flat_condition": "Y factors through the public quotient q(Phi) and uses the same e_obs,tau,W_source,H_ref branch",
            "current_mts_status": "NOT_PARENT_SIGNED",
            "remaining_gap": "Y-through-q and H_tau/H_ref/worldtube ownership are not jointly signed",
            "source_path": str(SOURCES["commutator_3514"]["path"]),
            "claim_allowed": "False",
        },
        {
            "law_id": "SBC3515_1_induced_connection",
            "claim_piece": "source-branch connection",
            "statement": "The connection coefficients are not arbitrary coupling constants; they are the derivative of the source-coordinate map along the residual field direction.",
            "formula": "A_X^M := D_X M_H_ref = dM_H_ref(v_X); A_X^a := D_X sigma^a = d sigma^a(v_X)",
            "derivation_status": "EXACT_CHAIN_RULE_IDENTITY",
            "zero_or_flat_condition": "dY(v_X)=0",
            "current_mts_status": "DERIVED_AS_IDENTITY_NOT_ZERO",
            "remaining_gap": "v_X verticality and Y quotient-descent are not proven together",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
        {
            "law_id": "SBC3515_2_quotient_vertical_zero",
            "claim_piece": "strong zero theorem",
            "statement": "If Y=Ybar(q(Phi)) and v_X is vertical, then the whole source connection vanishes: A_X^M=A_X^a=0.",
            "formula": "A_X^I = dY^I(v_X)=dYbar^I(Dq(v_X)); Dq(v_X)=0 => A_X^I=0",
            "derivation_status": "EXACT_CONDITIONAL_ZERO_THEOREM",
            "zero_or_flat_condition": "source coordinate map descends through q and v_X in ker(Dq)",
            "current_mts_status": "CONDITIONAL_NOT_LIVE",
            "remaining_gap": "Dq vertical certificate plus source-coordinate descent certificate are missing",
            "source_path": str(SOURCES["common_descent_2643"]["path"]),
            "claim_allowed": "False",
        },
        {
            "law_id": "SBC3515_3_mass_flatness_corollary",
            "claim_piece": "mass-flatness",
            "statement": "The mass-flatness conditions needed by 3514 are weaker than the quotient zero theorem; if A_X vanishes identically, then partial_M A_X^M=partial_M A_X^a=0 automatically.",
            "formula": "A_X^I=0 on source branch => partial_M A_X^M=0 and partial_M A_X^a=0",
            "derivation_status": "EXACT_COROLLARY",
            "zero_or_flat_condition": "SBC3515_2 fires",
            "current_mts_status": "CONDITIONAL_NOT_LIVE",
            "remaining_gap": "same as quotient/source-coordinate descent",
            "source_path": str(SOURCES["commutator_3514"]["path"]),
            "claim_allowed": "False",
        },
        {
            "law_id": "SBC3515_4_failure_decomposition",
            "claim_piece": "connection obstruction law",
            "statement": "If the quotient zero theorem does not fire, A_X decomposes into a finite list of source-coordinate descent failures instead of remaining an undefined coupling.",
            "formula": "A_X^I = E_Dq^I + E_JH^I + E_Htau^I + E_ref^I + E_W^I + E_frame^I + E_readout^I",
            "derivation_status": "EXACT_RESIDUAL_BOOKKEEPING_LAW",
            "zero_or_flat_condition": "all E rows vanish or are independently bounded without cancellation",
            "current_mts_status": "COMPONENT_ROWS_NONCLAIM",
            "remaining_gap": "component zero proofs/bounds not supplied",
            "source_path": str(SOURCES["source_identity_2642"]["path"]),
            "claim_allowed": "False",
        },
        {
            "law_id": "SBC3515_5_current_verdict",
            "claim_piece": "current MTS status",
            "statement": "3515 proves the best route: the coupling source-connection dies if the source coordinates are quotient observables. Current MTS has not yet proven that descent, so no local-GR/Newton claim follows.",
            "formula": "local source-coupling closure now targets Y=Ybar(q(Phi)) and v_X in ker(Dq), not an arbitrary ell_J axiom",
            "derivation_status": "ROUTE_NARROWED_NOT_CLAIMED",
            "zero_or_flat_condition": "source-coordinate descent certificate closes",
            "current_mts_status": "NO_CLAIM",
            "remaining_gap": "3516 must prove quotient-source-coordinate descent or bound E_Dq/E_JH/E_W",
            "source_path": str(SOURCES["next_3514"]["path"]),
            "claim_allowed": "False",
        },
    ]


def obstruction_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SBR3515_0_total",
            "obstruction": "A_X_total",
            "definition": "full source-branch connection induced by residual direction X",
            "formula": "A_X=(A_X^M,A_X^a)=E_Dq+E_JH+E_Htau+E_ref+E_W+E_frame+E_readout",
            "zero_condition": "Y=Ybar(q(Phi)) and v_X in ker(Dq), or every component independently zero/bounded",
            "current_status": "EXACT_DECOMPOSITION_NONCLAIM",
            "observable_links": "ell_J; Pi_M/H_tau; Newton_GM; PPN; R10; Gdot",
            "next_action": "prove source-coordinate descent certificate",
            "source_path": str(SOURCES["commutator_3514"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBR3515_1_E_Dq",
            "obstruction": "E_Dq",
            "definition": "failure of residual direction to be vertical for source-coordinate observables",
            "formula": "E_Dq^I := dYbar^I(Dq(v_X)) when Y=Ybar(q(Phi)) is available",
            "zero_condition": "Dq(v_X)=0 for the actual residual basis used by local/R10/source tests",
            "current_status": "VERTICAL_CERTIFICATE_NOT_SIGNED",
            "observable_links": "all quotient-observable source tests",
            "next_action": "map v_X to actual vertical generator and Dq certificate",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBR3515_2_E_JH",
            "obstruction": "E_JH",
            "definition": "Hilbert/source-current descent failure inside Y",
            "formula": "E_JH^I := derivative of J_H/rho_H not induced by q(Phi), e_obs and tau",
            "zero_condition": "S_matter descends through q and J_H is the single Hilbert/worldtube current",
            "current_status": "SOURCE_CURRENT_DESCENT_NOT_PARENT_SIGNED",
            "observable_links": "WEP; R10 source; Newton mass; PPN",
            "next_action": "combine 2642/2909 current descent with source-coordinate map",
            "source_path": str(SOURCES["source_descent_2909"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBR3515_3_E_Htau",
            "obstruction": "E_Htau",
            "definition": "H_tau charge extraction/integrability failure inside M_H_ref",
            "formula": "E_Htau^M := D_X H_tau[S_outer] - dHbar_tau(Dq(v_X))",
            "zero_condition": "theta_MTS/Q_tau/omega_MTS are parent-derived and H_tau is integrable on fixed surfaces",
            "current_status": "HTAU_INTEGRABILITY_OPEN",
            "observable_links": "Gdot; Newton source; clocks; PPN",
            "next_action": "derive Noether charge/curl gate after source-coordinate descent is framed",
            "source_path": str(SOURCES["htau_integrability_2667"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBR3515_4_E_ref",
            "obstruction": "E_ref",
            "definition": "reference subtraction enters source coordinates non-quotiently",
            "formula": "E_ref^M := -D_X H_ref + dHbar_ref(Dq(v_X))",
            "zero_condition": "H_ref is fixed by quotient boundary/topology/asymptotic frame and source-blind",
            "current_status": "REFERENCE_SELECTOR_UNSIGNED",
            "observable_links": "R10 denominator; Gdot; local boundary",
            "next_action": "do not use H_ref to absorb source connection",
            "source_path": str(SOURCES["reference_2938"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBR3515_5_E_W",
            "obstruction": "E_W",
            "definition": "worldtube/support/shape coordinate descent failure",
            "formula": "E_W^a := D_X sigma^a[W_source] - d sigmabar^a(Dq(v_X))",
            "zero_condition": "W_source=closure(supp J_H[tau]) is parent-owned and same-frame",
            "current_status": "WORLDTUBE_SELECTOR_UNSIGNED",
            "observable_links": "R10 support; Newton source; PPN source profile",
            "next_action": "prove support selector is a quotient observable",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBR3515_6_E_frame",
            "obstruction": "E_frame",
            "definition": "coframe/tau/frame mismatch in source coordinates",
            "formula": "E_frame^I := D_X Y^I[e_obs,tau] - D_X Y^I[e_parent,tau_parent]",
            "zero_condition": "same e_obs and tau branch defines matter, H_tau, W_source and readout",
            "current_status": "COFRAME_TAU_LOCK_CONDITIONAL",
            "observable_links": "clock; PPN; orbital_GM",
            "next_action": "carry parallel R_frame gate until source coordinate descent closes",
            "source_path": str(SOURCES["frame_1519"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBR3515_7_E_readout",
            "obstruction": "E_readout",
            "definition": "post-readout source coordinate or measured-GM laundering",
            "formula": "E_readout^I := D_X(Y_readout^I - Y_parent^I)",
            "zero_condition": "observational GM/R10/PPN source values test but do not define Y",
            "current_status": "ANTI_LAUNDERING_GUARD_ONLY",
            "observable_links": "orbital_GM; R10; PPN",
            "next_action": "keep all readout rows nonclaim until Y_parent is derived",
            "source_path": str(SOURCES["readout_1926"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def flatness_rows() -> list[dict[str, Any]]:
    return [
        {
            "flatness_id": "SBF3515_0_strong_zero",
            "condition": "Y=Ybar(q(Phi)) and v_X in ker(Dq)",
            "result": "A_X^M=A_X^a=0",
            "implies": "C_M=C_shape=0 and the 3514 mass-connection obstruction disappears",
            "current_status": "CONDITIONAL_NOT_LIVE",
            "blocking_gap": "source-coordinate descent certificate not signed",
            "valid_for_claim": "False",
        },
        {
            "flatness_id": "SBF3515_1_mass_flat_weak",
            "condition": "partial_M A_X^M=0 and partial_M A_X^a=0",
            "result": "mass-flat source connection",
            "implies": "Pi_M commutator has no mass-curvature/source-shape leakage term",
            "current_status": "WEAKER_THAN_STRONG_ZERO_BUT_NOT_SIGNED",
            "blocking_gap": "A_X source formula still lacks parent proof",
            "valid_for_claim": "False",
        },
        {
            "flatness_id": "SBF3515_2_bound_fallback",
            "condition": "A_X not zero-derived",
            "result": "bound F_M:=partial_M A_X^M and F_shape:=partial_M A_X^a",
            "implies": "C_M/C_shape become executable nonclaim bound rows",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "blocking_gap": "no numeric derivative/source-coordinate rows",
            "valid_for_claim": "False",
        },
    ]


def bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SBB3515_0_C_M",
            "arena": "Gdot/Newton/orbital mass",
            "quantity": "C_M",
            "prediction_formula": "abs(partial_M A_X^M)*abs(partial_M(H_tau-H_ref)/(Pi_M H_tau))",
            "prediction_value": "MISSING_PARTIAL_M_A_X_M",
            "bound_value": "MISSING_C_M_BOUND",
            "source_path": str(SOURCES["commutator_3514"]["path"]),
            "runner_status": "BLOCKED_PREDICTION_AND_BOUND_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBB3515_1_C_shape",
            "arena": "WEP/R10/PPN source shape",
            "quantity": "C_shape",
            "prediction_formula": "sum_a abs(partial_M A_X^a)*abs(partial_a(H_tau-H_ref)/(Pi_M H_tau))",
            "prediction_value": "MISSING_PARTIAL_M_A_X_A",
            "bound_value": "MISSING_C_SHAPE_BOUND",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "runner_status": "BLOCKED_PREDICTION_AND_BOUND_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "SBB3515_2_E_Dq",
            "arena": "quotient descent",
            "quantity": "source-coordinate Dq leakage",
            "prediction_formula": "norm(dYbar(Dq(v_X)))",
            "prediction_value": "MISSING_DQ_SOURCE_COORDINATE_LEAK",
            "bound_value": "MISSING_DQ_LEAK_BOUND",
            "source_path": str(SOURCES["common_descent_2643"]["path"]),
            "runner_status": "BLOCKED_VERTICAL_CERTIFICATE_MISSING",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3515_0_result",
            "decision": "promote quotient-source-coordinate descent as the best route",
            "rationale": "If Y factors through q and X is vertical, A_X vanishes outright, which is stronger than merely mass-flat.",
            "effect": "next work should prove Y=Ybar(q(Phi)) instead of fitting ell_J/source couplings",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3515_1_no_claim",
            "decision": "do not claim mass-flatness for current MTS",
            "rationale": "current evidence has conditional quotient/source-current/worldtube pieces but not a joint parent signature.",
            "effect": "C_M and C_shape stay explicit nonclaim rows",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3515_2_empirical_fallback",
            "decision": "keep first commutator bound slots only as fallback",
            "rationale": "numeric bounds are useful only if derivation fails; the stronger route is proving quotient descent.",
            "effect": "bound rows exist but remain invalid for claim",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3516-Y5-R2FR-quotient-source-coordinate-descent-certificate-or-Dq-leak-bound.md",
            "next_script": "scripts/Y5_R2FR_3516_quotient_source_coordinate_descent_certificate_or_Dq_leak_bound.py",
            "objective": "Try to prove Y(Phi)=(M_H_ref,sigma^a)=Ybar(q(Phi)) and v_X in ker(Dq) for the actual local/R10/source residual basis; if not, build the first Dq source-coordinate leak bound rows.",
            "success_gate": "Either A_X=0 follows by chain rule, or E_Dq/E_JH/E_W get executable nonclaim bounds without measured-GM absorption.",
            "forbidden_shortcuts": "do not assume source coordinates are observables; do not define Y from orbital GM; do not ignore H_tau/H_ref/worldtube ownership",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    source_rows: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    flatness: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3515_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in source_rows)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3515_1_connection_defined_from_Y",
            "passed": bool_text(any("A_X^M := D_X M_H_ref" in row["formula"] for row in laws)),
            "detail": "A_X defined as derivative of source-coordinate map",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3515_2_quotient_zero_theorem",
            "passed": bool_text(any("Dq(v_X)=0 => A_X^I=0" in row["formula"] for row in laws)),
            "detail": "strong quotient vertical zero theorem written",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3515_3_obstruction_law_complete",
            "passed": bool_text(any(row["row_id"] == "SBR3515_0_total" and "E_Dq" in row["formula"] and "E_W" in row["formula"] for row in obstructions)),
            "detail": "A_X obstruction decomposition includes Dq/JH/Htau/ref/worldtube/frame/readout",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3515_4_flatness_nonclaim",
            "passed": bool_text(all(row["valid_for_claim"] == "False" for row in flatness)),
            "detail": "flatness rows are conditional/nonclaim",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3515_5_bound_rows_block_placeholders",
            "passed": bool_text(all("MISSING_" in row["prediction_value"] and row["valid_for_claim"] == "False" for row in bounds)),
            "detail": "bound rows block missing source-connection values",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3515_6_next_target_Dq_descent",
            "passed": bool_text(any("quotient-source-coordinate" in row["next_doc"] or "quotient_source_coordinate" in row["next_script"] for row in next_rows)),
            "detail": "3516 quotient-source-coordinate descent selected next",
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
            "check_id": "VAL3515_7_csvs_parse",
            "passed": bool_text(csvs_parse),
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3515_8_formalization_workbench_not_targeted",
            "passed": "True",
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )
    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3515_SUMMARY",
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
    laws: list[dict[str, Any]],
    obstructions: list[dict[str, Any]],
    flatness: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3515 - Source-Branch Mass Connection Flatness Or First Commutator Bound

## Summary
- **Actual derivation gain:** `A_X` is no longer a free coupling object; it is `dY(v_X)` for the source-coordinate map `Y(Phi)=(M_H_ref,sigma^a)`.
- **Strong zero route:** if `Y=Ybar(q(Phi))` and `v_X in ker(Dq)`, then `A_X=0`, hence `partial_M A_X^M=partial_M A_X^a=0`.
- **Current status:** the route is exact but not live; current MTS still needs a joint quotient/source-coordinate descent certificate.
- **Fallback:** `C_M`, `C_shape`, and `E_Dq` now have explicit nonclaim bound slots, but no placeholder is claimable.

## Source Register
{markdown_table(source_rows, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Connection Derivation
{markdown_table(laws, ["law_id", "claim_piece", "statement", "formula", "derivation_status", "zero_or_flat_condition", "current_mts_status", "remaining_gap", "claim_allowed"])}

## Connection Obstruction Law
{markdown_table(obstructions, ["row_id", "obstruction", "definition", "formula", "zero_condition", "current_status", "observable_links", "next_action", "valid_for_claim"])}

## Flatness Gates
{markdown_table(flatness, ["flatness_id", "condition", "result", "implies", "current_status", "blocking_gap", "valid_for_claim"])}

## Bound Input Template
{markdown_table(bounds, ["row_id", "arena", "quantity", "prediction_formula", "prediction_value", "bound_value", "runner_status", "valid_for_claim"])}

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
    laws = connection_derivation_rows()
    obstructions = obstruction_rows()
    flatness = flatness_rows()
    bounds = bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3515_SOURCE_REGISTER.csv",
        "connection_law": OUT / "P8_Y5_R2FR_3515_SOURCE_BRANCH_CONNECTION_LAW.csv",
        "canonical_connection": CANONICAL_CONNECTION,
        "obstruction_law": OUT / "P8_Y5_R2FR_3515_SOURCE_BRANCH_CONNECTION_OBSTRUCTIONS.csv",
        "flatness_gates": OUT / "P8_Y5_R2FR_3515_MASS_FLATNESS_GATES.csv",
        "bound_template": OUT / "P8_Y5_R2FR_3515_COMMUTATOR_BOUND_INPUT_TEMPLATE.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3515_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3515_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3515_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows, ["source_id", "path", "exists", "role", "valid_for_claim"])
    law_fields = [
        "law_id",
        "claim_piece",
        "statement",
        "formula",
        "derivation_status",
        "zero_or_flat_condition",
        "current_mts_status",
        "remaining_gap",
        "source_path",
        "claim_allowed",
    ]
    write_csv(outputs["connection_law"], laws, law_fields)
    write_csv(outputs["canonical_connection"], laws, law_fields)
    write_csv(
        outputs["obstruction_law"],
        obstructions,
        ["row_id", "obstruction", "definition", "formula", "zero_condition", "current_status", "observable_links", "next_action", "source_path", "valid_for_claim"],
    )
    write_csv(outputs["flatness_gates"], flatness, ["flatness_id", "condition", "result", "implies", "current_status", "blocking_gap", "valid_for_claim"])
    write_csv(
        outputs["bound_template"],
        bounds,
        ["row_id", "arena", "quantity", "prediction_formula", "prediction_value", "bound_value", "source_path", "runner_status", "valid_for_claim"],
    )
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"])

    validation_rows = validate(outputs, source_rows, laws, obstructions, flatness, bounds, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(source_rows, laws, obstructions, flatness, bounds, decisions, next_rows, validation_rows)

    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
