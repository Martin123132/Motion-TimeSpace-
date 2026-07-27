from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4343"
CLAIM_ID = "L-184"
BRANCH = "MTS_R2FR_Y5_PARENT_ACTION_OWNER_FOR_KGAMMA_OR_KPERP_SECTOR_BOUND_RUNNER_4343"
DECISION = "KGAMMA_AUXILIARY_MULTIPLIER_OWNER_ACTION_DERIVED_METRIC_NULL_IF_ADJOINT_ZERO_KPERP_BOUND_RUNNER_RETAINED_NONCLAIM"
MARKER = "PPC4161_PARENT_ACTION_OWNER_FOR_KGAMMA_OR_KPERP_SECTOR_BOUND_RUNNER_4343"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_OWNER_FOR_KGAMMA_OR_KPERP_SECTOR_BOUND_RUNNER_4343"
NEXT_TARGET = "4344-Y5-R2FR-adjoint-zero-and-boundary-kernel-proof-or-first-Kperp-score-row.md"

FORMAL_PATH = FORMAL / "359-PPC4161-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md"
DOC_PATH = POST / "4343-Y5-R2FR-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4343_VALIDATION.csv"
GENERATED_UTC = datetime.now(timezone.utc).isoformat(timespec="seconds")

Y_GAMMA_LIMIT = 0.0002739826487147268
Y_BETA_LIMIT = 0.0009529831259642674
Y_CLOCK_LIMIT = 0.0006134828873394971


SOURCES = [
    (
        "SRC4343_00_4342_next",
        FORMAL / "358-PPC4161-KL-generator-for-KGamma-and-CRI-CDeltaKdiv-zero-branch.md",
        "4343-Y5-R2FR-parent-action-owner-for-KGamma-or-Kperp-sector-bound-runner.md",
        "4342 handoff selecting parent owner or Kperp bound route.",
    ),
    (
        "SRC4343_01_4342_KL",
        FORMAL / "358-PPC4161-KL-generator-for-KGamma-and-CRI-CDeltaKdiv-zero-branch.md",
        "Box A_Gamma^nu = -partial^nu Gamma_eff.",
        "Constructive KGamma generator to be parent-owned.",
    ),
    (
        "SRC4343_02_137_best_route",
        FORMAL / "137-transition-source-lift-action-block.md",
        "This is the best route, but it needs a parent action/source-lift block.",
        "Earlier source-lift file demanded an action block, not notation.",
    ),
    (
        "SRC4343_03_137_owner_equation",
        FORMAL / "137-transition-source-lift-action-block.md",
        "nabla_mu K_A^{mu nu} = -q_A^nu.",
        "Generic owner equation precedent.",
    ),
    (
        "SRC4343_04_138_hidden_stress",
        FORMAL / "138-metric-null-action-block-contract.md",
        "The metric-null transition block must be covariant without hidden metric stress.",
        "Metric-null owner block cannot hide stress in covariance.",
    ),
    (
        "SRC4343_05_138_C0C9",
        FORMAL / "138-metric-null-action-block-contract.md",
        "contract completeness = C0-C9 defined.",
        "Full metric-null contract remains the parent standard.",
    ),
    (
        "SRC4343_06_220_sector_split",
        FORMAL / "220-PPC4161-Kperp-sector-placement-theorem.md",
        "K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.",
        "Kperp sector split for fallback scoring.",
    ),
    (
        "SRC4343_07_220_no_claim",
        FORMAL / "220-PPC4161-Kperp-sector-placement-theorem.md",
        "The current corpus still lacks the parent EH/coframe identity, so no local-GR claim follows yet.",
        "Kperp sector placement is not yet a local-GR pass.",
    ),
    (
        "SRC4343_08_217_finite_ceiling",
        FORMAL / "217-PPC4161-Kperp-finite-coefficient-vector.md",
        "|W_i^K| C_T (|S_T|+|B_T|+|I_T|+|Z_T|) <= bound_i.",
        "Existing finite Kperp arena-bound formula.",
    ),
    (
        "SRC4343_09_216_energy_bound",
        FORMAL / "216-PPC4161-Kperp-boundary-zero-or-demotion.md",
        "||K_perp||_E <= C_T (||S_T|| + ||B_T|| + ||I_T|| + ||Z_T||).",
        "Existing Kperp energy bound.",
    ),
    (
        "SRC4343_10_194_Gcal",
        FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md",
        "G_cal := c^4 kappa_eff/(8*pi).",
        "Calibrated source-coupling caveat: local route does not predict G_N.",
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


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, path, needle, role in SOURCES:
        line_number = find_line(path, needle)
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
            }
        )
    return rows


def action_rows() -> List[Dict[str, str]]:
    return [
        {
            "action_id": "ACT4343_0_multiplier_owner",
            "name": "KGamma constrained auxiliary owner",
            "action_block": "S_RI=int_U sqrt(-g) Lambda_nu [L_RI A_Gamma^nu + nabla^nu Gamma_eff]",
            "fields": "A_Gamma^nu, Lambda_nu, Gamma_eff, g_mu_nu",
            "purpose": "parent-own the K_L/KGamma right-inverse equation before local scoring",
            "status": "CANDIDATE_PARENT_EXTENSION_DERIVED",
            "valid_for_claim": "False",
        },
        {
            "action_id": "ACT4343_1_flat_reduction",
            "name": "fixed flat reduction",
            "action_block": "S_RI^flat=int_U Lambda_nu [Box A_Gamma^nu + partial^nu Gamma_eff]",
            "fields": "A_Gamma^nu, Lambda_nu",
            "purpose": "recover Box A_Gamma=-grad Gamma and KGamma=K_L[A_Gamma] in fixed weak-field patch",
            "status": "DERIVED_LOCAL_FLAT_ACTION_SHAPE",
            "valid_for_claim": "False",
        },
        {
            "action_id": "ACT4343_2_covariant_operator",
            "name": "Ricci-corrected covariant owner",
            "action_block": "L_RI A^nu=(Box delta^nu_sigma+Ric^nu_sigma)A^sigma",
            "fields": "A_Gamma^nu, Lambda_nu, g_mu_nu",
            "purpose": "make the KGamma generator covariant instead of a post-hoc flat inverse",
            "status": "DERIVED_OPERATOR_FORM_KERNEL_AND_BOUNDARY_OPEN",
            "valid_for_claim": "False",
        },
        {
            "action_id": "ACT4343_3_metric_null_condition",
            "name": "adjoint multiplier kill condition",
            "action_block": "delta_A S_RI -> L_RI^dagger Lambda=0 plus boundary terms",
            "fields": "Lambda_nu",
            "purpose": "if Lambda=0 by adjoint no-kernel and boundary data, on-shell S_RI stress vanishes with the constraint",
            "status": "METRIC_NULL_ROUTE_DERIVED_CONDITIONAL",
            "valid_for_claim": "False",
        },
    ]


def euler_rows() -> List[Dict[str, str]]:
    return [
        {
            "el_id": "EL4343_0_vary_Lambda",
            "variation": "delta Lambda_nu",
            "equation": "L_RI A_Gamma^nu + nabla^nu Gamma_eff = 0",
            "consequence": "KGamma right-inverse identity follows through the K_L map",
            "status": "DERIVED",
            "valid_for_claim": "False",
        },
        {
            "el_id": "EL4343_1_vary_A",
            "variation": "delta A_Gamma^nu",
            "equation": "L_RI^dagger Lambda_nu = 0 plus boundary/corner terms",
            "consequence": "Lambda=0 if adjoint has no kernel and boundary data kill homogeneous modes",
            "status": "DERIVED_ADJOINT_ZERO_TARGET",
            "valid_for_claim": "False",
        },
        {
            "el_id": "EL4343_2_vary_metric",
            "variation": "delta g_mu_nu",
            "equation": "T_RI^(mu nu)=constraint-proportional terms + Lambda-proportional terms + boundary/corner terms",
            "consequence": "T_RI=0 only if constraint=0, Lambda=0, and boundary/corner stress is zero or routed",
            "status": "METRIC_NULL_CONDITIONAL_NOT_PARENT_SIGNED",
            "valid_for_claim": "False",
        },
        {
            "el_id": "EL4343_3_fail_branch",
            "variation": "failed adjoint/boundary kernel",
            "equation": "Lambda != 0 or B_RI != 0",
            "consequence": "owner block has a real metric stress tail and must enter Y_a",
            "status": "FINITE_BOUND_BRANCH_RETAINED",
            "valid_for_claim": "False",
        },
    ]


def metric_null_rows() -> List[Dict[str, str]]:
    return [
        {
            "audit_id": "MN4343_0_C0C9",
            "test": "C0-C9 metric-null contract",
            "finding": "the multiplier action targets C2/C3/C6/C7, but C0-C9 is not globally parent-adopted",
            "result": "PARTIAL_ADVANCE_NOT_FULL_CONTRACT",
            "next_action": "prove adjoint zero, boundary silence, covariance and block split simultaneously",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MN4343_1_no_hidden_stress",
            "test": "hidden metric stress",
            "finding": "on-shell stress is zero only if both the constraint and Lambda vanish and boundary/corner terms vanish",
            "result": "CONDITIONAL_METRIC_NULL_ROUTE",
            "next_action": "prove L_RI^dagger has no admissible zero modes under chosen boundary data",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MN4343_2_boundary",
            "test": "boundary/corner silence",
            "finding": "boundary data are still not source-fixed; boundary stress B_RI is kept as a scored row",
            "result": "BOUNDARY_ROW_OPEN",
            "next_action": "choose fixed Dirichlet/retarded/collar data and prove no boundary metric injection",
            "valid_for_claim": "False",
        },
        {
            "audit_id": "MN4343_3_Gcal_caveat",
            "test": "Newton coupling claim",
            "finding": "this owner route does not predict G_N; local coupling remains calibrated through G_cal",
            "result": "NO_GN_PREDICTION_CLAIM",
            "next_action": "keep calibrated source-coupling caveat in all local-GR summaries",
            "valid_for_claim": "False",
        },
    ]


def kperp_rows() -> List[Dict[str, str]]:
    return [
        {
            "kperp_id": "KP4343_0_sector_split",
            "quantity": "K_perp",
            "formula": "K_perp=K_metric_TT+K_vertical+K_boundary+K_extra_source",
            "condition": "sector labels fixed before scoring",
            "output": "only K_extra_source is an independent local residual",
            "status": "IMPORTED_SECTOR_SPLIT",
            "valid_for_claim": "False",
        },
        {
            "kperp_id": "KP4343_1_clean_zero",
            "quantity": "R_i^K",
            "formula": "R_i^K=0 if K_perp is GR TT/radiative, vertical quotient, or routed boundary with zero local projection",
            "condition": "EH/coframe identity, Dq=0/e_obs descent, and boundary readout route parent-signed",
            "output": "no extra Kperp score",
            "status": "CLEAN_ROUTE_PARENT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "kperp_id": "KP4343_2_finite_bound",
            "quantity": "||K_perp||_E",
            "formula": "||K_perp||_E <= C_T(||S_T||+||B_T||+||I_T||+||Z_T||)",
            "condition": "positive tensor operator, finite source/boundary/incoming/zero-mode rows",
            "output": "|R_i^K| <= W_i^K ||K_perp||_E",
            "status": "FINITE_RUNNER_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
        {
            "kperp_id": "KP4343_3_total_vector",
            "quantity": "Y_a^4343",
            "formula": "Y_a^4343 <= Pi_a^RI C_RI_curved + Pi_a^BRI B_RI + W_a^K C_T(S_T+B_T+I_T+Z_T)",
            "condition": "used if adjoint-zero or Kperp clean route fails",
            "output": f"compare to PPN_gamma<={Y_GAMMA_LIMIT}, PPN_beta<={Y_BETA_LIMIT}, clock<={Y_CLOCK_LIMIT}, plus R10/orbital/WEP gates",
            "status": "NONCLAIM_BOUND_VECTOR_READY",
            "valid_for_claim": "False",
        },
    ]


def input_rows() -> List[Dict[str, str]]:
    return [
        {
            "input_id": "IN4343_0_parent_adoption",
            "symbol": "S_RI",
            "definition": "parent adoption of the multiplier owner action",
            "status": "MISSING_PARENT_ADOPTION",
            "next_action": "decide whether S_RI is part of the parent action or remains a closure candidate",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4343_1_adjoint_gap",
            "symbol": "lambda_1(L_RI^dagger)",
            "definition": "no-kernel/coercivity gap for the adjoint multiplier equation",
            "status": "MISSING_ADJOINT_ZERO_PROOF",
            "next_action": "derive kernel-free boundary problem or score Lambda tail",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4343_2_boundary_stress",
            "symbol": "B_RI",
            "definition": "boundary/corner metric stress from integrating the owner block by parts",
            "status": "MISSING_ZERO_OR_BOUND",
            "next_action": "fix boundary data and prove B_RI=0 or source a finite bound",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4343_3_Kperp_sector",
            "symbol": "K_extra_source",
            "definition": "unrouted Kperp sector after GR TT/vertical/boundary placement",
            "status": "MISSING_ZERO_OR_BOUND",
            "next_action": "prove no extra sector or score Kperp finite runner",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4343_4_Kperp_coefficients",
            "symbol": "C_T,S_T,B_T,I_T,Z_T,W_i^K",
            "definition": "finite Kperp bound and arena transfer coefficients",
            "status": "MISSING_NUMERIC_SOURCE_ROWS",
            "next_action": "fill first source-backed Kperp row if clean route remains unsigned",
            "valid_for_claim": "False",
        },
        {
            "input_id": "IN4343_5_arena_projection",
            "symbol": "Pi_a^RI, Pi_a^BRI",
            "definition": "projection constants from owner commutator/boundary stress to local arenas",
            "status": "MISSING_ARENA_PROJECTION_CONSTANTS",
            "next_action": "fix before any R10/PPN/clock/orbital/WEP score",
            "valid_for_claim": "False",
        },
    ]


def branch_rows() -> List[Dict[str, str]]:
    return [
        {
            "branch_id": "BR4343_0_clean_owner",
            "branch": "adjoint-zero metric-null owner",
            "conditions": "S_RI parent-adopted; constraint=0; L_RI^dagger Lambda=0 has only Lambda=0; B_RI=0",
            "output": "KGamma owner has no extra local metric stress",
            "status": "BEST_ROUTE_DERIVED_CONDITIONS_OPEN",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4343_1_owner_tail",
            "branch": "owner stress tail",
            "conditions": "Lambda zero proof or boundary silence fails",
            "output": "score Pi_a^RI C_RI_curved + Pi_a^BRI B_RI",
            "status": "FINITE_BOUND_ROUTE",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4343_2_Kperp_clean",
            "branch": "Kperp sector non-extra",
            "conditions": "Kperp is GR TT/radiative, vertical quotient, or routed boundary",
            "output": "W_i^K=0 for independent extra source",
            "status": "PARENT_SECTOR_SIGNATURE_OPEN",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR4343_3_Kperp_score",
            "branch": "Kperp finite score",
            "conditions": "K_extra_source remains",
            "output": "score W_i^K C_T(S_T+B_T+I_T+Z_T)",
            "status": "FALLBACK_RUNNER_READY_VALUES_MISSING",
            "valid_for_claim": "False",
        },
    ]


def runner_rows() -> List[Dict[str, str]]:
    return [
        {
            "runner_id": "RUN4343_0_current",
            "branch_input": "current corpus through 4342",
            "action": "ADOPT_MULTIPLIER_OWNER_CANDIDATE_KEEP_CLAIM_FALSE",
            "output": "parent owner action shape derived; adjoint-zero and boundary gates selected; Kperp finite runner retained",
            "claim_policy": "no local-GR/R10/PPN/clock/orbital/WEP claim",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4343_1_zero_future",
            "branch_input": "adjoint-zero owner plus Kperp non-extra sector signed",
            "action": "ALLOW_THIS_TRANSITION_CHANNEL_CLOSURE",
            "output": "KGamma owner and Kperp no-extra branch quiet this channel",
            "claim_policy": "still requires remaining P_leak/source/projection gates",
            "valid_for_claim": "False",
        },
        {
            "runner_id": "RUN4343_2_bound_future",
            "branch_input": "owner/Kperp finite rows",
            "action": "RUN_NONCLAIM_LOCAL_VECTOR_SCORE",
            "output": "score Y_a^4343 against local arenas",
            "claim_policy": "claim only if all rows numeric, source-backed, fixed before scoring, and below gates",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    return [
        {
            "firewall_id": "FW4343_0",
            "forbidden_shortcut": "Treating a candidate S_RI as already in the parent action",
            "reason": "4343 derives a candidate extension; parent adoption is still an explicit missing input.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4343_1",
            "forbidden_shortcut": "Ignoring the adjoint multiplier equation",
            "reason": "Lambda != 0 creates a real metric stress tail.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4343_2",
            "forbidden_shortcut": "Calling covariance metric-null without boundary/corner stress control",
            "reason": "C7 hidden-stress issue is exactly the old failure mode.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4343_3",
            "forbidden_shortcut": "Treating Kperp sector placement as Kperp zero",
            "reason": "K_extra_source remains scoreable unless parent sector clauses remove it.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
        {
            "firewall_id": "FW4343_4",
            "forbidden_shortcut": "Claiming fundamental prediction of G_N",
            "reason": "local coupling remains calibrated as G_cal unless a parent scale law fixes kappa_*.",
            "status": "ACTIVE",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4343_0",
            "decision": DECISION,
            "reason": "a concrete multiplier owner action can parent-own KGamma and be metric-null if its adjoint multiplier and boundary stress vanish; otherwise the exact finite local vector is now exposed",
            "next_action": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4343_0",
            "item": "KGamma parent owner",
            "status": "CANDIDATE_ACTION_DERIVED_NOT_ADOPTED",
            "notes": "S_RI multiplier block is the first concrete parent-action route for KGamma",
        },
        {
            "status_id": "STAT4343_1",
            "item": "metric nullity",
            "status": "REDUCED_TO_ADJOINT_ZERO_AND_BOUNDARY_SILENCE",
            "notes": "hidden stress is no longer vague; it is Lambda and B_RI",
        },
        {
            "status_id": "STAT4343_2",
            "item": "Kperp",
            "status": "SECTOR_CLEAN_OR_FINITE_SCORE",
            "notes": "K_extra_source is the surviving scoreable sector if clean placement fails",
        },
        {
            "status_id": "STAT4343_3",
            "item": "next target",
            "status": "ADJOINT_ZERO_OR_FIRST_KPERP_ROW",
            "notes": NEXT_TARGET,
        },
    ]


def next_rows() -> List[Dict[str, str]]:
    return [
        {
            "next_target_id": "NT4343_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can L_RI^dagger Lambda=0 with chosen boundary data force Lambda=0 and B_RI=0, or must the first Kperp/source-tail score row be filled?",
            "preferred_route": "prove adjoint no-kernel plus boundary/corner silence for S_RI, then use Kperp sector placement to remove K_extra_source",
            "fallback_route": "fill first nonclaim Kperp or owner-tail row: C_T, S_T, B_T, I_T, Z_T, W_i^K, B_RI, Pi_a^RI",
        }
    ]


def write_docs(tables: Dict[str, List[Dict[str, str]]]) -> None:
    formal = f"""# 359 PPC4161 parent action owner for KGamma or Kperp sector bound runner

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Claim Status

Private nonclaim. This checkpoint does not prove public local GR, Newton, R10, PPN, clock safety, orbital safety, WEP safety, Maxwell closure, or a fundamental prediction of `G_N`.

## Result

4343 turns the 4342 `K_L/KGamma` generator into a concrete parent-action candidate:

```text
S_RI = int_U sqrt(-g) Lambda_nu [ L_RI A_Gamma^nu + nabla^nu Gamma_eff ].
```

The Euler-Lagrange split is:

```text
delta Lambda:  L_RI A_Gamma^nu + nabla^nu Gamma_eff = 0
delta A:       L_RI^dagger Lambda_nu = 0 + boundary/corner terms
delta g:       T_RI = constraint terms + Lambda terms + boundary/corner terms.
```

So the parent-owner route is now precise:

```text
constraint = 0,
Lambda = 0,
B_RI = 0
=> T_RI = 0
```

and the `KGamma` owner is metric-null on shell. If the adjoint equation has a kernel, or boundary/corner stress survives, that is no longer a foggy objection; it is a finite local-test tail:

```text
Y_a^4343 <= Pi_a^RI C_RI_curved + Pi_a^BRI B_RI
          + W_a^K C_T(S_T+B_T+I_T+Z_T).
```

`K_perp` is also made decision-ready:

```text
K_perp = K_metric_TT + K_vertical + K_boundary + K_extra_source.
```

Only `K_extra_source` is an independent MTS local residual. If it cannot be killed by parent sector placement, it must be scored by the existing Kperp finite-bound runner.

## Source Register

{md_table(tables["sources"], ["source_id", "path", "path_exists", "needle_found", "line_number", "role"])}

## Action Candidate

{md_table(tables["actions"], ["action_id", "name", "action_block", "fields", "purpose", "status", "valid_for_claim"])}

## Euler-Lagrange Rows

{md_table(tables["euler"], ["el_id", "variation", "equation", "consequence", "status", "valid_for_claim"])}

## Metric-Null Audit

{md_table(tables["metric_null"], ["audit_id", "test", "finding", "result", "next_action", "valid_for_claim"])}

## Kperp Runner

{md_table(tables["kperp"], ["kperp_id", "quantity", "formula", "condition", "output", "status", "valid_for_claim"])}

## Required Inputs

{md_table(tables["inputs"], ["input_id", "symbol", "definition", "status", "next_action", "valid_for_claim"])}

## Branch Runner

{md_table(tables["branches"], ["branch_id", "branch", "conditions", "output", "status", "valid_for_claim"])}

## Runner

{md_table(tables["runner"], ["runner_id", "branch_input", "action", "output", "claim_policy", "valid_for_claim"])}

## Claim Firewall

{md_table(tables["firewall"], ["firewall_id", "forbidden_shortcut", "reason", "status", "valid_for_claim"])}

## Decision

{md_table(tables["decision"], ["decision_id", "decision", "reason", "next_action", "claim_allowed", "valid_for_claim"])}

## Status

{md_table(tables["status"], ["status_id", "item", "status", "notes"])}

## Next Target

{md_table(tables["next"], ["next_target_id", "next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    post = f"""# 4343 Y5-R2FR parent action owner for KGamma or Kperp sector bound runner

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4343 builds the first concrete parent-action candidate for the `K_L/KGamma` route:

```text
S_RI = int sqrt(-g) Lambda_nu [L_RI A_Gamma^nu + nabla^nu Gamma_eff].
```

It is metric-null only if the adjoint equation forces `Lambda=0` and boundary stress `B_RI=0`. If not, the failure is now a scored local tail, not a vague objection. `Kperp` is split into GR TT, vertical, boundary, and extra-source sectors; only the extra-source sector survives as an independent bound row.

## Handoff

{md_table(tables["next"], ["next_target", "target_question", "preferred_route", "fallback_route"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")
    DOC_PATH.write_text(post, encoding="utf-8")


def append_claim_once() -> None:
    path = FORMAL / "02-claims-register.csv"
    existing = read_text(path)
    if CLAIM_ID in existing:
        return
    with path.open("a", newline="", encoding="utf-8") as handle:
        if existing and not existing.endswith("\n"):
            handle.write("\n")
        writer = csv.writer(handle)
        writer.writerow(
            [
                CLAIM_ID,
                "local_gr",
                (
                    "4343 derives a concrete multiplier parent-action candidate for the K_L/KGamma route: S_RI=int sqrt(-g) Lambda_nu[L_RI A_Gamma^nu+nabla^nu Gamma_eff]. "
                    "Variation in Lambda gives the right-inverse owner equation; variation in A gives the adjoint equation L_RI^dagger Lambda=0; variation in the metric shows the owner block is metric-null only if the constraint, Lambda and boundary/corner stress vanish. "
                    "Thus hidden stress is reduced to explicit Lambda and B_RI gates. The surviving Kperp sector is split into GR TT, vertical, boundary and K_extra_source pieces; only K_extra_source remains as an independent finite local residual if clean sector placement fails."
                ),
                "4343 source register, action candidate rows, Euler-Lagrange rows, metric-null audit, Kperp runner, required inputs, branch runner, runner, firewall, decision, status, next-target and validation CSV.",
                "private_multiplier_parent_owner_for_KGamma_adjoint_zero_or_Kperp_bound_nonclaim",
                "Prove L_RI^dagger Lambda=0 plus boundary data force Lambda=B_RI=0, or fill first Kperp/owner-tail score row.",
                "Treating candidate S_RI as parent-adopted; ignoring the adjoint multiplier; calling covariance metric-null without boundary stress control; treating Kperp sector placement as zero; or claiming a fundamental G_N prediction.",
            ]
        )


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

    add("VAL4343_sources_exist", "all source paths exist", all(row["path_exists"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4343_needles_found", "all source anchors found", all(row["needle_found"] == "True" for row in tables["sources"]), "source_register")
    add("VAL4343_action_candidate", "multiplier owner action row exists", any("Lambda_nu" in row["action_block"] for row in tables["actions"]), "actions")
    add("VAL4343_adjoint_equation", "adjoint equation row exists", any("dagger" in row["equation"] for row in tables["euler"]), "euler")
    add("VAL4343_metric_null_condition", "metric null condition requires Lambda and boundary zero", any("Lambda=0" in row["finding"] or "B_RI" in row["finding"] for row in tables["metric_null"]), "metric_null")
    add("VAL4343_kperp_sector", "Kperp sector split exists", any("K_extra_source" in row["formula"] for row in tables["kperp"]), "kperp")
    add("VAL4343_kperp_finite", "Kperp finite bound exists", any("C_T" in row["formula"] and "W_i" in row["output"] for row in tables["kperp"]), "kperp")
    add("VAL4343_parent_missing", "parent adoption remains missing", any(row["symbol"] == "S_RI" and row["status"] == "MISSING_PARENT_ADOPTION" for row in tables["inputs"]), "inputs")
    add("VAL4343_no_GN_claim", "fundamental GN prediction is firewalled", any("G_N" in row["forbidden_shortcut"] for row in tables["firewall"]), "firewall")
    add("VAL4343_no_claim_flags", "all valid_for_claim flags false", all(row.get("valid_for_claim", "False") == "False" for table in tables.values() for row in table if "valid_for_claim" in row), "all_tables")
    add("VAL4343_current_runner_nonclaim", "current runner keeps claim false", any(row["runner_id"] == "RUN4343_0_current" and "KEEP_CLAIM_FALSE" in row["action"] for row in tables["runner"]), "runner")
    add("VAL4343_next_target", "next target is 4344 adjoint zero or Kperp row", any("4344" in row["next_target"] for row in tables["next"]), "next")
    add("VAL4343_docs_exist", "formal and post docs exist", FORMAL_PATH.exists() and DOC_PATH.exists(), "docs")
    add("VAL4343_formal_marker", "formal marker exists", MARKER in read_text(FORMAL_PATH), "formal")
    add("VAL4343_post_handoff", "post doc contains handoff", NEXT_TARGET in read_text(DOC_PATH), "post")
    add("VAL4343_claim_row", f"{CLAIM_ID} claim-register row exists", CLAIM_ID in read_text(FORMAL / "02-claims-register.csv"), "claims")
    add("VAL4343_spine_marker", "spine marker exists", MARKER in read_text(FORMAL / "07-unification-spine.md"), "spine")
    add("VAL4343_packet_marker", "packet marker exists", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), "packet")

    for key, path in paths.items():
        if key == "validation":
            continue
        try:
            with path.open(newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
            parsed = True
        except Exception:
            parsed = False
        add(f"VAL4343_csv_parse_{key}", f"{key} CSV parses", parsed, str(path))

    return rows


def main() -> None:
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4343_SOURCE_REGISTER.csv",
        "actions": SOURCE_DIR / "P8_Y5_R2FR_4343_ACTION_CANDIDATE_ROWS.csv",
        "euler": SOURCE_DIR / "P8_Y5_R2FR_4343_EULER_LAGRANGE_ROWS.csv",
        "metric_null": SOURCE_DIR / "P8_Y5_R2FR_4343_METRIC_NULL_AUDIT.csv",
        "kperp": SOURCE_DIR / "P8_Y5_R2FR_4343_KPERP_BOUND_RUNNER.csv",
        "inputs": SOURCE_DIR / "P8_Y5_R2FR_4343_REQUIRED_INPUTS.csv",
        "branches": SOURCE_DIR / "P8_Y5_R2FR_4343_BRANCH_RUNNER.csv",
        "runner": SOURCE_DIR / "P8_Y5_R2FR_4343_RUNNER.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4343_CLAIM_FIREWALL.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4343_DECISION.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4343_STATUS.csv",
        "next": SOURCE_DIR / "P8_Y5_R2FR_4343_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    tables = {
        "sources": source_rows(),
        "actions": action_rows(),
        "euler": euler_rows(),
        "metric_null": metric_null_rows(),
        "kperp": kperp_rows(),
        "inputs": input_rows(),
        "branches": branch_rows(),
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
## PPC4161 4343 parent owner for KGamma

Marker: `{MARKER}`

4343 proposes the concrete owner action:

```text
S_RI = int sqrt(-g) Lambda_nu [L_RI A_Gamma^nu + nabla^nu Gamma_eff].
```

The route is metric-null only if `L_RI^dagger Lambda=0` forces `Lambda=0` and the boundary/corner stress `B_RI` vanishes. Otherwise the owner block contributes a finite local tail. `K_perp` is now split into GR TT, vertical, boundary, and `K_extra_source`; only the extra-source sector survives as an independent Kperp score.
""",
    )
    append_once(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        f"""
## 4343 packet parent owner for KGamma

Marker: `{PACKET_MARKER}`

Packet update: the KGamma route now has a candidate parent-action owner rather than a loose inverse. The live proof is adjoint-zero plus boundary silence; the fallback is a finite `Kperp`/owner-tail vector against local arenas.
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
