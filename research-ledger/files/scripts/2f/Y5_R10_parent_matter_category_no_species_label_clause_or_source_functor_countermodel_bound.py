from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "954-Y5-R10-parent-matter-category-no-species-label-clause-or-source-functor-countermodel-bound.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def md_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(fields) + " |"
    separator = "| " + " | ".join("---" for _field in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join([header, separator, *body])


def source_path(relative_path: str) -> Path:
    return ROOT / relative_path


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "953_doc",
            "path": "953-Y5-R10-no-species-label-source-functor-theorem-or-filled-coefficient-intake-review.md",
            "role": "handoff: conditional source-functor theorem and open label-forgetting clause",
            "needle": "parent label-forgetting quotient",
        },
        {
            "source_id": "953_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_953_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V953_11_validation_rows_ready",
        },
        {
            "source_id": "953_parent_contract",
            "path": "source-intake/mts_residuals/P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
            "role": "parent category clause list",
            "needle": "PMC953_1_label_forgetting_quotient",
        },
        {
            "source_id": "953_countermodel",
            "path": "source-intake/mts_residuals/P8_Y5_R10_953_COUNTERMODEL_LEDGER.csv",
            "role": "species-labelled source functor countermodel",
            "needle": "CM953_4_verdict",
        },
        {
            "source_id": "952_intake_template",
            "path": "source-intake/mts_residuals/P8_Y5_R10_952_COEFFICIENT_INTAKE_TEMPLATE.csv",
            "role": "nonclaim comparison bounds inherited for fallback route",
            "needle": "CIT952_2_WEP_surface_beta_source",
        },
        {
            "source_id": "source_current_contract",
            "path": "source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv",
            "role": "older source-current Ward/universality contract",
            "needle": "SC3_universal_kappa_coupling",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "no-marker/no-species source contract",
            "needle": "S4_source_normalization_species_blind",
        },
        {
            "source_id": "derived_zero_targets",
            "path": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv",
            "role": "selector-blind source theorem target",
            "needle": "DZ5_selector_blind_source",
        },
        {
            "source_id": "r11_missing_ledger",
            "path": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv",
            "role": "missing source-charge theorem or bound row",
            "needle": "R11SN_5_species_source_charge",
        },
        {
            "source_id": "631_source_charge",
            "path": "source-intake/mts_residuals/P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv",
            "role": "composition channel remains open if species labels survive",
            "needle": "Q631_2_composition_channel",
        },
    ]
    rows = []
    for spec in specs:
        path = source_path(spec["path"])
        exists = path.exists()
        needle_found = exists and spec["needle"] in read_text(path)
        rows.append(
            {
                **spec,
                "absolute_path": str(path),
                "exists": flag(exists),
                "needle_found": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def parent_label_forgetting_attempt() -> list[dict[str, str]]:
    return [
        {
            "attempt_id": "PLF954_0_target",
            "step": "parent source-domain label-forgetting",
            "mathematical_form": "q_src({(T_A,A)}) = T_total = sum_A T_A",
            "status": "target_from_953",
            "what_closes": "removes relative kappa_A/kappa_B from source coupling theorem",
            "gap": "target itself is not a derivation",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PLF954_1_total_variation_route",
            "step": "source is total variation of one matter action",
            "mathematical_form": "T_munu = (2/sqrt(-g_obs)) delta S_matter / delta g_obs^{munu}; S_matter=sum_A S_A",
            "status": "conditional_derivation_step_valid",
            "what_closes": "labelled decomposition disappears after taking the total Hilbert derivative",
            "gap": "only works if S_matter contains no source-only species weights before variation",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PLF954_2_prefactor_obstruction",
            "step": "species prefactors before variation block the proof",
            "mathematical_form": "S_matter = sum_A w_A S_A gives T_source=sum_A w_A T_A",
            "status": "counterexample_to_unconditional_derivation",
            "what_closes": "nothing; identifies the exact forbidden parent term",
            "gap": "diffeomorphism covariance and additivity still allow constant w_A",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PLF954_3_minimal_matter_normalization",
            "step": "canonical matter normalization must be fixed by nongravitational standards, not by source labels",
            "mathematical_form": "w_A=1 after field normalization; theta_A in S_A but no extra gravitational source coefficient",
            "status": "plausible_parent_clause_not_derived_here",
            "what_closes": "turns per-species source weights into forbidden double-counting of matter normalization",
            "gap": "needs an explicit parent action/schema clause, not just interpretive preference",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PLF954_4_field_equation_once",
            "step": "geometry equation couples once to the total variational source",
            "mathematical_form": "E_munu[e_obs,...] = kappa_univ T_munu[S_matter,e_obs]",
            "status": "conditional_GR_like_source_structure",
            "what_closes": "makes the GR/Newton source side structurally standard after calibration of kappa_univ",
            "gap": "left-hand EH/Newton limit and hidden residual currents are separate gates",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "attempt_id": "PLF954_5_verdict",
            "step": "parent label-forgetting derivation",
            "mathematical_form": "single S_matter total variation + no w_A + no hidden source spurions => q_src forgets A",
            "status": "exact_contract_written_not_parent_signed",
            "what_closes": "would close the 953 missing clause if adopted/derived by the parent action",
            "gap": "current corpus still has to prove or declare the no-prefactor matter-action clause",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parent_action_clause() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PAC954_0_single_matter_functional",
            "required_clause": "ordinary matter enters as one total matter functional on one observed coframe",
            "mathematical_form": "S_matter[Psi,e_obs,theta]=sum_A S_A[Psi_A,e_obs,theta_A]",
            "purpose": "source is one variational object, not separate labelled source channels",
            "current_status": "ready_as_parent_contract",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC954_1_no_source_prefactors",
            "required_clause": "no independent species source prefactors multiply matter actions",
            "mathematical_form": "partial S_matter / partial w_A = 0 for any source-only w_A; equivalently w_A is absent",
            "purpose": "forbids T_source=sum_A w_A T_A",
            "current_status": "exact_high_pressure_missing_clause",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC954_2_total_Hilbert_derivative",
            "required_clause": "the active ordinary source is the total Hilbert/coframe derivative of S_matter",
            "mathematical_form": "T_total := delta S_matter/delta e_obs = sum_A delta S_A/delta e_obs",
            "purpose": "performs label-forgetting by variation of the sum",
            "current_status": "conditional_math_clean",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC954_3_no_hidden_spurion_return",
            "required_clause": "no material marker, boundary class, domain selector, or post-readout mask reweights the source after variation",
            "mathematical_form": "partial_A kappa=partial_m kappa=partial_D kappa=partial_boundary kappa=0",
            "purpose": "prevents kappa_A returning under another name",
            "current_status": "named_by_prior_contracts_not_parent_signed",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC954_4_nonHilbert_current_split",
            "required_clause": "spin/torsion/boundary/non-Hilbert currents are absent, exact, projected silent, or retained as explicit residuals",
            "mathematical_form": "J_src = kappa_univ T_Hilbert + J_NH_retained; J_NH_retained=0 for derived local-GR branch",
            "purpose": "keeps the source theorem from being bypassed",
            "current_status": "open_parallel_gate",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PAC954_5_GR_source_limit_clause",
            "required_clause": "after PAC954_0..4, the source side reduces to the GR source term with one calibrated constant",
            "mathematical_form": "E_munu = kappa_univ T_munu; kappa_univ calibrated to 8 pi G_ref/c^4",
            "purpose": "connects the coupling branch to the GR/Newton reduction programme",
            "current_status": "conditional_on_parent_signature",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parse_positive_float(value: str) -> bool:
    try:
        return float(value) > 0.0
    except ValueError:
        return False


def source_functor_bound_targets() -> list[dict[str, str]]:
    rows = []
    for row in read_csv(OUT / "P8_Y5_R10_952_COEFFICIENT_INTAKE_TEMPLATE.csv"):
        numeric_bound = parse_positive_float(row["comparison_bound"])
        bound_id = row["intake_id"].replace("CIT952", "SCB954")
        if row["coefficient_symbol"] == "beta_source_normalized":
            countermodel_parameter = "epsilon_species_source_weight"
            projection_needed = "species-weight vector, source composition map, test-body sensitivity diagnostic"
        elif row["coefficient_symbol"] == "kappa_alpha_tau_clock_time":
            countermodel_parameter = "kappa_alpha_tau_clock_time_product"
            projection_needed = "alpha response coefficient times local clock/time residual"
        else:
            countermodel_parameter = "parent_zero_theorem_switch"
            projection_needed = "parent-signed PAC954 no-prefactor/no-spurion theorem"
        rows.append(
            {
                "bound_id": bound_id,
                "coefficient_symbol": row["coefficient_symbol"],
                "arena": row["arena"],
                "countermodel_parameter": countermodel_parameter,
                "comparison_bound": row["comparison_bound"],
                "units": row["units"],
                "bound_numeric_positive": flag(numeric_bound) if row["units"] != "boolean" else "not_applicable",
                "projection_needed": projection_needed,
                "candidate_prediction": "MISSING_PARENT_INPUT",
                "candidate_source_path": "MISSING_PARENT_SOURCE",
                "status": "bound_target_ready_prediction_missing",
                "accepted_for_scoring": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def countermodel_to_bound_map() -> list[dict[str, str]]:
    return [
        {
            "map_id": "CBM954_0_labelled_weight",
            "open_countermodel": "F_src({(T_A,A)})=sum_A kappa_A T_A",
            "residual_parameter": "epsilon_A=(kappa_A-kappa_ref)/kappa_ref",
            "first_test_arena": "MICROSCOPE/WEP composition diagnostics",
            "observable_shape": "eta_AB approximately sensitivity_weighted difference in epsilon_A",
            "required_inputs": "composition sensitivity matrix, source body composition, test body composition, chosen reference species",
            "current_status": "schema_only_no_numeric_prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "CBM954_1_hidden_spurion",
            "open_countermodel": "constant hidden source weights ride as superselection data",
            "residual_parameter": "s_A with kappa_A=kappa_0(1+epsilon s_A)",
            "first_test_arena": "WEP plus clock/product bounds if constants drift with time branch",
            "observable_shape": "composition-dependent acceleration or alpha-clock product",
            "required_inputs": "spurion-to-composition projection and source path for epsilon",
            "current_status": "schema_only_no_numeric_prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "CBM954_2_nonHilbert_current",
            "open_countermodel": "boundary, torsion, spin, or non-Hilbert current carries material labels",
            "residual_parameter": "J_NH[A,boundary] projection coefficient",
            "first_test_arena": "PPN/WEP/orbital source-normalization residuals",
            "observable_shape": "extra active mass or preferred-source residual",
            "required_inputs": "current decomposition, projection operator, local bound arena",
            "current_status": "schema_only_no_numeric_prediction",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "map_id": "CBM954_3_verdict",
            "open_countermodel": "if PAC954 is unsigned, the theory needs finite residual rows rather than a zero claim",
            "residual_parameter": "beta_source_normalized or retained source-weight vector",
            "first_test_arena": "WEP/source-normalization bound route",
            "observable_shape": "abs(predicted residual) <= arena bound",
            "required_inputs": "real coefficient, source path, derivation status, units, bound link",
            "current_status": "fallback_route_ready_but_unfilled",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC954_0_derivation_route",
            "topic": "parent label-forgetting",
            "result": "exact_parent_action_contract_identified",
            "reason": "total Hilbert variation of a single matter functional forgets labels, but only if source-only species prefactors are absent",
            "next_action": "turn PAC954 into a parent minimal-matter-action lemma and test it against hidden prefactor countermodels",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC954_1_obstruction",
            "topic": "species prefactor obstruction",
            "result": "unconditional_derivation_blocked",
            "reason": "S_matter=sum_A w_A S_A is covariant and additive but produces weighted source current",
            "next_action": "prove w_A is absent/canonical, or retain epsilon_A as finite residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC954_2_bound_route",
            "topic": "source-functor countermodel bound",
            "result": "fallback_bound_schema_ready_prediction_missing",
            "reason": "comparison bounds are available from prior nonclaim templates but no parent coefficient prediction exists",
            "next_action": "build a small residual runner only after epsilon_A or beta_source_normalized has real provenance",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE954_0_parent_label_forgetting",
            "claim": "parent matter/source category forgets species labels",
            "required_condition": "PAC954 no-prefactor total-variation clause parent-signed",
            "current_evidence": "exact contract written but unsigned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE954_1_single_kappa",
            "claim": "one universal source coupling follows",
            "required_condition": "953 conditional theorem plus 954 parent action clause both signed",
            "current_evidence": "953 theorem conditional; 954 clause unsigned",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE954_2_countermodel_bound",
            "claim": "species-labelled countermodel is below bounds",
            "required_condition": "finite epsilon/beta prediction with source path and units",
            "current_evidence": "bounds named, prediction missing",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE954_3_GR_Newton_source_side",
            "claim": "source side reduces to GR/Newton matter source",
            "required_condition": "single total Hilbert source, common kappa calibration, no non-Hilbert/boundary source residuals",
            "current_evidence": "source side route sharpened but hidden residual gates remain",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "955-Y5-R10-minimal-matter-action-source-coupling-lemma-or-species-weight-residual-runner.md",
            "objective": "formalize the PAC954 minimal-matter-action/no-source-prefactor lemma; if it fails, implement a strict residual runner for species weights using only sourced coefficient rows",
            "include": "single matter functional, total Hilbert variation, no source-only prefactors, common kappa calibration, species-weight residual schema",
            "exclude": "invented coefficients, WEP/local-GR claim, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed = 0
    for path in FORMALIZATION.rglob("*"):
        if not path.is_file():
            continue
        modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified > SCRIPT_START_UTC:
            changed += 1
    return changed


def validation(
    sources: list[dict[str, str]],
    attempt_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_953_VALIDATION.csv"))
    total_variation_valid = any(row["attempt_id"] == "PLF954_1_total_variation_route" and row["status"] == "conditional_derivation_step_valid" for row in attempt_rows)
    prefactor_obstruction_named = any(row["attempt_id"] == "PLF954_2_prefactor_obstruction" for row in attempt_rows)
    exact_clause_written = any(row["clause_id"] == "PAC954_1_no_source_prefactors" and row["current_status"] == "exact_high_pressure_missing_clause" for row in clause_rows)
    bound_rows_ready = len(bound_rows) == 5 and all(row["accepted_for_scoring"] == "false" and row["candidate_prediction"] == "MISSING_PARENT_INPUT" for row in bound_rows)
    numeric_bounds_ok = all(row["units"] == "boolean" or row["bound_numeric_positive"] == "true" for row in bound_rows)
    map_ready = any(row["map_id"] == "CBM954_3_verdict" and row["current_status"] == "fallback_route_ready_but_unfilled" for row in map_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = bool(target_rows) and target_rows[0]["next_target"].startswith("955-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, attempt_rows, clause_rows, bound_rows, map_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V954_0_sources_exist_and_needles", sources_ok, "all 954 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V954_1_prior_953_clean", prior_clean, "P8_Y5_BRR545_953_VALIDATION.csv clean")
    add("V954_2_total_variation_route_valid", total_variation_valid, "total Hilbert variation gives conditional label-forgetting")
    add("V954_3_prefactor_obstruction_named", prefactor_obstruction_named, "species prefactor obstruction explicitly recorded")
    add("V954_4_exact_parent_clause_written", exact_clause_written, "PAC954 no-source-prefactor clause written")
    add("V954_5_bound_targets_ready_nonclaim", bound_rows_ready, "fallback bound rows ready but predictions missing")
    add("V954_6_numeric_bounds_positive", numeric_bounds_ok, "numeric inherited bounds are positive where applicable")
    add("V954_7_countermodel_map_ready", map_ready, "countermodel-to-bound map written")
    add("V954_8_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V954_9_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V954_10_next_target_selected", target_selected, "955 minimal matter action lemma or residual runner selected")
    add("V954_11_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V954_12_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V954_13_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    attempt_rows: list[dict[str, str]],
    clause_rows: list[dict[str, str]],
    bound_rows: list[dict[str, str]],
    map_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 954 Y5 R10: Parent Matter Category No-Species-Label Clause Or Source-Functor Countermodel Bound

Status: `Y5_R10_954_parent_action_contract_identified_prefactor_obstruction_retained_nonclaim`

Claim ceiling: `exact_contract_only_no_parent_signature_no_single_kappa_claim_no_GR_Newton_source_claim`

## Result

This checkpoint improves the coupling branch: the no-species-label condition is no longer a vague wish. It can be obtained by a concrete variational mechanism.

If ordinary matter is one total functional of one observed coframe, and the active ordinary source is defined as the total Hilbert/coframe derivative of that full matter action, then the source side naturally sees `T_total = sum_A T_A`. The species decomposition is bookkeeping; the source object is the total variational derivative.

But the proof has a precise obstruction. If the parent permits `S_matter = sum_A w_A S_A`, with independent source-only weights `w_A`, then variation gives `T_source = sum_A w_A T_A`. That is still covariant, additive, and Ward-compatible. So the exact missing parent clause is: no independent species source prefactors before variation.

That is not grim; it is useful. The route to GR/Newton source behavior is now a specific parent-action lemma instead of a fog bank.

```text
single total matter action + total Hilbert variation + no source-only w_A
    => label-forgotten source
    => one kappa_univ after the 953 theorem
but PAC954 is still unsigned, so all claims remain blocked.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Parent Label-Forgetting Attempt

{md_table(attempt_rows, ["attempt_id", "step", "status", "what_closes", "gap", "parent_signed"])}

## Parent Action Clause

{md_table(clause_rows, ["clause_id", "required_clause", "purpose", "current_status", "parent_signed"])}

## Source-Functor Bound Targets

{md_table(bound_rows, ["bound_id", "coefficient_symbol", "arena", "countermodel_parameter", "comparison_bound", "units", "candidate_prediction", "status"])}

## Countermodel To Bound Map

{md_table(map_rows, ["map_id", "open_countermodel", "residual_parameter", "first_test_arena", "observable_shape", "current_status"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    attempt_rows = parent_label_forgetting_attempt()
    clause_rows = parent_action_clause()
    bound_rows = source_functor_bound_targets()
    map_rows = countermodel_to_bound_map()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(sources, attempt_rows, clause_rows, bound_rows, map_rows, decision_rows, claim_rows, target_rows)

    write_csv(
        OUT / "P8_Y5_R10_954_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_954_PARENT_LABEL_FORGETTING_ATTEMPT.csv",
        attempt_rows,
        [
            "attempt_id",
            "step",
            "mathematical_form",
            "status",
            "what_closes",
            "gap",
            "parent_signed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_954_PARENT_ACTION_CLAUSE.csv",
        clause_rows,
        [
            "clause_id",
            "required_clause",
            "mathematical_form",
            "purpose",
            "current_status",
            "parent_signed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_954_SOURCE_FUNCTOR_BOUND_TARGETS.csv",
        bound_rows,
        [
            "bound_id",
            "coefficient_symbol",
            "arena",
            "countermodel_parameter",
            "comparison_bound",
            "units",
            "bound_numeric_positive",
            "projection_needed",
            "candidate_prediction",
            "candidate_source_path",
            "status",
            "accepted_for_scoring",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_954_COUNTERMODEL_TO_BOUND_MAP.csv",
        map_rows,
        [
            "map_id",
            "open_countermodel",
            "residual_parameter",
            "first_test_arena",
            "observable_shape",
            "required_inputs",
            "current_status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_954_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_954_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_954_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_954_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, attempt_rows, clause_rows, bound_rows, map_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
