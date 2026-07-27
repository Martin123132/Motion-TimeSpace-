from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_908_projector_stress_Bianchi_fate_audited_retained_PPN_vector_nonclaim"
CLAIM_CEILING = "projector_stress_fate_audit_and_retained_PPN_vector_only_no_EH_no_Newton_no_PPN_claim"
NEXT_TARGET = "909-Y5-R10-Hamiltonian-PiM-charge-map-or-retained-projector-PPN-source-pack.md"

SOURCE_SPECS = [
    {
        "source_id": "907_doc",
        "path": ROOT / "907-Y5-R10-post-trace-closure-local-GR-residual-stack-priority.md",
        "needle": "projector/N5 stress fate",
        "role": "handoff selecting projector/Bianchi as the top local-GR residual gate",
    },
    {
        "source_id": "907_next_target",
        "path": OUT / "P8_Y5_R10_907_NEXT_TARGET.csv",
        "needle": "decide the local projector/N5 stress fate",
        "role": "prior selected target",
    },
    {
        "source_id": "907_validation",
        "path": OUT / "P8_Y5_BRR545_907_VALIDATION.csv",
        "needle": "V907_9_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "655_eh_premises",
        "path": OUT / "P8_Y5_R10_655_EH_ONLY_PREMISE_AUDIT.csv",
        "needle": "EHP655_P2_Ward_Euler_ownership",
        "role": "EH-only premise audit showing Ward/Euler ownership and extra-field gaps",
    },
    {
        "source_id": "660_projector_stress",
        "path": OUT / "P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv",
        "needle": "TPS660_1_metric_projector_stress",
        "role": "projector stress vector rows and missing source coefficients",
    },
    {
        "source_id": "660_commutator",
        "path": OUT / "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
        "needle": "CZ660_6_Hilbert_topological_equality",
        "role": "commutator and topological/Hilbert equality blockers",
    },
    {
        "source_id": "661_equality_attempt",
        "path": OUT / "P8_Y5_R10_661_EQUALITY_ATTEMPT.csv",
        "needle": "EQ661_6_residual_fallback",
        "role": "failed equality proof and retained residual fallback",
    },
    {
        "source_id": "663_pim_repair",
        "path": OUT / "P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv",
        "needle": "PR663_0_define_PiM_H",
        "role": "best next derivation route: Hamiltonian/covariant phase space Pi_M",
    },
    {
        "source_id": "789_ward_identity",
        "path": OUT / "P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv",
        "needle": "VWI789_3_Bianchi",
        "role": "Bianchi identity blocks arbitrary source terms",
    },
    {
        "source_id": "790_exchange_stress",
        "path": OUT / "P8_Y5_R10_790_EXCHANGE_STRESS_DECOMPOSITION.csv",
        "needle": "ESD790_1_exchange_longitudinal",
        "role": "exchange-current stress is the primary missing derivation",
    },
    {
        "source_id": "791_ward_zero",
        "path": OUT / "P8_Y5_R10_791_WARD_ZERO_THEOREM_GATE.csv",
        "needle": "WZG791_3_geometric_q_loc_zero",
        "role": "geometric q_loc zero theorem remains unproved",
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
            "what_changed": "audited the projector/N5 stress against zero, gauge-only, boundary-conserved, and retained-residual branches",
            "best_partial_result": "the Bianchi contract is now explicit: T_projector cannot be dropped unless it is theorem-zero, pure gauge with no local flux, conserved boundary-only, or explicitly retained",
            "hard_blockers": "metric variation of Pi_M, chain-map commutator zero, Hilbert/topological equality, Hamiltonian Pi_M integrability, source-frame equality, no boundary tail, and q_P response coefficients",
            "what_is_not_claimed": "projector stress zero, EH exterior, local GR, Newtonian source normalization, PPN pass, R10 pass, or matter conservation by ordinary matter alone",
            "decision": "retain q_P^nu/T_projector as an explicit nonclaim PPN/source residual until a parent Hamiltonian Pi_M map or source-backed coefficient pack closes it",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def projector_fate_audit_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "audit_id": "PFA908_0_theorem_zero",
            "branch": "projector_stress_zero",
            "required_condition": "delta_g Pi_M = 0, [d,Pi_M]J_H = 0, fixed domain/homology, and Pi_M J_H equals the observed Hilbert mass current up to exact zero-flux terms",
            "current_evidence": "660 has conditional metric-independent/topological clauses but chain-map, variation ownership, and Hilbert/topological equality are not parent-derived",
            "blocker": "MISSING_PROJECTOR_STRESS_MAP_AND_HILBERT_TOPOLOGICAL_EQUALITY",
            "fate": "not_signed",
            "selected_branch": False,
        },
        {
            "audit_id": "PFA908_1_gauge_only",
            "branch": "pure_gauge_or_improvement",
            "required_condition": "T_projector^{mu nu} = nabla_alpha B^{alpha mu nu} or local gauge variation with zero compact support flux and no PPN/readout residue",
            "current_evidence": "661 writes an exact-improvement target but leaves R_eq and boundary flux unproved",
            "blocker": "MISSING_ZERO_FLUX_IMPROVEMENT_THEOREM",
            "fate": "not_signed",
            "selected_branch": False,
        },
        {
            "audit_id": "PFA908_2_boundary_conserved",
            "branch": "boundary_only_conserved",
            "required_condition": "nabla_mu T_projector^{mu nu}=0 and integral over compact local boundary gives no source mass, preferred-frame, clock, R10, or PPN contribution",
            "current_evidence": "655 and 789 require boundary/source variation to be silent or explicit; no no-tail/no-flux theorem is signed",
            "blocker": "MISSING_BOUNDARY_NO_TAIL_AND_NO_FLUX_CERTIFICATE",
            "fate": "not_signed",
            "selected_branch": False,
        },
        {
            "audit_id": "PFA908_3_Hamiltonian_PiM_route",
            "branch": "parent_Hamiltonian_charge_map",
            "required_condition": "define Pi_M as the parent Hamiltonian/covariant-phase-space mass charge map with integrability, fixed reference, and same source frame",
            "current_evidence": "663 identifies Pi_M^H as the best next derivation target, but integrability/reference/source-frame clauses remain open",
            "blocker": "MISSING_HAMILTONIAN_PIM_INTEGRABILITY_AND_SOURCE_FRAME",
            "fate": "promising_next_derivation_target_not_closed",
            "selected_branch": False,
        },
        {
            "audit_id": "PFA908_4_retained_residual",
            "branch": "retain_explicit_projector_PPN_source_residual",
            "required_condition": "define q_P^nu := P_loc nabla_mu T_projector^{mu nu} and carry its response coefficients until zeroed or bounded",
            "current_evidence": "660, 789, 790, and 791 all point to retained source/projector residuals when Ward/Bianchi ownership is not signed",
            "blocker": "NO_NUMERIC_RESPONSE_COEFFICIENTS_YET",
            "fate": "selected_nonclaim_bookkeeping_branch",
            "selected_branch": True,
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def bianchi_ward_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "BWG908_0_contract",
            "gate": "Bianchi_conservation_contract",
            "mathematical_statement": "nabla_mu E^{mu nu}=0 forces nabla_mu(T_matter+T_MTS+T_boundary+T_projector)^{mu nu}=0 on shell",
            "status": "identity_contract_explicit",
            "meaning": "the projector sector must be zero, conserved, cancelled by exchange stress, or retained as a residual",
        },
        {
            "gate_id": "BWG908_1_no_silent_drop",
            "gate": "no_silent_projector_deletion",
            "mathematical_statement": "if nabla_mu T_projector^{mu nu} != 0, dropping it violates the metric Bianchi identity or hides a force in matter/source normalization",
            "status": "policy_pass_for_internal_gate",
            "meaning": "do not claim EH/local GR while projector divergence is unowned",
        },
        {
            "gate_id": "BWG908_2_exchange_carrier",
            "gate": "exchange_current_carrier",
            "mathematical_statement": "find T_Q^{mu nu} with nabla_mu T_Q^{mu nu}=-q_P^nu, or prove q_P^nu=0 under local boundary conditions",
            "status": "not_derived",
            "meaning": "790 makes this the primary missing derivation after the Ward split",
        },
        {
            "gate_id": "BWG908_3_local_GR_limit",
            "gate": "local_GR_suppression",
            "mathematical_statement": "local GR requires q_P^nu -> 0 or a source-backed map to gamma-1, beta-1, alpha_i, xi, Gdot/G, anomalous acceleration, clocks, or R10",
            "status": "bound_interface_needed",
            "meaning": "791 says q_loc zero is not derived and response coefficients are missing",
        },
        {
            "gate_id": "BWG908_4_parent_ownership",
            "gate": "parent_Ward_Euler_ownership",
            "mathematical_statement": "all hidden/projector/domain/boundary/source variables must be varied, harmless, or retained",
            "status": "open_fail_for_claim",
            "meaning": "655 blocks EH-only promotion until this is signed",
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def retained_ppn_source_vector_rows(generated_utc: str) -> list[dict[str, object]]:
    p660 = OUT / "P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv"
    c660 = OUT / "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv"
    e661 = OUT / "P8_Y5_R10_661_EQUALITY_ATTEMPT.csv"
    p663 = OUT / "P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv"
    w789 = OUT / "P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv"
    e790 = OUT / "P8_Y5_R10_790_EXCHANGE_STRESS_DECOMPOSITION.csv"
    w791 = OUT / "P8_Y5_R10_791_WARD_ZERO_THEOREM_GATE.csv"
    rows = [
        {
            "vector_id": "RPV908_0_metric_projector_stress",
            "symbol": "c_PiM_g",
            "definition": "coefficient mapping delta_g Pi_M or T_projector^{mu nu} into the local metric equation",
            "units": "dimensionless_after_EH_normalization_or_stress_energy_units",
            "observable_link": "PPN gamma, beta, alpha3, xi; local light bending/time delay/perihelion",
            "needed_input": "delta_g Pi_M stress map or metric-independent no-stress theorem",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP",
            "source_paths": f"{p660};{c660}",
        },
        {
            "vector_id": "RPV908_1_projector_divergence",
            "symbol": "q_P^nu",
            "definition": "P_loc nabla_mu T_projector^{mu nu}, the Bianchi-visible force/source residual from the projector sector",
            "units": "force_density_or_divergence_of_stress_units",
            "observable_link": "matter nonconservation, anomalous acceleration, PPN preferred-location terms, orbital residuals",
            "needed_input": "exchange-current carrier T_Q or q_P zero theorem plus local response coefficients",
            "current_status": "MISSING_EXCHANGE_CURRENT_AND_RESPONSE_MAP",
            "source_paths": f"{w789};{e790};{w791}",
        },
        {
            "vector_id": "RPV908_2_commutator_integral",
            "symbol": "I_commutator",
            "definition": "integral_A [d,Pi_M]J_H contribution to projected source-current drift",
            "units": "same_units_as_projected_source_current_integral",
            "observable_link": "radial M_eff hair, fifth force, R10/R11 source-normalization residuals",
            "needed_input": "parent commutator-zero theorem or sourced I_commutator profile with units",
            "current_status": "MISSING_COMMUTATOR_ZERO_OR_NUMERIC_INTEGRAL",
            "source_paths": f"{p660};{c660};{e661}",
        },
        {
            "vector_id": "RPV908_3_domain_homology_drift",
            "symbol": "c_domain",
            "definition": "variation of S2 representative, domain selector, normal, or homology class used by Pi_M",
            "units": "dimensionless_or_declared_domain_variation_units",
            "observable_link": "PPN alpha1, alpha2, alpha3, xi; Gdot/G; preferred-frame/source-drift rows",
            "needed_input": "topological/domain parent selector theorem or coefficient vector",
            "current_status": "MISSING_DOMAIN_SELECTOR_THEOREM_OR_VECTOR",
            "source_paths": f"{p660};{c660}",
        },
        {
            "vector_id": "RPV908_4_boundary_reference_tail",
            "symbol": "c_boundary",
            "definition": "boundary Hodge/DeWitt/reference subtraction contribution carried by Pi_M or the local exterior action",
            "units": "dimensionless_or_boundary_charge_units",
            "observable_link": "PPN beta, alpha3, xi; Gdot/G; boundary source-mass drift",
            "needed_input": "boundary metric parent origin plus no-reference-hair theorem or coefficient",
            "current_status": "MISSING_BOUNDARY_PROJECTOR_STRESS_INPUT",
            "source_paths": f"{p660};{e661};{w789}",
        },
        {
            "vector_id": "RPV908_5_Hamiltonian_PiM_residual",
            "symbol": "Delta_HPiM",
            "definition": "residual between old topological Pi_M and parent Hamiltonian/covariant-phase-space Pi_M^H after reference/source-frame matching",
            "units": "mass_charge_or_dimensionless_after_M_ref_normalization",
            "observable_link": "measured GM, Newtonian source mass, PPN source coefficients, radial calibration",
            "needed_input": "Hamiltonian charge integrability, fixed reference, same source measure, and exact zero-flux H/topological dictionary",
            "current_status": "MISSING_HAMILTONIAN_PIM_INTEGRABILITY_AND_SOURCE_FRAME",
            "source_paths": f"{p663};{e661}",
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
            "decision_id": "BD908_0_selected_branch",
            "selected_branch": "retain_projector_Bianchi_residual",
            "reason": "zero, gauge-only, and boundary-conserved branches all require unsigned parent clauses; silent deletion would violate the Bianchi discipline we are trying to impose",
            "immediate_next": "try to define Pi_M as a parent Hamiltonian/covariant-phase-space charge map; if that fails, source the retained PPN/source coefficients",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "BD908_1_reopen_zero_branch",
            "selected_branch": "conditional_reopen_only",
            "reason": "projector zero can reopen only if Pi_M^H integrability, Hilbert/source equality, commutator-zero, metric-independence, and boundary no-tail are parent-signed",
            "immediate_next": "do not use projector-zero as an assumption",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE908_0_projector_zero", "projector stress theorem-zero", "blocked: metric/projector variation and Hilbert/topological equality are not parent-derived"),
        ("CGATE908_1_gauge_only", "projector stress pure gauge/improvement", "blocked: zero-flux improvement theorem is not signed"),
        ("CGATE908_2_boundary_conserved", "projector boundary-only conserved", "blocked: no-tail/no-flux and no local PPN/source contribution are not proven"),
        ("CGATE908_3_EH_operator", "EH exterior/local GR operator", "blocked: projector/Bianchi residual must be zeroed or retained before EH promotion"),
        ("CGATE908_4_Newton_PPN", "Newtonian/PPN local-GR pass", "blocked: retained PPN/source vector has no source-backed coefficients"),
        ("CGATE908_5_R10", "R10/local short-range pass", "blocked: no valid MTS alpha row and projector/source residuals not mapped"),
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
            "objective": "attempt the parent Hamiltonian/covariant-phase-space Pi_M charge-map derivation; if it fails, convert the retained projector residual into source-ready PPN/orbital/clock/R10 coefficient rows",
            "include": "Pi_M^H definition, integrability, fixed reference, same source frame, boundary zero-flux dictionary, q_P response coefficients, retained source pack fallback",
            "exclude": "assuming projector zero, using trace finite-alpha evidence, claiming local GR/Newton/PPN/R10, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_907_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_907_VALIDATION.csv")
    return bool(rows) and all(row.get("result") == "pass" for row in rows)


def formalization_changed_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > CUTOFF:
            count += 1
    return count


def source_paths_exist(rows: list[dict[str, object]]) -> bool:
    for row in rows:
        raw = stringify(row.get("source_paths", ""))
        for item in [part.strip() for part in raw.split(";") if part.strip()]:
            if not Path(item).exists():
                return False
    return True


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
    fate_rows_: list[dict[str, object]],
    bianchi_rows_: list[dict[str, object]],
    retained_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        fate_rows_,
        bianchi_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V908_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V908_1_prior_907_clean",
            "result": "pass" if prior_907_clean() else "fail",
            "detail": "P8_Y5_BRR545_907_VALIDATION.csv clean",
        },
        {
            "check_id": "V908_2_projector_zero_not_promoted",
            "result": "pass"
            if all(row["selected_branch"] is False for row in fate_rows_ if row["branch"] != "retain_explicit_projector_PPN_source_residual")
            else "fail",
            "detail": "zero/gauge/boundary/Hamiltonian branches are not promoted",
        },
        {
            "check_id": "V908_3_retained_residual_selected",
            "result": "pass"
            if any(row["branch"] == "retain_explicit_projector_PPN_source_residual" and row["selected_branch"] is True for row in fate_rows_)
            else "fail",
            "detail": "q_P/T_projector retained as a nonclaim residual vector",
        },
        {
            "check_id": "V908_4_Bianchi_no_silent_drop",
            "result": "pass"
            if any(row["gate_id"] == "BWG908_1_no_silent_drop" and row["status"] == "policy_pass_for_internal_gate" for row in bianchi_rows_)
            else "fail",
            "detail": "Bianchi gate forbids dropping projector stress without theorem-zero or retained carrier",
        },
        {
            "check_id": "V908_5_retained_rows_nonclaim_and_missing_inputs",
            "result": "pass"
            if retained_rows_
            and all(row["valid_for_claim"] is False and row["score_ready"] is False and "MISSING_" in stringify(row["current_status"]) for row in retained_rows_)
            else "fail",
            "detail": "retained vector rows remain source-needed and invalid for claim",
        },
        {
            "check_id": "V908_6_retained_source_paths_exist",
            "result": "pass" if source_paths_exist(retained_rows_) else "fail",
            "detail": "every cited retained-vector source path exists",
        },
        {
            "check_id": "V908_7_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all projector/EH/Newton/PPN/R10 claim gates remain false",
        },
        {
            "check_id": "V908_8_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed/score_ready false where present",
        },
        {
            "check_id": "V908_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V908_10_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V908_11_validation_rows_ready",
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
    fate_rows_: list[dict[str, object]],
    bianchi_rows_: list[dict[str, object]],
    retained_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 908 - Y5/R10 Projector Stress Bianchi Fate Or Retained PPN Vector

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the projector/N5 stress is not theorem-zeroed; it is retained as an explicit nonclaim PPN/source residual.** This is the clean route, not the defeat route: the Bianchi identity now acts as a referee. If the parent theory cannot prove the projector sector is zero, pure gauge, or boundary-only conserved, we keep it visible instead of smuggling local GR by deletion.

## Exact 908 Finding
The attempted zero proof fails on the same root structure that has kept showing up: `Pi_M` is not yet a parent-owned Hamiltonian/covariant-phase-space charge map, the Hilbert/topological equality is not signed, metric/projector variation is not zeroed, and the boundary/source tail is not silent. Therefore `q_P^nu := P_loc nabla_mu T_projector^{{mu nu}}` must remain in the local residual stack until it is either parent-zeroed or source-bounded.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Projector Fate Audit
{md_table(fate_rows_)}

## Bianchi/Ward Gate
{md_table(bianchi_rows_)}

## Retained PPN/Source Vector
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
    fate_rows_ = projector_fate_audit_rows(generated_utc)
    bianchi_rows_ = bianchi_ward_gate_rows(generated_utc)
    retained_rows_ = retained_ppn_source_vector_rows(generated_utc)
    decision_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        fate_rows_,
        bianchi_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_908_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_908_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_908_PROJECTOR_STRESS_FATE_AUDIT.csv": fate_rows_,
        "P8_Y5_R10_908_BIANCHI_WARD_GATE.csv": bianchi_rows_,
        "P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv": retained_rows_,
        "P8_Y5_R10_908_BRANCH_DECISION.csv": decision_rows_,
        "P8_Y5_R10_908_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_908_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_908_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "908-Y5-R10-projector-stress-Bianchi-fate-or-retained-PPN-vector.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        fate_rows_,
        bianchi_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_908_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
