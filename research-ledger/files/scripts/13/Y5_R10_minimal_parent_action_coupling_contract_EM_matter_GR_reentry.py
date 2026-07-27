from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "990-Y5-R10-minimal-parent-action-coupling-contract-EM-matter-GR-reentry.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def md_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(md_cell(row.get(column, "")) for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "989_doc",
            "path": "989-Y5-R10-EM-lock-signature-input-or-alpha-source-normalization-owner.md",
            "role": "immediate coupling-owner handoff",
            "needle": "DEC989_3_best_next",
        },
        {
            "source_id": "989_EM_lock",
            "path": "source-intake/mts_residuals/P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
            "role": "EM-lock signature status",
            "needle": "ELA989_5_total",
        },
        {
            "source_id": "989_beta_source",
            "path": "source-intake/mts_residuals/P8_Y5_R10_989_BETA_SOURCE_OWNER_LEDGER.csv",
            "role": "finite alpha source-normalization debt",
            "needle": "BSO989_3_not_clock_screen",
        },
        {
            "source_id": "768_doc",
            "path": "768-Y5-R10-local-GR-EH-or-R11-reentry-after-alpha-WEP-quarantine.md",
            "role": "local GR reentry and Hamiltonian PiM live edge",
            "needle": "FB554_0_HPiM_integrability_reference_bound",
        },
        {
            "source_id": "768_EH_R11",
            "path": "source-intake/mts_residuals/P8_Y5_R10_768_EH_R11_REENTRY_AUDIT.csv",
            "role": "EH/R11 reentry audit",
            "needle": "EHR768_5_Hamiltonian_PiM",
        },
        {
            "source_id": "768_GR_Newton",
            "path": "source-intake/mts_residuals/P8_Y5_R10_768_GR_NEWTON_REQUIREMENT_MAP.csv",
            "role": "GR/Newton requirement map",
            "needle": "GN768_3_HPiM_integrability",
        },
        {
            "source_id": "768_source_edge",
            "path": "source-intake/mts_residuals/P8_Y5_R10_768_R11_SOURCE_NORMALIZATION_LIVE_EDGE.csv",
            "role": "source-normalization live edge",
            "needle": "RSN768_4_HPiM_repair",
        },
        {
            "source_id": "655_EH_premise",
            "path": "source-intake/mts_residuals/P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
            "role": "EH-only premise audit",
            "needle": "EHP655_P8_source_normalization",
        },
        {
            "source_id": "655_R11",
            "path": "source-intake/mts_residuals/P8_Y5_R10_655_R11_RETAINED_OPERATOR_VECTOR_STATUS.csv",
            "role": "retained non-EH operator vector families",
            "needle": "source_normalization_operator",
        },
        {
            "source_id": "767_bridge",
            "path": "source-intake/mts_residuals/P8_Y5_R10_767_LOCAL_GR_BRIDGE.csv",
            "role": "WEP closure/source/Newton bridge",
            "needle": "LGB767_2_Newton_source",
        },
    ]
    rows: list[dict[str, str]] = []
    for spec in specs:
        path = source_path(spec["path"])
        text = read_text(path)
        rows.append(
            {
                "source_id": spec["source_id"],
                "role": spec["role"],
                "path": spec["path"],
                "exists": flag(path.exists()),
                "needle_found": flag(spec["needle"] in text),
                "needle": spec["needle"],
                "valid_for_claim": "false",
            }
        )
    return rows


def parent_action_contract_rows() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PAC990_0_parent_fields_and_quotient",
            "contract_clause": "parent configuration Phi with quotient/readout q producing one observed geometry",
            "minimal_form": "q(Phi) -> (M,g_obs,e_hat,tau_obs) with all local observables read in the same branch",
            "would_buy": "common arena for WEP, clocks, Newtonian source, PPN, and EM readout",
            "current_status": "closure_visible_not_parent_signed",
            "blocks_if_missing": "frame/domain switches can fake passes",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAC990_1_gravity_operator",
            "contract_clause": "local exterior gravitational operator is EH-only or retained R11 vector is executable",
            "minimal_form": "S_g=(16*pi*G_ref)^-1 int sqrt(-g) R + boundary, OR explicit R11 operator coefficients with weak-field maps",
            "would_buy": "field equations that can be weak-field expanded rather than asserted",
            "current_status": "EH_unsigned_R11_template_only",
            "blocks_if_missing": "no honest local GR/Newton/PPN claim",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAC990_2_matter_functor",
            "contract_clause": "all matter descends through one species-blind observed matter functor",
            "minimal_form": "S_matter=sum_A S_A[Psi_A,e_hat,omega[e_hat],theta_A], with Lie_v theta_A=0",
            "would_buy": "WEP/no-alpha/no-mass vertices can become theorem-zero instead of closure",
            "current_status": "explicit_closure_not_theorem",
            "blocks_if_missing": "composition channels and clock constants remain active debts",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAC990_3_EM_lock",
            "contract_clause": "EM charge generator, Maxwell kinetic term, current normalization, and readout descend from one parent owner",
            "minimal_form": "T_Q fixed; F_Q^2 unique; S_int=sum_A n_A int A_Q J_A; Lie_v ln alpha_EM=0",
            "would_buy": "b_theta_alpha_EM=0 and alpha/Coulomb WEP-clock channel closes structurally",
            "current_status": "not_signed_unique_F2_counterexample_active",
            "blocks_if_missing": "finite alpha branch needs beta_source_alpha owner and clock/WEP maps",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAC990_4_source_charge",
            "contract_clause": "observed source mass is an integrable fixed-reference Hamiltonian charge",
            "minimal_form": "delta H_tau = int_S(delta Q_tau - i_tau theta), with delta^2H_tau=0, fixed B_ref, tau lock, and source equality",
            "would_buy": "Newtonian GM/source normalization before orbital, PPN, R10, or Gdot scoring",
            "current_status": "selected_live_edge_FB554_0",
            "blocks_if_missing": "EH-looking equations still lack measured Newtonian source",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAC990_5_Ward_Bianchi",
            "contract_clause": "all hidden/projector/domain/boundary variables are varied, on shell, topological, or retained as residual operators",
            "minimal_form": "nabla_mu T_total^{mu nu}=0 including selectors/boundaries, with no silent Euler leaks",
            "would_buy": "conservation compatibility for GR/Newton reduction and no preferred-frame/source hair",
            "current_status": "open",
            "blocks_if_missing": "Bianchi/conservation problem or retained R11 residual vector",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PAC990_6_PPN_readout",
            "contract_clause": "weak-field solution of the selected operator plus selected source charge reaches GR PPN values",
            "minimal_form": "gamma=beta=1, alpha_i=xi=0, no Gdot, no finite-range residue in observed frame",
            "would_buy": "actual local-GR/Newton empirical gate",
            "current_status": "not_ready",
            "blocks_if_missing": "no local-GR claim even if upstream clauses improve",
            "valid_for_claim": "false",
        },
    ]


def reentry_ladder_rows() -> list[dict[str, str]]:
    return [
        {
            "rung_id": "LAD990_0_visibility",
            "rung": "keep closures visible",
            "requirement": "WEP/matter-frame and alpha closures remain labelled, not silently promoted",
            "current_state": "satisfied_as_guard_only",
            "next_unlock": "parent-sign PAC990_2 and PAC990_3 or keep closure labels",
            "claim_status": "guard_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LAD990_1_operator",
            "rung": "select gravitational operator",
            "requirement": "EH-only theorem or executable R11 vector",
            "current_state": "blocked",
            "next_unlock": "derive metric-only second-order LC branch or fill R11 coefficients/maps",
            "claim_status": "blocked_nonclaim",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LAD990_2_source_mass",
            "rung": "derive observed source mass",
            "requirement": "integrable fixed-reference Hamiltonian Pi_M charge",
            "current_state": "best_live_edge",
            "next_unlock": "attack FB554_0: nonintegrability, reference drift, symplectic/boundary flux",
            "claim_status": "selected_next_derivation",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LAD990_3_Newton",
            "rung": "Newtonian limit",
            "requirement": "Poisson/inverse-square law with stable measured GM from the same source charge",
            "current_state": "not_reached",
            "next_unlock": "source equality plus weak-field operator solution",
            "claim_status": "not_ready",
            "valid_for_claim": "false",
        },
        {
            "rung_id": "LAD990_4_PPN",
            "rung": "PPN/local residual vector",
            "requirement": "gamma/beta/preferred-frame/Gdot/R10 finite-range predictions are zero or bounded",
            "current_state": "not_ready",
            "next_unlock": "operator+source weak-field map",
            "claim_status": "not_ready",
            "valid_for_claim": "false",
        },
    ]


def dependency_matrix_rows() -> list[dict[str, str]]:
    return [
        {
            "dependency_id": "DEP990_0_EM_not_GR",
            "if_clause": "PAC990_3_EM_lock succeeds",
            "then_effect": "alpha/Coulomb WEP-clock channel can close",
            "still_needed": "PAC990_1 operator, PAC990_4 source charge, PAC990_6 PPN",
            "warning": "EM silence does not prove EH/Newton",
            "valid_for_claim": "false",
        },
        {
            "dependency_id": "DEP990_1_EH_not_Newton",
            "if_clause": "PAC990_1 EH-looking equations succeed",
            "then_effect": "candidate local operator resembles GR",
            "still_needed": "PAC990_4 source normalization and PAC990_6 PPN readout",
            "warning": "metric equation without measured source mass is not Newton recovery",
            "valid_for_claim": "false",
        },
        {
            "dependency_id": "DEP990_2_WEP_not_source",
            "if_clause": "PAC990_2 one matter frame is used as closure",
            "then_effect": "private branch can be organized consistently",
            "still_needed": "parent matter functor theorem or explicit source/clock residual rows",
            "warning": "WEP closure cannot pay source-normalization or EH debt",
            "valid_for_claim": "false",
        },
        {
            "dependency_id": "DEP990_3_HPiM_first",
            "if_clause": "PAC990_4 Hamiltonian PiM charge is integrable and reference-fixed",
            "then_effect": "source-mass operator becomes meaningful",
            "still_needed": "source equality, Gauss/Newton readout, PPN vector",
            "warning": "this is the best next derivation target, not a pass",
            "valid_for_claim": "false",
        },
    ]


def failure_mode_rows() -> list[dict[str, str]]:
    return [
        {
            "failure_id": "FAIL990_0_smuggled_WEP",
            "failure_mode": "use one-frame matter closure as if parent-derived",
            "blocked_by": "PAC990_2/LAD990_0 labels",
            "required_fix": "parent matter functor theorem or explicit retained residual rows",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "FAIL990_1_smuggled_EH",
            "failure_mode": "write EH prose while extra fields/R11/source terms remain legal",
            "blocked_by": "PAC990_1 and 655 P1-P9 audit",
            "required_fix": "EH-only ladder closure or executable R11 vector",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "FAIL990_2_hidden_source_mass",
            "failure_mode": "substitute orbital GM or reference choice for derived source charge",
            "blocked_by": "PAC990_4 Hamiltonian charge contract",
            "required_fix": "FB554_0 integrability/reference/boundary proof or source-backed bound",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "FAIL990_3_alpha_proxy_mix",
            "failure_mode": "mix 987 Coulomb proxy, 651 DD charge, and clock K_alpha as one normalization",
            "blocked_by": "989/988 normalization gates",
            "required_fix": "explicit conversion theorem or keep separate rows",
            "valid_for_claim": "false",
        },
        {
            "failure_id": "FAIL990_4_R11_template_promotion",
            "failure_mode": "treat R11 template rows as predictions",
            "blocked_by": "655/768 R11 scaffold-only gates",
            "required_fix": "real coefficients, units, source paths, weak-field maps, and bounds",
            "valid_for_claim": "false",
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CG990_0_parent_action_spine",
            "claim": "minimal parent action is derived",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "contract clauses are written but not parent-signed",
        },
        {
            "gate_id": "CG990_1_EH_Newton",
            "claim": "MTS reduces to GR/Newton locally",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "operator, source charge, and PPN readout remain open",
        },
        {
            "gate_id": "CG990_2_WEP_clock",
            "claim": "WEP/clock alpha channels are solved",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "EM-lock and matter functor remain unsigned; beta_source is unowned",
        },
        {
            "gate_id": "CG990_3_empirical_scoring",
            "claim": "local tests can be scored as evidence",
            "gate_pass": "false",
            "claim_allowed": "false",
            "why_not": "FB554_0/source/operator/PPN rows are not theorem-zero or numeric source-backed",
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC990_0_contract_value",
            "topic": "parent-action spine",
            "result": "minimal contract written as nonclaim",
            "reason": "it unifies EM-lock, matter functor, source normalization, and local GR reentry obligations",
            "next_action": "use as checklist, not as proof",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC990_1_best_derivation_target",
            "topic": "next derivation",
            "result": "Hamiltonian PiM FB554_0 remains the best live edge",
            "reason": "source mass must be integrable/reference-fixed before Newton, PPN, R10, or orbital claims",
            "next_action": "derive or source-fill FB554_0 components",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC990_2_next_checkpoint",
            "topic": "next checkpoint",
            "result": "991-Y5-R10-Hamiltonian-PiM-FB5540-integrability-reference-lock-or-source-closure.md",
            "reason": "this attacks the source-mass operator directly under the new parent-action contract",
            "next_action": "prove delta_H_tau integrability/reference/boundary terms zero, or stage numeric nonclaim rows",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, str]]:
    return [
        {
            "next_target": "991-Y5-R10-Hamiltonian-PiM-FB5540-integrability-reference-lock-or-source-closure.md",
            "objective": "derive or bound the FB554_0 Hamiltonian PiM integrability/reference/boundary obstruction that controls observed source mass",
            "include": "delta H_tau integrability, fixed B_ref, tau lock, symplectic/boundary flux, same-frame source equality, nonclaim validation",
            "exclude": "local-GR pass, Newton pass, PPN pass, substituting orbital GM, invented source-charge values, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    start_timestamp = SCRIPT_START_UTC.timestamp()
    for dirpath, _, filenames in os.walk(FORMALIZATION):
        for filename in filenames:
            path = Path(dirpath) / filename
            try:
                if path.stat().st_mtime > start_timestamp:
                    count += 1
            except OSError:
                count += 1
    return count


def validation_rows(
    sources: list[dict[str, str]],
    contract: list[dict[str, str]],
    ladder: list[dict[str, str]],
    dependencies: list[dict[str, str]],
    failures: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> list[dict[str, str]]:
    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    contract_ok = all(row["valid_for_claim"] == "false" for row in contract) and any(row["clause_id"] == "PAC990_4_source_charge" for row in contract)
    ladder_ok = any(row["rung_id"] == "LAD990_2_source_mass" and row["current_state"] == "best_live_edge" for row in ladder)
    dependency_ok = all(row["valid_for_claim"] == "false" for row in dependencies) and any(row["dependency_id"] == "DEP990_3_HPiM_first" for row in dependencies)
    failure_ok = all(row["valid_for_claim"] == "false" for row in failures) and any(row["failure_id"] == "FAIL990_2_hidden_source_mass" for row in failures)
    claims_ok = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claims)
    decision_ok = any(row["decision_id"] == "DEC990_2_next_checkpoint" and "991-Y5-R10" in row["result"] for row in decisions)
    next_ok = bool(next_target) and next_target[0]["valid_for_claim"] == "false"
    formalization_count = formalization_changed_after_start()
    checks = [
        {"check_id": "V990_0_sources", "result": "pass" if sources_ok else "fail", "detail": "all local source files exist and needles are found"},
        {"check_id": "V990_1_contract_nonclaim", "result": "pass" if contract_ok else "fail", "detail": "parent-action contract written with source-charge clause and no promotions"},
        {"check_id": "V990_2_ladder_selects_source_mass", "result": "pass" if ladder_ok else "fail", "detail": "Hamiltonian PiM source mass remains selected live edge"},
        {"check_id": "V990_3_dependencies_safe", "result": "pass" if dependency_ok else "fail", "detail": "dependency matrix blocks EM/EH/WEP shortcut claims"},
        {"check_id": "V990_4_failure_modes_safe", "result": "pass" if failure_ok else "fail", "detail": "hidden source-mass and related failure modes are guarded"},
        {"check_id": "V990_5_claim_gates_safe", "result": "pass" if claims_ok else "fail", "detail": "parent action, GR/Newton, WEP/clock, and empirical claims are blocked"},
        {"check_id": "V990_6_next_decision", "result": "pass" if decision_ok else "fail", "detail": "991 FB554_0 Hamiltonian PiM target selected"},
        {"check_id": "V990_7_next_target_written", "result": "pass" if next_ok else "fail", "detail": "next target row is present and nonclaim"},
        {"check_id": "V990_8_formalization_untouched", "result": "pass" if formalization_count == 0 else "fail", "detail": f"formalization-workbench modified-file count since script start is {formalization_count}"},
    ]
    ready = all(row["result"] == "pass" for row in checks)
    return [
        {**row, "generated_utc": stamp()}
        for row in checks
    ] + [
        {
            "check_id": "V990_READY",
            "result": "pass" if ready else "fail",
            "detail": "990 checkpoint pack validation summary",
            "generated_utc": stamp(),
        }
    ]


def write_doc(
    sources: list[dict[str, str]],
    contract: list[dict[str, str]],
    ladder: list[dict[str, str]],
    dependencies: list[dict[str, str]],
    failures: list[dict[str, str]],
    claims: list[dict[str, str]],
    decisions: list[dict[str, str]],
    validation: list[dict[str, str]],
    next_target: list[dict[str, str]],
) -> None:
    lines = [
        "# 990 Y5 R10: Minimal Parent-Action Coupling Contract, EM/Matter/GR Reentry",
        "",
        "Status: `Y5_R10_990_minimal_parent_action_coupling_contract_written_nonclaim_HPiM_source_mass_selected_next`",
        "",
        "Claim ceiling: no parent-action derivation, no WEP/clock pass, no EH/Newton/PPN/local-GR claim, no empirical scoring claim.",
        "",
        "## Readout",
        "",
        "990 consolidates the coupling work into the actual action-level contract. The project now has a sharper target: MTS needs a parent action that owns the observed geometry, matter functor, EM normalization, source charge, Ward/Bianchi accounting, and weak-field PPN readout.",
        "",
        "This does not prove GR/Newton. It prevents the common fake wins. EM-lock would solve the alpha/WEP-clock channel but not EH/Newton; EH-like equations would still not fix measured source mass; WEP closure is useful only if labelled. The best next derivation remains the Hamiltonian `Pi_M`/`FB554_0` source-mass obstruction.",
        "",
        "## Source Register",
        "",
        md_table(sources, ["source_id", "role", "exists", "needle_found", "path"]),
        "",
        "## Parent Action Contract",
        "",
        md_table(contract, ["clause_id", "contract_clause", "minimal_form", "would_buy", "current_status", "blocks_if_missing", "valid_for_claim"]),
        "",
        "## GR/Newton Reentry Ladder",
        "",
        md_table(ladder, ["rung_id", "rung", "requirement", "current_state", "next_unlock", "claim_status", "valid_for_claim"]),
        "",
        "## Dependency Matrix",
        "",
        md_table(dependencies, ["dependency_id", "if_clause", "then_effect", "still_needed", "warning", "valid_for_claim"]),
        "",
        "## Failure Mode Ledger",
        "",
        md_table(failures, ["failure_id", "failure_mode", "blocked_by", "required_fix", "valid_for_claim"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "gate_pass", "claim_allowed", "why_not"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "topic", "result", "reason", "next_action", "valid_for_claim"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["check_id", "result", "detail", "generated_utc"]),
        "",
        "## Next Target",
        "",
        md_table(next_target, ["next_target", "objective", "include", "exclude", "valid_for_claim"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    contract = parent_action_contract_rows()
    ladder = reentry_ladder_rows()
    dependencies = dependency_matrix_rows()
    failures = failure_mode_rows()
    claims = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()
    validation = validation_rows(sources, contract, ladder, dependencies, failures, claims, decisions, next_target)

    write_csv(OUT / "P8_Y5_R10_990_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv", contract)
    write_csv(OUT / "P8_Y5_R10_990_GR_NEWTON_REENTRY_LADDER.csv", ladder)
    write_csv(OUT / "P8_Y5_R10_990_DEPENDENCY_MATRIX.csv", dependencies)
    write_csv(OUT / "P8_Y5_R10_990_FAILURE_MODE_LEDGER.csv", failures)
    write_csv(OUT / "P8_Y5_R10_990_CLAIM_GATE.csv", claims)
    write_csv(OUT / "P8_Y5_R10_990_DECISION_LEDGER.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_990_NEXT_TARGET.csv", next_target)
    write_csv(OUT / "P8_Y5_BRR545_990_VALIDATION.csv", validation)
    write_doc(sources, contract, ladder, dependencies, failures, claims, decisions, validation, next_target)


if __name__ == "__main__":
    main()
