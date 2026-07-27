from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "953-Y5-R10-no-species-label-source-functor-theorem-or-filled-coefficient-intake-review.md"
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
            "source_id": "952_doc",
            "path": "952-Y5-R10-single-source-coupling-selection-principle-or-coefficient-intake-template.md",
            "role": "handoff: Ward alone not enough; no-species-label naturality is target",
            "needle": "no-species-label naturality",
        },
        {
            "source_id": "952_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_952_VALIDATION.csv",
            "role": "previous checkpoint validation",
            "needle": "V952_11_validation_rows_ready",
        },
        {
            "source_id": "952_selection_attempt",
            "path": "source-intake/mts_residuals/P8_Y5_R10_952_SINGLE_SOURCE_SELECTION_ATTEMPT.csv",
            "role": "single-source coupling target and Ward counterpoint",
            "needle": "SSC952_2_no_species_label_naturality",
        },
        {
            "source_id": "952_intake_template",
            "path": "source-intake/mts_residuals/P8_Y5_R10_952_COEFFICIENT_INTAKE_TEMPLATE.csv",
            "role": "filled coefficient intake source for review",
            "needle": "CIT952_4_zero_theorem_switch",
        },
        {
            "source_id": "951_Ward_action",
            "path": "source-intake/mts_residuals/P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv",
            "role": "Ward bridge and species-weight countermodel",
            "needle": "SWA951_3_species_weight_countermodel",
        },
        {
            "source_id": "no_species_contract",
            "path": "source-intake/mts_residuals/P8_no_species_source_charge_CONTRACT.csv",
            "role": "no-marker/no-species source contract clauses",
            "needle": "S4_source_normalization_species_blind",
        },
        {
            "source_id": "763_no_marker_spurion",
            "path": "source-intake/mts_residuals/P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
            "role": "universal source weight blocker",
            "needle": "NMS763_3_universal_source_weight",
        },
        {
            "source_id": "631_source_test_charge",
            "path": "source-intake/mts_residuals/P8_Y5_R10_631_SOURCE_TEST_CHARGE_LAW.csv",
            "role": "composition/source charge branch still open if labels remain",
            "needle": "Q631_2_composition_channel",
        },
        {
            "source_id": "951_provenance_dryrun",
            "path": "source-intake/mts_residuals/P8_Y5_R10_951_PROVENANCE_GATE_DRYRUN.csv",
            "role": "prior coefficient dryrun rejection baseline",
            "needle": "PGD951_2_WEP_surface_beta_source",
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


def source_functor_theorem_attempt() -> list[dict[str, str]]:
    return [
        {
            "theorem_id": "NSF953_0_problem",
            "claim_shape": "derive one universal source coupling without importing WEP as an empirical axiom",
            "mathematical_form": "F_src({T_A}) ?= kappa_univ sum_A T_A",
            "status": "target_restated",
            "conditional_result": "would close beta_source_normalized only if relative kappa_A are structurally forbidden",
            "blocker": "Ward symmetry conserves species-weighted sums too",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF953_1_domain_fork",
            "claim_shape": "the source functor domain must forget species labels before coupling selection",
            "mathematical_form": "Obj(C_matter)->T_total, not Obj(C_matter)->(T_A,A)",
            "status": "critical_parent_category_fork",
            "conditional_result": "if A labels survive as source-functor data, kappa_A remains allowed",
            "blocker": "current parent corpus has not signed the label-forgetting quotient",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF953_2_conditional_uniqueness",
            "claim_shape": "covariant additive source functor of one observed coframe and no species labels is unique up to one scalar",
            "mathematical_form": "F_src(T_1+...+T_N)=kappa_univ(T_1+...+T_N)",
            "status": "conditional_theorem_clean",
            "conditional_result": "relative source weights kappa_A/kappa_B cannot be formed because A,B are not available arguments",
            "blocker": "no-species-label premise is exactly the unproved parent clause",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF953_3_additivity_limit",
            "claim_shape": "additivity removes nonlinear source mixing but not labelled constants",
            "mathematical_form": "F(T_A+T_B)=F(T_A)+F(T_B)",
            "status": "valid_but_insufficient_alone",
            "conditional_result": "excludes terms such as T_A T_B from the source map",
            "blocker": "F((T_A,A))=kappa_A T_A is still additive when labels remain",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF953_4_calibration_limit",
            "claim_shape": "measured G fixes only the common source normalization",
            "mathematical_form": "kappa_univ absorbed into G_ref; kappa_A/kappa_B invariant",
            "status": "valid_common_mode_only",
            "conditional_result": "one scalar can be calibrated away after the theorem",
            "blocker": "relative source weights are physical WEP-sensitive residuals",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "theorem_id": "NSF953_5_verdict",
            "claim_shape": "no-species-label source-functor theorem",
            "mathematical_form": "one observed coframe + source label-forgetting + covariance + additivity => one kappa_univ",
            "status": "conditional_proof_not_parent_derivation",
            "conditional_result": "mathematical route is sharp enough to use as a parent-action contract",
            "blocker": "the parent action/category must still prove or explicitly adopt label-forgetting",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def parent_category_contract() -> list[dict[str, str]]:
    return [
        {
            "clause_id": "PMC953_0_one_observed_coframe",
            "required_parent_clause": "all ordinary matter couples through one observed coframe before source extraction",
            "mathematical_form": "S_A=S_A[Psi_A,e_obs,omega[e_obs],theta_univ]",
            "role": "prevents frame-dependent source weights",
            "current_status": "partially_named_by_prior_contract",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PMC953_1_label_forgetting_quotient",
            "required_parent_clause": "the source functor sees the total Hilbert current, not a labelled family of species currents",
            "mathematical_form": "q_src({(T_A,A)})=T_total=sum_A T_A",
            "role": "kills relative kappa_A at the source-map domain level",
            "current_status": "exact_missing_clause",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PMC953_2_natural_additive_map",
            "required_parent_clause": "the source map is natural, covariant, linear/additive, and local in the observed coframe data",
            "mathematical_form": "F_src(phi_*T)=phi_*F_src(T), F_src(T+U)=F_src(T)+F_src(U)",
            "role": "turns the label-forgotten source into one scalar multiple of the Hilbert current",
            "current_status": "conditional_mathematics_clear",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PMC953_3_no_hidden_source_spurion",
            "required_parent_clause": "no hidden constants, masks, material markers, boundary classes, or post-readout maps reintroduce species dependence",
            "mathematical_form": "partial_A kappa=partial_m kappa=partial_boundary kappa=0",
            "role": "prevents a disguised kappa_A after label-forgetting",
            "current_status": "named_but_not_parent_signed",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PMC953_4_common_G_calibration",
            "required_parent_clause": "after uniqueness, the remaining scalar is calibrated by measured G rather than treated as a new composition field",
            "mathematical_form": "kappa_univ <-> 8 pi G_ref/c^4",
            "role": "turns the common mode into units/normalization",
            "current_status": "available_only_after_uniqueness",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "clause_id": "PMC953_5_contract_verdict",
            "required_parent_clause": "parent matter category must be label-forgetting at the source stage",
            "mathematical_form": "C_parent -> C_source forgets A before F_src is formed",
            "role": "the next derivation target",
            "current_status": "not_closed_current_corpus",
            "parent_signed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def countermodel_ledger() -> list[dict[str, str]]:
    return [
        {
            "countermodel_id": "CM953_0_labelled_additive_functor",
            "countermodel": "species labels remain source-map arguments",
            "mathematical_form": "F_src({(T_A,A)})=sum_A kappa_A T_A",
            "survives_ward": "true",
            "survives_additivity": "true",
            "excluded_by_current_parent": "false",
            "lesson": "Ward plus additivity cannot by itself prove universal coupling",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM953_1_constant_spurion_weights",
            "countermodel": "constant hidden species weights ride as superselection/spurion data",
            "mathematical_form": "kappa_A=kappa_0(1+epsilon s_A), partial_mu s_A=0",
            "survives_ward": "true",
            "survives_additivity": "true",
            "excluded_by_current_parent": "false",
            "lesson": "coordinate covariance does not remove constant species labels",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM953_2_composite_binding_sensitivity",
            "countermodel": "effective source mass includes composition-dependent binding response",
            "mathematical_form": "mu_A=mu_0+Delta mu_EM(A)+Delta mu_surface(A)",
            "survives_ward": "true",
            "survives_additivity": "conditional",
            "excluded_by_current_parent": "false",
            "lesson": "composite matter can reopen beta_source unless constants/source charges are also source-blind",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM953_3_boundary_or_nonHilbert_current",
            "countermodel": "boundary, torsion, spin, or non-Hilbert source current carries material labels",
            "mathematical_form": "J_src=kappa T_total+J_NH[A,boundary]",
            "survives_ward": "conditional",
            "survives_additivity": "conditional",
            "excluded_by_current_parent": "false",
            "lesson": "the theorem must specify Hilbert/coframe current only or separately kill non-Hilbert currents",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "countermodel_id": "CM953_4_verdict",
            "countermodel": "single-coupling theorem is conditional unless parent category excludes all label-carrying data",
            "mathematical_form": "not(parent_forgets_A) => exists F_src with kappa_A",
            "survives_ward": "true",
            "survives_additivity": "true",
            "excluded_by_current_parent": "false",
            "lesson": "next route must prove the label-forgetting quotient, not merely restate universality",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def filled_intake_review() -> list[dict[str, str]]:
    rows = []
    for source in read_csv(OUT / "P8_Y5_R10_952_COEFFICIENT_INTAKE_TEMPLATE.csv"):
        candidate_path = source.get("candidate_source_path", "")
        candidate_path_exists = bool(candidate_path) and not candidate_path.startswith("MISSING") and (ROOT / candidate_path).exists()
        missing = [
            field
            for field in [
                "candidate_value",
                "candidate_source_path",
                "source_row_id",
                "derivation_status",
            ]
            if source.get(field, "").startswith("MISSING")
        ]
        accepted = not missing and candidate_path_exists
        rows.append(
            {
                "review_id": source["intake_id"].replace("CIT952", "FIR953"),
                "coefficient_symbol": source["coefficient_symbol"],
                "arena": source["arena"],
                "candidate_value": source["candidate_value"],
                "candidate_source_path": candidate_path,
                "candidate_path_exists": flag(candidate_path_exists),
                "source_row_id": source["source_row_id"],
                "derivation_status": source["derivation_status"],
                "missing_fields": ";".join(missing),
                "accepted_for_951_gate": flag(accepted),
                "verdict": "READY_FOR_951_GATE_NONCLAIM" if accepted else "REJECTED_NOT_FILLED",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC953_0_conditional_theorem",
            "topic": "no-species-label source functor",
            "result": "conditional_uniqueness_proof_clean_but_not_parent_signed",
            "reason": "if the parent source category forgets species labels and admits only a covariant additive Hilbert-current map, relative kappa_A cannot be formed",
            "next_action": "derive the parent label-forgetting quotient or demote it to an explicit closure axiom",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC953_1_countermodel",
            "topic": "species-labelled source functor",
            "result": "countermodel_remains_open",
            "reason": "F_src({(T_A,A)})=sum_A kappa_A T_A is covariant, additive, and Ward-compatible if labels remain",
            "next_action": "attack the existence of species labels in the parent source domain rather than Ward conservation",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC953_2_filled_intake",
            "topic": "coefficient intake review",
            "result": "no_filled_rows_available",
            "reason": "all 952 intake rows still contain missing parent values or missing source paths",
            "next_action": "do not score finite coefficients until a row has real value, source path, row id, derivation status, units, and bound link",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE953_0_single_source_coupling",
            "claim": "parent action forces one universal source coupling",
            "required_condition": "parent-signed label-forgetting source category plus no hidden source spurions",
            "current_evidence": "conditional theorem only",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE953_1_finite_coefficient_scoring",
            "claim": "finite coefficient rows can be scored against clock/WEP bounds",
            "required_condition": "filled intake row passes 952 intake and 951 provenance gate",
            "current_evidence": "all intake rows rejected as unfilled placeholders",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE953_2_local_GR_or_WEP",
            "claim": "R10/WEP/local-GR source-coupling branch passes",
            "required_condition": "single-source theorem parent-signed or finite source residuals bounded with full provenance",
            "current_evidence": "neither route is closed",
            "gate_pass": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def next_target() -> list[dict[str, str]]:
    return [
        {
            "next_target": "954-Y5-R10-parent-matter-category-no-species-label-clause-or-source-functor-countermodel-bound.md",
            "objective": "try to derive the parent label-forgetting matter/source category clause; if it fails, convert the species-labelled source functor into an explicit finite bound target",
            "include": "parent quotient map, matter category objects, source functor domain, Hilbert-current restriction, no hidden source spurions, countermodel bound route",
            "exclude": "GitHub action, invented coefficient values, WEP/local-GR claim, formalization-workbench edits",
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
    theorem_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    countermodel_rows: list[dict[str, str]],
    intake_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    def add(check_id: str, passes: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passes else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_clean = all(row.get("result") == "pass" for row in read_csv(OUT / "P8_Y5_BRR545_952_VALIDATION.csv"))
    conditional_theorem_clean = any(
        row["theorem_id"] == "NSF953_5_verdict" and row["status"] == "conditional_proof_not_parent_derivation"
        for row in theorem_rows
    )
    exact_missing_clause_named = any(
        row["clause_id"] == "PMC953_1_label_forgetting_quotient" and row["current_status"] == "exact_missing_clause"
        for row in contract_rows
    )
    countermodel_open = any(
        row["countermodel_id"] == "CM953_4_verdict" and row["excluded_by_current_parent"] == "false"
        for row in countermodel_rows
    )
    intake_rejected = len(intake_rows) == 5 and all(row["accepted_for_951_gate"] == "false" and row["verdict"] == "REJECTED_NOT_FILLED" for row in intake_rows)
    decisions_nonclaim = all(row["claim_allowed"] == "false" for row in decision_rows)
    claim_gates_false = all(row["gate_pass"] == "false" and row["claim_allowed"] == "false" for row in claim_rows)
    target_selected = bool(target_rows) and target_rows[0]["next_target"].startswith("954-")
    valid_for_claim_false = all(
        row.get("valid_for_claim") == "false"
        for table in [sources, theorem_rows, contract_rows, countermodel_rows, intake_rows, decision_rows, claim_rows, target_rows]
        for row in table
    )
    formalization_changed = formalization_changed_after_start()

    add("V953_0_sources_exist_and_needles", sources_ok, "all 953 source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V953_1_prior_952_clean", prior_clean, "P8_Y5_BRR545_952_VALIDATION.csv clean")
    add("V953_2_conditional_theorem_clean", conditional_theorem_clean, "conditional no-species-label uniqueness theorem written")
    add("V953_3_exact_missing_clause_named", exact_missing_clause_named, "parent label-forgetting quotient identified as exact missing clause")
    add("V953_4_countermodel_remains_open", countermodel_open, "species-labelled additive functor countermodel remains open")
    add("V953_5_intake_review_rejects_unfilled_rows", intake_rejected, "all 952 intake rows remain rejected until filled")
    add("V953_6_decisions_nonclaim", decisions_nonclaim, "decision ledger remains nonclaim")
    add("V953_7_claim_gates_false", claim_gates_false, "all claim gates remain false")
    add("V953_8_next_target_selected", target_selected, "954 parent matter category clause or bound target selected")
    add("V953_9_no_claims_promoted", valid_for_claim_false, "all generated rows are valid_for_claim=false")
    add("V953_10_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V953_11_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    theorem_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    countermodel_rows: list[dict[str, str]],
    intake_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    target_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    doc = f"""# 953 Y5 R10: No-Species-Label Source-Functor Theorem Or Filled Coefficient Intake Review

Status: `Y5_R10_953_conditional_source_functor_theorem_clean_parent_label_forgetting_unsigned_nonclaim`

Claim ceiling: `conditional_theorem_only_no_single_kappa_claim_no_WEP_claim_no_local_GR_claim`

## Result

This checkpoint pushes the coupling problem into its cleanest shape.

The good news: the theorem route is now sharp. If the parent matter/source category first forgets species labels and the source functor is covariant, additive, local in one observed coframe, and restricted to the Hilbert/coframe current, then the only possible source normalization is one common scalar `kappa_univ` multiplying the total Hilbert current. In that conditional branch, relative weights `kappa_A/kappa_B` cannot even be written because the labels `A,B` are not source-functor arguments.

The bad news, but useful bad news: this is not yet a parent derivation. If species labels remain in the source domain, the countermodel `F_src({{(T_A,A)}})=sum_A kappa_A T_A` is still covariant, additive, and Ward-compatible. So the next derivation must attack the parent category/quotient, not Ward conservation.

The coefficient route remains locked. The 952 intake rows are still placeholders, so nothing can be scored.

```text
conditional win: no species labels => one kappa_univ;
open wound: prove the parent source domain forgets labels;
finite fallback: still no filled coefficient rows.
```

## Source Register

{md_table(sources, ["source_id", "role", "exists", "needle_found", "path"])}

## Source-Functor Theorem Attempt

{md_table(theorem_rows, ["theorem_id", "claim_shape", "status", "conditional_result", "blocker", "parent_signed"])}

## Parent Category Contract

{md_table(contract_rows, ["clause_id", "required_parent_clause", "role", "current_status", "parent_signed"])}

## Countermodel Ledger

{md_table(countermodel_rows, ["countermodel_id", "countermodel", "survives_ward", "survives_additivity", "excluded_by_current_parent", "lesson"])}

## Filled Intake Review

{md_table(intake_rows, ["review_id", "coefficient_symbol", "arena", "candidate_value", "candidate_path_exists", "missing_fields", "accepted_for_951_gate", "verdict"])}

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
    theorem_rows = source_functor_theorem_attempt()
    contract_rows = parent_category_contract()
    countermodel_rows = countermodel_ledger()
    intake_rows = filled_intake_review()
    decision_rows = decisions()
    claim_rows = claim_gates()
    target_rows = next_target()
    validation_rows = validation(
        sources,
        theorem_rows,
        contract_rows,
        countermodel_rows,
        intake_rows,
        decision_rows,
        claim_rows,
        target_rows,
    )

    write_csv(
        OUT / "P8_Y5_R10_953_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "role", "needle", "absolute_path", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
        theorem_rows,
        [
            "theorem_id",
            "claim_shape",
            "mathematical_form",
            "status",
            "conditional_result",
            "blocker",
            "parent_signed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_953_PARENT_CATEGORY_CONTRACT.csv",
        contract_rows,
        [
            "clause_id",
            "required_parent_clause",
            "mathematical_form",
            "role",
            "current_status",
            "parent_signed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_953_COUNTERMODEL_LEDGER.csv",
        countermodel_rows,
        [
            "countermodel_id",
            "countermodel",
            "mathematical_form",
            "survives_ward",
            "survives_additivity",
            "excluded_by_current_parent",
            "lesson",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_953_FILLED_INTAKE_REVIEW.csv",
        intake_rows,
        [
            "review_id",
            "coefficient_symbol",
            "arena",
            "candidate_value",
            "candidate_source_path",
            "candidate_path_exists",
            "source_row_id",
            "derivation_status",
            "missing_fields",
            "accepted_for_951_gate",
            "verdict",
            "claim_allowed",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        OUT / "P8_Y5_R10_953_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "topic", "result", "reason", "next_action", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_953_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "required_condition", "current_evidence", "gate_pass", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_953_NEXT_TARGET.csv",
        target_rows,
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_953_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, theorem_rows, contract_rows, countermodel_rows, intake_rows, decision_rows, claim_rows, target_rows, validation_rows)


if __name__ == "__main__":
    main()
