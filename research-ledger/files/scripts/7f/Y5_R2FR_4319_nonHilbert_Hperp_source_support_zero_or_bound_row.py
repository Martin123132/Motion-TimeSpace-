from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4319"
CLAIM_ID = "L-160"
BRANCH = "MTS_R2FR_Y5_NONHILBERT_HPERP_SOURCE_SUPPORT_ZERO_OR_BOUND_ROW_4319"
DECISION = "NSRC_NONHILBERT_REDUCED_TO_HPERP_DQ_SOURCE_PAIRING_ZERO_OR_BOUND_NONCLAIM"
MARKER = "PPC4161_NONHILBERT_HPERP_SOURCE_SUPPORT_ZERO_OR_BOUND_ROW_4319"
PACKET_MARKER = "PPC4161_PACKET_NONHILBERT_HPERP_SOURCE_SUPPORT_ZERO_OR_BOUND_ROW_4319"
NEXT_TARGET = "4320-Y5-R2FR-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md"

FORMAL_PATH = FORMAL / "335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md"
DOC_PATH = POST / "4319-Y5-R2FR-nonHilbert-Hperp-source-support-zero-or-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4319_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4319_00_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4318_NEXT_TARGET.csv",
        "Can N_src_nonHilbert be theorem-zeroed",
        "4318 handoff selecting N_src_nonHilbert/Hperp.",
    ),
    "SRC4319_01_Nsrc_component": (
        FORMAL / "319-PPC4161-source-boundary-silence-or-component-norms-for-m-lock.md",
        "N_src <= ||U_B||_inf ||S_cg_nonHilbert||_{E*}",
        "4303 N_src component norm.",
    ),
    "SRC4319_02_source_anchor": (
        FORMAL / "320-PPC4161-first-source-norms-or-visible-Hilbert-m-lock-signature.md",
        "N_src,strong <= U_B^2 A_src",
        "4304 private source-support anchor.",
    ),
    "SRC4319_03_standard_zero": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "N_src,strong_standard = 0.",
        "4305 standard source-support zero branch.",
    ),
    "SRC4319_04_source_split": (
        FORMAL / "321-PPC4161-source-amplitude-inner-charge-EM-residual-reduction.md",
        "S_A H_L^A = S_A H_perp^A",
        "4305 q-basic source split.",
    ),
    "SRC4319_05_Hperp_bound": (
        FORMAL / "259-PPC4161-Hperp-zero-theorem-or-source-defect-profile-first-real-row.md",
        "|S_A Hperp^A| <= C_S C_perp E_Dq,H",
        "4243 Hperp source-defect bound.",
    ),
    "SRC4319_06_Dq_adoption": (
        FORMAL / "260-PPC4161-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md",
        "all_i Dq_i[H_L]=0",
        "4244 clean zero route.",
    ),
    "SRC4319_07_Dq_bound": (
        FORMAL / "260-PPC4161-Dq-component-zero-adoption-or-Hperp-bound-input-fill.md",
        "|S_A Hperp^A|",
        "4244 finite Dq/Hperp bound route.",
    ),
    "SRC4319_08_Hq_strip": (
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "Dq_i[H_L]",
        "4245 H_q strip: only Hperp carries Dq debt.",
    ),
    "SRC4319_09_component_list": (
        FORMAL / "261-PPC4161-HL-qbasic-strip-and-Dq-bound-first-input-row.md",
        "Dq_source_readout[Hperp]",
        "4245 live Hperp component list.",
    ),
    "SRC4319_10_Nrest": (
        FORMAL / "334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md",
        "N_rest_nonEM^canon :=",
        "4318 canonical residual budget.",
    ),
    "SRC4319_11_Nsrc_priority": (
        FORMAL / "334-PPC4161-nonHilbert-support-drift-history-bound-prioritizer.md",
        "N_src_nonHilbert / Hperp",
        "4318 priority selection.",
    ),
}


def base_row() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
        "claim_allowed": "False",
        "valid_for_claim": "False",
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(col, "")).replace("\n", "<br>").replace("|", "\\|") for col in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = read_text(path) if path.exists() else ""
    if marker in existing:
        return
    with path.open("a", encoding="utf-8", newline="") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        handle.write("\n" + content.strip() + "\n")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path) if path.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr",
        (
            "4319 reduces the first component of N_rest_nonEM^canon, N_src_nonHilbert, to the Hperp source-support "
            "problem. Starting from N_src <= ||U_B||_inf ||S_cg_nonHilbert||, the q-basic strip gives "
            "H_L=H_q+Hperp with Dq_i[H_q]=0, so the non-Hilbert source channel is S_cg_nonHilbert = S_A Hperp^A "
            "plus any explicit source-readout residual. Therefore the exact zero branch is Hperp=0 or "
            "S_A Hperp^A=0 and R_src_readout=0, giving N_src_nonHilbert=0. The fallback is a no-cancellation "
            "bound N_src_nonHilbert <= ||U_B||_inf (C_S C_perp E_Dq,Hperp + ||R_src_readout||), with "
            "E_Dq,Hperp^2=sum_i w_i epsilon_i^2 and epsilon_i>=||Dq_i[Hperp]||. The private U_B^2 A_src_general "
            "anchor is retained as a branch-specific fallback, not a transition-shell proof. No local GR/Newton "
            "claim fires."
        ),
        (
            "4319 source register, Hperp source-support theorem audit, Dq component matrix, bound input schema, "
            "Nrest reduction formulas, runner, firewall, status, next-target and validation CSV."
        ),
        "private_Nsrc_nonHilbert_Hperp_zero_or_Dq_bound_nonclaim",
        (
            "Parent-sign Hperp=0/S_A Hperp^A=0 or source C_S, C_perp, E_Dq,Hperp, component epsilons, "
            "R_src_readout and U_B branch values before scoring local tests."
        ),
        (
            "Using U_B^2 suppression in transition shells without Hperp/Dq ownership, treating component Dq zeros "
            "for a generic v as zeros for H_L, deleting source-readout residuals, or claiming local GR/Newton while "
            "drift/history/boundary/nonlinear/lambda/source-equality/projection gates remain open."
        ),
    ]
    with path.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, purpose) in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        row = base_row()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "purpose": purpose,
            }
        )
        rows.append(row)
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "TH4319_0_start",
            "source-support norm",
            "N_src_nonHilbert <= ||U_B||_inf ||S_cg_nonHilbert||_{E*}",
            "imported from 4303 component ledger",
            "DERIVED_STARTING_ROW",
        ),
        (
            "TH4319_1_Hq_strip",
            "q-basic strip",
            "H_L = H_q + Hperp, H_q in ker(Dq), Hperp=(1-Pi_kerDq)H_L",
            "only Hperp carries non-q source support after quotient stripping",
            "DERIVED_DECOMPOSITION",
        ),
        (
            "TH4319_2_source_pairing",
            "source pairing split",
            "S_cg_nonHilbert = S_A Hperp^A + R_src_readout",
            "R_src_readout is zero only if source/readout factors through q",
            "ZERO_OR_BOUND_SPLIT",
        ),
        (
            "TH4319_3_exact_zero",
            "Nsrc zero branch",
            "Hperp=0 or S_A Hperp^A=0, and R_src_readout=0",
            "N_src_nonHilbert=0",
            "CONDITIONAL_ZERO_ROUTE",
        ),
        (
            "TH4319_4_Dq_bound",
            "Dq/Hperp finite branch",
            "|S_A Hperp^A| <= C_S C_perp E_Dq,Hperp",
            "N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp+||R_src_readout||)",
            "BOUND_ROUTE_READY_INPUTS_MISSING",
        ),
        (
            "TH4319_5_Ub_anchor",
            "private U_B^2 anchor",
            "N_src,strong <= U_B^2 A_src_general",
            "usable only on branch with sourced U_B and A_src_general; not a transition-shell shortcut",
            "BRANCH_SPECIFIC_FALLBACK",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for theorem_id, name, statement, implication, status in specs:
        row = base_row()
        row.update({"theorem_id": theorem_id, "name": name, "statement": statement, "implication": implication, "status": status})
        rows.append(row)
    return rows


def component_rows() -> List[Dict[str, str]]:
    components = [
        ("Dq_geom[Hperp]", "observed geometry/coframe descent"),
        ("Dq_tau[Hperp]", "clock/reference-time descent"),
        ("Dq_matter[Hperp]", "matter action descent"),
        ("Dq_source_readout[Hperp]", "source/readout factorization"),
        ("Dq_theta_marker[Hperp]", "theta/material marker silence"),
        ("Dq_boundary_projector[Hperp]", "boundary/projector ownership"),
        ("Dq_EM[Hperp]", "EM/Hodge/current descent"),
        ("Dq_coeff[Hperp]", "coefficient/normalization marker silence"),
    ]
    rows: List[Dict[str, str]] = []
    for index, (component, meaning) in enumerate(components):
        row = base_row()
        row.update(
            {
                "component_id": f"DC4319_{index}",
                "component": component,
                "meaning": meaning,
                "zero_condition": f"{component}=0 from parent Hperp certificate",
                "bound_input": f"epsilon_{index} >= ||{component}||",
                "status": "MISSING_ZERO_THEOREM_OR_EPSILON_VALUE",
            }
        )
        rows.append(row)
    return rows


def bound_input_rows() -> List[Dict[str, str]]:
    specs = [
        ("BI4319_0_UB", "U_B_inf", "sup norm/projection support coupling for source row", "dimensionless", "real branch value or theorem-zero", "MISSING_BRANCH_VALUE_OR_SCOPE", "False"),
        ("BI4319_1_CS", "C_S", "source pairing operator norm", "operator norm", "positive finite constant", "MISSING_SOURCE_OPERATOR_NORM", "False"),
        ("BI4319_2_Cperp", "C_perp", "Dq inverse/complement constant on Hperp", "operator norm", "positive finite constant", "MISSING_ARENA_PROJECTION", "False"),
        ("BI4319_3_EDq", "E_Dq,Hperp", "combined Hperp Dq defect", "Dq norm", "sqrt(sum_i w_i epsilon_i^2)", "FORMULA_READY_COMPONENT_VALUES_MISSING", "False"),
        ("BI4319_4_Rsrc", "R_src_readout", "source/readout residual not captured by S_A Hperp^A", "source dual norm", "zero theorem or finite bound", "MISSING_ZERO_THEOREM_OR_VALUE", "False"),
        ("BI4319_5_A_src", "A_src_general", "general branch source amplitude", "source amplitude norm", "real value or theorem-zero", "MISSING_PARENT_INPUT", "False"),
        ("BI4319_6_Nsrc", "N_src_nonHilbert", "first canonical non-EM residual component", "m-lock source norm", "zero or finite bound", "NONCLAIM_UNTIL_INPUTS_VALID", "False"),
    ]
    rows: List[Dict[str, str]] = []
    for input_id, symbol, meaning, units, required_value, status, value_valid in specs:
        row = base_row()
        row.update(
            {
                "input_id": input_id,
                "symbol": symbol,
                "meaning": meaning,
                "units_or_norm": units,
                "required_value": required_value,
                "status": status,
                "value_valid_for_claim": value_valid,
            }
        )
        rows.append(row)
    return rows


def formula_rows() -> List[Dict[str, str]]:
    specs = [
        (
            "F4319_0_norm",
            "source support norm",
            "N_src_nonHilbert <= ||U_B||_inf ||S_cg_nonHilbert||_{E*}",
            "4303 component ledger",
            "DERIVED",
        ),
        (
            "F4319_1_split",
            "H_L quotient split",
            "H_L = H_q + Hperp, H_q in ker(Dq), Hperp=(1-Pi_kerDq)H_L",
            "4245 q-basic strip",
            "DERIVED",
        ),
        (
            "F4319_2_source_pairing",
            "source pairing",
            "S_cg_nonHilbert = S_A Hperp^A + R_src_readout",
            "4319 source/readout split",
            "ZERO_OR_BOUND_FORMULA",
        ),
        (
            "F4319_3_zero",
            "exact Nsrc zero",
            "if Hperp=0 or S_A Hperp^A=0, and R_src_readout=0, then N_src_nonHilbert=0",
            "Dq/Hperp plus source-factor theorem",
            "CONDITIONAL_ZERO",
        ),
        (
            "F4319_4_EDq",
            "combined Dq defect",
            "E_Dq,Hperp^2 := sum_i w_i epsilon_i^2, epsilon_i >= ||Dq_i[Hperp]||",
            "4244/4245 finite branch",
            "FORMULA_READY_VALUES_MISSING",
        ),
        (
            "F4319_5_bound",
            "Hperp source bound",
            "N_src_nonHilbert <= ||U_B||_inf (C_S C_perp E_Dq,Hperp + ||R_src_readout||)",
            "main finite 4319 result",
            "BOUND_READY_INPUTS_MISSING",
        ),
        (
            "F4319_6_Ub2",
            "private source-power fallback",
            "N_src_nonHilbert <= U_B^2 A_src_general",
            "4304/4305 branch-specific fallback",
            "FALLBACK_READY_VALUES_MISSING",
        ),
        (
            "F4319_7_Nrest_reduced",
            "canonical budget after Nsrc zero",
            "N_rest_nonEM^canon -> N_drift_selector + N_history_transition + N_boundary_domain + N_N",
            "4318 plus F4319_3",
            "CONDITIONAL_REDUCTION",
        ),
        (
            "F4319_8_Nrest_bound",
            "canonical budget with finite Nsrc",
            "N_rest_nonEM^canon <= ||U_B||_inf(C_S C_perp E_Dq,Hperp+||R_src_readout||)+N_drift_selector+N_history_transition+N_boundary_domain+N_N",
            "4318 plus F4319_5",
            "BOUND_HANDOFF_READY_INPUTS_MISSING",
        ),
    ]
    rows: List[Dict[str, str]] = []
    for formula_id, name, formula, basis, status in specs:
        row = base_row()
        row.update({"formula_id": formula_id, "name": name, "formula": formula, "basis": basis, "status": status})
        rows.append(row)
    return rows


def runner_rows() -> List[Dict[str, str]]:
    specs = [
        ("RUN4319_0_current", "current corpus, Hperp component values not sourced", "USE_BOUND_SCHEMA", "N_src_nonHilbert is formula-ready but not claim-valid", "no local claim"),
        ("RUN4319_1_zero_branch", "Hperp/source-readout zero theorem signed", "ALLOW_NSRC_ZERO", "N_rest_nonEM^canon loses N_src_nonHilbert", "next attack drift selector"),
        ("RUN4319_2_Dq_bound", "component epsilons and constants sourced", "ALLOW_NONCLAIM_FINITE_BOUND", "N_src_nonHilbert finite and feedable into local tests", "claim only after full route gates"),
        ("RUN4319_3_Ub2_fallback", "U_B and A_src_general sourced in a local non-transition branch", "ALLOW_BRANCH_FALLBACK", "N_src_nonHilbert <= U_B^2 A_src_general", "reject for transition shell if U_B not small"),
        ("RUN4319_4_invalid_shortcut", "component theorems for generic v used as H_L certificates without adoption", "REJECT", "no score", "prevents smuggled closure"),
    ]
    rows: List[Dict[str, str]] = []
    for runner_id, scenario, action, output, note in specs:
        row = base_row()
        row.update({"runner_id": runner_id, "scenario": scenario, "action": action, "output": output, "note": note})
        rows.append(row)
    return rows


def firewall_rows() -> List[Dict[str, str]]:
    specs = [
        ("FW4319_0", "Do not promote Dq_i[v]=0 component theorems to Dq_i[H_L]=0 without an H_L argument certificate.", "ACTIVE"),
        ("FW4319_1", "Do not use U_B^2 suppression in transition shells unless U_B, A_src and Hperp ownership are sourced for that branch.", "ACTIVE"),
        ("FW4319_2", "Do not delete R_src_readout; source/readout nonfactorization is part of N_src_nonHilbert.", "ACTIVE"),
        ("FW4319_3", "Do not collapse E_Dq,Hperp to one component unless the other seven components are zero or bounded.", "ACTIVE"),
        ("FW4319_4", "Do not claim local GR/Newton after N_src closes; drift/history/boundary/nonlinear/lambda/source-equality/projection gates remain.", "ACTIVE"),
    ]
    rows: List[Dict[str, str]] = []
    for firewall_id, rule, status in specs:
        row = base_row()
        row.update({"firewall_id": firewall_id, "rule": rule, "status": status})
        rows.append(row)
    return rows


def decision_rows() -> List[Dict[str, str]]:
    specs = [
        ("DEC4319_0_gain", "NSRC_REDUCED_TO_HPERP_SOURCE_PAIRING", "N_src_nonHilbert now has a precise source-pairing object S_A Hperp^A plus residual.", "use F4319_5 or prove F4319_3"),
        ("DEC4319_1_zero", "ZERO_ROUTE_EXPLICIT", "Hperp=0 or S_A Hperp^A=0 with R_src_readout=0 kills N_src_nonHilbert.", "try Hperp component certificate next"),
        ("DEC4319_2_bound", "DQ_BOUND_ROUTE_EXPLICIT", "finite route is controlled by C_S C_perp E_Dq,Hperp and source-readout residual.", "source component epsilons if theorem route fails"),
        ("DEC4319_3_guard", "UB2_NOT_GLOBAL", "U_B^2 A_src is branch-specific and not a transition-shell proof.", "retain firewall"),
        ("DEC4319_4_next", "DQ_COMPONENT_CERTIFICATE_NEXT", "The next concrete work is proving/filling Dq_i[Hperp] component rows.", NEXT_TARGET),
        ("DEC4319_5_claim", "NO_LOCAL_CLAIM", "This closes/bounds only the first N_rest component.", "keep all claim flags false"),
    ]
    rows: List[Dict[str, str]] = []
    for decision_id, result, reason, next_action in specs:
        row = base_row()
        row.update({"decision_id": decision_id, "result": result, "reason": reason, "next_action": next_action})
        rows.append(row)
    return rows


def status_rows() -> List[Dict[str, str]]:
    specs = [
        ("STAT4319_0_Nsrc", "N_src_nonHilbert", "ZERO_OR_BOUND_FORMULA_READY", "needs Hperp zero or Dq component inputs"),
        ("STAT4319_1_Hperp", "Hperp", "PRIMARY_OBJECT", "non-q defect after H_q strip"),
        ("STAT4319_2_EDq", "E_Dq,Hperp", "VALUES_MISSING", "component epsilons not sourced"),
        ("STAT4319_3_Rsrc", "R_src_readout", "OPEN_ZERO_OR_BOUND", "source/readout factorization needed"),
        ("STAT4319_4_Nrest", "N_rest_nonEM^canon", "REDUCIBLE_IF_NSRC_ZERO", "then drift/history/boundary/N_N remain"),
        ("STAT4319_5_local", "local GR/Newton", "BLOCKED", "many downstream gates remain"),
    ]
    rows: List[Dict[str, str]] = []
    for status_id, obj, status, note in specs:
        row = base_row()
        row.update({"status_id": status_id, "object": obj, "status": status, "note": note})
        rows.append(row)
    return rows


def next_rows() -> List[Dict[str, str]]:
    row = base_row()
    row.update(
        {
            "next_target_id": "NT4319_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the eight Dq_i[Hperp] component rows be theorem-zeroed, starting with source/readout and geometry, or must first epsilon_i profile rows be filled?",
            "preferred_route": "prove Hperp is q-basic/in kernel for the needed component maps in the local source branch",
            "fallback_route": "fill nonclaim epsilon_i, C_S, C_perp and R_src_readout rows and route finite N_src into N_rest_nonEM^canon",
        }
    )
    return [row]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 335 PPC4161 nonHilbert Hperp source support zero or bound row

Marker: `{MARKER}`

## Decision

`{DECISION}`

4319 attacks the first component of `N_rest_nonEM^canon`:

```text
N_src_nonHilbert <= ||U_B||_inf ||S_cg_nonHilbert||_E*
```

The quotient split is:

```text
H_L = H_q + Hperp,
H_q in ker(Dq),
Hperp = (1-Pi_kerDq)H_L.
```

The useful source-pairing split is:

```text
S_cg_nonHilbert = S_A Hperp^A + R_src_readout.
```

Hence the exact branch is:

```text
Hperp=0 or S_A Hperp^A=0,
R_src_readout=0
=> N_src_nonHilbert=0.
```

If that does not close, the finite no-cancellation branch is:

```text
E_Dq,Hperp^2 := sum_i w_i epsilon_i^2,
epsilon_i >= ||Dq_i[Hperp]||,
N_src_nonHilbert <= ||U_B||_inf (C_S C_perp E_Dq,Hperp + ||R_src_readout||).
```

The old private anchor `N_src <= U_B^2 A_src_general` is retained only as a branch-specific fallback, not as a global transition-shell proof.

## Theorem Audit
{md_table(tables["theorem"], ["theorem_id", "name", "statement", "implication", "status"])}

## Dq Component Matrix
{md_table(tables["components"], ["component_id", "component", "meaning", "zero_condition", "bound_input", "status"])}

## Bound Inputs
{md_table(tables["bounds"], ["input_id", "symbol", "meaning", "units_or_norm", "required_value", "status", "value_valid_for_claim"])}

## Reduced Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "basis", "status"])}

## Runner
{md_table(tables["runner"], ["runner_id", "scenario", "action", "output", "note"])}

## Result

The first `N_rest_nonEM^canon` row is now cleanly reduced. If the Hperp/source-readout theorem closes, `N_src_nonHilbert=0`; otherwise it becomes a finite Dq/Hperp profile budget. No local GR/Newton claim fires.

Next target: `{NEXT_TARGET}`.
"""
    post = f"""# 4319 - nonHilbert Hperp source support zero or bound row

## Verdict

- `N_src_nonHilbert` is reduced to `S_A Hperp^A + R_src_readout`.
- Exact zero branch: `Hperp=0` or `S_A Hperp^A=0`, plus `R_src_readout=0`.
- Finite branch: `N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp + ||R_src_readout||)`.
- `U_B^2 A_src_general` is retained only as a branch-specific fallback, not a global transition-shell proof.

## Source Register
{md_table(tables["sources"], ["source_id", "source_path", "exists", "needle_found", "purpose"])}

## Theorem Audit
{md_table(tables["theorem"], ["theorem_id", "name", "statement", "status"])}

## Dq Component Matrix
{md_table(tables["components"], ["component", "zero_condition", "bound_input", "status"])}

## Bound Inputs
{md_table(tables["bounds"], ["symbol", "required_value", "status"])}

## Reduced Formulas
{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Decision
{md_table(tables["decision"], ["decision_id", "result", "reason", "next_action"])}

## Status
{md_table(tables["status"], ["status_id", "object", "status", "note"])}

## Next Target
{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def validate_csv(path: Path) -> Tuple[bool, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
    except Exception as exc:
        return False, f"csv parse failed: {exc}"
    if not rows:
        return False, "csv has no data rows"
    return True, f"csv parsed rows={len(rows)}"


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        row = base_row()
        row.update({"check_id": check_id, "description": description, "passed": str(passed), "evidence": evidence})
        rows.append(row)

    add("VAL4319_sources_exist", "all source paths exist", all(r["exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4319_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4319_theorem_zero", "zero theorem row exists", any(r["theorem_id"] == "TH4319_3_exact_zero" and "N_src_nonHilbert=0" in r["implication"] for r in tables["theorem"]), "theorem")
    add("VAL4319_bound_theorem", "Dq/Hperp bound theorem exists", any("C_S C_perp E_Dq,Hperp" in r["implication"] for r in tables["theorem"]), "theorem")
    add("VAL4319_components_8", "eight Dq components listed", len(tables["components"]) == 8, "components")
    add("VAL4319_source_readout_component", "source readout component included", any("source_readout" in r["component"] for r in tables["components"]), "components")
    add("VAL4319_inputs_nonclaim", "all bound inputs nonclaim", all(r["value_valid_for_claim"] == "False" for r in tables["bounds"]), "bounds")
    add("VAL4319_main_bound", "main Nsrc bound formula present", any("N_src_nonHilbert <= ||U_B||_inf" in r["formula"] and "R_src_readout" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4319_Nrest_handoff", "Nrest handoff formulas present", any(r["formula_id"] == "F4319_8_Nrest_bound" for r in tables["formulas"]), "formulas")
    add("VAL4319_runner_reject", "runner rejects generic-v shortcut", any(r["runner_id"] == "RUN4319_4_invalid_shortcut" and r["action"] == "REJECT" for r in tables["runner"]), "runner")
    add("VAL4319_firewall_transition", "firewall blocks transition U_B shortcut", any("transition shells" in r["rule"] for r in tables["firewall"]), "firewall")
    add("VAL4319_claim_false", "all rows keep claim flags false", all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for table in tables.values() for row in table), "all_tables")
    add("VAL4319_next_target", "next target is 4320", any("4320" in r["next_target"] for r in tables["next"]), "next")
    for name, path in paths.items():
        if name == "validation":
            continue
        ok, detail = validate_csv(path)
        add(f"VAL4319_csv_{name}", detail, ok, "generated_artifacts")
    add("VAL4319_docs", "formal and post checkpoint docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4319_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4319_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4319_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")
    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4319_SOURCE_REGISTER.csv",
        "theorem": SOURCE_DIR / "P8_Y5_R2FR_4319_HPERP_SOURCE_THEOREM_AUDIT.csv",
        "components": SOURCE_DIR / "P8_Y5_R2FR_4319_DQ_COMPONENT_MATRIX.csv",
        "bounds": SOURCE_DIR / "P8_Y5_R2FR_4319_NSRC_BOUND_INPUT_SCHEMA.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4319_REDUCED_NREST_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4319_LOCAL_ROUTE_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4319_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4319_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4319_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4319_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "theorem": theorem_rows(),
        "components": component_rows(),
        "bounds": bound_input_rows(),
        "formulas": formula_rows(),
        "runner": runner_rows(),
        "firewall": firewall_rows(),
        "decision": decision_rows(),
        "status": status_rows(),
        "next": next_rows(),
    }
    for key, rows in tables.items():
        write_csv(paths[key], rows)
    write_docs(tables)
    append_claim_once()
    append_once(
        FORMAL / "07-unification-spine.md",
        MARKER,
        f"""
## PPC4161 4319 nonHilbert Hperp source support zero or bound row

Marker: `{MARKER}`

4319 reduces `N_src_nonHilbert` to the Hperp source-pairing problem. With `H_L=H_q+Hperp`, `H_q in ker(Dq)`, the non-Hilbert source channel is `S_cg_nonHilbert = S_A Hperp^A + R_src_readout`. Thus `Hperp=0` or `S_A Hperp^A=0`, together with `R_src_readout=0`, gives `N_src_nonHilbert=0`; otherwise `N_src_nonHilbert <= ||U_B||_inf(C_S C_perp E_Dq,Hperp+||R_src_readout||)`. The `U_B^2 A_src_general` anchor remains branch-specific and is not a transition-shell shortcut.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4319 packet nonHilbert Hperp source support

Marker: `{PACKET_MARKER}`

Packet update: the first canonical non-EM residual row is now `Hperp` source pairing. Prove `Hperp`/`S_A Hperp^A` zero plus source-readout factorization, or pay the finite `C_S C_perp E_Dq,Hperp` profile cost.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} evidence={row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
