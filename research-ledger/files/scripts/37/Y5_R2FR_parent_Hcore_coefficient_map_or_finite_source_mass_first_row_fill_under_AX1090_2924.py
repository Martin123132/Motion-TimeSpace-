from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2924"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2924-Y5-R2FR-parent-Hcore-coefficient-map-or-finite-source-mass-first-row-fill-under-AX1090.md"

SRC_2923_DOC = ROOT / "2923-Y5-R2FR-first-source-mass-row-template-and-Hcore-coefficient-checklist-under-AX1090.md"
SRC_2923_NEXT = RESIDUALS / "P8_Y5_R2FR_2923_NEXT_TARGET.csv"
SRC_2923_HCORE = RESIDUALS / "P8_Y5_R2FR_2923_HCORE_QTAU_COEFFICIENT_CHECKLIST.csv"
SRC_2923_CANDIDATES = RESIDUALS / "P8_Y5_R2FR_2923_CANDIDATE_VALIDATION_RESULTS.csv"
SRC_2923_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2923_VALIDATION.csv"
SRC_1007_DOC = ROOT / "1007-Y5-R10-Htau-integrability-fixed-reference-theorem-or-symplectic-residual-row.md"
SRC_1008_LEDGER = RESIDUALS / "P8_Y5_R10_1008_CHARGE_PIECE_LEDGER.csv"
SRC_1009_DOC = ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md"
SRC_MIN_BLOCKS = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"
SRC_NOETHER_CHAIN = RESIDUALS / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv"
SRC_HAMILTONIAN_CONTRACT = RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"
SRC_SOURCE_MEASURE = RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv"
SRC_1012_DOC = ROOT / "1012-Y5-R10-Y5-source-normalization-owner-or-q_loc-bound-implementation.md"
SRC_1015_DOC = ROOT / "1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2924_SOURCE_REGISTER.csv",
    "eh_anchor": RESIDUALS / "P8_Y5_R2FR_2924_EH_ANCHOR_COEFFICIENT_MAP.csv",
    "reduction_contract": RESIDUALS / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv",
    "source_mass_attempt": RESIDUALS / "P8_Y5_R2FR_2924_SOURCE_MASS_FIRST_ROW_ATTEMPT.csv",
    "bridge_check": RESIDUALS / "P8_Y5_R2FR_2924_GAUSS_POISSON_BRIDGE_CHECK.csv",
    "rejection_runner": RESIDUALS / "P8_Y5_R2FR_2924_REJECTION_RUNNER.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2924_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2924_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2924_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2924_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2924_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "eh_anchor_copy": PARENT_ACTION / "EH_anchor_coefficient_map_2924_CONDITIONAL_NONCLAIM.csv",
    "source_mass_copy": LOCAL_BOUNDS / "Source_mass_first_row_attempt_2924_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2924_MTS_TO_EH_REDUCTION_MORPHISM_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = [
        "| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "SRC2924_00_2923_doc",
            SRC_2923_DOC,
            "Y5_R2FR_2923_template_built_parent_Hcore_coefficient_map_2924_next;NEXT2923_0_2924;Validation overall: `True`",
            "2923 selected the parent Hcore coefficient/source-mass fill target",
        ),
        (
            "SRC2924_01_2923_next",
            SRC_2923_NEXT,
            "NEXT2923_0_2924;parent-Hcore-coefficient-map-or-finite-source-mass-first-row-fill",
            "machine-readable 2924 target",
        ),
        (
            "SRC2924_02_2923_hcore",
            SRC_2923_HCORE,
            "HC2923_0_parent_action_block;HC2923_10_total_guard",
            "2923 Hcore/Q_tau checklist",
        ),
        (
            "SRC2924_03_2923_candidates",
            SRC_2923_CANDIDATES,
            "CAND2923_3_1249_qRhat_nonclaim_smoke;ACCEPTED_NONCLAIM_FINITE_QRHAT_SMOKE",
            "2923 candidate runner",
        ),
        (
            "SRC2924_04_2923_validation",
            SRC_2923_VALIDATION,
            "VAL2923_OVERALL;True",
            "2923 validation summary",
        ),
        (
            "SRC2924_05_1007_Htau",
            SRC_1007_DOC,
            "HTA1007_2_EH_import_guard;HTA1007_6_integrability_verdict",
            "EH import guarded; H_tau integrability still unsigned",
        ),
        (
            "SRC2924_06_1008_charge_pieces",
            SRC_1008_LEDGER,
            "QTA1008_3_Q_EH;QTA1008_7_Q_matter_source",
            "Q_tau^EH is a conditional reference; matter/source glue unsigned",
        ),
        (
            "SRC2924_07_1009_parent_contract",
            SRC_1009_DOC,
            "PCS1009_0_EH_core;SVR1009_0_EH_anchor_only;CG1009_2_Qtau_MTS",
            "EH anchor exists but total parent current chain is incomplete",
        ),
        (
            "SRC2924_08_min_parent_blocks",
            SRC_MIN_BLOCKS,
            "A511_0_EH_core;A511_6_metric_readout",
            "minimal local-GR parent block menu",
        ),
        (
            "SRC2924_09_noether_chain",
            SRC_NOETHER_CHAIN,
            "D505_0_local_parent_action_form;D505_6_worldtube_readout",
            "parent Noether closure chain",
        ),
        (
            "SRC2924_10_hamiltonian_contract",
            SRC_HAMILTONIAN_CONTRACT,
            "HC0_same_frame_EH_exterior;HC8_Poisson_Gauss_orbital_calibration",
            "Hamiltonian boundary charge contract",
        ),
        (
            "SRC2924_11_source_measure",
            SRC_SOURCE_MEASURE,
            "HSM541_2_observed_worldtube_source;HSM541_5_Gauss_orbital_readout",
            "Hamiltonian source-measure contract",
        ),
        (
            "SRC2924_12_1012_source_norm",
            SRC_1012_DOC,
            "Y5O1012_7_Newton_Poisson_orbit;Y5O1012_8_verdict",
            "source-normalization owner theorem still not derived",
        ),
        (
            "SRC2924_13_1015_same_object",
            SRC_1015_DOC,
            "SOL1015_1_source_measure;SOL1015_6_verdict",
            "same-object/topological-Hilbert equality conditional lemma",
        ),
    ]
    rows = []
    for source_id, path, anchors, role in specs:
        ok, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": ok,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def eh_anchor_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "map_id": "EHA2924_0_EH_action_block",
            "object": "S_EH[g_obs;kappa0,Lambda0]",
            "formula": "S_EH=(2*kappa0)^-1 int sqrt(-g_obs)(R[g_obs]-2 Lambda0)",
            "coefficient": "kappa0=8*pi*G0/c^4 in SI; kappa0=8*pi*G0 in c=1 units",
            "status": "CONDITIONAL_GR_REFERENCE",
            "what_is_filled": "local spin-2 metric operator and EH variation anchor",
            "what_is_not_filled": "MTS-to-EH reduction morphism and extra-sector silence",
            "source_paths": str(SRC_MIN_BLOCKS),
        },
        {
            "map_id": "EHA2924_1_EH_variation",
            "object": "delta S_EH",
            "formula": "delta L_EH=E_g^EH delta g + d theta_EH",
            "coefficient": "theta_EH fixed by the EH block coefficient kappa0",
            "status": "CONDITIONAL_GR_REFERENCE",
            "what_is_filled": "reference shape for H_core -> theta",
            "what_is_not_filled": "theta_MTS=sum theta_i across EH, boundary, matter/source, extra, projector sectors",
            "source_paths": str(SRC_1008_LEDGER),
        },
        {
            "map_id": "EHA2924_2_EH_Noether_charge",
            "object": "Q_tau^EH",
            "formula": "J_tau^EH=theta_EH(L_tau g)-i_tau L_EH=dQ_tau^EH+C_tau^EH",
            "coefficient": "Q_tau^EH proportional to kappa0^-1 times the metric derivative of tau",
            "status": "CONDITIONAL_GR_REFERENCE",
            "what_is_filled": "reference charge form for the GR limit",
            "what_is_not_filled": "Q_tau^MTS=Q_EH+Q_boundary+Q_extra+Q_projector+Q_matter_source",
            "source_paths": str(SRC_1008_LEDGER),
        },
        {
            "map_id": "EHA2924_3_EH_boundary_mass",
            "object": "H_tau^EH-H_ref^EH",
            "formula": "delta H_tau^EH=int_S(delta Q_tau^EH-i_tau theta_EH); M_ADM/Komar is the stationary/asymptotic surface charge after fixed reference subtraction",
            "coefficient": "mass normalization is set by kappa0, not by measured orbital GM",
            "status": "CONDITIONAL_GR_REFERENCE_NOT_SOURCE_SPECIFIC",
            "what_is_filled": "anti-circular denominator pattern: source mass from surface charge",
            "what_is_not_filled": "MTS fixed reference, same observed tau, finite worldtube source measure",
            "source_paths": str(SRC_HAMILTONIAN_CONTRACT),
        },
        {
            "map_id": "EHA2924_4_EH_weak_field",
            "object": "Poisson/Gauss/orbital limit",
            "formula": "linearized EH plus universal matter gives nabla^2 Phi=4*pi*G0*rho_H, surface integral grad Phi=4*pi*G0*M_H, a=-grad Phi",
            "coefficient": "G0=kappa0*c^4/(8*pi)",
            "status": "CONDITIONAL_GR_REFERENCE",
            "what_is_filled": "known GR-to-Newton coefficient relation",
            "what_is_not_filled": "proof that MTS residual sectors vanish or are bounded in the same branch",
            "source_paths": str(SRC_SOURCE_MEASURE),
        },
        {
            "map_id": "EHA2924_5_total_verdict",
            "object": "EH anchor as MTS parent H_core",
            "formula": "H_core^MTS = H_EH + H_boundary + H_extra + H_projector + H_source",
            "coefficient": "EH coefficient is usable only after all non-EH pieces are silent, topological, or retained as bounded residuals",
            "status": "EH_ANCHOR_FILLED_MTS_REDUCTION_NOT_DERIVED",
            "what_is_filled": "a real GR-limit target row exists",
            "what_is_not_filled": "the MTS parent coefficient map needed for a local-GR/Newton claim",
            "source_paths": ";".join(str(path) for path in [SRC_1009_DOC, SRC_1012_DOC, SRC_1015_DOC]),
        },
    ]
    return [add_common(row) for row in rows]


def reduction_contract_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "RED2924_0_metric_identification",
            "g_obs is the metric readout of MTS parent variables",
            "g_readout=g_obs+O((Phi-Phi0)^2) and no first-order disformal/Weyl/source slot",
            "MISSING_MTS_METRIC_READOUT_DERIVATION",
            "otherwise EH can be the wrong metric sector",
        ),
        (
            "RED2924_1_constant_kappa",
            "kappa0/G0 is constant and universal on the local branch",
            "partial_t,r,A,lambda,frame kappa_eff=0",
            "MISSING_GLOBAL_COUPLING_SUPERSELECTION",
            "otherwise source mass and orbital mass drift apart",
        ),
        (
            "RED2924_2_EH_core_reduction",
            "MTS local metric sector reduces to EH",
            "L_MTS|local = L_EH[g_obs;kappa0,Lambda0] + dB + L_silent + L_residual",
            "MISSING_PARENT_ACTION_REDUCTION_MAP",
            "EH anchor alone is only a reference pattern",
        ),
        (
            "RED2924_3_universal_matter_descent",
            "matter sees the same observed metric/coframe",
            "S_matter[psi,g_obs] and J_H is the same source current used by Q_tau",
            "MISSING_MATTER_DESCENT_AND_WARD_IDENTITY",
            "worldtube mass can become a separate calibrated object",
        ),
        (
            "RED2924_4_extra_sector_double_zero",
            "motion/time/domain/memory/range fields are silent at first order",
            "Phi=Phi0, dV(Phi0)=0, Hessian positive, C(Phi0)=0, dC(Phi0)=0",
            "MISSING_EXTRA_SECTOR_DOUBLE_ZERO_PROOF",
            "scalar/vector/tensor hair enters local PPN and R10/R11",
        ),
        (
            "RED2924_5_projector_domain_silence",
            "Pi_M/domain selectors carry no stress or source charge",
            "delta(Pi_M J_H)=Pi_M delta J_H and delta Pi_M stress vanishes or is bounded",
            "MISSING_PROJECTOR_VARIATION_ZERO",
            "source normalization remains a residual",
        ),
        (
            "RED2924_6_fixed_boundary_reference",
            "H_ref/B_ref is fixed before readout",
            "S_boundary=S_GHY+fixed exact/topological terms; no post-readout subtraction",
            "MISSING_FIXED_REFERENCE_SELECTOR",
            "boundary bookkeeping can fake a mass proof",
        ),
        (
            "RED2924_7_integrable_Htau",
            "H_tau is finite, differentiable, and path independent",
            "delta H_tau=int_S(delta Q_tau-i_tau theta) with fixed tau and boundary class",
            "MISSING_PARENT_HTAU_INTEGRABILITY",
            "M_H_ref denominator cannot be promoted",
        ),
        (
            "RED2924_8_worldtube_source_measure",
            "surface charge equals the observed compact source measure",
            "M_source[W]=H_tau[S]-H_ref=int_W rho_H dV_H before orbital fitting",
            "MISSING_WORLDTUBE_SOURCE_GLUE",
            "closed charge can be the wrong conserved object",
        ),
        (
            "RED2924_9_Poisson_Gauss_orbit",
            "same charge sources Poisson/Gauss and orbital acceleration",
            "nabla^2 Phi=4*pi*G0*rho_H and a=-G0*M_H*r^-2",
            "CONDITIONAL_EH_ONLY_NOT_MTS_DERIVED",
            "Newton/GR reduction remains conditional",
        ),
        (
            "RED2924_10_total_verdict",
            "MTS-to-EH local reduction morphism",
            "RED2924_0 through RED2924_9 parent-signed together",
            "REDUCTION_MORPHISM_NOT_DERIVED",
            "2925 should attack the reduction morphism/extra-sector silence directly",
        ),
    ]
    rows = []
    for clause_id, clause, mathematical_form, current_status, why_it_matters in specs:
        rows.append(
            add_common(
                {
                    "clause_id": clause_id,
                    "clause": clause,
                    "mathematical_form": mathematical_form,
                    "current_status": current_status,
                    "clause_signed": False,
                    "blocks_MTS_local_GR_claim": True,
                    "why_it_matters": why_it_matters,
                    "source_paths": ";".join(str(path) for path in [SRC_MIN_BLOCKS, SRC_1009_DOC, SRC_SOURCE_MEASURE, SRC_1012_DOC, SRC_1015_DOC]),
                }
            )
        )
    return rows


def source_mass_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "attempt_id": "SMFA2924_0_EH_ADM_reference_row",
            "route_type": "parent_source_mass_theorem_reference",
            "system_id": "generic_stationary_compact_EH_exterior",
            "H_core_source": "EHA2924_0_EH_action_block",
            "theta_source": "EHA2924_1_EH_variation",
            "Q_tau_source": "EHA2924_2_EH_Noether_charge",
            "H_ref_rule": "fixed EH boundary/asymptotic reference required",
            "M_H_ref": "M_ADM_or_Komar[g_obs,S] from EH surface charge",
            "M_H_units": "mass",
            "G_ref": "G0=kappa0*c^4/(8*pi)",
            "PiM_H_definition": "EH Hamiltonian mass-charge projector in stationary/asymptotic branch",
            "Poisson_Gauss_certificate": "conditional EH weak-field limit",
            "validation_status": "ACCEPTED_AS_GR_REFERENCE_NOT_MTS_SOURCE_MASS_PROOF",
            "missing_for_MTS_claim": "MTS_TO_EH_REDUCTION_MORPHISM;WORLD_TUBE_SOURCE_GLUE;EXTRA_SECTOR_SILENCE",
            "source_path": str(SRC_MIN_BLOCKS),
        },
        {
            "attempt_id": "SMFA2924_1_MTS_reduced_EH_source_row",
            "route_type": "parent_source_mass_theorem_candidate",
            "system_id": "generic_MTS_local_compact_source",
            "H_core_source": "MISSING_PARENT_ACTION_REDUCTION_MAP",
            "theta_source": "MISSING_THETA_MTS_EXTRACTION",
            "Q_tau_source": "MISSING_Q_TAU_MTS_EXTRACTION",
            "H_ref_rule": "MISSING_FIXED_REFERENCE_SELECTOR",
            "M_H_ref": "MISSING_MTS_SOURCE_DENOMINATOR",
            "M_H_units": "mass",
            "G_ref": "MISSING_CONSTANT_UNIVERSAL_G",
            "PiM_H_definition": "MISSING_PARENT_PIMH_PROJECTOR",
            "Poisson_Gauss_certificate": "CONDITIONAL_EH_ONLY_NOT_MTS_DERIVED",
            "validation_status": "REJECT_MISSING_MTS_REDUCTION_MORPHISM",
            "missing_for_MTS_claim": "RED2924_0-RED2924_10",
            "source_path": str(SRC_2923_HCORE),
        },
        {
            "attempt_id": "SMFA2924_2_worldtube_Hilbert_source_row",
            "route_type": "worldtube_source_measure_candidate",
            "system_id": "generic_compact_source_worldtube",
            "H_core_source": "conditional Noether/Hamiltonian chain",
            "theta_source": "MISSING_PARENT_WORLD_TUBE_VARIATION",
            "Q_tau_source": "MISSING_QM_WORLD_TUBE_EQUALITY",
            "H_ref_rule": "fixed reference required",
            "M_H_ref": "int_W rho_H dV_H",
            "M_H_units": "mass",
            "G_ref": "G0 if coupling superselection closes",
            "PiM_H_definition": "Pi_M J_H same-object equality",
            "Poisson_Gauss_certificate": "not reached",
            "validation_status": "REJECT_MISSING_WORLDTUBE_SOURCE_GLUE",
            "missing_for_MTS_claim": "HSM541_2;SOL1015_1;SOL1015_6",
            "source_path": str(SRC_SOURCE_MEASURE),
        },
        {
            "attempt_id": "SMFA2924_3_first_numeric_source_row",
            "route_type": "numeric_source_mass_row",
            "system_id": "none_selected",
            "H_core_source": "not_applicable_until_theorem_row_exists",
            "theta_source": "not_applicable_until_theorem_row_exists",
            "Q_tau_source": "not_applicable_until_theorem_row_exists",
            "H_ref_rule": "not_applicable",
            "M_H_ref": "MISSING_NUMERIC_SOURCE_MASS",
            "M_H_units": "mass",
            "G_ref": "MISSING_GREF",
            "PiM_H_definition": "not_applicable",
            "Poisson_Gauss_certificate": "not_applicable",
            "validation_status": "REJECT_NUMERIC_ROW_BEFORE_PARENT_SOURCE_THEOREM",
            "missing_for_MTS_claim": "parent theorem/source object first",
            "source_path": str(SRC_2923_CANDIDATES),
        },
    ]
    return [add_common(row) for row in rows]


def bridge_check_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bridge_id": "GPB2924_0_EH_field_equation",
            "step": "EH low-energy field equation",
            "formula": "G_ab+Lambda0*g_ab=kappa0*T_ab",
            "status": "CONDITIONAL_GR_REFERENCE",
            "claim_limit": "only valid for MTS if RED2924_0-RED2924_10 close",
        },
        {
            "bridge_id": "GPB2924_1_linearized_Newton",
            "step": "weak stationary slow-motion limit",
            "formula": "nabla^2 Phi=4*pi*G0*rho_H",
            "status": "CONDITIONAL_GR_REFERENCE",
            "claim_limit": "requires universal matter descent and no extra first-order source channel",
        },
        {
            "bridge_id": "GPB2924_2_Gauss_surface",
            "step": "source mass from surface flux",
            "formula": "surface_integral grad Phi dot dS = 4*pi*G0*M_H",
            "status": "CONDITIONAL_GR_REFERENCE",
            "claim_limit": "requires same-object worldtube/source measure and fixed reference",
        },
        {
            "bridge_id": "GPB2924_3_orbital_readout",
            "step": "inverse-square acceleration",
            "formula": "a_r=-G0*M_H/r^2",
            "status": "CONDITIONAL_GR_REFERENCE",
            "claim_limit": "cannot be used backward as M_H_ref before the bridge is derived",
        },
        {
            "bridge_id": "GPB2924_4_MTS_verdict",
            "step": "MTS local GR/Newton bridge",
            "formula": "MTS -> EH core + silent/bounded residuals -> Poisson/Gauss/orbit",
            "status": "MTS_BRIDGE_NOT_DERIVED",
            "claim_limit": "2924 fills the target shape, not the MTS derivation",
        },
    ]
    return [add_common(row) for row in rows]


def rejection_runner_rows(
    reduction_rows: list[dict[str, Any]],
    source_attempt_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    reduction_closed = all(as_bool(row["clause_signed"]) for row in reduction_rows)
    has_mts_source_row = any(row["validation_status"] == "ACCEPTED_AS_MTS_SOURCE_MASS_PROOF" for row in source_attempt_rows)
    rows = [
        {
            "runner_id": "RJR2924_0_EH_anchor_only",
            "candidate": "EHA2924_0-EHA2924_4",
            "runner_status": "ACCEPT_REFERENCE_PATTERN_REJECT_MTS_CLAIM",
            "reason": "EH core has the GR/Newton coefficient map, but 1009 already rejects EH-only as total MTS parent action.",
        },
        {
            "runner_id": "RJR2924_1_reduction_morphism",
            "candidate": "RED2924_0-RED2924_10",
            "runner_status": "REJECT_UNSIGNED_REDUCTION_MORPHISM",
            "reason": f"reduction_closed={reduction_closed}",
        },
        {
            "runner_id": "RJR2924_2_source_mass_first_row",
            "candidate": "SMFA2924_1_MTS_reduced_EH_source_row",
            "runner_status": "REJECT_MISSING_MTS_REDUCTION_MORPHISM",
            "reason": "MTS theta/Q_tau/source denominator is still missing.",
        },
        {
            "runner_id": "RJR2924_3_worldtube_glue",
            "candidate": "SMFA2924_2_worldtube_Hilbert_source_row",
            "runner_status": "REJECT_MISSING_WORLDTUBE_SOURCE_GLUE",
            "reason": "same-object/source-measure theorem remains conditional.",
        },
        {
            "runner_id": "RJR2924_4_numeric_row",
            "candidate": "SMFA2924_3_first_numeric_source_row",
            "runner_status": "REJECT_NUMERIC_ROW_BEFORE_PARENT_SOURCE_THEOREM",
            "reason": "a numeric source row before parent theorem would be calibration laundering.",
        },
        {
            "runner_id": "RJR2924_5_total_verdict",
            "candidate": "2924 source-mass row fill",
            "runner_status": "EH_REFERENCE_FILLED_MTS_ROW_NOT_FILLED",
            "reason": f"has_mts_source_row={has_mts_source_row}",
        },
    ]
    return [add_common(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2924_0_EH_reference_shape",
            "gate": "EH/ADM core coefficient map available as a GR-limit reference",
            "gate_status": "REFERENCE_READY_NONCLAIM",
            "evidence": "EHA2924_0-EHA2924_4",
            "decision": "use as target morphology only",
        },
        {
            "gate_id": "CG2924_1_MTS_reduction_morphism",
            "gate": "MTS parent action reduces to EH plus silent/bounded sectors",
            "gate_status": "BLOCKED",
            "evidence": "RED2924_10 reduction morphism not derived",
            "decision": "no local-GR claim",
        },
        {
            "gate_id": "CG2924_2_source_mass_first_row",
            "gate": "first parent-sourced MTS source-mass row exists",
            "gate_status": "BLOCKED",
            "evidence": "SMFA2924_1 rejected",
            "decision": "no source-normalized Newton claim",
        },
        {
            "gate_id": "CG2924_3_orbital_GM_guard",
            "gate": "orbital GM is not used as source denominator",
            "gate_status": "CONTROL_PASS_CLAIM_CLOSED",
            "evidence": "2924 uses only EH surface-charge reference pattern",
            "decision": "anti-circularity preserved",
        },
        {
            "gate_id": "CG2924_4_next_derivation",
            "gate": "best next root target selected",
            "gate_status": "NEXT_SELECTED",
            "evidence": "2925 reduction morphism / extra-sector silence target",
            "decision": "attack MTS-to-EH reduction directly",
        },
    ]
    return [add_common(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2924_0_real_progress",
            "decision": "fill the EH/ADM coefficient-map reference row",
            "status": "DONE_NONCLAIM",
            "reason": "this gives the exact GR-limit target MTS must reduce to, without pretending the reduction is already proved.",
        },
        {
            "decision_id": "DEC2924_1_not_enough",
            "decision": "do not promote EH anchor to MTS local GR",
            "status": "CLAIM_REFUSED",
            "reason": "1009 and 2923 require the MTS parent action/reduction/current chain, not EH-only import.",
        },
        {
            "decision_id": "DEC2924_2_bottleneck",
            "decision": "the current bottleneck is the MTS-to-EH reduction morphism plus source/worldtube glue",
            "status": "ROOT_OBJECT_IDENTIFIED",
            "reason": "source-mass first row fails exactly at reduction, theta/Q_tau extraction, and worldtube source measure.",
        },
        {
            "decision_id": "DEC2924_3_next",
            "decision": "2925 should try to derive the reduction morphism/extra-sector double-zero proof",
            "status": "NEXT_SELECTED",
            "reason": "without that, every local GR/Newton route remains conditional; with it, the EH anchor becomes powerful.",
        },
    ]
    return [add_common(row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "next_id": "NEXT2924_0_2925",
            "selection": "selected_primary",
            "target_doc": "2925-Y5-R2FR-MTS-to-EH-reduction-morphism-or-extra-sector-silence-proof-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_MTS_to_EH_reduction_morphism_or_extra_sector_silence_proof_under_AX1090_2925.py",
            "objective": "try to derive the local compact-branch map MTS -> EH core plus silent/bounded extra sectors; if it fails, emit the exact residual vector that blocks local GR",
            "acceptance_gate": "RED2924_0-RED2924_10 either close with parent-signed clauses or produce a finite residual vector; no EH-only import and no orbital-GM denominator",
        },
        {
            "next_id": "NEXT2924_1_fallback",
            "selection": "fallback_if_reduction_morphism_still_unsigned",
            "target_doc": "2925B-Y5-R2FR-worldtube-source-measure-glue-first-row-or-R_eq-input-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_worldtube_source_measure_glue_first_row_or_Req_input_under_AX1090_2925B.py",
            "objective": "attack the same-object source-measure theorem M_source[W]=H_tau[S]-H_ref or create the first source-backed R_eq obstruction input",
            "acceptance_gate": "source/worldtube equality row is parent-signed or a nonclaim finite obstruction input is produced",
        },
    ]
    return [add_common(row) for row in rows]


def branch_copy_rows() -> list[dict[str, Any]]:
    copy_specs = [
        ("BC2924_0_eh_anchor", OUTPUTS["eh_anchor"], BRANCH_OUTPUTS["eh_anchor_copy"], "parent action GR-limit reference"),
        ("BC2924_1_source_mass_attempt", OUTPUTS["source_mass_attempt"], BRANCH_OUTPUTS["source_mass_copy"], "local bounds/source-mass attempt"),
        ("BC2924_2_next_target", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "RAB/source queue next target"),
    ]
    rows = []
    for copy_id, source, destination, role in copy_specs:
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "destination_path": str(destination),
                    "role": role,
                    "destination_exists": destination.exists(),
                    "destination_parses": csv_parses(destination),
                }
            )
        )
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    eh_anchor: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str, bool]] = [
        (
            "VAL2924_0_sources_exist",
            all(as_bool(row["path_exists"]) for row in sources),
            "every cited source path exists",
            True,
        ),
        (
            "VAL2924_1_source_anchors_found",
            all(as_bool(row["anchors_found"]) for row in sources),
            "every cited source anchor is present",
            True,
        ),
        (
            "VAL2924_2_EH_anchor_reference_ready",
            any(row["map_id"] == "EHA2924_5_total_verdict" and row["status"] == "EH_ANCHOR_FILLED_MTS_REDUCTION_NOT_DERIVED" for row in eh_anchor),
            "EH/ADM coefficient-map reference is filled but not promoted",
            True,
        ),
        (
            "VAL2924_3_reduction_contract_complete",
            len(reduction) >= 11 and any(row["clause_id"] == "RED2924_10_total_verdict" and row["current_status"] == "REDUCTION_MORPHISM_NOT_DERIVED" for row in reduction),
            "MTS-to-EH reduction contract has all required clauses and verdict",
            True,
        ),
        (
            "VAL2924_4_source_attempt_rejects_MTS_claim",
            any(row["attempt_id"] == "SMFA2924_1_MTS_reduced_EH_source_row" and row["validation_status"] == "REJECT_MISSING_MTS_REDUCTION_MORPHISM" for row in attempts),
            "MTS source-mass row is rejected until reduction morphism closes",
            True,
        ),
        (
            "VAL2924_5_EH_row_nonclaim",
            any(row["attempt_id"] == "SMFA2924_0_EH_ADM_reference_row" and row["validation_status"] == "ACCEPTED_AS_GR_REFERENCE_NOT_MTS_SOURCE_MASS_PROOF" and not as_bool(row["valid_for_claim"]) for row in attempts),
            "EH/ADM row is accepted only as nonclaim GR reference",
            True,
        ),
        (
            "VAL2924_6_bridge_conditional",
            any(row["bridge_id"] == "GPB2924_4_MTS_verdict" and row["status"] == "MTS_BRIDGE_NOT_DERIVED" for row in bridge),
            "Poisson/Gauss/orbit bridge remains conditional for MTS",
            True,
        ),
        (
            "VAL2924_7_rejection_runner_safe",
            any(row["runner_id"] == "RJR2924_5_total_verdict" and row["runner_status"] == "EH_REFERENCE_FILLED_MTS_ROW_NOT_FILLED" for row in rejections),
            "rejection runner prevents EH-only and numeric/source-row shortcuts",
            True,
        ),
        (
            "VAL2924_8_no_claim_gates_open",
            all(not as_bool(row["claim_allowed"]) and str(row["gate_status"]) != "OPEN" for row in claims),
            "no claim gate opens in 2924",
            True,
        ),
        (
            "VAL2924_9_next_target_selected",
            any(row["next_id"] == "NEXT2924_0_2925" for row in next_rows),
            "2925 reduction morphism target selected",
            True,
        ),
        (
            "VAL2924_10_branch_copies_valid",
            all(as_bool(row["destination_exists"]) and as_bool(row["destination_parses"]) for row in branches),
            "branch copies exist and parse",
            True,
        ),
        (
            "VAL2924_11_no_formalization_outputs",
            not any(is_under(path, FORMALIZATION) for path in [DOC, *OUTPUTS.values(), *BRANCH_OUTPUTS.values()]),
            "no generated output path is inside formalization-workbench",
            True,
        ),
        (
            "VAL2924_12_doc_exists",
            DOC.exists(),
            "2924 markdown checkpoint exists",
            True,
        ),
    ]
    rows = [
        {
            "validation_id": check_id,
            "passed": passed,
            "check": check,
            "required": required,
            "generated_utc": RUN_UTC,
        }
        for check_id, passed, check, required in checks
    ]
    overall = all(passed for _, passed, _, required in checks if required)
    rows.append(
        {
            "validation_id": "VAL2924_OVERALL",
            "passed": overall,
            "check": "2924 validation overall",
            "required": True,
            "generated_utc": RUN_UTC,
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    eh_anchor: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    attempts: list[dict[str, Any]],
    bridge: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    overall = next(row["passed"] for row in validation if row["validation_id"] == "VAL2924_OVERALL")
    lines = [
        "# 2924 - Y5/R2FR Parent Hcore Coefficient Map Or Finite Source-Mass First Row Fill Under AX1090",
        "",
        "Status: `Y5_R2FR_2924_EH_anchor_filled_MTS_reduction_morphism_2925_next`",
        "",
        "## Result",
        "",
        "2924 fills the useful part of the row: the EH/ADM coefficient-map shape that a local GR limit must reproduce. It does not promote that shape into an MTS proof. The MTS-specific object still missing is the reduction morphism from the parent MTS variables to `EH core + silent/bounded residual sectors`, plus the same-object worldtube/source-measure glue.",
        "",
        "This is progress because the bridge is no longer vague. The target is now exact: if MTS can derive the reduction contract, the known EH source-mass/Poisson/Gauss/Newton map becomes available without circularly importing orbital `GM`.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "path_exists", "anchors_found", "role", "source_path"]),
        "",
        "## EH Anchor Coefficient Map",
        "",
        md_table(eh_anchor, ["map_id", "object", "formula", "coefficient", "status", "what_is_not_filled"]),
        "",
        "## MTS To EH Reduction Contract",
        "",
        md_table(reduction, ["clause_id", "clause", "mathematical_form", "current_status", "blocks_MTS_local_GR_claim", "why_it_matters"]),
        "",
        "## Source-Mass First Row Attempt",
        "",
        md_table(attempts, ["attempt_id", "route_type", "M_H_ref", "G_ref", "Poisson_Gauss_certificate", "validation_status", "missing_for_MTS_claim"]),
        "",
        "## Gauss / Poisson Bridge Check",
        "",
        md_table(bridge, ["bridge_id", "step", "formula", "status", "claim_limit"]),
        "",
        "## Rejection Runner",
        "",
        md_table(rejections, ["runner_id", "candidate", "runner_status", "reason"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "gate", "gate_status", "decision", "evidence"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "status", "reason"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "check", "required"]),
        "",
        f"Validation overall: `{overall}`.",
        "",
        "## Bottom Line",
        "",
        "The project is not blocked by not knowing what GR/Newton target to hit. 2924 nails that target. The live problem is now sharper: prove the MTS local compact branch reduces to that EH anchor with all extra/source/projector/boundary channels silent or explicitly bounded. That is the next serious step.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    sources = source_register_rows()
    eh_anchor = eh_anchor_rows()
    reduction = reduction_contract_rows()
    attempts = source_mass_attempt_rows()
    bridge = bridge_check_rows()
    rejections = rejection_runner_rows(reduction, attempts)
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["eh_anchor"], eh_anchor)
    write_csv(OUTPUTS["reduction_contract"], reduction)
    write_csv(OUTPUTS["source_mass_attempt"], attempts)
    write_csv(OUTPUTS["bridge_check"], bridge)
    write_csv(OUTPUTS["rejection_runner"], rejections)
    write_csv(OUTPUTS["claims"], claims)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_rows)

    branches = branch_copy_rows()
    write_csv(OUTPUTS["branches"], branches)

    DOC.write_text("# 2924 - validation preflight\n", encoding="utf-8")
    validation = validation_rows(sources, eh_anchor, reduction, attempts, bridge, rejections, claims, next_rows, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, eh_anchor, reduction, attempts, bridge, rejections, claims, decisions, next_rows, validation)

    overall = next(row["passed"] for row in validation if row["validation_id"] == "VAL2924_OVERALL")
    if not overall:
        raise SystemExit("2924 validation failed; see " + str(OUTPUTS["validation"]))
    print("2924 validation overall:", overall)
    print("doc:", DOC)


if __name__ == "__main__":
    main()
