import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3776"
BRANCH = "MTS_R2FR_Y5_TOTAL_HILBERT_SOURCE_INCLUSION_EM_POYNTING_AND_INTERIOR_MONOPOLE_CLOSURE_3776"
PCW = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main\post-checkpoint-work"
)
RESIDUALS = PCW / "source-intake" / "mts_residuals"
FORMALIZATION = PCW.parent / "formalization-workbench"
DOC_PATH = PCW / "3776-Y5-R2FR-total-Hilbert-source-inclusion-EM-Poynting-and-interior-monopole-closure.md"


OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3776_SOURCE_REGISTER.csv",
    "inclusion_theorem": RESIDUALS / "P8_Y5_R2FR_3776_TOTAL_HILBERT_SOURCE_INCLUSION_THEOREM.csv",
    "domain_audit": RESIDUALS / "P8_Y5_R2FR_3776_EM_POYNTING_DOMAIN_AUDIT.csv",
    "closure_attempt": RESIDUALS / "P8_Y5_R2FR_3776_INTERIOR_MONOPOLE_CLOSURE_ATTEMPT.csv",
    "reclassification": RESIDUALS / "P8_Y5_R2FR_3776_MUEXTRA_RECLASSIFICATION_VECTOR.csv",
    "bound_vector": RESIDUALS / "P8_Y5_R2FR_3776_REMAINING_BOUND_VECTOR.csv",
    "claim_gates": RESIDUALS / "P8_Y5_R2FR_3776_CLAIM_GATES.csv",
    "decision_rows": RESIDUALS / "P8_Y5_R2FR_3776_DECISION_ROWS.csv",
    "next_target": RESIDUALS / "P8_Y5_R2FR_3776_NEXT_TARGET.csv",
    "status": RESIDUALS / "P8_Y5_R2FR_3776_STATUS.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3776_VALIDATION.csv",
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
        "SRC3776_0_3775_doc": PCW / "3775-Y5-R2FR-no-harmonic-exterior-monopole-lemma-or-channel-support-certificates.md",
        "SRC3776_1_3775_monopole_lemma": RESIDUALS / "P8_Y5_R2FR_3775_NO_HARMONIC_MONOPOLE_LEMMA.csv",
        "SRC3776_2_3775_certificates": RESIDUALS / "P8_Y5_R2FR_3775_CHANNEL_SUPPORT_CERTIFICATE_ATTEMPT.csv",
        "SRC3776_3_3764_total_source": RESIDUALS / "P8_Y5_R2FR_3764_SAME_TOTAL_SOURCE_VARIATION_THEOREM.csv",
        "SRC3776_4_3760_EM_theorem": RESIDUALS / "P8_Y5_R2FR_3760_MAXWELL_EM_STRESS_SOURCE_THEOREM.csv",
        "SRC3776_5_3770_source_theorem": RESIDUALS / "P8_Y5_R2FR_3770_SOURCE_ACTION_ZERO_THEOREM.csv",
        "SRC3776_6_3771_theta_theorem": RESIDUALS / "P8_Y5_R2FR_3771_CONSTANT_MARKER_ZERO_THEOREM.csv",
        "SRC3776_7_3772_Newton_theorem": RESIDUALS / "P8_Y5_R2FR_3772_NEWTON_SOURCE_HAMILTONIAN_THEOREM.csv",
        "SRC3776_8_3774_component_bounds": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_COMPONENT_BOUND_VECTOR.csv",
        "SRC3776_9_3774_observable_matrix": RESIDUALS / "P8_Y5_R2FR_3774_MUEXTRA_OBSERVABLE_PROJECTION_MATRIX.csv",
        "SRC3776_10_3759_wep_eval": RESIDUALS / "P8_Y5_R2FR_3759_WEP_BOUND_EVALUATION.csv",
        "SRC3776_11_3761_ppn_eval": RESIDUALS / "P8_Y5_R2FR_3761_GAMMA_BETA_BOUND_EVALUATION.csv",
    }


def source_register(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "source_id": source_id,
            "source_path": str(path),
            "source_exists": path.exists(),
            "role": "3776 total Hilbert source inclusion and EM/Poynting interior monopole input",
        }
        for source_id, path in source_paths().items()
    ]


def find_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def imported_bounds() -> dict[str, str]:
    wep = find_row(source_paths()["SRC3776_10_3759_wep_eval"], "evaluation_id", "WB3759_2_max_allowed_residual")
    gamma = find_row(source_paths()["SRC3776_11_3761_ppn_eval"], "evaluation_id", "PGB3761_0_gamma_conditional_zero")
    beta = find_row(source_paths()["SRC3776_11_3761_ppn_eval"], "evaluation_id", "PGB3761_1_beta_conditional_zero")
    return {"wep": wep["bound_value"], "gamma": gamma["bound_value"], "beta": beta["bound_value"]}


def inclusion_theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "THI3776_0_total_source_action",
            "Assume one q_obs-descended source action S_src=S_matter+S_EM+S_binding+S_apparatus+S_int, with all sectors varied with respect to the same observed metric/coframe.",
            "This imports the 3764 and 3770 source descent contracts. It is the only non-smuggled route by which real stress moves into the GR-like source.",
            "SOURCE_INCLUSION_SIGNATURE_REQUIRED",
        ),
        (
            "THI3776_1_linear_Hilbert_sum",
            "T_total^{ab}:=(2/sqrt(-g_eff)) delta S_src/dg_eff_ab equals T_matter+T_EM+T_binding+T_apparatus+T_int by linearity of variation.",
            "The same Hilbert/coframe variation supplies one active source. No separate EM gravitational charge is introduced.",
            "EXACT_CONDITIONAL_TOTAL_STRESS_THEOREM",
        ),
        (
            "THI3776_2_EM_Ward_internal_exchange",
            "For descended Maxwell/matter sectors, nabla_a T_EM^{ab}=-F^b_c J^c and nabla_a T_matter^{ab}=+F^b_c J^c plus non-EM material forces, so Lorentz exchange cancels inside nabla_a T_total^{ab}.",
            "The Poynting vector and field momentum are part of T_EM^{0i}; they are internal total-stress bookkeeping when the same action descends.",
            "EXACT_CONDITIONAL_EM_WARD_INCLUSION",
        ),
        (
            "THI3776_3_domain_projector_requirement",
            "The source domain/projector must be a total-system domain, not a matter-only tube, whenever field energy or binding stress extends outside the material body.",
            "A Coulomb, dipole, magnetic, or Poynting exterior tail can have finite l=0 energy. If the domain cuts it off, it reappears as Q_EM_Poynting or Q_source_theta.",
            "EXACT_DOMAIN_REQUIREMENT",
        ),
        (
            "THI3776_4_interior_monopole_reclassification",
            "If total-source descent and total-system domain closure hold, EM/Poynting, binding, apparatus, interaction, and source-normalization monopoles are reclassified from mu_extra into M_H.",
            "This is not deletion: the mass is still there, but it is the same Hilbert mass that sources the Hamiltonian/Gauss charge.",
            "EXACT_CONDITIONAL_RECLASSIFICATION_THEOREM",
        ),
        (
            "THI3776_5_Newton_bridge_effect",
            "After reclassification, the 3772 active/passive/inertial mass theorem can use M_eff=M_H,total rather than matter-only mass, while leftover Q_i rows are only those not included in the same total source.",
            "This is how MTS can look like GR locally without pretending EM and binding energy do not gravitate.",
            "EXACT_CONDITIONAL_NEWTON_SOURCE_CLOSURE",
        ),
        (
            "THI3776_6_failure_mode",
            "If any sector action, coefficient, or domain fails to descend through q_obs, the unmatched monopole remains in mu_extra and must feed WEP, PPN, Newton GM, radial-hair, or R10 rows.",
            "This preserves the no-cancellation discipline from 3775.",
            "EXACT_RESIDUAL_FALLBACK",
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


def domain_audit_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "EDA3776_0_matter_only_tube",
            "matter-only material tube",
            "cuts off EM field energy, binding fields, apparatus stress, and interaction stress that extend outside matter labels",
            "unsafe for measured GM unless exterior field energy is proven zero or separately bounded",
            "REJECT_AS_DEFAULT_TOTAL_SOURCE_DOMAIN",
        ),
        (
            "EDA3776_1_total_system_tube",
            "total-system tube",
            "contains matter plus descended EM field stress, binding stress, apparatus energy, and interaction stress through the same q_obs source action",
            "clean domain for M_H,total if parent action signs descent and projector closure",
            "PREFERRED_CONDITIONAL_DOMAIN",
        ),
        (
            "EDA3776_2_EM_exterior_tail",
            "exterior EM field tail",
            "Coulomb/dipole/magnetic/Poynting fields can carry positive field energy outside the material radius",
            "belongs in M_H,total if Maxwell stress descends; otherwise becomes Q_EM_Poynting",
            "MUST_INCLUDE_OR_BOUND",
        ),
        (
            "EDA3776_3_Poynting_flux",
            "Poynting momentum/flux",
            "stationary bound systems may have circulating field momentum even when net flux through infinity is zero",
            "T_EM^{0i} is part of total stress; boundary flux still needs silence for nonstationary leakage",
            "INCLUDE_IN_TOTAL_STRESS_AND_CHECK_BOUNDARY_FLUX",
        ),
        (
            "EDA3776_4_binding_response",
            "binding and material response",
            "nuclear/EM binding and response coefficients alter inertial and active mass if not included consistently",
            "must descend as source/theta terms or feed Q_source_theta",
            "MUST_DESCEND_OR_BOUND",
        ),
        (
            "EDA3776_5_projector_PiM_total",
            "Pi_M_total",
            "projector must select the total Hilbert source current, not a sector-labelled matter-only current",
            "needed for Hamiltonian-Hilbert equality and no domain-wall flux",
            "PROJECTOR_CONSTRUCTION_REQUIRED",
        ),
    ]
    return [
        {
            **base(timestamp),
            "audit_id": audit_id,
            "object": object_name,
            "issue": issue,
            "consequence": consequence,
            "status": status,
            "claim_allowed": False,
        }
        for audit_id, object_name, issue, consequence, status in rows
    ]


def closure_attempt_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "IMA3776_0_total_source_theorem_exists",
            "conditional total Hilbert source theorem exists",
            "3764 STS3764_1, 3770 SAT3770_3, and THI3776_1",
            True,
            "the route is mathematically available",
        ),
        (
            "IMA3776_1_EM_standard_identity",
            "Maxwell Hilbert stress and Ward exchange identity exist",
            "3760 EMT3760_1 and EMT3760_2",
            True,
            "standard EM stress inclusion is structurally compatible",
        ),
        (
            "IMA3776_2_MTS_EM_parent_descent",
            "MTS parent signs emergent/low-energy EM descends to the same Maxwell Hilbert stress with universal Z_EM",
            "3760 EMT3760_4 remains MTS_PARENT_DESCENT_REQUIRED",
            False,
            "EM/Poynting cannot yet be moved out of mu_extra",
        ),
        (
            "IMA3776_3_total_system_domain",
            "Pi_M and the source domain include all descended field/binding/apparatus stress rather than matter-only support",
            "3775 CCA3775_7 and CCA3775_8 remain missing total-source inclusion",
            False,
            "exterior/interior field energy can still leak into Q_i",
        ),
        (
            "IMA3776_4_theta_superselection",
            "physical constants/material markers are q_obs-owned or superselected",
            "3771 CMT3771_2 remains parent_unsigned",
            False,
            "source/theta interior monopole can still shift M_H",
        ),
        (
            "IMA3776_5_no_sector_gravity_labels",
            "no species- or sector-labelled gravitational coupling survives inside S_src",
            "3764 STS3764_3 remains conditional, not parent-signed",
            False,
            "WEP and source-normalization rows remain live",
        ),
        (
            "IMA3776_6_verdict",
            "current branch closes EM/Poynting and source/theta interior monopoles",
            "route derived but parent descent, total domain, theta silence, and sector-label silence remain unsigned",
            False,
            "do not claim measured-GM or local-GR closure",
        ),
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


def reclassification_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        (
            "MRV3776_0_EM_Poynting",
            "Q_EM_Poynting",
            "M_H,total if S_EM descends through q_obs and Pi_M_total includes exterior field support; otherwise mu_extra",
            "MISSING_EM_TOTAL_HILBERT_SOURCE_INCLUSION_AND_TOTAL_DOMAIN",
            "highest priority honest stress channel",
        ),
        (
            "MRV3776_1_binding",
            "Q_binding_inside_source_theta",
            "M_H,total if binding/interaction terms are in S_src and theta markers are q_obs-owned; otherwise Q_source_theta",
            "MISSING_BINDING_THETA_DESCENT",
            "hidden active-mass and WEP channel",
        ),
        (
            "MRV3776_2_apparatus",
            "Q_apparatus",
            "M_H,total if apparatus/readout energy is included in the same source action and same observed frame; otherwise readout/source residual",
            "MISSING_APPARATUS_SOURCE_DESCENT",
            "clock/orbit/readout contamination channel",
        ),
        (
            "MRV3776_3_interaction",
            "Q_int",
            "M_H,total if interaction stress is varied with matter and fields in one action; otherwise internal exchange can look like external source leakage",
            "MISSING_INTERACTION_STRESS_DESCENT",
            "prevents double-counting Lorentz/binding exchange",
        ),
        (
            "MRV3776_4_source_normalization",
            "Q_source_norm",
            "M_H,total if source mass normalization is the same coefficient in NR, passive, active, and Hilbert roles; otherwise Newton GM residual",
            "MISSING_NEWTON_SOURCE_THETA_PROJECTION_COMPONENT",
            "main local Newton mechanics blocker",
        ),
    ]
    return [
        {
            **base(timestamp),
            "reclassification_id": reclassification_id,
            "channel": channel,
            "classification_rule": classification_rule,
            "current_status": current_status,
            "meaning": meaning,
            "claim_allowed": False,
        }
        for reclassification_id, channel, classification_rule, current_status, meaning in rows
    ]


def bound_vector_rows(timestamp: str, bounds: dict[str, str]) -> list[dict[str, object]]:
    rows = [
        (
            "RBV3776_0_EM_mass",
            "epsilon_EM_Poynting_mass",
            "|M_EM_unincluded|/M_H,total",
            "MISSING_EM_TOTAL_DOMAIN_OR_FIELD_ENERGY_BOUND",
            "dimensionless",
            "Newton GM; WEP; PPN",
        ),
        (
            "RBV3776_1_source_theta_mass",
            "epsilon_source_theta_mass",
            "C_mu_src epsilon_src + C_mu_theta epsilon_theta + b_source_norm",
            "MISSING_SOURCE_THETA_INTERIOR_MONOPOLE_PROJECTION",
            "dimensionless",
            "Newton GM; WEP; clocks",
        ),
        (
            "RBV3776_2_WEP_total_source",
            "eta_total_source_AB",
            "C_EM epsilon_EM_unincluded + C_theta epsilon_source_theta + C_sector epsilon_sector_gravity",
            bounds["wep"],
            "dimensionless",
            "WEP",
        ),
        (
            "RBV3776_3_gamma_total_source",
            "delta_gamma_total_source",
            "C_gamma_EM epsilon_EM_unincluded + C_gamma_src epsilon_source_theta + C_gamma_domain epsilon_domain",
            bounds["gamma"],
            "dimensionless",
            "PPN gamma",
        ),
        (
            "RBV3776_4_beta_total_source",
            "delta_beta_total_source",
            "C_beta_EM epsilon_EM_unincluded + C_beta_binding epsilon_binding + C_beta_nonlin epsilon_source_theta",
            bounds["beta"],
            "dimensionless",
            "PPN beta",
        ),
        (
            "RBV3776_5_domain_wall",
            "epsilon_total_domain_wall",
            "|int_wall n_a T_total^{ab} xi_b|/M_H,total",
            "MISSING_TOTAL_DOMAIN_WALL_FLUX_BOUND",
            "dimensionless",
            "Hamiltonian/Gauss; radial hair",
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
    theorem = any(row["theorem_id"] == "THI3776_4_interior_monopole_reclassification" for row in grouped["inclusion_theorem"])
    domain = any(row["audit_id"] == "EDA3776_5_projector_PiM_total" for row in grouped["domain_audit"])
    em_attempt = any(row["attempt_id"] == "IMA3776_2_MTS_EM_parent_descent" for row in grouped["closure_attempt"])
    verdict_closed = any(row["attempt_id"] == "IMA3776_6_verdict" and row["passes_clause"] is True for row in grouped["closure_attempt"])
    missing_bounds = any(str(row["bound_or_value"]).startswith("MISSING_") for row in grouped["bound_vector"])
    rows = [
        ("CG3776_0_sources", "all 3776 source paths exist", sources_exist, "path hygiene"),
        ("CG3776_1_inclusion_theorem", "total Hilbert-source inclusion theorem emitted", theorem, "real stress can be reclassified into M_H only by same-source variation"),
        ("CG3776_2_domain_audit", "matter-only tube rejected and Pi_M_total requirement emitted", domain, "field energy outside matter is not swept under the carpet"),
        ("CG3776_3_EM_attempt", "EM/Poynting parent-descent clause is audited", em_attempt, "highest-risk honest channel named"),
        ("CG3776_4_current_closure", "current branch closes EM/source interior monopoles", verdict_closed, "expected false until parent descent and total domain are signed"),
        ("CG3776_5_missing_bounds_nonclaim", "remaining bound rows stay explicit", missing_bounds, "no claim with placeholder field-energy/source coefficients"),
        ("CG3776_6_Newton_GM_claim", "measured-GM Newton claim allowed", False, "blocked until total-source inclusion/domain or bounds close"),
        ("CG3776_7_local_GR_claim", "local GR claim allowed", False, "blocked until total source, EH operator, and readout gates close"),
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
        ("DEC3776_0", "The clean GR-like route is not to delete EM/Poynting or binding energy; it is to include them in the same total Hilbert source M_H,total.", "treat EM/source inclusion as the next constructive proof target"),
        ("DEC3776_1", "A matter-only worldtube is unsafe for measured GM whenever field energy or binding stress extends outside material labels.", "construct Pi_M_total and a total-system domain before claiming Gauss closure"),
        ("DEC3776_2", "The MTS-specific missing signature is low-energy/emergent EM descent to universal Maxwell Hilbert stress with no sector-labelled gravitational coupling.", "derive or bound Z_EM, EM source descent, and field-support domain"),
        ("DEC3776_3", "Source/theta leakage is the same problem in different clothes: hidden source normalization must either be in M_H,total or become a Newton/WEP/clock residual.", "attack EM and source/theta inclusion together, not as separate patches"),
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
            "next_id": "NEXT3776_0",
            "target_doc": "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md",
            "target_script": "scripts/Y5_R2FR_3777_PiM_total_system_domain_and_EM_field_energy_source_map.py",
            "objective": "construct the total-system source projector Pi_M_total and domain rules that include EM/Poynting, binding, apparatus, and source/theta support; if construction fails, emit field-energy/source-domain bounds",
            "reason": "3776 shows total-source inclusion needs not only an action theorem but also the correct source domain/projector for field support outside matter labels",
            "claim_allowed": False,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            **base(timestamp),
            "status": "TOTAL_HILBERT_SOURCE_INCLUSION_THEOREM_DERIVED_DOMAIN_PROJECTOR_REQUIRED_NOT_PARENT_SIGNED",
            "summary": "3776 derives the total Hilbert-source inclusion route: EM/Poynting, binding, apparatus, interaction, and source-normalization monopoles move from mu_extra into M_H,total only if they descend through one q_obs source action and the source domain/projector includes their full field support. This is a real advance because it rejects the matter-only tube as the default for measured GM. Current MTS still cannot claim closure because emergent EM descent, Pi_M_total, theta/source silence, and sector-label silence remain unsigned.",
            "claim_allowed": False,
        }
    ]


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, object]]]) -> list[dict[str, object]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks = [
        ("sources_exist", "all 3776 source paths exist", all(Path(str(row["source_path"])).exists() for row in grouped["sources"])),
        ("generated_csvs_parse", "all generated 3776 csvs parse", all(read_csv(path) for path in generated_csvs)),
        ("total_source_theorem", "total Hilbert-source inclusion theorem emitted", any(row["theorem_id"] == "THI3776_1_linear_Hilbert_sum" for row in grouped["inclusion_theorem"])),
        ("domain_requirement", "total-system domain/projector requirement emitted", any(row["theorem_id"] == "THI3776_3_domain_projector_requirement" for row in grouped["inclusion_theorem"])),
        ("matter_only_rejected", "matter-only tube is rejected as default", any(row["audit_id"] == "EDA3776_0_matter_only_tube" and row["status"] == "REJECT_AS_DEFAULT_TOTAL_SOURCE_DOMAIN" for row in grouped["domain_audit"])),
        ("em_poynting_audited", "EM/Poynting inclusion attempt remains explicit", any(row["attempt_id"] == "IMA3776_2_MTS_EM_parent_descent" and row["passes_clause"] is False for row in grouped["closure_attempt"])),
        ("theta_audited", "source/theta interior monopole attempt remains explicit", any(row["attempt_id"] == "IMA3776_4_theta_superselection" and row["passes_clause"] is False for row in grouped["closure_attempt"])),
        ("no_closure_claim", "current branch does not close EM/source interior monopoles", any(row["attempt_id"] == "IMA3776_6_verdict" and row["passes_clause"] is False for row in grouped["closure_attempt"])),
        ("bounds_nonclaim", "missing bound rows remain nonclaim", any(str(row["bound_or_value"]).startswith("MISSING_") and row["claim_allowed"] is False for row in grouped["bound_vector"])),
        ("claim_gates_closed", "Newton/local-GR claims remain closed", all(row["passed"] is False for row in grouped["claim_gates"] if row["gate_id"] in {"CG3776_4_current_closure", "CG3776_6_Newton_GM_claim", "CG3776_7_local_GR_claim"})),
        ("next_target", "3777 Pi_M_total/domain target emitted", grouped["next_target"][0]["target_doc"] == "3777-Y5-R2FR-PiM-total-system-domain-and-EM-field-energy-source-map.md"),
        ("no_formalization_leak", "no 3776 files written to formalization-workbench", not FORMALIZATION.exists() or not list(FORMALIZATION.rglob("*3776*"))),
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
        "# 3776 - Total Hilbert Source Inclusion, EM/Poynting, And Interior Monopole Closure",
        "",
        "## Status",
        "",
        f"`{grouped['status'][0]['status']}`.",
        "",
        grouped["status"][0]["summary"],
        "",
        "## Result In Plain Terms",
        "",
        "3776 moves the local-GR route forward in the right direction: real stress-energy is not erased. EM field energy, Poynting momentum, binding energy, apparatus energy, and source normalization either belong to one total Hilbert mass `M_H,total`, or they remain explicit `mu_extra` channels. The source domain also has to be the total system, not just the matter-labelled body.",
        "",
        "## Total Hilbert Source Inclusion Theorem",
    ]
    for row in grouped["inclusion_theorem"]:
        lines.append(f"- `{row['theorem_id']}` `{row['status']}`: {row['statement']} Derivation: {row['derivation']}")
    lines.extend(["", "## EM/Poynting Domain Audit"])
    for row in grouped["domain_audit"]:
        lines.append(f"- `{row['audit_id']}` `{row['object']}` `{row['status']}`: {row['issue']} Consequence: {row['consequence']}.")
    lines.extend(["", "## Interior Monopole Closure Attempt"])
    for row in grouped["closure_attempt"]:
        lines.append(f"- `{row['attempt_id']}` pass=`{row['passes_clause']}`: {row['required_clause']}. Evidence: {row['evidence']}. Consequence: {row['consequence']}.")
    lines.extend(["", "## MuExtra Reclassification Vector"])
    for row in grouped["reclassification"]:
        lines.append(f"- `{row['reclassification_id']}` `{row['channel']}`: {row['classification_rule']} Status: `{row['current_status']}`.")
    lines.extend(["", "## Remaining Bound Vector"])
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
        "inclusion_theorem": inclusion_theorem_rows(timestamp),
        "domain_audit": domain_audit_rows(timestamp),
        "closure_attempt": closure_attempt_rows(timestamp),
        "reclassification": reclassification_rows(timestamp),
        "bound_vector": bound_vector_rows(timestamp, bounds),
        "decision_rows": decision_rows(timestamp),
        "next_target": next_target_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["claim_gates"] = claim_gate_rows(timestamp, grouped)

    write_csv(OUTPUTS["sources"], grouped["sources"])
    write_csv(OUTPUTS["inclusion_theorem"], grouped["inclusion_theorem"])
    write_csv(OUTPUTS["domain_audit"], grouped["domain_audit"])
    write_csv(OUTPUTS["closure_attempt"], grouped["closure_attempt"])
    write_csv(OUTPUTS["reclassification"], grouped["reclassification"])
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
        raise SystemExit(f"3776 validation failed: {failures}")
    print("wrote 3776 checkpoint: total Hilbert source inclusion and domain requirement emitted")


if __name__ == "__main__":
    main()
