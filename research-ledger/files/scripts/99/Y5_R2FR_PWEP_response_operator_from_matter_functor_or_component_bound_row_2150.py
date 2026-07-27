from __future__ import annotations

from pathlib import Path

from Y5_R2FR_Dq_vX_observed_metric_zero_or_finite_DObs_leak_row_2025 import (
    BRANCH_WEP,
    OUT,
    QUEUE,
    ROOT,
    SOURCE_WEIGHT_DOCS,
    base_row,
    count_formalization_modified,
    csv_rows_parse,
    md_table,
    read_text,
    remove_pycache,
    write_csv,
)


DOC = ROOT / "2150-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md"
REPO = ROOT.parent
FORMALIZATION = REPO / "formalization-workbench"

DOCS = {
    "2149": ROOT / "2149-Y5-R2FR-connection-hinge-bivector-owner-or-c2-map-fill.md",
    "1836": ROOT / "1836-Y5-R2FR-DeltaGamma-WEP-clock-lightcone-projection-skeleton.md",
    "1837": ROOT / "1837-Y5-R2FR-PWEP-response-operator-from-matter-functor-or-component-bound-row.md",
    "1838": ROOT / "1838-Y5-R2FR-ordinary-matter-action-signature-source-label-forgetting-or-WEP-bound-first-fill.md",
    "1839": ROOT / "1839-Y5-R2FR-source-shadow-ban-or-tauWEP-direct-product-first-source-row.md",
    "1840": ROOT / "1840-Y5-R2FR-EH-dominance-and-residual-sector-silence-or-operator-coefficient-pack.md",
    "1841": ROOT / "1841-Y5-R2FR-sector-action-variation-and-local-scaling-silence-or-operator-bounds.md",
}


def row(**kwargs: object) -> dict[str, object]:
    data = base_row()
    data["claim_allowed"] = False
    data.update(kwargs)
    return data


def truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "valid"}


def has_any(text: str, alternatives: list[str]) -> bool:
    return any(item in text for item in alternatives)


def find_line(path: Path, alternatives: list[str]) -> tuple[int, str]:
    text = read_text(path) if path.exists() else ""
    for line_number, line in enumerate(text.splitlines(), start=1):
        if has_any(line, alternatives):
            return line_number, line.strip()
    return 0, "MISSING_NEEDLE"


def formalization_has_2150_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    patterns = (
        "*2150-Y5-R2FR*",
        "*P8_Y5_PARENT_QLOC_2150*",
        "*Y5_R2FR_PWEP_response_operator_from_matter_functor_or_component_bound_row_2150*",
        "*AFRAME_PWEP_TO_EH_FRONTIER_2150*",
        "*JR2150*",
    )
    try:
        return any(path.is_file() for pattern in patterns for path in FORMALIZATION.rglob(pattern))
    except Exception:
        return False


def source_register_rows() -> list[dict[str, object]]:
    specs = [
        ("SRC2150_00_2149", DOCS["2149"], [["VAL2149_OVERALL"], ["P_WEP_FROM_MATTER_FUNCTOR_NEXT"]], "current handoff selects P_WEP response operator"),
        ("SRC2150_01_1836", DOCS["1836"], [["VAL1836_OVERALL"], ["P_WEP_FROM_MATTER_FUNCTOR_NEXT"], ["WEP_CLOCK_LIGHTCONE_PROJECTION_SKELETON_WRITTEN_NONCLAIM"]], "WEP/clock/lightcone projection skeleton"),
        ("SRC2150_02_1837", DOCS["1837"], [["VAL1837_OVERALL"], ["PWEP_ZERO_THEOREM_SHAPE_IS_EXACT_CONDITIONAL"], ["ORDINARY_MATTER_ACTION_SIGNATURE_NEXT"]], "exact conditional P_WEP zero theorem, not current proof"),
        ("SRC2150_03_1838", DOCS["1838"], [["VAL1838_OVERALL"], ["ORDINARY_MATTER_SIGNATURE_NOT_PARENT_SIGNED"], ["SOURCE_SHADOW_BAN_OR_TAUWEP_DIRECT_PRODUCT_NEXT"]], "ordinary matter/source-label route remains unsigned"),
        ("SRC2150_04_1839", DOCS["1839"], [["VAL1839_OVERALL"], ["SOURCE_SHADOW_CLASSIFIED_NOT_ZEROED"], ["EH dominance"]], "source-shadow classified but not killed; EH LHS handoff"),
        ("SRC2150_05_1840", DOCS["1840"], [["VAL1840_OVERALL"], ["EH_DOMINANCE_NOT_PARENT_PROVED"], ["SECTOR_ACTION_VARIATION_AND_LOCAL_SCALING_SILENCE_IS_NEXT"]], "EH dominance/residual operator pack"),
        ("SRC2150_06_1841", DOCS["1841"], [["VAL1841_OVERALL"], ["NO_NON_EH_SECTOR_FULLY_SILENCED"], ["sector Lagrangian/boundary owner"]], "sector variation/local scaling pushes to source-charge owner"),
    ]
    rows: list[dict[str, object]] = []
    for source_id, path, needle_groups, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles_found = exists and all(has_any(text, group) for group in needle_groups)
        rows.append(row(source_id=source_id, source_path=str(path), path_exists=exists, needles_found=needles_found, expected_needles="; ".join(" OR ".join(group) for group in needle_groups), role=role))
    return rows


def frontier_chain_rows() -> list[dict[str, object]]:
    chain = [
        ("PWF2150_0", "2149", "P_WEP live edge", "DeltaGamma projection frontier selects P_WEP from matter functor", "WEP response target"),
        ("PWF2150_1", "1836", "projection skeleton", "P_WEP, P_clock, P_lightcone declared with missing common units/projections", "no arena score-ready"),
        ("PWF2150_2", "1837", "P_WEP theorem", "universal observed-matter descent would force P_WEP=0", "exact conditional only"),
        ("PWF2150_3", "1838", "ordinary matter signature", "one ordinary matter action plus source-label forgetting would kill material WEP branch", "signature not parent-signed"),
        ("PWF2150_4", "1839", "source-shadow/tau sidecar", "source-shadow classified; tau_WEP/direct product acquisition staged nonclaim", "WEP scoring deferred"),
        ("PWF2150_5", "1840", "EH dominance handoff", "source-side pressure hands back to EH left-hand residual sectors", "EH dominance not proved"),
        ("PWF2150_6", "1841", "sector variation", "no non-EH sector fully silenced; obstruction becomes L_X/Theta_X/Q_X and M_H_ref owner", "source-charge owner next"),
    ]
    rows: list[dict[str, object]] = []
    for chain_id, checkpoint, object_name, gain, status in chain:
        source_path = DOCS[checkpoint]
        line_number, _ = find_line(source_path, ["Current verdict", "Current Verdict", "**Current verdict:**"])
        rows.append(row(chain_id=chain_id, checkpoint=checkpoint, source_path=str(source_path), verdict_line=line_number, object=object_name, gain=gain, current_status=status))
    return rows


def pwep_status_rows() -> list[dict[str, object]]:
    return [
        row(status_id="PWEP2150_0_exact_zero", object="P_WEP=0 conditional theorem", current_gain="universal observed-matter descent gives common-mode motion and WEP cancellation", blocker="ordinary matter functor, one observed frame, constants/current owner and readout kernels are not parent-signed", score_ready=False),
        row(status_id="PWEP2150_1_component_rows", object="WEP component-bound fallback", current_gain="spin/material/clock/projective/frame rows are staged with MICROSCOPE Ti/Pt bound anchors", blocker="component values, tau_WEP/direct product, common units and branch-locked product are missing", score_ready=False),
        row(status_id="PWEP2150_2_source_shadow", object="source-shadow label re-entry", current_gain="shadow source routes are classified into action, boundary, nonvariational, projector or decoupled blocks", blocker="not every source-like MTS term is classified/zeroed in one parent normal form", score_ready=False),
        row(status_id="PWEP2150_3_tau_direct", object="tau_WEP/direct product sidecar", current_gain="required official/source-backed inputs are explicit", blocker="no official readout/source/material/product rows are present for prediction scoring", score_ready=False),
        row(status_id="PWEP2150_4_handoff", object="WEP branch status", current_gain="WEP is disciplined but not promoted", blocker="left-hand EH residual sectors and source-normalization owner remain larger local-GR blockers", score_ready=False),
    ]


def eh_handoff_rows() -> list[dict[str, object]]:
    return [
        row(handoff_id="EH2150_0_EH_dominance", object="local Einstein-Hilbert LHS", current_status="NOT_PARENT_PROVED", required_next="zero/suppress all retained non-EH sectors or carry coefficients"),
        row(handoff_id="EH2150_1_DeltaE_pack", object="DeltaE_munu residual operator pack", current_status="STAGED_NONCLAIM", required_next="sector basis, coefficient units, local scaling and arena maps"),
        row(handoff_id="EH2150_2_sector_variation", object="sector-by-sector first variation", current_status="NO_SECTOR_FULLY_SILENCED", required_next="action owner, theta/Q accounting, boundary/reference lock and local scaling"),
        row(handoff_id="EH2150_3_source_charge_owner", object="L_X/Theta_X/Q_X plus M_H_ref owner", current_status="PRIMARY_NEXT_FRONTIER", required_next="derive Hamiltonian/source charge denominator or fill FB5540 row"),
        row(handoff_id="EH2150_4_Newton", object="Newton/Poisson reduction", current_status="BEHIND_EH_AND_SOURCE_NORMALIZATION", required_next="EH weak-field limit plus measured-G/worldtube source owner"),
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        row(decision_id="DEC2150_0_pwep", decision="PWEP_ZERO_CONDITIONAL_NOT_CURRENT_CLAIM", because="the WEP theorem is clean only if ordinary matter descent and source-label forgetting are parent-signed", next_action="do not score WEP or claim local GR"),
        row(decision_id="DEC2150_1_wep_sidecar", decision="WEP_COMPONENT_ROWS_STAGED_NONCLAIM", because="Delta_w_TiPt, tau_WEP/direct product and MICROSCOPE comparator are explicit but missing source-backed prediction inputs", next_action="hold WEP acquisition sidecar"),
        row(decision_id="DEC2150_2_handoff", decision="RETURN_TO_EH_LEFT_HAND_GATE", because="source-shadow/tau rows are acquisition-ready but the left-hand operator still lacks EH dominance", next_action="focus on sector variation/source-charge owner"),
        row(decision_id="DEC2150_3_next", decision="SECTOR_LAGRANGIAN_BOUNDARY_OWNER_NEXT", because="1841 shows no non-EH sector is silenced and the primary owner gap is L_X/Theta_X/Q_X plus M_H_ref", next_action="2151 source-charge owner or FB5540 row"),
        row(decision_id="DEC2150_4_claim_policy", decision="NO_LOCAL_GR_NEWTON_CLAIM", because="P_WEP, EH dominance, source normalization and empirical residual maps remain nonclaim", next_action="continue private derivation/test discipline"),
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        row(
            route_id="NEXT2150_0_2151",
            next_target="2151-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
            script="scripts/Y5_R2FR_sector_Lagrangian_boundary_owner_or_FB5540_source_row_2151.py",
            objective="Derive L_X, Theta_X, Q_X plus boundary/reference/tau ownership for the Hamiltonian source charge and M_H_ref denominator; if not, fill FB5540 numerator/denominator rows with units, signs, source paths and no-cancellation bookkeeping.",
            forbidden_shortcuts="do not claim WEP from conditional P_WEP; do not score WEP from tau shortcuts; do not assert EH dominance by notation; do not absorb residuals into measured G; no formalization-workbench edits; no GitHub action",
        )
    ]


def write_branch_copies(chain: list[dict[str, object]], pwep: list[dict[str, object]], eh: list[dict[str, object]], next_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    copies = [
        ("COPY2150_0_source_weight_docs", SOURCE_WEIGHT_DOCS / "AFRAME_PWEP_TO_EH_FRONTIER_2150_NONCLAIM.csv", pwep + eh),
        ("COPY2150_1_branch_locked_wep", BRANCH_WEP / "P8_Y5_PARENT_QLOC_2150_PWEP_NONCLAIM_STATUS.csv", chain + pwep),
        ("COPY2150_2_acquisition_queue", QUEUE / "JR2150_SECTOR_OWNER_FB5540_QUEUE.csv", next_rows + eh),
    ]
    results: list[dict[str, object]] = []
    for copy_id, destination, rows_to_write in copies:
        write_csv(destination, rows_to_write)
        results.append(row(copy_id=copy_id, destination=str(destination), path_exists=destination.exists(), row_count=len(rows_to_write), parse_ok=csv_rows_parse(destination)))
    return results


def validation_rows(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    pwep: list[dict[str, object]],
    eh: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    csv_paths: list[Path],
) -> list[dict[str, object]]:
    sources_ok = all(truthy(item["path_exists"]) and truthy(item["needles_found"]) for item in sources)
    chain_ok = len(chain) == 7 and chain[0]["checkpoint"] == "2149" and chain[-1]["checkpoint"] == "1841"
    pwep_ok = any(item["status_id"] == "PWEP2150_0_exact_zero" for item in pwep) and all(not truthy(item.get("score_ready", False)) for item in pwep)
    eh_ok = any(item["handoff_id"] == "EH2150_3_source_charge_owner" and item["current_status"] == "PRIMARY_NEXT_FRONTIER" for item in eh)
    decisions_ok = any(item["decision"] == "RETURN_TO_EH_LEFT_HAND_GATE" for item in decisions) and any(item["decision"] == "NO_LOCAL_GR_NEWTON_CLAIM" for item in decisions)
    next_ok = any(item["route_id"] == "NEXT2150_0_2151" for item in next_rows)
    copies_ok = all(truthy(item["path_exists"]) and truthy(item["parse_ok"]) for item in copies)
    csv_ok = all(path.exists() and csv_rows_parse(path) for path in csv_paths)
    no_claim_flags = all(
        not truthy(item.get("claim_allowed", False)) and not truthy(item.get("valid_for_claim", False))
        for group in (sources, chain, pwep, eh, decisions, next_rows, copies)
        for item in group
    )
    formalization_clean = count_formalization_modified() == 0 and not formalization_has_2150_artifacts()
    pycache_clean = not (Path(__file__).resolve().parent / "__pycache__").exists()
    all_ok = all([sources_ok, chain_ok, pwep_ok, eh_ok, decisions_ok, next_ok, copies_ok, csv_ok, no_claim_flags, formalization_clean, pycache_clean])
    checks = [
        ("VAL2150_00_sources", sources_ok, "2149 and 1836-1841 source checkpoints validate"),
        ("VAL2150_01_chain", chain_ok, "frontier chain runs from P_WEP target to 1841 sector/source-owner frontier"),
        ("VAL2150_02_pwep", pwep_ok, "P_WEP is exact conditional but not score-ready"),
        ("VAL2150_03_eh_handoff", eh_ok, "EH/source-charge owner is selected as primary next frontier"),
        ("VAL2150_04_decisions", decisions_ok, "decisions block WEP/local claims and return to EH LHS gate"),
        ("VAL2150_05_next", next_ok, "next target is 2151 sector Lagrangian/boundary owner or FB5540 row"),
        ("VAL2150_06_branch_copies", copies_ok, "branch copies exist and parse"),
        ("VAL2150_07_csv_parse", csv_ok, "all generated CSVs parse cleanly"),
        ("VAL2150_08_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL2150_09_formalization_clean", formalization_clean, "formalization-workbench untouched by 2150"),
        ("VAL2150_10_no_pycache", pycache_clean, "scripts __pycache__ removed"),
        ("VAL2150_OVERALL", all_ok, "2150 syncs P_WEP work to EH/source-owner frontier and keeps all WEP/local-GR claims blocked."),
    ]
    return [row(check_id=check_id, status="PASS" if passed else "FAIL", detail=detail) for check_id, passed, detail in checks]


def write_doc(
    sources: list[dict[str, object]],
    chain: list[dict[str, object]],
    pwep: list[dict[str, object]],
    eh: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    copies: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    content = "\n\n".join(
        [
            "# 2150 - Y5/R2FR P_WEP Response Operator From Matter Functor Or Component Bound Row",
            "## Current Verdict",
            "2150 does **not** prove WEP, `P_WEP=0`, MICROSCOPE scoring, local GR, Newton, PPN, clocks, R10, orbital tests, or any public claim. It syncs the current WEP response target to the deepest verified private frontier.",
            "The clean result is conditional: if ordinary matter universally descends through one observed coframe/metric/current/measure owner with no source-only species labels or readout re-entry, then `P_WEP=0`. Current MTS does not parent-sign that full matter signature, so WEP component-bound rows stay nonclaim.",
            "The strategic result is a handoff: WEP/source-shadow rows are disciplined and acquisition-ready, but the bigger local-GR blocker is now the left-hand EH/operator/source-normalization gate. The next pressure point is `L_X, Theta_X, Q_X` plus boundary/reference/tau ownership for `M_H_ref` and the FB5540 numerator pack.",
            "## Source Register",
            md_table(sources, ["source_id", "source_path", "path_exists", "needles_found", "role", "valid_for_claim"]),
            "## Frontier Chain",
            md_table(chain, ["chain_id", "checkpoint", "verdict_line", "object", "gain", "current_status", "valid_for_claim"]),
            "## P_WEP Status",
            md_table(pwep, ["status_id", "object", "current_gain", "blocker", "score_ready", "valid_for_claim"]),
            "## EH Handoff",
            md_table(eh, ["handoff_id", "object", "current_status", "required_next", "valid_for_claim"]),
            "## Decision Ledger",
            md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "## Next Target",
            md_table(next_rows, ["route_id", "next_target", "script", "objective", "forbidden_shortcuts", "valid_for_claim"]),
            "## Branch Copies",
            md_table(copies, ["copy_id", "destination", "path_exists", "row_count", "parse_ok", "valid_for_claim"]),
            "## Validation",
            md_table(validation, ["check_id", "status", "detail", "claim_allowed", "valid_for_claim"]),
        ]
    )
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCE_WEIGHT_DOCS.mkdir(parents=True, exist_ok=True)
    BRANCH_WEP.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    chain = frontier_chain_rows()
    pwep = pwep_status_rows()
    eh = eh_handoff_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    paths = {
        "sources": OUT / "P8_Y5_PARENT_QLOC_2150_SOURCE_REGISTER.csv",
        "chain": OUT / "P8_Y5_PARENT_QLOC_2150_FRONTIER_CHAIN.csv",
        "pwep": OUT / "P8_Y5_PARENT_QLOC_2150_PWEP_STATUS.csv",
        "eh": OUT / "P8_Y5_PARENT_QLOC_2150_EH_HANDOFF.csv",
        "decisions": OUT / "P8_Y5_PARENT_QLOC_2150_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_PARENT_QLOC_2150_NEXT_TARGET.csv",
        "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2150_BRANCH_COPIES.csv",
        "validation": OUT / "P8_Y5_BRR545_2150_VALIDATION.csv",
    }

    write_csv(paths["sources"], sources)
    write_csv(paths["chain"], chain)
    write_csv(paths["pwep"], pwep)
    write_csv(paths["eh"], eh)
    write_csv(paths["decisions"], decisions)
    write_csv(paths["next"], next_rows)

    copies = write_branch_copies(chain, pwep, eh, next_rows)
    write_csv(paths["branch_copies"], copies)

    remove_pycache()
    csv_paths = [path for key, path in paths.items() if key != "validation"] + [Path(str(copy["destination"])) for copy in copies]
    validation = validation_rows(sources, chain, pwep, eh, decisions, next_rows, copies, csv_paths)
    write_csv(paths["validation"], validation)
    write_doc(sources, chain, pwep, eh, decisions, next_rows, copies, validation)

    print(f"wrote {DOC}")
    print(f"validation {paths['validation']}")


if __name__ == "__main__":
    main()
