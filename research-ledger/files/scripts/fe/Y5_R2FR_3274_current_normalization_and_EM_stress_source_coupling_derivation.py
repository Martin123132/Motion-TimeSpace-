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

DOC = ROOT / "3274-Y5-R2FR-current-normalization-and-EM-stress-source-coupling-derivation-under-AX1090.md"

SRC_3273_DOC = ROOT / "3273-Y5-R2FR-alpha-owner-theorem-zero-or-source-backed-Ce-prediction-under-AX1090.md"
SRC_3273_DECOMP = OUT / "P8_Y5_R2FR_3273_ALPHA_COEFFICIENT_DECOMPOSITION.csv"
SRC_3273_NEXT = OUT / "P8_Y5_R2FR_3273_NEXT_TARGET.csv"
SRC_3272_ALPHA = OUT / "P8_Y5_R2FR_3272_SELECTED_ALPHA_EM_COUPLING_ROW_NONCLAIM.csv"
SRC_642_MD = OUT / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv"
SRC_642_TA = OUT / "P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv"
SRC_765_GATE = OUT / "P8_Y5_R10_765_MAXWELL_KINETIC_INHERITANCE_GATE.csv"
SRC_765_CEX = OUT / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
SRC_771_AUDIT = OUT / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"
SRC_771_ROUTE = OUT / "P8_Y5_R10_771_CURRENT_OWNER_ROUTE_COMPARISON.csv"
SRC_993_GATE = OUT / "P8_Y5_R10_993_CURRENT_EXTRACTION_GATE.csv"
SRC_993_SECTOR = OUT / "P8_Y5_R10_993_SECTOR_CURRENT_EXTRACTION_LEDGER.csv"
SRC_SC_WARD = OUT / "P8_source_current_Ward_universality_CONTRACT.csv"
SRC_CC_DIRECT = OUT / "P8_charge_current_equality_DIRECT_ATTEMPT.csv"
SRC_PARENT_NOETHER = OUT / "P8_PARENT_NOETHER_CLOSURE_THEOREM.csv"
SRC_1765_NOETHER = OUT / "P8_Y5_PARENT_QLOC_1765_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv"
SRC_1765_OWNER = OUT / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv"
SRC_GK_STRESS = OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3274_SOURCE_REGISTER.csv",
    "action_variation": OUT / "P8_Y5_R2FR_3274_EM_ACTION_VARIATION_DERIVATION.csv",
    "gauge_lock": OUT / "P8_Y5_R2FR_3274_CURRENT_NORMALIZATION_GAUGE_LOCK_LEMMA.csv",
    "stress_poynting": OUT / "P8_Y5_R2FR_3274_EM_STRESS_POYNTING_EXCHANGE_LAW.csv",
    "cj_owner": OUT / "P8_Y5_R2FR_3274_CJ_OWNER_AUDIT.csv",
    "cj_bound": OUT / "P8_Y5_R2FR_3274_CJ_CONDITIONAL_BOUND_ROWS_NONCLAIM.csv",
    "cj_runner": OUT / "P8_Y5_R2FR_3274_CJ_BOUND_RUNNER_RESULTS_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3274_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3274_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3274_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3274_VALIDATION.csv",
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
    return read_csv(SRC_3272_ALPHA)[0]


def alpha_bound() -> float:
    return float(alpha_bound_row()["bound_value"])


def cj_conditional_bound() -> float:
    return 0.5 * alpha_bound()


def source_register() -> list[dict[str, Any]]:
    sources = [
        (SRC_3273_DOC, "3273 handoff: C_e=2C_J-C_Z-C_R and next target", ["C_e :=", "C_J", "Next Target"]),
        (SRC_3273_DECOMP, "3273 decomposition CSV", ["ADECOMP3273_1", "2 C_J"]),
        (SRC_3273_NEXT, "3273 next target CSV", ["NEXT3273_0_3274", "Poynting"]),
        (SRC_3272_ALPHA, "3272 alpha/DD bound row", ["ALPHA3272_0", "bound_value"]),
        (SRC_642_MD, "Maxwell descent attempt", ["MD642_1", "Gauss_Ampere", "MD642_3"]),
        (SRC_642_TA, "Maxwell theorem-zero attempt", ["TA642_3", "TA642_4"]),
        (SRC_765_GATE, "Maxwell kinetic/current inheritance gate", ["MKI765_3", "same_current"]),
        (SRC_765_CEX, "current rescaling counterexamples", ["RCE765_2", "current_rescale"]),
        (SRC_771_AUDIT, "theta/Q_tau current owner audit", ["TQ771_5", "matter_coupling"]),
        (SRC_771_ROUTE, "current owner route comparison", ["COR771_C", "hybrid"]),
        (SRC_993_GATE, "current extraction gate", ["CEG993_1", "CEG993_4"]),
        (SRC_993_SECTOR, "sector current ledger including EM", ["SEC993_7", "EM_charge_coupling"]),
        (SRC_SC_WARD, "source-current Ward universality contract", ["SC2", "SC3"]),
        (SRC_CC_DIRECT, "charge-current equality direct attempt", ["CC2", "CC7"]),
        (SRC_PARENT_NOETHER, "parent Noether closure theorem", ["T505", "Noether"]),
        (SRC_1765_NOETHER, "Noether exchange collapse theorem", ["NEC1765_2", "weight_collapse"]),
        (SRC_1765_OWNER, "total Hilbert source owner audit", ["THO1765_3", "source_shadow"]),
        (SRC_GK_STRESS, "q_loc stress rewrite", ["SR513_0", "T_GK"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3274_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def action_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "AV3274_0_action_block",
            "object": "low-energy EM plus source block",
            "formula": "S[A,J;g,X]=int mu_obs[-Z_Q(X)F_Q^2/4 + s_J kappa_J(X) A_Q_mu J_Q^mu] + S_matter + S_owner[X]",
            "derivation": "Use one explicit sign flag s_J so the source normalization question is not hidden in conventions.",
            "status": "EXACT_STARTING_BLOCK_FOR_CJ_AUDIT",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "AV3274_1_Maxwell_equation",
            "object": "variation with respect to A_Q",
            "formula": "nabla_mu(Z_Q F_Q^{mu nu}) = -s_J kappa_J J_Q^nu",
            "derivation": "Integrate -Z_Q F^{mu nu} nabla_mu(delta A_nu) by parts and combine with s_J kappa_J J^nu delta A_nu.",
            "status": "DERIVED_FROM_ASSUMED_BLOCK",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "AV3274_2_weighted_current_conservation",
            "object": "divergence of Maxwell equation",
            "formula": "0 = nabla_nu nabla_mu(Z_Q F_Q^{mu nu}) = -s_J nabla_nu(kappa_J J_Q^nu)",
            "derivation": "antisymmetry of F_Q makes the double divergence vanish, so the source entering Maxwell is the weighted current kappa_J J_Q.",
            "status": "EXACT_CURRENT_CONSTRAINT",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "AV3274_3_CJ_definition",
            "object": "current/source normalization slope",
            "formula": "C_J := L_X ln kappa_J",
            "derivation": "This is the 3273 alpha decomposition component that controls Maxwell source normalization and Lorentz/Poynting transfer.",
            "status": "DEFINED_AS_FINITE_COUPLING_TARGET",
            "valid_for_claim": "false",
        },
        {
            "derivation_id": "AV3274_4_if_J_Noether_conserved",
            "object": "separately owned representation current",
            "formula": "if nabla_mu J_Q^mu=0 then J_Q^mu nabla_mu ln kappa_J=0",
            "derivation": "Substitute separate Noether conservation into nabla_mu(kappa_J J_Q^mu)=0.",
            "status": "GAUGE_CURRENT_LOCK_LEMMA",
            "valid_for_claim": "false",
        },
    ]


def gauge_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "lemma_id": "GL3274_0_statement",
            "lemma": "source-current gauge lock",
            "mathematical_statement": "Gauge invariance and the Maxwell equation require nabla_mu(kappa_J J_Q^mu)=0. If J_Q is already the parent Noether current with nabla_mu J_Q^mu=0, then J_Q^mu nabla_mu ln kappa_J=0.",
            "consequence": "A spatial/time/material variation in kappa_J is not free; it must either vanish on all allowed currents or be carried by an extra compensating current.",
            "status": "EXACT_CONDITIONAL_LEMMA",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "GL3274_1_arbitrary_current_corollary",
            "lemma": "constant kappa corollary",
            "mathematical_statement": "If the ordinary matter sector permits enough local current directions through each lab point, J_Q^mu nabla_mu ln kappa_J=0 for all such J_Q implies nabla_mu kappa_J=0 and hence C_J=0.",
            "consequence": "This is the clean route to source-normalization zero: not a fitted parameter, but a gauge-current consistency result.",
            "status": "VALID_IF_CURRENT_OWNER_AND_CURRENT_RICHNESS_SIGNED",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "GL3274_2_countermodel_compensator",
            "lemma": "compensator escape",
            "mathematical_statement": "nabla_mu(kappa_J J_Q^mu + J_comp^mu)=0 can hold with variable kappa_J if an extra parent current J_comp carries the mismatch.",
            "consequence": "Current MTS cannot promote C_J=0 unless it excludes compensator/source-shadow/non-Hilbert EM charge currents.",
            "status": "COUNTERMODEL_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "lemma_id": "GL3274_3_relation_to_3273",
            "lemma": "alpha row pressure",
            "mathematical_statement": "With C_Z=C_R=0, the 3273 law gives C_e=2C_J, so |C_J| <= |C_e|_bound/2.",
            "consequence": "The pure-alpha DD envelope can bound current normalization only under the explicit Maxwell/readout-zero side conditions.",
            "status": "CONDITIONAL_BOUND_ROUTE",
            "valid_for_claim": "false",
        },
    ]


def stress_poynting_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "SP3274_0_stress_tensor",
            "object": "EM Hilbert stress",
            "formula": "T_EM^{mu nu}=Z_Q(F_Q^{mu rho}F_Q^nu_rho - 1/4 g_obs^{mu nu}F_Q^2) up to the fixed metric-sign convention",
            "derivation": "Metric variation of the Maxwell kinetic block with Z_Q treated as the parent-owned scalar coefficient.",
            "status": "DERIVED_FROM_ASSUMED_BLOCK",
            "valid_for_claim": "false",
        },
        {
            "law_id": "SP3274_1_stress_exchange",
            "object": "covariant EM energy-momentum exchange",
            "formula": "nabla_mu T_EM^{mu nu} = s_J kappa_J F_Q^nu_mu J_Q^mu + Q_Z^nu, with Q_Z^nu proportional to F_Q^2 nabla^nu Z_Q and owner-sector Euler terms",
            "derivation": "Use the Maxwell equation plus the Bianchi identity; Z_Q gradients are not EM stress conservation, they are exchange with the parent owner of Z_Q.",
            "status": "EXACT_CONDITIONAL_EXCHANGE_LAW",
            "valid_for_claim": "false",
        },
        {
            "law_id": "SP3274_2_matter_exchange",
            "object": "Lorentz-force transfer",
            "formula": "nabla_mu(T_matter^{mu nu}+T_EM^{mu nu}+T_owner^{mu nu})=0; if Q_Z^nu=0 then nabla_mu T_matter^{mu nu}=-s_J kappa_J F_Q^nu_mu J_Q^mu",
            "derivation": "Diffeomorphism Ward identity for the combined parent block fixes the equal-and-opposite force law.",
            "status": "SOURCE_COUPLING_CONTRACT_DERIVED",
            "valid_for_claim": "false",
        },
        {
            "law_id": "SP3274_3_Poynting_readout",
            "object": "observer-frame EM energy flow",
            "formula": "u_EM=Z_Q(E^2+B^2)/2, S_EM^i=Z_Q(E x B)^i, and partial_t u_EM + div S_EM = -s_J kappa_J E.J + Z_Q/readout-gradient exchange terms",
            "derivation": "3+1 split of SP3274_1 in the observed coframe.",
            "status": "POYNTING_BACKGROUND_FIELD_ROUTE_MADE_EXPLICIT",
            "valid_for_claim": "false",
        },
        {
            "law_id": "SP3274_4_q_loc_link",
            "object": "relation to local residual q_loc",
            "formula": "unowned EM/source exchange contributes to the same kind of projected Ward residual as q_loc^nu=P_loc nabla_mu T_extra^{mu nu}",
            "derivation": "Imports the 513 stress rewrite: failed owner terms must be stress-exchange residuals, not silent closure assumptions.",
            "status": "LOCAL_RESIDUAL_MAPPING_READY",
            "valid_for_claim": "false",
        },
    ]


def cj_owner_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CJA3274_0_weighted_current_owned",
            "needed_signature": "J_Q is the parent Noether/representation current and the Maxwell source is exactly kappa_J J_Q.",
            "evidence": "642 supports Maxwell action shape; 771/993 say current owner/extraction remains scaffold-only.",
            "status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CJA3274_1_no_current_rescale",
            "needed_signature": "No q_A(X), c_A(X), kappa_A(X), source-shadow, or hidden current rescaling survives in S_int.",
            "evidence": "765 retains current rescale counterexample; 1765 collapses relative weights only conditionally to exchange blocks.",
            "status": "UNSIGNED_COUNTERMODEL_RETAINED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CJA3274_2_no_compensator_current",
            "needed_signature": "No extra J_comp current carries nabla(kappa_J J_Q) mismatch.",
            "evidence": "source-current and charge-current files retain non-Hilbert/extra/source-shadow channels.",
            "status": "UNSIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CJA3274_3_current_richness",
            "needed_signature": "ordinary lab matter supplies enough local current directions that J.nabla ln kappa_J=0 forces nabla kappa_J=0.",
            "evidence": "standard matter intuition supports this, but current corpus does not parent-sign the ordinary matter functor/readout at this level.",
            "status": "MATHEMATICALLY_CLEAN_BUT_NOT_PARENT_SIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "audit_id": "CJA3274_4_CJ_zero_verdict",
            "needed_signature": "CJA3274_0 through CJA3274_3 all pass under the same local generator.",
            "evidence": "3274 derives the pressure law, but current owner and compensator exclusions are not signed.",
            "status": "CJ_ZERO_NOT_PARENT_SIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
    ]


def cj_bound_rows() -> list[dict[str, Any]]:
    bound = alpha_bound()
    cj_bound = cj_conditional_bound()
    return [
        {
            "bound_id": "CJB3274_0_conditional_CJ_from_alpha",
            "coefficient": "C_J=L_X ln kappa_J",
            "side_conditions": "C_Z=0 and C_R=0, same local generator X, same observed coframe/readout",
            "bound_value": fmt(cj_bound),
            "bound_units": "dimensionless local logarithmic current-normalization coefficient",
            "bound_law": "|C_J| <= |C_e|_bound/2 because C_e=2C_J-C_Z-C_R",
            "source_bound": fmt(bound),
            "source_path": str(SRC_3272_ALPHA),
            "status": "CONDITIONAL_BOUND_ONLY_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "bound_id": "CJB3274_1_general_CJ_unbounded_by_alpha_alone",
            "coefficient": "C_J=L_X ln kappa_J",
            "side_conditions": "C_Z and C_R not both fixed zero",
            "bound_value": "MISSING_STANDALONE_GENERAL_CJ_BOUND",
            "bound_units": "dimensionless local logarithmic current-normalization coefficient",
            "bound_law": "C_e constrains only 2C_J-C_Z-C_R; without side conditions, C_J can trade against C_Z/C_R.",
            "source_bound": fmt(bound),
            "source_path": str(SRC_3273_DECOMP),
            "status": "REFUSE_STANDALONE_CJ_CLAIM",
            "valid_for_claim": "false",
        },
    ]


def numeric_or_none(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def cj_runner_rows() -> list[dict[str, Any]]:
    cj_bound = cj_conditional_bound()
    cases = [
        ("CJR3274_0_missing_CJ", "MISSING", "REFUSE_OR_FAIL", "MISSING_SOURCE_BACKED_CJ"),
        ("CJR3274_1_CJ_zero_conditional", "0", "PASS_NUMERIC_NONCLAIM", "CONDITIONAL_GAUGE_CURRENT_LOCK_ZERO_NOT_PARENT_SIGNED"),
        ("CJR3274_2_half_conditional_bound", fmt(0.5 * cj_bound), "PASS_NUMERIC_NONCLAIM", "SMOKE_NUMERIC_NONCLAIM"),
        ("CJR3274_3_at_conditional_bound", fmt(cj_bound), "PASS_NUMERIC_NONCLAIM", "SMOKE_NUMERIC_NONCLAIM"),
        ("CJR3274_4_twice_conditional_bound", fmt(2.0 * cj_bound), "FAIL_BOUND", "SMOKE_NUMERIC_NONCLAIM"),
        ("CJR3274_5_general_without_CZ_CR", fmt(0.5 * cj_bound), "REFUSE_OR_FAIL", "SIDE_CONDITIONS_MISSING_CZ_CR_NOT_ZEROED"),
    ]
    rows: list[dict[str, Any]] = []
    for case_id, cj_value, expected, source in cases:
        numeric = numeric_or_none(cj_value)
        side_conditions = "true" if case_id != "CJR3274_5_general_without_CZ_CR" else "false"
        if numeric is None or side_conditions == "false":
            ce_induced = "MISSING" if numeric is None else fmt(2.0 * numeric)
            abs_cj = "MISSING" if numeric is None else fmt(abs(numeric))
            ratio = "MISSING" if numeric is None else fmt(abs(numeric) / cj_bound)
            result = "REFUSE_OR_FAIL"
            pass_bound = False
        else:
            ce_induced_float = 2.0 * numeric
            ce_induced = fmt(ce_induced_float)
            abs_value = abs(numeric)
            abs_cj = fmt(abs_value)
            ratio = fmt(abs_value / cj_bound)
            pass_bound = abs_value <= cj_bound
            result = "PASS_NUMERIC_NONCLAIM" if pass_bound else "FAIL_BOUND"
        rows.append(
            {
                "case_id": case_id,
                "C_J_prediction": cj_value,
                "C_Z_zero_assumed": side_conditions,
                "C_R_zero_assumed": side_conditions,
                "C_e_induced_under_side_conditions": ce_induced,
                "C_J_bound_conditional": fmt(cj_bound),
                "abs_C_J": abs_cj,
                "prediction_over_bound": ratio,
                "prediction_source": source,
                "pass_bound": bool_str(pass_bound),
                "result": result,
                "expected": expected,
                "expectation_met": bool_str(result == expected),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3274_0_variation_derivation",
            "gate": "Maxwell equation and weighted-current conservation derived from explicit block",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "This is a derived low-energy contract, not a parent action signature by itself.",
        },
        {
            "gate_id": "GATE3274_1_gauge_current_lock",
            "gate": "gauge/current lemma identifies route to C_J=0",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "C_J=0 follows only if current owner, no compensator, and current-richness clauses are signed.",
        },
        {
            "gate_id": "GATE3274_2_Poynting_exchange",
            "gate": "Poynting/stress exchange law written",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "EM flow is now mapped to stress exchange and q_loc-style residuals.",
        },
        {
            "gate_id": "GATE3274_3_CJ_zero_parent_signed",
            "gate": "C_J=0 parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "current rescale/source-shadow/compensator exclusions remain unsigned.",
        },
        {
            "gate_id": "GATE3274_4_CJ_runner_disciplined",
            "gate": "runner refuses missing/general rows and fails over-bound smoke",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in cj_runner_rows())),
            "claim_allowed": "false",
            "detail": "conditional runner works only under C_Z=C_R=0 side conditions.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3274_0_real_progress",
            "decision": "C_J is now tied to a weighted-current conservation law, not left as a free symbol.",
            "why_it_moves_forward": "Maxwell variation gives nabla_mu(kappa_J J_Q^mu)=0 and therefore a sharp gauge-current route to C_J=0.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3274_1_poynting_route",
            "decision": "Poynting/EM stress flow is explicitly in the source-coupling stack.",
            "why_it_moves_forward": "S_EM=Z_Q E x B and stress exchange show where a background-field/flow interpretation must live without breaking conservation.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3274_2_CJ_status",
            "decision": "C_J=0 is plausible as a theorem route but not parent-signed.",
            "why_it_moves_forward": "the remaining proof debt is no compensator/source-shadow/current-rescale plus ordinary-current richness, not an undefined coupling mystery.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3274_3_bound_status",
            "decision": "|C_J| <= 6.948988557475e-13 is available only if C_Z=C_R=0.",
            "why_it_moves_forward": "future numeric or theorem-zero C_J rows can be scored immediately, but alpha data cannot bound general C_J alone.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3274_0_3275",
            "target_doc": "3275-Y5-R2FR-no-compensator-current-and-source-shadow-ban-or-finite-CJ-row-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3275_no_compensator_current_and_source_shadow_ban_or_finite_CJ_row.py",
            "objective": "Try to prove the no-compensator/source-shadow clause for kappa_J: show the only gauge current entering Maxwell is the parent Noether current, or emit the first source-backed finite C_J residual row.",
            "guardrail": "Do not re-prove Maxwell variation; start from 3274 weighted-current law and attack the remaining escape routes.",
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
    runner = cj_runner_rows()
    gates = promotion_gate_rows()
    cj_bound_value = cj_conditional_bound()
    validations = [
        {
            "check_id": "VAL3274_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3274_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3274_2_outputs_parse",
            "check": "all 3274 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3274_3_variation_law_present",
            "check": "Maxwell and weighted-current equations are present",
            "passed": bool_str(any(row["derivation_id"] == "AV3274_2_weighted_current_conservation" for row in action_variation_rows())),
            "detail": "nabla_mu(kappa_J J_Q^mu)=0",
        },
        {
            "check_id": "VAL3274_4_poynting_law_present",
            "check": "Poynting/stress exchange law is present",
            "passed": bool_str(any(row["law_id"] == "SP3274_3_Poynting_readout" for row in stress_poynting_rows())),
            "detail": "S_EM=Z_Q(E x B)",
        },
        {
            "check_id": "VAL3274_5_CJ_bound_positive",
            "check": "conditional C_J bound is positive numeric",
            "passed": bool_str(cj_bound_value > 0.0),
            "detail": fmt(cj_bound_value),
        },
        {
            "check_id": "VAL3274_6_CJ_zero_not_falsely_signed",
            "check": "C_J zero remains conditional rather than promoted",
            "passed": bool_str(cj_owner_rows()[-1]["status"] == "CJ_ZERO_NOT_PARENT_SIGNED"),
            "detail": cj_owner_rows()[-1]["status"],
        },
        {
            "check_id": "VAL3274_7_runner_expectations",
            "check": "C_J runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['case_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3274_8_claim_gates_false",
            "check": "no 3274 gate allows local-GR/WEP/Maxwell claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3274_9_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3274_10_overall",
            "check": "3274 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3274_10_overall")
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
    action = read_csv(OUTPUTS["action_variation"])
    gauge = read_csv(OUTPUTS["gauge_lock"])
    stress = read_csv(OUTPUTS["stress_poynting"])
    owner = read_csv(OUTPUTS["cj_owner"])
    bounds = read_csv(OUTPUTS["cj_bound"])
    runner = read_csv(OUTPUTS["cj_runner"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3274 - Current normalization and EM stress/source coupling derivation under AX1090

## Summary

3274 pushes the coupling problem forward into a concrete source law. Starting from the explicit low-energy block

`S[A,J;g,X]=int mu_obs[-Z_Q(X)F_Q^2/4 + s_J kappa_J(X) A_Q_mu J_Q^mu]`,

variation gives

`nabla_mu(Z_Q F_Q^{{mu nu}}) = -s_J kappa_J J_Q^nu`,

and therefore

`nabla_mu(kappa_J J_Q^mu)=0`.

So `C_J=L_X ln kappa_J` is not a free fudge factor. If `J_Q` is separately the parent Noether current, then `J_Q^mu nabla_mu ln kappa_J=0`; if ordinary currents are rich enough and there is no compensator/source-shadow current, this forces `C_J=0`. The current corpus does not yet sign those escape-route exclusions, so no local-GR/Maxwell claim is promoted.

## Action Variation
{md_table(action, ["derivation_id", "formula", "status", "derivation"])}

## Gauge/Current Lock
{md_table(gauge, ["lemma_id", "mathematical_statement", "consequence", "status"])}

## EM Stress and Poynting Exchange
{md_table(stress, ["law_id", "formula", "status", "derivation"])}

## C_J Owner Audit
{md_table(owner, ["audit_id", "needed_signature", "status", "blocks_CJ_zero"])}

## Conditional C_J Bound
{md_table(bounds, ["bound_id", "coefficient", "side_conditions", "bound_value", "status"])}

## C_J Runner
{md_table(runner, ["case_id", "C_J_prediction", "C_Z_zero_assumed", "C_R_zero_assumed", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

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
        "action_variation": action_variation_rows(),
        "gauge_lock": gauge_lock_rows(),
        "stress_poynting": stress_poynting_rows(),
        "cj_owner": cj_owner_rows(),
        "cj_bound": cj_bound_rows(),
        "cj_runner": cj_runner_rows(),
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
