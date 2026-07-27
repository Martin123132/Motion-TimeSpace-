from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "934-Y5-R10-beta-EH-exterior-nohair-stack-or-retained-bound-envelope.md"
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


def source_register() -> list[dict[str, str]]:
    specs = [
        {
            "source_id": "933_doc",
            "path": "933-Y5-R10-scalar-boundary-owner-or-beta-vacuum-Einstein-gate.md",
            "role": "selected beta EH exterior/no-hair stack",
            "needle": "N1-N6 no-hair + metric-only EH exterior",
        },
        {
            "source_id": "933_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_933_VALIDATION.csv",
            "role": "proves 933 validation passed",
            "needle": "V933_9_validation_rows_ready",
        },
        {
            "source_id": "247_EH_sufficiency",
            "path": "247-local-EH-exterior-sufficiency-stack-no-promotion.md",
            "role": "complete conditional EH sufficiency stack",
            "needle": "local_EH_exterior_sufficiency_stack_complete_as_conditional_theorem_parent_N_gates_open_no_promotion",
        },
        {
            "source_id": "238_metric_only",
            "path": "238-metric-only-exterior-reduction-or-nohair-theorem.md",
            "role": "metric-only exterior audit and no-hair target list",
            "needle": "metric_only_exterior_reduction_sector_audit_partial_nohair_not_derived_no_promotion",
        },
        {
            "source_id": "237_EH_contract",
            "path": "237-local-EH-exterior-action-contract.md",
            "role": "local EH exterior action contract",
            "needle": "local_EH_exterior_action_contract_sharp_metric_only_gate_written_parent_reduction_not_derived_no_promotion",
        },
        {
            "source_id": "230_exterior_vacuum",
            "path": "230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md",
            "role": "exterior vacuum-Einstein sufficient contract",
            "needle": "exterior_vacuum_sufficient_contract_no_parent_local_GR_or_PPN_promotion",
        },
        {
            "source_id": "908_projector_stress",
            "path": "908-Y5-R10-projector-stress-Bianchi-fate-or-retained-PPN-vector.md",
            "role": "projector stress/Bianchi retained PPN vector",
            "needle": "retain_projector_Bianchi_residual",
        },
        {
            "source_id": "local_bounds",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "Will 2014 beta bound row",
            "needle": "R4_beta",
        },
    ]
    rows = []
    for spec in specs:
        path = ROOT / spec["path"]
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


def nohair_stack_audit() -> list[dict[str, str]]:
    specs = [
        (
            "NH934_0_N1_Meff",
            "N1_Meff",
            "source mass is a conserved monopole with source-normalized M_eff",
            "conditional_gate",
            "source measure/worldtube equality still needs parent ownership before full promotion",
            "needed_for_beta_source_M",
        ),
        (
            "NH934_1_N2_no_TF",
            "N2_no_TF",
            "trace-free/shear source vanishes so gamma/slip stays silent",
            "conditional_gate",
            "scalar boundary owner from 932/933 not parent-signed",
            "needed_before_beta_so_first_order_slip_not_hidden",
        ),
        (
            "NH934_2_N3_strict_coframe",
            "N3_universal_strict_coframe",
            "one observed coframe owns matter, clocks, and orbital readout",
            "conditional_gate",
            "same-source calibration and matter descent remain unsigned",
            "needed_to_prevent_frame_split_beta",
        ),
        (
            "NH934_3_N4_exact_relative_memory",
            "N4_exact_relative_memory",
            "relative memory/current is exact, pure gauge, or boundary-cancelled",
            "conditional_gate",
            "boundary primitive/no-tail owner remains conditional",
            "needed_to_remove_Jrel_exterior_hair",
        ),
        (
            "NH934_4_N5_projector_stress",
            "N5_projector_stress_Bianchi_safe",
            "projector stress is zero, exact improvement with no flux, or retained in conserved total stress",
            "open_blocker",
            "projector stress/Bianchi route not closed; retained PPN vector exists",
            "primary_next_target",
        ),
        (
            "NH934_5_N6_auxiliary_nohair",
            "N6_auxiliary_nohair",
            "X/J_rel/V_def carry no exterior propagating degrees",
            "open_blocker",
            "auxiliary no-hair/rank-bracket proof remains unproved",
            "second_hard_target",
        ),
        (
            "NH934_6_metric_only_EH",
            "metric_only_second_order_operator",
            "compact exterior parent action reduces to metric-only EH through second PN order",
            "open_blocker",
            "metric-only exterior reduction is not parent-derived",
            "final_beta_theorem_gate",
        ),
    ]
    rows = []
    for audit_id, gate, requirement, current_status, blocker, role in specs:
        rows.append(
            {
                "audit_id": audit_id,
                "gate": gate,
                "requirement": requirement,
                "current_status": current_status,
                "blocker": blocker,
                "role": role,
                "promotion_allowed_now": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def beta_theorem_chain() -> list[dict[str, str]]:
    return [
        {
            "chain_id": "BETA934_0_stack_premise",
            "step": "assume N1-N6 plus metric-only exterior reduction",
            "mathematical_form": "N1∧N2∧N3∧N4∧N5∧N6∧metric_only_EH",
            "result_if_true": "nonmetric exterior hair is absent or retained below local bounds",
            "current_status": "premise_stack_incomplete",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "BETA934_1_EH_exterior",
            "step": "derive exterior vacuum Einstein equation",
            "mathematical_form": "G_mu_nu + Lambda_eff g_mu_nu = 0 outside compact source collars",
            "result_if_true": "static spherical exterior is in the GR vacuum class",
            "current_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "BETA934_2_Schwarzschild",
            "step": "apply static spherical no-hair/Birkhoff-style consequence",
            "mathematical_form": "ds^2=-(1-2G_eff M_eff/r)dt^2+(1-2G_eff M_eff/r)^-1dr^2+r^2dOmega^2",
            "result_if_true": "second-order weak-field coefficient is GR-like",
            "current_status": "conditional_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "BETA934_3_beta_one",
            "step": "read off PPN beta after same-source calibration",
            "mathematical_form": "g_00=-1+2U-2 beta U^2+O(U^3); Schwarzschild => beta=1",
            "result_if_true": "R4_beta is structurally silent",
            "current_status": "not_promoted",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "chain_id": "BETA934_4_bound_fallback",
            "step": "retain beta residual if theorem stack fails",
            "mathematical_form": "|K_BF_H| <= 7.8e-05/(|C_beta_FM| X_beta)",
            "result_if_true": "R4_beta can become scoreable only after C_beta_FM and X_beta are sourced",
            "current_status": "symbolic_bound_only",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def obstruction_priority() -> list[dict[str, str]]:
    return [
        {
            "priority_id": "OBS934_0_N5_projector_stress",
            "rank": "1",
            "obstruction": "N5_projector_stress_Bianchi_safe",
            "why_first": "Bianchi-visible projector stress can source gamma, beta, preferred-frame terms, or source drift if silently dropped",
            "required_next_test": "prove projector stress is metric-independent/exact-no-flux/conserved-boundary, or retain beta/PPN coefficients",
            "next_target": "935-Y5-R10-N5-projector-stress-zero-or-retained-beta-bound-input.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "priority_id": "OBS934_1_N6_auxiliary_nohair",
            "rank": "2",
            "obstruction": "N6_auxiliary_nohair",
            "why_first": "auxiliary exterior modes spoil Schwarzschild even if projector stress is safe",
            "required_next_test": "rank/bracket/no-pole or mass-gap proof for X/J_rel/V_def",
            "next_target": "after_N5_if_needed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "priority_id": "OBS934_2_metric_only_EH",
            "rank": "3",
            "obstruction": "metric_only_EH_exterior",
            "why_first": "beta=1 needs the actual exterior operator, not just absence of obvious hair",
            "required_next_test": "derive metric-only EH operator through second PN order",
            "next_target": "after_N5_N6",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE934_0_beta_one",
            "claim": "beta=1 is derived",
            "evidence": "N5, N6, and metric-only exterior gates are open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE934_1_metric_only_EH",
            "claim": "compact exterior is metric-only EH",
            "evidence": "older EH contract is conditional and parent reduction is not derived",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE934_2_numeric_beta_bound",
            "claim": "numeric KBFH beta bound is scoreable",
            "evidence": "C_beta_FM and X_beta are missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE934_3_local_GR",
            "claim": "local GR/Newton reduction is complete",
            "evidence": "beta stack is one coefficient gate; source normalization and retained PPN vector remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC934_0_beta_status",
            "decision": "beta_theorem_stack_incomplete",
            "reason": "conditional EH/Schwarzschild chain exists but N5, N6, and metric-only exterior are open",
            "consequence": "beta=1 not promoted",
            "next_action": "attack N5 projector stress first",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC934_1_bound_status",
            "decision": "retain_symbolic_beta_bound",
            "reason": "if theorem fails, beta can still become a bound row once C_beta_FM and X_beta are derived",
            "consequence": "|K_BF_H| <= 7.8e-05/(|C_beta_FM| X_beta) remains nonclaim",
            "next_action": "source C_beta_FM/X_beta only after N5/N6/EH route fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC934_2_next_target",
            "decision": "N5_projector_stress_selected",
            "reason": "projector stress is Bianchi-visible and already has retained PPN/source vector machinery",
            "consequence": "next checkpoint targets zero/improvement/conserved-boundary proof or retained beta coefficients",
            "next_action": "935-Y5-R10-N5-projector-stress-zero-or-retained-beta-bound-input.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
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
    stack_rows: list[dict[str, str]],
    chain_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior = read_csv(OUT / "P8_Y5_BRR545_933_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    stack_complete = len(stack_rows) == 7 and any(row["gate"] == "N5_projector_stress_Bianchi_safe" for row in stack_rows)
    open_blockers = {row["gate"] for row in stack_rows if row["current_status"] == "open_blocker"}
    required_open = {"N5_projector_stress_Bianchi_safe", "N6_auxiliary_nohair", "metric_only_second_order_operator"}
    open_required = required_open.issubset(open_blockers)
    beta_chain = any(row["chain_id"] == "BETA934_3_beta_one" and "beta=1" in row["mathematical_form"] for row in chain_rows)
    fallback = any(row["chain_id"] == "BETA934_4_bound_fallback" and "7.8e-05" in row["mathematical_form"] for row in chain_rows)
    n5_selected = any(row["obstruction"] == "N5_projector_stress_Bianchi_safe" and row["rank"] == "1" for row in obstruction_rows)
    next_selected = any("935-Y5-R10-N5" in row["next_action"] for row in decision_rows)
    no_claims = all(row["valid_for_claim"] == "false" for row in stack_rows + chain_rows + obstruction_rows + decision_rows + claim_rows)
    claims_false = all(row["claim_allowed"] == "false" for row in claim_rows)
    formalization_changed = formalization_changed_after_start()

    add("V934_0_sources_exist_and_needles", sources_ok, "all source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V934_1_prior_933_clean", prior_clean, "P8_Y5_BRR545_933_VALIDATION.csv clean")
    add("V934_2_stack_complete", stack_complete, "N1-N6 plus metric-only EH gates audited")
    add("V934_3_required_open_blockers_recorded", open_required, "N5, N6, and metric-only gates remain open")
    add("V934_4_beta_chain_recorded", beta_chain, "conditional beta=1 chain recorded")
    add("V934_5_bound_fallback_retained", fallback, "symbolic beta KBFH bound retained")
    add("V934_6_N5_selected_first", n5_selected, "N5 projector stress selected as next obstruction")
    add("V934_7_next_target_selected", next_selected, "935-Y5-R10-N5-projector-stress-zero-or-retained-beta-bound-input.md")
    add("V934_8_no_claims_promoted", no_claims, "all generated rows are nonclaim")
    add("V934_9_claim_gates_false", claims_false, "all claim gates remain false")
    add("V934_10_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V934_11_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    stack_rows: list[dict[str, str]],
    chain_rows: list[dict[str, str]],
    obstruction_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 934 - Y5/R10 Beta EH Exterior Nohair Stack Or Retained Bound Envelope

Generated: `{stamp()}`

Status: `Y5_R10_934_beta_EH_nohair_stack_audited_N5_selected_no_claim`

Claim ceiling: `conditional_beta_stack_and_symbolic_bound_only_no_beta_local_GR_or_KBFH_claim`

## Result

The beta route is now sharply fenced.

The conditional theorem is:

```text
N1-N6 no-hair + metric-only EH exterior
=> exterior vacuum Einstein
=> Schwarzschild exterior
=> beta = 1.
```

But the current stack is not closed. The open blockers are:

```text
N5 projector stress / Bianchi safety,
N6 auxiliary no-hair,
metric-only second-order EH exterior operator.
```

So beta is not promoted. The honest fallback remains:

```text
|K_BF_H| <= 7.8e-05/(|C_beta_FM| X_beta),
```

but that is also nonclaim until `C_beta_FM` and `X_beta` are derived or sourced.

The best next target is `N5`: projector stress is Bianchi-visible and can directly contaminate beta, gamma, preferred-frame terms, or source normalization if it is silently dropped.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Nohair Stack Audit

{md_table(stack_rows, ["audit_id", "gate", "requirement", "current_status", "blocker", "role"])}

## Beta Theorem Chain

{md_table(chain_rows, ["chain_id", "step", "mathematical_form", "result_if_true", "current_status"])}

## Obstruction Priority

{md_table(obstruction_rows, ["priority_id", "rank", "obstruction", "why_first", "required_next_test", "next_target"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

`935-Y5-R10-N5-projector-stress-zero-or-retained-beta-bound-input.md`

Try to prove projector stress is zero/gauge-only/exact-no-flux/conserved-boundary. If that fails, retain explicit beta/PPN response coefficients instead of pretending the EH exterior is clean.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    stack_rows = nohair_stack_audit()
    chain_rows = beta_theorem_chain()
    obstruction_rows = obstruction_priority()
    decision_rows = decisions()
    claim_rows = claim_gates()
    validation_rows = validation(sources, stack_rows, chain_rows, obstruction_rows, decision_rows, claim_rows)

    write_csv(
        OUT / "P8_Y5_R10_934_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_934_NOHAIR_STACK_AUDIT.csv",
        stack_rows,
        ["audit_id", "gate", "requirement", "current_status", "blocker", "role", "promotion_allowed_now", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_934_BETA_THEOREM_CHAIN.csv",
        chain_rows,
        ["chain_id", "step", "mathematical_form", "result_if_true", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_934_OBSTRUCTION_PRIORITY.csv",
        obstruction_rows,
        ["priority_id", "rank", "obstruction", "why_first", "required_next_test", "next_target", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_934_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_934_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_934_NEXT_TARGET.csv",
        [
            {
                "next_target": "935-Y5-R10-N5-projector-stress-zero-or-retained-beta-bound-input.md",
                "objective": "prove N5 projector stress is zero/gauge-only/exact-no-flux/conserved-boundary or retain explicit beta/PPN response coefficients",
                "include": "projector stress metric variation, Bianchi safety, exact improvement/no-flux route, retained beta/PPN coefficient fallback",
                "exclude": "beta pass claim, EH exterior claim, dropping projector stress silently, hidden G/M absorption, GitHub action, formalization-workbench edits",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        ],
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_934_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, stack_rows, chain_rows, obstruction_rows, decision_rows, claim_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")
    print("Y5_R10_934_beta_EH_nohair_stack_audited_N5_selected_no_claim")
    print(f"wrote {DOC}")
    print("next target: 935-Y5-R10-N5-projector-stress-zero-or-retained-beta-bound-input.md")


if __name__ == "__main__":
    main()
