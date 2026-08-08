from __future__ import annotations

import csv
import io
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4298"
CLAIM_ID = "L-139"
BRANCH = "MTS_R2FR_Y5_GAMMA_KHAT_HIDDEN_DEPENDENCE_FACTORISATION_OR_FIRST_DV_QTR_BOUND_ROW_4298"
DECISION = "GAMMA_KHAT_Q_FACTORISATION_NOT_PARENT_SIGNED_FIRST_DV_BOUND_MATRIX_BUILT_NONCLAIM"
MARKER = "PPC4161_GAMMA_KHAT_HIDDEN_DEPENDENCE_FACTORISATION_4298"
PACKET_MARKER = "PPC4161_PACKET_GAMMA_KHAT_HIDDEN_DEPENDENCE_FACTORISATION_4298"
NEXT_TARGET = "4299-Y5-R2FR-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md"

FORMAL_PATH = FORMAL / "314-PPC4161-Gamma-Khat-hidden-dependence-factorization-or-first-Dv-qtr-bound-row.md"
DOC_PATH = POST / "4298-Y5-R2FR-Gamma-Khat-hidden-dependence-factorization-or-first-Dv-qtr-bound-row.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4298_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4298_00_4297_formal": (
        FORMAL / "313-PPC4161-qtr-vertical-or-topological-rest-proof-attempt-for-PnonHilbert.md",
        "D_v Gamma_eff = 0,",
        "4297 handoff: factor Gamma_eff and K_hat or fill D_v coefficient rows.",
    ),
    "SRC4298_01_4297_expansion": (
        SOURCE_DIR / "P8_Y5_R2FR_4297_DQ_QTR_EXPANSION.csv",
        "D_v Gamma_eff",
        "4297 machine D_v q_tr expansion.",
    ),
    "SRC4298_02_4297_handoff": (
        SOURCE_DIR / "P8_Y5_R2FR_4297_FALLBACK_HANDOFF_ROWS.csv",
        "first_Dv_Gamma_eff_coefficient_row",
        "4297 selected first D_v coefficient rows.",
    ),
    "SRC4298_03_parent_v1": (
        FORMAL / "83-parent-equations-v1.md",
        "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}.",
        "Parent v1 defines Gamma_eff/K_hat/q current relation.",
    ),
    "SRC4298_04_parent_v0": (
        FORMAL / "36-minimal-parent-equations-v0.md",
        "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
        "Minimal parent v0 gives the same decomposition.",
    ),
    "SRC4298_05_Lcg_trace": (
        FORMAL / "90-Lcg-gradient-trace-bound.md",
        "Gamma_eff = L_cg^-2 F_L",
        "Trace-gradient gate shows local Gamma gradients are dangerous if not suppressed/factored.",
    ),
    "SRC4298_06_1010_GK": (
        POST / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "q_loc is retained as an explicit residual",
        "Gamma/Khat action-existence route is precise but not closed.",
    ),
    "SRC4298_07_1366_Gamma_shape": (
        POST / "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope.md",
        "Gamma_eff=L_cg^-2 F(m)",
        "Gamma_eff has a formula-shape seed, not a claim-grade q-basic density.",
    ),
    "SRC4298_08_3520_QAP": (
        POST / "3520-Y5-R2FR-quotient-action-principle-derives-q-normal-form-or-finite-source-bounds.md",
        "QAP_derives_3519_normal_form",
        "Quotient action principle would forbid nonbasic hidden dependence, but parent gates remain unsigned.",
    ),
    "SRC4298_09_297_cGamma": (
        FORMAL / "297-PPC4161-cGamma-transport-Bgrad-routing-zero-or-profile-source-pack.md",
        "R_transport_to_local",
        "Transition profile terms remain live if factorization fails.",
    ),
    "SRC4298_10_303_AJ": (
        FORMAL / "303-PPC4161-cGamma-AJ-real-profile-or-parent-coefficient-derivation.md",
        "PARENT_ZERO_NOT_DERIVED",
        "cGamma/AJ parent zero is not derived; explicit profile law retained.",
    ),
    "SRC4298_11_4293_req": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv",
        "REQ4293_WEP",
        "Local suppression thresholds to use when D_v terms survive.",
    ),
}

TERMS = [
    ("T4298_DVGAMMA", "D_v Gamma_eff", "nabla^nu(D_v Gamma_eff)", "trace/metric-proportional hidden dependence"),
    ("T4298_DVKHAT", "D_v K_hat", "-nabla_mu(D_v K_hat^{mu nu})", "trace-free/anisotropic hidden dependence"),
    ("T4298_CONN", "C_conn", "C_conn^nu[v;Gamma_eff,K_hat,g_obs]", "hidden metric/connection derivative channel"),
    ("T4298_BOUNDARY", "B_boundary", "boundary/topological pullback term", "boundary/superpotential support channel"),
]


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


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


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
                "4298 attempts to factor Gamma_eff and K_hat through q after the 4297 D_v q_tr expansion. The current "
                "corpus defines Gamma_eff and K_hat, and Gamma_eff has a nonclaim formula-shape seed Gamma_eff=L_cg^-2F(m), "
                "but it does not parent-sign that Gamma_eff, K_hat, the connection, and boundary support are q-basic for "
                "raw transition q_tr. Therefore D_v Gamma_eff, D_v K_hat, C_conn, and boundary terms remain live. 4298 "
                "builds the first D_v coefficient bound matrix against the 4293 WEP/PPN/clock/orbit/Gdot/R10 thresholds."
            ),
            (
                "4298 source register, factorization audit, D_v term split, D_v coefficient bound matrix, obstruction "
                "ledger, decision, firewall, status and validation CSV."
            ),
            "private_gamma_khat_factorization_not_parent_signed_first_dv_bound_matrix_nonclaim",
            (
                "Acquire a parent QAP/q-basic signature for Gamma_eff and K_hat, or source first D_v Gamma_eff / D_v K_hat "
                "coefficients small enough for the 4293 local suppression thresholds."
            ),
            (
                "Calling formula-shape Gamma_eff evidence q-basic proof, treating K_hat bookkeeping as metric-response "
                "factorization, or claiming local-GR/WEP/R10/PPN pass."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def req_rows() -> List[Dict[str, str]]:
    return csv_rows(SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv")


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


def factorization_audit_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "FA4298_0_Gamma_definition",
            "Gamma_eff",
            "Gamma_eff=-1/4 K_MTS or Gamma_eff=L_cg^-2 F(m) in local formula-shape branch",
            "DEFINED_NOT_Q_FACTORED",
            "Definition/formula-shape does not prove Gamma_eff(Phi)=Gamma_bar(q(Phi)).",
        ),
        (
            "FA4298_1_Gamma_q_basic",
            "D_v Gamma_eff=0",
            "requires Gamma_eff=Gamma_bar(q) or QAP/nonbasic-operator ban",
            "NOT_PARENT_SIGNED",
            "1366 says q-basic scalar-density action is not claim-grade; 3520 QAP remains conditional.",
        ),
        (
            "FA4298_2_Khat_definition",
            "K_hat",
            "trace-free residual in K_MTS=-Gamma_eff g + K_hat",
            "DEFINED_NOT_Q_FACTORED",
            "Trace-free bookkeeping does not prove K_hat=Kbar(q,g_obs).",
        ),
        (
            "FA4298_3_Khat_metric_response",
            "D_v K_hat=0",
            "requires K_hat=K_metric[Gamma_eff] or Khat=Kbar(q,g_obs)",
            "NOT_PARENT_SIGNED",
            "1010 retains Delta_K=K_hat-K_metric[Gamma_eff] and Helmholtz/action gaps.",
        ),
        (
            "FA4298_4_connection",
            "C_conn=0",
            "requires g_obs/coframe/connection factor through q before variation",
            "CONDITIONAL_SELECTOR_ONLY",
            "Ordinary local selector supports same observed metric; raw transition interface is not parent-signed.",
        ),
        (
            "FA4298_5_boundary",
            "B_boundary=0",
            "requires fixed/routed q-basic boundary/topological support",
            "NOT_PARENT_SIGNED",
            "Boundary/superpotential route is still open, not derived for raw q_tr.",
        ),
        (
            "FA4298_6_verdict",
            "D_v q_tr=0",
            "D_v Gamma_eff=0, D_v K_hat=0, C_conn=0, B_boundary=0",
            "NOT_PROVED",
            "At least Gamma_eff q-basicness and K_hat q-basic/metric-response ownership remain unsigned.",
        ),
    ]
    return [
        {
            **common(),
            "audit_id": audit_id,
            "object": obj,
            "needed_statement": statement,
            "status": status,
            "evidence_or_obstruction": evidence,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for audit_id, obj, statement, status, evidence in raw
    ]


def dv_term_split_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for term_id, term, formula, meaning in TERMS:
        rows.append(
            {
                **common(),
                "term_id": term_id,
                "term": term,
                "appears_in": "D_v q_tr^nu = nabla^nu(D_v Gamma_eff) - nabla_mu(D_v K_hat^{mu nu}) + C_conn^nu + B_boundary^nu",
                "formula_piece": formula,
                "meaning": meaning,
                "zero_status": "NOT_PARENT_SIGNED",
                "first_bound_row_status": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def coefficient_bound_matrix_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    requirements = [row for row in req_rows() if row.get("requirement_id", "").startswith("REQ4293_")]
    for term_id, term, formula, meaning in TERMS:
        for req in requirements:
            req_id = req.get("requirement_id", "")
            req_value = req.get("required_value", "MISSING")
            req_numeric = to_float(req_value)
            rows.append(
                {
                    **common(),
                    "matrix_id": f"CB4298_{len(rows):03d}",
                    "term_id": term_id,
                    "term": term,
                    "arena_requirement": req_id,
                    "required_value": req_value,
                    "units": req.get("units", "MISSING_UNITS"),
                    "term_formula_piece": formula,
                    "coefficient_symbol": f"Y_{term_id}_{req_id}",
                    "coefficient_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                    "coefficient_required_abs_max": req_value,
                    "required_value_positive": str(math.isfinite(req_numeric) and req_numeric > 0),
                    "comparison_status": "NOT_RUN_MISSING_COEFFICIENT",
                    "interpretation": f"{meaning}; coefficient must be <= arena threshold if zero theorem fails.",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
    return rows


def obstruction_rows() -> List[Dict[str, str]]:
    raw = [
        (
            "OB4298_0_formula_shape_not_basic",
            "Gamma_eff=L_cg^-2F(m) can still depend on hidden m,L_cg profiles",
            "D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg",
            "q-basicness requires D_v m=0 and D_v L_cg=0 or a parent QAP ban.",
        ),
        (
            "OB4298_1_Khat_metric_gap",
            "K_hat trace-free residual need not be metric response of Gamma_eff",
            "Delta_K := K_hat-K_metric[Gamma_eff] remains live",
            "D_v K_hat cannot be set to zero from trace decomposition alone.",
        ),
        (
            "OB4298_2_QAP_unsigned",
            "QAP would ban nonbasic hidden dependence",
            "QAP_derives_normal_form is conditional but parent gates fail",
            "Factorization route is real but not current proof.",
        ),
        (
            "OB4298_3_AJ_profile_live",
            "transition shell has live transport/B-gradient/cGamma profile terms",
            "R_transport_to_local and R_Bgrad_to_local remain profile/source obligations",
            "Even q-basic trace language does not erase transition support without profile/kernel proof.",
        ),
    ]
    return [
        {
            **common(),
            "obstruction_id": obs_id,
            "obstruction": obstruction,
            "formula_or_effect": effect,
            "meaning": meaning,
            "retained": "True",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for obs_id, obstruction, effect, meaning in raw
    ]


def control_case_rows() -> List[Dict[str, str]]:
    cases = [
        ("CTRL4298_full_factorization", True, True, True, True, True, "PASS_DV_QTR_ZERO"),
        ("CTRL4298_gamma_hidden", False, True, True, True, False, "FAIL_DV_GAMMA_BOUND_REQUIRED"),
        ("CTRL4298_khat_hidden", True, False, True, True, False, "FAIL_DV_KHAT_BOUND_REQUIRED"),
        ("CTRL4298_conn_hidden", True, True, False, True, False, "FAIL_CONN_BOUND_REQUIRED"),
        ("CTRL4298_boundary_live", True, True, True, False, False, "FAIL_BOUNDARY_BOUND_REQUIRED"),
        ("CTRL4298_all_missing", False, False, False, False, False, "FAIL_DV_GAMMA_BOUND_REQUIRED"),
    ]
    rows: List[Dict[str, str]] = []
    for case_id, gamma_ok, khat_ok, conn_ok, boundary_ok, expected_pass, expected_outcome in cases:
        actual_pass = gamma_ok and khat_ok and conn_ok and boundary_ok
        if actual_pass:
            actual_outcome = "PASS_DV_QTR_ZERO"
        elif not gamma_ok:
            actual_outcome = "FAIL_DV_GAMMA_BOUND_REQUIRED"
        elif not khat_ok:
            actual_outcome = "FAIL_DV_KHAT_BOUND_REQUIRED"
        elif not conn_ok:
            actual_outcome = "FAIL_CONN_BOUND_REQUIRED"
        else:
            actual_outcome = "FAIL_BOUNDARY_BOUND_REQUIRED"
        rows.append(
            {
                **common(),
                "control_id": case_id,
                "Gamma_eff_q_basic": str(gamma_ok),
                "K_hat_q_basic_or_metric_response": str(khat_ok),
                "connection_q_basic": str(conn_ok),
                "boundary_fixed_or_routed": str(boundary_ok),
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
            "decision_id": "D4298_0",
            "decision": DECISION,
            "what_moved": "Gamma/Khat factorization is now a concrete q-basicness and metric-response problem, with a first D_v coefficient matrix if the theorem route fails.",
            "best_next": "Try QAP/parent q-basic signature for Gamma_eff and K_hat, or source coefficients for D_v Gamma_eff and D_v K_hat against the 4293 thresholds.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def firewall_rows() -> List[Dict[str, str]]:
    raw = [
        ("FW4298_0_no_formula_shape_claim", "Gamma_eff=L_cg^-2F(m) is not q-basic proof unless m and L_cg factor through q."),
        ("FW4298_1_no_trace_decomp_claim", "K_hat being trace-free is not metric-response/factorization proof."),
        ("FW4298_2_no_QAP_overpromotion", "QAP normal-form derivation is conditional until parent equivalence/qmap/action gates are signed."),
        ("FW4298_3_bound_matrix_nonclaim", "Coefficient matrix rows are obligations, not pass evidence."),
        ("FW4298_4_nonclaim", "No local-GR/WEP/R10/PPN/clock/orbital claim is allowed from 4298."),
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
            "status_id": "STATUS4298_0",
            "Gamma_eff_q_factorization_parent_signed": "False",
            "K_hat_q_factorization_parent_signed": "False",
            "connection_commutator_zero_parent_signed": "False",
            "boundary_support_parent_signed": "False",
            "coefficient_bound_matrix_rows": str(len(coefficient_bound_matrix_rows())),
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "target_id": "NEXT4298_0",
            "next_target": NEXT_TARGET,
            "objective": "Either parent-sign QAP/q-basicness for Gamma_eff and K_hat, or source first D_v Gamma_eff/D_v K_hat coefficients against the 4293 local thresholds.",
            "fallback": "If no source coefficient exists, keep P_nonHilbert q_tr as an explicit nonclaim residual feeding WEP/PPN/clock/orbit/Gdot/R10 rows.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def formal_doc() -> str:
    reqs = {row.get("requirement_id", ""): row.get("required_value", "") for row in req_rows()}
    return f"""
# 314 Gamma/Khat hidden-dependence factorization or first D_v q_tr bound row

Marker: `{MARKER}`

Branch: `{BRANCH}`

Decision: `{DECISION}`

## Target

4297 reduced raw transition verticality to:

```text
D_v q_tr^nu =
  nabla^nu(D_v Gamma_eff)
- nabla_mu(D_v K_hat^(mu nu))
+ C_conn^nu
+ B_boundary^nu.
```

4298 asks whether the first two pieces factor through the quotient:

```text
Gamma_eff(Phi) = Gamma_bar(q(Phi)),
K_hat(Phi,g_obs) = Kbar(q(Phi),g_obs).
```

## Result

Current corpus:

```text
Gamma_eff is defined,
K_hat is defined,
Gamma_eff has formula-shape seed Gamma_eff=L_cg^-2 F(m),
QAP would forbid nonbasic hidden dependence if parent-signed,
but Gamma_eff/K_hat q-factorization is not parent-signed.
```

So:

```text
D_v Gamma_eff = 0        not proved,
D_v K_hat = 0            not proved,
C_conn = 0               not proved for raw transition interface,
B_boundary = 0           not proved for raw transition interface.
```

## Why formula-shape is not enough

If:

```text
Gamma_eff = L_cg^-2 F(m),
```

then:

```text
D_v Gamma_eff
= L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg.
```

So a q-basic theorem needs:

```text
D_v m = 0,
D_v L_cg = 0,
```

or a parent quotient-action/operator-domain ban on nonbasic hidden dependence.

## First D_v coefficient matrix

If the zero theorem fails, each term must satisfy arena thresholds. The harshest current row remains:

```text
Y_WEP <= {reqs.get('REQ4293_WEP', 'MISSING')}
```

and the local PPN/clock/orbit rows remain:

```text
Y_gamma <= {reqs.get('REQ4293_GAMMA', 'MISSING')}
Y_beta  <= {reqs.get('REQ4293_BETA', 'MISSING')}
Y_clock <= {reqs.get('REQ4293_CLOCK', 'MISSING')}
Y_orbit <= {reqs.get('REQ4293_ORBIT', 'MISSING')}
```

4298 creates missing coefficient rows for:

```text
D_v Gamma_eff,
D_v K_hat,
C_conn,
B_boundary.
```

## Status

Private nonclaim. The next target is `{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4298 Y5 R2FR Gamma/Khat factorization or first D_v q_tr bound row

## Purpose

Try to prove `Gamma_eff` and `K_hat` factor through `q`, so raw transition `D_v q_tr` vanishes. If not, generate first D_v coefficient bound rows.

## Outcome

Factorization is not parent-signed. `Gamma_eff` has a formula-shape seed, but q-basicness would also require `D_v m=0`, `D_v L_cg=0`, or a parent QAP/operator-domain theorem. `K_hat` remains a trace-free/metric-response gap, not a q-factored object.

## Next

Parent-sign QAP/q-basicness for `Gamma_eff` and `K_hat`, or source first D_v coefficients.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    audit = csv_rows(paths["factorization_audit"])
    terms = csv_rows(paths["dv_term_split"])
    matrix = csv_rows(paths["coefficient_bound_matrix"])
    controls = csv_rows(paths["control_cases"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4298_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited local sources exist"),
        ("VAL4298_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4298_2_factorization_not_proved",
            any(row["audit_id"] == "FA4298_6_verdict" and row["status"] == "NOT_PROVED" for row in audit)
            and any(row["audit_id"] == "FA4298_1_Gamma_q_basic" and row["status"] == "NOT_PARENT_SIGNED" for row in audit)
            and any(row["audit_id"] == "FA4298_3_Khat_metric_response" and row["status"] == "NOT_PARENT_SIGNED" for row in audit),
            "Gamma/Khat factorization verdict is not proved",
        ),
        (
            "VAL4298_3_dv_terms_complete",
            {row["term"] for row in terms} == {"D_v Gamma_eff", "D_v K_hat", "C_conn", "B_boundary"},
            "D_v term split has all four terms",
        ),
        (
            "VAL4298_4_matrix_complete",
            bool(matrix)
            and any(row["term"] == "D_v Gamma_eff" and row["arena_requirement"] == "REQ4293_WEP" for row in matrix)
            and any(row["term"] == "D_v K_hat" and row["arena_requirement"] == "REQ4293_GAMMA" for row in matrix)
            and all(row["comparison_status"] == "NOT_RUN_MISSING_COEFFICIENT" for row in matrix),
            "coefficient matrix includes DvGamma/DvKhat local thresholds and remains nonclaim",
        ),
        (
            "VAL4298_5_required_values_positive",
            bool(matrix) and all(row["required_value_positive"] == "True" for row in matrix),
            "all imported threshold values are positive numeric",
        ),
        (
            "VAL4298_6_control_cases",
            bool(controls) and all(row["expected_matches_actual"] == "True" for row in controls),
            "control cases distinguish factorization zero from coefficient obligations",
        ),
        ("VAL4298_7_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4298_8_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4298_9_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-139 private nonclaim row",
        ),
        (
            "VAL4298_10_spine_packet",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
        ("VAL4298_11_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4298_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4298_SOURCE_REGISTER.csv",
        "factorization_audit": SOURCE_DIR / "P8_Y5_R2FR_4298_FACTORISATION_AUDIT.csv",
        "dv_term_split": SOURCE_DIR / "P8_Y5_R2FR_4298_DV_TERM_SPLIT.csv",
        "coefficient_bound_matrix": SOURCE_DIR / "P8_Y5_R2FR_4298_DV_COEFFICIENT_BOUND_MATRIX.csv",
        "obstructions": SOURCE_DIR / "P8_Y5_R2FR_4298_OBSTRUCTION_LEDGER.csv",
        "control_cases": SOURCE_DIR / "P8_Y5_R2FR_4298_CONTROL_CASES.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4298_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4298_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4298_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4298_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["factorization_audit"], factorization_audit_rows())
    write_csv(paths["dv_term_split"], dv_term_split_rows())
    write_csv(paths["coefficient_bound_matrix"], coefficient_bound_matrix_rows())
    write_csv(paths["obstructions"], obstruction_rows())
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
        "PPC4161 4298 Gamma/Khat hidden-dependence factorization",
        (
            "4298 shows Gamma_eff/K_hat factorization through `q` is not parent-signed. `Gamma_eff=L_cg^-2F(m)` is only "
            "formula-shape unless `m` and `L_cg` are q-basic; `K_hat` still has metric-response/Helmholtz gaps. The first "
            "`D_v Gamma_eff`, `D_v K_hat`, connection, and boundary coefficient matrix is now built against 4293 thresholds."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4298 packet Gamma/Khat factorization gate",
        (
            "Packet update: raw `q_tr` silence now reduces to q-basic Gamma/Khat plus connection/boundary clauses. If QAP or "
            "factorization is not parent-signed, the new D_v coefficient matrix is the empirical fallback."
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
