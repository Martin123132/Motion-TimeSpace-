from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "2688"
BRANCH_ID = "Y5_R2FR_PARENT_SORT_CONSTRUCTOR_FROM_MTS_PRIMITIVES_OR_DELTA_W_COMPONENT_VALUES_2688"

ROOT = Path(__file__).resolve().parents[1]
SOURCE_INTAKE = ROOT / "source-intake"
RESIDUALS = SOURCE_INTAKE / "mts_residuals"
LOCAL_BOUNDS = SOURCE_INTAKE / "local_bounds"
WEP_RESIDUALS = SOURCE_INTAKE / "microscope" / "branch_locked_wep" / "residuals"
SOURCE_WEIGHT = SOURCE_INTAKE / "source-weight"

DOC_PATH = ROOT / "2688-Y5-R2FR-parent-sort-constructor-from-MTS-primitives-or-delta-w-component-values.md"

OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_R2FR_2688_SOURCE_REGISTER.csv",
    "constructor_audit": RESIDUALS / "P8_Y5_R2FR_2688_PARENT_SORT_CONSTRUCTOR_AUDIT.csv",
    "exhaustion_gate": RESIDUALS / "P8_Y5_R2FR_2688_CONSTRUCTOR_EXHAUSTION_GATE.csv",
    "nohom_impact": RESIDUALS / "P8_Y5_R2FR_2688_SORT_TO_NOHOM_IMPACT_LEDGER.csv",
    "deltaw_values": RESIDUALS / "P8_Y5_R2FR_2688_DELTAW_COMPONENT_VALUE_REQUIREMENTS_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / "P8_Y5_R2FR_2688_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / "P8_Y5_R2FR_2688_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_2688_CLAIM_GATES.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_R2FR_2688_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_2688_NEXT_TARGET.csv",
    "project_status": RESIDUALS / "P8_Y5_R2FR_2688_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / "P8_Y5_R2FR_2688_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "local_constructor_audit": LOCAL_BOUNDS / "parent_sort_constructor_audit_2688_NONCLAIM.csv",
    "local_deltaw_values": LOCAL_BOUNDS / "deltaw_component_value_requirements_2688_NONCLAIM.csv",
    "wep_constructor_audit": WEP_RESIDUALS / "parent_sort_constructor_audit_2688_NONCLAIM.csv",
    "wep_deltaw_values": WEP_RESIDUALS / "deltaw_component_value_requirements_2688_NONCLAIM.csv",
    "source_weight_deltaw_values": SOURCE_WEIGHT / "DELTAW_COMPONENT_VALUE_REQUIREMENTS_2688_NONCLAIM.csv",
}

SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "source_id": "SRC2688_2687_NEXT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2687_NEXT_TARGET.csv",
        "required_needles": ["NEXT2687_0_selected", "parent sort constructor", "Delta_w component rows remain nonclaim"],
        "purpose": "confirms selected 2688 constructor-or-values target",
    },
    {
        "source_id": "SRC2688_2687_NOHOM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2687_NOHOM_PROOF_ATTEMPT.csv",
        "required_needles": ["NH2687_1_conditional_constructor", "PARENT_SORT_DISJOINTNESS_NOHOM_NOT_DERIVED", "NH2687_5_verdict"],
        "purpose": "imports current no-Hom conditional status",
    },
    {
        "source_id": "SRC2688_2687_BASIS",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R2FR_2687_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv",
        "required_needles": ["DWB2687_0_vector_space", "DWB2687_9_acceptance", "POLICY_WRITTEN_NONCLAIM"],
        "purpose": "imports finite Delta_w component basis",
    },
    {
        "source_id": "SRC2688_1237_PRIMITIVES",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1237_MTS_PRIMITIVE_DERIVATION_AUDIT.csv",
        "required_needles": ["PRIM1237_3_observer_map", "PRIM1237_8_verdict", "DERIVATION_FAILS_CLOSURE_DEMOTION_REQUIRED"],
        "purpose": "imports primitive-to-sorted-grammar attempt",
    },
    {
        "source_id": "SRC2688_1237_CHAIN",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1237_SORTED_GRAMMAR_DERIVATION_CHAIN.csv",
        "required_needles": ["CHAIN1237_0_Qobs", "CHAIN1237_5_source_label_forgetting", "CHAIN1237_7_verdict"],
        "purpose": "imports exact broken links in sorted grammar chain",
    },
    {
        "source_id": "SRC2688_1236_CERT",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1236_PARENT_TYPED_OBJECT_LANGUAGE_CERTIFICATE_ATTEMPT.csv",
        "required_needles": ["CERT1236_0_parent_sorts", "CERT1236_5_source_label_forgetting", "CERTIFICATE_SCHEMA_VALID_NOT_PARENT_DERIVED"],
        "purpose": "imports typed certificate status",
    },
    {
        "source_id": "SRC2688_1220_TYPED",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv",
        "required_needles": ["PTOL1220_3_source_weight_exclusion", "PTOL1220_7_verdict", "PARENT_TYPED_OBJECT_LANGUAGE_SIGNATURE_NOT_DERIVED"],
        "purpose": "imports typed signature/source-weight exclusion gap",
    },
    {
        "source_id": "SRC2688_1045_FUNCTOR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1045_PARENT_MATTER_FUNCTOR_SIGNATURE_AUDIT.csv",
        "required_needles": ["MFS1045_2_matter_bundle_functor", "MFS1045_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_MATTER_FUNCTOR_NOT_SIGNED"],
        "purpose": "imports parent matter functor status",
    },
    {
        "source_id": "SRC2688_2485_NORMAL_FORM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_NORMAL_FORM_2485_NORMAL_FORM_CONTRACT.csv",
        "required_needles": ["NF2485_0_parent_action_skeleton", "SKELETON_WRITTEN_NOT_PARENT_DERIVED", "NF2485_3_Newton_Poisson_gate"],
        "purpose": "imports parent action skeleton and Newton gate",
    },
    {
        "source_id": "SRC2688_2485_GRAMMAR",
        "relative_path": "source-intake/mts_residuals/P8_Y5_PARENT_NORMAL_FORM_2485_DERIVATIVE_GRAMMAR.csv",
        "required_needles": ["DG2485_5_nonminimal_matter", "RETAIN_AS_SHADOW_OR_FINITE_SOURCE_RESIDUAL", "DG2485_6_projector_postvariation"],
        "purpose": "imports derivative grammar/source-shadow loopholes",
    },
    {
        "source_id": "SRC2688_2570_THEOREM",
        "relative_path": "source-intake/mts_residuals/P8_Y5_FIELD_QUOTIENT_2570_THEOREM_ATTEMPT.csv",
        "required_needles": ["THM2570_1_matter_and_coefficient_blindness", "FAILS_CURRENT_SIGNATURE_GATE", "THM2570_2_current_signature_application"],
        "purpose": "imports quotient chain-rule conditional theorem and failed current application",
    },
    {
        "source_id": "SRC2688_2570_GATES",
        "relative_path": "source-intake/mts_residuals/P8_Y5_FIELD_QUOTIENT_2570_CLAIM_GATES.csv",
        "required_needles": ["GATE2570_3_matter_descent", "GATE2570_4_coupling_descent", "GATE2570_5_local_GR_Newton"],
        "purpose": "imports local-GR/Newton claim gates",
    },
    {
        "source_id": "SRC2688_2652_STABILITY",
        "relative_path": "source-intake/mts_residuals/P8_Y5_ASR_DELTAW_MATRIX_2652_ACTION_SCALE_READOUT_STABILITY_ATTEMPT.csv",
        "required_needles": ["ASR2652_1_exact_conditional_theorem", "ACTION_SCALE_READOUT_STABILITY_NOT_PARENT_DERIVED", "ASR2652_6_verdict"],
        "purpose": "imports action-scale/readout stability gap",
    },
    {
        "source_id": "SRC2688_2652_MATRIX",
        "relative_path": "source-intake/mts_residuals/P8_Y5_ASR_DELTAW_MATRIX_2652_DELTAW_ARENA_PROJECTION_MATRIX_NONCLAIM.csv",
        "required_needles": ["DPM2652_0_core_vector", "DPM2652_6_no_cancellation_policy", "SYMBOLIC_MATRIX_ONLY_PARENT_VALUES_MISSING"],
        "purpose": "imports Delta_w projection matrix requirements",
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


def constructor_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "PSC2688_0_target",
            "parent sort constructor from MTS primitives",
            "Build a functor C_MTS: Prim_MTS -> ParentSorts that generates Q_obs, ordinary matter, coefficients, calibration, readout and residual slots before fitting.",
            "TARGET_SHARP",
            "This is the real leap needed to turn the typed no-Hom rule from a grammar discipline into a theorem.",
            "2687:NH2687_5_verdict;1237:PRIM1237_8_verdict",
            "false",
        ),
        (
            "PSC2688_1_Qobs_public_geometry",
            "observed public geometry/readout sort",
            "Motion-load and observer-map work supplies a plausible Q_obs/coframe route for local public geometry.",
            "PARTIAL_CONSTRUCTOR_QOBS_ONLY",
            "The Q_obs lane is promising, but it does not by itself generate the whole parent action grammar or source coefficient domain.",
            "1237:CHAIN1237_0_Qobs;2570:THM2570_0_chain_rule_descent",
            "false",
        ),
        (
            "PSC2688_2_matter_sort",
            "ordinary matter functor sort",
            "Ordinary matter should descend as S_matter[Psi,e_obs(q_parent(Phi)),theta_obs,c_vis] with one Hilbert source extraction.",
            "MATTER_SORT_UNSIGNED",
            "The matter bundle functor, vertical lift, constants split and no-shadow-frame clauses are still contracts rather than parent constructions.",
            "1045:MFS1045_2_matter_bundle_functor;1045:MFS1045_6_verdict",
            "false",
        ),
        (
            "PSC2688_3_active_source_coeff_domain",
            "active source coefficient constructor",
            "Coeff_active_source should be generated only from UniversalCalibration, total Hilbert source data and explicitly retained residual slots.",
            "CONSTRUCTOR_DOMAIN_NOT_DERIVED",
            "No inspected MTS primitive forbids SpeciesLabel, hidden markers, action-measure multipliers or readout selectors from being coefficient arguments.",
            "1220:PTOL1220_3_source_weight_exclusion;1236:CERT1236_5_source_label_forgetting",
            "false",
        ),
        (
            "PSC2688_4_source_label_forgetting",
            "total Hilbert source functor",
            "The source functor must forget source species labels before selecting gravitational/source coupling.",
            "SOURCE_LABEL_FORGETTING_NOT_DERIVED",
            "This is still the hinge: without it, w_A S_A and current-rescale countermodels remain legal.",
            "1237:CHAIN1237_5_source_label_forgetting;2485:DG2485_5_nonminimal_matter",
            "false",
        ),
        (
            "PSC2688_5_no_marker_no_extension",
            "no hidden/material/readout marker extension",
            "No hidden invariant, material marker, boundary selector or readout mask may extend the active-source coefficient domain.",
            "NO_MARKER_EXHAUSTION_UNSIGNED",
            "The current corpus names the guard but does not prove constructor exhaustion.",
            "1236:CERT1236_3_no_extension_marker;2687:NH2687_3_counterexamples",
            "false",
        ),
        (
            "PSC2688_6_action_scale_readout_stability",
            "one-owner action scale plus readout stability",
            "A tree-level source-zero theorem must survive measure, variation order, radiative closure, clocks, WEP, R10 and projector readouts.",
            "ACTION_SCALE_READOUT_STABILITY_UNSIGNED",
            "The exact conditional theorem exists, but one-owner action scale and readout no-reentry are not parent-signed.",
            "2652:ASR2652_1_exact_conditional_theorem;2652:ASR2652_6_verdict",
            "false",
        ),
        (
            "PSC2688_7_local_GR_Newton_effect",
            "effect on local GR/Newton branch",
            "If all constructor clauses closed, source-side residuals would narrow sharply and the local GR/Newton branch could move to equations rather than closures.",
            "DOWNSTREAM_EFFECT_ONLY",
            "Current local GR/Newton gates still require q_parent, EH origin, coupling owner, source normalization and residual silence.",
            "2570:GATE2570_5_local_GR_Newton;2485:NF2485_3_Newton_Poisson_gate",
            "false",
        ),
        (
            "PSC2688_8_verdict",
            "promote parent sort constructor as theorem",
            "Current MTS primitives derive the disjoint parent sorts and active-source constructor domain without syntax decree.",
            "PARENT_SORT_CONSTRUCTOR_NOT_DERIVED",
            "Q_obs is partially constructed, but matter/source coefficient constructor, source-label forgetting, no-marker exhaustion and stability remain unsigned.",
            "PSC2688_0_target through PSC2688_7_local_GR_Newton_effect",
            "false",
        ),
    ]
    return [
        {
            "constructor_id": row[0],
            "claim_piece": row[1],
            "formal_statement": row[2],
            "current_status": row[3],
            "proof_or_obstruction": row[4],
            "source_anchor": row[5],
            "parent_signed": row[6],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def exhaustion_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CEG2688_0_sort_list",
            "parent field/sort list is explicit",
            "PARTIAL_LIST_EXISTS_NOT_EXHAUSTIVE",
            "Q_obs/matter/q/private/projector/memory/boundary/coupling slots are catalogued, but cataloguing is not generation.",
            "2485:FS2485_0_public_geometry through FS2485_7_boundary_reference",
            "false",
        ),
        (
            "CEG2688_1_constructor_image",
            "every active-source coefficient lies in generated constructor image",
            "FAIL_IMAGE_NOT_PROVED",
            "No functor image theorem shows Coeff_active_source excludes species labels and hidden/readout markers.",
            "2687:NH2687_1_conditional_constructor",
            "false",
        ),
        (
            "CEG2688_2_no_shadow_source",
            "no nonminimal matter/source-shadow term survives",
            "FAIL_SHADOW_SOURCE_RETAINED",
            "f(X,Phi,labels)L_m and A(X)J_m remain retained as finite source residuals unless theorem-zero or sourced.",
            "2485:DG2485_5_nonminimal_matter",
            "false",
        ),
        (
            "CEG2688_3_no_measure_action_scale",
            "single parent hbar/action-density/current normalization owner",
            "FAIL_OWNER_NOT_DERIVED",
            "Relative action-scale factors can mimic Delta_w_measure.",
            "2652:ASR2652_2_action_scale_gap;2687:DWB2687_4_action_measure_jacobian",
            "false",
        ),
        (
            "CEG2688_4_no_readout_reentry",
            "readout/projector/effective maps cannot re-enter source coefficient codomain",
            "FAIL_READOUT_STABILITY_NOT_PARENT_DERIVED",
            "Projector commutators and readout transfer rows remain explicit residual channels.",
            "2485:DG2485_6_projector_postvariation;2652:ASR2652_3_readout_gap",
            "false",
        ),
        (
            "CEG2688_5_no_cancellation_guard",
            "finite branch cannot pass by fitted cancellation",
            "PASS_GUARD_ONLY",
            "Use sum_i |K_i Delta_w_i| or a sourced covariance envelope unless a parent identity proves cancellation.",
            "2652:DPM2652_6_no_cancellation_policy;2687:DWB2687_8_no_cancellation_policy",
            "true",
        ),
        (
            "CEG2688_6_verdict",
            "constructor exhaustion can be claimed",
            "CONSTRUCTOR_EXHAUSTION_NOT_PROVED",
            "The route is cleaner, but present evidence does not close the exhaustive constructor theorem.",
            "CEG2688_0_sort_list through CEG2688_5_no_cancellation_guard",
            "false",
        ),
    ]
    return [
        {
            "gate_id": row[0],
            "required_clause": row[1],
            "current_status": row[2],
            "failure_or_guard": row[3],
            "source_anchor": row[4],
            "gate_pass": row[5],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def nohom_impact_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "IMPACT2688_0_nohom",
            "parent no-Hom theorem",
            "WOULD_PROMOTE_IF_CONSTRUCTOR_AND_EXHAUSTION_SIGNED",
            "Hom_parent(SpeciesLabel/Hidden/Readout, Coeff_active_source)=empty_or_common would become theorem-level.",
            "NOT_PROMOTED_CURRENTLY",
        ),
        (
            "IMPACT2688_1_deltaw",
            "finite Delta_w branch",
            "REMAINS_REQUIRED",
            "Because constructor exhaustion failed, Delta_w components must be kept as finite source-ready rows.",
            "NONCLAIM_VALUE_REQUIREMENTS_ONLY",
        ),
        (
            "IMPACT2688_2_local_gr",
            "local GR/Newton source reduction",
            "NARROWS_BUT_DOES_NOT_CLOSE",
            "A signed constructor would help source universality, but local GR still needs EH origin, coupling owner, PPN equations and residual silence.",
            "LOCAL_GR_STILL_BLOCKED",
        ),
        (
            "IMPACT2688_3_best_route",
            "next proof target",
            "TOTAL_PARENT_ACTION_SOURCE_LABEL_FORGETTING",
            "The missing object is not another no-Hom restatement; it is the action/source functor that owns source-label forgetting.",
            "NEXT_TARGET_SELECTED",
        ),
    ]
    return [
        {
            "impact_id": row[0],
            "affected_branch": row[1],
            "effect_if_signed": row[2],
            "current_effect": row[3],
            "status": row[4],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def deltaw_value_requirement_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DWBV2688_0_common_projector",
            "P_perp/common calibration mode",
            "P_perp w with P_perp u_common=0",
            "source-weight vector space and composition weights p_A",
            "dimensionless projector",
            "COMMON_MODE_PROJECTOR_MISSING",
            "false",
        ),
        (
            "DWBV2688_1_delta_w_species",
            "Delta_w_species",
            "w_A=w_common(1+epsilon_A), sum_A p_A epsilon_A=0",
            "parent epsilon_A values or no-Hom theorem-zero, with species/material/source path",
            "dimensionless",
            "PARENT_VALUE_OR_ZERO_THEOREM_MISSING",
            "false",
        ),
        (
            "DWBV2688_2_current_rescale",
            "c_A_current_rescale",
            "Delta J_src=sum_A(c_A-c_common)J_A",
            "source-current owner/no-rescale theorem or coefficient row",
            "dimensionless",
            "CURRENT_OWNER_VALUE_MISSING",
            "false",
        ),
        (
            "DWBV2688_3_marker_hidden",
            "Delta_w_marker_hidden",
            "w_A=w_common[1+epsilon_marker I_marker(A,D,boundary,readout)]",
            "no-marker theorem or finite marker coefficient bounds",
            "dimensionless",
            "NO_MARKER_VALUE_MISSING",
            "false",
        ),
        (
            "DWBV2688_4_measure_action",
            "Delta_w_measure",
            "Delta_w_measure=P_perp log Z_A^measure",
            "single parent action-density/measure owner or numeric Z_A^measure bounds",
            "dimensionless logarithmic response",
            "ACTION_MEASURE_VALUE_MISSING",
            "false",
        ),
        (
            "DWBV2688_5_nonhilbert_current",
            "J_NH_retained",
            "J_src=kappa_univ T_Hilbert + sum_i C_i J_NH_i",
            "formula-level K_owner and q_retained zero proof or finite coefficient row",
            "declared by current channel",
            "NONHILBERT_CURRENT_VALUE_MISSING",
            "false",
        ),
        (
            "DWBV2688_6_mass_projector",
            "Delta_mu_projector",
            "Delta mu_obs=Pi_M(J_Hilbert+J_exchange+J_boundary)-Pi_M(J_Hilbert)",
            "closed calibrated mass projector or finite Delta_mu row",
            "dimensionless or declared GM units",
            "MASS_PROJECTOR_VALUE_MISSING",
            "false",
        ),
        (
            "DWBV2688_7_material_tensor",
            "R_material_X",
            "eta_AB ~ tau_WEP sum_X K_X C_X R_material_X(A,B)",
            "parent X basis, material tensor, coefficient vector, tau/readout/product convention",
            "declared parent-basis response units",
            "MATERIAL_TENSOR_AND_PARENT_VALUES_MISSING",
            "false",
        ),
        (
            "DWBV2688_8_arena_kernels",
            "K_arena/tau_arena/readout kernels",
            "observable_arena=K_arena dot Delta_w_eff with declared tau/readout/source map",
            "R10, WEP, PPN, clock and orbital kernels plus source/test body maps",
            "arena declared",
            "ARENA_PROJECTION_KERNELS_MISSING",
            "false",
        ),
        (
            "DWBV2688_9_no_cancellation",
            "no-cancellation envelope",
            "observable_bound uses sum_i |K_i Delta_w_i| or sourced covariance envelope",
            "parent identity for signed cancellation or no-cancellation policy",
            "policy",
            "POLICY_WRITTEN_GUARD_ONLY",
            "true",
        ),
        (
            "DWBV2688_10_acceptance",
            "finite Delta_w value acceptance",
            "each component has theorem-zero or numeric parent value plus projection kernel before scoring",
            "all component values, uncertainties/bounds, source paths, units, norm, K/tau/material/readout projection",
            "mixed declared by component",
            "FINITE_DELTAW_VALUES_STAGED_NONCLAIM",
            "false",
        ),
    ]
    return [
        {
            "requirement_id": row[0],
            "component": row[1],
            "formula_or_role": row[2],
            "required_source_input": row[3],
            "units": row[4],
            "current_status": row[5],
            "guard_pass": row[6],
            "numeric_value_present": "false",
            "source_path_present": "false",
            "projection_ready": "false",
            "score_ready": "false",
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    cases = [
        ("DRY2688_0_all_parent_signed", "true", "true", "true", "true", "true", "false", "THEOREM_READY_IF_PARENT_SOURCES_SIGNED"),
        ("DRY2688_1_syntax_decree_only", "false", "true", "true", "true", "true", "false", "REJECT_SYNTAX_DECREE_NOT_DERIVATION"),
        ("DRY2688_2_Qobs_only", "true", "false", "false", "false", "false", "false", "REJECT_QOBS_ONLY_NOT_SOURCE_CONSTRUCTOR"),
        ("DRY2688_3_values_missing", "false", "false", "false", "false", "false", "false", "REJECT_CONSTRUCTOR_AND_VALUES_MISSING"),
        ("DRY2688_4_values_without_projection", "false", "false", "false", "false", "true", "false", "REJECT_VALUES_WITHOUT_ARENA_PROJECTION"),
        ("DRY2688_5_cancellation_only", "false", "false", "false", "false", "true", "true", "REJECT_CANCELLATION_ONLY_PASS"),
    ]
    return [
        {
            "case_id": row[0],
            "qobs_route_present": row[1],
            "source_constructor_signed": row[2],
            "constructor_exhaustive": row[3],
            "stability_signed": row[4],
            "finite_values_present": row[5],
            "cancellation_only": row[6],
            "expected_status": row[7],
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for row in cases
    ]


def evaluate_dryrun(case: dict[str, Any]) -> str:
    if case["cancellation_only"] == "true":
        return "REJECT_CANCELLATION_ONLY_PASS"
    if case["source_constructor_signed"] == "true" and case["qobs_route_present"] == "false":
        return "REJECT_SYNTAX_DECREE_NOT_DERIVATION"
    if case["source_constructor_signed"] == "true" and case["constructor_exhaustive"] == "true" and case["stability_signed"] == "true":
        return "THEOREM_READY_IF_PARENT_SOURCES_SIGNED"
    if case["qobs_route_present"] == "true" and case["source_constructor_signed"] == "false":
        return "REJECT_QOBS_ONLY_NOT_SOURCE_CONSTRUCTOR"
    if case["finite_values_present"] == "true":
        return "REJECT_VALUES_WITHOUT_ARENA_PROJECTION"
    if case["constructor_exhaustive"] == "true" and case["source_constructor_signed"] == "false":
        return "REJECT_SYNTAX_DECREE_NOT_DERIVATION"
    return "REJECT_CONSTRUCTOR_AND_VALUES_MISSING"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        computed = evaluate_dryrun(case)
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
        ("CG2688_0_constructor", "parent sort constructor is derived from MTS primitives", "FAIL_PARENT_SORT_CONSTRUCTOR_NOT_DERIVED", "PSC2688_8_verdict", "false"),
        ("CG2688_1_exhaustion", "active-source coefficient constructor is exhaustive", "FAIL_CONSTRUCTOR_EXHAUSTION_NOT_PROVED", "CEG2688_6_verdict", "false"),
        ("CG2688_2_nohom", "no-Hom theorem can be promoted", "FAIL_NOHOM_REMAINS_CONDITIONAL", "IMPACT2688_0_nohom", "false"),
        ("CG2688_3_deltaw_values", "finite Delta_w components have parent values or theorem-zero rows", "FAIL_PARENT_COMPONENT_VALUES_MISSING", "DWBV2688_10_acceptance", "false"),
        ("CG2688_4_projection", "arena kernels/tau/readout/source maps are ready", "FAIL_ARENA_PROJECTIONS_MISSING", "DWBV2688_8_arena_kernels", "false"),
        ("CG2688_5_no_cancellation", "no cancellation-only pass is used", "PASS_GUARD_ONLY", "DWBV2688_9_no_cancellation", "true"),
        ("CG2688_6_verdict", "source coupling/local-GR branch can claim pass", "CLAIM_BLOCKED", "CG2688_0_constructor through CG2688_5_no_cancellation", "false"),
    ]
    return [
        {
            "gate_id": row[0],
            "condition": row[1],
            "current_status": row[2],
            "source_anchor": row[3],
            "gate_pass": row[4],
            "valid_for_claim": "false",
            "claim_allowed": "false",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2688_0_constructor",
            "decision": "DO_NOT_PROMOTE_PARENT_SORT_CONSTRUCTOR",
            "reason": "Q_obs construction exists only as a partial public-geometry lane; source coefficient constructor and exhaustion are unsigned.",
            "status": "DERIVATION_ATTEMPT_FAILED_USEFULLY",
            "next_dependency": "derive total parent action/source-label forgetting or supply finite Delta_w component values",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2688_1_nohom",
            "decision": "KEEP_NOHOM_AS_EXACT_CONDITIONAL",
            "reason": "The no-Hom statement is mathematically clean, but promoting it now would be syntax by decree.",
            "status": "NOHOM_NOT_PROMOTED",
            "next_dependency": "parent action source functor and no-extension theorem",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2688_2_deltaw",
            "decision": "BEGIN_VALUE_REQUIREMENT_BRANCH_WITHOUT_SCORING",
            "reason": "If the zero theorem is not signed, the honest fallback is parent component values plus arena projections, not fitted cancellations.",
            "status": "DELTAW_VALUES_STAGED_NONCLAIM",
            "next_dependency": "component values/theorem-zero rows, kernels, units, source paths and no-cancellation envelope",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
        {
            "decision_id": "DEC2688_3_next",
            "decision": "ATTACK_TOTAL_PARENT_ACTION_SOURCE_LABEL_FORGETTING_NEXT",
            "reason": "The constructor fails because the source functor owner is missing; the next leap should hit that owner directly before any public testing claim.",
            "status": "NEXT_TARGET_SELECTED",
            "next_dependency": "2689 total parent action/source-label forgetting or Delta_w component values",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "NEXT2688_0_selected",
            "kind": "selected",
            "target_doc": "2689-Y5-R2FR-total-parent-action-source-label-forgetting-or-delta-w-component-values.md",
            "target_script": "scripts/Y5_R2FR_total_parent_action_source_label_forgetting_or_delta_w_component_values_2689.py",
            "purpose": "try to derive the action/source functor owner that forgets species labels before source coupling; if it fails, turn Delta_w component requirements into source-ready value rows",
            "acceptance_gate": "either total parent action plus source-label forgetting is parent-signed, or Delta_w component value rows remain nonclaim with explicit value/source/unit/projection blockers",
            "forbidden_shortcuts": "syntax by decree; source labels forgotten by preference; Q_obs-only promotion; Delta_w=0 without parent theorem; cancellation-only pass; GitHub action; formalization-workbench edits",
            "ready_to_run": "true",
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("STATUS2688_0_Qobs", "public geometry/readout", "PARTIAL_QOBS_CONSTRUCTOR_EXISTS", "motion-load/observer map continues to look useful"),
        ("STATUS2688_1_constructor", "parent source constructor", "PARENT_SORT_CONSTRUCTOR_NOT_DERIVED", "source coefficient grammar still lacks parent generation/exhaustion"),
        ("STATUS2688_2_nohom", "source-coupling theorem", "NOHOM_EXACT_CONDITIONAL_ONLY", "not a dead end, but not a theorem claim"),
        ("STATUS2688_3_finite_values", "Delta_w fallback", "VALUE_REQUIREMENTS_STAGED_NONCLAIM", "finite route is now pointed at component values and arena kernels"),
        ("STATUS2688_4_local_gr", "local GR/Newton", "STILL_BLOCKED_BUT_NARROWER", "source universality is the missing hinge before equations can carry more weight"),
    ]
    return [
        {
            "status_id": row[0],
            "sector": row[1],
            "status": row[2],
            "meaning": row[3],
            "claim_allowed": "false",
            "next_action": "run 2689 total parent action/source-label forgetting target",
            "timestamp_utc": stamp(),
        }
        for row in rows
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": f"BC2688_{name}",
            "absolute_path": str(path),
            "relative_path": rel_path(path),
            "exists": as_bool(path.exists()),
            "valid_for_claim": "false",
            "timestamp_utc": stamp(),
        }
        for name, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    source_rows: list[dict[str, Any]],
    constructor: list[dict[str, Any]],
    exhaustion: list[dict[str, Any]],
    impact: list[dict[str, Any]],
    deltaw: list[dict[str, Any]],
    dryrun_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC_PATH]
    sources_ok = all(row["exists"] == "true" and not row["missing_needles"] for row in source_rows)
    qobs_partial = any(row["constructor_id"] == "PSC2688_1_Qobs_public_geometry" and row["current_status"] == "PARTIAL_CONSTRUCTOR_QOBS_ONLY" for row in constructor)
    verdict_blocked = any(row["constructor_id"] == "PSC2688_8_verdict" and row["current_status"] == "PARENT_SORT_CONSTRUCTOR_NOT_DERIVED" for row in constructor)
    exhaustion_blocked = any(row["gate_id"] == "CEG2688_6_verdict" and row["current_status"] == "CONSTRUCTOR_EXHAUSTION_NOT_PROVED" for row in exhaustion)
    nohom_not_promoted = any(row["impact_id"] == "IMPACT2688_0_nohom" and row["status"] == "NOT_PROMOTED_CURRENTLY" for row in impact)
    deltaw_nonclaim = all(
        row["valid_for_claim"] == "false"
        and row["claim_allowed"] == "false"
        and row["score_ready"] == "false"
        and row["numeric_value_present"] == "false"
        for row in deltaw
    )
    no_cancel_guard = any(row["requirement_id"] == "DWBV2688_9_no_cancellation" and row["guard_pass"] == "true" for row in deltaw)
    dryrun_ok = all(row["status_match"] == "true" and row["claim_allowed"] == "false" for row in dryrun_results)
    claim_blocked = all(row["valid_for_claim"] == "false" and row["claim_allowed"] == "false" for row in claim_gates)
    overall_claim_blocked = any(row["gate_id"] == "CG2688_6_verdict" and row["current_status"] == "CLAIM_BLOCKED" for row in claim_gates)
    csv_checks = {str(path): parse_csv(path) for path in list(OUTPUTS.values())[:-1]}
    branch_checks = {str(path): parse_csv(path) for path in BRANCH_OUTPUTS.values()}
    csv_ok = all(ok for ok, _, _ in csv_checks.values())
    branch_ok = all(ok for ok, _, _ in branch_checks.values())
    formalization_guard = all("formalization-workbench" not in str(path).lower() for path in output_paths)
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    next_target_ok = parse_csv(OUTPUTS["next_target"])[0] and "2689" in read_text(OUTPUTS["next_target"])
    checks = [
        ("VAL2688_sources_exist_and_needles_found", sources_ok, "all cited source paths exist and required needles were found"),
        ("VAL2688_qobs_partial_route_retained", qobs_partial, "Q_obs/public geometry route is retained as partial positive result"),
        ("VAL2688_constructor_not_promoted", verdict_blocked, "parent sort constructor is not promoted"),
        ("VAL2688_exhaustion_blocked", exhaustion_blocked, "constructor exhaustion remains blocked"),
        ("VAL2688_nohom_not_promoted", nohom_not_promoted, "no-Hom remains exact conditional only"),
        ("VAL2688_deltaw_values_nonclaim", deltaw_nonclaim, "Delta_w value rows are nonclaim and not score-ready"),
        ("VAL2688_no_cancellation_guard", no_cancel_guard, "no-cancellation guard is present"),
        ("VAL2688_dryrun_refusals", dryrun_ok, "dry-run refuses syntax decree, Q_obs-only, missing values/projections and cancellation-only cases"),
        ("VAL2688_claim_gates_block_claims", claim_blocked and overall_claim_blocked, "all claim gates block promotion"),
        ("VAL2688_csv_parse", csv_ok, f"parsed {len(csv_checks)} output CSVs"),
        ("VAL2688_branch_copies_parse", branch_ok, f"parsed {len(branch_checks)} branch-copy CSVs"),
        ("VAL2688_formalization_write_guard", formalization_guard, "no output path targets formalization-workbench"),
        ("VAL2688_pycache_absent_at_validation_time", pycache_absent, "scripts/__pycache__ absent when validation rows were built"),
        ("VAL2688_next_target_selected", next_target_ok, "2689 total parent action/source-label forgetting target selected"),
    ]
    overall = all(ok for _, ok, _ in checks)
    rows = [
        {"check_id": check_id, "passed": as_bool(ok), "detail": detail, "timestamp_utc": stamp()}
        for check_id, ok, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2688_OVERALL",
            "passed": as_bool(overall),
            "detail": "2688 tests the parent sort constructor leap, keeps Q_obs as a partial win, refuses no-Hom promotion, and stages Delta_w component value requirements",
            "timestamp_utc": stamp(),
        }
    )
    return rows


def write_document(
    source_rows: list[dict[str, Any]],
    constructor: list[dict[str, Any]],
    exhaustion: list[dict[str, Any]],
    impact: list[dict[str, Any]],
    deltaw: list[dict[str, Any]],
    dry_cases: list[dict[str, Any]],
    dry_results: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    status: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC_PATH.write_text(
        "\n".join(
            [
                "# 2688 - Y5/R2FR Parent Sort Constructor from MTS Primitives or Delta-w Component Values",
                "",
                "## Private Verdict",
                "",
                "Best shot taken: the parent sort constructor does not close yet. The good news is not trivial: the Q_obs / public-geometry route is a real partial constructor, not fluff. The bad news is that it does not generate the active-source coefficient domain.",
                "",
                "The exact missing hinge is now sharper: derive a total parent action/source functor that forgets species/source labels before source coupling, or keep Delta_w as a finite component vector with value/source/unit/projection requirements.",
                "",
                "No no-Hom, Delta_w=0, local-GR, WEP, R10, PPN, clock, orbital, Newton-source, or GitHub/public claim is allowed from this checkpoint.",
                "",
                "## Source Register",
                "",
                markdown_table(source_rows),
                "",
                "## Parent Sort Constructor Audit",
                "",
                markdown_table(constructor),
                "",
                "## Constructor Exhaustion Gate",
                "",
                markdown_table(exhaustion),
                "",
                "## Sort-to-NoHom Impact Ledger",
                "",
                markdown_table(impact),
                "",
                "## Delta-w Component Value Requirements",
                "",
                markdown_table(deltaw),
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
    constructor = constructor_audit_rows()
    exhaustion = exhaustion_gate_rows()
    impact = nohom_impact_rows()
    deltaw = deltaw_value_requirement_rows()
    dry_cases = dryrun_case_rows()
    dry_results = dryrun_result_rows(dry_cases)
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    status = project_status_rows()

    write_csv(OUTPUTS["source_register"], source_rows)
    write_csv(OUTPUTS["constructor_audit"], constructor)
    write_csv(OUTPUTS["exhaustion_gate"], exhaustion)
    write_csv(OUTPUTS["nohom_impact"], impact)
    write_csv(OUTPUTS["deltaw_values"], deltaw)
    write_csv(OUTPUTS["dryrun_cases"], dry_cases)
    write_csv(OUTPUTS["dryrun_results"], dry_results)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision_ledger"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)
    write_csv(OUTPUTS["project_status"], status)

    write_csv(BRANCH_OUTPUTS["local_constructor_audit"], constructor)
    write_csv(BRANCH_OUTPUTS["local_deltaw_values"], deltaw)
    write_csv(BRANCH_OUTPUTS["wep_constructor_audit"], constructor)
    write_csv(BRANCH_OUTPUTS["wep_deltaw_values"], deltaw)
    write_csv(BRANCH_OUTPUTS["source_weight_deltaw_values"], deltaw)

    branch_copies = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    validation = validation_rows(source_rows, constructor, exhaustion, impact, deltaw, dry_results, claim_gates)
    write_csv(OUTPUTS["validation"], validation)
    write_document(source_rows, constructor, exhaustion, impact, deltaw, dry_cases, dry_results, claim_gates, decisions, next_target, status, validation)

    print(f"wrote {DOC_PATH}")
    for key, path in OUTPUTS.items():
        print(f"{key}: {path}")
    for key, path in BRANCH_OUTPUTS.items():
        print(f"{key}: {path}")


if __name__ == "__main__":
    main()
