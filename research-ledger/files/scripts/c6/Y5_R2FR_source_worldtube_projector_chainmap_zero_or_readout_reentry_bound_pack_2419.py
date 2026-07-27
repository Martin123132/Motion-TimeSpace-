from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_SOURCE_WORLDTUBE_PROJECTOR_CHAINMAP_ZERO_OR_READOUT_REENTRY_BOUND_PACK_2419"
CHECKPOINT_ID = "2419"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2419-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2419_SOURCE_REGISTER.csv",
    "chainmap_gate": OUT / "P8_Y5_PARENT_QLOC_2419_CHAINMAP_ZERO_GATE.csv",
    "bound_pack": OUT / "P8_Y5_PARENT_QLOC_2419_CHAINMAP_READOUT_BOUND_PACK.csv",
    "bridge_update": OUT / "P8_Y5_PARENT_QLOC_2419_SOURCE_BRIDGE_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2419_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2419_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2419_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2419_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2419_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2419_CHAINMAP_ZERO_GATE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2419_CHAINMAP_BOUND_PACK_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_CHAINMAP_DECISION_2419_NONCLAIM.csv",
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


def formalization_has_2419_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2419-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2419*",
        "*P8_Y5_BRR545_2419*",
        "*Y5_R2FR_source_worldtube_projector_chainmap_zero_or_readout_reentry_bound_pack_2419*",
        "*JR2419*",
        "*PARENT_QLOC_CHAINMAP_DECISION_2419*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("2418_handoff", ROOT / "2418-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md", ["RNG2418_7_verdict", "NEXT2418_0_selected", "VAL2418_OVERALL"], "immediate handoff: source-worldtube/projector chain-map selected."),
        ("2354_chainmap", ROOT / "2354-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md", ["CMA2354_7_verdict", "ANT2354_8_verdict", "BP2354_0_total", "VAL2354_OVERALL"], "chain-map zero audit and bound pack."),
        ("2355_fixed_domain", ROOT / "2355-Y5-R2FR-worldtube-support-owner-fixed-domain-or-Icommutator-first-row.md", ["FDT2355_6_current_corpus_verdict", "SOC2355_8_verdict", "ICFR2355_0_total_first_row", "VAL2355_OVERALL"], "fixed-domain/support-owner theorem and first I_commutator row."),
        ("2356_source_descent", ROOT / "2356-Y5-R2FR-parent-source-current-descent-or-domain-motion-bound.md", ["SCD2356_6_current_corpus_verdict", "PDC2356_9_verdict", "DMB2356_0_total", "VAL2356_OVERALL"], "parent source-current descent theorem conditional and domain-motion bound rows."),
        ("1816_variation_order", ROOT / "1816-Y5-R2FR-variation-before-readout-source-selector-order-or-post-current-cA-row.md", ["VBR1816_6_verdict", "SSO1816_6_verdict", "VAL1816_OVERALL"], "variation-before-readout/source-selector order theorem."),
        ("2342_selector", ROOT / "2342-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md", ["SGB2342_0_selector_abs", "CG2342_1_worldtube_selector", "VAL2342_OVERALL"], "selector/source-GM bound origin."),
        ("2152_boundary_projector", ROOT / "2152-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md", ["PO2152_5_verdict", "SP2152_6_total_guard", "VAL2152_OVERALL"], "boundary/projector route and source pack guard."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needles, role in specs:
        text = read_text(path)
        found = [needle for needle in needles if needle in text]
        rows.append(base_row(source_id=source_id, source_path=str(path), path_exists=path.exists(), required_needles=";".join(needles), found_needles=";".join(found), needles_found=path.exists() and len(found) == len(needles), role=role))
    return rows


def chainmap_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="CMG2419_0_product_rule", object="projected Hilbert current", formal_identity="d(Pi_W J_H)=Pi_W dJ_H+[d,Pi_W]J_H and delta(Pi_W J_H)=Pi_W delta J_H+(delta Pi_W)J_H", current_status="EXACT_OBSTRUCTION_IDENTITY", missing_for_zero="fixed Pi_W chain-map and fixed source worldtube"),
        base_row(row_id="CMG2419_1_source_worldtube", object="W_source", formal_identity="W_source=closure(supp J_H[tau]) with compact regular support and buffer annulus", current_status="CONDITIONAL_SELECTOR_NOT_PARENT_SIGNED", missing_for_zero="parent source-current descent and support owner"),
        base_row(row_id="CMG2419_2_fixed_domain", object="A_ext/S_link", formal_identity="D_v W_source=0, D_v A_ext=0, and same linking surface used before readout", current_status="EXACT_CONDITIONAL_NOT_ACTIVE", missing_for_zero="fixed-domain parent owner"),
        base_row(row_id="CMG2419_3_chainmap", object="Pi_W/Pi_M", formal_identity="delta Pi_W=0 and [d,Pi_W]J_H=0 on the Hilbert-current complex", current_status="CONDITIONAL_MATH_NOT_PARENT_SIGNED", missing_for_zero="topological/projector representative and current complex owner"),
        base_row(row_id="CMG2419_4_source_descent", object="J_H descent", formal_identity="J_H=q^*Jbar_H and vertical source-current J_v^matter=0", current_status="CONDITIONAL_APPLICATION_BLOCKED", missing_for_zero="one parent matter-coupling action signs PDC2356 clauses"),
        base_row(row_id="CMG2419_5_MHref", object="M_H_ref denominator", formal_identity="I_commutator_abs_over_MHref uses positive same-frame M_H_ref, not observed orbital GM", current_status="MISSING_H_TAU_H_REF_MHREF", missing_for_zero="parent charge/source normalization"),
        base_row(row_id="CMG2419_6_verdict", object="source-worldtube/projector chain-map zero", formal_identity="CMG2419_0 through CMG2419_5 jointly imply selector/worldtube readout reentry zero", current_status="ZERO_NOT_DERIVED_BOUND_PACK_REQUIRED", missing_for_zero="source-current descent plus fixed support/domain/projector owner"),
    ]


def bound_pack_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="CBP2419_0_total", quantity="epsilon_chainmap_readout_abs", formula="I_commutator_abs + R_eq_abs + E_worldtube + E_projector_stress + E_domain_motion + E_current_escape + E_exterior + E_MHref_guard", status="ABSOLUTE_SUM_NONCLAIM", score_ready=False),
        base_row(row_id="CBP2419_1_Icommutator", quantity="I_commutator_abs", formula="abs(int_A [d,Pi_W]J_H) / M_H_ref", status="MISSING_CHAINMAP_ZERO_OR_SOURCE_ROW", score_ready=False),
        base_row(row_id="CBP2419_2_Req", quantity="R_eq_abs", formula="abs(Pi_W J_H - J_M_top - dB_zero) / M_H_ref", status="MISSING_HILBERT_TOPOLOGICAL_EQUALITY", score_ready=False),
        base_row(row_id="CBP2419_3_worldtube", quantity="E_worldtube", formula="abs(delta W_source)+abs(delta support profile)+abs(linking surface drift)", status="MISSING_SUPPORT_OWNER", score_ready=False),
        base_row(row_id="CBP2419_4_projector_stress", quantity="E_projector_stress", formula="abs(delta Pi_W/delta g)+abs(delta Hodge/domain representative)", status="MISSING_PROJECTOR_STRESS_BOUND", score_ready=False),
        base_row(row_id="CBP2419_5_domain_motion", quantity="E_domain_motion", formula="abs(int_A d chi_W wedge Pi_W J_H) + boundary crossing terms", status="MISSING_FIXED_DOMAIN", score_ready=False),
        base_row(row_id="CBP2419_6_current_escape", quantity="E_current_escape", formula="current outside fixed Hilbert/source complex or exterior annulus", status="MISSING_EXTERIOR_SILENCE", score_ready=False),
        base_row(row_id="CBP2419_7_MHref_guard", quantity="E_MHref_guard", formula="I_not_sourced(M_H_ref,H_tau,H_ref,Q_tau)", status="MISSING_DENOMINATOR", score_ready=False),
        base_row(row_id="CBP2419_8_no_cancellation", quantity="policy", formula="absolute sum; no cancellation between commutator, equality, worldtube, projector, domain, current or denominator terms", status="GUARD_READY", score_ready=False),
    ]


def bridge_update_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="BRU2419_0_selector_refinement", object="epsilon_selector_GM_abs", status="REFINED", update="dangerous selector/readout part now routes through epsilon_chainmap_readout_abs plus EFT/calibration/marker residues"),
        base_row(row_id="BRU2419_1_zero_route", object="chain-map zero theorem", status="CONDITIONAL_NOT_ACTIVE", update="if J_H descends, W_source/domain fixed, and Pi_W chain-map signed, selector reentry can be zeroed"),
        base_row(row_id="BRU2419_2_bound_route", object="chain-map bound pack", status="SCHEMA_READY_NO_VALUES", update="if zero route fails, component rows must be sourced before empirical tests"),
        base_row(row_id="BRU2419_3_source_bridge", object="source charge equals measured GM", status="STILL_BLOCKED", update="M_H_ref, source-current descent, and chain-map owner remain open"),
        base_row(row_id="BRU2419_4_next", object="minimal parent matter-coupling action", status="SELECTED_NEXT", update="one parent action signature is the least handwavy way to close source-current descent/support owner"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2419_0_product_identity", gate="product-rule obstruction written", passed=True, claim_effect="chain-map problem is exact, not vague"),
        base_row(gate_id="CG2419_1_chainmap_zero", gate="delta Pi_W=0 and [d,Pi_W]J_H=0", passed=False, claim_effect="I_commutator_abs retained"),
        base_row(gate_id="CG2419_2_fixed_worldtube", gate="fixed worldtube/domain owner", passed=False, claim_effect="E_worldtube/E_domain_motion retained"),
        base_row(gate_id="CG2419_3_source_descent", gate="parent source-current descent active", passed=False, claim_effect="source-current/domain rows retained"),
        base_row(gate_id="CG2419_4_MHref", gate="positive same-frame M_H_ref available", passed=False, claim_effect="bound pack not score-ready"),
        base_row(gate_id="CG2419_5_bound_score", gate="chain-map bound pack score-ready", passed=False, claim_effect="not empirical evidence"),
        base_row(gate_id="CG2419_6_sourceGM", gate="measured source-GM bridge closed", passed=False, claim_effect="source bridge blocked"),
        base_row(gate_id="CG2419_7_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, claim_effect="no public claim"),
        base_row(gate_id="CG2419_8_GitHub", gate="public/GitHub update", passed=False, claim_effect="private checkpoint only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2419_0_result", decision="CHAINMAP_ZERO_NOT_PROMOTED", rationale="the obstruction identity is exact but antecedents are unsigned", consequence="bound pack retained"),
        base_row(decision_id="DEC2419_1_progress", decision="SOURCE_SELECTOR_PROBLEM_REDUCED_TO_DESCENT_DOMAIN_PROJECTOR", rationale="worldtube/projector leakage is no longer vague", consequence="attack source-current descent/fixed-domain owner"),
        base_row(decision_id="DEC2419_2_bound_pack", decision="INSTALL_ABSOLUTE_CHAINMAP_BOUND_PACK", rationale="if theorem-zero fails, I_commutator/R_eq/domain/projector terms must be scoreable", consequence="no cancellation or orbital-GM denominator shortcut"),
        base_row(decision_id="DEC2419_3_next", decision="MINIMAL_PARENT_MATTER_COUPLING_ACTION_NEXT", rationale="2356 identifies this as the quickest honest route to source-current descent", consequence="target 2420/2357 synthesis"),
        base_row(decision_id="DEC2419_4_public_policy", decision="NO_LOCAL_GR_NO_GITHUB", rationale="source bridge remains blocked", consequence="continue private derivation work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="NEXT2419_0_selected", selection_status="selected", target_file="2420-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md", target_script="scripts/Y5_R2FR_minimal_parent_matter_coupling_action_or_domain_motion_input_2420.py", objective="write/test the minimal parent matter-coupling action that would sign source-current descent, no-source-slot, variation-before-readout and fixed support owner; otherwise keep domain-motion input rows", success_condition="parent action clauses jointly sign J_H=q^*Jbar_H and fixed W_source, or domain-motion inputs remain explicit nonclaim rows", do_not_do="do not claim fixed support by definition, use Noether conservation alone, or normalize with observed orbital GM"),
        base_row(route_id="NEXT2419_1_parallel", selection_status="held_parallel", target_file="2420b-Y5-R2FR-topological-PiW-representative-or-projector-stress-bound.md", target_script="scripts/Y5_R2FR_topological_PiW_representative_or_projector_stress_bound_2420b.py", objective="prove Pi_W is a fixed topological chain-map representative or assign projector-stress bound rows", success_condition="delta Pi_W=0 and [d,Pi_W]J_H=0 are parent-signed or projector-stress rows are source-ready", do_not_do="do not treat Hodge/domain projectors as topological without proof"),
    ]


def copy_branch_rows(gate: list[dict[str, Any]], bounds: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["chainmap_gate"], BRANCH_COPIES["queue"], gate),
        ("branch_wep", OUTPUTS["bound_pack"], BRANCH_COPIES["branch_wep"], bounds),
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
    rows.append(base_row(validation_id="VAL2419_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2419_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    gate_text = " ".join(str(row) for row in data["chainmap_gate"])
    rows.append(base_row(validation_id="VAL2419_02_product_identity", status="PASS" if "[d,Pi_W]J_H" in gate_text and "delta Pi_W" in gate_text else "FAIL", detail="projector product-rule obstruction recorded"))
    rows.append(base_row(validation_id="VAL2419_03_zero_not_promoted", status="PASS" if "ZERO_NOT_DERIVED_BOUND_PACK_REQUIRED" in gate_text else "FAIL", detail="chain-map zero remains nonclaim"))

    bound_text = " ".join(str(row) for row in data["bound_pack"])
    required_terms = ["I_commutator_abs", "R_eq_abs", "E_worldtube", "E_projector_stress", "E_domain_motion", "E_MHref_guard"]
    rows.append(base_row(validation_id="VAL2419_04_bound_pack_coverage", status="PASS" if all(term in bound_text for term in required_terms) else "FAIL", detail="chain-map bound pack covers commutator, equality, worldtube, projector, domain and denominator terms"))
    rows.append(base_row(validation_id="VAL2419_05_bound_pack_nonready", status="PASS" if all(not row["score_ready"] for row in data["bound_pack"]) else "FAIL", detail="bound pack remains non-score-ready"))

    bridge_text = " ".join(str(row) for row in data["bridge_update"])
    rows.append(base_row(validation_id="VAL2419_06_bridge_update", status="PASS" if "STILL_BLOCKED" in bridge_text and "SELECTED_NEXT" in bridge_text else "FAIL", detail="source bridge stays blocked and next target selected"))

    claim_gate_map = {row["gate_id"]: row for row in data["claim_gates"]}
    blocked_ids = ["CG2419_1_chainmap_zero", "CG2419_2_fixed_worldtube", "CG2419_3_source_descent", "CG2419_4_MHref", "CG2419_7_local_GR_Newton", "CG2419_8_GitHub"]
    rows.append(base_row(validation_id="VAL2419_07_claim_gates", status="PASS" if all(not claim_gate_map[row_id]["passed"] for row_id in blocked_ids) else "FAIL", detail="public/source/local/GitHub claims blocked"))

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(base_row(validation_id="VAL2419_08_next_target", status="PASS" if "2420-Y5-R2FR-minimal-parent-matter-coupling-action-or-domain-motion-input.md" in next_text else "FAIL", detail="minimal parent matter-coupling action selected next"))

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2419_09_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    copies = data["branch_copies"]
    rows.append(base_row(validation_id="VAL2419_10_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    generated = all_generated_rows(data)
    rows.append(base_row(validation_id="VAL2419_11_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    rows.append(base_row(validation_id="VAL2419_12_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2419_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(base_row(validation_id="VAL2419_OVERALL", status=overall, detail="2419 narrows selector reentry to source-worldtube/projector chain-map antecedents, rejects zero promotion, keeps bound pack nonclaim, and selects minimal parent matter-coupling action next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2419_OVERALL")
    lines = [
        "# 2419 - Y5/R2FR Source-Worldtube Projector Chainmap Zero Or Readout-Reentry Bound Pack",
        "",
        "## Result",
        "",
        "2419 turns the dangerous readout/source-selector channel into an exact chain-map problem.",
        "",
        "The obstruction is precise:",
        "",
        "`d(Pi_W J_H)=Pi_W dJ_H+[d,Pi_W]J_H`, and `delta(Pi_W J_H)=Pi_W delta J_H+(delta Pi_W)J_H`.",
        "",
        "So the source-worldtube/projector zero would follow if `W_source`, the exterior annulus, the linking surface, `Pi_W`, `J_H`, `tau`, and `M_H_ref` are all parent-owned, fixed before readout, and live on the same Hilbert-current complex. Current evidence does not sign those antecedents together. The chain-map zero is therefore not promoted; the bound pack remains live.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Chainmap Zero Gate",
        "",
        md_table(data["chainmap_gate"], ["row_id", "object", "formal_identity", "current_status", "missing_for_zero", "valid_for_claim"]),
        "",
        "## Chainmap Readout Bound Pack",
        "",
        md_table(data["bound_pack"], ["row_id", "quantity", "formula", "status", "score_ready", "valid_for_claim"]),
        "",
        "## Source Bridge Update",
        "",
        md_table(data["bridge_update"], ["row_id", "object", "status", "update", "valid_for_claim"]),
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
        "This is not a retreat. It is a compression: the source-selector problem now depends mainly on parent source-current descent and fixed worldtube/domain ownership. The next best strike is the minimal parent matter-coupling action that could sign those clauses together.",
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
        "chainmap_gate": chainmap_gate_rows(),
        "bound_pack": bound_pack_rows(),
        "bridge_update": bridge_update_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["chainmap_gate"], data["chainmap_gate"])
    write_csv(OUTPUTS["bound_pack"], data["bound_pack"])
    write_csv(OUTPUTS["bridge_update"], data["bridge_update"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["chainmap_gate"], data["bound_pack"], data["decision"])
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
