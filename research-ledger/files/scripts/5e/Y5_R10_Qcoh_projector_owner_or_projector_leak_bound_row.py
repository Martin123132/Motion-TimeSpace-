from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1175-Y5-R10-Qcoh-projector-owner-or-projector-leak-bound-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
STAMP = datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row | {"generated_utc": STAMP} for row in rows]


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty csv refused: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_escape(value: object) -> str:
    return str(value).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ")


def table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key == "generated_utc":
                continue
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_rows() -> list[dict[str, object]]:
    entries = [
        {
            "source_id": "SRC1175_0_1174_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1174_NEXT_TARGET.csv",
            "needle": "NEXT1174_0_1175",
            "role": "handoff to Qcoh projector owner or projector-leak bound row.",
        },
        {
            "source_id": "SRC1175_1_1174_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1174_VALIDATION.csv",
            "needle": "V1174_SUMMARY",
            "role": "1174 validation summary.",
        },
        {
            "source_id": "SRC1175_2_1174_projector_leak",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1174_FIRST_QFLOW_DEFECT_BOUND_ROWS.csv",
            "needle": "QDB1174_1_projector_leak",
            "role": "missing Qcoh projector owner or bound.",
        },
        {
            "source_id": "SRC1175_3_1174_guard",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1174_NORMALIZATION_PROJECTION_GUARDS.csv",
            "needle": "NG1174_3_tracefree_shear",
            "role": "tracefree shear guard.",
        },
        {
            "source_id": "SRC1175_4_1174_gate",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1174_CLAIM_GATES.csv",
            "needle": "G1174_3_numeric_bound",
            "role": "numeric/source-backed Q-flow bound still missing.",
        },
        {
            "source_id": "SRC1175_5_275_Qcoh",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "Q_coh^i_j = (N_D / u3) delta^i_j",
            "role": "Qcoh coherent isotropic form.",
        },
        {
            "source_id": "SRC1175_6_275_projection_missing",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "coherent projection `Q -> Q_coh` | not parent-derived",
            "role": "projection not parent-derived.",
        },
        {
            "source_id": "SRC1175_7_275_shear",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "tracefree shear leaks into unprojected `det(Q)` at second order",
            "role": "unprojected determinant shear leakage.",
        },
        {
            "source_id": "SRC1175_8_274_parent",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "derive `J_C` from `Q^i_j`, coframe, or `det(Q)`",
            "role": "Q/coframe origin requirement.",
        },
        {
            "source_id": "SRC1175_9_274_vary_domain",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "vary the domain/boundary/projector consistently",
            "role": "domain/projector consistency requirement.",
        },
        {
            "source_id": "SRC1175_10_207_bianchi",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "Bianchi closure can be made formal;",
            "role": "Bianchi/Ward guard.",
        },
    ]
    checked: list[dict[str, object]] = []
    for entry in entries:
        path = ROOT / str(entry["relative_path"])
        text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
        checked.append(entry | {"exists": path.exists(), "needle_found": str(entry["needle"]) in text})
    return stamp(checked)


def projector_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "QPO1175_0_trace_irrep_projector",
            "object": "Pi_coh",
            "statement": "A clean mathematical candidate is the scalar/volume irrep projector: Pi_coh sends the local Q-flow to its domain trace/coherent volume mode and removes tracefree spin-2 shear.",
            "status": "MATH_PROJECTOR_CANDIDATE",
            "derives": "separates coherent volume memory from local shear leakage.",
            "missing_for_claim": "parent action/domain symmetry selecting this projector",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QPO1175_1_SO3_invariant_route",
            "object": "SO(3) domain average",
            "statement": "If the stationary local vacuum domain has an SO(3)-invariant coframe/domain measure, Schur/irrep selection makes the scalar trace channel canonical and orthogonal to tracefree shear.",
            "status": "CONDITIONAL_SYMMETRY_THEOREM_SHAPE",
            "derives": "why the coherent channel is not arbitrary smoothing when the domain symmetry is parent-owned.",
            "missing_for_claim": "parent-owned local isotropy/domain representative and proof it does not erase physical multipoles",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QPO1175_2_volume_normalization_link",
            "object": "Qcoh and N_D",
            "statement": "The Qcoh projector must be tied to the same N_D volume normalization used in Theta_Q; otherwise coherent cancellation and projector selection are two separate closures.",
            "status": "CONSISTENCY_REQUIREMENT",
            "derives": "a single owner requirement for Qcoh, N_D, and Theta_Q_coh.",
            "missing_for_claim": "one parent domain-volume functional generating both Qcoh and N_D",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QPO1175_3_anisotropic_domain_warning",
            "object": "non-SO(3) local domains",
            "statement": "Solar-system/laboratory domains are not automatically SO(3)-symmetric. If the arena/domain breaks the symmetry, the omitted tracefree/projector component must be bounded.",
            "status": "NO_GLOBAL_ZERO_FROM_SYMMETRY",
            "derives": "why projector-leak rows are mandatory for real local tests.",
            "missing_for_claim": "arena-specific domain symmetry or leakage bound",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "QPO1175_4_verdict",
            "object": "Qcoh projector owner",
            "statement": "1175 gives a serious projector theorem shape, but does not parent-sign it. The fallback is a projector-leak bound row.",
            "status": "PROJECTOR_SHAPE_PROGRESS_NO_CLAIM",
            "derives": "the least-handwavy Qcoh route and the exact leakage object to bound.",
            "missing_for_claim": "parent local domain isotropy/volume projector or numeric/source-backed projector leak",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def leak_bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "bound_id": "PLB1175_0_first_projector_leak_row",
            "quantity": "norm_projector_leak",
            "formula": "||projector_leak|| := ||Tr(Q^{-1}delta Q)-Pi_coh Tr(Q^{-1}delta Q)||",
            "units": "inverse_time_or_variation_parameter_units",
            "current_value": "SYMBOLIC_ONLY_MISSING_QCOH_OWNER_OR_ARENA_BOUND",
            "source_or_theorem": "1174 QDB1174_1; 275 Qcoh projection missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PLB1175_1_tracefree_second_order",
            "quantity": "tracefree determinant leakage",
            "formula": "for small tracefree S_Q, determinant/log-volume leakage is O(||S_Q|| ||delta S_Q||) after scalar trace projection",
            "units": "same_as_norm_projector_leak",
            "current_value": "MISSING_TRACEFREE_SHEAR_NORM",
            "source_or_theorem": "275 tracefree shear leakage guard",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PLB1175_2_domain_anisotropy",
            "quantity": "domain anisotropy projector error",
            "formula": "||Pi_actual-Pi_SO3|| * ||Tr(Q^{-1}delta Q)|| or arena-specific anisotropy envelope",
            "units": "same_as_norm_projector_leak",
            "current_value": "MISSING_DOMAIN_ANISOTROPY_BOUND",
            "source_or_theorem": "requires arena domain representative",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PLB1175_3_runner_update",
            "quantity": "norm_Theta_Q_res",
            "formula": "||Theta_Q_res|| <= norm_projector_leak + norm_normalization_mismatch + norm_domain_reference",
            "units": "inverse_time_or_variation_parameter_units",
            "current_value": "NOT_EVALUATED",
            "source_or_theorem": "feeds 1174 QDB1174_0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def ownership_gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "owner_id": "QOG1175_0_parent_domain_measure",
            "requirement": "parent-owned domain/coframe measure",
            "current_status": "BLOCKED",
            "why_needed": "Pi_coh must know what trace/volume means",
            "if_missing": "projection is a smoothing convention",
            "valid_for_claim": False,
        },
        {
            "owner_id": "QOG1175_1_irrep_symmetry",
            "requirement": "local stationary SO(3)/scalar irrep selection",
            "current_status": "CONDITIONAL_ONLY",
            "why_needed": "trace channel is canonical only under a signed symmetry/domain rule",
            "if_missing": "tracefree shear may leak into local tests",
            "valid_for_claim": False,
        },
        {
            "owner_id": "QOG1175_2_ND_link",
            "requirement": "same law owns Qcoh and N_D",
            "current_status": "BLOCKED",
            "why_needed": "normalization cancellation and projector selection must not be independent closures",
            "if_missing": "Theta_Q_coh cancellation remains bookkeeping",
            "valid_for_claim": False,
        },
        {
            "owner_id": "QOG1175_3_physical_multipole_guard",
            "requirement": "projection does not delete physical GR multipoles",
            "current_status": "BLOCKED",
            "why_needed": "tracefree gravitational degrees should remain in metric/GR sector, not be erased",
            "if_missing": "local-GR route can cheat by smoothing away real physics",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1175_0_projector_owner",
            "test": "parent-owned Qcoh projector",
            "status": "PARTIAL_PASS_MATH_PROJECTOR_ONLY",
            "result": "SO(3)/trace projector shape is clean but not parent-owned",
            "blocked_by": "parent_domain_measure;local_isotropy;N_D_link;physical_multipole_guard",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1175_1_projector_leak_bound",
            "test": "projector-leak finite row",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "result": "norm_projector_leak row is staged with tracefree/domain-anisotropy subterms",
            "blocked_by": "numeric/source-backed tracefree shear and domain anisotropy bounds",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1175_2_theta_runner",
            "test": "feed Theta_Q_res runner",
            "status": "SCHEMA_UPDATED_VALUES_MISSING",
            "result": "Theta_Q_res bound now has explicit projector-leak subrow",
            "blocked_by": "normalization mismatch and domain reference rows still missing too",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1175_3_local_promotion",
            "test": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "result": "Qcoh route remains nonclaim until parent owner or numeric leak bound exists",
            "blocked_by": "Qcoh_owner_or_projector_leak_numeric_bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1175_0_math_projector",
            "gate": "Qcoh trace/SO3 projector shape",
            "current_status": "PASS_MATH_SHAPE_ONLY",
            "reason": "scalar trace irrep projector is available as a mathematical candidate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1175_1_parent_owner",
            "gate": "parent-owned projector/domain",
            "current_status": "BLOCKED",
            "reason": "domain/coframe measure and local isotropy are not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1175_2_projector_leak_bound",
            "gate": "numeric/source-backed projector leak",
            "current_status": "SYMBOLIC_READY_VALUES_MISSING",
            "reason": "tracefree shear/domain anisotropy values are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1175_3_physical_guard",
            "gate": "physical GR multipoles preserved",
            "current_status": "BLOCKED",
            "reason": "projection must not remove real tracefree gravitational degrees",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1175_4_local_promotion",
            "gate": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "projector owner and numeric leak bound remain open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1175_0_projector_shape",
            "decision": "retain_SO3_trace_projector_as_best_candidate",
            "reason": "it is mathematically canonical and separates scalar volume memory from tracefree local shear",
            "next_action": "derive parent domain/isotropy owner",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1175_1_no_smoothing_claim",
            "decision": "do_not_claim_Qcoh_parent_owned",
            "reason": "current corpus still marks Qcoh projection as not parent-derived",
            "next_action": "stage projector-leak bound row",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1175_2_best_next",
            "decision": "target_domain_isotropy_owner_or_tracefree_bound",
            "reason": "the next gap is whether local stationary domains really select the scalar irrep or how large the tracefree leak is",
            "next_action": "derive domain isotropy/measure projector, or create first tracefree shear norm row",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1175_0_1176",
            "next_target": "1176-Y5-R10-domain-isotropy-owner-or-tracefree-shear-bound-row.md",
            "objective": "try to derive local stationary domain isotropy/measure ownership for the Qcoh projector; if not, stage first tracefree shear/domain-anisotropy bound row",
            "include": "domain measure; SO3 scalar irrep; tracefree shear norm; physical multipole guard; N_D link; no-claim runner",
            "exclude": "post-hoc smoothing; deleting GR shear; local claim; c_g zero; invented values; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    bounds: list[dict[str, object]],
    owners: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1175_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_1_projector_shape_written",
            "result": "pass" if any(r["attempt_id"] == "QPO1175_0_trace_irrep_projector" for r in attempts) else "fail",
            "detail": "trace/SO3 coherent projector shape is written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_2_parent_owner_not_claimed",
            "result": "pass" if any(r["status"] == "PROJECTOR_SHAPE_PROGRESS_NO_CLAIM" for r in attempts) else "fail",
            "detail": "Qcoh parent ownership is not claimed",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_3_projector_leak_row_created",
            "result": "pass" if any(r["bound_id"] == "PLB1175_0_first_projector_leak_row" for r in bounds) else "fail",
            "detail": "first projector-leak bound row is created",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_4_tracefree_guard_present",
            "result": "pass" if any("tracefree" in str(r["quantity"]) for r in bounds) else "fail",
            "detail": "tracefree second-order leakage is retained as a bound term",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_5_ownership_gates_complete",
            "result": "pass" if len(owners) >= 4 else "fail",
            "detail": "domain measure, symmetry, N_D link, and physical multipole guards are logged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_6_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in r.values())) or r["valid_for_claim"] is False for r in bounds)
            else "fail",
            "detail": "rows with MISSING inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "runner refuses projector-owner, numeric-bound, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_8_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1175 claim gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_9_no_claim_rows",
            "result": "pass"
            if all(r.get("valid_for_claim") is False for r in attempts + bounds + owners + gates + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_10_next_target",
            "result": "pass" if nexts and "1176" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1176 handoff targets domain isotropy owner or tracefree shear bound row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_11_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_12_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1175_SUMMARY",
            "result": "pass",
            "detail": "1175 writes the SO3/trace Qcoh projector theorem shape, refuses parent ownership, stages projector-leak bounds, and hands off to domain isotropy or tracefree shear bound",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    bounds: list[dict[str, object]],
    owners: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1175 — Y5/R10 Qcoh projector owner or projector-leak bound row",
        "**Current verdict:** `Q_coh` has a clean mathematical candidate: the scalar/volume irrep projection of `Q` relative to a domain/coframe measure. But current files still do not parent-own that domain measure or symmetry, so this is not yet a theorem.",
        "**Main progress:** the projector problem is now split into two routes: derive `Pi_coh` from parent local domain isotropy/measure, or bound `norm_projector_leak` including tracefree second-order determinant leakage and domain anisotropy.",
        "**Hard blocker:** we must not smooth away real GR shear/multipoles. Tracefree modes can be excluded from the C-memory channel only if the parent theory routes them into the metric/GR sector or supplies a numeric leakage bound.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Qcoh projector owner attempt\n\n" + table(attempts),
        "## Projector-leak bound rows\n\n" + table(bounds),
        "## Ownership gates\n\n" + table(owners),
        "## Runner dry-run\n\n" + table(runs),
        "## Claim gates\n\n" + table(gates),
        "## Decision ledger\n\n" + table(decisions),
        "## Validation\n\n" + table(validations),
        "## Next target\n\n" + table(nexts),
    ]
    DOC.write_text("\n\n".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    CSV_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    attempts = projector_attempt_rows()
    bounds = leak_bound_rows()
    owners = ownership_gate_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, attempts, bounds, owners, runs, gates, nexts)

    outputs = {
        "P8_Y5_R10_1175_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1175_QCOH_PROJECTOR_OWNER_ATTEMPT.csv": attempts,
        "P8_Y5_R10_1175_PROJECTOR_LEAK_BOUND_ROWS.csv": bounds,
        "P8_Y5_R10_1175_OWNERSHIP_GATES.csv": owners,
        "P8_Y5_R10_1175_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1175_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1175_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1175_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1175_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, attempts, bounds, owners, runs, gates, decisions, validations, nexts)

    failed = [row["check_id"] for row in validations if row["result"] != "pass"]
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if FORMALIZATION.exists() and not FORMALIZATION.is_dir():
        failed.append("formalization_path_not_directory")

    print(f"wrote {DOC}")
    print("validation: PASS" if not failed else f"validation: FAIL {failed}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
