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

DOC = ROOT / "3275-Y5-R2FR-no-compensator-current-and-source-shadow-ban-or-finite-CJ-row-under-AX1090.md"

SRC_3274_DOC = ROOT / "3274-Y5-R2FR-current-normalization-and-EM-stress-source-coupling-derivation-under-AX1090.md"
SRC_3274_GAUGE = OUT / "P8_Y5_R2FR_3274_CURRENT_NORMALIZATION_GAUGE_LOCK_LEMMA.csv"
SRC_3274_CJ_BOUND = OUT / "P8_Y5_R2FR_3274_CJ_CONDITIONAL_BOUND_ROWS_NONCLAIM.csv"
SRC_3274_NEXT = OUT / "P8_Y5_R2FR_3274_NEXT_TARGET.csv"
SRC_642_MD = OUT / "P8_Y5_R10_642_MAXWELL_DESCENT_ATTEMPT.csv"
SRC_765_CEX = OUT / "P8_Y5_R10_765_RESCALING_COUNTEREXAMPLE_LEDGER.csv"
SRC_771_AUDIT = OUT / "P8_Y5_R10_771_THETA_QTAU_CURRENT_OWNER_AUDIT.csv"
SRC_993_GATE = OUT / "P8_Y5_R10_993_CURRENT_EXTRACTION_GATE.csv"
SRC_951_WARD = OUT / "P8_Y5_R10_951_SOURCE_CURRENT_WARD_ACTION_ATTEMPT.csv"
SRC_1030_DOC = ROOT / "1030-Y5-R10-single-public-metric-parent-action-derivation-or-cg-provenance-gate.md"
SRC_1046_DOC = ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md"
SRC_1765_NOETHER = OUT / "P8_Y5_PARENT_QLOC_1765_NOETHER_EXCHANGE_COLLAPSE_THEOREM.csv"
SRC_1765_OWNER = OUT / "P8_Y5_PARENT_QLOC_1765_TOTAL_HILBERT_SOURCE_OWNER_AUDIT.csv"
SRC_2508_PROOF = OUT / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_ONLY_SLOT_PROOF_ATTEMPT.csv"
SRC_2508_GATES = OUT / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_SLOT_THEOREM_GATES.csv"
SRC_2508_COUNTER = OUT / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv"
SRC_2508_RESIDUAL = OUT / "P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv"
SRC_2509_AUDIT = OUT / "P8_Y5_NO_SHADOW_2509_PARENT_CONSTRUCTOR_EXHAUSTION_AUDIT.csv"
SRC_2509_PIVOT = OUT / "P8_Y5_NO_SHADOW_2509_DERIVATION_OR_RESIDUAL_PIVOT_GATE.csv"
SRC_2616_SHADOW = OUT / "P8_Y5_EXCHANGE_GRAPH_GATE_2616_SOURCE_SHADOW_BAN_ATTEMPT.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3275_SOURCE_REGISTER.csv",
    "trichotomy": OUT / "P8_Y5_R2FR_3275_COMPENSATOR_CURRENT_TRICHOTOMY.csv",
    "minimal_theorem": OUT / "P8_Y5_R2FR_3275_MINIMAL_COVARIANT_DERIVATIVE_NO_SHADOW_THEOREM.csv",
    "source_shadow": OUT / "P8_Y5_R2FR_3275_SOURCE_SHADOW_ESCAPE_AUDIT.csv",
    "cj_rows": OUT / "P8_Y5_R2FR_3275_CJ_RESIDUAL_ROWS_NONCLAIM.csv",
    "cj_runner": OUT / "P8_Y5_R2FR_3275_CJ_RESIDUAL_RUNNER_RESULTS_NONCLAIM.csv",
    "promotion": OUT / "P8_Y5_R2FR_3275_PROMOTION_GATES.csv",
    "decision": OUT / "P8_Y5_R2FR_3275_DECISION_LEDGER.csv",
    "next": OUT / "P8_Y5_R2FR_3275_NEXT_TARGET.csv",
    "validation": OUT / "P8_Y5_BRR545_3275_VALIDATION.csv",
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


def conditional_cj_bound() -> float:
    row = read_csv(SRC_3274_CJ_BOUND)[0]
    return float(row["bound_value"])


def source_register() -> list[dict[str, Any]]:
    sources = [
        (SRC_3274_DOC, "3274 weighted-current handoff", ["nabla_mu(kappa_J", "C_J", "compensating"]),
        (SRC_3274_GAUGE, "3274 gauge-current lock lemma", ["GL3274_2", "compensator"]),
        (SRC_3274_CJ_BOUND, "3274 conditional C_J bound", ["CJB3274_0", "bound_value"]),
        (SRC_3274_NEXT, "3274 next target", ["NEXT3274_0_3275", "source-shadow"]),
        (SRC_642_MD, "Maxwell source-current descent shape", ["MD642_1", "source current normalization"]),
        (SRC_765_CEX, "current rescale counterexample", ["RCE765_2", "current_rescale"]),
        (SRC_771_AUDIT, "theta/Q_tau current owner audit", ["TQ771_5", "matter_coupling"]),
        (SRC_993_GATE, "parent current extraction gate", ["CEG993_4", "not_promoted"]),
        (SRC_951_WARD, "Ward action countermodel", ["SWA951_3", "species_weight_countermodel"]),
        (SRC_1030_DOC, "single-public metric/source countermodels", ["CM1030_1", "species_weighted_source"]),
        (SRC_1046_DOC, "no-shadow/source-only weight classification", ["CMA1046_4", "FV1046_6"]),
        (SRC_1765_NOETHER, "Noether exchange block collapse", ["NEC1765_2", "NEC1765_5"]),
        (SRC_1765_OWNER, "total Hilbert source owner audit", ["THO1765_3", "source_shadow"]),
        (SRC_2508_PROOF, "no-source-only slot proof attempt", ["NSP2508_1", "NSP2508_7"]),
        (SRC_2508_GATES, "no-source-slot theorem gates", ["GATE2508_6", "CLAIM_BLOCKED"]),
        (SRC_2508_COUNTER, "source-only countermodels", ["CM2508_0", "CM2508_5"]),
        (SRC_2508_RESIDUAL, "source-weight residual rows", ["RSW2508_1", "epsilon_kappaA_source"]),
        (SRC_2509_AUDIT, "constructor exhaustion audit", ["CEA2509_6", "PIVOT_REQUIRED"]),
        (SRC_2509_PIVOT, "derivation/residual pivot gate", ["PIV2509_2", "residual_route"]),
        (SRC_2616_SHADOW, "source-shadow ban attempt", ["SSB2616_2", "SSB2616_5"]),
    ]
    rows: list[dict[str, Any]] = []
    for idx, (path, role, needles) in enumerate(sources):
        rows.append(
            {
                "source_id": f"SRC3275_{idx}",
                "path": str(path),
                "exists": bool_str(path.exists()),
                "parse_ok": bool_str(parse_ok(path)),
                "role": role,
                "evidence_hits": evidence_hits(path, needles),
                "valid_for_claim": "false",
            }
        )
    return rows


def trichotomy_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "TRI3275_0_start",
            "assumption": "3274 weighted-current law",
            "equation": "nabla_mu(kappa_J J_Q^mu + J_comp^mu)=0",
            "derived_result": "If the parent Noether current obeys nabla_mu J_Q^mu=0, then nabla_mu J_comp^mu = -J_Q^mu nabla_mu kappa_J.",
            "meaning": "A variable kappa_J demands a real compensating divergence unless J_Q.nabla kappa_J vanishes.",
            "status": "EXACT_IDENTITY",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3275_1_exact_improvement",
            "assumption": "J_comp^mu=nabla_nu M^{nu mu} with M antisymmetric and compact/no-boundary-flux support",
            "equation": "nabla_mu J_comp^mu=0 identically",
            "derived_result": "exact improvement currents cannot compensate J_Q.nabla kappa_J; they only modify local stress/Poynting bookkeeping or boundary multipoles.",
            "meaning": "This class is not the dangerous escape for C_J, but it must remain in EM stress residuals if boundary flux is not zero.",
            "status": "PARTIAL_ZERO_FOR_CJ_COMPENSATION",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3275_2_separately_conserved_shadow",
            "assumption": "nabla_mu J_shadow^mu=0 and it enters Maxwell in addition to J_Q",
            "equation": "nabla_mu(kappa_J J_Q^mu + J_shadow^mu)=0",
            "derived_result": "a separately conserved shadow current cannot hide local kappa_J variation, but it can change active EM/source normalization as an independent block.",
            "meaning": "This becomes a finite source-shadow row, not a proof of source universality.",
            "status": "FINITE_SHADOW_BLOCK_RETAINED",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3275_3_nonconserved_compensator",
            "assumption": "J_comp is chosen so nabla_mu J_comp^mu=-J_Q^mu nabla_mu kappa_J",
            "equation": "J_comp carries exactly the mismatch created by variable kappa_J",
            "derived_result": "this is a new active source sector/coupling, not a derived Maxwell-Noether current; it must be parent-owned or bounded.",
            "meaning": "No local-GR/Maxwell source claim can ride on this object silently.",
            "status": "DANGEROUS_ESCAPE_REDUCED_TO_EXPLICIT_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "case_id": "TRI3275_4_no_compensator_corollary",
            "assumption": "J_comp=0 up to exact no-flux improvements, and ordinary currents span enough local directions",
            "equation": "J_Q^mu nabla_mu ln kappa_J=0 for all allowed J_Q",
            "derived_result": "nabla_mu kappa_J=0 locally and therefore C_J=0 under the same generator.",
            "meaning": "This is the clean theorem path; the remaining question is whether MTS parent grammar signs the assumptions.",
            "status": "EXACT_CONDITIONAL_CJ_ZERO_COROLLARY",
            "valid_for_claim": "false",
        },
    ]


def minimal_theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "MCD3275_0_minimal_domain",
            "claim_piece": "minimal covariant derivative source domain",
            "formal_statement": "A_Q enters ordinary charged matter only through D_Q psi=(nabla+i n_A A_Q)psi with fixed representation weights n_A, plus F_Q in the Maxwell kinetic block.",
            "proof_status": "EXACT_IF_PARENT_ACTION_DOMAIN_SIGNED",
            "what_it_kills": "source-shadow A.J terms, kappa_A source-only maps, and compensator currents not generated by the same representation action",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "MCD3275_1_Noether_current_identity",
            "claim_piece": "same current owns dynamics and Maxwell source",
            "formal_statement": "J_Q^mu = delta S_matter/delta A_Q_mu is the Noether current of the same U(1) representation, so gauge Ward identity gives nabla_mu J_Q^mu=0 on matter shell.",
            "proof_status": "STANDARD_VARIATIONAL_IDENTITY_UNDER_MCD3275_0",
            "what_it_kills": "independent source current normalization not tied to matter dynamics",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "MCD3275_2_no_source_shadow",
            "claim_piece": "no separate S_source",
            "formal_statement": "There is no functional S_source[A,J_shadow,kappa_A] used only in the field equation while S_matter controls ordinary dynamics.",
            "proof_status": "CONDITIONAL_OBJECT_LANGUAGE_THEOREM",
            "what_it_kills": "the cleanest source-shadow bypass around gauge-current lock",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "MCD3275_3_current_richness",
            "claim_piece": "current directions test gradient of kappa_J",
            "formal_statement": "For enough allowed local charged matter states, J_Q^mu nabla_mu ln kappa_J=0 for all J_Q implies nabla_mu kappa_J=0.",
            "proof_status": "MATHEMATICALLY_CLEAN_SIDE_CONDITION",
            "what_it_kills": "anisotropic or time/radial hidden kappa_J gradients",
            "valid_for_claim": "false",
        },
        {
            "proof_id": "MCD3275_4_verdict",
            "claim_piece": "C_J zero",
            "formal_statement": "MCD3275_0..3 plus no-flux exact improvements imply C_J=0.",
            "proof_status": "CJ_ZERO_CONDITIONAL_NOT_PARENT_SIGNED",
            "what_it_kills": "source-current normalization slope only if parent minimal domain is signed",
            "valid_for_claim": "false",
        },
    ]


def source_shadow_rows() -> list[dict[str, Any]]:
    return [
        {
            "escape_id": "ESC3275_0_current_rescale",
            "escape_route": "A_Q couples to q_A(X)J_A or kappa_A(X)J_A",
            "why_it_survives_now": "765 and 2508 retain current/source coefficient slots unless parent grammar forbids them.",
            "what_would_kill_it": "minimal covariant derivative source domain plus no Hom into active source coefficients",
            "status": "RETAINED_AS_CJ_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "escape_id": "ESC3275_1_source_shadow_functional",
            "escape_route": "S_source separate from S_matter supplies Maxwell/gravity source current",
            "why_it_survives_now": "2616 says the ban is contract-ready but parent-unsigned; Ward consistency only filters it.",
            "what_would_kill_it": "same variational action owns dynamics and source before readout",
            "status": "RETAINED_AS_CJ_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "escape_id": "ESC3275_2_exact_improvement",
            "escape_route": "J_comp=nabla_nu M^{nu mu}",
            "why_it_survives_now": "exact improvements can be legal boundary/local stress terms; they do not compensate variable kappa_J if divergence-free.",
            "what_would_kill_it": "compact no-boundary-flux theorem for the EM/source arena",
            "status": "CJ_SAFE_IF_NO_FLUX_ELSE_STRESS_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "escape_id": "ESC3275_3_nonHilbert_label_current",
            "escape_route": "label-carrying non-Hilbert ordinary source current",
            "why_it_survives_now": "1030/2508/2616 retain non-Hilbert and marker/source-map channels.",
            "what_would_kill_it": "no non-Hilbert label current theorem or finite source-backed coefficient",
            "status": "RETAINED_AS_CJ_RESIDUAL",
            "valid_for_claim": "false",
        },
        {
            "escape_id": "ESC3275_4_readout_reentry",
            "escape_route": "post-variation readout/projector/EFT map reintroduces source coefficient",
            "why_it_survives_now": "2508 and 2509 keep readout commutator/general effective-action reentry open.",
            "what_would_kill_it": "readout variation commutator zero theorem or source-backed residual row",
            "status": "RETAINED_AS_CJ_RESIDUAL",
            "valid_for_claim": "false",
        },
    ]


def cj_residual_rows() -> list[dict[str, Any]]:
    bound = conditional_cj_bound()
    return [
        {
            "row_id": "CJR3275_0_theorem_zero_if_minimal_domain_signed",
            "coefficient": "C_J=L_X ln kappa_J",
            "prediction_value": "0",
            "required_side_conditions": "minimal covariant derivative domain; no source-shadow; no nonconserved compensator; exact improvements no-flux; current richness; C_Z=C_R=0 for alpha-derived bound",
            "bound_value": fmt(bound),
            "status": "THEOREM_ZERO_CONDITIONAL_NONCLAIM",
            "source_path": str(OUTPUTS["minimal_theorem"]),
            "valid_for_claim": "false",
        },
        {
            "row_id": "CJR3275_1_missing_live_CJ",
            "coefficient": "C_J=L_X ln kappa_J",
            "prediction_value": "MISSING_PARENT_CJ_OR_ZERO_THEOREM",
            "required_side_conditions": "real parent coefficient or signed theorem-zero",
            "bound_value": fmt(bound),
            "status": "REFUSE_MISSING",
            "source_path": str(OUTPUTS["source_shadow"]),
            "valid_for_claim": "false",
        },
        {
            "row_id": "CJR3275_2_source_shadow_symbolic",
            "coefficient": "C_J_shadow",
            "prediction_value": "MISSING_NUMERIC_SOURCE_SHADOW_COEFFICIENT",
            "required_side_conditions": "source-shadow functional coefficient, projection to kappa_J, units, source path",
            "bound_value": fmt(bound),
            "status": "FINITE_ROW_SCHEMA_ONLY",
            "source_path": str(SRC_2508_RESIDUAL),
            "valid_for_claim": "false",
        },
        {
            "row_id": "CJR3275_3_exact_improvement_no_flux",
            "coefficient": "C_J_improvement",
            "prediction_value": "0",
            "required_side_conditions": "J_comp=nabla M exact, compact/no-boundary-flux support, no monopole/source normalization shift",
            "bound_value": fmt(bound),
            "status": "IMPROVEMENT_ZERO_CONDITIONAL_NONCLAIM",
            "source_path": str(OUTPUTS["trichotomy"]),
            "valid_for_claim": "false",
        },
        {
            "row_id": "CJR3275_4_half_bound_smoke",
            "coefficient": "C_J",
            "prediction_value": fmt(0.5 * bound),
            "required_side_conditions": "smoke numeric only; C_Z=C_R=0",
            "bound_value": fmt(bound),
            "status": "SMOKE_NUMERIC_NONCLAIM",
            "source_path": "SMOKE",
            "valid_for_claim": "false",
        },
        {
            "row_id": "CJR3275_5_twice_bound_smoke",
            "coefficient": "C_J",
            "prediction_value": fmt(2.0 * bound),
            "required_side_conditions": "smoke numeric only; C_Z=C_R=0",
            "bound_value": fmt(bound),
            "status": "SMOKE_NUMERIC_NONCLAIM",
            "source_path": "SMOKE",
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
        "CJR3275_0_theorem_zero_if_minimal_domain_signed": "PASS_NUMERIC_NONCLAIM",
        "CJR3275_1_missing_live_CJ": "REFUSE_OR_FAIL",
        "CJR3275_2_source_shadow_symbolic": "REFUSE_OR_FAIL",
        "CJR3275_3_exact_improvement_no_flux": "PASS_NUMERIC_NONCLAIM",
        "CJR3275_4_half_bound_smoke": "PASS_NUMERIC_NONCLAIM",
        "CJR3275_5_twice_bound_smoke": "FAIL_BOUND",
    }
    bound = conditional_cj_bound()
    rows: list[dict[str, Any]] = []
    for source in cj_residual_rows():
        value = numeric_or_none(source["prediction_value"])
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
                "case_id": f"RUN3275_{source['row_id']}",
                "row_id": source["row_id"],
                "prediction_value": source["prediction_value"],
                "bound_value": fmt(bound),
                "abs_prediction": abs_value,
                "prediction_over_bound": ratio,
                "pass_bound": bool_str(pass_bound),
                "result": result,
                "expected": expected[source["row_id"]],
                "expectation_met": bool_str(result == expected[source["row_id"]]),
                "valid_for_claim": "false",
            }
        )
    return rows


def promotion_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3275_0_compensator_trichotomy",
            "gate": "compensator classes are separated",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "exact improvement cannot hide variable kappa_J; nonconserved compensator is an explicit new source sector.",
        },
        {
            "gate_id": "GATE3275_1_minimal_domain_theorem",
            "gate": "minimal covariant derivative theorem stated",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "would kill source-shadow if parent action domain is signed.",
        },
        {
            "gate_id": "GATE3275_2_parent_signature",
            "gate": "no source-shadow/no compensator parent-signed",
            "passed": "false",
            "claim_allowed": "false",
            "detail": "constructor exhaustion and same-source-owner grammar remain unsigned in current corpus.",
        },
        {
            "gate_id": "GATE3275_3_finite_rows_ready",
            "gate": "finite C_J/source-shadow rows exist and runner refuses missing values",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner_rows())),
            "claim_allowed": "false",
            "detail": "runner distinguishes theorem-zero smoke, exact-improvement smoke, missing source-shadow, and over-bound values.",
        },
        {
            "gate_id": "GATE3275_4_no_local_GR_claim",
            "gate": "no local-GR/Newton/Maxwell pass promoted",
            "passed": "true",
            "claim_allowed": "false",
            "detail": "3275 reduces the escape hatch to explicit residuals; it does not close local GR.",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3275_0_real_gain",
            "decision": "The compensator loophole is now classified, not merely named.",
            "why_it_moves_forward": "Exact improvements are CJ-safe under no-flux; only real source-shadow/nonconserved compensators can hide variable kappa_J.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3275_1_best_theorem_route",
            "decision": "Minimal covariant derivative domain is the clean route to C_J=0.",
            "why_it_moves_forward": "If A_Q appears only inside D_Q with fixed representation weights, the same Noether current owns dynamics and source.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3275_2_current_status",
            "decision": "Current MTS does not yet parent-sign the no-source-shadow grammar.",
            "why_it_moves_forward": "The remaining proof debt is constructor exhaustion/single-source-owner, not an amorphous coupling gap.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "decision_id": "DEC3275_3_next_target",
            "decision": "Attack minimal covariant derivative domain or pivot to finite source-shadow coefficient acquisition.",
            "why_it_moves_forward": "This either closes C_J at parent level or produces the first actual numeric/source-backed C_J residual row.",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT3275_0_3276",
            "target_doc": "3276-Y5-R2FR-minimal-covariant-derivative-domain-or-first-source-shadow-coefficient-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3276_minimal_covariant_derivative_domain_or_first_source_shadow_coefficient.py",
            "objective": "Try to derive the parent action domain where A_Q enters charged matter only through D_Q with fixed representation weights; if this cannot be signed, acquire or stage the first source-backed finite source-shadow/C_J coefficient row.",
            "guardrail": "Do not repeat generic no-source-slot proofs unless a new parent constructor primitive is supplied; either sign the minimal A_Q domain or fill a finite residual row.",
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
            "check_id": "VAL3275_0_sources_exist",
            "check": "all cited source paths exist",
            "passed": bool_str(all(row["exists"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["exists"] != "true"),
        },
        {
            "check_id": "VAL3275_1_sources_parse",
            "check": "all cited source paths parse",
            "passed": bool_str(all(row["parse_ok"] == "true" for row in sources)),
            "detail": ";".join(row["source_id"] for row in sources if row["parse_ok"] != "true"),
        },
        {
            "check_id": "VAL3275_2_outputs_parse",
            "check": "all 3275 output CSVs parse",
            "passed": bool_str(output_csvs_parse()),
            "detail": "non-validation outputs parsed before validation write",
        },
        {
            "check_id": "VAL3275_3_trichotomy_present",
            "check": "compensator trichotomy includes exact improvement and nonconserved compensator cases",
            "passed": bool_str(any(row["case_id"] == "TRI3275_1_exact_improvement" for row in trichotomy_rows()) and any(row["case_id"] == "TRI3275_3_nonconserved_compensator" for row in trichotomy_rows())),
            "detail": "TRI3275_1 and TRI3275_3 present",
        },
        {
            "check_id": "VAL3275_4_minimal_theorem_nonclaim",
            "check": "minimal covariant derivative theorem remains conditional",
            "passed": bool_str(minimal_theorem_rows()[-1]["proof_status"] == "CJ_ZERO_CONDITIONAL_NOT_PARENT_SIGNED"),
            "detail": minimal_theorem_rows()[-1]["proof_status"],
        },
        {
            "check_id": "VAL3275_5_runner_expectations",
            "check": "C_J/source-shadow runner expectations all match",
            "passed": bool_str(all(row["expectation_met"] == "true" for row in runner)),
            "detail": ";".join(f"{row['row_id']}={row['result']}" for row in runner),
        },
        {
            "check_id": "VAL3275_6_claim_gates_false",
            "check": "no 3275 gate allows local-GR/WEP/Maxwell claim",
            "passed": bool_str(all(row["claim_allowed"] == "false" for row in gates)),
            "detail": "all claim_allowed=false",
        },
        {
            "check_id": "VAL3275_7_formalization_untouched",
            "check": "formalization-workbench modified-file count remains zero by this script",
            "passed": bool_str(formalization_changed_count() == 0),
            "detail": f"formalization_changed_count={formalization_changed_count()}",
        },
        {
            "check_id": "VAL3275_8_overall",
            "check": "3275 validation overall",
            "passed": "PENDING",
            "detail": "computed after rows are assembled",
        },
    ]
    overall = all(row["passed"] == "true" for row in validations if row["check_id"] != "VAL3275_8_overall")
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
    trichotomy = read_csv(OUTPUTS["trichotomy"])
    theorem = read_csv(OUTPUTS["minimal_theorem"])
    shadow = read_csv(OUTPUTS["source_shadow"])
    cj_rows = read_csv(OUTPUTS["cj_rows"])
    runner = read_csv(OUTPUTS["cj_runner"])
    gates = read_csv(OUTPUTS["promotion"])
    decisions = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next"])
    validations = read_csv(OUTPUTS["validation"])
    content = f"""# 3275 - No-compensator current and source-shadow ban or finite C_J row under AX1090

## Summary

3275 classifies the escape hatch left by 3274. Starting from

`nabla_mu(kappa_J J_Q^mu + J_comp^mu)=0`,

and assuming the parent Noether current has `nabla_mu J_Q^mu=0`, one obtains

`nabla_mu J_comp^mu = -J_Q^mu nabla_mu kappa_J`.

That gives a useful trichotomy. Exact improvement currents are divergence-free and cannot hide variable `kappa_J`; separately conserved shadow blocks are independent source sectors; only a nonconserved compensator can cancel `J_Q · grad(kappa_J)`, and that object is a new active source coupling, not a derived Maxwell/GR source law. Therefore the clean theorem route is now precise: prove that `A_Q` enters ordinary matter only through the minimal covariant derivative `D_Q` with fixed representation weights and no separate `S_source`.

## Compensator Trichotomy
{md_table(trichotomy, ["case_id", "equation", "derived_result", "status"])}

## Minimal Covariant Derivative Theorem
{md_table(theorem, ["proof_id", "claim_piece", "proof_status", "what_it_kills"])}

## Source-Shadow Escape Audit
{md_table(shadow, ["escape_id", "escape_route", "status", "what_would_kill_it"])}

## C_J Residual Rows
{md_table(cj_rows, ["row_id", "coefficient", "prediction_value", "bound_value", "status", "valid_for_claim"])}

## C_J Runner
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
        "trichotomy": trichotomy_rows(),
        "minimal_theorem": minimal_theorem_rows(),
        "source_shadow": source_shadow_rows(),
        "cj_rows": cj_residual_rows(),
        "cj_runner": runner_rows(),
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
