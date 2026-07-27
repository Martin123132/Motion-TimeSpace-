from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2636-Y5-R2FR-generator-elimination-priority-or-effective-GR-residual-vector-source-pack.md"

PREFIX = "P8_Y5_GENERATOR_EFFECTIVE_PACK_2636"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "generator_priority": RESIDUALS / f"{PREFIX}_GENERATOR_PRIORITY_MATRIX.csv",
    "theorem_zero": RESIDUALS / f"{PREFIX}_THEOREM_ZERO_ROUTE_GATE.csv",
    "effective_pack": RESIDUALS / f"{PREFIX}_EFFECTIVE_RESIDUAL_SOURCE_PACK.csv",
    "ppn_interface": RESIDUALS / f"{PREFIX}_PPN_INTERFACE_MAP.csv",
    "test_readiness": RESIDUALS / f"{PREFIX}_TEST_READINESS_GATES.csv",
    "route_guards": RESIDUALS / f"{PREFIX}_ROUTE_GUARDS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2636_VALIDATION.csv",
}

SOURCES = [
    {
        "source_id": "SRC2636_00_2635",
        "role": "immediate source-hunt freeze and generator queue",
        "path": ROOT / "2635-Y5-R2FR-universal-property-source-hunt-or-effective-residual-branch-freeze.md",
        "needles": ["UNIVERSAL_PROPERTY_ROUTE_FROZEN_AS_AXIOM_ONLY", "GEN2635_0_readout_projector", "VAL2635_OVERALL"],
    },
    {
        "source_id": "SRC2636_01_2623",
        "role": "primitive quotient marker/tower generator list",
        "path": ROOT / "2623-Y5-R2FR-primitive-quotient-no-natural-marker-no-integrated-out-tower-or-residual-bounds.md",
        "needles": ["PQT2623_3_no_extension_universal_property", "MRK2623_0_readout_projector", "TOW2623_4_overall", "VAL2623_OVERALL"],
    },
    {
        "source_id": "SRC2636_02_2625",
        "role": "field-domain certificate failure and readout residual template",
        "path": ROOT / "2625-Y5-R2FR-field-by-field-parent-domain-certificate-or-readout-residual-closure.md",
        "needles": ["FIELD_DOMAIN_CERTIFICATE_DOES_NOT_CLOSE", "RRT2625_0_E_readout_total", "VAL2625_OVERALL"],
    },
    {
        "source_id": "SRC2636_03_2633",
        "role": "parent-normal-form and effective residual vector synthesis",
        "path": ROOT / "2633-Y5-R2FR-parent-normal-form-DObs-EH-current-branch-synthesis-or-full-PPN-residual-fill.md",
        "needles": ["PARENT_NORMAL_FORM_GATE_WRITTEN_NOT_PASSED", "BLK2633_6_Delta_PPN_abs", "VAL2633_OVERALL"],
    },
    {
        "source_id": "SRC2636_04_2634",
        "role": "parent-action generating principle failure and source-hunt handoff",
        "path": ROOT / "2634-Y5-R2FR-parent-action-generating-principle-or-effective-GR-residual-branch.md",
        "needles": ["GENERATING_PRINCIPLE_NOT_DERIVED_CURRENT_CORPUS", "2635-Y5-R2FR-universal-property-source-hunt", "VAL2634_OVERALL"],
    },
    {
        "source_id": "SRC2636_05_2631",
        "role": "full PPN vector and source-prefactor coupling frontier",
        "path": ROOT / "2631-Y5-R2FR-current-branch-no-shadow-full-PPN-vector-or-residual-kernel-fill.md",
        "needles": ["FULL_PPN_VECTOR_IS_CURRENT_BRANCH_INTERFACE", "SOURCE_PREFACTOR_COUPLING_IS_NEXT_BEST_LEAP", "VAL2631_OVERALL"],
    },
    {
        "source_id": "SRC2636_06_2489",
        "role": "first PPN kernel and no-gamma-only guard",
        "path": ROOT / "2489-Y5-R2FR-first-common-frame-PPN-response-kernel-or-parent-no-shadow-clause.md",
        "needles": ["GAMMA_ONLY_PASS_FORBIDDEN", "PPNV2489_7_total_abs", "VAL2489_OVERALL"],
    },
    {
        "source_id": "SRC2636_07_2635_queue_csv",
        "role": "machine-readable generator elimination queue",
        "path": RESIDUALS / "P8_Y5_UNIVERSAL_PROPERTY_HUNT_2635_GENERATOR_ELIMINATION_QUEUE.csv",
        "needles": ["GEN2635_0_readout_projector", "GEN2635_4_domain_boundary_topology"],
    },
    {
        "source_id": "SRC2636_08_2635_pack_csv",
        "role": "machine-readable effective residual seed",
        "path": RESIDUALS / "P8_Y5_UNIVERSAL_PROPERTY_HUNT_2635_EFFECTIVE_RESIDUAL_PACK_SEED.csv",
        "needles": ["E_readout_total", "Delta_PPN_abs"],
    },
]


def ensure_dirs() -> None:
    for directory in (RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE):
        directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        return bool(read_csv(path))
    except Exception:
        return False


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
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *[
                "| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |"
                for row in rows
            ],
        ]
    )


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        text = read_text(source["path"])
        exists = source["path"].exists()
        needles_present = exists and all(needle in text for needle in source["needles"])
        rows.append(
            {
                "timestamp_utc": now(),
                "source_id": source["source_id"],
                "role": source["role"],
                "source_path": str(source["path"]),
                "exists": bool_text(exists),
                "needles_present": bool_text(needles_present),
                "needles": "; ".join(source["needles"]),
                "valid_for_claim": "False",
            }
        )
    return rows


def generator_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "priority": 1,
            "generator_id": "GEN2635_0_readout_projector",
            "source_queue_status": "CLOSURE_DISCIPLINED_NOT_THEOREM_ZERO",
            "parent_countermodel": "readout/projector section or varied reduced action can reintroduce source/operator terms",
            "theorem_zero_route": "closed Conf_parent/Args(S_parent) certificate with readout strictly after variation",
            "theorem_zero_route_status": "FAILED_CURRENTLY_FROM_2625",
            "residual_owner": "E_readout_total;projector_norm;marker_readout",
            "required_source_pack": "S_red form; P_read definition; variation path; source/readout provenance; units; projection kernel; baseline",
            "arenas": "PPN;WEP;R10;clocks;orbital",
            "selected_next": "True",
            "valid_for_claim": "False",
        },
        {
            "priority": 2,
            "generator_id": "GEN2635_1_continuous_marker_scalar",
            "source_queue_status": "OBSTRUCTION_PROVED_IF_INVARIANT_SCALAR_SURVIVES",
            "parent_countermodel": "covariant invariant scalar or memory marker can multiply R or source a fifth-force/clock sector",
            "theorem_zero_route": "generator-specific local invariant algebra triviality or no-natural-marker theorem",
            "theorem_zero_route_status": "GLOBAL_ROUTE_REJECTED_CURRENTLY",
            "residual_owner": "marker_scalar_coefficients;F_sigma_R;memory_scalar_amplitude",
            "required_source_pack": "scalar list; coupling term; coefficient units; source path; arena projection; zero-mode/boundary rule",
            "arenas": "PPN;R10;clocks;WEP",
            "selected_next": "False",
            "valid_for_claim": "False",
        },
        {
            "priority": 3,
            "generator_id": "GEN2635_2_species_constants_source_weights",
            "source_queue_status": "UNIVERSALITY_NOT_PARENT_DERIVED",
            "parent_countermodel": "species/source prefactor w_A S_A changes Hilbert source while preserving neat Ward-looking equations",
            "theorem_zero_route": "single label-forgotten matter functional plus no pre-action source prefactors plus projected mass owner",
            "theorem_zero_route_status": "OPEN_BUT_UNSIGNED_FROM_2631_2632_CHAIN",
            "residual_owner": "w_R;Delta_w;beta_w_source;beta_w_test;E_norm",
            "required_source_pack": "component basis; source species; tau/K/Qbar projections; WEP/clock/PPN/R10 baselines; units",
            "arenas": "WEP;clock;source_normalization;PPN;R10",
            "selected_next": "False",
            "valid_for_claim": "False",
        },
        {
            "priority": 4,
            "generator_id": "GEN2635_3_integrated_out_tower",
            "source_queue_status": "NO_TOWER_THEOREM_NOT_DERIVED",
            "parent_countermodel": "integrating out hidden scalar/vector/tensor sectors can regenerate R2/f(R)/Ricci2/Weyl2/nonlocal kernels",
            "theorem_zero_route": "sector Hessian plus source-independent solution audit or parent no-tower theorem",
            "theorem_zero_route_status": "NOT_DERIVED_FROM_2623_2633",
            "residual_owner": "DeltaE_MTS;R11_residual_operator;tower_operator_coefficients",
            "required_source_pack": "operator basis; coefficient dimensions; mass scale; projection kernel; PPN/R10/orbital comparator; no-cancellation rule",
            "arenas": "PPN;R10;orbital;local_GR",
            "selected_next": "False",
            "valid_for_claim": "False",
        },
        {
            "priority": 5,
            "generator_id": "GEN2635_4_domain_boundary_topology",
            "source_queue_status": "CONDITIONALLY_SAFE_NOT_DERIVED",
            "parent_countermodel": "domain class, endpoint, boundary charge, or local/cosmology split can become a hidden selector",
            "theorem_zero_route": "stress-free/no-flux/topological silence and boundary/domain no-hair theorem",
            "theorem_zero_route_status": "CONDITIONAL_ONLY",
            "residual_owner": "epsilon_endpoint_R;domain_class_residual;boundary_charge;delta_GM_readout_tail",
            "required_source_pack": "domain definition; endpoint map; boundary condition; orbital/light-time projection; baseline and units",
            "arenas": "orbital;R10;PPN;clocks;cosmology_local_split",
            "selected_next": "False",
            "valid_for_claim": "False",
        },
    ]


def theorem_zero_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "TZ2636_0_readout_domain",
            "target_zero": "E_readout_total=0 and projector_norm=0",
            "source_basis": "2625;2635",
            "required_clauses": "readout not in Conf_parent; readout not in Args(S_parent); variation before projection; no representative section coefficient",
            "current_result": "READOUT_ZERO_DEMOTED_TO_CLOSURE",
            "theorem_zero_claimed": "False",
            "fallback_residual_rows": "E_readout_total;projector_norm;marker_readout",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TZ2636_1_marker_scalar",
            "target_zero": "all continuous marker scalar coefficients vanish",
            "source_basis": "2623;2635",
            "required_clauses": "local invariant algebra triviality; no nonconstant natural marker functor; zero source/boundary mode",
            "current_result": "GLOBAL_NO_MARKER_ROUTE_REJECTED_OR_UNSIGNED",
            "theorem_zero_claimed": "False",
            "fallback_residual_rows": "marker_scalar_coefficients;memory_scalar_amplitude;F_sigma_R",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TZ2636_2_species_source_weights",
            "target_zero": "w_R=Delta_w=beta_w_source=0",
            "source_basis": "2631;2633;2635",
            "required_clauses": "single matter functional; no pre-action prefactors; projected mass/source-current owner before readout",
            "current_result": "SOURCE_PREFACTOR_COUPLING_OPEN_UNSIGNED",
            "theorem_zero_claimed": "False",
            "fallback_residual_rows": "w_R;Delta_w;beta_w_source;E_norm",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TZ2636_3_integrated_out_tower",
            "target_zero": "DeltaE_MTS=0 and no R2/fR/Ricci2/Weyl2/nonlocal tower survives",
            "source_basis": "2623;2633;2634",
            "required_clauses": "source-independent auxiliary solution; positive Hessian/large mass or zero coupling; locality kernel; operator-basis projection",
            "current_result": "NO_TOWER_THEOREM_NOT_DERIVED",
            "theorem_zero_claimed": "False",
            "fallback_residual_rows": "DeltaE_MTS;R11_residual_operator;tower_operator_coefficients",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TZ2636_4_boundary_domain",
            "target_zero": "epsilon_endpoint_R=domain_class_residual=boundary_charge=0",
            "source_basis": "2623;2489;2631",
            "required_clauses": "stress-free/no-flux boundary; topological silence; endpoint/readout stability; no hidden local/cosmology selector",
            "current_result": "CONDITIONALLY_SAFE_NOT_DERIVED",
            "theorem_zero_claimed": "False",
            "fallback_residual_rows": "epsilon_endpoint_R;domain_class_residual;delta_GM_readout_tail",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "TZ2636_5_full_ppn_vector",
            "target_zero": "Delta_PPN_abs=0",
            "source_basis": "2489;2631;2633",
            "required_clauses": "delta_p/q_R, b_R, beta, d_R, w_R, endpoint and readout components all zero or numerically sourced",
            "current_result": "FULL_VECTOR_INTERFACE_READY_VALUES_MISSING",
            "theorem_zero_claimed": "False",
            "fallback_residual_rows": "Delta_PPN_abs componentwise no-cancellation vector",
            "valid_for_claim": "False",
        },
    ]


def effective_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "EFF2636_0",
            "symbol": "e_EH_import",
            "owner_generator": "integrated_out_tower/parent_normal_form",
            "role": "EH import residual: using EH because GR works rather than deriving EH from MTS",
            "units_required": "dimensionless coefficient relative to EH operator or explicit operator-density units",
            "numeric_value_status": "MISSING_PARENT_ORIGIN",
            "source_path_required": "parent normal-form source proving or bounding EH import",
            "projection_kernel_required": "local weak-field operator projection",
            "baseline_required": "GR/EH local weak-field baseline",
            "no_cancellation_rule": "cannot be cancelled against DeltaE_MTS or readout terms",
            "arenas": "local_GR;Newton;PPN",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_1",
            "symbol": "e_kappaG",
            "owner_generator": "species_constants_source_weights",
            "role": "parent-to-measured-G coupling transfer residual",
            "units_required": "dimensionless fractional G transfer or explicit kappa mapping",
            "numeric_value_status": "MISSING_KAPPA_OWNER",
            "source_path_required": "parent normalization/source-worldtube convention",
            "projection_kernel_required": "Newtonian Poisson and orbital GM projection",
            "baseline_required": "measured G/GM fixed before test readout",
            "no_cancellation_rule": "fitted GM absorption is forbidden",
            "arenas": "Newton;orbital;PPN;WEP",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_2",
            "symbol": "DeltaE_MTS",
            "owner_generator": "integrated_out_tower",
            "role": "non-EH local operator residual in the public field equation",
            "units_required": "same rank-2 field-equation units as G_mn/T_mn or dimensionless response after projection",
            "numeric_value_status": "MISSING_OPERATOR_BOUNDS",
            "source_path_required": "operator-basis and coefficient source path",
            "projection_kernel_required": "PPN/R10/orbital weak-field projection",
            "baseline_required": "EH plus matter baseline",
            "no_cancellation_rule": "absolute operator envelope; no paired cancellation against source/readout tails",
            "arenas": "PPN;R10;orbital;local_GR",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_3",
            "symbol": "E_readout_total",
            "owner_generator": "readout_projector",
            "role": "readout/reduced-action backreaction residual",
            "units_required": "field-equation operator density or normalized dimensionless projected amplitude",
            "numeric_value_status": "MISSING_READOUT_ACTION_FORM",
            "source_path_required": "S_red form, P_read definition, variation path, readout/source provenance",
            "projection_kernel_required": "PPN/WEP/R10/clocks/orbital readout projection",
            "baseline_required": "variation-before-readout parent baseline",
            "no_cancellation_rule": "readout tail must be bounded independently before local scoring",
            "arenas": "PPN;WEP;R10;clocks;orbital",
            "status": "SELECTED_FIRST_SOURCE_PACK",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_4",
            "symbol": "projector_norm",
            "owner_generator": "readout_projector",
            "role": "commutator/projection leakage if P_read becomes a branch operator",
            "units_required": "1/length or dimensionless normalized commutator norm",
            "numeric_value_status": "MISSING_PROJECTOR_DEFINITION",
            "source_path_required": "projector definition, local domain, derivative operator, norm convention",
            "projection_kernel_required": "clock/source/PPN local projection",
            "baseline_required": "P_read absent from parent action",
            "no_cancellation_rule": "cannot be hidden inside gauge/readout calibration",
            "arenas": "WEP;clocks;R10;PPN",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_5",
            "symbol": "marker_scalar_coefficients",
            "owner_generator": "continuous_marker_scalar",
            "role": "F(sigma)R, memory scalar, or invariant scalar coefficient residual",
            "units_required": "coefficient-dependent: dimensionless prefactor, mass scale, or inverse-length powers",
            "numeric_value_status": "MISSING_SCALAR_GENERATOR_COMPONENTS",
            "source_path_required": "surviving scalar list and coupling grammar",
            "projection_kernel_required": "PPN/R10/clock/fifth-force projection",
            "baseline_required": "no-marker parent route or finite coefficient row",
            "no_cancellation_rule": "each scalar component carried separately before sums",
            "arenas": "PPN;R10;clocks;WEP",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_6",
            "symbol": "w_R;Delta_w;beta_w_source;beta_w_test",
            "owner_generator": "species_constants_source_weights",
            "role": "source-prefactor/source-current/matter-normalization residual vector",
            "units_required": "dimensionless source/action-weight response components",
            "numeric_value_status": "MISSING_COMPONENT_VECTOR",
            "source_path_required": "no-source-prefactor theorem or finite component basis",
            "projection_kernel_required": "WEP, clock, PPN beta/gamma, R10 source-leg projection",
            "baseline_required": "single matter functional and projected mass owner before readout",
            "no_cancellation_rule": "species/source components use absolute envelope, not relative cancellation",
            "arenas": "WEP;clock;source_normalization;PPN;R10",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_7",
            "symbol": "DObs_e_R",
            "owner_generator": "readout_projector/continuous_marker_scalar",
            "role": "observed coframe/readout leak from hidden or radial-cell directions",
            "units_required": "dimensionless coframe/readout response or explicit Jacobian units",
            "numeric_value_status": "DOBS_E_KERNEL_NOT_SIGNED",
            "source_path_required": "terminal public coframe and no-hidden-visible morphism proof or bound",
            "projection_kernel_required": "PPN, clock, orbital, source-normalization projection",
            "baseline_required": "ordinary matter and clocks factor through public coframe",
            "no_cancellation_rule": "readout/coframe leakage is additive in full PPN envelope",
            "arenas": "PPN;clocks;orbital;WEP",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_8",
            "symbol": "d_R_preferred_frame",
            "owner_generator": "domain_boundary_topology/continuous_marker_scalar",
            "role": "disformal/preferred-frame residual response matrix",
            "units_required": "dimensionless preferred-frame response components",
            "numeric_value_status": "MISSING_DISFORMAL_PREFERRED_FRAME_PROJECTION",
            "source_path_required": "no-disformal slot or normalized disformal ansatz",
            "projection_kernel_required": "alpha1/alpha2/alpha3/xi/gamma response matrix",
            "baseline_required": "public metric/coframe with no preferred-frame shadow",
            "no_cancellation_rule": "preferred-frame components independently bounded",
            "arenas": "PPN;orbital;pulsar",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_9",
            "symbol": "epsilon_endpoint_R;alpha_readout;delta_GM",
            "owner_generator": "domain_boundary_topology/readout_projector",
            "role": "endpoint, boundary, measured-GM and post-variation readout tails",
            "units_required": "dimensionless tail amplitudes or observable-specific timing/orbital units",
            "numeric_value_status": "MISSING_ENDPOINT_READOUT_KERNEL",
            "source_path_required": "endpoint silence, GM calibration, PPN gauge and readout stability source",
            "projection_kernel_required": "orbital/light-time/PPN/clock projection",
            "baseline_required": "source mass and gauge fixed before local comparison",
            "no_cancellation_rule": "no fitted-GM or endpoint cancellation shortcut",
            "arenas": "orbital;PPN;clocks;local_GR",
            "status": "BLOCKED_SOURCE_REQUIRED",
            "valid_for_claim": "False",
        },
        {
            "pack_id": "EFF2636_10",
            "symbol": "Delta_PPN_abs",
            "owner_generator": "all_generators",
            "role": "componentwise full local PPN no-cancellation envelope",
            "units_required": "dimensionless absolute PPN residual vector",
            "numeric_value_status": "SCHEMA_READY_VALUES_MISSING",
            "source_path_required": "component source rows for delta_p, b_R, beta, d_R, w_R, endpoint and readout",
            "projection_kernel_required": "Cassini/Mercury/LLR/pulsar/preferred-frame response basis",
            "baseline_required": "fitted LCDM/GR-like local baseline with no gamma-only pass",
            "no_cancellation_rule": "sum absolute components; no pair-cancellation shortcut",
            "arenas": "PPN;local_GR;Newton",
            "status": "BLOCKED_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def ppn_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "ppn_id": "PPNI2636_0_delta_p_qR",
            "component_symbol": "delta_p;q_R_hat",
            "generator_links": "domain_boundary_topology;reciprocal_lock",
            "observable_channels": "gamma_minus_1;beta_minus_1;local_GR_Newton",
            "current_source": "2489;2631",
            "comparator_status": "Cassini_gamma_comparator_only_not_claim",
            "required_value_or_theorem": "no-boundary-charge/source-descent theorem or finite source-normalized q_R_hat row",
            "guard": "no gamma-only pass",
            "valid_for_claim": "False",
        },
        {
            "ppn_id": "PPNI2636_1_bR_DObs",
            "component_symbol": "b_R;DObs_e_R",
            "generator_links": "readout_projector;terminal_public_coframe",
            "observable_channels": "gamma_minus_1;light_time;clocks",
            "current_source": "2489;2631;2633",
            "comparator_status": "conditional kernel ready but value/theorem missing",
            "required_value_or_theorem": "no-Weyl/no-shadow terminal public coframe or finite b_R/DObs_e row",
            "guard": "coframe/readout leak carried additively",
            "valid_for_claim": "False",
        },
        {
            "ppn_id": "PPNI2636_2_beta",
            "component_symbol": "Delta_beta_total_abs",
            "generator_links": "source_weights;operator_tower;readout_projector",
            "observable_channels": "beta_minus_1;perihelion;LLR",
            "current_source": "2489;2631;2633",
            "comparator_status": "Will_beta_comparator_only_not_claim",
            "required_value_or_theorem": "second-order source-normalized field equation or finite beta component vector",
            "guard": "source/operator/readout beta pieces cannot cancel by assumption",
            "valid_for_claim": "False",
        },
        {
            "ppn_id": "PPNI2636_3_dR",
            "component_symbol": "d_R_preferred_frame",
            "generator_links": "continuous_marker_scalar;domain_boundary_topology",
            "observable_channels": "alpha1;alpha2;alpha3;xi;gamma",
            "current_source": "2489;2631",
            "comparator_status": "preferred-frame comparator only not claim",
            "required_value_or_theorem": "no-disformal slot or preferred-frame response matrix",
            "guard": "alpha_i components independently bounded",
            "valid_for_claim": "False",
        },
        {
            "ppn_id": "PPNI2636_4_wR",
            "component_symbol": "w_R;Delta_w;beta_w_source",
            "generator_links": "species_constants_source_weights",
            "observable_channels": "beta_minus_1;WEP;Newton_GM;R10_source_leg;alpha3",
            "current_source": "2631;2633;2635",
            "comparator_status": "source-coupling frontier not scored",
            "required_value_or_theorem": "no-source-prefactor/no-double-counting theorem or finite component basis",
            "guard": "fitted GM/source normalization shortcut forbidden",
            "valid_for_claim": "False",
        },
        {
            "ppn_id": "PPNI2636_5_endpoint_readout",
            "component_symbol": "epsilon_endpoint_R;alpha_readout;delta_GM",
            "generator_links": "domain_boundary_topology;readout_projector",
            "observable_channels": "xi;alpha3;orbital_light_time;gamma/beta tails;clocks",
            "current_source": "2489;2631;2625",
            "comparator_status": "endpoint/readout kernel missing",
            "required_value_or_theorem": "endpoint silence and fixed-before-readout GM/gauge transfer or finite tail rows",
            "guard": "no post-variation measured-GM laundering",
            "valid_for_claim": "False",
        },
        {
            "ppn_id": "PPNI2636_6_total_abs",
            "component_symbol": "Delta_PPN_abs",
            "generator_links": "all_generators",
            "observable_channels": "all_PPN_local_GR",
            "current_source": "2489;2631;2633;2635",
            "comparator_status": "schema ready, values missing",
            "required_value_or_theorem": "all components theorem-zero or numerically sourced",
            "guard": "absolute envelope; no cancellation-only pass",
            "valid_for_claim": "False",
        },
    ]


def test_readiness_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "TRG2636_0_PPN",
            "arena": "PPN/local_GR",
            "required_inputs": "Delta_PPN_abs components with theorem-zero or numeric source rows",
            "current_status": "BLOCKED_VALUES_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "test_id": "TRG2636_1_R10",
            "arena": "short-range/R10",
            "required_inputs": "operator/readout/source coefficients plus real alpha(lambda) bound rows",
            "current_status": "BLOCKED_SOURCE_COEFFICIENTS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "test_id": "TRG2636_2_WEP",
            "arena": "WEP/source universality",
            "required_inputs": "species/source weights, matter functional owner, readout/source normalization",
            "current_status": "BLOCKED_SOURCE_WEIGHT_ROWS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "test_id": "TRG2636_3_clocks",
            "arena": "clock/time readout",
            "required_inputs": "DObs_e_R, b_R, marker scalar and endpoint/readout clock projection",
            "current_status": "BLOCKED_READOUT_CLOCK_KERNEL_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "test_id": "TRG2636_4_orbital_Newton",
            "arena": "Newton/orbital",
            "required_inputs": "e_kappaG, delta_GM, endpoint tail, source mass transfer, boundary charge",
            "current_status": "BLOCKED_FITTED_GM_GUARD_ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "test_id": "TRG2636_5_local_GR_reduction",
            "arena": "derived GR/Newton limit",
            "required_inputs": "parent normal form, EH coefficient owner, generator zeros or finite residual bounds",
            "current_status": "BLOCKED_PARENT_SIGNATURE_AND_RESIDUALS_MISSING",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def route_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "RG2636_0_no_universal_retry",
            "forbidden_move": "repeat global universal-property/no-extension proof without new source evidence",
            "reason": "2635 froze that route as axiom-only after current-corpus source hunt",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2636_1_no_axiom_as_derivation",
            "forbidden_move": "use primitive-minimal/free/initial language to zero residuals",
            "reason": "axiom-only closure cannot erase live marker/tower/readout countermodels",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2636_2_no_gamma_only",
            "forbidden_move": "claim local GR from Cassini/gamma channel only",
            "reason": "beta, disformal, source, endpoint and readout tails remain live",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2636_3_no_fitted_GM",
            "forbidden_move": "absorb coupling/source residuals into fitted G or GM",
            "reason": "Newtonian coupling must be parent-owned before testing",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2636_4_no_cancellation_only",
            "forbidden_move": "pass by cancellation among unmeasured residual components",
            "reason": "full local vector is an absolute componentwise envelope",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "guard_id": "RG2636_5_private_nonclaim",
            "forbidden_move": "public/GitHub/local-GR claim from 2636",
            "reason": "2636 is routing and source-pack discipline only",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CG2636_0_internal_route",
            "claim": "2636 may guide private next-step selection",
            "status": "ALLOW_INTERNAL_NONCLAIM",
            "passed": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2636_1_generator_zeros",
            "claim": "all surviving generator routes are theorem-zero",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2636_2_effective_pack_scored",
            "claim": "effective residual source pack is ready to score",
            "status": "BLOCKED_SOURCE_ROWS_MISSING",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2636_3_empirical_arenas",
            "claim": "PPN/WEP/R10/clocks/orbital claims are allowed",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2636_4_local_GR",
            "claim": "MTS derives local GR/Newton limit",
            "status": "BLOCKED",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "gate_id": "CG2636_5_public_use",
            "claim": "2636 is public/GitHub-ready proof material",
            "status": "FORBIDDEN",
            "passed": "False",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2636_0_result",
            "decision": "GENERATOR_PRIORITY_GATE_WRITTEN_NOT_PASSED",
            "reason": "2635 made the remaining local-GR problem finite but no generator zero is source-signed yet",
            "consequence": "attack generators in priority order or carry explicit residual rows",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2636_1_first_target",
            "decision": "READOUT_PROJECTOR_E_READOUT_SELECTED_FIRST",
            "reason": "it is priority 1, touches PPN/WEP/R10/clocks/orbital, and prevents reduced-action/readout laundering",
            "consequence": "2637 should try one narrow closed-domain certificate, else source E_readout_total/projector_norm rows",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC2636_2_effective_branch",
            "decision": "EFFECTIVE_GR_RESIDUAL_VECTOR_STAGED_NONCLAIM",
            "reason": "testing can become honest once every residual has units, source path, projection kernel, baseline and no-cancellation guard",
            "consequence": "no empirical scoring until residual rows are real or theorem-zero",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2637-Y5-R2FR-readout-projector-Ereadout-source-pack-or-closed-domain-certificate.md",
            "script": "scripts/Y5_R2FR_readout_projector_Ereadout_source_pack_or_closed_domain_certificate_2637.py",
            "objective": "try one narrow closed-domain certificate for the readout/projector only; if it does not close, source E_readout_total, projector_norm, section_backreaction and marker_readout residual rows with units/placeholders and valid_for_claim=false",
            "include": "2625 field-domain rows; 2625 RRT readout template; 2635 readout priority; 2633 residual vector; 2489/2631 readout and full-PPN tails",
            "exclude": "global universal-property retry, reduced-action variation as parent action, gamma-only pass, fitted GM, public/local-GR claim",
            "selected": "True",
            "valid_for_claim": "False",
        }
    ]


def branch_copy_pairs() -> list[tuple[str, Path, Path]]:
    return [
        ("COPY2636_priority", OUTPUTS["generator_priority"], LOCAL_BOUNDS / "Generator_priority_matrix_2636_NONCLAIM.csv"),
        ("COPY2636_theorem_zero", OUTPUTS["theorem_zero"], LOCAL_BOUNDS / "Theorem_zero_route_gate_2636_NONCLAIM.csv"),
        ("COPY2636_effective_pack", OUTPUTS["effective_pack"], LOCAL_BOUNDS / "Effective_residual_source_pack_2636_NONCLAIM.csv"),
        ("COPY2636_ppn_interface", OUTPUTS["ppn_interface"], LOCAL_BOUNDS / "PPN_interface_map_2636_NONCLAIM.csv"),
        ("COPY2636_test_readiness", OUTPUTS["test_readiness"], LOCAL_BOUNDS / "Test_readiness_gates_2636_NONCLAIM.csv"),
        ("COPY2636_next", OUTPUTS["next_target"], RAB_QUEUE / "JR2636_READOUT_PROJECTOR_E_READOUT_NEXT.csv"),
    ]


def copy_branch_artifacts() -> None:
    for _, source, target in branch_copy_pairs():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "copy_id": copy_id,
            "source_path": str(source),
            "copy_path": str(target),
            "source_exists": bool_text(source.exists()),
            "copy_exists": bool_text(target.exists()),
            "valid_for_claim": "False",
        }
        for copy_id, source, target in branch_copy_pairs()
    ]


def formalization_has_2636_outputs() -> bool:
    if not FORMALIZATION.exists():
        return False
    for path in FORMALIZATION.rglob("*2636*"):
        if path.is_file():
            return True
    for path in FORMALIZATION.rglob("*GENERATOR_EFFECTIVE_PACK_2636*"):
        if path.is_file():
            return True
    return False


def validation_rows(generated: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    output_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    copy_paths = [target for _, _, target in branch_copy_pairs()]
    checks = [
        (
            "VAL2636_00_sources",
            all(row["exists"] == "True" and row["needles_present"] == "True" for row in generated["source_register"]),
            "all cited source paths exist and required needles are present",
        ),
        (
            "VAL2636_01_priority_matrix",
            len(generated["generator_priority"]) == 5 and generated["generator_priority"][0]["generator_id"] == "GEN2635_0_readout_projector" and generated["generator_priority"][0]["selected_next"] == "True",
            "five surviving generators are ranked and readout/projector is selected first",
        ),
        (
            "VAL2636_02_theorem_zero_nonclaim",
            all(row["theorem_zero_claimed"] == "False" for row in generated["theorem_zero"]),
            "no theorem-zero route is falsely promoted",
        ),
        (
            "VAL2636_03_effective_pack",
            any(row["symbol"] == "E_readout_total" for row in generated["effective_pack"]) and any(row["symbol"] == "Delta_PPN_abs" for row in generated["effective_pack"]),
            "effective source pack includes readout residual and full PPN envelope",
        ),
        (
            "VAL2636_04_pack_nonclaim",
            all(row["valid_for_claim"] == "False" and row["status"].startswith(("BLOCKED", "SELECTED", "DOBS", "SCHEMA")) for row in generated["effective_pack"]),
            "all effective rows remain nonclaim and blocked/source-required",
        ),
        (
            "VAL2636_05_ppn_interface",
            any(row["component_symbol"] == "Delta_PPN_abs" for row in generated["ppn_interface"]) and all(row["valid_for_claim"] == "False" for row in generated["ppn_interface"]),
            "PPN interface keeps full-vector no-cancellation discipline",
        ),
        (
            "VAL2636_06_tests_blocked",
            all(row["claim_allowed"] == "False" and row["current_status"].startswith("BLOCKED") for row in generated["test_readiness"]),
            "all local arenas remain blocked until source rows/theorems exist",
        ),
        (
            "VAL2636_07_route_guards",
            any(row["guard_id"] == "RG2636_2_no_gamma_only" for row in generated["route_guards"]) and any(row["guard_id"] == "RG2636_3_no_fitted_GM" for row in generated["route_guards"]),
            "gamma-only and fitted-GM shortcuts are explicitly guarded",
        ),
        (
            "VAL2636_08_claim_gates",
            all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in generated["claim_gates"]),
            "no claim gate allows local GR or empirical pass",
        ),
        (
            "VAL2636_09_next_target",
            any(row["selected"] == "True" and row["next_target"].startswith("2637-Y5-R2FR-readout-projector") for row in generated["next_target"]),
            "2637 readout/projector E_readout target selected",
        ),
        (
            "VAL2636_10_branch_copies",
            all(path.exists() and csv_parses(path) for path in copy_paths),
            "nonclaim local_bounds copies and acquisition queue exist and parse",
        ),
        (
            "VAL2636_11_csv_parse",
            all(path.exists() and csv_parses(path) for path in output_csvs),
            "all generated 2636 CSVs parse",
        ),
        (
            "VAL2636_12_formalization_untouched",
            not formalization_has_2636_outputs(),
            "no 2636 outputs are written under formalization-workbench",
        ),
        (
            "VAL2636_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
    ]
    overall = all(status for _, status, _ in checks)
    rows = [
        {"check_id": check_id, "status": "PASS" if status else "FAIL", "detail": detail, "valid_for_claim": "False"}
        for check_id, status, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL2636_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "2636 generator elimination priority gate and effective GR residual source-pack routing",
            "valid_for_claim": "False",
        }
    )
    return rows


def write_markdown(generated: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]]) -> None:
    lines = [
        "# 2636 - Y5 R2/f(R) Generator Elimination Priority Or Effective GR Residual Vector Source Pack",
        "",
        "Status: `Y5_R2FR_2636_generator_priority_gate_written_readout_selected_effective_residual_pack_staged_nonclaim`",
        "",
        "Claim ceiling: no universal-property retry, no generator theorem-zero claim, no local-GR/Newton proof, no PPN/WEP/R10/clock/orbital pass, no fitted-GM shortcut, no public/GitHub action, and no `formalization-workbench` edit is made.",
        "",
        "## Summary",
        "",
        "2636 turns the frozen 2635 universal-property gap into a finite work queue. The important move is not to circle the same minimality language again: each surviving generator now has to be either theorem-zeroed from a source-backed route or carried as an explicit effective residual row with units, source path, projection kernel, baseline and no-cancellation guard.",
        "",
        "The first selected target is the readout/projector seam. It is not automatically the deepest physics, but it is the cleanest anti-cheat gate: if readout or reduced-action projection sneaks into the varied parent action, it can fake or erase local residuals across PPN, WEP, R10, clocks and orbital systems.",
        "",
        "## Source Register",
        md_table(generated["source_register"]),
        "",
        "## Generator Priority Matrix",
        md_table(generated["generator_priority"]),
        "",
        "## Theorem-Zero Route Gate",
        md_table(generated["theorem_zero"]),
        "",
        "## Effective Residual Source Pack",
        md_table(generated["effective_pack"]),
        "",
        "## PPN Interface Map",
        md_table(generated["ppn_interface"]),
        "",
        "## Test Readiness Gates",
        md_table(generated["test_readiness"]),
        "",
        "## Route Guards",
        md_table(generated["route_guards"]),
        "",
        "## Claim Gates",
        md_table(generated["claim_gates"]),
        "",
        "## Decision Ledger",
        md_table(generated["decision"]),
        "",
        "## Next Target",
        md_table(generated["next_target"]),
        "",
        "## Branch Copies",
        md_table(generated["branch_copies"]),
        "",
        "## Validation",
        md_table(validation),
        "",
        "## Plain-English Verdict",
        "",
        "This is progress, but not a victory lap. We have stopped looping the missing universal-property theorem and converted the remaining GR-reduction problem into named doors: readout/projector, marker scalar, source weights, integrated-out towers, and boundary/domain topology.",
        "",
        "Best next shot: 2637 should hit `E_readout_total` directly. Either prove readout is strictly post-variation and absent from the parent action, or keep the readout/projector residual as a sourced nonclaim row. That is the least slippery route into honest testing.",
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    generated = {
        "source_register": source_register_rows(),
        "generator_priority": generator_priority_rows(),
        "theorem_zero": theorem_zero_rows(),
        "effective_pack": effective_pack_rows(),
        "ppn_interface": ppn_interface_rows(),
        "test_readiness": test_readiness_rows(),
        "route_guards": route_guard_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for key, rows in generated.items():
        if key in OUTPUTS:
            write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    generated["branch_copies"] = branch_copy_rows()
    write_csv(OUTPUTS["branch_copies"], generated["branch_copies"])
    validation = validation_rows(generated)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(generated, validation)
    print(f"wrote {DOC_PATH}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
