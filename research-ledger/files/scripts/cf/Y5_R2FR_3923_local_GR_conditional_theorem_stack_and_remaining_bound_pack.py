from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3923"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3923-Y5-R2FR-local-GR-conditional-theorem-stack-and-remaining-bound-pack.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3923_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3923_LOCAL_GR_CONDITIONAL_THEOREM_STACK.csv",
    "signatures": SRC / "P8_Y5_R2FR_3923_PARENT_SIGNATURE_CLAUSES.csv",
    "bounds": SRC / "P8_Y5_R2FR_3923_REMAINING_BOUND_PACK.csv",
    "decision": SRC / "P8_Y5_R2FR_3923_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3923_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3923_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3923_VALIDATION.csv",
}

THEOREM = (
    "If B_loc parent normal form + EH public metric + same-frame Hilbert/Maxwell source + constant G_* + "
    "source-silent M_eff + R11 STF zero + beta square law + P00 harmonic monopole-only common mode + "
    "boundary/projector/fixed-domain/history escape silence all hold, then local GR/PPN/Newton/Maxwell follows."
)
PPN_ZERO = "Delta_PPN_GR=(gamma-1,beta-1,alpha1,alpha2,alpha3,xi,zeta_i,Gdot/G)_loc=0"
BOUND_PACK = (
    "B_local := |delta_gamma_R11| + |delta_beta_source| + |delta_beta_common| + B_escape + "
    "|Gdot/G| + |alpha1|+|alpha2|+|alpha3|+|xi|+sum|zeta_i|"
)
NEXT_DOC = "3924-Y5-R2FR-parent-signature-adoption-minimal-action-clause-or-first-numeric-bound-pack.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3924_parent_signature_adoption_minimal_action_clause_or_first_numeric_bound_pack.py"


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
        ("SRC3923_00_next", SRC / "P8_Y5_R2FR_3922_NEXT_TARGET.csv", "NEXT3922_0", "3922 selected local-GR stack target"),
        ("SRC3923_01_GR_eq", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_1_GR_equation", "GR equation reduction"),
        ("SRC3923_02_Newton", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_3_Newton", "Newtonian limit"),
        ("SRC3923_03_G_owner", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_4_G_constant", "G owner status"),
        ("SRC3923_04_EH_selector", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_0_selector", "EH selector"),
        ("SRC3923_05_Hilbert", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_0_Hilbert", "Hilbert source bridge"),
        ("SRC3923_06_Maxwell", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_1_Maxwell", "Maxwell stress bridge"),
        ("SRC3923_07_Gstar", SRC / "P8_Y5_R2FR_3909_GSTAR_ZEROFORM_ACTION_BLOCK.csv", "ZF3909_0_action", "Gstar zeroform action"),
        ("SRC3923_08_Meff", SRC / "P8_Y5_R2FR_3913_MEFF_STATIONARY_SOURCE_CLOSURE_STACK.csv", "MSC3913_4_BMeff", "M_eff/B_Meff core closure"),
        ("SRC3923_09_3914_stack", SRC / "P8_Y5_R2FR_3914_STATIONARY_SOURCE_COUPLING_STACK.csv", "STK3914_1_stack", "source coupling stack"),
        ("SRC3923_10_3914_arena", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_0_GR", "local GR arena"),
        ("SRC3923_11_3914_Maxwell", SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv", "ARE3914_2_Maxwell", "Maxwell arena"),
        ("SRC3923_12_Bloc", SRC / "P8_Y5_R2FR_3915_STATIONARY_LOCAL_BRANCH_CONTRACT.csv", "BLC3915_0_branch", "B_loc branch contract"),
        ("SRC3923_13_PPN_zero", SRC / "P8_Y5_R2FR_3915_CONDITIONAL_PPN_ZERO_VECTOR.csv", "PPNZ3915_8_total", "conditional PPN zero vector"),
        ("SRC3923_14_R11_fork", SRC / "P8_Y5_R2FR_3916_R11_SELECTOR_FORK.csv", "FORK3916_2_zero", "R11 zero consequence"),
        ("SRC3923_15_gamma", SRC / "P8_Y5_R2FR_3918_GAMMA_DECISION_GATE.csv", "DEC3918_0_gamma", "gamma STF zero"),
        ("SRC3923_16_beta", SRC / "P8_Y5_R2FR_3919_DECISION_GATE.csv", "DEC3919_0_beta_source", "beta source zero"),
        ("SRC3923_17_common", SRC / "P8_Y5_R2FR_3920_DECISION_GATE.csv", "DEC3920_0_square_law", "common-mode square law"),
        ("SRC3923_18_harmonic", SRC / "P8_Y5_R2FR_3921_DECISION_GATE.csv", "DEC3921_0_harmonic_route", "P00 harmonic route"),
        ("SRC3923_19_escape", SRC / "P8_Y5_R2FR_3922_DECISION_GATE.csv", "DEC3922_0_combined", "escape combined zero theorem"),
        ("SRC3923_20_escape_bound", SRC / "P8_Y5_R2FR_3922_ESCAPE_BOUND_VECTOR.csv", "ESC3922_9_total", "escape bound vector"),
        ("SRC3923_21_ppn_map", SRC / "P8_Y5_R2FR_3922_ESCAPE_TO_PPN_ORBITAL_MAP.csv", "MAP3922_7_Gdot", "escape to Gdot map"),
        ("SRC3923_22_validation", SRC / "P8_Y5_BRR545_3922_VALIDATION.csv", "VAL3922_14_no_pycache", "3922 validation handoff"),
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


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("THM3923_0_branch", "local branch", "B_loc product/source/stationary branch", "sets the arena where local-GR recovery is attempted", "CONDITIONAL_STACK_NODE"),
        ("THM3923_1_EH", "public metric equation", "S_Q -> EH operator selector => G_mu_nu+Lambda g_mu_nu=8*pi*G_*T_vis", "GR equation recovered if non-EH residuals are absent/topological/double-zero", "CONDITIONAL_STACK_NODE"),
        ("THM3923_2_source", "same-frame source", "T_vis includes matter and Maxwell/EM Hilbert stress in one observed frame", "Newton and EM stress use same public geometry/source denominator", "CONDITIONAL_STACK_NODE"),
        ("THM3923_3_G", "constant local coupling", "G_* zeroform/superselected and B_Meff=0 in stationary source collar", "local dotG channel zero inside stationary branch", "CONDITIONAL_STACK_NODE"),
        ("THM3923_4_Newton", "Newtonian limit", "weak-field slow-motion EH limit gives nabla^2 Phi=4*pi*G_*rho_H and a=-grad Phi", "Newton follows once source normalization is Hilbert-locked", "CONDITIONAL_STACK_NODE"),
        ("THM3923_5_gamma", "gamma", "P_TF[R11_ij]=0 => gamma-1=0", "STF/slip sector closed by EH/DZ/isotropy or bounded", "CONDITIONAL_STACK_NODE"),
        ("THM3923_6_beta", "beta", "B_source=A_source^2 and Delta_sq=0 => beta-1=0", "source square law and common-mode square law closed", "CONDITIONAL_STACK_NODE"),
        ("THM3923_7_common", "common mode", "P00 zero exterior => only universal constant monopole calibration survives", "radial/time/source/frame common-mode pieces become residuals", "CONDITIONAL_STACK_NODE"),
        ("THM3923_8_escape", "boundary/projector/domain/history", "escape silence theorem removes l>=1 multipoles and derivative hair", "otherwise escape bound pack remains live", "CONDITIONAL_STACK_NODE"),
        ("THM3923_9_ppn", "PPN conclusion", PPN_ZERO, "full local PPN vector is zero only if all prior nodes are parent-signed", "CONDITIONAL_CONCLUSION_NOT_CLAIM"),
        ("THM3923_10_total", "local-GR theorem statement", THEOREM, "this is the exact conditional theorem route assembled so far", "PRIVATE_THEOREM_STACK"),
    ]
    return [
        {
            "row_id": row_id,
            "node": node,
            "formula_or_statement": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, node, formula, meaning, status in data
    ]


def signature_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SIG3923_0_parent_normal_form", "product/Q-public normal form", "q_parent(Q,Y,H)=Q and matter/readout use Q_pub/q_src", "3914/3915 branch", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_1_EH_selector", "EH public metric selector", "local, diffeo, second-order, no extra public scalar/vector/tensor operator slots", "3906/3916", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_2_same_frame", "same-frame Hilbert/Maxwell source", "matter, EM stress, clocks, source charge, and orbits use one observed frame", "3906/3914", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_3_Gstar", "constant G_* owner", "zeroform/superselection or equivalent constant local coupling owner", "3909", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_4_Meff", "stationary Hilbert worldtube mass", "B_Meff=0 via Pi_M/H_tau/source collar stack", "3910-3914", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_5_R11", "R11 absence/double-zero/STF silence", "non-EH families absent/topological/double-zero and P_TF=0", "3916/3918", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_6_beta_square", "beta/source square law", "B_source=A_source^2 and common-mode Delta_sq=0", "3919/3920", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_7_P00", "P00 common-mode source silence", "P00[R11]=0 or harmonic exterior leaves only universal monopole", "3921", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_8_boundary", "boundary certificate", "scalar/topological no-flux, no vector/shear/normal exchange, fixed relative class", "3891/3892/3922", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_9_projector", "projector certificate", "fixed topological/metric-independent projector with source equality and no commutator", "3892/3431/3922", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_10_domain", "fixed q-basic domain", "no moving support, no hidden vector marker, no domain derivative stress", "3431/3895/3922", "PARENT_SIGNATURE_REQUIRED"),
        ("SIG3923_11_history", "no incoming history/nonlocal tail", "memory/history tail absent or bounded by suppression law", "3895/3922", "PARENT_SIGNATURE_OR_BOUND_REQUIRED"),
    ]
    return [
        {
            "row_id": row_id,
            "signature_clause": clause,
            "requirement": requirement,
            "source_family": source,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, clause, requirement, source, status in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BND3923_0_gamma", "delta_gamma_R11", "3918 source/STF bound", "abs(delta_gamma_R11) <= gamma bound if P_TF not zero"),
        ("BND3923_1_beta_source", "delta_beta_source", "3919 source square-law fallback", "abs(B_source/A_source^2-1) <= beta bound"),
        ("BND3923_2_beta_common", "delta_beta_common", "3920 Delta_sq fallback", "|Delta_sq|/(1+xi_1)^2 <= beta bound"),
        ("BND3923_3_Xi", "Xi_N/P00/common mode", "3921 Xi_N fill rows", "bound P00, xi0, multipoles, radial/time/source dependence"),
        ("BND3923_4_escape", "B_escape", "3922 boundary/projector/domain/history envelope", "absolute-sum escape bound"),
        ("BND3923_5_Gdot", "Gdot/G", "3908/3914/3920 time common-mode gate", "zero or <= 9.6e-15 yr^-1"),
        ("BND3923_6_alpha", "alpha1/alpha2/alpha3/xi", "3915/3922 PPN map", "zero by no-vector/no-flux/no-multipole or numeric bound"),
        ("BND3923_7_zeta", "zeta_i", "same-frame Hilbert/Bianchi stress", "zero by Hilbert source conservation or non-Hilbert stress bound"),
        ("BND3923_8_total", "B_local", BOUND_PACK, "all components absolute-summed; no fitted cancellation"),
    ]
    return [
        {
            "row_id": row_id,
            "residual": residual,
            "source_gate": gate,
            "bound_or_rule": rule,
            "numeric_value": "",
            "status": "ZERO_OR_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, residual, gate, rule in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3923_0_theorem",
            "decision": "local-GR route is now a coherent conditional theorem stack",
            "formula": THEOREM,
            "claim_status": "PRIVATE_CONDITIONAL_THEOREM_NOT_PUBLIC_CLAIM",
            "next_action": "choose parent-signature adoption route or first numeric bound pack",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3923_1_bound_pack",
            "decision": "if any theorem node fails, use the remaining bound pack",
            "formula": BOUND_PACK,
            "claim_status": "NONCLAIM_BOUND_INTERFACE",
            "next_action": "fill source-backed residuals without cancellation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3923_2_project_state",
            "decision": "we are no longer circling one missing coupling; the local route has named clauses and failure modes",
            "formula": "gamma, beta, common mode, P00, escape channels, Newton, Maxwell and source coupling are linked in one stack",
            "claim_status": "SERIOUS_PRIVATE_FRAMEWORK_PROGRESS_LOCAL_GR_STILL_UNPROMOTED",
            "next_action": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3923_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "attempt the minimal parent action/signature clause that signs the theorem stack; if it fails, start the first source-backed numeric bound pack",
            "why_this_next": "3923 has separated theorem assumptions from fallback residuals; the next decision is adoption versus scoring",
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
            "summary": "local-GR conditional theorem stack assembled with remaining bound pack",
            "sources_found": f"{found}/{len(source_rows)}",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def doc_text(timestamp: str, source_rows: list[dict[str, Any]]) -> str:
    found = sum(row["exists"] and row["needle_found"] for row in source_rows)
    return f"""# 3923 - Local GR Conditional Theorem Stack and Remaining Bound Pack

Timestamp: `{timestamp}`

## Result

The local-GR route is now assembled as a conditional theorem stack:

`{THEOREM}`.

Conditional PPN conclusion:

`{PPN_ZERO}`.

Fallback residual pack:

`{BOUND_PACK}`.

## Meaning

This is not a public local-GR claim. It is the private theorem map we needed: the route to GR/Newton/Maxwell/source coupling is explicit, and each possible failure now has a named residual or bound row. The next step is no longer “find the coupling” in the fog; it is either sign the minimal parent-action clauses, or start filling the first source-backed numeric bound pack.

## Source Register

- Source rows found: `{found}/{len(source_rows)}`
- Register: `source-intake\\mts_residuals\\P8_Y5_R2FR_3923_SOURCE_REGISTER.csv`
- Validation: `source-intake\\mts_residuals\\P8_Y5_BRR545_3923_VALIDATION.csv`

## Generated Tables

- `source-intake\\mts_residuals\\P8_Y5_R2FR_3923_LOCAL_GR_CONDITIONAL_THEOREM_STACK.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3923_PARENT_SIGNATURE_CLAUSES.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3923_REMAINING_BOUND_PACK.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3923_DECISION_GATE.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3923_NEXT_TARGET.csv`

## Next Target

`{NEXT_DOC}`
"""


def spine_block(timestamp: str) -> str:
    return f"""

## 3923 - Local GR Conditional Theorem Stack

Timestamp: `{timestamp}`

- Conditional theorem: `{THEOREM}`.
- PPN conclusion if signed: `{PPN_ZERO}`.
- Fallback bound pack: `{BOUND_PACK}`.
- Status: private conditional theorem stack assembled; no local-GR public claim until parent signatures or source-backed bounds close.
- Next: `{NEXT_DOC}`.
"""


def update_spine(timestamp: str) -> None:
    block = spine_block(timestamp)
    marker = "## 3923 - Local GR Conditional Theorem Stack"
    if SPINE_PATH.exists():
        text = read_text(SPINE_PATH)
        if marker in text:
            before = text.split(marker, 1)[0].rstrip()
            SPINE_PATH.write_text(before + block, encoding="utf-8")
        else:
            SPINE_PATH.write_text(text.rstrip() + block, encoding="utf-8")
    else:
        SPINE_PATH.write_text("# Local GR Coupling Spine - Current State\n" + block, encoding="utf-8")


def validation_rows(timestamp: str, source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theorem = theorem_rows(timestamp)
    signatures = signature_rows(timestamp)
    bounds = bound_rows(timestamp)
    decisions = decision_rows(timestamp)
    paths = list(OUTPUTS.values()) + [DOC_PATH, SCRIPT_PATH, SPINE_PATH]
    checks = [
        ("VAL3923_00_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL3923_01_needles_found", all(row["needle_found"] for row in source_rows), "all cited source needles found"),
        ("VAL3923_02_theorem_nodes", len(theorem) == 11, "local-GR theorem stack rows emitted"),
        ("VAL3923_03_signature_clauses", len(signatures) == 12, "parent signature clauses emitted"),
        ("VAL3923_04_bound_pack", len(bounds) == 9, "remaining bound pack emitted"),
        ("VAL3923_05_ppn_conclusion", any(row["row_id"] == "THM3923_9_ppn" for row in theorem), "PPN zero conclusion emitted"),
        ("VAL3923_06_project_state", any(row["row_id"] == "DEC3923_2_project_state" for row in decisions), "project state decision emitted"),
        ("VAL3923_07_nonclaim", all(str(row.get("valid_for_claim")) == "False" for group in (theorem, signatures, bounds, decisions) for row in group), "all new rows are nonclaim"),
        ("VAL3923_08_outputs_not_fwb", all(not FWB in path.parents for path in paths), "no generated output path is inside formalization-workbench"),
        ("VAL3923_09_doc_written", DOC_PATH.exists(), "checkpoint markdown exists"),
        ("VAL3923_10_spine_written", SPINE_PATH.exists() and "3923 - Local GR Conditional Theorem Stack" in read_text(SPINE_PATH), "spine updated"),
        ("VAL3923_11_next_target", next_rows(timestamp)[0]["next_doc"] == NEXT_DOC, "next target row emitted"),
        ("VAL3923_12_script_compiles", True, "script compiles"),
        ("VAL3923_13_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    write_csv(OUTPUTS["theorem"], theorem_rows(timestamp))
    write_csv(OUTPUTS["signatures"], signature_rows(timestamp))
    write_csv(OUTPUTS["bounds"], bound_rows(timestamp))
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
        raise SystemExit(f"3923 validation failed: {failed}")
    print(f"3923 complete: {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
