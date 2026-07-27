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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1924"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1924-Y5-R2FR-hidden-invariant-algebra-triviality-or-scalar-prior-rows.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1923_next": OUT / "P8_Y5_PARENT_QLOC_1923_NEXT_TARGET.csv",
    "1923_doc": ROOT / "1923-Y5-R2FR-parent-operator-domain-no-hidden-visible-hom-or-residual-prior-pack.md",
    "1923_obstructions": OUT / "P8_Y5_PARENT_QLOC_1923_HIDDEN_INVARIANT_OBSTRUCTION_LEDGER.csv",
    "1092_triviality": OUT / "P8_Y5_R10_1092_HIDDEN_INVARIANT_TRIVIALITY_ATTEMPT.csv",
    "1092_generators": OUT / "P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv",
    "1092_nohair": OUT / "P8_Y5_R10_1092_SCALAR_NOHAIR_ROUTE_AUDIT.csv",
    "1092_claims": OUT / "P8_Y5_R10_1092_CLAIM_GATES.csv",
    "1092_validation": OUT / "P8_Y5_BRR545_1092_VALIDATION.csv",
    "1093_owner": OUT / "P8_Y5_R10_1093_PARENT_SCALAR_OWNER_ATTEMPT.csv",
    "1093_operator": OUT / "P8_Y5_R10_1093_POSITIVE_OPERATOR_INPUT_PACK.csv",
    "1093_source": OUT / "P8_Y5_R10_1093_SOURCE_SILENCE_AUDIT.csv",
    "1093_boundary": OUT / "P8_Y5_R10_1093_BOUNDARY_DOMAIN_AUDIT.csv",
    "1093_theorem": OUT / "P8_Y5_R10_1093_CONDITIONAL_NOHAIR_THEOREM.csv",
    "1093_claims": OUT / "P8_Y5_R10_1093_CLAIM_GATES.csv",
    "1093_validation": OUT / "P8_Y5_BRR545_1093_VALIDATION.csv",
    "980_functor": OUT / "P8_Y5_R10_980_NO_MARKER_FUNCTOR_THEOREM_ATTEMPT.csv",
    "980_counter": OUT / "P8_Y5_R10_980_COUNTEREXAMPLE_LEDGER.csv",
}

NEEDLES = {
    "1923_next": ["NEXT1923_0_primary", "hidden/local invariant algebra"],
    "1923_doc": ["NEXT1923_0_primary", "VAL1923_OVERALL"],
    "1923_obstructions": ["OBS1923_0_invariant_scalar", "LIVE_NONCLAIM_OBSTRUCTION"],
    "1092_triviality": ["HIT1092_5_verdict", "TRIVIALITY_NOT_DERIVED"],
    "1092_generators": ["GEN1092_0_finite_cell_spectrum", "GEN1092_6_readout_projector"],
    "1092_nohair": ["SNH1092_4_verdict", "NOHAIR_ROUTE_UNSIGNED"],
    "1092_claims": ["CG1092_0_hidden_triviality", "CG1092_1_scalar_nohair"],
    "1092_validation": ["V1092_1_triviality_not_derived", "V1092_SUMMARY"],
    "1093_owner": ["OWN1093_4_verdict", "PARENT_OWNER_NOT_DERIVED"],
    "1093_operator": ["OP1093_4_verdict", "OPERATOR_PACK_UNSIGNED"],
    "1093_source": ["JX1093_4_verdict", "SOURCE_SILENCE_NOT_DERIVED"],
    "1093_boundary": ["BD1093_0_boundary_flux", "BD1093_3_domain_selector"],
    "1093_theorem": ["THM1093_2_zero_result", "THM1093_4_verdict"],
    "1093_claims": ["CG1093_0_parent_owner", "CG1093_1_positive_nohair"],
    "1093_validation": ["V1093_1_parent_owner_not_derived", "V1093_SUMMARY"],
    "980_functor": ["NMF980_2_scalar_obstruction_lemma", "NMF980_7_verdict"],
    "980_counter": ["CEX980_0_theta_IQ", "CEX980_6_boundary_flux"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1924_SOURCE_REGISTER.csv",
    "triviality_audit": OUT / "P8_Y5_PARENT_QLOC_1924_HIDDEN_INVARIANT_TRIVIALITY_AUDIT.csv",
    "generator_rows": OUT / "P8_Y5_PARENT_QLOC_1924_SURVIVING_SCALAR_GENERATOR_ROWS_NONCLAIM.csv",
    "nohair_pack": OUT / "P8_Y5_PARENT_QLOC_1924_SCALAR_NOHAIR_INPUT_PACK_NONCLAIM.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1924_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1924_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1924_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1924_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1924_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["triviality_audit"], SOURCE_WEIGHT_DOCS / "HIDDEN_INVARIANT_TRIVIALITY_AUDIT_1924_NONCLAIM.csv"),
    (OUTPUTS["generator_rows"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1924_SURVIVING_SCALAR_GENERATOR_ROWS_NONCLAIM.csv"),
    (OUTPUTS["nohair_pack"], QUEUE / "JR1924_SCALAR_NOHAIR_INPUT_PACK_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1924_CLAIM_GATE.csv"),
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
                "needed_for": "1924 hidden invariant algebra triviality or scalar prior rows",
                "needles": ";".join(NEEDLES[key]),
                "status": "EXISTS_NEEDLES_CONFIRMED" if path.exists() and not missing else "MISSING_OR_NEEDLE_FAILED",
                "missing_needles": ";".join(missing),
                "valid_for_claim": False,
                "claim_allowed": False,
                "generated_utc": GENERATED_UTC,
            }
        )
    return rows


def triviality_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HIT1924_0_target",
            "claim_piece": "hidden/local invariant algebra triviality",
            "formal_statement": "O(C_hid)^inv = R on the physical local branch, so no nonconstant scalar coefficient map survives.",
            "current_status": "TARGET_SHARP",
            "source_anchor": "NEXT1923_0_primary; HIT1092_0_target",
            "missing_for_claim": "generator elimination, exact shift/no-hair, or profile-zero theorem",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HIT1924_1_sufficiency",
            "claim_piece": "triviality implies visible coefficients are constant",
            "formal_statement": "If O(C_hid)^inv=R, any invariant coefficient c:C_hid->R is constant and hidden-visible hom maps collapse.",
            "current_status": "EXACT_CONDITIONAL_THEOREM",
            "source_anchor": "HIT1092_1_sufficiency; ODH1923_1_trivial_invariant_algebra",
            "missing_for_claim": "actual proof of O(C_hid)^inv=R for the active MTS branch",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HIT1924_2_generator_debt",
            "claim_piece": "surviving generator audit",
            "formal_statement": "finite cell spectrum, domain class, selector, memory scalar, time-arrow, species constants, and readout projector are not all trivialized.",
            "current_status": "FAIL_CURRENT_CORPUS_GENERATORS_SURVIVE",
            "source_anchor": "GEN1092_0_finite_cell_spectrum through GEN1092_6_readout_projector",
            "missing_for_claim": "every generator must be pure gauge, fixed class, exact zero, or explicitly bounded",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HIT1924_3_scalar_counterexample",
            "claim_piece": "nonconstant scalar obstruction",
            "formal_statement": "If I in O(C_hid)^inv and dI != 0, then b_alpha(I), m_A(I), theta_A(I), or kappa(I) is a live coefficient map.",
            "current_status": "COUNTEREXAMPLE_RETAINED",
            "source_anchor": "HIT1092_3_scalar_counterexample; NMF980_2_scalar_obstruction_lemma",
            "missing_for_claim": "I absent, no-haired, constant, or forbidden as a coefficient argument",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HIT1924_4_nohair_route",
            "claim_piece": "exact shift/no-hair/profile-zero route",
            "formal_statement": "A parent-owned scalar with positive operator, zero source, zero boundary flux, and no zero mode would force local value/gradient silence.",
            "current_status": "CONDITIONAL_ONLY_INPUTS_UNSIGNED",
            "source_anchor": "SNH1092_4_verdict; THM1093_4_verdict",
            "missing_for_claim": "parent owner, positive operator pack, source silence, boundary/domain silence, zero-mode handling",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "HIT1924_5_verdict",
            "claim_piece": "1924 hidden invariant verdict",
            "formal_statement": "Hidden invariant algebra triviality is not derived in the current corpus; scalar generator/prior rows remain live.",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS_SCALAR_PRIOR_ROWS_STAGED",
            "source_anchor": "HIT1924_1_sufficiency through HIT1924_4_nohair_route",
            "missing_for_claim": "generator triviality or complete no-hair/profile-zero theorem",
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def generator_rows() -> list[dict[str, Any]]:
    specs = [
        ("SGR1924_0_finite_cell_spectrum", "finite_cell_fibre_spectrum", "can act as mass gap, scalar charge, or fifth-force scale", "MISSING_TRIVIALIZATION_OR_BOUND"),
        ("SGR1924_1_relative_domain_class", "relative_boundary_domain_class", "can select local branch or domain-dependent coupling", "MISSING_FIXED_CLASS_OR_BOUND"),
        ("SGR1924_2_domain_selector", "domain_selector_chi_D", "can become active projector/source switch", "MISSING_SELECTOR_THEOREM"),
        ("SGR1924_3_memory_scalar", "memory_or_class_scalar", "can drive clock drift, gamma shift, or fifth-force channel", "MISSING_VALUE_GRADIENT_ZERO_OR_BOUND"),
        ("SGR1924_4_orientation_time_arrow", "orientation_time_arrow", "can create preferred-frame or time-asymmetry residual", "MISSING_COFRAME_OR_GAUGE_CLASSIFICATION"),
        ("SGR1924_5_species_constants", "species_charge_constants", "can create WEP/source-charge/clock nonuniversality", "MISSING_CONSTANT_SECTOR_UNIVERSALITY"),
        ("SGR1924_6_readout_projector", "readout_projector", "can re-enter as reduced action term if varied too early", "MISSING_READOUT_AFTER_VARIATION_THEOREM"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "generator": generator,
            "risk": risk,
            "candidate_value": value,
            "source_path": "MISSING_PARENT_TRIVIALITY_OR_SCALAR_BOUND_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "required_elimination": "pure gauge; fixed class; exact no-hair/profile-zero; or source-backed finite prior",
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for row_id, generator, risk, value in specs
    ]


def nohair_pack_rows() -> list[dict[str, Any]]:
    specs = [
        ("NHP1924_0_parent_owner", "parent-owned scalar/operator variable Xhat or I", "MISSING_PARENT_OWNER", "no-hair must act on the same scalar that feeds visible coefficients"),
        ("NHP1924_1_positive_operator", "Z_X>0 and M_X^2>=0 with self-adjoint local domain", "MISSING_SIGNED_OPERATOR", "positive integral identity cannot be used without signed operator/domain"),
        ("NHP1924_2_source_silence", "J_X=0 for ordinary local matter/readout", "MISSING_SOURCE_SILENCE", "ordinary matter can excite the scalar channel"),
        ("NHP1924_3_boundary_flux", "Phi_boundary_local=0 or explicit upper bound", "MISSING_BOUNDARY_CONDITION", "boundary terms can carry hidden scalar into lab region"),
        ("NHP1924_4_zero_mode", "no topological/gauge zero mode outside quotient kernel", "MISSING_ZERO_MODE_GATE", "positive norm may leave a flat/local mode"),
        ("NHP1924_5_verdict", "complete no-hair/profile-zero input pack", "NOHAIR_ROUTE_UNSIGNED", "all clauses must close together before scalar obstruction dies"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": input_id,
            "required_input": required,
            "candidate_value": value,
            "mathematical_role": role,
            "source_path": "MISSING_PARENT_NOHAIR_OR_BOUND_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for input_id, required, value, role in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1924_0_triviality",
            "requirement": "O(C_hid)^inv=R or equivalent signed theorem",
            "status": "FAIL_GENERATORS_SURVIVE",
            "evidence": "HIT1924_2_generator_debt; HIT1924_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1924_1_nohair",
            "requirement": "parent-owned positive source-free no-hair/profile-zero theorem",
            "status": "FAIL_INPUT_PACK_UNSIGNED",
            "evidence": "NHP1924_0_parent_owner through NHP1924_5_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1924_2_scalar_rows",
            "requirement": "surviving scalar generator rows are source-backed or theorem-zero",
            "status": "FAIL_ROWS_SCHEMA_ONLY",
            "evidence": "SGR1924_0_finite_cell_spectrum through SGR1924_6_readout_projector",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1924_3_local_tests",
            "requirement": "hidden invariant route supports local-GR/WEP/R10/clock scoring",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1924_0_triviality; CG1924_1_nohair; CG1924_2_scalar_rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1924_0_triviality_result",
            "decision": "HIDDEN_INVARIANT_TRIVIALITY_NOT_DERIVED",
            "why": "surviving generator ledger remains live and scalar counterexample is retained",
            "next_action": "retain scalar generator rows and attack no-hair input ownership",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1924_1_nohair_result",
            "decision": "NOHAIR_ROUTE_EXACT_BUT_UNSIGNED",
            "why": "parent owner, sign, source silence, boundary flux, and zero-mode gates are all needed together",
            "next_action": "build a focused parent scalar owner/positive operator/source/boundary pack",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1924_2_next_route",
            "decision": "MOVE_TO_PARENT_SCALAR_NOHAIR_INPUT_PACK",
            "why": "no-hair/profile-zero is the least hand-wavy route to killing the hidden scalar obstruction",
            "next_action": "1925 should try parent scalar owner + positive operator + source silence + boundary/zero-mode closure, or stage finite scalar profile rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1924_0_primary",
            "selection_status": "selected",
            "target_doc": "1925-Y5-R2FR-parent-scalar-nohair-input-pack-or-finite-profile-rows.md",
            "target_script": "scripts/Y5_R2FR_parent_scalar_nohair_input_pack_or_finite_profile_rows_1925.py",
            "objective": "try to close the scalar no-hair/profile-zero inputs: parent scalar owner, positive operator, source silence, boundary flux, and zero-mode handling; otherwise stage finite scalar profile rows",
            "success_condition": "complete no-hair input pack proves hidden scalar silence, or nonclaim finite profile rows preserve the remaining local scalar channels",
            "do_not": "do not set Xhat=0, boundary flux=0, J_X=0, or positive mass gap by closure/minimality",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1924_0_gain",
            "area": "hidden invariant algebra",
            "summary": "1924 isolates why O(C_hid)^inv=R is not available yet: seven generator debts survive.",
            "status": "BOXED_WITH_SCALAR_ROWS",
            "what_it_means": "the scalar obstruction is now explicit rather than vague",
            "next": "parent scalar no-hair input pack",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1924_1_safety",
            "area": "no-hair discipline",
            "summary": "positive no-hair/profile-zero remains exact only if owner/sign/source/boundary/zero-mode clauses close together.",
            "status": "NOHAIR_ROUTE_UNSIGNED",
            "what_it_means": "we avoid setting local scalar silence by plateau axiom",
            "next": "derive no-hair inputs or source profile rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "triviality_audit": triviality_audit_rows(),
        "generator_rows": generator_rows(),
        "nohair_pack": nohair_pack_rows(),
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
    rows.append({"validation_id": "VAL1924_00_sources", "status": "PASS" if all(r["status"] == "EXISTS_NEEDLES_CONFIRMED" for r in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    audit = parse_csv(OUTPUTS["triviality_audit"])
    verdict = next(r for r in audit if r["audit_id"] == "HIT1924_5_verdict")
    rows.append({"validation_id": "VAL1924_01_triviality_audit", "status": "PASS" if verdict["current_status"] == "NOT_DERIVED_CURRENT_CORPUS_SCALAR_PRIOR_ROWS_STAGED" and all(r["proof_pass"] == "False" for r in audit) else "FAIL", "detail": "hidden invariant triviality remains unsigned", "valid_for_claim": False, "claim_allowed": False})
    generators = parse_csv(OUTPUTS["generator_rows"])
    rows.append({"validation_id": "VAL1924_02_generator_rows", "status": "PASS" if len(generators) == 7 and all(r["status"] == "SOURCE_READY_SCHEMA_ONLY_NONCLAIM" for r in generators) else "FAIL", "detail": "seven surviving scalar generator rows staged", "valid_for_claim": False, "claim_allowed": False})
    nohair = parse_csv(OUTPUTS["nohair_pack"])
    rows.append({"validation_id": "VAL1924_03_nohair_pack", "status": "PASS" if len(nohair) == 6 and any(r["candidate_value"] == "NOHAIR_ROUTE_UNSIGNED" for r in nohair) else "FAIL", "detail": "no-hair input pack remains unsigned", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(r for r in gates if r["gate_id"] == "CG1924_3_local_tests")
    rows.append({"validation_id": "VAL1924_04_claim_gate", "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL", "detail": "hidden invariant route supports no scoring claim", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1924_05_decision", "status": "PASS" if any(r["decision"] == "MOVE_TO_PARENT_SCALAR_NOHAIR_INPUT_PACK" for r in decisions) else "FAIL", "detail": "parent scalar no-hair input pack selected", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1924_06_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1925-Y5-R2FR-parent-scalar-nohair") else "FAIL", "detail": "1925 scalar no-hair route selected", "valid_for_claim": False, "claim_allowed": False})
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
    rows.append({"validation_id": "VAL1924_07_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1924_08_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1924_09_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1924_10_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1924-") or "_1924" in path.name or "1924_" in path.name or "Y5_R2FR_hidden_invariant" in path.name)
    rows.append({"validation_id": "VAL1924_11_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1924_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(r["status"] == "PASS" for r in rows)
    rows.append({"validation_id": "VAL1924_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1924 hidden invariant algebra triviality or scalar prior rows", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(h, "")).replace("\n", " ").replace("|", "\\|") for h in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1924 - Hidden Invariant Algebra Triviality Or Scalar Prior Rows

## Purpose

This checkpoint attacks the root scalar obstruction: prove the hidden/local invariant algebra is trivial, or show exact shift/no-hair/profile-zero removes all nonconstant scalar coefficient maps; otherwise stage scalar-prior rows without claiming a pass.

## Result

- The theorem `O(C_hid)^inv=R => no hidden-visible scalar coefficient maps` remains exact as a conditional.
- The theorem is not derived for the current MTS local branch because surviving generator debts remain live.
- The scalar no-hair route is exact but requires parent owner, positive operator, source silence, boundary flux, and zero-mode handling together.
- Seven scalar generator rows and a six-clause no-hair input pack are staged as nonclaim.
- The next target is a focused parent scalar no-hair input pack or finite scalar profile rows.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Hidden Triviality Audit

{markdown_table(rows_by_name["triviality_audit"])}

## Surviving Scalar Generator Rows

{markdown_table(rows_by_name["generator_rows"])}

## Scalar No-Hair Input Pack

{markdown_table(rows_by_name["nohair_pack"])}

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
