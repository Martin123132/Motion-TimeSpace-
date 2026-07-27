from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3756"
BRANCH = "MTS_R2FR_Y5_NO_FLUX_PROJECTED_EXCHANGE_OR_COUPLING_RUNNER_3756"
PCW = Path(__file__).resolve().parents[1]
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3756-Y5-R2FR-no-flux-projected-exchange-or-coupling-runner.md"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(ts: str) -> dict[str, object]:
    return {
        "timestamp_utc": ts,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": False,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3756_0_3755_next": RESIDUALS / "P8_Y5_R2FR_3755_NEXT_TARGET.csv",
        "SRC3756_1_3755_residual_vector": RESIDUALS / "P8_Y5_R2FR_3755_COUPLING_RESIDUAL_VECTOR.csv",
        "SRC3756_2_3755_theorems": RESIDUALS / "P8_Y5_R2FR_3755_KAPPA_THEOREM_ROWS.csv",
        "SRC3756_3_3755_gates": RESIDUALS / "P8_Y5_R2FR_3755_CLAIM_GATES.csv",
        "SRC3756_4_3754_ward_flux": RESIDUALS / "P8_Y5_R2FR_3754_SOURCE_WARD_FLUX_LAW_ROWS.csv",
        "SRC3756_5_ward_owner": RESIDUALS / "P8_Ward_source_owner_identity_CONTRACT.csv",
        "SRC3756_6_source_ward": RESIDUALS / "P8_source_current_Ward_universality_CONTRACT.csv",
        "SRC3756_7_flux_contract": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "SRC3756_8_flux_residual_map": RESIDUALS / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "SRC3756_9_constant_gm_bounds": RESIDUALS / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv",
        "SRC3756_10_delta_kappa": RESIDUALS / "P8_delta_kappa_source_exchange_residual.csv",
    }


def source_register(ts: str) -> list[dict[str, object]]:
    purpose = {
        "SRC3756_0_3755_next": "imports exact 3756 target",
        "SRC3756_1_3755_residual_vector": "imports residual vector to dry-run",
        "SRC3756_2_3755_theorems": "imports Bianchi/exchange theorem context",
        "SRC3756_3_3755_gates": "imports open derivative/exchange gates",
        "SRC3756_4_3754_ward_flux": "imports Phi_side and Pi_M q_exchange balance law",
        "SRC3756_5_ward_owner": "imports owned-divergence/no-flux contract",
        "SRC3756_6_source_ward": "imports Hilbert/source Ward exchange clauses",
        "SRC3756_7_flux_contract": "imports mass-flux closure contract FC0-FC8",
        "SRC3756_8_flux_residual_map": "imports flux residual activation map",
        "SRC3756_9_constant_gm_bounds": "imports local coupling bound matrix",
        "SRC3756_10_delta_kappa": "imports delta_kappa_source residual definition",
    }
    return [
        {
            **base(ts),
            "source_id": source_id,
            "source_path": str(path),
            "purpose": purpose[source_id],
            "exists": path.exists(),
            "claim_allowed": False,
        }
        for source_id, path in source_paths().items()
    ]


def is_number(value: str) -> bool:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(parsed)


def no_flux_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "NF3756_0_balance_start",
            "Delta ell_M(J_H) = -Phi_side + int_C Pi_M q_exchange",
            "imported exact Stokes balance from 3754",
            "DERIVED_BALANCE",
            "source charge conservation reduces to two terms",
        ),
        (
            "NF3756_1_side_flux_definition",
            "Phi_side := int_side J_M through the worldtube/collar side boundary",
            "side boundary must be a fixed linking homology tube, not a moving fitted mask",
            "DEFINITION_READY",
            "if the side moves or carries flux, M_eff drift is physical",
        ),
        (
            "NF3756_2_topological_no_side_flux",
            "Phi_side=0 if J_M is a closed topological current and the side boundary is homologous with no source crossing",
            "requires parent-fixed worldtube/homology and no matter crossing side wall",
            "EXACT_CONDITIONAL_THEOREM",
            "not signed because worldtube/no-crossing theorem is not parent-derived",
        ),
        (
            "NF3756_3_owner_divergence_no_flux",
            "int_boundary Pi_M nabla_mu K_owner^{mu0}=int_boundary Pi_M K_owner^{i0} n_i dS",
            "zero only if K_owner has no projected normal flux or is a pure tangential/improvement class",
            "EXACT_CONDITIONAL_BOUNDARY_TEST",
            "current corpus marks this fail_open",
        ),
        (
            "NF3756_4_flux_bound",
            "|d ln M_eff/dt| <= (|Phi_side|+int|Pi_M q_exchange|)/(|ell_M(J_H)| Delta t)",
            "fallback when zero proof is unsigned",
            "BOUND_INTERFACE_READY",
            "feeds Gdot/radial/orbital residual rows",
        ),
    ]
    return [
        {
            **base(ts),
            "no_flux_id": row_id,
            "statement_or_formula": formula,
            "condition_or_derivation": condition,
            "status": status,
            "impact": impact,
            "claim_allowed": False,
        }
        for row_id, formula, condition, status, impact in rows
    ]


def exchange_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "EX3756_0_exchange_decomposition",
            "q_exchange = q_Hilbert_nonconservation + q_boundary + q_domain + q_memory + q_range + q_connection + q_kappa + q_retained",
            "project each term through Pi_M",
            "DECOMPOSITION_INTERFACE",
            "prevents treating all exchange as zero by naming channels",
        ),
        (
            "EX3756_1_projected_exchange_condition",
            "Pi_M q_exchange=0 iff every Pi_M q_i=0 or the nonzero terms are mapped and bounded in the residual vector",
            "no cancellation credit unless parent identity supplies it",
            "EXACT_CONDITIONAL_GATE",
            "Newton source calibration needs this, not just total Ward conservation",
        ),
        (
            "EX3756_2_kappa_exchange",
            "Pi_M q_kappa = Pi_M[kappa_eff^-1 T_obs^{mu nu} nabla_mu kappa_eff]",
            "zero if K_global superselection or Bianchi arbitrary-source premises are signed",
            "LIVE_FROM_3755",
            "otherwise activates delta_kappa_source",
        ),
        (
            "EX3756_3_boundary_domain_exchange",
            "Pi_M(q_boundary+q_domain)=0",
            "requires no-flux/no-domain-motion/no preferred-location theorem",
            "UNSIGNED",
            "otherwise activates mu_extra/radial/source residuals",
        ),
        (
            "EX3756_4_memory_range_exchange",
            "Pi_M(q_memory+q_range)=0",
            "requires no memory mass-channel leakage and no finite-range source branch",
            "UNSIGNED",
            "otherwise activates R10 alpha(lambda) and source-normalization rows",
        ),
        (
            "EX3756_5_verdict",
            "Pi_M q_exchange=0 is not proved in the current corpus",
            "dry-run residual runner is required",
            "NOT_CLAIMED",
            "local Newton/local GR remain blocked",
        ),
    ]
    return [
        {
            **base(ts),
            "exchange_id": row_id,
            "statement_or_formula": formula,
            "condition_or_derivation": condition,
            "status": status,
            "impact": impact,
            "claim_allowed": False,
        }
        for row_id, formula, condition, status, impact in rows
    ]


def runner_spec_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        ("RS3756_0_schema", "residual_id,symbol,arena,bound_value,units,prediction_status,prediction_value,score_status", "minimum runner columns"),
        ("RS3756_1_numeric_rule", "numeric bound rows score only when prediction_value is finite numeric", "abs(prediction_value)<=bound_value"),
        ("RS3756_2_curve_rule", "alpha(lambda) rows require a curve/table with lambda and alpha_predicted columns", "not scoreable from scalar placeholder"),
        ("RS3756_3_symbolic_rule", "zero_or_mapped_bound rows require a theorem-zero source or explicit mapped residual", "not scoreable from prose"),
        ("RS3756_4_claim_rule", "valid_for_claim remains false unless source path exists, units are recognized, prediction is numeric/table-backed, and bound comparison passes", "anti-smuggling rule"),
        ("RS3756_5_no_cancellation", "sum/total rows use absolute components, not tuned cancellation", "no-cancellation policy"),
    ]
    return [
        {
            **base(ts),
            "runner_spec_id": spec_id,
            "rule": rule,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for spec_id, rule, meaning in rows
    ]


def resolve_source_path(value: str) -> str:
    if not value:
        return ""
    candidate = Path(value)
    if candidate.is_absolute():
        return str(candidate)
    return str((PCW / value).resolve())


def runner_rows(ts: str) -> list[dict[str, object]]:
    rows = []
    for row in read_csv(source_paths()["SRC3756_1_3755_residual_vector"]):
        bound_value = row.get("bound_value", "")
        numeric_bound = is_number(bound_value)
        prediction_status = row.get("prediction_status", "")
        prediction_value = ""
        if bound_value == "alpha(lambda)":
            score_status = "BLOCKED_ALPHA_LAMBDA_CURVE_REQUIRED"
        elif "SUPERSELECTION_ZERO" in prediction_status or "THEOREM" in prediction_status:
            score_status = "BLOCKED_THEOREM_OR_NUMERIC_PREDICTION_REQUIRED"
        elif bound_value.startswith("zero_or") or bound_value.startswith("same-frame"):
            score_status = "BLOCKED_ZERO_OR_MAPPED_BOUND_REQUIRED"
        else:
            score_status = "BLOCKED_PREDICTION_VALUE_MISSING"
        bound_source = resolve_source_path(row.get("bound_source_path", ""))
        rows.append(
            {
                **base(ts),
                "runner_row_id": f"RUN3756_{row['residual_id']}",
                "residual_id": row["residual_id"],
                "symbol": row["symbol"],
                "arena": row["arena"],
                "bound_value": bound_value,
                "units": row.get("units", ""),
                "numeric_bound": numeric_bound,
                "bound_source_path_resolved": bound_source,
                "bound_source_exists": Path(bound_source).exists() if bound_source else False,
                "prediction_formula_or_meaning": row.get("prediction_formula_or_meaning", ""),
                "prediction_status": prediction_status,
                "prediction_value": prediction_value,
                "score_status": score_status,
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def decision_rows(ts: str) -> list[dict[str, object]]:
    rows = [
        (
            "DEC3756_0_no_flux",
            "NO_FLUX_THEOREM_CONDITIONAL_NOT_SIGNED",
            "Phi_side=0 follows for a fixed topological worldtube with no side crossing, but current sources still mark boundary/owner flux as fail_open.",
        ),
        (
            "DEC3756_1_exchange",
            "PROJECTED_EXCHANGE_ZERO_NOT_PROVED",
            "Pi_M q_exchange=0 requires channel-by-channel silence; kappa, boundary, domain, memory, and range channels remain live.",
        ),
        (
            "DEC3756_2_runner",
            "COUPLING_DRY_RUNNER_EMITTED",
            "The 3755 residual vector is now machine-dry-runnable and blocks claims until theorem-zero or numeric/table predictions are supplied.",
        ),
        (
            "DEC3756_3_next",
            "FILL_FIRST_RUNNER_ROW_OR_PROVE_NO_FLUX",
            "Best next move is either prove the side-flux/exchange zero clauses or fill the first scoreable Gdot/WEP/R10 residual input.",
        ),
    ]
    return [
        {
            **base(ts),
            "decision_id": decision_id,
            "decision": decision,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for decision_id, decision, meaning in rows
    ]


def claim_gate_rows(ts: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    all_sources = all(bool(row["exists"]) for row in grouped["sources"])
    runner_count = len(grouped["runner"]) == len(read_csv(source_paths()["SRC3756_1_3755_residual_vector"]))
    gates = [
        ("CG3756_0_sources", "all 3756 source paths exist", all_sources, "path hygiene"),
        ("CG3756_1_balance", "Ward flux balance imported", True, "Delta ell_M = -Phi_side + int Pi_M q_exchange"),
        ("CG3756_2_side_flux_zero", "Phi_side=0 fully proved", False, "conditional only; boundary flux fail_open remains"),
        ("CG3756_3_projected_exchange_zero", "Pi_M q_exchange=0 fully proved", False, "channel-by-channel exchange zero not signed"),
        ("CG3756_4_runner", "coupling dry-runner rows emitted", runner_count, "one row per 3755 residual"),
        ("CG3756_5_runner_claim_ready", "any runner row claim-ready", False, "predictions are missing/theorem-dependent"),
        ("CG3756_6_newton_claim", "Newton source calibration claim allowed", False, "no-flux/exchange and runner inputs incomplete"),
        ("CG3756_7_local_gr_claim", "local GR/PPN claim allowed", False, "PPN/source vector remains nonclaim"),
    ]
    return [
        {
            **base(ts),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in gates
    ]


def next_target_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "next_id": "NEXT3756_0",
            "target_doc": "3757-Y5-R2FR-first-coupling-runner-fill-or-side-flux-zero-proof.md",
            "target_script": "scripts/Y5_R2FR_3757_first_coupling_runner_fill_or_side_flux_zero_proof.py",
            "objective": "fill the first scoreable coupling runner row, prioritizing Gdot or WEP/source-charge, or prove the side-flux/no-projected-exchange clauses that zero the same rows",
            "why_this_next": "3756 creates the runner; the next movement must either supply a theorem-zero source or a numeric/table prediction for at least one live coupling residual",
            "claim_allowed": False,
        }
    ]


def status_rows(ts: str) -> list[dict[str, object]]:
    return [
        {
            **base(ts),
            "status_id": "STATUS3756_0",
            "status": "NO_FLUX_EXCHANGE_ZERO_CONDITIONAL_COUPLING_RUNNER_EMITTED",
            "summary": "3756 sharpens Phi_side=0 and Pi_M q_exchange=0 into explicit conditional theorem clauses, but they remain unsigned. A dry-run coupling residual runner is emitted for the 3755 Gdot/WEP/R10/radial/frame/gamma/beta rows.",
            "claim_allowed": False,
        }
    ]


def validation_rows(ts: str, paths: dict[str, Path], grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    runner = grouped["runner"]
    checks = [
        ("sources_exist", "all 3756 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("csv_parse", "all generated CSVs parse", all(len(read_csv(path)) > 0 for key, path in paths.items() if key not in {"doc", "validation"})),
        ("no_flux_conditional", "conditional side-flux theorem emitted", any(row["no_flux_id"] == "NF3756_2_topological_no_side_flux" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in grouped["no_flux"])),
        ("exchange_not_claimed", "projected exchange remains not claimed", any(row["exchange_id"] == "EX3756_5_verdict" and row["status"] == "NOT_CLAIMED" for row in grouped["exchange"])),
        ("runner_rows", "runner has one row per 3755 residual", len(runner) == len(read_csv(source_paths()["SRC3756_1_3755_residual_vector"]))),
        ("runner_blocks_claims", "runner rows remain nonclaim", all(str(row["claim_allowed"]) == "False" or row["claim_allowed"] is False for row in runner)),
        ("gdot_row", "runner includes Gdot row", any(row["residual_id"] == "KRV3755_0_Gdot" for row in runner)),
        ("r10_curve_block", "runner blocks alpha curve placeholder", any(row["residual_id"] == "KRV3755_2_range" and row["score_status"] == "BLOCKED_ALPHA_LAMBDA_CURVE_REQUIRED" for row in runner)),
        ("claim_gate_blocked", "local GR claim remains false", any(row["gate_id"] == "CG3756_7_local_gr_claim" and row["passed"] is False for row in grouped["gates"])),
        ("next_target", "3757 target emitted", grouped["next"][0]["target_doc"] == "3757-Y5-R2FR-first-coupling-runner-fill-or-side-flux-zero-proof.md"),
        ("no_formalization_leak", "no 3756 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3756*"))),
    ]
    return [
        {
            **base(ts),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if passed else "FAIL",
            "details": "",
        }
        for validation_id, description, passed in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3756 — No-Flux / Projected Exchange Or Coupling Runner",
        "",
        "## Status",
        "",
        "`NO_FLUX_EXCHANGE_ZERO_CONDITIONAL_COUPLING_RUNNER_EMITTED`.",
        "",
        "This checkpoint tries the theorem route first. It does not claim the source flux vanishes: it records the exact clauses needed and emits a dry-run runner for every live coupling residual.",
        "",
        "## No-Flux Clauses",
    ]
    for row in grouped["no_flux"]:
        lines.append(f"- `{row['no_flux_id']}` `{row['status']}`: {row['statement_or_formula']} — {row['impact']}")
    lines.extend(["", "## Projected Exchange Clauses"])
    for row in grouped["exchange"]:
        lines.append(f"- `{row['exchange_id']}` `{row['status']}`: {row['statement_or_formula']} — {row['impact']}")
    lines.extend(["", "## Runner Spec"])
    for row in grouped["runner_spec"]:
        lines.append(f"- `{row['runner_spec_id']}`: {row['rule']} — {row['meaning']}")
    lines.extend(["", "## Dry-Run Runner Rows"])
    for row in grouped["runner"]:
        lines.append(
            f"- `{row['runner_row_id']}` `{row['score_status']}`: `{row['symbol']}` arena `{row['arena']}` bound `{row['bound_value']} {row['units']}`"
        )
    lines.extend(["", "## Claim Gates"])
    for row in grouped["gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} — {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decisions"]:
        lines.append(f"- `{row['decision_id']}` `{row['decision']}`: {row['meaning']}")
    lines.extend(["", "## Next Target"])
    for row in grouped["next"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Source Register"])
    for row in grouped["sources"]:
        lines.append(f"- `{row['source_id']}` exists=`{row['exists']}`: `{row['source_path']}`")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    paths = {
        "doc": DOC_PATH,
        "sources": RESIDUALS / "P8_Y5_R2FR_3756_SOURCE_REGISTER.csv",
        "no_flux": RESIDUALS / "P8_Y5_R2FR_3756_NO_FLUX_THEOREM_CLAUSES.csv",
        "exchange": RESIDUALS / "P8_Y5_R2FR_3756_PROJECTED_EXCHANGE_CLAUSES.csv",
        "runner_spec": RESIDUALS / "P8_Y5_R2FR_3756_COUPLING_RUNNER_SPEC.csv",
        "runner": RESIDUALS / "P8_Y5_R2FR_3756_COUPLING_RUNNER_DRYRUN_RESULTS.csv",
        "gates": RESIDUALS / "P8_Y5_R2FR_3756_CLAIM_GATES.csv",
        "decisions": RESIDUALS / "P8_Y5_R2FR_3756_DECISION_ROWS.csv",
        "next": RESIDUALS / "P8_Y5_R2FR_3756_NEXT_TARGET.csv",
        "status": RESIDUALS / "P8_Y5_R2FR_3756_STATUS.csv",
        "validation": RESIDUALS / "P8_Y5_BRR545_3756_VALIDATION.csv",
    }
    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "no_flux": no_flux_rows(timestamp),
        "exchange": exchange_rows(timestamp),
        "runner_spec": runner_spec_rows(timestamp),
        "runner": runner_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = claim_gate_rows(timestamp, grouped)
    for key, rows in grouped.items():
        write_csv(paths[key], rows)
    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")
    grouped["validation"] = validation_rows(timestamp, paths, grouped)
    write_csv(paths["validation"], grouped["validation"])
    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3756 validation failed: {failures}")
    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists() and str(cache.resolve()).startswith(str(PCW.resolve())):
        shutil.rmtree(cache)
    print("wrote 3756 checkpoint: no-flux/exchange zero conditional; coupling dry-runner emitted")


if __name__ == "__main__":
    main()
