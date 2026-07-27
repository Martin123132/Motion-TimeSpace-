from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = MICROSCOPE / "quarantine" / "1714"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md"

SOURCE_FILES = {
    "1713_doc": ROOT / "1713-Y5-R2FR-source-functional-evenness-and-JZ-BZ-coupling-lock-or-profile-acquisition.md",
    "1713_validation": OUT / "P8_Y5_BRR545_1713_VALIDATION.csv",
    "1713_next": OUT / "P8_Y5_PARENT_QLOC_1713_NEXT_TARGET.csv",
    "1713_y5_basis": OUT / "P8_Y5_PARENT_QLOC_1713_Y5_PRIORITY_BASIS_LINK.csv",
    "1713_profile": OUT / "P8_Y5_PARENT_QLOC_1713_PROFILE_ACQUISITION_ROWS.csv",
    "1356_doc": ROOT / "1356-Y5-R10-RAB-worldtube-Hilbert-source-equality-or-R_eq-Icommutator-fill.md",
    "1356_equality": OUT / "P8_Y5_R10_1356_WORLDTUBE_HILBERT_EQUALITY_ATTEMPT.csv",
    "1356_residuals": OUT / "P8_Y5_R10_1356_REQ_ICOMMUTATOR_FILL.csv",
    "1356_guard": OUT / "P8_Y5_R10_1356_NO_CLOSED_WRONG_CHARGE_GUARD.csv",
    "1356_next": OUT / "P8_Y5_R10_1356_NEXT_TARGET.csv",
    "parent_worldtube": OUT / "P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
    "1013_doc": ROOT / "1013-Y5-R10-PiM-JH-flux-closure-or-measured-GM-obstruction-score.md",
    "1013_vector": OUT / "P8_Y5_R10_1013_MEASURED_GM_OBSTRUCTION_VECTOR.csv",
    "1014_doc": ROOT / "1014-Y5-R10-PiM-commutator-projector-variation-zero-or-coefficient-bound.md",
    "1014_commutator": OUT / "P8_Y5_R10_1014_PIM_COMMUTATOR_THEOREM_ATTEMPT.csv",
    "1014_coeffs": OUT / "P8_Y5_R10_1014_COEFFICIENT_BOUND_ROWS.csv",
    "1014_route": OUT / "P8_Y5_R10_1014_ROUTE_SPLIT.csv",
    "1015_gate": OUT / "P8_Y5_R10_1015_CLAIM_GATE.csv",
}

NEEDLES = {
    "1713_doc": ["worldtube-Hilbert charge", "NEXT1713_0_primary"],
    "1713_validation": ["VAL1713_OVERALL", "PASS"],
    "1713_next": ["1714-Y5-R2FR-Y5-worldtube-Hilbert-source-equality-or-Req-Icommutator-fill.md", "selected"],
    "1713_y5_basis": ["Y5B1713_0_radial_Meff_hair", "MISSING_VALUE_OR_THEOREM"],
    "1713_profile": ["ACQ1713_1_Y5_JZ_basis", "MISSING_EIGHT_CHANNEL_VALUES_OR_THEOREMS"],
    "1356_doc": ["closed wrong charge", "Pi_M J_H = J_M_top + dB_zero"],
    "1356_equality": ["WHE1356_8_verdict", "EQUALITY_THEOREM_NOT_PROVED"],
    "1356_residuals": ["REQ1356_0_R_eq_integral", "REQ1356_1_I_commutator"],
    "1356_guard": ["GUARD1356_0_closed_wrong_charge", "INSTALLED"],
    "1356_next": ["1357-Y5-R10-RAB-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md", "do not fit G"],
    "parent_worldtube": ["W504_4_worldtube_source_measure_glue", "not_yet_derived_core_missing_piece"],
    "1013_doc": ["exact measured-GM obstruction", "nonclaim"],
    "1013_vector": ["OBS1013_3_topological_equality_residual", "MISSING_R_EQ_INTEGRAL"],
    "1014_doc": ["[d,Pi_M]J_H=0", "not derived"],
    "1014_commutator": ["PCT1014_3_Hilbert_equality", "not_derived_key_blocker"],
    "1014_coeffs": ["PCC1014_1_I_commutator", "retained_unfilled"],
    "1014_route": ["PRS1014_1_topological_Hilbert_equality", "fail_open"],
    "1015_gate": ["CG1015_3_topological_Hilbert_equality", "same-class and boundary-zero hypotheses are not parent-signed"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1714_SOURCE_REGISTER.csv"
EQUALITY_ATTEMPT = OUT / "P8_Y5_PARENT_QLOC_1714_WORLDTUBE_HILBERT_EQUALITY_ATTEMPT.csv"
RESIDUAL_ROWS = OUT / "P8_Y5_PARENT_QLOC_1714_REQ_ICOMMUTATOR_RESIDUAL_ROWS.csv"
GUARD_ROWS = OUT / "P8_Y5_PARENT_QLOC_1714_CLOSED_WRONG_CHARGE_GUARD.csv"
CHAIN_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1714_SOURCE_TO_NEWTON_CHAIN_AUDIT.csv"
RUNNER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_1714_RUNNER_REFUSAL.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1714_NEXT_TARGET.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1714_CLAIM_GATE.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1714_VALIDATION.csv"

GENERATED_CSVS = [
    SOURCE_REGISTER,
    EQUALITY_ATTEMPT,
    RESIDUAL_ROWS,
    GUARD_ROWS,
    CHAIN_AUDIT,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

CLAIM_CHECKED_CSVS = [
    EQUALITY_ATTEMPT,
    RESIDUAL_ROWS,
    GUARD_ROWS,
    CHAIN_AUDIT,
    RUNNER_REFUSAL,
    NEXT_TARGET,
    CLAIM_GATE,
]

COPY_TARGETS = {
    EQUALITY_ATTEMPT: [
        QUARANTINE / "WORLDTUBE_HILBERT_EQUALITY_ATTEMPT.csv",
        BRANCH_RESIDUALS / "R2FR_worldtube_Hilbert_equality_attempt_1714.csv",
        QUEUE / "JR1714_WORLDTUBE_HILBERT_EQUALITY_ATTEMPT.csv",
    ],
    RESIDUAL_ROWS: [
        QUARANTINE / "REQ_ICOMMUTATOR_RESIDUAL_ROWS.csv",
        BRANCH_RESIDUALS / "R2FR_Req_Icommutator_residual_rows_1714.csv",
        QUEUE / "JR1714_REQ_ICOMMUTATOR_RESIDUAL_ROWS.csv",
    ],
    GUARD_ROWS: [
        QUARANTINE / "CLOSED_WRONG_CHARGE_GUARD.csv",
        BRANCH_RESIDUALS / "R2FR_closed_wrong_charge_guard_1714.csv",
        QUEUE / "JR1714_CLOSED_WRONG_CHARGE_GUARD.csv",
    ],
    CHAIN_AUDIT: [
        QUARANTINE / "SOURCE_TO_NEWTON_CHAIN_AUDIT.csv",
        BRANCH_RESIDUALS / "R2FR_source_to_Newton_chain_audit_1714.csv",
        QUEUE / "JR1714_SOURCE_TO_NEWTON_CHAIN_AUDIT.csv",
    ],
    RUNNER_REFUSAL: [
        QUARANTINE / "RUNNER_REFUSAL.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_1714.csv",
        QUEUE / "JR1714_RUNNER_REFUSAL.csv",
    ],
    NEXT_TARGET: [
        QUARANTINE / "NEXT_TARGET.csv",
        BRANCH_RESIDUALS / "R2FR_next_target_1714.csv",
        QUEUE / "JR1714_NEXT_TARGET.csv",
    ],
    CLAIM_GATE: [
        QUARANTINE / "CLAIM_GATE.csv",
        BRANCH_RESIDUALS / "R2FR_claim_gate_1714.csv",
        QUEUE / "JR1714_CLAIM_GATE.csv",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _field in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (source_key, path) in enumerate(SOURCE_FILES.items()):
        text = read_text(path) if path.exists() else ""
        needles = NEEDLES[source_key]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC1714_{index}_{source_key}",
                "source_key": source_key,
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": all(needle in text for needle in needles),
                "required_needles": ";".join(needles),
                "use_in_1714": "Y5 worldtube-Hilbert equality attempt and R_eq/I_commutator fill",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def equality_attempt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "WHE1714_0_worldtube_setup",
            "compact source worldtube and exterior annulus are defined",
            "W compact, A=exterior(W), S1/S2 link W, no source support in A",
            "SETUP_AVAILABLE",
            "Stokes comparison is meaningful once the charge form exists",
            "no clean inside/outside split means no mass-flux theorem",
        ),
        (
            "WHE1714_1_parent_Noether_charge",
            "parent diffeomorphism action supplies a Noether/Hamiltonian mass charge",
            "delta L=E_A delta Phi^A+dTheta; J_tau=Theta(Phi,L_tau Phi)-i_tau L; J_tau=dQ_M[tau]+constraints",
            "CONDITIONAL_NOT_PARENT_SUPPLIED",
            "standard covariant phase-space route identified",
            "without explicit parent L, Theta and Q_M[tau], normalization can be wrong",
        ),
        (
            "WHE1714_2_same_frame_Hilbert_current",
            "same-frame Hilbert/source current defines observed source mass",
            "J_H[e_obs] from matter Hilbert variation and M_source[W]=int_W Pi_M J_H",
            "NOT_PARENT_DERIVED",
            "same-frame requirement is known",
            "source-normalization hair can hide as fitted GM",
        ),
        (
            "WHE1714_3_topological_mass_identity",
            "exterior/topological charge is the mass charge, not merely closed",
            "J_M_top=dQ_M[tau] and Q_M[tau] is the measured source generator",
            "CHARGE_IDENTITY_NOT_ENOUGH",
            "surface independence is not enough",
            "closed wrong charge can mimic a conserved mass",
        ),
        (
            "WHE1714_4_same_object_equality",
            "projected Hilbert current equals topological mass current up to exact boundary term",
            "Pi_M J_H = J_M_top + dB_zero, with boundary flux zero on linked worldtube/exterior boundary",
            "NOT_DERIVED_KEY_BLOCKER",
            "this is the exact equality needed for Newton source recovery",
            "R_eq remains explicit",
        ),
        (
            "WHE1714_5_exterior_closure",
            "compact-exterior projected Hilbert flux closes without extra/projector/anomaly terms",
            "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H=0 after extra, boundary, projector and parent-anomaly channels vanish",
            "EXACT_OBSTRUCTION_NOT_ZERO",
            "product rule isolates I_commutator and companion terms",
            "I_commutator and radial/time/source residuals survive",
        ),
        (
            "WHE1714_6_worldtube_glue",
            "worldtube source measure equals exterior surface charge before fitting",
            "M_source[W]=int_S Q_M[tau]=M_eff for any valid linking surface S",
            "NOT_DERIVED_CORE_MISSING_PIECE",
            "core source-normalization bridge is named",
            "Newton recovery cannot use the charge as measured source mass",
        ),
        (
            "WHE1714_7_Newton_Poisson_orbit",
            "same charge sources Poisson/Gauss and inverse-square orbital acceleration",
            "Q_M[tau] -> Komar/ADM/Gauss mass and nabla^2 Phi=4 pi G_ref rho_H with fixed G_ref, no fitted-G absorption",
            "CONDITIONAL_NOT_PARENT_DERIVED",
            "Newton/GR limit target is precise",
            "right-looking conservation can still have wrong normalization or wrong source",
        ),
        (
            "WHE1714_8_verdict",
            "worldtube-Hilbert source equality theorem",
            "WHE1714_0 through WHE1714_7 all pass with parent action, Q_M, Pi_M, B_zero_flux and calibration",
            "EQUALITY_THEOREM_NOT_PROVED",
            "attempt reduces to exact same-object equality",
            "retain R_eq, I_commutator, B_zero_flux, projector stress, parent anomaly, radial leakage and calibration rows",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": clause_id,
            "claim_piece": claim_piece,
            "required_form": required_form,
            "current_status": status,
            "progress": progress,
            "if_missing": if_missing,
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for clause_id, claim_piece, required_form, status, progress, if_missing in rows
    ]


def residual_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "REQ1714_0_R_eq_integral",
            "R_eq[W,S]",
            "M_source[W] - int_S Q_M[tau]",
            "Pi_M J_H - J_M_top - dB_zero",
            "Newton source normalization; beta_minus_1; orbital GM; R10/R11 cross-checks",
            "mass or dimensionless delta GM/GM after normalization",
            "parent Q_M[tau], Pi_M J_H, B_zero_flux, calibration convention",
        ),
        (
            "REQ1714_1_I_commutator",
            "I_commutator",
            "int_A [d,Pi_M] J_H",
            "d(Pi_M J_H)=Pi_M dJ_H+[d,Pi_M]J_H",
            "projector/source hair; PPN preferred-frame; radial M_eff drift; R10/R11",
            "mass flux or dimensionless projected GM fraction",
            "explicit Pi_M, domain/topology dependence, J_H frame, exterior annulus A",
        ),
        (
            "REQ1714_2_B_zero_flux",
            "B_zero_flux",
            "worldtube/exterior boundary contribution from exact term dB_zero",
            "int_boundary B_zero=0 required for Pi_M J_H and J_M_top equality",
            "boundary monopole; beta_minus_1; Gdot/G; orbital calibration",
            "mass or dimensionless boundary GM fraction",
            "boundary condition, asymptotic falloff, inner-worldtube matching",
        ),
        (
            "REQ1714_3_projector_stress_beta_equiv",
            "beta_projector",
            "metric variation of Pi_M and equivalent projector stress in the source channel",
            "delta_g(Pi_M J_H) residual",
            "PPN beta/gamma/preferred-frame residual vector",
            "dimensionless PPN coefficient map",
            "metric response of Pi_M and same-frame source current",
        ),
        (
            "REQ1714_4_Delta_PiM",
            "Delta_PiM",
            "projector/domain mismatch between topological and Hilbert source selectors",
            "Pi_M^top - Pi_M^Hilbert",
            "source species/material dependence; WEP/source charge residuals",
            "dimensionless projector mismatch",
            "operator-level definition of both projectors and material/source map",
        ),
        (
            "REQ1714_5_epsilon_radial_Meff",
            "epsilon_radial_Meff",
            "radial dependence of measured effective mass in compact exterior annulus",
            "partial_r ln M_eff(r)",
            "orbital acceleration residual; inverse-square law; alpha(lambda)",
            "1/length or dimensionless per radial convention",
            "radial profile for exterior flux leakage and normalization",
        ),
        (
            "REQ1714_6_parent_anomaly_A_parent",
            "A_parent",
            "parent Noether anomaly or non-EH contribution to mass-current closure",
            "dJ_tau=A_parent plus constraints/off-shell source terms",
            "non-EH operator family; local-GR residual vector",
            "mass-current divergence or dimensionless normalized anomaly",
            "explicit parent Lagrangian and boundary symplectic potential",
        ),
        (
            "REQ1714_7_calibration_PPN_tail",
            "Delta_cal_PPN",
            "closed-charge-to-orbital-readout calibration mismatch after fixing G_ref",
            "G_fit M_charge - G_ref M_source",
            "beta_minus_1; Gdot/G; orbital GM consistency",
            "dimensionless fractional calibration vector",
            "absolute calibration theorem and no-absorption audit",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "residual_id": residual_id,
            "symbol": symbol,
            "definition": definition,
            "source_equation": equation,
            "observable_link": observable,
            "units_required": units,
            "required_to_score": required,
            "value_or_theorem": "MISSING",
            "accepted_for_scoring": False,
            "status": "RETAINED_NONCLAIM",
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for residual_id, symbol, definition, equation, observable, units, required in rows
    ]


def guard_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GUARD1714_0_closed_wrong_charge",
            "closed exterior charge is not enough for Newton recovery",
            "use dQ_M=0 or surface independence as proof that Q_M is measured source mass",
            "prove Pi_M J_H=J_M_top+dB_zero and B_zero_flux=0, or retain R_eq",
        ),
        (
            "GUARD1714_1_no_fitted_G_absorption",
            "do not absorb source residuals into fitted G",
            "hide radial/time/species/frame source-normalization terms by redefining G_fit",
            "split constant calibration from Z-dependent residual rows",
        ),
        (
            "GUARD1714_2_no_post_readout_projector",
            "Pi_M must be parent/before-readout, not a mask selected after seeing observables",
            "choose Pi_M to remove measured residual after orbital fitting",
            "derive Pi_M from parent quotient/topological structure before scoring",
        ),
        (
            "GUARD1714_3_no_reference_zero",
            "boundary and calibration zeros require theorem or sourced bound",
            "set B_zero_flux, I_commutator or R_eq to zero by reference choice",
            "supply theorem-zero certificates or nonclaim numeric source rows",
        ),
        (
            "GUARD1714_4_same_charge_chain",
            "one source charge must flow through worldtube measure, Hilbert/topological charge, Poisson source and orbit",
            "prove only one link and call it Newton/GR recovery",
            "audit every chain link or keep source-normalization residuals active",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "guardrail": guardrail,
            "forbidden_move": forbidden,
            "allowed_replacement": allowed,
            "status": "INSTALLED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, guardrail, forbidden, allowed in rows
    ]


def chain_audit_rows() -> list[dict[str, Any]]:
    rows = [
        ("CHAIN1714_0_parent_action", "parent covariant action and Noether charge", "L, Theta, J_tau, Q_M[tau]", "CONDITIONAL_NOT_SUPPLIED", "mass charge could be postulated/renormalized"),
        ("CHAIN1714_1_worldtube_source", "compact Hilbert/source worldtube measure", "M_source[W]=int_W Pi_M J_H[e_obs]", "NOT_PARENT_DERIVED", "observed source mass may differ from exterior charge"),
        ("CHAIN1714_2_same_object_equality", "Hilbert current equals topological current up to exact zero-flux boundary", "Pi_M J_H=J_M_top+dB_zero", "NOT_DERIVED_KEY_BLOCKER", "R_eq remains live"),
        ("CHAIN1714_3_projector_commutator", "projector commutes with exterior derivative/current closure", "[d,Pi_M]J_H=0", "NOT_DERIVED", "I_commutator remains live"),
        ("CHAIN1714_4_boundary_silence", "boundary improvement has no linked flux", "int_boundary B_zero=0", "OPEN", "boundary monopole/source calibration remains live"),
        ("CHAIN1714_5_Poisson_Gauss", "same charge sources weak-field Poisson/Gauss equation", "nabla^2 Phi=4 pi G_ref rho_H", "CONDITIONAL_NOT_PARENT_DERIVED", "Newton limit not claimable"),
        ("CHAIN1714_6_orbital_readout", "same charge produces inverse-square orbital acceleration with fixed calibration", "a_r=-G_ref M_source/r^2 and no fitted-G absorption", "CONDITIONAL_NOT_PARENT_DERIVED", "orbital GM can hide residual source-normalization"),
        ("CHAIN1714_7_verdict", "source-to-Newton chain", "all links above pass with source paths", "CHAIN_NOT_CLOSED", "Newton/local-GR source normalization remains blocked"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "chain_id": chain_id,
            "link": link,
            "required_identity": identity,
            "current_status": status,
            "failure_mode": failure,
            "parent_signed": False,
            "source_backed": False,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for chain_id, link, identity, status, failure in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        ("RUN1714_0_equality_claim", "claim M_source[W]=int_S Q_M[tau]=M_eff", "REJECT_NOT_PARENT_SIGNED", "same-object equality, B_zero_flux, parent Q_M and fixed calibration are unsigned"),
        ("RUN1714_1_closed_charge", "use closed/surface-independent charge as Newton source", "REJECT_CLOSED_WRONG_CHARGE", "closure does not prove measured source identity"),
        ("RUN1714_2_R_eq_score", "score R_eq/I_commutator rows", "NOT_RUN_TEMPLATE_ONLY", "residual rows are MISSING values/theorems and not source-backed"),
        ("RUN1714_3_fitted_G", "absorb residual source-normalization into fitted G", "FORBIDDEN_NO_ABSORPTION", "Z-dependent radial/time/species/frame residuals must remain explicit"),
        ("RUN1714_4_Newton_GR", "claim Newton/local-GR source normalization", "BLOCKED_NO_CLAIM", "source-to-Newton chain is not closed"),
        ("RUN1714_5_q_loc_profile", "promote finite q_loc profile", "NOT_RUN_TEMPLATE_ONLY", "q_loc/JZ/BZ coefficients remain missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "score_emitted": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for runner_id, case, status, reason in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "NEXT1714_0_primary",
            "1715-Y5-R2FR-PiM-commutator-fixed-topology-or-Icommutator-source-profile.md",
            "scripts/Y5_R2FR_PiM_commutator_fixed_topology_or_Icommutator_source_profile.py",
            "try to derive [d,Pi_M]J_H=0 from fixed topology, before-readout projector ownership and compact-exterior source silence; if not, fill I_commutator/source-profile rows",
            "selected",
        ),
        (
            "NEXT1714_1_parallel_Req",
            "1715b-Y5-R2FR-R_eq-topological-Hilbert-equality-bound-runner.md",
            "scripts/Y5_R2FR_R_eq_topological_Hilbert_equality_bound_runner.py",
            "parallel R_eq equality/bound route if commutator theorem stalls",
            "held_parallel",
        ),
        (
            "NEXT1714_2_parallel_Y6",
            "1715c-Y5-R2FR-Y6-extra-stress-DeltaK-bound-ledger.md",
            "scripts/Y5_R2FR_Y6_extra_stress_DeltaK_bound_ledger.py",
            "Y6 remains parallel but should not replace Y5 source-normalization gate",
            "held_parallel",
        ),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": route_id,
            "next_target": target,
            "script": script,
            "objective": objective,
            "selection_status": status,
            "success_condition": "Pi_M commutator theorem-zero certificate or explicit nonclaim I_commutator profile inputs with units and source paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for route_id, target, script, objective, status in rows
    ]


def claim_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG1714_0_worldtube_Hilbert_equality", "M_source[W]=int_S Q_M[tau]=M_eff is derived", "BLOCKED_NO_CLAIM", "same-object equality, B_zero_flux and parent Q_M are not signed"),
        ("CG1714_1_R_eq_Icomm_ready", "R_eq/I_commutator rows are numeric/source-backed and scoreable", "BLOCKED_NO_CLAIM", "rows are explicit but remain MISSING/nonclaim"),
        ("CG1714_2_closed_charge_Newton", "closed exterior charge is enough for Newton recovery", "BLOCKED_NO_CLAIM", "closed-wrong-charge guard forbids this move"),
        ("CG1714_3_Newton_GR_recovery", "Newton/local-GR source normalization can reopen", "BLOCKED_NO_CLAIM", "worldtube-Hilbert equality and calibration are blocked"),
        ("CG1714_4_q_loc_profile", "finite q_loc/JZ/BZ profile can be scored", "BLOCKED_NO_CLAIM", "q_loc/JZ/BZ coefficients remain missing"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            "gate_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, status, reason in rows
    ]


def parse_all(paths: list[Path]) -> bool:
    for path in paths:
        read_csv(path)
    return True


def claim_flags_false(paths: list[Path]) -> bool:
    checked_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "gate_pass",
        "score_emitted",
        "parent_signed",
        "source_backed",
        "accepted_for_scoring",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in checked_keys and truthy(value):
                    return False
    return True


def formalization_1714_hits() -> list[Path]:
    if not FORMALIZATION.exists():
        return []
    return [
        path
        for path in FORMALIZATION.rglob("*1714*")
        if path.is_file() and ".venv" not in path.parts and "__pycache__" not in path.parts
    ]


def copy_outputs() -> None:
    for source, targets in COPY_TARGETS.items():
        for target in targets:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    source_rows: list[dict[str, Any]],
    equality_rows: list[dict[str, Any]],
    residual_rows_: list[dict[str, Any]],
    guard_rows_: list[dict[str, Any]],
    chain_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    remove_pycache()
    checks = [
        ("VAL1714_0_sources_exist", all(row["exists"] for row in source_rows), "all cited source paths exist"),
        ("VAL1714_1_needles_present", all(row["needles_present"] for row in source_rows), "required source needles are present"),
        (
            "VAL1714_2_equality_not_promoted",
            any(row["clause_id"] == "WHE1714_8_verdict" and row["current_status"] == "EQUALITY_THEOREM_NOT_PROVED" for row in equality_rows),
            "worldtube-Hilbert equality theorem remains unproved",
        ),
        (
            "VAL1714_3_required_residuals_present",
            len(residual_rows_) >= 8
            and any(row["residual_id"] == "REQ1714_0_R_eq_integral" for row in residual_rows_)
            and any(row["residual_id"] == "REQ1714_1_I_commutator" for row in residual_rows_),
            "R_eq/I_commutator and companion residual rows are present",
        ),
        (
            "VAL1714_4_residuals_nonclaim",
            all(row["value_or_theorem"] == "MISSING" and row["status"] == "RETAINED_NONCLAIM" for row in residual_rows_),
            "residual rows remain missing/unscored/nonclaim",
        ),
        (
            "VAL1714_5_closed_wrong_charge_guard",
            len(guard_rows_) >= 4 and all(row["status"] == "INSTALLED" for row in guard_rows_),
            "closed-wrong-charge/no-fitted-G guardrails installed",
        ),
        (
            "VAL1714_6_source_to_Newton_chain_blocked",
            any(row["chain_id"] == "CHAIN1714_7_verdict" and row["current_status"] == "CHAIN_NOT_CLOSED" for row in chain_rows),
            "source-to-Newton chain remains blocked",
        ),
        (
            "VAL1714_7_runner_refuses_shortcuts",
            all("REJECT" in row["status"] or "NOT_RUN" in row["status"] or "FORBIDDEN" in row["status"] or "BLOCKED" in row["status"] for row in runner_rows_),
            "runner refuses closed-charge/fitted-G/Newton shortcuts",
        ),
        (
            "VAL1714_8_next_selected",
            any(row["route_id"] == "NEXT1714_0_primary" and row["selection_status"] == "selected" for row in next_rows_),
            "next target selects PiM commutator fixed-topology route",
        ),
        (
            "VAL1714_9_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" for row in claim_rows_),
            "all claim gates remain blocked",
        ),
        ("VAL1714_10_csv_parse", parse_all(GENERATED_CSVS), "all generated 1714 CSVs parse"),
        (
            "VAL1714_11_no_claim_flags",
            claim_flags_false(CLAIM_CHECKED_CSVS),
            "all generated scoring and claim flags remain false",
        ),
        (
            "VAL1714_12_branch_copies",
            all(target.exists() for targets in COPY_TARGETS.values() for target in targets),
            "branch/quarantine/queue copies exist",
        ),
        (
            "VAL1714_13_pycache_absent",
            not (ROOT / "scripts" / "__pycache__").exists(),
            "scripts __pycache__ absent",
        ),
        (
            "VAL1714_14_formalization_untouched",
            not formalization_1714_hits(),
            "no 1714 outputs found under formalization-workbench",
        ),
    ]
    rows = [
        {"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1714_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1714 Y5 worldtube-Hilbert equality and R_eq/I_commutator validation",
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    equality_rows: list[dict[str, Any]],
    residual_rows_: list[dict[str, Any]],
    guard_rows_: list[dict[str, Any]],
    chain_rows: list[dict[str, Any]],
    runner_rows_: list[dict[str, Any]],
    next_rows_: list[dict[str, Any]],
    claim_rows_: list[dict[str, Any]],
    validation_rows_: list[dict[str, Any]],
) -> None:
    content = "\n\n".join(
        [
            "# 1714 - Y5 Worldtube-Hilbert Source Equality Or R_eq/I_commutator Fill",
            "## Verdict\n"
            "- 1714 does not derive the worldtube-Hilbert source equality, so Newton/source-normalization stays blocked.\n"
            "- A closed exterior/topological charge is not enough; it must be the same object as the observed Hilbert/worldtube source mass.\n"
            "- The exact required bridge is `Pi_M J_H = J_M_top + dB_zero` plus zero linked boundary flux and fixed calibration.\n"
            "- The retained nonclaim residuals are `R_eq`, `I_commutator`, `B_zero_flux`, projector stress, `Delta_PiM`, radial `M_eff` leakage, parent anomaly and calibration tail.\n"
            "- The no-fitted-G/no-closed-wrong-charge guard is installed for the live R2FR branch.",
            "## Source Register\n" + table(source_rows, ["source_id", "source_key", "source_path", "exists", "needles_present"]),
            "## Worldtube-Hilbert Equality Attempt\n"
            + table(equality_rows, ["clause_id", "claim_piece", "required_form", "current_status", "progress", "if_missing"]),
            "## R_eq/I_commutator Residual Rows\n"
            + table(residual_rows_, ["residual_id", "symbol", "definition", "source_equation", "observable_link", "value_or_theorem", "status"]),
            "## Closed-Wrong-Charge Guard\n"
            + table(guard_rows_, ["guard_id", "guardrail", "forbidden_move", "allowed_replacement", "status"]),
            "## Source-To-Newton Chain Audit\n"
            + table(chain_rows, ["chain_id", "link", "required_identity", "current_status", "failure_mode"]),
            "## Runner Refusal\n" + table(runner_rows_, ["runner_id", "case", "status", "reason"]),
            "## Next Target\n" + table(next_rows_, ["route_id", "next_target", "script", "objective", "selection_status"]),
            "## Claim Gates\n" + table(claim_rows_, ["claim_id", "claim", "status", "reason"]),
            "## Validation\n" + table(validation_rows_, ["check_id", "result", "detail"]),
            "## Working Interpretation\n"
            "This is a good kind of failure: the gap is now local and algebraic, not vague. To connect MTS to Newton/GR honestly, we need the same charge to survive the chain worldtube source -> Hilbert current -> topological charge -> Poisson source -> orbital readout. The next best target is `[d,Pi_M]J_H=0`; if that falls, `I_commutator` becomes a finite residual to source and test.",
        ]
    )
    DOC.write_text(content + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    equality_rows = equality_attempt_rows()
    residual_rows_ = residual_rows()
    guard_rows_ = guard_rows()
    chain_rows = chain_audit_rows()
    runner_rows_ = runner_rows()
    next_rows_ = next_rows()
    claim_rows_ = claim_rows()

    write_csv(SOURCE_REGISTER, source_rows)
    write_csv(EQUALITY_ATTEMPT, equality_rows)
    write_csv(RESIDUAL_ROWS, residual_rows_)
    write_csv(GUARD_ROWS, guard_rows_)
    write_csv(CHAIN_AUDIT, chain_rows)
    write_csv(RUNNER_REFUSAL, runner_rows_)
    write_csv(NEXT_TARGET, next_rows_)
    write_csv(CLAIM_GATE, claim_rows_)
    copy_outputs()

    validation_rows_ = validation_rows(
        source_rows,
        equality_rows,
        residual_rows_,
        guard_rows_,
        chain_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
    )
    write_csv(VALIDATION, validation_rows_)
    write_doc(
        source_rows,
        equality_rows,
        residual_rows_,
        guard_rows_,
        chain_rows,
        runner_rows_,
        next_rows_,
        claim_rows_,
        validation_rows_,
    )

    print(f"wrote {DOC}")
    print(f"wrote {VALIDATION}")
    print(f"1714 validation {validation_rows_[-1]['result']}")


if __name__ == "__main__":
    main()
