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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2951"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2951-Y5-R2FR-parent-X-field-owner-or-ZX-MX2-source-row-under-AX1090.md"

SRC_2950_DOC = ROOT / "2950-Y5-R2FR-parent-X-operator-coefficient-or-finite-residual-input-acquisition-under-AX1090.md"
SRC_2950_NEXT = RESIDUALS / "P8_Y5_R2FR_2950_NEXT_TARGET.csv"
SRC_2950_PAYLOAD = RESIDUALS / "P8_Y5_R2FR_2950_OPERATOR_PAYLOAD_ACQUISITION_AUDIT.csv"
SRC_2950_OPERATOR = RESIDUALS / "P8_Y5_R2FR_2950_ZX_MX2_OPERATOR_STATUS.csv"
SRC_2949_INPUTS = RESIDUALS / "P8_Y5_R2FR_2949_POSITIVE_OPERATOR_INPUT_QUEUE.csv"
SRC_579_CONTRACT = RESIDUALS / "P8_Y5_R10_579_EXPLICIT_PARENT_X_BLOCK_CONTRACT.csv"
SRC_580_CANDIDATES = RESIDUALS / "P8_Y5_R10_580_PARENT_BLOCK_CANDIDATES.csv"
SRC_669_CANDIDATES = RESIDUALS / "P8_Y5_R10_669_MINIMAL_LX_OPERATOR_CANDIDATES.csv"
SRC_669_GATES = RESIDUALS / "P8_Y5_R10_669_LX_OWNER_GATE_TESTS.csv"
SRC_1018_DOC = ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"
SRC_1041_CLASSIFIER = RESIDUALS / "P8_Y5_R10_1041_PARENT_X_CANDIDATE_CLASSIFIER.csv"
SRC_1042_IDENTITY = RESIDUALS / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv"
SRC_1042_PREMISE = RESIDUALS / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv"
SRC_1042_SOURCE_ZERO = RESIDUALS / "P8_Y5_R10_1042_SOURCE_ZERO_CLAUSE_AUDIT.csv"
SRC_ACTION_TERMS = RESIDUALS / "P8_source_owner_parent_action_terms_CONTRACT.csv"
SRC_MIN_PARENT = RESIDUALS / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2951_SOURCE_REGISTER.csv",
    "owner_contract": RESIDUALS / "P8_Y5_R2FR_2951_PARENT_X_OWNER_CONTRACT.csv",
    "route_triage": RESIDUALS / "P8_Y5_R2FR_2951_PARENT_X_ROUTE_TRIAGE.csv",
    "coefficients": RESIDUALS / "P8_Y5_R2FR_2951_ZX_MX2_SOURCE_ROW_ATTEMPT.csv",
    "zero_mode": RESIDUALS / "P8_Y5_R2FR_2951_ZERO_MODE_POLICY_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2951_HARD_FORK_DECISION.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2951_CLAIM_GATES.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2951_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2951_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2951_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "owner_copy": PARENT_ACTION / "parent_X_owner_contract_2951_NONCLAIM.csv",
    "coefficient_copy": PARENT_ACTION / "ZX_MX2_source_row_attempt_2951_BLOCKED.csv",
    "next_copy": RAB_QUEUE / "JR2951_NOPOLE_VERTICAL_OR_POSITIVE_HESSIAN_HARD_FORK_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


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


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2951_00_2950_doc", SRC_2950_DOC, "Status: `Y5_R2FR_2950;NEXT2950_0_2951", "2950 handoff"),
        ("SRC2951_01_2950_next", SRC_2950_NEXT, "NEXT2950_0_2951", "machine-readable 2951 target"),
        ("SRC2951_02_2950_payload", SRC_2950_PAYLOAD, "PAY2950_0_X_field_owner;PAY2950_1_ZX;PAY2950_2_MX2", "2950 missing payload audit"),
        ("SRC2951_03_2950_operator", SRC_2950_OPERATOR, "OP2950_2_ZX_value;OP2950_3_MX2_value;OP2950_6_verdict", "2950 operator status"),
        ("SRC2951_04_2949_inputs", SRC_2949_INPUTS, "PIN2949_0_X_variable;PIN2949_2_ZX;PIN2949_3_MX2", "2949 positive operator queue"),
        ("SRC2951_05_579_contract", SRC_579_CONTRACT, "PXC579_0_branch_extremum;PXC579_1_positive_kinetic_residue;PXC579_2_positive_mass_gap", "explicit parent X block contract"),
        ("SRC2951_06_580_candidates", SRC_580_CANDIDATES, "PB580_0_absent_quotient_variable;PB580_2_positive_sourcefree_massive_X;PB580_3_massive_sourced_residual", "parent block candidate routes"),
        ("SRC2951_07_669_candidates", SRC_669_CANDIDATES, "LX669_0_absent_quotient_variable;LX669_2_positive_sourcefree_massive;LX669_3_massive_sourced_residual", "minimal L_X operator candidates"),
        ("SRC2951_08_669_gates", SRC_669_GATES, "G669_0_branch_extremum;G669_7_retained_residual_vector", "L_X owner gate tests"),
        ("SRC2951_09_1018_doc", SRC_1018_DOC, "LOC1018_0_LX_owner;CG1018_1_LX_owned", "sector Lagrangian owner audit"),
        ("SRC2951_10_1041_classifier", SRC_1041_CLASSIFIER, "XC1041_0_absent_quotient;XC1041_2_positive_sourcefree_physical_X", "parent X route classifier"),
        ("SRC2951_11_1042_identity", SRC_1042_IDENTITY, "NH1042_1_energy_identity;NH1042_5_verdict", "conditional no-hair identity"),
        ("SRC2951_12_1042_premise", SRC_1042_PREMISE, "NHP1042_0_LX_owner;NHP1042_6_verdict", "no-hair premise gates"),
        ("SRC2951_13_1042_source_zero", SRC_1042_SOURCE_ZERO, "SZ1042_0_matter_pullback;SZ1042_5_verdict", "source-zero clause audit"),
        ("SRC2951_14_action_terms", SRC_ACTION_TERMS, "A7_bulk_X_nohair_or_curve;A2_no_retained_source_constraint", "parent action term contract"),
        ("SRC2951_15_min_parent", SRC_MIN_PARENT, "A511_3_extra_field_silence;A511_6_metric_readout", "minimal parent local-GR action blocks"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def owner_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("OWN2951_0_field_identity", "X field identity", "one parent-owned object: absent quotient coordinate, first-class vertical direction, or physical extra field", "580/669/1041 give a menu, not a selected parent object", "NOT_PARENT_SELECTED", False, "defines what Z_X/M_X^2 would belong to"),
        ("OWN2951_1_action_owner", "S_X or no-S_X proof", "single parent action either contains S_X or proves no independent X variation before readout", "A7 and A511_3 name the required block; 1018/2950 say it is not owned", "MISSING_PARENT_ACTION_BLOCK", False, "prevents coefficient rows from being detached knobs"),
        ("OWN2951_2_euler_owner", "E_X equation", "delta S_parent/delta X gives explicit Euler expression and branch extremum E_X|0=0", "579 PXC579_0 is not_parent_filled; 669 G669_0 blocked", "MISSING_EULER_EXPRESSION", False, "allows no-hair or finite Green function to be legal"),
        ("OWN2951_3_field_normalization", "field normalization and units", "X normalization, action units, domain measure, and sign convention are fixed before scoring", "2950/2949 mark X variable and Z/M units missing", "MISSING_FIELD_UNITS", False, "makes Z_X and M_X^2 comparable"),
        ("OWN2951_4_ZX_owner", "Z_X / A_X^ij", "second variation gives positive kinetic/operator coefficient with source path", "579 gives formula_only; 1042 says formula_only_not_parent_signed", "FORMULA_ONLY_NOT_PARENT_SIGNED", False, "positive identity left-hand side becomes claim-grade"),
        ("OWN2951_5_MX2_owner", "M_X^2", "second variation gives positive mass/gap/range and zero-mode rule", "579 gives formula_only; 1042 says formula_only_not_parent_signed", "FORMULA_ONLY_NOT_PARENT_SIGNED", False, "lambda_X=sqrt(Z_X/M_X^2) becomes source-backed"),
        ("OWN2951_6_zero_mode_owner", "zero-mode/topology policy", "kernel is quotient/proper gauge or killed by boundary/reference data", "1042 NHP1042_5 keeps topology/kernel open", "TOPOLOGY_KERNEL_GATE_OPEN", False, "prevents a flat/topological X from evading the no-hair proof"),
        ("OWN2951_7_JX_owner", "J_X source law", "ordinary matter, boundary, projector, domain, and memory source channels vanish or are bounded channelwise", "1042 source-zero audit fails total J_X zero", "SOURCE_ZERO_NOT_DERIVED", False, "decides no-hair branch versus finite residual branch"),
        ("OWN2951_8_boundary_owner", "Phi_boundary_local / B_X", "boundary flux, source worldtube, reference subtraction, corners, and harmonic terms vanish or are bounded", "1042 and 1018 leave boundary owner open", "BOUNDARY_FLUX_ZERO_NOT_DERIVED", False, "turns integration by parts into a theorem rather than a closure"),
        ("OWN2951_9_readout_owner", "metric/source readout X-blindness", "g_readout and Pi_M have no linear X leakage, or leakage is explicitly scored", "A511_6 is a requirement, not a proved current-MTS fact", "READOUT_BLINDNESS_NOT_DERIVED", False, "protects Newton/PPN from hidden source normalization shifts"),
        ("OWN2951_10_verdict", "parent X owner", "all owner clauses above pass from one compatible parent route", "no inspected source supplies a single parent-signed X package", "PARENT_X_OWNER_NOT_ACQUIRED", False, "score rows and local-GR claim stay blocked"),
    ]
    return [
        add_common(
            {
                "clause_id": clause_id,
                "object": obj,
                "acceptance_test": acceptance,
                "evidence_summary": evidence,
                "current_status": status,
                "owner_acquired": acquired,
                "unlock_if_closed": unlock,
            }
        )
        for clause_id, obj, acceptance, evidence, status, acquired, unlock in rows
    ]


def route_triage_rows() -> list[dict[str, Any]]:
    rows = [
        ("ROUTE2951_0_absent_quotient", "X absent from physical quotient before variation", 1, "highest", "BEST_GR_REDUCTION_ROUTE_NOT_SIGNED", "explicit q map, tangent split, and proof X is not a physical variation", "derive no physical X pole without Z/M scoring", True),
        ("ROUTE2951_1_first_class_vertical", "X is first-class vertical/gauge/constraint direction", 2, "high", "BEST_ACTIVE_ROUTE_BUT_INCOMPLETE", "v_X in ker(Dq), Omega-flat momentum map, bracket closure, proper boundary charge", "derive K_X=0 or source/test charge zero by Noether identity", True),
        ("ROUTE2951_2_positive_sourcefree", "X is physical but positive and source-free locally", 3, "medium", "VIABLE_NOHAIR_ROUTE_INPUTS_MISSING", "parent L_X, Z_X>0, M_X^2>0, J_X=0, Phi_boundary=0, no kernel", "derive X=0 by the conditional no-hair identity", False),
        ("ROUTE2951_3_sourced_residual", "X is physical and finitely sourced", 4, "empirical", "EMPIRICAL_FALLBACK_ONLY", "Z_X, M_X^2, lambda_X, K_X, Qbar_XH, qbar_XT, bounds", "score alpha(lambda), WEP, PPN, clocks, orbital rows without local-GR claim", False),
        ("ROUTE2951_4_universal_conformal", "matter sees exp(2 a_X X)g", 5, "countermodel", "COUNTERMODEL_NOT_SOLUTION", "a_X=0 would need a separate parent theorem; otherwise a fifth force is live", "reject as cheap GR proof; use only as failure-mode test", False),
        ("ROUTE2951_5_memory_nonlocal", "X is a local face of memory/history kernel", 6, "open", "KERNEL_OWNER_MISSING", "parent kernel, spectrum, local lift, and source silence", "retain as nonlocal residual branch until kernel is owned", False),
    ]
    return [
        add_common(
            {
                "route_id": route_id,
                "parent_route": route,
                "rank": rank,
                "gr_reduction_power": power,
                "current_status": status,
                "missing_payload": missing,
                "next_test": next_test,
                "selected_for_2952_hard_fork": selected,
            }
        )
        for route_id, route, rank, power, status, missing, next_test, selected in rows
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    rows = [
        ("COEFF2951_0_ZX_formula", "Z_X / A_X^ij", "Z_X=(1/3) h_ij H_grad^ij or A_X^ij from the parent Hessian of S_X", "explicit second variation with field normalization and sign convention", "FORMULA_ONLY_NOT_PARENT_SIGNED", "MISSING", "operator_or_action_units", SRC_579_CONTRACT),
        ("COEFF2951_1_ZX_sign", "Z_X>0", "Z_X>=Z_min>0 on the compact local branch", "positive Hessian or ellipticity certificate from parent action", "MISSING_SIGN_CERTIFICATE", "MISSING", "operator_or_action_units", SRC_1042_PREMISE),
        ("COEFF2951_2_MX2_formula", "M_X^2", "M_X^2=H_0 and lambda_X=sqrt(Z_X/M_X^2)", "explicit potential/Hessian ratio with units and branch definition", "FORMULA_ONLY_NOT_PARENT_SIGNED", "MISSING", "inverse_length_squared_or_action_units", SRC_579_CONTRACT),
        ("COEFF2951_3_MX2_gap", "M_X^2>0", "M_X^2>=m_min^2>0 with no unhandled zero mode", "mass-gap proof plus topology/kernel policy", "MISSING_GAP_CERTIFICATE", "MISSING", "inverse_length_squared_or_action_units", SRC_1042_PREMISE),
        ("COEFF2951_4_lambdaX", "lambda_X", "lambda_X=sqrt(Z_X/M_X^2)", "both Z_X and M_X^2 source-backed in same normalization", "BLOCKED_BY_ZX_MX2", "MISSING", "length", SRC_2950_PAYLOAD),
        ("COEFF2951_5_candidate_row", "candidate Z_X/M_X^2 row", "smallest honest row is formula-only and nonclaim", "cannot promote until parent owner, Z sign, M gap, and zero-mode pass", "SOURCE_ROW_BLOCKED_NOT_SCORE_READY", "MISSING", "mixed", SRC_2950_OPERATOR),
    ]
    return [
        add_common(
            {
                "coefficient_id": coeff_id,
                "symbol": symbol,
                "proposed_definition": definition,
                "required_source": required,
                "current_status": status,
                "numeric_or_theorem_value": value,
                "units": units,
                "source_path": str(source_path),
                "source_path_exists": source_path.exists(),
                "accepted_for_scoring": False,
            }
        )
        for coeff_id, symbol, definition, required, status, value, units, source_path in rows
    ]


def zero_mode_rows() -> list[dict[str, Any]]:
    rows = [
        ("ZMG2951_0_no_pole", "absent quotient or first-class vertical route", "no physical X pole exists, so zero-mode question is removed before variation", "Q/vertical owner missing", "OPEN", False),
        ("ZMG2951_1_positive_gap", "positive physical route", "M_X^2 has a strict positive gap after quotienting proper gauge/topology", "M_X^2 gap and quotient kernel missing", "OPEN", False),
        ("ZMG2951_2_boundary_fixing", "boundary/reference route", "Dirichlet, Neumann, exact/topological, or fixed-reference boundary class kills constant/harmonic X", "boundary flux and harmonic mode owner missing", "OPEN", False),
        ("ZMG2951_3_sourcefree_right_side", "energy identity route", "J_X=0 and Phi_boundary_local=0 channelwise, so the positive norm forces X=0", "J_X and Phi_boundary clauses fail in 1042", "OPEN", False),
        ("ZMG2951_4_verdict", "zero-mode policy", "one of ZMG2951_0 through ZMG2951_3 closes without deleting GR charges", "no zero-mode policy is parent-signed", "ZERO_MODE_POLICY_NOT_ACQUIRED", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "route": route,
                "pass_condition": condition,
                "current_blocker": blocker,
                "current_status": status,
                "gate_pass": passed,
            }
        )
        for gate_id, route, condition, blocker, status, passed in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2951_0_result", "parent X owner not acquired", "the corpus has a route menu and conditional identities, but not a single parent-signed X object with action, variation, coefficients, source, and boundary", "do not score Z_X/M_X^2 or local-GR claims"),
        ("DEC2951_1_coefficient_result", "Z_X/M_X^2 source row attempt remains blocked", "the only available Z/M content is formula-only from a Hessian contract; no field normalization, units, signs, gap, or zero-mode policy exist", "keep coefficient rows nonclaim"),
        ("DEC2951_2_hard_fork", "next move should try no-pole/vertical before positive Hessian", "if X is absent or vertical before variation, local GR can be recovered without fitting a fifth-force sector; if not, X must be treated as a physical residual field", "build 2952 no-pole quotient or vertical-generator proof gate"),
        ("DEC2951_3_no_detour", "do not loop into R10/PPN scoring yet", "all downstream score formulas would still be placeholder arithmetic without the parent X owner or no-pole proof", "exclude alpha(lambda), I_X, orbital-GM denominator, and public claims"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2951_0_parent_X_owner", "parent X field/equation owner acquired", False, "PARENT_X_OWNER_NOT_ACQUIRED"),
        ("CG2951_1_no_pole", "X has no physical pole by quotient/vertical proof", False, "NOPOLE_ROUTE_NOT_PROVED"),
        ("CG2951_2_ZX_MX2", "Z_X/M_X^2 source row accepted", False, "COEFFICIENT_SOURCE_ROW_BLOCKED"),
        ("CG2951_3_nohair", "positive source-free no-hair closes", False, "NOHAIR_PREMISES_UNSIGNED"),
        ("CG2951_4_finite_residual", "finite residual branch score-ready", False, "LAMBDA_K_QBAR_QBAR_MISSING"),
        ("CG2951_5_local_GR", "local GR/Newton reduction allowed", False, "NO_LOCAL_GR_CLAIM"),
        ("CG2951_6_public", "public claim allowed", False, "PRIVATE_NONCLAIM_CHECKPOINT"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2951_0_2952",
                "priority": "selected_primary",
                "next_doc": "2952-Y5-R2FR-parent-X-no-pole-quotient-or-vertical-generator-proof-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_parent_X_no_pole_quotient_or_vertical_generator_proof_under_AX1090_2952.py",
                "objective": "Try to prove X has no physical pole by showing it is absent from the parent quotient before variation or is a first-class vertical direction with proper boundary charge. If this fails, explicitly demote to the positive physical X Hessian/source-pack route.",
                "include": "q map;physical tangent split;v_X in ker(Dq);Omega-flat/momentum-map test;bracket closure;proper boundary charge;matter descent;no-pole verdict;fallback to Z_X/M_X^2 source pack",
                "exclude": "Z_X/M_X^2 scoring;I_X scoring;alpha(lambda) scoring;EH-only substitution;orbital-GM denominator;claiming local GR;public claim;formalization-workbench edits;GitHub action",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("owner_copy", OUTPUTS["owner_contract"], BRANCH_OUTPUTS["owner_copy"]),
        ("coefficient_copy", OUTPUTS["coefficients"], BRANCH_OUTPUTS["coefficient_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())

    checks = [
        ("VAL2951_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2951_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all source anchors found", True),
        ("VAL2951_2_owner_contract_emitted", any(row["clause_id"] == "OWN2951_10_verdict" and row["owner_acquired"] is False for row in all_rows["owner_contract"]), "parent X owner contract emitted and blocked", True),
        ("VAL2951_3_no_route_claim", all(row["valid_for_claim"] is False for row in all_rows["route_triage"]), "route triage remains nonclaim", True),
        ("VAL2951_4_hard_fork_selected", any(row["route_id"] == "ROUTE2951_0_absent_quotient" and row["selected_for_2952_hard_fork"] is True for row in all_rows["route_triage"]), "absent quotient is selected for 2952 hard fork", True),
        ("VAL2951_5_coefficients_blocked", all(row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["coefficients"]), "Z_X/M_X^2 rows are blocked and nonclaim", True),
        ("VAL2951_6_zero_mode_blocked", any(row["gate_id"] == "ZMG2951_4_verdict" and row["gate_pass"] is False for row in all_rows["zero_mode"]), "zero-mode policy verdict is blocked", True),
        ("VAL2951_7_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates are blocked", True),
        ("VAL2951_8_next_target_written", any(row["next_id"] == "NEXT2951_0_2952" for row in all_rows["next"]), "2952 next target selected", True),
        ("VAL2951_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2951_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2951_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2951_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2951 outputs were written to formalization-workbench", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2951_OVERALL",
                "passed": overall,
                "check": "2951 validation overall",
                "required": True,
            }
        )
    )
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2951 - Y5 R2FR: parent X field owner or Z_X/M_X^2 source row under AX1090

Status: `Y5_R2FR_2951_parent_X_owner_not_acquired_ZX_MX2_source_row_blocked_no_pole_hard_fork_selected`

Claim ceiling: `no_parent_X_owner_no_no_pole_proof_no_ZX_no_MX2_no_zero_mode_policy_no_JX_zero_no_Ix_score_no_alpha_score_no_local_GR_no_Newton_no_R10_no_PPN_no_public_claim`

2951 asks the narrow question from 2950: can the corpus supply the parent `X` owner or the first source-backed `Z_X/M_X^2` coefficient row? The answer is:

- No parent `X` owner is acquired: the inspected corpus contains route menus, contracts, and conditional identities, but not one parent-signed `X` object with action, variation, coefficients, source, boundary, and readout.
- No `Z_X/M_X^2` source row is acquired: the available coefficient content is formula-only Hessian language without field normalization, units, signs, mass gap, or zero-mode policy.
- The least-circling next move is a hard fork: first try the cleaner no-pole route (`X` absent from quotient or first-class vertical before variation); if that fails, demote explicitly to a physical positive/residual `X` sector requiring real Hessian/source coefficients.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## Parent X Owner Contract

{md_table(all_rows["owner_contract"], ["clause_id", "object", "current_status", "owner_acquired", "unlock_if_closed"])}

## Parent X Route Triage

{md_table(all_rows["route_triage"], ["route_id", "parent_route", "rank", "gr_reduction_power", "current_status", "selected_for_2952_hard_fork"])}

## Z_X / M_X^2 Source Row Attempt

{md_table(all_rows["coefficients"], ["coefficient_id", "symbol", "current_status", "numeric_or_theorem_value", "units", "accepted_for_scoring"])}

## Zero-Mode Policy Gate

{md_table(all_rows["zero_mode"], ["gate_id", "route", "current_status", "gate_pass", "current_blocker"])}

## Hard Fork Decision

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "owner_contract": owner_contract_rows(),
        "route_triage": route_triage_rows(),
        "coefficients": coefficient_rows(),
        "zero_mode": zero_mode_rows(),
        "decision": decision_rows(),
        "claims": claim_gate_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2951 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
