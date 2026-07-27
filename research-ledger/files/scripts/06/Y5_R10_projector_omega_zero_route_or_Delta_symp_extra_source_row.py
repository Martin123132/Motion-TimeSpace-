from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_913_projector_omega_zero_route_attempted_not_parent_signed_Delta_symp_projector_source_rows_retained_nonclaim"
CLAIM_CEILING = "projector_omega_zero_route_and_Delta_symp_projector_source_rows_only_no_EH_no_Htau_no_PiM_H_no_local_GR_claim"
NEXT_TARGET = "914-Y5-R10-topological-absolute-PiM-parent-clause-or-projector-source-bound-pack.md"

SOURCE_SPECS = [
    {
        "source_id": "912_doc",
        "path": ROOT / "912-Y5-R10-EH-core-symplectic-baseline-vs-extra-sector-omega-ledger.md",
        "needle": "the next useful derivation target is the projector/Pi_M sector",
        "role": "handoff selecting projector omega",
    },
    {
        "source_id": "912_validation",
        "path": OUT / "P8_Y5_BRR545_912_VALIDATION.csv",
        "needle": "V912_10_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "912_extra_omega",
        "path": OUT / "P8_Y5_R10_912_EXTRA_SECTOR_OMEGA_LEDGER.csv",
        "needle": "ESO912_0_projector",
        "role": "projector omega selected next",
    },
    {
        "source_id": "912_delta_symp_extra",
        "path": OUT / "P8_Y5_R10_912_DELTA_SYMP_EXTRA_ROWS.csv",
        "needle": "DSE912_0_projector",
        "role": "Delta_symp_projector source row to refine",
    },
    {
        "source_id": "454_pim_algebra_doc",
        "path": ROOT / "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "needle": "conditional_symplectic_projector_theorem",
        "role": "Pi_M algebra and variation warning",
    },
    {
        "source_id": "454_pim_contract",
        "path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "needle": "PM5_projector_variation_owned",
        "role": "Pi_M algebra and variation ownership contract",
    },
    {
        "source_id": "455_flux_doc",
        "path": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "needle": "topological_current_route",
        "role": "topological mass-current route and closure blockers",
    },
    {
        "source_id": "456_variation_doc",
        "path": ROOT / "456-PiM-projector-variation-stress-ledger.md",
        "needle": "topological_zero_stress_route",
        "role": "projector variation stress and Hodge no-go",
    },
    {
        "source_id": "456_variation_contract",
        "path": OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "needle": "PV1_topological_absolute_charge_route",
        "role": "topological route, Hodge no-go, and retained stress contract",
    },
    {
        "source_id": "660_commutator_audit",
        "path": OUT / "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
        "needle": "CZ660_1_metric_independent_projector",
        "role": "projector commutator/metric-independence clauses",
    },
    {
        "source_id": "908_retained_vector",
        "path": OUT / "P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv",
        "needle": "RPV908_0_metric_projector_stress",
        "role": "retained q_P and c_PiM_g rows",
    },
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def stringify(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return "" if value is None else str(value)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: stringify(row.get(field, "")) for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def has_needle(path: Path, needle: str) -> bool:
    return path.exists() and needle in read_text(path)


def md_table(rows: list[dict[str, object]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [stringify(row.get(field, "")).replace("\n", " ").replace("|", "/") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows(generated_utc: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for spec in SOURCE_SPECS:
        path = Path(spec["path"])
        rows.append(
            {
                "source_id": spec["source_id"],
                "path": path,
                "exists": path.exists(),
                "needle_check": "pass" if has_needle(path, str(spec["needle"])) else "fail",
                "role": spec["role"],
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def nonclaim_summary_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "what_changed": "attempted the projector omega zero route and split topological absolute PiM from Hodge/DeWitt metric-dependent PiM",
            "best_partial_result": "projector omega has an exact conditional zero theorem if PiM is parent-derived as metric-independent absolute cohomology charge data with fixed topology, wedge/topological action, and no boundary/domain flux",
            "hard_blockers": "parent fixed S2/domain theorem, metric-independent PiM construction, topological/wedge source-normalization action, Hilbert/topological equality, chain-map property, boundary no-flux, and source calibration",
            "what_is_not_claimed": "omega_projector zero, projector stress zero, EH local exterior, integrable H_tau, parent-owned PiM_H, Newtonian limit, PPN pass, or local GR",
            "decision": "zero route not parent-signed; retain Delta_symp_projector, q_P^nu, and c_PiM_g while selecting topological absolute PiM parent clause as the next derivation target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def zero_route_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "clause_id": "ZP913_0_fixed_topology",
            "needed_statement": "compact local exterior topology and oriented S2 class are parent-selected before readout",
            "mathematical_form": "Sigma_ext ~= S2 x I and [S2] fixed by parent/domain theorem",
            "current_status": "conditional_open",
            "zero_effect": "prevents projector/domain motion from contributing omega_projector",
        },
        {
            "clause_id": "ZP913_1_metric_independent_PiM",
            "needed_statement": "Pi_M is absolute cohomology/charge data, not a Hodge/Green/DeWitt/readout projector",
            "mathematical_form": "delta_g Pi_M=0 and Pi_M J=ell_M(J) omega_M_top with ell_M topological",
            "current_status": "conditional_topological_route_not_parent_signed",
            "zero_effect": "kills bulk metric projector stress and local omega_projector",
        },
        {
            "clause_id": "ZP913_2_topological_action",
            "needed_statement": "the Pi_M/source-normalization term uses wedge/topological pairing and no metric inner product in the compact bulk",
            "mathematical_form": "S_PiM ~ integral lambda_M wedge d(Pi_M J) or class pairing with no sqrt(-g), star, Delta_g, or Green operator dependence",
            "current_status": "not_parent_derived",
            "zero_effect": "prevents topological label from smuggling metric dependence through the action",
        },
        {
            "clause_id": "ZP913_3_closed_generator",
            "needed_statement": "mass generator is closed and normalized on the allowed exterior complex",
            "mathematical_form": "d omega_M_top=0 and integral_S2 omega_M_top=1",
            "current_status": "formal_topological_shape_available_not_parent_owned",
            "zero_effect": "removes ell_M(J_H)d omega_M contribution",
        },
        {
            "clause_id": "ZP913_4_chain_map_domain",
            "needed_statement": "Pi_M commutes with d on the allowed Hilbert/source-current domain",
            "mathematical_form": "[d,Pi_M]J_H=0 for allowed J_H and dJ_H in domain(Pi_M)",
            "current_status": "not_parent_derived",
            "zero_effect": "zeros commutator/source-current contribution to projector flux",
        },
        {
            "clause_id": "ZP913_5_Hilbert_topological_equality",
            "needed_statement": "closed topological mass current equals observed Hilbert Pi_M mass current up to exact zero-flux terms",
            "mathematical_form": "Pi_M J_H = J_M_top + dB_zero with integral_boundary dB_zero=0",
            "current_status": "not_derived_key_blocker",
            "zero_effect": "prevents zeroing the wrong conserved current",
        },
        {
            "clause_id": "ZP913_6_boundary_domain_no_flux",
            "needed_statement": "boundary/domain variation has no compact mass, shear, vector, radial, time, range, or source flux",
            "mathematical_form": "integral_boundary Pi_M K_owner=0 or constant_global with partial_{t,r,A,lambda}=0",
            "current_status": "fail_open",
            "zero_effect": "prevents boundary-only projector stress from becoming local PPN/source hair",
        },
        {
            "clause_id": "ZP913_7_no_readout_mask",
            "needed_statement": "post-fit/readout projectors never enter the parent variation",
            "mathematical_form": "delta S_parent has no P_read or fitted Pi_M masks",
            "current_status": "policy_written_not_a_positive_derivation",
            "zero_effect": "blocks fake projector zero by construction after scoring",
        },
    ]
    for row in rows:
        row["parent_signed"] = False
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def route_fate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "route_id": "PR913_0_absolute_topological_PiM",
            "route": "metric_independent_absolute_charge",
            "mathematical_form": "Pi_M J = ell_M(J) omega_M_top; delta_g Pi_M=0; S_PiM topological/wedge in compact bulk",
            "fate": "best_zero_route_but_not_parent_signed",
            "reason": "conditional topological route exists, but fixed topology/domain, topological action, Hilbert equality, and boundary no-flux are not derived",
            "selected_for_next": True,
        },
        {
            "route_id": "PR913_1_Hodge_DeWitt_PiM",
            "route": "metric_dependent_Hodge_or_DeWitt_projector",
            "mathematical_form": "Pi_H(g) uses star, Delta_g, Green operator, or DeWitt inner product",
            "fate": "not_zero_safe",
            "reason": "metric dependence generically contributes delta_g Pi_M and omega_projector; cannot support local-GR reduction unless stress is cancelled or retained",
            "selected_for_next": False,
        },
        {
            "route_id": "PR913_2_boundary_only_projector",
            "route": "boundary_only_nohair",
            "mathematical_form": "omega_projector has no compact bulk support but leaves boundary/corner terms",
            "fate": "open_not_signed",
            "reason": "boundary no-hair/no-flux/no-vector/no-radial theorem is fail-open",
            "selected_for_next": False,
        },
        {
            "route_id": "PR913_3_owned_multiplier",
            "route": "lambda_M_or_projector_constraint",
            "mathematical_form": "E_lambdaM=0 or constraint imposes projector closure while stress is gauge/topological",
            "fate": "closure_only_unless_independently_owned",
            "reason": "no first-class/gauge/topological origin for lambda_M stress is present",
            "selected_for_next": False,
        },
        {
            "route_id": "PR913_4_retained_source_row",
            "route": "retain_Delta_symp_projector",
            "mathematical_form": "Delta_symp_projector = |int_S i_tau omega_projector|/M_ref with q_P^nu and c_PiM_g response rows",
            "fate": "selected_fallback_nonclaim",
            "reason": "required if any zero-route clause remains unsigned",
            "selected_for_next": False,
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def retained_source_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "PSR913_0_Delta_symp_projector",
            "symbol": "Delta_symp_projector",
            "definition": "mass-normalized projector/Pi_M symplectic obstruction contribution",
            "formula": "|integral_S i_tau omega_projector|/M_ref",
            "units": "dimensionless",
            "observable_link": "q_P^nu; c_PiM_g; gamma; beta; alpha3; xi; measured GM drift",
            "required_input": "projector omega-zero theorem or parent/source-backed coefficient",
            "current_status": "MISSING_PROJECTOR_OMEGA_ZERO_OR_COEFFICIENT",
        },
        {
            "source_id": "PSR913_1_c_PiM_g",
            "symbol": "c_PiM_g",
            "definition": "coefficient mapping delta_g Pi_M or retained projector stress into the local metric equation",
            "formula": "T_projector^{mu nu}/T_EH_scale or route-specific dimensionless normalization",
            "units": "dimensionless_after_EH_normalization_or_stress_energy_units",
            "observable_link": "gamma; beta; alpha3; xi; light/time/orbital residuals",
            "required_input": "metric projector stress map, topological no-stress theorem, or coefficient/profile",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP",
        },
        {
            "source_id": "PSR913_2_q_P",
            "symbol": "q_P^nu",
            "definition": "Bianchi-visible divergence of retained projector stress",
            "formula": "P_loc nabla_mu T_projector^{mu nu}",
            "units": "force_density_or_divergence_of_stress_units",
            "observable_link": "matter nonconservation; anomalous acceleration; preferred-frame/location PPN rows",
            "required_input": "q_P zero theorem, exchange-current carrier T_Q, or response coefficients",
            "current_status": "MISSING_EXCHANGE_CURRENT_AND_RESPONSE_MAP",
        },
        {
            "source_id": "PSR913_3_projector_boundary_flux",
            "symbol": "B_P_flux",
            "definition": "compact boundary/corner mass flux from Pi_M/projector variation",
            "formula": "integral_boundary Pi_M K_owner / M_ref",
            "units": "dimensionless",
            "observable_link": "radial source hair; beta; xi; Gdot; measured GM drift",
            "required_input": "boundary no-flux theorem or bounded flux coefficient",
            "current_status": "MISSING_BOUNDARY_NO_FLUX_INPUT",
        },
        {
            "source_id": "PSR913_4_projector_commutator",
            "symbol": "I_commutator",
            "definition": "projector/source-current commutator contribution",
            "formula": "integral_A [d,Pi_M]J_H / M_ref",
            "units": "dimensionless_or_mass_current_normalized",
            "observable_link": "radial M_eff hair; fifth force; R10/R11 source-normalization residuals",
            "required_input": "chain-map theorem [d,Pi_M]=0 or sourced commutator integral",
            "current_status": "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL",
        },
    ]
    for row in rows:
        row["score_ready"] = False
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "decision_id": "BD913_0_zero_route",
            "branch": "projector_omega_zero",
            "verdict": "conditional_theorem_written_not_parent_signed",
            "reason": "omega_projector vanishes if Pi_M is a parent-owned metric-independent topological charge map with topological action and zero boundary/domain flux, but current evidence does not sign those clauses",
            "policy": "do not claim projector zero; use topological absolute PiM parent clause as next derivation target",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "BD913_1_retained_rows",
            "branch": "Delta_symp_projector_source_pack",
            "verdict": "staged_unfilled_nonclaim",
            "reason": "if topological parent route fails, Delta_symp_projector, c_PiM_g, q_P, boundary flux, and commutator rows must be filled or bounded",
            "policy": "retained rows stay score_ready=false until theorem-zero or real coefficient/source inputs exist",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE913_0_omega_projector_zero", "omega_projector theorem-zero", "blocked: topological absolute PiM parent clauses are unsigned"),
        ("CGATE913_1_Hodge_zero_safe", "Hodge/DeWitt projector is zero-stress", "blocked: metric dependence generically gives projector stress unless retained/cancelled"),
        ("CGATE913_2_boundary_no_flux", "boundary-only projector stress is harmless", "blocked: boundary no-flux/no-hair theorem is fail-open"),
        ("CGATE913_3_Delta_symp_projector_scored", "Delta_symp_projector scored/bounded", "blocked: no coefficient/source row supplied"),
        ("CGATE913_4_EH_Htau_PiM", "EH/integrable H_tau/PiM_H", "blocked: projector omega remains open and source equality is unproved"),
        ("CGATE913_5_local_GR", "Newton/PPN/local GR reduction", "blocked: projector/source/PPN rows remain retained"),
    ]
    return [
        {
            "gate_id": gate_id,
            "claim": claim,
            "claim_allowed": False,
            "blocker": blocker,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
        for gate_id, claim, blocker in gates
    ]


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to parent-sign the topological absolute PiM clause: fixed S2/domain, metric-independent charge map, wedge/topological action, Hilbert/topological equality, and zero boundary flux; if not, fill the projector source-bound pack",
            "include": "absolute cohomology PiM, fixed topology/domain selector, no Hodge/Green/DeWitt dependence, chain-map property, boundary no-flux, c_PiM_g/q_P/Delta_symp_projector fallback",
            "exclude": "assuming projector omega vanishes, treating Hodge PiM as stress-free, claiming EH/local GR, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_912_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_912_VALIDATION.csv")
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF:
            count += 1
    return count


def all_generated_rows_nonclaim(row_groups: list[list[dict[str, object]]]) -> bool:
    for group in row_groups:
        for row in group:
            if "valid_for_claim" in row and stringify(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and stringify(row["claim_allowed"]).lower() != "false":
                return False
            if "score_ready" in row and stringify(row["score_ready"]).lower() != "false":
                return False
    return True


def validation_rows(
    generated_utc: str,
    source_rows_: list[dict[str, object]],
    summary_rows_: list[dict[str, object]],
    zero_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    retained_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        zero_rows_,
        route_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V913_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V913_1_prior_912_clean",
            "result": "pass" if prior_912_clean() else "fail",
            "detail": "P8_Y5_BRR545_912_VALIDATION.csv clean",
        },
        {
            "check_id": "V913_2_zero_route_not_parent_signed",
            "result": "pass" if zero_rows_ and all(row["parent_signed"] is False for row in zero_rows_) else "fail",
            "detail": "all projector zero-route clauses remain unsigned",
        },
        {
            "check_id": "V913_3_topological_route_selected_next",
            "result": "pass"
            if any(row["route"] == "metric_independent_absolute_charge" and row["selected_for_next"] is True for row in route_rows_)
            else "fail",
            "detail": "topological absolute PiM route selected as next derivation target",
        },
        {
            "check_id": "V913_4_Hodge_route_not_zero_safe",
            "result": "pass"
            if any(row["route"] == "metric_dependent_Hodge_or_DeWitt_projector" and row["fate"] == "not_zero_safe" for row in route_rows_)
            else "fail",
            "detail": "Hodge/DeWitt projector is not treated as stress-free",
        },
        {
            "check_id": "V913_5_retained_source_rows_nonclaim",
            "result": "pass"
            if retained_rows_
            and all(row["valid_for_claim"] is False and row["score_ready"] is False and "MISSING_" in stringify(row["current_status"]) for row in retained_rows_)
            else "fail",
            "detail": "Delta_symp_projector/q_P/c_PiM_g rows remain missing-input and invalid for claim",
        },
        {
            "check_id": "V913_6_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all projector/EH/Htau/PiM/local-GR claim gates remain false",
        },
        {
            "check_id": "V913_7_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed/score_ready false where present",
        },
        {
            "check_id": "V913_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V913_9_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V913_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_markdown(
    path: Path,
    generated_utc: str,
    summary_rows_: list[dict[str, object]],
    source_rows_: list[dict[str, object]],
    zero_rows_: list[dict[str, object]],
    route_rows_: list[dict[str, object]],
    retained_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 913 - Y5/R10 Projector Omega Zero Route Or Delta Symp Extra Source Row

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the projector omega zero route is conditionally sharp, but not parent-signed.** The safe route is not a Hodge/DeWitt projector pretending to be quiet. The safe route is a metric-independent absolute/topological `Pi_M` with fixed topology/domain, topological action, chain-map property, Hilbert/topological equality, and zero boundary flux. Current evidence does not sign that full chain, so `Delta_symp_projector`, `q_P^nu`, and `c_PiM_g` stay retained.

## Exact 913 Finding
The zero theorem would be:

```text
Pi_M J = ell_M(J) omega_M_top
delta_g Pi_M = 0
integral_S i_tau omega_projector = 0
```

but only if the parent theory owns the topology, the charge map, the action pairing, the source-current domain, and the boundary/domain no-flux clauses. Hodge/DeWitt implementations remain stress-bearing unless a separate cancellation theorem is supplied.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Projector Zero Route Clauses
{md_table(zero_rows_)}

## Route Fate Audit
{md_table(route_rows_)}

## Retained Projector Source Rows
{md_table(retained_rows_)}

## Branch Decision
{md_table(decision_rows_)}

## Claim Gate
{md_table(claim_rows_)}

## Next Target
{md_table(next_rows_)}

## Validation
{md_table(validation_rows_)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    source_rows_ = source_register_rows(generated_utc)
    summary_rows_ = nonclaim_summary_rows(generated_utc)
    zero_rows_ = zero_route_clause_rows(generated_utc)
    route_rows_ = route_fate_rows(generated_utc)
    retained_rows_ = retained_source_rows(generated_utc)
    decision_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        zero_rows_,
        route_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_913_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_913_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_913_PROJECTOR_ZERO_ROUTE_CLAUSES.csv": zero_rows_,
        "P8_Y5_R10_913_ROUTE_FATE_AUDIT.csv": route_rows_,
        "P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv": retained_rows_,
        "P8_Y5_R10_913_BRANCH_DECISION.csv": decision_rows_,
        "P8_Y5_R10_913_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_913_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_913_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "913-Y5-R10-projector-omega-zero-route-or-Delta-symp-extra-source-row.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        zero_rows_,
        route_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_913_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
