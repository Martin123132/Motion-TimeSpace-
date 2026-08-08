from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "2216"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2216-Y5-R2FR-parent-Hessian-signature-extraction-or-null-bound-rows.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2216_SOURCE_REGISTER.csv",
    "signature_extraction": OUT / "P8_Y5_PARENT_QLOC_2216_PARENT_HESSIAN_SIGNATURE_EXTRACTION.csv",
    "hessian_contract": OUT / "P8_Y5_PARENT_QLOC_2216_HESSIAN_DERIVATION_CONTRACT.csv",
    "null_bound_rows": OUT / "P8_Y5_PARENT_QLOC_2216_NULL_BOUND_ACQUISITION_ROWS.csv",
    "evidence_map": OUT / "P8_Y5_PARENT_QLOC_2216_SIGNATURE_EVIDENCE_MAP.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_2216_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2216_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2216_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2216_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2216_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2216_PARENT_HESSIAN_SIGNATURE_OR_NULL_BOUNDS_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2216_NULL_BOUND_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_HESSIAN_SIGNATURE_2216_NONCLAIM.csv",
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


def formalization_has_2216_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2216-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2216*",
        "*P8_Y5_BRR545_2216*",
        "*Y5_R2FR_parent_Hessian_signature_extraction_or_null_bound_rows_2216*",
        "*JR2216*",
        "*PARENT_QLOC_HESSIAN_SIGNATURE_2216*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "2215_handoff",
            ROOT / "2215-Y5-R2FR-MAB-lock-signature-or-pseudoinverse-residual-branch.md",
            ["NEXT2215_0_2216", "PINV2215_0_general_solution", "VAL2215_OVERALL"],
            "2215 selects parent Hessian signature extraction or null-bound rows.",
        ),
        (
            "2215_signature_rows",
            OUT / "P8_Y5_PARENT_QLOC_2215_MAB_SIGNATURE_ACQUISITION_ROWS.csv",
            ["MSA2215_0_parent_density", "MSA2215_8_Khat_identity", "MISSING_PARENT_INPUT"],
            "machine-readable list of missing M_AB parent-signature premises.",
        ),
        (
            "1010_action_guard",
            ROOT / "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            ["GKT1010_0_variational_route", "CG1010_1_metric_response", "V1010_SUMMARY"],
            "Gamma/Khat action-existence guardrail: route exact, current claim blocked.",
        ),
        (
            "gamma_owner_candidates",
            OUT / "P8_GAMMA_OWNER_CANDIDATE_ACTION.csv",
            ["GO516_A_response_doublet_quadratic_density", "GO516_D_residual_bound_runner", "best_candidate_not_current_MTS_derived"],
            "candidate Gamma_eff action routes, including response doublet.",
        ),
        (
            "gk_metric_response_audit",
            OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
            ["MA515_0_Gamma_scalar_density_owner", "MA515_1_Khat_metric_response", "MA515_6_units_and_readout"],
            "audit showing Gamma scalar density owner, Khat response and units are not signed.",
        ),
        (
            "response_doublet_contract",
            OUT / "P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            ["RD516_1_even_scalar_density", "RD516_3_positive_operator", "RD516_4_zero_odd_source"],
            "response-doublet clauses: even density candidate, positive operator and source zero are conditional.",
        ),
        (
            "response_doublet_variation",
            OUT / "P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            ["AV517_1_scalar_density", "AV517_4_Euler_equation", "blocked_by_source_current_rows"],
            "variation rows: formal double-zero exists, Euler/source closure blocked.",
        ),
        (
            "gk_action_candidates",
            OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
            ["GK514_A_metric_response_scalar_density", "GK514_D_residual_branch", "fallback_required"],
            "stress action candidates and fallback residual branch.",
        ),
        (
            "2211_zm_audit",
            OUT / "P8_Y5_PARENT_QLOC_2211_ZM_OWNER_AUDIT.csv",
            ["ZMO2211_1_M_from_response_doublet", "ZMO2211_5_verdict", "ALGEBRAIC_HESSIAN_CANDIDATE_ONLY"],
            "M_AB is a candidate Hessian only, not parent-signed.",
        ),
        (
            "2215_null_branch",
            OUT / "P8_Y5_PARENT_QLOC_2215_PSEUDOINVERSE_NULL_BRANCH.csv",
            ["PINV2215_0_general_solution", "PINV2215_2_visible_null", "M^+"],
            "null/pseudoinverse fallback branch from 2215.",
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


def signature_extraction_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            clause_id="PHS2216_0_candidate_density_shape",
            parent_signature="response-doublet candidate density shape",
            extraction_result="FOUND_CONDITIONAL_SHAPE",
            evidence="GO516_A and AV517_1 write Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4).",
            what_this_signs="formal Hessian shape only",
            what_remains_unsigned="parent action owner, field basis, units, Khat identity, source/boundary closure.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_1_parent_density_owner",
            parent_signature="Gamma_eff is an accepted parent scalar density/action term",
            extraction_result="NOT_FOUND_CURRENT_CORPUS",
            evidence="MA515_0 and GKT1010_0 keep this as candidate route, not current MTS derivation.",
            what_this_signs="would turn M_AB into a second variation of an action density",
            what_remains_unsigned="explicit field content, metric dependence, units, boundary convention.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_2_Khat_identity",
            parent_signature="K_hat equals K_metric[Gamma_eff] under one convention",
            extraction_result="NOT_MATCHED_CURRENT_CORPUS",
            evidence="MA515_1, KMR2207_2 and CG1010_1 block the metric-response match.",
            what_this_signs="would connect the formal Hessian to current q_loc/Khat branch",
            what_remains_unsigned="tensor structure comparison including derivative and boundary terms.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_3_Z_basis",
            parent_signature="Z^A quotient basis covers physical local residual directions",
            extraction_result="PARTIAL_FORMAL_DOUBLET_ONLY",
            evidence="AV517_0 defines Z=(R_+-R_-)/2 conditionally; RD516_0 says component coverage is partial.",
            what_this_signs="would define the Hessian coordinates",
            what_remains_unsigned="map to every physical local residual component and q_loc/PPN/source directions.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_4_pairing_units",
            parent_signature="inner product, measure and units for Z, M and source S",
            extraction_result="NOT_FOUND_CURRENT_CORPUS",
            evidence="MA515_6, ZMC2211_1 and CM2214_0 all require units/readout normalization.",
            what_this_signs="would make M^+S dimensionally meaningful",
            what_remains_unsigned="stress-density units, Z units, source pairing, arena normalization.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_5_self_adjoint_domain",
            parent_signature="self-adjoint local domain and boundary condition for M_AB",
            extraction_result="NOT_FOUND_CURRENT_CORPUS",
            evidence="ZMC2211_2 and RD516_6 keep domain/boundary no-flux open.",
            what_this_signs="would legalize spectral split and integration-by-parts identities",
            what_remains_unsigned="compact collar boundary, projector commutator, source-worldtube edge terms.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_6_rank_sign",
            parent_signature="rank/sign/coercivity theorem for M_AB on physical directions",
            extraction_result="NOT_FOUND_CURRENT_CORPUS",
            evidence="RD516_3 and LOCK2215_4 mark positivity/coercivity as formal candidate only.",
            what_this_signs="would decide inverse, pseudoinverse, negative mode or flat branch",
            what_remains_unsigned="spectral theorem, eigenbasis, lower bound c>0 or null/negative split.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_7_null_projector",
            parent_signature="P_null and gauge/constraint status",
            extraction_result="NOT_FOUND_CURRENT_CORPUS",
            evidence="PINV2215_1 and MSA2215_5 require P_null and source compatibility.",
            what_this_signs="would decide whether Z_null is gauge, constraint or physical",
            what_remains_unsigned="P_null construction, Dq_Z/L_null visibility, source orthogonality.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_8_source_compatibility",
            parent_signature="P_null S=0 or finite null forcing rows",
            extraction_result="NOT_FOUND_CURRENT_CORPUS",
            evidence="RD516_4, AV517_4, 1010 and 2215 all keep source-current/boundary forcing open.",
            what_this_signs="would prevent null directions from being driven by matter or boundary terms",
            what_remains_unsigned="J_A, B_A, CDB_A and R_src/readout projections onto null space.",
            parent_signed_now=False,
        ),
        base_row(
            clause_id="PHS2216_9_verdict",
            parent_signature="full parent Hessian signature",
            extraction_result="NOT_PARENT_SIGNED_CURRENT_CORPUS",
            evidence="only the candidate density shape is found, and it is conditional/nonclaim.",
            what_this_signs="would allow G_alg=M^{-1} or a controlled M^+ branch",
            what_remains_unsigned="all operational lock premises beyond shape.",
            parent_signed_now=False,
        ),
    ]


def hessian_contract_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            contract_id="HDC2216_0_second_variation_definition",
            contract_piece="parent Hessian definition",
            formula="H_AB := delta^2 Gamma_eff / delta Z^A delta Z^B |_{Z=0}",
            required_premises="Gamma_eff parent density; Z basis; pairing/units; domain/boundary convention",
            current_status="FORMAL_ONLY_NOT_PARENT_SIGNED",
            consequence_if_closed="H_AB can be identified with M_AB under a declared normalization.",
        ),
        base_row(
            contract_id="HDC2216_1_lock_operator",
            contract_piece="algebraic lock operator",
            formula="<X,M Y>_loc = integral_D sqrt(g) X^A H_AB Y^B",
            required_premises="local measure, field-space pairing, self-adjoint domain, boundary no-flux or retained boundary rows",
            current_status="MISSING_PAIRING_DOMAIN",
            consequence_if_closed="spectral split and coercivity tests become meaningful.",
        ),
        base_row(
            contract_id="HDC2216_2_spectral_split",
            contract_piece="positive/null/negative decomposition",
            formula="Z = Z_+ + Z_0 + Z_- with M Z_0=0 and <Z_+,MZ_+> >= c||Z_+||^2",
            required_premises="rank/sign theorem and null projector",
            current_status="MISSING_SPECTRAL_THEOREM",
            consequence_if_closed="inverse branch, pseudoinverse branch, or instability branch can be selected.",
        ),
        base_row(
            contract_id="HDC2216_3_null_source_gate",
            contract_piece="null compatibility",
            formula="P_null^B(J_B+B_B+C_B^CDB+R_B)=0",
            required_premises="P_null, source split, boundary/CDB/readout projections",
            current_status="MISSING_NULL_SOURCE_PROJECTION",
            consequence_if_closed="null directions can be called gauge/constraint rather than physical residual.",
        ),
        base_row(
            contract_id="HDC2216_4_observable_null_gate",
            contract_piece="null visibility",
            formula="L_null,A^I Z_null^A = 0 for all local arenas I, or finite bound rows exist",
            required_premises="arena projection maps, Dq_Z/readout descent, units",
            current_status="MISSING_L_NULL",
            consequence_if_closed="M^+ branch can be bounded or collapsed in observed tests.",
        ),
        base_row(
            contract_id="HDC2216_5_verdict",
            contract_piece="2216 Hessian contract verdict",
            formula="M_AB cannot yet be upgraded from candidate Hessian to parent lock.",
            required_premises="all HDC2216_0 through HDC2216_4",
            current_status="CONTRACT_WRITTEN_EXTRACTION_FAILED_CURRENT_CORPUS",
            consequence_if_closed="local strict branch can move toward GR/Newton reduction without plateau axiom.",
        ),
    ]


def null_bound_rows() -> list[dict[str, Any]]:
    specs = [
        (
            "NBR2216_0_parent_density",
            "Gamma_eff parent density/action owner",
            "GO516_A;GK514_A;GKT1010_0;MA515_0",
            "construct explicit scalar density with field content, metric dependence, units and boundary convention",
            "blocks H_AB definition",
        ),
        (
            "NBR2216_1_Khat_identity",
            "K_hat metric-response identity",
            "MA515_1;KMR2207_2;CG1010_1",
            "compute K_metric[Gamma_eff] and compare with existing K_hat including derivative/boundary terms",
            "blocks connection to q_loc branch",
        ),
        (
            "NBR2216_2_Z_basis",
            "physical Z basis and residual component map",
            "AV517_0;RD516_0;RD516_5",
            "map exchange-odd coordinates to q_loc/PPN/source/readout residual components",
            "blocks meaning of M_AB directions",
        ),
        (
            "NBR2216_3_pairing_units",
            "field-space pairing and units",
            "MA515_6;ZMC2211_1;CM2214_0",
            "declare local inner product, source pairing and dimensional normalization",
            "blocks M^+S numeric rows",
        ),
        (
            "NBR2216_4_domain",
            "self-adjoint domain/boundary condition",
            "ZMC2211_2;RD516_6;PHS2216_5",
            "derive compact collar domain or retain boundary charge rows",
            "blocks spectral theorem",
        ),
        (
            "NBR2216_5_rank_sign",
            "rank/sign/coercivity spectrum",
            "RD516_3;LOCK2215_4;HDC2216_2",
            "derive eigenvalue/rank theorem or classify positive/null/negative branches",
            "blocks inverse vs pseudoinverse choice",
        ),
        (
            "NBR2216_6_null_projector",
            "P_null and gauge/constraint status",
            "PINV2215_1;LOCK2215_5;HDC2216_3",
            "construct P_null and prove null directions gauge/constraint or physical",
            "blocks null residual demotion",
        ),
        (
            "NBR2216_7_null_source",
            "P_null S source compatibility",
            "RD516_4;AV517_4;PINV2215_1",
            "project J/B/CDB/R_src onto null space and prove zero or bound",
            "blocks consistency of MZ=S",
        ),
        (
            "NBR2216_8_L_null",
            "arena null visibility L_null",
            "PINV2215_2;ANP2215_0..6;HDC2216_4",
            "derive L_null for Newton/PPN/R10/WEP/clock/EM/orbital/R11 or bound each arena",
            "blocks local observability verdict",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for bound_id, missing_object, evidence_sources, required_action, blocks in specs:
        rows.append(
            base_row(
                bound_id=bound_id,
                missing_object=missing_object,
                evidence_sources=evidence_sources,
                required_action=required_action,
                blocks=blocks,
                current_value="MISSING_PARENT_INPUT",
                current_units="MISSING_UNITS_OR_NOT_APPLICABLE",
                numeric_bound="MISSING_SOURCE_BACKED_BOUND",
                status="NONCLAIM_ACQUISITION_ROW",
                score_ready=False,
                valid_prediction_row=False,
            )
        )
    return rows


def evidence_map_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            evidence_id="EVM2216_0_best_found",
            premise="best current positive evidence",
            source="GO516_A + AV517_1 + 2207",
            finding="response-doublet quadratic density shape exists conditionally",
            promotion_status="SHAPE_ONLY_NOT_PARENT_SIGNATURE",
            next_use="seed a parent-density construction attempt",
        ),
        base_row(
            evidence_id="EVM2216_1_hard_block",
            premise="parent action owner",
            source="MA515_0 + GKT1010_0",
            finding="no accepted scalar density owner with units/boundary convention",
            promotion_status="BLOCKS_HESSIAN",
            next_use="build Gamma_eff density explicitly or retain residual branch",
        ),
        base_row(
            evidence_id="EVM2216_2_hard_block",
            premise="Khat identity",
            source="MA515_1 + KMR2207_2 + CG1010_1",
            finding="K_hat is not matched to K_metric[Gamma_eff]",
            promotion_status="BLOCKS_CURRENT_QLOC_CONNECTION",
            next_use="metric variation comparison target for 2217",
        ),
        base_row(
            evidence_id="EVM2216_3_hard_block",
            premise="source/null compatibility",
            source="RD516_4 + AV517_4 + 1010 source-boundary gaps",
            finding="J_A/B_A/source terms remain live",
            promotion_status="BLOCKS_NULL_GAUGE_DEMOTION",
            next_use="project source terms onto P_null once P_null exists",
        ),
        base_row(
            evidence_id="EVM2216_4_verdict",
            premise="parent Hessian extraction",
            source="combined 2216 audit",
            finding="no M_AB parent-signature premise is closed beyond formal shape",
            promotion_status="NULL_BOUND_ROWS_REQUIRED",
            next_use="2217 response-doublet parent density and Khat identity construction",
        ),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            gate_id="CG2216_0_shape",
            gate="response-doublet Hessian shape found",
            status="PASS_NONCLAIM",
            reason="candidate density shape exists but is conditional.",
        ),
        base_row(
            gate_id="CG2216_1_parent_Hessian",
            gate="M_AB parent Hessian signature extracted",
            status="BLOCKED_NONCLAIM",
            reason="parent density, Khat identity, basis, units, domain, spectrum and null/source compatibility remain unsigned.",
        ),
        base_row(
            gate_id="CG2216_2_null_bound_rows",
            gate="null-bound acquisition rows emitted",
            status="PASS_NONCLAIM",
            reason="every missing spectral/null premise now has evidence-backed acquisition row.",
        ),
        base_row(
            gate_id="CG2216_3_score_ready",
            gate="any local/null bound score-ready",
            status="BLOCKED_NONCLAIM",
            reason="all values and numeric bounds are missing parent inputs.",
        ),
        base_row(
            gate_id="CG2216_4_local_GR_Newton",
            gate="local GR/Newton reduction claim",
            status="BLOCKED_NONCLAIM",
            reason="M_AB is not a parent lock and null visibility remains live.",
        ),
        base_row(
            gate_id="CG2216_5_GitHub",
            gate="GitHub/public update",
            status="BLOCKED_NONCLAIM",
            reason="private derivation checkpoint only.",
        ),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            decision_id="DEC2216_0_gain",
            decision="HESSIAN_SIGNATURE_AUDIT_COMPLETED",
            rationale="the exact missing parent-Hessian premises are mapped to existing evidence sources.",
            next_action="use the evidence map instead of re-litigating generic M_AB lock language.",
        ),
        base_row(
            decision_id="DEC2216_1_failure",
            decision="NO_PARENT_HESSIAN_SIGNATURE_FOUND",
            rationale="only conditional response-doublet shape exists; action owner and Khat identity fail.",
            next_action="retain M^+/null rows and do not promote local GR/Newton.",
        ),
        base_row(
            decision_id="DEC2216_2_best_next",
            decision="GAMMA_DENSITY_AND_KHAT_IDENTITY_NEXT",
            rationale="without an accepted Gamma_eff density and metric-response identity, later spectral work has no parent object to diagonalize.",
            next_action="2217 should build or reject the response-doublet parent density and Khat match.",
        ),
        base_row(
            decision_id="DEC2216_3_scope",
            decision="NULL_BOUNDS_ARE_ACQUISITION_NOT_EVIDENCE",
            rationale="the null-bound rows are organized missing inputs, not measurements or passes.",
            next_action="keep all generated rows nonclaim and private.",
        ),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(
            route_id="NEXT2216_0_2217",
            selection_status="selected",
            target_file="2217-Y5-R2FR-response-doublet-parent-density-and-Khat-identity-construction.md",
            target_script="scripts/Y5_R2FR_response_doublet_parent_density_and_Khat_identity_construction_2217.py",
            objective="construct or reject the response-doublet parent scalar density Gamma_eff with field content, metric dependence, units and boundary convention, then compare its metric variation to K_hat under one sign convention.",
            success_condition="Gamma_eff density owner or Khat identity gets parent-signed, or the mismatch is written as an explicit residual obstruction with source-backed rows.",
            do_not_do="do not assume K_hat identity by notation, do not claim local GR/Newton, do not use GitHub.",
        ),
        base_row(
            route_id="NEXT2216_1_Z_basis_parallel",
            selection_status="held_parallel",
            target_file="2217b-Y5-R2FR-Z-basis-pairing-units-and-component-map.md",
            target_script="scripts/Y5_R2FR_Z_basis_pairing_units_and_component_map_2217b.py",
            objective="derive the Z^A quotient basis, pairing, units and map to q_loc/PPN/source/readout components.",
            success_condition="Z basis and units become source-signed or acquisition rows become arena-specific.",
            do_not_do="do not infer physical component coverage from formal doublet notation.",
        ),
        base_row(
            route_id="NEXT2216_2_null_parallel",
            selection_status="held_parallel",
            target_file="2217c-Y5-R2FR-null-projector-source-compatibility-and-Lnull-bounds.md",
            target_script="scripts/Y5_R2FR_null_projector_source_compatibility_and_Lnull_bounds_2217c.py",
            objective="derive P_null, P_null S, and L_null arena projections or retain finite null-bound rows.",
            success_condition="null sector is gauge/constraint or finite visible residual rows are ready for future bounds.",
            do_not_do="do not call null directions gauge before P_null and L_null are derived.",
        ),
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("queue", OUTPUTS["null_bound_rows"], BRANCH_COPIES["queue"]),
        ("branch_wep", OUTPUTS["signature_extraction"], BRANCH_COPIES["branch_wep"]),
        ("beta_docs", OUTPUTS["hessian_contract"], BRANCH_COPIES["beta_docs"]),
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
    signature_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    null_rows: list[dict[str, Any]],
    evidence_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(validation_id: str, status: bool, detail: str) -> None:
        rows.append(base_row(validation_id=validation_id, status="PASS" if status else "FAIL", detail=detail))

    add("VAL2216_00_sources_exist", all(truthy(row.get("path_exists")) for row in source_rows), f"{sum(truthy(row.get('path_exists')) for row in source_rows)}/{len(source_rows)} sources exist")
    add("VAL2216_01_needles_found", all(truthy(row.get("needles_found")) for row in source_rows), f"{sum(truthy(row.get('needles_found')) for row in source_rows)}/{len(source_rows)} source needle sets found")

    sig_ok = any(row.get("clause_id") == "PHS2216_0_candidate_density_shape" and row.get("extraction_result") == "FOUND_CONDITIONAL_SHAPE" for row in signature_rows)
    sig_ok = sig_ok and any(row.get("clause_id") == "PHS2216_9_verdict" and row.get("extraction_result") == "NOT_PARENT_SIGNED_CURRENT_CORPUS" for row in signature_rows)
    sig_ok = sig_ok and all(not truthy(row.get("parent_signed_now")) for row in signature_rows)
    add("VAL2216_02_signature_extraction", sig_ok, "conditional shape found but no parent Hessian signature promoted")

    required_contracts = {"HDC2216_0_second_variation_definition", "HDC2216_1_lock_operator", "HDC2216_2_spectral_split", "HDC2216_3_null_source_gate", "HDC2216_4_observable_null_gate", "HDC2216_5_verdict"}
    contract_ok = required_contracts <= {row.get("contract_id") for row in contract_rows}
    add("VAL2216_03_hessian_contract", contract_ok, "Hessian derivation contract covers second variation, operator, spectrum, null source and visibility")

    null_ok = len(null_rows) == 9
    null_ok = null_ok and all(row.get("current_value") == "MISSING_PARENT_INPUT" for row in null_rows)
    null_ok = null_ok and all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in null_rows)
    add("VAL2216_04_null_bound_rows", null_ok, "nine null-bound acquisition rows emitted and non-score-ready")

    evidence_ok = any(row.get("evidence_id") == "EVM2216_4_verdict" and row.get("promotion_status") == "NULL_BOUND_ROWS_REQUIRED" for row in evidence_rows)
    add("VAL2216_05_evidence_map", evidence_ok, "evidence map records best positive evidence and hard blocks")

    claim_ok = any(row.get("gate_id") == "CG2216_1_parent_Hessian" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    claim_ok = claim_ok and any(row.get("gate_id") == "CG2216_4_local_GR_Newton" and row.get("status") == "BLOCKED_NONCLAIM" for row in claim_rows)
    add("VAL2216_06_claim_gate", claim_ok, "parent Hessian and local-GR/Newton claims remain blocked")

    decision_ok = any(row.get("decision") == "GAMMA_DENSITY_AND_KHAT_IDENTITY_NEXT" for row in decision_rows_)
    add("VAL2216_07_decision", decision_ok, "decision ledger selects Gamma density/Khat identity next")

    next_ok = any(row.get("route_id") == "NEXT2216_0_2217" and "Khat" in str(row.get("target_file")) for row in next_rows)
    add("VAL2216_08_next_target", next_ok, "2217 response-doublet parent density and Khat identity selected")

    csv_details: list[str] = []
    csv_ok = True
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_rows_parse(path)
        csv_ok = csv_ok and ok
        csv_details.append(f"{path.name}:{count if ok else detail}")
    add("VAL2216_09_csv_parse", csv_ok, "; ".join(csv_details))

    branch_ok = all(truthy(row.get("copied")) and truthy(row.get("parse_ok")) for row in copy_rows)
    add("VAL2216_10_branch_copies", branch_ok, ";".join(str(row.get("target_path")) for row in copy_rows))

    generated_groups = [source_rows, signature_rows, contract_rows, null_rows, evidence_rows, claim_rows, decision_rows_, next_rows, copy_rows]
    flags_false = all(
        not truthy(row.get("valid_for_claim")) and not truthy(row.get("claim_allowed"))
        for group in generated_groups
        for row in group
    )
    add("VAL2216_11_claim_flags_false", flags_false, "all generated rows keep valid_for_claim=false and claim_allowed=false")

    no_missing_promoted = all(not truthy(row.get("score_ready")) and not truthy(row.get("valid_prediction_row")) for row in null_rows)
    add("VAL2216_12_missing_not_promoted", no_missing_promoted, "null-bound missing inputs are not promoted to score-ready")

    formalization_clean = not formalization_has_2216_artifacts()
    add("VAL2216_13_formalization_clean", formalization_clean, "formalization-workbench has no 2216 artifacts")

    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    add("VAL2216_14_pycache_absent", pycache_absent, str(ROOT / "scripts" / "__pycache__"))

    pass_so_far = all(row.get("status") == "PASS" for row in rows)
    rows.append(
        base_row(
            validation_id="VAL2216_OVERALL",
            status="PASS" if pass_so_far else "FAIL",
            detail="2216 hunts the parent Hessian signature, finds only conditional response-doublet shape, emits evidence-backed null-bound acquisition rows, and selects Gamma density/Khat identity construction next",
        )
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    signature_rows: list[dict[str, Any]],
    contract_rows: list[dict[str, Any]],
    null_rows: list[dict[str, Any]],
    evidence_rows: list[dict[str, Any]],
    claim_rows: list[dict[str, Any]],
    decision_rows_: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    copy_rows: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    lines = [
        "# 2216 - Y5/R2FR Parent Hessian Signature Extraction Or Null-Bound Rows",
        "",
        "## Current Verdict",
        "",
        "2216 hunted the parent Hessian signature directly. The best positive evidence remains the response-doublet quadratic shape:",
        "",
        "`Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4)`.",
        "",
        "But this still does not parent-sign `M_AB`. The corpus does not yet supply the accepted scalar density owner, `K_hat = K_metric[Gamma_eff]` identity, physical `Z^A` basis, pairing/units, self-adjoint domain, rank/sign theorem, null projector, or null-source compatibility.",
        "",
        "So 2216 does **not** promote `M_AB` to a lock. It upgrades the fallback: every missing Hessian/null premise now has an evidence-backed nonclaim acquisition row.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Parent Hessian Signature Extraction",
        "",
        md_table(signature_rows, ["clause_id", "parent_signature", "extraction_result", "evidence", "what_this_signs", "what_remains_unsigned", "parent_signed_now", "valid_for_claim"]),
        "",
        "## Hessian Derivation Contract",
        "",
        md_table(contract_rows, ["contract_id", "contract_piece", "formula", "required_premises", "current_status", "consequence_if_closed", "valid_for_claim"]),
        "",
        "## Null-Bound Acquisition Rows",
        "",
        md_table(null_rows, ["bound_id", "missing_object", "evidence_sources", "required_action", "blocks", "current_value", "current_units", "numeric_bound", "status", "score_ready", "valid_prediction_row", "valid_for_claim"]),
        "",
        "## Signature Evidence Map",
        "",
        md_table(evidence_rows, ["evidence_id", "premise", "source", "finding", "promotion_status", "next_use", "valid_for_claim"]),
        "",
        "## Claim Gate",
        "",
        md_table(claim_rows, ["gate_id", "gate", "status", "reason", "valid_for_claim", "claim_allowed"]),
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
        "This is the non-glamorous but necessary answer. The strict local-GR path is not dead; it is demanding a real parent action. The next clean attack is not more tests and not more fifth-force language. It is: write the response-doublet parent density cleanly and check whether its metric variation really is `K_hat`. If that fails, we stop pretending `M_AB` is the lock and keep the null branch as a residual.",
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    remove_pycache()

    source_rows = source_register_rows()
    signature_rows = signature_extraction_rows()
    contract_rows = hessian_contract_rows()
    null_rows = null_bound_rows()
    evidence_rows = evidence_map_rows()
    claim_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    next_rows = next_target_rows()

    for path, rows in [
        (OUTPUTS["source_register"], source_rows),
        (OUTPUTS["signature_extraction"], signature_rows),
        (OUTPUTS["hessian_contract"], contract_rows),
        (OUTPUTS["null_bound_rows"], null_rows),
        (OUTPUTS["evidence_map"], evidence_rows),
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
        signature_rows,
        contract_rows,
        null_rows,
        evidence_rows,
        claim_rows,
        decision_rows_,
        next_rows,
        copy_rows,
    )
    write_csv(OUTPUTS["validation"], validation_rows_)

    write_doc(
        source_rows,
        signature_rows,
        contract_rows,
        null_rows,
        evidence_rows,
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
