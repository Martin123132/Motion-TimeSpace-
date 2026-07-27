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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1921"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1921-Y5-R2FR-constant-sector-superselection-or-alpha-mass-clock-first-rows.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1920_next": OUT / "P8_Y5_PARENT_QLOC_1920_NEXT_TARGET.csv",
    "1920_doc": ROOT / "1920-Y5-R2FR-source-weight-parent-current-owner-or-delta-w-first-rows.md",
    "1915_priority": OUT / "P8_Y5_PARENT_QLOC_1915_RESIDUAL_PRIORITY_MATRIX_NONCLAIM.csv",
    "1914_vector": OUT / "P8_Y5_PARENT_QLOC_1914_FINITE_RESIDUAL_VECTOR_V0_NONCLAIM.csv",
    "1912_axioms": OUT / "P8_Y5_PARENT_QLOC_1912_MINIMAL_AXIOM_DEBT_LEDGER_NONCLAIM.csv",
    "1913_typing": OUT / "P8_Y5_PARENT_QLOC_1913_Q_FUNCTOR_TYPING_MATRIX_NONCLAIM.csv",
    "1046_doc": ROOT / "1046-Y5-R10-no-shadow-frame-constant-marker-theorem-or-qbar-marker-coefficients.md",
    "1047_doc": ROOT / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
    "1047_theorem": OUT / "P8_Y5_R10_1047_CONSTANT_SUPERSELECTION_THEOREM_ATTEMPT.csv",
    "1047_coefficients": OUT / "P8_Y5_R10_1047_COEFFICIENT_PROVENANCE_ROWS.csv",
    "1047_claim_gates": OUT / "P8_Y5_R10_1047_CLAIM_GATES.csv",
    "1047_validation": OUT / "P8_Y5_BRR545_1047_VALIDATION.csv",
}

NEEDLES = {
    "1920_next": ["NEXT1920_0_primary", "constant_sector_residual"],
    "1920_doc": ["NEXT1920_0_primary", "VAL1920_OVERALL"],
    "1915_priority": ["constant_sector_residual", "IMPORTANT_BUT_SPLITS_INTO_MULTIPLE_CONSTANT_SUBSECTORS"],
    "1914_vector": ["FRV1914_constant_sector_residual", "MISSING_ARENA_KERNELS"],
    "1912_axioms": ["AX1912_3_fixed_constant_sector", "MISSING_AXIOM_NOT_ADOPTED"],
    "1913_typing": ["QTM1913_4_constants", "CONSTANT_SUPERSELECTION_UNSIGNED"],
    "1046_doc": ["QCC1046_0_b_alpha", "QCC1046_1_b_mA"],
    "1047_doc": ["CST1047_0_descent_or_superselection_criterion", "CG1047_4_local_tests"],
    "1047_theorem": ["CST1047_0_descent_or_superselection_criterion", "CST1047_5_verdict"],
    "1047_coefficients": ["CP1047_0_b_alpha", "CP1047_4_qbar_constants_abs"],
    "1047_claim_gates": ["CG1047_0_alpha_zero", "CG1047_4_local_tests"],
    "1047_validation": ["V1047_SUMMARY", "V1047_10_claim_gates_blocked"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1921_SOURCE_REGISTER.csv",
    "proof_audit": OUT / "P8_Y5_PARENT_QLOC_1921_CONSTANT_SUPERSELECTION_PROOF_AUDIT.csv",
    "coefficient_rows": OUT / "P8_Y5_PARENT_QLOC_1921_ALPHA_MASS_CLOCK_FIRST_ROWS_NONCLAIM.csv",
    "unit_guard": OUT / "P8_Y5_PARENT_QLOC_1921_NO_UNIT_RESCALING_GUARD.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1921_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1921_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1921_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1921_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1921_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["proof_audit"], SOURCE_WEIGHT_DOCS / "CONSTANT_SUPERSELECTION_PROOF_AUDIT_1921_NONCLAIM.csv"),
    (OUTPUTS["coefficient_rows"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1921_ALPHA_MASS_CLOCK_FIRST_ROWS_NONCLAIM.csv"),
    (OUTPUTS["coefficient_rows"], QUEUE / "JR1921_CONSTANT_SECTOR_COEFFICIENT_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1921_CLAIM_GATE.csv"),
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
                "needed_for": "1921 constant-sector superselection or alpha/mass/clock first rows",
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
            "audit_id": "CSP1921_0_conditional_criterion",
            "claim_piece": "exact local silence criterion",
            "formal_statement": "If theta(Phi)=theta_bar(q_loc(Phi)) or theta is discrete/topological superselection data, Dq_loc[v]=0 implies Lie_v theta=0.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "source_anchor": "CST1047_0_descent_or_superselection_criterion",
            "missing_for_claim": "parent classification of alpha_EM, mass ratios, nuclear/binding data, and clock constants",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSP1921_1_alpha_EM",
            "claim_piece": "alpha_EM vertical silence",
            "formal_statement": "b_alpha := Lie_v ln alpha_EM = 0 only if the parent signs charge-lattice owner, unique F_Q^2 normalization, no f_X F^2, and quotient readout.",
            "current_status": "BLOCKED_RETAIN_B_ALPHA",
            "source_anchor": "AGN1047_4_verdict; CG1047_0_alpha_zero",
            "missing_for_claim": "unique-F2, charge owner, no-alpha vertex, hbar*c/readout descent",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSP1921_2_mass_ratios",
            "claim_piece": "mass-ratio and binding vertical silence",
            "formal_statement": "b_mA and b_mu vanish only if dimensionless spectra, Yukawa/Higgs/QCD/binding data, and material sensitivities are quotient-owned or superselected.",
            "current_status": "BLOCKED_RETAIN_B_MASS",
            "source_anchor": "MRS1047_4_verdict; CG1047_1_mass_zero",
            "missing_for_claim": "parent matter spectrum, binding decomposition, no m_A(Xhat) or y_A(Xhat) vertices",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSP1921_3_clock_constants",
            "claim_piece": "clock-ratio vertical silence",
            "formal_statement": "b_clock_i is zero only after all upstream alpha, mass-ratio, nuclear, and clock-readout coefficients are zero or sourced.",
            "current_status": "INHERITS_ALPHA_MASS_NUCLEAR_AND_READOUT_DEBT",
            "source_anchor": "CST1047_3_clock_transitions; CG1047_2_clock_zero",
            "missing_for_claim": "clock sensitivity matrix beyond alpha rows, b_mu/b_nuc provenance, tau_clock/local dXhat projection",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSP1921_4_no_unit_cheat",
            "claim_piece": "dimensionless observable guard",
            "formal_statement": "Unit choices cannot erase Lie_v ln alpha_EM, Lie_v ln(m_A/m_B), or Lie_v ln(nu_i/nu_j).",
            "current_status": "GUARD_PASSED_POLICY_ONLY",
            "source_anchor": "CST1047_4_no_unit_rescaling_cheat",
            "missing_for_claim": "none as a guard; it blocks false proofs but does not prove zero",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CSP1921_5_verdict",
            "claim_piece": "1921 constant-sector verdict",
            "formal_statement": "The constant_sector_residual is not zero-derived in the current corpus; alpha, mass, nuclear, clock, and qbar-constant coefficients must be retained.",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS_COEFFICIENT_ROWS_STAGED",
            "source_anchor": "CSP1921_0_conditional_criterion through CSP1921_4_no_unit_cheat",
            "missing_for_claim": "parent ownership/signature or source-backed numerical coefficients",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    specs = [
        ("CCR1921_0_b_alpha", "b_alpha", "vertical derivative d ln alpha_EM/dXhat or equivalent gauge/readout derivative", "MISSING_B_ALPHA_OR_PARENT_ZERO_THEOREM", "Xhat^-1", "clock;EM spectra;WEP;R10"),
        ("CCR1921_1_b_mu", "b_mu", "vertical derivative of dimensionless mass ratios such as m_e/m_p", "MISSING_B_MU_OR_PARENT_ZERO_THEOREM", "Xhat^-1", "clock;WEP;composition;source_charge"),
        ("CCR1921_2_b_mA", "b_mA", "vertical derivative of material/species mass and binding response after removing unit-only common mode", "MISSING_B_MASS_OR_COMPOSITION_SENSITIVITY_MATRIX", "Xhat^-1", "MICROSCOPE;R10;clock;Newton_GM"),
        ("CCR1921_3_b_nuc", "b_nuc", "vertical derivative of nuclear/binding response not captured by alpha or simple mass ratios", "MISSING_NUCLEAR_BINDING_RESPONSE", "Xhat^-1", "clock;WEP;composition"),
        ("CCR1921_4_b_clock_i", "b_clock_i", "vertical derivative of a clock transition/ratio after alpha, mass, and nuclear projections", "MISSING_CLOCK_CONSTANT_PROJECTION", "Xhat^-1", "clock comparison;redshift/LPI;alpha drift"),
        ("CCR1921_5_qbar_constants_abs", "qbar_constants_abs", "absolute no-cancellation envelope for all constant-sector leakage into local observables", "MISSING_COMPONENT_VALUES", "dimensionless_after_projection", "WEP;clock;R10;EM;local_GR"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, symbol, definition, value, units, links in specs:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "residual_component": "constant_sector_residual",
                "symbol": symbol,
                "definition": definition,
                "candidate_value": value,
                "units": units,
                "source_path": "MISSING_PARENT_OR_EXPERIMENTAL_CONSTANT_COEFFICIENT_SOURCE",
                "source_row_id": "MISSING_SOURCE_ROW_ID",
                "required_parent_inputs": "constant_superselection; quotient_readout; Xhat_normalization; arena_projection; no_unit_rescaling_cheat",
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


def unit_guard_rows() -> list[dict[str, Any]]:
    guards = [
        ("URG1921_0_alpha_units", "set alpha_EM constant by unit convention", "FORBIDDEN_ALPHA_IS_DIMENSIONLESS"),
        ("URG1921_1_mass_units", "hide mass-ratio or binding variation in kg choice", "FORBIDDEN_FOR_DIMENSIONLESS_RATIOS"),
        ("URG1921_2_clock_units", "choose a clock unit to remove all clock-ratio drift", "FORBIDDEN_ONLY_ONE_SCALE_CAN_BE_CONVENTIONAL"),
        ("URG1921_3_coefficient_absorption", "fold b_alpha/b_mA/b_clock into source_weight/readout/frame residuals", "FORBIDDEN_CROSS_RESIDUAL_HIDE"),
        ("URG1921_4_local_claim", "call constant-sector fixed because Standard Model constants are usually constants", "FORBIDDEN_AS_DERIVATION"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": guard_id,
            "forbidden_move": move,
            "policy": policy,
            "reason": "constant-sector silence must be parent-derived or retained as explicit coefficients",
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
            "gate_id": "CG1921_0_constant_superselection",
            "requirement": "alpha/mass/clock constants are parent-classified as quotient-owned or superselected",
            "status": "FAIL_NOT_PARENT_SIGNED",
            "evidence": "CSP1921_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1921_1_coefficient_rows",
            "requirement": "b_alpha/b_mu/b_mA/b_nuc/b_clock/qbar_constants are theorem-zero or source-backed",
            "status": "FAIL_ROWS_SCHEMA_ONLY",
            "evidence": "CCR1921_0_b_alpha through CCR1921_5_qbar_constants_abs",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1921_2_unit_guard",
            "requirement": "no unit-rescaling or cross-residual hiding",
            "status": "PASS_GUARD_ONLY",
            "evidence": "URG1921_0_alpha_units through URG1921_4_local_claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1921_3_local_tests",
            "requirement": "constant sector supports WEP/R10/clock/local-GR scoring",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1921_0_constant_superselection; CG1921_1_coefficient_rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1921_0_derivation_result",
            "decision": "CONSTANT_SECTOR_ZERO_NOT_DERIVED",
            "why": "the conditional theorem is exact but actual alpha/mass/clock parent classifications are unsigned",
            "next_action": "retain coefficient rows and no-cancellation envelope",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1921_1_coefficients",
            "decision": "ALPHA_MASS_CLOCK_ROWS_STAGED_NONCLAIM",
            "why": "six coefficient rows now carry explicit missing inputs and observable links",
            "next_action": "do not score until theorem-zero or numeric/source-backed values replace all MISSING markers",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1921_2_next_residual",
            "decision": "MOVE_TO_EM_HIDDEN_F2_RESIDUAL",
            "why": "the alpha branch is blocked partly by unique-F2/no-extra-EM ownership, and 1915 ranks EM_hidden_F2 next",
            "next_action": "1922 should try unique Maxwell/F_Q^2 parent owner proof or stage finite hidden-F2 coefficient rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1921_0_primary",
            "selection_status": "selected",
            "target_doc": "1922-Y5-R2FR-EM-hidden-F2-unique-owner-or-finite-alpha-row.md",
            "target_script": "scripts/Y5_R2FR_EM_hidden_F2_unique_owner_or_finite_alpha_row_1922.py",
            "objective": "attack EM_hidden_F2_residual: prove a unique parent Maxwell/F_Q^2 owner with no independent hidden-visible F2 operator, or stage finite hidden-F2/alpha coefficient rows as nonclaim",
            "success_condition": "EM_hidden_F2_residual gets a parent theorem-zero source path, finite source-ready coefficient rows, or closure-only demotion with blockers preserved",
            "do_not": "do not claim EM-lock, alpha_EM constancy, WEP/clock pass, or local-GR reduction from a mere choice of EM normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1921_0_gain",
            "area": "constant sector",
            "summary": "1921 keeps the exact conditional superselection theorem but refuses to promote alpha/mass/clock silence without parent classification.",
            "status": "BOXED_WITH_COEFFICIENT_QUEUE",
            "what_it_means": "the algebra is clean; the missing thing is parent ownership of the actual constants",
            "next": "move to EM hidden F2/unique owner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1921_1_safety",
            "area": "units discipline",
            "summary": "dimensionless alpha, mass ratios, and clock ratios cannot be erased by units or shifted into other residuals.",
            "status": "NO_UNIT_RESCALING_GUARD_ACTIVE",
            "what_it_means": "we avoid a classic false proof of constant-sector silence",
            "next": "derive or source constant coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1921_2_next",
            "area": "residual priority",
            "summary": "EM_hidden_F2_residual is next because unique Maxwell ownership is the alpha_EM bottleneck.",
            "status": "NEXT_ATTACK_SELECTED",
            "what_it_means": "this is the natural bridge from constants into EM discipline",
            "next": "1922 EM hidden-F2 unique owner",
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
        "unit_guard": unit_guard_rows(),
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
            "validation_id": "VAL1921_00_sources",
            "status": "PASS" if all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources) else "FAIL",
            "detail": "all local source paths exist and needles found",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    proof = parse_csv(OUTPUTS["proof_audit"])
    verdict = next(r for r in proof if r["audit_id"] == "CSP1921_5_verdict")
    rows.append(
        {
            "validation_id": "VAL1921_01_proof_audit",
            "status": "PASS" if verdict["current_status"] == "NOT_DERIVED_CURRENT_CORPUS_COEFFICIENT_ROWS_STAGED" and all(r["proof_pass"] == "False" for r in proof) else "FAIL",
            "detail": "constant-sector zero proof remains unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    coeffs = parse_csv(OUTPUTS["coefficient_rows"])
    rows.append(
        {
            "validation_id": "VAL1921_02_coefficient_rows",
            "status": "PASS" if len(coeffs) == 6 and all(r["status"] == "SOURCE_READY_SCHEMA_ONLY_NONCLAIM" and r["valid_for_claim"] == "False" for r in coeffs) else "FAIL",
            "detail": "six alpha/mass/clock coefficient schemas staged as nonclaim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    guards = parse_csv(OUTPUTS["unit_guard"])
    rows.append(
        {
            "validation_id": "VAL1921_03_unit_guard",
            "status": "PASS" if len(guards) == 5 and all(r["status"] == "ACTIVE" for r in guards) else "FAIL",
            "detail": "unit-rescaling/cross-residual shortcuts forbidden",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(r for r in gates if r["gate_id"] == "CG1921_3_local_tests")
    rows.append(
        {
            "validation_id": "VAL1921_04_claim_gate",
            "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL",
            "detail": "constant sector supports no scoring claim",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append(
        {
            "validation_id": "VAL1921_05_decision",
            "status": "PASS" if any(r["decision"] == "MOVE_TO_EM_HIDDEN_F2_RESIDUAL" for r in decisions) else "FAIL",
            "detail": "EM_hidden_F2 residual selected after boxing constants",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append(
        {
            "validation_id": "VAL1921_06_next_target",
            "status": "PASS" if next_rows[0]["target_doc"].startswith("1922-Y5-R2FR-EM-hidden-F2") else "FAIL",
            "detail": "1922 EM hidden-F2 route selected",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    all_generated = [p for k, p in OUTPUTS.items() if k != "validation"]
    csv_ok = True
    claim_safe = True
    for path in all_generated:
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
            "validation_id": "VAL1921_07_claim_flags_safe",
            "status": "PASS" if claim_safe else "FAIL",
            "detail": "claim flags all false",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    rows.append(
        {
            "validation_id": "VAL1921_08_csv_parse",
            "status": "PASS" if csv_ok else "FAIL",
            "detail": "all generated CSVs parse with rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    rows.append(
        {
            "validation_id": "VAL1921_09_branch_copies",
            "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL",
            "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES),
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append(
        {
            "validation_id": "VAL1921_10_pycache_absent",
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
            if path.name.startswith("1921-")
            or "_1921" in path.name
            or "1921_" in path.name
            or "Y5_R2FR_constant_sector" in path.name
        )
    rows.append(
        {
            "validation_id": "VAL1921_11_formalization_untouched",
            "status": "PASS" if formalization_count == 0 else "FAIL",
            "detail": f"formalization_1921_artifact_count={formalization_count}",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append(
        {
            "validation_id": "VAL1921_OVERALL",
            "status": "PASS" if overall else "FAIL",
            "detail": "1921 constant-sector superselection or alpha/mass/clock first rows",
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
    content = f"""# 1921 - Constant-Sector Superselection Or Alpha/Mass/Clock First Rows

## Purpose

This checkpoint attacks the rank-4 `constant_sector_residual`: either prove masses, charges, `alpha_EM`, and clock constants are quotient-owned/superselected, or stage finite alpha/mass/clock coefficient rows without claiming a pass.

## Result

- The exact constant-silence criterion is retained: quotient descent or true discrete/topological superselection kills vertical derivatives.
- The actual MTS local branch does not yet prove that `alpha_EM`, mass ratios, nuclear/binding data, or clock constants satisfy that criterion.
- Six source-ready but nonclaim rows are staged: `b_alpha`, `b_mu`, `b_mA`, `b_nuc`, `b_clock_i`, and `qbar_constants_abs`.
- Unit-rescaling and cross-residual hiding are explicitly forbidden.
- The next target is `EM_hidden_F2_residual`, because unique Maxwell/F_Q^2 ownership is the `alpha_EM` bottleneck.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Constant Superselection Proof Audit

{markdown_table(rows_by_name["proof_audit"])}

## Alpha/Mass/Clock First Rows

{markdown_table(rows_by_name["coefficient_rows"])}

## No Unit-Rescaling Guard

{markdown_table(rows_by_name["unit_guard"])}

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
