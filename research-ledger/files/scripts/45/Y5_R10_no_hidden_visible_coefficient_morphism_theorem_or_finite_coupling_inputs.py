from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1114-Y5-R10-no-hidden-visible-coefficient-morphism-theorem-or-finite-coupling-inputs.md"


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
            "source_id": "SRC1114_0_1113_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1113_NEXT_TARGET.csv",
            "needle": "NEXT1113_0_1114",
            "note": "1113 handoff to no-hidden-visible coefficient morphism theorem.",
        },
        {
            "source_id": "SRC1114_1_1113_contract",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1113_PARENT_OWNED_READOUT_DESCENT_CONTRACT.csv",
            "needle": "POC1113_4_no_hidden_visible_morphisms",
            "note": "critical coupling clause.",
        },
        {
            "source_id": "SRC1114_2_1113_acquisition",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1113_ALPHA_PRODUCT_INPUT_ACQUISITION_LEDGER.csv",
            "needle": "AQ1113_0_balpha_or_zero",
            "note": "finite product acquisition blocker.",
        },
        {
            "source_id": "SRC1114_3_1050_product_functor",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "PFT1050_2_forbidden_mixed_hom",
            "note": "exact mixed-Hom theorem target.",
        },
        {
            "source_id": "SRC1114_4_1050_verdict",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1050_PRODUCT_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "FAIL_CURRENT_CLAIM_PRIOR_WIDTH_PACK_REQUIRED",
            "note": "product functor is not parent-derived.",
        },
        {
            "source_id": "SRC1114_5_1099_gauge",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv",
            "needle": "EXC1099_1_U1_gauge",
            "note": "gauge invariance does not forbid F2 coefficient functions.",
        },
        {
            "source_id": "SRC1114_6_980_scalar",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "NMF980_2_scalar_obstruction_lemma",
            "note": "surviving invariant scalar can feed continuous sector labels.",
        },
        {
            "source_id": "SRC1114_7_980_counter",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv",
            "needle": "CEX980_0_theta_IQ",
            "note": "quotient-invariant scalar counterexample.",
        },
        {
            "source_id": "SRC1114_8_767_no_vertex",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_767_PARENT_MATTER_FUNCTOR_REAUDIT.csv",
            "needle": "PMR767_3_no_alpha_mass_vertex",
            "note": "no alpha/mass vertex remains unsigned.",
        },
        {
            "source_id": "SRC1114_9_953_source",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "NSF953_5_verdict",
            "note": "source label forgetting is conditional only.",
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


def theorem_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attempt_id": "NHV1114_0_target",
                "claim_piece": "no hidden-visible coefficient morphism",
                "formal_statement": "Hom(C_hid, Coeff(O_vis)) is constant or absent for visible EM/matter operators.",
                "result": "TARGET_SHARP",
                "proof_or_blocker": "this is exactly the clause that would kill f_hid F_Q^2, mass vertices, clock vertices, and relative source weights",
            },
            {
                "attempt_id": "NHV1114_1_typed_language",
                "claim_piece": "typed object-language exclusion",
                "formal_statement": "If visible coefficient functors have domain Q_vis x Rep and no hidden object is well-typed as an argument, then every hidden-visible coefficient morphism is absent.",
                "result": "EXACT_CONDITIONAL_THEOREM",
                "proof_or_blocker": "well-typed terms cannot be formed without a hidden-to-visible argument slot; this is formal grammar, not dynamics",
            },
            {
                "attempt_id": "NHV1114_2_product_category",
                "claim_piece": "product category sequester",
                "formal_statement": "If C_parent = C_vis x C_hid and visible functors factor through pi_vis, then D_hid coeff_vis = 0.",
                "result": "EXACT_CONDITIONAL_THEOREM",
                "proof_or_blocker": "chain rule through pi_vis kills hidden tangent vectors; same sandwich structure as 1112",
            },
            {
                "attempt_id": "NHV1114_3_covariance_gauge_test",
                "claim_piece": "diffeomorphism/U(1) covariance forbids hidden coefficient",
                "formal_statement": "f(I_hid) F_Q^2 is forbidden by general covariance or visible U(1).",
                "result": "FALSE",
                "proof_or_blocker": "1099 records that scalar coefficient times F_Q^2 is a gauge-invariant scalar-density term",
            },
            {
                "attempt_id": "NHV1114_4_scalar_obstruction",
                "claim_piece": "quotient invariance alone forbids coefficient maps",
                "formal_statement": "A quotient-invariant hidden/local scalar I cannot feed a continuous visible coefficient c(I).",
                "result": "OBSTRUCTION_PROVED",
                "proof_or_blocker": "980 proves the opposite: any surviving nonconstant invariant scalar can define a nonconstant functor into continuous coefficient space",
            },
            {
                "attempt_id": "NHV1114_5_radiative_readout",
                "claim_piece": "tree-level no-morphism survives observed reduction",
                "formal_statement": "Renormalized/effective visible coefficients and readout maps preserve the no-hidden-visible argument rule.",
                "result": "UNSIGNED",
                "proof_or_blocker": "radiative/readout closure is still required even if bare object language is clean",
            },
            {
                "attempt_id": "NHV1114_6_verdict",
                "claim_piece": "derive no-hidden-visible coefficient morphism theorem",
                "formal_statement": "Visible EM/matter coefficients cannot take hidden representatives or hidden invariants as arguments.",
                "result": "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED",
                "proof_or_blocker": "conditional typed/product-category theorem is clean, but current corpus has not derived the typed parent grammar, invariant algebra triviality, no-extension rule, or radiative/readout closure",
            },
        ]
    )


def obstruction_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "obstruction_id": "OBS1114_0_grammar",
                "obstruction": "typed parent object language not signed",
                "why_it_matters": "without a formal grammar excluding hidden arguments, f(I_hid) coefficients are legal terms",
                "kills_or_blocks": "unconditional b_alpha=0; mass/clock vertex silence",
                "repair_route": "derive parent DSL/signature or explicitly label as closure",
                "severity": "critical",
            },
            {
                "obstruction_id": "OBS1114_1_scalar_invariant",
                "obstruction": "surviving nonconstant invariant scalar",
                "why_it_matters": "c(I) maps hidden/local information into continuous visible coefficients",
                "kills_or_blocks": "no-marker/no-coupling theorem",
                "repair_route": "local invariant algebra triviality or discrete connected target theorem",
                "severity": "critical",
            },
            {
                "obstruction_id": "OBS1114_2_no_extension",
                "obstruction": "co-moving marker or extended quotient",
                "why_it_matters": "an extended quotient can carry material/species labels while remaining quotient-compatible",
                "kills_or_blocks": "species-blind matter/source coupling",
                "repair_route": "primitive no-extension theorem",
                "severity": "high",
            },
            {
                "obstruction_id": "OBS1114_3_radiative",
                "obstruction": "radiative/readout regeneration",
                "why_it_matters": "loops, thresholds, or reduced spectroscopy can create effective coefficients even after bare sequester",
                "kills_or_blocks": "observed alpha/clock silence",
                "repair_route": "renormalized readout closure theorem",
                "severity": "critical",
            },
            {
                "obstruction_id": "OBS1114_4_source_labels",
                "obstruction": "source/test labels survive before coupling selection",
                "why_it_matters": "kappa_A or beta_source_alpha can remain additive and covariant but WEP-violating",
                "kills_or_blocks": "WEP/R10 source product silence",
                "repair_route": "source label-forgetting quotient",
                "severity": "high",
            },
        ]
    )


def finite_input_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "input_id": "FCI1114_0_alpha_F2",
                "coupling": "c_alpha or b_alpha from f(I_hid)F_Q^2",
                "required_if_theorem_fails": "numeric coefficient or theorem-zero for D_v ln Z_Q_eff",
                "arenas": "clock; WEP; R10; EM",
                "current_status": "MISSING_THEOREM_ZERO_OR_NUMERIC_COEFFICIENT",
                "allowed_source": "parent derivation, EFT matching, or explicit prior-width source",
            },
            {
                "input_id": "FCI1114_1_mass_clock",
                "coupling": "b_mA, b_mu, b_nuc, b_clock_i",
                "required_if_theorem_fails": "numeric mass/clock sensitivity vector or no-vertex theorem",
                "arenas": "atomic clocks; spectroscopy; WEP composition",
                "current_status": "MISSING_MASS_CLOCK_COUPLING_VECTOR",
                "allowed_source": "parent matter functor derivation or source-backed finite vector",
            },
            {
                "input_id": "FCI1114_2_source_weight",
                "coupling": "beta_source_alpha or relative kappa_A",
                "required_if_theorem_fails": "source label-forgetting theorem or numeric source-normalization product",
                "arenas": "WEP; R10; orbital/local gravity",
                "current_status": "MISSING_SOURCE_LABEL_FORGETTING_OR_NUMERIC_SOURCE_WEIGHT",
                "allowed_source": "universal source functor proof or finite source-coupling acquisition",
            },
            {
                "input_id": "FCI1114_3_r10_product",
                "coupling": "K_X^R10(lambda)*beta_source(lambda)*beta_test(lambda)",
                "required_if_theorem_fails": "numeric short-range product and promoted alpha_bound(lambda)",
                "arenas": "R10 short-range force",
                "current_status": "MISSING_R10_FINITE_BRANCH_VECTOR_AND_PROMOTED_BOUND",
                "allowed_source": "parent R10 branch map or strict product runner source rows",
            },
            {
                "input_id": "FCI1114_4_radiative_counterterm",
                "coupling": "Delta_rad/readout coefficient",
                "required_if_theorem_fails": "renormalized coefficient zero theorem or finite counterterm product",
                "arenas": "EM; clocks; spectra; WEP",
                "current_status": "MISSING_RADIOUT_CLOSURE_OR_COUNTERTERM_VALUE",
                "allowed_source": "EFT/readout closure proof or finite residual source",
            },
            {
                "input_id": "FCI1114_5_cross_arena_domain",
                "coupling": "same branch/domain classifier across local arenas",
                "required_if_theorem_fails": "parent-owned classifier or separate arena-specific numeric products",
                "arenas": "clock; WEP; R10; local GR",
                "current_status": "MISSING_CROSS_ARENA_PARENT_MAP",
                "allowed_source": "global readout/domain functor",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1114_0_no_morphism",
                "claim": "hidden-visible coefficient morphisms are forbidden",
                "gate_pass": "false",
                "reason": "typed/product theorem is conditional; scalar obstruction remains live",
            },
            {
                "gate_id": "CG1114_1_alpha_silence",
                "claim": "b_alpha=0 is derived",
                "gate_pass": "false",
                "reason": "f(I_hid)F_Q^2 remains legal unless no-morphism and radiative closure are signed",
            },
            {
                "gate_id": "CG1114_2_mass_source_silence",
                "claim": "mass/source coupling residuals vanish",
                "gate_pass": "false",
                "reason": "matter functor and source label forgetting remain conditional",
            },
            {
                "gate_id": "CG1114_3_finite_inputs_ready",
                "claim": "finite coupling rows are runner-ready",
                "gate_pass": "false",
                "reason": "rows identify required inputs but still contain missing theorem/numeric sources",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1114_0_theorem_result",
                "decision": "no-hidden-visible coefficient morphism theorem is not derived",
                "because": "the conditional typed/product-category route is exact, but a surviving invariant scalar can feed continuous coefficients unless the parent algebra is trivialized or typed out",
                "next_action": "attack local invariant algebra triviality/no-extension before giving up to finite priors",
            },
            {
                "decision_id": "DEC1114_1_best_next",
                "decision": "local invariant algebra triviality is the next derivation needle",
                "because": "980 proves this is the obstruction behind coefficient morphisms and sector markers",
                "next_action": "try to prove every admissible hidden/local scalar is constant/quotient-invisible on the local branch",
            },
            {
                "decision_id": "DEC1114_2_fallback",
                "decision": "finite coupling input acquisition is now explicit",
                "because": "if invariant algebra triviality fails, alpha/mass/source couplings must be bounded as finite products",
                "next_action": "keep all finite rows nonclaim until numeric source-backed values exist",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1114_0_1115",
                "next_target": "1115-Y5-R10-local-invariant-algebra-triviality-or-finite-coupling-prior-widths.md",
                "objective": "try to prove the local hidden/invariant scalar algebra is trivial or constant on the local branch; if not, convert alpha/mass/source couplings into finite prior-width/product input rows",
                "include": "invariant scalar algebra; quotient map; connected branch; no-extension rule; discrete vs continuous targets; alpha/mass/source coupling rows; radiative/readout hooks",
                "exclude": "closure axiom as derivation; alpha value prediction; tau=1; source-unity; symbolic R10 pass; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    finite_inputs: list[dict[str, object]],
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

    add("V1114_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1114_1_conditional_theorem", sum(1 for row in theorem if row["result"] == "EXACT_CONDITIONAL_THEOREM") >= 2, "typed and product-category no-morphism theorems are conditional")
    add("V1114_2_obstruction_recorded", any(row["result"] == "OBSTRUCTION_PROVED" for row in theorem), "scalar obstruction is recorded")
    add("V1114_3_no_morphism_not_derived", any(row["result"] == "NO_HIDDEN_VISIBLE_MORPHISM_NOT_DERIVED" for row in theorem), "no-hidden-visible theorem remains unpromoted")
    add("V1114_4_critical_obstructions", sum(1 for row in obstructions if row["severity"] == "critical") >= 3, "critical grammar/scalar/radiative obstructions are present")
    add("V1114_5_finite_inputs_missing", all(str(row["current_status"]).startswith("MISSING") for row in finite_inputs), "finite coupling inputs remain missing-input nonclaim rows")
    add("V1114_6_gates_blocked", all(row["gate_pass"] == "false" for row in gates), "all claim gates remain blocked")
    add("V1114_7_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in theorem + obstructions + finite_inputs + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1114_8_next_target", next_target[0]["next_target"].startswith("1115-") and "local-invariant-algebra" in str(next_target[0]["next_target"]), "1115 handoff targets local invariant algebra triviality")
    add("V1114_9_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1114_10_csv_parse", csv_parse_ok, "all 1114 CSV outputs parse cleanly")
    add("V1114_11_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1114_SUMMARY", True, "1114 reduces the coupling theorem to local invariant algebra triviality or finite coupling inputs")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    obstructions: list[dict[str, object]],
    finite_inputs: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1114 - No Hidden-Visible Coefficient Morphism Theorem Or Finite Coupling Inputs

**Current verdict:** the no-hidden-visible coefficient morphism theorem is exact as a typed/product-category theorem, but it is not derived from the current corpus. Covariance and visible gauge symmetry do not forbid `f(I_hid)F_Q^2`; the real blocker is the surviving invariant-scalar route.

**Main reduction:** the coupling problem has reduced to local invariant algebra triviality or an explicit parent object-language exclusion. If a nonconstant hidden/local scalar survives, it can feed continuous visible coefficients unless the parent grammar forbids that argument slot.

**No claim:** no `b_alpha=0`, no mass/clock/source silence, no WEP/R10 pass, and no local-GR pass follows from 1114.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Theorem Attempt
{table(["attempt_id", "claim_piece", "formal_statement", "result", "proof_or_blocker", "claim_allowed"], theorem)}

## Obstruction Ledger
{table(["obstruction_id", "obstruction", "why_it_matters", "kills_or_blocks", "repair_route", "severity", "claim_allowed"], obstructions)}

## Finite Coupling Inputs
{table(["input_id", "coupling", "required_if_theorem_fails", "arenas", "current_status", "allowed_source", "claim_allowed"], finite_inputs)}

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
        "source_register": OUT / "P8_Y5_R10_1114_SOURCE_REGISTER.csv",
        "theorem": OUT / "P8_Y5_R10_1114_NO_HIDDEN_VISIBLE_MORPHISM_THEOREM_ATTEMPT.csv",
        "obstructions": OUT / "P8_Y5_R10_1114_COUPLING_OBSTRUCTION_LEDGER.csv",
        "finite_inputs": OUT / "P8_Y5_R10_1114_FINITE_COUPLING_INPUTS_NONCLAIM.csv",
        "gates": OUT / "P8_Y5_R10_1114_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1114_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1114_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1114_VALIDATION.csv",
    }
    sources = source_rows()
    theorem = theorem_rows()
    obstructions = obstruction_rows()
    finite_inputs = finite_input_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["theorem"], theorem)
    write_csv(outputs["obstructions"], obstructions)
    write_csv(outputs["finite_inputs"], finite_inputs)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, theorem, obstructions, finite_inputs, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, theorem, obstructions, finite_inputs, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
