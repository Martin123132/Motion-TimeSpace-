from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

RUN15 = ROOT / "runs" / "20260530-232024-local-observables-data-map" / "results"
RUN16 = ROOT / "runs" / "20260530-232506-local-bounds-gate-runner" / "results"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv"

BRANCH_ID = "MTS_R2FR_RAB_LAMBDA_ORIGIN_OR_QR_ENVELOPE_RUNNER_2263"
DOC = ROOT / "2263-Y5-R2FR-RAB-constrained-parent-action-lambda-origin-or-qR-envelope-runner.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2263_00_2262_doc",
        "source_key": "2262_doc",
        "source_path": ROOT / "2262-Y5-R2FR-RAB-ownership-as-quotient-representative-or-finite-residual-envelope.md",
        "needles": ["NPR2262_3_best_derivation_route", "ENV2262_0_qR_local_residual", "NEXT2262_0_primary"],
        "role": "handoff: lambda-origin or finite q_R envelope selected",
    },
    {
        "source_id": "SRC2263_01_2262_validation",
        "source_key": "2262_validation",
        "source_path": OUT / "P8_Y5_BRR545_2262_VALIDATION.csv",
        "needles": ["VAL2262_OVERALL", "PASS"],
        "role": "confirms 2262 passed before 2263 starts",
    },
    {
        "source_id": "SRC2263_02_2262_envelope",
        "source_key": "2262_envelope",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2262_FINITE_RAB_RESIDUAL_ENVELOPE.csv",
        "needles": ["ENV2262_0_qR_local_residual", "FINITE_ENVELOPE_SCHEMA_READY_NONCLAIM"],
        "role": "nonclaim q_R/Q_R residual envelope seed",
    },
    {
        "source_id": "SRC2263_03_07_constraint",
        "source_key": "constraint_07",
        "source_path": ROOT / "07-nonpropagating-reciprocity-constraint.md",
        "needles": ["S_constraint = integral lambda_R R_AB", "no R_AB kinetic term", "parent origin is still open"],
        "role": "clean nonpropagating constraint route",
    },
    {
        "source_id": "SRC2263_04_08_phase",
        "source_key": "phase_08",
        "source_path": ROOT / "08-phase-volume-reciprocity-origin.md",
        "needles": ["T sqrt(S) = 1", "radial t-r clock-routing cell preservation", "candidate principle, not a parent theorem"],
        "role": "motion-capacity/radial-cell motivation",
    },
    {
        "source_id": "SRC2263_05_09_hamiltonian",
        "source_key": "hamiltonian_09",
        "source_path": ROOT / "09-hamiltonian-radial-cell-derivation.md",
        "needles": ["generic symplectic or Liouville phase-volume preservation does not derive p=1", "separately conserved"],
        "role": "rejects generic Hamiltonian/Liouville derivation",
    },
    {
        "source_id": "SRC2263_06_10_observer",
        "source_key": "observer_10",
        "source_path": ROOT / "10-observer-map-symplectic-contract.md",
        "needles": ["R_AB = ln(T^2 S)", "J_q = 1", "contract not satisfied"],
        "role": "R_AB/J_q normalization and missing theorem",
    },
    {
        "source_id": "SRC2263_07_11_current",
        "source_key": "current_11",
        "source_path": ROOT / "11-cell-current-origin-attempt.md",
        "needles": ["W partial_r R_AB = Q_R", "Q_R = 0", "ordinary cell-current conservation does not close"],
        "role": "ordinary current route leaves Q_R hair",
    },
    {
        "source_id": "SRC2263_08_12_noether",
        "source_key": "noether_12",
        "source_path": ROOT / "12-gauge-noether-origin-audit.md",
        "needles": ["Noether identity", "first-class parent constraint", "closure-only"],
        "role": "gauge/Noether audit: constraint possible but absent",
    },
    {
        "source_id": "SRC2263_09_14_sensitivity",
        "source_key": "sensitivity_14",
        "source_path": ROOT / "14-closure-deviation-PPN-sensitivity.md",
        "needles": ["q_R:", "Linear Sensitivities", "not observational constraints"],
        "role": "internal conversion coefficients from q_R/beta/clock/matter leaks to observables",
    },
    {
        "source_id": "SRC2263_10_15_map",
        "source_key": "map_15",
        "source_path": ROOT / "15-local-observables-data-map.md",
        "needles": ["q_R:", "2.3e-5", "screening-ready"],
        "role": "published local screening gates map",
    },
    {
        "source_id": "SRC2263_11_16_runner",
        "source_key": "runner_16",
        "source_path": ROOT / "16-local-bounds-gate-runner.md",
        "needles": ["q_R <= 2.3e-5", "Q_R = 0", "operational screening harness"],
        "role": "prior local bounds gate runner",
    },
    {
        "source_id": "SRC2263_12_gates_15",
        "source_key": "gates_15",
        "source_path": RUN15 / "mts_parameter_screening_gates.csv",
        "needles": ["q_R,2.3e-05", "delta_beta,7.16e-05", "Q_R,0.0"],
        "role": "machine-readable local screening gates",
    },
    {
        "source_id": "SRC2263_13_translations_15",
        "source_key": "translations_15",
        "source_path": RUN15 / "observable_bound_translations.csv",
        "needles": ["solar_light_bending", "mercury_perihelion_beta", "gps_gravitational_redshift"],
        "role": "machine-readable observable conversion coefficients",
    },
    {
        "source_id": "SRC2263_14_summary_16",
        "source_key": "summary_16",
        "source_path": RUN16 / "candidate_branch_summary.csv",
        "needles": ["closure_null", "qR_ten_times_gate", "kinetic_QR_hair_small_gamma"],
        "role": "prior pass/fail branch screening summary",
    },
    {
        "source_id": "SRC2263_15_gate_results_16",
        "source_key": "gate_results_16",
        "source_path": RUN16 / "branch_parameter_gate_results.csv",
        "needles": ["qR_at_cassini_gate", "Q_R", "fail"],
        "role": "prior parameter-by-parameter screening results",
    },
    {
        "source_id": "SRC2263_16_local_bounds",
        "source_key": "local_bounds",
        "source_path": LOCAL_BOUNDS,
        "needles": ["Cassini_Shapiro_gamma_2003", "R3_gamma", "R10_fifth_force"],
        "role": "local published-bound source ledger",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2263_SOURCE_REGISTER.csv",
    "lambda_origin_audit": OUT / "P8_Y5_PARENT_QLOC_2263_LAMBDA_ORIGIN_AUDIT.csv",
    "constraint_contract": OUT / "P8_Y5_PARENT_QLOC_2263_CONSTRAINED_PARENT_ACTION_CONTRACT.csv",
    "constraint_algebra_gates": OUT / "P8_Y5_PARENT_QLOC_2263_CONSTRAINT_ALGEBRA_GATES.csv",
    "screening_gates": OUT / "P8_Y5_PARENT_QLOC_2263_LOCAL_SCREENING_GATES.csv",
    "observable_translations": OUT / "P8_Y5_PARENT_QLOC_2263_OBSERVABLE_TRANSLATIONS.csv",
    "qr_candidate_runner": OUT / "P8_Y5_PARENT_QLOC_2263_QR_CANDIDATE_SCREENING_RUNNER.csv",
    "qr_candidate_impacts": OUT / "P8_Y5_PARENT_QLOC_2263_QR_CANDIDATE_OBSERVABLE_IMPACTS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2263_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2263_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2263_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2263_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2263_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2263_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue_contract": QUEUE / "JR2263_LAMBDA_ORIGIN_CONTRACT_NONCLAIM.csv",
    "queue_qr_runner": QUEUE / "JR2263_QR_SCREENING_RUNNER_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "RAB_lambda_origin_and_qR_screening_refusal_2263.csv",
    "beta_docs": BETA_DOCS / "RAB_LAMBDA_ORIGIN_OR_QR_ENVELOPE_2263_NONCLAIM.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        try:
            return str(path.relative_to(PROJECT_ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = next((key for key in ("check_id", "validation_id", "id") if key in rows[0]), "")
    result_key = next((key for key in ("result", "status") if key in rows[0]), "")
    if not result_key:
        return False
    overall = [row for row in rows if id_key and "overall" in row.get(id_key, "").lower()]
    return all(row.get(result_key, "").lower() == "pass" for row in (overall or rows))


def source_path(key: str) -> Path:
    return next(source["source_path"] for source in SOURCES if source["source_key"] == key)


def source_refs(*keys: str) -> str:
    return ";".join(rel(source_path(key)) for key in keys)


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": rel(path),
                "exists": exists,
                "needles": ";".join(source["needles"]),
                "needles_present": exists and all(needle in text for needle in source["needles"]),
                "validation_overall_pass": validation_pass(path) if "validation" in source["source_key"] else "",
                "role": source["role"],
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def lambda_origin_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "LAM2263_0_motion_capacity_identity",
            "candidate_origin": "c^2=v_space^2+v_clock^2+v_load^2",
            "derives": "T^2=1-L clock/load side",
            "does_not_derive": "spatial routing S or J_q=T sqrt(S)=1",
            "status": "PARTIAL_SUPPORT_ONLY",
            "why_it_fails": "clock capacity alone leaves the routing exponent p open",
            "source_path": source_refs("2262_doc", "phase_08"),
        },
        {
            "audit_id": "LAM2263_1_radial_cell_principle",
            "candidate_origin": "radial t-r clock-routing cell preservation",
            "derives": "if adopted, T sqrt(S)=1 and therefore R_AB=0/p=1",
            "does_not_derive": "why this specific cell is separately preserved",
            "status": "MOTIVATED_NOT_PARENT_DERIVED",
            "why_it_fails": "generic volume, Hamiltonian, and Liouville preservation are too weak",
            "source_path": source_refs("phase_08", "hamiltonian_09", "observer_10"),
        },
        {
            "audit_id": "LAM2263_2_cell_current",
            "candidate_origin": "conserved reciprocal-cell current",
            "derives": "W partial_r R_AB=Q_R",
            "does_not_derive": "Q_R=0",
            "status": "REJECTED_AS_ZERO_THEOREM",
            "why_it_fails": "ordinary current conservation creates a conserved hair charge rather than a constraint",
            "source_path": source_refs("current_11", "constraint_07"),
        },
        {
            "audit_id": "LAM2263_3_gauge_noether",
            "candidate_origin": "coordinate gauge, cell-scale gauge, or bare Noether identity",
            "derives": "a warning about what cannot be used",
            "does_not_derive": "lambda_R equation R_AB=0",
            "status": "REJECTED_CURRENT_SCAFFOLD",
            "why_it_fails": "areal radius fixes radial gauge; cell-scale changes observables; Noether identities relate equations but do not create a multiplier equation",
            "source_path": source_refs("noether_12", "observer_10"),
        },
        {
            "audit_id": "LAM2263_4_nonpropagating_constraint",
            "candidate_origin": "parent algebraic constraint S_lambda=int lambda_R R_AB",
            "derives": "R_AB=0 and no Q_R hair if parent-signed",
            "does_not_derive": "the parent origin of lambda_R",
            "status": "EXACT_CONDITIONAL_NOT_SIGNED",
            "why_it_fails": "current corpus can state the constraint but cannot yet derive it from primitives",
            "source_path": source_refs("constraint_07", "2262_doc"),
        },
        {
            "audit_id": "LAM2263_5_verdict",
            "candidate_origin": "lambda_R origin",
            "derives": "nothing claimable yet",
            "does_not_derive": "local GR/Newton/PPN safety",
            "status": "LAMBDA_ORIGIN_NOT_DERIVED_CURRENTLY",
            "why_it_fails": "the missing theorem is a constrained parent action or constraint algebra, not another name for reciprocity",
            "source_path": source_refs("2262_doc", "runner_16"),
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **row, "valid_for_claim": False, "claim_allowed": False} for row in rows]


def constrained_parent_action_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("CPA2263_0_parent_variable", "parent variable owns J_q or R_AB", "J_q=T sqrt(S), R_AB=2 ln J_q, and the parent action declares whether this is constrained data", "CONTRACT_WRITTEN_NOT_DERIVED", "derive the parent variable and measure from motion/time/space primitives"),
        ("CPA2263_1_multiplier_origin", "lambda_R origin", "lambda_R is a parent multiplier/reaction stress associated with radial-cell capacity balance, not an inserted GR lock", "MISSING_PARENT_ORIGIN", "derive lambda_R from a constraint algebra or variational capacity principle"),
        ("CPA2263_2_action_form", "nonpropagating action form", "S_parent=S_Q[Q,Psi,theta]+int mu lambda_R R_AB with no D R_AB term", "EXACT_IF_SIGNED", "show this is generated by ParentGenerate rather than appended"),
        ("CPA2263_3_variation", "constraint variation", "delta_lambda S=R_AB=0 and delta_R S solves lambda_R/reaction terms without producing Q_R hair", "FORMAL_CONDITIONAL", "prove allowed boundary variations and reaction stress ownership"),
        ("CPA2263_4_no_kinetic_operator", "operator exclusion", "D R_AB and D lambda_R constructors are absent or pure boundary-exact", "MISSING_GRAMMAR_PROOF", "typed ParentGenerate grammar must exclude kinetic reciprocal strain"),
        ("CPA2263_5_matter_order", "matter/readout order", "matter/readout uses the constrained observed coframe after parent variation, with no shadow frame", "UNSIGNED_READOUT_ORDER", "derive same-coframe matter functor and no-marker constants"),
        ("CPA2263_6_no_GR_import", "no GR import", "the constraint is not Schwarzschild AB=1, Einstein vacuum equations, or fitted p=1 in disguise", "POLICY_GATE_ACTIVE", "source the derivation from primitives only"),
        ("CPA2263_7_verdict", "constrained parent action", "CPA2263_0 through CPA2263_6 jointly close", "NOT_DERIVED_CURRENT_CORPUS", "move to q_R envelope until the parent action is supplied"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "contract_clause": clause,
            "required_statement": statement,
            "current_status": status,
            "missing_for_claim": missing,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for contract_id, clause, statement, status, missing in rows
    ]


def constraint_algebra_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CAG2263_0_primary_constraint", "primary multiplier", "pi_lambda approximately 0 and delta_lambda S=R_AB", "MISSING_PARENT_HAMILTONIAN"),
        ("CAG2263_1_secondary_constraint", "secondary radial-cell constraint", "R_AB approximately 0 preserved under parent evolution", "MISSING_CONSTRAINT_EVOLUTION"),
        ("CAG2263_2_reaction_stress", "reaction stress ownership", "lambda_R enters only as reaction stress enforcing cell balance, not as new long-range source", "MISSING_REACTION_STRESS_MAP"),
        ("CAG2263_3_boundary", "boundary/corner differentiability", "boundary variation has no R_AB hair charge or cancels with exact/proper term", "MISSING_BOUNDARY_PROOF"),
        ("CAG2263_4_degree_count", "degree count", "R_AB/lambda_R pair carries no propagating local degree", "MISSING_DIRAC_COUNT"),
        ("CAG2263_5_matter", "matter/source compatibility", "ordinary matter cannot source the constrained variable independently", "MISSING_MATTER_DESCENT"),
        ("CAG2263_6_verdict", "constraint algebra closes", "all constraint and boundary gates close jointly", "NOT_CLOSED"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "gate": gate,
            "required_statement": required,
            "current_status": status,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for gate_id, gate, required, status in rows
    ]


def local_screening_gate_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(source_path("gates_15")):
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "parameter": row["mts_parameter"],
                "adopted_screening_gate": row["adopted_screening_gate"],
                "gate_source": row["gate_source"],
                "why_this_gate": row["why_this_gate"],
                "claim_status": row["claim_status"],
                "source_path": rel(source_path("gates_15")),
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def observable_translation_rows() -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(source_path("translations_15")):
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "observable": row["observable"],
                "mts_parameter": row["mts_parameter"],
                "linear_coefficient": row["linear_coefficient"],
                "adopted_parameter_gate": row["adopted_parameter_gate"],
                "implied_1gate_observable_shift": row["implied_1gate_observable_shift"],
                "observable_unit": row["observable_unit"],
                "interpretation": row["interpretation"],
                "source_path": rel(source_path("translations_15")),
                "valid_for_claim": False,
            }
        )
    return rows


def gates_as_floats() -> dict[str, float]:
    return {row["mts_parameter"]: float(row["adopted_screening_gate"]) for row in read_csv(source_path("gates_15"))}


def coefficients_as_floats() -> dict[str, float]:
    return {
        f"{row['observable']}_vs_{row['mts_parameter']}": float(row["linear_coefficient"])
        for row in read_csv(source_path("translations_15"))
    }


def candidate_inputs() -> list[dict[str, Any]]:
    gates = gates_as_floats()
    return [
        {
            "candidate_id": "RUN2263_0_closure_control",
            "candidate_type": "control_baseline",
            "q_R": 0.0,
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "Q_R": 0.0,
            "has_numeric_values": True,
            "interpretation": "exact closure control; pass is not evidence for MTS",
        },
        {
            "candidate_id": "RUN2263_1_unsigned_lambda_constraint",
            "candidate_type": "theory_target_unsigned",
            "q_R": 0.0,
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "Q_R": 0.0,
            "has_numeric_values": True,
            "interpretation": "would pass if lambda_R parent origin were signed, but it is currently unsigned",
        },
        {
            "candidate_id": "RUN2263_2_MTS_unknown_qR",
            "candidate_type": "actual_MTS_gap_row",
            "q_R": "",
            "delta_beta": "",
            "alpha_clock": "",
            "epsilon_matter": "",
            "Q_R": "",
            "has_numeric_values": False,
            "interpretation": "actual MTS residual row lacks parent value/bound and cannot be scored",
        },
        {
            "candidate_id": "RUN2263_3_qR_at_gate",
            "candidate_type": "edge_case",
            "q_R": gates["q_R"],
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "Q_R": 0.0,
            "has_numeric_values": True,
            "interpretation": "gamma-like leakage exactly at adopted q_R screening gate",
        },
        {
            "candidate_id": "RUN2263_4_qR_ten_times_gate",
            "candidate_type": "fail_probe",
            "q_R": 10.0 * gates["q_R"],
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "Q_R": 0.0,
            "has_numeric_values": True,
            "interpretation": "gamma-like leakage deliberately too large",
        },
        {
            "candidate_id": "RUN2263_5_QR_hair_small_qR",
            "candidate_type": "theory_fail_probe",
            "q_R": 1.0e-6,
            "delta_beta": 0.0,
            "alpha_clock": 0.0,
            "epsilon_matter": 0.0,
            "Q_R": 1.0e-6,
            "has_numeric_values": True,
            "interpretation": "small q_R but nonzero Q_R hair violates closure theory gate",
        },
        {
            "candidate_id": "RUN2263_6_mixed_inside_gates",
            "candidate_type": "candidate_probe",
            "q_R": 1.0e-5,
            "delta_beta": 2.0e-5,
            "alpha_clock": 1.0e-5,
            "epsilon_matter": 1.0e-15,
            "Q_R": 0.0,
            "has_numeric_values": True,
            "interpretation": "small simultaneous leaks inside one-parameter screening gates",
        },
    ]


def qR_candidate_runner_rows() -> list[dict[str, Any]]:
    gates = gates_as_floats()
    rows = []
    for candidate in candidate_inputs():
        if not candidate["has_numeric_values"]:
            verdict = "not_scoreable_missing_parent_values"
            failed = "q_R;delta_beta;alpha_clock;epsilon_matter;Q_R"
            margins = "MISSING_PARENT_VALUE_OR_BOUND"
        else:
            failed_parameters = []
            margins_by_parameter = []
            for parameter in ("q_R", "delta_beta", "alpha_clock", "epsilon_matter", "Q_R"):
                value = float(candidate[parameter])
                gate = gates[parameter]
                if parameter == "Q_R":
                    passed = value == 0.0
                    margin = 0.0 if passed else -abs(value)
                else:
                    passed = abs(value) <= gate
                    margin = gate - abs(value)
                if not passed:
                    failed_parameters.append(parameter)
                margins_by_parameter.append(f"{parameter}:{margin}")
            if not failed_parameters and candidate["candidate_id"] == "RUN2263_0_closure_control":
                verdict = "pass_control_not_signal"
            elif not failed_parameters and candidate["candidate_id"] == "RUN2263_1_unsigned_lambda_constraint":
                verdict = "blocked_unsigned_theory_target"
                failed_parameters.append("lambda_R_parent_origin")
            elif not failed_parameters:
                verdict = "pass_screening_not_claim"
            else:
                verdict = "fail_screening"
            failed = ";".join(failed_parameters)
            margins = ";".join(margins_by_parameter)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "candidate_id": candidate["candidate_id"],
                "candidate_type": candidate["candidate_type"],
                "q_R": candidate["q_R"],
                "delta_beta": candidate["delta_beta"],
                "alpha_clock": candidate["alpha_clock"],
                "epsilon_matter": candidate["epsilon_matter"],
                "reciprocal_charge_Q_R": candidate["Q_R"],
                "verdict": verdict,
                "failed_parameters": failed,
                "margins": margins,
                "interpretation": candidate["interpretation"],
                "score_ready": False,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def qR_candidate_impact_rows() -> list[dict[str, Any]]:
    coefficients = coefficients_as_floats()
    rows = []
    for candidate in candidate_inputs():
        if not candidate["has_numeric_values"]:
            rows.append(
                {
                    "branch_id": BRANCH_ID,
                    "candidate_id": candidate["candidate_id"],
                    "observable": "all_local_observables",
                    "shift": "MISSING_PARENT_VALUE_OR_BOUND",
                    "unit": "mixed",
                    "depends_on": "q_R;delta_beta;alpha_clock;epsilon_matter",
                    "valid_for_claim": False,
                }
            )
            continue
        q_r = float(candidate["q_R"])
        delta_beta = float(candidate["delta_beta"])
        alpha_clock = float(candidate["alpha_clock"])
        epsilon_matter = float(candidate["epsilon_matter"])
        impact_specs = [
            ("solar_light_bending", coefficients["solar_light_bending_vs_q_R"] * q_r, "arcsec", "q_R"),
            ("solar_shapiro", coefficients["solar_shapiro_vs_q_R"] * q_r, "microseconds", "q_R"),
            (
                "mercury_perihelion_combined",
                coefficients["mercury_perihelion_gamma_vs_q_R"] * q_r
                + coefficients["mercury_perihelion_beta_vs_delta_beta"] * delta_beta,
                "arcsec_per_century",
                "q_R;delta_beta",
            ),
            ("gps_gravitational_redshift", coefficients["gps_gravitational_redshift_vs_alpha_clock"] * alpha_clock, "microseconds_per_day", "alpha_clock"),
            ("eotvos_proxy", coefficients["eotvos_proxy_vs_epsilon_matter"] * epsilon_matter, "dimensionless", "epsilon_matter"),
        ]
        for observable, shift, unit, depends_on in impact_specs:
            rows.append(
                {
                    "branch_id": BRANCH_ID,
                    "candidate_id": candidate["candidate_id"],
                    "observable": observable,
                    "shift": shift,
                    "unit": unit,
                    "depends_on": depends_on,
                    "valid_for_claim": False,
                }
            )
    return rows


def refusal_rows() -> list[dict[str, Any]]:
    rows = [
        ("REF2263_0_lambda_origin", "lambda_R parent origin derived", "BLOCKED", "LAM2263_5_verdict=LAMBDA_ORIGIN_NOT_DERIVED_CURRENTLY"),
        ("REF2263_1_constrained_action", "nonpropagating R_AB constraint is parent-signed", "BLOCKED", "CPA2263_7_verdict=NOT_DERIVED_CURRENT_CORPUS"),
        ("REF2263_2_constraint_algebra", "constraint algebra/degree count closes", "BLOCKED", "CAG2263_6_verdict=NOT_CLOSED"),
        ("REF2263_3_QR_zero", "Q_R=0 theorem", "BLOCKED", "current and boundary audits leave Q_R hair unless parent constraint is signed"),
        ("REF2263_4_actual_MTS_score", "actual MTS q_R row can be scored", "BLOCKED", "RUN2263_2_MTS_unknown_qR lacks parent values/bounds"),
        ("REF2263_5_local_GR", "derived local GR/Newton/PPN safety", "BLOCKED", "only closure/control and screening harness pass; no derivation claim"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "refusal_id": refusal_id,
            "attempted_claim": claim,
            "runner_result": result,
            "blocked_by": blocked_by,
            "score_eligible": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for refusal_id, claim, result, blocked_by in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2263_0_lambda_origin", "lambda_R origin from primitives", False, "candidate origins motivate but do not derive the multiplier"),
        ("CG2263_1_parent_constraint", "parent-signed nonpropagating R_AB constraint", False, "contract written but not parent-derived"),
        ("CG2263_2_constraint_algebra", "Dirac/constraint/boundary closure", False, "Hamiltonian, boundary, degree-count and matter gates remain missing"),
        ("CG2263_3_qR_numeric", "actual MTS q_R numeric envelope score", False, "actual q_R/Q_R values remain missing"),
        ("CG2263_4_empirical", "local empirical support for MTS", False, "screening harness is not raw-data likelihood and not evidence"),
        ("CG2263_5_local_GR_Newton", "derived local GR/Newton/PPN recovery", False, "not achieved; closure remains control baseline only"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": claim_id,
            "claim": claim,
            "gate_pass": gate_pass,
            "reason": reason,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for claim_id, claim, gate_pass, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2263_0_derivation",
            "decision": "LAMBDA_ORIGIN_NOT_DERIVED_CURRENTLY",
            "reason": "motion-capacity and radial-cell principles motivate lambda_R R_AB but do not supply parent multiplier origin or constraint algebra",
            "next_action": "do not claim local GR from the constraint",
        },
        {
            "decision_id": "DEC2263_1_contract",
            "decision": "CONSTRAINED_PARENT_ACTION_CONTRACT_WRITTEN",
            "reason": "the exact future contract is now stated: parent variable, multiplier origin, action form, no kinetic R_AB, boundary silence, matter order, no GR import",
            "next_action": "use this as the acceptance gate for any future derivation",
        },
        {
            "decision_id": "DEC2263_2_runner",
            "decision": "QR_ENVELOPE_RUNNER_OPERATIONAL_NONCLAIM",
            "reason": "screening gates and observable translations are wired, with pass/fail controls and MTS unknown row refused",
            "next_action": "fill parent q_R/Q_R values or derive zero before scoring",
        },
        {
            "decision_id": "DEC2263_3_next",
            "decision": "PARENT_CONSTRAINT_ALGEBRA_OR_QR_VALUE_SOURCE_NEXT",
            "reason": "the next useful step is either true constraint algebra construction or first source-backed q_R/Q_R parent value/bound",
            "next_action": "2264-Y5-R2FR-RAB-parent-constraint-algebra-or-first-qR-value-source.md",
        },
    ]
    return [{**{"branch_id": BRANCH_ID}, **row, "valid_for_claim": False, "claim_allowed": False} for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2263_0_primary",
            "next_target": "2264-Y5-R2FR-RAB-parent-constraint-algebra-or-first-qR-value-source.md",
            "script": "scripts/Y5_R2FR_RAB_parent_constraint_algebra_or_first_qR_value_source_2264.py",
            "objective": "try to build the actual parent constraint algebra for lambda_R/R_AB; if it fails, acquire the first source-backed parent q_R or Q_R value/bound row for the local screening runner",
            "selection_status": "selected",
            "success_condition": "constraint algebra gates close without GR import, or q_R/Q_R gets a sourced parent value/bound while still nonclaim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT2263_1_parallel",
            "next_target": "2264b-Y5-R2FR-RAB-raw-local-bound-source-refresh.md",
            "script": "scripts/Y5_R2FR_RAB_raw_local_bound_source_refresh_2264b.py",
            "objective": "refresh local published bound sources and provenance without using them as MTS evidence",
            "selection_status": "held_parallel",
            "success_condition": "local bound ledger sources are current, cited, and separated from MTS coefficient evidence",
            "valid_for_claim": False,
        },
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2263_contract",
            "source_path": rel(OUTPUTS["constraint_contract"]),
            "target_path": rel(COPY_TARGETS["queue_contract"]),
            "target_exists": COPY_TARGETS["queue_contract"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_contract"]) if COPY_TARGETS["queue_contract"].exists() else False,
            "reason": "lambda-origin constrained-parent-action contract nonclaim copy",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2263_qr_runner",
            "source_path": rel(OUTPUTS["qr_candidate_runner"]),
            "target_path": rel(COPY_TARGETS["queue_qr_runner"]),
            "target_exists": COPY_TARGETS["queue_qr_runner"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["queue_qr_runner"]) if COPY_TARGETS["queue_qr_runner"].exists() else False,
            "reason": "q_R/Q_R screening runner nonclaim copy",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2263_branch_wep",
            "source_path": rel(OUTPUTS["claim_gates"]),
            "target_path": rel(COPY_TARGETS["branch_wep"]),
            "target_exists": COPY_TARGETS["branch_wep"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["branch_wep"]) if COPY_TARGETS["branch_wep"].exists() else False,
            "reason": "branch-locked local/WEP refusal gates",
        },
        {
            "branch_id": BRANCH_ID,
            "copy_id": "BC2263_beta_docs",
            "source_path": rel(OUTPUTS["decision"]),
            "target_path": rel(COPY_TARGETS["beta_docs"]),
            "target_exists": COPY_TARGETS["beta_docs"].exists(),
            "target_parses": parse_csv(COPY_TARGETS["beta_docs"]) if COPY_TARGETS["beta_docs"].exists() else False,
            "reason": "portable lambda-origin/q_R-envelope decision ledger",
        },
    ]


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ") for header in headers) + " |")
    return "\n".join(lines)


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    lambda_rows = read_csv(OUTPUTS["lambda_origin_audit"])
    contract_rows = read_csv(OUTPUTS["constraint_contract"])
    algebra_rows = read_csv(OUTPUTS["constraint_algebra_gates"])
    gate_rows = read_csv(OUTPUTS["screening_gates"])
    translation_rows = read_csv(OUTPUTS["observable_translations"])
    runner_rows = read_csv(OUTPUTS["qr_candidate_runner"])
    impact_rows = read_csv(OUTPUTS["qr_candidate_impacts"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    next_rows = read_csv(OUTPUTS["next_target"])
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("VAL2263_0_sources_exist", all(row["exists"].lower() == "true" for row in source_rows), "all cited source paths exist"),
        ("VAL2263_1_needles_present", all(row["needles_present"].lower() == "true" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2263_2_prior_validation",
            any(row["source_key"] == "2262_validation" and row["validation_overall_pass"].lower() == "true" for row in source_rows),
            "2262 validation passes",
        ),
        (
            "VAL2263_3_lambda_not_derived",
            any(row["audit_id"] == "LAM2263_5_verdict" and row["status"] == "LAMBDA_ORIGIN_NOT_DERIVED_CURRENTLY" for row in lambda_rows),
            "lambda origin is not falsely promoted",
        ),
        (
            "VAL2263_4_contract_written",
            any(row["contract_id"] == "CPA2263_7_verdict" and row["current_status"] == "NOT_DERIVED_CURRENT_CORPUS" for row in contract_rows),
            "constrained parent-action contract written and kept unsigned",
        ),
        (
            "VAL2263_5_algebra_not_closed",
            any(row["gate_id"] == "CAG2263_6_verdict" and row["current_status"] == "NOT_CLOSED" for row in algebra_rows),
            "constraint algebra gates remain open",
        ),
        (
            "VAL2263_6_screening_gates_loaded",
            {row["parameter"] for row in gate_rows} >= {"q_R", "delta_beta", "alpha_clock", "epsilon_matter", "Q_R"},
            "local screening gates loaded",
        ),
        (
            "VAL2263_7_translations_loaded",
            any(row["observable"] == "solar_shapiro" and row["mts_parameter"] == "q_R" for row in translation_rows)
            and any(row["observable"] == "mercury_perihelion_beta" for row in translation_rows),
            "observable translation coefficients loaded",
        ),
        (
            "VAL2263_8_runner_controls",
            any(row["candidate_id"] == "RUN2263_0_closure_control" and row["verdict"] == "pass_control_not_signal" for row in runner_rows)
            and any(row["candidate_id"] == "RUN2263_4_qR_ten_times_gate" and row["verdict"] == "fail_screening" for row in runner_rows)
            and any(row["candidate_id"] == "RUN2263_2_MTS_unknown_qR" and row["verdict"] == "not_scoreable_missing_parent_values" for row in runner_rows),
            "q_R runner has pass/fail controls and refuses actual MTS unknown row",
        ),
        (
            "VAL2263_9_impacts_written",
            any(row["candidate_id"] == "RUN2263_3_qR_at_gate" and row["observable"] == "solar_shapiro" for row in impact_rows),
            "observable impacts written",
        ),
        (
            "VAL2263_10_refusal_blocks",
            all(row["claim_allowed"].lower() == "false" and row["score_eligible"].lower() == "false" for row in refusal),
            "refusal runner blocks current claims",
        ),
        (
            "VAL2263_11_claim_gates_blocked",
            all(row["gate_pass"].lower() == "false" and row["valid_for_claim"].lower() == "false" for row in claims),
            "claim gates remain blocked",
        ),
        (
            "VAL2263_12_next_selected",
            any(row["route_id"] == "NEXT2263_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "2264 parent constraint algebra or first q_R source target selected",
        ),
        ("VAL2263_13_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 2263 CSVs parse"),
        (
            "VAL2263_14_no_claim_flags",
            not any(
                row.get(key, "").lower() == "true"
                for path in generated_csvs
                for row in read_csv(path)
                for key in ("score_ready", "accepted_ready", "valid_for_claim", "claim_allowed")
            ),
            "no generated score/claim flags are true",
        ),
        (
            "VAL2263_15_branch_copies",
            all(row["target_exists"].lower() == "true" and row["target_parses"].lower() == "true" for row in read_csv(OUTPUTS["branch_copies"])),
            "branch/queue copies exist and parse",
        ),
        ("VAL2263_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        (
            "VAL2263_17_formalization_no_2263",
            not any(path.is_file() and "2263" in path.name for path in FORMALIZATION.rglob("*")),
            "formalization-workbench has no 2263 output files",
        ),
    ]
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2263_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2263 rejects current lambda-origin derivation, writes the constrained-parent-action contract, wires the q_R/Q_R nonclaim screening runner, and selects 2264",
        }
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv(OUTPUTS["source_register"])
    lambda_rows = read_csv(OUTPUTS["lambda_origin_audit"])
    contract_rows = read_csv(OUTPUTS["constraint_contract"])
    algebra_rows = read_csv(OUTPUTS["constraint_algebra_gates"])
    gate_rows = read_csv(OUTPUTS["screening_gates"])
    translation_rows = read_csv(OUTPUTS["observable_translations"])
    runner_rows = read_csv(OUTPUTS["qr_candidate_runner"])
    impact_rows = read_csv(OUTPUTS["qr_candidate_impacts"])
    refusal = read_csv(OUTPUTS["refusal"])
    claims = read_csv(OUTPUTS["claim_gates"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])
    copies = read_csv(OUTPUTS["branch_copies"])
    validation = read_csv(OUTPUTS["validation"])
    sections = [
        "# 2263 - Y5/R2FR R_AB Constrained Parent Action Lambda Origin Or q_R Envelope Runner",
        "",
        "## Verdict",
        "",
        "2263 tries the derivation route first. The nonpropagating `lambda_R R_AB` constraint is still the cleanest local-GR route because it kills reciprocal hair before it becomes a fifth-force/PPN residual. But the current corpus does **not** derive the parent origin of `lambda_R`.",
        "",
        "So the branch remains nonclaim. The exact constrained-parent-action contract is now written, and the fallback `q_R/Q_R` screening runner is wired to the existing local bounds gates. The runner has controls that pass/fail as expected, but the actual MTS row is refused because no parent `q_R` or `Q_R` value/bound exists yet.",
        "",
        "No local-GR/Newton, PPN, R10, WEP, clock, orbital, `lambda_R`, `R_AB=0`, `Q_R=0`, or empirical support claim is made.",
        "",
        "## Source Register",
        table(["source_id", "source_key", "source_path", "exists", "needles_present", "validation_overall_pass", "role"], source_rows),
        "",
        "## Lambda-Origin Audit",
        table(["audit_id", "candidate_origin", "derives", "does_not_derive", "status", "why_it_fails", "valid_for_claim"], lambda_rows),
        "",
        "## Constrained Parent Action Contract",
        table(["contract_id", "contract_clause", "required_statement", "current_status", "missing_for_claim", "valid_for_claim"], contract_rows),
        "",
        "## Constraint Algebra Gates",
        table(["gate_id", "gate", "required_statement", "current_status", "valid_for_claim"], algebra_rows),
        "",
        "## Local Screening Gates",
        table(["parameter", "adopted_screening_gate", "gate_source", "claim_status", "valid_for_claim"], gate_rows),
        "",
        "## Observable Translations",
        table(["observable", "mts_parameter", "linear_coefficient", "adopted_parameter_gate", "implied_1gate_observable_shift", "observable_unit", "valid_for_claim"], translation_rows),
        "",
        "## q_R Candidate Screening Runner",
        table(["candidate_id", "candidate_type", "q_R", "delta_beta", "alpha_clock", "epsilon_matter", "reciprocal_charge_Q_R", "verdict", "failed_parameters", "score_ready", "valid_for_claim"], runner_rows),
        "",
        "## q_R Candidate Observable Impacts",
        table(["candidate_id", "observable", "shift", "unit", "depends_on", "valid_for_claim"], impact_rows),
        "",
        "## Refusal Runner",
        table(["refusal_id", "attempted_claim", "runner_result", "blocked_by", "score_eligible", "valid_for_claim"], refusal),
        "",
        "## Claim Gates",
        table(["claim_id", "claim", "gate_pass", "reason", "valid_for_claim"], claims),
        "",
        "## Decision Ledger",
        table(["decision_id", "decision", "reason", "next_action", "valid_for_claim"], decisions),
        "",
        "## Next Target",
        table(["route_id", "next_target", "script", "objective", "selection_status", "success_condition"], next_rows),
        "",
        "## Branch Copies",
        table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], copies),
        "",
        "## Validation",
        table(["check_id", "result", "detail"], validation),
        "",
        "## Working Interpretation",
        "",
        "This is a useful narrowing. A derived local-GR lane now requires an actual constrained parent action, not another motivational sentence. If that parent action cannot be built, the honest route is a `q_R/Q_R` residual programme with hard local screens. That is not as glamorous as closing GR, but it is testable and it stops the branch from becoming a smuggled Schwarzschild axiom.",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    for directory in (OUT, QUEUE, MICROSCOPE, BETA_DOCS):
        directory.mkdir(parents=True, exist_ok=True)

    write_csv(OUTPUTS["source_register"], source_register_rows())
    write_csv(OUTPUTS["lambda_origin_audit"], lambda_origin_audit_rows())
    write_csv(OUTPUTS["constraint_contract"], constrained_parent_action_contract_rows())
    write_csv(OUTPUTS["constraint_algebra_gates"], constraint_algebra_gate_rows())
    write_csv(OUTPUTS["screening_gates"], local_screening_gate_rows())
    write_csv(OUTPUTS["observable_translations"], observable_translation_rows())
    write_csv(OUTPUTS["qr_candidate_runner"], qR_candidate_runner_rows())
    write_csv(OUTPUTS["qr_candidate_impacts"], qR_candidate_impact_rows())
    write_csv(OUTPUTS["refusal"], refusal_rows())
    write_csv(OUTPUTS["claim_gates"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next_target"], next_target_rows())

    shutil.copyfile(OUTPUTS["constraint_contract"], COPY_TARGETS["queue_contract"])
    shutil.copyfile(OUTPUTS["qr_candidate_runner"], COPY_TARGETS["queue_qr_runner"])
    shutil.copyfile(OUTPUTS["claim_gates"], COPY_TARGETS["branch_wep"])
    shutil.copyfile(OUTPUTS["decision"], COPY_TARGETS["beta_docs"])
    write_csv(OUTPUTS["branch_copies"], branch_copy_rows())

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    print(f"wrote {DOC}")
    print(f"wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
