from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2932"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2932-Y5-R2FR-kappa-ellJ-constant-proof-or-first-coupling-source-bound-under-AX1090.md"

SRC_2931_DOC = ROOT / "2931-Y5-R2FR-parent-source-coefficient-theorem-or-first-finite-local-residual-value-under-AX1090.md"
SRC_2931_NEXT = RESIDUALS / "P8_Y5_R2FR_2931_NEXT_TARGET.csv"
SRC_2931_RESIDUAL = RESIDUALS / "P8_Y5_R2FR_2931_MTS_COEFFICIENT_RESIDUAL_DECOMPOSITION.csv"
SRC_2931_CANDIDATES = RESIDUALS / "P8_Y5_R2FR_2931_FIRST_FINITE_VALUE_CANDIDATE_ROWS.csv"
SRC_2931_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2931_VALIDATION.csv"

SRC_2928_COUPLING = RESIDUALS / "P8_Y5_R2FR_2928_KAPPA_ELLJ_COUPLING_BASELINE_ROWS.csv"
SRC_2918_DOC = ROOT / "2918-Y5-R2FR-alpha3-source-current-kernel-or-no-disformal-slot-theorem-under-AX1090.md"
SRC_2918_COUPLING = RESIDUALS / "P8_Y5_R2FR_2918_COUPLING_OWNER_GATES.csv"
SRC_2918_PRODUCTS = RESIDUALS / "P8_Y5_R2FR_2918_ALPHA3_PRODUCT_BOUND_ROWS.csv"
SRC_2578_DOC = ROOT / "2578-Y5-R2FR-PiM-Hamiltonian-coupling-identity-or-source-backed-residual-fill.md"
SRC_2578_GATE = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_COUPLING_BASELINE_GATE.csv"
SRC_2578_LEDGER = RESIDUALS / "P8_Y5_PIM_HAMILTONIAN_COUPLING_2578_RESIDUAL_INPUT_LEDGER.csv"
SRC_2578_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2578_VALIDATION.csv"
SRC_2695_DOC = ROOT / "2695-Y5-R2FR-kappa-topological-superselection-parent-adoption-or-drift-residual-values.md"
SRC_2695_KAPPA = RESIDUALS / "P8_Y5_R2FR_2695_KAPPA_RESIDUAL_VALUE_REQUIREMENTS_NONCLAIM.csv"
SRC_KAPPA_MAP = RESIDUALS / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2932_SOURCE_REGISTER.csv",
    "constant_audit": RESIDUALS / "P8_Y5_R2FR_2932_KAPPA_ELLJ_CONSTANT_PROOF_AUDIT.csv",
    "kappa_reentry": RESIDUALS / "P8_Y5_R2FR_2932_TOPOLOGICAL_KAPPA_REENTRY_AUDIT.csv",
    "bound_ledger": RESIDUALS / "P8_Y5_R2FR_2932_COUPLING_FIRST_BOUND_ACQUISITION_LEDGER.csv",
    "impact": RESIDUALS / "P8_Y5_R2FR_2932_ALPHA3_BETA_NEWTON_IMPACT.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2932_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2932_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2932_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2932_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2932_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "constant_audit_copy": PARENT_ACTION / "Kappa_ellJ_constant_proof_audit_2932_NONCLAIM.csv",
    "bound_ledger_copy": LOCAL_BOUNDS / "Coupling_first_bound_acquisition_ledger_2932_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2932_KAPPA_DRIFT_SOURCE_BOUND_OR_ELLJ_OWNER_NEXT_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2932_00_2931_doc", SRC_2931_DOC, "NEXT2931_0_2932;Dln(kappa_MTS);Dln(ell_J);Validation overall: `True`", "2931 selected kappa/ellJ constant proof or first finite bound"),
        ("SRC2932_01_2931_next", SRC_2931_NEXT, "NEXT2931_0_2932;Dln(kappa_MTS);Dln(ell_J)", "machine-readable 2932 target"),
        ("SRC2932_02_2931_residual", SRC_2931_RESIDUAL, "CRD2931_5_coupling;Delta_coupling_source_abs", "coefficient residual coupling decomposition"),
        ("SRC2932_03_2931_candidates", SRC_2931_CANDIDATES, "FVC2931_3_Dln_kappa;FVC2931_4_Dln_ellJ", "first finite value candidates"),
        ("SRC2932_04_2931_validation", SRC_2931_VALIDATION, "VAL2931_OVERALL;True", "2931 validation summary"),
        ("SRC2932_05_2928_coupling", SRC_2928_COUPLING, "CB2928_0_kappa_alpha3;CB2928_1_ellJ_alpha3;CB2928_3_coupling_total", "kappa/ellJ local coupling rows"),
        ("SRC2932_06_2918_doc", SRC_2918_DOC, "A3K2918_4_kappa;A3K2918_5_ellJ;COUP2918_7_verdict", "alpha3 source-current kernel narrative"),
        ("SRC2932_07_2918_coupling", SRC_2918_COUPLING, "COUP2918_3_kappa;COUP2918_4_ellJ;COUP2918_7_verdict", "coupling owner gates"),
        ("SRC2932_08_2918_products", SRC_2918_PRODUCTS, "A3P2918_3_kappa;A3P2918_4_ellJ;A3P2918_6_total", "alpha3 product bound rows"),
        ("SRC2932_09_2578_doc", SRC_2578_DOC, "COG2578_0_kappa_constant;COG2578_2_ellJ_source_scale;VAL2578_OVERALL", "PiM/Hamiltonian coupling checkpoint"),
        ("SRC2932_10_2578_gate", SRC_2578_GATE, "COG2578_0_kappa_constant;COG2578_2_ellJ_source_scale;COG2578_4_verdict", "coupling baseline gate"),
        ("SRC2932_11_2578_ledger", SRC_2578_LEDGER, "RES2578_7_delta_kappa;RES2578_8_delta_ellJ;RES2578_9_total", "coupling residual input ledger"),
        ("SRC2932_12_2578_validation", SRC_2578_VALIDATION, "VAL2578_OVERALL;PASS", "2578 validation summary"),
        ("SRC2932_13_2695_doc", SRC_2695_DOC, "S_kappa_top = int_M kappa_eff dA_3;KAD2695_8_verdict;ZFD2695_7_verdict", "topological kappa parent adoption audit"),
        ("SRC2932_14_2695_kappa", SRC_2695_KAPPA, "KRR2695_0_time_drift;KRR2695_2_range_dependence;KRR2695_5_bianchi_exchange", "kappa residual value requirements"),
        ("SRC2932_15_kappa_map", SRC_KAPPA_MAP, "KR508_0_time_drift;KR508_2_range_dependence;KR508_5_Bianchi_exchange", "constant-kappa residual map"),
    ]
    rows = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def constant_audit_rows() -> list[dict[str, Any]]:
    specs = [
        ("KLC2932_0_kappa_route", "kappa_MTS constant route", "S_kappa_top=int_M kappa_eff dA_3 -> d kappa_eff=0", "PASS_CONDITIONAL_FROM_2695", "mathematical zero-gradient route exists if parent topological sector is adopted", True),
        ("KLC2932_1_kappa_parent_adoption", "kappa parent adoption", "A_3, kappa_eff, companion equation, stress silence, source blindness and boundary policy parent-signed", "PARENT_ADOPTION_FAILS_CURRENT_CORPUS", "2695 keeps field content/source blindness/boundary policy unsigned", False),
        ("KLC2932_2_kappa_observed_constant", "observed coupling constant", "Dln(kappa_MTS)=0 in local source/orbit/readout frame", "NOT_DERIVED_CURRENT_MTS", "zero-form spacetime constancy is not enough without source/frame/domain blindness and G_ref match", False),
        ("KLC2932_3_ellJ_owner", "ell_J source-current scale ownership", "ell_J fixed by parent matter/source-current normalization before readout", "SOURCE_SCALE_OWNER_OPEN", "2578/2928 name the gate but do not provide a parent owner theorem", False),
        ("KLC2932_4_no_reference_absorption", "no reference/readout absorption", "H_tau reference, boundary subtraction and measured GM cannot absorb kappa or ell_J shifts", "REFERENCE_ABSORPTION_NOT_EXCLUDED", "2578 leaves boundary/reference coupling silence open", False),
        ("KLC2932_5_coupling_total", "coupling baseline package", "Dln(kappa_MTS)=Dln(ell_J)=epsilon_Gref_match=Delta_boundary_coupling=0", "COUPLING_BASELINE_IDENTITY_NOT_DERIVED", "the package is source-ready but values/theorem-zeros are missing", False),
        ("KLC2932_6_verdict", "kappa/ellJ constant proof for current MTS", "constant-coupling theorem sufficient to remove these local GR residual heads", "CONSTANT_COUPLING_THEOREM_NOT_DERIVED_FIRST_BOUND_LEDGER_STAGED", "keep kappa route conditional and stage finite acquisition rows", False),
    ]
    return [
        add_common(
            {
                "audit_id": audit_id,
                "clause": clause,
                "required_identity": required_identity,
                "current_status": current_status,
                "reason": reason,
                "condition_passed": condition_passed,
                "adopted_for_claim": False,
                "source_paths": ";".join(str(path) for path in [SRC_2695_DOC, SRC_2578_GATE, SRC_2928_COUPLING, SRC_2918_COUPLING]),
            }
        )
        for audit_id, clause, required_identity, current_status, reason, condition_passed in specs
    ]


def kappa_reentry_rows() -> list[dict[str, Any]]:
    specs = [
        ("KTR2932_0_action", "candidate topological sector", "S_kappa_top = int_M kappa_eff dA_3", "ROUTE_EXISTS_CONDITIONAL", "clean non-plateau route; this is not just asserting kappa is constant"),
        ("KTR2932_1_A3_variation", "A_3 variation", "delta_A S = -int d kappa_eff wedge delta A_3 + boundary", "MATHEMATICAL_STEP_VALID_CONDITIONAL", "gives d kappa_eff=0 if A_3 and boundary policy are parent-owned"),
        ("KTR2932_2_connected_domain", "connected local domain", "d kappa_eff=0 -> kappa_eff=kappa_D", "CONDITIONAL_DOMAIN_CONSTANT", "local spacetime constancy follows only inside the parent topological branch"),
        ("KTR2932_3_companion", "kappa companion equation", "delta_kappa S gives only global/topological constraints", "UNSIGNED_COMPANION_EQUATION", "otherwise the route becomes scalar-tensor/source-current hair"),
        ("KTR2932_4_stress_source_blindness", "metric stress and source blindness", "delta_g S_kappa_top=0 and partial_A/source/lambda/frame kappa_eff=0", "UNSIGNED_METRIC_STRESS_SOURCE_BLINDNESS", "local tests still see source/range/frame hair unless this closes"),
        ("KTR2932_5_boundary", "boundary projection silence", "boundary term fixed/topological before source readout", "UNSIGNED_BOUNDARY_POLICY", "constant-kappa can otherwise move into source mass flux"),
        ("KTR2932_6_verdict", "topological kappa reentry", "derive Dln(kappa_MTS)=0 for current MTS", "ROUTE_BUILT_NOT_PROMOTED", "conditional theorem retained; no local-GR/Newton claim"),
    ]
    return [
        add_common(
            {
                "reentry_id": reentry_id,
                "step": step,
                "expression": expression,
                "current_status": current_status,
                "meaning": meaning,
                "mathematical_valid": current_status in {"ROUTE_EXISTS_CONDITIONAL", "MATHEMATICAL_STEP_VALID_CONDITIONAL", "CONDITIONAL_DOMAIN_CONSTANT", "ROUTE_BUILT_NOT_PROMOTED"},
                "parent_signed": False,
                "valid_for_claim": False,
                "source_paths": str(SRC_2695_DOC),
            }
        )
        for reentry_id, step, expression, current_status, meaning in specs
    ]


def bound_ledger_rows() -> list[dict[str, Any]]:
    specs = [
        ("CBL2932_0_dln_Geff_dt", "dln_Geff_dt", "kappa_time_drift", "D_t ln kappa_eff", "9.6e-15", "yr^-1", "Gdot_over_G;clock;orbital", "KRR2695_0_time_drift", "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_NUMERIC_DRIFT"),
        ("CBL2932_1_radial_Geff", "partial_r_ln_Geff", "kappa_radial_hair", "D_r ln kappa_eff", "zero radial hair or mapped local profile bound", "inverse_length_or_dimensionless_envelope", "gamma_minus_1;beta_minus_1;radial_source_hair", "KRR2695_1_radial_hair", "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_RADIAL_PROFILE"),
        ("CBL2932_2_alpha_kappa_lambda", "alpha_kappa(lambda)", "kappa_range_dependence", "finite-range/running coupling projection", "verified alpha(lambda) curve or theorem-zero", "range-dependent", "R10_fifth_force", "KRR2695_2_range_dependence", "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_ALPHA_CURVE"),
        ("CBL2932_3_eta_source_AB", "eta_source_AB;partial_A_ln_Geff", "kappa_species_source_charge", "material/source dependence of active gravitational source", "2.8e-15", "dimensionless", "R1_WEP_source_charge;measured_GM", "KRR2695_3_species_source_charge", "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_SOURCE_CHARGE_VALUE"),
        ("CBL2932_4_frame_domain", "delta_frame_source;partial_D_ln_Geff", "kappa_frame_domain_split", "frame/domain/boundary dependence of coupling", "one observed source frame or explicit residual below locks", "dimensionless", "WEP;clock;R11;domain_rows", "KRR2695_4_frame_domain_split", "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_FRAME_DOMAIN_VALUE"),
        ("CBL2932_5_bianchi_exchange", "delta_kappa_source", "kappa_bianchi_exchange", "P_loc[T_obs nabla kappa_eff] exchange residual", "same-frame arbitrary-source conservation theorem or explicit exchange coefficient", "operator/source_units", "R4;R7;R9;R10;R11", "KRR2695_5_bianchi_exchange", "MISSING_TOPOLOGICAL_PARENT_ADOPTION_OR_EXCHANGE_COEFFICIENT"),
        ("CBL2932_6_delta_kappa", "Dln(kappa_MTS)", "local_coupling_baseline", "Dln(kappa_MTS) or G_ref/kappa mismatch", "alpha3 projection target 4e-20 or arena-specific bound", "dimensionless", "Newton;alpha3;beta;clock;R10", "RES2578_7_delta_kappa;CB2928_0_kappa_alpha3", "MISSING_CONSTANT_KAPPA_PROOF_OR_VALUE"),
        ("CBL2932_7_delta_ellJ", "Dln(ell_J)", "source_current_scale", "Dln(ell_J) or source-current scale mismatch", "alpha3 projection target 4e-20 or source-current bound", "dimensionless", "Newton;WEP;PPN;orbital;alpha3", "RES2578_8_delta_ellJ;CB2928_1_ellJ_alpha3", "MISSING_CONSTANT_ELLJ_PROOF_OR_VALUE"),
        ("CBL2932_8_total", "Delta_coupling_source_abs", "total_coupling_source_envelope", "|K_alpha3_kappa Dln(kappa_MTS)|+|K_alpha3_ellJ Dln(ell_J)|+|epsilon_Gref_match|+|Delta_boundary_coupling|", "source-specific no-cancellation envelope", "mixed", "alpha3;beta;Newton;local_GR", "CB2928_3_coupling_total;RES2578_9_total", "SOURCE_READY_VALUES_MISSING"),
    ]
    return [
        add_common(
            {
                "ledger_id": ledger_id,
                "symbol": symbol,
                "component": component,
                "definition": definition,
                "target_bound_or_zero": target_bound_or_zero,
                "units": units,
                "arena_links": arena_links,
                "upstream_rows": upstream_rows,
                "current_status": current_status,
                "numeric_value_present": False,
                "theorem_zero": False,
                "selected_for_next_fill": ledger_id in {"CBL2932_0_dln_Geff_dt", "CBL2932_2_alpha_kappa_lambda", "CBL2932_6_delta_kappa", "CBL2932_7_delta_ellJ", "CBL2932_8_total"},
                "source_paths": ";".join(str(path) for path in [SRC_2695_KAPPA, SRC_KAPPA_MAP, SRC_2578_LEDGER, SRC_2928_COUPLING]),
            }
        )
        for ledger_id, symbol, component, definition, target_bound_or_zero, units, arena_links, upstream_rows, current_status in specs
    ]


def impact_rows() -> list[dict[str, Any]]:
    specs = [
        ("IM2932_0_Newton", "Newton/source normalization", "Dln(kappa_MTS), G_ref match and ell_J/source scale must be fixed or bounded", "BLOCKED_NONCLAIM", "coupling source envelope remains active"),
        ("IM2932_1_beta", "PPN beta", "coupling drift feeds Delta_A and delta_beta_source through source denominator", "BLOCKED_NONCLAIM", "2931 coefficient residual remains active"),
        ("IM2932_2_alpha3", "PPN alpha3", "alpha3_kappa=K_alpha3_kappa Dln(kappa_MTS), alpha3_ellJ=K_alpha3_ellJ Dln(ell_J)", "BLOCKED_NONCLAIM", "4e-20 comparator exists but product heads lack value/theorem-zero"),
        ("IM2932_3_R10_WEP_clock", "R10/WEP/clock/orbital arenas", "kappa range/source/time/frame dependence maps to fifth-force, WEP and clock/orbital residuals", "ACQUISITION_LEDGER_READY_NONCLAIM", "2695 rows provide target locks but not values"),
        ("IM2932_4_route", "best next route", "fill dln_Geff_dt / alpha_kappa(lambda) / Dln(kappa_MTS) / Dln(ell_J) first", "FORWARD_ROUTE_SELECTED", "turn coupling from symbolic blocker into measured or theorem-zero row"),
    ]
    return [
        add_common(
            {
                "impact_id": impact_id,
                "target": target,
                "requires": requires,
                "current_status": current_status,
                "reason": reason,
                "source_paths": ";".join(str(path) for path in [SRC_2931_DOC, SRC_2928_COUPLING, SRC_2918_PRODUCTS, SRC_2695_KAPPA]),
            }
        )
        for impact_id, target, requires, current_status, reason in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    specs = [
        ("CG2932_0_kappa_conditional", "topological kappa route is mathematically valid conditionally", "PASS_CONTROL_STRUCTURE", "2695 already derives d kappa_eff=0 if parent clauses close", False),
        ("CG2932_1_kappa_claim", "Dln(kappa_MTS)=0 is parent-derived for current MTS", "BLOCKED_NONCLAIM", "parent adoption/source blindness/boundary policy unsigned", False),
        ("CG2932_2_ellJ_claim", "Dln(ell_J)=0 is parent-derived for current MTS", "BLOCKED_NONCLAIM", "source-current scale owner open", False),
        ("CG2932_3_first_bound", "first finite coupling/source-current value is source-backed", "BLOCKED_NONCLAIM", "2932 stages ledger only; no numeric values imported", False),
        ("CG2932_4_alpha3", "alpha3 coupling products pass 4e-20", "BLOCKED_NONCLAIM", "K/product heads and Dln values missing", False),
        ("CG2932_5_Newton_beta_local_GR", "Newton/beta/local-GR pass from coupling branch", "BLOCKED_NONCLAIM", "constant coupling package not derived and RV2925 remains open", False),
        ("CG2932_6_next", "2933 source-bound target selected without looping", "PASS_GUARDRAIL", "move to a concrete kappa drift/range/source-current bound row", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "claim": claim,
                "current_status": current_status,
                "reason": reason,
                "claim_passed": claim_passed,
            }
        )
        for gate_id, claim, current_status, reason, claim_passed in specs
    ]


def decision_rows() -> list[dict[str, Any]]:
    specs = [
        ("DEC2932_0_kappa", "retain kappa topological mechanism as conditional", "the zero-form/three-form route is mathematically valid but not parent-adopted", "carry as candidate, no claim", False),
        ("DEC2932_1_ellJ", "do not claim ell_J constancy", "no topological/source-current parent owner theorem exists in the current chain", "keep Dln(ell_J) as active residual", False),
        ("DEC2932_2_values", "stage first finite coupling-bound ledger", "no theorem-zero currently closes kappa/ellJ, so values/bounds are the honest next path", "target kappa drift/range/source-current rows", False),
        ("DEC2932_3_next", "select kappa drift/range/source-current bound acquisition", "dln_Geff_dt and alpha_kappa(lambda) have concrete external-style target locks; ellJ remains source-current owner hunt", "2933 should acquire or prove one row", False),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": next_action,
                "valid_for_claim": valid_for_claim,
            }
        )
        for decision_id, decision, because, next_action, valid_for_claim in specs
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2932_0_2933",
                "selection": "selected_primary",
                "target_doc": "2933-Y5-R2FR-kappa-drift-range-source-bound-first-value-or-ellJ-owner-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_kappa_drift_range_source_bound_first_value_or_ellJ_owner_under_AX1090_2933.py",
                "objective": "try to close one coupling row: prove a parent-zero for dln_Geff_dt/alpha_kappa(lambda)/Dln(kappa_MTS)/Dln(ell_J), or acquire a finite source-backed nonclaim value/bound with units and arena map",
                "acceptance_gate": "one CBL2932 row becomes theorem-zero or finite/source-backed with source path, units, target comparator and valid_for_claim=false unless all parent gates close",
                "fallback": "if kappa source-bound acquisition is unavailable, attack ell_J source-current owner theorem directly",
                "valid_for_claim": False,
            }
        )
    ]


def branch_copy_rows() -> list[dict[str, Any]]:
    copies = [
        ("constant_audit_copy", OUTPUTS["constant_audit"], BRANCH_OUTPUTS["constant_audit_copy"]),
        ("bound_ledger_copy", OUTPUTS["bound_ledger"], BRANCH_OUTPUTS["bound_ledger_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows = []
    for copy_id, source_path, destination_path in copies:
        shutil.copyfile(source_path, destination_path)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source_path),
                    "destination_path": str(destination_path),
                    "source_exists": source_path.exists(),
                    "destination_exists": destination_path.exists(),
                    "destination_parses": csv_parses(destination_path),
                }
            )
        )
    return rows


def validation_rows() -> list[dict[str, Any]]:
    source_rows = read_csv_rows(OUTPUTS["sources"])
    constant_audit = read_csv_rows(OUTPUTS["constant_audit"])
    kappa_reentry = read_csv_rows(OUTPUTS["kappa_reentry"])
    bound_ledger = read_csv_rows(OUTPUTS["bound_ledger"])
    claims = read_csv_rows(OUTPUTS["claims"])
    next_rows = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])

    required_audit = {"KLC2932_0_kappa_route", "KLC2932_3_ellJ_owner", "KLC2932_6_verdict"}
    required_reentry = {"KTR2932_0_action", "KTR2932_1_A3_variation", "KTR2932_6_verdict"}
    required_symbols = {"dln_Geff_dt", "alpha_kappa(lambda)", "Dln(kappa_MTS)", "Dln(ell_J)", "Delta_coupling_source_abs"}
    promoted_rows = [
        row
        for row in [*constant_audit, *kappa_reentry, *bound_ledger]
        if as_bool(row.get("adopted_for_claim")) or as_bool(row.get("parent_signed")) or as_bool(row.get("numeric_value_present")) or as_bool(row.get("theorem_zero")) or as_bool(row.get("valid_for_claim"))
    ]
    all_paths = [Path(row["source_path"]) for row in source_rows if row.get("source_path")]
    no_formalization_2932 = not list(FORMALIZATION.rglob("*2932*")) if FORMALIZATION.exists() else True

    checks = [
        ("VAL2932_0_sources_exist", all(as_bool(row.get("path_exists")) for row in source_rows), "every cited source path exists"),
        ("VAL2932_1_source_anchors_found", all(as_bool(row.get("anchors_found")) for row in source_rows), "every cited source anchor is present"),
        ("VAL2932_2_outputs_parse", all(csv_parses(path) for path in OUTPUTS.values()), "all 2932 CSV outputs parse"),
        ("VAL2932_3_doc_exists", DOC.exists(), "2932 markdown checkpoint exists"),
        ("VAL2932_4_constant_audit_complete", required_audit <= {row.get("audit_id", "") for row in constant_audit}, "kappa/ellJ constant audit has required rows"),
        ("VAL2932_5_kappa_reentry_complete", required_reentry <= {row.get("reentry_id", "") for row in kappa_reentry}, "topological kappa reentry has required rows"),
        ("VAL2932_6_bound_ledger_complete", required_symbols <= {row.get("symbol", "") for row in bound_ledger}, "coupling bound ledger has required symbols"),
        ("VAL2932_7_no_rows_promoted", not promoted_rows, "no audit/reentry/ledger row is promoted to claim"),
        ("VAL2932_8_claims_closed", all(not as_bool(row.get("claim_passed")) for row in claims), "all claim gates remain closed"),
        ("VAL2932_9_next_target_selected", any(row.get("next_id") == "NEXT2932_0_2933" for row in next_rows), "2933 next target selected"),
        ("VAL2932_10_branch_copies_parse", all(as_bool(row.get("destination_parses")) for row in branches), "branch copies parse cleanly"),
        ("VAL2932_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in OUTPUTS.values()) and all(is_under(path, ROOT) for path in BRANCH_OUTPUTS.values()), "all outputs remain under post-checkpoint-work"),
        ("VAL2932_12_sources_not_formalization", all(not is_under(path, FORMALIZATION) for path in all_paths) if FORMALIZATION.exists() else True, "no formalization-workbench source/output dependency"),
        ("VAL2932_13_no_formalization_2932_outputs", no_formalization_2932, "no formalization-workbench 2932 outputs"),
    ]
    overall = all(passed for _, passed, _ in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "blocking_if_false": True,
            }
        )
        for validation_id, passed, check in checks
    ]
    rows.append(
        add_common(
            {
                "validation_id": "VAL2932_OVERALL",
                "passed": overall,
                "check": "2932 validation overall",
                "blocking_if_false": True,
            }
        )
    )
    return rows


def write_doc() -> None:
    source_rows = read_csv_rows(OUTPUTS["sources"])
    constant_audit = read_csv_rows(OUTPUTS["constant_audit"])
    kappa_reentry = read_csv_rows(OUTPUTS["kappa_reentry"])
    bound_ledger = read_csv_rows(OUTPUTS["bound_ledger"])
    impact = read_csv_rows(OUTPUTS["impact"])
    claims = read_csv_rows(OUTPUTS["claims"])
    decisions = read_csv_rows(OUTPUTS["decision"])
    next_rows = read_csv_rows(OUTPUTS["next"])
    branches = read_csv_rows(OUTPUTS["branches"])
    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row for row in validation if row.get("validation_id") == "VAL2932_OVERALL"), {})

    sections = [
        "# 2932 - Y5/R2FR Kappa/EllJ Constant Proof Or First Coupling Source Bound Under AX1090",
        "",
        "Status: `Y5_R2FR_2932_kappa_conditional_topological_route_retained_ellJ_owner_open_first_bound_2933_next`",
        "",
        "Claim ceiling: `kappa_topological_route_conditional_yes_kappa_claim_no_ellJ_claim_no_first_bound_no_Newton_no_beta_no_alpha3_no_local_GR_no_R10_no_GitHub_claim`",
        "",
        "## Summary",
        "",
        "2932 attacks the coupling wound directly. The `kappa_MTS` side has a real conditional mechanism:",
        "",
        "`S_kappa_top = int_M kappa_eff dA_3 -> d kappa_eff = 0`,",
        "",
        "but current MTS still has not parent-signed the topological sector, companion equation, metric/source blindness, and boundary policy. So `Dln(kappa_MTS)=0` is not claimed.",
        "",
        "`ell_J` is weaker: the corpus names it as a source-current scale that must be fixed before readout, but no comparable parent-owner theorem is present. So `Dln(ell_J)=0` is also not claimed.",
        "",
        "The useful output is a first-bound acquisition ledger. If we cannot prove constant coupling yet, we must measure or bound the live rows: `dln_Geff_dt`, `alpha_kappa(lambda)`, source/species charge, frame/domain split, Bianchi exchange, `Dln(kappa_MTS)`, and `Dln(ell_J)`.",
        "",
        "## Source Register",
        "",
        md_table(source_rows, ["source_id", "source_path", "path_exists", "anchors_found", "role", "missing_anchors"]),
        "",
        "## Kappa/EllJ Constant Proof Audit",
        "",
        md_table(constant_audit, ["audit_id", "clause", "required_identity", "current_status", "reason", "condition_passed", "adopted_for_claim"]),
        "",
        "## Topological Kappa Reentry Audit",
        "",
        md_table(kappa_reentry, ["reentry_id", "step", "expression", "current_status", "meaning", "mathematical_valid", "parent_signed", "valid_for_claim"]),
        "",
        "## Coupling First-Bound Acquisition Ledger",
        "",
        md_table(bound_ledger, ["ledger_id", "symbol", "component", "definition", "target_bound_or_zero", "units", "arena_links", "current_status", "numeric_value_present", "theorem_zero", "selected_for_next_fill"]),
        "",
        "## Alpha3/Beta/Newton Impact",
        "",
        md_table(impact, ["impact_id", "target", "requires", "current_status", "reason"]),
        "",
        "## Claim Gates",
        "",
        md_table(claims, ["gate_id", "claim", "current_status", "reason", "claim_passed"]),
        "",
        "## Decision Ledger",
        "",
        md_table(decisions, ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        "",
        md_table(next_rows, ["next_id", "selection", "target_doc", "target_script", "objective", "acceptance_gate", "fallback", "valid_for_claim"]),
        "",
        "## Branch Copies",
        "",
        md_table(branches, ["copy_id", "source_path", "destination_path", "source_exists", "destination_exists", "destination_parses"]),
        "",
        "## Validation",
        "",
        md_table(validation, ["validation_id", "passed", "check", "blocking_if_false"]),
        "",
        f"Validation overall: `{overall.get('passed', False)}`.",
        "",
        "## Bottom Line",
        "",
        "This is progress, but not a coupling victory. `kappa_MTS` has a serious conditional topological path; `ell_J` still lacks a parent owner. The theory therefore cannot claim Newton/GR recovery through constant coupling yet.",
        "",
        "The next best move is empirical/derivational pressure on one row: prove or bound `dln_Geff_dt`, `alpha_kappa(lambda)`, `Dln(kappa_MTS)`, or `Dln(ell_J)`. That would start turning the local-GR obstruction from symbolic debt into a testable finite vector.",
        "",
        "## Non-Claims",
        "",
        "- no parent-adopted `kappa_MTS` constant theorem is claimed;",
        "- no `ell_J` constant/source-owner theorem is claimed;",
        "- no first finite coupling value is source-backed yet;",
        "- no alpha3, beta, Newton, R10, WEP, clock, orbital, or local-GR pass is claimed;",
        "- no public/GitHub claim is made.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def main() -> None:
    write_csv(OUTPUTS["sources"], source_register_rows())
    write_csv(OUTPUTS["constant_audit"], constant_audit_rows())
    write_csv(OUTPUTS["kappa_reentry"], kappa_reentry_rows())
    write_csv(OUTPUTS["bound_ledger"], bound_ledger_rows())
    write_csv(OUTPUTS["impact"], impact_rows())
    write_csv(OUTPUTS["claims"], claim_gate_rows())
    write_csv(OUTPUTS["decision"], decision_rows())
    write_csv(OUTPUTS["next"], next_target_rows())
    write_csv(OUTPUTS["branches"], branch_copy_rows())
    DOC.write_text("# 2932 preflight\n", encoding="utf-8")
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()

    validation = read_csv_rows(OUTPUTS["validation"])
    overall = next((row for row in validation if row.get("validation_id") == "VAL2932_OVERALL"), {})
    print(f"wrote {DOC}")
    print(f"validation overall: {overall.get('passed')}")


if __name__ == "__main__":
    main()
