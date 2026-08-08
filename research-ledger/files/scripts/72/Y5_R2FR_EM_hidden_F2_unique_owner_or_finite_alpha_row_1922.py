from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
SOURCE_WEIGHT_DOCS = ROOT / "source-intake" / "source-weight" / "docs"
MICROSCOPE_COEFFS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "coefficients"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1922"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1922-Y5-R2FR-EM-hidden-F2-unique-owner-or-finite-alpha-row.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1921_next": OUT / "P8_Y5_PARENT_QLOC_1921_NEXT_TARGET.csv",
    "1921_doc": ROOT / "1921-Y5-R2FR-constant-sector-superselection-or-alpha-mass-clock-first-rows.md",
    "1915_priority": OUT / "P8_Y5_PARENT_QLOC_1915_RESIDUAL_PRIORITY_MATRIX_NONCLAIM.csv",
    "1914_vector": OUT / "P8_Y5_PARENT_QLOC_1914_FINITE_RESIDUAL_VECTOR_V0_NONCLAIM.csv",
    "988_em_lock": OUT / "P8_Y5_R10_988_EM_LOCK_THEOREM_GATE.csv",
    "989_em_audit": OUT / "P8_Y5_R10_989_EM_LOCK_SIGNATURE_AUDIT.csv",
    "989_validation": OUT / "P8_Y5_BRR545_989_VALIDATION.csv",
    "1048_f2_attempt": OUT / "P8_Y5_R10_1048_NO_EXTRA_F2_THEOREM_ATTEMPT.csv",
    "1048_vertex_audit": OUT / "P8_Y5_R10_1048_PARENT_VERTEX_SIGNATURE_AUDIT.csv",
    "1048_claims": OUT / "P8_Y5_R10_1048_CLAIM_GATES.csv",
    "1099_doc": ROOT / "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md",
    "1099_claims": OUT / "P8_Y5_R10_1099_CLAIM_GATES.csv",
    "1099_validation": OUT / "P8_Y5_BRR545_1099_VALIDATION.csv",
}

NEEDLES = {
    "1921_next": ["NEXT1921_0_primary", "EM_hidden_F2_residual"],
    "1921_doc": ["NEXT1921_0_primary", "VAL1921_OVERALL"],
    "1915_priority": ["EM_hidden_F2_residual", "PHYSICALLY_SHARP_BUT_NOT_FIRST_LOCAL_GR_GATE"],
    "1914_vector": ["FRV1914_EM_hidden_F2_residual", "MISSING_ARENA_KERNELS"],
    "988_em_lock": ["EMLOCK988_1_unique_Maxwell_F2", "EMLOCK988_5_theorem_verdict"],
    "989_em_audit": ["ELA989_1_unique_F2", "ELA989_5_total"],
    "989_validation": ["V989_2_unique_F2_counterexample", "V989_6_claim_gates_safe"],
    "1048_f2_attempt": ["F2T1048_1_no_scalar_counterterm", "F2T1048_3_verdict"],
    "1048_vertex_audit": ["PVS1048_1_no_extra_F2", "PVS1048_5_verdict"],
    "1048_claims": ["CG1048_0_no_extra_F2", "CG1048_3_local_GR"],
    "1099_doc": ["UEM1099_2_counterterm", "UEM1099_3_verdict"],
    "1099_claims": ["CG1099_0_no_extra_F2", "CG1099_2_WEP_R10_transfer"],
    "1099_validation": ["V1099_2_counterterm_retained", "V1099_SUMMARY"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1922_SOURCE_REGISTER.csv",
    "proof_audit": OUT / "P8_Y5_PARENT_QLOC_1922_UNIQUE_EM_F2_PROOF_AUDIT.csv",
    "coefficient_rows": OUT / "P8_Y5_PARENT_QLOC_1922_HIDDEN_F2_ALPHA_ROWS_NONCLAIM.csv",
    "guard": OUT / "P8_Y5_PARENT_QLOC_1922_COVARIANCE_GAUGE_INSUFFICIENCY_GUARD.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1922_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1922_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1922_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1922_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1922_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["proof_audit"], SOURCE_WEIGHT_DOCS / "UNIQUE_EM_F2_PROOF_AUDIT_1922_NONCLAIM.csv"),
    (OUTPUTS["coefficient_rows"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1922_HIDDEN_F2_ALPHA_ROWS_NONCLAIM.csv"),
    (OUTPUTS["coefficient_rows"], QUEUE / "JR1922_HIDDEN_F2_ALPHA_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1922_CLAIM_GATE.csv"),
]


def ensure_dirs() -> None:
    for path in [OUT, SOURCE_WEIGHT_DOCS, MICROSCOPE_COEFFS, QUEUE, QUARANTINE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, path in SOURCES.items():
        text = read_text(path) if path.exists() else ""
        missing = [needle for needle in NEEDLES[key] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_key": key,
                "source_path": str(path),
                "needed_for": "1922 EM hidden-F2 unique owner or finite alpha row",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def proof_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEF1922_0_target",
            "claim_piece": "unique parent Maxwell/F_Q2 owner",
            "formal_statement": "S_EM is the unique parent curvature-norm subblock for the observed charge generator T_Q, with no independent hidden-visible F_Q^2 operator.",
            "current_status": "TARGET_SHARP",
            "source_anchor": "NEXT1921_0_primary; UEM1099_0_target",
            "missing_for_claim": "parent-signed T_Q owner, fixed gauge norm, and operator-domain exhaustion",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEF1922_1_chain_rule",
            "claim_piece": "alpha vertical derivative zero if owner signature holds",
            "formal_statement": "If gauge normalization and alpha readout descend through q_loc or fixed representation data, Dq[v]=0 gives b_alpha=Lie_v ln alpha_EM=0.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "source_anchor": "UEM1099_1_chain_rule; F2T1048_0_unique_norm",
            "missing_for_claim": "all owner/readout clauses must be signed rather than chosen by convention",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEF1922_2_counterterm",
            "claim_piece": "scalar gauge-kinetic counterterm exclusion",
            "formal_statement": "DeltaS=-(1/4) int mu_obs f_X(Xhat) F_Q^2 is covariant and gauge-invariant unless a stronger parent rule forbids it.",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "source_anchor": "ELA989_1_unique_F2; UEM1099_2_counterterm; F2T1048_1_no_scalar_counterterm",
            "missing_for_claim": "operator-classification, product-sequester, exact shift, or no-hidden-visible hom theorem",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEF1922_3_current_readout",
            "claim_piece": "current owner and EM readout closure",
            "formal_statement": "charge-current normalization, Hodge/coframe readout, hbar*c conventions, and radiative reductions must be owned by the same parent EM block.",
            "current_status": "UNSIGNED",
            "source_anchor": "EMLOCK988_2_current_owner; EMLOCK988_3_readout_descent; F2T1048_2_no_radiative_reentry",
            "missing_for_claim": "current owner, readout descent, radiative/readout closure",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "UEF1922_4_verdict",
            "claim_piece": "1922 EM hidden-F2 verdict",
            "formal_statement": "The EM_hidden_F2_residual is not zero-derived in the current corpus; hidden-F2/alpha coefficients must be retained until parent operator-domain ownership is signed or sourced.",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS_HIDDEN_F2_ROWS_STAGED",
            "source_anchor": "UEF1922_0_target through UEF1922_3_current_readout",
            "missing_for_claim": "T_Q owner, no independent F2, no hidden-visible coefficient morphism, and radiative/readout closure",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    specs = [
        ("HFA1922_0_lambda_F2", "lambda_F2", "independent observed F_Q^2 coefficient or counterterm amplitude", "MISSING_NO_EXTRA_F2_THEOREM_OR_NUMERIC_COEFFICIENT", "dimensionless_or_declared", "clock;EM spectra;WEP;R10"),
        ("HFA1922_1_fX_slope", "d_ln_fX_dXhat", "vertical derivative of scalar gauge kinetic function f_X(Xhat)", "MISSING_FX_SLOPE_OR_SHIFT_SYMMETRY", "Xhat^-1", "clock;WEP;R10;alpha drift"),
        ("HFA1922_2_b_alpha_EM", "b_alpha_EM", "effective vertical derivative d ln alpha_EM/dXhat after EM owner/readout projection", "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM", "Xhat^-1", "clock;EM spectra;WEP;R10"),
        ("HFA1922_3_beta_source_alpha", "beta_source_alpha", "source/test alpha-channel normalization linking EM coefficient to WEP/R10", "MISSING_SOURCE_NORMALIZATION_OWNER", "dimensionless_or_declared", "WEP_MICROSCOPE_TiPt;R10_short_range"),
        ("HFA1922_4_tau_alpha_clock", "tau_alpha_clock", "clock/readout projection for alpha-channel local response", "MISSING_CLOCK_READOUT_PROJECTION", "dimensionless_or_declared", "clock_and_constant_drift"),
        ("HFA1922_5_alpha_abs_envelope", "alpha_hidden_F2_abs", "absolute no-cancellation envelope for hidden-F2 alpha leakage", "MISSING_COMPONENT_VALUES", "dimensionless_after_projection", "clock;WEP;R10;local_GR"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, symbol, definition, value, units, links in specs:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "residual_component": "EM_hidden_F2_residual",
                "symbol": symbol,
                "definition": definition,
                "candidate_value": value,
                "units": units,
                "source_path": "MISSING_PARENT_OR_EXPERIMENTAL_EM_F2_COEFFICIENT_SOURCE",
                "source_row_id": "MISSING_SOURCE_ROW_ID",
                "required_parent_inputs": "T_Q_owner; unique_F2_norm; no_fX_F2; no_hidden_visible_hom; radiative_readout_closure; arena_projection",
                "observable_links": links,
                "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
                "score_ready": False,
                "valid_prediction_row": False,
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def guard_rows() -> list[dict[str, Any]]:
    guards = [
        ("EGG1922_0_covariance", "claim diffeomorphism covariance forbids f_X F_Q^2", "FORBIDDEN_COVARIANCE_ALLOWS_SCALAR_DENSITY"),
        ("EGG1922_1_U1", "claim U(1) gauge invariance forbids f_X F_Q^2", "FORBIDDEN_GAUGE_INVARIANCE_ALLOWS_F2"),
        ("EGG1922_2_units", "set alpha_EM constant by EM normalization convention", "FORBIDDEN_ALPHA_IS_DIMENSIONLESS"),
        ("EGG1922_3_clock_only", "use clock alpha pressure as standalone WEP/R10 transfer", "FORBIDDEN_WITHOUT_BETA_TAU_KERNELS"),
        ("EGG1922_4_cross_residual", "hide hidden-F2 in constant/source/readout/frame residuals", "FORBIDDEN_CROSS_RESIDUAL_HIDE"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "forbidden_move": move,
            "policy": policy,
            "reason": "hidden-F2 is a legal local counterterm until a stronger parent operator-domain theorem forbids it",
            "status": "ACTIVE",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for guard_id, move, policy in guards
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1922_0_unique_F2",
            "requirement": "unique Maxwell/F_Q2 parent owner and no independent hidden-visible F2",
            "status": "FAIL_COUNTERTERM_RETAINED",
            "evidence": "UEF1922_2_counterterm; UEF1922_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1922_1_coefficients",
            "requirement": "hidden-F2/alpha rows are theorem-zero or source-backed",
            "status": "FAIL_ROWS_SCHEMA_ONLY",
            "evidence": "HFA1922_0_lambda_F2 through HFA1922_5_alpha_abs_envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1922_2_guard",
            "requirement": "covariance/gauge/unit/clock-only shortcuts refused",
            "status": "PASS_GUARD_ONLY",
            "evidence": "EGG1922_0_covariance through EGG1922_4_cross_residual",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1922_3_local_tests",
            "requirement": "EM hidden-F2 branch supports WEP/R10/clock/local-GR scoring",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1922_0_unique_F2; CG1922_1_coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1922_0_derivation_result",
            "decision": "EM_HIDDEN_F2_ZERO_NOT_DERIVED",
            "why": "f_X(Xhat)F_Q^2/lambda_F2 remains legal under covariance and U(1) unless parent operator-domain exhaustion is signed",
            "next_action": "retain hidden-F2/alpha coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1922_1_coefficients",
            "decision": "HIDDEN_F2_ALPHA_ROWS_STAGED_NONCLAIM",
            "why": "six rows now preserve the alpha/EM leakage channels without pretending to score them",
            "next_action": "do not claim EM-lock or alpha constancy until parent zero or numeric/source-backed values exist",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1922_2_next_route",
            "decision": "MOVE_TO_PARENT_OPERATOR_DOMAIN_NO_HIDDEN_VISIBLE_HOM",
            "why": "the same missing parent-domain theorem would attack hidden-F2, mass vertices, source weights, and clock/readout coefficients together",
            "next_action": "1923 should try no-hidden-visible-hom/operator-domain exhaustion before falling back to residual priors",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1922_0_primary",
            "selection_status": "selected",
            "target_doc": "1923-Y5-R2FR-parent-operator-domain-no-hidden-visible-hom-or-residual-prior-pack.md",
            "target_script": "scripts/Y5_R2FR_parent_operator_domain_no_hidden_visible_hom_or_residual_prior_pack_1923.py",
            "objective": "try to derive a parent operator-domain/no-hidden-visible-hom theorem forbidding hidden variables from feeding visible EM, mass, source-weight, and clock coefficients; otherwise stage residual-prior rows",
            "success_condition": "a signed parent-domain theorem closes several coupling residuals, or a nonclaim residual-prior pack preserves every live coefficient",
            "do_not": "do not use covariance, gauge invariance, minimality, unit choice, or public local-GR claims as a substitute for the parent-domain theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1922_0_gain",
            "area": "EM hidden-F2 residual",
            "summary": "1922 localizes the EM bottleneck to the legality of hidden scalar gauge-kinetic terms like f_X(Xhat)F_Q^2.",
            "status": "BOXED_WITH_HIDDEN_F2_QUEUE",
            "what_it_means": "EM-lock remains the clean route, but not a claim until the operator-domain ban is parent-signed",
            "next": "parent operator-domain/no-hidden-visible-hom",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1922_1_safety",
            "area": "symmetry discipline",
            "summary": "covariance, U(1), EM normalization, clock-only pressure, and cross-residual hiding are explicitly refused.",
            "status": "COUNTERTERM_GUARD_ACTIVE",
            "what_it_means": "we do not zero alpha by a normalization trick",
            "next": "derive operator-domain exhaustion or source alpha coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1922_2_next",
            "area": "derivation strategy",
            "summary": "the parent operator-domain/no-hidden-visible-hom theorem is now the best common route because it targets several coupling leaks at once.",
            "status": "NEXT_ATTACK_SELECTED",
            "what_it_means": "we pivot from one residual to the shared parent-domain cause",
            "next": "1923 no-hidden-visible-hom",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "proof_audit": proof_audit_rows(),
        "coefficient_rows": coefficient_rows(),
        "guard": guard_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "snapshot": snapshot_rows(),
    }


def copy_branch_artifacts() -> None:
    for source, destination in BRANCH_COPIES:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def validation_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    sources = parse_csv(OUTPUTS["source_register"])
    rows.append(
        {
            "validation_id": "VAL1922_00_sources",
            "status": "PASS" if all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    proof = parse_csv(OUTPUTS["proof_audit"])
    verdict = next(r for r in proof if r["audit_id"] == "UEF1922_4_verdict")
    rows.append(
        {
            "validation_id": "VAL1922_01_proof_audit",
            "status": "PASS" if verdict["current_status"] == "NOT_DERIVED_CURRENT_CORPUS_HIDDEN_F2_ROWS_STAGED" and all(r["proof_pass"] == "False" for r in proof) else "FAIL",
            "detail": "unique EM/F2 zero proof remains unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    coeffs = parse_csv(OUTPUTS["coefficient_rows"])
    rows.append(
        {
            "validation_id": "VAL1922_02_coefficient_rows",
            "status": "PASS" if len(coeffs) == 6 and all(r["status"] == "SOURCE_READY_SCHEMA_ONLY_NONCLAIM" and r["valid_for_claim"] == "False" for r in coeffs) else "FAIL",
            "detail": "six hidden-F2/alpha coefficient schemas staged as nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    guards = parse_csv(OUTPUTS["guard"])
    rows.append(
        {
            "validation_id": "VAL1922_03_guard",
            "status": "PASS" if len(guards) == 5 and all(r["status"] == "ACTIVE" for r in guards) else "FAIL",
            "detail": "covariance/gauge/unit shortcuts forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(r for r in gates if r["gate_id"] == "CG1922_3_local_tests")
    rows.append(
        {
            "validation_id": "VAL1922_04_claim_gate",
            "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL",
            "detail": "EM hidden-F2 residual supports no scoring claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append(
        {
            "validation_id": "VAL1922_05_decision",
            "status": "PASS" if any(r["decision"] == "MOVE_TO_PARENT_OPERATOR_DOMAIN_NO_HIDDEN_VISIBLE_HOM" for r in decisions) else "FAIL",
            "detail": "parent operator-domain/no-hidden-visible-hom route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append(
        {
            "validation_id": "VAL1922_06_next_target",
            "status": "PASS" if next_rows[0]["target_doc"].startswith("1923-Y5-R2FR-parent-operator-domain") else "FAIL",
            "detail": "1923 parent operator-domain route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    generated = [p for k, p in OUTPUTS.items() if k != "validation"]
    csv_ok = True
    claim_safe = True
    for path in generated:
        try:
            parsed = parse_csv(path)
            csv_ok = csv_ok and bool(parsed)
            for row in parsed:
                if row.get("valid_for_claim", "False") != "False" or row.get("claim_allowed", "False") != "False":
                    claim_safe = False
        except Exception:
            csv_ok = False
    rows.append(
        {
            "validation_id": "VAL1922_07_claim_flags_safe",
            "status": "PASS" if claim_safe else "FAIL",
            "detail": "claim flags all false",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    rows.append(
        {
            "validation_id": "VAL1922_08_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSVs parse with rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    rows.append(
        {
            "validation_id": "VAL1922_09_branch_copies",
            "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL",
            "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append(
        {
            "validation_id": "VAL1922_10_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(
            1
            for path in FORMALIZATION.rglob("*")
            if path.name.startswith("1922-")
            or "_1922" in path.name
            or "1922_" in path.name
            or "Y5_R2FR_EM_hidden_F2" in path.name
        )
    rows.append(
        {
            "validation_id": "VAL1922_11_formalization_untouched",
            "status": "PASS" if formalization_count == 0 else "FAIL",
            "detail": f"formalization_1922_artifact_count={formalization_count}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        {
            "validation_id": "VAL1922_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1922 EM hidden-F2 unique owner or finite alpha row",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("\n", " ").replace("|", "\\|") for h in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1922 - EM Hidden-F2 Unique Owner Or Finite Alpha Row

## Purpose

This checkpoint attacks `EM_hidden_F2_residual`: either prove a unique parent Maxwell/`F_Q^2` owner with no independent hidden-visible `F^2` operator, or stage finite hidden-F2/alpha rows without claiming a pass.

## Result

- The unique-EM-owner theorem remains exact only as a conditional.
- The decisive counterexample is retained: `f_X(Xhat) F_Q^2` or `lambda_F2 F_Q^2` is covariant and gauge-invariant unless a stronger parent operator-domain theorem forbids it.
- Six nonclaim rows are staged for hidden-F2/alpha leakage and projection factors.
- Covariance, U(1), unit normalization, clock-only pressure, and cross-residual hiding are explicitly refused.
- The next route is the shared parent-domain/no-hidden-visible-hom theorem, because it targets EM, mass, source-weight, and clock couplings together.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Unique EM/F2 Proof Audit

{markdown_table(rows_by_name["proof_audit"])}

## Hidden-F2 Alpha Rows

{markdown_table(rows_by_name["coefficient_rows"])}

## Covariance/Gauge Insufficiency Guard

{markdown_table(rows_by_name["guard"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Project Status Snapshot

{markdown_table(rows_by_name["snapshot"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()
    rows_by_name = build_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
