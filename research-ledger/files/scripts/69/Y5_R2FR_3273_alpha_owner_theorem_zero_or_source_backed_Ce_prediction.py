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

DOC = ROOT / "3273-Y5-R2FR-alpha-owner-theorem-zero-or-source-backed-Ce-prediction-under-AX1090.md"

SRC_3272_DOC = ROOT / "3272-Y5-R2FR-parent-visible-coefficient-algebra-construction-or-first-real-coupling-row-under-AX1090.md"
SRC_3272_ALPHA = OUT / "P8_Y5_R2FR_3272_SELECTED_ALPHA_EM_COUPLING_ROW_NONCLAIM.csv"
SRC_3272_RUNNER = OUT / "P8_Y5_R2FR_3272_ALPHA_EM_BOUND_RUNNER_RESULTS_NONCLAIM.csv"
SRC_3272_VAL = OUT / "P8_Y5_BRR545_3272_VALIDATION.csv"
SRC_988 = OUT / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv"
SRC_989 = OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv"
SRC_1051 = OUT / "P8_Y5_R10_1051_ALPHA_OWNER_RADIATIVE_CLOSURE_AUDIT.csv"
SRC_1057 = OUT / "P8_Y5_R10_1057_UNIQUE_MAXWELL_SUBBLOCK_THEOREM_ATTEMPT.csv"
SRC_1057_CT = OUT / "P8_Y5_R10_1057_F2_COUNTERTERM_LEDGER.csv"
SRC_1099_OWNER = OUT / "P8_Y5_R10_1099_EM_KINETIC_OWNER_THEOREM_ATTEMPT.csv"
SRC_1099_EXC = OUT / "P8_Y5_R10_1099_NO_EXTRA_F2_EXCLUSION_AUDIT.csv"
SRC_1099_ALPHA = OUT / "P8_Y5_R10_1099_ALPHA_COEFFICIENT_SOURCE_ROWS_NONCLAIM.csv"
SRC_1101_GAUGE = OUT / "P8_Y5_R10_1101_GAUGE_NORM_THEOREM_ATTEMPT.csv"
SRC_1101_CANDIDATES = OUT / "P8_Y5_R10_1101_GAUGE_NORM_OWNER_CANDIDATE_AUDIT.csv"
SRC_1101_ROUTE = OUT / "P8_Y5_R10_1101_ALPHA_ROUTE_DECISION.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3273_SOURCE_REGISTER.csv",
    "decomposition": OUT / "P8_Y5_R2FR_3273_ALPHA_COEFFICIENT_DECOMPOSITION.csv",
    "owner_audit": OUT / "P8_Y5_R2FR_3273_ALPHA_OWNER_CLAUSE_AUDIT.csv",
    "zero_theorem": OUT / "P8_Y5_R2FR_3273_ALPHA_ZERO_THEOREM_ATTEMPT.csv",
    "prediction_schema": OUT / "P8_Y5_R2FR_3273_CE_PREDICTION_SCHEMA.csv",
    "prediction_rows": OUT / "P8_Y5_R2FR_3273_CE_PREDICTION_ROWS_NONCLAIM.csv",
    "runner_results": OUT / "P8_Y5_R2FR_3273_CE_BOUND_RUNNER_RESULTS_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3273_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3273_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3273_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3273_VALIDATION.csv",
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


def alpha_bound_row() -> dict[str, str]:
    rows = read_csv(SRC_3272_ALPHA)
    return rows[0]


def alpha_bound() -> float:
    return float(alpha_bound_row()["bound_value"])


def source_register() -> list[dict[str, Any]]:
    sources = [
        (SRC_3272_DOC, "3272 selected the first finite alpha/EM coupling row", ["ALPHA3272_0", "C_e", "prediction"]),
        (SRC_3272_ALPHA, "source-backed pure-alpha DD envelope selected by 3272", ["ALPHA3272_0", "bound_value", "MISSING"]),
        (SRC_3272_RUNNER, "3272 bound-runner smoke expectations", ["ARUN3272_0", "ARUN3272_3"]),
        (SRC_3272_VAL, "3272 validation", ["VAL3272_8", "overall"]),
        (SRC_988, "EM lock theorem gate", ["EMLOCK988_1", "unique_Maxwell_F2", "EMLOCK988_5"]),
        (SRC_989, "EM lock signature audit", ["ELA989_1", "unique_F2", "ELA989_5"]),
        (SRC_1051, "alpha owner/radiative closure audit", ["AOR1051_0", "AOR1051_3"]),
        (SRC_1057, "unique Maxwell subblock theorem attempt", ["UMS1057_2", "UMS1057_5"]),
        (SRC_1057_CT, "F2 counterterm ledger", ["CT1057_0", "CT1057_1", "CT1057_2"]),
        (SRC_1099_OWNER, "EM kinetic owner theorem attempt", ["UEM1099_1", "UEM1099_2", "UEM1099_3"]),
        (SRC_1099_EXC, "no-extra-F2 exclusion audit", ["EXC1099_0", "EXC1099_5"]),
        (SRC_1099_ALPHA, "existing alpha coefficient source rows", ["ASR1099_0", "ASR1099_3"]),
        (SRC_1101_GAUGE, "gauge norm theorem attempt", ["GFT1101_1", "GFT1101_4"]),
        (SRC_1101_CANDIDATES, "gauge norm owner candidates", ["GNO1101_0", "GNO1101_6"]),
        (SRC_1101_ROUTE, "alpha route decision", ["ROUTE1101_2", "BEST_IMMEDIATE"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3273_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "decomp_id": "ADECOMP3273_0_low_energy_EM_normalization",
            "object": "visible low-energy Maxwell/source block",
            "formula": "S_EM=-1/4 int mu_obs Z_Q(X) F_Q^2 + int mu_obs kappa_J(X) A_Q_mu J_Q^mu + readout",
            "meaning": "Z_Q owns the Maxwell kinetic norm; kappa_J owns current/charge normalization; readout owns hbar*c/Hodge/coframe conversion.",
            "status": "EXACT_PARAMETRIZATION_OF_THE_MISSING_COUPLING",
            "source_basis": "1099 UEM1099_1; 988 EMLOCK988_1-3; 989 ELA989_1-3",
            "valid_for_claim": "false",
        },
        {
            "decomp_id": "ADECOMP3273_1_alpha_log_derivative_law",
            "object": "finite alpha/EM row coefficient",
            "formula": "C_e := L_X ln(alpha_EM) = 2 C_J - C_Z - C_R, where C_Z=L_X ln Z_Q, C_J=L_X ln kappa_J, C_R=L_X ln(readout_alpha)",
            "meaning": "This is the exact contract the parent action must satisfy; alpha zero is not magic, it is the vanishing of three owner slopes.",
            "status": "DERIVED_WITHIN_STANDARD_A_DOT_J_AND_ZF2_CONVENTION",
            "source_basis": "3272 ALPHA3272_0; 1099 UEM1099_1; 1101 GFT1101_1-2",
            "valid_for_claim": "false",
        },
        {
            "decomp_id": "ADECOMP3273_2_zero_condition",
            "object": "alpha-owner theorem zero",
            "formula": "If C_Z=0, C_J=0, and C_R=0 under the same quotient-local generator X, then C_e=0 exactly.",
            "meaning": "A parent-signed unique Maxwell owner, fixed current owner, and fixed readout would close the alpha channel without fitting.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "source_basis": "988 EMLOCK988_5; 1099 UEM1099_3; 1057 UMS1057_5",
            "valid_for_claim": "false",
        },
        {
            "decomp_id": "ADECOMP3273_3_live_counterterm_law",
            "object": "retained alpha leak",
            "formula": "DeltaS=-1/4 int mu_obs f_X(I_hid)F_Q^2 gives C_Z=L_X ln(Z_parent+f_X), hence C_e=-C_Z if C_J=C_R=0.",
            "meaning": "The current corpus cannot call C_e zero while hidden-visible F2 coefficient maps remain legal.",
            "status": "COUNTERTERM_SURVIVES_CURRENT_CORPUS",
            "source_basis": "1057 CT1057_1; 1099 UEM1099_2; 1099 EXC1099_0-1",
            "valid_for_claim": "false",
        },
    ]


def owner_clause_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "AOWN3273_0_CZ_Maxwell_kinetic_owner",
            "coefficient_owned": "C_Z=L_X ln Z_Q",
            "required_parent_signature": "Z_Q=C_P<T_Q,T_Q>_P is fixed parent representation/fibre-norm data and no independent lambda_A or f(I_hid)F_Q^2 term exists.",
            "current_evidence": "988 and 1057 both keep lambda_A/F2 counterterms legal; 1101 says gauge norm owner is not derived.",
            "status": "FAILED_CURRENT_CORPUS",
            "parent_signed": "false",
            "blocks_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AOWN3273_1_CJ_current_charge_owner",
            "coefficient_owned": "C_J=L_X ln kappa_J",
            "required_parent_signature": "matter current, charge lattice labels, and source normalization descend from the same compact T_Q Noether owner.",
            "current_evidence": "988 EMLOCK988_2 and 989 ELA989_2 list current owner as not parent-signed.",
            "status": "UNSIGNED",
            "parent_signed": "false",
            "blocks_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AOWN3273_2_CR_readout_owner",
            "coefficient_owned": "C_R=L_X ln(readout_alpha)",
            "required_parent_signature": "Hodge star, coframe, hbar*c, clock/spectroscopy readout, and dimensionless alpha conversion are quotient-fixed.",
            "current_evidence": "988 EMLOCK988_3, 989 ELA989_3, and 1051 AOR1051_0 keep readout leakage open.",
            "status": "UNSIGNED",
            "parent_signed": "false",
            "blocks_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AOWN3273_3_no_direct_alpha_vertex",
            "coefficient_owned": "no extra alpha/material binding vertex",
            "required_parent_signature": "S_matter has no alpha_EM(chi_X), f_A(chi_X)F^2, m_A(chi_X), or binding-response vertex after quotient projection.",
            "current_evidence": "988 EMLOCK988_4 and 1099 EXC1099_3-4 say this would work if parent-signed but is not signed now.",
            "status": "UNSIGNED_COUNTEREXAMPLE_CLASS_RETAINED",
            "parent_signed": "false",
            "blocks_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AOWN3273_4_radiative_effective_closure",
            "coefficient_owned": "loop/readout induced C_e",
            "required_parent_signature": "the effective action and laboratory readout do not regenerate a hidden-dependent F_Q^2 threshold after tree-level descent.",
            "current_evidence": "1057 CT1057_2 and 1099 EXC1099_5 keep radiative/readout closure unsigned.",
            "status": "UNSIGNED",
            "parent_signed": "false",
            "blocks_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "clause_id": "AOWN3273_5_alpha_owner_verdict",
            "coefficient_owned": "C_e",
            "required_parent_signature": "AOWN3273_0 through AOWN3273_4 are all parent-signed under the same local generator.",
            "current_evidence": "At least one required clause fails and the others are unsigned, so the zero theorem is conditional only.",
            "status": "ALPHA_OWNER_ZERO_NOT_PARENT_SIGNED",
            "parent_signed": "false",
            "blocks_zero": "true",
            "valid_for_claim": "false",
        },
    ]


def zero_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "ZTH3273_0_statement",
            "claim_piece": "alpha-owner zero theorem",
            "mathematical_statement": "For S_EM=-1/4 Z_Q F_Q^2 + kappa_J A_Q.J_Q with fixed alpha readout R_alpha, C_e=L_X ln alpha_EM=2C_J-C_Z-C_R. If C_Z=C_J=C_R=0, then C_e=0.",
            "derivation_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_or_blocker": "log differentiation of alpha_EM proportional to kappa_J^2/(Z_Q R_alpha)",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZTH3273_1_parent_owner_route",
            "claim_piece": "route that would set C_Z=C_J=C_R=0",
            "mathematical_statement": "Z_Q, kappa_J, and R_alpha descend from fixed parent representation/readout data, so Lie_X of each object vanishes on the local quotient fibre.",
            "derivation_status": "VALID_IF_OWNER_CLAUSES_SIGNED",
            "proof_or_blocker": "requires unique Maxwell norm, compact charge-current owner, and readout descent.",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZTH3273_2_current_corpus_test",
            "claim_piece": "can current MTS sign the owner route",
            "mathematical_statement": "Current source sweep tests AOWN3273_0..4.",
            "derivation_status": "FAILS_CURRENT_CORPUS",
            "proof_or_blocker": "independent F_Q^2 coefficient remains legal; current owner/readout/radiative clauses are unsigned.",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZTH3273_3_finite_route_if_zero_fails",
            "claim_piece": "source-backed nonzero C_e alternative",
            "mathematical_statement": "A numeric prediction may still pass only if C_Z, C_J, and C_R, or their combined C_e, are sourced and abs(C_e)<=1.389797711495e-12.",
            "derivation_status": "RUNNABLE_GATE_BUILT",
            "proof_or_blocker": "prediction remains absent; smoke rows only validate the gate.",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "ZTH3273_4_verdict",
            "claim_piece": "C_e=0 or finite prediction",
            "mathematical_statement": "C_e=0 is proven as a conditional theorem but not promoted; finite C_e prediction is not supplied by current parent sources.",
            "derivation_status": "NO_ALPHA_CLAIM",
            "proof_or_blocker": "missing parent-owned Maxwell kinetic/current/readout signatures or source-backed numeric C_e.",
            "valid_for_claim": "false",
        },
    ]


def prediction_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "field_id": "SCHEMA3273_0_CZ",
            "field": "C_Z",
            "meaning": "local logarithmic slope of Maxwell kinetic coefficient Z_Q",
            "accepted_source": "parent-signed unique gauge norm theorem or numeric source row for L_X ln Z_Q",
            "required_for_claim": "true",
        },
        {
            "field_id": "SCHEMA3273_1_CJ",
            "field": "C_J",
            "meaning": "local logarithmic slope of charge-current normalization kappa_J",
            "accepted_source": "parent-signed Noether/current owner theorem or numeric source row for L_X ln kappa_J",
            "required_for_claim": "true",
        },
        {
            "field_id": "SCHEMA3273_2_CR",
            "field": "C_R",
            "meaning": "local logarithmic slope of dimensionless alpha readout factors",
            "accepted_source": "parent-signed Hodge/coframe/hbar*c/readout descent theorem or numeric source row",
            "required_for_claim": "true",
        },
        {
            "field_id": "SCHEMA3273_3_Ce",
            "field": "C_e",
            "meaning": "C_e=2C_J-C_Z-C_R, directly compared to the 3272 pure alpha DD bound",
            "accepted_source": "computed from sourced components or direct sourced C_e row with normalization convention",
            "required_for_claim": "true",
        },
    ]


def ce_from_components(cz: float, cj: float, cr: float) -> float:
    return 2.0 * cj - cz - cr


def prediction_rows() -> list[dict[str, Any]]:
    bound = alpha_bound()
    half_ce = 0.5 * bound
    twice_ce = 2.0 * bound
    return [
        {
            "prediction_id": "CE3273_0_missing_parent_components",
            "C_Z": "MISSING_PARENT_MAXWELL_KINETIC_SLOPE",
            "C_J": "MISSING_PARENT_CURRENT_NORMALIZATION_SLOPE",
            "C_R": "MISSING_PARENT_READOUT_SLOPE",
            "C_e_prediction": "MISSING",
            "normalization_law": "C_e=2C_J-C_Z-C_R",
            "prediction_source": "MISSING_PARENT_COMPONENTS",
            "source_backed": "false",
            "parent_signed_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "prediction_id": "CE3273_1_theorem_zero_conditional",
            "C_Z": "0",
            "C_J": "0",
            "C_R": "0",
            "C_e_prediction": fmt(ce_from_components(0.0, 0.0, 0.0)),
            "normalization_law": "C_e=2C_J-C_Z-C_R",
            "prediction_source": str(OUTPUTS["zero_theorem"]),
            "source_backed": "false",
            "parent_signed_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "prediction_id": "CE3273_2_hidden_F2_counterterm_symbolic",
            "C_Z": "L_X ln(Z_parent+f_X(I_hid))",
            "C_J": "0_if_current_owner_signed_else_MISSING",
            "C_R": "0_if_readout_owner_signed_else_MISSING",
            "C_e_prediction": "MISSING_NUMERIC_COUNTERTERM_SLOPE",
            "normalization_law": "C_e=2C_J-C_Z-C_R",
            "prediction_source": str(SRC_1057_CT),
            "source_backed": "false",
            "parent_signed_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "prediction_id": "CE3273_3_half_bound_smoke",
            "C_Z": fmt(-half_ce),
            "C_J": "0",
            "C_R": "0",
            "C_e_prediction": fmt(half_ce),
            "normalization_law": "C_e=2C_J-C_Z-C_R",
            "prediction_source": "SMOKE_NUMERIC_NONCLAIM",
            "source_backed": "false",
            "parent_signed_zero": "false",
            "valid_for_claim": "false",
        },
        {
            "prediction_id": "CE3273_4_twice_bound_smoke",
            "C_Z": fmt(-twice_ce),
            "C_J": "0",
            "C_R": "0",
            "C_e_prediction": fmt(twice_ce),
            "normalization_law": "C_e=2C_J-C_Z-C_R",
            "prediction_source": "SMOKE_NUMERIC_NONCLAIM",
            "source_backed": "false",
            "parent_signed_zero": "false",
            "valid_for_claim": "false",
        },
    ]


def numeric_or_none(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def runner_results() -> list[dict[str, Any]]:
    bound = alpha_bound()
    source_row = alpha_bound_row()
    expected = {
        "CE3273_0_missing_parent_components": "REFUSE_OR_FAIL",
        "CE3273_1_theorem_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "CE3273_2_hidden_F2_counterterm_symbolic": "REFUSE_OR_FAIL",
        "CE3273_3_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "CE3273_4_twice_bound_smoke": "FAIL_BOUND",
    }
    rows: list[dict[str, Any]] = []
    for idx, pred in enumerate(prediction_rows()):
        value = numeric_or_none(pred["C_e_prediction"])
        if value is None:
            abs_prediction = "MISSING"
            ratio = "MISSING"
            pass_bound = False
            result = "REFUSE_OR_FAIL"
        else:
            abs_value = abs(value)
            abs_prediction = fmt(abs_value)
            ratio = fmt(abs_value / bound)
            pass_bound = abs_value <= bound
            result = "PASS_NUMERIC_NONCLAIM" if pass_bound else "FAIL_BOUND"
        rows.append(
            {
                "case_id": f"ARUN3273_{idx}_{pred['prediction_id']}",
                "prediction_id": pred["prediction_id"],
                "C_e_prediction": pred["C_e_prediction"],
                "bound_value": source_row["bound_value"],
                "bound_units": source_row["bound_units"],
                "bound_source": source_row["bound_source"],
                "abs_prediction": abs_prediction,
                "prediction_over_bound": ratio,
                "source_backed": pred["source_backed"],
                "parent_signed_zero": pred["parent_signed_zero"],
                "pass_bound": bool_str(pass_bound),
                "result": result,
                "expected": expected[pred["prediction_id"]],
                "expectation_met": bool_str(result == expected[pred["prediction_id"]]),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3273_0_decomposition_derived",
            "gate": "C_e decomposition is explicit",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "C_e=2C_J-C_Z-C_R gives the exact next contract, not a physical pass by itself.",
        },
        {
            "gate_id": "GATE3273_1_alpha_owner_zero_parent_signed",
            "gate": "all alpha-owner clauses parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "unique F2/gauge norm owner fails current corpus; current/readout/radiative clauses unsigned.",
        },
        {
            "gate_id": "GATE3273_2_source_backed_numeric_Ce",
            "gate": "sourced numeric C_e prediction exists",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "only missing/theorem-smoke/counterterm-smoke rows exist; no parent-owned numeric C_e.",
        },
        {
            "gate_id": "GATE3273_3_bound_runner_disciplined",
            "gate": "runner refuses missing rows and fails over-bound smoke",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner_results())),
            "claim_allowed": "false",
            "detail": "the gate is runnable but all claim rows remain nonclaim.",
        },
        {
            "gate_id": "GATE3273_4_no_local_GR_or_Maxwell_claim",
            "gate": "no local-GR/WEP/Maxwell pass is promoted",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3273 is a derivation contract plus finite-coefficient runner, not a closure claim.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3273_0_main_result",
            "decision": "C_e has been reduced to component slopes C_Z, C_J, and C_R.",
            "why_it_moves_forward": "the missing coupling is no longer a vague alpha-owner problem; it is a three-slope source-coupling contract.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3273_1_zero_route_status",
            "decision": "alpha-owner theorem zero is exact but not parent-signed.",
            "why_it_moves_forward": "we know precisely which signatures would make C_e=0 and which counterterm blocks the proof.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3273_2_finite_route_status",
            "decision": "finite C_e route is runnable but prediction-missing.",
            "why_it_moves_forward": "any future sourced prediction now immediately scores against the 1.389797711495e-12 pure-alpha envelope.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3273_3_next_route",
            "decision": "stop circling alpha and attack current/source normalization and EM stress next.",
            "why_it_moves_forward": "C_J is shared by Maxwell source coupling, Lorentz force normalization, Poynting/EM stress transfer, and the alpha row.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3273_0_3274",
            "target_doc": "3274-Y5-R2FR-current-normalization-and-EM-stress-source-coupling-derivation-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3274_current_normalization_and_EM_stress_source_coupling_derivation.py",
            "objective": "Derive or bound kappa_J/current normalization and EM stress transfer from the parent action: vary -Z_Q F^2/4 + kappa_J A.J, derive Maxwell equation, Lorentz-force exchange, Poynting/stress conservation, and identify whether C_J=0 or a numeric C_J prediction is source-backed.",
            "guardrail": "Do not re-open alpha generally; use the 3273 law C_e=2C_J-C_Z-C_R and push the source/current coupling piece.",
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
    owner_verdict = owner_clause_audit_rows()[-1]
    runner = runner_results()
    gates = promotion_gates()
    bound = alpha_bound()
    predictions = prediction_rows()
    validations = [
        {
            "check_id": "VAL3273_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3273_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3273_2_outputs_parse",
            "check": "all 3273 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3273_3_bound_positive",
            "check": "selected alpha bound is positive numeric",
            "passed": bool_str(bound > 0.0),
            "detail": fmt(bound),
        },
        {
            "check_id": "VAL3273_4_alpha_zero_not_falsely_signed",
            "check": "alpha-owner zero remains conditional rather than promoted",
            "passed": bool_str(owner_verdict["parent_signed"] == "false" and owner_verdict["status"] == "ALPHA_OWNER_ZERO_NOT_PARENT_SIGNED"),
            "detail": owner_verdict["status"],
        },
        {
            "check_id": "VAL3273_5_no_claim_prediction_rows",
            "check": "all C_e prediction rows remain nonclaim",
            "passed": bool_str(all(row["valid_for_claim"] == "false" for row in predictions)),
            "detail": ";".join(row["prediction_id"] for row in predictions if row["valid_for_claim"] != "false"),
        },
        {
            "check_id": "VAL3273_6_runner_expectations",
            "check": "C_e runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['prediction_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3273_7_claim_gates_false",
            "check": "no 3273 gate allows local-GR/WEP/Maxwell claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3273_8_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3273_9_overall",
            "check": "3273 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3273_9_overall")
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
    bound_row = alpha_bound_row()
    decomp = read_csv(OUTPUTS["decomposition"])
    audit = read_csv(OUTPUTS["owner_audit"])
    theorem = read_csv(OUTPUTS["zero_theorem"])
    preds = read_csv(OUTPUTS["prediction_rows"])
    runner = read_csv(OUTPUTS["runner_results"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3273 - Alpha-owner theorem zero or source-backed C_e prediction under AX1090

## Summary

3273 does **not** merely say the alpha coupling is missing. It reduces the missing object to an explicit local coupling law:

`C_e := L_X ln(alpha_EM) = 2 C_J - C_Z - C_R`.

Here `C_Z=L_X ln Z_Q` is the Maxwell kinetic slope, `C_J=L_X ln kappa_J` is the charge/current normalization slope, and `C_R=L_X ln(readout_alpha)` is the dimensionless readout slope. The zero theorem is exact if all three slopes vanish under the same local generator. The current corpus does **not** parent-sign that zero because independent/hidden/radiative `F_Q^2` counterterms and readout/current-owner gaps remain open.

## 3272 Alpha Bound Imported

| row_id | coefficient | bound_value | bound_units | current_status |
| --- | --- | --- | --- | --- |
| {bound_row['row_id']} | {bound_row['coefficient']} | {bound_row['bound_value']} | {bound_row['bound_units']} | {bound_row['current_status']} |

## Derived C_e Decomposition
{md_table(decomp, ["decomp_id", "formula", "status", "meaning"])}

## Alpha Owner Clause Audit
{md_table(audit, ["clause_id", "coefficient_owned", "status", "parent_signed", "blocks_zero"])}

## Zero Theorem Attempt
{md_table(theorem, ["proof_id", "claim_piece", "derivation_status", "proof_or_blocker"])}

## C_e Prediction Rows
{md_table(preds, ["prediction_id", "C_Z", "C_J", "C_R", "C_e_prediction", "source_backed", "parent_signed_zero", "valid_for_claim"])}

## C_e Bound Runner
{md_table(runner, ["prediction_id", "C_e_prediction", "bound_value", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

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
        "decomposition": decomposition_rows(),
        "owner_audit": owner_clause_audit_rows(),
        "zero_theorem": zero_theorem_rows(),
        "prediction_schema": prediction_schema_rows(),
        "prediction_rows": prediction_rows(),
        "runner_results": runner_results(),
        "promotion": promotion_gates(),
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
