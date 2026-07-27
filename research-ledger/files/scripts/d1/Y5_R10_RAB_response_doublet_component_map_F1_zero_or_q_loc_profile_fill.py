from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1282"
TITLE = "1282-Y5-R10-RAB-response-doublet-component-map-F1-zero-or-q_loc-profile-fill"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
COMPONENT_MAP_PATH = OUT_DIR / f"{PACK_ID}_RESPONSE_DOUBLET_COMPONENT_MAP_AUDIT.csv"
F1_ZERO_PATH = OUT_DIR / f"{PACK_ID}_F1_ZERO_THEOREM_AUDIT.csv"
PROFILE_REQUIREMENTS_PATH = OUT_DIR / f"{PACK_ID}_QLOC_PROFILE_FILL_REQUIREMENTS.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1282_VALIDATION.csv"


def source_path(relative_path: str) -> Path:
    path = Path(relative_path)
    if path.is_absolute():
        return path
    return ROOT / path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join(["---"] * len(fields)) + " |",
            *["| " + " | ".join(md_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def exists_and_contains(relative_path: str, needle: str) -> tuple[bool, bool]:
    path = source_path(relative_path)
    if not path.exists():
        return False, False
    if not needle:
        return True, True
    return True, needle in read_text(path)


def validation_row(check_id: str, check: str, passed: bool, details: str) -> dict[str, object]:
    return {
        "check_id": check_id,
        "check": check,
        "status": "PASS" if passed else "FAIL",
        "details": details,
    }


def is_false(value: object) -> bool:
    return str(value).strip().lower() in {"false", "0", "no"}


def contains_missing_marker(row: dict[str, object]) -> bool:
    return any("MISSING_" in str(value) for value in row.values())


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        COMPONENT_MAP_PATH,
        F1_ZERO_PATH,
        PROFILE_REQUIREMENTS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
        VALIDATION_PATH,
        DOC_PATH,
    ]
    return [path for path in generated_paths if FORMALIZATION in path.parents]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    source_register = [
        {
            "source_id": "SRC1282_0_1281_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1281_NEXT_TARGET.csv",
            "needle": "NEXT1281_0_1282",
            "role": "handoff into response-doublet component map or q_loc profile fill",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_1_doublet_contract_ppn",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "needle": "RD516_5_PPN_lock",
            "role": "explicit PPN/physical lock requirement for response-doublet theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_2_doublet_contract_source",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_CONTRACT.csv",
            "needle": "RD516_4_zero_odd_source",
            "role": "source and boundary charge silence requirement",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_3_doublet_variation_F1",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            "needle": "AV517_3_double_zero",
            "role": "formal F1 double-zero route",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_4_doublet_variation_euler",
            "local_path": "source-intake/mts_residuals/P8_RESPONSE_DOUBLET_ACTION_VARIATION.csv",
            "needle": "AV517_4_Euler_equation",
            "role": "Euler source-current obstruction",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_5_517_obstruction",
            "local_path": "517-response-doublet-action-variation-ledger-or-run-q_loc-bound.md",
            "needle": "OB517_2_PPN_lock",
            "role": "historical obstruction: Z can be auxiliary unless locked to measured residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_6_1011_lock",
            "local_path": "1011-Y5-R10-response-doublet-source-current-zero-or-q_loc-bound-fill.md",
            "needle": "RDT1011_6_PPN_lock",
            "role": "later proof attempt kept PPN lock blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_7_757_physical_lock",
            "local_path": "757-Y5-R10-response-doublet-physical-lock-or-real-q_loc-component-input.md",
            "needle": "PLC757_1_lock_map",
            "role": "full residual-vector lock contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_8_1281_profile_template",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1281_EPSILON_GK_QLOC_PROFILE_TEMPLATE_NONCLAIM.csv",
            "needle": "GKQ1281_TEMPLATE_DO_NOT_SCORE",
            "role": "invalid-by-design q_loc profile template to fill if theorem route fails",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_9_1281_tensor_contract",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1281_METRIC_RESPONSE_TENSOR_CONTRACT.csv",
            "needle": "MRT1281_1_Ward_consequence",
            "role": "1281 Ward consequence remains blocked by metric-response and Euler gaps",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1282_10_1279_residual",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1279_EXTRA_SECTOR_RESIDUAL_VECTOR.csv",
            "needle": "XRV1279_2_GK_q_loc",
            "role": "retained epsilon_GK_q_loc residual channel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    for row in source_register:
        exists, needle_found = exists_and_contains(str(row["local_path"]), str(row["needle"]))
        row["exists"] = exists
        row["needle_found"] = needle_found

    component_map = [
        {
            "map_id": "RCM1282_0_doublet_variables",
            "physical_channel": "response-doublet variables",
            "candidate_identification": "Z^A=(R_+^A-R_-^A)/2",
            "needed_for_claim": "parent exchange doublets cover every physical local residual channel",
            "current_evidence": "RD516_0 is partial/conditional; 517 and 1011 keep component derivation open",
            "status": "CONDITIONAL_AUXILIARY_VARIABLES_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "RCM1282_1_q_loc_vector_lock",
            "physical_channel": "q_loc^nu = P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu})",
            "candidate_identification": "Z_q^nu equals normalized q_loc^nu components in observed local frame",
            "needed_for_claim": "sourced Gamma_eff, K_hat, P_loc, units, and a full-rank Z_q to q_loc map",
            "current_evidence": "1281 has missing Gamma_eff formula, K_hat formula, metric variation, and Delta_K ledger",
            "status": "NOT_DERIVED_MISSING_GK_PLOC_PROFILE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "RCM1282_2_Y5_source_normalization_lock",
            "physical_channel": "measured source strength / Newton normalization",
            "candidate_identification": "Z_mu controls epsilon_mu and every source-normalization offset",
            "needed_for_claim": "source current closure, no extra mass projection, Gauss/orbital calibration, and PPN stability",
            "current_evidence": "517 and 1011 mark Y5 source normalization as exchange-even and hard-fail for odd-doublet erasure",
            "status": "FAILS_CURRENT_ROUTE_EXCHANGE_EVEN_SOURCE_SCALAR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "RCM1282_3_Y6_extra_stress_lock",
            "physical_channel": "non-EH local stress",
            "candidate_identification": "Z_T controls conserved/topological extra stress components",
            "needed_for_claim": "extra stress is topological/invisible or explicitly below PPN/operator bounds",
            "current_evidence": "Y6 can be conserved and Bianchi-silent while still metric-visible",
            "status": "NOT_DERIVED_CONSERVED_KERNEL_POSSIBLE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "RCM1282_4_PPN_vector_lock",
            "physical_channel": "Delta PPN_A = {gamma-1,beta-1,alpha_i,xi,zeta_i,Gdot,R11}",
            "candidate_identification": "Z_PPN has invertible response to full PPN residual vector",
            "needed_for_claim": "source-backed linear response operator from Z to PPN coefficients through tested order",
            "current_evidence": "RD516_5, OB517_2, RDT1011_6, and PLC757_1 all keep PPN lock unsigned",
            "status": "NOT_DERIVED_NO_RESPONSE_OPERATOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "RCM1282_5_boundary_coupling_lock",
            "physical_channel": "boundary/harmonic flux plus matter/source/readout coupling",
            "candidate_identification": "Z_H and Z_coupling control q_H, species/frame/source/photon/clock/orbit residuals",
            "needed_for_claim": "no-flux theorem plus one quotient-invariant matter/source/readout action",
            "current_evidence": "boundary metric response and full quotient-invariant matter/source/readout descent remain unsigned",
            "status": "NOT_DERIVED_BOUNDARY_AND_COUPLING_OPEN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "map_id": "RCM1282_6_verdict",
            "physical_channel": "full physical residual vector",
            "candidate_identification": "Z=0 implies q_loc=Y5=Y6=DeltaPPN=q_H=DeltaCoupling=0",
            "needed_for_claim": "RCM1282_0..5 all parent-signed and full-rank/coercive",
            "current_evidence": "multiple physical channels remain outside the proven auxiliary doublet map",
            "status": "COMPONENT_MAP_NOT_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    f1_zero_audit = [
        {
            "f1_id": "FZ1282_0_formal_quadratic_double_zero",
            "claim": "Gamma_eff = Gamma0 + 1/2 M_AB Z^A Z^B + O(Z^4) gives partial_A Gamma_eff|Z=0=0",
            "source_anchor": "AV517_2_first_variation_Z; AV517_3_double_zero",
            "current_status": "FORMAL_CONDITIONAL_PASS",
            "why_not_enough": "formal F1=0 only zeros the auxiliary Z response",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "f1_id": "FZ1282_1_physical_state_identification",
            "claim": "Z=0 is identical to the real local residual state",
            "source_anchor": "RD516_5_PPN_lock; PLC757_1_lock_map",
            "current_status": "FAIL_NOT_PARENT_SIGNED",
            "why_not_enough": "q_loc, Y5, Y6, PPN, boundary, and coupling residuals can sit outside Z or in ker(N)",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "f1_id": "FZ1282_2_no_linear_source_work",
            "claim": "J_A=0 and B_A=0 in the compact local branch",
            "source_anchor": "RD516_4_zero_odd_source; AV517_4_Euler_equation",
            "current_status": "FAIL_SOURCE_BOUNDARY_OPEN",
            "why_not_enough": "linear source or boundary work can drive a nonzero residual despite a quadratic potential",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "f1_id": "FZ1282_3_positive_coercive_operator",
            "claim": "M_AB/L_AB is positive after gauge and constraint removal",
            "source_anchor": "RD516_3_positive_operator; AV517_5_positive_theorem",
            "current_status": "CONDITIONAL_ONLY",
            "why_not_enough": "positivity on an auxiliary sector does not control un-mapped physical channels",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "f1_id": "FZ1282_4_metric_response_lock",
            "claim": "K_hat is the metric response of sqrt(-g) Gamma_eff with no leftover Delta_K",
            "source_anchor": "MRT1281_1_Ward_consequence",
            "current_status": "FAIL_METRIC_RESPONSE_AND_EULER_GAPS",
            "why_not_enough": "1281 blocked the Ward consequence because symbol/tensor variation inputs are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "f1_id": "FZ1282_5_verdict",
            "claim": "F1=0 proves q_loc^nu=0 and local PPN silence",
            "source_anchor": "RCM1282_6_verdict",
            "current_status": "FORMAL_DOUBLE_ZERO_NOT_PHYSICAL_QLOC_ZERO",
            "why_not_enough": "component map, no-linear-source, metric-response, and coercive full residual norm are all unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    profile_requirements = [
        {
            "requirement_id": "QPF1282_0_q_loc_formula",
            "profile_field": "q_loc_profile_formula",
            "required_content": "explicit q_loc^nu(x)=P_loc(nabla^nu Gamma_eff - nabla_mu K_hat^{mu nu}) profile or parent-zero theorem",
            "current_value": "MISSING_Q_LOC_PROFILE_FORMULA",
            "acceptance_gate": "source equation plus local branch domain/frame",
            "status": "MISSING_REQUIRED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPF1282_1_Gamma_eff",
            "profile_field": "Gamma_eff_formula",
            "required_content": "sourced Gamma_eff scalar/density with background subtraction and units",
            "current_value": "MISSING_GAMMA_EFF_FORMULA",
            "acceptance_gate": "same symbol used in variation, metric response, and local projection",
            "status": "MISSING_REQUIRED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPF1282_2_K_hat",
            "profile_field": "K_hat_formula",
            "required_content": "sourced K_hat^{mu nu} tensor and comparison to metric-response K_metric",
            "current_value": "MISSING_K_HAT_FORMULA;MISSING_DELTA_K_COMPARISON",
            "acceptance_gate": "Delta_K=0 theorem or explicit retained Delta_K residual bound",
            "status": "MISSING_REQUIRED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPF1282_3_P_loc",
            "profile_field": "P_loc_definition",
            "required_content": "local projector definition, domain, boundary conditions, and observed-frame pullback",
            "current_value": "MISSING_P_LOC_DEFINITION",
            "acceptance_gate": "projector is the same object used for PPN/clock/orbital arenas",
            "status": "MISSING_REQUIRED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPF1282_4_norm_units",
            "profile_field": "q_loc_units;norm_definition;normalization_reference",
            "required_content": "dimensioned q_loc units and dimensionless local norm A_loc or equivalent",
            "current_value": "MISSING_Q_LOC_UNITS;MISSING_LOCAL_NORM_DEFINITION;MISSING_A_REF_OR_DIMENSIONLESS_GATE",
            "acceptance_gate": "numeric bound can be compared to arena thresholds without hidden unit conversion",
            "status": "MISSING_REQUIRED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPF1282_5_arena_bounds",
            "profile_field": "arena_bound_threshold;bound_units",
            "required_content": "source-backed local thresholds for PPN, clock, orbital, local-GR, and R10 if relevant",
            "current_value": "MISSING_ARENA_BOUND_THRESHOLD;MISSING_BOUND_UNITS",
            "acceptance_gate": "each bound has source path, source anchor, units, and valid_for_claim=true only after all formula fields close",
            "status": "MISSING_REQUIRED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPF1282_6_no_cancellation",
            "profile_field": "cancellation_policy",
            "required_content": "no cancellation-based local pass unless protected by symmetry/identity",
            "current_value": "MISSING_PARENT_ZERO_CERTIFICATE",
            "acceptance_gate": "either theorem_zero or source-backed finite residual below every arena gate",
            "status": "MISSING_REQUIRED_INPUT",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "requirement_id": "QPF1282_7_row_status",
            "profile_field": "profile_row_liveness",
            "required_content": "template can become live only after QPF1282_0..6 close",
            "current_value": "GKQ1281_TEMPLATE_DO_NOT_SCORE",
            "acceptance_gate": "no MISSING_* markers; source anchors found; all claim flags still independently reviewed",
            "status": "TEMPLATE_REMAINS_INVALID_BY_DESIGN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    claim_gates = [
        {
            "gate_id": "CG1282_0_response_doublet_physical_zero",
            "claim": "response-doublet theorem proves physical local residual vector is zero",
            "required": "component map full-rank/coercive and no source/boundary work",
            "current_status": "BLOCKED_COMPONENT_MAP_NOT_CLOSED",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1282_1_q_loc_zero",
            "claim": "q_loc^nu=0",
            "required": "F1 zero applies to physical q_loc and Gamma/Khat/P_loc metric-response chain closes",
            "current_status": "BLOCKED_FORMAL_DOUBLE_ZERO_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1282_2_local_GR_PPN",
            "claim": "local GR/Newton/PPN silence",
            "required": "q_loc, Y5, Y6, PPN vector, boundary, and coupling residuals all zero or bounded",
            "current_status": "BLOCKED_RETAINED_RESIDUAL_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "CG1282_3_profile_bound_branch",
            "claim": "finite q_loc profile can be scored",
            "required": "all QPF1282 profile fields filled from source-backed equations/units/bounds",
            "current_status": "BLOCKED_TEMPLATE_INVALID",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decision = [
        {
            "decision_id": "DEC1282_0_formal_route_survives",
            "decision": "Keep the response-doublet mechanism as a real formal clue, not a claim.",
            "because": "It does produce a clean F1=0 shape for auxiliary Z variables when source and boundary terms vanish.",
            "next_action": "Use it only if the physical component map and no-linear-source theorem are parent-signed.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1282_1_current_route_blocked",
            "decision": "Do not promote the response-doublet double-zero to q_loc/local-GR silence.",
            "because": "q_loc, source normalization, extra stress, PPN coefficients, boundary flux, and coupling are not locked to Z.",
            "next_action": "Treat epsilon_GK_q_loc as retained and fill the q_loc profile/source contract or derive the missing projector/metric-response owners.",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1282_2_best_next_target",
            "decision": "Attack the q_loc profile fields directly, starting with P_loc/Gamma_eff/K_hat ownership.",
            "because": "The theorem path cannot close until the same physical objects are sourced anyway.",
            "next_action": "build 1283 q_loc profile source-fill or P_loc projector-owner gate",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1282_0_1283",
            "target_file": "1283-Y5-R10-RAB-q_loc-profile-source-fill-or-P_loc-projector-owner.md",
            "target_script": "scripts/Y5_R10_RAB_q_loc_profile_source_fill_or_Ploc_projector_owner.py",
            "task": "try to source or derive the concrete P_loc, Gamma_eff, K_hat, units, norm, and local arena bounds needed to turn epsilon_GK_q_loc from an invalid template into either a theorem-zero certificate or a finite nonclaim residual profile",
            "success_condition": "P_loc/Gamma_eff/K_hat are parent-sourced with compatible units and local domain, or the q_loc finite-profile row remains explicitly unscoreable with a blocker ledger",
            "do_not": "do not infer q_loc=0 from auxiliary response-doublet F1=0 and do not score placeholder profile rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_register)
    write_csv(COMPONENT_MAP_PATH, component_map)
    write_csv(F1_ZERO_PATH, f1_zero_audit)
    write_csv(PROFILE_REQUIREMENTS_PATH, profile_requirements)
    write_csv(CLAIM_GATES_PATH, claim_gates)
    write_csv(DECISION_PATH, decision)
    write_csv(NEXT_PATH, next_target)

    validations: list[dict[str, object]] = []
    validations.append(
        validation_row(
            "VAL1282_0_sources_exist",
            "all cited local sources exist",
            all(bool(row["exists"]) for row in source_register),
            f"{sum(bool(row['exists']) for row in source_register)}/{len(source_register)} sources exist",
        )
    )
    validations.append(
        validation_row(
            "VAL1282_1_needles_found",
            "all cited local needles found",
            all(bool(row["needle_found"]) for row in source_register),
            f"{sum(bool(row['needle_found']) for row in source_register)}/{len(source_register)} needles found",
        )
    )
    verdict = next(row for row in component_map if row["map_id"] == "RCM1282_6_verdict")
    validations.append(
        validation_row(
            "VAL1282_2_component_map_not_closed",
            "response-doublet map to physical residual vector is not closed",
            verdict["status"] == "COMPONENT_MAP_NOT_CLOSED" and is_false(verdict["valid_for_claim"]),
            "RCM1282_6_verdict=COMPONENT_MAP_NOT_CLOSED",
        )
    )
    f1_verdict = next(row for row in f1_zero_audit if row["f1_id"] == "FZ1282_5_verdict")
    validations.append(
        validation_row(
            "VAL1282_3_f1_formal_only",
            "formal F1 double-zero is not promoted to physical q_loc zero",
            f1_verdict["current_status"] == "FORMAL_DOUBLE_ZERO_NOT_PHYSICAL_QLOC_ZERO" and is_false(f1_verdict["valid_for_claim"]),
            "FZ1282_5_verdict=FORMAL_DOUBLE_ZERO_NOT_PHYSICAL_QLOC_ZERO",
        )
    )
    validations.append(
        validation_row(
            "VAL1282_4_profile_requirements_blocked",
            "q_loc profile requirements remain explicit missing inputs",
            all(contains_missing_marker(row) and is_false(row["valid_for_claim"]) for row in profile_requirements),
            f"profile_requirement_rows={len(profile_requirements)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1282_5_claim_gates_blocked",
            "all claim gates remain blocked",
            all("BLOCKED" in str(row["current_status"]) and is_false(row["claim_allowed"]) for row in claim_gates),
            f"claim_gate_rows={len(claim_gates)}",
        )
    )
    generated_tables = [
        SOURCE_REGISTER_PATH,
        COMPONENT_MAP_PATH,
        F1_ZERO_PATH,
        PROFILE_REQUIREMENTS_PATH,
        CLAIM_GATES_PATH,
        DECISION_PATH,
        NEXT_PATH,
    ]
    parse_details: list[str] = []
    csv_parse_ok = True
    for table_path in generated_tables:
        try:
            row_count = len(read_csv(table_path))
            parse_details.append(f"{table_path.name}:{row_count}")
        except Exception as exc:
            csv_parse_ok = False
            parse_details.append(f"{table_path.name}:ERROR:{exc}")
    validations.append(
        validation_row(
            "VAL1282_6_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parse_details),
        )
    )
    next_ok = next_target[0]["next_id"] == "NEXT1282_0_1283" and "P_loc" in str(next_target[0]["task"])
    validations.append(
        validation_row(
            "VAL1282_7_next_target_1283",
            "next target routes to q_loc profile source-fill or P_loc projector owner",
            next_ok,
            str(next_target[0]["target_file"]),
        )
    )
    formalization_hits = generated_inside_formalization()
    validations.append(
        validation_row(
            "VAL1282_8_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            not formalization_hits,
            f"formalization_generated_output_count={len(formalization_hits)}",
        )
    )
    validations.append(
        validation_row(
            "VAL1282_9_nonclaim_policy",
            "all generated rows remain nonclaim",
            all(
                is_false(row.get("valid_for_claim", False)) and is_false(row.get("claim_allowed", False))
                for rows in [source_register, component_map, f1_zero_audit, profile_requirements, claim_gates, decision, next_target]
                for row in rows
            ),
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        )
    )

    overall_pass = all(row["status"] == "PASS" for row in validations)
    validations.append(
        validation_row(
            "VAL1282_10_overall",
            "overall 1282 validation",
            overall_pass,
            "1282 keeps the response-doublet F1=0 as formal-only, blocks physical q_loc/local-GR promotion, and routes to concrete q_loc profile/P_loc ownership next",
        )
    )
    write_csv(VALIDATION_PATH, validations)

    doc = f"""# 1282 Y5 R10 RAB response-doublet component map F1 zero or q_loc profile fill

Generated: `{RUN_STARTED_UTC.isoformat()}`

**Current verdict:** 1282 does not derive physical `q_loc^nu=0`. The response-doublet route still has a beautiful formal move — quadratic/even `Gamma_eff` gives `F_1=0` at `Z=0` — but the current corpus does not prove that `Z=0` is the real local residual state.

**Main progress:** the exact missing bridge is now sharper: `Z` must be a full-rank/coercive coordinate on the physical residual vector, including `q_loc`, source normalization, extra stress, PPN coefficients, boundary flux, and matter/source/readout coupling. That bridge is not signed, so `epsilon_GK_q_loc` remains retained.

**Next derivation target:** fill or derive the concrete `q_loc` profile objects: `P_loc`, `Gamma_eff`, `K_hat`, units, norm, and local arena bounds. Same beast, less fog.

## Source Register

{markdown_table(source_register, ["source_id", "local_path", "needle", "exists", "needle_found", "role", "valid_for_claim", "claim_allowed"])}

## Response-Doublet Component Map Audit

{markdown_table(component_map, ["map_id", "physical_channel", "candidate_identification", "needed_for_claim", "current_evidence", "status", "valid_for_claim", "claim_allowed"])}

## F1 Zero Theorem Audit

{markdown_table(f1_zero_audit, ["f1_id", "claim", "source_anchor", "current_status", "why_not_enough", "valid_for_claim", "claim_allowed"])}

## q_loc Profile Fill Requirements

{markdown_table(profile_requirements, ["requirement_id", "profile_field", "required_content", "current_value", "acceptance_gate", "status", "valid_for_claim", "claim_allowed"])}

## Claim Gates

{markdown_table(claim_gates, ["gate_id", "claim", "required", "current_status", "valid_for_claim", "claim_allowed"])}

## Decision Ledger

{markdown_table(decision, ["decision_id", "decision", "because", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation

{markdown_table(validations, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
