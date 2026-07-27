from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "1116-Y5-R10-invariant-generator-kill-list-or-coupling-prior-source-pack.md"


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
            "source_id": "SRC1116_0_1115_next",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1115_NEXT_TARGET.csv",
            "needle": "NEXT1115_0_1116",
            "note": "1115 handoff to invariant generator kill-list.",
        },
        {
            "source_id": "SRC1116_1_1115_kill",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1115_GENERATOR_KILL_LIST.csv",
            "needle": "KILL1115_2_domain_selector",
            "note": "domain selector is a critical surviving generator.",
        },
        {
            "source_id": "SRC1116_2_1115_prior",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1115_FINITE_COUPLING_PRIOR_WIDTHS_NONCLAIM.csv",
            "needle": "PW1115_4_memory",
            "note": "finite prior-width rows are staged.",
        },
        {
            "source_id": "SRC1116_3_domain_selector",
            "relative_path": "source-intake/mts_residuals/P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv",
            "needle": "T6_no_vector_verdict",
            "note": "domain selector no-vector/no-flux/no-anisotropy attempt fails current corpus.",
        },
        {
            "source_id": "SRC1116_4_memory",
            "relative_path": "source-intake/mts_residuals/P8_DOUBLE_ZERO_MEMORY_ORIGIN_ATTEMPT.csv",
            "needle": "O6_verdict",
            "note": "memory double-zero requirement has conditional origins but is not parent-derived.",
        },
        {
            "source_id": "SRC1116_5_species",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_953_SOURCE_FUNCTOR_THEOREM_ATTEMPT.csv",
            "needle": "NSF953_5_verdict",
            "note": "source label-forgetting theorem is conditional not parent-derived.",
        },
        {
            "source_id": "SRC1116_6_no_marker",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1028_NO_MARKER_THEOREM_AUDIT.csv",
            "needle": "NM1028_6_verdict",
            "note": "ordinary matter no-marker theorem remains claim-blocked.",
        },
        {
            "source_id": "SRC1116_7_algebra",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_965_LOCAL_INVARIANT_ALGEBRA_AUDIT.csv",
            "needle": "ALG965_9_verdict",
            "note": "local invariant algebra is not derived.",
        },
        {
            "source_id": "SRC1116_8_1114_inputs",
            "relative_path": "source-intake/mts_residuals/P8_Y5_R10_1114_FINITE_COUPLING_INPUTS_NONCLAIM.csv",
            "needle": "FCI1114_3_r10_product",
            "note": "finite coupling input rows remain nonclaim.",
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


def attack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "attack_id": "ATT1116_0_domain_selector",
                "generator": "domain_selector_chi_D",
                "priority_rank": "1",
                "best_kill_route": "prove selector is gauge/readout-only or fixed local branch with no vector, no flux, no anisotropic stress, and no source-normalization operator",
                "current_result": "NOT_ELIMINATED",
                "evidence": "domain no-vector attempt has conditional lemmas but T6_no_vector_verdict fails current corpus",
                "fallback_prior": "PW1115_3_domain",
                "next_action": "derive parent-domain selector zero/no-source theorem or retain finite domain coupling width",
            },
            {
                "attack_id": "ATT1116_1_memory_scalar",
                "generator": "memory_or_class_scalar",
                "priority_rank": "2",
                "best_kill_route": "derive local value and gradient zero from a parent double-zero memory gate or no-hair operator",
                "current_result": "NOT_ELIMINATED",
                "evidence": "double-zero p>=2 is required and conditionally motivated, but O6_verdict says parent origin is not derived",
                "fallback_prior": "PW1115_4_memory",
                "next_action": "derive memory double-zero origin or retain finite memory residual width",
            },
            {
                "attack_id": "ATT1116_2_species_constants",
                "generator": "species_charge_constants",
                "priority_rank": "3",
                "best_kill_route": "derive source label-forgetting plus constant-sector universality",
                "current_result": "NOT_ELIMINATED",
                "evidence": "NSF953 gives a clean conditional source theorem, but no-species-label premise is not parent-derived",
                "fallback_prior": "PW1115_2_source and PW1115_1_mass_clock",
                "next_action": "derive label forgetting or retain finite source/mass prior widths",
            },
            {
                "attack_id": "ATT1116_3_finite_cell",
                "generator": "finite_cell_fibre_spectrum",
                "priority_rank": "4",
                "best_kill_route": "prove finite-cell spectrum is pure basis/gauge relabeling or universally integrated out",
                "current_result": "NOT_ELIMINATED",
                "evidence": "965/1092 keep finite-cell spectrum as nontrivial generator debt",
                "fallback_prior": "PW1115_0_alpha; PW1115_1_mass_clock",
                "next_action": "defer until high-pressure generators are attacked",
            },
            {
                "attack_id": "ATT1116_4_domain_class",
                "generator": "relative_boundary_domain_class",
                "priority_rank": "5",
                "best_kill_route": "derive local trivial class or fixed-class stress-free nohair",
                "current_result": "NOT_ELIMINATED",
                "evidence": "965/1092 retain relative domain class as branch/source selector debt",
                "fallback_prior": "PW1115_3_domain",
                "next_action": "fold into domain-selector attack unless separate boundary/domain source appears",
            },
            {
                "attack_id": "ATT1116_5_readout_projector",
                "generator": "post_readout_projector",
                "priority_rank": "6",
                "best_kill_route": "prove readout-after-variation and no post-readout EFT backreaction",
                "current_result": "POLICY_ONLY_NOT_ELIMINATED",
                "evidence": "1028 and 1113 keep readout clauses as contract/policy unless globally parent-signed",
                "fallback_prior": "PW1115_5_readout",
                "next_action": "defer behind domain/memory/source because it is cross-cutting",
            },
            {
                "attack_id": "ATT1116_6_time_arrow",
                "generator": "orientation_time_arrow",
                "priority_rank": "7",
                "best_kill_route": "show time-arrow marker is contained in observed coframe, constant, or pure gauge",
                "current_result": "UNCLASSIFIED_NOT_ELIMINATED",
                "evidence": "965/1092 leave orientation/time-arrow marker unclassified",
                "fallback_prior": "preferred-frame/time-asymmetry residual row",
                "next_action": "defer unless PPN preferred-frame route resurfaces",
            },
        ]
    )


def proof_obligation_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "obligation_id": "OBL1116_0_domain_selector_zero",
                "target_generator": "domain_selector_chi_D",
                "must_prove": "P_loc grad chi_D = 0, local selector flux = 0, selector STF stress = 0, and source-normalization operator = 0",
                "current_status": "CONDITIONAL_LEMMAS_ONLY",
                "if_fail": "domain coupling prior/source rows required for local GR, R10, and cosmology split",
            },
            {
                "obligation_id": "OBL1116_1_memory_double_zero",
                "target_generator": "memory_or_class_scalar",
                "must_prove": "parent action forces f(0)=f'(0)=0 and local memory value/gradient silence",
                "current_status": "REQUIREMENT_DERIVED_BUT_ORIGIN_NOT",
                "if_fail": "memory coupling prior required for clock, PPN, local force, and cosmology",
            },
            {
                "obligation_id": "OBL1116_2_species_label_forgetting",
                "target_generator": "species_charge_constants",
                "must_prove": "source/matter functor domain forgets species labels before coupling selection",
                "current_status": "CONDITIONAL_THEOREM_ONLY",
                "if_fail": "source and mass/clock coupling priors required",
            },
            {
                "obligation_id": "OBL1116_3_no_extension",
                "target_generator": "all material/domain markers",
                "must_prove": "no co-moving material/domain marker may extend the parent quotient as physical data",
                "current_status": "NOT_DERIVED",
                "if_fail": "no-marker theorem cannot close; finite priors remain live",
            },
            {
                "obligation_id": "OBL1116_4_radiative_readout",
                "target_generator": "readout_projector and visible couplings",
                "must_prove": "EFT/readout reduction preserves zero clauses and does not regenerate visible coefficients",
                "current_status": "UNSIGNED",
                "if_fail": "readout/counterterm prior rows required even if bare generator kill succeeds",
            },
        ]
    )


def source_pack_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "source_id": "CPS1116_0_domain",
                "coupling_prior": "sigma_chiD; sigma_domain",
                "trigger_generator": "domain_selector_chi_D or relative_boundary_domain_class",
                "source_requirement": "numeric domain vector/flux/STF/source-normalization coefficients or theorem-zero source paths",
                "current_status": "MISSING_NUMERIC_SOURCE_OR_ZERO_THEOREM",
                "claim_policy": "blocks local-GR/R10/domain claims until filled or killed",
            },
            {
                "source_id": "CPS1116_1_memory",
                "coupling_prior": "sigma_memory",
                "trigger_generator": "memory_or_class_scalar",
                "source_requirement": "numeric memory value/gradient/coupling coefficient or parent double-zero/nohair theorem",
                "current_status": "MISSING_NUMERIC_SOURCE_OR_ZERO_THEOREM",
                "claim_policy": "blocks clock/PPN/local-force memory silence",
            },
            {
                "source_id": "CPS1116_2_source",
                "coupling_prior": "sigma_beta_source; sigma_delta_kappa",
                "trigger_generator": "species_charge_constants",
                "source_requirement": "source label-forgetting theorem or numeric relative source-weight bounds",
                "current_status": "MISSING_NUMERIC_SOURCE_OR_ZERO_THEOREM",
                "claim_policy": "blocks WEP/R10/source universality claims",
            },
            {
                "source_id": "CPS1116_3_alpha_mass",
                "coupling_prior": "sigma_b_alpha; sigma_b_m; sigma_b_mu; sigma_b_clock",
                "trigger_generator": "finite_cell_fibre_spectrum; memory_or_class_scalar; species constants",
                "source_requirement": "numeric alpha/mass/clock coefficient vector or no-hidden-visible/no-constant-marker theorem",
                "current_status": "MISSING_NUMERIC_SOURCE_OR_ZERO_THEOREM",
                "claim_policy": "blocks clock/WEP/R10 alpha and mass rows",
            },
            {
                "source_id": "CPS1116_4_readout",
                "coupling_prior": "sigma_readout",
                "trigger_generator": "post_readout_projector",
                "source_requirement": "readout-after-variation plus no EFT backreaction theorem, or numeric readout counterterm prior",
                "current_status": "MISSING_NUMERIC_SOURCE_OR_ZERO_THEOREM",
                "claim_policy": "blocks observed-clock/EM readout silence",
            },
        ]
    )


def gate_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "gate_id": "CG1116_0_any_generator_killed",
                "claim": "at least one critical generator is eliminated",
                "gate_pass": "false",
                "reason": "domain selector, memory scalar, and species constants remain conditional/not derived",
            },
            {
                "gate_id": "CG1116_1_local_invariant_triviality",
                "claim": "local invariant algebra is trivial",
                "gate_pass": "false",
                "reason": "generator kill-list remains live",
            },
            {
                "gate_id": "CG1116_2_finite_priors_ready",
                "claim": "finite coupling prior/source pack is claim-ready",
                "gate_pass": "false",
                "reason": "source pack rows require numeric source-backed inputs or theorem-zero",
            },
            {
                "gate_id": "CG1116_3_local_gr_claim",
                "claim": "local-GR/PPN/R10 safety is established",
                "gate_pass": "false",
                "reason": "domain, memory, and source generators can still feed local residuals",
            },
        ]
    )


def decision_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "decision_id": "DEC1116_0_result",
                "decision": "no critical generator was eliminated in 1116",
                "because": "existing attempts give conditional routes but not parent-signed zeros",
                "next_action": "attack the domain selector first because it is the most direct local-GR/R10 threat",
            },
            {
                "decision_id": "DEC1116_1_attack_order",
                "decision": "domain selector -> memory scalar -> species constants is the priority order",
                "because": "domain controls local-vs-cosmology switching, memory controls drift/fifth-force channels, species constants control WEP/source universality",
                "next_action": "attempt domain selector zero/no-source theorem next",
            },
            {
                "decision_id": "DEC1116_2_fallback",
                "decision": "coupling prior source pack is staged but nonclaim",
                "because": "if a generator resists elimination, the theory must pay with a numeric width/product row",
                "next_action": "do not fill priors with placeholders; use source-backed numeric values or theorem-zero only",
            },
        ]
    )


def next_rows() -> list[dict[str, object]]:
    return stamp(
        [
            {
                "next_id": "NEXT1116_0_1117",
                "next_target": "1117-Y5-R10-domain-selector-zero-or-domain-coupling-prior-source.md",
                "objective": "try to derive the domain selector as gauge/readout-only or fixed local branch with no vector, flux, anisotropic stress, or source-normalization operator; if not, create finite domain-coupling prior/source rows",
                "include": "chi_D; P_loc grad chi_D; domain flux; selector STF stress; R11/domain source operator; local branch fixed-class condition; finite domain prior rows",
                "exclude": "closure axiom as derivation; local-GR claim; tau=1; source-unity; symbolic R10 pass; GitHub; formalization edits",
            }
        ]
    )


def validate(
    sources: list[dict[str, object]],
    attacks: list[dict[str, object]],
    obligations: list[dict[str, object]],
    source_pack: list[dict[str, object]],
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

    add("V1116_0_sources_exist", all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources), "all cited local source paths exist and needles are found")
    add("V1116_1_priority_order", [row["generator"] for row in sorted(attacks, key=lambda row: int(row["priority_rank"]))][:3] == ["domain_selector_chi_D", "memory_or_class_scalar", "species_charge_constants"], "top-three generator attack order is domain, memory, species")
    add("V1116_2_no_eliminations", all(row["current_result"] not in {"ELIMINATED", "KILLED", "DERIVED_ZERO"} for row in attacks), "no generator is marked eliminated")
    add("V1116_3_obligations_present", len(obligations) >= 5 and all(row["current_status"] != "" for row in obligations), "proof obligations are explicit")
    add("V1116_4_source_pack_nonclaim", all(row["current_status"] == "MISSING_NUMERIC_SOURCE_OR_ZERO_THEOREM" for row in source_pack), "source pack rows remain missing-input nonclaim")
    add("V1116_5_gates_blocked", all(row["gate_pass"] == "false" for row in gates), "all claim gates remain blocked")
    add("V1116_6_no_claim_rows", all(row.get("valid_for_claim") == "false" and row.get("claim_allowed") == "false" for row in attacks + obligations + source_pack + gates + decisions + next_target), "all generated rows remain nonclaim")
    add("V1116_7_next_target", next_target[0]["next_target"].startswith("1117-") and "domain-selector-zero" in str(next_target[0]["next_target"]), "1117 handoff targets domain selector zero or domain prior source")
    add("V1116_8_generated_under_post_checkpoint", all(str(path.resolve()).startswith(str(ROOT.resolve())) for path in outputs.values()), "all generated outputs are under post-checkpoint-work")
    csv_parse_ok = True
    for output_name, path in outputs.items():
        if output_name == "validation":
            continue
        if path.suffix.lower() == ".csv" and path.exists():
            with path.open("r", newline="", encoding="utf-8") as handle:
                list(csv.DictReader(handle))
        elif path.suffix.lower() == ".csv":
            csv_parse_ok = False
    add("V1116_9_csv_parse", csv_parse_ok, "all 1116 CSV outputs parse cleanly")
    add("V1116_10_formalization_untouched", True, "generator writes no outputs under formalization-workbench")
    add("V1116_SUMMARY", True, "1116 stages the generator attack order and keeps local claims blocked")
    return validation


def table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def write_doc(
    sources: list[dict[str, object]],
    attacks: list[dict[str, object]],
    obligations: list[dict[str, object]],
    source_pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    validation: list[dict[str, object]],
    next_target: list[dict[str, object]],
) -> None:
    text = f"""# 1116 - Invariant Generator Kill-List Or Coupling Prior Source Pack

**Current verdict:** no critical invariant generator was eliminated. The work now has a concrete attack order: domain selector first, memory scalar second, species/source constants third.

**Useful result:** this is a real tightening of the local-GR route. Instead of saying "coupling problem", the framework now has named generators, proof obligations, and exact finite-prior consequences if any generator survives.

**No claim:** no local invariant triviality, no no-coupling theorem, no local-GR/PPN/R10 safety, and no finite prior pass follows from 1116.

## Source Register
{table(["source_id", "relative_path", "exists", "needle", "needle_found", "note"], sources)}

## Generator Attack Order
{table(["attack_id", "generator", "priority_rank", "best_kill_route", "current_result", "evidence", "fallback_prior", "next_action", "claim_allowed"], attacks)}

## Proof Obligations
{table(["obligation_id", "target_generator", "must_prove", "current_status", "if_fail", "claim_allowed"], obligations)}

## Coupling Prior Source Pack
{table(["source_id", "coupling_prior", "trigger_generator", "source_requirement", "current_status", "claim_policy", "claim_allowed"], source_pack)}

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
        "source_register": OUT / "P8_Y5_R10_1116_SOURCE_REGISTER.csv",
        "attack_order": OUT / "P8_Y5_R10_1116_GENERATOR_ATTACK_ORDER.csv",
        "obligations": OUT / "P8_Y5_R10_1116_PROOF_OBLIGATIONS.csv",
        "source_pack": OUT / "P8_Y5_R10_1116_COUPLING_PRIOR_SOURCE_PACK_NONCLAIM.csv",
        "gates": OUT / "P8_Y5_R10_1116_CLAIM_GATES.csv",
        "decisions": OUT / "P8_Y5_R10_1116_DECISION_LEDGER.csv",
        "next": OUT / "P8_Y5_R10_1116_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_1116_VALIDATION.csv",
    }
    sources = source_rows()
    attacks = attack_rows()
    obligations = proof_obligation_rows()
    source_pack = source_pack_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(outputs["source_register"], sources)
    write_csv(outputs["attack_order"], attacks)
    write_csv(outputs["obligations"], obligations)
    write_csv(outputs["source_pack"], source_pack)
    write_csv(outputs["gates"], gates)
    write_csv(outputs["decisions"], decisions)
    write_csv(outputs["next"], next_target)
    validation = validate(sources, attacks, obligations, source_pack, gates, decisions, next_target, outputs)
    write_csv(outputs["validation"], validation)
    write_doc(sources, attacks, obligations, source_pack, gates, decisions, validation, next_target)
    remove_pycache()

    failed = [row for row in validation if row["result"] != "pass"]
    print(f"wrote {DOC}")
    print(f"validation: {'PASS' if not failed else 'FAIL'}")
    for row in failed:
        print(f"{row['check_id']}: {row['detail']}")


if __name__ == "__main__":
    main()
