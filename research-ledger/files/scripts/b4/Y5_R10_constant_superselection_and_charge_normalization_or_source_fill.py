from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "764-Y5-R10-constant-superselection-and-charge-normalization-or-source-fill.md"
NEXT_TARGET = "765-Y5-R10-parent-vertical-generator-norm-and-Maxwell-kinetic-inheritance-or-alpha-source-fill.md"
STATUS = "Y5_R10_764_constant_superselection_charge_normalization_gate_written_alpha_owner_still_unsigned"
CLAIM_CEILING = "constant_charge_descent_gate_only_no_btheta_zero_no_EM_charge_no_R10_WEP_clock_PPN_Newton_or_local_GR_pass"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

CONSTANT_SUPERSELECTION_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_764_CONSTANT_SUPERSELECTION_INPUT_CANDIDATE.csv"
CHARGE_NORMALIZATION_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_764_CHARGE_NORMALIZATION_INPUT_CANDIDATE.csv"
ALPHA_OWNER_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_764_ALPHA_OWNER_INPUT_CANDIDATE.csv"
MASS_CLOCK_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_764_MASS_CLOCK_RATIO_INPUT_CANDIDATE.csv"
ARENA_TAU_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_764_ARENA_TAU_INPUT_CANDIDATE.csv"
EM_INTERFACE_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_759_EM_CHARGE_INTERFACE_INPUT_CANDIDATE.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_764_SOURCE_REGISTER.csv"
CONSTANT_THEOREM_PATH = RESIDUALS / "P8_Y5_R10_764_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv"
CHARGE_GATE_PATH = RESIDUALS / "P8_Y5_R10_764_CHARGE_NORMALIZATION_DESCENT_GATE.csv"
ALPHA_OWNER_PATH = RESIDUALS / "P8_Y5_R10_764_ALPHA_EM_OWNER_AUDIT.csv"
BTHETA_UPDATE_PATH = RESIDUALS / "P8_Y5_R10_764_BTHETA_RESIDUAL_UPDATE.csv"
SOURCE_FILL_PATH = RESIDUALS / "P8_Y5_R10_764_SOURCE_FILL_SCHEMA.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_R10_764_DECISION_MATRIX.csv"
ROUTE_PATH = RESIDUALS / "P8_Y5_R10_764_ROUTE_UPDATE.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_764_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_764_VALIDATION.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "763_doc": {
        "path": POST_CHECKPOINT / "763-Y5-R10-no-marker-spurion-theorem-or-coupling-source-fill.md",
        "needles": [
            "Current result: **the no-marker/no-spurion theorem is only a classification theorem shape, not a parent-signed theorem**",
            "764-Y5-R10-constant-superselection-and-charge-normalization-or-source-fill.md",
        ],
        "role": "immediate constant/charge handoff",
    },
    "763_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_763_VALIDATION.csv",
        "needles": ["V763_15_validation_rows_ready", "V763_13_formalization_workbench_untouched"],
        "role": "prior validation guard",
    },
    "763_theorem_attempt": {
        "path": RESIDUALS / "P8_Y5_R10_763_NO_MARKER_SPURION_THEOREM_ATTEMPT.csv",
        "needles": ["NMS763_2_constant_superselection", "NMS763_6_verdict"],
        "role": "constant superselection open channel",
    },
    "638_constant_beta": {
        "path": POST_CHECKPOINT / "638-Y5-R10-constant-sector-zero-or-finite-beta-derivation.md",
        "needles": ["ZR638_1_alpha_EM", "DG638_1_dimensionless_observable_rule"],
        "role": "dimensionless-constant rule and finite beta fallback",
    },
    "642_charge_Maxwell": {
        "path": POST_CHECKPOINT / "642-Y5-R10-charge-unit-Maxwell-proof-extension-or-kappa-alpha-pressure-runner.md",
        "needles": ["TA642_4_coupling_normalization", "MD642_4_alpha_constant"],
        "role": "compact U1 partial result and alpha blocker",
    },
    "643_alpha_owner": {
        "path": POST_CHECKPOINT / "643-Y5-R10-alpha-normalization-owner-or-finite-coupling-bound-input-fill.md",
        "needles": ["AO643_5_parent_vertical_norm", "PVC643_6_vertical_alpha_silence"],
        "role": "best alpha-owner route",
    },
    "637_constant_ownership": {
        "path": POST_CHECKPOINT / "637-Y5-R10-parent-action-quotient-map-and-constant-ownership-derivation.md",
        "needles": ["CO637_0_descent_criterion", "CS637_1_em_charge_alpha"],
        "role": "constant descent criterion",
    },
    "640_charge_topology": {
        "path": POST_CHECKPOINT / "640-Y5-R10-charge-topology-or-kappa-alpha-numeric-prior.md",
        "needles": ["CTL640_3_gauge_kinetic_normalization", "KA640_2_finite_branch"],
        "role": "charge topology ladder and finite kappa_alpha fallback",
    },
    "459B_phase_current": {
        "path": POST_CHECKPOINT / "459B-Andersen-charge-amplitude-phase-current-gate.md",
        "needles": ["PC2_quantized_charge_unit", "PC4_Maxwell_limit"],
        "role": "external clue audit, not proof",
    },
    "762_charge_leak": {
        "path": RESIDUALS / "P8_Y5_R10_762_GEOMETRY_STACK_COUNTEREXAMPLE_LEDGER.csv",
        "needles": ["GCE762_3_charge_normalization_derivative", "fine-structure/charge residual survives"],
        "role": "charge derivative leak counterexample",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def text_contains(path: Path, needles: list[str]) -> bool:
    text = read_text(path)
    return bool(text) and all(needle in text for needle in needles)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and datetime.fromtimestamp(path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            count += 1
    return count


def make_source_register(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(spec["path"]),
            "exists": bool_string(Path(spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(spec["path"]), spec["needles"])),
            "role": spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, spec in SOURCES.items()
    ]


def constant_theorem_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CST764_0_descent_criterion",
            "statement": "A matter constant is locally silent exactly when it is fixed representation data or a quotient-owned function.",
            "mathematical_form": "If theta_i(Phi)=theta_bar_i(q(Phi)) or theta_i in Rep_i with trivial vertical action, then Lie_v theta_i=0 for every v in ker(Dq).",
            "derivation_status": "math_pass_conditional",
            "blocker": "the parent action has not classified every ordinary-sector theta_i",
            "observable_risk": "none if signed; otherwise b_theta",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CST764_1_dimensionless_rule",
            "statement": "Dimensionless constants cannot be hidden by unit convention.",
            "mathematical_form": "Lie_v ln C_i != 0 for C_i in {alpha_EM, mass ratios, binding fractions, clock ratios} is physical unless C_i descends/topological.",
            "derivation_status": "guardrail_pass",
            "blocker": "alpha_EM and mass/clock ratio ownership remains unsigned",
            "observable_risk": "clock, WEP, EM spectra, R10 composition, source/test charge",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CST764_2_unit_rescaling_exception",
            "statement": "Universal dimensionful rescaling is locally silent only when all dimensionless observables are unchanged.",
            "mathematical_form": "delta_v ln m_A = sigma for all masses can be readout/unit-only only if delta_v ln(m_A/m_B)=delta_v ln alpha_EM=delta_v ln nu_i/nu_j=0.",
            "derivation_status": "conditional_unit_guard",
            "blocker": "body composition and clock readout must be reduced to dimensionless ratios",
            "observable_risk": "false constant-zero if used on raw dimensionful masses",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CST764_3_discrete_label_escape",
            "statement": "Integer representation labels are smooth-vertical silent, but they do not fix continuous coupling strength.",
            "mathematical_form": "n_A in Z implies Lie_v n_A=0; alpha_EM still depends on the kinetic/coupling normalization g_EM.",
            "derivation_status": "partial_conditional_success",
            "blocker": "compact U1 charge labels do not own g_EM or the Maxwell kinetic coefficient",
            "observable_risk": "charge ratios may be safe while alpha strength remains open",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "theorem_id": "CST764_4_verdict",
            "statement": "Constant superselection is a clean sufficient route but not parent-signed for the current MTS local branch.",
            "mathematical_form": "b_theta=0 only after every dimensionless ordinary constant is quotient/topological/representation-owned or retained with a bound.",
            "derivation_status": "not_parent_signed",
            "blocker": "alpha_EM, charge normalization, mass ratios, clock ratios, and material preparation remain open",
            "observable_risk": "b_theta remains a live residual channel",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def charge_gate_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CNG764_0_U1_bundle_connection",
            "required_clause": "Observed EM is a parent-owned compact U1 connection that descends through q.",
            "mathematical_form": "A_Q(Phi)=q^* Abar_Q + dchi; F_Q=dA_Q=q^*Fbar_Q",
            "if_signed": "Bianchi/no-monopole half and gauge-representative silence are structurally available",
            "current_status": "partial_template_not_parent_signed",
            "failure_mode": "A_Q can be only analogy or can contain representative X-dependent pieces",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CNG764_1_integer_charge_representations",
            "required_clause": "Matter charges are integer representation weights of the same U1 fibre.",
            "mathematical_form": "D_A=d+i n_A A_Q + spin; n_A in Z and Lie_v n_A=0",
            "if_signed": "relative charge labels are locally vertical-silent",
            "current_status": "conditional_partial_success",
            "failure_mode": "does not fix Q_star/e or alpha_EM strength",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CNG764_2_Maxwell_kinetic_owner",
            "required_clause": "The Maxwell kinetic coefficient is inherited from the parent geometry, level, index, or fixed vertical-generator norm.",
            "mathematical_form": "S_EM=-1/(4 g_EM^2) int F_Q wedge *F_Q with Lie_v g_EM=0 and no independent f_X(Phi)F^2",
            "if_signed": "Gauss/Ampere normalization and alpha strength stop being free local couplings",
            "current_status": "not_parent_signed_hard_blocker",
            "failure_mode": "compactness leaves g_EM continuously rescalable",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CNG764_3_current_normalization",
            "required_clause": "The matter current and Maxwell source are normalized by the same parent object.",
            "mathematical_form": "d*F_Q=g_EM^2 *J_Q with J_Q from the same Noether/Ward current that supplies n_A A_Q coupling",
            "if_signed": "charge/current equality and Lorentz readout share one owner",
            "current_status": "not_parent_signed",
            "failure_mode": "q_A(X)A_mu J_A^mu or species current weights reopen b_theta/b_kappa",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CNG764_4_readout_constants",
            "required_clause": "hbar, c, clock readout, and coframe Hodge star are quotient-owned or pure readout convention.",
            "mathematical_form": "Lie_v ln(hbar c)=0 for dimensionless alpha_EM readout, and * is the observed descended coframe Hodge star",
            "if_signed": "alpha readout is not contaminated by clock/ruler convention",
            "current_status": "not_parent_signed",
            "failure_mode": "spectroscopy/clock ratios become direct b_theta probes",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "gate_id": "CNG764_5_alpha_derivative_identity",
            "required_clause": "Alpha silence follows only from the previous clauses.",
            "mathematical_form": "Lie_v ln alpha_EM = Lie_v ln(g_EM^2) - Lie_v ln(4 pi hbar c); this is zero only if the kinetic norm and readout constants are vertical-silent.",
            "if_signed": "kappa_alpha=0 is theorem-zero",
            "current_status": "identity_pass_zero_not_proved",
            "failure_mode": "finite kappa_alpha=d ln alpha_EM/dXhat must be retained",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def alpha_owner_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "owner_id": "AEO764_0_plain_U1_compactness",
            "candidate_owner": "compact U1 fibre alone",
            "what_it_owns": "integer charge labels and curvature form",
            "what_it_does_not_own": "continuous Maxwell kinetic coefficient g_EM or alpha_EM value",
            "status": "support_only_not_sufficient",
            "next_requirement": "tie kinetic coefficient to parent norm/level/index",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "AEO764_1_topological_level_or_index",
            "candidate_owner": "BF/Chern-Simons/anomaly/index/monopole-style level",
            "what_it_owns": "possibly charge unit or response level",
            "what_it_does_not_own": "4D low-energy Maxwell kinetic term unless the bulk coefficient inherits the level",
            "status": "possible_but_not_present_as_parent_theorem",
            "next_requirement": "show observed EM kinetic normalization is fixed by the level, not added after readout",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "AEO764_2_parent_vertical_generator_norm",
            "candidate_owner": "fixed parent vertical generator norm and kinetic subblock inheritance",
            "what_it_owns": "same object could own charge unit, A_Q normalization, F^2 coefficient, and current coupling",
            "what_it_does_not_own": "nothing unless no independent lambda_A F^2 or generator rescaling remains legal",
            "status": "best_route_not_proved",
            "next_requirement": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "AEO764_3_KK_radius_or_modulus",
            "candidate_owner": "compactification radius/volume/modulus",
            "what_it_owns": "g_EM if the radius is fixed and quotient-silent",
            "what_it_does_not_own": "local silence if the modulus can vary with Xhat",
            "status": "dangerous_open_route",
            "next_requirement": "derive modulus silence or retain kappa_alpha",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "owner_id": "AEO764_4_finite_alpha_residual",
            "candidate_owner": "no owner; empirical finite residual",
            "what_it_owns": "honest nonclaim testing corridor",
            "what_it_does_not_own": "derivation or local-GR reduction",
            "status": "fallback_if_owner_fails",
            "next_requirement": "Xhat unit, tau maps, material sensitivities, and bounds",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def btheta_update_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "BTU764_0_alpha_EM",
            "object": "alpha_EM",
            "zero_condition": "parent-owned quotient/topological/fixed kinetic normalization plus vertical-silent readout constants",
            "current_status": "open",
            "finite_if_fail": "kappa_alpha=d ln alpha_EM/dXhat",
            "test_arenas": "clocks;EM_spectra;WEP;R10_material_EM_binding",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "BTU764_1_charge_unit",
            "object": "q_A/e or n_A Q_star",
            "zero_condition": "integer representation labels plus fixed Q_star from the same parent owner as A_Q",
            "current_status": "partly_open",
            "finite_if_fail": "d ln q_A/dXhat or charge-current normalization residual",
            "test_arenas": "EM;WEP;source-test charge;clock/spectra",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "BTU764_2_mass_ratios",
            "object": "m_A/m_B, Yukawa/binding ratios",
            "zero_condition": "fixed representation/spectrum data or quotient-owned mass spectrum",
            "current_status": "open",
            "finite_if_fail": "kappa_mi=d ln ratio_i/dXhat and body beta_A",
            "test_arenas": "WEP;clocks;orbital source normalization;R10 composition",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "BTU764_3_clock_ratios",
            "object": "nu_i/nu_j",
            "zero_condition": "inherits alpha_EM, mass-ratio, and nuclear/binding zero conditions",
            "current_status": "open",
            "finite_if_fail": "kappa_clock_i=d ln nu_i/dXhat",
            "test_arenas": "atomic clocks;redshift;time branch",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "residual_id": "BTU764_4_btheta_vector",
            "object": "b_theta",
            "zero_condition": "all dimensionless constant/charge/mass/clock residuals theorem-zero or arena-projected below bounds",
            "current_status": "retained_residual_channel",
            "finite_if_fail": "b_theta=(kappa_alpha,kappa_mass,kappa_clock,kappa_charge,...) projected by arena sensitivity matrices",
            "test_arenas": "R10;WEP;clocks;EM;PPN only through separate operator map",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def source_fill_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "SFS764_0_constant_superselection_certificate",
            "artifact": str(CONSTANT_SUPERSELECTION_CANDIDATE_PATH),
            "required_columns": "constant_id;dimensionless_or_dimensionful;owner_type;vertical_derivative;source_path;valid_for_claim",
            "claim_gate": "every ordinary dimensionless constant is quotient/topological/representation-owned or retained",
            "current_status": f"schema_only_candidate_missing={bool_string(not CONSTANT_SUPERSELECTION_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS764_1_charge_normalization_certificate",
            "artifact": str(CHARGE_NORMALIZATION_CANDIDATE_PATH),
            "required_columns": "charge_object;bundle_owner;integer_label_status;Qstar_owner;current_normalization;source_path;valid_for_claim",
            "claim_gate": "charge labels, base unit, and current normalization share one parent owner",
            "current_status": f"schema_only_candidate_missing={bool_string(not CHARGE_NORMALIZATION_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS764_2_alpha_owner_certificate",
            "artifact": str(ALPHA_OWNER_CANDIDATE_PATH),
            "required_columns": "owner_candidate;gEM_status;F2_coefficient_status;readout_status;no_independent_rescale;source_path;valid_for_claim",
            "claim_gate": "alpha_EM is fixed by parent norm/level/index/readout and no f_X F2 term is legal",
            "current_status": f"schema_only_candidate_missing={bool_string(not ALPHA_OWNER_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS764_3_mass_clock_ratio_certificate",
            "artifact": str(MASS_CLOCK_CANDIDATE_PATH),
            "required_columns": "ratio_id;sector;owner_type;vertical_derivative;sensitivity_coefficients;source_path;valid_for_claim",
            "claim_gate": "mass and clock ratios are fixed/quotient-owned or supplied as finite sensitivities",
            "current_status": f"schema_only_candidate_missing={bool_string(not MASS_CLOCK_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS764_4_arena_tau_sensitivity_map",
            "artifact": str(ARENA_TAU_CANDIDATE_PATH),
            "required_columns": "arena;residual_component;tau_factor;sensitivity_vector;bound_source_path;valid_for_claim",
            "claim_gate": "finite b_theta components have arena projections and sourced bounds",
            "current_status": f"schema_only_candidate_missing={bool_string(not ARENA_TAU_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "fill_id": "SFS764_5_EM_charge_interface",
            "artifact": str(EM_INTERFACE_CANDIDATE_PATH),
            "required_columns": "sector;charge_current_owner;metric_or_coframe_used;normalization;alpha_or_charge_response;source_path;valid_for_claim",
            "claim_gate": "charge/current derivative operator descends or b_theta is bounded",
            "current_status": f"schema_only_candidate_missing={bool_string(not EM_INTERFACE_CANDIDATE_PATH.exists())}",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D764_0_constant_gate",
            "decision": "accept the constant descent criterion as conditional math",
            "reason": "Lie_v theta_i vanishes if theta_i is quotient-owned or fixed representation data",
            "claim_status": "conditional_only_not_parent_signed",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D764_1_alpha_owner",
            "decision": "do not claim alpha_EM or charge normalization silence",
            "reason": "compact U1 gives integer labels but not the continuous Maxwell kinetic coefficient",
            "claim_status": "not_promoted",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D764_2_next",
            "decision": "hunt the parent vertical-generator norm and Maxwell kinetic inheritance next",
            "reason": "this is the cleanest route to make charge unit, A_Q normalization, F2 coefficient, and current normalization one object",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def route_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "route_id": "RU764_0_allowed",
            "allowed_after_764": "use the constant descent criterion as a theorem template",
            "forbidden_after_764": "treat alpha_EM or mass ratios as silent without parent classification",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU764_1_allowed",
            "allowed_after_764": "claim compact U1 only as partial charge-label support",
            "forbidden_after_764": "infer the value or vertical silence of g_EM/alpha_EM from compactness alone",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "route_id": "RU764_2_allowed",
            "allowed_after_764": "retain finite b_theta source rows if the parent owner fails",
            "forbidden_after_764": "hide dimensionless constant variation in unit convention",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "constant/charge descent gate is exact enough, but alpha_EM owner is not signed",
            "hard_blocker": "continuous Maxwell kinetic normalization g_EM and charge-current normalization are not parent-owned",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def validate(
    sources: list[dict[str, Any]],
    constants: list[dict[str, Any]],
    charge_gate: list[dict[str, Any]],
    alpha_owner: list[dict[str, Any]],
    btheta: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    validation: list[dict[str, str]] = []
    validation.append({"check_id": "V764_0_source_paths_exist", "result": "pass" if all(row["exists"] == "true" for row in sources) else "fail", "detail": f"source_rows={len(sources)}"})
    validation.append({"check_id": "V764_1_source_needles_present", "result": "pass" if all(row["needle_check"] == "true" for row in sources) else "fail", "detail": "all local source needles present"})
    prior_763 = read_csv_rows(RESIDUALS / "P8_Y5_BRR545_763_VALIDATION.csv")
    validation.append({"check_id": "V764_2_prior_763_clean", "result": "pass" if prior_763 and all(row.get("result") == "pass" for row in prior_763) else "fail", "detail": "763 validation has no failures"})
    validation.append({"check_id": "V764_3_constant_theorem_written", "result": "pass" if len(constants) == 5 and any(row["theorem_id"] == "CST764_4_verdict" for row in constants) else "fail", "detail": "constant theorem rows present"})
    validation.append({"check_id": "V764_4_constant_not_parent_signed", "result": "pass" if any(row["theorem_id"] == "CST764_4_verdict" and row["derivation_status"] == "not_parent_signed" for row in constants) else "fail", "detail": "constant superselection remains nonclaim"})
    validation.append({"check_id": "V764_5_charge_gate_has_alpha_identity", "result": "pass" if any(row["gate_id"] == "CNG764_5_alpha_derivative_identity" and row["current_status"] == "identity_pass_zero_not_proved" for row in charge_gate) else "fail", "detail": "alpha derivative identity written without zero promotion"})
    validation.append({"check_id": "V764_6_alpha_owner_best_route_selected", "result": "pass" if any(row["owner_id"] == "AEO764_2_parent_vertical_generator_norm" and row["status"] == "best_route_not_proved" for row in alpha_owner) else "fail", "detail": "parent vertical-generator norm route selected"})
    expected_residuals = {"BTU764_0_alpha_EM", "BTU764_1_charge_unit", "BTU764_2_mass_ratios", "BTU764_3_clock_ratios", "BTU764_4_btheta_vector"}
    validation.append({"check_id": "V764_7_btheta_components_retained", "result": "pass" if {row["residual_id"] for row in btheta} == expected_residuals and all(row["valid_for_claim"] == "false" for row in btheta) else "fail", "detail": "b_theta components remain residuals"})
    validation.append({"check_id": "V764_8_source_fill_schema_written", "result": "pass" if len(source_fill) == 6 and all(row["valid_for_claim"] == "false" for row in source_fill) else "fail", "detail": "source-fill rows schema-only"})
    candidate_paths = [CONSTANT_SUPERSELECTION_CANDIDATE_PATH, CHARGE_NORMALIZATION_CANDIDATE_PATH, ALPHA_OWNER_CANDIDATE_PATH, MASS_CLOCK_CANDIDATE_PATH, ARENA_TAU_CANDIDATE_PATH, EM_INTERFACE_CANDIDATE_PATH]
    validation.append({"check_id": "V764_9_candidate_artifacts_not_faked", "result": "pass" if not any(path.exists() for path in candidate_paths) else "fail", "detail": "no claim-input artifacts fabricated"})
    all_generated = constants + charge_gate + alpha_owner + btheta + source_fill + decisions + routes + summary
    validation.append({"check_id": "V764_10_no_claim_rows_promoted", "result": "pass" if all(row.get("valid_for_claim") == "false" for row in all_generated) else "fail", "detail": "all generated rows valid_for_claim=false"})
    validation.append({"check_id": "V764_11_no_local_arena_claim", "result": "pass" if "no_EM_charge_no_R10_WEP_clock_PPN_Newton_or_local_GR_pass" in CLAIM_CEILING else "fail", "detail": "local/EM claims remain blocked"})
    validation.append({"check_id": "V764_12_next_target_selected", "result": "pass" if all(row.get("next_action") == NEXT_TARGET for row in routes) and all(row.get("next_target") == NEXT_TARGET for row in decisions) and summary[0].get("next_target") == NEXT_TARGET else "fail", "detail": NEXT_TARGET})
    output_paths = [
        Path(__file__),
        OUTPUT_DOC,
        SOURCE_REGISTER_PATH,
        CONSTANT_THEOREM_PATH,
        CHARGE_GATE_PATH,
        ALPHA_OWNER_PATH,
        BTHETA_UPDATE_PATH,
        SOURCE_FILL_PATH,
        DECISION_PATH,
        ROUTE_PATH,
        SUMMARY_PATH,
        VALIDATION_PATH,
    ]
    validation.append({"check_id": "V764_13_outputs_scoped", "result": "pass" if all(under_post(path) for path in output_paths) else "fail", "detail": "all outputs under post-checkpoint-work"})
    fw_count = formalization_changed_after_cutoff()
    validation.append({"check_id": "V764_14_formalization_workbench_untouched", "result": "pass" if fw_count == 0 else "fail", "detail": f"formalization_changed_after_cutoff={fw_count}"})
    validation.append({"check_id": "V764_15_validation_rows_ready", "result": "pass", "detail": "validation table constructed"})
    return validation


def build_doc(
    sources: list[dict[str, Any]],
    constants: list[dict[str, Any]],
    charge_gate: list[dict[str, Any]],
    alpha_owner: list[dict[str, Any]],
    btheta: list[dict[str, Any]],
    source_fill: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 764 - Y5 R10 Constant Superselection And Charge Normalization Or Source Fill

Start point: 763 made the hidden-spurion problem explicit. The sharpest concrete leak is `b_theta`: `theta_A`, `alpha_EM`, charge normalization, mass ratios, and clock ratios can still vary through the matter derivative operator even if the geometry stack descends.

Current result: **the constant/charge descent gate is now exact enough to use, but it does not close**. A constant is silent only if it is fixed representation data, quotient-owned, topological/discrete, or retained as a residual. Compact `U(1)` helps with integer charge labels, but it does not by itself fix the continuous Maxwell kinetic coefficient `g_EM` or the fine-structure strength `alpha_EM`.

## Summary

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target"])}

## Constant Superselection Theorem Attempt

{markdown_table(constants, ["theorem_id", "statement", "mathematical_form", "derivation_status", "blocker", "observable_risk", "valid_for_claim"])}

## Charge-Normalization Descent Gate

{markdown_table(charge_gate, ["gate_id", "required_clause", "mathematical_form", "if_signed", "current_status", "failure_mode", "valid_for_claim"])}

## Alpha-EM Owner Audit

{markdown_table(alpha_owner, ["owner_id", "candidate_owner", "what_it_owns", "what_it_does_not_own", "status", "next_requirement", "valid_for_claim"])}

## b_theta Residual Update

{markdown_table(btheta, ["residual_id", "object", "zero_condition", "current_status", "finite_if_fail", "test_arenas", "valid_for_claim"])}

## Source-Fill Schema

{markdown_table(source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Route Update

{markdown_table(routes, ["route_id", "allowed_after_764", "forbidden_after_764", "next_action", "valid_for_claim"])}

## Local Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Plain-English Verdict

This gets the coupling problem into the right language. Integer charge labels are not enough; the thing that must be owned is the normalization of the EM kinetic/current system. The next best shot is to prove that the observed EM connection is literally a parent vertical-generator subblock with a fixed norm, so `A_Q`, `F^2`, current normalization, and charge unit are one object rather than four knobs. If that fails, `kappa_alpha` stays as a finite residual and we source/bound it honestly.
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = make_source_register(generated_utc)
    constants = constant_theorem_rows(generated_utc)
    charge_gate = charge_gate_rows(generated_utc)
    alpha_owner = alpha_owner_rows(generated_utc)
    btheta = btheta_update_rows(generated_utc)
    source_fill = source_fill_rows(generated_utc)
    decisions = decision_rows(generated_utc)
    routes = route_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validate(sources, constants, charge_gate, alpha_owner, btheta, source_fill, decisions, routes, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(CONSTANT_THEOREM_PATH, constants, ["theorem_id", "statement", "mathematical_form", "derivation_status", "blocker", "observable_risk", "valid_for_claim", "generated_utc"])
    write_csv(CHARGE_GATE_PATH, charge_gate, ["gate_id", "required_clause", "mathematical_form", "if_signed", "current_status", "failure_mode", "valid_for_claim", "generated_utc"])
    write_csv(ALPHA_OWNER_PATH, alpha_owner, ["owner_id", "candidate_owner", "what_it_owns", "what_it_does_not_own", "status", "next_requirement", "valid_for_claim", "generated_utc"])
    write_csv(BTHETA_UPDATE_PATH, btheta, ["residual_id", "object", "zero_condition", "current_status", "finite_if_fail", "test_arenas", "valid_for_claim", "generated_utc"])
    write_csv(SOURCE_FILL_PATH, source_fill, ["fill_id", "artifact", "required_columns", "claim_gate", "current_status", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(ROUTE_PATH, routes, ["route_id", "allowed_after_764", "forbidden_after_764", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, constants, charge_gate, alpha_owner, btheta, source_fill, decisions, routes, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        print(f"wrote {OUTPUT_DOC}")
        print(f"wrote {VALIDATION_PATH}")
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)
    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")


if __name__ == "__main__":
    main()
