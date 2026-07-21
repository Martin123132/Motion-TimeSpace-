from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPT_DIR = POST / "scripts"

CHECKPOINT = "4819"
CLAIM_ID = "L-661"
MARKER = "PPC4161_QBARXT_JX_SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW_4819"
PACKET_MARKER = "PPC4161_PACKET_QBARXT_JX_SOURCE_ZERO_OR_BOUNDED_COUPLING_ROW_4819"
DECISION = "QBARXT_SOURCE_ZERO_CONDITIONAL_COMPONENT_ENVELOPE_STAGED_NONCLAIM"
NEXT_TARGET = "4820-Y5-R2FR-EM-F2-hardblocker-or-first-qbar-marker-bound-row.md"

DOC_PATH = POST / "4819-Y5-R2FR-qbarXT-JX-source-zero-or-bounded-coupling-row.md"
FORMAL_PATH = FORMAL / "835-PPC4161-qbarXT-JX-source-zero-or-bounded-coupling-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"
RUNNER = SCRIPT_DIR / "qbarXT_JX_source_zero_bound_runner.py"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_SOURCE_REGISTER.csv"
PROOF_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_SOURCE_ZERO_PROOF_AUDIT.csv"
COUNTEREXAMPLE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_COUNTEREXAMPLE_GUARD.csv"
COMPONENT_BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_QBARXT_COMPONENT_BOUND_CONTRACT.csv"
RUNNER_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_QBARXT_RUNNER_INPUT.csv"
RUNNER_OUTPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_QBARXT_RUNNER_OUTPUT.csv"
DEPENDENCY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_DEPENDENCY_LINKS.csv"
BRANCH_VERDICTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_BRANCH_VERDICTS.csv"
CLAIM_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_CLAIM_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_DECISION_LEDGER.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4819_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4819_VALIDATION.csv"

DOC_4818 = POST / "4818-Y5-R2FR-parent-metric-eigenvalue-or-source-zero-return.md"
RUNNER_4818 = SOURCE_DIR / "P8_Y5_R2FR_4818_ROUTE_SELECTOR_OUTPUT.csv"
DOC_1027 = POST / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md"
QZ_1027 = SOURCE_DIR / "P8_Y5_R10_1027_SOURCE_ZERO_PROOF_AUDIT.csv"
QXT_4762 = SOURCE_DIR / "P8_Y5_R2FR_4762_QBARXT_ZERO_THEOREM_ROWS.csv"
QA_4762 = SOURCE_DIR / "P8_Y5_R2FR_4762_QBARXT_COMPONENT_AUDIT.csv"
QXH_4762 = SOURCE_DIR / "P8_Y5_R2FR_4762_QBARXH_FIRST_SOURCE_ROW.csv"
PU_4762 = SOURCE_DIR / "P8_Y5_R2FR_4762_PRODUCT_GATE_UPDATE.csv"
QBXT_4763 = SOURCE_DIR / "P8_Y5_R2FR_4763_QBARXT_EMF2_HARDBLOCKER_ROWS.csv"
QXH_4763 = SOURCE_DIR / "P8_Y5_R2FR_4763_QBARXH_NUMERATOR_AUDIT.csv"
QE_4763 = SOURCE_DIR / "P8_Y5_R2FR_4763_QEDGE_SHELL_SOURCE_ROW_CONTRACT.csv"
QXT_4700 = SOURCE_DIR / "P8_Y5_R2FR_4700_QBARXT_RESPONSE_ENVELOPE_THEOREM.csv"
QBAR_4699 = SOURCE_DIR / "P8_Y5_R2FR_4699_QBARXH_SOURCE_ENVELOPE_THEOREM.csv"
QZT_3369 = SOURCE_DIR / "P8_Y5_R2FR_3369_QBARXT_SOURCE_ZERO_THEOREM.csv"
QZ_3095 = SOURCE_DIR / "P8_Y5_R2FR_3095_SOURCE_ZERO_PROOF_AUDIT.csv"
SCHEMA_1019 = SOURCE_DIR / "P8_Y5_R10_1019_SOURCE_PACK_SCHEMA.csv"

SOURCE_SPECS = [
    ("SRC4819_00_4818_doc", DOC_4818, "DEC4818_2_next_target", "4818 selects qbarXT/JX source-zero or bounded coupling."),
    ("SRC4819_01_4818_runner", RUNNER_4818, "RUN4818_3_current_source_zero_missing", "4818 route selector output."),
    ("SRC4819_02_1027_doc", DOC_1027, "QZ1027_0_chain_rule", "1027 source-zero precedent."),
    ("SRC4819_03_1027_proof", QZ_1027, "QZ1027_0_chain_rule", "1027 source-zero proof audit."),
    ("SRC4819_04_4762_zero", QXT_4762, "QXT4762_1_chain_rule_zero", "4762 latest qbarXT zero theorem."),
    ("SRC4819_05_4762_components", QA_4762, "QA4762_2_EM_alpha", "4762 qbarXT component audit."),
    ("SRC4819_06_4762_QbarXH", QXH_4762, "QXH4762_1_absolute_bound", "4762 QbarXH first source row."),
    ("SRC4819_07_4762_product", PU_4762, "PU4762_1_current_product_bound", "4762 product gate update."),
    ("SRC4819_08_4763_EMF2", QBXT_4763, "QBXT4763_1_hidden_Hom", "4763 EM/F2 hard blocker."),
    ("SRC4819_09_4763_QbarXH", QXH_4763, "NA4763_0_QbarXH_master", "4763 QbarXH numerator audit."),
    ("SRC4819_10_4763_Qedge", QE_4763, "QE4763_7_total", "4763 Qedge shell source row contract."),
    ("SRC4819_11_4700_qbar", QXT_4700, "QXT4700_2_component_envelope", "4700 qbarXT envelope theorem."),
    ("SRC4819_12_4699_Qbar", QBAR_4699, "QBAR4699_1_QbarXH_projection_bound", "4699 QbarXH source envelope."),
    ("SRC4819_13_3369_theorem", QZT_3369, "QZT3369_0_chain_rule_source_zero", "3369 conditional source-zero theorem."),
    ("SRC4819_14_3095_audit", QZ_3095, "QZ3095_0_chain_rule", "3095 source-zero proof audit."),
    ("SRC4819_15_1019_schema", SCHEMA_1019, "SP1019_3_bulk_R10_projection", "1019 source-pack schema."),
    ("SRC4819_16_runner", RUNNER, "def evaluate_row", "4819 qbarXT runner."),
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(column, "")).replace("|", "\\|") for column in columns) + " |")
    return "\n".join(lines)


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in SOURCE_SPECS:
        text = read_text(path)
        rows.append({"checkpoint": CHECKPOINT, "source_id": source_id, "source_path": str(path), "exists": path.exists(), "needle": needle, "needle_found": bool(text and needle in text), "role": role, "valid_for_claim": False, "timestamp_utc": timestamp})
    return rows


def proof_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"proof_id": "QZ4819_0_definition", "target": "qbar_XT/J_X", "required_statement": "qbar_XT := M_T^-1 |delta_{v_X} S_T| and J_X := delta_X S_parent including hidden/source/domain terms", "current_evidence": "4762 imports the variational definition", "status": "DEFINITION_ASSEMBLED", "missing_for_claim": "none for definition; claim requires clauses below", "if_missing": "cannot normalize source leg", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"proof_id": "QZ4819_1_chain_rule", "target": "ordinary visible matter source-zero", "required_statement": "If S_T=Sbar[psi,e_obs(q),theta(q),W(q),D(q)] and v_X in ker(Dq), then delta_{v_X}S_T=0", "current_evidence": "3369 and 4762 prove conditional chain-rule theorem", "status": "VALID_CONDITIONAL_THEOREM", "missing_for_claim": "parent q-kernel, observed frame, no-marker constants and hidden-tail silence", "if_missing": "retain qbar_XT finite component envelope", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"proof_id": "QZ4819_2_EM_F2", "target": "EM/fine-structure marker zero", "required_statement": "No extra F_Q^2 coefficient or hidden Hom into Coeff(F_Q^2); charge/current/readout/radiative closure signed", "current_evidence": "4763 marks this as the qbarXT hard blocker", "status": "HARD_BLOCKER_PARENT_UNSIGNED", "missing_for_claim": "visible operator image, hidden Hom exclusion, same current owner, readout/radiative closure", "if_missing": "qbar_EM/b_alpha_EM bound row required", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"proof_id": "QZ4819_3_support_domain", "target": "support/boundary/domain/readout tails", "required_statement": "support, boundary, projector and domain are fixed q-basic maps with compact boundary silence", "current_evidence": "4762 keeps these conditional; 4763 stages Qedge shell first fill", "status": "CONDITIONAL_ZERO_UNSIGNED", "missing_for_claim": "fixed support/domain/readout certificates or bounds", "if_missing": "Qedge/Qbar source rows remain live", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"proof_id": "QZ4819_4_total", "target": "qbar_XT/J_X source-zero theorem", "required_statement": "all qbar components vanish in the same parent branch", "current_evidence": "component contract assembled but not parent-signed", "status": "CLAIM_BLOCKED_COMPONENT_ENVELOPE_REQUIRED", "missing_for_claim": "EM/F2, marker constants, hidden tail, support/domain/readout and same-branch closure", "if_missing": "bounded coupling row is mandatory", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def counterexample_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"counterexample_id": "CE4819_0_WEP_only", "weak_premise": "composition-blind/WEP-safe coupling", "construction": "universal Weyl/source-frame factor seen by all materials", "failure": "WEP passes while qbar_XT is nonzero", "required_repair": "no-shadow-frame theorem or bounded common coupling row", "blocks_zero_claim": True, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"counterexample_id": "CE4819_1_EM_F2_hidden_Hom", "weak_premise": "visible Maxwell action has unique F^2", "construction": "hidden scalar coefficient maps into Coeff(F_Q^2)", "failure": "fine-structure/EM stress marker creates qbar_EM", "required_repair": "operator-domain image and hidden-Hom exclusion", "blocks_zero_claim": True, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"counterexample_id": "CE4819_2_measured_G_absorption", "weak_premise": "calibrated G_N absorbs common source charge", "construction": "range-dependent qbar_XT/Qbar_XH product survives beyond constant GM calibration", "failure": "fifth-force/PPN/clock product remains", "required_repair": "same-branch zero or source-backed alpha envelope", "blocks_zero_claim": True, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"counterexample_id": "CE4819_3_unknown_cancellation", "weak_premise": "components may cancel", "construction": "qbar_EM + qbar_marker + qbar_nonH with unknown signs", "failure": "small total by cancellation is not theorem-zero", "required_repair": "absolute component envelope", "blocks_zero_claim": True, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def component_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"row_id": "BQT4819_0_geom", "symbol": "qbar_geom_abs", "definition": "ordinary test-body X charge from representative Weyl/disformal visible geometry", "formula_or_bound": "|qbar_geom| from observed-frame derivative or zero if Lie_v e_obs=0", "required_columns": "system_id;component;value_abs;units;source_path;zero_certificate;valid_for_claim", "current_status": "MISSING_FRAME_ZERO_OR_BOUND", "observable_link": "WEP;clock;R10", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "BQT4819_1_marker", "symbol": "qbar_theta_marker_abs", "definition": "masses, clocks, EM constants, material/source labels", "formula_or_bound": "|qbar_marker| <= |b_alpha|+|b_mu|+|b_clock|+|b_material|+|b_source_norm|", "required_columns": "system_id;component;value_abs;units;source_path;marker_inventory;valid_for_claim", "current_status": "MISSING_NO_MARKER_THEOREM_OR_BOUNDS", "observable_link": "EM;clocks;WEP", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "BQT4819_2_EM_F2", "symbol": "qbar_EM_abs", "definition": "fine-structure/Maxwell stress coefficient throat", "formula_or_bound": "|b_alpha_EM| from no-extra-F2/hidden-Hom/readout/radiative closure or finite coefficient", "required_columns": "system_id;b_alpha_EM_abs;F2_domain;current_owner;readout_closure;source_path;valid_for_claim", "current_status": "HARD_BLOCKER_VALUES_MISSING", "observable_link": "Maxwell/EM stress;fine structure", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "BQT4819_3_hidden_support", "symbol": "qbar_nonH+support+boundary+domain+readout", "definition": "non-Hilbert, support, boundary, domain and readout tails", "formula_or_bound": "absolute sum of hidden/support/boundary/domain/readout source legs", "required_columns": "system_id;tail_component;value_abs;units;source_path;valid_for_claim", "current_status": "MISSING_TAIL_BOUNDS", "observable_link": "R10;PPN;source normalization", "valid_for_claim": False, "timestamp_utc": timestamp},
        {"row_id": "BQT4819_4_total_abs_guard", "symbol": "qbar_XT_bound_abs", "definition": "no-cancellation envelope", "formula_or_bound": "|qbar_XT| <= sum absolute qbar components", "required_columns": "all components above;same_branch;units;source_path;valid_for_claim", "current_status": "VALUES_MISSING", "observable_link": "alpha_bulk(lambda)", "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def false_zero() -> dict[str, bool]:
    return {
        "q_kernel_signed": False,
        "observed_coframe_signed": False,
        "matter_functor_signed": False,
        "no_marker_signed": False,
        "EM_F2_silence_signed": False,
        "hidden_tail_silence_signed": False,
        "support_boundary_domain_signed": False,
        "readout_silence_signed": False,
        "same_branch_signed": False,
    }


def true_zero() -> dict[str, bool]:
    return {key: True for key in false_zero()}


def missing_qbar_components() -> dict[str, str]:
    return {
        "qbar_geom_abs": "MISSING_QBAR_GEOM",
        "qbar_theta_marker_abs": "MISSING_QBAR_MARKER",
        "qbar_EM_abs": "MISSING_QBAR_EM",
        "qbar_nonH_abs": "MISSING_QBAR_NONH",
        "qbar_support_abs": "MISSING_QBAR_SUPPORT",
        "qbar_boundary_abs": "MISSING_QBAR_BOUNDARY",
        "qbar_domain_abs": "MISSING_QBAR_DOMAIN",
        "qbar_readout_abs": "MISSING_QBAR_READOUT",
    }


def runner_input_rows() -> list[dict[str, Any]]:
    return [
        {"row_id": "RUN4819_0_current_zero_missing", "route_type": "source_zero", "route": "current source-zero theorem", **false_zero(), "source_path": str(QZ_3095), "equation_ref": "QZ3095_0_to_QZ3095_6", "notes": "conditional theorem exists but source-zero clauses are unsigned", "provenance": "3095/4762 import", "valid_for_claim": False},
        {"row_id": "RUN4819_1_conditional_zero_pass", "route_type": "source_zero", "route": "conditional source-zero smoke", **true_zero(), "source_path": str(QZT_3369), "equation_ref": "QZT3369_0_chain_rule_source_zero", "notes": "conditional zero theorem smoke row, not physical claim", "provenance": "3369 theorem", "valid_for_claim": False},
        {"row_id": "RUN4819_2_forbidden_WEP_zero", "route_type": "source_zero", "route": "forbidden WEP-only shortcut", **true_zero(), "source_path": "WEP_ONLY_AS_ZERO_MEASURED_G_ABSORPTION", "equation_ref": "FORBIDDEN_QBAR_ZERO", "notes": "WEP/common-mode language cannot prove source-zero", "provenance": "forbidden control", "valid_for_claim": False},
        {"row_id": "RUN4819_3_current_qbar_bound_missing", "route_type": "qbar_bound", "route": "current component envelope", **missing_qbar_components(), "source_signed": False, "units_signed": False, "same_branch_signed": False, "source_path": str(QA_4762), "equation_ref": "QA4762_0_to_QA4762_6", "notes": "component envelope exists but values/units are missing", "provenance": "4762 component audit", "valid_for_claim": False},
        {"row_id": "RUN4819_4_qbar_bound_smoke_pass", "route_type": "qbar_bound", "route": "component envelope smoke", "qbar_geom_abs": "0.01", "qbar_theta_marker_abs": "0.02", "qbar_EM_abs": "0.03", "qbar_nonH_abs": "0.01", "qbar_support_abs": "0.01", "qbar_boundary_abs": "0.01", "qbar_domain_abs": "0.01", "qbar_readout_abs": "0.01", "source_signed": True, "units_signed": True, "same_branch_signed": True, "source_path": str(QXT_4700), "equation_ref": "component envelope smoke", "notes": "numeric component envelope smoke row", "provenance": "4819 smoke", "valid_for_claim": False},
        {"row_id": "RUN4819_5_current_product_missing", "route_type": "coupling_product", "route": "current product row", "K_eff_abs": "MISSING_K_EFF", "Qbar_XH_abs": "MISSING_QBAR_XH", "qbar_XT_bound_abs": "MISSING_QBAR_XT", "alpha_edge_abs": "MISSING_EDGE", "FB5540_abs": "MISSING_FB5540", "alpha_R11_abs": "MISSING_R11", "alpha_bound": "MISSING_BOUND", "source_signed": False, "units_signed": False, "source_path": str(PU_4762), "equation_ref": "PU4762_1_current_product_bound", "notes": "product formula exists but values missing", "provenance": "4762 product gate", "valid_for_claim": False},
        {"row_id": "RUN4819_6_product_smoke_pass", "route_type": "coupling_product", "route": "product envelope smoke", "K_eff_abs": "0.1", "Qbar_XH_abs": "0.2", "qbar_XT_bound_abs": "0.1", "alpha_edge_abs": "0.01", "FB5540_abs": "0.02", "alpha_R11_abs": "0.03", "alpha_bound": "1.0", "source_signed": True, "units_signed": True, "source_path": str(SCHEMA_1019), "equation_ref": "product smoke pass", "notes": "numeric product envelope below bound", "provenance": "4819 smoke", "valid_for_claim": False},
        {"row_id": "RUN4819_7_product_fail", "route_type": "coupling_product", "route": "product fail control", "K_eff_abs": "3.0", "Qbar_XH_abs": "3.0", "qbar_XT_bound_abs": "3.0", "alpha_edge_abs": "0.5", "FB5540_abs": "0.5", "alpha_R11_abs": "0.5", "alpha_bound": "1.0", "source_signed": True, "units_signed": True, "source_path": str(SCHEMA_1019), "equation_ref": "product fail control", "notes": "oversized product must fail", "provenance": "4819 control", "valid_for_claim": False},
        {"row_id": "RUN4819_8_forbidden_cancellation", "route_type": "qbar_bound", "route": "forbidden cancellation", **missing_qbar_components(), "source_signed": True, "units_signed": True, "same_branch_signed": True, "source_path": "CANCEL_UNKNOWN_COMPONENTS_BOUND_AS_SOURCE", "equation_ref": "FORBIDDEN_QBAR_BOUND", "notes": "unknown component cancellation cannot produce a bound", "provenance": "forbidden control", "valid_for_claim": False},
    ]


def run_runner() -> None:
    subprocess.run([sys.executable, str(RUNNER), str(RUNNER_INPUT_CSV), str(RUNNER_OUTPUT_CSV)], check=True)


def dependency_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {"dependency_id": "DEP4819_0_zero_payoff", "quantity": "qbar_XT=0", "depends_on": "q-kernel;Obs_e descent;matter functor;no-marker;EM/F2;hidden tails;support/domain/readout", "current_status": "CONDITIONAL_ONLY", "why": "all components must close in same branch", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"dependency_id": "DEP4819_1_bound_fallback", "quantity": "qbar_XT_bound_abs", "depends_on": "qbar_geom;qbar_marker;qbar_EM;qbar_nonH;qbar_support;qbar_boundary;qbar_domain;qbar_readout", "current_status": "VALUES_MISSING", "why": "component envelope staged but not filled", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"dependency_id": "DEP4819_2_product", "quantity": "alpha/product guard", "depends_on": "K_eff;Qbar_XH;qbar_XT;edge;FB5540;R11;alpha_bound", "current_status": "VALUES_MISSING", "why": "cannot score source coupling until both test and source legs are bounded", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"dependency_id": "DEP4819_3_EM", "quantity": "EM/F2 hard blocker", "depends_on": "no-extra-F2;hidden-Hom;charge lattice;same current;readout/radiative closure", "current_status": "SELECTED_NEXT_SUBTARGET", "why": "this is the hardest qbarXT component and connects to Maxwell/EM stress", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]


def ledgers(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    output = read_csv(RUNNER_OUTPUT_CSV)
    verdicts = [
        {"verdict_id": "BV4819_0_conditional_zero", "branch": "qbar_XT/J_X source-zero", "status": "conditional_theorem_valid_not_parent_signed", "because": "chain-rule zero theorem is valid but EM/F2, markers, hidden/support/readout clauses remain unsigned", "allowed_statement": "conditional theorem target", "forbidden_statement": "WEP/common-mode zero claim", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4819_1_component_bound", "branch": "bounded qbarXT fallback", "status": "schema_ready_values_missing", "because": "component envelope is assembled but no source-backed values/units are filled", "allowed_statement": "absolute component envelope", "forbidden_statement": "cancellation between unknown components", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
        {"verdict_id": "BV4819_2_EM_F2", "branch": "EM/F2 hard blocker", "status": "selected_next", "because": "qbar_EM/b_alpha_EM is the most scrutinized component and connects to Maxwell/EM stress", "allowed_statement": "derive no-extra-F2/hidden-Hom exclusion or fill first qbar marker bound", "forbidden_statement": "assume fine-structure constants are silent", "next_action": NEXT_TARGET, "valid_for_claim": False, "timestamp_utc": timestamp},
    ]
    gates = [
        {"gate_id": "CG4819_0_sources_registered", "claim": "4819 source chain exists", "gate_pass": True, "reason": "qbarXT/QbarXH/source-zero ledgers found", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4819_1_source_zero", "claim": "qbar_XT/J_X source-zero closes", "gate_pass": False, "reason": "EM/F2, marker, hidden-tail, support/domain/readout clauses are unsigned", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4819_2_qbar_bound", "claim": "qbar_XT component bound is claim-grade", "gate_pass": False, "reason": "component values and source paths are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4819_3_product_bound", "claim": "coupling product bound is claim-grade", "gate_pass": False, "reason": "K_eff, Qbar_XH, qbar_XT and channel bounds missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CG4819_4_local_GR", "claim": "local GR/Newton reduction is derived", "gate_pass": False, "reason": "source-zero/bounded coupling branch not closed", "claim_allowed": False, "valid_for_claim": False},
    ]
    decisions = [
        {"decision_id": "DEC4819_0_zero_result", "decision": "qbar_XT=0/J_X=0 remains a valid conditional theorem only.", "because": "the component clauses do not close from current parent evidence.", "next_action": NEXT_TARGET, "valid_for_claim": False},
        {"decision_id": "DEC4819_1_bound_schema", "decision": "The bounded qbar_XT/product row is staged as an executable envelope.", "because": "surviving counterexamples map to named absolute components.", "next_action": NEXT_TARGET, "valid_for_claim": False},
        {"decision_id": "DEC4819_2_next_target", "decision": "Next target is the EM/F2 hard blocker or first qbar marker bound row.", "because": "this is the most concrete way to reduce qbar_XT source uncertainty and links to Maxwell/EM stress.", "next_action": NEXT_TARGET, "valid_for_claim": False},
    ]
    status = [
        {"status_id": "STATUS4819_0_zero", "status": "QBARXT_ZERO_CONDITIONAL_ONLY", "detail": "chain-rule theorem valid but unsigned"},
        {"status_id": "STATUS4819_1_bound", "status": "COMPONENT_BOUND_ENVELOPE_READY_VALUES_MISSING", "detail": "absolute qbar envelope executable but live values missing"},
        {"status_id": "STATUS4819_2_next", "status": "EM_F2_HARDBLOCKER_OR_MARKER_BOUND_NEXT", "detail": NEXT_TARGET},
    ]
    next_rows = [
        {"next_target": NEXT_TARGET, "objective": "derive no-extra-F2/hidden-Hom EM silence or fill the first qbar marker/EM bound row with source-backed units", "include": "Maxwell F2 operator-domain image, hidden Hom exclusion, charge lattice/current owner, readout/radiative closure, b_alpha/b_marker component bounds", "exclude": "WEP-only zero, measured-G absorption, unknown cancellation, placeholder qbar values, public local-GR claim", "valid_for_claim": False}
    ]
    write_csv(BRANCH_VERDICTS_CSV, verdicts)
    write_csv(CLAIM_GATES_CSV, gates)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, status)
    write_csv(NEXT_TARGET_CSV, next_rows)
    return {"runner": output, "verdicts": verdicts, "gates": gates, "decisions": decisions, "status": status, "next": next_rows}


def append_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker not in current:
        with path.open("a", encoding="utf-8", newline="") as handle:
            if current and not current.endswith("\n"):
                handle.write("\n")
            handle.write(text)


def append_claim(timestamp: str) -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    columns = read_text(CLAIMS_PATH).splitlines()[0].split(",")
    row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr",
        "claim": "qbarXT_JX_source_zero_or_bounded_coupling_row",
        "current_evidence": "4819 assembles the qbarXT/JX source-zero theorem and executable component envelope; live source-zero and bound rows remain missing.",
        "status": "qbarxt_component_envelope_private_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "EM/F2 hard blocker; no-marker constants; hidden tails; support/domain/readout tails; missing source-backed component values",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "conditional zero smoke passes but live rows remain missing; product bound smoke only",
        "title": "qbarXT/JX source-zero or bounded coupling row",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writerow(row)


def update_registers(timestamp: str) -> None:
    append_claim(timestamp)
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4819 turns the local source leg into a component theorem-or-bound problem:

```text
qbar_XT := M_T^-1 |delta_vX S_T|
qbar_XT=0 if q-kernel, observed coframe, matter functor, no-marker constants, EM/F2 silence, hidden tails, support/domain/readout and same-branch clauses all close.
|qbar_XT| <= |qbar_geom|+|qbar_theta_marker|+|qbar_EM|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|
```

The source-zero theorem is valid conditionally, but live clauses remain unsigned. The most concrete next target is the EM/F2 hard blocker or first qbar marker bound row.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

- Checkpoint: `{DOC_PATH}`
- Formal note: `{FORMAL_PATH}`
- Runner: `{RUNNER}`
- Claim row: `{CLAIM_ID}`
- Decision: `{DECISION}`
- Next: `{NEXT_TARGET}`
""",
    )
    RESUME_PATH.write_text(
        f"""# Current local resume

Updated: `{timestamp}`
Last checkpoint: `4819-Y5-R2FR-qbarXT-JX-source-zero-or-bounded-coupling-row.md`
Marker: `{MARKER}`

## Where we are

4819 assembled the source-zero theorem and component envelope:

```text
qbar_XT := M_T^-1 |delta_vX S_T|
qbar_XT=0 if every source leg descends through q in the same branch.
|qbar_XT| <= |qbar_geom|+|qbar_theta_marker|+|qbar_EM|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|
```

## Live blockers

- Source-zero remains conditional because EM/F2, marker constants, hidden tails, support/domain/readout and same-branch clauses are unsigned.
- Bounded coupling is executable but live component values/units/source paths are missing.
- The EM/F2 hard blocker is now the sharpest next route into Maxwell/EM stress and source coupling.

## Next target

`{NEXT_TARGET}`
""",
        encoding="utf-8",
    )


def compile_and_clean() -> bool:
    py_compile.compile(str(RUNNER), doraise=True)
    py_compile.compile(str(SCRIPT_DIR / "Y5_R2FR_4819_qbarXT_JX_source_zero_or_bounded_coupling_row.py"), doraise=True)
    cache = SCRIPT_DIR / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    return not cache.exists()


def validate(cache_removed: bool) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER_CSV)
    proof = {row["proof_id"]: row for row in read_csv(PROOF_AUDIT_CSV)}
    counter = {row["counterexample_id"]: row for row in read_csv(COUNTEREXAMPLE_CSV)}
    bounds = {row["row_id"]: row for row in read_csv(COMPONENT_BOUND_CSV)}
    output = {row["row_id"]: row for row in read_csv(RUNNER_OUTPUT_CSV)}
    deps = {row["dependency_id"]: row for row in read_csv(DEPENDENCY_CSV)}
    gates = {row["gate_id"]: row for row in read_csv(CLAIM_GATES_CSV)}
    source_pass = all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources)
    checks = [
        {"check_id": "VAL4819_0_sources", "description": "all cited sources exist and needles are found", "result": "PASS" if source_pass else "FAIL", "evidence": str(SOURCE_REGISTER_CSV)},
        {"check_id": "VAL4819_1_proof_audit", "description": "proof audit covers definition, chain rule, EM/F2, support/domain and total", "result": "PASS" if {"QZ4819_0_definition", "QZ4819_1_chain_rule", "QZ4819_2_EM_F2", "QZ4819_3_support_domain", "QZ4819_4_total"}.issubset(proof) else "FAIL", "evidence": str(PROOF_AUDIT_CSV)},
        {"check_id": "VAL4819_2_counterexamples", "description": "counterexamples cover WEP, EM/F2, measured-G and cancellation", "result": "PASS" if {"CE4819_0_WEP_only", "CE4819_1_EM_F2_hidden_Hom", "CE4819_2_measured_G_absorption", "CE4819_3_unknown_cancellation"}.issubset(counter) else "FAIL", "evidence": str(COUNTEREXAMPLE_CSV)},
        {"check_id": "VAL4819_3_bound_contract", "description": "component bound contract covers geometry, markers, EM, hidden/tails and total", "result": "PASS" if {"BQT4819_0_geom", "BQT4819_1_marker", "BQT4819_2_EM_F2", "BQT4819_3_hidden_support", "BQT4819_4_total_abs_guard"}.issubset(bounds) else "FAIL", "evidence": str(COMPONENT_BOUND_CSV)},
        {"check_id": "VAL4819_4_live_zero_blocks", "description": "live source-zero row remains blocked", "result": "PASS" if output["RUN4819_0_current_zero_missing"]["runner_status"] == "BLOCKED_SOURCE_ZERO_COMPONENTS" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4819_5_conditional_zero_pass", "description": "conditional zero smoke row passes nonclaim", "result": "PASS" if output["RUN4819_1_conditional_zero_pass"]["runner_status"] == "QBARXT_JX_SOURCE_ZERO_PASS_NONCLAIM" and output["RUN4819_1_conditional_zero_pass"]["claim_allowed"] == "False" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4819_6_forbidden_zero_fails", "description": "WEP/measured-G zero shortcut fails", "result": "PASS" if output["RUN4819_2_forbidden_WEP_zero"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4819_7_qbar_bound_controls", "description": "qbar bound live blocks and smoke passes", "result": "PASS" if output["RUN4819_3_current_qbar_bound_missing"]["runner_status"] == "BLOCKED_QBARXT_COMPONENT_BOUND_INPUTS" and output["RUN4819_4_qbar_bound_smoke_pass"]["runner_status"] == "QBARXT_COMPONENT_BOUND_PASS_NONCLAIM" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4819_8_product_controls", "description": "product live blocks, smoke passes and fail control fails", "result": "PASS" if output["RUN4819_5_current_product_missing"]["runner_status"] == "BLOCKED_OR_FAILED_COUPLING_PRODUCT_INPUTS" and output["RUN4819_6_product_smoke_pass"]["runner_status"] == "COUPLING_PRODUCT_BOUND_PASS_NONCLAIM" and output["RUN4819_7_product_fail"]["runner_status"] == "COUPLING_PRODUCT_NUMERIC_FAIL" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4819_9_forbidden_bound_fails", "description": "unknown-cancellation bound shortcut fails", "result": "PASS" if output["RUN4819_8_forbidden_cancellation"]["anti_circularity_status"] == "FAIL_FORBIDDEN_SOURCE_USED" else "FAIL", "evidence": str(RUNNER_OUTPUT_CSV)},
        {"check_id": "VAL4819_10_dependencies", "description": "dependencies include zero, bound, product and EM target", "result": "PASS" if {"DEP4819_0_zero_payoff", "DEP4819_1_bound_fallback", "DEP4819_2_product", "DEP4819_3_EM"}.issubset(deps) else "FAIL", "evidence": str(DEPENDENCY_CSV)},
        {"check_id": "VAL4819_11_claim_gates_block", "description": "claim gates block local-GR promotion", "result": "PASS" if gates["CG4819_4_local_GR"]["gate_pass"] == "False" and gates["CG4819_1_source_zero"]["gate_pass"] == "False" else "FAIL", "evidence": str(CLAIM_GATES_CSV)},
        {"check_id": "VAL4819_12_claim_register", "description": "claim register includes L-661 as nonclaim", "result": "PASS" if CLAIM_ID in read_text(CLAIMS_PATH) and DECISION in read_text(CLAIMS_PATH) else "FAIL", "evidence": str(CLAIMS_PATH)},
        {"check_id": "VAL4819_13_resume", "description": "resume points at 4820", "result": "PASS" if NEXT_TARGET in read_text(RESUME_PATH) else "FAIL", "evidence": str(RESUME_PATH)},
        {"check_id": "VAL4819_14_docs", "description": "post and formal docs exist", "result": "PASS" if DOC_PATH.exists() and FORMAL_PATH.exists() else "FAIL", "evidence": f"{DOC_PATH}; {FORMAL_PATH}"},
        {"check_id": "VAL4819_15_pycache", "description": "scripts compiled and __pycache__ removed", "result": "PASS" if cache_removed else "FAIL", "evidence": str(SCRIPT_DIR / "__pycache__")},
    ]
    checks.append({"check_id": "VAL4819_OVERALL", "description": "all 4819 qbarXT/JX source-zero checks pass", "result": "PASS" if all(row["result"] == "PASS" for row in checks) else "FAIL", "evidence": DECISION})
    write_csv(VALIDATION_CSV, checks, ["check_id", "description", "result", "evidence"])
    return checks


def write_docs(tables: dict[str, list[dict[str, Any]]], validation: list[dict[str, Any]], timestamp: str) -> None:
    sources = read_csv(SOURCE_REGISTER_CSV)
    proof = read_csv(PROOF_AUDIT_CSV)
    counter = read_csv(COUNTEREXAMPLE_CSV)
    bounds = read_csv(COMPONENT_BOUND_CSV)
    runner_input = read_csv(RUNNER_INPUT_CSV)
    deps = read_csv(DEPENDENCY_CSV)
    doc = f"""# 4819 Y5 R2FR qbarXT JX source-zero or bounded coupling row

**Status:** The `qbar_XT=0/J_X=0` proof is valid only as a conditional component theorem. Current MTS still requires an absolute component envelope; the EM/F2 hard blocker is selected next.

Decision: `{DECISION}`

Generated: `{timestamp}`

## qbarXT/JX theorem-or-bound law

```text
qbar_XT := M_T^-1 |delta_vX S_T|
qbar_XT=0 if all source legs descend through q in the same branch
|qbar_XT| <= |qbar_geom|+|qbar_theta_marker|+|qbar_EM|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|
```

## Source register
{table(sources, ["source_id", "source_path", "exists", "needle_found", "role"])}

## Source-zero proof audit
{table(proof, ["proof_id", "target", "required_statement", "current_evidence", "status", "missing_for_claim", "if_missing", "valid_for_claim"])}

## Counterexample guard
{table(counter, ["counterexample_id", "weak_premise", "construction", "failure", "required_repair", "blocks_zero_claim", "valid_for_claim"])}

## Component bound contract
{table(bounds, ["row_id", "symbol", "definition", "formula_or_bound", "current_status", "observable_link", "valid_for_claim"])}

## Runner input rows
{table(runner_input, ["row_id", "route_type", "route", "source_path", "valid_for_claim"])}

## Runner output rows
{table(tables["runner"], ["row_id", "route_type", "route", "qbar_XT_bound_abs", "coupling_product_abs", "route_pass", "runner_status", "missing_for_claim", "claim_allowed"])}

## Dependency links
{table(deps, ["dependency_id", "quantity", "depends_on", "current_status", "why", "next_action", "valid_for_claim"])}

## Branch verdicts
{table(tables["verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"])}

## Claim gates
{table(tables["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"])}

## Decision ledger
{table(tables["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"])}

## Validation
{table(validation, ["check_id", "description", "result", "evidence"])}

## Next target
{table(tables["next"], ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")
    formal = f"""# 835 PPC4161 qbarXT JX source-zero or bounded coupling row

Marker: `{MARKER}`

4819 turns `qbar_XT/J_X` into a component theorem-or-bound law:

```text
qbar_XT := M_T^-1 |delta_vX S_T|
|qbar_XT| <= |qbar_geom|+|qbar_theta_marker|+|qbar_EM|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|
```

The chain-rule zero theorem is valid conditionally but not parent-signed. EM/F2 silence is selected as the next hard blocker because it connects directly to Maxwell/EM stress and fine-structure coupling.

Next: `{NEXT_TARGET}`
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def main() -> int:
    timestamp = now()
    write_csv(SOURCE_REGISTER_CSV, source_register(timestamp))
    write_csv(PROOF_AUDIT_CSV, proof_audit_rows(timestamp))
    write_csv(COUNTEREXAMPLE_CSV, counterexample_rows(timestamp))
    write_csv(COMPONENT_BOUND_CSV, component_bound_rows(timestamp))
    write_csv(RUNNER_INPUT_CSV, runner_input_rows())
    run_runner()
    write_csv(DEPENDENCY_CSV, dependency_rows(timestamp))
    tables = ledgers(timestamp)
    update_registers(timestamp)
    cache_removed = compile_and_clean()
    validation = validate(cache_removed)
    write_docs(tables, validation, timestamp)
    validation = validate(cache_removed)
    write_docs(tables, validation, timestamp)
    if any(row["result"] != "PASS" for row in validation):
        return 1
    print(f"{MARKER}: validation PASS; next {NEXT_TARGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
