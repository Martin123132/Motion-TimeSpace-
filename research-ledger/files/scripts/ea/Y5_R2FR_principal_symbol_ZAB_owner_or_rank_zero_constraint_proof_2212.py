from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2212"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2212-Y5-R2FR-principal-symbol-ZAB-owner-or-rank-zero-constraint-proof.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2212_SOURCE_REGISTER.csv",
    "strict_symbol_audit": OUT / "P8_Y5_PARENT_QLOC_2212_STRICT_L0_PRINCIPAL_SYMBOL_AUDIT.csv",
    "cdb_symbol_queue": OUT / "P8_Y5_PARENT_QLOC_2212_CDB_PRINCIPAL_SYMBOL_QUEUE.csv",
    "rank_zero_contract": OUT / "P8_Y5_PARENT_QLOC_2212_RANK_ZERO_CONSTRAINT_CONTRACT.csv",
    "branch_update": OUT / "P8_Y5_PARENT_QLOC_2212_BRANCH_SELECTION_UPDATE.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2212_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2212_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2212_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2212_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2212_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2212_RANK_ZERO_CONSTRAINT_OR_CDB_SYMBOL_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2212_STRICT_L0_RANK_ZERO_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_PRINCIPAL_SYMBOL_2212_NONCLAIM.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


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
        writer.writerows(rows)


def csv_rows_parse(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body: list[str] = []
    for row in rows:
        body.append(
            "| "
            + " | ".join(
                str(row.get(column, "")).replace("\n", " ").replace("|", "\\|")
                for column in columns
            )
            + " |"
        )
    return "\n".join([header, sep, *body])


def remove_pycache() -> None:
    cache = ROOT / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)


def formalization_has_2212_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2212-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2212*",
        "*P8_Y5_BRR545_2212*",
        "*Y5_R2FR_principal_symbol_ZAB_owner_or_rank_zero_constraint_proof_2212*",
        "*JR2212*",
        "*PARENT_QLOC_PRINCIPAL_SYMBOL_2212*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2211_handoff",
            ROOT / "2211-Y5-R2FR-parent-quadratic-residue-ZM-owner-or-constraint-branch.md",
            ["NEXT2211_0_2212", "HESSIAN_NOT_RANGE_LEMMA_INSTALLED", "VAL2211_OVERALL"],
            "2211 rejects M_AB-only range ownership and selects Z_AB principal symbol or rank-zero proof.",
        ),
        (
            "2111_response_split",
            OUT / "P8_Y5_PARENT_QLOC_2111_KMETRIC_RESPONSE_SPLIT.csv",
            ["KRS2111_1_volume", "KRS2111_4_connection", "KRS2111_8_deltaK"],
            "fixed-L0 Hilbert response split: algebraic pieces close; CDB terms remain live.",
        ),
        (
            "2112_cdb_component",
            ROOT / "2112-Y5-R2FR-CDB-component-zero-or-bound-Kconn-Kdomain-Kboundary.md",
            ["CZG2112_1_Kconn_metric_only", "CDB2112_1_Kconn_norm", "VAL2112_OVERALL"],
            "CDB componentization: K_conn is highest-leverage remaining connection/derivative blocker.",
        ),
        (
            "1591_cdb_memory",
            ROOT / "1591-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-or-cR2-bound-row.md",
            ["CMA1591_0_fixed_L0_scope", "CMA1591_1_K_conn", "VAL1591_OVERALL"],
            "fixed-L0 closure is algebraic only; CDB/memory zero theorem fails current claim.",
        ),
        (
            "1675_constraint_first",
            ROOT / "1675-Y5-R2FR-constraint-first-Z-elimination-and-coframe-source-descent.md",
            ["CFD1675_0_parent_constraint", "Dq_Z_norm = 0", "VAL1675_OVERALL"],
            "constraint-first descent route is coherent but not parent-signed.",
        ),
        (
            "1011_source_current",
            ROOT / "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
            ["RDT1011_3_source_current_zero", "RDT1011_5_positive_operator", "V1011_SUMMARY"],
            "source-current and boundary zero are still the active rank-zero blockers.",
        ),
        (
            "2207_response_doublet",
            ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["Gamma_eff = Gamma0 + 1/2 M_AB", "GMV2207_0_response_doublet_setup", "VAL2207_OVERALL"],
            "response-doublet supplies algebraic Hessian shape but not live Khat/principal-symbol ownership.",
        ),
        (
            "2211_coefficient_rows",
            OUT / "P8_Y5_PARENT_QLOC_2211_COEFFICIENT_ACQUISITION_ROWS.csv",
            ["ZMC2211_0_Z_AB_principal_symbol", "ZMC2211_3_source_current", "MISSING_PARENT_DERIVED"],
            "machine-readable 2211 coefficient rows: Z_AB and source-current missing.",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source_id,
                source_path=str(path),
                path_exists=path.exists(),
                required_needles=";".join(needles),
                found_needles=";".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=role,
            )
        )
    return rows


def strict_symbol_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            audit_id="PSA2212_0_strict_branch_definition",
            object="strict fixed-L0 algebraic response-doublet branch",
            principal_symbol_result="Z_AB_strict = 0",
            derivation="Gamma_eff^0 is taken as an algebraic scalar density in Z with fixed L0 and no derivative, connection, domain, boundary or projector dependence.",
            implication="the Euler/Hessian piece is algebraic: M_AB Z^B = J_A, not (-Z_AB Delta + M_AB)Z=J.",
            caveat="this statement applies only to the strict algebraic subbranch, not the unresolved live CDB branch.",
            passes_now=True,
        ),
        base_row(
            audit_id="PSA2212_1_volume_chain",
            object="K_vol",
            principal_symbol_result="NO_Z_DERIVATIVE",
            derivation="volume response is proportional to the metric and Fhat(m*) or subtraction; it does not create spatial derivatives of Z.",
            implication="cannot own a Yukawa range.",
            caveat="off-vacuum algebraic amplitude still belongs in Q_alg, not Z_AB.",
            passes_now=True,
        ),
        base_row(
            audit_id="PSA2212_2_m_chain",
            object="K_m / algebraic Hessian",
            principal_symbol_result="M_AB_CANDIDATE_ONLY",
            derivation="the response-doublet M_AB is a second derivative of the local algebraic density in Z.",
            implication="can supply mass/Hessian curvature but not a Laplacian coefficient.",
            caveat="needs parent adoption, units and sign before even the algebraic constraint is claimable.",
            passes_now=False,
        ),
        base_row(
            audit_id="PSA2212_3_L_chain",
            object="fixed L0 chain",
            principal_symbol_result="NO_RANGE_SCALE_FROM_L0",
            derivation="fixed L0 suppresses readout-length variation but does not become a kinetic coefficient for Z.",
            implication="L0 is not lambda_X and cannot be inserted as R10 range.",
            caveat="readout-length separation still requires parent adoption.",
            passes_now=True,
        ),
        base_row(
            audit_id="PSA2212_4_strict_verdict",
            object="strict fixed-L0 branch",
            principal_symbol_result="FINITE_RANGE_R10_REJECTED_FOR_STRICT_BRANCH",
            derivation="with no derivative principal symbol, there is no generalized eigenvalue problem M v = mu^2 Z v.",
            implication="strict branch must be treated as rank-zero/algebraic constraint route.",
            caveat="CDB may still reintroduce derivative terms in the live branch and is audited separately.",
            passes_now=True,
        ),
    ]


def cdb_symbol_queue_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            queue_id="CPS2212_0_K_conn",
            component="K_conn",
            possible_principal_symbol_role="connection/derivative dependence could create or obstruct Z_AB",
            current_status="LIVE_UNEXTRACTED",
            evidence="2112 ranks K_conn as the highest-leverage blocker; metric-only LC lemma is conditional not parent-signed.",
            required_extraction="derive whether Gamma_eff/Khat depends on nabla Z, affine Gamma, torsion, nonmetricity, or hypermomentum and record the principal derivative order.",
            branch_effect="if second-order elliptic term exists, finite-range branch can reopen; if absent, rank-zero branch strengthens",
            score_ready=False,
        ),
        base_row(
            queue_id="CPS2212_1_K_domain",
            component="K_domain",
            possible_principal_symbol_role="domain/window/support variation can imitate source or boundary kinetic leakage",
            current_status="LIVE_UNEXTRACTED",
            evidence="2112 and 1591 keep domain selector and support/readout variation unsigned.",
            required_extraction="derive parent domain selector or finite norm/source map for delta_g domain/support terms.",
            branch_effect="cannot use rank-zero theorem until domain cannot re-source Z",
            score_ready=False,
        ),
        base_row(
            queue_id="CPS2212_2_K_boundary",
            component="K_boundary",
            possible_principal_symbol_role="integration-by-parts boundary primitive can encode the missing derivative operator or source charge",
            current_status="NARROW_ZERO_PLUS_LIVE_SOURCE_BOUNDARY",
            evidence="proper compact collar zero is importable narrowly; source worldtubes/corners/reference terms remain live.",
            required_extraction="separate proper-collar zero from source-worldtube boundary charge and corner/reference rows.",
            branch_effect="rank-zero source-current proof must include boundary B_A=0 or finite boundary residual",
            score_ready=False,
        ),
        base_row(
            queue_id="CPS2212_3_K_comm",
            component="K_comm / P_loc",
            possible_principal_symbol_role="projector commutator can turn algebraic source into observed derivative residual",
            current_status="LIVE_UNEXTRACTED",
            evidence="2112 keeps projector/readout commutator leakage symbolic.",
            required_extraction="parent-own P_loc and show it commutes with divergence/readout or bound the commutator.",
            branch_effect="without this, q_loc can survive even if strict Z equation is algebraic",
            score_ready=False,
        ),
        base_row(
            queue_id="CPS2212_4_live_verdict",
            component="live CDB branch",
            possible_principal_symbol_role="only remaining place where a Z_AB kinetic residue may hide",
            current_status="FINITE_RANGE_STATUS_HELD_OPEN_BY_CDB",
            evidence="strict algebraic branch has Z_AB=0; CDB terms are unresolved.",
            required_extraction="componentwise principal-symbol extraction or rank-zero/no-source theorem with CDB included",
            branch_effect="no global local-GR or R10 claim until resolved",
            score_ready=False,
        ),
    ]


def rank_zero_contract_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            contract_id="RZC2212_0_algebraic_euler",
            clause="rank-zero Euler equation",
            exact_requirement="On the physical quotient, the strict branch gives M_AB Z^B = J_A plus boundary/projector/source terms.",
            current_status="CONTRACT_WRITTEN_NOT_PARENT_SIGNED",
            missing_for_proof="parent adoption of M_AB; invertibility/projector of M_AB; source split J_A; boundary B_A; domain and units",
            claim_effect="can only yield local silence if J_A and boundary/projector sources vanish or are algebraically eliminated",
        ),
        base_row(
            contract_id="RZC2212_1_source_current_zero",
            clause="J_A=0",
            exact_requirement="ordinary matter, source normalization, memory, bath and readout terms do not source the eliminated Z directions.",
            current_status="BLOCKED_NONCLAIM",
            missing_for_proof="1011 source-current zero; Y5/Y6 source silence; matter/coframe/source descent; no hidden marker/readout source",
            claim_effect="without J_A=0, rank-zero branch produces an algebraic residual, not GR",
        ),
        base_row(
            contract_id="RZC2212_2_boundary_zero",
            clause="B_A=0",
            exact_requirement="boundary primitive, corner, worldtube, reference and projector flux terms vanish on the same local branch.",
            current_status="BLOCKED_NONCLAIM",
            missing_for_proof="proper-collar theorem is narrow; source worldtube/corner/reference terms not signed",
            claim_effect="boundary charge can feed R10/WEP/orbital residuals even with Z_AB=0",
        ),
        base_row(
            contract_id="RZC2212_3_observed_descent",
            clause="Dq_Z=0 after elimination",
            exact_requirement="observed coframe, metric, connection, measure and readouts descend through visible variables only after Z is eliminated.",
            current_status="BLOCKED_NONCLAIM",
            missing_for_proof="1675 coframe/source/readout/boundary descent clauses remain unsigned",
            claim_effect="without descent, algebraic elimination can still be visible to PPN/R10/clocks/orbits",
        ),
        base_row(
            contract_id="RZC2212_4_invertible_algebraic_lock",
            clause="M_AB lock",
            exact_requirement="M_AB is nondegenerate or has a parent-owned constraint projector; null directions are gauge/constraint, not physical source modes.",
            current_status="MISSING_PARENT_SIGNATURE",
            missing_for_proof="M_AB sign/rank/eigenvectors and quotient basis",
            claim_effect="null or wrong-sign algebraic directions remain residual branches",
        ),
        base_row(
            contract_id="RZC2212_5_verdict",
            clause="rank-zero local-GR route",
            exact_requirement="M_AB lock + J_A=0 + B_A=0 + observed descent + CDB silence/bounds all close together.",
            current_status="PROMISING_ROUTE_NOT_CLAIMED",
            missing_for_proof="all above clauses in one parent branch",
            claim_effect="selected as next derivation route, no local-GR claim yet",
        ),
    ]


def branch_update_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            branch_id_local="BSU2212_0_strict_fixed_L0",
            previous_status="finite-range candidate held",
            update="RECLASSIFIED_AS_RANK_ZERO_ALGEBRAIC_SUBBRANCH",
            reason="strict branch has no Z_AB principal symbol; M_AB is algebraic Hessian only.",
            next_action="prove rank-zero source-current/boundary/descent theorem or retain algebraic residual",
        ),
        base_row(
            branch_id_local="BSU2212_1_live_CDB",
            previous_status="residual obstruction",
            update="ONLY_REMAINING_ZAB_HIDING_PLACE",
            reason="connection/domain/boundary/projector terms could contain derivative order or source leakage.",
            next_action="extract principal symbol from CDB or carry finite Q_cdb rows",
        ),
        base_row(
            branch_id_local="BSU2212_2_R10",
            previous_status="possible finite-range test lane",
            update="REJECTED_FOR_STRICT_BRANCH_HELD_FOR_LIVE_CDB_ONLY",
            reason="no lambda exists without a principal symbol; external R10 data cannot substitute for it.",
            next_action="do not run alpha(lambda) until live CDB produces Z_AB or another parent range owner",
        ),
        base_row(
            branch_id_local="BSU2212_3_PPN_or_local_GR",
            previous_status="blocked residual route",
            update="RANK_ZERO_SOURCE_CURRENT_ROUTE_SELECTED",
            reason="if no finite range exists, local GR must come from algebraic/source-current invisibility.",
            next_action="attempt J_A/B_A/Dq_Z theorem next",
        ),
        base_row(
            branch_id_local="BSU2212_4_verdict",
            previous_status="branch unselected",
            update="STRICT_BRANCH_SELECTED_FOR_CONSTRAINT_PROOF_NONCLAIM",
            reason="it is the cleanest derivable path after eliminating the false M_AB-to-lambda shortcut.",
            next_action="2213 rank-zero source-current identity or algebraic residual row",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2212_0_strict_symbol",
            gate="strict fixed-L0 branch has Z_AB=0",
            status="PASS_NONCLAIM",
            implication="finite-range R10 is rejected for the strict algebraic subbranch.",
        ),
        base_row(
            gate_id="CG2212_1_live_CDB_symbol",
            gate="live CDB principal symbol extracted",
            status="BLOCKED_NONCLAIM",
            implication="global branch selection remains open until CDB derivative order is known.",
        ),
        base_row(
            gate_id="CG2212_2_rank_zero_source",
            gate="rank-zero source-current theorem closes",
            status="BLOCKED_NONCLAIM",
            implication="J_A/B_A/descent clauses remain unsigned.",
        ),
        base_row(
            gate_id="CG2212_3_R10_score",
            gate="R10 alpha(lambda) can be scored",
            status="BLOCKED_NONCLAIM",
            implication="strict branch has no lambda; live CDB has no sourced lambda.",
        ),
        base_row(
            gate_id="CG2212_4_local_GR",
            gate="local GR/Newton reduction can be claimed",
            status="BLOCKED_NONCLAIM",
            implication="rank-zero route is promising but not proved.",
        ),
        base_row(
            gate_id="CG2212_5_GitHub",
            gate="public/github update",
            status="BLOCKED_NONCLAIM",
            implication="private derivation work only; no GitHub action.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2212_0_gain",
            decision="STRICT_L0_BRANCH_IS_RANK_ZERO",
            rationale="without derivative/CDB terms, the response-doublet branch is algebraic and has no finite-range principal symbol.",
            next_action="stop treating strict fixed-L0 branch as R10; test source-current constraint closure",
        ),
        base_row(
            decision_id="DEC2212_1_cdb",
            decision="CDB_IS_ONLY_REMAINING_ZAB_HIDING_PLACE",
            rationale="K_conn/K_domain/K_boundary/K_comm can still reintroduce derivative structure or source leakage.",
            next_action="keep CDB principal-symbol extraction as the live parallel blocker",
        ),
        base_row(
            decision_id="DEC2212_2_best_next",
            decision="RANK_ZERO_SOURCE_CURRENT_IDENTITY_NEXT",
            rationale="the clean GR-reduction path is now algebraic invisibility: M_AB lock plus J_A/B_A/Dq_Z silence.",
            next_action="derive J_A=0/B_A=0/descent or write algebraic residual row",
        ),
        base_row(
            decision_id="DEC2212_3_no_claim",
            decision="NO_R10_LOCAL_GR_CLAIM",
            rationale="2212 rejects a false finite-range route and opens the right proof, but does not close it.",
            next_action="keep all rows valid_for_claim=false until source-current theorem or finite residual bounds close",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2212_0_2213",
            selection_status="selected",
            target_file="2213-Y5-R2FR-rank-zero-source-current-identity-or-algebraic-residual-row.md",
            target_script="scripts/Y5_R2FR_rank_zero_source_current_identity_or_algebraic_residual_row_2213.py",
            objective="under the strict rank-zero fixed-L0 branch, try to prove M_AB Z^B=J_A has J_A=0, B_A=0, and observed descent Dq_Z=0; if not, stage the algebraic source residual row with units/source paths",
            success_condition="one rank-zero source-current clause is parent-signed or the algebraic residual/source coefficient row is explicitly staged nonclaim",
            do_not_do="do not resurrect R10 lambda for the strict branch, do not hide source-current terms, do not claim local GR/Newton, do not use GitHub action",
        ),
        base_row(
            route_id="NEXT2212_1_parallel_CDB",
            selection_status="held_parallel",
            target_file="2213b-Y5-R2FR-CDB-principal-symbol-extraction.md",
            target_script="scripts/Y5_R2FR_CDB_principal_symbol_extraction_2213b.py",
            objective="extract whether live K_conn/K_domain/K_boundary/K_comm contain a genuine Z_AB principal symbol or only finite residual/source leakage",
            success_condition="CDB derivative-order table separates kinetic Z_AB owner from source/boundary/projector residuals",
            do_not_do="do not delete CDB by strict algebraic closure",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["rank_zero_contract"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["strict_symbol_audit"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["cdb_symbol_queue"], BRANCH_COPIES["beta_docs"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        copied = False
        parse_ok = False
        count = 0
        if source.exists():
            shutil.copyfile(source, target)
            copied = True
            parse_ok, count, _ = csv_rows_parse(target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source),
                target_path=str(target),
                copied=copied,
                parse_ok=parse_ok,
                row_count=count,
            )
        )
    return rows


def validation_rows(
    source_rows: list[dict[str, Any]],
    strict_rows: list[dict[str, Any]],
    cdb_rows: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2212_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2212_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    strict_ok = any(row.get("audit_id") == "PSA2212_0_strict_branch_definition" and row.get("principal_symbol_result") == "Z_AB_strict = 0" for row in strict_rows)
    strict_ok = strict_ok and any(row.get("audit_id") == "PSA2212_4_strict_verdict" and "REJECTED" in str(row.get("principal_symbol_result")) for row in strict_rows)
    add("VAL2212_02_strict_symbol", strict_ok, "strict fixed-L0 branch classified as rank-zero/no finite-range principal symbol")

    cdb_ok = len(cdb_rows) == 5 and any(row.get("queue_id") == "CPS2212_4_live_verdict" and "HELD_OPEN" in str(row.get("current_status")) for row in cdb_rows)
    add("VAL2212_03_cdb_symbol_queue", cdb_ok, "CDB retained as only possible hidden Z_AB/derivative owner")

    rank_ok = any(row.get("contract_id") == "RZC2212_0_algebraic_euler" for row in rank_rows) and any(row.get("contract_id") == "RZC2212_5_verdict" and "PROMISING" in str(row.get("current_status")) for row in rank_rows)
    add("VAL2212_04_rank_zero_contract", rank_ok, "rank-zero algebraic/source-current contract written and not claimed")

    update_ok = any(row.get("branch_id_local") == "BSU2212_0_strict_fixed_L0" and "RANK_ZERO" in str(row.get("update")) for row in branch_rows_)
    update_ok = update_ok and any(row.get("branch_id_local") == "BSU2212_2_R10" and "REJECTED" in str(row.get("update")) for row in branch_rows_)
    add("VAL2212_05_branch_update", update_ok, "strict branch reclassified, R10 rejected for strict branch")

    claim_ok = any(row.get("gate_id") == "CG2212_3_R10_score" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2212_4_local_GR" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2212_06_claim_gate", claim_ok, "R10/local-GR claims remain blocked")

    decision_ok = any(row.get("decision") == "STRICT_L0_BRANCH_IS_RANK_ZERO" for row in decision_rows_) and any(row.get("decision") == "RANK_ZERO_SOURCE_CURRENT_IDENTITY_NEXT" for row in decision_rows_)
    add("VAL2212_07_decision", decision_ok, "decision ledger selects rank-zero source-current identity next")

    next_ok = any(row.get("route_id") == "NEXT2212_0_2213" and "rank-zero" in str(row.get("objective")) for row in next_rows)
    add("VAL2212_08_next_target", next_ok, "2213 rank-zero source-current identity selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2212_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2212_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, strict_rows, cdb_rows, rank_rows, branch_rows_, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2212_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    formalization_clean = not formalization_has_2212_artifacts()
    add("VAL2212_12_formalization_clean", formalization_clean, "formalization-workbench has no 2212 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2212_13_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2212_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2212 rejects finite-range R10 for the strict fixed-L0 algebraic branch, keeps live CDB as the only possible hidden Z_AB owner, and selects rank-zero source-current identity next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    strict_rows: list[dict[str, Any]],
    cdb_rows: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
    branch_rows_: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2212 - Y5/R2FR Principal Symbol ZAB Owner Or Rank-Zero Constraint Proof",
        "",
        "## Current Verdict",
        "",
        "2212 makes a real branch decision. In the strict fixed-`L0` algebraic response-doublet branch, there is no kinetic/principal-symbol owner for `Z_AB`. The branch has an algebraic Hessian `M_AB`, but no `-Z_AB Delta` term. Therefore the strict branch is rank-zero/algebraic, not finite-range Yukawa.",
        "",
        "So for this strict branch, R10 is the wrong language. The correct local-GR proof target is now:",
        "",
        "`M_AB Z^B = J_A`, plus `J_A=0`, `B_A=0`, and observed descent `Dq_Z=0`.",
        "",
        "The only caveat is live CDB: `K_conn`, `K_domain`, `K_boundary`, and `K_comm` may still hide derivative structure or source leakage. They remain a parallel blocker, not a reason to pretend the strict algebraic branch has a lambda.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Strict L0 Principal Symbol Audit",
        "",
        md_table(strict_rows, ["audit_id", "object", "principal_symbol_result", "derivation", "implication", "caveat", "passes_now", "valid_for_claim"]),
        "",
        "## CDB Principal Symbol Queue",
        "",
        md_table(cdb_rows, ["queue_id", "component", "possible_principal_symbol_role", "current_status", "evidence", "required_extraction", "branch_effect", "score_ready", "valid_for_claim"]),
        "",
        "## Rank-Zero Constraint Contract",
        "",
        md_table(rank_rows, ["contract_id", "clause", "exact_requirement", "current_status", "missing_for_proof", "claim_effect", "valid_for_claim"]),
        "",
        "## Branch Selection Update",
        "",
        md_table(branch_rows_, ["branch_id_local", "previous_status", "update", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decision_rows_, ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(copy_rows, ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation_rows_, ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Working Interpretation",
        "",
        "This is a useful leap forward. We are no longer trying to force the local branch to behave like a fifth-force model. The strict branch looks more like a constraint/elimination route: if the unwanted local variable is algebraically locked and source-silent, GR can emerge without needing a Yukawa suppression story. That is a better Grossmann-style path: derive the geometry, do not patch it.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    strict_rows = strict_symbol_audit_rows()
    cdb_rows = cdb_symbol_queue_rows()
    rank_rows = rank_zero_contract_rows()
    branch_rows_ = branch_update_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["strict_symbol_audit"], strict_rows),
        (OUTPUTS["cdb_symbol_queue"], cdb_rows),
        (OUTPUTS["rank_zero_contract"], rank_rows),
        (OUTPUTS["branch_update"], branch_rows_),
        (OUTPUTS["claim_gate"], claim_rows),
        (OUTPUTS["decision"], decision_rows_),
        (OUTPUTS["next_target"], next_rows),
    ]:
        write_csv(path, rows)

    copy_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branch_copies"], copy_rows)

    remove_pycache()
    validation_rows_ = validation_rows(
        source_rows,
        strict_rows,
        cdb_rows,
        rank_rows,
        branch_rows_,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        strict_rows,
        cdb_rows,
        rank_rows,
        branch_rows_,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
        validation_rows_,
    )

    remove_pycache()
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
