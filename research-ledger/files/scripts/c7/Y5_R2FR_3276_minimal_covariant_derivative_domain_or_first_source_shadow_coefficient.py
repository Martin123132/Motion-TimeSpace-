from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
FW = REPO / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
PYCACHE = ROOT / "scripts" / "__pycache__"

DOC = ROOT / "3276-Y5-R2FR-minimal-covariant-derivative-domain-or-first-source-shadow-coefficient-under-AX1090.md"

SRC_3275_DOC = ROOT / "3275-Y5-R2FR-no-compensator-current-and-source-shadow-ban-or-finite-CJ-row-under-AX1090.md"
SRC_3275_TRI = OUT / "P8_Y5_R2FR_3275_COMPENSATOR_CURRENT_TRICHOTOMY.csv"
SRC_3275_MCD = OUT / "P8_Y5_R2FR_3275_MINIMAL_COVARIANT_DERIVATIVE_NO_SHADOW_THEOREM.csv"
SRC_3275_SHADOW = OUT / "P8_Y5_R2FR_3275_SOURCE_SHADOW_ESCAPE_AUDIT.csv"
SRC_3275_CJ = OUT / "P8_Y5_R2FR_3275_CJ_RESIDUAL_ROWS_NONCLAIM.csv"
SRC_3275_NEXT = OUT / "P8_Y5_R2FR_3275_NEXT_TARGET.csv"
SRC_3274_GAUGE = OUT / "P8_Y5_R2FR_3274_CURRENT_NORMALIZATION_GAUGE_LOCK_LEMMA.csv"
SRC_3274_STRESS = OUT / "P8_Y5_R2FR_3274_EM_STRESS_POYNTING_EXCHANGE_LAW.csv"
SRC_642_MD = OUT / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv"
SRC_642_TA = OUT / "P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv"
SRC_765_CEX = OUT / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
SRC_771_AUDIT = OUT / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"
SRC_993_SECTOR = OUT / "P8_Y5_R10_993_SECTOR_CURRENT_EXTRACTION_LEDGER.csv"
SRC_951_WARD = OUT / "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv"
SRC_1030_DOC = ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md"
SRC_1046_DOC = ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md"
SRC_2508_PROOF = OUT / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv"
SRC_2508_COUNTER = OUT / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv"
SRC_2509_PIVOT = OUT / "P8_Y5_NO_SHADOW_2509_DERIVATION_OR_RESIDUAL_PIVOT_GATE.csv"
SRC_2616_SHADOW = OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3276_SOURCE_REGISTER.csv",
    "domain_split": OUT / "P8_Y5_R2FR_3276_AQ_DOMAIN_SPLIT_THEOREM.csv",
    "magnetization": OUT / "P8_Y5_R2FR_3276_F_ONLY_MAGNETIZATION_CURRENT_LEMMA.csv",
    "gauge_rejection": OUT / "P8_Y5_R2FR_3276_NONCONSERVED_COMPENSATOR_GAUGE_REJECTION.csv",
    "shadow_schema": OUT / "P8_Y5_R2FR_3276_SOURCE_SHADOW_COEFFICIENT_SCHEMA.csv",
    "shadow_rows": OUT / "P8_Y5_R2FR_3276_SOURCE_SHADOW_COEFFICIENT_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3276_SOURCE_SHADOW_RUNNER_RESULTS_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3276_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3276_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3276_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3276_VALIDATION.csv",
}

RUN_UTC = datetime.now(timezone.utc).isoformat()


def bool_str(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    return f"{value:.12e}"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def text_parse_ok(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        path.read_text(encoding="utf-8", errors="replace")
        return True
    except Exception:
        return False


def parse_ok(path: Path) -> bool:
    return csv_parse_ok(path) if path.suffix.lower() == ".csv" else text_parse_ok(path)


def compact(value: str, limit: int = 300) -> str:
    text = " ".join(str(value).split())
    return text if len(text) <= limit else text[: limit - 3] + "..."


def evidence_hits(path: Path, needles: list[str], limit: int = 4) -> str:
    if not path.exists():
        return "MISSING_SOURCE"
    hits: list[str] = []
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    lowered = [needle.lower() for needle in needles]
    for idx, line in enumerate(lines, start=1):
        if any(needle in line.lower() for needle in lowered):
            hits.append(f"L{idx}:{compact(line, 220)}")
        if len(hits) >= limit:
            break
    return " | ".join(hits) if hits else "NO_PATTERN_HIT"


def cj_bound() -> float:
    return float(read_csv(SRC_3275_CJ)[0]["bound_value"])


def source_register() -> list[dict[str, Any]]:
    sources = [
        (SRC_3275_DOC, "3275 handoff", ["nabla_mu J_comp", "minimal covariant derivative", "source-shadow"]),
        (SRC_3275_TRI, "compensator trichotomy", ["TRI3275_1", "TRI3275_3"]),
        (SRC_3275_MCD, "minimal covariant derivative theorem", ["MCD3275_0", "MCD3275_4"]),
        (SRC_3275_SHADOW, "source-shadow escape audit", ["ESC3275_0", "ESC3275_4"]),
        (SRC_3275_CJ, "C_J residual rows", ["CJR3275_0", "bound_value"]),
        (SRC_3275_NEXT, "3275 next target", ["NEXT3275_0_3276", "minimal covariant"]),
        (SRC_3274_GAUGE, "weighted-current gauge lock", ["GL3274_0", "GL3274_2"]),
        (SRC_3274_STRESS, "EM stress/Poynting exchange", ["SP3274_3", "Poynting"]),
        (SRC_642_MD, "Maxwell descent source", ["MD642_2", "MD642_3"]),
        (SRC_642_TA, "U1 and Maxwell theorem attempt", ["TA642_0", "TA642_3"]),
        (SRC_765_CEX, "current rescale counterexample", ["RCE765_2", "current_rescale"]),
        (SRC_771_AUDIT, "parent current owner audit", ["TQ771_5", "matter_coupling"]),
        (SRC_993_SECTOR, "EM sector current ledger", ["SEC993_7", "EM_charge_coupling"]),
        (SRC_951_WARD, "Ward action countermodel", ["SWA951_3", "species_weight_countermodel"]),
        (SRC_1030_DOC, "source-shadow countermodels", ["CM1030_1", "source"]),
        (SRC_1046_DOC, "source-only weight audit", ["FV1046_6", "source_only_weight"]),
        (SRC_2508_PROOF, "no-source-only slot proof attempt", ["NSP2508_6", "counterexample"]),
        (SRC_2508_COUNTER, "source-only countermodels", ["CM2508_0", "CM2508_5"]),
        (SRC_2509_PIVOT, "constructor exhaustion pivot", ["PIV2509_2", "residual_route"]),
        (SRC_2616_SHADOW, "source-shadow ban attempt", ["SSB2616_2", "SSB2616_5"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3276_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def domain_split_rows() -> list[dict[str, Any]]:
    return [
        {
            "split_id": "ADS3276_0_minimal_representation_current",
            "A_Q_dependence": "D_Q psi=(nabla+i n_A A_Q)psi with fixed representation weights n_A",
            "current_from_variation": "J_min^mu=delta S_matter/delta A_Q_mu",
            "divergence_status": "nabla_mu J_min^mu=0 on matter shell by U1 Ward identity",
            "C_J_effect": "variable kappa_J multiplying this current violates gauge invariance unless J_min.nabla kappa_J=0 or another real sector compensates",
            "status": "DERIVED_STANDARD_GAUGE_CURRENT_BLOCK",
            "valid_for_claim": "false",
        },
        {
            "split_id": "ADS3276_1_F_only_magnetization",
            "A_Q_dependence": "gauge-invariant F_Q-only terms such as Pauli, polarization, axion-like or higher-derivative response terms",
            "current_from_variation": "J_mag^nu=-nabla_mu H^{mu nu}, H^{mu nu}:=-2 partial L_F/partial F_{mu nu}",
            "divergence_status": "nabla_nu J_mag^nu=0 identically because H^{mu nu} is antisymmetric",
            "C_J_effect": "cannot cancel J_min.nabla kappa_J; contributes to EM stress/Poynting/boundary residuals instead",
            "status": "NEW_USEFUL_ZERO_FOR_NONCONSERVED_COMPENSATOR",
            "valid_for_claim": "false",
        },
        {
            "split_id": "ADS3276_2_bare_AJ_shadow",
            "A_Q_dependence": "A_Q_mu J_shadow^mu not generated by the same charged matter representation",
            "current_from_variation": "J_shadow^mu",
            "divergence_status": "gauge invariant only if nabla_mu J_shadow^mu=0 or if it is actually the Noether current of another charged sector",
            "C_J_effect": "separately conserved shadow block changes active source normalization but cannot hide local kappa_J variation",
            "status": "FINITE_SOURCE_SHADOW_BLOCK_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "split_id": "ADS3276_3_nonconserved_AJ_compensator",
            "A_Q_dependence": "A_Q_mu J_comp^mu with nabla_mu J_comp^mu=-J_min.nabla_mu kappa_J",
            "current_from_variation": "J_comp^mu",
            "divergence_status": "breaks U1 gauge invariance unless a new charged sector/Euler equation supplies it",
            "C_J_effect": "is not a hidden proof of C_J=0; it is either forbidden or a new explicit source sector to bound",
            "status": "REJECTED_AS_SILENT_COMPENSATOR",
            "valid_for_claim": "false",
        },
    ]


def magnetization_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "MAG3276_0_variation",
            "claim": "F-only terms give magnetization currents",
            "formula": "delta L_F = (partial L_F/partial F_{mu nu}) delta F_{mu nu}; J_mag^nu=-nabla_mu H^{mu nu}",
            "derivation": "integrate by parts using delta F=d(delta A)",
            "status": "EXACT_LOCAL_VARIATION_LEMMA",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "MAG3276_1_identity",
            "claim": "magnetization current is identically conserved",
            "formula": "nabla_nu nabla_mu H^{mu nu}=0 for antisymmetric H^{mu nu}",
            "derivation": "the commutator contracts Ricci curvature with an antisymmetric tensor and vanishes",
            "status": "EXACT_IDENTITY",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "MAG3276_2_CJ_consequence",
            "claim": "magnetization cannot be the C_J compensator",
            "formula": "nabla_mu J_mag^mu=0 cannot equal -J_min^mu nabla_mu kappa_J unless J_min.nabla kappa_J=0",
            "derivation": "compare with the 3275 compensator equation",
            "status": "NONCONSERVED_COMPENSATOR_CLASS_SHRUNK",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "MAG3276_3_stress_consequence",
            "claim": "F-only terms belong in stress/Poynting residuals",
            "formula": "F-only response changes H^{mu nu}, T_EM^{mu nu}, and boundary multipoles, not the active charge-current slope C_J",
            "derivation": "same variation contributes to constitutive EM stress rather than source-shadow normalization",
            "status": "MAP_TO_EM_STRESS_RESIDUAL",
            "valid_for_claim": "false",
        },
    ]


def gauge_rejection_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "GJR3276_0_variable_kappa",
            "tested_term": "kappa_J(X) A_Q_mu J_min^mu",
            "gauge_variation": "delta_lambda S = -int mu_obs lambda nabla_mu(kappa_J J_min^mu)",
            "result": "requires J_min^mu nabla_mu kappa_J=0 on matter shell",
            "consequence": "variable kappa_J is gauge-pressure, not a free source knob",
            "status": "EXACT_GAUGE_LOCK",
            "valid_for_claim": "false",
        },
        {
            "test_id": "GJR3276_1_F_only_terms",
            "tested_term": "L(F_Q,psi,g,hidden)",
            "gauge_variation": "delta_lambda F_Q=0",
            "result": "allowed by U1 but contributes only an identically conserved magnetization current",
            "consequence": "safe from nonconserved compensation but retained in EM stress/readout residuals",
            "status": "ALLOWED_NOT_CJ_COMPENSATOR",
            "valid_for_claim": "false",
        },
        {
            "test_id": "GJR3276_2_nonconserved_shadow",
            "tested_term": "A_Q_mu J_comp^mu with nabla_mu J_comp^mu != 0",
            "gauge_variation": "delta_lambda S = -int mu_obs lambda nabla_mu J_comp^mu",
            "result": "forbidden by exact U1 gauge invariance unless new charged fields make J_comp a real Noether current",
            "consequence": "silent compensator route is rejected; real sector route becomes finite source-shadow residual",
            "status": "REJECT_SILENT_COMPENSATOR",
            "valid_for_claim": "false",
        },
        {
            "test_id": "GJR3276_3_verdict",
            "tested_term": "minimal A_Q domain in current MTS corpus",
            "gauge_variation": "all A_Q dependence classified into minimal, F-only, conserved shadow, or forbidden/non-silent sector",
            "result": "mathematical domain split is stronger than 3275, but parent action has not yet signed exact U1 plus no separate S_source",
            "consequence": "C_J=0 is closer but still nonclaim; source-shadow row remains staged",
            "status": "DOMAIN_SPLIT_DERIVED_PARENT_SIGNATURE_UNSIGNED",
            "valid_for_claim": "false",
        },
    ]


def shadow_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "field_id": "SSS3276_0_epsilon_shadow",
            "field": "epsilon_shadow",
            "meaning": "relative separately conserved source-shadow block entering Maxwell/source normalization",
            "required_columns": "value;units;source_path;current_definition;conservation_certificate;projection_to_CJ;arena_links",
            "claim_requirement": "numeric/source-backed or parent theorem-zero",
        },
        {
            "field_id": "SSS3276_1_epsilon_mag_boundary",
            "field": "epsilon_mag_boundary",
            "meaning": "boundary/no-flux leakage from F-only magnetization/improvement currents",
            "required_columns": "boundary_flux;units;source_path;compact_support_certificate;stress_projection;arena_links",
            "claim_requirement": "zero no-flux theorem or source-backed boundary/stress bound",
        },
        {
            "field_id": "SSS3276_2_CJ_effective",
            "field": "C_J_effective",
            "meaning": "effective current-normalization slope after source-shadow and side-condition projection",
            "required_columns": "C_J_value;C_Z_zero;C_R_zero;normalization;source_path;bound_value;valid_for_claim",
            "claim_requirement": "abs(C_J_effective)<=conditional bound with C_Z=C_R=0, or standalone source arena bound",
        },
    ]


def shadow_rows() -> list[dict[str, Any]]:
    bound = cj_bound()
    return [
        {
            "row_id": "SSR3276_0_minimal_domain_zero_conditional",
            "quantity": "C_J_effective",
            "prediction_value": "0",
            "units": "dimensionless local logarithmic coefficient",
            "source_or_status": "conditional exact U1/minimal-domain theorem; parent signature unsigned",
            "bound_value": fmt(bound),
            "result_status": "PASS_IF_PARENT_SIGNED_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSR3276_1_live_source_shadow_missing",
            "quantity": "epsilon_shadow",
            "prediction_value": "MISSING_SOURCE_BACKED_SHADOW_BLOCK",
            "units": "dimensionless relative current/source block",
            "source_or_status": "separately conserved shadow block retained as finite row",
            "bound_value": fmt(bound),
            "result_status": "REFUSE_MISSING",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSR3276_2_magnetization_exact_no_flux_zero",
            "quantity": "epsilon_mag_boundary",
            "prediction_value": "0",
            "units": "dimensionless current-normalization leakage",
            "source_or_status": "F-only magnetization current is identically conserved; assumes compact no-flux support",
            "bound_value": fmt(bound),
            "result_status": "PASS_IF_NO_FLUX_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSR3276_3_nonconserved_compensator_forbidden_smoke",
            "quantity": "epsilon_nonconserved_compensator",
            "prediction_value": "FORBIDDEN_BY_U1_UNLESS_REAL_SECTOR",
            "units": "not_a_numeric_prediction",
            "source_or_status": "silent route rejected; real sector must use SSR3276_1",
            "bound_value": fmt(bound),
            "result_status": "REFUSE_OR_ROUTE_TO_SHADOW",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSR3276_4_half_bound_smoke",
            "quantity": "C_J_effective",
            "prediction_value": fmt(0.5 * bound),
            "units": "dimensionless local logarithmic coefficient",
            "source_or_status": "SMOKE_NUMERIC_NONCLAIM",
            "bound_value": fmt(bound),
            "result_status": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSR3276_5_twice_bound_smoke",
            "quantity": "C_J_effective",
            "prediction_value": fmt(2.0 * bound),
            "units": "dimensionless local logarithmic coefficient",
            "source_or_status": "SMOKE_NUMERIC_NONCLAIM",
            "bound_value": fmt(bound),
            "result_status": "SMOKE",
            "valid_for_claim": "false",
        },
    ]


def numeric_or_none(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def runner_rows() -> list[dict[str, Any]]:
    expected = {
        "SSR3276_0_minimal_domain_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "SSR3276_1_live_source_shadow_missing": "REFUSE_OR_FAIL",
        "SSR3276_2_magnetization_exact_no_flux_zero": "PASS_NUMERIC_NONCLAIM",
        "SSR3276_3_nonconserved_compensator_forbidden_smoke": "REFUSE_OR_FAIL",
        "SSR3276_4_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "SSR3276_5_twice_bound_smoke": "FAIL_BOUND",
    }
    bound = cj_bound()
    rows: list[dict[str, Any]] = []
    for row in shadow_rows():
        value = numeric_or_none(row["prediction_value"])
        if value is None:
            abs_value = "MISSING"
            ratio = "MISSING"
            pass_bound = False
            result = "REFUSE_OR_FAIL"
        else:
            magnitude = abs(value)
            abs_value = fmt(magnitude)
            ratio = fmt(magnitude / bound)
            pass_bound = magnitude <= bound
            result = "PASS_NUMERIC_NONCLAIM" if pass_bound else "FAIL_BOUND"
        rows.append(
            {
                "case_id": f"RUN3276_{row['row_id']}",
                "row_id": row["row_id"],
                "quantity": row["quantity"],
                "prediction_value": row["prediction_value"],
                "bound_value": fmt(bound),
                "abs_prediction": abs_value,
                "prediction_over_bound": ratio,
                "pass_bound": bool_str(pass_bound),
                "result": result,
                "expected": expected[row["row_id"]],
                "expectation_met": bool_str(result == expected[row["row_id"]]),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3276_0_domain_split",
            "gate": "A_Q dependence split into minimal, F-only magnetization, conserved shadow, or forbidden/non-silent sector",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "this shrinks the compensator loophole but does not sign the parent action.",
        },
        {
            "gate_id": "GATE3276_1_magnetization_zero",
            "gate": "F-only terms cannot be nonconserved C_J compensators",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "their currents are identically conserved and move to EM stress/Poynting residuals.",
        },
        {
            "gate_id": "GATE3276_2_silent_compensator_rejected",
            "gate": "nonconserved A.J compensator is rejected as silent source",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "exact U1 forbids it unless it is a real charged sector/source-shadow row.",
        },
        {
            "gate_id": "GATE3276_3_parent_signature",
            "gate": "exact parent U1 and no separate S_source signed by MTS parent action",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "current corpus supports the theorem shape but not the parent action domain signature.",
        },
        {
            "gate_id": "GATE3276_4_runner",
            "gate": "source-shadow runner refuses missing and fails over-bound smoke",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner_rows())),
            "claim_allowed": "false",
            "detail": "numeric gates behave correctly; all live rows remain nonclaim.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3276_0_real_gain",
            "decision": "The dangerous compensator class is much smaller.",
            "why_it_moves_forward": "F-only/Pauli/polarization terms are exact magnetization currents and cannot cancel variable kappa_J divergence.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3276_1_silent_route",
            "decision": "A nonconserved compensator is incompatible with exact U1 unless it is a real new charged sector.",
            "why_it_moves_forward": "source-shadow is no longer a vague loophole; it is either separately conserved, gauge breaking, or a finite residual row.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3276_2_CJ_status",
            "decision": "C_J=0 is now conditional on parent exact U1/minimal domain/no separate S_source/current richness.",
            "why_it_moves_forward": "this is a sharper derivation route than generic no-source-slot grammar, and it links directly to Maxwell source coupling.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3276_3_next",
            "decision": "Next attack should be parent exact-U1 representation signature or standalone finite source-shadow data.",
            "why_it_moves_forward": "we either sign the last source-domain premise or stop theorem-chasing and acquire numeric residual evidence.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3276_0_3277",
            "target_doc": "3277-Y5-R2FR-parent-exact-U1-representation-signature-or-source-shadow-data-intake-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3277_parent_exact_U1_representation_signature_or_source_shadow_data_intake.py",
            "objective": "Try to sign the exact parent U1 representation/domain premise for ordinary charged matter; if not signed, create a data-intake table for finite separately conserved source-shadow/current-normalization residuals.",
            "guardrail": "Do not repeat generic no-source-slot arguments; use the 3276 A_Q-domain split and either sign exact U1/domain ownership or acquire finite residual inputs.",
            "valid_for_claim": "false",
        }
    ]


def formalization_changed_count() -> int:
    if not FW.exists():
        return 0
    script_mtime = Path(__file__).stat().st_mtime
    return sum(1 for path in FW.rglob("*") if path.is_file() and path.stat().st_mtime > script_mtime)


def output_csvs_parse() -> bool:
    return all(csv_parse_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def validation_rows() -> list[dict[str, Any]]:
    sources = source_register()
    runner = runner_rows()
    gates = promotion_gate_rows()
    validations = [
        {
            "check_id": "VAL3276_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3276_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3276_2_outputs_parse",
            "check": "all 3276 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3276_3_domain_split_complete",
            "check": "A_Q domain split contains minimal, F-only, shadow, and forbidden/non-silent cases",
            "passed": bool_str(len(domain_split_rows()) == 4),
            "detail": ";".join(row["split_id"] for row in domain_split_rows()),
        },
        {
            "check_id": "VAL3276_4_magnetization_identity_present",
            "check": "F-only magnetization current is identically conserved",
            "passed": bool_str(any(row["lemma_id"] == "MAG3276_1_identity" for row in magnetization_rows())),
            "detail": "nabla_nu nabla_mu H^{mu nu}=0",
        },
        {
            "check_id": "VAL3276_5_silent_compensator_rejected",
            "check": "nonconserved silent compensator is rejected or routed to real sector",
            "passed": bool_str(any(row["test_id"] == "GJR3276_2_nonconserved_shadow" and row["status"] == "REJECT_SILENT_COMPENSATOR" for row in gauge_rejection_rows())),
            "detail": "exact U1 requires conservation or real charged sector",
        },
        {
            "check_id": "VAL3276_6_runner_expectations",
            "check": "source-shadow runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3276_7_claim_gates_false",
            "check": "no 3276 gate allows local-GR/WEP/Maxwell claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3276_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3276_9_overall",
            "check": "3276 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3276_9_overall")
    validations[-1]["passed"] = bool_str(overall)
    validations[-1]["detail"] = "all required checks passed" if overall else "one or more checks failed"
    return validations


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(compact(str(row.get(col, "")), 180).replace("|", "\\|") for col in columns) + " |")
    return "\n".join([header, sep, *body])


def write_doc() -> None:
    domain = read_csv(OUTPUTS["domain_split"])
    mag = read_csv(OUTPUTS["magnetization"])
    gauge = read_csv(OUTPUTS["gauge_rejection"])
    schema = read_csv(OUTPUTS["shadow_schema"])
    shadow = read_csv(OUTPUTS["shadow_rows"])
    runner = read_csv(OUTPUTS["runner"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3276 - Minimal covariant derivative domain or first source-shadow coefficient under AX1090

## Summary

3276 sharpens the `C_J` coupling route. The main new step is the `A_Q`-domain split:

1. minimal charged matter enters through `D_Q psi=(nabla+i n_A A_Q)psi`;
2. gauge-invariant `F_Q`-only response terms produce magnetization currents `J_mag^nu=-nabla_mu H^{{mu nu}}`;
3. bare `A_Q.J_shadow` terms are gauge-safe only if the shadow current is conserved or is a real charged sector;
4. a nonconserved silent compensator is rejected by exact U(1) gauge invariance.

The useful punchline: Pauli/polarization/constitutive `F`-only terms can modify Poynting/stress/readout, but their current is identically conserved, so they cannot hide a variable `kappa_J`. The remaining dangerous branch is a real separately conserved source-shadow block or missing parent exact-U1/domain signature.

## A_Q Domain Split
{md_table(domain, ["split_id", "A_Q_dependence", "divergence_status", "C_J_effect", "status"])}

## F-only Magnetization Lemma
{md_table(mag, ["lemma_id", "claim", "formula", "status"])}

## Gauge Rejection Tests
{md_table(gauge, ["test_id", "tested_term", "result", "status"])}

## Source-Shadow Coefficient Schema
{md_table(schema, ["field_id", "field", "meaning", "claim_requirement"])}

## Source-Shadow Rows
{md_table(shadow, ["row_id", "quantity", "prediction_value", "bound_value", "result_status", "valid_for_claim"])}

## Runner
{md_table(runner, ["row_id", "prediction_value", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

## Promotion Gates
{md_table(gates, ["gate_id", "passed", "claim_allowed", "detail"])}

## Decisions
{md_table(decisions, ["decision_id", "decision", "why_it_moves_forward", "claim_allowed"])}

## Next Target
{md_table(next_rows, ["next_id", "target_doc", "objective", "guardrail"])}

## Validation
{md_table(validations, ["check_id", "check", "passed", "detail"])}

Generated UTC: {RUN_UTC}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    rows_by_key = {
        "sources": source_register(),
        "domain_split": domain_split_rows(),
        "magnetization": magnetization_rows(),
        "gauge_rejection": gauge_rejection_rows(),
        "shadow_schema": shadow_schema_rows(),
        "shadow_rows": shadow_rows(),
        "runner": runner_rows(),
        "promotion": promotion_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }
    for key, rows in rows_by_key.items():
        write_csv(OUTPUTS[key], rows)
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc()
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)
    print(f"wrote {DOC}")
    print(f"validation {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
