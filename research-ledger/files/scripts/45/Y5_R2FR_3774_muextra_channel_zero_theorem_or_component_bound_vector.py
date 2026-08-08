import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3774"
BRANCH = "MTS_R2FR_Y5_MUEXTRA_CHANNEL_ZERO_THEOREM_OR_COMPONENT_BOUND_VECTOR_3774"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3774-Y5-R2FR-muextra-channel-zero-theorem-or-component-bound-vector.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3774_SOURCE_REGISTER.csv",
    "shell_identity": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_SHELL_BALANCE_IDENTITY.csv",
    "zero_theorem": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_CHANNEL_ZERO_THEOREM.csv",
    "zero_attempt": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_ZERO_ATTEMPT.csv",
    "component_bounds": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_COMPONENT_BOUND_VECTOR.csv",
    "observable_matrix": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_OBSERVABLE_PROJECTION_MATRIX.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3774_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3774_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3774_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3774_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3774_VALIDATION.csv",
}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base(timestamp: str, valid_for_claim: bool = False) -> dict[str, object]:
    return {
        "timestamp_utc": timestamp,
        "branch_id": BRANCH,
        "checkpoint_id": CHECKPOINT,
        "valid_for_claim": valid_for_claim,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_paths() -> dict[str, Path]:
    return {
        "SRC3774_0_3773_doc": PCW / "3773-Y5-R2FR-Hamiltonian-Gauss-surface-charge-equals-Hilbert-mass-or-muextra-bound.md",
        "SRC3774_1_3773_surface_theorem": RESIDUALS / "P8_Y5_R2FR_3773_HAMILTONIAN_GAUSS_SURFACE_THEOREM.csv",
        "SRC3774_2_3773_channels": RESIDUALS / "P8_Y5_R2FR_3773_MUEXTRA_CHANNEL_AUDIT.csv",
        "SRC3774_3_3773_residuals": RESIDUALS / "P8_Y5_R2FR_3773_MUEXTRA_RESIDUAL_COEFFICIENTS.csv",
        "SRC3774_4_3773_budget": RESIDUALS / "P8_Y5_R2FR_3773_MUEXTRA_BOUND_BUDGET.csv",
        "SRC3774_5_Hamiltonian_charge_contract": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "SRC3774_6_Poisson_Gauss_contract": RESIDUALS / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "SRC3774_7_3760_EM_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3774_8_3760_EM_budget": RESIDUALS / "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv",
        "SRC3774_9_3762_range_budget": RESIDUALS / "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv",
        "SRC3774_10_3768_kappa_budget": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv",
        "SRC3774_11_3769_shadow_budget": RESIDUALS / "P8_Y5_R2FR_3769_SHADOW_FRAME_BOUND_BUDGET.csv",
        "SRC3774_12_3770_source_budget": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_BOUND_BUDGET.csv",
        "SRC3774_13_3771_theta_budget": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_BOUND_BUDGET.csv",
        "SRC3774_14_3772_budget": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_GM_BOUND_BUDGET.csv",
        "SRC3774_15_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3774_16_3759_wep_eval": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3774 mu_extra zero theorem or component bound input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def imported_bounds() -> dict[str, str]:
    wep = find_row(source_paths()["SRC3774_16_3759_wep_eval"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3774_15_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3774_15_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    gdot = find_row(source_paths()["SRC3774_10_3768_kappa_budget"], "budget_id", "KBB3768_0_Gdot_total")
    return {
        "wep": wep["bound_value"],
        "gamma": gamma["bound_value"],
        "beta": beta["bound_value"],
        "gdot": gdot["bound_value"],
    }


def shell_identity_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "MSB3774_0_define_exterior_monopole",
            "For any sphere S_R in the local exterior, define mu_obs(R) by the normalized Gauss flux of Phi_obs in the same observed frame used by test-body readout.",
            "This is a definition of the measured monopole at radius R; it is not yet equal to G_eff M_H.",
            "mu_obs(R) := N_G int_{S_R} n^i partial_i Phi_obs dS",
            "EXACT_DEFINITION",
        ),
        (
            "MSB3774_1_shell_balance",
            "Between two homologous exterior spheres, the difference of measured monopoles equals the shell integral of every non-Hilbert or non-descended exterior source plus boundary/reference flux.",
            "Apply Stokes/Gauss to the reduced exterior field equation in divergence form, keeping all residual operators rather than hiding them in G.",
            "mu_obs(R2)-mu_obs(R1)=Delta Q_boundary+int_shell(R_nonEH+R_projector+R_memory+R_range+R_kappa+R_readout+R_EM+R_theta)dV",
            "EXACT_CONDITIONAL_SHELL_IDENTITY",
        ),
        (
            "MSB3774_2_component_split",
            "Taking R1 outside the compact Hilbert source and R2 at the comparison/readout surface gives mu_obs=G_eff M_H+sum_i Q_i.",
            "The 3773 Hamiltonian/Gauss bridge supplies G_eff M_H; all remaining shell or surface terms are defined as Q_i components of mu_extra.",
            "mu_extra=Q_boundary_ref+Q_projector_domain+Q_nonEH+Q_memory_bulk+Q_range+Q_delta_kappa+Q_readout_frame+Q_EM_Poynting+Q_source_theta",
            "EXACT_MUEXTRA_COMPONENT_IDENTITY",
        ),
        (
            "MSB3774_3_derivative_profile",
            "Any radial, temporal, range, species, or frame dependence of measured GM is the corresponding derivative of G_eff M_H plus the derivative of the Q_i sum.",
            "Differentiate the component identity; this is the no-hair test interface.",
            "partial_a ln mu_obs = partial_a ln(G_eff M_H) + partial_a mu_extra/mu_obs",
            "EXACT_DERIVATIVE_PROFILE_IDENTITY",
        ),
    ]
    return [
        {
            **base(timestamp),
            "identity_id": identity_id,
            "statement": statement,
            "derivation": derivation,
            "formula": formula,
            "status": status,
            "claim_allowed": False,
        }
        for identity_id, statement, derivation, formula, status in rows
    ]


def zero_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "MZT3774_0_master_zero",
            "If every residual channel is either same-Hilbert-source, has zero total extra interior monopole, is an exact divergence with zero flux on homologous boundaries, or is a pure gauge/reference variation, and no exterior harmonic 1/r mode remains, then mu_extra=0.",
            "Each Q_i is a surface or shell integral from MSB3774_2 plus any interior extra monopole not already inside M_H. Under those alternatives its integral vanishes or is already counted inside M_H. With no harmonic monopole, a zero shell derivative fixes the exterior charge to the reference value zero.",
            "EXACT_CONDITIONAL_MUEXTRA_ZERO_THEOREM",
        ),
        (
            "MZT3774_1_boundary_reference",
            "Q_boundary_ref=0 if the Hamiltonian reference subtraction is fixed on the connected local branch and its variation is q_obs-gauge or an exact boundary term with equal inner/outer flux.",
            "Then Delta B_ref is constant on the branch; the reference convention sets that constant to zero.",
            "EXACT_CONDITIONAL_BOUNDARY_ZERO",
        ),
        (
            "MZT3774_2_projector_domain",
            "Q_projector_domain=0 if Pi_M commutes with exterior divergence, the source domain is material/comoving, and no projector wall or corner term crosses the comparison shell.",
            "The shell integral of [d,Pi_M]J_H plus domain-wall current vanishes under those conditions.",
            "EXACT_CONDITIONAL_PROJECTOR_DOMAIN_ZERO",
        ),
        (
            "MZT3774_3_nonEH_operator",
            "Q_nonEH=0 if the exterior weak-field operator is EH/Poisson after q_obs reduction and every non-EH correction has compact support or faster-than-monopole falloff.",
            "The only possible contribution to the Gauss charge is the l=0 harmonic component of the exterior operator residual.",
            "EXACT_CONDITIONAL_NONEH_ZERO",
        ),
        (
            "MZT3774_4_memory_bulk",
            "Q_memory_bulk=0 if memory/topological terms are exact, have no boundary flux through the exterior spheres, and carry no harmonic monopole class in the exterior cohomology.",
            "Topological or memory terms affect the monopole only through their boundary/cohomology class.",
            "EXACT_CONDITIONAL_MEMORY_ZERO",
        ),
        (
            "MZT3774_5_range",
            "Q_range=0 if no unscreened finite-range mediator couples to the Hilbert source, or if its source charge vanishes for the body and test readout under q_obs.",
            "A Yukawa or extra scalar/vector mode contributes to mu_extra only through its l=0 source charge and range kernel.",
            "EXACT_CONDITIONAL_RANGE_ZERO",
        ),
        (
            "MZT3774_6_coupling_kappa",
            "Q_delta_kappa=0 if G_eff/kappa_eff is q_obs-owned or superselected and has no exterior radial, temporal, species, or frame dependence.",
            "Then the measured monopole is not reweighted between source and readout surfaces.",
            "EXACT_CONDITIONAL_COUPLING_ZERO",
        ),
        (
            "MZT3774_7_readout_frame",
            "Q_readout_frame=0 if slow test bodies follow the same q_obs metric/coframe potential used by the Gauss flux and no preferred-frame or apparatus readout offset survives.",
            "The orbital acceleration then reads exactly the same monopole that the surface integral defines.",
            "EXACT_CONDITIONAL_READOUT_ZERO",
        ),
        (
            "MZT3774_8_EM_Poynting",
            "Q_EM_Poynting=0 as an extra channel only if exterior EM field energy, binding energy, and Poynting momentum are included in the same descended Hilbert source, or if the exterior EM stress has zero l=0 energy/flux for the source class.",
            "Maxwell stress is not allowed to disappear; it must either be inside M_H or explicitly counted as Q_EM_Poynting.",
            "EXACT_CONDITIONAL_EM_POYNTING_ZERO",
        ),
        (
            "MZT3774_9_source_theta",
            "Q_source_theta=0 if the source action and every physical constant/material marker descend through q_obs or are superselected.",
            "Then vertical source/theta leakage cannot generate an exterior mass-normalization monopole.",
            "EXACT_CONDITIONAL_SOURCE_THETA_ZERO",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "derivation": derivation,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, derivation, status in rows
    ]


def zero_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("MZA3774_0_master_identity", "mu_extra component identity exists", "MSB3774_2 emitted", True, "all exterior-monopole leakage is now forced into Q_i rows"),
        ("MZA3774_1_boundary_reference", "fixed Hamiltonian reference and integrability", "3773/HZA3773_2 remains unsigned", False, "Q_boundary_ref stays live"),
        ("MZA3774_2_projector_domain", "Pi_M commutes with exterior divergence and no domain-wall flux", "3773/MEC3773_1 and HC6/SN4 remain unsigned", False, "Q_projector_domain stays live"),
        ("MZA3774_3_nonEH_operator", "EH/Poisson is the whole exterior l=0 operator", "local EH selected but not parent-derived", False, "Q_nonEH stays live"),
        ("MZA3774_4_memory_bulk", "memory/topological channel has no exterior harmonic monopole", "no parent cohomology/support certificate supplied", False, "Q_memory_bulk stays live"),
        ("MZA3774_5_range", "no finite-range source charge or unscreened mediator", "R10/range rows still require alpha(lambda) source charges", False, "Q_range stays live"),
        ("MZA3774_6_coupling_kappa", "kappa/G_eff is q_obs-owned or superselected in the exterior", "3768 kappa zero route remains unsigned", False, "Q_delta_kappa stays live"),
        ("MZA3774_7_readout_frame", "orbital readout uses the same q_obs potential as the surface flux", "3769/3772 frame-orbit rows remain unsigned", False, "Q_readout_frame stays live"),
        ("MZA3774_8_EM_Poynting", "EM/Poynting stress is inside the same Hilbert source or has zero exterior l=0 stress", "3760 gives the conditional route but not parent-signed descent", False, "Q_EM_Poynting stays live"),
        ("MZA3774_9_source_theta", "source action and constants/material markers descend or are superselected", "3770/3771 zero routes remain unsigned", False, "Q_source_theta stays live"),
        ("MZA3774_10_verdict", "current branch proves mu_extra=0", "component theorem exists, but no channel has parent-signed zero/support/no-harmonic certificates", False, "Newton measured-GM remains nonclaim"),
    ]
    return [
        {
            **base(timestamp),
            "attempt_id": attempt_id,
            "required_clause": required_clause,
            "evidence": evidence,
            "passes_clause": passes_clause,
            "consequence": consequence,
            "claim_allowed": False,
        }
        for attempt_id, required_clause, evidence, passes_clause, consequence in rows
    ]


def component_bound_rows(timestamp: str, bounds: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        (
            "MCB3774_0_boundary_reference",
            "Q_boundary_ref",
            "epsilon_boundary_ref",
            "|Delta B_ref|/(G_eff M_H)",
            "MISSING_FIXED_REFERENCE_INTEGRABILITY_COMPONENT",
            "dimensionless",
            "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv:HC2",
            "zero if boundary/reference subtraction is fixed and exact",
        ),
        (
            "MCB3774_1_projector_domain",
            "Q_projector_domain",
            "epsilon_projector_domain",
            "|int_shell ([d,Pi_M]J_H + J_wall)|/M_H",
            "MISSING_PROJECTOR_COMMUTATOR_DOMAIN_WALL_COMPONENT",
            "dimensionless",
            "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv:HC6",
            "zero if projected source flux is closed on the material exterior",
        ),
        (
            "MCB3774_2_nonEH_operator",
            "Q_nonEH",
            "epsilon_nonEH_mass",
            "|int_shell R_nonEH dV|/M_H",
            "MISSING_NON_EH_L0_OPERATOR_COMPONENT",
            "dimensionless",
            "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv:PG3",
            "zero if exterior operator is pure EH/Poisson in the l=0 sector",
        ),
        (
            "MCB3774_3_memory_bulk",
            "Q_memory_bulk",
            "epsilon_memory_bulk",
            "|Q_topological + Q_memory_l0|/M_H",
            "MISSING_MEMORY_TOPOLOGICAL_HARMONIC_MONOPOLE_COMPONENT",
            "dimensionless",
            "P8_Y5_R2FR_3773_MUEXTRA_CHANNEL_AUDIT.csv:MEC3773_3_memory_bulk",
            "zero if memory/topological terms have no exterior harmonic monopole",
        ),
        (
            "MCB3774_4_range",
            "Q_range",
            "epsilon_range_mass_or_alpha_lambda",
            "alpha(lambda) or |sum_X K_X Q_source_X Q_test_X exp(-r/lambda_X)|",
            "MISSING_RANGE_SOURCE_CHARGE_AND_BOUND_CURVE_COMPONENTS",
            "range-dependent",
            "P8_Y5_R2FR_3762_RANGE_RADIAL_FRAME_RESIDUAL_BUDGET.csv:RRF_BUD3762_0_alpha_lambda",
            "zero if no unscreened finite-range mediator or source charge exists",
        ),
        (
            "MCB3774_5_coupling_kappa",
            "Q_delta_kappa",
            "epsilon_delta_kappa",
            "|Delta ln G_eff| + |partial_r ln G_eff| L + |partial_t ln G_eff| T",
            bounds["gdot"],
            "yr^-1_envelope_plus_dimensionless_projection",
            "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv:KBB3768_0_Gdot_total",
            "zero if kappa/G_eff is q_obs-owned or superselected",
        ),
        (
            "MCB3774_6_readout_frame",
            "Q_readout_frame",
            "epsilon_readout_frame",
            "|mu_fit/mu_flux - 1|",
            "MISSING_ORBITAL_FRAME_READOUT_COMPONENT",
            "dimensionless",
            "P8_Y5_R2FR_3769_SHADOW_FRAME_BOUND_BUDGET.csv:SBB3769_6_Newton_frame_calibration",
            "zero if orbit and flux use the same q_obs potential",
        ),
        (
            "MCB3774_7_EM_Poynting",
            "Q_EM_Poynting",
            "epsilon_EM_Poynting_mass",
            "|int_ext (T_EM00/c^2 + div S_EM/c^4) dV|/M_H unless included in M_H",
            "MISSING_EM_HILBERT_DESCENT_OR_EXTERIOR_L0_STRESS_COMPONENT",
            "dimensionless",
            "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv:EMR3760_0_WEP_EM_binding",
            "zero only as an extra if EM/Poynting is in the same Hilbert source or exterior l=0 stress vanishes",
        ),
        (
            "MCB3774_8_source_theta",
            "Q_source_theta",
            "epsilon_source_theta_mass",
            "C_mu_src epsilon_src + C_mu_theta epsilon_theta + b_source_norm",
            "MISSING_NEWTON_SOURCE_THETA_PROJECTION_COMPONENT",
            "dimensionless",
            "P8_Y5_R2FR_3771_CONSTANT_MARKER_BOUND_BUDGET.csv:CBB3771_8_Newton_source_norm",
            "zero if source action and material/constants markers descend through q_obs or are superselected",
        ),
        (
            "MCB3774_9_total",
            "mu_extra",
            "epsilon_mu_extra",
            "sum_i |Q_i|/(G_eff M_H)",
            "MISSING_COMPONENT_VALUES_FOR_MUEXTRA_TOTAL",
            "dimensionless",
            "P8_Y5_R2FR_3773_MUEXTRA_BOUND_BUDGET.csv:MUB3773_1_mu_extra",
            "zero if every component row above is parent-zeroed",
        ),
    ]
    return [
        {
            **base(timestamp),
            "component_id": component_id,
            "channel_symbol": channel_symbol,
            "residual_symbol": residual_symbol,
            "bound_formula": bound_formula,
            "bound_or_value": bound_or_value,
            "units": units,
            "source": source,
            "zero_condition": zero_condition,
            "component_signed": False,
            "claim_allowed": False,
        }
        for component_id, channel_symbol, residual_symbol, bound_formula, bound_or_value, units, source, zero_condition in rows
    ]


def observable_matrix_rows(timestamp: str, bounds: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        ("MOM3774_0_Newton_GM", "delta_ln_mu_obs", "epsilon_HH + epsilon_Gauss + epsilon_mu_extra + epsilon_orbit + |delta ln G_eff|", "MISSING_NEWTON_GM_RESIDUAL_BOUND_OR_COMPONENTS", "Newton/orbital GM", False),
        ("MOM3774_1_WEP", "eta_source_AB", "C_WEP^EM epsilon_EM_Poynting_mass + C_WEP^theta epsilon_source_theta + C_WEP^range epsilon_range + epsilon_projector_domain", bounds["wep"], "WEP/composition", False),
        ("MOM3774_2_Gdot", "dln_mu_obs_dt", "|d_t ln G_eff| + |d_t epsilon_mu_extra| + |d_t ln M_H|", bounds["gdot"], "LLR/Gdot", False),
        ("MOM3774_3_gamma", "delta_gamma", "C_gamma^H epsilon_HH + C_gamma^G epsilon_Gauss + C_gamma^mu epsilon_mu_extra + C_gamma^EM epsilon_EM", bounds["gamma"], "Cassini/Shapiro", False),
        ("MOM3774_4_beta", "delta_beta", "C_beta^H epsilon_HH + C_beta^mu epsilon_mu_extra + C_beta^nonEH epsilon_nonEH + C_beta^source epsilon_source_theta", bounds["beta"], "PPN beta", False),
        ("MOM3774_5_R10", "alpha(lambda)", "P_R10[Q_range,Q_projector_domain,Q_source_theta]", "MISSING_R10_BOUND_CURVE_AND_SOURCE_CHARGES", "short-range inverse-square", False),
        ("MOM3774_6_radial_hair", "partial_r_ln_mu_obs", "|partial_r ln G_eff| + sum_i |partial_r Q_i|/|mu_obs|", "MISSING_RADIAL_PROFILE_OR_NO_HAIR_THEOREM", "radial/orbital profile", False),
        ("MOM3774_7_EM_charge_bridge", "epsilon_EM_Poynting_mass", "zero only if EM field stress is already inside total Hilbert source; otherwise exterior EM energy is an explicit mass channel", "MISSING_EM_HILBERT_DESCENT_OR_EXTERIOR_L0_STRESS_COMPONENT", "EM/charge/source coupling", False),
    ]
    return [
        {
            **base(timestamp),
            "matrix_id": matrix_id,
            "observable": observable,
            "projection_formula": projection_formula,
            "bound_or_target": bound_or_target,
            "arena": arena,
            "score_ready": score_ready,
            "claim_allowed": False,
        }
        for matrix_id, observable, projection_formula, bound_or_target, arena, score_ready in rows
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    shell_identity = any(row["identity_id"] == "MSB3774_2_component_split" for row in grouped["shell_identity"])
    master_zero = any(row["theorem_id"] == "MZT3774_0_master_zero" for row in grouped["zero_theorem"])
    nine_components = len([row for row in grouped["component_bounds"] if row["component_id"] != "MCB3774_9_total"]) == 9
    em_channel = any(row["channel_symbol"] == "Q_EM_Poynting" for row in grouped["component_bounds"])
    all_components_signed = all(row["component_signed"] is True for row in grouped["component_bounds"])
    missing_components = any(str(row["bound_or_value"]).startswith("MISSING_") for row in grouped["component_bounds"])
    nonclaim = all(row["claim_allowed"] is False for table in grouped.values() for row in table if "claim_allowed" in row)
    rows = [
        ("CG3774_0_sources", "all 3774 source paths exist", sources_exist, "path hygiene"),
        ("CG3774_1_shell_identity", "mu_extra shell/component identity emitted", shell_identity, "Q_i rows are mathematically defined"),
        ("CG3774_2_master_zero_theorem", "master no-extra-monopole zero theorem emitted", master_zero, "zero route is real but conditional"),
        ("CG3774_3_component_vector", "all nine 3773 channels have component bound rows", nine_components, "no named channel is dropped"),
        ("CG3774_4_EM_Poynting_kept", "EM/Poynting channel remains explicit", em_channel, "not hidden inside fitted G"),
        ("CG3774_5_components_parent_signed", "all Q_i components are parent-zeroed or numeric", all_components_signed, "expected false until support/no-harmonic certificates exist"),
        ("CG3774_6_missing_components_nonclaim", "missing component rows remain nonclaim blockers", missing_components, "no pass from placeholders"),
        ("CG3774_7_nonclaim_hygiene", "all rows remain private/nonclaim unless parent-signed", nonclaim, "protects the framework from overclaiming"),
        ("CG3774_8_Newton_GM_claim", "first-order measured-GM Newton claim allowed", False, "blocked until Q_i components close and orbital readout is signed"),
    ]
    return [
        {
            **base(timestamp),
            "gate_id": gate_id,
            "gate": gate,
            "passed": passed,
            "details": details,
            "claim_allowed": False,
        }
        for gate_id, gate, passed, details in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3774_0", "The measured-GM obstruction is no longer a formless missing coupling; it is the exterior monopole sum mu_extra=sum_i Q_i.", "future work must either zero or bound each Q_i."),
        ("DEC3774_1", "The strongest general route is a no-harmonic-exterior-monopole lemma: compact support, exact divergence with zero flux, same-Hilbert-source inclusion, or pure gauge/reference kills a channel.", "turn parent-action work into support/no-harmonic certificates."),
        ("DEC3774_2", "EM/Poynting cannot be waved away: exterior electromagnetic energy and momentum either belong to the same Hilbert source or remain an explicit mass channel.", "use this as the bridge between charge work and local-GR source normalization."),
        ("DEC3774_3", "The current branch does not claim mu_extra=0 because none of the nine Q_i components is parent-signed or numerically filled.", "keep Newton/local-GR claim gates closed."),
    ]
    return [
        {
            **base(timestamp),
            "decision_id": decision_id,
            "decision": decision,
            "action": action,
            "claim_allowed": False,
        }
        for decision_id, decision, action in rows
    ]


def next_target_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "next_id": "NEXT3774_0",
            "target_doc": "3775-Y5-R2FR-no-harmonic-exterior-monopole-lemma-or-channel-support-certificates.md",
            "target_script": "scripts/Y5_R2FR_3775_no_harmonic_exterior_monopole_lemma_or_channel_support_certificates.py",
            "objective": "try to prove the support/no-harmonic certificate that kills boundary, projector, non-EH, memory, range, coupling, readout, EM/Poynting, and source/theta monopoles; otherwise emit channel-specific support certificates and bound blockers",
            "reason": "3774 reduces mu_extra to Q_i exterior monopoles; a no-harmonic support lemma is the cleanest route to close several channels without arbitrary tuning",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "MUEXTRA_SHELL_BALANCE_AND_COMPONENT_ZERO_THEOREM_DERIVED_COMPONENT_BOUNDS_EMITTED_NOT_PARENT_SIGNED",
            "summary": "3774 derives the exact shell-balance identity for the exterior measured-GM residual: mu_extra is the sum of nine named exterior/interior monopole channels, not a vague coupling hole. It proves the conditional no-extra-monopole theorem: a channel vanishes if it is same-Hilbert-source, has zero total extra interior monopole, is exact-divergence with zero exterior flux, is pure gauge/reference, and carries no exterior harmonic 1/r mode. The current branch still cannot claim mu_extra=0 because those support/no-harmonic/interior-monopole certificates are not parent-signed and component values remain placeholders.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3774 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3774 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("shell_identity", "mu_extra component shell identity emitted", any(row["identity_id"] == "MSB3774_2_component_split" for row in grouped["shell_identity"])),
        ("master_zero_theorem", "master no-extra-monopole theorem emitted", any(row["theorem_id"] == "MZT3774_0_master_zero" for row in grouped["zero_theorem"])),
        ("all_channels_present", "all nine 3773 mu_extra channels have component rows", len([row for row in grouped["component_bounds"] if row["component_id"] != "MCB3774_9_total"]) == 9),
        ("em_poynting_explicit", "EM/Poynting channel is explicit and not hidden", any(row["channel_symbol"] == "Q_EM_Poynting" for row in grouped["component_bounds"])),
        ("component_missing_nonclaim", "missing component values remain nonclaim", any(str(row["bound_or_value"]).startswith("MISSING_") and row["claim_allowed"] is False for row in grouped["component_bounds"])),
        ("numeric_envelopes_imported", "WEP/PPN/Gdot envelopes imported", all(any(str(row.get("bound_or_target", row.get("bound_or_value", ""))) == value for row in grouped["observable_matrix"] + grouped["component_bounds"]) for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15"})),
        ("zero_not_claimed", "current branch does not claim mu_extra zero", any(row["attempt_id"] == "MZA3774_10_verdict" and row["passes_clause"] is False for row in grouped["zero_attempt"])),
        ("claim_gates_closed", "Newton/local-GR claim remains closed", any(row["gate_id"] == "CG3774_8_Newton_GM_claim" and row["passed"] is False for row in grouped["claim_gates"])),
        ("next_target", "3775 no-harmonic exterior monopole target emitted", grouped["next_target"][0]["target_doc"] == "3775-Y5-R2FR-no-harmonic-exterior-monopole-lemma-or-channel-support-certificates.md"),
        ("no_formalization_leak", "no 3774 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3774*"))),
    ]
    return [
        {
            **base(timestamp),
            "validation_id": validation_id,
            "description": description,
            "result": "PASS" if result else "FAIL",
            "details": "" if result else "check failed",
        }
        for validation_id, description, result in checks
    ]


def render_doc(grouped: dict[str, list[dict[str, object]]]) -> str:
    lines = [
        "# 3774 - MuExtra Channel Zero Theorem Or Component Bound Vector",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "3774 does the thing we needed here: it stops treating `mu_extra` as fog. The exterior measured-GM residual is now a concrete Gauss-shell balance. Every possible extra monopole must be one of nine named `Q_i` components. The clean win condition is also concrete: prove each channel has no exterior harmonic monopole, or include it inside the same Hilbert source, or bound it.",
        "",
        "## Shell Balance Identity",
    ]
    for row in grouped["shell_identity"]:
        lines.append(f"- `{row['identity_id']}` `{row['status']}`: {row['statement']} Formula: `{row['formula']}`. Derivation: {row['derivation']}")
    lines.extend(["", "## Channel Zero Theorem"])
    for row in grouped["zero_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Derivation: {row['derivation']}")
    lines.extend(["", "## Current Zero Attempt"])
    for row in grouped["zero_attempt"]:
        lines.append(f"- `{row['attempt_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Evidence: {row['evidence']}. Consequence: {row['consequence']}.")
    lines.extend(["", "## Component Bound Vector"])
    for row in grouped["component_bounds"]:
        lines.append(f"- `{row['component_id']}` `{row['channel_symbol']}` -> `{row['residual_symbol']}`: {row['bound_formula']} <= `{row['bound_or_value']}` `{row['units']}`. Zero: {row['zero_condition']}.")
    lines.extend(["", "## Observable Projection Matrix"])
    for row in grouped["observable_matrix"]:
        lines.append(f"- `{row['matrix_id']}` `{row['observable']}`: {row['projection_formula']} <= `{row['bound_or_target']}`. Arena: {row['arena']}.")
    lines.extend(["", "## Claim Gates"])
    for row in grouped["claim_gates"]:
        lines.append(f"- `{row['gate_id']}` pass=`{row['passed']}`: {row['gate']} - {row['details']}")
    lines.extend(["", "## Decisions"])
    for row in grouped["decision_rows"]:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} Action: {row['action']}.")
    lines.extend(["", "## Next Target"])
    for row in grouped["next_target"]:
        lines.append(f"- `{row['target_doc']}`: {row['objective']}")
    lines.extend(["", "## Validation"])
    for row in grouped["validation"]:
        lines.append(f"- `{row['validation_id']}` `{row['result']}`: {row['description']}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    timestamp = stamp()
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    bounds = imported_bounds()

    grouped: dict[str, list[dict[str, object]]] = {
        "sources": source_register(timestamp),
        "shell_identity": shell_identity_rows(timestamp),
        "zero_theorem": zero_theorem_rows(timestamp),
        "zero_attempt": zero_attempt_rows(timestamp),
        "component_bounds": component_bound_rows(timestamp, bounds),
        "observable_matrix": observable_matrix_rows(timestamp, bounds),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["shell_identity"], grouped["shell_identity"])
    write_csv(OUTPUTS["zero_theorem"], grouped["zero_theorem"])
    write_csv(OUTPUTS["zero_attempt"], grouped["zero_attempt"])
    write_csv(OUTPUTS["component_bounds"], grouped["component_bounds"])
    write_csv(OUTPUTS["observable_matrix"], grouped["observable_matrix"])
    write_csv(OUTPUTS["claim_gates"], grouped["claim_gates"])
    write_csv(OUTPUTS["decision_rows"], grouped["decision_rows"])
    write_csv(OUTPUTS["next_target"], grouped["next_target"])
    write_csv(OUTPUTS["status"], grouped["status"])

    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])

    DOC_PATH.write_text(render_doc(grouped), encoding="utf-8")

    cache = Path(__file__).resolve().parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    failures = [row for row in grouped["validation"] if row["result"] != "PASS"]
    if failures:
        raise SystemExit(f"3774 validation failed: {failures}")
    print("wrote 3774 checkpoint: mu_extra shell balance and component zero theorem emitted")


if __name__ == "__main__":
    main()
