from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4297"
CLAIM_ID = "L-138"
BRANCH = "MTS_R2FR_Y5_QTR_VERTICAL_OR_TOPOLOGICAL_REST_PROOF_ATTEMPT_FOR_PNONHILBERT_4297"
DECISION = "QTR_VERTICAL_TOPOLOGICAL_REST_NOT_DERIVED_OBSTRUCTION_EXPLICIT_NONCLAIM"
MARKER = "PPC4161_QTR_VERTICAL_OR_TOPOLOGICAL_REST_PROOF_ATTEMPT_4297"
PACKET_MARKER = "PPC4161_PACKET_QTR_VERTICAL_OR_TOPOLOGICAL_REST_PROOF_ATTEMPT_4297"
NEXT_TARGET = "4298-Y5-R2FR-Gamma-Khat-hidden-dependence-factorization-or-first-Dv-qtr-bound-row.md"

FORMAL_PATH = FORMAL / "313-PPC4161-qtr-vertical-or-topological-rest-proof-attempt-for-PnonHilbert.md"
DOC_PATH = POST / "4297-Y5-R2FR-qtr-vertical-or-topological-rest-proof-attempt-for-PnonHilbert.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4297_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4297_00_4296_formal": (
        FORMAL / "312-PPC4161-Pleak-transition-component-zero-attempts-or-bound-row-selection.md",
        "prove Dq[q_tr]=0 or q_tr=dB/topological-rest.",
        "4296 handoff target for the P_nonHilbert proof attempt.",
    ),
    "SRC4297_01_4296_attempts": (
        SOURCE_DIR / "P8_Y5_R2FR_4296_COMPONENT_ZERO_ATTEMPTS.csv",
        "BEST_NEXT_ATTEMPT_NOT_YET_SIGNED",
        "4296 machine rows identify q-verticality as the next best attempt.",
    ),
    "SRC4297_02_4296_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4296_BOUND_SELECTION_ROWS.csv",
        "REQ4293_WEP",
        "4296 fallback bound selections remain active if verticality fails.",
    ),
    "SRC4297_03_193_quotient": (
        FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md",
        "R_proj = Pi_loc D Obar_loc[Dq[v]] = 0.",
        "Quotient naturality theorem that would kill local response if q_tr is vertical.",
    ),
    "SRC4297_04_298_qtr_def": (
        FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md",
        "q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}.",
        "Raw transition current definition used for the Dq expansion.",
    ),
    "SRC4297_05_137_source_lift": (
        FORMAL / "137-transition-source-lift-action-block.md",
        "Sigma_metric source lift parent-derived = false;",
        "Earlier source-lift route explicitly did not derive metric-nullity.",
    ),
    "SRC4297_06_138_metric_null": (
        FORMAL / "138-metric-null-action-block-contract.md",
        "metric_null_action_block_contract_defined_not_derived_route_contract_only",
        "Metric-null action route is contract-only.",
    ),
    "SRC4297_07_196_rest": (
        FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md",
        "q-owned exact/topological/silent rest.",
        "Minimal parent candidate allows silent rest but does not prove raw q_tr is in it.",
    ),
    "SRC4297_08_300_direct_fail": (
        FORMAL / "300-PPC4161-real-transition-shell-profile-calculator.md",
        "cannot be treated as a direct local metric source",
        "Direct metric-source route is failed and cannot be reused.",
    ),
    "SRC4297_09_301_nonlocal": (
        FORMAL / "301-PPC4161-transition-nonlocal-owner-kernel-or-explicit-local-closure-lock.md",
        "does **not** derive `K_Q`",
        "Nonlocal owner kernel remains not derived.",
    ),
}


def common() -> Dict[str, str]:
    return {
        "checkpoint": CHECKPOINT,
        "branch": BRANCH,
        "generated_utc": STAMP,
        "decision": DECISION,
    }


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_line(values: List[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="")
    writer.writerow(values)
    return handle.getvalue()


def append_unique_block(path: Path, marker: str, heading: str, body: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    block = f"\n\n## {heading}\n\nMarker: `{marker}`\n\n{body}\n"
    write_text(path, text.rstrip() + block)


def append_claim() -> None:
    path = FORMAL / "02-claims-register.csv"
    text = read_text(path)
    if any(line.startswith(f"{CLAIM_ID},") for line in text.splitlines()):
        return
    row = csv_line(
        [
            CLAIM_ID,
            "local_gr",
            (
                "4297 attempts the direct q_tr vertical/topological-rest proof for P_nonHilbert_action_domain. The exact "
                "variation of q_tr = grad Gamma_eff - div K_hat shows the required clauses: D_v Gamma_eff=0, D_v K_hat=0 "
                "or exact cancellation, the covariant-derivative/connection commutator vanishes, and boundary/topological "
                "support is fixed or routed. Current corpus does not parent-sign these clauses for raw q_tr. A hidden-scalar "
                "countermodel Gamma_eff=Gamma_bar(q)+epsilon I_hid with Dq[I_hid]=0 but D_v I_hid!=0 blocks automatic "
                "verticality. Topological/superpotential rest remains a viable route but not derived."
            ),
            (
                "4297 source register, Dq expansion, verticality clause audit, topological-rest attempt, obstruction "
                "ledger, fallback handoff rows, control cases, decision, firewall, status and validation CSV."
            ),
            "private_qtr_vertical_topological_rest_not_derived_nonclaim",
            (
                "Factor Gamma_eff and K_hat through q, or derive q_tr as q-owned topological/superpotential rest; otherwise "
                "fill first D_v q_tr bound rows against the 4293 suppression vector."
            ),
            (
                "Assuming quotient vertical silence applies to raw q_tr without proving q_tr in ker(Dq), treating "
                "conservation ownership as metric-nullity, or claiming local-GR/R10/WEP pass."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                **common(),
                "source_id": source_id,
                "path": str(path),
                "exists": str(path.exists()),
                "required_text": needle,
                "required_text_found": str(needle in text),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def dq_expansion_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "DQ4297_0_definition",
            "q_tr^nu",
            "nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
            "definition imported from 298",
            "KNOWN_DEFINITION",
        ),
        (
            "DQ4297_1_vertical_variation",
            "D_v q_tr^nu",
            "nabla^nu(D_v Gamma_eff) - nabla_mu(D_v K_hat^{mu nu}) + C_conn^nu[v; Gamma_eff,K_hat,g_obs]",
            "chain rule for a vertical variation v in ker(Dq)",
            "DERIVED_EXPANSION",
        ),
        (
            "DQ4297_2_exact_zero_condition",
            "D_v q_tr^nu = 0",
            "D_v Gamma_eff=0 and D_v K_hat^{mu nu}=0 and C_conn^nu=0, or exact parent identity cancels the full combination",
            "sufficient condition for quotient vertical silence to apply",
            "CONDITION_NOT_PARENT_SIGNED",
        ),
        (
            "DQ4297_3_response_zero_condition",
            "P_nonHilbert_action_domain q_tr = 0",
            "R_loc[D_v q_tr]=0 or Sigma_metric[q_tr]=0 or q_tr=dB/topological with fixed boundary",
            "weaker response-level condition if full D_v q_tr is not zero",
            "CONDITION_NOT_PARENT_SIGNED",
        ),
        (
            "DQ4297_4_bound_if_nonzero",
            "P_nonHilbert_action_domain q_tr != 0",
            "route to 4293 suppression vector and first D_v Gamma/Khat coefficient rows",
            "fallback if factorization/topological proof fails",
            "BOUND_ROUTE_ACTIVE",
        ),
    ]
    return [
        {
            **common(),
            "row_id": row_id,
            "object": obj,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for row_id, obj, formula, meaning, status in raw
    ]


def verticality_clause_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "VC4297_0_q_factor_Gamma",
            "Gamma_eff factors through q",
            "Gamma_eff(Phi)=Gamma_bar(q(Phi))",
            "D_v Gamma_eff=0",
            "UNSIGNED_FOR_RAW_QTR",
            "Gamma_eff may still carry hidden/transition dependence.",
        ),
        (
            "VC4297_1_q_factor_Khat",
            "K_hat factors through q",
            "K_hat^{mu nu}(Phi,g_obs)=Kbar^{mu nu}(q(Phi),g_obs)",
            "D_v K_hat=0 up to q-owned metric variation",
            "UNSIGNED_FOR_RAW_QTR",
            "K_hat was previously an owner/current object, not a parent-signed q-functor.",
        ),
        (
            "VC4297_2_connection_commutator",
            "covariant derivative commutes with vertical reduction",
            "C_conn^nu[v;Gamma_eff,K_hat,g_obs]=0",
            "no hidden metric/connection dependence in nabla",
            "UNSIGNED_FOR_RAW_QTR",
            "138 warns metric dependence can hide in sqrt(-g), nabla, contractions, or connections.",
        ),
        (
            "VC4297_3_parent_identity",
            "full combination cancels as a parent identity",
            "nabla^nu(D_v Gamma_eff)-nabla_mu(D_v K_hat^{mu nu})+C_conn^nu=0",
            "verticality without individual factorization",
            "NOT_DERIVED",
            "298 rejected pointwise Gamma/Khat cancellation and Div^-1 compensators.",
        ),
        (
            "VC4297_4_boundary_support",
            "boundary support is fixed/routed",
            "pullback B_v|partial W_loc fixed, exact, or Hamiltonian-routed",
            "vertical/topological rest has no local bulk response",
            "UNSIGNED_FOR_RAW_QTR",
            "137/138 list boundary/superpotential as open theorem route.",
        ),
        (
            "VC4297_5_verdict",
            "q_tr in ker(Dq)",
            "D_v q_tr=0 for all v in ker(Dq)",
            "would close P_nonHilbert by 193",
            "NOT_PROVED",
            "at least VC4297_0, VC4297_1, VC4297_2 and boundary support remain unsigned.",
        ),
    ]
    return [
        {
            **common(),
            "clause_id": clause_id,
            "clause": clause,
            "mathematical_statement": statement,
            "effect": effect,
            "status": status,
            "evidence_or_obstruction": evidence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for clause_id, clause, statement, effect, status, evidence in raw
    ]


def topological_rest_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "TR4297_0_exact_superpotential",
            "q_tr^nu = nabla_mu U^{[mu nu]}",
            "U has fixed/routed boundary pullback and no bulk Hilbert stress",
            "NOT_DERIVED",
            "137/138 list boundary/superpotential as possible only if derived.",
        ),
        (
            "TR4297_1_topological_density",
            "q_tr comes from variation of a topological density",
            "delta S_top/delta g_obs = 0 and no local coefficient/readout dependence",
            "NOT_DERIVED",
            "196 allows q-owned silent rest, but raw transition is not placed there.",
        ),
        (
            "TR4297_2_conservation_owner",
            "q_tr^nu + nabla_mu K_own^{mu nu}=0",
            "conservation accounting only",
            "INSUFFICIENT",
            "298 says owner conservation can still gravitate locally.",
        ),
        (
            "TR4297_3_nonlocal_owner_kernel",
            "q_Q^nu(x)=int K_Q(x,y) q_tr(y)",
            "nonlocal owner routes local metric response away",
            "NOT_DERIVED",
            "301 says K_Q is not derived from parent action/source-lift/response kernel.",
        ),
        (
            "TR4297_4_verdict",
            "q_tr topological rest",
            "q_tr=dB/topological/q-owned silent rest",
            "NOT_PROVED",
            "topological rest remains a route, not an achieved theorem.",
        ),
    ]
    return [
        {
            **common(),
            "rest_id": rest_id,
            "route": route,
            "required_condition": condition,
            "status": status,
            "evidence_or_obstruction": evidence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for rest_id, route, condition, status, evidence in raw
    ]


def obstruction_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "OBS4297_0_hidden_scalar_Gamma",
            "Gamma_eff = Gamma_bar(q) + epsilon I_hid",
            "Dq[I_hid]=0 but D_v I_hid != 0 gives D_v q_tr^nu = epsilon nabla^nu(D_v I_hid) when K_hat is q-owned.",
            "blocks automatic verticality from quotient language alone",
        ),
        (
            "OBS4297_1_hidden_Khat",
            "K_hat = Kbar(q) + epsilon H_hid^{mu nu}",
            "D_v q_tr^nu contains -epsilon nabla_mu(D_v H_hid^{mu nu}).",
            "requires K_hat factorization or parent cancellation identity",
        ),
        (
            "OBS4297_2_connection_dependence",
            "nabla = nabla[g_obs(Phi)] with hidden metric/connection channel",
            "C_conn^nu can survive even if scalar pieces look q-owned.",
            "requires same observed metric/coframe factorization before variation",
        ),
        (
            "OBS4297_3_Div_inverse_compensator",
            "K_hat = Div^-1(grad Gamma_eff)",
            "would cancel by construction but is boundary-dependent and not a parent identity.",
            "already rejected in 298",
        ),
        (
            "OBS4297_4_direct_shell_metric_source",
            "P_metric,loc q_tr direct",
            "fails the 4284/300 profile calculator by huge local-response factors.",
            "cannot be used as local-GR route",
        ),
    ]
    return [
        {
            **common(),
            "obstruction_id": obs_id,
            "countermodel_or_obstruction": model,
            "mathematical_effect": effect,
            "meaning": meaning,
            "retained": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for obs_id, model, effect, meaning in raw
    ]


def fallback_handoff_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row in csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4296_BOUND_SELECTION_ROWS.csv"):
        if row.get("component") != "P_nonHilbert_action_domain q_tr":
            continue
        rows.append(
            {
                **common(),
                "handoff_id": f"FH4297_{len(rows):02d}",
                "component": row["component"],
                "selected_bound_or_input": row["selected_bound_or_input"],
                "selected_value": row["selected_value"],
                "units": row["units"],
                "status": "ACTIVE_IF_4298_FACTORISATION_FAILS",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    rows.extend(
        [
            {
                **common(),
                "handoff_id": "FH4297_DVGAMMA",
                "component": "P_nonHilbert_action_domain q_tr",
                "selected_bound_or_input": "first_Dv_Gamma_eff_coefficient_row",
                "selected_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                "units": "observable-projected dimensionless coefficient",
                "status": "NEXT_BOUND_ROW_IF_FACTORISATION_FAILS",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            },
            {
                **common(),
                "handoff_id": "FH4297_DVKHAT",
                "component": "P_nonHilbert_action_domain q_tr",
                "selected_bound_or_input": "first_Dv_K_hat_coefficient_row",
                "selected_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                "units": "observable-projected dimensionless coefficient",
                "status": "NEXT_BOUND_ROW_IF_FACTORISATION_FAILS",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            },
        ]
    )
    return rows


def control_case_rows() -> List[Dict[str, str]]:
    cases = [
        ("CTRL4297_0_full_factorization", True, True, True, True, True, "PASS_QTR_VERTICAL"),
        ("CTRL4297_1_hidden_gamma", False, True, True, True, False, "FAIL_DV_GAMMA_LIVE"),
        ("CTRL4297_2_hidden_khat", True, False, True, True, False, "FAIL_DV_KHAT_LIVE"),
        ("CTRL4297_3_connection_live", True, True, False, True, False, "FAIL_CONNECTION_COMMUTATOR_LIVE"),
        ("CTRL4297_4_boundary_live", True, True, True, False, False, "FAIL_BOUNDARY_TOPOLOGICAL_SUPPORT_LIVE"),
        ("CTRL4297_5_parent_identity", False, False, False, True, False, "FAIL_DV_GAMMA_LIVE"),
    ]
    rows: List[Dict[str, str]] = []
    for case_id, gamma_factor, khat_factor, commutator_zero, boundary_fixed, expected_pass, expected_outcome in cases:
        actual_pass = gamma_factor and khat_factor and commutator_zero and boundary_fixed
        if actual_pass:
            actual_outcome = "PASS_QTR_VERTICAL"
        elif not gamma_factor:
            actual_outcome = "FAIL_DV_GAMMA_LIVE"
        elif not khat_factor:
            actual_outcome = "FAIL_DV_KHAT_LIVE"
        elif not commutator_zero:
            actual_outcome = "FAIL_CONNECTION_COMMUTATOR_LIVE"
        elif not boundary_fixed:
            actual_outcome = "FAIL_BOUNDARY_TOPOLOGICAL_SUPPORT_LIVE"
        else:
            actual_outcome = "FAIL_PARENT_IDENTITY_NOT_SUPPLIED"
        rows.append(
            {
                **common(),
                "control_id": case_id,
                "Gamma_eff_q_factorized": str(gamma_factor),
                "K_hat_q_factorized": str(khat_factor),
                "connection_commutator_zero": str(commutator_zero),
                "boundary_fixed_or_routed": str(boundary_fixed),
                "actual_pass": str(actual_pass),
                "expected_pass": str(expected_pass),
                "actual_outcome": actual_outcome,
                "expected_outcome": expected_outcome,
                "expected_matches_actual": str(actual_pass == expected_pass and actual_outcome == expected_outcome),
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "D4297_0",
            "decision": DECISION,
            "what_moved": "Raw q_tr verticality is now reduced to factorization of Gamma_eff and K_hat plus connection/boundary support; automatic quotient silence is blocked by an explicit hidden-scalar countermodel.",
            "best_next": "Try to prove Gamma_eff and K_hat factor through q, or fill first D_v Gamma/Khat bound rows.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4297_0_no_quotient_shortcut", "Quotient naturality applies only after proving q_tr is vertical or q-owned before variation."),
        ("FW4297_1_no_conservation_metric_null", "Conservation ownership is not metric-nullity and does not prove local response zero."),
        ("FW4297_2_no_div_inverse", "Boundary-dependent Div^-1 cancellation is not a parent identity."),
        ("FW4297_3_no_direct_shell_revival", "The failed direct shell metric-source route cannot be revived as verticality."),
        ("FW4297_4_nonclaim", "No local-GR/WEP/R10/PPN/clock/orbital claim is allowed from 4297."),
    ]
    return [
        {
            **common(),
            "firewall_id": fw_id,
            "rule": rule,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for fw_id, rule in raw
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STATUS4297_0",
            "q_tr_verticality_proved": "False",
            "q_tr_topological_rest_proved": "False",
            "obstruction_countermodel_retained": "True",
            "live_factorization_targets": "D_v Gamma_eff;D_v K_hat;C_conn;boundary_support",
            "fallback_rows_active": str(len(fallback_handoff_rows())),
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4297_0",
            "next_target": NEXT_TARGET,
            "objective": "Prove Gamma_eff and K_hat factor through q on the local transition branch, or fill first D_v Gamma_eff / D_v K_hat coefficient rows feeding the 4293 suppression vector.",
            "success_condition": "D_v Gamma_eff=0, D_v K_hat=0, C_conn=0 and boundary support fixed/routed, or numeric/source-backed rows for the surviving terms.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    return f"""
# 313 q_tr vertical or topological-rest proof attempt for P_nonHilbert

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Target

4296 left the best route:

```text
P_nonHilbert_action_domain q_tr = 0
```

by proving either:

```text
Dq[q_tr] = 0
```

or:

```text
q_tr = dB/topological/q-owned silent rest.
```

## Expansion

The raw transition current is:

```text
q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^(mu nu).
```

For a vertical variation `v in ker(Dq)`:

```text
D_v q_tr^nu
 = nabla^nu(D_v Gamma_eff)
 - nabla_mu(D_v K_hat^(mu nu))
 + C_conn^nu[v; Gamma_eff, K_hat, g_obs].
```

Therefore quotient silence requires:

```text
D_v Gamma_eff = 0,
D_v K_hat^(mu nu) = 0,
C_conn^nu = 0,
boundary/topological support fixed or routed.
```

or a parent identity proving the whole combination zero.

## Obstruction

Verticality is not automatic. A countermodel is:

```text
Gamma_eff = Gamma_bar(q) + epsilon I_hid,
Dq[I_hid] = 0,
D_v I_hid != 0.
```

Then:

```text
D_v q_tr^nu = epsilon nabla^nu(D_v I_hid)
```

unless `K_hat` cancels it by a parent identity. That identity is not in the current corpus.

## Topological-rest route

The route remains viable if one can prove:

```text
q_tr^nu = nabla_mu U^[mu nu]
```

with fixed/routed boundary pullback and no bulk Hilbert stress, or if `q_tr` comes from q-owned topological/silent rest. Current files identify this as an open theorem route, not a derived result.

## Status

```text
q_tr verticality proved = false
q_tr topological rest proved = false
```

Next target: `{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4297 Y5 R2FR q_tr vertical or topological-rest proof attempt

## Purpose

Try to prove the raw transition current is vertical or q-owned topological rest, so the first `P_leak` component vanishes without tuning.

## Outcome

The proof does not close. The exact expansion shows that `Gamma_eff`, `K_hat`, the covariant derivative/connection, and boundary support must all factor through the quotient or cancel by a parent identity. Current corpus does not sign that for raw `q_tr`.

## Next

Try to factor `Gamma_eff` and `K_hat` through `q`, or create first `D_v Gamma_eff` / `D_v K_hat` bound rows.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    expansion = csv_rows(paths["dq_expansion"])
    clauses = csv_rows(paths["verticality_clauses"])
    rest = csv_rows(paths["topological_rest"])
    obstructions = csv_rows(paths["obstructions"])
    handoff = csv_rows(paths["fallback_handoff"])
    controls = csv_rows(paths["control_cases"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4297_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited local sources exist"),
        ("VAL4297_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4297_2_dq_expansion",
            any(row["row_id"] == "DQ4297_1_vertical_variation" and "D_v Gamma_eff" in row["formula"] and "D_v K_hat" in row["formula"] for row in expansion),
            "D_v q_tr expansion is written",
        ),
        (
            "VAL4297_3_verticality_not_proved",
            any(row["clause_id"] == "VC4297_5_verdict" and row["status"] == "NOT_PROVED" for row in clauses),
            "verticality verdict remains not proved",
        ),
        (
            "VAL4297_4_topological_not_proved",
            any(row["rest_id"] == "TR4297_4_verdict" and row["status"] == "NOT_PROVED" for row in rest),
            "topological rest verdict remains not proved",
        ),
        (
            "VAL4297_5_countermodel_retained",
            any(row["obstruction_id"] == "OBS4297_0_hidden_scalar_Gamma" and row["retained"] == "True" for row in obstructions),
            "hidden scalar countermodel is retained",
        ),
        (
            "VAL4297_6_handoff_rows",
            any(row["selected_bound_or_input"] == "REQ4293_WEP" for row in handoff)
            and any(row["selected_bound_or_input"] == "first_Dv_Gamma_eff_coefficient_row" for row in handoff)
            and any(row["selected_bound_or_input"] == "first_Dv_K_hat_coefficient_row" for row in handoff),
            "fallback handoff includes 4293 bounds and first Dv coefficient rows",
        ),
        (
            "VAL4297_7_control_cases",
            bool(controls) and all(row["expected_matches_actual"] == "True" for row in controls),
            "control cases distinguish factorized verticality from live obstruction",
        ),
        ("VAL4297_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4297_9_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4297_10_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-138 private nonclaim row",
        ),
        (
            "VAL4297_11_spine_packet",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
        ("VAL4297_12_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4297_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
    return [
        {
            **common(),
            "check_id": check_id,
            "description": description,
            "passed": str(passed),
            "evidence": "generated_artifacts",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for check_id, passed, description in validations
    ]


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    paths = {
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4297_SOURCE_REGISTER.csv",
        "dq_expansion": SOURCE_DIR / "P8_Y5_R2FR_4297_DQ_QTR_EXPANSION.csv",
        "verticality_clauses": SOURCE_DIR / "P8_Y5_R2FR_4297_VERTICALITY_CLAUSE_AUDIT.csv",
        "topological_rest": SOURCE_DIR / "P8_Y5_R2FR_4297_TOPOLOGICAL_REST_ATTEMPT.csv",
        "obstructions": SOURCE_DIR / "P8_Y5_R2FR_4297_OBSTRUCTION_COUNTERMODELS.csv",
        "fallback_handoff": SOURCE_DIR / "P8_Y5_R2FR_4297_FALLBACK_HANDOFF_ROWS.csv",
        "control_cases": SOURCE_DIR / "P8_Y5_R2FR_4297_CONTROL_CASES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4297_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4297_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4297_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4297_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["dq_expansion"], dq_expansion_rows())
    write_csv(paths["verticality_clauses"], verticality_clause_rows())
    write_csv(paths["topological_rest"], topological_rest_rows())
    write_csv(paths["obstructions"], obstruction_rows())
    write_csv(paths["fallback_handoff"], fallback_handoff_rows())
    write_csv(paths["control_cases"], control_case_rows())
    write_csv(paths["decision"], decision_rows())
    write_csv(paths["firewall"], firewall_rows())
    write_csv(paths["status"], status_rows())
    write_csv(paths["next_target"], next_target_rows())
    write_text(FORMAL_PATH, formal_doc())
    write_text(DOC_PATH, checkpoint_doc())
    append_claim()
    append_unique_block(
        FORMAL / "07-unification-spine.md",
        MARKER,
        "PPC4161 4297 q_tr vertical/topological-rest proof attempt",
        (
            "4297 derives the exact `D_v q_tr` expansion and shows raw transition verticality is not automatic. "
            "`D_v Gamma_eff`, `D_v K_hat`, connection commutator, and boundary/topological support must be parent-signed. "
            "A hidden-scalar Gamma countermodel is retained, so the next target is factorization or first D_v coefficient rows."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4297 packet q_tr vertical/topological-rest attempt",
        (
            "Packet update: quotient silence is not allowed to touch raw `q_tr` until `Gamma_eff` and `K_hat` factor through "
            "`q` or `q_tr` is proven topological/superpotential rest. Otherwise first `D_v` bound rows are required."
        ),
    )
    write_csv(paths["validation"], validation_rows(paths))
    failed = [row for row in csv_rows(paths["validation"]) if row["passed"] != "True"]
    print(f"{CHECKPOINT}: wrote {len(paths) - 1} csv artifacts plus validation")
    print(f"{CHECKPOINT}: validation rows={len(csv_rows(paths['validation']))} failed={len(failed)}")
    print(f"{CHECKPOINT}: decision={DECISION}")
    if failed:
        for row in failed:
            print(f"FAILED {row['check_id']}: {row['description']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
