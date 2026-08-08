from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_BOUNDARY_SOURCE_OWNER_PUBLIC_ACTIVATION_GATE_2417"
CHECKPOINT_ID = "2417"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2417-Y5-R2FR-boundary-source-owner-public-activation-gate.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2417_SOURCE_REGISTER.csv",
    "activation_gate": OUT / "P8_Y5_PARENT_QLOC_2417_BOUNDARY_SOURCE_OWNER_ACTIVATION_GATE.csv",
    "factorization": OUT / "P8_Y5_PARENT_QLOC_2417_SOURCE_BOUNDARY_RESIDUAL_FACTORIZATION.csv",
    "route_matrix": OUT / "P8_Y5_PARENT_QLOC_2417_THEOREM_ROUTE_MATRIX.csv",
    "public_status": OUT / "P8_Y5_PARENT_QLOC_2417_PUBLIC_LOCAL_GR_STATUS_LEDGER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2417_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2417_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2417_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2417_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2417_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2417_BOUNDARY_SOURCE_OWNER_GATE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2417_SOURCE_BOUNDARY_FACTORIZATION_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_BOUNDARY_SOURCE_OWNER_DECISION_2417_NONCLAIM.csv",
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


def formalization_has_2417_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2417-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2417*",
        "*P8_Y5_BRR545_2417*",
        "*Y5_R2FR_boundary_source_owner_public_activation_gate_2417*",
        "*JR2417*",
        "*PARENT_QLOC_BOUNDARY_SOURCE_OWNER_DECISION_2417*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("2416_signature_spine", ROOT / "2416-Y5-R2FR-parent-ordinary-action-variable-signature-spine.md", ["PAS2416_9_verdict", "NEXT2416_0_selected", "VAL2416_OVERALL"], "immediate handoff: parent signature spine written but public activation blocked."),
        ("2350_boundary", ROOT / "2350-Y5-R2FR-boundary-improvement-current-zero-or-P4-boundary-row.md", ["BIC2350_7_verdict", "P4B2350_0_boundary_total", "VAL2350_OVERALL"], "boundary/improvement current remains primary private-branch leak."),
        ("2351_theta_Qtau", ROOT / "2351-Y5-R2FR-parent-theta-Qtau-Htau-Href-extraction-or-source-row.md", ["PCR2351_7_verdict", "HHS2351_5_status", "SMB2351_0_target", "VAL2351_OVERALL"], "theta/Q_tau/H_tau/H_ref/M_H_ref reconciliation and source-measure bridge target."),
        ("2352_source_GM", ROOT / "2352-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md", ["SGS2352_7_verdict", "BRS2352_0_total", "NEXT2352_0", "VAL2352_OVERALL"], "source-charge equals measured GM remains unproved; readout no-reentry selected."),
        ("2151_source_owner", ROOT / "2151-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md", ["SOC2151_7_verdict", "RT2151_5_verdict", "VAL2151_OVERALL"], "source-owner map and FB5540 source row gate."),
        ("2152_boundary_projector", ROOT / "2152-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md", ["BE2152_5_verdict", "PO2152_5_verdict", "SP2152_6_total_guard", "VAL2152_OVERALL"], "boundary exactness/projector route narrowed but not closed."),
        ("2153_BX_primitive", ROOT / "2153-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md", ["PVT2153_5_verdict", "BXG2153_5_verdict", "VAL2153_OVERALL"], "B_X primitive still not parent-derived; edge-bound fill staged."),
        ("2144_source_bridge", ROOT / "2144-Y5-R2FR-MHref-Qtau-Gref-source-readout-bridge-or-closure.md", ["BRIDGE2144_6_verdict", "DHSRC2144_8_total", "VAL2144_OVERALL"], "source-readout bridge decomposed through Delta_Hsrc."),
        ("2145_integrability", ROOT / "2145-Y5-R2FR-Delta-Hsrc-integrability-reference-lock-or-first-source-row.md", ["NEST2145_1_epsilon_Hsrc", "NEST2145_10_current_frontier", "VAL2145_OVERALL"], "Delta_Hsrc/integrability chain points to current/source owner."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(base_row(source_id=source_id, source_path=str(path), path_exists=path.exists(), required_needles=";".join(needles), found_needles=";".join(found), needles_found=path.exists() and len(found) == len(needles), role=role))
    return rows


def activation_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="BSOG2417_0_parent_signature", gate="parent ordinary action variable signature", required_law="PAS2416_0..PAS2416_8 active in public parent theory", current_status="WRITTEN_NONCLAIM_NOT_PUBLICLY_DERIVED", failure_mode="private branch cannot be exported as public GR reduction"),
        base_row(row_id="BSOG2417_1_theta_Qtau", gate="theta_MTS and Q_tau^MTS owner", required_law="delta L_parent = E delta Phi + d theta_MTS and J_tau=dQ_tau^MTS+C_tau on local branch", current_status="TEMPLATE_EXISTS_OWNER_CHAIN_UNSIGNED", failure_mode="Hamiltonian charge denominator cannot be normalized"),
        base_row(row_id="BSOG2417_2_Htau_integrability", gate="H_tau integrability", required_law="delta H_tau[S]=int_S(delta Q_tau^MTS-i_tau theta_MTS) is field-space closed with fixed reference", current_status="INTEGRABILITY_NOT_CLOSED", failure_mode="M_H_ref source denominator remains placeholder"),
        base_row(row_id="BSOG2417_3_Href_MHref", gate="fixed H_ref and positive same-frame M_H_ref", required_law="M_H_ref=H_tau[S_outer]-H_ref>0 before orbital/readout calibration", current_status="MISSING_H_TAU_H_REF_MHREF", failure_mode="orbital GM backfill would be circular"),
        base_row(row_id="BSOG2417_4_source_measure", gate="Hamiltonian charge equals measured source", required_law="G_ref^-1 int_S Q_tau^MTS-H_ref = M_eff[Pi_M^H J_H^dress]", current_status="NOT_DERIVED_FACTORISED", failure_mode="Newton source normalization remains blocked"),
        base_row(row_id="BSOG2417_5_selector_readout", gate="readout/source selector no-reentry", required_law="source/worldtube/readout selectors act downstream and cannot create a source charge after variation", current_status="LIVE_SELECTED_SUBGATE", failure_mode="measured GM equality can be contaminated by readout labels"),
        base_row(row_id="BSOG2417_6_Hilbert_projector", gate="Hilbert/topological equality and projector commutator", required_law="Pi_M J_H = J_M_top + dB_zero and [d,Pi_M]J_H=0 or bounded", current_status="OPEN_PARALLEL_GATE", failure_mode="R_eq and I_commutator stay in epsilon_sourceGM"),
        base_row(row_id="BSOG2417_7_boundary_BX", gate="B_X primitive and boundary exactness", required_law="B_X=d_S b_X with harmonic/corner/kernel terms zero or source-bounded", current_status="PRECISE_BUT_NOT_DERIVED", failure_mode="edge/source leakage and epsilon_boundary_abs remain live"),
        base_row(row_id="BSOG2417_8_nonHilbert", gate="non-Hilbert and extra charge tails", required_law="spin/projective/boundary/non-Hilbert current projections vanish or are bounded before source readout", current_status="COMPONENT_PACK_NONCLAIM", failure_mode="extra current can masquerade as source mass"),
        base_row(row_id="BSOG2417_9_verdict", gate="boundary/source-owner public activation", required_law="BSOG2417_0 through BSOG2417_8 close together", current_status="FAIL_CURRENT_PUBLIC_ACTIVATION", failure_mode="local GR/Newton remains blocked; use residual factorization"),
    ]


def factorization_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="FAC2417_0_total", quantity="epsilon_source_boundary_abs", formula="epsilon_signature + epsilon_MHref + epsilon_selector_GM + epsilon_R_eq + epsilon_I_commutator + epsilon_BX_edge + epsilon_nonHilbert + epsilon_PG_orbit + epsilon_readout_reentry", status="ABSOLUTE_SUM_NONCLAIM", score_ready=False),
        base_row(row_id="FAC2417_1_signature", quantity="epsilon_signature", formula="I_not_publicly_derived(PAS2416_0..PAS2416_8)", status="PRIVATE_BRANCH_GUARD", score_ready=False),
        base_row(row_id="FAC2417_2_MHref", quantity="epsilon_MHref", formula="abs(delta_H_tau_nonintegrable + Delta_ref + Delta_symp + boundary_flux)/M_H_ref", status="MISSING_H_TAU_H_REF_MHREF", score_ready=False),
        base_row(row_id="FAC2417_3_selector", quantity="epsilon_selector_GM", formula="source/worldtube/readout selector mismatch in measured GM bridge", status="READOUT_NO_REENTRY_SELECTED_NEXT", score_ready=False),
        base_row(row_id="FAC2417_4_projector", quantity="epsilon_R_eq + epsilon_I_commutator", formula="Hilbert/topological equality residual plus M_H_ref^-1 int_A [d,Pi_M]J_H", status="OPEN_PARALLEL_GATE", score_ready=False),
        base_row(row_id="FAC2417_5_boundary_edge", quantity="epsilon_BX_edge", formula="edge exactness/harmonic/kernel/corner/source projection residual from B_X route", status="BX_PRIMITIVE_NOT_DERIVED", score_ready=False),
        base_row(row_id="FAC2417_6_nonHilbert", quantity="epsilon_nonHilbert", formula="spin/projective/boundary/non-Hilbert source projection tails", status="COMPONENT_PACK_NONCLAIM", score_ready=False),
        base_row(row_id="FAC2417_7_orbit_readout", quantity="epsilon_PG_orbit + epsilon_readout_reentry", formula="Poisson-Gauss/orbital/readout transfer mismatch after source-charge step", status="DEFERRED_UNTIL_PARENT_SOURCE_GATE", score_ready=False),
        base_row(row_id="FAC2417_8_no_cancellation", quantity="policy", formula="no cancellation between source, boundary, readout, projector, non-Hilbert, or orbital terms without a parent-signed identity", status="GUARD_READY", score_ready=False),
    ]


def route_matrix_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="ROUTE2417_0_readout_selector", route="readout no-reentry/source-selector zero", status="SELECT_PRIMARY_NEXT", why="2352 identifies this as the live source-GM subgate after connection and boundary narrowing", success_effect="removes epsilon_selector_GM and tightens source-charge measured-GM bridge"),
        base_row(route_id="ROUTE2417_1_boundary_BX", route="B_X vertical quotient / edge primitive", status="KEEP_PARALLEL", why="2153 says B_X primitive is still not parent-derived", success_effect="removes or bounds epsilon_BX_edge"),
        base_row(route_id="ROUTE2417_2_Htau_MHref", route="theta/Q_tau/H_tau/H_ref/M_H_ref extraction", status="KEEP_PARALLEL", why="2351 says M_H_ref is missing and cannot be backfilled from orbital GM", success_effect="normalizes boundary/source residual rows in same frame"),
        base_row(route_id="ROUTE2417_3_Hilbert_projector", route="Hilbert equality and projector commutator", status="KEEP_PARALLEL", why="2351/2152 keep R_eq and I_commutator open", success_effect="blocks post-variation source relabeling"),
        base_row(route_id="ROUTE2417_4_source_pack", route="finite source-bound acquisition", status="FALLBACK_ONLY", why="if theorem routes fail, residual rows need real values, units and source paths", success_effect="empirical local gates become possible without false zero claims"),
        base_row(route_id="ROUTE2417_5_verdict", route="combined public activation", status="FAIL_CURRENT_CLAIM_SELECT_SUBGATE", why="too many gates remain open for a public local-GR claim", success_effect="next work is focused on readout/source-selector no-reentry"),
    ]


def public_status_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="PUB2417_0_private_branch", object="private LC/no-Gamma/SRNG branch", status="usable internally", implication="not public evidence and not GitHub-ready"),
        base_row(row_id="PUB2417_1_source_gate", object="source charge equals measured GM", status="not derived", implication="Newton source normalization blocked"),
        base_row(row_id="PUB2417_2_boundary_gate", object="boundary/source owner", status="precise but open", implication="epsilon_boundary_abs/edge leakage retained"),
        base_row(row_id="PUB2417_3_residual_stack", object="FB5540/P4 source pack", status="schema-ready no values", implication="not an empirical pass"),
        base_row(row_id="PUB2417_4_local_GR", object="local GR/Newton reduction", status="closer but unclaimed", implication="requires source/charge boundary activation plus remaining operator/source-current identities"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2417_0_gate_written", gate="boundary/source-owner activation gate written", passed=True, claim_effect="public proof requirements are explicit"),
        base_row(gate_id="CG2417_1_public_activation", gate="boundary/source-owner public activation closes", passed=False, claim_effect="local GR/Newton remains blocked"),
        base_row(gate_id="CG2417_2_sourceGM", gate="source-charge equals measured GM", passed=False, claim_effect="Newton source normalization blocked"),
        base_row(gate_id="CG2417_3_MHref", gate="M_H_ref positive same-frame sourced", passed=False, claim_effect="cannot normalize source/boundary residuals"),
        base_row(gate_id="CG2417_4_BX", gate="B_X primitive/edge zero derived", passed=False, claim_effect="edge boundary leakage retained"),
        base_row(gate_id="CG2417_5_readout_selector", gate="readout/source-selector no-reentry proved", passed=False, claim_effect="selected next subgate"),
        base_row(gate_id="CG2417_6_source_pack_score", gate="finite residual/source pack score-ready", passed=False, claim_effect="not empirical evidence"),
        base_row(gate_id="CG2417_7_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, claim_effect="no public claim"),
        base_row(gate_id="CG2417_8_GitHub", gate="public/GitHub update", passed=False, claim_effect="private checkpoint only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2417_0_result", decision="PUBLIC_ACTIVATION_FAILS_BUT_IS_FACTORED", rationale="the local source/boundary problem is decomposed into named subgates", consequence="no more vague coupling fog"),
        base_row(decision_id="DEC2417_1_primary_next", decision="READOUT_SELECTOR_NO_REENTRY_NEXT", rationale="2352 selects it as the live measured-GM bridge subgate", consequence="attack source-worldtube/readout contamination before scoring local tests"),
        base_row(decision_id="DEC2417_2_parallel", decision="KEEP_BX_AND_MHREF_PARALLEL", rationale="boundary edge leakage and M_H_ref denominator remain independent blockers", consequence="do not forget 2153/2351 routes"),
        base_row(decision_id="DEC2417_3_fallback", decision="KEEP_SOURCE_PACK_NONCLAIM", rationale="if theorem zero fails, empirical work needs sourced rows and no-cancellation sums", consequence="no fitted GM or EH import shortcut"),
        base_row(decision_id="DEC2417_4_public_policy", decision="NO_LOCAL_GR_NO_GITHUB", rationale="private branch is sharper, but public source/charge activation is not closed", consequence="continue private derivation work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="NEXT2417_0_selected", selection_status="selected", target_file="2418-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md", target_script="scripts/Y5_R2FR_readout_no_reentry_source_selector_zero_or_component_row_2418.py", objective="prove that readout/source-worldtube selectors cannot re-enter the source charge after variation, or stage epsilon_selector_GM as an explicit nonclaim component row", success_condition="epsilon_selector_GM is theorem-zero under parent action/readout separation, or finite source-backed rows are emitted with no-cancellation guards", do_not_do="do not fill source mass from orbital GM or define selector equality by name"),
        base_row(route_id="NEXT2417_1_parallel", selection_status="held_parallel", target_file="2418b-Y5-R2FR-BX-vertical-quotient-or-edge-bound-row.md", target_script="scripts/Y5_R2FR_BX_vertical_quotient_or_edge_bound_row_2418b.py", objective="continue B_X primitive/edge leakage route from 2153", success_condition="B_X=d_S b_X is parent-derived or edge-bound rows are source-ready and nonclaim", do_not_do="do not treat Stokes exactness alone as boundary zero"),
    ]


def copy_branch_rows(gate: list[dict[str, Any]], factor: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["activation_gate"], BRANCH_COPIES["queue"], gate),
        ("branch_wep", OUTPUTS["factorization"], BRANCH_COPIES["branch_wep"], factor),
        ("beta_docs", OUTPUTS["decision"], BRANCH_COPIES["beta_docs"], decision),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source_path, target_path, source_rows in copy_specs:
        write_csv(target_path, source_rows)
        parse_ok, row_count, parse_detail = csv_rows_parse(target_path)
        rows.append(base_row(copy_id=copy_id, source_path=str(source_path), target_path=str(target_path), copied=target_path.exists(), parse_ok=parse_ok, row_count=row_count, parse_detail=parse_detail))
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
    rows.append(base_row(validation_id="VAL2417_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2417_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    gate_text = " ".join(str(row) for row in data["activation_gate"])
    required_gates = ["theta_MTS", "H_tau integrability", "M_H_ref", "Hamiltonian charge equals measured source", "readout/source selector no-reentry", "B_X primitive"]
    rows.append(base_row(validation_id="VAL2417_02_gate_coverage", status="PASS" if all(gate in gate_text for gate in required_gates) else "FAIL", detail="boundary/source-owner activation gate covers charge, denominator, selector, projector and boundary clauses"))
    rows.append(base_row(validation_id="VAL2417_03_public_activation_blocked", status="PASS" if "FAIL_CURRENT_PUBLIC_ACTIVATION" in gate_text else "FAIL", detail="public activation remains blocked"))

    factor_text = " ".join(str(row) for row in data["factorization"])
    rows.append(base_row(validation_id="VAL2417_04_factorization", status="PASS" if "epsilon_source_boundary_abs" in factor_text and "epsilon_selector_GM" in factor_text and "epsilon_BX_edge" in factor_text else "FAIL", detail="source/boundary residual factorization written"))
    rows.append(base_row(validation_id="VAL2417_05_factorization_nonready", status="PASS" if all(not row["score_ready"] for row in data["factorization"]) else "FAIL", detail="factorization remains non-score-ready"))

    route_text = " ".join(str(row) for row in data["route_matrix"])
    rows.append(base_row(validation_id="VAL2417_06_route_selection", status="PASS" if "SELECT_PRIMARY_NEXT" in route_text and "readout no-reentry/source-selector zero" in route_text else "FAIL", detail="readout/source-selector route selected while boundary and MHref remain parallel"))

    public_text = " ".join(str(row) for row in data["public_status"])
    rows.append(base_row(validation_id="VAL2417_07_public_status", status="PASS" if "closer but unclaimed" in public_text and "not derived" in public_text else "FAIL", detail="public local-GR status remains unclaimed"))

    claim_gate_map = {row["gate_id"]: row for row in data["claim_gates"]}
    blocked_ids = ["CG2417_1_public_activation", "CG2417_2_sourceGM", "CG2417_3_MHref", "CG2417_4_BX", "CG2417_5_readout_selector", "CG2417_7_local_GR_Newton", "CG2417_8_GitHub"]
    rows.append(base_row(validation_id="VAL2417_08_claim_gates", status="PASS" if all(not claim_gate_map[row_id]["passed"] for row_id in blocked_ids) else "FAIL", detail="public/local/GitHub claims blocked"))

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(base_row(validation_id="VAL2417_09_next_target", status="PASS" if "2418-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md" in next_text else "FAIL", detail="readout/source-selector no-reentry selected next"))

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2417_10_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    copies = data["branch_copies"]
    rows.append(base_row(validation_id="VAL2417_11_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    generated = all_generated_rows(data)
    rows.append(base_row(validation_id="VAL2417_12_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    rows.append(base_row(validation_id="VAL2417_13_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2417_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(base_row(validation_id="VAL2417_OVERALL", status=overall, detail="2417 writes the boundary/source-owner public activation gate, keeps local GR/Newton blocked, factorizes residuals, and selects readout/source-selector no-reentry next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2417_OVERALL")
    lines = [
        "# 2417 - Y5/R2FR Boundary Source Owner Public Activation Gate",
        "",
        "## Result",
        "",
        "2417 does not close local GR/Newton, but it stops the boundary/source-owner problem being a fog bank.",
        "",
        "The public activation gate is now explicit. To promote the private LC/no-Gamma branch, the parent theory must own `theta_MTS`, `Q_tau`, `H_tau`, fixed `H_ref`, positive same-frame `M_H_ref`, source-selector/readout separation, Hilbert/projector equality, and the boundary `B_X` primitive or a finite edge/source bound.",
        "",
        "Current status: the gate fails publicly. The useful result is factorization: the surviving source/boundary residual is now an absolute sum of named subgates, not a generic coupling worry. The primary next subgate is readout no-reentry / source-selector zero, with B_X and M_H_ref held in parallel.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Boundary Source Owner Activation Gate",
        "",
        md_table(data["activation_gate"], ["row_id", "gate", "required_law", "current_status", "failure_mode", "valid_for_claim"]),
        "",
        "## Source Boundary Residual Factorization",
        "",
        md_table(data["factorization"], ["row_id", "quantity", "formula", "status", "score_ready", "valid_for_claim"]),
        "",
        "## Theorem Route Matrix",
        "",
        md_table(data["route_matrix"], ["route_id", "route", "status", "why", "success_effect", "valid_for_claim"]),
        "",
        "## Public Local GR Status Ledger",
        "",
        md_table(data["public_status"], ["row_id", "object", "status", "implication", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(data["claim_gates"], ["gate_id", "gate", "passed", "claim_effect", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        "",
        md_table(data["decision"], ["decision_id", "decision", "rationale", "consequence", "valid_for_claim"]),
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
        "This is a good narrowing. We are not at derived GR, but we now know the next live throat: source/readout selectors must not re-enter the parent source charge after variation. If that closes, the source-GM bridge gets materially stronger. If it fails, `epsilon_selector_GM` becomes a real residual row instead of a ghost.",
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
        "activation_gate": activation_gate_rows(),
        "factorization": factorization_rows(),
        "route_matrix": route_matrix_rows(),
        "public_status": public_status_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["activation_gate"], data["activation_gate"])
    write_csv(OUTPUTS["factorization"], data["factorization"])
    write_csv(OUTPUTS["route_matrix"], data["route_matrix"])
    write_csv(OUTPUTS["public_status"], data["public_status"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["activation_gate"], data["factorization"], data["decision"])
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
