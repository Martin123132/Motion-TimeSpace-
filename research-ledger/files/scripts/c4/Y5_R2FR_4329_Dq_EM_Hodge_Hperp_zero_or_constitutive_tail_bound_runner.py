from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4329"
CLAIM_ID = "L-170"
BRANCH = "MTS_R2FR_Y5_DQ_EM_HODGE_HPERP_ZERO_OR_CONSTITUTIVE_TAIL_BOUND_4329"
DECISION = "SAME_HODGE_CLOSED_COLLAR_DQ_EM_ZERO_IMPORTED_CONDITIONALLY_EM_HODGE_FRAME_TAIL_REMOVED_GLOBAL_EM_ALPHA_OPEN_NONCLAIM"
MARKER = "PPC4161_DQ_EM_HODGE_HPERP_ZERO_OR_CONSTITUTIVE_TAIL_BOUND_4329"
PACKET_MARKER = "PPC4161_PACKET_DQ_EM_HODGE_HPERP_ZERO_OR_CONSTITUTIVE_TAIL_BOUND_4329"
NEXT_TARGET = "4330-Y5-R2FR-coefficient-drift-zero-or-source-backed-tail-bound.md"

FORMAL_PATH = FORMAL / "345-PPC4161-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md"
DOC_PATH = POST / "4329-Y5-R2FR-Dq-EM-Hodge-Hperp-zero-or-constitutive-tail-bound.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4329_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")


SOURCES = [
    (
        "SRC4329_00_next",
        SOURCE_DIR / "P8_Y5_R2FR_4328_NEXT_TARGET.csv",
        "Can Dq_EM[Hperp]",
        "4328 handoff: EM/Hodge is the next live geometry-tail gate.",
    ),
    (
        "SRC4329_01_poynting_owner",
        FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md",
        "Poynting vector is not a separate background field",
        "Maxwell-Hodge Hilbert stress owns Poynting flux; no double-counting.",
    ),
    (
        "SRC4329_02_dqem_vector",
        FORMAL / "275-PPC4161-EM-Hodge-component-zero-or-residual-vector.md",
        "Dq_EM[Hperp]=0",
        "4259 Dq_EM zero contract and visible EM residual vector.",
    ),
    (
        "SRC4329_03_delta_hodge",
        FORMAL / "276-PPC4161-Delta-Hodge-EM-closure-or-bound.md",
        "Delta_Hodge_EM = 0",
        "4260 Hodge uniqueness separated from parent action-domain clauses.",
    ),
    (
        "SRC4329_04_action_domain",
        FORMAL / "277-PPC4161-visible-EM-action-domain-fork-or-constitutive-bound.md",
        "visible EM action-domain contribution to `Delta_Hodge_EM` is conditionally zero",
        "4261 visible Maxwell-Hodge action-domain is signed only in the standard visible branch.",
    ),
    (
        "SRC4329_05_readout",
        FORMAL / "278-PPC4161-visible-EM-readout-guard-or-charge-normalization-bound.md",
        "C_Hodge_readout = 0.",
        "4262 calibrated q-basic EM readout/coupling silence.",
    ),
    (
        "SRC4329_06_closed_collar",
        FORMAL / "279-PPC4161-Dq-EM-closed-collar-adoption-or-radiative-boundary-row.md",
        "Dq_EM = 0.0",
        "4263 adopts Dq_EM zero only for standard visible static closed-collar tests.",
    ),
    (
        "SRC4329_07_hodge_owner",
        FORMAL / "331-PPC4161-Hodge-constitutive-owner-zero-or-DeltaHodge-bound.md",
        "HT4315_1_same_action",
        "4315 same-Hodge zero-or-bound contract.",
    ),
    (
        "SRC4329_08_4328_live_tail",
        FORMAL / "344-PPC4161-parent-no-extra-frame-signature-or-cg-bdis-bound-runner.md",
        "epsilon_EM_Hodge_frame",
        "4328 live residual tail to be reduced.",
    ),
    (
        "SRC4329_09_guard",
        FORMAL / "293-PPC4161-matter-interface-action-domain-proof-or-canonical-gX-source-fill.md",
        "Dq_EM = 0.",
        "4277 guard row lists Dq_EM as a required escape blocker.",
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
                "em_local_gr",
                "4329 imports the older 4259-4263 EM result into the newer 4328 geometry bottleneck. In the standard visible, q-basic, same-Hodge, static closed-collar branch, Maxwell-Hodge uses the observed Hodge star, EM readout/coupling markers are fixed before variation, Poynting is Hilbert EM flux rather than a second force, and radiative collar flux is zero or routed as a boundary term. Therefore the live epsilon_EM_Hodge_frame tail can be set to zero only on that branch: Delta_Hodge_EM=0 and Dq_EM[Hperp]=Dq_EM_C1=0. Global Maxwell/QED, alpha_EM, charge normalization, open radiation, constitutive deformation, coefficient drift, Xi_src_hidden and public local-GR claims remain open.",
                "4329 source register, EM-Hodge clause audit, zero rows, constitutive tail bound, geometry/source-readout update formulas, runner, firewall, decision, status, next-target and validation CSV.",
                "private_same_Hodge_closed_collar_EM_tail_zero_conditionally_nonclaim",
                "Attack coefficient drift epsilon_coeff next, or fill source-backed constitutive/open-radiation tails for non-standard EM branches.",
                "Using same-Hodge closure as a global Maxwell derivation; predicting alpha_EM or charge scale; erasing open radiative Poynting flux; treating Dq_EM zero outside the standard visible closed-collar branch; or claiming local GR/R10/PPN/clock pass while coefficient/Xi/source-readout gates remain open.",
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


def clause_rows() -> List[Dict[str, str]]:
    return [
        {
            "clause_id": "CL4329_0_unique_hodge",
            "clause": "observed Hodge uniqueness",
            "statement": "fixed g_obs, e_obs, orientation and volume determine the visible Hodge star *_obs",
            "source_basis": "4260/4315",
            "status": "EXACT_MATH_LEMMA",
            "effect": "mathematical Hodge ambiguity removed once observed geometry is fixed",
        },
        {
            "clause_id": "CL4329_1_same_action",
            "clause": "same-Hodge Maxwell action",
            "statement": "S_EM=-(4 mu0)^-1 int F wedge *_obs F with no independent chi_EM or hidden EM metric",
            "source_basis": "4261/4315 standard visible branch",
            "status": "CONDITIONAL_BRANCH_SIGNED",
            "effect": "Delta_Hodge_EM=0 in the calibrated visible same-Hodge branch",
        },
        {
            "clause_id": "CL4329_2_readout_coupling",
            "clause": "q-basic calibrated EM readout",
            "statement": "theta_obs, alpha_EM, charges, g_J, lambda_A and material labels are fixed before variation; readout is pure postprocessing",
            "source_basis": "4262",
            "status": "CONDITIONAL_BRANCH_SIGNED",
            "effect": "C_Hodge_readout=b_alpha=C_JQ=0 on the branch without deriving alpha_EM",
        },
        {
            "clause_id": "CL4329_3_poynting_owner",
            "clause": "Poynting owned by Hilbert stress",
            "statement": "S_i=-T_EM(n,e_i)=(E cross B)_i, so Poynting is not an extra background force",
            "source_basis": "4175/4259",
            "status": "CONDITIONAL_OWNER_SIGNED",
            "effect": "standalone Poynting double-counting is forbidden",
        },
        {
            "clause_id": "CL4329_4_closed_collar",
            "clause": "static closed collar or routed boundary flux",
            "statement": "net radiative EM flux through the local collar is zero for the static/quasi-static branch, otherwise it is an explicit boundary term",
            "source_basis": "4263",
            "status": "CONDITIONAL_BRANCH_SIGNED",
            "effect": "Dq_EM[Hperp]=Dq_EM_C1=0 only in closed-collar local tests",
        },
        {
            "clause_id": "CL4329_5_global_deformation",
            "clause": "global/open/deformed EM branch",
            "statement": "independent chi_EM, hidden Hodge metric, alpha/current drift, orientation flux, or open radiation reopens the constitutive bound fork",
            "source_basis": "4259-4263/4315",
            "status": "RETAIN_BOUND_FORK",
            "effect": "no global Maxwell, alpha, charge-scale or public local-GR claim",
        },
    ]


def zero_rows() -> List[Dict[str, str]]:
    return [
        {
            "zero_id": "ZERO4329_0_Delta_Hodge_EM",
            "symbol": "Delta_Hodge_EM",
            "zero_statement": "Delta_Hodge_EM=0",
            "branch_conditions": "same observed Hodge Maxwell action, no independent chi_EM, no hidden/disformal EM metric, q-basic readout",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4329_1_Dq_EM",
            "symbol": "Dq_EM[Hperp]",
            "zero_statement": "Dq_EM[Hperp]=0 and Dq_EM_C1=0",
            "branch_conditions": "standard visible branch plus static/quasi-static closed collar or routed boundary flux",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4329_2_epsilon_EM_Hodge_frame",
            "symbol": "epsilon_EM_Hodge_frame",
            "zero_statement": "epsilon_EM_Hodge_frame=0",
            "branch_conditions": "ZERO4329_0 + ZERO4329_1 + Poynting Hilbert-owner/no-double-count rule",
            "status": "CONDITIONAL_ZERO_IMPORTED_INTO_4328_GEOMETRY_CORE",
            "valid_for_claim": "False",
        },
        {
            "zero_id": "ZERO4329_3_Poynting_extra",
            "symbol": "R_standalone_Poynting",
            "zero_statement": "R_standalone_Poynting=0",
            "branch_conditions": "Poynting appears only as T_EM flux in Maxwell-Hodge Hilbert stress",
            "status": "CONDITIONAL_ZERO",
            "valid_for_claim": "False",
        },
    ]


def tail_rows() -> List[Dict[str, str]]:
    return [
        {
            "tail_id": "TAIL4329_0_Delta_chi_principal",
            "symbol": "Delta_chi_principal",
            "meaning": "principal constitutive tensor mismatch",
            "bound_contribution": "||Delta_chi_principal||",
            "when_live": "independent EM constitutive tensor or hidden EM metric survives",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4329_1_Delta_chi_skewon",
            "symbol": "Delta_chi_skewon",
            "meaning": "skewon/nonreciprocal/dissipative constitutive piece",
            "bound_contribution": "||Delta_chi_skewon||",
            "when_live": "non-Maxwell constitutive sector survives",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4329_2_dtheta_EM",
            "symbol": "dtheta_EM",
            "meaning": "axion-gradient/pseudoscalar or EM marker drift",
            "bound_contribution": "L||dtheta_EM||",
            "when_live": "theta_EM is not q-basic calibrated visible data",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4329_3_C_Hodge_hidden",
            "symbol": "C_Hodge_hidden",
            "meaning": "hidden/motion/time field defines a disformal or medium-like EM Hodge star",
            "bound_contribution": "|C_Hodge_hidden|",
            "when_live": "extra EM frame slot survives in the parent/effective action",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4329_4_C_Hodge_readout",
            "symbol": "C_Hodge_readout",
            "meaning": "readout regenerates Hodge or alpha response",
            "bound_contribution": "|C_Hodge_readout|",
            "when_live": "readout is not pure postprocessing",
            "status": "ZERO_IN_STANDARD_BRANCH_RETAINED_OUTSIDE",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4329_5_Delta_orientation_flux",
            "symbol": "Delta_orientation_flux",
            "meaning": "orientation/time-orientation or boundary normal mismatch",
            "bound_contribution": "|Delta_orientation_flux|",
            "when_live": "collar orientation is not fixed before variation",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4329_6_Phi_EM_rad",
            "symbol": "Phi_EM_rad",
            "meaning": "open radiative Poynting flux through the local collar",
            "bound_contribution": "|Phi_EM_rad|/M_ref or explicit boundary Hamiltonian flux",
            "when_live": "non-static/open radiative local system",
            "status": "BOUNDARY_ROW_RETAINED",
            "valid_for_claim": "False",
        },
        {
            "tail_id": "TAIL4329_7_b_alpha_CJQ",
            "symbol": "b_alpha + C_JQ",
            "meaning": "EM kinetic/current normalization drift",
            "bound_contribution": "|b_alpha|+|C_JQ|",
            "when_live": "alpha/current normalization is parent-active instead of calibrated q-basic data",
            "status": "RETAINED_OUTSIDE_BRANCH",
            "valid_for_claim": "False",
        },
    ]


def formula_rows() -> List[Dict[str, str]]:
    return [
        {
            "formula_id": "F4329_0_same_hodge_zero",
            "name": "same-Hodge zero",
            "formula": "fixed(g_obs,e_obs,orientation,vol_obs) and S_EM=-(4 mu0)^-1 int F wedge *_obs F with no chi_EM => Delta_Hodge_EM=0",
            "status": "CONDITIONAL_ZERO_DERIVED",
        },
        {
            "formula_id": "F4329_1_Dq_EM_closed_collar",
            "name": "Dq_EM closed-collar zero",
            "formula": "F4329_0 + q-basic EM constants + pure readout + Phi_EM_rad=0_or_boundary_routed => Dq_EM[Hperp]=Dq_EM_C1=0",
            "status": "CONDITIONAL_ZERO_IMPORTED",
        },
        {
            "formula_id": "F4329_2_no_poynting_double_count",
            "name": "Poynting owner",
            "formula": "S_i=-T_EM(n,e_i)=(E cross B)_i, so Poynting contributes through Hilbert EM stress and not as a second source force",
            "status": "OWNER_RULE",
        },
        {
            "formula_id": "F4329_3_constitutive_bound",
            "name": "open/deformed EM no-cancellation envelope",
            "formula": "||Delta_Hodge_EM|| <= ||Delta_chi_principal|| + ||Delta_chi_skewon|| + L||dtheta_EM|| + |C_Hodge_hidden| + |C_Hodge_readout| + |Delta_orientation_flux|",
            "status": "BOUND_RETAINED_OUTSIDE_BRANCH",
        },
        {
            "formula_id": "F4329_4_geometry_core_update",
            "name": "4328 geometry core after EM-Hodge branch import",
            "formula": "epsilon_geom_core <= C_coeff epsilon_coeff + C_readout epsilon_readout_frame + C_terminal epsilon_terminal + C_EMopen epsilon_EM_open_boundary + tail_guard_sum",
            "status": "REDUCED_BUT_OPEN",
        },
        {
            "formula_id": "F4329_5_source_readout_update",
            "name": "source-readout after EM-Hodge reduction",
            "formula": "epsilon_source_readout <= (L_T L_mg + L_g) epsilon_geom_core_after_EM + Xi_src_hidden",
            "status": "NONCLAIM_HANDOFF",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4329_0_standard_visible_closed_collar",
            "branch_input": "standard visible q-basic same-Hodge static closed-collar branch",
            "action": "ALLOW_EM_HODGE_FRAME_ZERO",
            "output": "epsilon_EM_Hodge_frame=0, Dq_EM=0, Delta_Hodge_EM=0",
            "claim_policy": "private nonclaim until coefficient/Xi/projection gates close",
        },
        {
            "runner_id": "RUN4329_1_open_radiation",
            "branch_input": "open/radiative EM collar",
            "action": "KEEP_BOUNDARY_FLUX_ROW",
            "output": "epsilon_EM_open_boundary receives Phi_EM_rad",
            "claim_policy": "must be source-backed before local test use",
        },
        {
            "runner_id": "RUN4329_2_constitutive_deformation",
            "branch_input": "independent chi_EM or hidden/disformal EM Hodge slot",
            "action": "KEEP_CONSTITUTIVE_BOUND",
            "output": "Delta_Hodge_EM envelope retained",
            "claim_policy": "no zero, no local-GR claim",
        },
        {
            "runner_id": "RUN4329_3_global_Maxwell_alpha",
            "branch_input": "derive Maxwell/QED/alpha_EM/charge scale from same-Hodge local branch",
            "action": "REJECT",
            "output": "Hodge matching fixes cone/operator shape, not coupling scale or QED",
            "claim_policy": "firewall",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4329_0_global_Maxwell",
            "forbidden_shortcut": "same-Hodge local closure proves global Maxwell/QED",
            "reason": "the branch imports calibrated visible Maxwell-Hodge, it does not derive global EM",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4329_1_alpha_charge",
            "forbidden_shortcut": "Delta_Hodge_EM=0 predicts alpha_EM or charge normalization",
            "reason": "Hodge uniqueness does not fix Maxwell kinetic/current normalization",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4329_2_open_radiation",
            "forbidden_shortcut": "erase radiative Poynting flux",
            "reason": "open EM flux is boundary/Hamiltonian data, not a zero",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4329_3_overpromote_DqEM",
            "forbidden_shortcut": "use Dq_EM=0 outside the standard visible closed-collar branch",
            "reason": "deformed/open EM branches retain explicit tail rows",
            "status": "BLOCK",
        },
        {
            "firewall_id": "FW4329_4_local_GR_claim",
            "forbidden_shortcut": "claim local GR/R10/PPN/clock pass from EM closure alone",
            "reason": "coefficient drift, readout-frame, terminal and Xi_src_hidden gates remain open",
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
            "summary": "The live 4328 EM/Hodge frame tail is conditionally removed in the standard visible same-Hodge closed-collar branch by importing 4259-4263 and 4315. Outside that branch the constitutive/open-radiation tail bound remains.",
            "next_action": NEXT_TARGET,
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4329_0_EM_Hodge",
            "item": "epsilon_EM_Hodge_frame",
            "status": "CONDITIONAL_ZERO_IN_STANDARD_BRANCH",
            "notes": "removed from 4328 geometry core only under same-Hodge q-basic closed-collar branch",
        },
        {
            "status_id": "STAT4329_1_Dq_EM",
            "item": "Dq_EM[Hperp]",
            "status": "CONDITIONAL_ZERO_IMPORTED",
            "notes": "4259-4263 already adopted this for standard visible static tests",
        },
        {
            "status_id": "STAT4329_2_open_EM",
            "item": "open/deformed EM",
            "status": "BOUND_RETAINED",
            "notes": "constitutive and radiative tails remain outside branch",
        },
        {
            "status_id": "STAT4329_3_geometry_core",
            "item": "epsilon_geom_core",
            "status": "REDUCED_BUT_OPEN",
            "notes": "coefficient drift/readout/terminal/Xi tails remain",
        },
        {
            "status_id": "STAT4329_4_next",
            "item": "epsilon_coeff",
            "status": "NEXT_TARGET",
            "notes": "coefficient drift is now the cleanest remaining geometry-tail target",
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4329_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can the coefficient drift epsilon_coeff be zeroed by q-basic parent coefficient ownership, or must it become a source-backed finite tail?",
            "preferred_route": "prove all local visible coefficients in the reduced branch are q-basic/calibrated before variation and not hidden field functions",
            "fallback_route": "write finite coefficient-drift rows for kappa/G_N calibration, EM normalization, source weights, clock constants and local projection matrices",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    FORMAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    formal = f"""# 345 - PPC4161 Dq-EM-Hodge Hperp zero or constitutive tail bound

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Private nonclaim

4329 does **not** prove global Maxwell/QED, `alpha_EM`, charge quantization, public local GR, Newtonian mechanics, R10, PPN, clock safety, or orbital safety.

It does make one real reduction in the current local-GR route: the `epsilon_EM_Hodge_frame` tail retained by 4328 is conditionally zero in the standard visible, q-basic, same-Hodge, static closed-collar branch.

## Derived branch law

The imported chain is:

```text
fixed(g_obs,e_obs,orientation,vol_obs)
+ S_EM=-(4 mu0)^-1 int F wedge *_obs F
+ no independent chi_EM / hidden EM metric
+ q-basic calibrated EM readout/couplings before variation
+ Poynting counted once as Hilbert EM flux
+ static closed collar or routed boundary flux
=> Delta_Hodge_EM=0
=> Dq_EM[Hperp]=Dq_EM_C1=0
=> epsilon_EM_Hodge_frame=0
```

Outside that branch, the constitutive/open-radiation envelope remains live.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Clause Audit

{md_table(tables["clauses"], ["clause_id", "clause", "statement", "status", "effect"])}

## Zero Rows

{md_table(tables["zeros"], ["zero_id", "symbol", "zero_statement", "branch_conditions", "status", "valid_for_claim"])}

## Retained Constitutive/Open Tails

{md_table(tables["tails"], ["tail_id", "symbol", "meaning", "bound_contribution", "status", "valid_for_claim"])}

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
    post = f"""# 4329 Y5-R2FR Dq-EM-Hodge Hperp zero or constitutive tail bound

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

`epsilon_EM_Hodge_frame` is no longer a vague geometry-tail bucket in the standard local branch. It is zero if the same observed Hodge Maxwell action, q-basic calibrated EM readout, Hilbert-owned Poynting flux, and closed-collar/static boundary clauses all hold.

This is still private and conditional. Open radiation, independent constitutive tensors, hidden EM metrics, alpha/current drift, and global Maxwell/QED remain outside the claim.

## Reduced Geometry Core

{md_table(tables["formulas"], ["formula_id", "formula", "status"])}

## Remaining Tails

{md_table(tables["tails"], ["tail_id", "symbol", "when_live", "bound_contribution", "status"])}

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

    add("VAL4329_sources_exist", "all source paths exist", all(r["path_exists"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4329_needles_found", "all source anchors found", all(r["needle_found"] == "True" for r in tables["sources"]), "source_register")
    add("VAL4329_same_hodge_zero", "Delta_Hodge_EM zero row exists", any(r["symbol"] == "Delta_Hodge_EM" for r in tables["zeros"]), "zeros")
    add("VAL4329_DqEM_zero", "Dq_EM zero row exists", any(r["symbol"] == "Dq_EM[Hperp]" for r in tables["zeros"]), "zeros")
    add("VAL4329_live_tail_removed", "epsilon_EM_Hodge_frame zero row exists", any(r["symbol"] == "epsilon_EM_Hodge_frame" and "4328" in r["status"] for r in tables["zeros"]), "zeros")
    add("VAL4329_poynting_owner", "Poynting double-counting is blocked", any("Poynting" in r["symbol"] for r in tables["zeros"]) and any("Poynting" in r["forbidden_shortcut"] for r in tables["firewall"]), "zeros/firewall")
    add("VAL4329_constitutive_bound", "constitutive bound formula retained", any("Delta_chi_principal" in r["formula"] and "C_Hodge_hidden" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4329_geometry_formula_reduced", "geometry formula no longer carries epsilon_EM_Hodge_frame", any(r["formula_id"] == "F4329_4_geometry_core_update" and "epsilon_EM_Hodge_frame" not in r["formula"] and "epsilon_coeff" in r["formula"] for r in tables["formulas"]), "formulas")
    add("VAL4329_open_radiation_tail", "open radiation boundary tail retained", any(r["symbol"] == "Phi_EM_rad" for r in tables["tails"]), "tails")
    add("VAL4329_alpha_not_claimed", "alpha/current drift retained outside branch", any("b_alpha" in r["symbol"] for r in tables["tails"]) and any("alpha_EM" in r["forbidden_shortcut"] for r in tables["firewall"]), "tails/firewall")
    add("VAL4329_global_Maxwell_rejected", "global Maxwell/QED shortcut rejected", any("global Maxwell" in r["forbidden_shortcut"] for r in tables["firewall"]), "firewall")
    add("VAL4329_runner_modes", "runner has zero, bound and reject modes", {"ALLOW_EM_HODGE_FRAME_ZERO", "KEEP_CONSTITUTIVE_BOUND", "REJECT"}.issubset({r["action"] for r in tables["runner"]}), "runner")
    add("VAL4329_all_claim_flags_false", "all rows with valid_for_claim keep false", all(r.get("valid_for_claim", "False") == "False" for table in tables.values() for r in table if "valid_for_claim" in r), "all_tables")
    add("VAL4329_next_coeff", "next target is coefficient drift", any("coefficient-drift" in r["next_target"] and "epsilon_coeff" in r["target_question"] for r in tables["next"]), "next")
    add("VAL4329_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4329_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4329_post_next", "post doc names next target", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4329_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4329_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4329_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4329_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4329_SOURCE_REGISTER.csv",
        "clauses": SOURCE_DIR / "P8_Y5_R2FR_4329_EM_HODGE_CLAUSE_AUDIT.csv",
        "zeros": SOURCE_DIR / "P8_Y5_R2FR_4329_EM_HODGE_ZERO_ROWS.csv",
        "tails": SOURCE_DIR / "P8_Y5_R2FR_4329_CONSTITUTIVE_TAIL_BOUND.csv",
        "formulas": SOURCE_DIR / "P8_Y5_R2FR_4329_GEOMETRY_UPDATE_FORMULAS.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4329_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4329_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4329_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4329_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4329_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "clauses": clause_rows(),
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
## PPC4161 4329 Dq-EM-Hodge Hperp zero or constitutive tail bound

Marker: `{MARKER}`

4329 imports the older 4259-4263 EM branch into the newer 4328 geometry bottleneck. In the standard visible, q-basic, same-Hodge, static closed-collar branch, `Delta_Hodge_EM=0`, `Dq_EM[Hperp]=Dq_EM_C1=0`, and the live `epsilon_EM_Hodge_frame` tail is removed from the reduced geometry core. Open/deformed EM remains explicit through constitutive and radiative boundary tail rows. No global Maxwell/QED, `alpha_EM`, charge scale, local-GR, PPN, R10, clock, or orbital claim fires.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4329 packet Dq-EM-Hodge branch import

Marker: `{PACKET_MARKER}`

Packet update: the EM/Hodge geometry tail is now branch-resolved rather than vague. Same-Hodge Maxwell plus q-basic calibrated EM readout and closed-collar Poynting routing gives a private conditional zero; constitutive deformation, open radiation, alpha/current scale, coefficient drift and `Xi_src_hidden` remain live outside that branch.
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
