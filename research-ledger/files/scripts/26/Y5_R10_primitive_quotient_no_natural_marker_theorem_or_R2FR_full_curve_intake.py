from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def flag(value: bool) -> str:
    return "true" if value else "false"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


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


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    since = SCRIPT_START_UTC.astimezone().strftime("%Y-%m-%dT%H:%M:%S")
    literal = str(FORMALIZATION).replace("'", "''")
    command = (
        "$since=[datetime]::Parse('"
        + since
        + "'); "
        + "$count=(Get-ChildItem -LiteralPath '"
        + literal
        + "' -Recurse -File | Where-Object { $_.LastWriteTime -gt $since } | Measure-Object).Count; "
        + "Write-Output $count"
    )
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    try:
        return int(completed.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return -2


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "964_doc",
            "path_type": "local",
            "path": "964-Y5-R10-parent-no-higher-derivative-minimality-theorem-or-R2FR-nonclaim-runner.md",
            "role": "immediate handoff: minimality theorem failed and primitive quotient/no-marker target selected",
            "needle": "965-Y5-R10-primitive-quotient-no-natural-marker-theorem-or-R2FR-full-curve-intake.md",
        },
        {
            "source_id": "413_no_marker",
            "path_type": "local",
            "path": "413-no-marker-parent-action-theorem-attempt.md",
            "role": "fixed active spurion conditional exclusion and material marker loophole",
            "needle": "co_moving_material_marker",
        },
        {
            "source_id": "414_invariant_algebra",
            "path_type": "local",
            "path": "414-local-quotient-invariant-algebra-triviality-gate.md",
            "role": "exact local invariant algebra triviality condition and generator list",
            "needle": "I_loc(Q) = I_geom[J^k(e_obs)] tensor constants",
        },
        {
            "source_id": "423_no_extension",
            "path_type": "local",
            "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
            "role": "primitive universal property and no-natural-marker theorem failure source",
            "needle": "no_natural_marker_functor",
        },
        {
            "source_id": "563_real_bound_checkpoint",
            "path_type": "local",
            "path": "563-Y5-R10-real-bound-curve-acquisition-and-alpha-row-smoke-runner.md",
            "role": "real R10 bound acquisition policy and anchor-only nonclaim warning",
            "needle": "anchor_only_non_curve",
        },
        {
            "source_id": "563_bound_curve_contract",
            "path_type": "local",
            "path": "source-intake/mts_residuals/P8_Y5_R10_BOUND_CURVE_REAL_DATA_CONTRACT.csv",
            "role": "contract requiring positive numeric full alpha(lambda) bound rows",
            "needle": "BC562_1_bound_curve_file",
        },
        {
            "source_id": "962_scalar_bound_fallback",
            "path_type": "local",
            "path": "source-intake/mts_residuals/P8_Y5_R10_962_SCALAR_BOUND_FALLBACK_ROWS.csv",
            "role": "R2/fR scalar bound fallback rows and Lee/Kapner anchors",
            "needle": "R2B962_2_Lee2020_anchor",
        },
        {
            "source_id": "lee_2020_eotwash_arxiv",
            "path_type": "web",
            "path": "https://arxiv.org/abs/2002.11761",
            "role": "modern Eot-Wash short-range inverse-square-law source for full alpha(lambda) curve extraction",
            "needle": "url_recorded",
        },
        {
            "source_id": "lee_2020_eotwash_pubmed",
            "path_type": "web",
            "path": "https://pubmed.ncbi.nlm.nih.gov/32216404/",
            "role": "bibliographic source for the 2020 short-range Eot-Wash result",
            "needle": "url_recorded",
        },
        {
            "source_id": "kapner_2007_eotwash",
            "path_type": "web",
            "path": "https://arxiv.org/abs/hep-ph/0611184",
            "role": "older Eot-Wash short-range continuity anchor",
            "needle": "url_recorded",
        },
        {
            "source_id": "adelberger_2003_review",
            "path_type": "web",
            "path": "https://arxiv.org/abs/hep-ph/0307284",
            "role": "review continuity source for inverse-square/fifth-force conventions",
            "needle": "url_recorded",
        },
    ]
    rows = []
    for spec in specs:
        is_local = spec["path_type"] == "local"
        absolute_path = source_path(spec["path"]) if is_local else ""
        exists = absolute_path.exists() if is_local else spec["path"].startswith("https://")
        if is_local and exists:
            needle_found = spec["needle"] in read_text(absolute_path)
        else:
            needle_found = not is_local and spec["needle"] == "url_recorded"
        rows.append(
            {
                **spec,
                "absolute_path": str(absolute_path) if is_local else spec["path"],
                "exists_or_recorded": flag(exists),
                "needle_found_or_na": flag(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def primitive_quotient_theorem_attempt() -> list[dict[str, str]]:
    rows = [
        {
            "attempt_id": "PQ965_0_theorem_target",
            "theorem_piece": "primitive quotient object",
            "would_need_to_show": "Q_MTS is the free/minimal primitive quotient generated by motion, time, and space, not a selected submodel of a larger admissible parent",
            "current_evidence": "423 states this as the needed universal-property theorem but does not prove the category, morphisms, or initial/minimal object",
            "status": "not_derived",
            "why_not_closed": "a covariant extension Q_tilde=(Q,m)/G_rel remains legal unless the primitive object is parent-signed",
            "consequence": "material-marker absence cannot earn theorem-zero credit",
        },
        {
            "attempt_id": "PQ965_1_fixed_spurion",
            "theorem_piece": "fixed active spurions",
            "would_need_to_show": "a fixed non-orbit label is not a function on the strict quotient configuration space",
            "current_evidence": "413 and 423 give a conditional quotient argument against fixed active labels",
            "status": "conditional_pass_if_strict_quotient_parent_proven",
            "why_not_closed": "this kills fixed labels only, not transforming/covariant marker fields",
            "consequence": "useful anti-cheat result, but insufficient for local GR",
        },
        {
            "attempt_id": "PQ965_2_no_natural_marker_functor",
            "theorem_piece": "no-natural-marker functor",
            "would_need_to_show": "there is no natural covariant construction m=M(Q_MTS,matter,class data) producing nonconstant local scalars or source labels",
            "current_evidence": "414 lists extra local invariant generators; 423 marks no_natural_marker_functor as not derived",
            "status": "not_derived",
            "why_not_closed": "finite-cell spectra, domain/class data, memory scalars, and species constants can be quotient-invariant",
            "consequence": "R1/R2/R5/R10/R11 remain retained or closure-only",
        },
        {
            "attempt_id": "PQ965_3_material_extension",
            "theorem_piece": "material marker extension exclusion",
            "would_need_to_show": "every nontrivial marker extension is either pure gauge, a universal auxiliary constant, stress-free topology, or absent from Conf_parent",
            "current_evidence": "423 classifies transforming material markers as legal extended theories unless no-extension is proven",
            "status": "not_proven_live_countermodel",
            "why_not_closed": "the extension can be covariant and still generate local matter pullback/source-charge/fifth-force terms",
            "consequence": "source-side zero remains a closure contract, not a theorem",
        },
        {
            "attempt_id": "PQ965_4_local_invariant_algebra",
            "theorem_piece": "local invariant algebra triviality",
            "would_need_to_show": "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor universal constants in the local vacuum branch",
            "current_evidence": "414 states the condition exactly and records extra generators",
            "status": "not_derived",
            "why_not_closed": "several independent generators are not reduced to observed geometry, constants, gauge, or zero-gradient local silence",
            "consequence": "no-marker theorem cannot be promoted locally",
        },
        {
            "attempt_id": "PQ965_5_verdict",
            "theorem_piece": "primitive quotient/no-natural-marker theorem",
            "would_need_to_show": "PQ965_0 through PQ965_4 all pass with no live marker countermodels",
            "current_evidence": "fixed spurion conditional pass exists, but primitive universal property and local invariant algebra remain unsigned",
            "status": "THEOREM_NOT_PROVEN_CURRENT_CORPUS",
            "why_not_closed": "live covariant marker and quotient-invariant scalar countermodels remain",
            "consequence": "must keep deriving generator elimination or use explicit nonclaim residual/bound route",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = "false"
        row["generated_utc"] = stamp()
    return rows


def local_invariant_algebra_audit() -> list[dict[str, str]]:
    specs = [
        ("ALG965_0_constants", "universal constants", "allowed_if_universal", False, "none if truly source-independent", "prove universal and species-independent"),
        ("ALG965_1_observed_geometry", "observed geometry jets J^k(e_obs)", "allowed_geometry", False, "EH operator selection remains separate", "use in same-frame EH/Newton branch"),
        ("ALG965_2_finite_cell_spectrum", "finite-cell fibre spectrum", "not_eliminated", True, "can act as scalar charge, mass gap, or fifth-force scale", "integrate out universally, prove constant, or retain finite residual"),
        ("ALG965_3_relative_domain_class", "relative boundary/domain class", "not_eliminated", True, "can select local branch or domain-dependent coupling", "derive physical local trivial class or fixed-class closure"),
        ("ALG965_4_domain_selector", "domain selector chi_D", "not_eliminated", True, "can become active projector or source-dependent switch", "derive selector theorem separating local vacuum from cosmology"),
        ("ALG965_5_memory_class_scalar", "memory/class scalar", "not_eliminated", True, "clock drift, gamma shift, fifth-force, or non-EH prefactor", "prove local value/gradient silence or bound the retained row"),
        ("ALG965_6_orientation_time_arrow", "orientation/time-arrow marker", "not_classified", True, "can produce preferred-frame or parity/time-asymmetry residuals", "show contained in e_obs, constant, or pure gauge"),
        ("ALG965_7_species_constants", "species/source constants", "not_universalized", True, "WEP/source-charge/clock nonuniversality", "derive constant-sector universality or retain product bounds"),
        ("ALG965_8_readout_projector", "readout projector", "no_cheat_rule_only", True, "can re-enter as reduced action term if varied too early", "prove readout-after-variation theorem"),
        ("ALG965_9_verdict", "I_loc(Q_MTS)=I_geom plus constants", "not_derived", True, "marker couplings remain technically admissible", "attack generators one by one before local-GR claim"),
    ]
    rows = []
    for generator_id, generator, status, blocks, damage, required in specs:
        rows.append(
            {
                "generator_id": generator_id,
                "generator": generator,
                "local_status": status,
                "blocks_no_marker": flag(blocks),
                "possible_damage": damage,
                "required_elimination": required,
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def marker_countermodel_review() -> list[dict[str, str]]:
    specs = [
        {
            "counter_id": "MC965_0_fixed_active_spurion",
            "countermodel": "fixed active label or projector",
            "admissibility": "conditionally_excluded",
            "why_survives_or_killed": "not a strict quotient function if the parent quotient space is proven",
            "damage": "would otherwise smuggle local projector dependence",
            "required_blocker": "strict quotient parent configuration proof",
            "current_status": "conditionally_killed_only",
        },
        {
            "counter_id": "MC965_1_comoving_material_marker",
            "countermodel": "co-moving material marker m varied with matter",
            "admissibility": "live",
            "why_survives_or_killed": "can transform covariantly and descend to an extended quotient",
            "damage": "source charge, WEP pressure, fifth-force numerator",
            "required_blocker": "primitive universal-property no-extension theorem",
            "current_status": "not_killed",
        },
        {
            "counter_id": "MC965_2_quotient_invariant_scalar",
            "countermodel": "quotient-invariant class scalar sigma(Q)",
            "admissibility": "live",
            "why_survives_or_killed": "is already a quotient function, so covariance alone does not remove it",
            "damage": "clock/gamma/fifth-force/non-EH prefactor",
            "required_blocker": "local invariant algebra triviality or local silence theorem",
            "current_status": "not_killed",
        },
        {
            "counter_id": "MC965_3_domain_class_marker",
            "countermodel": "relative/domain class marker or chi_D selector",
            "admissibility": "live",
            "why_survives_or_killed": "local trivial class has not been derived; selector could be physical rather than gauge",
            "damage": "local/cosmology split can become an unsourced branch axiom",
            "required_blocker": "domain selector theorem or fixed-class closure label",
            "current_status": "not_killed",
        },
        {
            "counter_id": "MC965_4_species_constant_marker",
            "countermodel": "species-dependent constants theta_A(I_Q)",
            "admissibility": "live",
            "why_survives_or_killed": "constant-sector universality is not proven",
            "damage": "WEP and source-charge residuals",
            "required_blocker": "constant-sector universality theorem",
            "current_status": "not_killed",
        },
        {
            "counter_id": "MC965_5_post_readout_EFT_marker",
            "countermodel": "post-readout reduced action marker",
            "admissibility": "closure_blocked_not_theorem_blocked",
            "why_survives_or_killed": "a no-cheat rule exists, but the parent readout-after-variation theorem is not fully formalized",
            "damage": "closure-zero can be mistaken for theorem-zero",
            "required_blocker": "exact parent readout-after-variation theorem",
            "current_status": "policy_blocked_only",
        },
        {
            "counter_id": "MC965_6_universal_auxiliary",
            "countermodel": "universal auxiliary field",
            "admissibility": "conditionally_safe",
            "why_survives_or_killed": "safe only if unique, source-independent, and reducing to constants after variation",
            "damage": "otherwise reappears as scalar force or non-EH operator",
            "required_blocker": "source-independent universal auxiliary solution",
            "current_status": "safe_case_not_derived",
        },
        {
            "counter_id": "MC965_7_topological_marker",
            "countermodel": "topological/boundary marker",
            "admissibility": "conditionally_safe",
            "why_survives_or_killed": "safe only if it has no local stress, no matter vertex, and no exchange/class leakage",
            "damage": "can carry boundary/domain class information",
            "required_blocker": "stress-free topological silence theorem",
            "current_status": "safe_case_not_derived",
        },
    ]
    rows = []
    for spec in specs:
        rows.append({**spec, "valid_for_claim": "false", "generated_utc": stamp()})
    return rows


def r2fr_full_curve_intake_manifest() -> list[dict[str, str]]:
    rows = [
        {
            "intake_id": "R2FC965_0_Lee2020_full_curve_required",
            "row_type": "bound_curve_target",
            "artifact_or_branch": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
            "source_url_or_path": "https://arxiv.org/abs/2002.11761",
            "lambda_value_um": "not_acquired_full_curve",
            "alpha_bound_or_predicted": "not_acquired_full_curve",
            "extraction_method": "digitize published alpha(lambda) exclusion curve or locate machine-readable table",
            "status": "full_curve_required_not_acquired",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "anchor points do not replace the bound curve needed at the MTS predicted lambda",
        },
        {
            "intake_id": "R2FC965_1_Lee2020_anchor_smoke",
            "row_type": "anchor_only_non_curve",
            "artifact_or_branch": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
            "source_url_or_path": "https://arxiv.org/abs/2002.11761",
            "lambda_value_um": "38.6",
            "alpha_bound_or_predicted": "alpha_equals_1_anchor_only",
            "extraction_method": "source-backed threshold anchor carried from 962/563 for smoke provenance only",
            "status": "anchor_recorded_nonclaim",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "not a dense curve and not sufficient for alpha(lambda) interpolation/scoring",
        },
        {
            "intake_id": "R2FC965_2_Kapner2007_anchor_smoke",
            "row_type": "anchor_only_non_curve",
            "artifact_or_branch": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
            "source_url_or_path": "https://arxiv.org/abs/hep-ph/0611184",
            "lambda_value_um": "56",
            "alpha_bound_or_predicted": "abs_alpha_less_than_or_about_1_anchor_only",
            "extraction_method": "older continuity anchor carried from 962/563 for regression sanity only",
            "status": "anchor_recorded_nonclaim",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "older single anchor cannot score a retained R2/fR or MTS finite branch",
        },
        {
            "intake_id": "R2FC965_3_MTS_R2FR_prediction_required",
            "row_type": "mts_prediction_target",
            "artifact_or_branch": "MTS_R2FR_candidate_or_retained_scalar_branch",
            "source_url_or_path": "source-intake/mts_residuals/P8_Y5_R10_962_SCALAR_BOUND_FALLBACK_ROWS.csv",
            "lambda_value_um": "not_parent_sourced",
            "alpha_bound_or_predicted": "requires_c_R2_or_fRR_normalization_screening_and_coupling",
            "extraction_method": "derive parent coefficient, scalar mass, source coupling, and screening map before scoring",
            "status": "parent_prediction_absent",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "R2/fR zero theorem not signed and finite scalar prediction lacks numeric parent inputs",
        },
        {
            "intake_id": "R2FC965_4_parent_zero_signature",
            "row_type": "zero_theorem_target",
            "artifact_or_branch": "MTS_parent_metric_second_order_minimality_route",
            "source_url_or_path": "source-intake/mts_residuals/P8_Y5_R10_964_MINIMALITY_THEOREM_ATTEMPT.csv",
            "lambda_value_um": "not_applicable_if_zero",
            "alpha_bound_or_predicted": "zero_if_primitive_no_marker_and_second_order_parent_are_signed",
            "extraction_method": "prove parent no-higher-derivative plus no-natural-marker theorem",
            "status": "zero_theorem_unsigned",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "965 theorem attempt keeps marker and scalar countermodels live",
        },
        {
            "intake_id": "R2FC965_5_runner_acceptance_rule",
            "row_type": "runner_policy",
            "artifact_or_branch": "scripts/R10_alpha_lambda_bound_prediction_runner.py",
            "source_url_or_path": "source-intake/mts_residuals/P8_Y5_R10_BOUND_CURVE_REAL_DATA_CONTRACT.csv",
            "lambda_value_um": "positive_numeric_required",
            "alpha_bound_or_predicted": "positive_numeric_bound_and_numeric_prediction_required",
            "extraction_method": "log-log interpolate only inside a sourced positive full-curve domain",
            "status": "policy_ready_inputs_absent",
            "ready_for_runner": "false",
            "valid_for_claim": "false",
            "reason_blocked": "claim stays false until bound and MTS rows are numeric, sourced, and non-placeholder",
        },
    ]
    for row in rows:
        row["generated_utc"] = stamp()
    return rows


def claim_gates() -> list[dict[str, str]]:
    specs = [
        ("G965_0_primitive_quotient", "primitive quotient parent theorem", "universal property proved with no admissible extension", "not_proven"),
        ("G965_1_no_natural_marker", "no-natural-marker theorem", "no nonconstant natural marker functor or quotient-invariant scalar remains", "not_proven"),
        ("G965_2_local_invariant_algebra", "local invariant algebra triviality", "only observed geometry jets and universal constants remain", "not_proven"),
        ("G965_3_R2FR_zero", "R2/fR theorem-zero", "parent second-order minimality and no scalar/class extension signed", "not_proven"),
        ("G965_4_R2FR_full_curve", "R2/fR finite-branch R10 score", "numeric MTS prediction plus full sourced alpha(lambda) bound curve", "inputs_absent"),
        ("G965_5_local_GR", "local GR/Newton/PPN promotion", "same-frame EH/source plus local no-marker and residual closure", "not_proven"),
    ]
    rows = []
    for gate_id, claim, required, evidence in specs:
        rows.append(
            {
                "gate_id": gate_id,
                "claim": claim,
                "required_condition": required,
                "current_evidence": evidence,
                "gate_pass": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    specs = [
        (
            "DEC965_0_theorem_result",
            "primitive quotient/no-natural-marker theorem",
            "not_proven",
            "fixed spurions are conditionally excluded, but covariant material markers and quotient-invariant scalars remain legal",
            "attack the local invariant generator list directly or keep fixed-class closure labels",
        ),
        (
            "DEC965_1_R2FR_route",
            "R2/fR scalar branch",
            "retained_nonclaim",
            "R2/fR zero is not signed and finite scalar prediction lacks parent-sourced alpha/lambda",
            "stage full-curve Lee2020 intake only as a nonclaim runner input until parent coefficients exist",
        ),
        (
            "DEC965_2_data_policy",
            "R10 bound data",
            "full_curve_required",
            "anchor-only alpha=1 thresholds are useful provenance but not scoring rows",
            "digitize or source machine-readable alpha(lambda) curve before any finite-branch R10 claim",
        ),
        (
            "DEC965_3_next_hinge",
            "best next derivation route",
            "generator_elimination_first",
            "the obstruction is now sharper than generic coupling: it is the surviving local invariant generator algebra",
            "attempt finite-cell/domain/memory/species/readout generator elimination one-by-one",
        ),
    ]
    rows = []
    for decision_id, topic, result, reason, next_action in specs:
        rows.append(
            {
                "decision_id": decision_id,
                "topic": topic,
                "result": result,
                "reason": reason,
                "next_action": next_action,
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "966-Y5-R10-local-invariant-generator-elimination-or-R2FR-curve-digitizer.md",
            "objective": "attack the surviving local invariant generators from 414 one by one; if no theorem closes, keep fixed-class closure explicit and optionally digitize the Lee2020 R10 full curve for nonclaim finite-branch pressure",
            "include": "finite-cell fibre spectrum; domain selector chi_D; memory/class scalar; species constants; readout projector; optional full-curve intake dry-run",
            "exclude": "EH/local-GR claim, invented alpha/lambda coefficients, anchor-only claim rows, GitHub action, formalization-workbench edits",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
    ]


def validation(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    algebra_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    intake_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    source_paths_ok = all(row["exists_or_recorded"] == "true" for row in sources)
    source_needles_ok = all(row["needle_found_or_na"] == "true" for row in sources)
    theorem_not_claimed = any(
        row["attempt_id"] == "PQ965_5_verdict" and row["status"] == "THEOREM_NOT_PROVEN_CURRENT_CORPUS"
        for row in theorem_rows
    )
    fixed_spurion_conditionally_killed = any(
        row["attempt_id"] == "PQ965_1_fixed_spurion" and "conditional_pass" in row["status"] for row in theorem_rows
    )
    live_marker_count = sum(1 for row in counter_rows if row["current_status"] == "not_killed")
    algebra_blockers = sum(1 for row in algebra_rows if row["blocks_no_marker"] == "true")
    full_curve_required_nonclaim = any(
        row["intake_id"] == "R2FC965_0_Lee2020_full_curve_required"
        and row["status"] == "full_curve_required_not_acquired"
        and row["valid_for_claim"] == "false"
        for row in intake_rows
    )
    all_intake_nonclaim = all(row["valid_for_claim"] == "false" and row["ready_for_runner"] == "false" for row in intake_rows)
    no_claim_gates = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in decision_rows)
    target_written = bool(target_rows) and target_rows[0]["valid_for_claim"] == "false"
    no_placeholder_claim_rows = all(
        not (
            row.get("valid_for_claim") == "true"
            and any("MISSING" in str(value) or "not_acquired" in str(value) or "not_parent_sourced" in str(value) for value in row.values())
        )
        for row in [*intake_rows, *claim_rows, *decision_rows]
    )
    no_formalization_edits = formalization_changed_after_start() == 0
    rows = []
    checks = [
        ("V965_0_source_paths_or_urls_recorded", source_paths_ok, "all local sources exist and web source strings are recorded"),
        ("V965_1_source_needles_found", source_needles_ok, "all local source needles found; web rows marked url_recorded"),
        ("V965_2_theorem_not_overclaimed", theorem_not_claimed, "primitive quotient/no-natural-marker theorem is explicitly not proven"),
        ("V965_3_fixed_spurion_partial_result", fixed_spurion_conditionally_killed, "fixed active spurion conditional exclusion retained"),
        ("V965_4_marker_countermodels_live", live_marker_count >= 4, f"{live_marker_count} live marker countermodels remain"),
        ("V965_5_algebra_blockers_recorded", algebra_blockers >= 6, f"{algebra_blockers} local invariant generators still block no-marker theorem"),
        ("V965_6_full_curve_nonclaim_staged", full_curve_required_nonclaim, "Lee2020 full-curve intake target staged without claim"),
        ("V965_7_all_intake_rows_nonclaim", all_intake_nonclaim, "all R2/fR intake rows remain nonclaim and runner-blocked"),
        ("V965_8_claim_gates_false", no_claim_gates, "no R10, R2/fR, local-GR, or EH claim gate passes"),
        ("V965_9_decisions_nonclaim", decisions_nonclaim, "decision rows do not claim evidence"),
        ("V965_10_no_placeholder_claim_rows", no_placeholder_claim_rows, "no placeholder or not-acquired row is valid_for_claim=true"),
        ("V965_11_next_target_written", target_written, "966 next target selected"),
        ("V965_12_formalization_untouched", no_formalization_edits, "formalization-workbench modified-file count since script start is zero"),
    ]
    for check_id, result, detail in checks:
        rows.append(
            {
                "check_id": check_id,
                "result": "pass" if result else "fail",
                "detail": detail,
                "generated_utc": stamp(),
            }
        )
    rows.append(
        {
            "check_id": "V965_13_validation_rows_ready",
            "result": "pass" if all(row["result"] == "pass" for row in rows) else "fail",
            "detail": "965 validation pack assembled",
            "generated_utc": stamp(),
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    algebra_rows: list[dict[str, str]],
    counter_rows: list[dict[str, str]],
    intake_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 965 Y5 R10: Primitive Quotient No-Natural-Marker Theorem Or R2/fR Full-Curve Intake

Status: `Y5_R10_965_primitive_quotient_no_marker_theorem_not_proven_R2FR_full_curve_intake_staged_nonclaim`

Claim ceiling: no primitive quotient theorem, no no-natural-marker theorem, no R2/fR zero, no R10 pass, no PPN pass, no EH/Newton/local-GR claim is made.

## Readout

This was the clean derivation-first shot. It partly bites: a fixed active spurion is still conditionally excluded by strict quotient logic. But the theorem does not close, because a co-moving material marker, quotient-invariant class scalar, domain selector, species constant, or post-readout reduced-action marker can remain covariant unless the parent object is proven primitive-minimal.

So the obstruction is no longer vague "coupling trouble". It is the local invariant algebra: MTS must prove that the local quotient has no matter-visible generators beyond observed geometry jets and universal constants, or else those generators must be retained as explicit residual/closure rows.

The R2/fR branch is therefore kept honest: no zero claim, no finite-branch score, and no anchor-only R10 pass. The full Lee2020 alpha(lambda) curve is staged as a future nonclaim intake target only.

## Source Register

{md_table(sources, ["source_id", "path_type", "role", "exists_or_recorded", "needle_found_or_na", "path"])}

## Primitive Quotient / No-Natural-Marker Theorem Attempt

{md_table(theorem_rows, ["attempt_id", "theorem_piece", "status", "why_not_closed", "consequence"])}

## Local Invariant Algebra Audit

{md_table(algebra_rows, ["generator_id", "generator", "local_status", "blocks_no_marker", "possible_damage", "required_elimination"])}

## Marker Countermodel Review

{md_table(counter_rows, ["counter_id", "countermodel", "admissibility", "current_status", "damage", "required_blocker"])}

## R2/fR Full-Curve Intake Manifest

{md_table(intake_rows, ["intake_id", "row_type", "artifact_or_branch", "lambda_value_um", "alpha_bound_or_predicted", "status", "valid_for_claim"])}

## Claim Gate

{md_table(claim_rows, ["gate_id", "claim", "current_evidence", "gate_pass", "claim_allowed"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "topic", "result", "reason", "next_action"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

{md_table(target_rows, ["next_target", "objective", "include", "exclude", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    sources = source_register()
    theorem_rows = primitive_quotient_theorem_attempt()
    algebra_rows = local_invariant_algebra_audit()
    counter_rows = marker_countermodel_review()
    intake_rows = r2fr_full_curve_intake_manifest()
    claim_rows = claim_gates()
    decision_rows = decisions()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        theorem_rows,
        algebra_rows,
        counter_rows,
        intake_rows,
        claim_rows,
        decision_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_965_SOURCE_REGISTER.csv",
        sources,
        [
            "source_id",
            "path_type",
            "path",
            "role",
            "needle",
            "absolute_path",
            "exists_or_recorded",
            "needle_found_or_na",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_965_PRIMITIVE_QUOTIENT_THEOREM_ATTEMPT.csv",
        theorem_rows,
        [
            "attempt_id",
            "theorem_piece",
            "would_need_to_show",
            "current_evidence",
            "status",
            "why_not_closed",
            "consequence",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_965_LOCAL_INVARIANT_ALGEBRA_AUDIT.csv",
        algebra_rows,
        [
            "generator_id",
            "generator",
            "local_status",
            "blocks_no_marker",
            "possible_damage",
            "required_elimination",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_965_MARKER_COUNTERMODEL_REVIEW.csv",
        counter_rows,
        [
            "counter_id",
            "countermodel",
            "admissibility",
            "why_survives_or_killed",
            "damage",
            "required_blocker",
            "current_status",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_965_R2FR_FULL_CURVE_INTAKE_MANIFEST.csv",
        intake_rows,
        [
            "intake_id",
            "row_type",
            "artifact_or_branch",
            "source_url_or_path",
            "lambda_value_um",
            "alpha_bound_or_predicted",
            "extraction_method",
            "status",
            "ready_for_runner",
            "valid_for_claim",
            "reason_blocked",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_965_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_965_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_965_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_965_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, theorem_rows, algebra_rows, counter_rows, intake_rows, claim_rows, decision_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
