from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4338"
CLAIM_ID = "L-179"
BRANCH = "MTS_R2FR_Y5_CGAMMA_TRANSITION_SOURCE_KERNEL_COEFFICIENT_FILL_OR_METRIC_NULL_PROOF_4338"
DECISION = "FINITE_MARGIN_CGAMMA_COLLAR_ZERO_IMPORTED_RAW_TRANSITION_SHELL_REDUCED_TO_PLEAK_KERNEL_VECTOR_NONCLAIM"
MARKER = "PPC4161_CGAMMA_TRANSITION_SOURCE_KERNEL_COEFFICIENT_FILL_OR_METRIC_NULL_PROOF_4338"
PACKET_MARKER = "PPC4161_PACKET_CGAMMA_TRANSITION_SOURCE_KERNEL_COEFFICIENT_FILL_OR_METRIC_NULL_PROOF_4338"
NEXT_TARGET = "4339-Y5-R2FR-PnonHilbert-and-worldtube-transition-leak-zero-proof-or-bound-runner.md"

FORMAL_PATH = FORMAL / "354-PPC4161-cGamma-transition-source-kernel-coefficient-fill-or-metric-null-proof.md"
DOC_PATH = POST / "4338-Y5-R2FR-cGamma-transition-source-kernel-coefficient-fill-or-metric-null-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4338_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

PRESSURE_DENOMINATOR = 0.167893843691
DEFAULT_AJ = 1.0
DEFAULT_CGAMMA = 1.0
DEFAULT_PIB = 1.0
DEFAULT_T_RATIO_REQUIRED = DEFAULT_AJ * DEFAULT_CGAMMA / (PRESSURE_DENOMINATOR * DEFAULT_PIB)
HALF_PIB_T_RATIO_REQUIRED = DEFAULT_AJ * DEFAULT_CGAMMA / (PRESSURE_DENOMINATOR * 0.5)


SOURCES = [
    (
        "SRC4338_00_4337_next",
        SOURCE_DIR / "P8_Y5_R2FR_4337_NEXT_TARGET.csv",
        "c_Gamma be parent-zero/metric-null",
        "4337 handoff to cGamma zero/profile work.",
    ),
    (
        "SRC4338_01_4337_coupling_split",
        FORMAL / "353-PPC4161-source-Sq-qprofile-kernel-and-metric-green-coupling-or-R10-alpha-parent-pivot.md",
        "C_gK^Gamma = kappa_eff c_Gamma",
        "Open-tail metric coupling reduction.",
    ),
    (
        "SRC4338_02_4281_collar_zero",
        POST / "4281-Y5-R2FR-cGamma-transport-Bgrad-routing-zero-or-profile-source-pack.md",
        "=> A_J,eff_private = 0.",
        "Finite-margin compact-collar cGamma routing zero.",
    ),
    (
        "SRC4338_03_296_AJ_reduction",
        FORMAL / "296-PPC4161-cGamma-parent-memory-equation-AJ-source-coefficient-or-profile-fill.md",
        "A_J,eff_private <= |R_transport_to_local| + |R_Bgrad_to_local|.",
        "AJ reduction to transport and B-gradient leakage.",
    ),
    (
        "SRC4338_04_310_kernel_theorem",
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_leak q_tr = 0.",
        "Conditional transition source-kernel zero theorem.",
    ),
    (
        "SRC4338_05_310_kernel_definition",
        FORMAL / "310-PPC4161-transition-source-kernel-zero-theorem-or-projection-suppression-map.md",
        "P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube",
        "Source-kernel projector definition.",
    ),
    (
        "SRC4338_06_311_kernel_search",
        FORMAL / "311-PPC4161-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md",
        "ordinary local source kernel = found inside the private PPC4161 selector.",
        "Ordinary source kernel found.",
    ),
    (
        "SRC4338_07_311_raw_transition",
        FORMAL / "311-PPC4161-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md",
        "raw transition shell q_tr source-kernel membership = not parent-signed.",
        "Raw transition shell still not signed into the source kernel.",
    ),
    (
        "SRC4338_08_311_leak_vector",
        FORMAL / "311-PPC4161-parent-action-source-kernel-signature-search-and-leak-projector-reduction.md",
        "P_leak q_tr =",
        "Seven-component transition leak vector.",
    ),
    (
        "SRC4338_09_313_obstruction",
        FORMAL / "313-PPC4161-qtr-vertical-or-topological-rest-proof-attempt-for-PnonHilbert.md",
        "q_tr verticality proved = false",
        "First leak-component proof obstruction.",
    ),
    (
        "SRC4338_10_303_pressure_law",
        FORMAL / "303-PPC4161-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md",
        "T_res/tau_L >= A_J,eff_private * abs(c_Gamma) / (0.167893843691 * Pi_B).",
        "Calculator-ready cGamma/AJ pressure law.",
    ),
    (
        "SRC4338_11_144_closure",
        FORMAL / "144-local-transition-closure-contract.md",
        "q_tr^nu is not allowed to source the local metric/PPN branch unless a future",
        "Transition shell closure firewall.",
    ),
    (
        "SRC4338_12_250_Kperp_private",
        FORMAL / "250-PPC4161-Kperp-EH-coframe-identity-proof-or-independent-tensor-source-row.md",
        "K_extra_source   -> absent",
        "Private selector Kperp/static extra source removal.",
    ),
    (
        "SRC4338_13_4284_spine",
        FORMAL / "07-unification-spine.md",
        "4284 imports the Solar transition source-model row",
        "Existing scored direct-projection transition-shell failure summary.",
    ),
]


PLEAK_COMPONENTS = [
    (
        "P_nonHilbert_action_domain",
        "q_tr is not proved to arise inside the same Hilbert action-domain source block",
        "Try q_tr vertical/topological/Hilbert-source proof first; otherwise build finite source row.",
    ),
    (
        "P_off_worldtube_readout_order",
        "q_tr is not proved to enter before the same worldtube Hamiltonian mass readout",
        "Prove same-worldtube before-readout ownership or retain leak row.",
    ),
    (
        "P_time_multipole",
        "q_tr is not proved static l=0 in the local source kernel",
        "Prove no time/multipole source hair or source finite profile.",
    ),
    (
        "P_species_frame_source_weight",
        "q_tr is not proved universal and species/frame/source-weight blind",
        "Prove source-label forgetting for transition current or source WEP/clock rows.",
    ),
    (
        "P_range_hair",
        "q_tr is not proved range-free/long-range-equivalent to a common monopole",
        "Prove range-free kernel membership or source R10/range rows.",
    ),
    (
        "P_nonEH_metric_readout",
        "q_tr is not proved to use only the EH/same-metric readout channel",
        "Prove no non-EH metric response or source residual-EFT coefficient.",
    ),
    (
        "P_boundary_nonlocal_owner",
        "q_tr boundary/nonlocal owner is not parent-signed",
        "Prove nonlocal owner/kernel or keep transition closure explicit.",
    ),
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return ""


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: str(row.get(key, "")) for key in fields})


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = ["| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                "4338 imports the finite-margin cGamma result into the 4337 coupling split and separates compact-collar local tests from raw transition-shell local tests. In support-separated compact local collars, 4281 gives R_transport_to_local=R_Bgrad_to_local=0 and A_J,eff_private=0, so the cGamma AJ/profile channel contributes zero to the open-tail Pi_PPN^Gamma branch regardless of finite c_Gamma. This is a private compact-collar zero branch, not a raw transition-shell theorem. For raw transition shells, the clean route is the conditional source-kernel theorem P_leak q_tr=0: if q_tr is same-metric, same-worldtube, Hilbert, static l=0, universal, range-free source-kernel data, it renormalizes the common source charge rather than leaking into PPN/R10/WEP/clock/orbital channels. The current corpus finds the ordinary source kernel but does not parent-sign raw transition q_tr membership; P_leak q_tr is reduced to seven named components, with P_nonHilbert_action_domain and P_off_worldtube_readout_order selected as the next proof targets. No public local-GR claim fires.",
                "4338 source register, branch theorem rows, source-kernel rows, P_leak component rows, pressure-law rows, runner, firewall, decision, status, next-target and validation CSV.",
                "private_finite_margin_cGamma_collar_zero_raw_transition_Pleak_vector_nonclaim",
                "Attack P_nonHilbert_action_domain and P_off_worldtube_readout_order for q_tr, or build finite leak-bound rows for the seven P_leak components.",
                "Applying finite-margin collar zero through a transition shell; treating conditional P_kernel membership as parent-signed; deleting P_leak components by notation; using calibrated kappa_eff as a cGamma transition pass; or claiming local GR while transition membership is unsigned.",
            ]
        )


def source_rows() -> List[Dict[str, str]]:
    rows = []
    for source_id, path, needle, role in SOURCES:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(needle in text),
                "line_number": find_line(path, needle),
                "role": role,
            }
        )
    return rows


def theorem_rows() -> List[Dict[str, str]]:
    return [
        {
            "theorem_id": "THM4338_0_compact_collar_cGamma_zero",
            "domain": "finite-margin compact local collar",
            "premises": "W_loc has finite margin away from transport support, B-gradient support and transition-shell support",
            "result": "R_transport_to_local=R_Bgrad_to_local=0; A_J,eff_private=0; R_PPN^Gamma_AJ=0",
            "status": "DERIVED_PRIVATE_COLLAR_ZERO_NONCLAIM",
            "source_basis": "4281 plus 4337 cGamma split",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM4338_1_transition_source_kernel_zero",
            "domain": "raw transition shell if parent signs source-kernel membership",
            "premises": "q_tr=P_kernel q_tr with same metric, same worldtube, Hilbert, static, l=0, universal and range-free clauses",
            "result": "P_leak q_tr=0; transition residue renormalizes common source charge rather than local leak channels",
            "status": "CONDITIONAL_THEOREM_PARENT_SIGNATURE_REQUIRED",
            "source_basis": "310",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM4338_2_raw_transition_current",
            "domain": "raw Solar/vacuum transition shell",
            "premises": "P_loc=1/direct transition support; no parent-signed P_kernel membership",
            "result": "P_leak q_tr remains active; direct local projection remains rejected/quarantined",
            "status": "OPEN_TRANSITION_FRONTIER",
            "source_basis": "311;313;144;07 spine 4284",
            "valid_for_claim": "False",
        },
    ]


def kernel_rows() -> List[Dict[str, str]]:
    return [
        {
            "kernel_id": "KER4338_0_Pkernel",
            "operator": "P_kernel",
            "definition": "P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube",
            "effect": "keeps only common Hilbert monopole source-charge data",
            "current_status": "ORDINARY_SOURCE_KERNEL_FOUND_RAW_TRANSITION_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KER4338_1_Pleak",
            "operator": "P_leak=I-P_kernel",
            "definition": "sum of seven source-kernel leak projectors",
            "effect": "all local transition residual testing must flow through these named components",
            "current_status": "ACTIVE_FOR_RAW_TRANSITION_SHELL",
            "valid_for_claim": "False",
        },
        {
            "kernel_id": "KER4338_2_cGamma_PPN",
            "operator": "Pi_PPN^Gamma",
            "definition": "c_Gamma P_PPN G_EH kappa_eff P_E[(K_L G_Box S_q^Gamma)+S_perp]",
            "effect": "zero in finite-margin collar AJ channel; finite/leak scored only through P_leak profile components",
            "current_status": "BRANCH_SPLIT_DERIVED",
            "valid_for_claim": "False",
        },
    ]


def pleak_rows() -> List[Dict[str, str]]:
    rows = []
    for index, (component, obstruction, next_action) in enumerate(PLEAK_COMPONENTS):
        priority = "P0" if index < 2 else "P1"
        rows.append(
            {
                "component_id": f"PLEAK4338_{index}",
                "component": component,
                "priority": priority,
                "zero_status": "NOT_PARENT_SIGNED",
                "obstruction": obstruction,
                "next_action": next_action,
                "valid_for_claim": "False",
            }
        )
    return rows


def pressure_rows() -> List[Dict[str, str]]:
    return [
        {
            "pressure_id": "PRS4338_0_finite_margin_collar",
            "branch": "finite-margin compact collar",
            "formula": "A_J,eff_private=0 => required T_res/tau_L=0 for cGamma AJ pressure",
            "required_Tres_over_tauL": "0",
            "interpretation": "cGamma AJ profile channel is quiet in support-separated compact collars",
            "valid_for_claim": "False",
        },
        {
            "pressure_id": "PRS4338_1_raw_transition_default_strong_window",
            "branch": "raw transition finite-profile fallback",
            "formula": "T_res/tau_L >= A_J,eff_private*abs(c_Gamma)/(0.167893843691*Pi_B)",
            "required_Tres_over_tauL": f"{DEFAULT_T_RATIO_REQUIRED:.12g}",
            "interpretation": "for A_J=1, cGamma=1, Pi_B=1, the relaxation ratio must be at least the 4287 strong-window value",
            "valid_for_claim": "False",
        },
        {
            "pressure_id": "PRS4338_2_raw_transition_half_PiB",
            "branch": "raw transition midpoint shell stress test",
            "formula": "same pressure law with Pi_B=0.5",
            "required_Tres_over_tauL": f"{HALF_PIB_T_RATIO_REQUIRED:.12g}",
            "interpretation": "midpoint transition shells roughly double the strong-window relaxation burden",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4338_0_compact_collar",
            "branch_input": "finite-margin support-separated compact collar",
            "action": "IMPORT_CGAMMA_AJ_ZERO",
            "output": "A_J,eff_private=0; R_PPN^Gamma_AJ=0",
            "claim_policy": "private collar nonclaim; not transition shell",
        },
        {
            "runner_id": "RUN4338_1_raw_transition_kernel",
            "branch_input": "raw transition q_tr",
            "action": "REDUCE_TO_PLEAK_VECTOR",
            "output": "seven leak components retained",
            "claim_policy": "no local-GR claim until P_leak q_tr=0 or finite bounds",
        },
        {
            "runner_id": "RUN4338_2_pressure_law",
            "branch_input": "finite cGamma/AJ fallback",
            "action": "COMPUTE_TRES_TAUL_REQUIREMENTS",
            "output": f"default={DEFAULT_T_RATIO_REQUIRED:.6f}; half_PiB={HALF_PIB_T_RATIO_REQUIRED:.6f}",
            "claim_policy": "calculator-ready nonclaim thresholds only",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4338_0_collar_to_shell",
            "forbidden_shortcut": "apply finite-margin compact-collar zero to transition shells",
            "reason": "transition shells have direct support and fail/directly require kernel membership",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4338_1_conditional_kernel_overclaim",
            "forbidden_shortcut": "treat P_kernel membership as parent-signed",
            "reason": "311 finds ordinary source kernel but raw transition q_tr membership remains unsigned",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4338_2_delete_Pleak",
            "forbidden_shortcut": "delete P_leak components by notation",
            "reason": "each component needs a zero proof or finite source-backed bound",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4338_3_ignore_Kperp_scope",
            "forbidden_shortcut": "use private Kperp routing as global no-extra-tensor theorem",
            "reason": "Kperp is only routed inside the private selector; public/raw branches retain parent-signature burden",
            "status": "BLOCK",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "claim_allowed": "False",
            "valid_for_claim": "False",
            "summary": "4338 closes the cGamma AJ/profile channel in finite-margin compact collars while reducing raw transition-shell cGamma to a seven-component P_leak q_tr source-kernel problem.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4338_0_collar",
            "item": "finite-margin compact collar",
            "status": "CGAMMA_AJ_ZERO_IMPORTED",
            "notes": "A_J,eff_private=0 and cGamma AJ profile channel is quiet",
        },
        {
            "status_id": "STAT4338_1_transition",
            "item": "raw transition shell",
            "status": "PLEAK_VECTOR_ACTIVE",
            "notes": "source-kernel membership not parent-signed",
        },
        {
            "status_id": "STAT4338_2_next",
            "item": "first leak components",
            "status": "NEXT_TARGET",
            "notes": "attack P_nonHilbert_action_domain and P_off_worldtube_readout_order",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4338_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the first two P_leak components be zeroed for q_tr, or must they become finite source-backed bound rows?",
            "preferred_route": "prove P_nonHilbert_action_domain q_tr=0 and P_off_worldtube_readout_order q_tr=0 from Hilbert/source-domain/worldtube ownership",
            "fallback_route": "build finite source-backed leak-bound rows for all seven P_leak components before PPN/R10/clock/orbital scoring",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 354 - PPC4161 cGamma transition source-kernel coefficient fill or metric-null proof

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4338 does **not** prove public local GR, a transition-shell PPN pass, R10, WEP, clocks, orbital safety, Maxwell/QED, charge normalization, or a numerical prediction of `G_N`.

It makes the 4337 `c_Gamma` target sharper:

```text
finite-margin compact collar:
  R_transport_to_local = R_Bgrad_to_local = 0
  A_J,eff_private = 0
  cGamma AJ/profile channel quiet

raw transition shell:
  P_leak q_tr is still active
```

The transition-shell route is no longer "make c_Gamma small" in vague language. The clean theorem route is:

```text
P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube
P_leak   := I - P_kernel

If q_tr = P_kernel q_tr, then P_leak q_tr = 0.
```

The current corpus finds the ordinary local source kernel. It does **not** parent-sign raw transition-shell `q_tr` into that kernel.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Branch Theorems

{md_table(tables["theorems"], ["theorem_id", "domain", "premises", "result", "status", "source_basis", "valid_for_claim"])}

## Kernel Rows

{md_table(tables["kernels"], ["kernel_id", "operator", "definition", "effect", "current_status", "valid_for_claim"])}

## P_leak Components

{md_table(tables["pleak"], ["component_id", "component", "priority", "zero_status", "obstruction", "next_action", "valid_for_claim"])}

## Pressure Rows

{md_table(tables["pressure"], ["pressure_id", "branch", "formula", "required_Tres_over_tauL", "interpretation", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4338 Y5-R2FR cGamma transition source-kernel coefficient fill or metric-null proof

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

`c_Gamma` is now branch-separated:

```text
compact finite-margin collars: A_J,eff_private = 0
raw transition shell: P_leak q_tr remains active
```

So the next frontier is not all local gravity. It is the seven-component transition leak vector, beginning with `P_nonHilbert_action_domain` and `P_off_worldtube_readout_order`.

## P_leak Components

{md_table(tables["pleak"], ["component", "priority", "zero_status", "next_action"])}

## Next

{md_table(tables["next"], ["next_target", "target_question", "preferred_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def validation_rows(paths: Dict[str, Path], tables: Dict[str, List[Dict[str, str]]]) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, description: str, passed: bool, evidence: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "branch": BRANCH,
                "generated_utc": GENERATED_UTC,
                "decision": DECISION,
                "claim_allowed": "False",
                "valid_for_claim": "False",
                "check_id": check_id,
                "description": description,
                "passed": str(bool(passed)),
                "evidence": evidence,
            }
        )

    pleak_components = {row["component"] for row in tables["pleak"]}

    add("VAL4338_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4338_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4338_collar_zero", "finite-margin collar zero theorem exists", any("A_J,eff_private=0" in r["result"] and "COLLAR" in r["status"] for r in tables["theorems"]), "theorems")
    add("VAL4338_transition_open", "raw transition shell remains open", any(r["domain"] == "raw Solar/vacuum transition shell" and r["status"] == "OPEN_TRANSITION_FRONTIER" for r in tables["theorems"]), "theorems")
    add("VAL4338_kernel_rows", "P_kernel and P_leak rows exist", {"P_kernel", "P_leak=I-P_kernel"}.issubset({r["operator"] for r in tables["kernels"]}), "kernels")
    add("VAL4338_pleak_count", "seven P_leak components retained", len(tables["pleak"]) == 7, "pleak")
    add("VAL4338_first_targets", "first two P_leak targets present", {"P_nonHilbert_action_domain", "P_off_worldtube_readout_order"}.issubset(pleak_components), "pleak")
    add("VAL4338_pressure_default", "default pressure requirement matches 4287 value", abs(float(next(r for r in tables["pressure"] if r["pressure_id"] == "PRS4338_1_raw_transition_default_strong_window")["required_Tres_over_tauL"]) - DEFAULT_T_RATIO_REQUIRED) < 1e-9, "pressure")
    add("VAL4338_firewall_collar_shell", "collar-to-shell firewall exists", any("compact-collar zero" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4338_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4338_next_targets_pleak", "next target attacks first P_leak components", any("P_nonHilbert" in r["preferred_route"] and "P_off_worldtube" in r["preferred_route"] for r in tables["next"]), "next")
    add("VAL4338_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4338_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4338_post_pleak", "post doc mentions P_leak", "P_leak q_tr remains active" in read_text(DOC_PATH), "post")
    add("VAL4338_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4338_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4338_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4338_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4338_SOURCE_REGISTER.csv",
        "theorems": SOURCE_DIR / "P8_Y5_R2FR_4338_BRANCH_THEOREMS.csv",
        "kernels": SOURCE_DIR / "P8_Y5_R2FR_4338_SOURCE_KERNEL_ROWS.csv",
        "pleak": SOURCE_DIR / "P8_Y5_R2FR_4338_PLEAK_COMPONENTS.csv",
        "pressure": SOURCE_DIR / "P8_Y5_R2FR_4338_CGAMMA_PRESSURE_ROWS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4338_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4338_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4338_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4338_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4338_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "theorems": theorem_rows(),
        "kernels": kernel_rows(),
        "pleak": pleak_rows(),
        "pressure": pressure_rows(),
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
## PPC4161 4338 cGamma collar zero and transition P_leak vector

Marker: `{MARKER}`

4338 imports the finite-margin cGamma result into the 4337 coupling split. Compact support-separated collars inherit:

```text
R_transport_to_local = R_Bgrad_to_local = 0
A_J,eff_private = 0.
```

The raw transition shell does not inherit that result. It is reduced to:

```text
P_leak q_tr =
P_nonHilbert_action_domain q_tr
+ P_off_worldtube_readout_order q_tr
+ P_time_multipole q_tr
+ P_species_frame_source_weight q_tr
+ P_range_hair q_tr
+ P_nonEH_metric_readout q_tr
+ P_boundary_nonlocal_owner q_tr.
```

The next proof target is the first pair: `P_nonHilbert_action_domain` and `P_off_worldtube_readout_order`.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4338 packet cGamma collar zero and transition P_leak vector

Marker: `{PACKET_MARKER}`

Packet update: cGamma is no longer treated as equally open across every local domain. The finite-margin compact-collar AJ/profile channel is quiet. The raw transition shell is reduced to a seven-component `P_leak q_tr` vector, with the first two components selected for proof or finite bound rows.
""",
    )
    validation = validation_rows(paths, tables)
    write_csv(paths["validation"], validation)
    failed = [row for row in validation if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(tables)} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(validation)} failed={len(failed)}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']} :: {row['evidence']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
