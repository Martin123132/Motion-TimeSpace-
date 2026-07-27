from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4122-Y5-R2FR-source-mass-quotient-signature-or-JXZ-normalization.md"

TIMESTAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
BRANCH_ID = "MTS_R2FR_Y5_SOURCE_MASS_QUOTIENT_OR_JXZ_NORMALIZATION_4122"
CHECKPOINT_ID = "4122"
DECISION = "SOURCE_MASS_QUOTIENT_UNSIGNED_JXZ_NORMALIZATION_DEFINED_FIRST_COMPARATOR_SELECTED"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4122_00_4121_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4121_NEXT_TARGET.csv",
        "4122-Y5-R2FR-source-mass-quotient-signature-or-JXZ-normalization.md",
        "4121 selected source-mass quotient signature versus JX/JZ normalization.",
    ),
    "SRC4122_01_4121_status": (
        SOURCE_DIR / "P8_Y5_R2FR_4121_STATUS.csv",
        "SOURCE_READOUT_DESCENT_THEOREM_DERIVED_JXZ_SYMBOLIC_ROWS_ACTIVE",
        "Current-chain source/readout coupling law handoff.",
    ),
    "SRC4122_02_4121_residual": (
        SOURCE_DIR / "P8_Y5_R2FR_4121_JXZ_SOURCE_RESIDUAL_ROWS.csv",
        "JXZ4121_0_source_readout_residual",
        "Current-chain symbolic JX/JZ residual rows.",
    ),
    "SRC4122_03_4121_norm_req": (
        SOURCE_DIR / "P8_Y5_R2FR_4121_JXZ_NORMALIZATION_REQUIREMENTS.csv",
        "NRM4121_0_field_basis",
        "Current-chain normalization requirements.",
    ),
    "SRC4122_04_3636_status": (
        SOURCE_DIR / "P8_Y5_R2FR_3636_STATUS.csv",
        "SOURCE_MASS_QUOTIENT_UNSIGNED_JX_NORMALIZATION_DEFINED_FIRST_COMPARATOR_SELECTED",
        "Older source-mass quotient/normalization checkpoint.",
    ),
    "SRC4122_05_3636_signature": (
        SOURCE_DIR / "P8_Y5_R2FR_3636_SOURCE_MASS_QUOTIENT_SIGNATURE.csv",
        "SMQ3636_1_dimensionless_source_charge",
        "Older beta_X source-charge definition.",
    ),
    "SRC4122_06_3636_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_3636_PARENT_SIGNATURE_AUDIT.csv",
        "SMA3636_7_verdict",
        "Older parent signature audit for source mass quotient.",
    ),
    "SRC4122_07_3636_norm": (
        SOURCE_DIR / "P8_Y5_R2FR_3636_JX_NORMALIZATION_GATE.csv",
        "JXN3636_4_force_projection",
        "Older JX normalization gate.",
    ),
    "SRC4122_08_3636_comparator": (
        SOURCE_DIR / "P8_Y5_R2FR_3636_FIRST_COMPARATOR_CHANNEL.csv",
        "CMP3636_0_first_channel_species_source_charge",
        "Older first comparator selection.",
    ),
    "SRC4122_09_constant_gm": (
        SOURCE_DIR / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv",
        "Z0_decomposition_identity",
        "Measured-GM decomposition identity and derivative-hair premises.",
    ),
    "SRC4122_10_gm_runner": (
        SOURCE_DIR / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
        "P8_species_source_charge",
        "Existing source-normalization residual runner inputs.",
    ),
    "SRC4122_11_template": (
        SOURCE_DIR / "P8_source_normalization_residual_vector_TEMPLATE.csv",
        "P8_species_source_charge",
        "Template definitions for source-normalization comparator channels.",
    ),
    "SRC4122_12_charge_current": (
        SOURCE_DIR / "P8_charge_current_equality_DIRECT_ATTEMPT.csv",
        "CC3_projected_mass_current",
        "Charge-current route for source mass and measured GM.",
    ),
    "SRC4122_13_mass_flux": (
        SOURCE_DIR / "P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "MF2_Euler_flux_closure",
        "Mass flux/projector/Euler calibration contract.",
    ),
    "SRC4122_14_script": (
        SCRIPT_PATH,
        "Y5_R2FR_4122_source_mass_quotient_signature_or_JXZ_normalization.py",
        "Reproducible generator for this 4122 checkpoint.",
    ),
}


def row_base() -> dict:
    return {"timestamp_utc": TIMESTAMP, "branch_id": BRANCH_ID, "checkpoint_id": CHECKPOINT_ID}


def write_csv(path: Path, rows: List[dict]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty csv: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def contains(path: Path, needle: str) -> bool:
    if not path.exists():
        return False
    return needle in path.read_text(encoding="utf-8", errors="replace")


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def source_register() -> List[dict]:
    rows: List[dict] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        row = row_base()
        row.update(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(contains(path, needle)),
                "role": role,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def signature_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "SMQ4122_0_decomposition",
            "measured source monopole",
            "mu_obs=G_eff M_eff(1+epsilon_mu)",
            "separates coupling, conserved source charge, and extra mass-channel hair.",
            "partial_A ln G_eff=partial_A ln M_eff=partial_A ln(1+epsilon_mu)=0 for A in {X_N,Z_N} componentwise",
            "IDENTITY_AVAILABLE_NOT_ZERO",
        ),
        (
            "SMQ4122_1_dimensionless_source_charge",
            "beta_A_source",
            "beta_A^H:=partial_{A_N} ln mu_obs=partial_{A_N} ln G_eff+partial_{A_N} ln M_eff+partial_{A_N} ln(1+epsilon_mu), A in {X,Z}",
            "dimensionless source coupling feeding J_X/J_Z and source-charge residuals.",
            "beta_A^H=0 for every source body/material/channel, with no cancellation credit unless parent identity proves it",
            "DERIVED_NORMALIZED_COUPLING_DEFINITION",
        ),
        (
            "SMQ4122_2_projected_mass",
            "M_eff",
            "M_eff=integral_{S or Sigma} Pi_M J_H with Pi_M parent-derived before readout",
            "mass used in Newtonian/orbital calibration must be the parent Hilbert/Ward source charge, not fitted orbital denominator.",
            "partial_A Pi_M=0, partial_A J_H=0, and d(Pi_M J_H)=0 in compact exterior",
            "CONDITIONAL_NOT_PARENT_SIGNED",
        ),
        (
            "SMQ4122_3_GM_Gauss_readout",
            "GM_obs",
            "mu_obs=G_eff M_eff equals Poisson/Gauss/orbital monopole in the same observed frame",
            "absolute calibration must not import orbital GM as premise.",
            "constant universal G_eff, absolute calibration, no radial/range hair, and no extra mass-channel charge",
            "CONDITIONAL_NOT_PARENT_SIGNED",
        ),
        (
            "SMQ4122_4_source_zero_theorem",
            "J_A_source",
            "J_A_source=rho_H beta_A^H/A_* plus geometry/boundary/EM terms after normalization",
            "if beta_A^H=0 and geometry/boundary/EM components vanish, source current from 4121 is zero.",
            "M_obs=M_bar(q), G_obs=G_bar(q), B_obs=B_bar(q), EM_obs=EM_bar(q) or proper/exact/scored separately",
            "THEOREM_CONDITIONAL_NOT_LIVE",
        ),
    ]
    for signature_id, obj, identity, derivation, zero_condition, status in data:
        row = row_base()
        row.update(
            {
                "signature_id": signature_id,
                "object": obj,
                "required_identity": identity,
                "derivation": derivation,
                "quotient_zero_condition": zero_condition,
                "status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def audit_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("SMA4122_0_Geff", "G_eff/kappa_eff is parent-fixed, universal, derivative-silent, and range-blind", "Z1_global_coupling_superselection", "OPEN_NOT_PARENT_DERIVED", "dln_Geff_dt; eta_source_AB; alpha(lambda); delta_frame_source"),
        ("SMA4122_1_Meff_flux", "M_eff is a parent projected Hilbert/Ward source charge with d(Pi_M J_H)=0", "Z2_calibrated_PiM_flux_conservation; CC3; MF2", "OPEN_NOT_PARENT_DERIVED", "dln_Meff_dt; partial_r_ln_mu_obs; Delta_PiM; Delta_flux"),
        ("SMA4122_2_mu_extra", "epsilon_mu=0 or universal derivative-free calibration with no active boundary/bulk/domain/memory/non-EH mass charge", "Z3_mu_extra_zero_or_universal_constant; R11_source_normalization_operator", "FAILED_MISSING_COEFFICIENT_VECTOR", "mu_extra_boundary_bulk_domain; R11_source_normalization_operator; alpha3; xi"),
        ("SMA4122_3_species", "source charge is species/material blind", "Z4_species_blind_source_action; P8_species_source_charge", "OPEN_NOT_PARENT_DERIVED", "eta_source_AB"),
        ("SMA4122_4_radial_range", "measured source strength has no radial/range-dependent hair", "Z5_no_radial_or_range_hair; P8_radial_source_hair; P8_range_dependence", "OPEN_NOT_PARENT_DERIVED", "partial_r_ln_mu_obs; alpha(lambda)"),
        ("SMA4122_5_frame_calibration", "source variation and matter/orbit readout use one observed frame", "Z6_same_frame_source_pullback; Delta_frame", "PARTIAL_CONDITIONAL_ONLY", "delta_frame_source; clock/source calibration split"),
        ("SMA4122_6_EM_calibration", "EM/Poynting source calibration descends through q or is separately physical", "EM_obs=EM_bar(q) or coefficient row", "OPEN_EM_RISK", "J_XZ_EM_source; Maxwell stress boundary flux"),
        ("SMA4122_7_verdict", "M_obs=M_bar(q) is parent-signed for rest mass, GM, Hamiltonian source, orbit readout, and EM source calibration", "4121 next target", "SOURCE_MASS_QUOTIENT_NOT_SIGNED_JXZ_NORMALIZATION_REQUIRED", "J_X/J_Z normalized source-charge rows active"),
    ]
    for audit_id, required_clause, anchor, result, residual in data:
        row = row_base()
        row.update(
            {
                "audit_id": audit_id,
                "required_clause": required_clause,
                "source_anchor": anchor,
                "current_result": result,
                "residual_if_failed": residual,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def normalization_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        ("JXZN4122_0_field_coordinate", "A_N for A in {X,Z}", "A_N:=A/A_* is the dimensionless normalized fibre/source-coupling coordinate", "dimensionless", "field scale A_* or parent canonical normalization from X/Z kinetic term", "symbolic_normalization_declared_scale_missing"),
        ("JXZN4122_1_source_charge", "beta_A^H", "beta_A^H:=partial_{A_N} ln mu_obs = partial_{A_N} ln G_eff + partial_{A_N} ln M_eff + partial_{A_N} ln(1+epsilon_mu)", "dimensionless", "component derivatives or theorem-zero certificates for G_eff, M_eff, epsilon_mu", "formula_ready_components_missing"),
        ("JXZN4122_2_source_current_density", "J_A_source", "J_A_source=rho_H beta_A^H/A_* for dimensional A, or rho_H beta_A^H for dimensionless A_N", "energy_density_per_A or energy_density_for_dimensionless_AN", "rho_H convention, A_* or canonical field units, source support/worldtube", "symbolic_current_law_units_not_fixed"),
        ("JXZN4122_3_test_charge", "beta_A^T", "beta_A^T:=partial_{A_N} ln m_test_obs for test body/clock/matter readout", "dimensionless", "test-body matter pullback and species/material marker map", "needed_for_force_comparison_missing"),
        ("JXZN4122_4_force_projection", "alpha_A(lambda_A)", "alpha_A(lambda_A)=K_A beta_A^H beta_A^T with lambda_A=sqrt(Z_A/M_A^2), after parent Green-function normalization", "dimensionless function of range", "K_A, beta_A^H, beta_A^T, lambda_A, real R10 bound curve", "not_scoreable_until_operator_and_charges_numeric_or_zero"),
        ("JXZN4122_5_source_normalization_vector", "D_a ln mu_obs", "D_a ln mu_obs=D_a ln G_eff+D_a ln M_eff+D_a ln(1+epsilon_mu) for a in {t,r,A,lambda,frame}", "yr^-1, inverse_length, dimensionless, or range-dependent", "channel derivatives and no-cancellation parent identity if terms are combined", "runner_skeleton_ready_but_values_missing"),
        ("JXZN4122_6_EM_source_charge", "beta_A^EM", "beta_A^EM:=partial_{A_N} ln EM_obs or EM source calibration coefficient", "dimensionless or EM-flux normalized", "EM stress/readout map and Poynting flux normalization", "symbolic_EM_charge_missing"),
    ]
    for norm_id, quantity, definition, units, needed_input, score_status in data:
        row = row_base()
        row.update(
            {
                "norm_id": norm_id,
                "quantity": quantity,
                "definition": definition,
                "units": units,
                "needed_input": needed_input,
                "score_status": score_status,
                "valid_for_claim": "False",
                "claim_allowed": "False",
            }
        )
        rows.append(row)
    return rows


def comparator_rows() -> List[dict]:
    rows: List[dict] = []
    data = [
        (
            "CMP4122_0_first_channel_species_source_charge",
            1,
            "P8_species_source_charge",
            "eta_source_AB;eta_WEP_source_charge",
            "eta_source_AB=2|beta_A^H(source1)-beta_A^H(source2)|/|2+beta_A^H(source1)+beta_A^H(source2)|; small-charge limit approx |Delta beta_A^H|",
            "2.8e-15 or derived universal source charge",
            "dimensionless source-charge channel tests species/material blindness without requiring an R10 curve first",
            "beta_A^H for materials A/B, material map, parent field normalization if beta uses dimensional field",
            "comparator_selected_not_numeric",
        ),
        (
            "CMP4122_1_second_channel_Gdot",
            2,
            "P8_Geff_time_drift plus P8_Meff_conservation",
            "Gdot_over_G",
            "d_t ln mu_obs=d_t ln G_eff+d_t ln M_eff+d_t ln(1+epsilon_mu)",
            "9.6e-15 yr^-1 or derived zero from existing template",
            "time drift can score source-normalization leak when composition maps are unavailable",
            "time derivative profile and separation of G_eff, M_eff, epsilon_mu",
            "comparator_available_values_missing",
        ),
        (
            "CMP4122_2_third_channel_R10",
            3,
            "P8_range_dependence",
            "delta_G_or_fifth_force_yukawa",
            "alpha_A(lambda_A)=K_A beta_A^H beta_A^T",
            "verified alpha(lambda) curve or derived zero",
            "direct R10/fifth-force channel, but needs operator and bound curve machinery",
            "K_A, lambda_A, beta charges, real bound curve",
            "deferred_curve_and_operator_missing",
        ),
        (
            "CMP4122_3_fourth_channel_EM",
            4,
            "EM_source_flux",
            "EM stress/Poynting flux source coupling",
            "J_A_EM ~ beta_A^EM T_EM or boundary Poynting projection",
            "Maxwell stress theorem-zero or sourced EM comparator",
            "keeps EM honest without hijacking the first local source-charge test",
            "EM normalization, flux projector, and bound/observable target",
            "em_comparator_defined_not_numeric",
        ),
    ]
    for comparator_id, rank, channel, observable, formula, bound, why_first, missing, status in data:
        row = row_base()
        row.update(
            {
                "comparator_id": comparator_id,
                "rank": rank,
                "channel": channel,
                "observable_link": observable,
                "prediction_formula": formula,
                "bound_or_target": bound,
                "why_ranked_here": why_first,
                "missing_to_score": missing,
                "score_status": status,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def decision_rows() -> List[dict]:
    data = [
        (
            "DEC4122_0_source_quotient",
            "Measured source mass/GM/Hamiltonian/orbit/EM readout is not parent-signed as q-data in the live corpus.",
            "SOURCE_MASS_QUOTIENT_NOT_SIGNED",
            "do not claim Newton/local-GR source normalization from source descent alone.",
        ),
        (
            "DEC4122_1_jxz_normalization",
            "J_X/J_Z source coupling now has normalized charge language: beta_A=partial_{A_N} ln mu_obs and J_A_source=rho_H beta_A/A_*.",
            "JXZ_NORMALIZATION_SYMBOLICALLY_DEFINED",
            "fill beta_A component derivatives or prove beta_A=0 from parent quotient data.",
        ),
        (
            "DEC4122_2_first_comparator",
            "The first comparator channel should be source-charge WEP eta_source_AB, with Gdot second and R10 alpha(lambda) third.",
            "FIRST_COMPARATOR_SELECTED",
            "next target should derive species/material blindness or fill beta_A^H differences.",
        ),
        (
            "DEC4122_3_claim",
            "No source-zero, Newton, local-GR, R10/R11, WEP, PPN, clock, Gdot, or EM-source claim is allowed from this checkpoint.",
            "NO_CLAIM",
            "normalization and comparator selection are machinery, not evidence of a pass.",
        ),
    ]
    rows: List[dict] = []
    for decision_id, decision, status, next_action in data:
        row = row_base()
        row.update(
            {
                "decision_id": decision_id,
                "decision": decision,
                "status": status,
                "next_action": next_action,
                "claim_allowed": "False",
                "valid_for_claim": "False",
            }
        )
        rows.append(row)
    return rows


def next_target_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "next_id": "NEXT4122_0",
            "target_doc": "4123-Y5-R2FR-species-blind-source-charge-zero-or-betaXZ-row.md",
            "target_script": "scripts/Y5_R2FR_4123_species_blind_source_charge_zero_or_betaXZ_row.py",
            "objective": "try to derive beta_X^H=beta_Z^H species/material blindness from parent matter/source quotient data; if not, create beta_X/beta_Z species-difference rows for eta_source_AB with units, material map, and bound target",
            "success_gate": "species/material blindness is theorem-zero from q-data, or eta_source_AB has nonclaim executable beta_X/beta_Z difference skeleton tied to the 2.8e-15 target",
            "reason": "4122 selects source-charge WEP as the first comparator for normalized J_X/J_Z source coupling.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def status_rows() -> List[dict]:
    row = row_base()
    row.update(
        {
            "status_id": "STATUS4122_0",
            "result": DECISION,
            "summary": (
                "4122 attempts the source-mass quotient signature and keeps it unsigned: measured source mass/GM/"
                "Hamiltonian/orbit/EM readout is not yet parent-signed as q-data. The fallback is now sharper: normalize "
                "source coupling with beta_A=partial_{A_N} ln mu_obs for A in {X,Z} and J_A_source=rho_H beta_A/A_*. "
                "The first comparator channel is source-charge WEP eta_source_AB, before Gdot and R10 alpha(lambda)."
            ),
            "source_mass_quotient_signed": "False",
            "jxz_normalization_defined": "True",
            "first_comparator_selected": "True",
            "score_ready": "False",
            "claim_state": "no source_zero, Newton, local_GR, R10, R11, WEP, PPN, clock, Gdot, or EM_source claim",
            "next_target": "4123 species-blind source-charge zero or betaX/betaZ row",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    )
    return [row]


def output_paths() -> Dict[str, Path]:
    return {
        "P8_Y5_R2FR_4122_SOURCE_REGISTER": SOURCE_DIR / "P8_Y5_R2FR_4122_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_4122_SOURCE_MASS_QUOTIENT_SIGNATURE": SOURCE_DIR / "P8_Y5_R2FR_4122_SOURCE_MASS_QUOTIENT_SIGNATURE.csv",
        "P8_Y5_R2FR_4122_PARENT_SIGNATURE_AUDIT": SOURCE_DIR / "P8_Y5_R2FR_4122_PARENT_SIGNATURE_AUDIT.csv",
        "P8_Y5_R2FR_4122_JXZ_NORMALIZATION_GATE": SOURCE_DIR / "P8_Y5_R2FR_4122_JXZ_NORMALIZATION_GATE.csv",
        "P8_Y5_R2FR_4122_FIRST_COMPARATOR_CHANNEL": SOURCE_DIR / "P8_Y5_R2FR_4122_FIRST_COMPARATOR_CHANNEL.csv",
        "P8_Y5_R2FR_4122_DECISION_GATES": SOURCE_DIR / "P8_Y5_R2FR_4122_DECISION_GATES.csv",
        "P8_Y5_R2FR_4122_NEXT_TARGET": SOURCE_DIR / "P8_Y5_R2FR_4122_NEXT_TARGET.csv",
        "P8_Y5_R2FR_4122_STATUS": SOURCE_DIR / "P8_Y5_R2FR_4122_STATUS.csv",
    }


def write_doc(outputs: Dict[str, Path]) -> None:
    sections = [
        "# 4122 - Source-Mass Quotient Signature or JX/JZ Normalization",
        "",
        "## Verdict",
        "",
        f"- Decision: `{DECISION}`.",
        "- Source-mass quotient signature remains unsigned: measured mass/GM/Hamiltonian/orbit/EM readout is not yet proven q-owned.",
        "- Fallback is now normalized: `beta_A^H=partial_{A_N} ln mu_obs` and `J_A_source=rho_H beta_A^H/A_*` for `A in {X,Z}`.",
        "- First comparator is source-charge WEP `eta_source_AB`; `Gdot` is second; R10 `alpha(lambda)` is third.",
        "- No source-zero or local-GR claim is made.",
        "",
        "## Generated Outputs",
        "",
    ]
    for name, path in outputs.items():
        sections.append(f"- `{name}`: `{path}`")
    sections.extend(["", "## Source-Mass Signature", "", "| signature_id | required_identity | status |", "|---|---|---|"])
    for row in signature_rows():
        sections.append(f"| {row['signature_id']} | `{row['required_identity']}` | {row['status']} |")
    sections.extend(["", "## Normalization Gate", "", "| norm_id | quantity | definition | score_status |", "|---|---|---|---|"])
    for row in normalization_rows():
        sections.append(f"| {row['norm_id']} | {row['quantity']} | `{row['definition']}` | {row['score_status']} |")
    sections.extend(["", "## First Comparator", "", "| comparator_id | rank | observable_link | score_status |", "|---|---|---|---|"])
    for row in comparator_rows():
        sections.append(f"| {row['comparator_id']} | {row['rank']} | {row['observable_link']} | {row['score_status']} |")
    sections.extend(["", "## Next Target", "", "- `4123-Y5-R2FR-species-blind-source-charge-zero-or-betaXZ-row.md`", "- Try species/material blindness first; if it fails, make beta-difference rows executable against the `2.8e-15` source-charge target.", ""])
    DOC_PATH.write_text("\n".join(sections), encoding="utf-8")


def write_outputs() -> Dict[str, Path]:
    outputs = output_paths()
    writers = {
        "P8_Y5_R2FR_4122_SOURCE_REGISTER": source_register,
        "P8_Y5_R2FR_4122_SOURCE_MASS_QUOTIENT_SIGNATURE": signature_rows,
        "P8_Y5_R2FR_4122_PARENT_SIGNATURE_AUDIT": audit_rows,
        "P8_Y5_R2FR_4122_JXZ_NORMALIZATION_GATE": normalization_rows,
        "P8_Y5_R2FR_4122_FIRST_COMPARATOR_CHANNEL": comparator_rows,
        "P8_Y5_R2FR_4122_DECISION_GATES": decision_rows,
        "P8_Y5_R2FR_4122_NEXT_TARGET": next_target_rows,
        "P8_Y5_R2FR_4122_STATUS": status_rows,
    }
    for key, writer in writers.items():
        write_csv(outputs[key], writer())
    write_doc(outputs)
    return outputs


def flatten_rows(paths: Iterable[Path]) -> str:
    parts: List[str] = []
    for path in paths:
        for row in parse_csv(path):
            parts.append(" ".join(str(value) for value in row.values()))
    return " ".join(parts)


def validate(outputs: Dict[str, Path]) -> List[dict]:
    checks: List[dict] = []

    def add(check_id: str, description: str, passed: bool, detail: str) -> None:
        row = row_base()
        row.update({"check_id": check_id, "description": description, "passed": str(bool(passed)), "detail": detail})
        checks.append(row)

    sources = source_register()
    add(
        "VAL4122_0_sources",
        "all cited local source paths exist and contain required needles",
        all(row["exists"] == "True" and row["needle_found"] == "True" for row in sources),
        "; ".join(f"{row['source_id']}={row['exists']}/{row['needle_found']}" for row in sources),
    )
    add("VAL4122_1_doc", "checkpoint markdown exists and names decision", DOC_PATH.exists() and DECISION in DOC_PATH.read_text(encoding="utf-8"), str(DOC_PATH))

    parse_ok = True
    parse_counts: Dict[str, object] = {}
    for key, path in outputs.items():
        try:
            rows = parse_csv(path)
            parse_counts[key] = len(rows)
            parse_ok = parse_ok and len(rows) > 0
        except Exception as exc:
            parse_ok = False
            parse_counts[key] = repr(exc)
    add("VAL4122_2_csv_parse", "all generated CSV outputs parse and are nonempty", parse_ok, str(parse_counts))

    signature_text = flatten_rows([outputs["P8_Y5_R2FR_4122_SOURCE_MASS_QUOTIENT_SIGNATURE"]])
    signature_ok = all(token in signature_text for token in ["mu_obs=G_eff M_eff", "beta_A^H", "M_eff", "GM_obs", "J_A_source"])
    add("VAL4122_3_signature", "source-mass signature covers mu decomposition, beta, mass, GM, and source-zero theorem", signature_ok, "signature tokens checked")

    audit_text = flatten_rows([outputs["P8_Y5_R2FR_4122_PARENT_SIGNATURE_AUDIT"]])
    audit_ok = all(token in audit_text for token in ["OPEN_NOT_PARENT_DERIVED", "FAILED_MISSING_COEFFICIENT_VECTOR", "SOURCE_MASS_QUOTIENT_NOT_SIGNED", "EM"])
    add("VAL4122_4_audit", "audit blocks source-mass quotient claim and includes EM risk", audit_ok, "audit tokens checked")

    norm_text = flatten_rows([outputs["P8_Y5_R2FR_4122_JXZ_NORMALIZATION_GATE"]])
    norm_ok = all(token in norm_text for token in ["A_N", "beta_A^H", "J_A_source", "alpha_A(lambda_A)", "beta_A^EM"])
    add("VAL4122_5_normalization", "normalization gate defines field coordinate, beta, source current, force projection, and EM charge", norm_ok, "normalization tokens checked")

    comparator_text = flatten_rows([outputs["P8_Y5_R2FR_4122_FIRST_COMPARATOR_CHANNEL"]])
    comparator_ok = all(token in comparator_text for token in ["eta_source_AB", "2.8e-15", "Gdot_over_G", "alpha_A(lambda_A)", "EM"])
    add("VAL4122_6_comparators", "comparator table ranks source-charge, Gdot, R10, and EM", comparator_ok, "comparator tokens checked")

    next_rows = parse_csv(outputs["P8_Y5_R2FR_4122_NEXT_TARGET"])
    next_ok = len(next_rows) == 1 and next_rows[0].get("target_doc") == "4123-Y5-R2FR-species-blind-source-charge-zero-or-betaXZ-row.md"
    add("VAL4122_7_next_target", "next target is 4123 species-blind source charge", next_ok, str(next_rows))

    status_rows_local = parse_csv(outputs["P8_Y5_R2FR_4122_STATUS"])
    status_ok = bool(status_rows_local) and status_rows_local[0].get("result") == DECISION and "no source_zero" in status_rows_local[0].get("claim_state", "")
    add("VAL4122_8_status", "status records normalization and no-claim state", status_ok, "status row checked")

    all_rows: List[dict] = []
    for path in outputs.values():
        all_rows.extend(parse_csv(path))
    no_claim = all(row.get("claim_allowed") in ("False", "") and row.get("valid_for_claim") in ("False", "") for row in all_rows)
    add("VAL4122_9_no_claim_flags", "all generated rows remain no-claim and invalid for claim", no_claim, f"row_count={len(all_rows)}")

    output_paths_all = list(outputs.values()) + [DOC_PATH]
    in_scope = all(is_under(path, ROOT) for path in output_paths_all)
    formalization_output = any(is_under(path, FORMALIZATION) for path in output_paths_all)
    formalization_touched = False
    if FORMALIZATION.exists():
        formalization_touched = any(FORMALIZATION.rglob("*R2FR_4122*")) or any(FORMALIZATION.rglob("4122-Y5-R2FR*"))
    add("VAL4122_10_scope", "outputs stay in post-checkpoint-work and not formalization-workbench", in_scope and not formalization_output and not formalization_touched, f"doc={DOC_PATH}; csv_count={len(outputs)}")

    compile_ok = True
    compile_detail = "py_compile ok"
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except Exception as exc:
        compile_ok = False
        compile_detail = repr(exc)
    add("VAL4122_11_compile", "generator script compiles", compile_ok, compile_detail)
    return checks


def main() -> None:
    outputs = write_outputs()
    validation_rows = validate(outputs)
    validation_path = SOURCE_DIR / "P8_Y5_BRR545_4122_VALIDATION.csv"
    write_csv(validation_path, validation_rows)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    failed = [row for row in validation_rows if row["passed"] != "True"]
    print(f"wrote: {DOC_PATH}")
    for path in outputs.values():
        print(f"wrote: {path}")
    print(f"validation: {validation_path}")
    if failed:
        print("failed checks:")
        for row in failed:
            print(f"- {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print("all validation checks passed")


if __name__ == "__main__":
    main()
