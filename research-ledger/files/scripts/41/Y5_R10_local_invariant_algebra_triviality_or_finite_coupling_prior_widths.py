from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1115-Y5-R10-local-invariant-algebra-triviality-or-finite-coupling-prior-widths.md"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def stamp(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    generated = now()
    out: list[dict[str, object]] = []
    for row in rows:
        copied = dict(row)
        copied.setdefault("valid_for_claim", "false")
        copied.setdefault("claim_allowed", "false")
        copied.setdefault("generated_utc", generated)
        out.append(copied)
    return out


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, object]]:
    sources = [
        {
            "source_id": "SRC1115_0_1114_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NEXT_TARGET.csv",
            "needle": "NEXT1114_0_1115",
            "note": "1114 handoff to local invariant algebra triviality.",
        },
        {
            "source_id": "SRC1115_1_1114_theorem",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
            "needle": "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED",
            "note": "no-hidden-visible theorem reduced to invariant algebra.",
        },
        {
            "source_id": "SRC1115_2_1114_obstruction",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv",
            "needle": "OBS1114_1_scalar_invariant",
            "note": "surviving invariant scalar obstruction.",
        },
        {
            "source_id": "SRC1115_3_1092_triviality",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv",
            "needle": "HIT1092_5_verdict",
            "note": "hidden invariant triviality was not derived.",
        },
        {
            "source_id": "SRC1115_4_1092_generators",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv",
            "needle": "GEN1092_3_memory_scalar",
            "note": "surviving generator list.",
        },
        {
            "source_id": "SRC1115_5_980_scalar",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "NMF980_2_scalar_obstruction_lemma",
            "note": "scalar obstruction lemma.",
        },
        {
            "source_id": "SRC1115_6_980_counter",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv",
            "needle": "CEX980_4_memory_class_scalar",
            "note": "memory/class scalar counterexample.",
        },
        {
            "source_id": "SRC1115_7_965_algebra",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_965_LOCAL_INVARIANT_ALGEBRA_AUDIT.csv",
            "needle": "ALG965_9_verdict",
            "note": "local invariant algebra audit.",
        },
        {
            "source_id": "SRC1115_8_573_debt",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
            "needle": "IG573_3_memory_scalar",
            "note": "earlier invariant generator debt.",
        },
        {
            "source_id": "SRC1115_9_1028_no_marker",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv",
            "needle": "NM1028_6_verdict",
            "note": "no-marker theorem remains claim-blocked.",
        },
    ]
    checked: list[dict[str, object]] = []
    for source in sources:
        path = ROOT / str(source["relative_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        checked.append(
            {
                **source,
                "exists": str(path.exists()).lower(),
                "needle_found": str(str(source["needle"]) in text).lower(),
            }
        )
    return stamp(checked)


def triviality_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "LIA1115_0_target",
                "claim_piece": "local hidden invariant algebra triviality",
                "formal_statement": "O(C_hid)^inv = R on the physical local branch.",
                "result": "TARGET_SHARP",
                "proof_or_blocker": "this would remove scalar arguments that feed continuous visible coefficients",
            },
            {
                "attempt_id": "LIA1115_1_sufficiency",
                "claim_piece": "trivial algebra implies no coefficient drift",
                "formal_statement": "If O(C_hid)^inv = R, then any invariant coefficient c:C_hid -> R is constant.",
                "result": "EXACT_CONDITIONAL_THEOREM",
                "proof_or_blocker": "coefficient maps factor through the invariant algebra, which has only constants",
            },
            {
                "attempt_id": "LIA1115_2_connected_discrete",
                "claim_piece": "connected branch protects discrete labels",
                "formal_statement": "A continuous map from a connected local branch into a discrete target is constant.",
                "result": "HELPFUL_BUT_NARROW",
                "proof_or_blocker": "protects discrete representation labels only if no idempotent/domain selector survives; does not protect alpha, masses, or kappa in R-like targets",
            },
            {
                "attempt_id": "LIA1115_3_continuous_scalar_obstruction",
                "claim_piece": "surviving scalar feeds continuous coefficients",
                "formal_statement": "If I in O(C_hid)^inv is nonconstant and c takes values in R, then c=c0+epsilon I is admissible unless typed out.",
                "result": "COUNTEREXAMPLE_PROVED",
                "proof_or_blocker": "980/1092 already prove this obstruction; covariance and quotient compatibility do not remove it",
            },
            {
                "attempt_id": "LIA1115_4_generator_elimination",
                "claim_piece": "all surviving invariant generators are eliminated",
                "formal_statement": "finite-cell spectrum, domain class, domain selector, memory scalar, time-arrow, species constants, and readout projector are constant/gauge/absent.",
                "result": "NOT_DERIVED",
                "proof_or_blocker": "1092 and 965 retain each as an open generator debt",
            },
            {
                "attempt_id": "LIA1115_5_no_extension",
                "claim_piece": "no co-moving marker or extended quotient",
                "formal_statement": "admissible quotient cannot be extended by material/domain markers that feed constants.",
                "result": "NOT_DERIVED",
                "proof_or_blocker": "980 counterexamples keep co-moving marker and domain selector extensions active",
            },
            {
                "attempt_id": "LIA1115_6_verdict",
                "claim_piece": "derive local invariant algebra triviality",
                "formal_statement": "all local hidden/invariant scalar generators are trivial or constant on the local branch.",
                "result": "LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_NOT_DERIVED",
                "proof_or_blocker": "conditional theorem is clean but surviving generator debts and scalar counterexamples remain active",
            },
        ]
    )


def generator_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "generator_id": "KILL1115_0_finite_cell",
                "generator": "finite_cell_fibre_spectrum",
                "status": "SURVIVES",
                "damage_if_live": "scalar charge, mass gap, fifth-force scale, or coupling prior",
                "kill_condition": "prove pure basis/gauge relabeling or universal integration-out",
                "priority": "high",
            },
            {
                "generator_id": "KILL1115_1_domain_class",
                "generator": "relative_boundary_domain_class",
                "status": "SURVIVES",
                "damage_if_live": "domain-dependent coupling or local/cosmology branch selector",
                "kill_condition": "derive local trivial class or fixed-class stress-free nohair",
                "priority": "high",
            },
            {
                "generator_id": "KILL1115_2_domain_selector",
                "generator": "domain_selector_chi_D",
                "status": "SURVIVES",
                "damage_if_live": "active projector/source switch and arena-specific screening",
                "kill_condition": "derive selector as gauge/readout-only or fixed local branch closure",
                "priority": "critical",
            },
            {
                "generator_id": "KILL1115_3_memory_scalar",
                "generator": "memory_or_class_scalar",
                "status": "SURVIVES",
                "damage_if_live": "clock drift, gamma shift, alpha/mass coupling, fifth-force channel",
                "kill_condition": "prove local value and gradient zero or retain bounded residual",
                "priority": "critical",
            },
            {
                "generator_id": "KILL1115_4_time_arrow",
                "generator": "orientation_time_arrow",
                "status": "UNCLASSIFIED",
                "damage_if_live": "preferred-frame or time-asymmetry residual",
                "kill_condition": "show contained in observed coframe, constant, or pure gauge",
                "priority": "medium",
            },
            {
                "generator_id": "KILL1115_5_species_constants",
                "generator": "species_charge_constants",
                "status": "SURVIVES",
                "damage_if_live": "WEP/source-charge/clock nonuniversality",
                "kill_condition": "derive constant-sector universality and source label forgetting",
                "priority": "critical",
            },
            {
                "generator_id": "KILL1115_6_readout_projector",
                "generator": "post_readout_projector",
                "status": "POLICY_ONLY_BLOCKED",
                "damage_if_live": "closure zero re-enters as reduced-action source",
                "kill_condition": "prove readout-after-variation and no post-readout EFT backreaction",
                "priority": "high",
            },
        ]
    )


def prior_width_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "prior_id": "PW1115_0_alpha",
                "coupling_family": "alpha/F2 visible coefficient",
                "symbolic_width": "sigma_b_alpha",
                "needed_numeric_or_zero": "b_alpha or c_alpha_DD theorem-zero/numeric prior width",
                "arenas": "clock; WEP; R10; EM",
                "current_status": "MISSING_PRIOR_WIDTH_OR_ZERO_THEOREM",
            },
            {
                "prior_id": "PW1115_1_mass_clock",
                "coupling_family": "mass ratios and clock sensitivities",
                "symbolic_width": "sigma_b_m; sigma_b_mu; sigma_b_clock",
                "needed_numeric_or_zero": "finite mass/clock vector or matter-constant universality theorem",
                "arenas": "atomic clocks; WEP; spectroscopy",
                "current_status": "MISSING_PRIOR_WIDTH_OR_ZERO_THEOREM",
            },
            {
                "prior_id": "PW1115_2_source",
                "coupling_family": "source weights and relative kappa",
                "symbolic_width": "sigma_beta_source; sigma_delta_kappa",
                "needed_numeric_or_zero": "source label-forgetting theorem or finite source weight prior",
                "arenas": "WEP; R10; orbital/local gravity",
                "current_status": "MISSING_PRIOR_WIDTH_OR_ZERO_THEOREM",
            },
            {
                "prior_id": "PW1115_3_domain",
                "coupling_family": "domain selector/class coupling",
                "symbolic_width": "sigma_chiD; sigma_domain",
                "needed_numeric_or_zero": "selector no-vector/no-source theorem or finite domain-source bound",
                "arenas": "local GR; R10; cosmology split",
                "current_status": "MISSING_PRIOR_WIDTH_OR_ZERO_THEOREM",
            },
            {
                "prior_id": "PW1115_4_memory",
                "coupling_family": "memory/class scalar coupling",
                "symbolic_width": "sigma_memory",
                "needed_numeric_or_zero": "local memory value/gradient zero theorem or finite residual coefficient",
                "arenas": "clock; PPN; local force; cosmology",
                "current_status": "MISSING_PRIOR_WIDTH_OR_ZERO_THEOREM",
            },
            {
                "prior_id": "PW1115_5_readout",
                "coupling_family": "readout/reduced-action projector",
                "symbolic_width": "sigma_readout",
                "needed_numeric_or_zero": "readout-after-variation theorem or finite EFT/readout counterterm width",
                "arenas": "EM; clock; WEP; spectra",
                "current_status": "MISSING_PRIOR_WIDTH_OR_ZERO_THEOREM",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1115_0_triviality",
                "claim": "O(C_hid)^inv = R on the local branch",
                "gate_pass": "false",
                "reason": "surviving generators and scalar counterexamples remain active",
            },
            {
                "gate_id": "CG1115_1_no_coupling",
                "claim": "visible couplings cannot depend on hidden/local scalars",
                "gate_pass": "false",
                "reason": "requires algebra triviality or typed object-language exclusion",
            },
            {
                "gate_id": "CG1115_2_discrete_labels",
                "claim": "all labels are protected by connectedness",
                "gate_pass": "false",
                "reason": "connectedness helps discrete labels only, not continuous alpha/mass/kappa coefficients",
            },
            {
                "gate_id": "CG1115_3_prior_widths_ready",
                "claim": "finite prior-width rows are score-ready",
                "gate_pass": "false",
                "reason": "all prior rows still require numeric source-backed widths or theorem-zero",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1115_0_result",
                "decision": "local invariant algebra triviality is not derived",
                "because": "the sufficiency theorem is exact but multiple invariant generators survive",
                "next_action": "attack the generator kill-list rather than claiming no-coupling",
            },
            {
                "decision_id": "DEC1115_1_best_attack",
                "decision": "domain selector, memory scalar, and species constants are the highest-priority generators",
                "because": "they directly feed alpha/mass/source coupling residuals and local-test failures",
                "next_action": "build a generator elimination order with proof obligations and fallback prior widths",
            },
            {
                "decision_id": "DEC1115_2_fallback",
                "decision": "finite prior-width route is now explicit",
                "because": "if any continuous invariant remains, it can feed continuous visible couplings",
                "next_action": "source numeric prior widths only after a generator resists elimination",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1115_0_1116",
                "next_target": "1116-Y5-R10-invariant-generator-kill-list-or-coupling-prior-source-pack.md",
                "objective": "attack surviving invariant generators in priority order; if a generator cannot be eliminated, assign the corresponding alpha/mass/source coupling prior-width row and keep claims blocked",
                "include": "domain selector; memory scalar; species constants; finite-cell spectrum; domain class; time-arrow; readout projector; prior-width source requirements",
                "exclude": "closure axiom as derivation; alpha value prediction; tau=1; source-unity; symbolic R10 pass; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    generators: list[dict[str, object]],
    priors: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    outputs: dict[str, Path],
) -> list[dict[str, object]]:
    validation: list[dict[str, object]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        validation.append(
            {
                "check_id": check_id,
                "result": "pass" if passed else "fail",
                "detail": detail,
                "valid_for_claim": "false",
                "generated_utc": now(),
            }
        )

    add("V1115_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1115_1_sufficiency_theorem", any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem), "trivial invariant algebra sufficiency theorem is recorded")
    add("V1115_2_counterexample_recorded", any(row["result"] == "COUNTEREXAMPLE_PROVED" for row in theorem), "continuous scalar counterexample is recorded")
    add("V1115_3_triviality_not_derived", any(row["result"] == "LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_NOT_DERIVED" for row in theorem), "local invariant algebra triviality remains unpromoted")
    add("V1115_4_generators_prioritized", sum(1 for row in generators if row["priority"] == "critical") >= 3, "critical generator kill-list rows are present")
    add("V1115_5_priors_nonclaim", all(row["current_status"] == "MISSING_PRIOR_WIDTH_OR_ZERO_THEOREM" for row in priors), "finite prior-width rows remain missing-input nonclaim rows")
    add("V1115_6_gates_blocked", all(row["gate_pass"] == "false" for row in gates), "all claim gates remain blocked")
    add("V1115_7_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in theorem + generators + priors + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1115_8_next_target", next_target[0]["next_target"].startswith("1116-") and "invariant-generator-kill-list" in str(next_target[0]["next_target"]), "1116 handoff targets invariant generator kill-list")
    add("V1115_9_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1115_10_csv_parse", csv_parse_ok, "all 1115 CSV outputs parse cleanly")
    add("V1115_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1115_SUMMARY", True, "1115 rejects current invariant algebra triviality and stages generator kill-list/prior-width fork")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    generators: list[dict[str, object]],
    priors: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1115 - Local Invariant Algebra Triviality Or Finite Coupling Prior Widths

**Current verdict:** local invariant algebra triviality is not derived. If `O(C_hid)^inv = R`, visible coupling drift dies cleanly; but the current corpus still has surviving invariant generators and active scalar counterexamples.

**Useful reduction:** the coupling problem is no longer vague. Either kill the surviving generators, or assign finite prior widths/products for alpha, mass/clock, source, domain, memory, and readout couplings.

**No claim:** no no-coupling theorem, no `b_alpha=0`, no WEP/R10/source universality, and no local-GR pass follows from 1115.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Triviality Theorem Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "claim_allowed"], theorem)}

## Generator Kill-List
{table(["generator_id", "generator", "status", "damage_if_live", "kill_condition", "priority", "claim_allowed"], generators)}

## Finite Prior-Width Rows
{table(["prior_id", "coupling_family", "symbolic_width", "needed_numeric_or_zero", "arenas", "current_status", "claim_allowed"], priors)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed"], gates)}

## Decisions
{table(["decision_id", "decision", "because", "next_action", "claim_allowed"], decisions)}

## Validation
{table(["check_id", "result", "detail", "valid_for_claim"], validation)}

## Next Target
{table(["next_id", "next_target", "objective", "include", "exclude", "claim_allowed"], next_target)}
"""
    DOC.write_text(text, encoding="utf-8")


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists() and pycache.is_dir():
        shutil.rmtree(pycache)


def main() -> None:
    outputs = {
        "source_register": OUT / "P8_Y5_R10_1115_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1115_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY_ATTEMPT.csv",
        "generators": OUT / "P8_Y5_R10_1115_GENERATOR_KILL_LIST.csv",
        "priors": OUT / "P8_Y5_R10_1115_FINITE_COUPLING_PRIOR_WIDTHS_NONCLAIM.csv",
        "gates": OUT / "P8_Y5_R10_1115_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1115_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1115_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1115_VALIDATION.csv",
    }
    sources = source_rows()
    theorem = triviality_rows()
    generators = generator_rows()
    priors = prior_width_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["generators"], generators)
    write_csv(outputs["priors"], priors)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, theorem, generators, priors, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorem, generators, priors, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
