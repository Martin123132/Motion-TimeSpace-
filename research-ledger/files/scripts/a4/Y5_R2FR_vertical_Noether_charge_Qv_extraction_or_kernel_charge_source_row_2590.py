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

BRANCH_ID = "MTS_R2FR_VERTICAL_NOETHER_CHARGE_QV_2590"
CHECKPOINT_ID = "2590"

DOC = ROOT / "2590-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_VERTICAL_QV_2590_SOURCE_REGISTER.csv",
    "extraction_contract": OUT / "P8_Y5_VERTICAL_QV_2590_EXTRACTION_CONTRACT.csv",
    "sector_piece_ledger": OUT / "P8_Y5_VERTICAL_QV_2590_SECTOR_PIECE_LEDGER.csv",
    "kernel_charge_rows": OUT / "P8_Y5_VERTICAL_QV_2590_KERNEL_CHARGE_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_VERTICAL_QV_2590_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_VERTICAL_QV_2590_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_VERTICAL_QV_2590_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_VERTICAL_QV_2590_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_VERTICAL_QV_2590_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2590_VALIDATION.csv",
}

COPY_TARGETS = {
    "extraction_contract": QUEUE / "JR2590_VERTICAL_QV_EXTRACTION_CONTRACT_NONCLAIM.csv",
    "sector_piece_ledger": QUEUE / "JR2590_VERTICAL_QV_SECTOR_PIECE_LEDGER_NONCLAIM.csv",
    "kernel_charge_rows": LOCAL_BOUNDS / "Vertical_Qv_kernel_charge_rows_2590_NONCLAIM.csv",
    "next_target": QUEUE / "JR2590_VERTICAL_SECTOR_VARIATION_LEDGER_NEXT.csv",
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
            "source_id": "SRC2590_00_2589_handoff",
            "source_path": ROOT / "2589-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md",
            "needles": ["NEXT2589_0_selected", "VKC2589_2_theta_Qv", "VAL2589_OVERALL"],
            "role": "active handoff selecting vertical Noether charge extraction",
        },
        {
            "source_id": "SRC2590_01_2589_next_queue",
            "source_path": QUEUE / "JR2589_VERTICAL_NOETHER_CHARGE_QV_NEXT.csv",
            "needles": ["NEXT2589_0_selected", "2590-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md"],
            "role": "machine-readable 2590 task and guardrails",
        },
        {
            "source_id": "SRC2590_02_2393_doc",
            "source_path": ROOT / "2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md",
            "needles": ["VNC2393_0_parent_variation", "VQL2393_0_kernel_charge", "VAL2393_OVERALL"],
            "role": "prior vertical Noether charge contract to refresh into current chain",
        },
        {
            "source_id": "SRC2590_03_2393_theorem_csv",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2393_VERTICAL_NOETHER_CHARGE_THEOREM.csv",
            "needles": ["VNC2393_1_vertical_current", "VNC2393_5_verdict"],
            "role": "formal Q_v theorem rows: current route exact but unclaimed",
        },
        {
            "source_id": "SRC2590_04_2393_kernel_rows",
            "source_path": OUT / "P8_Y5_PARENT_QLOC_2393_KERNEL_CHARGE_SOURCE_ROWS.csv",
            "needles": ["VQL2393_0_kernel_charge", "VQL2393_5_total"],
            "role": "kernel-charge source-row schema inherited from 2393",
        },
        {
            "source_id": "SRC2590_05_1008_theta_qtau",
            "source_path": ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "needles": ["PVA1008_1_theta_MTS", "QTA1008_1_theta_total", "CG1008_0_parent_theta"],
            "role": "parent theta/charge extraction guardrail: theta_MTS not extracted",
        },
        {
            "source_id": "SRC2590_06_1009_sector_contract",
            "source_path": ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needles": ["PCS1009_9_total_parent_contract", "CG1009_1_theta_MTS", "V1009_SUMMARY"],
            "role": "parent sector variation contract: total action not promoted",
        },
        {
            "source_id": "SRC2590_07_noether_chain",
            "source_path": OUT / "P8_PARENT_NOETHER_CLOSURE_DERIVATION_CHAIN.csv",
            "needles": ["D505_0_local_parent_action_form", "D505_2_charge_form", "D505_4_zero_premises"],
            "role": "Noether closure chain showing residual charge pieces must vanish or be bounded",
        },
        {
            "source_id": "SRC2590_08_noether_identity_limit",
            "source_path": OUT / "P8_Y5_R10_824_NOETHER_VARIATION_AUDIT.csv",
            "needles": ["N824_3_Ccoh_multiplier_limit", "N824_4_Bianchi_conservation_gate"],
            "role": "Noether identity warns ownership is not a zero-current theorem",
        },
        {
            "source_id": "SRC2590_09_gauge_identity_attempt",
            "source_path": OUT / "P8_Y5_R10_917_GAUGE_NOETHER_IDENTITY_ATTEMPT.csv",
            "needles": ["NIA917_1_mass_gauge_symmetry", "NIA917_3_Noether_identity_limit"],
            "role": "mass-gauge/source-response Noether route remains parent-unsigned",
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


def extraction_contract_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "contract_id": "VQC2590_0_parent_variation",
            "step": "parent variation identity",
            "required_equation": "delta L_parent = E_A delta Phi^A + dTheta_parent(Phi;delta Phi)",
            "current_status": "MISSING_TOTAL_PARENT_ACTION_AND_THETA",
            "why_it_matters": "without a sourced L_parent and Theta_parent, Q_v is just notation",
            "residual_if_missing": "epsilon_theta_piece_missing;epsilon_kernel_charge",
        },
        {
            "contract_id": "VQC2590_1_vertical_generator",
            "step": "vertical generator action",
            "required_equation": "v_epsilon in ker(Dq), with v_epsilon acting on every parent field and boundary/reference datum",
            "current_status": "MISSING_PARENT_VERTICAL_GENERATOR_ACTION",
            "why_it_matters": "a kernel direction cannot be gauge unless its full field-space action is known",
            "residual_if_missing": "epsilon_q_rank_or_integrability;epsilon_v_action_missing",
        },
        {
            "contract_id": "VQC2590_2_noether_current",
            "step": "vertical Noether current",
            "required_equation": "delta_v L_parent = dmu_v + E_A v^A, J_v = Theta_parent(v_epsilon) - mu_v",
            "current_status": "FORMAL_SHAPE_ONLY",
            "why_it_matters": "J_v is the object that decides whether vertical motion carries Hamiltonian charge",
            "residual_if_missing": "epsilon_mu_v_missing;epsilon_kernel_charge",
        },
        {
            "contract_id": "VQC2590_3_charge_decomposition",
            "step": "charge and constraint split",
            "required_equation": "J_v = dQ_v + C_v, with C_v proportional to parent constraints in the same branch",
            "current_status": "MISSING_VERTICAL_QV_AND_CONSTRAINTS",
            "why_it_matters": "zero charge cannot be claimed from a conservation identity alone",
            "residual_if_missing": "epsilon_Qv_piece_missing;epsilon_Cv_constraint_missing",
        },
        {
            "contract_id": "VQC2590_4_kernel_hamiltonian",
            "step": "kernel Hamiltonian variation",
            "required_equation": "delta H_v[S] = int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece)",
            "current_status": "MISSING_HV_SURFACE_FORM",
            "why_it_matters": "this is the numerator of epsilon_kernel_charge",
            "residual_if_missing": "epsilon_kernel_charge;epsilon_Hv_integrability",
        },
        {
            "contract_id": "VQC2590_5_zero_compact_flux",
            "step": "zero compact local flux",
            "required_equation": "delta H_v[S]=0 for every allowed linked compact local surface S, or source-bound it",
            "current_status": "MISSING_ZERO_FLUX_CERTIFICATE",
            "why_it_matters": "this is the actual local-vacuum/kernel-nullness prize",
            "residual_if_missing": "epsilon_kernel_charge;epsilon_Bv_ambiguity",
        },
        {
            "contract_id": "VQC2590_6_denominator",
            "step": "positive same-frame denominator",
            "required_equation": "M_H_ref = H_tau - H_ref > 0 in the same q/e_obs/tau branch",
            "current_status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "why_it_matters": "finite residual rows cannot be scored without a non-fitted normalization",
            "residual_if_missing": "all normalized Q_v rows remain non-score-ready",
        },
        {
            "contract_id": "VQC2590_7_verdict",
            "step": "current verdict",
            "required_equation": "VQC2590_0 through VQC2590_6 all pass with source paths and parent signatures",
            "current_status": "QV_EXTRACTION_CONTRACT_READY_PARENT_UNSIGNED",
            "why_it_matters": "2590 confirms the correct derivation route but refuses the local-GR shortcut",
            "residual_if_missing": "Delta_vertical_Noether_charge_total_over_MH",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def sector_piece_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "piece_id": "QVP2590_0_EH_reference",
            "sector": "EH/local geometry reference",
            "theta_piece": "Theta_EH[e_obs]",
            "Qv_piece": "Q_v^EH[v;e_obs]",
            "current_status": "REFERENCE_ONLY_NOT_TOTAL_MTS",
            "missing_to_close": "MTS parent reduction and silent-sector certificates before EH can be the only piece",
            "residual_if_missing": "epsilon_Qv_piece_missing",
        },
        {
            "piece_id": "QVP2590_1_boundary_reference",
            "sector": "boundary/reference/improvement",
            "theta_piece": "Theta_boundary + delta B_ref",
            "Qv_piece": "Q_v^boundary + B_v",
            "current_status": "MISSING_FIXED_BEFORE_READOUT_CONVENTION",
            "missing_to_close": "fixed improvement ambiguity, no post-readout counterterm and compact no-flux proof",
            "residual_if_missing": "epsilon_Bv_ambiguity",
        },
        {
            "piece_id": "QVP2590_2_extra_motion_time",
            "sector": "motion/time/domain/memory residual",
            "theta_piece": "Theta_extra[v]",
            "Qv_piece": "Q_v^extra + C_v^extra",
            "current_status": "MISSING_EXTRA_SECTOR_VARIATION",
            "missing_to_close": "local silence/double-zero or finite source-backed extra-sector charge",
            "residual_if_missing": "epsilon_Qv_piece_missing",
        },
        {
            "piece_id": "QVP2590_3_projector_source_measure",
            "sector": "projector/source-measure Pi_M",
            "theta_piece": "Theta_projector[v]",
            "Qv_piece": "Q_v^projector + C_v^projector",
            "current_status": "MISSING_PROJECTOR_SYMPLECTIC_ALGEBRA",
            "missing_to_close": "Pi_M parent variation, chain map, closure and measured-GM calibration",
            "residual_if_missing": "epsilon_Qv_piece_missing;epsilon_Cv_constraint_missing",
        },
        {
            "piece_id": "QVP2590_4_matter_source",
            "sector": "matter/source/worldtube glue",
            "theta_piece": "Theta_matter/source[v]",
            "Qv_piece": "Q_v^matter/source + C_v^matter",
            "current_status": "MISSING_MATTER_SOURCE_GLUE",
            "missing_to_close": "Hilbert current equality, matter descent, worldtube support, no source-prefactor and boundary silence",
            "residual_if_missing": "epsilon_matter_kernel;epsilon_hidden_source_slot",
        },
        {
            "piece_id": "QVP2590_5_constraint_total",
            "sector": "constraint and C_v total",
            "theta_piece": "constraint-proportional pieces",
            "Qv_piece": "C_v = C_EH + C_extra + C_projector + C_matter + C_boundary",
            "current_status": "MISSING_CONSTRAINT_TOTAL_ZERO_OR_BOUND",
            "missing_to_close": "each C_v piece is parent EOM/proper constraint or source-bounded",
            "residual_if_missing": "epsilon_Cv_constraint_missing;epsilon_kernel_charge",
        },
        {
            "piece_id": "QVP2590_6_total",
            "sector": "total vertical Noether charge",
            "theta_piece": "Theta_parent(v)=sum sector Theta_i(v)",
            "Qv_piece": "Q_v=sum sector Q_v^i",
            "current_status": "TOTAL_NOT_PROMOTED",
            "missing_to_close": "all sector pieces above must be theorem-zero, fixed, or finite-sourced in a common branch",
            "residual_if_missing": "Delta_vertical_Noether_charge_total_over_MH",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def kernel_charge_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "VQL2590_0_kernel_charge",
            "symbol": "epsilon_kernel_charge",
            "definition": "abs(int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece))/M_H_ref",
            "units": "dimensionless Hamiltonian charge leakage",
            "current_value": "MISSING_THETA_PARENT;MISSING_Q_V;MISSING_B_V;MISSING_C_V;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "local_GR;Newton;PPN;R10;clock;orbital",
        },
        {
            "row_id": "VQL2590_1_theta_piece",
            "symbol": "epsilon_theta_piece_missing",
            "definition": "abs(int_S i_v(Theta_EH+Theta_matter+Theta_extra+Theta_projector+Theta_boundary)_missing)/M_H_ref",
            "units": "dimensionless symplectic-potential leakage",
            "current_value": "MISSING_SECTOR_THETA_SPLIT;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "H_tau;M_H_ref;local_GR",
        },
        {
            "row_id": "VQL2590_2_Qv_piece",
            "symbol": "epsilon_Qv_piece_missing",
            "definition": "abs(int_S(Q_v_EH+Q_v_matter+Q_v_extra+Q_v_projector+Q_v_boundary)_missing)/M_H_ref",
            "units": "dimensionless vertical charge piece leakage",
            "current_value": "MISSING_QV_SECTOR_LEDGER;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "local_GR;Newton;source_mass",
        },
        {
            "row_id": "VQL2590_3_Bv_ambiguity",
            "symbol": "epsilon_Bv_ambiguity",
            "definition": "abs(int_S delta B_v_unfixed)/M_H_ref",
            "units": "dimensionless boundary-improvement ambiguity",
            "current_value": "MISSING_BV_CONVENTION;MISSING_FIXED_BEFORE_READOUT_CERTIFICATE;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "clock;orbital;PPN;boundary",
        },
        {
            "row_id": "VQL2590_4_Cv_constraint",
            "symbol": "epsilon_Cv_constraint_missing",
            "definition": "abs(int_S C_v_nonconstraint_or_unbounded)/M_H_ref",
            "units": "dimensionless constraint leakage",
            "current_value": "MISSING_PARENT_CONSTRAINT_SPLIT;MISSING_EOM_SOURCE;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "Bianchi;conservation;source_current",
        },
        {
            "row_id": "VQL2590_5_integrability",
            "symbol": "epsilon_Hv_integrability",
            "definition": "curl_fieldspace int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece)/M_H_ref",
            "units": "dimensionless field-space curl",
            "current_value": "MISSING_FIELDSPACE_CURL_TEST;MISSING_SURFACE_CLASS;MISSING_M_H_REF",
            "source_path": "MISSING_SOURCE_PATH",
            "observable_link": "Hamiltonian_integrability;clock;orbital",
        },
        {
            "row_id": "VQL2590_TOTAL",
            "symbol": "Delta_vertical_Noether_charge_total_over_MH",
            "definition": "epsilon_kernel_charge + epsilon_theta_piece_missing + epsilon_Qv_piece_missing + epsilon_Bv_ambiguity + epsilon_Cv_constraint_missing + epsilon_Hv_integrability",
            "units": "dimensionless after M_H_ref",
            "current_value": "COMPONENTS_MISSING",
            "source_path": "THIS_CHECKPOINT_SYMBOLIC_LEDGER_ONLY",
            "observable_link": "q_owner;Newton;local_GR;PPN;R10;clock;orbital",
        },
    ]
    return [
        with_stamp(
            {
                **row,
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
        for row in rows
    ]


def runner_refusal_rows(charge_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in charge_rows:
        failure_reasons = ["VALID_FOR_CLAIM_FALSE", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE"]
        if row_value(row["source_path"]) == "MISSING_SOURCE_PATH":
            failure_reasons.append("MISSING_SOURCE_PATH")
        if row["symbol"] == "epsilon_kernel_charge":
            failure_reasons.append("QV_EXTRACTION_REQUIRED_BEFORE_KERNEL_NULLNESS")
        if row["row_id"] == "VQL2590_TOTAL":
            failure_reasons.append("COMPONENT_ROWS_NOT_SCORE_READY")
        rows.append(
            with_stamp(
                {
                    "runner_id": f"VQR2590_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_QV_RESIDUAL",
                    "failure_reasons": failure_reasons,
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
            "gate_id": "CG2590_0_formal_Qv_contract",
            "claim": "formal vertical Q_v extraction route is written",
            "gate_status": "PASS_NONCLAIM_THEOREM_SHAPE_ONLY",
            "reason": "delta L, J_v, Q_v, C_v, B_v and delta H_v tests are explicit",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2590_1_parent_action_theta",
            "claim": "total L_parent and Theta_parent are extracted",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "1008/1009 still leave total parent current-chain action and sector theta pieces unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2590_2_vertical_Qv",
            "claim": "Q_v is extracted for current MTS",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "vertical generator action, mu_v, Q_v, constraints and sector pieces are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2590_3_zero_kernel_flux",
            "claim": "kernel compact flux is zero",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "B_v convention, surface class, integrability and zero-flux certificate are missing",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2590_4_EH_import",
            "claim": "EH charge alone supplies MTS vertical Q_v",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "EH can only be reference/template until all retained MTS sectors are zero, fixed or bounded",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2590_5_q_obse_local_GR",
            "claim": "q/Obs_e, Newton or local-GR can be promoted from 2590",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "Q_v extraction is upstream and still unclosed; source charge, M_H_ref, EH exterior, Poisson/Gauss, PPN and boundary locks remain open",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2590_0_accept_Qv_contract",
            "decision": "VERTICAL_QV_EXTRACTION_CONTRACT_ACCEPTED",
            "reason": "the right object is a sector-derived Q_v with compact-flux control, not a slogan that the kernel is gauge",
            "effect": "kernel nullness now requires parent variation and sector charge bookkeeping",
        },
        {
            "decision_id": "DEC2590_1_no_Qv_claim",
            "decision": "QV_NOT_EXTRACTED_FOR_CURRENT_MTS",
            "reason": "total parent action, Theta_parent, v action, mu_v, Q_v, C_v, B_v, surface class, integrability and M_H_ref are missing",
            "effect": "epsilon_kernel_charge and Delta_vertical_Noether_charge_total_over_MH remain nonclaim",
        },
        {
            "decision_id": "DEC2590_2_EH_shortcut_refused",
            "decision": "EH_ONLY_CHARGE_IMPORT_REJECTED",
            "reason": "EH charge is a reference anchor only; extra/projector/matter/boundary pieces can carry vertical charge",
            "effect": "no parent q/Obs_e, Newton, local-GR, PPN, clock or orbital claim is reopened",
        },
        {
            "decision_id": "DEC2590_3_next",
            "decision": "VERTICAL_SECTOR_VARIATION_LEDGER_SELECTED_NEXT",
            "reason": "the least-cheatable next step is to split Theta_parent(v), mu_v, Q_v and C_v by sector",
            "effect": "2591 should derive the sector ledger or keep theta/Qv/Cv piece rows nonclaim",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2590_0_selected",
            "selection_status": "selected",
            "target_file": "2591-Y5-R2FR-vertical-sector-variation-ledger-or-Qv-piece-leak-rows.md",
            "target_script": "scripts/Y5_R2FR_vertical_sector_variation_ledger_or_Qv_piece_leak_rows_2591.py",
            "task": "derive sector pieces of Theta_parent(v), mu_v, Q_v and C_v for EH/local geometry, boundary/reference, extra/residual, projector/source-measure, and matter/source sectors",
            "success_condition": "all retained sector pieces are theorem-zero, fixed before readout, constraint-proportional, or source-bounded in one parent branch",
            "fallback_condition": "fill epsilon_theta_piece_missing, epsilon_Qv_piece_missing, epsilon_Cv_constraint_missing and epsilon_Bv_ambiguity with sector source paths and valid_for_claim=false",
            "guardrails": "no EH-only total charge; no post-readout counterterm; no q/Obs_e tautology; no fitted M_H_ref; no local-GR/Newton claim; no GitHub; no formalization-workbench edits",
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
                    "copy_id": f"COPY2590_{copy_id}",
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

    add("VAL2590_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    add(
        "VAL2590_01_parent_variation_present",
        any(row["contract_id"] == "VQC2590_0_parent_variation" and "delta L_parent" in row["required_equation"] for row in data["extraction_contract"]),
        "parent variation identity is recorded",
    )
    add(
        "VAL2590_02_vertical_current_present",
        any(row["contract_id"] == "VQC2590_2_noether_current" and "J_v" in row["required_equation"] for row in data["extraction_contract"]),
        "vertical Noether current formula is recorded",
    )
    add(
        "VAL2590_03_kernel_hamiltonian_present",
        any(row["contract_id"] == "VQC2590_4_kernel_hamiltonian" and "delta H_v" in row["required_equation"] for row in data["extraction_contract"]),
        "kernel Hamiltonian variation test is recorded",
    )
    required_sectors = {"EH/local geometry reference", "boundary/reference/improvement", "motion/time/domain/memory residual", "projector/source-measure Pi_M", "matter/source/worldtube glue", "total vertical Noether charge"}
    present_sectors = {row["sector"] for row in data["sector_piece_ledger"]}
    add("VAL2590_04_sector_ledger_present", required_sectors.issubset(present_sectors), "sector piece ledger covers retained Q_v sectors")
    required_symbols = {
        "epsilon_kernel_charge",
        "epsilon_theta_piece_missing",
        "epsilon_Qv_piece_missing",
        "epsilon_Bv_ambiguity",
        "epsilon_Cv_constraint_missing",
        "epsilon_Hv_integrability",
        "Delta_vertical_Noether_charge_total_over_MH",
    }
    present_symbols = {row["symbol"] for row in data["kernel_charge_rows"]}
    add("VAL2590_05_kernel_charge_rows_present", required_symbols.issubset(present_symbols), "all Q_v kernel-charge rows are present")
    add(
        "VAL2590_06_kernel_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["kernel_charge_rows"]),
        "Q_v charge rows remain non-score-ready and nonclaim",
    )
    add(
        "VAL2590_07_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses all unfilled Q_v residual rows",
    )
    add(
        "VAL2590_08_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2590_4_EH_import" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"]),
        "EH-only shortcut, local-GR and Newton claims remain blocked",
    )
    add("VAL2590_09_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets valid_for_claim=true or claim_allowed=true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2590-Y5-R2FR-vertical-Noether*",
            "*Y5_R2FR_vertical_Noether_charge_Qv*",
            "*P8_Y5_VERTICAL_QV_2590*",
            "*JR2590*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2590_10_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2590 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add(
        "VAL2590_11_next_selected",
        any(row["route_id"] == "NEXT2590_0_selected" and "2591-Y5-R2FR-vertical-sector-variation-ledger" in row["target_file"] for row in data["next"]),
        "2591 vertical sector variation ledger selected next",
    )
    add(
        "VAL2590_12_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2590_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2590_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2590_OVERALL",
        overall,
        "2590 refreshes the vertical Q_v extraction contract in the current chain, refuses EH-only and gauge-by-name shortcuts, keeps Q_v rows nonclaim, and selects a sector variation ledger next",
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
        "# 2590 Y5 R2FR vertical Noether charge Qv extraction or kernel-charge source row",
        "",
        "**Status:** private nonclaim derivation checkpoint. The correct `Q_v` extraction contract is now refreshed in the current 2589->2590 chain, but current MTS still has no parent-signed total action, `Theta_parent`, vertical generator action, `mu_v`, sector `Q_v`, compact flux theorem, or positive same-frame `M_H_ref`.",
        "",
        "**Main result:** the local kernel cannot be called gauge unless a parent variation gives `delta L_parent = E_A delta Phi^A + dTheta_parent`, the vertical current `J_v = Theta_parent(v)-mu_v`, the split `J_v=dQ_v+C_v`, and the local Hamiltonian variation `delta H_v[S]=int_S(delta Q_v - i_v Theta_parent + delta B_v + C_v_piece)`. For current MTS this is an exact extraction route, not a pass. `epsilon_kernel_charge`, sector theta/Qv/Cv rows, boundary ambiguity and integrability remain nonclaim.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Extraction Contract",
        markdown_table(data["extraction_contract"], ["contract_id", "step", "required_equation", "current_status", "why_it_matters", "residual_if_missing", "valid_for_claim", "claim_allowed"]),
        "",
        "## Sector Piece Ledger",
        markdown_table(data["sector_piece_ledger"], ["piece_id", "sector", "theta_piece", "Qv_piece", "current_status", "missing_to_close", "residual_if_missing", "valid_for_claim", "claim_allowed"]),
        "",
        "## Kernel Charge Rows",
        markdown_table(data["kernel_charge_rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "observable_link", "score_ready", "valid_for_claim", "claim_allowed"]),
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
        "This is a useful kind of hard stop. We are not blocked by vibe; we are blocked by a concrete missing object: the sector-derived vertical charge. The next move is therefore not another broad critique, but a ledger of each retained sector's `Theta_parent(v)`, `mu_v`, `Q_v`, and `C_v`. If those pieces vanish or become bounded in one branch, the local-GR path gets sharper. If one survives, it tells us exactly what physical residual the theory must own.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    charge_rows = kernel_charge_rows()
    data = {
        "sources": source_register_rows(),
        "extraction_contract": extraction_contract_rows(),
        "sector_piece_ledger": sector_piece_rows(),
        "kernel_charge_rows": charge_rows,
        "runner_refusal": runner_refusal_rows(charge_rows),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["extraction_contract"], data["extraction_contract"])
    write_csv(OUTPUTS["sector_piece_ledger"], data["sector_piece_ledger"])
    write_csv(OUTPUTS["kernel_charge_rows"], data["kernel_charge_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2590_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
