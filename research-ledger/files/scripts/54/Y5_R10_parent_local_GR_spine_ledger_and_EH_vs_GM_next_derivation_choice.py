from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "957-Y5-R10-parent-local-GR-spine-ledger-and-EH-vs-GM-next-derivation-choice.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "956_doc",
            "path": "956-Y5-R10-source-side-GR-reduction-spine-and-left-hand-EH-gate-map.md",
            "role": "handoff: source-side spine and left-hand EH/Newton gates",
            "needle": "full GR/Newton reduction not claimable yet",
        },
        {
            "source_id": "956_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_956_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V956_12_validation_rows_ready",
        },
        {
            "source_id": "956_source_spine",
            "path": "source-intake/mts_residuals/P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv",
            "role": "source-side GR/Newton conditional spine",
            "needle": "SSG956_5_source_side_verdict",
        },
        {
            "source_id": "956_left_hand_gates",
            "path": "source-intake/mts_residuals/P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv",
            "role": "left-hand EH/Newton gate map",
            "needle": "LHG956_0_EH_core_selection",
        },
        {
            "source_id": "956_hidden_gates",
            "path": "source-intake/mts_residuals/P8_Y5_R10_956_HIDDEN_CURRENT_BYPASS_GATES.csv",
            "role": "hidden current bypass gates",
            "needle": "HCG956_5_worldtube_source_measure",
        },
        {
            "source_id": "510_worldtube_doc",
            "path": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
            "role": "worldtube/source-measure glue theorem route and dependencies",
            "needle": "MTS_transfer_premises_open",
        },
        {
            "source_id": "509_flux_theorem",
            "path": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
            "role": "source-measure flux theorem rows",
            "needle": "T509_2_no_extra_mass_channel",
        },
        {
            "source_id": "509_flux_clauses",
            "path": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
            "role": "measured-GM/source-measure clauses",
            "needle": "SM509_6_Gauss_orbital_calibration",
        },
        {
            "source_id": "529_EH_blockers",
            "path": "source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_BLOCKERS.csv",
            "role": "highest-priority EH/source-calibrated blockers",
            "needle": "BL529_1_measured_GM",
        },
        {
            "source_id": "529_EH_stack",
            "path": "source-intake/mts_residuals/P8_Y5_SOURCE_CALIBRATED_EH_PROOF_STACK.csv",
            "role": "source-calibrated EH proof stack",
            "needle": "SCEH529_7_beta_local_GR_gate",
        },
        {
            "source_id": "655_EH_premises",
            "path": "source-intake/mts_residuals/P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
            "role": "EH-only premise audit",
            "needle": "EHP655_P6_second_order",
        },
        {
            "source_id": "912_EH_baseline",
            "path": "source-intake/mts_residuals/P8_Y5_R10_912_EH_CORE_BASELINE.csv",
            "role": "conditional EH baseline and omega-extra warning",
            "needle": "EHB912_3_EH_does_not_silence_extras",
        },
    ]
    rows = []
    for spec in specs:
        path = source_path(spec["path"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_local_gr_spine_ledger() -> list[dict[str, str]]:
    return [
        {
            "ledger_id": "PLG957_0_observed_frame",
            "layer": "frame/readout",
            "requirement": "one observed coframe/metric across matter, source, clocks, photons, orbital and PPN readout",
            "current_state": "conditional_not_full_PPN_parent_closure",
            "blocks": "all local observable comparisons if split",
            "next_needed": "same-frame/readout theorem through O(U^2)",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ledger_id": "PLG957_1_source_side",
            "layer": "right-hand/source",
            "requirement": "source side equals one common kappa times total Hilbert matter current",
            "current_state": "conditional_spine_from_953_956",
            "blocks": "WEP/source-normalization/local Newton claim if hidden source weights survive",
            "next_needed": "parent no-source-prefactor theorem or sourced species-weight residual bounds",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ledger_id": "PLG957_2_EH_operator",
            "layer": "left-hand/operator",
            "requirement": "compact local exterior field operator reduces to EH plus harmless Lambda/background",
            "current_state": "not_parent_derived_highest_priority",
            "blocks": "EH charge inheritance, one-parameter no-hair, PPN vector, measured-GM transfer",
            "next_needed": "metric-only second-order EH selection theorem or executable R11/nonEH residual vector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ledger_id": "PLG957_3_extra_sector_silence",
            "layer": "hidden/extra sectors",
            "requirement": "motion/time/domain/memory/projector/boundary/connection sectors carry no independent local charge/stress",
            "current_state": "active_primary_obstruction",
            "blocks": "EH integrability, no-hair, source mass, PPN vector",
            "next_needed": "sector-specific no-hair/topological/gauge silence or sourced residual rows",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ledger_id": "PLG957_4_worldtube_GM",
            "layer": "Newton/source-measure",
            "requirement": "worldtube dressed source charge equals exterior charge and measured orbital GM",
            "current_state": "not_derived_depends_on_EH_charge_transfer",
            "blocks": "Newtonian mechanics reduction even if equation shape is EH-like",
            "next_needed": "Noether/Hamiltonian charge inheritance, fixed Pi_M, flux closure, Gauss/orbital calibration",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "ledger_id": "PLG957_5_PPN_completion",
            "layer": "empirical local tests",
            "requirement": "all PPN and local residual components are theorem-zero or scored below bounds without cancellation",
            "current_state": "promotion_gates_fail_for_claim",
            "blocks": "local GR claim after any leading-order Newton-looking result",
            "next_needed": "fill/theorem-zero residual vector rows for gamma, beta, alpha_i, xi, Gdot/range/source terms",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def branch_scorecard() -> list[dict[str, str]]:
    return [
        {
            "branch_id": "B957_EH_OPERATOR",
            "branch": "EH-only operator selection",
            "primary_question": "Does the local exterior MTS operator reduce to metric-only second-order EH plus harmless background?",
            "unlocks": "EH charge baseline; one-parameter no-hair; nonEH/R11 residual cleanup; PPN operator side; prerequisite for MTS worldtube transfer",
            "depends_on": "observed-frame clause; extra-sector silence or retained residual vector",
            "risk": "broad and hard; must confront scalar/vector/domain/boundary/connection sectors",
            "evidence_priority": "highest_BL529_0_and_central_EHP655_P6",
            "score_upstream_leverage": "5",
            "score_tractability": "3",
            "score_direct_Newton_relevance": "4",
            "score_total": "12",
            "selected_next": "true",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "branch_id": "B957_GM_WORLDTUBE",
            "branch": "measured-GM/worldtube calibration",
            "primary_question": "Does the dressed worldtube Hamiltonian/Noether charge equal exterior mass and orbital GM?",
            "unlocks": "Newtonian source normalization; radial M_eff closure; Gdot/range/source-measure guardrail",
            "depends_on": "EH/symplectic charge inheritance; fixed Pi_M; extra-sector charge silence; Gauss/orbital readout",
            "risk": "narrower, but current 510 route says MTS transfer premises depend on EH fixed point and extra-sector silence",
            "evidence_priority": "highest_BL529_1_but_downstream_of_EH_charge_transfer",
            "score_upstream_leverage": "4",
            "score_tractability": "4",
            "score_direct_Newton_relevance": "5",
            "score_total": "13_raw_but_dependency_penalty_select_second",
            "selected_next": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def dependency_ordering() -> list[dict[str, str]]:
    return [
        {
            "order_id": "ORD957_0",
            "step": "observed-frame/source-side contract",
            "why_before_next": "otherwise EH/GM/PPN readouts can refer to different geometries",
            "status": "conditional_spine_available_not_full_claim",
            "next_use": "input to EH and GM branches",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "order_id": "ORD957_1",
            "step": "EH/operator fixed point",
            "why_before_next": "worldtube theorem transfer needs EH/symplectic charge inheritance and extra-sector control",
            "status": "selected_next_branch",
            "next_use": "958 EH-core selection/no-extra-operator pass",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "order_id": "ORD957_2",
            "step": "worldtube/measured-GM calibration",
            "why_before_next": "after EH charge baseline, prove the mass parameter equals dressed source charge and orbital GM",
            "status": "queued_second_not_dropped",
            "next_use": "Newtonian mechanics reduction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "order_id": "ORD957_3",
            "step": "PPN residual vector completion",
            "why_before_next": "local GR cannot be claimed from leading Newtonian order alone",
            "status": "later_full_claim_gate",
            "next_use": "solar-system/local-GR robustness pass",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_branch_contract() -> list[dict[str, str]]:
    return [
        {
            "contract_id": "NBC957_0_EH_core_target",
            "required_deliverable": "minimal EH-core selection theorem attempt",
            "mathematical_form": "E_MTS = G_munu + Lambda g_munu + DeltaE_extra; prove DeltaE_extra=0 or classify residuals",
            "acceptance_gate": "each nonEH/R11/extra operator term is absent, gauge/topological/no-hair, or retained with executable coefficient row",
            "failure_output": "R11/nonEH residual vector with source paths and no placeholders",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "NBC957_1_metric_only_second_order",
            "required_deliverable": "metric-only second-order premise audit",
            "mathematical_form": "local 4D diffeo-invariant metric-only second-order action -> EH+Lambda style operator",
            "acceptance_gate": "connection, nonmetricity, torsion, scalar/vector, nonlocal, and higher-derivative terms are parent-excluded or residualized",
            "failure_output": "operator-family table by sector with bound route",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "NBC957_2_symplectic_charge_transfer",
            "required_deliverable": "EH charge baseline transfer precondition",
            "mathematical_form": "omega_total = omega_EH + omega_extra; require omega_extra=0/gauge/topological/no-flux or bounded",
            "acceptance_gate": "no extra-sector symplectic flux contaminates Hamiltonian mass charge",
            "failure_output": "omega_extra residual ledger feeding worldtube/PPN gates",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "contract_id": "NBC957_3_no_claim_guard",
            "required_deliverable": "explicit no-promotion policy",
            "mathematical_form": "EH_selected=false until parent proof or executable residual vector passes",
            "acceptance_gate": "no local-GR/Newton/PPN claim promoted from EH baseline alone",
            "failure_output": "blocker ledger, not public theorem prose",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC957_0_branch_choice",
            "topic": "EH vs measured-GM next derivation",
            "result": "select_EH_operator_first_GM_second",
            "reason": "measured-GM/worldtube is essential, but current worldtube transfer explicitly depends on EH/symplectic fixed point and extra-sector silence; EH/operator branch is upstream",
            "next_action": "attempt EH-core operator selection or produce executable R11/nonEH residual vector",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC957_1_project_state",
            "topic": "parent-local-GR bridge",
            "result": "not_claimable_but_ordered",
            "reason": "the required bridge is now ordered into source side, EH/operator side, measured-GM calibration, and PPN completion",
            "next_action": "use the 957 ledger as the local-GR roadmap and avoid mixing branch claims",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC957_2_GM_route",
            "topic": "measured-GM/worldtube route",
            "result": "queued_not_rejected",
            "reason": "GM calibration is required for Newton, but should be attacked once EH charge baseline and omega_extra control are clearer",
            "next_action": "carry GM clauses forward as immediate downstream branch after EH-core attempt",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE957_0_EH_selected",
            "claim": "MTS local exterior selects EH operator",
            "required_condition": "958 branch proves metric-only second-order EH core or executable residual vector passes bounds",
            "current_evidence": "selected as next derivation; not yet proved",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE957_1_Newton_GM",
            "claim": "MTS derives Newtonian measured-GM source calibration",
            "required_condition": "EH/symplectic charge transfer plus worldtube/Gauss/orbital calibration",
            "current_evidence": "queued downstream; dependencies open",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE957_2_local_GR",
            "claim": "MTS local-GR/PPN branch passes",
            "required_condition": "source side, EH side, measured-GM side, hidden-current side, and full PPN vector all pass",
            "current_evidence": "roadmap only; multiple gates open",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "958-Y5-R10-EH-core-operator-selection-or-executable-R11-nonEH-vector.md",
            "objective": "attempt the EH-core metric-only second-order operator selection branch; if it fails, create an executable R11/nonEH residual vector with required source/projection fields and no placeholders accepted for claim",
            "include": "EH baseline, local 4D metric-only premises, second-order/Lovelock-style gate, extra-sector omega silence, R11/nonEH vector fallback",
            "exclude": "measured-GM claim, local-GR claim, invented coefficients, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    spine_rows: list[dict[str, str]],
    score_rows: list[dict[str, str]],
    order_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_956_VALIDATION.csv"))
    spine_complete = len(spine_rows) == 6 and any(row["ledger_id"] == "PLG957_4_worldtube_GM" for row in spine_rows)
    branch_selected = any(row["branch_id"] == "B957_EH_OPERATOR" and row["selected_next"] == "true" for row in score_rows)
    gm_queued = any(row["branch_id"] == "B957_GM_WORLDTUBE" and row["selected_next"] == "false" for row in score_rows)
    order_clean = len(order_rows) == 4 and order_rows[1]["status"] == "selected_next_branch"
    contract_ready = len(contract_rows) == 4 and all(row["valid_for_claim"] == "false" for row in contract_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = bool(target_rows) and target_rows[0]["next_target"].startswith("958-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, spine_rows, score_rows, order_rows, contract_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V957_0_sources_exist_and_needles", sources_ok, "all 957 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V957_1_prior_956_clean", prior_clean, "P8_Y5_BRR545_956_VALIDATION.csv clean")
    add("V957_2_spine_ledger_complete", spine_complete, "parent-local-GR spine ledger covers source, EH, GM, PPN layers")
    add("V957_3_EH_branch_selected", branch_selected, "EH/operator selection chosen as upstream next branch")
    add("V957_4_GM_branch_queued", gm_queued, "measured-GM/worldtube branch queued second, not rejected")
    add("V957_5_dependency_order_clean", order_clean, "dependency ordering keeps EH before GM transfer")
    add("V957_6_next_contract_ready", contract_ready, "958 EH/R11 branch contract written")
    add("V957_7_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V957_8_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V957_9_next_target_selected", target_selected, "958 EH-core operator branch selected")
    add("V957_10_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V957_11_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V957_12_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    spine_rows: list[dict[str, str]],
    score_rows: list[dict[str, str]],
    order_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 957 Y5 R10: Parent Local-GR Spine Ledger And EH Vs GM Next Derivation Choice

Status: `Y5_R10_957_parent_local_GR_spine_ordered_EH_operator_selected_GM_queued_nonclaim`

Claim ceiling: `roadmap_and_branch_selection_only_no_EH_claim_no_Newton_claim_no_local_GR_claim`

## Result

This checkpoint turns the local-GR bridge into an ordered ledger.

The source side is now a conditional but sharp route. The two remaining big boss fights are EH/operator selection and measured-GM/worldtube calibration. Both matter. The choice for the next derivation is EH/operator selection first, measured-GM second.

Why? Because the worldtube/measured-GM route is not rejected — it is essential for Newton. But the existing worldtube theorem route says MTS inherits the GR-style source-measure glue only after EH/symplectic charge transfer, fixed projector, and extra-sector charge silence. That makes EH/operator selection the upstream branch.

```text
next selected: EH-core operator selection / R11-nonEH residual vector.
queued second: measured-GM/worldtube calibration.
no claim promoted: this is a branch-ordering checkpoint.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Parent Local-GR Spine Ledger

{md_table(spine_rows, ["ledger_id", "layer", "requirement", "current_state", "blocks", "next_needed"])}

## Branch Scorecard

{md_table(score_rows, ["branch_id", "branch", "evidence_priority", "score_total", "selected_next", "risk"])}

## Dependency Ordering

{md_table(order_rows, ["order_id", "step", "why_before_next", "status", "next_use"])}

## Next Branch Contract

{md_table(contract_rows, ["contract_id", "required_deliverable", "acceptance_gate", "failure_output"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    spine_rows = parent_local_gr_spine_ledger()
    score_rows = branch_scorecard()
    order_rows = dependency_ordering()
    contract_rows = next_branch_contract()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, spine_rows, score_rows, order_rows, contract_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_957_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_957_PARENT_LOCAL_GR_SPINE_LEDGER.csv",
        spine_rows,
        ["ledger_id", "layer", "requirement", "current_state", "blocks", "next_needed", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_957_BRANCH_SCORECARD.csv",
        score_rows,
        [
            "branch_id",
            "branch",
            "primary_question",
            "unlocks",
            "depends_on",
            "risk",
            "evidence_priority",
            "score_upstream_leverage",
            "score_tractability",
            "score_direct_Newton_relevance",
            "score_total",
            "selected_next",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_957_DEPENDENCY_ORDERING.csv",
        order_rows,
        ["order_id", "step", "why_before_next", "status", "next_use", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_957_NEXT_BRANCH_CONTRACT.csv",
        contract_rows,
        ["contract_id", "required_deliverable", "mathematical_form", "acceptance_gate", "failure_output", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_957_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_957_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_957_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_957_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, spine_rows, score_rows, order_rows, contract_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
