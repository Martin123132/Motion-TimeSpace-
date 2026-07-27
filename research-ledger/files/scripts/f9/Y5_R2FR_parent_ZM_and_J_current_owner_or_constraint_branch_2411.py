from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_PARENT_ZM_AND_J_CURRENT_OWNER_OR_CONSTRAINT_BRANCH_2411"
CHECKPOINT_ID = "2411"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2411-Y5-R2FR-parent-ZM-and-J-current-owner-or-constraint-branch.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2411_SOURCE_REGISTER.csv",
    "zmj_owner_audit": OUT / "P8_Y5_PARENT_QLOC_2411_ZMJ_OWNER_AUDIT.csv",
    "lemmas": OUT / "P8_Y5_PARENT_QLOC_2411_HESSIAN_RANGE_SOURCE_LEMMAS.csv",
    "branch_decision": OUT / "P8_Y5_PARENT_QLOC_2411_BRANCH_DECISION.csv",
    "contract": OUT / "P8_Y5_PARENT_QLOC_2411_COEFFICIENT_OR_ZERO_CONTRACT.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2411_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2411_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2411_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2411_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2411_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2411_ZMJ_CONSTRAINT_BRANCH_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2411_SOURCE_CURRENT_CONTRACT_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_ZMJ_OWNER_AUDIT_2411_NONCLAIM.csv",
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


def formalization_has_2411_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2411-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2411*",
        "*P8_Y5_BRR545_2411*",
        "*Y5_R2FR_parent_ZM_and_J_current_owner_or_constraint_branch_2411*",
        "*JR2411*",
        "*PARENT_QLOC_ZMJ_OWNER_AUDIT_2411*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2410_handoff",
            ROOT / "2410-Y5-R2FR-R10-q-loc-Yukawa-source-map-or-bound-curve-blocker.md",
            ["NEXT2410_0_selected", "SMG2410_4_q_loc_bridge_contract", "VAL2410_OVERALL"],
            "current chain selects parent Z/M/J ownership after tightening the R10 source-map gate.",
        ),
        (
            "2211_zm_demoter",
            ROOT / "2211-Y5-R2FR-parent-quadratic-residue-ZM-owner-or-constraint-branch.md",
            ["HVR2211_0_hessian_not_range", "ZMO2211_5_verdict", "VAL2211_OVERALL"],
            "prior proof that algebraic M_AB alone is not a Yukawa range owner.",
        ),
        (
            "2345_current_owner_normal_form",
            ROOT / "2345-Y5-R2FR-current-owner-normal-form-from-parent-variation-or-sourceGM-residual-first-row.md",
            ["CNF2345_1_hilbert_owner", "CNF2345_4_nonhilbert_split", "VAL2345_OVERALL"],
            "current-owner normal form: Hilbert source is a partial theorem; non-Hilbert/readout tails remain live.",
        ),
        (
            "1680_source_current_contract",
            ROOT / "1680-Y5-R2FR-source-current-owner-zero-theorem-or-finite-coefficient-contract.md",
            ["single_source_current_owner", "PROOF1680_6_verdict", "VAL1680_OVERALL"],
            "source-current zero theorem remains conditional; finite R_source contract is locked.",
        ),
        (
            "2207_response_doublet",
            ROOT / "2207-Y5-R2FR-Gamma-eff-metric-variation-or-first-q-loc-response-operator-row.md",
            ["Gamma_eff = Gamma0 + 1/2 M_AB", "KMR2207_2_Khat_identity", "VAL2207_OVERALL"],
            "response-doublet gives M_AB-shaped Hessian candidate but Khat identity remains unsigned.",
        ),
        (
            "2210_range_operator_csv",
            OUT / "P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_DERIVATION.csv",
            ["ROD2210_1_generalized_range_spectrum", "lambda_i=1/sqrt(mu_i^2)", "MISSING_PARENT_COEFFICIENTS"],
            "range owner law: lambda comes from parent Z/M spectrum if finite-range branch exists.",
        ),
        (
            "2345_current_residual_csv",
            OUT / "P8_Y5_PARENT_QLOC_2345_SOURCEGM_CURRENT_OWNER_RESIDUAL_FIRST_ROW.csv",
            ["RCO2345_0_schema", "MISSING_COMPONENT_VALUES", "local_GR"],
            "machine-readable current-owner residual row for non-Hilbert/sourceGM channels.",
        ),
        (
            "1680_zero_clauses_csv",
            OUT / "P8_Y5_PARENT_QLOC_1680_SOURCE_CURRENT_OWNER_ZERO_THEOREM_CLAUSES.csv",
            ["CL1680_4", "single_source_current_owner", "MISSING_CURRENT_OWNER"],
            "machine-readable source-current zero theorem clauses.",
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


def zmj_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            audit_id="ZMJ2411_0_M_hessian_candidate",
            object="M_AB / H_AB",
            owner_question="Does response-doublet Gamma_eff supply a parent Hessian or mass matrix?",
            current_result="CANDIDATE_ONLY",
            what_passes="Gamma_eff quadratic shape gives an algebraic M_AB target and double-zero structure.",
            what_fails="Gamma_eff is not fully parent-adopted; Khat identity, units, domain, source split, and live variation remain unsigned.",
            repair="derive H_AB := second_Z Gamma_eff on a parent-owned quotient basis with units/sign/source convention",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMJ2411_1_Z_principal_symbol",
            object="Z_AB / kinetic residue",
            owner_question="Does the same parent branch supply the principal symbol -Z_AB Delta on the physical quotient?",
            current_result="NOT_SOURCE_SIGNED",
            what_passes="range-owner law identifies exactly what Z_AB would mean.",
            what_fails="no physical quotient kinetic/principal-symbol owner is signed in the current chain; CDB/domain/boundary terms remain live.",
            repair="extract principal symbol from Gamma_eff/Khat/CDB parent branch or prove rank-zero/no finite-range branch",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMJ2411_2_J_hilbert_source",
            object="J_Hilbert",
            owner_question="Does ordinary matter supply a unique source current before readout?",
            current_result="PARTIAL_CONDITIONAL_THEOREM",
            what_passes="given common ordinary matter action and variation-before-readout, Hilbert/coframe source ownership is exact.",
            what_fails="common action syntax, source-blind object language, pre-action species weights, and readout stability are not fully parent-signed.",
            repair="parent-sign common matter action plus variation-before-readout and source-blind syntax, or retain finite source coefficients",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMJ2411_3_J_nonHilbert_tail",
            object="J_NH / boundary / readout / shadow connection",
            owner_question="Are all non-Hilbert source channels zero or bounded?",
            current_result="LIVE_RESIDUAL",
            what_passes="2345 isolates a strict epsilon_current_owner_NH_abs residual schema.",
            what_fails="spin/torsion, boundary, readout reentry, improvement, and shadow-connection projections have missing component values or zero proofs.",
            repair="prove P_source[J_NH]=0 channelwise or fill finite component-bound rows",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMJ2411_4_q_loc_bridge",
            object="q_loc to J_i",
            owner_question="Can q_loc be mapped into the eigenmode source current J_i?",
            current_result="BRIDGE_UNSIGNED",
            what_passes="2410 writes the legal bridge form J_i=S_i[I_div^{-1}(q_loc)] or q_loc=P_loc b_i[(L_iX_i)-J_i]+boundary.",
            what_fails="tau_i, inverse-divergence convention, T_GK owner, b_i, and boundary terms are not parent-owned.",
            repair="derive bridge maps from parent variation or demote q_loc to residual-bound-only",
            passes_now=False,
        ),
        base_row(
            audit_id="ZMJ2411_5_verdict",
            object="parent Z/M/J owner stack",
            owner_question="Can current MTS source-sign a finite-range R10 local branch?",
            current_result="NO_FULL_ZMJ_OWNER_SIGNED",
            what_passes="M candidate, range law, legal source-map contract, and partial Hilbert source theorem are all sharper.",
            what_fails="Z principal symbol, source-current silence, non-Hilbert projections, q_loc bridge, and full data curve remain incomplete.",
            repair="next target must choose principal-symbol Z_AB owner or rank-zero/source-current identity",
            passes_now=False,
        ),
    ]


def lemma_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            lemma_id="LEM2411_0_hessian_not_range",
            statement="An algebraic Hessian M_AB is not a finite-range Yukawa operator unless paired with a physical quotient kinetic/principal symbol Z_AB.",
            proof_sketch="Yukawa range is the inverse mass scale of a differential operator (-Z Delta+M). With only M, the equation is algebraic or constraint-like, not a propagating finite-range Green problem.",
            implication="response-doublet M_AB cannot be used as lambda evidence by itself.",
            status="PROVED_AS_GATE_LEMMA",
        ),
        base_row(
            lemma_id="LEM2411_1_hilbert_owner_not_full_source_silence",
            statement="Hilbert source ownership after a common matter action kills post-variation source rescaling but does not by itself silence pre-action weights or non-Hilbert currents.",
            proof_sketch="If weights or non-Hilbert channels enter before variation, the conserved source simply inherits them; Ward/Bianchi conservation does not force universality.",
            implication="J_A remains a partial theorem plus residual stack, not a closed local-GR source proof.",
            status="PROVED_AS_GATE_LEMMA",
        ),
        base_row(
            lemma_id="LEM2411_2_rank_zero_route",
            statement="If Z_AB has rank zero on the physical quotient, finite-range R10 is the wrong branch; local GR must come from algebraic elimination or source-current identity.",
            proof_sketch="No physical principal symbol means no finite-range Green kernel. The remaining equation is constraint/algebraic/boundary controlled, so suppression must be source silence or bounded residuals.",
            implication="rank-zero could be good news, but only if J_i and boundary/source tails close.",
            status="CONSTRAINT_BRANCH_OPENED",
        ),
        base_row(
            lemma_id="LEM2411_3_no_Bianchi_shortcut",
            statement="Bianchi/Ward compatibility is necessary but not enough to prove the residual source vanishes.",
            proof_sketch="A weighted sum of separately conserved currents can still be conserved. Conservation alone does not identify a universal source normalization.",
            implication="local GR needs source-current ownership plus no extra source slots, not conservation rhetoric.",
            status="GUARDRAIL_ACTIVE",
        ),
        base_row(
            lemma_id="LEM2411_4_verdict",
            statement="The finite-range local branch is not dead, but it is not score-ready; the cleaner derivation fork is Z_AB principal-symbol owner versus rank-zero/source-current identity.",
            proof_sketch="The current chain has an M candidate and partial J theorem, but no Z owner and no full source-current silence.",
            implication="continue deriving; do not publish or score R10 from this branch yet.",
            status="BRANCH_FORK_SHARPENED",
        ),
    ]


def branch_decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            branch_id_local="BD2411_0_finite_range_R10",
            old_status="candidate",
            new_status="DEMOTED_TO_COEFFICIENT_ACQUISITION",
            reason="M_AB candidate exists, but Z_AB principal symbol and J_i source owner are not signed.",
            required_next="Z_AB/M_AB/J_i coefficient rows with source paths, units, and domain, plus full bound curve",
            claim_effect="no R10 score",
        ),
        base_row(
            branch_id_local="BD2411_1_rank_zero_constraint",
            old_status="held possibility",
            new_status="PROMOTED_TO_NEXT_PROOF_FORK",
            reason="absence of Z_AB may be a clean GR route if the physical quotient is constraint/rank-zero and source currents vanish or are bounded.",
            required_next="principal-symbol rank proof plus J_H/J_NH/boundary source identity",
            claim_effect="could support local GR only after source silence closes",
        ),
        base_row(
            branch_id_local="BD2411_2_spectral_memory",
            old_status="possible",
            new_status="HELD_NONCLAIM",
            reason="if the parent gives a spectrum rather than finite matrices, R10 needs a spectral envelope, not one lambda.",
            required_next="spectral density, positive measure, and source/test weight envelope",
            claim_effect="no single-lambda score",
        ),
        base_row(
            branch_id_local="BD2411_3_source_residual_bound",
            old_status="fallback",
            new_status="RETAINED",
            reason="if zero proofs fail, non-Hilbert/source-current residuals need explicit finite coefficient rows.",
            required_next="epsilon_current_owner_NH_abs components or theorem-zero proofs",
            claim_effect="local-GR claim remains blocked but tests can become honest bounds",
        ),
        base_row(
            branch_id_local="BD2411_4_verdict",
            old_status="R10 route tempting",
            new_status="NO_BRANCH_SELECTED_YET",
            reason="current evidence sharpens the fork but does not source-sign Z, J, domain, q_loc bridge, or source silence.",
            required_next="2412 principal symbol Z_AB or rank-zero source-current identity",
            claim_effect="no local-GR/Newton/R10 claim",
        ),
    ]


def contract_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            contract_id="CON2411_0_Z_AB",
            symbol="Z_AB",
            needed_for="finite range lambda_i and ghost-free local operator",
            acceptable_evidence="principal symbol of a parent-owned physical quotient operator or rank-zero certificate",
            current_status="MISSING_SOURCE_SIGNED_OWNER",
            next_action="extract from Gamma_eff/Khat/CDB variation or prove absent/rank-zero",
        ),
        base_row(
            contract_id="CON2411_1_M_AB",
            symbol="M_AB",
            needed_for="mass/Hessian part of local branch",
            acceptable_evidence="second variation of parent Gamma_eff/action on same quotient basis as Z_AB",
            current_status="CANDIDATE_ONLY",
            next_action="sign units/domain/source convention and live Khat/action match",
        ),
        base_row(
            contract_id="CON2411_2_J_H",
            symbol="J_Hilbert",
            needed_for="ordinary matter source leg",
            acceptable_evidence="common matter action plus variation-before-readout and source-blind syntax",
            current_status="PARTIAL_CONDITIONAL_THEOREM",
            next_action="parent-sign common action/readout order or retain finite source weights",
        ),
        base_row(
            contract_id="CON2411_3_J_NH",
            symbol="J_NH",
            needed_for="non-Hilbert/boundary/readout source silence",
            acceptable_evidence="channelwise zero proof or finite epsilon_current_owner_NH_abs component rows",
            current_status="LIVE_RESIDUAL",
            next_action="prove P_source[J_NH]=0 or fill component-bound pack",
        ),
        base_row(
            contract_id="CON2411_4_domain",
            symbol="Dom(L_AB)",
            needed_for="self-adjoint spectrum and no hidden boundary source",
            acceptable_evidence="quotient/domain/no-flux theorem or explicit boundary charge row",
            current_status="MISSING_DOMAIN_CERTIFICATE",
            next_action="derive boundary/domain descent before any spectrum claim",
        ),
        base_row(
            contract_id="CON2411_5_q_loc_bridge",
            symbol="S_i[I_div^{-1}(q_loc)]",
            needed_for="mapping q_loc into source current J_i",
            acceptable_evidence="parent-owned inverse-divergence/T_GK/tau_i map with units and boundary terms",
            current_status="MISSING_BRIDGE_OWNER",
            next_action="derive bridge or demote q_loc to residual-bound-only",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2411_0_M_candidate", gate="M_AB Hessian candidate exists", status="PASS_NONCLAIM", implication="useful target, not a range by itself"),
        base_row(gate_id="CG2411_1_Z_owner", gate="Z_AB principal-symbol owner exists", status="BLOCKED_NONCLAIM", implication="finite range remains unselected"),
        base_row(gate_id="CG2411_2_J_owner", gate="source current J_i is parent-owned and source-silent or bounded", status="BLOCKED_NONCLAIM", implication="q_loc/R10 source map remains unscored"),
        base_row(gate_id="CG2411_3_rank_zero_constraint", gate="rank-zero/source-current identity closes", status="BLOCKED_NONCLAIM", implication="constraint route is promising but unproved"),
        base_row(gate_id="CG2411_4_R10_score", gate="R10 alpha(lambda) can be scored", status="BLOCKED_NONCLAIM", implication="Z/J/charges/full curve missing"),
        base_row(gate_id="CG2411_5_local_GR_Newton", gate="local GR/Newton reduction follows", status="BLOCKED_NONCLAIM", implication="operator/source closure still missing"),
        base_row(gate_id="CG2411_6_GitHub", gate="public/GitHub update", status="BLOCKED_PRIVATE", implication="private derivation work only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2411_0_gain",
            decision="ZMJ_FORK_SHARPENED",
            rationale="The exact local obstruction is now Z principal-symbol ownership plus J source-current closure, not vague coupling anxiety.",
            next_action="attack Z_AB rank/principal symbol and source-current identity together",
        ),
        base_row(
            decision_id="DEC2411_1_demote",
            decision="FINITE_RANGE_R10_DEMOTED_UNTIL_ZJ_EXISTS",
            rationale="M_AB candidate plus partial Hilbert J theorem is insufficient for a finite-range R10 score.",
            next_action="keep R10 as coefficient-acquisition/data-parallel only",
        ),
        base_row(
            decision_id="DEC2411_2_promising_route",
            decision="RANK_ZERO_CONSTRAINT_ROUTE_PROMOTED",
            rationale="If Z_AB is absent on the physical quotient, the clean local-GR route is algebraic/constraint source silence rather than Yukawa suppression.",
            next_action="derive principal-symbol rank and J_H/J_NH/boundary source identity",
        ),
        base_row(
            decision_id="DEC2411_3_no_claim",
            decision="NO_GITHUB_NO_LOCAL_CLAIM",
            rationale="This checkpoint is important private derivation discipline, not public evidence.",
            next_action="keep all rows valid_for_claim=false",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2411_0_selected",
            selection_status="selected",
            target_file="2412-Y5-R2FR-principal-symbol-ZAB-or-rank-zero-source-current-identity.md",
            target_script="scripts/Y5_R2FR_principal_symbol_ZAB_or_rank_zero_source_current_identity_2412.py",
            objective="extract the principal symbol of the Gamma_eff/Khat/CDB branch; either source-sign physical Z_AB or prove rank-zero and derive the required source-current identity",
            success_condition="Z_AB owner row becomes source-signed nonclaim, or finite-range R10 is rejected for this branch and a rank-zero plus J_H/J_NH source identity contract is written",
            do_not_do="do not infer Z from M, ignore non-Hilbert source tails, claim R10/local GR, or use GitHub",
        ),
        base_row(
            route_id="NEXT2411_1_fallback",
            selection_status="held_fallback",
            target_file="2412b-Y5-R2FR-current-owner-residual-component-bound-pack.md",
            target_script="scripts/Y5_R2FR_current_owner_residual_component_bound_pack_2412b.py",
            objective="if source-current zero proof fails, fill finite component-bound rows for epsilon_current_owner_NH_abs",
            success_condition="component rows have units, source paths, arena links, and remain nonclaim until numeric",
            do_not_do="do not hide source residuals inside measured GM or q_loc",
        ),
    ]


def copy_branch_rows(contract: list[dict[str, Any]], branch_decision: list[dict[str, Any]], audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["branch_decision"], BRANCH_COPIES["queue"], branch_decision),
        ("branch_wep", OUTPUTS["contract"], BRANCH_COPIES["branch_wep"], contract),
        ("beta_docs", OUTPUTS["zmj_owner_audit"], BRANCH_COPIES["beta_docs"], audit),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=str(source_path),
                target_path=str(target_path),
                copied=target_path.exists(),
                parse_ok=parse_ok,
                row_count=row_count,
                parse_detail=parse_detail,
            )
        )
    return rows


def all_generated_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, value in data.items():
        if key != "validation":
            rows.extend(value)
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = data["source_register"]
    rows.append(
        base_row(validation_id="VAL2411_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist")
    )
    rows.append(
        base_row(validation_id="VAL2411_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found")
    )

    audit_text = " ".join(str(row) for row in data["zmj_owner_audit"])
    rows.append(
        base_row(validation_id="VAL2411_02_zmj_audit", status="PASS" if "NO_FULL_ZMJ_OWNER_SIGNED" in audit_text and "LIVE_RESIDUAL" in audit_text else "FAIL", detail="Z/M/J stack audited without promotion")
    )

    lemma_text = " ".join(str(row) for row in data["lemmas"])
    rows.append(
        base_row(validation_id="VAL2411_03_gate_lemmas", status="PASS" if "Hessian" in lemma_text and "Hilbert source ownership" in lemma_text and "rank zero" in lemma_text else "FAIL", detail="hessian-not-range, source-silence, and rank-zero lemmas recorded")
    )

    branch_text = " ".join(str(row) for row in data["branch_decision"])
    rows.append(
        base_row(validation_id="VAL2411_04_branch_decision", status="PASS" if "DEMOTED_TO_COEFFICIENT_ACQUISITION" in branch_text and "PROMOTED_TO_NEXT_PROOF_FORK" in branch_text else "FAIL", detail="finite-range R10 demoted and rank-zero fork promoted")
    )

    contract = data["contract"]
    rows.append(
        base_row(validation_id="VAL2411_05_contract_rows", status="PASS" if len(contract) == 6 and all("MISSING" in row["current_status"] or "CANDIDATE" in row["current_status"] or "PARTIAL" in row["current_status"] or "LIVE" in row["current_status"] for row in contract) else "FAIL", detail=f"contract rows={len(contract)} all nonclaim/missing-partial-live")
    )

    claim = data["claim_gate"]
    rows.append(
        base_row(validation_id="VAL2411_06_claim_gates", status="PASS" if all(not row["valid_for_claim"] and not row["claim_allowed"] for row in claim) else "FAIL", detail="R10/local-GR/GitHub gates remain blocked")
    )

    decision_text = " ".join(str(row) for row in data["decision"])
    rows.append(
        base_row(validation_id="VAL2411_07_decision", status="PASS" if "ZMJ_FORK_SHARPENED" in decision_text and "NO_GITHUB_NO_LOCAL_CLAIM" in decision_text else "FAIL", detail="decision ledger records gain without public/local claim")
    )

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(
        base_row(validation_id="VAL2411_08_next_target", status="PASS" if "2412-Y5-R2FR-principal-symbol-ZAB-or-rank-zero-source-current-identity.md" in next_text else "FAIL", detail="2412 principal-symbol/rank-zero source-current target selected")
    )

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2411_09_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    branch_copies = data["branch_copies"]
    rows.append(
        base_row(validation_id="VAL2411_10_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in branch_copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in branch_copies))
    )

    generated = all_generated_rows(data)
    rows.append(
        base_row(validation_id="VAL2411_11_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false")
    )
    rows.append(
        base_row(validation_id="VAL2411_12_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2411_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work")
    )
    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(
        base_row(validation_id="VAL2411_OVERALL", status=overall, detail="2411 sharpens the parent Z/M/J fork, keeps finite-range R10 demoted, promotes principal-symbol Z_AB or rank-zero source-current identity as the next proof target")
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2411_OVERALL")
    lines = [
        "# 2411 - Y5/R2FR Parent ZM And J Current Owner Or Constraint Branch",
        "",
        "## Result",
        "",
        "2411 says the quiet bit out loud: the local branch now has a clean two-lock throat.",
        "",
        "1. `M_AB` from the response-doublet is only a Hessian-shaped candidate. It is not a range unless the parent also supplies a physical quotient principal symbol `Z_AB`.",
        "2. `J_A` has a real partial theorem: Hilbert/coframe variation owns the source after a common matter action is fixed. But that does not silence pre-action source weights, non-Hilbert currents, boundary/improvement terms, readout reentry, or shadow-connection source channels.",
        "",
        "So finite-range R10 is demoted until `Z_AB` and `J_A` are signed together. The better next proof fork is: find the principal symbol, or prove rank-zero/constraint plus source-current identity. That route is closer to derived local GR than forcing a fifth-force score.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Z/M/J Owner Audit",
        "",
        md_table(data["zmj_owner_audit"], ["audit_id", "object", "owner_question", "current_result", "what_passes", "what_fails", "repair", "passes_now", "valid_for_claim"]),
        "",
        "## Hessian Range Source Lemmas",
        "",
        md_table(data["lemmas"], ["lemma_id", "statement", "proof_sketch", "implication", "status", "valid_for_claim"]),
        "",
        "## Branch Decision",
        "",
        md_table(data["branch_decision"], ["branch_id_local", "old_status", "new_status", "reason", "required_next", "claim_effect", "valid_for_claim"]),
        "",
        "## Coefficient Or Zero Contract",
        "",
        md_table(data["contract"], ["contract_id", "symbol", "needed_for", "acceptable_evidence", "current_status", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(data["claim_gate"], ["gate_id", "gate", "status", "implication", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(data["decision"], ["decision_id", "decision", "rationale", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(data["next_target"], ["route_id", "selection_status", "target_file", "target_script", "objective", "success_condition", "do_not_do", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(data["branch_copies"], ["copy_id", "source_path", "target_path", "copied", "parse_ok", "row_count", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(data["validation"], ["validation_id", "status", "detail", "valid_for_claim", "claim_allowed"]),
        "",
        "## Practical Status",
        "",
        "This is not circling. It is the fork we needed: either the local branch has a real differential operator and source current, or it is a constraint/source-silence route. The former can become R10-testable; the latter can become a cleaner GR-limit derivation. Both are better than pretending `M_AB` or `q_loc` alone already did the job.",
        "",
        f"Validation overall: `{overall['status']}`.",
    ]
    DOC.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    BETA_DOCS.mkdir(parents=True, exist_ok=True)

    data: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register_rows(),
        "zmj_owner_audit": zmj_owner_audit_rows(),
        "lemmas": lemma_rows(),
        "branch_decision": branch_decision_rows(),
        "contract": contract_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["zmj_owner_audit"], data["zmj_owner_audit"])
    write_csv(OUTPUTS["lemmas"], data["lemmas"])
    write_csv(OUTPUTS["branch_decision"], data["branch_decision"])
    write_csv(OUTPUTS["contract"], data["contract"])
    write_csv(OUTPUTS["claim_gate"], data["claim_gate"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["contract"], data["branch_decision"], data["zmj_owner_audit"])
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
