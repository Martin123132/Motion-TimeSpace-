from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1511-Y5-parent-GR-Newton-reentry-spine-inventory-and-strongest-local-limit-contract.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1510_validation": OUT / "P8_Y5_BRR545_1510_VALIDATION.csv",
    "1510_reentry_plan": OUT / "P8_Y5_R10_1510_PARENT_GR_DERIVATION_REENTRY_PLAN.csv",
    "1510_local_status": OUT / "P8_Y5_R10_1510_LOCAL_GR_NEWTON_STATUS.csv",
    "868_reduction_chain": OUT / "P8_Y5_R10_868_LOCAL_GR_REDUCTION_CHAIN.csv",
    "868_blockers": OUT / "P8_Y5_R10_868_LOCAL_GR_BLOCKER_AUDIT.csv",
    "907_rollup": OUT / "P8_Y5_R10_907_LOCAL_GR_RESIDUAL_STACK_ROLLUP.csv",
    "956_gate_map": OUT / "P8_Y5_R10_956_LEFT_HAND_EH_NEWTON_GATE_MAP.csv",
    "956_source_spine": OUT / "P8_Y5_R10_956_SOURCE_SIDE_GR_NEWTON_SPINE.csv",
    "957_parent_spine": OUT / "P8_Y5_R10_957_PARENT_LOCAL_GR_SPINE_LEDGER.csv",
    "958_eh_premise": OUT / "P8_Y5_R10_958_EH_PREMISE_AUDIT.csv",
    "958_eh_attempt": OUT / "P8_Y5_R10_958_EH_CORE_SELECTION_ATTEMPT.csv",
    "990_ladder": OUT / "P8_Y5_R10_990_GR_NEWTON_REENTRY_LADDER.csv",
    "1212_parent_lhs": OUT / "P8_Y5_R10_1212_PARENT_LHS_EH_NEWTON_ATTEMPT.csv",
    "1339_eh_gate": OUT / "P8_Y5_R10_1339_EH_LEFT_HAND_REDUCTION_GATE.csv",
    "1339_newton_blockers": OUT / "P8_Y5_R10_1339_NEWTON_TRANSFER_BLOCKERS.csv",
    "1473_newton_ppn": OUT / "P8_Y5_R10_1473_NEWTON_PPN_LOCAL_GR_GATE_UPDATE.csv",
    "1485_verdict": OUT / "P8_Y5_R10_1485_LOCAL_GR_NEWTON_REDUCTION_VERDICT.csv",
}

ARTIFACT_INVENTORY = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_ARTIFACT_INVENTORY.csv"
CONTRACT = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_MINIMAL_LOCAL_LIMIT_CONTRACT.csv"
CLAIM_LEDGER = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_STRONGEST_CLAIMS_LEDGER.csv"
BLOCKER_STACK = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_OPEN_BLOCKER_STACK.csv"
PRIORITY_DECISION = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_DERIVATION_PRIORITY_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_LOCAL_GR_NEWTON_STATUS.csv"
SCORE_READINESS = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_SCORE_READINESS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_REJECTION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_GR_NEWTON_1511_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1511_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1511"
QUAR_INVENTORY = QUARANTINE / "PARENT_GR_NEWTON_ARTIFACT_INVENTORY_NONCLAIM.csv"
QUAR_CONTRACT = QUARANTINE / "MINIMAL_LOCAL_LIMIT_CONTRACT_NONCLAIM.csv"
QUAR_PRIORITY = QUARANTINE / "DERIVATION_PRIORITY_DECISION_NONCLAIM.csv"
BRANCH_INVENTORY = BRANCH_RESIDUALS / "parent_gr_newton_artifact_inventory_nonclaim_1511.csv"
BRANCH_CONTRACT = BRANCH_RESIDUALS / "parent_gr_newton_minimal_local_limit_contract_nonclaim_1511.csv"
BRANCH_PRIORITY = BRANCH_RESIDUALS / "parent_gr_newton_derivation_priority_decision_nonclaim_1511.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "passes_for_claim", "R10_pass_for_claim"]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def inventory_rows() -> list[dict[str, Any]]:
    rows = [
        ("INV1511_0_868_chain", "868 local-GR reduction chain", "full local-GR reduction stack from quotient/matter descent to PPN vector", "strong_required_chain", "conditional/open; no claim", source_list("868_reduction_chain", "868_blockers")),
        ("INV1511_1_907_rollup", "907 residual stack rollup", "prioritizes EH operator and projector/Bianchi as highest blockers", "strong_priority_evidence", "nonclaim priority map", source_list("907_rollup")),
        ("INV1511_2_956_left_hand", "956 left-hand EH/Newton gate map", "EH core, extra-sector silence, nohair, measured-GM, constant source normalization, PPN completion", "strong_gate_map", "all claim flags false", source_list("956_gate_map")),
        ("INV1511_3_956_source", "956 source-side GR/Newton spine", "ordinary source side can be standard if one coframe, no source-only species slot, total Hilbert source, common kappa", "conditional_source_spine", "not parent signed", source_list("956_source_spine")),
        ("INV1511_4_957_parent_spine", "957 parent local-GR spine ledger", "six-layer parent spine from observed frame to PPN completion", "strong_rollup", "EH operator highest priority and extra sectors active", source_list("957_parent_spine")),
        ("INV1511_5_958_EH_attempt", "958 EH core selection attempt", "Lovelock-style route known if local 4D metric-only second-order LC no-extra-field premises close", "best_EH_theorem_shape", "not parent derived", source_list("958_eh_premise", "958_eh_attempt")),
        ("INV1511_6_990_ladder", "990 GR/Newton reentry ladder", "source mass was live edge earlier, but operator remains blocked", "useful_ladder", "needs updated selection after R10 freeze", source_list("990_ladder")),
        ("INV1511_7_1212_parent_lhs", "1212 parent LHS EH/Newton attempt", "guards against importing EH or GR smuggling; parent LHS zero blocked", "critical_guardrail", "parent LHS not derived", source_list("1212_parent_lhs")),
        ("INV1511_8_1339_EH_gate", "1339 EH left-hand gate", "metric-only local 4D, second-order, Levi-Civita, extra-sector silence, source-GM transfer", "strongest_operator_gate", "central blockers remain", source_list("1339_eh_gate")),
        ("INV1511_9_1339_Newton", "1339 Newton transfer blockers", "Newton needs EH operator, source closure, and GM calibration", "strong_Newton_guard", "Newton claim blocked", source_list("1339_newton_blockers")),
        ("INV1511_10_1473_PPN", "1473 Newton/PPN gate update", "double-zero, Newton, and PPN fail for claim but residual policy passes", "good_nonclaim_policy", "no promotion", source_list("1473_newton_ppn")),
        ("INV1511_11_1485_verdict", "1485 reduction verdict", "best derivation route was quotient descent of ordinary matter, but PPN/readout and WEP products remain open", "source_side_hint", "not full local-GR", source_list("1485_verdict")),
        ("INV1511_12_1510_reentry", "1510 R10 freeze and GR reentry", "R10 frozen; parent GR/Newton route selected", "current_route_authority", "continue derivation", source_list("1510_reentry_plan", "1510_local_status", "1510_validation")),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "inventory_id": inventory_id,
            "artifact": artifact,
            "contribution": contribution,
            "strength": strength,
            "claim_status": status,
            "source_paths": sources,
            **flags(),
        }
        for inventory_id, artifact, contribution, strength, status, sources in rows
    ]


def contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("LLC1511_0_branch_selector", "local branch selector", "compact non-cosmological branch with q_loc/observed quotient owned by parent", "q_loc(Phi) exists and local observables factor through it", "CONDITIONAL_NOT_PARENT_SIGNED", "868"),
        ("LLC1511_1_observed_frame", "one observed metric/coframe", "ordinary matter, clocks, photons, orbital readout share e_obs/g_obs through PPN order", "e_obs=e_matter=e_source=e_readout up to O(U^2)", "CONDITIONAL_NOT_FULL_PPN_SIGNED", "956/957/1339"),
        ("LLC1511_2_matter_source", "minimal matter/source side", "source is one common kappa times total Hilbert matter current with no species/source-only slot", "delta S_matter/delta e_obs = T_total and kappa_univ calibrated", "CONDITIONAL_CONTRACT_NOT_PARENT_SIGNED", "956/1485"),
        ("LLC1511_3_EH_operator", "Einstein-Hilbert left-hand operator", "local exterior metric action is 4D, diffeo-invariant, metric-only, Levi-Civita, second-order", "E_MTS^{mu nu}=G^{mu nu}+Lambda g^{mu nu}+DeltaE_extra", "CENTRAL_BLOCKER_NOT_DERIVED", "958/1339"),
        ("LLC1511_4_extra_silence", "extra-sector silence", "motion/time/domain/memory/projector/boundary/connection sectors are zero, gauge, topological no-flux, no-haired, or bounded", "DeltaE_extra=0 or explicit residual vector", "ACTIVE_PRIMARY_OBSTRUCTION", "907/956/957"),
        ("LLC1511_5_bianchi", "Bianchi/conservation safety", "all retained residual stress is conserved and no hidden q_loc force exchange survives", "nabla_mu E_total^{mu nu}=0 and q_loc^nu=0 or bounded", "OPEN_HARD", "868/907/1212"),
        ("LLC1511_6_GM_transfer", "worldtube measured-GM transfer", "EH mass/exterior charge equals Hilbert/worldtube source charge and measured orbital GM", "mu_EH=G_ref M_H[worldtube]=GM_orbital/c^2", "NOT_DERIVED", "956/957/1339"),
        ("LLC1511_7_Newton_PPN", "Newton and PPN completion", "weak-field gives Poisson/inverse-square plus GR PPN residual vector zero/bounded", "nabla^2 Phi=4 pi G rho; gamma=beta=1; alpha_i=xi=Gdot=0 or bounded", "NOT_READY", "868/907/1473"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "contract_layer": layer,
            "requirement": requirement,
            "mathematical_form": form,
            "current_status": status,
            "source_cluster": cluster,
            **flags(),
        }
        for contract_id, layer, requirement, form, status, cluster in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CLAIM1511_0_source_side", "source-side GR/Newton matter term", "conditional spine exists: one coframe + total Hilbert source + common kappa", "PRIVATE_CONDITIONAL_STRENGTH", "not parent-signed; no public claim"),
        ("CLAIM1511_1_EH_algebra", "EH weak-field coefficient algebra", "if EH premises pass, Poisson coefficient algebra is clean", "PRIVATE_CONDITIONAL_STRENGTH", "does not prove EH premises or measured GM"),
        ("CLAIM1511_2_R10", "R10 short-range branch", "real source anchors acquired, but scoring frozen", "DISCIPLINED_EMPIRICAL_GATE", "not local-GR proof"),
        ("CLAIM1511_3_local_GR", "local GR reduction", "not claimable until EH operator, extra silence, Bianchi, GM, and PPN close", "NOT_CLAIMABLE", "central derivation work remains"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "object": obj,
            "strongest_private_statement": statement,
            "status": status,
            "guardrail": guardrail,
            **flags(),
        }
        for claim_id, obj, statement, status, guardrail in rows
    ]


def blocker_rows() -> list[dict[str, Any]]:
    rows = [
        ("BL1511_0_EH_operator", "EH operator selection", "CENTRAL_BLOCKER", "without EH/LC/second-order metric-only selection, the left-hand field equation may not be GR", "derive parent metric-only second-order LC theorem or emit executable non-EH vector"),
        ("BL1511_1_extra_sector", "extra-sector silence", "ACTIVE_PRIMARY_OBSTRUCTION", "extra fields/projectors/memory/boundary terms can carry local stress, charge, or hair", "prove zero/gauge/topological/nohair or retain residual rows"),
        ("BL1511_2_Bianchi", "Bianchi/projector conservation safety", "OPEN_HARD", "dropping projector stress would fake an EH exterior and may break local conservation", "derive conserved-zero fate or retained PPN vector"),
        ("BL1511_3_GM_transfer", "measured GM/worldtube transfer", "NOT_DERIVED", "EH-shaped equation is not Newtonian mechanics without stable source normalization", "derive Noether/Hamiltonian/Gauss source transfer"),
        ("BL1511_4_PPN", "PPN residual vector", "NOT_READY", "Poisson leading order is not full local GR", "fill gamma/beta/preferred-frame/Gdot/clock/WEP residual vector after operator/source gates"),
        ("BL1511_5_R10", "R10 finite range", "FROZEN_LOWER_PRIORITY_NOW", "empirical short-range scoring lacks full curve/tau/alpha", "keep frozen while parent derivation proceeds"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocker": blocker,
            "priority": priority,
            "why_it_matters": why,
            "next_resolution": resolution,
            **flags(),
        }
        for blocker_id, blocker, priority, why, resolution in rows
    ]


def priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "PRIO1511_0",
            "selected_next_target": "EH operator selection / non-EH residual vector",
            "why_selected": "it is the highest shared blocker across 907, 956, 957, 958, 1212, and 1339; without it Newton and PPN coefficients are premature",
            "route": "try derivation first: parent metric-only second-order Levi-Civita local branch; if not, emit executable non-EH residual vector",
            "deferred": "R10 digitization, PPN numeric scoring, and source-GM transfer until operator branch is owned enough to mean something",
            **flags(),
        }
    ]


def local_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LGS1511_0",
            "object": "GR/Newton derivability route",
            "status": "REENTERED_WITH_CONTRACT",
            "effect": "future work can attack exact clauses rather than broad vibes",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LGS1511_1",
            "object": "local GR claim",
            "status": "NOT_CLAIMABLE",
            "effect": "EH operator, extra-sector silence, Bianchi, GM, and PPN gates remain open",
            **flags(),
        },
    ]


def score_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "score_id": "SCORE1511_0",
            "status": "NOT_SCORE_READY",
            "reason": "this is a derivation inventory/contract checkpoint, not an empirical score",
            "active_blockers": "; ".join(row["blocker"] for row in blockers),
            **flags(),
        }
    ]


def rejection_rows(blockers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": blocker["blocker_id"].replace("BL", "REJ"),
            "rejected_shortcut": f"claim local GR while {blocker['blocker']} remains open",
            "reason": blocker["why_it_matters"],
            **flags(),
        }
        for blocker in blockers
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1511_0_1512",
            "next_target": "1512-Y5-parent-EH-operator-selection-theorem-or-nonEH-residual-vector.md",
            "script": "scripts/Y5_parent_EH_operator_selection_theorem_or_nonEH_residual_vector.py",
            "objective": "try to derive the local 4D metric-only second-order Levi-Civita EH operator selection from the parent branch; if it cannot be signed, emit the executable non-EH residual vector instead of claiming GR",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    for path in [QUARANTINE, BRANCH_RESIDUALS]:
        path.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (ARTIFACT_INVENTORY, QUAR_INVENTORY),
        (CONTRACT, QUAR_CONTRACT),
        (PRIORITY_DECISION, QUAR_PRIORITY),
        (ARTIFACT_INVENTORY, BRANCH_INVENTORY),
        (CONTRACT, BRANCH_CONTRACT),
        (PRIORITY_DECISION, BRANCH_PRIORITY),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], inventory: list[dict[str, Any]], contract: list[dict[str, Any]], blockers: list[dict[str, Any]], priority: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    inventory_covers_core = len(inventory) >= 12 and any(row["inventory_id"] == "INV1511_5_958_EH_attempt" for row in inventory)
    contract_has_layers = len(contract) == 8 and any(row["contract_id"] == "LLC1511_3_EH_operator" and row["current_status"] == "CENTRAL_BLOCKER_NOT_DERIVED" for row in contract)
    blockers_prioritize_eh = blockers[0]["blocker_id"] == "BL1511_0_EH_operator" and blockers[0]["priority"] == "CENTRAL_BLOCKER"
    priority_selects_eh = priority[0]["selected_next_target"] == "EH operator selection / non-EH residual vector"
    local_claim_false = all(row["valid_for_claim"] is False and row["claim_allowed"] is False for row in contract + blockers + priority)
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_INVENTORY, QUAR_CONTRACT, QUAR_PRIORITY, BRANCH_INVENTORY, BRANCH_CONTRACT, BRANCH_PRIORITY])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1511_0_sources", source_paths_exist, "all cited GR/Newton source paths exist"),
        ("VAL1511_1_inventory_core", inventory_covers_core, "artifact inventory covers core EH/local-GR spine"),
        ("VAL1511_2_contract_layers", contract_has_layers, "minimal local-limit contract has 8 layers and marks EH operator as central blocker"),
        ("VAL1511_3_blocker_priority", blockers_prioritize_eh, "open blocker stack prioritizes EH operator selection first"),
        ("VAL1511_4_priority_decision", priority_selects_eh, "next derivation target is EH operator selection or non-EH residual vector"),
        ("VAL1511_5_no_claim", local_claim_false, "contract/blocker/priority rows are nonclaim"),
        ("VAL1511_6_csv_parse", csv_parse_ok, "all generated 1511 CSVs parse cleanly"),
        ("VAL1511_7_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
        ("VAL1511_8_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1511_9_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1511_10_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1511_11_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1511 inventoried the GR/Newton spine, extracted the minimal local-limit contract, and selected EH operator selection as the next derivation target"
            if overall
            else "1511 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    inventory: list[dict[str, Any]],
    contract: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    blockers: list[dict[str, Any]],
    priority: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1511 - Parent GR/Newton Reentry Spine Inventory and Strongest Local-Limit Contract",
                "",
                "## Verdict",
                "- The existing corpus already contains a usable GR/Newton spine: source-side matter descent is conditionally strong, but the left-hand EH/operator route is still not parent-derived.",
                "- The minimal local-limit contract is now explicit: local branch selector, one observed frame, minimal matter source, EH operator, extra-sector silence, Bianchi safety, GM transfer, and Newton/PPN completion.",
                "- The next best derivation target is the EH operator selection theorem; if it cannot be signed, the honest fallback is an executable non-EH residual vector.",
                "",
                "## Artifact Inventory",
                md_table(inventory, ["inventory_id", "artifact", "strength", "claim_status"]),
                "",
                "## Minimal Local-Limit Contract",
                md_table(contract, ["contract_id", "contract_layer", "current_status", "mathematical_form"]),
                "",
                "## Strongest Private Claims",
                md_table(claims, ["claim_id", "object", "status", "guardrail"]),
                "",
                "## Open Blocker Stack",
                md_table(blockers, ["blocker_id", "blocker", "priority", "next_resolution"]),
                "",
                "## Priority Decision",
                md_table(priority, ["decision_id", "selected_next_target", "route", "deferred"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    inventory = inventory_rows()
    contract = contract_rows()
    claims = claim_rows()
    blockers = blocker_rows()
    priority = priority_rows()
    local_status = local_status_rows()
    score = score_rows(blockers)
    rejections = rejection_rows(blockers)
    next_rows = next_target_rows()

    write_csv(ARTIFACT_INVENTORY, inventory)
    write_csv(CONTRACT, contract)
    write_csv(CLAIM_LEDGER, claims)
    write_csv(BLOCKER_STACK, blockers)
    write_csv(PRIORITY_DECISION, priority)
    write_csv(LOCAL_STATUS, local_status)
    write_csv(SCORE_READINESS, score)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        ARTIFACT_INVENTORY,
        CONTRACT,
        CLAIM_LEDGER,
        BLOCKER_STACK,
        PRIORITY_DECISION,
        LOCAL_STATUS,
        SCORE_READINESS,
        REJECTION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, inventory, contract, blockers, priority)
    write_csv(VALIDATION, validation)
    write_doc(inventory, contract, claims, blockers, priority, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
