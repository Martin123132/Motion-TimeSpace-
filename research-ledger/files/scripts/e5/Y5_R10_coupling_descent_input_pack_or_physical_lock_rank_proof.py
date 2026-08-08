from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "778-Y5-R10-coupling-descent-input-pack-or-physical-lock-rank-proof.md"
NEXT_TARGET = "779-Y5-R10-parent-coupling-descent-signature-or-source-measure-bound-runner.md"
STATUS = "Y5_R10_778_coupling_descent_theorem_written_conditionally_parent_signature_missing_input_pack_created_nonclaim"
CLAIM_CEILING = "conditional_coupling_descent_theorem_and_schema_input_pack_only_no_coupling_zero_no_source_measure_bound_no_physical_lock_rank_no_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_778_SOURCE_REGISTER.csv"
DESCENT_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_778_COUPLING_DESCENT_THEOREM_GATE.csv"
RANK_PROOF_PATH = RESIDUALS / "P8_Y5_R10_778_PHYSICAL_LOCK_RANK_PROOF_ATTEMPT.csv"
INPUT_PACK_PATH = RESIDUALS / "P8_Y5_R10_778_COUPLING_DESCENT_INPUT_PACK.csv"
BOUND_SCHEMA_PATH = RESIDUALS / "P8_Y5_R10_778_SOURCE_MEASURE_BOUND_SCHEMA.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_778_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_778_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_778_VALIDATION.csv"

COUPLING_DESCENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_COUPLING_DESCENT_INPUT_CANDIDATE.csv"
CQMU_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_CQMU_COEFFICIENT_INPUT_CANDIDATE.csv"
SOURCE_FLUX_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_SOURCE_FLUX_VALUE_INPUT_CANDIDATE.csv"
READOUT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_EM_CLOCK_ORBIT_READOUT_INPUT_CANDIDATE.csv"
PPN_COUPLING_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_PPN_COUPLING_RESPONSE_INPUT_CANDIDATE.csv"

SCHEMA_ONLY_INPUTS = [
    COUPLING_DESCENT_CANDIDATE_PATH,
    CQMU_CANDIDATE_PATH,
    SOURCE_FLUX_CANDIDATE_PATH,
    READOUT_CANDIDATE_PATH,
    PPN_COUPLING_CANDIDATE_PATH,
]

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_778_COUPLING_DESCENT_ZERO_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_778_PHYSICAL_LOCK_RANK_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_778_BOBS_SOURCE_MEASURE_BOUND_CLAIM.csv",
    RESIDUALS / "P8_Y5_R10_778_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    DESCENT_THEOREM_PATH,
    RANK_PROOF_PATH,
    INPUT_PACK_PATH,
    BOUND_SCHEMA_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
    *SCHEMA_ONLY_INPUTS,
]

SOURCES: dict[str, dict[str, Any]] = {
    "777_doc": {
        "path": POST_CHECKPOINT / "777-Y5-R10-physical-residual-lock-map-or-Bobs-source-measure-first-pack.md",
        "needles": ["PRL777_5_coupling_source_measure", "D777_3_next_target"],
        "role": "immediate 778 handoff: coupling/source-measure branch selected",
    },
    "777_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_777_VALIDATION.csv",
        "needles": ["V777_4_lock_verdict_not_proved", "pass"],
        "role": "prior validation guard",
    },
    "777_lock_map": {
        "path": RESIDUALS / "P8_Y5_R10_777_PHYSICAL_RESIDUAL_LOCK_MAP.csv",
        "needles": ["PRL777_5_coupling_source_measure", "PRL777_6_verdict"],
        "role": "physical residual lock map",
    },
    "777_source_measure_pack": {
        "path": RESIDUALS / "P8_Y5_R10_777_BOBS_SOURCE_MEASURE_FIRST_PACK.csv",
        "needles": ["BSM777_0_coupling_descent_input", "MISSING_COUPLING_DESCENT_INPUT"],
        "role": "source-measure pack schema handoff",
    },
    "758_parent_contract": {
        "path": RESIDUALS / "P8_Y5_R10_758_PARENT_ACTION_CONTRACT_ATTEMPT.csv",
        "needles": ["PAC758_3_universal_coupling_owner", "PAC758_5_verdict"],
        "role": "full residual-vector parent-action contract",
    },
    "759_coupling_audit": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_OWNER_ACTION_AUDIT.csv",
        "needles": ["COA759_1_quotient_matter_descent", "COA759_6_verdict"],
        "role": "universal coupling owner audit",
    },
    "759_coupling_runner": {
        "path": RESIDUALS / "P8_Y5_R10_759_COUPLING_RESIDUAL_ACQUISITION_RUNNER.csv",
        "needles": ["CAR759_0_coupling_descent_input", "CAR759_5_PPN_coupling_response"],
        "role": "older coupling acquisition runner",
    },
    "776_variation": {
        "path": RESIDUALS / "P8_Y5_R10_776_RESPONSE_DISPLACEMENT_VARIATION_LEDGER.csv",
        "needles": ["RAV776_4_source_measure_coupling", "B_obs_source_measure"],
        "role": "source-measure coupling obstruction from variation ledger",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(source_spec["path"]),
            "exists": bool_string(Path(source_spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(source_spec["path"]), source_spec["needles"])),
            "role": source_spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, source_spec in SOURCES.items()
    ]


def descent_theorem_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CDT778_0_parent_quotient_map",
            "clause": "parent quotient and vertical directions exist",
            "mathematical_form": "q: Phi_parent -> Phi_bar; v_X in ker(Dq); delta_v q(Phi_parent)=0",
            "would_imply": "representative variations are gauge/quotient directions, not physical couplings",
            "current_status": "formal_clause_written_not_parent_signed",
            "missing": "explicit current-MTS q(Phi), Dq, and vertical generator basis",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CDT778_1_observed_geometry_descent",
            "clause": "single observed geometry descends through q",
            "mathematical_form": "e_obs = e_bar[q(Phi_parent), theta]; g_obs=e_obs^T eta e_obs; Lie_v e_obs=0",
            "would_imply": "matter/source/clock/photon/orbit see the same geometry",
            "current_status": "conditional_only",
            "missing": "parent-signed e_obs map and proof no hidden Weyl/disformal representative enters",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CDT778_2_matter_action_descent",
            "clause": "matter action is quotient-invariant",
            "mathematical_form": "S_matter[Phi_parent,Psi]=Sbar_matter[q(Phi_parent),Psi,theta]; Lie_v S_matter=0",
            "would_imply": "vertical variations cannot create fifth-force/source-measure coupling work",
            "current_status": "not_parent_signed",
            "missing": "explicit matter Lagrangian and source path tying it to MTS parent fields",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CDT778_3_source_current_descent",
            "clause": "source current is Hilbert-owned before measured-GM calibration",
            "mathematical_form": "T_m^{mu nu}=2/sqrt(-g_obs) delta S_matter/delta g_obs_mu_nu; J_H[tau]=T_m^{mu nu} tau_nu dSigma_mu",
            "would_imply": "source mass/readout is not an independent coupling knob",
            "current_status": "not_closed",
            "missing": "source-current closure, Pi_M/Gauss normalization, and orbital calibration descent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CDT778_4_readout_descent",
            "clause": "clock, photon, orbit, EM/charge, and PPN readouts descend through the same observed structure",
            "mathematical_form": "O_A = O_A[e_obs,Psi_A,owned charges]; partial O_A/partial C_hidden = 0",
            "would_imply": "readout leakage does not fake or hide q_loc/Y5/Y6/PPN residuals",
            "current_status": "not_closed",
            "missing": "readout functionals and no-hidden-map proof for every arena",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CDT778_5_species_constant_lock",
            "clause": "species constants do not depend on local MTS/domain/source fields",
            "mathematical_form": "partial_{Phi,D,kappa_local} m_A = partial_{Phi,D,kappa_local} q_A = 0 at fixed e_obs",
            "would_imply": "WEP/clock/EM-charge residuals are not sourced by hidden local labels",
            "current_status": "not_closed",
            "missing": "mass/charge/clock constants owner and EM charge interface source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CDT778_6_boundary_source_measure_silence",
            "clause": "descent variation has no leftover boundary/source-measure work",
            "mathematical_form": "delta_v S_matter + delta_v S_readout = 0 and B_obs_source_measure = 0 under compact-local boundary conditions",
            "would_imply": "source-measure part of B_obs vanishes rather than needing a numeric bound",
            "current_status": "not_closed",
            "missing": "boundary/source/corner/no-flux theorem or finite flux input rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CDT778_7_theorem_result",
            "clause": "conditional coupling descent theorem",
            "mathematical_form": "If CDT778_0..CDT778_6 close, then DeltaCoupling_A=0 and B_obs_source_measure/M_H=0 for quotient-vertical local variations.",
            "would_imply": "coupling block can be removed from the physical residual nullspace problem",
            "current_status": "conditional_theorem_only_not_current_MTS_claim",
            "missing": "all parent signatures and source/readout/boundary clauses above",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def rank_proof_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "rank_id": "RPA778_0_block_form",
            "claim_attempt": "split L^I_A into geometry, boundary, and coupling blocks",
            "mathematical_form": "L = [[L_geom, L_gc], [L_bg, L_boundary], [L_cg, L_coupling]] after gauge quotient",
            "result": "formal_decomposition_only",
            "blocker": "component matrices are not sourced",
            "next_input": "q_loc/Y5/Y6/PPN/boundary/coupling response rows",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "RPA778_1_coupling_block_zero",
            "claim_attempt": "use coupling descent theorem to set L_coupling=0 and B_obs_source_measure=0",
            "mathematical_form": "Lie_v S_matter=Lie_v S_readout=0 -> partial R_phys^coupling/partial R^A = 0 for vertical representative modes",
            "result": "not_promoted",
            "blocker": "CDT778_0..CDT778_6 are unsigned in current corpus",
            "next_input": "parent coupling descent signature or source-measure bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "RPA778_2_Y5_coupling_leak",
            "claim_attempt": "show measured-GM/source normalization is insensitive to coupling/readout labels",
            "mathematical_form": "partial epsilon_mu/partial C_hidden = 0 at fixed e_obs and fixed Hilbert source current",
            "result": "not_closed",
            "blocker": "source current and orbital calibration descent are not signed",
            "next_input": "source-current descent row or finite C_qmu bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "RPA778_3_PPN_coupling_leak",
            "claim_attempt": "show PPN coefficients do not receive hidden coupling/readout contributions",
            "mathematical_form": "partial DeltaPPN_I/partial C_hidden = 0 or sourced W^I_coupling",
            "result": "not_closed",
            "blocker": "PPN coupling response rows are absent",
            "next_input": "PPN coupling response input candidate",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "rank_id": "RPA778_4_verdict",
            "claim_attempt": "promote physical-lock rank proof after coupling descent",
            "mathematical_form": "rank(L)=dim(R_phys) and ker(L) contains only gauge/quotient directions",
            "result": "rank_proof_not_complete",
            "blocker": "coupling descent theorem is conditional and response matrices are unsourced",
            "next_input": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def input_pack_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "pack_id": "CIP778_0_coupling_descent_candidate",
            "artifact": str(COUPLING_DESCENT_CANDIDATE_PATH),
            "required_columns": "system_id;source_channel;matter_action_owner;uses_e_obs;uses_q_parent;hidden_frame_map;coupling_descent_status;source_path;valid_for_claim",
            "purpose": "prove or falsify quotient-invariant matter/source/readout descent",
            "current_status": "schema_created_rows_missing_parent_signatures",
            "promotion_gate": "all sector rows have real source_path, uses_e_obs=true, uses_q_parent=true, hidden_frame_map=absent, and valid_for_claim=true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CIP778_1_Cqmu_candidate",
            "artifact": str(CQMU_CANDIDATE_PATH),
            "required_columns": "system_id;source_channel;C_qmu;units;q_loc_component;M_H_ref;normalization;source_path;valid_for_claim",
            "purpose": "bound source-measure leakage if theorem-zero fails",
            "current_status": "schema_created_numeric_values_missing",
            "promotion_gate": "positive units, numeric C_qmu, sourced normalization, valid_for_claim=true",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CIP778_2_source_flux_candidate",
            "artifact": str(SOURCE_FLUX_CANDIDATE_PATH),
            "required_columns": "system_id;annulus_or_surface;flux_value;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "purpose": "supply B_obs_source_measure/M_H value or bound",
            "current_status": "schema_created_flux_values_missing",
            "promotion_gate": "finite flux, M_H_ref, source path, assumptions, no-cancellation flag",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CIP778_3_readout_candidate",
            "artifact": str(READOUT_CANDIDATE_PATH),
            "required_columns": "sector;readout_functional;uses_e_obs;uses_hidden_map;coefficient;units;source_path;valid_for_claim",
            "purpose": "audit EM/clock/orbit/source readout leakage",
            "current_status": "schema_created_readout_coefficients_missing",
            "promotion_gate": "uses_hidden_map=false or finite sourced coefficient bound",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "pack_id": "CIP778_4_PPN_coupling_candidate",
            "artifact": str(PPN_COUPLING_CANDIDATE_PATH),
            "required_columns": "PPN_coefficient;coupling_channel;linear_response;gauge;frame;source_path;valid_for_claim",
            "purpose": "audit whether coupling/readout leakage enters PPN coefficients",
            "current_status": "schema_created_PPN_responses_missing",
            "promotion_gate": "linear_response numeric/theorem-zero with gauge and frame source",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bound_schema_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "SMB778_0_theorem_zero_route",
            "route": "derive B_obs_source_measure=0",
            "required_input": "CDT778_0..CDT778_6 parent-signed",
            "status": "conditional_only",
            "claim_rule": "promote only if every descent clause is signed and boundary/source work is silent",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "SMB778_1_numeric_bound_route",
            "route": "bound B_obs_source_measure/M_H",
            "required_input": "C_qmu coefficients, flux values, M_H_ref, readout response coefficients, and source paths",
            "status": "schema_only",
            "claim_rule": "promote only if every component is valid_for_claim=true and no cancellation between unknowns is used",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "bound_id": "SMB778_2_fail_closed_route",
            "route": "if neither theorem-zero nor numeric bound closes",
            "required_input": "explicit residual coefficient remains in local branch",
            "status": "fallback_open",
            "claim_rule": "local-GR recovery remains blocked and coupling residual must enter empirical fits",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def coupling_descent_candidate_rows() -> list[dict[str, Any]]:
    rows = []
    for channel in ["matter_action", "source_current", "clock_readout", "photon_readout", "orbit_readout", "EM_charge_interface", "PPN_readout"]:
        rows.append(
            {
                "system_id": "MTS_local_branch",
                "source_channel": channel,
                "matter_action_owner": "MISSING_PARENT_SIGNED_OWNER",
                "uses_e_obs": "MISSING",
                "uses_q_parent": "MISSING",
                "hidden_frame_map": "MISSING_ABSENCE_PROOF",
                "coupling_descent_status": "MISSING_COUPLING_DESCENT_SIGNATURE",
                "source_path": "MISSING_SOURCE_PATH",
                "valid_for_claim": "false",
            }
        )
    return rows


def cqmu_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "system_id": "MTS_local_branch",
            "source_channel": channel,
            "C_qmu": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "units": "MISSING_UNITS",
            "q_loc_component": "MISSING_QLOC_COMPONENT",
            "M_H_ref": "MISSING_MH_REFERENCE",
            "normalization": "MISSING_NORMALIZATION",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": "false",
        }
        for channel in ["source_mass", "orbit_readout", "clock_readout", "EM_charge", "PPN_response"]
    ]


def source_flux_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "system_id": "MTS_local_branch",
            "annulus_or_surface": surface,
            "flux_value": "MISSING_FLUX_VALUE_OR_NO_FLUX_THEOREM",
            "M_H_ref": "MISSING_MH_REFERENCE",
            "units": "MISSING_UNITS",
            "source_path": "MISSING_SOURCE_PATH",
            "assumptions": "MISSING_BOUNDARY_AND_SOURCE_ASSUMPTIONS",
            "valid_for_claim": "false",
        }
        for surface in ["compact_local_boundary", "orbital_calibration_annulus", "clock_lab_region", "EM_charge_interface"]
    ]


def readout_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": sector,
            "readout_functional": "MISSING_READOUT_FUNCTIONAL",
            "uses_e_obs": "MISSING",
            "uses_hidden_map": "MISSING_ABSENCE_OR_BOUND",
            "coefficient": "MISSING_COEFFICIENT",
            "units": "MISSING_UNITS",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": "false",
        }
        for sector in ["clock", "photon", "orbit", "EM_charge", "source_mass", "PPN"]
    ]


def ppn_coupling_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "PPN_coefficient": coefficient,
            "coupling_channel": "MISSING_CHANNEL_MAP",
            "linear_response": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "gauge": "MISSING_GAUGE_CERTIFICATE",
            "frame": "MISSING_FRAME_CERTIFICATE",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": "false",
        }
        for coefficient in ["gamma", "beta", "alpha1", "alpha2", "alpha3", "xi", "zeta1_to_zeta4", "Gdot", "R11"]
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D778_0_descent_theorem_written",
            "decision": "keep the quotient coupling-descent theorem as the clean derivation route",
            "reason": "if matter/readout/source actions descend through q(Phi), representative coupling work is gauge/quotient and can vanish",
            "claim_status": "conditional_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D778_1_rank_proof_not_promoted",
            "decision": "do not promote physical-lock rank proof",
            "reason": "the coupling block and response matrices are still unsigned or unsourced",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D778_2_input_pack_created",
            "decision": "create schema-only input pack rows for coupling descent, C_qmu, source flux, readouts, and PPN coupling",
            "reason": "this turns the missing coupling into concrete source rows rather than a vague worry",
            "claim_status": "schema_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D778_3_next_target",
            "decision": "try to parent-sign the coupling descent clauses or run the source-measure bound route",
            "reason": "that decides whether the coupling problem is a theorem-zero branch or an empirical residual coefficient",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "coupling descent has a clean conditional theorem, but current MTS lacks the parent signatures; input packs now exist as schema-only nonclaim rows",
            "hard_blocker": "matter/source/readout/EM/PPN descent through one parent-owned observed geometry is not yet proved",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def candidate_files_parse() -> bool:
    for path in SCHEMA_ONLY_INPUTS:
        rows = read_csv_rows(path)
        if not rows:
            return False
        if any(row.get("valid_for_claim") != "false" for row in rows):
            return False
    return True


def candidate_rows_have_missing_markers() -> bool:
    for path in SCHEMA_ONLY_INPUTS:
        rows = read_csv_rows(path)
        if not rows:
            return False
        for row in rows:
            if "MISSING" not in ",".join(str(value) for value in row.values()):
                return False
    return True


def validation_rows(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    rank_proof: list[dict[str, Any]],
    input_pack: list[dict[str, Any]],
    bound_schema: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    expected_theorem_ids = {
        "CDT778_0_parent_quotient_map",
        "CDT778_1_observed_geometry_descent",
        "CDT778_2_matter_action_descent",
        "CDT778_3_source_current_descent",
        "CDT778_4_readout_descent",
        "CDT778_5_species_constant_lock",
        "CDT778_6_boundary_source_measure_silence",
        "CDT778_7_theorem_result",
    }
    expected_rank_ids = {
        "RPA778_0_block_form",
        "RPA778_1_coupling_block_zero",
        "RPA778_2_Y5_coupling_leak",
        "RPA778_3_PPN_coupling_leak",
        "RPA778_4_verdict",
    }
    expected_pack_ids = {
        "CIP778_0_coupling_descent_candidate",
        "CIP778_1_Cqmu_candidate",
        "CIP778_2_source_flux_candidate",
        "CIP778_3_readout_candidate",
        "CIP778_4_PPN_coupling_candidate",
    }

    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_777_clean = all(validation_clean(number) for number in range(665, 778))
    theorem_gate_complete = expected_theorem_ids.issubset({row["theorem_id"] for row in theorem})
    theorem_not_promoted = any(
        row["theorem_id"] == "CDT778_7_theorem_result" and row["current_status"] == "conditional_theorem_only_not_current_MTS_claim"
        for row in theorem
    )
    rank_attempt_complete = expected_rank_ids.issubset({row["rank_id"] for row in rank_proof})
    rank_not_promoted = any(row["rank_id"] == "RPA778_4_verdict" and row["result"] == "rank_proof_not_complete" for row in rank_proof)
    input_pack_complete = expected_pack_ids.issubset({row["pack_id"] for row in input_pack})
    bound_schema_complete = len(bound_schema) == 3
    candidate_artifacts_exist = all(path.exists() for path in SCHEMA_ONLY_INPUTS)
    schema_inputs_parse = candidate_files_parse()
    schema_inputs_missing = candidate_rows_have_missing_markers()
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, theorem, rank_proof, input_pack, bound_schema, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D778_3_next_target" for row in decisions)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V778_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V778_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V778_2_prior_665_777_clean", prior_665_777_clean, "665-777 validation rows have no failures"),
        ("V778_3_theorem_gate_complete", theorem_gate_complete, "coupling descent theorem clauses complete"),
        ("V778_4_theorem_not_promoted", theorem_not_promoted, "conditional theorem not treated as current-MTS proof"),
        ("V778_5_rank_attempt_complete", rank_attempt_complete, "physical-lock rank proof attempt rows complete"),
        ("V778_6_rank_not_promoted", rank_not_promoted, "rank proof remains blocked"),
        ("V778_7_input_pack_complete", input_pack_complete, "coupling descent input pack rows complete"),
        ("V778_8_bound_schema_complete", bound_schema_complete, "source-measure bound route schema complete"),
        ("V778_9_schema_inputs_created", candidate_artifacts_exist, "schema-only candidate CSVs exist"),
        ("V778_10_schema_inputs_parse_false", schema_inputs_parse, "candidate rows parse and remain valid_for_claim=false"),
        ("V778_11_schema_inputs_missing_markers", schema_inputs_missing, "candidate rows keep MISSING markers"),
        ("V778_12_no_claim_rows_promoted", no_claim_rows_promoted, "all generated summary rows valid_for_claim=false"),
        ("V778_13_claim_artifacts_absent", claim_artifacts_absent, "no zero/rank/bound/local-GR claim artifact fabricated"),
        ("V778_14_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V778_15_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V778_16_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V778_17_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    rank_proof: list[dict[str, Any]],
    input_pack: list[dict[str, Any]],
    bound_schema: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 778 - Y5 R10 Coupling Descent Input Pack Or Physical-Lock Rank Proof

Current result: **the coupling route has a clean conditional theorem, but not a current-MTS proof yet**. If the matter/source/readout actions really descend through a parent quotient `q(Phi)` and one observed geometry `e_obs`, then quotient-vertical representative motion cannot create physical coupling work: `Lie_v S_matter = Lie_v S_readout = 0` and the source-measure piece can be theorem-zero. The problem is that the parent signatures are still missing, so 778 creates the first schema-only input pack instead of smuggling in the coupling zero.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Coupling Descent Theorem Gate

{markdown_table(theorem, ["theorem_id", "clause", "mathematical_form", "would_imply", "current_status", "missing", "valid_for_claim"])}

## Physical-Lock Rank Proof Attempt

{markdown_table(rank_proof, ["rank_id", "claim_attempt", "mathematical_form", "result", "blocker", "next_input", "valid_for_claim"])}

## Coupling Descent Input Pack

{markdown_table(input_pack, ["pack_id", "artifact", "required_columns", "purpose", "current_status", "promotion_gate", "valid_for_claim"])}

## Source-Measure Bound Schema

{markdown_table(bound_schema, ["bound_id", "route", "required_input", "status", "claim_rule", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

This is a good narrowing rather than a retreat. The coupling problem now has two honest routes: either parent-sign the descent theorem and set the source-measure block to zero, or treat the source-measure block as a finite residual with sourced coefficients. The local-GR route should not pass until one of those routes closes.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    theorem = descent_theorem_rows(generated_utc)
    rank_proof = rank_proof_rows(generated_utc)
    input_pack = input_pack_rows(generated_utc)
    bound_schema = bound_schema_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)

    write_csv(COUPLING_DESCENT_CANDIDATE_PATH, coupling_descent_candidate_rows(), ["system_id", "source_channel", "matter_action_owner", "uses_e_obs", "uses_q_parent", "hidden_frame_map", "coupling_descent_status", "source_path", "valid_for_claim"])
    write_csv(CQMU_CANDIDATE_PATH, cqmu_candidate_rows(), ["system_id", "source_channel", "C_qmu", "units", "q_loc_component", "M_H_ref", "normalization", "source_path", "valid_for_claim"])
    write_csv(SOURCE_FLUX_CANDIDATE_PATH, source_flux_candidate_rows(), ["system_id", "annulus_or_surface", "flux_value", "M_H_ref", "units", "source_path", "assumptions", "valid_for_claim"])
    write_csv(READOUT_CANDIDATE_PATH, readout_candidate_rows(), ["sector", "readout_functional", "uses_e_obs", "uses_hidden_map", "coefficient", "units", "source_path", "valid_for_claim"])
    write_csv(PPN_COUPLING_CANDIDATE_PATH, ppn_coupling_candidate_rows(), ["PPN_coefficient", "coupling_channel", "linear_response", "gauge", "frame", "source_path", "valid_for_claim"])

    validation = validation_rows(sources, theorem, rank_proof, input_pack, bound_schema, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(DESCENT_THEOREM_PATH, theorem, ["theorem_id", "clause", "mathematical_form", "would_imply", "current_status", "missing", "valid_for_claim", "generated_utc"])
    write_csv(RANK_PROOF_PATH, rank_proof, ["rank_id", "claim_attempt", "mathematical_form", "result", "blocker", "next_input", "valid_for_claim", "generated_utc"])
    write_csv(INPUT_PACK_PATH, input_pack, ["pack_id", "artifact", "required_columns", "purpose", "current_status", "promotion_gate", "valid_for_claim", "generated_utc"])
    write_csv(BOUND_SCHEMA_PATH, bound_schema, ["bound_id", "route", "required_input", "status", "claim_rule", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, theorem, rank_proof, input_pack, bound_schema, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"778 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
