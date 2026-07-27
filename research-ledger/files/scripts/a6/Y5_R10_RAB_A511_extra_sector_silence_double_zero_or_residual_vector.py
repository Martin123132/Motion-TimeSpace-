from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


PACK_ID = "P8_Y5_R10_1279"
TITLE = "1279-Y5-R10-RAB-A511-extra-sector-silence-double-zero-or-residual-vector"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "source-intake" / "mts_residuals"
RAB_INTAKE_DIR = ROOT / "source-intake" / "rab-sector"
DOC_PATH = ROOT / f"{TITLE}.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
RUN_STARTED_UTC = datetime.now(timezone.utc)


SOURCE_REGISTER_PATH = OUT_DIR / f"{PACK_ID}_SOURCE_REGISTER.csv"
EXTRA_LEDGER_PATH = OUT_DIR / f"{PACK_ID}_A511_EXTRA_SECTOR_LEDGER.csv"
DOUBLE_ZERO_PATH = OUT_DIR / f"{PACK_ID}_DOUBLE_ZERO_SILENCE_AUDIT.csv"
RESIDUAL_VECTOR_PATH = OUT_DIR / f"{PACK_ID}_EXTRA_SECTOR_RESIDUAL_VECTOR.csv"
EH_IMPACT_PATH = OUT_DIR / f"{PACK_ID}_EH_INHERITANCE_IMPACT.csv"
VALIDATOR_RESCAN_PATH = OUT_DIR / f"{PACK_ID}_ZR_VALIDATOR_RESCAN.csv"
CLAIM_GATES_PATH = OUT_DIR / f"{PACK_ID}_CLAIM_GATES.csv"
DECISION_PATH = OUT_DIR / f"{PACK_ID}_DECISION_LEDGER.csv"
NEXT_PATH = OUT_DIR / f"{PACK_ID}_NEXT_TARGET.csv"
VALIDATION_PATH = OUT_DIR / "P8_Y5_BRR545_1279_VALIDATION.csv"


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


def validate_intake_row(path: Path, intake_class: str, row: dict[str, str]) -> dict[str, object]:
    row_id = row.get("row_id") or row.get("template_id") or row.get("coefficient_symbol") or "MISSING_ROW_ID"
    required_columns = [
        "coefficient_symbol",
        "coefficient_value",
        "coefficient_units",
        "normalization_convention",
        "parent_action_block",
        "source_path",
        "source_anchor",
        "arena_projection",
        "valid_for_claim",
        "claim_allowed",
    ]
    missing_columns = [column for column in required_columns if column not in row]
    source_raw = str(row.get("source_path", "")).strip()
    anchor = str(row.get("source_anchor", "")).strip()
    source = None if not source_raw or source_raw.startswith("MISSING_") else source_path(source_raw)
    source_exists = bool(source and source.exists())
    anchor_found = bool(source_exists and anchor and not anchor.startswith("MISSING_") and anchor in read_text(source))
    reasons: list[str] = []
    if intake_class == "docs":
        reasons.append("DOCS_TEMPLATE_NOT_LIVE_INTAKE")
    if missing_columns:
        reasons.append("MISSING_REQUIRED_COLUMNS:" + ";".join(missing_columns))
    if contains_missing_marker(row):
        reasons.append("MISSING_MARKER_PRESENT")
    if source is None:
        reasons.append("SOURCE_PATH_MISSING_OR_PLACEHOLDER")
    elif not source_exists:
        reasons.append("SOURCE_PATH_NOT_FOUND")
    if not anchor or anchor.startswith("MISSING_"):
        reasons.append("SOURCE_ANCHOR_MISSING_OR_PLACEHOLDER")
    elif source_exists and not anchor_found:
        reasons.append("SOURCE_ANCHOR_NOT_FOUND")
    if str(row.get("valid_for_claim", "")).strip().lower() == "true" or str(row.get("claim_allowed", "")).strip().lower() == "true":
        reasons.append("CLAIM_FLAG_TRUE_REJECTED_IN_PRIVATE_NONCLAIM_PHASE")
    return {
        "scan_id": f"SCAN1279_{intake_class}_{path.stem}_{row_id}",
        "intake_class": intake_class,
        "file_path": str(path),
        "row_id": row_id,
        "coefficient_symbol": row.get("coefficient_symbol", ""),
        "status": "REJECT" if reasons else "ACCEPT_NONCLAIM_SOURCE_READY",
        "reasons": "|".join(reasons) if reasons else "NO_PLACEHOLDERS_SOURCE_ANCHOR_FOUND_NONCLAIM",
        "source_exists": source_exists,
        "anchor_found": anchor_found,
        "intake_eligible": not reasons,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def scan_rab_intake() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for intake_class in ["docs", "raw", "accepted"]:
        directory = RAB_INTAKE_DIR / intake_class
        directory.mkdir(parents=True, exist_ok=True)
        for path in sorted(directory.glob("*.csv")):
            for row in read_csv(path):
                results.append(validate_intake_row(path, intake_class, row))
    return results


def generated_inside_formalization() -> list[Path]:
    generated_paths = [
        SOURCE_REGISTER_PATH,
        EXTRA_LEDGER_PATH,
        DOUBLE_ZERO_PATH,
        RESIDUAL_VECTOR_PATH,
        EH_IMPACT_PATH,
        VALIDATOR_RESCAN_PATH,
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
            "source_id": "SRC1279_0_1278_next",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1278_NEXT_TARGET.csv",
            "needle": "NEXT1278_0_1279",
            "purpose": "handoff into A511_3 extra-sector silence audit",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_1_1278_priority",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1278_A511_ORIGIN_PRIORITY_LADDER.csv",
            "needle": "APL1278_0_extra_silence",
            "purpose": "A511_3 selected as next derivation target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_2_A511_block",
            "local_path": "source-intake/mts_residuals/P8_MIN_PARENT_LOCAL_GR_ACTION_BLOCKS.csv",
            "needle": "A511_3_extra_field_silence",
            "purpose": "extra-field silence fixed-point requirement",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_3_zero_chain_stress",
            "local_path": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv",
            "needle": "V5_delta_g_stress",
            "purpose": "metric-stress debt blocks local-GR promotion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_4_zero_chain_source",
            "local_path": "source-intake/mts_residuals/P8_PARENT_LOCAL_ZERO_VARIATION_CHAIN.csv",
            "needle": "V7_R11_source",
            "purpose": "source-normalization/non-EH operator debt",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_5_symbol_gamma",
            "local_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "needle": "Gamma_eff",
            "purpose": "Gamma/Khat/q_loc extra residual channel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_6_symbol_memory",
            "local_path": "source-intake/mts_residuals/P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
            "needle": "memory / B_mem / U_mem / I_M",
            "purpose": "memory channel requiring local double-zero origin",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_7_1009_GK",
            "local_path": "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needle": "SVC1009_1_GK_missing_action",
            "purpose": "Gamma/Khat parent action existence blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_8_1010_verdict",
            "local_path": "1010-Y5-R10-Gamma-Khat-action-existence-Helmholtz-or-q_loc-residual-retention.md",
            "needle": "GKT1010_6_verdict",
            "purpose": "Gamma/Khat/q_loc zero route written but not closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "source_id": "SRC1279_9_validator",
            "local_path": "source-intake/mts_residuals/P8_Y5_R10_1269_ZR_INTAKE_VALIDATOR_SUMMARY.csv",
            "needle": "NO_ACCEPTED_SOURCE_READY_ROWS",
            "purpose": "finite residual source rows remain absent",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    extra_ledger = [
        {
            "channel_id": "XSL1279_0_generic_Phi",
            "sector": "generic_extra_fields",
            "candidate_parent_block": "A511_3_extra_field_silence",
            "needed_silence": "Phi=Phi0; dV(Phi0)=0; Hessian(V)>0; C(Phi0)=0; dC(Phi0)=0; local stress zero",
            "current_evidence": "A511 block states requirement but does not derive it",
            "status": "REQUIREMENT_NOT_PARENT_DERIVED",
            "fallback_component": "epsilon_extra_generic_metric_stress",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "channel_id": "XSL1279_1_Gamma_Khat_q_loc",
            "sector": "Gamma_eff/K_hat/q_loc",
            "candidate_parent_block": "A511_3_extra_field_silence plus A511_6 readout",
            "needed_silence": "S_GK exists; metric response matches K_hat; Helmholtz passes; Euler closure and double-zero make q_loc=0",
            "current_evidence": "1010 retains q_loc as explicit nonclaim residual",
            "status": "BLOCKED_BY_ACTION_EXISTENCE_HELMHOLTZ",
            "fallback_component": "epsilon_GK_q_loc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "channel_id": "XSL1279_2_memory",
            "sector": "memory/B_mem/U_mem/I_M",
            "candidate_parent_block": "A511_3 extra silence plus A511_4 projector selector",
            "needed_silence": "memory activation is chi_D^2/double-zero locally and smooth/controlled cosmologically",
            "current_evidence": "symbol map marks memory as empirically interesting conditional EFT not parent-derived",
            "status": "BLOCKED_BY_MEMORY_DOUBLE_ZERO_ORIGIN",
            "fallback_component": "epsilon_memory_activation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "channel_id": "XSL1279_3_range_transition",
            "sector": "L_cg/ell_tr/range scale",
            "candidate_parent_block": "A511_3 extra silence and domain/operator spectrum",
            "needed_silence": "local branch has no arena switch and range/tail contributions are zero or source-bounded",
            "current_evidence": "symbol map keeps ell_tr/L_cg open",
            "status": "BLOCKED_BY_SCALE_ORIGIN",
            "fallback_component": "epsilon_extra_range_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "channel_id": "XSL1279_4_domain_kinematics",
            "sector": "u^mu/h/X/Qcoh/chi_D",
            "candidate_parent_block": "A511_4 with overlap into A511_3 stress",
            "needed_silence": "local stationary compact branch forces X_D=0, Qcoh_D=0, projector stress=0",
            "current_evidence": "zero chain has formal partial passes but V4/V5/V6 remain claim-blocked",
            "status": "BLOCKED_BY_DOMAIN_PROJECTOR_STRESS",
            "fallback_component": "epsilon_domain_projector_stress",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "channel_id": "XSL1279_5_boundary_symplectic",
            "sector": "K_hat/boundary/symplectic spillover",
            "candidate_parent_block": "A511_3 plus A511_5",
            "needed_silence": "boundary/symplectic contribution is exact, fixed, or zero in local exterior",
            "current_evidence": "1009 marks missing theta/Q_tau contributions",
            "status": "BLOCKED_BY_THETA_QTAU_BOUNDARY",
            "fallback_component": "epsilon_extra_boundary_symplectic",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    double_zero = [
        {
            "audit_id": "DZS1279_0_background_amplitude",
            "condition": "extra fields sit at local fixed point Phi=Phi0",
            "required_evidence": "parent Euler equations force Phi0 on stationary compact/local branch",
            "current_status": "NOT_PARENT_SIGNED",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_fail": "epsilon_extra_background_amplitude",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DZS1279_1_first_variation",
            "condition": "dV(Phi0)=0 and all linear couplings vanish",
            "required_evidence": "source/equation paths for every retained extra field",
            "current_status": "MISSING_FIELD_BY_FIELD_PROOF",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_fail": "epsilon_extra_first_variation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DZS1279_2_Hessian_positive",
            "condition": "Hessian(V)>0 or positive operator gives local stability/no hair",
            "required_evidence": "mass gap/operator spectrum for motion/time/domain/memory/range sectors",
            "current_status": "MISSING_SPECTRAL_CERTIFICATE",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_fail": "epsilon_extra_range_tail",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DZS1279_3_curvature_coupling",
            "condition": "C(Phi0)=0 and dC(Phi0)=0 for non-EH curvature couplings",
            "required_evidence": "action-level coupling map and variation",
            "current_status": "MISSING_COUPLING_CERTIFICATE",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_fail": "epsilon_extra_curvature_coupling",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DZS1279_4_metric_stress",
            "condition": "delta_g S_extra=0 or topological/silent locally",
            "required_evidence": "V5_delta_g_stress cleared and no hidden stress certificate",
            "current_status": "BLOCKED_BY_V5_STRESS_DEBT",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_fail": "epsilon_extra_metric_stress",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DZS1279_5_source_normalization",
            "condition": "extra sector carries no source-normalized Newton/PPN/R10 charge locally",
            "required_evidence": "V7_R11_source cleared and same-frame source map signed",
            "current_status": "BLOCKED_BY_V7_SOURCE_DEBT",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_fail": "epsilon_extra_source_charge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DZS1279_6_GK_q_loc",
            "condition": "Gamma/Khat/q_loc derives zero from action existence, Helmholtz, Euler closure, double-zero, and boundary",
            "required_evidence": "1010 GKT1010_0..6 pass",
            "current_status": "BLOCKED_BY_1010_FAIL_CURRENT_CLAIM",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_fail": "epsilon_GK_q_loc",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "audit_id": "DZS1279_7_verdict",
            "condition": "A511_3 extra-sector silence is parent-derived",
            "required_evidence": "DZS1279_0..6 all pass",
            "current_status": "NOT_DERIVED",
            "result": "EXTRA_SILENCE_NOT_CLOSED",
            "residual_if_fail": "retain full extra-sector residual vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    residual_vector = [
        {
            "residual_id": "XRV1279_0_metric_stress",
            "component": "epsilon_extra_metric_stress",
            "formula_or_bound_needed": "abs(delta_g S_extra projected into local EH equations)/M_ref or equivalent dimensionless norm",
            "source_status": "MISSING_PARENT_STRESS_CERTIFICATE_OR_NUMERIC_BOUND",
            "maps_to_tests": "PPN;local_GR;R11_EH_operator_ledger",
            "current_status": "RETAIN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "XRV1279_1_source_charge",
            "component": "epsilon_extra_source_charge",
            "formula_or_bound_needed": "source-normalized extra charge relative to measured GM/source mass",
            "source_status": "MISSING_SOURCE_NORMALIZATION_CERTIFICATE",
            "maps_to_tests": "Newton;R10;WEP;PPN",
            "current_status": "RETAIN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "XRV1279_2_GK_q_loc",
            "component": "epsilon_GK_q_loc",
            "formula_or_bound_needed": "norm of P_loc(nabla Gamma_eff - div K_hat) after Euler/boundary projection",
            "source_status": "MISSING_S_GK_HELMHOLTZ_EULER_DOUBLE_ZERO_BOUNDARY_CERTIFICATES",
            "maps_to_tests": "PPN;clock;orbital;local_GR",
            "current_status": "RETAIN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "XRV1279_3_memory_activation",
            "component": "epsilon_memory_activation",
            "formula_or_bound_needed": "local memory amplitude/exposure after chi_D or double-zero suppression",
            "source_status": "MISSING_MEMORY_DOUBLE_ZERO_OR_LOCAL_SUPPRESSION_CERTIFICATE",
            "maps_to_tests": "cosmology;clock;PPN;R10",
            "current_status": "RETAIN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "XRV1279_4_range_tail",
            "component": "epsilon_extra_range_tail",
            "formula_or_bound_needed": "finite-range Yukawa/spectral envelope or theorem-zero for local range tail",
            "source_status": "MISSING_MASS_GAP_OR_RANGE_ENVELOPE",
            "maps_to_tests": "R10;PPN;orbital",
            "current_status": "RETAIN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "XRV1279_5_curvature_coupling",
            "component": "epsilon_extra_curvature_coupling",
            "formula_or_bound_needed": "non-EH curvature coupling and first derivative at Phi0",
            "source_status": "MISSING_C_PHI_ZERO_AND_DCPHI_ZERO_CERTIFICATE",
            "maps_to_tests": "PPN;local_GR;cosmology",
            "current_status": "RETAIN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "residual_id": "XRV1279_6_boundary_symplectic",
            "component": "epsilon_extra_boundary_symplectic",
            "formula_or_bound_needed": "boundary/symplectic flux contribution to local Hamiltonian/readout",
            "source_status": "MISSING_THETA_QTAU_BOUNDARY_CERTIFICATE",
            "maps_to_tests": "source_measure;orbital;local_GR",
            "current_status": "RETAIN_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    eh_impact = [
        {
            "impact_id": "EHI1279_0_A511_3_status",
            "dependency": "A511_3_extra_field_silence",
            "current_status": "BLOCKED",
            "effect_on_EH_inheritance": "local EH fixed point remains blocked even if EH core anchor exists",
            "next_action": "attack the concrete GK/q_loc first-variation route or source residual vector components",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "impact_id": "EHI1279_1_closure_runner",
            "dependency": "1278 local closure firewall",
            "current_status": "PROTECTS_TESTS",
            "effect_on_EH_inheritance": "closure tests cannot hide extra-sector leakage as derivation",
            "next_action": "keep closure_only labels through any local benchmark run",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    validator_rescan = scan_rab_intake()
    docs_rows = [row for row in validator_rescan if row["intake_class"] == "docs"]
    raw_rows = [row for row in validator_rescan if row["intake_class"] == "raw"]
    accepted_rows = [row for row in validator_rescan if row["intake_class"] == "accepted"]
    accepted_ready = [row for row in validator_rescan if row["intake_eligible"] and row["intake_class"] in {"raw", "accepted"}]

    claim_gates = [
        {
            "gate_id": "GATE1279_0_A511_3_silence",
            "claim": "A511_3 extra-sector silence is parent-derived",
            "status": "BLOCKED",
            "reason": "double-zero, Hessian, curvature-coupling, metric-stress, source, and GK/q_loc clauses remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1279_1_EH_inheritance",
            "claim": "MTS inherits local EH fixed point",
            "status": "BLOCKED",
            "reason": "A511_3 remains a blocker before readout/projector/boundary gates are even reached",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1279_2_residual_vector",
            "claim": "extra-sector residual vector is claim-bounded",
            "status": "BLOCKED",
            "reason": "residual components are named but not source-bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1279_3_finite_rows",
            "claim": "finite residual rows can be scored",
            "status": "BLOCKED",
            "reason": f"docs={len(docs_rows)} raw={len(raw_rows)} accepted={len(accepted_rows)} accepted_ready={len(accepted_ready)}",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "gate_id": "GATE1279_4_local_tests",
            "claim": "local GR/Newton/R10/PPN/clock/orbital pass",
            "status": "BLOCKED",
            "reason": "extra-sector silence is not derived and residuals are not bounded",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    decisions = [
        {
            "decision_id": "DEC1279_0_silence_result",
            "decision": "do not promote A511_3 extra-sector silence",
            "because": "the double-zero/Hessian/source/stress chain is not parent-signed",
            "status": "EXTRA_SILENCE_NOT_CLOSED",
            "next_action": "attack Gamma_eff/K_hat/q_loc first-variation route as the sharpest concrete subproblem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1279_1_residual_vector",
            "decision": "retain a full extra-sector residual vector",
            "because": "surviving extra channels must be named before any local test can be trusted",
            "status": "RESIDUAL_VECTOR_WRITTEN_NONCLAIM",
            "next_action": "turn components into source-backed bounds or parent-zero certificates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "decision_id": "DEC1279_2_next_target",
            "decision": "prioritize Gamma/Khat/q_loc action existence and double-zero",
            "because": "1010 already localizes the hardest concrete A511_3 residual channel",
            "status": "GK_QLOC_SELECTED",
            "next_action": "reopen S_GK/Helmholtz/Euler/double-zero/boundary route in the A511_3 context",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]

    next_target = [
        {
            "next_id": "NEXT1279_0_1280",
            "target_file": "1280-Y5-R10-RAB-Gamma-Khat-qloc-action-existence-or-extra-residual-bound.md",
            "target_script": "scripts/Y5_R10_RAB_Gamma_Khat_qloc_action_existence_or_extra_residual_bound.py",
            "task": "try to close the Gamma_eff/K_hat/q_loc first-variation route inside A511_3 by proving action existence, metric response, Helmholtz integrability, Euler closure, double-zero, and boundary silence; if this fails, make epsilon_GK_q_loc a source-bound residual row",
            "success_condition": "q_loc is parent-zero on the local branch, or epsilon_GK_q_loc is retained with a strict source/bound contract",
            "do_not": "do not use plateau, closure-only local tests, or EH anchor-only import to set q_loc=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]

    generated_tables = [
        (SOURCE_REGISTER_PATH, source_register),
        (EXTRA_LEDGER_PATH, extra_ledger),
        (DOUBLE_ZERO_PATH, double_zero),
        (RESIDUAL_VECTOR_PATH, residual_vector),
        (EH_IMPACT_PATH, eh_impact),
        (VALIDATOR_RESCAN_PATH, validator_rescan),
        (CLAIM_GATES_PATH, claim_gates),
        (DECISION_PATH, decisions),
        (NEXT_PATH, next_target),
    ]
    for path, rows in generated_tables:
        write_csv(path, rows)

    source_checks = [exists_and_contains(row["local_path"], row["needle"]) for row in source_register]
    all_sources_exist = all(exists for exists, _ in source_checks)
    all_needles_found = all(found for _, found in source_checks)
    ledger_has_core_channels = {row["fallback_component"] for row in extra_ledger} >= {
        "epsilon_GK_q_loc",
        "epsilon_memory_activation",
        "epsilon_extra_range_tail",
        "epsilon_extra_boundary_symplectic",
    }
    silence_not_closed = any(
        row["audit_id"] == "DZS1279_7_verdict" and row["result"] == "EXTRA_SILENCE_NOT_CLOSED"
        for row in double_zero
    )
    residual_vector_complete = {row["component"] for row in residual_vector} >= {
        "epsilon_extra_metric_stress",
        "epsilon_extra_source_charge",
        "epsilon_GK_q_loc",
        "epsilon_memory_activation",
        "epsilon_extra_range_tail",
        "epsilon_extra_curvature_coupling",
        "epsilon_extra_boundary_symplectic",
    }
    eh_blocked_by_A511_3 = any(
        row["impact_id"] == "EHI1279_0_A511_3_status" and row["current_status"] == "BLOCKED"
        for row in eh_impact
    )
    docs_rejected = len(docs_rows) > 0 and all(row["status"] == "REJECT" for row in docs_rows)
    no_live_rows = len(raw_rows) == 0 and len(accepted_rows) == 0 and len(accepted_ready) == 0
    claim_gates_blocked = all(row["status"] == "BLOCKED" for row in claim_gates)
    all_generated_rows = [
        *source_register,
        *extra_ledger,
        *double_zero,
        *residual_vector,
        *eh_impact,
        *validator_rescan,
        *claim_gates,
        *decisions,
        *next_target,
    ]
    nonclaim_policy = all(is_false(row.get("valid_for_claim")) and is_false(row.get("claim_allowed")) for row in all_generated_rows)
    formalization_generated = generated_inside_formalization()

    parsed_details = []
    csv_parse_ok = True
    for path, _rows in generated_tables:
        try:
            parsed_rows = read_csv(path)
            parsed_details.append(f"{path.name}:{len(parsed_rows)}")
        except Exception as exc:
            csv_parse_ok = False
            parsed_details.append(f"{path.name}:ERROR:{exc}")

    validation = [
        validation_row(
            "VAL1279_0_sources_exist",
            "all cited local sources exist",
            all_sources_exist,
            f"{sum(1 for exists, _ in source_checks if exists)}/{len(source_checks)} sources exist",
        ),
        validation_row(
            "VAL1279_1_needles_found",
            "all cited local needles found",
            all_needles_found,
            f"{sum(1 for _, found in source_checks if found)}/{len(source_checks)} needles found",
        ),
        validation_row(
            "VAL1279_2_extra_ledger",
            "extra-sector ledger covers core A511_3 leakage channels",
            ledger_has_core_channels,
            f"extra_ledger_rows={len(extra_ledger)}",
        ),
        validation_row(
            "VAL1279_3_silence_not_closed",
            "double-zero silence theorem is not promoted",
            silence_not_closed,
            "DZS1279_7_verdict=EXTRA_SILENCE_NOT_CLOSED",
        ),
        validation_row(
            "VAL1279_4_residual_vector",
            "extra-sector residual vector is explicit",
            residual_vector_complete,
            f"residual_vector_rows={len(residual_vector)}",
        ),
        validation_row(
            "VAL1279_5_EH_impact",
            "EH inheritance remains blocked by A511_3",
            eh_blocked_by_A511_3,
            "EHI1279_0_A511_3_status=BLOCKED",
        ),
        validation_row(
            "VAL1279_6_finite_fallback_locked",
            "finite branch has no source-backed accepted rows",
            docs_rejected and no_live_rows,
            f"docs_rows={len(docs_rows)}; raw_rows={len(raw_rows)}; accepted_rows={len(accepted_rows)}; accepted_ready={len(accepted_ready)}",
        ),
        validation_row(
            "VAL1279_7_claim_gates_blocked",
            "all claim gates remain blocked",
            claim_gates_blocked,
            f"claim_gate_rows={len(claim_gates)}",
        ),
        validation_row(
            "VAL1279_8_nonclaim_policy",
            "all generated rows remain nonclaim",
            nonclaim_policy,
            "valid_for_claim=false and claim_allowed=false throughout generated tables",
        ),
        validation_row(
            "VAL1279_9_next_target_1280",
            "next target routes to Gamma/Khat/q_loc action existence or residual bound",
            next_target[0]["next_id"] == "NEXT1279_0_1280",
            str(next_target[0]["target_file"]),
        ),
        validation_row(
            "VAL1279_10_csv_parse",
            "all generated CSVs parse cleanly",
            csv_parse_ok,
            "; ".join(parsed_details),
        ),
        validation_row(
            "VAL1279_11_formalization_untouched",
            "formalization-workbench untouched by generated outputs",
            len(formalization_generated) == 0,
            f"formalization_generated_output_count={len(formalization_generated)}",
        ),
    ]
    overall_pass = all(row["status"] == "PASS" for row in validation)
    validation.append(
        validation_row(
            "VAL1279_12_overall",
            "overall 1279 validation",
            overall_pass,
            "1279 attempts A511_3 extra-sector silence, blocks the double-zero theorem, retains an explicit extra-sector residual vector, and selects Gamma/Khat/q_loc as the next sharp subtarget",
        )
    )
    write_csv(VALIDATION_PATH, validation)

    doc = f"""# {TITLE}

**Current verdict:** 1279 does not derive A511_3 extra-sector silence. The double-zero/Hessian/source/stress chain is not parent-signed, and `Gamma_eff/K_hat/q_loc`, memory, range, curvature coupling, metric stress, source charge, and boundary/symplectic channels must remain explicit residuals.

**Main progress:** the extra-sector blocker is no longer vague. Every live leakage channel is now named in a residual vector, so the local closure runner cannot hide extra stress/source leakage behind `C_R=0`.

**Next derivation target:** the sharpest concrete subproblem is `Gamma_eff/K_hat/q_loc`, because 1010 already shows the exact action-existence/Helmholtz/Euler/double-zero/boundary route needed to make `q_loc=0` real rather than a plateau axiom.

**No-claim guard:** no A511_3 silence, EH inheritance, local-GR/Newton, R10, PPN, clock, orbital, zero-residual, or finite residual branch is claim-valid.

Run timestamp UTC: `{RUN_STARTED_UTC.isoformat()}`

## Source Register
{markdown_table(source_register, ["source_id", "local_path", "needle", "purpose", "valid_for_claim", "claim_allowed"])}

## A511 Extra-Sector Ledger
{markdown_table(extra_ledger, ["channel_id", "sector", "candidate_parent_block", "needed_silence", "current_evidence", "status", "fallback_component", "valid_for_claim", "claim_allowed"])}

## Double-Zero Silence Audit
{markdown_table(double_zero, ["audit_id", "condition", "required_evidence", "current_status", "result", "residual_if_fail", "valid_for_claim", "claim_allowed"])}

## Extra-Sector Residual Vector
{markdown_table(residual_vector, ["residual_id", "component", "formula_or_bound_needed", "source_status", "maps_to_tests", "current_status", "valid_for_claim", "claim_allowed"])}

## EH Inheritance Impact
{markdown_table(eh_impact, ["impact_id", "dependency", "current_status", "effect_on_EH_inheritance", "next_action", "valid_for_claim", "claim_allowed"])}

## Z_R Validator Rescan
{markdown_table(validator_rescan, ["scan_id", "intake_class", "row_id", "coefficient_symbol", "status", "reasons", "source_exists", "anchor_found", "intake_eligible", "valid_for_claim", "claim_allowed"])}

## Claim Gates
{markdown_table(claim_gates, ["gate_id", "claim", "status", "reason", "valid_for_claim", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "because", "status", "next_action", "valid_for_claim", "claim_allowed"])}

## Next Target
{markdown_table(next_target, ["next_id", "target_file", "target_script", "task", "success_condition", "do_not", "valid_for_claim", "claim_allowed"])}

## Validation
{markdown_table(validation, ["check_id", "check", "status", "details"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


if __name__ == "__main__":
    main()
