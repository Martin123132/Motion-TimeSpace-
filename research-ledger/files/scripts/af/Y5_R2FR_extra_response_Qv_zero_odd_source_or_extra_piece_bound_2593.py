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

BRANCH_ID = "MTS_R2FR_EXTRA_RESPONSE_QV_2593"
CHECKPOINT_ID = "2593"

DOC = ROOT / "2593-Y5-R2FR-extra-response-Qv-zero-odd-source-or-extra-piece-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_EXTRA_RESPONSE_QV_2593_SOURCE_REGISTER.csv",
    "zero_odd_audit": OUT / "P8_Y5_EXTRA_RESPONSE_QV_2593_ZERO_ODD_SOURCE_AUDIT.csv",
    "bound_rows": OUT / "P8_Y5_EXTRA_RESPONSE_QV_2593_BOUND_ROWS.csv",
    "runner_refusal": OUT / "P8_Y5_EXTRA_RESPONSE_QV_2593_RUNNER_REFUSAL.csv",
    "claim_gates": OUT / "P8_Y5_EXTRA_RESPONSE_QV_2593_CLAIM_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_EXTRA_RESPONSE_QV_2593_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_EXTRA_RESPONSE_QV_2593_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_EXTRA_RESPONSE_QV_2593_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2593_VALIDATION.csv",
}

COPY_TARGETS = {
    "zero_odd_audit": QUEUE / "JR2593_EXTRA_RESPONSE_ZERO_ODD_AUDIT_NONCLAIM.csv",
    "bound_rows": LOCAL_BOUNDS / "Extra_response_Qv_bound_rows_2593_NONCLAIM.csv",
    "next_target": QUEUE / "JR2593_SOURCE_NORMALIZATION_Y5_NEXT.csv",
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
            "source_id": "SRC2593_00_2592_handoff",
            "source_path": ROOT / "2592-Y5-R2FR-non-EH-sector-Qv-zero-priority-gate-or-source-pack.md",
            "needles": ["NEXT2592_0_selected", "ZNE2592_1_extra_response", "VAL2592_OVERALL"],
            "role": "active handoff selecting extra/response Qv zero-odd-source target",
        },
        {
            "source_id": "SRC2593_01_2592_next_queue",
            "source_path": QUEUE / "JR2592_EXTRA_RESPONSE_QV_ZERO_ODD_SOURCE_NEXT.csv",
            "needles": ["NEXT2592_0_selected", "2593-Y5-R2FR-extra-response-Qv-zero-odd-source-or-extra-piece-bound.md"],
            "role": "machine-readable 2593 task and guardrails",
        },
        {
            "source_id": "SRC2593_02_response_contract_csv",
            "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "needles": ["RD516_1_even_scalar_density", "RD516_4_zero_odd_source", "RD516_6_boundary_no_flux"],
            "role": "current response-doublet local-silence contract",
        },
        {
            "source_id": "SRC2593_03_516_doc",
            "source_path": ROOT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
            "needles": ["RD516_4_zero_odd_source", "F516_2_double_zero", "F516_5_local_GR_claim"],
            "role": "Gamma_eff scalar-density owner candidate and double-zero route",
        },
        {
            "source_id": "SRC2593_04_494_doc",
            "source_path": ROOT / "494-exchange-doublet-component-map-or-coefficient-branch.md",
            "needles": ["Y5_source_normalization", "Y6_stress_Bianchi", "V494_4_hard_rows_identified"],
            "role": "exchange-doublet component map and hard Y5/Y6 blockers",
        },
        {
            "source_id": "SRC2593_05_local_action_blocks",
            "source_path": OUT / "P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needles": ["A511_3_extra_field_silence", "A511_6_metric_readout"],
            "role": "minimal local-GR action-block silence/readout requirements",
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


def zero_odd_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "ERZ2593_0_component_map",
            "clause": "full exchange-doublet component map",
            "zero_condition": "Every local leakage component Y0-Y6 maps to exchange-odd parent variables Z^A=(R_+^A-R_-^A)/2",
            "current_status": "PARTIAL_COMPONENT_MAP_ONLY",
            "evidence": "494 maps Y2/Y3 as conditional routes but leaves Y0,Y1,Y4,Y5,Y6 unresolved or retained",
            "blocker": "Y5 source normalization and Y6 extra stress are hard blockers",
        },
        {
            "audit_id": "ERZ2593_1_even_density",
            "clause": "even scalar density",
            "zero_condition": "Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4), so partial_A Gamma_eff|Z=0=0",
            "current_status": "CANDIDATE_WRITTEN_NOT_MATCHED",
            "evidence": "516 writes the quadratic owner candidate and conditional double-zero",
            "blocker": "candidate has not been matched to current MTS variables and K_hat definitions",
        },
        {
            "audit_id": "ERZ2593_2_metric_response",
            "clause": "K_hat metric response",
            "zero_condition": "K_hat^{mu nu}=2/sqrt(-g) delta(sqrt(-g) Gamma_eff)/delta g_mu_nu minus fixed volume convention",
            "current_status": "NOT_CHECKED_CURRENT_MTS",
            "evidence": "516 states the metric-response match is required",
            "blocker": "no sector variation proves existing K_hat equals the metric response of Gamma_eff",
        },
        {
            "audit_id": "ERZ2593_3_positive_operator",
            "clause": "positive self-adjoint operator",
            "zero_condition": "M_AB and derivative operator are positive after gauge/constraint removal on compact local collars",
            "current_status": "FORMAL_CANDIDATE_ONLY",
            "evidence": "516/RD516_3 records positivity as a formal route",
            "blocker": "no operator domain, constraint quotient, boundary condition or eigenvalue proof is supplied",
        },
        {
            "audit_id": "ERZ2593_4_zero_odd_source",
            "clause": "zero exchange-odd local source",
            "zero_condition": "J_Z=0 and B_Z=0 for matter, boundary and source-normalization channels",
            "current_status": "NOT_DERIVED_HARD_BLOCK",
            "evidence": "516/RD516_4 and 494 identify Y5 source-normalization and Y6 stress as hard blockers",
            "blocker": "measured GM/source normalization is naturally exchange-even, and conserved extra stress can survive oddness",
        },
        {
            "audit_id": "ERZ2593_5_PPN_lock",
            "clause": "PPN/local residual lock",
            "zero_condition": "Z^A equals the physical q_loc/PPN residual vector through beta,gamma,alpha_i,xi,Gdot,R11 order",
            "current_status": "NOT_DERIVED",
            "evidence": "516/RD516_5 requires Z^A=Y_loc^A through local gates",
            "blocker": "component map is partial and Y5/Y6 stop the lock",
        },
        {
            "audit_id": "ERZ2593_6_boundary_no_flux",
            "clause": "boundary no-flux",
            "zero_condition": "integrations by parts and boundary metric response carry no compact local force/mass flux",
            "current_status": "OPEN",
            "evidence": "516/RD516_6 leaves boundary no-flux open",
            "blocker": "no fixed-reference boundary theorem or q_loc bound row closes the term",
        },
        {
            "audit_id": "ERZ2593_7_verdict",
            "clause": "extra-response Qv zero",
            "zero_condition": "ERZ2593_0 through ERZ2593_6 pass in the same local branch",
            "current_status": "EXTRA_RESPONSE_QV_ZERO_NOT_PROVED_CURRENT_CORPUS",
            "evidence": "double-zero shape is coherent but current MTS lacks the component map, metric-response, source-zero, PPN-lock and boundary pieces",
            "blocker": "epsilon_Qv_extra_piece remains nonclaim; next target should attack Y5 source normalization first",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "ERB2593_0_component_map",
            "symbol": "epsilon_extra_component_map",
            "definition": "unmapped or unproved Y0-Y6 exchange-doublet components contributing to Q_v^extra",
            "units": "dimensionless component-map defect",
            "current_value": "Y0_Y1_Y4_NOT_DERIVED;Y5_HARD_BLOCK;Y6_RETAINED_DEBT",
            "source_path": ROOT / "494-exchange-doublet-component-map-or-coefficient-branch.md",
            "observable_link": "PPN;R11;Newton;local_GR",
        },
        {
            "row_id": "ERB2593_1_even_density",
            "symbol": "epsilon_extra_even_density_match",
            "definition": "failure of current Gamma_eff to match an even quadratic scalar density with no linear Z term",
            "units": "dimensionless density-matching defect",
            "current_value": "CANDIDATE_WRITTEN_NOT_MATCHED_TO_CURRENT_MTS",
            "source_path": ROOT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
            "observable_link": "q_loc;local_GR;PPN",
        },
        {
            "row_id": "ERB2593_2_metric_response",
            "symbol": "epsilon_Khat_metric_response",
            "definition": "norm(K_hat - metric_response(sqrt(-g) Gamma_eff)) in local branch",
            "units": "stress/metric-response defect",
            "current_value": "MISSING_KHAT_METRIC_RESPONSE_MATCH",
            "source_path": ROOT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
            "observable_link": "Bianchi;conservation;local_GR",
        },
        {
            "row_id": "ERB2593_3_positive_operator",
            "symbol": "epsilon_extra_operator_positivity",
            "definition": "negative/zero unowned modes of M_AB or derivative operator after gauge/constraint quotient",
            "units": "operator gap defect",
            "current_value": "MISSING_OPERATOR_DOMAIN;MISSING_CONSTRAINT_QUOTIENT;MISSING_BOUNDARY_CONDITIONS",
            "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "observable_link": "stability;local_silence",
        },
        {
            "row_id": "ERB2593_4_zero_odd_source",
            "symbol": "epsilon_extra_odd_source",
            "definition": "abs(J_Z)+abs(B_Z) from matter, boundary, source-normalization and extra-stress channels",
            "units": "dimensionless odd-source leakage after normalization",
            "current_value": "Y5_SOURCE_NORMALIZATION_HARD_BLOCK;Y6_EXTRA_STRESS_RETAINED_DEBT",
            "source_path": ROOT / "494-exchange-doublet-component-map-or-coefficient-branch.md",
            "observable_link": "Newton;source_mass;PPN;R11",
        },
        {
            "row_id": "ERB2593_5_PPN_lock",
            "symbol": "epsilon_extra_PPN_lock",
            "definition": "failure of Z^A to equal physical q_loc/PPN residual vector through beta,gamma,alpha_i,xi,Gdot,R11",
            "units": "dimensionless PPN-lock defect",
            "current_value": "MISSING_Z_TO_YLOC_LOCK;MISSING_Y5_Y6_THEOREMS",
            "source_path": ROOT / "516-Gamma-eff-scalar-density-owner-or-q_loc-bound-runner.md",
            "observable_link": "PPN;R11;local_GR",
        },
        {
            "row_id": "ERB2593_6_boundary_flux",
            "symbol": "epsilon_extra_boundary_flux",
            "definition": "compact local boundary force/mass flux from extra-response integrations by parts or metric response",
            "units": "dimensionless boundary-flux leakage",
            "current_value": "MISSING_BOUNDARY_NO_FLUX_THEOREM",
            "source_path": OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "observable_link": "clock;orbital;PPN",
        },
        {
            "row_id": "ERB2593_TOTAL",
            "symbol": "epsilon_Qv_extra_piece",
            "definition": "abs(int_S(Q_v^extra + C_v^extra - i_v Theta_extra))/M_H_ref",
            "units": "dimensionless extra-sector vertical charge",
            "current_value": "COMPONENTS_MISSING",
            "source_path": DOC,
            "observable_link": "PPN;R10;clock;cosmology_branching;local_GR",
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


def runner_refusal_rows(rows_in: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in rows_in:
        reasons = ["VALID_FOR_CLAIM_FALSE", "MISSING_ZERO_THEOREM_OR_NUMERIC_VALUE"]
        if not row["source_path_exists"]:
            reasons.append("MISSING_SOURCE_PATH")
        if row["symbol"] == "epsilon_extra_odd_source":
            reasons.append("Y5_Y6_HARD_BLOCKERS_NOT_CLOSED")
        if row["row_id"] == "ERB2593_TOTAL":
            reasons.append("EXTRA_RESPONSE_COMPONENT_ROWS_NOT_SCORE_READY")
        rows.append(
            with_stamp(
                {
                    "runner_id": f"ERR2593_{row['row_id']}",
                    "target_id": row["row_id"],
                    "symbol": row["symbol"],
                    "verdict": "REFUSED_NONCLAIM_EXTRA_RESPONSE_ROW",
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
            "gate_id": "CG2593_0_double_zero_shape",
            "claim": "quadratic response-doublet shape can give F1=0 conditionally",
            "gate_status": "PASS_CONDITIONAL_SHAPE_ONLY",
            "reason": "if Gamma_eff is even quadratic and Z=0, the linear variation vanishes",
            "gate_pass": True,
        },
        {
            "gate_id": "CG2593_1_current_MTS_owner",
            "claim": "current MTS derives the Gamma_eff owner and K_hat response",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "component map, metric-response match, positive operator and PPN lock are not parent-signed",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2593_2_zero_odd_source",
            "claim": "extra/response odd source is zero",
            "gate_status": "BLOCKED_HARD_NONCLAIM",
            "reason": "Y5 source-normalization and Y6 stress remain explicit hard blockers",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2593_3_extra_Qv_zero",
            "claim": "epsilon_Qv_extra_piece is theorem-zero",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "zero-odd-source, PPN-lock and boundary-no-flux clauses are unsigned",
            "gate_pass": False,
        },
        {
            "gate_id": "CG2593_4_local_GR_Newton",
            "claim": "local GR/Newton follows from the response-doublet route",
            "gate_status": "BLOCKED_NONCLAIM",
            "reason": "2593 only narrows the extra-sector obstruction; it does not close it",
            "gate_pass": False,
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False, "claim_allowed": False}) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2593_0_double_zero_shape_retained",
            "decision": "RESPONSE_DOUBLET_DOUBLE_ZERO_SHAPE_REMAINS_BEST_ROUTE",
            "reason": "an even quadratic Gamma_eff would kill the linear local source if the component map and source-zero clauses close",
            "effect": "keep deriving this route rather than demoting it yet",
        },
        {
            "decision_id": "DEC2593_1_no_extra_zero_claim",
            "decision": "EXTRA_RESPONSE_QV_ZERO_NOT_CLAIMED",
            "reason": "current MTS has not closed component map, K_hat response, positivity, zero odd source, PPN lock or boundary no-flux",
            "effect": "epsilon_Qv_extra_piece remains nonclaim",
        },
        {
            "decision_id": "DEC2593_2_next",
            "decision": "Y5_SOURCE_NORMALIZATION_SELECTED_NEXT",
            "reason": "494 identifies source normalization as the next priority for Newton/GR recovery and it blocks zero odd source directly",
            "effect": "2594 should try to prove measured GM/source normalization is pure even EH plus odd/local-zero non-EH operators, or fill coefficient rows",
        },
    ]
    return [with_stamp({**row, "valid_for_claim": False}) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT2593_0_selected",
            "selection_status": "selected",
            "target_file": "2594-Y5-R2FR-Y5-source-normalization-even-scalar-theorem-or-coefficient-fill.md",
            "target_script": "scripts/Y5_R2FR_Y5_source_normalization_even_scalar_theorem_or_coefficient_fill_2594.py",
            "task": "try to prove measured GM/source normalization is a pure even EH/Hilbert-source object while all non-EH normalization operators are exchange-odd/local-zero or coefficient-bounded",
            "success_condition": "Y5 source-normalization no longer sources J_Z and epsilon_extra_odd_source can drop the Y5 hard blocker",
            "fallback_condition": "fill c_domain_source_normalization_operator and source-normalization coefficient rows with units, source paths and valid_for_claim=false",
            "guardrails": "no Newton/local-GR claim; no fitted GM import; no oddness-by-naming; no total-zero switch; no hidden source cancellation; no GitHub; no formalization-workbench edits",
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
                    "copy_id": f"COPY2593_{copy_id}",
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

    add("VAL2593_00_sources_exist", all(row["source_pass"] is True for row in data["sources"]), "all cited local source paths exist and needles are present")
    required_audits = {"ERZ2593_0_component_map", "ERZ2593_1_even_density", "ERZ2593_2_metric_response", "ERZ2593_3_positive_operator", "ERZ2593_4_zero_odd_source", "ERZ2593_5_PPN_lock", "ERZ2593_6_boundary_no_flux", "ERZ2593_7_verdict"}
    present_audits = {row["audit_id"] for row in data["zero_odd_audit"]}
    add("VAL2593_01_zero_odd_audit_complete", required_audits.issubset(present_audits), "zero-odd-source audit covers every required clause")
    required_symbols = {"epsilon_extra_component_map", "epsilon_extra_even_density_match", "epsilon_Khat_metric_response", "epsilon_extra_operator_positivity", "epsilon_extra_odd_source", "epsilon_extra_PPN_lock", "epsilon_extra_boundary_flux", "epsilon_Qv_extra_piece"}
    present_symbols = {row["symbol"] for row in data["bound_rows"]}
    add("VAL2593_02_bound_rows_present", required_symbols.issubset(present_symbols), "extra-response bound rows are present")
    add("VAL2593_03_bound_sources_exist", all(row["source_path_exists"] is True for row in data["bound_rows"]), "bound rows point to existing local sources")
    add(
        "VAL2593_04_rows_nonclaim",
        all(row["score_ready"] is False and row["valid_for_claim"] is False for row in data["bound_rows"]),
        "extra-response rows remain non-score-ready and nonclaim",
    )
    add(
        "VAL2593_05_runner_refuses",
        all(row["score_ready"] is False and row["claim_allowed"] is False for row in data["runner_refusal"]),
        "runner refuses all unfilled extra-response rows",
    )
    add(
        "VAL2593_06_claim_gates_safe",
        all(row["claim_allowed"] is False for row in data["claim_gates"])
        and any(row["gate_id"] == "CG2593_2_zero_odd_source" and row["gate_status"] == "BLOCKED_HARD_NONCLAIM" for row in data["claim_gates"]),
        "extra-response zero, local-GR and Newton claims remain blocked",
    )
    add("VAL2593_07_no_claim_flags", generated_rows_have_no_claim_flags(data), "no generated row sets valid_for_claim=true or claim_allowed=true")

    formalization_artifacts = []
    if FORMALIZATION.exists():
        for pattern in (
            "*2593-Y5-R2FR-extra-response*",
            "*Y5_R2FR_extra_response_Qv*",
            "*P8_Y5_EXTRA_RESPONSE_QV_2593*",
            "*JR2593*",
        ):
            formalization_artifacts.extend(FORMALIZATION.rglob(pattern))
    add(
        "VAL2593_08_no_formalization_artifacts",
        not formalization_artifacts,
        "no 2593 artifacts were written to formalization-workbench",
        ";".join(str(path) for path in formalization_artifacts),
    )
    add(
        "VAL2593_09_next_selected",
        any(row["route_id"] == "NEXT2593_0_selected" and "2594-Y5-R2FR-Y5-source-normalization" in row["target_file"] for row in data["next"]),
        "2594 Y5 source-normalization target selected next",
    )
    add(
        "VAL2593_10_branch_copies",
        all(row["source_exists"] is True and row["target_exists"] is True for row in data["copies"]),
        "nonclaim branch copies exist",
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed, count, error = csv_parses(path)
        add(f"VAL2593_CSV_{path.stem}", parsed and count > 0, f"CSV parses with {count} rows", error)
    for key, path in COPY_TARGETS.items():
        parsed, count, error = csv_parses(path)
        add(f"VAL2593_COPY_CSV_{key}", parsed and count > 0, f"copy CSV parses with {count} rows", error)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2593_OVERALL",
        overall,
        "2593 keeps the response-doublet double-zero route as a conditional candidate, refuses extra-response Qv zero for current MTS, and selects Y5 source-normalization as the next hard blocker",
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
        "# 2593 Y5 R2FR extra-response Qv zero-odd-source or extra-piece bound",
        "",
        "**Status:** private nonclaim derivation checkpoint. The response-doublet route remains the best-looking route to a local double-zero, but current MTS does not yet prove the extra/response sector has zero vertical `Q_v`.",
        "",
        "**Main result:** a quadratic even `Gamma_eff` can conditionally give `F_1=0`, but the current corpus still has hard blockers: incomplete Y0-Y6 component map, unmatched `K_hat` metric response, formal-only positivity, unproved PPN lock, open boundary no-flux, and especially Y5 source-normalization plus Y6 extra stress. No local-GR/Newton claim is made.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "missing_needles", "source_pass", "role", "valid_for_claim"]),
        "",
        "## Zero-Odd-Source Audit",
        markdown_table(data["zero_odd_audit"], ["audit_id", "clause", "zero_condition", "current_status", "evidence", "blocker", "valid_for_claim", "claim_allowed"]),
        "",
        "## Bound Rows",
        markdown_table(data["bound_rows"], ["row_id", "symbol", "definition", "units", "current_value", "source_path", "source_path_exists", "observable_link", "score_ready", "valid_for_claim", "claim_allowed"]),
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
        "This is still progress, even though it is not a win. The double-zero mechanism is not nonsense; it is a conditional mechanism with named missing signatures. The next real fight is Y5: source normalization. If measured GM can be shown to be pure even EH/Hilbert source while non-EH normalization operators are odd/local-zero or bounded, the extra-response route gets a lot healthier. If not, this route carries a real local residual.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    LOCAL_BOUNDS.mkdir(parents=True, exist_ok=True)

    bound_data = bound_rows()
    data = {
        "sources": source_register_rows(),
        "zero_odd_audit": zero_odd_audit_rows(),
        "bound_rows": bound_data,
        "runner_refusal": runner_refusal_rows(bound_data),
        "claim_gates": claim_gate_rows(),
        "decisions": decision_rows(),
        "next": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["sources"])
    write_csv(OUTPUTS["zero_odd_audit"], data["zero_odd_audit"])
    write_csv(OUTPUTS["bound_rows"], data["bound_rows"])
    write_csv(OUTPUTS["runner_refusal"], data["runner_refusal"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision_ledger"], data["decisions"])
    write_csv(OUTPUTS["next_target"], data["next"])

    data["copies"] = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], data["copies"])

    data["validations"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validations"])
    write_doc(data)

    overall = next(row for row in data["validations"] if row["check_id"] == "VAL2593_OVERALL")
    print(f"{overall['check_id']} {overall['status']}: {overall['notes']}")
    print(f"doc={DOC}")
    print(f"validation={OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
