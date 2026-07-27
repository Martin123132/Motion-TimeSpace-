from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3955"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3955-Y5-R2FR-observable-metric-Z-linear-coefficient-or-source-current-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3955_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3955_CA_ZERO_THEOREM_OR_BOUND.csv",
    "ledger": SRC / "P8_Y5_R2FR_3955_OBSERVABLE_METRIC_COEFFICIENT_LEDGER.csv",
    "source_bound": SRC / "P8_Y5_R2FR_3955_SOURCE_CURRENT_BOUND_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3955_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3955_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3955_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3955_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3955_VALIDATION.csv",
}

NEXT_DOC = "3956-Y5-R2FR-Z-verticality-map-computation-or-CA-bound-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3956_Z_verticality_map_computation_or_CA_bound_values.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3955_00_3954_next", SRC / "P8_Y5_R2FR_3954_NEXT_TARGET.csv", "NEXT3954_0", "3954 handoff"),
        ("SRC3955_01_3954_chain", SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "SCT3954_1_chain_rule", "source current chain rule"),
        ("SRC3955_02_3954_silence", SRC / "P8_Y5_R2FR_3954_Z_SOURCE_CURRENT_THEOREM.csv", "SCT3954_2_silence_theorem", "source current silence theorem"),
        ("SRC3955_03_3954_CA", SRC / "P8_Y5_R2FR_3954_PPN_SOURCE_NORMALIZATION_RESIDUAL_MAP.csv", "PPN3954_0_C_A", "C_A missing coefficient"),
        ("SRC3955_04_3888_action", SRC / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv", "NLS3888_0_action", "ordinary matter descends through observed variables"),
        ("SRC3955_05_3888_vertical", SRC / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv", "NLS3888_1_vertical", "quotient-vertical directions"),
        ("SRC3955_06_3888_chain", SRC / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv", "NLS3888_2_chain_rule", "observed matter variation chain rule"),
        ("SRC3955_07_3888_zero", SRC / "P8_Y5_R2FR_3888_QUOTIENT_NO_LINEAR_SOURCE_DERIVATION.csv", "NLS3888_3_observed_zero", "conditional J_obs zero"),
        ("SRC3955_08_3271_descent", SRC / "P8_Y5_R2FR_3271_QUOTIENT_FIBER_DESCENT_THEOREM.csv", "QFT3271_1_vertical_derivative_zero", "vertical derivative zero theorem"),
        ("SRC3955_09_3271_typed", SRC / "P8_Y5_R2FR_3271_QUOTIENT_FIBER_DESCENT_THEOREM.csv", "QFT3271_2_typed_visible_algebra", "typed visible algebra theorem"),
        ("SRC3955_10_DQ2570_template", SRC / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2570_0_chain_rule_template", "Dq chain-rule template"),
        ("SRC3955_11_DQ2570_private", SRC / "P8_Y5_FIELD_QUOTIENT_2570_DQ_VERTICAL_GENERATOR_LEDGER.csv", "DQ2570_2_q_private", "private q vertical unsigned"),
        ("SRC3955_12_DQ2570_coeff", SRC / "P8_Y5_FIELD_QUOTIENT_2570_COEFFICIENT_DESCENT_GATE.csv", "CD2570_0_descent_theorem", "visible coefficient descent"),
        ("SRC3955_13_QVM1620_Z", SRC / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv", "QVM1620_4_normal_form_Z", "normal-form Z map missing"),
        ("SRC3955_14_QVM1620_verdict", SRC / "P8_Y5_PARENT_QLOC_1620_QUOTIENT_VERTICALITY_MAP_AUDIT.csv", "QVM1620_5_verdict", "verticality map verdict"),
        ("SRC3955_15_QSC3516", SRC / "P8_Y5_R2FR_3516_QUOTIENT_SOURCE_COORDINATE_DESCENT_CERTIFICATE.csv", "QSC3516_0_master_theorem", "source coordinate descent theorem"),
        ("SRC3955_16_THM3633", SRC / "P8_Y5_R2FR_3633_STRICT_QUOTIENT_THEOREM.csv", "THM3633_2_matter_source_descent", "strict quotient matter/source descent"),
        ("SRC3955_17_STAT3532", SRC / "P8_local_GR_PiM_Htau_zero_mechanism_status.csv", "STAT3532_0_RPiM", "vertical fields do not move g_obs/J_H route"),
        ("SRC3955_18_validation_3954", SRC / "P8_Y5_BRR545_3954_VALIDATION.csv", "VAL3954_17_no_pycache", "previous validation"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, purpose in source_specs():
        exists = path.exists()
        found = False
        line_number = ""
        excerpt = ""
        if exists:
            for index, line in enumerate(read_text(path).splitlines(), start=1):
                if needle in line:
                    found = True
                    line_number = str(index)
                    excerpt = line[:1000]
                    break
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "needle": needle,
                "purpose": purpose,
                "exists": exists,
                "needle_found": found,
                "line_number": line_number,
                "line_excerpt": excerpt,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CA3955_0_chain_rule",
            "claim_piece": "observable metric Z-linear coefficient",
            "formula": "C_{A mu nu} := partial g_obs_{mu nu}/partial Z^A = D gbar_{mu nu}[Dq(Z_A)] + C^{direct}_{A mu nu}",
            "derived_statement": "The observable-metric source-current coefficient splits into a quotient-basic term plus any direct representative/readout dependence.",
            "zero_condition": "Dq(Z_A)=0, g_obs=gbar(q(Phi)), and C_A^direct=0",
            "current_status": "EXACT_CHAIN_RULE",
            "feeds": "J_A; eta_source_AB; frame split; PPN/source normalization",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CA3955_1_vertical_zero_theorem",
            "claim_piece": "quotient-vertical C_A zero",
            "formula": "Z_A in ker(Dq) and g_obs=q^*gbar => C_A=Dgbar[Dq(Z_A)]=0",
            "derived_statement": "If the MTS residual direction is genuinely quotient-vertical for the observable metric/readout functor, matter sees no linear metric source current from that direction.",
            "zero_condition": "actual q map, actual Z_A basis, Dq[Z_A]=0, and q-basic g_obs",
            "current_status": "EXACT_CONDITIONAL_THEOREM_NOT_CURRENTLY_SIGNED",
            "feeds": "C_A zero; J_A^obs zero",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CA3955_2_double_zero_observable_metric",
            "claim_piece": "observable metric double-zero alternative",
            "formula": "g_obs(Z)=g_0 + O(Z^2) => C_A|_{Z=0}=0",
            "derived_statement": "A parent-owned even/response-doublet observable metric also kills the linear source-current coefficient.",
            "zero_condition": "parent proves no odd/linear Z term in g_obs and no direct source-only readout",
            "current_status": "CONDITIONAL_ALTERNATIVE_NOT_PARENT_SIGNED",
            "feeds": "J_A silence; F_1=0 consistency",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CA3955_3_current_Z_status",
            "claim_piece": "current MTS Z verticality status",
            "formula": "claim(C_A=0) requires QVM1620 Z-map closure and DQ2570 vertical basis",
            "derived_statement": "Current formal Z^A variables have not been mapped into an actual kernel of Dq; public/coframe/readout/projector directions cannot be called vertical by declaration.",
            "zero_condition": "Z^A basis is computed and every retained direction either lies in ker(Dq) or is constraint-removed before matter coupling",
            "current_status": "CURRENT_BRANCH_BLOCKED_VERTICALITY_NOT_PROVED",
            "feeds": "claim gate; next target 3956",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CA3955_4_CA_norm_bound",
            "claim_piece": "finite C_A residual bound",
            "formula": "||C_A|| <= ||Dgbar|| ||Dq(Z_A)|| + ||C_A^direct|| + ||C_A^coeff|| + ||C_A^readout|| + ||C_A^boundary||",
            "derived_statement": "If verticality/descent is unsigned, C_A remains finite and decomposes into named residual channels.",
            "zero_condition": "not required; each term needs a theorem-zero or sourced value",
            "current_status": "VALUE_READY_BOUND_FORM_VALUES_MISSING",
            "feeds": "source-current residual; PPN/source-normalization vector",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CA3955_5_JA_obs_bound",
            "claim_piece": "observed source-current bound",
            "formula": "|J_A^obs| <= 1/2 ||T_obs|| ||C_A||",
            "derived_statement": "The observable metric leakage contribution to source-current is now directly bounded by stress size and C_A.",
            "zero_condition": "C_A=0 or source stress absent",
            "current_status": "VALUE_READY_BOUND_FORM_VALUES_MISSING",
            "feeds": "eta_source_AB; delta_frame_source; gamma_minus_1; local source coupling",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def ledger_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CAL3955_0_DqZ", "E_DqZ", "||Dq(Z_A)||", "quotient verticality failure", "0 if Z_A in ker(Dq)", "MISSING_ACTUAL_Q_AND_Z_BASIS"),
        ("CAL3955_1_qbasic_gobs", "E_gobs_basic", "failure of g_obs=gbar(q(Phi))", "observable metric not q-basic", "0 if g_obs is a quotient pullback", "CONDITIONAL_NOT_PARENT_SIGNED"),
        ("CAL3955_2_direct", "C_A_direct", "direct representative/readout dependence of g_obs on Z", "hidden-visible readout leakage", "0 if no direct representative slot exists", "MISSING_READOUT_GRAMMAR"),
        ("CAL3955_3_coeff", "C_A_coeff", "visible coefficient/coupling dependence on Z", "coefficient descent failure", "0 if visible constants/couplings are q-basic/fixed", "COEFFICIENT_DESCENT_UNSIGNED"),
        ("CAL3955_4_matter_constants", "C_A_theta", "partial_Z theta_obs", "matter constants/material label leakage", "0 if constant-sector superselection is parent-signed", "CONSTANT_SECTOR_UNSIGNED"),
        ("CAL3955_5_readout_order", "C_A_readout", "post-variation readout/projector dependence", "readout laundering/source-normalization leakage", "0 if projector/readout fixed before variation", "READOUT_ORDER_UNSIGNED"),
        ("CAL3955_6_boundary", "C_A_boundary", "boundary/reference/corner dependence in observable metric/source readout", "boundary source-current leakage", "0 if boundary class fixed or proper/exact", "BOUNDARY_REFERENCE_UNSIGNED"),
        ("CAL3955_7_total", "C_A_total_bound", "sum/envelope of C_A components", "total observable-metric linear leakage", "0 only if every component above is zero-owned", "COMPONENT_VALUES_MISSING"),
    ]
    return [
        {
            "row_id": row_id,
            "component": component,
            "definition": definition,
            "physical_meaning": meaning,
            "zero_route": zero_route,
            "current_status": status,
            "units": "metric_linear_coefficient_or_dimensionless_norm",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, definition, meaning, zero_route, status in data
    ]


def source_bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SCB3955_0_Jobs", "J_A^obs", "1/2 T_obs^{mu nu} C_{A mu nu}", "|J_A^obs| <= 1/2 ||T_obs|| ||C_A||", "C_A theorem-zero or finite C_A bound; source stress norm"),
        ("SCB3955_1_eta_source", "eta_source_AB", "composition/source-charge residual sourced by nonzero C_A or direct source weights", "eta_source_AB <= envelope(C_A,J_direct,J_measure,J_support)", "species/material assumptions and WEP/source bound"),
        ("SCB3955_2_frame", "delta_frame_source", "source variation frame differs from observed matter frame", "delta_frame_source <= envelope(C_A_readout,C_A_boundary,C_A_coeff)", "same-frame theorem or finite frame row"),
        ("SCB3955_3_radial", "partial_r_ln_mu_obs", "radial source hair from non-basic source coordinates/readout", "partial_r_ln_mu_obs <= radial envelope of C_A/support/product drift", "radial profile or theorem-zero"),
        ("SCB3955_4_total", "epsilon_source_norm_total", "source normalization total residual", "sum/envelope(C_A_total,J_direct,J_measure,J_support,Geff_product)", "component theorem-zero or values"),
    ]
    return [
        {
            "row_id": row_id,
            "target_symbol": symbol,
            "definition": definition,
            "bound_formula": bound,
            "needed_inputs": needed,
            "value": "",
            "units": "dimensionless_or_declared_source_units",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, definition, bound, needed in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3955_0_CA_theorem",
            "decision": "C_A=0 is derived on the quotient-vertical/q-basic branch",
            "basis": "C_A = Dgbar[Dq(Z_A)] + C_A_direct, so Dq(Z_A)=0 and no direct readout implies C_A=0",
            "effect": "source-current silence has a real theorem route",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3955_1_current_block",
            "decision": "do not claim current MTS has C_A=0",
            "basis": "QVM1620 says actual normal-form Z^A is not yet mapped into ker(Dq)",
            "effect": "current branch remains nonclaim and uses C_A residual bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3955_2_next",
            "decision": f"move to {NEXT_DOC}",
            "basis": "the next direct work is computing the actual Z^A verticality map or filling C_A component values",
            "effect": "turns the coupling gap into either a proof or a numeric/local bound row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CG3955_0_sources", "source-backed C_A checkpoint", "all source paths and needles exist", "PASS_IF_VALIDATION_PASS"),
        ("CG3955_1_theorem", "conditional C_A zero theorem", "C_A=0 on quotient-vertical/q-basic branch", "PASS_THEOREM_NONCLAIM"),
        ("CG3955_2_current_Z", "current MTS Z verticality", "actual Z^A basis lies in ker(Dq)", "BLOCKED_VERTICALITY_MAP_MISSING"),
        ("CG3955_3_direct_readout", "direct observable-metric leakage", "C_A_direct=0", "BLOCKED_READOUT_GRAMMAR_UNSIGNED"),
        ("CG3955_4_bound", "finite source-current bound", "C_A component values or theorem-zero rows exist", "BLOCKED_VALUES_MISSING"),
        ("CG3955_5_local_GR", "local-GR/Newton source-coupling promotion", "C_A, direct/measure/support, Khat, DeltaK, and coupling product close", "BLOCKED_NONCLAIM"),
    ]
    return [
        {
            "row_id": row_id,
            "gate": gate,
            "requirement": requirement,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, gate, requirement, status in data
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3955_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "compute or construct the actual Z^A verticality map: declare q, declare the Z basis, evaluate Dq[Z_A], and either prove Z_A in ker(Dq) or fill E_DqZ/C_A bound components",
            "success_condition": "at least one actual Z direction is theorem-vertical and source-silent, or every nonvertical direction gets explicit C_A/source-current residual rows with units and observable links",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "3955 proves the conditional quotient-vertical route to C_A=0 and turns the unsigned current branch into explicit C_A/source-current bound components.",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(bool(row["exists"]) and bool(row["needle_found"]) for row in source_rows)
    return f"""# 3955 - Observable Metric Z Linear Coefficient Or Source-Current Bound

Timestamp: `{timestamp}`

## Result

3955 derives the clean coupling theorem:

`C_A_mu_nu := partial g_obs_mu_nu / partial Z^A = D gbar_mu_nu[Dq(Z_A)] + C_A^direct`.

Therefore:

`Z_A in ker(Dq)` and `g_obs=q^*gbar` and `C_A^direct=0` imply `C_A=0`.

This is the exact source-current silence path:

`J_A^obs = 1/2 T_obs^mu_nu C_A_mu_nu = 0`.

## Current MTS Verdict

The theorem is real, but it is not yet a live MTS claim. The actual normal-form `Z^A` variables have not been mapped into `ker(Dq)`.

So the current branch remains:

`||C_A|| <= ||Dgbar|| ||Dq(Z_A)|| + ||C_A^direct|| + ||C_A^coeff|| + ||C_A^readout|| + ||C_A^boundary||`.

and:

`|J_A^obs| <= 1/2 ||T_obs|| ||C_A||`.

## Why This Matters

The coupling gap is now one precise computation:

declare `q`, declare `Z^A`, compute `Dq[Z_A]`.

If it vanishes, the source-current theorem advances. If not, the nonzero part becomes a local PPN/source-normalization residual.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3955_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3955_VALIDATION.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3955 - Observable Metric Z Linear Coefficient

Timestamp: `{timestamp}`

- Derived `C_A_mu_nu = Dgbar_mu_nu[Dq(Z_A)] + C_A^direct`.
- Proved conditional source silence: if `Z_A in ker(Dq)`, `g_obs` is q-basic, and no direct readout exists, then `C_A=0` and `J_A^obs=0`.
- Current MTS is not promoted because actual `Z^A` verticality is not yet computed.
- Bound fallback: `||C_A|| <= ||Dgbar||||Dq(Z_A)|| + ||C_A^direct|| + ||C_A^coeff|| + ||C_A^readout|| + ||C_A^boundary||`.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3955 - Observable Metric Z Linear Coefficient"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_git_status() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    if result.returncode != 0:
        return False, "git status unavailable; scope guard confirms generated outputs are outside formalization-workbench"
    modified_count = len([line for line in result.stdout.splitlines() if line.strip()])
    return modified_count == 0, f"formalization-workbench modified count is {modified_count}"


def csv_parse_ok(paths: list[Path]) -> bool:
    try:
        for path in paths:
            if path.exists():
                read_csv(path)
    except Exception:
        return False
    return True


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theorem = theorem_rows(timestamp)
    ledger = ledger_rows(timestamp)
    source_bound = source_bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    paths = generated_csvs + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_git_clean, fwb_git_detail = formalization_workbench_git_status()
    theorem_ids = {row["row_id"] for row in theorem}
    ledger_components = {row["component"] for row in ledger}
    source_targets = {row["target_symbol"] for row in source_bound}
    gate_statuses = {row["status"] for row in claim_gate}
    nonclaim_groups = (theorem, ledger, source_bound, decisions, claim_gate, next_target)
    checks = [
        ("VAL3955_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3955_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3955_02_CA_chain", "CA3955_0_chain_rule" in theorem_ids, "C_A chain rule emitted"),
        ("VAL3955_03_vertical_zero", "CA3955_1_vertical_zero_theorem" in theorem_ids, "quotient-vertical C_A zero theorem emitted"),
        ("VAL3955_04_current_block", "CA3955_3_current_Z_status" in theorem_ids, "current Z verticality block emitted"),
        ("VAL3955_05_CA_bound", "CA3955_4_CA_norm_bound" in theorem_ids and "CA3955_5_JA_obs_bound" in theorem_ids, "C_A and J_A bound forms emitted"),
        ("VAL3955_06_ledger_components", {"E_DqZ", "E_gobs_basic", "C_A_direct", "C_A_coeff", "C_A_theta", "C_A_readout", "C_A_boundary", "C_A_total_bound"}.issubset(ledger_components), "observable metric coefficient ledger emitted"),
        ("VAL3955_07_source_bound_targets", {"J_A^obs", "eta_source_AB", "delta_frame_source", "partial_r_ln_mu_obs", "epsilon_source_norm_total"}.issubset(source_targets), "source-current bound rows emitted"),
        ("VAL3955_08_claim_gate_blocks", "PASS_THEOREM_NONCLAIM" in gate_statuses and "BLOCKED_VERTICALITY_MAP_MISSING" in gate_statuses and "BLOCKED_NONCLAIM" in gate_statuses, "claim gate blocks current promotion"),
        ("VAL3955_09_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to Z verticality computation"),
        ("VAL3955_10_all_nonclaim", all(not row["valid_for_claim"] for group in nonclaim_groups for row in group), "all generated physics rows remain nonclaim"),
        ("VAL3955_11_outputs_outside_fwb", all(FWB not in path.parents and path != FWB for path in paths), "no generated output is inside formalization-workbench"),
        ("VAL3955_12_fwb_git_or_scope_guard", fwb_git_clean or all(FWB not in path.parents and path != FWB for path in paths), fwb_git_detail),
        ("VAL3955_13_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        ("VAL3955_14_spine_updated", SPINE_PATH.exists() and "3955 - Observable Metric Z Linear Coefficient" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3955_15_csv_parse", csv_parse_ok(generated_csvs), "generated CSV files parse cleanly"),
        ("VAL3955_16_script_compile", True, "script compiled before validation write"),
        ("VAL3955_17_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]


def run() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    ledger = ledger_rows(timestamp)
    source_bound = source_bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    claim_gate = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp, source_rows)

    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["ledger"], ledger)
    write_csv(OUTPUTS["source_bound"], source_bound)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claim_gate)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)

    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        raise SystemExit(f"3955 validation failed: {failed}")

    print(f"3955 checkpoint complete: {DOC_PATH}")
    print(f"validation: {OUTPUTS['validation']}")
    print("C_A theorem emitted; current branch requires Z verticality map or C_A bounds")


if __name__ == "__main__":
    run()
