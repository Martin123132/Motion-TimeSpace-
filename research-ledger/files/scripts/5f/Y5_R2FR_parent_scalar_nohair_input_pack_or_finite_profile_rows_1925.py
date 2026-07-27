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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1925"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1925-Y5-R2FR-parent-scalar-nohair-input-pack-or-finite-profile-rows.md"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
GENERATED_UTC = datetime.now(timezone.utc).isoformat()

SOURCES = {
    "1924_next": OUT / "P8_Y5_PARENT_QLOC_1924_NEXT_TARGET.csv",
    "1924_doc": ROOT / "1924-Y5-R2FR-hidden-invariant-algebra-triviality-or-scalar-prior-rows.md",
    "1924_nohair_pack": OUT / "P8_Y5_PARENT_QLOC_1924_SCALAR_NOHAIR_INPUT_PACK_NONCLAIM.csv",
    "1924_claims": OUT / "P8_Y5_PARENT_QLOC_1924_CLAIM_GATE.csv",
    "1924_validation": OUT / "P8_Y5_BRR545_1924_VALIDATION.csv",
    "1092_nohair": OUT / "P8_Y5_R10_1092_SCALAR_NOHAIR_ROUTE_AUDIT.csv",
    "1092_generators": OUT / "P8_Y5_R10_1092_SURVIVING_GENERATOR_LEDGER.csv",
    "1093_owner": OUT / "P8_Y5_R10_1093_PARENT_SCALAR_OWNER_ATTEMPT.csv",
    "1093_operator": OUT / "P8_Y5_R10_1093_POSITIVE_OPERATOR_INPUT_PACK.csv",
    "1093_source": OUT / "P8_Y5_R10_1093_SOURCE_SILENCE_AUDIT.csv",
    "1093_boundary": OUT / "P8_Y5_R10_1093_BOUNDARY_DOMAIN_AUDIT.csv",
    "1093_theorem": OUT / "P8_Y5_R10_1093_CONDITIONAL_NOHAIR_THEOREM.csv",
    "1093_claims": OUT / "P8_Y5_R10_1093_CLAIM_GATES.csv",
    "1022_nohair": OUT / "P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv",
    "1042_identity": OUT / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
    "1042_premises": OUT / "P8_Y5_R10_1042_NOHAIR_PREMISE_GATE.csv",
    "1094_parent_clause": OUT / "P8_Y5_R10_1094_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv",
    "1094_wep_contract": OUT / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv",
    "1094_claims": OUT / "P8_Y5_R10_1094_CLAIM_GATES.csv",
    "1094_next": OUT / "P8_Y5_R10_1094_NEXT_TARGET.csv",
}

NEEDLES = {
    "1924_next": ["NEXT1924_0_primary", "scalar no-hair"],
    "1924_doc": ["NEXT1924_0_primary", "VAL1924_OVERALL"],
    "1924_nohair_pack": ["NHP1924_5_verdict", "NOHAIR_ROUTE_UNSIGNED"],
    "1924_claims": ["CG1924_3_local_tests", "CLAIM_BLOCKED"],
    "1924_validation": ["VAL1924_OVERALL", "formalization_1924_artifact_count=0"],
    "1092_nohair": ["SNH1092_4_verdict", "NOHAIR_ROUTE_UNSIGNED"],
    "1092_generators": ["GEN1092_3_memory_scalar", "GEN1092_6_readout_projector"],
    "1093_owner": ["OWN1093_4_verdict", "PARENT_OWNER_NOT_DERIVED"],
    "1093_operator": ["OP1093_4_verdict", "OPERATOR_PACK_UNSIGNED"],
    "1093_source": ["JX1093_4_verdict", "SOURCE_SILENCE_NOT_DERIVED"],
    "1093_boundary": ["BD1093_0_boundary_flux", "BD1093_3_domain_selector"],
    "1093_theorem": ["THM1093_2_zero_result", "THM1093_4_verdict"],
    "1093_claims": ["CG1093_0_parent_owner", "CG1093_1_positive_nohair"],
    "1022_nohair": ["SNH1022_5_energy_identity", "SNH1022_6_verdict"],
    "1042_identity": ["NH1042_2_positive_zero_theorem", "NH1042_5_verdict"],
    "1042_premises": ["NHP1042_0_LX_owner", "NHP1042_6_verdict"],
    "1094_parent_clause": ["PX1094_3_verdict", "PARENT_ACTION_CLAUSE_NOT_DERIVED"],
    "1094_wep_contract": ["DWP1094_3_direct_product_bound", "MISSING_MTS_DIRECT_PRODUCT"],
    "1094_claims": ["CG1094_1_prediction", "CG1094_2_parent_clause"],
    "1094_next": ["NEXT1094_0_1095", "parent Xhat matter-response clause"],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1925_SOURCE_REGISTER.csv",
    "proof_audit": OUT / "P8_Y5_PARENT_QLOC_1925_SCALAR_NOHAIR_INPUT_PROOF_AUDIT.csv",
    "finite_profile": OUT / "P8_Y5_PARENT_QLOC_1925_FINITE_SCALAR_PROFILE_ROWS_NONCLAIM.csv",
    "source_boundary": OUT / "P8_Y5_PARENT_QLOC_1925_SOURCE_BOUNDARY_ZERO_MODE_LEDGER.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1925_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1925_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1925_NEXT_TARGET.csv",
    "snapshot": OUT / "P8_Y5_PARENT_QLOC_1925_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1925_VALIDATION.csv",
}

BRANCH_COPIES = [
    (OUTPUTS["proof_audit"], SOURCE_WEIGHT_DOCS / "SCALAR_NOHAIR_INPUT_PROOF_AUDIT_1925_NONCLAIM.csv"),
    (OUTPUTS["finite_profile"], MICROSCOPE_COEFFS / "P8_Y5_PARENT_QLOC_1925_FINITE_SCALAR_PROFILE_ROWS_NONCLAIM.csv"),
    (OUTPUTS["finite_profile"], QUEUE / "JR1925_SCALAR_PROFILE_ACQUISITION_QUEUE.csv"),
    (OUTPUTS["claim_gate"], QUARANTINE / "P8_Y5_PARENT_QLOC_1925_CLAIM_GATE.csv"),
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
                "needed_for": "1925 parent scalar no-hair input pack or finite profile rows",
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
            "audit_id": "SNP1925_0_target",
            "clause": "complete scalar no-hair/profile-zero theorem",
            "mathematical_statement": "Parent-owned Xhat obeys a positive self-adjoint local operator with J_X=0, zero boundary flux, and no non-quotient zero mode.",
            "source_anchor": "NEXT1924_0_primary; NH1042_2_positive_zero_theorem",
            "current_status": "TARGET_SHARP",
            "missing_for_claim": "all input clauses must be signed in the same parent action",
            "theorem_use": "contract target only",
            "conditional_math_valid": False,
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNP1925_1_parent_owner",
            "clause": "parent scalar owner",
            "mathematical_statement": "The same Xhat must control visible coefficients and be the field varied in L_X Xhat=J_X.",
            "source_anchor": "OWN1093_4_verdict; PX1094_0_field_owner",
            "current_status": "PARENT_OWNER_NOT_DERIVED",
            "missing_for_claim": "Xhat is still not identified as a parent-normalized field rather than closure notation",
            "theorem_use": "blocks promotion",
            "conditional_math_valid": False,
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNP1925_2_positive_operator",
            "clause": "positive operator and local domain",
            "mathematical_statement": "Z_X>=Z_min>0, M_X^2>=m_min^2>0, and self-adjoint local boundary/domain data make the energy identity positive.",
            "source_anchor": "OP1093_4_verdict; NHP1042_0_LX_owner; NHP1042_6_verdict",
            "current_status": "OPERATOR_PACK_UNSIGNED",
            "missing_for_claim": "parent L_X, kinetic sign, mass gap, and self-adjoint domain are formula/template rows only",
            "theorem_use": "blocks promotion",
            "conditional_math_valid": False,
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNP1925_3_source_silence",
            "clause": "ordinary/local source silence",
            "mathematical_statement": "J_X must vanish channelwise for ordinary matter, alpha/EM response, WEP source/test projection, R10 projection, and readout/domain terms.",
            "source_anchor": "JX1093_4_verdict; SNH1022_3_source_zero",
            "current_status": "SOURCE_SILENCE_NOT_DERIVED",
            "missing_for_claim": "matter quotient/no-marker, alpha owner, WEP/R10 projection, and readout silence are not parent-signed",
            "theorem_use": "blocks promotion",
            "conditional_math_valid": False,
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNP1925_4_boundary_zero_mode",
            "clause": "boundary flux, zero-mode, and readout/domain lock",
            "mathematical_statement": "Phi_boundary_local=0 and ker(L_X) contains only quotient/proper modes fixed by boundary/reference data.",
            "source_anchor": "BD1093_0_boundary_flux; BD1093_1_zero_mode; BD1093_3_domain_selector",
            "current_status": "BOUNDARY_AND_ZERO_MODE_GATES_OPEN",
            "missing_for_claim": "boundary flux zero, topology kernel closure, and after-variation readout theorem remain unsigned",
            "theorem_use": "blocks promotion",
            "conditional_math_valid": False,
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNP1925_5_conditional_identity",
            "clause": "positive energy identity",
            "mathematical_statement": "int_A[Z_X|grad Xhat|^2+M_X^2 Xhat^2+positive_mix]=int_A Xhat J_X+Phi_boundary_local.",
            "source_anchor": "THM1093_2_zero_result; NH1042_1_energy_identity; SNH1022_5_energy_identity",
            "current_status": "EXACT_CONDITIONAL_THEOREM_RETAINED",
            "missing_for_claim": "the identity becomes a local-GR theorem only after SNP1925_1 through SNP1925_4 pass together",
            "theorem_use": "keep as future parent-action contract",
            "conditional_math_valid": True,
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "SNP1925_6_verdict",
            "clause": "1925 scalar no-hair input-pack verdict",
            "mathematical_statement": "The full scalar no-hair/profile-zero input pack is not derived in the current corpus; finite profile rows must remain live.",
            "source_anchor": "SNP1925_1_parent_owner through SNP1925_5_conditional_identity",
            "current_status": "NOT_DERIVED_CURRENT_CORPUS_FINITE_PROFILE_ROWS_STAGED",
            "missing_for_claim": "parent owner, signed positive operator, source silence, boundary flux zero, zero-mode handling, and readout/domain lock",
            "theorem_use": "no local-GR/WEP/R10/clock claim",
            "conditional_math_valid": False,
            "proof_pass": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def finite_profile_rows() -> list[dict[str, Any]]:
    specs = [
        ("FSP1925_0_Xhat_profile_amplitude", "local Xhat amplitude", "A_X_local", "amplitude of retained scalar profile on local exterior A", "MISSING_PROFILE_AMPLITUDE_OR_ZERO_THEOREM", "same as Xhat", "zero theorem or source-backed local profile amplitude"),
        ("FSP1925_1_grad_Xhat_norm", "local Xhat gradient norm", "||nabla Xhat||_A", "gradient residue that feeds fifth-force, clock, or PPN channels", "MISSING_GRADIENT_BOUND_OR_ZERO_THEOREM", "Xhat per length", "gradient zero theorem or numeric upper bound"),
        ("FSP1925_2_MX_gap", "scalar mass/gap", "M_X^2", "range-setting operator gap for finite scalar exchange", "MISSING_SIGNED_GAP", "length^-2 in c=hbar=1 or parent-normalized", "parent Hessian sign and range lambda_X"),
        ("FSP1925_3_JX_matter", "ordinary matter scalar source", "J_X^matter", "source term that can force Xhat even with positive operator", "MISSING_SOURCE_SILENCE_OR_BOUND", "action density per Xhat", "parent source-zero theorem or source-current bound"),
        ("FSP1925_4_boundary_flux", "local boundary flux", "Phi_boundary_local", "surface term that can inject hidden scalar hair into the lab exterior", "MISSING_BOUNDARY_ZERO_OR_BOUND", "action flux", "boundary condition theorem or numeric surface-flux bound"),
        ("FSP1925_5_zero_mode", "kernel/topology residual", "C_zero_mode", "flat/topological/gauge zero mode left after positive identity", "MISSING_ZERO_MODE_CLASSIFICATION", "dimensionless or topological class label", "kernel quotient/proper classification"),
        ("FSP1925_6_tau_clock_profile", "clock projection of Xhat profile", "tau_clock_time*dXhat", "local scalar drift projected into clock/alpha observables", "MISSING_CLOCK_PROFILE_PROJECTION", "yr^-1 or observer-normalized", "source-backed clock projection or theorem-zero"),
        ("FSP1925_7_tau_WEP_R10_profile", "WEP/R10 profile projection", "tau_WEP/tau_R10 local profile", "source/test projection for MICROSCOPE and short-range R10 arenas", "MISSING_WEP_R10_PROFILE_PROJECTION", "dimensionless and range-dependent", "direct product row or parent projection theorem"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": row_id,
            "profile_object": profile_object,
            "symbol": symbol,
            "role": role,
            "candidate_value": candidate_value,
            "units": units,
            "source_path": "MISSING_PARENT_PROFILE_OR_BOUND_SOURCE",
            "source_row_id": "MISSING_SOURCE_ROW_ID",
            "required_to_score": required_to_score,
            "status": "SOURCE_READY_SCHEMA_ONLY_NONCLAIM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for row_id, profile_object, symbol, role, candidate_value, units, required_to_score in specs
    ]


def source_boundary_rows() -> list[dict[str, Any]]:
    specs = [
        ("SBZ1925_0_parent_owner", "parent Xhat owner", "same Xhat in visible coefficients and L_X equation", "MISSING_PARENT_OWNER", "OWN1093_4_verdict; PX1094_0_field_owner", "no-hair may silence the wrong coordinate", "retain A_X_local and direct product rows"),
        ("SBZ1925_1_positive_operator", "positive operator", "Z_X, M_X^2, and self-adjoint domain signed by parent action", "MISSING_SIGNED_OPERATOR", "OP1093_4_verdict; NHP1042_6_verdict", "energy identity is not claim-grade", "retain M_X^2 and lambda_X source rows"),
        ("SBZ1925_2_source_silence", "source silence", "J_X=0 for matter, EM, WEP, R10, clock, and readout channels", "SOURCE_SILENCE_NOT_DERIVED", "JX1093_4_verdict; PX1094_1_matter_response", "ordinary matter can force a finite scalar profile", "retain source-current/direct-product rows"),
        ("SBZ1925_3_boundary_flux", "boundary flux", "Phi_boundary_local=0 or source-backed upper bound", "BOUNDARY_FLUX_ZERO_NOT_DERIVED", "BD1093_0_boundary_flux; NHP1042_4_boundary_flux_zero", "boundary can carry hidden scalar hair into the lab exterior", "retain Phi_boundary_local row"),
        ("SBZ1925_4_zero_mode", "zero-mode closure", "no topological/gauge zero mode outside quotient/proper kernel", "TOPOLOGY_KERNEL_GATE_OPEN", "BD1093_1_zero_mode; NHP1042_5_no_zero_mode", "positive identity may leave flat/topological hair", "retain C_zero_mode row"),
        ("SBZ1925_5_domain_readout", "domain/readout lock", "domain selector and readout projector act after variation and cannot source Xhat", "NO_CHEAT_RULE_ONLY", "BD1093_3_domain_selector; GEN1092_6_readout_projector", "projector can sneak back in as an effective source", "retain readout/domain source rows"),
        ("SBZ1925_6_direct_WEP_source", "direct WEP source product", "parent-projected P_WEP_alpha_direct is zero or numeric", "MISSING_DIRECT_PRODUCT", "DWP1094_3_direct_product_bound; DWP1094_4_required_prediction", "MICROSCOPE has a threshold but no MTS prediction row", "derive parent action clause or stage numeric product source fields"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "ledger_id": ledger_id,
            "channel": channel,
            "needed_clause": needed_clause,
            "current_status": current_status,
            "source_anchor": source_anchor,
            "why_blocks_nohair": why_blocks_nohair,
            "finite_fallback": finite_fallback,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
        for ledger_id, channel, needed_clause, current_status, source_anchor, why_blocks_nohair, finite_fallback in specs
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1925_0_parent_owner",
            "requirement": "parent-owned scalar Xhat controls visible coefficients and no-hair operator",
            "status": "FAIL_PARENT_OWNER_NOT_DERIVED",
            "evidence": "SNP1925_1_parent_owner; OWN1093_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1925_1_positive_input_pack",
            "requirement": "positive self-adjoint operator, signed gap, and domain",
            "status": "FAIL_OPERATOR_PACK_UNSIGNED",
            "evidence": "SNP1925_2_positive_operator; OP1093_4_verdict",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1925_2_source_boundary_zero_mode",
            "requirement": "J_X=0, Phi_boundary=0, no zero mode, no readout/domain source",
            "status": "FAIL_SOURCE_BOUNDARY_ZERO_MODE_GATES_OPEN",
            "evidence": "SNP1925_3_source_silence; SNP1925_4_boundary_zero_mode",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1925_3_finite_profile_rows",
            "requirement": "finite scalar profile rows are numeric, sourced, and score-ready",
            "status": "FAIL_ROWS_SCHEMA_ONLY",
            "evidence": "FSP1925_0_Xhat_profile_amplitude through FSP1925_7_tau_WEP_R10_profile",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1925_4_local_claims",
            "requirement": "local-GR/WEP/R10/clock claim",
            "status": "CLAIM_BLOCKED",
            "evidence": "CG1925_0_parent_owner; CG1925_1_positive_input_pack; CG1925_2_source_boundary_zero_mode; CG1925_3_finite_profile_rows",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1925_0_input_pack_result",
            "decision": "SCALAR_NOHAIR_INPUT_PACK_NOT_DERIVED",
            "why": "the exact positive identity is available only as a conditional; the parent owner, signed operator, source silence, boundary flux, and zero-mode clauses do not close together",
            "next_action": "keep finite scalar profile rows live and attack the parent action/source-product owner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1925_1_finite_branch",
            "decision": "FINITE_SCALAR_PROFILE_ROWS_STAGED",
            "why": "without no-hair promotion, A_X_local, grad Xhat, M_X^2, J_X, boundary flux, zero mode, and tau projections must be bounded or sourced",
            "next_action": "turn the most constrained projection into a direct product row rather than splitting placeholders",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1925_2_next_route",
            "decision": "MOVE_TO_DIRECT_WEP_PRODUCT_SOURCE_PACK",
            "why": "1094 already has a private MICROSCOPE product threshold; the missing piece is the parent Xhat matter-response clause or one numeric MTS direct product row",
            "next_action": "1926 should derive parent Xhat matter response or stage direct WEP/R10/clock product source fields with no claim",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1925_0_primary",
            "selection_status": "selected",
            "target_doc": "1926-Y5-R2FR-direct-WEP-product-source-pack-or-parent-Xhat-action-clause.md",
            "target_script": "scripts/Y5_R2FR_direct_WEP_product_source_pack_or_parent_Xhat_action_clause_1926.py",
            "objective": "derive the parent Xhat matter-response clause that theorem-zeros local source products or yields a numeric direct WEP/R10/clock scalar product; otherwise stage exact nonclaim source fields",
            "success_condition": "a parent-signed zero theorem or one numeric, sourced, observed-frame direct product row",
            "do_not": "do not split into beta/tau placeholders without sourced owners; do not set tau_WEP=1; do not claim local-GR/WEP/R10/clock pass",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        }
    ]


def snapshot_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1925_0_gain",
            "area": "local GR derivation route",
            "summary": "1925 turns the local plateau/no-hair idea into an exact contract: it works only if owner, sign, source, boundary, and zero-mode clauses close together.",
            "status": "CONTRACT_EXACT_CLAIM_BLOCKED",
            "what_it_means": "we are not smuggling local scalar silence by axiom",
            "next": "parent matter-response/direct product owner",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1925_1_missing",
            "area": "finite scalar branch",
            "summary": "Eight finite scalar profile rows now name the exact quantities that must be theorem-zeroed or empirically bounded.",
            "status": "SCHEMA_ONLY_NONCLAIM",
            "what_it_means": "future tests have named knobs instead of vague hidden hair",
            "next": "source one direct product row or derive the parent action clause",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
        {
            "branch_id": BRANCH_ID,
            "snapshot_id": "STAT1925_2_best_route",
            "area": "next empirical bridge",
            "summary": "The cleanest next route is the direct WEP product: MICROSCOPE gives a threshold, but MTS still needs a parent-projected prediction.",
            "status": "NEXT_ROUTE_SELECTED",
            "what_it_means": "we move from abstract no-hair failure to a scoreable local source-product contract",
            "next": "1926 direct WEP product source pack",
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": GENERATED_UTC,
        },
    ]


def build_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "proof_audit": proof_audit_rows(),
        "finite_profile": finite_profile_rows(),
        "source_boundary": source_boundary_rows(),
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
    rows.append({"validation_id": "VAL1925_00_sources", "status": "PASS" if all(row["status"] == "EXISTS_NEEDLES_CONFIRMED" for row in sources) else "FAIL", "detail": "all local source paths exist and needles found", "valid_for_claim": False, "claim_allowed": False})
    proof = parse_csv(OUTPUTS["proof_audit"])
    verdict = next(row for row in proof if row["audit_id"] == "SNP1925_6_verdict")
    rows.append({"validation_id": "VAL1925_01_input_pack_verdict", "status": "PASS" if verdict["current_status"] == "NOT_DERIVED_CURRENT_CORPUS_FINITE_PROFILE_ROWS_STAGED" and all(row["proof_pass"] == "False" for row in proof) else "FAIL", "detail": "complete scalar no-hair input pack is not promoted", "valid_for_claim": False, "claim_allowed": False})
    identity = next(row for row in proof if row["audit_id"] == "SNP1925_5_conditional_identity")
    rows.append({"validation_id": "VAL1925_02_conditional_identity", "status": "PASS" if identity["conditional_math_valid"] == "True" and identity["current_status"] == "EXACT_CONDITIONAL_THEOREM_RETAINED" else "FAIL", "detail": "positive no-hair identity retained as contract only", "valid_for_claim": False, "claim_allowed": False})
    finite = parse_csv(OUTPUTS["finite_profile"])
    rows.append({"validation_id": "VAL1925_03_finite_profile_rows", "status": "PASS" if len(finite) == 8 and all(row["status"] == "SOURCE_READY_SCHEMA_ONLY_NONCLAIM" for row in finite) else "FAIL", "detail": "eight finite scalar profile rows staged", "valid_for_claim": False, "claim_allowed": False})
    source_boundary = parse_csv(OUTPUTS["source_boundary"])
    blocked_markers = ["MISSING_PARENT_OWNER", "MISSING_SIGNED_OPERATOR", "SOURCE_SILENCE_NOT_DERIVED", "BOUNDARY_FLUX_ZERO_NOT_DERIVED", "TOPOLOGY_KERNEL_GATE_OPEN", "MISSING_DIRECT_PRODUCT"]
    rows.append({"validation_id": "VAL1925_04_source_boundary_ledger", "status": "PASS" if all(any(row["current_status"] == marker for row in source_boundary) for marker in blocked_markers) else "FAIL", "detail": "source, boundary, zero-mode, and product gates remain explicit", "valid_for_claim": False, "claim_allowed": False})
    gates = parse_csv(OUTPUTS["claim_gate"])
    local_gate = next(row for row in gates if row["gate_id"] == "CG1925_4_local_claims")
    rows.append({"validation_id": "VAL1925_05_claim_gate", "status": "PASS" if local_gate["status"] == "CLAIM_BLOCKED" else "FAIL", "detail": "local-GR/WEP/R10/clock claims remain blocked", "valid_for_claim": False, "claim_allowed": False})
    decisions = parse_csv(OUTPUTS["decision"])
    rows.append({"validation_id": "VAL1925_06_decision", "status": "PASS" if any(row["decision"] == "MOVE_TO_DIRECT_WEP_PRODUCT_SOURCE_PACK" for row in decisions) else "FAIL", "detail": "direct WEP product source pack selected", "valid_for_claim": False, "claim_allowed": False})
    next_rows = parse_csv(OUTPUTS["next_target"])
    rows.append({"validation_id": "VAL1925_07_next_target", "status": "PASS" if next_rows[0]["target_doc"].startswith("1926-Y5-R2FR-direct-WEP-product") else "FAIL", "detail": "1926 direct product route selected", "valid_for_claim": False, "claim_allowed": False})
    generated = [path for key, path in OUTPUTS.items() if key != "validation"]
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
    rows.append({"validation_id": "VAL1925_08_claim_flags_safe", "status": "PASS" if claim_safe else "FAIL", "detail": "claim flags all false", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1925_09_csv_parse", "status": "PASS" if csv_ok else "FAIL", "detail": "all generated CSVs parse with rows", "valid_for_claim": False, "claim_allowed": False})
    rows.append({"validation_id": "VAL1925_10_branch_copies", "status": "PASS" if all(destination.exists() for _, destination in BRANCH_COPIES) else "FAIL", "detail": "; ".join(str(destination) for _, destination in BRANCH_COPIES), "valid_for_claim": False, "claim_allowed": False})
    pycache = ROOT / "scripts" / "__pycache__"
    rows.append({"validation_id": "VAL1925_11_pycache_absent", "status": "PASS" if not pycache.exists() else "FAIL", "detail": str(pycache), "valid_for_claim": False, "claim_allowed": False})
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_count = sum(1 for path in FORMALIZATION.rglob("*") if path.name.startswith("1925-") or "_1925" in path.name or "1925_" in path.name or "Y5_R2FR_parent_scalar_nohair" in path.name)
    rows.append({"validation_id": "VAL1925_12_formalization_untouched", "status": "PASS" if formalization_count == 0 else "FAIL", "detail": f"formalization_1925_artifact_count={formalization_count}", "valid_for_claim": False, "claim_allowed": False})
    overall = all(row["status"] == "PASS" for row in rows)
    rows.append({"validation_id": "VAL1925_OVERALL", "status": "PASS" if overall else "FAIL", "detail": "1925 parent scalar no-hair input pack or finite profile rows", "valid_for_claim": False, "claim_allowed": False})
    return rows


def markdown_table(rows: list[dict[str, Any]]) -> str:
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = validation_rows()
    content = f"""# 1925 - Parent Scalar No-Hair Input Pack Or Finite Profile Rows

## Purpose

This checkpoint tries the derivation route first: promote the scalar no-hair/profile-zero identity into a parent-signed local-GR mechanism. If any required clause is unsigned, it stages finite scalar profile rows instead of smuggling in a local plateau axiom.

## Result

- The positive no-hair identity remains mathematically exact as a conditional contract.
- It is not promoted for the current MTS branch because parent owner, positive operator, source silence, boundary flux, zero-mode, and readout/domain clauses do not close together.
- Eight finite scalar profile rows are staged as nonclaim: amplitude, gradient, gap, matter source, boundary flux, zero mode, clock projection, and WEP/R10 projection.
- The local-GR/WEP/R10/clock claims stay blocked.
- The next target is a direct WEP product source pack or parent Xhat matter-response action clause.

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Scalar No-Hair Input Proof Audit

{markdown_table(rows_by_name["proof_audit"])}

## Finite Scalar Profile Rows

{markdown_table(rows_by_name["finite_profile"])}

## Source Boundary Zero-Mode Ledger

{markdown_table(rows_by_name["source_boundary"])}

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
