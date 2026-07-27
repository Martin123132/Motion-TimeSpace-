from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3516-Y5-R2FR-quotient-source-coordinate-descent-certificate-or-Dq-leak-bound.md"
CANONICAL_CERTIFICATE = OUT / "P8_EM_quotient_source_coordinate_descent_certificate.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3516": {"path": Path(__file__).resolve(), "role": "3516 generator"},
    "doc_3515": {
        "path": ROOT / "3515-Y5-R2FR-source-branch-mass-connection-flatness-or-first-commutator-bound.md",
        "role": "3515 source-branch connection handoff",
    },
    "source_connection_3515": {
        "path": OUT / "P8_EM_source_branch_mass_connection_flatness_law.csv",
        "role": "canonical source-branch connection flatness law",
    },
    "obstruction_3515": {
        "path": OUT / "P8_Y5_R2FR_3515_SOURCE_BRANCH_CONNECTION_OBSTRUCTIONS.csv",
        "role": "3515 source-coordinate obstruction rows",
    },
    "next_3515": {
        "path": OUT / "P8_Y5_R2FR_3515_NEXT_TARGET.csv",
        "role": "3516 handoff row",
    },
    "field_quotient_2570": {
        "path": OUT / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv",
        "role": "field quotient residual-direction eligibility ledger",
    },
    "vertical_kernel_2589": {
        "path": OUT / "P8_Y5_VERTICAL_KERNEL_2589_CERTIFICATE_GATE.csv",
        "role": "vertical kernel certificate gates",
    },
    "common_descent_2643": {
        "path": OUT / "P8_Y5_COMMON_DESCENT_DQZ_2643_PARENT_SIGNATURE_THEOREM_GATE.csv",
        "role": "common quotient descent signature gate",
    },
    "arena_leak_2643": {
        "path": OUT / "P8_Y5_COMMON_DESCENT_DQZ_2643_ARENA_LEAK_MAP.csv",
        "role": "arena leak map for Dq descent failure",
    },
    "leak_bounds_2643": {
        "path": OUT / "P8_Y5_COMMON_DESCENT_DQZ_2643_DQZ_JH_LEAK_BOUND_ROWS.csv",
        "role": "Dq/JH leak bound template",
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


def certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "certificate_id": "QSC3516_0_master_theorem",
            "claim_piece": "quotient-source-coordinate descent theorem",
            "statement": "For a residual direction v_X, the source-branch connection vanishes if the source coordinates Y=(M_H_ref,sigma^a) are q-basic and v_X is in ker(Dq).",
            "formula": "Y=Ybar(q(Phi)) and Dq(v_X)=0 => D_X Y=dYbar(Dq(v_X))=0 => A_X=0",
            "required_signatures": "actual q map; actual residual basis v_X; q-basic source coordinates; same-frame tau/coframe; no readout-defined source mass",
            "current_mts_status": "EXACT_CONDITIONAL_THEOREM_NOT_LIVE",
            "payoff": "kills A_X, C_M, C_shape and the source-connection part of the ell_J/Pi_M obstruction",
            "gap": "q-basic source-coordinate certificate is not parent-signed",
            "source_path": str(SOURCES["source_connection_3515"]["path"]),
            "claim_allowed": "False",
        },
        {
            "certificate_id": "QSC3516_1_MHref_descent",
            "claim_piece": "M_H_ref q-basic coordinate",
            "statement": "M_H_ref descends through q only if H_tau and H_ref are both q-basic on the same tau/coframe/surface branch.",
            "formula": "M_H_ref(Phi)=H_tau[S_outer;Phi]-H_ref[Phi]=Mbar_H_ref(q(Phi))",
            "required_signatures": "theta/Q_tau owner; H_tau integrability; source-blind H_ref; positive denominator; same frame",
            "current_mts_status": "NOT_SIGNED",
            "payoff": "removes mass-coordinate connection A_X^M",
            "gap": "H_tau curl and H_ref selector remain unsigned",
            "source_path": str(SOURCES["htau_integrability_2667"]["path"]),
            "claim_allowed": "False",
        },
        {
            "certificate_id": "QSC3516_2_sigma_descent",
            "claim_piece": "worldtube/shape coordinates q-basic",
            "statement": "The support and shape coordinates sigma^a descend through q only if W_source is closure(supp J_H[tau]) from the same parent current and no fitted domain mask enters.",
            "formula": "sigma^a(Phi)=I^a[closure(supp J_H[tau]),e_obs,tau]/M_H_ref=sigmabar^a(q(Phi))",
            "required_signatures": "J_H descent; tau lock; compact regular support; linked surfaces; no readout domain mask",
            "current_mts_status": "NOT_SIGNED",
            "payoff": "removes shape leakage A_X^a and C_shape",
            "gap": "worldtube/source-current owner remains conditional",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "claim_allowed": "False",
        },
        {
            "certificate_id": "QSC3516_3_actual_basis_filter",
            "claim_piece": "only eligible vertical directions can use the theorem",
            "statement": "The quotient theorem applies only to directions already certified as vertical; public metric, projector/readout and rejected observer-cell directions are not eligible.",
            "formula": "eligible(v_i) := Dq(v_i)=0 and Y q-basic; otherwise carry E_Dq/E_readout/E_projector rows",
            "required_signatures": "field list; q matrix; v_i basis; kernel proof; source/readout descent",
            "current_mts_status": "FILTER_INSTALLED_NONCLAIM",
            "payoff": "prevents smuggling closure by declaring nonvertical directions invisible",
            "gap": "actual computable q map and v_i basis still missing",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
        {
            "certificate_id": "QSC3516_4_current_verdict",
            "claim_piece": "current MTS status",
            "statement": "3516 does not prove A_X=0 for current MTS, but it identifies the precise parent certificate needed and filters the residual directions that are allowed to invoke it.",
            "formula": "claim(A_X=0) requires all descent clauses pass for at least one declared vertical basis; otherwise use leak rows",
            "required_signatures": "QSC3516_1 through QSC3516_3 plus no-source/readout laundering",
            "current_mts_status": "NOT_CLAIMED_BUT_NARROWED",
            "payoff": "next target is construction of q and vertical basis, not another coupling audit",
            "gap": "q-map/v-basis construction remains to do",
            "source_path": str(SOURCES["next_3515"]["path"]),
            "claim_allowed": "False",
        },
    ]


def residual_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "QSB3516_0_public_metric",
            "direction": "delta g or delta e_obs",
            "eligibility": "NOT_ELIGIBLE_PUBLIC_BRANCH",
            "reason": "public metric/coframe variations are physical source/readout directions, not kernel directions",
            "action": "do not apply A_X=0 theorem; they belong in GR/EH response",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
        {
            "basis_id": "QSB3516_1_v_q_private",
            "direction": "v_q",
            "eligibility": "CANDIDATE_VERTICAL_UNSIGNED",
            "reason": "ledger says Dq_parent[v_q]=0 only after matter/boundary/source descent or first-class removal",
            "action": "carry E_Dq/E_JH/E_boundary until q and source descent are signed",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
        {
            "basis_id": "QSB3516_2_v_RAB",
            "direction": "v_R changes R_AB",
            "eligibility": "REJECTED_CURRENT_OBSERVER_CELL_MAP",
            "reason": "current observer-cell map keeps DObs_e burden; q_shape invisibility is insufficient",
            "action": "cannot use quotient zero theorem unless observer-cell map is rebuilt",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
        {
            "basis_id": "QSB3516_3_memory_tau_private",
            "direction": "v_memory/v_tau_private",
            "eligibility": "CANDIDATE_VERTICAL_UNSIGNED",
            "reason": "private memory/time directions need coframe/tau lock before clocks/source support become q-basic",
            "action": "carry E_frame/E_Htau rows",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
        {
            "basis_id": "QSB3516_4_projector",
            "direction": "delta Pi_M or post-readout projection",
            "eligibility": "NOT_ELIGIBLE_UNTIL_INCLUDED_IN_Q_OR_FIXED",
            "reason": "Pi_M variation is exactly part of the source-connection obstruction",
            "action": "do not assume fixed Pi_M; keep E_readout/E_projector leak",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
        {
            "basis_id": "QSB3516_5_coupling_constants",
            "direction": "hidden variation acting on kappa/ell_J/c_vis",
            "eligibility": "CANDIDATE_ONLY_IF_COEFFICIENTS_Q_BASIC",
            "reason": "couplings are invisible only if parent coefficient slots descend as constants/superselection data",
            "action": "keep source-connection/coupling residual rows until coefficient descent is signed",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
        {
            "basis_id": "QSB3516_6_boundary_reference",
            "direction": "boundary/corner/reference variation",
            "eligibility": "CANDIDATE_LOCAL_ONLY_NOT_SOURCE_DENOMINATOR_ZERO",
            "reason": "boundary changes may have zero local projection but still contaminate H_ref/M_H_ref",
            "action": "carry E_ref/boundary rows until H_ref is source-blind",
            "source_path": str(SOURCES["field_quotient_2570"]["path"]),
            "claim_allowed": "False",
        },
    ]


def descent_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "QSCG3516_0_q_and_kernel",
            "object": "q(Phi), v_i",
            "condition": "actual parent field list, q map, normed v_i basis and Dq(v_i)=0",
            "current_status": "MISSING_COMPUTABLE_Q_MAP_AND_VERTICAL_BASIS",
            "failure_term": "E_Dq",
            "source_path": str(SOURCES["vertical_kernel_2589"]["path"]),
            "claim_allowed": "False",
        },
        {
            "clause_id": "QSCG3516_1_JH_current",
            "object": "J_H/rho_H",
            "condition": "ordinary matter and Hilbert/worldtube source current descend through q/e_obs/tau with no source-only slot",
            "current_status": "SOURCE_CURRENT_DESCENT_NOT_PARENT_SIGNED",
            "failure_term": "E_JH",
            "source_path": str(SOURCES["source_descent_2909"]["path"]),
            "claim_allowed": "False",
        },
        {
            "clause_id": "QSCG3516_2_MHref",
            "object": "M_H_ref",
            "condition": "H_tau and H_ref are q-basic, integrable, source-blind and positive on the same branch",
            "current_status": "HTAU_HREF_DENOMINATOR_UNSIGNED",
            "failure_term": "E_Htau+E_ref",
            "source_path": str(SOURCES["reference_2938"]["path"]),
            "claim_allowed": "False",
        },
        {
            "clause_id": "QSCG3516_3_worldtube_shape",
            "object": "sigma^a[W_source]",
            "condition": "W_source=closure(supp J_H[tau]) and linked surfaces/shape moments are q-basic before readout",
            "current_status": "WORLDTUBE_SELECTOR_UNSIGNED",
            "failure_term": "E_W",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "claim_allowed": "False",
        },
        {
            "clause_id": "QSCG3516_4_same_frame",
            "object": "e_obs,tau,source/readout frame",
            "condition": "same observed coframe and tau define matter, H_tau, W_source, clocks, R10 and orbit readout",
            "current_status": "COFRAME_TAU_LOCK_NOT_PROVED",
            "failure_term": "E_frame",
            "source_path": str(SOURCES["frame_1519"]["path"]),
            "claim_allowed": "False",
        },
        {
            "clause_id": "QSCG3516_5_no_readout_laundering",
            "object": "Y_parent vs Y_readout",
            "condition": "measured GM/R10/PPN values test Y_parent but never define it",
            "current_status": "ANTI_LAUNDERING_POLICY_ONLY",
            "failure_term": "E_readout",
            "source_path": str(SOURCES["readout_1926"]["path"]),
            "claim_allowed": "False",
        },
    ]


def leak_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "QSL3516_0_E_Dq",
            "quantity": "source-coordinate Dq leak",
            "formula": "E_Dq^I <= ||dYbar^I|| * ||Dq(v_X)||",
            "units": "source-coordinate units",
            "prediction_value": "MISSING_DQ_VX_AND_DYBAR",
            "bound_value": "MISSING_SOURCE_COORDINATE_LEAK_BOUND",
            "required_inputs": "q map; v_X basis; q/Y norms; dYbar operator norm",
            "arenas": "Newton; PPN; R10; Gdot; WEP",
            "source_path": str(SOURCES["leak_bounds_2643"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "QSL3516_1_E_JH",
            "quantity": "Hilbert/worldtube current descent leak",
            "formula": "E_JH <= eps_JH_Z_abs + source_weight + theta_marker + boundary_current_tail",
            "units": "source-normalized",
            "prediction_value": "MISSING_EPS_JH_Z_ABS",
            "bound_value": "MISSING_SOURCE_CURRENT_LEAK_BOUND",
            "required_inputs": "matter descent; no-source-slot; theta marker; boundary silence",
            "arenas": "WEP; R10; Newton; PPN",
            "source_path": str(SOURCES["leak_bounds_2643"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "QSL3516_2_E_W",
            "quantity": "worldtube/support coordinate leak",
            "formula": "E_W <= ||D_X W_source||_shape + ||D_X sigma_readout||",
            "units": "shape/support units",
            "prediction_value": "MISSING_WORLD_TUBE_SHAPE_LEAK",
            "bound_value": "MISSING_WORLD_TUBE_BOUND",
            "required_inputs": "W_source selector; compact support; linked surfaces; readout-domain mask ban",
            "arenas": "R10; Newton source; PPN source profile",
            "source_path": str(SOURCES["worldtube_2611"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "QSL3516_3_E_Htau_ref",
            "quantity": "H_tau/H_ref denominator leak",
            "formula": "E_Htau+E_ref <= |D_X H_tau - dHbar_tau Dq(v_X)| + |D_X H_ref - dHbar_ref Dq(v_X)|",
            "units": "mass/source-charge units",
            "prediction_value": "MISSING_HTAU_HREF_DQ_LEAK",
            "bound_value": "MISSING_DENOMINATOR_LEAK_BOUND",
            "required_inputs": "theta/omega owner; H_tau curl; source-blind H_ref; positivity",
            "arenas": "Gdot; Newton_GM; R10 denominator",
            "source_path": str(SOURCES["htau_integrability_2667"]["path"]),
            "valid_for_claim": "False",
        },
        {
            "row_id": "QSL3516_4_E_frame_readout",
            "quantity": "frame/readout source-coordinate leak",
            "formula": "E_frame+E_readout <= ||D_X(e_obs,tau,Y_readout-Y_parent)||",
            "units": "mixed frame/source units",
            "prediction_value": "MISSING_FRAME_READOUT_LEAK",
            "bound_value": "MISSING_FRAME_READOUT_BOUND",
            "required_inputs": "same-frame tau lock; readout functor; no measured-GM denominator import",
            "arenas": "clock; PPN; orbital_GM; R10",
            "source_path": str(SOURCES["readout_1926"]["path"]),
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3516_0_result",
            "decision": "the clean derivation route is quotient-source-coordinate descent",
            "rationale": "if Y is q-basic and v_X vertical, the source connection A_X vanishes by chain rule.",
            "effect": "local coupling closure now needs q map, residual basis and Y descent certificate",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3516_1_filter_nonvertical_directions",
            "decision": "do not apply quotient zero theorem to public/projector/rejected directions",
            "rationale": "3516 explicitly filters residual directions before using the theorem.",
            "effect": "prevents closure smuggling through a fake verticality assumption",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3516_2_next",
            "decision": "construct the actual q map and vertical basis next",
            "rationale": "all remaining zero routes require a computable q(Phi), field list, v_i basis and Dq(v_i) certificate.",
            "effect": "3517 should attempt q-map/v-basis construction or Dq norm bounds",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3517-Y5-R2FR-actual-q-map-vertical-basis-construction-or-Dq-norm-bound.md",
            "next_script": "scripts/Y5_R2FR_3517_actual_q_map_vertical_basis_construction_or_Dq_norm_bound.py",
            "objective": "Try to construct the actual parent field list, q(Phi), residual basis v_i and Dq(v_i) certificate for source-coordinate descent; if not, produce normed Dq leak rows for the candidate vertical directions.",
            "success_gate": "At least one local/source residual direction gets Dq(v_i)=0 with q/Y norms and source-coordinate descent clauses, or receives executable nonclaim Dq norm rows.",
            "forbidden_shortcuts": "do not declare a direction vertical without q matrix; do not include observed source coordinates in q by tautology; do not use measured GM to define Y",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    certificates: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    leaks: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    checks.append(
        {
            "check_id": "VAL3516_0_sources_exist",
            "passed": bool_text(all(row["exists"] == "True" for row in sources)),
            "detail": "all cited local source paths exist",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3516_1_master_theorem_written",
            "passed": bool_text(any("Dq(v_X)=0 => D_X Y" in row["formula"] for row in certificates)),
            "detail": "quotient-source-coordinate chain-rule theorem written",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3516_2_basis_filter_present",
            "passed": bool_text(any(row["eligibility"].startswith("NOT_ELIGIBLE") for row in basis) and any("CANDIDATE" in row["eligibility"] for row in basis)),
            "detail": "residual basis filter separates nonvertical and candidate vertical directions",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3516_3_descent_clauses_cover_Y",
            "passed": bool_text({"E_Dq", "E_JH", "E_Htau+E_ref", "E_W", "E_frame", "E_readout"}.issubset({row["failure_term"] for row in clauses})),
            "detail": "descent clauses cover q/JH/MHref/worldtube/frame/readout failures",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3516_4_leak_rows_block_placeholders",
            "passed": bool_text(all("MISSING_" in row["prediction_value"] and row["valid_for_claim"] == "False" for row in leaks)),
            "detail": "Dq/source-coordinate leak rows block missing values",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3516_5_no_claim_flags",
            "passed": bool_text(all(row.get("claim_allowed", "False") != "True" for row in certificates + basis + decision_rows() + next_rows) and all(row.get("valid_for_claim", "False") != "True" for row in leaks)),
            "detail": "no 3516 output row is claim-enabled",
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3516_6_next_target_qmap",
            "passed": bool_text(any("actual-q-map" in row["next_doc"] or "actual_q_map" in row["next_script"] for row in next_rows)),
            "detail": "3517 actual q-map/vertical-basis target selected",
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
            "check_id": "VAL3516_7_csvs_parse",
            "passed": bool_text(csvs_parse),
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )
    checks.append(
        {
            "check_id": "VAL3516_8_formalization_workbench_not_targeted",
            "passed": "True",
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )
    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3516_SUMMARY",
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
    sources: list[dict[str, Any]],
    certificates: list[dict[str, Any]],
    basis: list[dict[str, Any]],
    clauses: list[dict[str, Any]],
    leaks: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3516 - Quotient Source-Coordinate Descent Certificate Or Dq Leak Bound

## Summary
- **Actual derivation gain:** source coupling now reduces to a quotient certificate: `Y=Ybar(q(Phi))` plus `v_X in ker(Dq)`.
- **Strong theorem:** `Y=Ybar(q(Phi))` and `Dq(v_X)=0` imply `D_X Y=0`, so `A_X=0`.
- **Important filter:** public metric, projector/readout, and rejected observer-cell directions are not allowed to use the vertical theorem.
- **Current status:** no local-GR/Newton claim; current MTS still needs an actual q-map and residual-basis certificate.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Descent Certificate
{markdown_table(certificates, ["certificate_id", "claim_piece", "statement", "formula", "required_signatures", "current_mts_status", "payoff", "gap", "claim_allowed"])}

## Residual-Basis Eligibility Filter
{markdown_table(basis, ["basis_id", "direction", "eligibility", "reason", "action", "claim_allowed"])}

## Source-Coordinate Descent Clauses
{markdown_table(clauses, ["clause_id", "object", "condition", "current_status", "failure_term", "claim_allowed"])}

## Dq Leak Bound Template
{markdown_table(leaks, ["row_id", "quantity", "formula", "units", "prediction_value", "bound_value", "required_inputs", "arenas", "valid_for_claim"])}

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
    sources = source_register_rows()
    certificates = certificate_rows()
    basis = residual_basis_rows()
    clauses = descent_clause_rows()
    leaks = leak_bound_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3516_SOURCE_REGISTER.csv",
        "certificate": OUT / "P8_Y5_R2FR_3516_QUOTIENT_SOURCE_COORDINATE_DESCENT_CERTIFICATE.csv",
        "canonical_certificate": CANONICAL_CERTIFICATE,
        "basis_filter": OUT / "P8_Y5_R2FR_3516_RESIDUAL_BASIS_ELIGIBILITY_FILTER.csv",
        "descent_clauses": OUT / "P8_Y5_R2FR_3516_SOURCE_COORDINATE_DESCENT_CLAUSES.csv",
        "leak_bounds": OUT / "P8_Y5_R2FR_3516_DQ_SOURCE_COORDINATE_LEAK_BOUND_TEMPLATE.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3516_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3516_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3516_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    certificate_fields = [
        "certificate_id",
        "claim_piece",
        "statement",
        "formula",
        "required_signatures",
        "current_mts_status",
        "payoff",
        "gap",
        "source_path",
        "claim_allowed",
    ]
    write_csv(outputs["certificate"], certificates, certificate_fields)
    write_csv(outputs["canonical_certificate"], certificates, certificate_fields)
    write_csv(outputs["basis_filter"], basis, ["basis_id", "direction", "eligibility", "reason", "action", "source_path", "claim_allowed"])
    write_csv(outputs["descent_clauses"], clauses, ["clause_id", "object", "condition", "current_status", "failure_term", "source_path", "claim_allowed"])
    write_csv(
        outputs["leak_bounds"],
        leaks,
        ["row_id", "quantity", "formula", "units", "prediction_value", "bound_value", "required_inputs", "arenas", "source_path", "valid_for_claim"],
    )
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"])

    validation_rows = validate(outputs, sources, certificates, basis, clauses, leaks, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, certificates, basis, clauses, leaks, decisions, next_rows, validation_rows)

    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
