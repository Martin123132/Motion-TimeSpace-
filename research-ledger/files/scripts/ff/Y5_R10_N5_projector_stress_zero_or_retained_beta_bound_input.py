from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "935-Y5-R10-N5-projector-stress-zero-or-retained-beta-bound-input.md"
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
            "source_id": "934_doc",
            "path": "934-Y5-R10-beta-EH-exterior-nohair-stack-or-retained-bound-envelope.md",
            "role": "selected N5 projector stress as beta obstruction",
            "needle": "N5 projector stress / Bianchi safety",
        },
        {
            "source_id": "934_validation",
            "path": "source-intake/mts_residuals/P8_Y5_BRR545_934_VALIDATION.csv",
            "role": "proves 934 validation passed",
            "needle": "V934_11_validation_rows_ready",
        },
        {
            "source_id": "908_projector_Bianchi",
            "path": "908-Y5-R10-projector-stress-Bianchi-fate-or-retained-PPN-vector.md",
            "role": "N5 fate audit and retained PPN/source vector",
            "needle": "retain_projector_Bianchi_residual",
        },
        {
            "source_id": "660_projector_vector",
            "path": "source-intake/mts_residuals/P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv",
            "role": "projector stress vector components",
            "needle": "TPS660_1_metric_projector_stress",
        },
        {
            "source_id": "660_commutator",
            "path": "source-intake/mts_residuals/P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
            "role": "commutator/projector zero clauses",
            "needle": "CZ660_3_chain_map_property",
        },
        {
            "source_id": "789_Ward_identity",
            "path": "source-intake/mts_residuals/P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv",
            "role": "Bianchi/Ward identity source discipline",
            "needle": "VWI789_3_Bianchi",
        },
        {
            "source_id": "790_exchange_stress",
            "path": "source-intake/mts_residuals/P8_Y5_R10_790_EXCHANGE_STRESS_DECOMPOSITION.csv",
            "role": "exchange-current carrier and anisotropic stress decomposition",
            "needle": "ESD790_1_exchange_longitudinal",
        },
        {
            "source_id": "791_Ward_zero",
            "path": "source-intake/mts_residuals/P8_Y5_R10_791_WARD_ZERO_THEOREM_GATE.csv",
            "role": "q_loc/Q_matter taxonomy and bound fallback",
            "needle": "WZG791_4_bound_fallback",
        },
        {
            "source_id": "663_PiM_repair",
            "path": "source-intake/mts_residuals/P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv",
            "role": "Hamiltonian/covariant phase-space Pi_M repair route",
            "needle": "PR663_0_define_PiM_H",
        },
        {
            "source_id": "local_bounds",
            "path": "source-intake/local_bounds/local_bound_claims.csv",
            "role": "R4 beta bound",
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


def zero_route_audit() -> list[dict[str, str]]:
    specs = [
        (
            "N5Z935_0_theorem_zero",
            "projector_stress_zero",
            "delta_g Pi_M=0; [d,Pi_M]J_H=0; fixed domain/homology; Pi_M J_H equals observed Hilbert mass current up to exact zero-flux terms",
            "not_signed",
            "metric/projector variation, chain-map property, and Hilbert/topological equality remain unsigned",
        ),
        (
            "N5Z935_1_gauge_improvement",
            "pure_gauge_or_exact_improvement",
            "T_projector^{mu nu}=nabla_alpha B^{alpha mu nu} with zero compact local flux and no readout residue",
            "not_signed",
            "zero-flux improvement theorem and boundary tail silence remain unsigned",
        ),
        (
            "N5Z935_2_boundary_conserved",
            "boundary_only_conserved",
            "nabla_mu T_projector^{mu nu}=0 and compact boundary integral gives no source mass, PPN, clock, R10, or preferred-frame residue",
            "not_signed",
            "no-tail/no-flux/no-local-observable certificate missing",
        ),
        (
            "N5Z935_3_Hamiltonian_PiM",
            "parent_Hamiltonian_charge_map",
            "Pi_M := Pi_M^H from covariant phase-space Hamiltonian charge with integrability, fixed reference, and same source frame",
            "promising_but_not_closed",
            "Delta_symp, B_zero_flux, H_ref, source frame, and topological equivalence remain unsourced",
        ),
        (
            "N5Z935_4_exchange_carrier",
            "exchange_current_carrier",
            "find T_Q^{mu nu} with nabla_mu T_Q^{mu nu}=-q_P^nu so total stress remains Bianchi-compatible",
            "not_derived",
            "T_Q carrier and local metric response coefficients are missing",
        ),
        (
            "N5Z935_5_retained_residual",
            "retain_explicit_N5_beta_PPN_residual",
            "carry q_P^nu/T_projector response coefficients until zeroed or bounded",
            "selected_nonclaim",
            "numeric response coefficients and source-backed amplitudes missing",
        ),
    ]
    rows = []
    for audit_id, branch, mathematical_form, current_status, blocker in specs:
        rows.append(
            {
                "audit_id": audit_id,
                "branch": branch,
                "mathematical_form": mathematical_form,
                "current_status": current_status,
                "blocker": blocker,
                "promotion_allowed_now": "false",
                "selected_fallback": flag(branch == "retain_explicit_N5_beta_PPN_residual"),
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def retained_beta_inputs() -> list[dict[str, str]]:
    specs = [
        (
            "N5B935_0_c_beta_PiM",
            "C_beta_PiM",
            "coefficient mapping T_projector/delta_g Pi_M into beta-1",
            "dimensionless_after_EH_normalization",
            "MISSING_PROJECTOR_STRESS_MAP",
        ),
        (
            "N5B935_1_qP_carrier",
            "q_P^nu",
            "P_loc nabla_mu T_projector^{mu nu}; Bianchi-visible force/source residual",
            "force_density_or_divergence_of_stress_units",
            "MISSING_EXCHANGE_CURRENT_AND_RESPONSE_MAP",
        ),
        (
            "N5B935_2_I_commutator",
            "I_commutator",
            "integral_A [d,Pi_M]J_H source-current drift",
            "same_units_as_projected_source_current_integral",
            "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL",
        ),
        (
            "N5B935_3_boundary_tail",
            "c_boundary",
            "boundary Hodge/DeWitt/reference tail contribution to beta/source mass",
            "dimensionless_or_boundary_charge_units",
            "MISSING_BOUNDARY_PROJECTOR_STRESS_INPUT",
        ),
        (
            "N5B935_4_Hamiltonian_residual",
            "Delta_HPiM",
            "residual between old topological Pi_M and Hamiltonian/covariant phase-space Pi_M^H",
            "mass_charge_or_dimensionless_after_M_ref_normalization",
            "MISSING_HAMILTONIAN_PIM_INTEGRABILITY_AND_SOURCE_FRAME",
        ),
        (
            "N5B935_5_beta_bound",
            "beta_minus_one_N5",
            "|beta-1|_N5 <= 7.8e-05; |K_BF_H| <= 7.8e-05/(|C_beta_N5| X_N5)",
            "dimensionless_bound",
            "MISSING_C_BETA_N5; MISSING_X_N5; MISSING_SOURCE_NORMALIZED_SECOND_ORDER_READOUT",
        ),
    ]
    rows = []
    for input_id, symbol, definition, units, missing in specs:
        rows.append(
            {
                "input_id": input_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "missing_before_score": missing,
                "score_ready": "false",
                "claim_allowed": "false",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        )
    return rows


def local_arena_map() -> list[dict[str, str]]:
    specs = [
        ("N5A935_0_gamma", "R3_gamma", "T_projector trace-free/spatial response can create gamma/slip if not trace-only", "C_gamma_PiM"),
        ("N5A935_1_beta", "R4_beta", "second-order metric response and boundary/reference tail can shift beta", "C_beta_PiM"),
        ("N5A935_2_alpha3_xi", "R7_alpha3;R8_xi", "domain/homology drift or vector leakage can create preferred-frame/location residuals", "C_alpha3_PiM;C_xi_PiM"),
        ("N5A935_3_Gdot", "R9_Gdot", "reference/source-frame drift can mimic source-mass drift", "C_Gdot_PiM"),
        ("N5A935_4_R10", "R10_fifth_force", "source-current drift or boundary tail can look like short-range fifth-force/source normalization", "C_R10_PiM(lambda)"),
    ]
    return [
        {
            "arena_id": arena_id,
            "local_rows": local_rows,
            "hazard": hazard,
            "needed_projection": projection,
            "current_status": "missing_projection_coefficient",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        }
        for arena_id, local_rows, hazard, projection in specs
    ]


def decisions() -> list[dict[str, str]]:
    return [
        {
            "decision_id": "DEC935_0_N5_zero",
            "decision": "N5_zero_not_closed",
            "reason": "theorem-zero, exact-improvement, boundary-conserved, Hamiltonian-PiM, and exchange-carrier routes all retain unsigned parent clauses",
            "consequence": "beta/EH exterior cannot promote through N5",
            "next_action": "retain explicit N5 beta/PPN input pack",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC935_1_best_derivation_route",
            "decision": "Hamiltonian_PiM_still_best_derivation_route",
            "reason": "a parent covariant-phase-space Pi_M can eliminate wrong-current projector stress at the source if integrability/source-frame clauses close",
            "consequence": "attempt Pi_M^H integrability before sourcing many empirical coefficients",
            "next_action": "936-Y5-R10-Hamiltonian-PiM-integrability-or-N5-beta-coefficient-source-pack.md",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "decision_id": "DEC935_2_bound_route",
            "decision": "retained_beta_bound_inputs_staged",
            "reason": "if Pi_M^H route fails, N5 must become a source-backed beta/PPN response vector",
            "consequence": "no beta score until C_beta_N5 and X_N5 are real",
            "next_action": "source coefficient pack only after derivation attempt fails",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]


def claim_gates() -> list[dict[str, str]]:
    return [
        {
            "gate_id": "CGATE935_0_N5_zero",
            "claim": "N5 projector stress is zero/gauge-only/boundary-conserved",
            "evidence": "all zero routes remain unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE935_1_beta_EH",
            "claim": "beta EH exterior stack can pass N5",
            "evidence": "N5 retained residual still active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE935_2_beta_bound_score",
            "claim": "N5 beta bound is numeric/scoreable",
            "evidence": "C_beta_N5 and X_N5 missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "gate_id": "CGATE935_3_local_GR",
            "claim": "local GR/Newton follows after N5",
            "evidence": "N6, metric-only EH, source normalization, and PPN vector remain open",
            "claim_allowed": "false",
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
    zero_rows: list[dict[str, str]],
    beta_inputs: list[dict[str, str]],
    arena_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    rows = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail, "generated_utc": stamp()})

    sources_ok = all(row["exists"] == "true" and row["needle_found"] == "true" for row in sources)
    prior = read_csv(OUT / "P8_Y5_BRR545_934_VALIDATION.csv")
    prior_clean = prior and all(row.get("result") == "pass" for row in prior)
    zero_not_closed = all(row["promotion_allowed_now"] == "false" for row in zero_rows)
    retained_selected = any(row["selected_fallback"] == "true" and row["branch"] == "retain_explicit_N5_beta_PPN_residual" for row in zero_rows)
    beta_inputs_blocked = beta_inputs and all(row["score_ready"] == "false" and row["claim_allowed"] == "false" for row in beta_inputs)
    beta_bound_present = any(row["input_id"] == "N5B935_5_beta_bound" and "7.8e-05" in row["definition"] for row in beta_inputs)
    arena_map_ready = len(arena_rows) == 5 and all(row["valid_for_claim"] == "false" for row in arena_rows)
    next_selected = any("936-Y5-R10-Hamiltonian-PiM" in row["next_action"] for row in decision_rows)
    no_claims = all(row["valid_for_claim"] == "false" for row in zero_rows + beta_inputs + arena_rows + decision_rows + claim_rows)
    claims_false = all(row["claim_allowed"] == "false" for row in claim_rows)
    formalization_changed = formalization_changed_after_start()

    add("V935_0_sources_exist_and_needles", sources_ok, "all source paths exist and needles are present" if sources_ok else "missing source path or needle")
    add("V935_1_prior_934_clean", prior_clean, "P8_Y5_BRR545_934_VALIDATION.csv clean")
    add("V935_2_zero_routes_not_promoted", zero_not_closed, "all N5 zero routes remain unpromoted")
    add("V935_3_retained_residual_selected", retained_selected, "explicit N5 beta/PPN residual fallback selected")
    add("V935_4_beta_inputs_blocked", beta_inputs_blocked, "retained beta inputs are staged but blocked")
    add("V935_5_beta_bound_present", beta_bound_present, "7.8e-05 beta bound envelope retained")
    add("V935_6_arena_map_ready", arena_map_ready, "N5 hazards mapped to gamma/beta/preferred/R10 arenas")
    add("V935_7_next_target_selected", next_selected, "936-Y5-R10-Hamiltonian-PiM-integrability-or-N5-beta-coefficient-source-pack.md")
    add("V935_8_no_claims_promoted", no_claims, "all generated rows are nonclaim")
    add("V935_9_claim_gates_false", claims_false, "all claim gates remain false")
    add("V935_10_formalization_workbench_untouched", formalization_changed == 0, f"formalization_changed_after_start={formalization_changed}")
    add("V935_11_validation_rows_ready", True, "validation table constructed")
    return rows


def write_doc(
    sources: list[dict[str, str]],
    zero_rows: list[dict[str, str]],
    beta_inputs: list[dict[str, str]],
    arena_rows: list[dict[str, str]],
    decision_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    validation_rows: list[dict[str, str]],
) -> None:
    text = f"""# 935 - Y5/R10 N5 Projector Stress Zero Or Retained Beta Bound Input

Generated: `{stamp()}`

Status: `Y5_R10_935_N5_projector_stress_zero_not_closed_retained_beta_PPN_inputs_staged`

Claim ceiling: `N5_projector_stress_fate_and_retained_bound_inputs_only_no_beta_EH_or_local_GR_pass`

## Result

N5 does not close yet.

The zero routes remain unsigned:

```text
delta_g Pi_M = 0,
[d,Pi_M]J_H = 0,
Pi_M J_H = observed Hilbert mass current + exact zero-flux terms,
T_projector = exact/gauge improvement with no compact flux,
or boundary-only conserved with no local observable tail.
```

The Bianchi rule is therefore active: projector stress cannot be silently dropped from the beta/EH exterior stack.

The retained beta fallback is staged as:

```text
|beta-1|_N5 <= 7.8e-05,
|K_BF_H| <= 7.8e-05/(|C_beta_N5| X_N5),
```

but it is not scoreable because `C_beta_N5`, `X_N5`, projector stress amplitudes, exchange-current carrier, commutator integral, and Hamiltonian Pi_M residuals are still missing.

The best next derivation route is still parent Hamiltonian/covariant phase-space `Pi_M^H`: if that closes, it can kill the wrong-current projector problem at the root.

## Source Register

{md_table(sources, ["source_id", "path", "role", "needle_found", "valid_for_claim"])}

## N5 Zero Route Audit

{md_table(zero_rows, ["audit_id", "branch", "mathematical_form", "current_status", "blocker", "selected_fallback"])}

## Retained Beta Inputs

{md_table(beta_inputs, ["input_id", "symbol", "definition", "missing_before_score", "score_ready", "claim_allowed"])}

## Local Arena Map

{md_table(arena_rows, ["arena_id", "local_rows", "hazard", "needed_projection", "current_status"])}

## Decision Ledger

{md_table(decision_rows, ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim"])}

## Claim Gates

{md_table(claim_rows, ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim"])}

## Validation

{md_table(validation_rows, ["check_id", "result", "detail", "generated_utc"])}

## Next Target

`936-Y5-R10-Hamiltonian-PiM-integrability-or-N5-beta-coefficient-source-pack.md`

Try to make `Pi_M` a parent Hamiltonian/covariant-phase-space charge map with integrability, fixed reference, same source frame, and zero-flux equivalence. If that fails, fill source-backed N5 beta/PPN coefficient rows.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    sources = source_register()
    zero_rows = zero_route_audit()
    beta_inputs = retained_beta_inputs()
    arena_rows = local_arena_map()
    decision_rows = decisions()
    claim_rows = claim_gates()
    validation_rows = validation(sources, zero_rows, beta_inputs, arena_rows, decision_rows, claim_rows)

    write_csv(
        OUT / "P8_Y5_R10_935_SOURCE_REGISTER.csv",
        sources,
        ["source_id", "path", "absolute_path", "role", "needle", "exists", "needle_found", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_935_N5_ZERO_ROUTE_AUDIT.csv",
        zero_rows,
        ["audit_id", "branch", "mathematical_form", "current_status", "blocker", "promotion_allowed_now", "selected_fallback", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_935_RETAINED_BETA_BOUND_INPUTS.csv",
        beta_inputs,
        ["input_id", "symbol", "definition", "units", "missing_before_score", "score_ready", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_935_LOCAL_ARENA_MAP.csv",
        arena_rows,
        ["arena_id", "local_rows", "hazard", "needed_projection", "current_status", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_935_DECISION_LEDGER.csv",
        decision_rows,
        ["decision_id", "decision", "reason", "consequence", "next_action", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_935_CLAIM_GATE.csv",
        claim_rows,
        ["gate_id", "claim", "evidence", "claim_allowed", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_R10_935_NEXT_TARGET.csv",
        [
            {
                "next_target": "936-Y5-R10-Hamiltonian-PiM-integrability-or-N5-beta-coefficient-source-pack.md",
                "objective": "make Pi_M a parent Hamiltonian/covariant-phase-space charge map or fill source-backed N5 beta/PPN coefficient rows",
                "include": "Pi_M^H definition, integrability, fixed reference, same source frame, zero-flux topological equivalence, N5 beta coefficient fallback",
                "exclude": "projector zero assumption, beta pass claim, EH exterior claim, hidden source calibration, GitHub action, formalization-workbench edits",
                "valid_for_claim": "false",
                "generated_utc": stamp(),
            }
        ],
        ["next_target", "objective", "include", "exclude", "valid_for_claim", "generated_utc"],
    )
    write_csv(
        OUT / "P8_Y5_BRR545_935_VALIDATION.csv",
        validation_rows,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_doc(sources, zero_rows, beta_inputs, arena_rows, decision_rows, claim_rows, validation_rows)

    failures = [row for row in validation_rows if row["result"] != "pass"]
    if failures:
        raise SystemExit(f"validation failed: {failures}")
    print("Y5_R10_935_N5_projector_stress_zero_not_closed_retained_beta_PPN_inputs_staged")
    print(f"wrote {DOC}")
    print("next target: 936-Y5-R10-Hamiltonian-PiM-integrability-or-N5-beta-coefficient-source-pack.md")


if __name__ == "__main__":
    main()
