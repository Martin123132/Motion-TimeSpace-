from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_914_topological_absolute_PiM_clause_attempted_not_parent_signed_projector_bound_pack_retained_nonclaim"
CLAIM_CEILING = "topological_absolute_PiM_parent_clause_and_projector_source_bound_pack_only_no_projector_zero_no_Newton_PPN_or_local_GR_claim"
DOC_NAME = "914-Y5-R10-topological-absolute-PiM-parent-clause-or-projector-source-bound-pack.md"
NEXT_TARGET = "915-Y5-R10-Hilbert-topological-mass-current-equality-or-projector-bound-pack-fill.md"

SOURCE_SPECS = [
    {
        "source_id": "913_doc",
        "path": ROOT / "913-Y5-R10-projector-omega-zero-route-or-Delta-symp-extra-source-row.md",
        "needle": "the projector omega zero route is conditionally sharp, but not parent-signed",
        "role": "immediate handoff selecting topological absolute PiM",
    },
    {
        "source_id": "913_validation",
        "path": OUT / "P8_Y5_BRR545_913_VALIDATION.csv",
        "needle": "V913_10_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "913_zero_clauses",
        "path": OUT / "P8_Y5_R10_913_PROJECTOR_ZERO_ROUTE_CLAUSES.csv",
        "needle": "ZP913_5_Hilbert_topological_equality",
        "role": "unsigned zero-route clauses",
    },
    {
        "source_id": "913_retained_rows",
        "path": OUT / "P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv",
        "needle": "PSR913_0_Delta_symp_projector",
        "role": "projector source-bound fallback rows",
    },
    {
        "source_id": "454_pim_algebra_doc",
        "path": ROOT / "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "needle": "conditional_symplectic_projector_theorem",
        "role": "PiM algebra and fixed S2 warning",
    },
    {
        "source_id": "454_pim_contract",
        "path": OUT / "P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "needle": "PM0_fixed_exterior_topology",
        "role": "PiM algebra contract",
    },
    {
        "source_id": "455_flux_doc",
        "path": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "needle": "topological_current_route",
        "role": "topological mass-current route and equality blocker",
    },
    {
        "source_id": "455_flux_contract",
        "path": OUT / "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "needle": "FC5_topological_mass_current_origin",
        "role": "flux-closure/topological current contract",
    },
    {
        "source_id": "456_variation_doc",
        "path": ROOT / "456-PiM-projector-variation-stress-ledger.md",
        "needle": "topological_zero_stress_route",
        "role": "projector variation stress and Hodge rejection",
    },
    {
        "source_id": "456_variation_contract",
        "path": OUT / "P8_PiM_projector_variation_stress_CONTRACT.csv",
        "needle": "PV1_topological_absolute_charge_route",
        "role": "topological PiM/no-Hodge stress contract",
    },
    {
        "source_id": "660_commutator_audit",
        "path": OUT / "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
        "needle": "CZ660_6_Hilbert_topological_equality",
        "role": "commutator and Hilbert/topological equality blocker",
    },
    {
        "source_id": "908_retained_ppn_vector",
        "path": OUT / "P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv",
        "needle": "RPV908_0_metric_projector_stress",
        "role": "retained local PPN/source vector",
    },
    {
        "source_id": "912_delta_symp",
        "path": OUT / "P8_Y5_R10_912_DELTA_SYMP_EXTRA_ROWS.csv",
        "needle": "DSE912_0_projector",
        "role": "Delta_symp_projector extra-sector row",
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
            "what_changed": "converted the 913 topological absolute PiM route into an explicit future parent-action contract and kept the projector source-bound pack active",
            "best_partial_result": "a zero-stress projector route is mathematically clean only if Pi_M is a metric-independent absolute cohomology charge map and the observed Hilbert mass current equals the topological mass current on shell",
            "hard_blockers": "fixed S2/domain selection, topological absolute charge map, metric-free action, chain-map/source-current domain, Hilbert/topological equality, boundary no-flux, and measured-GM calibration are not parent-signed",
            "what_is_not_claimed": "topological PiM parent derivation, omega_projector zero, Delta_symp_projector zero, Newtonian source closure, PPN pass, local-GR reduction, or measured-GM calibration",
            "decision": "topological route remains the best low-scrutiny route, but current corpus cannot sign it; retain projector source-bound rows and target the Hilbert/topological equality next",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def topological_parent_clause_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "clause_id": "TPC914_0_fixed_oriented_exterior",
            "parent_action_contract": "the parent branch selects a compact oriented local exterior and S2 homology class before any readout or orbital scoring",
            "mathematical_form": "Sigma_ext ~= S2 x I, [S2] fixed, delta[S2]=0, L_X[S2]=0 on allowed local branch",
            "why_needed": "otherwise ell_M changes with domain/readout and Pi_M becomes a preferred-boundary source",
            "current_status": "not_parent_signed",
            "evidence_anchor": "454:PM0, 456:PV4, 660:CZ660_0, 913:ZP913_0",
        },
        {
            "clause_id": "TPC914_1_absolute_charge_functional",
            "parent_action_contract": "ell_M is an absolute cohomology charge functional on the parent source-current complex, not an orbit-fit or Hodge-selected mask",
            "mathematical_form": "ell_M(J)=integral_[S2] J with delta_g ell_M=0 and ell_M defined before P_read",
            "why_needed": "makes the mass projection metric-independent at the level of the charge",
            "current_status": "conditional_from_prior_contracts_not_parent_signed",
            "evidence_anchor": "454:PM3, 456:PV1, 913:ZP913_1",
        },
        {
            "clause_id": "TPC914_2_topological_generator",
            "parent_action_contract": "the mass generator is a normalized closed topological representative, not a Hodge harmonic representative whose metric variation is silently dropped",
            "mathematical_form": "d omega_M_top=0, integral_[S2] omega_M_top=1, delta_g omega_M_top=0",
            "why_needed": "zeros ell_M(J)d omega_M and avoids delta_g star/Delta/Green stress",
            "current_status": "formal_shape_available_not_parent_owned",
            "evidence_anchor": "454:PM2, 456:PV1/PV2, 913:ZP913_3",
        },
        {
            "clause_id": "TPC914_3_metric_free_topological_action",
            "parent_action_contract": "the PiM/topological source-normalization block uses only wedge, exterior derivative, class pairing, and orientation data in the compact local bulk",
            "mathematical_form": "S_top[Pi_M] contains no sqrt(-g), star_g, Delta_g, G_Delta(g), DeWitt inner product, or least-energy projector",
            "why_needed": "prevents a topological label from reintroducing metric projector stress through the action",
            "current_status": "not_parent_derived",
            "evidence_anchor": "456:topological_name_metric_action, 913:ZP913_2",
        },
        {
            "clause_id": "TPC914_4_chain_map_domain",
            "parent_action_contract": "Pi_M commutes with d on the allowed Hilbert/source-current domain and the domain is stable under the parent Euler/Ward flow",
            "mathematical_form": "[d,Pi_M]J_H=0 for J_H,dJ_H in Dom(Pi_M)",
            "why_needed": "otherwise d(Pi_M J_H) contains a commutator flux that is exactly the retained source row",
            "current_status": "not_parent_derived",
            "evidence_anchor": "455:FC2/FC3, 660:CZ660_3, 913:ZP913_4",
        },
        {
            "clause_id": "TPC914_5_Hilbert_topological_equality",
            "parent_action_contract": "the closed topological mass current is proven equal to the observed Hilbert PiM mass current on shell, up to exact zero-flux terms",
            "mathematical_form": "J_M^top = Pi_M J_H + dB_zero and integral_boundary dB_zero=0",
            "why_needed": "without this, topology may close the wrong current and cannot derive Newtonian source closure",
            "current_status": "not_derived_key_blocker",
            "evidence_anchor": "455:FC5, 660:CZ660_6, 913:ZP913_5",
        },
        {
            "clause_id": "TPC914_6_boundary_domain_no_flux",
            "parent_action_contract": "boundary and domain variations carry no compact mass, shear, vector, clock, radial, time, range, or source-normalization hair",
            "mathematical_form": "integral_boundary Pi_M K_owner=0 or constant_global with partial_t,partial_r,partial_A,partial_lambda all zero",
            "why_needed": "boundary-only projector stress is still observable unless it is class-only and derivative-silent",
            "current_status": "fail_open",
            "evidence_anchor": "455:FC4, 456:PV3, 913:ZP913_6",
        },
        {
            "clause_id": "TPC914_7_measured_GM_calibration_after_closure",
            "parent_action_contract": "after closure, the conserved topological/Hilbert mass charge calibrates to the measured Newtonian monopole with constant universal G_eff",
            "mathematical_form": "mu_obs=G_eff M_eff, M_eff proportional to ell_M(J_H), partial_t/r/lambda(G_eff M_eff)=0 in local exterior",
            "why_needed": "a closed cohomology charge is not automatically the measured orbital GM",
            "current_status": "not_parent_derived",
            "evidence_anchor": "454:V5, 455:FC7, 913 local-GR gate",
        },
        {
            "clause_id": "TPC914_8_no_readout_mask_in_parent_variation",
            "parent_action_contract": "P_read, fitted masks, and posterior scoring operators stay outside delta S_parent",
            "mathematical_form": "delta S_parent contains no P_read and no fitted Pi_M; readout acts only after the parent equations",
            "why_needed": "blocks an easy but fake projector-zero proof",
            "current_status": "policy_written_not_positive_derivation",
            "evidence_anchor": "456:PV7, 913:ZP913_7",
        },
    ]
    for row in rows:
        row.update(
            {
                "parent_signed": False,
                "zero_route_claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def metric_dependence_rejection_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "route_id": "MDR914_0_Hodge_star_projector",
            "candidate_route": "choose omega_M by Hodge harmonic representative and ignore delta_g star",
            "failure_mode": "delta_g star_g changes the representative and produces projector stress",
            "route_fate": "rejected_as_zero_route_retained_if_used",
            "fallback": "use absolute topological class data or retain c_PiM_g/Delta_symp_projector",
        },
        {
            "route_id": "MDR914_1_Green_Laplacian_projector",
            "candidate_route": "define Pi_M by least-energy, Green operator, or Laplacian inverse",
            "failure_mode": "delta_g Delta_g and delta_g G_Delta create nonlocal metric response",
            "route_fate": "rejected_as_zero_route_retained_if_used",
            "fallback": "retain I_commutator and projector stress bound rows",
        },
        {
            "route_id": "MDR914_2_DeWitt_inner_product_split",
            "candidate_route": "make mass/shear/memory blocks orthogonal with a DeWitt or boundary metric split",
            "failure_mode": "orthogonality itself varies unless the metric block is parent-owned and no-hair",
            "route_fate": "not_zero_safe_without_full_stress_ledger",
            "fallback": "retain c_PiM_g and local PPN residual vector",
        },
        {
            "route_id": "MDR914_3_boundary_only_without_nohair",
            "candidate_route": "push all projector stress to a compact boundary and call the exterior vacuum",
            "failure_mode": "boundary monopole, shear, vector, radial, clock, range, or source hair still changes observables",
            "route_fate": "conditional_only_fail_open",
            "fallback": "retain B_P_flux and tau_R10/PPN/clock/orbital source inputs",
        },
        {
            "route_id": "MDR914_4_lambdaM_magic_wand",
            "candidate_route": "append lambda_M d(Pi_M J_H)=0 after seeing the source closure gap",
            "failure_mode": "mathematically sufficient but explanatory only if lambda_M has independent gauge/topological/Ward origin",
            "route_fate": "closure_only_unless_parent_owned",
            "fallback": "target Hilbert/topological equality or keep closure explicit",
        },
        {
            "route_id": "MDR914_5_readout_mask_in_action",
            "candidate_route": "place the fitted/scored Pi_M mask inside S_parent",
            "failure_mode": "post-fit readout becomes a hidden external source and violates variation order",
            "route_fate": "forbidden",
            "fallback": "readout only after parent equations",
        },
    ]
    for row in rows:
        row.update(
            {
                "accepted_zero_route": False,
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def projector_source_bound_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "source_id": "PSB914_0_Delta_symp_projector",
            "symbol": "Delta_symp_projector",
            "definition": "mass-normalized projector/PiM symplectic obstruction |integral_S i_tau omega_projector|",
            "arena": "R10, PPN, clocks, orbital, local-GR source closure",
            "units": "dimensionless_or_model_normalized_to_GM_source",
            "needed_inputs": "parent theta/omega_projector, tau/source normalization, local bound map, coefficient profile",
            "source_paths": "P8_Y5_R10_912_DELTA_SYMP_EXTRA_ROWS.csv; P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv",
            "current_status": "MISSING_PARENT_TOPOLOGICAL_ZERO_OR_BOUND_COEFFICIENT",
        },
        {
            "source_id": "PSB914_1_c_PiM_g",
            "symbol": "c_PiM_g",
            "definition": "coefficient mapping delta_g Pi_M/projector stress into weak-field metric/source observables",
            "arena": "PPN, local-GR, orbital residuals",
            "units": "model_coefficient",
            "needed_inputs": "weak-field operator basis, normalization, local metric response, source path",
            "source_paths": "P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv; P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv",
            "current_status": "MISSING_WEAK_FIELD_COEFFICIENT_MAP",
        },
        {
            "source_id": "PSB914_2_q_P",
            "symbol": "q_P^nu",
            "definition": "Bianchi-visible divergence/source residual of retained projector stress",
            "arena": "conservation, PPN, clocks, orbital systems",
            "units": "force_density_or_normalized_source_divergence",
            "needed_inputs": "nabla_mu T_projector^{mu nu}, projection operator, local exterior background, residual vector map",
            "source_paths": "P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv; P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv",
            "current_status": "MISSING_PROJECTOR_STRESS_DIVERGENCE",
        },
        {
            "source_id": "PSB914_3_B_P_flux",
            "symbol": "B_P_flux",
            "definition": "compact boundary/corner mass flux from PiM/projector/domain variation",
            "arena": "R10, source-normalization, orbital GM drift, clock/local boundary tests",
            "units": "mass_flux_or_dimensionless_fractional_GM_shift",
            "needed_inputs": "boundary current K_owner, Pi_M projection, no-hair/fixed-domain proof or bound coefficients",
            "source_paths": "P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv; P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
            "current_status": "MISSING_BOUNDARY_NO_FLUX_PROOF_OR_BOUND_INPUT",
        },
        {
            "source_id": "PSB914_4_I_commutator",
            "symbol": "I_commutator",
            "definition": "source-current/domain commutator contribution [d,Pi_M]J_H integrated through the compact exterior",
            "arena": "R10, PPN, local source closure",
            "units": "normalized_flux_or_dimensionless_integral",
            "needed_inputs": "allowed source-current domain, chain-map proof, Hilbert current regularity, exterior integration measure",
            "source_paths": "P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv; P8_Y5_R10_913_RETAINED_PROJECTOR_SOURCE_ROWS.csv",
            "current_status": "MISSING_CHAIN_MAP_DOMAIN_PROOF",
        },
        {
            "source_id": "PSB914_5_Delta_HT_current",
            "symbol": "Delta_HT_current",
            "definition": "mismatch between closed topological mass current and observed Hilbert PiM mass current",
            "arena": "Newtonian source closure, measured GM calibration, PPN/local-GR gate",
            "units": "current_mismatch_or_normalized_mass_flux",
            "needed_inputs": "J_M^top, Pi_M J_H, exact improvement B_zero, boundary zero-flux proof",
            "source_paths": "P8_PiM_flux_closure_Ward_topological_CONTRACT.csv; P8_Y5_R10_913_PROJECTOR_ZERO_ROUTE_CLAUSES.csv",
            "current_status": "MISSING_HILBERT_TOPOLOGICAL_EQUALITY",
        },
        {
            "source_id": "PSB914_6_c_domain",
            "symbol": "c_domain",
            "definition": "coefficient for preferred-domain/homology variation if fixed S2/domain theorem fails",
            "arena": "preferred-frame, orbital, PPN, range/local tests",
            "units": "model_coefficient",
            "needed_inputs": "domain selector variation, normal/vector response, bound arena projection, source path",
            "source_paths": "P8_PiM_projector_variation_stress_CONTRACT.csv; P8_Y5_R10_660_COMMUTATOR_ZERO_AUDIT.csv",
            "current_status": "MISSING_FIXED_DOMAIN_OR_DOMAIN_BOUND_COEFFICIENT",
        },
    ]
    for row in rows:
        row.update(
            {
                "score_ready": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def branch_decision_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "branch_id": "BD914_0_topological_zero_attempt",
            "input_from_913": "try to parent-sign topological absolute PiM",
            "verdict": "attempted_not_parent_signed",
            "reason": "the corpus has conditional topology/projector templates but not the parent equality J_M^top = Pi_M J_H, not fixed-domain/no-flux, and not measured-GM calibration",
            "action": "do not claim omega_projector zero or local-GR",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD914_1_fallback_bound_pack",
            "input_from_913": "retain Delta_symp_projector, q_P^nu, c_PiM_g, B_P_flux, and I_commutator",
            "verdict": "retained_nonclaim_pack_extended",
            "reason": "without parent zero, these are the honest local/source observables that must be bounded or derived away",
            "action": "keep source rows score_ready=false until coefficients, units, profiles, and arena projections are sourced",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "branch_id": "BD914_2_next_derivation_target",
            "input_from_913": "topological route is best low-scrutiny path",
            "verdict": "select_915_Hilbert_topological_equality",
            "reason": "fixed-domain and metric-independence matter, but the decisive blocker is proving the closed topological current is the observed Hilbert mass current rather than a parallel silent label",
            "action": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "CGATE914_0_topological_PiM_parent_signed",
            "claim": "Pi_M is parent-derived as absolute topological charge data",
            "blocker": "fixed-domain, charge map, topological action, chain-map, equality, no-flux, and calibration clauses unsigned",
        },
        {
            "gate_id": "CGATE914_1_projector_omega_zero",
            "claim": "omega_projector and Delta_symp_projector are theorem-zero",
            "blocker": "topological parent route not signed and Hodge route rejected as zero-safe",
        },
        {
            "gate_id": "CGATE914_2_Hodge_projector_zero_safe",
            "claim": "Hodge/DeWitt/Green projector can be used without stress",
            "blocker": "metric dependence generically creates retained projector stress",
        },
        {
            "gate_id": "CGATE914_3_bound_pack_scored",
            "claim": "projector source-bound pack is executable against R10/PPN/clocks/orbital data",
            "blocker": "coefficients, profiles, units, and arena projections are missing",
        },
        {
            "gate_id": "CGATE914_4_Newton_measured_GM",
            "claim": "closed PiM current gives measured Newtonian GM",
            "blocker": "Hilbert/topological equality and measured-GM calibration are not derived",
        },
        {
            "gate_id": "CGATE914_5_local_GR",
            "claim": "local exterior reduces to GR/PPN-safe metric branch",
            "blocker": "projector/source residuals remain retained and unbounded",
        },
    ]
    for row in rows:
        row.update(
            {
                "claim_allowed": False,
                "valid_for_claim": False,
                "generated_utc": generated_utc,
            }
        )
    return rows


def next_target_rows(generated_utc: str) -> list[dict[str, object]]:
    return [
        {
            "next_target": NEXT_TARGET,
            "objective": "try to derive J_M^top = Pi_M J_H + dB_zero from a parent topological/current sector; if not, convert Delta_HT_current into the source-bound pack",
            "include": "topological mass current, Hilbert current, exact improvement B_zero, zero boundary flux, chain-map/source-domain clauses, calibration impact",
            "exclude": "claiming topological closure by naming, using Hodge/DeWitt stress-free, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime)
            if modified > CUTOFF:
                count += 1
    return count


def all_nonclaim(tables: list[list[dict[str, object]]]) -> bool:
    guarded_fields = ("valid_for_claim", "claim_allowed", "score_ready", "zero_route_claim_allowed", "accepted_zero_route")
    for rows in tables:
        for row in rows:
            for field in guarded_fields:
                if field in row and stringify(row[field]).lower() != "false":
                    return False
    return True


def validation_rows(
    generated_utc: str,
    sources: list[dict[str, object]],
    topo: list[dict[str, object]],
    metric: list[dict[str, object]],
    pack: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    generated_tables: list[list[dict[str, object]]],
) -> list[dict[str, object]]:
    prior_rows = read_csv(OUT / "P8_Y5_BRR545_913_VALIDATION.csv")
    formalization_count = formalization_changed_after_cutoff()
    checks = [
        {
            "check_id": "V914_0_sources_exist_and_needles",
            "result": "pass" if all(row["exists"] and row["needle_check"] == "pass" for row in sources) else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V914_1_prior_913_clean",
            "result": "pass" if prior_rows and all(row.get("result") == "pass" for row in prior_rows) else "fail",
            "detail": "P8_Y5_BRR545_913_VALIDATION.csv clean",
        },
        {
            "check_id": "V914_2_topological_clause_not_parent_signed",
            "result": "pass" if topo and all(not row["parent_signed"] for row in topo) else "fail",
            "detail": "all topological absolute PiM clauses remain unsigned",
        },
        {
            "check_id": "V914_3_key_blocker_recorded",
            "result": "pass" if any(row["clause_id"] == "TPC914_5_Hilbert_topological_equality" and row["current_status"] == "not_derived_key_blocker" for row in topo) else "fail",
            "detail": "Hilbert/topological equality is recorded as the decisive blocker",
        },
        {
            "check_id": "V914_4_metric_dependent_routes_not_zero_safe",
            "result": "pass" if metric and all(not row["accepted_zero_route"] for row in metric) else "fail",
            "detail": "Hodge/Green/DeWitt/readout routes are not accepted as stress-free",
        },
        {
            "check_id": "V914_5_projector_source_bound_pack_nonclaim",
            "result": "pass" if pack and all(not row["score_ready"] and not row["valid_for_claim"] and str(row["current_status"]).startswith("MISSING_") for row in pack) else "fail",
            "detail": "all projector source-bound rows remain missing-input and invalid for claim",
        },
        {
            "check_id": "V914_6_claim_gates_false",
            "result": "pass" if gates and all(not row["claim_allowed"] for row in gates) else "fail",
            "detail": "all topological/projector/Newton/local-GR claim gates remain false",
        },
        {
            "check_id": "V914_7_all_generated_rows_nonclaim",
            "result": "pass" if all_nonclaim(generated_tables) else "fail",
            "detail": "all generated rows keep guarded claim fields false",
        },
        {
            "check_id": "V914_8_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V914_9_next_target_selected",
            "result": "pass" if next_rows and next_rows[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V914_10_validation_rows_ready",
            "result": "pass",
            "detail": "validation table constructed",
        },
    ]
    for row in checks:
        row["generated_utc"] = generated_utc
    return checks


def write_doc(
    generated_utc: str,
    sources: list[dict[str, object]],
    summary: list[dict[str, object]],
    topo: list[dict[str, object]],
    metric: list[dict[str, object]],
    pack: list[dict[str, object]],
    decisions: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_rows: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    path = ROOT / DOC_NAME
    content = f"""# 914 - Y5/R10 Topological Absolute PiM Parent Clause Or Projector Source-Bound Pack

Private post-checkpoint-work note. This is not a public Newtonian, PPN, WEP, fifth-force, local-GR, measured-GM, or unified-field claim.

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the topological absolute `Pi_M` route remains the cleanest local-GR-facing route, but it is not parent-signed.** It would be a real derivation only if the parent theory supplies a fixed exterior `S2` class, a metric-independent charge map, a metric-free topological action, a chain-map/source domain, the equality `J_M^top = Pi_M J_H + dB_zero`, zero boundary flux, and measured-GM calibration. Current corpus does not sign that chain, so the projector source-bound pack remains live and non-claim.

## Exact 914 Finding

The clean theorem would be:

```text
Pi_M J_H = ell_M(J_H) omega_M_top,
delta_g Pi_M = 0,
d omega_M_top = 0,
[d,Pi_M]J_H = 0,
J_M^top = Pi_M J_H + dB_zero,
integral_boundary dB_zero = 0.
```

If all clauses were parent-derived, the projector contribution could be topological/absolute rather than a local metric stress. But the current evidence stops one step short: it has templates and conditional routes, not the parent action that proves the Hilbert current and topological current are the same physical mass current.

Practical read: this is a good narrowing, not a failure. The Hodge/DeWitt route is pretty but noisy; the absolute topological route is quiet but needs a real parent equality theorem. No free lunch, chume — but at least the lunch menu is now readable.

## Non-Claim Summary
{md_table(summary)}

## Source Register
{md_table(sources)}

## Topological Parent Clause Audit
{md_table(topo)}

## Metric-Dependence Rejection Audit
{md_table(metric)}

## Projector Source-Bound Pack
{md_table(pack)}

## Branch Decision
{md_table(decisions)}

## Claim Gate
{md_table(gates)}

## Next Target
{md_table(next_rows)}

## Validation
{md_table(validation)}
"""
    path.write_text(content, encoding="utf-8")


def main() -> None:
    generated_utc = now_utc()
    sources = source_register_rows(generated_utc)
    summary = nonclaim_summary_rows(generated_utc)
    topo = topological_parent_clause_rows(generated_utc)
    metric = metric_dependence_rejection_rows(generated_utc)
    pack = projector_source_bound_pack_rows(generated_utc)
    decisions = branch_decision_rows(generated_utc)
    gates = claim_gate_rows(generated_utc)
    next_rows = next_target_rows(generated_utc)

    generated_tables = [sources, summary, topo, metric, pack, decisions, gates, next_rows]
    validation = validation_rows(generated_utc, sources, topo, metric, pack, gates, next_rows, generated_tables)
    generated_tables.append(validation)

    write_csv(OUT / "P8_Y5_R10_914_SOURCE_REGISTER.csv", sources)
    write_csv(OUT / "P8_Y5_R10_914_NONCLAIM_SUMMARY.csv", summary)
    write_csv(OUT / "P8_Y5_R10_914_TOPOLOGICAL_PARENT_CLAUSE_AUDIT.csv", topo)
    write_csv(OUT / "P8_Y5_R10_914_METRIC_DEPENDENCE_REJECTION_AUDIT.csv", metric)
    write_csv(OUT / "P8_Y5_R10_914_PROJECTOR_SOURCE_BOUND_PACK.csv", pack)
    write_csv(OUT / "P8_Y5_R10_914_BRANCH_DECISION.csv", decisions)
    write_csv(OUT / "P8_Y5_R10_914_CLAIM_GATE.csv", gates)
    write_csv(OUT / "P8_Y5_R10_914_NEXT_TARGET.csv", next_rows)
    write_csv(OUT / "P8_Y5_BRR545_914_VALIDATION.csv", validation)
    write_doc(generated_utc, sources, summary, topo, metric, pack, decisions, gates, next_rows, validation)

    failed = [row for row in validation if row["result"] != "pass"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)

    print(STATUS)
    print(f"wrote {ROOT / DOC_NAME}")
    print(f"next target: {NEXT_TARGET}")


if __name__ == "__main__":
    main()
