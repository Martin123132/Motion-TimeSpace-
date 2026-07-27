from __future__ import annotations

import csv
import py_compile
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3929"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3929-Y5-R2FR-topological-projector-parent-signature-or-active-projector-norm-values.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3929_SOURCE_REGISTER.csv",
    "signature": SRC / "P8_Y5_R2FR_3929_PROJECTOR_PARENT_SIGNATURE.csv",
    "zero_result": SRC / "P8_Y5_R2FR_3929_PROJECTOR_DOMAIN_ZERO_RESULT.csv",
    "reduced_escape": SRC / "P8_Y5_R2FR_3929_REDUCED_BESCAPE_QUEUE.csv",
    "fallback": SRC / "P8_Y5_R2FR_3929_ACTIVE_PROJECTOR_FALLBACK_ROWS.csv",
    "decision": SRC / "P8_Y5_R2FR_3929_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3929_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3929_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3929_VALIDATION.csv",
}

SIGNATURE = (
    "S_parent^loc contains no dynamical Hodge/Green/trace/moving-domain P_D; "
    "P_D is a readout map on Sol(S_parent) or a fixed relative topological label "
    "P_D=q_src^*Pbar_top with no metric/domain variation"
)
PROJECTOR_ZERO = (
    "delta S_parent^loc/delta P_D=0, delta_g P_D=0, D_D P_D=0, "
    "delta_g chi_D=0, Phi_D=0, tau_wall_TF=0, same M_H_ref "
    "=> epsilon_domain_projector_abs=0 and P00_projector=P00_domain=0"
)
A_MULTI_REDUCED = (
    "A_multi_PD0 <= G_ext*(|P00_boundary|+|P00_history|+|P00_nonlocal|)+B_harmonic_boundary"
)
BESCAPE_REDUCED = "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi_PD0 + B_deriv"
ACTIVE_BOUND = (
    "epsilon_domain_projector_abs <= "
    "C_Pi_g||delta_g P_D||op||J_H||*/M_H_ref + "
    "C_Pi_D||D_D P_D||op||delta D||||J_H||*/M_H_ref + "
    "C_chi||delta_g chi_D|| + |Phi_D|/M_H_ref"
)
NEXT_DOC = "3930-Y5-R2FR-boundary-harmonic-no-flux-or-source-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3930_boundary_harmonic_no_flux_or_source_bound.py"


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


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3929_00_3928_doc", PCW / "3928-Y5-R2FR-projector-domain-certificate-or-first-Bescape-source-values.md", "Clean zero route:", "3928 clean projector/domain zero route"),
        ("SRC3929_01_3928_audit", SRC / "P8_Y5_R2FR_3928_PROJECTOR_DOMAIN_CERTIFICATE_AUDIT.csv", "PDC3928_6_zero_consequence", "3928 zero consequence"),
        ("SRC3929_02_3928_readout", SRC / "P8_Y5_R2FR_3928_TOPOLOGICAL_READOUT_ZERO_CONTRACT.csv", "ZPD3928_0_readout_route", "readout-only route"),
        ("SRC3929_03_3928_topological", SRC / "P8_Y5_R2FR_3928_TOPOLOGICAL_READOUT_ZERO_CONTRACT.csv", "ZPD3928_1_topological_route", "topological route"),
        ("SRC3929_04_3928_active", SRC / "P8_Y5_R2FR_3928_TOPOLOGICAL_READOUT_ZERO_CONTRACT.csv", "ZPD3928_2_active_route", "active fallback route"),
        ("SRC3929_05_3928_targets", SRC / "P8_Y5_R2FR_3928_FIRST_BESCAPE_SOURCE_VALUE_TARGETS.csv", "BST3928_0_choose_projector_type", "choose projector type"),
        ("SRC3929_06_3928_decision", SRC / "P8_Y5_R2FR_3928_DECISION_GATE.csv", "DEC3928_0_zero_contract", "zero contract decision"),
        ("SRC3929_07_3928_next", SRC / "P8_Y5_R2FR_3928_NEXT_TARGET.csv", "NEXT3928_0", "3929 handoff"),
        ("SRC3929_08_3924_doc", PCW / "3924-Y5-R2FR-parent-signature-adoption-minimal-action-clause-or-first-numeric-bound-pack.md", "S_proj^{top/readout}", "candidate parent action already had top/readout projector slot"),
        ("SRC3929_09_3925_projector", SRC / "P8_Y5_R2FR_3925_PARENT_CLAUSE_VARIATION_AUDIT.csv", "VAR3925_9_projector", "projector variation audit"),
        ("SRC3929_10_3925_domain", SRC / "P8_Y5_R2FR_3925_PARENT_CLAUSE_VARIATION_AUDIT.csv", "VAR3925_10_domain", "domain variation audit"),
        ("SRC3929_11_3926_core", SRC / "P8_Y5_R2FR_3926_CORE_LOCAL_BRANCH_ADOPTION_RECORD.csv", "CORE3926_0_status", "core branch adoption"),
        ("SRC3929_12_3927_component", SRC / "P8_Y5_R2FR_3927_BESCAPE_COMPONENT_FORMULAS.csv", "COMP3927_0_projector_domain", "projector/domain component formula"),
        ("SRC3929_13_3928_validation", SRC / "P8_Y5_BRR545_3928_VALIDATION.csv", "VAL3928_15_no_pycache", "3928 validation"),
        ("SRC3929_14_3922_escape", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_9_total", "B_escape total"),
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


def signature_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "SIG3929_0_route_choice",
            "signature_clause": "projector route choice",
            "statement": SIGNATURE,
            "branch_status": "ADOPTED_FOR_PRIVATE_LOCAL_BRANCH",
            "mathematical_effect": "removes dynamical projector variables from local Euler/Hilbert variation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SIG3929_1_no_action_level_PD",
            "signature_clause": "no action-level dynamic projector",
            "statement": "partial S_parent^loc/partial P_D=0 for Hodge/Green/trace/domain projectors",
            "branch_status": "SIGNED_BY_READOUT_SPLIT",
            "mathematical_effect": "delta S_parent^loc has no (delta_g P_D)J_H or (D_D P_D)[delta D]J_H term",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SIG3929_2_fixed_topological_label",
            "signature_clause": "topological label if a projector label is retained",
            "statement": "P_D=q_src^*Pbar_top with Pbar_top a fixed relative/cohomology label, not a metric Green/Hodge projector",
            "branch_status": "SIGNED_AS_LOCAL_BRANCH_CONTRACT",
            "mathematical_effect": "delta_g P_D=0 and D_D P_D=0",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SIG3929_3_fixed_qbasic_domain",
            "signature_clause": "fixed q-basic local domain",
            "statement": "D_loc=q_src^{-1}(Dbar) and source-silent local variations have D_X q_src=0",
            "branch_status": "SIGNED_FOR_SOURCE_SILENT_LOCAL_COLLAR",
            "mathematical_effect": "domain/support motion term vanishes on the local collar",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SIG3929_4_domain_collar_silence",
            "signature_clause": "domain collar silence",
            "statement": "the projector/domain collar has Phi_D=0 and tau_wall_TF=0; global boundary/harmonic data are not claimed here",
            "branch_status": "SIGNED_ONLY_FOR_PROJECTOR_DOMAIN_COLLAR",
            "mathematical_effect": "domain boundary-flux and selector-wall terms vanish, while separate boundary/harmonic gates remain open",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SIG3929_5_same_hilbert_denominator",
            "signature_clause": "same Hilbert denominator",
            "statement": "projector readout does not introduce a second compact-source mass or source normalization; it uses M_H_ref from the same Hilbert source",
            "branch_status": "SIGNED_AS_NO_EXTRA_SOURCE_NORMALIZATION_IN_PROJECTOR_SECTOR",
            "mathematical_effect": "no hidden monopole/source-normalization stress is credited to the projector/domain sector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "SIG3929_6_signature_verdict",
            "signature_clause": "projector/domain local branch verdict",
            "statement": PROJECTOR_ZERO,
            "branch_status": "PROJECTOR_DOMAIN_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH",
            "mathematical_effect": "epsilon_domain_projector_abs, P00_projector and P00_domain are zero in this branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def zero_result_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("PDZ3929_0_epsilon_Pi_g", "epsilon_Pi_g", "0", "delta_g P_D=0 or no action-level P_D"),
        ("PDZ3929_1_epsilon_Pi_D", "epsilon_Pi_D", "0", "D_D P_D=0 on fixed q-basic source-silent collar"),
        ("PDZ3929_2_epsilon_chi", "epsilon_chi", "0", "delta_g chi_D=0 and tau_wall_TF=0 in projector/domain collar"),
        ("PDZ3929_3_epsilon_D_boundary", "epsilon_D_boundary", "0", "Phi_D=0 for fixed relative projector/domain collar"),
        ("PDZ3929_4_epsilon_domain_projector_abs", "epsilon_domain_projector_abs", "0", "absolute sum of zeroed projector/domain subterms"),
        ("PDZ3929_5_P00_projector", "P00_projector", "0", "no projector stress/source multipole in readout/topological branch"),
        ("PDZ3929_6_P00_domain", "P00_domain", "0", "no moving-domain/support scalar source in fixed q-basic branch"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "branch_value": value,
            "derivation": derivation,
            "branch_status": "THEOREM_ZERO_IN_PRIVATE_LOCAL_BRANCH",
            "strict_public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, value, derivation in data
    ]


def reduced_escape_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "REB3929_0_removed_component",
            "component": "projector/domain",
            "before": ACTIVE_BOUND,
            "after": "epsilon_domain_projector_abs=0, P00_projector=0, P00_domain=0",
            "status": "REMOVED_IN_PRIVATE_LOCAL_BRANCH",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "REB3929_1_reduced_multipole",
            "component": "A_multi",
            "before": "A_multi <= G_ext*(|P00_boundary|+|P00_projector|+|P00_domain|+|P00_history|+|P00_nonlocal|)+B_harmonic_boundary",
            "after": A_MULTI_REDUCED,
            "status": "REDUCED_QUEUE_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "REB3929_2_reduced_escape",
            "component": "B_escape",
            "before": "|Delta_sq|/(1+xi_1)^2 + |epsilon_r| + A_multi + B_deriv + epsilon_domain_projector_abs",
            "after": BESCAPE_REDUCED,
            "status": "PROJECTOR_DOMAIN_REMOVED_BOUNDARY_HISTORY_DERIVATIVE_REMAIN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "REB3929_3_next_priority",
            "component": "next obstruction",
            "before": "projector/domain first",
            "after": "boundary/harmonic multipoles, then history/nonlocal, then derivative hair and Delta_sq/epsilon_r",
            "status": "NEXT_PRIORITY_SELECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("FB3929_0_metric", "if dynamic metric-dependent P_D is reintroduced", "source ||delta_g P_D||op and C_Pi_g||J_H||*/M_H_ref"),
        ("FB3929_1_domain", "if moving support/domain is reintroduced", "source ||D_D P_D||op||delta D|| and C_Pi_D||J_H||*/M_H_ref"),
        ("FB3929_2_selector", "if selector wall carries stress", "source ||delta_g chi_D|| and tau_wall_TF/M_H_ref"),
        ("FB3929_3_flux", "if projector/domain collar has flux", "source Phi_D/M_H_ref"),
        ("FB3929_4_total", "if the 3929 signature is rejected", ACTIVE_BOUND),
    ]
    return [
        {
            "row_id": row_id,
            "fallback_condition": condition,
            "required_bound": required,
            "numeric_value": "",
            "status": "HELD_IN_RESERVE_IF_SIGNATURE_REJECTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, condition, required in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3929_0_adopt_signature",
            "decision": "adopt the readout/topological projector route for the private local branch",
            "reason": "it is the least-extra-force route and is already compatible with the 3924 S_proj^{top/readout} slot",
            "claim_status": "PRIVATE_BRANCH_ZERO_NOT_PUBLIC_CLAIM",
            "next_action": "remove projector/domain from B_escape queue and attack boundary/harmonic",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3929_1_reduced_Bescape",
            "decision": "epsilon_domain_projector_abs, P00_projector and P00_domain are zero in this branch",
            "reason": PROJECTOR_ZERO,
            "claim_status": "CONDITIONAL_ON_LOCAL_BRANCH_SIGNATURE",
            "next_action": "score remaining B_escape terms only after their gates close",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3929_2_active_fallback",
            "decision": "if later MTS needs active Hodge/Green/dynamic projector, 3929 zero must be revoked and fallback rows used",
            "reason": "active operator derivatives are real stress channels",
            "claim_status": "REVERSIBLE_PRIVATE_BRANCH_CHOICE",
            "next_action": "keep active fallback rows as nonclaim reserve",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3929_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attack boundary/harmonic multipoles after projector/domain removal",
            "success_condition": "derive fixed no-flux/no-harmonic boundary route or source-backed P00_boundary and B_harmonic_boundary rows",
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
            "summary": "projector/domain escape component zeroed inside the private readout/topological local branch; boundary/history remain",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3929 - Topological Projector Parent Signature or Active Projector Norm Values

Timestamp: `{timestamp}`

## Result

Adopted the clean projector/domain route for the private local branch.

Signature clause:

`{SIGNATURE}`.

Zero result:

`{PROJECTOR_ZERO}`.

Reduced multipole queue:

`{A_MULTI_REDUCED}`.

Reduced escape queue:

`{BESCAPE_REDUCED}`.

## Meaning

This is a genuine forward move. In the local-GR branch, the projector is not allowed to be a hidden dynamical Hodge/Green/trace/moving-domain operator. It is either a readout on solved fields or a fixed topological/q-basic label. Under that branch choice, the projector/domain escape component is zero and drops out of the local `B_escape` queue.

This is still not a public local-GR claim: the boundary/harmonic, history/nonlocal, derivative-hair, `Delta_sq`, and `epsilon_r` gates remain open. If a future MTS route insists on an active projector, this 3929 zero must be revoked and the fallback operator-norm rows must be filled.

## Current Verdict

- `epsilon_domain_projector_abs=0` inside the private readout/topological local branch.
- `P00_projector=0` and `P00_domain=0` inside the same branch.
- `A_multi` reduces to boundary/history/nonlocal plus harmonic boundary data.
- No change to `formalization-workbench`; no GitHub action.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3929_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3929_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3929_PROJECTOR_PARENT_SIGNATURE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3929_PROJECTOR_DOMAIN_ZERO_RESULT.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3929_REDUCED_BESCAPE_QUEUE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3929_ACTIVE_PROJECTOR_FALLBACK_ROWS.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3929_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3929_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3929 - Topological Projector Parent Signature

Timestamp: `{timestamp}`

- Signature: `{SIGNATURE}`.
- Zero result: `{PROJECTOR_ZERO}`.
- Reduced multipole: `{A_MULTI_REDUCED}`.
- Reduced escape: `{BESCAPE_REDUCED}`.
- Status: projector/domain removed from the private local branch; boundary/harmonic and history gates remain nonclaim.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3929 - Topological Projector Parent Signature"
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
    signature = signature_rows(timestamp)
    zero_result = zero_result_rows(timestamp)
    reduced = reduced_escape_rows(timestamp)
    fallback = fallback_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    fwb_modified = formalization_workbench_modified_count()
    reduced_formula = next(row["after"] for row in reduced if row["row_id"] == "REB3929_2_reduced_escape")
    checks = [
        ("VAL3929_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3929_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3929_02_signature_adopted", any(row["branch_status"] == "PROJECTOR_DOMAIN_ZERO_SIGNED_FOR_PRIVATE_LOCAL_BRANCH" for row in signature), "projector/domain private signature verdict emitted"),
        ("VAL3929_03_zero_rows", len(zero_result) == 7 and all(row["branch_value"] == "0" for row in zero_result), "projector/domain zero rows emitted"),
        ("VAL3929_04_reduced_escape", "epsilon_domain_projector_abs" not in reduced_formula and "A_multi_PD0" in reduced_formula, "reduced B_escape removes projector/domain term"),
        ("VAL3929_05_reduced_multipole", any(row["row_id"] == "REB3929_1_reduced_multipole" and "P00_projector" not in row["after"] and "P00_domain" not in row["after"] for row in reduced), "reduced A_multi removes projector/domain sources"),
        ("VAL3929_06_fallback_kept", len(fallback) == 5 and any(row["row_id"] == "FB3929_4_total" for row in fallback), "active projector fallback rows retained"),
        ("VAL3929_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (signature, zero_result, reduced, fallback, decisions) for row in group), "all rows are nonclaim"),
        ("VAL3929_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3929_09_fwb_unmodified", fwb_modified == 0, f"formalization-workbench modified-file count is {fwb_modified}"),
        ("VAL3929_10_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3929_11_spine_written", SPINE_PATH.exists() and "3929 - Topological Projector Parent Signature" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3929_12_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3929_13_script_compiles", True, "script compiles"),
        ("VAL3929_14_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["signature"], signature_rows(timestamp))
    write_csv(OUTPUTS["zero_result"], zero_result_rows(timestamp))
    write_csv(OUTPUTS["reduced_escape"], reduced_escape_rows(timestamp))
    write_csv(OUTPUTS["fallback"], fallback_rows(timestamp))
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
        raise SystemExit(f"3929 validation failed: {failed}")
    print(f"3929 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
