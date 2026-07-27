from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_READOUT_NO_REENTRY_SOURCE_SELECTOR_ZERO_OR_COMPONENT_ROW_2418"
CHECKPOINT_ID = "2418"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_WEP = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "2418-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md"

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2418_SOURCE_REGISTER.csv",
    "no_reentry_gate": OUT / "P8_Y5_PARENT_QLOC_2418_READOUT_NO_REENTRY_GATE.csv",
    "selector_components": OUT / "P8_Y5_PARENT_QLOC_2418_SELECTOR_REENTRY_COMPONENT_ROWS.csv",
    "source_bridge_update": OUT / "P8_Y5_PARENT_QLOC_2418_SOURCE_GM_BRIDGE_UPDATE.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2418_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2418_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2418_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2418_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2418_VALIDATION.csv",
}

BRANCH_COPIES = {
    "queue": QUEUE / "JR2418_READOUT_SELECTOR_GATE_NONCLAIM.csv",
    "branch_wep": BRANCH_WEP / "P8_Y5_PARENT_QLOC_2418_SELECTOR_REENTRY_COMPONENTS_NONCLAIM.csv",
    "beta_docs": BETA_DOCS / "PARENT_QLOC_READOUT_SELECTOR_DECISION_2418_NONCLAIM.csv",
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


def formalization_has_2418_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2418-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2418*",
        "*P8_Y5_BRR545_2418*",
        "*Y5_R2FR_readout_no_reentry_source_selector_zero_or_component_row_2418*",
        "*JR2418*",
        "*PARENT_QLOC_READOUT_SELECTOR_DECISION_2418*",
    )
    return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("2417_handoff", ROOT / "2417-Y5-R2FR-boundary-source-owner-public-activation-gate.md", ["BSOG2417_5_selector_readout", "NEXT2417_0_selected", "VAL2417_OVERALL"], "immediate handoff: readout/source-selector no-reentry selected."),
        ("2353_no_reentry", ROOT / "2353-Y5-R2FR-readout-no-reentry-source-selector-zero-or-component-row.md", ["RNE2353_7_verdict", "RRC2353_0_total", "SSG2353_7_verdict", "VAL2353_OVERALL"], "prior readout no-reentry audit: pure postprocessing safe, general selector zero rejected."),
        ("2352_sourceGM", ROOT / "2352-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md", ["SGS2352_7_verdict", "BRS2352_5_readout_reentry", "NEXT2352_0", "VAL2352_OVERALL"], "source-GM synthesis identifies readout reentry as live next gate."),
        ("2342_selector_contract", ROOT / "2342-Y5-R2FR-source-charge-equals-measured-GM-or-selector-bound.md", ["SSC2342_0_selector", "SGB2342_0_selector_abs", "VAL2342_OVERALL"], "source-GM bridge selector/source-measure contract and bound rows."),
        ("2343_same_frame", ROOT / "2343-Y5-R2FR-NoSourceOnlySpeciesSlot-and-same-frame-GM-descent-or-sourceGM-bound.md", ["SFGD2343_3_no_reentry", "CM2343_4_readout_selector_reentry", "VAL2343_OVERALL"], "same-frame GM descent keeps readout no-reentry as a blocker."),
        ("2344_current_owner", ROOT / "2344-Y5-R2FR-parent-source-blind-matter-functor-current-owner-or-sourceGM-bound.md", ["CO2344_3_readout_order", "CKM2344_3_readout_reentry", "VAL2344_OVERALL"], "current-owner theorem leaves readout stability unsigned."),
        ("2335_srng", ROOT / "2335-Y5-R2FR-source-readout-noGamma-action-argument-certificate.md", ["SRNG2335_6_verdict", "THM2335_3_SRNG_sum", "VAL2335_OVERALL"], "SRNG certificate is partial and private/nonclaim."),
        ("1816_variation_before_readout", ROOT / "1816-Y5-R2FR-variation-before-readout-source-selector-order-or-post-current-cA-row.md", ["VBR1816_6_verdict", "SSO1816_6_verdict", "VAL1816_OVERALL"], "older variation-before-readout/source-selector order theorem source."),
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


def no_reentry_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="RNG2418_0_target", readout_piece="readout/source-selector no-reentry", theorem_status="TARGET_SHARPENED", result="decides whether epsilon_selector_GM can be theorem-zero or must remain a source-GM residual", remaining_gap="projector/worldtube/readout chain-map proof"),
        base_row(row_id="RNG2418_1_pure_postprocessing", readout_piece="pure solution-to-data maps", theorem_status="EXACT_CONDITIONAL_ZERO", result="R_post: Sol(S_parent)/G -> Data that is absent from S_parent/S_eff and has no source-coefficient codomain cannot alter parent source variation", remaining_gap="must prove actual local readouts are this type"),
        base_row(row_id="RNG2418_2_variation_before_readout", readout_piece="variation-before-readout order", theorem_status="EXACT_CONDITIONAL_THEOREM", result="if T_H/J_H are formed before readout maps, pure readout cannot reweight source charge", remaining_gap="global parent/action/readout order certificate"),
        base_row(row_id="RNG2418_3_source_worldtube_projector", readout_piece="source worldtube/projector", theorem_status="LIVE_COUNTERMODEL", result="field-dependent W_source, Pi_W or domain projectors can select or reweight source support unless chain-map fixed", remaining_gap="delta Pi_W=0 and [d,Pi_W]J_H=0"),
        base_row(row_id="RNG2418_4_EFT_radiative", readout_piece="effective/radiative pre-variation readout", theorem_status="LIVE_COUNTERMODEL", result="readout-reduced effective action can feed back into variation if varied before parent source is formed", remaining_gap="typed EFT/readout separation certificate"),
        base_row(row_id="RNG2418_5_calibration_feedback", readout_piece="GM/PPN/calibration readout", theorem_status="LIVE_COUNTERMODEL", result="choosing calibration masks/source labels after seeing readout can hide source-GM residuals", remaining_gap="fixed-before-readout calibration rule"),
        base_row(row_id="RNG2418_6_hidden_marker", readout_piece="material/species/source labels", theorem_status="LIVE_COUNTERMODEL", result="readout labels can reintroduce forbidden source/species coefficients if not forgotten before coupling", remaining_gap="source-blind functor/current-owner public signature"),
        base_row(row_id="RNG2418_7_verdict", readout_piece="general no-reentry", theorem_status="GENERAL_ZERO_NOT_DERIVED_COMPONENT_ROW_REQUIRED", result="pure postprocessing zero is retained, but general selector/readout no-reentry is not public", remaining_gap="2354/2419 source-worldtube/projector chain-map or component rows"),
    ]


def selector_component_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="SRCOMP2418_0_total", quantity="epsilon_selector_GM_abs", component="absolute selector/source-GM reentry envelope", formula="E_projector_worldtube + E_source_worldtube + E_EFT_readout + E_calibration_feedback + E_hidden_marker + E_arena_transfer", current_value="MISSING_COMPONENT_VALUES", score_ready=False),
        base_row(row_id="SRCOMP2418_1_projector_worldtube", quantity="E_projector_worldtube", component="field-dependent projector/domain/source-worldtube", formula="||delta Pi_W J_H|| + ||[d,Pi_W]J_H|| + ||delta W_source||", current_value="MISSING_CHAINMAP_CERTIFICATE_OR_BOUND", score_ready=False),
        base_row(row_id="SRCOMP2418_2_source_worldtube", quantity="E_source_worldtube", component="source support/profile/composition selector", formula="||delta W_source|| + ||delta source_profile|| + ||composition_selector_reentry||", current_value="MISSING_SOURCE_WORLD_TUBE_CERTIFICATE", score_ready=False),
        base_row(row_id="SRCOMP2418_3_EFT_readout", quantity="E_EFT_readout", component="pre-variation reduced/effective readout action", formula="||delta S_eff_readout/delta source|| after parent split", current_value="MISSING_EFT_DOMAIN_SEPARATION", score_ready=False),
        base_row(row_id="SRCOMP2418_4_calibration_feedback", quantity="E_calibration_feedback", component="GM/PPN/calibration mask feedback", formula="||delta calibration_mask(source,readout)||", current_value="MISSING_FIXED_BEFORE_READOUT_RULE", score_ready=False),
        base_row(row_id="SRCOMP2418_5_hidden_marker", quantity="E_hidden_marker", component="material/species/source label reentry", formula="||P_source(label_readout -> coefficient)||", current_value="MISSING_LABEL_FORGETTING_CERTIFICATE", score_ready=False),
        base_row(row_id="SRCOMP2418_6_arena_transfer", quantity="E_arena_transfer", component="cross-arena readout transfer", formula="||K_arena_to_source readout residual||", current_value="MISSING_ARENA_SPECIFIC_TRANSFER_MAP", score_ready=False),
        base_row(row_id="SRCOMP2418_7_no_cancellation", quantity="policy", component="absolute no-cancellation guard", formula="sum absolute components; no cancellation between readout/projector/calibration/species channels unless parent-signed", current_value="GUARD_READY", score_ready=False),
    ]


def source_bridge_update_rows() -> list[dict[str, Any]]:
    return [
        base_row(row_id="SBU2418_0_pure_win", object="pure postprocessing", status="CONDITIONAL_ZERO_RETAINED", bridge_effect="safe readout class exists; this is a useful theorem but not enough for source-GM bridge"),
        base_row(row_id="SBU2418_1_selector_live", object="epsilon_selector_GM_abs", status="LIVE_PRIMARY_SUBGATE", bridge_effect="source-charge equals measured GM cannot close until this is zero or bounded"),
        base_row(row_id="SBU2418_2_sourceGM_factor", object="epsilon_sourceGM_bridge_abs", status="UPDATED", bridge_effect="epsilon_sourceGM_bridge_abs includes epsilon_selector_GM_abs plus M_H_ref, relative sourceGM, non-Hilbert, and Poisson/Gauss terms"),
        base_row(row_id="SBU2418_3_GR_Newton", object="local GR/Newton", status="BLOCKED_NONCLAIM", bridge_effect="readout/source selector is one gate, not the whole GR reduction"),
        base_row(row_id="SBU2418_4_next", object="source-worldtube/projector chain-map", status="SELECTED_NEXT", bridge_effect="delta Pi_W=0 and [d,Pi_W]J_H=0 is now the least-mushy target"),
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        base_row(gate_id="CG2418_0_pure_postprocessing", gate="pure postprocessing no-reentry conditional theorem", passed=True, claim_effect="safe readout subclass retained"),
        base_row(gate_id="CG2418_1_general_no_reentry", gate="general readout/source-selector no-reentry", passed=False, claim_effect="epsilon_selector_GM_abs retained"),
        base_row(gate_id="CG2418_2_projector_chainmap", gate="source-worldtube/projector chain-map zero", passed=False, claim_effect="selected next target"),
        base_row(gate_id="CG2418_3_component_score", gate="selector component rows numeric and sourced", passed=False, claim_effect="not empirical evidence"),
        base_row(gate_id="CG2418_4_sourceGM_bridge", gate="source charge equals measured GM", passed=False, claim_effect="source-GM bridge remains blocked"),
        base_row(gate_id="CG2418_5_local_GR_Newton", gate="local GR/Newton reduction derived", passed=False, claim_effect="no public claim"),
        base_row(gate_id="CG2418_6_GitHub", gate="public/GitHub update", passed=False, claim_effect="private checkpoint only"),
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        base_row(decision_id="DEC2418_0_result", decision="PURE_POSTPROCESSING_ZERO_RETAINED", rationale="pure solution-to-data maps are harmless by conditional theorem", consequence="keep the clean readout subclass"),
        base_row(decision_id="DEC2418_1_no_overclaim", decision="GENERAL_SELECTOR_ZERO_REJECTED", rationale="worldtube/projector/EFT/calibration/species-label maps can reenter source selection", consequence="epsilon_selector_GM_abs remains live"),
        base_row(decision_id="DEC2418_2_component_pack", decision="SELECTOR_COMPONENT_ROWS_INSTALLED", rationale="unsafe readout pieces need theorem-zero or finite source-backed rows", consequence="no cancellation or measured-GM hiding"),
        base_row(decision_id="DEC2418_3_next", decision="SOURCE_WORLDTUBE_PROJECTOR_CHAINMAP_NEXT", rationale="delta Pi_W=0 and [d,Pi_W]J_H=0 are the precise next obstructions", consequence="target 2419/2354 chain-map theorem"),
        base_row(decision_id="DEC2418_4_public_policy", decision="NO_LOCAL_GR_NO_GITHUB", rationale="source-GM bridge remains open", consequence="continue private derivation work"),
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        base_row(route_id="NEXT2418_0_selected", selection_status="selected", target_file="2419-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md", target_script="scripts/Y5_R2FR_source_worldtube_projector_chainmap_zero_or_readout_reentry_bound_pack_2419.py", objective="prove delta Pi_W=0 and [d,Pi_W]J_H=0 for source-worldtube/projector readout, or stage readout-reentry bound pack components", success_condition="projector/worldtube selector zero is parent-signed, or E_projector_worldtube/E_source_worldtube rows are explicit, sourced placeholders with claim flags false", do_not_do="do not treat pure postprocessing theorem as proof for field-dependent projectors"),
        base_row(route_id="NEXT2418_1_parallel", selection_status="held_parallel", target_file="2419b-Y5-R2FR-parent-readout-domain-closure-adoption-decision.md", target_script="scripts/Y5_R2FR_parent_readout_domain_closure_adoption_decision_2419b.py", objective="decide whether to adopt a strict parent readout-domain separation clause as private nonclaim or pursue deeper derivation", success_condition="readout-domain closure is either derived, private-locked, or converted to explicit residual rows", do_not_do="do not call adoption a public derivation"),
    ]


def copy_branch_rows(gate: list[dict[str, Any]], components: list[dict[str, Any]], decision: list[dict[str, Any]]) -> list[dict[str, Any]]:
    copy_specs = [
        ("queue", OUTPUTS["no_reentry_gate"], BRANCH_COPIES["queue"], gate),
        ("branch_wep", OUTPUTS["selector_components"], BRANCH_COPIES["branch_wep"], components),
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
    rows.append(base_row(validation_id="VAL2418_00_sources_exist", status="PASS" if all(row["path_exists"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['path_exists'])}/{len(sources)} sources exist"))
    rows.append(base_row(validation_id="VAL2418_01_needles_found", status="PASS" if all(row["needles_found"] for row in sources) else "FAIL", detail=f"{sum(1 for row in sources if row['needles_found'])}/{len(sources)} source needle sets found"))

    gate_text = " ".join(str(row) for row in data["no_reentry_gate"])
    rows.append(base_row(validation_id="VAL2418_02_pure_zero_retained", status="PASS" if "EXACT_CONDITIONAL_ZERO" in gate_text and "pure solution-to-data" in gate_text else "FAIL", detail="pure postprocessing zero theorem retained"))
    rows.append(base_row(validation_id="VAL2418_03_general_zero_rejected", status="PASS" if "GENERAL_ZERO_NOT_DERIVED_COMPONENT_ROW_REQUIRED" in gate_text and "LIVE_COUNTERMODEL" in gate_text else "FAIL", detail="general selector/readout zero rejected"))

    component_text = " ".join(str(row) for row in data["selector_components"])
    required_components = ["E_projector_worldtube", "E_source_worldtube", "E_EFT_readout", "E_calibration_feedback", "E_hidden_marker", "E_arena_transfer"]
    rows.append(base_row(validation_id="VAL2418_04_component_coverage", status="PASS" if all(component in component_text for component in required_components) else "FAIL", detail="selector reentry component rows cover projector, worldtube, EFT, calibration, marker and arena transfer"))
    rows.append(base_row(validation_id="VAL2418_05_components_nonready", status="PASS" if all(not row["score_ready"] for row in data["selector_components"]) else "FAIL", detail="selector components remain non-score-ready"))

    bridge_text = " ".join(str(row) for row in data["source_bridge_update"])
    rows.append(base_row(validation_id="VAL2418_06_bridge_update", status="PASS" if "LIVE_PRIMARY_SUBGATE" in bridge_text and "SELECTED_NEXT" in bridge_text else "FAIL", detail="source-GM bridge updated with selector as live subgate"))

    claim_gate_map = {row["gate_id"]: row for row in data["claim_gates"]}
    blocked_ids = ["CG2418_1_general_no_reentry", "CG2418_2_projector_chainmap", "CG2418_3_component_score", "CG2418_4_sourceGM_bridge", "CG2418_5_local_GR_Newton", "CG2418_6_GitHub"]
    rows.append(base_row(validation_id="VAL2418_07_claim_gates", status="PASS" if all(not claim_gate_map[row_id]["passed"] for row_id in blocked_ids) else "FAIL", detail="public/source-GM/local/GitHub claims blocked"))

    next_text = " ".join(str(row) for row in data["next_target"])
    rows.append(base_row(validation_id="VAL2418_08_next_target", status="PASS" if "2419-Y5-R2FR-source-worldtube-projector-chainmap-zero-or-readout-reentry-bound-pack.md" in next_text else "FAIL", detail="source-worldtube/projector chain-map selected next"))

    csv_ok = True
    details: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        parse_ok, row_count, parse_detail = csv_rows_parse(path)
        csv_ok = csv_ok and parse_ok and row_count > 0
        details.append(f"{path.name}:{row_count}:{parse_detail}")
    rows.append(base_row(validation_id="VAL2418_09_csv_parse", status="PASS" if csv_ok else "FAIL", detail="; ".join(details)))

    copies = data["branch_copies"]
    rows.append(base_row(validation_id="VAL2418_10_branch_copies", status="PASS" if all(row["copied"] and row["parse_ok"] for row in copies) else "FAIL", detail=";".join(str(row["target_path"]) for row in copies)))

    generated = all_generated_rows(data)
    rows.append(base_row(validation_id="VAL2418_11_no_claim_flags", status="PASS" if all(not row.get("valid_for_claim", False) and not row.get("claim_allowed", False) for row in generated) else "FAIL", detail="all generated rows keep valid_for_claim=false and claim_allowed=false"))
    rows.append(base_row(validation_id="VAL2418_12_formalization_untouched_by_outputs", status="PASS" if not formalization_has_2418_artifacts() else "FAIL", detail="script outputs stay inside post-checkpoint-work"))

    overall = "PASS" if all(row["status"] == "PASS" for row in rows) else "FAIL"
    rows.append(base_row(validation_id="VAL2418_OVERALL", status=overall, detail="2418 retains pure-postprocessing zero, rejects general selector no-reentry, stages epsilon_selector_GM component rows, and selects source-worldtube/projector chain-map next"))
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    overall = next(row for row in data["validation"] if row["validation_id"] == "VAL2418_OVERALL")
    lines = [
        "# 2418 - Y5/R2FR Readout No-Reentry Source Selector Zero Or Component Row",
        "",
        "## Result",
        "",
        "2418 keeps the useful win and refuses the dangerous overclaim.",
        "",
        "Pure postprocessing readout is harmless as an exact conditional theorem: if the map is only `R_post: Sol(S_parent)/G -> Data`, absent from the parent/effective action and not a source-coefficient object, it cannot alter the parent source variation.",
        "",
        "But the general readout/source-selector zero is **not** derived. Source worldtube projectors, field-dependent domains, effective/radiative readout actions, calibration masks, material markers and cross-arena transfer maps can re-enter the measured-GM bridge unless their chain-map/domain clauses are signed.",
        "",
        "So `epsilon_selector_GM_abs` stays live and explicit. The next target is the source-worldtube/projector chain-map: `delta Pi_W=0` and `[d,Pi_W]J_H=0`, or a readout-reentry bound pack.",
        "",
        "## Source Register",
        "",
        md_table(data["source_register"], ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
        "",
        "## Readout No-Reentry Gate",
        "",
        md_table(data["no_reentry_gate"], ["row_id", "readout_piece", "theorem_status", "result", "remaining_gap", "valid_for_claim"]),
        "",
        "## Selector Reentry Component Rows",
        "",
        md_table(data["selector_components"], ["row_id", "quantity", "component", "formula", "current_value", "score_ready", "valid_for_claim"]),
        "",
        "## Source GM Bridge Update",
        "",
        md_table(data["source_bridge_update"], ["row_id", "object", "status", "bridge_effect", "valid_for_claim"]),
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
        "This is a useful cut. Readout is not a villain; sloppy readout is. The framework now distinguishes harmless postprocessing from source-selecting maps that can corrupt the measured-GM bridge. Next we go after the chain-map condition directly.",
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
        "no_reentry_gate": no_reentry_gate_rows(),
        "selector_components": selector_component_rows(),
        "source_bridge_update": source_bridge_update_rows(),
        "claim_gates": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }

    write_csv(OUTPUTS["source_register"], data["source_register"])
    write_csv(OUTPUTS["no_reentry_gate"], data["no_reentry_gate"])
    write_csv(OUTPUTS["selector_components"], data["selector_components"])
    write_csv(OUTPUTS["source_bridge_update"], data["source_bridge_update"])
    write_csv(OUTPUTS["claim_gates"], data["claim_gates"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next_target"], data["next_target"])

    data["branch_copies"] = copy_branch_rows(data["no_reentry_gate"], data["selector_components"], data["decision"])
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
