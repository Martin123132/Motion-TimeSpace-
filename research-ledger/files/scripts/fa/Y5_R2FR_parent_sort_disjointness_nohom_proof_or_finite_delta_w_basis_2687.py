from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2687"
BRANCH_ID = "Y5_R2FR_PARENT_SORT_DISJOINTNESS_NOHOM_PROOF_OR_FINITE_DELTA_W_BASIS_2687"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"

DOC_PATH = ROOT / "2687-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-delta-w-basis.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2687_SOURCE_REGISTER.csv",
    "nohom_attempt": RESIDUALS / "P8_Y5_R2FR_2687_NOHOM_PROOF_ATTEMPT.csv",
    "nohom_gate": RESIDUALS / "P8_Y5_R2FR_2687_NOHOM_GATE.csv",
    "finite_basis": RESIDUALS / "P8_Y5_R2FR_2687_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2687_DELTABASIS_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2687_DELTABASIS_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2687_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2687_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2687_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2687_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2687_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_nohom_attempt": LOCAL_BOUNDS / "parent_sort_disjointness_nohom_attempt_2687_NONCLAIM.csv",
    "local_finite_basis": LOCAL_BOUNDS / "finite_delta_w_component_basis_2687_NONCLAIM.csv",
    "wep_nohom_attempt": WEP_RESIDUALS / "parent_sort_disjointness_nohom_attempt_2687_NONCLAIM.csv",
    "wep_finite_basis": WEP_RESIDUALS / "finite_delta_w_component_basis_2687_NONCLAIM.csv",
    "source_weight_finite_basis": SOURCE_WEIGHT / "FINITE_DELTAW_COMPONENT_BASIS_2687_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2687_2686_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2686_NEXT_TARGET.csv",
        "required_needles": ["NEXT2686_0_selected", "no-Hom(SpeciesLabel/Hidden/Readout, Coeff_active_source)", "Delta_w_AB is decomposed"],
        "purpose": "confirms selected 2687 no-Hom/finite-basis target",
    },
    {
        "source_id": "SRC2687_2686_REQUIREMENTS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2686_SORT_DISJOINTNESS_NOHOM_REQUIREMENTS_NONCLAIM.csv",
        "required_needles": ["SDN2686_2_nohom_species_source", "MISSING_SPECIES_TO_SOURCE_NOHOM", "SDN2686_7_verdict"],
        "purpose": "imports current no-Hom requirements",
    },
    {
        "source_id": "SRC2687_2686_QAUDIT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2686_Q_DESCENT_ADMISSIBILITY_AUDIT.csv",
        "required_needles": ["QDA2686_2_source_prefactor_counterexample", "COUNTEREXAMPLE_SURVIVES_Q_DESCENT_ALONE", "QDA2686_5_verdict"],
        "purpose": "imports q-descent insufficiency and counterexample",
    },
    {
        "source_id": "SRC2687_1896_ATTEMPT",
        "relative_path": "source-intake/microscope/branch_locked_wep/residuals/P8_Y5_PARENT_QLOC_1896_PARENT_SORT_DISJOINTNESS_NOHOM_ATTEMPT.csv",
        "required_needles": ["NH1896_1_conditional_typed_proof", "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED", "NH1896_5_verdict"],
        "purpose": "imports older no-Hom proof attempt",
    },
    {
        "source_id": "SRC2687_1896_VALIDATION",
        "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1896_VALIDATION.csv",
        "required_needles": ["VAL1896_01_nohom_verdict", "VAL1896_02_deltaw_basis", "VAL1896_OVERALL"],
        "purpose": "imports older validation status",
    },
    {
        "source_id": "SRC2687_2651_ATTEMPT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_NOHOM_DELTABASIS_2651_PARENT_SORT_NOHOM_CONSTRUCTOR_ATTEMPT.csv",
        "required_needles": ["NH2651_1_parent_sort_constructor", "PARENT_SORT_NOHOM_CONSTRUCTOR_NOT_DERIVED", "NH2651_5_verdict"],
        "purpose": "imports later no-Hom constructor attempt",
    },
    {
        "source_id": "SRC2687_2651_BASIS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_NOHOM_DELTABASIS_2651_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv",
        "required_needles": ["DWB2651_0_vector_space", "DWB2651_9_acceptance", "POLICY_WRITTEN_NONCLAIM"],
        "purpose": "imports finite Delta_w basis",
    },
    {
        "source_id": "SRC2687_2651_CLAIMS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_NOHOM_DELTABASIS_2651_CLAIM_GATES.csv",
        "required_needles": ["CG2651_0_nohom", "FAIL_PARENT_SORT_NOHOM_CONSTRUCTOR_NOT_DERIVED", "CLAIM_BLOCKED"],
        "purpose": "imports later claim gate status",
    },
    {
        "source_id": "SRC2687_1236_CERT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
        "required_needles": ["CERT1236_0_parent_sorts", "CERT1236_5_source_label_forgetting", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
        "purpose": "imports typed sort certificate",
    },
    {
        "source_id": "SRC2687_1220_TYPED",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
        "required_needles": ["PTOL1220_3_source_weight_exclusion", "PTOL1220_7_verdict", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
        "purpose": "imports typed signature verdict",
    },
    {
        "source_id": "SRC2687_1066_SCALAR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1066_SOURCE_SCALAR_EXCLUSION_LEMMA.csv",
        "required_needles": ["SSE1066_4_quantum_action_scale_obstruction", "SSE1066_5_verdict", "CONDITIONAL_SOURCE_SCALAR_EXCLUSION_NOT_PARENT_DERIVED"],
        "purpose": "imports action-scale/source-scalar obstruction",
    },
    {
        "source_id": "SRC2687_1045_FUNCTOR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "required_needles": ["MFS1045_2_matter_bundle_functor", "MFS1045_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
        "purpose": "imports matter functor status",
    },
]


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def as_bool(value: bool) -> str:
    return "true" if value else "false"


def path_for(relative_path: str) -> Path:
    return ROOT / relative_path


def rel_path(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            if not reader.fieldnames:
                return False, 0, "missing_header"
            return True, len(rows), "parsed"
    except Exception as exc:  # pragma: no cover
        return False, 0, f"{type(exc).__name__}: {exc}"


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("|", "\\|").replace("\n", "<br>") for h in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for spec in SOURCE_SPECS:
        path = path_for(spec["relative_path"])
        text = read_text(path)
        needles = list(spec["required_needles"])
        found = [needle for needle in needles if needle in text]
        missing = [needle for needle in needles if needle not in text]
        rows.append(
            {
                "source_id": spec["source_id"],
                "relative_path": spec["relative_path"],
                "absolute_path": str(path),
                "exists": as_bool(path.exists()),
                "required_needles": ";".join(needles),
                "found_needles": ";".join(found),
                "missing_needles": ";".join(missing),
                "purpose": spec["purpose"],
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def nohom_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NH2687_0_target",
            "claim_piece": "parent sort disjointness / no-Hom theorem",
            "formal_statement": "Hom_parent(SpeciesLabel, Coeff_active_source)=empty_or_common and Hom_parent(HiddenMarker/Readout, Coeff_active_source)=empty_or_common before variation/readout",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is exactly the theorem needed to make source-only Delta_w_AB unformable instead of merely small",
            "source_anchor": "2686:SDN2686_2_nohom_species_source;1896:NH1896_0_target;2651:NH2651_0_target",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "NH2687_1_conditional_constructor",
            "claim_piece": "active-source coefficient constructor",
            "formal_statement": "Coeff_active_source is generated only from UniversalCalibration, explicitly retained residuals, and total Hilbert source data; labels and markers are not domain arguments",
            "status": "EXACT_CONDITIONAL_CONSTRUCTOR",
            "proof_or_obstruction": "if parent-derived, there is no legal source-only species coefficient map; currently the constructor is still a typed grammar contract",
            "source_anchor": "2651:NH2651_1_parent_sort_constructor;1236:CERT1236_0_parent_sorts",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "NH2687_2_product_sequester",
            "claim_piece": "visible/source functor factorization",
            "formal_statement": "If C_parent factors through visible/source data times bookkeeping labels and source coefficient functors factor through the visible/source projection, label tangents annihilate active-source coefficients",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "chain-rule proof is valid after product/source sequester is signed; current corpus does not derive that factorization from primitives",
            "source_anchor": "1896:NH1896_2_product_category_route;2686:QDA2686_5_verdict",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "NH2687_3_counterexamples",
            "claim_piece": "why no-Hom is not yet proof",
            "formal_statement": "Disconnected species sectors, hidden invariant scalars, domain/material markers, action-scale coefficients, and readout masks can still define source coefficient maps unless explicitly typed out",
            "status": "COUNTEREXAMPLES_RETAINED",
            "proof_or_obstruction": "naturality, q-descent, Ward conservation, and candidate typing do not erase these legal coefficient routes",
            "source_anchor": "2686:QDA2686_2_source_prefactor_counterexample;1066:SSE1066_4_quantum_action_scale_obstruction",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "NH2687_4_stability",
            "claim_piece": "tree no-Hom survives measure/readout/radiative projection",
            "formal_statement": "One parent action-density/measure owner plus readout/source-worldtube stability prevents source coefficients from returning through S_eff, loops, clocks, WEP readout, or local projectors",
            "status": "ACTION_SCALE_READOUT_STABILITY_UNSIGNED",
            "proof_or_obstruction": "even a tree-level no-Hom constructor would not be local-claim grade without this stability package",
            "source_anchor": "2651:NH2651_4_action_scale_readout_stability;1066:SSE1066_5_verdict",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
        {
            "attempt_id": "NH2687_5_verdict",
            "claim_piece": "promote no-Hom as current theorem",
            "formal_statement": "Current MTS parent primitives derive no-Hom(SpeciesLabel/Hidden/Readout, Coeff_active_source) without closure axioms",
            "status": "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED",
            "proof_or_obstruction": "exact conditional proof exists, but parent sort constructor, constructor exhaustion, product sequester, no-marker route, and action-scale/readout stability are not signed together",
            "source_anchor": "NH2687_0_target through NH2687_4_stability",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        },
    ]


def nohom_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("NHG2687_0_parent_sort_constructor", "parent sorts are derived from MTS primitives", "MISSING_PARENT_SORT_CONSTRUCTOR", "no-Hom becomes theorem-level rather than syntax decree", "object-language route remains closure"),
        ("NHG2687_1_constructor_exhaustion", "all active-source coefficient constructors are exhausted before readout", "MISSING_CONSTRUCTOR_EXHAUSTION", "no extra source coefficient can be added after the fact", "finite Delta_w basis remains live"),
        ("NHG2687_2_no_species_hom", "SpeciesLabel has no morphism to active-source coefficients", "EXACT_CONDITIONAL_NOT_PARENT_SIGNED", "pre-action Delta_w_species is ill-typed", "relative species prefactor remains live"),
        ("NHG2687_3_no_hidden_readout_hom", "hidden/domain/boundary/readout markers cannot be retyped as source coefficients", "NO_MARKER_READOUT_HOM_NOT_PROVED", "c(I_hid) and C_eff tails are theorem-zero candidates", "marker/readout source weights stay finite"),
        ("NHG2687_4_action_scale_readout", "action-scale/measure/readout stability preserves no-Hom", "ACTION_SCALE_READOUT_STABILITY_UNSIGNED", "tree no-Hom survives WEP/R10/clock/PPN projection", "finite residual route is mandatory"),
        ("NHG2687_5_verdict", "all no-Hom gates close", "NOHOM_CLAIM_BLOCKED", "Delta_w source components become theorem-zero subject to projection/readout gates", "finite Delta_w basis is the honest branch"),
    ]
    return [
        {
            "gate_id": gate_id,
            "required_clause": clause,
            "current_status": status,
            "if_pass": if_pass,
            "if_fail": if_fail,
            "gate_pass": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, clause, status, if_pass, if_fail in rows
    ]


def finite_basis_rows() -> list[dict[str, Any]]:
    rows = [
        ("DWB2687_0_vector_space", "Delta_w_vector_space", "finite source-weight residual vector after universal common calibration mode is removed", "Delta_w = P_perp w, P_perp u_common=0; norm is L1/no-cancellation envelope or declared arena covariance norm", "BASIS_SCHEMA_NONCLAIM_PARENT_COMPONENT_VALUES_MISSING", "parent coefficient vector, composition weights p_A, norm choice, no-cancellation policy, source path", "dimensionless"),
        ("DWB2687_1_preaction_species", "Delta_w_species", "relative pre-variation species/action/source prefactor after common-mode subtraction", "w_A=w_common(1+epsilon_A), sum_A p_A epsilon_A=0 for declared composition/source weights", "LIVE_COUNTERMODEL_COMPONENT_SYMBOLIC_ONLY", "parent epsilon_A vector or no-Hom theorem-zero", "dimensionless"),
        ("DWB2687_2_current_rescale", "c_A_current_rescale", "post-variation species/source current rescale J_A -> c_A J_A", "Delta J_src=sum_A(c_A-c_common)J_A", "CURRENT_OWNER_MISSING_NONCLAIM", "source-current owner/no-rescale theorem or coefficient row", "dimensionless"),
        ("DWB2687_3_marker_spurion", "Delta_w_marker_hidden", "hidden invariant, material marker, boundary/domain class, or readout mask that reweights source strength", "w_A=w_common[1+epsilon_marker I_marker(A,D,boundary,readout)]", "NO_MARKER_THEOREM_UNSIGNED_NONCLAIM", "no-marker/no-hidden-visible theorem or finite marker coefficient bounds", "dimensionless"),
        ("DWB2687_4_action_measure_jacobian", "Delta_w_measure", "relative hbar/action-density/measure/Jacobian multiplier that can mimic source weighting while leaving some classical equations unchanged", "S_matter=sum_A Z_A^measure S_A; Delta_w_measure=P_perp log Z_A^measure", "ACTION_SCALE_MEASURE_OWNER_UNSIGNED_NONCLAIM", "single parent action-density/measure owner or numeric Z_A^measure bounds", "dimensionless logarithmic response"),
        ("DWB2687_5_nonhilbert_current", "J_NH_retained", "non-Hilbert, boundary, exchange, memory, range, connection, spin/torsion, or improvement current bypassing total Hilbert source", "J_src=kappa_univ T_Hilbert + sum_i C_i J_NH,i", "OPEN_PARALLEL_GATE_NONCLAIM", "formula-level K_owner and q_retained zero proof or finite coefficient row", "declared by current channel"),
        ("DWB2687_6_mass_projector", "Delta_mu_projector", "measured-GM/orbital mass projector, exchange, boundary, anomaly, or Gauss calibration residual", "Delta mu_obs=Pi_M(J_Hilbert+J_exchange+J_boundary)-Pi_M(J_Hilbert)", "PROJECTED_FLUX_OPEN_NONCLAIM", "closed calibrated mass projector or finite Delta_mu row", "dimensionless or declared GM units"),
        ("DWB2687_7_material_basis_link", "R_material_X", "material response tensor mapping finite source-weight components into WEP/test-body contrasts", "eta_AB ~ tau_WEP sum_X K_X C_X R_material_X(A,B), with all legs sourced before scoring", "PARENT_MATERIAL_TENSOR_BASIS_BLOCKED_NONCLAIM", "parent X basis, material tensor, coefficient vector, tau/readout/product convention", "declared parent-basis response units"),
        ("DWB2687_8_no_cancellation_policy", "basis_policy", "multi-component scores use a no-cancellation envelope unless a parent identity proves signed cancellation", "observable_bound uses sum_i |K_i Delta_w_i| or a declared covariance envelope; no fitted cancellation pass", "POLICY_WRITTEN_NONCLAIM", "arena K/tau/material projections and parent coefficient values", "policy"),
        ("DWB2687_9_acceptance", "finite_Delta_w_basis_acceptance", "finite basis is score-ready only when every component has theorem-zero or parent coefficient value plus arena projection kernels", "claim row requires zero-proof or numeric C_i, source path, units, norm, K/tau/material/readout projection and no-cancellation policy", "FINITE_DELTAW_BASIS_STAGED_NONCLAIM", "all component values/theorem-zeros plus projections", "mixed declared by component"),
    ]
    return [
        {
            "basis_id": basis_id,
            "component": component,
            "definition": definition,
            "basis_formula": formula,
            "current_status": status,
            "missing_for_claim": missing,
            "units": units,
            "score_ready": "false",
            "valid_prediction_row": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for basis_id, component, definition, formula, status, missing, units in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    rows = [
        ("DRY2687_0_nohom_unsigned", "false", "false", "false", "false", "false", "false", "REFUSED_NOHOM_NOT_PARENT_DERIVED"),
        ("DRY2687_1_syntax_decree", "false", "true", "false", "false", "false", "false", "REFUSED_SYNTAX_BY_DECREE"),
        ("DRY2687_2_basis_no_values", "true", "false", "false", "false", "false", "false", "REFUSED_PARENT_DELTAW_VALUES_MISSING"),
        ("DRY2687_3_projection_missing", "true", "false", "true", "false", "false", "true", "REFUSED_PROJECTION_KERNELS_NOT_READY"),
        ("DRY2687_4_cancellation", "true", "false", "true", "true", "true", "true", "REFUSED_CANCELLATION_ONLY_PASS"),
        ("DRY2687_5_counterfactual_ready", "true", "false", "true", "true", "false", "true", "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM"),
    ]
    return [
        {
            "case_id": case_id,
            "nohom_parent_signed": nohom,
            "uses_syntax_decree": syntax,
            "basis_has_parent_values": values,
            "projection_ready": projection,
            "uses_cancellation": cancellation,
            "score_attempt": score,
            "expected_status": expected,
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for case_id, nohom, syntax, values, projection, cancellation, score, expected in rows
    ]


def compute_dryrun(case: dict[str, Any]) -> str:
    if case["uses_syntax_decree"] == "true":
        return "REFUSED_SYNTAX_BY_DECREE"
    if case["nohom_parent_signed"] != "true":
        return "REFUSED_NOHOM_NOT_PARENT_DERIVED"
    if case["basis_has_parent_values"] != "true":
        return "REFUSED_PARENT_DELTAW_VALUES_MISSING"
    if case["projection_ready"] != "true":
        return "REFUSED_PROJECTION_KERNELS_NOT_READY"
    if case["uses_cancellation"] == "true":
        return "REFUSED_CANCELLATION_ONLY_PASS"
    return "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        computed = compute_dryrun(case)
        rows.append(
            {
                "case_id": case["case_id"],
                "computed_status": computed,
                "expected_status": case["expected_status"],
                "status_match": as_bool(computed == case["expected_status"]),
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "timestamp_utc": stamp(),
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2687_0_nohom", "parent no-Hom theorem is signed", "FAIL_PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED", "NH2687_5_verdict", "false"),
        ("CG2687_1_deltaw_values", "finite Delta_w basis has parent coefficient values or theorem-zero rows", "FAIL_BASIS_SCHEMA_NONCLAIM_PARENT_COMPONENT_VALUES_MISSING", "DWB2687_0_vector_space", "false"),
        ("CG2687_2_projection", "arena projection/tau/material kernels are sourced before scoring", "FAIL_PROJECTION_KERNELS_NOT_READY", "DWB2687_7_material_basis_link", "false"),
        ("CG2687_3_no_cancellation", "no cancellation-only pass is used", "PASS_POLICY_WRITTEN_NONCLAIM", "DWB2687_8_no_cancellation_policy", "true"),
        ("CG2687_4_verdict", "source-weight zero or finite Delta_w branch can claim pass", "CLAIM_BLOCKED", "CG2687_0_nohom through CG2687_3_no_cancellation", "false"),
    ]
    return [
        {
            "gate_id": gate_id,
            "condition": condition,
            "current_status": status,
            "source_anchor": anchor,
            "gate_pass": gate_pass,
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for gate_id, condition, status, anchor, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2687_0_nohom",
            "decision": "DO_NOT_PROMOTE_NOHOM",
            "reason": "typed/product proof is exact conditionally, but parent sort construction and stability gates remain unsigned",
            "status": "NOHOM_ROUTE_SHARP_BUT_UNSIGNED",
            "next_dependency": "derive parent sort constructor from MTS primitives",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2687_1_basis",
            "decision": "FINITE_DELTAW_BASIS_STAGED_AS_HONEST_FALLBACK",
            "reason": "components, common-mode projector, action-measure leg, material-basis link, and no-cancellation policy are explicit but value/projection inputs are missing",
            "status": "FINITE_DELTAW_BASIS_NONCLAIM",
            "next_dependency": "parent values or theorem-zero rows plus arena projections",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2687_2_next",
            "decision": "ATTACK_PARENT_SORT_CONSTRUCTOR_NEXT",
            "reason": "repeating no-Hom without deriving the constructor would be circling; the next leap is primitive-to-sort construction",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "2688 parent sort constructor from MTS primitives or Delta_w component values",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2687_0_selected",
            "kind": "selected",
            "target_doc": "2688-Y5-R2FR-parent-sort-constructor-from-MTS-primitives-or-delta-w-component-values.md",
            "target_script": "scripts/Y5_R2FR_parent_sort_constructor_from_MTS_primitives_or_delta_w_component_values_2688.py",
            "purpose": "derive parent sort constructor and constructor exhaustion from MTS primitives so no-Hom is theorem-level; if that fails, begin source-ready Delta_w component values",
            "acceptance_gate": "either disjoint parent sorts and active-source constructor domain are derived without syntax decree, or finite Delta_w component rows remain nonclaim with value/source/projection requirements",
            "forbidden_shortcuts": "syntax by decree; treating typed schema as proof; Delta_w=0 by preference; WEP/R10 bound inversion; cancellation-only pass; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2687_0_nohom", "source-coupling theorem", "NOHOM_EXACT_CONDITIONAL_NOT_DERIVED", "the formal no-Hom theorem is sharp but not parent-signed"),
        ("STATUS2687_1_finite_basis", "Delta_w_AB fallback", "FINITE_BASIS_EXPLICIT_NONCLAIM", "the finite source-weight route is now componentized rather than vague"),
        ("STATUS2687_2_next", "derivation route", "PARENT_SORT_CONSTRUCTOR_IS_NEXT_LEAP", "the next proof must derive sorts/constructors from MTS primitives instead of restating grammar"),
    ]
    return [
        {
            "status_id": status_id,
            "sector": sector,
            "status": status,
            "meaning": meaning,
            "claim_allowed": "false",
            "next_action": "run 2688 parent sort constructor target",
            "timestamp_utc": stamp(),
        }
        for status_id, sector, status, meaning in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2687_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(source_rows: list[dict[str, Any]], nohom: list[dict[str, Any]], gates: list[dict[str, Any]], basis: list[dict[str, Any]], dryrun_results: list[dict[str, Any]], claim_gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    conditional_exact = any(row["attempt_id"] == "NH2687_1_conditional_constructor" and row["status"] == "EXACT_CONDITIONAL_CONSTRUCTOR" for row in nohom)
    verdict_blocked = any(row["attempt_id"] == "NH2687_5_verdict" and row["status"] == "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED" for row in nohom)
    counterexamples_retained = any(row["attempt_id"] == "NH2687_3_counterexamples" and row["status"] == "COUNTEREXAMPLES_RETAINED" for row in nohom)
    gates_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in gates)
    basis_nonclaim = all(row["score_ready"] == "false" and row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in basis)
    policy_written = any(row["basis_id"] == "DWB2687_8_no_cancellation_policy" and row["current_status"] == "POLICY_WRITTEN_NONCLAIM" for row in basis)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in claim_gates)
    no_cancellation_guard = any(row["gate_id"] == "CG2687_3_no_cancellation" and row["gate_pass"] == "true" and row["claim_allowed"] == "false" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2688" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2687_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2687_conditional_nohom_written", conditional_exact, "conditional no-Hom constructor theorem is written"),
        ("VAL2687_nohom_not_promoted", verdict_blocked, "no-Hom theorem is not promoted"),
        ("VAL2687_counterexamples_retained", counterexamples_retained, "counterexamples remain retained"),
        ("VAL2687_nohom_gates_block", gates_blocked, "no-Hom gates remain nonclaim"),
        ("VAL2687_finite_basis_nonclaim", basis_nonclaim, "finite Delta_w basis rows are nonclaim/not score-ready"),
        ("VAL2687_no_cancellation_policy", policy_written and no_cancellation_guard, "no-cancellation policy is present as guard only"),
        ("VAL2687_dryrun_refusals", dryrun_ok, "dry-run refuses unsigned no-Hom, syntax decree, missing values, missing projections and cancellation-only passes"),
        ("VAL2687_claim_gates_block_claims", claim_blocked, "claim gates block promotion"),
        ("VAL2687_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2687_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2687_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2687_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2687_next_target_selected", next_target_ok, "2688 parent sort constructor target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2687_OVERALL",
            "passed": as_bool(overall),
            "detail": "2687 consolidates no-Hom as exact conditional, refuses promotion, stages finite Delta_w basis, and selects parent sort constructor as next leap",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(source_rows: list[dict[str, Any]], nohom: list[dict[str, Any]], gates: list[dict[str, Any]], basis: list[dict[str, Any]], dry_cases: list[dict[str, Any]], dry_results: list[dict[str, Any]], claim_gates: list[dict[str, Any]], decisions: list[dict[str, Any]], next_target: list[dict[str, Any]], status: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2687 — Y5/R2FR Parent Sort Disjointness No-Hom Proof or Finite Delta-w Basis",
                "",
                "## Private Verdict",
                "",
                "The no-Hom route is mathematically clean but not yet parent-derived. If the parent sort constructor is signed, `Hom(SpeciesLabel/Hidden/Readout, Coeff_active_source)=empty_or_common` and source-only `Delta_w_AB` cannot be formed. Current evidence still marks this as an exact conditional, not a theorem.",
                "",
                "This is not a dead end. It is the sharpest load-bearing beam so far: either derive the parent sort constructor from MTS primitives, or stop trying to erase `Delta_w_AB` and treat it as a finite component basis.",
                "",
                "No local-GR, WEP, R10, PPN, clock, orbital, or Newton-source claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## No-Hom Attempt",
                "",
                markdown_table(nohom),
                "",
                "## No-Hom Gate",
                "",
                markdown_table(gates),
                "",
                "## Finite Delta-w Component Basis",
                "",
                markdown_table(basis),
                "",
                "## Dry-Run Cases",
                "",
                markdown_table(dry_cases),
                "",
                "## Dry-Run Results",
                "",
                markdown_table(dry_results),
                "",
                "## Claim Gates",
                "",
                markdown_table(claim_gates),
                "",
                "## Decisions",
                "",
                markdown_table(decisions),
                "",
                "## Next Target",
                "",
                markdown_table(next_target),
                "",
                "## Project Status Snapshot",
                "",
                markdown_table(status),
                "",
                "## Validation",
                "",
                markdown_table(validation),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    source_rows = source_register_rows()
    nohom = nohom_attempt_rows()
    gates = nohom_gate_rows()
    basis = finite_basis_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["nohom_attempt"], nohom)
    write_csv(OUTPUTS["nohom_gate"], gates)
    write_csv(OUTPUTS["finite_basis"], basis)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_nohom_attempt"], nohom)
    write_csv(BRANCH_OUTPUTS["local_finite_basis"], basis)
    write_csv(BRANCH_OUTPUTS["wep_nohom_attempt"], nohom)
    write_csv(BRANCH_OUTPUTS["wep_finite_basis"], basis)
    write_csv(BRANCH_OUTPUTS["source_weight_finite_basis"], basis)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(source_rows, nohom, gates, basis, dry_results, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, nohom, gates, basis, dry_cases, dry_results, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
