from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
OUT = ROOT / "source-intake" / "mts_residuals"
SCRIPT_PATH = ROOT / "scripts" / "Y5_R10_alpha_normalization_owner_or_finite_coupling_bound_input_fill.py"
DOC_PATH = ROOT / "643-Y5-R10-alpha-normalization-owner-or-finite-coupling-bound-input-fill.md"

STATUS = "Y5_R10_alpha_owner_hunt_identifies_parent_vertical_norm_as_best_route_but_unproved_finite_inputs_still_missing"
CLAIM_CEILING = "alpha_normalization_owner_hunt_and_finite_input_contract_only_no_kappa_alpha_zero_no_numeric_alpha_score_no_local_claim"
NEXT_TARGET = "644-Y5-R10-parent-vertical-norm-coupling-owner-proof-or-demotion.md"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def source_register_rows() -> list[dict[str, object]]:
    sources = [
        ("S643_0", "checkpoint_642_doc", ROOT / "642-Y5-R10-charge-unit-Maxwell-proof-extension-or-kappa-alpha-pressure-runner.md", "immediate prior verdict: U1 partial, coupling owner missing"),
        ("S643_1", "validation_642", OUT / "P8_Y5_BRR545_642_VALIDATION.csv", "prior checkpoint validation input"),
        ("S643_2", "theorem_zero_attempt_642", OUT / "P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv", "U1/Maxwell/coupling blocker ledger"),
        ("S643_3", "runner_schema_blocks_642", OUT / "P8_Y5_R10_642_RUNNER_SCHEMA_BLOCKS.csv", "finite-coupling missing input ledger"),
        ("S643_4", "boundary_current_charge_287", ROOT / "287-boundary-current-charge-owner-attempt.md", "relative boundary current and Q_star obstruction"),
        ("S643_5", "k9_ward_index_288", ROOT / "288-k9-Ward-index-level-attempt.md", "level/index obstruction"),
        ("S643_6", "two_ninth_charge_attempt_109", ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md", "Q_star and Ward trace missing in amplitude branch"),
        ("S643_7", "endpoint_charge_110", ROOT / "110-endpoint-charge-equation-attempt.md", "endpoint equation and Qstar blocker"),
        ("S643_8", "boundary_charge_decision_140", ROOT / "140-boundary-charge-amplitude-decision-gate.md", "charge amplitude promotion blockers"),
        ("S643_9", "universal_coupling_contract_240", ROOT / "240-universal-coupling-parent-contract-or-local-bound-data-runner.md", "forbidden alpha_EM(Z) direct coupling warning"),
        ("S643_10", "parent_hamiltonian_trace_current_332", ROOT / "332-parent-Hamiltonian-trace-current-gate.md", "unit-coupling inheritance pattern and rescalability warning"),
        ("S643_11", "generator_script_643", SCRIPT_PATH, "this checkpoint generator"),
    ]
    return [
        {
            "source_id": source_id,
            "label": label,
            "path": rel(path),
            "exists": bool_text(path.exists()),
            "role": role,
            "valid_for_claim": "false",
        }
        for source_id, label, path, role in sources
    ]


def owner_candidate_rows() -> list[dict[str, object]]:
    return [
        {
            "owner_id": "AO643_0_compact_U1",
            "route": "compact U1 fibre",
            "mechanism": "periodic phase and integer representations label charge sectors",
            "what_it_can_fix": "relative/integer charge labels after Q_star exists",
            "rescaling_test": "fails_to_fix_coupling",
            "corpus_status": "partial_from_642",
            "main_blocker": "Q_star and g_EM remain rescalable",
            "rank": "support_only",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "AO643_1_Dirac_flux_monopole",
            "route": "Dirac or flux quantization",
            "mechanism": "electric and magnetic charges obey a quantized product; flux periods are integral",
            "what_it_can_fix": "charge product or flux unit if the magnetic/topological flux unit is parent-fixed",
            "rescaling_test": "passes_only_if_flux_unit_independently_owned",
            "corpus_status": "not_present_as_parent_theorem",
            "main_blocker": "no MTS magnetic/topological flux unit fixes e or g_EM",
            "rank": "high_value_possible_route",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "AO643_2_BF_or_Chern_Simons_level",
            "route": "topological BF/Chern-Simons level",
            "mechanism": "integer level fixes a boundary/topological response coefficient",
            "what_it_can_fix": "possibly a boundary charge lattice or response level",
            "rescaling_test": "does_not_fix_4D_Maxwell_kinetic_term_unless_bulk_inherits_level",
            "corpus_status": "flagged_open_from_288",
            "main_blocker": "no parent boundary level couples to the observed 4D Maxwell kinetic normalization",
            "rank": "possible_but_not_best",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "AO643_3_anomaly_or_Ward_index",
            "route": "anomaly cancellation / Ward index theorem",
            "mechanism": "consistency of charged matter fixes representation lattice or an effective level",
            "what_it_can_fix": "charge ratios and possibly a level denominator k",
            "rescaling_test": "usually_fixes_representations_not_low_energy_alpha",
            "corpus_status": "attempted_287_288_109_110_not_closed",
            "main_blocker": "no operator, complex, anomaly, or Ward identity with fixed index/level",
            "rank": "best_charge_unit_route_but_not_alpha_value_route",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "AO643_4_KK_radius_or_compactification_volume",
            "route": "Kaluza-Klein radius / compactification volume",
            "mechanism": "gauge coupling inherits from parent metric volume or radius",
            "what_it_can_fix": "g_EM if the compact radius/volume is fixed by the same parent geometry",
            "rescaling_test": "passes_only_if_radius_modulus_is_fixed_and_locally_silent",
            "corpus_status": "not_derived_in_MTS_charge_branch",
            "main_blocker": "unfixed radius/modulus becomes an alpha variation channel",
            "rank": "dangerous_but_real_candidate",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "AO643_5_parent_vertical_norm",
            "route": "parent vertical generator norm / subblock inheritance",
            "mechanism": "A_mu is the projection of the parent connection on a compact vertical generator T_Q whose norm is fixed by the parent metric/symplectic form",
            "what_it_can_fix": "g_EM as a literal inherited subblock coefficient rather than an added lambda_A",
            "rescaling_test": "passes_if_no_independent_lambda_A_or_generator_rescaling_is_allowed",
            "corpus_status": "best_new_contract_not_yet_proved",
            "main_blocker": "need parent action, generator normalization, measure/coframe descent, and no extra F^2 invariant",
            "rank": "selected_next_route",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "AO643_6_spectral_or_unification_boundary",
            "route": "spectral action / unification boundary / RG flow",
            "mechanism": "UV action fixes relative gauge kinetic coefficients, RG maps to low energy",
            "what_it_can_fix": "possibly alpha_EM after UV scale, thresholds, and matter content are fixed",
            "rescaling_test": "fails_without_UV_scale_and_thresholds",
            "corpus_status": "outside_current_MTS_parent_action",
            "main_blocker": "would import a large external particle-physics sector",
            "rank": "later_extension_not_current_best",
            "valid_for_claim": "false",
        },
        {
            "owner_id": "AO643_7_finite_coupling_empirical",
            "route": "finite kappa_alpha as bounded parameter",
            "mechanism": "accept alpha response and constrain it against clocks/WEP/R10/spectra",
            "what_it_can_fix": "nothing derivational; gives an honest empirical corridor",
            "rescaling_test": "not_a_coupling_owner",
            "corpus_status": "runner_schema_ready_from_642",
            "main_blocker": "Xhat unit, tau maps, sensitivities, and source normalizations are missing",
            "rank": "fallback",
            "valid_for_claim": "false",
        },
    ]


def rescaling_no_go_rows() -> list[dict[str, object]]:
    return [
        {
            "test_id": "RNG643_0_connection_rescale",
            "test": "Can A_mu -> s A_mu and g_EM -> s g_EM leave the same equations after redefining current/charge units?",
            "if_yes": "coupling normalization is conventional or free",
            "current_result": "yes_for_plain_U1_closure",
            "owner_implication": "compactness alone cannot own alpha_EM",
            "valid_for_claim": "false",
        },
        {
            "test_id": "RNG643_1_add_independent_F2",
            "test": "Can the parent action add lambda_A F_munu F^munu as a separate invariant?",
            "if_yes": "lambda_A is a free coupling and D_v alpha_EM is not theorem-zero",
            "current_result": "not_forbidden_by_current_corpus",
            "owner_implication": "must prove literal subblock inheritance or symmetry forbiddance",
            "valid_for_claim": "false",
        },
        {
            "test_id": "RNG643_2_generator_norm",
            "test": "Is the vertical generator T_Q normalized by a fixed lattice/metric, so T_Q -> s T_Q is illegal?",
            "if_yes": "charge unit and kinetic normalization can share one parent owner",
            "current_result": "not_derived",
            "owner_implication": "this is the next proof target",
            "valid_for_claim": "false",
        },
        {
            "test_id": "RNG643_3_modulus_silence",
            "test": "If g_EM depends on a radius/volume/modulus, is that modulus quotient-fixed and locally silent?",
            "if_yes": "KK/volume route could avoid clock/spectra disaster",
            "current_result": "not_derived",
            "owner_implication": "KK-style route remains dangerous until local silence is proved",
            "valid_for_claim": "false",
        },
    ]


def selected_contract_rows() -> list[dict[str, object]]:
    return [
        {
            "clause_id": "PVC643_0_parent_bundle",
            "needed_statement": "The MTS parent state has a compact vertical U(1)-like charge fibre with generator T_Q.",
            "why_it_matters": "gives a real charge fibre rather than a borrowed EM label",
            "current_status": "partial_template_only",
            "acceptance_test": "T_Q appears in the parent configuration/action, not only in the closure ledger",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PVC643_1_fixed_generator_norm",
            "needed_statement": "The norm <T_Q,T_Q> is fixed by a parent metric/symplectic/lattice structure and cannot be rescaled.",
            "why_it_matters": "blocks the A_mu/T_Q rescaling freedom that makes g_EM arbitrary",
            "current_status": "missing",
            "acceptance_test": "derive a dimensionless or dimensional norm from existing parent variables without fitting alpha_EM",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PVC643_2_connection_projection",
            "needed_statement": "The observed EM connection A_mu is the parent connection projected onto T_Q.",
            "why_it_matters": "ties matter charge and Maxwell curvature to the same parent object",
            "current_status": "missing",
            "acceptance_test": "show F_Q = dA_Q + ... descends to the observed EM two-form",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PVC643_3_kinetic_subblock_inheritance",
            "needed_statement": "The Maxwell F_Q^2 term is a literal subblock of the parent kinetic/curvature norm with no independent lambda_A.",
            "why_it_matters": "this would own g_EM rather than insert it",
            "current_status": "missing",
            "acceptance_test": "prove no separate covariant F_Q^2 invariant can be added without double-counting or breaking the parent constraint",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PVC643_4_measure_coframe_descent",
            "needed_statement": "The measure and Hodge star in the F_Q^2 term descend to the same observed local coframe used by matter.",
            "why_it_matters": "prevents a hidden frame/clock dependence that would re-open alpha pressure",
            "current_status": "missing",
            "acceptance_test": "map parent measure/coframe to local observed units and show vertical local variations are silent",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PVC643_5_charge_current_same_owner",
            "needed_statement": "The Noether/boundary current couples to the same A_Q with charge unit Q_star fixed by the same T_Q normalization.",
            "why_it_matters": "ties charge unit and gauge kinetic normalization together",
            "current_status": "missing",
            "acceptance_test": "derive Q/e or Q/Q_star and the Maxwell source normalization from one parent object",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "PVC643_6_vertical_alpha_silence",
            "needed_statement": "D_v ln alpha_EM = 0 follows because T_Q norm, parent kinetic norm, hbar/c readout, and charge lattice are quotient-fixed.",
            "why_it_matters": "this is the actual kappa_alpha zero theorem",
            "current_status": "conditional_future_theorem",
            "acceptance_test": "all prior clauses pass and no alpha_EM(Xhat) or f_A(Xhat)F^2 vertex remains",
            "valid_for_claim": "false",
        },
    ]


def finite_bound_fill_rows() -> list[dict[str, object]]:
    rows = read_csv(OUT / "P8_Y5_R10_642_RUNNER_SCHEMA_BLOCKS.csv")
    mapping = {
        "RS642_0": ("FBF643_0", "Xhat_unit_owner", "derive from parent vertical norm or define explicit finite prior unit"),
        "RS642_1": ("FBF643_1", "arena_tau_maps", "derive tau_R10/tau_WEP/tau_clock/tau_EM projection maps"),
        "RS642_2": ("FBF643_2", "alpha_sensitivity_coefficients", "source or compute material/clock alpha sensitivity coefficients"),
        "RS642_3": ("FBF643_3", "R10_body_EM_binding", "map short-range body composition to EM binding/source response"),
        "RS642_4": ("FBF643_4", "alpha_owner_or_prior", "close parent owner or explicitly choose finite nonclaim prior"),
    }
    out: list[dict[str, object]] = []
    for row in rows:
        fill_id, target, action = mapping[row["input_id"]]
        out.append(
            {
                "fill_id": fill_id,
                "target": target,
                "from_642_input": row["needed_input"],
                "current_status": row["status"],
                "next_action": action,
                "blocks_numeric_score": row["blocks_numeric_score"],
                "valid_for_claim": "false",
            }
        )
    return out


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D643_0",
            "selected_route": "parent_vertical_norm",
            "why_selected": "it is the only route in the current MTS language that can tie charge unit, Maxwell kinetic normalization, matter current, and local vertical silence to one parent object",
            "current_status": "best_route_not_proved",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
        },
        {
            "decision_id": "D643_1",
            "selected_route": "finite_coupling_fallback",
            "why_selected": "kept as honest fallback if the vertical norm cannot be parent-signed",
            "current_status": "schema_ready_inputs_missing",
            "next_target": "fill only after owner proof fails or is demoted",
            "valid_for_claim": "false",
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "selected_owner_candidate": "AO643_5_parent_vertical_norm",
            "kappa_alpha_zero_claim": "false",
            "numeric_score_allowed": "false",
            "strongest_positive_result": "the coupling hunt has a best MTS-native target: fixed norm of the compact vertical charge generator with no independent F2 coefficient",
            "hardest_blocker": "no parent action currently proves the vertical generator norm, connection projection, kinetic subblock inheritance, and current normalization are one object",
            "next_target": NEXT_TARGET,
        }
    ]


def validation_rows(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    rescale_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
) -> list[dict[str, object]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("V643_0_source_paths_exist", all(row["exists"] == "true" for row in source_rows), "all cited local source paths exist"))
    prior = read_csv(OUT / "P8_Y5_BRR545_642_VALIDATION.csv")
    checks.append(("V643_1_prior_642_validation_clean", all(row.get("result") == "pass" for row in prior), "642 validation remains clean"))
    checks.append(("V643_2_selected_owner_present", any(row["owner_id"] == "AO643_5_parent_vertical_norm" and row["rank"] == "selected_next_route" for row in owner_rows), "parent vertical norm route is selected"))
    checks.append(("V643_3_no_owner_claim_valid", all(row["valid_for_claim"] == "false" for row in owner_rows), "owner candidates are nonclaim"))
    checks.append(("V643_4_rescaling_no_go_has_blocker", any(row["current_result"] in {"not_forbidden_by_current_corpus", "not_derived"} for row in rescale_rows), "rescaling/free-coupling blockers remain explicit"))
    checks.append(("V643_5_contract_has_required_clauses", len(contract_rows) >= 6 and any(row["clause_id"] == "PVC643_3_kinetic_subblock_inheritance" for row in contract_rows), "vertical-norm contract includes kinetic subblock inheritance"))
    checks.append(("V643_6_contract_nonclaim", all(row["valid_for_claim"] == "false" for row in contract_rows), "proof contract is not claim-valid"))
    checks.append(("V643_7_finite_inputs_still_block_score", all(row["blocks_numeric_score"] == "true" and row["valid_for_claim"] == "false" for row in finite_rows), "finite-coupling inputs still block numeric scoring"))
    checks.append(("V643_8_decision_nonclaim", all(row["valid_for_claim"] == "false" for row in decision), "decision rows do not claim pass"))
    checks.append(("V643_9_summary_nonclaim", summary[0]["numeric_score_allowed"] == "false" and summary[0]["kappa_alpha_zero_claim"] == "false", "summary stays nonclaim"))

    fw = ROOT.parent / "formalization-workbench"
    cutoff = datetime(2026, 5, 31, 14, 42, 0).timestamp()
    changed_after_cutoff = 0
    if fw.exists():
        for path in fw.rglob("*"):
            if path.is_file() and path.stat().st_mtime > cutoff:
                changed_after_cutoff += 1
    checks.append(("V643_10_formalization_workbench_unchanged", changed_after_cutoff == 0, f"formalization files changed after cutoff: {changed_after_cutoff}"))

    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now_iso(),
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            text = str(row.get(column, "")).replace("|", "\\|").replace("\n", " ")
            values.append(text)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def write_doc(
    source_rows: list[dict[str, object]],
    owner_rows: list[dict[str, object]],
    rescale_rows: list[dict[str, object]],
    contract_rows: list[dict[str, object]],
    finite_rows: list[dict[str, object]],
    decision: list[dict[str, object]],
    summary: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    lines = [
        "# 643 Y5/R10 Alpha Normalization Owner or Finite Coupling Bound Input Fill",
        "",
        "## Verdict",
        "",
        f"- Status: `{STATUS}`",
        f"- Claim ceiling: `{CLAIM_CEILING}`",
        "- The best current hunt result is not Dirac, not Chern-Simons, not plain compact `U(1)`: it is parent vertical-generator norm/subblock inheritance.",
        "- In plain terms: the coupling is owned only if the EM connection is a projection of a parent compact vertical generator whose norm and kinetic term cannot be independently rescaled.",
        "- This is a strong target but not yet a proof. The finite-coupling branch remains nonclaim because the projection units and arena maps are missing.",
        "",
        "## Source Register",
        "",
        markdown_table(source_rows, ["source_id", "label", "path", "exists", "role"]),
        "",
        "## Owner Candidate Matrix",
        "",
        markdown_table(owner_rows, ["owner_id", "route", "what_it_can_fix", "rescaling_test", "corpus_status", "rank", "main_blocker"]),
        "",
        "## Rescaling No-Go Tests",
        "",
        markdown_table(rescale_rows, ["test_id", "test", "current_result", "owner_implication"]),
        "",
        "## Selected Parent Vertical Norm Contract",
        "",
        markdown_table(contract_rows, ["clause_id", "needed_statement", "current_status", "acceptance_test"]),
        "",
        "## Finite Coupling Bound Input Fill",
        "",
        markdown_table(finite_rows, ["fill_id", "target", "from_642_input", "current_status", "next_action", "blocks_numeric_score"]),
        "",
        "## Decision",
        "",
        markdown_table(decision, ["decision_id", "selected_route", "current_status", "why_selected", "next_target"]),
        "",
        "## Validation",
        "",
        markdown_table(validation, ["check_id", "result", "detail"]),
        "",
        "## Interpretation",
        "",
        "- This is the coupling goblin finally cornered into a small room: the theory must forbid an independent `lambda_A F^2` coefficient.",
        "- If the parent vertical norm exists and is fixed, MTS has a real route to `kappa_alpha = 0` without cheating.",
        "- If that norm cannot be derived, we stop trying to topologically wish away alpha and move to a finite-coupling bound programme.",
        "",
        "## Nonclaim Summary",
        "",
        markdown_table(summary, ["status", "selected_owner_candidate", "kappa_alpha_zero_claim", "numeric_score_allowed", "hardest_blocker", "next_target"]),
        "",
    ]
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    source_rows = source_register_rows()
    owner_rows = owner_candidate_rows()
    rescale_rows = rescaling_no_go_rows()
    contract_rows = selected_contract_rows()
    finite_rows = finite_bound_fill_rows()
    decision = decision_rows()
    summary = nonclaim_summary_rows()
    validation = validation_rows(source_rows, owner_rows, rescale_rows, contract_rows, finite_rows, decision, summary)

    write_csv(OUT / "P8_Y5_R10_643_SOURCE_REGISTER.csv", source_rows)
    write_csv(OUT / "P8_Y5_R10_643_OWNER_CANDIDATE_MATRIX.csv", owner_rows)
    write_csv(OUT / "P8_Y5_R10_643_RESCALING_NO_GO.csv", rescale_rows)
    write_csv(OUT / "P8_Y5_R10_643_PARENT_VERTICAL_NORM_CONTRACT.csv", contract_rows)
    write_csv(OUT / "P8_Y5_R10_643_FINITE_BOUND_INPUT_FILL.csv", finite_rows)
    write_csv(OUT / "P8_Y5_BRR545_643_DECISION.csv", decision)
    write_csv(OUT / "P8_Y5_R10_643_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_BRR545_643_VALIDATION.csv", validation)
    write_doc(source_rows, owner_rows, rescale_rows, contract_rows, finite_rows, decision, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"wrote_doc={DOC_PATH}")
    print(f"wrote_csv_dir={OUT}")
    print(f"owner_candidates={len(owner_rows)}")
    print(f"selected_owner=AO643_5_parent_vertical_norm")
    print(f"validation_rows={len(validation)}")
    print(f"validation_failures={len(failures)}")
    print(f"status={STATUS}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for row in failures:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
