from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4332"
CLAIM_ID = "L-173"
BRANCH = "MTS_R2FR_Y5_XI_SRC_HIDDEN_ZERO_OR_SOURCE_LABEL_TAIL_BOUND_4332"
DECISION = "SOURCE_LABEL_FORGETTING_HILBERT_OWNER_ZERO_IMPORTED_CONDITIONALLY_XI_REDUCED_TO_OPEN_SOURCE_TAILS_NONCLAIM"
MARKER = "PPC4161_XI_SRC_HIDDEN_ZERO_OR_SOURCE_LABEL_TAIL_BOUND_4332"
PACKET_MARKER = "PPC4161_PACKET_XI_SRC_HIDDEN_ZERO_OR_SOURCE_LABEL_TAIL_BOUND_4332"
NEXT_TARGET = "4333-Y5-R2FR-standard-branch-source-readout-rollup-or-open-tail-test-pack.md"

FORMAL_PATH = FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md"
DOC_PATH = POST / "4332-Y5-R2FR-Xi-src-hidden-zero-or-source-label-tail-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4332_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


SOURCES = [
    (
        "SRC4332_00_next",
        SOURCE_DIR / "P8_Y5_R2FR_4331_NEXT_TARGET.csv",
        "Xi_src_hidden",
        "4331 handoff selecting the hidden source-prefactor/source-label tail gate.",
    ),
    (
        "SRC4332_01_master_Xi",
        FORMAL / "340-PPC4161-hidden-source-prefactor-and-marker-tail-zero-or-bound.md",
        "Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + R_source_normalization + delta_w_EM + R_no_direct_m_charge + R_environment_selector",
        "4324 master hidden source-prefactor budget.",
    ),
    (
        "SRC4332_02_tail_bound",
        FORMAL / "340-PPC4161-hidden-source-prefactor-and-marker-tail-zero-or-bound.md",
        "Xi_src_hidden <= C_w",
        "4324 derivative/source-label fallback bound.",
    ),
    (
        "SRC4332_03_source_readout_hidden",
        FORMAL / "337-PPC4161-Dq-source-readout-factorization-zero-or-Rsrc-epsilon-row.md",
        "epsilon_SR_hidden=0",
        "4321 hidden source-readout tail zero condition.",
    ),
    (
        "SRC4332_04_matter_hidden",
        FORMAL / "338-PPC4161-Dq-matter-descent-lift-or-geometry-theta-bound-row.md",
        "epsilon_matter_hidden=0",
        "4322 hidden matter/source-prefactor tail zero condition.",
    ),
    (
        "SRC4332_05_marker_tail",
        FORMAL / "339-PPC4161-Dq-theta-marker-Hperp-zero-lift-or-marker-tail-bound.md",
        "marker/source-label tails remain explicit outside that branch",
        "4323 marker/source-label tail firewall.",
    ),
    (
        "SRC4332_06_no_hidden_slots",
        FORMAL / "320-PPC4161-first-source-norms-or-visible-Hilbert-m-lock-signature.md",
        "No independent f(m,X)F^2, source-label drift, hidden Hodge drift, or species marker coupling",
        "4304 says the no-hidden-slot theorem was not yet signed globally.",
    ),
    (
        "SRC4332_07_EM_weight",
        FORMAL / "329-PPC4161-EM-Ward-current-normalization-or-collar-residual-bound-values.md",
        "zero on source-label-forgetting Hilbert branch",
        "4313 EM source/readout weight tail branch.",
    ),
    (
        "SRC4332_08_geometry_bottleneck",
        FORMAL / "343-PPC4161-Dq-geometry-no-shadow-or-epsilon-geom-profile-reduction.md",
        "source-readout closes only if epsilon_geom_core=0 and Xi_src_hidden=0",
        "4327 local claim gate needs Xi zero.",
    ),
    (
        "SRC4332_09_4331_update",
        FORMAL / "347-PPC4161-readout-frame-terminal-tail-zero-or-projection-bound.md",
        "epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_projection + Xi_src_hidden",
        "4331 reduced source-readout update handing to Xi.",
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
                "4332 turns the Xi_src_hidden gate into an explicit source-label-forgetting theorem attempt. In the Hilbert-owner standard branch, no hidden source weights w_A(Phi), no source-normalization reentry N_src(Phi), no marker/source-label/environment selector, no hidden matter operator, no EM species/readout weight, and no independent m-boundary source charge may enter before variation. Under that full clause set, epsilon_matter_hidden=epsilon_SR_hidden=R_marker_source_label=R_hidden_weights=R_source_normalization=delta_w_EM=R_no_direct_m_charge=R_environment_selector=0, hence Xi_src_hidden=0. The corpus still does not globally parent-sign those clauses, so outside the standard source-label-forgetting branch Xi_open is retained as a finite no-cancellation source-label tail. No local GR/R10/PPN/clock/orbital claim fires.",
                "4332 source register, Xi clause audit, component zero rows, open-tail bound rows, source-readout update formulas, runner, firewall, decision, status, next-target and validation CSV.",
                "private_Xi_source_label_forgetting_zero_conditionally_with_open_tail_firewall_nonclaim",
                "Roll up the standard branch source-readout closure and build the open-tail local-test projection pack before any empirical local claim.",
                "Declaring source labels zero without Hilbert-owner/no-hidden-slot action-domain clauses; hiding source normalization in theta or measured constants; cancelling Xi components across sectors; using EM source-label forgetting as a global Maxwell/QED result; or claiming local GR/R10/PPN/clock pass while open source/projection tails remain.",
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


def audit_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "AUD4332_0_master_gate",
            "clause": "Xi_src_hidden is the remaining source-label/hidden-prefactor gate after 4331",
            "source_basis": "4324/4327/4331",
            "status": "TARGET_GATE_CONFIRMED",
            "effect": "source-readout closes only if Xi and reduced geometry/open projection tails close",
        },
        {
            "audit_id": "AUD4332_1_Hilbert_source_owner",
            "clause": "all source weights, normalizations and source markers are q-basic Hilbert-owned data fixed before variation",
            "source_basis": "4321/4324",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "effect": "D_Hperp ln w_A = D_Hperp ln N_src = D_Hperp theta_src = 0",
        },
        {
            "audit_id": "AUD4332_2_no_hidden_matter",
            "clause": "no direct hidden matter operator, no direct matter-X vertex and no independent matter-frame source prefactor",
            "source_basis": "4322/4328",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "effect": "epsilon_matter_hidden=0",
        },
        {
            "audit_id": "AUD4332_3_no_hidden_source_readout",
            "clause": "source readout contains no hidden weights, post-readout labels, projector commutator or worldtube selector before variation",
            "source_basis": "4321/4326/4331",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "effect": "epsilon_SR_hidden and Rsrc hidden pieces vanish in the standard branch",
        },
        {
            "audit_id": "AUD4332_4_EM_source_weight",
            "clause": "EM source/current weight is the same Hilbert/Maxwell-owned source-label-forgetting branch",
            "source_basis": "4313/4329",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "effect": "delta_w_EM=0 only in the visible same-Hodge Hilbert branch",
        },
        {
            "audit_id": "AUD4332_5_no_environment_selector",
            "clause": "no environment/medium selector or active source label enters the action before variation",
            "source_basis": "4323/4324",
            "status": "CONDITIONAL_ZERO_ROUTE",
            "effect": "R_marker_source_label=R_environment_selector=0",
        },
        {
            "audit_id": "AUD4332_6_global_parent_gap",
            "clause": "4304 does not globally parent-sign no-hidden-slot/source-label forgetting",
            "source_basis": "4304/4324",
            "status": "NOT_GLOBAL_PARENT_SIGNED",
            "effect": "Xi zero remains branch-local and nonclaim; open-tail rows retained outside branch",
        },
    ]


def zero_rows() -> List[Dict[str, str]]:
    component_conditions = [
        ("ZERO4332_0_matter_hidden", "epsilon_matter_hidden", "0", "no direct hidden matter operator, matter-X vertex, disformal ordinary-frame slot or source-prefactor dependence"),
        ("ZERO4332_1_SR_hidden", "epsilon_SR_hidden", "0", "no hidden source weights, post-readout tails, projector commutator or source-label drift before variation"),
        ("ZERO4332_2_marker_label", "R_marker_source_label", "0", "theta/source labels are q-basic or fixed before variation"),
        ("ZERO4332_3_hidden_weights", "R_hidden_weights", "0", "D_Hperp ln w_A=0 for all source/species weights"),
        ("ZERO4332_4_source_norm", "R_source_normalization", "0", "D_Hperp ln N_src=0 and no source normalization reentry through theta or measured constants"),
        ("ZERO4332_5_EM_weight", "delta_w_EM", "0", "EM current/source weight is Hilbert-owned and source-label forgetting"),
        ("ZERO4332_6_no_direct_m_charge", "R_no_direct_m_charge", "0", "no independent m-boundary/source charge or direct matter-X charge slot"),
        ("ZERO4332_7_env_selector", "R_environment_selector", "0", "no environment/medium selector before variation"),
        ("ZERO4332_8_Xi", "Xi_src_hidden", "0", "all component zero rows ZERO4332_0 through ZERO4332_7 hold simultaneously"),
    ]
    return [
        {
            "zero_id": zero_id,
            "symbol": symbol,
            "zero_value": zero_value,
            "branch_conditions": branch_conditions,
            "status": "CONDITIONAL_ZERO_IN_SOURCE_LABEL_FORGETTING_HILBERT_OWNER_BRANCH",
            "valid_for_claim": "False",
        }
        for zero_id, symbol, zero_value, branch_conditions in component_conditions
    ]


def tail_rows() -> List[Dict[str, str]]:
    return [
        {
            "tail_id": "TAIL4332_0_hidden_weights",
            "symbol": "R_hidden_weights",
            "open_branch_trigger": "w_A(Phi) or species/source weights enter before variation",
            "bound_contribution": "C_w ||D_Hperp ln w_A||",
            "arena_links": "R10/PPN/clock/orbital/source-readout",
            "status": "RETAINED_OUTSIDE_STANDARD_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4332_1_source_norm",
            "symbol": "R_source_normalization",
            "open_branch_trigger": "N_src(Phi), theta_src(Phi) or source normalization reenters through calibrated constants",
            "bound_contribution": "C_norm ||D_Hperp ln N_src|| + C_mark ||D_Hperp theta_src||",
            "arena_links": "clock/calibration/source amplitude",
            "status": "RETAINED_OUTSIDE_STANDARD_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4332_2_hidden_operator",
            "symbol": "epsilon_matter_hidden",
            "open_branch_trigger": "hidden matter operator, direct matter-X vertex or ordinary-frame disformal slot survives",
            "bound_contribution": "C_op ||D_Hperp O_hidden||",
            "arena_links": "PPN/WEP/orbital",
            "status": "RETAINED_OUTSIDE_STANDARD_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4332_3_EM_weight",
            "symbol": "delta_w_EM",
            "open_branch_trigger": "EM species/readout/current weight is not source-label forgetting",
            "bound_contribution": "C_EM ||delta_w_EM||",
            "arena_links": "EM/clock/PPN/radiation",
            "status": "RETAINED_OUTSIDE_STANDARD_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4332_4_inner_charge",
            "symbol": "R_no_direct_m_charge",
            "open_branch_trigger": "independent m-boundary/source charge or inner support charge survives",
            "bound_contribution": "C_inner ||Q_m^H||",
            "arena_links": "inner/source-domain/local fifth force",
            "status": "RETAINED_OUTSIDE_STANDARD_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4332_5_environment",
            "symbol": "R_environment_selector",
            "open_branch_trigger": "environment/medium/source-label selector enters before variation",
            "bound_contribution": "C_env ||D_Hperp sigma_env||",
            "arena_links": "lab material/clock/PPN screening checks",
            "status": "RETAINED_OUTSIDE_STANDARD_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4332_6_Xi_open",
            "symbol": "Xi_open",
            "open_branch_trigger": "any Xi component is not zero-signed",
            "bound_contribution": "sum of retained no-cancellation component bounds",
            "arena_links": "all local arenas",
            "status": "CANONICAL_OPEN_TAIL_NAME",
            "valid_for_claim": "False",
        },
    ]


def formula_rows() -> List[Dict[str, str]]:
    return [
        {
            "formula_id": "F4332_0_Xi_definition",
            "name": "master hidden source-prefactor definition",
            "formula": "Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + R_source_normalization + delta_w_EM + R_no_direct_m_charge + R_environment_selector",
            "status": "IMPORTED_FROM_4324",
        },
        {
            "formula_id": "F4332_1_source_label_zero",
            "name": "source-label-forgetting zero",
            "formula": "D_Hperp ln w_A=D_Hperp ln N_src=D_Hperp theta_src=D_Hperp sigma_env=0, O_hidden=0, delta_w_EM=0, Q_m^H=0 => Xi_src_hidden=0",
            "status": "CONDITIONAL_BRANCH_ZERO_NOT_GLOBAL_PARENT_SIGNED",
        },
        {
            "formula_id": "F4332_2_Xi_open_bound",
            "name": "open branch no-cancellation bound",
            "formula": "Xi_open <= C_w||D_Hperp ln w_A|| + C_norm||D_Hperp ln N_src|| + C_mark||D_Hperp theta_src|| + C_op||D_Hperp O_hidden|| + C_EM||delta_w_EM|| + C_inner||Q_m^H|| + C_env||D_Hperp sigma_env||",
            "status": "BOUND_READY_VALUES_MISSING",
        },
        {
            "formula_id": "F4332_3_source_readout_update",
            "name": "source-readout after Xi reduction",
            "formula": "epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_projection + Xi_open",
            "status": "REDUCED_TO_GEOMETRY_PLUS_OPEN_SOURCE_TAILS",
        },
        {
            "formula_id": "F4332_4_standard_branch_rollup",
            "name": "standard branch source-readout closure condition",
            "formula": "if Xi_src_hidden=0 and epsilon_geom_core_after_projection=0, then epsilon_source_readout=0; with 4331, epsilon_geom_core_after_projection <= C_EMopen epsilon_EM_open_boundary + C_coeff_open epsilon_coeff_open + C_proj epsilon_projection_open + tail_guard_sum",
            "status": "ROLLUP_READY_NOT_CLAIM",
        },
        {
            "formula_id": "F4332_5_local_claim_gate",
            "name": "local claim gate",
            "formula": "local claim requires Xi_src_hidden=0, epsilon_geom_core_after_projection=0, sourced local projection matrices, and no open EM/coefficient/projection/source tails",
            "status": "CLAIM_BLOCKED",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4332_0_current_corpus",
            "branch_input": "current corpus without global no-hidden-slot parent signature",
            "action": "KEEP_XI_OPEN",
            "output": "Xi_open finite tail retained",
            "claim_policy": "no local claim",
        },
        {
            "runner_id": "RUN4332_1_standard_Hilbert_owner",
            "branch_input": "source-label-forgetting Hilbert-owner clauses all signed",
            "action": "ALLOW_XI_ZERO",
            "output": "Xi_src_hidden=0 conditionally",
            "claim_policy": "still requires geometry/open-tail/local projection closure",
        },
        {
            "runner_id": "RUN4332_2_hidden_weight_present",
            "branch_input": "any w_A(Phi), N_src(Phi), theta_src(Phi), sigma_env(Phi), O_hidden, delta_w_EM or Q_m^H survives",
            "action": "USE_COMPONENT_BOUND",
            "output": "component contributes to Xi_open",
            "claim_policy": "valid_for_claim=false until sourced and projected",
        },
        {
            "runner_id": "RUN4332_3_source_norm_hide",
            "branch_input": "source normalization hidden inside theta, G_cal or readout convention",
            "action": "REJECT_HIDE",
            "output": "route term back to R_source_normalization",
            "claim_policy": "firewall",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4332_0_no_hidden_slot_global",
            "forbidden_shortcut": "treat 4304 no-hidden-slot as globally signed",
            "reason": "4304 explicitly retains residual rows and asks for theorem/bounds",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4332_1_source_label_notation",
            "forbidden_shortcut": "rename source labels or source normalization into theta/readout/calibrated constants",
            "reason": "4323/4324 route those terms into R_marker_source_label and R_source_normalization",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4332_2_cancellation",
            "forbidden_shortcut": "cancel Xi components across matter, EM, source-readout and inner charge sectors",
            "reason": "4324 defines Xi as a no-cancellation master budget",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4332_3_EM_global",
            "forbidden_shortcut": "use EM source-label forgetting as a global Maxwell/QED or charge-normalization proof",
            "reason": "4313/4329 only support the visible Hilbert same-Hodge branch",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4332_4_local_claim",
            "forbidden_shortcut": "claim local GR/R10/PPN/clock/orbital pass from Xi zero alone",
            "reason": "open projection, nonstandard source tails, sourced matrices and local test projection rows remain",
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
            "summary": "Xi_src_hidden is zero in the source-label-forgetting Hilbert-owner branch, because every component of the 4324 master budget is then killed by an action-domain no-hidden-source-slot clause. The corpus does not globally sign that theorem, so Xi_open remains the canonical source-label tail outside the branch.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4332_0_Xi",
            "item": "Xi_src_hidden",
            "status": "CONDITIONAL_ZERO_IN_STANDARD_HILBERT_OWNER_BRANCH",
            "notes": "not globally parent-signed; Xi_open retained outside branch",
        },
        {
            "status_id": "STAT4332_1_source_readout",
            "item": "epsilon_source_readout",
            "status": "REDUCED_TO_GEOMETRY_PLUS_XI_OPEN",
            "notes": "4331 geometry core plus 4332 Xi gate are now the rollup inputs",
        },
        {
            "status_id": "STAT4332_2_local_claim",
            "item": "local GR/R10/PPN/clock/orbital",
            "status": "BLOCKED",
            "notes": "needs open-tail projection pack and sourced local matrices before scoring",
        },
        {
            "status_id": "STAT4332_3_next",
            "item": "rollup/test pack",
            "status": "NEXT_TARGET",
            "notes": "build standard-branch source-readout closure statement and open-tail empirical projection pack",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4332_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the standard branch be rolled into an explicit source-readout/local-GR closure contract while keeping open source/projection tails as test-pack inputs?",
            "preferred_route": "prove the standard branch implication Xi=0 plus reduced geometry=open-tail-free gives epsilon_source_readout=0, then list exact sourced matrices needed for R10/PPN/clock/orbital tests",
            "fallback_route": "retain Xi_open, epsilon_projection_open, epsilon_EM_open_boundary and epsilon_coeff_open as source-backed local-test rows",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 348 - PPC4161 Xi source-hidden zero or source-label tail bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4332 does **not** prove public local GR, Newtonian mechanics, R10, PPN, WEP, clock safety, orbital safety, Maxwell/QED, charge normalization, or a global no-hidden-slot theorem.

It does take a real step: the foggy hidden-source coupling is no longer a loose complaint. It has a branch-local zero theorem and an explicit open-tail fallback.

## Core Law

```text
Xi_src_hidden
:= epsilon_matter_hidden
 + epsilon_SR_hidden
 + R_marker_source_label
 + R_hidden_weights
 + R_source_normalization
 + delta_w_EM
 + R_no_direct_m_charge
 + R_environment_selector.

Source-label-forgetting Hilbert-owner branch:
D_Hperp ln w_A = 0,
D_Hperp ln N_src = 0,
D_Hperp theta_src = 0,
D_Hperp sigma_env = 0,
O_hidden = 0,
delta_w_EM = 0,
Q_m^H = 0
=> Xi_src_hidden = 0.
```

Outside that branch, `Xi_open` is retained as a no-cancellation source-label tail.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Xi Clause Audit

{md_table(tables["audit"], ["audit_id", "clause", "source_basis", "status", "effect"])}

## Component Zero Rows

{md_table(tables["zeros"], ["zero_id", "symbol", "zero_value", "branch_conditions", "status", "valid_for_claim"])}

## Open Source-Label Tail Rows

{md_table(tables["tails"], ["tail_id", "symbol", "open_branch_trigger", "bound_contribution", "arena_links", "status", "valid_for_claim"])}

## Formula Updates

{md_table(tables["formulas"], ["formula_id", "name", "formula", "status"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4332 Y5-R2FR Xi source-hidden zero or source-label tail bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

`Xi_src_hidden` is zero only inside the source-label-forgetting Hilbert-owner branch. Outside that branch, `Xi_open` becomes the canonical finite source-label/source-prefactor tail.

## Source-Readout Update

{md_table(tables["formulas"], ["formula_id", "formula", "status"])}

## Open Tail Inputs

{md_table(tables["tails"], ["tail_id", "symbol", "bound_contribution", "arena_links", "status"])}

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

    add("VAL4332_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4332_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4332_definition", "Xi definition imported", any(r["formula_id"] == "F4332_0_Xi_definition" and "epsilon_matter_hidden" in r["formula"] and "R_environment_selector" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4332_all_components_zeroed", "all Xi component zero rows exist", {"epsilon_matter_hidden", "epsilon_SR_hidden", "R_marker_source_label", "R_hidden_weights", "R_source_normalization", "delta_w_EM", "R_no_direct_m_charge", "R_environment_selector", "Xi_src_hidden"}.issubset({r["symbol"] for r in tables["zeros"]}), "zeros")
    add("VAL4332_zero_formula", "source-label zero formula names derivative clauses", any("D_Hperp ln w_A" in r["formula"] and "Xi_src_hidden=0" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4332_open_bound", "open Xi bound contains major source-label tails", any("Xi_open <=" in r["formula"] and "D_Hperp ln N_src" in r["formula"] and "Q_m^H" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4332_source_readout_update", "source-readout update uses Xi_open", any(r["formula_id"] == "F4332_3_source_readout_update" and "Xi_open" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4332_rollup_ready", "standard branch rollup condition present", any(r["formula_id"] == "F4332_4_standard_branch_rollup" and "epsilon_source_readout=0" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4332_no_global_parent", "global no-hidden-slot claim blocked", any("globally signed" in r["forbidden_shortcut"] for r in tables["firewall"]) and any(r["status"] == "NOT_GLOBAL_PARENT_SIGNED" for r in tables["audit"]), "firewall/audit")
    add("VAL4332_no_cancellation", "Xi component cancellation blocked", any("cancel Xi components" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4332_source_norm_hide_blocked", "source normalization hiding blocked", any("source normalization" in r["forbidden_shortcut"] and "theta" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4332_runner_modes", "runner has zero, open and reject modes", {"ALLOW_XI_ZERO", "KEEP_XI_OPEN", "USE_COMPONENT_BOUND", "REJECT_HIDE"}.issubset({r["action"] for r in tables["runner"]}), "runner")
    add("VAL4332_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4332_next_rollup", "next target is rollup/test pack", any("source-readout-rollup" in r["next_target"] and "local-GR closure contract" in r["target_question"] for r in tables["next"]), "next")
    add("VAL4332_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4332_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4332_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4332_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4332_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4332_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4332_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4332_SOURCE_REGISTER.csv",
        "audit": SOURCE_DIR / "P8_Y5_R2FR_4332_XI_CLAUSE_AUDIT.csv",
        "zeros": SOURCE_DIR / "P8_Y5_R2FR_4332_XI_COMPONENT_ZERO_ROWS.csv",
        "tails": SOURCE_DIR / "P8_Y5_R2FR_4332_XI_OPEN_TAIL_ROWS.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4332_SOURCE_READOUT_UPDATE_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4332_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4332_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4332_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4332_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4332_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "audit": audit_rows(),
        "zeros": zero_rows(),
        "tails": tail_rows(),
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
## PPC4161 4332 Xi source-hidden zero or source-label tail bound

Marker: `{MARKER}`

4332 resolves the `Xi_src_hidden` gate into a branch-local theorem plus an honest open-tail fallback. In the source-label-forgetting Hilbert-owner branch, all source weights, source normalizations, marker/source labels, environment selectors, hidden matter operators, EM source weights and independent m-boundary source charges are fixed/q-basic before variation; therefore every component of `Xi_src_hidden` vanishes and `Xi_src_hidden=0`. The corpus does not globally parent-sign that no-hidden-slot theorem, so `Xi_open` is retained outside the standard branch. The next rollup target is to combine `Xi=0` with the 4331 reduced geometry core and list exact local-test projection inputs.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4332 packet Xi source-hidden zero

Marker: `{PACKET_MARKER}`

Packet update: the hidden source-prefactor problem is now a precise source-label-forgetting gate. Standard Hilbert-owner source data kill `Xi_src_hidden`; nonstandard source labels feed `Xi_open` as the canonical no-cancellation local-test tail.
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
