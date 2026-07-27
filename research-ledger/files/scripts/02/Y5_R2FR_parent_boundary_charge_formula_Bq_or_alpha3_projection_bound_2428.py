from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_BOUNDARY_CHARGE_FORMULA_BQ_OR_ALPHA3_PROJECTION_BOUND_2428"
CHECKPOINT_ID = "2428"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2428-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2428_SOURCE_REGISTER.csv",
    "formula": OUT / "P8_Y5_PARENT_QLOC_2428_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
    "owner_gate": OUT / "P8_Y5_PARENT_QLOC_2428_BQ_OWNER_GATE.csv",
    "reference_split": OUT / "P8_Y5_PARENT_QLOC_2428_REFERENCE_PROJECTION_SPLIT.csv",
    "cocycle": OUT / "P8_Y5_PARENT_QLOC_2428_KBOUNDARY_COCYCLE_CONTRACT.csv",
    "alpha3": OUT / "P8_Y5_PARENT_QLOC_2428_ALPHA3_PROJECTION_COEFFICIENT_TEMPLATE.csv",
    "r10_edge": OUT / "P8_Y5_PARENT_QLOC_2428_R10_EDGE_CONTRACT.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2428_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2428_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2428_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2428_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2428_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2428_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_formula": QUEUE / "JR2428_BQ_QQ_FORMULA_CONTRACT_NONCLAIM.csv",
    "queue_alpha3": QUEUE / "JR2428_ALPHA3_COEFFICIENT_RULE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "parent_Bq_Qq_alpha3_nonclaim_2428.csv",
    "beta_docs": BETA_DOCS / "BQ_QQ_ALPHA3_2428_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2428_00_2427_handoff",
        "source_path": ROOT / "2427-Y5-R2FR-boundary-charge-Qq-Kboundary-zero-or-beta-bound-first-row.md",
        "needles": ["NEXT2427_0_selected", "BRES2427_1_K_boundary_alpha3_q", "VAL2427_OVERALL"],
        "role": "current handoff selecting parent B_q/Q_q boundary formula",
    },
    {
        "source_id": "SRC2428_01_2427_validation",
        "source_path": OUT / "P8_Y5_BRR545_2427_VALIDATION.csv",
        "needles": ["VAL2427_OVERALL", "PASS"],
        "role": "confirms 2427 passed before 2428",
    },
    {
        "source_id": "SRC2428_02_2427_compact",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2427_COMPACT_PROPER_BOUNDARY_SILENCE_LEMMA.csv",
        "needles": ["QQK2427_6_verdict", "DERIVED_NARROW_SUBLEMMA_FULL_CLAIM_BLOCKED"],
        "role": "narrow compact/proper zero inherited into formula contract",
    },
    {
        "source_id": "SRC2428_03_2427_projection",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2427_FIRST_BETA_PROJECTION_TEMPLATE.csv",
        "needles": ["FBP2427_0_boundary_alpha3_q", "4e-20"],
        "role": "alpha3 and R10 fallback projection templates",
    },
    {
        "source_id": "SRC2428_04_2294_precedent",
        "source_path": ROOT / "2294-Y5-R2FR-parent-boundary-charge-formula-Bq-or-alpha3-projection-bound.md",
        "needles": ["BQF2294_4_verdict", "A3P2294_0_formula", "VAL2294_OVERALL"],
        "role": "prior q boundary formula contract checkpoint",
    },
    {
        "source_id": "SRC2428_05_2246_formula",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2246_PARENT_BOUNDARY_CHARGE_FORMULA.csv",
        "needles": ["BRF2246_1_candidate_charge_density", "FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED"],
        "role": "R_AB boundary charge formula scaffold",
    },
    {
        "source_id": "SRC2428_06_2246_cocycle",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2246_KBOUNDARY_COCYCLE_CONTRACT.csv",
        "needles": ["KBC2246_0_contract", "KBC2246_2_source_alpha3"],
        "role": "R_AB cocycle and alpha3 projection scaffold",
    },
    {
        "source_id": "SRC2428_07_local_alpha3_bound",
        "source_path": LOCAL_BOUNDS,
        "needles": ["Will_2014_PPN_alpha3_table", "4e-20"],
        "role": "source-backed alpha3 comparator anchor",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def formula_rows() -> list[dict[str, Any]]:
    return [
        base_row(formula_id="BQF2428_0_bulk_pairing", object="boundary pairing from D C_q", formula="delta int_Sigma epsilon_q C_q contains - int_partialSigma n_mu epsilon_q delta P_q^mu plus convention-dependent density terms", status="DERIVED_FROM_DCQ_CONTRACT", missing_inputs="P_q and density convention not parent-owned", claim_effect="identifies the boundary charge density that must be cancelled, exact, or bounded", score_ready=False),
        base_row(formula_id="BQF2428_1_candidate_charge_density", object="B_q surface density", formula="B_q = sigma n_mu P_q^mu + B_ct_q + B_ref_q + B_exact_q, with sigma fixed by the G_bulk +/- Q convention", status="FORMULA_SHAPE_DERIVED_SIGN_CONVENTION_OPEN", missing_inputs="P_q, counterterm, reference subtraction, exact primitive, and density convention missing", claim_effect="turns q edge charge into a concrete coefficient contract rather than a vague coupling", score_ready=False),
        base_row(formula_id="BQF2428_2_candidate_Qq", object="Q_q boundary charge", formula="Q_q[epsilon]=int_partialSigma epsilon_q B_q dS", status="CONTRACT_READY_NOT_PARENT_SIGNED", missing_inputs="requires Theta_q/L_q sector owner and allowed q boundary class", claim_effect="proper compact branch gives zero; source/large branch remains scoreable residual", score_ready=False),
        base_row(formula_id="BQF2428_3_exactness_route", object="exact/pure boundary repair", formula="B_q=d_boundary b_q+B_q^pure and int_partialSigma epsilon_q d_boundary b_q=int_partialpartialSigma epsilon_q b_q-int_partialSigma d_boundary epsilon_q b_q", status="MATHEMATICAL_ROUTE_ONLY", missing_inputs="b_q, harmonic sector, corner terms, and range-kernel derivative term not derived", claim_effect="exactness can close only with boundary-class and range-kernel conditions", score_ready=False),
        base_row(formula_id="BQF2428_4_verdict", object="parent B_q/Q_q formula status", formula="B_q/Q_q formula shape is explicit, but parent ownership is not closed", status="FORMULA_CONTRACT_BUILT_FULL_CLAIM_BLOCKED", missing_inputs="MISSING_PARENT_LQ_THETAQ_PQ_REFERENCE_PROJECTOR", claim_effect="move to parent q-sector Theta_q/P_q owner or alpha3/R10 nonclaim coefficient rows", score_ready=False),
    ]


def owner_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="BQG2428_0_Lq_owner", needed_object="parent q-sector Lagrangian block L_q", acceptance_test="L_q or parent constraint C_q must be selected from parent action, not reverse-engineered from a bound", current_status="MISSING_LQ_OR_CQ_OWNER", if_missing="B_q/Q_q cannot be parent-derived"),
        base_row(gate_id="BQG2428_1_Thetaq_owner", needed_object="parent symplectic potential Theta_q", acceptance_test="delta L_q=E_q delta q + d Theta_q(delta q) with finite boundary jet order", current_status="MISSING_THETA_Q", if_missing="Q_q differentiability and K_boundary bracket cannot be computed"),
        base_row(gate_id="BQG2428_2_Pq_owner", needed_object="boundary momentum P_q^mu", acceptance_test="P_q is derived from L_q/Theta_q or parent variation, not inserted as a free vector density", current_status="MISSING_PQ_OWNER", if_missing="B_q=n.P_q is a contract only"),
        base_row(gate_id="BQG2428_3_density_convention", needed_object="tensor versus densitized P_q convention", acceptance_test="choose C_q=-nabla_mu P_q^mu+J_q or C_q=-(1/sqrt(g))partial_mu Ptilde_q^mu+J_q before signs/units", current_status="CONVENTION_GATE_OPEN", if_missing="B_q sign, volume terms, and units are ambiguous"),
        base_row(gate_id="BQG2428_4_boundary_class", needed_object="allowed q boundary class", acceptance_test="proper compact, source/worldtube, reference, and range-kernel boundary classes must be separated", current_status="BOUNDARY_CLASS_SPLIT_OPEN", if_missing="compact zero cannot be promoted to source/test silence"),
        base_row(gate_id="BQG2428_5_verdict", needed_object="claim-grade B_q owner package", acceptance_test="BQG2428_0 through BQG2428_4 pass together", current_status="FAIL_CURRENT_CLAIM_BQ_NOT_PARENT_OWNED", if_missing="keep B_q/Q_q rows as nonclaim coefficient contracts"),
    ]


def reference_split_rows() -> list[dict[str, Any]]:
    return [
        base_row(split_id="RPS2428_0_GR_charge_guard", object="observed GR Hamiltonian/reference charges", rule="do not set ADM/time/rotation/Newtonian mass charges to zero when killing q-representative charge", required_input="boundary generator split and reference subtraction", status="GUARD_RETAINED"),
        base_row(split_id="RPS2428_1_representative_q_charge", object="proper compact representative-q charge", rule="Q_q^proper=0 from 2427 collar lemma", required_input="extension to non-proper/source boundary values", status="NARROW_ZERO_ONLY"),
        base_row(split_id="RPS2428_2_edge_source_projection", object="edge/source residual charge", rule="Qbar_edge_qH(lambda)=Pi_M^H[int_partialSigma F_lambda epsilon_q B_q dS]/M_H", required_input="Pi_M^H, F_lambda, B_q owner, source boundary class, units", status="RETAIN_NONCLAIM_RESIDUAL"),
        base_row(split_id="RPS2428_3_no_double_count", object="bulk/edge source split", rule="Q_q_total=Q_q_bulk+Q_q_edge with orthogonal support or absolute-tail summation", required_input="support split and no-cancellation policy", status="CLAIM_BLOCKED_UNTIL_SPLIT_OWNED"),
    ]


def cocycle_rows() -> list[dict[str, Any]]:
    return [
        base_row(cocycle_id="KBC2428_0_contract", object="boundary cocycle", formula="K_boundary[epsilon,eta]=delta_eta Q_q[epsilon]-delta_epsilon Q_q[eta]-Q_q[[epsilon,eta]] plus possible i_veta i_vepsilon Omega_boundary convention terms", needed_inputs="differentiable G_q, parent Omega_Y, v_q action on all fields, sign convention", current_status="FORMULA_CONTRACT_ONLY", score_ready=False),
        base_row(cocycle_id="KBC2428_1_proper_zero", object="proper compact cocycle", formula="K_boundary=0 when epsilon_q, eta_q, and required finite jets vanish on the boundary collar", needed_inputs="same finite-jet boundary class as 2427", current_status="NARROW_ZERO_INHERITED", score_ready=False),
        base_row(cocycle_id="KBC2428_2_source_alpha3", object="preferred-frame flux projection", formula="alpha3_MTS_q=K_boundary_alpha3_q*Phi_boundary_local_q", needed_inputs="K_boundary_alpha3_q, Phi_boundary_local_q, projection normalization", current_status="SOURCE_ANCHOR_READY_COEFFICIENTS_MISSING", score_ready=False),
        base_row(cocycle_id="KBC2428_3_R10_edge", object="short-range edge exchange projection", formula="alpha_q_edge(lambda) uses Qbar_edge_qH(lambda) qbar_qT(lambda) with absolute tails", needed_inputs="B_q, F_lambda, source/test support, K_q^R10(lambda), bound curve", current_status="R10_EDGE_CONTRACT_ONLY", score_ready=False),
    ]


def alpha3_rows() -> list[dict[str, Any]]:
    return [
        base_row(projection_id="A3P2428_0_formula", observable="alpha3", mts_formula="alpha3_MTS_q=K_boundary_alpha3_q*Phi_boundary_local_q", external_bound="4e-20", reference="source-intake/local_bounds/local_bound_claims.csv:Will_2014_PPN_alpha3_table", coefficient_bound_rule="if Phi_boundary_local_q is numeric and nonzero, |K_boundary_alpha3_q| <= 4e-20/|Phi_boundary_local_q|", current_status="COEFFICIENT_RULE_WRITTEN_PHI_AND_K_MISSING", score_ready=False),
        base_row(projection_id="A3P2428_1_theorem_zero_route", observable="alpha3", mts_formula="alpha3_MTS_q=0 if K_boundary_alpha3_q=0 or Phi_boundary_local_q=0 from a parent theorem", external_bound="4e-20", reference="source-intake/local_bounds/local_bound_claims.csv:Will_2014_PPN_alpha3_table", coefficient_bound_rule="theorem-zero must cite B_q exactness/no-flux or boundary flux amplitude zero", current_status="THEOREM_ZERO_NOT_SIGNED", score_ready=False),
        base_row(projection_id="A3P2428_2_numeric_route", observable="alpha3", mts_formula="|K_boundary_alpha3_q*Phi_boundary_local_q| <= 4e-20", external_bound="4e-20", reference="source-intake/local_bounds/local_bound_claims.csv:Will_2014_PPN_alpha3_table", coefficient_bound_rule="requires source-backed K, Phi, normalization, uncertainty policy, and no-cancellation tail addition", current_status="NUMERIC_ROUTE_INPUTS_MISSING", score_ready=False),
    ]


def r10_edge_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="R10E2428_0_Qbar_edge_qH", object="Qbar_edge_qH(lambda)", formula="Pi_M^H[int_partialSigma F_lambda(s) epsilon_q B_q(s) dS]/M_H", missing_inputs="B_q owner; F_lambda; Pi_M^H; source boundary class; units", score_ready=False),
        base_row(row_id="R10E2428_1_alpha_edge_bound", object="alpha_q_edge(lambda)", formula="|alpha_q_edge(lambda)| <= |K_q^R10(lambda)| |Qbar_edge_qH(lambda) qbar_qT(lambda)| + abs_tail_q(lambda)", missing_inputs="K_q^R10(lambda); qbar_qT; alpha_bound(lambda); absolute tail rows; valid units", score_ready=False),
    ]


def refusal_rows(groups: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in groups:
        for row in group:
            ident = row.get("formula_id") or row.get("gate_id") or row.get("split_id") or row.get("cocycle_id") or row.get("projection_id") or row.get("row_id")
            attempted = row.get("object") or row.get("needed_object") or row.get("observable") or ident
            result = row.get("status") or row.get("current_status") or "not_claim_promoted"
            reason = row.get("missing_inputs") or row.get("if_missing") or row.get("needed_inputs") or row.get("coefficient_bound_rule") or "SCORE_READY_FALSE"
            rows.append(base_row(refusal_id=f"REF2428_{ident}", attempted_claim=attempted, result=result, reason=f"{reason}; SCORE_READY_FALSE; VALID_FOR_CLAIM_FALSE", score_ready=False))
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(claim_id="CGATE2428_0_Bq_formula", claim="B_q/Q_q is parent-derived", gate_pass=False, reason="formula shape is explicit, but L_q, Theta_q, P_q, density convention, reference terms, and boundary class are not parent-owned"),
        base_row(claim_id="CGATE2428_1_full_local_GR", claim="full q no-pole/local-GR branch is closed", gate_pass=False, reason="B_q/Q_q is only one clause; Omega/DCq, degree count, and matter/no-marker descent remain open"),
        base_row(claim_id="CGATE2428_2_alpha3", claim="q alpha3 projection row is executable", gate_pass=False, reason="source-backed alpha3 bound exists but K_boundary_alpha3_q and Phi_boundary_local_q are missing"),
        base_row(claim_id="CGATE2428_3_R10_edge", claim="R10 q edge row is executable", gate_pass=False, reason="B_q owner, F_lambda, source/test supports, K_q^R10(lambda), and valid bound curve are missing"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2428_0_formula_status", decision="BQ_QQ_IS_A_CONCRETE_FORMULA_CONTRACT", rationale="D C_q boundary pairing fixes the required surface density up to sign/density/reference conventions", consequence="select or derive the parent L_q/Theta_q/P_q package, or retain B_q/Q_q as nonclaim coefficient contract"),
        base_row(decision_id="DEC2428_1_alpha3_status", decision="ALPHA3_BOUND_RULE_READY_COEFFICIENTS_MISSING", rationale="|K_boundary_alpha3_q Phi_boundary_local_q| <= 4e-20 is exact once K and Phi exist", consequence="derive theorem-zero for K/Phi or source numeric values with normalization"),
        base_row(decision_id="DEC2428_2_R10_status", decision="R10_EDGE_IS_SOURCE_TEST_PRODUCT_WITH_ABSOLUTE_TAILS", rationale="finite q exchange cannot be scored as a naked linear coupling", consequence="derive B_q, F_lambda, source/test support, K_q^R10(lambda), and alpha_bound(lambda) before scoring"),
        base_row(decision_id="DEC2428_3_next", decision="TRY_THETAQ_PQ_OWNER_NEXT", rationale="Theta_q is upstream of P_q, B_q, differentiability, K_boundary, and alpha3 projection coefficient", consequence="2429 parent q-sector Theta_q/P_q owner or boundary coefficient prior"),
        base_row(decision_id="DEC2428_4_claim_policy", decision="KEEP_PRIVATE_NONCLAIM", rationale="formula contract is not a parent-owned prediction", consequence="no GitHub action"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2428_0_selected",
            selection_status="selected",
            target_file="2429-Y5-R2FR-parent-q-sector-Thetaq-Pq-owner-or-boundary-coefficient-prior.md",
            target_script="scripts/Y5_R2FR_parent_q_sector_Thetaq_Pq_owner_or_boundary_coefficient_prior_2429.py",
            objective="try to derive or select the parent q-sector symplectic potential Theta_q and momentum P_q that own B_q; if this cannot close, create nonclaim priors/templates for K_boundary_alpha3_q, Phi_boundary_local_q, and Qbar_edge_qH",
            success_condition="Theta_q/P_q are parent-owned with finite-jet boundary order and convention, or boundary coefficient priors remain explicit nonclaim templates",
            do_not_do="do not invent numeric K/Phi/Qbar values, delete GR charges, score naked linear c_g, cancel residuals, claim R10/local-GR pass, edit formalization-workbench, or push GitHub",
        )
    ]


def copy_branch_rows(formula: list[dict[str, Any]], alpha3: list[dict[str, Any]], r10: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue_formula", OUTPUTS["formula"], COPY_TARGETS["queue_formula"], formula),
        ("queue_alpha3", OUTPUTS["alpha3"], COPY_TARGETS["queue_alpha3"], alpha3),
        ("branch_wep", OUTPUTS["alpha3"], COPY_TARGETS["branch_wep"], alpha3),
        ("beta_docs", OUTPUTS["r10_edge"], COPY_TARGETS["beta_docs"], r10),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, copied_rows in copy_specs:
        write_csv(target_path, copied_rows)
        rows.append(
            base_row(
                copy_id=f"BC2428_{copy_id}",
                source_path=source_path,
                target_path=target_path,
                target_exists=target_path.exists(),
                row_count=len(copied_rows),
                purpose="B_q/Q_q formula contract quarantine copy",
            )
        )
    return rows


def formalization_has_2428_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2428-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2428*",
        "*P8_Y5_BRR545_2428*",
        "*Y5_R2FR_parent_boundary_charge_formula_Bq_or_alpha3_projection_bound_2428*",
        "*JR2428*",
        "*BQ_QQ_ALPHA3_2428*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def flags_safe(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "gate_pass"):
                value = row.get(key)
                if value is True or stringify(value).lower() == "true":
                    return False
    return True


def build_validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    formula = rows_by_name["formula"]
    owner = rows_by_name["owner_gate"]
    alpha3 = rows_by_name["alpha3"]
    r10 = rows_by_name["r10_edge"]
    next_rows = rows_by_name["next_target"]

    csv_results = []
    for name, path in OUTPUTS.items():
        if name == "validation":
            continue
        parses, row_count, message = csv_parses(path)
        csv_results.append((name, parses, row_count, message))
    for copy_key, copy_path in COPY_TARGETS.items():
        parses, row_count, message = csv_parses(copy_path)
        csv_results.append((f"copy_{copy_key}", parses, row_count, message))

    checks = [
        ("VAL2428_SOURCES_EXIST", all(row["path_exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL2428_NEEDLES_FOUND", all(row["needles_found"] for row in source_rows), "all source needles found"),
        ("VAL2428_BQ_FORMULA", any(row["formula_id"] == "BQF2428_2_candidate_Qq" and "int_partialSigma" in row["formula"] for row in formula), "Q_q boundary charge formula contract written"),
        ("VAL2428_OWNER_BLOCKED", any(row["gate_id"] == "BQG2428_5_verdict" and "FAIL_CURRENT_CLAIM" in row["current_status"] for row in owner), "B_q owner package remains blocked"),
        ("VAL2428_ALPHA3_BOUND_RULE", any(row["projection_id"] == "A3P2428_0_formula" and row["external_bound"] == "4e-20" for row in alpha3), "alpha3 coefficient bound rule uses source-backed anchor"),
        ("VAL2428_R10_EDGE_NONCLAIM", all(not row["score_ready"] for row in r10), "R10 edge contract remains nonclaim"),
        ("VAL2428_NEXT_SELECTED", any(row["route_id"] == "NEXT2428_0_selected" and "Thetaq-Pq" in row["target_file"] for row in next_rows), "Theta_q/P_q ownership selected next"),
        ("VAL2428_FLAGS_SAFE", flags_safe(rows_by_name), "no claim/score flags are true"),
        ("VAL2428_BRANCH_COPIES", all(row["target_exists"] for row in branch_copy_rows), "branch copy files written"),
        ("VAL2428_CSV_PARSE", all(item[1] and item[2] > 0 for item in csv_results), "all generated CSV and branch copies parse with rows"),
        ("VAL2428_NO_FORMALIZATION_OUTPUT", not formalization_has_2428_artifacts(), "no 2428 artifacts written into formalization-workbench"),
    ]

    rows = [
        base_row(validation_id=validation_id, status="PASS" if passed else "FAIL", detail=detail, fatal=not passed)
        for validation_id, passed, detail in checks
    ]
    overall_passed = all(row["status"] == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2428_OVERALL",
            status="PASS" if overall_passed else "FAIL",
            detail="2428 builds the q B_q/Q_q boundary-charge formula contract, blocks parent ownership claims, writes alpha3/R10 edge nonclaim bounds, and selects Theta_q/P_q ownership next",
            fatal=not overall_passed,
        )
    )
    return rows


def write_document(rows_by_name: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> None:
    content = f"""# 2428 Y5 R2FR Parent Boundary Charge Formula Bq Or Alpha3 Projection Bound

## Result

2428 turns the q boundary leak into an explicit formula contract: `Q_q[epsilon]=int_partialSigma epsilon_q B_q dS`.

The candidate density is `B_q=sigma n_mu P_q^mu+B_ct_q+B_ref_q+B_exact_q`, but this is not parent-owned until `L_q`, `Theta_q`, and `P_q` are derived or selected. The alpha3 fallback is now an exact inequality: `|K_boundary_alpha3_q Phi_boundary_local_q| <= 4e-20`, still nonclaim because both MTS coefficients are missing.

## Practical Status

- **Progress:** q edge leakage must pass through named `B_q/Q_q` surface-density rows.
- **Still missing:** parent `L_q`, symplectic potential `Theta_q`, momentum `P_q`, density convention, reference subtraction, and boundary class.
- **Alpha3:** source-backed comparator exists, but MTS projection coefficients do not.
- **R10:** edge exchange remains a source/test product with absolute tails.
- **Next target:** derive/select `Theta_q/P_q` or keep boundary coefficient priors nonclaim.

## Source Register

{table(["source_id", "source_path", "path_exists", "needles_found", "role"], rows_by_name["source_register"])}

## Parent Boundary Charge Formula

{table(["formula_id", "object", "formula", "status", "missing_inputs", "claim_effect", "score_ready"], rows_by_name["formula"])}

## Bq Owner Gate

{table(["gate_id", "needed_object", "acceptance_test", "current_status", "if_missing"], rows_by_name["owner_gate"])}

## Reference Projection Split

{table(["split_id", "object", "rule", "required_input", "status"], rows_by_name["reference_split"])}

## Kboundary Cocycle Contract

{table(["cocycle_id", "object", "formula", "needed_inputs", "current_status", "score_ready"], rows_by_name["cocycle"])}

## Alpha3 Projection Coefficient Rule

{table(["projection_id", "observable", "mts_formula", "external_bound", "reference", "coefficient_bound_rule", "current_status", "score_ready"], rows_by_name["alpha3"])}

## R10 Edge Contract

{table(["row_id", "object", "formula", "missing_inputs", "score_ready"], rows_by_name["r10_edge"])}

## Refusal Runner

{table(["refusal_id", "attempted_claim", "result", "reason", "score_ready"], rows_by_name["refusal"])}

## Claim Gates

{table(["claim_id", "claim", "gate_pass", "reason"], rows_by_name["claim_gates"])}

## Decision Ledger

{table(["decision_id", "decision", "rationale", "consequence"], rows_by_name["decision"])}

## Next Target

{table(["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do"], rows_by_name["next_target"])}

## Validation

{table(["validation_id", "status", "detail", "fatal"], validation_rows)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    formula = formula_rows()
    alpha3 = alpha3_rows()
    r10 = r10_edge_rows()
    rows_by_name = {
        "source_register": source_register_rows(),
        "formula": formula,
        "owner_gate": owner_gate_rows(),
        "reference_split": reference_split_rows(),
        "cocycle": cocycle_rows(),
        "alpha3": alpha3,
        "r10_edge": r10,
        "refusal": refusal_rows([formula, owner_gate_rows(), reference_split_rows(), cocycle_rows(), alpha3, r10]),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_copy_rows = copy_branch_rows(formula, alpha3, r10)
    rows_by_name["branch_copies"] = branch_copy_rows
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows)

    validation_rows = build_validation_rows(rows_by_name, branch_copy_rows)
    write_csv(OUTPUTS["validation"], validation_rows)
    write_document(rows_by_name, validation_rows)
    remove_pycache()

    overall = next(row for row in validation_rows if row["validation_id"] == "VAL2428_OVERALL")
    print(f"{DOC}")
    print(f"{OUTPUTS['validation']}")
    print(f"VAL2428_OVERALL={overall['status']}")


if __name__ == "__main__":
    main()
