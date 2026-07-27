from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1758"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1758 - Primitive Minimality Invariant Algebra Or Aaffine Bound"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1758_0_1757_doc",
        "source_key": "1757_handoff",
        "source_path": ROOT / "1757-Y5-R2FR-centered-origin-no-linear-marker-symmetry-proof-or-Ahidden-bound.md",
        "needles": ["PRIMITIVE_MINIMALITY_INVARIANT_ALGEBRA_IS_NEXT_BEST_ROUTE", "A_affine"],
    },
    {
        "source_id": "SRC1758_1_1757_proof_obligations",
        "source_key": "1757_proof_obligations",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_PROOF_OBLIGATIONS.csv",
        "needles": ["PO1757_3_primitive_minimality", "PO1757_4_invariant_algebra"],
    },
    {
        "source_id": "SRC1758_2_1757_Aaffine",
        "source_key": "1757_affine_bound_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1757_AFFINE_SOURCE_BOUND_ROWS.csv",
        "needles": ["ASB1757_2_A_affine", "MISSING_COMMON_ESTAR_NORM_AND_AFFINE_VALUES"],
    },
    {
        "source_id": "SRC1758_3_573_minimality",
        "source_key": "573_primitive_minimality",
        "source_path": RESIDUALS / "P8_Y5_R10_573_PRIMITIVE_MINIMAL_THEOREM_ATTEMPT.csv",
        "needles": ["PM573_1_material_marker_no_extension", "PM573_3_local_invariant_algebra"],
    },
    {
        "source_id": "SRC1758_4_573_generator_debt",
        "source_key": "573_invariant_generator_debt",
        "source_path": RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv",
        "needles": ["IG573_0_finite_fibre_spectrum", "IG573_5_readout_projector"],
    },
    {
        "source_id": "SRC1758_5_573_decision",
        "source_key": "573_decision",
        "source_path": RESIDUALS / "P8_Y5_BRR545_573_DECISION.csv",
        "needles": ["D573_1_no_promotion", "extra local invariant generators remain"],
    },
    {
        "source_id": "SRC1758_6_575_constant_source",
        "source_key": "575_constant_source_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_575_CONSTANT_SOURCE_LOCK_CONTRACT.csv",
        "needles": ["CL575_1_trivial_MTS_action", "CL575_4_universal_coupling"],
    },
    {
        "source_id": "SRC1758_7_575_decision",
        "source_key": "575_decision",
        "source_path": RESIDUALS / "P8_Y5_BRR545_575_DECISION.csv",
        "needles": ["D575_1_constant_lock_not_closed", "finite qbar_XT remains"],
    },
    {
        "source_id": "SRC1758_8_977_certificate",
        "source_key": "977_constant_source_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_977_CONSTANT_SOURCE_CERTIFICATE_ATTEMPT.csv",
        "needles": ["CSC977_7_verdict", "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED"],
    },
    {
        "source_id": "SRC1758_9_977_counterexamples",
        "source_key": "977_counterexample_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_977_COUNTEREXAMPLE_AUDIT.csv",
        "needles": ["CEA977_6_verdict", "finite qbar/source envelope remains live"],
    },
    {
        "source_id": "SRC1758_10_986_parent_zero",
        "source_key": "986_parent_zero_theorem",
        "source_path": RESIDUALS / "P8_Y5_R10_986_PARENT_ZERO_THEOREM_GATE.csv",
        "needles": ["PZT986_3_verdict", "ZERO_THEOREM_RELATIVE_NOT_PARENT_SIGNED"],
    },
    {
        "source_id": "SRC1758_11_976_gate",
        "source_key": "976_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_976_CLAIM_GATE.csv",
        "needles": ["CGATE976_2_no_linear_marker", "CGATE976_4_local_GR"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_SOURCE_REGISTER.csv",
    "primitive_minimality": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_PRIMITIVE_MINIMALITY_ATTEMPT.csv",
    "invariant_algebra": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_INVARIANT_ALGEBRA_AUDIT.csv",
    "constant_source": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_CONSTANT_SOURCE_UNIVERSALITY_AUDIT.csv",
    "aaffine_interface": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_AAFFINE_BOUND_INTERFACE.csv",
    "source_zero_status": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_SOURCE_ZERO_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_DECISION_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_CLAIM_GATE.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1758_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1758_VALIDATION.csv",
}


COPY_MAP = {
    "primitive_minimality": "R2FR_1758_PRIMITIVE_MINIMALITY_ATTEMPT.csv",
    "invariant_algebra": "R2FR_1758_INVARIANT_ALGEBRA_AUDIT.csv",
    "constant_source": "R2FR_1758_CONSTANT_SOURCE_UNIVERSALITY_AUDIT.csv",
    "aaffine_interface": "R2FR_1758_AAFFINE_BOUND_INTERFACE.csv",
    "source_zero_status": "R2FR_1758_SOURCE_ZERO_STATUS.csv",
    "decision": "R2FR_1758_DECISION_LEDGER.csv",
    "claim_gate": "R2FR_1758_CLAIM_GATE.csv",
    "next_target": "R2FR_1758_NEXT_TARGET.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("|", "\\|").replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        needles_present = all(needle in text for needle in needles)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(exists),
                "needles": "; ".join(needles),
                "needles_present": yesno(needles_present),
                "used_for": "1758 primitive minimality/invariant algebra or Aaffine bound",
                "timestamp_utc": UTC,
            }
        )
    return rows


def primitive_minimality_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PM1758_0_target",
            "claim": "primitive parent configuration has no extended marker quotient",
            "mathematical_form": "Conf_parent = Q_MTS, not Q_tilde=(Q_MTS,m)/G_rel",
            "result": "TARGET_EXACT",
            "what_it_would_buy": "co-moving material/domain markers cannot generate X0(q), ell_marker, theta_A(m), or direct qbar_XT marker charge",
            "what_remains": "parent minimality is a contract, not a theorem forbidding all quotient extensions",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PM1758_1_fixed_spurions",
            "claim": "fixed external labels are excluded",
            "mathematical_form": "m_fixed is not a function on Q=Phi/G_rep",
            "result": "CONDITIONAL_PASS_IF_STRICT_QUOTIENT",
            "what_it_would_buy": "fixed non-orbit covectors cannot source X",
            "what_remains": "does not exclude co-moving material markers or quotient-invariant class scalars",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PM1758_2_material_marker_no_extension",
            "claim": "co-moving material markers are forbidden",
            "mathematical_form": "no natural extension Q_tilde=(Q_MTS,m)/G_rel with m carrying material/domain/source data",
            "result": "NOT_DERIVED",
            "what_it_would_buy": "would remove theta_A(m(X)), direct marker covectors, and some qbar_XT source charges",
            "what_remains": "current corpus has a minimality contract but no theorem excluding extended quotient objects",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PM1758_3_no_natural_marker_functor",
            "claim": "no nonconstant marker functor on local branch",
            "mathematical_form": "Nat(Q_MTS,Marker)_loc = constants",
            "result": "REDUCED_TO_INVARIANT_ALGEBRA_TRIVIALITY",
            "what_it_would_buy": "partial_X theta_A=0 if constants factor through marker-free functors",
            "what_remains": "local invariant algebra still has uneliminated candidate generators",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "PM1758_4_promotion",
            "claim": "primitive minimality promotes A_shift=A_marker=0",
            "mathematical_form": "primitive minimality + no marker functors + no invariant dual => X0=0 and ell_marker=0",
            "result": "BLOCKED_FOR_CLAIM",
            "what_it_would_buy": "would close the leading affine F_1 obstruction",
            "what_remains": "primitive minimality and invariant algebra triviality are not parent-derived",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def invariant_algebra_rows() -> list[dict[str, Any]]:
    debts = [
        ("IA1758_0_target", "target algebra", "I_loc(Q_MTS)=I_geom[J^k(e_obs)] tensor Const", "TARGET_EXACT", "would block local marker functors", "MISSING_LOCAL_INVARIANT_ALGEBRA_TRIVIALITY"),
        ("IA1758_1_fibre", "finite_cell_fibre_spectrum", "finite fibre spectrum can act as material/source marker or effective charge label", "NOT_TRIVIALIZED", "can build ell_marker or source weights", "MISSING_FIBRE_SPECTRUM_UNIVERSAL_OR_GAUGE_PROOF"),
        ("IA1758_2_domain_class", "relative_boundary_domain_class", "relative/domain class can carry local source/class marker", "NOT_DERIVED", "can create boundary/domain charge", "MISSING_LOCAL_TRIVIAL_CLASS_OR_CLASS_NOHAIR"),
        ("IA1758_3_chiD", "chi_D/domain_selector", "domain selector can become preferred-frame/source-normalization/R10/R11 marker", "NOT_DERIVED", "can create source/projector dependence", "MISSING_SELECTOR_GAUGE_OR_LOCAL_TRIVIAL_BRANCH"),
        ("IA1758_4_memory_scalar", "memory_or_class_scalar", "memory/class scalar can enter clock/source/fifth-force channels", "NOT_SILENCED_AS_THEOREM", "can generate ell_marker or A_mu_even", "MISSING_LOCAL_VALUE_GRADIENT_ZERO_OR_BOUND"),
        ("IA1758_5_species_constants", "species_charge_constants", "species constants can act as WEP/source-charge/clock markers", "NOT_UNIVERSALIZED", "can generate theta_A(X), kappa_A, and source weights", "MISSING_CONSTANT_SOURCE_UNIVERSALITY"),
        ("IA1758_6_readout_projector", "post_readout_projector", "post-readout projector can re-enter as reduced-action source if not kept after variation", "NO_CHEAT_RULE_ONLY", "fake closure zeros can become EFT sources", "MISSING_FULL_PARENT_DOMAIN_READOUT_AUDIT"),
    ]
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "generator": generator,
            "risk": risk,
            "current_status": status,
            "damage_if_survives": damage,
            "needed_elimination": needed,
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        }
        for audit_id, generator, risk, status, damage, needed in debts
    ]


def constant_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CS1758_0_representation_data",
            "required_clause": "matter constants are representation/superselection data",
            "mathematical_form": "theta_A in Rep_A, not theta_A(X,I_Q,m,h)",
            "current_status": "VALID_RELATIVE_THEOREM",
            "blocks_if_missing": "constants become local MTS marker channels",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CS1758_1_trivial_MTS_action",
            "required_clause": "MTS selectors/invariants/markers/memory/fibre directions act trivially on constants",
            "mathematical_form": "L_X theta_A=L_IQ theta_A=L_m theta_A=L_h theta_A=0",
            "current_status": "NOT_PARENT_DERIVED",
            "blocks_if_missing": "theta_A(I_Q), theta_A(m), theta_A(h) counterexamples remain legal",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CS1758_2_no_direct_constant_vertices",
            "required_clause": "no direct MTS-dependent matter constants",
            "mathematical_form": "no alpha_EM(X)F^2, no m_A(X), no q_A X_mu J_A^mu",
            "current_status": "FORBIDDEN_VERTEX_POLICY_ONLY",
            "blocks_if_missing": "clock, WEP, and fifth-force residuals return",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CS1758_3_Hilbert_source",
            "required_clause": "ordinary active source is the Hilbert/coframe current",
            "mathematical_form": "tau_a^mu=det(e)^-1 delta S_m/delta e_mu^a",
            "current_status": "CONDITIONAL_STANDARD_IDENTITY",
            "blocks_if_missing": "source current can be fitted/readout-defined",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CS1758_4_universal_kappa",
            "required_clause": "field equation uses one universal coupling for Hilbert current",
            "mathematical_form": "E_munu=kappa_univ T_munu, not sum_A kappa_A T_A_munu",
            "current_status": "NOT_PARENT_DERIVED",
            "blocks_if_missing": "species-weighted active source charge remains",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CS1758_5_Bianchi_limit",
            "required_clause": "do not overclaim Bianchi",
            "mathematical_form": "nabla_mu E^{mu nu}=0 exposes grad(kappa) residual unless no-exchange/source owner closes",
            "current_status": "OVERCLAIM_BLOCKER_RETAINED",
            "blocks_if_missing": "Bianchi can hide exchange/source terms by notation",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "CS1758_6_verdict",
            "required_clause": "constant/source universality certificate",
            "mathematical_form": "theta_A fixed representation data + one global kappa + Hilbert current => b_theta=b_kappa=0",
            "current_status": "RELATIVE_CERTIFICATE_READY_PARENT_UNSIGNED",
            "blocks_if_missing": "finite qbar/source envelope remains live",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
    ]


def aaffine_interface_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AAI1758_0_zero_condition",
            "quantity": "Z_affine",
            "required_form": "Z_affine=True only if primitive minimality, invariant algebra triviality, no trivial dual, and constant/source universality all pass",
            "current_status": "FALSE_PARENT_UNSIGNED",
            "formula": "Z_affine = Z_shift and Z_marker",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1757_AFFINE_SOURCE_BOUND_ROWS.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AAI1758_1_A_shift",
            "quantity": "A_shift",
            "required_form": "||L_X X0(q)||_{E*}, or theorem-zero from parent zero section",
            "current_status": "MISSING_CENTERED_ORIGIN_ZERO_OR_A_SHIFT",
            "formula": "A_shift >= 0 in declared E* norm",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1757_AFFINE_SOURCE_BOUND_ROWS.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AAI1758_2_A_marker",
            "quantity": "A_marker",
            "required_form": "||ell_marker||_{E*}, or theorem-zero from no-marker package",
            "current_status": "MISSING_NO_MARKER_THEOREM_OR_A_MARKER",
            "formula": "A_marker <= A_fibre + A_domain + A_chiD + A_memory + A_species + A_readout",
            "source_path": str(RESIDUALS / "P8_Y5_R10_573_INVARIANT_GENERATOR_DEBT.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AAI1758_3_A_affine",
            "quantity": "A_affine",
            "required_form": "A_affine <= A_shift + A_marker in one declared E* norm",
            "current_status": "MISSING_COMMON_ESTAR_NORM_AND_COMPONENT_VALUES",
            "formula": "||J_affine||_{E*} <= A_affine",
            "source_path": "AAI1758_1_A_shift; AAI1758_2_A_marker",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "interface_id": "AAI1758_4_R_affine",
            "quantity": "R_affine",
            "required_form": "||R_affine|| <= ||P_arena L_X^{-1}|| A_affine with declared operator/projection norms",
            "current_status": "MISSING_OPERATOR_INVERSE_ARENA_PROJECTION_AND_UNITS",
            "formula": "source residual response to affine hidden current",
            "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1757_AFFINE_SOURCE_BOUND_ROWS.csv"),
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def source_zero_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1758_0_affine",
            "quantity": "J_affine",
            "current_status": "NOT_ZEROED",
            "evidence": "primitive minimality and invariant algebra triviality fail current claim",
            "remaining_gap": "A_shift, A_marker, A_affine remain missing/nonclaim",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1758_1_marker_package",
            "quantity": "marker/source package",
            "current_status": "REDUCED_TO_NAMED_GENERATOR_DEBTS",
            "evidence": "finite fibre, domain class, chi_D, memory scalar, species constants, readout projector retained",
            "remaining_gap": "eliminate each generator or bound its marker covector",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "SZ1758_2_source_silence",
            "quantity": "S_cg(D_L=0,Y)",
            "current_status": "NOT_DERIVED",
            "evidence": "affine source not zeroed and other hidden channels remain from 1756",
            "remaining_gap": "J_hidden not zero; coupling chain is next derivation target",
            "claim_allowed": no(),
            "valid_for_claim": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1758_0_minimality",
            "decision": "PRIMITIVE_MINIMALITY_NOT_PROVED",
            "reason": "fixed spurions can be excluded conditionally, but co-moving material/domain markers and quotient extensions remain legal",
            "next_action": "do not set A_shift or A_marker to zero from minimality",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1758_1_invariant_algebra",
            "decision": "LOCAL_INVARIANT_ALGEBRA_NOT_TRIVIALIZED",
            "reason": "finite fibre spectrum, relative/domain class, chi_D, memory scalar, species constants, and readout projector generators remain",
            "next_action": "retain A_marker component rows or eliminate generators one by one",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1758_2_constant_source",
            "decision": "CONSTANT_SOURCE_UNIVERSALITY_RELATIVE_NOT_PARENT_SIGNED",
            "reason": "representation-data and universal-kappa route is coherent but not derived from primitives",
            "next_action": "keep WEP/clock/source-normalization source envelope live",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1758_3_Aaffine",
            "decision": "A_AFFINE_INTERFACE_WRITTEN_NONCLAIM",
            "reason": "the zero theorem failed, so A_shift/A_marker/A_affine must remain explicit residual inputs",
            "next_action": "do not claim F_1=0; use the interface if a numerical/nonclaim source-envelope pass is needed",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1758_4_best_next",
            "decision": "COUPLING_CHAIN_SOURCE_IS_NEXT_BEST_DERIVATION_ROUTE",
            "reason": "affine source is now fully named and nonclaim; the next hidden source in J_hidden is the coupling-chain term f'(0) C_obs partial_X chi_D",
            "next_action": "build 1759 coupling-chain source double-zero proof or A_chain bound",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1758_0_primitive_minimality",
            "claim": "primitive minimality forbids all marker quotient extensions",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_CO_MOVING_MARKER_AND_QUOTIENT_EXTENSION_THEOREM_MISSING",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1758_1_invariant_algebra",
            "claim": "local invariant algebra has no marker/source generators",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_GENERATOR_DEBTS_RETAINED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1758_2_constant_source",
            "claim": "matter constants and source weights are universally source-blind",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_CONSTANT_SOURCE_UNIVERSALITY_PARENT_SIGNATURE",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1758_3_Aaffine_zero",
            "claim": "A_affine=0",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_A_SHIFT_A_MARKER_ZERO_THEOREMS_NOT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "GATE1758_4_local_GR_Newton",
            "claim": "local GR/Newton/PPN/R10/WEP/clock/orbital branch can claim",
            "gate_pass": no(),
            "status": "BLOCKED",
            "blocker": "BLOCKED_AFFINE_AND_OTHER_HIDDEN_SOURCE_CHANNELS_ACTIVE",
            "claim_allowed": no(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1758_0_primary",
            "next_target": "1759-Y5-R2FR-coupling-chain-source-double-zero-proof-or-Achain-bound.md",
            "script": "scripts/Y5_R2FR_coupling_chain_source_double_zero_proof_or_Achain_bound.py",
            "objective": "try to derive f(0)=f'(0)=0 or delta_X chi_D=0 at the local fixed point; otherwise carry A_chain as a finite nonclaim residual",
            "success_condition": "observable coupling chain source is theorem-zero or becomes an explicit finite residual row",
            "selection_status": "selected",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1758_1_fallback",
            "next_target": "1759b-Y5-R2FR-Aaffine-E-star-bound-runner.md",
            "script": "scripts/Y5_R2FR_Aaffine_E_star_bound_runner.py",
            "objective": "turn A_shift/A_marker/A_affine into a runnable nonclaim source-envelope interface with units and operator/projection norms",
            "success_condition": "A_affine rows parse with declared E* units, sources, and valid_for_claim=false until bounds pass",
            "selection_status": "held_fallback",
            "score_ready": no(),
            "valid_prediction_row": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "primitive_minimality": primitive_minimality_rows(),
        "invariant_algebra": invariant_algebra_rows(),
        "constant_source": constant_source_rows(),
        "aaffine_interface": aaffine_interface_rows(),
        "source_zero_status": source_zero_status_rows(),
        "decision": decision_rows(),
        "claim_gate": claim_gate_rows(),
        "next_target": next_target_rows(),
    }


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1758_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1758_{key.upper()}.csv")


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                if row.get(field) == "True":
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values())
            if "MISSING_" in text:
                for field in ("score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"):
                    if row.get(field) == "True":
                        return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1758_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1758_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1758*"):
        path_text = str(path)
        if "\\.venv\\" in path_text or "\\__pycache__\\" in path_text:
            continue
        if path.is_file():
            return False
    return True


def minimality_not_proved(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["attempt_id"] == "PM1758_2_material_marker_no_extension"
        and row["result"] == "NOT_DERIVED"
        for row in rows_map["primitive_minimality"]
    )


def generator_debts_retained(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return sum(
        1
        for row in rows_map["invariant_algebra"]
        if row["current_status"] in {"NOT_TRIVIALIZED", "NOT_DERIVED", "NOT_SILENCED_AS_THEOREM", "NOT_UNIVERSALIZED", "NO_CHEAT_RULE_ONLY"}
    ) >= 5


def aaffine_interface_nonclaim(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    rows = rows_map["aaffine_interface"]
    return len(rows) >= 5 and all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in rows)


def source_zero_blocked(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["status_id"] == "SZ1758_2_source_silence"
        and row["current_status"] == "NOT_DERIVED"
        for row in rows_map["source_zero_status"]
    )


def next_selected(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    return any(
        row["route_id"] == "NEXT1758_0_primary"
        and row["selection_status"] == "selected"
        for row in rows_map["next_target"]
    )


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    sources = rows_map["source_register"]
    claims = rows_map["claim_gate"]

    validation = [
        check("VAL1758_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1758_1_needles_present", all(row["needles_present"] == "True" for row in sources), "required source needles are present", "one or more source needles missing"),
        check("VAL1758_2_minimality_not_proved", minimality_not_proved(rows_map), "primitive minimality remains unproved", "minimality verdict missing or promoted"),
        check("VAL1758_3_generator_debts_retained", generator_debts_retained(rows_map), "invariant-generator debts retained", "generator debt ledger incomplete or promoted"),
        check("VAL1758_4_aaffine_interface_nonclaim", aaffine_interface_nonclaim(rows_map), "A_affine interface remains nonclaim", "A_affine interface missing or promoted"),
        check("VAL1758_5_source_zero_blocked", source_zero_blocked(rows_map), "source-zero status remains blocked", "source-zero status missing or promoted"),
        check("VAL1758_6_claim_gates_safe", all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claims), "all claim gates remain blocked", "one or more claim gates opened"),
        check("VAL1758_7_no_claim_flags", no_claim_flags(rows_map), "claim/no-score flags stay false", "one or more claim/no-score flags enabled"),
        check("VAL1758_8_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready", "a MISSING_* row is marked ready"),
        check("VAL1758_9_decision_next", any(row["decision_id"] == "DEC1758_4_best_next" and row["decision"] == "COUPLING_CHAIN_SOURCE_IS_NEXT_BEST_DERIVATION_ROUTE" for row in rows_map["decision"]), "decision selects coupling-chain source route", "best-next decision missing"),
        check("VAL1758_10_next_selected", next_selected(rows_map), "next target selected", "next target missing"),
        check("VAL1758_11_csv_parse", parsed_ok, "all generated 1758 CSVs parse", "one or more generated 1758 CSVs failed to parse"),
        check("VAL1758_12_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1758_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1758_14_formalization_untouched", formalization_untouched(), "no 1758 outputs found under formalization-workbench", "1758 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1758_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1758 primitive minimality/invariant algebra or Aaffine bound" if overall else "one or more 1758 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1758 tries the common parent package behind `A_shift=0` and `A_marker=0`: primitive minimality plus local invariant-algebra triviality.",
        "- Fixed external spurions can be excluded conditionally by strict quotient logic, but co-moving material/domain markers and quotient extensions are not parent-forbidden.",
        "- The local invariant algebra is not trivialized: finite fibre spectrum, relative/domain class, `chi_D`, memory scalar, species constants, and readout projector debts remain.",
        "- Constant/source universality is coherent as a relative theorem, but not parent-signed; WEP/clock/source-normalization envelopes remain live.",
        "- Therefore `A_affine` is not zero-claimed; it remains an explicit nonclaim source interface.",
        "- No GitHub, public, local-GR, Newton, PPN, WEP, clock, orbital, R10, or `q_loc=0` claim is made.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Primitive Minimality Attempt",
        markdown_table(rows_map["primitive_minimality"], ["attempt_id", "claim", "mathematical_form", "result", "what_it_would_buy", "what_remains"]),
        "",
        "## Invariant Algebra Audit",
        markdown_table(rows_map["invariant_algebra"], ["audit_id", "generator", "risk", "current_status", "damage_if_survives", "needed_elimination"]),
        "",
        "## Constant/Source Universality Audit",
        markdown_table(rows_map["constant_source"], ["clause_id", "required_clause", "mathematical_form", "current_status", "blocks_if_missing"]),
        "",
        "## A-affine Bound Interface",
        markdown_table(rows_map["aaffine_interface"], ["interface_id", "quantity", "required_form", "current_status", "formula"]),
        "",
        "## Source-Zero Status",
        markdown_table(rows_map["source_zero_status"], ["status_id", "quantity", "current_status", "evidence", "remaining_gap"]),
        "",
        "## Decisions",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1758 does not give the miracle, but it makes the failure productive. The affine-source zero theorem now has a precise parent package, and that package fails at named places rather than in fog: quotient extensions, invariant generators, and constant/source universality. Since the affine channel is now ledgered as `A_affine`, the next derivation-first move is the coupling-chain source: prove the coupling cannot inject `J_X` at the local fixed point, or carry `A_chain` explicitly.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1758-Y5-R2FR-primitive-minimality-invariant-algebra-or-Aaffine-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1758_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1758 validation FAIL")
    print("1758 validation PASS")


if __name__ == "__main__":
    main()
