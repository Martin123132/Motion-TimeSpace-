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

CHECKPOINT = "4299"
CLAIM_ID = "L-140"
BRANCH = "MTS_R2FR_Y5_DVGAMMA_DVKHAT_FIRST_SOURCE_COEFFICIENT_OR_QAP_PARENT_SIGNATURE_4299"
DECISION = "QAP_PARENT_SIGNATURE_NOT_CLOSED_DVGAMMA_DVKHAT_FIRST_SOURCE_COEFFICIENT_TEMPLATES_BUILT_NONCLAIM"
MARKER = "PPC4161_DVGAMMA_DVKHAT_FIRST_SOURCE_COEFFICIENT_OR_QAP_SIGNATURE_4299"
PACKET_MARKER = "PPC4161_PACKET_DVGAMMA_DVKHAT_FIRST_SOURCE_COEFFICIENT_OR_QAP_SIGNATURE_4299"
NEXT_TARGET = "4300-Y5-R2FR-DvGamma-m-Lcg-zero-or-first-coefficient-source-row.md"

FORMAL_PATH = FORMAL / "315-PPC4161-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md"
DOC_PATH = POST / "4299-Y5-R2FR-DvGamma-DvKhat-first-source-coefficient-or-QAP-parent-signature.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4299_VALIDATION.csv"

STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4299_00_4298_formal": (
        FORMAL / "314-PPC4161-Gamma-Khat-hidden-dependence-factorization-or-first-Dv-qtr-bound-row.md",
        "D_v Gamma_eff = 0        not proved,",
        "4298 handoff: Gamma/Khat q-factorisation failed and D_v rows are required.",
    ),
    "SRC4299_01_4298_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4298_FACTORISATION_AUDIT.csv",
        "FA4298_6_verdict",
        "4298 machine verdict: D_v q_tr=0 is not proved.",
    ),
    "SRC4299_02_4298_matrix": (
        SOURCE_DIR / "P8_Y5_R2FR_4298_DV_COEFFICIENT_BOUND_MATRIX.csv",
        "CB4298_000",
        "4298 coefficient matrix supplies the local threshold map.",
    ),
    "SRC4299_03_3520_QAP": (
        POST / "3520-Y5-R2FR-quotient-action-principle-derives-q-normal-form-or-finite-source-bounds.md",
        "QAP_derives_3519_normal_form",
        "3520 gives the conditional QAP theorem but keeps parent gates unsigned.",
    ),
    "SRC4299_04_3521_QAP_gate": (
        POST / "3521-Y5-R2FR-MTS-primitives-to-quotient-action-principle-or-explicit-adoption-gate.md",
        "QAP_NOT_PARENT_DERIVED_YET_EXPLICIT_ADOPTION_GATE_REQUIRED",
        "3521 states the primitive-to-QAP derivation is not yet parent-owned.",
    ),
    "SRC4299_05_1366_Gamma_shape": (
        POST / "1366-Y5-R10-RAB-Gamma-eff-scalar-density-definition-hunt-or-q_loc-envelope.md",
        "Gamma_eff=L_cg^-2F(m)",
        "1366 provides the nonclaim Gamma_eff formula-shape seed and live Delta_K gap.",
    ),
    "SRC4299_06_1010_DeltaK": (
        POST / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
        "Delta_K | K_hat - K_metric[Gamma_eff]",
        "1010 retains the Gamma/Khat metric-response gap.",
    ),
    "SRC4299_07_parent_equations": (
        FORMAL / "83-parent-equations-v1.md",
        "Gamma_eff = -1/4 K_MTS.",
        "Parent equations define Gamma_eff and the trace/trace-free split.",
    ),
    "SRC4299_08_Lcg_gradient": (
        FORMAL / "90-Lcg-gradient-trace-bound.md",
        "|nabla Gamma_eff|",
        "L_cg gradient gate supplies the chain-rule shape behind D_v Gamma_eff.",
    ),
    "SRC4299_09_4293_requirements": (
        SOURCE_DIR / "P8_Y5_R2FR_4293_REQUIRED_SUPPRESSION_ROWS.csv",
        "REQ4293_WEP",
        "4293 supplies the WEP/PPN/clock/orbit/Gdot/R10 required suppression rows.",
    ),
}

QAP_CLAUSES = [
    (
        "QAP4299_0_equivalence_relation",
        "parent history equivalence relation",
        "MTS must define Phi~Phi' from motion/time/space identity before readout.",
        "3521 says this is strongly motivated but not formalized as a parent equivalence relation.",
        "NOT_PARENT_SIGNED",
    ),
    (
        "QAP4299_1_qmap_kernel",
        "field-by-field vertical kernel",
        "For every local vertical v in ker(Dq), Gamma_eff, K_hat, connection and boundary data must be q-basic.",
        "4298 and 4297 show raw q_tr verticality still requires explicit D_v clauses.",
        "NOT_PARENT_SIGNED",
    ),
    (
        "QAP4299_2_action_descent",
        "action descends before matter/source variation",
        "S_parent[Phi,Psi] must equal Sbar[q(Phi),Psi] up to proper boundary/action-unit terms.",
        "3520 only gives conditional consequences; 3521 keeps action descent behind the primitive identity gate.",
        "CONDITIONAL_ONLY",
    ),
    (
        "QAP4299_3_boundary_properness",
        "boundary/reference data are q-basic or exact",
        "No boundary, reference subtraction, source mask, or corner term may select representatives inside a q-fibre.",
        "1010/1366 keep boundary/source-current gaps active for local residuals.",
        "NOT_PARENT_SIGNED",
    ),
    (
        "QAP4299_4_no_hidden_tower",
        "no hidden non-EH tower after quotient descent",
        "Nonbasic Gamma/Khat, disformal, Weyl, source-label or marker operators must be absent or residual-bounded.",
        "3520 blocks direct nonbasic source operators conditionally, but parent-owned exhaustion is not proved.",
        "NOT_PARENT_SIGNED",
    ),
    (
        "QAP4299_5_verdict",
        "QAP parent signature for D_v Gamma_eff/D_v K_hat",
        "If all QAP clauses passed, D_v Gamma_eff=D_v K_hat=C_conn=B_boundary=0 for raw transition q_tr.",
        "At least equivalence, kernel, action descent, boundary and no-hidden-tower clauses are unsigned.",
        "QAP_NOT_PARENT_SIGNED_USE_COEFFICIENT_ROUTE",
    ),
]

DVGAMMA_ROWS = [
    (
        "DVG4299_0_chain_rule",
        "D_v Gamma_eff",
        "D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg",
        "Gamma_eff=L_cg^-2F(m)",
        "Exact chain-rule route once Gamma_eff formula-shape is adopted.",
        "DERIVED_FORMULA_SHAPE_NONCLAIM",
    ),
    (
        "DVG4299_1_m_zero_clause",
        "D_v m",
        "D_v m = 0",
        "m must be q-basic or an invariant scalar of the quotient parent state.",
        "Would kill the first D_v Gamma_eff source leg.",
        "NOT_PARENT_SIGNED",
    ),
    (
        "DVG4299_2_Lcg_zero_clause",
        "D_v ln L_cg",
        "D_v ln L_cg = 0",
        "L_cg must be q-basic or fixed by quotient-invariant coarse-graining geometry.",
        "Would kill the second D_v Gamma_eff source leg.",
        "NOT_PARENT_SIGNED",
    ),
    (
        "DVG4299_3_first_coefficient",
        "C_DvGamma_total",
        "C_DvGamma_total := |P_obs nabla(L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg)|/a_ref",
        "Requires sourced m profile, L_cg profile, F_m normalization, projection P_obs and local acceleration/reference norm.",
        "This is the first measurable coefficient if the zero theorem fails.",
        "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
    ),
]

DVKHAT_ROWS = [
    (
        "DVK4299_0_metric_response_split",
        "D_v K_hat",
        "D_v K_hat = D_v Delta_K + D_v K_metric[Gamma_eff]",
        "Delta_K := K_hat - K_metric[Gamma_eff]",
        "This separates the true Khat mismatch from the Gamma-driven metric-response piece.",
        "DERIVED_SPLIT_NONCLAIM",
    ),
    (
        "DVK4299_1_DeltaK_zero_clause",
        "D_v Delta_K",
        "D_v Delta_K = 0",
        "K_hat must equal the variational metric response to Gamma_eff, including connection/domain/boundary terms.",
        "Would remove the independent trace-free residual leakage.",
        "NOT_PARENT_SIGNED",
    ),
    (
        "DVK4299_2_Kmetric_clause",
        "D_v K_metric[Gamma_eff]",
        "D_v K_metric[Gamma_eff] = K_metric'[Gamma_eff] D_v Gamma_eff + connection/domain/boundary kernels",
        "If D_v Gamma_eff=0 and all kernels descend, this term can vanish.",
        "Depends on the D_v Gamma_eff gate plus the 1010 Helmholtz/action-existence route.",
        "CONDITIONAL_ON_DVGAMMA_AND_HELMHOLTZ",
    ),
    (
        "DVK4299_3_memory_gradient_option",
        "D_v K_hat_memory",
        "D_v K_hat_memory = (D_v b_mem) S_m + b_mem D_v S_m + connection/g_obs terms",
        "Only valid if a memory-gradient ansatz is explicitly adopted for K_hat.",
        "Possible coefficient route, not a parent definition.",
        "OPTIONAL_ANSATZ_NOT_CLAIM",
    ),
    (
        "DVK4299_4_first_coefficient",
        "C_DvKhat_total",
        "C_DvKhat_total := |P_obs nabla_mu(D_v Delta_K^{mu nu}+D_v K_metric[Gamma_eff]^{mu nu})|/a_ref",
        "Requires sourced Delta_K tensor norm, metric-response kernels, projection P_obs and local acceleration/reference norm.",
        "This is the first measurable coefficient if Khat equality cannot be proved.",
        "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
    ),
]

COEFFICIENTS = [
    (
        "C4299_DVGAMMA_M",
        "D_v Gamma_eff",
        "m-profile hidden dependence leg",
        "C_m := |P_obs nabla(L_cg^-2 F_m D_v m)|/a_ref",
        "D_v m source row, F_m, L_cg profile, projection and a_ref",
    ),
    (
        "C4299_DVGAMMA_LCG",
        "D_v Gamma_eff",
        "L_cg hidden dependence leg",
        "C_Lcg := |P_obs nabla(2 Gamma_eff D_v ln L_cg)|/a_ref",
        "D_v ln L_cg source row, Gamma_eff profile, projection and a_ref",
    ),
    (
        "C4299_DVGAMMA_TOTAL",
        "D_v Gamma_eff",
        "total trace channel",
        "C_DvGamma_total := |P_obs nabla(D_v Gamma_eff)|/a_ref",
        "C_m and C_Lcg, with no cancellation credit unless parent-signed",
    ),
    (
        "C4299_DVKHAT_DELTAK",
        "D_v K_hat",
        "metric-response mismatch channel",
        "C_DeltaK := |P_obs nabla_mu D_v Delta_K^{mu nu}|/a_ref",
        "Delta_K tensor source row and divergence/projection norm",
    ),
    (
        "C4299_DVKHAT_KMETRIC",
        "D_v K_hat",
        "Gamma metric-response channel",
        "C_Kmetric := |P_obs nabla_mu D_v K_metric[Gamma_eff]^{mu nu}|/a_ref",
        "Gamma_eff metric-response kernels and Helmholtz/action-existence route",
    ),
    (
        "C4299_DVKHAT_BMEM",
        "D_v K_hat",
        "memory-gradient ansatz channel",
        "C_bmem := |P_obs nabla_mu[(D_v b_mem)S_m + b_mem D_v S_m]^{mu nu}|/a_ref",
        "Only if K_hat memory-gradient ansatz is explicitly selected and sourced",
    ),
    (
        "C4299_CONN",
        "C_conn",
        "connection/commutator channel",
        "C_conn := |P_obs C_conn^nu[v;Gamma_eff,K_hat,g_obs]|/a_ref",
        "Connection/coframe descent or direct commutator norm",
    ),
    (
        "C4299_BOUNDARY",
        "B_boundary",
        "boundary/topological support channel",
        "C_boundary := |P_obs B_boundary^nu[v]|/a_ref",
        "No-flux/proper-boundary theorem or boundary norm row",
    ),
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
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
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
                "4299 tests whether the Quotient Action Principle can parent-sign the 4298 D_v Gamma_eff and D_v K_hat zero "
                "conditions. The QAP route would be the clean theorem, but the current corpus still lacks a parent-owned "
                "history equivalence relation, qmap kernel, action descent, boundary properness and hidden-tower exhaustion. "
                "Therefore 4299 activates the coefficient route: D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg, "
                "and D_v K_hat = D_v Delta_K + D_v K_metric[Gamma_eff]. Numeric/source coefficient rows are templates only."
            ),
            (
                "4299 source register, QAP parent signature audit, D_v Gamma reduction rows, D_v Khat reduction rows, first "
                "source-coefficient template, coefficient-to-4293 gate, decision, firewall, status, next-target and validation CSV."
            ),
            "private_qap_not_parent_signed_dvgamma_dvkhat_coefficient_route_nonclaim",
            (
                "Try to prove D_v m=0 and D_v ln L_cg=0 from quotient identity, or source the first D_v Gamma_eff coefficient "
                "against the 4293 WEP-dominated local bound vector."
            ),
            (
                "Treating QAP as already derived, using the coefficient templates as numeric evidence, allowing cancellation "
                "between D_v Gamma_eff and D_v K_hat without a parent identity, or claiming local GR/PPN/WEP/R10 pass."
            ),
        ]
    )
    path.write_text(text.rstrip() + "\n" + row + "\n", encoding="utf-8")


def requirement_rows() -> List[Dict[str, str]]:
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


def qap_parent_signature_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for clause_id, clause, required_signature, current_evidence, status in QAP_CLAUSES:
        rows.append(
            {
                **common(),
                "clause_id": clause_id,
                "clause": clause,
                "required_signature": required_signature,
                "current_evidence": current_evidence,
                "status": status,
                "fires_now": "False",
                "effect_if_signed": "D_v Gamma_eff=D_v K_hat=C_conn=B_boundary=0 for the raw transition branch" if clause_id.endswith("_verdict") else "supports QAP parent signature",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def dvgamma_reduction_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for reduction_id, object_name, formula, required_input, interpretation, status in DVGAMMA_ROWS:
        rows.append(
            {
                **common(),
                "reduction_id": reduction_id,
                "object": object_name,
                "formula_or_clause": formula,
                "required_input": required_input,
                "interpretation": interpretation,
                "status": status,
                "zero_claim": "False",
                "coefficient_required": "True" if status == "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW" else "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def dvkhat_reduction_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for reduction_id, object_name, formula, required_input, interpretation, status in DVKHAT_ROWS:
        rows.append(
            {
                **common(),
                "reduction_id": reduction_id,
                "object": object_name,
                "formula_or_clause": formula,
                "required_input": required_input,
                "interpretation": interpretation,
                "status": status,
                "zero_claim": "False",
                "coefficient_required": "True" if status == "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW" else "False",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def coefficient_template_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for coefficient_id, term, channel, definition, required_source in COEFFICIENTS:
        rows.append(
            {
                **common(),
                "coefficient_id": coefficient_id,
                "term": term,
                "channel": channel,
                "definition": definition,
                "required_source_or_parent_input": required_source,
                "current_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                "units": "dimensionless_after_projection_normalization",
                "source_path": "MISSING_SOURCE_PATH",
                "status": "TEMPLATE_NONCLAIM",
                "no_cancellation_credit": "True",
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
    return rows


def coefficient_to_4293_gate_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    requirements = requirement_rows()
    for coefficient_id, term, channel, definition, _required_source in COEFFICIENTS:
        for requirement in requirements:
            required_value = requirement.get("required_value", "MISSING_REQUIRED_VALUE")
            required_numeric = to_float(required_value)
            rows.append(
                {
                    **common(),
                    "gate_id": f"G4299_{len(rows):03d}",
                    "coefficient_id": coefficient_id,
                    "term": term,
                    "channel": channel,
                    "arena_requirement": requirement.get("requirement_id", ""),
                    "arena": requirement.get("arena", ""),
                    "observable": requirement.get("observable", ""),
                    "required_value": required_value,
                    "units": requirement.get("units", ""),
                    "requirement_law": requirement.get("law", ""),
                    "coefficient_definition": definition,
                    "coefficient_value": "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW",
                    "required_value_positive_numeric": str(math.isfinite(required_numeric) and required_numeric > 0),
                    "comparison_status": "NOT_RUN_MISSING_COEFFICIENT",
                    "interpretation": "Zero theorem preferred; otherwise this coefficient must satisfy the imported 4293 local threshold.",
                    "claim_allowed": "False",
                    "valid_for_claim": "False",
                }
            )
    return rows


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "decision_id": "DEC4299_0",
            "selected_route": "COEFFICIENT_ROUTE_AFTER_QAP_SIGNATURE_FAIL",
            "reason": "QAP would kill the D_v terms cleanly, but 3521/3520 do not parent-sign all QAP clauses for raw transition q_tr.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "decision_id": "DEC4299_1",
            "selected_route": "ATTACK_DVGAMMA_FIRST",
            "reason": "The WEP threshold is the harshest row, and D_v Gamma_eff has the cleanest chain-rule split into D_v m and D_v ln L_cg.",
            "next_target": NEXT_TARGET,
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def firewall_rows() -> List[Dict[str, str]]:
    forbidden = [
        ("FW4299_0", "Do not use QAP as a hidden axiom; if adopted, label it QAP_LC closure."),
        ("FW4299_1", "Do not treat C4299_* template rows as sourced numeric coefficients."),
        ("FW4299_2", "Do not cancel D_v Gamma_eff against D_v K_hat unless a parent identity forces term-by-term cancellation."),
        ("FW4299_3", "Do not claim local GR, WEP, PPN, R10, clock or orbital pass from 4299."),
        ("FW4299_4", "Do not demote Delta_K without the 1010 metric-response/Helmholtz/action-existence route."),
    ]
    return [
        {
            **common(),
            "firewall_id": firewall_id,
            "forbidden_move": forbidden_move,
            "status": "ACTIVE",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
        for firewall_id, forbidden_move in forbidden
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "status_id": "STAT4299_0",
            "object": "QAP_parent_signature",
            "status": "NOT_PARENT_SIGNED",
            "effect": "D_v zero theorem does not fire.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4299_1",
            "object": "D_v Gamma_eff",
            "status": "CHAIN_RULE_REDUCED_TO_D_v_m_AND_D_v_ln_Lcg",
            "effect": "Next derivation target becomes q-basic m/L_cg or first coefficient source row.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4299_2",
            "object": "D_v K_hat",
            "status": "SPLIT_TO_Delta_K_AND_Kmetric_RESPONSE",
            "effect": "Khat branch remains tied to Delta_K/Helmholtz/action-existence gap.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            **common(),
            "status_id": "STAT4299_3",
            "object": "local_precision_claim",
            "status": "BLOCKED_NONCLAIM",
            "effect": "No local-GR/PPN/WEP/R10 pass is promoted.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            **common(),
            "next_target_id": "NT4299_0",
            "next_target": NEXT_TARGET,
            "target_question": "Can D_v m=0 and D_v ln L_cg=0 be derived from the quotient/identity structure, or must the first D_v Gamma_eff coefficient be sourced against 4293?",
            "preferred_route": "derive q-basic m and L_cg first; only then try numeric/source fallback",
            "fallback_route": "fill C4299_DVGAMMA_M and C4299_DVGAMMA_LCG with sourced profile coefficients and compare to WEP/PPN/clock/orbit gates",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def markdown_table(rows: List[Dict[str, str]], columns: List[str]) -> str:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _column in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(row.get(column, "").replace("\n", " ") for column in columns) + " |")
    return "\n".join(lines)


def formal_doc() -> str:
    requirements = {row.get("requirement_id", ""): row.get("required_value", "") for row in requirement_rows()}
    qap_rows = qap_parent_signature_rows()
    dvgamma_rows = dvgamma_reduction_rows()
    dvkhat_rows = dvkhat_reduction_rows()
    coefficient_rows = coefficient_template_rows()
    return f"""
# 315 PPC4161 DvGamma/DvKhat first source coefficient or QAP parent signature

Marker: `{MARKER}`

## Decision

`{DECISION}`

This checkpoint tries the clean route first: parent-sign QAP strongly enough that raw transition vertical directions cannot change `Gamma_eff`, `K_hat`, the local connection, or boundary support. That route does not close yet, so 4299 converts the gap into explicit first-source coefficient rows rather than another vague "something missing" note.

## QAP signature gate

{markdown_table(qap_rows, ["clause_id", "clause", "status", "current_evidence"])}

## D_v Gamma_eff reduction

Using the nonclaim formula-shape seed:

```text
Gamma_eff = L_cg^-2 F(m),
```

the transition vertical variation is:

```text
D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg.
```

{markdown_table(dvgamma_rows, ["reduction_id", "object", "formula_or_clause", "status"])}

## D_v K_hat reduction

The current safe split is:

```text
Delta_K := K_hat - K_metric[Gamma_eff],
D_v K_hat = D_v Delta_K + D_v K_metric[Gamma_eff].
```

{markdown_table(dvkhat_rows, ["reduction_id", "object", "formula_or_clause", "status"])}

## First coefficient templates

{markdown_table(coefficient_rows, ["coefficient_id", "term", "channel", "current_value", "status"])}

## 4293 gates

The harshest imported local requirement remains:

```text
Y_WEP <= {requirements.get("REQ4293_WEP", "MISSING")}
```

The other near-local precision gates are:

```text
Y_gamma <= {requirements.get("REQ4293_GAMMA", "MISSING")}
Y_beta  <= {requirements.get("REQ4293_BETA", "MISSING")}
Y_clock <= {requirements.get("REQ4293_CLOCK", "MISSING")}
Y_orbit <= {requirements.get("REQ4293_ORBIT", "MISSING")}
```

Every `C4299_*` row is currently `MISSING_NUMERIC_PARENT_OR_SOURCE_ROW`, so no comparison is claim-grade.

## Result

4299 is real forward movement but not a victory lap: the local branch no longer says merely "QAP/coupling missing". It now says exactly which two first Gamma legs must vanish or be bounded:

```text
D_v m = 0,
D_v ln L_cg = 0,
```

and exactly which Khat residual has to be killed or sourced:

```text
Delta_K = K_hat - K_metric[Gamma_eff].
```

Next target: `{NEXT_TARGET}`.
"""


def checkpoint_doc() -> str:
    return f"""
# 4299 Y5 R2FR DvGamma/DvKhat first source coefficient or QAP parent signature

## Outcome

QAP is the clean route, but it is not parent-signed for raw transition `q_tr`. The coefficient route is therefore activated without making a local-GR claim.

## Key reductions

```text
D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg
```

```text
D_v K_hat = D_v Delta_K + D_v K_metric[Gamma_eff]
Delta_K := K_hat - K_metric[Gamma_eff]
```

## Next

Try to prove `D_v m=0` and `D_v ln L_cg=0` from quotient/identity structure. If that fails, source the first `D_v Gamma_eff` coefficient against the 4293 WEP-dominated local bound vector.
"""


def validation_rows(paths: Dict[str, Path]) -> List[Dict[str, str]]:
    sources = csv_rows(paths["sources"])
    qap_audit = csv_rows(paths["qap_parent_signature"])
    dvgamma = csv_rows(paths["dvgamma_reduction"])
    dvkhat = csv_rows(paths["dvkhat_reduction"])
    coefficient_templates = csv_rows(paths["coefficient_templates"])
    gates = csv_rows(paths["coefficient_to_4293_gate"])
    no_claim_rows = True
    for key, path in paths.items():
        if key == "validation":
            continue
        for row in csv_rows(path):
            if row.get("claim_allowed") == "True" or row.get("valid_for_claim") == "True":
                no_claim_rows = False
    validations = [
        ("VAL4299_0_sources_exist", bool(sources) and all(row["exists"] == "True" for row in sources), "all cited local sources exist"),
        ("VAL4299_1_needles_found", bool(sources) and all(row["required_text_found"] == "True" for row in sources), "all source needles found"),
        (
            "VAL4299_2_qap_verdict_blocked",
            any(row["clause_id"] == "QAP4299_5_verdict" and row["status"] == "QAP_NOT_PARENT_SIGNED_USE_COEFFICIENT_ROUTE" for row in qap_audit),
            "QAP route is explicitly blocked, not silently adopted",
        ),
        (
            "VAL4299_3_dvgamma_chain_rule",
            any(row["reduction_id"] == "DVG4299_0_chain_rule" and "D_v m" in row["formula_or_clause"] and "D_v ln L_cg" in row["formula_or_clause"] for row in dvgamma)
            and any(row["reduction_id"] == "DVG4299_3_first_coefficient" and row["status"] == "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW" for row in dvgamma),
            "D_v Gamma_eff reduced to m/L_cg legs plus first coefficient",
        ),
        (
            "VAL4299_4_dvkhat_split",
            any(row["reduction_id"] == "DVK4299_0_metric_response_split" and "Delta_K" in row["formula_or_clause"] for row in dvkhat)
            and any(row["reduction_id"] == "DVK4299_4_first_coefficient" and row["status"] == "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW" for row in dvkhat),
            "D_v K_hat split to Delta_K and metric-response rows",
        ),
        (
            "VAL4299_5_coefficient_templates_nonclaim",
            bool(coefficient_templates)
            and any(row["coefficient_id"] == "C4299_DVGAMMA_TOTAL" for row in coefficient_templates)
            and any(row["coefficient_id"] == "C4299_DVKHAT_DELTAK" for row in coefficient_templates)
            and all(row["current_value"] == "MISSING_NUMERIC_PARENT_OR_SOURCE_ROW" for row in coefficient_templates),
            "first source coefficient templates exist and remain missing/nonclaim",
        ),
        (
            "VAL4299_6_4293_gate_links",
            bool(gates)
            and any(row["coefficient_id"] == "C4299_DVGAMMA_TOTAL" and row["arena_requirement"] == "REQ4293_WEP" for row in gates)
            and any(row["coefficient_id"] == "C4299_DVKHAT_DELTAK" and row["arena_requirement"] == "REQ4293_GAMMA" for row in gates)
            and all(row["comparison_status"] == "NOT_RUN_MISSING_COEFFICIENT" for row in gates),
            "coefficient rows are linked to 4293 thresholds but not scored",
        ),
        (
            "VAL4299_7_required_values_positive",
            bool(gates) and all(row["required_value_positive_numeric"] == "True" for row in gates),
            "all imported 4293 required values are positive numeric",
        ),
        ("VAL4299_8_formal_doc", FORMAL_PATH.exists() and MARKER in read_text(FORMAL_PATH), "formal document exists with marker"),
        ("VAL4299_9_checkpoint_doc", DOC_PATH.exists() and CHECKPOINT in read_text(DOC_PATH), "post-checkpoint document exists"),
        (
            "VAL4299_10_claim_row",
            any(line.startswith(f"{CLAIM_ID},") for line in read_text(FORMAL / "02-claims-register.csv").splitlines()),
            "claims register contains L-140 private nonclaim row",
        ),
        (
            "VAL4299_11_spine_packet",
            MARKER in read_text(FORMAL / "07-unification-spine.md")
            and PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"),
            "spine and packet markers exist",
        ),
        ("VAL4299_12_no_claim_rows", no_claim_rows, "all generated rows remain nonclaim rows"),
    ]
    for name, path in paths.items():
        if name == "validation":
            continue
        validations.append((f"VAL4299_csv_{name}", bool(csv_rows(path)), f"{path.name} parses with rows"))
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
        "sources": SOURCE_DIR / "P8_Y5_R2FR_4299_SOURCE_REGISTER.csv",
        "qap_parent_signature": SOURCE_DIR / "P8_Y5_R2FR_4299_QAP_PARENT_SIGNATURE_AUDIT.csv",
        "dvgamma_reduction": SOURCE_DIR / "P8_Y5_R2FR_4299_DVGAMMA_REDUCTION_ROWS.csv",
        "dvkhat_reduction": SOURCE_DIR / "P8_Y5_R2FR_4299_DVKHAT_REDUCTION_ROWS.csv",
        "coefficient_templates": SOURCE_DIR / "P8_Y5_R2FR_4299_FIRST_SOURCE_COEFFICIENT_TEMPLATE.csv",
        "coefficient_to_4293_gate": SOURCE_DIR / "P8_Y5_R2FR_4299_COEFFICIENT_TO_4293_GATE.csv",
        "decision": SOURCE_DIR / "P8_Y5_R2FR_4299_DECISION.csv",
        "firewall": SOURCE_DIR / "P8_Y5_R2FR_4299_CLAIM_FIREWALL.csv",
        "status": SOURCE_DIR / "P8_Y5_R2FR_4299_STATUS.csv",
        "next_target": SOURCE_DIR / "P8_Y5_R2FR_4299_NEXT_TARGET.csv",
        "validation": VALIDATION_PATH,
    }
    write_csv(paths["sources"], source_rows())
    write_csv(paths["qap_parent_signature"], qap_parent_signature_rows())
    write_csv(paths["dvgamma_reduction"], dvgamma_reduction_rows())
    write_csv(paths["dvkhat_reduction"], dvkhat_reduction_rows())
    write_csv(paths["coefficient_templates"], coefficient_template_rows())
    write_csv(paths["coefficient_to_4293_gate"], coefficient_to_4293_gate_rows())
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
        "PPC4161 4299 DvGamma/DvKhat first source coefficient or QAP signature",
        (
            "4299 tries the QAP parent signature first and keeps it blocked rather than smuggled. The fallback is now concrete: "
            "`D_v Gamma_eff = L_cg^-2 F_m D_v m - 2 Gamma_eff D_v ln L_cg`, while `D_v K_hat` splits into `D_v Delta_K` plus "
            "`D_v K_metric[Gamma_eff]`. The first source-coefficient templates are linked to the 4293 WEP/PPN/clock/orbit gates."
        ),
    )
    append_unique_block(
        FORMAL / "180-PPC4161-private-local-packet-integration.md",
        PACKET_MARKER,
        "4299 packet QAP-vs-coefficient handoff",
        (
            "Packet update: the next derivation no longer chases the whole coupling fog. It attacks `D_v m=0` and "
            "`D_v ln L_cg=0` first, with `Delta_K` kept as the Khat residual ledger."
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
