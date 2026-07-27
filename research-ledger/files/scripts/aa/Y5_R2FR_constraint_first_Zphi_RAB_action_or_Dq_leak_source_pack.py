from __future__ import annotations

import csv
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
RAB_SECTOR = ROOT / "source-intake" / "rab-sector"
QUEUE = RAB_SECTOR / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1668"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1668-Y5-R2FR-constraint-first-Zphi-RAB-action-or-Dq-leak-source-pack.md"

SOURCE_FILES = {
    "1667_doc": ROOT / "1667-Y5-R2FR-parent-field-chart-and-quotient-map-Dq-on-Zphi-or-retained-Dq-leak.md",
    "1667_validation": OUT / "P8_Y5_BRR545_1667_VALIDATION.csv",
    "1667_constraint": OUT / "P8_Y5_PARENT_QLOC_1667_CONSTRAINT_FIRST_BRANCH_AUDIT.csv",
    "1667_dq_leaks": OUT / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv",
    "1576_constraint_test": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_CONSTRAINT_NO_POLE_TEST.csv",
    "1576_no_pole": OUT / "P8_Y5_PARENT_QLOC_1576_RAB_NO_POLE_THEOREM_ATTEMPT.csv",
    "1621_constraint_gate": OUT / "P8_Y5_PARENT_QLOC_1621_CONSTRAINT_FIRST_ZMAP_GATE.csv",
    "1621_no_pole_audit": OUT / "P8_Y5_PARENT_QLOC_1621_NO_POLE_THEOREM_AUDIT.csv",
    "1622_vertical_null": OUT / "P8_Y5_PARENT_QLOC_1622_VERTICAL_NULL_BAN_ATTEMPT.csv",
    "1623_no_vertical_metric": OUT / "P8_Y5_PARENT_QLOC_1623_NO_VERTICAL_METRIC_THEOREM_ATTEMPT.csv",
    "1624_no_vertical_metric_decision": OUT / "P8_Y5_PARENT_QLOC_1624_NO_VERTICAL_METRIC_DECISION.csv",
    "1555_first_class_contract": OUT / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv",
    "1562_constraint_class": OUT / "P8_Y5_PARENT_QLOC_1562_CONSTRAINT_CLASS_GATE.csv",
    "1238_first_class_RAB": OUT / "P8_Y5_R10_1238_FIRST_CLASS_RAB_CONSTRAINT_ATTEMPT.csv",
    "1528_lambda_phi": OUT / "P8_Y5_PARENT_QLOC_1528_LAMBDA_PHI_ENERGY_THEOREM.csv",
    "1529_lambda_phi_bounds": OUT / "P8_Y5_PARENT_QLOC_1529_LAMBDA_PHI_BOUND_INPUT_LEDGER.csv",
    "1022_vertical_quotient": OUT / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv",
    "1037_no_pole": OUT / "P8_Y5_R10_1037_NO_PHYSICAL_X_POLE_AUDIT.csv",
    "1038_no_pole_gate": OUT / "P8_Y5_R10_1038_NO_POLE_CLAIM_GATE.csv",
    "782_overconstraint": OUT / "P8_Y5_R10_782_OVERCONSTRAINT_RISK_LEDGER.csv",
}

NEEDLES = {
    "1667_doc": ["constraint-first", "`Dq` leak rows become source-pack inputs"],
    "1667_validation": ["VAL1667_OVERALL", "PASS"],
    "1667_constraint": ["CFB1667_5_verdict", "SELECT_NEXT_CONSTRAINT_OR_DQ_LEAK_BOUND"],
    "1667_dq_leaks": ["DQL1667_7_Scg_envelope", "RETAINED_NONCLAIM_DQ_LEAK_INPUT"],
    "1576_constraint_test": ["CNP1576_5_verdict", "FAIL_CURRENT_CLAIM_CONSTRAINT_NO_POLE_NOT_DERIVED"],
    "1576_no_pole": ["NPT1576_3_verdict", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_DERIVED"],
    "1621_constraint_gate": ["CFG1621_7_verdict", "CONSTRAINT_FIRST_ZMAP_NOT_DERIVED"],
    "1621_no_pole_audit": ["NPA1621_5_verdict", "NO_POLE_NOT_DERIVED_CURRENT_MTS"],
    "1622_vertical_null": ["VNB1622_5_verdict", "VERTICAL_NULL_BAN_NOT_PARENT_SIGNED"],
    "1623_no_vertical_metric": ["NVM1623_4_verdict", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED"],
    "1624_no_vertical_metric_decision": ["NVD1624_4_verdict", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED_FINAL_CURRENT_AUDIT"],
    "1555_first_class_contract": ["FCC1555_7_no_GR_import", "PASS_GUARD_NONCLAIM"],
    "1562_constraint_class": ["CLASS1562_5_second_class", "BETTER_CONDITIONAL_THAN_FIRST_CLASS"],
    "1238_first_class_RAB": ["FCR1238_5_verdict", "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED"],
    "1528_lambda_phi": ["LPE1528_6_theorem_shape", "THEOREM_SHAPE_WRITTEN_NOT_SIGNED"],
    "1529_lambda_phi_bounds": ["BIN1529_8_no_cancellation_guard", "GUARD_WRITTEN"],
    "1022_vertical_quotient": ["VQC1022_7_verdict", "fail_current_claim_but_best_next_target"],
    "1037_no_pole": ["NP1037_6_verdict", "FAIL_CURRENT_CLAIM_NO_POLE_NOT_PROVED"],
    "1038_no_pole_gate": ["NPG1038_0_exact_no_pole", "false"],
    "782_overconstraint": ["ORL782_4_retrofit", "guard_active"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1668_SOURCE_REGISTER.csv"
CONSTRAINT_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1668_CONSTRAINT_FIRST_ACTION_ATTEMPT.csv"
NO_POLE_GATE = OUT / "P8_Y5_PARENT_QLOC_1668_NO_POLE_GATE_AUDIT.csv"
OVERCONSTRAINT_GUARD = OUT / "P8_Y5_PARENT_QLOC_1668_OVERCONSTRAINT_GUARD.csv"
DQ_SOURCE_PACK = OUT / "P8_Y5_PARENT_QLOC_1668_DQ_LEAK_SOURCE_PACK_SCHEMA.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1668_DECISION.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1668_CLAIM_GATE.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1668_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1668_VALIDATION.csv"

GENERATED = [
    SOURCE_REGISTER,
    CONSTRAINT_ATTEMPT,
    NO_POLE_GATE,
    OVERCONSTRAINT_GUARD,
    DQ_SOURCE_PACK,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

CLAIM_CHECKED = [
    CONSTRAINT_ATTEMPT,
    NO_POLE_GATE,
    OVERCONSTRAINT_GUARD,
    DQ_SOURCE_PACK,
    DECISION,
    CLAIM_GATE,
    NEXT_TARGET,
]

COPY_TARGETS = {
    CONSTRAINT_ATTEMPT: [
        QUARANTINE / "CONSTRAINT_FIRST_ACTION_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_constraint_first_action_attempt_nonclaim_1668.csv",
        QUEUE / "JR1668_CONSTRAINT_FIRST_ACTION_ATTEMPT_NONCLAIM.csv",
    ],
    NO_POLE_GATE: [
        QUARANTINE / "NO_POLE_GATE_AUDIT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_no_pole_gate_audit_nonclaim_1668.csv",
        QUEUE / "JR1668_NO_POLE_GATE_AUDIT_NONCLAIM.csv",
    ],
    DQ_SOURCE_PACK: [
        QUARANTINE / "DQ_LEAK_SOURCE_PACK_SCHEMA_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_Dq_leak_source_pack_schema_nonclaim_1668.csv",
        QUEUE / "JR1668_DQ_LEAK_SOURCE_PACK_SCHEMA_NONCLAIM.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_nonclaim_1668.csv",
        QUEUE / "JR1668_NEXT_TARGET_NONCLAIM.csv",
    ],
}


def ensure_dirs() -> None:
    for directory_path in [OUT, QUARANTINE, BRANCH_RESIDUALS, QUEUE]:
        directory_path.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_string(value: object) -> str:
    return str(value).strip().lower()


def all_claim_flags_false(paths: list[Path]) -> bool:
    flag_names = {
        "accepted_for_scoring",
        "claim_allowed",
        "claim_ready",
        "local_gr_claim_allowed",
        "parent_signed",
        "score_allowed",
        "score_ready",
        "source_backed",
        "theorem_closed",
        "theorem_closed_for_claim",
        "valid_for_claim",
        "valid_for_mts_claim",
        "valid_prediction_row",
        "valid_for_runner",
    }
    for path in paths:
        for row in csv_rows(path):
            for flag_name in flag_names.intersection(row):
                if bool_string(row[flag_name]) == "true":
                    return False
    return True


def source_register_rows() -> list[dict[str, object]]:
    rows = []
    for source_id, path in SOURCE_FILES.items():
        text = read_text(path)
        needles = NEEDLES[source_id]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needles_found": all(needle in text for needle in needles),
                "needles": "; ".join(needles),
                "role": "1668 constraint-first Z/phi/R_AB action or Dq leak source-pack input",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def constraint_attempt_rows() -> list[dict[str, object]]:
    rows = [
        ("CFA1668_0_magic_multiplier_guard", "S += int sqrt(-g) lambda_R R_AB or lambda_Z Z", "imposes a residual zero on shell", "REJECT_MAGIC_MULTIPLIER_AS_DERIVATION", "1576/1621/1238: multiplier origin must be parent-derived, not inserted to force GR"),
        ("CFA1668_1_RAB_algebraic_auxiliary", "E_lambda: R_AB=0 and E_R fixes lambda_R algebraically before readout", "removes visible R_AB/J_q before matter sees it", "BEST_CONDITIONAL_ROUTE_NOT_SIGNED", "1562 marks second-class auxiliary route better than first-class but unsigned"),
        ("CFA1668_2_Z_constraint", "lambda_Z Z=0 or equivalent normal-form source-free constraint", "would remove formal Z before q formation", "POSSIBLE_BUT_PARENT_ORIGIN_UNSIGNED", "1667 selected this but no parent action/constraint origin exists"),
        ("CFA1668_3_phi_auxiliary", "local phi action/constraint with stress silence and boundary control", "could keep Khat-shape algebra without matter-visible phi hair", "THEOREM_SHAPE_WRITTEN_NOT_SIGNED", "1528 gives lambda_phi theorem shape but boundary/no-flux/zero-mode branch owners are missing"),
        ("CFA1668_4_first_class_no_pole", "Omega_flat(v)=delta C, closed brackets, degree count, Q=0/proper", "would make residual direction gauge/topological rather than physical", "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED", "1555/1238/1037 keep phase space, generator, brackets, degree count, and boundary missing"),
        ("CFA1668_5_no_vertical_metric", "constructor grammar forbids vertical metric/connection and hence kinetic pole", "would ban local kinetic term without plateau axiom", "NO_VERTICAL_METRIC_THEOREM_NOT_DERIVED", "1622/1623/1624 keep object language/constructor exhaustion unsigned"),
        ("CFA1668_6_positive_nohair_fallback", "positive operator plus J=0 and boundary flux=0", "would set physical residual to zero in local exterior", "VALUES_AND_SOURCE_ZERO_MISSING", "1576/1621 require Z_R, M_R^2, J=0, boundary flux=0"),
        ("CFA1668_7_absent_nonprimitive", "R_AB/Z/phi not primitive parent fields and never vary in matter action", "would remove variation slot and beta/source charge", "NOT_PARENT_PROVED", "needs parent field grammar/readout derivation"),
        ("CFA1668_8_verdict", "constraint-first removal before matter/readout", "preferred derivation route", "CONSTRAINT_FIRST_NOT_DERIVED_CURRENT_CORPUS", "source-pack Dq leak rows remain required"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": attempt_id,
            "route": route,
            "if_true": if_true,
            "status": status,
            "evidence": evidence,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for attempt_id, route, if_true, status, evidence in rows
    ]


def no_pole_gate_rows() -> list[dict[str, object]]:
    rows = [
        ("NPG1668_0_q_kernel", "q parent-defined and Dq[v]=0", "1505/1667 fail current q/Dq computation", "MISSING_Q_DQ"),
        ("NPG1668_1_action_descent", "S_bulk descends through q or constraint-reduced variables before variation", "1022 says conditional only", "ACTION_DESCENT_UNSIGNED"),
        ("NPG1668_2_momentum_map", "delta G=Omega(deltaPhi,v), G=int epsilon C+Q", "1037/1555 say Omega, DC, generator missing", "MISSING_OMEGA_DCX_GENERATOR"),
        ("NPG1668_3_boundary_silence", "Q_X=0/exact/proper and no compact edge source", "1576/1037 keep boundary charge missing", "BOUNDARY_CHARGE_OPEN"),
        ("NPG1668_4_degree_count", "constraint removes pair rather than hiding dynamics", "1555/1037 say degree count missing", "DEGREE_COUNT_MISSING"),
        ("NPG1668_5_matter_readout", "ordinary matter/readout descends after constraint reduction", "1576/1022/778 keep matter descent conditional", "MATTER_DESCENT_UNSIGNED"),
        ("NPG1668_6_overconstraint", "local theorem does not kill galaxy/cosmology/EM mechanisms by overbroad coupling owner", "782 overconstraint risks are open", "SCOPE_GUARD_OPEN"),
        ("NPG1668_7_verdict", "no physical Z/phi/R_AB local pole/source", "1038 gate false; 1621/1576 fail current claim", "NO_POLE_NOT_PROVED_CURRENT_CORPUS"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "required_gate": gate,
            "evidence": evidence,
            "status": status,
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, evidence, status in rows
    ]


def overconstraint_rows() -> list[dict[str, object]]:
    rows = [
        ("OCG1668_0_symbol_collision", "do not rename existing fields into Q to make coupling vanish", "field-map proof must preserve MTS meanings", "GUARD_ACTIVE"),
        ("OCG1668_1_overkill", "ordinary-matter coupling owner must not erase desired galaxy/cosmology/memory sectors", "separate local matter quotient from residual/gravity dynamics", "GUARD_ACTIVE"),
        ("OCG1668_2_boundary_silence", "bulk constraint silence is insufficient without boundary/source-measure proof", "retain boundary leak rows if no certificate", "GUARD_ACTIVE"),
        ("OCG1668_3_frame_readout", "clocks/photons/EM/orbits cannot use hidden frame maps", "readout maps must be written or bounded", "GUARD_ACTIVE"),
        ("OCG1668_4_retrofit", "do not adopt owner action only because it recovers GR", "requires independent spine compatibility", "GUARD_ACTIVE"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "risk_guard": guard,
            "required_mitigation": mitigation,
            "status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, guard, mitigation, status in rows
    ]


def dq_source_pack_rows() -> list[dict[str, object]]:
    rows = [
        ("DSP1668_0_Dq_Z", "Dq_Z_norm", "arena dependent", "Z normal-form quotient leak", "MISSING_NUMERIC_OR_THEOREM_ZERO", "source path to q(Phi), Z basis, Dq[partial_Z], norm convention, arena projection"),
        ("DSP1668_1_Dq_phi", "Dq_phi_norm", "arena dependent", "phi improvement quotient leak", "MISSING_NUMERIC_OR_THEOREM_ZERO", "source path to phi action, q dependence, Dq[partial_phi], boundary/domain convention"),
        ("DSP1668_2_Dq_RAB_Jq", "Dq_RAB_or_Jq_norm", "arena dependent", "R_AB/J_q cell-visible leak", "MISSING_NUMERIC_OR_THEOREM_ZERO", "source path to q cell map or constraint that removes R_AB/J_q"),
        ("DSP1668_3_C_qm", "C_qm=||DObs_e[Dq[v]]||", "coframe norm", "geometry pullback/source stress", "MISSING_NUMERIC_OR_THEOREM_ZERO", "observed coframe functor and local weak-field norm"),
        ("DSP1668_4_S_direct", "S_direct", "E* forcing units", "direct matter/source dependence", "MISSING_NUMERIC_OR_THEOREM_ZERO", "matter/source action domain exclusion or derivative bound"),
        ("DSP1668_5_S_boundary", "S_boundary", "E* or boundary charge units", "compact boundary/source-memory coupling", "MISSING_NUMERIC_OR_THEOREM_ZERO", "Q_X/B_X boundary charge and projection norm"),
        ("DSP1668_6_marker", "Dtheta_marker_Dq_leak", "dimensionless", "constants/material markers", "MISSING_NUMERIC_OR_THEOREM_ZERO", "mass/charge/clock constant owner or marker derivative bound"),
        ("DSP1668_7_Scg_envelope", "S_cg_norm <= 0.5||T||_source*C_qm + S_direct + S_source_norm_extra + S_boundary", "E* forcing units", "absolute no-cancellation envelope", "SCHEMA_READY_INPUTS_MISSING", "all component rows above with no cancellation"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "source_pack_id": source_pack_id,
            "symbol": symbol,
            "units": units,
            "channel": channel,
            "status": status,
            "needed_source_inputs": inputs,
            "source_backed": False,
            "accepted_for_scoring": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for source_pack_id, symbol, units, channel, status, inputs in rows
    ]


def decision_rows() -> list[dict[str, object]]:
    rows = [
        ("DEC1668_0_constraint", "CONSTRAINT_FIRST_NOT_DERIVED", "cleanest route remains open but parent origin/class/boundary/matter gates fail", "do not promote q_loc=0/local GR"),
        ("DEC1668_1_second_class", "SECOND_CLASS_AUXILIARY_REMAINS_BEST_CONDITIONAL_ROUTE", "it removes visible residuals before matter sees them without calling them gauge", "target parent origin of lambda_Z/lambda_R/phi action if new source evidence appears"),
        ("DEC1668_2_no_pole", "NO_POLE_NOT_PROVED", "first-class/no-pole needs q, Omega, DC, boundary, degree count, matter descent", "retain finite pole/source branch"),
        ("DEC1668_3_source_pack", "DQ_LEAK_SOURCE_PACK_STAGED", "Dq leak rows now have source-pack fields and units/status placeholders", "fill real q/Dq or bounds before empirical scoring"),
        ("DEC1668_4_next", "NEXT_DQ_LEAK_BOUND_SOURCE_PACK_UNITS_ARENA", "constraint proof failed current corpus, so build source-ready bound inputs", "prepare arena projections for R10/PPN/WEP/clock/orbit without claims"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for decision_id, decision, reason, next_action in rows
    ]


def claim_rows() -> list[dict[str, object]]:
    rows = [
        ("CG1668_0_constraint_origin", "parent constraint/no-pole action removes Z/phi/R_AB before matter", False, "BLOCKED", "constraint origin not parent-derived"),
        ("CG1668_1_first_class", "first-class/no-pole certificate closes", False, "BLOCKED", "Omega/DC/bracket/boundary/degree count missing"),
        ("CG1668_2_second_class", "second-class/algebraic auxiliary elimination closes", False, "BLOCKED", "parent sort/no-derivative/matter/boundary gates unsigned"),
        ("CG1668_3_phi_silence", "phi/lambda_phi stress and zero-mode silence close", False, "BLOCKED", "boundary/no-flux/zero-mode certificates missing"),
        ("CG1668_4_Dq_source_pack_claim", "Dq leak source pack can be scored", False, "NO_CLAIM", "source-backed numeric/theorem-zero inputs missing"),
        ("CG1668_5_local_GR_Newton", "local GR/Newton follows", False, "NO_CLAIM", "constraint route fails current corpus and Dq leaks remain"),
        ("CG1668_6_empirical_passes", "PPN/R10/WEP/clock/orbit passes follow", False, "NO_CLAIM", "no arena pass until source pack is filled and bounded"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "status": status,
            "blocker": blocker,
            "local_gr_claim_allowed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, claim, gate_pass, status, blocker in rows
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "1669-Y5-R2FR-Dq-leak-bound-source-pack-units-and-arena-projections.md",
            "script": "scripts/Y5_R2FR_Dq_leak_bound_source_pack_units_and_arena_projections.py",
            "objective": "turn retained Dq leak symbols into a source-ready nonclaim bound pack with units, source requirements, and arena projections for R10, PPN, WEP, clocks, and orbital tests",
            "success_condition": "each retained Dq/source/boundary leak has a declared unit convention, source input requirement, arena projection placeholder, and valid_for_claim=false until sourced",
            "forbidden_shortcuts": "no invented numeric Dq values; no cancellation; no local GR/Newton/PPN/R10/WEP claim; no GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
            "score_allowed": False,
        }
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)


def validation_rows(
    source_rows: list[dict[str, object]],
    attempt: list[dict[str, object]],
    no_pole: list[dict[str, object]],
    guards: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
) -> list[dict[str, object]]:
    generated_csv_parse = True
    try:
        for generated_path in GENERATED:
            csv_rows(generated_path)
    except Exception:
        generated_csv_parse = False

    generated_name_markers = (
        "1668-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1668",
        "P8_Y5_BRR545_1668",
        "JR1668",
        "Y5_R2FR_constraint_first_Zphi_RAB",
    )
    formalization_dirty = (
        any(
            "1668" in path.name
            and any(marker in path.name for marker in generated_name_markers)
            for path in FORMALIZATION.rglob("*1668*")
        )
        if FORMALIZATION.exists()
        else False
    )
    constraint_failed = any(row["attempt_id"] == "CFA1668_8_verdict" and row["status"] == "CONSTRAINT_FIRST_NOT_DERIVED_CURRENT_CORPUS" for row in attempt)
    no_pole_failed = any(row["gate_id"] == "NPG1668_7_verdict" and row["status"] == "NO_POLE_NOT_PROVED_CURRENT_CORPUS" for row in no_pole)
    guards_active = all(row["status"] == "GUARD_ACTIVE" for row in guards)
    source_pack_nonclaim = all(row["claim_allowed"] is False and row["valid_for_claim"] is False and row["valid_prediction_row"] is False for row in source_pack)
    next_target_selected = next_targets[0]["next_target"] == "1669-Y5-R2FR-Dq-leak-bound-source-pack-units-and-arena-projections.md"

    checks = [
        ("VAL1668_0_sources_exist", all(row["path_exists"] and row["needles_found"] for row in source_rows), "all cited 1668 source paths exist and needles are present"),
        ("VAL1668_1_constraint_failed_current", constraint_failed, "constraint-first route remains not derived"),
        ("VAL1668_2_no_pole_failed_current", no_pole_failed, "no-pole route remains not proved"),
        ("VAL1668_3_overconstraint_guards_active", guards_active, "overconstraint/retrofit guards remain active"),
        ("VAL1668_4_source_pack_nonclaim", source_pack_nonclaim, "Dq leak source pack remains nonclaim/unscored"),
        ("VAL1668_5_decision_source_pack", any(row["decision"] == "DQ_LEAK_SOURCE_PACK_STAGED" for row in decisions), "decision records source-pack fallback"),
        ("VAL1668_6_claim_gates_safe", all(row["claim_allowed"] is False and row["valid_for_claim"] is False for row in claim), "all claim gates keep MTS local claims false"),
        ("VAL1668_7_next_target_selected", next_target_selected, "next target selects Dq leak source-pack units and arena projections"),
        ("VAL1668_8_csv_parse", generated_csv_parse, "all generated 1668 CSVs parse"),
        ("VAL1668_9_no_mts_claim_flags", all_claim_flags_false(CLAIM_CHECKED), "all 1668 generated rows keep MTS claim/no-score flags false"),
        ("VAL1668_10_branch_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" not in str(target)), "branch/quarantine copies exist"),
        ("VAL1668_11_queue_copies", all(target.exists() for targets in COPY_TARGETS.values() for target in targets if "acquisition-queue" in str(target)), "acquisition queue nonclaim copies exist"),
        ("VAL1668_12_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1668_13_formalization_untouched", not formalization_dirty, "no 1668 outputs found under formalization-workbench"),
    ]
    rows = [
        {
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL1668_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1668 constraint-first Z/phi/R_AB action or Dq leak source-pack validation",
            "valid_for_mts_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, object]],
    attempt: list[dict[str, object]],
    no_pole: list[dict[str, object]],
    guards: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    decisions: list[dict[str, object]],
    claim: list[dict[str, object]],
    next_targets: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    text = f"""# 1668 - Constraint-First Z/phi/R_AB Action Or Dq Leak Source Pack

**Private status:** constraint-first derivation attempt plus source-pack fallback. No `q_loc=0`, local-GR pass, Newton pass, PPN pass, R10 pass, WEP pass, clock pass, orbital pass, or public claim is made.

## Verdict

The constraint-first route is still the cleanest derivation idea, but it does **not** close in the current corpus.

```text
Best conditional route:
remove Z/phi/R_AB before matter/readout sees them.

Current result:
constraint origin unsigned,
no-pole certificate unsigned,
boundary/matter/readout gates unsigned,
no-vertical-metric theorem not derived.
```

So `1668` stages the retained `Dq` leak rows into a source-pack schema. This keeps us honest: if the elegant constraint route cannot be derived, the leak has to be bounded in R10/PPN/WEP/clock/orbit arenas rather than hidden.

## Source Register

{markdown_table(source_rows, ["source_id", "path", "path_exists", "needles_found", "role"])}

## Constraint-First Action Attempt

{markdown_table(attempt, ["attempt_id", "route", "if_true", "status", "evidence"])}

## No-Pole Gate Audit

{markdown_table(no_pole, ["gate_id", "required_gate", "evidence", "status"])}

## Overconstraint Guard

{markdown_table(guards, ["guard_id", "risk_guard", "required_mitigation", "status"])}

## Dq Leak Source Pack Schema

{markdown_table(source_pack, ["source_pack_id", "symbol", "units", "channel", "status", "needed_source_inputs"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "reason", "next_action"])}

## Claim Gates

{markdown_table(claim, ["gate_id", "claim", "gate_pass", "status", "blocker"])}

## Next Target

{markdown_table(next_targets, ["next_target", "script", "objective", "success_condition"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Working Interpretation

The theory is being forced into a good shape here. Either the local residual variables are removed by a genuine parent mechanism before ordinary matter sees them, or they become measurable/boundable leak channels. That is exactly the fork a serious GR/Newton-reduction programme needs. The next job is less glamorous but valuable: make the retained leak rows arena-ready without inventing numbers.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    source_rows = source_register_rows()
    attempt = constraint_attempt_rows()
    no_pole = no_pole_gate_rows()
    guards = overconstraint_rows()
    source_pack = dq_source_pack_rows()
    decisions = decision_rows()
    claim = claim_rows()
    next_targets = next_rows()

    for path, rows in [
        (SOURCE_REGISTER, source_rows),
        (CONSTRAINT_ATTEMPT, attempt),
        (NO_POLE_GATE, no_pole),
        (OVERCONSTRAINT_GUARD, guards),
        (DQ_SOURCE_PACK, source_pack),
        (DECISION, decisions),
        (CLAIM_GATE, claim),
        (NEXT_TARGET, next_targets),
    ]:
        write_csv(path, rows)

    copy_outputs()
    validation = validation_rows(source_rows, attempt, no_pole, guards, source_pack, decisions, claim, next_targets)
    write_csv(VALIDATION, validation)
    write_doc(source_rows, attempt, no_pole, guards, source_pack, decisions, claim, next_targets, validation)

    if any(row["result"] == "FAIL" for row in validation):
        raise SystemExit("1668 validation failed; see P8_Y5_BRR545_1668_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print("1668 validation PASS")


if __name__ == "__main__":
    main()
