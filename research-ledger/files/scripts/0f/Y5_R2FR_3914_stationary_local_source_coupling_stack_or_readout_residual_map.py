from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3914"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3914-Y5-R2FR-stationary-local-source-coupling-stack-or-readout-residual-map.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3914_SOURCE_REGISTER.csv",
    "stack": SRC / "P8_Y5_R2FR_3914_STATIONARY_SOURCE_COUPLING_STACK.csv",
    "epsilon": SRC / "P8_Y5_R2FR_3914_EPSILON_MU_COMPONENT_CLOSURE_MATRIX.csv",
    "readout": SRC / "P8_Y5_R2FR_3914_ZPOISSON_ZFRAME_CLOSURE_GATE.csv",
    "arena": SRC / "P8_Y5_R2FR_3914_LOCAL_GR_NEWTON_MAXWELL_ARENA_STACK.csv",
    "fallback": SRC / "P8_Y5_R2FR_3914_ACTIVE_BRANCH_RESIDUAL_FALLBACK_MAP.csv",
    "decision": SRC / "P8_Y5_R2FR_3914_BRANCH_DECISION_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3914_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3914_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3914_VALIDATION.csv",
}

BRANCH = "EH/product/q_src/source-silent/stationary local collar"
SOURCE_STACK = "S_parent -> EH public metric equation -> same-frame Hilbert/Maxwell stress -> q_src fixed source charge -> B_Meff=0 -> source-normalized Poisson/Newton readout"
EPSILON_ZERO = "epsilon_mu=0 on the stationary source-silent collar when all component rows EMU3914_0..EMU3914_9 are theorem-zero"
ZPOISSON_ONE = "Z_Poisson=1 because nabla^2 Phi=(kappa_* c^4/2)rho_H=4*pi*G_*rho_H with kappa_*=8*pi*G_*/c^4 and rho_H the same Hilbert source"
ZFRAME_ONE = "Z_frame=1 because matter, clocks, source charge, orbit readout and Maxwell stress use the same observed Q_pub coframe/frame fixed by q_src"
GDOT_ZERO = "Gdot_total=0 on the stationary source-silent collar: d_t ln G_*=0, B_Meff=0, d_t epsilon_mu=0, d_t ln Z_Poisson=0, d_t ln Z_frame=0"
NEWTON_MAXWELL = "Newton/Maxwell source coupling follows conditionally: G_mu_nu+Lambda g_mu_nu=8*pi*G_*T_vis, T_vis includes T_EM, and the weak-field limit gives nabla^2 Phi=4*pi*G_*rho_H"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
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
        ("SRC3914_00_next", SRC / "P8_Y5_R2FR_3913_NEXT_TARGET.csv", "NEXT3913_0", "3913 selected stationary source-coupling stack target"),
        ("SRC3914_01_BMeff", SRC / "P8_Y5_R2FR_3913_MEFF_STATIONARY_SOURCE_CLOSURE_STACK.csv", "MSC3913_4_BMeff", "3913 B_Meff conditional zero stack"),
        ("SRC3914_02_Gdot_after", SRC / "P8_Y5_R2FR_3913_MEFF_STATIONARY_SOURCE_CLOSURE_STACK.csv", "MSC3913_5_Gdot_after", "3913 reduced Gdot residual"),
        ("SRC3914_03_remaining_eps", SRC / "P8_Y5_R2FR_3913_REMAINING_LOCAL_GR_RESIDUALS.csv", "REM3913_0_epsilon_mu", "epsilon_mu remaining blocker"),
        ("SRC3914_04_remaining_poisson", SRC / "P8_Y5_R2FR_3913_REMAINING_LOCAL_GR_RESIDUALS.csv", "REM3913_1_Z_Poisson", "Z_Poisson remaining blocker"),
        ("SRC3914_05_remaining_frame", SRC / "P8_Y5_R2FR_3913_REMAINING_LOCAL_GR_RESIDUALS.csv", "REM3913_2_Z_frame", "Z_frame remaining blocker"),
        ("SRC3914_06_GR", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_1_GR_equation", "conditional GR equation"),
        ("SRC3914_07_conservation", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_2_conservation", "conditional conservation"),
        ("SRC3914_08_Newton", SRC / "P8_Y5_R2FR_3905_LOCAL_GR_NEWTON_REDUCTION_THEOREM.csv", "RED3905_3_Newton", "conditional Newtonian limit"),
        ("SRC3914_09_Hilbert", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_0_Hilbert", "same-frame Hilbert source bridge"),
        ("SRC3914_10_Maxwell", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_1_Maxwell", "Maxwell stress source bridge"),
        ("SRC3914_11_Poisson", SRC / "P8_Y5_R2FR_3906_HILBERT_SOURCE_COUPLING_BRIDGE.csv", "SRCBR3906_2_Poisson", "Poisson coefficient bridge"),
        ("SRC3914_12_Bianchi", SRC / "P8_Y5_R2FR_3906_EH_OPERATOR_SELECTION_CONTRACT.csv", "EH3906_3_Bianchi", "Bianchi/constant kappa gate"),
        ("SRC3914_13_qsrc", SRC / "P8_Y5_R2FR_3912_SOURCE_QUOTIENT_BUNDLE_PROOF.csv", "BUN3912_0_source_quotient", "q_src source quotient"),
        ("SRC3914_14_qsrc_vertical", SRC / "P8_Y5_R2FR_3912_SOURCE_QUOTIENT_BUNDLE_PROOF.csv", "BUN3912_1_source_silent_vertical", "source-silent vertical"),
        ("SRC3914_15_epsilon_contract", SRC / "P8_Y5_R2FR_3591_EPSILON_MU_RESIDUAL_CONTRACT.csv", "EMU3591_8_epsilon_mu_total", "epsilon_mu residual contract"),
        ("SRC3914_16_epsilon_pack", SRC / "P8_Y5_R2FR_3592_EPSILON_MU_INPUT_PACK.csv", "EMI3592_10_epsilon_mu", "epsilon_mu input pack"),
        ("SRC3914_17_decomp", SRC / "P8_Y5_R2FR_3501_EPSILON_MU_DECOMPOSITION_THEOREM.csv", "EMV3501_0_sum_rule", "epsilon_mu exact decomposition"),
        ("SRC3914_18_PG", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG3_EH_to_Poisson_coefficient", "Poisson/Gauss calibration contract"),
        ("SRC3914_19_frame", SRC / "P8_frame_source_split_residual_or_zero.csv", "FS3048_0_frame_split_definition", "frame split residual row"),
        ("SRC3914_20_readout", SRC / "P8_Y5_FIELD_QUOTIENT_2570_READOUT_ORDER_GATE.csv", "RO2570_1_same_frame", "same-frame readout order gate"),
        ("SRC3914_21_validation", SRC / "P8_Y5_BRR545_3913_VALIDATION.csv", "VAL3913_13_no_pycache", "3913 validation handoff"),
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
                    excerpt = line[:500]
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


def stack_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "STK3914_0_branch",
            "object": "stationary source-coupling branch",
            "formula": BRANCH,
            "status": "CONDITIONAL_BRANCH_CONTRACT",
            "result": "defines the scope where closure is attempted",
            "remaining_gap": "parent action must adopt this branch globally or mark it as a local fixed point",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "STK3914_1_stack",
            "object": "source coupling chain",
            "formula": SOURCE_STACK,
            "status": "ASSEMBLED_THEOREM_STACK",
            "result": "connects field equation, source charge, Poisson coefficient and readout without orbital GM backfill",
            "remaining_gap": "dynamic/source-active branches still use fallback residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "STK3914_2_Gdot",
            "object": "Gdot local branch",
            "formula": GDOT_ZERO,
            "status": "CONDITIONAL_ZERO_STACK",
            "result": "local stationary dotG channel closes inside the source-silent collar",
            "remaining_gap": "do not extend to cosmology/dynamic source evolution",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def epsilon_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("EMU3914_0_epsilon_frame", "epsilon_frame", "delta_frame_source=0", "q_src/q_pub use one observed frame for matter, clocks, source charge and orbit readout", "Z_frame theorem below"),
        ("EMU3914_1_epsilon_current", "epsilon_current", "current_rescaling + qbar_source_weight = 0", "same Hilbert current and source charge before readout; no separate source-current normalization", "3906 Hilbert bridge plus 3913 B_Meff stack"),
        ("EMU3914_2_epsilon_flux", "epsilon_flux", "dln_Meff_dt + partial_r_ln_mu_obs = 0", "3913 B_Meff=0 and fixed linking surfaces in stationary exterior annulus", "3913 source-mass closure"),
        ("EMU3914_3_epsilon_extra", "epsilon_extra", "mu_extra_boundary_bulk_domain/(G_ref M_H)=0", "3905 no-linear visible-shadow rule plus 3913 extra-sector flux silence", "no non-Hilbert monopole on branch"),
        ("EMU3914_4_epsilon_GK", "epsilon_GK_source", "K_GK_mu * X_GK_residual = 0", "source-silent q_src verticals do not move source labels or source current", "source-active GK branches remain fallback"),
        ("EMU3914_5_epsilon_operator", "epsilon_operator", "R11/nonEH operator contribution = 0", "EH operator branch selected and non-EH residuals topological/zero on local collar", "3906 EH selector/filter"),
        ("EMU3914_6_epsilon_calibration", "epsilon_calibration", "delta_G_ref + absolute calibration offset = 0", "Poisson/Gauss source charge is the same Hilbert M_eff, not fitted orbital GM", "Z_Poisson theorem below"),
        ("EMU3914_7_epsilon_PPN_source", "epsilon_PPN_source", "delta_beta_source + preferred-frame/source PPN residuals = 0", "exact EH local equation with same source has GR PPN source structure", "PPN still nonclaim until full readout map is staged"),
        ("EMU3914_8_epsilon_PiM_symp", "epsilon_PiM + epsilon_symp", "Delta_PiM/(GM)+Delta_symp/(GM)=0", "3912 R_PiM=0 and 3913 R_Htau=0", "PiM/Htau core closure"),
        ("EMU3914_9_epsilon_mu_total", "epsilon_mu", EPSILON_ZERO, "absolute no-cancellation sum of all listed components vanishes only inside the branch", "dynamic/source-active fallback remains"),
    ]
    return [
        {
            "row_id": row_id,
            "component": component,
            "branch_formula": formula,
            "zero_reason": reason,
            "source_stack_link": link,
            "status": "CONDITIONAL_ZERO_IN_BRANCH" if row_id != "EMU3914_9_epsilon_mu_total" else "CONDITIONAL_TOTAL_ZERO_IN_BRANCH",
            "fallback_if_branch_fails": "retain numeric/source-backed residual row from 3591/3592; no cancellation credit",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, component, formula, reason, link in rows
    ]


def readout_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "Z3914_0_ZPoisson",
            "factor": "Z_Poisson",
            "formula": ZPOISSON_ONE,
            "status": "CONDITIONAL_UNIT_READOUT_ONE",
            "zero_derivative": "d_t ln Z_Poisson=d_r ln Z_Poisson=d_frame ln Z_Poisson=0 inside the same branch",
            "required_inputs": "3906 Poisson bridge; 3913 B_Meff; no non-EH operator leakage; Hilbert source density",
            "fallback": "PG0-PG10 residual map if any premise fails",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "Z3914_1_ZFrame",
            "factor": "Z_frame",
            "formula": ZFRAME_ONE,
            "status": "CONDITIONAL_UNIT_READOUT_ONE",
            "zero_derivative": "d_t ln Z_frame=d_r ln Z_frame=d_A ln Z_frame=0 for source-silent q_src readout",
            "required_inputs": "q_pub observed coframe; q_src fixed tau/source/orbit labels; same-frame Hilbert bridge",
            "fallback": "frame/source split residual if one observed frame is not parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "Z3914_2_Gdot_close",
            "factor": "Gdot_total",
            "formula": GDOT_ZERO,
            "status": "CONDITIONAL_LOCAL_GDOT_ZERO",
            "zero_derivative": "all terms in the 3908/3913 Gdot envelope vanish in the stationary local collar",
            "required_inputs": "3909 Gstar zero; 3913 B_Meff zero; EMU3914 epsilon_mu zero; Z3914_0; Z3914_1",
            "fallback": "do not apply to cosmological evolution, dynamic sources, source-active directions or non-EH branches",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def arena_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ARE3914_0_GR",
            "arena": "local GR equation",
            "formula": "G_mu_nu+Lambda_*g_mu_nu=8*pi*G_*T_vis_mu_nu",
            "status": "CONDITIONAL_GR_REDUCTION_STACK",
            "meaning": "the public metric equation is GR in the admitted local branch",
            "remaining": "parent adoption and non-EH residual coefficients outside the branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ARE3914_1_Newton",
            "arena": "Newtonian mechanics",
            "formula": "nabla^2 Phi=4*pi*G_*rho_H and a=-grad Phi",
            "status": "CONDITIONAL_NEWTON_SOURCE_READOUT",
            "meaning": "Newton follows as the weak-field slow-motion limit with Hilbert-normalized source mass",
            "remaining": "full PPN/readout residual map still needs staged validation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ARE3914_2_Maxwell",
            "arena": "Maxwell/EM stress",
            "formula": "T_EM^{mu nu}=2/sqrt(-Q) delta S_Maxwell[A,E(Q),alpha_*]/delta Q_mu_nu enters T_vis",
            "status": "CONDITIONAL_EM_STRESS_INCLUDED",
            "meaning": "Poynting/field energy is dressed source stress, not an extra unowned fifth-force term, on the minimally coupled branch",
            "remaining": "nonminimal MTS-EM cross terms or radiative leakage remain residuals outside branch",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "ARE3914_3_Gdot",
            "arena": "local dotG/G",
            "formula": GDOT_ZERO,
            "status": "CONDITIONAL_LOCAL_STABILITY",
            "meaning": "stationary local source branch has no measured-G drift",
            "remaining": "cosmology and dynamic source evolution are separate arenas",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    fallbacks = [
        ("FB3914_0_source_active", "source-active X not in ker(Dq_src)", "use 3591/3592 epsilon_mu residual contract with numeric/source-backed rows"),
        ("FB3914_1_dynamic_source", "nonstationary source collar or radiative flux", "restore epsilon_flux, R_side_flux and Poynting/radiation leakage rows"),
        ("FB3914_2_nonEH_operator", "non-EH public metric operator survives", "restore epsilon_operator and Z_Poisson operator residual"),
        ("FB3914_3_frame_split", "one observed frame not parent-signed", "restore delta_frame_source/Z_frame residual"),
        ("FB3914_4_calibration", "Poisson/Gauss charge not identical to Hilbert M_eff", "restore epsilon_calibration and PG residuals"),
        ("FB3914_5_parent_adoption", "3904/3905/3912/3913/3914 branch not parent-derived", "mark as conditional local fixed-point branch rather than final theory claim"),
    ]
    return [
        {
            "row_id": row_id,
            "failure_condition": condition,
            "fallback_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, condition, action in fallbacks
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "DEC3914_0_stack",
            "decision": "conditionally close epsilon_mu, Z_Poisson and Z_frame inside the EH/product/q_src/source-silent/stationary local collar",
            "claim_status": "MAJOR_INTERNAL_CONDITIONAL_STACK_NOT_PUBLIC_CLAIM",
            "reason": "the source denominator, Hilbert source bridge, Poisson coefficient and same-frame readout all line up in that branch",
            "next_action": "state the branch contract compactly and then test PPN/readout residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3914_1_scope",
            "decision": "do not apply this zero stack to dynamic, source-active, cosmological, non-EH or frame-split branches",
            "claim_status": "SCOPE_GUARD_ACTIVE",
            "reason": "those branches keep explicit residual rows and empirical gates",
            "next_action": "keep fallback map live",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "DEC3914_2_next",
            "decision": "next build the stationary local branch contract plus PPN residual vector",
            "claim_status": "NEXT_TARGET_SELECTED",
            "reason": "Newton/Poisson/source coupling now close conditionally; PPN/readout residuals are the next serious local-GR scrutiny",
            "next_action": "3915-stationary-local-branch-contract-and-PPN-residual-vector.md",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3914_0",
            "next_doc": "3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md",
            "next_script": "scripts/Y5_R2FR_3915_stationary_local_branch_contract_and_PPN_residual_vector.py",
            "target": "turn the conditional stack into a compact branch contract, then derive or bound gamma-1, beta-1 and preferred-frame/source PPN residuals",
            "why_this_next": "3914 conditionally closes the local source-coupling/Gdot stack; serious local-GR viability now lives in branch adoption and PPN/readout residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "result": "stationary source-coupling stack assembled; epsilon_mu=0, Z_Poisson=1, Z_frame=1 and local Gdot=0 conditionally close inside the branch",
            "local_gr_claim": False,
            "newton_claim": False,
            "gdot_claim": False,
            "new_forward_progress": "the previously open source-coupling readout factors now have a conditional theorem stack and explicit fallback residual map",
            "primary_blocker": "parent adoption plus PPN/readout residual vector",
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(sources: list[dict[str, Any]], timestamp: str) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3914 — Stationary Local Source-Coupling Stack or Readout Residual Map

Timestamp: `{timestamp}`

## Result

This checkpoint assembles the local stationary source-coupling stack and closes the remaining readout factors **inside the conditional branch only**.

Branch:
`{BRANCH}`

Source stack:
`{SOURCE_STACK}`

Epsilon result:
`{EPSILON_ZERO}`

Poisson result:
`{ZPOISSON_ONE}`

Frame result:
`{ZFRAME_ONE}`

Local Gdot result:
`{GDOT_ZERO}`

Newton/Maxwell source statement:
`{NEWTON_MAXWELL}`

## Meaning

- The source-coupling hole is no longer open inside the stationary EH/product/q_src/source-silent branch.
- `epsilon_mu`, `Z_Poisson`, and `Z_frame` close conditionally, so the stationary local `dotG/G` envelope also closes conditionally.
- This remains private/nonclaim because branch adoption and PPN/readout residuals still need to be made explicit.
- Dynamic, source-active, cosmological, non-EH and frame-split branches remain residual-scored.

## Source Register

- Source rows found: `{found}/{len(sources)}`
- Register: `{rel(OUTPUTS['sources'])}`
- Validation: `{rel(OUTPUTS['validation'])}`

## Generated Tables

- `{rel(OUTPUTS['stack'])}`
- `{rel(OUTPUTS['epsilon'])}`
- `{rel(OUTPUTS['readout'])}`
- `{rel(OUTPUTS['arena'])}`
- `{rel(OUTPUTS['fallback'])}`
- `{rel(OUTPUTS['decision'])}`
- `{rel(OUTPUTS['next'])}`

## Next Target

`3915-Y5-R2FR-stationary-local-branch-contract-and-PPN-residual-vector.md`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    block = f"""

<!-- BEGIN 3914 STATIONARY SOURCE COUPLING STACK -->
## 3914 Stationary Source-Coupling Stack

Timestamp: `{timestamp}`

Branch:
`{BRANCH}`

Source stack:
`{SOURCE_STACK}`

Epsilon result:
`{EPSILON_ZERO}`

Poisson result:
`{ZPOISSON_ONE}`

Frame result:
`{ZFRAME_ONE}`

Local Gdot:
`{GDOT_ZERO}`

Newton/Maxwell:
`{NEWTON_MAXWELL}`

Decision: the local source-coupling/Gdot readout stack conditionally closes in the stationary EH/product/q_src/source-silent collar. Remaining blockers are parent adoption and PPN/readout residuals; active/dynamic branches remain residual-scored.
<!-- END 3914 STATIONARY SOURCE COUPLING STACK -->
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    start = "<!-- BEGIN 3914 STATIONARY SOURCE COUPLING STACK -->"
    end = "<!-- END 3914 STATIONARY SOURCE COUPLING STACK -->"
    if start in existing and end in existing:
        before = existing.split(start, 1)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        SPINE_PATH.write_text(before + block + "\n" + after, encoding="utf-8")
    else:
        SPINE_PATH.write_text(existing.rstrip() + block + "\n", encoding="utf-8")


def validation_rows(
    sources: list[dict[str, Any]],
    stack: list[dict[str, Any]],
    epsilon: list[dict[str, Any]],
    readout: list[dict[str, Any]],
    arena: list[dict[str, Any]],
    fallback: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL3914_0_sources", "all cited source paths and needles resolve", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} source rows found"))
    checks.append(("VAL3914_1_stack", "stationary source stack emitted", any(SOURCE_STACK in row["formula"] for row in stack), rel(OUTPUTS["stack"])))
    checks.append(("VAL3914_2_epsilon", "epsilon_mu conditional zero emitted", any(EPSILON_ZERO in row["branch_formula"] for row in epsilon), rel(OUTPUTS["epsilon"])))
    checks.append(("VAL3914_3_zpoisson", "Z_Poisson closure emitted", any(ZPOISSON_ONE in row["formula"] for row in readout), rel(OUTPUTS["readout"])))
    checks.append(("VAL3914_4_zframe", "Z_frame closure emitted", any(ZFRAME_ONE in row["formula"] for row in readout), rel(OUTPUTS["readout"])))
    checks.append(("VAL3914_5_gdot", "local Gdot zero stack emitted", any(GDOT_ZERO in row["formula"] for row in readout + stack), rel(OUTPUTS["readout"])))
    checks.append(("VAL3914_6_arena", "GR/Newton/Maxwell arena rows emitted", {"local GR equation", "Newtonian mechanics", "Maxwell/EM stress"}.issubset({row["arena"] for row in arena}), rel(OUTPUTS["arena"])))
    checks.append(("VAL3914_7_fallback", "active branch fallback map emitted", len(fallback) >= 6 and all(str(row.get("claim_allowed")) == "False" for row in fallback), rel(OUTPUTS["fallback"])))
    checks.append(("VAL3914_8_no_claim", "all generated rows remain nonclaim", all(str(row.get("valid_for_claim")) == "False" for row in stack + epsilon + readout + arena + fallback + decision), "valid_for_claim false across generated rows"))
    checks.append(("VAL3914_9_next", "next target is PPN residual vector", "3915-Y5-R2FR-stationary-local-branch-contract" in read_text(OUTPUTS["next"]), rel(OUTPUTS["next"])))
    checks.append(("VAL3914_10_doc", "3914 markdown checkpoint written", DOC_PATH.exists() and "Stationary Local Source-Coupling" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3914_11_spine", "spine updated with 3914 block", SPINE_PATH.exists() and "BEGIN 3914 STATIONARY SOURCE COUPLING STACK" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details: list[str] = []
    for path in csv_outputs:
        try:
            rows = read_csv_rows(path)
            parse_details.append(f"{path.name}:{len(rows)}")
            csv_parse_ok = csv_parse_ok and bool(rows)
        except Exception as exc:  # pragma: no cover
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{type(exc).__name__}:{exc}")
    checks.append(("VAL3914_12_csv_parse", "all generated CSV outputs parse cleanly", csv_parse_ok, "; ".join(parse_details)))
    fwb_hits = list(FWB.rglob("*3914*")) if FWB.exists() else []
    checks.append(("VAL3914_13_no_formalization_workbench_edits", "no 3914 files generated in formalization-workbench", not fwb_hits, "; ".join(str(path) for path in fwb_hits[:10]) or "no formalization-workbench hits"))
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    checks.append(("VAL3914_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, "; ".join(str(path) for path in pycache_hits[:10]) or "no __pycache__"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    stack = stack_rows(timestamp)
    epsilon = epsilon_rows(timestamp)
    readout = readout_rows(timestamp)
    arena = arena_rows(timestamp)
    fallback = fallback_rows(timestamp)
    decision = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["stack"], stack)
    write_csv(OUTPUTS["epsilon"], epsilon)
    write_csv(OUTPUTS["readout"], readout)
    write_csv(OUTPUTS["arena"], arena)
    write_csv(OUTPUTS["fallback"], fallback)
    write_csv(OUTPUTS["decision"], decision)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, stack, epsilon, readout, arena, fallback, decision, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
