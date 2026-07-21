from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4738"
CLAIM_ID = "L-580"
MARKER = "PPC4161_TRACEFREE_KHAT_RIGHT_INVERSE_PARENT_ACTION_OR_CONSERVATION_QUARANTINE_EQUATIONS_4738"
PACKET_MARKER = "PPC4161_PACKET_TRACEFREE_KHAT_RIGHT_INVERSE_PARENT_ACTION_OR_CONSERVATION_QUARANTINE_EQUATIONS_4738"
DECISION = "TRACEFREE_RI_PARENT_ACTION_UNSIGNED_QUARANTINE_EQUATIONS_CONTRACT_STAGED_NONCLAIM"
NEXT_TARGET = "4739-Y5-R2FR-CdeltaKdiv-profile-row-and-RI-commutator-zero-or-quarantine-owner-proof.md"

DOC_PATH = POST / "4738-Y5-R2FR-tracefree-Khat-right-inverse-parent-action-or-conservation-quarantine-equations.md"
FORMAL_PATH = FORMAL / "754-PPC4161-tracefree-Khat-right-inverse-parent-action-or-conservation-quarantine-equations.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_SOURCE_REGISTER.csv"
TRACEFREE_DERIVATION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_TRACEFREE_RIGHT_INVERSE_DERIVATION.csv"
PARENT_CONTRACT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_PARENT_ACTION_OWNER_CONTRACT.csv"
QUARANTINE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_CONSERVATION_QUARANTINE_EQUATIONS.csv"
FINITE_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_FINITE_RESIDUAL_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_ROUTE_SELECTION_MATRIX.csv"
GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4738_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4738_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4738_0_4737_next", SOURCE_DIR / "P8_Y5_R2FR_4737_NEXT_TARGET.csv", "trace-free R_T with div R_T=grad Gamma_eff", "4737 handoff"),
    ("SRC4738_1_4737_contract", SOURCE_DIR / "P8_Y5_R2FR_4737_TRACEFREE_RIGHT_INVERSE_CONTRACT.csv", "RINV4737_1_divergence_identity", "trace-free right-inverse contract"),
    ("SRC4738_2_4737_doc", POST / "4737-Y5-R2FR-transition-shell-current-solver-or-Khat-cancellation-identity.md", "trace-free right-inverse R_T", "4737 summary"),
    ("SRC4738_3_357_prior", FORMAL / "357-PPC4161-Khat-right-inverse-parent-signature-or-DeltaK-divergence-bound.md", "K_hat = K_Gamma[Gamma_eff] + Delta_K", "prior Khat right-inverse branch"),
    ("SRC4738_4_357_bound", FORMAL / "357-PPC4161-Khat-right-inverse-parent-signature-or-DeltaK-divergence-bound.md", "C_DeltaK_div :=", "DeltaK divergence bound contract"),
    ("SRC4738_5_4341_contract", SOURCE_DIR / "P8_Y5_R2FR_4341_PARENT_SIGNATURE_CONTRACT.csv", "KRI4341_0_parent_owner", "parent-owner clauses"),
    ("SRC4738_6_4341_bounds", SOURCE_DIR / "P8_Y5_R2FR_4341_BOUND_ROWS.csv", "BND4341_2_CDeltaKdiv", "finite residual rows"),
    ("SRC4738_7_eq_register", FORMAL / "05-equation-register.md", "q^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}.", "core q-current equation"),
    ("SRC4738_8_eq_tracefree", FORMAL / "05-equation-register.md", "g_mu_nu K_hat^{mu nu} = 0", "Khat trace-free constraint"),
    ("SRC4738_9_134_quarantine", FORMAL / "134-conservation-owned-quarantine-equations.md", "q_tr^nu + nabla_mu K_own^{mu nu} = 0.", "conservation-owned quarantine equations"),
    ("SRC4738_10_134_not_parent", FORMAL / "134-conservation-owned-quarantine-equations.md", "but it is not yet a parent-theory result.", "quarantine nonclaim status"),
    ("SRC4738_11_135_kernel", FORMAL / "135-quarantine-projector-parent-origin.md", "R_loc^nu_alpha q_tr^alpha = 0.", "metric response kernel route"),
    ("SRC4738_12_135_not_derived", FORMAL / "135-quarantine-projector-parent-origin.md", "But current parent v1 does not contain this action block.", "kernel parent blocker"),
    ("SRC4738_13_133_tracefree", FORMAL / "133-exact-transition-cancellation-or-projector-theorem.md", "Its divergence is not fixed by the trace split alone.", "tracefree not divergence control"),
    ("SRC4738_14_298_shortcut", FORMAL / "298-PPC4161-transition-shell-cancellation-projector-theorem-or-profile-source-rows.md", "because that is a boundary-dependent compensator, not a parent identity.", "unowned inverse rejection"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    TRACEFREE_DERIVATION_CSV,
    PARENT_CONTRACT_CSV,
    QUARANTINE_CSV,
    FINITE_ROWS_CSV,
    ROUTE_MATRIX_CSV,
    GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def source_path(source_id: str) -> str:
    for row_id, path_object, _needle, _role in SOURCE_SPECS:
        if row_id == source_id:
            return str(path_object)
    raise KeyError(source_id)


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def tracefree_derivation_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "TFRI4738_0_target",
            "Find symmetric trace-free R_T^{mu nu}[Gamma_eff] such that nabla_mu R_T^{mu nu}=nabla^nu Gamma_eff.",
            "This is the non-cheating version of Khat cancellation from 4737.",
            "TARGET_FROM_4737",
            "SRC4738_1_4737_contract",
        ),
        (
            "TFRI4738_1_scalar_ansatz",
            "R_T^{mu nu}[phi]=nabla^mu nabla^nu phi-(1/4)g^{mu nu}Box phi in four dimensions.",
            "The trace vanishes identically, so this is the simplest legal trace-free candidate.",
            "DERIVED_TRACEFREE_SHAPE",
            "SRC4738_8_eq_tracefree",
        ),
        (
            "TFRI4738_2_divergence",
            "nabla_mu R_T^{mu nu}=(3/4)nabla^nu Box phi+R^nu_sigma nabla^sigma phi plus convention-sign curvature terms.",
            "Matching grad Gamma_eff requires a potential equation, not an algebraic substitution.",
            "DERIVED_DIVERGENCE_LAW",
            "SRC4738_13_133_tracefree",
        ),
        (
            "TFRI4738_3_flat_limit",
            "On a locally flat collar, Box phi=(4/3)Gamma_eff plus homogeneous/boundary data gives div R_T=grad Gamma_eff.",
            "The route can work formally in the weak collar only as a Green-function construction with fixed boundary data.",
            "FORMAL_LOCAL_LIMIT_ONLY",
            "SRC4738_14_298_shortcut",
        ),
        (
            "TFRI4738_4_curved_integrability",
            "Curved backgrounds require grad Gamma_eff-Ric(nabla phi) to be an exact gradient compatible with the chosen boundary/domain.",
            "Curvature terms create a curl/integrability and same-geometry condition that must be parent-owned.",
            "INTEGRABILITY_CONDITION_OPEN",
            "SRC4738_5_4341_contract",
        ),
        (
            "TFRI4738_5_nonlocal_status",
            "The construction uses inverse Box or a trace-free divergence right inverse, so it is closure unless the parent action supplies the operator, gauge, boundary and domain.",
            "This proves the route is mathematically sharp but not yet a parent theorem.",
            "PARENT_SIGNATURE_MISSING",
            "SRC4738_3_357_prior",
        ),
        (
            "TFRI4738_6_deltaK_remainder",
            "With K_hat=R_T[Gamma_eff]+Delta_K, q_tr^nu=-nabla_mu Delta_K^{mu nu}+C_TF_RI^nu+C_conn^nu+B_boundary^nu.",
            "Even a legal R_T leaves Delta_K and commutator/boundary rows to zero or bound.",
            "FINITE_REMAINDER_LAW",
            "SRC4738_4_357_bound",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "statement": statement,
            "meaning": meaning,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, statement, meaning, status, source_id in specs
    ]


def parent_contract_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "PACT4738_0_owner_field",
            "Parent action contains R_T or a potential/superpotential field with a multiplier enforcing trace-free divergence.",
            "delta S_parent/delta lambda_nu -> nabla_mu R_T^{mu nu}-nabla^nu Gamma_eff=0 and delta S_parent/delta eta -> g_mu_nu R_T^{mu nu}=0",
            "UNSIGNED",
            "Without this, R_T is the rejected Div^-1 shortcut.",
        ),
        (
            "PACT4738_1_same_geometry",
            "The covariant derivative, metric/coframe, support collar, and observable readout use the same parent geometry to required order.",
            "C_conn=0 or source-backed C_conn bound",
            "UNSIGNED",
            "A right inverse in one geometry can fail after local projection/readout.",
        ),
        (
            "PACT4738_2_boundary_domain",
            "Boundary, gauge and Green-function domain are selected before scoring and are not retuned per test.",
            "C_TF_RI=[D_v,nabla_mu R_T]Gamma_eff=0 or bounded",
            "UNSIGNED",
            "The inverse-operator route is nonlocal and boundary-sensitive.",
        ),
        (
            "PACT4738_3_metric_null_owner",
            "The owner/multiplier block has zero or bounded direct local metric response.",
            "Pi_metric delta S_RI/delta g_loc <= arena budget",
            "UNSIGNED",
            "Cancelling q_tr is not enough if the owner block sources PPN/R10/clocks elsewhere.",
        ),
        (
            "PACT4738_4_deltaK_kernel",
            "The leftover Delta_K lies in the projected divergence kernel or has finite source-backed arena bounds.",
            "P_loc nabla_mu Delta_K^{mu nu}=0 or C_DeltaK_div sourced",
            "UNSIGNED",
            "The observable channel sees divergence, not trace alone.",
        ),
        (
            "PACT4738_5_ordinary_matter_GR",
            "The same kernel/quarantine theorem must not switch off ordinary matter gravity.",
            "R_loc T_matter != 0 and reduces to GR/Newton while R_loc q_tr=0",
            "UNSIGNED",
            "A projector that kills all local response would also kill the required GR limit.",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "contract_id": contract_id,
            "required_clause": required_clause,
            "mathematical_form": mathematical_form,
            "current_status": current_status,
            "why_it_matters": why_it_matters,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for contract_id, required_clause, mathematical_form, current_status, why_it_matters in specs
    ]


def quarantine_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QUAR4738_0_current_definition",
            "q_tr^nu := nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}",
            "transition current remains visible",
            "DEFINED",
            "SRC4738_9_134_quarantine",
        ),
        (
            "QUAR4738_1_decomposition",
            "q_tr^nu=q_Q^nu+q_gal^nu+q_cos^nu+q_owner^nu+q_metric,loc^nu",
            "no deletion; every piece is accounted for",
            "EQUATION_STAGED",
            "SRC4738_9_134_quarantine",
        ),
        (
            "QUAR4738_2_owner_balance",
            "nabla_mu K_A^{mu nu}=-q_A^nu and q_tr^nu+nabla_mu K_own^{mu nu}=0",
            "conservation-owned current accounting",
            "EQUATION_STAGED",
            "SRC4738_9_134_quarantine",
        ),
        (
            "QUAR4738_3_metric_kernel",
            "R_loc^nu_alpha q_tr^alpha=0, equivalently P_metric,loc q_tr=0",
            "clean non-cheating local metric quarantine theorem shape",
            "THEOREM_SHAPE_ONLY",
            "SRC4738_11_135_kernel",
        ),
        (
            "QUAR4738_4_ppn_small_fallback",
            "||R_loc q_tr||/a_ref <= 4.212667126774669e-17 if exact kernel fails",
            "severe finite fallback; must be source-backed before claim",
            "BOUND_REQUIRED",
            "SRC4738_10_134_not_parent",
        ),
        (
            "QUAR4738_5_nonclaim",
            "Parent projector origin and owner dynamics are not derived in current parent v1.",
            "quarantine is contract, not local-GR proof",
            "NONCLAIM",
            "SRC4738_12_135_not_derived",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "equation_id": equation_id,
            "equation": equation,
            "role": role,
            "status": status,
            "source_id": source_id,
            "source_path": source_path(source_id),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for equation_id, equation, role, status, source_id in specs
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FIN4738_0_qtr_reduction",
            "q_tr^nu",
            "q_tr^nu=-nabla_mu Delta_K^{mu nu}+C_TF_RI^nu+C_conn^nu+B_boundary^nu+Q_quarantine_leak^nu",
            "Delta_K profile; trace-free right-inverse commutator; same-geometry connection; boundary/domain; quarantine leakage",
            "DERIVED_FORMULA_INPUTS_OPEN",
        ),
        (
            "FIN4738_1_CDeltaKdiv",
            "C_DeltaK_div",
            "C_DeltaK_div=||P_loc nabla_mu D_v Delta_K^{mu nu}||_obs/a_ref",
            "local profile and arena projection norm",
            "FIRST_PROFILE_ROW_TO_FILL_OR_ZERO",
        ),
        (
            "FIN4738_2_CTFRI",
            "C_TF_RI",
            "C_TF_RI=||P_loc[D_v,nabla_mu R_T]Gamma_eff||_obs/a_ref",
            "right-inverse operator, Green data, boundary/domain variation",
            "COMMUTATOR_ZERO_OR_BOUND_REQUIRED",
        ),
        (
            "FIN4738_3_Ckernel",
            "C_kernel",
            "C_kernel=||R_loc q_tr||_obs/a_ref",
            "metric response operator and proof q_tr in Ker(R_loc)",
            "KERNEL_THEOREM_OR_BOUND_REQUIRED",
        ),
        (
            "FIN4738_4_arena_vector",
            "Y_a^transition",
            "Y_a <= Pi_Delta C_DeltaK_div + Pi_RI C_TF_RI + Pi_conn C_conn + Pi_bdry C_boundary + Pi_kernel C_kernel",
            "PPN, R10, clocks, orbital and WEP arena projection constants",
            "SOURCE_BACKED_PROJECTIONS_OPEN",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": row_id,
            "quantity": quantity,
            "formula": formula,
            "required_inputs": required_inputs,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, quantity, formula, required_inputs, status in specs
    ]


def route_matrix_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "ROUTE4738_0_parent_tracefree_RI",
            "parent_tracefree_right_inverse",
            "best_exact_route_but_unsigned",
            "Use scalar/York/superpotential trace-free right inverse only if parent action owns operator, boundary, gauge and metric-null stress.",
            "try next only if a real parent action block can be written",
        ),
        (
            "ROUTE4738_1_conservation_quarantine",
            "conservation_owned_quarantine",
            "clean_contract_but_not_theorem",
            "Keep q_tr conserved and owned while proving R_loc q_tr=0 or source-bounding leakage.",
            "continue as fallback and finite-row route",
        ),
        (
            "ROUTE4738_2_direct_shell_bound",
            "direct_transition_shell_bound",
            "severe_not_preferred",
            "Without identity/kernel, the shell needs about 4.2e-17 suppression before it can score as local safe.",
            "not viable without sourced cancellation or response-kernel proof",
        ),
        (
            "ROUTE4738_3_fake_metric_Khat",
            "Khat_equals_Gamma_g",
            "rejected_firewall",
            "Violates trace-free Khat and reopens the 4737 anti-cheat gate.",
            "never use",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "status": status,
            "detail": detail,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, status, detail, next_action in specs
    ]


def gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4738_0_tracefree_shape", "Trace-free Hessian/York shape is derived but not parent-promoted.", "closed_derived_nonclaim", False),
        ("GATE4738_1_parent_action_owner", "Promote only if parent action owns R_T operator, gauge, boundary, domain and metric-null stress.", "closed_unsigned", False),
        ("GATE4738_2_deltaK_commutator", "Promote only if Delta_K divergence and R_T commutator vanish or are source-backed finite rows.", "closed_inputs_open", False),
        ("GATE4738_3_quarantine_kernel", "Promote quarantine only if R_loc is derived and q_tr is in Ker(R_loc) while matter still gives GR/Newton.", "closed_unsigned", False),
        ("GATE4738_4_no_direct_claim", "No local-GR, PPN, R10, clock, orbital, Newtonian or public claim from 4738.", "closed_firewall", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "status": status,
            "valid_for_claim": valid_for_claim,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, status, valid_for_claim in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4738_0_no_unowned_inverse", "Do not use inverse Box, Div^-1, York decomposition or Green data unless the parent action owns them before scoring."),
        ("FW4738_1_no_trace_only_pass", "Trace-free Khat or trace-free R_T does not by itself control divergence or local metric response."),
        ("FW4738_2_no_metric_killing", "A response kernel may not kill ordinary matter gravity; it must preserve the GR/Newton channel."),
        ("FW4738_3_no_quarantine_claim", "Conservation-owned quarantine is an explicit contract until projector origin and owner dynamics are parent-derived."),
        ("FW4738_4_no_GitHub_action", "No GitHub action is performed by this checkpoint."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "summary": "4738 derives the legal trace-free right-inverse shape and its divergence law. It shows the route needs an inverse differential operator/boundary data, so it remains closure unless parent-owned. Conservation-owned quarantine equations are staged with an explicit R_loc kernel theorem target.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4738_0_local_only",
            "status": "local_only_private_checkpoint",
            "detail": "Generated local post-checkpoint and formalization files only.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4738_1_science_verdict",
            "status": "derivation_progress_parent_signature_missing",
            "detail": "Trace-free right-inverse mechanism is mathematically sharpened, but parent action ownership, Delta_K divergence, RI commutators and R_loc kernel proof remain open.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "4738 proved the right-inverse route is a real inverse-operator/superpotential problem, not an algebraic Khat trick.",
            "preferred_route": "Try to prove C_DeltaK_div=0 and C_TF_RI=0 from parent-owned Delta_K/kernel structure, while preserving matter GR/Newton response.",
            "fallback_route": "Build source-backed finite rows for C_DeltaK_div, C_TF_RI, C_conn, C_boundary and C_kernel across PPN/R10/clocks/orbital/WEP.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def bullets(rows: list[dict[str, Any]], id_key: str, text_key: str) -> str:
    return "\n".join(f"- `{row[id_key]}`: {row[text_key]}" for row in rows)


def write_docs(
    timestamp: str,
    derivation: list[dict[str, Any]],
    parent_contract: list[dict[str, Any]],
    quarantine: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4738 Y5 R2FR: Trace-Free Khat Right-Inverse Parent Action Or Conservation Quarantine Equations

Generated: `{timestamp}`

## Summary

- Work is local-only and private.
- The exact transition-current route has now been sharpened into a real trace-free right-inverse problem.
- A legal trace-free candidate exists in form, but it needs an inverse differential operator plus boundary/gauge/domain data.
- Therefore this checkpoint does **not** claim local GR: it stages the parent-action contract and the conservation-owned quarantine equations.

## Core Derivation

Use the four-dimensional trace-free Hessian candidate:

```text
R_T^{{mu nu}}[phi] = nabla^mu nabla^nu phi - (1/4) g^{{mu nu}} Box phi
g_mu_nu R_T^{{mu nu}} = 0
```

Its divergence is:

```text
nabla_mu R_T^{{mu nu}}
  = (3/4) nabla^nu Box phi + R^nu_sigma nabla^sigma phi
```

up to sign conventions for the curvature commutator. So matching:

```text
nabla_mu R_T^{{mu nu}} = nabla^nu Gamma_eff
```

requires a parent-owned potential/superpotential equation:

```text
(3/4) nabla^nu Box phi + R^nu_sigma nabla^sigma phi = nabla^nu Gamma_eff
```

In the local flat limit this reduces to `Box phi = (4/3) Gamma_eff + homogeneous data`, but that is a Green-function construction, not an algebraic identity.

## Trace-Free Right-Inverse Rows

{bullets(derivation, "row_id", "statement")}

## Parent Action Owner Contract

{bullets(parent_contract, "contract_id", "required_clause")}

## Conservation Quarantine Equations

{bullets(quarantine, "equation_id", "equation")}

## Finite Residual Rows

{bullets(finite, "row_id", "formula")}

## Route Matrix

{bullets(routes, "route_id", "route")}

## Promotion Gates

{bullets(gates, "gate_id", "gate")}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`

No GitHub action was performed.
"""
    write_text(DOC_PATH, doc)

    formal = f"""# 754 PPC4161: Trace-Free Khat Right-Inverse Parent Action Or Conservation Quarantine Equations

Generated: `{timestamp}`

## Current Status

`{DECISION}`

## What Was Actually Derived

The legal trace-free candidate is:

```text
R_T^{{mu nu}} = nabla^mu nabla^nu phi - (1/4)g^{{mu nu}}Box phi
```

and:

```text
nabla_mu R_T^{{mu nu}} = (3/4)nabla^nu Box phi + R^nu_sigma nabla^sigma phi.
```

So an exact cancellation of:

```text
q_tr^nu = nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}}
```

is possible only if the parent theory owns the potential/superpotential equation, its boundary data, and its local metric response.

## Why This Is Progress

This is no longer vague missingness. The local branch now has a precise theorem target:

```text
K_hat = R_T[Gamma_eff] + Delta_K
P_loc div Delta_K = 0 or finite
R_loc q_tr = 0 while ordinary matter still gives GR/Newton
```

## Nonclaim Boundary

No local-GR, PPN, R10, clock, orbital or Newtonian pass is claimed. The next checkpoint must either prove the Delta_K/right-inverse commutator/kernel zeros or build the finite residual rows.

## Next

`{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Result: the trace-free `K_hat` route is mathematically sharpened into `R_T[phi]=Hess(phi)-1/4 g Box phi`.
- Divergence law: `div R_T=(3/4)grad Box phi + Ric(nabla phi)`, so exact cancellation needs parent-owned inverse/operator and boundary data.
- Quarantine route: `R_loc q_tr=0` is the clean local metric kernel theorem, but it remains unsigned.
- Next local route: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet update: transition-shell local safety is now reduced to parent trace-free right-inverse ownership or explicit response-kernel quarantine.
- Claim status: nonclaim; no local-GR/PPN/R10/Newtonian pass.
""",
    )
    write_text(
        RESUME_PATH,
        f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4738-Y5-R2FR-tracefree-Khat-right-inverse-parent-action-or-conservation-quarantine-equations.md`

## Decision

`{DECISION}`

## What moved forward

- The legal trace-free right-inverse candidate was derived as a Hessian/York-style operator.
- Its divergence law shows exact cancellation needs a parent-owned inverse differential operator, boundary/gauge/domain data and metric-null owner stress.
- Conservation-owned quarantine was made explicit through `q_tr + div K_own = 0` plus the response-kernel target `R_loc q_tr = 0`.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
""",
    )


def add_claim_once(timestamp: str) -> None:
    with CLAIMS_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fieldnames = reader.fieldnames or []
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    new_row = {
        "claim_id": CLAIM_ID,
        "domain": "local_gr_newton_bridge",
        "claim": "4738 derives the legal trace-free Khat right-inverse shape and shows exact transition-current cancellation requires parent-owned inverse/operator, boundary and metric-null owner structure.",
        "current_evidence": "Generated source register, trace-free derivation rows, parent-action owner contract, conservation quarantine equations, finite residual rows, route matrix, gates, firewalls, decision, status, next target and validation.",
        "status": "tracefree_RI_parent_action_unsigned_quarantine_contract_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Promoting inverse-operator closure, tracefree shape, or quarantine bookkeeping as derived local GR.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "Delta_K divergence, RI commutator, boundary/connection tails, metric response kernel and ordinary matter GR/Newton preservation remain open.",
        "title": "Trace-free Khat right-inverse parent action or conservation quarantine equations",
        "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
    }
    for fieldname in fieldnames:
        new_row.setdefault(fieldname, "")
    rows.append(new_row)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def cleanup_pycache() -> None:
    pycache_path = POST / "scripts" / "__pycache__"
    if pycache_path.exists():
        shutil.rmtree(pycache_path)


def validation_rows(
    sources: list[dict[str, Any]],
    derivation: list[dict[str, Any]],
    parent_contract: list[dict[str, Any]],
    quarantine: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    generated_with_validation = GENERATED_CSVS + [VALIDATION_CSV]
    checks = [
        ("VAL4738_0_sources_exist", all(source["exists"] for source in sources), "all cited 4738 source paths exist"),
        ("VAL4738_1_needles_found", all(source["needle_found"] for source in sources), "all cited 4738 source needles found"),
        ("VAL4738_2_tracefree_candidate", any(row["row_id"] == "TFRI4738_1_scalar_ansatz" for row in derivation), "trace-free Hessian candidate row exists"),
        ("VAL4738_3_divergence_law", any(row["row_id"] == "TFRI4738_2_divergence" for row in derivation), "right-inverse divergence law row exists"),
        ("VAL4738_4_nonlocal_parent_gate", any(row["row_id"] == "TFRI4738_5_nonlocal_status" for row in derivation), "inverse operator remains parent-signature gated"),
        ("VAL4738_5_parent_contract_unsigned", len(parent_contract) >= 6 and all(row["valid_for_claim"] is False for row in parent_contract), "parent owner contract has unsigned nonclaim clauses"),
        ("VAL4738_6_quarantine_equations", any(row["equation_id"] == "QUAR4738_3_metric_kernel" for row in quarantine), "R_loc quarantine kernel equation staged"),
        ("VAL4738_7_finite_rows", any(row["row_id"] == "FIN4738_2_CTFRI" for row in finite), "C_TF_RI finite/zero row staged"),
        ("VAL4738_8_fake_route_rejected", any(row["route"] == "Khat_equals_Gamma_g" and row["status"] == "rejected_firewall" for row in routes), "fake metric Khat route rejected"),
        ("VAL4738_9_claim_gates_closed", all(row["valid_for_claim"] is False for row in gates), "all claim gates remain closed"),
        ("VAL4738_10_docs_written", DOC_PATH.exists() and FORMAL_PATH.exists(), "checkpoint and formal documents written"),
        ("VAL4738_11_spine_packet_markers", MARKER in read_text(SPINE_PATH) and PACKET_MARKER in read_text(PACKET_PATH), "spine and packet markers inserted"),
        ("VAL4738_12_claim_row_added", CLAIM_ID in read_text(CLAIMS_PATH), "claims register contains L-580"),
        ("VAL4738_13_resume_updated", NEXT_TARGET in read_text(RESUME_PATH), "resume points to 4739 next target"),
        ("VAL4738_14_csv_parse", all(parse_csv(csv_path) for csv_path in generated_with_validation if csv_path.exists()), "all generated 4738 CSV files parse cleanly"),
        ("VAL4738_15_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "check_id": "VAL4738_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "4738 trace-free Khat right-inverse parent action or conservation quarantine equations validation",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    derivation = tracefree_derivation_rows(timestamp)
    parent_contract = parent_contract_rows(timestamp)
    quarantine = quarantine_rows(timestamp)
    finite = finite_rows(timestamp)
    routes = route_matrix_rows(timestamp)
    gates = gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(TRACEFREE_DERIVATION_CSV, derivation)
    write_csv(PARENT_CONTRACT_CSV, parent_contract)
    write_csv(QUARANTINE_CSV, quarantine)
    write_csv(FINITE_ROWS_CSV, finite)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, derivation, parent_contract, quarantine, finite, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, derivation, parent_contract, quarantine, finite, routes, gates, timestamp))


if __name__ == "__main__":
    main()
