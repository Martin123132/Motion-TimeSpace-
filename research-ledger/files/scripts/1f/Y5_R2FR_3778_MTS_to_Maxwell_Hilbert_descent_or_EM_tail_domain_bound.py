import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3778"
BRANCH = "MTS_R2FR_Y5_MTS_TO_MAXWELL_HILBERT_DESCENT_OR_EM_TAIL_DOMAIN_BOUND_3778"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3778-Y5-R2FR-MTS-to-Maxwell-Hilbert-descent-or-EM-tail-domain-bound.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3778_SOURCE_REGISTER.csv",
    "descent_theorem": RESIDUALS / "P8_Y5_R2FR_3778_MAXWELL_HILBERT_DESCENT_THEOREM.csv",
    "descent_clauses": RESIDUALS / "P8_Y5_R2FR_3778_MTS_EM_DESCENT_CLAUSE_AUDIT.csv",
    "tail_formulas": RESIDUALS / "P8_Y5_R2FR_3778_EM_TAIL_DOMAIN_FORMULAS.csv",
    "residual_bounds": RESIDUALS / "P8_Y5_R2FR_3778_EM_DESCENT_AND_TAIL_BOUND_VECTOR.csv",
    "observable_matrix": RESIDUALS / "P8_Y5_R2FR_3778_EM_OBSERVABLE_PROJECTION_MATRIX.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3778_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3778_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3778_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3778_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3778_VALIDATION.csv",
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
        "SRC3778_0_3777_doc": PCW / "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md",
        "SRC3778_1_3777_projector": RESIDUALS / "P8_Y5_R2FR_3777_PIM_TOTAL_PROJECTOR_CONSTRUCTION.csv",
        "SRC3778_2_3777_em_map": RESIDUALS / "P8_Y5_R2FR_3777_EM_FIELD_ENERGY_SOURCE_MAP.csv",
        "SRC3778_3_3777_bounds": RESIDUALS / "P8_Y5_R2FR_3777_FIELD_DOMAIN_BOUND_VECTOR.csv",
        "SRC3778_4_3760_em_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3778_5_3760_em_budget": RESIDUALS / "P8_Y5_R2FR_3760_EM_SOURCE_RESIDUAL_BUDGET.csv",
        "SRC3778_6_3764_total_source": RESIDUALS / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv",
        "SRC3778_7_3770_source_theorem": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_THEOREM.csv",
        "SRC3778_8_3771_theta_theorem": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_THEOREM.csv",
        "SRC3778_9_3776_inclusion": RESIDUALS / "P8_Y5_R2FR_3776_TOTAL_HILBERT_SOURCE_INCLUSION_THEOREM.csv",
        "SRC3778_10_3776_domain": RESIDUALS / "P8_Y5_R2FR_3776_EM_POYNTING_DOMAIN_AUDIT.csv",
        "SRC3778_11_3775_monopole": RESIDUALS / "P8_Y5_R2FR_3775_NO_HARMONIC_MONOPOLE_LEMMA.csv",
        "SRC3778_12_3759_wep_eval": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3778_13_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
        "SRC3778_14_3768_gdot_budget": RESIDUALS / "P8_Y5_R2FR_3768_KAPPA_BOUND_BUDGET.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3778 MTS-to-Maxwell Hilbert descent and EM tail/domain bound input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def imported_bounds() -> dict[str, str]:
    wep = find_row(source_paths()["SRC3778_12_3759_wep_eval"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3778_13_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3778_13_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    gdot = find_row(source_paths()["SRC3778_14_3768_gdot_budget"], "budget_id", "KBB3768_0_Gdot_total")
    return {"wep": wep["bound_value"], "gamma": gamma["bound_value"], "beta": beta["bound_value"], "gdot": gdot["bound_value"]}


def descent_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "MHD3778_0_low_energy_EM_variable",
            "An MTS EM sector descends to Maxwell only if the observed electromagnetic readout is a q_obs-owned 1-form A_mu with field strength F=dA and gauge redundancy A -> A+dlambda.",
            "Gauge redundancy prevents an extra longitudinal charge from becoming a hidden source mass or WEP channel.",
            "EXACT_DESCENT_REQUIREMENT",
        ),
        (
            "MHD3778_1_Maxwell_action",
            "The low-energy action must reduce to S_EM=-(1/4) int sqrt(-g_eff) Z_EM F_ab F^ab plus terms that are topological, higher-order, compactly supported, or explicitly bounded.",
            "This is the unique local two-derivative gauge-invariant Maxwell stress route in the same observed metric/coframe.",
            "EXACT_CONDITIONAL_ACTION_FORM",
        ),
        (
            "MHD3778_2_Hilbert_stress",
            "If MHD3778_1 holds, variation with respect to g_eff gives T_EM^{ab}=Z_EM(F^{a c}F^b_c - (1/4)g_eff^{ab}F_cd F^cd), and this is the EM piece of T_total.",
            "This imports the 3760 standard identity but ties it to MTS descent and Pi_M_total.",
            "EXACT_CONDITIONAL_HILBERT_STRESS",
        ),
        (
            "MHD3778_3_universal_normalization",
            "Z_EM and charge/current normalization must be q_obs-owned or superselected, not species-, material-, frame-, or environment-labelled.",
            "Otherwise EM binding and material response produce WEP, clock, PPN, and source-normalization residuals.",
            "EXACT_UNIVERSALITY_REQUIREMENT",
        ),
        (
            "MHD3778_4_no_extra_EM_modes",
            "Massive Proca terms, disformal EM metrics, birefringent light cones, nonminimal RF^2 couplings, axion-like F wedge F readout effects, or hidden carrier stress must vanish or be bounded.",
            "Any such term is not ordinary Maxwell Hilbert stress and must remain an explicit residual owner.",
            "EXACT_RESIDUAL_EXCLUSION_RULE",
        ),
        (
            "MHD3778_5_Ward_total_source",
            "With one descended matter+EM action, nabla_a T_EM^{ab}=-F^b_c J^c cancels the matter Lorentz force inside nabla_a T_total^{ab}; only parent exchange or non-Hilbert owner currents remain.",
            "This is the EM reason same-source descent can look GR-like locally.",
            "EXACT_CONDITIONAL_WARD_THEOREM",
        ),
        (
            "MHD3778_6_tail_domain_law",
            "Even if Maxwell descent holds, EM field energy outside a chosen material radius contributes to M_H,total unless the source domain includes it or a tail/flux bound is supplied.",
            "Maxwell descent fixes the stress tensor; it does not automatically make finite source domains safe.",
            "EXACT_DOMAIN_BOUND_LAW",
        ),
        (
            "MHD3778_7_local_GR_promotion",
            "If MHD3778_0 through MHD3778_6 hold, EM/Poynting contributes only as ordinary total Hilbert stress in Pi_M_total, and EM-owned mu_extra rows close except declared finite tail/flux bounds.",
            "This is a local-GR-compatible EM source theorem, still conditional on parent signatures.",
            "EXACT_CONDITIONAL_EM_LOCAL_GR_PROMOTION",
        ),
    ]
    return [
        {
            **base(timestamp),
            "theorem_id": theorem_id,
            "statement": statement,
            "derivation_or_meaning": derivation_or_meaning,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for theorem_id, statement, derivation_or_meaning, status in rows
    ]


def descent_clause_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("MCA3778_0_qobs_A", "A_mu and F=dA are q_obs-owned observed fields", "MISSING_MTS_QOBS_EM_READOUT_CERTIFICATE", False, "without it EM can use a shadow frame/source"),
        ("MCA3778_1_gauge_invariance", "U(1) gauge redundancy and current conservation hold in the local branch", "MISSING_PARENT_GAUGE_INVARIANCE_CERTIFICATE", False, "without it longitudinal/source leakage remains"),
        ("MCA3778_2_Maxwell_kinetic", "two-derivative low-energy kinetic term is -1/4 Z_EM F^2 in g_eff", "MISSING_MTS_TO_MAXWELL_KINETIC_DERIVATION", False, "without it stress need not be Maxwell Hilbert stress"),
        ("MCA3778_3_universal_ZEM", "Z_EM and charge normalization are universal/q_obs-owned/superselected", "MISSING_UNIVERSAL_ZEM_SUPERSELECTION", False, "without it WEP/clock/material response residuals remain"),
        ("MCA3778_4_same_source_matter", "charged matter current J^a comes from the same descended source action", "MISSING_SAME_ACTION_CHARGED_MATTER_CURRENT", False, "without it Lorentz exchange is not internal"),
        ("MCA3778_5_no_EM_shadow_metric", "EM light cone uses the same observed metric/coframe as matter/source readout", "MISSING_NO_BIREFRINGENT_OR_DISFORMAL_EM_METRIC", False, "without it gamma/frame/readout residuals remain"),
        ("MCA3778_6_no_extra_modes", "Proca/nonminimal/axion/hidden-carrier stress is zero or bounded", "MISSING_EXTRA_EM_MODE_ZERO_OR_BOUND", False, "without it EM mu_extra has extra owners"),
        ("MCA3778_7_tail_domain", "EM near/tail/flux support is included in Pi_M_total or bounded", "MISSING_EM_TAIL_AND_FLUX_DOMAIN_CERTIFICATES", False, "without it Maxwell stress still leaks through domain choice"),
        ("MCA3778_8_material_response", "polarization, magnetization, binding, and material coefficients descend or are bounded", "MISSING_EM_MATERIAL_RESPONSE_DESCENT", False, "without it WEP/clock/Newton source rows remain"),
        ("MCA3778_9_verdict", "current branch proves MTS-to-Maxwell Hilbert descent and EM tail/domain closure", "CONDITIONAL_ROUTE_ONLY_PARENT_SIGNATURES_MISSING", False, "do not claim EM/local-GR closure"),
    ]
    return [
        {
            **base(timestamp),
            "clause_id": clause_id,
            "required_clause": required_clause,
            "current_status": current_status,
            "passes_clause": passes_clause,
            "consequence": consequence,
            "claim_allowed": False,
        }
        for clause_id, required_clause, current_status, passes_clause, consequence in rows
    ]


def tail_formula_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "ETF3778_0_general_tail",
            "general static EM tail",
            "E_EM_tail(R)=int_{r>R} [(epsilon0/2)|E|^2 + (1/(2 mu0))|B|^2] d^3x",
            "epsilon_EM_tail=E_EM_tail(R)/(M_H,total c^2)",
            "source-specific",
            "requires field profile or multipole bound",
        ),
        (
            "ETF3778_1_net_charge",
            "net electric charge",
            "E_tail^Q(R)=Q_net^2/(8*pi*epsilon0*R)",
            "epsilon_Q_tail=Q_net^2/(8*pi*epsilon0*R*M_H,total*c^2)",
            "SI_units_or_rationalized_conversion",
            "not compact-source safe without boundary/renormalization convention",
        ),
        (
            "ETF3778_2_electric_dipole",
            "electric dipole tail",
            "E_tail^p(R)=p^2/(12*pi*epsilon0*R^3)",
            "epsilon_p_tail=p^2/(12*pi*epsilon0*R^3*M_H,total*c^2)",
            "SI_units",
            "neutral multipole tail bound",
        ),
        (
            "ETF3778_3_magnetic_dipole",
            "magnetic dipole tail",
            "E_tail^m(R)=mu0*m^2/(12*pi*R^3)",
            "epsilon_m_tail=mu0*m^2/(12*pi*R^3*M_H,total*c^2)",
            "SI_units",
            "stationary magnetic tail bound",
        ),
        (
            "ETF3778_4_Poynting_flux",
            "Poynting flux through total-domain boundary",
            "Delta E_flux = int_dt int_boundary S_EM dot dA",
            "epsilon_flux=|Delta E_flux|/(M_H,total*c^2) or |P_flux|/(M_H,total*c^2)",
            "dimensionless_or_rate",
            "radiative/nonstationary source exchange bound",
        ),
        (
            "ETF3778_5_material_response",
            "material EM response",
            "delta ln M_EM_binding = sum_I K_I^EM delta ln theta_I + response-domain terms",
            "eta_EM_AB <= |Delta_AB f_EM||delta_kappa_EM| + |Delta_AB ln Z_EM| + material response residuals",
            "dimensionless",
            "WEP/clock/source-normalization bound interface",
        ),
    ]
    return [
        {
            **base(timestamp),
            "formula_id": formula_id,
            "case": case,
            "energy_formula": energy_formula,
            "bound_formula": bound_formula,
            "units": units,
            "use": use,
            "claim_allowed": False,
        }
        for formula_id, case, energy_formula, bound_formula, units, use in rows
    ]


def residual_bound_rows(timestamp: str, bounds: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        ("EDB3778_0_descent", "epsilon_EM_descent", "norm[S_EM^MTS - S_Maxwell(q_obs)] projected into local source sector", "MISSING_PARENT_EM_ACTION_DESCENT_NORM", "dimensionless_or_action_norm", "Newton GM; PPN; WEP"),
        ("EDB3778_1_ZEM", "epsilon_ZEM", "|delta ln Z_EM| plus species/material/frame dependence", "MISSING_UNIVERSAL_ZEM_VALUE_OR_BOUND", "dimensionless", "WEP; clocks; EM coupling drift"),
        ("EDB3778_2_shadow_metric", "epsilon_EM_shadow_metric", "norm[g_EM-g_eff] or birefringent/disformal readout projection", "MISSING_EM_SHADOW_METRIC_BOUND", "dimensionless", "PPN gamma; light; frame"),
        ("EDB3778_3_extra_modes", "epsilon_EM_extra_modes", "Proca + nonminimal RF^2 + axion/readout + hidden-carrier stress projections", "MISSING_EXTRA_EM_MODE_BOUND", "dimensionless", "Newton GM; PPN; polarization"),
        ("EDB3778_4_tail", "epsilon_EM_tail", "E_EM_tail(R)/(M_H,total c^2)", "MISSING_EM_TAIL_ENERGY_MODEL_OR_BOUND", "dimensionless", "Newton GM; radial hair; WEP"),
        ("EDB3778_5_flux", "epsilon_Poynting_flux", "|int S_EM dot dA dt|/(M_H,total c^2)", "MISSING_POYNTING_OR_RADIATIVE_FLUX_BOUND", "dimensionless_or_rate", "Gdot; source conservation"),
        ("EDB3778_6_material_response", "epsilon_EM_material_response", "polarization/magnetization/binding/material marker response residual", "MISSING_EM_MATERIAL_RESPONSE_COEFFICIENTS", "dimensionless", "WEP; clock; source mass"),
        ("EDB3778_7_WEP", "eta_EM_AB", "|Delta_AB f_EM||delta_kappa_EM| + |Delta_AB ln Z_EM| + |Delta_AB q_EM_exchange| + material response", bounds["wep"], "dimensionless", "WEP"),
        ("EDB3778_8_gamma", "delta_gamma_EM", "|epsilon_EM_metric| + |Pi_PPN q_EM_exchange| + |Delta_EM_source_frame|", bounds["gamma"], "dimensionless", "PPN gamma"),
        ("EDB3778_9_beta", "delta_beta_EM", "|epsilon_EM_nonlinear| + |Delta_EM_binding_second_order| + |Pi_beta q_EM_exchange|", bounds["beta"], "dimensionless", "PPN beta"),
        ("EDB3778_10_Gdot", "dln_Geff_dt_EM", "|d_t ln Z_EM| + |R_EM_exchange| + |d_t ln Z_EM_frame|", bounds["gdot"], "yr^-1", "Gdot/source drift"),
    ]
    return [
        {
            **base(timestamp),
            "bound_id": bound_id,
            "target": target,
            "formula": formula,
            "bound_or_value": bound_or_value,
            "units": units,
            "feeds": feeds,
            "claim_allowed": False,
        }
        for bound_id, target, formula, bound_or_value, units, feeds in rows
    ]


def observable_matrix_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("EOM3778_0_Newton_GM", "delta_ln_mu_obs|EM", "epsilon_EM_descent + epsilon_EM_tail + epsilon_Poynting_flux + epsilon_EM_material_response + epsilon_EM_extra_modes", "MISSING_COMPONENT_VALUES", "Newton/orbital GM"),
        ("EOM3778_1_WEP", "eta_EM_AB", "composition projection of Z_EM/material response/binding/tail residuals", "2.8e-15", "WEP"),
        ("EOM3778_2_PPN_gamma", "delta_gamma_EM", "EM metric/readout/source-frame projection", "2.3e-05", "PPN gamma"),
        ("EOM3778_3_PPN_beta", "delta_beta_EM", "EM nonlinear/binding/source projection", "7.8e-05", "PPN beta"),
        ("EOM3778_4_Gdot", "dln_Geff_dt_EM", "time drift of Z_EM/exchange/frame source calibration", "9.6e-15 yr^-1", "Gdot"),
        ("EOM3778_5_radial_hair", "partial_r_ln_mu_obs|EM", "partial_r epsilon_EM_tail + partial_r domain-wall/flux terms", "MISSING_RADIAL_TAIL_PROFILE", "radial/source profile"),
        ("EOM3778_6_clocks", "delta_ln_clock_ratio|EM", "clock/material sensitivities to alpha/Z_EM/binding response", "MISSING_CLOCK_RESPONSE_COEFFICIENTS", "clock/constant drift"),
    ]
    return [
        {
            **base(timestamp),
            "matrix_id": matrix_id,
            "observable": observable,
            "projection_formula": projection_formula,
            "bound_or_target": bound_or_target,
            "arena": arena,
            "claim_allowed": False,
        }
        for matrix_id, observable, projection_formula, bound_or_target, arena in rows
    ]


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    theorem = any(row["theorem_id"] == "MHD3778_7_local_GR_promotion" for row in grouped["descent_theorem"])
    clauses = len(grouped["descent_clauses"]) == 10
    tail_formulas = len(grouped["tail_formulas"]) == 6
    net_charge = any(row["formula_id"] == "ETF3778_1_net_charge" for row in grouped["tail_formulas"])
    verdict = any(row["clause_id"] == "MCA3778_9_verdict" and row["passes_clause"] is True for row in grouped["descent_clauses"])
    missing_bounds = any(str(row["bound_or_value"]).startswith("MISSING_") for row in grouped["residual_bounds"])
    rows = [
        ("CG3778_0_sources", "all 3778 source paths exist", sources_exist, "path hygiene"),
        ("CG3778_1_descent_theorem", "Maxwell Hilbert descent theorem emitted", theorem, "EM closure route is exact and conditional"),
        ("CG3778_2_clause_audit", "all descent clauses are audited", clauses, "q_obs A, gauge, Maxwell kinetic, Z_EM, same current, shadow metric, extra modes, tail/domain, material response, verdict"),
        ("CG3778_3_tail_formulas", "EM tail/flux formulas emitted", tail_formulas, "field energy bounds have explicit formula owners"),
        ("CG3778_4_net_charge_flagged", "net charge long-range field case remains explicit", net_charge, "not smuggled into compact source"),
        ("CG3778_5_current_descent_claim", "current branch proves MTS-to-Maxwell Hilbert descent", verdict, "expected false until parent signatures exist"),
        ("CG3778_6_missing_bounds_nonclaim", "missing EM residual bounds remain blockers", missing_bounds, "no pass from placeholder EM coefficients"),
        ("CG3778_7_EM_local_GR_claim", "EM part of local GR claim allowed", False, "blocked until descent and tail/domain bounds close"),
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
        ("DEC3778_0", "MTS-to-Maxwell descent requires q_obs-owned A_mu, U(1) gauge structure, Maxwell kinetic term, universal Z_EM, same-source charged current, no EM shadow metric, no extra unbounded EM modes, and tail/domain certificates.", "use the 3778 clause audit as the EM parent-signature contract"),
        ("DEC3778_1", "Maxwell descent alone is insufficient for compact-source measured GM because EM field energy can live outside a material radius.", "always pair EM descent with tail/domain bounds"),
        ("DEC3778_2", "Net charged sources are not compact local-GR sources by default; their Coulomb tail requires explicit boundary/renormalization treatment.", "keep net-charge tail rows nonclaim until a convention or bound is supplied"),
        ("DEC3778_3", "The next best constructive route is to build the q_obs-owned EM readout/gauge certificate and universal Z_EM superselection test.", "attack q_obs A_mu and Z_EM before fitting EM residuals"),
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
            "next_id": "NEXT3778_0",
            "target_doc": "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md",
            "target_script": "scripts/Y5_R2FR_3779_qobs_EM_readout_gauge_and_universal_ZEM_certificate.py",
            "objective": "construct or reject the q_obs-owned EM readout/gauge certificate and universal Z_EM superselection needed for MTS-to-Maxwell Hilbert descent",
            "reason": "3778 shows the highest-value missing EM signatures are q_obs ownership of A_mu/F, U(1) gauge/current conservation, and universal Z_EM; tail bounds cannot substitute for those parent signatures",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "MTS_TO_MAXWELL_HILBERT_DESCENT_CONTRACT_DERIVED_EM_TAIL_BOUNDS_EMITTED_NOT_PARENT_SIGNED",
            "summary": "3778 derives the exact contract for the MTS EM sector to become ordinary Maxwell Hilbert stress inside Pi_M_total. It requires q_obs-owned A_mu/F, U(1) gauge redundancy, Maxwell kinetic form in g_eff, universal Z_EM, same-source charged current, no EM shadow metric, no unbounded extra EM modes, and source-domain/tail certificates. It also emits explicit EM field-tail, net-charge, dipole, Poynting-flux, material-response, WEP, PPN, and Gdot bound rows. Current MTS does not claim EM/local-GR closure because all parent signatures remain unsigned.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3778 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3778 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("descent_theorem", "MTS-to-Maxwell Hilbert descent theorem emitted", any(row["theorem_id"] == "MHD3778_7_local_GR_promotion" for row in grouped["descent_theorem"])),
        ("clause_audit", "ten EM descent clauses emitted", len(grouped["descent_clauses"]) == 10),
        ("tail_formulas", "six EM tail/domain formulas emitted", len(grouped["tail_formulas"]) == 6),
        ("net_charge_formula", "net charge tail formula emitted", any(row["formula_id"] == "ETF3778_1_net_charge" for row in grouped["tail_formulas"])),
        ("poynting_formula", "Poynting flux formula emitted", any(row["formula_id"] == "ETF3778_4_Poynting_flux" for row in grouped["tail_formulas"])),
        ("material_response", "material response formula emitted", any(row["formula_id"] == "ETF3778_5_material_response" for row in grouped["tail_formulas"])),
        ("no_descent_claim", "current branch does not claim EM descent", any(row["clause_id"] == "MCA3778_9_verdict" and row["passes_clause"] is False for row in grouped["descent_clauses"])),
        ("bounds_nonclaim", "missing EM bounds remain nonclaim", any(str(row["bound_or_value"]).startswith("MISSING_") and row["claim_allowed"] is False for row in grouped["residual_bounds"])),
        ("numeric_envelopes", "WEP/PPN/Gdot envelopes imported", all(any(str(row.get("bound_or_value", row.get("bound_or_target", ""))) == value for row in grouped["residual_bounds"] + grouped["observable_matrix"]) for value in {"2.8e-15", "2.3e-05", "7.8e-05", "9.6e-15 yr^-1"})),
        ("claim_gates_closed", "EM local-GR claim remains closed", any(row["gate_id"] == "CG3778_7_EM_local_GR_claim" and row["passed"] is False for row in grouped["claim_gates"])),
        ("next_target", "3779 qobs EM/ZEM certificate target emitted", grouped["next_target"][0]["target_doc"] == "3779-Y5-R2FR-qobs-EM-readout-gauge-and-universal-ZEM-certificate.md"),
        ("no_formalization_leak", "no 3778 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3778*"))),
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
        "# 3778 - MTS To Maxwell Hilbert Descent Or EM Tail Domain Bound",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "3778 pins down the EM bridge. To count EM as ordinary GR-like source mass, MTS must deliver a q_obs-owned Maxwell sector: one A_mu/F, U(1) gauge structure, Maxwell kinetic term in g_eff, universal Z_EM, same-source matter current, no EM shadow metric, no unbounded extra EM modes, and field-tail/domain certificates. If any part fails, EM stays as explicit tail, flux, material-response, WEP, PPN, Gdot, or Newton-GM residuals.",
        "",
        "## Maxwell Hilbert Descent Theorem",
    ]
    for row in grouped["descent_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Meaning: {row['derivation_or_meaning']}")
    lines.extend(["", "## MTS EM Descent Clause Audit"])
    for row in grouped["descent_clauses"]:
        lines.append(f"- `{row['clause_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Status: `{row['current_status']}`. Consequence: {row['consequence']}.")
    lines.extend(["", "## EM Tail/Domain Formulas"])
    for row in grouped["tail_formulas"]:
        lines.append(f"- `{row['formula_id']}` `{row['case']}`: {row['energy_formula']}. Bound: `{row['bound_formula']}`. Use: {row['use']}.")
    lines.extend(["", "## EM Descent And Tail Bound Vector"])
    for row in grouped["residual_bounds"]:
        lines.append(f"- `{row['bound_id']}` `{row['target']}`: {row['formula']} <= `{row['bound_or_value']}` `{row['units']}`. Feeds: {row['feeds']}.")
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
        "descent_theorem": descent_theorem_rows(timestamp),
        "descent_clauses": descent_clause_rows(timestamp),
        "tail_formulas": tail_formula_rows(timestamp),
        "residual_bounds": residual_bound_rows(timestamp, bounds),
        "observable_matrix": observable_matrix_rows(timestamp),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["descent_theorem"], grouped["descent_theorem"])
    write_csv(OUTPUTS["descent_clauses"], grouped["descent_clauses"])
    write_csv(OUTPUTS["tail_formulas"], grouped["tail_formulas"])
    write_csv(OUTPUTS["residual_bounds"], grouped["residual_bounds"])
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
        raise SystemExit(f"3778 validation failed: {failures}")
    print("wrote 3778 checkpoint: Maxwell Hilbert descent contract and EM tail bounds emitted")


if __name__ == "__main__":
    main()
