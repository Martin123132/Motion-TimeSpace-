from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_kappa_Gref_source_residual_lock_contract_written_no_parent_coefficient_or_Rsrc_zero_nonclaim"
CLAIM_CEILING = "coupling_source_normalization_contract_only_no_Delta_Poisson_fill_no_Gauss_orbit_no_Newton_no_PPN_no_R10_no_local_GR_claim"
NEXT_TARGET = "703-Y5-R10-parent-action-coupling-lock-or-Rsrc-channel-zero-theorem.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "702-Y5-R10-kappa-Gref-source-residual-coefficient-fill.md"
FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

OUTPUT_PATHS = [
    DOC_PATH,
    RESIDUALS / "P8_Y5_R10_702_SOURCE_REGISTER.csv",
    RESIDUALS / "P8_Y5_R10_702_KAPPA_GREF_LOCK_AUDIT.csv",
    RESIDUALS / "P8_Y5_R10_702_RSRC_CHANNEL_DECOMPOSITION.csv",
    RESIDUALS / "P8_Y5_R10_702_RHOH_FRAME_NORMALIZATION_PACK.csv",
    RESIDUALS / "P8_Y5_R10_702_DELTA_POISSON_CANDIDATE_FILL.csv",
    RESIDUALS / "P8_Y5_R10_702_EVALUATOR.csv",
    RESIDUALS / "P8_Y5_R10_702_CLAIM_GATE_EVALUATION.csv",
    RESIDUALS / "P8_Y5_R10_702_DECISION.csv",
    RESIDUALS / "P8_Y5_R10_702_NONCLAIM_SUMMARY.csv",
    RESIDUALS / "P8_Y5_BRR545_702_VALIDATION.csv",
]

SOURCE_PATHS = {
    "402_doc": ROOT / "402-EH-source-normalization-parent-pair.md",
    "424_doc": ROOT / "424-same-frame-EH-source-Poisson-reduction-gate.md",
    "425_doc": ROOT / "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
    "429_doc": ROOT / "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
    "523_doc": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "529_doc": ROOT / "529-Y5-source-calibrated-EH-family-proof-stack-or-R11-beta-fill.md",
    "531_doc": ROOT / "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md",
    "652_doc": ROOT / "652-Y5-R10-WEP-source-normalization-or-common-geometry-zero-theorem.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "696_doc": ROOT / "696-Y5-R10-MHref-same-frame-denominator-or-BTF-product-bound-guard.md",
    "700_doc": ROOT / "700-Y5-R10-EH-Poisson-coefficient-parent-premise-or-PG-residual-numeric-fill.md",
    "701_doc": ROOT / "701-Y5-R10-Delta-Poisson-source-coefficient-fill-or-Gauss-orbit-bridge.md",
    "701_validation": RESIDUALS / "P8_Y5_BRR545_701_VALIDATION.csv",
    "701_zero_audit": RESIDUALS / "P8_Y5_R10_701_DELTA_POISSON_ZERO_THEOREM_AUDIT.csv",
    "701_source_pack": RESIDUALS / "P8_Y5_R10_701_DELTA_POISSON_SOURCE_COEFFICIENT_PACK.csv",
    "701_bridge": RESIDUALS / "P8_Y5_R10_701_GAUSS_ORBIT_BRIDGE_GATE.csv",
    "700_delta_fill": RESIDUALS / "P8_Y5_R10_700_DELTA_POISSON_FILL_ROW.csv",
    "700_parent": RESIDUALS / "P8_Y5_R10_700_PARENT_PREMISE_AUDIT.csv",
    "pg_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
    "gauss_ppn_test": RESIDUALS / "P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv",
    "source_norm_scorecard": RESIDUALS / "P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
    "657_channels": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
    "696_denominator_audit": RESIDUALS / "P8_Y5_R10_696_MHREF_DENOMINATOR_AUDIT.csv",
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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


def validation_failures(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "missing", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate.is_file() and datetime.fromtimestamp(candidate.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    generated = now()
    roles = {
        "402_doc": "EH/source-normalization parent pair",
        "424_doc": "same-frame EH-source Poisson reduction gate",
        "425_doc": "EH retained ledger and test plan",
        "429_doc": "Ward/Bianchi exchange owner for source residual",
        "523_doc": "Gauss/orbital calibration and source-normalization residual scorecard",
        "529_doc": "source-calibrated EH proof stack",
        "531_doc": "Newton and beta residual envelope",
        "652_doc": "WEP/source-normalization zero-theorem attempt",
        "655_doc": "EH operator selection under WEP closure",
        "657_doc": "source-normalization family and R11 channel vector",
        "696_doc": "M_H_ref denominator blocker",
        "700_doc": "EH Poisson coefficient parent-premise audit",
        "701_doc": "Delta_Poisson conditional zero and coefficient pack",
        "701_validation": "701 validation gate",
        "701_zero_audit": "701 zero-theorem audit",
        "701_source_pack": "701 unfilled source-coefficient pack",
        "701_bridge": "701 Gauss/orbit bridge block",
        "700_delta_fill": "700 unfilled Delta_Poisson row",
        "700_parent": "700 parent premise audit",
        "pg_contract": "Hamiltonian charge to Poisson/Gauss calibration contract",
        "gauss_ppn_test": "Gauss and PPN readout test ledger",
        "source_norm_scorecard": "source-normalization residual scorecard",
        "657_channels": "eight source-normalization residual channels",
        "696_denominator_audit": "M_H_ref denominator audit",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": "true" if path.exists() else "false",
            "role": roles[source_id],
            "generated_utc": generated,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def kappa_gref_lock_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "KG702_0_reference_definition",
            "kappa_ref",
            "kappa_ref := 8*pi*G_ref/c^4",
            "independent universal G_ref selected before local orbit/Gauss scoring",
            "definition_only",
            "no claim; defines the comparison coefficient",
            source_list("402_doc", "424_doc", "701_source_pack"),
        ),
        (
            "KG702_1_parent_EH_lock",
            "kappa_eff_equals_kappa_ref",
            "epsilon_G := abs(kappa_eff/kappa_ref - 1)",
            "parent action fixes a constant observed-frame EH/source coefficient",
            "not_parent_signed",
            "Delta_G remains retained",
            source_list("402_doc", "424_doc", "700_parent", "701_zero_audit"),
        ),
        (
            "KG702_2_constancy",
            "constant coupling",
            "partial_t kappa_eff = partial_r kappa_eff = partial_lambda kappa_eff = 0",
            "global/local coupling superselection theorem or residual profile",
            "not_parent_derived",
            "time/range/domain drift can imitate local-G failure",
            source_list("429_doc", "523_doc", "source_norm_scorecard"),
        ),
        (
            "KG702_3_species_blind",
            "source-blind coupling",
            "partial_A kappa_eff = 0 for source composition/species label A",
            "WEP/source-charge theorem or eta_source_AB bound",
            "not_parent_derived",
            "WEP/source-normalization residual remains retained",
            source_list("652_doc", "657_doc", "source_norm_scorecard"),
        ),
        (
            "KG702_4_frame_blind",
            "same-frame coupling",
            "kappa_eff[source frame] = kappa_eff[metric/orbit/clock frame]",
            "same-frame descent certificate",
            "conditional_not_parent_derived",
            "frame mismatch can re-enter Delta_Poisson",
            source_list("424_doc", "429_doc", "700_parent"),
        ),
        (
            "KG702_5_value_or_bound",
            "numeric/theorem-zero epsilon_G",
            "epsilon_G <= epsilon_G_bound or epsilon_G = 0",
            "source path with coefficient value, theorem zero, or executable residual bound",
            "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "cannot fill Delta_Poisson",
            source_list("701_source_pack", "source_norm_scorecard"),
        ),
        (
            "KG702_6_verdict",
            "coupling lock",
            "G_ref = kappa_eff*c^4/(8*pi) with constant universal kappa_eff",
            "KG702_1 through KG702_5 satisfied",
            "fail_current_corpus",
            "no kappa/G_ref claim",
            source_list("701_doc", "701_source_pack"),
        ),
    ]
    return [
        {
            "lock_id": lock_id,
            "target": target,
            "mathematical_form": form,
            "required_evidence": evidence,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": paths,
            "generated_utc": generated,
        }
        for lock_id, target, form, evidence, status, effect, paths in rows
    ]


def rsrc_channel_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "RSRC702_0_total",
            "R_src",
            "R_src = div(E_nonEH)+T_obs grad(kappa_eff)+E_Z grad(Z)+F_projector+F_boundary+F_domain+F_nonmetric+R_rho",
            "zero theorem or dimensionful upper bound for every channel",
            "MISSING_SOURCE_RESIDUAL_BOUND",
            "Poisson_source_density_units",
            "false",
            source_list("429_doc", "657_doc", "657_channels", "source_norm_scorecard"),
        ),
        (
            "RSRC702_1_nonEH_divergence",
            "div(E_nonEH)",
            "local divergence of retained non-EH operator/source terms",
            "EH-only theorem or R11 coefficient vector",
            "R11_OPERATOR_VECTOR_UNFILLED",
            "Poisson_source_density_units",
            "false",
            source_list("425_doc", "655_doc", "657_channels"),
        ),
        (
            "RSRC702_2_kappa_gradient",
            "T_obs grad(kappa_eff)",
            "source force from coupling drift",
            "constant coupling theorem or derivative bound",
            "MISSING_KAPPA_DERIVATIVE_BOUND",
            "force_density_or_source_density_equivalent",
            "false",
            source_list("429_doc", "523_doc", "source_norm_scorecard"),
        ),
        (
            "RSRC702_3_auxiliary_Z",
            "E_Z grad(Z)",
            "auxiliary/off-shell exchange projected into local source",
            "auxiliary on-shell descent or local projection zero",
            "AUXILIARY_ONSHELL_NOT_PROVED",
            "Poisson_source_density_units",
            "false",
            source_list("429_doc", "657_doc"),
        ),
        (
            "RSRC702_4_projector_domain",
            "F_projector+F_domain",
            "commutator/domain force from local projection and Pi_M ownership",
            "projector/domain silence theorem or bound",
            "MISSING_PROJECTOR_DOMAIN_BOUND",
            "Poisson_source_density_units",
            "false",
            source_list("429_doc", "523_doc", "657_channels"),
        ),
        (
            "RSRC702_5_boundary",
            "F_boundary",
            "boundary/counterterm contribution to the local source mass",
            "boundary no-hair/counterterm guard or integral bound",
            "MISSING_BOUNDARY_FLUX_BOUND",
            "Poisson_source_density_units",
            "false",
            source_list("523_doc", "696_doc", "696_denominator_audit"),
        ),
        (
            "RSRC702_6_nonmetric_exchange",
            "F_nonmetric",
            "matter exchange from nonmetric/coframe mismatch",
            "metric compatibility or nonmetric exchange bound",
            "NONMETRIC_EXCHANGE_NOT_PARENT_DERIVED",
            "Poisson_source_density_units",
            "false",
            source_list("424_doc", "429_doc", "700_parent"),
        ),
        (
            "RSRC702_7_density_normalization",
            "R_rho",
            "difference between rho_eff/rho_H and measured nonrelativistic Hilbert density",
            "rho_H normalization and compact-source stress silence",
            "MISSING_RHOH_NORMALIZATION",
            "Poisson_source_density_units",
            "false",
            source_list("529_doc", "652_doc", "701_source_pack"),
        ),
        (
            "RSRC702_8_verdict",
            "R_src zero/bound",
            "epsilon_src := abs(R_src)/(4*pi*G_ref*rho_H)",
            "all RSRC702_1 through RSRC702_7 theorem-zero or bounded",
            "fail_current_corpus",
            "epsilon_src remains unfilled",
            "false",
            source_list("429_doc", "701_zero_audit", "701_source_pack"),
        ),
    ]
    return [
        {
            "channel_id": channel_id,
            "channel": channel,
            "mathematical_form": form,
            "required_evidence": evidence,
            "current_status": status,
            "units": units,
            "valid_for_claim": valid,
            "source_paths": paths,
            "generated_utc": generated,
        }
        for channel_id, channel, form, evidence, status, units, valid, paths in rows
    ]


def rhoh_frame_pack_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("RF702_0_positive_density", "rho_H > 0 in the compact local source", "compact nonrelativistic Hilbert source theorem", "MISSING_RHOH_POSITIVITY_THEOREM", "blocks normalized residual denominator"),
        ("RF702_1_same_density", "rho_H equals the density in the 00 operator/source variation", "matter action Hilbert-source descent", "MISSING_SOURCE_DENSITY_DESCENT", "prevents coefficient readout"),
        ("RF702_2_pressure_stress_silence", "pressure/stress/internal currents do not alter the leading Poisson source", "post-Newtonian source expansion or stress bound", "MISSING_STRESS_SOURCE_BOUND", "keeps R_rho active"),
        ("RF702_3_same_frame", "source, metric, coframe, clock, and orbit frames are identified", "same-frame descent certificate", "MISSING_SAME_FRAME_CERTIFICATE", "keeps Delta_frame active"),
        ("RF702_4_counterterm_guard", "boundary counterterm convention does not subtract physical source mass", "boundary/counterterm guard", "MISSING_COUNTERTERM_GUARD", "keeps M_H_ref blocked"),
        ("RF702_5_MHref_link", "rho_H volume/source mass links to M_H_ref and measured GM without circularity", "independent M_H_ref normalization row", "MISSING_CERTIFIED_POSITIVE_M_H_REF", "blocks Gauss/orbit promotion"),
        ("RF702_6_verdict", "rho_H/frame normalization claim", "all RF702 rows above signed", "fail_current_corpus", "no source-normalized Newton claim"),
    ]
    return [
        {
            "pack_id": pack_id,
            "target": target,
            "required_evidence": evidence,
            "current_status": status,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("424_doc", "523_doc", "529_doc", "652_doc", "696_denominator_audit", "701_source_pack"),
            "generated_utc": generated,
        }
        for pack_id, target, evidence, status, effect in rows
    ]


def delta_candidate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        (
            "DPF702_0_symbolic_bound",
            "Delta_Poisson",
            "Delta_Poisson <= epsilon_G + epsilon_src + epsilon_rho + epsilon_frame + epsilon_operator + epsilon_boundary",
            "MISSING_NUMERIC_EPSILON_VECTOR",
            "formula_written_inputs_missing",
            "dimensionless",
            "MISSING_EPSILON_VECTOR_SOURCE_PATH",
            source_list("701_source_pack", "source_norm_scorecard"),
        ),
        (
            "DPF702_1_epsilon_G",
            "epsilon_G",
            "epsilon_G := abs(kappa_eff/kappa_ref - 1), kappa_ref=8*pi*G_ref/c^4",
            "MISSING_KAPPA_GREF_LOCK",
            "unfilled",
            "dimensionless",
            "MISSING_KAPPA_GREF_SOURCE_PATH",
            source_list("402_doc", "424_doc", "701_zero_audit"),
        ),
        (
            "DPF702_2_epsilon_src",
            "epsilon_src",
            "epsilon_src := abs(R_src)/(4*pi*G_ref*rho_H)",
            "MISSING_RSRC_BOUND",
            "unfilled",
            "dimensionless",
            "MISSING_RSRC_SOURCE_PATH",
            source_list("429_doc", "657_channels", "source_norm_scorecard"),
        ),
        (
            "DPF702_3_epsilon_rho_frame",
            "epsilon_rho_plus_frame",
            "density/frame mismatch contribution retained separately from R_src if the Hilbert source is not same-frame normalized",
            "MISSING_RHOH_AND_FRAME_LOCK",
            "unfilled",
            "dimensionless",
            "MISSING_RHOH_FRAME_SOURCE_PATH",
            source_list("424_doc", "523_doc", "652_doc"),
        ),
        (
            "DPF702_4_conditional_zero",
            "conditional theorem",
            "if epsilon_G=epsilon_src=epsilon_rho=epsilon_frame=epsilon_operator=epsilon_boundary=0 then Delta_Poisson=0",
            "CONDITIONAL_THEOREM_ONLY",
            "not_parent_signed",
            "dimensionless",
            "MISSING_PARENT_ZERO_PROOF_PATH",
            source_list("701_zero_audit", "701_source_pack"),
        ),
        (
            "DPF702_5_first_fill_row",
            "claim-ready Delta_Poisson fill",
            "numeric/theorem-zero value for DP700_0_first_Delta_Poisson_fill",
            "MISSING_VALUE_OR_THEOREM_ZERO",
            "still_unfilled_after_702",
            "dimensionless",
            "MISSING_CLAIM_READY_SOURCE_PATH",
            source_list("700_delta_fill", "701_source_pack"),
        ),
    ]
    return [
        {
            "fill_id": fill_id,
            "target": target,
            "formula": formula,
            "value_or_bound": value_or_bound,
            "current_status": status,
            "units": units,
            "source_path": source_path,
            "valid_for_claim": "false",
            "source_paths": paths,
            "generated_utc": generated,
        }
        for fill_id, target, formula, value_or_bound, status, units, source_path, paths in rows
    ]


def evaluator_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("EVAL702_0_kappa_fill", "Can kappa_eff/G_ref be filled now?", "No. The identity is algebraically clear, but no parent coefficient or independent G_ref lock is sourced.", "fail_blocked", NEXT_TARGET),
        ("EVAL702_1_source_residual_fill", "Can R_src be set to zero now?", "No. Ward/Bianchi gives ownership, not silence; every projected channel still needs theorem-zero or a bound.", "fail_blocked", NEXT_TARGET),
        ("EVAL702_2_rhoH_frame", "Can rho_H/frame normalization be accepted as standard?", "Only as a conditional GR-limit assumption, not as a parent-derived MTS result.", "fail_blocked", NEXT_TARGET),
        ("EVAL702_3_best_route", "What is the best next strike?", "Try a parent-action coupling lock first; if that fails, attack R_src channel-zero rows one by one.", "route_selected", NEXT_TARGET),
    ]
    return [
        {
            "eval_id": eval_id,
            "question": question,
            "answer": answer,
            "result": result,
            "next_action": next_action,
            "valid_for_claim": "false",
            "source_paths": source_list("701_doc", "701_source_pack", "429_doc", "523_doc"),
            "generated_utc": generated,
        }
        for eval_id, question, answer, result, next_action in rows
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("CG702_0_sources", "all source files load", "source register exists check", "pass_structure", "allows checkpoint only"),
        ("CG702_1_prior_701", "701 validation clean", "701 validation has no failures", "pass_structure", "inherits clean predecessor"),
        ("CG702_2_kappa_lock", "kappa_eff/G_ref lock", "MISSING_NUMERIC_OR_THEOREM_ZERO", "fail_blocked", "no coupling claim"),
        ("CG702_3_Rsrc", "source residual zero/bound", "MISSING_SOURCE_RESIDUAL_BOUND", "fail_blocked", "no Delta_Poisson fill"),
        ("CG702_4_rhoH_frame", "rho_H and same-frame source normalization", "MISSING_RHOH_AND_FRAME_LOCK", "fail_blocked", "no measured-GM claim"),
        ("CG702_5_Gauss_orbit", "Gauss/orbit promotion", "Delta_Poisson and M_H_ref still missing", "fail_blocked", "no Newton/orbit claim"),
        ("CG702_6_local_GR", "PPN/R10/local-GR promotion", "not reached", "fail_blocked", "no PPN/R10/local-GR claim"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "observed_state": observed,
            "result": result,
            "claim_effect": effect,
            "valid_for_claim": "false",
            "source_paths": source_list("701_validation", "701_source_pack", "701_bridge", "696_denominator_audit"),
            "generated_utc": generated,
        }
        for gate_id, gate, observed, result, effect in rows
    ]


def decision_rows() -> list[dict[str, str]]:
    generated = now()
    rows = [
        ("D702_0_coupling_identity", "kappa_eff/G_ref identity", "definition_and_contract_written", "kappa_ref=8*pi*G_ref/c^4 isolates the coupling residual epsilon_G without proving it zero", NEXT_TARGET),
        ("D702_1_source_residual", "R_src decomposition", "channel_pack_written_unfilled", "Ward/Bianchi residual ownership is decomposed into local channels but no zero theorem lands yet", NEXT_TARGET),
        ("D702_2_delta_fill", "Delta_Poisson fill", "not_filled", "the candidate bound is symbolic because epsilon_G and epsilon_src are not numeric/theorem-zero", NEXT_TARGET),
        ("D702_3_next", "next target", "selected", "parent action coupling lock is the least-scrutiny route; source residual channel zeros are the fallback", NEXT_TARGET),
    ]
    return [
        {
            "decision_id": decision_id,
            "target": target,
            "result": result,
            "reason": reason,
            "next_action": next_action,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
        for decision_id, target, result, reason, next_action in rows
    ]


def summary_rows() -> list[dict[str, str]]:
    generated = now()
    return [
        {
            "summary_id": "S702_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "kappa_eff/G_ref and R_src are now split into an explicit coefficient lock plus a channelwise source-residual pack",
            "hardest_blocker": "no parent-signed constant universal coupling and no R_src channel-zero theorem or bound",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated,
        }
    ]


def has_missing_marker(row: dict[str, str]) -> bool:
    return "MISSING" in " ".join(str(value) for value in row.values())


def validation_rows(source_rows, kappa_rows, rsrc_rows, rhoh_rows, delta_rows, evaluator, gates, decisions, summary):
    generated = now()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = len(validation_failures("701_validation"))
    source_pack = read_csv(SOURCE_PATHS["701_source_pack"])
    source_pack_unfilled = any(has_missing_marker(row) for row in source_pack)
    kappa_verdict = [row for row in kappa_rows if row["lock_id"] == "KG702_6_verdict"][0]
    rsrc_verdict = [row for row in rsrc_rows if row["channel_id"] == "RSRC702_8_verdict"][0]
    rhoh_verdict = [row for row in rhoh_rows if row["pack_id"] == "RF702_6_verdict"][0]
    delta_still_unfilled = [row for row in delta_rows if row["fill_id"] == "DPF702_5_first_fill_row"][0]["value_or_bound"] == "MISSING_VALUE_OR_THEOREM_ZERO"
    no_claim = all(
        row.get("valid_for_claim") != "true"
        for group in [kappa_rows, rsrc_rows, rhoh_rows, delta_rows, evaluator, gates, decisions, summary]
        for row in group
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gates) and any(
        row["result"] == "fail_blocked" for row in gates
    )
    scoped = all(str(path).startswith(str(ROOT)) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_count()
    checks = [
        ("V702_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V702_1_prior_701_clean", prior_failures == 0, f"701_validation_failures={prior_failures}"),
        ("V702_2_701_source_pack_unfilled", source_pack_unfilled, "701 source pack still contains MISSING markers"),
        ("V702_3_kappa_lock_blocks", kappa_verdict["current_status"] == "fail_current_corpus", kappa_verdict["claim_effect"]),
        ("V702_4_Rsrc_channels_block", rsrc_verdict["current_status"] == "fail_current_corpus" and len(rsrc_rows) == 9, f"rsrc_rows={len(rsrc_rows)}"),
        ("V702_5_rhoH_frame_blocks", rhoh_verdict["current_status"] == "fail_current_corpus", rhoh_verdict["claim_effect"]),
        ("V702_6_delta_candidate_unfilled", delta_still_unfilled and any(has_missing_marker(row) for row in delta_rows), "Delta_Poisson fill remains nonclaim"),
        ("V702_7_gates_block_claim", gates_block, f"gate_rows={len(gates)}"),
        ("V702_8_no_claim_rows_promoted", no_claim, "all generated rows valid_for_claim=false"),
        ("V702_9_next_target_selected", summary[0]["next_target"] == NEXT_TARGET and decisions[-1]["next_action"] == NEXT_TARGET, NEXT_TARGET),
        ("V702_10_outputs_scoped", scoped, "all outputs under post-checkpoint-work"),
        ("V702_11_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V702_12_status_nonclaim", "no_Delta_Poisson_fill" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [{"check_id": cid, "result": "pass" if ok else "fail", "detail": detail, "generated_utc": generated} for cid, ok, detail in checks]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(source_rows, kappa_rows, rsrc_rows, rhoh_rows, delta_rows, evaluator, gates, decisions, summary, validation) -> None:
    doc = f"""# 702 - Y5 R10 Kappa Gref Source Residual Coefficient Fill

## Verdict

702 confirms the coupling suspicion. The cleanest honest decomposition is:

```text
kappa_ref := 8*pi*G_ref/c^4
epsilon_G := abs(kappa_eff/kappa_ref - 1)
epsilon_src := abs(R_src)/(4*pi*G_ref*rho_H)

Delta_Poisson <= epsilon_G
               + epsilon_src
               + epsilon_rho
               + epsilon_frame
               + epsilon_operator
               + epsilon_boundary
```

This is useful because it isolates the exact local-GR lock. MTS needs either a parent-action theorem that fixes constant universal `kappa_eff = kappa_ref`, or a real sourced residual bound for `epsilon_G`. Separately, Ward/Bianchi ownership must be upgraded from "every force has an owner" to "every local source channel is zero or bounded."

No coupling, source-normalization, Newton, PPN, R10, Gauss/orbit, or local-GR claim is promoted.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Kappa Gref Lock Audit

{markdown_table(kappa_rows, ["lock_id", "target", "current_status", "claim_effect", "valid_for_claim"])}

## Rsrc Channel Decomposition

{markdown_table(rsrc_rows, ["channel_id", "channel", "current_status", "units", "valid_for_claim"])}

## RhoH Frame Normalization Pack

{markdown_table(rhoh_rows, ["pack_id", "target", "current_status", "claim_effect", "valid_for_claim"])}

## Delta Poisson Candidate Fill

{markdown_table(delta_rows, ["fill_id", "target", "value_or_bound", "current_status", "source_path", "valid_for_claim"])}

## Evaluator

{markdown_table(evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    kappa_rows = kappa_gref_lock_rows()
    rsrc_rows = rsrc_channel_rows()
    rhoh_rows = rhoh_frame_pack_rows()
    delta_rows = delta_candidate_rows()
    evaluator = evaluator_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    summary = summary_rows()
    validation = validation_rows(source_rows, kappa_rows, rsrc_rows, rhoh_rows, delta_rows, evaluator, gates, decisions, summary)

    write_csv(RESIDUALS / "P8_Y5_R10_702_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_702_KAPPA_GREF_LOCK_AUDIT.csv", kappa_rows, ["lock_id", "target", "mathematical_form", "required_evidence", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_702_RSRC_CHANNEL_DECOMPOSITION.csv", rsrc_rows, ["channel_id", "channel", "mathematical_form", "required_evidence", "current_status", "units", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_702_RHOH_FRAME_NORMALIZATION_PACK.csv", rhoh_rows, ["pack_id", "target", "required_evidence", "current_status", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_702_DELTA_POISSON_CANDIDATE_FILL.csv", delta_rows, ["fill_id", "target", "formula", "value_or_bound", "current_status", "units", "source_path", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_702_EVALUATOR.csv", evaluator, ["eval_id", "question", "answer", "result", "next_action", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_702_CLAIM_GATE_EVALUATION.csv", gates, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_702_DECISION.csv", decisions, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_702_NONCLAIM_SUMMARY.csv", summary, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_702_VALIDATION.csv", validation, ["check_id", "result", "detail", "generated_utc"])
    write_doc(source_rows, kappa_rows, rsrc_rows, rhoh_rows, delta_rows, evaluator, gates, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"kappa_rows={len(kappa_rows)}")
    print(f"rsrc_rows={len(rsrc_rows)}")
    print(f"delta_rows={len(delta_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
