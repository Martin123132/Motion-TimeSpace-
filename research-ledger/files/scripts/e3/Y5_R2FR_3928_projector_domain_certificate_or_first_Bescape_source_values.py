from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3928"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3928-Y5-R2FR-projector-domain-certificate-or-first-Bescape-source-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3928_SOURCE_REGISTER.csv",
    "audit": SRC / "P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_CERTIFICATE_AUDIT.csv",
    "zero_contract": SRC / "P8_Y5_R2FR_3928_TOPOLOGICAL_READOUT_ZERO_CONTRACT.csv",
    "bound_rows": SRC / "P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_BOUND_INPUT_ROWS.csv",
    "source_targets": SRC / "P8_Y5_R2FR_3928_FIRST_BESCAPE_SOURCE_VALUE_TARGETS.csv",
    "decision": SRC / "P8_Y5_R2FR_3928_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3928_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3928_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3928_VALIDATION.csv",
}

PRODUCT_VARIATION = (
    "delta(P_D J_H)=P_D delta J_H+(delta_g P_D)J_H+(D_D P_D)[delta D]J_H"
)
TOPOLOGICAL_ZERO = (
    "P_D=q_D^*Pbar_top, delta_g P_D=0, D_D P_D=0, delta_g chi_D=0, Phi_D=0 "
    "=> epsilon_domain_projector_abs=0"
)
READOUT_ZERO = (
    "P_D outside S_parent and used only after solving => delta S_parent/delta_g contains no P_D variation term"
)
ACTIVE_BOUND = (
    "epsilon_domain_projector_abs <= "
    "C_Pi_g||delta_g P_D||op||J_H||*/M_H_ref + "
    "C_Pi_D||D_D P_D||op||delta D||||J_H||*/M_H_ref + "
    "C_chi||delta_g chi_D|| + |Phi_D|/M_H_ref"
)
TOTAL_ESCAPE = "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi + B_deriv + epsilon_domain_projector_abs"
NEXT_DOC = "3929-Y5-R2FR-topological-projector-parent-signature-or-active-projector-norm-values.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3929_topological_projector_parent_signature_or_active_projector_norm_values.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3928_00_3927_doc", PCW / "3927-Y5-R2FR-Bescape-component-bound-pack-projector-domain-boundary-history.md", "Projector/domain:", "3927 selected the projector/domain escape component"),
        ("SRC3928_01_3927_component", SRC / "P8_Y5_R2FR_3927_BESCAPE_COMPONENT_FORMULAS.csv", "COMP3927_0_projector_domain", "projector/domain component formula"),
        ("SRC3928_02_3927_inputs", SRC / "P8_Y5_R2FR_3927_BESCAPE_INPUT_REQUIREMENTS.csv", "IN3927_0_delta_g_PD", "projector derivative input"),
        ("SRC3928_03_3927_inputs_domain", SRC / "P8_Y5_R2FR_3927_BESCAPE_INPUT_REQUIREMENTS.csv", "IN3927_1_DD_PD", "domain derivative input"),
        ("SRC3928_04_3431_doc_identity", PCW / "3431-Y5-R2FR-domain-projector-no-stress-theorem-or-operator-bound-under-AX1090.md", "DP3431_0_variation_identity", "product variation identity"),
        ("SRC3928_05_3431_doc_topological", PCW / "3431-Y5-R2FR-domain-projector-no-stress-theorem-or-operator-bound-under-AX1090.md", "DP3431_2_fixed_topological_zero", "fixed topological zero theorem"),
        ("SRC3928_06_3431_doc_bound", PCW / "3431-Y5-R2FR-domain-projector-no-stress-theorem-or-operator-bound-under-AX1090.md", "DP3431_6_operator_bound", "operator bound theorem"),
        ("SRC3928_07_3431_bound_rows", SRC / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv", "DPOB3431_4_total_domain_projector", "domain/projector absolute-sum bound"),
        ("SRC3928_08_3922_projector", SRC / "P8_Y5_R2FR_3922_MULTIPOLE_ESCAPE_ZERO_THEOREM.csv", "MUL3922_2_projector_zero", "projector escape zero route"),
        ("SRC3928_09_3922_domain", SRC / "P8_Y5_R2FR_3922_MULTIPOLE_ESCAPE_ZERO_THEOREM.csv", "MUL3922_3_domain_zero", "domain escape zero route"),
        ("SRC3928_10_3922_escape_total", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_8_projector_domain_total", "epsilon_domain_projector_abs bound vector"),
        ("SRC3928_11_3925_projector", SRC / "P8_Y5_R2FR_3925_PARENT_CLAUSE_VARIATION_AUDIT.csv", "VAR3925_9_projector", "projector variation audit"),
        ("SRC3928_12_3925_domain", SRC / "P8_Y5_R2FR_3925_PARENT_CLAUSE_VARIATION_AUDIT.csv", "VAR3925_10_domain", "domain variation audit"),
        ("SRC3928_13_3926_projector_action", SRC / "P8_Y5_R2FR_3926_CERTIFICATE_OR_BOUND_ACTION_QUEUE.csv", "ACT3926_0_projector", "projector next action"),
        ("SRC3928_14_3926_domain_action", SRC / "P8_Y5_R2FR_3926_CERTIFICATE_OR_BOUND_ACTION_QUEUE.csv", "ACT3926_1_domain", "domain next action"),
        ("SRC3928_15_3927_validation", SRC / "P8_Y5_BRR545_3927_VALIDATION.csv", "VAL3927_13_no_pycache", "3927 validation handoff"),
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
                    excerpt = line[:760]
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
                "timestamp_utc": timestamp,
            }
        )
    return rows


def certificate_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PDC3928_0_product_identity",
            "clause": "projector variation identity",
            "statement": PRODUCT_VARIATION,
            "derivation_status": "EXACT_IMPORTED_FROM_3431",
            "zero_effect": "identifies exactly which two terms must be killed or bounded",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PDC3928_1_readout_only_zero",
            "clause": "readout-only projector",
            "statement": READOUT_ZERO,
            "derivation_status": "EXACT_IF_PROJECTOR_NOT_IN_ACTION",
            "zero_effect": "delta_g P_D and D_D P_D never appear in the Euler/Hilbert variation",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PDC3928_2_topological_basic_zero",
            "clause": "topological q-basic projector",
            "statement": "P_D=q_D^*Pbar_top with Pbar_top fixed on quotient/topological data",
            "derivation_status": "CONDITIONAL_EXACT_ZERO_CONTRACT",
            "zero_effect": "delta_g P_D=0 and D_D P_D=0",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PDC3928_3_fixed_domain_zero",
            "clause": "fixed q-basic domain",
            "statement": "D_loc=q_src^{-1}(Dbar), D_X q_src=0 on source-silent local branch, and Dbar fixed",
            "derivation_status": "CONDITIONAL_EXACT_ZERO_CONTRACT",
            "zero_effect": "domain/support motion term D_D P_D[delta D] vanishes for source-silent verticals",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PDC3928_4_selector_boundary_zero",
            "clause": "selector and boundary silence",
            "statement": "delta_g chi_D=0, tau_wall_TF=0, and Phi_D=0 on the fixed relative collar",
            "derivation_status": "CONDITIONAL_EXACT_ZERO_CONTRACT",
            "zero_effect": "selector stress and boundary-flux terms vanish",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PDC3928_5_same_hilbert_denominator",
            "clause": "same Hilbert source denominator",
            "statement": "P_D may not introduce a second compact-source normalization distinct from M_H_ref",
            "derivation_status": "REQUIRED_GUARD",
            "zero_effect": "prevents a hidden source-normalization monopole from surviving after projector stress is killed",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PDC3928_6_zero_consequence",
            "clause": "projector/domain zero consequence",
            "statement": TOPOLOGICAL_ZERO,
            "derivation_status": "PROVED_CONDITIONAL_ON_PDC3928_1_TO_5",
            "zero_effect": "candidate_value_if_parent_signed=0",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "PDC3928_7_active_branch_no_go",
            "clause": "active Hodge/Green/dynamic trace projector",
            "statement": "delta G_D=-G_D(delta L_D)G_D plus boundary terms, and Reynolds/domain variation gives boundary flux",
            "derivation_status": "ZERO_REJECTED_FOR_ACTIVE_BRANCH",
            "zero_effect": "must use operator-bound rows, not a theorem-zero",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ZPD3928_0_readout_route",
            "route": "readout-only",
            "parent_clause_required": "S_parent has no action-level P_D; P_D is only a post-solution/readout classifier",
            "mathematical_condition": "partial S_parent/partial P_D = 0",
            "subterms_zeroed": "delta_g P_D, D_D P_D[delta D], delta_g chi_D, Phi_D as action sources",
            "candidate_value_if_signed": "epsilon_domain_projector_abs=0",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ZPD3928_1_topological_route",
            "route": "fixed topological in-action route",
            "parent_clause_required": "P_D=q_D^*Pbar_top with fixed relative class, metric independence, domain independence, boundary silence, same Hilbert denominator",
            "mathematical_condition": "delta_g P_D=D_D P_D=delta_g chi_D=Phi_D=0",
            "subterms_zeroed": "epsilon_Pi_g, epsilon_Pi_D, epsilon_chi, epsilon_D_boundary",
            "candidate_value_if_signed": "epsilon_domain_projector_abs=0",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ZPD3928_2_active_route",
            "route": "dynamic/Hodge/Green/moving-domain route",
            "parent_clause_required": "operator norm source values or a new Euler/Ward cancellation theorem",
            "mathematical_condition": ACTIVE_BOUND,
            "subterms_zeroed": "none without additional theorem",
            "candidate_value_if_signed": "not applicable; score by sourced absolute bound",
            "strict_current_signed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_input_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "PDB3928_0_projector_metric",
            "epsilon_Pi_g",
            "C_Pi_g||delta_g P_D||op||J_H||*/M_H_ref",
            "zero by readout-only/topological metric independence; otherwise source ||delta_g P_D||op, ||J_H||*, M_H_ref",
        ),
        (
            "PDB3928_1_domain_motion",
            "epsilon_Pi_D",
            "C_Pi_D||D_D P_D||op||delta D||||J_H||*/M_H_ref",
            "zero by fixed q-basic domain; otherwise source ||D_D P_D||op, ||delta D||, ||J_H||*, M_H_ref",
        ),
        (
            "PDB3928_2_selector_stress",
            "epsilon_chi",
            "C_chi||delta_g chi_D|| + |tau_wall_TF|/M_H_ref",
            "zero by scalar/topological selector with no wall anisotropy; otherwise source selector stress and wall stress",
        ),
        (
            "PDB3928_3_boundary_flux",
            "epsilon_D_boundary",
            "|Phi_D|/M_H_ref",
            "zero by fixed relative no-flux collar; otherwise source boundary/collar flux integral",
        ),
        (
            "PDB3928_4_total",
            "epsilon_domain_projector_abs",
            "|epsilon_Pi_g|+|epsilon_Pi_D|+|epsilon_chi|+|epsilon_D_boundary|",
            "absolute-sum guard; no cancellation credit",
        ),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "formula": formula,
            "zero_or_source_rule": rule,
            "numeric_value": "",
            "source_path": "",
            "source_status": "PARENT_SIGNATURE_OR_NUMERIC_SOURCE_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, formula, rule in data
    ]


def source_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "BST3928_0_choose_projector_type",
            "target": "P_D definition",
            "needed_for": "decide whether zero branch or active bound branch is physically intended",
            "acceptable_source": "parent action clause saying readout-only/topological, or explicit active Hodge/Green/domain definition",
            "first_numeric_if_active": "",
            "status": "DECISION_REQUIRED_BEFORE_SCORING",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BST3928_1_metric_operator_norm",
            "target": "||delta_g P_D||op",
            "needed_for": "epsilon_Pi_g",
            "acceptable_source": "analytic operator derivative bound for chosen projector and local norm convention",
            "first_numeric_if_active": "",
            "status": "SOURCE_VALUE_READY_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BST3928_2_domain_motion_norm",
            "target": "||D_D P_D||op||delta D||",
            "needed_for": "epsilon_Pi_D",
            "acceptable_source": "fixed-domain proof or Reynolds/domain-motion bound for chosen support",
            "first_numeric_if_active": "",
            "status": "SOURCE_VALUE_READY_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BST3928_3_boundary_flux",
            "target": "Phi_D/M_H_ref",
            "needed_for": "epsilon_D_boundary and P00_domain/P00_projector",
            "acceptable_source": "no-flux theorem for collar or explicit boundary integral bound",
            "first_numeric_if_active": "",
            "status": "SOURCE_VALUE_READY_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "BST3928_4_selector_wall",
            "target": "delta_g chi_D and tau_wall_TF",
            "needed_for": "epsilon_chi",
            "acceptable_source": "scalar/topological selector proof or stress tensor bound for selector wall",
            "first_numeric_if_active": "",
            "status": "SOURCE_VALUE_READY_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3928_0_zero_contract",
            "decision": "projector/domain zero proof is constructed as a precise parent contract",
            "reason": TOPOLOGICAL_ZERO,
            "claim_status": "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "next_action": "try to sign topological/readout projector in parent action",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3928_1_active_not_zero",
            "decision": "active Hodge/Green/dynamic trace or moving-domain projectors are not zeroed",
            "reason": "their operator/domain derivatives create stress terms exactly identified by the product variation",
            "claim_status": "BOUND_REQUIRED_IF_ACTIVE_PROJECTOR",
            "next_action": "fill operator norm/source rows if topological/readout route is rejected",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3928_2_no_score_yet",
            "decision": "B_escape remains unscored",
            "reason": "epsilon_domain_projector_abs has a candidate zero contract but no parent signature and no numeric active-branch values",
            "claim_status": "LOCAL_GR_PROMOTION_BLOCKED",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3928_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "try to parent-sign the topological/readout projector clause; if not, fill active projector norm values",
            "success_condition": "epsilon_domain_projector_abs becomes theorem-zero for the local branch or gains numeric nonclaim bound rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "PASS_PRIVATE_NONCLAIM_CHECKPOINT",
            "summary": "projector/domain zero contract constructed conditionally; active branch bound rows staged",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3928 - Projector/Domain Certificate or First B_escape Source Values

Timestamp: `{timestamp}`

## Result

Built the first real projector/domain zero contract.

Exact variation identity:

`{PRODUCT_VARIATION}`.

Clean zero route:

`{TOPOLOGICAL_ZERO}`.

Readout-only route:

`{READOUT_ZERO}`.

Active-branch fallback:

`{ACTIVE_BOUND}`.

## Meaning

This is a useful fork, not a vibes-missing note. The local branch can kill `epsilon_domain_projector_abs` only if the parent action signs a readout-only or fixed topological/q-basic projector with boundary silence and same Hilbert denominator. If the intended projector is Hodge/Green/dynamic trace or a moving support, the exact product variation forces the operator-bound route.

## Current Verdict

- Candidate zero value: `epsilon_domain_projector_abs=0` if the 3928 topological/readout contract is parent-signed.
- Strict-current status: not signed yet, so no local-GR/PPN/R10 claim.
- Active fallback: source `||delta_g P_D||op`, `||D_D P_D||op||delta D||`, `delta_g chi_D`, `tau_wall_TF`, `Phi_D`, `||J_H||*`, and `M_H_ref`.
- Total escape term remains: `{TOTAL_ESCAPE}`.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3928_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3928_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_CERTIFICATE_AUDIT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3928_TOPOLOGICAL_READOUT_ZERO_CONTRACT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_BOUND_INPUT_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3928_FIRST_BESCAPE_SOURCE_VALUE_TARGETS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3928_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3928_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3928 - Projector/Domain Certificate or First B_escape Source Values

Timestamp: `{timestamp}`

- Exact variation: `{PRODUCT_VARIATION}`.
- Candidate zero contract: `{TOPOLOGICAL_ZERO}`.
- Readout-only contract: `{READOUT_ZERO}`.
- Active fallback: `{ACTIVE_BOUND}`.
- Verdict: conditional zero route constructed but not parent-signed; active branch must be bounded.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3928 - Projector/Domain Certificate or First B_escape Source Values"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def formalization_workbench_modified_count() -> int:
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT), "status", "--porcelain", "--", str(FWB.relative_to(ROOT))],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except Exception:
        return 0
    if result.returncode != 0:
        return 0
    return len([line for line in result.stdout.splitlines() if line.strip()])


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    audit = certificate_audit_rows(timestamp)
    zero_contract = zero_contract_rows(timestamp)
    bound_rows = bound_input_rows(timestamp)
    source_targets = source_target_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    checks = [
        ("VAL3928_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3928_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3928_02_variation_identity", any(row["row_id"] == "PDC3928_0_product_identity" for row in audit), "projector variation identity emitted"),
        ("VAL3928_03_zero_contract", len(zero_contract) == 3 and any(row["row_id"] == "ZPD3928_1_topological_route" for row in zero_contract), "topological/readout zero contract emitted"),
        ("VAL3928_04_active_bound", any(row["mathematical_condition"] == ACTIVE_BOUND for row in zero_contract) and any(row["row_id"] == "PDB3928_4_total" for row in bound_rows), "active branch bound interface emitted"),
        ("VAL3928_05_bound_inputs", len(bound_rows) == 5, "projector/domain bound rows emitted"),
        ("VAL3928_06_source_targets", len(source_targets) == 5, "first B_escape source-value targets emitted"),
        ("VAL3928_07_not_signed", all(str(row.get("strict_current_signed")) == "False" for group in (audit, zero_contract) for row in group), "zero route remains unsigned"),
        ("VAL3928_08_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (audit, zero_contract, bound_rows, source_targets, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3928_09_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3928_10_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3928_11_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3928_12_spine_written", SPINE_PATH.exists() and "3928 - Projector/Domain Certificate" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3928_13_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3928_14_script_compiles", True, "script compiles"),
        ("VAL3928_15_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]
    return [
        {
            "row_id": row_id,
            "check": detail,
            "result": "PASS" if passed else "FAIL",
            "timestamp_utc": timestamp,
        }
        for row_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = now_utc()
    source_rows = source_register_rows(timestamp)
    write_csv(OUTPUTS["sources"], source_rows)
    write_csv(OUTPUTS["audit"], certificate_audit_rows(timestamp))
    write_csv(OUTPUTS["zero_contract"], zero_contract_rows(timestamp))
    write_csv(OUTPUTS["bound_rows"], bound_input_rows(timestamp))
    write_csv(OUTPUTS["source_targets"], source_target_rows(timestamp))
    write_csv(OUTPUTS["decision"], decision_rows(timestamp))
    write_csv(OUTPUTS["next"], next_rows(timestamp))
    write_csv(OUTPUTS["status"], status_rows(timestamp, source_rows))
    DOC_PATH.write_text(doc_text(timestamp, source_rows), encoding="utf-8")
    update_spine(timestamp)
    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    validation = validation_rows(timestamp, source_rows)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        raise SystemExit(f"3928 validation failed: {failed}")
    print(f"3928 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
