from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3883"
BRANCH = "MTS_R2FR_Y5_HILBERT_SOURCE_AND_MAXWELL_STRESS_LOCK_3883"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3883-Y5-R2FR-Hilbert-source-and-Maxwell-stress-lock-or-residual-vector.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3882_NEXT = OUT / "P8_Y5_R2FR_3882_NEXT_TARGET.csv"
CSV_3882_EL = OUT / "P8_Y5_R2FR_3882_EULER_LAGRANGE_BIANCHI_CHAIN.csv"
CSV_3882_REDUCTION = OUT / "P8_Y5_R2FR_3882_LOCAL_NEWTON_GR_REDUCTION_MAP.csv"
CSV_3882_VALIDATION = OUT / "P8_Y5_BRR545_3882_VALIDATION.csv"
CSV_SOURCE_STACK = OUT / "P8_source_normalized_Newton_branch_STACK.csv"
CSV_OWNER = OUT / "P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv"
CSV_PG = OUT / "P8_PG_calibration_residual_MAP.csv"
CSV_PG_TEMPLATE = OUT / "P8_PG_calibration_residual_INPUT_TEMPLATE.csv"
CSV_HILBERT_MONOPOLE = OUT / "P8_Hilbert_monopole_calibration_CONTRACT.csv"
CSV_HAMILTONIAN_CHARGE = OUT / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"
CSV_CHARGE_CURRENT_DIRECT = OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv"
CSV_CHARGE_CURRENT_RESIDUAL = OUT / "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv"
CSV_HILBERT_DIV = OUT / "P8_Y5_HILBERT_CURRENT_2467_DIVERGENCE_IDENTITY.csv"
CSV_HILBERT_EXCHANGE = OUT / "P8_Y5_HILBERT_CURRENT_2467_EXCHANGE_CURRENT_IDENTITY.csv"
CSV_HWT_ATTEMPT = OUT / "P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv"
CSV_HWT_CONTRACT = OUT / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv"
CSV_MIN_MATTER = OUT / "P8_Y5_MIN_PARENT_MATTER_2587_ACTION_CONTRACT.csv"
CSV_MIN_MATTER_GATE = OUT / "P8_Y5_MIN_PARENT_MATTER_2587_ADOPTION_GATE.csv"
CSV_MATTER_DESCENT = OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_MATTER_WORLDTUBE_DESCENT_ATTEMPT.csv"
CSV_DIRECT_GRAMMAR = OUT / "P8_Y5_DIRECT_MATTER_GRAMMAR_GATE_2612_NO_DIRECT_MATTER_X_VERTEX_GRAMMAR_ATTEMPT.csv"
CSV_MATTER_OWNER = OUT / "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_OWNER_THEOREM_ATTEMPT.csv"
CSV_EM_BOUND = OUT / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"
CSV_EM_POYNTING = OUT / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"
CSV_EM_ACCOUNTING = OUT / "P8_Y5_EM_Poynting_Hilbert_source_accounting_status.csv"
CSV_EM_FLUX_STATUS = OUT / "P8_Y5_I_matter_EM_flux_status.csv"
CSV_EM_JQ_STATUS = OUT / "P8_Y5_Jq_matter_EM_Poynting_subcomponent_status.csv"
CSV_EM_CURRENT = OUT / "P8_EM_current_source_Ward_alpha_source_residual.csv"
CSV_EM_HODGE = OUT / "P8_EM_Hodge_flow_rule_bound_or_zero.csv"
CSV_FRAME = OUT / "P8_frame_source_split_residual_or_zero.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3883_SOURCE_REGISTER.csv",
    "source_lock": OUT / "P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv",
    "maxwell": OUT / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv",
    "residuals": OUT / "P8_Y5_R2FR_3883_MATTER_EM_RESIDUAL_VECTOR.csv",
    "newton": OUT / "P8_Y5_R2FR_3883_NEWTON_SOURCE_DENSITY_BRIDGE.csv",
    "runner": OUT / "P8_Y5_R2FR_3883_RUNNER_UPDATE.csv",
    "gates": OUT / "P8_Y5_R2FR_3883_CLAIM_GATES.csv",
    "next": OUT / "P8_Y5_R2FR_3883_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3883_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3883_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3883_00_next", CSV_3882_NEXT, "NEXT3882_0", "3882 selected Hilbert/Maxwell target"),
    ("SRC3883_01_metric", CSV_3882_EL, "EL3882_2_metric", "constant-branch metric equation"),
    ("SRC3883_02_bianchi", CSV_3882_EL, "EL3882_3_Bianchi", "Bianchi identity"),
    ("SRC3883_03_source_scope", CSV_3882_REDUCTION, "RED3882_4_source_scope", "source/Hilbert open gate"),
    ("SRC3883_04_em_scope", CSV_3882_REDUCTION, "RED3882_5_EM_scope", "Maxwell stress next gate"),
    ("SRC3883_05_3882_valid", CSV_3882_VALIDATION, "VAL3882_17_next_target", "3882 validation"),
    ("SRC3883_06_SN3", CSV_SOURCE_STACK, "SN3_charge_equals_Hilbert_mass_current", "Hilbert mass current rung"),
    ("SRC3883_07_SN5", CSV_SOURCE_STACK, "SN5_EH_to_Poisson_coefficient", "EH-to-Poisson source rung"),
    ("SRC3883_08_SN8", CSV_SOURCE_STACK, "SN8_Gauss_surface_integral", "Gauss source rung"),
    ("SRC3883_09_SN10", CSV_SOURCE_STACK, "SN10_no_derivative_hair", "source derivative hair rung"),
    ("SRC3883_10_Y5O1", CSV_OWNER, "Y5O_1_same_observed_coframe", "same observed coframe owner"),
    ("SRC3883_11_Y5O3", CSV_OWNER, "Y5O_3_parent_source_charge", "parent source charge owner"),
    ("SRC3883_12_Y5O5", CSV_OWNER, "Y5O_5_no_extra_mass_projection", "no extra mass projection"),
    ("SRC3883_13_PG1", CSV_PG, "PG1_charge_equals_projected_Hilbert_source", "charge-current split"),
    ("SRC3883_14_PG3", CSV_PG, "PG3_EH_to_Poisson_coefficient", "operator/source residual"),
    ("SRC3883_15_PG6", CSV_PG, "PG6_zero_mu_extra_and_source_residuals", "mu_extra source residual"),
    ("SRC3883_16_PG8", CSV_PG, "PG8_no_derivative_hair", "derivative hair"),
    ("SRC3883_17_template_boundary", CSV_PG_TEMPLATE, "P8_boundary_bulk_domain_mu_extra", "mu_extra template"),
    ("SRC3883_18_HM0", CSV_HILBERT_MONOPOLE, "HM0_Hilbert_current_input", "Hilbert current input"),
    ("SRC3883_19_HM2", CSV_HILBERT_MONOPOLE, "HM2_mass_flux_closure", "mass flux closure"),
    ("SRC3883_20_HM5", CSV_HILBERT_MONOPOLE, "HM5_zero_mu_extra", "zero extra mass"),
    ("SRC3883_21_HC4", CSV_HAMILTONIAN_CHARGE, "HC4_charge_equals_PiM_Hilbert_mass", "Hamiltonian-to-Hilbert mass"),
    ("SRC3883_22_HC8", CSV_HAMILTONIAN_CHARGE, "HC8_Poisson_Gauss_orbital_calibration", "Gauss/orbital calibration"),
    ("SRC3883_23_CC2", CSV_CHARGE_CURRENT_DIRECT, "CC2_EH_constraint_source_link", "EH source link"),
    ("SRC3883_24_CC7", CSV_CHARGE_CURRENT_DIRECT, "CC7_closed_flux_and_Gauss_calibration", "closed flux and Gauss calibration"),
    ("SRC3883_25_Delta_flux", CSV_CHARGE_CURRENT_RESIDUAL, "Delta_flux", "flux residual"),
    ("SRC3883_26_Delta_extra", CSV_CHARGE_CURRENT_RESIDUAL, "Delta_extra", "extra source residual"),
    ("SRC3883_27_DIV1", CSV_HILBERT_DIV, "DIV2467_1_full_divergence", "Hilbert current divergence"),
    ("SRC3883_28_DIV4", CSV_HILBERT_DIV, "DIV2467_4_Killing_clock", "Killing current closure"),
    ("SRC3883_29_EXC2", CSV_HILBERT_EXCHANGE, "EXC2467_2_total_stress_route", "total stress route"),
    ("SRC3883_30_HWT1", CSV_HWT_ATTEMPT, "HWT536_1_observed_Hilbert_measure_owned", "observed Hilbert measure"),
    ("SRC3883_31_PAC537_1", CSV_HWT_CONTRACT, "PAC537_1_single_observed_source_frame", "single observed source frame"),
    ("SRC3883_32_MCA2587_4", CSV_MIN_MATTER, "MCA2587_4_variation_before_readout", "variation before readout"),
    ("SRC3883_33_AD2587_2", CSV_MIN_MATTER_GATE, "AD2587_2_eobs_tau", "e_obs/tau same frame gate"),
    ("SRC3883_34_MWD2611_1", CSV_MATTER_DESCENT, "MWD2611_1_conditional_theorem", "matter quotient pullback"),
    ("SRC3883_35_NDV2612_3", CSV_DIRECT_GRAMMAR, "NDV2612_3_relative_countermodel", "relative source prefactor countermodel"),
    ("SRC3883_36_MNO2646_5", CSV_MATTER_OWNER, "MNO2646_5_countermodel", "source-only relative weight countermodel"),
    ("SRC3883_37_EMB0", CSV_EM_BOUND, "EMB3503_0_Delta_Hodge_EM", "EM Hodge mismatch"),
    ("SRC3883_38_EMB4", CSV_EM_BOUND, "EMB3503_4_Phi_EM_rad", "radiative Poynting flux"),
    ("SRC3883_39_EMB6", CSV_EM_BOUND, "EMB3503_6_Delta_J_total", "total Hilbert current closure"),
    ("SRC3883_40_EMF0", CSV_EM_POYNTING, "EMF3502_0_minimal_bound_field_stress", "minimal bound Maxwell stress"),
    ("SRC3883_41_EMF1", CSV_EM_POYNTING, "EMF3502_1_radiative_poynting_flux", "radiative Poynting flux"),
    ("SRC3883_42_EMF5", CSV_EM_POYNTING, "EMF3502_5_matter_EM_internal_exchange", "matter-EM internal exchange"),
    ("SRC3883_43_EM_accounting", CSV_EM_ACCOUNTING, "EM_POYNTING_ONCE_THEOREM_CONDITIONAL_BOUND_BRANCH_ACTIVE", "EM once-only accounting"),
    ("SRC3883_44_EM_flux_status", CSV_EM_FLUX_STATUS, "I_matter_EM_flux", "matter EM flux status"),
    ("SRC3883_45_EM_JQ", CSV_EM_JQ_STATUS, "JQ_MATTER_EM_POYNTING_SUBCOMPONENT_BOUND_FILLED_XI_OWNER_STILL_MISSING", "Jq EM/Poynting subcomponent"),
    ("SRC3883_46_CSR2", CSV_EM_CURRENT, "CSR3508_2_beta_source_alpha", "alpha/source marker"),
    ("SRC3883_47_CSR6", CSV_EM_CURRENT, "CSR3508_6_nonHilbert_bypass", "non-Hilbert source bypass"),
    ("SRC3883_48_DHB0", CSV_EM_HODGE, "DHB3504_0_Delta_Hodge_EM", "Hodge flow aggregate"),
    ("SRC3883_49_frame", CSV_FRAME, "FS3048_0_frame_split_definition", "frame/source split residual"),
]

MATTER_ACTION = (
    "S_matter^3883 = S_ord[psi,e_obs(q),theta] - (1/(4*mu0)) int sqrt(-g_obs) F_mn F^mn "
    "+ int sqrt(-g_obs) A_mu J^mu[psi,e_obs,theta], with no direct C_*, A_3, source-label, range, or readout selector."
)

HILBERT_STRESS = (
    "T_H^{mu nu}:=-(2/sqrt(-g_obs))*delta S_matter^3883/delta g_obs_{mu nu}; "
    "this is the same T_H^{mu nu} appearing in G_munu+Lambda g_munu=kappa0 T_H_munu."
)

MAXWELL_STRESS = (
    "T_EM^{mu nu}=(1/mu0)(F^{mu alpha}F^nu_alpha - 1/4 g_obs^{mu nu}F_{alpha beta}F^{alpha beta})."
)

POYNTING_RULE = (
    "In a local observed frame, S_Poynting^i=c*T_EM^{0i}; bound-field energy belongs inside T_H once, while net boundary flux "
    "Phi_EM_rad=int_boundary S_Poynting.n dA remains a source-drift residual unless stationary/no-flux is proved."
)

NEWTON_SOURCE = (
    "rho_H := T_H^{mu nu}u_mu u_nu/c^2; in the weak static frame T_00=rho_H c^2 and the 3882 metric equation gives nabla^2 Phi=4*pi*G0*rho_H."
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return ""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")).replace("\n", " ").replace("|", "\\|") for col in columns) + " |")
    return "\n".join(lines)


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_Hilbert_source_Maxwell_stress_lock",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def source_lock_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("HSL3883_0_action", "same matter action", MATTER_ACTION, "CANDIDATE_ACTION_INSERTED", "puts ordinary matter and EM into one observed source action"),
        ("HSL3883_1_Hilbert_definition", "Hilbert stress definition", HILBERT_STRESS, "DERIVED_BY_VARIATION", "field equation source is not a post-fit orbital GM"),
        ("HSL3883_2_same_source", "same-source lock", "Because the 3882 metric equation varies S_matter^3883, the source in the Einstein equation and the source defining rho_H are the same T_H.", "CANDIDATE_SAME_SOURCE_LOCK", "closes the pure notation gap between curvature source and Newton density"),
        ("HSL3883_3_variation_order", "variation before readout", "T_H and J_H[tau] are functional derivatives before Pi_M, support fitting, orbital calibration, or arena readout.", "NO_BACKFILL_GUARD", "prevents measured GM from defining the source after the fact"),
        ("HSL3883_4_conservation", "total stress conservation", "Diffeomorphism invariance plus field equations give nabla_mu T_H^{mu nu}=0 for the total matter+EM source on shell.", "CONDITIONAL_TOTAL_CONSERVATION", "ordinary matter and EM exchange internally, but total source is conserved"),
        ("HSL3883_5_limits", "remaining source limits", "Pi_M closure, Hamiltonian boundary charge equality, Gauss/orbital calibration, frame lock, and PPN source stability are not proved by HSL3883 alone.", "OPEN_RESIDUAL_GUARD", "keeps Newton/local-GR promotion blocked"),
    ]
    return [
        {
            "lock_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "effect": effect,
            "candidate_lock": True,
            "global_corpus_adopted": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, effect in raw_rows
    ]


def maxwell_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("MX3883_0_action", "minimal Maxwell action", "-(1/(4*mu0)) int sqrt(-g_obs) F_mn F^mn", "INSERTED_IN_CANDIDATE_MATTER_ACTION", "standard Maxwell stress follows from the same observed metric"),
        ("MX3883_1_stress", "Maxwell Hilbert stress", MAXWELL_STRESS, "DERIVED_BY_METRIC_VARIATION", "EM energy, pressure, and field momentum source gravity through T_H"),
        ("MX3883_2_Maxwell_equation", "Maxwell equation", "nabla_mu F^{mu nu}=mu0 J^nu from A_mu variation", "DERIVED_CONDITIONAL_CURRENT_OWNER", "EM current is the same matter current used in the action"),
        ("MX3883_3_exchange", "matter-EM exchange", "nabla_mu T_EM^{mu nu}=-F^{nu lambda}J_lambda and nabla_mu T_ord^{mu nu}=+F^{nu lambda}J_lambda, hence nabla_mu(T_ord+T_EM)^{mu nu}=0", "DERIVED_TOTAL_STRESS_ACCOUNTING", "Lorentz exchange is internal, not an extra gravitational source"),
        ("MX3883_4_poynting", "Poynting accounting", POYNTING_RULE, "DERIVED_ONCE_ONLY_ACCOUNTING", "Poynting is a stress component/flux, not a second source term"),
        ("MX3883_5_nonminimal_guard", "nonminimal EM guard", "Delta_Hodge_EM, w_EM, C_XF2, C_JQ, Phi_EM_rad and C_EM_readout remain explicit residuals unless theorem-zero or bounded.", "OPEN_EM_RESIDUAL_VECTOR", "prevents claiming Maxwell/EM stress while hidden couplings survive"),
    ]
    return [
        {
            "maxwell_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "effect": effect,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, effect in raw_rows
    ]


def residual_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("MER3883_0_Delta_source_frame", "delta_frame_source", "source variation and matter/readout do not use one observed frame", "same e_obs for matter, EM, clocks, source, and orbit", "P8_frame_source_split_residual_or_zero.csv"),
        ("MER3883_1_Delta_w_species", "Delta_w_species", "relative pre-action source weights alter Hilbert source", "parent matter grammar excludes source-only weights", "P8_Y5_MATTER_NORMALIZATION_OWNER_2646_OWNER_THEOREM_ATTEMPT.csv"),
        ("MER3883_2_Delta_Hodge_EM", "Delta_Hodge_EM", "EM Hodge/constitutive rule differs from g_obs", "observed Hodge is uniquely pulled from e_obs/q", "P8_EM_Hodge_flow_rule_bound_or_zero.csv"),
        ("MER3883_3_w_EM", "w_EM", "independent Maxwell action/stress multiplier", "unique Maxwell normalization plus alpha/current owner", "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"),
        ("MER3883_4_C_XF2", "C_XF2", "hidden/motion/time field couples to F^2 or F*F", "operator-domain exclusion or source-backed bound", "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"),
        ("MER3883_5_C_JQ", "C_JQ", "charge/current normalization ambiguity", "current, charge, alpha and Maxwell normalization owned together", "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"),
        ("MER3883_6_Phi_EM_rad", "Phi_EM_rad", "net radiative/background Poynting flux through local boundary", "stationary isolated branch or measured flux bound", "P8_EM_Poynting_source_flux_or_cross_term_vector.csv"),
        ("MER3883_7_Delta_J_total", "Delta_J_total", "total Hilbert current does not close after matter-EM/extras", "same parent variation and stationary source-free exterior", "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv"),
        ("MER3883_8_Delta_PiM", "Delta_PiM_metric", "Pi_M variation/projector stress leaks into mass source", "Pi_M parent-owned and covariantly constant or bounded", "P8_Hilbert_monopole_calibration_CONTRACT.csv"),
        ("MER3883_9_Delta_Gauss", "Delta_cal", "Hilbert source not calibrated to Gauss/orbital monopole", "Gauss surface integral and slow-particle readout derived", "P8_charge_current_equality_RESIDUAL_DECOMPOSITION.csv"),
        ("MER3883_10_Delta_PPN", "delta_beta_source;gamma_minus_1", "first-order source lock not stable at PPN order", "second-order weak-field source/operator calculation", "P8_PG_calibration_residual_MAP.csv"),
    ]
    return [
        {
            "residual_id": row_id,
            "symbol": symbol,
            "meaning": meaning,
            "zero_condition": zero,
            "fallback_artifact": artifact,
            "current_status": "RETAINED_NONCLAIM_RESIDUAL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, meaning, zero, artifact in raw_rows
    ]


def newton_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("NSB3883_0_density", "Hilbert density", NEWTON_SOURCE, "CANDIDATE_DENSITY_BRIDGE", "identifies the density in Poisson as Hilbert source density"),
        ("NSB3883_1_EM_bound_fields", "bound EM fields", "ordinary bound EM field energy contributes to rho_H through T_EM^{00}/c^2 exactly once", "CANDIDATE_ONCE_ONLY", "EM binding is not a separate calibrated GM term"),
        ("NSB3883_2_flux", "radiative flux", "dM_H/dt receives -Phi_EM_rad/c^2 if net boundary Poynting flux is nonzero", "RETAIN_FLUX_IF_NOT_STATIONARY", "keeps Gdot/source-time hair honest"),
        ("NSB3883_3_Poisson", "Poisson coefficient", "with 3882 constant G0 and same T_H, nabla^2 Phi=4*pi*G0*rho_H", "EXACT_CONDITIONAL_ON_GAUSS_AND_READOUT", "still needs Gauss/orbital mass calibration"),
        ("NSB3883_4_no_GR_promotion", "scope guard", "first-order Hilbert source lock does not prove gamma=1, beta=1, preferred-frame zeros, or no non-EH operators", "NO_LOCAL_GR_PROMOTION", "PPN/R11 vector remains live"),
    ]
    return [
        {
            "bridge_id": row_id,
            "piece": piece,
            "statement": statement,
            "status": status,
            "remaining_gate": gate,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, piece, statement, status, gate in raw_rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, object]]:
    raw_rows = [
        ("RUNU3883_0_source_lock", "b_MHref_lock", "b_MHref_lock := b_Hilbert_mismatch+b_EM_once+b_PiM+b_Gauss+b_flux+b_source_frame+b_source_weight", "SOURCE_LOCK_DECOMPOSED"),
        ("RUNU3883_1_candidate_zeros", "candidate zeros", "b_Hilbert_mismatch=0 and b_EM_once=0 inside the 3883 candidate action; live claim keeps them nonclaim until parent adoption", "CANDIDATE_ONLY"),
        ("RUNU3883_2_EM_residual", "b_EM_residual", "b_EM_residual := b_Hodge_EM+b_wEM+b_XF2+b_JQ+b_PhiEMrad+b_EM_readout", "EM_RESIDUAL_VECTOR_EXPLICIT"),
        ("RUNU3883_3_Newton", "Newton source", "rho_source -> rho_H := T_H(u,u)/c^2 with T_H=T_ord+T_EM from the same action", "NEWTON_DENSITY_BRIDGE"),
        ("RUNU3883_4_top", "z_g_active,cal", "|z_g_active,cal| <= b_Qstar + b_Noether + b_tail_rel + b_Gcommon with b_MHref_lock refined by 3883", "NO_CANCELLATION_RUNNER"),
    ]
    return [
        {
            "update_id": row_id,
            "runner_field": field,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, field, rule, status in raw_rows
    ]


def gates_rows(
    sources: list[dict[str, object]],
    source_lock: list[dict[str, object]],
    maxwell: list[dict[str, object]],
    residuals: list[dict[str, object]],
    newton: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    source_count = sum(1 for row in sources if row["exists"] and row["needle_found"])
    checks = [
        ("G3883_0_sources", source_count == len(sources), f"{source_count}/{len(sources)} sources resolved"),
        ("G3883_1_Hilbert", any(row["lock_id"] == "HSL3883_1_Hilbert_definition" for row in source_lock), "Hilbert stress defined by variation"),
        ("G3883_2_same_source", any(row["lock_id"] == "HSL3883_2_same_source" for row in source_lock), "same-source lock candidate exists"),
        ("G3883_3_Maxwell", any(row["maxwell_id"] == "MX3883_1_stress" and "F^{mu alpha}" in str(row["statement"]) for row in maxwell), "Maxwell stress derived"),
        ("G3883_4_Poynting", any(row["maxwell_id"] == "MX3883_4_poynting" for row in maxwell), "Poynting accounting present"),
        ("G3883_5_residual_vector", len(residuals) >= 10, f"{len(residuals)} retained matter/EM residuals"),
        ("G3883_6_Newton_density", any(row["bridge_id"] == "NSB3883_0_density" for row in newton), "rho_H bridge present"),
        ("G3883_7_no_claim", True, "Pi_M/Gauss/orbital/PPN/global adoption remain open"),
    ]
    return [
        {
            "gate_id": gate_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, passed, detail in checks
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3883_0",
            "target_checkpoint": "3884-Y5-R2FR-PiM-Hilbert-flux-Gauss-monopole-calibration-or-residual-bound.md",
            "script": "scripts/Y5_R2FR_3884_PiM_Hilbert_flux_Gauss_monopole_calibration_or_residual_bound.py",
            "objective": "derive Pi_M projected Hilbert mass flux closure and the Gauss/orbital monopole calibration from the same source; if it fails, emit executable dln_Meff_dt, radial source hair, and Gauss calibration residual rows",
            "why_next": "3883 locks the candidate stress source and Maxwell accounting; Newton still needs the projected Hilbert mass to be closed and equal to the Gauss/orbital monopole",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3883_0",
            "branch": BRANCH,
            "summary": "candidate same-Hilbert-source lock and Maxwell stress/Poynting once-only accounting derived; residual vector keeps Hodge, normalization, nonminimal EM, radiative flux, PiM, Gauss, source-weight, frame and PPN gates explicit",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(
    sources: list[dict[str, object]],
    source_lock: list[dict[str, object]],
    maxwell: list[dict[str, object]],
    residuals: list[dict[str, object]],
    newton: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    resolved = sum(1 for row in sources if row["exists"] and row["needle_found"])
    doc = f"""# 3883 - Hilbert Source and Maxwell Stress Lock or Residual Vector

Generated: `{timestamp}`

## Result

3883 inserts the candidate matter/EM source action:

`{MATTER_ACTION}`

The source stress is:

`{HILBERT_STRESS}`

and the Maxwell part is:

`{MAXWELL_STRESS}`

This gives a clean candidate same-source bridge: the stress in the local field equation, the Newton density, and the EM/Poynting stress are all one Hilbert source before readout. No claim is made yet because the parent adoption, Pi_M flux, Gauss/orbital calibration and PPN stability remain open.

## Same Hilbert Source Lock

{markdown_table(source_lock, ["lock_id", "piece", "statement", "status", "effect"])}

## Maxwell Stress and Poynting Derivation

{markdown_table(maxwell, ["maxwell_id", "piece", "statement", "status", "effect"])}

## Newton Source Density Bridge

{markdown_table(newton, ["bridge_id", "piece", "statement", "status", "remaining_gate"])}

## Matter/EM Residual Vector

{markdown_table(residuals, ["residual_id", "symbol", "meaning", "zero_condition", "fallback_artifact"])}

## Runner Update

{markdown_table(runner, ["update_id", "runner_field", "rule", "status"])}

## Source Register

Resolved `{resolved}/{len(sources)}` source rows.

{markdown_table(sources, ["source_id", "path", "needle_found", "role"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "detail", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3883 makes the source side sharper. EM/Poynting is no longer a vague extra field: in the candidate action it is part of the same Hilbert stress exactly once, with radiative flux retained if nonzero. The next hard step is the mass-charge step: prove `Pi_M J_H` is closed and calibrates to the Gauss/orbital monopole, or bound the remaining `M_eff`/radial/Gauss residuals.
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    start = "<!-- BEGIN 3883 HILBERT MAXWELL SOURCE LOCK -->"
    end = "<!-- END 3883 HILBERT MAXWELL SOURCE LOCK -->"
    block = f"""{start}

## 3883 - Hilbert source and Maxwell stress lock

Candidate matter/EM action:

`{MATTER_ACTION}`

Hilbert source:

`{HILBERT_STRESS}`

Maxwell/Poynting:

`{MAXWELL_STRESS}`

`{POYNTING_RULE}`

Newton density bridge:

`{NEWTON_SOURCE}`

Nonclaim guard: same-source and Maxwell once-only accounting are candidate-locked, but parent adoption, Pi_M flux closure, Gauss/orbital calibration, Hodge/normalization/nonminimal EM residuals, radiative flux, source weights, frame split and PPN stability remain live.

Generated outputs:
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv`
- `source-intake\\mts_residuals\\P8_Y5_R2FR_3883_MATTER_EM_RESIDUAL_VECTOR.csv`
- `source-intake\\mts_residuals\\P8_Y5_BRR545_3883_VALIDATION.csv`

Next gate: `3884`, Pi_M Hilbert flux and Gauss monopole calibration.

<!-- Generated by 3883 at {timestamp} -->
{end}
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if start in existing and end in existing:
        before = existing.split(start)[0].rstrip()
        after = existing.split(end, 1)[1].lstrip()
        new_text = f"{before}\n\n{block}\n\n{after}".rstrip() + "\n"
    else:
        new_text = existing.rstrip() + "\n\n" + block + "\n"
    SPINE_PATH.write_text(new_text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    source_lock: list[dict[str, object]],
    maxwell: list[dict[str, object]],
    residuals: list[dict[str, object]],
    newton: list[dict[str, object]],
    runner: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    checks: list[tuple[str, str, bool, str]] = []
    all_sources = all(row["exists"] and row["needle_found"] for row in sources)
    checks.append(("VAL3883_0_sources", "all cited source paths exist and needles are found", all_sources, f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved"))
    checks.append(("VAL3883_1_source_action", "matter/EM action inserted", any(row["lock_id"] == "HSL3883_0_action" and "F_mn F^mn" in str(row["statement"]) for row in source_lock), "HSL3883_0_action"))
    checks.append(("VAL3883_2_Hilbert", "Hilbert stress defined by variation", any(row["lock_id"] == "HSL3883_1_Hilbert_definition" and "delta S_matter" in str(row["statement"]) for row in source_lock), "HSL3883_1"))
    checks.append(("VAL3883_3_same_source", "same-source lock row exists", any(row["lock_id"] == "HSL3883_2_same_source" for row in source_lock), "HSL3883_2"))
    checks.append(("VAL3883_4_Maxwell_stress", "Maxwell stress row exists", any(row["maxwell_id"] == "MX3883_1_stress" and "F^{mu alpha}" in str(row["statement"]) for row in maxwell), "MX3883_1"))
    checks.append(("VAL3883_5_Poynting", "Poynting accounting row exists", any(row["maxwell_id"] == "MX3883_4_poynting" and "Phi_EM_rad" in str(row["statement"]) for row in maxwell), "MX3883_4"))
    checks.append(("VAL3883_6_residual_vector", "matter/EM residual vector includes required residuals", {"Delta_Hodge_EM", "w_EM", "C_XF2", "Phi_EM_rad", "Delta_PiM_metric", "Delta_cal"}.issubset({str(row["symbol"]) for row in residuals}), "required residual symbols"))
    checks.append(("VAL3883_7_Newton_density", "Newton density bridge uses rho_H", any(row["bridge_id"] == "NSB3883_0_density" and "rho_H" in str(row["statement"]) for row in newton), "NSB3883_0"))
    checks.append(("VAL3883_8_runner", "runner decomposes b_MHref_lock", any(row["runner_field"] == "b_MHref_lock" for row in runner), "b_MHref_lock"))
    checks.append(("VAL3883_9_no_claim_gates", "no gate allows a claim", all(str(row["claim_allowed"]) == "False" for row in gates), "claim_allowed=false"))
    checks.append(("VAL3883_10_doc", "markdown checkpoint exists with bottom line", DOC_PATH.exists() and "EM/Poynting is no longer a vague extra field" in read_text(DOC_PATH), rel(DOC_PATH)))
    checks.append(("VAL3883_11_spine", "spine updated with 3883 block", SPINE_PATH.exists() and "BEGIN 3883 HILBERT MAXWELL SOURCE LOCK" in read_text(SPINE_PATH), rel(SPINE_PATH)))
    csv_outputs = [path for key, path in OUTPUTS.items() if key != "validation"]
    csv_parse_ok = True
    parse_details = []
    for path in csv_outputs:
        try:
            parse_details.append(f"{path.name}:{len(read_csv_rows(path))}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{path.name}:{exc}")
    checks.append(("VAL3883_12_csv_parse", "all generated CSV outputs parse", csv_parse_ok, "; ".join(parse_details)))
    formalization_hits = []
    generated_patterns = ("3883-Y5", "P8_Y5_R2FR_3883", "P8_Y5_BRR545_3883")
    if FWB.exists():
        formalization_hits = [
            path
            for path in FWB.rglob("*3883*")
            if path.is_file() and any(pattern in path.name for pattern in generated_patterns)
        ]
    checks.append(("VAL3883_13_formalization_untouched", "no generated 3883 files appear in formalization-workbench", not formalization_hits, f"{len(formalization_hits)} hits"))
    pycache_hits = [path for path in (PCW / "scripts").rglob("__pycache__") if path.is_dir()]
    checks.append(("VAL3883_14_no_pycache", "scripts __pycache__ removed", not pycache_hits, f"{len(pycache_hits)} pycache dirs"))
    checks.append(("VAL3883_15_all_nonclaim", "all analytical rows are nonclaim", all(str(row.get("valid_for_claim")) == "False" for collection in [source_lock, maxwell, residuals, newton, runner] for row in collection), "valid_for_claim=false"))
    checks.append(("VAL3883_16_next_target", "next target attacks PiM/Gauss calibration", any("PiM-Hilbert-flux-Gauss" in str(row["target_checkpoint"]) for row in next_rows(timestamp)), "3884 PiM/Gauss"))
    return [
        {
            "check_id": check_id,
            "description": description,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, description, passed, detail in checks
    ]


def main() -> int:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    source_lock = source_lock_rows(timestamp)
    maxwell = maxwell_rows(timestamp)
    residuals = residual_rows(timestamp)
    newton = newton_rows(timestamp)
    runner = runner_rows(timestamp)
    gates = gates_rows(sources, source_lock, maxwell, residuals, newton, timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["source_lock"], source_lock)
    write_csv(OUTPUTS["maxwell"], maxwell)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["newton"], newton)
    write_csv(OUTPUTS["runner"], runner)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, source_lock, maxwell, residuals, newton, runner, gates, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, source_lock, maxwell, residuals, newton, runner, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_HILBERT_SOURCE_MAXWELL_STRESS_LOCK")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
