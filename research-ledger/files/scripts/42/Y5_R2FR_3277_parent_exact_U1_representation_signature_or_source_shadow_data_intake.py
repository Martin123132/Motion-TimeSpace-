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

DOC = ROOT / "3277-Y5-R2FR-parent-exact-U1-representation-signature-or-source-shadow-data-intake-under-AX1090.md"

SRC_3276_DOC = ROOT / "3276-Y5-R2FR-minimal-covariant-derivative-domain-or-first-source-shadow-coefficient-under-AX1090.md"
SRC_3276_SPLIT = OUT / "P8_Y5_R2FR_3276_AQ_DOMAIN_SPLIT_THEOREM.csv"
SRC_3276_MAG = OUT / "P8_Y5_R2FR_3276_F_ONLY_MAGNETIZATION_CURRENT_LEMMA.csv"
SRC_3276_GAUGE = OUT / "P8_Y5_R2FR_3276_NONCONSERVED_COMPENSATOR_GAUGE_REJECTION.csv"
SRC_3276_SHADOW = OUT / "P8_Y5_R2FR_3276_SOURCE_SHADOW_COEFFICIENT_ROWS_NONCLAIM.csv"
SRC_3276_NEXT = OUT / "P8_Y5_R2FR_3276_NEXT_TARGET.csv"
SRC_3275_MCD = OUT / "P8_Y5_R2FR_3275_MINIMAL_COVARIANT_DERIVATIVE_NO_SHADOW_THEOREM.csv"
SRC_642_MD = OUT / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv"
SRC_642_TA = OUT / "P8_Y5_R10_642_THEOREM_ZERO_ATTEMPT.csv"
SRC_765_CEX = OUT / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
SRC_1814_VISIBLE = OUT / "P8_Y5_PARENT_QLOC_1814_VISIBLE_CONNECTION_CURRENT_OWNER_THEOREM.csv"
SRC_1814_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1814_CURRENT_OWNER_AUDIT.csv"
SRC_1815_NO_RESCALE = OUT / "P8_Y5_PARENT_QLOC_1815_NO_CURRENT_RESCALE_THEOREM.csv"
SRC_2508_PROOF = OUT / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv"
SRC_2508_COUNTER = OUT / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv"
SRC_2509_PIVOT = OUT / "P8_Y5_NO_SHADOW_2509_DERIVATION_OR_RESIDUAL_PIVOT_GATE.csv"
SRC_2616_SHADOW = OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv"
SRC_951_WARD = OUT / "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv"
SRC_1889_WARD = OUT / "P8_Y5_PARENT_QLOC_1889_SOURCE_CURRENT_WARD_OWNER_ATTEMPT.csv"
SRC_1920_PROOF = OUT / "P8_Y5_PARENT_QLOC_1920_SOURCE_WEIGHT_PARENT_CURRENT_PROOF_ATTEMPT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3277_SOURCE_REGISTER.csv",
    "signature": OUT / "P8_Y5_R2FR_3277_EXACT_U1_PARENT_SIGNATURE_AUDIT.csv",
    "theorem": OUT / "P8_Y5_R2FR_3277_REPRESENTATION_CURRENT_THEOREM.csv",
    "shadow_intake": OUT / "P8_Y5_R2FR_3277_SOURCE_SHADOW_DATA_INTAKE_SCHEMA.csv",
    "shadow_rows": OUT / "P8_Y5_R2FR_3277_SOURCE_SHADOW_INTAKE_ROWS_NONCLAIM.csv",
    "runner": OUT / "P8_Y5_R2FR_3277_SOURCE_SHADOW_BOUND_RUNNER_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3277_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3277_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3277_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3277_VALIDATION.csv",
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
    return float(read_csv(SRC_3276_SHADOW)[0]["bound_value"])


def source_register() -> list[dict[str, Any]]:
    sources = [
        (SRC_3276_DOC, "3276 handoff", ["A_Q-domain split", "source-shadow", "U(1)"]),
        (SRC_3276_SPLIT, "A_Q domain split", ["ADS3276_0", "ADS3276_3"]),
        (SRC_3276_MAG, "F-only magnetization lemma", ["MAG3276_1", "identically conserved"]),
        (SRC_3276_GAUGE, "nonconserved compensator rejection", ["GJR3276_2", "REJECT_SILENT"]),
        (SRC_3276_SHADOW, "3276 source-shadow rows", ["SSR3276_1", "bound_value"]),
        (SRC_3276_NEXT, "3276 next target", ["NEXT3276_0_3277", "exact U1"]),
        (SRC_3275_MCD, "minimal covariant derivative theorem", ["MCD3275_0", "MCD3275_4"]),
        (SRC_642_MD, "Maxwell descent", ["MD642_0", "MD642_2"]),
        (SRC_642_TA, "parent U1 theorem attempt", ["TA642_0", "TA642_1"]),
        (SRC_765_CEX, "rescaling counterexamples", ["RCE765_1", "RCE765_2"]),
        (SRC_1814_VISIBLE, "visible connection/current owner theorem", ["VCC1814_0", "VCC1814_4"]),
        (SRC_1814_AUDIT, "current owner audit", ["COA1814_0", "COA1814_4"]),
        (SRC_1815_NO_RESCALE, "no current rescale theorem", ["NCR1815_0", "NCR1815_4"]),
        (SRC_2508_PROOF, "no-source-only slot attempt", ["NSP2508_0", "NSP2508_7"]),
        (SRC_2508_COUNTER, "source-only countermodels", ["CM2508_0", "CM2508_5"]),
        (SRC_2509_PIVOT, "constructor exhaustion pivot", ["PIV2509_2", "residual_route"]),
        (SRC_2616_SHADOW, "source-shadow ban attempt", ["SSB2616_0", "SSB2616_5"]),
        (SRC_951_WARD, "Ward source-current limits", ["SWA951_2", "SWA951_5"]),
        (SRC_1889_WARD, "source-current Ward owner attempt", ["SWO1889_3", "SWO1889_7"]),
        (SRC_1920_PROOF, "source-weight parent-current proof attempt", ["SWP1920_0", "SWP1920_5"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3277_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def signature_rows() -> list[dict[str, Any]]:
    return [
        {
            "sig_id": "U1SIG3277_0_parent_connection",
            "required_signature": "A_Q is the T_Q projection of a parent U(1) connection before readout.",
            "mathematical_form": "A_parent=A_Q T_Q + A_perp, with F_Q=dA_Q and dF_Q=0",
            "current_evidence": "642 gives the U1/connection shape, 765/1814 keep projection/current owner unsigned.",
            "status": "PARTIAL_SHAPE_NOT_PARENT_SIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "sig_id": "U1SIG3277_1_fixed_generator_lattice",
            "required_signature": "T_Q has fixed compact lattice/normalization and matter representation weights n_A are fixed parent data.",
            "mathematical_form": "exp(2*pi*T_Q)=1; D_X n_A=0; no T_Q rescale compensated by current labels",
            "current_evidence": "642 has integer charge-label support; 765 retains generator/current rescale counterexamples.",
            "status": "UNSIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "sig_id": "U1SIG3277_2_associated_matter_domain",
            "required_signature": "charged matter is an associated-bundle representation and A_Q enters ordinary dynamics through D_Q only, aside from F-only response terms.",
            "mathematical_form": "S_matter[psi,D_Q psi,F_Q,g_obs,theta_fixed], no independent A_Q.J_shadow source functional",
            "current_evidence": "3276 splits the domain and proves F-only current conservation; 2508/2616 say no S_source/no-shadow grammar is not parent-signed.",
            "status": "DOMAIN_SPLIT_DERIVED_PARENT_SIGNATURE_UNSIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "sig_id": "U1SIG3277_3_exact_gauge_invariance",
            "required_signature": "off-shell U(1) gauge invariance holds for arbitrary local lambda before readout.",
            "mathematical_form": "delta_lambda S_parent=0; any A_Q.J term requires nabla_mu J^mu=0 or a real charged-sector Ward identity",
            "current_evidence": "3276 rejects nonconserved silent compensator by exact U1; current corpus has not signed full parent U1 action.",
            "status": "MATHEMATICALLY_DERIVED_PARENT_ACTION_UNSIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "sig_id": "U1SIG3277_4_readout_transfer",
            "required_signature": "source/test/readout maps use the same parent current after variation, with no c_A/kappa_A reentry.",
            "mathematical_form": "J_readout=P_read[J_Q] with P_read coefficient-free or source-backed; no J_A -> c_A J_A parent slot",
            "current_evidence": "1815 demotes post-variation c_A conditionally, but readout order/source-shadow exclusions remain unsigned.",
            "status": "UNSIGNED_REENTRY_RETAINED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
        {
            "sig_id": "U1SIG3277_5_verdict",
            "required_signature": "U1SIG3277_0 through U1SIG3277_4 all pass in one parent action branch.",
            "mathematical_form": "then C_J=0 up to F-only no-flux stress residuals and finite separately conserved source-shadow blocks",
            "current_evidence": "signature chain is exact as a theorem target but not current proof.",
            "status": "EXACT_U1_REPRESENTATION_SIGNATURE_NOT_PARENT_SIGNED",
            "blocks_CJ_zero": "true",
            "valid_for_claim": "false",
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "REP3277_0_statement",
            "claim_piece": "representation current theorem",
            "formal_statement": "If charged matter is a parent associated-bundle representation with fixed weights n_A and A_Q enters through D_Q plus F-only terms, then the A_Q source current is J_Q=delta S_matter/delta A_Q and is the U(1) Noether current.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "consequence": "independent current normalization is not available inside the parent action domain",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "REP3277_1_nonconserved_shadow",
            "claim_piece": "nonconserved source-shadow exclusion",
            "formal_statement": "A bare A_Q_mu J_comp^mu with nabla_mu J_comp^mu != 0 violates exact U(1) for arbitrary lambda unless J_comp is generated by real charged fields and their Euler equations.",
            "proof_status": "DERIVED_GAUGE_REJECTION",
            "consequence": "silent compensation for variable kappa_J is rejected",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "REP3277_2_conserved_shadow",
            "claim_piece": "separately conserved shadow block",
            "formal_statement": "A separately conserved J_shadow may be gauge-safe, but it is an independent source sector or readout block; it cannot be used as a proof that C_J=0.",
            "proof_status": "FINITE_RESIDUAL_BRANCH",
            "consequence": "shadow blocks require numeric/source-backed intake or parent no-shadow proof",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "REP3277_3_CJ_zero",
            "claim_piece": "current-normalization zero",
            "formal_statement": "If the parent exact-U1 representation signature is signed, no separate S_source exists, current-richness holds, and F-only improvements have no flux/source-normalization leakage, then C_J=0.",
            "proof_status": "CONDITIONAL_CJ_ZERO_NOT_PROMOTED",
            "consequence": "the source-coupling route is precise but not claimable in current corpus",
            "valid_for_claim": "false",
        },
        {
            "theorem_id": "REP3277_4_fallback",
            "claim_piece": "finite source-shadow intake",
            "formal_statement": "If exact U1/domain ownership remains unsigned, score epsilon_shadow, c_A, pre-action w_A, readout reentry, and magnetization boundary leakage as explicit nonclaim rows.",
            "proof_status": "DATA_INTAKE_ROUTE_BUILT",
            "consequence": "stops theorem-looping and opens empirical/source-backed residual branch",
            "valid_for_claim": "false",
        },
    ]


def intake_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "field_id": "INT3277_0_source_id",
            "field": "source_id/source_path",
            "meaning": "local file or source proving theorem-zero or numeric finite coefficient",
            "required": "true",
        },
        {
            "field_id": "INT3277_1_current_type",
            "field": "current_type",
            "meaning": "minimal_Noether, conserved_shadow, pre_action_weight, readout_reentry, magnetization_boundary, nonconserved_forbidden",
            "required": "true",
        },
        {
            "field_id": "INT3277_2_conservation_certificate",
            "field": "conservation_certificate",
            "meaning": "nabla_mu J^mu=0 proof, real charged-sector Ward identity, no-flux theorem, or explicit failure",
            "required": "true",
        },
        {
            "field_id": "INT3277_3_projection_to_CJ",
            "field": "projection_to_CJ",
            "meaning": "map from residual current/source block to C_J_effective under 3276 side conditions",
            "required": "true",
        },
        {
            "field_id": "INT3277_4_numeric_value",
            "field": "numeric_value",
            "meaning": "dimensionless coefficient or MISSING; must not be inferred from fitted success",
            "required": "true",
        },
        {
            "field_id": "INT3277_5_claim_flags",
            "field": "valid_for_claim",
            "meaning": "false unless source path, units, projection, conservation, and bound comparison are all real",
            "required": "true",
        },
    ]


def shadow_intake_rows() -> list[dict[str, Any]]:
    bound = cj_bound()
    return [
        {
            "row_id": "SSI3277_0_exact_U1_zero_conditional",
            "current_type": "minimal_Noether",
            "coefficient": "C_J_effective",
            "numeric_value": "0",
            "units": "dimensionless local logarithmic coefficient",
            "conservation_certificate": "exact if U1SIG3277_0..4 parent-signed",
            "projection_to_CJ": "identity",
            "bound_value": fmt(bound),
            "status": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3277_1_conserved_shadow_missing",
            "current_type": "conserved_shadow",
            "coefficient": "epsilon_shadow",
            "numeric_value": "MISSING_SOURCE_BACKED_CONSERVED_SHADOW",
            "units": "dimensionless relative source-current coefficient",
            "conservation_certificate": "MISSING",
            "projection_to_CJ": "MISSING_SHADOW_TO_CJ_PROJECTION",
            "bound_value": fmt(bound),
            "status": "INTAKE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3277_2_current_rescale_missing",
            "current_type": "current_rescale",
            "coefficient": "c_A_or_kappa_A",
            "numeric_value": "MISSING_CURRENT_RESCALE_COEFFICIENT",
            "units": "dimensionless relative current normalization",
            "conservation_certificate": "current may be conserved but normalization is independent",
            "projection_to_CJ": "MISSING_C_A_TO_CJ_MAP",
            "bound_value": fmt(bound),
            "status": "INTAKE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3277_3_pre_action_weight_missing",
            "current_type": "pre_action_weight",
            "coefficient": "w_A",
            "numeric_value": "MISSING_PRE_ACTION_WEIGHT",
            "units": "dimensionless action/source weight",
            "conservation_certificate": "weighted current can conserve but is parent-domain debt",
            "projection_to_CJ": "MISSING_WA_TO_CJ_MAP",
            "bound_value": fmt(bound),
            "status": "INTAKE_REQUIRED",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3277_4_magnetization_no_flux_zero",
            "current_type": "magnetization_boundary",
            "coefficient": "epsilon_mag_boundary",
            "numeric_value": "0",
            "units": "dimensionless current-normalization leakage",
            "conservation_certificate": "F-only current identically conserved plus compact no-flux support",
            "projection_to_CJ": "zero under no-flux side condition",
            "bound_value": fmt(bound),
            "status": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3277_5_nonconserved_forbidden",
            "current_type": "nonconserved_forbidden",
            "coefficient": "J_comp_nonconserved",
            "numeric_value": "FORBIDDEN_BY_EXACT_U1_UNLESS_REAL_CHARGED_SECTOR",
            "units": "not numeric",
            "conservation_certificate": "fails exact U1 if silent",
            "projection_to_CJ": "route to SSI3277_1 if real sector",
            "bound_value": fmt(bound),
            "status": "REFUSE_SILENT_COMPENSATOR",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3277_6_half_bound_smoke",
            "current_type": "smoke",
            "coefficient": "C_J_effective",
            "numeric_value": fmt(0.5 * bound),
            "units": "dimensionless local logarithmic coefficient",
            "conservation_certificate": "SMOKE_NUMERIC_NONCLAIM",
            "projection_to_CJ": "identity",
            "bound_value": fmt(bound),
            "status": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "SSI3277_7_twice_bound_smoke",
            "current_type": "smoke",
            "coefficient": "C_J_effective",
            "numeric_value": fmt(2.0 * bound),
            "units": "dimensionless local logarithmic coefficient",
            "conservation_certificate": "SMOKE_NUMERIC_NONCLAIM",
            "projection_to_CJ": "identity",
            "bound_value": fmt(bound),
            "status": "SMOKE",
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
        "SSI3277_0_exact_U1_zero_conditional": "PASS_NUMERIC_NONCLAIM",
        "SSI3277_1_conserved_shadow_missing": "REFUSE_OR_FAIL",
        "SSI3277_2_current_rescale_missing": "REFUSE_OR_FAIL",
        "SSI3277_3_pre_action_weight_missing": "REFUSE_OR_FAIL",
        "SSI3277_4_magnetization_no_flux_zero": "PASS_NUMERIC_NONCLAIM",
        "SSI3277_5_nonconserved_forbidden": "REFUSE_OR_FAIL",
        "SSI3277_6_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "SSI3277_7_twice_bound_smoke": "FAIL_BOUND",
    }
    bound = cj_bound()
    rows: list[dict[str, Any]] = []
    for row in shadow_intake_rows():
        value = numeric_or_none(row["numeric_value"])
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
                "case_id": f"RUN3277_{row['row_id']}",
                "row_id": row["row_id"],
                "current_type": row["current_type"],
                "numeric_value": row["numeric_value"],
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
            "gate_id": "GATE3277_0_exact_U1_theorem",
            "gate": "exact-U1 representation theorem stated",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "the theorem is exact conditionally but parent signature remains unsigned.",
        },
        {
            "gate_id": "GATE3277_1_parent_signature",
            "gate": "parent connection/lattice/matter-domain/readout signatures all pass",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "A_Q projection, fixed lattice/current owner, no S_source, and readout transfer remain unsigned.",
        },
        {
            "gate_id": "GATE3277_2_silent_compensator_closed",
            "gate": "nonconserved silent source-shadow rejected by exact U1",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "if it exists as a real sector, it must enter finite source-shadow intake.",
        },
        {
            "gate_id": "GATE3277_3_data_intake_built",
            "gate": "finite source-shadow data-intake schema and runner built",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner_rows())),
            "claim_allowed": "false",
            "detail": "missing live coefficients are refused; theorem-smoke and numeric-smoke gates behave correctly.",
        },
        {
            "gate_id": "GATE3277_4_no_local_claim",
            "gate": "no local-GR/Newton/Maxwell pass promoted",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3277 is a source-domain theorem/data-interface checkpoint.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3277_0_exact_route",
            "decision": "Exact parent U(1) would close the dangerous current-normalization route.",
            "why_it_moves_forward": "if A_Q is parent-owned and matter is a fixed representation, J_Q is the Noether current and nonconserved compensators are forbidden.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3277_1_current_status",
            "decision": "Current corpus has the theorem shape but not the parent signature.",
            "why_it_moves_forward": "we now know the exact clauses: connection projection, fixed lattice, associated matter domain, exact U1, and readout transfer.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3277_2_fallback",
            "decision": "The fallback is now finite source-shadow data intake, not another generic no-source-slot loop.",
            "why_it_moves_forward": "conserved shadow, current rescale, pre-action weight, readout reentry, and magnetization boundary leakage have separate rows.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3277_3_next",
            "decision": "Next should acquire/source finite rows or sign one exact-U1 clause from parent text.",
            "why_it_moves_forward": "this prevents wasting tokens on repeating the same theorem-contract without new evidence.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3277_0_3278",
            "target_doc": "3278-Y5-R2FR-source-shadow-finite-row-acquisition-or-parent-U1-clause-source-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3278_source_shadow_finite_row_acquisition_or_parent_U1_clause_source.py",
            "objective": "Use the 3277 intake schema to either source one exact parent-U1 clause from the corpus, or fill the first finite source-shadow/current-rescale/pre-action-weight/readout coefficient row with real provenance.",
            "guardrail": "Do not repeat no-source-slot/minimality arguments unless a new parent source is cited; choose one clause or one finite row and make it source-backed or explicitly blocked.",
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
    signature = signature_rows()
    runner = runner_rows()
    gates = promotion_gate_rows()
    validations = [
        {
            "check_id": "VAL3277_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3277_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3277_2_outputs_parse",
            "check": "all 3277 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3277_3_signature_not_falsely_signed",
            "check": "exact U1 parent signature remains nonclaim",
            "passed": bool_str(signature[-1]["status"] == "EXACT_U1_REPRESENTATION_SIGNATURE_NOT_PARENT_SIGNED"),
            "detail": signature[-1]["status"],
        },
        {
            "check_id": "VAL3277_4_intake_rows_nonclaim",
            "check": "all source-shadow intake rows remain nonclaim",
            "passed": bool_str(all(row["valid_for_claim"] == "false" for row in shadow_intake_rows())),
            "detail": "",
        },
        {
            "check_id": "VAL3277_5_runner_expectations",
            "check": "source-shadow runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3277_6_claim_gates_false",
            "check": "no 3277 gate allows local-GR/WEP/Maxwell claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3277_7_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3277_8_overall",
            "check": "3277 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3277_8_overall")
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
    signature = read_csv(OUTPUTS["signature"])
    theorem = read_csv(OUTPUTS["theorem"])
    schema = read_csv(OUTPUTS["shadow_intake"])
    rows = read_csv(OUTPUTS["shadow_rows"])
    runner = read_csv(OUTPUTS["runner"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3277 - Parent exact-U1 representation signature or source-shadow data intake under AX1090

## Summary

3277 tests the clean source-coupling route: exact parent U(1) representation ownership. If `A_Q` is a parent connection, `T_Q` has fixed lattice normalization, charged matter is an associated representation with fixed weights, and source/readout maps use the current after variation, then `J_Q=delta S_matter/delta A_Q` is the Noether current and `C_J=0` follows under the 3276 side conditions.

Current MTS does not yet sign all those clauses. The useful fallback is therefore finite data intake, not another no-source-slot loop: conserved source-shadow blocks, current rescalings, pre-action weights, readout reentry, and magnetization boundary leakage are separated as rows.

## Exact U1 Parent Signature Audit
{md_table(signature, ["sig_id", "required_signature", "status", "blocks_CJ_zero"])}

## Representation Current Theorem
{md_table(theorem, ["theorem_id", "claim_piece", "proof_status", "consequence"])}

## Source-Shadow Intake Schema
{md_table(schema, ["field_id", "field", "meaning", "required"])}

## Source-Shadow Intake Rows
{md_table(rows, ["row_id", "current_type", "coefficient", "numeric_value", "status", "valid_for_claim"])}

## Bound Runner
{md_table(runner, ["row_id", "current_type", "numeric_value", "prediction_over_bound", "result", "expectation_met", "valid_for_claim"])}

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
        "signature": signature_rows(),
        "theorem": theorem_rows(),
        "shadow_intake": intake_schema_rows(),
        "shadow_rows": shadow_intake_rows(),
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
