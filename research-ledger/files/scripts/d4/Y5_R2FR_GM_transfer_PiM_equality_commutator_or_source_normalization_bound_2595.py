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

BRANCH_ID = "MTS_R2FR_GM_TRANSFER_PIM_2595"
CHECKPOINT_ID = "2595"

DOC = ROOT / "2595-Y5-R2FR-GM-transfer-PiM-equality-commutator-or-source-normalization-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_GM_TRANSFER_2595_SOURCE_REGISTER.csv",
    "transfer_gate": OUT / "P8_Y5_GM_TRANSFER_2595_TRANSFER_GATE.csv",
    "component_rows": OUT / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_GM_TRANSFER_2595_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_GM_TRANSFER_2595_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_GM_TRANSFER_2595_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_GM_TRANSFER_2595_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_GM_TRANSFER_2595_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2595_VALIDATION.csv",
}

COPY_TARGETS = {
    "transfer_gate": QUEUE / "JR2595_GM_TRANSFER_PIM_GATE_NONCLAIM.csv",
    "component_rows": LOCAL_BOUNDS / "GM_transfer_PiM_component_rows_2595_NONCLAIM.csv",
    "next_target": QUEUE / "JR2595_MHREF_TAU_FRAME_LOCK_NEXT.csv",
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
            "source_id": "SRC2595_00_2594_handoff",
            "source_path": ROOT / "2594-Y5-R2FR-Y5-source-normalization-even-scalar-theorem-or-coefficient-fill.md",
            "needles": ["NEXT2594_0_selected", "YSN2594_5_GM_transfer", "VAL2594_OVERALL"],
            "role": "active handoff selecting GM-transfer/PiM equality",
        },
        {
            "source_id": "SRC2595_01_2594_next_queue",
            "source_path": QUEUE / "JR2594_GM_TRANSFER_PIM_EQUALITY_NEXT.csv",
            "needles": ["NEXT2594_0_selected", "2595-Y5-R2FR-GM-transfer-PiM-equality-commutator-or-source-normalization-bound.md"],
            "role": "machine-readable 2595 task and guardrails",
        },
        {
            "source_id": "SRC2595_02_1517_runner_doc",
            "source_path": ROOT / "1517-Y5-parent-PiM-equality-commutator-bound-runner-or-worldtube-glue-reentry.md",
            "needles": ["SCHEMA1517_2_R_eq", "SCHEMA1517_8_total", "VAL1517_13_overall"],
            "role": "strict PiM absolute-envelope runner",
        },
        {
            "source_id": "SRC2595_03_1518_commutator_doc",
            "source_path": ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
            "needles": ["COM1518_8_verdict", "ACQ1518_5_total", "VAL1518_13_overall"],
            "role": "commutator zero/source-acquisition audit",
        },
        {
            "source_id": "SRC2595_04_1517_schema",
            "source_path": OUT / "P8_Y5_PARENT_PIM_1517_RUNNER_SCHEMA.csv",
            "needles": ["SCHEMA1517_2_R_eq", "SCHEMA1517_8_total"],
            "role": "machine runner component schema",
        },
        {
            "source_id": "SRC2595_05_1518_acquisition",
            "source_path": OUT / "P8_Y5_PARENT_PIM_1518_SOURCE_ACQUISITION_ROWS.csv",
            "needles": ["ACQ1518_0_R_eq", "ACQ1518_5_total"],
            "role": "R_eq/I_commutator/MHref source acquisition rows",
        },
        {
            "source_id": "SRC2595_06_PiM_contract",
            "source_path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "needles": ["PM5_projector_variation_owned", "PM6_flux_closure_requires_Ward_or_Euler", "PM7_absolute_calibration_deferred"],
            "role": "Pi_M variation, closure and calibration contract",
        },
        {
            "source_id": "SRC2595_07_worldtube_glue",
            "source_path": OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
            "needles": ["W504_2_mass_charge_form", "W504_4_worldtube_source_measure_glue", "W504_5_calibration_and_limits"],
            "role": "worldtube/source-measure glue and weak-field calibration clauses",
        },
        {
            "source_id": "SRC2595_08_1516_gm_gate",
            "source_path": OUT / "P8_Y5_PARENT_CR11_1516_GM_TRANSFER_CHAIN_GATE.csv",
            "needles": ["GM1516_1_pim_equality", "GM1516_6_verdict"],
            "role": "source-normalization GM-transfer chain gate",
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


def transfer_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "GMT2595_0_parent_charge",
            "claim_piece": "parent Hamiltonian/Hilbert source charge",
            "required_identity": "H_xi or B_xi is the same source charge varied by matter in the same e_obs/tau branch",
            "current_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "if_missing": "a conserved charge can be unrelated to measured source mass",
            "residual": "MISSING_PARENT_SOURCE_CHARGE",
        },
        {
            "gate_id": "GMT2595_1_PiM_equality",
            "claim_piece": "Pi_M equality",
            "required_identity": "B_xi/G_eff = M_H[Pi_M J_H] = int_S Q_M[tau] before orbital fitting",
            "current_status": "MISSING_CHARGE_CURRENT_IDENTITY",
            "if_missing": "closed topological/source charge can be the wrong object",
            "residual": "R_eq_integral",
        },
        {
            "gate_id": "GMT2595_2_commutator",
            "claim_piece": "projected product rule",
            "required_identity": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H and [d,Pi_M]J_H=0 on the physical source-current complex",
            "current_status": "PIM_COMMUTATOR_ZERO_NOT_PROVED",
            "if_missing": "projected Hilbert current can leak even if dJ_H is controlled",
            "residual": "I_commutator",
        },
        {
            "gate_id": "GMT2595_3_boundary_flux",
            "claim_piece": "boundary/reference zero flux",
            "required_identity": "dB_zero and fixed reference terms do not shift the compact source mass",
            "current_status": "MISSING_CERTIFICATE_OR_BOUND",
            "if_missing": "source mass can move into exact/reference bookkeeping",
            "residual": "B_zero_flux",
        },
        {
            "gate_id": "GMT2595_4_projector_stress",
            "claim_piece": "projector stress",
            "required_identity": "metric/Hodge/DeWitt dependence of Pi_M carries zero stress or source-backed stress bound",
            "current_status": "MISSING_CERTIFICATE_OR_NUMERIC_BOUND",
            "if_missing": "projector itself can source PPN/source-normalization residues",
            "residual": "epsilon_projector_stress",
        },
        {
            "gate_id": "GMT2595_5_worldtube_glue",
            "claim_piece": "worldtube source-measure glue",
            "required_identity": "M_source[W]=int_S Q_M[tau]=M_eff on linked surfaces before fitting",
            "current_status": "NOT_YET_DERIVED_CORE_MISSING_PIECE",
            "if_missing": "exterior charge can be conserved but not the measured source monopole",
            "residual": "R_worldtube_glue",
        },
        {
            "gate_id": "GMT2595_6_MHref_tau_surface",
            "claim_piece": "positive same-frame denominator and surfaces",
            "required_identity": "M_H_ref, tau, S1/S2, annulus and homology class are parent-owned before readout",
            "current_status": "MISSING_TAU_MHREF_SURFACE_LOCK",
            "if_missing": "R_eq/I_commutator cannot be normalized claim-safely",
            "residual": "M_H_ref;surface_homology_lock;tau_frame_lock",
        },
        {
            "gate_id": "GMT2595_7_no_orbital_shortcut",
            "claim_piece": "no observed-GM shortcut",
            "required_identity": "slow-orbit measured GM is an output of the transfer chain, not the denominator/proof input",
            "current_status": "GUARDRAIL_ACTIVE_NOT_THEOREM",
            "if_missing": "the target observable is smuggled into the derivation",
            "residual": "epsilon_GM_absorption_shortcut",
        },
        {
            "gate_id": "GMT2595_8_total",
            "claim_piece": "GM transfer total",
            "required_identity": "all component rows pass in one same-frame parent branch with an absolute no-cancellation envelope",
            "current_status": "GM_TRANSFER_NOT_DERIVED_CURRENT_CORPUS",
            "if_missing": "Y5 source-normalized Newton remains blocked",
            "residual": "epsilon_PiM_total_abs",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def component_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "GMC2595_0_R_eq",
            "symbol": "R_eq_integral",
            "definition": "integral_S(Pi_M J_H - J_M_top - dB_zero) on same source worldtube/surface",
            "units": "mass_or_charge_units",
            "current_value": "MISSING_R_EQ_INTEGRAL",
            "source_path": ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
            "observable_link": "source_mass;Newton;R11",
        },
        {
            "row_id": "GMC2595_1_I_commutator",
            "symbol": "I_commutator",
            "definition": "integral_A [d,Pi_M]J_H over fixed compact exterior annulus",
            "units": "mass_or_charge_units",
            "current_value": "MISSING_I_COMMUTATOR",
            "source_path": ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
            "observable_link": "radial_Meff;source_normalization;PPN",
        },
        {
            "row_id": "GMC2595_2_B_zero_flux",
            "symbol": "B_zero_flux",
            "definition": "compact boundary/reference exact flux that shifts source mass",
            "units": "mass_or_charge_units",
            "current_value": "MISSING_BOUNDARY_ZERO_FLUX_CERTIFICATE",
            "source_path": ROOT / "1517-Y5-parent-PiM-equality-commutator-bound-runner-or-worldtube-glue-reentry.md",
            "observable_link": "boundary;clock;orbital;PPN",
        },
        {
            "row_id": "GMC2595_3_projector_stress",
            "symbol": "epsilon_projector_stress",
            "definition": "dimensionless stress/source-normalization contribution from metric-dependent Pi_M",
            "units": "dimensionless",
            "current_value": "MISSING_PROJECTOR_STRESS_MAP_OR_THEOREM_ZERO",
            "source_path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
            "observable_link": "PPN;R11;source_mass",
        },
        {
            "row_id": "GMC2595_4_MHref",
            "symbol": "M_H_ref",
            "definition": "positive same-frame Hilbert/Hamiltonian source mass denominator",
            "units": "mass_or_energy_units",
            "current_value": "MISSING_M_H_REF",
            "source_path": ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
            "observable_link": "normalization;Hamiltonian_charge;source_mass",
        },
        {
            "row_id": "GMC2595_5_surfaces",
            "symbol": "surface_homology_lock",
            "definition": "S1/S2/A_ext/r1/r2/worldtube homology class fixed before readout",
            "units": "topological_and_length_metadata",
            "current_value": "MISSING_SURFACE_AND_HOMOLOGY_INPUTS",
            "source_path": ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
            "observable_link": "source_mass;radial_Meff",
        },
        {
            "row_id": "GMC2595_6_tau_frame",
            "symbol": "tau_frame_lock",
            "definition": "same tau/source/charge/readout frame for J_H, Q_M, M_H_ref and orbital readout",
            "units": "certificate",
            "current_value": "MISSING_TAU_FRAME_LOCK",
            "source_path": ROOT / "1518-Y5-parent-PiM-commutator-zero-theorem-or-R_eq-I_commutator-source-acquisition.md",
            "observable_link": "clock;source_mass;orbital",
        },
        {
            "row_id": "GMC2595_TOTAL",
            "symbol": "epsilon_PiM_total_abs",
            "definition": "abs(R_eq)/M_H_ref + abs(I_commutator)/M_H_ref + abs(B_zero_flux)/M_H_ref + abs(epsilon_projector_stress)",
            "units": "dimensionless absolute no-cancellation envelope",
            "current_value": "COMPONENTS_MISSING",
            "source_path": DOC,
            "observable_link": "Y5_source_normalization;Newton;local_GR;PPN;R11",
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


def runner_refusal_rows(component_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in component_data:
        reasons = ["VALID_FOR_CLAIM_FALSE", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE"]
        if not row["source_path_exists"]:
            reasons.append("MISSING_SOURCE_PATH")
        if row["symbol"] == "I_commutator":
            reasons.append("PIM_CHAINMAP_COMMUTATOR_NOT_PROVED")
        if row["symbol"] == "M_H_ref":
            reasons.append("ORBITAL_GM_DENOMINATOR_REJECTED")
        if row["row_id"] == "GMC2595_TOTAL":
            reasons.append("PIM_COMPONENT_ROWS_NOT_SCORE_READY")
        rows.append(
            with_stamp(
                {
                    "runner_id": f"GMR2595_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_GM_TRANSFER_ROW",
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
            "gate_id": "CG2595_0_schema",
            "claim": "GM-transfer/PiM absolute envelope is explicit",
            "gate_status": "PASS_NONCLAIM_STRUCTURE_ONLY",
            "reason": "R_eq, commutator, boundary, projector stress, M_H_ref and surface/tau locks are named",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2595_1_ward_only",
            "claim": "Ward conservation alone proves source mass equality",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "[d,Pi_M]J_H and projector stress remain live",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2595_2_orbital_GM_input",
            "claim": "observed orbital GM can normalize/prove the transfer",
            "gate_status": "REJECTED_SHORTCUT",
            "reason": "orbital GM is the target output, not a proof input",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2595_3_GM_transfer",
            "claim": "parent charge equals measured source mass",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "equality, commutator, boundary, stress, worldtube glue and M_H_ref are not sourced",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2595_4_Newton_local_GR",
            "claim": "source-normalized Newton/local GR is derived",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "GM transfer is upstream of the Y5 source-normalization theorem and remains open",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2595_0_runner_retained",
            "decision": "STRICT_PIM_ABSOLUTE_ENVELOPE_RETAINED",
            "reason": "tuned cancellation between equality, commutator, boundary and projector stress terms would fake source ownership",
            "effect": "future evidence must fill named component rows",
        },
        {
            "decision_id": "DEC2595_1_no_GM_transfer_claim",
            "decision": "GM_TRANSFER_NOT_DERIVED",
            "reason": "Pi_M equality, commutator zero, boundary zero, projector stress zero, worldtube glue and M_H_ref are all unsigned",
            "effect": "Y5 source-normalized Newton remains blocked",
        },
        {
            "decision_id": "DEC2595_2_next",
            "decision": "MHREF_TAU_FRAME_LOCK_SELECTED_NEXT",
            "reason": "without the same-frame positive denominator and surfaces, no R_eq/I_commutator row can become score-ready",
            "effect": "2596 should build the M_H_ref/tau/surface lock or first source-ready denominator rows",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2595_0_selected",
            "selection_status": "selected",
            "target_file": "2596-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row.md",
            "target_script": "scripts/Y5_R2FR_MHref_tau_source_frame_surface_lock_or_first_denominator_row_2596.py",
            "task": "parent-sign one observed coframe and tau/source/charge/readout lock needed for M_H_ref, S1/S2/A_ext surfaces and same-source worldtube; otherwise write first nonclaim denominator/surface rows",
            "success_condition": "M_H_ref, tau frame and linked surfaces become source-backed enough to score R_eq/I_commutator rows",
            "fallback_condition": "first source-ready nonclaim rows for M_H_ref, tau_frame_lock, surface_homology_lock and annulus metadata",
            "guardrails": "no orbital GM denominator; no post-readout surfaces; no Ward-only proof; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
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
                    "copy_id": f"COPY2595_{copy_id}",
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

    add("VAL2595_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_gate_ids = {f"GMT2595_{idx}_{name}" for idx, name in [(0, "parent_charge"), (1, "PiM_equality"), (2, "commutator"), (3, "boundary_flux"), (4, "projector_stress"), (5, "worldtube_glue"), (6, "MHref_tau_surface"), (7, "no_orbital_shortcut"), (8, "total")]}
    present_gate_ids = {row["gate_id"] for row in data["transfer_gate"]}
    add("VAL2595_01_transfer_gate_complete", required_gate_ids.issubset(present_gate_ids), "GM-transfer gate covers all required components")
    required_symbols = {"R_eq_integral", "I_commutator", "B_zero_flux", "epsilon_projector_stress", "M_H_ref", "surface_homology_lock", "tau_frame_lock", "epsilon_PiM_total_abs"}
    present_symbols = {row["symbol"] for row in data["component_rows"]}
    add("VAL2595_02_component_rows_present", required_symbols.issubset(present_symbols), "component rows cover equality, commutator, boundary, stress, denominator, surfaces and total")
    add("VAL2595_03_component_sources_exist", all(row["source_path_exists"] is True for row in data["component_rows"]), "component rows point to existing local sources")
    add("VAL2595_04_rows_nonclaim", all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["component_rows"]), "GM-transfer rows remain non-score-ready and nonclaim")
    add("VAL2595_05_runner_refuses", all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]), "runner refuses all unfilled GM-transfer rows")
    add(
        "VAL2595_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2595_2_orbital_GM_input" and row["gate_status"] == "REJECTED_SHORTCUT" for row in data["claim_gates"]),
        "orbital-GM, Ward-only, Newton and local-GR shortcuts remain blocked",
    )
    add("VAL2595_07_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets valid_for_claim=true or claim_allowed=true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2595-Y5-R2FR-GM-transfer*",
            "*Y5_R2FR_GM_transfer_PiM*",
            "*P8_Y5_GM_TRANSFER_2595*",
            "*JR2595*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2595_08_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2595 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add("VAL2595_09_next_selected", any(row["route_id"] == "NEXT2595_0_selected" and "2596-Y5-R2FR-MHref-tau-source-frame" in row["target_file"] for row in data["next"]), "2596 M_H_ref/tau/source-frame lock selected next")
    add("VAL2595_10_branch_copies", all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]), "nonclaim branch copies exist")

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2595_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2595_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2595_OVERALL",
        overall,
        "2595 refreshes the GM-transfer/PiM equality absolute-envelope runner in the current chain, blocks Ward/orbital-GM shortcuts, keeps rows nonclaim, and selects M_H_ref/tau/surface lock next",
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
        "# 2595 Y5 R2FR GM-transfer PiM equality commutator or source-normalization bound",
        "",
        "**Status:** private nonclaim derivation checkpoint. The GM-transfer/PiM equality runner is refreshed in the current chain, but current MTS still does not prove that the parent charge is the measured source mass.",
        "",
        "**Main result:** source-normalized Newton needs more than a conserved current. It needs the same parent Hamiltonian/Hilbert charge to equal `Pi_M J_H`, worldtube source mass, and slow-orbit measured `GM` before fitting. The live obstruction is the absolute envelope over `R_eq_integral`, `I_commutator`, `B_zero_flux`, `epsilon_projector_stress`, and missing same-frame `M_H_ref`/surface/tau locks. No Newton/local-GR claim is made.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Transfer Gate",
        markdown_table(data["transfer_gate"], ["gate_id", "claim_piece", "required_identity", "current_status", "if_missing", "residual", "valid_for_claim", "claim_allowed"]),
        "",
        "## Component Rows",
        markdown_table(data["component_rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "source_path_exists", "observable_link", "score_ready", "valid_for_claim", "claim_allowed"]),
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
        "This is the right obstruction to have found. If `M_H_ref`, tau, surfaces and source worldtube are not parent-owned, every later coefficient row floats. The next step should not be a bigger claim; it should pin down the denominator and source frame so the equality/commutator rows can eventually be scored.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    component_data = component_rows()
    data = {
        "sources": source_register_rows(),
        "transfer_gate": transfer_gate_rows(),
        "component_rows": component_data,
        "runner_refusal": runner_refusal_rows(component_data),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["transfer_gate"], data["transfer_gate"])
    write_csv(OUTPUTS["component_rows"], data["component_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2595_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
