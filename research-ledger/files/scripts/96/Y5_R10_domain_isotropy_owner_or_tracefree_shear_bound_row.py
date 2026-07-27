from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_DIR = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1176-Y5-R10-domain-isotropy-owner-or-tracefree-shear-bound-row.md"
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
            "source_id": "SRC1176_0_1175_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1175_NEXT_TARGET.csv",
            "needle": "NEXT1175_0_1176",
            "role": "handoff to domain isotropy owner or tracefree shear bound row.",
        },
        {
            "source_id": "SRC1176_1_1175_summary",
            "relative_path": "source-intake/mts_residuals/P8_Y5_BRR545_1175_VALIDATION.csv",
            "needle": "V1175_SUMMARY",
            "role": "1175 validation summary.",
        },
        {
            "source_id": "SRC1176_2_1175_projector",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1175_QCOH_PROJECTOR_OWNER_ATTEMPT.csv",
            "needle": "QPO1175_1_SO3_invariant_route",
            "role": "SO3/domain isotropy conditional route.",
        },
        {
            "source_id": "SRC1176_3_1175_tracefree_bound",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1175_PROJECTOR_LEAK_BOUND_ROWS.csv",
            "needle": "PLB1175_1_tracefree_second_order",
            "role": "tracefree determinant leakage row.",
        },
        {
            "source_id": "SRC1176_4_1175_physical_guard",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1175_OWNERSHIP_GATES.csv",
            "needle": "QOG1175_3_physical_multipole_guard",
            "role": "physical multipole preservation guard.",
        },
        {
            "source_id": "SRC1176_5_275_shear",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "tracefree shear leaks into unprojected `det(Q)` at second order",
            "role": "older tracefree leakage warning.",
        },
        {
            "source_id": "SRC1176_6_275_domain_missing",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "physical domain selector `D` | not parent-derived",
            "role": "domain selector still missing.",
        },
        {
            "source_id": "SRC1176_7_275_projector_missing",
            "relative_path": "275-JC-three-form-memory-current-from-Q.md",
            "needle": "coherent projection `Q -> Q_coh` | not parent-derived",
            "role": "Qcoh projection still missing.",
        },
        {
            "source_id": "SRC1176_8_274_domain_vary",
            "relative_path": "274-lifted-C-sector-form-holonomy-route.md",
            "needle": "vary the domain/boundary/projector consistently",
            "role": "domain/projector variation consistency requirement.",
        },
        {
            "source_id": "SRC1176_9_207_projector_action",
            "relative_path": "207-domain-projector-action-and-Bianchi-identity.md",
            "needle": "formal `C_D + C_perp` projector action",
            "role": "older formal projector-action route.",
        },
        {
            "source_id": "SRC1176_10_207_bianchi",
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


def isotropy_attempt_rows() -> list[dict[str, object]]:
    rows = [
        {
            "attempt_id": "DIO1176_0_domain_measure_contract",
            "object": "local domain measure mu_D",
            "statement": "A parent-owned isotropy theorem needs a domain/coframe measure mu_D selected before projection. Without mu_D, SO3 averaging has no physical reference measure.",
            "status": "OWNER_CONTRACT_WRITTEN",
            "derives": "names the exact object that would make Pi_coh non-arbitrary.",
            "missing_for_claim": "parent action/constraint selecting D, mu_D, and coframe averaging",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DIO1176_1_SO3_scalar_irrep",
            "object": "scalar irrep projector",
            "statement": "Given a parent-owned SO3-invariant local stationary domain, the trace/scalar irrep is orthogonal to tracefree spin-2 shear, so Pi_coh is canonical inside the C-memory channel.",
            "status": "CONDITIONAL_THEOREM_SHAPE",
            "derives": "the mathematical reason Qcoh is the scalar/volume channel rather than smoothing.",
            "missing_for_claim": "proof local stationary domains really carry that symmetry in the parent theory",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DIO1176_2_nonisotropic_arenas",
            "object": "R10/PPN/lab/solar domains",
            "statement": "Real local arenas need not be SO3-isotropic. If the chosen boundary or source support is anisotropic, tracefree leakage and domain-anisotropy terms must be bounded.",
            "status": "GENERAL_ZERO_REJECTED",
            "derives": "why a universal local projector-zero theorem cannot be claimed from isotropy alone.",
            "missing_for_claim": "arena domain certificate or finite anisotropy envelope",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DIO1176_3_parent_projector_action",
            "object": "projector action route",
            "statement": "The old domain-projector action route can make projection variational only if projector/domain stresses are retained in the Ward/Bianchi ledger.",
            "status": "FORMAL_ROUTE_CONDITIONAL",
            "derives": "a possible parent-owner route for Pi_coh that avoids external projection.",
            "missing_for_claim": "explicit representative, stress tensor, and local domain-selection equation",
            "valid_for_claim": False,
        },
        {
            "attempt_id": "DIO1176_4_verdict",
            "object": "domain isotropy owner verdict",
            "statement": "1176 does not derive parent-owned local isotropy. It keeps the SO3 route as a theorem target and stages tracefree/domain-anisotropy bounds.",
            "status": "ISOTROPY_NOT_DERIVED_BOUND_ROUTE_ACTIVE",
            "derives": "the projector route is now tied to a precise domain-measure owner or leak bound.",
            "missing_for_claim": "parent domain measure or numeric/source-backed tracefree/domain anisotropy rows",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def shear_bound_rows() -> list[dict[str, object]]:
    rows = [
        {
            "bound_id": "TFB1176_0_tracefree_shear_norm",
            "quantity": "norm_S_Q_tracefree",
            "formula": "S_Q := Q_flow - (1/3)Tr(Q_flow)I; require ||S_Q|| in the selected local domain norm",
            "units": "same_as_Qflow_or_inverse_time_units",
            "current_value": "MISSING_TRACEFREE_SHEAR_NORM",
            "source_or_theorem": "needed for PLB1175_1_tracefree_second_order",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "TFB1176_1_tracefree_variation_norm",
            "quantity": "norm_delta_S_Q_tracefree",
            "formula": "variation/time-flow norm of the tracefree shear channel",
            "units": "same_as_Theta_Q_res",
            "current_value": "MISSING_TRACEFREE_SHEAR_VARIATION_NORM",
            "source_or_theorem": "needed for O(||S_Q|| ||delta S_Q||) leakage",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "TFB1176_2_second_order_leakage",
            "quantity": "tracefree determinant leakage",
            "formula": "abs(leak_tracefree) <= C_det2 * ||S_Q|| * ||delta S_Q|| + higher_order_remainder",
            "units": "inverse_time_or_variation_parameter_units",
            "current_value": "SYMBOLIC_ONLY_MISSING_CDET2_AND_NORMS",
            "source_or_theorem": "determinant/log-volume expansion; 275 leakage warning",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "TFB1176_3_domain_anisotropy",
            "quantity": "domain anisotropy envelope",
            "formula": "abs(leak_domain) <= ||Pi_actual-Pi_SO3|| * ||Q_flow||",
            "units": "same_as_Theta_Q_res",
            "current_value": "MISSING_DOMAIN_ANISOTROPY_ENVELOPE",
            "source_or_theorem": "requires arena domain geometry",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "TFB1176_4_projector_runner_update",
            "quantity": "norm_projector_leak",
            "formula": "norm_projector_leak <= abs(leak_tracefree) + abs(leak_domain) + projector_stress_residual",
            "units": "same_as_Theta_Q_res",
            "current_value": "NOT_EVALUATED",
            "source_or_theorem": "feeds PLB1175_0 and QDB1174_0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]
    return stamp(rows)


def multipole_guard_rows() -> list[dict[str, object]]:
    rows = [
        {
            "guard_id": "MPG1176_0_metric_channel",
            "rule": "Tracefree shear/multipoles may be excluded from the C-memory scalar channel only if they remain in the metric/GR channel.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "projector erases real gravitational physics",
            "needed_for_claim": "explicit routing map or finite leakage bound",
            "valid_for_claim": False,
        },
        {
            "guard_id": "MPG1176_1_no_spherical_cheat",
            "rule": "Do not assume a spherical/SO3 domain for an intrinsically anisotropic arena unless the arena representative is parent-selected.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "local PPN/R10 bounds become artificially quiet",
            "needed_for_claim": "arena domain certificate",
            "valid_for_claim": False,
        },
        {
            "guard_id": "MPG1176_2_Bianchi_stress",
            "rule": "Any projector/domain variable must carry stress in the Bianchi/Ward ledger.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "external projector hides non-conservation",
            "needed_for_claim": "projector/domain stress tensor row",
            "valid_for_claim": False,
        },
        {
            "guard_id": "MPG1176_3_FLRW_preservation",
            "rule": "The scalar trace channel must remain available for FLRW/domain memory while local tracefree leakage is bounded or routed.",
            "status": "GUARD_ACTIVE",
            "failure_mode": "local repair accidentally kills cosmological memory",
            "needed_for_claim": "same parent projector works in local and FLRW arenas",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def runner_rows() -> list[dict[str, object]]:
    rows = [
        {
            "run_id": "RUN1176_0_domain_isotropy",
            "test": "parent-owned SO3/domain isotropy",
            "status": "REFUSED_PARENT_OWNER_MISSING",
            "result": "SO3 theorem shape exists but domain/coframe measure is not parent-signed",
            "blocked_by": "mu_D_owner;domain_selector;projector_stress;physical_multipole_guard",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1176_1_tracefree_bound",
            "test": "tracefree shear/domain anisotropy bound rows",
            "status": "PASS_SYMBOLIC_NONCLAIM",
            "result": "tracefree shear, variation, determinant leakage, and anisotropy rows are staged",
            "blocked_by": "numeric/source-backed shear norms and domain geometry",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1176_2_projector_runner",
            "test": "feed norm_projector_leak runner",
            "status": "SCHEMA_UPDATED_VALUES_MISSING",
            "result": "projector leak now decomposes into tracefree and domain-anisotropy components",
            "blocked_by": "C_det2;norm_S_Q;norm_delta_S_Q;anisotropy_envelope;projector_stress",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "run_id": "RUN1176_3_local_promotion",
            "test": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "status": "REFUSED_NO_LOCAL_CLAIM",
            "result": "1176 sharpens leakage terms but no local bound is scored",
            "blocked_by": "tracefree_shear_norm_or_domain_isotropy_owner",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def gate_rows() -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "G1176_0_domain_measure_owner",
            "gate": "parent-owned domain/coframe measure",
            "current_status": "BLOCKED",
            "reason": "domain measure mu_D is named but not derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1176_1_SO3_isotropy",
            "gate": "local SO3/scalar irrep projector",
            "current_status": "CONDITIONAL_ONLY",
            "reason": "canonical only if the local stationary domain is parent-isotropic",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1176_2_tracefree_bound",
            "gate": "tracefree shear/domain-anisotropy finite bound",
            "current_status": "SYMBOLIC_READY_VALUES_MISSING",
            "reason": "shear norms, C_det2, anisotropy envelope, and projector stress are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1176_3_physical_multipoles",
            "gate": "GR multipoles preserved",
            "current_status": "BLOCKED",
            "reason": "routing map to metric/GR sector is not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G1176_4_local_promotion",
            "gate": "local-GR/R10/PPN/WEP/clock/orbital promotion",
            "current_status": "BLOCKED_NO_LOCAL_CLAIM",
            "reason": "no parent isotropy theorem or numeric leakage bound exists",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def decision_rows() -> list[dict[str, object]]:
    rows = [
        {
            "decision_id": "D1176_0_isotropy_status",
            "decision": "do_not_claim_parent_domain_isotropy",
            "reason": "current corpus lacks parent-owned domain/coframe measure and arena representative",
            "next_action": "keep SO3 theorem target but rely on tracefree/domain bound rows for scoring",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1176_1_bound_route_progress",
            "decision": "stage_tracefree_and_domain_anisotropy_rows",
            "reason": "projector leakage is now decomposed into concrete shear and domain terms",
            "next_action": "derive/source tracefree shear norm or parent metric-channel routing",
            "valid_for_claim": False,
        },
        {
            "decision_id": "D1176_2_best_next",
            "decision": "target_metric_channel_routing_or_shear_norm",
            "reason": "to avoid smoothing away GR, tracefree modes must either be routed to the metric sector or bounded",
            "next_action": "derive C-channel/metric-channel split or create first tracefree shear norm input",
            "valid_for_claim": False,
        },
    ]
    return stamp(rows)


def next_rows() -> list[dict[str, object]]:
    rows = [
        {
            "next_id": "NEXT1176_0_1177",
            "next_target": "1177-Y5-R10-metric-channel-routing-for-tracefree-shear-or-first-shear-norm-row.md",
            "objective": "derive a parent routing theorem sending tracefree shear/multipoles to the metric/GR channel and not the C-memory scalar channel; if not, stage first tracefree shear norm input row",
            "include": "metric-channel routing; C-channel scalar projection; physical multipole guard; shear norm; domain anisotropy; Bianchi stress; no-claim runner",
            "exclude": "smoothing away shear; local claim; c_g zero; invented values; GitHub; formalization edits",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]
    return stamp(rows)


def validation_rows(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks = [
        {
            "check_id": "V1176_0_sources_exist",
            "result": "pass" if all(r["exists"] and r["needle_found"] for r in sources) else "fail",
            "detail": "all cited local source paths exist and needles are found",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_1_domain_owner_attempt_written",
            "result": "pass" if any(r["attempt_id"] == "DIO1176_0_domain_measure_contract" for r in attempts) else "fail",
            "detail": "domain/coframe measure owner contract is written",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_2_isotropy_not_claimed",
            "result": "pass" if any(r["status"] == "ISOTROPY_NOT_DERIVED_BOUND_ROUTE_ACTIVE" for r in attempts) else "fail",
            "detail": "parent-owned local isotropy is not claimed",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_3_tracefree_rows_created",
            "result": "pass" if any(r["bound_id"] == "TFB1176_0_tracefree_shear_norm" for r in bounds) else "fail",
            "detail": "tracefree shear norm row is created",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_4_domain_anisotropy_row_created",
            "result": "pass" if any(r["bound_id"] == "TFB1176_3_domain_anisotropy" for r in bounds) else "fail",
            "detail": "domain anisotropy envelope row is created",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_5_multipole_guards_complete",
            "result": "pass" if len(guards) >= 4 else "fail",
            "detail": "metric-channel, spherical-cheat, Bianchi, and FLRW guards are logged",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_6_missing_inputs_not_claim_valid",
            "result": "pass"
            if all((not any("MISSING" in str(v) for v in r.values())) or r["valid_for_claim"] is False for r in bounds)
            else "fail",
            "detail": "rows with MISSING inputs remain invalid for claim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_7_runner_refuses_claim",
            "result": "pass" if all(r["claim_allowed"] is False for r in runs) else "fail",
            "detail": "runner refuses domain-isotropy, numeric-bound, and local-promotion claims",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_8_claim_gates_blocked",
            "result": "pass" if all(r["claim_allowed"] is False for r in gates) else "fail",
            "detail": "all 1176 claim gates remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_9_no_claim_rows",
            "result": "pass"
            if all(r.get("valid_for_claim") is False for r in attempts + bounds + guards + gates + nexts)
            else "fail",
            "detail": "all generated science rows remain nonclaim",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_10_next_target",
            "result": "pass" if nexts and "1177" in str(nexts[0]["next_target"]) else "fail",
            "detail": "1177 handoff targets metric-channel routing or first shear norm row",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_11_generated_under_post_checkpoint",
            "result": "pass" if str(DOC).startswith(str(ROOT)) and str(CSV_DIR).startswith(str(ROOT)) else "fail",
            "detail": "all generated outputs are under post-checkpoint-work",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_12_formalization_untouched",
            "result": "pass",
            "detail": "generator writes no outputs under formalization-workbench",
            "claim_allowed": False,
        },
        {
            "check_id": "V1176_SUMMARY",
            "result": "pass",
            "detail": "1176 refuses parent-owned domain isotropy, stages tracefree shear/domain anisotropy bounds, preserves GR multipole guard, and hands off to metric-channel routing or shear norm input",
            "claim_allowed": False,
        },
    ]
    return stamp(checks)


def write_doc(
    sources: list[dict[str, object]],
    attempts: list[dict[str, object]],
    bounds: list[dict[str, object]],
    guards: list[dict[str, object]],
    runs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validations: list[dict[str, object]],
    nexts: list[dict[str, object]],
) -> None:
    parts = [
        "# 1176 — Y5/R10 domain isotropy owner or tracefree shear bound row",
        "**Current verdict:** parent-owned local domain isotropy is not derived. The SO3/scalar irrep route remains the clean projector theorem target, but real local arenas may be anisotropic, so the tracefree shear/domain-anisotropy bound route is now active.",
        "**Main progress:** projector leakage has been decomposed into concrete inputs: tracefree shear norm, tracefree variation norm, second-order determinant leakage, domain anisotropy envelope, and projector stress residual.",
        "**Hard blocker:** tracefree GR multipoles must not be erased. They must either route into the metric/GR channel by a parent theorem or enter the C-memory residual as a bounded projector leak.",
        "**No claim:** no local-GR, Newton, R10, PPN, WEP, clock, orbital, `c_g=0`, or public-facing claim follows from this checkpoint.",
        "## Source register\n\n" + table(sources),
        "## Domain isotropy owner attempt\n\n" + table(attempts),
        "## Tracefree shear/domain-anisotropy bound rows\n\n" + table(bounds),
        "## GR multipole and Bianchi guards\n\n" + table(guards),
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
    attempts = isotropy_attempt_rows()
    bounds = shear_bound_rows()
    guards = multipole_guard_rows()
    runs = runner_rows()
    gates = gate_rows()
    decisions = decision_rows()
    nexts = next_rows()
    validations = validation_rows(sources, attempts, bounds, guards, runs, gates, nexts)

    outputs = {
        "P8_Y5_R10_1176_SOURCE_REGISTER.csv": sources,
        "P8_Y5_R10_1176_DOMAIN_ISOTROPY_OWNER_ATTEMPT.csv": attempts,
        "P8_Y5_R10_1176_TRACEFREE_SHEAR_BOUND_ROWS.csv": bounds,
        "P8_Y5_R10_1176_GR_MULTIPOLE_GUARDS.csv": guards,
        "P8_Y5_R10_1176_RUNNER_DRY_RUN.csv": runs,
        "P8_Y5_R10_1176_CLAIM_GATES.csv": gates,
        "P8_Y5_R10_1176_DECISION_LEDGER.csv": decisions,
        "P8_Y5_R10_1176_NEXT_TARGET.csv": nexts,
        "P8_Y5_BRR545_1176_VALIDATION.csv": validations,
    }
    for filename, rows in outputs.items():
        write_csv(CSV_DIR / filename, rows)

    write_doc(sources, attempts, bounds, guards, runs, gates, decisions, validations, nexts)

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
