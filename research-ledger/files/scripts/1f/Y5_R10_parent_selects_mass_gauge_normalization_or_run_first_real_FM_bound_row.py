from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
DOC_NAME = "923-Y5-R10-parent-selects-mass-gauge-normalization-or-run-first-real-FM-bound-row.md"
STATUS = "Y5_R10_923_Hamiltonian_mass_charge_normalization_selected_as_best_candidate_not_parent_signed_first_FM_WEP_bound_row_blocked_nonclaim"
CLAIM_CEILING = "normalization_candidate_and_first_FM_bound_row_only_no_WEP_R10_PPN_clock_orbital_or_local_GR_claim"
NEXT_TARGET = "924-Y5-R10-Hamiltonian-mass-charge-normalization-contract-or-FM-bound-row-expansion.md"
GENERATED = datetime.now(timezone.utc).isoformat()
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        cells = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def b(value: bool) -> str:
    return "true" if value else "false"


def source_specs() -> list[dict[str, str]]:
    return [
        {
            "source_id": "922_doc",
            "path": "922-Y5-R10-KBFH-parent-units-and-normalization-or-local-bound-smoke-runner.md",
            "role": "hands off unit branches and fail-closed smoke runner",
            "needle": "The strict smoke runner therefore",
        },
        {
            "source_id": "922_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_922_VALIDATION.csv",
            "role": "proves 922 validated and remained nonclaim",
            "needle": "V922_11_validation_rows_ready",
        },
        {
            "source_id": "922_unit_audit",
            "path": "source-intake/mts_residuals/P8_Y5_R10_922_KBFH_UNIT_BRANCH_AUDIT.csv",
            "role": "unit branch audit including measured-GM calibration blocker",
            "needle": "KBU922_4_measured_GM_calibration",
        },
        {
            "source_id": "539_Hamiltonian_PiM",
            "path": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
            "role": "Hamiltonian mass charge repair branch",
            "needle": "Define Pi_M^H from the parent Hamiltonian surface charge itself.",
        },
        {
            "source_id": "457_Hamiltonian_charge",
            "path": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
            "role": "conditional Hamiltonian boundary charge theorem and calibration warning",
            "needle": "conditional_Hamiltonian_boundary_charge_theorem",
        },
        {
            "source_id": "501_Hilbert_worldtube",
            "path": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
            "role": "best route defines Q_M from same parent Hilbert compact-source worldtube",
            "needle": "The best route is to define Q_M from the same parent Hilbert compact-source worldtube before readout.",
        },
        {
            "source_id": "359_guardrail",
            "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
            "role": "source-locked local bound pressure ranking; WEP is hardest guardrail",
            "needle": "eta_WEP",
        },
        {
            "source_id": "427_bounds_discipline",
            "path": "427-source-normalization-bounds-csv-template-fill.md",
            "role": "local bounds are residual-channel constraints, not MTS predictions",
            "needle": "these are bounds on possible residual channels",
        },
        {
            "source_id": "local_bound_claims",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "real local-bound source row used for first FM row",
            "needle": "R1_WEP_source_charge",
        },
        {
            "source_id": "921_arena_map",
            "path": "source-intake/mts_residuals/P8_Y5_R10_921_LOCAL_BOUND_ARENA_MAP.csv",
            "role": "arena map showing R1 WEP source-charge row and R10 symbolic status",
            "needle": "BAM921_0_WEP",
        },
    ]


def build_sources() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in source_specs():
        path = ROOT / spec["path"]
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": b(exists),
                "needle_found": b(needle_found),
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "current_result": "Hamiltonian mass-charge normalization is the only clean non-circular candidate, but source-measure/Gauss calibration is not parent-signed",
            "what_changed": "first real local-bound FM row is created against the sourced WEP source-charge bound, and it blocks cleanly",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def normalization_attempt_rows() -> list[dict[str, object]]:
    return [
        {
            "attempt_id": "NORM923_0_topological_connection",
            "candidate": "A_M as dimensionless topological connection",
            "normalization_rule": "holonomy exp(i integral A_M) dimensionless; K_BF_H absorbs source-charge units",
            "strength": "fits BF/topological no-local-DOF story",
            "failure_or_open_clause": "can be the wrong conserved object unless equal to Hamiltonian/Hilbert mass charge",
            "status": "demoted_as_independent_normalization",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "attempt_id": "NORM923_1_ordinary_gauge_potential",
            "candidate": "A_M as inverse-length gauge potential",
            "normalization_rule": "K_BF_H resembles ordinary force coupling after weak-field reduction",
            "strength": "easy to compare to fifth-force language",
            "failure_or_open_clause": "imports kinetic/range conventions not derived by the nonpropagating BF branch",
            "status": "not_lead_branch",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "attempt_id": "NORM923_2_Hamiltonian_mass_charge",
            "candidate": "A_M couples to the parent Hamiltonian mass charge current",
            "normalization_rule": "choose K_BF_H so the charge sourced by A_M is Q_tau/M_eff with fixed G_ref calibration",
            "strength": "least circular branch because Pi_M is defined by the parent charge rather than post-readout topology",
            "failure_or_open_clause": "requires integrable Q_tau, same-source worldtube glue, Gauss-Poisson calibration, and PPN readout",
            "status": "best_candidate_not_parent_signed",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "attempt_id": "NORM923_3_measured_GM_after_fit",
            "candidate": "choose K_BF_H by absorbing mismatch into measured GM",
            "normalization_rule": "fit K_BF_H so local bounds look small",
            "strength": "none for a derivation",
            "failure_or_open_clause": "forbidden post-hoc normalization/free G-M absorption",
            "status": "rejected_no_cheat",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def branch_decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "NBD923_0_select_target",
            "selected_target": "Hamiltonian_mass_charge_normalization",
            "selection_type": "best_candidate_for_next_derivation_not_a_claim",
            "reason": "it ties the mass-gauge coupling to the same parent charge that would later support Newton/Gauss/PPN",
            "remaining_required_proof": "Q_tau integrability; source worldtube equality; k_M/K_BF_H relation; Gauss-Poisson calibration; no boundary flux",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "decision_id": "NBD923_1_first_bound_row",
            "selected_target": "R1_WEP_source_charge",
            "selection_type": "first_real_nonclaim_bound_row",
            "reason": "WEP source-charge bound is sourced, numeric, dimensionless, and directly stresses universal coupling",
            "remaining_required_proof": "K_BF_H normalization; species coefficient C_eta_AB; numeric dPiMJ_leak; source path for MTS residual",
            "parent_selected": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def local_bound_row(row_id: str) -> dict[str, str]:
    rows = read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    for row in rows:
        if row["row_id"] == row_id:
            return row
    raise KeyError(row_id)


def first_bound_rows() -> list[dict[str, object]]:
    bound = local_bound_row("R1_WEP_source_charge")
    return [
        {
            "fm_bound_id": "FM923_0_WEP_source_charge_nonclaim",
            "source_dataset_id": bound["dataset_id"],
            "local_bound_row": bound["row_id"],
            "test_arena": bound["test_arena"],
            "observable": bound["observable"],
            "upper_bound": bound["upper_bound"],
            "bound_units": bound["units"],
            "FM_prediction_symbol": "eta_FM_AB",
            "FM_prediction_formula": "eta_FM_AB = |C_eta_AB K_BF_H A_M_norm dPiMJ_leak|",
            "FM_prediction_value": "MISSING_KBFH_NORMALIZATION",
            "MTS_source_path": "MISSING_PARENT_NORMALIZATION_SOURCE",
            "score_status": "blocked_missing_MTS_inputs",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def strict_eval_rows(bound_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in bound_rows:
        blocked = any("MISSING" in str(value) for value in row.values()) or row["valid_for_claim"] != "true"
        rows.append(
            {
                "eval_id": row["fm_bound_id"].replace("FM", "EVAL"),
                "local_bound_row": row["local_bound_row"],
                "observable": row["observable"],
                "FM_prediction_value": row["FM_prediction_value"],
                "upper_bound": row["upper_bound"],
                "runner_status": "blocked" if blocked else "candidate",
                "block_reason": "missing_KBFH_or_MTS_residual_source" if blocked else "all_inputs_present",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": GENERATED,
            }
        )
    return rows


def blocker_rows() -> list[dict[str, object]]:
    return [
        {
            "blocker_id": "BLK923_0_Qtau_integrability",
            "missing_input": "integrable parent Hamiltonian mass charge Q_tau with fixed reference",
            "why_needed": "without it Pi_M^H is not a parent charge map",
            "next_action": "write Hamiltonian mass-charge normalization contract",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK923_1_worldtube_glue",
            "missing_input": "same Hilbert compact-source worldtube equals the Hamiltonian charge source",
            "why_needed": "prevents topological charge from being the wrong conserved object",
            "next_action": "prove or bound source-measure equality",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK923_2_KBFH_kM_relation",
            "missing_input": "parent relation between BF level k_M and source coupling K_BF_H",
            "why_needed": "fixes the units and normalization of the matter-current coupling",
            "next_action": "derive from A_M/B_M variation and charge normalization",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "blocker_id": "BLK923_3_first_bound_numeric",
            "missing_input": "numeric eta_FM_AB built from C_eta_AB, K_BF_H, A_M_norm, and dPiMJ_leak",
            "why_needed": "first real WEP row cannot score without an MTS residual value",
            "next_action": "fill source-backed nonclaim numeric row only after parent normalization exists",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def gate_rows() -> list[dict[str, object]]:
    return [
        {
            "gate_id": "CGATE923_0_parent_normalization",
            "claim": "parent action selects K_BF_H/A_M/J_Pi normalization",
            "blocker": "Hamiltonian branch selected only as next derivation target, not proved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE923_1_first_bound_score",
            "claim": "first FM WEP row scores against MICROSCOPE source-charge bound",
            "blocker": "FM prediction value and source path are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
        {
            "gate_id": "CGATE923_2_local_GR",
            "claim": "normalization route supports local-GR/Newton/PPN pass",
            "blocker": "Gauss-Poisson and PPN readout calibration are not parent-derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        },
    ]


def next_rows() -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "write the Hamiltonian mass-charge normalization contract tying Q_tau, k_M, K_BF_H, Pi_M^H J_H, and measured GM; if it fails, expand nonclaim FM bound rows",
            "include": "Q_tau integrability, same-source worldtube, k_M/K_BF_H relation, Gauss-Poisson normalization, WEP row fill requirements",
            "exclude": "post-fit normalization, free G/M absorption, claiming a local-bound pass, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": GENERATED,
        }
    ]


def formalization_changed_count() -> int:
    formalization = ROOT.parent / "formalization-workbench"
    if not formalization.exists():
        return 0
    return sum(
        1
        for path in formalization.rglob("*")
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def all_false(rows: list[dict[str, object]], fields: tuple[str, ...]) -> bool:
    return all(str(row.get(field, "")).strip().lower() != "true" for row in rows for field in fields)


def validation_rows(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    decisions: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    eval_rows: list[dict[str, object]],
    blockers: list[dict[str, object]],
    gates: list[dict[str, object]],
) -> list[dict[str, object]]:
    source_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior = OUT / "P8_Y5_BRR545_922_VALIDATION.csv"
    prior_ok = prior.exists() and "V922_11_validation_rows_ready" in read_text(prior)
    bound = bound_rows[0]
    sourced_bound_ok = bound["upper_bound"] == "2.8e-15" and bound["bound_units"] == "dimensionless"
    eval_blocked = all(row["runner_status"] == "blocked" for row in eval_rows)
    false_fields = ("parent_selected", "claim_allowed", "valid_for_claim")
    generated = attempts + decisions + bound_rows + eval_rows + blockers + gates
    changed = formalization_changed_count()
    return [
        {
            "check_id": "V923_0_sources_exist_and_needles",
            "result": "pass" if source_ok else "fail",
            "detail": "all source paths exist and needles are present" if source_ok else "missing source or needle",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_1_prior_922_clean",
            "result": "pass" if prior_ok else "fail",
            "detail": "P8_Y5_BRR545_922_VALIDATION.csv clean" if prior_ok else "922 validation missing or incomplete",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_2_normalization_not_parent_selected",
            "result": "pass" if all_false(attempts, false_fields) else "fail",
            "detail": "Hamiltonian branch is best candidate but no normalization branch is parent-selected",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_3_first_bound_row_source_backed",
            "result": "pass" if sourced_bound_ok else "fail",
            "detail": "first FM row uses sourced R1 WEP upper_bound=2.8e-15 dimensionless",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_4_first_bound_row_blocks",
            "result": "pass" if eval_blocked else "fail",
            "detail": "first FM row blocks because MTS coupling normalization/residual source is missing",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_5_blockers_explicit",
            "result": "pass" if all_false(blockers, ("valid_for_claim",)) and len(blockers) >= 4 else "fail",
            "detail": "Q_tau, worldtube, kM/KBFH, and numeric WEP blockers are explicit",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_6_claim_gates_false",
            "result": "pass" if all_false(gates, false_fields) else "fail",
            "detail": "normalization, first-bound score, and local-GR gates remain false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_7_all_generated_rows_nonclaim",
            "result": "pass" if all_false(generated, false_fields) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_8_formalization_workbench_untouched",
            "result": "pass" if changed == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={changed}",
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_9_next_target_selected",
            "result": "pass" if NEXT_TARGET.startswith("924-") else "fail",
            "detail": NEXT_TARGET,
            "generated_utc": GENERATED,
        },
        {
            "check_id": "V923_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
            "generated_utc": GENERATED,
        },
    ]


def write_doc(
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    attempts: list[dict[str, object]],
    decisions: list[dict[str, object]],
    bound_rows: list[dict[str, object]],
    eval_rows: list[dict[str, object]],
    blockers: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 923 - Y5/R10 Parent Selects Mass-Gauge Normalization Or Run First Real FM Bound Row

Private normalization/local-bound checkpoint. This is not a public WEP, R10, clock, PPN, orbital, local-GR, Newtonian, or unified-field claim.

Status: `{STATUS}`

Claim ceiling: `{CLAIM_CEILING}`

Current result: **the Hamiltonian mass-charge normalization is the best non-circular candidate, but it is not yet parent-signed.**

The no-cheat selection is:

```text
Pi_M := Pi_M^H from the parent Hamiltonian mass charge Q_tau,
K_BF_H fixed by the same Q_tau -> M_eff -> G_ref Gauss/Poisson normalization.
```

That would be the right road because it prevents the BF/topological current from being the wrong conserved object. But the road is not paved yet: `Q_tau` integrability, same-source worldtube glue, `k_M/K_BF_H`, and Gauss-Poisson calibration remain open.

So the checkpoint also writes the first real-shaped FM bound row against a sourced local constraint:

```text
R1_WEP_source_charge: eta_WEP_source_charge <= 2.8e-15.
```

It blocks, correctly, because the MTS-side prediction is still `MISSING_KBFH_NORMALIZATION`.

## Non-Claim Summary

{md_table(summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])}

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])}

## Parent Normalization Selection Attempt

{md_table(attempts, ["attempt_id", "candidate", "normalization_rule", "strength", "failure_or_open_clause", "status", "parent_selected", "valid_for_claim", "generated_utc"])}

## Branch Decision

{md_table(decisions, ["decision_id", "selected_target", "selection_type", "reason", "remaining_required_proof", "parent_selected", "valid_for_claim", "generated_utc"])}

## First FM Bound Row Nonclaim

{md_table(bound_rows, ["fm_bound_id", "source_dataset_id", "local_bound_row", "test_arena", "observable", "upper_bound", "bound_units", "FM_prediction_symbol", "FM_prediction_formula", "FM_prediction_value", "MTS_source_path", "score_status", "valid_for_claim", "generated_utc"])}

## Strict Row Evaluation

{md_table(eval_rows, ["eval_id", "local_bound_row", "observable", "FM_prediction_value", "upper_bound", "runner_status", "block_reason", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])}

## Claim Gate

{md_table(gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])}

## Next Target

{md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])}

## Validation

{md_table(validation, ["check_id", "result", "detail", "generated_utc"])}
"""
    (ROOT / DOC_NAME).write_text(body, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    src = build_sources()
    summary = summary_rows()
    attempts = normalization_attempt_rows()
    decisions = branch_decision_rows()
    bound_rows = first_bound_rows()
    eval_rows = strict_eval_rows(bound_rows)
    blockers = blocker_rows()
    gates = gate_rows()
    next_target = next_rows()
    validation = validation_rows(src, attempts, decisions, bound_rows, eval_rows, blockers, gates)

    write_csv(OUT / "P8_Y5_R10_923_SOURCE_REGISTER.csv", src, ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_923_NONCLAIM_SUMMARY.csv", summary, ["status", "claim_ceiling", "current_result", "what_changed", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_923_PARENT_NORMALIZATION_SELECTION_ATTEMPT.csv", attempts, ["attempt_id", "candidate", "normalization_rule", "strength", "failure_or_open_clause", "status", "parent_selected", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_923_NORMALIZATION_BRANCH_DECISION.csv", decisions, ["decision_id", "selected_target", "selection_type", "reason", "remaining_required_proof", "parent_selected", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_923_FIRST_FM_BOUND_ROW_NONCLAIM.csv", bound_rows, ["fm_bound_id", "source_dataset_id", "local_bound_row", "test_arena", "observable", "upper_bound", "bound_units", "FM_prediction_symbol", "FM_prediction_formula", "FM_prediction_value", "MTS_source_path", "score_status", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_923_STRICT_ROW_EVALUATION.csv", eval_rows, ["eval_id", "local_bound_row", "observable", "FM_prediction_value", "upper_bound", "runner_status", "block_reason", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_923_BLOCKER_LEDGER.csv", blockers, ["blocker_id", "missing_input", "why_needed", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_923_CLAIM_GATE.csv", gates, ["gate_id", "claim", "blocker", "claim_allowed", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_R10_923_NEXT_TARGET.csv", next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"])
    write_csv(OUT / "P8_Y5_BRR545_923_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(src, summary, attempts, decisions, bound_rows, eval_rows, blockers, gates, next_target, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        raise SystemExit(f"validation failed: {failed}")
    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
