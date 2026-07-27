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

BRANCH_ID = "MTS_R2FR_Y5_SOURCE_NORMALIZATION_2594"
CHECKPOINT_ID = "2594"

DOC = ROOT / "2594-Y5-R2FR-Y5-source-normalization-even-scalar-theorem-or-coefficient-fill.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_SOURCE_NORM_2594_SOURCE_REGISTER.csv",
    "theorem_stack": OUT / "P8_Y5_SOURCE_NORM_2594_THEOREM_STACK.csv",
    "even_odd_audit": OUT / "P8_Y5_SOURCE_NORM_2594_EVEN_ODD_AUDIT.csv",
    "channel_vector": OUT / "P8_Y5_SOURCE_NORM_2594_CHANNEL_VECTOR.csv",
    "runner_refusal": OUT / "P8_Y5_SOURCE_NORM_2594_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_SOURCE_NORM_2594_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_SOURCE_NORM_2594_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_SOURCE_NORM_2594_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_SOURCE_NORM_2594_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2594_VALIDATION.csv",
}

COPY_TARGETS = {
    "theorem_stack": QUEUE / "JR2594_Y5_SOURCE_NORMALIZATION_THEOREM_STACK_NONCLAIM.csv",
    "channel_vector": LOCAL_BOUNDS / "Y5_source_normalization_channel_vector_2594_NONCLAIM.csv",
    "next_target": QUEUE / "JR2594_GM_TRANSFER_PIM_EQUALITY_NEXT.csv",
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
    if isinstance(value, (list, tuple)):
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
            "source_id": "SRC2594_00_2593_handoff",
            "source_path": ROOT / "2593-Y5-R2FR-extra-response-Qv-zero-odd-source-or-extra-piece-bound.md",
            "needles": ["NEXT2593_0_selected", "ERZ2593_4_zero_odd_source", "VAL2593_OVERALL"],
            "role": "active handoff selecting Y5 source-normalization",
        },
        {
            "source_id": "SRC2594_01_2593_next_queue",
            "source_path": QUEUE / "JR2593_SOURCE_NORMALIZATION_Y5_NEXT.csv",
            "needles": ["NEXT2593_0_selected", "2594-Y5-R2FR-Y5-source-normalization-even-scalar-theorem-or-coefficient-fill.md"],
            "role": "machine-readable 2594 task and guardrails",
        },
        {
            "source_id": "SRC2594_02_495_doc",
            "source_path": ROOT / "495-source-normalization-even-scalar-theorem-or-coefficient-fill.md",
            "needles": ["S5_Newton_gate", "E3_measured_GM_offset", "F0_c_domain_source_normalization_operator"],
            "role": "prior source-normalization theorem stack and coefficient fill gate",
        },
        {
            "source_id": "SRC2594_03_496_doc",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
            "needles": ["R11SN_0_radial_Meff_hair", "R11SN_7_absolute_calibration_offset", "V496_3_channel_coverage"],
            "role": "eight-channel mu_extra/R11 source-normalization vector",
        },
        {
            "source_id": "SRC2594_04_1516_doc",
            "source_path": ROOT / "1516-Y5-parent-cR11-source-normalization-owner-or-GM-transfer-gate.md",
            "needles": ["OWN1516_6_verdict", "GM1516_6_verdict", "REJ1516_0_measured_GM_input"],
            "role": "c_R11 alias lock, source-owner theorem, GM transfer gate",
        },
        {
            "source_id": "SRC2594_05_1516_gm_gate",
            "source_path": OUT / "P8_Y5_PARENT_CR11_1516_GM_TRANSFER_CHAIN_GATE.csv",
            "needles": ["GM1516_1_pim_equality", "GM1516_6_verdict"],
            "role": "machine GM-transfer chain gate rows",
        },
        {
            "source_id": "SRC2594_06_1516_channel_vector",
            "source_path": OUT / "P8_Y5_PARENT_CR11_1516_CHANNEL_VECTOR_LOCK.csv",
            "needles": ["CH1516_2", "CH1516_8_verdict"],
            "role": "machine source-normalization channel vector lock",
        },
        {
            "source_id": "SRC2594_07_494_doc",
            "source_path": ROOT / "494-exchange-doublet-component-map-or-coefficient-branch.md",
            "needles": ["Y5_source_normalization", "G2_source_normalization", "D2_next_priority"],
            "role": "exchange oddness limit for Y5",
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


def theorem_stack_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "YSN2594_0_same_frame",
            "claim_piece": "same observed source frame",
            "required_identity": "matter, clocks, orbital readout, EH operator and source charge use one e_obs/q/tau branch",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "why_needed": "frame/source normalization can otherwise be hidden as a change of units or coframe",
            "residual_if_missing": "Delta_frame_source_over_MH;epsilon_non_EH_branch_mismatch",
        },
        {
            "theorem_id": "YSN2594_1_constant_kappa",
            "claim_piece": "constant universal kappa",
            "required_identity": "G_EH=kappa c^4/(8pi), with partial_t G_EH=partial_r G_EH=partial_A G_EH=0 and no species dependence",
            "current_status": "NOT_PARENT_DERIVED",
            "why_needed": "source-normalized Newton cannot tolerate hidden Gdot, range-dependent G or source species drift",
            "residual_if_missing": "epsilon_time_drift;epsilon_species_A;epsilon_radial_Meff",
        },
        {
            "theorem_id": "YSN2594_2_EH_Gauss_mass",
            "claim_piece": "observed mass is EH/Hilbert Gauss-law source",
            "required_identity": "mu_obs=G_EH M_EH=surface Gauss/ADM/Hamiltonian charge before orbital fitting",
            "current_status": "CONDITIONAL_ONLY",
            "why_needed": "measured orbital GM cannot be used as its own proof",
            "residual_if_missing": "GM1516_1_pim_equality;epsilon_Qv_matter_source_piece",
        },
        {
            "theorem_id": "YSN2594_3_mu_extra_zero",
            "claim_piece": "non-EH source-normalization operators vanish or are bounded",
            "required_identity": "mu_extra=sum_i mu_i is zero by theorem or has source-backed coefficients for every radial/boundary/domain/bulk/operator/species/time/calibration channel",
            "current_status": "EIGHT_CHANNEL_VECTOR_RETAINED_NONCLAIM",
            "why_needed": "even non-EH source offsets are not killed by exchange oddness",
            "residual_if_missing": "c_domain_source_normalization_operator;epsilon_nonEH_source;Delta_mu_extra_total_over_MH",
        },
        {
            "theorem_id": "YSN2594_4_no_absorption_cheat",
            "claim_piece": "no GM absorption shortcut",
            "required_identity": "range/time/species/radial/aniso/source hair cannot be absorbed into fitted measured GM",
            "current_status": "GUARDRAIL_ACTIVE_NOT_A_THEOREM",
            "why_needed": "fitting GM would make the target readout an input",
            "residual_if_missing": "epsilon_calibration;epsilon_radial_Meff;epsilon_time_drift",
        },
        {
            "theorem_id": "YSN2594_5_GM_transfer",
            "claim_piece": "Hamiltonian/Hilbert/worldtube/orbital GM transfer",
            "required_identity": "H_xi or B_xi equals M_H[Pi_M J_H], equals worldtube source mass, and gives slow-orbit mu_obs before fitting",
            "current_status": "GM_TRANSFER_NOT_DERIVED_CURRENT_CORPUS",
            "why_needed": "a conserved charge can be the wrong mass unless Pi_M/worldtube glue closes",
            "residual_if_missing": "R_eq_integral;I_commutator;B_zero_flux;epsilon_PiM_total_abs",
        },
        {
            "theorem_id": "YSN2594_6_PPN_source_stability",
            "claim_piece": "first-order Newton source stable through PPN",
            "required_identity": "source normalization remains stable through beta/gamma/alpha_i/xi/Gdot/R11 order",
            "current_status": "SECOND_ORDER_SOURCE_STABILITY_MISSING",
            "why_needed": "Newton-looking recovery is not local GR until PPN source/operator residues close",
            "residual_if_missing": "LRV_DOMAIN_R11_SOURCE_NORMALIZATION;PPN_source_stability_rows",
        },
        {
            "theorem_id": "YSN2594_7_verdict",
            "claim_piece": "source-normalized Newton/local-GR gate",
            "required_identity": "YSN2594_0 through YSN2594_6 all pass in one parent branch",
            "current_status": "SOURCE_NORMALIZED_NEWTON_NOT_DERIVED_CURRENT_CORPUS",
            "why_needed": "this is the current Y5 blocker inherited by the extra-response zero-odd-source route",
            "residual_if_missing": "Delta_Y5_source_normalization_total_over_MH",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def even_odd_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "EO2594_0_EH_source",
            "quantity": "G_EH M_EH",
            "parity": "even_observed_allowed",
            "status": "ALLOWED_NEEDED_NOT_KILLED",
            "reason": "this is the desired Newtonian source, not a residual to remove",
        },
        {
            "audit_id": "EO2594_1_odd_extra_source",
            "quantity": "mu_extra_odd",
            "parity": "odd",
            "status": "KILLABLE_ONLY_IF_ZERO_ODD_SOURCE_THEOREM_CLOSES",
            "reason": "exchange symmetry helps only after component map and J_Z/B_Z silence are parent-signed",
        },
        {
            "audit_id": "EO2594_2_even_extra_source",
            "quantity": "mu_extra_even",
            "parity": "even",
            "status": "NOT_KILLED_BY_EXCHANGE",
            "reason": "even non-EH source offsets survive Z -> -Z and need independent theorem-zero or coefficients",
        },
        {
            "audit_id": "EO2594_3_measured_GM_offset",
            "quantity": "c_domain_source_normalization_operator",
            "parity": "unknown_even_allowed",
            "status": "RETAINED_HARD_BLOCK",
            "reason": "observed measured GM is naturally exchange-even; oddness-by-naming is forbidden",
        },
        {
            "audit_id": "EO2594_4_verdict",
            "quantity": "Y5_source_normalization",
            "parity": "mixed",
            "status": "EXCHANGE_ODD_INSUFFICIENT",
            "reason": "Y5 can only close through source-owner/GM-transfer theorem or explicit channel coefficients",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def channel_vector_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "YSNC2594_0_radial",
            "channel": "radial_Meff_hair",
            "symbol": "epsilon_radial_Meff",
            "definition": "mu_radial_Meff_hair/(G_EH*M_EH)",
            "current_value": "MISSING_RADIAL_NOHAIR_THEOREM_OR_NUMERIC_PROFILE",
            "units": "dimensionless_or_profile_units_declared",
            "maps_to": "beta;alpha(lambda);R11",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
        },
        {
            "row_id": "YSNC2594_1_boundary",
            "channel": "boundary_monopole_shift",
            "symbol": "epsilon_boundary",
            "definition": "mu_boundary/(G_EH*M_EH)",
            "current_value": "MISSING_BOUNDARY_NOHAIR_THEOREM_OR_NUMERIC_COEFFICIENT",
            "units": "dimensionless",
            "maps_to": "beta;alpha3;xi;Gdot;R11",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
        },
        {
            "row_id": "YSNC2594_2_domain",
            "channel": "domain_projector_mass",
            "symbol": "c_domain_source_normalization_operator",
            "definition": "mu_domain_projector/(G_EH*M_EH)",
            "current_value": "MISSING_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS",
            "units": "dimensionless",
            "maps_to": "alpha1;alpha2;alpha3;xi;R11",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
        },
        {
            "row_id": "YSNC2594_3_bulk",
            "channel": "bulk_X_Yukawa_tail",
            "symbol": "epsilon_bulk_X",
            "definition": "mu_bulk_X/(G_EH*M_EH)",
            "current_value": "MISSING_BULK_MASS_GAP_THEOREM_OR_ALPHA_LAMBDA_CURVE",
            "units": "dimensionless_plus_length_scale",
            "maps_to": "R10;R11;alpha(lambda)",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
        },
        {
            "row_id": "YSNC2594_4_nonEH",
            "channel": "nonEH_operator_potential",
            "symbol": "epsilon_nonEH_source",
            "definition": "mu_nonEH_operator/(G_EH*M_EH)",
            "current_value": "MISSING_EH_ONLY_THEOREM_OR_NONEH_OPERATOR_COEFFICIENT_MAP",
            "units": "dimensionless_or_operator_units_declared",
            "maps_to": "gamma;beta;R10;R11",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
        },
        {
            "row_id": "YSNC2594_5_species",
            "channel": "species_source_charge",
            "symbol": "epsilon_species_A",
            "definition": "Delta_A mu_obs/(G_EH*M_EH)",
            "current_value": "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR",
            "units": "dimensionless_by_species_pair",
            "maps_to": "WEP;clock;R11",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
        },
        {
            "row_id": "YSNC2594_6_time",
            "channel": "time_drift",
            "symbol": "epsilon_time_drift",
            "definition": "mu_time_drift/(G_EH*M_EH)",
            "current_value": "MISSING_STATIONARITY_THEOREM_OR_TIME_DRIFT_COEFFICIENT",
            "units": "dimensionless_or_per_time_with_map",
            "maps_to": "Gdot;R9;R11",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
        },
        {
            "row_id": "YSNC2594_7_calibration",
            "channel": "absolute_calibration_offset",
            "symbol": "epsilon_calibration",
            "definition": "mu_absolute_calibration_offset/(G_EH*M_EH)",
            "current_value": "MISSING_PARENT_FIXED_UNIVERSAL_CALIBRATION_THEOREM_OR_RETAINED_OFFSET",
            "units": "dimensionless",
            "maps_to": "beta;Gdot;R11",
            "source_path": ROOT / "496-R11-source-normalization-operator-vector-minimum-fill.md",
        },
        {
            "row_id": "YSNC2594_TOTAL",
            "channel": "source_normalization_total",
            "symbol": "Delta_Y5_source_normalization_total_over_MH",
            "definition": "absolute sum of all eight mu_extra channels plus GM-transfer/source-owner gaps",
            "current_value": "COMPONENTS_MISSING",
            "units": "dimensionless after M_H_ref",
            "maps_to": "Newton;local_GR;PPN;R11;R10",
            "source_path": DOC,
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "source_path_exists": Path(row["source_path"]).exists() if row["source_path"] != DOC else True,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows(channel_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in channel_rows:
        reasons = ["VALID_FOR_CLAIM_FALSE", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE"]
        if not row["source_path_exists"]:
            reasons.append("MISSING_SOURCE_PATH")
        if row["symbol"] == "c_domain_source_normalization_operator":
            reasons.append("DOMAIN_SOURCE_NORMALIZATION_HARD_BLOCK")
        if row["row_id"] == "YSNC2594_TOTAL":
            reasons.append("SOURCE_NORMALIZATION_CHANNELS_NOT_SCORE_READY")
        rows.append(
            with_stamp(
                {
                    "runner_id": f"YSNR2594_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_SOURCE_NORMALIZATION_ROW",
                    "failure_reasons": reasons,
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
            "gate_id": "CG2594_0_theorem_stack_shape",
            "claim": "source-normalized Newton theorem stack is explicit",
            "gate_status": "PASS_NONCLAIM_STRUCTURE_ONLY",
            "reason": "same-frame, kappa, EH Gauss mass, mu_extra, no-absorption, GM transfer and PPN stability are separated",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2594_1_exchange_odd_kills_Y5",
            "claim": "exchange oddness alone kills source normalization",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "measured GM and even source offsets are exchange-even unless a separate theorem closes",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2594_2_mu_extra_zero",
            "claim": "all non-EH source-normalization channels vanish",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "eight-channel mu_extra vector remains theorem/numeric missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2594_3_GM_transfer",
            "claim": "parent source charge equals orbital measured GM",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "Pi_M equality, commutator silence, worldtube glue and orbital readout are not derived",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2594_4_Newton_local_GR",
            "claim": "source-normalized Newton/local-GR is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "Y5 source normalization and Y6 extra stress remain live",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2594_0_theorem_stack_retained",
            "decision": "SOURCE_NORMALIZATION_THEOREM_STACK_RETAINED",
            "reason": "the right Newton gate is same-frame EH source plus constant kappa plus zero/bounded mu_extra plus GM transfer",
            "effect": "Y5 is a precise derivation target, not a vague complaint",
        },
        {
            "decision_id": "DEC2594_1_no_Newton_claim",
            "decision": "SOURCE_NORMALIZED_NEWTON_NOT_CLAIMED",
            "reason": "mu_extra channels, GM transfer, PPN source stability and same-branch ownership are not closed",
            "effect": "local GR/Newton remains blocked",
        },
        {
            "decision_id": "DEC2594_2_next",
            "decision": "GM_TRANSFER_PIM_EQUALITY_SELECTED_NEXT",
            "reason": "without proving the parent charge equals the Hilbert/projected/worldtube/orbital source mass, coefficient rows cannot become a source-normalized Newton theorem",
            "effect": "2595 should attack Pi_M equality/commutator/worldtube glue or keep R_eq/I_commutator/B_zero_flux rows nonclaim",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2594_0_selected",
            "selection_status": "selected",
            "target_file": "2595-Y5-R2FR-GM-transfer-PiM-equality-commutator-or-source-normalization-bound.md",
            "target_script": "scripts/Y5_R2FR_GM_transfer_PiM_equality_commutator_or_source_normalization_bound_2595.py",
            "task": "prove parent Hamiltonian/Hilbert charge equals Pi_M J_H, worldtube source mass and slow-orbit measured GM before fitting, or fill R_eq_integral, I_commutator, B_zero_flux, projector_stress, M_H_ref and epsilon_PiM_total_abs rows",
            "success_condition": "GM transfer chain no longer blocks Y5 source-normalization theorem stack",
            "fallback_condition": "strict source-ready nonclaim PiM/worldtube/commutator coefficient rows",
            "guardrails": "no observed orbital GM as proof; no Ward-only proof; no fitted GM absorption; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
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
                    "copy_id": f"COPY2594_{copy_id}",
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

    add("VAL2594_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_theorems = {f"YSN2594_{idx}_{suffix}" for idx, suffix in [(0, "same_frame"), (1, "constant_kappa"), (2, "EH_Gauss_mass"), (3, "mu_extra_zero"), (4, "no_absorption_cheat"), (5, "GM_transfer"), (6, "PPN_source_stability"), (7, "verdict")]}
    present_theorems = {row["theorem_id"] for row in data["theorem_stack"]}
    add("VAL2594_01_theorem_stack_complete", required_theorems.issubset(present_theorems), "source-normalization theorem stack covers all required rungs")
    required_channels = {"radial_Meff_hair", "boundary_monopole_shift", "domain_projector_mass", "bulk_X_Yukawa_tail", "nonEH_operator_potential", "species_source_charge", "time_drift", "absolute_calibration_offset", "source_normalization_total"}
    present_channels = {row["channel"] for row in data["channel_vector"]}
    add("VAL2594_02_channel_vector_complete", required_channels.issubset(present_channels), "eight mu_extra channels plus total row are present")
    add("VAL2594_03_channel_sources_exist", all(row["source_path_exists"] is True for row in data["channel_vector"]), "channel rows point to existing local sources")
    add(
        "VAL2594_04_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["channel_vector"]),
        "source-normalization rows remain non-score-ready and nonclaim",
    )
    add(
        "VAL2594_05_even_odd_guard",
        any(row["audit_id"] == "EO2594_4_verdict" and row["status"] == "EXCHANGE_ODD_INSUFFICIENT" for row in data["even_odd_audit"]),
        "exchange oddness is explicitly insufficient for Y5",
    )
    add(
        "VAL2594_06_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses all unfilled source-normalization rows",
    )
    add(
        "VAL2594_07_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2594_1_exchange_odd_kills_Y5" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"]),
        "exchange-odd shortcut, Newton and local-GR claims remain blocked",
    )
    add("VAL2594_08_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets valid_for_claim=true or claim_allowed=true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2594-Y5-R2FR-Y5-source-normalization*",
            "*Y5_R2FR_Y5_source_normalization*",
            "*P8_Y5_SOURCE_NORM_2594*",
            "*JR2594*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2594_09_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2594 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add(
        "VAL2594_10_next_selected",
        any(row["route_id"] == "NEXT2594_0_selected" and "2595-Y5-R2FR-GM-transfer-PiM-equality" in row["target_file"] for row in data["next"]),
        "2595 GM-transfer/PiM equality target selected next",
    )
    add(
        "VAL2594_11_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2594_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2594_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2594_OVERALL",
        overall,
        "2594 refreshes the Y5 source-normalization theorem stack, locks the eight-channel mu_extra vector into the current chain, refuses exchange-odd/GM-fitting shortcuts, and selects GM-transfer/PiM equality next",
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
        "# 2594 Y5 R2FR Y5 source-normalization even-scalar theorem or coefficient fill",
        "",
        "**Status:** private nonclaim derivation checkpoint. The Y5 source-normalization theorem stack is explicit in the current chain, but current MTS has not derived source-normalized Newton or local GR.",
        "",
        "**Main result:** exchange oddness cannot kill measured `GM` by itself because the desired EH/Hilbert source mass is exchange-even, and even non-EH source offsets can also survive. The route is: same frame, constant universal `kappa`, EH/Hilbert Gauss mass, zero or bounded `mu_extra`, no fitted-GM absorption, GM-transfer/PiM/worldtube equality, and PPN source stability. Current MTS fails this full stack, so the eight-channel `mu_extra` vector remains nonclaim.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Theorem Stack",
        markdown_table(data["theorem_stack"], ["theorem_id", "claim_piece", "required_identity", "current_status", "why_needed", "residual_if_missing", "valid_for_claim", "claim_allowed"]),
        "",
        "## Even/Odd Audit",
        markdown_table(data["even_odd_audit"], ["audit_id", "quantity", "parity", "status", "reason", "valid_for_claim", "claim_allowed"]),
        "",
        "## Channel Vector",
        markdown_table(data["channel_vector"], ["row_id", "channel", "symbol", "definition", "current_value", "units", "maps_to", "source_path", "source_path_exists", "score_ready", "valid_for_claim", "claim_allowed"]),
        "",
        "## Runner Refusal",
        markdown_table(data["runner_refusal"], ["runner_id", "target_id", "symbol", "verdict", "failure_reasons", "score_ready", "claim_allowed", "valid_for_claim"]),
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
        "This is the exact place where engineering instincts help: measured `GM` is not a decorative parameter, it is the load path. If the parent charge, projected Hilbert current, worldtube mass and orbital readout are not the same object before fitting, Newton recovery is not derived. The next clean move is therefore the GM-transfer/PiM equality gate.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    channel_rows = channel_vector_rows()
    data = {
        "sources": source_register_rows(),
        "theorem_stack": theorem_stack_rows(),
        "even_odd_audit": even_odd_audit_rows(),
        "channel_vector": channel_rows,
        "runner_refusal": runner_refusal_rows(channel_rows),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["theorem_stack"], data["theorem_stack"])
    write_csv(OUTPUTS["even_odd_audit"], data["even_odd_audit"])
    write_csv(OUTPUTS["channel_vector"], data["channel_vector"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2594_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
