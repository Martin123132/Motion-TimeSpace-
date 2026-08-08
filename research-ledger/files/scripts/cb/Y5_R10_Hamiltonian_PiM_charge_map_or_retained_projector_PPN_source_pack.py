from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

STATUS = "Y5_R10_909_Hamiltonian_PiM_charge_map_candidate_built_integrability_unsigned_retained_source_pack_staged_nonclaim"
CLAIM_CEILING = "Hamiltonian_PiM_candidate_and_retained_projector_source_pack_only_no_measured_GM_no_Newton_no_PPN_no_local_GR_claim"
NEXT_TARGET = "910-Y5-R10-Hamiltonian-PiM-integrability-reference-subgate-or-retained-source-pack-fill.md"

SOURCE_SPECS = [
    {
        "source_id": "908_doc",
        "path": ROOT / "908-Y5-R10-projector-stress-Bianchi-fate-or-retained-PPN-vector.md",
        "needle": "the projector/N5 stress is not theorem-zeroed",
        "role": "handoff retaining q_P/T_projector as a nonclaim residual",
    },
    {
        "source_id": "908_validation",
        "path": OUT / "P8_Y5_BRR545_908_VALIDATION.csv",
        "needle": "V908_11_validation_rows_ready",
        "role": "prior checkpoint validation",
    },
    {
        "source_id": "663_pim_repair",
        "path": OUT / "P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv",
        "needle": "PR663_0_define_PiM_H",
        "role": "best next derivation target: Hamiltonian/covariant phase space Pi_M",
    },
    {
        "source_id": "457_hamiltonian_charge_doc",
        "path": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "needle": "conditional_Hamiltonian_boundary_charge_theorem",
        "role": "Hamiltonian boundary charge route and no-overclaim policy",
    },
    {
        "source_id": "457_hamiltonian_contract",
        "path": OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needle": "HC2_differentiable_integrable_Hxi",
        "role": "machine contract for Hamiltonian integrability and charge-to-source debt",
    },
    {
        "source_id": "458_pg_gate_doc",
        "path": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "needle": "conditional_Poisson_Gauss_calibration_theorem",
        "role": "measured-GM bridge conditions from Hamiltonian charge to Poisson/Gauss/orbit",
    },
    {
        "source_id": "458_pg_contract",
        "path": OUT / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "needle": "PG1_charge_equals_projected_Hilbert_source",
        "role": "machine PG contract mapping charge/current equality and calibration gaps",
    },
    {
        "source_id": "459_pg_residual_map",
        "path": OUT / "P8_PG_calibration_residual_MAP.csv",
        "needle": "PG1_charge_equals_projected_Hilbert_source",
        "role": "fallback residual mapping if Hamiltonian PiM proof does not close",
    },
    {
        "source_id": "523_gauss_orbital_doc",
        "path": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
        "needle": "GO523_0_observed_orbital_monopole",
        "role": "orbital GM scorecard showing calibration remains unfilled",
    },
    {
        "source_id": "660_projector_stress",
        "path": OUT / "P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv",
        "needle": "TPS660_1_metric_projector_stress",
        "role": "retained projector stress source pack inputs",
    },
    {
        "source_id": "661_equality_attempt",
        "path": OUT / "P8_Y5_R10_661_EQUALITY_ATTEMPT.csv",
        "needle": "EQ661_2_worldtube_charge_route",
        "role": "worldtube/Hilbert/topological charge equality route and blockers",
    },
    {
        "source_id": "789_ward_identity",
        "path": OUT / "P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv",
        "needle": "VWI789_3_Bianchi",
        "role": "Bianchi/Ward safety for retained projector stress",
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
            "what_changed": "constructed the exact Hamiltonian Pi_M candidate map and audited the clauses needed to make it a parent-owned source charge",
            "best_partial_result": "Pi_M^H can be written as a clean conditional covariant-phase-space charge map; it would replace the old topological Pi_M only if integrability, fixed reference, same source frame, no extra charge, and Poisson/Gauss calibration close",
            "hard_blockers": "parent action symplectic current, charge integrability, observed-time generator normalization, fixed reference, source-frame equality, projector variation silence, no extra charge, and measured-GM calibration",
            "what_is_not_claimed": "Hamiltonian charge parent derivation, Pi_M/Hilbert source equality, measured GM, source-normalized Newton, PPN pass, R10 pass, or local GR",
            "decision": "treat Pi_M^H as the derivation candidate, but keep the projector/source pack retained and invalid for claim until parent clauses or numeric bounds exist",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def hamiltonian_candidate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "candidate_id": "HPC909_0_parent_fields",
            "clause": "parent covariant phase space",
            "mathematical_form": "Phi=(g,e,omega,psi_matter,X_MTS,projector/domain/boundary data); L_parent[Phi] diffeomorphism covariant",
            "meaning": "the charge map must be born from the parent action rather than from a late readout projector",
            "current_status": "MISSING_EXPLICIT_PARENT_SYMPLECTIC_CURRENT",
            "closes": "prevents Pi_M^H from being a dressed closure symbol",
        },
        {
            "candidate_id": "HPC909_1_charge_variation",
            "clause": "Iyer-Wald/Hamiltonian variation",
            "mathematical_form": "delta H_tau = integral_S(delta Q_tau - i_tau Theta) with tau the observed local time generator",
            "meaning": "this is the formal route for defining a mass charge from the parent action",
            "current_status": "FORMAL_CANDIDATE_WRITTEN_NOT_PARENT_EVALUATED",
            "closes": "Hamiltonian boundary charge existence if integrable",
        },
        {
            "candidate_id": "HPC909_2_integrated_charge",
            "clause": "integrated reference-fixed mass charge",
            "mathematical_form": "M_H[S,tau] := (H_tau[S]-H_ref)/(G_eff_ref) or equivalent route-normalized boundary mass",
            "meaning": "defines a candidate source mass only after reference and normalization are fixed once",
            "current_status": "MISSING_FIXED_REFERENCE_AND_NORMALIZATION",
            "closes": "charge normalization/reference ambiguity",
        },
        {
            "candidate_id": "HPC909_3_PiM_H_definition",
            "clause": "Hamiltonian Pi_M map",
            "mathematical_form": "Pi_M^H J_H := M_H[S,tau] omega_M^H, with integral_S omega_M^H=1 and d omega_M^H=0 on the allowed exterior complex",
            "meaning": "turns Pi_M from an independent topological projector into the parent charge-map representative",
            "current_status": "CANDIDATE_DEFINITION_ONLY",
            "closes": "old Pi_M/topological conserved-wrong-object loophole if equality and flux conditions close",
        },
        {
            "candidate_id": "HPC909_4_old_PiM_dictionary",
            "clause": "old topological Pi_M equivalence",
            "mathematical_form": "Pi_M^top J_H = Pi_M^H J_H + dB_Htop + R_Htop",
            "meaning": "old topological Pi_M earns credit only if residual and boundary flux vanish or are bounded",
            "current_status": "MISSING_R_HTOP_AND_BOUNDARY_ZERO_FLUX",
            "closes": "Hilbert/topological equality debt from 660/661/663",
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def integrability_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "gate_id": "HIG909_0_tau_generator",
            "required_condition": "observed time generator tau is fixed by the same matter/coframe frame used for clocks and orbits",
            "mathematical_test": "tau=partial_t/asymptotic Killing/quasilocal admissible generator with fixed normalization and no frame split",
            "current_evidence": "457 HC1 and 523 CAL523_0 remain conditional/not parent-derived",
            "result": "fail_for_claim",
            "fallback_residual": "delta_frame_source; alpha_clock_redshift; preferred-frame vector",
        },
        {
            "gate_id": "HIG909_1_symplectic_integrability",
            "required_condition": "delta H_tau is finite and path-independent on the local exterior phase space",
            "mathematical_test": "integral_S i_tau omega(delta_1 Phi,delta_2 Phi)=0 or exact on allowed variations; H_ref fixed once",
            "current_evidence": "457 HC2 and 663 PR663_1 mark integrability/reference as not derived",
            "result": "fail_for_claim",
            "fallback_residual": "Delta_symp; boundary_reference_shift",
        },
        {
            "gate_id": "HIG909_2_constraints_on_shell",
            "required_condition": "all bulk/projector/domain/boundary/source variables are varied and constraints vanish or are retained",
            "mathematical_test": "C_tau=0 including E_X,E_P,E_D,E_boundary and source-normalization equations",
            "current_evidence": "457 HC3 and 655 Ward/Euler ownership remain open",
            "result": "fail_for_claim",
            "fallback_residual": "mu_extra_boundary_bulk_domain; c_nonEH_operator_vector; q_P^nu",
        },
        {
            "gate_id": "HIG909_3_no_extra_charge",
            "required_condition": "hidden/projector/boundary/domain/memory/range/coupling sectors carry no unowned mass charge",
            "mathematical_test": "Q_nonEH+Q_PiM+Q_boundary+Q_domain+Q_memory+Q_range+Q_delta_kappa=0 or retained with units",
            "current_evidence": "457 HC5 is fail_open and 908 retains projector stress",
            "result": "fail_for_claim",
            "fallback_residual": "c_PiM_g; c_boundary; alpha(lambda); dln_Geff_dt",
        },
        {
            "gate_id": "HIG909_4_source_measure_equality",
            "required_condition": "Hamiltonian charge equals the same projected Hilbert source used by matter and Poisson",
            "mathematical_test": "B_tau/G_eff = M_eff[Pi_M^H J_H] and delta B_tau = delta integral_S Pi_M^H J_H",
            "current_evidence": "458 PG1, 523 CAL523_1, and 661 equality attempt remain not parent-derived",
            "result": "fail_for_claim",
            "fallback_residual": "epsilon_charge; dln_Meff_dt; mu_extra_boundary_bulk_domain",
        },
        {
            "gate_id": "HIG909_5_Poisson_Gauss_orbital_calibration",
            "required_condition": "source charge calibrates to the observed inverse-square orbital GM with no residual source terms",
            "mathematical_test": "surface_int grad Phi dot dS = 4 pi G_eff M_H and a_r=-G_eff M_H/r^2 in observed frame",
            "current_evidence": "458 PG4-PG8 and 523 scorecard are unfilled/not parent-derived",
            "result": "fail_for_claim",
            "fallback_residual": "epsilon_Gauss; epsilon_orbit; partial_r_ln_mu_obs; eta_source_AB",
        },
    ]
    for row in rows:
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def source_equality_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "equality_id": "SEQ909_0_best_possible_theorem",
            "statement": "If the parent action supplies integrable H_tau, fixed H_ref, same observed source frame, no extra charge, and Poisson/Gauss calibration, then Pi_M^H can replace the old Pi_M as the mass-channel owner.",
            "mathematical_form": "Pi_M^H J_H := ((H_tau-H_ref)/G_eff_ref) omega_M^H; Pi_M^top J_H = Pi_M^H J_H + dB_Htop + R_Htop; require R_Htop=0 and integral_boundary dB_Htop=0",
            "status": "valid_conditional_theorem_not_satisfied",
            "claim_credit": "none_until_clauses_close",
        },
        {
            "equality_id": "SEQ909_1_why_not_enough",
            "statement": "A conserved Hamiltonian charge alone is not measured source mass; it can include hidden boundary/projector/non-EH/domain/coupling charge.",
            "mathematical_form": "H_tau = G_eff M_H + Q_projector + Q_boundary + Q_nonEH + Q_domain + Q_delta_kappa",
            "status": "overclaim_blocker_active",
            "claim_credit": "none",
        },
        {
            "equality_id": "SEQ909_2_worldtube_route",
            "statement": "The cleanest equality route is to make the source worldtube, Hilbert current, and Hamiltonian charge one parent object before readout.",
            "mathematical_form": "W_source=supp(J_H[e_obs]); M_source[W]=H_tau[S]-H_ref; J_M^H=PD(W_source) with zero exchange/boundary tail",
            "status": "best_route_but_missing_worldtube_selector_and_source_measure",
            "claim_credit": "none",
        },
        {
            "equality_id": "SEQ909_3_retained_fallback",
            "statement": "If any equality clause remains unsigned, the mismatch is a measurable source-normalization/projector residual rather than a closure axiom.",
            "mathematical_form": "epsilon_HPiM = |Delta_symp|+|B_zero_flux|+|R_Htop|+|I_commutator|+|Delta_extra| normalized by M_ref",
            "status": "fallback_staged_unfilled",
            "claim_credit": "none",
        },
    ]
    for row in rows:
        row["valid_for_claim"] = False
        row["generated_utc"] = generated_utc
    return rows


def retained_source_pack_rows(generated_utc: str) -> list[dict[str, object]]:
    rows = [
        {
            "pack_id": "RSP909_0_symplectic_integrability_residual",
            "symbol": "Delta_symp",
            "definition": "failure of delta H_tau to be integrable/path-independent on the allowed local exterior phase space",
            "units": "mass_charge_or_dimensionless_after_M_ref",
            "observable_link": "measured GM calibration; beta; Gdot; boundary reference drift",
            "required_input": "parent symplectic current and integrability proof, or numeric/reference residual",
            "source_paths": f"{OUT / 'P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv'};{OUT / 'P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv'}",
            "current_status": "MISSING_PARENT_SYMPLECTIC_INTEGRABILITY",
        },
        {
            "pack_id": "RSP909_1_Htop_residual",
            "symbol": "R_Htop",
            "definition": "residual between old topological Pi_M current and Hamiltonian Pi_M^H current after exact boundary improvement",
            "units": "mass_current_or_dimensionless_after_M_ref",
            "observable_link": "dln_Meff_dt; radial source hair; fifth force; source-normalization beta",
            "required_input": "Pi_M^top/Pi_M^H dictionary with zero-flux improvement, or residual profile",
            "source_paths": f"{OUT / 'P8_Y5_R10_661_EQUALITY_ATTEMPT.csv'};{OUT / 'P8_Y5_R10_663_PIM_REPAIR_OR_DEMOTION.csv'}",
            "current_status": "MISSING_HTOP_ZERO_EQUIVALENCE",
        },
        {
            "pack_id": "RSP909_2_projector_metric_stress",
            "symbol": "c_PiM_g",
            "definition": "metric variation of Pi_M/Pi_M^H or retained T_projector contribution to the local metric equation",
            "units": "dimensionless_after_EH_normalization_or_stress_energy_units",
            "observable_link": "gamma; beta; alpha3; xi; local light/time/orbital residuals",
            "required_input": "delta_g Pi_M theorem-zero, Hamiltonian charge metric variation, or sourced stress coefficient",
            "source_paths": f"{OUT / 'P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv'};{OUT / 'P8_Y5_R10_660_PROJECTOR_STRESS_VECTOR.csv'}",
            "current_status": "MISSING_PROJECTOR_STRESS_MAP",
        },
        {
            "pack_id": "RSP909_3_projector_divergence_force",
            "symbol": "q_P^nu",
            "definition": "P_loc nabla_mu T_projector^{mu nu}, the Bianchi-visible residual if projector stress is not zero/conserved",
            "units": "force_density_or_divergence_of_stress_units",
            "observable_link": "matter nonconservation; anomalous acceleration; preferred-frame/location PPN rows",
            "required_input": "exchange carrier T_Q, q_P zero theorem, or response coefficient map",
            "source_paths": f"{OUT / 'P8_Y5_R10_908_RETAINED_PPN_SOURCE_VECTOR.csv'};{OUT / 'P8_Y5_R10_789_VARIATION_WARD_IDENTITY_GATE.csv'}",
            "current_status": "MISSING_EXCHANGE_CURRENT_AND_RESPONSE_MAP",
        },
        {
            "pack_id": "RSP909_4_charge_current_mismatch",
            "symbol": "epsilon_charge",
            "definition": "(B_tau/G_eff - M_H[Pi_M^H J_H])/M_H, the Hamiltonian-to-Hilbert source mismatch",
            "units": "dimensionless",
            "observable_link": "measured GM; source normalization; dln_Meff_dt; mu_extra",
            "required_input": "charge-current equality proof or numeric mismatch with units/source",
            "source_paths": f"{OUT / 'P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv'};{OUT / 'P8_PG_calibration_residual_MAP.csv'}",
            "current_status": "MISSING_CHARGE_CURRENT_EQUALITY_PROOF_OR_VALUE",
        },
        {
            "pack_id": "RSP909_5_orbital_calibration_mismatch",
            "symbol": "epsilon_orbit",
            "definition": "(r^2 |a_r|-G_eff M_H)/(G_eff M_H) after same-frame Hamiltonian/Gauss calibration",
            "units": "dimensionless",
            "observable_link": "Newtonian orbital GM; radial source hair; R10 range dependence; PPN source stability",
            "required_input": "slow-particle same-frame readout proof or orbital residual profile",
            "source_paths": f"{ROOT / '523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md'};{OUT / 'P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv'}",
            "current_status": "MISSING_ORBITAL_GM_CALIBRATION_PROOF_OR_VALUE",
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
            "decision_id": "BD909_0_derivation_attempt",
            "branch": "Hamiltonian_PiM_candidate",
            "verdict": "candidate_constructed_not_parent_signed",
            "reason": "the map can be written cleanly, but the needed symplectic integrability, fixed reference, same source frame, no-extra-charge, and Poisson/Gauss clauses are all unsigned",
            "policy": "use Pi_M^H as the next derivation skeleton, not as a claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "BD909_1_fallback",
            "branch": "retained_projector_source_pack",
            "verdict": "source_pack_staged_unfilled",
            "reason": "if any Hamiltonian clause stays open, the residuals must be scoreable rows: Delta_symp, R_Htop, c_PiM_g, q_P^nu, epsilon_charge, epsilon_orbit",
            "policy": "do not promote Newton/local GR until rows are theorem-zero or bounded with real units/sources",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        },
    ]


def claim_gate_rows(generated_utc: str) -> list[dict[str, object]]:
    gates = [
        ("CGATE909_0_PiM_H_defined", "Pi_M^H parent charge-map claim", "blocked: candidate definition lacks parent symplectic current and integrability proof"),
        ("CGATE909_1_integrability", "integrable Hamiltonian mass charge", "blocked: delta H_tau path independence and fixed reference not derived"),
        ("CGATE909_2_source_equality", "Hamiltonian charge equals Hilbert/PiM source", "blocked: source-frame/worldtube equality and old PiM dictionary not signed"),
        ("CGATE909_3_projector_stress_zero", "projector stress zero/conserved", "blocked: c_PiM_g and q_P^nu remain missing source coefficients"),
        ("CGATE909_4_measured_GM", "measured orbital GM derived", "blocked: Poisson/Gauss/orbital calibration and zero residual scorecard unfilled"),
        ("CGATE909_5_Newton_PPN_local_GR", "source-normalized Newton/PPN/local GR", "blocked: first-order measured GM and second-order source stability are not proven"),
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
            "objective": "attack the narrow Hamiltonian integrability/reference clause first; if it cannot close, begin filling the retained source pack with theorem-zero or numeric bounded rows",
            "include": "parent symplectic current, delta H_tau integrability, H_ref/reference rule, tau normalization, Delta_symp row, boundary zero-flux, retained pack fallback",
            "exclude": "claiming Pi_M^H by definition, assuming measured GM, hiding projector stress, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
            "generated_utc": generated_utc,
        }
    ]


def prior_908_clean() -> bool:
    rows = read_csv(OUT / "P8_Y5_BRR545_908_VALIDATION.csv")
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
    candidate_rows_: list[dict[str, object]],
    integrability_rows_: list[dict[str, object]],
    equality_rows_: list[dict[str, object]],
    retained_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
) -> list[dict[str, object]]:
    formalization_count = formalization_changed_count()
    row_groups = [
        summary_rows_,
        candidate_rows_,
        integrability_rows_,
        equality_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    ]
    checks = [
        {
            "check_id": "V909_0_sources_exist_and_needles",
            "result": "pass"
            if all(row["exists"] is True and row["needle_check"] == "pass" for row in source_rows_)
            else "fail",
            "detail": "all source paths exist and needles are present",
        },
        {
            "check_id": "V909_1_prior_908_clean",
            "result": "pass" if prior_908_clean() else "fail",
            "detail": "P8_Y5_BRR545_908_VALIDATION.csv clean",
        },
        {
            "check_id": "V909_2_candidate_written_not_promoted",
            "result": "pass"
            if any(row["candidate_id"] == "HPC909_3_PiM_H_definition" and row["current_status"] == "CANDIDATE_DEFINITION_ONLY" for row in candidate_rows_)
            else "fail",
            "detail": "Pi_M^H candidate definition exists but grants no claim credit",
        },
        {
            "check_id": "V909_3_integrability_fails_for_claim",
            "result": "pass" if integrability_rows_ and all(row["result"] == "fail_for_claim" for row in integrability_rows_) else "fail",
            "detail": "all Hamiltonian integrability/source clauses remain unsigned",
        },
        {
            "check_id": "V909_4_conditional_theorem_status",
            "result": "pass"
            if any(row["equality_id"] == "SEQ909_0_best_possible_theorem" and row["status"] == "valid_conditional_theorem_not_satisfied" for row in equality_rows_)
            else "fail",
            "detail": "conditional Hamiltonian PiM theorem stated without promotion",
        },
        {
            "check_id": "V909_5_retained_source_pack_nonclaim_missing_inputs",
            "result": "pass"
            if retained_rows_
            and all(row["valid_for_claim"] is False and row["score_ready"] is False and "MISSING_" in stringify(row["current_status"]) for row in retained_rows_)
            else "fail",
            "detail": "retained pack rows remain missing-input/source-needed and invalid for claim",
        },
        {
            "check_id": "V909_6_retained_source_paths_exist",
            "result": "pass" if source_paths_exist(retained_rows_) else "fail",
            "detail": "every retained source-pack path exists",
        },
        {
            "check_id": "V909_7_claim_gates_false",
            "result": "pass" if all(row["claim_allowed"] is False for row in claim_rows_) else "fail",
            "detail": "all PiM/measured-GM/Newton/PPN/local-GR claim gates remain false",
        },
        {
            "check_id": "V909_8_all_generated_rows_nonclaim",
            "result": "pass" if all_generated_rows_nonclaim(row_groups) else "fail",
            "detail": "all generated rows keep valid_for_claim/claim_allowed/score_ready false where present",
        },
        {
            "check_id": "V909_9_formalization_workbench_untouched",
            "result": "pass" if formalization_count == 0 else "fail",
            "detail": f"formalization_changed_after_cutoff={formalization_count}",
        },
        {
            "check_id": "V909_10_next_target_selected",
            "result": "pass" if next_rows_ and next_rows_[0]["next_target"] == NEXT_TARGET else "fail",
            "detail": NEXT_TARGET,
        },
        {
            "check_id": "V909_11_validation_rows_ready",
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
    candidate_rows_: list[dict[str, object]],
    integrability_rows_: list[dict[str, object]],
    equality_rows_: list[dict[str, object]],
    retained_rows_: list[dict[str, object]],
    decision_rows_: list[dict[str, object]],
    claim_rows_: list[dict[str, object]],
    next_rows_: list[dict[str, object]],
    validation_rows_: list[dict[str, object]],
) -> None:
    content = f"""# 909 - Y5/R10 Hamiltonian PiM Charge Map Or Retained Projector PPN Source Pack

Status: `{STATUS}`
Claim ceiling: `{CLAIM_CEILING}`
Generated UTC: `{generated_utc}`

Current result: **the Hamiltonian `Pi_M^H` route is the best derivation skeleton, but it is not parent-signed yet.** We can write the exact candidate map using covariant-phase-space/Hamiltonian charge logic, but the integrability, fixed-reference, source-frame, no-extra-charge, and Poisson/Gauss/orbital clauses are still unpaid bills. So the map is useful; it is not yet a Newton/local-GR victory lap.

## Exact 909 Finding
The clean conditional route is:

```text
delta H_tau = integral_S(delta Q_tau - i_tau Theta)
M_H[S,tau] = (H_tau[S]-H_ref)/G_eff_ref
Pi_M^H J_H := M_H[S,tau] omega_M^H
```

This would be a serious way to make `Pi_M` parent-owned. But current evidence only supports the conditional skeleton. Until the parent action supplies the symplectic current, integrability, observed-time generator, fixed reference, source equality, projector silence, and measured-GM calibration, `Pi_M^H` stays a derivation target and the projector/source residual pack stays retained.

## Nonclaim Summary
{md_table(summary_rows_)}

## Source Register
{md_table(source_rows_)}

## Hamiltonian PiM Candidate
{md_table(candidate_rows_)}

## Integrability and Calibration Gate
{md_table(integrability_rows_)}

## Source Equality Theorem Attempt
{md_table(equality_rows_)}

## Retained Projector/Source Pack
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
    candidate_rows_ = hamiltonian_candidate_rows(generated_utc)
    integrability_rows_ = integrability_gate_rows(generated_utc)
    equality_rows_ = source_equality_rows(generated_utc)
    retained_rows_ = retained_source_pack_rows(generated_utc)
    decision_rows_ = branch_decision_rows(generated_utc)
    claim_rows_ = claim_gate_rows(generated_utc)
    next_rows_ = next_target_rows(generated_utc)
    validation_rows_ = validation_rows(
        generated_utc,
        source_rows_,
        summary_rows_,
        candidate_rows_,
        integrability_rows_,
        equality_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
    )

    outputs = {
        "P8_Y5_R10_909_SOURCE_REGISTER.csv": source_rows_,
        "P8_Y5_R10_909_NONCLAIM_SUMMARY.csv": summary_rows_,
        "P8_Y5_R10_909_HAMILTONIAN_PIM_CANDIDATE.csv": candidate_rows_,
        "P8_Y5_R10_909_INTEGRABILITY_GATE.csv": integrability_rows_,
        "P8_Y5_R10_909_SOURCE_EQUALITY_ATTEMPT.csv": equality_rows_,
        "P8_Y5_R10_909_RETAINED_PROJECTOR_SOURCE_PACK.csv": retained_rows_,
        "P8_Y5_R10_909_BRANCH_DECISION.csv": decision_rows_,
        "P8_Y5_R10_909_CLAIM_GATE.csv": claim_rows_,
        "P8_Y5_R10_909_NEXT_TARGET.csv": next_rows_,
        "P8_Y5_BRR545_909_VALIDATION.csv": validation_rows_,
    }
    for filename, rows in outputs.items():
        write_csv(OUT / filename, rows)

    doc_path = ROOT / "909-Y5-R10-Hamiltonian-PiM-charge-map-or-retained-projector-PPN-source-pack.md"
    write_markdown(
        doc_path,
        generated_utc,
        summary_rows_,
        source_rows_,
        candidate_rows_,
        integrability_rows_,
        equality_rows_,
        retained_rows_,
        decision_rows_,
        claim_rows_,
        next_rows_,
        validation_rows_,
    )

    failed = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"wrote {doc_path}")
    print(f"wrote {OUT / 'P8_Y5_BRR545_909_VALIDATION.csv'}")
    print(f"status={STATUS}")
    if failed:
        print("failed_validation=" + ",".join(row["check_id"] for row in failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
