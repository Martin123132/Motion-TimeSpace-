from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4016"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4016-Y5-R2FR-Gref-superselection-universal-calibration-or-Gdot-range-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4016_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4016_GLOBAL_COUPLING_AUDIT.csv",
    "finite": SRC / "P8_Y5_R2FR_4016_GREF_DRIFT_RANGE_FINITE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4016_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4016_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4016_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4016_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4016_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4016_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4016_VALIDATION.csv",
}

NEXT_DOC = "4017-Y5-R2FR-kappa-sector-parent-insertion-or-Gref-residual-runner.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4017_kappa_sector_parent_insertion_or_Gref_residual_runner.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4016_00_handoff", SRC / "P8_Y5_R2FR_4015_NEXT_TARGET.csv", "NEXT4015_0", "4015 handoff"),
        ("SRC4016_01_4015_policy", SRC / "P8_Y5_R2FR_4015_GAUSS_POISSON_GREF_NEWTON_THEOREM.csv", "GPN4015_5_G_constant_policy", "4015 G constant policy"),
        ("SRC4016_02_4015_Grow", SRC / "P8_Y5_R2FR_4015_NEWTON_BRIDGE_FINITE_ROWS.csv", "NBR4015_11_epsilon_G_run", "4015 G running finite row"),
        ("SRC4016_03_4015_range", SRC / "P8_Y5_R2FR_4015_NEWTON_BRIDGE_FINITE_ROWS.csv", "NBR4015_12_epsilon_range", "4015 range finite row"),
        ("SRC4016_04_4015_Gkappa", SRC / "P8_Y5_R2FR_4015_NEWTON_BRIDGE_FINITE_ROWS.csv", "NBR4015_4_C_Gref_kappa", "4015 Gref/kappa row"),
        ("SRC4016_05_CU0", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU0_same_frame_EH_source", "same-frame EH source"),
        ("SRC4016_06_CU1", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU1_global_coupling_status", "global coupling status"),
        ("SRC4016_07_CU2", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU2_no_MTS_invariant_dependence", "no MTS invariant dependence"),
        ("SRC4016_08_CU3", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU3_species_source_blindness", "species/source blindness"),
        ("SRC4016_09_CU4", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU4_no_range_radial_running", "no range/radial running"),
        ("SRC4016_10_CU5", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU5_Bianchi_exchange_zero", "Bianchi exchange zero"),
        ("SRC4016_11_CU6", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU6_constant_only_calibration_policy", "constant-only calibration policy"),
        ("SRC4016_12_CU7", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU7_measured_GM_product_silence", "measured GM product silence"),
        ("SRC4016_13_CU8", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU8_retained_residual_fallback", "retained residual fallback"),
        ("SRC4016_14_GS0", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS0_configuration_factorization", "configuration factorization"),
        ("SRC4016_15_GS1", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS1_kappa_not_local_field", "kappa not local field"),
        ("SRC4016_16_GS2", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS2_trivial_MTS_action_on_kappa", "trivial MTS action on kappa"),
        ("SRC4016_17_GS3", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS3_no_species_marker_source_label", "no species/source marker"),
        ("SRC4016_18_GS4", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS4_no_range_radial_time_dependence", "no range/radial/time dependence"),
        ("SRC4016_19_GS5", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS5_Bianchi_arbitrary_source_consistency", "Bianchi arbitrary-source consistency"),
        ("SRC4016_20_GS6", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS6_constant_offset_policy", "constant offset policy"),
        ("SRC4016_21_GS7", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS7_scalar_branch_fallback", "scalar fallback"),
        ("SRC4016_22_GS8", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS8_evaluator_mapping", "evaluator mapping"),
        ("SRC4016_23_KGL0", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_0_delta_kappa", "delta kappa"),
        ("SRC4016_24_KGL1", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_1_zeta_w_common", "common matter action line"),
        ("SRC4016_25_KGL2", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_2_delta_ellJ", "source current normalization"),
        ("SRC4016_26_KGL3", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_3_R_frame", "frame normalization"),
        ("SRC4016_27_KGL4", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_4_Geff_product", "G product gate"),
        ("SRC4016_28_KGL5", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_5_epsilon_Gref_match", "Gref match guard"),
        ("SRC4016_29_Z1", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z1_global_coupling_superselection", "constant GM global coupling premise"),
        ("SRC4016_30_Z5", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z5_no_radial_or_range_hair", "constant GM radial/range premise"),
        ("SRC4016_31_Z7", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z7_parent_identity_cancellation", "no tuned cancellation premise"),
        ("SRC4016_32_decision", SRC / "P8_CONSTANT_GM_ZERO_OR_RESIDUAL_DECISION.csv", "constant_GM_promoted", "constant GM decision"),
        ("SRC4016_33_bound_Gdot", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_Geff_time_drift", "Gdot bound target"),
        ("SRC4016_34_bound_radial", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_radial_source_hair", "radial source hair target"),
        ("SRC4016_35_bound_range", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_range_dependence", "range target"),
        ("SRC4016_36_bound_frame", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_frame_calibration_split", "frame target"),
        ("SRC4016_37_bound_beta", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_nonlinear_beta_source_residue", "PPN beta target"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "GSS4016_0_global_sector_factorization",
            "claim_piece": "global coupling sector",
            "mathematical_form": "Q_parent ~= Q_dyn x K_G with kappa_* in K_G and T_local K_G=0; local compact-support variations satisfy delta_local kappa_*=0",
            "derived_result": "if the parent object language really factorizes this way, kappa is not a local scalar and has no local Euler-Lagrange hair",
            "status": "EXACT_CONDITIONAL_SUPERSELECTION_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GSS4016_1_no_Hom_to_coupling",
            "claim_piece": "no source/range/domain dependence",
            "mathematical_form": "Hom(source_label,K_G)=Hom(material_label,K_G)=Hom(range, K_G)=Hom(domain,K_G)=Hom(memory,K_G)=0",
            "derived_result": "without a morphism into the global coupling sector, partial_A kappa_*=partial_lambda kappa_*=partial_r kappa_*=partial_D kappa_*=0",
            "status": "EXACT_CONDITIONAL_NO_HOM_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GSS4016_2_same_branch_calibration",
            "claim_piece": "G_ref/kappa calibration identity",
            "mathematical_form": "G_ref := c^4 kappa_*/(8*pi) on the same branch, before source/readout; C_Gref_kappa=ln(kappa_eff c^4/(8*pi G_ref))=0",
            "derived_result": "the bridge can use one coupling consistently, but this is calibration of the constant, not a prediction of its numerical value",
            "status": "EXACT_CALIBRATION_IDENTITY_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GSS4016_3_derivative_silence",
            "claim_piece": "no Gdot/radial/range/source drift",
            "mathematical_form": "D_X ln G_ref=0 for X in {t,r,A,lambda,frame,domain,memory,projector} if G_ref descends from the same fixed kappa_* and X acts only on Q_dyn/readout data",
            "derived_result": "time, radial, source-label, range and frame drift are zero only under the global-sector/no-Hom clauses; otherwise they remain empirical residual rows",
            "status": "EXACT_CONDITIONAL_DERIVATIVE_ZERO",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GSS4016_4_Bianchi_guard",
            "claim_piece": "Bianchi cannot be abused",
            "mathematical_form": "nabla_mu(kappa T^{mu nu})=0 gives T^{mu nu} nabla_mu kappa + kappa nabla_mu T^{mu nu}=0; nabla kappa=0 follows only for arbitrary separately conserved same-frame sources",
            "derived_result": "Bianchi is a consistency gate, not a magic derivation of constant G when exchange/source terms remain open",
            "status": "ANTI_OVERCLAIM_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GSS4016_5_product_cancellation_guard",
            "claim_piece": "no tuned measured-GM cancellation",
            "mathematical_form": "D_X ln(G_eff M_eff(1+epsilon_mu))=0 cannot be used unless D_X ln G_eff, D_X ln M_eff and D_X ln(1+epsilon_mu) vanish separately or by a parent identity",
            "derived_result": "measured GM cannot hide a drifting coupling behind compensating source-mass or boundary terms",
            "status": "ANTI_TUNING_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GSS4016_6_absolute_G_policy",
            "claim_piece": "absolute Newton constant value",
            "mathematical_form": "constant_global shift in kappa_* is calibration-only unless parent action supplies a dimensionful normalization theorem for K_G",
            "derived_result": "4016 may close universality/drift, but not the numerical value of G",
            "status": "CALIBRATION_NOT_NUMERICAL_PREDICTION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GSS4016_7_finite_residual_vector",
            "claim_piece": "finite fallback if superselection is unsigned",
            "mathematical_form": "epsilon_Gref_superselection_4016 <= |C_sector|+|C_local_scalar|+|C_noHom|+|C_Gref_kappa|+|D_t lnG|/B_Gdot+L_r|partial_r lnG|+|partial_A lnG|+|partial_lambda lnG|+|partial_frame lnG|+|delta_kappa_exchange|+|C_product_tuning|+|C_absolute_G_claim|",
            "derived_result": "failed superselection clauses are now executable residual channels instead of hidden inside measured GM",
            "status": "FINITE_GREF_SUPERSELECTION_VECTOR_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("GCA4016_0_sector_factorization", "parent configuration splits dynamical fields from K_G", "UNSIGNED", "kappa may be a local scalar/source-normalization field", "derive parent action normal form or retain C_sector"),
        ("GCA4016_1_no_local_variation", "delta_local kappa_*=0 before local field variation", "UNSIGNED", "Gdot/fifth-force/scalar-tensor leakage", "derive zero-form/superselection status or retain C_local_scalar"),
        ("GCA4016_2_no_Hom", "no morphism from source/material/range/domain/memory labels into K_G", "UNSIGNED", "composition/range/domain-dependent active gravitational charge", "prove no-Hom object-language gate or retain partial_A/partial_lambda rows"),
        ("GCA4016_3_same_branch_calibration", "one kappa_* fixes EH, Hamiltonian, Poisson, Gauss and PPN comparison maps", "CONDITIONAL", "different effective G values can appear in different arenas", "bind to 4015 bridge and later PPN vector"),
        ("GCA4016_4_Bianchi", "Bianchi used only with separately conserved arbitrary same-frame matter", "GUARD_REQUIRED", "exchange terms can masquerade as constant-G proof", "retain delta_kappa_exchange unless exchange owners are zero"),
        ("GCA4016_5_product_tuning", "measured GM product silence is not tuned cancellation", "GUARD_REQUIRED", "drifting G hidden by drifting M_eff or mu_extra", "require separate zeros or parent identity"),
        ("GCA4016_6_absolute_value", "numerical value of G is not claimed from calibration", "POLICY_LOCKED", "overclaim that GR/MTS derives a measured dimensionful constant from Newtonian data", "keep absolute G as calibration until normalization theorem exists"),
    ]
    return [
        {
            "audit_id": audit_id,
            "clause": clause,
            "current_status": status,
            "risk_if_open": risk,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, clause, status, risk, next_action in rows
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("GREF4016_0_master", "epsilon_Gref_superselection_4016", "|C_sector|+|C_local_scalar|+|C_noHom|+|C_Gref_kappa|+|D_t lnG|/B_Gdot+L_r|partial_r lnG|+|partial_A lnG|+|partial_lambda lnG|+|partial_frame lnG|+|delta_kappa_exchange|+|C_product_tuning|+|C_absolute_G_claim|", "MISSING_PARENT_SIGNATURES_OR_NUMERIC_RESIDUALS", "dimensionless envelope", "G_ref superselection master row", "Gdot; R10; WEP; Newton; PPN; clocks"),
        ("GREF4016_1_C_sector", "C_sector", "failure of Q_parent ~= Q_dyn x K_G", "ZERO_IF_PARENT_GLOBAL_SECTOR_SIGNED_ELSE_RETAIN", "dimensionless", "coupling sector factorization", "Gdot; PPN"),
        ("GREF4016_2_C_local_scalar", "C_local_scalar", "indicator or coefficient for kappa in Gamma(E_local)", "ZERO_IF_KAPPA_NOT_LOCAL_FIELD_SIGNED_ELSE_RETAIN", "dimensionless", "local scalar coupling hair", "Gdot; fifth_force; PPN"),
        ("GREF4016_3_C_noHom", "C_noHom", "Hom(source/range/domain/memory,K_G) leakage", "ZERO_IF_NO_HOM_GATE_SIGNED_ELSE_RETAIN", "dimensionless", "source/range/domain coupling leakage", "WEP; R10; clocks"),
        ("GREF4016_4_C_Gref_kappa", "C_Gref_kappa", "ln(kappa_eff*c^4/(8*pi*G_ref))", "ZERO_IF_SAME_BRANCH_CALIBRATION_FIXED_ELSE_RETAIN", "dimensionless", "Gref/kappa arena mismatch", "Newton; PPN"),
        ("GREF4016_5_Gdot", "D_t_lnG", "D_t ln G_ref", "ZERO_IF_SUPERSELECTION_SIGNED_ELSE_BOUND_TARGET_9.6e-15_per_yr", "yr^-1", "time drift of G", "Gdot; clocks; orbital systems"),
        ("GREF4016_6_radial", "partial_r_lnG", "partial_r ln G_ref", "ZERO_IF_NO_RADIAL_HAIR_SIGNED_ELSE_PROFILE_REQUIRED", "inverse_length", "radial coupling hair", "R10; orbital systems"),
        ("GREF4016_7_source_species", "partial_A_lnG", "partial_A ln G_ref or source-label derivative", "ZERO_IF_NO_SOURCE_LABEL_HOM_SIGNED_ELSE_WEP_SOURCE_ROW", "dimensionless", "source/species active gravitational charge", "WEP; Newton"),
        ("GREF4016_8_range", "partial_lambda_lnG", "partial_lambda ln G_ref or alpha(lambda) projection", "ZERO_IF_NO_RANGE_HAIR_SIGNED_ELSE_ALPHA_CURVE_REQUIRED", "range-dependent", "finite-range coupling hair", "R10"),
        ("GREF4016_9_frame_domain", "partial_frame_domain_lnG", "partial_frame lnG + partial_domain lnG", "ZERO_IF_SAME_FRAME_DOMAIN_SIGNED_ELSE_RETAIN", "dimensionless", "frame/domain coupling split", "clocks; PPN"),
        ("GREF4016_10_Bianchi_exchange", "delta_kappa_exchange", "kappa^-1 P_loc[T_obs nabla kappa] or exchange-compensated divergence", "ZERO_IF_ARBITRARY_SOURCE_CONSERVATION_SIGNED_ELSE_RETAIN", "force density or dimensionless projection", "Bianchi exchange residual", "PPN; local_GR"),
        ("GREF4016_11_product_tuning", "C_product_tuning", "attempted cancellation in D_X ln(G_eff M_eff(1+epsilon_mu)) without parent identity", "FORBIDDEN_AS_PASS_INPUT", "dimensionless", "measured-GM cancellation guard", "Newton; Gdot"),
        ("GREF4016_12_absolute_G", "C_absolute_G_claim", "claim that calibration predicts numerical G without parent normalization theorem", "FORBIDDEN_OVERCLAIM", "dimensionless", "absolute G claim guard", "theory interpretation"),
    ]
    return [
        {
            "row_id": row_id,
            "coefficient": coefficient,
            "formula": formula,
            "value": value,
            "units": units,
            "role": role,
            "observable_links": links,
            "status": "FINITE_NONCLAIM_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, coefficient, formula, value, units, role, links in rows
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    cases = [
        ("CASE4016_0_full_superselection_signed", True, True, True, True, True, False, False, "all superselection and no-Hom clauses signed"),
        ("CASE4016_1_sector_open", False, True, True, True, True, False, False, "no parent factorization into global coupling sector"),
        ("CASE4016_2_local_scalar_kappa", True, False, True, True, True, False, False, "kappa behaves as local scalar field"),
        ("CASE4016_3_noHom_open", True, True, False, True, True, False, False, "source/range/domain Hom into coupling sector survives"),
        ("CASE4016_4_Bianchi_only_attempt", False, False, False, False, True, True, False, "tries to infer constant G from Bianchi alone"),
        ("CASE4016_5_product_cancellation_attempt", True, True, False, True, True, False, True, "tries to hide G drift inside measured GM product"),
        ("CASE4016_6_constant_offset_branch", True, True, True, True, True, False, False, "only a global constant offset remains"),
        ("CASE4016_7_numeric_residual_pack", False, False, False, False, False, False, False, "component rows exist but have no sourced numeric predictions"),
    ]
    return [
        {
            "case_id": case_id,
            "sector_factorized": sector,
            "not_local_scalar": not_local,
            "no_Hom": no_hom,
            "same_branch_calibration": same_branch,
            "separately_conserved_sources": conserved,
            "Bianchi_only": bianchi_only,
            "product_cancellation": product_cancel,
            "description": description,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for case_id, sector, not_local, no_hom, same_branch, conserved, bianchi_only, product_cancel, description in cases
    ]


def truthy(row: dict[str, Any], key: str) -> bool:
    return str(row[key]).lower() == "true" if isinstance(row[key], str) else bool(row[key])


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in cases:
        if truthy(row, "Bianchi_only"):
            owner_status = "BIANCHI_ONLY_CONSTANT_G_PROOF_REJECTED"
            residual_result = "delta_kappa_exchange"
            claim_result = "NO_CONSTANT_G_CLAIM"
            next_action = "prove arbitrary same-frame conserved sources or keep exchange residual"
        elif truthy(row, "product_cancellation"):
            owner_status = "MEASURED_GM_CANCELLATION_REJECTED"
            residual_result = "C_product_tuning"
            claim_result = "NO_MEASURED_GM_SILENCE_CLAIM"
            next_action = "require separate zeros or explicit parent identity"
        elif not truthy(row, "sector_factorized"):
            owner_status = "GREF_SUPERSELECTION_BLOCKED"
            residual_result = "C_sector"
            claim_result = "NO_GLOBAL_COUPLING_CLAIM"
            next_action = "insert or derive parent K_G coupling sector"
        elif not truthy(row, "not_local_scalar"):
            owner_status = "LOCAL_KAPPA_SCALAR_BRANCH_ACTIVE"
            residual_result = "C_local_scalar+D_t_lnG+partial_r_lnG"
            claim_result = "NO_GDOT_RANGE_SILENCE_CLAIM"
            next_action = "either prove kappa is not local or run scalar-coupling residual bounds"
        elif not truthy(row, "no_Hom"):
            owner_status = "SOURCE_RANGE_HOM_BLOCKED"
            residual_result = "C_noHom+partial_A_lnG+partial_lambda_lnG"
            claim_result = "NO_SOURCE_BLIND_OR_R10_CLAIM"
            next_action = "prove no-Hom gate or build source/range residual rows"
        elif not truthy(row, "same_branch_calibration"):
            owner_status = "GREF_KAPPA_CALIBRATION_BLOCKED"
            residual_result = "C_Gref_kappa"
            claim_result = "NO_NEWTON_COUPLING_MATCH_CLAIM"
            next_action = "bind EH/Hamiltonian/Poisson/PPN arenas to same kappa"
        elif row["case_id"] == "CASE4016_6_constant_offset_branch":
            owner_status = "GLOBAL_CONSTANT_CALIBRATION_ONLY"
            residual_result = "DERIVATIVE_ZERO_BUT_ABSOLUTE_VALUE_NOT_PREDICTED"
            claim_result = "UNIVERSALITY_CONDITIONAL_NO_NUMERICAL_G_CLAIM"
            next_action = "look for parent normalization theorem only after local universality is closed"
        elif row["case_id"] == "CASE4016_0_full_superselection_signed":
            owner_status = "CONDITIONAL_GREF_SUPERSELECTION_LOCK"
            residual_result = "D_t_D_r_D_A_D_lambda_D_frame_lnG_ZERO_IF_PARENT_SIGNED"
            claim_result = "CONSTANT_UNIVERSAL_GREF_CONDITIONAL_ONLY"
            next_action = "move to kappa-sector insertion or then PPN source stability"
        else:
            owner_status = "FINITE_GREF_RESIDUAL_PACK_NONCLAIM"
            residual_result = "FULL_GREF_DRIFT_RANGE_VECTOR_REQUIRED"
            claim_result = "NO_CLAIM"
            next_action = "source numeric residuals or parent-sign the zero theorem"
        rows.append(
            {
                "case_id": row["case_id"],
                "owner_status": owner_status,
                "residual_result": residual_result,
                "claim_result": claim_result,
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEC4016_0_theorem", "keep G_ref superselection as exact conditional theorem", "factorized global K_G sector plus no-Hom clauses would derive all local/range/source derivatives zero", "the coupling gap is now a parent action-sector problem"),
        ("DEC4016_1_Bianchi_guard", "reject Bianchi-only constant-G proof", "Bianchi permits exchange-compensated kappa gradients unless arbitrary same-frame conservation is signed", "delta_kappa_exchange remains live"),
        ("DEC4016_2_calibration_policy", "allow one constant G_ref calibration but no numerical-G prediction", "dimensionful measured constants need a parent normalization theorem to be predicted", "no absolute G claim"),
        ("DEC4016_3_no_tuned_GM", "reject measured-GM product cancellation", "a drifting G cannot be hidden by a drifting source charge without a parent identity", "Gdot/source residuals stay visible"),
        ("DEC4016_4_next", f"move to {NEXT_DOC}", "current files do not parent-sign K_G; best next work is to attempt the kappa-sector insertion or run residuals", "keeps derivation-first route alive"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            "effect": effect,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, rationale, effect in rows
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("CLAIM4016_0_superselection", "parent-owned G_ref superselection", False, "conditional theorem written but K_G sector not parent-signed"),
        ("CLAIM4016_1_Gdot", "Gdot/range/source drift zero", False, "derivative zeros require unsigned sector/no-Hom clauses"),
        ("CLAIM4016_2_absolute_G", "numerical value of G predicted", False, "calibration identity is not a dimensionful normalization theorem"),
        ("CLAIM4016_3_Newton", "Newton/local source coupling pass", False, "4015 bridge still needs Gref and charge/source closures"),
        ("CLAIM4016_4_local_GR", "local GR pass", False, "PPN second-order source stability remains open"),
    ]
    return [
        {
            "claim_id": claim_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for claim_id, claim, allowed, reason in gates
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4016_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "attempt to insert a minimal parent kappa/G_ref sector into the action grammar and prove it is global/no-Hom, otherwise emit executable Gdot/range/source residual rows",
            "success_condition": "K_G is parent-owned, not a local field, has no source/range/domain Hom, and calibrates EH/Hamiltonian/Poisson/PPN maps on the same branch; otherwise residual rows remain nonclaim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "G_ref/kappa superselection reduced to an exact conditional global-sector/no-Hom theorem with Bianchi, product-cancellation and absolute-G overclaim guards; drift/range/source finite rows retained.",
            "claim_allowed": False,
            "next_doc": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["needle_found"])
    lines = [
        "# 4016 - G_ref Superselection Universal Calibration Or Gdot/Range Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "This checkpoint attacks the coupling directly.",
        "",
        "The clean route is:",
        "",
        "`Q_parent ~= Q_dyn x K_G`, with `kappa_* in K_G` and `T_local K_G=0`.",
        "",
        "Then compact-support local variations obey `delta_local kappa_*=0`, so `kappa_*` is not a scalar field with local hair.",
        "",
        "The second required clause is the no-Hom gate:",
        "",
        "`Hom(source_label,K_G)=Hom(material_label,K_G)=Hom(range,K_G)=Hom(domain,K_G)=Hom(memory,K_G)=0`.",
        "",
        "If those clauses are parent-signed, then",
        "",
        "`D_X ln G_ref=0` for `X in {t,r,A,lambda,frame,domain,memory,projector}`.",
        "",
        "The same-branch calibration is simply",
        "",
        "`G_ref := c^4 kappa_*/(8*pi)`.",
        "",
        "That can make one universal coupling channel. It still does **not** predict the numerical value of `G`; it prevents source/range/time/frame drift once the parent sector is signed.",
        "",
        "## Bianchi Guard",
        "",
        "`nabla_mu(kappa T^{mu nu})=0` gives `T^{mu nu} nabla_mu kappa + kappa nabla_mu T^{mu nu}=0`.",
        "",
        "So Bianchi only forces `nabla kappa=0` in an arbitrary-source, same-frame, separately conserved matter branch. If exchange terms remain, the exchange row stays live. No magic constant-G proof.",
        "",
        "## Finite Residual Vector",
        "",
        "`epsilon_Gref_superselection_4016 <= |C_sector|+|C_local_scalar|+|C_noHom|+|C_Gref_kappa|+|D_t lnG|/B_Gdot+L_r|partial_r lnG|+|partial_A lnG|+|partial_lambda lnG|+|partial_frame lnG|+|delta_kappa_exchange|+|C_product_tuning|+|C_absolute_G_claim|`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: owner=`{row['owner_status']}`, residual=`{row['residual_result']}`, claim=`{row['claim_result']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is progress on the actual coupling problem. The theory now has a precise way to make `G_ref` universal without pretending to derive the measured number: parent-owned global coupling sector plus no-Hom into it. Current corpus does not yet parent-sign that sector, so claims stay blocked and residual rows remain live.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4016 - Gref Superselection Coupling Gate"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `G_ref/kappa` is reduced to an exact conditional global-sector theorem: `Q_parent ~= Q_dyn x K_G`, `kappa_* in K_G`, `T_local K_G=0`, plus no-Hom from source/material/range/domain/memory labels into `K_G`.
- If signed, `D_X ln G_ref=0` for `X={{t,r,A,lambda,frame,domain,memory,projector}}`, and one same-branch calibration `G_ref=c^4 kappa_*/(8*pi)` feeds EH, Hamiltonian, Poisson, Gauss and later PPN maps.
- Guard: Bianchi alone does not derive constant `G`; `nabla_mu(kappa T^{{mu nu}})=0` only forces `nabla kappa=0` for arbitrary separately conserved same-frame sources, otherwise `delta_kappa_exchange` remains live.
- Guard: measured `GM` product silence cannot hide tuned cancellation among `G_eff`, `M_eff`, and `mu_extra`.
- Finite fallback: `epsilon_Gref_superselection_4016 <= |C_sector|+|C_local_scalar|+|C_noHom|+|C_Gref_kappa|+|D_t lnG|/B_Gdot+L_r|partial_r lnG|+|partial_A lnG|+|partial_lambda lnG|+|partial_frame lnG|+|delta_kappa_exchange|+|C_product_tuning|+|C_absolute_G_claim|`.
- No claim: universal/drift-free `G_ref` is conditional; numerical `G` is not predicted.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4016 - Gref Superselection Coupling Gate" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4016_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4016_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, theorem_id in enumerate(
        [
            "GSS4016_0_global_sector_factorization",
            "GSS4016_1_no_Hom_to_coupling",
            "GSS4016_2_same_branch_calibration",
            "GSS4016_3_derivative_silence",
            "GSS4016_4_Bianchi_guard",
            "GSS4016_5_product_cancellation_guard",
            "GSS4016_6_absolute_G_policy",
            "GSS4016_7_finite_residual_vector",
        ],
        start=2,
    ):
        add(f"VAL4016_{idx:02d}_theorem", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    for idx, audit_id in enumerate(
        [
            "GCA4016_0_sector_factorization",
            "GCA4016_1_no_local_variation",
            "GCA4016_2_no_Hom",
            "GCA4016_3_same_branch_calibration",
            "GCA4016_4_Bianchi",
            "GCA4016_5_product_tuning",
            "GCA4016_6_absolute_value",
        ],
        start=10,
    ):
        add(f"VAL4016_{idx:02d}_audit", any(row["audit_id"] == audit_id for row in audit), f"{audit_id} present")
    master = next(row for row in finite if row["row_id"] == "GREF4016_0_master")
    add("VAL4016_17_master_vector", "D_t lnG" in master["formula"] and "C_absolute_G_claim" in master["formula"], "master vector contains drift and absolute-G guards")
    for idx, row_id in enumerate(
        [
            "GREF4016_1_C_sector",
            "GREF4016_2_C_local_scalar",
            "GREF4016_3_C_noHom",
            "GREF4016_4_C_Gref_kappa",
            "GREF4016_5_Gdot",
            "GREF4016_6_radial",
            "GREF4016_7_source_species",
            "GREF4016_8_range",
            "GREF4016_9_frame_domain",
            "GREF4016_10_Bianchi_exchange",
            "GREF4016_11_product_tuning",
            "GREF4016_12_absolute_G",
        ],
        start=18,
    ):
        add(f"VAL4016_{idx:02d}_{row_id}", any(row["row_id"] == row_id for row in finite), f"{row_id} present")
    case_lookup = {row["case_id"]: row for row in results}
    add("VAL4016_30_full_case", case_lookup["CASE4016_0_full_superselection_signed"]["owner_status"] == "CONDITIONAL_GREF_SUPERSELECTION_LOCK", "full superselection case locks conditionally")
    add("VAL4016_31_sector_case", case_lookup["CASE4016_1_sector_open"]["residual_result"] == "C_sector", "sector-open case routed")
    add("VAL4016_32_local_scalar_case", "D_t_lnG" in case_lookup["CASE4016_2_local_scalar_kappa"]["residual_result"], "local scalar case activates Gdot/radial rows")
    add("VAL4016_33_noHom_case", "partial_lambda_lnG" in case_lookup["CASE4016_3_noHom_open"]["residual_result"], "no-Hom failure activates source/range rows")
    add("VAL4016_34_Bianchi_guard", case_lookup["CASE4016_4_Bianchi_only_attempt"]["owner_status"] == "BIANCHI_ONLY_CONSTANT_G_PROOF_REJECTED", "Bianchi-only proof rejected")
    add("VAL4016_35_product_guard", case_lookup["CASE4016_5_product_cancellation_attempt"]["owner_status"] == "MEASURED_GM_CANCELLATION_REJECTED", "product cancellation rejected")
    add("VAL4016_36_constant_offset", case_lookup["CASE4016_6_constant_offset_branch"]["owner_status"] == "GLOBAL_CONSTANT_CALIBRATION_ONLY", "constant offset treated as calibration")
    add("VAL4016_37_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4016_38_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4016_39_doc_exists", DOC_PATH.exists() and "Q_parent ~= Q_dyn x K_G" in read_text(DOC_PATH), "document written with global-sector theorem")
    add("VAL4016_40_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4016_41_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4016_42_compile", compile_ok, "script compiles")
    add("VAL4016_43_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [
        sources,
        theorem,
        audit,
        finite,
        results,
        read_csv(OUTPUTS["decision"]),
        read_csv(OUTPUTS["claim_gate"]),
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4016_44_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4016_45_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4016_46_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4016_47_no_absolute_G_claim", "does **not** predict the numerical value of `G`" in read_text(DOC_PATH), "absolute G value not claimed")
    add("VAL4016_48_Bianchi_text", "Bianchi only forces" in read_text(DOC_PATH), "Bianchi guard recorded")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    finite = finite_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, theorem, audit, finite, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4016 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
