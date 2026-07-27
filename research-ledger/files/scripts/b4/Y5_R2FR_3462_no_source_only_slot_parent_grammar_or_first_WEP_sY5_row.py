from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3462-Y5-R2FR-no-source-only-slot-parent-grammar-or-first-WEP-sY5-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3462": Path(__file__).resolve(),
    "doc_3461": ROOT / "3461-Y5-R2FR-parent-source-category-label-forgetting-or-sY5-coefficient-fill-under-AX1090.md",
    "sy5_3461": OUT / "P8_Y5_R2FR_3461_SY5_COEFFICIENT_FILL.csv",
    "fill_3461": OUT / "P8_Y5_R2FR_3461_FIRST_FILL_REQUIREMENTS.csv",
    "doc_3460": ROOT / "3460-Y5-R2FR-source-current-owner-for-doublet-or-Y5-source-normalization-bound-under-AX1090.md",
    "bound_3460": OUT / "P8_Y5_R2FR_3460_Y5_BOUND_PLUG_ROWS.csv",
    "doc_3459": ROOT / "3459-Y5-R2FR-response-doublet-energy-identity-source-zero-or-q_loc-bound-under-AX1090.md",
    "residual_3459": OUT / "P8_Y5_R2FR_3459_RESIDUAL_BOUNDS.csv",
    "doc_1065": ROOT / "1065-Y5-R10-no-source-only-slot-parent-grammar-or-first-relative-weight-numeric-row.md",
    "grammar_1065": OUT / "P8_Y5_R10_1065_PARENT_GRAMMAR_AUDIT.csv",
    "wep_schema_1065": OUT / "P8_Y5_R10_1065_FIRST_WEP_NUMERIC_ROW_SCHEMA.csv",
    "wep_product_1065": OUT / "P8_Y5_R10_1065_WEP_RELATIVE_WEIGHT_PRODUCT_CANDIDATE_NONCLAIM.csv",
    "claim_gates_1065": OUT / "P8_Y5_R10_1065_CLAIM_GATES.csv",
    "requirements_1064": OUT / "P8_Y5_R10_1064_NUMERIC_SOURCE_REQUIREMENTS.csv",
    "bound_import_1064": OUT / "P8_Y5_R10_1064_RELATIVE_WEIGHT_BOUND_IMPORT.csv",
    "material_1061": OUT / "P8_Y5_R10_1061_WEP_MATERIAL_CONVENTION.csv",
    "inputs_1061": OUT / "P8_Y5_R10_1061_INPUT_FILL_LEDGER.csv",
    "contract_1055": OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv",
    "counter_1055": OUT / "P8_Y5_R10_1055_COUNTEREXAMPLE_LEDGER.csv",
    "minimal_955": OUT / "P8_Y5_R10_955_MINIMAL_MATTER_ACTION_LEMMA.csv",
    "source_functor_953": OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body: list[str] = []
    for row in rows:
        values = [
            str(row.get(field, ""))
            .replace("\n", "<br>")
            .replace("|", "/")
            for field in fields
        ]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def source_register() -> list[dict[str, Any]]:
    roles = {
        "script_3462": "generator for this checkpoint",
        "doc_3461": "live parent-category/source-weight predecessor",
        "sy5_3461": "s_Y5 coefficient split feeding 3460 and 3459",
        "fill_3461": "first-fill requirement for WEP/source-weight row",
        "doc_3460": "source-current owner and Y5 source-normalization bound",
        "bound_3460": "J_norm and q_loc bound plug rows",
        "doc_3459": "response-doublet energy identity and amplitude bound",
        "residual_3459": "3459 residual-bound rows",
        "doc_1065": "older no-source-only-slot grammar attempt",
        "grammar_1065": "older parent grammar audit rows",
        "wep_schema_1065": "older first WEP numeric row schema",
        "wep_product_1065": "older WEP nonclaim product row",
        "claim_gates_1065": "older claim-gate refusal rows",
        "requirements_1064": "numeric/source requirements for WEP, PPN, Gdot, R10",
        "bound_import_1064": "local empirical bound imports",
        "material_1061": "MICROSCOPE Ti/Pt material convention",
        "inputs_1061": "missing tau_WEP and source-normalization inputs",
        "contract_1055": "parent action contract candidate",
        "counter_1055": "counterexample ledger for source weights",
        "minimal_955": "minimal matter action lemma",
        "source_functor_953": "source functor theorem attempt",
        "local_bounds": "source-backed local bound ledger",
    }
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
        }
        for key, path in SOURCES.items()
    ]


def observable_grammar_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "NSO3462_0_target_theorem",
            "claim": "No source-only species scalar w_A is allowed in the parent matter/source language.",
            "attempt": "derive from observable algebra, quotient descent, covariance, additivity, and local Hilbert source ownership",
            "result": "TARGET_EXACT",
            "derivation_or_obstruction": "If proved, every relative source weight Delta_w_AB is theorem-zero and FFR3461_0 closes without a numeric prior.",
            "source_path": str(SOURCES["fill_3461"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NSO3462_1_observable_algebra_completion",
            "claim": "Observable algebra alone excludes inert gravitational-only coefficients.",
            "attempt": "require every matter coefficient to be visible in nongravitational readout, representation data, or universal geometry",
            "result": "SUFFICIENT_IF_COMPLETENESS_AXIOM_ADDED",
            "derivation_or_obstruction": "The corpus has not proved that the listed observable algebra is complete; a coefficient can be invisible to nongravitational equations yet visible in gravitational source strength.",
            "source_path": str(SOURCES["grammar_1065"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NSO3462_2_covariance_bianchi",
            "claim": "Diffeomorphism covariance and Bianchi identities force all species weights equal.",
            "attempt": "use nabla_mu G^{mu nu}=0 and on-shell conservation to remove relative source prefactors",
            "result": "FAILS_AS_THEOREM",
            "derivation_or_obstruction": "Bianchi requires conservation of the total weighted source, not equality of constant weights; each separately conserved sector can carry a different constant w_A.",
            "source_path": str(SOURCES["bound_3460"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NSO3462_3_action_descent",
            "claim": "Matter-action descent through one observed coframe forbids w_A.",
            "attempt": "write S_matter=sum_A S_A[e_obs,Psi_A,theta_A] and demand a species-blind measure/coframe",
            "result": "PARTIAL_ONLY",
            "derivation_or_obstruction": "Species-blind measure/coframe blocks geometric reintroduction, but a constant multiplier w_A S_A still descends through the same measure unless syntax forbids it.",
            "source_path": str(SOURCES["minimal_955"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NSO3462_4_field_redefinition",
            "claim": "All w_A are removable by field normalization.",
            "attempt": "absorb w_A into Psi_A normalization and measured parameters",
            "result": "NOT_GENERAL",
            "derivation_or_obstruction": "Free equations may hide an overall factor, but interactions, Noether currents, quantum/statistical action weights, composites, and readout conventions can leave a source-only residual.",
            "source_path": str(SOURCES["wep_schema_1065"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NSO3462_5_current_owner_route",
            "claim": "A single Noether/Hilbert stress-current owner would forbid source-only weights.",
            "attempt": "make gravitational source the unique conserved energy-momentum flow of all matter and fields, including EM/Poynting flux, with no separate source selector",
            "result": "BEST_DERIVATION_ROUTE_NOT_YET_CLOSED",
            "derivation_or_obstruction": "This is stronger than abstract grammar: it can kill w_A by ownership, but 3460 still marks the current/source owner as missing.",
            "source_path": str(SOURCES["doc_3460"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NSO3462_6_countermodel_test",
            "claim": "Current primitives already exclude a live countermodel.",
            "attempt": "test against S=S_geo+sum_A w_A S_A[e_obs,Psi_A,theta_A] with constant w_A and the same descended geometry",
            "result": "COUNTERMODEL_SURVIVES",
            "derivation_or_obstruction": "The model is local, covariant, additive, uses one observed coframe, and changes source strength without changing isolated classical matter equations; therefore current axioms do not prove w_A absent.",
            "source_path": str(SOURCES["counter_1055"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "audit_id": "NSO3462_7_verdict",
            "claim": "Derive Delta_w_AB=0 from current no-source-only-slot grammar.",
            "attempt": "close all clauses NSO3462_1 through NSO3462_6 as parent-derived",
            "result": "REJECTED_IN_CURRENT_AXIOM_SET",
            "derivation_or_obstruction": "This is not a vibes-missing result: it is an obstruction. A future parent action must add observable-algebra completeness or a unique source-current owner to forbid w_A.",
            "source_path": str(SOURCES["doc_3461"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def no_go_countermodel() -> list[dict[str, Any]]:
    return [
        {
            "counter_id": "CE3462_0_action",
            "object": "weighted descended matter action",
            "construction": "S_parent = S_geo[q(Phi)] + sum_A w_A S_A[e_obs(q(Phi)), Psi_A, theta_A]",
            "passes": "locality; covariance; additive sectors; one descended coframe; Hilbert variation exists",
            "fails_or_blocks": "universal source coupling and WEP if w_A != w_B",
            "why_it_matters": "It shows covariance/descent/minimal local form alone cannot be the proof of Delta_w_AB=0.",
            "valid_for_claim": False,
        },
        {
            "counter_id": "CE3462_1_eom",
            "object": "isolated matter equations",
            "construction": "delta(w_A S_A)=w_A delta S_A, so classical isolated EOM are unchanged for constant nonzero w_A",
            "passes": "nongravitational readout can miss the coefficient at the classical isolated level",
            "fails_or_blocks": "source strength from delta S/delta g scales by w_A",
            "why_it_matters": "This is the precise source-only loophole the grammar theorem must kill.",
            "valid_for_claim": False,
        },
        {
            "counter_id": "CE3462_2_bianchi",
            "object": "conservation",
            "construction": "if nabla_mu T_A^{mu nu}=0 on shell, then nabla_mu(sum_A w_A T_A^{mu nu})=0 for constant w_A",
            "passes": "Bianchi consistency",
            "fails_or_blocks": "does not imply w_A=w_B",
            "why_it_matters": "Local GR consistency is not enough; equivalence/source universality is an extra ownership theorem.",
            "valid_for_claim": False,
        },
        {
            "counter_id": "CE3462_3_exit",
            "object": "route to defeat the countermodel",
            "construction": "prove source = unique Noether-Hilbert energy-momentum current of the complete observable field algebra, not an independently weighted source map",
            "passes": "would tie matter inertia, EM/Poynting flow, and gravity source to one conserved current",
            "fails_or_blocks": "not yet derived in current corpus",
            "why_it_matters": "The next derivation should target current ownership, not another abstract label-forgetting pass.",
            "valid_for_claim": False,
        },
    ]


def wep_sy5_product_row() -> list[dict[str, Any]]:
    bound = "2.8e-15"
    return [
        {
            "row_id": "WEP3462_0_empirical_bound_anchor",
            "target": "FFR3461_0_WEP_first_row",
            "quantity": "MICROSCOPE Ti/Pt source-charge Eotvos bound",
            "symbol": "eta_TiPt_bound",
            "value_or_status": bound,
            "units": "dimensionless",
            "source_path": str(SOURCES["local_bounds"]),
            "source_row": "R1_WEP_source_charge",
            "source_valid": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "WEP3462_1_material_pair",
            "target": "FFR3461_0_WEP_first_row",
            "quantity": "test-body convention",
            "symbol": "AB",
            "value_or_status": "TA6V_minus_PtRh10",
            "units": "dimensionless convention",
            "source_path": str(SOURCES["material_1061"]),
            "source_row": "MCON1061_0_test_pair",
            "source_valid": True,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "WEP3462_2_delta_w",
            "target": "FFR3461_0_WEP_first_row",
            "quantity": "relative source-weight contrast",
            "symbol": "Delta_w_TiPt",
            "value_or_status": "MISSING_PARENT_THEOREM_ZERO_OR_NUMERIC_PRIOR",
            "units": "dimensionless",
            "source_path": str(SOURCES["doc_3461"]),
            "source_row": "SY5C3461_1_relative_species_weight; FFR3461_0_WEP_first_row",
            "source_valid": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "WEP3462_3_tau_WEP",
            "target": "FFR3461_0_WEP_first_row",
            "quantity": "local lab/source/orbit/readout projection",
            "symbol": "tau_WEP",
            "value_or_status": "MISSING_LAB_SOURCE_ORBIT_PROJECTION",
            "units": "dimensionless",
            "source_path": str(SOURCES["inputs_1061"]),
            "source_row": "INF1061_4_tau_WEP",
            "source_valid": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "WEP3462_4_product",
            "target": "FFR3461_0_WEP_first_row",
            "quantity": "first scoreable s_Y5 relative-source product",
            "symbol": "P_WEP_sY5 = abs(Delta_w_TiPt * tau_WEP)",
            "value_or_status": "MISSING_DELTA_W_TiPt_TIMES_TAU_WEP_PRODUCT",
            "units": "dimensionless",
            "source_path": str(OUT / "P8_Y5_R2FR_3462_WEP_SY5_PRODUCT_ROW.csv"),
            "source_row": "WEP3462_2_delta_w; WEP3462_3_tau_WEP",
            "source_valid": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "row_id": "WEP3462_5_bound_test",
            "target": "FFR3461_0_WEP_first_row",
            "quantity": "nonclaim comparison rule",
            "symbol": "P_WEP_sY5 <= eta_TiPt_bound",
            "value_or_status": "BLOCKED_UNTIL_PRODUCT_NUMERIC_OR_THEOREM_ZERO",
            "units": "dimensionless",
            "source_path": str(SOURCES["requirements_1064"]),
            "source_row": "REQ1064_0_WEP_species",
            "source_valid": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def bound_chain_update() -> list[dict[str, Any]]:
    return [
        {
            "chain_id": "CHAIN3462_0_to_3461",
            "feeds": "FFR3461_0_WEP_first_row",
            "update": "first WEP s_Y5 row is now explicitly instantiated in the live R2FR chain",
            "formula": "P_WEP_sY5 = abs(Delta_w_TiPt * tau_WEP)",
            "current_status": "SCHEMA_FILLED_PRODUCT_MISSING",
            "remaining_input": "Delta_w_TiPt theorem-zero or numeric prior; tau_WEP projection",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3462_1_to_3460",
            "feeds": "Y5B3460_0_source_work_norm",
            "update": "Delta_w_TiPt is one concrete component of the C_w ||Delta_w|| source-work term",
            "formula": "J_norm <= C_Y5 ||s_Y5|| + C_w ||Delta_w|| + Q_nonH + Q_boundary_source + Q_domain_source + Q_range + Q_time",
            "current_status": "BOUND_FORM_READY_INPUTS_MISSING",
            "remaining_input": "map P_WEP_sY5 back to ||Delta_w|| through tau_WEP, or prove Delta_w=0",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3462_2_to_3459",
            "feeds": "RDB3459_0_Z_amplitude",
            "update": "source-current residual controls the response-doublet amplitude",
            "formula": "||Z|| <= (J_norm + sqrt(J_norm^2 + 4 lambda_min |B_flux|))/(2 lambda_min)",
            "current_status": "AMPLITUDE_BOUND_FORMAL_NOT_ZERO",
            "remaining_input": "J_norm theorem-zero or numeric upper bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "chain_id": "CHAIN3462_3_to_q_loc",
            "feeds": "RDB3459_1_q_loc_Hilbert_branch",
            "update": "q_loc suppression cannot be promoted until source-current residual is owned or bounded",
            "formula": "Q_q_loc <= N_P[J_norm + Q_boundary_flux] + Q_DeltaK",
            "current_status": "LOCAL_GR_BRANCH_STILL_GATED",
            "remaining_input": "single source-current owner, no-boundary source flux, and K_hat/Hilbert closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def refusal_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "RG3462_0_no_theorem_promotion",
            "forbidden_shortcut": "declare Delta_w_TiPt=0 because source-only weights look ugly",
            "reason": "the countermodel survives current axioms",
            "required_to_open": "observable-algebra completeness theorem or unique source-current owner",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "RG3462_1_no_tau_unity",
            "forbidden_shortcut": "set tau_WEP=1 by convention",
            "reason": "tau_WEP is the lab/source/orbit/readout projection, not a unit choice",
            "required_to_open": "local projection derivation with material/source map",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "RG3462_2_no_measured_G_absorption",
            "forbidden_shortcut": "absorb relative source weights into measured G",
            "reason": "measured G can absorb only a common universal range/time/species/frame independent normalization",
            "required_to_open": "prove w_A=w_common for all species or score the residual as WEP/PPN/R10",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "RG3462_3_no_cancellation_claim",
            "forbidden_shortcut": "use signed cancellation between materials or hidden channels",
            "reason": "first WEP row uses an absolute product and must not hide source defects in cancellations",
            "required_to_open": "numeric absolute product with source paths or a theorem-zero",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "RG3462_4_no_local_GR_claim",
            "forbidden_shortcut": "claim q_loc -> 0 from this checkpoint",
            "reason": "3462 provides a no-go obstruction and nonclaim WEP schema, not a source-zero proof",
            "required_to_open": "close current ownership/source residuals and boundary/domain gates feeding 3459",
            "gate_pass": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3462_0_grammar_attempt",
            "decision": "Reject no-source-only-slot as derivable from the current abstract grammar alone.",
            "because": "The weighted descended action countermodel is local, covariant, additive, conserved, and uses one coframe while retaining Delta_w_AB.",
            "next_action": "Stop repeating label-forgetting. Derive a unique source-current owner or add a real observable-algebra completeness theorem.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3462_1_wep_row",
            "decision": "Instantiate the first WEP s_Y5 product row as nonclaim live chain data.",
            "because": "FFR3461_0 now has explicit bound, material convention, Delta_w, tau_WEP, and product slots feeding 3460 and 3459.",
            "next_action": "Either prove Delta_w_TiPt=0 by source-current ownership or derive tau_WEP and a numeric Delta_w prior width.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3462_2_best_route",
            "decision": "The best forward attack is a single-source-current derivation, not another missing-row sweep.",
            "because": "If the parent source is the unique Noether/Hilbert stress-energy flow of matter plus fields, including EM/Poynting energy flux, w_A has no independent slot.",
            "next_action": "3463 should attack source-current ownership from Noether/Hilbert/Poynting flow and use WEP/tau only as the fallback bound branch.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3463-Y5-R2FR-single-source-current-owner-from-Noether-Poynting-flow-or-WEP-tau-map-under-AX1090.md",
            "next_script": "scripts/Y5_R2FR_3463_single_source_current_owner_from_Noether_Poynting_flow_or_WEP_tau_map.py",
            "objective": "Try to derive the universal source coupling by making gravity couple to the unique conserved energy-momentum flow of all parent fields, including EM/Poynting stress; if that fails, derive the WEP tau projection and keep the first product row nonclaim.",
            "success_gate": "Either Delta_w_AB is theorem-zero because there is no independent source selector beyond the unique stress-current, or P_WEP_sY5 receives sourced Delta_w/tau inputs with units and refusal gates.",
            "exclude": "new GitHub action; formalization-workbench edits; setting tau_WEP=1; absorbing relative weights into measured G; local-GR/WEP claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validate(paths: dict[str, Path], datasets: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    stamp = now()

    sources = datasets["source_register"]
    missing_sources = [row["source_id"] for row in sources if not row["exists"]]
    checks.append(
        {
            "check_id": "VAL3462_0_sources_exist",
            "passed": not missing_sources,
            "detail": f"{len(sources) - len(missing_sources)}/{len(sources)} source paths exist; missing={';'.join(missing_sources) or 'none'}",
            "timestamp_utc": stamp,
        }
    )

    grammar = datasets["observable_grammar_audit"]
    result_map = {row["audit_id"]: row["result"] for row in grammar}
    checks.append(
        {
            "check_id": "VAL3462_1_grammar_no_go_recorded",
            "passed": result_map.get("NSO3462_6_countermodel_test") == "COUNTERMODEL_SURVIVES"
            and result_map.get("NSO3462_7_verdict") == "REJECTED_IN_CURRENT_AXIOM_SET",
            "detail": ";".join(f"{key}={value}" for key, value in result_map.items()),
            "timestamp_utc": stamp,
        }
    )

    counter = datasets["no_go_countermodel"]
    checks.append(
        {
            "check_id": "VAL3462_2_countermodel_constructed",
            "passed": any("sum_A w_A S_A" in str(row.get("construction", "")) for row in counter)
            and any(
                "bianchi" in str(row.get("why_it_matters", "")).lower()
                or "conservation" in str(row.get("object", "")).lower()
                for row in counter
            ),
            "detail": ";".join(row["counter_id"] for row in counter),
            "timestamp_utc": stamp,
        }
    )

    wep = datasets["wep_sy5_product_row"]
    wep_symbols = {row["symbol"] for row in wep}
    all_wep_nonclaim = all(str(row["valid_for_claim"]).lower() == "false" for row in wep)
    checks.append(
        {
            "check_id": "VAL3462_3_wep_product_schema_nonclaim",
            "passed": "P_WEP_sY5 = abs(Delta_w_TiPt * tau_WEP)" in wep_symbols
            and all_wep_nonclaim
            and any(row["value_or_status"] == "2.8e-15" for row in wep),
            "detail": ";".join(f"{row['row_id']}={row['value_or_status']}" for row in wep),
            "timestamp_utc": stamp,
        }
    )

    gates = datasets["refusal_gates"]
    checks.append(
        {
            "check_id": "VAL3462_4_refusal_gates_closed",
            "passed": len(gates) >= 5 and all(str(row["gate_pass"]).lower() == "false" for row in gates),
            "detail": ";".join(row["gate_id"] for row in gates),
            "timestamp_utc": stamp,
        }
    )

    chain = datasets["bound_chain_update"]
    checks.append(
        {
            "check_id": "VAL3462_5_chain_feeds_3461_3460_3459",
            "passed": any("FFR3461_0" in row["feeds"] for row in chain)
            and any("Y5B3460_0" in row["feeds"] for row in chain)
            and any("RDB3459_0" in row["feeds"] for row in chain),
            "detail": ";".join(f"{row['chain_id']}->{row['feeds']}" for row in chain),
            "timestamp_utc": stamp,
        }
    )

    claim_rows = [
        row
        for rows in datasets.values()
        for row in rows
        if str(row.get("valid_for_claim", "")).lower() == "true"
        or str(row.get("claim_allowed", "")).lower() == "true"
    ]
    checks.append(
        {
            "check_id": "VAL3462_6_no_claim_rows",
            "passed": not claim_rows,
            "detail": f"claim_like_rows={len(claim_rows)}",
            "timestamp_utc": stamp,
        }
    )

    parse_details: list[str] = []
    parse_ok = True
    for name, path in paths.items():
        if path.suffix.lower() == ".csv":
            if name == "validation" and not path.exists():
                parse_details.append(f"{path.name}:pending_write")
                continue
            try:
                parse_details.append(f"{path.name}:{len(read_csv(path))}")
            except Exception as exc:  # pragma: no cover - validation output
                parse_ok = False
                parse_details.append(f"{path.name}:PARSE_FAIL:{exc}")
    checks.append(
        {
            "check_id": "VAL3462_7_csv_parse",
            "passed": parse_ok,
            "detail": ";".join(parse_details),
            "timestamp_utc": stamp,
        }
    )

    formalization_has_outputs = any(FORMALIZATION.rglob("*3462*")) if FORMALIZATION.exists() else False
    checks.append(
        {
            "check_id": "VAL3462_8_formalization_untouched_by_3462",
            "passed": not formalization_has_outputs,
            "detail": f"formalization_exists={FORMALIZATION.exists()}; 3462_outputs_in_formalization={formalization_has_outputs}",
            "timestamp_utc": stamp,
        }
    )

    next_rows = datasets["next_target"]
    checks.append(
        {
            "check_id": "VAL3462_9_next_target_3463",
            "passed": len(next_rows) == 1 and "single-source-current" in next_rows[0]["next_doc"],
            "detail": next_rows[0]["next_doc"],
            "timestamp_utc": stamp,
        }
    )

    overall = all(row["passed"] for row in checks)
    checks.append(
        {
            "check_id": "VAL3462_SUMMARY",
            "passed": overall,
            "detail": "PASS" if overall else "FAIL",
            "timestamp_utc": stamp,
        }
    )
    return checks


def write_doc(datasets: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3462 - No-Source-Only-Slot Parent Grammar Or First WEP sY5 Row Under AX1090",
        "",
        "**Current verdict:** the no-source-only-slot grammar does not derive from the current abstract primitives. This is now a no-go obstruction, not just a missing-input vibe: a weighted descended action with constant `w_A` survives locality, covariance, additivity, one-coframe descent, and Bianchi conservation.",
        "",
        "**Useful progress:** the exact route forward is sharper. Either prove a unique source-current owner for all matter/field energy flow, including EM/Poynting stress, or keep `Delta_w_AB` as a finite WEP/PPN/R10 residual. The first live WEP `s_Y5` product row is instantiated but remains nonclaim.",
        "",
        "## Source Register",
        md_table(datasets["source_register"]),
        "",
        "## Observable Grammar Derivation Audit",
        md_table(datasets["observable_grammar_audit"]),
        "",
        "## No-Go Countermodel",
        md_table(datasets["no_go_countermodel"]),
        "",
        "## First WEP sY5 Product Row",
        md_table(datasets["wep_sy5_product_row"]),
        "",
        "## Bound Chain Update",
        md_table(datasets["bound_chain_update"]),
        "",
        "## Refusal Gates",
        md_table(datasets["refusal_gates"]),
        "",
        "## Decision Ledger",
        md_table(datasets["decision_ledger"]),
        "",
        "## Validation",
        md_table(datasets["validation"]),
        "",
        "## Next Target",
        md_table(datasets["next_target"]),
        "",
        "## Bottom Line",
        "",
        "- The current grammar path cannot honestly claim `Delta_w_AB=0`; the countermodel blocks it.",
        "- The work did move forward: the blocker is now mathematically localized to source-current ownership, not generic category-label forgetting.",
        "- The best next derivation is to make gravity couple to the unique conserved stress-current of the parent fields; if that succeeds, source-only `w_A` has nowhere to live.",
        "- Until then, WEP/PPN/R10 rows remain nonclaim finite-residual branches.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    paths = {
        "source_register": OUT / "P8_Y5_R2FR_3462_SOURCE_REGISTER.csv",
        "observable_grammar_audit": OUT / "P8_Y5_R2FR_3462_OBSERVABLE_GRAMMAR_DERIVATION_AUDIT.csv",
        "no_go_countermodel": OUT / "P8_Y5_R2FR_3462_NO_GO_COUNTERMODEL.csv",
        "wep_sy5_product_row": OUT / "P8_Y5_R2FR_3462_WEP_SY5_PRODUCT_ROW.csv",
        "bound_chain_update": OUT / "P8_Y5_R2FR_3462_BOUND_CHAIN_UPDATE.csv",
        "refusal_gates": OUT / "P8_Y5_R2FR_3462_REFUSAL_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3462_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3462_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3462_VALIDATION.csv",
    }
    datasets = {
        "source_register": source_register(),
        "observable_grammar_audit": observable_grammar_audit(),
        "no_go_countermodel": no_go_countermodel(),
        "wep_sy5_product_row": wep_sy5_product_row(),
        "bound_chain_update": bound_chain_update(),
        "refusal_gates": refusal_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
    }
    for key, rows in datasets.items():
        write_csv(paths[key], rows)
    datasets["validation"] = validate(paths, datasets)
    write_csv(paths["validation"], datasets["validation"])
    write_doc(datasets)


if __name__ == "__main__":
    main()
