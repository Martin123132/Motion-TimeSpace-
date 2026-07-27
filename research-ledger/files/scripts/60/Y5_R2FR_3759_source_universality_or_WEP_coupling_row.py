import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3759"
BRANCH = "MTS_R2FR_Y5_SOURCE_UNIVERSALITY_OR_WEP_COUPLING_ROW_3759"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3759-Y5-R2FR-source-universality-or-WEP-coupling-row.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3759_SOURCE_REGISTER.csv",
    "universality": RESIDUALS / "P8_Y5_R2FR_3759_SOURCE_UNIVERSALITY_THEOREM.csv",
    "wep_bound": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
    "runner_patch": RESIDUALS / "P8_Y5_R2FR_3759_COUPLING_RUNNER_PATCH.csv",
    "em_source_contract": RESIDUALS / "P8_Y5_R2FR_3759_EM_STRESS_SOURCE_CONTRACT.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3759_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3759_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3759_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3759_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3759_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3759_0_3758_doc": PCW / "3758-Y5-R2FR-kappa-superselection-signature-or-Gdot-numeric-bound.md",
        "SRC3759_1_3758_next": RESIDUALS / "P8_Y5_R2FR_3758_NEXT_TARGET.csv",
        "SRC3759_2_3758_runner": RESIDUALS / "P8_Y5_R2FR_3758_COUPLING_RUNNER_PATCH.csv",
        "SRC3759_3_3758_kappa_contract": RESIDUALS / "P8_Y5_R2FR_3758_KAPPA_SUPERSELECTION_ACTION_CONTRACT.csv",
        "SRC3759_4_3755_residual_vector": RESIDUALS / "P8_Y5_R2FR_3755_COUPLING_RESIDUAL_VECTOR.csv",
        "SRC3759_5_3755_kappa": RESIDUALS / "P8_Y5_R2FR_3755_KAPPA_THEOREM_ROWS.csv",
        "SRC3759_6_3754_flux_law": RESIDUALS / "P8_Y5_R2FR_3754_SOURCE_WARD_FLUX_LAW_ROWS.csv",
        "SRC3759_7_source_current_contract": RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv",
        "SRC3759_8_owner_identity": RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "SRC3759_9_gm_matrix": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "SRC3759_10_local_bounds": PCW / "source-intake" / "local_bounds" / "local_bound_claims.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3759 WEP/source-universality derivation input",
        }
        for source_id, path in source_paths().items()
    ]


def universality_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "SU3759_0_same_action",
            "All local matter species couple through one matter action S_matter[psi_A, g_eff, theta] with no species-labelled gravitational coupling kappa_A.",
            "This is the standard metric-coupling route to WEP; in MTS it must be a parent action signature.",
            "REQUIRED_ACTION_SIGNATURE",
            False,
        ),
        (
            "SU3759_1_same_hilbert_source",
            "The source current is the Hilbert/coframe current of the same observed matter action for every composition A.",
            "Imported from the 3754 same-frame source requirement; still requires parent adoption.",
            "EXACT_IF_SAME_ACTION",
            False,
        ),
        (
            "SU3759_2_source_blind_kappa",
            "If kappa_eff is in K_global and K_global has no species/source-label action, then partial_A ln kappa_eff = 0.",
            "This imports the 3755 source-blindness theorem.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            False,
        ),
        (
            "SU3759_3_passive_active_ratio",
            "For composition A, define Xi_A := Q_source,A/M_inertial,A. WEP source universality requires d_A ln Xi_A = 0.",
            "This is the active/passive source-charge ratio that must not depend on composition.",
            "DEFINITION_BRIDGE",
            True,
        ),
        (
            "SU3759_4_eta_zero",
            "If d_A ln kappa_eff=0, d_A ln Xi_A=0, and frame/exchange residuals are source-blind, then eta_source_AB=0.",
            "This gives the conditional WEP row.",
            "EXACT_CONDITIONAL_ZERO_THEOREM",
            False,
        ),
        (
            "SU3759_5_eta_residual",
            "eta_source_AB <= |Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange|.",
            "No-cancellation residual formula for the MICROSCOPE/WEP row.",
            "BOUND_DERIVED",
            True,
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "premise_or_note": premise_or_note,
            "status": status,
            "derived_inside_3759": derived,
            "parent_signed": False if not derived else "definition_or_bound",
            "claim_allowed": False,
        }
        for theorem_id, statement, premise_or_note, status, derived in entries
    ]


def em_source_contract_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "EMSC3759_0_same_stress",
            "Electromagnetic field energy, binding energy, and material stress must enter the same Hilbert/coframe source T_H used by the local gravitational coupling.",
            "Otherwise composition-dependent EM binding energy becomes an unowned WEP residual.",
            "REQUIRED_FOR_WEP_AND_MAXWELL_ROUTE",
        ),
        (
            "EMSC3759_1_no_side_channel_charge",
            "There must be no separate species-labelled EM-source coupling kappa_EM,A in the Newton/PPN source term.",
            "A side-channel EM coupling would directly populate eta_source_AB.",
            "REQUIRED_FOR_SOURCE_UNIVERSALITY",
        ),
        (
            "EMSC3759_2_maxwell_later_gate",
            "The later Maxwell/EM derivation must prove that EM stress is conserved/exchanged consistently with the same total stress tensor, not pasted on after gravity.",
            "This links the WEP row to the Maxwell/EM-stress programme.",
            "NEXT_GATE_PREP",
        ),
    ]
    return [
        {
            **base(timestamp),
            "contract_id": contract_id,
            "contract_clause": contract_clause,
            "why_it_matters": why_it_matters,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for contract_id, contract_clause, why_it_matters, status in entries
    ]


def parse_wep_bound() -> float:
    runner_rows = read_csv(source_paths()["SRC3759_2_3758_runner"])
    wep_row = next(row for row in runner_rows if row["residual_id"] == "KRV3755_1_species_source")
    bound_value = float(wep_row["bound_value"])
    if not math.isfinite(bound_value) or bound_value <= 0:
        raise ValueError("invalid WEP bound")
    return bound_value


def wep_bound_rows(timestamp: str) -> list[dict[str, object]]:
    bound_value = parse_wep_bound()
    return [
        {
            **base(timestamp),
            "evaluation_id": "WB3759_0_conditional_zero",
            "observable": "eta_source_AB",
            "units": "dimensionless",
            "prediction_formula": "eta_source_AB = 0",
            "prediction_value": 0.0,
            "bound_value": bound_value,
            "score_status": "CONDITIONAL_NUMERIC_PASS_IF_SOURCE_UNIVERSALITY_SIGNED",
            "required_parent_signatures": "SU3759_0_same_action;SU3759_2_source_blind_kappa;SU3759_4_eta_zero;EMSC3759_0_same_stress",
            "valid_prediction_row": False,
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "evaluation_id": "WB3759_1_residual_bound",
            "observable": "eta_source_AB",
            "units": "dimensionless",
            "prediction_formula": "|Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange|",
            "prediction_value": "MISSING_NUMERIC_COMPOSITION_COMPONENTS",
            "bound_value": bound_value,
            "score_status": "BOUND_FORMULA_READY_NUMERIC_COMPONENTS_MISSING",
            "required_parent_signatures": "none if every composition residual component is numerically bounded",
            "valid_prediction_row": False,
            "claim_allowed": False,
        },
        {
            **base(timestamp),
            "evaluation_id": "WB3759_2_max_allowed_residual",
            "observable": "allowed_absolute_composition_budget",
            "units": "dimensionless",
            "prediction_formula": "composition residual budget must be <= MICROSCOPE/WEP bound under no-cancellation policy",
            "prediction_value": bound_value,
            "bound_value": bound_value,
            "score_status": "NUMERIC_TARGET_FOR_FUTURE_COMPONENT_FILL",
            "required_parent_signatures": "component rows must sum to <= bound",
            "valid_prediction_row": True,
            "claim_allowed": False,
        },
    ]


def runner_patch_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_row in read_csv(source_paths()["SRC3759_2_3758_runner"]):
        patched = {
            **base(timestamp),
            "patched_runner_row_id": f"RUN3759_{source_row['residual_id']}",
            "source_runner_row": source_row["patched_runner_row_id"],
            "residual_id": source_row["residual_id"],
            "symbol": source_row["symbol"],
            "arena": source_row["arena"],
            "bound_value": source_row["bound_value"],
            "units": source_row["units"],
            "prediction_status_3758": source_row["prediction_status_3758"],
            "score_status_3758": source_row["score_status_3758"],
            "prediction_status_3759": source_row["prediction_status_3758"],
            "score_status_3759": source_row["score_status_3758"],
            "prediction_or_bound_formula_3759": source_row["prediction_or_bound_formula_3758"],
            "conditional_score_ready": source_row["conditional_score_ready"],
            "valid_prediction_row": False,
            "claim_allowed": False,
            "notes": "unchanged from 3758",
        }
        if source_row["residual_id"] == "KRV3755_1_species_source":
            patched.update(
                {
                    "prediction_status_3759": "ZERO_OR_COMPOSITION_RESIDUAL_BOUNDED_SOURCE_UNIVERSALITY_LAW",
                    "score_status_3759": "CONDITIONAL_ZERO_OR_WEP_RESIDUAL_BOUND_READY",
                    "prediction_or_bound_formula_3759": "|Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange| <= 2.8e-15; zero if source universality is parent-signed",
                    "conditional_score_ready": True,
                    "notes": "3759 derives WEP/source-universality zero condition and residual budget; numeric composition components remain missing",
                }
            )
        rows.append(patched)
    return rows


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    gates = [
        ("CG3759_0_sources", "all 3759 source paths exist", all_sources, "path hygiene"),
        ("CG3759_1_universality_zero", "source-universality WEP zero theorem emitted", True, "conditional theorem exists"),
        ("CG3759_2_wep_bound", "WEP residual bound formula derived", True, "no-cancellation absolute composition budget"),
        ("CG3759_3_same_action_parent_signed", "same matter action/source current parent-signed", False, "contract emitted but not adopted by parent action"),
        ("CG3759_4_em_same_stress_parent_signed", "EM/binding stress included in same Hilbert source", False, "Maxwell/EM stress gate remains open"),
        ("CG3759_5_numeric_composition_components", "all WEP residual components numeric", False, "composition components missing"),
        ("CG3759_6_WEP_claim", "WEP/source universality claim allowed", False, "conditional zero or bound not fully sourced"),
        ("CG3759_7_local_gr_claim", "local GR/PPN claim allowed", False, "PPN and EM-stress gates remain open"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    entries = [
        (
            "DEC3759_0",
            "The WEP row is now in the same state as Gdot: conditionally zero if the parent action signs universality, otherwise bounded by an explicit residual sum.",
            "do not claim WEP yet; use the row as a parent-action design gate",
        ),
        (
            "DEC3759_1",
            "EM/binding stress is not optional for WEP: it must be part of the same source tensor or composition dependence reappears.",
            "make Maxwell/EM stress the next gate rather than postponing it indefinitely",
        ),
        (
            "DEC3759_2",
            "This improves the MTS-to-GR route because local GR needs universal metric/coframe coupling before PPN gamma/beta are meaningful.",
            "next derive same-source Maxwell stress or explicitly track its residual",
        ),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in entries
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3759_0",
            "target_doc": "3760-Y5-R2FR-Maxwell-EM-stress-same-source-current-or-residual.md",
            "target_script": "scripts/Y5_R2FR_3760_Maxwell_EM_stress_same_source_current_or_residual.py",
            "objective": "derive that EM field stress and binding energy sit inside the same Hilbert/coframe source current used by local gravity, or emit an EM composition/source residual row that feeds WEP and PPN",
            "reason": "3759 shows WEP depends on EM/binding stress being source-universal; this also begins the Maxwell/EM-stress connection requested by the programme",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "WEP_SOURCE_UNIVERSALITY_ZERO_OR_RESIDUAL_BUDGET_DERIVED",
            "summary": "3759 derives eta_source_AB=0 under same-action/source-blind-kappa/same-EM-stress signatures, and otherwise gives a composition residual budget that must be <= 2.8e-15.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3759 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3759 csvs parse", all(read_csv(path) for path in generated_csvs)),
        (
            "wep_zero_theorem",
            "WEP conditional zero theorem emitted",
            any(row["theorem_id"] == "SU3759_4_eta_zero" and row["status"] == "EXACT_CONDITIONAL_ZERO_THEOREM" for row in grouped["universality"]),
        ),
        (
            "wep_residual_bound",
            "WEP residual bound emitted",
            any(row["theorem_id"] == "SU3759_5_eta_residual" and row["status"] == "BOUND_DERIVED" for row in grouped["universality"]),
        ),
        (
            "wep_bound_value",
            "WEP budget uses 2.8e-15",
            any(str(row["bound_value"]) == "2.8e-15" for row in grouped["wep_bound"]),
        ),
        (
            "em_source_contract",
            "EM same-source contract emitted",
            any(row["contract_id"] == "EMSC3759_0_same_stress" for row in grouped["em_source_contract"]),
        ),
        (
            "runner_patch_nonclaim",
            "patched runner remains nonclaim",
            all(str(row["claim_allowed"]) == "False" or row["claim_allowed"] is False for row in grouped["runner_patch"]),
        ),
        (
            "wep_claim_blocked",
            "WEP claim remains false",
            any(row["gate_id"] == "CG3759_6_WEP_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "local_gr_not_claimed",
            "local GR remains unclaimed",
            any(row["gate_id"] == "CG3759_7_local_gr_claim" and row["passed"] is False for row in grouped["claim_gates"]),
        ),
        (
            "next_target",
            "3760 target emitted",
            grouped["next_target"][0]["target_doc"] == "3760-Y5-R2FR-Maxwell-EM-stress-same-source-current-or-residual.md",
        ),
        (
            "no_formalization_leak",
            "no 3759 files written to formalization-workbench",
            not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3759*")),
        ),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3759 — Source Universality Or WEP Coupling Row",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Derivation",
        "",
        "The WEP/source row is the composition version of the coupling problem. If every local matter composition couples through the same matter action and the same Hilbert/coframe source current, then there is no species-labelled gravitational charge. In that case `eta_source_AB=0`.",
        "",
        "If the parent action does not sign that universality, the live residual is",
        "",
        "`eta_source_AB <= |Delta_AB ln kappa_eff| + |Delta_AB ln Xi| + |Delta_AB ln Z_frame| + |Delta_AB exchange|`.",
        "",
        "The no-cancellation target is `<= 2.8e-15`. EM and binding energy must sit in the same source tensor, otherwise composition dependence leaks straight into this row.",
        "",
        "## Source Universality Clauses",
    ]
    for row in grouped["universality"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']}")
    lines.extend(["", "## EM Stress Source Contract"])
    for row in grouped["em_source_contract"]:
        lines.append(f"- `{row['contract_id']}` `{row['status']}`: {row['contract_clause']}")
    lines.extend(["", "## WEP Bound Evaluation"])
    for row in grouped["wep_bound"]:
        lines.append(
            f"- `{row['evaluation_id']}` `{row['score_status']}`: `{row['prediction_formula']}` versus `{row['bound_value']} {row['units']}` claim=`{row['claim_allowed']}`"
        )
    lines.extend(["", "## Runner Patch"])
    for row in grouped["runner_patch"]:
        lines.append(f"- `{row['patched_runner_row_id']}` `{row['score_status_3759']}`: {row['prediction_or_bound_formula_3759']}")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "universality": universality_rows(timestamp),
        "wep_bound": wep_bound_rows(timestamp),
        "runner_patch": runner_patch_rows(timestamp),
        "em_source_contract": em_source_contract_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["universality"], grouped["universality"])
    write_csv(OUTPUTS["wep_bound"], grouped["wep_bound"])
    write_csv(OUTPUTS["runner_patch"], grouped["runner_patch"])
    write_csv(OUTPUTS["em_source_contract"], grouped["em_source_contract"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3759 validation failed: {failures}")
    print("wrote 3759 checkpoint: WEP source-universality zero or residual budget derived")


if __name__ == "__main__":
    main()
