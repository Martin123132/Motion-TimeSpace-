from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "933-Y5-R10-scalar-boundary-owner-or-beta-vacuum-Einstein-gate.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
SCRIPT_START_UTC = datetime.now(timezone.utc)


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
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
            "source_id": "932_doc",
            "path": "932-Y5-R10-gamma-zero-parent-condition-or-beta-WEP-pivot.md",
            "role": "conditional gamma-zero theorem and beta pivot",
            "needle": "conditional zero route",
        },
        {
            "source_id": "932_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_932_VALIDATION.csv",
            "role": "proves 932 validation passed",
            "needle": "V932_9_validation_rows_ready",
        },
        {
            "source_id": "229_scalar_owner",
            "path": "229-second-order-beta-or-boundary-scalar-owner.md",
            "role": "scalar boundary symmetry owner and beta reduction",
            "needle": "scalar_boundary_symmetry_owner_derived_sufficient_beta_reduced_to_vacuum_Einstein_gate_no_PPN_promotion",
        },
        {
            "source_id": "230_exterior_vacuum",
            "path": "230-exterior-vacuum-Einstein-branch-or-Jrel-representative.md",
            "role": "exterior vacuum-Einstein conditional beta route",
            "needle": "exterior_vacuum_sufficient_contract_no_parent_local_GR_or_PPN_promotion",
        },
        {
            "source_id": "237_EH_contract",
            "path": "237-local-EH-exterior-action-contract.md",
            "role": "local EH exterior action contract",
            "needle": "local_EH_exterior_action_contract_sharp_metric_only_gate_written_parent_reduction_not_derived_no_promotion",
        },
        {
            "source_id": "238_metric_only",
            "path": "238-metric-only-exterior-reduction-or-nohair-theorem.md",
            "role": "metric-only exterior and no-hair target audit",
            "needle": "metric_only_exterior_reduction_sector_audit_partial_nohair_not_derived_no_promotion",
        },
        {
            "source_id": "247_EH_sufficiency",
            "path": "247-local-EH-exterior-sufficiency-stack-no-promotion.md",
            "role": "complete conditional EH sufficiency stack N1-N6",
            "needle": "local_EH_exterior_sufficiency_stack_complete_as_conditional_theorem_parent_N_gates_open_no_promotion",
        },
        {
            "source_id": "local_bounds",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "R4 beta bound source row",
            "needle": "R4_beta",
        },
    ]
    rows = []
    for spec in specs:
        source_path = ROOT / spec["path"]
        exists = source_path.exists()
        needle_found = exists and spec["needle"] in read_text(source_path)
        rows.append(
            {
                **spec,
                "absolute_path": str(source_path),
                "exists": bool_text(exists),
                "needle_found": bool_text(needle_found),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def scalar_boundary_owner_audit() -> list[dict[str, str]]:
    rows = [
        {
            "audit_id": "SBO933_0_scalar_action_form",
            "clause": "compact boundary action has scalar-only form",
            "mathematical_form": "S_boundary = int_boundary sqrt(|gamma|) F(Y_scalar)",
            "effect": "variation is trace-only if Y_scalar has no hidden tensor/tangential dependence",
            "current_status": "conditional_owner_from_229_243",
            "missing_for_promotion": "derive Y_scalar as the only parent-allowed boundary variable set",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SBO933_1_trace_only_variation",
            "clause": "boundary stress has no trace-free part",
            "mathematical_form": "tau_AB = tau gamma_AB; tau_AB^TF=0",
            "effect": "no anisotropic slip source for gamma at first PPN order",
            "current_status": "conditional_if_scalar_action_owned",
            "missing_for_promotion": "prove delta Y_scalar/delta gamma^AB contributes no trace-free component",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SBO933_2_no_tangential_channel",
            "clause": "no tangential memory shear, K_TF_AB, vector, or l>=2 boundary channel",
            "mathematical_form": "J_rel_A=0; K_TF_AB=0; B_TF=0; vector hair=0 on compact local branch",
            "effect": "removes hidden homogeneous or sourced slip modes",
            "current_status": "not_parent_signed",
            "missing_for_promotion": "derive no-shear/no-vector boundary selection from current MTS parent variables",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SBO933_3_same_source_frame",
            "clause": "boundary scalar response uses same source/readout frame as g_00 calibration",
            "mathematical_form": "M_source = Q_tau = integral_C J_H^H and spatial curvature sees the same charge",
            "effect": "prevents gamma-zero proof from hiding wrong-source calibration",
            "current_status": "not_parent_signed",
            "missing_for_promotion": "Hilbert-worldtube/PiM source equality and Gauss-Poisson readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "audit_id": "SBO933_4_result",
            "clause": "scalar-boundary owner promotion decision",
            "mathematical_form": "SBO933_0..SBO933_3 all parent-signed",
            "effect": "would promote conditional C_gamma_FM=0 route",
            "current_status": "fail_for_current_claim",
            "missing_for_promotion": "at least scalar variable set, no-shear channel, and source-frame proof remain unsigned",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def beta_vacuum_gate() -> list[dict[str, str]]:
    rows = [
        {
            "gate_id": "BVG933_0_gamma_slip_prereq",
            "requirement": "first-order gamma/slip is zero or retained as a bound",
            "mathematical_form": "C_gamma_FM=0 or |K_BF_H| <= 2.3e-05/(|C_gamma_FM|X_FM)",
            "effect_if_pass": "second-order beta can be considered without hiding first-order slip",
            "current_status": "conditional_only",
            "blocker": "scalar-boundary owner not parent-signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BVG933_1_EH_exterior_operator",
            "requirement": "compact exterior parent action reduces to metric-only EH form",
            "mathematical_form": "S_ext[g]=int_E sqrt(-g)(R-2 Lambda_eff)/(16*pi*G_eff) + boundary/reference terms",
            "effect_if_pass": "vacuum field equation outside source is Einstein",
            "current_status": "not_parent_derived",
            "blocker": "metric-only exterior reduction remains open",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BVG933_2_N_nohair_stack",
            "requirement": "N1-N6 no-hair gates remove nonmetric exterior degrees",
            "mathematical_form": "M_eff monopole only; projector stress zero/retained; X/J_rel/V_def no exterior hair; boundary primitive gauge-only",
            "effect_if_pass": "exterior has only source mass and allowed constants",
            "current_status": "open_N5_N6_metric_only",
            "blocker": "projector stress, auxiliary no-hair, and metric-only parent reduction are not proved",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BVG933_3_Schwarzschild_consequence",
            "requirement": "static spherical compact exterior is Schwarzschild",
            "mathematical_form": "ds^2=-(1-2GM/r)dt^2+(1-2GM/r)^-1dr^2+r^2dOmega^2",
            "effect_if_pass": "PPN beta=1 after same source-normalized M",
            "current_status": "conditional_consequence_only",
            "blocker": "BVG933_1 and BVG933_2 are not signed",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "BVG933_4_beta_bound_fallback",
            "requirement": "if beta theorem fails, retain a symbolic bound row",
            "mathematical_form": "|beta-1| = |C_beta_FM X_beta K_BF_H| <= 7.8e-05",
            "effect_if_pass": "could bound K_BF_H once C_beta_FM and X_beta are sourced",
            "current_status": "symbolic_only",
            "blocker": "C_beta_FM, X_beta, and source-normalized second-order response are missing",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return rows


def retained_bound_envelope() -> list[dict[str, str]]:
    return [
        {
            "envelope_id": "RBE933_0_gamma_zero_conditional",
            "row": "R3_gamma",
            "formula": "C_gamma_FM=0 if scalar-boundary/no-shear/same-source clauses are parent-signed",
            "status": "conditional_zero_not_promoted",
            "needed_to_score_or_zero": "SBO933_0..SBO933_3",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "envelope_id": "RBE933_1_beta_symbolic_bound",
            "row": "R4_beta",
            "formula": "|K_BF_H| <= 7.8e-05/(|C_beta_FM| X_beta)",
            "status": "symbolic_bound_only",
            "needed_to_score_or_zero": "C_beta_FM, X_beta, metric-only EH exterior, source-normalized second-order readout",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "envelope_id": "RBE933_2_WEP_deferred",
            "row": "R1_WEP_source_charge",
            "formula": "eta_AB = C_WEP_AB K_BF_H X_WEP_AB",
            "status": "deferred_harder_species_map",
            "needed_to_score_or_zero": "species/source-charge descent and material-composition projection",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC933_0_scalar_owner",
            "decision": "scalar_boundary_owner_not_parent_signed",
            "reason": "existing 229/243 route is a strong sufficient symmetry condition, but current parent variables do not yet force scalar-only boundary data",
            "consequence": "gamma-zero remains conditional",
            "next_action": "do not claim C_gamma_FM=0 until scalar/no-shear/source-frame clauses are parent-derived",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC933_1_beta_route",
            "decision": "beta_reduces_to_EH_exterior_stack",
            "reason": "230/237/238/247 show beta=1 follows from metric-only EH exterior plus no-hair gates",
            "consequence": "beta is a theorem-stack problem, not an independent fit parameter",
            "next_action": "934-Y5-R10-beta-EH-exterior-nohair-stack-or-retained-bound-envelope.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC933_2_WEP_defer",
            "decision": "defer_WEP_until_source_descent",
            "reason": "WEP needs species/source-charge projection and is more delicate than beta after gamma",
            "consequence": "do not use WEP as the next derivation bottleneck unless beta route stalls completely",
            "next_action": "keep WEP as retained residual arena",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "claim_id": "CGATE933_0_gamma_zero",
            "claim": "gamma-zero is parent-derived for current MTS",
            "evidence": "scalar owner remains unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "claim_id": "CGATE933_1_beta_one",
            "claim": "beta=1 is derived",
            "evidence": "EH exterior/no-hair stack is conditional and N5/N6/metric-only gates remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "claim_id": "CGATE933_2_beta_bound_numeric",
            "claim": "numeric beta bound on K_BF_H exists",
            "evidence": "C_beta_FM and X_beta are symbolic",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "claim_id": "CGATE933_3_WEP",
            "claim": "WEP/source-charge safety is derived",
            "evidence": "species/source-charge map deferred",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def formalization_changed_after_start() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for candidate_path in FORMALIZATION.rglob("*"):
        if not candidate_path.is_file():
            continue
        modified_time = datetime.fromtimestamp(candidate_path.stat().st_mtime, timezone.utc)
        if modified_time > SCRIPT_START_UTC:
            changed_count += 1
    return changed_count


def validation(
    sources: list[dict[str, str]],
    scalar_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    envelope_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior_validation = read_csv(OUT / "P8_Y5_BRR545_932_VALIDATION.csv")
    prior_clean = prior_validation and all(row.get("result") == "pass" for row in prior_validation)
    scalar_fail_recorded = any(row["audit_id"] == "SBO933_4_result" and row["current_status"] == "fail_for_current_claim" for row in scalar_rows)
    beta_stack_recorded = any(row["gate_id"] == "BVG933_3_Schwarzschild_consequence" for row in beta_rows)
    beta_bound_retained = any(row["envelope_id"] == "RBE933_1_beta_symbolic_bound" for row in envelope_rows)
    beta_next_selected = any("934-Y5-R10-beta-EH-exterior" in row["next_action"] for row in decision_rows)
    no_claims = all(row["valid_for_claim"] == "false" for row in scalar_rows + beta_rows + envelope_rows + decision_rows + gate_rows)
    gates_false = all(row["claim_allowed"] == "false" for row in gate_rows)
    formalization_changed = formalization_changed_after_start()

    add("V933_0_sources_exist_and_needles", sources_ok, "all source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V933_1_prior_932_clean", prior_clean, "P8_Y5_BRR545_932_VALIDATION.csv clean")
    add("V933_2_scalar_owner_fail_recorded", scalar_fail_recorded, "scalar boundary owner is not parent-signed")
    add("V933_3_beta_stack_recorded", beta_stack_recorded, "beta=1 conditional Schwarzschild/EH stack recorded")
    add("V933_4_beta_bound_retained", beta_bound_retained, "symbolic beta KBFH envelope retained")
    add("V933_5_beta_next_selected", beta_next_selected, "934 beta EH exterior/no-hair target selected")
    add("V933_6_no_claims_promoted", no_claims, "all generated rows are nonclaim")
    add("V933_7_claim_gates_false", gates_false, "all claim gates remain false")
    add("V933_8_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V933_9_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    scalar_rows: list[dict[str, str]],
    beta_rows: list[dict[str, str]],
    envelope_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 933 - Y5/R10 Scalar Boundary Owner Or Beta Vacuum-Einstein Gate

Generated: `{stamp()}`

Status: `Y5_R10_933_scalar_boundary_owner_not_parent_signed_beta_EH_exterior_stack_selected`

Claim ceiling: `scalar_boundary_and_beta_EH_gate_only_no_gamma_beta_WEP_or_local_GR_pass`

## Result

The scalar-boundary route is strong, but still conditional.

If the parent action really restricts compact boundary data to

```text
S_boundary = int_boundary sqrt(|gamma|) F(Y_scalar),
```

with no trace-free/tangential/vector/source-frame leakage, then the boundary stress is trace-only and the `932` gamma-zero route is structurally good.

But current MTS has not yet parent-signed the scalar-only variable set, no-shear channel, or same-source calibration. So `C_gamma_FM=0` is still not a claim.

For beta, the clean route is not WEP first. Beta reduces to:

```text
N1-N6 no-hair + metric-only EH exterior
=> Schwarzschild exterior
=> beta = 1.
```

That stack is already written in older checkpoints, but the open gates remain `N5`, `N6`, and metric-only exterior reduction. If the theorem route fails, retain the symbolic beta envelope:

```text
|K_BF_H| <= 7.8e-05/(|C_beta_FM| X_beta).
```

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## Scalar Boundary Owner Audit

{md_table(scalar_rows, ["audit_id", "clause", "mathematical_form", "effect", "current_status", "missing_for_promotion"])}

## Beta Vacuum-Einstein Gate

{md_table(beta_rows, ["gate_id", "requirement", "mathematical_form", "effect_if_pass", "current_status", "blocker"])}

## Retained Bound Envelope

{md_table(envelope_rows, ["envelope_id", "row", "formula", "status", "needed_to_score_or_zero"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(gate_rows, ["claim_id", "claim", "evidence", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

`934-Y5-R10-beta-EH-exterior-nohair-stack-or-retained-bound-envelope.md`

Attack the beta theorem stack directly: either close the metric-only EH exterior/no-hair gates, or keep beta as a symbolic retained bound row.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    scalar_rows = scalar_boundary_owner_audit()
    beta_rows = beta_vacuum_gate()
    envelope_rows = retained_bound_envelope()
    decision_rows = decisions()
    gate_rows = claim_gates()
    validation_rows = validation(sources, scalar_rows, beta_rows, envelope_rows, decision_rows, gate_rows)

    write_csv(
        OUT / "P8_Y5_R10_933_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_933_SCALAR_BOUNDARY_OWNER_AUDIT.csv",
        scalar_rows,
        ["audit_id", "clause", "mathematical_form", "effect", "current_status", "missing_for_promotion", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_933_BETA_VACUUM_EINSTEIN_GATE.csv",
        beta_rows,
        ["gate_id", "requirement", "mathematical_form", "effect_if_pass", "current_status", "blocker", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_933_RETAINED_BOUND_ENVELOPE.csv",
        envelope_rows,
        ["envelope_id", "row", "formula", "status", "needed_to_score_or_zero", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_933_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_933_CLAIM_GATE.csv",
        gate_rows,
        ["claim_id", "claim", "evidence", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_933_NEXT_TARGET.csv",
        [
            {
                "next_target": "934-Y5-R10-beta-EH-exterior-nohair-stack-or-retained-bound-envelope.md",
                "objective": "close or reject the beta=1 EH exterior/no-hair theorem stack, then retain beta bound envelope if needed",
                "include": "N1-N6 no-hair audit, metric-only EH exterior action, source-normalized Schwarzschild readout, beta symbolic bound fallback",
                "exclude": "beta pass claim, gamma pass claim, WEP source-charge claim, hidden G/M absorption, GitHub action, formalization-workbench edits",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        ],
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_933_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, scalar_rows, beta_rows, envelope_rows, decision_rows, gate_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")
    print("Y5_R10_933_scalar_boundary_owner_not_parent_signed_beta_EH_exterior_stack_selected")
    print(f"wrote {DOC}")
    print("next target: 934-Y5-R10-beta-EH-exterior-nohair-stack-or-retained-bound-envelope.md")


if __name__ == "__main__":
    main()
