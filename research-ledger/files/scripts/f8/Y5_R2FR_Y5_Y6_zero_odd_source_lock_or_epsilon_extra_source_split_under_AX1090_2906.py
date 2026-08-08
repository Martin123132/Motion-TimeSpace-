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
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2906-Y5-R2FR-Y5-Y6-zero-odd-source-lock-or-epsilon-extra-source-split-under-AX1090.md"

SRC_2905_DOC = ROOT / "2905-Y5-R2FR-extra-response-operator-source-boundary-signature-or-epsilon-extra-bound-under-AX1090.md"
SRC_2905_NEXT = RESIDUALS / "P8_Y5_R2FR_2905_NEXT_TARGET.csv"
SRC_2905_CERT = RESIDUALS / "P8_Y5_R2FR_2905_EXTRA_RESPONSE_SILENCE_CERTIFICATE.csv"
SRC_2905_PACK = RESIDUALS / "P8_Y5_R2FR_2905_EPSILON_EXTRA_BOUND_PACK.csv"
SRC_494_DOC = ROOT / "494-exchange-doublet-component-map-or-coefficient-branch.md"
SRC_2594_DOC = ROOT / "2594-Y5-R2FR-Y5-source-normalization-even-scalar-theorem-or-coefficient-fill.md"
SRC_2594_STACK = RESIDUALS / "P8_Y5_SOURCE_NORM_2594_THEOREM_STACK.csv"
SRC_2594_VECTOR = RESIDUALS / "P8_Y5_SOURCE_NORM_2594_CHANNEL_VECTOR.csv"
SRC_2595_DOC = ROOT / "2595-Y5-R2FR-GM-transfer-PiM-equality-commutator-or-source-normalization-bound.md"
SRC_2595_GATE = RESIDUALS / "P8_Y5_GM_TRANSFER_2595_TRANSFER_GATE.csv"
SRC_2595_COMPONENTS = RESIDUALS / "P8_Y5_GM_TRANSFER_2595_COMPONENT_ROWS.csv"
SRC_2593_AUDIT = RESIDUALS / "P8_Y5_EXTRA_RESPONSE_QV_2593_ZERO_ODD_SOURCE_AUDIT.csv"
SRC_2593_BOUNDS = RESIDUALS / "P8_Y5_EXTRA_RESPONSE_QV_2593_BOUND_ROWS.csv"
SRC_RESPONSE_DOUBLET = RESIDUALS / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv"
SRC_PIM_CONTRACT = RESIDUALS / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"
SRC_WORLDTUBE_GLUE = RESIDUALS / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2906_SOURCE_REGISTER.csv",
    "lock": RESIDUALS / "P8_Y5_R2FR_2906_Y5_Y6_ZERO_ODD_SOURCE_LOCK_AUDIT.csv",
    "split": RESIDUALS / "P8_Y5_R2FR_2906_EPSILON_EXTRA_SOURCE_SPLIT.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2906_RUNNER_STATUS.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2906_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2906_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2906_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2906_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2906_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "lock_copy": RAB_QUEUE / "JR2906_Y5_Y6_ZERO_ODD_SOURCE_LOCK_AUDIT_NONCLAIM.csv",
    "split_copy": LOCAL_BOUNDS / "Extra_response_Y5_Y6_source_split_2906_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2906_MHREF_TAU_SOURCE_FRAME_SURFACE_LOCK_NEXT.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
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


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2906_00_2905_doc", SRC_2905_DOC, "Y5 source normalization and Y6 extra stress are the source channels;NEXT2905_0_2906", "current-chain handoff selecting Y5/Y6 source lock"),
        ("SRC2906_01_2905_next", SRC_2905_NEXT, "NEXT2905_0_2906;try to prove Y5 source-normalization and Y6 extra-stress", "machine-readable 2906 target"),
        ("SRC2906_02_2905_cert", SRC_2905_CERT, "XRS2905_4_zero_odd_source_Y5;XRS2905_5_zero_odd_source_Y6", "current extra-response certificate with Y5/Y6 blockers"),
        ("SRC2906_03_2905_pack", SRC_2905_PACK, "XRB2905_4_Y5_source;XRB2905_5_Y6_stress", "current epsilon-extra bound pack"),
        ("SRC2906_04_494_doc", SRC_494_DOC, "Y5 source normalization and Y6 extra stress remain hard blockers;Y6_stress_Bianchi", "exchange-doublet component map"),
        ("SRC2906_05_2594_doc", SRC_2594_DOC, "exchange oddness cannot kill measured `GM`;eight-channel `mu_extra` vector remains nonclaim", "Y5 source-normalization theorem stack"),
        ("SRC2906_06_2594_stack", SRC_2594_STACK, "YSN2594_3_mu_extra_zero;YSN2594_7_verdict", "machine source-normalization theorem stack"),
        ("SRC2906_07_2594_vector", SRC_2594_VECTOR, "YSNC2594_4_nonEH;YSNC2594_TOTAL", "machine Y5 mu_extra channel vector"),
        ("SRC2906_08_2595_doc", SRC_2595_DOC, "source-normalized Newton needs more than a conserved current;M_H_ref", "GM-transfer/PiM equality checkpoint"),
        ("SRC2906_09_2595_gate", SRC_2595_GATE, "GMT2595_5_worldtube_glue;GMT2595_8_total", "machine GM-transfer gate"),
        ("SRC2906_10_2595_components", SRC_2595_COMPONENTS, "GMC2595_4_MHref;GMC2595_TOTAL", "machine GM-transfer component rows"),
        ("SRC2906_11_2593_audit", SRC_2593_AUDIT, "ERZ2593_4_zero_odd_source;ERZ2593_7_verdict", "prior zero-odd-source audit"),
        ("SRC2906_12_2593_bounds", SRC_2593_BOUNDS, "ERB2593_4_zero_odd_source;ERB2593_TOTAL", "prior extra-response source/bound rows"),
        ("SRC2906_13_response_contract", SRC_RESPONSE_DOUBLET, "RD516_4_zero_odd_source;RD516_5_PPN_lock", "response-doublet source and PPN lock contract"),
        ("SRC2906_14_PiM_contract", SRC_PIM_CONTRACT, "PM4_projector_algebra;conditional", "Pi_M projector/source-measure contract"),
        ("SRC2906_15_worldtube_glue", SRC_WORLDTUBE_GLUE, "W504_4_worldtube_source_measure_glue;not_yet_derived_core_missing_piece", "worldtube/source-measure glue gap"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        anchors_found, missing_anchors = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": anchors_found,
                    "missing_anchors": missing_anchors,
                }
            )
        )
    return rows


def lock_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "LOCK2906_0_Y5_EH_source",
            "Y5 desired EH/Hilbert source",
            "Measured source mass is an even EH/Hilbert/Gauss charge in the same q/e_obs/tau branch, not an odd residual to kill.",
            "CONDITIONAL_ONLY",
            "This part should survive; the problem is proving it is the same parent charge as source, worldtube and orbital readout before fitting.",
            "MISSING_GM_TRANSFER_AND_MHREF_LOCK",
            SRC_2594_STACK,
        ),
        (
            "LOCK2906_1_Y5_nonEH_mu_extra",
            "Y5 non-EH source offsets",
            "All non-EH source-normalization channels mu_extra are zero, odd-local-zero, or source-bounded in one branch.",
            "NOT_DERIVED",
            "Exchange oddness cannot remove even non-EH offsets; eight mu_extra channels remain unfilled.",
            "MISSING_MU_EXTRA_ZERO_OR_COEFFICIENTS",
            SRC_2594_VECTOR,
        ),
        (
            "LOCK2906_2_Y5_no_absorption",
            "no fitted-GM absorption",
            "Measured orbital GM is an output of the parent source transfer chain, never a denominator or proof input.",
            "GUARDRAIL_ACTIVE_NOT_THEOREM",
            "Fitting away mu_extra would fake Newton recovery.",
            "MISSING_NO_ABSORPTION_THEOREM_AS_BRANCH_SIGNATURE",
            SRC_2595_GATE,
        ),
        (
            "LOCK2906_3_Y5_PiM_worldtube",
            "PiM/worldtube transfer",
            "Parent Hamiltonian/Hilbert charge equals Pi_M J_H, worldtube source mass and slow-orbit measured GM before fitting.",
            "GM_TRANSFER_NOT_DERIVED",
            "A conserved current can be the wrong mass if Pi_M commutator, boundary flux or worldtube glue survives.",
            "R_eq_integral;I_commutator;B_zero_flux;epsilon_PiM_total_abs",
            SRC_2595_COMPONENTS,
        ),
        (
            "LOCK2906_4_Y6_stress_parity",
            "Y6 extra-stress parity",
            "Every extra-stress channel is exchange-odd and locally zero at Z=0, or else explicitly excluded from observed local stress by q-basic descent.",
            "RETAINED_DEBT",
            "The current component map permits conserved exchange-even extra stress.",
            "MISSING_Y6_STRESS_PARITY_THEOREM",
            SRC_494_DOC,
        ),
        (
            "LOCK2906_5_Y6_constraint_or_topological",
            "Y6 constraint/topological silence",
            "Extra stress is constraint-proportional, topological, pure boundary with zero compact flux, or source-bounded in the same local branch.",
            "NOT_DERIVED",
            "Bianchi/Noether ownership alone does not make stress vanish.",
            "MISSING_TEXTRA_CONSTRAINT_OR_TOPOLOGICAL_CERTIFICATE",
            SRC_494_DOC,
        ),
        (
            "LOCK2906_6_Y6_projector_stress",
            "Y6 projector/source-measure stress",
            "Metric/Hodge/DeWitt dependence of Pi_M carries zero stress or a source-backed bound compatible with PPN.",
            "MISSING_CERTIFICATE_OR_NUMERIC_BOUND",
            "Projector stress can re-enter source normalization and PPN even when ordinary stress is controlled.",
            "epsilon_projector_stress",
            SRC_PIM_CONTRACT,
        ),
        (
            "LOCK2906_7_same_branch",
            "same branch source lock",
            "Y5 and Y6 clauses hold simultaneously with the extra-response doublet, non-EH silence gate, M_ref, tau and linked surfaces.",
            "MISSING_SAME_BRANCH_CERTIFICATE",
            "Y5 and Y6 cannot be closed in separate branches and then combined rhetorically.",
            "epsilon_extra_source_branch_mismatch",
            SRC_2905_DOC,
        ),
        (
            "LOCK2906_8_verdict",
            "Y5/Y6 zero-odd-source lock",
            "LOCK2906_0 through LOCK2906_7 pass; then epsilon_extra_odd_source_Y5 and epsilon_extra_odd_source_Y6 may be theorem-zero.",
            "Y5_Y6_ZERO_ODD_SOURCE_LOCK_NOT_PROVED_CURRENT_CORPUS",
            "The theorem route remains open, but current MTS must carry Y5 and Y6 as explicit nonclaim source rows.",
            "epsilon_extra_odd_source_Y5;epsilon_extra_odd_source_Y6",
            SRC_2905_CERT,
        ),
    ]
    return [
        add_common(
            {
                "lock_id": lock_id,
                "clause": clause,
                "required_signature": required_signature,
                "current_status": current_status,
                "reason": reason,
                "residual_if_missing": residual_if_missing,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "same_branch_certified": False,
                "accepted_for_local_gr": False,
            }
        )
        for lock_id, clause, required_signature, current_status, reason, residual_if_missing, source_path in specs
    ]


def split_rows() -> list[dict[str, Any]]:
    specs = [
        ("SPL2906_0_Y5_GM_transfer", "epsilon_Y5_GM_transfer", "failure of parent Hamiltonian/Hilbert charge to equal Pi_M J_H, worldtube source mass and slow-orbit GM before fitting", "dimensionless after M_ref", "MISSING_R_EQ_I_COMMUTATOR_B_ZERO_PIM_WORLD_TUBE_MHREF", SRC_2595_COMPONENTS, "Newton;source_mass;PPN;R11"),
        ("SPL2906_1_Y5_mu_extra", "epsilon_Y5_mu_extra_vector", "absolute source-normalization leakage from radial, boundary, domain, bulk, nonEH, species, time and calibration channels", "dimensionless after M_ref", "EIGHT_CHANNEL_MU_EXTRA_VECTOR_UNFILLED", SRC_2594_VECTOR, "Newton;local_GR;PPN;R10;R11;WEP"),
        ("SPL2906_2_Y5_absorption_guard", "epsilon_Y5_GM_absorption_shortcut", "1 if observed/fitted orbital GM is used as denominator/proof input for source normalization else 0", "boolean guard", "ORBITAL_GM_DENOMINATOR_REJECTED_GUARD_ACTIVE", SRC_2595_GATE, "Newton;orbital;local_GR"),
        ("SPL2906_3_Y5_total", "epsilon_extra_odd_source_Y5", "absolute no-cancellation envelope for Y5 source-normalization contribution to extra-response odd source", "dimensionless after M_ref", "COMPONENTS_MISSING", SRC_2905_PACK, "Newton;source_mass;PPN;R11"),
        ("SPL2906_4_Y6_parity", "epsilon_Y6_stress_parity", "extra stress not proven exchange-odd/local-zero or q-basic invisible", "dimensionless stress leakage", "MISSING_Y6_STRESS_PARITY_THEOREM", SRC_494_DOC, "Bianchi;PPN;local_GR"),
        ("SPL2906_5_Y6_constraint", "epsilon_Y6_constraint_topological", "extra stress not proven constraint-proportional, topological, or compact-boundary silent", "dimensionless stress leakage", "MISSING_TEXTRA_CONSTRAINT_TOPOLOGICAL_CERTIFICATE", SRC_494_DOC, "Bianchi;conservation;local_GR"),
        ("SPL2906_6_Y6_projector", "epsilon_Y6_projector_stress", "projector/source-measure stress not proven zero or source-backed bounded", "dimensionless stress/source leakage", "MISSING_PROJECTOR_STRESS_MAP_OR_THEOREM_ZERO", SRC_PIM_CONTRACT, "PPN;source_mass;R11"),
        ("SPL2906_7_Y6_total", "epsilon_extra_odd_source_Y6", "absolute no-cancellation envelope for Y6 extra-stress contribution to extra-response odd source", "dimensionless after M_ref", "COMPONENTS_MISSING", SRC_2905_PACK, "PPN;local_GR;Bianchi"),
        ("SPL2906_8_source_branch", "epsilon_extra_source_branch_mismatch", "1 if Y5/Y6 source-lock clauses require a branch different from the extra-response/non-EH silence branch else 0", "boolean branch guard", "MISSING_SAME_BRANCH_COMPATIBILITY_PROOF", SRC_2905_CERT, "q_owner;same_frame;local_GR"),
        ("SPL2906_TOTAL", "epsilon_extra_odd_source_Y5Y6_total", "epsilon_extra_odd_source_Y5 + epsilon_extra_odd_source_Y6 + epsilon_extra_source_branch_mismatch as an absolute no-cancellation source envelope", "dimensionless after M_ref", "COMPONENTS_MISSING", SRC_2905_PACK, "PPN;R10;clock;orbital;local_GR"),
    ]
    return [
        add_common(
            {
                "row_id": row_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "current_value": current_value,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "observable_link": observable_link,
                "parent_signed": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for row_id, symbol, definition, units, current_value, source_path, observable_link in specs
    ]


def runner_rows() -> list[dict[str, Any]]:
    specs = [
        ("RUN2906_0_zero_lock_claim", "REFUSED_UNSIGNED_Y5_Y6_LOCK", "Y5 EH source; Y5 mu_extra; no GM absorption; PiM/worldtube transfer; Y6 stress parity; Y6 constraint/topological silence; Y6 projector stress; same branch", 0, "Y5/Y6 clauses remain unsigned"),
        ("RUN2906_1_split_rows", "STAGED_NONCLAIM_SOURCE_SPLIT", "epsilon_Y5_GM_transfer;epsilon_Y5_mu_extra_vector;epsilon_Y5_GM_absorption_shortcut;epsilon_extra_odd_source_Y5;epsilon_Y6_stress_parity;epsilon_Y6_constraint_topological;epsilon_Y6_projector_stress;epsilon_extra_odd_source_Y6", 0, "split rows are explicit but unfilled"),
        ("RUN2906_2_next_denominator", "NEXT_TARGET_SELECTED", "M_H_ref/tau/source-frame/surface lock", 0, "without denominator and same-frame surfaces the Y5/Y6 rows cannot become score-ready"),
    ]
    return [
        add_common(
            {
                "runner_id": runner_id,
                "status": status,
                "required_components": required_components,
                "components_evaluable": components_evaluable,
                "reason": reason,
                "runner_ready": False,
            }
        )
        for runner_id, status, required_components, components_evaluable, reason in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2906_0_lock_shape", "Y5/Y6 zero-odd-source lock is explicit", "PASS_NONCLAIM_STRUCTURE_ONLY", "Y5 source normalization and Y6 stress clauses are separated", True),
        ("CG2906_1_Y5_zero", "Y5 source-normalization does not source the extra mode", "BLOCKED_NONCLAIM", "GM transfer, mu_extra zero/bounds, no-absorption and M_ref/surface locks are missing", False),
        ("CG2906_2_Y6_zero", "Y6 extra stress does not source the extra mode", "BLOCKED_NONCLAIM", "stress parity, topological/constraint silence and projector stress are unsigned", False),
        ("CG2906_3_exchange_odd_shortcut", "exchange oddness alone kills Y5/Y6", "REJECTED_SHORTCUT", "measured GM is exchange-even and conserved extra stress can survive", False),
        ("CG2906_4_score_ready", "Y5/Y6 source split is score-ready", "BLOCKED_NONCLAIM", "numeric values, M_ref, arena projections and source-backed coefficients are missing", False),
        ("CG2906_5_local_GR_Newton", "local GR/Newton follows after 2906", "BLOCKED_NONCLAIM", "2906 splits the source residual; it does not close it", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_status": gate_status,
                "reason": reason,
                "gate_pass": gate_pass,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, claim, gate_status, reason, gate_pass in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2906_0_lock_attempt", "Y5_Y6_ZERO_ODD_SOURCE_LOCK_NOT_PROMOTED", "Y5 measured-GM/source normalization and Y6 extra stress both retain legal source paths into the extra response", "keep theorem route open but carry split residual rows"),
        ("DEC2906_1_split_accepted", "EPSILON_EXTRA_SOURCE_SPLIT_ACCEPTED", "Y5 and Y6 are different physical wounds and should not be hidden inside one opaque epsilon", "future tests can bound the two source channels separately"),
        ("DEC2906_2_next", "MHREF_TAU_SOURCE_FRAME_SURFACE_LOCK_SELECTED_NEXT", "without positive same-frame M_ref, tau and linked surfaces, neither Y5 nor Y6 split rows can be scored honestly", "2907 should pin denominator/frame/surface data or keep denominator rows nonclaim"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "reason": reason,
                "effect": effect,
            }
        )
        for decision_id, decision, reason, effect in specs
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "route_id": "NEXT2906_0_2907",
                "selection_status": "selected_primary",
                "target_file": "2907-Y5-R2FR-MHref-tau-source-frame-surface-lock-or-first-denominator-row-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_MHref_tau_source_frame_surface_lock_or_first_denominator_row_under_AX1090_2907.py",
                "task": "parent-sign one observed coframe/tau/source/charge/readout lock for M_ref and linked surfaces, or write first source-ready denominator and surface rows without using observed orbital GM as proof",
                "success_condition": "M_ref, tau_frame_lock and surface_homology_lock become parent-owned enough to score Y5/Y6 and PiM/worldtube rows",
                "fallback_condition": "nonclaim rows for M_ref, tau_frame_lock, surface_homology_lock, annulus metadata and denominator provenance with valid_for_claim=false",
                "guardrails": "no orbital GM denominator; no post-readout surfaces; no Ward-only proof; no fitted GM absorption; no Newton/local-GR claim; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    specs = [
        ("BR2906_0_lock_copy", OUTPUTS["lock"], BRANCH_OUTPUTS["lock_copy"], "RAB queue copy of Y5/Y6 zero-odd-source lock audit"),
        ("BR2906_1_split_copy", OUTPUTS["split"], BRANCH_OUTPUTS["split_copy"], "local-bounds copy of Y5/Y6 epsilon-extra source split"),
        ("BR2906_2_next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"], "RAB queue copy of 2907 MHref/tau/source-frame target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in specs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def formalization_touched() -> bool:
    if not FORMALIZATION.exists():
        return False
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for candidate in FORMALIZATION.rglob("*"):
        try:
            if candidate.is_file() and candidate.stat().st_mtime >= start_timestamp:
                return True
        except OSError:
            return True
    return False


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    lock_rows_data = all_rows["lock"]
    split_rows_data = all_rows["split"]
    runner_rows_data = all_rows["runner"]
    claim_rows_data = all_rows["claims"]
    next_rows_data = all_rows["next"]
    branch_rows_data = all_rows["branches"]
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    required_symbols = {
        "epsilon_Y5_GM_transfer",
        "epsilon_Y5_mu_extra_vector",
        "epsilon_Y5_GM_absorption_shortcut",
        "epsilon_extra_odd_source_Y5",
        "epsilon_Y6_stress_parity",
        "epsilon_Y6_constraint_topological",
        "epsilon_Y6_projector_stress",
        "epsilon_extra_odd_source_Y6",
        "epsilon_extra_source_branch_mismatch",
        "epsilon_extra_odd_source_Y5Y6_total",
    }
    found_symbols = {row["symbol"] for row in split_rows_data}
    checks = [
        ("VAL2906_0_sources_exist", all(row["path_exists"] for row in source_rows), "all registered source paths exist"),
        ("VAL2906_1_source_anchors", all(row["anchors_found"] for row in source_rows), "all registered source anchors were found"),
        ("VAL2906_2_lock_audit_complete", len(lock_rows_data) == 9 and any(row["lock_id"] == "LOCK2906_8_verdict" for row in lock_rows_data), "Y5/Y6 lock audit has all clauses"),
        ("VAL2906_3_lock_nonclaim", all(not row["theorem_zero_adopted"] and not row["accepted_for_local_gr"] for row in lock_rows_data), "Y5/Y6 lock rows remain unsigned nonclaim"),
        ("VAL2906_4_split_symbols_present", required_symbols <= found_symbols, "Y5/Y6 source split symbols are present"),
        ("VAL2906_5_split_paths_exist", all(row["source_path_exists"] for row in split_rows_data), "split rows point to existing local sources"),
        ("VAL2906_6_rows_nonclaim", all(not row["valid_for_claim"] and not row["accepted_for_scoring"] for row in split_rows_data), "split rows remain non-score-ready and nonclaim"),
        ("VAL2906_7_runner_refuses", any(row["runner_id"] == "RUN2906_0_zero_lock_claim" and row["status"] == "REFUSED_UNSIGNED_Y5_Y6_LOCK" for row in runner_rows_data), "runner refuses unsigned Y5/Y6 zero-lock claim"),
        ("VAL2906_8_claim_gates_safe", all(not row["claim_allowed"] for row in claim_rows_data) and any(row["gate_id"] == "CG2906_5_local_GR_Newton" and row["gate_status"] == "BLOCKED_NONCLAIM" for row in claim_rows_data), "local-GR/Newton claims remain blocked"),
        ("VAL2906_9_next_target_2907", any(row["route_id"] == "NEXT2906_0_2907" and row["selected"] for row in next_rows_data), "2907 MHref/tau/source-frame target selected"),
        ("VAL2906_10_branch_copies_exist", all(row["exists"] for row in branch_rows_data), "branch copies were written"),
        ("VAL2906_11_csv_outputs_parse", all(csv_parses(path) for path in csv_outputs), "all generated CSV outputs parse cleanly"),
        ("VAL2906_12_formalization_untouched_during_run", not formalization_touched(), "formalization-workbench was not touched during this run"),
    ]
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL2906_OVERALL", overall, "2906 validation overall"))
    return [
        {
            "check_id": check_id,
            "passed": passed,
            "detail": detail,
            "generated_utc": now(),
        }
        for check_id, passed, detail in checks
    ]


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 2906 - Y5 R2FR Y5/Y6 Zero-Odd-Source Lock or Epsilon Extra Source Split Under AX1090",
        "",
        f"Run: `runs/{SCRIPT_START_UTC.strftime('%Y%m%d-%H%M%S')}-Y5-R2FR-Y5-Y6-zero-odd-source-lock-or-epsilon-extra-source-split-under-AX1090`",
        "Status: `Y5_R2FR_2906_Y5_Y6_zero_odd_source_lock_not_proved_source_split_accepted_2907_next`",
        "Claim ceiling: `Y5_Y6_source_split_nonclaim_only_no_extra_Qv_zero_no_source_normalized_Newton_no_PPN_no_R10_no_local_GR_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2906 tries the direct Y5/Y6 zero-odd-source lock. It does not close in the current corpus.",
        "",
        "The result is useful rather than grim: Y5 and Y6 are now separated into different live residuals. Y5 is the measured-GM/source-normalization load path; Y6 is conserved extra stress. Exchange oddness alone cannot erase either one.",
        "",
        "So `epsilon_Qv_extra_piece` is no longer a foggy bucket. Its source part now has explicit Y5 and Y6 rows that must be theorem-zero, source-bounded, or kept as local residuals before local-GR/Newton can reopen.",
        "",
        "## Source Register",
        "",
        md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Y5/Y6 Zero-Odd-Source Lock Audit",
        "",
        md_table(all_rows["lock"], ["lock_id", "clause", "current_status", "required_signature", "reason", "residual_if_missing", "valid_for_claim"]),
        "",
        "## Epsilon Extra Source Split",
        "",
        md_table(all_rows["split"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "observable_link", "valid_for_claim"]),
        "",
        "## Runner Status",
        "",
        md_table(all_rows["runner"], ["runner_id", "status", "required_components", "components_evaluable", "reason", "runner_ready", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(all_rows["claims"], ["gate_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(all_rows["decision"], ["decision_id", "decision", "reason", "effect", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(all_rows["next"], ["route_id", "selection_status", "target_file", "target_script", "task", "success_condition", "fallback_condition", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(all_rows["branches"], ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(all_rows["validation"], ["check_id", "passed", "detail", "generated_utc"]),
        "",
        "## Working Read",
        "",
        "This is a real narrowing of the wound. The theory is not dying here; it is being forced to pay its source bill. If Y5 measured source normalization and Y6 extra stress can be made parent-owned or bounded, the response-doublet route still has teeth. If they cannot, they become the local residual the theory must carry into PPN/R10/clock/orbital tests.",
        "",
        "The next move is denominator/frame/surface ownership: without `M_ref`, `tau` and linked surfaces, the Y5/Y6 rows cannot be scored honestly.",
        "",
        "## Forbidden Claims From 2906",
        "",
        "- Y5 source normalization is locally silent.",
        "- Y6 extra stress is locally silent.",
        "- `epsilon_extra_odd_source_Y5=0`, `epsilon_extra_odd_source_Y6=0`, or `epsilon_Qv_extra_piece=0`.",
        "- Exchange oddness alone proves source-normalized Newton.",
        "- Observed orbital GM may be used as a denominator/proof input.",
        "- Source-normalized Newton, PPN, R10, clock, orbital or local GR is proved.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {}
    all_rows["sources"] = source_register_rows()
    all_rows["lock"] = lock_rows()
    all_rows["split"] = split_rows()
    all_rows["runner"] = runner_rows()
    all_rows["claims"] = claim_gate_rows()
    all_rows["decision"] = decision_rows()
    all_rows["next"] = next_rows()

    for key in ["sources", "lock", "split", "runner", "claims", "decision", "next"]:
        write_csv(OUTPUTS[key], all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_doc(all_rows)

    overall = next(row["passed"] for row in all_rows["validation"] if row["check_id"] == "VAL2906_OVERALL")
    print(f"2906 validation overall: {overall}")
    print(DOC)


if __name__ == "__main__":
    main()
