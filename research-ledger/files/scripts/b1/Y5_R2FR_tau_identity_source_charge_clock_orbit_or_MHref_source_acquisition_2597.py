from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R2FR_TAU_IDENTITY_SOURCE_CHARGE_CLOCK_ORBIT_2597"
CHECKPOINT_ID = "2597"

DOC = ROOT / "2597-Y5-R2FR-tau-identity-source-charge-clock-orbit-or-MHref-source-acquisition.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_TAU_IDENTITY_2597_SOURCE_REGISTER.csv",
    "theorem_audit": OUT / "P8_Y5_TAU_IDENTITY_2597_THEOREM_AUDIT.csv",
    "role_residual_rows": OUT / "P8_Y5_TAU_IDENTITY_2597_ROLE_RESIDUAL_ROWS.csv",
    "mhref_acquisition_rows": OUT / "P8_Y5_TAU_IDENTITY_2597_MHREF_SOURCE_ACQUISITION_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_TAU_IDENTITY_2597_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_TAU_IDENTITY_2597_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_TAU_IDENTITY_2597_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_TAU_IDENTITY_2597_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_TAU_IDENTITY_2597_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2597_VALIDATION.csv",
}

COPY_TARGETS = {
    "theorem_audit": QUEUE / "JR2597_TAU_IDENTITY_THEOREM_AUDIT_NONCLAIM.csv",
    "role_residual_rows": LOCAL_BOUNDS / "Tau_identity_role_residual_rows_2597_NONCLAIM.csv",
    "mhref_acquisition_rows": LOCAL_BOUNDS / "MHref_tau_source_acquisition_rows_2597_NONCLAIM.csv",
    "next_target": QUEUE / "JR2597_PARENT_STATIONARY_TAU_OR_SOURCE_ROWS_NEXT.csv",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def with_stamp(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "timestamp_utc": utc_now(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        **row,
    }


def row_value(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple, set)):
        return ";".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row_value(row.get(field, "")) for field in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return bool(rows), len(rows), ""
    except Exception as exc:  # pragma: no cover - validation reports the error.
        return False, 0, str(exc)


def path_has_needles(path: Path, needles: list[str]) -> list[str]:
    if not path.exists():
        return needles
    text = path.read_text(encoding="utf-8", errors="replace")
    return [needle for needle in needles if needle not in text]


def source_register_rows() -> list[dict[str, Any]]:
    source_specs = [
        {
            "source_id": "SRC2597_00_2596_handoff",
            "source_path": ROOT / "2596-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row.md",
            "needles": ["NEXT2596_0_selected", "MHL2596_2_tau_identity", "VAL2596_OVERALL"],
            "role": "active handoff selecting tau identity/M_H_ref source acquisition",
        },
        {
            "source_id": "SRC2597_01_2596_next_queue",
            "source_path": QUEUE / "JR2596_TAU_IDENTITY_OR_MHREF_SOURCE_ACQUISITION_NEXT.csv",
            "needles": ["NEXT2596_0_selected", "2597-Y5-R2FR-tau-identity-source-charge-clock-orbit-or-MHref-source-acquisition.md"],
            "role": "machine-readable 2597 target and guardrails",
        },
        {
            "source_id": "SRC2597_02_685_tau_doc",
            "source_path": ROOT / "685-Y5-R10-tau-generator-Killing-clock-lock-or-frame-residual-fill.md",
            "needles": ["TGC685_0_define_tau_obs", "TGC685_6_verdict"],
            "role": "prior tau generator contract and failure diagnosis",
        },
        {
            "source_id": "SRC2597_03_685_tau_contract",
            "source_path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "needles": ["TGC685_2_Hamiltonian_boundary_route", "TGC685_5_orbit_readout_route", "TGC685_6_verdict"],
            "role": "machine tau source/charge/clock/orbit/boundary contract",
        },
        {
            "source_id": "SRC2597_04_684_tau_audit",
            "source_path": OUT / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
            "needles": ["TGA684_0_source_tau", "TGA684_6_total"],
            "role": "older tau role audit feeding M_H_ref denominator",
        },
        {
            "source_id": "SRC2597_05_2390_same_frame",
            "source_path": ROOT / "2390-Y5-R2FR-observed-coframe-pullback-same-frame-lock-or-frame-source-leak-values.md",
            "needles": ["SFL2390_3_tau_lock", "SFL2390_5_MHref_link", "VAL2390_OVERALL"],
            "role": "same-frame tau/coframe/M_H_ref anti-circularity guard",
        },
        {
            "source_id": "SRC2597_06_2588_observed_stack",
            "source_path": ROOT / "2588-Y5-R2FR-observed-stack-q-eobs-tau-parent-owner-or-source-leak-fill.md",
            "needles": ["OSA2588_5_tau_identity", "OSC2588_7_MHref", "VAL2588_OVERALL"],
            "role": "observed-stack q/e_obs/tau owner theorem remains conditional",
        },
        {
            "source_id": "SRC2597_07_1519_mhref_schema",
            "source_path": OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
            "needles": ["MHR1519_2_tau", "MHR1519_7_MHref"],
            "role": "strict first-row schema for tau and M_H_ref",
        },
        {
            "source_id": "SRC2597_08_1008_theta_qtau",
            "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "needles": ["PVA1008_1_theta_MTS", "QTA1008_8_Q_total", "CG1008_1_Qtau_total"],
            "role": "theta_MTS/Q_tau extraction remains unsigned",
        },
        {
            "source_id": "SRC2597_09_2596_denominator_rows",
            "source_path": OUT / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
            "needles": ["MHD2596_2_tau", "MHD2596_5_MHref", "MHD2596_TOTAL"],
            "role": "current M_H_ref denominator rows that 2597 attempts to source",
        },
    ]

    rows: list[dict[str, Any]] = []
    for source in source_specs:
        source_path = source["source_path"]
        missing_needles = path_has_needles(source_path, source["needles"])
        rows.append(
            with_stamp(
                {
                    "source_id": source["source_id"],
                    "source_path": source_path,
                    "exists": source_path.exists(),
                    "missing_needles": missing_needles,
                    "source_pass": source_path.exists() and not missing_needles,
                    "role": source["role"],
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def theorem_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "TIA2597_0_parent_tau_definition",
            "clause": "parent-selected tau_obs",
            "required_identity": "tau_obs is selected by the parent q/e_obs branch and boundary/clock normalization before matter/source/readout",
            "conditional_derivation": "if tau_obs is a q-basic vector field on Q_vis, every descended role can compare against the same object",
            "current_status": "MISSING_PARENT_TAU_OBS_DEFINITION",
            "residual_if_missing": "epsilon_tau_selector",
            "blocks": "source;charge;clock;orbit;boundary",
        },
        {
            "audit_id": "TIA2597_1_stationary_generator",
            "clause": "stationary exterior generator",
            "required_identity": "Lie_tau g_obs=0 on the local exterior with fixed boundary normalization",
            "conditional_derivation": "then j_M^mu=T_H^{mu nu} tau_nu is conserved when same-frame Hilbert conservation holds",
            "current_status": "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE",
            "residual_if_missing": "epsilon_stationary_tau",
            "blocks": "mass_current;Hamiltonian_charge",
        },
        {
            "audit_id": "TIA2597_2_q_eobs_basicness",
            "clause": "q/e_obs basicness",
            "required_identity": "tau_obs, e_obs, source support and boundary surfaces descend through the same q/e_obs data",
            "conditional_derivation": "vertical representative changes then cannot alter clock/source/orbit tau roles",
            "current_status": "MISSING_Q_OBS_E_PARENT_OWNER",
            "residual_if_missing": "epsilon_q_owner;epsilon_DObs_e",
            "blocks": "same_frame_readout",
        },
        {
            "audit_id": "TIA2597_3_hamiltonian_charge",
            "clause": "Hamiltonian charge identity",
            "required_identity": "delta H_tau = int_S(delta Q_tau^MTS - i_tau theta_MTS) is integrable for the same tau_obs",
            "conditional_derivation": "then H_tau is a physical charge functional instead of a normalization convention",
            "current_status": "MISSING_THETA_QTAU_TOTAL_AND_INTEGRABILITY",
            "residual_if_missing": "theta_MTS_source;Q_tau_MTS_source;delta_H_tau_curl",
            "blocks": "M_H_ref;PiM_runner",
        },
        {
            "audit_id": "TIA2597_4_clock_normalization",
            "clause": "clock normalization",
            "required_identity": "local clocks read proper time from e_obs and normalize tau_clock=tau_obs, not a separate chi closure time",
            "conditional_derivation": "clock tests then calibrate the same generator used by H_tau rather than only bounding drift",
            "current_status": "CLOCK_PRODUCT_BOUND_ONLY",
            "residual_if_missing": "epsilon_clock_tau",
            "blocks": "clock;redshift;R10_alpha",
        },
        {
            "audit_id": "TIA2597_5_orbit_readout",
            "clause": "slow-orbit readout",
            "required_identity": "orbit equations use g_obs and tau_obs after H_tau has been linked to Poisson/Gauss source, before GM fitting",
            "conditional_derivation": "GM_orbit becomes a derived readout of M_H_ref rather than the denominator input",
            "current_status": "MISSING_POISSON_GAUSS_ORBIT_BRIDGE",
            "residual_if_missing": "epsilon_orbit_tau;Delta_GM_circularity",
            "blocks": "Newton;orbital;PPN",
        },
        {
            "audit_id": "TIA2597_6_boundary_reference",
            "clause": "fixed boundary reference",
            "required_identity": "H_ref and boundary counterterms are fixed once in the same tau_obs branch before source/orbit/clock readout",
            "conditional_derivation": "M_H_ref=H_tau-H_ref is then not a fitted counterterm or lapse rescaling trick",
            "current_status": "MISSING_FIXED_HREF_TAU_REFERENCE",
            "residual_if_missing": "Delta_ref_tau;M_H_ref",
            "blocks": "denominator_positivity",
        },
        {
            "audit_id": "TIA2597_7_surface_support",
            "clause": "surface/support descent",
            "required_identity": "S1/S2/A_ext, source worldtube and annulus are q/e_obs/tau fixed before scoring",
            "conditional_derivation": "equality/commutator residuals cannot be erased by post-readout surface choices",
            "current_status": "MISSING_SURFACE_SUPPORT_DESCENT",
            "residual_if_missing": "surface_homology_lock;alpha_readout_or_Delta_W_support",
            "blocks": "R_eq;I_commutator",
        },
        {
            "audit_id": "TIA2597_8_verdict",
            "clause": "one-tau theorem verdict",
            "required_identity": "TIA2597_0 through TIA2597_7 are all parent-signed in the same q/e_obs branch",
            "conditional_derivation": "only then tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs is claim-grade",
            "current_status": "TAU_IDENTITY_NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "residual_if_missing": "Delta_tau_identity_total",
            "blocks": "M_H_ref;Newton;PPN;local_GR",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "theorem_signed": False,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def role_residual_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "TIR2597_0_source",
            "symbol": "epsilon_tau_source",
            "definition": "projected mismatch between tau used in source/matter variation and parent tau_obs",
            "formula": "||tau_source - tau_obs||_{J_H}/||tau_obs||",
            "units": "dimensionless_projected_norm",
            "current_value": "MISSING_SOURCE_VARIATION_TAU",
            "source_path": OUT / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
            "observable_link": "source_mass;WEP;PiM",
        },
        {
            "row_id": "TIR2597_1_charge",
            "symbol": "epsilon_tau_charge",
            "definition": "projected mismatch between Hamiltonian charge generator and parent tau_obs",
            "formula": "||tau_charge - tau_obs||_{deltaH}/||tau_obs||",
            "units": "dimensionless_projected_norm",
            "current_value": "MISSING_INTEGRABLE_CHARGE_TAU",
            "source_path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "observable_link": "H_tau;M_H_ref;Newton",
        },
        {
            "row_id": "TIR2597_2_clock",
            "symbol": "epsilon_tau_clock",
            "definition": "projected mismatch between clock normalization generator and parent tau_obs",
            "formula": "||tau_clock - tau_obs||_{clock}/||tau_obs||",
            "units": "dimensionless_projected_norm",
            "current_value": "CLOCK_PRODUCT_BOUND_ONLY_NOT_GENERATOR_LOCK",
            "source_path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "observable_link": "clocks;redshift;alpha_EM",
        },
        {
            "row_id": "TIR2597_3_orbit",
            "symbol": "epsilon_tau_orbit",
            "definition": "projected mismatch between slow-orbit readout time and parent tau_obs",
            "formula": "||tau_orbit - tau_obs||_{orbit}/||tau_obs||",
            "units": "dimensionless_projected_norm",
            "current_value": "MISSING_POISSON_GAUSS_ORBIT_BRIDGE",
            "source_path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "observable_link": "orbital_GM;PPN;Newton",
        },
        {
            "row_id": "TIR2597_4_boundary",
            "symbol": "epsilon_tau_boundary",
            "definition": "projected mismatch between boundary/reference tau and parent tau_obs",
            "formula": "||tau_boundary - tau_obs||_{boundary}/||tau_obs||",
            "units": "dimensionless_projected_norm",
            "current_value": "MISSING_FIXED_HREF_TAU_REFERENCE",
            "source_path": OUT / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
            "observable_link": "H_ref;M_H_ref;surface_charge",
        },
        {
            "row_id": "TIR2597_5_frame",
            "symbol": "epsilon_tau_frame",
            "definition": "representative/frame sensitivity of tau_obs under q/e_obs vertical changes",
            "formula": "sup_{v in ker(Dq)} ||Lie_v tau_obs||/||tau_obs||",
            "units": "dimensionless_operator_norm",
            "current_value": "MISSING_Q_OBS_E_TAU_BASICNESS",
            "source_path": OUT / "P8_Y5_OBS_STACK_2588_OWNER_CERTIFICATE.csv",
            "observable_link": "same_frame;clock;source;orbit",
        },
        {
            "row_id": "TIR2597_TOTAL",
            "symbol": "Delta_tau_identity_total",
            "definition": "absolute no-cancellation envelope over source, charge, clock, orbit, boundary and frame tau mismatches",
            "formula": "sum_i |epsilon_tau_i|",
            "units": "dimensionless_envelope_after_MHref_lock",
            "current_value": "COMPONENTS_MISSING",
            "source_path": OUT / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
            "observable_link": "M_H_ref;Newton;PPN;R10;clock;orbital;local_GR",
        },
    ]

    stamped_rows: list[dict[str, Any]] = []
    for row in rows:
        source_path = row["source_path"]
        stamped_rows.append(
            with_stamp(
                {
                    **row,
                    "source_path_exists": source_path.exists(),
                    "score_ready": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        )
    return stamped_rows


def mhref_acquisition_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "MHA2597_0_branch",
            "field": "same_parent_branch_id",
            "required_input": "unique q/e_obs/tau branch ID for the local source/test system",
            "current_value": "MISSING_BRANCH_ID",
            "source_path": OUT / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
            "anti_shortcut": "no anonymous M_H_ref denominator",
        },
        {
            "row_id": "MHA2597_1_tau_obs",
            "field": "tau_obs_definition",
            "required_input": "parent-selected tau_obs(q,e_obs,boundary_clock) before readout",
            "current_value": "MISSING_PARENT_TAU_OBS_DEFINITION",
            "source_path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "anti_shortcut": "no lapse/time-coordinate convention as evidence",
        },
        {
            "row_id": "MHA2597_2_tau_source",
            "field": "tau_source_variation",
            "required_input": "same tau_obs appears in source/matter variation and Hilbert/source current",
            "current_value": "MISSING_SOURCE_VARIATION_TAU",
            "source_path": OUT / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
            "anti_shortcut": "no post-readout source time",
        },
        {
            "row_id": "MHA2597_3_theta_MTS",
            "field": "theta_MTS",
            "required_input": "full parent symplectic potential including EH, boundary, extra, projector and matter/source pieces",
            "current_value": "MISSING_THETA_MTS_SOURCE",
            "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "anti_shortcut": "no EH-only theta import",
        },
        {
            "row_id": "MHA2597_4_Qtau_MTS",
            "field": "Q_tau_MTS",
            "required_input": "total parent Noether/Hamiltonian charge for tau_obs with every retained sector extracted, zeroed or bounded",
            "current_value": "MISSING_Q_TAU_MTS_SOURCE",
            "source_path": OUT / "P8_Y5_R10_1008_CHARGE_DECOMPOSITION_SCHEMA.csv",
            "anti_shortcut": "no reference-only charge",
        },
        {
            "row_id": "MHA2597_5_Htau",
            "field": "H_tau_surface_charge",
            "required_input": "integrable surface Hamiltonian H_tau[S_outer] in same q/e_obs/tau branch",
            "current_value": "MISSING_H_TAU",
            "source_path": OUT / "P8_Y5_PARENT_FRAME_1519_MHREF_FIRST_ROW_SCHEMA.csv",
            "anti_shortcut": "no orbital GM substitution",
        },
        {
            "row_id": "MHA2597_6_Href",
            "field": "H_ref_reference",
            "required_input": "fixed reference/counterterm selected before source/orbit/clock readout",
            "current_value": "MISSING_H_REF",
            "source_path": OUT / "P8_Y5_PARENT_FRAME_1519_DENOMINATOR_ACQUISITION_LEDGER.csv",
            "anti_shortcut": "no fitted counterterm",
        },
        {
            "row_id": "MHA2597_7_MHref",
            "field": "M_H_ref",
            "required_input": "positive finite M_H_ref=H_tau-H_ref with units and uncertainty",
            "current_value": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "source_path": OUT / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
            "anti_shortcut": "no bare mass or reference-one convention",
        },
        {
            "row_id": "MHA2597_8_surfaces",
            "field": "S1_S2_Aext_surface_lock",
            "required_input": "linked S1/S2/A_ext surfaces, homology class, annulus and source-free exterior fixed before scoring",
            "current_value": "MISSING_SURFACE_HOMOLOGY_LOCK",
            "source_path": OUT / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
            "anti_shortcut": "no post-readout mask/surface choice",
        },
        {
            "row_id": "MHA2597_9_orbit_bridge",
            "field": "Poisson_Gauss_orbit_bridge",
            "required_input": "slow-orbit GM readout derived from same H_tau/M_H_ref before fitted orbital GM is used",
            "current_value": "MISSING_POISSON_GAUSS_ORBIT_BRIDGE",
            "source_path": OUT / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
            "anti_shortcut": "orbital GM is output, not input",
        },
        {
            "row_id": "MHA2597_10_acceptance",
            "field": "tau_MHref_acceptance",
            "required_input": "all rows above are source-backed, numeric or theorem-zero, units-compatible and same-branch",
            "current_value": "BLOCKED_NONCLAIM",
            "source_path": OUT / "P8_Y5_MHREF_2596_DENOMINATOR_ROWS.csv",
            "anti_shortcut": "no local-GR/Newton promotion from placeholders",
        },
    ]

    stamped_rows: list[dict[str, Any]] = []
    for row in rows:
        source_path = row["source_path"]
        stamped_rows.append(
            with_stamp(
                {
                    **row,
                    "source_path_exists": source_path.exists(),
                    "units": "source_schema_or_certificate",
                    "score_ready": False,
                    "valid_prediction_row": False,
                    "valid_for_claim": False,
                    "claim_allowed": False,
                }
            )
        )
    return stamped_rows


def runner_refusal_rows(role_rows: list[dict[str, Any]], acquisition_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in role_rows:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"TUR2597_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol_or_field": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_TAU_ROLE_ROW",
                    "failure_reasons": "VALID_FOR_CLAIM_FALSE;MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE;TAU_IDENTITY_NOT_PARENT_SIGNED",
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    for row in acquisition_rows:
        rows.append(
            with_stamp(
                {
                    "runner_id": f"TUR2597_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol_or_field": row["field"],
                    "verdict": "REFUSED_NONCLAIM_MHREF_SOURCE_ROW",
                    "failure_reasons": "VALID_FOR_CLAIM_FALSE;MISSING_SOURCE_BACKED_INPUT;ANTI_CIRCULARITY_GUARD_ACTIVE",
                    "score_ready": False,
                    "claim_allowed": False,
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "CG2597_0_tau_identity_claim",
            "claim": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary is parent-derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "parent tau_obs, q/e_obs basicness, Hamiltonian integrability, clock normalization, orbit bridge and fixed reference are unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2597_1_lapse_shortcut",
            "claim": "choose homogeneous lapse/time coordinate to make tau roles equal",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "time rescaling is gauge until clocks, H_tau and H_ref transform consistently from the parent action",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2597_2_EH_only_charge",
            "claim": "use EH Hamiltonian charge as total MTS H_tau",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "theta_MTS and Q_tau^MTS require EH, boundary, extra, projector and matter/source sectors or signed zero/bounds",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2597_3_orbital_GM_denominator",
            "claim": "use fitted orbital GM as M_H_ref denominator",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "orbital GM is the derived readout target, not a denominator proof input",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2597_4_clock_only_tau",
            "claim": "clock-product tau map alone fixes the Hamiltonian/source generator",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "clock bounds constrain drift but do not by themselves sign source variation, Q_tau or H_ref",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2597_5_fitted_Href",
            "claim": "select H_ref after seeing source/orbit residuals",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "reference subtraction must be fixed before readout or it can absorb the effect being tested",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2597_6_Newton_local_GR",
            "claim": "source-normalized Newton/local GR is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "one-tau/M_H_ref denominator lock is upstream and unclosed",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2597_0_conditional_theorem",
            "decision": "ONE_TAU_THEOREM_CONDITIONAL_ONLY",
            "reason": "the mathematical route is clean if parent q/e_obs, stationary tau, theta/Q_tau, clocks, orbit and boundary reference all descend together",
            "effect": "tau identity is kept as a theorem contract, not discarded",
        },
        {
            "decision_id": "DEC2597_1_no_live_promotion",
            "decision": "TAU_IDENTITY_NOT_PARENT_SIGNED",
            "reason": "current sources do not construct tau_obs or prove it is the same generator for source, charge, clock, orbit and boundary reference",
            "effect": "M_H_ref and source-normalized Newton remain blocked",
        },
        {
            "decision_id": "DEC2597_2_source_rows_staged",
            "decision": "FIRST_TAU_MHREF_SOURCE_ROWS_STAGED_NONCLAIM",
            "reason": "we now have exact fields to fill rather than a vague coupling complaint",
            "effect": "future evidence must fill tau_obs, theta_MTS, Q_tau, H_tau, H_ref, surfaces and orbit bridge explicitly",
        },
        {
            "decision_id": "DEC2597_3_next",
            "decision": "PARENT_STATIONARY_TAU_OR_FIRST_SOURCE_ROWS_SELECTED_NEXT",
            "reason": "the first unsigned clause is tau_obs itself; proving that is cleaner than scoring downstream residuals",
            "effect": "2598 should derive parent stationary tau from q/e_obs/boundary-clock data or acquire first role-specific source rows",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2597_0_selected",
            "selection_status": "selected",
            "target_file": "2598-Y5-R2FR-parent-stationary-tau-generator-or-first-tau-role-source-rows.md",
            "target_script": "scripts/Y5_R2FR_parent_stationary_tau_generator_or_first_tau_role_source_rows_2598.py",
            "task": "derive tau_obs as a parent-selected stationary/boundary-clock generator in the same q/e_obs branch; if that fails, fill first source-backed tau_source, tau_charge, tau_clock, tau_orbit, tau_boundary rows",
            "success_condition": "tau_obs is source-backed enough that tau role residuals can be theorem-zero or numerically bounded",
            "fallback_condition": "nonclaim source rows for each tau role plus H_tau/H_ref/surface acquisition fields",
            "guardrails": "no lapse shortcut; no EH-only H_tau; no orbital GM denominator; no fitted H_ref; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
            "valid_for_claim": False,
        }
    ]
    return [with_stamp(row) for row in rows]


def copy_branch_outputs() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target_path in COPY_TARGETS.items():
        source_path = OUTPUTS[copy_id]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            with_stamp(
                {
                    "copy_id": f"COPY2597_{copy_id}",
                    "source_path": source_path,
                    "target_path": target_path,
                    "source_exists": source_path.exists(),
                    "target_exists": target_path.exists(),
                    "valid_for_claim": False,
                }
            )
        )
    return rows


def generated_rows_have_no_claim_flags(data: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in data.values():
        for row in rows:
            if row.get("valid_for_claim") is True or row.get("claim_allowed") is True:
                return False
            if row.get("theorem_signed") is True or row.get("score_ready") is True:
                return False
    return True


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, condition: bool, notes: str, detail: str = "") -> None:
        rows.append(
            with_stamp(
                {
                    "check_id": check_id,
                    "status": "PASS" if condition else "FAIL",
                    "notes": notes,
                    "detail": detail,
                    "valid_for_claim": False,
                }
            )
        )

    add("VAL2597_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_audit_ids = {f"TIA2597_{idx}_{name}" for idx, name in [(0, "parent_tau_definition"), (1, "stationary_generator"), (2, "q_eobs_basicness"), (3, "hamiltonian_charge"), (4, "clock_normalization"), (5, "orbit_readout"), (6, "boundary_reference"), (7, "surface_support"), (8, "verdict")]}
    present_audit_ids = {row["audit_id"] for row in data["theorem_audit"]}
    add("VAL2597_01_theorem_audit_complete", required_audit_ids.issubset(present_audit_ids), "one-tau theorem audit covers all source/charge/clock/orbit/boundary clauses")
    add(
        "VAL2597_02_theorem_not_promoted",
        any(row["audit_id"] == "TIA2597_8_verdict" and row["current_status"] == "TAU_IDENTITY_NOT_PARENT_SIGNED_CURRENT_CORPUS" for row in data["theorem_audit"])
        and all(row["theorem_signed"] is False for row in data["theorem_audit"]),
        "tau identity remains conditional and nonclaim",
    )
    required_role_symbols = {
        "epsilon_tau_source",
        "epsilon_tau_charge",
        "epsilon_tau_clock",
        "epsilon_tau_orbit",
        "epsilon_tau_boundary",
        "epsilon_tau_frame",
        "Delta_tau_identity_total",
    }
    present_role_symbols = {row["symbol"] for row in data["role_rows"]}
    add("VAL2597_03_role_rows_present", required_role_symbols.issubset(present_role_symbols), "role residual rows cover source, charge, clock, orbit, boundary, frame and total")
    add("VAL2597_04_role_sources_exist", all(row["source_path_exists"] is True for row in data["role_rows"]), "role rows point to existing local sources")
    required_fields = {
        "same_parent_branch_id",
        "tau_obs_definition",
        "tau_source_variation",
        "theta_MTS",
        "Q_tau_MTS",
        "H_tau_surface_charge",
        "H_ref_reference",
        "M_H_ref",
        "S1_S2_Aext_surface_lock",
        "Poisson_Gauss_orbit_bridge",
        "tau_MHref_acceptance",
    }
    present_fields = {row["field"] for row in data["mhref_rows"]}
    add("VAL2597_05_mhref_acquisition_complete", required_fields.issubset(present_fields), "M_H_ref source-acquisition rows cover tau, charge, reference, surfaces and orbit bridge")
    add("VAL2597_06_mhref_sources_exist", all(row["source_path_exists"] is True for row in data["mhref_rows"]), "M_H_ref acquisition rows point to existing local sources")
    add(
        "VAL2597_07_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["role_rows"])
        and all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["mhref_rows"]),
        "all tau/M_H_ref rows remain non-score-ready and nonclaim",
    )
    add("VAL2597_08_runner_refuses", all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "runner refuses every unfilled tau/M_H_ref row")
    add(
        "VAL2597_09_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2597_1_lapse_shortcut" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2597_3_orbital_GM_denominator" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"]),
        "lapse/EH-only/orbital-GM/clock-only/fitted-Href shortcuts and local-GR claims remain blocked",
    )
    add("VAL2597_10_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets valid_for_claim, claim_allowed, theorem_signed, or score_ready true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2597-Y5-R2FR-tau-identity*",
            "*Y5_R2FR_tau_identity*",
            "*P8_Y5_TAU_IDENTITY_2597*",
            "*JR2597*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2597_11_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2597 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add("VAL2597_12_next_selected", any(row["route_id"] == "NEXT2597_0_selected" and "2598-Y5-R2FR-parent-stationary-tau-generator" in row["target_file"] for row in data["next"]), "2598 parent stationary tau/source-row target selected next")
    add("VAL2597_13_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2597_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2597_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2597_OVERALL",
        overall,
        "2597 proves only a conditional one-tau theorem, refuses live promotion, stages tau/M_H_ref source rows, and selects parent stationary tau or first source rows next",
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, separator]
    for row in rows:
        values = [row_value(row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 2597 Y5 R2FR tau identity source charge clock orbit or MHref source acquisition",
        "",
        "**Status:** private nonclaim derivation checkpoint. The one-tau route is mathematically clean as a conditional theorem, but current MTS still does not parent-sign the generator that would make source, Hamiltonian charge, clocks, orbit and boundary reference one object.",
        "",
        "**Main result:** if a parent-selected `tau_obs(q,e_obs)` is stationary, q/e_obs-basic, clock-normalized, Hamiltonian-integrable and fixed at the boundary before readout, then `tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs` follows as a same-branch identity. Current sources do not sign those clauses, so 2597 refuses promotion and stages exact nonclaim source-acquisition rows for the next attack.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## One-Tau Theorem Audit",
        markdown_table(data["theorem_audit"], ["audit_id", "clause", "required_identity", "conditional_derivation", "current_status", "residual_if_missing", "blocks", "theorem_signed", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Tau Role Residual Rows",
        markdown_table(data["role_rows"], ["row_id", "symbol", "definition", "formula", "units", "current_value", "source_path", "source_path_exists", "observable_link", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## MHref Source Acquisition Rows",
        markdown_table(data["mhref_rows"], ["row_id", "field", "required_input", "current_value", "units", "source_path", "source_path_exists", "anti_shortcut", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "symbol_or_field", "verdict", "failure_reasons", "score_ready", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gates",
        markdown_table(data["claim_gates"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "guardrails", "valid_for_claim"]),
        "",
        "## Branch Copies",
        markdown_table(data["copies"], ["copy_id", "source_path", "target_path", "source_exists", "target_exists", "valid_for_claim"]),
        "",
        "## Validation",
        markdown_table(data["validations"], ["check_id", "status", "notes", "detail", "valid_for_claim"]),
        "",
        "## Practical Status",
        "",
        "This is not a dead-end; it is the coupling bottleneck in a sharper suit. The useful result is that the missing object is now very specific: a parent stationary `tau_obs` that the source current, Hamiltonian charge, clocks, orbit and boundary reference all inherit before readout. Without that, `M_H_ref` is still an honest closure/source-acquisition row, not a claim.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    role_rows = role_residual_rows()
    mhref_rows = mhref_acquisition_rows()
    data = {
        "sources": source_register_rows(),
        "theorem_audit": theorem_audit_rows(),
        "role_rows": role_rows,
        "mhref_rows": mhref_rows,
        "runner_refusal": runner_refusal_rows(role_rows, mhref_rows),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["theorem_audit"], data["theorem_audit"])
    write_csv(OUTPUTS["role_residual_rows"], data["role_rows"])
    write_csv(OUTPUTS["mhref_acquisition_rows"], data["mhref_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2597_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
