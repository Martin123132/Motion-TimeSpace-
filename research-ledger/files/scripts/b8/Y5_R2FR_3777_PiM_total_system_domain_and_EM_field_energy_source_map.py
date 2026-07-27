import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3777"
BRANCH = "MTS_R2FR_Y5_PIM_TOTAL_SYSTEM_DOMAIN_AND_EM_FIELD_ENERGY_SOURCE_MAP_3777"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3777_SOURCE_REGISTER.csv",
    "projector": RESIDUALS / "P8_Y5_R2FR_3777_PIM_TOTAL_PROJECTOR_CONSTRUCTION.csv",
    "domain_rules": RESIDUALS / "P8_Y5_R2FR_3777_TOTAL_SYSTEM_DOMAIN_RULES.csv",
    "em_source_map": RESIDUALS / "P8_Y5_R2FR_3777_EM_FIELD_ENERGY_SOURCE_MAP.csv",
    "closure_attempt": RESIDUALS / "P8_Y5_R2FR_3777_PIM_TOTAL_CLOSURE_ATTEMPT.csv",
    "bound_vector": RESIDUALS / "P8_Y5_R2FR_3777_FIELD_DOMAIN_BOUND_VECTOR.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3777_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3777_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3777_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3777_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3777_VALIDATION.csv",
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
        "SRC3777_0_3776_doc": PCW / "3776-Y5-R2FR-total-Hilbert-source-inclusion-EM-Poynting-and-interior-monopole-closure.md",
        "SRC3777_1_3776_inclusion_theorem": RESIDUALS / "P8_Y5_R2FR_3776_TOTAL_HILBERT_SOURCE_INCLUSION_THEOREM.csv",
        "SRC3777_2_3776_domain_audit": RESIDUALS / "P8_Y5_R2FR_3776_EM_POYNTING_DOMAIN_AUDIT.csv",
        "SRC3777_3_3776_reclassification": RESIDUALS / "P8_Y5_R2FR_3776_MUEXTRA_RECLASSIFICATION_VECTOR.csv",
        "SRC3777_4_3776_bounds": RESIDUALS / "P8_Y5_R2FR_3776_REMAINING_BOUND_VECTOR.csv",
        "SRC3777_5_3775_monopole_lemma": RESIDUALS / "P8_Y5_R2FR_3775_NO_HARMONIC_MONOPOLE_LEMMA.csv",
        "SRC3777_6_3775_certificates": RESIDUALS / "P8_Y5_R2FR_3775_CHANNEL_SUPPORT_CERTIFICATE_ATTEMPT.csv",
        "SRC3777_7_3764_total_source": RESIDUALS / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv",
        "SRC3777_8_3760_EM_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3777_9_3770_source_theorem": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_THEOREM.csv",
        "SRC3777_10_3771_theta_theorem": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_THEOREM.csv",
        "SRC3777_11_3773_surface_theorem": RESIDUALS / "P8_Y5_R2FR_3773_HAMILTONIAN_GAUSS_SURFACE_THEOREM.csv",
        "SRC3777_12_3774_component_bounds": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_COMPONENT_BOUND_VECTOR.csv",
        "SRC3777_13_3759_wep_eval": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3777_14_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3777 Pi_M_total source projector and total-system domain input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def imported_bounds() -> dict[str, str]:
    wep = find_row(source_paths()["SRC3777_13_3759_wep_eval"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3777_14_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3777_14_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    return {"wep": wep["bound_value"], "gamma": gamma["bound_value"], "beta": beta["bound_value"]}


def projector_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "PIM3777_0_observed_time_charge",
            "Choose the same observed time generator xi/tau_obs used by the Hamiltonian/Gauss charge and slow-orbit readout.",
            "If the mass projector uses a different time, M_H,total can differ from the orbital monopole by a frame/readout residual.",
            "SETUP_REQUIRED",
        ),
        (
            "PIM3777_1_total_current",
            "Define J_M,total^a[xi] := -(T_total^{a}{}_{b} xi^b)/c^2 for the descended total Hilbert stress T_total=T_matter+T_EM+T_binding+T_apparatus+T_int.",
            "This is the total active mass-energy current. EM/Poynting is included through T_EM, not by adding a separate fifth-force charge.",
            "EXACT_CONDITIONAL_TOTAL_CURRENT_DEFINITION",
        ),
        (
            "PIM3777_2_projector_definition",
            "Pi_M_total maps a q_obs source history to M_H,total[W,Sigma,xi] = int_{Sigma cap D_total(W)} n_a J_M,total^a[xi] dSigma plus declared finite tail terms that are not cut by D_total.",
            "The projector is a bookkeeping map from total stress to monopole source charge; it is not an empirical fit of GM.",
            "EXACT_CONDITIONAL_PROJECTOR_DEFINITION",
        ),
        (
            "PIM3777_3_domain_closure",
            "D_total must include matter support, descended EM field support assigned to the source, binding/interaction support, apparatus/readout support, and source/theta normalization support up to a boundary where total flux is zero or bounded.",
            "This prevents matter-only cuts from manufacturing Q_EM_Poynting or Q_source_theta.",
            "EXACT_TOTAL_SYSTEM_DOMAIN_RULE",
        ),
        (
            "PIM3777_4_no_double_counting",
            "Any stress included in M_H,total must be removed from mu_extra; any stress not included must stay in a named Q_i row with a bound.",
            "The same field energy cannot be both source mass and extra monopole.",
            "EXACT_NO_DOUBLE_COUNTING_RULE",
        ),
        (
            "PIM3777_5_conservation_condition",
            "If xi is stationary/Killing in the local exterior, total source descent holds, parent exchange is silent, and the total-domain side flux vanishes, then d(Pi_M_total J_M,total)=0 outside the chosen total source.",
            "This is the bridge from source projector to Hamiltonian/Gauss equality.",
            "EXACT_CONDITIONAL_CLOSED_TOTAL_FLUX_THEOREM",
        ),
        (
            "PIM3777_6_measured_GM_condition",
            "If PIM3777_1 through PIM3777_5 are parent-signed and the 3773 Hamiltonian/Gauss charge equality uses Pi_M_total, then mu_obs=G_eff M_H,total up to the remaining non-total-source Q_i channels.",
            "This is the constructive measured-GM route after rejecting matter-only mass.",
            "EXACT_CONDITIONAL_MEASURED_GM_PROMOTION",
        ),
    ]
    return [
        {
            **base(timestamp),
            "projector_id": projector_id,
            "statement": statement,
            "derivation_or_meaning": derivation_or_meaning,
            "status": status,
            "parent_signed": False,
            "claim_allowed": False,
        }
        for projector_id, statement, derivation_or_meaning, status in rows
    ]


def domain_rule_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "TSD3777_0_matter_core",
            "matter core",
            "included",
            "material rest mass, kinetic energy, pressure/internal stress, and matter charge current support",
            "MISSING_PARENT_SIGNED_QOBS_MATTER_SOURCE_DOMAIN",
        ),
        (
            "TSD3777_1_EM_near_field",
            "EM near field",
            "included_if_descended",
            "Coulomb/magnetic/dipole near-field energy and stress assigned to the same source system",
            "MISSING_EM_DESCENT_AND_NEAR_FIELD_DOMAIN",
        ),
        (
            "TSD3777_2_EM_tail",
            "EM exterior tail",
            "include_or_bound",
            "long-range field energy outside the practical source surface; neutral multipole tails may be bounded by E_tail(R)/M_H c^2, net-charge tails require explicit treatment",
            "MISSING_EM_TAIL_CLASS_AND_BOUND",
        ),
        (
            "TSD3777_3_Poynting_flux",
            "Poynting flux/momentum",
            "include_and_check_flux",
            "stationary circulating field momentum belongs to T_EM; radiative or nonstationary flux through the boundary must be zero or bounded",
            "MISSING_POYNTING_BOUNDARY_FLUX_CERTIFICATE",
        ),
        (
            "TSD3777_4_binding_interaction",
            "binding and interaction stress",
            "included_if_descended",
            "EM/nuclear/material binding and interaction stress that changes inertial and active mass",
            "MISSING_BINDING_INTERACTION_SOURCE_DESCENT",
        ),
        (
            "TSD3777_5_apparatus_readout",
            "apparatus/readout support",
            "include_or_exclude_with_readout_bound",
            "readout devices, clock support, and calibration stress only when they are part of the measured source system",
            "MISSING_APPARATUS_DOMAIN_DECLARATION",
        ),
        (
            "TSD3777_6_theta_source_norm",
            "source/theta normalization support",
            "included_if_superselected_or_qobs_owned",
            "constant/material-marker source normalization that fixes active/passive/inertial mass equality",
            "MISSING_THETA_SOURCE_NORMALIZATION_DESCENT",
        ),
        (
            "TSD3777_7_boundary_surface",
            "total-domain boundary",
            "zero_or_bound_flux",
            "boundary selected so n_a T_total^{ab} xi_b has no unowned side flux, or the flux is a named residual",
            "MISSING_TOTAL_DOMAIN_WALL_FLUX_CERTIFICATE",
        ),
    ]
    return [
        {
            **base(timestamp),
            "domain_rule_id": domain_rule_id,
            "support_class": support_class,
            "domain_action": domain_action,
            "definition": definition,
            "current_status": current_status,
            "claim_allowed": False,
        }
        for domain_rule_id, support_class, domain_action, definition, current_status in rows
    ]


def em_source_map_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "ESM3777_0_descended_Maxwell",
            "descended Maxwell field",
            "T_EM^{ab}=Z_EM(F^{a c}F^b_c - 1/4 g_eff^{ab}F^2)",
            "M_H,total",
            "requires MTS parent descent to same q_obs Maxwell Hilbert stress",
            "MISSING_MTS_EM_MAXWELL_DESCENT",
        ),
        (
            "ESM3777_1_neutral_bound_source",
            "neutral bound source",
            "near-field EM/binding energy plus multipole tail",
            "M_H,total plus tail bound",
            "tail energy must be included up to boundary or bounded by E_tail(R)/M_H c^2",
            "MISSING_NEUTRAL_EM_TAIL_BOUND",
        ),
        (
            "ESM3777_2_net_charge_source",
            "net charged source",
            "Coulomb 1/r field with field energy outside every finite material radius",
            "explicit field-domain problem",
            "not safe as compact local source unless total field energy/renormalization and boundary convention are signed",
            "MISSING_NET_CHARGE_FIELD_ENERGY_RENORMALIZATION_OR_BOUND",
        ),
        (
            "ESM3777_3_magnetic_stationary",
            "stationary magnetic/source current",
            "magnetic field energy and possible circulating Poynting momentum",
            "M_H,total if same action and no net boundary flux",
            "T_EM^{0i} is included; net Poynting flux through boundary must vanish or be bounded",
            "MISSING_STATIONARY_POYNTING_FLUX_CERTIFICATE",
        ),
        (
            "ESM3777_4_radiative_EM",
            "radiative EM field",
            "outgoing/incoming radiation crossing source boundary",
            "not closed source mass without flux term",
            "radiation flux is a time-dependent source exchange term, not a static Newton GM mass",
            "MISSING_RADIATIVE_FLUX_BOUND",
        ),
        (
            "ESM3777_5_material_response",
            "material response/binding markers",
            "polarization, magnetization, nuclear/EM binding fractions, and material coefficients",
            "M_H,total if theta/source markers descend",
            "otherwise composition-dependent WEP/clock/Newton residual",
            "MISSING_MATERIAL_RESPONSE_THETA_DESCENT",
        ),
    ]
    return [
        {
            **base(timestamp),
            "map_id": map_id,
            "field_class": field_class,
            "source_content": source_content,
            "classification": classification,
            "condition": condition,
            "current_status": current_status,
            "claim_allowed": False,
        }
        for map_id, field_class, source_content, classification, condition, current_status in rows
    ]


def closure_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("PCA3777_0_projector_defined", "Pi_M_total has a precise conditional definition", "PIM3777_2 emitted", True, "construction route exists"),
        ("PCA3777_1_domain_rules_defined", "total-system domain rules cover matter, EM, tail, Poynting, binding, apparatus, theta, and boundary", "TSD3777_0 through TSD3777_7 emitted", True, "source support map is explicit"),
        ("PCA3777_2_no_double_counting", "included stress is removed from mu_extra and excluded stress remains Q_i", "PIM3777_4 emitted", True, "bookkeeping trap is closed at formula level"),
        ("PCA3777_3_EM_parent_descent", "MTS parent signs low-energy EM descends to universal Maxwell Hilbert stress", "3760 EMT3760_4 still unsigned", False, "Pi_M_total cannot yet claim EM inclusion"),
        ("PCA3777_4_EM_tail_bound", "EM exterior tail class and energy bound are supplied", "ESM3777_1/2/3/4 remain missing tail/flux certificates", False, "Q_EM_Poynting remains live"),
        ("PCA3777_5_theta_domain", "source/theta normalization support descends or is superselected", "3771 CMT3771_2 remains parent-unsigned", False, "Q_source_theta remains live"),
        ("PCA3777_6_boundary_flux", "total-domain boundary has zero or bounded side flux", "TSD3777_7 remains missing wall-flux certificate", False, "domain-wall residual remains live"),
        ("PCA3777_7_verdict", "current branch closes Pi_M_total for measured GM", "projector/domain construction exists but EM descent, tail bounds, theta silence, and boundary flux are unsigned", False, "do not claim Newton/local-GR closure"),
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


def bound_vector_rows(timestamp: str, bounds: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        (
            "FDB3777_0_EM_tail",
            "epsilon_EM_tail",
            "E_EM_tail(R)/(M_H,total c^2)",
            "MISSING_EM_TAIL_ENERGY_MODEL_OR_BOUND",
            "dimensionless",
            "Newton GM; radial hair; WEP",
        ),
        (
            "FDB3777_1_Poynting_flux",
            "epsilon_Poynting_flux",
            "|int_boundary S_EM dot dA dt|/(M_H,total c^2)",
            "MISSING_POYNTING_FLUX_BOUND",
            "dimensionless_or_rate",
            "Gdot; source conservation; radiation",
        ),
        (
            "FDB3777_2_total_domain_wall",
            "epsilon_total_domain_wall",
            "|int_wall n_a T_total^{ab} xi_b|/M_H,total",
            "MISSING_TOTAL_DOMAIN_WALL_FLUX_BOUND",
            "dimensionless",
            "Hamiltonian/Gauss; radial hair",
        ),
        (
            "FDB3777_3_theta_source_norm",
            "epsilon_theta_source_norm",
            "|delta M_source_norm|/M_H,total",
            "MISSING_THETA_SOURCE_NORMALIZATION_DESCENT_OR_BOUND",
            "dimensionless",
            "Newton GM; WEP; clock",
        ),
        (
            "FDB3777_4_WEP_domain",
            "eta_domain_AB",
            "C_EM epsilon_EM_tail + C_theta epsilon_theta_source_norm + C_mat epsilon_material_response",
            bounds["wep"],
            "dimensionless",
            "WEP",
        ),
        (
            "FDB3777_5_gamma_domain",
            "delta_gamma_domain",
            "C_gamma_EM epsilon_EM_tail + C_gamma_domain epsilon_total_domain_wall",
            bounds["gamma"],
            "dimensionless",
            "PPN gamma",
        ),
        (
            "FDB3777_6_beta_domain",
            "delta_beta_domain",
            "C_beta_EM epsilon_EM_tail + C_beta_theta epsilon_theta_source_norm + C_beta_bound epsilon_binding",
            bounds["beta"],
            "dimensionless",
            "PPN beta",
        ),
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


def claim_gate_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    sources_exist = all(Path(str(row["source_path"])).exists() for row in grouped["sources"])
    projector_defined = any(row["projector_id"] == "PIM3777_2_projector_definition" for row in grouped["projector"])
    domain_complete = len(grouped["domain_rules"]) == 8
    em_map_complete = len(grouped["em_source_map"]) == 6
    no_double_count = any(row["projector_id"] == "PIM3777_4_no_double_counting" for row in grouped["projector"])
    verdict = any(row["attempt_id"] == "PCA3777_7_verdict" and row["passes_clause"] is True for row in grouped["closure_attempt"])
    missing_bounds = any(str(row["bound_or_value"]).startswith("MISSING_") for row in grouped["bound_vector"])
    rows = [
        ("CG3777_0_sources", "all 3777 source paths exist", sources_exist, "path hygiene"),
        ("CG3777_1_projector_defined", "Pi_M_total conditional projector is defined", projector_defined, "constructive route exists"),
        ("CG3777_2_domain_rules", "total-system domain rules cover required support classes", domain_complete, "matter-only tube replaced by total-domain map"),
        ("CG3777_3_EM_source_map", "EM field classes are mapped to include/bound decisions", em_map_complete, "neutral, charged, stationary, radiative, material-response cases separated"),
        ("CG3777_4_no_double_counting", "no-double-counting rule emitted", no_double_count, "stress cannot be both M_H,total and mu_extra"),
        ("CG3777_5_current_closure", "current branch closes Pi_M_total for measured GM", verdict, "expected false until EM descent/tail/theta/flux certificates exist"),
        ("CG3777_6_missing_bounds_nonclaim", "missing field/domain bounds remain blockers", missing_bounds, "no pass from placeholder tail/domain rows"),
        ("CG3777_7_Newton_GM_claim", "measured-GM Newton claim allowed", False, "blocked until Pi_M_total clauses close or bounds are numeric"),
        ("CG3777_8_local_GR_claim", "local GR claim allowed", False, "blocked until total source, EH operator, charge equality, and readout close"),
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
        ("DEC3777_0", "Pi_M_total is now an explicit conditional projector over total Hilbert stress and a declared total-system domain, not a vague same-source phrase.", "use PIM3777_2/PIM3777_3 as the source-normalization contract"),
        ("DEC3777_1", "EM field support must be classified: neutral bound tails, net charge tails, stationary Poynting momentum, and radiative flux have different closure/bound rules.", "do not treat all EM stress as one generic residual"),
        ("DEC3777_2", "No double counting is mandatory: stress included in M_H,total must be removed from mu_extra; stress not included must remain a named Q_i bound.", "protect the measured-GM bridge from fitted bookkeeping"),
        ("DEC3777_3", "The next physical proof target is MTS-to-Maxwell Hilbert descent with universal Z_EM and source/tail domain certificates.", "attack EM descent and tail/flux bounds next"),
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
            "next_id": "NEXT3777_0",
            "target_doc": "3778-Y5-R2FR-MTS-to-Maxwell-Hilbert-descent-or-EM-tail-domain-bound.md",
            "target_script": "scripts/Y5_R2FR_3778_MTS_to_Maxwell_Hilbert_descent_or_EM_tail_domain_bound.py",
            "objective": "derive whether the MTS EM sector descends to universal Maxwell Hilbert stress with source-domain/tail certificates; if not, emit explicit EM field-energy, Poynting-flux, and material-response bounds",
            "reason": "3777 constructs Pi_M_total conditionally; the remaining highest-risk clauses are EM parent descent and finite field-support/tail/domain certificates",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "PIM_TOTAL_CONDITIONAL_PROJECTOR_AND_EM_FIELD_SOURCE_MAP_DERIVED_NOT_PARENT_SIGNED",
            "summary": "3777 constructs the conditional Pi_M_total projector and total-system domain map. It defines total mass as the observed-time projection of total Hilbert stress over matter, EM field support, binding, apparatus, interaction, and source/theta support, with explicit no-double-counting against mu_extra. It separates EM cases into neutral tail, net charge tail, stationary Poynting, radiative flux, and material response. Current MTS still cannot claim measured-GM closure because EM parent descent, tail/flux certificates, theta/source normalization, and total boundary flux are unsigned.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3777 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3777 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("projector_defined", "Pi_M_total projector definition emitted", any(row["projector_id"] == "PIM3777_2_projector_definition" for row in grouped["projector"])),
        ("domain_closure", "total-system domain rule emitted", any(row["projector_id"] == "PIM3777_3_domain_closure" for row in grouped["projector"])),
        ("no_double_counting", "no-double-counting rule emitted", any(row["projector_id"] == "PIM3777_4_no_double_counting" for row in grouped["projector"])),
        ("domain_classes", "eight total-system domain support classes emitted", len(grouped["domain_rules"]) == 8),
        ("em_classes", "six EM/source classes emitted", len(grouped["em_source_map"]) == 6),
        ("net_charge_flagged", "net charge field-energy case remains explicit", any(row["map_id"] == "ESM3777_2_net_charge_source" for row in grouped["em_source_map"])),
        ("radiative_flux_flagged", "radiative EM flux case remains explicit", any(row["map_id"] == "ESM3777_4_radiative_EM" for row in grouped["em_source_map"])),
        ("closure_not_claimed", "current branch does not close Pi_M_total", any(row["attempt_id"] == "PCA3777_7_verdict" and row["passes_clause"] is False for row in grouped["closure_attempt"])),
        ("bounds_nonclaim", "missing field/domain bounds remain nonclaim", any(str(row["bound_or_value"]).startswith("MISSING_") and row["claim_allowed"] is False for row in grouped["bound_vector"])),
        ("claim_gates_closed", "Newton/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3777_5_current_closure", "CG3777_7_Newton_GM_claim", "CG3777_8_local_GR_claim"})),
        ("next_target", "3778 EM descent/tail target emitted", grouped["next_target"][0]["target_doc"] == "3778-Y5-R2FR-MTS-to-Maxwell-Hilbert-descent-or-EM-tail-domain-bound.md"),
        ("no_formalization_leak", "no 3777 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3777*"))),
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
        "# 3777 - Pi_M Total-System Domain And EM Field-Energy Source Map",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "3777 turns `Pi_M_total` from a phrase into a conditional construction. The total source is the observed-time projection of total Hilbert stress over a total-system domain. Matter-only mass is not enough when EM fields, Poynting momentum, binding, apparatus, or source-normalization support are part of the physical system. Anything included in `M_H,total` is removed from `mu_extra`; anything not included stays as a bound row.",
        "",
        "## Pi_M Total Projector Construction",
    ]
    for row in grouped["projector"]:
        lines.append(f"- `{row['projector_id']}` `{row['status']}`: {row['statement']} Meaning: {row['derivation_or_meaning']}")
    lines.extend(["", "## Total-System Domain Rules"])
    for row in grouped["domain_rules"]:
        lines.append(f"- `{row['domain_rule_id']}` `{row['support_class']}` action=`{row['domain_action']}`: {row['definition']} Status: `{row['current_status']}`.")
    lines.extend(["", "## EM Field-Energy Source Map"])
    for row in grouped["em_source_map"]:
        lines.append(f"- `{row['map_id']}` `{row['field_class']}` -> `{row['classification']}`: {row['source_content']} Condition: {row['condition']}. Status: `{row['current_status']}`.")
    lines.extend(["", "## Closure Attempt"])
    for row in grouped["closure_attempt"]:
        lines.append(f"- `{row['attempt_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Evidence: {row['evidence']}. Consequence: {row['consequence']}.")
    lines.extend(["", "## Field/Domain Bound Vector"])
    for row in grouped["bound_vector"]:
        lines.append(f"- `{row['bound_id']}` `{row['target']}`: {row['formula']} <= `{row['bound_or_value']}` `{row['units']}`. Feeds: {row['feeds']}.")
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
        "projector": projector_rows(timestamp),
        "domain_rules": domain_rule_rows(timestamp),
        "em_source_map": em_source_map_rows(timestamp),
        "closure_attempt": closure_attempt_rows(timestamp),
        "bound_vector": bound_vector_rows(timestamp, bounds),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["projector"], grouped["projector"])
    write_csv(OUTPUTS["domain_rules"], grouped["domain_rules"])
    write_csv(OUTPUTS["em_source_map"], grouped["em_source_map"])
    write_csv(OUTPUTS["closure_attempt"], grouped["closure_attempt"])
    write_csv(OUTPUTS["bound_vector"], grouped["bound_vector"])
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
        raise SystemExit(f"3777 validation failed: {failures}")
    print("wrote 3777 checkpoint: Pi_M_total projector and EM field source map emitted")


if __name__ == "__main__":
    main()
