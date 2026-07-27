from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_local_stationary_Killing_certificate_attempt_failed_epsilon_nonstationary_tau_residual_staged_nonclaim"
CLAIM_CEILING = "stationary_Killing_certificate_or_residual_row_only_no_MH_ref_no_Qbar_no_R10_no_PPN_no_orbital_no_local_GR_claim"
NEXT_TARGET = "687-Y5-R10-parent-domain-selector-to-stationary-generator-or-epsilon-tau-bound.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "686-Y5-R10-local-stationary-domain-Killing-certificate-or-tau-residual-row.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "455_doc": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
    "455_contract": RESIDUALS / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
    "457_doc": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
    "457_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
    "484_doc": ROOT / "484-parent-local-zero-action-clause-attempt.md",
    "602_doc": ROOT / "602-Y5-R10-bound-domain-selector-or-compact-shell-unit-map-fill.md",
    "602_validation": RESIDUALS / "P8_Y5_BRR545_602_VALIDATION.csv",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "655_validation": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
    "655_eh_audit": RESIDUALS / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
    "655_decision": RESIDUALS / "P8_Y5_R10_655_EH_OR_R11_DECISION_GATES.csv",
    "684_doc": ROOT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
    "684_validation": RESIDUALS / "P8_Y5_BRR545_684_VALIDATION.csv",
    "684_frame_contract": RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
    "684_tau_audit": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
    "685_doc": ROOT / "685-Y5-R10-tau-generator-Killing-clock-lock-or-frame-residual-fill.md",
    "685_validation": RESIDUALS / "P8_Y5_BRR545_685_VALIDATION.csv",
    "685_tau_contract": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
    "685_killing_gate": RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
    "685_residual_template": RESIDUALS / "P8_Y5_R10_685_TAU_FRAME_RESIDUAL_TEMPLATE.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "455_doc": "Ward/Killing mass-current route",
        "455_contract": "FC1 stationary or Hamiltonian time-generator contract",
        "457_doc": "Hamiltonian boundary charge route",
        "457_contract": "HC1 observed time-generator contract",
        "484_doc": "conditional local-zero theorem using stationary Killing/comoving branch",
        "602_doc": "conditional bound-domain selector and local stationary branch blocker",
        "602_validation": "602 validation gate",
        "655_doc": "EH-only exterior selection blocker",
        "655_validation": "655 validation gate",
        "655_eh_audit": "EH-only premise audit",
        "655_decision": "EH-or-R11 decision gates",
        "684_doc": "observed tau/coframe lock predecessor",
        "684_validation": "684 validation gate",
        "684_frame_contract": "one-frame/tau contract rows",
        "684_tau_audit": "tau role audit rows",
        "685_doc": "tau generator/Killing-clock predecessor",
        "685_validation": "685 validation gate",
        "685_tau_contract": "tau generator contract rows",
        "685_killing_gate": "Killing/clock blocker gates",
        "685_residual_template": "tau/frame residual templates",
        "boundary_reference_status": "M_H_ref claim-valid status",
    }
    return [
        {
            "source_id": source_id,
            "path": str(source_path),
            "exists": bool_text(source_path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, source_path in SOURCE_PATHS.items()
    ]


def stationary_certificate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "clause_id": "LSC686_0_domain",
            "certificate_clause": "parent-selected compact local stationary domain",
            "required_identity": "D_loc and its boundary are selected by parent equations, not by a fitted arena label",
            "mathematical_form": "delta_{chi_D,D} S_parent=0 => D_loc with admissible boundary and no empirical window",
            "current_status": "conditional_not_parent_derived",
            "blocker": "602 keeps N_D, P_MTS,D, local trivial class, and normalization unowned",
            "if_closed": "tau can be attached to a real local branch rather than a chosen box",
            "valid_for_claim": "false",
            "source_paths": source_list("602_doc", "484_doc"),
            "generated_utc": now,
        },
        {
            "clause_id": "LSC686_1_stationary_solution",
            "certificate_clause": "observed stationary exterior solution",
            "required_identity": "there exists a timelike tau_obs with L_tau g_obs=0 through the tested local exterior",
            "mathematical_form": "L_tau g_obs_{mu nu}=2 nabla_{(mu} tau_{nu)}=0",
            "current_status": "missing_local_stationary_Killing_certificate",
            "blocker": "no parent theorem selects the local solution as stationary rather than approximately bound",
            "if_closed": "Hilbert stress conservation can be projected into a conserved mass current",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "685_killing_gate", "684_tau_audit"),
            "generated_utc": now,
        },
        {
            "clause_id": "LSC686_2_same_tau",
            "certificate_clause": "same tau for source, charge, clock, orbit, and boundary",
            "required_identity": "tau_source=tau_charge=tau_clock=tau_orbit=tau_boundary=tau_obs",
            "mathematical_form": "J_H[tau_obs], H_tau_obs, clock proper time, orbital readout, and H_ref share one normalized generator",
            "current_status": "blocked_by_685",
            "blocker": "685 shows the tau roles are still conditional or separately normalized",
            "if_closed": "M_H_ref becomes less gauge/convention sensitive",
            "valid_for_claim": "false",
            "source_paths": source_list("684_frame_contract", "685_tau_contract"),
            "generated_utc": now,
        },
        {
            "clause_id": "LSC686_3_EH_or_exterior_operator",
            "certificate_clause": "EH-only or executable exterior operator",
            "required_identity": "exterior field equations reduce to EH metric-only stationary branch, or every non-EH operator is retained numerically",
            "mathematical_form": "S_ext -> S_EH[g_obs]+B or c_R11 vector supplied with weak-field maps",
            "current_status": "fail_current_claim",
            "blocker": "655 keeps EH-only unsigned and R11 vector template-only",
            "if_closed": "stationary local geometry could inherit the GR-like Killing/Hamiltonian machinery",
            "valid_for_claim": "false",
            "source_paths": source_list("655_doc", "655_eh_audit", "655_decision"),
            "generated_utc": now,
        },
        {
            "clause_id": "LSC686_4_Hilbert_stress_conservation",
            "certificate_clause": "same-frame Hilbert stress is separately conserved",
            "required_identity": "nabla_mu T_H^{mu nu}=0 in the same observed frame after hidden sectors are varied or retained",
            "mathematical_form": "nabla_mu T_H^{mu nu}=0; no extra exchange current in the mass channel",
            "current_status": "conditional_not_parent_derived",
            "blocker": "Ward conservation is total; mass-channel/projector/domain/boundary exchange silence is not theorem-zero",
            "if_closed": "Killing current divergence reduces to T_H symgrad(tau)",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "457_contract"),
            "generated_utc": now,
        },
        {
            "clause_id": "LSC686_5_boundary_reference",
            "certificate_clause": "stationary boundary and reference subtraction are fixed",
            "required_identity": "boundary class, H_ref, and tau normalization are parent-fixed and source-independent",
            "mathematical_form": "partial_{source,r,t,frame,lambda} Delta_ref=0 and delta H_tau integrable",
            "current_status": "blocked_open",
            "blocker": "boundary/reference status has no claim-ready M_H_ref row",
            "if_closed": "nonstationary tau leakage can be normalized by a stable denominator",
            "valid_for_claim": "false",
            "source_paths": source_list("457_contract", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "clause_id": "LSC686_6_no_exchange_leak",
            "certificate_clause": "hidden, projector, boundary, coupling, and domain fluxes are silent",
            "required_identity": "Pi_M(F_X+F_P+F_B+F_D+F_nm+T d kappa)=0 in the local mass channel",
            "mathematical_form": "d(Pi_M J_H)=0 without retained mu_extra, dM_eff, Gdot, source/range, or R11 leakage",
            "current_status": "not_parent_derived",
            "blocker": "455/655 keep residual channels active",
            "if_closed": "local mass charge becomes a closed current rather than closure-only",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "655_eh_audit"),
            "generated_utc": now,
        },
        {
            "clause_id": "LSC686_7_verdict",
            "certificate_clause": "local stationary/Killing certificate",
            "required_identity": "all preceding clauses close with no MISSING, conditional-only, or template-only status",
            "mathematical_form": "certificate=true => epsilon_nonstationary_tau=0 theorem-zero",
            "current_status": "certificate_failed_nonclaim",
            "blocker": "domain, stationarity, tau lock, EH/R11, stress, boundary, and exchange clauses remain unsigned",
            "if_closed": "move back to M_H_ref denominator and Qbar promotion gates",
            "valid_for_claim": "false",
            "source_paths": source_list("602_doc", "655_doc", "684_doc", "685_doc"),
            "generated_utc": now,
        },
    ]


def killing_identity_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "identity_id": "KIA686_0_exact_identity",
            "claim": "stress-current divergence identity",
            "derivation": "For j_tau^mu=T_H^{mu nu} tau_nu, nabla_mu j_tau^mu=(nabla_mu T_H^{mu nu})tau_nu+T_H^{mu nu}nabla_mu tau_nu.",
            "current_result": "formal_identity",
            "claim_effect": "shows exactly what must vanish; does not itself prove local stationarity",
            "valid_for_claim": "false",
            "source_paths": source_list("455_doc", "455_contract"),
            "generated_utc": now,
        },
        {
            "identity_id": "KIA686_1_Killing_zero",
            "claim": "Killing plus same-frame Hilbert conservation makes the tau current closed",
            "derivation": "If nabla_mu T_H^{mu nu}=0 and nabla_{(mu}tau_{nu)}=0, then T_H^{mu nu}nabla_mu tau_nu=T_H^{mu nu}nabla_{(mu}tau_{nu)}=0.",
            "current_result": "conditional_theorem",
            "claim_effect": "would close the Ward/Killing route if tau_obs and T_H were parent-owned",
            "valid_for_claim": "false",
            "source_paths": source_list("455_contract", "685_tau_contract"),
            "generated_utc": now,
        },
        {
            "identity_id": "KIA686_2_current_MTS_gap",
            "claim": "current MTS does not yet supply both premises",
            "derivation": "685 blocks tau_obs; 655 blocks EH-only/local operator silence; 602 blocks parent-selected local domain; 455 blocks exchange/projector silence.",
            "current_result": "proof_attempt_fails",
            "claim_effect": "epsilon_nonstationary_tau must remain an active residual, not theorem-zero",
            "valid_for_claim": "false",
            "source_paths": source_list("602_doc", "655_doc", "685_killing_gate", "455_contract"),
            "generated_utc": now,
        },
        {
            "identity_id": "KIA686_3_residual_definition",
            "claim": "nonstationary tau residual is the honest fallback",
            "derivation": "epsilon_nonstationary_tau := |integral_V T_H^{mu nu}nabla_{(mu}tau_{nu)} dV_tau| / M_ref_candidate, with M_ref_candidate not claim-ready until M_H_ref closes.",
            "current_result": "residual_row_staged",
            "claim_effect": "keeps the local branch testable without smuggling a plateau/stationarity axiom",
            "valid_for_claim": "false",
            "source_paths": source_list("685_residual_template", "boundary_reference_status"),
            "generated_utc": now,
        },
    ]


def nonstationary_residual_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "residual_id": "NTR686_0_epsilon_nonstationary_tau",
            "residual_quantity": "epsilon_nonstationary_tau",
            "definition": "dimensionless mass-current leakage from non-Killing observed tau: abs(int_V T_H^{mu nu} nabla_(mu tau_nu) dV_tau)/M_ref_candidate",
            "required_columns": "system_id;domain_id;tau_definition;sym_grad_tau_source;stress_source;volume_or_surface_rule;M_ref_candidate;epsilon_nonstationary_tau;units;source_file;assumptions;valid_for_claim",
            "current_status": "MISSING_STATIONARY_KILLING_CERTIFICATE_OR_SOURCE_BACKED_BOUND",
            "units": "dimensionless after numerator and M_ref_candidate are in the same energy/mass units",
            "affected_claims": "M_H_ref;Qbar;R10;PPN;orbital;local_GR",
            "valid_for_claim": "false",
            "source_paths": source_list("685_residual_template", "455_contract", "457_contract"),
            "generated_utc": now,
        },
        {
            "residual_id": "NTR686_1_tau_domain_selector_mismatch",
            "residual_quantity": "delta_tau_domain_selector",
            "definition": "mismatch between the tau used to define stationarity and the parent/domain selector that chooses the local compact branch",
            "required_columns": "system_id;domain_selector_source;tau_source;delta_tau_domain_selector;units;source_file;valid_for_claim",
            "current_status": "MISSING_PARENT_DOMAIN_SELECTOR_TO_TAU_MAP",
            "units": "dimensionless fractional mismatch",
            "affected_claims": "local_stationary_certificate;M_H_ref;local_GR",
            "valid_for_claim": "false",
            "source_paths": source_list("602_doc", "684_tau_audit", "685_tau_contract"),
            "generated_utc": now,
        },
        {
            "residual_id": "NTR686_2_stationary_boundary_reference_shift",
            "residual_quantity": "Delta_ref_stationary_tau_over_Mref",
            "definition": "reference/boundary energy shift produced by choosing a stationary tau not parent-locked to clocks and sources",
            "required_columns": "system_id;boundary_class;H_ref_tau_shift;M_ref_candidate;Delta_ref_stationary_tau_over_Mref;units;source_file;valid_for_claim",
            "current_status": "MISSING_FIXED_REFERENCE_TAU_BOUNDARY_CLASS",
            "units": "dimensionless",
            "affected_claims": "M_H_ref;R10;PPN;orbital",
            "valid_for_claim": "false",
            "source_paths": source_list("457_contract", "boundary_reference_status", "685_residual_template"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG686_0_stationary_certificate",
            "gate": "local stationary/Killing certificate",
            "required_state": "all LSC686 clauses parent-derived",
            "observed_state": "domain, tau, EH/R11, stress, boundary, and exchange clauses fail or remain conditional",
            "result": "fail_blocked",
            "claim_effect": "epsilon_nonstationary_tau remains active",
            "valid_for_claim": "false",
            "source_paths": source_list("685_killing_gate", "655_eh_audit", "602_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG686_1_MH_ref",
            "gate": "M_H_ref denominator",
            "required_state": "integrable H_tau_obs and fixed reference with same tau",
            "observed_state": "tau and boundary/reference locks remain unsigned",
            "result": "fail_blocked",
            "claim_effect": "no Qbar/R10 denominator promotion",
            "valid_for_claim": "false",
            "source_paths": source_list("684_doc", "685_doc", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG686_2_local_GR",
            "gate": "local-GR/PPN promotion",
            "required_state": "EH/R11, source-normalization, tau, and residual gates all closed",
            "observed_state": "655 EH-only fails; 685 tau lock fails; 686 stationarity fails",
            "result": "fail_policy",
            "claim_effect": "no local-GR, PPN, orbital, or R10 claim",
            "valid_for_claim": "false",
            "source_paths": source_list("655_decision", "685_validation"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG686_3_next_work",
            "gate": "next target selection",
            "required_state": "pick derivation-first target or source-bound fallback",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "try parent domain-selector-to-tau map before numeric epsilon bound",
            "valid_for_claim": "false",
            "source_paths": source_list("602_doc", "685_residual_template"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D686_0_proof_attempt",
            "target": "local stationary/Killing certificate",
            "result": "failed_for_claim",
            "reason": "the Killing identity is clean, but the parent does not yet select the stationary observed tau/domain/exterior package",
            "next_action": "do not mark epsilon_nonstationary_tau theorem-zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D686_1_residual_row",
            "target": "epsilon_nonstationary_tau",
            "result": "staged",
            "reason": "the exact missing object is now measurable/form-fillable as T_H symgrad(tau) over a same-frame denominator",
            "next_action": "derive parent selector-to-tau map or source a bound with units and M_ref candidate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D686_2_next",
            "target": "domain selector to stationary generator",
            "result": "selected",
            "reason": "this is less circular than inserting local stationarity and less premature than scoring a placeholder residual",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S686_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "Killing-current proof route is exact but conditional; local stationary/Killing certificate is not parent-signed; epsilon_nonstationary_tau residual rows are staged.",
            "hardest_blocker": "parent-selected local stationary tau/domain/exterior package",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def all_valid_for_claim_false(rows_by_name: dict[str, list[dict[str, str]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, str]],
    certificate_rows: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "certificate": certificate_rows,
        "identity": identity_rows,
        "residual": residual_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["602_validation", "655_validation", "684_validation", "685_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    certificate_blocks_claim = all(row["valid_for_claim"] == "false" for row in certificate_rows) and any(
        "fail" in row["current_status"] or "missing" in row["current_status"].lower() or "blocked" in row["current_status"].lower()
        for row in certificate_rows
    )
    residuals_staged = all(row["valid_for_claim"] == "false" for row in residual_rows) and all(
        "MISSING_" in row["current_status"] for row in residual_rows
    )
    identity_has_residual = any(row["identity_id"] == "KIA686_3_residual_definition" for row in identity_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(
        row["result"].startswith("fail") for row in gate_rows
    )
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_)
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_686_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_686_LOCAL_STATIONARY_CERTIFICATE.csv",
        RESIDUALS / "P8_Y5_R10_686_KILLING_IDENTITY_ATTEMPT.csv",
        RESIDUALS / "P8_Y5_R10_686_NONSTATIONARY_TAU_RESIDUAL_ROW.csv",
        RESIDUALS / "P8_Y5_R10_686_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_686_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_686_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_686_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)

    checks = [
        (
            "V686_0_source_paths_exist",
            not missing_sources,
            "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources),
        ),
        (
            "V686_1_prior_validations_clean",
            all(count == 0 for count in prior_failure_counts.values()),
            ";".join(f"{key}={value}" for key, value in prior_failure_counts.items()),
        ),
        (
            "V686_2_certificate_rows_complete",
            len(certificate_rows) == 8,
            f"certificate_rows={len(certificate_rows)}",
        ),
        (
            "V686_3_certificate_fails_cleanly",
            certificate_blocks_claim,
            "certificate blocks claim and keeps explicit blockers visible",
        ),
        (
            "V686_4_Killing_identity_not_overclaimed",
            identity_has_residual and all(row["valid_for_claim"] == "false" for row in identity_rows),
            "identity proves conditional route only and emits residual fallback",
        ),
        (
            "V686_5_nonstationary_residual_staged",
            residuals_staged,
            f"residual_rows={len(residual_rows)}",
        ),
        (
            "V686_6_claim_gates_block",
            gates_block,
            "claim gates keep M_H_ref/Qbar/R10/PPN/orbital/local_GR blocked",
        ),
        (
            "V686_7_no_claim_rows_promoted",
            no_claim_rows,
            "all generated 686 rows remain valid_for_claim=false",
        ),
        (
            "V686_8_next_target_selected",
            next_selected,
            NEXT_TARGET,
        ),
        (
            "V686_9_generated_outputs_scoped",
            scoped_outputs,
            "all 686 outputs target post-checkpoint-work",
        ),
        (
            "V686_10_formalization_workbench_untouched",
            formalization_count == 0,
            f"formalization_changed_after_cutoff={formalization_count}",
        ),
        (
            "V686_11_status_nonclaim",
            "no_MH_ref" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING,
            CLAIM_CEILING,
        ),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(
    source_rows: list[dict[str, str]],
    certificate_rows: list[dict[str, str]],
    identity_rows: list[dict[str, str]],
    residual_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 686 - Y5 R10 Local Stationary Domain Killing Certificate Or Tau Residual Row

## Verdict

686 tried the clean GR-like move:

```text
j_tau^mu = T_H^{{mu nu}} tau_nu
nabla_mu j_tau^mu
  = (nabla_mu T_H^{{mu nu}}) tau_nu
  + T_H^{{mu nu}} nabla_(mu tau_nu)
```

If the parent theory gives same-frame Hilbert conservation and a parent-selected observed Killing/stationary generator, then the current is closed. That would be a serious route toward `M_H_ref`, measured mass conservation, and local-GR reduction.

But current MTS does not yet parent-sign the required package. The local domain selector is conditional, `tau_obs` is not one source/charge/clock/orbit/boundary generator, EH-only/R11 exterior selection is still open, and boundary/exchange silence remains unsigned.

So the theorem-zero route fails for claim. The honest fallback is now explicit: retain `epsilon_nonstationary_tau` and related tau/domain/reference mismatch rows until a parent selector-to-stationary-generator theorem or a real source-backed bound exists.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Local Stationary Certificate

{markdown_table(certificate_rows, ["clause_id", "certificate_clause", "required_identity", "current_status", "blocker", "if_closed", "valid_for_claim"])}

## Killing Identity Attempt

{markdown_table(identity_rows, ["identity_id", "claim", "current_result", "claim_effect", "valid_for_claim"])}

## Nonstationary Tau Residual Row

{markdown_table(residual_rows, ["residual_id", "residual_quantity", "current_status", "units", "affected_claims", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    certificate_rows = stationary_certificate_rows()
    identity_rows = killing_identity_rows()
    residual_rows = nonstationary_residual_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        certificate_rows,
        identity_rows,
        residual_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_686_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_686_LOCAL_STATIONARY_CERTIFICATE.csv", certificate_rows, ["clause_id", "certificate_clause", "required_identity", "mathematical_form", "current_status", "blocker", "if_closed", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_686_KILLING_IDENTITY_ATTEMPT.csv", identity_rows, ["identity_id", "claim", "derivation", "current_result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_686_NONSTATIONARY_TAU_RESIDUAL_ROW.csv", residual_rows, ["residual_id", "residual_quantity", "definition", "required_columns", "current_status", "units", "affected_claims", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_686_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_686_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_686_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_686_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(
        source_rows,
        certificate_rows,
        identity_rows,
        residual_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
        validation_rows_,
    )

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"certificate_rows={len(certificate_rows)}")
    print(f"identity_rows={len(identity_rows)}")
    print(f"residual_rows={len(residual_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
