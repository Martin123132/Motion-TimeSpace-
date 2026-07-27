from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R2FR_MASS_SECTOR_BMHAT_OWNER_OR_WEP_NUCLEAR_BINDING_GAP_2442"
CHECKPOINT_ID = "2442"

ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

DOC = ROOT / "2442-Y5-R2FR-mass-sector-bmhat-owner-or-WEP-nuclear-binding-gap.md"

ETA_MICROSCOPE_1SIGMA = 2.745906e-15
DELTA_Q_MHAT_PT_MINUS_TI = 3.33e-3
DELTA_Q_E_PT_MINUS_TI = 2.04e-3

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2442_SOURCE_REGISTER.csv",
    "zero_theorem": OUT / "P8_Y5_PARENT_QLOC_2442_MASS_ZERO_THEOREM_ATTEMPT.csv",
    "owner_audit": OUT / "P8_Y5_PARENT_QLOC_2442_MATTER_SPECTRUM_OWNER_AUDIT.csv",
    "coefficient_ledger": OUT / "P8_Y5_PARENT_QLOC_2442_BMHAT_BNUC_COEFFICIENT_LEDGER.csv",
    "wep_projection": OUT / "P8_Y5_PARENT_QLOC_2442_WEP_NUCLEAR_BINDING_PROJECTION.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2442_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_PARENT_QLOC_2442_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2442_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2442_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2442_VALIDATION.csv",
}

COPY_TARGETS = {
    "queue_zero_theorem": QUEUE / "JR2442_MASS_ZERO_THEOREM_ATTEMPT_NONCLAIM.csv",
    "queue_coefficients": QUEUE / "JR2442_BMHAT_BNUC_COEFFICIENT_LEDGER_NONCLAIM.csv",
    "branch_wep_projection": MICROSCOPE / "WEP_nuclear_binding_projection_nonclaim_2442.csv",
    "beta_docs_mass_owner": BETA_DOCS / "MASS_SECTOR_OWNER_AUDIT_2442_NONCLAIM.csv",
}

SOURCES = [
    {
        "source_id": "SRC2442_00_2441_handoff",
        "source_path": ROOT / "2441-Y5-R2FR-MTS-to-DD-charge-map-or-WEP-source-leg-owner.md",
        "needles": [
            "NEXT2441_0_selected",
            "DDMAP2441_1_missing_b_mhat",
            "WRF2441_0_reduced_DD_MTS",
            "VAL2441_OVERALL",
        ],
        "role": "fresh handoff selecting mass-sector owner or WEP nuclear-binding gap",
    },
    {
        "source_id": "SRC2442_01_2440_material_sensitivity",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_MATERIAL_SENSITIVITY_BASIS.csv",
        "needles": ["WMS2440_2_Pt_minus_Ti", "3.330000e-03", "2.040000e-03"],
        "role": "source-backed Ti/Pt Damour-Donoghue material contrast factors",
    },
    {
        "source_id": "SRC2442_02_2440_wep_projection",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2440_WEP_K_VECTOR_PROJECTION.csv",
        "needles": ["D_mhat_source", "D_e_source", "eta_bound_1sigma=2.745906e-15"],
        "role": "current WEP K-vector formula and bound scale",
    },
    {
        "source_id": "SRC2442_03_1805_doc",
        "source_path": ROOT / "1805-Y5-R2FR-no-extra-F2-no-mass-vertex-signature-or-alpha-mass-bound-matrix.md",
        "needles": ["No-Mass-Vertex Theorem Attempt", "MVT1805_4_verdict", "VT1805_5_binding_X"],
        "role": "current-branch precedent for the no-mass-vertex theorem attempt",
    },
    {
        "source_id": "SRC2442_04_1805_no_mass_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1805_NO_MASS_VERTEX_THEOREM_ATTEMPT.csv",
        "needles": ["MVT1805_0_fixed_rep_spectrum", "MVT1805_2_binding_response", "FAIL_CURRENT_CLAIM_RETAIN_MASS_CLOCK_MATRIX"],
        "role": "machine-readable no-mass-vertex theorem status",
    },
    {
        "source_id": "SRC2442_05_1805_vertex_csv",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_1805_ALLOWED_FORBIDDEN_VERTEX_TABLE.csv",
        "needles": ["VT1805_3_mass_X", "VT1805_4_yukawa_X", "VT1805_5_binding_X"],
        "role": "dangerous mass, Yukawa and binding vertices still legal unless parent-forbidden",
    },
    {
        "source_id": "SRC2442_06_1047_mass_precedent",
        "source_path": ROOT / "1047-Y5-R10-constant-superselection-alpha-mass-clock-theorem-or-coefficient-provenance.md",
        "needles": ["MRS1047_4_verdict", "CP1047_2_b_mA", "CG1047_1_mass_zero"],
        "role": "older mass-ratio audit retaining b_mA because matter spectrum is not parent-derived",
    },
    {
        "source_id": "SRC2442_07_1098_owner_signature",
        "source_path": ROOT / "1098-Y5-R10-ordinary-constant-owner-action-signature-or-source-backed-coefficient-prior.md",
        "needles": ["OCS1098_2_matter_spectrum_owner", "FV1098_4_binding_X", "OCT1098_3_verdict"],
        "role": "older ordinary-sector owner signature showing mass/binding vertices remain live",
    },
    {
        "source_id": "SRC2442_08_1104_signature_ledger",
        "source_path": ROOT / "1104-Y5-R10-parent-ordinary-sector-action-signature-or-explicit-closure-ledger.md",
        "needles": ["SIG1104_2_matter_spectrum_owner", "THM1104_2_counterexample_if_any_clause_missing", "DEC1104_0_signature_status"],
        "role": "ordinary-sector action signature ledger with explicit mass/binding counterexample",
    },
]


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def base_row(**kwargs: Any) -> dict[str, Any]:
    row = {
        "timestamp_utc": timestamp(),
        "branch_id": BRANCH_ID,
        "checkpoint_id": CHECKPOINT_ID,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    row.update(kwargs)
    return row


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(row.get(key, "")) for key in fields})


def csv_parses(path: Path) -> tuple[bool, int, str]:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        return True, len(rows), "OK"
    except Exception as exc:
        return False, 0, f"{type(exc).__name__}: {exc}"


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = [stringify(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        needles = source["needles"]
        found = [needle for needle in needles if needle in text]
        rows.append(
            base_row(
                source_id=source["source_id"],
                source_path=path,
                path_exists=path.exists(),
                required_needles="; ".join(needles),
                found_needles="; ".join(found),
                needles_found=path.exists() and len(found) == len(needles),
                role=source["role"],
            )
        )
    return rows


def zero_theorem_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "theorem_id": "MZT2442_0_setup",
            "claim_piece": "mass-sector vertical silence setup",
            "mathematical_form": "q: ParentFields -> quotient variables; v in ker(Dq); theta_matter = theta_rep or theta_bar(q(Phi))",
            "proof_step": "For any dimensionless matter parameter theta_A that factors through q or a fixed representation label, Lie_v theta_A = d theta_bar(Dq[v]) = 0.",
            "current_status": "EXACT_CONDITIONAL",
            "missing_for_claim": "parent action must sign full matter-spectrum owner and no hidden mass/binding/readout vertices",
            "if_missing": "b_mhat, b_mu, b_nuc and b_bind remain live residual coefficients",
            "theorem_proven_conditionally": True,
        },
        {
            "theorem_id": "MZT2442_1_fixed_mass_ratios",
            "claim_piece": "b_mu and b_mhat vanish under fixed representation spectrum",
            "mathematical_form": "b_mhat := Lie_v ln(mhat/Lambda_QCD); b_mu := Lie_v ln(m_e/m_p)",
            "proof_step": "If Yukawa/Higgs/QCD scales and observable mass ratios are representation or quotient data, their logarithmic vertical derivatives vanish.",
            "current_status": "EXACT_CONDITIONAL",
            "missing_for_claim": "MISSING_PARENT_DERIVATION_OF_ELECTRON_PROTON_LIGHT_QUARK_QCD_SPECTRUM",
            "if_missing": "composition-dependent WEP/R10 and clock mass channels stay live",
            "theorem_proven_conditionally": True,
        },
        {
            "theorem_id": "MZT2442_2_fixed_binding_response",
            "claim_piece": "b_nuc and b_bind vanish under quotient-owned binding functions",
            "mathematical_form": "b_bind,A := Lie_v ln(B_A/m_A); beta_A := partial ln m_A / partial q_matter",
            "proof_step": "If nuclear binding fractions and material response functions are theta_bar(q,Rep_A), vertical motion invisible to q cannot change them.",
            "current_status": "EXACT_CONDITIONAL",
            "missing_for_claim": "MISSING_BINDING_DECOMPOSITION_AND_NO_MATERIAL_MARKER_VERTEX",
            "if_missing": "Ti/Pt WEP channel cannot be treated as alpha-only",
            "theorem_proven_conditionally": True,
        },
        {
            "theorem_id": "MZT2442_3_counterterm",
            "claim_piece": "current corpus allows mass/binding countervertices",
            "mathematical_form": "DeltaS = int mu_obs [m_A(Xhat) psi_bar_A psi_A + y_A(Xhat) psi_A H psi_B + B_A(Xhat) O_bind,A]",
            "proof_step": "These terms are local scalar operators unless the parent object language or symmetry forbids hidden-to-visible coefficient morphisms.",
            "current_status": "COUNTERMODEL_ACTIVE",
            "missing_for_claim": "MISSING_OPERATOR_CLASSIFICATION_OR_NO_HIDDEN_VISIBLE_COEFFICIENT_MORPHISM",
            "if_missing": "zero theorem is not promoted in the actual framework",
            "theorem_proven_conditionally": False,
        },
        {
            "theorem_id": "MZT2442_4_verdict",
            "claim_piece": "mass-sector zero theorem promotion",
            "mathematical_form": "MZT2442_0 + MZT2442_1 + MZT2442_2 + no-counterterm/no-readout closure => b_mhat=b_mu=b_nuc=b_bind=0",
            "proof_step": "The theorem is mathematically clean as a contract, but not parent-signed by the current corpus.",
            "current_status": "FAIL_CURRENT_CLAIM_RETAIN_MASS_BINDING_COEFFICIENTS",
            "missing_for_claim": "MISSING_PARENT_MATTER_SPECTRUM_OWNER; MISSING_NO_MASS_VERTEX; MISSING_BINDING_RESPONSE_OWNER; MISSING_SOURCE_LEG",
            "if_missing": "build explicit nonclaim coefficient rows and keep WEP/local-GR blocked",
            "theorem_proven_conditionally": False,
        },
    ]
    return [base_row(**row) for row in rows]


def owner_audit_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "audit_id": "MSO2442_0_parent_domain",
            "owner_clause": "ordinary matter action object language declared before fitting local tests",
            "required_form": "S_matter = Sbar_matter[q(Phi), Psi, theta_rep] with explicit allowed local operators",
            "evidence_status": "PARTIAL_CONTRACT_ONLY",
            "blocks": "post-hoc mass/binding coefficient functions remain legal",
            "gap_class": "MISSING_PARENT_SIGNATURE",
            "gate_pass": False,
        },
        {
            "audit_id": "MSO2442_1_mass_ratios",
            "owner_clause": "dimensionless mass ratios are quotient-owned or representation-superselected",
            "required_form": "m_A/m_B = f_AB(q,Rep_A,Rep_B) or fixed representation data",
            "evidence_status": "NOT_PARENT_DERIVED",
            "blocks": "b_mhat and b_mu cannot be zeroed",
            "gap_class": "MISSING_MATTER_SPECTRUM_OWNER",
            "gate_pass": False,
        },
        {
            "audit_id": "MSO2442_2_yukawa_qcd",
            "owner_clause": "Yukawa, Higgs and QCD scale response has no hidden coefficient slot",
            "required_form": "no y_A(Xhat), m_A(Xhat), Lambda_QCD(Xhat) or hidden-visible coefficient morphism",
            "evidence_status": "COUNTERVERTEX_LEGAL",
            "blocks": "mass-sector vertical leakage survives even if metric descent works",
            "gap_class": "MISSING_NO_MASS_VERTEX_RULE",
            "gate_pass": False,
        },
        {
            "audit_id": "MSO2442_3_binding_response",
            "owner_clause": "nuclear/EM binding response descends from the same owned constants",
            "required_form": "B_A(Phi)=Bbar_A(q(Phi),theta_rep,Rep_A) and no B_A(Xhat), beta_A(Xhat)",
            "evidence_status": "UNSIGNED",
            "blocks": "b_nuc, b_bind and beta_A stay live in WEP/R10/clocks",
            "gap_class": "MISSING_BINDING_RESPONSE_OWNER",
            "gate_pass": False,
        },
        {
            "audit_id": "MSO2442_4_source_leg",
            "owner_clause": "Earth/source vertical drive leg is derived once and shared across local arenas",
            "required_form": "S_E^q = P_source[q, J_E, screen] with fixed q normalization",
            "evidence_status": "MISSING",
            "blocks": "coefficient slopes cannot become WEP source charges",
            "gap_class": "MISSING_SOURCE_LEG",
            "gate_pass": False,
        },
        {
            "audit_id": "MSO2442_5_readout_radiative",
            "owner_clause": "tree-level matter silence survives effective, material and clock readout reduction",
            "required_form": "renormalized mass/binding/clock observables factor through the same quotient owner",
            "evidence_status": "UNSIGNED",
            "blocks": "local experiments can see readout residuals even if parent action looks silent",
            "gap_class": "MISSING_READOUT_CLOSURE",
            "gate_pass": False,
        },
        {
            "audit_id": "MSO2442_6_verdict",
            "owner_clause": "mass-sector q-blindness is parent-signed",
            "required_form": "all MSO2442_0 through MSO2442_5 clauses pass",
            "evidence_status": "BLOCKED_RETAIN_COEFFICIENTS",
            "blocks": "WEP/local-GR branch remains nonclaim",
            "gap_class": "MASS_OWNER_NOT_CLOSED",
            "gate_pass": False,
        },
    ]
    return [base_row(**row) for row in rows]


def coefficient_ledger_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "coefficient_id": "BML2442_0_b_mhat",
            "symbol": "b_mhat",
            "definition": "Lie_v ln(mhat/Lambda_QCD) or equivalent DD light-quark mass channel slope with respect to q",
            "units": "q^-1 or dimensionless per normalized q",
            "feeds": "D_mhat_source; WEP Ti/Pt mass charge; R10 source/test qbar; clock mass-ratio rows",
            "source_or_theorem_needed": "parent matter-spectrum owner theorem or source-backed MTS-to-DD projection coefficient",
            "current_status": "RETAIN_NONCLAIM",
            "single_component_smoke_bound": f"|S_E^q*b_mhat| <= {ETA_MICROSCOPE_1SIGMA / DELTA_Q_MHAT_PT_MINUS_TI:.6e} if all other WEP channels vanish",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "BML2442_1_b_mu",
            "symbol": "b_mu",
            "definition": "Lie_v ln(m_e/m_p) or clock/R10-relevant dimensionless mass-ratio slope",
            "units": "q^-1 or dimensionless per normalized q",
            "feeds": "clock frequency ratios; material standards; possible R10 source normalization",
            "source_or_theorem_needed": "matter-spectrum owner and clock/material readout map",
            "current_status": "RETAIN_NONCLAIM",
            "single_component_smoke_bound": "not scored from Ti/Pt WEP alone without K_mu/material sensitivity",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "BML2442_2_b_nuc",
            "symbol": "b_nuc",
            "definition": "Lie_v nuclear response coefficient after separating quark-mass, QCD and EM binding pieces",
            "units": "q^-1 or dimensionless per normalized q",
            "feeds": "WEP composition charge; clock nuclear sensitivity; R10 material qbar",
            "source_or_theorem_needed": "binding decomposition, material sensitivity matrix and no hidden binding vertex theorem",
            "current_status": "RETAIN_NONCLAIM",
            "single_component_smoke_bound": "not scored until DeltaQ_nuc or beta_A matrix is sourced",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "BML2442_3_b_bind",
            "symbol": "b_bind",
            "definition": "Lie_v ln(B_A/m_A) for isotope/material-dependent binding fraction response",
            "units": "q^-1 or dimensionless per normalized q",
            "feeds": "WEP nuclear binding correction and material response tail",
            "source_or_theorem_needed": "isotopic/material binding response owner or source-backed composition matrix",
            "current_status": "RETAIN_NONCLAIM",
            "single_component_smoke_bound": "not scored until material response matrix is sourced",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "BML2442_4_S_E_q",
            "symbol": "S_E^q",
            "definition": "Earth/source vertical drive leg converting coefficient slopes into source charges",
            "units": "normalized q amplitude for source body",
            "feeds": "D_e_source=S_E^q*b_alpha and D_mhat_source=S_E^q*b_mhat",
            "source_or_theorem_needed": "source Hamiltonian/current owner, q normalization and local screening/projection rule",
            "current_status": "MISSING_SOURCE_LEG_NONCLAIM",
            "single_component_smoke_bound": "all product bounds remain on S_E^q*b_i, not b_i alone",
            "valid_for_claim": False,
        },
    ]
    return [base_row(**row) for row in rows]


def wep_projection_rows() -> list[dict[str, Any]]:
    b_mhat_product_bound = ETA_MICROSCOPE_1SIGMA / DELTA_Q_MHAT_PT_MINUS_TI
    b_alpha_product_bound = ETA_MICROSCOPE_1SIGMA / DELTA_Q_E_PT_MINUS_TI
    rows = [
        {
            "projection_id": "WNB2442_0_current_reduced_formula",
            "formula": "eta_TiPt ~= DeltaQ_mhat*S_E^q*b_mhat + DeltaQ_e*S_E^q*b_alpha + DeltaQ_nuc*S_E^q*b_nuc + direct_delta_w_block + direct_delta_w_shadow + projector_tail_abs",
            "known_inputs": f"DeltaQ_mhat={DELTA_Q_MHAT_PT_MINUS_TI:.6e}; DeltaQ_e={DELTA_Q_E_PT_MINUS_TI:.6e}; eta_bound_1sigma={ETA_MICROSCOPE_1SIGMA:.6e}",
            "unknown_inputs": "S_E^q; b_mhat; b_alpha; b_nuc; DeltaQ_nuc; direct_delta_w_block; direct_delta_w_shadow; projector_tail_abs",
            "projection_status": "FORMULA_READY_NONCLAIM_MASS_CHANNEL_LIVE",
            "score_ready": False,
        },
        {
            "projection_id": "WNB2442_1_mass_product_smoke",
            "formula": "|S_E^q*b_mhat| <= eta_bound/|DeltaQ_mhat| if b_alpha=b_nuc=direct_delta_w=projector_tail=0",
            "known_inputs": f"eta_bound/DeltaQ_mhat={b_mhat_product_bound:.6e}",
            "unknown_inputs": "all zero premises; S_E^q separation from b_mhat",
            "projection_status": "ONE_COMPONENT_SMOKE_ONLY_NOT_MTS_CLAIM",
            "score_ready": False,
        },
        {
            "projection_id": "WNB2442_2_alpha_product_smoke",
            "formula": "|S_E^q*b_alpha| <= eta_bound/|DeltaQ_e| if b_mhat=b_nuc=direct_delta_w=projector_tail=0",
            "known_inputs": f"eta_bound/DeltaQ_e={b_alpha_product_bound:.6e}",
            "unknown_inputs": "mass-sector zero theorem and source leg",
            "projection_status": "ALPHA_ONLY_CONDITIONAL_TOO_STRONG",
            "score_ready": False,
        },
        {
            "projection_id": "WNB2442_3_no_cancellation_envelope",
            "formula": "|DeltaQ_mhat*S_E^q*b_mhat| + |DeltaQ_e*S_E^q*b_alpha| + |DeltaQ_nuc*S_E^q*b_nuc| + |direct_delta_w_block| + |direct_delta_w_shadow| + |projector_tail_abs| <= eta_bound",
            "known_inputs": "MICROSCOPE eta anchor and DD Ti/Pt mhat/e charge contrast",
            "unknown_inputs": "component magnitudes and DeltaQ_nuc/material response matrix",
            "projection_status": "NO_CANCELLATION_ENVELOPE_ONLY",
            "score_ready": False,
        },
        {
            "projection_id": "WNB2442_4_verdict",
            "formula": "WEP cannot be closed by b_alpha alone unless the mass/binding/direct/source-shadow channels are theorem-zero or bounded in the same shared local projection.",
            "known_inputs": "2441 b_alpha map plus 2440 DD material sensitivity",
            "unknown_inputs": "mass owner theorem or b_mhat/b_nuc bound rows; S_E^q",
            "projection_status": "WEP_LOCAL_GR_REMAINS_BLOCKED",
            "score_ready": False,
        },
    ]
    return [base_row(**row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2442_0_conditional_theorem", "mass-sector zero theorem has exact conditional contract", "PASS_NONCLAIM", "chain rule proof is valid if matter spectrum/binding/readout descend through q or fixed representation data", True),
        ("CG2442_1_parent_signed", "current parent action signs the mass-sector contract", "BLOCKED", "mass/Yukawa/QCD/binding/readout countervertices are not parent-forbidden", False),
        ("CG2442_2_bmhat_zero", "b_mhat can be set to zero in current framework", "BLOCKED", "zero theorem is not promoted", False),
        ("CG2442_3_bmhat_bound", "b_mhat/b_nuc can be numerically bounded as MTS coefficients", "BLOCKED", "only product smoke bounds exist and source leg/material nuclear matrix are missing", False),
        ("CG2442_4_WEP_score", "MICROSCOPE WEP can score local branch", "BLOCKED", "mass, source leg, direct source-weight and shadow channels remain open", False),
        ("CG2442_5_local_GR", "local GR/Newton limit is closed by this checkpoint", "BLOCKED", "WEP is only one local prerequisite and remains nonclaim", False),
    ]
    return [
        base_row(
            claim_id=claim_id,
            claim=claim,
            gate_status=status,
            reason=reason,
            gate_pass=gate_pass,
        )
        for claim_id, claim, status, reason, gate_pass in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC2442_0_theorem",
            "decision": "MASS_ZERO_THEOREM_ACCEPTED_ONLY_AS_CONDITIONAL_CONTRACT",
            "rationale": "the chain-rule proof is real, but the current parent action does not sign the required matter-spectrum and binding owner clauses",
            "consequence": "do not claim b_mhat=b_nuc=0",
        },
        {
            "decision_id": "DEC2442_1_gap",
            "decision": "B_MHAT_BNUC_RETAINED_AS_LIVE_COEFFICIENTS",
            "rationale": "mass/Yukawa/QCD/binding countervertices are legal under the current grammar",
            "consequence": "WEP, R10 and clock maps must carry these coefficients or prove them zero later",
        },
        {
            "decision_id": "DEC2442_2_wep",
            "decision": "ALPHA_ONLY_WEP_ROUTE_REJECTED_FOR_NOW",
            "rationale": "Ti/Pt WEP sensitivity has a larger mhat contrast than the EM contrast and direct/shadow tails still exist",
            "consequence": "WEP remains an absolute-envelope problem, not a one-channel alpha bound",
        },
        {
            "decision_id": "DEC2442_3_next",
            "decision": "TARGET_PARENT_MATTER_SPECTRUM_OWNER_SIGNATURE_OR_SOURCE_LEG_BOUND_PACK",
            "rationale": "the next leap must either sign the matter-spectrum owner contract or build real source-leg/product coefficient rows",
            "consequence": "select 2443",
        },
        {
            "decision_id": "DEC2442_4_public",
            "decision": "NO_GITHUB_ACTION",
            "rationale": "private derivation checkpoint with nonclaim rows",
            "consequence": "continue goal work privately",
        },
    ]
    return [base_row(**row) for row in rows]


def next_target_rows() -> list[dict[str, Any]]:
    row = {
        "route_id": "NEXT2442_0_selected",
        "selection_status": "selected",
        "target_file": "2443-Y5-R2FR-parent-matter-spectrum-owner-signature-or-bmhat-bnuc-source-leg-bound-pack.md",
        "target_script": "scripts/Y5_R2FR_parent_matter_spectrum_owner_signature_or_bmhat_bnuc_source_leg_bound_pack_2443.py",
        "task": "try to sign the parent matter-spectrum owner clauses that would zero b_mhat/b_nuc; if not, build source-ready nonclaim bound-product rows for S_E^q*b_mhat, S_E^q*b_nuc and shared WEP/R10/clock projections",
        "acceptance_target": "either parent matter-spectrum owner closes without hidden mass/binding/readout vertices, or retained coefficient rows have explicit source-leg/material-matrix blockers and remain valid_for_claim=false",
        "guardrails": "do not use alpha-only WEP closure; do not set source leg to 1; do not hide mass/binding in units; do not claim WEP/local GR; do not edit formalization-workbench; do not push GitHub",
    }
    return [base_row(**row)]


def copy_outputs() -> list[dict[str, Any]]:
    copy_specs = {
        "queue_zero_theorem": (OUTPUTS["zero_theorem"], COPY_TARGETS["queue_zero_theorem"], "mass zero theorem attempt nonclaim queue"),
        "queue_coefficients": (OUTPUTS["coefficient_ledger"], COPY_TARGETS["queue_coefficients"], "b_mhat/b_nuc coefficient ledger nonclaim queue"),
        "branch_wep_projection": (OUTPUTS["wep_projection"], COPY_TARGETS["branch_wep_projection"], "WEP nuclear-binding projection branch copy"),
        "beta_docs_mass_owner": (OUTPUTS["owner_audit"], COPY_TARGETS["beta_docs_mass_owner"], "mass-sector owner audit for beta docs"),
    }
    rows: list[dict[str, Any]] = []
    for copy_id, (source, target, notes) in copy_specs.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.exists():
            shutil.copyfile(source, target)
        rows.append(
            base_row(
                copy_id=copy_id,
                source_path=source,
                target_path=target,
                source_exists=source.exists(),
                target_exists=target.exists(),
                notes=notes,
            )
        )
    return rows


def validation_rows(data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, ok: bool, notes: str, detail: str = "") -> None:
        rows.append(
            {
                "check_id": check_id,
                "status": "PASS" if ok else "FAIL",
                "notes": notes,
                "detail": detail,
            }
        )

    source_rows = data["source_register"]
    theorem_rows = data["zero_theorem"]
    owner_rows = data["owner_audit"]
    coefficient_rows = data["coefficient_ledger"]
    wep_rows = data["wep_projection"]
    gate_rows = data["claim_gates"]
    next_rows = data["next_target"]
    copy_rows = data["branch_copies"]

    add("VAL2442_00_sources_exist", all(row["path_exists"] for row in source_rows), "all cited source paths exist")
    add("VAL2442_01_source_needles", all(row["needles_found"] for row in source_rows), "all cited source needles are present")
    add(
        "VAL2442_02_conditional_theorem_written",
        any(row["theorem_id"] == "MZT2442_0_setup" and row["current_status"] == "EXACT_CONDITIONAL" for row in theorem_rows),
        "mass-sector chain-rule theorem is written as an exact conditional",
    )
    add(
        "VAL2442_03_zero_not_promoted",
        any(row["theorem_id"] == "MZT2442_4_verdict" and "FAIL_CURRENT_CLAIM" in row["current_status"] for row in theorem_rows),
        "zero theorem is not promoted under current evidence",
    )
    add(
        "VAL2442_04_owner_gaps_explicit",
        all(not row["gate_pass"] for row in owner_rows if row["audit_id"] != "MSO2442_0_parent_domain"),
        "matter-spectrum, binding, source and readout gaps are explicit",
    )
    required_symbols = {"b_mhat", "b_mu", "b_nuc", "b_bind", "S_E^q"}
    found_symbols = {row["symbol"] for row in coefficient_rows}
    add("VAL2442_05_coefficient_rows_present", required_symbols <= found_symbols, "b_mhat/b_mu/b_nuc/b_bind/source-leg rows are present")
    add(
        "VAL2442_06_no_claim_coefficients",
        all(not row.get("valid_for_claim", False) for row in coefficient_rows),
        "all retained coefficient rows are nonclaim",
    )
    add(
        "VAL2442_07_wep_projection_nonclaim",
        all(not row["score_ready"] for row in wep_rows),
        "WEP projection rows are formula/smoke only, not score-ready",
    )
    add(
        "VAL2442_08_alpha_only_rejected",
        any(row["decision"] == "ALPHA_ONLY_WEP_ROUTE_REJECTED_FOR_NOW" for row in data["decisions"]),
        "alpha-only WEP closure is explicitly rejected for now",
    )
    add(
        "VAL2442_09_claim_gates_blocked",
        all((row["claim_id"] == "CG2442_0_conditional_theorem" and row["gate_status"] == "PASS_NONCLAIM") or row["gate_status"] == "BLOCKED" for row in gate_rows),
        "claim gates are blocked except the nonclaim conditional theorem",
    )
    add(
        "VAL2442_10_next_target_written",
        len(next_rows) == 1 and next_rows[0]["route_id"] == "NEXT2442_0_selected",
        "2443 parent matter-spectrum/source-leg target selected",
    )
    add(
        "VAL2442_11_branch_copies",
        all(row["source_exists"] and row["target_exists"] for row in copy_rows),
        "branch copies exist",
    )
    formalization_hits: list[Path] = []
    if FORMALIZATION.exists():
        for path in FORMALIZATION.rglob("*"):
            name = path.name
            if any(marker in name for marker in ("2442-", "_2442", "2442_", "P8_Y5_PARENT_QLOC_2442", "P8_Y5_BRR545_2442")):
                formalization_hits.append(path)
    add(
        "VAL2442_12_no_formalization_artifacts",
        len(formalization_hits) == 0,
        "no 2442 artifacts were written to formalization-workbench",
        "; ".join(str(path) for path in formalization_hits),
    )

    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        ok, count, detail = csv_parses(path)
        add(f"VAL2442_CSV_{path.stem}", ok, f"CSV parses with {count} rows", detail)

    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2442_OVERALL",
        overall,
        "2442 proves the mass-sector zero theorem only as a conditional contract, keeps b_mhat/b_nuc live, and selects the parent matter-spectrum/source-leg target next",
    )
    return rows


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    source_rows = data["source_register"]
    theorem_rows = data["zero_theorem"]
    owner_rows = data["owner_audit"]
    coefficient_rows = data["coefficient_ledger"]
    wep_rows = data["wep_projection"]
    gate_rows = data["claim_gates"]
    decision_rows_data = data["decisions"]
    next_rows = data["next_target"]
    copy_rows = data["branch_copies"]
    validation_rows_data = data["validation"]

    content = f"""# 2442 - Y5/R2FR Mass Sector Bmhat Owner Or WEP Nuclear Binding Gap

## Result
- 2442 proves the useful part: if the parent matter sector descends through the quotient or fixed representation data, then `b_mhat`, `b_mu`, `b_nuc`, and `b_bind` vanish by the chain rule.
- That proof is only a conditional contract. The current corpus still permits hidden mass/Yukawa/QCD/binding/readout coefficient vertices unless a stronger parent object-language rule forbids them.
- Therefore the WEP branch cannot be closed as alpha-only. `D_mhat_source` remains live, and the Ti/Pt WEP formula must carry mass/binding/source-leg/direct-shadow terms.
- The safe product-scale smoke bound is `|S_E^q*b_mhat| <= {ETA_MICROSCOPE_1SIGMA / DELTA_Q_MHAT_PT_MINUS_TI:.6e}` only if all other WEP channels vanish. It is not an MTS claim.
- Next target is 2443: try to sign the parent matter-spectrum owner contract or build explicit nonclaim source-leg/product coefficient rows.

## Source Register
{table(["source_id", "source_path", "path_exists", "needles_found", "role"], source_rows)}

## Mass Zero Theorem Attempt
{table(["theorem_id", "claim_piece", "mathematical_form", "proof_step", "current_status", "missing_for_claim", "if_missing", "theorem_proven_conditionally", "valid_for_claim"], theorem_rows)}

## Matter Spectrum Owner Audit
{table(["audit_id", "owner_clause", "required_form", "evidence_status", "blocks", "gap_class", "gate_pass", "valid_for_claim"], owner_rows)}

## Bmhat / Bnuc Coefficient Ledger
{table(["coefficient_id", "symbol", "definition", "units", "feeds", "source_or_theorem_needed", "current_status", "single_component_smoke_bound", "valid_for_claim"], coefficient_rows)}

## WEP Nuclear Binding Projection
{table(["projection_id", "formula", "known_inputs", "unknown_inputs", "projection_status", "score_ready", "valid_for_claim"], wep_rows)}

## Claim Gates
{table(["claim_id", "claim", "gate_status", "reason", "gate_pass", "valid_for_claim"], gate_rows)}

## Decision Ledger
{table(["decision_id", "decision", "rationale", "consequence", "valid_for_claim"], decision_rows_data)}

## Next Target
{table(["route_id", "selection_status", "target_file", "target_script", "task", "acceptance_target", "guardrails"], next_rows)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "source_exists", "target_exists", "notes"], copy_rows)}

## Validation
{table(["check_id", "status", "notes", "detail"], validation_rows_data)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    data: dict[str, list[dict[str, Any]]] = {}
    data["source_register"] = source_register_rows()
    data["zero_theorem"] = zero_theorem_rows()
    data["owner_audit"] = owner_audit_rows()
    data["coefficient_ledger"] = coefficient_ledger_rows()
    data["wep_projection"] = wep_projection_rows()
    data["claim_gates"] = claim_gate_rows()
    data["decisions"] = decision_rows()
    data["next_target"] = next_target_rows()

    for key in [
        "source_register",
        "zero_theorem",
        "owner_audit",
        "coefficient_ledger",
        "wep_projection",
        "claim_gates",
        "decisions",
        "next_target",
    ]:
        write_csv(OUTPUTS[key], data[key])

    data["branch_copies"] = copy_outputs()
    write_csv(OUTPUTS["branch_copies"], data["branch_copies"])

    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    data["validation"] = validation_rows(data)
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)


if __name__ == "__main__":
    main()
