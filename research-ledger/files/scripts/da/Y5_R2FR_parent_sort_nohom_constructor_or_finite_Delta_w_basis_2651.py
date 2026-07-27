from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "2651"
FORMALIZATION = PROJECT / "formalization-workbench"
DOC_PATH = ROOT / "2651-Y5-R2FR-parent-sort-nohom-constructor-or-finite-Delta-w-basis.md"

CHECKPOINT = "2651"
BRANCH_ID = "Y5_R2FR_PARENT_SORT_NOHOM_OR_FINITE_DELTAW_BASIS_2651"
PREFIX = "P8_Y5_NOHOM_DELTABASIS_2651"

OUTPUTS = {
    "source_register": RESIDUALS / f"{PREFIX}_SOURCE_REGISTER.csv",
    "nohom_attempt": RESIDUALS / f"{PREFIX}_PARENT_SORT_NOHOM_CONSTRUCTOR_ATTEMPT.csv",
    "nohom_gate": RESIDUALS / f"{PREFIX}_NOHOM_GATE.csv",
    "deltaw_basis": RESIDUALS / f"{PREFIX}_FINITE_DELTAW_COMPONENT_BASIS_NONCLAIM.csv",
    "projection_contracts": RESIDUALS / f"{PREFIX}_ARENA_PROJECTION_CONTRACTS_NONCLAIM.csv",
    "dryrun_cases": RESIDUALS / f"{PREFIX}_NOHOM_DELTABASIS_DRYRUN_CASES.csv",
    "dryrun_results": RESIDUALS / f"{PREFIX}_NOHOM_DELTABASIS_DRYRUN_RESULTS.csv",
    "claim_gates": RESIDUALS / f"{PREFIX}_CLAIM_GATES.csv",
    "decision": RESIDUALS / f"{PREFIX}_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / f"{PREFIX}_NEXT_TARGET.csv",
    "project_status": RESIDUALS / f"{PREFIX}_PROJECT_STATUS_SNAPSHOT.csv",
    "branch_copies": RESIDUALS / f"{PREFIX}_BRANCH_COPIES.csv",
    "validation": RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2651_NOHOM_OR_FINITE_DELTAW_BASIS_NONCLAIM.csv",
    "local_bounds": LOCAL_BOUNDS / "finite_Delta_w_basis_2651_NONCLAIM.csv",
    "source_weight": SOURCE_WEIGHT / "FINITE_DELTAW_COMPONENT_BASIS_2651_NONCLAIM.csv",
    "microscope": MICROSCOPE / "P8_Y5_2651_NOHOM_DELTABASIS_NONCLAIM.csv",
    "quarantine": QUARANTINE / "P8_Y5_2651_NOHOM_DELTABASIS_DRYRUN_RESULTS.csv",
}

SOURCE_SPECS: dict[str, dict[str, Any]] = {
    "2650_doc": {
        "path": ROOT / "2650-Y5-R2FR-no-source-prefactor-object-language-proof-or-parent-material-tensor-basis.md",
        "needles": ["NSP2650_6_verdict", "DEC2650_2_no_more_free_circling", "VAL2650_OVERALL"],
        "role": "immediate hard-fork handoff",
    },
    "2645_doc": {
        "path": ROOT / "2645-Y5-R2FR-no-source-prefactor-parent-action-clause-or-first-JH-DqZ-component-row.md",
        "needles": ["NSP2645_5_pre_action_countermodel", "XIC2645_1_Delta_w_species"],
        "role": "live source-prefactor countermodel and Delta_w component",
    },
    "2646_doc": {
        "path": ROOT / "2646-Y5-R2FR-matter-normalization-owner-or-Delta-w-species-coefficient-source-row.md",
        "needles": ["MNO2646_2_natural_nohom_route", "DWS2646_0_delta_w_species"],
        "role": "natural no-Hom support and symbolic coefficient owner",
    },
    "2647_doc": {
        "path": ROOT / "2647-Y5-R2FR-ordinary-matter-action-signature-or-Delta-w-projection-kernels.md",
        "needles": ["OMC2647_7_verdict", "DK2647_1_WEP"],
        "role": "ordinary matter signature and projection-kernel debt",
    },
    "2648_doc": {
        "path": ROOT / "2648-Y5-R2FR-source-functor-label-forgetting-or-Delta-w-WEP-kernel-v0.md",
        "needles": ["SFL2648_5_verdict", "WEPK2648_5_acceptance", "VAL2648_OVERALL"],
        "role": "source-label forgetting and WEP kernel v0 blocker",
    },
    "1066_doc": {
        "path": ROOT / "1066-Y5-R10-parent-action-syntax-source-scalar-exclusion-or-WEP-Delta-w-prior-width.md",
        "needles": ["SSE1066_5_verdict", "ODR1066_4_verdict", "TWP1066_7_verdict"],
        "role": "source-scalar exclusion and tau projection debt",
    },
    "1225_doc": {
        "path": ROOT / "1225-Y5-R10-tau-WEP-source-worldtube-readout-projection.md",
        "needles": ["ACQ1225_0_official_readout_arrays", "ACQ1225_5_delta_w", "VAL1225_4_acquisition_table_complete"],
        "role": "tau/readout/source product blocker",
    },
    "1896_doc": {
        "path": ROOT / "1896-Y5-R2FR-parent-sort-disjointness-nohom-proof-or-finite-deltaw-basis.md",
        "needles": ["NH1896_5_verdict", "DWB1896_0_vector_space", "VAL1896_OVERALL"],
        "role": "older no-Hom/finite-basis analogue",
    },
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    for path in list(OUTPUTS.values()) + list(BRANCH_COPIES.values()) + [DOC_PATH]:
        path.parent.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as csvfile:
        return list(csv.DictReader(csvfile))


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    header = "| " + " | ".join(fieldnames) + " |"
    separator = "| " + " | ".join("---" for _ in fieldnames) + " |"
    body: list[str] = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fieldnames]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    generated = timestamp()
    for source_id, spec in SOURCE_SPECS.items():
        path = Path(spec["path"])
        text = read_text(path)
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            {
                "source_id": f"SRC2651_{source_id}",
                "role": spec["role"],
                "path": str(path),
                "exists": path.exists(),
                "needles_required": len(spec["needles"]),
                "missing_needles": "; ".join(missing),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_SOURCE_OR_NEEDLE",
                "valid_for_claim": False,
                "timestamp_utc": generated,
            }
        )
    return rows


def nohom_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NH2651_0_target",
            "claim_piece": "parent sort no-Hom theorem",
            "formal_statement": "Hom_parent(SpeciesLabel, Coeff_active_source)=empty and Hom_parent(Marker_hidden, Coeff_active_source)=empty before variation/readout.",
            "status": "TARGET_SHARP",
            "proof_or_obstruction": "this is the exact theorem needed to make source-only w_A unformable rather than merely small",
            "source_anchor": "2650:TYP2650_1_no_species_to_source_coeff;1896:NH1896_0_target",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NH2651_1_parent_sort_constructor",
            "claim_piece": "active-source coefficient constructor",
            "formal_statement": "Coeff_active_source is generated only from UniversalCalibration, retained explicitly declared residuals, and observed total Hilbert source data; SpeciesLabel and hidden/readout markers are not domain arguments.",
            "status": "EXACT_CONDITIONAL_CONSTRUCTOR",
            "proof_or_obstruction": "if this constructor is parent-derived, no map can read a species label into a source coefficient",
            "source_anchor": "2650:TYP2650_0_parent_sorts;2646:MNO2646_2_natural_nohom_route",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NH2651_2_product_sequester_route",
            "claim_piece": "visible/source functor factorization",
            "formal_statement": "If C_parent factors as visible/source data times bookkeeping labels and source coefficient functors factor only through the visible/source projection, label tangents annihilate active-source coefficients.",
            "status": "EXACT_CONDITIONAL_NOT_PARENT_DERIVED",
            "proof_or_obstruction": "the chain-rule proof works, but current corpus has not derived product-category source factorization from MTS primitives",
            "source_anchor": "1896:NH1896_2_product_category_route;2648:SFL2648_5_verdict",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NH2651_3_counterexamples_retained",
            "claim_piece": "why no-Hom is not current proof",
            "formal_statement": "Disconnected species sectors, source-scalar targets, action-scale coefficients, material markers, boundary/readout masks and hidden invariant scalars can still define source coefficient maps unless explicitly typed out.",
            "status": "COUNTEREXAMPLES_RETAINED",
            "proof_or_obstruction": "naturality, Ward conservation, and candidate typing are not enough while these object-language routes remain legal",
            "source_anchor": "1066:SSE1066_5_verdict;2650:NSP2650_3_disconnected_species_countermodel",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NH2651_4_action_scale_readout_stability",
            "claim_piece": "tree theorem survives measure/readout/radiative projection",
            "formal_statement": "One parent action-density/measure owner plus readout/source-worldtube stability prevents a source coefficient from returning through S_eff, loops, spectroscopy, clocks, WEP readout or local projectors.",
            "status": "ACTION_SCALE_READOUT_STABILITY_UNSIGNED",
            "proof_or_obstruction": "even a tree-level no-Hom constructor is not claim-grade without this stability package",
            "source_anchor": "2650:NSP2650_4_action_scale_measure_gap;1225:ACQ1225_0_official_readout_arrays",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "attempt_id": "NH2651_5_verdict",
            "claim_piece": "promote no-Hom constructor as current theorem",
            "formal_statement": "Current MTS parent primitives derive Hom(SpeciesLabel,Coeff_active_source)=empty without adding a closure axiom.",
            "status": "PARENT_SORT_NOHOM_CONSTRUCTOR_NOT_DERIVED",
            "proof_or_obstruction": "the theorem is exact conditionally, but parent sort construction, product sequester, no-marker exhaustion, and action-scale/readout stability are not signed together",
            "source_anchor": "NH2651_0_target through NH2651_4_action_scale_readout_stability",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def nohom_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "NHG2651_0_parent_sort_constructor",
            "required_clause": "parent sort constructor is derived from MTS primitives",
            "current_status": "MISSING_PARENT_SORT_CONSTRUCTOR",
            "if_pass": "no-Hom is theorem-level rather than syntax decree",
            "if_fail": "object-language route remains private closure",
            "source_anchor": "2650:TYP2650_0_parent_sorts",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NHG2651_1_no_species_hom",
            "required_clause": "SpeciesLabel has no morphism to active source coefficient slots",
            "current_status": "EXACT_CONDITIONAL_NOT_PARENT_SIGNED",
            "if_pass": "pre-action Delta_w_species is ill-typed",
            "if_fail": "relative species prefactor remains live",
            "source_anchor": "2650:TYP2650_1_no_species_to_source_coeff",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NHG2651_2_no_marker_hom",
            "required_clause": "hidden/domain/boundary/readout markers cannot be retyped as source coefficients",
            "current_status": "NO_MARKER_THEOREM_NOT_PROVED",
            "if_pass": "Delta_w_marker_hidden is theorem-zero",
            "if_fail": "hidden marker source weights stay in finite basis",
            "source_anchor": "2650:TYP2650_4_no_marker_readout_return",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NHG2651_3_action_scale_readout",
            "required_clause": "action-scale/measure/readout stability preserves no-Hom",
            "current_status": "ACTION_SCALE_READOUT_STABILITY_UNSIGNED",
            "if_pass": "tree-level no-Hom can survive into WEP/clock/PPN/local projections",
            "if_fail": "finite residual route is mandatory",
            "source_anchor": "2650:NSP2650_4_action_scale_measure_gap;1225:ACQ1225_0_official_readout_arrays",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "NHG2651_4_verdict",
            "required_clause": "no-Hom source-weight zero theorem",
            "current_status": "NOHOM_CLAIM_BLOCKED",
            "if_pass": "Delta_w source components become theorem-zero subject to projection/readout gates",
            "if_fail": "finite Delta_w basis is the honest branch",
            "source_anchor": "NHG2651_0_parent_sort_constructor through NHG2651_3_action_scale_readout",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]


def deltaw_basis_rows() -> list[dict[str, Any]]:
    return [
        {
            "basis_id": "DWB2651_0_vector_space",
            "component": "Delta_w_vector_space",
            "definition": "finite source-weight residual vector after universal common calibration mode is removed",
            "basis_formula": "Delta_w = P_perp w, P_perp u_common=0; norm is L1/no-cancellation envelope or explicitly declared arena covariance norm",
            "current_status": "BASIS_SCHEMA_NONCLAIM_PARENT_COMPONENT_VALUES_MISSING",
            "missing_for_claim": "parent coefficient vector, composition weights p_A, norm choice, no-cancellation policy, source path",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_1_preaction_species",
            "component": "Delta_w_species",
            "definition": "relative pre-variation species/action/source prefactor after common-mode subtraction",
            "basis_formula": "w_A=w_common(1+epsilon_A), sum_A p_A epsilon_A=0 for declared composition/source weights",
            "current_status": "LIVE_COUNTERMODEL_COMPONENT_SYMBOLIC_ONLY",
            "missing_for_claim": "parent epsilon_A vector or no-Hom theorem-zero",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_2_current_rescale",
            "component": "c_A_current_rescale",
            "definition": "post-variation species/source current rescale J_A -> c_A J_A",
            "basis_formula": "Delta J_src=sum_A(c_A-c_common)J_A",
            "current_status": "CURRENT_OWNER_MISSING_NONCLAIM",
            "missing_for_claim": "source-current owner/no-rescale theorem or coefficient row",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_3_marker_spurion",
            "component": "Delta_w_marker_hidden",
            "definition": "hidden invariant, material marker, boundary/domain class, or readout mask that reweights source strength",
            "basis_formula": "w_A=w_common[1+epsilon_marker I_marker(A,D,boundary,readout)]",
            "current_status": "NO_MARKER_THEOREM_UNSIGNED_NONCLAIM",
            "missing_for_claim": "no-marker/no-hidden-visible theorem or finite marker coefficient bounds",
            "units": "dimensionless",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_4_action_measure_jacobian",
            "component": "Delta_w_measure",
            "definition": "relative hbar/action-density/measure/Jacobian multiplier that can mimic source weighting while leaving some classical equations unchanged",
            "basis_formula": "S_matter=sum_A Z_A^measure S_A; Delta_w_measure=P_perp log Z_A^measure",
            "current_status": "ACTION_SCALE_MEASURE_OWNER_UNSIGNED_NONCLAIM",
            "missing_for_claim": "single parent action-density/measure owner or numeric Z_A^measure bounds",
            "units": "dimensionless logarithmic response",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_5_nonhilbert_current",
            "component": "J_NH_retained",
            "definition": "non-Hilbert, boundary, exchange, memory, range, connection, spin/torsion, or improvement current bypassing total Hilbert source",
            "basis_formula": "J_src=kappa_univ T_Hilbert + sum_i C_i J_NH,i",
            "current_status": "OPEN_PARALLEL_GATE_NONCLAIM",
            "missing_for_claim": "formula-level K_owner and q_retained zero proof or finite coefficient row",
            "units": "declared by current channel",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_6_mass_projector",
            "component": "Delta_mu_projector",
            "definition": "measured-GM/orbital mass projector, exchange, boundary, anomaly, or Gauss calibration residual",
            "basis_formula": "Delta mu_obs=Pi_M(J_Hilbert+J_exchange+J_boundary)-Pi_M(J_Hilbert)",
            "current_status": "PROJECTED_FLUX_OPEN_NONCLAIM",
            "missing_for_claim": "closed calibrated mass projector or finite Delta_mu row",
            "units": "dimensionless or declared GM units",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_7_material_basis_link",
            "component": "R_material_X",
            "definition": "material response tensor mapping finite source-weight components into WEP/test-body contrasts",
            "basis_formula": "eta_AB ~ tau_WEP sum_X K_X C_X R_material_X(A,B), with all legs sourced before scoring",
            "current_status": "PARENT_MATERIAL_TENSOR_BASIS_BLOCKED_NONCLAIM",
            "missing_for_claim": "parent X basis, material tensor, coefficient vector, tau/readout/product convention",
            "units": "declared parent-basis response units",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_8_no_cancellation_policy",
            "component": "basis_policy",
            "definition": "multi-component scores use a no-cancellation envelope unless a parent identity proves signed cancellation",
            "basis_formula": "observable_bound uses sum_i |K_i Delta_w_i| or a declared covariance envelope; no fitted cancellation pass",
            "current_status": "POLICY_WRITTEN_NONCLAIM",
            "missing_for_claim": "arena K/tau/material projections and parent coefficient values",
            "units": "policy",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "basis_id": "DWB2651_9_acceptance",
            "component": "finite_Delta_w_basis_acceptance",
            "definition": "finite basis is score-ready only when each component has theorem-zero or parent coefficient value plus arena projection kernels",
            "basis_formula": "claim row requires zero-proof or numeric C_i, source path, units, norm, K/tau/material/readout projection and no-cancellation policy",
            "current_status": "FINITE_DELTAW_BASIS_STAGED_NONCLAIM",
            "missing_for_claim": "all component values/theorem-zeros plus projections",
            "units": "mixed declared by component",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def projection_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "projection_id": "PRJ2651_0_WEP",
            "arena": "WEP_MICROSCOPE_TiPt",
            "observable": "eta_TA6V_PtRh10",
            "contract": "eta_AB = tau_WEP * sum_i K_WEP_i(source,orbit,readout) * R_material_i(A,B) * Delta_w_i",
            "missing_inputs": "parent Delta_w_i values or zero-proofs; full material tensor; official readout arrays; tau/source-worldtube product",
            "source_anchor": "1225:ACQ1225_0_official_readout_arrays;2650:PMTB2650_6_acceptance",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ2651_1_R10",
            "arena": "R10_short_range",
            "observable": "alpha(lambda) fifth-force/source residual",
            "contract": "alpha_pred(lambda)=sum_i K_R10_i(lambda) * Delta_w_i with sourced bound curve and units",
            "missing_inputs": "numeric parent coefficients; real bound curve rows; material/source charge convention; lambda dependence",
            "source_anchor": "2647:DK2647_2_R10;1066:TWP1066_7_verdict",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ2651_2_PPN",
            "arena": "local_PPN",
            "observable": "gamma,beta,preferred-frame/source residual vector",
            "contract": "Delta_PPN=sum_i K_PPN_i(local geometry/source calibration) * Delta_w_i",
            "missing_inputs": "local projection operator; source coefficient values; metric limit map; PPN observable convention",
            "source_anchor": "2647:DK2647_3_PPN;2650:NHG2651_PENDING",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ2651_3_clock",
            "arena": "clock_redshift",
            "observable": "clock transition/local time residual",
            "contract": "Delta_clock=sum_i K_clock_i(atom,transition,source,readout) * Delta_w_i",
            "missing_inputs": "clock material response basis; readout/stability theorem; parent coefficients",
            "source_anchor": "2647:DK2647_4_clock;1225:ACQ1225_0_official_readout_arrays",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "projection_id": "PRJ2651_4_orbital",
            "arena": "orbital_GM",
            "observable": "GM/orbital source normalization residual",
            "contract": "Delta_mu_obs=sum_i K_orbital_i(source body,orbit,projector) * Delta_w_i",
            "missing_inputs": "mass projector; exchange/boundary flux audit; source composition convention; orbital covariance",
            "source_anchor": "2651:DWB2651_6_mass_projector;2649:QSRC2649_5_projected_mass_gap",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {"case_id": "DRY2651_0_nohom_unsigned", "nohom_parent_signed": False, "uses_syntax_decree": False, "basis_has_parent_values": False, "projection_ready": False, "uses_cancellation": False, "score_attempt": False, "expected_status": "REFUSED_NOHOM_NOT_PARENT_DERIVED", "valid_for_claim": False},
        {"case_id": "DRY2651_1_syntax_decree", "nohom_parent_signed": False, "uses_syntax_decree": True, "basis_has_parent_values": False, "projection_ready": False, "uses_cancellation": False, "score_attempt": False, "expected_status": "REFUSED_SYNTAX_BY_DECREE", "valid_for_claim": False},
        {"case_id": "DRY2651_2_basis_no_values", "nohom_parent_signed": True, "uses_syntax_decree": False, "basis_has_parent_values": False, "projection_ready": False, "uses_cancellation": False, "score_attempt": False, "expected_status": "REFUSED_PARENT_DELTAW_VALUES_MISSING", "valid_for_claim": False},
        {"case_id": "DRY2651_3_cancellation", "nohom_parent_signed": True, "uses_syntax_decree": False, "basis_has_parent_values": True, "projection_ready": False, "uses_cancellation": True, "score_attempt": True, "expected_status": "REFUSED_CANCELLATION_ONLY_PASS", "valid_for_claim": False},
        {"case_id": "DRY2651_4_projection_missing", "nohom_parent_signed": True, "uses_syntax_decree": False, "basis_has_parent_values": True, "projection_ready": False, "uses_cancellation": False, "score_attempt": True, "expected_status": "REFUSED_PROJECTION_KERNELS_NOT_READY", "valid_for_claim": False},
        {"case_id": "DRY2651_5_symbolic_score", "nohom_parent_signed": False, "uses_syntax_decree": False, "basis_has_parent_values": False, "projection_ready": True, "uses_cancellation": False, "score_attempt": True, "expected_status": "REFUSED_SYMBOLIC_COMPONENT_SCORING", "valid_for_claim": False},
        {"case_id": "DRY2651_6_counterfactual_ready", "nohom_parent_signed": True, "uses_syntax_decree": False, "basis_has_parent_values": True, "projection_ready": True, "uses_cancellation": False, "score_attempt": True, "expected_status": "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM", "valid_for_claim": False},
    ]


def evaluate_dryrun_case(row: dict[str, Any]) -> str:
    if row["uses_syntax_decree"]:
        return "REFUSED_SYNTAX_BY_DECREE"
    if row["uses_cancellation"] and row["score_attempt"]:
        return "REFUSED_CANCELLATION_ONLY_PASS"
    if not row["nohom_parent_signed"] and row["score_attempt"] and row["projection_ready"]:
        return "REFUSED_SYMBOLIC_COMPONENT_SCORING"
    if not row["nohom_parent_signed"]:
        return "REFUSED_NOHOM_NOT_PARENT_DERIVED"
    if not row["basis_has_parent_values"]:
        return "REFUSED_PARENT_DELTAW_VALUES_MISSING"
    if row["score_attempt"] and not row["projection_ready"]:
        return "REFUSED_PROJECTION_KERNELS_NOT_READY"
    return "COUNTERFACTUAL_READY_NOT_CURRENT_CLAIM"


def dryrun_result_rows(cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    generated = timestamp()
    return [
        {
            "case_id": row["case_id"],
            "computed_status": evaluate_dryrun_case(row),
            "expected_status": row["expected_status"],
            "status_match": evaluate_dryrun_case(row) == row["expected_status"],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": generated,
        }
        for row in cases
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CG2651_0_nohom", "condition": "parent no-Hom theorem is signed", "current_status": "FAIL_PARENT_SORT_NOHOM_CONSTRUCTOR_NOT_DERIVED", "source_anchor": f"{OUTPUTS['nohom_attempt'].name}:NH2651_5_verdict", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2651_1_deltaw_values", "condition": "finite Delta_w basis has parent coefficient values or theorem-zero rows", "current_status": "FAIL_BASIS_SCHEMA_NONCLAIM_PARENT_COMPONENT_VALUES_MISSING", "source_anchor": f"{OUTPUTS['deltaw_basis'].name}:DWB2651_0_vector_space", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2651_2_projection", "condition": "arena projection/tau/material kernels are sourced before scoring", "current_status": "FAIL_PROJECTION_KERNELS_NOT_READY", "source_anchor": f"{OUTPUTS['projection_contracts'].name}:PRJ2651_0_WEP", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2651_3_no_cancellation", "condition": "no cancellation-only pass is used", "current_status": "PASS_POLICY_WRITTEN_NONCLAIM", "source_anchor": f"{OUTPUTS['deltaw_basis'].name}:DWB2651_8_no_cancellation_policy", "gate_pass": False, "valid_for_claim": False},
        {"gate_id": "CG2651_4_verdict", "condition": "source-weight zero or finite Delta_w branch can claim pass", "current_status": "CLAIM_BLOCKED", "source_anchor": "CG2651_0_nohom through CG2651_3_no_cancellation", "gate_pass": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"decision_id": "DEC2651_0_nohom", "decision": "DO_NOT_PROMOTE_NOHOM_THEOREM", "reason": "typed/product proof is exact conditionally but parent sort constructor and stability gates remain unsigned", "status": "NOHOM_ROUTE_SHARP_BUT_UNSIGNED", "next_dependency": "parent sort grammar or action-scale/readout stability", "valid_for_claim": False},
        {"decision_id": "DEC2651_1_basis", "decision": "FINITE_DELTAW_BASIS_STAGED_NONCLAIM", "reason": "components, common-mode projector, arena contracts and no-cancellation policy are explicit but have no parent values", "status": "TEST_BRANCH_STRUCTURED_NOT_NUMERIC", "next_dependency": "source parent coefficient values or build arena projection matrix", "valid_for_claim": False},
        {"decision_id": "DEC2651_2_next", "decision": "SELECT_2652_ACTION_SCALE_READOUT_OR_PROJECTION_MATRIX", "reason": "even a clean tree no-Hom theorem is not claim-grade if w_A can return through measure/readout; if proof fails, the projection matrix is the next empirical object", "status": "NEXT_TARGET_SELECTED", "next_dependency": "2652 action-scale/readout stability or Delta_w projection matrix", "valid_for_claim": False},
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_id": "NEXT2651_0_selected",
            "status": "selected",
            "next_doc": "2652-Y5-R2FR-action-scale-readout-stability-or-Delta-w-projection-matrix.md",
            "next_script": "scripts/Y5_R2FR_action_scale_readout_stability_or_Delta_w_projection_matrix_2652.py",
            "target": "Try to prove one action-scale/measure/readout owner prevents source weights from returning after tree-level no-Hom; if it fails, build the Delta_w arena projection matrix as nonclaim.",
            "must_include": "action-density owner; measure/hbar owner; readout/source-worldtube stability; projection matrix K_i for WEP/R10/PPN/clock/orbital; tau/material/source dependencies",
            "must_exclude": "tree-level grammar claim alone; symbolic Delta_w scoring; cancellation-only passes; bound-as-prediction; local-GR/WEP claim; GitHub action; formalization-workbench edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {"status_id": "STAT2651_0_nohom", "area": "source coupling theorem", "summary": "the no-Hom target is exact but still parent-unsigned", "risk_level": "NARROW_PARENT_GRAMMAR_GAP", "project_meaning": "the coupling problem is reduced to parent sort/grammar plus stability theorem", "next_action": "derive action-scale/readout stability or parent sort grammar", "valid_for_claim": False},
        {"status_id": "STAT2651_1_finite_branch", "area": "finite residual testing", "summary": "Delta_w finite basis is explicit enough for projection matrices but has no parent coefficient values", "risk_level": "TEST_BRANCH_STRUCTURED_NOT_NUMERIC", "project_meaning": "if derivation fails, the empirical branch is no longer amorphous", "next_action": "build projection matrix or source coefficients", "valid_for_claim": False},
        {"status_id": "STAT2651_2_project_overview", "area": "GR/Newton reduction bridge", "summary": "source universality remains the central local bridge debt", "risk_level": "HARD_BUT_LOCALIZED", "project_meaning": "not solved, but the missing coupling object is finally named and bounded by gates", "next_action": "2652 action-scale/readout stability", "valid_for_claim": False},
    ]


def branch_copy_rows(basis_rows: list[dict[str, Any]], dryrun_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    write_csv(BRANCH_COPIES["queue"], basis_rows)
    write_csv(BRANCH_COPIES["local_bounds"], basis_rows)
    write_csv(BRANCH_COPIES["source_weight"], basis_rows)
    write_csv(BRANCH_COPIES["microscope"], basis_rows)
    write_csv(BRANCH_COPIES["quarantine"], dryrun_rows)
    return [
        {
            "copy_id": copy_id,
            "path": str(path),
            "exists": path.exists(),
            "parseable_csv": path.exists() and len(csv_rows(path)) >= 1,
            "purpose": "2651 no-Hom/finite-Delta_w nonclaim handoff",
            "valid_for_claim": False,
        }
        for copy_id, path in BRANCH_COPIES.items()
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    cases = dryrun_case_rows()
    dryrun_results = dryrun_result_rows(cases)
    basis = deltaw_basis_rows()
    rows = {
        "source_register": source_register_rows(),
        "nohom_attempt": nohom_attempt_rows(),
        "nohom_gate": nohom_gate_rows(),
        "deltaw_basis": basis,
        "projection_contracts": projection_contract_rows(),
        "dryrun_cases": cases,
        "dryrun_results": dryrun_results,
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }
    rows["branch_copies"] = branch_copy_rows(basis, dryrun_results)
    return rows


def generated_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"] + list(BRANCH_COPIES.values())


def all_generated_csv_parse(paths: list[Path]) -> bool:
    for path in paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            csv_rows(path)
        except Exception:
            return False
    return True


def formalization_hit_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    patterns = [
        "*2651-Y5-R2FR*",
        f"*{PREFIX}*",
        "*P8_Y5_BRR545_2651*",
        "*Y5_R2FR_parent_sort_nohom_constructor_or_finite_Delta_w_basis_2651*",
        "*JR2651*",
    ]
    hits: list[Path] = []
    for pattern in patterns:
        hits.extend(FORMALIZATION.rglob(pattern))
    return len([path for path in hits if path.is_file()])


def validation_rows(rows: dict[str, list[dict[str, Any]]], paths: list[Path]) -> list[dict[str, Any]]:
    source_ok = all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in rows["source_register"])
    nohom_ok = any(row["attempt_id"] == "NH2651_5_verdict" and row["status"] == "PARENT_SORT_NOHOM_CONSTRUCTOR_NOT_DERIVED" for row in rows["nohom_attempt"])
    gate_ok = any(row["gate_id"] == "NHG2651_4_verdict" and row["current_status"] == "NOHOM_CLAIM_BLOCKED" and not row["gate_pass"] for row in rows["nohom_gate"])
    basis_ok = any(row["basis_id"] == "DWB2651_9_acceptance" and row["current_status"] == "FINITE_DELTAW_BASIS_STAGED_NONCLAIM" for row in rows["deltaw_basis"])
    projection_ok = all(not row["score_ready"] and not row["valid_for_claim"] for row in rows["projection_contracts"])
    dryrun_ok = all(row["status_match"] and not row["claim_allowed"] for row in rows["dryrun_results"])
    claim_ok = all(not row["gate_pass"] and not row["valid_for_claim"] for row in rows["claim_gates"])
    next_ok = any("2652-Y5-R2FR-action-scale-readout-stability" in row["next_doc"] for row in rows["next_target"])
    branch_ok = all(row["exists"] and row["parseable_csv"] for row in rows["branch_copies"])
    csv_ok = all_generated_csv_parse(paths)
    formal_ok = formalization_hit_count() == 0
    pycache_ok = not (ROOT / "scripts" / "__pycache__").exists()
    checks = [
        ("VAL2651_00_sources", source_ok, "all cited source paths exist and required needles are present"),
        ("VAL2651_01_nohom_verdict", nohom_ok, "no-Hom constructor remains exact conditional, not parent theorem"),
        ("VAL2651_02_nohom_gate", gate_ok, "no-Hom claim gate remains blocked"),
        ("VAL2651_03_deltaw_basis", basis_ok, "finite Delta_w basis rows are nonclaim/not score-ready"),
        ("VAL2651_04_projection_contracts", projection_ok, "arena projection contracts are explicit but not score-ready"),
        ("VAL2651_05_dryrun", dryrun_ok, "dry-run refuses unsigned no-Hom, syntax decree, missing values, cancellation, projection gaps, and symbolic scoring"),
        ("VAL2651_06_claim_gates_false", claim_ok, "all claim gates remain blocked"),
        ("VAL2651_07_next_target", next_ok, "2652 next target is recorded"),
        ("VAL2651_08_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL2651_09_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2651_10_formalization_untouched", formal_ok, "no 2651 outputs are written under formalization-workbench"),
        ("VAL2651_11_pycache_absent", pycache_ok, "scripts __pycache__ absent"),
    ]
    generated = timestamp()
    out = [
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for validation_id, passed, detail in checks
    ]
    out.append(
        {
            "timestamp_utc": generated,
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "valid_for_claim": False,
            "claim_allowed": False,
            "validation_id": "VAL2651_OVERALL",
            "status": "PASS" if all(row["status"] == "PASS" for row in out) else "FAIL",
            "detail": "2651 refuses no-Hom promotion, stages finite Delta_w basis/projection contracts, and selects action-scale/readout stability or projection matrix next",
        }
    )
    return out


def write_doc(rows: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 2651 - Parent Sort No-Hom Constructor Or Finite Delta_w Basis

## Purpose

This checkpoint is the hard fork after 2650: either derive `Hom(SpeciesLabel,Coeff_active_source)=empty` from the parent sort constructor, or stop trying to erase `Delta_w` and make the finite residual basis explicit.

## Result

- The no-Hom theorem is exact conditionally, but still not parent-derived from MTS primitives.
- The obstruction is now localized: parent sort constructor, product/source sequester, no-marker exhaustion, and action-scale/readout stability must be signed together.
- The finite `Delta_w` basis is explicit: common-mode projector, pre-action species prefactor, current rescale, marker spurion, action/measure Jacobian, non-Hilbert current, mass projector, material-basis link, and no-cancellation policy.
- No component is score-ready; no WEP/R10/PPN/clock/orbital/local-GR claim is made.

## Source Register

{markdown_table(rows["source_register"])}

## No-Hom Attempt

{markdown_table(rows["nohom_attempt"])}

## No-Hom Gate

{markdown_table(rows["nohom_gate"])}

## Finite Delta_w Component Basis

{markdown_table(rows["deltaw_basis"])}

## Arena Projection Contracts

{markdown_table(rows["projection_contracts"])}

## Dry-Run Cases

{markdown_table(rows["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows["dryrun_results"])}

## Claim Gates

{markdown_table(rows["claim_gates"])}

## Decision Ledger

{markdown_table(rows["decision"])}

## Next Target

{markdown_table(rows["next_target"])}

## Project Status Snapshot

{markdown_table(rows["project_status"])}

## Branch Copies

{markdown_table(rows["branch_copies"])}

## Validation

{markdown_table(validation)}
"""
    DOC_PATH.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows = build_rows()
    for name, table in rows.items():
        if name in OUTPUTS and name != "validation":
            write_csv(OUTPUTS[name], table)
    remove_pycache()
    rows["validation"] = validation_rows(rows, generated_paths())
    write_csv(OUTPUTS["validation"], rows["validation"])
    write_doc(rows)
    remove_pycache()


if __name__ == "__main__":
    main()
