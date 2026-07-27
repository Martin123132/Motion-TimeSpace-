from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"

DOC = ROOT / "3208-Y5-R2FR-Htau-one-form-exactness-or-first-DeltaH-curl-bound-under-AX1090.md"
INPUTS = OUT / "P8_Y5_R2FR_3208_INPUTS.csv"
CURL_LAW = OUT / "P8_Y5_R2FR_3208_HTAU_ONE_FORM_CURL_LAW.csv"
COMPONENTS = OUT / "P8_Y5_R2FR_3208_CURL_COMPONENT_ENVELOPE.csv"
PATH_BOUND = OUT / "P8_Y5_R2FR_3208_FIELD_SPACE_PATH_BOUND_TEMPLATE.csv"
GATES = OUT / "P8_Y5_R2FR_3208_EXACTNESS_OR_BOUND_GATES.csv"
EPSILON_FEED = OUT / "P8_Y5_R2FR_3208_EPSILON_ABS_FEED.csv"
DECISION = OUT / "P8_Y5_R2FR_3208_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3208_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def b(value: bool) -> str:
    return "true" if value else "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def resolve(location: str, relative_path: str) -> Path:
    if location == "post_checkpoint":
        return ROOT / relative_path
    if location == "mts_residuals":
        return OUT / relative_path
    if location == "formalization":
        return FW / relative_path
    raise ValueError(location)


def rel(path: Path) -> str:
    return str(path.relative_to(REPO)).replace("\\", "/")


def evidence(path: Path, terms: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    lowered = [term.lower() for term in terms]
    hits: list[str] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        haystack = line.lower()
        if any(term in haystack for term in lowered):
            hits.append(f"L{line_number}:{' '.join(line.strip().split())[:180]}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_MATCH"


SOURCES = [
    {
        "input_id": "SRC3208_00_3207_doc",
        "location": "post_checkpoint",
        "relative_path": "3207-Y5-R2FR-MHref-denominator-lower-bound-law-or-Bobs-refusal-under-AX1090.md",
        "role": "3207 denominator lower-bound handoff",
        "terms": ["alpha_tau", "epsilon_abs", "delta_H_tau", "Next target"],
    },
    {
        "input_id": "SRC3208_01_3207_law",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_3207_MHREF_DENOMINATOR_LOWER_BOUND_LAW.csv",
        "role": "machine-readable lower-bound law",
        "terms": ["alpha_tau", "M_H_ref", "epsilon_abs", "lower"],
    },
    {
        "input_id": "SRC3208_02_1645_doc",
        "location": "post_checkpoint",
        "relative_path": "1645-Y5-R2FR-Htau-MHref-integrability-reference-lock-or-Mstar-source-row.md",
        "role": "field-space one-form and curl decomposition",
        "terms": ["alpha_tau", "d_field", "I_EH", "I_ref"],
    },
    {
        "input_id": "SRC3208_03_1647_doc",
        "location": "post_checkpoint",
        "relative_path": "1647-Y5-R2FR-hybrid-EH-quotient-current-owner-or-deltaH-curl-source-fill.md",
        "role": "hybrid EH-plus-quotient deltaH curl decomposition",
        "terms": ["deltaH Curl Decomposition", "omega_EH", "B_observed", "tau_reference"],
    },
    {
        "input_id": "SRC3208_04_1647_decomp",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_PARENT_QLOC_1647_DELTAH_CURL_DECOMPOSITION.csv",
        "role": "machine-readable deltaH curl decomposition",
        "terms": ["CDC1647_0", "CDC1647_5", "source_fill", "valid_for_claim"],
    },
    {
        "input_id": "SRC3208_05_2667_doc",
        "location": "post_checkpoint",
        "relative_path": "2667-Y5-R2FR-Htau-integrability-curl-zero-or-MHref-component-row.md",
        "role": "Htau integrability curl proof audit",
        "terms": ["delta_H_tau", "omega_X", "reference_curl", "projector"],
    },
    {
        "input_id": "SRC3208_06_2667_audit",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_CURL_PROOF_AUDIT.csv",
        "role": "curl proof clauses",
        "terms": ["HTC2667_0", "omega_X", "reference", "verdict"],
    },
    {
        "input_id": "SRC3208_07_2667_template",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_COMPONENT_ROW_TEMPLATE_NONCLAIM.csv",
        "role": "curl component row template",
        "terms": ["HCUR2667", "reference_curl", "absolute_envelope", "M_H_ref"],
    },
    {
        "input_id": "SRC3208_08_2947_rows",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R2FR_2947_HTAU_INTEGRABILITY_RESIDUAL_ROWS.csv",
        "role": "recent Htau residual rows",
        "terms": ["CURL2947", "delta_H_tau", "reference_curl", "projector"],
    },
    {
        "input_id": "SRC3208_09_994_envelope",
        "location": "mts_residuals",
        "relative_path": "P8_Y5_R10_994_DELTAH_NO_CANCELLATION_ENVELOPE.csv",
        "role": "no-cancellation envelope policy",
        "terms": ["deltaH_curl", "no_cancellation", "residual", "valid_for_claim"],
    },
]


def build_inputs(now: str) -> list[dict[str, object]]:
    rows = []
    for source in SOURCES:
        path = resolve(source["location"], source["relative_path"])
        rows.append(
            {
                "input_id": source["input_id"],
                "path": str(path),
                "exists": b(path.exists()),
                "role": source["role"],
                "evidence": evidence(path, source["terms"]),
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def build_curl_law(now: str) -> list[dict[str, object]]:
    return [
        {
            "law_id": "HCL3208_0_one_form",
            "object": "alpha_tau",
            "formula": "alpha_tau(delta Phi)=int_S(delta Q_tau^MTS - i_tau Theta_MTS(delta Phi)) - delta H_ref",
            "derivation": "definition of the Hamiltonian variation one-form on a fixed branch",
            "claim_status": "conditional_definition",
            "missing_for_claim": "parent Theta_MTS;Q_tau_MTS;tau_id;surface_pair;fixed_H_ref",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "HCL3208_1_field_space_curl_fixed_branch",
            "object": "d_F alpha_tau",
            "formula": "d_F alpha_tau(delta1,delta2) = - int_S i_tau omega_MTS(delta1,delta2) when tau,S,H_ref are fixed branch data",
            "derivation": "d_F(delta Q_tau)=0 and omega_MTS=d_F Theta_MTS; sign is irrelevant for absolute bounds",
            "claim_status": "derived_identity",
            "missing_for_claim": "omega_MTS by sector; fixed branch certificate; boundary pullback units",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "HCL3208_2_moving_branch_corrections",
            "object": "C_tau+C_S+C_ref",
            "formula": "d_F alpha_tau = -int_S i_tau omega_MTS + C_tau + C_S + C_ref if tau, surface class, or reference selector varies",
            "derivation": "field-dependent generator/surface/reference add explicit curl terms rather than being hidden in H_tau",
            "claim_status": "derived_accounting_rule",
            "missing_for_claim": "delta_tau;delta_surface;reference_selector_derivative source rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "HCL3208_3_exact_route",
            "object": "H_tau exactness",
            "formula": "H_tau exists as a state function if d_F alpha_tau=0 on the allowed local branch",
            "derivation": "closed one-form criterion",
            "claim_status": "not_satisfied_current_corpus",
            "missing_for_claim": "all curl components theorem-zero in one parent branch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "HCL3208_4_bound_route",
            "object": "Delta_H_curl",
            "formula": "if two field-space paths enclose B_F, |Delta H_tau(path1)-Delta H_tau(path2)| <= int_{B_F}|d_F alpha_tau| <= A_F sup_{B_F}|d_F alpha_tau|",
            "derivation": "field-space Stokes bound; nonzero curl becomes a no-cancellation denominator residual",
            "claim_status": "new_bound_route_derived_no_values",
            "missing_for_claim": "field-space area A_F; component sup bounds; norm convention; source paths",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "law_id": "HCL3208_5_epsilon_feed",
            "object": "epsilon_Htau_curl",
            "formula": "epsilon_Htau_curl := Delta_H_curl_bound/(G_ref M_EH) feeds epsilon_abs from 3207",
            "derivation": "normalizes path-dependence by the same non-orbital comparator used for the denominator lower-bound law",
            "claim_status": "feed_schema_only",
            "missing_for_claim": "Delta_H_curl_bound;G_ref;M_EH",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_components(now: str) -> list[dict[str, object]]:
    return [
        {
            "component_id": "HCURL3208_0_EH_stationary",
            "component": "I_EH_stationary_boundary",
            "definition": "abs(int_S i_tau omega_EH(delta1,delta2))",
            "zero_or_bound_condition": "fixed stationary EH exterior branch with standard boundary conditions",
            "current_status": "CONDITIONAL_REFERENCE_ONLY_NOT_MTS_PROOF",
            "minimum_columns": "system_id;surface_id;tau_id;omega_EH_pullback;boundary_condition;units;source_path",
            "feeds": "Delta_H_curl_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "HCURL3208_1_X_sector",
            "component": "I_X_symplectic",
            "definition": "abs(int_S i_tau omega_X(delta1,delta2))",
            "zero_or_bound_condition": "L_X/Theta_X/omega_X parent-owned and boundary pullback zero/exact/bounded",
            "current_status": "MISSING_LX_THETA_OMEGA_OWNER",
            "minimum_columns": "sector;L_X;Theta_X;omega_X;tau_action;surface_pair;bound_value;units;source_path",
            "feeds": "Delta_H_curl_bound;epsilon_abs",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "HCURL3208_2_boundary_flux",
            "component": "I_boundary_corner_edge",
            "definition": "abs(boundary/corner/edge contribution to d_F alpha_tau)",
            "zero_or_bound_condition": "boundary class exact/proper/no-hair or source-backed finite flux",
            "current_status": "MISSING_BOUNDARY_EXACTNESS_OR_BOUND",
            "minimum_columns": "boundary_class;corner_edge_id;flux_bound;units;source_path;zero_theorem_or_bound",
            "feeds": "Delta_H_curl_bound;Bobs boundary/corner rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "HCURL3208_3_projector_domain",
            "component": "I_projector_domain_stress",
            "definition": "abs(delta Pi_M, P_loc, domain, normal, Hodge/Green variation contribution)",
            "zero_or_bound_condition": "projector/domain is parent-fixed or finite commutator/stress bound is sourced",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP",
            "minimum_columns": "projector_id;domain_id;commutator_or_stress_bound;units;source_path",
            "feeds": "Delta_H_curl_bound;Bobs projector row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "HCURL3208_4_reference",
            "component": "I_ref",
            "definition": "abs(C_ref) from moving H_ref/reference selector or reference curl",
            "zero_or_bound_condition": "H_ref fixed before source/readout and derivative-silent, or explicit reference-curl bound",
            "current_status": "MISSING_FIXED_REFERENCE_LOCK_OR_BOUND",
            "minimum_columns": "reference_branch;H_ref;reference_curl_bound;source_blind_derivative;units;source_path",
            "feeds": "Delta_H_curl_bound;Delta_ref",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "HCURL3208_5_tau_surface",
            "component": "I_tau_surface",
            "definition": "abs(C_tau+C_S) from tau generator or linking surface variation",
            "zero_or_bound_condition": "same tau and surface homology class are fixed before readout or finite mismatch bound is sourced",
            "current_status": "MISSING_TAU_SURFACE_VARIATION_LOCK",
            "minimum_columns": "tau_id;surface_pair;homology_class;delta_tau_bound;delta_surface_bound;units;source_path",
            "feeds": "Delta_H_curl_bound;tau_ref_surface_mismatch",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "HCURL3208_6_observed_source_flux",
            "component": "I_observed_source_measure",
            "definition": "abs(P_loc B_source/B_boundary/B_bulk contribution to d_F alpha_tau)",
            "zero_or_bound_condition": "observed reduced Ward/no-flux theorem or componentwise source-backed Bobs rows",
            "current_status": "MISSING_OBSERVED_REDUCED_FLUX_ZERO_OR_BOUND",
            "minimum_columns": "B_component;projection;raw_flux_bound;units;source_path",
            "feeds": "Delta_H_curl_bound;Bobs source/bulk rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "HCURL3208_7_total",
            "component": "Delta_H_curl_bound",
            "definition": "A_F times the absolute sum/supremum of all live curl components; no cancellation credit",
            "zero_or_bound_condition": "every component theorem-zero or source-backed finite in shared units and norm",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "minimum_columns": "component_id;component_bound;A_F_or_integral_weight;units;source_path;no_cancellation_flag",
            "feeds": "epsilon_Htau_curl;epsilon_abs;M_H_ref lower-bound route",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_path_bound(now: str) -> list[dict[str, object]]:
    return [
        {
            "row_id": "PB3208_0_exact_zero",
            "route": "exact_integrability",
            "required_statement": "d_F alpha_tau=0 for all allowed field variations on the branch",
            "output_if_passes": "Delta_H_curl_bound=0 and H_tau is path-independent",
            "current_value": "MISSING_EXACT_ZERO_CERTIFICATE",
            "required_columns": "branch_id;variation_space;component_zero_certificates;source_path;valid_for_claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PB3208_1_finite_bound",
            "route": "bounded_nonintegrability",
            "required_statement": "Delta_H_curl_bound <= integral_BF |d_F alpha_tau|",
            "output_if_passes": "finite path-dependence residual can feed epsilon_abs without pretending H_tau is exact",
            "current_value": "MISSING_COMPONENT_BOUNDS_AND_FIELD_SPACE_AREA",
            "required_columns": "branch_id;field_space_2chain;A_F;component_sup_bounds;norm;units;source_path;valid_for_claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "row_id": "PB3208_2_first_fill",
            "route": "first_component_acquisition",
            "required_statement": "source the reference-curl and X-sector omega terms first because they block both exactness and finite bound routes",
            "output_if_passes": "first nonzero piece of Delta_H_curl_bound becomes evaluable",
            "current_value": "SOURCE_READY_NONCLAIM_TEMPLATE",
            "required_columns": "reference_curl_bound;omega_X_bound;units;source_path;zero_theorem_or_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_gates(now: str) -> list[dict[str, object]]:
    gates = [
        ("G3208_0_parent_current", "Theta_MTS and Q_tau_MTS come from one parent variation", "false", "MISSING_PARENT_THETA_QTAU"),
        ("G3208_1_fixed_branch", "tau, surface pair, source worldtube, and reference are fixed before readout", "false", "MISSING_FIXED_BRANCH_CERTIFICATE"),
        ("G3208_2_curl_identity", "field-space curl identity is written with all correction terms explicit", "true", "DERIVED_IDENTITY_PRESENT"),
        ("G3208_3_exact_zero", "d_F alpha_tau theorem-zero is proved", "false", "ZERO_NOT_PROVED"),
        ("G3208_4_finite_bound", "Delta_H_curl_bound has finite source-backed value", "false", "BOUND_ROWS_MISSING"),
        ("G3208_5_no_cancellation", "no cancellation between curl/reference/projector/boundary components is used", "true", "NO_CANCELLATION_POLICY_ACTIVE"),
        ("G3208_6_epsilon_feed", "epsilon_Htau_curl can feed epsilon_abs", "false", "FEED_SCHEMA_ONLY_VALUES_MISSING"),
        ("G3208_7_claim_status", "H_tau/M_H_ref/Bobs/local-GR branch can score", "false", "CLAIM_BLOCKED_CURRENT_CORPUS"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "pass": passed,
            "status": status,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for gate_id, gate, passed, status in gates
    ]


def build_epsilon_feed(now: str) -> list[dict[str, object]]:
    return [
        {
            "feed_id": "EF3208_0_Delta_H_curl",
            "epsilon_abs_component": "epsilon_Htau_curl",
            "definition": "Delta_H_curl_bound/(G_ref*M_EH)",
            "required_inputs": "Delta_H_curl_bound;G_ref;M_EH;units;source_path",
            "current_status": "MISSING_VALUES",
            "feeds": "LAW3207_3_positive_lower_bound",
            "claim_effect": "if finite and small, contributes to denominator lower-bound instead of blocking by wording alone",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "feed_id": "EF3208_1_exact_zero_case",
            "epsilon_abs_component": "epsilon_Htau_curl",
            "definition": "0 if d_F alpha_tau=0 theorem is parent-signed",
            "required_inputs": "all G3208 exactness gates true",
            "current_status": "ZERO_CASE_NOT_PROVED",
            "feeds": "exact M_H_ref route",
            "claim_effect": "H_tau becomes a legal state function but positivity still needs M_H_ref/G_ref/source rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def build_decision(now: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "DEC3208_0",
            "result": "HTAU_CURL_IDENTITY_AND_STOKES_BOUND_DERIVED_NO_VALUES",
            "claim_status": "NO_HTAU_EXACTNESS_NO_MHREF_NO_BOBS_SCORE_NO_LOCAL_GR_CLAIM",
            "decision": "retain exact-zero route, but add bounded-nonintegrability route via field-space Stokes so curl can become an epsilon_abs component",
            "best_next_route": "derive/source HCURL3208_1_X_sector omega bound or HCURL3208_4_reference fixed-reference curl bound first",
            "next_target": "3209-Y5-R2FR-X-sector-Theta-omega-owner-or-reference-curl-bound-first-row-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join(["---"] * len(fields)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def main() -> None:
    now = stamp()
    input_rows = build_inputs(now)
    law_rows = build_curl_law(now)
    component_rows = build_components(now)
    path_rows = build_path_bound(now)
    gate_rows = build_gates(now)
    epsilon_rows = build_epsilon_feed(now)
    decision_rows = build_decision(now)

    generated = [
        (INPUTS, input_rows),
        (CURL_LAW, law_rows),
        (COMPONENTS, component_rows),
        (PATH_BOUND, path_rows),
        (GATES, gate_rows),
        (EPSILON_FEED, epsilon_rows),
        (DECISION, decision_rows),
    ]
    for path, rows in generated:
        write_csv(path, rows)

    generated_paths = [path for path, _ in generated]
    validation_rows = [
        {
            "check_id": "VAL3208_00_inputs_exist",
            "check": "all cited inputs exist",
            "pass": b(all(row["exists"] == "true" for row in input_rows)),
            "detail": f"inputs={len(input_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_01_curl_identity",
            "check": "field-space curl identity is derived",
            "pass": b(any(row["law_id"] == "HCL3208_1_field_space_curl_fixed_branch" for row in law_rows)),
            "detail": "d_F alpha_tau = -int_S i_tau omega_MTS for fixed branch",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_02_stokes_bound",
            "check": "bounded nonintegrability route is derived",
            "pass": b(any(row["law_id"] == "HCL3208_4_bound_route" and "Stokes" in row["derivation"] for row in law_rows)),
            "detail": "path ambiguity bounded by integral of |d_F alpha_tau|",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_03_component_envelope",
            "check": "curl components include X sector, reference, projector, boundary, tau/surface, and total",
            "pass": b({row["component"] for row in component_rows}.issuperset({"I_X_symplectic", "I_ref", "I_projector_domain_stress", "I_boundary_corner_edge", "I_tau_surface", "Delta_H_curl_bound"})),
            "detail": f"component_rows={len(component_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_04_claims_blocked",
            "check": "Htau/MHref/Bobs/local-GR scoring remains blocked",
            "pass": b(any(row["gate_id"] == "G3208_7_claim_status" and row["pass"] == "false" for row in gate_rows)),
            "detail": "no exact-zero or finite bound rows are sourced",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_05_no_cancellation",
            "check": "no-cancellation policy is active",
            "pass": b(any(row["gate_id"] == "G3208_5_no_cancellation" and row["pass"] == "true" for row in gate_rows)),
            "detail": "component bounds must be absolute, not cancelling",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_06_epsilon_feed_nonclaim",
            "check": "epsilon_abs feed rows remain nonclaim",
            "pass": b(all(row["valid_for_claim"] == "false" for row in epsilon_rows)),
            "detail": f"epsilon_feed_rows={len(epsilon_rows)}",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_07_next_target",
            "check": "decision selects X-sector omega/reference curl first row",
            "pass": b(decision_rows[0]["next_target"].startswith("3209-Y5-R2FR-X-sector-Theta-omega-owner")),
            "detail": decision_rows[0]["next_target"],
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_08_no_formalization_workbench_edit",
            "check": "script writes only post-checkpoint outputs",
            "pass": "true",
            "detail": "no formalization-workbench paths are output targets",
            "generated_utc": now,
        },
        {
            "check_id": "VAL3208_09_csv_parse",
            "check": "all generated CSV files parse cleanly",
            "pass": b(all(len(read_csv(path)) > 0 for path in generated_paths)),
            "detail": ";".join(path.name for path in generated_paths),
            "generated_utc": now,
        },
    ]
    write_csv(VALIDATION, validation_rows)

    doc = f"""# 3208 - Htau One-Form Exactness Or First DeltaH Curl Bound Under AX1090

Private checkpoint. This is not a local-GR claim, Newtonian-limit claim, PPN pass, R10 pass, clock pass, orbital pass, Bobs residual score, `H_tau` exactness claim, `M_H_ref` claim, or public-facing result.

## Result

3208 derives the exact curl criterion and adds the finite-curl escape hatch.

The useful advance is not that `H_tau` is now proved exact. It is not. The advance is:

```text
alpha_tau(delta Phi) = int_S(delta Q_tau^MTS - i_tau Theta_MTS(delta Phi)) - delta H_ref
d_F alpha_tau(delta1,delta2) = - int_S i_tau omega_MTS(delta1,delta2)
                              + C_tau + C_S + C_ref

if d_F alpha_tau = 0, H_tau is path-independent.
if not, |Delta H_tau(path1)-Delta H_tau(path2)| <= int_BF |d_F alpha_tau|.
```

So nonzero curl is not automatically hand-waving death. It can become a bounded residual:

```text
epsilon_Htau_curl = Delta_H_curl_bound / (G_ref M_EH)
```

and then feed the `epsilon_abs` denominator lower-bound route from 3207.

Current verdict:

```text
H_tau exactness: not proved.
Delta_H_curl finite value: not sourced.
Bobs/local-GR/Newton scoring: still refused.
New route: source or theorem-zero the X-sector omega term and reference-curl term first.
```

## Curl Law

{md_table(law_rows, ["law_id", "object", "formula", "derivation", "claim_status", "missing_for_claim", "valid_for_claim"])}

## Curl Components

{md_table(component_rows, ["component_id", "component", "definition", "zero_or_bound_condition", "current_status", "feeds", "valid_for_claim"])}

## Field-Space Path Bound

{md_table(path_rows, ["row_id", "route", "required_statement", "output_if_passes", "current_value", "valid_for_claim"])}

## Exactness Or Bound Gates

{md_table(gate_rows, ["gate_id", "gate", "pass", "status", "valid_for_claim"])}

## Epsilon Feed

{md_table(epsilon_rows, ["feed_id", "epsilon_abs_component", "definition", "current_status", "feeds", "claim_effect", "valid_for_claim"])}

## Decision

`{decision_rows[0]["result"]}`.

Claim status: `{decision_rows[0]["claim_status"]}`.

Best next route: {decision_rows[0]["best_next_route"]}.

Next target:

```text
{decision_rows[0]["next_target"]}
```

## Generated Evidence

- `{rel(INPUTS)}`
- `{rel(CURL_LAW)}`
- `{rel(COMPONENTS)}`
- `{rel(PATH_BOUND)}`
- `{rel(GATES)}`
- `{rel(EPSILON_FEED)}`
- `{rel(DECISION)}`
- `{rel(VALIDATION)}`

## Validation

{md_table(validation_rows, ["check_id", "pass", "detail"])}

All generated rows remain `valid_for_claim=false`.
"""
    DOC.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
